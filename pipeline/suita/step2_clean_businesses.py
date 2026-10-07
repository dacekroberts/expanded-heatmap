"""Suita step 2: the city's two food lists of 2026-03-31 (revised and old law), its barber,
beauty-salon and laundry registers of 2026-08-31 and MHLW's notifications, classified and joined
to MLIT's block file - the shared Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/suita/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.suita import config  # noqa: E402

if __name__ == "__main__":
    run(config)
