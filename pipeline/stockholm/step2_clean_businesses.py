"""Stockholm step 2: the food inspection register (one row per inspection) ->
one row per premises -> the food storefronts placed inside Stockholms kommun.

    python pipeline/stockholm/step2_clean_businesses.py

Reads the cache only (pipeline/stockholm/fetch_sources.py downloads). What a
reader should know before trusting the counts printed below:

  * the register is INSPECTIONS: a premises (ObjektId) is its LATEST record by
    TillsynsDatum, for name, address and position; its types are every type
    any of its records carries, joined with " | ";
  * the inspection text (Beskrivning, Anmarkning, Nr, Typ, Kontrollorsak,
    Kontrollomrade) is never read;
  * an untyped premises (not inspected since the type field arrived in 2024)
    goes on only when the taxonomy's name rules call it a storefront AND it
    was last inspected in config.NAME_CLASSIFIED_YEARS (owner, 2026-09-28),
    flagged `name_classified`;
  * a type the taxonomy does not know stops the step.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.stockholm import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
READ = ["OBJECTID", "ObjektId", "AnlaggningsNamn", "Fastighet", "Adress", "AnlaggningsTyp",
        "GeoPositionNorr", "GeoPositionOst", "Riskklass", "VerksamhetsTyp", "TillsynsDatum",
        "longitude", "latitude"]
NEVER_READ = ("Beskrivning", "Anmarkning", "Nr", "Typ", "Kontrollorsak", "Kontrollomrade")


def premises(df):
    """One row per ObjektId: the latest record, with every type it has had."""
    df = df.sort_values(["ObjektId", "TillsynsDatum", "OBJECTID"])
    types = (df.dropna(subset=["VerksamhetsTyp"]).groupby("ObjektId")["VerksamhetsTyp"]
             .agg(lambda s: TAX.SEPARATOR.join(sorted(set(s)))))
    p = df.groupby("ObjektId").tail(1).set_index("ObjektId")
    p["types"] = types.reindex(p.index).fillna("")
    return p.reset_index()


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}: run python pipeline/stockholm/fetch_sources.py")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(config.REGISTER_CSV, usecols=READ, dtype=str, encoding="utf-8")
    assert not set(NEVER_READ) & set(df.columns)
    print(f"  {len(df):,} inspection rows, {df['ObjektId'].nunique():,} premises (ObjektId); "
          f"inspections {df['TillsynsDatum'].min()[:10]} to {df['TillsynsDatum'].max()[:10]}")

    seen = sorted({t for t in df["VerksamhetsTyp"].dropna().unique()})
    print("  types: " + "; ".join(f"{t} {n:,}" for t, n in df["VerksamhetsTyp"].value_counts().items()))
    unknown = sorted(set(seen) - TAX.KNOWN_TYPES)
    if unknown:
        sys.exit(f"  type(s) the taxonomy does not know: {unknown}")

    p = premises(df)
    p["last_year"] = p["TillsynsDatum"].str[:4]
    p["business_name"] = p["AnlaggningsNamn"].fillna("").str.strip()
    typed = p["types"] != ""
    print(f"\n  {len(p):,} premises: typed {int(typed.sum()):,}, untyped {int((~typed).sum()):,}")
    print("    by type combination: " + "; ".join(
        f"{t or '(none)'} {n:,}" for t, n in p["types"].value_counts().items()))

    # Untyped: the name rules, only for the years the owner accepted.
    by_name = p["business_name"].map(TAX.name_bucket)
    p["name_classified"] = (~typed) & by_name.notna() & p["last_year"].isin(config.NAME_CLASSIFIED_YEARS)
    print(f"    untyped and a storefront by name: {int(((~typed) & by_name.notna()).sum()):,}, "
          f"of which last inspected in {'/'.join(config.NAME_CLASSIFIED_YEARS)}: "
          f"{int(p['name_classified'].sum()):,}")
    p.loc[p["name_classified"], "types"] = TAX.NAME_CLASSIFIED_VALUE
    p[TAX.VALUE_COLUMN] = p["types"]

    typed_store = typed & p["types"].str.split(r" \| ").map(
        lambda ts: any(t in TAX.TYPE_TO_BUCKET for t in ts))
    by_rule = pd.Series([TAX.classify({TAX.VALUE_COLUMN: v, "business_name": n})
                         for v, n in zip(p["types"], p["business_name"])], index=p.index)
    named_out = typed_store & by_rule.isna()
    print(f"    typed storefronts {int(typed_store.sum()):,}; excluded by name (an institutional "
          f"kitchen, or a pharmacy): {int(named_out.sum()):,}")
    p = filter_to_storefront(p, config.TAXONOMY_SYSTEM)
    print(f"  {len(p):,} storefront premises after filter_to_storefront()")

    lat = pd.to_numeric(p["latitude"], errors="coerce")
    lon = pd.to_numeric(p["longitude"], errors="coerce")
    p = p.assign(latitude=lat, longitude=lon)
    no_point = p["latitude"].isna() | p["longitude"].isna()
    print(f"  {int(no_point.sum()):,} without a position, NOT placed ({no_point.mean():.1%})")
    p = p[~no_point].copy()

    # Control: the served point against the register's own SWEREF 99 18 00.
    n, e = pd.to_numeric(p["GeoPositionNorr"], errors="coerce"), pd.to_numeric(p["GeoPositionOst"], errors="coerce")
    both = n.notna() & e.notna()
    to_m = Transformer.from_crs(config.REGISTER_POSITION_CRS, config.CRS_PROJECTED, always_xy=True)
    to_m2 = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    ax, ay = to_m.transform(e[both].values, n[both].values)
    bx, by = to_m2.transform(p["longitude"][both].values, p["latitude"][both].values)
    d = ((pd.Series(ax) - pd.Series(bx)) ** 2 + (pd.Series(ay) - pd.Series(by)) ** 2) ** 0.5
    print(f"  point vs SWEREF 99 18 00 position, {int(both.sum()):,} premises: median {d.median():.2f} m, "
          f"max {d.max():.1f} m, over 10 m {int((d > 10).sum())}")

    box = config.STOCKHOLM_BBOX
    in_box = p["latitude"].between(box["lat_min"], box["lat_max"]) & \
        p["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    p = p[in_box]
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(p["longitude"], p["latitude"]), index=p.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(city)
    print(f"  {int((~inside).sum()):,} outside Stockholms kommun, dropped")
    p = p[inside]

    out = p.rename(columns={"ObjektId": "objekt_id", "TillsynsDatum": "last_inspected"})[
        ["objekt_id", "business_name", "latitude", "longitude", TAX.VALUE_COLUMN,
         "name_classified", "last_inspected"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    bucket = [TAX.classify(dict(zip([TAX.VALUE_COLUMN, *TAX.EXTRA_COLUMNS], v)))
              for v in zip(out[TAX.VALUE_COLUMN], out["business_name"], out["name_classified"])]
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)} "
          f"({int(out['name_classified'].sum()):,} classified from the name)")
    print("    " + ", ".join(f"{TAX.legend_label(b)} {n:,}" for b, n in pd.Series(bucket).value_counts().items()))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
