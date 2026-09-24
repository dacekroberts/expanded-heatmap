"""Rome step 2: SUAP premises -> storefronts, placed by joining ANNCSU.

    python pipeline/rome/step2_clean_businesses.py

  * SUAP rows -> ESTABLISHMENTS on (STRUTTURA_GESTIONE, NUMERO_ESERCIZIO) -
    NUMERO_ESERCIZIO alone restarts in every municipio. An establishment
    holding two authorisations (a bar that also sells goods) takes the more
    specific: Food service, then Personal services, then Retail.
  * Classified by the taxonomy (pipeline/taxonomies/rome_suap.py).
  * Placed by JOINING ANNCSU, Italy's house-number archive, on the city's own
    street code (ANNCSU `CODICE_COMUNALE` = SUAP `CODICE_VIA`) + civic number +
    suffix. Civic level only: exactly, or with the suffix dropped where every
    such civic lies in one place. A street's centroid is never used - on a
    long Roman street it can be kilometres from the shop.
  * The register carries NO business name, so every pin shows its activity
    and address.
Nothing here fetches.
"""
import json
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.rome import config, suap  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies import rome_suap as TAX  # noqa: E402

PRIORITY = {TAX.FOOD: 0, TAX.PERSONAL: 1, TAX.RETAIL: 2}
# Suffix-dropped matches are accepted only when every ANNCSU civic of that
# number on that street lies within this distance of the others (one building).
ONE_PLACE_M = 60


