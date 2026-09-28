"""Download everything Fukuoka's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/fukuoka/fetch_sources.py [city|isj|mlit|osm|all] [--force]

  * city  - Fukuoka City's food list (permits from before 2021-06) and its
            barber, beauty and laundry registers, from data.bodik.jp (CC BY
            4.0); and MHLW's 食品衛生申請等システム open data for the city
            (40130, PDL 1.0), a plain GET;
  * isj   - MLIT 位置参照情報 for the 7 wards, block (24.0a) and town-chōme
            (19.0b) (PDL 1.0);
  * mlit  - MLIT N02 railways and N03 Fukuoka Prefecture administrative areas,
            into the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
            CC BY 4.0);
  * osm   - OpenStreetMap station names in the city's box (ODbL), through
            pipeline/osm.py.

BODIK answered 500, 502 and 504 on the day of the brief (2026-09-24):
japan_fetch.get retries with backoff, and a failure there is not a dead source
- re-run before concluding anything.

A file already on disk is kept (most were downloaded during screening,
2026-09-24 to 09-27) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/fukuoka/provenance.json (bytes,
sha256, when). The work is pipeline/countries/japan_fetch.py, shared by every
Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.fukuoka import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
