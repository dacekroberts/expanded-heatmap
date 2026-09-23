"""Lille (Regional) step 2: SIRENE -> the storefronts in the communes the
network serves.

    python pipeline/lille/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`, like every French city.
What is Lille's own lives in `config.py`: the eleven served communes' INSEE
codes (plus the two legacy codes SIRENE still carries a handful of rows under),
the sanity bounding box, and the per-city catch-all verdict.

THE FIRST FRENCH CITY WHOSE FILTER IS A SET RATHER THAN A PLACE. The same
shared function takes a tuple of exact codes where Paris and Marseille passed
one arrondissement prefix and Toulouse one commune - which is why it was
written to take a tuple from the start.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_register import build_storefronts
from pipeline.lille import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Lille (Regional)", config.LILLE_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
