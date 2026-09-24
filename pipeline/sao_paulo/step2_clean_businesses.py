"""São Paulo step 2: CNEFE 2022 -> the storefronts the census enumerated in
município 3550308.

    python pipeline/sao_paulo/step2_clean_businesses.py

Thin over `pipeline/countries/brazil_register.py`. Everything about reading
CNEFE is national; what is São Paulo's own lives in `config.py` - the zip, the
sanity box - and in `boundary.py`, the polygon.

What a reader should know before trusting the counts printed below:

  * a row is one use-type at one address - a shopping centre is one pin or a
    few, not one per shop;
  * the categories are this project's reading of the enumerator's free text,
    and the fifth of rows no rule can read is dropped, more of them in
    affluent districts;
  * at an address that also holds a dwelling the pin shows its category only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.brazil_register import build_storefronts  # noqa: E402
from pipeline.sao_paulo import config  # noqa: E402
from pipeline.sao_paulo.boundary import city_polygon  # noqa: E402


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out, unclassified = build_storefronts(config, config.SP_BBOX,
                                          city_polygon(verbose=False))
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    unclassified.to_csv(config.UNCLASSIFIED_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    print(f"  {len(unclassified):,} unclassifiable points -> "
          f"{config.UNCLASSIFIED_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
