"""Philadelphia taxonomy - the `licensetype` field from L&I's business
license data, not NAICS.

Philadelphia's live-verified business-license source is "Licenses and
Inspections Business Licenses" (Carto SQL API, phl.carto.com, table
business_licenses) - full address and geometry (`the_geom`,
`geocode_x`/`geocode_y`) confirmed populated, but no NAICS field anywhere
in the 47-column schema. The real classification field is `licensetype`
(e.g. "Rental", "Food Preparing and Serving", "Vacant Residential
Property / Lot"). See docs/city_shortlist.md and docs/project_context.md
("Taxonomy plurality").

STATUS: only the handful of values actually seen in the live sample-row
check are mapped below - a starting skeleton, not a verified mapping.
Pull the full distinct-value list (`SELECT DISTINCT licensetype FROM
business_licenses` against the Carto SQL API) before running this
against real data.
"""

# licensetype (exact string, uppercased) -> bucket name from
# pipeline.taxonomies.CATEGORY_BUCKETS. Only entries actually confirmed
# live are listed.
LICENSETYPE_TO_BUCKET = {
    "FOOD PREPARING AND SERVING": "Food service",
    # Confirmed live sample values that are NOT storefront-commercial for
    # this project's purposes - explicitly excluded rather than left to
    # silently fall through, so a future reader can tell "checked, not a
    # match" from "not yet checked."
    "RENTAL": None,
    "VACANT RESIDENTIAL PROPERTY / LOT": None,
}


FIELD_LABEL = "License type"
VALUE_COLUMN = "licensetype"


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` must carry a `licensetype` key."""
    license_type = (row.get("licensetype") or "").strip().upper()
    if not license_type:
        return None
    return LICENSETYPE_TO_BUCKET.get(license_type)
