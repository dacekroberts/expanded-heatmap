"""NAICS taxonomy - the mapping used by every city whose open-data export
carries a NAICS field (San Diego, San Francisco and Los Angeles so far;
Chicago uses its own licence taxonomy instead).

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

# Prefixes carved back OUT of the groups above, for every city, because they are
# not storefronts by their own definition - not a privacy carve-out but a
# correction to what "storefront commercial density" means. A broad prefix match
# is what swept them in. Decided 2026-09-21; see DECISIONS.md and
# docs/excluded_categories.md.
#
#   454    Nonstore retailers - electronic shopping, mail-order, direct selling,
#          vending-machine operators, fuel dealers. NAICS itself calls these
#          "nonstore", yet the "45" prefix pulled them into Retail. They were
#          10.1% of Los Angeles's pins, 9.0% of San Diego's, 1.7% of San
#          Francisco's, and 454390 (direct selling) was the largest remaining
#          group of mapped personal names at residential addresses.
#   81293  Parking lots and garages. A parking trip is planned, not incidental
#          foot traffic from a station, so it sits outside this project's
#          question. (Excluded on the same reasoning in a sibling project.)
#          Low privacy signal (~4% residential) - this one is about scope.
#
# A prefix here always wins over NAICS_GROUPS, so "454" beats "45" and "81293"
# beats "812". Anything added here changes every NAICS city's counts: re-run the
# pipelines, the drift check and scripts/check_personal_exposure.py.
NAICS_EXCLUDE_PREFIXES = ("454", "81293")

# Individual 6-digit NAICS codes worth hand-sampling per city before trusting
# the prefix filter alone. Each is a national NAICS catch-all (it sweeps a
# large, undifferentiated bucket into its prefix), so the *need to check* is
# national even though the *verdict* varies by city:
#
#   812930  Parking Lots and Garages
#     RESOLVED 2026-09-21: excluded for every city, via the 81293 prefix in
#     NAICS_EXCLUDE_PREFIXES above. A parking trip is planned rather than
#     incidental station foot traffic, which puts it outside this project's
#     question; a sibling project excluded it on the same reasoning. It was
#     888 mapped pins in Los Angeles, 637 in San Francisco, 104 in San Diego.
#     This was a scope call, not a privacy one (~4% residential).
#   812990  All Other Personal Services
#     A prior single-city hand-sample (Seattle, 40 rows) found ~90%
#     non-storefront (home-based sole proprietors, professional offices,
#     services that travel to the customer) and excluded it. Re-sample per
#     city: the real profile depends on local registration patterns.
#     VERDICT SO FAR - Los Angeles: EXCLUDED (2026-09-21). Sampled against
#     the rendered map, not a row list: 812990 supplied 2,255 of the ~4,100
#     mapped pins whose displayed name looked like an individual's, and 37%
#     of those had an APT/UNIT/STE/# in the street address. Excluded on two
#     grounds - mostly not a storefront, and a personal-name/home-address
#     exposure on a public map. Set in that city's NAICS_EXCLUDE_CODES.
#     San Francisco: EXCLUDED (2026-09-21). Its own licence data labels this
#     code "SOLO MASSAGE ESTABLISHMENT" rather than the generic name: 414
#     mapped pins, 31 (7%) with a person-like name at a residential address -
#     the highest residential share of any category there, and a sensitive one
#     (a sole operator working from home). Set in that city's
#     NAICS_EXCLUDE_CODES.
#     San Diego: still included, and its residual is small but NOT measurable
#     the same way - its address_suite holds bare values ("A", "101") with no
#     APT/STE token, so address text cannot flag a residence there. Its better
#     signal is ownership_type: of 3,117 mapped rows, 1,298 are SOLE
#     proprietorships and 903 (29%) display a name identical to the owner's.
#     That is a dba the owner chose to register under their own name - a
#     deliberate public commercial act - not a fallback the pipeline
#     substituted, so it was left in. Revisit if a better residence signal
#     appears. (Its codes are variable length: match the 81299 prefix there,
#     not the 6-digit code.)
#   459999  All Other Miscellaneous Retailers
#     The same prior hand-sample (25 rows) found ~70% plausible walk-in
#     storefronts (niche independent shops without their own code) and kept
#     it. Also worth re-sampling per city.
#
# Verdicts so far are recorded per code above. When a city is sampled, record
# the sample size and reasoning in DECISIONS.md, add the code to that city's
# NAICS_EXCLUDE_CODES in its own config.py (applied as a printed filter in its
# step 2), and list it in docs/excluded_categories.md. Use
# NAICS_EXCLUDE_PREFIXES above only for exclusions that hold for every city.
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
    storefront category (including the non-storefront prefixes carved out by
    NAICS_EXCLUDE_PREFIXES, which win over NAICS_GROUPS)."""
    code = str(code)
    if code.startswith(NAICS_EXCLUDE_PREFIXES):
        return None
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
