"""Download everything Suita's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/suita/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's 衛生管理課 open data (CC BY 4.0): the two food lists
              of 2026-03-31 (revised law and old law) and the barber, beauty
              and laundry registers of 2026-08-31; MHLW's 食品衛生申請等システム
              open data for the city (27205; PDL 1.0);
  * isj     - MLIT 位置参照情報 for the one municipality (27205), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Osaka administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
              CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (every city file was downloaded at Step 0,
2026-10-06) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/suita/provenance.json (bytes,
sha256, when). The work is pipeline/countries/japan_fetch.py, shared by every
Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.suita import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
