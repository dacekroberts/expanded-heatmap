"""Download everything Sagamihara's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/sagamihara/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's food-permit list of 2026-03-31 and its monthly zip of
              new and closed permits (April to August 2026), its barber and
              beauty registers of 2026-03-31 with their monthly new and closed
              zips, and its laundry register of 2026-03-31 (CC BY 4.0, the
              city's own CKAN catalogue), each a zip of CSV and PDF read from
              its resource's current URL, since every resource is replaced in
              place (config.SOURCE_RESOURCES);
  * isj     - MLIT 位置参照情報 for the three wards (14151-14153), block
              (24.0a) and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Kanagawa administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0); the N03 files of Tokyo and Yamanashi, which name the
              stations beyond the city line, are in the same cache;
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the city's lists and the ISJ files were
downloaded at Step 0, 2026-10-04) and recorded, dated by its modification
time; --force re-downloads. Each file is recorded in
outputs/sagamihara/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.sagamihara import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
