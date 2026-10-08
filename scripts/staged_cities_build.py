"""Build docs/staged_cities.json: the cities ranked for screening but not yet
built, placed on the macro map so scripts/stress_overview.py can measure the
Overview at the size the site is heading for (owner, 2026-10-04).

The roster is the master list's "Unscreened, ranked" section
(docs/city_master_list.md). A staged entry is a planning record, never a
city: nothing in app/ reads this file, and a city's real cities.py entry is
written by its own build, with its own centre and name.

Japanese centres are the mean of the municipality's N02 station positions
(MLIT N02-24, inside the N03-2025 boundary), so a large municipality such as
Iwaki is centred on its rail, not its mountains; a municipality with no
station falls back to its polygon's representative point. Every other centre
is an approximate city centre typed by hand, good to a few kilometres, which
is all the macro map's zooms resolve.

    python scripts/staged_cities_build.py      # pipeline environment

Reads the shared cache under data/japan/raw/ (pipeline/countries/japan.py's
SHARED_RAW); fetches nothing.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.countries.japan import N02_ZIP, SHARED_RAW  # noqa: E402

OUT = ROOT / "docs" / "staged_cities.json"
UNIVERSE = ROOT / "docs" / "coverage_sweep" / "japan_universe_mhlw.csv"

# The eight traditional regions, by prefecture code.
JP8 = {**{"01": "Hokkaido"},
       **{f"{p:02d}": "Tohoku" for p in range(2, 8)},
       **{f"{p:02d}": "Kanto" for p in range(8, 15)},
       **{f"{p:02d}": "Chubu" for p in range(15, 24)},
       **{f"{p:02d}": "Kansai" for p in range(24, 31)},
       **{f"{p:02d}": "Chugoku" for p in range(31, 36)},
       **{f"{p:02d}": "Shikoku" for p in range(36, 40)},
       **{f"{p:02d}": "Kyushu-Okinawa" for p in range(40, 48)}}

# The prefectures with a view of their own on the macro map (app/cities.py's
# JAPAN_REGIONS); every other prefecture's cities sit in their region.
PREF_VIEWS = {"11": "Saitama Prefecture", "12": "Chiba Prefecture", "13": "Tokyo Metropolis",
              "27": "Osaka Prefecture", "28": "Hyogo Prefecture"}

# Japan wave 4 in the master list's order: (display name, municipality,
# prefecture code, station-group tier). Display names are provisional; a
# build may rename (Ōta and Ina share their names with other places).
JAPAN = [
    ("Tsu", "津市", "24", "15+"), ("Fukushima", "福島市", "07", "15+"),
    ("Ichihara", "市原市", "12", "15+"), ("Ichinomiya", "一宮市", "23", "15+"),
    ("Toyokawa", "豊川市", "23", "15+"), ("Aomori", "青森市", "02", "15+"),
    ("Ōita", "大分市", "44", "15+"), ("Fuji", "富士市", "22", "15+"),
    ("Akashi", "明石市", "28", "15+"), ("Fujisawa", "藤沢市", "14", "15+"),
    ("Asahikawa", "旭川市", "01", "15+"), ("Matsue", "松江市", "32", "15+"),
    ("Okazaki", "岡崎市", "23", "15+"), ("Kamakura", "鎌倉市", "14", "15+"),
    ("Suita", "吹田市", "27", "15+"),
    ("Iwaki", "いわき市", "07", "8-14"), ("Nagaoka", "長岡市", "15", "8-14"),
    ("Fuchū", "府中市", "13", "8-14"), ("Hachinohe", "八戸市", "02", "8-14"),
    ("Tachikawa", "立川市", "13", "8-14"), ("Uji", "宇治市", "26", "8-14"),
    ("Gifu", "岐阜市", "21", "8-14"), ("Hirakata", "枚方市", "27", "8-14"),
    ("Akita", "秋田市", "05", "8-14"), ("Amagasaki", "尼崎市", "28", "8-14"),
    ("Kawagoe", "川越市", "11", "8-14"), ("Kōriyama", "郡山市", "07", "8-14"),
    ("Kasugai", "春日井市", "23", "8-14"), ("Toyonaka", "豊中市", "27", "8-14"),
    ("Sakura", "佐倉市", "12", "8-14"), ("Ino", "いの町", "39", "8-14"),
    ("Nankoku", "南国市", "39", "8-14"), ("Hino", "日野市", "13", "8-14"),
    ("Ibaraki", "茨木市", "27", "8-14"), ("Imizu", "射水市", "16", "8-14"),
    ("Tokorozawa", "所沢市", "11", "8-14"), ("Tokushima", "徳島市", "36", "8-14"),
    ("Chōfu", "調布市", "13", "8-14"), ("Machida", "町田市", "13", "8-14"),
    ("Ōta", "太田市", "10", "8-14"), ("Kawaguchi", "川口市", "11", "8-14"),
    ("Higashimurayama", "東村山市", "13", "8-14"), ("Koshigaya", "越谷市", "11", "8-14"),
    ("Kakogawa", "加古川市", "28", "8-14"), ("Yamato", "大和市", "14", "8-14"),
    ("Kasukabe", "春日部市", "11", "8-14"),
    ("Tama", "多摩市", "13", "3-7"), ("Urayasu", "浦安市", "12", "3-7"),
    ("Yachiyo", "八千代市", "12", "3-7"), ("Itami", "伊丹市", "28", "3-7"),
    ("Moriguchi", "守口市", "27", "3-7"), ("Nagakute", "長久手市", "23", "3-7"),
    ("Minoh", "箕面市", "27", "3-7"), ("Kadoma", "門真市", "27", "3-7"),
    ("Ina", "伊奈町", "11", "3-7"), ("Nishitōkyō", "西東京市", "13", "3-7"),
    ("Isesaki", "伊勢崎市", "10", "3-7"), ("Higashiyamato", "東大和市", "13", "3-7"),
    ("Settsu", "摂津市", "27", "3-7"), ("Ageo", "上尾市", "11", "3-7"),
    ("Neyagawa", "寝屋川市", "27", "3-7"), ("Saga", "佐賀市", "41", "3-7"),
    ("Sōka", "草加市", "11", "3-7"), ("Tsukuba", "つくば市", "08", "3-7"),
    ("Nisshin", "日進市", "23", "3-7"), ("Urasoe", "浦添市", "47", "3-7"),
]

# The Japanese cities docs/build_plan_2026-10-07.md builds in phases 1 and 2
# that are not in the ranked roster above (briefed from earlier waves), so the
# macro map's Japanese views can be measured against what is actually coming
# (Staging's call 198, 2026-10-07). Same fields; the tier is not recorded.
PLANNED_EXTRA = [
    ("Maebashi", "前橋市", "10", ""), ("Fukuyama", "福山市", "34", ""),
    ("Mito", "水戸市", "08", ""), ("Morioka", "盛岡市", "03", ""),
    ("Sagamihara", "相模原市", "14", ""), ("Funabashi", "船橋市", "12", ""),
    ("Matsudo", "松戸市", "12", ""), ("Ichikawa", "市川市", "12", ""),
    ("Yao", "八尾市", "27", ""), ("Takatsuki", "高槻市", "27", ""),
    ("Shizuoka", "静岡市", "22", ""), ("Kanazawa", "金沢市", "17", ""),
    ("Matsumoto", "松本市", "20", ""), ("Tottori", "鳥取市", "31", ""),
    ("Yamagata", "山形市", "06", ""), ("Kure", "呉市", "34", ""),
]
JAPAN += PLANNED_EXTRA

# The plan's phase for each Japanese city it builds, under the roster's names
# (Fuchū is Fuchū (Tokyo), Ageo is Ageo (Regional), Ibaraki is Ibaraki
# (Osaka) in the plan). Absent means not in phases 1 or 2.
PLAN_PHASE = {
    **dict.fromkeys(["Higashiyamato", "Nishitōkyō", "Tama", "Higashimurayama", "Ageo",
                     "Sōka", "Tokorozawa", "Kasukabe", "Fuchū", "Chōfu", "Tachikawa", "Hino",
                     "Toyonaka", "Hirakata", "Suita", "Itami", "Kakogawa", "Amagasaki", "Uji",
                     "Maebashi", "Fukuyama", "Ichinomiya", "Tsu", "Fukushima", "Iwaki", "Akita",
                     "Ōita", "Gifu", "Mito", "Morioka"], 1),
    **dict.fromkeys(["Koshigaya", "Sagamihara", "Fujisawa", "Kawaguchi", "Funabashi", "Matsudo",
                     "Ichikawa", "Urayasu", "Sakura", "Yachiyo", "Ichihara", "Ibaraki", "Minoh",
                     "Moriguchi", "Kadoma", "Neyagawa", "Yao", "Takatsuki", "Shizuoka",
                     "Kanazawa", "Okazaki", "Aomori", "Matsue", "Fuji", "Matsumoto", "Tottori",
                     "Yamagata", "Kure"], 2),
}

# (display name, country, rank, region under today's scheme (Europe West or
#  Europe East by country since 2026-10-07), label tier,
#  mode, lat, lon). Approximate centres. The Greater Copenhagen Light Rail
# is not here: it extends Copenhagen's own page (owner, 2026-10-04), so it
# adds no dot; as a page of its own its dot sat 1.3-1.7 px from Copenhagen's.
OTHERS = [
    ("Arad", "Romania", 2, "Europe East", "minor", "tram", 46.19, 21.31),
    ("Brăila", "Romania", 2, "Europe East", "minor", "tram", 45.27, 27.96),
    ("Craiova", "Romania", 2, "Europe East", "minor", "tram", 44.32, 23.80),
    ("Galați", "Romania", 2, "Europe East", "minor", "tram", 45.44, 28.01),
    ("Oradea", "Romania", 2, "Europe East", "minor", "tram", 47.07, 21.92),
    ("Ploiești", "Romania", 2, "Europe East", "minor", "tram", 44.95, 26.04),
    ("Hódmezővásárhely", "Hungary", 2, "Europe East", "minor", "tram", 46.42, 20.33),
    ("Adana", "Türkiye", 4, "West Asia", None, "metro", 37.00, 35.32),
    ("Perugia", "Italy", 4, "Europe West", "minor", "light_rail", 43.11, 12.39),
    ("Johannesburg", "South Africa", 4, "Africa", None, "metro", -26.20, 28.05),
    ("Tshwane", "South Africa", 4, "Africa", "minor", "metro", -25.75, 28.23),
    ("Ekurhuleni", "South Africa", 4, "Africa", "minor", "metro", -26.17, 28.30),
    ("Thane", "India", 4, "South Asia", None, "metro", 19.22, 72.98),
    ("Mira-Bhayandar", "India", 4, "South Asia", "minor", "metro", 19.30, 72.85),
    ("Navi Mumbai", "India", 4, "South Asia", "minor", "metro", 19.03, 73.03),
    ("Ghaziabad", "India", 4, "South Asia", "minor", "metro", 28.67, 77.45),
    ("Memphis", "United States", 4, "United States East", "minor", "tram", 35.15, -90.05),
]


def japan_centres():
    codes = {}
    for line in UNIVERSE.read_text(encoding="utf-8").splitlines()[1:]:
        f = line.split(",")
        codes[(f[4][:2], f[1])] = f[4]
    want = {code: name for name, muni, pref, _ in JAPAN for code in [codes[(pref, muni)]]}
    stations = gpd.read_file(f"zip://{N02_ZIP}!UTF-8/N02-24_Station.geojson").to_crs(6668)
    stations["geometry"] = stations.geometry.to_crs(3857).centroid.to_crs(6668)
    out = {}
    for pref in sorted({c[:2] for c in want}):
        zip_path = SHARED_RAW / f"N03-20250101_{pref}_GML.zip"
        muni = gpd.read_file(f"zip://{zip_path}!N03-20250101_{pref}.geojson").to_crs(6668)
        # A designated city (Sagamihara, Shizuoka) is in N03 as its wards, each
        # with its own code; its rows carry the city's name in N03_004 (the
        # ward's in N03_005) and take the city's code here.
        by_name = {name: code for code, name in
                   ((c, n) for (p, n), c in codes.items() if p == pref) if code in want}
        ward = muni["N03_004"].isin(by_name) & ~muni["N03_007"].isin(want)
        muni.loc[ward, "N03_007"] = muni.loc[ward, "N03_004"].map(by_name)
        muni = muni[muni["N03_007"].isin(want)].dissolve("N03_007").reset_index()
        hits = gpd.sjoin(stations, muni[["N03_007", "geometry"]], predicate="within")
        for code, poly in zip(muni["N03_007"], muni.geometry):
            pts = hits[hits["N03_007"] == code].geometry
            if len(pts):
                lat, lon, how = pts.y.mean(), pts.x.mean(), f"mean of {len(pts)} N02 stations"
            else:
                p = poly.representative_point()
                lat, lon, how = p.y, p.x, "N03 representative point"
            out[want[code]] = (round(lat, 3), round(lon, 3), how)
    missing = set(want.values()) - set(out)
    assert not missing, missing
    return out


def main():
    centres = japan_centres()
    rows = []
    for name, muni, pref, tier in JAPAN:
        lat, lon, how = centres[name]
        jp8 = JP8[pref]
        rows.append({
            "name": name, "country": "Japan", "rank": 3, "municipality": muni,
            "pref": pref, "jp8": jp8,
            # The eight traditional regions, with five prefectures as views of
            # their own (owner, 2026-10-04 and 2026-10-07; app/cities.py's
            # JAPAN_REGIONS).
            "region": PREF_VIEWS.get(pref, jp8),
            "plan_phase": PLAN_PHASE.get(name),
            "label_tier": "minor", "mode": "light_rail", "station_groups": tier or None,
            "lat": lat, "lon": lon, "centre": how})
    for name, country, rank, region, tier, mode, lat, lon in OTHERS:
        rows.append({"name": name, "country": country, "rank": rank, "region": region,
                     "label_tier": tier, "mode": mode, "lat": lat, "lon": lon,
                     "centre": "approximate city centre"})
    doc = {"_about": ("Cities ranked for screening, not built: a planning record for "
                      "scripts/stress_overview.py. Nothing in app/ reads it. Built by "
                      "scripts/staged_cities_build.py from docs/city_master_list.md's "
                      "'Unscreened, ranked' section (2026-10-04). Mode and label tier are "
                      "guesses for the stress test; each build sets its own."),
           "cities": rows}
    OUT.write_bytes((json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(f"{len(rows)} staged cities -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
