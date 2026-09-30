"""Download Strasbourg's raw inputs: the rolling feed (always fresh), the
commune and EPCI contours, OpenStreetMap geometry where the config asks for it,
and the national SIRENE parquets (shared).

    python pipeline/strasbourg/fetch_sources.py [--skip-parquet] [--force]

Thin over `pipeline/countries/france_tram_fetch.py`. Deliberately not named
step*.py, so drift_check.py never runs it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_tram_fetch import fetch_all
from pipeline.strasbourg import config

if __name__ == "__main__":
    fetch_all(config)
