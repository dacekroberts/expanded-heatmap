"""Japan: the facts shared by every Japanese city, measured 2026-09-24.

Profiled for ten cities at once: Tokyo, Osaka, Kobe, Sapporo and Fukuoka
buildable, plus five screened. The business leg is **each city's own
food-permit list** (and its 生活衛生 registers for personal services). Those
are per city, in per-city formats, and none is national. The coordinate leg
is a JOIN to MLIT's 位置参照情報 in `japan_register.py`. This module holds
the shared rest:

  * Rail: MLIT 国土数値情報 **N02** (railways), one national file, PDL 1.0.
    JR and the private railways INCLUDED (owner, 2026-09-24). **The
    Shinkansen EXCLUDED** (owner, 2026-09-24: long-distance travel between
    cities), as `N02_002 == "1"`.
  * Scope: **the city line only** (owner, 2026-09-24). Each permit list covers
    only its own city, so a station beyond the line would get an empty ring.
    The line is MLIT **N03** (administrative areas), the union of the city's
    ward polygons by `N03_007`. `stub_test()` measures what the cut does to
    each line; an urban line cut to a stub goes back to the owner.
  * Projected CRS per city: the UTM zone, never copied between cities.

**Nothing here fetches.** The URLs are for a city's `fetch_sources.py`, and
the readers read the shared cache (`data/japan/raw/`, gitignored).
"""
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
# ONE CACHE FOR THE COUNTRY, as France's and Norway's: N02 is national, and a
# prefecture's N03 serves every city in it.
SHARED_RAW = _ROOT / "data" / "japan" / "raw"

N02_URL = "https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip"
N02_ZIP = SHARED_RAW / "N02-24_GML.zip"
N02_STATIONS = "UTF-8/N02-24_Station.geojson"
N02_SECTIONS = "UTF-8/N02-24_RailroadSection.geojson"
# N02 EDITIONS, per city (Hiroshima, 2026-09-30): a city reads the edition its
# CITIES entry names ("n02"), N02-24 by default, so a newer edition moves no
# built city until its own drift check is run on it. N02-24 (MLIT metadata
# 2025-03-26) predates Hiroden's 駅前大橋線 (opened 2025-08-03): it still draws
# the abandoned 的場町-猿猴橋町-広島駅 track and the closed 猿猴橋町 stop. N02-25
# (published 2026-04-07, metadata 2026-03-06) has the new layout (no 猿猴橋町;
# 皆実線's new 松川町). Same columns and CRS; the zip nests its members one
# folder deeper. edition -> (URL, local zip, stations member, sections member)
N02_EDITIONS = {
    "24": (N02_URL, N02_ZIP, N02_STATIONS, N02_SECTIONS),
    "25": ("https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-25/N02-25_GML.zip", SHARED_RAW / "N02-25_GML.zip",
           "N02-25_GML/UTF-8/N02-25_Station.geojson", "N02-25_GML/UTF-8/N02-25_RailroadSection.geojson"),
}


def n02(slug=None):
    """The N02 edition a city reads: (URL, zip, stations member, sections member)."""
    return N02_EDITIONS[CITIES.get(slug, {}).get("n02", "24")]
# N02_001 railway class · N02_002 operator type (1 = Shinkansen, 2 = JR
# conventional, 3 = public, 4 = private, 5 = third sector) · N02_003 line name
# · N02_004 operator · N02_005 station name. Station geometry is a LineString
# (the platform), so a station point is its centroid.
SHINKANSEN = "1"

N03_URL_TEMPLATE = "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2025/N03-20250101_{pref}_GML.zip"
N03_ZIP_TEMPLATE = "N03-20250101_{pref}_GML.zip"

