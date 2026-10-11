"""Minneapolis taxonomy - the City's food-inspection `FacilityCategory`, not
NAICS, with a name layer inside the kept categories.

Step 2 derives a premises kind (VALUE_COLUMN) from the category and the
facility's name, by premises_kind() below. The register types every facility,
so its category decides first:

  RESTAURANT                  Food service
  GROCERY, MEAT MARKET,       Retail (New York's precedent: a food register's
  MARKET, LIQOFFSALE          shops are shops; LIQOFFSALE is one off-sale
                              liquor store, NAICS 445320)
  everything else             out, as the register names it: INSTITUTION,
                              BOARD AND LODGING, CATERER (R1), FOOD TRUCK,
                              FOOD CART, LIMITED MOBILE, MRKTVENDOR, VENDOR
                              (mobile units and stalls), FOODSHELF, WHOLESALE

THEN, INSIDE THE KEPT CATEGORIES, WHAT A NAME SAYS THE PREMISES IS
(docs/category_rules.md; Stockholm's precedent for a typed register's
canteens): the register files a contract caterer's workplace outlet or a
hospital cafeteria as a RESTAURANT, and a vending route or a workplace
micro-market as a GROCERY.

  institutional   R1: contract caterers (Sodexo, Aramark, Compass/Eurest),
                  hospital, school, church and campus-dining kitchens,
                  employee dining, event caterers with no counter, shared
                  commissary kitchens, treatment houses (H148)
  vending         nonstore retail: vending routes (Canteen Vending)
  lodging         hotels' kitchens and pantry shops - out in every city
  venue           recreation (NAICS 71) and members' clubs: theatre and
                  stadium concessions, event and arts centres, museums, gyms,
                  the private city and country clubs (Ottawa's call)
  pharmacy        a food register's pharmacies are out (the rule's default;
                  Ottawa's one layer is its owner-decided exception)
  adult           R3, where the name itself says so (CABARET)

A shop that also caters ("... RESTAURANT & CATERING", "... BAKERY &
CATERING") stays. Every hit was read at the build and
`outputs/minneapolis/excluded_premises.csv` lists each one with its rule.
"""
import re

FIELD_LABEL = "Facility category"
VALUE_COLUMN = "premises_kind"

FOOD_CATEGORIES = {"RESTAURANT"}
SHOP_CATEGORIES = {"GROCERY", "MEAT MARKET", "MARKET", "LIQOFFSALE"}
# What the register says; step 2 asserts every category it meets is here.
# UNCATEGORISED: three facilities the register leaves blank (a park board,
# two restaurants by name) - out, not guessed into a bucket.
OUT_CATEGORIES = {"INSTITUTION", "BOARD AND LODGING", "CATERER", "FOOD TRUCK", "FOOD CART",
                  "LIMITED MOBILE", "MRKTVENDOR", "VENDOR", "FOODSHELF", "WHOLESALE",
                  "UNCATEGORISED"}

INSTITUTIONAL = "Institutional kitchen"
VENDING = "Vending"
LODGING = "Hotel"
VENUE = "Recreation venue or club"
PHARMACY = "Pharmacy"
ADULT = "Adult venue"

VALUE_TO_BUCKET = {"RESTAURANT": "Food service", "GROCERY": "Retail", "MEAT MARKET": "Retail",
                   "MARKET": "Retail", "LIQOFFSALE": "Retail"}
NAME_KINDS = {INSTITUTIONAL, VENDING, LODGING, VENUE, PHARMACY, ADULT}
KNOWN_KINDS = set(VALUE_TO_BUCKET) | OUT_CATEGORIES | NAME_KINDS

