"""Download Den Haag's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/den_haag/fetch_sources.py [--force]

Keyless downloads. The permit layer and the BAG are re-taken on every run (the
BAG is updated daily; the permit layer's own edit date is recorded); OSM is
cached and re-fetched with --force. Overpass queries run one at a time.

THE PERMIT LAYER IS ASKED FOR BY FIELD NAME (config.HORECA_FIELDS). The
applicant, KvK number and legal form are never requested, and the fetch stops,
writing nothing, if any of them arrives.
"""
import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.den_haag import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
PAUSE_S = 1.0


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _get_json(url, params, tries=4):
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=180)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            if attempt == tries - 1:
                raise SystemExit(f"  {url[:100]}: {type(e).__name__}: {e}")
            time.sleep(10 * (attempt + 1))


def fetch_horeca():
    meta = _get_json(config.HORECA_URL, {"f": "json"})
    if meta.get("name") != "Horecavergunningen":
        sys.exit(f"  the layer is now {meta.get('name')!r}, not 'Horecavergunningen' - re-read it")
    served = {f["name"] for f in meta.get("fields", [])}
    missing = sorted(set(config.HORECA_FIELDS) - served)
    if missing:
        sys.exit(f"  the layer no longer serves {missing} - re-read its schema")
    edited = (meta.get("editingInfo") or {}).get("dataLastEditDate")
    feats, off = [], 0
    while True:
        page = _get_json(config.HORECA_URL + "/query", {
            "where": "1=1", "outFields": ",".join(config.HORECA_FIELDS), "outSR": "4326",
            "orderByFields": "FID", "resultOffset": off,
            "resultRecordCount": config.HORECA_PAGE, "f": "json"})
        if "error" in page:
            sys.exit(f"  query error: {page['error']}")
        got = page.get("features") or []
        feats.extend(got)
        off += len(got)
        if not got or (not page.get("exceededTransferLimit") and len(got) < config.HORECA_PAGE):
            break
        time.sleep(PAUSE_S)
    arrived = set().union(*[f["attributes"].keys() for f in feats]) if feats else set()
    leaked = sorted(arrived & set(config.HORECA_FORBIDDEN))
    if leaked:
        sys.exit(f"  the layer returned {leaked}, which were not asked for - nothing written")
    extra = sorted(arrived - set(config.HORECA_FIELDS))
    if extra:
        sys.exit(f"  the layer returned fields not asked for: {extra} - nothing written")
    count = _get_json(config.HORECA_URL + "/query",
                      {"where": "1=1", "returnCountOnly": "true", "f": "json"}).get("count")
    if len(feats) != count or len(feats) < config.HORECA_MIN_ROWS:
        sys.exit(f"  {len(feats):,} features read against {count} reported - a failed fetch")
    fids = [f["attributes"]["FID"] for f in feats]
    if len(set(fids)) != len(fids):
        sys.exit("  duplicate FIDs across pages - the paging is not stable")
    config.HORECA_JSON.write_text(json.dumps(feats, ensure_ascii=False), encoding="utf-8")
    keep_meta = {k: meta.get(k) for k in ("name", "description", "copyrightText",
                                         "editingInfo", "currentVersion")}
    config.HORECA_META_JSON.write_text(json.dumps(keep_meta, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    edited_utc = (datetime.fromtimestamp(edited / 1000, timezone.utc).isoformat(timespec="seconds")
                  if edited else None)
    print(f"  {len(feats):,} permits; layer data last edited {edited_utc}")
    return {"url": config.HORECA_URL, "features": len(feats), "fields": list(config.HORECA_FIELDS),
            "data_last_edited_utc": edited_utc, "retrieved": _now(),
            "sha256": _sha256(config.HORECA_JSON)}


def fetch_bag():
    out, start = [], 0
    while True:
        page = _get_json(config.BAG_WFS_URL, {
            "service": "WFS", "version": "2.0.0", "request": "GetFeature",
            "typeName": "bag:verblijfsobject", "outputFormat": "application/json",
            "srsName": "EPSG:4326", "count": str(config.BAG_WFS_PAGE), "startIndex": str(start),
            "sortBy": "identificatie", "FILTER": config.BAG_WFS_FILTER})
        feats = page.get("features") or []
        out.extend(feats)
        if len(feats) < config.BAG_WFS_PAGE:
            break
        start += len(feats)
        time.sleep(PAUSE_S)
    ids = [f["properties"]["identificatie"] for f in out]
    if len(set(ids)) != len(ids):
        sys.exit("  duplicate BAG identifiers across pages - the paging is not stable")
    if len(out) < config.BAG_MIN_ROWS:
        sys.exit(f"  {len(out):,} BAG units - a failed fetch, nothing written")
    config.BAG_UNITS_JSON.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"  {len(out):,} shop-class units in use "
          f"({config.BAG_UNITS_JSON.stat().st_size:,} bytes)")
    return {"url": config.BAG_WFS_URL, "records": len(out), "retrieved": _now(),
            "sha256": _sha256(config.BAG_UNITS_JSON)}


def fetch_osm(force):
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"="tram"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no relations, or one without members - a FAILED fetch")
    print(f"  rail: {len(rels)} relations via {host}")
    gem = ("[out:json][timeout:240];"
           f'relation["boundary"="administrative"]["admin_level"="8"]["ref:gemeentecode"]'
           f"({s},{w},{n},{e});out geom;")
    els2, host2 = osm.fetch(gem, config.OSM_GEMEENTEN_JSON, force=force)
    codes = {x.get("tags", {}).get("ref:gemeentecode") for x in els2}
    if config.GEMEENTE_CODE not in codes:
        sys.exit(f"  gemeenten: Den Haag ({config.GEMEENTE_CODE}) missing")
    print(f"  gemeenten: {len(els2)} boundary relations via {host2}")
    return host, host2


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-fetch the OSM caches too")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Gemeente Den Haag, Horecavergunningen (layer 2):")
    horeca = fetch_horeca()
    print("\nPDOK BAG (shop-class units in use, gemeente 0518):")
    bag = fetch_bag()
    print("\nOpenStreetMap (keyless):")
    host, host2 = fetch_osm(args.force)

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(), "horeca": horeca, "bag_units": bag,
            "osm": {"rail_host": host, "gemeenten_host": host2, "bbox": config.RAIL_BBOX},
            "files_utc": {p.name: stamp(p) for p in (
                config.HORECA_JSON, config.BAG_UNITS_JSON, config.OSM_ROUTES_JSON,
                config.OSM_GEMEENTEN_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
