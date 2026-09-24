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
# N02_001 railway class · N02_002 operator type (1 = Shinkansen, 2 = JR
# conventional, 3 = public, 4 = private, 5 = third sector) · N02_003 line name
# · N02_004 operator · N02_005 station name. Station geometry is a LineString
# (the platform), so a station point is its centroid.
SHINKANSEN = "1"

N03_URL_TEMPLATE = "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2025/N03-20250101_{pref}_GML.zip"
N03_ZIP_TEMPLATE = "N03-20250101_{pref}_GML.zip"

# MLIT 位置参照情報, per municipality (ward): block level and town-chōme level.
ISJ_BLOCK_URL_TEMPLATE = "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/{code}-24.0a.zip"
ISJ_CHOME_URL_TEMPLATE = "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/{code}-19.0b.zip"

# The buildable cities (Band A, 2026-09-24). `wards` are 全国地方公共団体コード
# without the check digit, the keys of both N03 (`N03_007`) and the ISJ files.
# Tokyo is the 8 wards with a full, current food list (owner): the others
# publish none, or only partially (see docs/build_briefs/tokyo.md).
CITIES = {
    "tokyo": {"name": "東京都区部 (8 wards)", "pref": "13", "epsg": 32654,
              "wards": ["13102", "13103", "13104", "13106", "13108", "13110", "13112", "13113"]},
    "osaka": {"name": "大阪市", "pref": "27", "epsg": 32653,
              "wards": ["27102", "27103", "27104", "27106", "27107", "27108", "27109", "27111", "27113",
                        "27114", "27115", "27116", "27117", "27118", "27119", "27120", "27121", "27122",
                        "27123", "27124", "27125", "27126", "27127", "27128"]},
    "kobe": {"name": "神戸市", "pref": "28", "epsg": 32653,
             "wards": ["28101", "28102", "28105", "28106", "28107", "28108", "28109", "28110", "28111"]},
    "sapporo": {"name": "札幌市", "pref": "01", "epsg": 32654,
                "wards": [f"011{n:02d}" for n in range(1, 11)]},
    "fukuoka": {"name": "福岡市", "pref": "40", "epsg": 32652,
                "wards": [f"4013{n}" for n in range(1, 8)]},
    # Band A 2026-09-24 (owner), on a register rebuilt from its permit stream
    "kyoto": {"name": "京都市", "pref": "26", "epsg": 32653,
              "wards": [f"261{n:02d}" for n in range(1, 12)]},
}


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


def stations(include_shinkansen=False):
    """Every N02 station as a point (the platform's centroid), EPSG:4326, with
    the line and operator. The Shinkansen is dropped unless asked for. The
    centroid is taken in a projected CRS, never in degrees (the project's
    invariant). Web Mercator is enough for a platform-length line."""
    st = _read_geojson(N02_ZIP, N02_STATIONS)
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
    st = stations()
    st["inside"] = st.geometry.within(city)
    g = st.groupby(["N02_004", "N02_003", "N02_001", "N02_002"])
    out = g["inside"].agg(total="size", inside="sum").reset_index()
    out = out[out["inside"] > 0].copy()
    out["share"] = (out["inside"] / out["total"]).round(2)
    return out.sort_values(["share", "inside"]).rename(columns={
        "N02_004": "operator", "N02_003": "line", "N02_001": "class", "N02_002": "operator_type"})
