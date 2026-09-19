"""New York City taxonomy - DCA's own license-category field, not NAICS.

NYC's live-verified business-license source is DCA's "Issued Licenses"
dataset (Socrata data.cityofnewyork.us, id w7w3-xahh) - full address and
lat/long confirmed populated, but no NAICS field anywhere in the schema.
The real classification fields are `business_category` (fine-grained,
e.g. "Secondhand Dealer - General") and `license_type` (coarser, e.g.
"Premises"). See docs/city_shortlist.md, "Pass, with a real caveat"
originally, reclassified PASS once NAICS stopped being mandatory
(docs/project_context.md, "Taxonomy plurality").

STATUS: only the handful of category values actually seen in the live
sample-row check are mapped below. This is a starting skeleton, not a
verified full mapping - pull the full distinct-value list of
`business_category` (a `SELECT DISTINCT business_category` against the
Socrata resource endpoint) before running this against real data, the
same way NAICS_CATCHALL_CODES_TO_CHECK in naics.py exists precisely so a
prefix-level guess doesn't get treated as a checked fact.
"""

# business_category (exact string, uppercased for matching) -> bucket
# name from pipeline.taxonomies.CATEGORY_BUCKETS. Only entries actually
# confirmed live are listed; everything else falls through to None
# (unclassified) until the full distinct-value list is pulled and this
# table is filled in properly.
BUSINESS_CATEGORY_TO_BUCKET = {
    # Confirmed live sample value, but "Secondhand Dealer - General" is
    # itself ambiguous (could be a walk-in storefront or a wholesale
    # operation) - needs a hand sample before trusting the bucket below,
    # same caution NAICS catch-all codes get (see naics.py).
    "SECONDHAND DEALER - GENERAL": "Retail",
}


FIELD_LABEL = "Business category"
VALUE_COLUMN = "business_category"


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` must carry a `business_category` key."""
    category = (row.get("business_category") or "").strip().upper()
    if not category:
        return None
    return BUSINESS_CATEGORY_TO_BUCKET.get(category)
