"""Tama step 2: the Tokyo Metropolitan Government's Tama ledgers cut
to the city by address, with MHLW's Tokyo filings the ledgers lack (one pin
where a premises is in both), classified and joined to MLIT's block file - the
shared Japanese step 2 (pipeline/countries/japan_step2.py) over the Tama
cities' shared leg (pipeline/countries/tokyo_tama.py).

Reads the cache and NEVER fetches.

    python pipeline/tama/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.tama import config  # noqa: E402

if __name__ == "__main__":
    run(config)
