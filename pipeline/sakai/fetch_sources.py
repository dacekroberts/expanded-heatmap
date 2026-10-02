"""Download everything Sakai's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/sakai/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's food-permit list as of 2026-04-01 (R80401.csv), its
              monthly new-permit and closure files for April to August 2026
              (R0804.csv ... R0808haigyou.csv; CC BY 4.0, 堺市オープンデータ
              利用規約), and MHLW's 食品衛生申請等システム open data for Sakai
              (PDL 1.0);
  * isj     - MLIT 位置参照情報 for the 7 wards (27141-27147), block (24.0a) and
              town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Osaka administrative areas, into the
              country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY 4.0);
  * osm     - OpenStreetMap station and tram-stop names in the city's box
              (ODbL), through pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the city's files, MHLW's file and the ISJ files
were downloaded at Step 0, 2026-10-02) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/sakai/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.sakai import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
