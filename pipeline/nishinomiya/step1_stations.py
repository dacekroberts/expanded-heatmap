"""Nishinomiya step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Nishinomiya's own choices are in config.py (the
Hankyu Kobe, JR Kobe and JR Takarazuka Lines drawn as cut, owner 2026-10-02).

Reads the cache and NEVER fetches.

    python pipeline/nishinomiya/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.nishinomiya import config  # noqa: E402

if __name__ == "__main__":
    run(config)
