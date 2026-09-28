"""South Korea's LOCALDATA permit registers, for every city after Seoul.

Seoul's step 2 (pipeline/seoul/step2_clean_businesses.py) was written against
Seoul's own republication. The SAME national register reaches the other cities
under different column names, in a different file format and with one field
moved, and Seoul's code, which selects by exact name, reads every one of those
differences as nothing rather than as an error. Daegu measured them
(docs/build_briefs/daegu.md, 2026-09-27); Busan's API is the same register. So
the rules live here, where the next city has to pass through them, rather than
in a sibling city's comments (osm-rail's meta-rule):

  * every field is resolved from a list of the names it has been published
    under, and a header that carries none of them RAISES;
  * a telephone column that NEVER_READ does not name RAISES, so the guard
    always covers the column that is actually there (Seoul's 전화번호 is
    Daegu's 소재지전화);
  * the sub-type is taken per ROW: 업태구분명 where it has a value, else
    위생업태명. Daegu's health-food file carries 업태구분명 on every row and
    blank on every row, and a per-column choice drops every row under the
    in-store rule;
  * a keep-only rule that keeps nothing from a file with open rows RAISES;
  * the building-key regex is built from the city's prefix and matches 구 and
    군 (Daegu's 달성군 and 군위군), and a match rate under 95% RAISES;
  * a register whose addresses are masked with * (Daegu's health-food file,
    every row) RAISES unless the city's config declares it. Masked rows keep
    their published point and take the building of any row on the same point.

Seoul is not moved onto this module: its outputs are the drift baseline, and
nothing here changes them. The bucket, placement, de-duplication and privacy
rules are Seoul's, ported unchanged (the owner's calls of 2026-09-24).
"""
import re
import sys
import unicodedata

import numpy as np
import pandas as pd

from pipeline.baseline import emit
from pipeline.korean_names import personal_name_at_home
from pipeline.taxonomies import korea_localdata as tax

# field -> every name it has been published under (Seoul's first).
FIELDS = {
    "관리번호": ("관리번호",),
    "영업상태명": ("영업상태명",),
    "사업장명": ("사업장명",),
    "road_address": ("도로명주소", "도로명전체주소"),
    "lot_address": ("지번주소", "소재지전체주소"),
    "x": ("좌표정보(X)", "좌표정보X(EPSG5174)"),
    "y": ("좌표정보(Y)", "좌표정보Y(EPSG5174)"),
}
# At least one of these carries the sub-type; which one varies by row.
SUBTYPE_FIELDS = ("업태구분명", "위생업태명")
PHONE_MARK = "전화"

# Which permit names a retail premises when several are held at one building:
# the most specific first; the tobacco permit, an adjunct, last (Seoul's order).
RETAIL_PRIORITY = ["대규모점포", "휴게음식점", "제과점영업", "축산판매업", "즉석판매제조가공업",
                   "식품판매업(기타)", "건강기능식품일반판매업", "담배소매업"]
BRANDS = {
    "CU": r"씨유|(?<![A-Z])CU(?![A-Z])",
    "GS25": r"GS\s*25|지에스\s*25|GS편의점",
    "7-Eleven": r"세븐일레븐|세븐-일레븐|7-?ELEVEN|코리아세븐",
    "emart24": r"이마트\s*24|EMART\s*24|위드미",
    "Ministop": r"미니스톱|MINISTOP",
}
WITHHELD = "Name withheld"
MIN_KEY_RATE = 0.95


def columns_to_read(header, source, never_read):
    """{field: source column} for one register's header. Raises on a missing
    field or an unguarded telephone column; never selects a never-read one."""
    header = [str(h).strip() for h in header]
    # A phone column is 전화 in the published files (전화번호, 소재지전화) and a
    # ...tel code in the API's JSON (Busan's sitetel).
    phones = [h for h in header
              if (PHONE_MARK in h or h.lower().endswith("tel")) and h not in never_read]
    if phones:
        sys.exit(f"{source}: telephone column(s) {phones} are not in NEVER_READ - name the "
                 f"column that is actually there, or the guard covers nothing")
    picked = {}
    for field, names in FIELDS.items():
        hit = [n for n in names if n in header]
        if len(hit) != 1:
            sys.exit(f"{source}: field {field!r} found as {hit or 'nothing'} among the names "
                     f"{names} - a renamed column reads as empty; add the new name to "
                     f"korea.FIELDS")
        picked[field] = hit[0]
    subs = [n for n in SUBTYPE_FIELDS if n in header]
    if not subs:
        sys.exit(f"{source}: neither of {SUBTYPE_FIELDS} is in the header")
    for s in subs:
        picked[s] = s
    if set(picked.values()) & set(never_read):
        sys.exit(f"{source}: a never-read column was selected")
    return picked


