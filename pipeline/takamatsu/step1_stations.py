"""Takamatsu step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Takamatsu's own choices are in config.py (the
Kotoden Nagao Line drawn through to 高松築港 over the Kotohira Line's track,
the Yakuri Cable left out as a sightseeing funicular).

Reads the cache and NEVER fetches.

    python pipeline/takamatsu/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.takamatsu import config  # noqa: E402

if __name__ == "__main__":
    run(config)
