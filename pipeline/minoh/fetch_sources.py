"""Download everything Minoh's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/minoh/fetch_sources.py [city|isj|mlit|osm|control|all] [--force]

  * city    - Osaka Prefecture's 理容所届出施設一覧 and 美容所届出施設一覧 from BODIK (XLSX:
              each kind's full list as of 2026-03-31 and five monthly new-premises files,
              the 32 municipalities the prefecture licenses; CC BY 4.0), cut to Minoh by
              step 2;
  * isj     - MLIT 位置参照情報 for the one municipality (27220), block (24.0a)
              and town-chōme (19.0b) (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Osaka administrative areas,
              into the country's shared cache data/japan/raw/ (N02 PDL 1.0,
              N03 CC BY 4.0);
  * osm     - OpenStreetMap station names in the city's box (ODbL), through
              pipeline/osm.py;
  * control - the Economic Census table for the join control (shared cache).

The prefecture's twelve files were fetched at Step 0 (2026-10-06) into
data/osaka_pref/raw/ and copied unchanged here (Ibaraki, Moriguchi and Kadoma
read the same files); BODIK rate-limits, so a re-fetch is one file at a time,
20 s apart. A file already on disk is kept and recorded, dated by its
modification time; --force re-downloads. Each file is recorded in
outputs/minoh/provenance.json (bytes, sha256, when). The work is
pipeline/countries/japan_fetch.py, shared by every Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.minoh import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
