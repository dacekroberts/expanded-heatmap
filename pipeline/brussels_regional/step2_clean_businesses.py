"""Brussels (Regional) step 2: KBO's companies' establishment units, joined to
BeST-Address Brussels, filtered by four storefront rules -> the storefronts on
the map, in the 18 communes outside the City of Brussels.

    python pipeline/brussels_regional/step2_clean_businesses.py

Reads the caches only (`fetch_sources.py` verifies them; KBO is the owner's
download). Run it through the heavy-job gate: the first run builds the KBO
extract from the 313 MB zip (0.94 GB peak, measured 2026-10-04), later runs
read the parquet extract.

THE BASE (the licence plus currency, the brief): companies only
(TypeOfEnterprise 2), JuridicalSituation 000, the establishment address
(BAET) not struck off, in a bucket. THE BUCKET: any MAIN code in a bucket,
Food service over Retail over Personal services; establishment-level codes
first, the company's only when the unit has none; NACE-BEL 2025, 2008 only
where 2025 gives no code. Personal services is then dropped (off on this
page). THE FOUR RULES drop a unit when:
  A every in-bucket MAIN code is a catch-all (belgium_kbo's lists);
  B its address (postcode + street + number, box ignored) hosts 5 or more
    companies' units of any activity and juridical situation, fewer than half
    of them in a bucket;
  C its box is a plain number once the prefix is removed (0 is a ground-floor
    mark, not a number);
  D it lists 10 or more distinct MAIN codes, at least one outside the buckets.
Then PLACED at a number tier of the BeST join (pipeline/countries/belgium_best.py)
and SCOPED by the matched point's municipality_id among the 18 NIS codes,
never by postcode; the commune polygons and KBO's municipality field are
checked against it and the disagreements counted.

THE CONTROL runs first and stops the step if it does not reproduce (the
brief's figures, config.CONTROL_*).

NAMES: the unit's commercial name (TypeOfDenomination 003), else the
company's name (001); never contact.csv. Nothing here prints a name, a number
or an address: counts and field names only.
"""
import json
import re
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.brussels_regional import agreement, config  # noqa: E402
from pipeline.countries import belgium_best as best  # noqa: E402
from pipeline.countries import belgium_kbo as kbo  # noqa: E402
from pipeline.countries.belgium import (BEST_BRUSSELS_ZIP, KBO_ZIP,  # noqa: E402
                                        brussels_region_communes)
from pipeline.name_keys import keys_of  # noqa: E402
from pipeline.taxonomies import belgium_kbo as tax  # noqa: E402

FETCH = "pipeline/brussels_regional/fetch_sources.py"
COMMUNES_FETCH = "pipeline/brussels/fetch_sources.py"
BUCKETS = tax.PRIORITY
LANG_ORDER = {"1": 0, "2": 1, "0": 2, "3": 3, "4": 4}   # French, Dutch, unknown, German, English
REPORT = {}


def say(msg=""):
    print(msg)


def pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def by_bucket(mask, df):
    return {b: int((mask & (df["bucket"] == b)).sum()) for b in BUCKETS}


def line(label, counts):
    say(f"  {label:<52} " + "  ".join(f"{counts[b]:>7,}" for b in BUCKETS))


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
def zip_meta(path):
    meta = path.with_name(path.name + ".json")
    if not path.exists() or not meta.exists():
        sys.exit(f"missing {path.name} or its meta JSON\nRun: python {FETCH}")
    return json.loads(meta.read_text(encoding="utf-8"))


def load_extract():
    meta = zip_meta(KBO_ZIP)
    stamp = config.KBO_EXTRACT_DIR / "kbo_extract.json"
    current = json.loads(stamp.read_text(encoding="utf-8")) if stamp.exists() else {}
    if current.get("zip_sha256") != meta["sha256"]:
        say("KBO extract: building from the cached zip (no network)")
        lo, hi = config.REGION_POSTCODE_RANGE
        kbo.extract(KBO_ZIP, config.KBO_EXTRACT_DIR, lo, hi, log=say)
        kbo.write_extract_meta(config.KBO_EXTRACT_DIR, {
            "zip": KBO_ZIP.name, "zip_sha256": meta["sha256"], "postcodes": [lo, hi],
            **kbo.read_meta(KBO_ZIP)})
    else:
        say("KBO extract: cached, matches the zip's sha256")
    return kbo.load(config.KBO_EXTRACT_DIR)


