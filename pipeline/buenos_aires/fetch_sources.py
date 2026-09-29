"""Download Buenos Aires' raw inputs: the land-use survey and the parcel layer
from BA Data's CDN, and three OpenStreetMap queries (Subte and Premetro route
relations, their member nodes, CABA's boundary).

Deliberately NOT named step*.py, so pipeline/drift_check.py never runs it: a
step never fetches (see CLAUDE.md). Overpass goes through `pipeline/osm.py`.

    python pipeline/buenos_aires/fetch_sources.py            # skips what exists
    python pipeline/buenos_aires/fetch_sources.py --force    # re-download
"""

import argparse
import hashlib
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.osm import OVERPASS_USER_AGENT as USER_AGENT, fetch as osm_fetch
from pipeline.buenos_aires.config import (
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_BOUNDARY_RELATION,
    OSM_NETWORK,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    PARCELS_CSV,
    PARCELS_SHA256,
    PARCELS_URL,
    SURVEY_CSV,
    SURVEY_SHA256,
    SURVEY_URL,
)

# Subway AND tram relations of the Subte network, so step 1 sees the Premetro
# and decides on it explicitly rather than never having looked. The network
# filter keeps the Tramway Histórico (a heritage line, no network tag) out.
_RELS = (f'relation["type"="route"]["route"~"^(subway|tram)$"]'
         f'["network"="{OSM_NETWORK}"]({OSM_BBOX})')

# Stations from ROUTE-RELATION MEMBERSHIP, never from node tags (osm-rail).
Q_STATIONS = f"""
[out:json][timeout:90];
{_RELS}->.routes;
node(r.routes);
out body;
"""

Q_ROUTES = f"""
[out:json][timeout:90];
{_RELS};
out geom;
"""

# By relation id, which needs no area index; step 1 asserts its name and level.
Q_BOUNDARY = f"""
[out:json][timeout:90];
relation({OSM_BOUNDARY_RELATION});
out geom;
"""


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def download(url, path, expected_sha, what, force):
    """Stream to disk (the parcel file is 329 MB), resuming a dropped transfer
    with a range request - the parcel download dropped once at 183 MB."""
    if path.exists() and not force:
        got = sha256(path)
        note = "matches the recorded hash" if got == expected_sha else f"NEW HASH {got}"
        print(f"  cached {path.name} ({path.stat().st_size:,} bytes; {note})")
        return
    print(f"  downloading {what}: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(path.suffix + ".part")
    if force and part.exists():
        part.unlink()
    for _attempt in range(3):
        have = part.stat().st_size if part.exists() else 0
        headers = {"User-Agent": USER_AGENT}
        if have:
            headers["Range"] = f"bytes={have}-"
        try:
            with requests.get(url, headers=headers, stream=True, timeout=300) as r:
                r.raise_for_status()
                mode = "ab" if have and r.status_code == 206 else "wb"
                with open(part, mode) as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
            break
        except requests.RequestException as e:
            print(f"    interrupted at {part.stat().st_size if part.exists() else 0:,} bytes: {e}")
    else:
        raise SystemExit(f"{what}: three attempts failed; the partial file is kept.")
    with open(part, "rb") as f:
        head = f.read(64)
    if head.lstrip().startswith(b"<"):
        raise SystemExit(f"{what} is HTML, not CSV (first bytes {head[:16]!r}).")
    part.replace(path)
    got = sha256(path)
    print(f"  wrote {path.name} ({path.stat().st_size:,} bytes, sha256 {got})")
    if got != expected_sha:
        print("  NOTE: a new release - the recorded hash in config.py is the build's "
              "baseline; update it and re-measure before rebuilding.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    print("=== Buenos Aires: fetch raw sources ===\n")
    print("BA Data (CDN):")
    download(SURVEY_URL, SURVEY_CSV, SURVEY_SHA256, "land-use survey 2022-2024", args.force)
    download(PARCELS_URL, PARCELS_CSV, PARCELS_SHA256, "Parcelas", args.force)

    print("\nOpenStreetMap:")
    failed = []
    for query, path, what in (
            (Q_STATIONS, OSM_STATIONS_JSON, "route-relation member nodes"),
            (Q_ROUTES, OSM_ROUTES_JSON, "Subte and Premetro route relations"),
            (Q_BOUNDARY, OSM_BOUNDARY_JSON, "CABA's boundary")):
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
