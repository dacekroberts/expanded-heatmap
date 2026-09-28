"""Fukuoka step 2: the city's own food list (permits from before 2021-06), MHLW's
online filings and the city's barber, beauty and laundry registers, classified
and joined to MLIT's block file - the shared Japanese step 2
(pipeline/countries/japan_step2.py), with MHLW's own point where the block join
misses and one pin where a premises is in both food lists.

Reads the cache and NEVER fetches.

    python pipeline/fukuoka/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.fukuoka import config  # noqa: E402

if __name__ == "__main__":
    run(config)
