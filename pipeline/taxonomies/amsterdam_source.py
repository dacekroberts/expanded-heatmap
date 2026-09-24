"""Amsterdam: two layers of different kinds, dispatched on `source`.

  * `permit` - the city's live hospitality-permit register
    (`horeca/exploitatievergunning`). Its own `zaakCategorie`, and for the
    catch-all `Onbekend` its `zaakSpecificatie`, decide whether a permit is a
    storefront. Every kept permit is Food service.
  * `bag` - a unit in the national building register (BAG) whose use class is
    `winkelfunctie` (shop). The BAG records what a unit is FOR, not what is in
    it: no name, no activity. So a hairdresser and a clothes shop are the same
    row, and retail and personal services CANNOT be split here. Every such unit
    goes in the Retail bucket, and its legend row says "Shops and services" -
    owner's decision 2026-09-24, with the page saying the split other cities
    show is not available here.

The same dispatching shape as New York's and Milan's taxonomies
(`EXTRA_COLUMNS = ("source", ...)`); `map_common.py` needed no change.

THE PERMIT MAPPING IS THE OWNER'S, 2026-09-24. In: restaurants, cafés,
alcohol-free (lunchrooms, coffee houses, sandwich shops, ice cream), fast
food, eethuis, the with-function-room variants, the shop-plus-horeca
`Mengformule`, coffeeshops and nightclubs - every one a premises with a street
door where a customer buys food or drink. Out: `Additionele horeca` (318 -
sports-club canteens, community centres, theatre and cinema foyers: catering
INSIDE a non-commercial venue), `Culturele horeca` (venues), `Sociëteit`
(members-only student and private clubs - Rome's `Circoli Privati` rule),
`Hotel` and `Zalenverhuur` (hall hire). The 241 `Onbekend` permits are sorted
by their own specification on exactly the same line.
"""

FIELD_LABEL = "Activity"
VALUE_COLUMN = "activity"
EXTRA_COLUMNS = ("source", "zaak_categorie", "zaak_specificatie")

SOURCES = ("permit", "bag")

# zaakCategorie -> kept (True) or out (False). `Onbekend` is decided by
# specification below; a category not listed here is unknown and raises in
# step 2, so a new value cannot slip onto the map or off it silently.
PERMIT_CATEGORIES = {
    "Restaurant": True, "Café": True, "Alcoholvrij": True, "Fastfood": True,
    "Eethuis": True, "Restaurant met zaalverhuur": True, "Café met zaalverhuur": True,
    "Mengformule": True, "Coffeeshop": True, "Nachtzaak": True,
    "Additionele horeca": False, "Culturele horeca": False, "Sociëteit": False,
    "Hotel": False, "Zalenverhuur": False,
    "Onbekend": None,
}

# For `Onbekend` only: zaakSpecificatie -> kept or out, on the categories' line.
ONBEKEND_SPECS = {
    "Lunchroom": True, "Fastfood restaurant": True, "Snackbar": True, "Coffeeshop": True,
    "Grillroom": True, "Fastfood": True, "Nachtclub": True, "Discotheek": True,
    "IJssalon": True, "Tearoom": True, "Eetcafe": True, "Restaurant met zaalverhuur": True,
    "Alcohol verstrekkend bedrijf- dagzaak": True,
    "Zalenverhuur": False, "Hotel": False, "Horeca VI": False,
    "Culturele horeca (Horeca VI)": False, "Bioscoopfoyer": False, "Jongerencentrum": False,
    "Sporthal": False, "Sociëteit": False, "Warenhuis": False, "Onbekend": False,
    None: False,
}

# The tooltip's activity line, in English. The register's own words are
# Dutch and mostly self-explanatory; these are the ones a reader would not
# guess, keyed by specification first, then category.
_LABELS = {
    "Restaurant": "Restaurant", "Café": "Café (bar)", "Eetcafé": "Café serving food",
    "Eetcafe": "Café serving food", "Nachtclub": "Nightclub", "Discotheek": "Nightclub",
    "Lunchroom": "Lunchroom", "Koffiehuis": "Coffee house", "Broodjeszaak": "Sandwich shop",
    "IJssalon": "Ice cream parlour", "Tearoom": "Tearoom", "Snackbar": "Snack bar",
    "Fastfood": "Fast food", "Fastfood restaurant": "Fast food", "Afhaalrestaurant": "Takeaway",
    "Cafetaria": "Snack bar", "Grillroom": "Grill room", "Coffeeshop": "Coffeeshop",
    "Eethuis": "Eatery", "Restaurant met zaalverhuur": "Restaurant with function room",
    "Café met zaalverhuur": "Café with function room", "Mengformule winkel": "Shop with café",
    "Alcohol verstrekkend bedrijf- dagzaak": "Café (bar)",
}
BAG_LABEL = "Shop or service unit"


def permit_kept(categorie, specificatie):
    """True / False for a permit, or raise on a category never seen."""
    if categorie not in PERMIT_CATEGORIES:
        raise ValueError(f"unmapped permit category {categorie!r} - map it in "
                         f"pipeline/taxonomies/amsterdam_source.py")
    kept = PERMIT_CATEGORIES[categorie]
    if kept is None:
        if specificatie not in ONBEKEND_SPECS:
            raise ValueError(f"unmapped Onbekend specification {specificatie!r}")
        kept = ONBEKEND_SPECS[specificatie]
    return kept


def activity_label(categorie, specificatie):
    return _LABELS.get(specificatie) or _LABELS.get(categorie) or categorie


def classify(row):
    """A cleaned row -> a bucket name, or None if it is not a storefront."""
    source = str(row.get("source", "")).strip()
    if source == "bag":
        return "Retail"
    if source == "permit":
        cat = row.get("zaak_categorie")
        spec = row.get("zaak_specificatie")
        spec = None if spec is None or spec != spec or spec == "" else spec  # NaN -> None
        return "Food service" if permit_kept(cat, spec) else None
    return None


def legend_label(bucket):
    return {"Retail": "Shops and services"}.get(bucket, bucket)
