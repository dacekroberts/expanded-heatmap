"""Hong Kong step 2: FEHD's licensed storefronts, at FEHD's own points.

  1. Read the three daily XML registers - what is licensed today (their own
     GENERATION_DATE, their own code lists).
  2. Keep the storefront licence types (pipeline/taxonomies/hong_kong_fehd.py).
  3. Place each licence at FEHD's point for it, from the same register on the
     CSDI portal, joined by LICENCE NUMBER. A licence with no point there yet is
     left off and counted - never placed by guessing from its address.
  4. One pin per premises: the same shop sign at the same address is one
     storefront however many licences it holds.

Reads the cache and NEVER fetches.

    python pipeline/hong_kong/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.hong_kong import config  # noqa: E402
from pipeline.hong_kong.register import read_points, read_register  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.hong_kong_fehd import CODE_TO_BUCKET, STOREFRONT_CODES  # noqa: E402

BUCKET_RANK = {"Food service": 0, "Retail": 1, "Personal services": 2}


def need(path):
    if not path.exists():
        sys.exit(f"missing {path}.\nRun: python pipeline/hong_kong/fetch_sources.py registers")


def main():
    rows, gens, points = [], {}, {}
    for name, fname in config.FEHD_FILES.items():
        need(config.DATA_RAW / fname)
        need(config.DATA_RAW / f"csdi_{config.CSDI_LAYERS[name][1]}.geojson")
        regs, gen, types, dists = read_register(name)
        pts, n_feats, dup = read_points(name)
        gens[name] = gen
        print(f"  {name:<12} register {len(regs):>6,} licences (generated {gen}); CSDI {n_feats:>6,} "
              f"records, {len(pts):>6,} with a point, {dup} repeated licence numbers")
        points.update({(name, k): v for k, v in pts.items()})
        for r in regs:
            code = r["TYPE"]
            if code not in CODE_TO_BUCKET:
                sys.exit(f"unmapped licence code {code!r} ({types.get(code)}) in {name}")
            rows.append({"register": name, "licence_code": code, "licence_type": types.get(code, code),
                         "licence_no": r["LICNO"], "business_name": r["SS"], "address": r["ADR"],
                         "district": dists.get(r["DIST"], r["DIST"]), "expires": r["EXPDATE"]})
    df = pd.DataFrame(rows)
    print(f"Registers: {len(df):,} licences")
    emit("licences", len(df))
    exp = pd.to_datetime(df["expires"], format="%Y-%m-%d", errors="coerce")
    print(f"  expiry unreadable on {int(exp.isna().sum())}; expired before generation: "
          f"{int((exp < pd.Timestamp(max(gens.values()))).sum())}")

    df = df[df["licence_code"].isin(STOREFRONT_CODES)].copy()
    print(f"  storefront licence types: {len(df):,}  "
          + ", ".join(f"{k} {v:,}" for k, v in df["licence_code"].value_counts().items()))
    emit("storefront_licences", len(df))
    # FEHD files food trucks under their own "district": a licence for a
    # vehicle, not a premises, and its "address" is a pitch.
    truck = df["district"].eq(config.FOOD_TRUCK_DISTRICT)
    print(f"  food trucks (a vehicle, not a premises): {int(truck.sum())} - left out")
    emit("food_trucks", int(truck.sum()))
    df = df[~truck].copy()

    # --- FEHD's own point, by licence number -----------------------------------
    hit = [points.get((reg, lic)) for reg, lic in zip(df["register"], df["licence_no"])]
    df["latitude"] = [h[0] if h else None for h in hit]
    df["longitude"] = [h[1] if h else None for h in hit]
    df["csdi_code"] = [h[2] if h else None for h in hit]
    missing = df["latitude"].isna()
    print(f"\n  placed at FEHD's own point: {int((~missing).sum()):,}; no point on CSDI yet: "
          f"{int(missing.sum()):,} ({missing.mean():.2%}) - left off")
    emit("no_csdi_point", int(missing.sum()))
    df = df[~missing].copy()
    wrong_type = df["csdi_code"].ne(df["licence_code"])
    if wrong_type.any():
        sys.exit(f"{int(wrong_type.sum())} licence numbers carry a different type on CSDI - read them")
    b = config.HONG_KONG_BBOX
    inside = df["latitude"].between(b["lat_min"], b["lat_max"]) & df["longitude"].between(b["lon_min"], b["lon_max"])
    if (~inside).any():
        sys.exit(f"{int((~inside).sum())} CSDI points outside the SAR's box - read them")

    # --- one pin per premises --------------------------------------------------
    df["rank"] = df["licence_code"].map(CODE_TO_BUCKET).map(BUCKET_RANK)
    df = df.sort_values(["rank", "licence_no"])
    key = df["business_name"].str.upper().str.strip() + "|" + df["address"].str.upper().str.strip()
    dup = key.duplicated()
    print(f"  {int(dup.sum()):,} licences are a second licence at the same shop sign and address "
          f"- one pin per premises, the first-ranked licence kept")
    emit("second_licences", int(dup.sum()))
    df = df[~dup].copy()

    # FEHD's placeholder where a licence carries no shop sign ("No Record",
    # "(no record found)") is not a name, and a tooltip must not read as one.
    nosign = df["business_name"].str.strip().str.match(r"(?i)^\(?\s*no\s+record(\s+found)?\s*\)?$")
    df.loc[nosign, "business_name"] = config.NO_SHOP_SIGN
    print(f"  {int(nosign.sum()):,} licences carry FEHD's no-record placeholder for a shop sign - "
          f"shown as {config.NO_SHOP_SIGN!r}")
    emit("no_shop_sign", int(nosign.sum()))

    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    if len(df) != before:
        sys.exit("filter_to_storefront disagrees with the taxonomy's own storefront codes")
    print(f"\n  {len(df):,} storefronts: " + ", ".join(
        f"{k} {n:,}" for k, n in df["licence_code"].map(CODE_TO_BUCKET).value_counts().items()))
    emit("storefronts", len(df))
    out = df[["licence_no", "business_name", "address", "district", "latitude", "longitude",
              "licence_type", "licence_code"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
