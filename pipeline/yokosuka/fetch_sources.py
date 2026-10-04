"""Download everything Yokosuka's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/yokosuka/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's food-permit list and its barber, beauty-salon and two
              laundry lists (CC BY 4.0) on BODIK, each read from its CKAN
              resource's current URL, since every file is renamed each month
              (config.SOURCE_RESOURCES);
  * isj     - MLIT 位置参照情報 for the one municipality (14201), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Kanagawa administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the city's lists and the ISJ files were
downloaded at Step 0, 2026-10-02) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/yokosuka/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.yokosuka import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
