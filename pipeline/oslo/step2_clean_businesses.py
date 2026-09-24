"""Oslo step 2: Enhetsregisteret -> the storefronts located in the kommune.

    python pipeline/oslo/step2_clean_businesses.py

Thin over `pipeline/countries/norway_register.py`. Everything about reading
the register is national; what is Oslo's own lives in `config.py` - the kommune
number, the address file, the sanity box and the catch-all verdict.

What a reader should know before trusting the counts printed below:

  * the filter is each sub-unit's own LOCATION address, never the paged API's
    `kommunenummer`, which does not constrain it;
  * a sole trader's name is never shown - the pin carries the address;
  * the register is SN2025 (NACE Rev. 2.1), which files a web shop under the
    product it sells, so online-only sellers cannot be excluded by code.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.norway_register import build_storefronts
from pipeline.oslo import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Oslo", config.OSLO_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
