"""Download everything Naha's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/naha/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Naha City's three BODIK packages from data.bodik.jp (CC BY 4.0),
              each resource pinned by id in pipeline/naha/bodik_files.py: the
              monthly new food permits (shinki_syokuhin, 140 workbooks,
              2015-04 to 2026-08), the monthly renewals
              (472018_keizoku_syokuhin, 73 workbooks, 2015-04 to 2021-05) and
              the barber and beauty-salon registers as of 2026-09-04
              (472018_ribiyou). BODIK's copies only, never the city site's
              own files, and one file every 21 s (config.FETCH_PAUSE_S):
              BODIK rate-limits;
  * isj     - MLIT 位置参照情報 for the one municipality (47201), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Okinawa administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC
              BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the food workbooks were downloaded on
2026-10-11, the registers and the MLIT address files on 2026-10-12) and
recorded, dated by its modification time; --force re-downloads. Each file is
recorded in outputs/naha/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.naha import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
