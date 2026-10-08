"""One colour per transit line, site-wide: the lines more than one city's map
draws.

THE OWNER'S HARD LINE (2026-10-07): a line represented on more than one city
map gets its own distinct colour, the same on every map, even if other lines'
colours are reassigned to fit. Before this registry the JR Kobe Line was five
colours on six maps and the JR Sanyo Line four on six, because each Japanese
city chose its colours alone (scripts/line_colour_search.py, per city).

IDENTITY is operator plus public line, never a display name alone: Tram 1 in
Amsterdam and Tram 1 in Antwerp are different lines, and so are the Tozai
Lines of Kyoto, Sapporo and Tokyo (three operators). The JR Tokaido Line is
two identities, JR East's (Kawasaki, Yokohama) and JR Central's (Gifu,
Hamamatsu, Ichinomiya). One public line run by two operators is one identity:
the JR Sanyo Line is JR West's and, Shimonoseki to Moji, JR Kyushu's, and
Shimonoseki's map draws both stretches. A through-service a map names
differently is the same line: Yokohama's "JR Keihin-Tohoku / Negishi Line" is
the JR Keihin-Tohoku Line, Tokyo's "JR Yokosuka / Sobu Rapid Line" the JR
Yokosuka Line, and Tokyo's "JR Utsunomiya / Takasaki Line" one identity with
Utsunomiya's JR Utsunomiya Line and Ageo's JR Takasaki Line (JR East colours
the pair alike).

EACH ENTRY: the public name, the operator, the one colour, and `maps`
({city slug: that city's config line key}). A city's config reads a shared
line's colour from here (`line_registry.colour(<id>)`) and never holds its own
value for it. A line only one map draws has no entry.

HOW EACH COLOUR WAS CHOSEN (2026-10-07; the comment above each entry says
which, with its margins over every map that draws it):
  * already one colour on every map: kept;
  * else the operator's own line colour where it clears every constraint on
    every map and CIE76 45 from the pins (JR West's JR Kobe Line blue);
  * else the project colour one of its maps already drew that fits the most
    maps with the fewest reassignments;
  * else the colour nearest the operator's hue that fits every map.
The constraints on each map: CIE76 >= 20 from every pin colour the map draws
(the owner's floor), 3:1 contrast on both map pages, >= linecolour.HARD_FLOOR
from every other line on the map (>= 12 for a pair this change created), >= 18
from every line within 500 m, and dark-mode labels that
linecolour.dark_label_colours() can separate. Where a shared line's colour
collided, the OTHER (unshared) line on that map moved, hue kept; each city's
config records its moves. The full table, old colours and margins:
docs/decisions_drafts/line-registry.md.

INHERITED pages draw a parent page's lines in the parent's colours by import
(Brussels (Regional) imports Brussels' LINE_COLOURS), so one value already
serves both and they need no entries; scripts/check_line_identity.py still
compares the two maps line by line.

scripts/check_line_identity.py fails when a registered line's colour in any
config differs from its entry, and when two maps draw what looks like one line
(the same name over the same track, or a Japanese line of one operator under
one name) without an entry joining them or a NOT_SAME record parting them.
"""

# child page slug -> the page whose colours it imports
INHERITED = {"brussels_regional": "brussels"}

# {(city, key), (city, key)} pairs the check would take for one line that are
# two: none yet.
NOT_SAME = []

