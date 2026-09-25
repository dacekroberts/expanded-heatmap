"""Step 2 for every Taiwanese city: the national tax register's storefronts in the
city, joined to the city's door plates. Moved here from Taichung's step 2 on
2026-09-25, unchanged in behaviour (Taichung reproduced 66,115), so Taoyuan and
Taipei share one copy. A city's step 2 calls run(config, "<City>", "<slug>").

  1. The register rows whose address starts with the city's prefixes and whose
     industry code is in a storefront division (487 online shopping excluded).
  2. The head-office rule (owner 2026-09-25, measured on Taipei): a company's
     head-office or single-site row on the 3rd floor or higher, or with a room
     number, is an office - dropped, unless its building holds 20 or more
     storefront rows (a market or a mall).
  3. The JOIN: the address parsed to district, street, lane, alley and number
     and looked up in the door-plate file - the district is part of the key
     (Taichung: one street name recurs in several districts); then the parent
     number's plate (tier 2). Unmatched rows are left off.
  4. The name rule (owner 2026-09-23): a name is shown only when it is a trade
     name; otherwise the tooltip shows the register's own industry name.

Reads the cache and NEVER fetches.
"""
import collections
import csv
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import taiwan  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402

DISTRICT = re.compile(r"^(.{1,3}?(?:區|鄉|鎮|市))")
FLOOR = re.compile(r"(\d+|[一二三四五六七八九十]+)樓")
COMPANY = "公司"
SMALL_DISTRICT_KEYS = 20


def need(path, what, arg, slug):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/{slug}/fetch_sources.py {arg}")
    return path


def district_of(addr, config):
    a = taiwan.nfkc(addr).replace("台", "臺")
    for p in config.ADDRESS_PREFIXES:
        a = a.replace(taiwan.nfkc(p).replace("台", "臺"), "", 1)
    m = DISTRICT.match(a)
    return m.group(1) if m else ""


def floor_of(addr):
    m = FLOOR.search(taiwan.nfkc(addr))
    return int(taiwan.cn_num(m.group(1))) if m else 0


def load_plates(config, slug):
    """{(district, street, lane, alley, number): (lon, lat)}. A file with WGS84
    columns (Taichung) is read as is; one with only projected coordinates names
    them "x"/"y" in PLATE_COLS and its CRS in PLATE_CRS (Taoyuan: TWD97 TM2)."""
    cols = config.PLATE_COLS
    xcol, ycol = (cols["x"], cols["y"]) if "x" in cols else (cols["lon"], cols["lat"])
    keys, xs, ys = [], [], []
    plates_nd = collections.defaultdict(set)
    with need(config.DOORPLATE_CSV, "door plates", "doorplates", slug).open(
            encoding="utf-8-sig", errors="replace", newline="") as f:
        rd = csv.DictReader(f)
        dcol = config.PLATE_DISTRICT_COL
        for r in rd:
            k = taiwan.plate_key(r[cols["street"]], r[cols["lane"]], r[cols["alley"]], r[cols["num"]])
            if not k:
                continue
            try:
                x, y = float(r[xcol]), float(r[ycol])
            except ValueError:
                continue
            d = r[dcol].strip()
            keys.append((d, *k))
            xs.append(x)
            ys.append(y)
            plates_nd[k].add(d)
    if getattr(config, "PLATE_CRS", None):
        from pyproj import Transformer
        xs, ys = Transformer.from_crs(config.PLATE_CRS, "EPSG:4326", always_xy=True).transform(xs, ys)
    plates = {}
    for k, x, y in zip(keys, xs, ys):
        plates.setdefault(k, (float(x), float(y)))
    return plates, plates_nd


def district_codes(df, plates_nd):
    """The door-plate file names a district by CODE, the register by NAME. Learn
    the mapping from the keys that exist in ONE district only, and refuse a
    district whose rows disagree."""
    votes = collections.defaultdict(collections.Counter)
    for d, k in zip(df.district, df.key):
        # An address with no parsable district cannot be keyed; it is not a
        # district to learn (New Taipei: two such rows voted 中和's code).
        if d and k and len(plates_nd.get(k, ())) == 1:
            votes[d][next(iter(plates_nd[k]))] += 1
    mapping = {}
    print("  district name -> door-plate code (learned from single-district keys):")
    for d, c in sorted(votes.items(), key=lambda kv: -sum(kv[1].values())):
        code, n = c.most_common(1)[0]
        share = n / sum(c.values())
        total = sum(c.values())
        small = total < SMALL_DISTRICT_KEYS
        print(f"    {d:<6} {code}  {n:>6,} of {total:>6,} ({share:.1%})"
              + ("  - small sample: majority taken" if small else ""))
        # 90% where the sample is large; a clear majority where it is not
        # (New Taipei's rural 雙溪區 has 9 single-district keys, 6 agreeing).
        if share < (0.5 if small else 0.9):
            sys.exit(f"district {d} maps to several codes {dict(c)} - read the addresses")
        mapping[d] = code
    if len(set(mapping.values())) != len(mapping):
        sys.exit(f"two district names learned one code: {mapping}")
    return mapping


