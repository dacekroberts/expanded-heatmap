"""Download everything Mito's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/mito/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - MHLW's open data for Mito (PDL 1.0), the city's food list; the
              city's barber, beauty-salon, general-laundry and laundry
              pick-up-counter lists from its 生活衛生関係施設一覧 page (CC-BY,
              no version given);
  * isj     - MLIT 位置参照情報 for the one municipality (08201), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Ibaraki administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (every city file and the ISJ files were
downloaded at Step 0, 2026-10-06) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/mito/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.mito import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