REGISTRY = {
    # the project's colour every map already drew (hue-matched to the operator); pins >= 30.3, lines >= 18.1, lines beside it >= 18.1.
    "hankai-line": {
        "name": "Hankai Line", "operator": "Hankai Tramway", "colour": "#449418",
        "maps": {"osaka": "RH", "sakai": "RH"},
    },
    # the project's colour amagasaki already drew; pins >= 45.2, lines >= 21.4, lines beside it >= 21.4.
    "hankyu-itami-line": {
        "name": "Hankyu Itami Line", "operator": "Hankyu", "colour": "#A04820",
        "maps": {"amagasaki": "HI", "itami": "HI"},
    },
    # the project's colour osaka already drew; pins >= 45.0, lines >= 16.4, lines beside it >= 18.0.
    "hankyu-kobe-line": {
        "name": "Hankyu Kobe Line", "operator": "Hankyu", "colour": "#C9785D",
        "maps": {"amagasaki": "HK", "kobe": "HQ", "nishinomiya": "HQ", "osaka": "HK"},
    },
    # the project's colour osaka already drew; pins >= 45.9, lines >= 18.0, lines beside it >= 18.0.
    "hankyu-kyoto-line": {
        "name": "Hankyu Kyoto Line", "operator": "Hankyu", "colour": "#87544B",
        "maps": {"kyoto": "HY", "osaka": "HY", "suita": "HY"},
    },
    # the project's colour osaka already drew; pins >= 45.8, lines >= 18.0, lines beside it >= 18.0.
    "hankyu-senri-line": {
        "name": "Hankyu Senri Line", "operator": "Hankyu", "colour": "#BA7E7B",
        "maps": {"osaka": "HS", "suita": "HS"},
    },
    # the project's colour osaka already drew; pins >= 45.4, lines >= 18.1, lines beside it >= 18.2.
    "hankyu-takarazuka-line": {
        "name": "Hankyu Takarazuka Line", "operator": "Hankyu", "colour": "#B7572D",
        "maps": {"osaka": "HT", "toyonaka": "HT"},
    },
    # the project's colour kobe already drew; pins >= 65.0, lines >= 16.8, lines beside it >= 19.6.
    "hanshin-main-line": {
        "name": "Hanshin Main Line", "operator": "Hanshin", "colour": "#3A6588",
        "maps": {"amagasaki": "SH", "kobe": "HS", "nishinomiya": "HS", "osaka": "SH"},
    },
    # the project's colour osaka already drew; pins >= 45.7, lines >= 18.3, lines beside it >= 25.3.
    "hanshin-namba-line": {
        "name": "Hanshin Namba Line", "operator": "Hanshin", "colour": "#4E665A",
        "maps": {"amagasaki": "SN", "osaka": "SN"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 45.7, lines >= 68.1, lines beside it >= 91.5.
    "ise-railway-ise-line": {
        "name": "Ise Railway Ise Line", "operator": "Ise Railway", "colour": "#9840A0",
        "maps": {"tsu": "IS", "yokkaichi": "IS"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 54.6, lines >= 18.8, lines beside it >= 18.8.
    "jr-west-biwako-line": {
        "name": "JR Biwako Line", "operator": "JR West", "colour": "#406878",
        "maps": {"kyoto": "JB", "otsu": "JB"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 54.7, lines >= 11.8, lines beside it >= 23.5.
    "jr-east-chuo-line": {
        "name": "JR Chuo Line", "operator": "JR East", "colour": "#F05820",
        "maps": {"hino": "JC", "tachikawa": "JC", "tokyo": "JC"},
    },
    # the project's colour kitakyushu already drew; pins >= 45.2, lines >= 18.3, lines beside it >= 18.3.
    "jr-kyushu-fukuhoku-yutaka-line": {
        "name": "JR Fukuhoku Yutaka Line", "operator": "JR Kyushu", "colour": "#A04820",
        "maps": {"fukuoka": "JS", "kitakyushu": "JF"},
    },
    # the project's colour higashiosaka, hirakata already drew; pins >= 46.0, lines >= 19.9, lines beside it >= 19.9.
    "jr-west-gakkentoshi-line": {
        "name": "JR Gakkentoshi Line", "operator": "JR West", "colour": "#C000A8",
        "maps": {"higashiosaka": "JG", "hirakata": "JG", "osaka": "JG"},
    },
    # the project's colour sapporo already drew; pins >= 24.5, lines >= 18.9, lines beside it >= 18.9.
    "jr-hokkaido-hakodate-main-line": {
        "name": "JR Hakodate Main Line", "operator": "JR Hokkaido", "colour": "#70A000",
        "maps": {"hakodate": "JH", "sapporo": "JH"},
    },
    # the project's colour osaka already drew; pins >= 41.1, lines >= 18.0, lines beside it >= 18.0.
    "jr-west-hanwa-line": {
        "name": "JR Hanwa Line", "operator": "JR West", "colour": "#CF8400",
        "maps": {"osaka": "JR", "sakai": "JR"},
    },
    # the project's colour kumamoto already drew; pins >= 46.3, lines >= 18.1, lines beside it >= 18.1.
    "jr-kyushu-hohi-main-line": {
        "name": "JR Hohi Main Line", "operator": "JR Kyushu", "colour": "#F05030",
        "maps": {"kumamoto": "JH", "oita": "HH"},
    },
    # the project's colour iwaki, tokyo already drew; pins >= 45.7, lines >= 18.8, lines beside it >= 18.8.
    "jr-east-joban-line": {
        "name": "JR Joban Line", "operator": "JR East", "colour": "#20A800",
        "maps": {"iwaki": "JB", "mito": "JJ", "tokyo": "JJ"},
    },
    # the project's colour fukuoka, kagoshima, kitakyushu, kumamoto already drew; pins >= 51.6, lines >= 18.1, lines beside it >= 18.1.
    "jr-kyushu-kagoshima-main-line": {
        "name": "JR Kagoshima Main Line", "operator": "JR Kyushu", "colour": "#E80010",
        "maps": {"fukuoka": "JK", "kagoshima": "JK", "kitakyushu": "JK", "kumamoto": "JK", "kurume": "JK"},
    },
    # the project's colour kawasaki, tokyo already drew; pins >= 50.6, lines >= 13.6, lines beside it >= 19.1.
    "jr-east-keihin-tohoku-line": {
        "name": "JR Keihin-Tohoku Line", "operator": "JR East", "colour": "#08A0C0",
        "maps": {"kawasaki": "JK", "tokyo": "JK", "yokohama": "JK"},
    },
    # JR West's own line colour; pins >= 82.7, lines >= 19.1, lines beside it >= 19.1.
    "jr-west-kobe-line": {
        "name": "JR Kobe Line", "operator": "JR West", "colour": "#0072BC",
        "maps": {"amagasaki": "JK", "himeji": "JA", "kakogawa": "JA", "kobe": "JK", "nishinomiya": "JK",
                 "osaka": "JK"},
    },
    # the project's colour kyoto already drew; pins >= 49.6, lines >= 18.8, lines beside it >= 18.8.
    "jr-west-kosei-line": {
        "name": "JR Kosei Line", "operator": "JR West", "colour": "#7098A8",
        "maps": {"kyoto": "JC", "otsu": "JC"},
    },
    # the project's colour kyoto already drew; pins >= 50.6, lines >= 17.5, lines beside it >= 18.8.
    "jr-west-kyoto-line": {
        "name": "JR Kyoto Line", "operator": "JR West", "colour": "#08A0C0",
        "maps": {"kyoto": "JA", "osaka": "JY", "suita": "JY"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 44.4, lines >= 81.8, lines beside it >= 90.7.
    "jr-kyushu-kyudai-main-line": {
        "name": "JR Kyudai Main Line", "operator": "JR Kyushu", "colour": "#30A800",
        "maps": {"kurume": "JQ", "oita": "KD"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 54.7, lines >= 33.6, lines beside it >= 33.6.
    "jr-east-musashino-line": {
        "name": "JR Musashino Line", "operator": "JR East", "colour": "#F05820",
        "maps": {"fuchu_tokyo": "JM", "higashimurayama": "JM", "tokorozawa": "JM"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 23.2, lines >= 19.1, lines beside it >= 19.1.
    "jr-east-nambu-line": {
        "name": "JR Nambu Line", "operator": "JR East", "colour": "#B09000",
        "maps": {"fuchu_tokyo": "JN", "kawasaki": "JN", "tachikawa": "JN", "yokohama": "JN"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 33.2, lines >= 21.5, lines beside it >= 27.1.
    "jr-west-nara-line": {
        "name": "JR Nara Line", "operator": "JR West", "colour": "#A87840",
        "maps": {"kyoto": "JD", "uji": "JD"},
    },
    # JR Kyushu's own line colour; pins >= 82.3, lines >= 37.2, lines beside it >= 40.4.
    "jr-kyushu-nippo-main-line": {
        "name": "JR Nippo Main Line", "operator": "JR Kyushu", "colour": "#0068B7",
        "maps": {"kagoshima": "JN", "kitakyushu": "JN", "oita": "NP"},
    },
    # the project's colour higashiosaka, suita already drew; pins >= 57.3, lines >= 18.8, lines beside it >= 22.5.
    "jr-west-osaka-higashi-line": {
        "name": "JR Osaka Higashi Line", "operator": "JR West", "colour": "#A088A0",
        "maps": {"higashiosaka": "JH", "osaka": "OH", "suita": "OH"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 53.6, lines >= 45.4, lines beside it >= 45.4.
    "jr-east-ou-line": {
        "name": "JR Ou Line", "operator": "JR East", "colour": "#E07800",
        "maps": {"akita": "OU", "fukushima": "OU"},
    },
    # the project's colour fukuyama, okayama, shimonoseki already drew; pins >= 51.4, lines >= 15.8, lines beside it >= 18.8.
    "jr-west-sanyo-line": {
        "name": "JR Sanyo Line", "operator": "JR West and JR Kyushu", "colour": "#007890",
        "maps": {"fukuyama": "JS", "himeji": "JS", "hiroshima": "JS", "kitakyushu": "JS", "okayama": "JS",
                 "shimonoseki": "JS"},
    },
    # the project's colour amagasaki, itami, kobe already drew; pins >= 20.1, lines >= 19.5, lines beside it >= 35.2.
    "jr-west-takarazuka-line": {
        "name": "JR Takarazuka Line", "operator": "JR West", "colour": "#A8903C",
        "maps": {"amagasaki": "JT", "itami": "JT", "kobe": "JT", "nishinomiya": "JT"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 25.2, lines >= 56.3, lines beside it >= 56.3.
    "jr-east-tohoku-line": {
        "name": "JR Tohoku Line", "operator": "JR East", "colour": "#007430",
        "maps": {"fukushima": "TH", "morioka": "TH"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 53.6, lines >= 12.0, lines beside it >= 24.4.
    "jr-east-tokaido-line": {
        "name": "JR Tokaido Line", "operator": "JR East", "colour": "#E07800",
        "maps": {"kawasaki": "JT", "yokohama": "JT"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 62.6, lines >= 16.1, lines beside it >= 19.1.
    "jr-central-tokaido-line": {
        "name": "JR Tokaido Line", "operator": "JR Central", "colour": "#E86810",
        "maps": {"gifu": "TK", "hamamatsu": "JT", "ichinomiya": "TK"},
    },
    # the project's colour osaka already drew; pins >= 45.1, lines >= 19.9, lines beside it >= 19.9.
    "jr-west-tozai-line": {
        "name": "JR Tōzai Line", "operator": "JR West", "colour": "#FF21C0",
        "maps": {"amagasaki": "JH", "osaka": "JH"},
    },
    # the colour nearest the operator's #FFDD00 that clears every map (none drawn before did); pins >= 45.2, lines >= 15.2, lines beside it >= 24.4.
    "jr-east-tsurumi-line": {
        "name": "JR Tsurumi Line", "operator": "JR East", "colour": "#A05000",
        "maps": {"kawasaki": "JI", "yokohama": "JI"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 53.6, lines >= 11.0, lines beside it >= 18.3.
    "jr-east-utsunomiya-takasaki-line": {
        "name": "JR Utsunomiya / Takasaki Line", "operator": "JR East", "colour": "#E07800",
        "maps": {"ageo_regional": "JT", "tokyo": "JU", "utsunomiya": "JU"},
    },
    # the project's colour osaka already drew; pins >= 45.0, lines >= 18.1, lines beside it >= 18.1.
    "jr-west-yamatoji-line": {
        "name": "JR Yamatoji Line", "operator": "JR West", "colour": "#12A500",
        "maps": {"nara": "JY", "osaka": "JQ"},
    },
    # JR East's own line colour; pins >= 82.5, lines >= 12.7, lines beside it >= 23.4.
    "jr-east-yokosuka-line": {
        "name": "JR Yokosuka Line", "operator": "JR East", "colour": "#0070B9",
        "maps": {"kawasaki": "JO", "tokyo": "JO", "yokohama": "JO", "yokosuka": "JO"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 50.6, lines >= 70.8, lines beside it >= 70.8.
    "jr-shikoku-yosan-line": {
        "name": "JR Yosan Line", "operator": "JR Shikoku", "colour": "#08A0C0",
        "maps": {"matsuyama": "JY", "takamatsu": "JY"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 25.2, lines >= 16.4, lines beside it >= 45.2.
    "keihan-keishin-line": {
        "name": "Keihan Keishin Line", "operator": "Keihan", "colour": "#949054",
        "maps": {"kyoto": "KK", "otsu": "KK"},
    },
    # the project's colour osaka already drew; pins >= 37.3, lines >= 16.4, lines beside it >= 18.0.
    "keihan-main-line": {
        "name": "Keihan Main Line", "operator": "Keihan", "colour": "#7B7B5A",
        "maps": {"hirakata": "KM", "kyoto": "KM", "osaka": "KM"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 45.7, lines >= 18.8, lines beside it >= 70.3.
    "keihan-uji-line": {
        "name": "Keihan Uji Line", "operator": "Keihan", "colour": "#20A800",
        "maps": {"kyoto": "KU", "uji": "KU"},
    },
    # the project's colour kawasaki, yokohama, yokosuka already drew; pins >= 45.5, lines >= 13.3, lines beside it >= 18.1.
    "keikyu-main-line": {
        "name": "Keikyu Main Line", "operator": "Keikyu", "colour": "#E81820",
        "maps": {"kawasaki": "KK", "tokyo": "KK", "yokohama": "KK", "yokosuka": "KK"},
    },
    # the project's colour chofu, fuchu_tokyo, hino, tama already drew; pins >= 64.6, lines >= 16.6, lines beside it >= 29.8.
    "keio-line": {
        "name": "Keio Line", "operator": "Keio", "colour": "#B030D0",
        "maps": {"chofu": "KO", "fuchu_tokyo": "KO", "hino": "KO", "tama": "KO", "tokyo": "KO"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 45.2, lines >= 31.3, lines beside it >= 31.3.
    "keio-sagamihara-line": {
        "name": "Keio Sagamihara Line", "operator": "Keio", "colour": "#F000B8",
        "maps": {"chofu": "KS", "kawasaki": "KO", "tama": "KS"},
    },
    # the project's colour nara already drew; pins >= 46.4, lines >= 12.2, lines beside it >= 18.2.
    "kintetsu-kyoto-line": {
        "name": "Kintetsu Kyoto Line", "operator": "Kintetsu", "colour": "#F85838",
        "maps": {"kyoto": "KT", "nara": "KT", "uji": "KT"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 46.2, lines >= 18.3, lines beside it >= 18.3.
    "kintetsu-nagoya-line": {
        "name": "Kintetsu Nagoya Line", "operator": "Kintetsu", "colour": "#E00018",
        "maps": {"tsu": "KN", "yokkaichi": "KN"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 46.2, lines >= 18.3, lines beside it >= 18.3.
    "kintetsu-nara-line": {
        "name": "Kintetsu Nara Line", "operator": "Kintetsu", "colour": "#E00018",
        "maps": {"higashiosaka": "KN", "nara": "KN"},
    },
    # the project's colour tsu already drew; pins >= 46.4, lines >= 16.5, lines beside it >= 18.3.
    "kintetsu-osaka-line": {
        "name": "Kintetsu Osaka Line", "operator": "Kintetsu", "colour": "#F85838",
        "maps": {"higashiosaka": "KO", "osaka": "KO", "tsu": "KO"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 45.5, lines >= 38.1, lines beside it >= 120.0.
    "kita-osaka-kyuko-namboku-line": {
        "name": "Kita-Osaka Kyuko Namboku Line", "operator": "Kita-Osaka Kyuko", "colour": "#E81820",
        "maps": {"suita": "KK", "toyonaka": "KK"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 51.6, lines >= 18.1, lines beside it >= 18.1.
    "meitetsu-nagoya-main-line": {
        "name": "Meitetsu Nagoya Main Line", "operator": "Meitetsu", "colour": "#E80010",
        "maps": {"gifu": "NH", "ichinomiya": "NH"},
    },
    # the project's colour osaka already drew; pins >= 45.1, lines >= 16.5, lines beside it >= 18.0.
    "osaka-metro-midosuji-line": {
        "name": "Midōsuji Line", "operator": "Osaka Metro", "colour": "#E4151E",
        "maps": {"osaka": "M", "sakai": "M"},
    },
    # the project's colour sakai already drew; pins >= 23.2, lines >= 20.5, lines beside it >= 20.5.
    "nankai-koya-line": {
        "name": "Nankai Kōya Line", "operator": "Nankai", "colour": "#B09000",
        "maps": {"osaka": "NK", "sakai": "NK"},
    },
    # the project's colour osaka already drew; pins >= 30.4, lines >= 18.0, lines beside it >= 18.0.
    "nankai-main-line": {
        "name": "Nankai Main Line", "operator": "Nankai", "colour": "#9F6900",
        "maps": {"osaka": "NM", "sakai": "NM"},
    },
    # the project's colour fukuoka already drew; pins >= 54.0, lines >= 18.3, lines beside it >= 83.7.
    "nishitetsu-tenjin-omuta-line": {
        "name": "Nishitetsu Tenjin Omuta Line", "operator": "Nishitetsu", "colour": "#688090",
        "maps": {"fukuoka": "NT", "kurume": "NT"},
    },
    # the project's colour tokyo already drew; pins >= 56.4, lines >= 10.3, lines beside it >= 19.6.
    "odakyu-odawara-line": {
        "name": "Odakyu Odawara Line", "operator": "Odakyu", "colour": "#687888",
        "maps": {"kawasaki": "OH", "tokyo": "OH"},
    },
    # the colour nearest the operator's #2288CC that clears every map (none drawn before did); pins >= 77.0, lines >= 12.7, lines beside it >= 35.1.
    "odakyu-tama-line": {
        "name": "Odakyu Tama Line", "operator": "Odakyu", "colour": "#2890D8",
        "maps": {"kawasaki": "OT", "tama": "OT"},
    },
    # the project's colour osaka already drew; pins >= 23.3, lines >= 18.5, lines beside it >= 28.3.
    "osaka-metro-chuo-line": {
        "name": "Osaka Metro Chuo Line", "operator": "Osaka Metro", "colour": "#5D662A",
        "maps": {"higashiosaka": "C", "osaka": "C"},
    },
    # Osaka Monorail's own line colour; pins >= 81.9, lines >= 37.6, lines beside it >= 37.6.
    "osaka-monorail-main-line": {
        "name": "Osaka Monorail Main Line", "operator": "Osaka Monorail", "colour": "#0067B0",
        "maps": {"itami": "MO", "suita": "MO", "toyonaka": "MO"},
    },
    # the project's colour himeji, kakogawa already drew; pins >= 45.4, lines >= 18.9, lines beside it >= 18.9.
    "sanyo-electric-main-line": {
        "name": "Sanyo Electric Main Line", "operator": "Sanyo Electric Railway", "colour": "#D01810",
        "maps": {"himeji": "SM", "kakogawa": "SM", "kobe": "SM"},
    },
    # the project's colour higashiyamato, tachikawa already drew; pins >= 50.6, lines >= 48.5, lines beside it >= 48.5.
    "seibu-haijima-line": {
        "name": "Seibu Haijima Line", "operator": "Seibu", "colour": "#08A0C0",
        "maps": {"higashimurayama": "SH", "higashiyamato": "SH", "tachikawa": "SH"},
    },
    # the project's colour nishitokyo, tokorozawa already drew; pins >= 43.0, lines >= 11.0, lines beside it >= 22.5.
    "seibu-ikebukuro-line": {
        "name": "Seibu Ikebukuro Line", "operator": "Seibu", "colour": "#D08000",
        "maps": {"nishitokyo": "SI", "tokorozawa": "SI", "tokyo": "SI"},
    },
    # the project's colour tokyo already drew; pins >= 48.3, lines >= 12.1, lines beside it >= 23.7.
    "seibu-shinjuku-line": {
        "name": "Seibu Shinjuku Line", "operator": "Seibu", "colour": "#906888",
        "maps": {"higashimurayama": "SS", "nishitokyo": "SS", "tokorozawa": "SS", "tokyo": "SS"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 47.5, lines >= 25.2, lines beside it >= 40.2.
    "sotetsu-jr-link-line": {
        "name": "Sotetsu-JR Link Line", "operator": "JR East", "colour": "#805878",
        "maps": {"kawasaki": "SJ", "yokohama": "SJ"},
    },
    # the project's colour every map already drew (hue-matched to the operator); pins >= 53.6, lines >= 23.6, lines beside it >= 23.6.
    "tama-toshi-monorail": {
        "name": "Tama Toshi Monorail", "operator": "Tama Toshi Monorail", "colour": "#E07800",
        "maps": {"higashiyamato": "MONO", "hino": "MONO", "tachikawa": "MONO"},
    },
    # the project's colour tokyo already drew; pins >= 51.4, lines >= 10.2, lines beside it >= 32.1.
    "tobu-skytree-line": {
        "name": "Tobu Skytree Line", "operator": "Tobu", "colour": "#007890",
        "maps": {"kasukabe": "TS", "soka": "TS", "tokyo": "TS"},
    },
    # the project's colour tokyo already drew; pins >= 45.7, lines >= 10.1, lines beside it >= 18.6.
    "tokyu-den-en-toshi-line": {
        "name": "Tokyu Den-en-toshi Line", "operator": "Tokyu", "colour": "#789090",
        "maps": {"kawasaki": "DT", "tokyo": "DT", "yokohama": "DT"},
    },
    # Tokyu's own line colour; pins >= 64.2, lines >= 13.6, lines beside it >= 23.4.
    "tokyu-meguro-line": {
        "name": "Tokyu Meguro Line", "operator": "Tokyu", "colour": "#009CD2",
        "maps": {"kawasaki": "MG", "tokyo": "MG"},
    },
    # the project's colour tokyo already drew; pins >= 49.2, lines >= 11.8, lines beside it >= 18.3.
    "tokyu-oimachi-line": {
        "name": "Tokyu Oimachi Line", "operator": "Tokyu", "colour": "#D07020",
        "maps": {"kawasaki": "OM", "tokyo": "OM"},
    },
    # the project's colour yokohama already drew; pins >= 46.7, lines >= 14.6, lines beside it >= 18.3.
    "tokyu-toyoko-line": {
        "name": "Tokyu Toyoko Line", "operator": "Tokyu", "colour": "#C03008",
        "maps": {"kawasaki": "TY", "tokyo": "TY", "yokohama": "TY"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "seoul-subway-line-1": {
        "name": "Line 1", "operator": "Korail and Seoul Metro", "colour": "#004A85",
        "maps": {"anyang": "L1", "bucheon": "L1", "incheon": "L1", "seoul": "L1", "suwon": "L1",
                 "uijeongbu": "L1"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "seoul-subway-line-3": {
        "name": "Line 3", "operator": "Seoul Metro and Korail", "colour": "#ED6C00",
        "maps": {"goyang": "L3", "seoul": "L3"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "seoul-subway-line-4": {
        "name": "Line 4", "operator": "Seoul Metro and Korail", "colour": "#009BCE",
        "maps": {"ansan": "L4", "anyang": "L4", "namyangju": "L4", "seoul": "L4", "siheung": "L4"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "seoul-subway-line-7": {
        "name": "Line 7", "operator": "Seoul Metro and Incheon Transit", "colour": "#6E7E31",
        "maps": {"bucheon": "L7", "incheon": "L7", "seoul": "L7", "uijeongbu": "L7"},
    },
    # Seoul Metro's #D11D70 darkened, hue kept, as Seoul's config records.
    "seoul-subway-line-8": {
        "name": "Line 8", "operator": "Seoul Metro", "colour": "#92144E",
        "maps": {"namyangju": "L8", "seongnam": "L8", "seoul": "L8"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "shinbundang-line": {
        "name": "Shinbundang Line", "operator": "NeoTrans", "colour": "#B81B30",
        "maps": {"seongnam": "SBD", "seoul": "SBD", "suwon": "SBD", "yongin": "SBD"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "gyeongui-jungang-line": {
        "name": "Gyeongui–Jungang Line", "operator": "Korail", "colour": "#6AC2B3",
        "maps": {"goyang": "GJ", "namyangju": "GJ", "seoul": "GJ"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "suin-bundang-line": {
        "name": "Suin–Bundang Line", "operator": "Korail", "colour": "#ECA300",
        "maps": {"ansan": "SB", "incheon": "SB", "seongnam": "SB", "seoul": "SB", "siheung": "SB",
                 "suwon": "SB", "yongin": "SB"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "gyeongchun-line": {
        "name": "Gyeongchun Line", "operator": "Korail", "colour": "#007A62",
        "maps": {"namyangju": "GC", "seoul": "GC"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "seohae-line": {
        "name": "Seohae Line", "operator": "Seohae Rail", "colour": "#5EAC41",
        "maps": {"ansan": "SH", "bucheon": "SH", "siheung": "SH"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "busan-gimhae-lrt": {
        "name": "Busan–Gimhae LRT", "operator": "Busan–Gimhae Light Rail Transit", "colour": "#8652A1",
        "maps": {"busan": "BGL", "gimhae": "BGL"},
    },
    # the operator's own colour, as OSM's route relation carries it.
    "taoyuan-airport-mrt": {
        "name": "Airport MRT", "operator": "Taoyuan Metro", "colour": "#2C5AA5",
        "maps": {"taipei": "A", "taoyuan": "A"},
    },
}


def colour(identity):
    """The one colour of a registered line, for a city config to draw."""
    try:
        return REGISTRY[identity]["colour"]
    except KeyError:
        raise KeyError(f"{identity!r} is not in pipeline/line_registry.py's REGISTRY") from None


def identity_of(city, key):
    """The registered identity a city's config key draws, or None."""
    for ident, entry in REGISTRY.items():
        if entry["maps"].get(city) == key:
            return ident
    return None


def members():
    """[(identity, city, key)] for every map entry in the registry."""
    return [(ident, city, key) for ident, entry in REGISTRY.items() for city, key in entry["maps"].items()]
