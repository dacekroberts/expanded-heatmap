"""Step 1 - Guadalajara's Tren Ligero stations, from OpenStreetMap.

Mexico's second city, and the one that shows what did NOT generalise from the
first. Same country, same register, same taxonomy, same licence - and a
different station object: Mexico City has 184 `railway=station` nodes,
Guadalajara has one. Here the stations are `railway=stop` with
`network=Mi Tren`, 96 nodes collapsing to 48 names at exactly 2 per name.

Why not GTFS: the only feed expired 2023-01-28 and predates Línea 4 (opened
2025-12-15) entirely. See config.py.

WHAT THIS STEP HAS THAT MEXICO CITY'S DOES NOT: gate 3. siteur.gob.mx answers,
so `PUBLISHED_STATIONS_PER_LINE` carries the operator's own figures and this
step checks OSM against them.
"""

import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.stations import verify_stations
from pipeline.guadalajara.config import (
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    LINE_NAMES,
    MUNICIPIOS_KEEP,
    OSM_BBOX,
    OSM_BOUNDARY_JSON,
    OSM_EXCLUDE_RAILWAY,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OSM_STATION_NETWORK,
    OSM_STATION_RAILWAY,
    OVERPASS_HOSTS,
    OVERPASS_USER_AGENT,
    PUBLISHED_STATIONS_PER_LINE,
    STATIONS_CSV,
    STATION_MUNICIPIOS_CSV,
)

# The four municipios together are ~1,150 km2 (Guadalajara 151, Zapopan 1,164
# ... the union is dominated by Zapopan and Tlajomulco). A wide band, because
# this is a union of four rather than one city, and the gate exists to catch a
# ring that did not close rather than to pin an exact figure.
BOUNDARY_AREA_KM2_MIN = 1_500.0
BOUNDARY_AREA_KM2_MAX = 4_500.0


def overpass(query, cache_path, label):
    if cache_path.exists():
        print(f"  {label}: cached {cache_path.name}")
        return json.loads(cache_path.read_text(encoding="utf-8"))
    last = None
    for attempt in range(2):
        for host in OVERPASS_HOSTS:
            try:
                r = requests.post(host, data={"data": query}, timeout=300,
                                  headers={"User-Agent": OVERPASS_USER_AGENT})
                print(f"  {label}: {host.split('/')[2]} HTTP {r.status_code} "
                      f"{len(r.content):,} bytes")
                if r.status_code == 200:
                    payload = r.json()
                    if not payload.get("elements"):
                        print(f"  {label}: 200 but EMPTY - not cached, next host")
                        last = "empty result"
                        time.sleep(3)
                        continue
                    cache_path.parent.mkdir(parents=True, exist_ok=True)
                    cache_path.write_text(r.text, encoding="utf-8")
                    return payload
                last = f"HTTP {r.status_code}"
            except Exception as exc:                    # noqa: BLE001
                print(f"  {label}: {host.split('/')[2]} {type(exc).__name__}")
                last = type(exc).__name__
            time.sleep(3)
    raise SystemExit(
        f"Every Overpass host failed for {label} (last: {last}). A fact about "
        "Overpass, not about Guadalajara - retry before concluding anything."
    )


# STATIONS COME FROM ROUTE-RELATION MEMBERSHIP, NOT FROM NODE LABELS, and this
# is the second time in two cities that a label filter lost real stations.
#
# The first version of this query was
# `node["railway"]["network"="Mi Tren"](bbox)`, which returned 96 nodes and
# **silently omitted every one of Línea 4's 8 stops**, because that line opened
# 2025-12-15 and its stop nodes carry no `network` tag at all. The result was a
# 49-station set with zero stations in Tlajomulco de Zúñiga - a map missing the
# same line the rejected GTFS feed was missing, arrived at by a different
# route. Mexico City's config says in capitals "MATCH ON THE MODE, NEVER ON THE
# NETWORK LABEL ALONE"; that warning sat in the previous city's config, which
# is not a file anyone opens while writing the next one.
#
# Membership in a named route relation is the strongest available evidence that
# a node is a station on a line, and it cannot omit a line that has a relation.
# The relations themselves ARE network-tagged (all 8 carry `Mi Tren`), so the
# filter is safe at relation level - it was only ever wrong at node level.
Q_STATIONS = f"""
[out:json][timeout:280];
relation["type"="route"]["route"~"^(light_rail|subway)$"]["network"="{OSM_STATION_NETWORK}"]({OSM_BBOX})->.routes;
node(r.routes);
out body;
"""

Q_ROUTES = f"""
[out:json][timeout:280];
(
  relation["type"="route"]["route"~"^(light_rail|subway)$"]["network"="{OSM_STATION_NETWORK}"]({OSM_BBOX});
);
out geom;
"""

