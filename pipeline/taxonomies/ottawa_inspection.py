"""Ottawa Public Health's food-safety inspection feed - a register with NO
classification field at all, so the "taxonomy" is a premises kind that step 2
derives from the premises NAME and address, by the rules below.

**ONE BUCKET.** Every premises in the feed is one OPH inspects for food
safety: restaurants, cafés, bars, take-outs AND food shops (grocers,
convenience stores, pharmacies that sell food, butchers, bakeries) - the
LIVES format carries no type, so the two cannot be told apart by any field.
They are drawn as ONE Food service layer whose legend says it holds both
(owner, 2026-09-29: food shops and pharmacies kept in the one layer, the FSA
cities' precedent for an inspection register's pharmacies). Kitchener-
Waterloo's food layer is the same shape.

**WHAT IS LEFT OUT, BY NAME** (owner, 2026-09-29, on a read of every hit):

  institutional   R1, food with no counter of its own: schools and école,
                  daycares and garderies, hospitals' patient kitchens and
                  cafeterias, retirement and long-term-care homes, churches
                  and parishes, community centres, staff and workplace
                  cafeterias, contract caterers' outlets (Aramark, Sodexo,
                  Compass), shelters, missions and food banks, camps, jails
  club            recreation and members' clubs (NAICS 71 and 8134): golf,
                  country, curling and yacht clubs, Legion halls, arenas
  mobile          R1 / mobile units: special-event vendors, food trucks and
                  carts (most have no point at all)
  lodging/funeral hotels' breakfast rooms and banquet kitchens (a hotel's own
                  named bar or restaurant stays), bed and breakfasts, funeral
                  homes - both out in every city

Event caterers are institutional under R1 (the Minneapolis call); a shop that
also caters ("... TAKEOUT AND CATERING", "... DELI & CATERING") stays.

A name rule both over- and under-catches. The patterns are phrases, not bare
words, because bare words catch SCHOOL HOUSE PIZZA, MARRIOTT RESIDENCE INN
and UNIVERSITY TAVERN; every hit was read at the build and
`outputs/ottawa/excluded_premises.csv` lists each one with its rule.
"""
import re
import unicodedata

FIELD_LABEL = "Premises"
VALUE_COLUMN = "premises_kind"

FOOD = "Food premises"
INSTITUTIONAL = "Institutional kitchen"
CLUB = "Club or recreation venue"
MOBILE = "Mobile or event vendor"
OTHER_TRADE = "Lodging or funeral home"

VALUE_TO_BUCKET = {FOOD: "Food service"}
EXCLUDED_KINDS = {INSTITUTIONAL, CLUB, MOBILE, OTHER_TRADE}
KNOWN_KINDS = set(VALUE_TO_BUCKET) | EXCLUDED_KINDS

