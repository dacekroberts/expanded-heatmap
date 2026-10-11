"""Download everything Kanazawa's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/kanazawa/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city catalogue's 食品衛生関係営業許可施設一覧
              (catalog-data.city.kanazawa.ishikawa.jp, cc-by under the city's
              open-data terms): the datastore dump of resource 09a49521, the
              resource page's own download link (its upload path answers
              HTTP 500), a snapshot of the permits in term in early April
              2024;
  * isj     - MLIT 位置参照情報 for 17201, block (24.0a) and town-chōme
              (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Ishikawa administrative areas,
              into the country's shared cache data/japan/raw/ (N02 PDL 1.0,
              N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the list and the ISJ files were downloaded at
Step 0, 2026-10-05) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/kanazawa/provenance.json
(bytes, sha256, when). The work is pipeline/countries/japan_fetch.py, shared
by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.kanazawa import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
