"""Zurich: the Stadt Zürich's Gastwirtschaftsbetriebe register, keyed on its
own `betriebsart` (the kind of licensed premises) - not NAICS.

The register (Stadtpolizei Zürich, Fachgruppe Bewilligung Gastro; Open Data
Zürich, CC0) lists the premises the city licenses to serve food and drink, and
the shops, kiosks and petrol stations it licenses to sell alcohol. One row per
premises, every row `betriebsstatus` "Offen" (the publisher: published rows
are always open). 14 values on 2026-09-30, every one with an explicit home
below; an unknown value RAISES, so a new kind stops step 2.

TWO BUCKETS, NOT THREE (owner, 2026-09-30; the tram-city skill, section 5:
`narrowed`, "Two"):
  * Food service - the food-and-drink licences.
  * Retail - PARTIAL: only the shops licensed to sell alcohol, on the
    tobacco-retail precedent of Seoul and Gyeonggi, with the gap disclosed.
    Its legend and layer read "Licensed shops", never plain "Retail".
  * No personal services: the register has none.

THE CALLS, each with its precedent (docs/category_rules.md):
  * Dancing / Disco is Food service: nightclubs not named as adult are kept
    (R5; Toronto and Edmonton). The brief's screen had put dance halls out;
    the standing rule decides, and the hand-off says so.
  * Cabaret / Nachtclub is out: the register names it as a cabaret (R3).
  * Kantine / Mensa is out: staff and institutional canteens (R1).
  * Ausgabestelle is out: the city files caterers, kiosks with seating and
    food trucks under it (R1 and the mobile-unit rule); the 56 rows mix
    lido and sports-ground stands with snack counters and do not say which.
  * Patentbefreit (exempt from the licence) is out: a catch-all of staff
    restaurants, care-home and school kitchens, a guest house, a beauty
    studio and a few cafés (25 rows, read by name 2026-09-30).
  * Veranstaltungsraum is out: rooms hired for events, not storefronts.
  * Restaurants that are really institutional kitchens (care homes, staff
    restaurants, hospital cafeterias, clubhouses) are licensed as ordinary
    Gastwirtschaft. About 79 of the 2,335 food rows by name (3.4%). They stay,
    and the page says some remain: a name rule here is the owner's call
    (Stockholm's was, on 13% of its register).
"""

FIELD_LABEL = "License type"
VALUE_COLUMN = "betriebsart"

R, F, OUT = "Retail", "Food service", None

# betriebsart -> (bucket, what a pin calls it in English). Counts are the
# register's rows on 2026-09-30 (3,487).
TYPES = {
    # --- Food service (2,335) ---------------------------------------------------
    "Gastwirtschaft": (F, "Restaurant, café or bar"),                           # 2,099
    "Nebenwirtschaft": (F, "Café or bar inside another business"),              # 192
    "Kleinwirtschaft": (F, "Small restaurant or bar"),                          # 30
    "Dancing / Disco": (F, "Club or disco"),                                    # 10
    "Take Away": (F, "Takeaway"),                                               # 3
    "Aussenliegende Saisonwirtschaft": (F, "Seasonal outdoor restaurant"),      # 1
    # --- Retail: shops licensed to sell alcohol (1,028) ------------------------
    "Kleinverkaufsstelle": (R, "Shop licensed to sell alcohol"),                # 954
    "Kiosk": (R, "Kiosk"),                                                      # 53
    "Tankstelle": (R, "Gas station shop"),                                   # 21
    # --- Out (124) --------------------------------------------------------------
    "Ausgabestelle": (OUT, "food stand, caterer or food truck"),                # 56
    "Kantine / Mensa": (OUT, "canteen"),                                        # 31
    "Patentbefreit": (OUT, "exempt from the licence"),                          # 25
    "Cabaret / Nachtclub": (OUT, "cabaret"),                                    # 6
    "Veranstaltungsraum": (OUT, "event room"),                                  # 6
}

LEGEND = {R: "Licensed shops", F: "Food service"}


def _key(row):
    v = row.get(VALUE_COLUMN)
    v = v.strip() if isinstance(v, str) else ""
    if v not in TYPES:
        raise KeyError(f"Zurich betriebsart {v!r} has no home in zurich_gastwirtschaft.py - "
                       f"map it before step 2 runs")
    return v


def classify(row: dict):
    return TYPES[_key(row)][0]


def label(row: dict):
    """The kind of premises in English, for the pin."""
    return TYPES[_key(row)][1]


def display_value(value) -> str:
    """How the licence type reads on a pin: English first, the register's own
    word after it ("Kiosk" needs no gloss)."""
    english = TYPES[_key({VALUE_COLUMN: value})][1]
    return english if english == value else f"{english} ({value})"


def legend_label(bucket: str) -> str:
    return LEGEND.get(bucket, bucket)


def layer_label(bucket: str) -> str:
    return LEGEND.get(bucket, bucket)


assert TYPES["Dancing / Disco"][0] == "Food service", "nightclubs are kept (R5)"
assert TYPES["Cabaret / Nachtclub"][0] is None, "cabarets are out (R3)"
assert TYPES["Kantine / Mensa"][0] is None, "canteens are out (R1)"
assert TYPES["Tankstelle"][0] == "Retail", "petrol stations are kept (R4)"
assert {v[0] for v in TYPES.values()} == {"Retail", "Food service", None}, "two buckets"
