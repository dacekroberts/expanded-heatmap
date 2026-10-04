"""Daejeon step 2: SEMAS's 상가(상권)정보 -> Daejeon's storefronts, each on the
register's own point.

    python pipeline/daejeon/step2_clean_businesses.py

Reads the country cache only (pipeline/countries/korea_sbiz_fetch.py). The
rules - the province member found by its rows, the columns read, the SEMAS
taxonomy (owner, 2026-09-29), the branch in the name, the Korean personal-name
pass - live in pipeline/countries/korea_sbiz.py, shared with Incheon and the
Gyeonggi satellites. The city is its five 구 by 시군구코드 (config); the
whole city is kept, so rows far from Line 1 add to the all-city layer and
nothing to the rings.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import korea_sbiz  # noqa: E402
from pipeline.daejeon import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out = korea_sbiz.storefronts(config.SEMAS_SIDO, config.SEMAS_SIGUNGU,
                                  sigungu_codes=config.SEMAS_SIGUNGU_CODES)
    kept = filter_to_storefront(out, config.TAXONOMY_SYSTEM)
    if len(kept) != len(out):
        sys.exit("filter_to_storefront dropped rows the buckets already decided")
    emit("storefronts", len(kept))
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    kept.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(kept):,} storefronts "
          f"(SEMAS edition {korea_sbiz.edition()})")


if __name__ == "__main__":
    main()
