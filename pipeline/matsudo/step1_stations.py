"""Matsudo step 1: stations and line geometry from MLIT N02, cut at the city
line - the shared Japanese step 1 (pipeline/countries/japan_step1.py), which
Kobe built. Matsudo's own choices are in config.py (seven lines cut at the
line, two of them one-station stubs kept as cut).

Reads the cache and NEVER fetches.

    python pipeline/matsudo/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.matsudo import config  # noqa: E402

if __name__ == "__main__":
    run(config)
