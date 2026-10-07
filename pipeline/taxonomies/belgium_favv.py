"""FAVV-AFSCA's operator list (Belgium's food-safety agency), keyed on each
establishment's place type (`PAP PLA`) and activity (`PAP ACT`) - not NAICS.
Antwerp and Ghent are the first cities on it, placed on Flanders' VKBO points
(`pipeline/countries/belgium_favv.py`).

**ONE REGISTER, FOOD ONLY**, as Göteborg's (`sweden_livsmedel.py`): every row
is a food business the agency controls, so there is no Personal services
bucket and "Retail" is FOOD retail, labelled "Food shops" in the legend and
the layer menu.

ONE ROW PER OPERATOR x PLACE x ACTIVITY x PRODUCT. An establishment (`OP N°
Unique Id`, a KBO establishment number 2xxxxxxxxx or a FAVV-internal
9xxxxxxxxx) usually carries several rows. Step 2 hands classify() the
establishment's distinct place/activity pairs, joined as "PL92/AC66;PL83/AC66"
in `favv_pairs`, and the module decides the establishment as a whole. The
order is fixed in code (ORDER below), so a premises with two kept place types
always takes the same one: the screen's set order moved bakery and butcher
counts by 1-3 between runs (the Antwerp brief).

THE RULES, first match wins (the briefs' classification; the owner's calls of
2026-10-03 on caterers and complementary retail):

  1. An INSTITUTIONAL place type anywhere on the establishment -> out (R1:
     school, crèche, rest home, hospital, prison, central and other
     collective kitchens, baby-milk kitchens). PROVISIONAL, on the R1
     precedent as Göteborg and Stockholm apply it (an institution's kitchen is
     out even where it is typed as a restaurant). Measured 2026-10-04 before
     the join: Antwerp 28 establishments that also carry a kept type (16
     schools, 9 collective kitchens, 3 rest homes, 1 prison), Ghent 9. An
     owner call: the briefs' counts kept them.
     A BED AND BREAKFAST (PL23) anywhere on the establishment -> out, by the
     same reading: lodging is out, and a lodging's own restaurant is carved
     out of food service (Den Haag's "hotel-restaurant", premises-taxonomy
     Step 5). PROVISIONAL: measured 2026-10-04 before the join, Antwerp 16
     and Ghent 18 B&Bs also carry a kept type. FAVV has no hotel place type,
     so a hotel's kitchen registered as a restaurant cannot be told apart and
     stays.
  2. Food service: PL92 restaurant, PL12 bar or café (débit de boisson), PL46
     friterie, PL70 pita house; never on an AC94 ambulant row.
  3. Food shops: PL9 butcher, PL10 bakery, PL72 fishmonger (each not AC94),
     then PL29 retailer with AC96, AC68 or AC93. A pharmacy (PL93) is never a
     food shop on a food-only register (Stockholm's precedent; 0 overlap
     measured in either city).
  4. Everything else is out, with its reason (OUT_REASON): PL83 caterers
     (owner, R1), PL29 with AC95 "complementary retail" (owner), vehicles and
     ambulant sales, lodging, vending, wholesale, production, transport,
     farms.

Food shops rank ABOVE caterers, so a butcher-caterer (a registered shop that
also caters) is kept as a shop. PROVISIONAL, on Göteborg's precedent (a
caterer stays where its register shows a counter: Chez Kny Bistro &
Catering). The screen ranked caterers above food shops: 14 establishments in
each city move (Antwerp's food shops 1,847 here against the brief's 1,833 on
its 14 postcodes, Ghent 968 against 954). An owner call.
"""

FIELD_LABEL = "FAVV category"
# FAVV's own description of the place type the establishment is shown as,
# written as the register writes it (French in the EN file).
VALUE_COLUMN = "favv_category"
# The establishment's distinct place/activity pairs, "PL92/AC66;PL83/AC66".
EXTRA_COLUMNS = ("favv_pairs",)
PAIR_SEP = ";"

INSTITUTIONAL = {
    "PL6",    # Autre cuisine de collectivité (other collective kitchen)
    "PL27",   # Crêche
    "PL28",   # Cuisine centrale (central kitchen)
    "PL30",   # Ecole
    "PL48",   # Biberonnerie (baby-milk kitchen)
    "PL49",   # Hôpital
    "PL58",   # Maison de repos (rest home)
    "PL75",   # Prison
}
FOOD_SERVICE = ("PL92", "PL12", "PL46", "PL70")
SPECIALIST_SHOPS = ("PL9", "PL10", "PL72")
RETAILER = "PL29"
RETAIL_ACTIVITIES = ("AC96", "AC68", "AC93")
AMBULANT = "AC94"
PHARMACY = "PL93"
CATERER = "PL83"
COMPLEMENTARY = "AC95"

# The fixed order a premises' place types are tried in: the briefs' order.
ORDER = FOOD_SERVICE + SPECIALIST_SHOPS + (RETAILER,)
BUCKET = {**{c: "Food service" for c in FOOD_SERVICE},
          **{c: "Retail" for c in SPECIALIST_SHOPS + (RETAILER,)}}

