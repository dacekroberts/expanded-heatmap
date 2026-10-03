"""Shimonoseki step 2: MHLW's open data for the city (food permits and
notifications), classified and joined to MLIT's block file, MHLW's own point
where the join misses - the shared Japanese step 2
(pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/shimonoseki/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.shimonoseki import config  # noqa: E402

if __name__ == "__main__":
    run(config)
