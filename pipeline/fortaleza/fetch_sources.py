"""Download Fortaleza (Regional)'s raw inputs - thin over pipeline/countries/brazil_fetch.py.
DELIBERATELY NOT NAMED step*.py, so drift_check.py never runs it.

    python pipeline/fortaleza/fetch_sources.py [--force]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.brazil_fetch import run  # noqa: E402
from pipeline.fortaleza import config  # noqa: E402

EXTRA = []

if __name__ == "__main__":
    run(config, [(k, url, config.DATA_RAW / name, magic.encode()) for k, url, name, magic in EXTRA])
