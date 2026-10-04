"""Higashiosaka step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Higashiosaka's own choices are in config.py (Osaka Metro's Chuo Line
drawn cut, the Keihanna Line under its own name, 片町線 as the Gakkentoshi
Line, Nara's N03 naming the stations beyond the prefecture line).

Reads the cache and NEVER fetches.

    python pipeline/higashiosaka/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.higashiosaka import config  # noqa: E402

if __name__ == "__main__":
    run(config)
