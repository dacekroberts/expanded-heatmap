"""DB25 - Denmark's industrial classification (Dansk Branchekode 2025), keyed
at the 6-digit national sub-class.

**NATIONAL, NOT PER-CITY.** DB25 is Danmarks Statistik's, and CVR is one
register for the whole country - France's and Norway's shape. Copenhagen is
the first city on it; a second Danish city inherits this module unchanged.
Per-city verdicts do NOT belong here - see "What this module deliberately does
NOT decide" below.

**IT IS DB25, NOT DB07 - AND THE BRIEF ASSUMED DB07.** Measured 2026-09-24:
every current hovedbranche code in Kobenhavn and Frederiksberg is six digits
(153,986 of 153,986), classes that exist only in NACE Rev. 2.1 are populated
(`962100` frisør 1,351, `962200` skønhed 1,064, `478100` motorkøretøjer 111,
`479100` formidling 100) and Rev. 2's 96.02 / 96.09 have no rows. CVR
recoded every active unit on 1 January 2025. DB25 is Denmark's version of
**NACE Rev. 2.1** - the same parent as Norway's SN2025 - so this module's
exclusions are Oslo's, matched at the shared 4-digit class, and the two
changes Oslo recorded reach Copenhagen too:

  * **Motor-vehicle retail moved INTO division 47** (47.81-47.83). Kept, on
    Madrid's precedent, as in Oslo.
  * **The store / non-store distinction was ABOLISHED.** A web shop is filed
    under the product it sells, so distance selling CANNOT be excluded by
    code here. A limit to disclose, not a filter to pretend.

**WHY THE 6-DIGIT LEVEL.** CVR's `Branche` file carries `vaerdiTekst` -
Danmarks Statistik's own label - beside every code, and only at six digits,
which is also the finest level: Barcelona's, Paris's and Oslo's shape. The
brief's shallower "levels" were computed by truncating codes and judging them
by a sibling's label, which is order-dependent, and are not used.

**THE THREE DIVISIONS.** As in NAF and SN2025, the buckets are whole
divisions:

    47  Detailhandel                        -> Retail
    56  Restaurationsvirksomhed             -> Food service
    96  Personlige serviceydelser           -> Personal services

**THE LABELS ARE THE REGISTER'S, VERBATIM.** Step 2 carries `vaerdiTekst` as
VALUE_COLUMN; `classify()` matches on the code in EXTRA_COLUMNS and never on
label text.
"""

# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

FIELD_LABEL = "Branchekode (DB25)"
VALUE_COLUMN = "db25_label"
EXTRA_COLUMNS = ("db25_code",)


# ---------------------------------------------------------------------------
# What this module deliberately does NOT decide
# ---------------------------------------------------------------------------
#
# A catch-all's composition is a fact about a city, so the verdict lives in
# `pipeline/<city>/config.py` (CATCH_ALL_EXCLUDE), as in France and Norway.
# These are the codes whose own label is residual wording - "anden/andre",
# "øvrige", "i.a.n." (ikke andetsteds nævnt). They are classified normally.
CATCH_ALL_CODES = {
    "969900",   # Andre personlige serviceydelser i.a.n.
    "471200",   # Anden ikke-specialiseret detailhandel
    "472700",   # Detailhandel med andre fødevarer
    "475590",   # Detailhandel med boligtekstiler, belysnings- og husholdningsartikler i.a.n.
    "476990",   # Detailhandel med andre kulturelle artikler i.a.n
    "477800",   # Detailhandel med andre nye varer
    "561190",   # Drift af øvrige spisesteder
}


# ---------------------------------------------------------------------------
# Structural exclusions - NOT premises, anywhere in Denmark
# ---------------------------------------------------------------------------
#
# Matched on the 4-digit NACE Rev. 2.1 CLASS, which DB25 shares with SN2025 -
# so these are Oslo's, read against DB25's own labels 2026-09-24. A class is
# excluded whole: every 6-digit code under it carries the same activity.
NOT_PREMISES_CLASSES = {
    # Intermediation - NEW in NACE Rev. 2.1: agents and platforms arranging a
    # sale or a service for someone else. No counter to walk up to.
    "4791",     # Formidlingsaktiviteter inden for ikke-specialiseret detailhandel
    "4792",     # Formidlingsaktiviteter inden for specialiseret detailhandel
    "5640",     # Formidlingsaktiviteter i forbindelse med restaurationsaktiviteter
    "9640",     # Formidlingsaktiviteter inden for personlige serviceydelser

    # Mobile food stalls - France's "éventaires et marchés" reasoning: a
    # pitch, not a storefront, and the registered location is the trader's.
    "5612",     # Drift af mobile madboder

    # Event catering - the work happens AT THE EVENT (Oslo's reasoning, which
    # deliberately differs from France's traiteur).
    "5621",     # Event catering

    # Contract catering and canteens - a kitchen inside someone else's
    # institution.
    "5622",     # Catering på kontrakt og andre restaurationsaktiviteter

    # Personal services performed in the client's home.
    "9691",     # Levering af personlige serviceydelser i hjemmet
}

# ONE DANISH ADDITION, at the 6-digit level because DB25 splits the class
# where SN2025 does not: 96.10 is industrial laundries AND the dry cleaner on
# the corner, and only the first is excluded. `961020` - "renserier og
# selvbetjeningsvaskerier" - stays.
NOT_PREMISES_CODES = {
    "961010",   # Drift af erhvervs- og institutionsvaskerier
}

_DIVISION_BUCKETS = {
    "47": "Retail",
    "56": "Food service",
    "96": "Personal services",
}


def normalise_code(value):
    """The register's code as a canonical 6-digit string, `561110`.

    CVR publishes it flat; a dotted `56.11.10` is accepted too, because an
    unrecognised format would make classify() return None for every row and
    empty the map rather than raise.
    """
    if value is None:
        return ""
    code = str(value).strip().replace(".", "").replace(" ", "")
    if not code or code.upper() == "NAN":
        return ""
    return code


def classify(row):
    """Bucket for a row, or None if it is not tracked storefront commerce."""
    code = normalise_code(row.get("db25_code"))
    if len(code) != 6 or not code.isdigit():
        return None
    if code in NOT_PREMISES_CODES or code[:4] in NOT_PREMISES_CLASSES:
        return None
    return _DIVISION_BUCKETS.get(code[:2])


def legend_label(bucket):
    """The division numbers beside the bucket, so a reader can check the
    mapping against Danmarks Statistik's published classification."""
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    return f"{bucket} - DB25 {'/'.join(divisions)}"


# Every exclusion must sit in a tracked division, or it is dead weight that
# hides a typo.
assert all(c[:2] in _DIVISION_BUCKETS
           for c in NOT_PREMISES_CLASSES | NOT_PREMISES_CODES | CATCH_ALL_CODES), \
    "a DB25 exclusion names a code outside divisions 47/56/96"
assert not any(c[:4] in NOT_PREMISES_CLASSES or c in NOT_PREMISES_CODES
               for c in CATCH_ALL_CODES), \
    "a code cannot be both structurally excluded and a per-city catch-all"
