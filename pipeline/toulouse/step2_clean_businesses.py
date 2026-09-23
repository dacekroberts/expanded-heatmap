"""Toulouse step 2: SIRENE -> the storefronts inside the commune.

    python pipeline/toulouse/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`. Everything about reading
SIRENE is national and shared with Paris, Marseille and the two French cities
after this one; what is Toulouse's own lives in `config.py` - the commune code
`31555`, the sanity bounding box, and the per-city catch-all verdict.

⚠ THIS CITY WITHHOLDS THE MOST. The brief measured `statutDiffusion` masking at
**16.0%** of Toulouse's rows against Paris's 8.5% - the highest of the six
French candidates - and France masks the name, the address AND the geolocation
together. So the usable set is materially smaller than the bucket count
suggests, and the drop is a property of the source rather than of this filter.
The counts printed below are the place to read it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_register import build_storefronts
from pipeline.toulouse import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Toulouse", config.TOULOUSE_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
