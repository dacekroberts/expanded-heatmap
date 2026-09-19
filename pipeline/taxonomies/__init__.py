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
    ("Food service", "#eb6834"),
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
    "nyc_dca": "pipeline.taxonomies.nyc_dca",
    "chicago_license": "pipeline.taxonomies.chicago_license",
    "phl_licensetype": "pipeline.taxonomies.phl_licensetype",
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
    keep = df[col].map(lambda v: module.classify({col: v}) is not None)
    return df[keep]
