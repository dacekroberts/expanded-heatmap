"""Download everything Kyoto's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/kyoto/fetch_sources.py [city|isj|mlit|osm|all] [--force]

  * city  - the City's pinned resources (config.PORTAL_RESOURCES) from
            data.city.kyoto.lg.jp ONLY (CC BY 4.0): the 2021 food list and
            every monthly list since (00414, 00541), and the barber, beauty and
            laundry lists (00530). The portal has no API: each file through its
            resource page's download button (japan_fetch.portal_file), checked
            by its magic bytes, an HTML page refused;
  * isj   - MLIT 位置参照情報 for the 11 wards, block (24.0a) and town-chōme
            (19.0b) (PDL 1.0);
  * mlit  - MLIT N02 railways and N03 Kyoto Prefecture administrative areas,
            into the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
            CC BY 4.0);
  * osm   - OpenStreetMap station and tram-stop names in the city's box (ODbL),
            through pipeline/osm.py.

A file already on disk is kept (the portal files were downloaded at the
2026-09-24 screen) and recorded, dated by its modification time; --force
re-downloads. Each file is recorded in outputs/kyoto/provenance.json (bytes,
sha256, when). The work is pipeline/countries/japan_fetch.py, shared by every
Japanese city.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import japan_fetch  # noqa: E402
from pipeline.kyoto import config  # noqa: E402

if __name__ == "__main__":
    japan_fetch.main(config, __doc__)
