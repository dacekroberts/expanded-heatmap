"""Charleroi step 1: every station of the light metro's M2, M3 and M4.

    python pipeline/charleroi/step1_stations.py

Reads the cache only; `fetch_sources.py` installs the feed.

On the shared `pipeline/countries/belgium_tec.py` (Liege's step 1 too): TEC's
route_type 1 routes matched on route_short_name, platforms collapsed on
parent_station, then on the stop's own name (Tirou's two parents merged, the
owner's call), the three station gates, the daytime headways (the light-rail
15-minute test), each line's drawn shapes, and the split at the Ville de
Charleroi (INS 52011). M2 runs on into Fontaine-l'Eveque and Anderlues: drawn
to its end (owner, 2026-10-03), its stops there listed, not ringed. No stop is
thinned.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.charleroi import config  # noqa: E402
from pipeline.countries.belgium_tec import build_stations  # noqa: E402


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    build_stations(config)