# ---------------------------------------------------------------------------
# Units, codes, buckets, rules
# ---------------------------------------------------------------------------
def code_sets(act):
    """{entity: {version: frozenset(codes)}} of MAIN codes."""
    a = act[["EntityNumber", "NaceVersion", "NaceCode"]].drop_duplicates()
    g = a.groupby(["EntityNumber", "NaceVersion"])["NaceCode"].agg(frozenset)
    out = {}
    for (ent, ver), codes in g.items():
        out.setdefault(ent, {})[ver] = codes
    return out


def unit_codes(est, ent, sets):
    """(codes, version, level) by the brief's order: the unit's own 2025, its
    2008, then the company's 2025, its 2008."""
    for level, key in (("establishment", est), ("enterprise", ent)):
        s = sets.get(key, {})
        for ver in (tax.V2025, tax.V2008):
            if s.get(ver):
                return s[ver], ver, level
    return frozenset(), None, None


def build_units(x):
    adr = x["addresses"].copy()
    adr["struck"] = adr["DateStrikingOff"].notna()
    # One address per unit: a current one where the unit has several.
    adr = adr.sort_values(["EntityNumber", "struck"]).drop_duplicates("EntityNumber")
    u = x["units"].merge(adr, left_on="EstablishmentNumber", right_on="EntityNumber", how="inner")
    u = u.merge(x["enterprises"][["EnterpriseNumber", "JuridicalSituation", "JuridicalForm"]],
                on="EnterpriseNumber", how="left")
    sets = code_sets(x["activities"])
    rows = [unit_codes(e, c, sets) for e, c in zip(u["EstablishmentNumber"], u["EnterpriseNumber"])]
    u["codes"] = [r[0] for r in rows]
    u["version"] = [r[1] for r in rows]
    u["code_level"] = [r[2] for r in rows]
    bk = [tax.unit_bucket(c, v or tax.V2025) for c, v in zip(u["codes"], u["version"])]
    u["bucket"] = [b for b, _ in bk]
    u["nace_code"] = [c for _, c in bk]
    u["in_bucket_codes"] = [frozenset(c for c in cs if tax.code_bucket(c, v or tax.V2025))
                            for cs, v in zip(u["codes"], u["version"])]
    return u


GROUND_MARK = re.compile(r"\b(rdc|rez|rc|gv|glv|gelijkvloers|ground|0)\b")
FLOOR_MARK = re.compile(r"\b(et|etg|etage|eme|er|verd|verdieping|floor|e)\b|\d+(e|er|eme|st|nd|rd|th)\b")


def box_is_number(raw):
    """Rule C: the box is a plain number once its prefix is removed. A
    ground-floor mark (RDC, RC, GV, gelijkvloers, a lone 0) or a floor mark
    (2e, etage, verdieping) is not a number (the screen's box_kind)."""
    f = best.fold(raw)
    if not f or GROUND_MARK.search(f) or FLOOR_MARK.search(f):
        return False
    return best.box_norm(raw).isdigit()


