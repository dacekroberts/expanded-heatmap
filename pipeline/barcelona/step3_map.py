"""Step 3 - Render Barcelona's heatmap to a standalone HTML file.

Thin, like every other city's. Calls `load_osm_line_shapes` for the third time,
on different grounds again: Mexico City because every agency host is
unreachable, Guadalajara because the only feed is three years stale and missing
a line, Barcelona because the operator's feed is behind a free account and the
agency route would need four feeds where OSM needs one.

`label_focus` is the municipal boundary, reusing step 1's loader rather than
re-deriving it, so the map and the station scope cannot disagree about where
Barcelona is. It matters here: L8 and L10 Sud run well past the city to
Cornella, Sant Boi and El Prat, and L9 Sud reaches the airport, so without it
three labels would be dragged far from the rest of the network.
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.map_common import load_osm_line_shapes, render_heatmap   # noqa: E402
from pipeline.barcelona.step1_stations import canonical_ref, load_boundary  # noqa: E402
from pipeline.barcelona.config import (                                # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CENSUS_YEAR,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    OSM_ROUTES_JSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)


def refs_as_this_cache_spells_them():
    """canonical ref -> the exact `ref` string in the cached routes file.

    `load_osm_line_shapes` matches a relation by EXACT ref, and Barcelona's
    refs are not spelled the same everywhere: `overpass-api.de` writes `L10N`
    where `overpass.kumi.systems` writes `L10 Nord`. A hardcoded spelling would
    make the loader print a WARNING and carry on with one line missing - a
    silent loss, and the same failure this project already had when a stale
    GTFS feed dropped Guadalajara's Linea 4.

    So the spelling is resolved from the file actually being read, and a
    missing line raises.
    """
    data = json.loads(OSM_ROUTES_JSON.read_text(encoding="utf-8"))
    found = {}
    for rel in data.get("elements", []):
        raw = rel.get("tags", {}).get("ref")
        if raw:
            found.setdefault(canonical_ref(raw), raw)
    missing = [k for k in LINE_NAMES if k not in found]
    if missing:
        raise SystemExit(
            f"{OSM_ROUTES_JSON.name} has no relation for {missing}. Every line "
            "in LINE_NAMES must be drawable, or the map loses one silently.")
    return {k: found[k] for k in LINE_NAMES}


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, OSM_ROUTES_JSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run fetch_sources.py, then step1 and "
                     f"step2, first.")

    actual = refs_as_this_cache_spells_them()
    line_specs = {
        key: (actual[key], LINE_COLOURS[key], LINE_NAMES[key], None)
        for key in LINE_NAMES
    }

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title=("Metro de Barcelona: commercial density around the "
                   f"stations ({CENSUS_YEAR} premises census)"),
        city_name="Barcelona",
        system_name="Metro de Barcelona",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_osm_line_shapes(OSM_ROUTES_JSON, line_specs,
                                   "Metro de Barcelona"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=load_boundary(),
    )


if __name__ == "__main__":
    main()
