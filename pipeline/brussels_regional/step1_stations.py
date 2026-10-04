"""Brussels (Regional) step 1: STIB's stations in the Region's other 18 communes.

    python pipeline/brussels_regional/step1_stations.py

Reads the cache only: STIB's feed and the Region's commune limits are the City
of Brussels page's downloads (`pipeline/brussels/fetch_sources.py`). The
machinery is shared in `pipeline/countries/belgium_stib.py`; what is this
page's own:

  * **The scope is the Brussels-Capital Region less the City of Brussels**:
    the 18 communes' polygons. The City's 25 underground stations are the
    Brussels page's, including the four under the Petite Ceinture whose
    platforms' mean point falls in Saint-Josse or Ixelles.
  * **The corridor is structural**: STIB's parent stations, the underground
    metro and premetro set, in scope (45 of 70).
  * Stations outside are named: in the City (on the Brussels page), or
    outside the Region.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.brussels_regional import config  # noqa: E402
from pipeline.countries.belgium import brussels_region_communes  # noqa: E402
from pipeline.countries.belgium_stib import base, build  # noqa: E402

FETCH = "pipeline/brussels/fetch_sources.py"


def main():
    com = brussels_region_communes(config.COMMUNES_GEOJSON, FETCH)
    scope = com[com["nis"] != config.CITY_COMMUNE_CODE]
    codes = sorted(scope["nis"])
    if hasattr(config, "SCOPE_CODES") and sorted(config.SCOPE_CODES) != codes:
        sys.exit(f"SCOPE_CODES {sorted(config.SCOPE_CODES)} differ from the Region less the City {codes}")
    area = float(scope.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    print(f"The 18 communes: {area:.1f} km2")
    if len(scope) != 18 or not 125 <= area <= 135:
        sys.exit(f"{len(scope)} communes, {area:.1f} km2: expected 18 and about 129.6 km2")
    region18 = scope.geometry.union_all()
    city = com[com["nis"] == config.CITY_COMMUNE_CODE].geometry.union_all()

    def inside_of(by_all, pts):
        inside = set(by_all.index[pts.within(region18).values])
        return {n for n in inside if base(n) not in config.CITY_CORRIDOR}

    def corridor_of(inside_names, underground):
        return {n for n in inside_names if base(n) in underground}

    def reason_outside(name, pt):
        if base(name) in config.CITY_CORRIDOR or city.contains(pt):
            return "in the City of Brussels (21004), outside the 18 communes: on the Brussels page"
        return "outside the Brussels-Capital Region"

    build(config, label="Brussels (Regional)", fetch=FETCH, inside_of=inside_of,
          corridor_of=corridor_of, reason_outside=reason_outside,
          corridor_count=config.CORRIDOR_COUNT)


if __name__ == "__main__":
    main()