# The join CONTROL (owner's choice, 2026-09-24; the download approved
# 2026-09-28): the 2021 Economic Census for Business Activity, 第9-1A表
# 「産業(小分類)別全事業所数－全国、都道府県、市区町村」 - every ward's 飲食店
# (industry 76) establishments, all establishments (private and public), as of
# 2021-06-01. One national XLSX; column B is "<code>_<name>". The 2024 基礎調査
# table was not used: it drops sole traders with no employees, most small bars.
ESTAT_CENSUS_URL = "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040067884&fileKind=0"
ESTAT_CENSUS_XLSX = SHARED_RAW / "estat_census_r3_b1_009_1a.xlsx"

# MLIT 位置参照情報, per municipality (ward): block level and town-chōme level.
ISJ_BLOCK_URL_TEMPLATE = "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/{code}-24.0a.zip"
ISJ_CHOME_URL_TEMPLATE = "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/{code}-19.0b.zip"

# The buildable cities (Band A, 2026-09-24). `wards` are 全国地方公共団体コード
# without the check digit, the keys of both N03 (`N03_007`) and the ISJ files.
# Tokyo is the wards with a full, current food list (owner), read from
# pipeline/tokyo/wards.py - the one place a ward is switched on (2026-09-28);
# the others' stations are drawn hollow (their codes: tokyo_wards.NO_DATA_WARDS).
from pipeline.tokyo import wards as tokyo_wards  # noqa: E402 - dependency-free, no cycle
from pipeline.countries.japan_register import ALL_RULES, WAVE2_RULES  # noqa: E402 - no import back

