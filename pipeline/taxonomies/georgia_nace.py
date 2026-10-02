"""NACE Rev. 2 as Georgia publishes it (NCG 006-2016, a national fifth digit:
`47.59.2`), keyed at the national leaf. Geostat's Statistical Business
Register carries it as `Activity_2_Code`, single-valued.

**NATIONAL, NOT PER-CITY**, like `france_naf.py`, on which this module is
modelled: the three buckets are divisions 47, 56 and 96, with the standing
exclusions of `docs/category_rules.md` at the leaf. Built for Tbilisi
(2026-10-02); any later Georgian city reads the same register.

**NEVER KEY ON `Activity_Code`.** The register also carries the old
Rev. 1.1-shaped code (`52.11.0` retail, `93.02.0` hairdressing); its numbers
mean different trades.

**THE CLOSED LIST.** Every code that occurs in divisions 45, 47, 56 and 96 is
named below as kept (`KEPT`) or left out (`OUT`, with the rule). Step 2 exits
on a code in those divisions that is in neither, so a refresh that brings a
new leaf is seen rather than silently dropped. Measured on 63,511 active
Tbilisi rows, 2026-10-02: 47 kept codes in division 47 (two of them
group-only, `47.2` and `47.79`), 2 in 56, 3 in 96, and 3 in 45.

**THE LABELS ARE GEOSTAT'S**, from each row's `Activity_2_Name` (English,
British spelling and the source's typos kept verbatim, as France keeps
INSEE's). The code rides along in EXTRA_COLUMNS so `classify()` matches on the
code, never on label text.

Catch-all share of the kept rows: 1,422 of 14,806 (9.6%; 47.19.0, 47.78.0,
47.59.9, 47.29.0, `47.2`), measured 2026-10-02 before division 45 joined.
"""

FIELD_LABEL = "Activity (NACE Rev. 2)"
VALUE_COLUMN = "activity_label"
EXTRA_COLUMNS = ("activity_code",)

_DIVISION_BUCKETS = {
    "45": "Retail",
    "47": "Retail",
    "56": "Food service",
    "96": "Personal services",
}

KEPT = {
    # --- Division 45: vehicle SALES only (R4: car dealers are Retail; repair
    # and wholesale stay out). The owner kept the precedent, 2026-10-02,
    # rather than France's disclosed exception.
    "45.11.2",  # Retail and retail sale of new and used vehicles (sic)
    "45.19.0",  # Sale of other motor vehicles
    "45.32.0",  # Retail trade of motor vehicle parts and accessories (NAICS 441310)
    # --- Division 47: Retail ---------------------------------------------
    "47.11.0", "47.19.0", "47.2", "47.21.0", "47.22.0", "47.23.0", "47.24.0",
    "47.25.0", "47.26.0", "47.29.0",
    # Fuel at a station (R4).
    "47.30.1", "47.30.2", "47.30.3", "47.30.9",
    "47.41.0", "47.42.0", "47.43.0",
    "47.51.0", "47.52.0", "47.53.0", "47.54.0",
    "47.59.1", "47.59.2", "47.59.3", "47.59.4", "47.59.9",
    "47.61.0", "47.62.0", "47.63.0", "47.64.0", "47.65.0",
    "47.71.0", "47.72.1", "47.72.2",
    # 47.73.1 is a veterinary PHARMACY (retail of veterinary medicines), not
    # a clinic, which would be 75.00.
    "47.73.1", "47.73.9", "47.74.0", "47.75.0", "47.76.1", "47.76.2",
    "47.77.0", "47.78.0",
    "47.79", "47.79.1", "47.79.2", "47.79.3", "47.79.4",
    # --- Division 56: Food service -----------------------------------------
    # 56.10.0 merges restaurants with mobile food service; the national leaf
    # does not split them, so it is kept whole.
    "56.10.0", "56.30.0",
    # --- Division 96: Personal services ------------------------------------
    "96.01.0", "96.02.0", "96.04.0",
}

OUT = {
    # Division 45: everything but sales (R4).
    "45.11.1": "wholesale and retail of vehicles - the wholesale half decides it (R4)",
    "45.11.3": "intermediation in vehicle trade - an agent, not a dealer (R4)",
    "45.20.0": "vehicle maintenance and repair (repairs are out)",
    "45.31.0": "wholesale of vehicle parts (R4)",
    "45.40.0": "motorcycle sale WITH maintenance and repair, one code (R4, repair)",
    # Market stalls (R1: a pitch, not a storefront).
    "47.81.0": "stalls and markets, food (R1)",
    "47.82.0": "stalls and markets, textiles and clothing (R1)",
    "47.89.0": "stalls and markets, other goods (R1)",
    # Nonstore retail.
    "47.91.1": "mail order or internet - no premises",
    "47.91.2": "internet auctions - no premises",
    "47.99.0": "other retail not in stores, stalls or markets - no premises",
    # Food with no counter of its own (R1).
    "56.2": "event catering and other food service, group only (R1)",
    "56.21.0": "event catering (R1)",
    "56.29.0": "contract catering and canteens (R1)",
    # Funeral (owner, 2026-09-28) and the personal-services catch-all (R2).
    "96.03.0": "funeral and related activities - off every map",
    "96.09": "other personal services n.e.c., group only (R2)",
    "96.09.1": "pet training (R2 catch-all)",
    "96.09.2": "pet boarding (R2 catch-all)",
    "96.09.4": "pet grooming and tattooing (R2 catch-all)",
    "96.09.9": "other personal care n.e.c. (R2 catch-all)",
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
    against the published classification (NAF's legend does the same)."""
    divisions = sorted(d for d, b in _DIVISION_BUCKETS.items() if b == bucket)
    if not divisions:
        return bucket
    return f"{bucket} - NACE {'/'.join(divisions)}"


_both = sorted(KEPT & set(OUT))
assert not _both, f"codes both kept and left out: {_both}"
_stray = sorted(c for c in KEPT | set(OUT) if c[:2] not in _DIVISION_BUCKETS)
assert not _stray, f"codes outside the tracked divisions: {_stray}"
_counts = {}
for _c in KEPT:
    _counts[_c[:2]] = _counts.get(_c[:2], 0) + 1
# Measured 2026-10-02 on the active Tbilisi rows.
assert _counts == {"45": 3, "47": 47, "56": 2, "96": 3}, f"kept-code counts drifted: {_counts}"
