"""Den Haag: two layers of different kinds, dispatched on `source`.

  * `permit` - the Gemeente Den Haag's hospitality-permit layer
    (`Horeca_nieuw` layer 2, "Horecavergunningen"), the layer the city's own
    permit map reads. Its type of business (`TYPEBEDRIJ`, repaired from
    double-encoded UTF-8 by step 2) decides whether a permit is a storefront.
    Every kept permit is Food service.
  * `bag` - a unit in the national building register (BAG) whose use class is
    `winkelfunctie`. What a unit is FOR, not what is in it, so retail and
    personal services cannot be split: every unit is Retail, labelled "Shops
    and services" - Amsterdam's owner decision of 2026-09-24, the same data,
    and Rotterdam's.

Rotterdam's two-layer shape (`rotterdam_source`) with Amsterdam's permit side
(`amsterdam_source`): Rotterdam's module classifies notice kinds rebuilt from
gazette titles, which this layer does not have, so Den Haag needs its own.

THE TYPE MAPPING FOLLOWS AMSTERDAM'S (owner, 2026-09-24) and
docs/category_rules.md, matched by what each premises IS. In: restaurants,
cafés, lunchrooms, coffee houses, takeaways, snack bars, ice cream, bakeries'
cafés, beach pavilions, coffeeshops, nightclubs and sports bars - premises with
a street door where a customer buys food or drink. Out, as Amsterdam's
`Additionele horeca`, `Culturele horeca`, `Sociëteit`, `Hotel` and
`Zalenverhuur`: sports-club canteens and club houses, community, youth and
cultural centres, theatre and cinema foyers, event sites, party centres and
hall hire, cooking studios, members' clubs, hotels and their restaurants (as
Florence leaves restaurants inside hotels out), and the department store
(Amsterdam's `Warenhuis`). Out by the rules: caterers and staff canteens (R1),
sex businesses (R3), gaming halls and the casino (R5), recreation (pool halls,
bowling, dance schools, sports halls). Out as no food premises at all: a beauty
salon, an estate agent, a gym, and blank or "niet van toepassing" types. A type
not listed here raises in step 2, so a new value cannot slip onto the map or
off it silently.
"""

FIELD_LABEL = "Activity"
VALUE_COLUMN = "activity"
EXTRA_COLUMNS = ("source", "type_bedrijf")

SOURCES = ("permit", "bag")

# TYPEBEDRIJ (repaired) -> kept (True) or out (False), with the tooltip's
# English label for the kept ones.
PERMIT_TYPES = {
    # --- kept: Food service ---------------------------------------------------
    "restaurant": True, "café": True, "lunchroom": True, "café-restaurant": True,
    "afhaalwinkel": True, "snackbar": True, "cafetaria": True, "koffiehuis": True,
    "broodjeszaak": True, "fastfoodrestaurant": True, "eetcafé": True, "ijssalon": True,
    "eethuis": True, "pizzeria": True, "shoarmazaak": True, "grillroom": True,
    "grillrestaurant": True, "café-bar": True, "restaurant-lunchroom": True,
    "lunchroom/restaurant": True, "brasserie": True, "grandcafé": True,
    "koffiehuis/lunchroom": True, "lunchroom/ijssalon": True, "tearoom": True,
    "coffeecorner": True, "croissanterie": True, "juicebar": True, "bar-bistro": True,
    "traiteur": True, "bakkerij": True, "food court": True,
    # A beach pavilion is a restaurant or bar on the beach, open to anyone.
    "strandpaviljoen": True,
    # Coffeeshops: kept, as Amsterdam's and Rotterdam's are (owner, 2026-09-24).
    "coffeeshop": True,
    # Nightclubs (not adult): kept (docs/category_rules.md, R5).
    "discotheek": True, "café-discotheek": True, "nachtclub": True,
    # A sports bar is a café. Club canteens the register types this way are
    # re-typed by their own description in step 2 (CANTEEN_WORDS).
    "sportcafé": True,
    # Every permit of this type is a restaurant or lunchroom by its own
    # description (six, 2026-09-30); the type names the building it is in.
    "attractiecentrum": True,
    # --- out ------------------------------------------------------------------
    # Catering inside a non-commercial venue (Amsterdam's Additionele horeca).
    "sportkantine": False, "clubgebouw": False, "kantine": False, "buurtcentrum": False,
    "jongerencentrum": False, "sportcomplex": False, "sporthal": False,
    # Venues (Amsterdam's Culturele horeca), events, halls and members' clubs.
    "theaterfoyer": False, "bioscoopfoyer": False, "cultureel centrum": False,
    "evenementenlokatie": False, "partycentrum": False, "zalenverhuur": False,
    "kookstudio": False, "sociëteit": False,
    "begraafplaats en crematorium": False,
    # Lodging, and the restaurants inside hotels.
    "hotel": False, "hotel-restaurant": False, "restaurant/hotelbar": False,
    "bed & breakfast": False,
    # The department store (Amsterdam's Warenhuis).
    "warenhuis": False,
    # Rules R1, R3, R5 and recreation.
    "cateringsbedrijf": False, "seksinrichting": False, "amusementshal": False,
    "speelautomatenhal": False, "casino": False, "poolbiljart": False,
    "bowlingcentrum": False, "dansschool": False, "sportschool": False,
    # No food premises, or no type.
    "schoonheidssalon": False, "makelaar": False, "niet van toepassing": False, "": False,
}

