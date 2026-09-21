"""Step 2 - Build New York's storefront business list from FOUR registries.

Input:  data/new_york/raw/dohmh_restaurants.csv          (43nn-pn8j)
        data/new_york/raw/nys_retail_food_stores.csv     (9a8c-vfzj)
        data/new_york/raw/nys_appearance_enhancement.csv (y3u4-jbgh)
        data/new_york/raw/dca_licenses.csv               (w7w3-xahh)
        data/new_york/raw/city_boundary.geojson
Output: data/new_york/processed/businesses_clean.csv

New York has no general business licence, so no single registry answers "what
businesses are here" (see pipeline/taxonomies/new_york.py for the Step 0
evidence). Each source is loaded by its own function, normalised to the same
columns, and tagged with `source`; the taxonomy dispatches on that tag.

Shared columns produced: source, source_key, business_name, business_category,
address, zip, latitude, longitude, coord_status, borough.

Two things this step is careful about:

1. **One row per site, across sources.** A bodega with a food counter holds a
   DOHMH permit AND an NYS retail food licence AND often a DCA tobacco licence.
   Merging on address alone would be wrong in New York, where one address
   routinely holds many distinct storefronts (a mall, a tower, a row of shops
   sharing a number), so the key is address AND a normalised business name.
   That under-merges rather than over-merges - a spelling difference between
   registries leaves two rows - which inflates density slightly instead of
   deleting real businesses. Both numbers are printed so the trade-off stays
   visible.

2. **No registrant names.** The NYS salon registry's `license_holder_name` is
   an individual's name; it is not downloaded (see config.SOURCES) and this
   step asserts it never arrives. Only registered trade names are written.

Rows whose source supplies no coordinates keep coord_status='missing' and are
recovered in step 3 by address geocoding, rather than being dropped - the
add-city skill's rule about never silently losing a large share of rows.

Run:  python pipeline/new_york/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.new_york.config import (  # noqa: E402
    AS_OF_DATE,
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    DOHMH_ACTIVE_WITHIN_DAYS,
    DOHMH_CLOSED_ACTIONS,
    DOHMH_NEVER_INSPECTED,
    NEW_YORK_BBOX,
    NY_STATE_BBOX,
    SOURCES,
    TAXONOMY_SYSTEM,
    SOURCE_ENCODING,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.new_york import (  # noqa: E402
    DCA_ADJUNCT_CATEGORIES,
    NYS_SALON_EXCLUDE_LICENSE_TYPES,
    NYS_SALON_KEEP_LICENSE_TYPES,
    SOURCE_PRIORITY,
    nys_store_label,
)

SHARED_COLUMNS = [
    "source", "source_key", "business_name", "business_category",
    "address", "unit", "zip", "latitude", "longitude", "coord_status", "borough",
]
# `unit` is carried deliberately, and New York is the first city where it is
# worth carrying. San Diego's residence check turned out to be unmeasurable
# because its unit values are bare ("A", "101") with no APT/STE token, so a 0%
# reading there was a measurement gap, not a clean result (DECISIONS.md,
# 2026-09-21). DCA gives a STRUCTURED unit_type - APT, STE, FL, RM as separate
# values - so scripts/check_personal_exposure.py can tell a flat from a
# commercial suite here without guessing from address text.

# Street-name spellings differ between city and state registries, so the dedup
# key normalises the common ones. Applied to whole words only.
_STREET_ABBREV = {
    "AVENUE": "AVE", "AV": "AVE", "STREET": "ST", "ROAD": "RD",
    "BOULEVARD": "BLVD", "BLVD": "BLVD", "PLACE": "PL", "DRIVE": "DR",
    "PARKWAY": "PKWY", "PKY": "PKWY", "TERRACE": "TER", "COURT": "CT",
    "LANE": "LN", "HIGHWAY": "HWY", "TURNPIKE": "TPKE", "EXPRESSWAY": "EXPY",
    "SQUARE": "SQ", "PLAZA": "PLZ", "CIRCLE": "CIR", "BROADWAY": "BROADWAY",
    "EAST": "E", "WEST": "W", "NORTH": "N", "SOUTH": "S",
}
# Corporate suffixes stripped before comparing two registries' names.
_CORP_SUFFIX = re.compile(
    r"\b(INC|INCORPORATED|LLC|L L C|LLP|PLLC|CORP|CORPORATION|CO|COMPANY|"
    r"LTD|LP|THE|AND|&)\b")


def norm_address(value: str) -> str:
    """"1234  East Broadway Ave." -> "1234 E BROADWAY AVE". House numbers keep
    their digits; leading zeros go."""
    text = re.sub(r"[^A-Za-z0-9 ]", " ", str(value or "").upper())
    words = []
    for word in text.split():
        if word.isdigit():
            words.append(word.lstrip("0") or "0")
        else:
            words.append(_STREET_ABBREV.get(word, word))
    return " ".join(words)


def norm_name(value: str) -> str:
    """A business name reduced to its comparable core: "Joe's Pizza, Inc." ->
    "JOESPIZZA"."""
    text = re.sub(r"[^A-Za-z0-9 ]", " ", str(value or "").upper())
    text = _CORP_SUFFIX.sub(" ", text)
    return re.sub(r"[^A-Z0-9]", "", text)


def _finish(df, source, spec, category, name, address, zip_col, lat, lon,
            borough=None, unit=None):
    """Assemble one source's normalised frame."""
    out = pd.DataFrame({
        "source": source,
        "source_key": df[spec["key_column"]].astype(str).str.strip(),
        "business_name": name.fillna("").str.strip(),
        "business_category": category.fillna("").str.strip(),
        "address": address.fillna("").str.strip(),
        "unit": ("" if unit is None else unit.fillna("").str.strip()),
        "zip": zip_col.fillna("").astype(str).str.strip().str.slice(0, 5),
        "latitude": pd.to_numeric(lat, errors="coerce"),
        "longitude": pd.to_numeric(lon, errors="coerce"),
    })
    out["borough"] = "" if borough is None else borough.fillna("").str.strip()
    out["coord_status"] = "source"
    out.loc[out["latitude"].isna() | out["longitude"].isna(), "coord_status"] = "missing"
    return out


