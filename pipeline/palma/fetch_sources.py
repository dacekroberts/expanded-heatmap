"""Download Palma's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/palma/fetch_sources.py [--force]

All keyless: the Consell de Mallorca's register (GOIB catalogue), Catastro's
INSPIRE addresses for Palma (certificates from the OS store), and from
OpenStreetMap the municipality, its neighbours and the Metro's relations. A
cached file is never replaced without --force.
"""
import argparse
import io
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests
import truststore

truststore.inject_into_ssl()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.palma import config  # noqa: E402
from pipeline.palma.step1_stations import polygon_from_relation  # noqa: E402  (no network)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, dest, force, label, check=None):
    if dest.exists() and not force:
        print(f"  {label}: cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    r = requests.get(url, timeout=600, headers=HEADERS)
    r.raise_for_status()
    if len(r.content) < 1000:
        sys.exit(f"  {label}: a {len(r.content)}-byte answer - a failed fetch, not a negative")
    if check:
        check(r.content)
    dest.write_bytes(r.content)
    print(f"  {label}: {len(r.content):,} bytes -> {dest.name}")


def check_register(content):
    head = content[:4000].decode("utf-8-sig", "replace")
    for col in ("Denominació comercial", "Direcció", "Municipi", "Grup", "Estat"):
        if col not in head:
            sys.exit(f"  register: no {col!r} column in the answer - not the register")


def check_catastro(content):
    if content[:2] != b"PK":
        sys.exit(f"  catastro: not a zip ({content[:60]!r}). Not cached")
    names = zipfile.ZipFile(io.BytesIO(content)).namelist()
    if "A.ES.SDGC.AD.07040.gml" not in names:
        sys.exit(f"  catastro: members {names} lack A.ES.SDGC.AD.07040.gml")


def fetch_boundary(force):
    """Palma (OSM relation 341321), polygonised from its outer ways - Prague's
    and Glasgow's method - and gated on its area."""
    import geopandas as gpd
    from shapely.geometry import mapping
    if config.CITY_BOUNDARY_GEOJSON.exists() and not force:
        print(f"  boundary: cached {config.CITY_BOUNDARY_GEOJSON.name}")
        return None
    els, host = osm.fetch(f"[out:json][timeout:180];rel({config.BOUNDARY_OSM_RELATION});out geom;",
                          config.BOUNDARY_OSM_CACHE, force=force)
    poly = polygon_from_relation(els)
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"  Palma's polygon is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "geometry": mapping(poly),
         "properties": {"osm_relation": config.BOUNDARY_OSM_RELATION}}), encoding="utf-8")
    print(f"  boundary: {km2:.1f} km2 (via {host})")
    return host


def fetch_rail(force):
    s, w, n, e = config.RAIL_BBOX
    modes = "|".join(config.ROUTE_TYPES)
    q = ("[out:json][timeout:120];"
         f'(relation["type"="route"]["route"~"^({modes})$"]({s},{w},{n},{e}););'
         "out geom;node(r);out tags center;")
    els, host = osm.fetch(q, config.OSM_ROUTES_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no route relations came back - a FAILED fetch, not a negative")
    print(f"  rail: {len(rels)} relations via {host}")
    # The municipalities the relations' stops fall in, to NAME a station
    # outside Palma (step 1).
    q2 = ("[out:json][timeout:180];"
          f'relation["boundary"="administrative"]["admin_level"="8"]({s},{w},{n},{e});out geom;')
    els2, _ = osm.fetch(q2, config.NEIGHBOURS_OSM_CACHE, force=force)
    print(f"  municipalities: {sum(x['type'] == 'relation' for x in els2)} in the rail box")
    return host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download cached files")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    print("Register (GOIB catalogue):")
    get(config.REGISTER_URL, config.REGISTER_CSV, args.force, "register", check=check_register)
    print("\nCatastro INSPIRE addresses (OS trust store):")
    get(config.CATASTRO_URL, config.CATASTRO_ZIP, args.force, "catastro", check=check_catastro)
    # Overpass last: its 504s come in waves, and a re-run skips what is cached.
    print("\nOpenStreetMap (keyless):")
    fetch_boundary(args.force)
    host = fetch_rail(args.force)

    def stamp(path):
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(
            timespec="seconds")

    with zipfile.ZipFile(config.CATASTRO_ZIP) as z:
        cat_date = "%04d-%02d-%02d" % z.getinfo("A.ES.SDGC.AD.07040.gml").date_time[:3]
    files = {p.name: stamp(p) for p in (config.REGISTER_CSV, config.CATASTRO_ZIP,
                                        config.CITY_BOUNDARY_GEOJSON, config.OSM_ROUTES_JSON,
                                        config.NEIGHBOURS_OSM_CACHE)}
    prov = {"written_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "as_of_date": config.REGISTER_UPDATED, "catastro_date": cat_date, "files_utc": files,
            "sources": {"register": config.REGISTER_URL, "register_dataset": config.REGISTER_DATASET_URI,
                        "catastro": config.CATASTRO_URL, "catastro_atom": config.CATASTRO_ATOM_URL,
                        "boundary_osm_relation": config.BOUNDARY_OSM_RELATION}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files and never "
          f"fetch.")


if __name__ == "__main__":
    main()
