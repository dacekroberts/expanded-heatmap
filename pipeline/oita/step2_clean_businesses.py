"""Ōita step 2: the city's food-permit list and its barber, beauty-salon and
laundry lists (each register with its 2026 months) and its notification
list (call 212), MHLW's file lending only its points,
classified and joined to MLIT's block file - the shared Japanese step 2
(pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/oita/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.oita import config  # noqa: E402

if __name__ == "__main__":
    run(config)
