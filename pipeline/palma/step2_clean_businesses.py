"""Step 2 - Palma's food premises from the Consell de Mallorca's register of
restaurant and entertainment establishments, placed by their own coordinates
or by Catastro's address points.

Input:  data/palma/raw/empreses_restauracio_mallorca.csv   (the register)
        data/palma/raw/A.ES.SDGC.AD.07040.zip               (Catastro addresses)
        data/palma/raw/city_boundary.geojson                (the municipality)
Output: data/palma/processed/businesses_clean.csv
        outputs/palma/excluded_premises.csv

What a reader should know before trusting the counts printed below:

  * **Active is `Estat == "Alta"`**, in `Municipi` PALMA (the Consell's own
    assignment); "Baixa temporal" is out.
  * **Placement has tiers, each counted** (the address-join skill's step 6):
    the register's own coordinate (ETRS89 / UTM 31N, about one row in
    eight); else Catastro's point for the same street and number; else the
    nearest listed number on the same side within config.NEAREST_NUMBER_MAX;
    else unplaced, with the reason. The join is pipeline/countries/
    spain_catastro.py, and its CONTROL is the rows that carry both a
    coordinate and an address: where the join puts them against where the
    register does (printed; re-run after any change to the parser).
  * **What is left out** - catering (R1) by type, and what a name says a
    premises is - is pipeline/taxonomies/palma_restauracio.py, listed row by
    row in excluded_premises.csv with the unplaced rows.
  * **`Explotador/s` is never read**: it names the operator, sometimes a
    person with a tax id. The trade name (`Denominació comercial`) is shown.

Run:  python pipeline/palma/step2_clean_businesses.py
"""
import re
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import spain_catastro as sc  # noqa: E402
from pipeline.palma import config  # noqa: E402

from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.taxonomies.palma_restauracio import (  # noqa: E402
    KNOWN_KINDS, VALUE_TO_BUCKET, premises_kind)

OUT = ["source_key", "business_name", "premises_kind", "establishment_type", "address",
       "placement", "latitude", "longitude"]
# "<street>, <number><rest>. <postcode> <locality>, PALMA, Mallorca": the
# first comma followed by a number (or S/N) ends the street.
ADDRESS = re.compile(r"^(?P<street>.*?),\s*(?P<num>S/N|S\.N\.|\d+\s*[A-Za-z]?\b)(?P<rest>.*)$")
POSTCODE = re.compile(r"\b(07\d{3})\b")
# Street names the register and Catastro spell differently, read at the
# build: Passeig Marítim is the popular name of Avinguda de Gabriel Roca,
# which is what Catastro files.
ALIASES = {"MARITIM": "GABRIEL ROCA"}


def parse_address(text):
    """(street, number, suffix, postcode) from the register's `Direcció`."""
    m = ADDRESS.match(text)
    pc = POSTCODE.search(text)
    if not m:
        return text, None, "", pc.group(1) if pc else ""
    number, suffix = sc.split_number(m.group("num").replace(" ", ""))
    return m.group("street"), number, suffix, pc.group(1) if pc else ""


