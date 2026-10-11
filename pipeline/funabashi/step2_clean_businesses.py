"""Funabashi step 2: the city's barber and beauty-salon registers of
2026-08-01 and its laundry register of 2026-07-01, classified and joined to
MLIT's block file - the shared Japanese step 2
(pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/funabashi/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.funabashi import config  # noqa: E402

if __name__ == "__main__":
    run(config)
