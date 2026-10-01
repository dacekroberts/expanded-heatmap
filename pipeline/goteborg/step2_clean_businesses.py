"""Göteborg step 2: the food register -> the food storefronts placed inside
Göteborgs Stad.

    python pipeline/goteborg/step2_clean_businesses.py

Reads the cache only (pipeline/goteborg/fetch_sources.py downloads). What a
reader should know before trusting the counts printed below:

  * the register is ONE ROW PER PREMISES, with no dates of any kind;
  * its `typ` is Göteborg's own local type, so this step DERIVES the
    taxonomy's `VerksamhetsTyp` from it (config.TYP_STOREFRONT); every other
    type is out with its reason (config.TYP_EXCLUDED), and a type in neither
    table stops the step;
  * a blank `typ` goes on only where the taxonomy's name rules call the name a
    storefront (owner, call 20), flagged `name_classified`;
  * typed storefronts still pass the module's name tests (an institutional
    kitchen, a caterer or mobile unit, a pharmacy);
  * vending machines are dropped by name (config.VENDING_NAME);
  * `lat`/`lon` place each premises, checked against the register's own
    SWEREF 99 12 00 position; a premises at the register's FALLBACK point
    (the Environment Administration's own address, for rows with no correct
    address) is not placed, nor one at an apartment (a home); the kommun
    polygon drops anything outside;
  * a premises named only as a person shows its address (config.PERSON_NAMED).
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.goteborg import config  # noqa: E402
from pipeline.goteborg.kommuner import goteborg_geometry  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
FETCH = "pipeline/goteborg/fetch_sources.py"


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}: run python {FETCH}")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(config.REGISTER_CSV, sep=";", encoding="utf-8-sig", dtype=str,
                     keep_default_na=False)
    if tuple(df.columns) != config.REGISTER_COLUMNS:
        sys.exit(f"register columns changed: {list(df.columns)}")
    df["typ"] = df["typ"].str.strip()
    df["business_name"] = df["namn"].str.strip()
    print(f"  {len(df):,} register rows (one per premises)")

    # The derived type. Mapped-type checks first: a type the tables do not know
    # stops the step rather than vanishing.
    assert not set(config.TYP_STOREFRONT) & set(config.TYP_EXCLUDED)
    assert set(config.TYP_STOREFRONT.values()) <= set(TAX.TYPE_TO_BUCKET)
    seen = set(df["typ"]) - {""}
    unknown = sorted(seen - set(config.TYP_STOREFRONT) - set(config.TYP_EXCLUDED))
    if unknown:
        sys.exit(f"  typ value(s) neither kept nor excluded: {unknown} - read them by name "
                 f"and add each to config.TYP_STOREFRONT or TYP_EXCLUDED")
    stale = sorted((set(config.TYP_STOREFRONT) | set(config.TYP_EXCLUDED)) - seen)
    if stale:
        print(f"  note: config types no longer in the register: {stale}")

    blank = df["typ"] == ""
    store = df["typ"].isin(config.TYP_STOREFRONT)
    excl = df["typ"].isin(config.TYP_EXCLUDED)
    print(f"    typed storefront types {int(store.sum()):,}; excluded types "
          f"{int(excl.sum()):,}; blank typ {int(blank.sum()):,}")
    reasons = df[excl].groupby(df.loc[excl, "typ"].map(config.TYP_EXCLUDED)).size()
    for why, n in reasons.sort_values(ascending=False).items():
        print(f"      out {n:>5,}  {why}")

    # Owner call 20: a blank typ is classified by name, or dropped.
    by_name = df["business_name"].map(TAX.name_bucket)
    df["name_classified"] = blank & by_name.notna()
    print(f"    blank typ classified by name: {int(df['name_classified'].sum()):,} "
          f"(food service {int((blank & (by_name == 'Food service')).sum())}, food shops "
          f"{int((blank & (by_name == 'Retail')).sum())}); dropped "
          f"{int((blank & by_name.isna()).sum()):,}")

    df[TAX.VALUE_COLUMN] = df["typ"].map(config.TYP_STOREFRONT).fillna("")
    df.loc[df["name_classified"], TAX.VALUE_COLUMN] = TAX.NAME_CLASSIFIED_VALUE
    p = df[store | df["name_classified"]].copy()

    vend = p["business_name"].str.contains(config.VENDING_NAME, regex=True)
    print(f"    vending machines dropped by name: {int(vend.sum())} "
          f"({'; '.join(p.loc[vend, 'business_name'])})")
    p = p[~vend]

    by_rule = pd.Series([TAX.classify({TAX.VALUE_COLUMN: v, "business_name": n,
                                       "name_classified": c})
                         for v, n, c in zip(p[TAX.VALUE_COLUMN], p["business_name"],
                                            p["name_classified"])], index=p.index)
    named_out = (~p["name_classified"]) & by_rule.isna()
    print(f"    typed storefronts excluded by the module's name tests (an institutional "
          f"kitchen, a caterer or mobile unit, a pharmacy): {int(named_out.sum()):,}")
    for t, n in p.loc[named_out, ["typ", "business_name"]].itertuples(index=False):
        print(f"      {t:<16} {n}")
    p = filter_to_storefront(p, config.TAXONOMY_SYSTEM)
    print(f"  {len(p):,} storefront premises after filter_to_storefront()")

    p["latitude"] = pd.to_numeric(p["lat"], errors="coerce")
    p["longitude"] = pd.to_numeric(p["lon"], errors="coerce")
    no_point = p["latitude"].isna() | p["longitude"].isna()
    print(f"  {int(no_point.sum()):,} without a position, NOT placed")
    p = p[~no_point].copy()

    # Control: lat/lon against the register's own SWEREF 99 12 00 (y north, x east).
    n = pd.to_numeric(p["y_sweref991200"], errors="coerce")
    e = pd.to_numeric(p["x_sweref991200"], errors="coerce")
    both = n.notna() & e.notna()
    ax, ay = Transformer.from_crs(config.REGISTER_POSITION_CRS, config.CRS_PROJECTED,
                                  always_xy=True).transform(e[both].values, n[both].values)
    bx, by = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED,
                                  always_xy=True).transform(p["longitude"][both].values,
                                                            p["latitude"][both].values)
    d = ((pd.Series(ax) - pd.Series(bx)) ** 2 + (pd.Series(ay) - pd.Series(by)) ** 2) ** 0.5
    print(f"  lat/lon vs SWEREF 99 12 00, {int(both.sum()):,} premises: median {d.median():.2f} m, "
          f"max {d.max():.1f} m, over 10 m {int((d > 10).sum())}")
    if d.median() > 5:
        sys.exit("  the two positions disagree - an axis or CRS error upstream")

    # The fallback point: no correct address, so placed at the Environment
    # Administration's own address point (config). Centred on the AMBULERANDE
    # rows of the WHOLE register, measured in SWEREF 99 12 00 metres.
    rx = pd.to_numeric(df["x_sweref991200"], errors="coerce")
    ry = pd.to_numeric(df["y_sweref991200"], errors="coerce")
    amb = df["adress"].str.upper().str.strip().str.startswith(config.FALLBACK_ADDRESS_PREFIX)
    if amb.sum() < config.FALLBACK_MIN_ROWS:
        sys.exit(f"  only {int(amb.sum())} AMBULERANDE rows - the fallback point cannot be "
                 f"located; re-read the register")
    cx, cy = rx[amb].median(), ry[amb].median()
    spread = ((rx[amb] - cx) ** 2 + (ry[amb] - cy) ** 2) ** 0.5
    if spread.quantile(0.9) > config.FALLBACK_RADIUS_M:
        sys.exit(f"  the AMBULERANDE rows no longer share one point (90th percentile "
                 f"{spread.quantile(0.9):.0f} m) - re-read how the register places them")
    r = ((e - cx) ** 2 + (n - cy) ** 2) ** 0.5
    at_fallback = r < config.FALLBACK_RADIUS_M
    print(f"  at the fallback point ({cx:.0f} E, {cy:.0f} N, SWEREF 99 12 00; within "
          f"{config.FALLBACK_RADIUS_M:.0f} m), NOT placed: {int(at_fallback.sum())} "
          f"({at_fallback.mean():.1%})")
    p = p[~at_fallback]
    home = p["adress"].str.contains(config.HOME_ADDRESS, regex=True)
    print(f"  at an apartment (a home), left off: {int(home.sum())}")
    p = p[~home]

    box = config.GOTEBORG_BBOX
    in_box = p["latitude"].between(box["lat_min"], box["lat_max"]) & \
        p["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    p = p[in_box]
    city = gpd.GeoSeries([goteborg_geometry()], crs=config.CRS_GEOGRAPHIC
                         ).to_crs(config.CRS_PROJECTED).iloc[0]
    pts = gpd.GeoSeries(gpd.points_from_xy(p["longitude"], p["latitude"]), index=p.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(city)
    print(f"  {int((~inside).sum()):,} outside Göteborgs Stad, dropped")
    p = p[inside]

    # A premises named only as a person shows its address (config.PERSON_NAMED).
    p = p.copy()
    person = p["business_name"].isin(config.PERSON_NAMED)
    gone = set(config.PERSON_NAMED) - set(p.loc[person, "business_name"])
    if gone:
        sys.exit(f"PERSON_NAMED names no longer shown: {sorted(gone)} - re-read the list")
    if (person & p["name_classified"]).any():
        sys.exit("a PERSON_NAMED premises is classified by its name - its bucket would be "
                 "lost with the name; decide it by hand")
    before = [TAX.classify({TAX.VALUE_COLUMN: v, "business_name": n, "name_classified": c})
              for v, n, c in zip(p[TAX.VALUE_COLUMN], p["business_name"], p["name_classified"])]
    p["name_is_address"] = person
    p["business_name"] = p["business_name"].where(~person, p["adress"].str.strip().str.title())
    after = [TAX.classify({TAX.VALUE_COLUMN: v, "business_name": n, "name_classified": c})
             for v, n, c in zip(p[TAX.VALUE_COLUMN], p["business_name"], p["name_classified"])]
    if before != after:
        sys.exit("showing an address in place of a name changed a premises' bucket")
    print(f"  named only as a person (config.PERSON_NAMED): {int(person.sum())} show the address")

    out = p[["business_name", "latitude", "longitude", TAX.VALUE_COLUMN, "name_classified",
             "typ", "adress", "name_is_address"]].sort_values(["business_name", "latitude"])
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    bucket = pd.Series([TAX.classify({TAX.VALUE_COLUMN: v, "business_name": nm,
                                      "name_classified": c})
                        for v, nm, c in zip(out[TAX.VALUE_COLUMN], out["business_name"],
                                            out["name_classified"])])
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)} "
          f"({int(out['name_classified'].sum()):,} classified from the name)")
    print("    " + ", ".join(f"{TAX.legend_label(b)} {k:,}" for b, k in bucket.value_counts().items()))
    emit("register_rows", len(df))
    emit("storefronts", len(out))
    emit("name_classified", int(out["name_classified"].sum()))
    emit("name_as_address", int(out["name_is_address"].sum()))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
