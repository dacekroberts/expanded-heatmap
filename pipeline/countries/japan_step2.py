"""Step 2 for every Japanese city: the city's own permit lists and 生活衛生
registers, classified by japan_eigyo and placed by the MLIT join
(japan_register.py). Built for Kobe (2026-09-27), the first Japanese city; one
copy for every Japanese city. A city's step 2 calls run(config).

  1. Each source in config.SOURCES read by column NAME (japan_register's
     premises columns); `source` names the register ("food", "barber",
     "beauty", "laundry"), which decides Personal services.
  2. Not a premises dropped: vehicles, stalls, "anywhere in the city" (一円),
     storeless pick-ups. Then the taxonomy: every row it does not bucket
     (manufacturing, vending machines, institutional catering...) is dropped
     and counted by the rule that decided it.
  3. The JOIN, tiered: block, town-chōme centroid, none. Block and chōme are
     kept and the tier travels with the row; unplaced rows are dropped,
     counted and sampled. Where a list publishes its own coordinates and the
     config names it in OWN_POINT_FALLBACK, a block miss takes the publisher's
     point instead (tier "own"; Fukuoka's MHLW rows), or another publisher's
     point for the same premises (config.POINT_DONORS; Toyama). Where one
     premises is in two lists (config.SUPERSEDES), the older list's row goes
     (Fukuoka).
  4. One pin per premises and bucket: rows repeating (address, trade name,
     bucket) are one premises holding several permits of one kind.
  5. The name rule (owner 2026-09-27): where the trade name IS the operator's
     own name (japan_register.name_is_operator, compared in memory), the map
     shows the permit type instead. Counted; the operator's name is never kept.
  6. The owner's 菓子 / そうざい call (2026-09-24): the share of those rows whose
     trade name reads as a factory or central kitchen is MEASURED and printed,
     for the page and DECISIONS.md, not filtered.

Config needs: SOURCES, source_csv(), REQUIRED_COLUMNS, ISJ_DIR, PREFECTURE,
MUNICIPALITY, CITY_BBOX, TAXONOMY_SYSTEM, BUSINESSES_CLEAN_CSV, SLUG. Optional,
each named where it is defined: source_rows, SOURCE_MUNICIPALITY, SOURCE_KIND,
ADDRESS_BY_CONSENT, OWN_POINT_FALLBACK, POINT_DONORS, SUPERSEDES, and with
OFFICIAL_SHARES, SHARE_DATES and REGISTER_SHARES (the Tama cities); a city
without wards says so in japan.CITIES ("wardless"). Reads the cache and NEVER
fetches.
"""
import collections
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import japan_register as jr  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies import japan_eigyo  # noqa: E402

# A trade name that reads as a production site rather than a counter.
FACTORY = re.compile(r"工場|製造所|製造部|セントラルキッチン|センター|本社|事業所|倉庫")
# What a register row is called when its name is withheld.
REGISTER_TYPE = {"barber": "理容所", "beauty": "美容所", "laundry": "クリーニング所"}


def need(path, slug):
    if not Path(path).exists():
        sys.exit(f"missing {path}\nRun: python pipeline/{slug}/fetch_sources.py")
    return path


def source_rows(config, key):
    """A source's rows: its file, or config.source_rows(key) where a city's
    source is not one file - Kyoto's rebuilt food register
    (japan_register.kyoto_permit_stream) and its registers, each a complete
    list plus the months since (2026-09-28)."""
    if hasattr(config, "source_rows"):
        return config.source_rows(key)
    return jr.city_rows(need(config.source_csv(key), config.SLUG))


def municipality(config, key):
    """The municipality a source's addresses are read against: the city's, or
    config.SOURCE_MUNICIPALITY[key] where each source is one municipality of
    its own - Tokyo's special wards, each its own publisher, where the WARD is
    the municipality (港区, 渋谷区) and an address may start at the town (Taitō)."""
    return getattr(config, "SOURCE_MUNICIPALITY", {}).get(key, config.MUNICIPALITY)


def kind(config, key):
    """What a source IS, as japan_eigyo reads it ("food", "mhlw", "barber",
    "beauty", "laundry"): the key itself, or config.SOURCE_KIND[key] where a
    city has several sources of one kind - Tokyo's wards, each with its own
    food list and registers (food_13103, barber_13103; 2026-09-28). The KEY
    names a source in SUPERSEDES, SHARE_SKIP, ADDRESS_BY_CONSENT and
    OWN_POINT_FALLBACK; the KIND decides its bucket and is the output's
    `source` column."""
    return getattr(config, "SOURCE_KIND", {}).get(key, key)


def key_addr(a):
    return re.sub(r"[‐‑‒–—―−ｰー－]", "-", unicodedata.normalize("NFKC", a or "").replace(" ", "").replace("　", ""))


