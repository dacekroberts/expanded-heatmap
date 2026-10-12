"""Naha step 2: the food register rebuilt from the city's monthly new-permit and
renewal files (in term on 2026-08-31) and its barber and beauty-salon
registers (2026-09-04), classified and joined to MLIT's block file - the
shared Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/naha/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.naha import config  # noqa: E402

if __name__ == "__main__":
    run(config)