# Mexican municipios are admin_level 6 in OSM; 8 is asked for too rather than
# assumed, because an empty result here would look like "no stations in scope"
# three steps later.
#
# THE BBOX IS LOAD-BEARING, and leaving it off produced a confidently wrong
# answer on the first run: an unbounded name search matched **Guadalajara in
# SPAIN** - also admin_level 6, also named Guadalajara - and the "keep the
# largest polygon" tie-breaker below then selected it on purpose, giving a
# 26,814 km2 "Guadalajara" against the municipio's ~151. The union-area gate
# caught it. Two lessons kept here rather than in a commit message: a name
# search without a geographic filter is a global search, and a tie-breaker on
# SIZE is exactly backwards when the wrong candidate is a province.
_NAMES = "|".join(MUNICIPIOS_KEEP)
Q_BOUNDARY = f"""
[out:json][timeout:280];
(
  relation["boundary"="administrative"]["admin_level"="6"]["name"~"^({_NAMES})$"]({OSM_BBOX});
  relation["boundary"="administrative"]["admin_level"="8"]["name"~"^({_NAMES})$"]({OSM_BBOX});
);
out geom;
"""


def _poly(rel):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer" and m.get("geometry")]
    if not lines:
        return None
    polys = list(polygonize(linemerge(MultiLineString(lines))))
    return unary_union(polys) if polys else None


def load_boundaries():
    """One polygon per municipio, plus their union."""
    data = overpass(Q_BOUNDARY, OSM_BOUNDARY_JSON, "boundaries")
    rels = [e for e in data["elements"] if e["type"] == "relation"]
    by_name = {}
    for rel in rels:
        name = rel["tags"].get("name")
        if name not in MUNICIPIOS_KEEP:
            continue
        geom = _poly(rel)
        if geom is None:
            continue
        # Several OSM relations can share a municipio name - typically the
        # municipio and a locality inside it. Keep the SMALLEST that still
        # contains the bbox's centre of gravity... in practice, keep the
        # smallest, because the failure mode here was a PROVINCE matching the
        # name (see Q_BOUNDARY) and size was what selected it. With the bbox
        # filter in place both candidates are local, and the municipio is the
        # larger of a municipio/locality pair - so assert instead of guessing.
        prev = by_name.get(name)
        if prev is not None:
            raise SystemExit(
                f"Two boundary relations named {name!r} inside the bbox "
                f"({prev.area:.4f} and {geom.area:.4f} sq deg). Do not pick by "
                "size - that is what selected Guadalajara, Spain on the first "
                "run. Inspect them and name the right admin_level explicitly."
            )
        by_name[name] = geom
    missing = [m for m in MUNICIPIOS_KEEP if m not in by_name]
    if missing:
        raise SystemExit(
            f"No usable boundary polygon for {missing}. All four are required: "
            "this is a regional build and a missing municipio would silently "
            "drop that municipio's stations."
        )
    union = unary_union(list(by_name.values()))
    area = (gpd.GeoSeries([union], crs=CRS_GEOGRAPHIC)
            .to_crs(CRS_PROJECTED).area.iloc[0] / 1e6)
    print(f"  boundaries: {len(by_name)} municipios, union {area:,.0f} km2")
    for name, g in by_name.items():
        a = (gpd.GeoSeries([g], crs=CRS_GEOGRAPHIC)
             .to_crs(CRS_PROJECTED).area.iloc[0] / 1e6)
        print(f"      {name:26s} {a:7,.0f} km2")
    if not BOUNDARY_AREA_KM2_MIN <= area <= BOUNDARY_AREA_KM2_MAX:
        raise SystemExit(
            f"union area {area:,.0f} km2 outside "
            f"{BOUNDARY_AREA_KM2_MIN:,.0f}-{BOUNDARY_AREA_KM2_MAX:,.0f} - the "
            "rings probably did not assemble."
        )
    return by_name, union


