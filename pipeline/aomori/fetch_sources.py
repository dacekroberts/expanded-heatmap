"""Download everything Aomori's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/aomori/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's 食品営業許可施設一覧 (保健所 生活衛生課, CC BY 4.0 through
              青森市オープンデータ利用規約): r0808zendate.csv, every food permit
              in term on 2026-08-31, from the city's own host;
  * isj     - MLIT 位置参照情報 for 02201, block (24.0a) and town-chōme
              (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Aomori administrative areas,
              into the country's shared cache data/japan/raw/ (N02 PDL 1.0,
              N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the list and the ISJ files were downloaded at
Step 0, 2026-10-06) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/aomori/provenance.json (bytes,
sha256, when). MHLW's 02201 file, cached beside the list at Step 0, is a
control read by no step and is not fetched here. The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.aomori import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
