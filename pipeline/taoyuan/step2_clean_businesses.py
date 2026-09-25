"""Taoyuan step 2: the national tax register's Taoyuan storefronts, joined to
Taoyuan's door plates - the shared Taiwanese step 2 (pipeline/countries/
taiwan_step2.py), with Taoyuan's TWD97 door plates reprojected (PLATE_CRS).

Reads the cache and NEVER fetches.

    python pipeline/taoyuan/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.taiwan_step2 import run  # noqa: E402
from pipeline.taoyuan import config  # noqa: E402

if __name__ == "__main__":
    run(config, "Taoyuan", "taoyuan")
