"""Download a city's PLACES from OpenStreetMap for the place search. NOT a
step: drift_check.py never runs this file, and the index step exits naming it
when its cache is missing.

    python pipeline/place_index_fetch.py <city> [--force]

Two Overpass queries per city, one after the other (the owner's rule: one in
flight per session, none in parallel, 60 s after a 504 or 429, all in
pipeline/osm.py), cut by the city's own boundary (config.PLACE_AREA): QUERY,
cached at config.PLACE_OSM_JSON, and EXTRA_QUERY, at
config.PLACE_OSM_EXTRA_JSON; each recorded in outputs/<slug>/provenance.json
("osm_places", "osm_places_extra"; a cache already on disk is recorded
without a query). Together:

  * every named highway way, with its node ids, and those nodes' positions
    (streets, and the intersections derived from shared nodes);
  * named junction nodes (Japan signs its intersections: 四条烏丸);
  * places, as nodes or areas (wards, districts, neighborhoods, the 町 of
    Kyoto; Sydney's Darling Harbour is an area);
  * stations and tram stops;
  * landmarks: attractions, museums, viewpoints, artworks, historic sites,
    places of worship, parks, gardens and stadiums, universities, town halls,
    libraries, theaters and arts centres, airports, peaks, beaches, bays,
    rivers, named markets (kept only when notable, owner 2026-10-07). The
    sample cities found Wrigley Field, Cloud Gate and the airports missing
    (2026-10-08).

Places only, never business records (owner, 2026-10-07): nothing here is
queried by shop, office, craft or a commercial amenity, and the index step
drops any landmark that carries one of those tags.

ODbL 1.0: the index built from this is a Derivative Database (OSMF's
Substantial guideline), published under ODbL with the credit every map already
shows; docs/data_sources.md has the row.
"""
import argparse
import datetime
import hashlib
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline import osm, place_index  # noqa: E402

QUERY = """[out:json][timeout:170];
area{area}->.a;
way["highway"]["name"](area.a)->.w;
.w out body qt;
node(w.w);
out skel qt;
(
  node["place"]["name"](area.a);
  node["name"]["highway"="traffic_signals"](area.a);
  node["name"]["junction"](area.a);
  nwr["railway"~"^(station|halt|tram_stop)$"]["name"](area.a);
  nwr["public_transport"="station"]["name"](area.a);
  nwr["tourism"~"^(attraction|museum|viewpoint|gallery|zoo|aquarium|theme_park)$"]["name"](area.a);
  nwr["historic"]["name"](area.a);
  nwr["amenity"="place_of_worship"]["name"](area.a);
  nwr["leisure"~"^(park|garden)$"]["name"](area.a);
  nwr["amenity"~"^(university|college)$"]["name"](area.a);
  nwr["amenity"="marketplace"]["name"](area.a);
  node["natural"="peak"]["name"](area.a);
  way["waterway"="river"]["name"](area.a);
);
out tags center qt;
"""
# The classes the sample cities found missing (2026-10-08: Chicago's Wrigley
# Field and Cloud Gate, Sydney's Darling Harbour, every airport), in a query
# of their own: added to QUERY they timed it out at 174 s on Chicago and
# Vancouver. Places as areas (QUERY has the nodes), stadiums, artworks,
# civic buildings, airports, beaches and bays.
EXTRA_QUERY = """[out:json][timeout:170];
area{area}->.a;
(
  way["place"]["name"](area.a);
  rel["place"]["name"](area.a);
  nwr["tourism"="artwork"]["name"](area.a);
  nwr["leisure"="stadium"]["name"](area.a);
  nwr["amenity"~"^(townhall|library|theatre|arts_centre)$"]["name"](area.a);
  nwr["aeroway"="aerodrome"]["name"](area.a);
  nwr["natural"~"^(beach|bay)$"]["name"](area.a);
);
out tags center qt;
"""


def record(config, path, key, how):
    """Record one cache in outputs/<slug>/provenance.json under `key`
    ("osm_places", "osm_places_extra"), in the shape the city's other OSM
    downloads use (japan_fetch.record): the file, its bytes and sha256, the
    element count, the host, OSM's own timestamp (osm_base), the exact query
    and when it was written. A cache already on disk is recorded as kept,
    dated by its modification time."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    prov_path = getattr(config, "PROVENANCE_JSON", None) or (
        Path(__file__).parent.parent / "outputs" / place_index.city_of(config)[0] / "provenance.json")
    prov = json.loads(prov_path.read_text(encoding="utf-8")) if prov_path.exists() else {}
    data = path.read_bytes()
    prov[key] = {
        "bytes": len(data),
        "elements": len(payload.get("elements") or []),
        "file": path.name,
        "host": payload.get("_fetched_from"),
        "how": how,
        "osm_base": payload.get("osm3s", {}).get("timestamp_osm_base"),
        "query": payload.get("_query"),
        "retrieved": datetime.datetime.fromtimestamp(
            path.stat().st_mtime, datetime.timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    prov_path.parent.mkdir(parents=True, exist_ok=True)
    # Bytes, so the committed file stays LF on Windows.
    prov_path.write_bytes((json.dumps(prov, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))
    return prov_path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("city")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")
    # One after the other, never in parallel (the owner's Overpass rule).
    for query, path, key in ((QUERY, config.PLACE_OSM_JSON, "osm_places"),
                             (EXTRA_QUERY, config.PLACE_OSM_EXTRA_JSON, "osm_places_extra")):
        kept = path.exists() and not args.force
        els, host = osm.fetch(query.format(area=config.PLACE_AREA), path, force=args.force,
                              timeout=180, deadline=900)
        kinds = {}
        for e in els:
            kinds[e["type"]] = kinds.get(e["type"], 0) + 1
        print(f"{path.name}: {len(els):,} elements from {host} {kinds}")
        prov = record(config, path, key, "kept (on disk from an earlier run)" if kept else "fetched")
        print(f"recorded in {prov.relative_to(Path(__file__).parent.parent)} as {key}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
