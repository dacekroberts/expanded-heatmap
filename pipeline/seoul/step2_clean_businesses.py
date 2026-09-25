"""Seoul step 2: seventeen permit registers -> one row per storefront premises.

  1. Read each register by NAMED columns; the telephone column is never read
     (asserted). Keep 영업/정상 (open) rows.
  2. Bucket with the korea_localdata taxonomy: keyed on the permit type, the
     sub-type only taking rows out (food trucks, catering, wholesale channels,
     e-commerce health-food sellers) or moving them (convenience stores and
     confectioners holding a café permit are shops).
  3. Place each on its own point (EPSG:5174 -> WGS84). A row with an address
     and no point borrows the point of any other row, open or closed, in the
     eight core registers at the same building - the road address to the
     building number, else the lot address (the brief's measured join).
  4. One pin per premises: food and personal services once per building and
     name; retail once per building and brand for the five convenience-store
     chains, by name otherwise - a convenience store can hold a tobacco, a café
     and a health-food permit at once. The most specific permit names it; the
     tobacco permit, an adjunct, only adds a pin where nothing else does.
  5. Withhold a trade name that is a bare personal name at a residential
     address (pipeline/korean_names.py).

Reads the cache and NEVER fetches.

    python pipeline/seoul/step2_clean_businesses.py
"""
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.korean_names import personal_name_at_home  # noqa: E402
from pipeline.seoul import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, korea_localdata as tax  # noqa: E402

TO_WGS = Transformer.from_crs(config.CRS_REGISTER, config.CRS_GEOGRAPHIC, always_xy=True)
WANTED = ["관리번호", "영업상태명", "사업장명", "도로명주소", "지번주소",
          "좌표정보(X)", "좌표정보(Y)", "업태구분명", "위생업태명"]
ROAD_RE = r"^서울특별시\s+(\S+구)\s+(\S+?(?:로|길))\s+(?:지하\s*)?(\d+(?:-\d+)?)"
LOT_RE = r"^서울특별시\s+(\S+구)\s+(\S+?(?:동|가|리))\s+(?:산\s*)?(\d+(?:-\d+)?)"
BRANDS = {
    "CU": r"씨유|(?<![A-Z])CU(?![A-Z])",
    "GS25": r"GS\s*25|지에스\s*25|GS편의점",
    "7-Eleven": r"세븐일레븐|세븐-일레븐|7-?ELEVEN|코리아세븐",
    "emart24": r"이마트\s*24|EMART\s*24|위드미",
    "Ministop": r"미니스톱|MINISTOP",
}
# Which permit names a retail premises when several are held at one building:
# the most specific first; the tobacco permit, an adjunct, last.
RETAIL_PRIORITY = ["OA-16096", "OA-16095", "OA-16084", "OA-16071", "OA-16085",
                   "OA-16080", "OA-16070", "OA-16144"]
WITHHELD = "Name withheld"


def read_register(oa):
    path = config.register_csv(oa)
    if not path.exists():
        sys.exit(f"missing {path}.\nRun: python pipeline/seoul/fetch_sources.py registers")
    with open(path, "rb") as f:
        header = [h.strip('"') for h in f.readline().decode(config.REGISTER_ENCODING).strip().split(",")]
    cols = [c for c in WANTED if c in header]
    assert not set(config.NEVER_READ) & set(cols), "a never-read column was requested"
    df = pd.read_csv(path, encoding=config.REGISTER_ENCODING, dtype=str, usecols=cols,
                     keep_default_na=False, encoding_errors="replace")
    assert not set(config.NEVER_READ) & set(df.columns), "a never-read column was loaded"
    df["oa"] = oa
    sub = df["업태구분명"] if "업태구분명" in df else df.get("위생업태명", pd.Series("", index=df.index))
    df["subtype"] = sub.str.strip()
    return df.drop(columns=[c for c in ("업태구분명", "위생업태명") if c in df])


def building_keys(df):
    road = df["도로명주소"].str.extract(ROAD_RE)
    lot = df["지번주소"].str.extract(LOT_RE)
    df["road_key"] = (road[0] + "|" + road[1] + "|" + road[2]).where(road[2].notna())
    df["lot_key"] = (lot[0] + "|" + lot[1] + "|" + lot[2]).where(lot[2].notna())
    return df


def xy(df):
    x = pd.to_numeric(df["좌표정보(X)"].str.strip(), errors="coerce")
    y = pd.to_numeric(df["좌표정보(Y)"].str.strip(), errors="coerce")
    ok = x.notna() & y.notna() & (x > 0) & (y > 0)
    return x.where(ok), y.where(ok)


