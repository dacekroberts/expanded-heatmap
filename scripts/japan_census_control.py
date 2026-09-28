"""The Economic Census join control for the Japanese cities (PLAN, "Join
control"; the owner's chosen control, 2026-09-24): Food service pins on the
map per ward, against the 2021 Economic Census's 飲食店 establishments in that
ward (japan_official.census(), industry 76, all establishments).

Establishments counted on the ground against the permits a list holds: a
list that is complete and placed well lands near the census in every ward,
and a ward far off either way says the join, the list or the scope is wrong
there. Not a share to publish - the census is 2021 and counts establishments,
not permits.

LIGHT BY DESIGN: the first attempt (2026-09-28) dissolved each prefecture's
whole N03 file and died with a MemoryError beside a drift check. This keeps
only the city's own ward polygons (N03_007 in japan.CITIES[slug]["wards"]),
dissolved per ward, and joins the pins point-in-polygon, one city at a time.
Still announce it as a heavy job (CLAUDE.md [#memory]).

Reads the cache (the city's businesses_clean.csv, N03, the census XLSX);
prints; touches nothing.

    python scripts/japan_census_control.py [city ...]     # default: every built Japanese city
"""
import gc
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import geopandas as gpd  # noqa: E402
import pandas as pd  # noqa: E402

from pipeline.countries import japan, japan_official  # noqa: E402
from pipeline.taxonomies import japan_eigyo  # noqa: E402

CITIES = ["kobe", "osaka", "sapporo", "fukuoka", "kyoto", "tokyo"]


def ward_polygons(slug):
    city = japan.CITIES[slug]
    z = japan.SHARED_RAW / japan.N03_ZIP_TEMPLATE.format(pref=city["pref"])
    n03 = japan._read_geojson(z, z.name.replace("_GML.zip", ".geojson"))
    n03 = n03[n03["N03_007"].isin(city["wards"])][["N03_004", "N03_005", "N03_007", "geometry"]].copy()
    n03["name"] = n03["N03_005"].fillna("").where(n03["N03_005"].fillna("") != "", n03["N03_004"])
    return n03.dissolve("N03_007", aggfunc="first").to_crs(4326)


def control(slug, census):
    path = Path(__file__).parent.parent / "data" / slug / "processed" / "businesses_clean.csv"
    if not path.exists():
        print(f"\n=== {slug}: no businesses_clean.csv - run its step 2 first")
        return None
    d = pd.read_csv(path, dtype=str, low_memory=False).fillna("")
    d = d[[japan_eigyo.classify(r) == "Food service" for r in d.to_dict("records")]]
    pts = gpd.GeoDataFrame(d[[]], geometry=gpd.points_from_xy(d["longitude"].astype(float),
                                                              d["latitude"].astype(float)), crs=4326)
    wards = ward_polygons(slug)
    w = wards[["name", "geometry"]].reset_index().rename(columns={"N03_007": "ward_code"})
    hit = gpd.sjoin(pts, w, predicate="within", how="left")
    per = hit["ward_code"].value_counts()
    print(f"\n=== {slug}: {len(d):,} Food service pins; {int(hit['ward_code'].isna().sum()):,} outside every ward")
    print(f"    {'ward':10} {'code':6} {'map':>7} {'census':>7} {'map/census':>10}")
    rows = []
    for code, w in wards.iterrows():
        n, c = int(per.get(code, 0)), census.get(code)
        rows.append((w["name"], code, n, c))
        ratio = f"{n / c:10.2f}" if c else "         —"
        print(f"    {w['name']:10} {code:6} {n:>7,} {c if c is not None else '—':>7} {ratio}")
    tn, tc = sum(r[2] for r in rows), sum(r[3] or 0 for r in rows)
    print(f"    {'ALL':10} {'':6} {tn:>7,} {tc:>7,} {tn / tc if tc else float('nan'):10.2f}")
    del d, pts, wards, hit
    gc.collect()
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    census = japan_official.census()
    if not census:
        sys.exit(f"missing {japan.ESTAT_CENSUS_XLSX} - python pipeline/<city>/fetch_sources.py control")
    print(f"control: {japan_official.CENSUS_SOURCE}; {len(census):,} municipalities")
    for slug in sys.argv[1:] or CITIES:
        control(slug, census)
        # its first version is a suspect in 2026-09-28's second crash: report
        # the peak, so a heavy run is measured, not assumed light
        try:
            import psutil
            print(f"    peak memory so far: {psutil.Process().memory_info().peak_wset / 2 ** 30:.2f} GB")
        except (ImportError, AttributeError):
            pass


if __name__ == "__main__":
    main()
