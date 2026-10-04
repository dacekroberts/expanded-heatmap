"""Nara step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Nara's own choices are in config.py (Kintetsu's Nara, Kyoto
and Kashihara lines and JR's Kansai and Sakurai lines, cut at the city line).

Reads the cache and NEVER fetches.

    python pipeline/nara/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.nara import config  # noqa: E402

if __name__ == "__main__":
    run(config)
