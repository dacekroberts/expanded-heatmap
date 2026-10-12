"""THE TRAVEL SWITCH FOR EVERY CITY, IN ONE PLACE (owner, 2026-10-11).

`render_heatmap` asks `for_city(<city folder>)` for the Travel basemap's
arguments whenever a city's map step passes no `open_basemap` of its own, so
going live is one edit here and one re-render of the maps: the city files
stay untouched. **Switched off while `PACK_HOST` is None**: every map then
renders exactly as before (docs/decisions_drafts/basemap.md, 2026-10-11).

The host is expected to serve, under PACK_HOST:

    packs/<city folder>.pmtiles     one pack per city, range-readable
    lib/                            the five files of FULL_TRAVEL_GL_FILES
    lib/fonts/<font>/<range>.pbf    the Noto glyphs, with OFL.txt and
                                    TRADEMARKS.txt beside them
    lib/licenses/                   each library's license file

which is the layout of the upload folder
(data/_basemap_build/host_upload_2026-10/). A pack's reader-facing notices
are in docs/data_sources.md, "The Travel basemap".
"""

# The host's address, with no trailing slash, or None: the Travel view off.
PACK_HOST = None

# The local label language of each city, as @protomaps/basemaps 5.7.2 names
# it (its `lang` option; `name:<code>` in the pack). A city not listed has
# English labels only and no pill: the English-speaking countries, and
# Tbilisi and Dublin, whose local-language codes the style does not carry
# (Georgian) or readers would not expect over English (Irish). Where a
# country has more than one language the city's own is used; Barcelona and
# Palma take Spanish, since the style has no Catalan.
LOCAL_LANG = {
    "es": ["buenos_aires", "mendoza", "guadalajara", "mexico_city", "monterrey",
           "barcelona", "madrid", "palma"],
    "fr": ["angers", "avignon", "besancon", "bordeaux", "brest", "caen", "dijon", "grenoble",
           "le_havre", "le_mans", "lille", "marseille", "montpellier", "mulhouse", "nantes",
           "nice", "orleans", "paris", "reims", "rennes", "rouen", "saint_etienne",
           "strasbourg", "toulouse", "tours", "valenciennes",
           "brussels", "brussels_regional", "charleroi", "liege", "montreal", "geneva"],
    "nl": ["antwerp", "ghent", "amsterdam", "den_haag", "rotterdam"],
    "pt": ["belo_horizonte", "brasilia", "fortaleza", "porto_alegre", "recife",
           "rio_de_janeiro", "salvador", "santos", "sao_paulo"],
    "cs": ["brno", "liberec", "most", "olomouc", "ostrava", "plzen", "prague"],
    "da": ["aarhus", "copenhagen", "odense"],
    "de": ["berlin", "bremen", "gelsenkirchen", "zurich"],
    "el": ["thessaloniki"],
    "it": ["florence", "milan", "rome"],
    "lv": ["daugavpils", "liepaja", "riga"],
    "no": ["bergen", "oslo"],
    "ro": ["bucharest"],
    "sv": ["goteborg", "stockholm"],
    "zh-Hant": ["hong_kong", "taichung", "taipei", "taoyuan"],
    "ja": ["ageo_regional", "akita", "amagasaki", "chofu", "fuchu_tokyo", "fukui", "fukuoka",
           "fukushima", "fukuyama", "gifu", "hakodate", "hamamatsu", "higashimurayama",
           "higashiosaka", "higashiyamato", "himeji", "hino", "hirakata", "hiroshima",
           "ichinomiya", "itami", "iwaki", "kagoshima", "kakogawa", "kasukabe", "kawasaki",
           "kitakyushu", "kobe", "kochi", "kumamoto", "kurume", "kyoto", "maebashi",
           "matsuyama", "mito", "morioka", "nagasaki", "nara", "nishinomiya", "nishitokyo",
           "oita", "okayama", "osaka", "otsu", "sakai", "sapporo", "sasebo", "shimonoseki",
           "soka", "suita", "tachikawa", "takamatsu", "tama", "tokorozawa", "tokyo", "toyama",
           "toyonaka", "toyota", "tsu", "uji", "utsunomiya", "yokkaichi", "yokohama",
           "yokosuka"],
    "ko": ["ansan", "anyang", "bucheon", "busan", "daegu", "daejeon", "gimhae", "gimpo",
           "goyang", "gwangju", "incheon", "namyangju", "seongnam", "seoul", "siheung",
           "suwon", "uijeongbu", "yongin"],
}
# The pill's text where the code in capitals would not do.
PILL_TEXT = {"zh-Hant": "ZH"}

# Named ferry and cable-car routes that get a legend row in a city's Travel
# view, as [(kind, name)] with kind "ferry" or "aerialway". Every route is
# drawn and named along its line whether listed or not; a row is for a route
# a rider would look for by name. The pilot's two; the rest wait for the
# multi-route ferry work (drafts log, "Later, in order").
ROUTES = {
    "florence": [("ferry", "Arno Boat")],
    "avignon": [("ferry", "Bac du Rocher des Doms")],
}

_LANG_OF = {city: code for code, cities in LOCAL_LANG.items() for city in cities}
if len(_LANG_OF) != sum(len(v) for v in LOCAL_LANG.values()):
    raise ValueError("pipeline/travel_packs.py: a city is listed under two languages")


def for_city(city):
    """render_heatmap's `open_basemap` arguments for one city folder, or None
    while the Travel view is switched off."""
    if not PACK_HOST:
        return None
    from pipeline.map_common import FULL_TRAVEL_GL_FILES
    lang = _LANG_OF.get(city)
    return dict(
        pmtiles_url=f"{PACK_HOST}/packs/{city}.pmtiles",
        local_lang=lang, local_name=PILL_TEXT.get(lang),
        libs=[f"{PACK_HOST}/lib/{f}" for f in FULL_TRAVEL_GL_FILES],
        assets=f"{PACK_HOST}/lib",
        routes=list(ROUTES.get(city, ())),
    )
