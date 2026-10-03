"""Kawasaki step 1: stations and line geometry from MLIT N02, cut at the city line -
the shared Japanese step 1 (pipeline/countries/japan_step1.py), which Kobe
built. Kawasaki's own choices are in config.py (JR East's services as routes
over N02's 東海道線, Tokyu's Meguro and Oimachi Lines the same way, the Nambu
Branch split off N02's 南武線, 武蔵小杉's two platforms joined).

Reads the cache and NEVER fetches.

    python pipeline/kawasaki/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.kawasaki import config  # noqa: E402

if __name__ == "__main__":
    run(config)
