"""Prague step 2: ROS02 + RES + RUIAN -> the storefronts trading in obec 554782.

    python pipeline/prague/step2_clean_businesses.py

Thin over `pipeline/countries/czechia_register.py`. Everything about reading
the registers is national; what is Prague's own lives in `config.py` - the
obec, the sanity box and the catch-all verdict.

What a reader should know before trusting the counts printed below:

  * the location is the ESTABLISHMENT's (ROS02), never the owner's seat (RES);
  * the activity is the OWNER's single CZ-NACE 2025 code, inherited by every
    establishment it holds;
  * a natural person's premises at their own registered seat is excluded, and
    every other natural person's or partnership's pin shows its address.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.czechia_register import build_storefronts  # noqa: E402
from pipeline.prague import config  # noqa: E402


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, config.PRAGUE_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
