"""Ghent step 1: De Lijn's Ghent trams (T1, T2, T4) -> stations inside the city.

    python pipeline/ghent/step1_stations.py

Reads the caches only (`pipeline/ghent/fetch_sources.py` downloads). Shared
with Antwerp (`pipeline/countries/belgium_tram.py`, `build`): the lines
matched on route_short_name, platforms merged by name, the city polygon, the
stops outside listed with their commune (T2's Melle terminus), no thinning,
halved rings.

The first run reads the 1.79 GB stop_times.txt; run it through the memory
gate:

    python scripts/heavy_job.py run --label "ghent step 1" --session belgium -- python pipeline/ghent/step1_stations.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.belgium_tram import build  # noqa: E402
from pipeline.ghent import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    build(config, "ghent", "pipeline/ghent/fetch_sources.py")