def own_coordinates_check(config, df):
    """Where a list carries its OWN coordinates (Osaka's swapped 経度 / 緯度;
    japan_register.permits_from_rows swaps them back), measure the join against
    them: an independent check, never the map's source. Printed and emitted
    per tier; a list without coordinates (Kobe's) prints nothing. Distances in
    the city's projected CRS, never in degrees."""
    has = df[df["pub"].notna()]
    if has.empty:
        return
    import geopandas as gpd

    def proj(lats, lons):
        return gpd.GeoSeries(gpd.points_from_xy(lons, lats), crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)

    d = proj(has["latitude"].values, has["longitude"].values).distance(
        proj([p[0] for p in has["pub"]], [p[1] for p in has["pub"]]), align=False)
    d.index = has.index
    print(f"  the list's own coordinates against the join ({len(has):,} of {len(df):,} placed rows carry them):")
    for tier in ("block", "chome"):
        t = d[has["tier"] == tier]
        if len(t):
            print(f"    {tier:6} {len(t):>7,}  median {t.median():>5.0f} m   within 250 m {(t <= 250).mean():.1%}   "
                  f"over 1 km {int((t > 1000).sum()):,}")
            emit(f"own_coords_{tier}_median_m", int(round(t.median())))
            emit(f"own_coords_{tier}_within_250m_pct", round(100 * (t <= 250).mean(), 1))


def _after(d, date):
    """A row's date (config.SHARE_DATES) falls after the official count's date."""
    return d is not None and d == d and str(d) > date


def at_date(rows, official, key):
    """The share AT THE OFFICIAL COUNT'S DATE (the owner's calls 187-189,
    2026-10-06): a list that adds new permits month by month, and keeps few
    old ones, reads high against a count of a year and a half before. The rows
    first permitted (or confirmed) after that date are left out of the
    numerator; config.SHARE_DATES names each source's date column. Tokyo's
    Tama ledgers (East-1, 2026-10-07): Higashiyamato's 505 restaurant rows
    against the yearbook's 528 read 95.6%, and 75.2% at the date (the brief).
    A row with no date is kept and counted."""
    from pipeline.countries import japan_official
    date = japan_official.YEARBOOK_DATE
    after = rows["dated"].map(lambda d: _after(d, date)) if "dated" in rows else pd.Series(False, index=rows.index)
    undated = int(rows["dated"].map(lambda d: d is None or d != d).sum()) if "dated" in rows else len(rows)
    n = len(rows) - int(after.sum())
    share = round(100 * n / official, 1)
    print(f"      at {date}: {n:>7,} of {official:>7,}  {share:5.1f}%   ({int(after.sum()):,} dated after it, "
          f"{undated:,} undated)")
    emit(key, n)
    return {"kind": "restaurants", "rows_at_date": n, "share_at_date_pct": share, "date": date, "undated": undated}


def register_shares(df, muni, code):
    """Each register's share of the official count (config.REGISTER_SHARES;
    Tokyo's yearbook table 19-7, the owner's call 189, 2026-10-06): its rows
    in the municipality, storeless pick-up counters and closed rows out, all
    rows and at the count's date. Stops where no official count covers it."""
    from pipeline.countries import japan_official
    official = japan_official.registers(muni)
    out = []
    for kind in japan_official.REGISTER_COLUMNS:
        rows = df[(df["kind"] == kind) & (df["muni"] == muni) & ~df["mobile"] & ~df["closed"]]
        if rows.empty:
            continue
        if not official.get(kind):
            sys.exit(f"no official {kind} count for {muni}: is the yearbook's table 19-7 cached?")
        n, o = len(rows), official[kind]
        print(f"    {kind:8} {n:>7,} of {o:>7,}  {100 * n / o:5.1f}%   ({japan_official.YEARBOOK_REGISTERS_SOURCE})")
        emit(f"official_{kind}_rows_{code}", n)
        emit(f"official_{kind}_count_{code}", o)
        entry = {"municipality": muni, "code": code, "kind": kind, "rows": n, "official": o,
                 "share_pct": round(100 * n / o, 1), "source": japan_official.YEARBOOK_REGISTERS_SOURCE}
        entry.update(at_date(rows, o, f"official_{kind}_rows_at_date_{code}"), kind=kind)
        out.append(entry)
    return out


