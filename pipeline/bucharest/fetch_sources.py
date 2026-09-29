"""Download Bucharest's OpenStreetMap inputs into data/bucharest/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/bucharest/fetch_sources.py [--force]

THE REGISTER IS NOT DOWNLOADED HERE. DSVSA's hosts serve a browser challenge,
so the owner fetches its files in their own browser (the Band C memo's
condition); this script only checks they are present and prints each file's
SHA-256, and a cookie is never replayed. Then the municipality and its six
sectors, the metro, and (if absent) the OSM address objects.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.bucharest import config


def register_files():
    out = {}
    for folder, files in ((config.DATA_RAW, config.ANIMAL_FILES),
                          (config.DATA_RAW / "non-animal", config.NON_ANIMAL_FILES)):
        for name in files:
            p = folder / name
            if not p.exists():
                sys.exit(f"  missing {p}: the owner fetches DSVSA's files in their browser")
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            out[f"{folder.name}/{name}"] = sha
            print(f"  {name[:60]:62} {p.stat().st_size:>9,} B  sha256 {sha[:16]}")
    return out


def polygon_of(rel):
    from shapely.geometry import LineString, MultiLineString
    from shapely.ops import linemerge, polygonize, unary_union
    lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer" and len(m.get("geometry") or []) >= 2]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def fetch_boundary(force):
    import geopandas as gpd
    from shapely.geometry import mapping
    from pipeline import osm

    if config.CITY_BOUNDARY_GEOJSON.exists() and not force:
        print(f"  {'city_boundary':28} cached")
        return
    els, host = osm.fetch(f"[out:json][timeout:180];rel({config.BOUNDARY_OSM_RELATION});out geom;",
                          config.BOUNDARY_OSM_CACHE, force=force)
    rel = [e for e in els if e.get("type") == "relation"]
    if len(rel) != 1 or rel[0]["tags"].get("name") != config.BOUNDARY_OSM_NAME:
        sys.exit(f"  relation {config.BOUNDARY_OSM_RELATION} is not {config.BOUNDARY_OSM_NAME}: "
                 f"{[r['tags'].get('name') for r in rel]}")
    poly = polygon_of(rel[0])
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"  the municipality polygon is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "geometry": mapping(poly),
         "properties": {"osm_relation": config.BOUNDARY_OSM_RELATION}}), encoding="utf-8")
    print(f"  {'city_boundary':28} {km2:.1f} km2 (via {host})")


def fetch_sectors(force):
    """The six sectors, one polygon each, named by their number."""
    import re
    import geopandas as gpd
    from shapely.geometry import mapping
    from pipeline import osm

    if config.SECTORS_GEOJSON.exists() and not force:
        print(f"  {'sectors':28} cached")
        return
    els, host = osm.fetch(config.SECTORS_QUERY, config.SECTORS_OSM_CACHE, force=force)
    feats = []
    for e in (e for e in els if e.get("type") == "relation"):
        m = re.search(r"\b([1-6])\b", e["tags"].get("name", ""))
        if not m:
            continue
        poly = polygon_of(e)
        feats.append({"type": "Feature", "geometry": mapping(poly),
                      "properties": {"sector": m.group(1), "name": e["tags"].get("name"),
                                     "osm_relation": e["id"]}})
    got = sorted(f["properties"]["sector"] for f in feats)
    if got != ["1", "2", "3", "4", "5", "6"]:
        sys.exit(f"  sectors found: {got} ({[e['tags'].get('name') for e in els if e.get('type') == 'relation']})")
    g = gpd.GeoDataFrame.from_features(feats, crs=config.CRS_GEOGRAPHIC)
    km2 = g.to_crs(config.CRS_PROJECTED).area / 1e6
    config.SECTORS_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats},
                                                 ensure_ascii=False), encoding="utf-8")
    print(f"  {'sectors':28} " + ", ".join(f"{s} {a:.1f} km2" for s, a in zip(g['sector'], km2))
          + f"; total {km2.sum():.1f} (via {host})")


def fetch_addresses(force):
    """The join target. Cached under its fetch date; a re-fetch writes a NEW
    dated file, and config.OSM_ADDRESSES_CSV is then pointed at it on purpose."""
    import urllib.request
    from pipeline import osm

    if config.OSM_ADDRESSES_CSV.exists() and not force:
        print(f"  {'osm_addresses':28} cached ({config.OSM_ADDRESSES_CSV.name}, "
              f"{config.OSM_ADDRESSES_CSV.stat().st_size:,} B)")
        return
    target = config.DATA_RAW / f"osm_addresses_{datetime.now(timezone.utc).date()}.csv"
    req = urllib.request.Request(osm.OVERPASS_HOSTS[0], data=config.OSM_ADDRESSES_QUERY.encode("utf-8"),
                                 headers={"User-Agent": osm.OVERPASS_USER_AGENT})
    with urllib.request.urlopen(req, timeout=600) as r:
        body = r.read()
    target.write_bytes(body)
    print(f"  {'osm_addresses':28} {len(body):,} B -> {target.name}; point config.OSM_ADDRESSES_CSV at it")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    shas = register_files()
    fetch_boundary(args.force)
    fetch_sectors(args.force)
    fetch_addresses(args.force)

    from pipeline import osm
    els, host = osm.fetch(config.OSM_ROUTES_QUERY, config.OSM_ROUTES_JSON, force=args.force)
    rels = [e for e in els if e.get("type") == "relation"]
    print(f"  {'osm_rail_routes':28} {len(rels)} route relations (via {host})")
    els, host = osm.fetch(config.OSM_STOPS_QUERY, config.OSM_STOPS_JSON, force=args.force)
    print(f"  {'osm_rail_stops':28} {len(els)} stop and platform members (via {host})")

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "register_date": config.REGISTER_DATE,
            "register_files_sha256": shas,
            "osm_addresses": config.OSM_ADDRESSES_CSV.name}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
