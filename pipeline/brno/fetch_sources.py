"""Download Brno's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/brno/fetch_sources.py

Thin over `pipeline/countries/czechia_fetch.py`. Everything rolling is fetched
fresh on every run: KORDIS's feed (republished weekly), the obec's RUIAN file
(named by month through ČÚZK's ATOM service) and the two OSM queries. The
national ROS02, RES and CZ-NACE files are checked in the shared cache, never
fetched from here.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.brno import config  # noqa: E402
from pipeline.countries import czechia_fetch as F  # noqa: E402


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    prov = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
            if config.PROVENANCE_JSON.exists() else {})

    print("National (shared by every Czech city, checked not fetched):")
    F.national(prov)

    print("\nBrno:")
    F.ruian(config, prov)
    F.download(config.GTFS_URL, config.GTFS_ZIP, "gtfs.zip (KORDIS JMK)", b"PK\x03\x04")
    F.record(prov, "gtfs", config.GTFS_ZIP, config.GTFS_URL, F.now())
    prov["gtfs_calendar"] = F.gtfs_calendar_window(config.GTFS_ZIP)
    prov["osm_boundary_host"] = F.osm_boundaries(config)
    prov["osm_tram_host"] = F.osm_trams(config)
    prov["osm_fetched"] = F.now()

    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")


if __name__ == "__main__":
    F.utf8_console()
    main()
