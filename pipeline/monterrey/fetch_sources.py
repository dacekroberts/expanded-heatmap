"""Download Monterrey (Regional)'s raw inputs: three OSM queries, the DENUE
export for Nuevo León, and the operator's network map (read, never shown).

Deliberately NOT named step*.py, so pipeline/drift_check.py never runs it: a
step never fetches (see CLAUDE.md). Overpass goes through `pipeline/osm.py`,
which tries every mirror and refuses an empty or partial 200.

    python pipeline/monterrey/fetch_sources.py            # skips what exists
    python pipeline/monterrey/fetch_sources.py --force    # re-download
"""

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.osm import fetch as osm_fetch
from pipeline.monterrey.config import (
    DENUE_URL,
    DENUE_ZIP,
    MUNIDS,
    OPERATOR_MAP_PDF,
    OPERATOR_MAP_URL,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_NETWORK,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OVERPASS_USER_AGENT,
)

# STATIONS FROM ROUTE-RELATION MEMBERSHIP, never from node tags - osm-rail's
# rule, and here it is what keeps 11 unbuilt monorail stations (tagged
# railway=station + construction=yes) off the map.
Q_STATIONS = f"""
[out:json][timeout:280];
relation["type"="route"]["route"~"^(light_rail|subway)$"]["network"="{OSM_NETWORK}"]({OSM_BBOX})->.routes;
node(r.routes);
out body;
"""

# Monorail is asked for too, so step 1 can SEE a Línea 4 or 6 relation the day
# one is added and refuse to continue, rather than never having looked.
Q_ROUTES = f"""
[out:json][timeout:280];
(
  relation["type"="route"]["route"~"^(light_rail|subway|monorail)$"]["network"="{OSM_NETWORK}"]({OSM_BBOX});
);
out geom;
"""

# Boundaries by INEGI's municipio code, not by name: `INEGI:MUNID` is the same
# key as DENUE's cve_ent + cve_mun. Bounded by the bbox anyway - osm-rail's
# rule, learned when an unbounded name search found Guadalajara, Spain.
_IDS = "|".join(MUNIDS)
Q_BOUNDARY = f"""
[out:json][timeout:280];
(
  relation["boundary"="administrative"]["admin_level"="6"]["INEGI:MUNID"~"^({_IDS})$"]({OSM_BBOX});
);
out geom;
"""


def download(url, path, magic, what, force):
    if path.exists() and not force:
        print(f"  cached {path.name} ({path.stat().st_size:,} bytes)")
        return
    print(f"  downloading {what}: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=900, headers={"User-Agent": OVERPASS_USER_AGENT})
    r.raise_for_status()
    # Magic bytes, not the filename the server claims (add-country).
    if not r.content.startswith(magic):
        raise SystemExit(f"{what} is not what it claims (first bytes {r.content[:8]!r}).")
    path.write_bytes(r.content)
    print(f"  wrote {path.name} ({path.stat().st_size:,} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    print("=== Monterrey (Regional): fetch raw sources ===\n")
    print("INEGI DENUE:")
    download(DENUE_URL, DENUE_ZIP, b"PK\x03\x04", "DENUE Nuevo León", args.force)

    print("\nOperator's network map (gate 3 and Línea 3's colour; never shown):")
    download(OPERATOR_MAP_URL, OPERATOR_MAP_PDF, b"%PDF", "Metrorrey network map", args.force)

    # OpenStreetMap last, and a failure does not stop the others: every mirror
    # timed out on 2026-09-27 while INEGI and nl.gob.mx answered, and a mirror
    # outage is a fact about the mirrors, not a reason to leave the rest unfetched.
    print("\nOpenStreetMap:")
    failed = []
    for query, path, what in (
            (Q_STATIONS, OSM_STATIONS_JSON, "route-relation member nodes"),
            (Q_ROUTES, OSM_ROUTES_JSON, "Metrorrey route relations"),
            (Q_BOUNDARY, OSM_BOUNDARY_JSON, "the four municipio boundaries")):
        if path.exists() and not args.force:
            print(f"  cached {path.name}")
            continue
        try:
            elements, host = osm_fetch(query, path, force=args.force)
        except RuntimeError as e:
            print(f"  FAILED {path.name}: {str(e)[:160]}")
            failed.append(path.name)
            continue
        print(f"  {path.name}: {len(elements):,} elements via {host}  ({what})")

    if failed:
        raise SystemExit(f"\nNot fetched: {failed}. Re-run later; cached files are kept.")
    print("\nDone. The steps read these and never fetch.")


if __name__ == "__main__":
    main()
