"""Kitchener–Waterloo taxonomy - the Region of Waterloo Public Health's own
inspection types (the bulk zips' SUBCATEGORY), not NAICS, with a name test
inside the kept types.

Step 2 derives a premises kind (VALUE_COLUMN) from the type and the premises
name, by premises_kind() below (owner, 2026-09-30: use SUBCATEGORY, food
shops as their own layer, institutional kitchens out by type).

BY TYPE, FOOD ("Food, General" only; the Institutional, Mobile Vendor and
Processing Plant categories are out whole):

  Restaurant, Food Take Out, Cocktail Bar/ Nightclub (R5: kept), Snack Bar /
  Refreshment Stand, Ice Cream / Yogurt Vendor
                                   Food service
  Food store convenience / Variety, Supermarket, Bakery, Butcher Shop, Fish
  Shop, Produce Vendor             Retail, drawn as "Food shops" - food shops
                                   count as food on the macro legend (owner,
                                   2026-09-30), so the city is two categories
  Caterer / Commissary (R1), Community Kitchen, Church Kitchen Facility,
  School Cafeteria, Serving Kitchen, Workplace Cafeteria, Food Bank, Banquet
  Hall (R2's wedding halls; Pittsburgh's banquet halls), Food Warehouse /
  Depot, Food Vending Facility (vending), Transient / Low Use, and every
  Institutional type
                                   out, as the register names it

A premises in the live layer that the zips do not yet hold (opened since the
zips' date) has no type: it stays Food service by default (owner,
2026-09-30), disclosed.

BY TYPE, PERSONAL SERVICES: all nine kept - Aesthetics, Hair Salon, Barber
Shop, Tattooing / Micropigmentation, Waxing, Ear / Body Piercing,
Electrolysis, Facials, Massage (commercial massage is kept,
docs/category_rules.md). Medi-spas stay: the Region inspects them as
personal services. A premises with no type in the zip stays too.

THEN, INSIDE THE KEPT TYPES, WHAT A NAME SAYS THE PREMISES IS
(docs/category_rules.md; Pittsburgh's and Ottawa's rules, adapted):

  institutional   R1: campus outlets (UW -, WLU -, Conestoga College, St.
                  Jerome's), hospital outlets (WRHN), school nutrition
                  programmes, churches, community centres, food banks,
                  salons inside a care home, a school of aesthetics,
                  caterers with no counter
  venue           recreation (NAICS 71) and members' clubs: the Aud's stands,
                  arenas, recreation complexes, golf, ski, racquet, tennis,
                  curling and lawn-bowling clubs, bowling lanes, cinemas,
                  theatres, the museum, amusement and play venues, gyms and
                  yoga, the ballyard, Bingeman Park, ethnic and service clubs,
                  the Legion
  lodging         a hotel's back of house and a bare hotel name; a hotel's own
                  named bar or restaurant stays (Ottawa's rule)
  pharmacy        a food register's pharmacies are out (Minneapolis's and
                  Pittsburgh's default)
  market stall    R1: the Kitchener Market's Saturday stalls (NKFM -); its
                  upper-level food hall's counters, named so, stay
  mobile          mobile and at-home units; "FIXED AND MOBILE" stays
  storage         a storage room, not a storefront

Every hit was read at the build and `outputs/kitchener_waterloo/
excluded_premises.csv` lists each one with its rule.
"""
import re

FIELD_LABEL = "Premises type"
VALUE_COLUMN = "premises_kind"

FOOD_SERVICE_TYPES = {"Restaurant", "Food Take Out", "Cocktail Bar/ Nightclub",
                      "Snack Bar / Refreshment Stand", "Ice Cream / Yogurt Vendor"}
FOOD_SHOP_TYPES = {"Food store convenience / Variety", "Supermarket", "Bakery", "Butcher Shop",
                   "Fish Shop", "Produce Vendor"}
PERSONAL_TYPES = {"Aesthetics", "Hair Salon", "Barber Shop", "Tattooing / Micropigmentation",
                  "Waxing", "Ear / Body Piercing", "Electrolysis", "Facials", "Massage"}
FOOD_CATEGORY = "Food, General"
PERSONAL_CATEGORY = "Personal Services"

RESTAURANT = "Restaurant or bar"
FOOD_SHOP = "Food shop"
PERSONAL = "Personal services"
VALUE_TO_BUCKET = {RESTAURANT: "Food service", FOOD_SHOP: "Retail", PERSONAL: "Personal services"}

OTHER_TYPE = "Type not a storefront"
OTHER_CATEGORY = "Institutional, mobile or processing category"
INSTITUTIONAL = "Institutional kitchen or service"
VENUE = "Recreation venue or club"
LODGING = "Hotel back of house"
PHARMACY = "Pharmacy"
STALL = "Market stall"
MOBILE = "Mobile or at-home unit"
STORAGE = "Storage"
NAME_KINDS = {INSTITUTIONAL, VENUE, LODGING, PHARMACY, STALL, MOBILE, STORAGE}
KNOWN_KINDS = set(VALUE_TO_BUCKET) | NAME_KINDS | {OTHER_TYPE, OTHER_CATEGORY}

