"""Download everything Sōka's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/soka/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Saitama Prefecture's files, into the shared
              data/saitama_pref/raw/ (saitama_pref.fetch): the live new-law and
              old-law food layers (queried whole and paged, never 電話番号), the
              R8.3.31 old-law list, the FY-end 生活衛生 list and the months to
              2026-08 (PDL 1.0 through the GIS catalogue and the portal's
              record, calls 143 and 171);
  * isj     - MLIT 位置参照情報 for the one municipality (11221), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Saitama administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (every file here was downloaded at Step 0,
2026-10-06) and recorded, dated by its modification time; --force re-downloads,
except a food layer, whose refresh is a new dated file. Each file is recorded
in outputs/soka/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city, with
saitama_pref.fetch in place of its plain-GET "city" part. MHLW's 11000 file in
data/soka/raw/ is a Step 0 control only, never a source.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch, saitama_pref  # noqa: E402
from pipeline.soka import config  # noqa: E402

if __name__ == "__main__":
    # The layers need a paged query, which japan_fetch's plain GET would cut
    # at its first page
    japan_fetch.PARTS["city"] = saitama_pref.fetch
    japan_fetch.main(config, __doc__)
