"""Download everything Matsumoto's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/matsumoto/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's 生活衛生 registers on LinkData.org (work rdf1s8757i,
              published by 松本市 DX推進本部; marked CC BY 3.0 there, CC BY 4.0
              under the city's terms): the barber, beauty-salon and laundry
              tables as of 2026-10-01, saved under dated names
              (config.SOURCE_FILES). LinkData overwrites a table in place, so
              --force replaces the edition: re-read the work page's date and
              rename the files first;
  * isj     - MLIT 位置参照情報 for 20202, block (24.0a) and town-chōme
              (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Nagano administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
              CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the ISJ files were downloaded at Step 0,
2026-10-06; the three register tables on 2026-10-11) and recorded, dated by
its modification time; --force re-downloads. Each file is recorded in
outputs/matsumoto/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.matsumoto import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
