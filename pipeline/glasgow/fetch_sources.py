"""Download Glasgow's raw inputs into data/glasgow/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/glasgow/fetch_sources.py [--force]

The FSA's file for Glasgow City (authority 776, Scotland's FHIS scheme), named
by code. It must parse as XML and carry authority 776's code, because a wrong
URL can answer 200 with an HTML page. Then the boundary and the Subway from
OpenStreetMap.
"""
import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.glasgow import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, timeout=600):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_boundary(force):
    """Glasgow City (OSM relation 1906767), polygonised from its outer ways -
    Prague's method - and gated on its area, so a partial answer cannot pass."""
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
        sys.exit(f"  Glasgow City polygon is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "geometry": mapping(poly),
         "properties": {"osm_relation": config.BOUNDARY_OSM_RELATION}}), encoding="utf-8")
    print(f"  {'city_boundary':28} {km2:.1f} km2 (via {host})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.FSA_XML.parent, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    if config.FSA_XML.exists() and not args.force:
        print(f"  {'FSA ' + config.FSA_AUTHORITY_CODE:28} cached ({config.FSA_XML.stat().st_size:,} bytes)")
    else:
        body = get(config.FSA_FILE_URL)
        root = ET.fromstring(body)
        codes = {e.text for e in root.iter("LocalAuthorityCode")}
        if codes != {config.FSA_AUTHORITY_CODE}:
            sys.exit(f"  the file carries authority code(s) {codes}, expected {config.FSA_AUTHORITY_CODE}")
        config.FSA_XML.write_bytes(body)
        print(f"  {'FSA ' + config.FSA_AUTHORITY_CODE:28} {len(body):,} bytes")

    fetch_boundary(args.force)

    from pipeline import osm
    els, host = osm.fetch(config.OSM_ROUTES_QUERY, config.OSM_ROUTES_JSON, force=args.force)
    rels = [e for e in els if e.get("type") == "relation"]
    print(f"  {'osm_rail_routes':28} {len(rels)} route relations (via {host})")
    els, host = osm.fetch(config.OSM_STOPS_QUERY, config.OSM_STOPS_JSON, force=args.force)
    print(f"  {'osm_rail_stops':28} {len(els)} stop nodes (via {host})")

    # The file's own <ExtractDate> - the date the page states (the FSA's
    # condition: show when the information was updated).
    with open(config.FSA_XML, encoding="utf-8") as fh:
        head = fh.read(400)
    i = head.find("<ExtractDate>")
    extract = head[i + 13:i + 23] if i >= 0 else ""
    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fsa_file_url": config.FSA_FILE_URL,
            "fsa_authority": {"code": config.FSA_AUTHORITY_CODE, "name": config.FSA_AUTHORITY_NAME},
            "fsa_extract_date": extract}
    print(f"  FSA extract date {extract}")
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
