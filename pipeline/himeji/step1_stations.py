"""Himeji step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Himeji's own choices are in config.py (JR West's
N02 山陽線 drawn as the JR Kobe Line and the Sanyo Line, each a route meeting
at 姫路; every line cut at the city line).

Reads the cache and NEVER fetches.

    python pipeline/himeji/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.himeji import config  # noqa: E402

if __name__ == "__main__":
    run(config)
