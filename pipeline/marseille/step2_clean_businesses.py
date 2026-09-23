"""Marseille step 2: SIRENE -> the storefronts inside the commune.

    python pipeline/marseille/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`. Everything about reading
SIRENE is national and shared with Paris and the three French cities after
this one; what is Marseille's own lives in `config.py` - the commune prefix
`132`, the sanity bounding box, and the per-city catch-all verdict.

This file existing as ten lines rather than 250 is the point: it was written
second, and a copy would have been the thing four more cities inherited.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_register import build_storefronts
from pipeline.marseille import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Marseille", config.MARSEILLE_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
