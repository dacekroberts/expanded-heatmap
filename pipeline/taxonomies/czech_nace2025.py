"""CZ-NACE 2025 - Czechia's classification of economic activities, matched
on PREFIX at whatever depth a row carries.

**NATIONAL, NOT PER-CITY.** CZ-NACE 2025 is ČSÚ's, and RES is one register
for the whole country; Prague is the first city on it. Per-city verdicts do
NOT belong here (CATCH_ALL_EXCLUDE lives in the city's config).

**IT IS CZ-NACE 2025 - NACE Rev. 2.1 - read from RES's `NACE2025` column, not
its older `NACE`.** Measured 2026-09-24 on Prague: Rev.-2.1-only classes are
populated (96210 hairdressing 7,166; 56110 restaurants 7,780; 47810 car
retail 107), and the column is deeper (65% of Praha rows at 5 digits against
52%). Same parent as Norway's SN2025 and Denmark's DB25, so the structural
exclusions below are theirs, and the two Rev. 2.1 changes apply here too:
car retail sits in division 47 (kept), and web shops cannot be excluded by
code (disclosed).

**RAGGED DEPTH, SO NO LEVEL CAN BE CHOSEN - the first taxonomy here that
matches on PREFIX.** RES stores whatever depth a subject declared: in Prague's
storefront rows `471` (3,878) and `47` (1,040) sit beside `47250` and
`96210`. Every row still carries its division, so bucketing is safe; an
exclusion is written as the SHORTEST prefix that means only the excluded
activity, so it catches a row at any depth below it and none above.

**THE LABELS ARE ČSÚ's, VERBATIM**, from codebooks 6101-6105 (one per level),
looked up at the row's own depth by the step that loads RES. `classify()`
matches on the code in EXTRA_COLUMNS and never on label text.
"""

FIELD_LABEL = "CZ-NACE 2025"
VALUE_COLUMN = "nace2025_label"
EXTRA_COLUMNS = ("nace2025_code",)

_DIVISION_BUCKETS = {
    "47": "Retail",
    "56": "Food service",
    "96": "Personal services",
}

# ---------------------------------------------------------------------------
# Structural exclusions - NOT premises, anywhere in Czechia
# ---------------------------------------------------------------------------
#
# Oslo's and Copenhagen's NACE Rev. 2.1 set, read against ČSÚ's own labels
# 2026-09-24, each written as the shortest prefix that names ONLY it:
NOT_PREMISES_PREFIXES = {
    # 47.9 in Rev. 2.1 is ENTIRELY intermediation (47.91 non-specialised,
    # 47.92 specialised) - "Zprostředkování v oblasti ... maloobchodu".
    "479": "Zprostředkování v oblasti maloobchodu",
    # 56.12, mobile food - France's "éventaires et marchés" reasoning.
    "5612": "Poskytování stravování v mobilních zařízeních",
    # 56.2 is catering and contract food service (56.21, 56.22) - the work
    # happens at the event or inside someone else's institution.
    "562": "Cateringové činnosti, smluvní a ostatní stravovací služby",
    # 56.4 and 96.4, intermediation for food service and personal services.
    "564": "Zprostředkování v oblasti stravování",
    "964": "Zprostředkování v oblasti osobních služeb",
    # 96.91, personal services in the customer's household.
    "9691": "Poskytování osobních služeb v domácnostech",
}

# Codes whose own label is residual wording ("ostatní", "j. n." - jinde
# neuvedené). Classified normally; the per-city verdict is CATCH_ALL_EXCLUDE.
CATCH_ALL_CODES = {
    "47120",   # Ostatní nespecializovaný maloobchod
    "47270",   # Specializovaný maloobchod s ostatními potravinami
    "47690",   # Maloobchod s výrobky pro kulturní rozhled a rekreaci j. n.
    "47780",   # Maloobchod s ostatním novým zbožím
    "47799",   # Maloobchod s ostatním použitým zbožím
    "96990",   # Poskytování ostatních osobních služeb j. n.
}


def normalise_code(value):
    """RES's code as a digit string at its own depth (`471`, `96210`)."""
    if value is None:
        return ""
    code = str(value).strip().replace(".", "").replace(" ", "")
    if not code or code.upper() == "NAN" or not code.isdigit():
        return ""
    return code


def excluded(code):
    """The structural exclusion a code falls under, or None."""
    return next((p for p in NOT_PREMISES_PREFIXES if code.startswith(p)), None)


def classify(row):
    """Bucket for a row, or None if it is not tracked storefront commerce."""
    code = normalise_code(row.get("nace2025_code"))
    if len(code) < 2 or excluded(code):
        return None
    return _DIVISION_BUCKETS.get(code[:2])


def legend_label(bucket):
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    return f"{bucket} - CZ-NACE {'/'.join(divisions)}"


assert all(p[:2] in _DIVISION_BUCKETS for p in NOT_PREMISES_PREFIXES), \
    "a CZ-NACE exclusion names a code outside divisions 47/56/96"
assert not any(excluded(c) for c in CATCH_ALL_CODES), \
    "a code cannot be both structurally excluded and a per-city catch-all"
