"""NOGA 2008 as the Canton of Geneva's business register (REG) carries it:
six digits on every row (`CODE_NOGA`), the label beside it (`BRANCHE`).
Keyed at the six-digit leaf.

Georgia's NACE module (`georgia_nace.py`) applied to NOGA, Switzerland's
NACE Rev. 2 with a national sixth digit: the three buckets are divisions 47,
56 and 96 plus vehicle sales in 45, with the standing exclusions of
`docs/category_rules.md` at the leaf (the brief's counting rules,
`docs/build_briefs/geneva.md`; the owner's calls of 2026-10-04: traiteurs
out on R1 and Georgia's precedent, not France's).

**THE CLOSED LIST.** Every code that occurs among the register's
establishments in divisions 45, 47, 56 and 96 (measured 2026-10-07 on the
file of 2026-10-04, 7,884 establishment rows in those divisions, canton-wide)
is named below as kept (`KEPT`) or left out (`OUT`, with the rule). Step 2
exits on a code in those divisions that is in neither, so a daily refresh
that brings a new leaf is seen rather than silently dropped.

**THE LABELS ARE THE REGISTER'S**, from each row's `BRANCHE` (French, as
published). The code rides along in EXTRA_COLUMNS so `classify()` matches on
the code, never on label text.

The premises type (`TYPE_LOCAL`) is not this module's: step 2 drops
home-based, itinerant and stand rows before classifying.
"""

FIELD_LABEL = "Activity (NOGA 2008)"
VALUE_COLUMN = "activity_label"
EXTRA_COLUMNS = ("activity_code",)

_DIVISION_BUCKETS = {
    "45": "Retail",
    "47": "Retail",
    "56": "Food service",
    "96": "Personal services",
}

KEPT = {
    # --- Division 45: vehicle and parts SALES only (R4); repair, washing and
    # wholesale stay out.
    "451102",  # retail of cars and light vehicles
    "451902",  # retail of other motor vehicles (> 3.5 t)
    "453200",  # retail of motor vehicle parts and accessories
    # Motorcycle sale WITH repair, one code: R4's merged type goes whole
    # (Georgia keeps 45.40).
    "454000",
    # --- Division 47: Retail, in stores ------------------------------------
    "471101", "471102", "471103", "471104", "471105", "471901", "471902",
    "472100", "472200", "472300", "472401",
    # Bakery with a tea room: a bakery first, so Retail, as every 47.24.
    "472402",
    "472500", "472600", "472901", "472902",
    # Fuel at a station (R4).
    "473000",
    "474100", "474200", "474300",
    "475100", "475201", "475202", "475300", "475400", "475901", "475902", "475903",
    "476100", "476201", "476202", "476300", "476401", "476402", "476500",
    "477101", "477102", "477103", "477104", "477105", "477201", "477202",
    "477300", "477400", "477501", "477502",
    # Farm and garden supply, flowers, pets and pet supplies: shops.
    "477601", "477602", "477603",
    "477700", "477802", "477803", "477804", "477805", "477806",
    "477901", "477902",
    # --- Division 56: Food service -------------------------------------------
    "561001",  # restaurants, cafés, snack bars, tea rooms, ice-cream parlours
    "561002",  # restaurants with rooms
    "563001",  # bars
    "563002",  # discothèques and night clubs (kept, R5)
    # --- Division 96: Personal services --------------------------------------
    "960101", "960102",   # laundries, dry cleaning
    "960201", "960202",   # hairdressers, beauty institutes
    "960401", "960402",   # saunas and solariums, other physical well-being
}

OUT = {
    # Division 45: everything but sales (R4).
    "451101": "intermediation and wholesale of cars - an agent or wholesaler, not a dealer (R4)",
    "452001": "vehicle maintenance and repair (repairs are out)",
    "452002": "body repair and painting (repairs are out)",
    "452030": "vehicle washing and cleaning - a vehicle service, not retail (R4)",
    "453100": "wholesale of vehicle parts (R4)",
    # Fuel delivered to homes: no counter (the nonstore row).
    "477801": "retail of heating fuel and fuels - a dealer, not a station (R4's nonstore row)",
    # Market stalls (R1: a pitch, not a storefront).
    "478100": "stalls and markets, food (R1)",
    "478900": "stalls and markets, other goods (R1)",
    # Nonstore retail.
    "479100": "mail order or internet - no premises",
    "479900": "other retail not in stores, stalls or markets - no premises",
    # Food with no counter of its own (R1), or an office.
    "561003": "administration and management of restaurants - an office",
    "562100": "event caterers (R1; owner 2026-10-04, Georgia's precedent, not France's)",
    "562900": "other food service: contract catering and canteens (R1)",
    # Funeral (owner, 2026-09-28) and the personal-services catch-all (R2).
    "960300": "funeral services - off every map",
    "960900": "other personal services n.e.c. (R2 catch-all)",
}

TRACKED_DIVISIONS = tuple(_DIVISION_BUCKETS)


def normalise_code(value):
    if value is None:
        return ""
    code = str(value).strip()
    return "" if code.upper() in ("", "NAN") else code


def classify(row):
    """Bucket for a row, or None if it is not tracked storefront commerce."""
    code = normalise_code(row.get("activity_code"))
    if code not in KEPT:
        return None
    return _DIVISION_BUCKETS.get(code[:2])


def unlisted(codes):
    """Codes in the tracked divisions that are neither kept nor left out: a
    new leaf the module has not decided. Step 2 exits on any."""
    return sorted({normalise_code(c) for c in codes
                   if normalise_code(c)[:2] in TRACKED_DIVISIONS}
                  - KEPT - set(OUT))


def legend_label(bucket):
    """The divisions behind each bucket, so a reader can check the mapping
    against the published classification."""
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    return f"{bucket} - NOGA {'/'.join(divisions)}"


_both = sorted(KEPT & set(OUT))
assert not _both, f"codes both kept and left out: {_both}"
_stray = sorted(c for c in KEPT | set(OUT) if c[:2] not in _DIVISION_BUCKETS)
assert not _stray, f"codes outside the tracked divisions: {_stray}"
_counts = {}
for _c in KEPT:
    _counts[_c[:2]] = _counts.get(_c[:2], 0) + 1
# Measured 2026-10-07 on the REG file of 2026-10-04.
assert _counts == {"45": 4, "47": 57, "56": 4, "96": 6}, f"kept-code counts drifted: {_counts}"
