"""Riga: two layers of different kinds, dispatched on `source` - Amsterdam's and
Rotterdam's shape.

  * `excise` - a premises in the State Revenue Service's (VID) excise-licence
    register whose place type (`Darbibas_vietas_tips`) reads as food service:
    café, bar, restaurant, pizzeria, canteen... Step 2 decides which; every row
    that reaches this module is Food service. The register's licence HOLDER is
    never read, so these dots carry the place type, not a name.
  * `cadastre` - a State Land Service (VZD) premise group of use class 1230
    (trade) whose name reads as a shop or a personal service. The cadastre
    records what a unit is FOR, so retail and services are one category,
    "Shops and services" - Amsterdam's owner decision, the same kind of data.
"""

FIELD_LABEL = "Kind"
VALUE_COLUMN = "activity"
EXTRA_COLUMNS = ("source",)

SOURCES = ("excise", "cadastre")


def classify(row):
    source = str(row.get("source", "")).strip()
    if source == "cadastre":
        return "Retail"
    if source == "excise":
        return "Food service"
    return None


def legend_label(bucket):
    return {"Retail": "Shops and services"}.get(bucket, bucket)


# The layer menu names the categories as the legend does.
layer_label = legend_label