def main():
    print("=== Step 1: Guadalajara stations (OpenStreetMap) ===\n")
    print("Fetching OSM:")
    st_data = overpass(Q_STATIONS, OSM_STATIONS_JSON, "stations")
    rt_data = overpass(Q_ROUTES, OSM_ROUTES_JSON, "routes")
    by_muni, boundary = load_boundaries()

    nodes = [e for e in st_data["elements"] if e["type"] == "node" and "tags" in e]
    print(f"\nRaw Mi Tren railway nodes in bbox: {len(nodes):,}")
    tagged = pd.DataFrame([{
        "name": (e["tags"].get("name") or "").strip(),
        "railway": e["tags"].get("railway"),
        "latitude": e["lat"],
        "longitude": e["lon"],
    } for e in nodes])

    for bad in OSM_EXCLUDE_RAILWAY:
        n = int((tagged["railway"] == bad).sum())
        if n:
            print(f"  excluded railway={bad:18s} {n:5d}")
    platforms = tagged[tagged["railway"].isin(OSM_STATION_RAILWAY)
                       & (tagged["name"] != "")].copy()
    print(f"  railway={'/'.join(OSM_STATION_RAILWAY)} with a name: {len(platforms):,}")

    # A LINE-SUFFIX ALIAS, which is the project's third encounter with this
    # collapse mechanism after Calgary's suffixes and Toronto's conventions.
    # OSM carries "Independencia" and "Independencia L3" as separate names for
    # one station box - the spacing gate caught them at 4 m apart, which is not
    # two stations. Stripping a trailing " L<digit>" merges them.
    before_names = platforms["name"].nunique()
    platforms["name"] = platforms["name"].str.replace(r"\s+L\d+$", "", regex=True)
    merged = before_names - platforms["name"].nunique()
    if merged:
        print(f"  line-suffix alias merged {merged} name(s) "
              f"(e.g. 'Independencia L3' -> 'Independencia')")

    grouped = (platforms.groupby("name", as_index=False)
               .agg(latitude=("latitude", "mean"),
                    longitude=("longitude", "mean"),
                    nodes=("name", "size")))
    per = grouped["nodes"].value_counts().to_dict()
    print(f"\nCollapsed {len(platforms):,} stop positions -> {len(grouped):,} "
          f"stations by name")
    print(f"  nodes-per-name distribution: {per}")
    if set(per) != {2}:
        print("  NOTE not uniformly 2 per name - check the odd ones before "
              "trusting the collapse:")
        for _, r in grouped[grouped["nodes"] != 2].iterrows():
            print(f"      {r['name']:28s} {r['nodes']} nodes")

    # --- boundary filter, and WHICH municipio each station is in -----------
    gdf = gpd.GeoDataFrame(
        grouped,
        geometry=gpd.points_from_xy(grouped["longitude"], grouped["latitude"]),
        crs=CRS_GEOGRAPHIC)
    inside = gdf.within(boundary)
    kept = gdf[inside].copy()
    outside = gdf[~inside].copy()
    print(f"\nInside the four municipios: {len(kept):,}")
    print(f"Outside: {len(outside):,}")

    muni_of = []
    for geom in kept.geometry:
        hit = next((n for n, g in by_muni.items() if geom.within(g)), "(edge)")
        muni_of.append(hit)
    kept["municipio"] = muni_of
    print("\nStations per municipio (the regional-build record):")
    for m, n in kept["municipio"].value_counts().items():
        print(f"    {m:26s} {n:3d}")
    STATION_MUNICIPIOS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (kept.drop(columns="geometry").rename(columns={"name": "station"})
     [["station", "municipio", "latitude", "longitude"]]
     .sort_values(["municipio", "station"])
     .to_csv(STATION_MUNICIPIOS_CSV, index=False))
    print(f"  wrote {STATION_MUNICIPIOS_CSV.name}")

    if len(outside):
        b_proj = gpd.GeoSeries([boundary], crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).iloc[0]
        dist = (outside.to_crs(CRS_PROJECTED).geometry
                .apply(lambda g: g.distance(b_proj)).round(0))
        (outside.drop(columns="geometry")
         .assign(distance_outside_m=dist.values, lines="Mi Tren")
         .rename(columns={"name": "station"})
         [["station", "latitude", "longitude", "lines", "distance_outside_m"]]
         .sort_values("distance_outside_m", ascending=False)
         .to_csv(EXCLUDED_STATIONS_CSV, index=False))
        print(f"  wrote {EXCLUDED_STATIONS_CSV.name} ({len(outside)} excluded)")

    # --- the gates, including gate 3 ---------------------------------------
    print("\n--- station verification ---")
    rels = [e for e in rt_data["elements"] if e["type"] == "relation"]
    refs = sorted({r["tags"].get("ref") for r in rels if r["tags"].get("ref")})
    print(f"Route relations: {len(rels)} over {len(refs)} refs: {', '.join(refs)}")
    if len(rels) < 2 * len(LINE_NAMES):
        raise SystemExit(
            f"Only {len(rels)} route relations for {len(LINE_NAMES)} lines; "
            "expected 2 per line. An empty or partial Overpass result must "
            "fail here rather than pass silently.")
    missing = [r for r in refs if r not in LINE_NAMES]
    if missing:
        raise SystemExit(f"OSM refs with no name in LINE_NAMES: {missing}")

    actual = {}
    for ref in refs:
        mine = [r for r in rels if r["tags"].get("ref") == ref]
        best = max(mine, key=lambda x: sum(
            1 for m in x.get("members", ()) if str(m.get("role", "")).startswith("stop")))
        n = sum(1 for m in best.get("members", ())
                if str(m.get("role", "")).startswith("stop"))
        actual[LINE_NAMES[ref]] = n
    print(f"OSM stop-members per line: {actual}")
    print(f"SITEUR's published counts  : {PUBLISHED_STATIONS_PER_LINE}")
    print("  (SITEUR publishes no count for Líneas 1 or 3; none is invented)")

    st_out = kept.drop(columns="geometry").rename(columns={"name": "station"})
    verify_stations(
        city="Guadalajara",
        platforms=platforms,
        stations=st_out,
        crs_projected=CRS_PROJECTED,
        expected_per_line=PUBLISHED_STATIONS_PER_LINE,
        actual_per_line={k: v for k, v in actual.items()
                         if k in PUBLISHED_STATIONS_PER_LINE},
    )

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (st_out.sort_values("station")[["station", "latitude", "longitude"]]
     .to_csv(STATIONS_CSV, index=False))
    print(f"\nWrote {len(st_out)} stations to {STATIONS_CSV}")


if __name__ == "__main__":
    main()
