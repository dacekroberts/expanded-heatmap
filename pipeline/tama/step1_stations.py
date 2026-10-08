"""Tama step 1: stations and line geometry from MLIT N02, cut at the
city line - the shared Japanese step 1 (pipeline/countries/japan_step1.py),
which Kobe built. Tama's own choices are in config.py (the Odakyu Tama and
Keio Sagamihara lines cut at the city line, the Keio Line's one station drawn
as cut, the Tama Toshi Monorail's one station left out).

Reads the cache and NEVER fetches.

    python pipeline/tama/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.tama import config  # noqa: E402

if __name__ == "__main__":
    run(config)
