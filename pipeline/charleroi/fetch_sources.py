"""Install and verify Charleroi's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/charleroi/fetch_sources.py

Downloads nothing new. TEC's feed is installed from the copy the owner
ratified (a re-fetch after the Belgian Mobility portal's terms change is the
owner's call, since the portal counts access as acceptance); LoGIC's
GeoPackage is checked against its recorded sha256 (the SPW download, never the
MapServer); the commune polygons are OpenStreetMap's, read from the cache the
lead fetched (`belgium_fetch.fetch_communes` sends no query while the cache
exists). Writes outputs/charleroi/provenance.json, which the page caption reads.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.charleroi import config  # noqa: E402
from pipeline.countries import belgium_logic, belgium_tec  # noqa: E402
from pipeline.countries.belgium_fetch import fetch_communes  # noqa: E402


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("TEC's GTFS (the ratified copy):")
    tec = belgium_tec.install_feed()
    print(f"  {belgium_tec.FEED_ZIP.name}: feed_version {tec['feed_version']}, "
          f"{tec['feed_start_date']} to {tec['feed_end_date']}")
    print("\nLoGIC 2024 (the downloaded GeoPackage):")
    logic = belgium_logic.verify_logic()
    pts = belgium_logic.read_points(config.FETCH, ins=config.LOGIC_INS)
    first, last = belgium_logic.survey_window(pts)
    logic.update({"ins": config.LOGIC_INS, "points": len(pts),
                  "surveyed_from": first, "surveyed_to": last})
    print(f"  {len(pts):,} points with INS {config.LOGIC_INS}, surveyed {first} to {last}")
    print("\nOpenStreetMap communes (cache only):")
    if not config.OSM_COMMUNES_JSON.exists():
        sys.exit(f"{config.OSM_COMMUNES_JSON} missing: the Overpass query is the lead's "
                 f"(one per city, one in flight per session)")
    host = fetch_communes(config.COMMUNE_BBOX, config.OSM_COMMUNES_JSON, config.NIS)
    stamp = datetime.fromtimestamp(config.OSM_COMMUNES_JSON.stat().st_mtime, timezone.utc)
    prov = {
        "written_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tec_gtfs": tec,
        "logic": logic,
        "osm_communes": {"host": host, "bbox": config.COMMUNE_BBOX, "nis": config.NIS,
                         "file_utc": stamp.isoformat(timespec="seconds")},
    }
    # LF on Windows too: the file is committed.
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8", newline="\n")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