INSTITUTIONAL_PATTERNS = [
    # schools and childcare (English and French)
    r"\bSCHOOL\b(?! HOUSE)", r"\bECOLE\b", r"\bPRE-?SCHOOL\b", r"\bMONTESSORI\b",
    r"\bDAY ?CARE\b", r"\bCHILD ?CARE\b", r"\bGARDERIE\b", r"EARLY LEARNING", r"\bCPE\b",
    r"\bHEADSTART\b", r"\bKINDERGARTEN\b", r"COLLEGIATE INSTITUTE",
    # hospitals and care homes
    r"\bHOSPITAL\b(?!.*TIM HORTONS)", r"\bHOPITAL\b", r"PATIENT (SERVICES|KITCHEN)",
    r"RETIREMENT", r"LONG.?TERM CARE", r"\bCARE (HOME|COMMUNITY|CENTRE)\b", r"NURSING HOME",
    r"SENIORS? (RESIDENCE|CENTRE|HOME)", r"SENIOR CENTRE", r"\bEXTENDICARE\b",
    r"\bCHARTWELL\b", r"\bVENVI\b", r"\bRIVERSTONE\b", r"\bHOSPICE\b", r"\bCHSLD\b", r"\bCSLD\b",
    r"^RESIDENCE ", r"\bASPIRA\b",
    # places of worship
    r"\bCHURCH\b", r"\bEGLISE\b", r"\bPARISH\b", r"\bPAROISSE\b", r"\bCATHEDRAL\b",
    r"\bSYNAGOGUE\b", r"\bMOSQUE\b",
    # community and social services
    r"COMMUNITY (CENTRE|CENTER|CTRE|HALL|HOUSE|RESOURCE|HEALTH|KITCHEN)", r"RECREATION CENT",
    r"\bSHELTER\b", r"\bMISSION\b", r"FOOD BANK", r"OUT OF THE COLD", r"SALVATION ARMY",
    r"MINISTRIES", r"SUMMER CAMP", r"\bCAMP (OTTONABEE|KITCHEN)",
    r"\bJAIL\b", r"DETENTION", r"CORRECTIONAL",
    # staff and contract catering
    r"\bCAFETERIA\b", r"STAFF (CAFETERIA|KITCHEN|CANTEEN)", r"^(SODEXO|ARAMARK|COMPASS)\b",
    # the second read's misses (the given-name and word probes, 2026-09-29)
    r"HIGHSCHOOL", r"\((BF|D\.H\.)\)", r"\bPROGRAM\b", r"\bFLECK\b", r"^PETER D CLARK",
    r"CENTRE (EDUCATIF|PARASCOLAIRE|DE JOUR)", r"CHILD (DEVELOPMENT|LEARNING) CENTRE",
    r"CHILDREN'?S (CENTRE|SERVICES)", r"FAMILY CENTRE", r"EMERGENCY FOOD", r"HOWARD SOCIETY",
    r"^ATRIA\b", r"^(HILLEL|CARLETON|STRATHMERE)[ -]LODGE", r"^(GRACE HILL|LEPAGE|BILLINGSWOOD) MANOR",
    r"HUNT CLUB MANOR", r"MICHELLE HEIGHTS CENTRE",
    # event caterers with no counter (R1); "... TAKEOUT AND CATERING" is a
    # shop that also caters, and stays
    r"^(?!.*(TAKEOUT|DELI|DINING|BAKE|CAFE|RESTAURANT|KITCHEN AND|FOOD AND|& CATERING|AND CATERING)).*\bCATER",
]
CLUB_PATTERNS = [
    r"\bARENA\b", r"\bLEGION\b", r"\bCURLING\b", r"GOLF (&|AND) COUNTRY", r"GOLF (CLUB|COURSE)",
    r"COUNTRY CLUB", r"YACHT CLUB", r"\bYMCA\b", r"\bYWCA\b",
    r"(SOCCER|SPORTS|TENNIS|PICKLEBALL|AQUATIC|KIDS) CLUB", r"(BOYS AND GIRLS|GIRLS AND BOYS) CLUB",
    r"LIONS?'?S? (CLUB|CANTEEN)", r"OTTAWA VALLEY HUNT CLUB", r"MASONIC", r"\bMOVATI\b",
    r"BOWLING CENTRE", r"HOCKEY TRAINING", r"(HAWKS|MIRACLE LEAGUE|TERRY FOX|ALLSTARS) CANTEEN",
]
# Lodging and funeral homes: out in every city (docs/category_rules.md).
OTHER_TRADE_PATTERNS = [
    r"FUNERAL", r"ECONO LODGE", r"BED AND BREAKFAST",
    # a hotel's breakfast room or banquet kitchen; its own named bar or
    # restaurant ("MYRA'S BAR AND KITCHEN - HOLIDAY INN") stays
    r"^(?!.*(BAR|RESTAURANT|PUB|GRILL|KITCHEN|TAKE-?OUT|CHINESE|ALE HOUSE|GIFT SHOP|QUINN))"
    r".*\b(INN|INNS|HOTELS?|SUITES|MARRIOTT|HILTON)\b",
]
MOBILE_NAME_PATTERNS = [
    r"FOOD TRUCK", r"CHIP TRUCK", r"CHIP STAND", r"CANTEEN TRUCK", r"SPECIAL EVENT",
    r"\bMOBILE\b", r"ON WHEELS", r"FOOD CART", r"HOT DOG CART",
]
MOBILE_ADDRESS_PATTERNS = [r"SPECIAL EVENT", r"\bMOBILE\b", r"NO FIXED", r"\bVARIOUS\b"]

_INST = re.compile("|".join(INSTITUTIONAL_PATTERNS))
_CLUB = re.compile("|".join(CLUB_PATTERNS))
_MOBILE_NAME = re.compile("|".join(MOBILE_NAME_PATTERNS))
_MOBILE_ADDR = re.compile("|".join(MOBILE_ADDRESS_PATTERNS))
_OTHER = re.compile("|".join(OTHER_TRADE_PATTERNS))


def fold(text):
    """Upper-case ASCII, accents dropped: 'École' and 'ECOLE' match alike."""
    return unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode().upper()


def premises_kind(name, address):
    """The kind step 2 writes to VALUE_COLUMN, mobile first (a food truck named
    for a school is still a truck), then institutional, club, lodging."""
    n, a = fold(name), fold(address)
    if _MOBILE_NAME.search(n) or _MOBILE_ADDR.search(a):
        return MOBILE
    if _INST.search(n):
        return INSTITUTIONAL
    if _CLUB.search(n):
        return CLUB
    if _OTHER.search(n):
        return OTHER_TRADE
    return FOOD


def legend_label(bucket):
    return {"Food service": "Restaurants and food shops"}.get(bucket, bucket)


# The layer control names each bucket the way the legend does; until
# 2026-10-07 it said "Food service" beside a legend that says "Restaurants
# and food shops".
layer_label = legend_label


def classify(row):
    """Bucket for a row, or None if it is not a tracked storefront."""
    return VALUE_TO_BUCKET.get((row.get(VALUE_COLUMN) or "").strip())


assert not set(VALUE_TO_BUCKET) & EXCLUDED_KINDS
