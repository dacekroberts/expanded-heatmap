"""Kumamoto step 2: the city's restaurant list, MHLW's online filings and the
city's 生活衛生 registers, classified and joined to MLIT's block file - the shared Japanese step 2
(pipeline/countries/japan_step2.py), which Kobe built.

Reads the cache and NEVER fetches.

    python pipeline/kumamoto/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.kumamoto import config  # noqa: E402

if __name__ == "__main__":
    run(config)
