"""SN2025 - Norway's standard industrial classification, keyed at the 5-digit
national sub-class.

**NATIONAL, NOT PER-CITY.** SN2025 is Statistics Norway's (SSB), and the
Brønnøysund Register Centre's Enhetsregisteret is one register for the whole
country - France's shape, not Spain's. Oslo is the first city on it; a second
Norwegian city inherits this module unchanged. Per-city verdicts do NOT belong
here - see "What this module deliberately does NOT decide" below.

**IT IS SN2025, NOT SN2007 - AND THE BRIEF ASSUMED SN2007.** Measured
2026-09-24 on the register's own labels: `47.810` reads *Detaljhandel med
motorvogner* and `96.230` *Aktiviteter i dagspa, badstue og dampbad*. Neither
exists in SN2007. SN2025 is Norway's version of **NACE Rev. 2.1**, which the
register switched to, and two of its changes reach this project directly:

  * **Motor-vehicle retail moved INTO division 47** (47.81-47.83; it was
    division 45). Kept, on Madrid's precedent: NAICS 441 sits inside 44-45, so
    "every other city in this project already counts a car dealer as retail".
  * **The store / non-store distinction was ABOLISHED.** NACE Rev. 2 had
    "retail sale via mail order or via Internet" and "via stalls and markets"
    as their own codes, and France excludes them by code. Rev. 2.1 files a web
    shop under the product it sells. **So distance selling CANNOT be excluded
    by code here** - an online-only clothes seller is `47.710` like a clothes
    shop. That is a limit to disclose, not a filter to pretend.

**WHY THE 5-DIGIT LEVEL.** Every row in the register carries a 5-digit code
(13,458 of 13,458 Oslo bucket rows), so a level can be chosen - unlike
Prague's ragged CZ-NACE. The brief's premises-taxonomy measurement (against
SSB's labels) found catch-all shares of 38.4% at group, 18.5% at class and
15.5% at the 5-digit level: the finest level, Barcelona's and Paris's shape.

**THE THREE DIVISIONS.** As in NAF, the buckets map onto whole divisions:

    47  Detaljhandel               -> Retail
    56  Serveringsvirksomhet       -> Food service
    96  Personlig tjenesteyting    -> Personal services

**THE LABELS ARE THE REGISTER'S, VERBATIM.** Brønnøysund publishes
`naeringskode1.beskrivelse` beside every code, which is SSB's own wording.
Step 2 carries it as VALUE_COLUMN; `classify()` matches on the code in
EXTRA_COLUMNS and never on label text.
"""

# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

FIELD_LABEL = "Næringskode (SN2025)"
VALUE_COLUMN = "sn2025_label"
EXTRA_COLUMNS = ("sn2025_code",)

# The register's columns, for a city config's RAW_* settings.
REGISTER_CODE_COLUMN = "naeringskode1.kode"
REGISTER_LABEL_COLUMN = "naeringskode1.beskrivelse"


# ---------------------------------------------------------------------------
# What this module deliberately does NOT decide
# ---------------------------------------------------------------------------
#
# A catch-all's composition is a fact about a city, so the verdict lives in
# `pipeline/<city>/config.py` (CATCH_ALL_EXCLUDE), as in France. These are the
# codes whose own SSB label is residual wording - "ellers", "annen/andre",
# "ikke nevnt annet sted". They are classified normally here.
CATCH_ALL_CODES = {
    "96.990",   # Andre personlige tjenester ikke nevnt annet sted
    "47.120",   # Detaljhandel med bredt vareutvalg ellers
    "47.270",   # Detaljhandel med nærings- og nytelsesmidler ellers
    "47.559",   # Detaljhandel med innredningsartikler ikke nevnt annet sted
    "47.690",   # Detaljhandel med kulturvarer ikke nevnt annet sted
    "47.780",   # Annen detaljhandel med andre nye varer
}


# ---------------------------------------------------------------------------
# Structural exclusions - NOT premises, anywhere in Norway
# ---------------------------------------------------------------------------
#
# A code whose own label says the activity happens away from a shop is not a
# storefront in any Norwegian city, so these belong to the classification.
# Each was read against its label and Oslo's measured profile (share with
# registered employees / share with an ENK sole-trader parent), 2026-09-24.
NOT_PREMISES = {
    # Intermediation - NEW in NACE Rev. 2.1: agents and platforms that arrange
    # a sale or a service for someone else. There is no counter to walk up to.
    "47.910",   # Formidlingstjenester ... detaljhandel med bredt vareutvalg
    "47.920",   # Formidlingstjenester ... detaljhandel med spesialisert vareutvalg
    "56.400",   # Formidlingstjenester tilknyttet serveringsvirksomhet
    "96.400",   # Formidlingstjenester tilknyttet personlig tjenesteyting

    # Mobile food outlets - France's "éventaires et marchés" reasoning: a
    # pitch, not a storefront, and the registered location is the trader's.
    "56.120",   # Drift av mobile serveringssteder

    # Canteens and contract catering - a kitchen inside someone else's
    # institution. France excludes the same shape (56.29A, restauration
    # collective sous contrat) and Milan by keyword ("mensa").
    "56.220",   # Kantinedrift og annen cateringvirksomhet

    # Event catering. ⚠ THIS DIFFERS FROM FRANCE, deliberately: NAF's 56.21Z
    # "services des traiteurs" is kept there, because a French traiteur is
    # usually a shop. Norway's label says the work happens AT THE EVENT, and
    # Oslo's profile agrees - 27% have registered employees, 53% an ENK parent.
    "56.210",   # Catering for arrangementer

    # Personal services performed in the client's household.
    "96.910",   # Personlig tjenesteyting i husholdninger
}

_DIVISION_BUCKETS = {
    "47": "Retail",
    "56": "Food service",
    "96": "Personal services",
}


def normalise_code(value):
    """The register's code as a canonical `47.110`.

    Brønnøysund publishes it dotted (`47.110`); a flat `47110` is accepted too,
    because an unrecognised format would make `classify()` return None for
    every row and empty the map rather than raise.
    """
    if value is None:
        return ""
    code = str(value).strip().replace(" ", "")
    if not code or code.upper() == "NAN":
        return ""
    if "." not in code and len(code) == 5 and code.isdigit():
        code = f"{code[:2]}.{code[2:]}"
    return code


def classify(row):
    """Bucket for a row, or None if it is not tracked storefront commerce."""
    code = normalise_code(row.get("sn2025_code"))
    if not code or code in NOT_PREMISES:
        return None
    return _DIVISION_BUCKETS.get(code[:2])


def legend_label(bucket):
    """The division numbers beside the bucket, so a reader can check the
    mapping against SSB's published classification."""
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    return f"{bucket} - SN2025 {'/'.join(divisions)}"


# Every excluded code must sit in a tracked division, or it is dead weight
# that hides a typo.
assert all(c[:2] in _DIVISION_BUCKETS for c in NOT_PREMISES | CATCH_ALL_CODES), \
    "an SN2025 exclusion names a code outside divisions 47/56/96"
assert not (NOT_PREMISES & CATCH_ALL_CODES), \
    "a code cannot be both structurally excluded and a per-city catch-all"
