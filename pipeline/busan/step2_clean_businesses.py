"""Busan step 2: fourteen permit types -> one row per storefront premises.

Seoul's rules through pipeline/countries/korea.py, as Daegu's. Busan's rows are
the LocalDataService API's own JSON, fields in lowercase codes; they are renamed
to the published names korea.FIELDS resolves (config.FIELD_RENAME), and the
module does the rest:

  1. Resolve every field by name and keep only those; the telephone field
     (sitetel) is never loaded (asserted). Keep 영업/정상 (open) rows - the pulls
     are FULL, never state-filtered (a state filter drops every permit since
     2025-02).
  2. Bucket with the korea_localdata taxonomy, the register keyed by its permit
     type; the sub-type taken per row (uptaenm, else sntuptaenm - the health-
     food channel is in sntuptaenm, and salons' sntuptaenm holds combined
     values, so uptaenm must win where it has one).
  3. Place each on its own point (EPSG:5174 -> WGS84), else a donor's at the
     same building, keyed 구 or 군 (기장군).
  4. One pin per premises, and 5. the Korean privacy pass - as Seoul.

Reads the cache and NEVER fetches.

    python pipeline/busan/step2_clean_businesses.py
"""
import json
import sys
from pathlib import Path

import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.busan import config  # noqa: E402
from pipeline.countries import korea  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402

TO_WGS = Transformer.from_crs(config.CRS_REGISTER, config.CRS_GEOGRAPHIC, always_xy=True)


def read_register(k):
    permit_type, _, svc = config.REGISTERS[k]
    path = config.register_json(k)
    if not path.exists():
        sys.exit(f"missing {path}.\nRun: python pipeline/busan/fetch_sources.py registers")
    rows = json.loads(path.read_text(encoding="utf-8"))
    if {r.get("opnsvcid") for r in rows} != {svc}:
        sys.exit(f"{path.name}: not a pull of {svc} alone")
    header = sorted({f for r in rows for f in r})
    # The API's codes under the published names; any other field keeps its code,
    # so korea.columns_to_read still sees (and refuses) an unguarded phone field.
    renamed = [config.FIELD_RENAME.get(f, f) for f in header]
    picked = korea.columns_to_read(renamed, path.name, config.NEVER_READ)
    back = {v: k2 for k2, v in config.FIELD_RENAME.items()}
    cols = [back.get(c, c) for c in picked.values()]
    # A null field reads as "", never as the text "None".
    raw = pd.DataFrame([{c: ("" if r.get(c) is None else str(r.get(c))) for c in cols}
                        for r in rows])
    raw = raw.rename(columns=config.FIELD_RENAME)
    df = korea.normalise(raw, picked, path.name, config.NEVER_READ, permit_type)
    return korea.building_keys(df, config.CITY_PREFIX, path.name,
                               masked_ok=k in config.MASKED_ADDRESS_FILES)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    registers = {k: read_register(k) for k in config.REGISTERS}
    out = korea.build_storefronts(registers, config.ACTIVE_STATUS, TO_WGS,
                                  config.BUSAN_BBOX, config.COORD_DONORS)
    kept = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(kept) != len(out):
        sys.exit("filter_to_storefront dropped rows the buckets already decided")
    emit("storefronts", len(kept))
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    kept.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(kept):,} storefronts")


if __name__ == "__main__":
    main()
