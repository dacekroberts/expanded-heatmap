"""Download everything Takatsuki's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/takatsuki/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - MHLW's 食品衛生申請等システム open-data file for Takatsuki (27207; UTF-8
              CSV, PDL 1.0);
  * isj     - MLIT 位置参照情報 for the one municipality (27207), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Osaka administrative areas,
              into the country's shared cache data/japan/raw/ (N02 PDL 1.0,
              N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

MHLW's file was fetched at Step 0 (2026-10-06). A file already on disk is kept
and recorded, dated by its modification time; --force re-downloads. Each file
is recorded in outputs/takatsuki/provenance.json (bytes, sha256, when). The
work is pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.takatsuki import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