def main():
    for p in (config.REGISTER_CSV, config.CATASTRO_ZIP, config.CITY_BOUNDARY_GEOJSON):
        if not p.exists():
            sys.exit(f"missing {p}\nRun: python pipeline/palma/fetch_sources.py")
    reg = pd.read_csv(config.REGISTER_CSV, sep=";", encoding="utf-8-sig", dtype=str,
                      keep_default_na=False, usecols=config.REGISTER_COLUMNS)
    assert "Explotador/s" not in reg.columns
    print(f"Register: {len(reg):,} rows island-wide")
    df = reg[reg["Municipi"].str.strip().str.upper() == config.MUNICIPI].copy()
    print(f"In Palma: {len(df):,}; states {df['Estat'].value_counts().to_dict()}")
    if not df["Signatura"].is_unique:
        sys.exit("Signatura is not unique within Palma")
    df["reason"] = np.where(df["Estat"].isin(config.ACTIVE_STATES), "", "Not active (" + df["Estat"] + ")")

    # --- The premises kind: type, then name ----------------------------------
    df["premises_kind"] = [premises_kind(g, n) for g, n in
                           zip(df["Grup"], df["Denominació comercial"])]
    assert set(df["premises_kind"]) <= KNOWN_KINDS, set(df["premises_kind"]) - KNOWN_KINDS
    active = df["reason"] == ""
    kept = active & df["premises_kind"].isin(VALUE_TO_BUCKET)
    df.loc[active & ~kept, "reason"] = df.loc[active & ~kept, "premises_kind"]
    print("\nActive by type:")
    print(df[active]["Grup"].value_counts().to_string())
    print("\nActive by kind:")
    print(df[active]["premises_kind"].value_counts().to_string())
    for kind, n in df[active]["premises_kind"].value_counts().items():
        emit("kind_" + "".join(ch if ch.isalnum() else "_" for ch in kind.lower()), int(n))

    # --- Placement: the register's coordinate, then Catastro ----------------
    addresses = sc.read_addresses(config.CATASTRO_ZIP, "A.ES.SDGC.AD.07040.gml")
    print(f"\nCatastro: {len(addresses):,} address points, {addresses['street_id'].nunique():,} "
          f"streets, {addresses['street_key'].nunique():,} name keys")
    joiner = sc.Joiner(addresses, config.NEAREST_NUMBER_MAX, aliases=ALIASES)
    parsed = [parse_address(t) for t in df["Direcció"]]
    tiers, xs, ys, hows = [], [], [], []
    for street, number, suffix, pc in parsed:
        kind, key = sc.street_key(street)
        ckey, how = joiner.resolve(key)
        tier, x, y = joiner.place(ckey, number, suffix, kind, pc)
        tiers.append(tier), xs.append(x), ys.append(y), hows.append(how)
    df["join_tier"], df["jx"], df["jy"], df["join_key_how"] = tiers, xs, ys, hows
    df["rx"] = pd.to_numeric(df["UTM (X)"], errors="coerce")
    df["ry"] = pd.to_numeric(df["UTM(Y)"], errors="coerce")

    # THE CONTROL: rows with both a register coordinate and a joined point.
    both = df["rx"].notna() & df["jx"].notna()
    dist = np.hypot(df.loc[both, "rx"] - df.loc[both, "jx"], df.loc[both, "ry"] - df.loc[both, "jy"])
    agree = float((dist <= config.CONTROL_AGREE_M).mean())
    print(f"\nCONTROL: {int(both.sum())} rows carry both; the join lands a median "
          f"{dist.median():.1f} m from the register's point, {agree:.1%} within "
          f"{config.CONTROL_AGREE_M} m (p90 {dist.quantile(0.9):.0f} m)")
    emit("control_rows", int(both.sum()))
    emit("control_within_100m_pct", round(agree * 100, 1))

    has_reg = df["rx"].notna()
    df["placement"] = np.where(has_reg, "register",
                               np.where(df["jx"].notna(), "catastro_" + df["join_tier"], ""))
    df["x"] = df["rx"].where(has_reg, df["jx"])
    df["y"] = df["ry"].where(has_reg, df["jy"])
    unplaced = kept & df["x"].isna()
    df.loc[unplaced, "reason"] = "Not placed: " + df.loc[unplaced, "join_tier"]
    k = df[kept]
    print("\nKept premises by placement tier:")
    print(k["placement"].replace("", "unplaced").value_counts().to_string())
    print("Unplaced by reason:")
    print(k[k["x"].isna()]["join_tier"].value_counts().to_string())
    print("Joined keys by how the street was matched:")
    print(k[~k["rx"].notna() & k["jx"].notna()]["join_key_how"].value_counts().to_string())
    for tier, n in k["placement"].replace("", "unplaced").value_counts().items():
        emit(f"placed_{tier}", int(n))
    placed_share = float(k["x"].notna().mean())
    print(f"Placed: {placed_share:.1%} of {len(k):,} kept premises")

    # --- In the municipality: the placed point against the boundary ---------
    city = shape(__import__("json").loads(config.CITY_BOUNDARY_GEOJSON.read_text(
        encoding="utf-8"))["geometry"])
    placed = kept & df["x"].notna()
    pts = gpd.GeoSeries(gpd.points_from_xy(df.loc[placed, "x"], df.loc[placed, "y"]),
                        crs=config.CATASTRO_CRS, index=df.index[placed]).to_crs(config.CRS_GEOGRAPHIC)
    outside = ~pts.within(city)
    df.loc[outside[outside].index, "reason"] = "Point outside the municipality"
    print(f"Placed points outside the municipality: {int(outside.sum())}")
    emit("outside_city", int(outside.sum()))
    # The register's own latitude/longitude columns are not used: its UTM
    # pair is the same point (the control) and every placed row, joined or
    # not, is projected from one CRS here.
    df["latitude"], df["longitude"] = np.nan, np.nan
    df.loc[pts.index, "longitude"] = pts.x
    df.loc[pts.index, "latitude"] = pts.y

    df["address"] = df["Direcció"].str.replace(r",\s*PALMA,\s*Mallorca\s*$", "", regex=True).str.strip()
    excluded = df[df["reason"] != ""]
    excluded[["Signatura", "Denominació comercial", "Grup", "address", "reason"]].rename(columns={
        "Signatura": "source_key", "Denominació comercial": "business_name",
        "Grup": "establishment_type"}).sort_values(["reason", "business_name"]).to_csv(
        config.EXCLUDED_PREMISES_CSV, index=False, encoding="utf-8")
    print(f"{len(excluded):,} left out -> {config.EXCLUDED_PREMISES_CSV.relative_to(config.ROOT)}")
    print(excluded["reason"].value_counts().to_string())

    out = df[df["reason"] == ""].copy()
    out = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    assert all(tax.classify({tax.VALUE_COLUMN: v}) for v in out[tax.VALUE_COLUMN])
    out["business_name"] = out["Denominació comercial"].str.strip()
    out["establishment_type"] = out["Grup"]
    out["source_key"] = out["Signatura"]
    b = config.PALMA_BBOX
    assert out["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert out["longitude"].between(b["lon_min"], b["lon_max"]).all()
    emit("storefronts", len(out))
    out = out[OUT].sort_values("source_key").reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
