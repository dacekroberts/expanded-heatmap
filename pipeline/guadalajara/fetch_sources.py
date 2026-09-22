"""Download Guadalajara's raw inputs: three OSM queries and the DENUE export.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline, and a step must therefore
never fetch anything itself. This city was one of three exceptions to that
invariant: fetching lived in step1 and step2 behind a cache check, which is
offline only when the gitignored raw directory happens to be populated. Moved
out 2026-09-22 with the outputs unchanged.

The Overpass fetching now goes through `pipeline/osm.py`, which carries a rule
this city's own code did not: a mirror can return a PARTIAL result with HTTP
200 and no `remark`, not only an empty one.

    python pipeline/guadalajara/fetch_sources.py            # skips what exists
    python pipeline/guadalajara/fetch_sources.py --force    # re-download
"""

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.osm import fetch as osm_fetch
from pipeline.guadalajara.config import (
    DENUE_URL,
    DENUE_ZIP,
    MUNICIPIOS_KEEP,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OSM_STATION_NETWORK,
    OVERPASS_USER_AGENT,
)

# STATIONS COME FROM ROUTE-RELATION MEMBERSHIP, NOT FROM NODE LABELS.
#
# The first version of this query was
# `node["railway"]["network"="Mi Tren"](bbox)`, which returned 96 nodes and
# **silently omitted every one of Linea 4's 8 stops**, because that line opened
# 2025-12-15 and its stop nodes carry no `network` tag at all. The result was a
# 49-station set with zero stations in Tlajomulco de Zuniga - a map missing the
# same line the rejected GTFS feed was missing, arrived at by a different route.
#
# Membership in a named route relation is the strongest available evidence that
# a node is a station on a line, and it cannot omit a line that has a relation.
# The relations themselves ARE network-tagged (all 8 carry `Mi Tren`), so the
# filter is safe at relation level - it was only ever wrong at node level.
Q_STATIONS = f"""
[out:json][timeout:280];
relation["type"="route"]["route"~"^(light_rail|subway)$"]["network"="{OSM_STATION_NETWORK}"]({OSM_BBOX})->.routes;
node(r.routes);
out body;
"""

Q_ROUTES = f"""
[out:json][timeout:280];
(
  relation["type"="route"]["route"~"^(light_rail|subway)$"]["network"="{OSM_STATION_NETWORK}"]({OSM_BBOX});
);
out geom;
"""

# Mexican municipios are admin_level 6 in OSM; 8 is asked for too rather than
# assumed, because an empty result here would look like "no stations in scope"
# three steps later.
#
# THE BBOX IS LOAD-BEARING, and leaving it off produced a confidently wrong
# answer on the first run: an unbounded name search matched **Guadalajara in
# SPAIN** - also admin_level 6, also named Guadalajara - and a "keep the
# largest polygon" tie-breaker then selected it on purpose, giving a 26,814 km2
# "Guadalajara" against the municipio's ~151. A name search without a
# geographic filter is a global search, and a tie-breaker on SIZE is exactly
# backwards when the wrong candidate is a province.
_NAMES = "|".join(MUNICIPIOS_KEEP)
Q_BOUNDARY = f"""
[out:json][timeout:280];
(
  relation["boundary"="administrative"]["admin_level"="6"]["name"~"^({_NAMES})$"]({OSM_BBOX});
  relation["boundary"="administrative"]["admin_level"="8"]["name"~"^({_NAMES})$"]({OSM_BBOX});
);
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

    print("=== Guadalajara: fetch raw sources ===\n")
    print("OpenStreetMap:")
    for query, path, what in (
            (Q_STATIONS, OSM_STATIONS_JSON, "route-relation member nodes"),
            (Q_ROUTES, OSM_ROUTES_JSON, "Mi Tren route relations"),
            (Q_BOUNDARY, OSM_BOUNDARY_JSON, "the four municipio boundaries")):
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