def run(config, city, slug, tag="", write=True):
    """tag prefixes the baseline figures (a regional city runs this once per
    city); write=False returns the table without writing it."""
    sys.stdout.reconfigure(encoding="utf-8")
    plates, plates_nd = load_plates(config, slug)
    shared = sum(1 for v in plates_nd.values() if len(v) > 1)
    print(f"  door plates: {len(plates):,} keys with district; {shared:,} street/number keys "
          f"occur in more than one district - why the district is part of the key")
    emit(tag + "doorplate_keys", len(plates))

    rows = []
    for r in taiwan.register_rows(config.ADDRESS_PREFIXES, need(taiwan.REGISTER_ZIP, "tax register", "register", slug)):
        b = taiwan.bucket_of(r.get("行業代號"))
        if b is None or not r.get("統一編號"):
            continue
        rows.append({"id": r["統一編號"].strip(), "parent": (r.get("總機構統一編號") or "").strip(),
                     "name": (r.get("營業人名稱") or "").strip(),
                     "org": (r.get("組織別名稱") or "").strip(),
                     "industry_code": r["行業代號"].strip(), "industry": (r.get("名稱") or "").strip(),
                     "address": (r.get("營業地址") or "").strip(), "bucket": b})
    df = pd.DataFrame(rows)
    print(f"  register rows in {city}, storefront divisions: {len(df):,}  "
          f"{df.bucket.value_counts().to_dict()}")
    emit(tag + "storefront_rows", len(df))

    df["district"] = df.address.map(lambda a: district_of(a, config))
    parsed = [taiwan.parse(a, config.ADDRESS_PREFIXES) for a in df.address]
    df["key"] = parsed
    codes = district_codes(df, plates_nd)
    emit(tag + "districts", len(codes))
    df["district"] = df.district.map(codes).fillna("")
    df["building"] = [(d, *k[:3], k[3].split("-")[0]) if k else None
                      for d, k in zip(df.district, parsed)]

    # --- the head-office rule ------------------------------------------------
    per_building = df.building.value_counts()
    company_hq = df.org.str.contains(COMPANY) & (df.parent == "")
    officey = df.address.map(lambda a: floor_of(a) >= config.OFFICE_FLOOR_MIN or "室" in taiwan.nfkc(a))
    exempt = df.building.map(per_building).fillna(0) >= config.OFFICE_EXEMPT_ROWS_AT_ADDRESS
    drop = company_hq & officey & ~exempt
    print(f"  head-office rule: {int((company_hq & officey).sum()):,} company head-office rows look "
          f"like offices; {int((company_hq & officey & exempt).sum()):,} exempt (a building with "
          f"{config.OFFICE_EXEMPT_ROWS_AT_ADDRESS}+ storefront rows); {int(drop.sum()):,} dropped")
    emit(tag + "office_like_dropped", int(drop.sum()))
    df = df[~drop].copy()

    # --- the join --------------------------------------------------------------
    how, lon, lat = [], [], []
    for d, k in zip(df.district, df.key):
        pt, h = None, "unparsed"
        if k:
            pt = plates.get((d, *k))
            h = "exact" if pt else "no plate"
            if pt is None:
                pt = plates.get((d, k[0], k[1], k[2], k[3].split("-")[0]))
                h = "base number" if pt else h
        how.append(h)
        lon.append(pt[0] if pt else None)
        lat.append(pt[1] if pt else None)
    df["placed"], df["longitude"], df["latitude"] = how, lon, lat
    tab = pd.crosstab(df.bucket, df.placed, margins=True)
    print("  the join by bucket:\n" + "\n".join("    " + ln for ln in tab.to_string().splitlines()))
    ok = df.placed.isin(["exact", "base number"])
    print(f"  placed {ok.mean():.1%} of {len(df):,}")
    for k, n in df.placed.value_counts().items():
        emit(tag + f"join_{k.replace(' ', '_')}", int(n))
    miss = df[~ok]
    stall = miss.address.str.contains("攤|市場|高架橋下")
    print(f"  of {len(miss):,} unplaced, {int(stall.sum()):,} read as market or viaduct stalls; samples:")
    for a in miss.address.iloc[:: max(1, len(miss) // 8)][:8]:
        print(f"     {a[:50]}")
    df = df[ok].copy()
    bb = config.CITY_BBOX
    inb = df.latitude.between(bb["lat_min"], bb["lat_max"]) & df.longitude.between(bb["lon_min"], bb["lon_max"])
    emit(tag + "out_of_bounds", int((~inb).sum()))
    df = df[inb].copy()

    # --- the name rule -----------------------------------------------------------
    trade = [taiwan.is_trade_name(n, o) for n, o in zip(df.name, df.org)]
    df["business_name"] = df.name.where(pd.Series(trade, index=df.index), df.industry)
    hidden = len(df) - sum(trade)
    print(f"  names shown: {sum(trade):,}; sole proprietors shown by their industry instead: "
          f"{hidden:,} ({hidden / len(df):.1%})")
    emit(tag + "names_hidden", hidden)

    out = df[["business_name", "industry", "industry_code", "latitude", "longitude", "address",
              "org"]]
    kept = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(kept) != len(out):
        sys.exit("filter_to_storefront dropped rows the buckets already decided")
    emit(tag + "storefronts", len(kept))
    if write:
        kept.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
        print(f"  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(kept):,} storefronts")
    return kept

