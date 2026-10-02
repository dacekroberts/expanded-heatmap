"""Download Manchester (Regional)'s raw inputs into data/manchester/raw/
(gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/manchester/fetch_sources.py [--force] [--no-osm]

The method is pipeline/countries/uk_fetch.py: the seven FSA authority files
by code, Code-Point Open from London's cache, one Overpass query (Metrolink
and the seven districts) and NaPTAN's Greater Manchester area.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries import uk_fetch  # noqa: E402
from pipeline.manchester import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    uk_fetch.main(config)
