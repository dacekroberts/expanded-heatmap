"""WZ 2025 - Germany's classification of economic activities (NACE Rev. 2.1),
as a chamber of commerce (IHK) publishes it for its members, matched on PREFIX.

**NAMED FOR THE SOURCE KIND, NOT THE COUNTRY.** The codes are Destatis's
WZ 2025, but what the buckets can hold is decided by who is in an IHK
register: every trading business EXCEPT the crafts (Handwerk), which belong to
the Handwerkskammer instead. So hairdressers (96.21) and laundries (96.10) are
all but absent - 180 and 215 rows in IHK Berlin's 367,575 (2026-09-28), where
they are the largest personal-services classes in every other city here - and
bakers, butchers and opticians are thin. That is a property of any IHK
register, and the legend says it. IHK Berlin is the first (and, as of
2026-09-28, the only chamber that publishes one).

**IT IS NACE Rev. 2.1 AT 4 DIGITS (`nace_id`), NOT WZ 2008 SUBCLASSES.**
Measured on Berlin 2026-09-28: `5610` has 0 rows, `5611` (56.11 Restaurants,
a Rev. 2.1 class) 14,962. The finer `ihk_branch_id` is IHK's OWN scheme (5-7
digits under the WZ class: `47122`, `962201` Nagelstudio); it is read only
for per-city catch-all verdicts, never for bucketing. Same parent as
czech_nace2025, norway_sn2025 and denmark_db25, so the structural exclusions
below are theirs, and the two Rev. 2.1 consequences apply: car retail sits in
division 47 (kept), and online shops cannot be excluded by code (no IHK branch
label names mail order or online retail).

**RAGGED DEPTH**: 2,389 of Berlin's rows carry a 2- or 3-digit `nace_id`
(`47`, `561`). Every row still carries its division, so bucketing is safe; an
exclusion is the SHORTEST prefix that means only the excluded activity.

**THE LABELS ARE THE REGISTER'S OWN** (`nace_desc`, German, verbatim).
`classify()` matches on the code in EXTRA_COLUMNS and never on label text.
"""

FIELD_LABEL = "WZ 2025"
VALUE_COLUMN = "nace_desc"
EXTRA_COLUMNS = ("nace_id", "ihk_branch_id")   # the branch only for INCLUDE_BRANCHES

_DIVISION_BUCKETS = {
    "47": "Retail",
    "56": "Food service",
    "96": "Personal services",
}

# What the bucket holds, where an IHK register cannot hold all of it. Legend
# text only - classification never reads this. KEPT SHORT ON PURPOSE: the
# legend must fit the label solver's 274 px model (map_common.LEGEND_MODEL_W);
# "(no hairdressers or laundries)" made Berlin's legend 379 px at the 1000 px
# frame and put 6 line labels under it. The page and
# docs/excluded_categories.md say what is missing.
# DRAFT, awaiting the owner's approval of the wording (2026-09-28).
_BUCKET_NOTES = {
    "Personal services": "partial",
}

# ---------------------------------------------------------------------------
# Structural exclusions - NOT premises, in any IHK register
# ---------------------------------------------------------------------------
#
# Oslo's, Copenhagen's and Prague's NACE Rev. 2.1 set, read against the
# register's own German labels 2026-09-28:
NOT_PREMISES_PREFIXES = {
    # 47.9 in Rev. 2.1 is entirely intermediation (47.91, 47.92).
    "479": "Vermittlungstätigkeiten für den Einzelhandel",
    # 56.12, mobile food.
    "5612": "Mobile Gastronomie",
    # 56.2, catering: the work happens at the event or in someone else's
    # institution.
    "562": "Event-Caterer; Sonstige Caterer",
    # 56.4 and 96.4, intermediation for food service and personal services.
    "564": "Vermittlungstätigkeiten für gastronomische Dienstleistungen",
    "964": "Vermittlungstätigkeiten für persönliche Dienstleistungen",
    # 96.91, personal services in the customer's household.
    "9691": "Persönliche Dienstleistungen in Haushalten",
    # 96.3 is entirely 96.30, funeral and related activities. Funeral services
    # off every map (owner, 2026-09-28): not storefronts.
    "963": "Bestattungswesen",
}

# Codes whose own label is residual wording ("sonstige", "a. n. g."), at the
# WZ level. Classified normally; the per-city verdict is the city config's
# CATCH_ALL_EXCLUDE, which may also name IHK branch codes.
CATCH_ALL_CODES = {
    "4712",   # Sonstiger Einzelhandel mit Waren verschiedener Art
    "4727",   # Einzelhandel mit sonstigen Nahrungs- und Genussmitteln
    "4769",   # Einzelhandel mit Kunst- und Kulturerzeugnissen a. n. g.
    "4778",   # Einzelhandel mit sonstigen Neuwaren
    "9699",   # Erbringung von sonstigen überwiegend persönlichen Dienstleistungen a. n. g.
}


def normalise_code(value):
    """The register's code as a digit string at its own depth (`47`, `5611`)."""
    if value is None:
        return ""
    code = str(value).strip().replace(".", "").replace(" ", "")
    if not code or code.upper() == "NAN" or not code.isdigit():
        return ""
    return code


def excluded(code):
    """The structural exclusion a code falls under, or None."""
    return next((p for p in NOT_PREMISES_PREFIXES if code.startswith(p)), None)


# IHK branches carried INTO a bucket from a class that is not one (the class
# alone cannot say it). 64922 Leihhäuser - pawnshops, filed in 6492 other
# credit granting; kept as Retail in every city (R5; owner, 2026-09-29,
# DECISIONS "Category check: the owner's calls"). 35 in Berlin.
INCLUDE_BRANCHES = {"64922": "Retail"}


def classify(row):
    """Bucket for a row, or None if it is not tracked storefront commerce."""
    branch = str(row.get("ihk_branch_id") or "").strip()
    if branch in INCLUDE_BRANCHES:
        return INCLUDE_BRANCHES[branch]
    code = normalise_code(row.get("nace_id"))
    if len(code) < 2 or excluded(code):
        return None
    return _DIVISION_BUCKETS.get(code[:2])


def legend_label(bucket):
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    note = _BUCKET_NOTES.get(bucket)
    head = f"{bucket} ({note})" if note else bucket
    return f"{head} - WZ {'/'.join(divisions)}"


assert all(p[:2] in _DIVISION_BUCKETS for p in NOT_PREMISES_PREFIXES), \
    "a WZ exclusion names a code outside divisions 47/56/96"
assert not any(excluded(c) for c in CATCH_ALL_CODES), \
    "a code cannot be both structurally excluded and a per-city catch-all"
