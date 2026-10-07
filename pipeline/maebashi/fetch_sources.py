"""Download everything Maebashi's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/maebashi/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - MHLW's open data for Maebashi (PDL 1.0); the city's food file
              from its former system (CC BY 4.0) and its 生活衛生 registers'
              base zip and ten monthly new and closed zips (CC BY 2.1 JP), on
              BODIK (a monthly zip's URL read from the dataset page by its
              file name, config.SOURCE_LINKS);
  * isj     - MLIT 位置参照情報 for the one municipality (10201), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Gunma administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (every city file and the ISJ files were
downloaded at Step 0, 2026-10-04 and 2026-10-05) and recorded, dated by its
modification time; --force re-downloads. Each file is recorded in
outputs/maebashi/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.maebashi import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
