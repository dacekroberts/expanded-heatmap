"""Download everything Okazaki's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/okazaki/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's 食品等営業許可・届出一覧 on BODIK (organization 232025,
              CC BY 4.0 under the city's terms): one CSV of every food permit
              in term, replaced in place; and MHLW's 食品衛生申請等システム open
              data for 23202 (PDL 1.0). BODIK rate-limits: a re-fetch is
              spaced at least 20 s from any other BODIK request by hand;
  * isj     - MLIT 位置参照情報 for 23202, block (24.0a) and town-chōme
              (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Aichi administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
              CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the two lists and the ISJ files were
downloaded at Step 0, 2026-10-06) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/okazaki/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.okazaki import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
