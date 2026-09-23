"""Download Guadalajara's raw inputs. Run this before the steps.

    python pipeline/guadalajara/fetch_sources.py            # skips what exists
    python pipeline/guadalajara/fetch_sources.py --force    # re-download

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline, and the steps must therefore
never fetch anything themselves.

THE LAST OF THREE. Mexico City, Madrid and this city all kept their fetching
inside step1/step2 behind a cache check, which is offline only when the
gitignored raw directory happens to be populated. Mexico City moved out
2026-09-22, Madrid the same day on its own branch, and this file closes the
set - after which no `pipeline/*/step*.py` imports an HTTP client at all, and
`scripts/check_no_fetch_in_steps.py` keeps it that way.

WHY IT MATTERS, GIVEN THE STEPS ALREADY WORKED
----------------------------------------------
**A drift check asks whether the COMMITTED CODE still produces the COMMITTED
OUTPUT.** A step that re-downloads first asks whether the CURRENT UPSTREAM
does - a different question, and one that passes or fails for reasons no
commit here caused. Demonstrated 2026-09-22: `drift_check.py` in a fresh
worktree pulled a 39 MB DENUE zip and three Overpass responses for the Mexican
cities and reported zero drift, while Toronto stopped correctly with "no
data/<city>/raw/ - nothing to run against". Toronto also proved the hazard is
not theoretical: re-fetching its register produced a map missing a storefront
that is in the committed one, while the row-count baseline reported identical.

WHAT MOVED HERE KEEPS ITS OWN HARD-WON BEHAVIOUR, and this city's is not
Mexico City's despite the shared country:

  * **Two passes over the host list, not one**, with a 3-second pause. Kept as
    it was found; the sibling city uses one pass and 2 seconds, and neither
    number has been measured against the other. A refactor is a bad moment to
    quietly change a retry policy.
  * **An empty 200 is a FAILURE, never cached.** `overpass.osm.ch` once
    returned 272 bytes and an empty element list, which cached as the vacuous
    claim that every ref had exactly 2 direction relations over an empty set.
  * **The DENUE zip is checked by MAGIC BYTES**, not by the filename the
    server claims - add-country's rule, learned from a portal serving a PNG
    under a CSV's Content-Disposition.
"""

import argparse
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.guadalajara.config import (  # noqa: E402
    DENUE_URL,
    DENUE_ZIP,
    MUNICIPIOS_KEEP,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OSM_STATION_NETWORK,
    OVERPASS_HOSTS,
    OVERPASS_USER_AGENT,
)

# STATIONS COME FROM ROUTE-RELATION MEMBERSHIP, NOT FROM NODE LABELS, and this
# is the second time in two cities that a label filter lost real stations.
#
# The first version of this query was
# `node["railway"]["network"="Mi Tren"](bbox)`, which returned 96 nodes and
# **silently omitted every one of Línea 4's 8 stops**, because that line opened
# 2025-12-15 and its stop nodes carry no `network` tag at all. The result was a
# 49-station set with zero stations in Tlajomulco de Zúñiga - a map missing the
# same line the rejected GTFS feed was missing, arrived at by a different
# route. Mexico City's config says in capitals "MATCH ON THE MODE, NEVER ON THE
# NETWORK LABEL ALONE"; that warning sat in the previous city's config, which
# is not a file anyone opens while writing the next one.
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
# SPAIN** - also admin_level 6, also named Guadalajara - and step 1's
# "keep the largest polygon" tie-breaker then selected it on purpose, giving a
# 26,814 km2 "Guadalajara" against the municipio's ~151. The union-area gate
# caught it. Two lessons kept here rather than in a commit message: a name
# search without a geographic filter is a global search, and a tie-breaker on
# SIZE is exactly backwards when the wrong candidate is a province.
_NAMES = "|".join(MUNICIPIOS_KEEP)
Q_BOUNDARY = f"""
[out:json][timeout:280];
(
  relation["boundary"="administrative"]["admin_level"="6"]["name"~"^({_NAMES})$"]({OSM_BBOX});
  relation["boundary"="administrative"]["admin_level"="8"]["name"~"^({_NAMES})$"]({OSM_BBOX});
);
out geom;
"""


def overpass(query, cache_path, label, force):
    """POST to Overpass, two passes over the host list. Cached, because a 504
    from one host is a fact about that host and re-running should not depend on
    which one answered."""
    if cache_path.exists() and not force:
        print(f"  {label}: have {cache_path.name} "
              f"({cache_path.stat().st_size:,} bytes) - skipping")
        return
    last = None
    for _attempt in range(2):
        for host in OVERPASS_HOSTS:
            try:
                r = requests.post(host, data={"data": query}, timeout=300,
                                  headers={"User-Agent": OVERPASS_USER_AGENT})
                print(f"  {label}: {host.split('/')[2]} HTTP {r.status_code} "
                      f"{len(r.content):,} bytes")
                if r.status_code == 200:
                    payload = r.json()
                    # A 200 WITH NO ELEMENTS IS NOT A SUCCESS, and caching it
                    # is worse than failing - see this module's docstring.
                    if not payload.get("elements"):
                        print(f"  {label}: 200 but EMPTY - not cached, "
                              "next host")
                        last = "empty result"
                        time.sleep(3)
                        continue
                    cache_path.parent.mkdir(parents=True, exist_ok=True)
                    cache_path.write_text(r.text, encoding="utf-8")
                    print(f"  {label}: wrote {cache_path.name} "
                          f"({cache_path.stat().st_size:,} bytes)")
                    return
                last = f"HTTP {r.status_code}"
            except Exception as exc:                    # noqa: BLE001
                print(f"  {label}: {host.split('/')[2]} {type(exc).__name__}")
                last = type(exc).__name__
            time.sleep(3)
    raise SystemExit(
        f"Every Overpass host failed for {label} (last: {last}). A fact about "
        "Overpass, not about Guadalajara - retry before concluding anything."
    )


def download_denue(force):
    if DENUE_ZIP.exists() and not force:
        print(f"  denue: have {DENUE_ZIP.name} "
              f"({DENUE_ZIP.stat().st_size:,} bytes) - skipping")
        return
    print(f"  denue: GET {DENUE_URL}")
    DENUE_ZIP.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(DENUE_URL, timeout=900,
                     headers={"User-Agent": OVERPASS_USER_AGENT})
    r.raise_for_status()
    # Magic bytes, not the filename the server claims - see the docstring.
    if not r.content.startswith(b"PK\x03\x04"):
        raise SystemExit(
            f"DENUE download is not a ZIP (first bytes {r.content[:8]!r}). "
            "Check what the server actually sent before trusting it."
        )
    DENUE_ZIP.write_bytes(r.content)
    print(f"  denue: wrote {DENUE_ZIP.stat().st_size:,} bytes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download even if the file is already present")
    args = ap.parse_args()

    print("Rail geometry (OpenStreetMap via Overpass):")
    overpass(Q_BOUNDARY, OSM_BOUNDARY_JSON, "boundaries", args.force)
    overpass(Q_STATIONS, OSM_STATIONS_JSON, "stations", args.force)
    overpass(Q_ROUTES, OSM_ROUTES_JSON, "routes", args.force)

    print("\nBusinesses (INEGI DENUE, entidad 14 = Jalisco):")
    download_denue(args.force)

    print("\nDone. Next: python pipeline/guadalajara/step1_stations.py")


if __name__ == "__main__":
    main()
