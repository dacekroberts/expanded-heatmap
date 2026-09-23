"""Dublin step 2: the rateable valuation register -> storefront premises.

Reads the cache fetch_sources.py wrote and NEVER fetches.

    python pipeline/dublin/step2_clean_businesses.py

Three things are unusual here and all three are deliberate:

  1. THE COORDINATES NEED NO GEOCODING AND NO REPROJECTION. `Xitm`/`Yitm` are
     already EPSG:2157 in metres on 99.87% of rows, which is the CRS this city
     measures in, so the only transform is 2157 -> 4326 for display.
  2. THERE IS NO BUSINESS NAME IN THE SOURCE. `business_name` is the street
     address. See config.NAME_COLUMN for why that is a structural privacy
     result rather than a filter.
  3. `Eircode` IS DROPPED AT LOAD, before anything can persist it.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.dublin import config
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module


def load_raw():
    if not config.BUSINESSES_RAW_JSON.exists():
        sys.exit(f"missing {config.BUSINESSES_RAW_JSON}.\n"
                 f"Run: python pipeline/dublin/fetch_sources.py")
    rows = json.loads(config.BUSINESSES_RAW_JSON.read_text(encoding="utf-8"))
    df = pd.DataFrame(rows)
    print(f"Raw register: {len(df):,} rows, {len(df.columns)} columns")

    # DROPPED AT LOAD, not filtered later, so no processed file can carry it.
    dropped = [c for c in config.DROP_COLUMNS if c in df.columns]
    if dropped:
        df = df.drop(columns=dropped)
        print(f"  dropped at load: {dropped} "
              f"(third-party database right - see DECISIONS.md)")

    # THE SOURCE HAS NO NAME COLUMN OF ANY KIND. Asserted rather than assumed,
    # so a future refresh that adds one fails loudly instead of quietly
    # publishing people. This is the structural form of the check New York can
    # only make by excluding a column it knows is there.
    namelike = [c for c in df.columns if any(
        t in c.lower() for t in ("name", "occupier", "tenant", "owner",
                                 "ratepayer", "proprietor", "person",
                                 "contact"))]
    if namelike:
        sys.exit(f"  THE REGISTER NOW CARRIES {namelike}. Dublin's privacy "
                 f"position is that no such column exists, so this build must "
                 f"not proceed until that is re-decided. See DECISIONS.md, "
                 f"2026-09-22.")
    print("  no name/occupier/owner column present (asserted)")

    for authority, n in df["LocalAuthority"].value_counts().items():
        print(f"    {authority:32s} {n:7,}")
    return df


def report_unknown_segments(df):
    """Segments that are neither classified nor deliberately excluded.

    The taxonomy maps 318 segments measured on 2026-09-22. A register refresh
    can introduce a new one, and an unmapped segment is silently non-storefront
    - it would simply vanish from the map. This is what makes that visible.
    """
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    unknown = {}
    for value in df[tax.VALUE_COLUMN]:
        for seg in tax._segments(value):
            if not tax.is_known(seg):
                unknown[seg] = unknown.get(seg, 0) + 1
    if unknown:
        print(f"\n  {len(unknown)} UNMAPPED `Uses` segment(s) - neither "
              f"classified nor listed as non-storefront:")
        for seg, n in sorted(unknown.items(), key=lambda kv: -kv[1])[:20]:
            print(f"    {seg[:52]:54s} {n:6,}")
        print("  Each is being treated as non-storefront. Map it in "
              "pipeline/taxonomies/dublin_uses.py or add it to the excluded "
              "list, so the two cases stop looking identical.")
    else:
        print("\n  every `Uses` segment is either classified or explicitly "
              "excluded")


def main():
    df = load_raw()
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)

    # The raw column is already the taxonomy's VALUE_COLUMN, so the rename
    # every other city does is a no-op here.
    assert config.RAW_CLASSIFICATION_COLUMN == tax.VALUE_COLUMN

    report_unknown_segments(df)

    n0 = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"\nStorefront filter: {n0:,} -> {len(df):,}")
    print(df.assign(_b=[tax.classify(r) for r in df.to_dict("records")])
            ["_b"].value_counts().to_string())

    n1 = len(df)
    pattern = "|".join(config.EXCLUDE_USES_CONTAINING)
    df = df[~df[tax.VALUE_COLUMN].str.upper().str.contains(pattern, na=False)]
    print(f"\nNot-a-trading-storefront filter "
          f"({', '.join(config.EXCLUDE_USES_CONTAINING)}): "
          f"{n1:,} -> {len(df):,}")

    n2 = len(df)
    df = df[df["Xitm"].notna() & df["Yitm"].notna()
            & (df["Xitm"] != 0) & (df["Yitm"] != 0)]
    print(f"\nCoordinates present: {n2:,} -> {len(df):,} "
          f"({n2 - len(df)} dropped)")

    # ITM -> WGS84. The ONLY transform in this build: both sources are already
    # in EPSG:2157, so nothing is projected to do the geometry, only to draw.
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["Xitm"], df["Yitm"]),
        crs=config.CRS_PROJECTED)
    wgs = gdf.to_crs(config.CRS_GEOGRAPHIC)
    gdf["longitude"] = wgs.geometry.x
    gdf["latitude"] = wgs.geometry.y

    n3 = len(gdf)
    b = config.DUBLIN_BBOX
    gdf = gdf[gdf["latitude"].between(b["lat_min"], b["lat_max"])
              & gdf["longitude"].between(b["lon_min"], b["lon_max"])]
    print(f"Bounds check: {n3:,} -> {len(gdf):,} ({n3 - len(gdf)} outside)")

    # Confirm against the real boundary, not just the box. This is the check
    # that would catch a register row filed to the wrong authority.
    boundary = json.loads(config.BOUNDARY_GEOJSON.read_text(encoding="utf-8"))
    region = gpd.GeoDataFrame(
        [{"authority": f["properties"][config.BOUNDARY_NAME_FIELD],
          "geometry": shape(f["geometry"])} for f in boundary["features"]],
        crs=config.CRS_GEOGRAPHIC).dissolve(by="authority").reset_index()

    n4 = len(gdf)
    joined = gpd.sjoin(gdf.to_crs(config.CRS_GEOGRAPHIC),
                       region[["authority", "geometry"]],
                       how="left", predicate="within")
    joined = joined[~joined.index.duplicated(keep="first")]
    outside = joined["authority"].isna().sum()
    if outside:
        print(f"In the dissolved boundary: {n4:,} -> {n4 - outside:,} "
              f"({outside} outside every authority polygon)")
    joined = joined[joined["authority"].notna()]

    n5 = len(joined)
    joined = joined.drop_duplicates(subset=["PropertyNumber"])
    print(f"Deduplicate on PropertyNumber: {n5:,} -> {len(joined):,}")

    out = pd.DataFrame({
        "business_name": joined[config.NAME_COLUMN].fillna("").astype(str),
        "latitude": joined["latitude"],
        "longitude": joined["longitude"],
        tax.VALUE_COLUMN: joined[tax.VALUE_COLUMN],
        "Category": joined["Category"],
        "authority": joined["authority"],
    })
    out = out[out["business_name"].str.strip() != ""]
    out = out.sort_values(["business_name", "latitude"]).reset_index(drop=True)

    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\nwrote {config.BUSINESSES_CLEAN_CSV.name}  {len(out):,} rows")
    print("\nBy authority:")
    print(out["authority"].value_counts().to_string())
    buckets = pd.Series([tax.classify(r) for r in joined.to_dict("records")])
    print("\nBy bucket:")
    print(buckets.value_counts().to_string())

    emit("register_rows", n0)
    emit("storefront_rows", len(out))
    emit("retail", int((buckets == "Retail").sum()))
    emit("food_service", int((buckets == "Food service").sum()))
    emit("personal_services", int((buckets == "Personal services").sum()))


if __name__ == "__main__":
    main()
