"""Download everything Kōchi's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/kochi/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's full barber and beauty-salon lists (理容所一覧,
              美容所一覧, as of 2026-03-31) and their monthly additions to
              2026-08-31 (CC BY 4.0, 生活衛生営業施設情報（高知市オープンデータ）);
  * isj     - MLIT 位置参照情報 for 39201, block (24.0a) and town-chōme (19.0b)
              (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Kōchi administrative areas, into the
              country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY 4.0);
  * osm     - OpenStreetMap station and tram-stop names in the city's box
              (ODbL), through pipeline/osm.py;
  * control - the Economic Census table (shared cache; the food control, which
              does not apply to this page, kept for the shared tooling).

A file already on disk is kept (the city's lists and the ISJ files were
downloaded at Step 0, 2026-10-02) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/kochi/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.kochi import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
