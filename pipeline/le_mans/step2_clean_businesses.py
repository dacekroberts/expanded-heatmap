"""Le Mans step 2: SIRENE -> the storefronts in scope.

    python pipeline/le_mans/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`, as every French city is;
what is Le Mans's own lives in `config.py`. Scaffolded by
scripts/scaffold_france_batch.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_register import build_storefronts
from pipeline.le_mans import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Le Mans", config.LE_MANS_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