def load_dohmh(spec):
    """DOHMH restaurant inspections -> one row per establishment (camis)."""
    df = pd.read_csv(spec["file"], dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"  loaded {len(df):,} inspection rows")

    df["_date"] = pd.to_datetime(df["inspection_date"], errors="coerce")
    real = df[df["_date"] != pd.Timestamp(DOHMH_NEVER_INSPECTED)]
    latest = real.groupby("camis")["_date"].max()
    print(f"  {df['camis'].nunique():,} distinct establishments "
          f"({df['camis'].nunique() - len(latest):,} never inspected, kept)")

    cutoff = pd.Timestamp(AS_OF_DATE) - pd.Timedelta(days=DOHMH_ACTIVE_WITHIN_DAYS)
    stale = set(latest[latest < cutoff].index)
    print(f"  inspection recency: dropping {len(stale):,} establishments whose last "
          f"inspection predates {cutoff.date()} (closed or long gone)")

    # The most recent inspection's action decides whether it was shut.
    last_actions = (
        real.merge(latest.rename("_latest"), on="camis")
        .query("_date == _latest")
        .assign(_action=lambda d: d["action"].fillna("").str.strip().str.upper())
        .groupby("camis")["_action"].apply(set)
    )
    closed = {c for c, actions in last_actions.items()
              if any(any(flag in a for flag in DOHMH_CLOSED_ACTIONS) for a in actions)}
    print(f"  closed at last inspection: dropping {len(closed & set(latest.index) - stale):,} "
          f"more ({len(closed):,} closed overall)")

    drop = stale | closed
    keep = df[~df["camis"].isin(drop)]
    # One row per establishment: the latest row carries the current name/address.
    keep = keep.sort_values(["camis", "_date"]).drop_duplicates("camis", keep="last")
    print(f"  one row per establishment: {len(keep):,} rows")

    address = (keep["building"].fillna("").str.strip() + " "
               + keep["street"].fillna("").str.strip()).str.strip()
    return _finish(keep, "dohmh", spec,
                   category=keep["cuisine_description"],
                   name=keep["dba"], address=address, zip_col=keep["zipcode"],
                   lat=keep["latitude"], lon=keep["longitude"], borough=keep["boro"])


def load_nys_store(spec):
    """NYS Retail Food Stores -> retail food stores in the five boroughs."""
    df = pd.read_csv(spec["file"], dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"  loaded {len(df):,} rows (NYC counties, filtered at download)")

    before = len(df)
    df = df[df["operation_type"].fillna("").str.strip().str.upper() == "STORE"]
    print(f"  operation_type == Store: {before:,} -> {len(df):,} rows")

    before = len(df)
    df = df[df["estab_type"].fillna("").str.upper().str.startswith("A")]
    print(f"  estab_type contains 'A' (Store, Article 28-A): {before:,} -> {len(df):,} rows")

    # georeference is "POINT (lon lat)".
    point = df["georeference"].fillna("").str.extract(
        r"POINT \((-?\d+\.?\d*) (-?\d+\.?\d*)\)")
    address = (df["street_number"].fillna("").str.strip() + " "
               + df["street_name"].fillna("").str.strip()).str.strip()
    name = df["dba_name"].where(df["dba_name"].fillna("").str.strip() != "",
                                df["entity_name"])
    return _finish(df, "nys_store", spec,
                   category=df["estab_type"].map(nys_store_label),
                   name=name, address=address, zip_col=df["zip_code"],
                   lat=point[1], lon=point[0], unit=df["address_line_2"])


