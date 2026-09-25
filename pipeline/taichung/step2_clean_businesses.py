"""Taichung step 2: the national tax register's Taichung storefronts, joined to
Taichung's door plates - the shared Taiwanese step 2 (pipeline/countries/
taiwan_step2.py), which this file built and then moved there.

Reads the cache and NEVER fetches.

    python pipeline/taichung/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.taiwan_step2 import run  # noqa: E402
from pipeline.taichung import config  # noqa: E402

if __name__ == "__main__":
    run(config, "Taichung", "taichung")
