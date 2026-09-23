"""Download Lille (Regional)'s raw inputs into data/lille/raw/ (gitignored); the
national SIRENE parquets are read from the shared country cache.

DELIBERATELY NOT NAMED step*.py. `drift_check.py` globs step*.py, so a download
living in a step would turn every drift check into a question about the current
upstream rather than about the committed code.

    python pipeline/lille/fetch_sources.py [--force] [--skip-parquet]

WHERE THIS DIFFERS FROM EVERY OTHER FRENCH CITY: there is no GTFS. Paris,
Marseille and Toulouse each read one operator feed; Lille reads four MEL WFS
layers, the national commune API and one Overpass query, because the feed has
no shapes.txt and everything it would add, MEL already publishes first-party.
See config.py's station-scope section for the source-by-line table.

OSM goes through pipeline/osm.py's fetch(), which caches the answer: two
mirrors return different data for the same bbox on the same day, so the cached
JSON is the only reproducible input, and --force re-fetches deliberately.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import france
from pipeline.lille import config
from pipeline.osm import fetch as osm_fetch

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _get(url, timeout=300):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _save_geojson(url, dest, label, want_geom):
    body = _get(url)
    obj = json.loads(body)
    feats = obj.get("features") or []
    # An empty FeatureCollection is a failed request, not an empty network -
    # the same guard map_common's loaders apply to their inputs.
    if not feats:
        sys.exit(f"  {label}: 0 features from {url[:90]}... - not written")
    kinds = {(f.get("geometry") or {}).get("type") for f in feats}
    if not kinds <= want_geom:
        sys.exit(f"  {label}: geometry {sorted(map(str, kinds))}, expected "
                 f"{sorted(want_geom)} - not written")
    dest.write_bytes(body)
    print(f"  {label:22s} {len(feats):>4} features  {len(body):>11,} bytes")
    return len(feats)


def fetch_wfs(force):
    geoms = {config.METRO_STATIONS_GEOJSON: {"Point"},
             config.TRAM_STOPS_GEOJSON: {"Point"},
             config.TRAM_LINES_GEOJSON: {"LineString", "MultiLineString"},
             config.LINE_COLOURS_GEOJSON: {None, "Point", "LineString",
                                           "MultiLineString"}}
    counts = {}
    for dest, layer in config.WFS_LAYERS.items():
        label = layer.split(":")[1]
        if dest.exists() and not force:
            n = len(json.loads(dest.read_text(encoding="utf-8"))["features"])
            print(f"  {label:22s} cached ({n} features)")
            counts[layer] = n
            continue
        params = {"service": "WFS", "version": "2.0.0", "request": "GetFeature",
                  "typeNames": layer, "outputFormat": "application/json",
                  "srsName": "EPSG:4326"}
        url = f"{config.WFS_URL}?{urllib.parse.urlencode(params)}"
        counts[layer] = _save_geojson(url, dest, label, geoms[dest])
    return counts


def fetch_communes(force):
    dest = config.MEL_COMMUNES_GEOJSON
    if dest.exists() and not force:
        print(f"  {'mel_communes':22s} cached")
        return
    n = _save_geojson(config.MEL_COMMUNES_URL, dest, "mel_communes",
                      {"Polygon", "MultiPolygon"})
    # 95 is MEL's commune count; a different number means the EPCI changed or
    # the API returned a partial answer, and either wants a look before use.
    if n != 95:
        print(f"  ⚠ MEL returned {n} communes, not 95 - check before trusting it")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-parquet", action="store_true")
    args = ap.parse_args()
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "wfs_url": config.WFS_URL,
            "wfs_layers": list(config.WFS_LAYERS.values()),
            "communes_url": config.MEL_COMMUNES_URL,
            "osm_query": config.OSM_ROUTES_QUERY}

    print("MEL WFS (Licence Ouverte 2.0):")
    prov["wfs_feature_counts"] = fetch_wfs(args.force)
    print("\nCommune contours (geo.api.gouv.fr):")
    fetch_communes(args.force)

    print("\nOpenStreetMap route relations (one query, cached):")
    elements, host = osm_fetch(config.OSM_ROUTES_QUERY, config.OSM_ROUTES_JSON,
                               force=args.force)
    rels = [e for e in elements if e.get("type") == "relation"]
    refs = sorted({(e["tags"].get("route"), e["tags"].get("ref")) for e in rels})
    print(f"  {len(rels)} relations from {host}: {refs}")
    prov["osm_host"] = host
    prov["osm_relations"] = len(rels)

    print("\nNational register (shared across every French city):")
    if args.skip_parquet:
        print("  SKIPPED (--skip-parquet)")
    for dest, label in ((config.SIRENE_PARQUET, "sirene_etab"),
                        (config.GEOLOC_PARQUET, "sirene_geoloc")):
        if dest.exists():
            print(f"  {label:22s} cached ({dest.stat().st_size:,} bytes) - "
                  f"shared at {france.SHARED_RAW}")
        elif not args.skip_parquet:
            sys.exit(f"  {label}: not cached. Run an earlier French city's "
                     f"fetch_sources.py, which resolves and streams it.")

    config.PROVENANCE_JSON.write_text(
        json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")
