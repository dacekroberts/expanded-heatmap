"""Download Gelsenkirchen's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/gelsenkirchen/fetch_sources.py [--survey] [--skip-osm]

  * The City's commercial-premises survey: the three themed layers of the
    Infrastrukturdatenbank by WFS 2.0, ONLY the properties in
    config.WFS_PROPERTIES (owner, 2026-10-05, call 5), paged at
    config.WFS_PAGE and sorted on `id`, in the survey's own EPSG:25832. KEPT,
    not re-taken, unless --survey is given: the city edits the layers, and the
    map states the fetch date of the files it was built from. A cached file
    whose sha256 differs from its record stops the script. The full copies of
    2026-10-04 (gewerbe_*.geojson) are never touched.
  * OpenStreetMap: every tram, light-rail and subway route relation with a
    member in the city's box, its member nodes, the box's tram stop nodes,
    and the boundaries of the city and its neighbours, in ONE Overpass
    query (osm-rail: one query per city, one in flight per session), split
    into the two files step 1 reads. Rolling, so re-taken on every run unless
    --skip-osm is given.

Each file is recorded in outputs/gelsenkirchen/provenance.json.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.gelsenkirchen import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _get_layer(layer):
    """Every row of one layer, the requested properties only, paged."""
    feats, urls, crs, matched = [], [], None, None
    start = 0
    while True:
        params = {"service": "WFS", "version": "2.0.0", "request": "GetFeature",
                  "typeNames": f"{config.WFS_NAMESPACE}:{layer}",
                  "propertyName": ",".join(config.WFS_PROPERTIES),
                  "outputFormat": "application/json", "srsName": config.CRS_SURVEY,
                  "sortBy": "id", "count": config.WFS_PAGE, "startIndex": start}
        r = requests.get(config.WFS_URL, params=params, headers=HEADERS, timeout=180)
        r.raise_for_status()
        if "json" not in (r.headers.get("content-type") or ""):
            sys.exit(f"  {layer}: the WFS answered {r.headers.get('content-type')}, not JSON "
                     f"- nothing written")
        j = r.json()
        urls.append(r.url)
        crs = crs or j.get("crs")
        matched = j.get("numberMatched", j.get("totalFeatures"))
        page = j.get("features") or []
        feats.extend(page)
        start += len(page)
        if not page or start >= int(matched):
            break
    return feats, urls, crs, int(matched)


def fetch_survey(force=False):
    """The three reduced layers, fetched once and verified thereafter."""
    if force or not config.SURVEY_META.exists() or not all(
            p.exists() for p in config.SURVEY_FILES.values()):
        meta = {"source": "Stadt Gelsenkirchen, Infrastrukturdatenbank (GeoServer WFS 2.0)",
                "wfs": config.WFS_URL, "licence": "dl-zero-de/2.0", "licence_url": config.LICENCE_URL,
                "properties": list(config.WFS_PROPERTIES), "fetched_utc": _now(), "files": []}
        for layer in config.LAYERS:
            feats, urls, crs, matched = _get_layer(layer)
            lo, hi = config.SURVEY_ROWS[layer]
            if len(feats) != matched or not lo <= matched <= hi:
                sys.exit(f"  {layer}: {len(feats)} features of {matched} matched, expected "
                         f"{lo}-{hi} - nothing written")
            extra = sorted({k for f in feats for k in f.get("properties", {})}
                           - set(config.WFS_PROPERTIES) - {"Veroeffentlicht", "Istonline"})
            if extra:
                sys.exit(f"  {layer}: the WFS returned properties not requested: {extra} - "
                         f"nothing written")
            dest = config.SURVEY_FILES[layer]
            body = {"type": "FeatureCollection", "crs": crs, "numberMatched": matched,
                    "features": feats}
            dest.write_bytes(json.dumps(body, ensure_ascii=False).encode("utf-8"))
            meta["files"].append({"layer": layer, "file": dest.name, "numberMatched": matched,
                                  "features": len(feats), "request_urls": urls,
                                  "bytes": dest.stat().st_size, "sha256": sha256(dest)})
            print(f"  {layer}: {len(feats):,} rows -> {dest.name}")
        config.SURVEY_META.write_bytes(
            (json.dumps(meta, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    meta = json.loads(config.SURVEY_META.read_text(encoding="utf-8"))
    for rec in meta["files"]:
        path = config.DATA_RAW / rec["file"]
        if sha256(path) != rec["sha256"]:
            sys.exit(f"  {rec['file']}: sha256 differs from its record - re-fetch with --survey")
        print(f"  {rec['layer']}: {rec['features']:,} rows, {rec['bytes']:,} bytes (verified)")
    return {"wfs": meta["wfs"], "licence": meta["licence"], "licence_url": meta["licence_url"],
            "properties": meta["properties"], "fetched_utc": meta["fetched_utc"],
            "files": [{k: rec[k] for k in ("layer", "file", "features", "bytes", "sha256")}
                      for rec in meta["files"]]}


def split(els):
    """The one answer as the two files step 1 reads: route relations with
    their member nodes and the city's tram stop nodes; the boundaries."""
    bnd = [e for e in els if e["type"] == "relation"
           and e.get("tags", {}).get("boundary") == "administrative"]
    ids = {e["id"] for e in bnd}
    rail = [e for e in els if not (e["type"] == "relation" and e["id"] in ids)]
    return rail, bnd


