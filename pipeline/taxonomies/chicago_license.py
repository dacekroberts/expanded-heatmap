"""Chicago taxonomy - the city's own license-code/business-activity fields,
not NAICS.

Chicago's live-verified business-license source is "Business Licenses"
(Socrata data.cityofchicago.org, id r5kz-chrr) - full address and lat/long
confirmed populated, but a catalog-wide search for "NAICS" on that portal
returned zero results. The real classification fields are
`license_code`/`license_description` (e.g. "7009 / Pharmaceutical
Representative") and `business_activity_id`/`business_activity` (e.g.
"990 / Markets/Promotes Pharmaceuticals..."). See docs/city_shortlist.md
and docs/project_context.md ("Taxonomy plurality").

STATUS (2026-09-19): only the two catch-all license types are classified,
and they are the largest active groups (about 39% of active licenses).
"Limited Business License" and "Regulated Business License" say nothing
about what the business does, so they are classified by `business_activity`
(see classify()). The other ~148 license_description values are NOT yet
mapped, so this taxonomy is incomplete: pull the full distinct list and add
them to LICENSE_DESCRIPTION_TO_BUCKET before running it against real data.
"""

# license_description (exact string, uppercased) -> bucket name from
# pipeline.taxonomies.CATEGORY_BUCKETS, for license types that identify the
# business on their own (Retail Food Establishment, Tavern, ...). Still to do.
LICENSE_DESCRIPTION_TO_BUCKET = {}

# License types that don't identify the business: classified by activity.
CATCH_ALL_DESCRIPTIONS = {"LIMITED BUSINESS LICENSE", "REGULATED BUSINESS LICENSE"}

# business_activity matching. An activity value can list several activities
# joined by " | "; the first one that matches a bucket decides. Matched as
# substrings of the uppercased activity. Personal services are tested first
# only so that "Hair Services | Retail Sales of ..." reads as its first part.
# Buckets follow what the NAICS taxonomy counts (44/45 retail, 812 personal
# services), so cities stay comparable; gyms and fitness classes (NAICS 713940
# and 611620) and the Administrative / Financial / Consulting / Tax / Wholesale
# / Staffing / Travel / Shipping / Car wash / Hotel / Hazardous / "Miscellaneous
# Commercial Services" activities match nothing here and so are excluded.
PERSONAL_SERVICE_ACTIVITIES = (
    "HAIR SERVICES", "HAIR, NAIL", "NAIL SERVICES", "SKINCARE SERVICES",
    "SKIN CARE", "WAXING", "MASSAGE", "TATTOO", "LAUNDROMAT",
    "DRY CLEANING - DROP OFF", "CLOTHING ALTERATIONS",
    "MISCELLANEOUS PERSONAL SERVICES",
)
RETAIL_ACTIVITIES = (
    "RETAIL SALE",                      # "Retail Sales of ...", "Retail Sale of ..."
    "SALE OF FURNITURE", "SALE OF ART", "SALE OF VEHICLE PARTS",
    "SALES / CAR RENTAL", "SALES / RENTAL / LEASE OF MOTORIZED",   # vehicle sales
)
HOME_BASED_MARKER = "(HOME BASED"       # a home business is not a storefront

FIELD_LABEL = "License"
VALUE_COLUMN = "license_description"
# filter_to_storefront() passes these to classify() as well as VALUE_COLUMN.
EXTRA_COLUMNS = ("business_activity",)


def legend_label(bucket: str) -> str:
    return bucket


def _classify_activity(activity: str):
    for part in activity.split("|"):
        part = part.strip().upper()
        if not part or HOME_BASED_MARKER in part:
            continue
        if any(p in part for p in PERSONAL_SERVICE_ACTIVITIES):
            return "Personal services"
        if any(p in part for p in RETAIL_ACTIVITIES):
            return "Retail"
    return None


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` carries `license_description` and, for the catch-all license types,
    `business_activity`. A catch-all row with no activity is unclassifiable
    and excluded."""
    description = (row.get("license_description") or "").strip().upper()
    if not description:
        return None
    if description in CATCH_ALL_DESCRIPTIONS:
        return _classify_activity(row.get("business_activity") or "")
    return LICENSE_DESCRIPTION_TO_BUCKET.get(description)
