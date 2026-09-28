"""Download everything Tokyo's pipeline reads. NOT a step: drift_check.py never
runs this file, and every step exits naming it when its cache is missing.

    python pipeline/tokyo/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - each active ward's food list and registers (the roster,
              pipeline/tokyo/wards.py: the Tokyo catalogue's, the wards' own
              sites, Shibuya's ArcGIS site and Meguro's BODIK, each CC BY 4.0
              under its own terms), and MHLW's 食品衛生申請等システム open data
              for Chūō, Minato, Shinjuku and Kōtō (PDL 1.0), plain GETs;
  * isj     - MLIT 位置参照情報 for the active wards, block (24.0a) and
              town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02 railways and N03 Tokyo's administrative areas, into the
              country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY 4.0);
  * osm     - OpenStreetMap station and tram-stop names in the 23 wards' box
              (ODbL), through pipeline/osm.py;
  * control - the 2021 Economic Census table (e-Stat), the join control.

A file already on disk is kept (every ward file was downloaded during the
2026-09-24 screen and the 2026-09-28 research) and recorded, dated by its
modification time; --force re-downloads. Each file is recorded in
outputs/tokyo/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.tokyo import config  # noqa: E402

if __name__ == "__main__":
    # no wards.check() here: the fetch is what supplies a missing file
    japan_fetch.main(config, __doc__)
