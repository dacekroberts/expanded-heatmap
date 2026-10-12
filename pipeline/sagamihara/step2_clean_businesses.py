"""Sagamihara step 2: the city's food-permit, barber and beauty-salon registers
rebuilt to 2026-08-31 from the 2026-03-31 lists and the months since, and its
laundry register of 2026-03-31, classified and joined to MLIT's block file -
the shared Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/sagamihara/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.sagamihara import config  # noqa: E402

if __name__ == "__main__":
    run(config)