INSTITUTIONAL_PATTERNS = [
    r"^(SODEXO|ARAMARK|COMPASS GROUP|EUREST)\b", r"\bEUREST DINING\b", r"EMPLOYEE DINING",
    r"\bHOSPITAL\b", r"MEDICAL (CENTER|CTR)", r"PATIENT SERVICES",
    r"(?<!RESTAURANT & )\bCAFETERIA\b", r"\bSCHOOL\b", r"\bCHURCH\b", r"MINISTRY CENTER",
    r"COMMUNITY (CENTER|LIFE)", r"^H148 - ", r"^WEWORK\b", r"BANQUETS KITCHEN", r"COMM(ISSARY)? KITCHEN",
    r"^KITCHEN SPACE$",
    # event caterers with no counter (R1); a shop that also caters stays
    r"^(?!.*(TAKEOUT|DELI|DINING|BAKE|CAFE|RESTAURANT|KITCHEN AND|FOOD AND|& CATERING|AND CATERING))"
    r".*\bCATER",
]
VENDING_PATTERNS = [r"\bVENDING\b", r"^CANTEEN (AT|VENDING)\b", r"^CANTEEN-"]
LODGING_PATTERNS = [r"\bHOTEL\b", r"\bSUITES\b", r"\bMARRIOTT\b", r"\bHILTON\b", r"\bHYATT\b",
                    r"RESIDENCE INN", r"INN & SUITES", r"INN EXPRESS", r"GARDEN INN",
                    r"NICOLLET ISLAND INN", r"\bWESTIN\b", r"\bSHERATON\b", r"\bRADISSON\b",
                    r"\bLOEWS\b", r"\bKIMPTON\b", r"BEST WESTERN", r"\bDOUBLETREE\b",
                    r"HOLIDAY INN", r"CROWNE PLAZA", r"COURTYARD BY", r"\bHOMEWOOD\b"]
# R3: premises the register's own name calls adult ("cabaret" is the rule's
# own word, after Tokyo's).
# "THE NICOLLET DINER AND ROXY'S CABARET" is a 24-hour diner, and stays.
ADULT_PATTERNS = [r"^(?!.*DINER).*\bCABARET\b"]
VENUE_PATTERNS = [
    r"^(?!.*(CAFE|LOUNGE|BAR|CLOUDLAND)).*\bTHEAT(ER|RE)\b", r"^PARADE STADIUM$",
    r"ORCHESTRA HALL", r"\bCINEMA\b", r"MEMORY LANES", r"\bBOWLING\b",
    r"EVENT CENTER", r"CULTURAL CENTER", r"ARTS CENTER", r"\bMUSEUM\b", r"\bARMORY\b",
    r"\bFITNESS\b", r"^(MINNEAPOLIS|MINIKAHDA) CLUB$", r"^CAMPUS CLUB\b",
]
PHARMACY_PATTERNS = [r"\bPHARMACY\b"]
# A university's own name on a RESTAURANT is its campus dining; on a GROCERY
# it is the campus bookstore, which stays.
CAMPUS_DINING = re.compile(r"^(UNIVERSITY OF (ST THOMAS|MN)|SAINT MARY'S UNIVERSITY)\b")

_RULES = [(ADULT, re.compile("|".join(ADULT_PATTERNS))),
          (VENDING, re.compile("|".join(VENDING_PATTERNS))),
          (INSTITUTIONAL, re.compile("|".join(INSTITUTIONAL_PATTERNS))),
          (LODGING, re.compile("|".join(LODGING_PATTERNS))),
          (VENUE, re.compile("|".join(VENUE_PATTERNS))),
          (PHARMACY, re.compile("|".join(PHARMACY_PATTERNS)))]


def display_name(name):
    """The register's name up to its first line break: two names carry a
    clerk's note on a second line ('BRIM' + a licence memo)."""
    return str(name or "").split("\n")[0].strip()


def premises_kind(category, name):
    """The kind step 2 writes to VALUE_COLUMN: the register's category, unless
    a kept category's name says the premises is one of NAME_KINDS (vending
    first, so a caterer's vending route is vending)."""
    cat = (category or "").strip().upper()
    if cat not in VALUE_TO_BUCKET:
        return cat
    n = display_name(name).upper()
    if cat == "RESTAURANT" and CAMPUS_DINING.search(n):
        return INSTITUTIONAL
    for kind, rx in _RULES:
        if rx.search(n):
            return kind
    return cat


def legend_label(bucket):
    # The retail layer is food shops only: the register holds no other shop.
    return {"Retail": "Grocery and food shops"}.get(bucket, bucket)


# The layer control names each bucket the way the legend does; until
# 2026-10-07 it said "Retail" beside a legend that says "Grocery and food
# shops".
layer_label = legend_label


# The Retail bucket here is food shops only, so its pins are olive, not retail
# blue (owner, 2026-10-07: one pin colour per meaning; pipeline/taxonomies
# MEANING_COLOURS).
PIN_MEANINGS = {"Retail": "Food shops"}


def classify(row):
    """Bucket for a row, or None if it is not a tracked storefront."""
    return VALUE_TO_BUCKET.get((row.get(VALUE_COLUMN) or "").strip().upper())


assert not set(VALUE_TO_BUCKET) & (OUT_CATEGORIES | NAME_KINDS)
