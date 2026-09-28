"""Download everything Kobe's pipeline reads. NOT a step: drift_check.py never
runs this file, and every step exits naming it when its cache is missing.

    python pipeline/kobe/fetch_sources.py [city|isj|mlit|osm|all] [--force]

  * city  - Kobe City's food-permit list and its barber, beauty and laundry
            registers (生活衛生関係許可施設等の情報提供; CC BY 2.1 JP);
  * isj   - MLIT 位置参照情報 for the 9 wards, block (24.0a) and town-chōme
            (19.0b) (PDL 1.0);
  * mlit  - MLIT N02 railways and N03 Hyōgo administrative areas, into the
            country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY 4.0);
  * osm   - OpenStreetMap station names in the city's box (ODbL), through
            pipeline/osm.py.

A file already on disk is kept (most were downloaded during screening,
2026-09-24) and recorded, dated by its modification time; --force re-downloads.
Each file is recorded in outputs/kobe/provenance.json (bytes, sha256, when).
The work is pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.kobe import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
