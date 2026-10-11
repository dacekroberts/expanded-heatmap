"""Download everything Kawaguchi's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/kawaguchi/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - the city's food CSV (食品等営業許可・届出一覧: the full list of
              permits and notifications on 2026-03-31 with the new premises of
              April, May and July 2026 stacked in one file; CC BY 2.1 JP, the
              city's own site);
  * isj     - MLIT 位置参照情報 for the one municipality (11203), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Saitama administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0); step 1 also reads Tokyo's N03 (config.N03_NEIGHBOR_PREFS),
              which Tokyo's fetch caches;
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

A file already on disk is kept (the food CSV and the ISJ files were downloaded
at Step 0, 2026-10-06) and recorded, dated by its modification time; --force
re-downloads. The CSV on disk is the edition of 2026-08-19 (2,095,941 bytes);
the city has since published a newer one, and config.source_rows stops on any
edition it was not measured for. Each file is recorded in
outputs/kawaguchi/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.kawaguchi import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
