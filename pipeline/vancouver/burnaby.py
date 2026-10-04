"""Burnaby's business licences, filtered and classified for Vancouver (Regional).

Source: gis.burnaby.ca OpenData/OpenData1/MapServer/17 "Business Licences",
downloaded by pipeline/vancouver/fetch_sources.py to
data/burnaby/raw/burnaby_business_licences.csv.
ACCOUNT_NAME (the holder's own name) is never fetched, so the only name is
TRADE_NAME and there is no fallback. LEGAL_TYPE is the property's legal type
(LAND, STRATA), not a business form, and is not read.
"""

import pandas as pd

COLUMNS = ["source", "key", "business_name", "address", "category",
           "latitude", "longitude", "_used_fallback"]

# Most specific first: one licence at one point keeps the first bucket here.
# Same order as pipeline/taxonomies/vancouver.py BUCKET_PRIORITY.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]

# The placeholder point is located by coordinate at 7 decimal places (about
# 1 cm), which absorbs float noise in the CSV round trip.
_COORD_DP = 7


def _clean(series):
    return series.fillna("").astype(str).str.strip()


def _address(df):
    parts = _clean(df["HOUSE"]) + " " + _clean(df["STREET"]) + " " + _clean(df["UNIT"])
    return parts.str.replace(r"\s+", " ", regex=True).str.strip()


def find_placeholder(df):
    """The most repeated point in the whole layer and its row count.

    Measured 2026-10-02: 2,179 rows (contractors, mobile businesses, food
    peddlers) at one point, addressed BUSINESS - NON RESIDENT or LICENSING -
    UNKNOWN. The next busiest point holds 337 rows (a mall).
    """
    pts = pd.DataFrame({"lat": df["lat"].round(_COORD_DP),
                        "lon": df["lon"].round(_COORD_DP)})
    counts = pts.value_counts()
    (lat, lon), n = counts.index[0], int(counts.iloc[0])
    return lat, lon, n


def load_burnaby(csv_path, classify):
    """Return the bucketed Burnaby rows in the shared multi-source shape.

    `classify` takes a LICENCE_TYPE_NAME string and returns a bucket or None.
    """
    raw = pd.read_csv(csv_path, dtype=str)
    print(f"Burnaby: {len(raw):,} rows read, "
          f"{raw['LICENCE_TYPE_NAME'].nunique()} licence types")
    raw["lat"] = pd.to_numeric(raw["lat"], errors="coerce")
    raw["lon"] = pd.to_numeric(raw["lon"], errors="coerce")

    ph_lat, ph_lon, ph_n = find_placeholder(raw)
    print(f"  placeholder point: {ph_lat}, {ph_lon} holds {ph_n:,} rows")

    raw["bucket"] = _clean(raw["LICENCE_TYPE_NAME"]).map(classify)
    kept = raw[raw["bucket"].notna()].copy()
    print(f"  in a bucket: {len(kept):,} rows "
          f"{kept['bucket'].value_counts().to_dict()}")

    no_point = kept["lat"].isna() | kept["lon"].isna()
    if no_point.any():
        print(f"  dropped with no point: {int(no_point.sum()):,}")
    kept = kept[~no_point]

    # One licence at one point: keep the highest-priority bucket.
    kept["_rank"] = kept["bucket"].map(BUCKET_PRIORITY.index)
    kept["_plat"] = kept["lat"].round(_COORD_DP)
    kept["_plon"] = kept["lon"].round(_COORD_DP)
    before = len(kept)
    kept = (kept.sort_values(["_rank", "OBJECTID"])
                .drop_duplicates(["LICENCE_NUMBER", "_plat", "_plon"], keep="first"))
    print(f"  de-duplicated on licence and point: {before:,} -> {len(kept):,} "
          f"{kept['bucket'].value_counts().to_dict()}")

    on_ph = (kept["_plat"] == ph_lat) & (kept["_plon"] == ph_lon)
    assert not on_ph.any(), (
        f"{int(on_ph.sum())} bucketed rows sit on the placeholder point "
        f"{ph_lat}, {ph_lon}; their types: "
        f"{kept.loc[on_ph, 'LICENCE_TYPE_NAME'].value_counts().to_dict()}")
    print("  bucketed rows on the placeholder point: 0")

    out = pd.DataFrame({
        "source": "burnaby",
        "key": _clean(kept["LICENCE_NUMBER"]),
        "business_name": _clean(kept["TRADE_NAME"]),
        "address": _address(kept),
        "category": _clean(kept["LICENCE_TYPE_NAME"]),
        "latitude": kept["lat"],
        "longitude": kept["lon"],
        "_used_fallback": False,
    })[COLUMNS].reset_index(drop=True)
    blank = (out["business_name"] == "").sum()
    print(f"  blank trade names: {blank}")
    print(f"Burnaby: {len(out):,} rows returned")
    return out
