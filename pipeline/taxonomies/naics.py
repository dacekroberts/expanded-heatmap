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
#   8122   Death care services - 812210 funeral homes and funeral services,
#          812220 cemeteries and crematories. Funeral services off every map
#          (owner, 2026-09-28): not storefronts. Shops selling funeral goods
#          are retail (45) and stay.
#   72231  Food service contractors  \  Food with no counter of its own
#   72232  Caterers                   > (owner, 2026-09-29): an institutional
#   72233  Mobile food services      /  or contract canteen, an event caterer
#          and a food truck serve no walk-in public at a premises of their
#          own. Five-digit prefixes, so San Diego's variable-length codes
#          (72231, 72232, 72233) are caught with the six-digit ones. The
#          undifferentiated 7223 / 72230 / 722300 ("special food services",
#          3,392 rows in Los Angeles) is NOT excluded: it mixes all three
#          with real counters, and the code alone cannot tell them apart.
#          ONE PER-CITY EXEMPTION: Montréal keeps 722320 (owner,
#          2026-09-29) - its street survey's caterers are traiteur shops, as
#          France's 56.21Z. See naics_montreal.py; every other NAICS city
#          excludes caterers.
#   81299  All other personal services - the "other personal services"
#          catch-all (owner, 2026-09-29), excluded for every city. It was a
#          per-city verdict before (Los Angeles and San Francisco excluded
#          812990 in their own configs; San Diego's 81299 and Montreal's
#          812990 were still mapped). The four-digit 8129 is NOT this code:
#          it is the whole industry group (pet care, photofinishing too).
#   812193 San Diego's own "MASSAGE PARLORS" - adult and hostess venues off
#          every map (owner, 2026-09-29). Not a national NAICS code (NAICS
#          has 812191 and 812199 only); San Diego's registry extends 81219
#          locally, and keeps 812198 MASSAGE THERAPY and 812194 MASSAGE
#          TECHNICIAN as their own codes, which stay.
#   445132 Vending machine operators \  NAICS 2022 moved 454's vending and
#   457210 Fuel dealers               / fuel-dealer codes INTO the retail
#          prefixes, so the "454" carve-out missed them (Los Angeles and San
#          Francisco's registries use both editions). Nonstore, out (owner,
#          2026-09-29, DECISIONS "Category check: the owner's calls"). Their
#          neighbours 445131 convenience retailers and 457110/457120 gasoline
#          stations stay.
#
# A prefix here always wins over NAICS_GROUPS, so "454" beats "45" and "81293"
# beats "812". Anything added here changes every NAICS city's counts: re-run the
# pipelines, the drift check and scripts/check_personal_exposure.py.
NAICS_EXCLUDE_PREFIXES = ("454", "81293", "8122",
                          "72231", "72232", "72233",   # (owner, 2026-09-29) R1
                          "81299",                     # (owner, 2026-09-29) R2
                          "812193",                    # (owner, 2026-09-29) R3
                          "445132", "457210")          # (owner, 2026-09-29) NAICS 2022 nonstore

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
#     RESOLVED 2026-09-29: excluded for every city, via the 81299 prefix in
#     NAICS_EXCLUDE_PREFIXES above (owner, "other personal services"
#     catch-all). The per-city history below is kept as the reasoning trail.
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


# The 2026-09-29 carve-outs (owner), each checked against its near misses: a
# prefix one digit short would take a real counter or a kept code with it.
for _c, _want in [("722310", None), ("72231", None), ("722320", None), ("72232", None),
                  ("722330", None), ("72233", None),
                  ("722300", "Food service"), ("7223", "Food service"),
                  ("72230", "Food service"), ("72234", "Food service"),
                  ("722511", "Food service"), ("722410", "Food service"),
                  ("812990", None), ("81299", None), ("812999", None),
                  ("8129", "Personal services"), ("812910", "Personal services"),
                  ("812193", None), ("812198", "Personal services"),
                  ("812194", "Personal services"), ("812199", "Personal services"),
                  ("812196", "Personal services"),
                  ("445132", None), ("445131", "Retail"), ("457210", None),
                  ("457110", "Retail"), ("457120", "Retail")]:
    assert naics_group(_c) == _want, (_c, naics_group(_c), _want)
