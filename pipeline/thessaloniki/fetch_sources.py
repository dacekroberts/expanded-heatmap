"""Download everything Thessaloniki's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/thessaloniki/fetch_sources.py [--refresh-wfs] [--force-osm]

  * the City's active-shop-licence layer: the brief's ONE WFS 2.0.0
    GetFeature, from sdi.thessaloniki.gr's GeoServer only (never
    maps.thessaloniki.gr). The cached file is kept and its sha256 checked
    against the meta JSON beside it; --refresh-wfs repeats the request, and
    an answer whose numberReturned is under numberMatched is refused;
  * OpenStreetMap: Line 1's route relations with their stop nodes, the
    station objects and the municipalities in the box, in ONE Overpass query
    (osm-rail: one query per city) through pipeline/osm.py, then split into
    the three files step 1 reads (Gimhae's shape). No query is sent while the
    cache exists; --force-osm sends it again.

Each file is recorded in outputs/thessaloniki/provenance.json.
"""
import datetime as dt
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.thessaloniki import config  # noqa: E402

USER_AGENT = "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"
PROV = {}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_wfs(refresh=False):
    """The one GetFeature. Kept from cache unless refresh is asked for."""
    dest, meta_path = config.LICENCES_GEOJSON, config.LICENCES_META
    if refresh or not dest.exists():
        print(f"  GET {config.WFS_URL}")
        req = urllib.request.Request(config.WFS_URL, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=300) as r:
            body = r.read()
            ctype = r.headers.get("Content-Type")
        payload = json.loads(body.decode("utf-8"))
        matched, returned = payload.get("numberMatched"), payload.get("numberReturned")
        feats = payload.get("features") or []
        if matched is None or returned is None or int(returned) < int(matched) \
                or len(feats) != int(matched):
            sys.exit(f"WFS answer refused: numberMatched {matched}, numberReturned {returned}, "
                     f"{len(feats)} features - one request must carry every row")
        lo, hi = config.LICENCES_ROWS
        if not lo <= len(feats) <= hi:
            sys.exit(f"{len(feats)} rows, outside {lo}-{hi}: re-measure the buckets before "
                     f"caching it (the brief's rows check)")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        meta_path.write_text(json.dumps({
            "url": config.WFS_URL, "fetched": dt.date.today().isoformat(),
            "bytes": len(body), "sha256": sha256(dest), "rows": len(feats),
            "content_type": ctype,
            "approved": "owner, 2026-10-04 (Thessaloniki to B; the brief's named source)",
            "licence": "CC BY 4.0, data.gov.gr record "
                       "gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton "
                       "(read 2026-10-04)"}, ensure_ascii=False), encoding="utf-8")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    got = sha256(dest)
    if got != meta["sha256"]:
        sys.exit(f"{dest.name}: sha256 {got} is not the meta's {meta['sha256']} - the cache "
                 f"changed outside this script")
    print(f"  {dest.name:48s} {dest.stat().st_size:>11,} bytes  {meta['rows']:,} rows  "
          f"fetched {meta['fetched']}")
    PROV["licences"] = {"file": dest.name, "url": meta["url"], "page": config.DATASET_PAGE,
                        "licence": config.LICENCE_URL, "bytes": meta["bytes"],
                        "sha256": meta["sha256"], "rows": meta["rows"],
                        "retrieved": meta["fetched"], "data_date": None}


def split(els):
    """The one answer as the three files step 1 reads: route relations with
    their member nodes; station objects; the boundary relations."""
    routes = [e for e in els if e["type"] == "relation" and e.get("tags", {}).get("type") == "route"]
    member_ids = {m["ref"] for r in routes for m in r.get("members", []) if m["type"] == "node"}
    rail, seen = list(routes), set()
    for e in els:
        if e["type"] == "node" and e["id"] in member_ids and e["id"] not in seen and "lat" in e:
            rail.append(e)
            seen.add(e["id"])
    stations, seen = [], set()
    for e in els:
        if e["type"] in ("node", "way") and e.get("tags", {}).get("railway") == "station":
            if (e["type"], e["id"]) not in seen and ("lat" in e or "center" in e):
                stations.append(e)
                seen.add((e["type"], e["id"]))
    boundary = [e for e in els if e["type"] == "relation"
                and e.get("tags", {}).get("boundary") == "administrative"]
    return rail, stations, boundary


def fetch_osm(force=False):
    s, w, n, e = config.OSM_BBOX
    box = f"({s},{w},{n},{e})"
    levels = "|".join(config.BOUNDARY_ADMIN_LEVELS)
    # Metro relations by ROUTE TYPE, never by network (osm-rail); no
    # route=train, so the suburban railway's geometry is not pulled. The
    # municipalities by admin level inside the box (a bounded search, never a
    # global one by name); step 1 picks the city by name and level and checks
    # its area.
    q = (f'[out:json][timeout:180];'
         f'relation["type"="route"]["route"~"^(subway|light_rail)$"]{box}->.r;'
         f'(node["railway"="station"]{box};way["railway"="station"]{box};)->.s;'
         f'relation["boundary"="administrative"]["admin_level"~"^({levels})$"]{box}->.b;'
         f'.r out geom;node(r.r);out body;.s out tags center;.b out geom;')
    els, host = osm.fetch(q, config.OSM_ALL_JSON, force=force, timeout=240)
    payload = json.loads(config.OSM_ALL_JSON.read_text(encoding="utf-8"))
    base = payload.get("osm3s", {}).get("timestamp_osm_base")
    PROV["osm"] = {"file": config.OSM_ALL_JSON.name, "host": host, "query": q,
                   "bytes": config.OSM_ALL_JSON.stat().st_size,
                   "sha256": sha256(config.OSM_ALL_JSON), "osm_base": base}
    for key, part, dest in zip(("osm_rail", "osm_station_names", "osm_boundary"), split(els),
                               (config.RAIL_OSM_JSON, config.STATION_OSM_JSON,
                                config.BOUNDARY_OSM_JSON)):
        if not part:
            sys.exit(f"the OSM answer holds nothing for {dest.name} - an empty part is not "
                     f"an empty city")
        dest.write_bytes(json.dumps({"osm3s": payload.get("osm3s", {}), "elements": part},
                                    ensure_ascii=False).encode("utf-8"))
        kinds = {}
        for el in part:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        print(f"  {dest.name:28s} {dest.stat().st_size:>11,} bytes  {kinds}  via {host}")
        PROV[key] = {"file": dest.name, "split_from": config.OSM_ALL_JSON.name,
                     "bytes": dest.stat().st_size, "sha256": sha256(dest), "elements": kinds,
                     "osm_base": base}


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    fetch_wfs(refresh="--refresh-wfs" in sys.argv)
    fetch_osm(force="--force-osm" in sys.argv)
    config.PROVENANCE_JSON.write_text(json.dumps(PROV, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8", newline="\n")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
