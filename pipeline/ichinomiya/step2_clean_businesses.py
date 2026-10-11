"""Ichinomiya step 2: the city's food list of 2026-03-31 kept whole plus its
monthly lists to 2026-08-31, its barber, beauty-salon and laundry lists with
the 2026 months, and MHLW's notifications, classified and joined to MLIT's
block file - the shared Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/ichinomiya/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.ichinomiya import config  # noqa: E402

if __name__ == "__main__":
    run(config)
