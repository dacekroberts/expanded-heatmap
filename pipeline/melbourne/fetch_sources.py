"""Download Melbourne's raw inputs into data/melbourne/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/melbourne/fetch_sources.py [--force]

The City of Melbourne's CLUE business establishments, the 2024 census only, as
one CSV export checked against the census's own count; the dataset's licence
field is recorded so a change shows. Then the LGA boundary and the rail from
OpenStreetMap.
"""
import argparse
import csv
import io
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.melbourne import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, timeout=600):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=timeout) as r:
        return r.read()


def fetch_clue(force):
    if config.CLUE_CSV.exists() and not force:
        print(f"  {'clue_2024':28} cached ({config.CLUE_CSV.stat().st_size:,} bytes)")
        return
    body = get(config.CLUE_EXPORT_URL)
    rows = list(csv.DictReader(io.StringIO(body.decode("utf-8-sig"))))
    if len(rows) != config.CLUE_EXPECTED_ROWS:
        sys.exit(f"  CLUE {config.CLUE_YEAR} export holds {len(rows):,} rows, not "
                 f"{config.CLUE_EXPECTED_ROWS:,} - read it first")
    years = {r.get("census_year", "")[:4] for r in rows}
    if years != {config.CLUE_YEAR}:
        sys.exit(f"  census years {sorted(years)} in the export, expected {config.CLUE_YEAR}")
    config.CLUE_CSV.write_bytes(body)
    print(f"  {'clue_2024':28} {len(body):,} bytes, {len(rows):,} rows")


def fetch_boundary(force):
    """The City of Melbourne (OSM relation 2404870), polygonised from its outer
    ways - Prague's method - and gated on its area."""
    from shapely.geometry import LineString, MultiLineString, mapping
    from shapely.ops import linemerge, polygonize, unary_union
    import geopandas as gpd
    from pipeline import osm

    if config.CITY_BOUNDARY_GEOJSON.exists() and not force:
        print(f"  {'city_boundary':28} cached")
        return
    els, host = osm.fetch(f"[out:json][timeout:180];rel({config.BOUNDARY_OSM_RELATION});out geom;",
                          config.BOUNDARY_OSM_CACHE, force=force)
    lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
             for e in els for m in e.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer"]
    poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"  City of Melbourne polygon is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "geometry": mapping(poly),
         "properties": {"osm_relation": config.BOUNDARY_OSM_RELATION}}), encoding="utf-8")
    print(f"  {'city_boundary':28} {km2:.1f} km2 (via {host})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    fetch_clue(args.force)
    meta = json.loads(get(config.CLUE_DATASET_URL))
    dm = (meta.get("metas") or {}).get("default") or {}

    fetch_boundary(args.force)

    from pipeline import osm
    els, host = osm.fetch(config.OSM_ROUTES_QUERY, config.OSM_ROUTES_JSON, force=args.force)
    rels = [e for e in els if e.get("type") == "relation"]
    print(f"  {'osm_rail_routes':28} {len(rels)} route relations (via {host})")
    els, host = osm.fetch(config.OSM_STOPS_QUERY, config.OSM_STOPS_JSON, force=args.force)
    print(f"  {'osm_rail_stops':28} {len(els)} stop nodes (via {host})")

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "clue_dataset_url": config.CLUE_DATASET_URL,
            "clue_year": config.CLUE_YEAR,
            "clue_modified": dm.get("modified"),
            "clue_license": dm.get("license"),
            "clue_license_url": dm.get("license_url")}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"  CLUE licence {prov['clue_license']}, modified {prov['clue_modified']}")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
