"""Download Pittsburgh's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/pittsburgh/fetch_sources.py [--force]

Four keyless downloads: Allegheny County's geocoded food facilities (WPRDC),
the Census place polygon, the Census county subdivisions around the lines,
and OSM's rail relations (Overpass).
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.pittsburgh import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get(url, dest, force, label, params=None, min_bytes=100):
    if dest.exists() and not force:
        print(f"  {label}: cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    r = requests.get(url, params=params, timeout=600, headers=HEADERS)
    r.raise_for_status()
    if len(r.content) < min_bytes or b'"error"' in r.content[:200]:
        sys.exit(f"  {label}: a failed fetch, not a negative: {r.content[:200]!r}")
    dest.write_bytes(r.content)
    print(f"  {label}: {len(r.content):,} bytes -> {dest.name}")


def fetch_rail():
    s, w, n, e = config.RAIL_BBOX
    modes = "|".join(config.ROUTE_TYPES)
    q = ("[out:json][timeout:120];"
         f'(relation["type"="route"]["route"~"^({modes})$"]({s},{w},{n},{e}););'
         "out geom;node(r);out tags center;")
    els, host = osm.fetch(q, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no route relations came back - a FAILED fetch, not a negative")
    print(f"  rail: {len(rels)} relations via {host}")
    return host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download cached files")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    print("Boundaries:")
    get(config.CITY_BOUNDARY_URL, config.CITY_BOUNDARY_GEOJSON, args.force, "place",
        params=config.CITY_BOUNDARY_QUERY)
    s, w, n, e = config.RAIL_BBOX
    get(config.COUSUB_URL, config.COUSUB_GEOJSON, args.force, "county subdivisions",
        params={"geometry": f"{w},{s},{e},{n}", "geometryType": "esriGeometryEnvelope",
                "inSR": "4326", "spatialRel": "esriSpatialRelIntersects",
                "outFields": "GEOID,NAME", "outSR": "4326", "f": "geojson"})
    print("\nFood facilities:")
    get(config.FACILITIES_URL, config.FACILITIES_CSV, args.force, "facilities",
        min_bytes=3_000_000)
    # Overpass last: its 504s come in waves, and a re-run skips what is cached.
    print("\nOpenStreetMap (keyless):")
    host = fetch_rail()

    def stamp(path):
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(
            timespec="seconds")

    files = [config.FACILITIES_CSV, config.CITY_BOUNDARY_GEOJSON, config.COUSUB_GEOJSON,
             config.OSM_ROUTES_JSON]
    prov = {"written_utc": _now(), "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "as_of_date": config.AS_OF_DATE, "register_date": config.REGISTER_DATE,
            "files_utc": {p.name: stamp(p) for p in files},
            "sources": {"food_facilities": {"endpoint": config.FACILITIES_URL}}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these "
          f"files and never fetch.")


if __name__ == "__main__":
    main()
