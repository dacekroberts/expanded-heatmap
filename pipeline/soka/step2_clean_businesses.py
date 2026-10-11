"""Sōka step 2: Saitama Prefecture's food layers, R8.3.31 old-law list and
生活衛生 lists, cut to the city by address, classified and joined to MLIT's
block file - the shared Japanese step 2 (pipeline/countries/japan_step2.py)
over the Saitama pages' shared leg (pipeline/countries/saitama_pref.py).

Reads the cache and NEVER fetches.

    python pipeline/soka/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.soka import config  # noqa: E402

if __name__ == "__main__":
    run(config)
