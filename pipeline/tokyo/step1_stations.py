"""Tokyo step 1: stations and line geometry from MLIT N02, cut at the 23 wards'
line - the shared Japanese step 1 (pipeline/countries/japan_step1.py). Tokyo's
own choices are in config.py: JR East's nine public services, each a route over
the legal lines it runs on; the 15 wards without business data drawn hollow.

Reads the cache and NEVER fetches.

    python pipeline/tokyo/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step1 import run  # noqa: E402
from pipeline.tokyo import config  # noqa: E402

if __name__ == "__main__":
    run(config)
