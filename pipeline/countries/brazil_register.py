"""Read IBGE's CNEFE 2022 for one Brazilian city: every establishment the
census enumerator identified, classified, placed and privacy-screened.

Shared by every Brazilian city. The city's config supplies `CNEFE_ZIPS` (one
zip per município - a regional page lists several); its step 2 passes the
sanity box and the city polygon. What the printed counts mean:

  * a ROW is one use-type at one address, not one business - a shopping
    centre is one row or a few (accepted and disclosed, 2026-09-23);
  * a row no rule classifies is DROPPED, never guessed - and the share dropped
    is higher in affluent districts, so those are under-drawn. Their points
    (never their text) are kept aside for the city's build check;
  * at an address that also holds a dwelling the pin shows its category,
    never the enumerator's description.
"""
import collections
import csv
import io
import sys
import zipfile

import pandas as pd
import shapely

from pipeline.baseline import emit
from pipeline.countries import brazil as BR
from pipeline.taxonomies import brazil_cnefe as TAX
from pipeline.taxonomies import filter_to_storefront

SYSTEM = "brazil_cnefe"
DROPPED_LABELS = ("unmatched", "catch-all")


def _rows(zips):
    for path in zips:
        if not path.exists():
            sys.exit(f"Missing {path}. Run the city's fetch_sources.py first.")
        z = zipfile.ZipFile(path)
        members = [i for i in z.infolist() if i.filename.lower().endswith(".csv")]
        if len(members) != 1:
            sys.exit(f"{path.name}: expected one CSV member, found "
                     f"{[m.filename for m in members]}")
        with z.open(members[0]) as raw:
            f = io.TextIOWrapper(raw, encoding=BR.CSV_ENCODING, newline="")
            yield from csv.DictReader(f, delimiter=BR.CSV_DELIMITER)


def _place(df, bbox, polygon, what):
    """Coordinate level, sanity box, city polygon - each drop printed."""
    before = len(df)
    by_level = df["nv_geo_coord"].value_counts().sort_index()
    df = df[df["nv_geo_coord"].isin(BR.COORD_LEVELS_KEEP)]
    print(f"  {what}: coordinate levels {({k: int(v) for k, v in by_level.items()})}; "
          f"{before - len(df):,} outside levels {'/'.join(BR.COORD_LEVELS_KEEP)} dropped")
    df = df.assign(latitude=pd.to_numeric(df["latitude"], errors="coerce"),
                   longitude=pd.to_numeric(df["longitude"], errors="coerce"))
    n = len(df)
    df = df[df["latitude"].between(bbox["lat_min"], bbox["lat_max"])
            & df["longitude"].between(bbox["lon_min"], bbox["lon_max"])]
    print(f"  {what}: {n - len(df):,} dropped on the sanity bounding box")
    n = len(df)
    inside = shapely.contains_xy(polygon, df["longitude"].to_numpy(),
                                 df["latitude"].to_numpy())
    df = df[inside]
    print(f"  {what}: {n - len(df):,} outside the city polygon")
    return df


