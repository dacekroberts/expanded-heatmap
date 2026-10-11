"""Download everything Gifu's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/gifu/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Gifu City's food permit and notification lists (c212016-072)
              and its barber and beauty registers (c212016-075), CC BY 2.0,
              from Gifu Prefecture's CKAN (gifu-opendata.pref.gifu.lg.jp);
  * isj     - MLIT 位置参照情報 for the one municipality (21201), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Gifu administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (every city file and the ISJ files were
downloaded at Step 0, 2026-10-06) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/gifu/provenance.json (bytes, sha256, when). MHLW's open data for 21201
is a control only and is not fetched here. The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.gifu import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
