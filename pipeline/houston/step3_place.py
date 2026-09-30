"""Step 3 - Place Houston's storefronts: an address join to the City's Site
Addresses (public domain), then the US Census Bureau's geocoder for the
residue, then the City's TIGER polygon.

Input:  data/houston/processed/businesses_clean.csv
        data/houston/raw/Export_SiteAddresses.zip   (fetch_sources.py)
Output: data/houston/processed/businesses_geocoded.csv

The join (the address-join skill): the street as filed with its unit cut,
exact first, then both sides put through the same canonical form (street
words abbreviated, a letter on the house number dropped), then that form under
any ZIP where the street address is unique. A street address
with several points (one per unit) is placed at their mean. What neither pass
matches goes to the Census geocoder (street and ZIP only, never a name),
cached by batch hash so a drift check stays offline.

Run:  python pipeline/houston/step3_place.py
"""
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.census_geocoder import geocode_addresses  # noqa: E402
from pipeline.houston import config  # noqa: E402

GDB = f"zip://{config.SITE_ADDRESSES_ZIP.as_posix()}!Export_SiteAddresses.gdb"
SA_COLUMNS = ["fulladdr", "addrnum", "unitid", "unittype", "municipality", "zipcode", "addrtype"]

# One spelling for the words a street is filed under two ways ("HIGHWAY 6 N" /
# "HWY 6 N"), applied to BOTH sides. The USPS suffix abbreviations plus the
# highway words the brief's sample missed on.
WORDS = {
    "HIGHWAY": "HWY", "FREEWAY": "FWY", "PARKWAY": "PKWY", "BOULEVARD": "BLVD",
    "STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "ROAD": "RD", "LANE": "LN",
    "COURT": "CT", "CIRCLE": "CIR", "PLACE": "PL", "TRAIL": "TRL", "EXPRESSWAY": "EXPY",
    "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W", "SAINT": "ST",
    "FARM-TO-MARKET": "FM", "FARM": "FM", "TOLLWAY": "TOLL", "TERRACE": "TER",
    "SQUARE": "SQ", "PLAZA": "PLZ", "LOOP": "LOOP", "CROSSING": "XING",
}
UNIT_WORDS = r"\s(?:STE|SUITE|UNIT|APT|BLDG|SPC|SPACE|RM|ROOM|FL|FLOOR|LOT|TRLR|#)\b.*$|\s#.*$"


def canonical(street):
    s = re.sub(r"[^A-Z0-9 ]", " ", str(street).upper())
    toks = s.split()
    if toks and re.fullmatch(r"\d+[A-Z]", toks[0]):
        toks[0] = toks[0][:-1]              # "3901C BELLAIRE BLVD" -> 3901
    return " ".join(WORDS.get(t, t) for t in toks)


def site_addresses():
    """The Site Addresses as street key -> mean point, cached as parquet."""
    cache = config.SITE_ADDRESSES_PARQUET
    if cache.exists() and cache.stat().st_mtime > config.SITE_ADDRESSES_ZIP.stat().st_mtime:
        return pd.read_parquet(cache)
    if not config.SITE_ADDRESSES_ZIP.exists():
        sys.exit(f"missing {config.SITE_ADDRESSES_ZIP}\nRun: python pipeline/houston/fetch_sources.py")
    import pyogrio
    gdf = pyogrio.read_dataframe(GDB, columns=SA_COLUMNS).to_crs(config.CRS_GEOGRAPHIC)
    print(f"  Site Addresses: {len(gdf):,} points")
    df = pd.DataFrame({
        "street": gdf["fulladdr"].fillna("").str.upper().str.replace(UNIT_WORDS, "", regex=True)
                  .str.replace(r"\s+", " ", regex=True).str.strip(),
        "zip": gdf["zipcode"].fillna("").astype(str).str.slice(0, 5),
        "municipality": gdf["municipality"].fillna(""),
        "addrtype": gdf["addrtype"].fillna(""),
        "latitude": gdf.geometry.y, "longitude": gdf.geometry.x})
    del gdf
    df = df[df["street"].str.match(r"^\d")]
    df.to_parquet(cache, index=False)
    return df


def collapse(sa, key):
    """One row per key: the mean point, and whether every typed point says
    Residential (a blank type says nothing)."""
    g = sa.assign(_res=sa["addrtype"].isin(["Residential", "RES"]),
                  _typed=sa["addrtype"] != "").groupby(key)
    out = g.agg(latitude=("latitude", "mean"), longitude=("longitude", "mean"),
                points=("latitude", "size"), residential=("_res", "sum"), typed=("_typed", "sum"))
    out["residential"] = (out["residential"] > 0) & (out["residential"] == out["typed"])
    return out.drop(columns="typed")


