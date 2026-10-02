"""Download everything Nagasaki's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/nagasaki/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's BODIK lists (CC BY 4.0): the food permits in force on
              2023-06-30 and the barber, beauty-salon and laundry lists to
              2023-03-31; and MHLW's 食品衛生申請等システム open data for
              Nagasaki (PDL 1.0), current. NEVER the city's own 2026 list
              (64426.xlsx), which is not permitted without its permission;
  * isj     - MLIT 位置参照情報 for 42201, block (24.0a) and town-chōme (19.0b)
              (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Nagasaki administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
              CC BY 4.0);
  * osm     - OpenStreetMap station and tram-stop names in the city's box
              (ODbL), through pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the BODIK lists, MHLW's file and the ISJ files
were downloaded at Step 0, 2026-10-02) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/nagasaki/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.nagasaki import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
