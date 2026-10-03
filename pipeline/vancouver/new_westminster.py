"""New Westminster leg of Vancouver (Regional): resident business licences
placed by an address join to the City's own address points.

Sources (both City of New Westminster, ArcGIS Online org A7O8YnTNtzRPIn7T):
- BUSINESS_LICENSES_(RESIDENTS)/FeatureServer/0, a table with no geometry.
- Address_Point/FeatureServer/0, 42,690 points, fetched with outSR=4326.
Downloaded by pipeline/vancouver/fetch_sources.py; this module never fetches.

Licence: "Contains information licenced under the Open Government Licence -
City of New Westminster."

Join (measured 2026-10-03 on the 2026-09-27 edit; re-measure if either layer
is re-published):
- Tier 1, exact: the first line of CIVIC_ADDRESS equals an address point's
  ADDRESS, unit included. No case or whitespace folding was needed: both
  layers come from the same City address system (0 rows with stray spacing
  or lower case). 846 of 856 bucketed rows.
- Tier 2, unit dropped: the unit prefix ("217C-", "107-") is removed and
  HOUSE + STREET is matched; the unit is missing from the address file but
  the building is not. 8 rows, every key a single location.
- Unmatched: 2 rows (one civic number absent from the address file, one
  "FRONT ST PARKADE" with no civic number). Dropped and listed.
No street-suffix or directional normalisation is applied: no miss called for
one. No fuzzy matching, ever (address-join skill).

Duplicate keys in the address file: units of one building usually share one
coordinate. A key at several points is placed at their centroid only when
the points lie within DUPLICATE_SPREAD_M of each other; a wider key is
dropped as ambiguous and listed, never resolved by picking one point.
"""
import re

import numpy as np
import pandas as pd
from pyproj import Transformer

SOURCE = "new_westminster"
FORBIDDEN = {"LICENCEE_NAME", "MAILING_ADDRESS"}
# Units of one building share a coordinate; 5 m allows for rounding only.
DUPLICATE_SPREAD_M = 5.0
# One licence may cover adjacent civic numbers (one shop at 944 and 946
# TWELFTH ST); its rows collapse to one pin only when this close.
SAME_LICENCE_SPREAD_M = 30.0
CRS_PROJECTED = "EPSG:32610"   # UTM 10N, the Vancouver build's projected CRS
APPROVED_YEARS = {"2025", "2026"}

UNIT_RX = re.compile(r"^(?:(?P<unit>.+)-)?(?P<house>\d+)\s+(?P<street>.+)$")
OUT = ["source", "key", "business_name", "address", "category",
       "category_label", "latitude", "longitude", "_used_fallback"]


def _first_line(s):
    return str(s or "").splitlines()[0].strip() if str(s or "").strip() else ""


def _base_key(line):
    m = UNIT_RX.match(line)
    return f"{m['house']} {m['street']}" if m else None


def _resolve(points, key_col, xy):
    """One coordinate per key: centroid when the key's points lie within
    DUPLICATE_SPREAD_M, otherwise flagged ambiguous."""
    df = pd.DataFrame({"k": points[key_col].values, "x": xy[0], "y": xy[1],
                       "lon": points["lon"].values, "lat": points["lat"].values})
    g = df.groupby("k").agg(n=("x", "size"), x0=("x", "min"), x1=("x", "max"),
                            y0=("y", "min"), y1=("y", "max"),
                            lon=("lon", "mean"), lat=("lat", "mean"))
    g["spread"] = np.hypot(g.x1 - g.x0, g.y1 - g.y0)
    g["ambiguous"] = g.spread > DUPLICATE_SPREAD_M
    return g[["n", "spread", "ambiguous", "lon", "lat"]]


