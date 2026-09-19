"""NAICS taxonomy - the mapping used by every city whose open-data export
carries a NAICS field (San Diego and San Francisco so far; Los Angeles is
next).

What is national and reusable: NAICS_GROUPS below - which broad NAICS
prefixes count as storefront commercial, and which shared bucket each feeds.
That is a category-definition choice, not something tied to one city's data.

What is NOT settled here: which specific 6-digit catch-all codes to exclude
or keep (see NAICS_CATCHALL_CODES_TO_CHECK). Those verdicts depend on a
city's actual registrants and must be hand-sampled per city.

Per-group top-code subcategories (e.g. "Clothing & accessories" as retail's
biggest code) are deliberately not defined here: a top-codes-by-count list
is derived from one city's data, not a national ranking, so compute it per
city from that city's cleaned data if it's ever wanted.
"""

# The broad groups used for classification, map colouring and the legend.
# Prefix match on the code as a string, so "44" catches 441, 4411, 44111.
# Widening this changes results materially - it is one of the most
# consequential analyst choices in this kind of project; record any change
# in DECISIONS.md. Candidates worth a sensitivity check: "71" Arts,
# entertainment, recreation; "721" Accommodation; "621" Ambulatory health
# care (clinics, dentists).
#
# Each entry is (bucket name from pipeline.taxonomies.CATEGORY_BUCKETS,
# NAICS prefixes feeding it).
NAICS_GROUPS = [
    ("Retail", ("44", "45")),
    ("Food service", ("722",)),
    ("Personal services", ("812",)),
]

# Individual 6-digit NAICS codes worth hand-sampling per city before trusting
# the prefix filter alone. Each is a national NAICS catch-all (it sweeps a
# large, undifferentiated bucket into its prefix), so the *need to check* is
# national even though the *verdict* varies by city:
#
#   812930  Parking Lots and Garages
#     A planned trip decision, not incidental foot traffic - likely to be
#     excluded everywhere, but unverified for the cities built so far.
#   812990  All Other Personal Services
#     A prior single-city hand-sample (Seattle, 40 rows) found ~90%
#     non-storefront (home-based sole proprietors, professional offices,
#     services that travel to the customer) and excluded it. Re-sample per
#     city: the real profile depends on local registration patterns.
#   459999  All Other Miscellaneous Retailers
#     The same prior hand-sample (25 rows) found ~70% plausible walk-in
#     storefronts (niche independent shops without their own code) and kept
#     it. Also worth re-sampling per city.
#
# Neither built city has been hand-sampled yet (see PLAN.md). When a city is
# sampled, record the verdict and sample size in DECISIONS.md and add
#   NAICS_STOREFRONT_EXCLUDE = {code: (label, reasoning + sample size)}
# here, applied in that city's step 2.
NAICS_CATCHALL_CODES_TO_CHECK = {
    "812930": "Parking Lots and Garages",
    "812990": "All Other Personal Services",
    "459999": "All Other Miscellaneous Retailers",
}

FIELD_LABEL = "NAICS code"
VALUE_COLUMN = "naics"


def naics_label(name: str, prefixes: tuple) -> str:
    return f"{name} — NAICS Code: {'/'.join(prefixes)}"


def legend_label(bucket: str) -> str:
    """Taxonomy-module interface: legend text for a bucket."""
    for name, prefixes in NAICS_GROUPS:
        if name == bucket:
            return naics_label(name, prefixes)
    return bucket


def naics_group(code: str):
    """A NAICS code -> its bucket name, or None if it's not a tracked
    storefront category."""
    code = str(code)
    for name, prefixes in NAICS_GROUPS:
        if code.startswith(prefixes):
            return name
    return None


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` must carry a `naics` key with the raw code string."""
    code = row.get("naics")
    if not code:
        return None
    return naics_group(code)
