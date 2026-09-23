"""Paris step 2: SIRENE -> the storefronts inside the commune, with coordinates.

    python pipeline/paris/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`, the way every city's
`step3_map.py` is thin over `map_common.render_heatmap()`. SIRENE is ONE
national register, so the 250 lines this file used to hold were the same 250
lines the next four French cities would each need, with nothing keeping the
copies in agreement. Moved 2026-09-23 while building Marseille.

What remains Paris's own is in `config.py`: the commune prefix `751`, the
sanity bounding box, and the per-city catch-all verdict.

Reads the cache only; `fetch_sources.py` downloads. The two parquets it reads
are national and live in one shared country cache.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_register import build_storefronts
from pipeline.paris import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "Paris", config.PARIS_BBOX)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
