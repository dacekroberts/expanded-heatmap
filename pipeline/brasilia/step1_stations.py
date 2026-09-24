"""Brasília step 1: stations from OpenStreetMap - thin over
pipeline/countries/brazil_rail.py (the whitelist, gate 3 and the scope live in
config.py).

    python pipeline/brasilia/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.brazil_rail import build_stations  # noqa: E402
from pipeline.brasilia import config  # noqa: E402

if __name__ == "__main__":
    build_stations(config)
