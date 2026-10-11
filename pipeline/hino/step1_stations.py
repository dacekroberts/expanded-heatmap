"""Hino step 1: stations and line geometry from MLIT N02, cut at the
city line - the shared Japanese step 1 (pipeline/countries/japan_step1.py),
which Kobe built. Hino's own choices are in config.py (the Keio Line, the
Tama Toshi Monorail and the JR Chuo Line cut at the city line, the Keio
Dobutsuen Line drawn whole, 高幡不動 and 多摩動物公園 one station each).

Reads the cache and NEVER fetches.

    python pipeline/hino/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.hino import config  # noqa: E402

if __name__ == "__main__":
    run(config)
