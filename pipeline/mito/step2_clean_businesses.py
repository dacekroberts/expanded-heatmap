"""Mito step 2: MHLW's filings for the city and its barber, beauty-salon and
laundry lists as of 2026-07-02, classified and joined to MLIT's block file -
the shared Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/mito/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.mito import config  # noqa: E402

if __name__ == "__main__":
    run(config)
