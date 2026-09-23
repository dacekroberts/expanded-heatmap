"""Milan step 1: metro stations from ATM's own layers, filtered to the comune.

Rail is the agency's: ds535 (station points) and ds539 (alignments), with
ds533 as the station-to-route join. OpenStreetMap is not used - both of
osm-rail's first two steps passed.

Reads the cache and NEVER fetches.

    python pipeline/milan/step1_stations.py
"""
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.milan import config
from pipeline.stations import verify_stations


def load(path, what):
    if not path.exists():
        sys.exit(f"missing {what} at {path}.\n"
                 f"Run: python pipeline/milan/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def collapse_name(raw):
    """130 features -> ~125 physical stations.

    THREE RULES, because ATM models interchanges two incompatible ways and a
    distance threshold is wrong in BOTH directions: WAGNER and BUONARROTI sit
    277 m apart and are different stations, while LORETO M2 and LORETO M1 sit
    231 m apart and are one. So this is by name, per the brief's measurement.
    """
    name = str(raw).strip().upper()
    name = config.STATION_ALIASES.get(name, name)
    name = re.sub(config.STATION_NAME_SUFFIX, "", name).strip()
    return config.STATION_ALIASES.get(name, name)


def main():
    stops = load(config.METRO_STOPS_GEOJSON, "metro stops")
    seq = load(config.METRO_SEQUENCE_GEOJSON, "metro sequence")
    boundary = load(config.BOUNDARY_GEOJSON, "boundary")

    feats = stops["features"]
    print(f"ds535: {len(feats)} station features")

    rows = []
    for f in feats:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"][:2]
        rows.append({
            "raw_name": str(p.get("nome", "")).strip(),
            "station": collapse_name(p.get("nome", "")),
            "linee": str(p.get("linee", "")).strip(),
            "id_ferm": str(p.get("id_amat", p.get("id_ferm", ""))),
            "latitude": lat,
            "longitude": lon,
        })
    platforms = pd.DataFrame(rows)

    stations = (platforms.groupby("station", as_index=False)
                .agg(latitude=("latitude", "mean"),
                     longitude=("longitude", "mean"),
                     linee=("linee", lambda s: ",".join(sorted(
                         {x for v in s for x in str(v).split(",") if x.strip()}
                     )))))
    print(f"  collapsed {len(platforms)} features -> {len(stations)} stations")
    merged = platforms.groupby("station")["raw_name"].nunique()
    for name in sorted(merged[merged > 1].index):
        variants = sorted(set(platforms.loc[platforms.station == name,
                                            "raw_name"]))
        print(f"    merged: {name:26s} <- {variants}")

    verify_stations(city="Milan", platforms=platforms, stations=stations,
                    crs_projected=config.CRS_PROJECTED)

    # GATE 3, against the agency's OWN join table rather than against this
    # build's arithmetic - the only check outside the data, and the one that
    # caught Toronto.
    #
    # ds533 carries `percorso` and `id_ferm` but NOT `linea` - the line comes
    # from ds539, so this is a THREE-layer join, not two. And ds533's
    # `id_ferm` is a STRING ("906") where ds535's `id_amat` is an INT (869):
    # a raw join gives 130 of 130 misses, which reads as a scope problem
    # rather than a type one.
    lines = load(config.METRO_LINES_GEOJSON, "metro lines")
    percorso_line = {str(f["properties"]["percorso"]):
                     str(f["properties"]["linea"]).strip()
                     for f in lines["features"]}
    per_line = {}
    for f in seq["features"]:
        p = f["properties"]
        line = percorso_line.get(str(p.get("percorso", "")).strip())
        if line:
            per_line.setdefault(line, set()).add(str(p.get("id_ferm", "")))

    print("\n  stations per line, from ATM's own join table (gate 3):")
    for line in sorted(per_line):
        print(f"    M{line:5s} {len(per_line[line]):3d}")
    joined = set().union(*per_line.values()) if per_line else set()
    ours = set(platforms["id_ferm"])
    print(f"    union  {len(joined):3d}  (ds535 has {len(platforms)} features)")

    # A JOIN THAT MATCHES NOTHING MUST FAIL, NOT PASS. The first version of
    # this guarded `if total and ...`, so a zero-row join - which is what a
    # wrong column name or an uncast key produces - skipped the check
    # silently and printed "union 0" as though it were a finding.
    if not per_line:
        sys.exit("  ds533 x ds539 joined to NOTHING. That is a column-name or "
                 "key-type failure in this code, not a fact about Milan.")
    missed = joined - ours
    if len(missed) > 8:
        sys.exit(f"  {len(missed)} of {len(joined)} ids in ds533 are absent "
                 f"from ds535 - check the str/int cast on id_ferm before "
                 f"reading this as a real gap. Examples: {sorted(missed)[:6]}")
    print(f"    {len(joined & ours)} of {len(joined)} ids resolve into ds535")

    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations.longitude, stations.latitude),
        crs=config.CRS_GEOGRAPHIC)
    region = gpd.GeoDataFrame.from_features(boundary["features"],
                                            crs=config.CRS_GEOGRAPHIC)
    area = region.to_crs(config.CRS_PROJECTED).geometry.area.sum() / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    print(f"\nBoundary: {len(region)} feature(s), {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"  boundary area {area:.1f} km2 outside {lo}-{hi}. A ring "
                 f"that did not close returns a perfectly valid geometry and "
                 f"only fails when stations are counted.")

    one = region.geometry.union_all()
    inside = gdf[gdf.geometry.within(one)].copy()
    outside = gdf[~gdf.geometry.within(one)].copy()
    print(f"\nIn the comune: {len(inside)} of {len(gdf)}")
    print(f"Excluded (outside Milan): {len(outside)}")
    for name in sorted(outside["station"]):
        print(f"  {name}")

    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    out = (inside[["station", "latitude", "longitude", "linee"]]
           .sort_values("station").reset_index(drop=True))
    out.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\nwrote {config.STATIONS_CSV.name}  {len(out)} stations")

    excl = outside[["station", "latitude", "longitude"]].copy()
    excl["reason"] = "outside the Comune di Milano boundary"
    excl.sort_values("station").to_csv(config.EXCLUDED_STATIONS_CSV,
                                       index=False, encoding="utf-8")
    print(f"wrote {config.EXCLUDED_STATIONS_CSV.name}  {len(excl)} stations")

    # One feature per line, for map_common's GeoJSON loader. ds539 carries 31
    # alignment VARIANTS across five lines - short workings as well as
    # end-to-end runs - so the choice of which to draw is made here, from the
    # percorso ids the brief measured as longest, rather than left to step 3.
    picked = []
    for line_key, percorso in config.LINE_PERCORSI.items():
        match = [f for f in lines["features"]
                 if str(f["properties"].get("percorso")) == percorso]
        if not match:
            sys.exit(f"  percorso {percorso} for {line_key} is not in ds539. "
                     f"ATM has republished the layer and the alignment ids "
                     f"have moved; re-read the longest variant per line.")
        feat = dict(match[0])
        feat["properties"] = dict(feat["properties"], line=line_key)
        picked.append(feat)
        n_pts = len(feat["geometry"]["coordinates"])
        print(f"    {line_key}  percorso {percorso}  {n_pts:4d} vertices  "
              f"{feat['properties'].get('nome', '')[:44]}")
    config.LINES_GEOJSON.write_text(
        json.dumps({"type": "FeatureCollection", "features": picked}),
        encoding="utf-8")
    print(f"wrote {config.LINES_GEOJSON.name}  {len(picked)} lines")

    emit("metro_features", len(platforms))
    emit("lines_drawn", len(picked))
    emit("stations_collapsed", len(stations))
    emit("stations_in_comune", len(out))
    emit("stations_excluded", len(excl))


if __name__ == "__main__":
    main()
