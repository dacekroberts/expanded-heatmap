"""Download Newcastle (Regional)'s raw inputs into data/newcastle/raw/
(gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/newcastle/fetch_sources.py [--force]

The FSA's register: one bulk XML for each of the five Tyne and Wear
authorities, named by code (the FSA files them under a wider region). Each
file must parse as XML and carry its own authority's code, because a wrong URL
can answer 200 with an HTML page. Code-Point Open is copied from London's
cache, the same GB-wide file. Then the five districts and the Metro from
OpenStreetMap.
"""
import argparse
import json
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.newcastle import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, timeout=600):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_boundary(force):
    """The union of the five districts' OSM relations, each polygonised from
    its outer ways - Prague's method - gated on the union's area."""
    from shapely.geometry import LineString, MultiLineString, mapping
    from shapely.ops import linemerge, polygonize, unary_union
    import geopandas as gpd
    from pipeline import osm

    if config.CITY_BOUNDARY_GEOJSON.exists() and not force:
        print(f"  {'city_boundary':28} cached")
        return
    ids = ",".join(str(i) for i in config.BOUNDARY_OSM_RELATIONS)
    els, host = osm.fetch(f"[out:json][timeout:180];rel(id:{ids});out geom;",
                          config.BOUNDARY_OSM_CACHE, force=force)
    got = {e["id"] for e in els if e.get("type") == "relation"}
    if got != set(config.BOUNDARY_OSM_RELATIONS):
        sys.exit(f"  boundary relations returned {sorted(got)}, expected {sorted(config.BOUNDARY_OSM_RELATIONS)}")
    polys = []
    for e in els:
        lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                 for m in e.get("members", [])
                 if m.get("type") == "way" and m.get("role") == "outer"]
        poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
        km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
        print(f"    {config.BOUNDARY_OSM_RELATIONS[e['id']]:<22} {km2:6.1f} km2")
        polys.append(poly)
    union = unary_union(polys)
    km2 = gpd.GeoSeries([union], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"  Tyne and Wear union is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "geometry": mapping(union),
         "properties": {"osm_relations": sorted(config.BOUNDARY_OSM_RELATIONS)}}), encoding="utf-8")
    print(f"  {'city_boundary':28} {km2:.1f} km2 (via {host})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.FSA_RAW_DIR, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    total = 0
    for code, name in config.FSA_AUTHORITIES.items():
        dest = config.FSA_RAW_DIR / f"{code}.xml"
        if dest.exists() and not args.force:
            total += dest.stat().st_size
            continue
        body = get(config.FSA_FILE_URL.format(code=code))
        root = ET.fromstring(body)
        codes = {e.text for e in root.iter("LocalAuthorityCode")}
        if codes != {code}:
            sys.exit(f"  {name}: file carries authority code(s) {codes}, expected {code}")
        dest.write_bytes(body)
        total += len(body)
        print(f"  {name:<28} {len(body):>11,} bytes")
    print(f"  {len(config.FSA_AUTHORITIES)} authority files, {total:,} bytes")

    # Code-Point Open: London's cached copy of the same GB-wide file.
    if config.CODEPOINT_ZIP.exists() and not args.force:
        print(f"  {'codepo_gb.zip':28} cached ({config.CODEPOINT_ZIP.stat().st_size:,} bytes)")
    else:
        if not config.CODEPOINT_SOURCE.exists():
            sys.exit(f"  no {config.CODEPOINT_SOURCE}: run python pipeline/london/fetch_sources.py first")
        shutil.copyfile(config.CODEPOINT_SOURCE, config.CODEPOINT_ZIP)
        print(f"  {'codepo_gb.zip':28} copied from London's cache "
              f"({config.CODEPOINT_ZIP.stat().st_size:,} bytes)")
    london_prov = config.ROOT / "outputs" / "london" / "provenance.json"
    codepoint_edition = json.loads(london_prov.read_text(encoding="utf-8")).get("codepoint_edition")

    fetch_boundary(args.force)

    from pipeline import osm
    els, host = osm.fetch(config.OSM_ROUTES_QUERY, config.OSM_ROUTES_JSON, force=args.force)
    rels = [e for e in els if e.get("type") == "relation"]
    print(f"  {'osm_rail_routes':28} {len(rels)} route relations (via {host})")
    els, host = osm.fetch(config.OSM_STOPS_QUERY, config.OSM_STOPS_JSON, force=args.force)
    print(f"  {'osm_rail_stops':28} {len(els)} stop nodes (via {host})")

    # Each file's own <ExtractDate> - the date the page states (the FSA's
    # condition: show when the information was updated).
    extracts = {}
    for code, name in config.FSA_AUTHORITIES.items():
        with open(config.FSA_RAW_DIR / f"{code}.xml", encoding="utf-8") as fh:
            head = fh.read(400)
        i = head.find("<ExtractDate>")
        extracts[name] = head[i + 13:i + 23] if i >= 0 else ""
    dates = sorted(d for d in extracts.values() if d)
    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fsa_file_url": config.FSA_FILE_URL,
            "fsa_authorities": config.FSA_AUTHORITIES,
            "fsa_extract_dates": extracts,
            "fsa_extract_range": [dates[0], dates[-1]] if dates else [],
            "codepoint_edition": codepoint_edition}
    print(f"  FSA extract dates {dates[0]} to {dates[-1]}")
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
