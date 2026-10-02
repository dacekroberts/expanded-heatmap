"""Okayama step 2: MHLW's food filings for the city, classified and joined to
MLIT's block file - the shared Japanese step 2
(pipeline/countries/japan_step2.py), which Kobe built.

Reads the cache and NEVER fetches.

    python pipeline/okayama/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.okayama import config  # noqa: E402

if __name__ == "__main__":
    run(config)
