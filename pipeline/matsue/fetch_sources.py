"""Download everything Matsue's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/matsue/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - 松江市's 生活衛生 registers on Shimane Prefecture's portal
              (shimane-opendata.jp, PDL 1.0): the barber, beauty-salon and
              laundry lists as of 2026-08-31 (resources 76779, 76780 and
              76781; config._LISTS). The portal gives each month's list a new
              resource id, so the URLs are pinned to this edition;
  * isj     - MLIT 位置参照情報 for 32201, block (24.0a) and town-chōme
              (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Shimane administrative areas,
              into the country's shared cache data/japan/raw/ (N02 PDL 1.0,
              N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache;
              this page has no food leg, so no step reads it).

A file already on disk is kept (the three lists and the ISJ files were
downloaded at Step 0, 2026-10-06) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/matsue/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.matsue import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
