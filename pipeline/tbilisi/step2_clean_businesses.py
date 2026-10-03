"""Tbilisi step 2: Geostat's active entities with a factual address in the city,
reduced to storefronts at a real coordinate.

    python pipeline/tbilisi/step2_clean_businesses.py

Reads the cache and NEVER fetches (`fetch_sources.py` downloads).

In order:
  1. The personal columns are absent (they were dropped at fetch), and no
     individual entrepreneur's row carries a name.
  2. Every code in the tracked divisions is decided by the taxonomy
     (`georgia_nace.unlisted`), then the taxonomy keeps the storefronts.
  3. Placement: a row with no coordinate is dropped and counted; a row on a
     placeholder point (config.PLACEHOLDER_POINTS, re-derived here from the
     rule and compared) is dropped and counted; a coordinate outside the
     city boundary is dropped and counted.
  4. The name: a company's registered name, in Georgian; an individual
     entrepreneur's pin shows the category only (owner, 2026-10-01).
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.tbilisi import config  # noqa: E402

OUT_COLUMNS = ["stat_id", "business_name", "activity_label", "activity_code",
               "legal_form", "district", "latitude", "longitude"]


def point_key(lat, lon):
    return (round(lat, config.PLACEHOLDER_DECIMALS), round(lon, config.PLACEHOLDER_DECIMALS))


def placeholder_points(df):
    """Candidate placeholders: points carrying PLACEHOLDER_MIN_ROWS+ active
    rows whose commonest legal-entity factual address is not a street
    address (a bare name, or blank) and is shared by at least
    PLACEHOLDER_MIN_COMPANIES companies. Whether a bare name is a district or
    settlement is read by a person (config: PLACEHOLDER_POINTS or
    NOT_PLACEHOLDERS). Returns {point: (rows, companies sharing, name)}."""
    located = df[df["_key"].notna()]
    sizes = located.groupby("_key").size()
    big = sizes[sizes >= config.PLACEHOLDER_MIN_ROWS].index
    companies = located[(located["_key"].isin(big)) & ~located["_person"]]
    found = {}
    for key, grp in companies.groupby("_key"):
        top = grp["factual_address_key"].fillna("").value_counts()
        if top.empty:
            continue
        # A value starting "#" is a street address, kept only as a hash.
        name, n = top.index[0], int(top.iloc[0])
        if not name.startswith("#") and n >= config.PLACEHOLDER_MIN_COMPANIES:
            found[key] = (int(sizes[key]), n, name or "(blank)")
    return found


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    for path in (config.BUSINESSES_RAW_CSV, config.CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"missing {path}\nRun: python pipeline/tbilisi/fetch_sources.py, "
                     f"then step 1")
    taxonomy = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    df = pd.read_csv(config.BUSINESSES_RAW_CSV, dtype=str, keep_default_na=False)
    print(f"  register: {len(df):,} active entities, factual address in Tbilisi")
    emit("register_rows", len(df))

    # --- 1. Personal columns ---------------------------------------------
    leaked = sorted(set(config.PERSONAL_COLUMNS) & set(df.columns))
    if leaked:
        sys.exit(f"personal columns in the cache: {leaked}. Re-fetch; never read them")
    df["_person"] = df["Legal_Form_ID"] == config.INDIVIDUAL_ENTREPRENEUR_FORM
    if (df.loc[df["_person"], "Full_Name"] != "").any():
        sys.exit("an individual entrepreneur's row carries a name: the fetch must blank it")
    if (df["Region_Code2"] != "11").any():
        sys.exit("a row whose factual region is not 11")

    # --- 2. Classification -----------------------------------------------
    new = taxonomy.unlisted(df["Activity_2_Code"])
    if new:
        sys.exit(f"codes in the tracked divisions the taxonomy has not decided: {new}")
    df["activity_code"] = df["Activity_2_Code"].str.strip()
    df["activity_label"] = df["Activity_2_Name"].str.strip()

    # Placeholder points are derived on EVERY active row with a coordinate.
    lat = pd.to_numeric(df[config.LAT_COLUMN], errors="coerce")
    lon = pd.to_numeric(df[config.LON_COLUMN], errors="coerce")
    df["latitude"], df["longitude"] = lat, lon
    has = lat.notna() & lon.notna() & (lat != 0) & (lon != 0)
    df["_key"] = [point_key(a, b) if h else None for a, b, h in zip(lat, lon, has)]
    if "factual_address_key" not in df.columns:
        sys.exit("the register cache has no factual_address_key: re-pull with "
                 "python pipeline/tbilisi/fetch_sources.py --only register --force")
    found = placeholder_points(df)
    print(f"\n  placeholder candidates ({config.PLACEHOLDER_MIN_ROWS}+ rows; commonest company "
          f"address a bare name or blank, shared by {config.PLACEHOLDER_MIN_COMPANIES}+ companies):")
    for key, (n, shared, name) in sorted(found.items(), key=lambda kv: -kv[1][0]):
        print(f"    {key[0]:.6f}, {key[1]:.6f}  {n:>5} rows  {shared:>4} companies  {name}")
    expected = {point_key(*k) for k in config.PLACEHOLDER_POINTS}
    rejected = {point_key(*k) for k in config.NOT_PLACEHOLDERS}
    unread = sorted(set(found) - expected - rejected)
    by_reading = {point_key(*k) for k in config.PLACEHOLDERS_BY_READING}
    gone = sorted(expected - set(found) - by_reading)
    if unread or gone:
        sys.exit(f"placeholder candidates not yet read: {unread}; listed points no longer "
                 f"candidates: {gone}. Read each name: a district or settlement goes in "
                 f"config.PLACEHOLDER_POINTS, a street or real place in NOT_PLACEHOLDERS")
    emit("placeholder_points", len(expected))

    kept = filter_to_storefront(df, config.TAXONOMY_SYSTEM).copy()
    kept["bucket"] = [taxonomy.classify({"activity_code": c}) for c in kept["activity_code"]]
    print(f"\n  storefronts by the taxonomy: {len(kept):,}")
    print(kept["bucket"].value_counts().to_string())
    for b, n in kept["bucket"].value_counts().items():
        emit(f"storefronts_{b.lower().replace(' ', '_')}", int(n))
    emit("division_45_kept", int(kept["activity_code"].str.startswith("45").sum()))

    # --- 3. Placement ----------------------------------------------------
    no_coord = kept["_key"].isna()
    on_placeholder = kept["_key"].isin(expected)
    b = config.TBILISI_BBOX
    in_box = (kept["latitude"].between(b["lat_min"], b["lat_max"])
              & kept["longitude"].between(b["lon_min"], b["lon_max"]))
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    city = city.geometry.union_all()
    cand = kept[~no_coord & ~on_placeholder & in_box]
    inside = gpd.GeoSeries(gpd.points_from_xy(cand["longitude"], cand["latitude"]),
                           index=cand.index, crs=config.CRS_GEOGRAPHIC).within(city)
    outside = ~no_coord & ~on_placeholder & ~kept.index.isin(inside[inside].index)
    near_station = kept[on_placeholder].groupby("_key").size()
    print(f"\n  no coordinate:        {int(no_coord.sum()):>6,}")
    print(f"  on a placeholder:     {int(on_placeholder.sum()):>6,}")
    print(f"  outside the city:     {int(outside.sum()):>6,}")
    print(f"  placed:               {int(inside.sum()):>6,} "
          f"({inside.sum() / len(kept):.1%} of storefronts)")
    emit("dropped_no_coordinate", int(no_coord.sum()))
    emit("dropped_placeholder", int(on_placeholder.sum()))
    emit("dropped_outside_city", int(outside.sum()))
    for key, n in near_station.sort_values(ascending=False).items():
        print(f"    placeholder {key[0]:.6f}, {key[1]:.6f}: {n} storefronts "
              f"({config.PLACEHOLDER_POINTS.get(key, '?')})")
    placed = kept.loc[inside[inside].index].copy()

    # --- 4. Names ----------------------------------------------------------
    named = ~placed["_person"] & (placed["Full_Name"].str.strip() != "")
    placed["business_name"] = placed["Full_Name"].str.strip().where(named,
                                                                    placed["activity_label"])
    print(f"\n  named (companies): {int(named.sum()):,}; category only (individual "
          f"entrepreneurs, or no name): {int((~named).sum()):,}")
    emit("named_companies", int(named.sum()))
    emit("category_only", int((~named).sum()))
    emit("individual_entrepreneurs", int(placed["_person"].sum()))

    out = placed.rename(columns={"Stat_ID": "stat_id", "Legal_Form": "legal_form",
                                 "City_name2": "district"})[OUT_COLUMNS]
    out = out.sort_values("stat_id")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    emit("storefronts_placed", len(out))


if __name__ == "__main__":
    main()
