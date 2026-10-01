"""Pittsburgh taxonomy - Allegheny County Health Department's food-facility
`category_cd`, not NAICS, with a name test inside the kept categories.

Step 2 derives a premises kind (VALUE_COLUMN) from the category and the
facility's name, by premises_kind() below. The register types every facility,
so its category decides first:

  201, 202, 211, 212       Food service: restaurants with or without liquor,
                           chain or not
  111-118                  Retail: supermarkets, retail/convenience stores,
                           packaged-food shops and bakeries, chain or not.
                           Supermarkets and bakeries were missing from the
                           brief's list; they are food shops by any reading.
                           "Chain Packaged Food Only" (116) also holds
                           general retailers that sell packaged food (T J
                           Maxx, Dollar General, Five Below): real storefronts,
                           kept
  everything else          out, as the register names it: caterers and
                           transient caterers (R1), mobile tiers, commissaries,
                           processors and warehouses, institutional kitchens
                           (4xx: child, adult, university, hospital,
                           religious, community; 6xx: schools), boarding and
                           nursing homes (3xx), banquet halls, social clubs
                           (250, members' bars: Ottawa's call), temporary
                           events, pool snack bars

THEN, INSIDE THE KEPT CATEGORIES, WHAT A NAME SAYS THE PREMISES IS
(docs/category_rules.md; Minneapolis's layer, adapted). The County licenses
each stand of a venue on its own, as "Acrisure Stadium / Walk Thru Brew 139"
or "Market C @ UPMC Shadyside", so the host's name decides:

  adult           R3, where the name says so (a "... Cabaret" that is not a
                  cabaret theatre; a "Gentlemen's Club")
  venue           recreation (NAICS 71) and gambling (R5): the stadium,
                  arena, ballpark and events-centre stands, the casino's
                  outlets, zoo, aviary, museum and science-centre cafés,
                  theatres, cinemas, bowling, golf and fitness, the private
                  city clubs
  nonstore        dark stores (goPuff, DashMart) and vending
  hotel           a hotel's back of house - main and banquet kitchens,
                  employee cafés, club lounges, gift shops, pantries - and a
                  bare hotel name with no bar or restaurant in it; a hotel's
                  own named bar or restaurant stays (Ottawa's rule)
  pharmacy        a food register's pharmacies are out (Minneapolis's
                  default)
  institutional   R1: workplace micro-markets (Market C) and contract
                  caterers (Laurel Foodsystems, Parkhurst, Bon Appétit),
                  hospital outlets (UPMC, AHN), campus dining (Pitt Eats,
                  CMU, Duquesne, Chatham, Point Park, CCAC), church cafés,
                  employee cafeterias, commissaries, caterers with no counter

Every hit was read at the build and `outputs/pittsburgh/excluded_premises.csv`
lists each one with its rule.
"""
import re

FIELD_LABEL = "Facility category"
VALUE_COLUMN = "premises_kind"

FOOD_CODES = {"201", "202", "211", "212"}
SHOP_CODES = {"111", "112", "113", "114", "115", "116", "117", "118"}

ADULT = "Adult venue"
VENUE = "Recreation venue, casino or club"
NONSTORE = "Nonstore or vending"
LODGING = "Hotel back of house"
PHARMACY = "Pharmacy"
INSTITUTIONAL = "Institutional kitchen"
NAME_KINDS = {ADULT, VENUE, NONSTORE, LODGING, PHARMACY, INSTITUTIONAL}

RESTAURANT = "RESTAURANT"
FOOD_SHOP = "FOOD SHOP"
VALUE_TO_BUCKET = {RESTAURANT: "Food service", FOOD_SHOP: "Retail"}
OTHER = "OTHER CATEGORY"
KNOWN_KINDS = set(VALUE_TO_BUCKET) | NAME_KINDS | {OTHER}

