"""Step 3 - Place Dallas's storefronts: an address join to the City's Address
Points, then the US Census Bureau's geocoder for the residue, then the City's
TIGER polygon. Houston's step 3, on Dallas's address layer.

Input:  data/dallas/processed/businesses_clean.csv
        data/dallas/raw/address_points.csv   (fetch_sources.py)
Output: data/dallas/processed/businesses_geocoded.csv

The join (the address-join skill), Houston's passes: the street as filed with
its unit cut, exact within its ZIP; then both sides in the same canonical form
(street words abbreviated, a letter on the house number dropped), within the
ZIP; then that form under any ZIP where the street address is unique. Then the
brief's fourth tier: the NEAREST listed number on the same side of the same
canonical street and ZIP, within 10 (the brief's sample: 1.7%; Incheon's and
Palma's rule). A street address with several points is placed at their mean.
What none matches goes to the Census geocoder (street and ZIP only, never a
name), cached by batch hash so a drift check stays offline.

NOT RUN HERE: Houston's "a person's business at a Residential point is a home".
The Address Points carry an ADDRESSTYPE code (T, B, A, P, ...) that neither the
layer nor its ArcGIS item documents, so no code is read as Residential; the
rule waits on the codes' meaning (flagged for review time). A personally owned
outlet still shows its address, never a name (step 2), and one at an
apartment or trailer is still left off.

Run:  python pipeline/dallas/step3_place.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.census_geocoder import geocode_addresses  # noqa: E402
from pipeline.dallas import config  # noqa: E402

# Houston's one spelling for the words a street is filed under two ways,
# applied to BOTH sides.
WORDS = {
    "HIGHWAY": "HWY", "FREEWAY": "FWY", "PARKWAY": "PKWY", "BOULEVARD": "BLVD",
    "STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "ROAD": "RD", "LANE": "LN",
    "COURT": "CT", "CIRCLE": "CIR", "PLACE": "PL", "TRAIL": "TRL", "EXPRESSWAY": "EXPY",
    "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W", "SAINT": "ST",
    "FARM-TO-MARKET": "FM", "FARM": "FM", "TOLLWAY": "TOLL", "TERRACE": "TER",
    "SQUARE": "SQ", "PLAZA": "PLZ", "LOOP": "LOOP", "CROSSING": "XING",
}
NEAREST_NUMBER_MAX = 10


def canonical(street):
    s = re.sub(r"[^A-Z0-9 ]", " ", str(street).upper())
    toks = s.split()
    if toks and re.fullmatch(r"\d+[A-Z]", toks[0]):
        toks[0] = toks[0][:-1]              # "3901C BELLAIRE BLVD" -> 3901
    return " ".join(WORDS.get(t, t) for t in toks)


def address_points():
    """The Address Points as street + ZIP rows with their point."""
    if not config.ADDRESS_POINTS_CSV.exists():
        sys.exit(f"missing {config.ADDRESS_POINTS_CSV}\nRun: python pipeline/dallas/fetch_sources.py")
    ap = pd.read_csv(config.ADDRESS_POINTS_CSV, dtype=str, keep_default_na=False)
    print(f"  Address Points: {len(ap):,} points")
    ap = ap[(ap["HOUSENUMBER"] != "") & (ap["FULLSTREETNAME"] != "") & (ap["latitude"] != "")]
    num = ap["HOUSENUMBER"].str.replace(r"\.0$", "", regex=True)
    street = (num + " " + ap["FULLSTREETNAME"].str.upper()).str.replace(r"\s+", " ", regex=True).str.strip()
    return pd.DataFrame({"street": street, "number": pd.to_numeric(num, errors="coerce"),
                         "name": ap["FULLSTREETNAME"].str.upper().str.strip(),
                         "zip": ap["ZIPCODE"].str.replace(r"\.0$", "", regex=True).str.slice(0, 5),
                         "latitude": pd.to_numeric(ap["latitude"]), "longitude": pd.to_numeric(ap["longitude"])})


def collapse(sa, key):
    g = sa.groupby(key)
    return g.agg(latitude=("latitude", "mean"), longitude=("longitude", "mean"),
                 points=("latitude", "size"))


def nearest_same_side(rest, sa):
    """The nearest listed number on the same side (parity) of the same canonical
    street name and ZIP, within NEAREST_NUMBER_MAX."""
    sa = sa.dropna(subset=["number"]).copy()
    sa["cname"] = sa["name"].map(canonical)
    sa["parity"] = (sa["number"] % 2).astype(int)
    idx = {k: g for k, g in sa.groupby(["cname", "zip", "parity"])}
    out = []
    for _, r in rest.iterrows():
        m = re.match(r"^(\d+)[A-Z]?\s+(.*)$", r["street"])
        if not m:
            continue
        n, name = int(m.group(1)), canonical(m.group(2))
        g = idx.get((name, r["zip"], n % 2))
        if g is None:
            continue
        d = (g["number"] - n).abs()
        best = d.min()
        if best <= NEAREST_NUMBER_MAX:
            hit = g[d == best]
            out.append({"permit": r["permit"], "latitude": hit["latitude"].mean(),
                        "longitude": hit["longitude"].mean(), "points": len(hit),
                        "number_gap": int(best)})
    return pd.DataFrame(out, columns=["permit", "latitude", "longitude", "points", "number_gap"])


def main():
    if not config.BUSINESSES_CLEAN_CSV.exists():
        sys.exit("Run step2_clean_businesses.py first.")
    df = pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype=str, keep_default_na=False)
    df["name_is_address"] = df["name_is_address"] == "True"
    print(f"Placing {len(df):,} storefronts")

    sa = address_points()
    print(f"  Address Points with a house number: {len(sa):,} points, "
          f"{sa['street'].nunique():,} street addresses")

    sa1 = collapse(sa, ["street", "zip"])
    sa["canon"] = sa["street"].map(canonical)
    sa2 = collapse(sa, ["canon", "zip"])
    df["canon"] = df["street"].map(canonical)

    p1 = df.join(sa1, on=["street", "zip"], how="inner")
    rest = df[~df["permit"].isin(p1["permit"])]
    p2 = rest.join(sa2, on=["canon", "zip"], how="inner")
    rest = rest[~rest["permit"].isin(p2["permit"])]
    zips = sa.groupby("canon")["zip"].nunique()
    sa3 = collapse(sa[sa["canon"].isin(zips[zips == 1].index)], ["canon"])
    p3j = rest.join(sa3, on="canon", how="inner")
    rest = rest[~rest["permit"].isin(p3j["permit"])]
    near = nearest_same_side(rest, sa)
    p4 = rest.merge(near, on="permit", how="inner")
    rest = rest[~rest["permit"].isin(p4["permit"])]
    print(f"  join pass 1 (street as filed): {len(p1):,} ({len(p1) / len(df):.1%})")
    print(f"  join pass 2 (canonical form):  {len(p2):,}")
    print(f"  join pass 3 (unique street, any ZIP): {len(p3j):,}")
    print(f"  join pass 4 (nearest number, same side, within {NEAREST_NUMBER_MAX}): {len(p4):,}")
    emit("joined", len(p1) + len(p2) + len(p3j))
    emit("joined_nearest", len(p4))

    print(f"  to the Census geocoder: {len(rest):,}")
    matched = geocode_addresses(rest, id_col="permit", street_col="street", zip_col="zip",
                                city="Dallas", state="TX", cache_dir=config.GEOCODE_CACHE_DIR)
    p5 = rest.merge(matched[["id", "latitude", "longitude"]].rename(columns={"id": "permit"}),
                    on="permit", how="inner")
    p5["points"] = 0
    print(f"  Census matched {len(p5):,} of {len(rest):,}")
    emit("census_geocoded", len(p5))
    unplaced = len(rest) - len(p5)

    placed = pd.concat([p1.assign(placed_by="address_points"),
                        p2.assign(placed_by="address_points"),
                        p3j.assign(placed_by="address_points"),
                        p4.assign(placed_by="address_points_nearest"),
                        p5.assign(placed_by="census")], ignore_index=True)
    print(f"  placed {len(placed):,} of {len(df):,} ({len(placed) / len(df):.1%}); "
          f"{unplaced:,} unplaced")
    emit("unplaced", unplaced)

    b = config.DALLAS_BBOX
    ok = (placed["latitude"].between(b["lat_min"], b["lat_max"])
          & placed["longitude"].between(b["lon_min"], b["lon_max"]))
    if (~ok).any():
        print(f"  {int((~ok).sum()):,} placed outside the city's box, dropped")
    placed = placed[ok]

    # POINT-IN-BOUNDARY: the register's flag says inside SOME city's limits,
    # and "DALLAS" is the postal city. TIGER's polygon decides.
    import geopandas as gpd
    from pipeline.dallas.step1_stations import city_polygon
    city = city_polygon()
    pts = gpd.GeoSeries(gpd.points_from_xy(placed["longitude"], placed["latitude"]),
                        crs=config.CRS_GEOGRAPHIC, index=placed.index)
    inside = pts.within(city)
    print(f"  inside the City of Dallas: {int(inside.sum()):,} of {len(placed):,} "
          f"({int((~inside).sum()):,} outside the city, dropped)")
    emit("outside_city", int((~inside).sum()))
    placed = placed[inside]
    by = placed["placed_by"].value_counts()
    print("  placed by: " + ", ".join(f"{k} {v:,} ({v / len(placed):.1%})" for k, v in by.items()))

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
