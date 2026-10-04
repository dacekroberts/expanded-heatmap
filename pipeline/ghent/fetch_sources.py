"""Download Ghent's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/ghent/fetch_sources.py [--keep-vkbo] [--refresh-favv] [--refresh-feed]

Antwerp's four sources (pipeline/antwerp/fetch_sources.py), shared through
pipeline/countries/belgium_fetch.py's fetch_city: De Lijn's GTFS and FAVV's
list, one copy each for both cities; OpenStreetMap's communes in Ghent's rail
box (cached; no query is sent while the cache exists); VKBO paged through
the WFS for NIS 44021. Then outputs/ghent/provenance.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.belgium_fetch import fetch_city  # noqa: E402
from pipeline.ghent import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    fetch_city(config, sys.argv[1:])