def load_nys_salon(spec):
    """NYS appearance-enhancement / barber BUSINESS licences."""
    df = pd.read_csv(spec["file"], dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"  loaded {len(df):,} statewide rows")

    # The registrant's own name must never reach the map.
    assert "license_holder_name" not in df.columns, (
        "license_holder_name was downloaded for the salon registry; it is an "
        "individual's name and must not be. Fix the $select in config.SOURCES.")

    before = len(df)
    kinds = df["license_type"].fillna("").str.strip().str.upper()
    df = df[kinds.isin(NYS_SALON_KEEP_LICENSE_TYPES)]
    print(f"  business licence types only: {before:,} -> {len(df):,} rows "
          f"(dropped {', '.join(sorted(NYS_SALON_EXCLUDE_LICENSE_TYPES))}: "
          "individuals renting space in another licensee's shop)")

    point = df["georeference"].fillna("").str.extract(
        r"POINT \((-?\d+\.?\d*) (-?\d+\.?\d*)\)")
    category = kinds.loc[df.index].map(NYS_SALON_KEEP_LICENSE_TYPES)
    return _finish(df, "nys_salon", spec,
                   category=category, name=df["business_name"],
                   address=df["business_address_1"], zip_col=df["business_zip"],
                   lat=point[1], lon=point[0], unit=df["business_address_2"])


def load_dca(spec):
    """DCWP issued licences -> active premises licences only."""
    df = pd.read_csv(spec["file"], dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"  loaded {len(df):,} rows (Active + Premises, filtered at download)")

    before = len(df)
    df = df[(df["license_status"].fillna("").str.strip() == "Active")
            & (df["license_type"].fillna("").str.strip() == "Premises")]
    print(f"  re-applied Active + Premises (deterministic re-run): {before:,} -> {len(df):,} rows")
    print("  NOTE: license_type == Premises is what excludes DCA's 'Individual' "
          "licences - licences held by a person, often at a home address.")

    address = (df["address_building"].fillna("").str.strip() + " "
               + df["address_street_name"].fillna("").str.strip()).str.strip()
    # business_name is the legal entity name and is populated on every row;
    # dba_trade_name is blank on ~83% and is used only when present.
    dba = df["dba_trade_name"].fillna("").str.strip()
    name = dba.where(dba != "", df["business_name"])
    print(f"  display name: {(dba != '').sum():,} rows use dba_trade_name, "
          f"{(dba == '').sum():,} fall back to business_name (the legal entity name, "
          "never blank in this registry)")
    # unit_type is structured (APT / STE / FL / RM as separate values), which is
    # what makes the residence check in scripts/check_personal_exposure.py
    # measurable for this city - see the SHARED_COLUMNS note.
    unit = (df["unit_type"].fillna("").str.strip() + " "
            + df["apt_suite"].fillna("").str.strip()).str.strip()
    return _finish(df, "dca", spec,
                   category=df["business_category"], name=name,
                   address=address, zip_col=df["address_zip"],
                   lat=df["latitude"], lon=df["longitude"],
                   borough=df["address_borough"], unit=unit)


LOADERS = {
    "dohmh": load_dohmh,
    "nys_store": load_nys_store,
    "nys_salon": load_nys_salon,
    "dca": load_dca,
}


