"""Download everything Shizuoka's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/shizuoka/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's 生活衛生 registers on BODIK (organization 221007,
              CC BY 4.0 under the city's terms): the barber, beauty-salon and
              laundry lists as of 2026-03-31 and each trade's monthly files of
              new permits since (config._LISTS). BODIK rate-limits: a re-fetch
              of more than one file is spaced at least 20 s apart by hand;
  * isj     - MLIT 位置参照情報 for the three wards (22101 to 22103), block
              (24.0a) and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Shizuoka administrative areas,
              into the country's shared cache data/japan/raw/ (N02 PDL 1.0,
              N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the lists and the ISJ files were downloaded
at Step 0, 2026-10-05; the barber list and the two September files on
2026-10-11) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/shizuoka/provenance.json
(bytes, sha256, when). The work is pipeline/countries/japan_fetch.py, shared
by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.shizuoka import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
