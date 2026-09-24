"""Rotterdam step 2: permit premises rebuilt from notices + BAG shop units.

    python pipeline/rotterdam/step2_clean_businesses.py

Two layers of different kinds, read from the cache fetch_sources.py wrote:

  * PERMIT PREMISES - rebuilt, because Rotterdam publishes no hospitality
    register. Every exploitation-permit decision is a Gemeenteblad notice with
    a point; a permit runs five years (a coffeeshop's one), so the premises in
    business are approximately the places with a grant inside that term before
    the harvest date. Notices are sorted by their OWN TITLE - the rubric alone
    is not the set - and grants for one place, which land within a few metres,
    are merged. No trade name is used: a notice's title and abstract sometimes
    carry one, and the page promises none.
  * BAG SHOP UNITS - every `winkelfunctie` unit in use, from PDOK, with its
    address. A unit also registered as a dwelling is left off (Amsterdam's
    owner call). No name, no activity: the pin shows its address.

A shop-class unit at a permit premises is the same premises; the notices carry
no address, so the two are de-duplicated by DISTANCE (config.DEDUP_M), the
permit kept. Every count is printed. Nothing here fetches.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.rotterdam import config  # noqa: E402
from pipeline.rotterdam.boundary import city_polygon  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies import rotterdam_source as TAX  # noqa: E402

# A notice's kind, read from its own title, first match wins. THREE title forms
# exist, measured on the 2026-09-24 harvest: the decision sentence ("... heeft
# besloten een exploitatievergunning te verlenen voor:"), "kind - street
# number", and - to early 2022 - "Exploitatievergunning verleend aan <name>"
# (284) beside "Vergunning Drank en Horeca verleend aan <name>" (165, the
# alcohol licence under the law the Alcoholwet replaced). A title that fits no
# kind is left out and printed: on that harvest, pre-emption-right notices
# ("voorlopig voorkeursrecht" - not "voorlopige"), a few planning notices, and
# regulations.
KINDS = (
    ("withdrawn", r"intrek|ingetrokken"),
    ("refused", r"weiger"),
    ("coffeeshop", r"coffeeshop"),
    ("event", r"kortlopende"),
    ("sex business", r"seksbedrijf|seksinrichting"),
    ("gaming", r"kansspelautomaten|speelautomaten|aanwezigheidsvergunning|^aanwezigheid\s+-"),
    ("terrace", r"terrasvlonder|tom[-\s]+beschikking|^terras"),
    ("alcohol licence", r"alcoholwet|drank en horeca"),
    ("bylaw permit", r"artikel \d+[:.]\d+ van de apv"),
    ("voorlopige", r"voorlopige"),
    ("exploitatie", r"exploitatievergunning te (verlenen|wijzigen)|^exploitatie\s+-"
                    r"|^exploitatievergunning verleend"),
)
KEPT = set(TAX.PERMIT_KINDS)


def _load(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/rotterdam/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def kind_of(title):
    t = (title or "").lower()
    for kind, pat in KINDS:
        if re.search(pat, t):
            return kind
    return "unrecognised"


def _utm(lon, lat):
    return gpd.GeoSeries(gpd.points_from_xy(lon, lat), crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED)


def clusters(pts, link_m):
    """Single-linkage groups of points within link_m of each other (projected)."""
    xy = np.column_stack([pts.x.values, pts.y.values])
    parent = list(range(len(xy)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    order = np.argsort(xy[:, 0])
    for a_pos, a in enumerate(order):
        for b in order[a_pos + 1:]:
            if xy[b, 0] - xy[a, 0] > link_m:
                break
            if np.hypot(*(xy[a] - xy[b])) <= link_m:
                parent[find(a)] = find(b)
    return [find(i) for i in range(len(xy))]


def load_permits(as_of):
    raw = pd.DataFrame(_load(config.NOTICES_JSON))
    print(f"  notices harvested: {len(raw):,}")
    emit("notices", len(raw))
    raw["kind"] = raw["title"].map(kind_of)
    print("  by kind (their own titles): " + ", ".join(
        f"{k} {v:,}" for k, v in raw["kind"].value_counts().items()))
    odd = raw[raw["kind"] == "unrecognised"]
    if len(odd):
        print(f"  {len(odd)} titles fit no kind - left out:")
        for t in odd["title"].head(8):
            print(f"      {t[:110]}")
    pt = raw["locatiepunt"].fillna("").str.extract(r"^\s*([-\d.]+)\s+([-\d.]+)\s*$").astype(float)
    raw["latitude"], raw["longitude"] = pt[0], pt[1]
    raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
    lo_permit = pd.Timestamp(as_of.replace(year=as_of.year - config.PERMIT_YEARS))
    lo_shop = pd.Timestamp(as_of.replace(year=as_of.year - config.COFFEESHOP_YEARS))
    window = np.where(raw["kind"] == "coffeeshop", raw["date"] >= lo_shop, raw["date"] >= lo_permit)
    grants = raw[raw["kind"].isin(KEPT) & window].copy()
    no_point = int(grants["latitude"].isna().sum())
    print(f"  kept kinds inside their term (exploitation and provisional since {lo_permit.date()}, "
          f"coffeeshops since {lo_shop.date()}): {len(grants):,}; {no_point} with no point - dropped")
    grants = grants.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)
    emit("grants_in_term", len(grants))

    # --- one premises per place ---------------------------------------------
    pts = _utm(grants["longitude"], grants["latitude"])
    grants["premises"] = clusters(pts, config.MERGE_M)
    exact = grants.groupby(["latitude", "longitude"]).ngroups
    print(f"  {len(grants):,} grants -> {grants['premises'].nunique():,} premises merged within "
          f"{config.MERGE_M:g} m ({exact:,} exact points)")

    # A withdrawal or refusal at a premises, dated after its latest grant, ends it.
    ends = raw[raw["kind"].isin(["withdrawn", "refused"])].dropna(subset=["latitude"])
    ended = set()
    if len(ends):
        gp = _utm(grants["longitude"], grants["latitude"])
        for _, e in ends.iterrows():
            ep = _utm([e["longitude"]], [e["latitude"]]).iloc[0]
            near = grants[gp.distance(ep).values <= config.MERGE_M]
            for pid, g in near.groupby("premises"):
                if g["date"].max() < e["date"]:
                    ended.add(pid)
    print(f"  {len(ends)} withdrawal or refusal notice(s); {len(ended)} premises ended by one")
    grants = grants[~grants["premises"].isin(ended)]

    latest = grants.sort_values("date").groupby("premises").tail(1)
    shop = grants.groupby("premises")["kind"].agg(lambda k: "coffeeshop" in set(k))
    latest = latest.assign(kind=np.where(latest["premises"].map(shop), "coffeeshop", latest["kind"]))
    print("  premises by kind: " + ", ".join(f"{k} {v:,}" for k, v in latest["kind"].value_counts().items()))
    emit("permit_premises", len(latest))
    return pd.DataFrame({
        "record_id": "permit:" + latest["identifier"].astype(str),
        "source": "permit",
        "business_name": TAX.PERMIT_NAME,
        "name_is_address": False,
        "address": None,
        "latitude": latest["latitude"].values,
        "longitude": latest["longitude"].values,
        "activity": latest["kind"].map(TAX.PERMIT_KINDS).values,
        "notice_kind": latest["kind"].values,
        "last_notice": latest["date"].dt.date.astype(str).values,
    })


def load_bag():
    feats = _load(config.BAG_UNITS_JSON)
    units = pd.DataFrame([f["properties"] for f in feats])
    units["longitude"] = [f["geometry"]["coordinates"][0] for f in feats]
    units["latitude"] = [f["geometry"]["coordinates"][1] for f in feats]
    print(f"  BAG shop-class units in use: {len(units):,}")
    emit("bag_units_in_use", len(units))
    classes = units["gebruiksdoel"].fillna("").map(lambda s: {x.strip() for x in s.split(",") if x.strip()})
    also = classes.map(lambda c: bool(c & set(config.BAG_EXCLUDE_IF_ALSO)))
    mixed = classes.map(len) > 1
    print(f"  {int((~mixed).sum()):,} shop-only, {int(mixed.sum()):,} mixed, of which "
          f"{int(also.sum()):,} also a dwelling - LEFT OFF (Amsterdam's owner call)")
    units = units[~also].copy()
    emit("bag_units_kept", len(units))

    def addr(r):
        s = f"{r['openbare_ruimte']} {r['huisnummer']}{r['huisletter'] or ''}"
        return f"{s}-{r['toevoeging']}" if r["toevoeging"] else s
    units["address"] = units.apply(addr, axis=1)
    return pd.DataFrame({
        "record_id": "bag:" + units["identificatie"].astype(str),
        "source": "bag",
        "business_name": units["address"].values,
        "name_is_address": True,
        "address": units["address"].values,
        "latitude": units["latitude"].values,
        "longitude": units["longitude"].values,
        "activity": TAX.BAG_LABEL,
        "notice_kind": None,
        "last_notice": None,
    })


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    # The term is counted back from the HARVEST date, never from today, so a
    # rebuild of the same cache gives the same premises.
    as_of = date.fromisoformat(prov["notices"]["retrieved"][:10])
    print(f"Permit notices (harvested {as_of}):")
    permits = load_permits(as_of)
    print("\nBAG:")
    bag = load_bag()

    # --- de-duplication: a shop unit at a permit premises ------------------
    pp = _utm(permits["longitude"], permits["latitude"])
    bp = _utm(bag["longitude"], bag["latitude"])
    tree = gpd.GeoDataFrame(geometry=pp)
    nearest = gpd.sjoin_nearest(gpd.GeoDataFrame(geometry=bp), tree, distance_col="d")
    d = nearest.groupby(level=0)["d"].min().reindex(range(len(bag)))
    print("\n  nearest permit premises to each shop unit: " + ", ".join(
        f"<= {m:g} m {int((d <= m).sum()):,}" for m in (0.5, 1, 3, 5, 10, 25)))
    dup = (d <= config.DEDUP_M).values
    print(f"  de-duplication within {config.DEDUP_M:g} m: {int(dup.sum()):,} shop units at a kept "
          f"permit premises - the permit is kept (it says what trades there)")
    emit("bag_deduplicated", int(dup.sum()))
    bag = bag[~dup]

    df = pd.concat([permits, bag], ignore_index=True)
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    if len(df) != before:
        sys.exit(f"filter_to_storefront dropped {before - len(df)} rows the layers already "
                 f"decided - the taxonomy and step 2 disagree")

    # --- both layers are the gemeente's own; check rather than assume -------
    poly = city_polygon(verbose=False)
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(poly).values
    if (~inside).any():
        print(f"  {int((~inside).sum())} rows fall outside the gemeente polygon - dropped: " + ", ".join(
            f"{k} {v}" for k, v in df.loc[~inside, "source"].value_counts().items()))
    df = df[inside]
    b = config.ROTTERDAM_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()
    if df["record_id"].duplicated().any():
        sys.exit("a record appears twice")

    print(f"\n  {len(df):,} storefronts: " + ", ".join(
        f"{k} {v:,}" for k, v in df["source"].value_counts().items()))
    emit("storefronts", len(df))
    out = df[["record_id", "source", "business_name", "name_is_address", "address",
              "latitude", "longitude", "activity", "notice_kind", "last_notice"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
