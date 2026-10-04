"""Liege step 1: every stop of the tram, T1.

    python pipeline/liege/step1_stations.py

Reads the cache only; `fetch_sources.py` installs the feed.

On the shared `pipeline/countries/belgium_tec.py` (Charleroi's step 1 too):
TEC's only route_type 0 route matched on route_short_name, platforms collapsed
on parent_station, then on the stop's own name (Liege Expo's two parents
merged, the owner's call), the three station gates with gate 3 against the
City of Liege's own stop list (a mismatch stops the step), the daytime
headway, the drawn shapes, and the split at the Ville de Liege (INS 62063),
which holds every stop. No stop is thinned.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.belgium_tec import build_stations  # noqa: E402
from pipeline.liege import config  # noqa: E402


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    build_stations(config)
