"""Kyoto step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py). Kyoto's own
choices are in config.py (the 18 lines, the Biwako Line split off 東海道線, the
two funiculars and the Sagano scenic line left out).

Reads the cache and NEVER fetches.

    python pipeline/kyoto/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.kyoto import config  # noqa: E402

if __name__ == "__main__":
    run(config)