def need(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/rome/fetch_sources.py")
    return path


def _num(s):
    s = (s or "").strip().lstrip("0")
    return s or None


def load_anncsu():
    z = zipfile.ZipFile(need(config.ANNCSU_ZIP))
    name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
    a = pd.read_csv(z.open(name), dtype=str, sep=";", encoding="utf-8",
                    usecols=["CODICE_ISTAT", "CODICE_COMUNALE", "CIVICO", "ESPONENTE",
                             "COORD_X_COMUNE", "COORD_Y_COMUNE"])
    a = a[a["CODICE_ISTAT"] == config.ISTAT_COMUNE].copy()
    # WGS84 longitude / latitude, written with DECIMAL COMMAS ("12,4713327").
    a["lon"] = pd.to_numeric(a["COORD_X_COMUNE"].str.replace(",", ".", regex=False), errors="coerce")
    a["lat"] = pd.to_numeric(a["COORD_Y_COMUNE"].str.replace(",", ".", regex=False), errors="coerce")
    print(f"  ANNCSU {name}: {len(a):,} civic numbers in comune {config.ISTAT_COMUNE}, "
          f"{int(a['lon'].notna().sum()):,} with a point")
    a = a.dropna(subset=["lon", "lat"])
    a["via"] = a["CODICE_COMUNALE"].map(_num)
    a["civ"] = a["CIVICO"].map(_num)
    a["esp"] = a["ESPONENTE"].fillna("").str.strip().str.upper()
    exact = a.groupby(["via", "civ", "esp"])[["lat", "lon"]].first()
    by_civ = a.groupby(["via", "civ"]).agg(lat=("lat", "mean"), lon=("lon", "mean"),
                                           dlat=("lat", lambda s: s.max() - s.min()),
                                           dlon=("lon", lambda s: s.max() - s.min()))
    # one place: every civic of this number within ONE_PLACE_M
    span_m = ((by_civ["dlat"] * 111_000) ** 2 + (by_civ["dlon"] * 83_000) ** 2) ** 0.5
    by_civ = by_civ[span_m <= ONE_PLACE_M][["lat", "lon"]]
    return exact, by_civ


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    s = suap.read(need(config.SUAP_CSV))
    print(f"  SUAP rows: {len(s):,}")
    emit("suap_rows", len(s))
    unknown = set(s["DESCRIZIONE"].dropna()) - set(TAX.DESCRIZIONE_BUCKETS) - TAX.DESCRIZIONE_OUT
    if unknown:
        sys.exit(f"unmapped DESCRIZIONE values - map them in rome_suap.py: {sorted(unknown)}")

    s["bucket"] = [TAX.bucket(d, sp) for d, sp in zip(s["DESCRIZIONE"], s["SPECIALIZZAZIONE"])]
    s["prio"] = s["bucket"].map(PRIORITY)
    key = ["STRUTTURA_GESTIONE", "NUMERO_ESERCIZIO"]
    n_est = s[key].drop_duplicates().shape[0]
    print(f"  establishments: {n_est:,}")
    emit("establishments", n_est)
    lab = s["DESCRIZIONE"] == "Laboratorio Artigianale e non"
    print(f"  workshop catch-all rows: {int(lab.sum()):,}, of which "
          f"{int((lab & s['SPECIALIZZAZIONE'].isna()).sum()):,} carry no specialisation - dropped")

    kept = s[s["bucket"].notna()].sort_values(key + ["prio"])
    est = kept.drop_duplicates(subset=key, keep="first").copy()
    mixed = kept.groupby(key)["bucket"].nunique()
    print(f"  storefront establishments: {len(est):,} "
          f"({int((mixed > 1).sum()):,} hold two kinds of authorisation - the more specific wins)")
    for b, n in est["bucket"].value_counts().items():
        print(f"      {b:<18} {n:>7,}")
    emit("storefront_establishments", len(est))

    # --- the ANNCSU join -----------------------------------------------------
    exact, by_civ = load_anncsu()
    est["via"] = est["CODICE_VIA"].map(_num)
    est["civ"] = est["CIVICO"].map(_num)
    est["esp"] = est["ESP_CIVICO"].fillna("").str.strip().str.upper()
    e = est.join(exact, on=["via", "civ", "esp"])
    tier = pd.Series("exact", index=e.index).where(e["lat"].notna(), None)
    loose = e[e["lat"].isna()][["via", "civ"]].join(by_civ, on=["via", "civ"])
    e.loc[loose.index, ["lat", "lon"]] = loose[["lat", "lon"]]
    tier = tier.where(tier.notna(), pd.Series("civic, suffix dropped", index=e.index).where(e["lat"].notna(), None))
    no_civ = e["civ"].isna()
    tier = tier.fillna(pd.Series("no civic number", index=e.index).where(no_civ, "not found"))
    e["tier"] = tier
    print("\n  placed at civic level:")
    for t, n in e["tier"].value_counts().items():
        print(f"      {t:<24} {n:>7,}  ({n / len(e):.1%})")
    by_mun = e.assign(ok=e["lat"].notna()).groupby("MUNICIPIO")["ok"].mean().sort_values()
    print(f"  worst municipi: " + ", ".join(f"{m} {v:.1%}" for m, v in by_mun.head(3).items()))
    placed = e["lat"].notna()
    emit("placed", int(placed.sum()))
    e = e[placed]
    b = config.ROME_BBOX
    inside = e["lat"].between(b["lat_min"], b["lat_max"]) & e["lon"].between(b["lon_min"], b["lon_max"])
    if not inside.all():
        print(f"  {int((~inside).sum())} dropped on the sanity bounding box")
    e = e[inside]

    # DATA_INIZIO is an Excel serial date (22715 = 1962-03-10).
    start = pd.to_numeric(e["DATA_INIZIO"], errors="coerce")
    e["start_year"] = start.map(lambda v: (date(1899, 12, 30) + timedelta(days=int(v))).year
                                if v == v and v > 0 else None)

    def addr(r):
        civ = f" {r['CIVICO'].lstrip('0')}" if r["CIVICO"] else ""
        esp = f"/{r['ESP_CIVICO']}" if r["ESP_CIVICO"] else ""
        return f"{(r['DESCRIZIONE_VIA'] or '').title()}{civ}{esp}"
    out = pd.DataFrame({
        "record_id": "suap:" + e["STRUTTURA_GESTIONE"].str.replace(" ", "_") + ":" + e["NUMERO_ESERCIZIO"],
        "business_name": [addr(r) for _, r in e.iterrows()],
        "name_is_address": True,
        "latitude": e["lat"].values,
        "longitude": e["lon"].values,
        "activity": [TAX.activity_label(d, sp) for d, sp in zip(e["DESCRIZIONE"], e["SPECIALIZZAZIONE"])],
        "descrizione": e["DESCRIZIONE"].values,
        "specializzazione": e["SPECIALIZZAZIONE"].values,
        "municipio": e["MUNICIPIO"].values,
        "start_year": e["start_year"].values,
        "join_tier": e["tier"].values,
    })
    before = len(out)
    out = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(out) != before:
        sys.exit("filter_to_storefront disagrees with step 2's own classification")
    if out["record_id"].duplicated().any():
        sys.exit("an establishment appears twice")
    print(f"\n  {len(out):,} storefronts placed")
    emit("storefronts", len(out))
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
