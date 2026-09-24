"""Shared category buckets, plus the registry of per-taxonomy-system modules.

Every city's local business classification - NAICS, a city's own license-
category field, or (eventually) a non-US system like the EU's NACE - maps
INTO this same small set of buckets. The buckets are what the map's
legend/coloring/toggle logic actually uses; no taxonomy-specific code
(a NAICS prefix, a Chicago license_code) should leak past this layer into
app/pipeline code that isn't the taxonomy module itself.

This exists because criterion 3 of the city shortlist (docs/city_shortlist.md)
was originally "has NAICS + geocoding," and live verification found that
requirement too strict: New York, Chicago, and Philadelphia all have solid,
live, geocoded business-license data, just under their own local taxonomy
instead of NAICS. Rather than disqualify real cities over a naming
difference, each city's config names which taxonomy system its raw data
uses (`TAXONOMY_SYSTEM`), and the matching module here does the mapping
into buckets.
"""

# The default bucket set. A city's taxonomy module is not required to populate all three (a
# thin dataset might only support one or two), but should not invent a
# fourth without updating this list - the legend/coloring logic iterates
# over this fixed set.
CATEGORY_BUCKETS = [
    ("Retail", "#2a78d6"),
    # MAGENTA, NOT ORANGE, and it is the heat layer that forced it. Changed
    # 2026-09-21 together with map_common.HEAT_GRADIENT, because the two are
    # one decision: the old `#eb6834` sat **3.1 degrees of hue and Delta-E 9.5**
    # from the heat ramp's own midpoint, so a food-service pin was already
    # nearly the same colour as the wash it was drawn on - a live problem, not
    # a predicted one. Against the new burnt-orange ramp it would have been
    # Delta-E 10.7.
    #
    # `#C2185B` sits 48.2 degrees off the new ramp's midpoint and Delta-E 49.6
    # from its nearest stop: a 4.6x separation. The three buckets stay distinct
    # from each other (minimum pairwise Delta-E 84, down from 94 - Retail's
    # blue against this magenta), and it reads strongly on both basemaps
    # (83.8 light, 73.8 dark) since pin fills are NOT filtered in dark mode.
    ("Food service", "#C2185B"),
    ("Personal services", "#1baf7a"),
]

