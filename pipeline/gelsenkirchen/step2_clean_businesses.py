"""Step 2 - Gelsenkirchen's storefronts from the City's survey of its
commercial premises.

    python pipeline/gelsenkirchen/step2_clean_businesses.py

Input:  data/gelsenkirchen/raw/idb_gewerbe_{gastronomie,einzelhandel,dienstleistung}.geojson
        data/gelsenkirchen/raw/osm_boundaries.json      (the city polygon)
Output: data/gelsenkirchen/processed/businesses_clean.csv

Reads the cache only; `fetch_sources.py` downloads. What a reader should know
before trusting the counts printed below:

  * **Three themed layers, one survey** (food, retail, services), each with
    its own category field, classified by
    pipeline/taxonomies/gelsenkirchen_gewerbe.py on (layer, category). The
    vacant-unit layers (`gewerbe`, `gewerbe-leerstand`) are never read.
  * **Rows with no category are left out and disclosed** (owner, 2026-10-04).
  * **Services were recorded chiefly inside the city's designated centres**,
    so personal services are thin away from them: the centre class (LAGEBEZ)
    is measured per bucket below and carried to the processed file, never to
    a page or a map.
  * **The dot shows the sign**; a sign read as a person's own name shows the
    category instead (config.PERSON_NAMED, keys; `signs.py`). The contact,
    free-text and address fields are never fetched (config.NEVER_READ).
  * **Scope is the survey's own** (the City's premises), CHECKED against the
    city's OpenStreetMap polygon: a point more than config.POLYGON_TOLERANCE_M
    outside it stops the step. The postcode is a cross-check only.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.gelsenkirchen import config  # noqa: E402
from pipeline.gelsenkirchen.signs import chain_signs, person_rows, person_sign, normalise_sign  # noqa: E402
from pipeline.name_keys import keys_of  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

# LAGEBEZ's centre classes, by prefix (the brief): main centres, district
# centres, local-supply centres, prospective local centres, supplementary
# sites, integrated and non-integrated locations. Longest prefix first.
CENTRE_CLASSES = (("persp. NVZ_", "persp. NVZ"), ("Erg.St._", "Erg.St."), ("HZ_", "HZ"),
                  ("STZ_", "STZ"), ("NVZ_", "NVZ"), ("int", "int"), ("niL", "niL"))
DESIGNATED = ("HZ", "STZ", "NVZ", "persp. NVZ", "Erg.St.")


def centre_class(v):
    v = v.strip() if isinstance(v, str) else ""
    if not v:
        return "blank"
    for prefix, cls in CENTRE_CLASSES:
        if v.startswith(prefix):
            return cls
    sys.exit(f"LAGEBEZ {v!r} is not a known centre class - read it before step 2 runs")


def _text(v):
    return v.strip() if isinstance(v, str) else ""


def load_survey():
    """The three cached layers as one DataFrame, checked, classified: layer,
    id, sign, category, assortment, centre, plz, x25832, y25832, bucket,
    label, kept (classified into a bucket). Scope is not applied here."""
    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    frames = []
    for layer in config.LAYERS:
        path = config.SURVEY_FILES[layer]
        if not path.exists():
            sys.exit(f"missing {path}\nRun: python {config.FETCH}")
        j = json.loads(path.read_text(encoding="utf-8"))
        crs_name = ((j.get("crs") or {}).get("properties") or {}).get("name", "")
        if not crs_name.endswith("25832"):
            sys.exit(f"{path.name}: CRS {crs_name!r}, not {config.CRS_SURVEY}")
        feats = j["features"]
        keys = {k for f in feats for k in f["properties"]}
        leaked = sorted(keys & set(config.NEVER_READ))
        if leaked:
            sys.exit(f"{path.name} holds never-read field(s) {leaked}: re-fetch with "
                     f"python {config.FETCH} --survey")
        rows = []
        for f in feats:
            p, g = f["properties"], f.get("geometry") or {}
            if g.get("type") != "Point":
                sys.exit(f"{layer} id {p.get('id')}: geometry {g.get('type')}, not a point")
            x, y = g["coordinates"][:2]
            rows.append({"layer": config.LAYER_KEYS[layer], "id": p["id"],
                         "sign": _text(p.get("Name")), "typus": p.get("GEWERBETYPUSBEZ"),
                         "category": _text({"gewerbe_gastronomie": p.get("KAT_GASTRO"),
                                            "gewerbe_einzelhandel": p.get("HAUPTWARENGRUPPEBEZ"),
                                            "gewerbe_dienstleistung": p.get("KAT_DL")}[layer]),
                         "assortment": _text(p.get("KERNSORTIMENTBEZ"))
                         if layer == "gewerbe_einzelhandel" else "",
                         "lagebez": p.get("LAGEBEZ"), "plz": _text(str(p.get("PLZ") or "")),
                         "published": p.get("Veroeffentlicht") is True and p.get("Istonline") is True,
                         "x25832": x, "y25832": y, "X": p.get("X"), "Y": p.get("Y")})
        df = pd.DataFrame(rows)
        if set(df["typus"]) != {config.LAYER_TYPUS[layer]}:
            sys.exit(f"{layer}: GEWERBETYPUSBEZ is {sorted(set(df['typus'].astype(str)))}, "
                     f"not {config.LAYER_TYPUS[layer]!r} on every row")
        if df["id"].isna().any() or df["id"].duplicated().any():
            sys.exit(f"{layer}: `id` is missing or repeats")
        if not df["published"].all():
            sys.exit(f"{layer}: {int((~df['published']).sum())} row(s) not marked published "
                     f"(Veroeffentlicht and Istonline): such a row must not be drawn")
        dxy = ((df["x25832"] - df["X"].astype(float)) ** 2
               + (df["y25832"] - df["Y"].astype(float)) ** 2) ** 0.5
        if not (dxy <= config.XY_TOLERANCE_M).all():
            sys.exit(f"{layer}: the geometry and X/Y disagree by up to {dxy.max():.3f} m")
        print(f"  {layer}: {len(df):,} rows; geometry and X/Y agree to {1000 * dxy.max():.0f} mm")
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    if df["id"].duplicated().any():
        sys.exit("an `id` appears in two layers: the layers are no longer disjoint")
    blank = df["sign"] == ""
    if blank.any():
        sys.exit(f"{int(blank.sum())} row(s) with no sign: decide what the dot shows first")
    cols = [tax.VALUE_COLUMN, *tax.EXTRA_COLUMNS]
    df["bucket"] = [tax.classify(dict(zip(cols, v))) for v in zip(*(df[c] for c in cols))]
    df["label"] = [tax.label(dict(zip(cols, v))) for v in zip(*(df[c] for c in cols))]
    df["kept"] = df["bucket"].notna()
    df["centre"] = df["lagebez"].map(centre_class)
    return df


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    print("The City's commercial-premises survey (cached reduced layers):")
    df = load_survey()
    emit("survey_rows", len(df))

    # --- what each rule takes out ------------------------------------------------
    print("\n  by layer and verdict:")
    for (layer, bucket), g in df.groupby(["layer", df["bucket"].fillna("out")]):
        print(f"    {layer:<15} {bucket:<18} {len(g):>5,}")
    out = df[~df["kept"]]
    uncategorised = out[out["category"] == ""]
    print(f"\n  left out: {len(out):,}, of which {len(uncategorised)} with no category "
          f"({', '.join(f'{n} {k}' for k, n in uncategorised['layer'].value_counts().items())})")
    for lab, n in out[out["category"] != ""]["label"].value_counts().items():
        print(f"    {lab:<36} {n:>4}")
    emit("uncategorised_out", len(uncategorised))

    # --- scope: the city polygon -----------------------------------------------
    from pipeline.gelsenkirchen.boundary import city_geometry

    city = gpd.GeoSeries([city_geometry()], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).iloc[0]
    pts = gpd.GeoSeries(gpd.points_from_xy(df["x25832"], df["y25832"]),
                        crs=config.CRS_SURVEY, index=df.index).to_crs(config.CRS_PROJECTED)
    inside = pts.within(city)
    dist = pts.distance(city)
    print(f"\n  inside the city polygon (OpenStreetMap): {int(inside.sum()):,}; outside "
          f"{int((~inside).sum())}, at most {dist.max():.0f} m beyond it")
    far = dist > config.POLYGON_TOLERANCE_M
    if far.any():
        sys.exit(f"{int(far.sum())} survey point(s) lie more than "
                 f"{config.POLYGON_TOLERANCE_M:.0f} m outside the city polygon")
    # The survey is the City's own record of its own premises, so the polygon
    # checks the scope rather than cutting it (Liège's precedent: the
    # publisher's scope, the OSM polygon a check). A kept point just outside
    # OSM's line (1, 1 m out, 2026-10-07) is an edge difference between the
    # two boundaries, and stays.
    kept_outside = int((df["kept"] & ~inside).sum())
    print(f"  kept rows outside the polygon, within {config.POLYGON_TOLERANCE_M:.0f} m (kept): "
          f"{kept_outside}")
    emit("kept_outside_polygon", kept_outside)

    ll = pts.to_crs(config.CRS_GEOGRAPHIC)
    df["latitude"], df["longitude"] = ll.y.round(7), ll.x.round(7)
    kept = filter_to_storefront(df[df["kept"]], config.TAXONOMY_SYSTEM).copy()
    b = config.GELSENKIRCHEN_BBOX
    ok = (kept["latitude"].between(b["lat_min"], b["lat_max"])
          & kept["longitude"].between(b["lon_min"], b["lon_max"]))
    if not ok.all():
        sys.exit(f"{int((~ok).sum())} point(s) outside the sanity box")
    plz_other = ~kept["plz"].isin(config.CITY_PLZ) & (kept["plz"] != "")
    print(f"  postcode cross-check on the kept rows: {int(plz_other.sum())} outside the "
          f"city's postcodes, {int((kept['plz'] == '').sum())} blank (a cross-check only)")

    # --- the centres: the personal-services gap, measured ------------------------
    print("\n  share in a designated centre or supplementary site (LAGEBEZ, measured):")
    for bucket, g in kept.groupby("bucket"):
        share = g["centre"].isin(DESIGNATED).mean()
        print(f"    {bucket:<18} {len(g):>5,}  {100 * share:.1f}%  "
              + ", ".join(f"{c} {n}" for c, n in g["centre"].value_counts().items()))

    # --- the dot's name: the sign, a person's own name withheld ------------------
    point = kept["x25832"].round(1).astype(str) + "," + kept["y25832"].round(1).astype(str)
    allpoint = df["x25832"].round(1).astype(str) + "," + df["y25832"].round(1).astype(str)
    chains = chain_signs(df["sign"], allpoint)
    key = keys_of(kept["sign"])
    withheld_keys = set(config.PERSON_NAMED) | set(config.PERSON_NAMED_BY_EYE)
    person = key.isin(withheld_keys)
    gone = withheld_keys - set(key[person])
    if gone:
        sys.exit(f"{len(gone)} PERSON_NAMED key(s) no longer match a sign: re-generate the "
                 f"list (python -m pipeline.gelsenkirchen.signs --person-keys)")
    proposed = kept["sign"].map(person_sign) & ~kept["sign"].map(normalise_sign).isin(chains)
    unlisted = proposed & ~person
    if unlisted.any():
        sys.exit(f"{int(unlisted.sum())} sign(s) read as a person's own name are not in "
                 f"PERSON_NAMED: re-generate the list (count only; never print them)")
    kept["business_name"] = kept["sign"].where(~person, kept["label"])
    shaped_chain = kept["sign"].map(person_sign) & ~proposed
    print(f"\n  dot names: the sign on {int((~person).sum()):,}; the category shown instead on "
          f"{int(person.sum())} sign(s) read as a person's own name (config.PERSON_NAMED, keys)")
    print(f"  person-shaped signs kept as brands (found at two or more points): "
          f"{int(shaped_chain.sum())}")
    emit("signs_withheld", int(person.sum()))
    shared = point.duplicated(keep=False)
    print(f"  rows sharing a point with another (drawn as they are): {int(shared.sum())}")

    outcols = ["id", "layer", "category", "assortment", "business_name", "latitude",
               "longitude", "centre"]
    res = kept[outcols].sort_values(["layer", "id"]).reset_index(drop=True)
    res.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8", lineterminator="\n")
    by = kept["bucket"].value_counts()
    print(f"\n{len(res):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)} "
          f"{by.to_dict()}")
    emit("storefronts", len(res))
    emit("retail", int(by.get("Retail", 0)))
    emit("food_service", int(by.get("Food service", 0)))
    emit("personal_services", int(by.get("Personal services", 0)))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
