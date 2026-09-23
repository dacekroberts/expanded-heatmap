"""Download Barcelona's raw inputs: the premises census and three OSM queries.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline, and a step must therefore
never fetch anything itself. San Francisco's fetch_sources.py states that as an
invariant, and it is currently conditional rather than absolute: Madrid, Mexico
City and Guadalajara import `requests` inside their step files. They are
cache-guarded, so a populated `data/<city>/raw/` runs offline - but that
directory is gitignored, so a fresh clone is not. **Barcelona does not add a
fourth exception**, which is cheaper to do now than to unpick later.

It matters more here than in most cities, because Barcelona's rail is OSM and
the Overpass mirrors DISAGREE with each other - measured 2026-09-22, they
return different tram and funicular counts for this bbox and even spell the
northern L10 segment differently (`L10N` against `L10 Nord`). Caching is what
makes a rebuild reproducible; re-querying would not be.

    python pipeline/barcelona/fetch_sources.py            # skips what exists
    python pipeline/barcelona/fetch_sources.py --force    # re-download
"""

import argparse
import csv
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.osm import fetch as osm_fetch
from pipeline.barcelona.config import (
    ACTIVE_COLUMN,
    BUSINESSES_RAW_CSV,
    CKAN_BASE,
    CKAN_RESOURCE_ID,
    CENSUS_YEAR,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    USECOLS,
)

UA = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}

Q_ROUTES = f"""
[out:json][timeout:280];
(
  relation["type"="route"]["route"~"^(subway|funicular)$"]({OSM_BBOX});
);
out geom;
"""

def stations_query(route_elements):
    """The relations' member nodes, asked for BY ID.

    NOT `node["railway"="station"](bbox)`: that returns the station boxes,
    which are a DIFFERENT OBJECT from the `stop_position` nodes a PTv2 route
    relation contains. Measured here - 225 station nodes, 378 relation member
    nodes, and **no overlap at all** - so combining the two filters yields an
    empty set.

    And not the obvious `relation[...](bbox)->.routes; node(r.routes);` either,
    which re-runs the whole relation search server-side and is what the mirrors
    kept failing on. The route relations are already cached with their member
    ids, so this asks for exactly those 378 nodes - a far cheaper query, and a
    deterministic one, since the id list comes from the cached file rather than
    from whatever a mirror returns today.
    """
    ids = sorted({m["ref"] for rel in route_elements
                  for m in rel.get("members", ())
                  if m.get("type") == "node"})
    if not ids:
        raise SystemExit("No node members in the cached routes file.")
    return ids, f"""
[out:json][timeout:280];
node(id:{",".join(str(i) for i in ids)});
out body;
"""

# Spanish municipalities are admin_level 8. THE BBOX IS LOAD-BEARING: an
# unbounded name search for "Barcelona" also matches the province and the
# comarca, and the Guadalajara build lost time to exactly this - an unbounded
# search matched Guadalajara, SPAIN, and a largest-polygon tie-breaker then
# chose it deliberately.
Q_BOUNDARY = f"""
[out:json][timeout:280];
(
  relation["boundary"="administrative"]["admin_level"="8"]["name"="Barcelona"]({OSM_BBOX});
);
out geom;
"""


def fetch_census(force):
    """The 2022 premises census, via CKAN's datastore, paged.

    `USECOLS` is the privacy control and it is applied AT DOWNLOAD: the census
    carries 50 fields and this asks for eleven. `Nom_Local` is a trade name and
    is 100% populated, so unlike Los Angeles there is no registrant-name column
    to fall back to and none is requested.
    """
    if BUSINESSES_RAW_CSV.exists() and not force:
        print(f"  census: cached {BUSINESSES_RAW_CSV.name}")
        return

    rows, offset, limit = [], 0, 10_000
    while True:
        url = f"{CKAN_BASE}/datastore_search?" + urllib.parse.urlencode({
            "resource_id": CKAN_RESOURCE_ID,
            "limit": limit,
            "offset": offset,
            "fields": ",".join(USECOLS),
        })
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=300) as r:
            got = json.loads(r.read().decode("utf-8"))["result"]["records"]
        rows.extend(got)
        if len(got) < limit:
            break
        offset += limit
        print(f"    ... {len(rows):,}")

    if not rows:
        raise SystemExit("CKAN returned no rows - a portal problem, not a fact "
                         "about Barcelona. Retry before concluding anything.")

    BUSINESSES_RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    with io.open(BUSINESSES_RAW_CSV, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(USECOLS),
                                extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    active = sum(1 for r in rows if (r.get(ACTIVE_COLUMN) or "").strip() == "Actiu")
    print(f"  census {CENSUS_YEAR}: {len(rows):,} rows, {active:,} Actiu "
          f"-> {BUSINESSES_RAW_CSV.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download even if the file exists")
    args = ap.parse_args()

    print("=== Barcelona: fetch raw sources ===\n")
    print("OpenStreetMap:")

    # Routes first: the station query is derived from their member ids.
    if OSM_ROUTES_JSON.exists() and not args.force:
        print(f"  cached {OSM_ROUTES_JSON.name}")
        route_elements = json.loads(
            OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
    else:
        route_elements, host = osm_fetch(Q_ROUTES, OSM_ROUTES_JSON,
                                         force=args.force)
        print(f"  {OSM_ROUTES_JSON.name}: {len(route_elements):,} relations "
              f"via {host}")

    if OSM_BOUNDARY_JSON.exists() and not args.force:
        print(f"  cached {OSM_BOUNDARY_JSON.name}")
    else:
        elements, host = osm_fetch(Q_BOUNDARY, OSM_BOUNDARY_JSON,
                                   force=args.force)
        print(f"  {OSM_BOUNDARY_JSON.name}: {len(elements)} relation(s) via "
              f"{host}  (the municipal boundary)")

    if OSM_STATIONS_JSON.exists() and not args.force:
        print(f"  cached {OSM_STATIONS_JSON.name}")
    else:
        ids, query = stations_query(route_elements)
        elements, host = osm_fetch(query, OSM_STATIONS_JSON, force=args.force)
        print(f"  {OSM_STATIONS_JSON.name}: {len(elements):,} of {len(ids):,} "
              f"member nodes via {host}")

    print("\nOpen Data BCN:")
    fetch_census(args.force)

    print("\nDone. The steps read these and never fetch.")


if __name__ == "__main__":
    main()
