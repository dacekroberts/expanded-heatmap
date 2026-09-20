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

Only 55 license_description values are active in the city (2026-09-20), and
the 24 largest cover 98% of active rows, so every value seen in that pull is
either mapped below or deliberately left unmapped (= excluded). A description
that first appears in a later pull is excluded until it is added here.

Some license types name the business (Tavern, Package Goods); others say
nothing about it (Limited / Regulated Business License) or cover very
different businesses (Retail Food Establishment, Animal Care License), and are
classified by business_activity. A site can hold several licenses, so step 2
keeps one per site (LICENSE_PRIORITY in pipeline/chicago/config.py).
"""

# license_description (uppercased) -> bucket name from
# pipeline.taxonomies.CATEGORY_BUCKETS, for license types that identify the
# business on their own. Anything absent is excluded: adjunct licenses that
# attach to a business already counted (Consumption on Premises, Outdoor
# Patio, Late Hour, Music and Dance), vehicle repair (Motor Vehicle
# Services), parking (Commercial Garage), temporary or mobile trading
# (Pop-Up, Mobile Food, Special Event, Peddler), catering and shared kitchens,
# pawnbrokers, amusements, child care, manufacturing, wholesale, and the rest
# of the long tail that isn't a walk-in storefront of the three categories.
LICENSE_DESCRIPTION_TO_BUCKET = {
    "TAVERN": "Food service",
    "PACKAGE GOODS": "Retail",         # liquor stores
    "FILLING STATION": "Retail",       # gas stations
    "SECONDHAND DEALER": "Retail",
    "TOBACCO": "Retail",               # counts only where a site has no primary license (step 2)
}

# License types classified by business_activity instead.
CATCH_ALL_DESCRIPTIONS = {"LIMITED BUSINESS LICENSE", "REGULATED BUSINESS LICENSE"}
FOOD_ESTABLISHMENT = "RETAIL FOOD ESTABLISHMENT"
ANIMAL_CARE = "ANIMAL CARE LICENSE"

# business_activity matching. An activity value can list several activities
# joined by " | "; for the catch-alls the first one that matches a bucket
# decides. Matched as substrings of the uppercased activity. Buckets follow
# what the NAICS taxonomy counts (44/45 retail, 722 food service, 812
# personal services), so cities stay comparable; gyms and fitness classes
# (NAICS 713940 and 611620) and the Administrative / Financial / Consulting /
# Tax / Wholesale / Staffing / Travel / Shipping / Car wash / Hotel /
# Hazardous / "Miscellaneous Commercial Services" activities match nothing
# here and so are excluded.
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

# Retail Food Establishment: preparing or serving food makes it Food service,
# even when the same license also lists retail food sales (a grocery with a
# deli, ~8% of these licenses); otherwise retail food sales make it Retail.
FOOD_SERVICE_ACTIVITIES = (
    "PREPARATION OF FOOD", "PREPARATION AND SALE OF COFFEE",
    "SALE OF FOOD PREPARED ONSITE", "EXPEDITED RESTAURANT",
)
# Animal Care License: grooming is a personal service, retail sales are retail;
# veterinary hospitals, boarding, day care and shelters are excluded.
ANIMAL_GROOMING_ACTIVITIES = ("ANIMAL GROOMING",)

FIELD_LABEL = "License"
VALUE_COLUMN = "license_description"
# filter_to_storefront() passes these to classify() as well as VALUE_COLUMN.
EXTRA_COLUMNS = ("business_activity",)


def legend_label(bucket: str) -> str:
    return bucket


def _parts(activity: str):
    """The activity's parts, uppercased, without blanks or home-based ones."""
    parts = (p.strip().upper() for p in activity.split("|"))
    return [p for p in parts if p and HOME_BASED_MARKER not in p]


def _has(parts, patterns):
    return any(pat in part for part in parts for pat in patterns)


def _first_match(activity: str):
    for part in _parts(activity):
        if _has([part], PERSONAL_SERVICE_ACTIVITIES):
            return "Personal services"
        if _has([part], RETAIL_ACTIVITIES):
            return "Retail"
    return None


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` carries `license_description` and, for the license types classified
    by activity, `business_activity`. Such a row with no activity is
    unclassifiable and excluded."""
    description = (row.get("license_description") or "").strip().upper()
    if not description:
        return None
    if description in LICENSE_DESCRIPTION_TO_BUCKET:
        return LICENSE_DESCRIPTION_TO_BUCKET[description]
    activity = row.get("business_activity")
    if not isinstance(activity, str):
        return None
    if description in CATCH_ALL_DESCRIPTIONS:
        return _first_match(activity)
    if description == FOOD_ESTABLISHMENT:
        parts = _parts(activity)
        if _has(parts, FOOD_SERVICE_ACTIVITIES):
            return "Food service"
        return "Retail" if _has(parts, RETAIL_ACTIVITIES) else None
    if description == ANIMAL_CARE:
        parts = _parts(activity)
        if _has(parts, ANIMAL_GROOMING_ACTIVITIES):
            return "Personal services"
        return "Retail" if _has(parts, RETAIL_ACTIVITIES) else None
    return None
