"""Higashimurayama step 1: stations and line geometry from MLIT N02, cut at the
city line - the shared Japanese step 1 (pipeline/countries/japan_step1.py),
which Kobe built. Higashimurayama's own choices are in config.py (Seibu's five
lines and JR East's Musashino Line cut at the city line, three one-station
stubs drawn as cut, the Leo Liner left out).

Reads the cache and NEVER fetches.

    python pipeline/higashimurayama/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.higashimurayama import config  # noqa: E402

if __name__ == "__main__":
    run(config)