def rule_flags(u):
    v = u["version"].fillna(tax.V2025)
    u["rule_a"] = [tax.only_catch_alls(cs, ver) for cs, ver in zip(u["codes"], v)]
    u["any_catch_all"] = [any(tax.is_catch_all(c, ver) for c in ib)
                          for ib, ver in zip(u["in_bucket_codes"], v)]
    # B: the companies' units at the address (postcode + street + number and
    # letter, box ignored), any activity and juridical situation, struck-off
    # addresses included as the screen counted them.
    street = u["StreetFR"].where(u["StreetFR"].notna(), u["StreetNL"])
    lang = np.where(u["StreetFR"].notna(), "fr", "nl")
    num = [best.parse_number(h) for h in u["HouseNumber"]]
    skey = [best.street_key(s, lg) if isinstance(s, str) else "" for s, lg in zip(street, lang)]
    has_key = np.array([bool(n) and bool(s) for (n, _, _), s in zip(num, skey)])
    u["addr_key"] = (u["Zipcode"].astype(str) + "|" + skey + "|" + [n + l for n, l, _ in num])
    grp = u[has_key].groupby("addr_key")
    n_at = grp.size()
    in_at = grp["bucket"].apply(lambda s: int(s.notna().sum()))
    crowded = n_at[(n_at >= config.RULE_B_MIN_UNITS)
                   & (in_at < config.RULE_B_IN_BUCKET_SHARE * n_at)].index
    u["rule_b"] = u["addr_key"].isin(set(crowded)) & has_key
    u["rule_c"] = u["Box"].map(box_is_number)
    u["rule_d"] = [len(cs) >= config.RULE_D_MIN_CODES
                   and any(tax.code_bucket(c, ver) is None for c in cs)
                   for cs, ver in zip(u["codes"], v)]
    REPORT["rule_b_addresses"] = int(len(crowded))
    return u


# ---------------------------------------------------------------------------
# Scope helpers
# ---------------------------------------------------------------------------
def kbo_municipality_nis(u):
    """KBO's municipality field (FR or NL text) -> NIS, learned from BeST's
    own commune names, then its postal names (Laeken, Haren, ...); a name that
    spans communes resolves to None."""
    names = {}
    with zipfile.ZipFile(BEST_BRUSSELS_ZIP) as z:
        n = [m for m in z.namelist() if m.endswith(".csv")][0]
        with z.open(n) as f:
            m = pd.read_csv(f, dtype=str, usecols=["municipality_id", "municipality_name_fr",
                                                   "municipality_name_nl", "postname_fr",
                                                   "postname_nl"]).drop_duplicates()
    for col in ("municipality_name_fr", "municipality_name_nl"):
        for name, nis in zip(m[col], m["municipality_id"]):
            names.setdefault(best.fold(name), set()).add(nis)
    post = {}
    for col in ("postname_fr", "postname_nl"):
        for name, nis in zip(m[col], m["municipality_id"]):
            post.setdefault(best.fold(name), set()).add(nis)
    for k, v in post.items():
        if k not in names:
            names[k] = v
    def one(fr, nl):
        for s in (fr, nl):
            hit = names.get(best.fold(s)) if isinstance(s, str) else None
            if hit and len(hit) == 1:
                return next(iter(hit))
        return None
    return [one(fr, nl) for fr, nl in zip(u["MunicipalityFR"], u["MunicipalityNL"])]


