"""Tsu step 2: Mie Prefecture's food-permit list and its barber and
beauty-salon registers (as of 2026-08-31), cut to Tsu by address
(config.source_rows), classified and joined to MLIT's block file - the shared
Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/tsu/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.tsu import config  # noqa: E402

if __name__ == "__main__":
    run(config)