def norm_name(s):
    return unicodedata.normalize("NFKC", s).replace("�", "").strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    frames, donors = [], []
    print("Registers (open rows):")
    for oa, kind in config.REGISTERS.items():
        df = building_keys(read_register(oa))
        df["x"], df["y"] = xy(df)
        if oa in config.COORD_DONORS:
            donors.append(df.loc[df.x.notna(), ["road_key", "lot_key", "x", "y"]])
        act = df[df["영업상태명"] == config.ACTIVE_STATUS].copy()
        print(f"  {oa} {kind:<14} {len(df):>8,} rows  {len(act):>7,} open")
        emit(f"open_{oa}", len(act))
        frames.append(act)
    df = pd.concat(frames, ignore_index=True)
    emit("open_rows", len(df))

    # --- 2. buckets ---------------------------------------------------------
    df["bucket"] = [tax.classify({"oa": o, "subtype": s}) for o, s in zip(df.oa, df.subtype)]
    print("\n  open rows by bucket before de-duplication:")
    for b, n in df.bucket.value_counts(dropna=False).items():
        print(f"    {str(b):<18} {n:>8,}")
    df = df[df.bucket.notna()].copy()
    emit("bucketed_rows", len(df))

    # --- 3. points ----------------------------------------------------------
    don = pd.concat(donors, ignore_index=True)
    by_road = don.dropna(subset=["road_key"]).groupby("road_key")[["x", "y"]].median()
    by_lot = don.dropna(subset=["lot_key"]).groupby("lot_key")[["x", "y"]].median()
    print(f"\n  donor building points: {len(by_road):,} by road address, {len(by_lot):,} by lot "
          f"(from {len(don):,} rows, open or closed, of the eight core registers)")
    df["placed"] = np.where(df.x.notna(), "own point", "")
    need = df.x.isna()
    r = df.loc[need, "road_key"].map(by_road.x)
    df.loc[need & r.notna(), ["x", "y"]] = np.c_[r.dropna(), df.loc[need, "road_key"].map(by_road.y).dropna()]
    df.loc[need & r.notna(), "placed"] = "road address"
    need = df.x.isna()
    lt = df.loc[need, "lot_key"].map(by_lot.x)
    df.loc[need & lt.notna(), ["x", "y"]] = np.c_[lt.dropna(), df.loc[need, "lot_key"].map(by_lot.y).dropna()]
    df.loc[need & lt.notna(), "placed"] = "lot address"
    tab = pd.crosstab(df.bucket, df.placed.replace("", "UNPLACED"))
    print("  placement by bucket:\n" + "\n".join("    " + ln for ln in tab.to_string().splitlines()))
    # Control: a row that has its own point, against its building's donor point.
    own = df[df.placed == "own point"]
    ctl = own.road_key.map(by_road.x)
    d = np.hypot(own.x - ctl, own.y - own.road_key.map(by_road.y)).dropna()
    print(f"  control, own point vs its building's point ({len(d):,} rows): median {d.median():.0f} m, "
          f"90th {d.quantile(.9):.0f} m, 99th {d.quantile(.99):.0f} m, over 100 m {(d > 100).mean():.1%}")
    for k, n in df.placed.replace("", "unplaced").value_counts().items():
        emit(f"placed_{k.replace(' ', '_')}", int(n))
    df = df[df.x.notna()].copy()
    df["longitude"], df["latitude"] = TO_WGS.transform(df.x.values, df.y.values)
    bb = config.SEOUL_BBOX
    inb = df.latitude.between(bb["lat_min"], bb["lat_max"]) & df.longitude.between(bb["lon_min"], bb["lon_max"])
    print(f"  outside the sanity box: {int((~inb).sum()):,}")
    emit("out_of_bounds", int((~inb).sum()))
    df = df[inb].copy()

    # --- 4. one pin per premises ---------------------------------------------
    df["name"] = df["사업장명"].map(norm_name)
    emit("names_with_undecodable_byte", int(df["사업장명"].str.contains("�").sum()))
    df["name_key"] = df.name.str.upper().str.replace(r"\s+", "", regex=True)
    df["building"] = df.road_key.fillna(df.lot_key).fillna(
        df.x.round(0).astype(str) + "," + df.y.round(0).astype(str))
    df["permit_type"] = [tax.kind(o, s) for o, s in zip(df.oa, df.subtype)]
    upper = df.name.str.upper()
    df["brand"] = None
    for brand, pat in BRANDS.items():
        df.loc[df.brand.isna() & upper.str.contains(pat, regex=True), "brand"] = brand
    retail = df.bucket == tax.RETAIL
    df.loc[retail & df.brand.notna(), "permit_type"] = tax.CONVENIENCE_STORE
    df["dedup"] = df.name_key
    df.loc[retail & df.brand.notna(), "dedup"] = df.brand
    rank = {oa: i for i, oa in enumerate(RETAIL_PRIORITY)}
    df["rank"] = [rank.get(o, 0) if b == tax.RETAIL else 0 for o, b in zip(df.oa, df.bucket)]
    before = df.bucket.value_counts()
    df = df.sort_values(["rank", "oa", "관리번호"]).drop_duplicates(["bucket", "building", "dedup"])
    after = df.bucket.value_counts()
    print("\n  one per premises (bucket, building, brand or name):")
    for b in after.index:
        print(f"    {b:<18} {before[b]:>8,} -> {after[b]:>8,}")
        emit(f"premises_{b.split()[0].lower()}", int(after[b]))
    cs = int((df.permit_type == tax.CONVENIENCE_STORE).sum())
    print(f"    convenience stores: {cs:,}")
    emit("convenience_stores", cs)

    # --- 5. privacy ----------------------------------------------------------
    df["address"] = df["도로명주소"].where(df["도로명주소"].str.strip() != "", df["지번주소"])
    flag = [personal_name_at_home(n, a) for n, a in zip(df.name, df.address)]
    df["business_name"] = df.name.where(~pd.Series(flag, index=df.index), WITHHELD)
    print(f"\n  names withheld (a personal name at a residential address): {sum(flag):,}")
    print("    " + str(df[flag].bucket.value_counts().to_dict()))
    emit("names_withheld", int(sum(flag)))
    blank = df.business_name.str.strip() == ""
    df.loc[blank, "business_name"] = "No name on the permit"
    emit("names_blank", int(blank.sum()))

    out = df[["business_name", "permit_type", "oa", "subtype", "latitude", "longitude", "address"]]
    kept = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(kept) != len(out):
        sys.exit("filter_to_storefront dropped rows the buckets already decided")
    emit("storefronts", len(kept))
    kept.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(kept):,} storefronts")


if __name__ == "__main__":
    main()