CITIES = {
    "tokyo": {"name": "東京都区部", "pref": "13", "epsg": 32654, "rules": WAVE2_RULES,
              "wards": tokyo_wards.ACTIVE_CODES},
    # N02-25 since 2026-10-03 (owner): N02-24 lacks the Chūō Line's
    # Yumeshima, opened 2025-01-19.
    "osaka": {"name": "大阪市", "pref": "27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES,
              "wards": ["27102", "27103", "27104", "27106", "27107", "27108", "27109", "27111", "27113",
                        "27114", "27115", "27116", "27117", "27118", "27119", "27120", "27121", "27122",
                        "27123", "27124", "27125", "27126", "27127", "27128"]},
    "kobe": {"name": "神戸市", "pref": "28", "epsg": 32653, "rules": WAVE2_RULES,
             "wards": ["28101", "28102", "28105", "28106", "28107", "28108", "28109", "28110", "28111"]},
    "sapporo": {"name": "札幌市", "pref": "01", "epsg": 32654, "rules": WAVE2_RULES,
                "wards": [f"011{n:02d}" for n in range(1, 11)]},
    "fukuoka": {"name": "福岡市", "pref": "40", "epsg": 32652, "rules": WAVE2_RULES,
                "wards": [f"4013{n}" for n in range(1, 8)]},
    # Band A 2026-09-24 (owner), on a register rebuilt from its permit stream
    "kyoto": {"name": "京都市", "pref": "26", "epsg": 32653, "rules": WAVE2_RULES,
              "wards": [f"261{n:02d}" for n in range(1, 12)]},
    # Band B 2026-09-29 (owner): personal services only, the 18 wards
    "yokohama": {"name": "横浜市", "pref": "14", "epsg": 32654, "rules": WAVE2_RULES,
                 "wards": [f"141{n:02d}" for n in range(1, 19)]},
    # Band B 2026-09-29 (owner): food only, the 8 wards
    "hiroshima": {"name": "広島市", "pref": "34", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES,
                  "wards": [f"341{n:02d}" for n in range(1, 9)]},
    # Kansai-1 (the A/B build plan, 2026-10-07), each on N02-25 as its brief
    # measured, one municipality each ("wardless"), and the foundation's
    # ALL_RULES (no "rules" key).
    "toyonaka": {"name": "豊中市", "pref": "27", "epsg": 32653, "n02": "25", "wardless": True, "wards": ["27203"]},
    "hirakata": {"name": "枚方市", "pref": "27", "epsg": 32653, "n02": "25", "wardless": True, "wards": ["27210"]},
    "suita": {"name": "吹田市", "pref": "27", "epsg": 32653, "n02": "25", "wardless": True, "wards": ["27205"]},
    "itami": {"name": "伊丹市", "pref": "28", "epsg": 32653, "n02": "25", "wardless": True, "wards": ["28207"]},
    "kakogawa": {"name": "加古川市", "pref": "28", "epsg": 32653, "n02": "25", "wardless": True, "wards": ["28210"]},
    "amagasaki": {"name": "尼崎市", "pref": "28", "epsg": 32653, "n02": "25", "wardless": True, "wards": ["28202"]},
    "uji": {"name": "宇治市", "pref": "26", "epsg": 32653, "n02": "25", "wardless": True, "wards": ["26204"]},
    # The 2026-10-01 batch (owner released 2026-10-02), each on N02-25 as its
    # brief measured (Kagoshima's 仙巌園 and Fukui's Hapi-line are not in
    # N02-24; Sakai's Semboku line is under Nankai only in N02-25). "wardless":
    # one municipality, so an address is never split at a 区 (Toyama's 太田北区)
    # and MLIT keys every town under an empty ward.
    "matsuyama": {"name": "松山市", "pref": "38", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                  "wards": ["38201"]},
    "toyama": {"name": "富山市", "pref": "16", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
               "wards": ["16201"]},
    "kumamoto": {"name": "熊本市", "pref": "43", "epsg": 32652, "n02": "25", "rules": WAVE2_RULES,
                 "wards": [f"4310{n}" for n in range(1, 6)]},
    "fukui": {"name": "福井市", "pref": "18", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
              "wards": ["18201"]},
    "nagasaki": {"name": "長崎市", "pref": "42", "epsg": 32652, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                 "wards": ["42201"]},
    "utsunomiya": {"name": "宇都宮市", "pref": "09", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                   "wards": ["09201"]},
    "kitakyushu": {"name": "北九州市", "pref": "40", "epsg": 32652, "n02": "25", "rules": WAVE2_RULES,
                   "wards": ["40101", "40103", "40105", "40106", "40107", "40108", "40109"]},
    "sakai": {"name": "堺市", "pref": "27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES,
              "wards": [f"2714{n}" for n in range(1, 8)]},
    "hakodate": {"name": "函館市", "pref": "01", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                 "wards": ["01202"]},
    "kagoshima": {"name": "鹿児島市", "pref": "46", "epsg": 32652, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                  "wards": ["46201"]},
    "okayama": {"name": "岡山市", "pref": "33", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES,
                "wards": [f"3310{n}" for n in range(1, 5)]},
    "kochi": {"name": "高知市", "pref": "39", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
              "wards": ["39201"]},
    # Japan wave 2 (owner released 2026-10-02), each on N02-25 as its brief
    # measured. Hamamatsu's three wards are the 2024-01-01 ones (中央区 22138,
    # 浜名区 22139, 天竜区 22140): MLIT's ISJ and N03 key them so, and the old
    # seven codes answer 404. "rules": the join rules this wave added
    # (japan_register.WAVE2_RULES), opt-in at first; every Japanese city
    # reads them since 2026-10-04 (owner), the twenty above included.
    "kawasaki": {"name": "川崎市", "pref": "14", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES,
                 "wards": [f"1413{n}" for n in range(1, 8)]},
    "yokosuka": {"name": "横須賀市", "pref": "14", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                 "wards": ["14201"]},
    "himeji": {"name": "姫路市", "pref": "28", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
               "wards": ["28201"]},
    "nishinomiya": {"name": "西宮市", "pref": "28", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                    "wards": ["28204"]},
    "takamatsu": {"name": "高松市", "pref": "37", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                  "wards": ["37201"]},
    "toyota": {"name": "豊田市", "pref": "23", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
               "wards": ["23211"]},
    "yokkaichi": {"name": "四日市市", "pref": "24", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                  "wards": ["24202"]},
    "otsu": {"name": "大津市", "pref": "25", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
             "wards": ["25201"]},
    "nara": {"name": "奈良市", "pref": "29", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
             "wards": ["29201"]},
    "hamamatsu": {"name": "浜松市", "pref": "22", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES,
                  "wards": ["22138", "22139", "22140"]},
    "higashiosaka": {"name": "東大阪市", "pref": "27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                     "wards": ["27227"]},
    "kurume": {"name": "久留米市", "pref": "40", "epsg": 32652, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
               "wards": ["40203"]},
    "sasebo": {"name": "佐世保市", "pref": "42", "epsg": 32652, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
               "wards": ["42202"]},
    "shimonoseki": {"name": "下関市", "pref": "35", "epsg": 32652, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
                    "wards": ["35201"]},
}

# THE CITIES BUILT BEFORE THE JAPAN FOUNDATION (2026-10-07): they keep
# WAVE2_RULES, so their maps do not move; every city after them reads
# ALL_RULES (japan_register.WAVE5_RULES too). Leave a new city's "rules" out,
# or switch one rule off in "rules_off" with its reason ({rule: why}); a
# brief's `"rules": WAVE2_RULES` predates the foundation and is refused below.
# A built city moves to ALL_RULES only at a review time that re-renders it
# (docs/decisions_drafts/japan-foundation.md, the re-render proposal).
BUILT_BEFORE_FOUNDATION = frozenset({
    "tokyo", "osaka", "kobe", "sapporo", "fukuoka", "kyoto", "yokohama", "hiroshima", "matsuyama", "toyama",
    "kumamoto", "fukui", "nagasaki", "utsunomiya", "kitakyushu", "sakai", "hakodate", "kagoshima", "okayama",
    "kochi", "kawasaki", "yokosuka", "himeji", "nishinomiya", "takamatsu", "toyota", "yokkaichi", "otsu", "nara",
    "hamamatsu", "higashiosaka", "kurume", "sasebo", "shimonoseki"})


def city_rules(slug):
    """The japan_register rules a city reads: its CITIES "rules", or ALL_RULES
    less its "rules_off"."""
    c = CITIES.get(slug, {})
    return frozenset(c.get("rules", ALL_RULES)) - frozenset(c.get("rules_off", {}))


for _slug, _c in CITIES.items():
    _unknown = set(_c.get("rules", ())) | set(_c.get("rules_off", {}))
    if _unknown - ALL_RULES:
        raise ValueError(f"japan.CITIES[{_slug!r}]: unknown rule(s) {sorted(_unknown - ALL_RULES)}")
    if _slug not in BUILT_BEFORE_FOUNDATION and ALL_RULES - city_rules(_slug) - set(_c.get("rules_off", {})):
        raise ValueError(
            f"japan.CITIES[{_slug!r}] reads {sorted(ALL_RULES - city_rules(_slug))} off: a city built after the "
            f"Japan foundation (2026-10-07) reads every shared rule. Leave out \"rules\" (a brief's "
            f"\"rules\": WAVE2_RULES predates it), or name each rule off in \"rules_off\" with its reason.")


def prefecture_municipalities(pref):
    """Every municipality of a prefecture as an address may spell it, from N03's
    attributes (the shared cache, never fetched): a city (上尾市), a designated
    city whose wards N03 lists apart (札幌市), a town with and without its
    district (北足立郡伊奈町, 伊奈町). Read for japan_register's "other_muni" rule
    (the Japan foundation, 2026-10-07)."""
    import json
    import zipfile

    z = SHARED_RAW / N03_ZIP_TEMPLATE.format(pref=pref)
    if not z.exists():
        raise FileNotFoundError(f"{z} is missing - a city's fetch_sources.py downloads it")
    with zipfile.ZipFile(z) as zf:
        feats = json.loads(zf.read(z.name.replace("_GML.zip", ".geojson")))["features"]
    names = set()
    for f in feats:
        p = f["properties"]
        upper, muni = p.get("N03_003") or "", p.get("N03_004") or ""
        if upper.endswith("市"):
            names.add(upper)
        elif upper.endswith("郡") and muni:
            names |= {upper + muni, muni}
        elif muni:
            names.add(muni)
    return names


def osm_station_query(bbox):
    """The Overpass query for station NAMES in a city's box (S, W, N, E): which
    stations exist is N02's; OSM supplies name:en. Nodes and station ways, the
    ways by their centre (a big station is mapped as an area). Kobe's."""
    box = "({},{},{},{})".format(*bbox)
    return (f'[out:json][timeout:120];'
            f'(node["railway"~"^(station|halt)$"]{box};way["railway"="station"]{box};);out tags center;')


def osm_tram_stop_query(bbox):
    """OSM tags a tram stop railway=tram_stop, which osm_station_query does not
    take: without this, Osaka's 22 in-city Hankai stops have no name
    (2026-09-27). Any city with a tram N02 draws needs it (Sapporo's streetcar,
    Tokyo's Arakawa Line)."""
    box = "({},{},{},{})".format(*bbox)
    # `out body`, not `out tags`: a node's coordinates come only with its body
    return f'[out:json][timeout:120];node["railway"="tram_stop"]{box};out body;'


def _read_geojson(zip_path, member):
    import io
    import zipfile

    import geopandas as gpd

    if not Path(zip_path).exists():
        raise FileNotFoundError(f"{zip_path} is missing - a city's fetch_sources.py downloads it "
                                f"(this module never fetches)")
    with zipfile.ZipFile(zip_path) as zf:
        return gpd.read_file(io.BytesIO(zf.read(member)))


def city_boundary(slug, wards=None):
    """The city's own area: the union of its wards' N03 polygons, EPSG:4326.
    `wards` overrides the city's list, to measure a scope before choosing it.

    NEVER DRAW IT. Use it to pick stations and anchor labels only. N03 is CC BY
    4.0, but its boundaries derive from GSI survey data, and reproducing them
    as a map may need GSI's approval under the Survey Act (測量法). The licence
    read of 2026-09-24 left that open (`docs/data_sources.md`, Japan section)."""
    city = CITIES[slug]
    want = wards or city["wards"]
    z = SHARED_RAW / N03_ZIP_TEMPLATE.format(pref=city["pref"])
    n03 = _read_geojson(z, z.name.replace("_GML.zip", ".geojson"))
    wards = n03[n03["N03_007"].isin(want)]
    missing = set(want) - set(wards["N03_007"])
    if missing:
        raise ValueError(f"{slug}: N03 has no polygon for ward(s) {sorted(missing)}")
    return wards.to_crs(4326).union_all()


def stations(include_shinkansen=False, slug=None):
    """Every N02 station as a point (the platform's centroid), EPSG:4326, with
    the line and operator. The Shinkansen is dropped unless asked for. The
    centroid is taken in a projected CRS, never in degrees (the project's
    invariant). Web Mercator is enough for a platform-length line. `slug`
    picks the city's N02 edition (n02)."""
    _, zp, member, _ = n02(slug)
    st = _read_geojson(zp, member)
    if not include_shinkansen:
        st = st[st["N02_002"] != SHINKANSEN]
    st = st.to_crs(3857)
    st["geometry"] = st.geometry.centroid
    return st.to_crs(4326)


def stub_test(slug, wards=None):
    """Per line (operator + line name): stations in the whole network against
    stations inside the city line. The owner's test (after Rennes and Lille):
    an URBAN line the city line cuts to a stub goes back to the owner.
    Returns a DataFrame; judging which lines are urban is left to the reader.
    `wards` measures an alternative scope (Tokyo's, with and without Chiyoda)."""
    city = city_boundary(slug, wards)
    st = stations(slug=slug)
    st["inside"] = st.geometry.within(city)
    g = st.groupby(["N02_004", "N02_003", "N02_001", "N02_002"])
    out = g["inside"].agg(total="size", inside="sum").reset_index()
    out = out[out["inside"] > 0].copy()
    out["share"] = (out["inside"] / out["total"]).round(2)
    return out.sort_values(["share", "inside"]).rename(columns={
        "N02_004": "operator", "N02_003": "line", "N02_001": "class", "N02_002": "operator_type"})