# Registered lazily (import the taxonomy module by name via this dict) so
# adding a new taxonomy - a new US city's own license field, or a future
# non-US system like NACE - never requires touching this file's imports.
# Each module must expose:
#   classify(row: dict) -> str | None
#       a bucket name from CATEGORY_BUCKETS, or None if the row doesn't map
#       to any tracked bucket (e.g. a license type this project doesn't
#       count as storefront commercial).
#   FIELD_LABEL: str
#       how the raw classification value is labelled in a map tooltip
#       (e.g. "NAICS code") - map code must never hardcode a taxonomy's name.
#   VALUE_COLUMN: str
#       the column in a city's businesses_clean.csv holding that raw value.
#   legend_label(bucket: str) -> str
#       the legend row text for a bucket (NAICS appends its prefixes,
#       e.g. "Retail - NAICS Code: 44/45"; a local taxonomy can just return
#       the bucket name).
TAXONOMY_MODULES = {
    "naics": "pipeline.taxonomies.naics",
    "chicago_license": "pipeline.taxonomies.chicago_license",
    "phl_licensetype": "pipeline.taxonomies.phl_licensetype",
    # New York dispatches over four registries rather than reading one
    # classification field - it is the first city whose coverage could not come
    # from a single source. `nyc_dca` (a skeleton, never used by a build) was
    # retired into it on 2026-09-21 when Step 0 showed the DCA licence file is
    # a regulated-activity list, not a business registry. See new_york.py.
    "new_york": "pipeline.taxonomies.new_york",
    # Boston: three registries dispatched on a `source` column, like New York.
    # Two buckets only - Massachusetts licenses cosmetology at state level and
    # publishes no address-bearing export, so Personal services has no source.
    "boston_licensecat": "pipeline.taxonomies.boston_licensecat",
    # Miami-Dade's Local Business Tax CATGRYNAME. Its file has a NAICS column
    # that is NULL on every row, so NAICS is unavailable despite being in the
    # schema - see miami_catgryname.py.
    "miami_catgryname": "pipeline.taxonomies.miami_catgryname",
    # Washington D.C.'s Basic Business License BUSINESSACTIVITY - the first
    # non-NAICS source here that covers all three buckets on its own, so unlike
    # New York's and Boston's it dispatches over no `source` column.
    "dc_businessactivity": "pipeline.taxonomies.dc_businessactivity",
    "vancouver": "pipeline.taxonomies.vancouver",
    "calgary_licencetype": "pipeline.taxonomies.calgary_licencetype",
    "edmonton_licencecategory": "pipeline.taxonomies.edmonton_licencecategory",
    # Toronto's MLS Category. The only Canadian register with no general-retail
    # licence, so its Retail bucket is the REGULATED slice alone (4.2% of its
    # storefronts) - New York's and Boston's shape rather than Calgary's.
    "toronto_mlscategory": "pipeline.taxonomies.toronto_mlscategory",
    "scian": "pipeline.taxonomies.scian",
    "madrid_epigrafe": "pipeline.taxonomies.madrid_epigrafe",
    # Barcelona's four-level Catalan scheme, keyed on its FINEST level -
    # the opposite of Madrid, and for a measured reason: the group level dumps
    # 35% of the city into `Altres` and buries 720 hotels inside its
    # restaurants group. It also dispatches `Altres` on two further columns,
    # because that value means five different things depending on its parent.
    "barcelona_activitat": "pipeline.taxonomies.barcelona_activitat",
    "dublin_uses": "pipeline.taxonomies.dublin_uses",
    "milan_source": "pipeline.taxonomies.milan_source",
    # NAF rev. 2 - the FIRST taxonomy here that is NATIONAL rather than a
    # city's own. SIRENE is one register for the whole country, so five French
    # cities (france.py's BUILD_SEQUENCE) share this module and a correction
    # reaches all of them. Keyed at the sous-classe, Barcelona's shape: the
    # groupe level puts 49.4% of Paris in "other" against 19.3% at level 5.
    "france_naf": "pipeline.taxonomies.france_naf",
    "norway_sn2025": "pipeline.taxonomies.norway_sn2025",
    "denmark_db25": "pipeline.taxonomies.denmark_db25",
    "czech_nace2025": "pipeline.taxonomies.czech_nace2025",
    # IBGE's CNEFE 2022 - the first FREE-TEXT taxonomy: no code list, so
    # ordered keyword rules on the enumerator's description, lifted unchanged
    # from staging's scripts/screen_cnefe.py. National, like france_naf.
    "brazil_cnefe": "pipeline.taxonomies.brazil_cnefe",
    # Future, non-US: "nace": "pipeline.taxonomies.nace"
}


def load_taxonomy_module(system: str):
    """Import and return the taxonomy module for a registered system name
    (the same string a city's registry.yaml entry names under
    `taxonomy.system`)."""
    import importlib

    if system not in TAXONOMY_MODULES:
        raise ValueError(
            f"Unknown taxonomy system {system!r}. Registered: "
            f"{sorted(TAXONOMY_MODULES)}. Add a module to "
            "pipeline/taxonomies/ and register it in TAXONOMY_MODULES "
            "before using it in a city's registry entry."
        )
    return importlib.import_module(TAXONOMY_MODULES[system])


def filter_to_storefront(df, system: str):
    """Keep only rows the city's taxonomy maps to a tracked storefront
    bucket (classify() is not None). Step 2 of every city uses this instead
    of filtering on NAICS prefixes directly, so a local-taxonomy city (New
    York, Chicago, Philadelphia) needs no change to its step 2 logic.

    df must already carry the taxonomy's VALUE_COLUMN - a city's step 2
    renames its raw classification column to that name right after loading.
    """
    module = load_taxonomy_module(system)
    col = module.VALUE_COLUMN
    if col not in df.columns:
        raise KeyError(
            f"{system!r} taxonomy expects a {col!r} column; got {list(df.columns)[:8]}... "
            "Rename the city's raw classification column to it before filtering."
        )
    # A taxonomy whose classify() needs more than one field (Chicago's catch-all
    # license types are classified by business_activity) lists the extra columns
    # in EXTRA_COLUMNS; single-column taxonomies (NAICS) don't define it.
    cols = [col, *getattr(module, "EXTRA_COLUMNS", ())]
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"{system!r} taxonomy also needs column(s) {missing}; got {list(df.columns)[:8]}...")
    keep = [module.classify(dict(zip(cols, values))) is not None for values in zip(*(df[c] for c in cols))]
    return df[keep]
