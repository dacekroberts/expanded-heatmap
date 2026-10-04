"""Hamamatsu step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Hamamatsu's own choices are in config.py (the Enshu Railway wholly
inside; Tenhama and JR's Tokaido and Iida lines cut at the city line, with
Aichi's and Nagano's N03 naming the stations beyond the prefecture line).

Reads the cache and NEVER fetches.

    python pipeline/hamamatsu/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.hamamatsu import config  # noqa: E402

if __name__ == "__main__":
    run(config)
