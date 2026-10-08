"""Bremen: the 2022 regional retail survey's main goods group (Hauptwarengruppe,
`HWG_C`), a closed list of 19 codes - not NAICS.

"Einzelhandelsbestand in der Region Bremen 2022" (Kommunalverbund
Niedersachsen/Bremen e.V., CC BY) counts every retail site in the region and
files each under ONE main goods group, with a floor-area class beside it.
The public variant has no name and no address, so a pin shows the group's
English label (Florence's no-name precedent), and the survey's own German
words follow it on the pin's second line.

KEYED ON THE CODE, never the label (the brief): the floor-area field shows
one code under two labels, so a label is not a key. Step 2 checks that each
code still carries the German label written below and stops if the survey
relabels one. An unknown code RAISES, so a new goods group stops step 2.

ONE LEVEL, ONE BUCKET. The survey holds retail only (the record: retail
businesses "im engeren Sinn"), so every group is Retail, matched by what the
premises is (docs/category_rules.md). Groups 2 and 10 are the pharmacies and
opticians rows of category_rules.md, kept as in every general-retail source.

THE CATCH-ALL (premises-taxonomy Step 2), measured on the cached file,
City of Bremen rows: code 19, "Sonstige EH-Einrichtungen" (other retail
facilities), 94 of 3,153 (3.0%), under the 5% line. The scheme has one level
in the public file, so no finer key exists. Kept as Retail (owner,
2026-10-05, brief call 1): the survey files them as retail establishments in
a survey of retail only, and the public file gives nothing finer.
"""

FIELD_LABEL = "Main goods group (2022 survey)"
VALUE_COLUMN = "hwg_code"

R = "Retail"

# HWG_C -> (bucket, the survey's German label, the English label a pin
# shows). Counts: City of Bremen rows / region rows, cached file (fetched
# 2026-10-04), measured 2026-10-07.
GROUPS = {
    1: (R, "Nahrungs-/Genussmittel", "Food and drink store"),                     # 1,141 / 1,978
    2: (R, "Apotheken/ Drogerie/ Parfümerie", "Pharmacy, drugstore or perfumery"),  # 209 / 351
    3: (R, "Blumen/ Zoo", "Florist or pet store"),                                # 27 / 70
    4: (R, "Büroartikel, Schreibwaren, Zeitungen Zeitschriften",
        "Stationery or newsagent"),                                               # 56 / 100
    5: (R, "Bücher", "Bookstore"),                                                # 43 / 72
    6: (R, "Spielwaren, Hobby", "Toy or hobby store"),                            # 53 / 83
    7: (R, "Bekleidung und Zubehör", "Clothing and accessories"),                 # 417 / 681
    8: (R, "Schuhe/ Lederwaren", "Shoes or leather goods"),                       # 70 / 117
    9: (R, "Sport/ Freizeit", "Sporting goods"),                                  # 93 / 166
    10: (R, "Optik, Hörgeräte, Sanitätswaren, orthopädische Waren",
         "Optician, hearing aids or medical supply"),                             # 152 / 271
    11: (R, "Uhren/ Schmuck", "Watches or jewelry"),                              # 105 / 156
    12: (R, "Elektro/ Leuchten", "Electrical goods or lighting"),                 # 32 / 53
    13: (R, "Medien", "Electronics and media"),                                   # 157 / 242
    14: (R, "GPK/ Geschenke/ Hausrat", "Glassware, gifts or housewares"),         # 133 / 226
    15: (R, "Haus-/ Heimtextilien", "Home textiles"),                             # 51 / 99
    16: (R, "Teppiche/ Bodenbeläge", "Carpets or flooring"),                      # 27 / 47
    17: (R, "Baumarkt-/ Gartencenterspezifische Sortimente",
         "DIY or garden center"),                                                 # 201 / 511
    18: (R, "Möbel/ Antiquitäten", "Furniture or antiques"),                      # 92 / 162
    19: (R, "Sonstige EH-Einrichtungen", "Other retail"),                         # 94 / 188 (the catch-all)
}
CATCH_ALL = (19,)


def code_of(value) -> int:
    """The goods-group code as an int, from the GeoJSON's int or a CSV's
    text; raises on a code the module has not decided."""
    try:
        code = int(str(value).strip())
    except ValueError:
        raise KeyError(f"Bremen goods group {value!r} is not a code - step 2 writes HWG_C") from None
    if code not in GROUPS:
        raise KeyError(f"Bremen goods group {code} has no home in bremen_einzelhandel.py - "
                       f"read the survey's label for it before step 2 runs")
    return code


def german_label(value) -> str:
    return GROUPS[code_of(value)][1]


def label(value) -> str:
    """The pin's bold line: the survey carries no name, so the group's English
    label stands in for one."""
    return GROUPS[code_of(value)][2]


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    return GROUPS[code_of(row.get(VALUE_COLUMN))][0]


def display_value(value) -> str:
    """How the goods group reads on a pin's second line: the survey's own
    German words."""
    return german_label(value)


def legend_label(bucket: str) -> str:
    return bucket


assert sorted(GROUPS) == list(range(1, 20)), "the survey's 19 goods groups, 1 to 19"
assert {b for b, _, _ in GROUPS.values()} == {R}, "a retail survey: every group is Retail"
assert len({en for _, _, en in GROUPS.values()}) == len(GROUPS), "one English label per group"
assert GROUPS[19][0] == R, "the catch-all stays Retail (owner, 2026-10-05, call 1)"