INSTITUTIONAL_PATTERNS = [
    r"^UW\s*-", r"^WLU\s*-", r"CONESTOGA (COLLEGE|STUDENT)", r"ST\.? JEROME'?S UNIVERSITY",
    r"\bWRHN\b", r"GRAND RIVER HOSPITAL", r"NUTRITION FOR LEARNING", r"\bCHURCH\b(?!'S)",
    r"COMMUNITY (CENTRE|CENTER)", r"FOOD BANK", r"LONG TERM CARE", r"RETIREMENT HOME",
    r"\bRH$", r"SCHOOL OF AESTHETICS",
    # a caterer with no counter (R1); "... TAKE-OUT & CATERING" is a shop that
    # also caters, and stays (Ottawa's rule)
    r"^(?!.*(TAKE-?OUT|DELI|DINING|BAKE|CAFE|RESTAURANT|& CATERING|AND CATERING)).*\bCATER",
]
VENUE_PATTERNS = [
    r"MEMORIAL AUDITORIUM", r"\bARENA\b", r"RECREATION COMPLEX", r"TWIN PADS", r"\bGOLF(?!'S)",
    r"HALFWAY HOUSE", r"SKI CLUB", r"RACQUET CLUB", r"TENNIS CLUB", r"BOWLING CLUB",
    r"GRANITE CLUB", r"\bLANES\b", r"CINEMA", r"THEATRE", r"CENTRE IN THE SQUARE",
    r"CONRAD CENTRE", r"THEMUSEUM", r"ESCAPOLOGY", r"TRAPPED KW", r"TRAMPOLINE",
    r"AXE THROWING", r"FUNVILLA", r"PLAYTOWN", r"\bVR\b", r"GAMING LOUNGE", r"RETRO ROLLERS",
    r"\bMOVATI\b", r"\bYOGA\b", r"BALLYARD", r"BINGEMAN PARK", r"GREY SILO",
    r"CONCORDIA CLUB", r"ALPINE CLUB", r"SPORTSMEN CLUB", r"CORTINA CLUB", r"PORTUGUESE CLUB",
    r"\bLEGION\b",
]
# A hotel's breakfast room, servery or bare name; its own named bar or
# restaurant stays ("ARBOR KITCHEN & BAR (at the DOUBLE TREE BY HILTON)").
LODGING_PATTERNS = [
    r"^(?!.*(BAR|RESTAURANT|PUB|GRILL|KITCHEN|CAFE|JAZZ|MEDI SPA))"
    r".*\b(INN|HOTEL|SUITES|MARRIOTT|HILTON)\b",
]
PHARMACY_PATTERNS = [r"SHOPPERS DRUG MART", r"\bREXALL\b", r"PHARMA PLUS", r"PHARMACY"]
# The Kitchener Market (300 King St E): its upper level is a food hall of
# fixed counters open through the week, kept as a market building's shops;
# the rest (the lower level and the unlabelled) is the Saturday farmers'
# market's stalls (R1). Only a name that says "UPPER LEVEL" is kept.
STALL_PATTERNS = [r"^NKFM\s*-(?!.*UPPER LEVEL)"]
MOBILE_PATTERNS = [r"(?<!FIXED AND )\bMOBILE\b", r"AT-HOME", r"ICE CREAM BIKE", r"FOOD TRUCK"]
STORAGE_PATTERNS = [r"-\s*STORAGE\b"]

_ORDER = [(MOBILE, MOBILE_PATTERNS), (STALL, STALL_PATTERNS), (STORAGE, STORAGE_PATTERNS),
          (INSTITUTIONAL, INSTITUTIONAL_PATTERNS), (VENUE, VENUE_PATTERNS),
          (LODGING, LODGING_PATTERNS), (PHARMACY, PHARMACY_PATTERNS)]
_COMPILED = [(k, re.compile("|".join(p))) for k, p in _ORDER]


def name_kind(name):
    """The name rule a premises falls under, or None."""
    n = str(name or "").upper().strip()
    for kind, rx in _COMPILED:
        if rx.search(n):
            return kind
    return None


def premises_kind(category, subcategory, name):
    """The kind step 2 writes to VALUE_COLUMN. The category decides first,
    then the type (None: the zips do not hold the premises yet), then the
    name."""
    sub = subcategory if isinstance(subcategory, str) and subcategory else None
    if category == PERSONAL_CATEGORY:
        base = PERSONAL if sub is None or sub in PERSONAL_TYPES else OTHER_TYPE
    elif category == FOOD_CATEGORY:
        if sub is None or sub in FOOD_SERVICE_TYPES:
            base = RESTAURANT
        elif sub in FOOD_SHOP_TYPES:
            base = FOOD_SHOP
        else:
            base = OTHER_TYPE
    else:
        return OTHER_CATEGORY
    if base == OTHER_TYPE:
        return base
    return name_kind(name) or base


def legend_label(bucket):
    return {"Food service": "Restaurants and bars", "Retail": "Food shops"}.get(bucket, bucket)


def classify(row):
    """Bucket for a row, or None if it is not a tracked storefront."""
    return VALUE_TO_BUCKET.get((row.get(VALUE_COLUMN) or "").strip())


assert not set(VALUE_TO_BUCKET) & NAME_KINDS
