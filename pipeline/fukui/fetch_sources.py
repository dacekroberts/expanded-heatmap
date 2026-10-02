"""Download everything Fukui's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/fukui/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's month-end food-permit workbook and its barber,
              beauty-salon and laundry workbooks, the newest sheet as of
              2026-08-31 (福井市, CC BY-SA, the site default);
  * isj     - MLIT 位置参照情報 for 18201, block (24.0a) and town-chōme (19.0b)
              (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Fukui administrative areas, into the
              country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY 4.0);
  * osm     - OpenStreetMap station and tram-stop names in the city's box
              (ODbL), through pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the city's workbooks and the ISJ files were
downloaded at Step 0, 2026-10-02) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/fukui/provenance.json (bytes, sha256, when); its row count is every
sheet's (the shared fetch reads the whole workbook), twelve months over, while
step 2 reads the newest sheet only. The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.fukui import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
