"""Brussels step 2: hub.brussels's inventory -> the storefronts on the map.

    python pipeline/brussels/step2_clean_businesses.py

Reads the cache only; `fetch_sources.py` downloads. Every unit carries a point
(`geo_point_2d`); scope is the City's polygon, re-checked here. Vacant units
and the types `brussels_hub.py` leaves out are dropped; a unit with several
types takes the highest kept bucket (Food service, Retail, Personal services).

The dot's name is the shop sign (`name_fr`, else `name_nl`, `name_en`). A sign
read as a person's own name is withheld by KEY (config.PERSON_NAMED,
pipeline/name_keys.py) and the dot shows its type instead; so does a unit with
no sign. The Google link columns never reach this step (the fetch leaves
them out), and the step stops if one does.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.brussels import config  # noqa: E402
from pipeline.countries.belgium import brussels_region_communes  # noqa: E402
from pipeline.name_keys import keys_of  # noqa: E402
from pipeline.taxonomies import brussels_hub as tax  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402

FETCH = "pipeline/brussels/fetch_sources.py"


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    if not config.HUB_JSON.exists():
        sys.exit(f"missing {config.HUB_JSON}\nRun: python {FETCH}")
    rows = json.loads(config.HUB_JSON.read_text(encoding=config.SOURCE_ENCODING))
    df = pd.DataFrame(rows)
    leaked = set(df.columns) & set(config.HUB_NEVER)
    if leaked:
        sys.exit(f"Google link column(s) in the cache: {sorted(leaked)}. Re-fetch.")
    print(f"hub.brussels inventory: {len(df):,} units")
    emit("hub_rows", len(df))
    dates = df["last_update"].astype(str).str[:10].value_counts()
    print(f"  survey dates: {dates.to_dict()}")
    if list(dates.index) != [config.HUB_SURVEY_DATE]:
        sys.exit(f"expected one survey dated {config.HUB_SURVEY_DATE}: a new survey, re-measure")
    if df["objectid"].duplicated().any():
        sys.exit("duplicate objectid")

    # Every type known before any filter: an unknown one stops the build.
    n_types = df[tax.VALUE_COLUMN].map(lambda v: len(tax.types_of(v)))
    print(f"  {int((n_types >= 2).sum()):,} units carry two or more types")
    emit("units_multi_type", int((n_types >= 2).sum()))

    df["latitude"] = df["geo_point_2d"].map(lambda p: (p or {}).get("lat"))
    df["longitude"] = df["geo_point_2d"].map(lambda p: (p or {}).get("lon"))
    no_pt = df["latitude"].isna() | df["longitude"].isna()
    print(f"  without a point: {int(no_pt.sum())}")
    df = df[~no_pt].copy()
    b = config.BRUSSELS_BBOX
    in_box = df["latitude"].between(b["lat_min"], b["lat_max"]) & \
        df["longitude"].between(b["lon_min"], b["lon_max"])
    print(f"  outside the sanity box: {int((~in_box).sum())}")
    df = df[in_box].copy()

    com = brussels_region_communes(config.COMMUNES_GEOJSON, FETCH)
    city = com[com["nis"] == config.COMMUNE_CODE].geometry.union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        index=df.index, crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(city)
    print(f"  outside the City's polygon: {int((~inside).sum())}")
    df = df[inside.values].copy()

    vacant = df[tax.VALUE_COLUMN].map(
        lambda v: tax.types_of(v) == ["Cellule vide - Statut inconnu"])
    print(f"  vacant units: {int(vacant.sum()):,}")
    emit("vacant", int(vacant.sum()))
    df = df[~vacant].copy()

    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM).copy()
    print(f"  types left out (lodging, recreation, offices, repairs, ...): {before - len(df):,}")
    df["category"] = [tax.classify({tax.VALUE_COLUMN: v}) for v in df[tax.VALUE_COLUMN]]
    counts = df["category"].value_counts()
    for bkt in tax.PRIORITY:
        print(f"    {bkt:<18} {int(counts.get(bkt, 0)):>6,}")
        emit(f"bucket_{bkt.lower().replace(' ', '_')}", int(counts.get(bkt, 0)))
    two = df[tax.VALUE_COLUMN].map(
        lambda v: len({tax.TYPE_TO_BUCKET[t] for t in tax.types_of(v) if t in tax.TYPE_TO_BUCKET}) >= 2)
    print(f"  units typed in two or more buckets (highest kept): {int(two.sum()):,}")
    emit("units_two_buckets", int(two.sum()))

    def first(*cols):
        out = pd.Series(pd.NA, index=df.index, dtype="object")
        for c in cols:
            v = df[c].where(df[c].astype(str).str.strip().ne("") & df[c].notna())
            out = out.fillna(v)
        return out

    df["business_name"] = first("name_fr", "name_nl", "name_en")
    unnamed = df["business_name"].isna()
    person = keys_of(df["business_name"].fillna("")).isin(config.PERSON_NAMED) & ~unnamed
    print(f"  no sign: {int(unnamed.sum())}; sign withheld as a person's own name: {int(person.sum())}")
    emit("names_withheld", int(person.sum()))
    df.loc[unnamed | person, "business_name"] = df.loc[unnamed | person, tax.VALUE_COLUMN]
    df["name_is_type"] = unnamed | person

    out = df[["objectid", "business_name", "name_is_type", tax.VALUE_COLUMN, "category",
              "address_fr", "postalcode", "latitude", "longitude"]].rename(
                  columns={"address_fr": "address"})
    out = out.sort_values("objectid")
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    emit("storefronts", len(out))


if __name__ == "__main__":
    main()
