"""Download a city's PLACES from OpenStreetMap for the place search. NOT a
step: drift_check.py never runs this file, and the index step exits naming it
when its cache is missing.

    python pipeline/place_index_fetch.py <city> [--force]

One Overpass query per city (the owner's rule: one in flight per session,
none in parallel, 60 s after a 504 or 429, all in pipeline/osm.py), cut by the
city's own boundary (config.PLACE_AREA), cached at config.PLACE_OSM_JSON:

  * every named highway way, with its node ids, and those nodes' positions
    (streets, and the intersections derived from shared nodes);
  * named junction nodes (Japan signs its intersections: 四条烏丸);
  * place nodes (wards, districts, neighborhoods, the 町 of Kyoto);
  * stations and tram stops;
  * landmarks: attractions, museums, viewpoints, historic sites, places of
    worship, parks and gardens, universities, peaks, rivers, named markets
    (kept only when notable, owner 2026-10-07).

Places only, never business records (owner, 2026-10-07): nothing here is
queried by shop, office, craft or a commercial amenity, and the index step
drops any landmark that carries one of those tags.

ODbL 1.0: the index built from this is a Derivative Database (OSMF's
Substantial guideline), published under ODbL with the credit every map already
shows; docs/data_sources.md has the row.
"""
import argparse
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline import osm  # noqa: E402

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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("city")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    config = importlib.import_module(f"pipeline.{args.city}.config")
    query = QUERY.format(area=config.PLACE_AREA)
    els, host = osm.fetch(query, config.PLACE_OSM_JSON, force=args.force, timeout=180, deadline=900)
    kinds = {}
    for e in els:
        kinds[e["type"]] = kinds.get(e["type"], 0) + 1
    print(f"{config.PLACE_OSM_JSON.name}: {len(els):,} elements from {host} {kinds}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
