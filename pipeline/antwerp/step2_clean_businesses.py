"""Antwerp step 2: FAVV-AFSCA's food operators -> the food premises placed
inside the city, Borsbeek included.

    python pipeline/antwerp/step2_clean_businesses.py

Reads the caches only (`pipeline/antwerp/fetch_sources.py` downloads). The
chain is shared with Ghent (`pipeline/countries/belgium_favv.py`,
`run_step2`), every stage printed:

  * FAVV's rows in the fifteen postcodes (Borsbeek's 2150 included, merged
    into Antwerp 2025-01-01), grouped by establishment and classified as a
    whole (`pipeline/taxonomies/belgium_favv.py`): food service and food
    shops kept; caterers, complementary retail and the rest out, each counted;
  * joined on the establishment number to VKBO, paged for NIS 11002 and
    Borsbeek's old 11007; VKBO's (0,0) placeholder dropped;
  * kept inside Antwerp's polygon (OSM, NIS 11002, Borsbeek included); the
    step stops if no 2150 premises arrives;
  * a pin shows the type of premises, never a name: no name, phone or email
    column exists anywhere in the chain (asserted).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.antwerp import config  # noqa: E402
from pipeline.countries.belgium_favv import run_step2  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    run_step2(config, "antwerp", "pipeline/antwerp/fetch_sources.py")
