"""Download Antwerp's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/antwerp/fetch_sources.py [--keep-vkbo] [--refresh-favv] [--refresh-feed]

Four sources, shared with Ghent where they can be (pipeline/countries/
belgium_fetch.py, fetch_city):

  * De Lijn's GTFS, one copy for both cities at data/belgium/raw/: the copy
    fetched 2026-10-03 and ratified by the owner, taken from the brief
    check's cache after its sha256 is checked. A new download
    (--refresh-feed) is the owner's call: the Belgian Mobility portal counts
    each access as accepting its terms;
  * FAVV-AFSCA's operator list, one copy for Belgium (--refresh-favv);
  * OpenStreetMap's communes in the rail box (cached; no query is sent while
    the cache exists);
  * VKBO, paged through the WFS for NIS 11002 and Borsbeek's 11007, the four
    fields and the point only, 5,000 rows a page, 1.5 s apart (--keep-vkbo
    reuses the cached pages).

Then outputs/antwerp/provenance.json, which the page's caption reads.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.antwerp import config  # noqa: E402
from pipeline.countries.belgium_fetch import fetch_city, fetch_tram_route_stops  # noqa: E402

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1:] == ["--left-bank-trams"]:
        # Only the one Overpass query naming the stops of lines 3, 9 and 15
        # (absent from the feed during works); nothing else is fetched or
        # rewritten. The stops found go in config.CLOSED_FOR_WORKS by hand.
        fetch_tram_route_stops(config.COMMUNES_BBOX, config.WORKS_ABSENT_TRAM_REFS,
                               config.OSM_WORKS_TRAMS_JSON)
    elif sys.argv[1:] == ["--all-tram-routes"]:
        # The broad query: every tram route relation in the box, any ref
        # (owner, 2026-10-04), when the narrow one returned none.
        fetch_tram_route_stops(config.COMMUNES_BBOX, None, config.OSM_ALL_TRAMS_JSON)
    else:
        fetch_city(config, sys.argv[1:])