def normalise(raw, picked, source, never_read, permit_type):
    """One register's rows, renamed to the fields above, with the per-row
    sub-type and the register's permit type in `oa` (the taxonomy key)."""
    if set(never_read) & set(raw.columns):
        sys.exit(f"{source}: a never-read column was loaded")
    df = pd.DataFrame({f: raw[c].fillna("").astype(str).str.strip()
                       for f, c in picked.items() if f not in SUBTYPE_FIELDS})
    sub = pd.Series("", index=raw.index)
    for s in SUBTYPE_FIELDS:
        if s in picked:
            v = raw[s].fillna("").astype(str).str.strip()
            sub = sub.where(sub != "", v)
    df["subtype"] = sub
    if tax.key(permit_type) not in tax.FILES:
        sys.exit(f"{source}: permit type {permit_type!r} is not in the taxonomy")
    df["oa"] = permit_type
    return df


def building_keys(df, prefix, source, masked_ok=False):
    """road_key and lot_key: gu or gun | street or dong | number. A match rate
    under 95% on rows that have an address raises - a regex that misses a whole
    district (a 군 read as 구) fails loudly rather than leaving rows unkeyed.

    A register can mask its house numbers with * (Daegu's health-food register
    masks every one). Those rows cannot be keyed and are left out of the rate;
    a register where more than 1% are masked raises unless the city's config
    declares it (masked_ok), so masking arriving in a new file is seen."""
    masked = df.road_address.str.contains(r"\*", regex=True) | df.lot_address.str.contains(r"\*", regex=True)
    if masked.mean() > 0.01 and not masked_ok:
        sys.exit(f"{source}: {masked.mean():.1%} of addresses are masked with * - declare the "
                 f"file in the city's MASKED_ADDRESS_FILES if the publisher masks it")
    df["address_masked"] = masked
    p = re.escape(prefix)
    road = df["road_address"].str.extract(
        rf"^{p}\s+(\S+[구군])\s+(?:\S+[읍면]\s+)?(\S+?(?:로|길))\s+(?:지하\s*)?(\d+(?:-\d+)?)")
    lot = df["lot_address"].str.extract(
        rf"^{p}\s+(\S+[구군])\s+(?:\S+[읍면]\s+)?(\S+?(?:동|가|리))\s+(?:산\s*)?(\d+(?:-\d+)?)")
    df["road_key"] = (road[0] + "|" + road[1] + "|" + road[2]).where(road[2].notna())
    df["lot_key"] = (lot[0] + "|" + lot[1] + "|" + lot[2]).where(lot[2].notna())
    df.loc[masked, ["road_key", "lot_key"]] = None
    has = ((df.road_address != "") | (df.lot_address != "")) & ~masked
    keyed = df.road_key.notna() | df.lot_key.notna()
    rate = keyed[has].mean() if has.any() else 1.0
    if rate < MIN_KEY_RATE:
        sample = df.loc[has & ~keyed, ["road_address", "lot_address"]].head(5).to_string()
        sys.exit(f"{source}: only {rate:.1%} of addressed rows got a building key "
                 f"(prefix {prefix!r}) - the regex is missing a district shape:\n{sample}")
    return df


def xy(df):
    x = pd.to_numeric(df["x"], errors="coerce")
    y = pd.to_numeric(df["y"], errors="coerce")
    ok = x.notna() & y.notna() & (x > 0) & (y > 0)
    return x.where(ok), y.where(ok)


def norm_name(s):
    return unicodedata.normalize("NFKC", s).replace("�", "").strip()


