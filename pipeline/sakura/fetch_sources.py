"""Download everything Sakura's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/sakura/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Chiba Prefecture's files, into the shared data/chiba_pref/raw/
              (chiba_pref.fetch): the barber list (as of 2025-03-31), the
              beauty and laundry lists (2026-03-31) and their monthly
              新規施設 files of 2026-04 to 2026-08, from
              opendata.pref.chiba.lg.jp only (PDL 1.0);
  * isj     - MLIT 位置参照情報 for the one municipality (12212), block (24.0a)
              and town-chome (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Chiba administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the thirteen workbooks and the ISJ files were
downloaded at Step 0, 2026-10-05 and 06, the workbooks copied into the shared
Chiba cache at Matsudo's build, 2026-10-11) and recorded, dated by its modification time;
--force re-downloads, except a Chiba workbook, whose new edition is a new file
under a new name. Each file is recorded in outputs/sakura/provenance.json
(bytes, sha256, when). The work is pipeline/countries/japan_fetch.py, shared
by every Japanese city, with chiba_pref.fetch in place of its plain-GET "city"
part.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import chiba_pref, japan_fetch  # noqa: E402
from pipeline.sakura import config  # noqa: E402

if __name__ == "__main__":
    # The files live in the shared Chiba cache and are counted sheet by sheet,
    # which japan_fetch's own "city" part does not do
    japan_fetch.PARTS["city"] = chiba_pref.fetch
    japan_fetch.main(config, __doc__)
