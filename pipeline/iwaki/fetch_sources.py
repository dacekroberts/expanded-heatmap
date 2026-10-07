"""Download everything Iwaki's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/iwaki/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's 保健所 生活衛生課 lists (CC BY 4.0): the food list of
              permits in term on 2026-03-31, the five monthly lists of new
              food permits (April to August 2026), and the barber and beauty
              list as of 2026-05-31 with its four monthly lists of new
              premises (June to September 2026);
  * isj     - MLIT 位置参照情報 for the one municipality (07204), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Fukushima administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (every city file and the ISJ files were
downloaded at Step 0, 2026-10-06) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/iwaki/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.iwaki import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
