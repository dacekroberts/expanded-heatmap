"""Hamamatsu step 2: the city's barber, beauty-salon and two laundry registers,
classified and joined to MLIT's block file, the city's own point where the
join gives only a centroid - the shared Japanese step 2
(pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches.

    python pipeline/hamamatsu/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.hamamatsu import config  # noqa: E402

if __name__ == "__main__":
    run(config)