def load_new_westminster(licences_csv, points_csv, classify):
    lic = pd.read_csv(licences_csv, dtype=str, keep_default_na=False)
    leaked = FORBIDDEN & set(lic.columns)
    assert not leaked, f"forbidden columns in the licence cache: {sorted(leaked)}"
    pts = pd.read_csv(points_csv, dtype={"ADDRESS": str, "STREET": str,
                                         "UNIT": str})
    print(f"\nNew Westminster: {len(lic):,} licence rows, "
          f"{len(pts):,} address points")

    # Resident filter. The layer is the residents' extract, so this is a
    # guard that should drop nothing.
    before = len(lic)
    lic = lic[lic.RESIDENT_STATUS.str.strip().str.upper() != "NON-RESIDENT"]
    print(f"  resident: {before:,} -> {len(lic):,}")

    # Current-licence filter. Every row is LICENCE_STATE APPROVED; approvals
    # run 2025-11-18 (the bulk renewal for the 2026 licence year, 2,463 rows)
    # to 2026-09. Kept: APPROVED with an approval date in 2025 or 2026. A row
    # approved earlier, or with an unparseable date, would be a lapsed or
    # broken licence and is dropped.
    before = len(lic)
    approved = pd.to_datetime(lic.APPROVED_DATE, format="%Y%m%d", errors="coerce")
    ok = (lic.LICENCE_STATE.str.strip().str.upper() == "APPROVED") & \
        approved.dt.year.astype("Int64").astype(str).isin(APPROVED_YEARS)
    lic = lic[ok.values].copy()
    print(f"  approved 2025-2026: {before:,} -> {len(lic):,} "
          f"(approval dates {approved[ok].min():%Y-%m-%d} to "
          f"{approved[ok].max():%Y-%m-%d})")

    lic["category"] = lic.NAICS_CODE.str.strip()
    lic["bucket"] = [classify(c) if c else None for c in lic.category]
    lic = lic[lic.bucket.notna()].copy()
    print(f"  bucketed: {len(lic):,} ("
          + ", ".join(f"{b}={n:,}" for b, n in lic.bucket.value_counts().items())
          + ")")

    # Keys into the address file.
    t = Transformer.from_crs("EPSG:4326", CRS_PROJECTED, always_xy=True)
    pts["lon"] = pd.to_numeric(pts.lon)
    pts["lat"] = pd.to_numeric(pts.lat)
    xy = t.transform(pts.lon.values, pts.lat.values)
    pts["exact"] = pts.ADDRESS.str.strip()
    pts["base"] = (pd.to_numeric(pts.HOUSE).astype("Int64").astype(str) + " "
                   + pts.STREET.str.strip())
    ex = _resolve(pts, "exact", xy)
    bs = _resolve(pts, "base", xy)
    print(f"  address file: {int((ex.n > 1).sum())} full addresses at more "
          f"than one point ({int(ex.ambiguous.sum())} spread over "
          f"{DUPLICATE_SPREAD_M:g} m); {int((bs.n > 1).sum()):,} "
          f"house+street keys at more than one point "
          f"({int(bs.ambiguous.sum())} spread over {DUPLICATE_SPREAD_M:g} m)")

    lic["line1"] = lic.CIVIC_ADDRESS.map(_first_line)
    lic["base"] = lic.line1.map(_base_key)
    tier, lon, lat = [], [], []
    for line, base in zip(lic.line1, lic.base):
        if line in ex.index:
            r, name = ex.loc[line], "exact"
        elif base is not None and base in bs.index:
            r, name = bs.loc[base], "unit dropped"
        else:
            tier.append("unmatched"); lon.append(np.nan); lat.append(np.nan)
            continue
        if r.ambiguous:
            tier.append(f"ambiguous ({name})"); lon.append(np.nan); lat.append(np.nan)
            continue
        tier.append(name); lon.append(r.lon); lat.append(r.lat)
    lic["tier"], lic["longitude"], lic["latitude"] = tier, lon, lat

    n = len(lic)
    print("  join tiers:")
    for name in ["exact", "unit dropped", "ambiguous (exact)",
                 "ambiguous (unit dropped)", "unmatched"]:
        k = int((lic.tier == name).sum())
        if k or name in ("exact", "unit dropped", "unmatched"):
            print(f"    {name:<26}{k:>5}  ({k / n:.1%})")
    miss = lic[lic.latitude.isna()]
    for a, c, tr in zip(miss.line1, miss.category, miss.tier):
        print(f"    dropped [{tr}]: {a} | NAICS {c}")
    lic = lic[lic.latitude.notna()].copy()

    # One licence number can cover adjacent civic numbers. Collapse to one
    # row at the centroid when its points are close; otherwise stop.
    dup = lic[lic.LICENCE.duplicated(keep=False)]
    keep = lic[~lic.LICENCE.duplicated(keep=False)]
    merged = []
    for key, grp in dup.groupby("LICENCE", sort=False):
        gx, gy = t.transform(grp.longitude.values, grp.latitude.values)
        spread = float(np.hypot(np.ptp(gx), np.ptp(gy)))
        if spread > SAME_LICENCE_SPREAD_M or grp.category.nunique() > 1:
            raise SystemExit(f"licence {key}: {len(grp)} rows {spread:.0f} m "
                             f"apart or with different codes; decide by hand")
        row = grp.sort_values("ObjectId", key=lambda s: s.astype(int)).iloc[0].copy()
        row["line1"] = " / ".join(grp.line1)
        row["longitude"], row["latitude"] = grp.longitude.mean(), grp.latitude.mean()
        merged.append(row)
        print(f"  licence {key}: {len(grp)} addresses {spread:.0f} m apart "
              f"collapsed to one pin ({row['line1']})")
    if merged:
        lic = pd.concat([keep, pd.DataFrame(merged)], ignore_index=True)
    assert lic.LICENCE.is_unique

    # Postal-code control: the licence's second line against the matched
    # point's own postal code, on the exact tier.
    pc = lic.CIVIC_ADDRESS.str.extract(r"([A-Z]\d[A-Z] ?\d[A-Z]\d)\s*$")[0]
    ap_pc = pts.drop_duplicates("exact").set_index("exact").POSTAL_CODE
    on_exact = lic.tier == "exact"
    a = pc[on_exact].fillna("").str.replace(" ", "")
    b = lic.line1[on_exact].map(ap_pc).fillna("").str.replace(" ", "")
    both = (a != "") & (b != "")
    print(f"  postal-code control (exact tier, {int(on_exact.sum())} rows): "
          f"{int((both & (a == b)).sum())} agree, "
          f"{int((both & (a != b)).sum())} conflict, "
          f"{int((~both).sum())} with a postal code missing on one side")

    out = pd.DataFrame({
        "source": SOURCE,
        "key": lic.LICENCE.str.strip(),
        # BUSINESS_NAME is the name the licence is issued under. A sole
        # proprietor with no trade name is published under their own name;
        # see looks_personal in the report.
        "business_name": lic.BUSINESS_NAME.str.strip(),
        "address": lic.line1,
        # Shown in the tooltip as "NAICS <code>", as Los Angeles (Regional) does.
        "category": "NAICS " + lic.category,
        "category_label": lic.NAICS_DESCRIPTION.str.strip(),
        "latitude": lic.latitude.astype(float),
        "longitude": lic.longitude.astype(float),
        # LICENCEE_NAME is never fetched, so there is no fallback name.
        "_used_fallback": False,
    })
    print(f"  placed: {len(out):,}")
    return out[OUT].reset_index(drop=True)
