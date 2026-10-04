"""Shimonoseki step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Shimonoseki's own choices are in config.py (JR Kyushu's stub drawn as
part of the JR Sanyo Line, the San'in Line left out beyond 小串, Fukuoka's N03
naming the station beyond the strait).

Reads the cache and NEVER fetches.

    python pipeline/shimonoseki/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.shimonoseki import config  # noqa: E402

if __name__ == "__main__":
    run(config)
