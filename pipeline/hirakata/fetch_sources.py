"""Download everything Hirakata's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/hirakata/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's lists from www.city.hirakata.osaka.jp (CC BY 2.1 JP):
              the food list of every permit in term on 2026-03-31 and the
              monthly new-permit files of April to August 2026 (page
              0000023479); the barber, beauty and laundry registers as of the
              end of March 2026 and their monthly new-premises files (beauty
              April to July, barbers July; page 0000025284); MHLW's
              食品衛生申請等システム open data for the city (27210; PDL 1.0);
  * isj     - MLIT 位置参照情報 for the one municipality (27210), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Osaka administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC
              BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the food lists, the March registers and
MHLW's file were downloaded at Step 0, 2026-10-06; the registers' months at
the build, 2026-10-07, owner's call 155) and recorded, dated by its
modification time; --force re-downloads. Each file is recorded in
outputs/hirakata/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.hirakata import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
