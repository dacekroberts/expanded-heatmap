"""Download everything Tsu's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/tsu/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Mie Prefecture's food-permit list and its barber and
              beauty-salon registers on BODIK (CC BY 4.0), three XLSX files
              all published as 202608.xlsx and saved under their own names;
              each covers the prefecture except Yokkaichi, and step 2 cuts
              Tsu's rows by address (config.source_rows);
  * isj     - MLIT 位置参照情報 for the one municipality (24201), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Mie administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

MHLW's open data for Mie (24000_food_business_all.csv, in data/tsu/raw/ from
Step 0) is a control the brief measured, read by no step, so it is not
fetched or recorded here.

A file already on disk is kept (every list and the ISJ files were downloaded
at Step 0, 2026-10-06) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/tsu/provenance.json (bytes,
sha256, when). The work is pipeline/countries/japan_fetch.py, shared by every
Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.tsu import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
