"""Step 2 - Liege's storefronts from Wallonia's LoGIC 2024 survey.

    python pipeline/liege/step2_clean_businesses.py

Input:  data/belgium/raw/logic/LOGIC_2024.gpkg     (the downloaded GeoPackage)
        data/liege/raw/osm_communes.json            (the commune polygon check)
        data/liege/processed/stations.csv           (step 1: the rings)
Output: data/liege/processed/businesses_clean.csv
        data/liege/processed/logic_coverage.json

On the shared `pipeline/countries/belgium_logic.py` (Charleroi's step 2 too).
What a reader should know before trusting the counts printed below:

  * **Two buckets** (pipeline/taxonomies/wallonia_logic.py): Commerce de
    detail is Retail, HoReCa is Food service with hotels inside it (kept and
    disclosed, owner); Services (a catch-all) and Cellule vide (vacant) out.
  * **Complete only inside the commercial perimeters**: outside them the
    survey records only shops over 200 m2 of sales area (the publisher). The
    coverage inside the station rings is printed before the counts are
    trusted (the owner's "measure first").
  * **The dot shows the shop sign**; a sign read as a person's own name, or a
    blank one, shows the class instead (config.PERSON_NAMED, keys). The
    street and number are never read.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.belgium_logic import build_businesses  # noqa: E402
from pipeline.liege import config  # noqa: E402


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    build_businesses(config)
