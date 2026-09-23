"""Download Mexico City's raw inputs. Run this before the steps.

    python pipeline/mexico_city/fetch_sources.py [--force]

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline, and the steps must therefore
never fetch anything themselves.

WHY THIS FILE EXISTS AT ALL, GIVEN THE STEPS ALREADY WORKED
-----------------------------------------------------------
They worked by fetching on a cache miss, which is invisible on a machine that
already has `data/mexico_city/raw/` and wrong everywhere else. Demonstrated
2026-09-22: `python pipeline/drift_check.py` in a fresh worktree downloaded a
39 MB DENUE zip and three Overpass responses for this city and its two
siblings, then reported zero drift - while Toronto, which keeps its fetching
here, stopped correctly with "no data/<city>/raw/ - nothing to run against".

That difference matters beyond tidiness. **A drift check asks whether the
COMMITTED CODE still produces the COMMITTED OUTPUT.** A step that re-downloads
first asks whether the CURRENT UPSTREAM does - a different question, and one
that passes or fails for reasons no commit here caused. Toronto proved the
hazard is real the same day: re-fetching its register produced a map missing a
storefront that is in the committed one, while `baseline.json` reported
identical because the row counts happened to match.

TWO THINGS MOVED HERE, AND BOTH KEEP THEIR OWN HARD-WON BEHAVIOUR.

**Overpass is tried host by host, and an empty 200 is a FAILURE.**
`overpass.osm.ch` once returned 272 bytes and an empty element list for the
routes query; cached, that produced the vacuous claim that "every ref has
exactly 2 direction relations" over an empty set. An empty payload is never
cached and moves to the next host.

**The DENUE zip is checked by MAGIC BYTES, not by the filename the server
claims** - `add-country`'s rule, learned from a portal serving a PNG under a
CSV's Content-Disposition.
"""

import argparse
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.mexico_city.config import (  # noqa: E402
    DENUE_URL,
    DENUE_ZIP,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OVERPASS_HOSTS,
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


def overpass(query, cache_path, label, force):
    """POST to Overpass, trying each host. Cached, because a 504 from one host
    is a fact about that host and re-running should not depend on which one
    answered."""
    if cache_path.exists() and not force:
        print(f"  {label}: have {cache_path.name} "
              f"({cache_path.stat().st_size:,} bytes) - skipping")
        return
    last = None
    for host in OVERPASS_HOSTS:
        try:
            r = requests.post(host, data={"data": query}, timeout=300,
                              headers={"User-Agent": OVERPASS_USER_AGENT})
            print(f"  {label}: {host.split('/')[2]} HTTP {r.status_code} "
                  f"{len(r.content):,} bytes")
            if r.status_code == 200:
                payload = r.json()
                # A 200 WITH NO ELEMENTS IS NOT A SUCCESS, and caching it is
                # worse than failing - see this module's docstring.
                if not payload.get("elements"):
                    print(f"  {label}: {host.split('/')[2]} 200 but EMPTY - "
                          "not cached, trying next host")
                    last = "empty result"
                    time.sleep(2)
                    continue
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_text(r.text, encoding="utf-8")
                print(f"  {label}: wrote {cache_path.name} "
                      f"({cache_path.stat().st_size:,} bytes)")
                return
            last = f"HTTP {r.status_code}"
        except Exception as exc:                        # noqa: BLE001
            print(f"  {label}: {host.split('/')[2]} {type(exc).__name__}")
            last = f"{type(exc).__name__}"
        time.sleep(2)
    raise SystemExit(
        f"Every Overpass host failed for {label} (last: {last}). This is a "
        "fact about Overpass, not about Mexico City - retry before concluding "
        "anything about the data."
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
    overpass(Q_BOUNDARY, OSM_BOUNDARY_JSON, "boundary", args.force)
    overpass(Q_STATIONS, OSM_STATIONS_JSON, "stations", args.force)
    overpass(Q_ROUTES, OSM_ROUTES_JSON, "routes", args.force)

    print("\nBusinesses (INEGI DENUE):")
    download_denue(args.force)

    print("\nDone. Next: python pipeline/mexico_city/step1_stations.py")


if __name__ == "__main__":
    main()
