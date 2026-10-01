"""Riga step 2: two layers - food service from the excise register, shops and
services from the cadastre's trade premise groups (docs/build_briefs/riga.md).

Thin over `pipeline/countries/latvia_register.py` since 2026-09-30, when the
tram kit lifted this step there for Liepāja and Daugavpils; the control
(`scripts/latvia_register_control.py`) showed the output unchanged. What is
Riga's own is passed in here: its address points, its ATVK, its list of
degrading buildings.

Layer 1, `excise`: current licences at a still-open place in Riga whose place
type reads as food service, one row per ADDRESS and place type (a premises
holds several licences - alcohol, tobacco, beer - and the holder is never read,
so de-duplication cannot be by holder). Placed by joining the address to Riga's
own address points: exact, then with the unit after " - " dropped.

Layer 2, `cadastre`: premise groups of use class 1230 whose name reads as a shop
or a personal service (config.NAME_RULES, first match wins), placed at their
building's footprint centroid by building cadastre number; those in a building
the city lists as degrading are dropped.

Reads the cache and NEVER fetches.

    python pipeline/riga/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import latvia_register as LV  # noqa: E402
from pipeline.riga import config  # noqa: E402

FETCH = "pipeline/riga/fetch_sources.py"
ATVK = "0001000"


def need(name):
    return LV.need(config.DATA_RAW / name, FETCH)


def build():
    """Riga's storefront frame, written by main() and rebuilt by the control."""
    from pipeline.riga.step1_stations import city_polygon

    lut = LV.address_lut_gpkg(need("adreses.gpkg"), config.CRS_SOURCE_LV,
                              config.CRS_GEOGRAPHIC)
    layers = [
        LV.excise_layer(config, excise_csv=need("pdb_akclicences_odata.csv"), city="Rīga",
                        lut=lut, lut_label="Riga's address points"),
        LV.cadastre_layer(config, premisegroup_zip=need("premisegroup.zip"), atvk=ATVK,
                          kk_zip=need(f"{ATVK}_kk_shp.zip"), city="Riga",
                          degrading_gpkg=need("vidi_degradejosas_buves.gpkg")),
    ]
    _, _, poly = city_polygon()
    return LV.combine(config, layers, poly)


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = build()
    df.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    LV.utf8_console()
    main()
