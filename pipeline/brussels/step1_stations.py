"""Brussels step 1: STIB's metro, premetro and tram stations in the City.

    python pipeline/brussels/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads. The machinery (regular
routes, places, thinning, bilingual names) is shared with Brussels (Regional)
in `pipeline/countries/belgium_stib.py`; what is the City's own is here:

  * **The scope is the commune polygon (NIS 21004).**
  * **The corridor is the City's 25 underground stations, by name** (the
    City's entrances dataset). Botanique, Madou, Porte de Namur and Rogier lie
    under the Petite Ceinture, the commune's boundary, so a corridor station
    counts as inside by name; three of the 25 (Anneessens, Bourse, Lemonnier)
    are served by trams alone.
  * Stations outside are named with their commune from the Region's commune
    limits, or as outside the Region.
"""
import sys
from pathlib import Path

import geopandas as gpd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.brussels import config  # noqa: E402
from pipeline.countries.belgium import brussels_region_communes  # noqa: E402
from pipeline.countries.belgium_stib import base, build  # noqa: E402

FETCH = "pipeline/brussels/fetch_sources.py"


def main():
    com = brussels_region_communes(config.COMMUNES_GEOJSON, FETCH)
    city = com[com["nis"] == config.COMMUNE_CODE].geometry.union_all()
    area = float(gpd.GeoSeries([city], crs=config.CRS_GEOGRAPHIC)
                 .to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6)
    lo, hi = config.COMMUNE_AREA_KM2
    print(f"City of Brussels ({config.COMMUNE_CODE}): {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"the City's polygon is {area:.1f} km2, outside {lo}-{hi}")

    def inside_of(by_all, pts):
        inside = set(by_all.index[pts.within(city).values])
        return inside | {n for n in by_all.index if base(n) in config.CORRIDOR}

    def corridor_of(inside_names, underground):
        corridor = {n for n in inside_names if base(n) in config.CORRIDOR}
        missing = set(config.CORRIDOR) - {base(n) for n in corridor}
        if missing:
            sys.exit(f"corridor stations missing from the feed: {sorted(missing)}")
        return corridor

    def reason_outside(_name, pt):
        hit = com[com.contains(pt)]
        return (f"in {hit.iloc[0]['name_fr']} ({hit.iloc[0]['nis']}), outside the City of Brussels"
                if len(hit) == 1 else "outside the Brussels-Capital Region")

    build(config, label="Brussels", fetch=FETCH, inside_of=inside_of,
          corridor_of=corridor_of, reason_outside=reason_outside,
          corridor_count=config.CORRIDOR_COUNT)


if __name__ == "__main__":
    main()
