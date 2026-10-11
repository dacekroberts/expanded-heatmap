"""Download everything Amagasaki's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/amagasaki/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's own open data (CC BY 4.0), from
              www.city.amagasaki.hyogo.jp: the food permit and notification
              lists of 2026-08-31 (renamed each month, so a re-download reads
              the current link from the page) and the barber, beauty and
              laundry registers of 2026-08-31;
  * isj     - MLIT 位置参照情報 for the one municipality (28202), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Hyōgo administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
              CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

MHLW's open data for 28202 is a control read at the brief, never a source,
so it is not fetched here. A file already on disk is kept (every city file
was downloaded at Step 0, 2026-10-06) and recorded, dated by its
modification time; --force re-downloads. Each file is recorded in
outputs/amagasaki/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.amagasaki import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