def build_storefronts(cfg, bbox, polygon):
    """(storefronts, unclassified) DataFrames for one city."""
    home = set()
    kept, dropped = [], []
    labels = collections.Counter()
    rescued = collections.Counter()
    n_rows = 0
    for row in _rows(cfg.CNEFE_ZIPS):
        n_rows += 1
        sp = row["COD_ESPECIE"]
        if sp in BR.ESPECIE_DWELLING:
            home.add(BR.address_key(row))
            continue
        if sp != BR.ESPECIE_ESTABLISHMENT:
            continue
        label, bucket, how = TAX.classify_description(row["DSC_ESTABELECIMENTO"])
        labels[label] += 1
        if how != "rules":
            rescued[(how, label)] += 1
        rec = {"cod_unico_endereco": row["COD_UNICO_ENDERECO"],
               "latitude": row["LATITUDE"], "longitude": row["LONGITUDE"],
               "nv_geo_coord": row["NV_GEO_COORD"].strip()}
        if bucket:
            rec.update(key=BR.address_key(row),
                       description=row["DSC_ESTABELECIMENTO"].strip(),
                       cnefe_category=bucket,
                       estab_indicator=row[BR.ESTAB_INDICATOR].strip())
            kept.append(rec)
        elif label in DROPPED_LABELS:
            rec["label"] = label
            dropped.append(rec)

    n = sum(labels.values())
    print(f"\nCNEFE: {n_rows:,} rows; {n:,} establishment rows (COD_ESPECIE "
          f"{BR.ESPECIE_ESTABLISHMENT}); {len(home):,} addresses holding a dwelling")
    print("  classification (brazil_cnefe; head noun wins, vacancy absolute):")
    for label, c in labels.most_common():
        print(f"      {label:<28} {c:>9,}  {c / n:6.1%}")
    ca = sum(labels[x] for x in DROPPED_LABELS)
    print(f"  mapped to a bucket: {len(kept):,} ({len(kept) / n:.1%}); "
          f"unclassifiable (dropped, not guessed): {ca:,} ({ca / n:.1%})")
    for how in ("edit distance", "version 2"):
        got = {lab: c for (h, lab), c in rescued.most_common() if h == how}
        print(f"  rescued by the {how} pass (rules v{TAX.RULES_VERSION}): "
              f"{sum(got.values()):,} {got}")

    df = pd.DataFrame(kept)
    if df["cod_unico_endereco"].duplicated().any():
        sys.exit("COD_UNICO_ENDERECO repeats among mapped rows - a row is no "
                 "longer one use-type at one address; re-read IBGE's dictionary")
    df["shares_dwelling"] = df["key"].isin(home)
    df = df.drop(columns="key")

    print("\nPlacement:")
    df = _place(df, bbox, polygon, "storefronts")
    unclassified = _place(pd.DataFrame(dropped), bbox, polygon, "unclassified")

    # Privacy (the owner's decision of 2026-09-23): the category, never the
    # description, wherever the address also holds a dwelling.
    named = df["description"].map(lambda d: bool(TAX.person_name_in(TAX.norm(d))))
    print(f"\nPrivacy: {int(df['shares_dwelling'].sum()):,} of {len(df):,} "
          f"({df['shares_dwelling'].mean():.1%}) share an address with a dwelling "
          f"and show their category only")
    print(f"  a first name in the description: {int(named.sum()):,}; of those at a "
          f"dwelling address (hidden): {int((named & df['shares_dwelling']).sum()):,}; "
          f"shown, as a trade name at a non-dwelling address: "
          f"{int((named & ~df['shares_dwelling']).sum()):,}")
    df["business_name"] = df["description"].where(~df["shares_dwelling"],
                                                  df["cnefe_category"])
    df = df.drop(columns="description")

    before = len(df)
    df = filter_to_storefront(df, SYSTEM)
    assert len(df) == before, "every kept row already carries a bucket"
    ind = df["estab_indicator"].value_counts(normalize=True).sort_index()
    print(f"\n  establishments per row: " + ", ".join(
        f"{k or '-'}={v:.1%}" for k, v in ind.items())
        + "  (1 one, 2 two-to-ten, 3 over ten, 4 unknown)")
    for b in TAX.BUCKETS:
        print(f"      {b:<20} {int((df['cnefe_category'] == b).sum()):>9,}")
    # The drift baseline: a re-release of CNEFE, or any change to the rules,
    # moves these, and drift_check.py says so.
    emit("cnefe_rows", n_rows)
    emit("establishment_rows", n)
    emit("mapped_rows", len(kept))
    emit("rescued_version_2", sum(c for (h, _), c in rescued.items() if h == "version 2"))
    emit("storefronts", len(df))
    emit("shares_dwelling", int(df["shares_dwelling"].sum()))
    emit("unclassified_placed", len(unclassified))
    cols = ["cod_unico_endereco", "business_name", "cnefe_category",
            "latitude", "longitude", "shares_dwelling", "nv_geo_coord",
            "estab_indicator"]
    return (df[cols].reset_index(drop=True),
            unclassified[["latitude", "longitude", "label"]].reset_index(drop=True))
