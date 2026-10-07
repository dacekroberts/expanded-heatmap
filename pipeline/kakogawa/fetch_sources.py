"""Download everything Kakogawa's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/kakogawa/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Hyōgo Prefecture's food permit and notification lists and its
              barber, beauty-salon and laundry registers (XLSX, the whole
              prefecture less its five health-centre cities; CC BY 4.0 through
              the catalogue's terms), cut to Kakogawa by step 2;
  * isj     - MLIT 位置参照情報 for the one municipality (28210), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Hyōgo administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC
              BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

The prefecture's files were fetched at Step 0 (2026-10-06) into
data/hyogo_pref/raw/ and copied unchanged here (Kakogawa reads the same
files). A file already on disk is kept and recorded, dated by its
modification time; --force re-downloads. Each file is recorded in
outputs/kakogawa/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.kakogawa import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
