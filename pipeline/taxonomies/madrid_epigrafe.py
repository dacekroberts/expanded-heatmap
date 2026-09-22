"""Madrid taxonomy - the city's own desc_epigrafe field, not NAICS.

Scaffolded by scripts/scaffold_city.py as a SKELETON: nothing is mapped yet.
Before building the city, pull the full distinct-value list of
`desc_epigrafe` (with counts, restricted to the rows step 2 will keep), map
each value to one of the buckets in pipeline.taxonomies.CATEGORY_BUCKETS, and
hand-sample any catch-all values (see chicago_license.py for the worked
example, including classifying some values by a second field).

Values not listed are excluded (classify() returns None).
"""

# desc_epigrafe (uppercased) -> bucket name. TODO: fill from the real
# distinct-value pull.
VALUE_TO_BUCKET = {}

FIELD_LABEL = "Actividad (epígrafe)"
VALUE_COLUMN = "desc_epigrafe"
# TODO: if some values must be classified by a second field (a catch-all that
# says nothing about the business), list its column(s) here; filter_to_storefront()
# and the map's pin grouping then pass them to classify() too.
# EXTRA_COLUMNS = ("some_other_column",)


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    value = (row.get(VALUE_COLUMN) or "").strip().upper()
    if not value:
        return None
    return VALUE_TO_BUCKET.get(value)
