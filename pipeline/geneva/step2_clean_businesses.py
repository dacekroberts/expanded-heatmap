"""Geneva (Regional) step 2: the canton's business register (REG) -> the
storefront establishments in the 12 tram communes, each on its own LV95
point.

    python pipeline/geneva/step2_clean_businesses.py

Reads the cached zip only (`fetch_sources.py` downloads). The rules, each
from the brief (docs/build_briefs/geneva.md) and the owner's three calls of
2026-10-04:
  * establishment rows only; company rows with no establishment row are
    left out and disclosed (call 1), and counted here;
  * home-based, itinerant and market-stand premises dropped before
    classification (the brief; call 3 for the stands);
  * NOGA 2008 at the six-digit leaf through `geneva_noga`, a closed list:
    a code in a tracked division the module has not decided stops the step;
  * scope by the 12 commune polygons (OSM), cross-checked against the
    register's own PHYS_COMMUNE;
  * the name rule (call 2, Tucson's and Kansas City's precedent): a sole
    trader's trade name is withheld, and the street address shown, where it
    reads as the registrant's own - it shares a word with the registrant's
    legal name (which for an Entreprise individuelle carries the owner's
    surname by law) or is shaped like a person's name. The legal name is
    read in memory for that test and never written.
Phone, fax, e-mail and legal-name columns never reach processed/.
"""
import io
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit  # noqa: E402
from pipeline.geneva import config  # noqa: E402
from pipeline.geneva.communes import region_geometry  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

FETCH = "pipeline/geneva/fetch_sources.py"
# Words a trade name and a legal name share without naming a person: French
# function words and the legal-form tails. Kept short on purpose: a word left
# off only withholds one more name, which shows its address instead.
_SHARED_NOT_A_NAME = {
    "de", "des", "du", "la", "le", "les", "et", "chez", "au", "aux", "sur", "en",
    "sarl", "sa", "gmbh", "ag", "the", "and", "of",
}


