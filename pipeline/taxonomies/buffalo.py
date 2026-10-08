"""Buffalo taxonomy - a DISPATCHING taxonomy over three registries, New York's
shape (the multi-source-city skill), because Buffalo's own licence file is a
regulated-activity list rather than a business register.

  source      registry                                         bucket
  ----------  -----------------------------------------------  ------------------
  city        City of Buffalo Business Licenses (qcyy-feh8)    by `descript`, below
  nys_store   NYS Retail Food Stores (9a8c-vfzj)                Retail
  nys_salon   NYS Appearance Enhancement / Barber BUSINESS      Personal services
              licences (y3u4-jbgh)

The City's file holds 12,131 licences, mostly elevators (2,935), fuel devices
(1,182) and amusement shows (1,004): the storefront codes are the short list
below, read against docs/category_rules.md. `VALUE_COLUMN` is each registry's
own category string, `EXTRA_COLUMNS` carries `source`.

Personal information: no registrant's own name is read. The City's file has
no person column; the salon registry's `license_holder_name` is never
downloaded (step 2 asserts it).
"""

SOURCES = ("city", "nys_store", "nys_salon")

# Which source wins when one site is in several (step 2's dedup): the City's
# food licence identifies a restaurant most specifically; then the State's
# grocery licence over the City's own Food Store licence, since the State's
# register is the one every grocer must hold; then salons; the City's retail
# slice last.
SOURCE_PRIORITY = ("city_food", "nys_store", "nys_salon", "city")

# The City's `descript` -> bucket, on docs/category_rules.md.
CITY_DESCRIPT_TO_BUCKET = {
    "RESTAURANT": "Food service",
    "RESTAURANT TAKE OUT": "Food service",
    # A restaurant licensed for dancing - a nightclub or a bar with a floor:
    # nightclubs are kept as Food service (category_rules, R5).
    "RESTAURANT / DANCE": "Food service",
    "BAKERS AND CONFECTIONERS": "Food service",
    "FOOD STORE": "Retail",
    "MEAT FISH & POULTRY": "Retail",
    # Car dealers kept as Retail (R4).
    "USED CAR DEALER": "Retail",
    "SECOND HAND DEALER": "Retail",
    "TOBACCO HOOKAH VAPING": "Retail",
    # Pawnbrokers kept as Retail (R5); New York and Chicago are the disclosed
    # exceptions, not the rule.
    "PAWNBROKER": "Retail",
    "PET SHOP": "Retail",
    "SELF-SRV LAUNDRY / DRY CLEANER": "Personal services",
    "CLOTHES-DRY CLEANERS PERMIT": "Personal services",
}

# Downloaded but never a pin, each with its reason.
CITY_DESCRIPT_EXCLUDED = {
    # R1: event caterers have no counter of their own. The brief counted
    # Caterer as food; the rule is the precedent, and it is followed.
    "CATERER": "Food with no counter of its own (category_rules R1)",
    # A restaurant's permit to seat on the pavement, not a premises: it adds no
    # pin (the brief's "adjunct, never a pin").
    "SIDEWALK CAFE": "A permission a restaurant holds, not a premises",
}

NYS_STORE_BUCKET = "Retail"
NYS_SALON_BUCKET = "Personal services"
# Business licences only; the renters are individuals working a chair inside
# another licensee's shop (New York's rule).
NYS_SALON_KEEP_LICENSE_TYPES = {
    "DOSAEBUSINESS": "Appearance enhancement business",
    "DOSBARSHOPOWNER": "Barber shop",
}
NYS_SALON_EXCLUDE_LICENSE_TYPES = ("DOSAERENTER", "DOSBARRENTER")

FIELD_LABEL = "Category"
VALUE_COLUMN = "business_category"
EXTRA_COLUMNS = ("source",)


# The Retail layer here is a licensed slice, not general retail, so the
# legend and the layer menu name what it holds (owner, 2026-10-07; measured
# on the clean file: food 76.5%, used cars 15.0%, secondhand 4.9% of 728).
# Its pins stay retail blue (owner).
def legend_label(bucket: str) -> str:
    return {"Retail": "Food stores, used-car and secondhand dealers"}.get(bucket, bucket)


layer_label = legend_label


def classify(row: dict):
    """Dispatch on `source`. An unknown source is a step 2 bug and raises."""
    source = (row.get("source") or "").strip()
    if not source:
        return None
    if source == "nys_store":
        return NYS_STORE_BUCKET
    if source == "nys_salon":
        return NYS_SALON_BUCKET
    if source == "city":
        return CITY_DESCRIPT_TO_BUCKET.get(
            (row.get("business_category") or "").strip().upper())
    raise ValueError(f"Unknown Buffalo source {source!r}; expected one of {SOURCES}")
