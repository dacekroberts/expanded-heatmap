"""Kurashiki step 2: the city's year-end list of food-business permits in
force (the PDF's text, read as rows by config.source_rows, one row a permit
number), classified and joined to MLIT's block file - the shared Japanese
step 2 (pipeline/countries/japan_step2.py).

Reads the cache and NEVER fetches; the PDF's text is made by
fetch_sources.py.

    python pipeline/kurashiki/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries.japan_step2 import run  # noqa: E402
from pipeline.kurashiki import config  # noqa: E402

if __name__ == "__main__":
    run(config)