_LABELS = {
    "restaurant": "Restaurant", "café": "Café (bar)", "lunchroom": "Lunchroom",
    "café-restaurant": "Café-restaurant", "afhaalwinkel": "Takeaway",
    "snackbar": "Snack bar", "cafetaria": "Snack bar", "koffiehuis": "Coffee house",
    "broodjeszaak": "Sandwich shop", "fastfoodrestaurant": "Fast food",
    "eetcafé": "Café serving food", "ijssalon": "Ice cream parlour", "eethuis": "Eatery",
    "pizzeria": "Pizzeria", "shoarmazaak": "Shawarma shop", "grillroom": "Grill room",
    "grillrestaurant": "Grill room", "café-bar": "Café (bar)",
    "restaurant-lunchroom": "Restaurant and lunchroom",
    "lunchroom/restaurant": "Restaurant and lunchroom", "brasserie": "Brasserie",
    "grandcafé": "Grand café", "koffiehuis/lunchroom": "Coffee house",
    "lunchroom/ijssalon": "Lunchroom", "tearoom": "Tearoom", "coffeecorner": "Coffee bar",
    "croissanterie": "Bakery café", "juicebar": "Juice bar", "bar-bistro": "Bistro",
    "traiteur": "Delicatessen", "bakkerij": "Bakery café", "food court": "Food court",
    "strandpaviljoen": "Beach pavilion", "coffeeshop": "Coffeeshop",
    "discotheek": "Nightclub", "café-discotheek": "Nightclub", "nachtclub": "Nightclub",
    "sportcafé": "Sports bar", "attractiecentrum": "Restaurant",
}
PERMIT_NAME = "Hospitality premises"
BAG_LABEL = "Shop or service unit"


def permit_kept(type_bedrijf):
    """True / False for a permit's (repaired) type, or raise on a type never seen."""
    t = (type_bedrijf or "").strip()
    if t not in PERMIT_TYPES:
        raise ValueError(f"unmapped permit type {type_bedrijf!r} - map it in "
                         f"pipeline/taxonomies/den_haag_source.py")
    return PERMIT_TYPES[t]


def activity_label(type_bedrijf):
    t = (type_bedrijf or "").strip()
    return _LABELS.get(t, t)


def classify(row):
    """A cleaned row -> a bucket name, or None if it is not a storefront."""
    source = str(row.get("source", "")).strip()
    if source == "bag":
        return "Retail"
    if source == "permit":
        t = row.get("type_bedrijf")
        t = "" if t is None or t != t else t  # NaN -> ""
        return "Food service" if permit_kept(t) else None
    return None


def legend_label(bucket):
    return {"Retail": "Shops and services"}.get(bucket, bucket)


# The layer control names the bucket the way the legend does.
layer_label = legend_label
