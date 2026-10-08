"""Bremen step 2: the 2022 regional retail survey -> the shops in the City of
Bremen, each on its own survey point.

    python pipeline/bremen/step2_clean_businesses.py

Reads the cached zip and the cached OSM boundary only (`fetch_sources.py`
downloads). The rules, each from the brief (docs/build_briefs/bremen.md) and
the owner's calls of 2026-10-05:
  * the six fields of the public variant, by exact name; any other field
    stops the step (the privacy reading rests on there being no name or
    address field);
  * the city by the survey's own `Gemeinde` field ("Bremen"), cross-checked
    against the Stadtgemeinde's OSM polygon in EPSG:25832, the survey's own
    CRS; a disagreement is counted by municipality and stops the step unless
    config records it;
  * the goods group through `bremen_einzelhandel`, a closed list of 19 codes;
    an unknown code stops the step, and each code's German label is checked;
  * every floor-area class is kept, the "k.A." (not given) class included;
  * rows sharing a point are drawn as they are (shops in one building).
A pin shows the group's English label: the survey has no names.
"""
import json
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.bremen import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

FETCH = "pipeline/bremen/fetch_sources.py"


def load():
    """The survey's rows as a frame: the six fields plus x, y (EPSG:25832)."""
    if not config.SURVEY_ZIP.exists():
        sys.exit(f"missing {config.SURVEY_ZIP}.\nRun: python {FETCH}")
    with zipfile.ZipFile(config.SURVEY_ZIP) as z:
        if config.SURVEY_MEMBER not in z.namelist():
            sys.exit(f"{config.SURVEY_MEMBER} missing from the zip: {z.namelist()} - re-read the file")
        d = json.loads(z.read(config.SURVEY_MEMBER).decode(config.SURVEY_ENCODING))
    crs = (((d.get("crs") or {}).get("properties") or {}).get("name") or "")
    if not crs.endswith(config.CRS_SURVEY.split(":")[1]):
        sys.exit(f"survey CRS {crs!r}, not {config.CRS_SURVEY} - re-read the file")
    rows, fields, kinds = [], set(), set()
    for f in d["features"]:
        pr, g = f["properties"], f.get("geometry") or {}
        fields.add(tuple(sorted(pr)))
        kinds.add(g.get("type"))
        x, y = (g.get("coordinates") or [None, None])[:2]
        rows.append({**{k: pr.get(k) for k in config.SURVEY_FIELDS}, "x": x, "y": y})
    if fields != {tuple(sorted(config.SURVEY_FIELDS))}:
        sys.exit(f"survey fields are now {sorted(fields)}, not {sorted(config.SURVEY_FIELDS)} - "
                 f"re-read the file before anything is published (a name or address field "
                 f"changes the privacy reading)")
    if kinds != {"Point"}:
        sys.exit(f"geometry types {sorted(map(str, kinds))}, not Point only - re-read the file")
    df = pd.DataFrame(rows)
    if len(df) < config.SURVEY_MIN_ROWS:
        sys.exit(f"{len(df):,} rows - a failed or truncated download, not a smaller region")
    if df[["x", "y"]].isna().any().any() or (df[["x", "y"]] == 0).any().any():
        sys.exit("survey rows with a null or zero coordinate - re-read the file")
    if df["id"].duplicated().any():
        sys.exit("survey ids repeat - re-read the file")
    return df


def classify_rows(df, tax):
    """hwg_code, checked against the module's German label; floor class kept."""
    df = df.copy()
    df["hwg_code"] = df["HWG_C"].map(tax.code_of)   # raises on an unknown code
    relabelled = df.loc[df["HWG"] != df["hwg_code"].map(tax.german_label),
                        ["hwg_code", "HWG"]].drop_duplicates()
    if len(relabelled):
        sys.exit("the survey relabels goods group(s) "
                 f"{sorted(relabelled['hwg_code'].unique())} - re-read the code list")
    return df


