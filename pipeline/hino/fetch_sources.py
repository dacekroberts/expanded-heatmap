"""Download everything Hino's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/hino/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the Tokyo Metropolitan Government's five Tama ledgers (CC BY 4.0
              through the Tokyo catalogue) and MHLW's Tokyo file (13000; PDL
              1.0), each cut to the city by step 2 (pipeline/countries/tokyo_tama.py);
  * isj     - MLIT 位置参照情報 for the one municipality (13212), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Tokyo administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the ledgers and MHLW's file were copied
unchanged from data/tokyo_tama/raw/, and the ISJ pair downloaded into
data/hino/raw/isj/ for the brief, 2026-10-06) and recorded, dated by
its modification time; --force re-downloads. Each file is recorded in
outputs/hino/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.hino import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
