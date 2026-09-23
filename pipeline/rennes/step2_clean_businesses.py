"""Rennes step 2: SIRENE -> the storefronts inside the commune.

    python pipeline/rennes/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`. Everything about reading
SIRENE is national and shared with the four French cities before this one;
what is Rennes' own lives in `config.py` - the commune code `35238`, the
sanity bounding box, and the per-city catch-all verdict.

The brief measured Rennes as the best-named French city (53.5% of bucket rows
carry a premises name, against Paris's 39.6%) and the least masked after Paris
(9.8%), and as the smallest - roughly 4,800 bucket rows, a floor. The counts
printed below are the place to read all three.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_register import build_storefronts
from pipeline.rennes import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Rennes", config.RENNES_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