# FAVV's descriptions (the EN file, 2026-09-28) of the place types the map
# shows, and the English name each pin carries in place of a business name
# (no name is ever shown: Berlin's precedent).
FAVV_DESCRIPTION = {
    "PL92": "Restaurant",
    "PL12": "Débit de boisson",
    "PL46": "Friterie",
    "PL70": "Pita-house, pita-bar",
    "PL9": "Boucherie",
    "PL10": "Boulangerie",
    "PL72": "Poissonnerie",
    "PL29": "Détaillant",
}
PIN_LABEL = {
    "PL92": "Restaurant",
    "PL12": "Bar or café",
    "PL46": "Friterie",
    "PL70": "Pita shop",
    "PL9": "Butcher",
    "PL10": "Bakery",
    "PL72": "Fishmonger",
    "PL29": "Food shop",
}

# Why an establishment with no kept pair is out, tried in this order and
# counted by step 2. Anything else is "not a storefront type".
OUT_REASON = (
    (lambda places, pairs: CATERER in places, "caterer (PL83; R1, owner 2026-10-03)"),
    (lambda places, pairs: (RETAILER, COMPLEMENTARY) in pairs,
     "complementary retail (PL29 with AC95; owner 2026-10-03)"),
    (lambda places, pairs: "PL88" in places or any(a == AMBULANT for _, a in pairs),
     "vehicle or ambulant sales (PL88, AC94)"),
    (lambda places, pairs: bool({"PL57", "PL39"} & places), "vending (PL57, PL39)"),
    (lambda places, pairs: PHARMACY in places, "pharmacy (PL93; a food-only register)"),
)
OTHER_OUT = "not a storefront type (wholesale, production, transport, farm, other)"
INSTITUTION_OUT = "institutional kitchen (R1; provisional, see the docstring)"
LODGING = "PL23"  # Chambres avec petit déjeuner (bed and breakfast)
LODGING_OUT = "bed and breakfast (PL23; lodging, its kitchen included: provisional)"


def parse_pairs(value):
    """'PL92/AC66;PL83/AC66' -> {('PL92', 'AC66'), ('PL83', 'AC66')}."""
    if not isinstance(value, str) or not value.strip():
        return set()
    out = set()
    for part in value.split(PAIR_SEP):
        part = part.strip()
        if not part:
            continue
        pla, _, act = part.partition("/")
        out.add((pla.strip().upper(), act.strip().upper()))
    return out


def establishment_class(pairs):
    """(place code shown, bucket) for a kept establishment, or (None, reason).

    `pairs` is a set of (PAP PLA code, PAP ACT code) or the joined string."""
    if isinstance(pairs, str):
        pairs = parse_pairs(pairs)
    places = {p for p, _ in pairs}
    if places & INSTITUTIONAL:
        return None, INSTITUTION_OUT
    if LODGING in places:
        return None, LODGING_OUT
    kept = set()
    for p, a in pairs:
        if p in FOOD_SERVICE and a != AMBULANT:
            kept.add(p)
        elif p in SPECIALIST_SHOPS and a != AMBULANT:
            kept.add(p)
        elif p == RETAILER and a in RETAIL_ACTIVITIES:
            kept.add(p)
    if kept and PHARMACY in places and not kept & set(FOOD_SERVICE):
        return None, "pharmacy (PL93; a food-only register)"
    for code in ORDER:
        if code in kept:
            return code, BUCKET[code]
    for test, why in OUT_REASON:
        if test(places, pairs):
            return None, why
    return None, OTHER_OUT


def legend_label(bucket):
    return {"Retail": "Food shops"}.get(bucket, bucket)


# The layer menu says what the legend says, as on the Swedish maps.
layer_label = legend_label


# The Retail bucket here is food shops only, so its pins are olive, not retail
# blue (owner, 2026-10-07: one pin colour per meaning; pipeline/taxonomies
# MEANING_COLOURS).
PIN_MEANINGS = {"Retail": "Food shops"}


def classify(row):
    """Bucket for an establishment, or None if it is not a tracked storefront."""
    code, bucket = establishment_class(row.get("favv_pairs") or "")
    return bucket if code else None


assert set(ORDER) == set(FAVV_DESCRIPTION) == set(PIN_LABEL) == set(BUCKET)
assert not set(ORDER) & INSTITUTIONAL
# The two owner calls and the provisional orderings, pinned.
assert classify({"favv_pairs": "PL83/AC66"}) is None
assert classify({"favv_pairs": "PL29/AC95"}) is None
assert classify({"favv_pairs": "PL9/AC68;PL83/AC66"}) == "Retail"
assert establishment_class("PL92/AC66;PL12/AC66")[0] == "PL92"
assert establishment_class("PL29/AC96;PL10/AC68")[0] == "PL10"
assert classify({"favv_pairs": "PL92/AC66;PL30/AC66"}) is None
assert classify({"favv_pairs": "PL92/AC66;PL23/AC66"}) is None
assert classify({"favv_pairs": "PL10/AC94"}) is None
