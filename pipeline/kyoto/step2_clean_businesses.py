"""Kyoto step 2: the food register REBUILT from the 2021 list and every monthly
list since (japan_register.kyoto_permit_stream, pinned at config.AS_OF), and the
city's barber, beauty and laundry lists, classified and joined to MLIT's block
file - the shared Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/kyoto/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.kyoto import config  # noqa: E402

if __name__ == "__main__":
    run(config)
