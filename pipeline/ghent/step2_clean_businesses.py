"""Ghent step 2: FAVV-AFSCA's food operators -> the food premises placed
inside the city.

    python pipeline/ghent/step2_clean_businesses.py

Reads the caches only (`pipeline/ghent/fetch_sources.py` downloads). Antwerp's
chain (`pipeline/countries/belgium_favv.py`, `run_step2`), every stage
printed: FAVV's rows in the ten postcodes, classified per establishment;
joined to VKBO (NIS 44021), the (0,0) placeholder dropped; kept inside Ghent's
polygon. A pin shows the type of premises, never a name.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.belgium_favv import run_step2  # noqa: E402
from pipeline.ghent import config  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    run_step2(config, "ghent", "pipeline/ghent/fetch_sources.py")
