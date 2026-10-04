"""NACE-BEL 2025 (and NACE-BEL 2008 where a unit has no 2025 code), as KBO/BCE
Open Data files it on companies' establishment units - not NAICS.

**A THIN BELGIAN MODULE OVER czech_nace2025.** NACE-BEL 2025 is NACE Rev. 2.1
with Belgian 5- and 7-digit sub-codes, so the division buckets (47 Retail, 56
Food service, 96 Personal services) and the structural exclusions by prefix
are czech_nace2025's, imported, never copied. Two more are added on
france_naf.py's precedent (docs/build_briefs/brussels_regional.md, "The bucket
rule"): 96.101 industrial laundries (France's 96.01A, "de gros") and 47.781
heating-fuel dealers (France's 47.78B; the category rules' nonstore row).

**KBO's codes are 5 digits, no dots** (`56111`, measured 2026-10-04 on 200,000
activity rows: every code 5 digits). Labels are FPS Economy's own (`code.csv`,
French), looked up by the step that reads KBO; `classify()` matches on the
code and never on label text.

**NACE-BEL 2008 only where a unit has no 2025 MAIN code** (0.1% decide on it,
the brief): france_naf.py's structural set at class level, written as
prefixes - 47.8 market stalls, 47.9 nonstore, 56.2 catering, 96.03 funeral,
96.011 industrial laundries, 47.781 heating fuel.

**ONE UNIT, SEVERAL MAIN CODES.** 36% of legal establishments list five or
more distinct MAIN codes, unordered. The rule measured and approved (owner,
2026-10-03, call 12): any MAIN code in a bucket, priority Food service over
Retail over Personal services (`unit_bucket()`). Step 2 runs the priority
BEFORE it drops Personal services (off on the Brussels (Regional) page), so
a unit with a food or retail code keeps that bucket and a personal-only unit
leaves the map. `classify()` answers for one code, as every taxonomy does;
step 2 writes the code that decided the unit's bucket.

**CATCH_ALL_CODES is rule A's list** (step 2): a unit whose every in-bucket
MAIN code is one of these is dropped. Belgium's list, not Czechia's (whose
CATCH_ALL_CODES differs). Classified normally here; the verdict is step 2's.
"""
from pipeline.taxonomies import czech_nace2025 as _cz

FIELD_LABEL = "Activity (NACE-BEL)"
VALUE_COLUMN = "nace_label"
EXTRA_COLUMNS = ("nace_code", "nace_version")

FOOD, RETAIL, PERSONAL = "Food service", "Retail", "Personal services"
PRIORITY = (FOOD, RETAIL, PERSONAL)

V2025, V2008 = "2025", "2008"

_DIVISION_BUCKETS = dict(_cz._DIVISION_BUCKETS)

# NACE-BEL 2025: czech_nace2025's prefixes plus the two on france_naf.py's
# precedent.
NOT_PREMISES_2025 = {
    **_cz.NOT_PREMISES_PREFIXES,
    "96101": "industrial laundries (france_naf 96.01A, de gros)",
    "47781": "heating-fuel dealers, nonstore (france_naf 47.78B; category rules)",
}

# NACE-BEL 2008, class level, france_naf.py's structural set.
NOT_PREMISES_2008 = {
    "478": "market stalls (france_naf 47.81Z-47.89Z)",
    "479": "nonstore retail (france_naf 47.91, 47.99)",
    "562": "catering and contract food service (france_naf 56.21Z, 56.29A)",
    "9603": "funeral services (france_naf 96.03Z)",
    "96011": "industrial laundries (france_naf 96.01A)",
    "47781": "heating-fuel dealers, nonstore (france_naf 47.78B)",
}

# Rule A's catch-alls (the brief, "The base, then the four rules"): residual
# wording in FPS Economy's own labels ("autre", "nca").
CATCH_ALL_CODES_2025 = frozenset({
    "47120",   # Autre commerce de détail non spécialisé
    "47279",   # Autres commerces de détail alimentaires nca
    "47690",   # Commerce de détail de biens culturels et de loisirs nca
    "47789",   # Autre commerce de détail de biens neufs nca
    "96999",   # Autres services personnels
})
# 2008's own list where 2008 decides (0.1% of units): the screen's
# (staging's kbo_screen_defs.py, 2026-10-03), which the brief's counts were
# measured with: 47.191 and 47.192 non-food non-specialised, 47.299 other
# food nca, 47.789 other new goods nca, 96.099 other personal services.
CATCH_ALL_CODES_2008 = frozenset({"47191", "47192", "47299", "47789", "96099"})


