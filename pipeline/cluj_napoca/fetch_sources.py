"""Download Cluj-Napoca's OpenStreetMap inputs into data/cluj_napoca/raw/
(gitignored). NOT a step: drift_check.py never runs this file, and every step
exits naming it when its cache is missing.

    python pipeline/cluj_napoca/fetch_sources.py [--force]

THE REGISTER IS NOT DOWNLOADED HERE. DSVSA Cluj's hosts refuse scripts, so the
owner saved its files in their own browser (2026-10-07); this script checks
each is present and that its SHA-256 is the one config.py records, and a
cookie is never replayed. A changed file is a new fetch to re-measure.

Then, from OpenStreetMap through pipeline/osm.py, ONE Overpass query at a
time: the municipality's boundary (relation 3277038), CTP's tram relations
with their stop nodes, and (if absent) the address objects inside the
municipality, written to a file named for its fetch date.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.bucharest.fetch_sources import polygon_of  # noqa: E402
from pipeline.cluj_napoca import config  # noqa: E402


def register_files():
    out = {}
    for folder, files in ((config.DATA_RAW, config.ANIMAL_FILES),
                          (config.DATA_RAW / "non-animal", config.NON_ANIMAL_FILES)):
        for name, (sha16, stated) in files.items():
            p = folder / name
            if not p.exists():
                sys.exit(f"  missing {p}: the owner saves DSVSA Cluj's files in their browser")
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            if not sha.startswith(sha16):
                sys.exit(f"  {name}: sha256 {sha[:16]}, not the {sha16} measured on 2026-10-07 - a new "
                         f"edition; re-measure it before pointing config.py at it")
            out[f"{folder.name}/{name}"] = {"sha256": sha, "date_in_file": stated}
            print(f"  {name[:62]:64} {p.stat().st_size:>9,} B  sha256 {sha[:16]}  dated {stated}")
    return out


def fetch_boundary(force):
    import geopandas as gpd
    from shapely.geometry import mapping

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


def fetch_rail(force):
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"~"^(tram|light_rail|subway)$"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            "node(r.r);out body;")
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  tram relations missing or without members - a FAILED fetch")
    modes = sorted({r["tags"].get("route") for r in rels})
    print(f"  {'osm_rail':28} {len(rels)} route relations, modes {modes} (via {host})")
    if modes != ["tram"]:
        sys.exit(f"  route modes {modes}: a subway or light-rail relation is new (the metro was under "
                 f"construction on 2026-10-07) - re-read the brief's watch item")


def fetch_addresses(force):
    """The join target. Cached under its fetch date; a re-fetch writes a NEW
    dated file, and config.OSM_ADDRESSES_CSV is then pointed at it on purpose."""
    import urllib.request

    if config.OSM_ADDRESSES_CSV.exists() and not force:
        print(f"  {'osm_addresses':28} cached ({config.OSM_ADDRESSES_CSV.name}, "
              f"{config.OSM_ADDRESSES_CSV.stat().st_size:,} B)")
        return
    target = config.DATA_RAW / f"osm_addresses_{datetime.now(timezone.utc).date()}.csv"
    req = urllib.request.Request(osm.OVERPASS_HOSTS[0], data=config.OSM_ADDRESSES_QUERY.encode("utf-8"),
                                 headers={"User-Agent": osm.OVERPASS_USER_AGENT})
    with urllib.request.urlopen(req, timeout=600) as r:
        body = r.read()
    rows = body.count(b"\n") - 1
    if rows < config.OSM_ADDRESSES_MIN:
        sys.exit(f"  osm_addresses: {rows:,} rows, under {config.OSM_ADDRESSES_MIN:,} - a partial answer, "
                 f"nothing written")
    target.write_bytes(body)
    print(f"  {'osm_addresses':28} {len(body):,} B, {rows:,} rows -> {target.name}"
          + ("" if target == config.OSM_ADDRESSES_CSV else "; point config.OSM_ADDRESSES_CSV at it"))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    files = register_files()
    fetch_boundary(args.force)
    fetch_rail(args.force)
    fetch_addresses(args.force)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "register_dates": [config.REGISTER_DATE_FIRST, config.REGISTER_DATE_LAST],
            "register_files": files,
            "osm_addresses": config.OSM_ADDRESSES_CSV.name}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