def fetch_osm():
    # A bbox, not an area filter or is_in: the area form drew 504s from
    # overpass-api.de and an empty 200 from kumi.systems on 2026-10-07, and
    # the boundaries are named by their municipality keys instead.
    s, w, n, e = config.RAIL_BBOX
    box = f"({s},{w},{n},{e})"
    keys = "|".join(config.PLACE_AGS)
    q = ("[out:json][timeout:180];"
         f'relation["type"="route"]["route"~"^(tram|light_rail|subway)$"]{box}->.r;'
         f'relation["boundary"="administrative"]["{config.AGS_TAG}"~"^({keys})$"]->.b;'
         ".r out geom;"
         f'(node(r.r);node["railway"="tram_stop"]{box};);out body;'
         ".b out geom;")
    els, host = osm.fetch(q, config.OSM_ALL_JSON, force=True, timeout=240)
    payload = json.loads(config.OSM_ALL_JSON.read_text(encoding="utf-8"))
    rail, bnd = split(els)
    rels = [x for x in rail if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no relations, or one without members - a FAILED fetch")
    if not any(b.get("tags", {}).get(config.AGS_TAG) == config.CITY_AGS for b in bnd):
        sys.exit(f"  boundaries: no relation tagged {config.AGS_TAG}={config.CITY_AGS} - "
                 f"a FAILED fetch")
    for part, dest in ((rail, config.OSM_ROUTES_JSON), (bnd, config.OSM_BOUNDARIES_JSON)):
        dest.write_bytes(json.dumps({"osm3s": payload.get("osm3s", {}), "elements": part},
                                    ensure_ascii=False).encode("utf-8"))
    print(f"  rail: {len(rels)} relations; boundaries: {len(bnd)}; via {host}")
    return {"host": host, "query": q,
            "osm_base": payload.get("osm3s", {}).get("timestamp_osm_base"),
            "sha256": sha256(config.OSM_ALL_JSON)}


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    prov = {}
    if config.PROVENANCE_JSON.exists():
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    print("Stadt Gelsenkirchen, commercial-premises survey (dl-de/zero-2.0):")
    prov["survey"] = fetch_survey(force="--survey" in sys.argv)
    if "--skip-osm" not in sys.argv:
        print("\nOpenStreetMap (keyless):")
        prov["osm"] = fetch_osm()
        prov["osm_fetched_utc"] = datetime.fromtimestamp(
            config.OSM_ALL_JSON.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")
    prov["written_utc"] = _now()
    # LF on Windows too: the file is committed.
    config.PROVENANCE_JSON.write_bytes(
        (json.dumps(prov, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