def main():
    if not config.BUSINESSES_CLEAN_CSV.exists():
        sys.exit("Run step2_clean_businesses.py first.")
    df = pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype=str, keep_default_na=False)
    df["name_is_address"] = df["name_is_address"] == "True"
    print(f"Placing {len(df):,} storefronts")

    sa = site_addresses()
    print(f"  Site Addresses with a house number: {len(sa):,} points, "
          f"{sa['street'].nunique():,} street addresses")

    # Pass 1: the street exactly, within its ZIP (a street address can repeat
    # across the region's ZIPs); pass 2: the canonical form, within its ZIP.
    sa1 = collapse(sa, ["street", "zip"])
    sa["canon"] = sa["street"].map(canonical)
    sa2 = collapse(sa, ["canon", "zip"])
    df["canon"] = df["street"].map(canonical)

    p1 = df.join(sa1, on=["street", "zip"], how="inner")
    rest = df[~df["permit"].isin(p1["permit"])]
    p2 = rest.join(sa2, on=["canon", "zip"], how="inner")
    rest = rest[~rest["permit"].isin(p2["permit"])]
    # Pass 3: the canonical form under ANY ZIP, only where the street address
    # is unique across the region's ZIPs (a permit's ZIP can be the post
    # office's, not the point's).
    zips = sa.groupby("canon")["zip"].nunique()
    sa3 = collapse(sa[sa["canon"].isin(zips[zips == 1].index)], ["canon"])
    p3j = rest.join(sa3, on="canon", how="inner")
    rest = rest[~rest["permit"].isin(p3j["permit"])]
    print(f"  join pass 1 (street as filed): {len(p1):,} ({len(p1) / len(df):.1%})")
    print(f"  join pass 2 (canonical form):  {len(p2):,}")
    print(f"  join pass 3 (unique street, any ZIP): {len(p3j):,}")
    emit("joined", len(p1) + len(p2) + len(p3j))

    # The residue to the Census Bureau: street and ZIP only.
    print(f"  to the Census geocoder: {len(rest):,}")
    matched = geocode_addresses(rest, id_col="permit", street_col="street", zip_col="zip",
                                city="Houston", state="TX", cache_dir=config.GEOCODE_CACHE_DIR)
    p3 = rest.merge(matched[["id", "latitude", "longitude"]].rename(columns={"id": "permit"}),
                    on="permit", how="inner")
    p3["points"], p3["residential"] = 0, False
    print(f"  Census matched {len(p3):,} of {len(rest):,}")
    emit("census_geocoded", len(p3))
    unplaced = len(rest) - len(p3)

    placed = pd.concat([p1.assign(placed_by="site_addresses"),
                        p2.assign(placed_by="site_addresses"),
                        p3j.assign(placed_by="site_addresses"),
                        p3.assign(placed_by="census")], ignore_index=True)
    print(f"  placed {len(placed):,} of {len(df):,} ({len(placed) / len(df):.1%}); "
          f"{unplaced:,} unplaced")

    b = config.HOUSTON_BBOX
    ok = (placed["latitude"].between(b["lat_min"], b["lat_max"])
          & placed["longitude"].between(b["lon_min"], b["lon_max"]))
    if (~ok).any():
        print(f"  {int((~ok).sum()):,} placed outside the city's box, dropped")
    placed = placed[ok]

    # POINT-IN-BOUNDARY: the register's flag says inside SOME city's limits,
    # and "HOUSTON" is the postal city. TIGER's polygon decides.
    import geopandas as gpd
    from pipeline.houston.step1_stations import city_polygon
    city = city_polygon()
    pts = gpd.GeoSeries(gpd.points_from_xy(placed["longitude"], placed["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=placed.index)
    inside = pts.within(city)
    print(f"  inside the City of Houston: {int(inside.sum()):,} of {len(placed):,} "
          f"({int((~inside).sum()):,} outside the city, dropped)")
    emit("outside_city", int((~inside).sum()))
    placed = placed[inside]

    # A PERSON'S BUSINESS AT A RESIDENTIAL POINT IS A HOME (owner, 2026-09-29,
    # the brief's recommendation): the City types the point Residential, and
    # the permit holder is a person. A measured home signal, not a guess from
    # the name. A company at such a point stays: its name is a company's.
    home = placed["name_is_address"] & placed["residential"].astype(bool)
    print(f"  personally owned at a Residential point: {int(home.sum()):,} left off as homes "
          f"(companies at a Residential point: "
          f"{int((~placed['name_is_address'] & placed['residential'].astype(bool)).sum()):,}, kept)")
    emit("personal_at_residential", int(home.sum()))
    placed = placed[~home]

    out = placed[["permit", "business_name", "naics", "address", "zip", "org_type",
                  "name_is_address", "placed_by", "latitude", "longitude"]] \
        .sort_values("permit").reset_index(drop=True)
    out["latitude"] = out["latitude"].round(6)
    out["longitude"] = out["longitude"].round(6)
    out.to_csv(config.BUSINESSES_PLACED_CSV, index=False, encoding="utf-8")
    emit("placed", len(out))
    print(f"\n{len(out):,} placed -> {config.BUSINESSES_PLACED_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
