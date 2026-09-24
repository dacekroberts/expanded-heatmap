"""Rio de Janeiro step 2: CNEFE 2022 -> the storefronts the census enumerated in the
scope - thin over pipeline/countries/brazil_register.py.

    python pipeline/rio_de_janeiro/step2_clean_businesses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.brazil_register import build_storefronts  # noqa: E402
from pipeline.rio_de_janeiro import config  # noqa: E402
from pipeline.rio_de_janeiro.boundary import city_polygon  # noqa: E402


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out, unclassified = build_storefronts(config, config.SANITY_BBOX, city_polygon(verbose=False))
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    unclassified.to_csv(config.UNCLASSIFIED_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts, {len(unclassified):,} unclassifiable points")


if __name__ == "__main__":
    main()