def summary(df, tax):
    """Counts per goods group and floor class, and the catch-all share: counts
    only, never a row."""
    n = len(df)
    by = df["hwg_code"].value_counts()
    print(f"  per goods group ({n:,} rows):")
    for code, k in by.items():
        print(f"    {code:>2} {k:>5}  {tax.label(code)}")
    catch = int(df["hwg_code"].isin(tax.CATCH_ALL).sum())
    print(f"  catch-all {tax.CATCH_ALL} (Sonstige EH-Einrichtungen): {catch:,} of {n:,} "
          f"({catch / n:.1%})")
    print("  per floor-area class (all kept): " + ", ".join(
        f"{c} {k:,}" for c, k in df["Gr_Kl_C"].value_counts().sort_index().items()))
    return catch


def city_polygon_25832():
    # Imported here so load()/summary() run before the OSM cache exists.
    from pipeline.bremen.boundary import city_geometry
    return gpd.GeoSeries([city_geometry()], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).iloc[0]


def main():
    df = load()
    print(f"Loaded {len(df):,} survey rows from {config.SURVEY_ZIP.name}, "
          f"{df['Gemeinde'].nunique()} municipalities")
    emit("rows", len(df))
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    df = classify_rows(df, tax)

    by_label = df["Gemeinde"] == config.CITY_GEMEINDE
    pts = gpd.GeoSeries(gpd.points_from_xy(df["x"], df["y"]), crs=config.CRS_SURVEY, index=df.index)
    in_city = pts.within(city_polygon_25832())
    disagree = by_label != in_city
    print(f"  Gemeinde = {config.CITY_GEMEINDE!r}: {int(by_label.sum()):,}; other "
          f"municipalities: {int((~by_label).sum()):,}")
    print(f"  inside the city polygon: {int(in_city.sum()):,}; labelled Bremen and inside "
          f"{int((by_label & in_city).sum()):,}, labelled Bremen and outside "
          f"{int((by_label & ~in_city).sum())}, labelled elsewhere and inside "
          f"{int((~by_label & in_city).sum())}")
    if disagree.any():
        print("  disagreements by municipality: " + ", ".join(
            f"{g} {k}" for g, k in df.loc[disagree, "Gemeinde"].value_counts().items()))
    emit("polygon_label_disagree", int(disagree.sum()))
    if int(disagree.sum()) != config.POLYGON_DISAGREE_EXPECTED:
        sys.exit(f"{int(disagree.sum())} rows where the Gemeinde field and the city polygon "
                 f"disagree, config records {config.POLYGON_DISAGREE_EXPECTED} - read them")

    # Scope: the survey's own Gemeinde field (the owner's call 2).
    df, pts = df[by_label].copy(), pts[by_label]
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    if len(df) != before:
        sys.exit(f"{before - len(df)} rows left no bucket - every goods group is Retail")
    catch = summary(df, tax)
    emit("catch_all", catch)

    shared = df.duplicated(["x", "y"], keep=False)
    print(f"  distinct points {df[['x', 'y']].drop_duplicates().shape[0]:,}; rows sharing a "
          f"point with another (drawn as they are): {int(shared.sum())}")

    ll = pts.to_crs(config.CRS_GEOGRAPHIC)
    df["longitude"], df["latitude"] = ll.x.round(6), ll.y.round(6)
    b = config.BREMEN_BBOX
    if not (df["latitude"].between(b["lat_min"], b["lat_max"]).all()
            and df["longitude"].between(b["lon_min"], b["lon_max"]).all()):
        sys.exit("a point outside the sanity box - re-read the CRS")
    df["business_name"] = df["hwg_code"].map(tax.label)

    out = (df[["id", "business_name", "hwg_code", "latitude", "longitude"]]
           .sort_values("id").reset_index(drop=True))
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n{len(out):,} shops -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)} "
          f"{{'Retail': {len(out):,}}}")
    emit("storefronts", len(out))
    emit("retail", len(out))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
