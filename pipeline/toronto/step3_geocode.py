"""Step 3 - geocode Toronto's storefronts against the One Address Repository.

Input:  data/toronto/processed/businesses_clean.csv
        data/toronto/raw/address_points.csv          (525,440 points)
        data/toronto/raw/toronto_boundary_wgs84.zip
Output: data/toronto/processed/businesses_geocoded.csv

TORONTO IS THE ONLY CANADIAN CITY OF SIX THAT NEEDS THIS STEP. Its register
carries no coordinate field of any kind, and **Canada has no national bulk
geocoder** - there is no equivalent of the US Census bulk service that Los
Angeles and Washington D.C. use. The answer is not a geocoder at all: it is a
join against the City's own address-point layer, published under the same
licence as the business data.

THE NORMALISATION THAT MATTERS IS ONE LINE, AND IT IS NOT STREET
NORMALISATION.
------------------------------------------------------------------
The build brief named the obstacle as matching "with no street normalisation",
implying abbreviations and suffixes were the problem. They are not. The
register writes the UNIT into the address line and the repository does not
carry units:

    "280 SPADINA AVE, #308"        ->  repository has "280 SPADINA AVE"
    "1835 EGLINTON AVE W, 2ND FLR" ->  repository has "1835 EGLINTON AVE W"

20,091 rows look like that. Measured 2026-09-21:

    raw case + whitespace join              48.1% of all licence rows
    everything from the first comma dropped 73.1% of all licence rows
                                            92.8% of STOREFRONT rows

**And the brief's own 71.4% was the wrong denominator** - measured across all
159,872 rows, more than half of which are person-held licences (tow truck
owners, master plumbers, taxicab owners) with no premises address to match at
all. On the rows this map actually uses it is 92.8%, so Toronto's density is
not "a floor resting on a 71.4% match" but a near-complete measurement.

WHAT THE UNMATCHED REMAINDER IS, MEASURED RATHER THAN ASSUMED
------------------------------------------------------------
The brief ASSERTED the misses were evenly distributed and flagged that nobody
had checked. Checked:

  - **By ward** - the axis that would distort the map's spatial pattern, which
    is the thing this project shows. Across the wards holding at least 200
    storefront rows the match rate runs 73.6% to 97.8%: a **1.3x spread**,
    standard deviation 5.4 points. Mild.
  - **By issue year** - flat, no trend.
  - **By category** - biased in Toronto's favour; the misses concentrate in the
    person-held licences this map excludes anyway.
  - **The residual** concentrates on a few plaza and mall addresses the
    repository does not carry as one string (`1571 SANDHURST CIR`, `8 WESTMORE
    DR`), so it under-counts a handful of malls rather than a district.

A first pass on the broken 48.1% join showed a **12x** ward spread and looked
disqualifying. It was an artefact of the join. That is why this step asserts
the match rate against `GEOCODE_MATCH_RATE_MIN` - a measurement taken through
a broken instrument is not evidence, and the instrument has to reproduce a
known number first.

`MUNICIPALITY_NAME` IS NOT A CITY FILTER
----------------------------------------
The brief says the repository "returns `MUNICIPALITY_NAME`, so it doubles as
the in-city filter". It does not: the field holds the **six pre-1998
municipalities** that amalgamated into Toronto - former Toronto, Scarborough,
North York, Etobicoke, York, East York - so matching "Toronto" keeps 30% of the
city and would silently drop most of Line 2. That is Los Angeles' `CITY_KEEP`
trap. Every point in this repository is in Toronto, so no municipal filter is
needed; the boundary polygon is the check.

Run:  python pipeline/toronto/step3_geocode.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.counts import pct  # noqa: E402
from pipeline.toronto.config import (  # noqa: E402
    ADDRESS_MUNICIPALITY_COLUMN,
    ADDRESS_POINTS_CSV,
    ADDRESS_TRAILING_UNIT_PATTERN,
    ADDRESS_UNIT_PATTERN,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_GEOCODED_CSV,
    CITY_BOUNDARY_ZIP,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GEOCODE_MATCH_RATE_MIN,
    MUNICIPALITY_VALUES_EXPECTED,
    TORONTO_BBOX,
)

UNIT = re.compile(ADDRESS_UNIT_PATTERN)
TRAIL = re.compile(ADDRESS_TRAILING_UNIT_PATTERN)
WS = re.compile(r"\s+")


def norm_licence(s):
    """The register's address, with the unit stripped - the one line that
    takes the match rate from 48.1% to 92.8%."""
    s = str(s or "").upper().strip()
    s = UNIT.sub("", s)
    s = TRAIL.sub("", s)
    return WS.sub(" ", s).strip()


def norm_repo(s):
    """The repository's ADDRESS_FULL carries no unit, so case and whitespace
    only - deliberately NOT the same function, so the asymmetry is visible."""
    return WS.sub(" ", str(s or "").upper().strip())


def main():
    for p in (BUSINESSES_CLEAN_CSV, ADDRESS_POINTS_CSV, CITY_BOUNDARY_ZIP):
        if not p.exists():
            sys.exit(f"Missing {p.name}. Run the earlier steps first.")

    biz = pd.read_csv(BUSINESSES_CLEAN_CSV, dtype=str)
    print(f"storefronts to geocode: {len(biz):,}")

    addr = pd.read_csv(ADDRESS_POINTS_CSV, dtype=str, low_memory=False,
                       usecols=["ADDRESS_FULL", ADDRESS_MUNICIPALITY_COLUMN,
                                "geometry"])
    print(f"address points: {len(addr):,}")

    munis = set(addr[ADDRESS_MUNICIPALITY_COLUMN].dropna().unique())
    print(f"  {ADDRESS_MUNICIPALITY_COLUMN} holds {len(munis)} values - the "
          f"pre-1998 municipalities, NOT a city filter: "
          f"{', '.join(sorted(munis))}")
    unexpected = munis - set(MUNICIPALITY_VALUES_EXPECTED)
    if unexpected:
        print(f"  NOTE: unexpected value(s) {sorted(unexpected)} - if a "
              f"neighbouring municipality has been added, this layer is no "
              f"longer Toronto-only and DOES need filtering.")

    # The 4326 CSV's `geometry` is a GeoJSON **MultiPoint** string, not WKT:
    #   {"coordinates": [[-79.5190367341825, 43.5996761490216]], "type": "MultiPoint"}
    # A WKT `POINT(...)` pattern matches nothing here and yields a 0% join,
    # which is what GEOCODE_MATCH_RATE_MIN caught on the first run. Taking the
    # first coordinate pair is correct: every row carries exactly one point
    # despite the MultiPoint wrapper.
    xy = addr["geometry"].str.extract(
        r"\[\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\]")
    addr["longitude"] = pd.to_numeric(xy[0], errors="coerce")
    addr["latitude"] = pd.to_numeric(xy[1], errors="coerce")
    bad = addr["latitude"].isna() | addr["longitude"].isna()
    if bad.any():
        print(f"  {int(bad.sum()):,} address points with unparseable geometry "
              f"- dropped")
        addr = addr[~bad]

    addr["k"] = addr["ADDRESS_FULL"].map(norm_repo)
    lookup = addr.drop_duplicates("k").set_index("k")[
        ["latitude", "longitude", ADDRESS_MUNICIPALITY_COLUMN]]
    print(f"  {len(lookup):,} distinct normalised addresses")

    # --- the join ----------------------------------------------------------
    biz["k"] = biz["address"].map(norm_licence)
    joined = biz.join(lookup, on="k")
    matched = joined["latitude"].notna()
    rate = matched.mean()
    # The set is named because the unnamed version of this number - 71.4%,
    # measured across all 159,872 licence rows including person-held ones with
    # no premises to match - understated the city's coverage for a day.
    print(f"\nmatched: {pct(int(matched.sum()), len(biz), 'storefront rows')}")
    print(f"  for contrast, WITHOUT stripping the unit the rate is ~48% - "
          f"that one line is the whole geocoder")
    if rate < GEOCODE_MATCH_RATE_MIN:
        sys.exit(
            f"  match rate {100 * rate:.1f}% is below "
            f"{100 * GEOCODE_MATCH_RATE_MIN:.0f}%, which was 92.8% on "
            f"2026-09-21. Do NOT accept a lower rate and carry on: a broken "
            f"join produced a 12x ward-level bias that read as a property of "
            f"the data. Check norm_licence() against a sample of unmatched "
            f"addresses first."
        )

    unmatched = joined[~matched]
    print(f"\nunmatched {len(unmatched):,} - the most repeated addresses "
          f"(plazas the repository does not carry as one string):")
    for a, n in unmatched["k"].value_counts().head(5).items():
        print(f"    {n:>4} x  {a}")

    # bias check, printed every run so a regression is visible as a number
    if "Ward" in joined.columns:
        w = joined.assign(m=matched).groupby(
            joined["Ward"].fillna("<blank>"))["m"].agg(["size", "mean"])
        w = w[w["size"] >= 200]
        if len(w) > 1:
            lo, hi = w["mean"].min(), w["mean"].max()
            print(f"\nward bias check: {len(w)} wards with >=200 rows, match "
                  f"rate {100 * lo:.1f}% to {100 * hi:.1f}% "
                  f"({hi / max(lo, 1e-9):.1f}x spread, "
                  f"std {100 * w['mean'].std():.1f} points)")
            if hi / max(lo, 1e-9) > 3.0:
                print("  WARNING: a spread above 3x distorts the map's spatial "
                      "pattern, which is what this project shows. On "
                      "2026-09-21 the true spread was 1.3x and a 12x reading "
                      "meant the JOIN was broken, not the data.")

    df = joined[matched].copy()
    df["geocode_source"] = "toronto_one_address_repository"

    in_box = (df["latitude"].between(TORONTO_BBOX["lat_min"],
                                     TORONTO_BBOX["lat_max"])
              & df["longitude"].between(TORONTO_BBOX["lon_min"],
                                        TORONTO_BBOX["lon_max"]))
    if int((~in_box).sum()):
        print(f"\n{int((~in_box).sum()):,} outside the sanity box - dropped")
    df = df[in_box].copy()

    # --- the boundary: a CHECK --------------------------------------------
    b = gpd.read_file(CITY_BOUNDARY_ZIP)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    geom = b.to_crs(CRS_PROJECTED).union_all()
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = gdf.geometry.within(geom)
    print(f"\ninside the city boundary: {int(inside.sum()):,} of {len(gdf):,} "
          f"({int((~inside).sum()):,} outside - the repository is Toronto-only, "
          f"so a large number here would mean the wrong boundary layer)")
    df = gdf[inside].drop(columns="geometry").copy()

    out = df.drop(columns=[c for c in ("k", ADDRESS_MUNICIPALITY_COLUMN)
                           if c in df.columns])
    BUSINESSES_GEOCODED_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(BUSINESSES_GEOCODED_CSV, index=False)
    print(f"\nWrote {len(out):,} geocoded storefronts to "
          f"{BUSINESSES_GEOCODED_CSV}")


if __name__ == "__main__":
    main()
