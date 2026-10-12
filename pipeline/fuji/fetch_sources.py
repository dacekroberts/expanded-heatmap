"""Download everything Fuji's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/fuji/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Shizuoka Prefecture's 生活衛生 registers on its open-data portal
              (opendata.pref.shizuoka.jp, datasets 11261 to 11263, author
              衛生課, CC BY): the barber, beauty-salon and laundry lists as of
              2026-03-31 and each trade's monthly files of new premises,
              April to August 2026 (config._LISTS: 18 files). The portal
              answered HTTP 429 to the nineteenth request of a run spaced 2 s
              apart (Step 0, 2026-10-06): a re-fetch of more than a few files
              is spaced by hand, 5 s or more, and waits 60 s after a 429;
  * isj     - MLIT 位置参照情報 for 22210, block (24.0a) and town-chōme
              (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Shizuoka administrative areas,
              into the country's shared cache data/japan/raw/ (N02 PDL 1.0,
              N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the lists and the ISJ files were downloaded
at Step 0, 2026-10-06) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/fuji/provenance.json (bytes,
sha256, when). The work is pipeline/countries/japan_fetch.py, shared by every
Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.fuji import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
