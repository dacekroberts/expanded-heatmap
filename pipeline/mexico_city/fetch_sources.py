"""Download Mexico City's raw inputs. Run this before the steps.

    python pipeline/mexico_city/fetch_sources.py [--force]
    python pipeline/mexico_city/fetch_sources.py --regional [--skip-osm]

`--regional` (implied when config.REGIONAL is on) also fetches what Mexico
City (Regional) adds: DENUE entidad 15 in its two parts and the four State of
México municipio boundaries. `--skip-osm` leaves every Overpass query unasked
(one query in flight per session; CLAUDE.md).

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
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.osm import fetch as osm_fetch  # noqa: E402
from pipeline.mexico_city.config import (  # noqa: E402
    DENUE_REGIONAL_URLS,
    DENUE_REGIONAL_ZIPS,
    DENUE_URL,
    DENUE_ZIP,
    MUNIDS,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_MUNICIPIOS_JSON,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OVERPASS_HOSTS,
    OVERPASS_USER_AGENT,
    REGIONAL,
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


# Mexico City (Regional): the four municipios by INEGI's code, Monterrey's
# query (pipeline/monterrey/fetch_sources.py). `INEGI:MUNID` is DENUE's
# cve_ent + cve_mun, so boundaries and register join on one key. Bounded by
# the bbox, osm-rail's rule (an unbounded name search once found Guadalajara,
# Spain). Fetched through pipeline/osm.py, which refuses an empty 200, a
# remark and an all-zero count, and keeps the owner's 60 s after a 504 or 429.
_IDS = "|".join(MUNIDS)
Q_MUNICIPIOS = f"""
[out:json][timeout:280];
(
  relation["boundary"="administrative"]["admin_level"="6"]["INEGI:MUNID"~"^({_IDS})$"]({OSM_BBOX});
);
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


def download_denue_regional(force):
    """Entidad 15's two parts, each checked by magic bytes and each read for
    its member list. The single-ZIP URL for 15 is a soft 404, which is why
    the URLs come from denue_urls() and never denue_url()."""
    for url, path in zip(DENUE_REGIONAL_URLS, DENUE_REGIONAL_ZIPS):
        if path.exists() and not force:
            print(f"  denue 15: have {path.name} "
                  f"({path.stat().st_size:,} bytes) - skipping")
        else:
            print(f"  denue 15: GET {url}")
            path.parent.mkdir(parents=True, exist_ok=True)
            r = requests.get(url, timeout=900,
                             headers={"User-Agent": OVERPASS_USER_AGENT})
            r.raise_for_status()
            if not r.content.startswith(b"PK\x03\x04"):
                raise SystemExit(
                    f"{url} is not a ZIP (first bytes {r.content[:8]!r}, "
                    f"{len(r.content):,} bytes, {r.headers.get('Content-Type')}). "
                    "The single-ZIP URL for 15 answers 200 with an HTML page; "
                    "check what the server actually sent."
                )
            path.write_bytes(r.content)
            print(f"  denue 15: wrote {path.name} ({path.stat().st_size:,} bytes)")
        with zipfile.ZipFile(path) as zf:
            print(f"      members: {zf.namelist()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download even if the file is already present")
    ap.add_argument("--regional", action="store_true",
                    help="also fetch Mexico City (Regional)'s inputs "
                         "(implied when config.REGIONAL is on)")
    ap.add_argument("--skip-osm", action="store_true",
                    help="ask no Overpass query in this run")
    args = ap.parse_args()
    regional = REGIONAL or args.regional

    if args.skip_osm:
        print("Rail geometry (OpenStreetMap via Overpass): skipped (--skip-osm)")
    else:
        print("Rail geometry (OpenStreetMap via Overpass):")
        overpass(Q_BOUNDARY, OSM_BOUNDARY_JSON, "boundary", args.force)
        overpass(Q_STATIONS, OSM_STATIONS_JSON, "stations", args.force)
        overpass(Q_ROUTES, OSM_ROUTES_JSON, "routes", args.force)
        if regional:
            elements, host = osm_fetch(Q_MUNICIPIOS, OSM_MUNICIPIOS_JSON,
                                       force=args.force)
            print(f"  municipios: {OSM_MUNICIPIOS_JSON.name}, "
                  f"{len(elements):,} elements via {host}")

    print("\nBusinesses (INEGI DENUE):")
    download_denue(args.force)
    if regional:
        download_denue_regional(args.force)

    print("\nDone. Next: python pipeline/mexico_city/step1_stations.py")


if __name__ == "__main__":
    main()
