"""Rotterdam: two layers of different kinds, dispatched on `source`.

  * `permit` - a premises REBUILT from the exploitation-permit decisions
    Rotterdam publishes in its Gemeenteblad (KOOP's official publications).
    Step 2 decides which notices count, by each notice's own title, and keeps
    only premises with a grant inside the permit's term; every kept premises
    is Food service. The notices carry no trade name for the map to show
    (their titles and abstracts sometimes do, and are never used).
  * `bag` - a unit in the national building register (BAG) whose use class is
    `winkelfunctie`. What a unit is FOR, not what is in it, so retail and
    personal services cannot be split: every unit is Retail, labelled "Shops
    and services" - Amsterdam's owner decision of 2026-09-24, the same data.

Amsterdam's shape (`amsterdam_source`), with the permit side reduced to what a
notice title can say. `map_common.py` needed no change.
"""

FIELD_LABEL = "Activity"
VALUE_COLUMN = "activity"
EXTRA_COLUMNS = ("source", "notice_kind")

SOURCES = ("permit", "bag")

# The notice kinds step 2 KEEPS - an exploitation permit (granted, amended or
# provisional) or a coffeeshop's. Everything else it reads - alcohol-licence,
# terrace, gaming-machine, event and sex-business notices, refusals and
# withdrawals - never reaches this module.
PERMIT_KINDS = {"exploitatie": "Exploitation permit", "voorlopige": "Provisional permit",
                "coffeeshop": "Coffeeshop"}
PERMIT_NAME = "Hospitality premises"
BAG_LABEL = "Shop or service unit"


def classify(row):
    """A cleaned row -> a bucket name, or None if it is not a storefront."""
    source = str(row.get("source", "")).strip()
    if source == "bag":
        return "Retail"
    if source == "permit":
        kind = row.get("notice_kind")
        if kind not in PERMIT_KINDS:
            raise ValueError(f"unmapped notice kind {kind!r} - map it in "
                             f"pipeline/taxonomies/rotterdam_source.py")
        return "Food service"
    return None


def legend_label(bucket):
    return {"Retail": "Shops and services"}.get(bucket, bucket)


layer_label = legend_label