def official_shares(config, df, write=True):
    """Each municipality's share of the official restaurant count
    (japan_official: Tokyo's yearbook per ward, e-Stat per city), measured the
    Tokyo brief's way: the lists' 飲食店 permit rows, vehicles and stalls
    included, closed rows out. Opt-in (config.OFFICIAL_SHARES = True): Tokyo's
    page states each ward's share, and a share it states must be the one this
    build measured (owner 2026-09-28). Emitted to the baseline - rows and count,
    so drift_check flags a moved share - and written to
    outputs/<slug>/official_shares.json for the page to read, never retyped."""
    if not getattr(config, "OFFICIAL_SHARES", False):
        return
    import json

    from pipeline.countries import japan_official
    codes = getattr(config, "MUNICIPALITY_CODES", {})
    # config.SHARE_SKIP: sources left out of the share - Tokyo's MHLW slices,
    # since the page states each ward's share of its OWN list (owner 2026-09-28)
    food = df[~df["kind"].isin(japan_eigyo.PERSONAL_SOURCES) & ~df["closed"]
              & ~df["source"].isin(getattr(config, "SHARE_SKIP", ()))
              & df["type"].fillna("").str.contains("飲食")]
    rows = food["muni"].value_counts()
    out = []
    print("  share of the official restaurant count (飲食店 rows, vehicles in, closed out):")
    for muni in dict.fromkeys(municipality(config, k) for k in config.SOURCES):
        n = int(rows.get(muni, 0))
        official, source = japan_official.restaurants(config.PREFECTURE, muni)
        if not official:
            sys.exit(f"no official count for {muni}: is its yearbook or e-Stat table cached?")
        share = round(100 * n / official, 1)
        code = codes.get(muni, muni)
        print(f"    {muni:6} {n:>7,} of {official:>7,}  {share:5.1f}%   ({source})")
        emit(f"official_rows_{code}", n)
        emit(f"official_count_{code}", official)
        out.append({"municipality": muni, "code": code, "rows": n, "official": official, "share_pct": share,
                    "source": source})
        if getattr(config, "SHARE_DATES", {}):
            out[-1].update(at_date(food[food["muni"] == muni], official, f"official_rows_at_date_{code}"))
        if getattr(config, "REGISTER_SHARES", False):
            out += register_shares(df, muni, code)
    if not write:
        return
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    # bytes, so Windows text mode never turns the committed LF file to CRLF
    (config.OUTPUTS / "official_shares.json").write_bytes(
        (json.dumps(out, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


# A publisher's DEFAULT point (owner, 2026-10-02): MHLW parks a filing it
# cannot place on one stand-in coordinate, Kagoshima's and Utsunomiya's city
# halls, a point given to rows in 13 different towns in Okayama. A point the
# publisher gives to rows in this many distinct towns or more is never used to
# place a row; the row keeps its town-chōme centroid, or stays unplaced.
SHARED_POINT_TOWNS = 3


def _pt4(p):
    return (round(p[0], 4), round(p[1], 4))


def shared_points(rows):
    """The publisher points (to about 10 m) given to rows in SHARED_POINT_TOWNS
    or more distinct (ward, town) pairs: default points, not premises."""
    towns = collections.defaultdict(set)
    for w, t, p in rows:
        if p is not None and p == p:
            towns[_pt4(p)].add((w, t))
    return {pt for pt, ts in towns.items() if len(ts) >= SHARED_POINT_TOWNS}


# A publisher's points that sit this far from the block point, as a median over
# its block-tier rows, are not in the block file's datum. Higashiōsaka's
# (2026-10-03) sit a median 448 m off in one consistent direction: the old
# Tokyo Datum (EPSG:4301), 37 m once shifted to JGD2000. The built cities'
# publishers measure 32-51 m.
DATUM_OFFSET_M = 200


def datum_guard(config, rows):
    """Stop before a publisher's points place any row if they are offset as a
    datum shift would offset them (rows: one source's joined rows). Measured in
    the city's projected CRS, never in degrees."""
    has = rows[(rows["tier"] == "block") & rows["pub"].map(lambda p: p is not None and p == p)]
    if len(has) < 20:
        return
    import geopandas as gpd

    def proj(pts):
        return gpd.GeoSeries(gpd.points_from_xy([p[1] for p in pts], [p[0] for p in pts]),
                             crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)

    d = proj(list(has["pt"])).distance(proj(list(has["pub"])), align=False)
    if d.median() > DATUM_OFFSET_M:
        sys.exit(f"the publisher's own points sit a median {d.median():.0f} m from the block point "
                 f"({len(has):,} block rows): another datum (the old Tokyo Datum, as Higashiosaka's)? "
                 f"Shift them before OWN_POINT_FALLBACK uses them.")


def own_point_fallback(config, joined):
    """Where the block join misses a row from a source that publishes its own
    coordinates (config.OWN_POINT_FALLBACK, e.g. {"mhlw"}), the publisher's point
    places it: tier "own". Fukuoka's MHLW rows (2026-09-28): MHLW's
    points sit a median 36 m from the block point, closer than any town-chōme
    centroid, and the misses are rural 大字 the block file does not cover. A
    point outside CITY_BBOX is not used, nor a default point (shared_points).
    Changes `joined` in place."""
    sources = getattr(config, "OWN_POINT_FALLBACK", set())
    if not sources:
        return
    bb = config.CITY_BBOX
    mine = joined["source"].isin(sources)
    datum_guard(config, joined[mine])
    # Towns are counted only over rows the join read (owner's call 202,
    # 2026-10-07): an address the join could not parse keeps its raw tail in
    # `town`, so one premises written three ways (Kasukabe's AEON Mall, 下柳 and
    # 下柳イオンモール…) counted as three towns and its own point was refused.
    # A switch (japan_register's "default_joined"): built cities keep the old
    # count until a review time re-renders them.
    read = mine & (joined["tier"] != "none") if "default_joined" in japan_rules(config) else mine
    default = shared_points(zip(joined.loc[read, "ward"], joined.loc[read, "town"], joined.loc[read, "pub"]))
    inb = joined["pub"].map(lambda p: p is not None and p == p and bb["lat_min"] <= p[0] <= bb["lat_max"]
                            and bb["lon_min"] <= p[1] <= bb["lon_max"] and _pt4(p) not in default)
    refused = mine & (joined["tier"] != "block") & joined["pub"].map(
        lambda p: p is not None and p == p and _pt4(p) in default)
    if refused.any():
        print(f"  a default point ({len(default)} given to {SHARED_POINT_TOWNS}+ towns) refused for "
              f"{int(refused.sum()):,} rows")
    emit("own_point_default_refused", int(refused.sum()))
    take = mine & (joined["tier"] != "block") & inb
    for tier, n in joined.loc[take, "tier"].value_counts().items():
        print(f"  the publisher's own point where the block join gave {tier}: {n:,}")
        emit(f"own_point_from_{tier}", int(n))
    joined["pt"] = [pub if t else pt for t, pub, pt in zip(take, joined["pub"], joined["pt"])]
    joined.loc[take, "tier"] = "own"


def point_donors(config, joined):
    """Where the block join misses a row and ANOTHER publisher lists the same
    premises with its own point, that point places it (config.POINT_DONORS =
    {recipient source: donor source}; tier "own"). Toyama (2026-10-02): its
    own list is complete but carries no coordinates, its 大字 addresses miss
    MLIT's block file (12.2% at a town centroid a median 360 m away), and
    MHLW's open data has a point for 614 of those 738 rows. The donor is read
    for its points only, never drawn: matched on ward, town and trade name,
    and used only where every donor row of that key gives one point (to about
    10 m) inside CITY_BBOX. Changes `joined` in place."""
    donors = getattr(config, "POINT_DONORS", {})
    if not donors:
        return
    bb = config.CITY_BBOX
    wardless = japan_wardless(config)
    for recipient, donor in donors.items():
        ps = read_permits(config, donor, source_rows(config, donor), japan_rules(config))
        default = shared_points((p["ward"], p["town"], p["pub"]) for p in ps)
        pts = collections.defaultdict(set)
        for p in ps:
            if p["pub"] and not p["closed"] and p["name"]:
                pts[(p["ward"], p["town"], jr._name_key(p["name"]))].add(_pt4(p["pub"]))
        one = {k: next(iter(v)) for k, v in pts.items() if len(v) == 1}
        one = {k: v for k, v in one.items() if v not in default
               and bb["lat_min"] <= v[0] <= bb["lat_max"] and bb["lon_min"] <= v[1] <= bb["lon_max"]}
        keys = [(w, t, jr._name_key(n)) for w, t, n in zip(joined["ward"], joined["town"], joined["name"])]
        take = pd.Series([k in one for k in keys], index=joined.index)
        take &= (joined["source"] == recipient) & (joined["tier"] != "block")
        for tier, n in joined.loc[take, "tier"].value_counts().items():
            print(f"  {donor}'s point for a {recipient} row where the block join gave {tier}: {n:,}")
            emit(f"point_from_{donor}_for_{recipient}_{tier}", int(n))
        joined["pt"] = [one[k] if t else pt for t, k, pt in zip(take, keys, joined["pt"])]
        joined.loc[take, "tier"] = "own"


def japan_wardless(config):
    """A city without wards (japan.CITIES' "wardless"): its addresses are never
    split at a 区 (japan_register.permits_from_rows)."""
    from pipeline.countries import japan
    return bool(japan.CITIES.get(config.SLUG, {}).get("wardless"))


def japan_rules(config):
    """The rules a city reads (japan.city_rules: a built city's CITIES "rules",
    WAVE2_RULES; ALL_RULES for every city after the Japan foundation), the
    same set on the MLIT side and the list's."""
    from pipeline.countries import japan
    return japan.city_rules(config.SLUG)


def page_municipalities(config):
    """A page of several municipalities (japan.CITIES' "municipalities",
    {code: MLIT's 市区町村名}; Ageo (Regional)): their names, else ()."""
    from pipeline.countries import japan
    return tuple(japan.CITIES.get(config.SLUG, {}).get("municipalities", {}).values())


def city_gaiji(config):
    """A city's own private-use code points (japan.CITIES' "gaiji",
    {code point: character}; Kawaguchi's 塚, 蓮, 樋), as a translate table."""
    from pipeline.countries import japan
    g = japan.CITIES.get(config.SLUG, {}).get("gaiji")
    return str.maketrans(g) if g else None


def other_municipalities(config):
    """The prefecture's municipalities other than the page's own, as addresses
    spell them, for the "other_muni" rule. A name the page's own municipality
    starts with is left out, so 伊奈町 never cuts an address of 伊奈町's page."""
    from pipeline.countries import japan
    own = {config.MUNICIPALITY, *getattr(config, "SOURCE_MUNICIPALITY", {}).values(), *page_municipalities(config)}
    pref = japan.CITIES[config.SLUG]["pref"]
    return tuple(sorted((n for n in japan.prefecture_municipalities(pref)
                         if not any(o.startswith(n) or n.startswith(o) for o in own)), key=len, reverse=True))


def read_permits(config, key, rows, rules, others=()):
    """One source's rows through japan_register.permits_from_rows, with the
    city's municipalities, gaiji, old place names (japan.CITIES'
    "town_aliases", Matsue's {"八雲村": "八雲町"}) and the other municipalities'
    names."""
    from pipeline.countries import japan
    aliases = japan.CITIES.get(config.SLUG, {}).get("town_aliases")
    return jr.permits_from_rows(rows, config.PREFECTURE, municipality(config, key), japan_wardless(config), rules,
                                others, page_municipalities(config), city_gaiji(config), aliases)


# The new-city checks (the Japan foundation, 2026-10-07): each trap a brief
# found by hand, raised where the next city passes. A city built before the
# foundation is not checked, since its lists carry columns read the old way.
OPERATOR_LIKE = re.compile(r"氏名|代表者|営業者|開設者|申請者|法人名|設置者")
NOT_A_NAME = re.compile(r"住所|所在地|電話|TEL|ＴＥＬ|方書|ビル名|ﾋﾞﾙ名|役職|肩書|都道府県|市町村|フラグ|郵便|番号|"
                        r"カナ|かな|ﾌﾘｶﾞﾅ|フリガナ|区分|種別")


def check_new_city_columns(config, key, rows, ps, rules):
    """Stop a new city's build where a source's columns are not read: no
    address (Hirakata's 営業所所在地①, Gifu's 営業所在地: every row read "not a
    premises"), no trade name (Tsu's 営業所屋号: the name rule compared
    nothing), no type on a food list (Gifu's 営業種別), an operator-like column
    the name rule does not compare (Neyagawa's two), or a permit term with no
    pinned as-of (calls 161 and 172). config.NOT_OPERATOR ({column: why})
    and config.NO_TRADE_NAME ({source key: why}) record a column read and
    judged otherwise."""
    from pipeline.countries import japan
    if config.SLUG in japan.BUILT_BEFORE_FOUNDATION or not rows:
        return
    heads = set().union(*(r.keys() for r in rows[:200])) - {None}
    where = f"{key}: header {sorted(map(str, heads))}"
    if not any(p["addr"].strip() for p in ps) and not any(p.get("out") for p in ps):
        sys.exit(f"{key}: no row has an address in japan_register.ADDR_COLS. Add the list's spelling there.\n{where}")
    if not any(p["name"].strip() for p in ps) and key not in getattr(config, "NO_TRADE_NAME", {}):
        sys.exit(f"{key}: no row has a trade name in japan_register.NAME_COLS (the name rule would compare "
                 f"nothing). Add the list's spelling, or name the source in config.NO_TRADE_NAME.\n{where}")
    if kind(config, key) not in japan_eigyo.PERSONAL_SOURCES and not any(p["type"].strip() for p in ps):
        sys.exit(f"{key}: no row has a type in japan_register.TYPE_COLS. Add the list's spelling.\n{where}")
    unread = sorted(h for h in map(str, heads) if OPERATOR_LIKE.search(h) and not NOT_A_NAME.search(h)
                    and h not in jr.operator_cols(rules) and h not in getattr(config, "NOT_OPERATOR", {}))
    if unread:
        sys.exit(f"{key}: {unread} look like operator columns the name rule does not compare. Add each to "
                 f"japan_register.OPERATOR_COLS, or record it in config.NOT_OPERATOR with why.\n{where}")
    if ({"past_term", "late_start"} & rules and any(p.get("end") or p.get("start") for p in ps)
            and key not in getattr(config, "TERM_AS_OF", {})):
        sys.exit(f"{key}: its rows carry a permit term (japan_register.END_COLS / START_COLS) but "
                 f"config.TERM_AS_OF names no pinned as-of for it (calls 161 and 172; never today).")


def drop_superseded(config, df):
    """One premises in two lists (config.SUPERSEDES = {newer: (older, ...)}):
    Fukuoka's city list holds permits from before 2021-06 and MHLW's the online
    filings since, and a renewal moves a premises from one to the other; the
    screen found 1.3% in both. A row of an older list whose ward, town, block,
    trade name and bucket repeat a row of the newer list is dropped (the
    screen's own key: the two lists spell addresses differently)."""
    sup = getattr(config, "SUPERSEDES", {})
    if not sup:
        return df
    key = pd.Series(list(zip(df["ward"], df["town"], df["block"].fillna(""), df["name"].map(jr._name_key),
                             df["bucket"])), index=df.index)
    drop = pd.Series(False, index=df.index)
    for newer, older in sup.items():
        have = set(key[df["source"] == newer])
        d = df["source"].isin(older) & key.isin(have)
        print(f"  in both lists, the {'/'.join(older)} row dropped for the {newer} row: {int(d.sum()):,}")
        emit(f"superseded_by_{newer}", int(d.sum()))
        drop |= d
    return df[~drop].copy()


def set_aside(config, df, rules):
    """The rows a WAVE5 rule set aside in japan_register (`out`), and step 2's
    own mobile-salon rule ("idou": Maebashi's three salons with 移動 in the
    address and the name, where the type says nothing), counted by reason
    before the closed rows and before any de-duplication: Ōita's 301 masked
    rows share seven (address, type) keys and would fold into seven phantom
    premises. Nothing changes for a built city (no rule, no `out`)."""
    why = df["out"].fillna("") if "out" in df else pd.Series("", index=df.index)
    if "idou" in rules:
        idou = df["kind"].isin(japan_eigyo.PERSONAL_SOURCES) & (
            df["addr"].fillna("").str.contains("移動") | df["name"].fillna("").str.contains("移動")) & (why == "")
        why = why.where(~idou, "mobile salon (移動)")
    if not (why != "").any():
        return df
    for reason, n in why[why != ""].value_counts().items():
        print(f"  set aside, {reason}: {n:,}")
        emit("set_aside_" + re.sub(r"[^a-z]+", "_", reason.lower()).strip("_"), int(n))
    return df[why == ""].copy()


def out_of_term(config, df, rules):
    """Calls 161 and 172 (owner, 2026-10-06): a permit past its term on the
    source's pinned as-of is dropped, and one that starts after it waits
    (config.TERM_AS_OF = {source key: date}, never today). Kure's three
    restaurants that start on 2026-09-01 or 10-01; Mito's 80 MHLW permits
    still listed past their 許可満了日."""
    if not {"past_term", "late_start"} & rules or "end" not in df:
        return df
    asof = {k: jr.wareki_date(str(v)) for k, v in getattr(config, "TERM_AS_OF", {}).items()}
    on = [asof.get(s) for s in df["source"]]

    def cmp(col, rule, sign):
        if rule not in rules or col not in df:
            return pd.Series(False, index=df.index)
        return pd.Series([bool(d and a and isinstance(d, type(a)) and sign * (d - a).days > 0)
                          for d, a in zip(df[col], on)], index=df.index)
    past = cmp("end", "past_term", -1)
    late = cmp("start", "late_start", 1)
    for label, m, k in (("past its term (call 161)", past, "past_term"), ("starting after the as-of (call 172)", late,
                                                                         "late_start")):
        print(f"  permits {label}: {int(m.sum()):,}")
        emit(f"permits_{k}", int(m.sum()))
    return df[~(past | late)].copy()


def run(config, write=True):
    sys.stdout.reconfigure(encoding="utf-8")
    need(config.ISJ_DIR, config.SLUG)
    rules = japan_rules(config)
    blocks, chome = jr.load_city_isj(config.ISJ_DIR, rules, by_municipality=bool(page_municipalities(config)))
    print(f"  MLIT 位置参照情報: {len(blocks):,} block keys, {len(chome):,} town-chōme keys")
    others = other_municipalities(config) if "other_muni" in rules else ()

    permits = []
    for key in config.SOURCES:
        rows = list(source_rows(config, key))
        missing = [c for c in config.REQUIRED_COLUMNS[key] if c not in rows[0]]
        if missing:
            sys.exit(f"{key}: header lacks {missing}")
        flags = [jr.name_is_operator(r, rules) for r in rows]
        ps = read_permits(config, key, rows, rules, others)
        check_new_city_columns(config, key, rows, ps, rules)
        # the date a row is measured by for the share at the official count's
        # date (config.SHARE_DATES = {source key: column}; at_date)
        date_col = getattr(config, "SHARE_DATES", {}).get(key)
        for p, f, r in zip(ps, flags, rows):
            p["source"], p["name_is_operator"], p["muni"] = key, f, municipality(config, key)
            p["kind"] = kind(config, key)
            if date_col:
                p["dated"] = jr.wareki_date(r.get(date_col))
        permits += ps
        emit(f"rows_{key}", len(ps))
        print(f"  {key:8} {len(ps):>7,} rows")
    del rows  # the raw rows carry the operator columns; nothing below may see them

    df = pd.DataFrame(permits)
    if "asterisk" in rules:
        # Ōita's three trade names masked with asterisks at a visible address:
        # the pin shows the permit type, never the asterisks
        masked = df["name"].map(lambda s: bool(jr.ASTERISKS.fullmatch(unicodedata.normalize("NFKC", s or "").strip())))
        df["name_is_operator"] = df["name_is_operator"] | masked
        print(f"  trade names masked by the publisher (shown as the permit type): {int(masked.sum())}")
        emit("names_masked", int(masked.sum()))
    # THE NAME RULE HOLDS PER PREMISES, not per row (Osaka, 2026-09-27): one
    # premises' second permit may record its operator differently, and the
    # one-pin-per-premises step below can keep that unflagged row - Osaka showed
    # an operator's own name on 2 pins that way (a restaurant's two food permits;
    # a salon registered as both barber and beauty). Any flagged row withholds
    # every row sharing its trade name and its block - the join's own key
    # (ward, town, block), since the salon's two registers spell the building
    # and floor differently - across registers.
    prem = pd.Series(list(zip(df["ward"], df["town"], df["block"].fillna(""), df["name"].map(jr._name_key))),
                     index=df.index)
    flagged = set(prem[df["name_is_operator"]])
    spread = prem.isin(flagged) & ~df["name_is_operator"]
    df["name_is_operator"] = df["name_is_operator"] | prem.isin(flagged)
    print(f"  name rule by premises: {int(spread.sum())} more row(s) share a flagged row's block and trade name")
    emit("name_rule_spread_rows", int(spread.sum()))
    if "name_city" in rules:
        # ACROSS PREMISES (owner, call 205, 2026-10-07): a trade name the rule
        # flags anywhere in the city is withheld everywhere in it. A citywide
        # stall (一円) has no block, so the spread above cannot carry its flag
        # to a fixed premises of the same name (Suita, 1 pin). The privacy
        # check matches trade-name keys city-wide the same way.
        keys = set(df.loc[df["name_is_operator"], "name"].map(jr._name_key)) - {""}
        across = df["name"].map(jr._name_key).isin(keys) & ~df["name_is_operator"]
        df["name_is_operator"] = df["name_is_operator"] | across
        print(f"  name rule across premises (call 205): {int(across.sum())} more row(s) share a flagged trade name")
        if across.any():
            emit("name_rule_city_rows", int(across.sum()))
    official_shares(config, df, write)
    df = set_aside(config, df, rules)
    # MHLW's open data keeps closed premises, marked (Fukuoka's second source)
    closed = df["closed"]
    if closed.any():
        print(f"  closed (廃業): {int(closed.sum()):,}")
        emit("closed", int(closed.sum()))
    df = df[~closed].copy()
    df = out_of_term(config, df, rules)
    # MHLW publishes an address only where the filer agreed to it (Fukuoka;
    # config.ADDRESS_BY_CONSENT): a row without one cannot be placed, and its
    # count is the page's disclosure. Elsewhere a blank address stays "not a
    # premises".
    noaddr = (df["addr"].fillna("").str.strip() == "") & df["source"].isin(getattr(config, "ADDRESS_BY_CONSENT", ()))
    if noaddr.any():
        by = df[noaddr]["source"].value_counts().to_dict()
        print(f"  no address published (not placeable): {int(noaddr.sum()):,}  {by}")
        emit("no_address", int(noaddr.sum()))
    mobile = df["mobile"]
    print(f"  not a premises (vehicle, stall, 一円, storeless): {int((mobile & ~noaddr).sum()):,}")
    emit("not_a_premises", int((mobile & ~noaddr).sum()))
    df = df[~mobile].copy()
    if "combined_form" in rules:
        before = df["form"].copy()
        df["form"] = df["form"].map(japan_eigyo.resolve_combined)
        n = int((before.fillna("") != df["form"].fillna("")).sum())
        print(f"  combined 業態 cells read as their restaurant form (call 158): {n:,}")
        emit("combined_form_restaurant", n)
    decided = [japan_eigyo.explain(t, s, f, rules) for t, s, f in zip(df["type"], df["kind"], df["form"])]
    df["bucket"] = [b for b, _ in decided]
    df["rule"] = [r for _, r in decided]
    out = df[df["bucket"].isna()]
    print(f"  not a storefront, by rule: {int(len(out)):,}")
    for (rule, n) in out["rule"].value_counts().items():
        print(f"    {n:>6,}  {rule}")
    emit("not_storefront", len(out))
    df = df[df["bucket"].notna()].copy()
    print(f"  storefront rows: {len(df):,}  {df['bucket'].value_counts().to_dict()}")
    by_form = df[df["rule"].str.endswith("(業態)")]
    for (rule, bucket), n in by_form.groupby(["rule", "bucket"]).size().items():
        print(f"    kept by 業態: {n:>5,}  {bucket:<12} {rule}")

    # --- the join --------------------------------------------------------------
    joined = pd.DataFrame(jr.join_city(df.to_dict("records"), blocks, chome, japan_rules(config)))
    own_point_fallback(config, joined)
    point_donors(config, joined)
    tab = pd.crosstab(joined["bucket"], joined["tier"], margins=True)
    print("  the join by bucket:\n" + "\n".join("    " + ln for ln in tab.to_string().splitlines()))
    for tier, n in joined["tier"].value_counts().items():
        emit(f"join_{tier}", int(n))
    none = joined[joined["tier"] == "none"]
    print(f"  unplaced {len(none):,} ({len(none) / len(joined):.1%}); samples:")
    for a in none["addr"].iloc[:: max(1, len(none) // 10)][:10]:
        print(f"     {a}")
    df = joined[joined["tier"] != "none"].copy()
    df["latitude"] = [p[0] for p in df["pt"]]
    df["longitude"] = [p[1] for p in df["pt"]]
    own_coordinates_check(config, df)
    bb = config.CITY_BBOX
    inb = df["latitude"].between(bb["lat_min"], bb["lat_max"]) & df["longitude"].between(bb["lon_min"], bb["lon_max"])
    if not inb.all():
        sys.exit(f"{int((~inb).sum())} joined points outside CITY_BBOX - an MLIT key from another place?")

    df = drop_superseded(config, df)

    # --- one pin per premises and bucket ------------------------------------------
    df["premises"] = [(key_addr(a), jr._name_key(n), b) for a, n, b in zip(df["addr"], df["name"], df["bucket"])]
    dup = df["premises"].duplicated()
    print(f"  one pin per premises and bucket: {int(dup.sum()):,} repeat rows dropped "
          f"(one premises, several permits of one kind)")
    emit("repeat_permits_dropped", int(dup.sum()))
    df = df[~dup].copy()

    # --- the name rule --------------------------------------------------------------
    hidden = df["name_is_operator"]
    df["permit_type"] = [REGISTER_TYPE.get(s, t) for s, t in zip(df["kind"], df["type"])]
    df["business_name"] = df["name"].where(~hidden, df["permit_type"])
    print(f"  names withheld (the trade name IS the operator's own name): {int(hidden.sum())}; "
          f"shown as their permit type")
    emit("names_withheld", int(hidden.sum()))

    # --- the owner's 菓子 / そうざい measurement --------------------------------------
    made = df["rule"].str.startswith(("confectioner", "deli"))
    fac = made & df["name"].map(lambda s: bool(FACTORY.search(unicodedata.normalize("NFKC", s or ""))))
    print(f"  菓子 / そうざい rows: {int(made.sum()):,}; trade name reads as a factory or central kitchen: "
          f"{int(fac.sum()):,} ({fac.sum() / max(1, made.sum()):.1%}) - kept, measured (owner 2026-09-24)")
    emit("sweets_deli_rows", int(made.sum()))
    emit("sweets_deli_factory_like", int(fac.sum()))

    out = df[["business_name", "permit_type", "kind", "form", "latitude", "longitude", "addr", "tier"]].rename(
        columns={"addr": "address", "kind": "source"})
    kept = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(kept) != len(out):
        sys.exit("filter_to_storefront dropped rows the buckets already decided")
    counts = collections.Counter(japan_eigyo.classify(r) for r in kept.to_dict("records"))
    print(f"  storefronts: {len(kept):,}  {dict(counts)}")
    for b, n in counts.items():
        emit(f"storefronts_{b.replace(' ', '_').lower()}", n)
    emit("storefronts", len(kept))
    if write:
        kept.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
        print(f"  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(kept):,} storefronts")
    return kept
