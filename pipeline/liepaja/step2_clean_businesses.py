"""Liepāja step 2: Riga's two layers, through `pipeline/countries/latvia_register.py`.

    python pipeline/liepaja/step2_clean_businesses.py

  * `excise`: VID's excise register (Riga's national cache), current licences
    at a still-open food place in Liepāja, one per address and kind, placed on
    VZD's national address file aw_eka.csv (exact, then with the unit after
    " - " dropped). The holder is never read.
  * `cadastre`: VZD's premise groups of use class 1230 in ATVK 0005000 whose
    name reads as a shop or a personal service (Riga's NAME_RULES), placed at
    the building's footprint by cadastre number. Liepāja publishes no list of
    degrading buildings, so none is dropped for that.

Both are kept inside the city polygon (step 1's). Reads the cache and NEVER
fetches.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import latvia_register as LV  # noqa: E402
from pipeline.liepaja import config  # noqa: E402
from pipeline.liepaja.step1_stations import FETCH, city_polygon  # noqa: E402


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    lut = LV.address_lut_aw_eka(LV.need(config.AW_EKA_CSV, FETCH), config.CITY_NAME_LV)
    layers = [
        LV.excise_layer(config, excise_csv=LV.need(config.EXCISE_CSV, "pipeline/riga/fetch_sources.py"),
                        city=config.CITY_NAME_LV, lut=lut, lut_label="VZD's address points"),
        LV.cadastre_layer(config, premisegroup_zip=LV.need(config.PREMISEGROUP_ZIP,
                                                           "pipeline/riga/fetch_sources.py"),
                          atvk=config.ATVK, kk_zip=LV.need(config.KK_ZIP, FETCH),
                          city=config.CITY_NAME_LV),
    ]
    df = LV.combine(config, layers, city_polygon())
    df.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    LV.utf8_console()
    main()
