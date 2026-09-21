"""Rank Canada's candidate cities on STOREFRONT density, comparably.

    python scripts/rank_canada_storefront_density.py [--cache DIR]

WHY THIS EXISTS. The Canada profile of 2026-09-21 ranked six cities on
"businesses within the outermost 0.6 mi ring, divided by in-city stations" and
got Vancouver 861, Surrey 549, Montreal 252, Edmonton 153, Calgary 103,
Toronto 41. Only Toronto's figure was storefront-filtered; the other five
counted every mappable licence, including the residential rentals, contractors
and professional offices this project never maps. So the numbers were not
comparable with each other, nor with the US cities they were being judged
against (D.C. ~173, Boston ~39), and the inflation was **not uniform** - it
ranged from 1.0x to 4.2x, biasing licence-register cities against Montreal's
commerce survey.

This recomputes all of them on one basis. It is deliberately Canada-specific:
Calgary's and Edmonton's category maps below are their own vocabularies, and
the three Mobility Database ids are hardcoded. A city in another country needs
its own equivalent, not this file.

WHAT "COMPARABLE" MEANS HERE, and the two mistakes this file is shaped to
avoid:

  1. **Filter to storefronts before counting.** Buckets are anchored on
     `pipeline/taxonomies/naics.py` - Retail 44-45 less 454 nonstore, Food
     service 722, Personal services 812 less 81293 parking - so the result is
     on the same footing as every built city.

  2. **Count the UNION of the rings, never the sum of per-station counts.**
     A first version of this measurement summed per-station counts and
     reported Montreal at 440 per station against a true 151, because the
     Metro's stations are close enough that one business sits inside several
     rings. The union is the number of distinct businesses near rail; the sum
     is a different quantity and is not what any other figure in this project
     means.

Montreal needs no category map: its `SCIAN` IS NAICS, so `naics.py` applies
unchanged. That is also why it is the cheapest of the four still unbuilt.

Toronto is NOT recomputed. Its 41 was already storefront-filtered, so it is
the one figure that was on the right basis - though read it as a FLOOR rather
than a point estimate, because it rests on geocoding 159,872 addresses against
the City's address repository at a 71.4% exact-match rate, and the unmatched
29% are not known to be distributed evenly.
"""

import argparse
import io
import sys
import zipfile
from datetime import date
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.taxonomies.naics import naics_group  # noqa: E402

OUTER_M = 0.6 * 1609.344
R, F, P = "Retail", "Food service", "Personal services"

CATALOG = "https://bit.ly/catalogs-csv"
# Per-city projected CRS, derived from each longitude, never shared.
FEEDS = {
    "montreal": {"mdb": "2126", "crs": "EPSG:32618"},
    "calgary": {"mdb": "712", "crs": "EPSG:32611"},
    "edmonton": {"mdb": "714", "crs": "EPSG:32612"},
}

# Montreal's Metro reaches Laval and Longueuil, which are off the island and
# outside the agglomeration scope this project decided for the city. Excluded
# by name because the boundary layer is not needed to identify four stations
# whose ring holds ZERO surveyed premises - the data names them itself.
#
# Station Jean-Drapeau is NOT excluded: it is on Ile Sainte-Helene, inside
# Montreal, and legitimately has no commerce around it. Dropping a genuine
# in-city station because it scores zero would inflate the rate.
MONTREAL_OFF_ISLAND = ("Cartier", "De la Concorde", "Montmorency", "Longueuil")

# --- Calgary: 96 real categories, ',\n'-delimited ---------------------------
# NOT 173: that figure came from splitting on a bare "\n", which over-splits a
# ",\n" delimiter and counts fragments as categories.
CALGARY_BUCKETS = {
    "RETAIL DEALER - PREMISES": R, "TOBACCO RETAILER": R, "VAPE RETAILER": R,
    "MOTOR VEHICLE DEALER - PREMISES": R, "LIQUOR STORE": R,
    "SECONDHAND DEALER": R, "FUEL SALES/STORAGE": R, "CANNABIS STORE": R,
    "PAWN SHOP": R, "BOOK STORE": R,
    "FOOD SERVICE - PREMISES (SEATING)": F, "FOOD SERVICE - PREMISES": F,
    "FOOD SERVICE - PREMISES (NO SEATING)": F,
    "PERSONAL SERVICE": P, "MASSAGE CENTRE (COMMERCIAL)": P,
    "PERSONAL SERVICE (TATTOO)": P, "PERSONAL SERVICE (MICROBLADING)": P,
    "FABRIC CLEANING": P, "KENNEL SERVICE/PET DEALER": P,
}
# Deliberately not buckets, each for a reason this project has met before:
#   ALCOHOL BEVERAGE SALES (*), OUTDOOR PATIO - endorsements held BY a premises
#     that already has a food-service licence. Counting them double-counts one
#     restaurant (D.C.'s endorsement problem).
#   PERSONAL SERVICE (INDEPENDENT CHAIR OPERATOR) - a chair renter inside
#     someone else's shop; New York drops these for that exact reason.
#   PERSONAL SERVICE (FITNESS CONDITIONING) - NAICS 713940, excluded as
#     Vancouver's Fitness Centre is.
#   MOTOR VEHICLE REPAIR AND SERVICE, AUTO BODY SHOP - NAICS 811, not 812.
#   MASSAGE CENTRE is a bucket here although Vancouver's RMT is not, and the
#     difference is real: massage therapy is a regulated health profession in
#     British Columbia and is NOT regulated in Alberta.

