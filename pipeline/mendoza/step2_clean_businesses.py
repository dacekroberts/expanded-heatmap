"""Step 2 - Mendoza's storefronts from the capital's commercial accounts list.

Input:  data/mendoza/raw/comercios_limpio.json
        data/mendoza/raw/osm.json            (the Ciudad de Mendoza's boundary)
Output: data/mendoza/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **Open commercial accounts at June 2025**, one per business
    (`comercio_id`), each with up to 30 activity rows. Only the RAM rows (the
    business type) classify; signage, scale and motor fee rows never do.
  * **One bucket per business** (`mendoza_rama.classify_business`): every
    RAM row is classified and the first in-scope bucket in BUCKET_PRIORITY
    wins, so one storefront rama puts the business on the map. A business
    with no RAM row is out.
  * **Placed at the register's own point**, read in Gauss-Kruger zone 2
    (EPSG:5344) and kept only inside the Ciudad de Mendoza.
  * **A person's name never labels a pin** (Vancouver's rule, the brief): a
    trade name written as a person's own, surname first ("SURNAME,
    GIVEN-NAME"), shows the business type instead.
  * **No row is printed**: field names and counts only (the brief).

Run:  python pipeline/mendoza/step2_clean_businesses.py
"""
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.mendoza import config  # noqa: E402
from pipeline.mendoza.step1_stations import capital_polygon  # noqa: E402
from pipeline.residence import looks_organisational  # noqa: E402
from pipeline.taxonomies import load_taxonomy_module  # noqa: E402

FETCH = "pipeline/mendoza/fetch_sources.py"
LF = chr(10)
TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)

# Spanish company forms and trade words: a name carrying one is an
# organisation's, never a person's.
ORG_ES = re.compile(r"\b(S\.?\s?A\.?|S\.?\s?R\.?\s?L\.?|S\.?\s?A\.?\s?S\.?|SRL|SAS|SA|SH|"
                    r"HNOS|HERMANOS|CIA|COOP|COOPERATIVA|ASOC|ASOCIACION|FUNDACION|GRUPO|"
                    r"SOCIEDAD|EMPRESA|COMERCIAL|DISTRIBUIDORA|INDUSTRIAS)\b")


def reads_as_person(name):
    """The register's sole-trader form: a comma between surname and given
    name. "&" or a digit never counts, nor any company or trade word."""
    s = str(name or "").strip().upper()
    if "," not in s or re.search(r"[&\d]", s):
        return False
    return not ORG_ES.search(s) and not looks_organisational(s)


def load():
    if not config.REGISTER_JSON.exists():
        sys.exit(f"missing {config.REGISTER_JSON}\nRun: python {FETCH}")
    raw = json.loads(config.REGISTER_JSON.read_text(encoding="utf-8"))
    rows = raw if isinstance(raw, list) else next(v for v in raw.values() if isinstance(v, list))
    cols = ["comercio_id", "nombre_fantasia", "tipo_actividad", "desc_full", "x", "y"]
    return pd.DataFrame(rows)[cols]


def main():
    df = load()
    print(f"Loaded {len(df):,} activity rows for {df['comercio_id'].nunique():,} businesses "
          f"(open accounts, {config.REGISTER_DATA_DATE})")
    emit("activity_rows", len(df))
    emit("businesses", int(df["comercio_id"].nunique()))

    ram = df[df[TAX.TYPE_COLUMN].fillna("").str.strip().str.upper() == TAX.RAM_TYPE]
    ramas = ram.groupby(TAX.BUSINESS_ID_COLUMN)[TAX.VALUE_COLUMN].agg(list)
    # One row per business for its name and point; the activity fields of
    # whichever row came first say nothing about the business, so they go.
    biz = (df.drop_duplicates(TAX.BUSINESS_ID_COLUMN).set_index(TAX.BUSINESS_ID_COLUMN)
             .drop(columns=[TAX.TYPE_COLUMN, TAX.VALUE_COLUMN]))
    no_ram = ~biz.index.isin(ramas.index)
    print(f"  with no RAM row (no business type): {int(no_ram.sum()):,}, out")
    emit("no_ram_row", int(no_ram.sum()))
    picked = ramas.map(TAX.classify_business)
    biz = biz.loc[ramas.index].assign(bucket=picked.map(lambda t: t[0]),
                                      rama=picked.map(lambda t: t[1]))
    counts = biz["bucket"].value_counts(dropna=False)
    print("  one bucket per business: " + ", ".join(f"{b} {n:,}" for b, n in counts.items()))
    biz = biz[biz["bucket"].notna()].copy()
    emit("storefront_businesses", len(biz))

    x = pd.to_numeric(biz["x"], errors="coerce")
    y = pd.to_numeric(biz["y"], errors="coerce")
    no_point = x.isna() | y.isna() | (x == 0) | (y == 0)
    print(f"  no usable point: {int(no_point.sum()):,}")
    biz, x, y = biz[~no_point], x[~no_point], y[~no_point]
    pts = gpd.GeoSeries(gpd.points_from_xy(x, y), crs=config.REGISTER_CRS,
                        index=biz.index).to_crs(config.CRS_GEOGRAPHIC)
    biz["longitude"], biz["latitude"] = pts.x, pts.y
    inside = pts.within(capital_polygon())
    print(f"  outside the Ciudad de Mendoza: {int((~inside).sum()):,}, dropped")
    emit("outside_city", int((~inside).sum()))
    biz = biz[inside].copy()

    name = biz["nombre_fantasia"].fillna("").astype(str).str.strip()
    person = name.map(reads_as_person)
    biz["name_is_category"] = person | (name == "")
    biz["business_name"] = name.where(~biz["name_is_category"], biz["rama"].str.strip())
    print(f"  a trade name written as a person's own, surname first: {int(person.sum()):,} "
          f"-> the business type shown")
    emit("name_as_category", int(biz["name_is_category"].sum()))

    b = config.MENDOZA_BBOX
    assert biz["latitude"].between(b["lat_min"], b["lat_max"]).all()
    assert biz["longitude"].between(b["lon_min"], b["lon_max"]).all()

    out = biz.reset_index().rename(columns={TAX.BUSINESS_ID_COLUMN: "comercio_id",
                                            "rama": TAX.VALUE_COLUMN})[
        ["comercio_id", "business_name", TAX.VALUE_COLUMN, "name_is_category",
         "latitude", "longitude"]]
    out = out.sort_values("comercio_id").reset_index(drop=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator=LF)
    final = out[TAX.VALUE_COLUMN].map(lambda v: TAX.classify({TAX.VALUE_COLUMN: v}))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}: "
          + ", ".join(f"{k} {v:,}" for k, v in final.value_counts().items()))
    emit("premises", len(out))
    for k, v in final.value_counts().items():
        emit(f"bucket_{k.lower().replace(' ', '_')}", int(v))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
