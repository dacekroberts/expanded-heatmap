"""Download Mexico City's raw inputs: three OSM queries and the DENUE export.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline, and a step must therefore
never fetch anything itself. San Francisco's fetch_sources.py has stated that
as an invariant since 2026-09-21, and this city was one of three exceptions to
it: the fetching lived in step1 and step2, cache-guarded, so a populated
`data/mexico_city/raw/` ran offline and drift behaved - but that directory is
gitignored, so **a fresh clone would have gone to the network from inside a
drift check.** Conditional is not the same as deterministic.

Moved out 2026-09-22 with the outputs unchanged; drift confirms it.

The Overpass fetching now goes through `pipeline/osm.py`, which carries a rule
this city's own code did not: a mirror can return a PARTIAL result with HTTP
200 and no `remark`, not merely an empty one. The empty-200 rule was learned
here - overpass.osm.ch returned 272 bytes over an empty set and a caller
reported it as a finding - and the partial case was measured on Barcelona.

    python pipeline/mexico_city/fetch_sources.py            # skips what exists
    python pipeline/mexico_city/fetch_sources.py --force    # re-download
"""

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.osm import fetch as osm_fetch
from pipeline.mexico_city.config import (
    DENUE_URL,
    DENUE_ZIP,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OVERPASS_USER_AGENT,
)

Q_STATIONS = f"""
[out:json][timeout:280];
(
  node["railway"]({OSM_BBOX});
);
out body;
"""

# `out geom`, NOT `out tags`: the member way geometry is the line alignment the
# map draws, and it is the OSM analogue of GTFS shapes.txt. Without it this
# city would have station dots and no lines, which breaks the project's
# invariant that every line is drawn, labelled and in the legend.
Q_ROUTES = f"""
[out:json][timeout:280];
(
  relation["type"="route"]["route"="subway"]({OSM_BBOX});
  relation["type"="route"]["route"="light_rail"]({OSM_BBOX});
);
out geom;
"""

Q_BOUNDARY = """
[out:json][timeout:280];
relation["boundary"="administrative"]["admin_level"="4"]["name"="Ciudad de México"];
out geom;
"""


def fetch_denue(force):
    if DENUE_ZIP.exists() and not force:
        print(f"  cached {DENUE_ZIP.name} ({DENUE_ZIP.stat().st_size:,} bytes)")
        return
    print(f"  downloading {DENUE_URL}")
    DENUE_ZIP.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(DENUE_URL, timeout=900,
                     headers={"User-Agent": OVERPASS_USER_AGENT})
    r.raise_for_status()
    # Magic bytes, not the filename the server claims - add-country's rule,
    # learned from Busan serving a PNG under a CSV's Content-Disposition.
    if not r.content.startswith(b"PK\x03\x04"):
        raise SystemExit(
            f"DENUE download is not a ZIP (first bytes {r.content[:8]!r}). "
            "Check what the server actually sent before trusting it."
        )
    DENUE_ZIP.write_bytes(r.content)
    print(f"  wrote {DENUE_ZIP.stat().st_size:,} bytes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    print("=== Mexico City: fetch raw sources ===\n")
    print("OpenStreetMap:")
    for query, path, what in (
            (Q_STATIONS, OSM_STATIONS_JSON, "railway nodes"),
            (Q_ROUTES, OSM_ROUTES_JSON, "subway and light-rail routes"),
            (Q_BOUNDARY, OSM_BOUNDARY_JSON, "the CDMX boundary")):
        if path.exists() and not args.force:
            print(f"  cached {path.name}")
            continue
        elements, host = osm_fetch(query, path, force=args.force)
        print(f"  {path.name}: {len(elements):,} elements via {host}  ({what})")

    print("\nINEGI DENUE:")
    fetch_denue(args.force)

    print("\nDone. The steps read these and never fetch.")


if __name__ == "__main__":
    main()