# --- Edmonton: 60 real categories, ';'-delimited ---------------------------
# NOT 67, on the same kind of miscount.
EDMONTON_BUCKETS = {
    "Retail Sales (Minor)": R, "Retail Sales (Major)": R,
    "Retail Sales (Convenience Store)": R,
    "Tobacco and Vaping Product Sales": R,
    "Alcohol Sales (Consumption Off-Premises)": R,
    "Vehicle Sales and Rental": R, "Second Hand Dealer": R,
    "Cannabis Retail Sales": R, "Vehicle Wash / Fueling Station": R,
    "Oleoresin Capsicum (OC) Spray Sales": R,
    "Restaurant or Food Service": F,
    "Alcohol Sales (Consumption On-Premises / Minors Allowed)": F,
    "Alcohol Sales (Consumption On-Premises / Minors Prohibited)": F,
    "Personal Service": P,
    "Health Enhancement Centre (Accredited)": P,
    "Health Enhancement Centre (Accredited / Independent)": P,
    "Animal Breeding and Boarding Facility": P,
}
# Not buckets: Public Market Vendor, Food Truck / Food Cart, Travelling or
# Temporary Sales (mobile, i.e. the NAICS 454 reasoning); Food Processing /
# Catering Service, which merges NAICS 311 manufacturing with 7223 catering
# and leads with processing - counting it would add 583 rows, the largest
# single sensitivity in this file; and everything office, residential-rental,
# wholesale, manufacturing, repair, school, recreation and accommodation.
#
# Edmonton's `licencetype` STATES whether a business is home-based, exactly as
# Surrey's does - Commercial 25,105, Home Based 14,114, Non-Resident 2,108,
# Massage Practitioner 1,582, Adult Services 763. Only Commercial is counted.
# The last two are licences held by a person rather than a premises.
EDMONTON_LICENCE_TYPE_KEEP = "Commercial"

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
# donnees.montreal.ca answers a plain client with `RBAC: access denied`.
BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0 Safari/537.36"),
    "Accept": "text/csv,*/*",
}

SOURCES = {
    "montreal": ("https://donnees.montreal.ca/dataset/"
                 "f8582c4d-a933-4306-bb27-d883e13dd207/resource/"
                 "01ded48e-f982-4703-975e-4be0769ef3ee/download/"
                 "occupation-commerciale-2025.csv"),
    "calgary": "https://data.calgary.ca/resource/vdjc-pybd.csv?$limit=60000",
    "edmonton": "https://data.edmonton.ca/resource/qhi4-bdpu.csv?$limit=60000",
}


def fetch(url, path: Path, browser=False):
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, headers=BROWSER_HEADERS if browser else HEADERS,
                     timeout=900)
    if r.status_code != 200:
        sys.exit(f"{path.name}: HTTP {r.status_code}\n{r.text[:300]}")
    path.write_bytes(r.content)
    return path


