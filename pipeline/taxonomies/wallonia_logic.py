"""Charleroi and Liege: Wallonia's LoGIC 2024 shop survey, keyed on its own
`NATURE` - not NAICS.

LoGIC (Service public de Wallonie, with SEGEFA, ULiege; CC BY 4.0) is a field
survey of summer 2024: one point per ground-floor commercial cell, read by
`pipeline/countries/belgium_logic.py`. NATURE is its only classification and
has four values, every one with an explicit home below; an unknown value
RAISES, so a new edition with a new class stops step 2.

ONE LEVEL, SO NO LEVEL TO CHOOSE (premises-taxonomy Step 1). The catch-all is
`Services`: 7,851 of 37,701 points in Wallonia (20.8%), 454 of 2,653 in
Charleroi and 623 of 3,761 in Liege (2026-10-04). It mixes hairdressers with
banks, insurers, travel and estate agencies and offices, and no second field
splits it (the shop sign is free text), so it cannot be dispatched and is left
out whole: R2's logic (docs/category_rules.md). That makes the map two
categories, not three (`narrowed`, "Two", owner 2026-10-03).

  * Commerce de detail -> Retail.
  * HoReCa -> Food service. HOTELS ARE INSIDE IT and are kept and disclosed,
    not split (owner, 2026-10-03, Belgium build call 9): the class does not
    separate lodging, and only a keyword pass on the sign could, which is not
    register quality. A departure from the lodging rule, recorded in
    scripts/category_continuity_table.py as the owner's exception.
  * Services -> out (the catch-all, above).
  * Cellule vide -> out (a vacant unit).
"""

FIELD_LABEL = "Nature (LoGIC)"
VALUE_COLUMN = "NATURE"

R, F, OUT = "Retail", "Food service", None

# NATURE as the register writes it -> (bucket, the pin's English gloss).
# Counts: Wallonia / Charleroi (INS 52011) / Liege (INS 62063), 2026-10-04.
TYPES = {
    "Commerce de détail": (R, "Shop"),                                  # 16,254 / 980 / 1,477
    "HoReCa": (F, "Restaurant, café, bar or hotel"),                    # 6,746 / 450 / 868
    "Services": (OUT, "Service premises"),                              # 7,851 / 454 / 623
    "Cellule vide": (OUT, "Vacant unit"),                               # 6,850 / 769 / 793
}


def _key(row):
    v = row.get(VALUE_COLUMN)
    v = v.strip() if isinstance(v, str) else ""
    if v not in TYPES:
        raise KeyError(f"LoGIC NATURE {v!r} has no home in wallonia_logic.py - "
                       f"map it before step 2 runs")
    return v


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    return TYPES[_key(row)][0]


def label(row: dict):
    """The pin's English gloss for the class."""
    return TYPES[_key(row)][1]


def display_value(value) -> str:
    """How the class reads on a pin: English first, the register's own word
    after it."""
    return f"{TYPES[_key({VALUE_COLUMN: value})][1]} ({value})"


def legend_label(bucket: str) -> str:
    return bucket


assert TYPES["Services"][0] is None, "the services catch-all is out (R2)"
assert TYPES["Cellule vide"][0] is None, "vacant units are out"
assert TYPES["HoReCa"][0] == "Food service", "horeca, hotels included, is Food service (owner)"
assert {v[0] for v in TYPES.values()} == {"Retail", "Food service", None}, "two buckets"
