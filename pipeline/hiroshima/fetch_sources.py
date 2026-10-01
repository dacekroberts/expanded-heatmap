"""Download everything Hiroshima's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/hiroshima/fetch_sources.py [city|isj|mlit|osm|all] [--force]

  * city  - the city's full list of counter-application food permits
            (食品営業許可施設一覧（令和8年3月末時点）; PDL 1.0 through DataEye) and
            MHLW's 食品衛生申請等システム open data for Hiroshima City (PDL 1.0);
  * isj   - MLIT 位置参照情報 for the 8 wards, block (24.0a) and town-chōme
            (19.0b) (PDL 1.0);
  * mlit  - MLIT N02 railways and N03 Hiroshima administrative areas, into the
            country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY 4.0);
  * osm   - OpenStreetMap station and tram-stop names in the city's box (ODbL),
            through pipeline/osm.py.

A file already on disk is kept (the city's list and the ISJ files were
downloaded during screening, 2026-09-24) and recorded, dated by its
modification time; --force re-downloads. Each file is recorded in
outputs/hiroshima/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.hiroshima import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
