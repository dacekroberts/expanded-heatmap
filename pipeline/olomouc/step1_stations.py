"""Olomouc step 1: tram stations from OpenStreetMap's route relations.

    python pipeline/olomouc/step1_stations.py

Thin over `pipeline/countries/czechia_osm_tram.py`, which runs the shared
`pipeline/osm_tram.py` (the tram kits' module): every relation kept or named in
config.NOT_DRAWN, stops collapsed by name, the station gates, scope over the
obce, and the drawn geometry written for step 3. Reads the cache only;
`fetch_sources.py` downloads.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.olomouc import config  # noqa: E402
from pipeline.countries.czechia_osm_tram import step1  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    step1(config)
