"""Detecting a business that is really someone's home, shared across cities.

Why this module exists: the residence test in
`scripts/check_personal_exposure.py` can only fire on an `APT`/`FL`/`RM`/`#`
indicator in the address text, so it cannot see a sole trader at a detached
house. Measured against city property registers on 2026-09-21, that blind spot
was three orders of magnitude wide in the NAICS cities:

    Chicago         0 pins   (home occupations already excluded by taxonomy)
    New York       10 pins   (0.02%)
    Philadelphia    8 pins   (filtered)
    San Francisco 217 pins   (1.19%)
    Los Angeles  ~1,000-2,000 pins
    San Diego     unmeasured, and the only city with no signal at all

The pattern is always the same - a person's name displayed at a parcel the
city's own assessor calls residential and which the owner occupies - so the
logic lives here and each city supplies its own columns.

**The lesson that cost the most to learn: land use alone is not a signal.** In a
dense city, shops sit inside residential buildings. "Residential parcel" flags
7.95% of Philadelphia's pins, including 147 thirty-plus-seat restaurants on
`APARTMENTS > 4 UNITS` parcels; New York's single largest category under its
pins is `Mixed Residential & Commercial` at 20,257; San Francisco's is
`Multi-Family Residential` at 5,733. Acting on land use alone would delete
hundreds of real storefronts. So a city's residential set must contain only
*purely* residential categories - never mixed use, never apartment blocks - and
the flag must pair it with a name or entity test.

Treat what this finds as a SCOPE question first: a food or beauty business run
from the owner's house is not a storefront, which is easier to justify than a
privacy carve-out and fixes both.
"""

import re

# Tokens that make a name read as an organisation rather than a person. Kept
# broad on purpose: a false "organisation" only makes the flag conservative,
# and a conservative flag deletes fewer real businesses.
_ORG = re.compile(
    r"\b(INC|LLC|L\.?L\.?C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PC|PLC|GROUP|"
    r"ENTERPRISE|ENTERPRISES|HOLDING|HOLDINGS|SERVICES|SERVICE|SALON|SHOP|STORE|"
    r"MARKET|CAFE|RESTAURANT|BAR|GRILL|PIZZA|LIQUOR|CLEANERS|CLEANER|BARBER|NAIL|"
    r"NAILS|SPA|STUDIO|BOUTIQUE|DELI|BAKERY|FOOD|FOODS|MART|CENTER|CENTRE|TRUST|"
    r"ASSOCIATION|ASSOC|PARTNERS|PARTNERSHIP|VENTURES|VENTURE|BROS|BROTHERS|THE|AND|"
    r"OF|DBA|USA|INTERNATIONAL|MANAGEMENT|PROPERTIES|REALTY|CONSTRUCTION|DESIGN|"
    r"SOLUTIONS|SYSTEMS|TECHNOLOGIES|CONSULTING|MEDICAL|DENTAL|CLINIC|CHURCH|SCHOOL|"
    r"ACADEMY|FOUNDATION|INSTITUTE|SUPPLY|WHOLESALE|RETAIL|AUTO|MOTORS|REPAIR|"
    r"PLUMBING|ELECTRIC|TRUCKING|TRANSPORT|LOGISTICS|BEAUTY|HAIR|SKIN|MASSAGE|"
    r"TATTOO|LAUNDRY|PET|DOG|KIDS|HOUSE|HOME|CITY|CLUB|LOUNGE|GIFTS)\b")
# Punctuation and digits that a personal name does not contain. NOTE this also
# rejects the surname-first form ("Smith, John"), which registries do use -
# scripts/check_personal_exposure.py reports that separately for exactly this
# reason. Kept here so the flag stays conservative.
_NOT_A_NAME = re.compile(r"[&/,\d\.]")
_PERSON = re.compile(
    r"^[A-Z][A-Za-z'\-]{1,}(?:\s+[A-Z])?\s+[A-Z][A-Za-z'\-]{1,}$")


def looks_personal(name) -> bool:
    """Does this displayed name read as an individual's own name?

    Two or three tokens, no organisation word, no digits or punctuation. The
    organisation guard is not optional: without it "STARBUCKS CORPORATION" is
    two alphabetic words and matches the shape test.
    """
    s = str(name or "").strip()
    if not s:
        return False
    return (bool(_PERSON.match(s))
            and not _ORG.search(s.upper())
            and not _NOT_A_NAME.search(s.upper()))


def flag_home_based(names, *, residential, owner_occupied=None,
                    individual=None):
    """Rows that are a person's name at what the city says is a home.

    names:          Series of displayed business names.
    residential:    boolean Series - the parcel is PURELY residential by the
                    city's own classification (never mixed use, never
                    apartments; see the module docstring).
    owner_occupied: optional boolean Series - a homestead or homeowner's
                    exemption is claimed, i.e. the owner lives there. Where a
                    city publishes this, it is the strongest single signal,
                    but it over-fires alone (Philadelphia: 162 of its 189 hits
                    were mixed-use rowhouses whose owner lives above the shop).
    individual:     optional boolean Series - the registry itself records the
                    licensee as an individual rather than a company.

    All supplied conditions are required together. Returns a boolean Series.
    """
    mask = names.map(looks_personal) & residential.fillna(False)
    if owner_occupied is not None:
        mask &= owner_occupied.fillna(False)
    if individual is not None:
        mask &= individual.fillna(False)
    return mask


def report(label, mask, total, extra=None):
    """One printed line per city, in the same shape everywhere, so the numbers
    are comparable across step 2 outputs and against DECISIONS.md."""
    n = int(mask.sum())
    print(f"Residence filter ({label}): {total:,} -> {total - n:,} rows "
          f"({n:,} removed, {100 * n / total:.2f}%)")
    if n and extra is not None:
        for name, series in extra.items():
            print(f"  by {name}: "
                  f"{series[mask].value_counts(dropna=False).head(6).to_dict()}")