def main():
    missing = [s for s, spec in SOURCES.items() if not spec["file"].exists()]
    if missing:
        sys.exit(f"Missing raw files for {missing}. Run:\n"
                 "  python pipeline/new_york/fetch_sources.py")
    if not CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"No boundary file at {CITY_BOUNDARY_GEOJSON}; see config.py.")

    frames = []
    for source in SOURCES:
        print(f"\n=== {source} ===")
        frame = LOADERS[source](SOURCES[source])
        frame = frame[SHARED_COLUMNS]
        print(f"  -> {len(frame):,} normalised rows "
              f"({(frame['coord_status'] == 'missing').sum():,} without coordinates)")
        frames.append(frame)

    df = pd.concat(frames, ignore_index=True)
    print(f"\n=== combined ===\n{len(df):,} rows from {len(frames)} registries")

    # --- Storefront categories (dispatches on `source`) ----------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"Storefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")
    for source in SOURCES:
        print(f"  {source}: {(df['source'] == source).sum():,} rows")

    # --- A name is required to display anything ------------------------------
    before = len(df)
    df = df[df["business_name"].str.strip() != ""]
    print(f"Has a business name: {before:,} -> {len(df):,} rows")

    # --- Coordinate sanity: two different problems, two treatments -----------
    # An out-of-city coordinate is either a business that is genuinely
    # somewhere else (the NYS registries are statewide) or a New York business
    # with a broken coordinate. Telling them apart is what NY_STATE_BBOX is
    # for; see the note there. Conflating them would either delete real
    # storefronts or geocode 16k upstate salons.
    b, state = NEW_YORK_BBOX, NY_STATE_BBOX
    has_coords = df["coord_status"] == "source"
    in_city_box = (df["latitude"].between(b["lat_min"], b["lat_max"])
                   & df["longitude"].between(b["lon_min"], b["lon_max"]))
    in_state = (df["latitude"].between(state["lat_min"], state["lat_max"])
                & df["longitude"].between(state["lon_min"], state["lon_max"]))

    elsewhere = has_coords & ~in_city_box & in_state
    if elsewhere.any():
        print(f"\nOut of scope: dropping {int(elsewhere.sum()):,} rows located "
              "elsewhere in New York State (the two NYS registries are statewide "
              "and carry no NYC marker of their own)")
        for source in SOURCES:
            n = int((elsewhere & (df["source"] == source)).sum())
            if n:
                print(f"  {source}: {n:,}")
        df = df[~elsewhere]

    corrupt = (df["coord_status"] == "source") & ~(
        df["latitude"].between(b["lat_min"], b["lat_max"])
        & df["longitude"].between(b["lon_min"], b["lon_max"]))
    if corrupt.any():
        null_island = int(((df.loc[corrupt, "latitude"].abs() < 0.01)
                           & (df.loc[corrupt, "longitude"].abs() < 0.01)).sum())
        print(f"Corrupt coordinates: blanking {int(corrupt.sum()):,} rows that are "
              f"not valid New York points at all ({null_island:,} at exactly (0,0)) "
              "for step 3 to recover by address")
        df.loc[corrupt, ["latitude", "longitude"]] = pd.NA
        df.loc[corrupt, "coord_status"] = "missing"

    print(f"Coordinates: {int((df['coord_status'] == 'source').sum()):,} from source, "
          f"{int((df['coord_status'] == 'missing').sum()):,} to geocode in step 3")

    # --- One row per site, across sources ------------------------------------
    df["_addr_key"] = (df["address"].map(norm_address) + "|" + df["zip"])
    df["_name_key"] = df["business_name"].map(norm_name)
    df["_site_key"] = df["_addr_key"] + "|" + df["_name_key"]

    # What address-only merging would have done, for the record.
    addr_only = len(df) - df["_addr_key"].nunique()
    print(f"\nDedup: {addr_only:,} rows share an address with another row - "
          "NOT merged on address alone (one New York address routinely holds "
          "several distinct storefronts)")

    rank = {s: i for i, s in enumerate(SOURCE_PRIORITY)}
    df["_src_rank"] = df["source"].map(rank).fillna(len(rank)).astype(int)
    # A DCA adjunct licence (tobacco, e-cigarette, stoop line stand) is a
    # permission a business holds, not the business, so it loses to anything
    # else at the same site.
    df["_adjunct"] = (
        (df["source"] == "dca")
        & df["business_category"].str.upper().isin(DCA_ADJUNCT_CATEGORIES)
    ).astype(int)

    before = len(df)
    df = (df.sort_values(["_site_key", "_adjunct", "_src_rank", "source_key"])
            .drop_duplicates("_site_key"))
    print(f"One row per site (address + business name): {before:,} -> {len(df):,} rows")
    for source in SOURCES:
        print(f"  {source}: {(df['source'] == source).sum():,} rows survive")

    # --- Boundary filter, for rows that have coordinates now -----------------
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                else boundary.to_crs(CRS_GEOGRAPHIC))
    city = boundary.geometry.union_all()
    located = df[df["coord_status"] == "source"]
    pts = gpd.GeoSeries(
        gpd.points_from_xy(located["longitude"], located["latitude"]),
        crs=CRS_GEOGRAPHIC, index=located.index)
    outside = located.index[~pts.within(city).values]
    before = len(df)
    df = df.drop(index=outside)
    print(f"\nInside the five boroughs: {before:,} -> {len(df):,} rows "
          f"({len(outside):,} located outside the city, dropped)")
    print("  (the statewide NYS registries have no NYC marker of their own, so "
          "this polygon test is what scopes them)")

    df = (df[SHARED_COLUMNS]
          .sort_values(["source", "source_key"])
          .reset_index(drop=True))
    df["record_id"] = df.index.astype(str)

    print("\nBy bucket:")
    taxonomy = load_taxonomy_module(TAXONOMY_SYSTEM)
    buckets = [taxonomy.classify({"business_category": c, "source": s})
               for c, s in zip(df["business_category"], df["source"])]
    print(pd.Series(buckets).value_counts().to_string())

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")
    print(f"{int((df['coord_status'] == 'missing').sum()):,} rows still need "
          "coordinates - run step3_geocode.py next.")


if __name__ == "__main__":
    main()
