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

STATUS: only the handful of values actually seen in the live sample-row
check are mapped below - a starting skeleton, not a verified mapping.
Chicago publishes a full license-code reference table; pull it (or a
`SELECT DISTINCT license_description` against the resource endpoint)
before running this against real data.
"""

# license_description (exact string, uppercased) -> bucket name from
# pipeline.taxonomies.CATEGORY_BUCKETS. Only the one confirmed live
# sample value is listed; it's also a poor example (a pharmaceutical
# rep is not storefront-commercial the way this project defines it) -
# left in deliberately unmapped (None) as a reminder that Chicago's real
# license-code table needs to be pulled and reviewed for which codes
# actually mean walk-in storefronts before this taxonomy is usable.
LICENSE_DESCRIPTION_TO_BUCKET = {
    # "Pharmaceutical Representative" - confirmed live sample value, but
    # not a storefront category. Left unmapped on purpose.
    "PHARMACEUTICAL REPRESENTATIVE": None,
}


FIELD_LABEL = "License"
VALUE_COLUMN = "license_description"


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` must carry a `license_description` key."""
    description = (row.get("license_description") or "").strip().upper()
    if not description:
        return None
    return LICENSE_DESCRIPTION_TO_BUCKET.get(description)
