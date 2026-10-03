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
ADDRESS_BY_CONSENT, OWN_POINT_FALLBACK, POINT_DONORS, SUPERSEDES; a city
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
    default = shared_points(zip(joined.loc[mine, "ward"], joined.loc[mine, "town"], joined.loc[mine, "pub"]))
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
        ps = jr.permits_from_rows(source_rows(config, donor), config.PREFECTURE, municipality(config, donor),
                                  wardless, japan_rules(config))
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
    """The join rules a city opts into (japan.CITIES' "rules";
    japan_register.WAVE2_RULES), the same set on the MLIT side and the list's."""
    from pipeline.countries import japan
    return frozenset(japan.CITIES.get(config.SLUG, {}).get("rules", ()))


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


def run(config, write=True):
    sys.stdout.reconfigure(encoding="utf-8")
    need(config.ISJ_DIR, config.SLUG)
    blocks, chome = jr.load_city_isj(config.ISJ_DIR, japan_rules(config))
    print(f"  MLIT 位置参照情報: {len(blocks):,} block keys, {len(chome):,} town-chōme keys")

    permits = []
    for key in config.SOURCES:
        rows = list(source_rows(config, key))
        missing = [c for c in config.REQUIRED_COLUMNS[key] if c not in rows[0]]
        if missing:
            sys.exit(f"{key}: header lacks {missing}")
        flags = [jr.name_is_operator(r) for r in rows]
        ps = jr.permits_from_rows(rows, config.PREFECTURE, municipality(config, key), japan_wardless(config),
                                  japan_rules(config))
        for p, f in zip(ps, flags):
            p["source"], p["name_is_operator"], p["muni"] = key, f, municipality(config, key)
            p["kind"] = kind(config, key)
        permits += ps
        emit(f"rows_{key}", len(ps))
        print(f"  {key:8} {len(ps):>7,} rows")
    del rows  # the raw rows carry the operator columns; nothing below may see them

    df = pd.DataFrame(permits)
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
    official_shares(config, df, write)
    # MHLW's open data keeps closed premises, marked (Fukuoka's second source)
    closed = df["closed"]
    if closed.any():
        print(f"  closed (廃業): {int(closed.sum()):,}")
        emit("closed", int(closed.sum()))
    df = df[~closed].copy()
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
    decided = [japan_eigyo.explain(t, s, f) for t, s, f in zip(df["type"], df["kind"], df["form"])]
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
