"""SCIAN - Sistema de Clasificacion Industrial de America del Norte, the
Mexican member of the NAICS family, as published in INEGI's DENUE.

READ THIS BEFORE ASSUMING naics.py WOULD HAVE WORKED. SCIAN and NAICS are the
same trilateral standard and agree at the detailed level - a beauty salon is
812110 in both, a taco restaurant 722514 in both - but **they do not agree on
the retail sector number**, and this project's Retail bucket is anchored on
exactly that:

    bucket             NAICS (US)            SCIAN (MX)
    Retail             44-45                 46            <-- DIFFERENT
    Wholesale          42                    43            (neither is a bucket)
    Food service       722                   722           same
    Personal services  812                   812           same

`docs/global_country_shortlist.md` recorded "SCIAN = NAICS, so the taxonomy may
transfer". Measured against DENUE on 2026-09-22, that is right for two buckets
of three and wrong for the largest. naics.py pointed at DENUE finds **no rows
at all** under 44/45 and silently leaves 212,251 CDMX retail rows - 45.87% of
the whole file - unclassified.

So this module exists for two prefixes, and is otherwise naics.py's logic. It
is deliberately a separate module rather than a flag on naics.py: the two
classify different countries' registers, and a shared module with a country
switch would put the most consequential constant in this project behind an
argument.

MEASURED on DENUE 2026-09-22, Ciudad de Mexico (state 09, 462,732 units) with
Jalisco (state 14, 401,813) as the second reading, per add-country's rule that
a capital alone is not a country:

    46   Retail               212,251   45.87%
    81   (all)                 67,707   14.63%   <- see the 812 carve-out below
    72   (all)                 58,167   12.57%   <- includes 721, see below
    43   Wholesale             15,525    3.36%   (not a bucket, as in NAICS)

The three buckets together are **73.07%** of DENUE CDMX and 68.39% of
Guadalajara - the highest storefront share of any register measured in this
project, against Philadelphia's 79% landlords and Finland's 53% real estate.
"""

# (bucket name from pipeline.taxonomies.CATEGORY_BUCKETS, SCIAN prefixes).
# Prefix match on the code as a string, so "46" catches 461, 4611, 461110.
#
# NOTE these are the SAME PRECISION as naics.py's, deliberately: Food service
# is 722 and not 72, and Personal services is 812 and not 81. Widening either
# to two digits is the obvious-looking mistake and it is wrong in both
# countries:
#   721  Accommodation - hotels. 999 units in CDMX. A hotel is not food service.
#   811  Repair and maintenance - 27,216 units in Jalisco, the largest single
#        block inside 81. Auto repair is not a personal service, and this
#        project has never counted 811 in any city.
#   813  Civic, religious and professional associations - 5,392 in Jalisco.
#        Not a storefront.
# Counting `72` instead of `722` once inflated this project's CDMX food service
# from 57,168 to 58,167.
SCIAN_GROUPS = [
    ("Retail", ("46",)),
    ("Food service", ("722",)),
    ("Personal services", ("812",)),
]

# Carved back OUT of the groups above, the SCIAN twins of naics.py's
# NAICS_EXCLUDE_PREFIXES. Same reasoning, different code numbers - which is the
# point of this module.
#
#   469     Comercio al por menor exclusivamente a traves de Internet, y
#           catalogos impresos, television y similares. SCIAN's nonstore
#           retail subsector, the exact twin of NAICS 454, and excluded for the
#           same reason: it is not a storefront and SCIAN itself says so in the
#           name. Small here - 90 units in CDMX, 42 in Jalisco - unlike the US,
#           where nonstore was 10.1% of Los Angeles's pins. Recorded because
#           the SIZE differing does not change the reasoning.
#   812410  Estacionamientos y pensiones para vehiculos automotores. Parking,
#           the twin of NAICS 81293. 2,230 units in CDMX. A parking trip is
#           planned rather than incidental foot traffic from a station, so it
#           sits outside this project's question.
#   8123    Servicios funerarios y administracion de cementerios - 812310
#           funeral services, 812321/812322 private and public cemeteries.
#           Funeral services off every map (owner, 2026-09-28): not
#           storefronts. NOT naics.py's 8122: SCIAN numbers death care 8123
#           and laundries 8122 (812210 Lavanderias y tintorerias), the reverse
#           of NAICS, so copying the NAICS prefix would drop every laundry.
#   7223    Servicios de preparacion de alimentos por encargo - 722310
#           comedor para empresas e instituciones, 722320 alimentos para
#           ocasiones especiales, 722330 alimentos en unidades moviles. Food
#           with no counter of its own (owner, 2026-09-29): an institutional
#           canteen, an event caterer and a food truck. Unlike Los Angeles'
#           NAICS 722300, DENUE never files a row at the undifferentiated
#           7223 level - all three six-digit codes are named - so the whole
#           industry group goes. Checked against SCIAN's own labels, not
#           copied from naics.py: the numbers happen to agree here.
#   812990  Otros servicios personales - the "other personal services"
#           catch-all, excluded everywhere (owner, 2026-09-29). SCIAN has no
#           code of its own for tattooing, so any tattoo studio DENUE files
#           here goes with it.
#   812130  Sanitarios publicos y bolerias - public toilets and shoe-shine
#           stands (owner, 2026-09-29): neither is a walk-in shop. Its
#           sibling 812120 Banos publicos (bathhouses) stays.
#
# A prefix here always wins over SCIAN_GROUPS.
SCIAN_EXCLUDE_PREFIXES = ("469", "812410", "8123",
                          "7223",               # (owner, 2026-09-29) R1
                          "812990", "812130")   # (owner, 2026-09-29) R2

