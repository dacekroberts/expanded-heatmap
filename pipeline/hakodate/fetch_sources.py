"""Download everything Hakodate's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/hakodate/fetch_sources.py [city|isj|mlit|osm|control|estat|all] [--force]

  * city    - the city's barber, beauty-salon and laundry registers, as of
              2026-08-31 (CC BY 2.1 JP, 「環境衛生関係施設等の情報」);
  * isj     - MLIT 位置参照情報 for 01202, block (24.0a) and town-chōme (19.0b)
              (PDL 1.0);
  * mlit    - MLIT N02-25 railways and N03 Hokkaido administrative areas, into
              the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY
              4.0);
  * osm     - OpenStreetMap station and tram-stop names in the city's box
              (ODbL), through pipeline/osm.py;
  * control - the Economic Census table (shared cache; the food control, which
              does not apply to this page, kept for the shared tooling);
  * estat   - e-Stat's 衛生行政報告例 FY2024 生活衛生 第10表 and 第11表, the
              official count the registers were measured against (a
              measurement only, never drawn; owner approved, 2026-10-02).

A file already on disk is kept (every file was downloaded at Step 0,
2026-10-02) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/hakodate/provenance.json (bytes,
sha256, when). The work is pipeline/countries/japan_fetch.py, shared by every
Japanese city; only the e-Stat control is this city's own.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.hakodate import config  # noqa: E402


def fetch_estat(force):
    """The two e-Stat CSVs (cp932) into data/hakodate/raw/, recorded."""
    for key, (name, url) in config.ESTAT_CONTROL.items():
        dest = config.DATA_RAW / name
        how = japan_fetch.get(url, dest, force)
        print(f"  {name:40s} {dest.stat().st_size:>8,} bytes  ({how})")
        japan_fetch.record(config, key, file=name, url=url, bytes=dest.stat().st_size,
                           sha256=japan_fetch.sha256(dest), retrieved=japan_fetch.when(dest), how=how,
                           use="measurement only (the official count), never drawn")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--force"]
    if args[:1] == ["estat"]:
        sys.stdout.reconfigure(encoding="utf-8")
        fetch_estat("--force" in sys.argv[1:])
    else:
        japan_fetch.main(config, __doc__)
        if not args or args[0] == "all":
            fetch_estat("--force" in sys.argv[1:])
