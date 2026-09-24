"""Copenhagen step 2: CVR + DAR -> the storefronts located in Kobenhavn and
Frederiksberg.

    python pipeline/copenhagen/step2_clean_businesses.py

Thin over `pipeline/countries/denmark_register.py`. Everything about reading
the registers is national; what is Copenhagen's own lives in `config.py` - the
two kommuner, the sanity box and the catch-all verdict.

What a reader should know before trusting the counts printed below:

  * the filter is each production unit's own LOCATION address
    (`beliggenhedsadresse`) and CVR's own kommune code on it, never a polygon;
  * CVR is a JOIN of six national files on `CVREnhedsId`, never on `pNummer`;
  * a personally owned business's name is never shown, nor any name carrying
    the sole-trader marker `v/` - the pin carries the address;
  * the register is DB25 (NACE Rev. 2.1), which files a web shop under the
    product it sells, so online-only sellers cannot be excluded by code.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.copenhagen import config  # noqa: E402
from pipeline.countries.denmark_register import build_storefronts  # noqa: E402


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, config.COPENHAGEN_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
