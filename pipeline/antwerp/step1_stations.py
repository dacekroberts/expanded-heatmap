"""Antwerp step 1: De Lijn's Antwerp trams -> stations inside the city.

    python pipeline/antwerp/step1_stations.py

Reads the caches only (`pipeline/antwerp/fetch_sources.py` downloads). The
work is shared with Ghent (`pipeline/countries/belgium_tram.py`, `build`):
the lines matched on route_short_name, platforms merged by name, the city
polygon (Borsbeek included), the stops outside listed with their commune, no
thinning, halved rings.

What is Antwerp's own: THE WORKS SHAPE. Lines 3, 5, 9 and 15 are not in the
current feed and no tram serves the left bank (Linkeroever); A3 and A9 run on
the right bank. The left-bank stations are closed for works
(config.CLOSED_FOR_WORKS, docs/category_rules.md "Station scope"): listed, not
drawn, and the build stops when the feed serves one again or a closed line
returns.

The first run reads the 1.79 GB stop_times.txt; run it through the memory
gate:

    python scripts/heavy_job.py run --label "antwerp step 1" --session belgium -- python pipeline/antwerp/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.antwerp import config  # noqa: E402
from pipeline.countries.belgium_tram import build  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    build(config, "antwerp", "pipeline/antwerp/fetch_sources.py")
