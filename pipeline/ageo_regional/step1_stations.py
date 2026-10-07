"""Ageo (Regional) step 1: stations and line geometry from MLIT N02, cut at the
line of Ageo City and Ina Town - the shared Japanese step 1
(pipeline/countries/japan_step1.py), which Kobe built. Ageo (Regional)'s own
choices are in config.py (the New Shuttle's seven stations, cut once at the
Saitama City line; the JR Takasaki Line's two).

Reads the cache and NEVER fetches.

    python pipeline/ageo_regional/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.ageo_regional import config  # noqa: E402

if __name__ == "__main__":
    run(config)
