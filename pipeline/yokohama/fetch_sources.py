"""Download everything Yokohama's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/yokohama/fetch_sources.py [city|isj|mlit|osm|all] [--force]

  * city  - the city's barber, beauty and laundry registers
            (環境衛生関係施設一覧, as of 2026-04-01; CC BY 4.0), one zip each
            holding 18 ward CSVs;
  * isj   - MLIT 位置参照情報 for the 18 wards, block (24.0a) and town-chōme
            (19.0b) (PDL 1.0);
  * mlit  - MLIT N02 railways and N03 Kanagawa administrative areas, into the
            country's shared cache data/japan/raw/ (N02 PDL 1.0, N03 CC BY 4.0);
  * osm   - OpenStreetMap station names in the city's box (ODbL), through
            pipeline/osm.py.

A file already on disk is kept (the registers were downloaded during
screening, 2026-09-24, and are byte-identical to the city's copies of
2026-09-30) and recorded, dated by its modification time; --force re-downloads.
Each file is recorded in outputs/yokohama/provenance.json (bytes, sha256, when).
The work is pipeline/countries/japan_fetch.py, shared by every Japanese city;
only the city part is Yokohama's own, because its registers are CSVs inside a
zip, which japan_register.city_rows does not read (it reads zipped .xlsx).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.yokohama import config  # noqa: E402


def fetch_city(config, force):
    for key, (name, url, page) in config.SOURCE_FILES.items():
        dest = config.source_csv(key)
        how = japan_fetch.get(url, dest, force)
        rows = list(config.source_rows(key))
        missing = [c for c in config.REQUIRED_COLUMNS[key] if c not in rows[0]]
        if missing:
            sys.exit(f"{dest.name}: header lacks {missing} - not the file the brief read")
        print(f"  {dest.name:22s} {dest.stat().st_size:>10,} bytes {len(rows):>7,} rows  ({how})")
        japan_fetch.record(config, f"city_{key}", file=name, url=url, dataset_page=page,
                           bytes=dest.stat().st_size, sha256=japan_fetch.sha256(dest), rows=len(rows),
                           as_of=japan_fetch.as_of(config, key),
                           retrieved=japan_fetch.when(dest), how=how)


if __name__ == "__main__":
    japan_fetch.PARTS["city"] = fetch_city
    japan_fetch.main(config, __doc__)
