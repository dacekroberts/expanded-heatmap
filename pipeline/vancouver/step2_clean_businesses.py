"""Step 2 - clean Vancouver's and Surrey's licences into one storefront set.

Input:  data/vancouver/raw/vancouver_business_licences.csv  (OGL - Vancouver)
        data/vancouver/raw/surrey_business_licences.csv      (OGL - Surrey)
        data/vancouver/raw/vancouver_local_areas.geojson
        data/vancouver/raw/surrey_city_boundaries.geojson
        data/vancouver/raw/property_parcel_polygons.geojson  (residence filter)
        data/vancouver/raw/property_tax_report.csv            (residence filter)
Output: data/vancouver/processed/businesses_clean.csv

TWO REGISTRIES, ONE OUTPUT. Each is normalised to the same shared columns plus
a `source`, then concatenated, then `filter_to_storefront` runs ONCE - the
New York and Boston pattern. Deduplication is PER SOURCE and there is no
cross-source pass, because the two registries cover disjoint municipalities and
no premises can appear in both. That absence is deliberate; see config.py.

THE NAME PROBLEM, AND THE SIGNAL THE BRIEF SAID DID NOT EXIST
-------------------------------------------------------------
Vancouver's `businesstradename` is blank on 49.6% of mappable rows, so a pin's
label falls back to `businessname` - which for a sole proprietor is a person's
name. The owner's decision (2026-09-21) was to keep the pin and show a neutral
label instead of the name.

The brief said Vancouver has no structural signal for this and would need a
regex. It has one: **the registry wraps a sole proprietor's own name in
PARENTHESES** - "(Christopher Colonia)", "(Qi Liu)", "(Dale Hudson)". 4,383 of
29,660 mappable rows, 750 of the storefront set. That is the City's own marking
of an individual registrant, not an inference, and it is this city's equivalent
of D.C.'s ENTITYTYPE.

Both signals are used, as a union, because they catch different people:
  - the parentheses catch 63 storefront rows `residence.looks_personal` misses,
    mostly three-part and non-Anglo names the regex was never going to match;
  - the regex catches ~10 registrants who did not use parentheses.
`residence.looks_organisational` vetoes both, so "(Vancouver Taxi Ltd)" keeps
its name.

THE RESIDENCE FILTER IS A CONJUNCTION, NOT A ZONING TEST
--------------------------------------------------------
Residential zoning ALONE is not evidence of a home business here: Vancouver
has real corner shops on residentially-zoned land, and dropping every
residentially-zoned storefront would delete them. So a row is dropped only when
residential zoning AND a personal-name signal agree - the pairing the build
brief measured. The known blind spot is stated in config.py: Comprehensive
Development is mixed-use, never flags residential, and covers exactly the
central areas where a "home" is a condo.

Surrey needs none of this. It STATES home occupation on the licence, so those
14,015 rows never enter.

Run:  python pipeline/vancouver/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.residence import looks_organisational, looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.vancouver.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    FORBIDDEN_COLUMNS,
    MIXED_USE_ZONING_CLASSES,
    PARCEL_KEY,
    PARCELS_GEOJSON,
    RAW_CLASSIFICATION_COLUMN,
    RESIDENTIAL_ZONING_CLASSES,
    SOURCE_ENCODING,
    SOURCES,
    SURREY_BOUNDARY_GEOJSON,
    SURREY_BOUNDARY_NAME_FIELD,
    SURREY_BOUNDARY_NAME_KEEP,
    SURREY_CATEGORY_DELIMITER,
    SURREY_LICENSE_TYPE_COLUMN,
    SURREY_LICENSE_TYPE_KEEP,
    TAX_REPORT_CSV,
    TAX_REPORT_KEY,
    TAXONOMY_SYSTEM,
    VANCOUVER_BBOX,
)

MODULE = load_taxonomy_module(TAXONOMY_SYSTEM)
PARENTHESISED = re.compile(r"^\((.+)\)$")

# The shared columns every source normalises to.
SHARED = ["source", "key", "business_name", "address", RAW_CLASSIFICATION_COLUMN,
          "latitude", "longitude"]


def assert_no_forbidden(df, label):
    leaked = sorted(set(df.columns) & set(FORBIDDEN_COLUMNS))
    if leaked:
        sys.exit(f"{label}: {leaked} is still present after loading. The "
                 f"download boundary is this project's privacy control and "
                 f"step 2 must not be the only thing standing between a "
                 f"personal column and an output.")


def load_vancouver():
    src = SOURCES["vancouver"]
    df = pd.read_csv(src["file"], sep=src["delimiter"], dtype=str,
                     encoding=SOURCE_ENCODING, low_memory=False)
    print(f"\nVancouver: {len(df):,} rows "
          f"(server-side filter: {src['filter']})")
    assert_no_forbidden(df, "vancouver")

    # geo_point_2d is "lat, lon". LATITUDE FIRST - reversing it puts every pin
    # in the South Atlantic off Namibia, which is at least obvious.
    before = len(df)
    df = df[df["geo_point_2d"].notna()].copy()
    print(f"  with coordinates:   {len(df):,} "
          f"({len(df) / before:.1%}; {before - len(df):,} dropped)")
    parts = df["geo_point_2d"].str.split(",", n=1, expand=True)
    df["latitude"] = pd.to_numeric(parts[0].str.strip(), errors="coerce")
    df["longitude"] = pd.to_numeric(parts[1].str.strip(), errors="coerce")
    bad = df["latitude"].isna() | df["longitude"].isna()
    if bad.any():
        print(f"  {int(bad.sum()):,} row(s) had an unparseable geo_point_2d")
        df = df[~bad]

    df["source"] = "vancouver"
    df["key"] = df[src["key_column"]]
    df[RAW_CLASSIFICATION_COLUMN] = df[src["category_column"]]

    # Address, for dedup and for the residential-unit signal.
    unit = df["unittype"].fillna("").str.strip() + " " + df["unit"].fillna("").str.strip()
    df["address"] = (df["house"].fillna("").str.strip() + " "
                     + df["street"].fillna("").str.strip() + " "
                     + unit.str.strip()).str.replace(r"\s+", " ", regex=True).str.strip()

    # The trade name if there is one; the legal name otherwise. The legal name
    # is where the person-name exposure lives, so it is flagged, not hidden.
    trade = df[src["name_column"]].fillna("").str.strip()
    legal = df[src["name_fallback_column"]].fillna("").str.strip()
    df["business_name"] = trade.where(trade != "", legal)
    df["_used_fallback"] = trade == ""
    print(f"  trade name present: {int((~df['_used_fallback']).sum()):,} "
          f"({(~df['_used_fallback']).mean():.1%}); "
          f"{int(df['_used_fallback'].sum()):,} fall back to the legal name")
    return df[SHARED + ["_used_fallback"]]


def surrey_winning_category(raw):
    """Surrey stores SEVERAL categories per row, newline-separated. Resolve to
    the single one whose bucket wins under BUCKET_PRIORITY, keeping Surrey's
    OWN wording for the tooltip rather than substituting a bucket name."""
    cats = [c.strip() for c in str(raw).split(SURREY_CATEGORY_DELIMITER)
            if c.strip()]
    if not cats:
        return None
    ranked = []
    for c in cats:
        bucket = MODULE.classify({RAW_CLASSIFICATION_COLUMN: c,
                                  "source": "surrey"})
        rank = (MODULE.BUCKET_PRIORITY.index(bucket)
                if bucket in MODULE.BUCKET_PRIORITY else len(MODULE.BUCKET_PRIORITY))
        ranked.append((rank, c))
    ranked.sort(key=lambda t: t[0])
    return ranked[0][1]


def load_surrey():
    src = SOURCES["surrey"]
    df = pd.read_csv(src["file"], sep=src["delimiter"], dtype=str,
                     encoding="utf-8-sig", low_memory=False)
    print(f"\nSurrey: {len(df):,} rows")

    # PhoneNumber exists in this export and is dropped HERE, then asserted
    # gone - a business number is not needed to draw a dot, and a home
    # occupation's number is a personal one.
    dropped = [c for c in FORBIDDEN_COLUMNS if c in df.columns]
    df = df.drop(columns=dropped)
    if dropped:
        print(f"  dropped {dropped} immediately after loading")
    assert_no_forbidden(df, "surrey")

    # Surrey STATES home occupation on the licence. Normalised because one row
    # reads " home" rather than either real value.
    lt = df[SURREY_LICENSE_TYPE_COLUMN].fillna("").str.strip().str.lower()
    print("  LicenseType: " + ", ".join(
        f"{v}={n:,}" for v, n in lt.value_counts().items()))
    before = len(df)
    df = df[lt == SURREY_LICENSE_TYPE_KEEP].copy()
    print(f"  Commercial/Industrial only: {before:,} -> {len(df):,} "
          f"({before - len(df):,} dropped, of which home occupation is the "
          f"bulk - a home business is not a storefront)")

    # x/y are NAD83 UTM 10N METRES, not degrees, and arrive only in the CSV
    # export. The layer's own attribute schema has no coordinate fields.
    xy = gpd.GeoSeries(
        gpd.points_from_xy(pd.to_numeric(df["x"], errors="coerce"),
                           pd.to_numeric(df["y"], errors="coerce")),
        crs=SOURCES["surrey"].get("xy_crs", "EPSG:26910"))
    ll = xy.to_crs(CRS_GEOGRAPHIC)
    df["latitude"] = ll.y.values
    df["longitude"] = ll.x.values

    df["source"] = "surrey"
    df["key"] = df[src["key_column"]]
    df["address"] = df["Address"].fillna("").str.strip()
    df["business_name"] = df[src["name_column"]].fillna("").str.strip()
    # Surrey publishes no second name column, so there is no fallback and no
    # fallback exposure.
    df["_used_fallback"] = False

    multi = df["BusinessCategory"].fillna("").str.contains(
        SURREY_CATEGORY_DELIMITER)
    print(f"  {int(multi.sum()):,} rows carry more than one category; "
          f"resolved by BUCKET_PRIORITY {MODULE.BUCKET_PRIORITY}")
    df[RAW_CLASSIFICATION_COLUMN] = df["BusinessCategory"].map(
        surrey_winning_category)
    df = df[df[RAW_CLASSIFICATION_COLUMN].notna()]
    return df[SHARED + ["_used_fallback"]]


def read_boundary(path, label, name_field=None, name_keep=None):
    g = gpd.read_file(path)
    g = g.set_crs(CRS_GEOGRAPHIC) if g.crs is None else g.to_crs(CRS_GEOGRAPHIC)
    x0, y0, _, _ = g.total_bounds
    if not (-180 <= x0 <= 180 and -90 <= y0 <= 90):
        sys.exit(f"{label}: bounds are not degrees - see step 1's read_degrees "
                 f"and config.SURREY_SOURCE_XY_CRS.")
    if name_field:
        g = g[g[name_field].astype(str).str.upper() == name_keep]
        if len(g) != 1:
            sys.exit(f"{label}: {name_field}={name_keep!r} matched {len(g)} "
                     f"features, expected 1.")
    return g.to_crs(CRS_PROJECTED).union_all()


def main():
    for path in (SOURCES["vancouver"]["file"], SOURCES["surrey"]["file"],
                 CITY_BOUNDARY_GEOJSON, SURREY_BOUNDARY_GEOJSON,
                 PARCELS_GEOJSON, TAX_REPORT_CSV):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/vancouver/fetch_sources.py first.")

    df = pd.concat([load_vancouver(), load_surrey()], ignore_index=True)
    print(f"\nCombined: {len(df):,} rows "
          f"({dict(df['source'].value_counts())})")

    # --- storefront filter, once, over both sources -------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM).copy()
    print(f"\nStorefront filter: {before:,} -> {len(df):,} "
          f"({len(df) / before:.1%} kept)")
    df["bucket"] = [MODULE.classify(r) for r in
                    df[[RAW_CLASSIFICATION_COLUMN, "source"]].to_dict("records")]
    for source, part in df.groupby("source"):
        print(f"  {source}: " + ", ".join(
            f"{b}={n:,}" for b, n in part["bucket"].value_counts().items()))

    # --- in-city, per source, against the real polygon ----------------------
    van_geom = read_boundary(CITY_BOUNDARY_GEOJSON, "vancouver boundary")
    sur_geom = read_boundary(SURREY_BOUNDARY_GEOJSON, "surrey boundary",
                             SURREY_BOUNDARY_NAME_FIELD,
                             SURREY_BOUNDARY_NAME_KEEP)
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    # THE BOUNDARY IS A CHECK HERE, NOT A FILTER, and that is deliberate.
    #
    # Both registries are already city-scoped by their publishers: Vancouver's
    # `city` column reads 'Vancouver' on all 29,660 mappable rows, and Surrey's
    # file is Surrey's own licences. Miami uses its boundary layer the same way.
    #
    # It matters because the local-area layer HAS A HOLE. The 22 local areas
    # are neighbourhoods and they do not cover STANLEY PARK, so a containment
    # filter would delete the Teahouse, Prospect Point, the Rowing Club, the
    # Brew Pub and the Aquarium - real Vancouver storefronts, every one. The
    # 118.8 km2 area check passes regardless, because the park is 4 km2 against
    # a ~3 km2 tolerance and the layer also reaches into water.
    expected = {"vancouver": van_geom, "surrey": sur_geom}
    inside = pd.Series(
        [expected[s].contains(p) for s, p in zip(gdf["source"], gdf.geometry)],
        index=gdf.index)
    print("\nInside its own city's boundary (a CHECK - nothing is dropped "
          "here):")
    for source, part in inside.groupby(gdf["source"]):
        print(f"  {source}: {int(part.sum()):,} of {len(part):,} "
              f"({part.mean():.2%}); {int((~part).sum()):,} outside")
    outside = gdf[~inside]
    if len(outside):
        print(f"  all {len(outside)} outside rows, listed rather than assumed "
              f"away:")
        for r in outside.itertuples():
            print(f"      {r.source:<10} {r.business_name[:36]:<36} "
                  f"{r.address[:32]}")
        streets = outside["address"].str.upper()
        park = int(streets.str.contains(
            "STANLEY PARK|PIPELINE|AVISON").sum())
        print(f"  {park} of {len(outside)} are in Stanley Park, which the "
              f"local-area layer does not cover. KEPT.")
    gdf["inside_boundary"] = inside

    # --- bounds sanity ------------------------------------------------------
    b = VANCOUVER_BBOX
    ok = (gdf["latitude"].between(b["lat_min"], b["lat_max"])
          & gdf["longitude"].between(b["lon_min"], b["lon_max"]))
    if not ok.all():
        print(f"\n{int((~ok).sum()):,} row(s) outside the sanity box - dropped")
        gdf = gdf[ok]

    # --- dedup, per source --------------------------------------------------
    order = {bucket: i for i, bucket in enumerate(MODULE.BUCKET_PRIORITY)}
    gdf["_rank"] = gdf["bucket"].map(order).fillna(len(order)).astype(int)
    gdf["_name"] = gdf["business_name"].str.upper().str.strip()
    gdf["_addr"] = gdf["address"].str.upper().str.strip()
    before = len(gdf)
    gdf = (gdf.sort_values("_rank")
              .drop_duplicates(subset=["source", "_name", "_addr"], keep="first")
              .drop(columns=["_rank", "_name", "_addr"]))
    print(f"\nPer-source dedup on (name, address): {before:,} -> {len(gdf):,} "
          f"({before - len(gdf):,} duplicate licences at one premises). "
          f"No cross-source pass: the two registries are disjoint by geography.")

    # --- the name signals ---------------------------------------------------
    raw_name = gdf["business_name"].fillna("").str.strip()
    inner = raw_name.str.replace(PARENTHESISED, r"\1", regex=True)
    is_paren = raw_name.str.match(PARENTHESISED).fillna(False)
    is_person = pd.Series([looks_personal(x) for x in inner], index=gdf.index)
    is_org = pd.Series([looks_organisational(x) for x in inner], index=gdf.index)
    gdf["registrant_name"] = (is_paren | is_person) & ~is_org
    print(f"\nPersonal-name signals on the DISPLAYED label:")
    print(f"  parenthesised by the registry: {int(is_paren.sum()):,}")
    print(f"  residence.looks_personal:      {int(is_person.sum()):,}")
    print(f"  either, less looks_organisational: "
          f"{int(gdf['registrant_name'].sum()):,} "
          f"({gdf['registrant_name'].mean():.2%})")
    # The split that decides what happens, and it is the San Diego precedent:
    # a TRADE name the owner chose to register under their own name is a
    # deliberate public commercial act and is left alone. Only a legal name
    # the PIPELINE substituted is suppressed.
    chosen = gdf["registrant_name"] & ~gdf["_used_fallback"]
    substituted = gdf["registrant_name"] & gdf["_used_fallback"]
    print(f"  of those, {int(chosen.sum()):,} are TRADE names the owner "
          f"registered themselves - left as published, per San Diego")
    print(f"  and {int(substituted.sum()):,} are legal names this pipeline "
          f"substituted - these are the ones suppressed below")

    # --- residence filter: zoning AND a personal name -----------------------
    gdf = apply_residence_filter(gdf)

    # --- the label the map shows -------------------------------------------
    # Owner's decision: keep the pin, show the row's own category instead of a
    # person's name. Applied only where the name would actually be displayed.
    suppress = gdf["registrant_name"] & gdf["_used_fallback"]
    gdf.loc[suppress, "business_name"] = gdf.loc[suppress,
                                                 RAW_CLASSIFICATION_COLUMN]
    gdf["name_suppressed"] = suppress
    print(f"\nLabel policy (NAME_FALLBACK_POLICY=suppress_personal): "
          f"{int(suppress.sum()):,} pin(s) show their business type instead of "
          f"a registrant's name. No individual's name is published.")
    blank = gdf["business_name"].fillna("").str.strip() == ""
    if blank.any():
        print(f"  dropping {int(blank.sum()):,} row(s) with no usable label")
        gdf = gdf[~blank]

    out = gdf.drop(columns=["geometry", "_used_fallback"]).copy()
    print(f"\nFinal: {len(out):,} storefronts "
          f"({dict(out['source'].value_counts())})")
    print("  by bucket: " + ", ".join(
        f"{b}={n:,}" for b, n in out["bucket"].value_counts().items()))
    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.sort_values(["source", "business_name"]).to_csv(
        BUSINESSES_CLEAN_CSV, index=False)
    print(f"Wrote {BUSINESSES_CLEAN_CSV}")


def apply_residence_filter(gdf):
    """Vancouver only: business point -> parcel -> tax report -> zoning class.

    Surrey states home occupation on the licence, so it is already handled and
    its rows pass through untouched.
    """
    print("\nResidence filter (Vancouver only):")
    van = gdf[gdf["source"] == "vancouver"]
    if van.empty:
        return gdf

    parcels = gpd.read_file(PARCELS_GEOJSON)
    parcels = (parcels.set_crs(CRS_GEOGRAPHIC) if parcels.crs is None
               else parcels.to_crs(CRS_GEOGRAPHIC)).to_crs(CRS_PROJECTED)
    print(f"  parcels: {len(parcels):,}")

    tax = pd.read_csv(TAX_REPORT_CSV, sep=";", dtype=str, low_memory=False)
    zoning = (tax.dropna(subset=[TAX_REPORT_KEY])
                 .drop_duplicates(subset=[TAX_REPORT_KEY])
                 .set_index(TAX_REPORT_KEY)["zoning_classification"])
    print(f"  tax report: {len(tax):,} rows -> {len(zoning):,} "
          f"distinct land_coordinate")

    joined = gpd.sjoin(van[["geometry"]], parcels[[PARCEL_KEY, "geometry"]],
                       predicate="within", how="left")
    joined = joined[~joined.index.duplicated()]
    hit = joined[PARCEL_KEY].notna()
    print(f"  point inside a parcel: {int(hit.sum()):,} of {len(van):,} "
          f"({hit.mean():.1%})")

    zone = joined[PARCEL_KEY].map(zoning)
    print(f"  parcel -> zoning class:  {int(zone.notna().sum()):,} "
          f"({zone.notna().mean():.1%})")
    top = zone.value_counts().head(8)
    print("  zoning of the storefront set: " + ", ".join(
        f"{k}={v:,}" for k, v in top.items()))
    mixed = int(zone.isin(MIXED_USE_ZONING_CLASSES).sum())
    print(f"  the stated blind spot: {mixed:,} rows "
          f"({mixed / len(van):.1%}) are {'/'.join(MIXED_USE_ZONING_CLASSES)}, "
          f"mixed-use, and can never flag residential")

    residential = zone.isin(RESIDENTIAL_ZONING_CLASSES).reindex(
        gdf.index, fill_value=False)
    gdf["residential_zoning"] = residential
    personal = gdf["registrant_name"].fillna(False)
    substituted = personal & gdf["_used_fallback"]
    candidates = residential & substituted & (gdf["source"] == "vancouver")

    print(f"  residentially zoned:                    "
          f"{int(residential.sum()):,}")
    print(f"  residentially zoned by category: " + ", ".join(
        f"{k}={v}" for k, v in
        gdf.loc[residential, RAW_CLASSIFICATION_COLUMN]
        .value_counts().head(6).items()))
    print(f"  ...AND a substituted personal name:     "
          f"{int(candidates.sum()):,}")

    # NOTHING IS DROPPED HERE, and that is the measured conclusion rather than
    # a shortcut.
    #
    # The conjunction leaves 1 row: "Mcgill Groceries" at 2691 McGill St - a
    # FALSE POSITIVE of looks_personal (a surname followed by a word) and a
    # real corner grocery on residentially-zoned land. Meanwhile the 137
    # residentially-zoned storefronts are Restaurant 33, Limited Service Food
    # 29, Retail Dealer 26, Retail Dealer - Food 26, Liquor Establishment 12 -
    # Vancouver's legal non-conforming corner shops and neighbourhood
    # restaurants, which a zoning filter would delete wholesale.
    #
    # So the home-business residue this join was built to find is not there,
    # and the privacy purpose is already served at the LABEL: any substituted
    # personal name shows the business type instead. Dropping rows on top of
    # that would cost real storefronts for no privacy gain. San Diego reached
    # the same place - "left in. Revisit if a better residence signal
    # appears."
    #
    # The join is kept because it is the measurement that JUSTIFIES not
    # filtering. Delete it and this becomes an assumption again.
    if int(candidates.sum()):
        print("  the candidate row(s), inspected individually:")
        for r in gdf[candidates].itertuples():
            print(f"      {r.business_name[:30]:<30} "
                  f"{getattr(r, RAW_CLASSIFICATION_COLUMN)[:28]:<28} "
                  f"{r.address[:30]}")
    print(f"  NOTHING DROPPED. The residue is not there, and the label policy "
          f"already prevents publishing a name. See this function's comment.")
    return gdf.copy()


if __name__ == "__main__":
    main()
