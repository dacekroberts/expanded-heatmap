"""Step 2 - Ottawa's food premises from Ottawa Public Health's inspection feed.

Input:  data/ottawa/raw/yelp_ottawa_healthscores_FoodSafety.zip  (LIVES)
        data/ottawa/raw/wards_2022_2026.geojson                  (the City)
Output: data/ottawa/processed/businesses_clean.csv
        outputs/ottawa/excluded_premises.csv

What a reader should know before trusting the counts printed below:

  * **The feed has no status and no closing date.** A premises counts when
    OPH inspected it within config.CURRENCY_YEARS before config.AS_OF_DATE
    (the feed's own date); the inspection is the only sign it still trades.
  * **It has no type field either**, so restaurants and food shops are one
    layer (pipeline/taxonomies/ottawa_inspection.py), and what is left out -
    institutional kitchens, clubs, mobile and event vendors - is decided by
    the premises NAME, listed row by row in excluded_premises.csv.
  * **In-city is point-in-boundary** against the dissolved wards; `city` is
    a postal free-text field (OTTAWA, OTATWA, Manotick, Kanata...).
  * **`phone_number` is never read.** The premises name is shown as the feed
    gives it; check_personal_exposure.py measures whether any is a person's.

Run:  python pipeline/ottawa/step2_clean_businesses.py
"""
import io
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.ottawa import config  # noqa: E402

from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.ottawa_inspection import FOOD, KNOWN_KINDS, premises_kind  # noqa: E402

# Never `phone_number`: the columns read are named, and the step asserts it.
BUSINESS_COLUMNS = ["business_id", "name", "address", "city", "postal_code",
                    "latitude", "longitude"]
OUT = ["source_key", "business_name", "premises_kind", "address", "postal_code",
       "last_inspected", "latitude", "longitude"]


def main():
    if not config.FEED_ZIP.exists():
        sys.exit(f"missing {config.FEED_ZIP}\nRun: python pipeline/ottawa/fetch_sources.py")
    with zipfile.ZipFile(config.FEED_ZIP) as z:
        feed_date = z.read("feed_info.csv").decode("utf-8").splitlines()[-1].split(",")[0].strip('"')
        biz = pd.read_csv(io.BytesIO(z.read("businesses.csv")), dtype=str,
                          usecols=BUSINESS_COLUMNS, keep_default_na=False)
        ins = pd.read_csv(io.BytesIO(z.read("inspections.csv")), dtype=str,
                          usecols=["business_id", "date"])
    assert "phone_number" not in biz.columns
    as_of = pd.Timestamp(config.AS_OF_DATE)
    if feed_date != as_of.strftime("%Y%m%d"):
        sys.exit(f"feed_info says {feed_date}, config.AS_OF_DATE {config.AS_OF_DATE}: "
                 "a re-fetched feed needs the date moved with it")
    if not biz["business_id"].is_unique:
        sys.exit("business_id is not unique in businesses.csv")
    print(f"Feed {feed_date}: {len(biz):,} premises, {len(ins):,} inspections")

    # --- Currency: inspected within two years -------------------------------
    ins["d"] = pd.to_datetime(ins["date"].str[:8], format="%Y%m%d", errors="raise")
    last = ins.groupby("business_id")["d"].max()
    cut = as_of - pd.DateOffset(years=config.CURRENCY_YEARS)
    biz["last_inspected"] = biz["business_id"].map(last)
    recent = biz[biz["last_inspected"] >= cut].copy()
    print(f"Inspected since {cut.date()}: {len(recent):,} "
          f"({len(biz) - len(recent):,} older or never inspected)")
    emit("inspected_recently", len(recent))

    # --- The premises kind, by name -----------------------------------------
    recent["premises_kind"] = [premises_kind(n, a) for n, a in
                               zip(recent["name"], recent["address"])]
    assert set(recent["premises_kind"]) <= KNOWN_KINDS
    recent["latitude"] = pd.to_numeric(recent["latitude"], errors="coerce")
    recent["longitude"] = pd.to_numeric(recent["longitude"], errors="coerce")
    nopoint = (recent["premises_kind"] == FOOD) & (
        recent["latitude"].fillna(0).eq(0) | recent["longitude"].fillna(0).eq(0))
    recent["reason"] = recent["premises_kind"].where(recent["premises_kind"] != FOOD, "")
    recent.loc[nopoint, "reason"] = "No point in the feed"
    print("\nBy kind:")
    print(recent["premises_kind"].value_counts().to_string())
    print(f"Food premises with no point: {int(nopoint.sum()):,} (the feed withholds "
          "the address of shelters and similar as RESTRICTED)")
    for kind, n in recent["premises_kind"].value_counts().items():
        emit(f"kind_{kind.lower().replace(' ', '_')}", int(n))
    emit("no_point", int(nopoint.sum()))

    # --- In the City: point-in-boundary against the dissolved wards ----------
    placed = recent[recent["reason"] == ""].copy()
    wards = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    shape = wards.geometry.union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(placed["longitude"], placed["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=placed.index)
    inside = pts.within(shape)
    out_of_city = placed[~inside]
    print(f"Outside the City's wards: {len(out_of_city):,}")
    if len(out_of_city):
        print(out_of_city[["name", "address", "city", "latitude", "longitude"]]
              .head(10).to_string())
    recent.loc[out_of_city.index, "reason"] = "Point outside the City"
    emit("outside_city", len(out_of_city))

    excluded = recent[recent["reason"] != ""]
    excluded[["business_id", "name", "address", "reason"]].rename(
        columns={"business_id": "source_key", "name": "business_name"}).sort_values(
        ["reason", "business_name"]).to_csv(config.EXCLUDED_PREMISES_CSV, index=False,
                                            encoding="utf-8")
    print(f"{len(excluded):,} left out -> {config.EXCLUDED_PREMISES_CSV.relative_to(config.ROOT)}")

    df = recent[recent["reason"] == ""].copy()
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    assert all(tax.classify({tax.VALUE_COLUMN: v}) for v in df[tax.VALUE_COLUMN])

    # --- The displayed name is the feed's own premises name -----------------
    # NOT pipeline.residence's looks_personal shape test, which Sacramento
    # uses: measured here it flags 1,340 of 5,031 names, and a read of 120 of
    # them found trade names throughout (TIM HORTONS, FIVE GUYS, NO FRILLS,
    # FARM BOY) - an upper-case two-word trade name has a person's shape.
    # check_personal_exposure.py measures what remains instead.
    df["business_name"] = df["name"].str.strip()

    dup = df.duplicated(["name", "address"], keep=False)
    print(f"Premises sharing a name and address with another id: {int(dup.sum()):,} "
          "(kept: the feed gives each its own id)")

    b = config.OTTAWA_BBOX
    assert df["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert df["longitude"].between(b["lon_min"], b["lon_max"]).all()

    df["source_key"] = df["business_id"]
    df["last_inspected"] = df["last_inspected"].dt.strftime("%Y-%m-%d")
    emit("storefronts", len(df))
    out = df[OUT].sort_values("source_key").reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