ADULT_PATTERNS = [r"CABARET(?! THEAT)", r"GENTLEMEN'?S CLUB"]
VENUE_PATTERNS = [
    r"ACRISURE STADIUM", r"PPG PAINTS ARENA", r"PNC PARK", r"HIGHMARK STADIUM",
    r"PETERSEN EVENTS", r"COOPER FIELDHOUSE", r"^DLCC\b", r"CONVENTION CENTER", r"^STAGE AE\b",
    r"CASINO", r"\bZOO\b", r"AVIARY", r"\bMUSEUM\b", r"SCIENCE CENTER", r"CONSERVATORY",
    r"\bTHEAT(ER|RE)\b", r"\bCINEMAS?\b", r"\bBOWLING\b", r"SPINS BOWL", r"\bGOLF\b",
    r"\bFITNESS\b", r"^DUQUESNE CLUB\b", r"^UNIVERSITY CLUB$", r"ROONEY SPORTS COMPLEX",
    r"PETERSEN SPORTS COMPLEX",
]
NONSTORE_PATTERNS = [r"\bGOPUFF\b", r"^DASHMART\b", r"\bVENDING\b"]
HOTEL_PATTERNS = [
    r"\bHOTEL\b", r"\bSUITES\b", r"MARRIOTT", r"HILTON", r"HYATT", r"OMNI WILLIAM PENN",
    r"WYNDHAM", r"SHERATON", r"WESTIN", r"^ ?RENAISSANCE PITTSBURGH", r"DOUBLETREE",
    r"HAMPTON INN", r"GARDEN INN", r"RESIDENCE INN", r"HOLIDAY INN", r"^COURTYARD PITTSBURGH",
    r"FAIRMONT", r"KIMPTON", r"RADISSON",
]
HOTEL_BACK_OF_HOUSE = [r"EMPLOYEE", r"BANQUET", r"MAIN KITCHEN", r"CLUB LOUNGE", r"GIFT SHOP",
                       r"\bPANTRY\b"]
HOTEL_OUTLET_WORDS = [r"\bBAR\b", r"RESTAURANT", r"\bPUB\b", r"GRILLE?\b", r"BISTRO",
                      r"BRASSERIE", r"TAVERN"]
PHARMACY_PATTERNS = [r"PHARMAC", r"PHAMAC", r"^RITE AID\b", r"^CVS\b", r"^WALGREENS\b"]
INSTITUTIONAL_PATTERNS = [
    r"^MARKET C\b", r"\bMARKET C\b", r"LAUREL FOODSYSTEMS", r"^PARKHURST\b", r"BON APPETIT",
    r"SODEXO", r"ARAMARK", r"EUREST", r"\bUPMC\b", r"\bAHN\b", r"HOSPITAL",
    r"^PITT EATS\b", r"^CMU / ", r"^DUQUESNE UNIVERSITY", r"^CHATHAM UNIVERSITY",
    r"^POINT PARK UNIVERSITY", r"\bCCAC\b", r"@ UNIVERSITY OF PITTSBURGH",
    r"(?<!THE )\bCHURCH\b(?! BREW)", r"EMPLOYEE", r"CAFETERIA", r"^(?!.*DELI).*COMMISSARY",
    # caterers with no counter (R1); a shop or grill that also caters stays
    r"^(?!.*(GRILL|DELI|BAKE|CAFE|RESTAURANT|& CATERING|AND CATERING)).*\bCATER",
    r"CATERING KITCHEN",
]


def _rx(patterns):
    return re.compile("|".join(patterns))


_ADULT, _VENUE, _NONSTORE = _rx(ADULT_PATTERNS), _rx(VENUE_PATTERNS), _rx(NONSTORE_PATTERNS)
_HOTEL, _HOTEL_BOH, _HOTEL_OUTLET = (_rx(HOTEL_PATTERNS), _rx(HOTEL_BACK_OF_HOUSE),
                                     _rx(HOTEL_OUTLET_WORDS))
_PHARMACY, _INST = _rx(PHARMACY_PATTERNS), _rx(INSTITUTIONAL_PATTERNS)
_SEP = re.compile(r"\s*(?: / |@)\s*")


def fold(name):
    return str(name or "").upper().replace("’", "'").replace("É", "E").strip()


def hotel_back_of_house(n):
    """A hotel's own kitchen or service, as opposed to its named bar or restaurant."""
    if not _HOTEL.search(n):
        return False
    if _HOTEL_BOH.search(n):
        return True
    has_outlet = len(_SEP.split(n, maxsplit=1)) > 1
    return not has_outlet and not _HOTEL_OUTLET.search(n)


def premises_kind(category_cd, name):
    """The kind step 2 writes to VALUE_COLUMN."""
    cd = str(category_cd or "").strip()
    if cd in FOOD_CODES:
        base = RESTAURANT
    elif cd in SHOP_CODES:
        base = FOOD_SHOP
    else:
        return OTHER
    n = fold(name)
    if _ADULT.search(n):
        return ADULT
    if _VENUE.search(n):
        return VENUE
    if _NONSTORE.search(n):
        return NONSTORE
    if hotel_back_of_house(n):
        return LODGING
    if _PHARMACY.search(n):
        return PHARMACY
    if _INST.search(n) and not re.search(r"^UNIVERSITY STORE\b", n):
        return INSTITUTIONAL
    return base


def legend_label(bucket):
    # The retail layer is shops the health department licenses for food.
    return {"Retail": "Food-selling shops"}.get(bucket, bucket)


def classify(row):
    """Bucket for a row, or None if it is not a tracked storefront."""
    return VALUE_TO_BUCKET.get((row.get(VALUE_COLUMN) or "").strip().upper())


assert not set(VALUE_TO_BUCKET) & (NAME_KINDS | {OTHER})