# What DENUE calls the activity, in Spanish, as INEGI wrote it. The tooltip
# shows the register's own words rather than a translation - add-country's
# rule, so cross-city comparison survives on the English bucket names without
# hiding what the source actually said.
FIELD_LABEL = "Actividad (SCIAN)"
VALUE_COLUMN = "scian_actividad"

# classify() reads the 6-digit CODE, not the label above: `nombre_act` is free
# text that INEGI can reword between editions, while `codigo_act` is the
# standard. Step 2 carries both.
EXTRA_COLUMNS = ("scian",)


def scian_label(name: str, prefixes: tuple) -> str:
    return f"{name} — SCIAN: {'/'.join(prefixes)}"


def legend_label(bucket: str) -> str:
    """Taxonomy-module interface: legend text for a bucket."""
    for name, prefixes in SCIAN_GROUPS:
        if name == bucket:
            return scian_label(name, prefixes)
    return bucket


# Exact codes carried INTO a bucket from outside the group prefixes.
#   522452  Casas de empeño - pawnshops, which DENUE files in credit (5224)
#           under a code of their own. Pawnbrokers are kept as Retail in every
#           city (R5; owner, 2026-09-29, DECISIONS "Category check: the owner's
#           calls"); 381 in Mexico City's file. Its credit neighbours stay out.
SCIAN_INCLUDE_CODES = {"522452": "Retail"}


def scian_group(code: str):
    """A SCIAN code -> its bucket name, or None if it is not a tracked
    storefront category."""
    code = str(code)
    if code in SCIAN_INCLUDE_CODES:
        return SCIAN_INCLUDE_CODES[code]
    if code.startswith(SCIAN_EXCLUDE_PREFIXES):
        return None
    for name, prefixes in SCIAN_GROUPS:
        if code.startswith(prefixes):
            return name
    return None


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` must carry a `scian` key with the raw 6-digit code."""
    code = row.get("scian")
    if not code:
        return None
    return scian_group(code)


# Import-time guards on the codes this module actually turns on, in the style of
# edmonton_licencecategory.py. These are real DENUE codes measured on
# 2026-09-22; if a future SCIAN revision renumbers them, this fails loudly at
# import rather than silently reclassifying a city.
assert scian_group("461110") == "Retail", "abarrotes must be Retail"
assert scian_group("463211") == "Retail", "ropa must be Retail"
assert scian_group("722514") == "Food service", "taqueria must be Food service"
assert scian_group("812110") == "Personal services", "salon must be Personal services"
# The carve-outs, each of which would otherwise be swept in by a group prefix.
assert scian_group("469110") is None, "nonstore retail must be excluded"
assert scian_group("812410") is None, "parking must be excluded"
assert scian_group("812310") is None, "funeral services must be excluded"
assert scian_group("812322") is None, "cemeteries must be excluded"
assert scian_group("812210") == "Personal services", "laundries (SCIAN 8122) must stay"
# (owner, 2026-09-29): the no-counter food codes, the catch-all, and toilets /
# shoe-shine go; their near neighbours stay.
for _c in ("722310", "722320", "722330", "812990", "812130"):
    assert scian_group(_c) is None, f"{_c} must be excluded (owner, 2026-09-29)"
assert scian_group("722511") == "Food service", "restaurants (7225) must stay"
assert scian_group("722412") == "Food service", "bars (7224) must stay"
assert scian_group("812120") == "Personal services", "banos publicos must stay"
assert scian_group("812910") == "Personal services", "photo developing must stay"
assert scian_group("721111") is None, "hotels must NOT be Food service"
assert scian_group("811111") is None, "auto repair must NOT be Personal services"
assert scian_group("813210") is None, "religious associations must NOT be a bucket"
# And the one that makes this module necessary at all.
assert scian_group("445110") is None, (
    "NAICS 445 must not classify here - SCIAN numbers retail 46, and a code "
    "in the NAICS 44-45 range appearing in DENUE would mean the wrong "
    "classification standard was applied to the file."
)
