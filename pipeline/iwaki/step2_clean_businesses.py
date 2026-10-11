"""Iwaki step 2: the city's food list of 2026-03-31 with its five months of
new permits, and its barber and beauty-salon list of 2026-05-31 with its four
months of new premises, classified and joined to MLIT's block file - the
shared Japanese step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/iwaki/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.iwaki import config  # noqa: E402

if __name__ == "__main__":
    run(config)
