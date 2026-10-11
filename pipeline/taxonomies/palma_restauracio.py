"""Palma taxonomy - the Consell de Mallorca's register of restaurant and
entertainment establishments, typed by its own `Grup`, not NAICS, with a name
test inside the kept types. Step 2 derives a premises kind (VALUE_COLUMN)
from the type and the trade name, by premises_kind() below.

ONE BUCKET (owner, 2026-09-29: a food-only page, Glasgow's twin). Every kept
type is food service:

  Bar, Restaurant, Bar-cafeteria, Cafeteria, Bar-copes, Cafè concert, Club
  de platja        food service
  Discoteca, Sala de festes, Sala de ball
                   food service: nightclubs are kept (R5, docs/category_rules.md)
  Catering         out (R1: food with no counter of its own)

Bakeries the register types as a bar or café ("FORN ...", "PANADERIA ...")
stay: the type says they seat customers.

THEN, WHAT A NAME SAYS THE PREMISES IS (docs/category_rules.md; Ottawa's and
Pittsburgh's rules), each read at the build:

  adult           R3, where the name says so (a "whiskería", table dance)
  venue           recreation (NAICS 71) and members' clubs: sports, tennis,
                  padel, riding, golf and nautical clubs, sports centres and
                  pool bars, cinemas; and gambling (R5): bingo, "casino" (in
                  Spain a members' club as often as a gaming hall)
  institutional   R1: parish and school bars, clinics' cafeterias, a
                  community centre's canteen
  lodging         a bare hotel name; a hotel's own named café or restaurant
                  ("RESTAURANTE HOTEL ALMUDAINA") stays (Ottawa's rule)

Every hit is listed with its rule in `outputs/palma/excluded_premises.csv`.
"""
import re
import unicodedata

FIELD_LABEL = "Establishment type"
VALUE_COLUMN = "premises_kind"

FOOD_TYPES = {"Bar", "Restaurant", "Bar-cafeteria", "Cafeteria", "Bar-copes", "Cafè concert",
              "Club de platja", "Discoteca", "Sala de festes", "Sala de ball"}
OUT_TYPES = {"Catering": "Catering (no counter)"}

FOOD = "Bar, café or restaurant"
ADULT = "Adult venue"
VENUE = "Recreation venue, club or gaming"
INSTITUTIONAL = "Institutional canteen"
LODGING = "Hotel"
OTHER_TYPE = "Catering (no counter)"
UNKNOWN_TYPE = "Type not in the register's list"
VALUE_TO_BUCKET = {FOOD: "Food service"}
NAME_KINDS = {ADULT, VENUE, INSTITUTIONAL, LODGING}
KNOWN_KINDS = set(VALUE_TO_BUCKET) | NAME_KINDS | {OTHER_TYPE, UNKNOWN_TYPE}

ADULT_PATTERNS = [r"\bW?H?ISKERIA\b", r"\bTABLE DANCE\b", r"\bSTRIP", r"\bALTERNE\b", r"\bEROTIC"]
VENUE_PATTERNS = [
    r"\bCLUB (DEPORTIVO|DE TENIS|DE BALL ESPORTIU|ESCUELA EQUITACION|PADEL)\b", r"\bPADEL\b",
    r"SPORT & TENNIS CLUB", r"\bPOLIESPORTIU\b", r"\bPISCINA\b", r"\bGOLF\b",
    r"\bCLUB (NAUTICO|MARITIMO|MTMO)\b", r"\bNAUTIC(O)?\b", r"R\.C\.N\.P\.",
    # a cinema, not a bar or restaurant named after one ("BAR CINE CLUB ...")
    r"^CINE\b", r"MULTICINES", r"\bBINGO\b", r"^CASINO\b",
]
INSTITUTIONAL_PATTERNS = [r"\bPARROQU", r"\bBAR DE L.ESCOLA\b", r"\bCLINICA\b", r"\bPOLICLINICA\b",
                          r"\bCENTRE SOCIAL\b"]
# A bare hotel name; its own named café, bar or restaurant stays. Not
# "hostal", which in Catalan is also an inn-restaurant (HOSTAL DE'S PLA).
LODGING_PATTERNS = [r"^(?!.*(CAFE|CAFETERIA|RESTAURANT|BAR\b|GRILL|TERRAZA)).*\bHOTEL\b"]

_ORDER = [(ADULT, ADULT_PATTERNS), (VENUE, VENUE_PATTERNS),
          (INSTITUTIONAL, INSTITUTIONAL_PATTERNS), (LODGING, LODGING_PATTERNS)]
_COMPILED = [(k, re.compile("|".join(p))) for k, p in _ORDER]


def fold(text):
    """Upper-case ASCII, accents dropped: 'Nàutic' and 'NAUTIC' match alike."""
    return unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode().upper()


def name_kind(name):
    n = fold(name).strip()
    for kind, rx in _COMPILED:
        if rx.search(n):
            return kind
    return None


def premises_kind(grup, name):
    """The kind step 2 writes to VALUE_COLUMN: the type decides first, then the
    name."""
    if grup in OUT_TYPES:
        return OUT_TYPES[grup]
    if grup not in FOOD_TYPES:
        return UNKNOWN_TYPE
    return name_kind(name) or FOOD


def legend_label(bucket):
    return {"Food service": "Bars, cafés and restaurants"}.get(bucket, bucket)


# The layer control names each bucket the way the legend does; until
# 2026-10-07 it said "Food service" beside a legend that says "Bars, cafés
# and restaurants".
layer_label = legend_label


def classify(row):
    """Bucket for a row, or None if it is not a tracked storefront."""
    return VALUE_TO_BUCKET.get((row.get(VALUE_COLUMN) or "").strip())


assert not set(VALUE_TO_BUCKET) & NAME_KINDS