def rail_stations(city, cache: Path):
    """Station list for one city, from its GTFS. Prints the feed's expiry."""
    spec = FEEDS[city]
    cat = fetch(CATALOG, cache / "mdb_catalog.csv")
    df = pd.read_csv(cat, dtype=str, low_memory=False)
    idcol = next(c for c in df.columns if c.strip() == "mdb_source_id")
    urlcol = next(c for c in df.columns if "urls.latest" in c)
    row = df[df[idcol] == spec["mdb"]]
    if row.empty:
        sys.exit(f"{city}: mdb {spec['mdb']} not in the catalogue")
    zp = fetch(row.iloc[0][urlcol], cache / f"gtfs_{city}.zip")
    z = zipfile.ZipFile(zp)

    if "feed_info.txt" in z.namelist():
        fi = pd.read_csv(io.BytesIO(z.read("feed_info.txt")), dtype=str)
        end = str(fi.iloc[0].get("feed_end_date", "") or "")
        if end and end != "nan":
            ed = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
            days = (ed - date.today()).days
            print(f"  feed_end_date {end} ({days:+d} days)"
                  f"{'  *** STALE - use the agency feed for a real build ***' if days < 0 else ''}")
    else:
        print("  no feed_info.txt (declares no expiry)")

    routes = pd.read_csv(io.BytesIO(z.read("routes.txt")), dtype=str)
    # route_type 2 is commuter rail and is not urban rail, here as everywhere.
    rail = routes[routes["route_type"].isin({"0", "1", "5", "7", "12"})]
    trips = pd.read_csv(io.BytesIO(z.read("trips.txt")), dtype=str)
    stl = pd.read_csv(io.BytesIO(z.read("stop_times.txt")), dtype=str,
                      usecols=["trip_id", "stop_id"])
    stops = pd.read_csv(io.BytesIO(z.read("stops.txt")), dtype=str)
    rt = trips[trips["route_id"].isin(set(rail["route_id"]))]
    served = stl[stl["trip_id"].isin(set(rt["trip_id"]))]
    rs = stops[stops["stop_id"].isin(set(served["stop_id"]))].copy()
    rs["station"] = rs["stop_name"].str.strip()
    agg = rs.groupby("station").agg(
        lat=("stop_lat", lambda s: pd.to_numeric(s).mean()),
        lon=("stop_lon", lambda s: pd.to_numeric(s).mean())).reset_index()
    print(f"  {len(rail)} urban-rail routes, {len(agg)} stations")
    return agg


def union_ring_count(points, stations, crs):
    """Distinct storefronts inside the UNION of every station's outer ring.

    The union, not the sum of per-station counts - see the module docstring.
    """
    b = gpd.GeoDataFrame(points,
                         geometry=gpd.points_from_xy(points.lon, points.lat),
                         crs=4326).to_crs(crs)
    s = gpd.GeoDataFrame(stations,
                         geometry=gpd.points_from_xy(stations.lon, stations.lat),
                         crs=4326).to_crs(crs)
    return int(b.geometry.within(s.geometry.buffer(OUTER_M).union_all()).sum())


def split_bucket(value, table, delim):
    """A premises may hold several categories; it counts if ANY is a bucket."""
    if not isinstance(value, str):
        return None
    for part in value.split(delim):
        got = table.get(part.strip())
        if got:
            return got
    return None


def montreal(cache: Path):
    print("\n=== Montreal - SCIAN is NAICS, so naics.py applies unchanged ===")
    df = pd.read_csv(fetch(SOURCES["montreal"], cache / "montreal.csv",
                           browser=True), dtype=str, low_memory=False)
    print(f"  survey rows: {len(df):,}")
    vac = df["USAGE1"].eq("VACANT")
    print(f"  VACANT units excluded: {int(vac.sum()):,} "
          f"(an empty shopfront is not a business)")
    df = df[~vac]
    real = df["SCIAN"].fillna("").str.len().eq(6)
    print(f"  usable 6-digit SCIAN: {int(real.sum()):,} of {len(df):,} "
          f"({real.mean():.1%}) - the rest are 1-character placeholders")
    df = df[real].copy()
    df["bucket"] = [naics_group(c) for c in df["SCIAN"]]
    sf = df[df["bucket"].notna()].copy()
    print(f"  storefront: {len(sf):,} ({len(sf)/len(df):.1%} of non-vacant) - "
          f"the highest share of any source in this project, because this is a "
          f"street-level commerce SURVEY rather than a licence register")
    print("    " + ", ".join(f"{k}={v:,}" for k, v in
                             sf["bucket"].value_counts().items()))
    sf["lat"] = pd.to_numeric(sf["LAT"], errors="coerce")
    sf["lon"] = pd.to_numeric(sf["LONG"], errors="coerce")
    sf = sf.dropna(subset=["lat", "lon"])
    st = rail_stations("montreal", cache)
    off = st["station"].str.contains("|".join(MONTREAL_OFF_ISLAND))
    print(f"  off-island stations dropped ({int(off.sum())}, in Laval and "
          f"Longueuil): {list(st[off]['station'])}")
    st = st[~off]
    n = union_ring_count(sf, st, FEEDS["montreal"]["crs"])
    return n, len(st)


