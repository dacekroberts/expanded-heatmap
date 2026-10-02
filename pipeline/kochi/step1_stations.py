"""Kōchi step 1: stations and line geometry from MLIT N02, cut at the city
line - the shared Japanese step 1 (pipeline/countries/japan_step1.py), which
Kobe built. Kōchi's own choices are in config.py (the lines; Tosaden's four
tram lines drawn by their signed names).

Reads the cache and NEVER fetches.

    python pipeline/kochi/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.kochi import config  # noqa: E402

if __name__ == "__main__":
    run(config)
