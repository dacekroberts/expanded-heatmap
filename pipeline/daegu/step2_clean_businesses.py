"""Daegu step 2: fourteen permit registers -> one row per storefront premises.

Seoul's rules through pipeline/countries/korea.py, which resolves Daegu's
renamed columns and raises on the ones Seoul's code would read as nothing:

  1. Read each register's header, resolve every field by the names it is
     published under, and read ONLY those columns - the telephone column
     (소재지전화) is never loaded (asserted). Keep 영업/정상 (open) rows.
  2. Bucket with the korea_localdata taxonomy, the register keyed by its permit
     type; the sub-type taken per row (업태구분명, else 위생업태명 - the health-
     food file's 업태구분명 is blank on every row).
  3. Place each on its own point (EPSG:5174 -> WGS84), else a donor's at the
     same building, keyed 구 or 군 (달성군, 군위군).
  4. One pin per premises, and 5. the Korean privacy pass - as Seoul.

Reads the cache and NEVER fetches.

    python pipeline/daegu/step2_clean_businesses.py
"""
import sys
import warnings
from pathlib import Path

import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import korea  # noqa: E402
from pipeline.daegu import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402

TO_WGS = Transformer.from_crs(config.CRS_REGISTER, config.CRS_GEOGRAPHIC, always_xy=True)
# openpyxl warns that the portal's workbooks carry no default style; harmless.
warnings.filterwarnings("ignore", message="Workbook contains no default style")


def read_register(k):
    permit_type = config.REGISTERS[k][0]
    path = config.register_xlsx(k)
    if not path.exists():
        sys.exit(f"missing {path}.\nRun: python pipeline/daegu/fetch_sources.py registers")
    header = pd.read_excel(path, nrows=0).columns
    picked = korea.columns_to_read(header, path.name, config.NEVER_READ)
    raw = pd.read_excel(path, dtype=str, usecols=list(picked.values()))
    df = korea.normalise(raw, picked, path.name, config.NEVER_READ, permit_type)
    return korea.building_keys(df, config.CITY_PREFIX, path.name,
                               masked_ok=k in config.MASKED_ADDRESS_FILES)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    registers = {k: read_register(k) for k in config.REGISTERS}
    out = korea.build_storefronts(registers, config.ACTIVE_STATUS, TO_WGS,
                                  config.DAEGU_BBOX, config.COORD_DONORS)
    kept = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(kept) != len(out):
        sys.exit("filter_to_storefront dropped rows the buckets already decided")
    emit("storefronts", len(kept))
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    kept.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(kept):,} storefronts")


if __name__ == "__main__":
    main()