def normalise_code(value):
    """KBO's code as a digit string (`56111`); dots and spaces dropped."""
    if value is None:
        return ""
    code = str(value).strip().replace(".", "").replace(" ", "")
    if not code or code.upper() == "NAN" or not code.isdigit():
        return ""
    return code


def normalise_version(value):
    v = str(value).strip() if value is not None else ""
    return V2008 if v == V2008 else V2025


def excluded(code, version=V2025):
    """The structural exclusion a code falls under, or None."""
    table = NOT_PREMISES_2008 if normalise_version(version) == V2008 else NOT_PREMISES_2025
    return next((p for p in table if code.startswith(p)), None)


def code_bucket(code, version=V2025):
    """Bucket for one code, or None if it is not tracked storefront commerce."""
    code = normalise_code(code)
    if len(code) < 2 or excluded(code, version):
        return None
    return _DIVISION_BUCKETS.get(code[:2])


def is_catch_all(code, version=V2025):
    """A catch-all at 5 digits; a Belgian 7-digit sub-code (`4712021`) is its
    5-digit parent's."""
    table = CATCH_ALL_CODES_2008 if normalise_version(version) == V2008 else CATCH_ALL_CODES_2025
    return normalise_code(code)[:5] in table


def only_catch_alls(codes, version=V2025):
    """Rule A (the screen's definition, which the brief's counts measure):
    every MAIN code in divisions 47, 56 and 96 is a catch-all. A code the
    structural exclusions remove still counts as a non-catch-all there;
    codes outside the three divisions are ignored."""
    div = [normalise_code(c) for c in codes if normalise_code(c)[:2] in _DIVISION_BUCKETS]
    return bool(div) and all(is_catch_all(c, version) for c in div)


def label_code(code):
    """NACE-BEL's written form: `47.120`, `47.120.21`."""
    c = normalise_code(code)
    if len(c) == 7:
        return f"{c[:2]}.{c[2:5]}.{c[5:]}"
    return f"{c[:2]}.{c[2:]}" if len(c) > 2 else c


def unit_bucket(codes, version=V2025):
    """The unit's bucket from ALL its MAIN codes: any code in a bucket,
    Food service over Retail over Personal services. Returns (bucket, code
    that decided it), or (None, None). Within the winning bucket the decisive
    code is the lowest non-catch-all code, else the lowest code, so the
    written code is deterministic."""
    found = {}
    for c in codes:
        c = normalise_code(c)
        b = code_bucket(c, version)
        if b:
            found.setdefault(b, set()).add(c)
    for b in PRIORITY:
        if b in found:
            best = sorted(found[b], key=lambda c: (is_catch_all(c, version), c))[0]
            return b, best
    return None, None


def legend_label(bucket):
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    return f"{bucket} - NACE-BEL {'/'.join(divisions)}"


def classify(row):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py): the
    bucket of the row's decisive code. A row without a version is 2025."""
    return code_bucket(row.get("nace_code"), row.get("nace_version"))


assert all(p[:2] in _DIVISION_BUCKETS for p in NOT_PREMISES_2025), \
    "a NACE-BEL 2025 exclusion names a code outside divisions 47/56/96"
assert all(p[:2] in _DIVISION_BUCKETS for p in NOT_PREMISES_2008), \
    "a NACE-BEL 2008 exclusion names a code outside divisions 47/56/96"
assert not any(excluded(c) for c in CATCH_ALL_CODES_2025), \
    "a 2025 code cannot be both structurally excluded and a catch-all"
assert not any(excluded(c, V2008) for c in CATCH_ALL_CODES_2008), \
    "a 2008 code cannot be both structurally excluded and a catch-all"
# Car retail is Retail in Rev. 2.1 (R4); fuel at a station stays; heating fuel goes.
assert code_bucket("47811") == RETAIL and code_bucket("47300") == RETAIL
assert code_bucket("47781") is None and code_bucket("47781", V2008) is None
assert unit_bucket(["47120", "56111", "96210"]) == (FOOD, "56111")
assert unit_bucket(["96210", "47789"]) == (RETAIL, "47789")
