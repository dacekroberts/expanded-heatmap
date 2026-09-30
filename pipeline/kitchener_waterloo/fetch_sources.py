"""Download Kitchener–Waterloo's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/kitchener_waterloo/fetch_sources.py [--force]

All keyless: the Region of Waterloo's two inspection layers (ArcGIS, by
object id), its two bulk inspection zips (curl - see config), its Cities and
Towns and ION Stops layers, and OSM's rail relations (Overpass). A cached
file is never replaced without --force.
"""
import argparse
import io
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.kitchener_waterloo import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
CHUNK = 500


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def arcgis_json(url, params):
    r = requests.get(url, params={**params, "f": "json"}, timeout=300, headers=HEADERS)
    r.raise_for_status()
    body = r.json()
    if "error" in body:
        sys.exit(f"  {url}: {body['error']}")
    return body


def layer(url, dest, force, label, fields, where="1=1"):
    """Every feature of an ArcGIS layer as GeoJSON, fetched by object id in
    chunks (the layers cap an answer at 1,000), with the named fields only."""
    if dest.exists() and not force:
        print(f"  {label}: cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    ids = sorted(arcgis_json(f"{url}/query", {"where": where, "returnIdsOnly": "true"})["objectIds"])
    features = []
    for i in range(0, len(ids), CHUNK):
        # An OBJECTID range, not an objectIds list: the proxy answers a
        # 500-id list with HTTP 500 (2026-09-30).
        part = ids[i:i + CHUNK]
        r = requests.get(f"{url}/query", timeout=300, headers=HEADERS, params={
            "where": f"({where}) AND OBJECTID >= {part[0]} AND OBJECTID <= {part[-1]}",
            "outFields": ",".join(fields), "outSR": "4326", "f": "geojson"})
        r.raise_for_status()
        features += r.json()["features"]
    if len(features) != len(ids):
        sys.exit(f"  {label}: {len(features):,} features for {len(ids):,} ids - a failed fetch")
    body = json.dumps({"type": "FeatureCollection", "features": features})
    assert "SiteTelephone" not in body
    dest.write_text(body, encoding="utf-8")
    print(f"  {label}: {len(features):,} features -> {dest.name}")


def curl_zip(url, dest, force, label, members):
    """The zip host fails Python's TLS handshake (config), so the system curl
    fetches it, verification on. Only a zip holding the expected members is
    cached."""
    if dest.exists() and not force:
        print(f"  {label}: cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    curl = shutil.which("curl")
    if not curl:
        sys.exit("  curl is not on PATH; this host needs it (see config)")
    tmp = dest.with_suffix(".part")
    subprocess.run([curl, "-sS", "--fail", "-A", HEADERS["User-Agent"], "-o", str(tmp), url],
                   check=True, timeout=600)
    content = tmp.read_bytes()
    if content[:2] != b"PK":
        tmp.unlink()
        sys.exit(f"  {label}: not a zip ({content[:60]!r}). Not cached")
    names = set(zipfile.ZipFile(io.BytesIO(content)).namelist())
    if not set(members) <= names:
        tmp.unlink()
        sys.exit(f"  {label}: members {sorted(names)} lack {sorted(set(members) - names)}")
    tmp.replace(dest)
    print(f"  {label}: {len(content):,} bytes -> {dest.name}")


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

    print("Inspection layers (ArcGIS):")
    layer(config.FOOD_LAYER_URL, config.FOOD_LAYER_GEOJSON, args.force, "food",
          config.LAYER_FIELDS)
    layer(config.PERSONAL_LAYER_URL, config.PERSONAL_LAYER_GEOJSON, args.force, "personal",
          config.LAYER_FIELDS)
    print("\nInspection zips (curl):")
    curl_zip(config.FOOD_ZIP_URL, config.FOOD_ZIP, args.force, "food zip",
             config.FOOD_ZIP_MEMBERS)
    curl_zip(config.PERSONAL_ZIP_URL, config.PERSONAL_ZIP, args.force, "personal zip",
             config.PERSONAL_ZIP_MEMBERS)
    print("\nBoundaries and ION stops (ArcGIS):")
    names = ",".join(f"'{n}'" for n in config.CITY_NAMES)
    layer(config.BOUNDARY_URL, config.CITY_BOUNDARY_GEOJSON, args.force, "cities",
          ["PlaceName", "Municipality", "Within_RMW"], where=f"PlaceName IN ({names})")
    if config.ION_STOPS_JSON.exists() and not args.force:
        print(f"  ION stops: cached {config.ION_STOPS_JSON.name}")
    else:
        stops = arcgis_json(f"{config.ION_STOPS_URL}/query",
                            {"where": "1=1", "outFields": "*", "returnGeometry": "false"})
        config.ION_STOPS_JSON.write_text(json.dumps(stops), encoding="utf-8")
        print(f"  ION stops: {len(stops['features'])} rows -> {config.ION_STOPS_JSON.name}")
    # Overpass last: its 504s come in waves, and a re-run skips what is cached.
    print("\nOpenStreetMap (keyless):")
    host = fetch_rail()

    def stamp(path):
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(
            timespec="seconds")

    with zipfile.ZipFile(config.FOOD_ZIP) as z:
        zip_date = "%04d-%02d-%02d" % z.getinfo(config.FOOD_ZIP_MEMBERS[0]).date_time[:3]
    files = {p.name: stamp(p) for p in (
        config.FOOD_LAYER_GEOJSON, config.PERSONAL_LAYER_GEOJSON, config.FOOD_ZIP,
        config.PERSONAL_ZIP, config.CITY_BOUNDARY_GEOJSON, config.ION_STOPS_JSON,
        config.OSM_ROUTES_JSON)}
    prov = {"written_utc": _now(), "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "as_of_date": config.AS_OF_DATE, "zip_member_date": zip_date, "files_utc": files,
            "sources": {"food_layer": config.FOOD_LAYER_URL,
                        "personal_layer": config.PERSONAL_LAYER_URL,
                        "food_zip": config.FOOD_ZIP_URL, "personal_zip": config.PERSONAL_ZIP_URL,
                        "cities": config.BOUNDARY_URL, "ion_stops": config.ION_STOPS_URL}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these "
          f"files and never fetch.")


if __name__ == "__main__":
    main()