def calgary(cache: Path):
    print("\n=== Calgary ===")
    df = pd.read_csv(fetch(SOURCES["calgary"], cache / "calgary.csv"),
                     dtype=str, low_memory=False)
    print(f"  rows: {len(df):,}   (homeoccind is 'N' on every one of them, so "
          f"it is not a usable home-business discriminator)")
    df["bucket"] = [split_bucket(v, CALGARY_BUCKETS, ",\n")
                    for v in df["licencetypes"]]
    sf = df[df["bucket"].notna()].copy()
    print(f"  storefront: {len(sf):,}   " + ", ".join(
        f"{k}={v:,}" for k, v in sf["bucket"].value_counts().items()))
    pt = sf["point"].fillna("").str.extract(r"([-\d.]+)\s+([-\d.]+)")
    sf["lon"] = pd.to_numeric(pt[0], errors="coerce")
    sf["lat"] = pd.to_numeric(pt[1], errors="coerce")
    sf = sf.dropna(subset=["lat", "lon"])
    print(f"  with coordinates: {len(sf):,}")
    st = rail_stations("calgary", cache)
    return union_ring_count(sf, st, FEEDS["calgary"]["crs"]), len(st)


def edmonton(cache: Path):
    print("\n=== Edmonton ===")
    df = pd.read_csv(fetch(SOURCES["edmonton"], cache / "edmonton.csv"),
                     dtype=str, low_memory=False)
    print(f"  rows: {len(df):,}")
    print("  licencetype: " + ", ".join(
        f"{k}={v:,}" for k, v in df["licencetype"].value_counts().items()))
    df = df[df["licencetype"] == EDMONTON_LICENCE_TYPE_KEEP].copy()
    print(f"  Commercial only: {len(df):,} - home occupation is STATED on the "
          f"licence here, as it is in Surrey")
    df["bucket"] = [split_bucket(v, EDMONTON_BUCKETS, ";")
                    for v in df["business_licence_category"]]
    sf = df[df["bucket"].notna()].copy()
    print(f"  storefront: {len(sf):,}   " + ", ".join(
        f"{k}={v:,}" for k, v in sf["bucket"].value_counts().items()))
    sf["lat"] = pd.to_numeric(sf["latitude"], errors="coerce")
    sf["lon"] = pd.to_numeric(sf["longitude"], errors="coerce")
    before = len(sf)
    sf = sf.dropna(subset=["lat", "lon"])
    print(f"  with coordinates: {len(sf):,} of {before:,} "
          f"({len(sf)/before:.1%}) - far better than the 53.3% recorded for "
          f"the whole file, which included the Home Based placeholders")
    st = rail_stations("edmonton", cache)
    return union_ring_count(sf, st, FEEDS["edmonton"]["crs"]), len(st)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None,
                    help="directory for downloads (default: a temp dir). "
                         "Never the working tree - these are raw probes.")
    args = ap.parse_args()
    cache = Path(args.cache) if args.cache else Path(
        __import__("tempfile").mkdtemp(prefix="rank-canada-"))
    print(f"cache: {cache}")

    rows = [("Montreal", *montreal(cache)),
            ("Calgary", *calgary(cache)),
            ("Edmonton", *edmonton(cache))]
    # Measured by the built pipeline rather than re-derived here.
    rows += [("Vancouver (built)", 4129, 20), ("Surrey (built)", 539, 4)]

    print("\n" + "=" * 70)
    print("COMPARABLE: storefronts in the 0.6 mi ring per in-city station")
    print(f"{'city':<22}{'in ring':>10}{'stations':>10}{'per station':>13}"
          f"{'published':>11}")
    published = {"Vancouver (built)": 861, "Surrey (built)": 549,
                 "Montreal": 252, "Edmonton": 153, "Calgary": 103}
    for label, n, s in sorted(rows, key=lambda t: -t[1] / max(t[2], 1)):
        pub = published.get(label)
        rate = n / max(s, 1)
        infl = f"{pub/rate:.1f}x" if pub else ""
        print(f"{label:<22}{n:>10,}{s:>10}{rate:>13.0f}"
              f"{(str(pub) + ' ' + infl) if pub else '-':>11}")
    print(f"{'Toronto':<22}{'-':>10}{234:>10}{41:>13}{'41 1.0x':>11}")
    print("\nFor scale, storefront-based: D.C. ~173, Boston ~39.")
    print("The inflation is NOT uniform - that is why the published order "
          "could not be trusted.")


if __name__ == "__main__":
    main()