def _fold(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode("ascii")
    return {w for w in re.findall(r"[a-z]{3,}", s.lower()) if w not in _SHARED_NOT_A_NAME}


def load():
    if not config.REG_ZIP.exists():
        sys.exit(f"missing {config.REG_ZIP}.\nRun: python {FETCH}")
    with zipfile.ZipFile(config.REG_ZIP) as z:
        raw = z.read(config.REG_MEMBER)
    df = pd.read_csv(io.BytesIO(raw), sep=";", encoding="utf-8-sig", dtype=str,
                     keep_default_na=False)
    missing = sorted(set(config.REG_COLUMNS) - set(df.columns))
    if missing:
        sys.exit(f"REG columns gone: {missing} - re-read the dataset's documentation")
    if len(df) < config.REG_MIN_ROWS:
        sys.exit(f"{len(df):,} rows - a failed fetch, not a smaller canton")
    return df[list(config.REG_COLUMNS)]


def main():
    df = load()
    print(f"Loaded {len(df):,} REG rows: {df['TYPE_REG'].value_counts().to_dict()}")
    emit("rows", len(df))
    if set(df["STATUT_REG"]) != {"En activité"}:
        sys.exit(f"STATUT_REG values {sorted(set(df['STATUT_REG']))} - the register is "
                 f"published active-only; re-read it before filtering")

    tax = load_taxonomy_module(config.TAXONOMY_SYSTEM)
    companies = df[df["TYPE_REG"] == "Entreprise"].set_index("ID_ENTREPRISE")
    est = df[df["TYPE_REG"] == config.RECORD_TYPE].copy()
    est["activity_code"], est["activity_label"] = est["CODE_NOGA"], est["BRANCHE"]
    unknown = tax.unlisted(est["activity_code"])
    if unknown:
        sys.exit(f"NOGA codes in a tracked division the taxonomy has not decided: {unknown}")

    # Company rows with a bucket code and no establishment row: left out (call 1),
    # counted for the page, inside the region only.
    comp = companies.reset_index()
    comp["activity_code"], comp["activity_label"] = comp["CODE_NOGA"], comp["BRANCHE"]
    comp = filter_to_storefront(comp, config.TAXONOMY_SYSTEM)
    comp = comp[~comp["ID_ENTREPRISE"].isin(set(est["ID_ENTREPRISE"]))]

    # What the 12 communes lose, for docs/excluded_categories.md: tracked-
    # division rows dropped by premises type, and rows left out by code.
    region = gpd.GeoSeries([region_geometry()], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).iloc[0]

    def inside(frame):
        pts = gpd.GeoSeries(gpd.points_from_xy(pd.to_numeric(frame["E"]), pd.to_numeric(frame["N"])),
                            crs=config.CRS_REGISTER, index=frame.index)
        return pts, pts.within(region)

    tracked = est["activity_code"].str[:2].isin(tax.TRACKED_DIVISIONS)
    scope_tracked = est[tracked & inside(est)[1]]
    by_type = scope_tracked[scope_tracked["TYPE_LOCAL"].isin(config.DROP_PREMISES)]
    print("  in the 12 communes, storefront-coded rows dropped by premises type: "
          + ", ".join(f"{k} {v}" for k, v in by_type.assign(
              b=by_type["activity_code"].map(lambda c: tax.classify({"activity_code": c})))
              .dropna(subset=["b"])["TYPE_LOCAL"].value_counts().items()))
    out_coded = scope_tracked[~scope_tracked["TYPE_LOCAL"].isin(config.DROP_PREMISES)
                              & scope_tracked["activity_code"].isin(set(tax.OUT))]
    print("  in the 12 communes, left out by code: " + ", ".join(
        f"{c} {n}" for c, n in out_coded["activity_code"].value_counts().items()))

    dropped = est["TYPE_LOCAL"].isin(config.DROP_PREMISES)
    est = est[~dropped]
    print(f"  establishments: {len(est) + int(dropped.sum()):,}; dropped by premises type "
          f"({', '.join(config.DROP_PREMISES)}): {int(dropped.sum()):,}")
    est = filter_to_storefront(est, config.TAXONOMY_SYSTEM)
    est["bucket"] = [tax.classify({"activity_code": c}) for c in est["activity_code"]]
    print(f"  storefront establishments, canton: {len(est):,} "
          f"{est['bucket'].value_counts().to_dict()}")

    # Scope: the 12 commune polygons, on the register's own LV95 point.
    pts, in_region = inside(est)
    by_label = est["PHYS_COMMUNE"].isin(config.REG_COMMUNE_LABELS)
    print(f"  in the 12 communes by polygon: {int(in_region.sum()):,}; by PHYS_COMMUNE: "
          f"{int(by_label.sum()):,}; polygon only {int((in_region & ~by_label).sum())}, "
          f"label only {int((~in_region & by_label).sum())}")
    emit("polygon_label_disagree", int((in_region != by_label).sum()))
    est, pts = est[in_region].copy(), pts[in_region]
    cpts, c_in = inside(comp)
    gap = comp[c_in]
    print(f"  company rows with a storefront code and no establishment row, in the 12 "
          f"communes (left out, call 1): {len(gap):,} "
          f"{gap['activity_code'].map(lambda c: tax.classify({'activity_code': c})).value_counts().to_dict()}")
    emit("company_only_left_out", len(gap))

    office = est["TYPE_LOCAL"] == "Bureau/étude/cabinet"
    print(f"  kept rows typed Bureau/étude/cabinet: {int(office.sum()):,}, by code:")
    for (code, label), n in est[office].groupby(["activity_code", "activity_label"]).size() \
            .sort_values(ascending=False).items():
        print(f"    {code} {n:>4}  {label}")
    emit("office_typed", int(office.sum()))

    # The name rule (call 2).
    form = est["ID_ENTREPRISE"].map(companies["NATURE_JURID"]).fillna("")
    legal = est["ID_ENTREPRISE"].map(companies["RAISON_SOCIALE"]).fillna("")
    name = est["NOM"].str.strip()
    sole = form == config.SOLE_TRADER
    unknown_form = form == ""
    shares = pd.Series([bool(_fold(n) & _fold(lg)) for n, lg in zip(name, legal)], index=est.index)
    shaped = name.map(looks_personal)
    office = est["TYPE_LOCAL"] == config.OFFICE_PREMISES
    withhold = (sole & (shares | shaped)) | (unknown_form & shaped) | (office & shaped) | (name == "")
    est["address"] = (est["PHYS_RUE"].str.strip() + " " + est["PHYS_NUMRUE"].str.strip()).str.strip()
    est["business_name"] = name.where(~withhold, est["address"])
    print(f"  sole traders: {int(sole.sum()):,}; their names withheld (the address shown): "
          f"{int((sole & withhold).sum()):,} (shares a word with the legal name "
          f"{int((sole & shares).sum()):,}, shaped like a person's {int((sole & shaped).sum()):,})")
    print(f"  legal form unknown (no company row in the canton): {int(unknown_form.sum()):,}, "
          f"withheld as person-shaped {int((unknown_form & shaped).sum()):,}; no trade name "
          f"{int((name == '').sum()):,}")
    print(f"  office-typed: {int(office.sum()):,} kept; person-shaped names there shown as the "
          f"address, any legal form: {int((office & shaped & ~sole & ~unknown_form).sum()):,} "
          f"beyond the sole-trader rule")
    emit("office_person_shaped_withheld", int((office & shaped & ~sole & ~unknown_form).sum()))
    emit("names_withheld", int(withhold.sum()))
    del legal

    ll = pts.to_crs(config.CRS_GEOGRAPHIC)
    est["longitude"], est["latitude"] = ll.x.round(6), ll.y.round(6)
    est["commune"] = est["PHYS_COMMUNE"]
    out = (est.rename(columns={"ID_ETABLISSEMENT": "id"})
           [["id", "business_name", "activity_label", "activity_code", "address", "commune",
             "latitude", "longitude"]]
           .sort_values("id").reset_index(drop=True))
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    by = est["bucket"].value_counts().to_dict()
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)} {by}")
    emit("storefronts", len(out))
    for b in ("Food service", "Retail", "Personal services"):
        emit(b.lower().replace(" ", "_"), int(by.get(b, 0)))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