def pick_names(den, units):
    """(name, source) per unit: the unit's commercial name, else the company's."""
    d = den.copy()
    d["lang_rank"] = d["Language"].map(LANG_ORDER).fillna(9)
    d = d.sort_values(["EntityNumber", "TypeOfDenomination", "lang_rank", "Denomination"])
    commercial = d[d["TypeOfDenomination"] == kbo.COMMERCIAL_NAME].drop_duplicates("EntityNumber")
    company = d[d["TypeOfDenomination"] == kbo.COMPANY_NAME].drop_duplicates("EntityNumber")
    cm = dict(zip(commercial["EntityNumber"], commercial["Denomination"]))
    co = dict(zip(company["EntityNumber"], company["Denomination"]))
    names, sources = [], []
    for est, ent in zip(units["EstablishmentNumber"], units["EnterpriseNumber"]):
        if cm.get(est):
            names.append(cm[est]); sources.append("commercial")
        elif co.get(ent):
            names.append(co[ent]); sources.append("company")
        else:
            names.append(None); sources.append("none")
    return names, sources


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    best_meta = zip_meta(BEST_BRUSSELS_ZIP)
    x = load_extract()
    kmeta = kbo.read_meta(KBO_ZIP)
    say(f"KBO snapshot {kmeta['SnapshotDate']}, extract {kmeta['ExtractNumber']}; "
        f"BeST {best_meta.get('fetched')}")

    u = build_units(x)
    say(f"\nCompanies' establishment units with an establishment address in the Region's "
        f"postcodes: {len(u):,}")
    lv = u["code_level"].value_counts(dropna=False).to_dict()
    vv = u["version"].value_counts(dropna=False).to_dict()
    say(f"  codes from: {lv}; NACE version used: {vv}")
    u = rule_flags(u)

    # --- The base -----------------------------------------------------------
    say(f"\n  {'filter':<52} " + "  ".join(f"{b[:7]:>7}" for b in BUCKETS))
    in_bucket = u["bucket"].notna()
    line("in a bucket (any juridical situation or address)", by_bucket(in_bucket, u))
    js = u["JuridicalSituation"] == "000"
    line("  and JuridicalSituation 000", by_bucket(in_bucket & js, u))
    base = in_bucket & js & ~u["struck"]
    line("  and the establishment address not struck off = BASE", by_bucket(base, u))
    REPORT["base"] = by_bucket(base, u)
    for r in "abcd":
        REPORT[f"rule_{r}"] = by_bucket(base & u[f"rule_{r}"], u)
        line(f"    rule {r.upper()} names", REPORT[f"rule_{r}"])
    dropped = u["rule_a"] | u["rule_b"] | u["rule_c"] | u["rule_d"]
    kept = base & ~dropped
    REPORT["kept"] = by_bucket(kept, u)
    line("  after rules A-D = KEPT", REPORT["kept"])
    REPORT["catch_all_share_base"] = {b: pct(int((base & u["any_catch_all"] & (u["bucket"] == b)).sum()),
                                             int((base & (u["bucket"] == b)).sum())) for b in BUCKETS}
    say(f"  catch-all code on the unit (any in-bucket MAIN code), share of the base: "
        f"{REPORT['catch_all_share_base']}")

    # --- The join -----------------------------------------------------------
    say("\nBeST-Address Brussels: loading")
    b = best.load(BEST_BRUSSELS_ZIP)
    say(f"  rows read {b.attrs['rows_read']:,}; kept {len(b):,} "
        f"({b['status'].value_counts().to_dict()})")
    idx = best.Index(b)
    multi = idx.street_keys_in_several_postcodes()
    say(f"  street keys (strict, either language) in more than one postcode: {multi:,}")
    REPORT["street_keys_multi_postcode"] = multi
    j = [idx.join(pc, sf, sn, h, bx) if bs else (None, None)
         for pc, sf, sn, h, bx, bs in zip(u["Zipcode"], u["StreetFR"], u["StreetNL"],
                                          u["HouseNumber"], u["Box"], base)]
    u["tier"] = [t for t, _ in j]
    u["lat"] = [r[1] if r else np.nan for _, r in j]
    u["lon"] = [r[2] if r else np.nan for _, r in j]
    u["best_nis"] = [r[3] if r else None for _, r in j]
    tiers = config.KEEP_LOOSE_TIER and best.PLACED_TIERS or (1, 2, 3)
    u["placed"] = u["tier"].isin(tiers)

    def tier_table(mask, title):
        say(f"\n  join tiers, {title}:")
        out = {}
        for bk in BUCKETS + ("All",):
            m = mask & ((u["bucket"] == bk) if bk != "All" else True)
            n = int(m.sum())
            row = {best.TIER_NAMES[t]: pct(int((m & (u["tier"] == t)).sum()), n) for t in (1, 2, 3, 4, 5, 0)}
            row["placed"] = pct(int((m & u["placed"]).sum()), n)
            row["units"] = n
            out[bk] = row
            say(f"    {bk:<18} {n:>7,}  " + "  ".join(f"{k[:14]} {v}" for k, v in row.items()
                                                    if k not in ("units",)))
        return out

    REPORT["join_region"] = tier_table(base, "the base, Region (all postcodes)")
    city_pc = u["Zipcode"].astype(str).isin(config.CITY_POSTCODES)
    REPORT["join_city_control"] = tier_table(base & city_pc, "the base, the City's four postcodes (CONTROL)")

    # --- The control ----------------------------------------------------------
    ctl = REPORT["join_city_control"]["All"]
    say(f"\nCONTROL join: exact {ctl['exact']} (brief {config.CONTROL_JOIN['exact']}), "
        f"placed {ctl['placed']} (brief {config.CONTROL_JOIN['placed']})")
    start = pd.to_datetime(u["StartDate"], format="%d-%m-%Y", errors="coerce")
    survey = pd.Timestamp(config.SURVEY_DATE)
    u["bset"] = [frozenset(filter(None, (tax.code_bucket(c, ver or tax.V2025) for c in cs)))
                 for cs, ver in zip(u["codes"], u["version"])]
    xy = gpd.GeoSeries(gpd.points_from_xy(u["lon"], u["lat"]), crs=config.CRS_GEOGRAPHIC)
    u["geom"] = list(xy.to_crs(config.CRS_PROJECTED).values)
    hub = agreement.hub_points(config.HUB_JSON, config.CITY_POSTCODES, config.CRS_PROJECTED)
    evaluated = kept & u["placed"] & city_pc & (start <= survey)
    pool = kept & u["placed"]
    say(f"  survey rows on the four postcodes: {len(hub):,}; KBO units evaluated: "
        f"{int(evaluated.sum()):,}; recall pool (kept, placed, Region): {int(pool.sum()):,}")
    REPORT["agreement"] = {}
    for radius in (config.MATCH_RADIUS_M, 5.0):
        res = agreement.measure(u[evaluated], u[pool], hub, radius)
        for bk, r in res.items():
            r["ratio_placed_to_survey"] = round(int((kept & u["placed"] & city_pc & (u["bucket"] == bk)).sum())
                                                / r["hub_shops"], 2) if r["hub_shops"] else None
            say(f"  {radius:>4g} m {bk:<18} precision {r['precision']}  recall {r['recall']}  "
                f"(evaluated {r['kbo_units']:,}, survey {r['hub_shops']:,}; "
                f"City placed / survey {r['ratio_placed_to_survey']})")
        REPORT["agreement"][f"{radius:g} m"] = res
    # Before the rules, for the record.
    ev0, pool0 = base & u["placed"] & city_pc & (start <= survey), base & u["placed"]
    REPORT["agreement"]["before rules, 15 m"] = agreement.measure(u[ev0], u[pool0], hub,
                                                                 config.MATCH_RADIUS_M)
    say("  before the rules, 15 m: " + "; ".join(
        f"{bk} {r['precision']}/{r['recall']}" for bk, r in REPORT["agreement"]["before rules, 15 m"].items()))
    # The loose tier's own precision (evaluated units placed at tier 4 only).
    ev4 = evaluated & (u["tier"] == 4)
    if ev4.any():
        r4 = agreement.measure(u[ev4], u[pool], hub, config.MATCH_RADIUS_M)
        REPORT["agreement"]["tier 4 only, 15 m"] = r4
        say("  tier 4 only, 15 m precision: " + "; ".join(
            f"{bk} {r['precision']} of {r['kbo_units']}" for bk, r in r4.items()))
    for t in (1, 2, 3):
        evt = evaluated & (u["tier"] == t)
        rt = agreement.measure(u[evt], u[pool], hub, config.MATCH_RADIUS_M)
        REPORT["agreement"][f"tier {t} only, 15 m"] = rt
        say(f"  tier {t} only, 15 m precision: " + "; ".join(
            f"{bk} {r['precision']} of {r['kbo_units']}" for bk, r in rt.items()))

    off = []
    ag = REPORT["agreement"][f"{config.MATCH_RADIUS_M:g} m"]
    tol = config.CONTROL_TOLERANCE_PTS
    for key, want in config.CONTROL_JOIN.items():
        if abs(ctl[key] - want) > tol:
            off.append(f"join {key} {ctl[key]} vs {want}")
    for bk, (p, r) in config.CONTROL_AGREEMENT.items():
        if abs(ag[bk]["precision"] - p) > tol or abs(ag[bk]["recall"] - r) > tol:
            off.append(f"{bk} {ag[bk]['precision']}/{ag[bk]['recall']} vs {p}/{r}")
    REPORT["control_reproduced"] = not off
    config.STEP2_REPORT_JSON.write_text(json.dumps(REPORT, indent=2, default=str), encoding="utf-8")
    if off:
        sys.exit("CONTROL NOT REPRODUCED (" + "; ".join(off) + "): no count is trusted")
    say("  CONTROL REPRODUCED")

    # --- Scope: the 18 communes by the matched point's NIS code ---------------
    placed = kept & u["placed"]
    line("\n  kept and placed at a number tier (Region)", by_bucket(placed, u))
    REPORT["placed_region"] = by_bucket(placed, u)
    p = u[placed].copy()
    p["kbo_nis"] = kbo_municipality_nis(p)
    com = brussels_region_communes(config.COMMUNES_GEOJSON, COMMUNES_FETCH)
    pts = gpd.GeoDataFrame(geometry=gpd.points_from_xy(p["lon"], p["lat"]), index=p.index,
                           crs=config.CRS_GEOGRAPHIC)
    hit = gpd.sjoin(pts, com[["nis", "geometry"]], how="left", predicate="within")
    hit = hit[~hit.index.duplicated()]
    p["poly_nis"] = hit["nis"].astype(object).where(hit["nis"].notna(), None)
    in_scope = p["best_nis"].isin(set(config.SCOPE_CODES))
    dis_poly = int((p["best_nis"] != p["poly_nis"]).sum())
    dis_kbo = int((p["kbo_nis"].notna() & (p["best_nis"] != p["kbo_nis"])).sum())
    no_kbo = int(p["kbo_nis"].isna().sum())
    scope_edge = int((in_scope != p["kbo_nis"].isin(set(config.SCOPE_CODES))).sum())
    REPORT["scope"] = {"best_vs_polygon": dis_poly, "best_vs_kbo_field": dis_kbo,
                       "kbo_field_unresolved": no_kbo, "in_or_out_differs_from_kbo_field": scope_edge,
                       "best_nis_city": int((p["best_nis"] == config.CITY_COMMUNE_CODE).sum())}
    say(f"  scope checks (placed units, Region): BeST NIS vs commune polygon disagree {dis_poly:,}; "
        f"vs KBO's municipality field {dis_kbo:,} ({no_kbo:,} field values unresolved); "
        f"in/out of the 18 differs from the field's answer {scope_edge:,}")
    p = p[in_scope].copy()
    say(f"  in the 18 communes (BeST municipality_id): " + ", ".join(
        f"{bk} {int((p['bucket'] == bk).sum()):,}" for bk in BUCKETS))
    REPORT["placed_18"] = {bk: int((p["bucket"] == bk).sum()) for bk in BUCKETS}
    off_b = p["bucket"].isin(config.BUCKETS_OFF)
    say(f"  {', '.join(config.BUCKETS_OFF)} off on this page: {int(off_b.sum()):,} units leave")
    p = p[~off_b].copy()
    REPORT["per_commune"] = {config.SCOPE_CODES[n]: {bk: int(((p["best_nis"] == n) & (p["bucket"] == bk)).sum())
                                                    for bk in BUCKETS if bk not in config.BUCKETS_OFF}
                             for n in config.SCOPE_CODES}

    # --- Names, labels, output ----------------------------------------------
    names, sources = pick_names(x["denominations"], p)
    p["business_name"] = names
    p["name_source"] = sources
    REPORT["names"] = p["name_source"].value_counts().to_dict()
    say(f"  dot names: {REPORT['names']}")
    labels = kbo.code_labels(KBO_ZIP)
    p["nace_version"] = p["version"]
    p["nace_label"] = [f"{c[:2]}.{c[2:]} {labels.get((v, c), '')}".strip()
                       for c, v in zip(p["nace_code"], p["nace_version"])]
    unnamed = p["business_name"].isna()
    person = keys_of(p["business_name"].fillna("")).isin(config.PERSON_NAMED) & ~unnamed
    p.loc[unnamed | person, "business_name"] = p.loc[unnamed | person, "nace_label"]
    p["name_is_type"] = unnamed | person
    say(f"  no name: {int(unnamed.sum())}; withheld as a person's own name: {int(person.sum())}")
    p["category"] = p["bucket"]
    p["latitude"], p["longitude"] = p["lat"], p["lon"]
    street = p["StreetFR"].where(p["StreetFR"].notna(), p["StreetNL"])
    box = p["Box"].where(p["Box"].notna(), "")
    p["address"] = (street.fillna("") + " " + p["HouseNumber"].fillna("")
                    + np.where(box != "", " bte " + box, "") + ", " + p["Zipcode"].astype(str))
    p["municipality_nis"] = p["best_nis"]
    p["join_tier"] = p["tier"].astype(int)
    out = p[["business_name", "name_source", "name_is_type", "nace_label", "nace_code", "nace_version",
             "category", "address", "municipality_nis", "join_tier", "latitude", "longitude"]]
    out = out.sort_values(["municipality_nis", "latitude", "longitude", "nace_code", "business_name"])
    bb = config.BRUSSELS_REGIONAL_BBOX
    assert out["latitude"].between(bb["lat_min"], bb["lat_max"]).all()
    assert out["longitude"].between(bb["lon_min"], bb["lon_max"]).all()
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    say(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    for bk in BUCKETS:
        if bk not in config.BUCKETS_OFF:
            emit(f"bucket_{bk.lower().replace(' ', '_')}", int((out["category"] == bk).sum()))
    emit("storefronts", len(out))

    near_city_only(out)
    config.STEP2_REPORT_JSON.write_text(json.dumps(REPORT, indent=2, default=str), encoding="utf-8")


def near_city_only(out):
    """Placed units within the ring's outer edge of a City station and of no
    regional one (they fall outside every ring on this page)."""
    if not config.CITY_STATIONS_CSV.exists():
        say("  (no City stations file: near-a-City-station count skipped)")
        return
    def proj(df):
        g = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), crs=config.CRS_GEOGRAPHIC)
        return g.to_crs(config.CRS_PROJECTED)
    pts = proj(out)
    city = proj(pd.read_csv(config.CITY_STATIONS_CSV))
    near_city = pts.distance(city.union_all()) <= config.NEAR_CITY_STATION_M
    if config.STATIONS_CSV.exists():
        reg = proj(pd.read_csv(config.STATIONS_CSV))
        near_reg = pts.distance(reg.union_all()) <= config.NEAR_CITY_STATION_M
        what = "this page's stations.csv"
    else:
        near_reg = pd.Series(False, index=pts.index)
        what = "no regional stations yet (upper bound)"
    only = near_city.values & ~near_reg.values
    REPORT["near_city_station_only"] = {
        "radius_m": round(config.NEAR_CITY_STATION_M, 1), "regional_stations": what,
        "near_city_station": int(near_city.sum()), "near_city_station_only": int(only.sum()),
        "by_bucket": {bk: int((only & (out["category"] == bk).values).sum()) for bk in BUCKETS}}
    say(f"  within {config.NEAR_CITY_STATION_M:.1f} m of a City station: {int(near_city.sum()):,}; "
        f"of those, within it of no regional station: {int(only.sum()):,} ({what})")


if __name__ == "__main__":
    main()