def build_storefronts(registers, active_status, to_wgs, bbox, donor_keys):
    """Seoul's steps 2-5 over normalised registers: buckets, placement (own
    point, else a donor's at the same building), one pin per premises, and the
    Korean privacy pass. registers: {file key: normalised frame}. Returns the
    frame step 2 writes."""
    frames, donors = [], []
    print("Registers (open rows):")
    for k, df in registers.items():
        df = df.copy()
        df["file"] = k
        df["x"], df["y"] = xy(df)
        if k in donor_keys:
            donors.append(df.loc[df.x.notna(), ["road_key", "lot_key", "x", "y"]])
        act = df[df["영업상태명"] == active_status].copy()
        print(f"  {k:<10} {df.oa.iloc[0]:<14} {len(df):>8,} rows  {len(act):>7,} open")
        emit(f"open_{k}", len(act))
        frames.append(act)
    df = pd.concat(frames, ignore_index=True)
    emit("open_rows", len(df))

    # --- buckets ---------------------------------------------------------------
    df["bucket"] = [tax.classify({"oa": o, "subtype": s}) for o, s in zip(df.oa, df.subtype)]
    for k, g in df.groupby("file"):
        only = tax.ONLY.get(tax.key(g.oa.iloc[0]))
        if only and len(g) and g.bucket.isna().all():
            sys.exit(f"{k}: the keep-only rule {sorted(only)} kept none of {len(g):,} open "
                     f"rows - its sub-types are {g.subtype.value_counts().head(5).to_dict()}")
    print("\n  open rows by bucket before de-duplication:")
    for b, n in df.bucket.value_counts(dropna=False).items():
        print(f"    {str(b):<18} {n:>8,}")
    df = df[df.bucket.notna()].copy()
    emit("bucketed_rows", len(df))

    # --- points ----------------------------------------------------------------
    don = pd.concat(donors, ignore_index=True)
    by_road = don.dropna(subset=["road_key"]).groupby("road_key")[["x", "y"]].median()
    by_lot = don.dropna(subset=["lot_key"]).groupby("lot_key")[["x", "y"]].median()
    print(f"\n  donor building points: {len(by_road):,} by road address, {len(by_lot):,} by lot "
          f"(from {len(don):,} rows, open or closed, of the donor registers)")
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
    own = df[df.placed == "own point"]
    ctl = own.road_key.map(by_road.x)
    d = np.hypot(own.x - ctl, own.y - own.road_key.map(by_road.y)).dropna()
    print(f"  control, own point vs its building's point ({len(d):,} rows): median {d.median():.0f} m, "
          f"90th {d.quantile(.9):.0f} m, 99th {d.quantile(.99):.0f} m, over 100 m {(d > 100).mean():.1%}")
    for k, n in df.placed.replace("", "unplaced").value_counts().items():
        emit(f"placed_{k.replace(' ', '_')}", int(n))
    df = df[df.x.notna()].copy()
    df["longitude"], df["latitude"] = to_wgs.transform(df.x.values, df.y.values)
    inb = (df.latitude.between(bbox["lat_min"], bbox["lat_max"])
           & df.longitude.between(bbox["lon_min"], bbox["lon_max"]))
    print(f"  outside the sanity box: {int((~inb).sum()):,}")
    emit("out_of_bounds", int((~inb).sum()))
    df = df[inb].copy()

    # --- one pin per premises ----------------------------------------------------
    df["name"] = df["사업장명"].map(norm_name)
    emit("names_with_undecodable_byte", int(df["사업장명"].str.contains("�").sum()))
    df["name_key"] = df.name.str.upper().str.replace(r"\s+", "", regex=True)
    # The building: its road address, else its lot address, else - for a row
    # whose address was masked or unparsed - the key of any other row standing
    # on the same point (LOCALDATA gives one building one point), else the
    # point itself. Without the middle step a convenience store's masked
    # health-food permit would be a second pin beside its tobacco permit.
    df["point"] = df.x.round(0).astype(str) + "," + df.y.round(0).astype(str)
    keyed = df.road_key.fillna(df.lot_key)
    at_point = keyed.dropna().groupby(df.point).first()
    df["building"] = keyed.fillna(df.point.map(at_point)).fillna(df.point)
    emit("building_from_shared_point", int((keyed.isna() & df.point.isin(at_point.index)).sum()))
    df["permit_type"] = [tax.kind(o, s) for o, s in zip(df.oa, df.subtype)]
    upper = df.name.str.upper()
    df["brand"] = None
    for brand, pat in BRANDS.items():
        df.loc[df.brand.isna() & upper.str.contains(pat, regex=True), "brand"] = brand
    retail = df.bucket == tax.RETAIL
    df.loc[retail & df.brand.notna(), "permit_type"] = tax.CONVENIENCE_STORE
    df["dedup"] = df.name_key
    df.loc[retail & df.brand.notna(), "dedup"] = df.brand
    rank = {t: i for i, t in enumerate(RETAIL_PRIORITY)}
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

    # --- privacy ---------------------------------------------------------------
    df["address"] = df["road_address"].where(df["road_address"] != "", df["lot_address"])
    flag = [personal_name_at_home(n, a) for n, a in zip(df.name, df.address)]
    df["business_name"] = df.name.where(~pd.Series(flag, index=df.index), WITHHELD)
    print(f"\n  names withheld (a personal name at a residential address): {sum(flag):,}")
    print("    " + str(df[flag].bucket.value_counts().to_dict()))
    emit("names_withheld", int(sum(flag)))
    blank = df.business_name.str.strip() == ""
    df.loc[blank, "business_name"] = "No name on the permit"
    emit("names_blank", int(blank.sum()))
    return df[["business_name", "permit_type", "oa", "subtype", "latitude", "longitude", "address"]]
