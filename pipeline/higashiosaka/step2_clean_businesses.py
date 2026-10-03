"""Higashiosaka step 2: the city's food-permit register, rebuilt from its full
list of 2026-04-01 and the monthly new permits to 2026-08-31
(config.source_rows), classified and joined to MLIT's block file - the shared
Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/higashiosaka/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.higashiosaka import config  # noqa: E402

if __name__ == "__main__":
    run(config)
