"""Milan step 2: six registers -> one storefront table.

Reads the cache and NEVER fetches.

    python pipeline/milan/step2_clean_businesses.py

Three things are unusual and all three are measured, not assumed:

  1. NO CROSS-SOURCE DEDUPLICATION. The six are disjoint registers (`Codice`
     unique within each, zero collisions between any pair), address cannot be
     a key (15,613 of 28,131 `vicinato` rows already share one), and `insegna`
     is too sparse to merge on. See config.SOURCES.
  2. THE BUCKET IS THE REGISTER. Every in-dataset classification field is
     26-64% blank or corrupted by concatenation; `Area di Competenza` is the
     only clean one and it names the register.
  3. NO REGISTER CARRIES A PERSONAL NAME, so the name fallback is an address
     and Los Angeles' failure mode cannot occur.
"""
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.milan import config
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module
from pipeline.taxonomies import milan_source as _tax

PERSONAL_HINTS = ("nome", "cognome", "titolare", "proprietar", "legale",
                  "rappresentante", "ragione", "nominativo", "codice_fiscale")


def load_source(key, spec):
    path = config.DATA_RAW / f"{key}.json"
    if not path.exists():
        sys.exit(f"missing {path}.\nRun: python pipeline/milan/fetch_sources.py")
    df = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))

    # ASSERTED, not assumed: no register may carry a personal name. If a
    # refresh ever adds one, this build stops rather than quietly publishing
    # people - the structural form of the check, as for Dublin.
    flagged = [c for c in df.columns
               if any(h in c.lower() for h in PERSONAL_HINTS)]
    if flagged:
        sys.exit(f"  {key} NOW CARRIES {flagged}. Milan's privacy position is "
                 f"that no register has a personal-name column; this must be "
                 f"re-decided before the build proceeds.")

    n0 = len(df)
    # `fuori piano` licenses premises OUTSIDE the commercial plan, and at least
    # 15.9% is not a public storefront. 15.9% IS A FLOOR: the clause column is
    # 62.4% blank, so this filter cannot be complete and the page says so.
    if key == "pe_fuori_piano":
        hay = (df.get("settore_storico_pe", "").astype(str) + " "
               + df.get("fuori_piano", "").astype(str)).str.lower()
        drop = hay.str.contains("|".join(config.FUORI_PIANO_EXCLUDE), na=False)
        df = df[~drop]
        print(f"    not-a-public-storefront filter: {n0:,} -> {len(df):,} "
              f"({int(drop.sum())} canteens, clubs and parish halls)")

    lon = pd.to_numeric(df.get("LONG_X_4326"), errors="coerce")
    lat = pd.to_numeric(df.get("LAT_Y_4326"), errors="coerce")
    n1 = len(df)
    ok = lon.notna() & lat.notna() & (lon != 0) & (lat != 0)
    df, lon, lat = df[ok], lon[ok], lat[ok]

    name_col = spec["name_col"]
    name = (df[name_col].astype(str).str.strip()
            if name_col and name_col in df.columns
            else pd.Series([""] * len(df), index=df.index))
    name = name.replace({"None": "", "nan": ""})
    fallback = df[config.NAME_FALLBACK_COLUMN].astype(str).str.strip()
    used_name = int((name != "").sum())

    out = pd.DataFrame({
        "business_name": name.where(name != "", fallback),
        "latitude": lat,
        "longitude": lon,
        "attivita": ([_tax.activity_label(key, v, spec["label_fallback"])
                      for v in df[spec["label_col"]]]
                     if spec["label_col"] in df.columns
                     else [spec["label_fallback"]] * len(df)),
        "source": key,
        "codice": df["Codice"].astype(str),
        "has_sign": (name != "").to_numpy(),
    })
    print(f"  {key:18s} {n0:6,} -> {len(out):6,}  "
          f"({n1 - len(out)} without usable coordinates) | "
          f"trade name on {used_name:,} ({used_name/max(len(out),1)*100:4.1f}%)")
    return out


def main():
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    # The config and the taxonomy each name a bucket per register. Asserted so
    # they cannot drift into disagreeing silently.
    assert {k: v["bucket"] for k, v in config.SOURCES.items()} \
        == tax.SOURCE_BUCKETS, "config.SOURCES and the taxonomy disagree"

    print("Registers:")
    frames = [load_source(k, s) for k, s in config.SOURCES.items()]
    df = pd.concat(frames, ignore_index=True)
    print(f"\nCombined: {len(df):,} rows")

    # `Codice` is unique WITHIN a register and never collides BETWEEN them, so
    # this asserts rather than drops - a duplicate here would mean a register
    # changed shape.
    dupes = int(df["codice"].duplicated().sum())
    if dupes:
        sys.exit(f"  {dupes} duplicate Codice across the six registers. They "
                 f"were measured disjoint on 2026-09-22; re-check before "
                 f"assuming a dedup is wanted.")
    print("  Codice is unique across all six (asserted, not deduplicated)")

    n = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"Storefront filter: {n:,} -> {len(df):,}")

    b = config.MILAN_BBOX
    n = len(df)
    df = df[df["latitude"].between(b["lat_min"], b["lat_max"])
            & df["longitude"].between(b["lon_min"], b["lon_max"])]
    print(f"Bounds check: {n:,} -> {len(df):,}")

    boundary = json.loads(config.BOUNDARY_GEOJSON.read_text(encoding="utf-8"))
    region = gpd.GeoDataFrame.from_features(boundary["features"],
                                            crs=config.CRS_GEOGRAPHIC)
    one = region.geometry.union_all()
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs=config.CRS_GEOGRAPHIC)
    n = len(gdf)
    gdf = gdf[gdf.geometry.within(one)]
    print(f"Inside the comune boundary: {n:,} -> {len(gdf):,}")

    # THE RATE THE PAGE QUOTES. The per-register lines above are not it: the
    # page said "about a fifth" until 2026-09-23 while this measured 15.3%,
    # because three registers carry no name field at all and only the
    # per-register rates (17.7% on the largest) were ever printed.
    signed = int(gdf["has_sign"].sum())
    print(f"Shop sign on {signed:,} of {len(gdf):,} storefronts "
          f"({signed / max(len(gdf), 1) * 100:.1f}%) - the figure the Milan page "
          f"quotes; the rest are labelled with their address")

    out = (pd.DataFrame(gdf.drop(columns=["geometry", "has_sign"]))
           .sort_values(["source", "codice"]).reset_index(drop=True))
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\nwrote {config.BUSINESSES_CLEAN_CSV.name}  {len(out):,} rows")

    buckets = pd.Series([tax.classify(r) for r in out.to_dict("records")])
    print("\nBy bucket:")
    print(buckets.value_counts().to_string())
    print("\nBy source:")
    print(out["source"].value_counts().to_string())
    print("\nActivity labels shown in the tooltip:")
    print(out["attivita"].value_counts().head(14).to_string())

    emit("register_rows", sum(s["rows"] for s in config.SOURCES.values()))
    emit("storefront_rows", len(out))
    emit("retail", int((buckets == "Retail").sum()))
    emit("food_service", int((buckets == "Food service").sum()))
    emit("personal_services", int((buckets == "Personal services").sum()))


if __name__ == "__main__":
    main()
