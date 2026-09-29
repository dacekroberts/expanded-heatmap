"""Sweden's food-control register types (Livsmedelsverket's `VerksamhetsTyp`,
as Stockholms stad's Livsmedelstillsyn layer carries them) - not NAICS.
Stockholm is the first city on it.

**ONE REGISTER, FOOD ONLY.** Every premises is one the city's food control
inspects, so there is no Personal services bucket, and "Retail" is FOOD retail
only. Its legend reads "Food shops" (the Japanese and UK cities' precedent,
owner 2026-09-27), never "Retail".

TYPES. Two are storefronts; a premises can carry several (step 2 joins them
with " | "), and it is a storefront if any of its types is:

  Restaurang-, catering- och barverksamhet  -> Food service
  Detaljhandel                              -> Retail ("Food shops")

Every other type is listed in EXCLUDED_TYPES so a NEW one stops step 2.

NAMES. Two jobs, both measured by Staging on typed premises (DECISIONS,
2026-09-28, "Stockholm is built on its register as frozen"):

  * NOT_STOREFRONT_NAME removes catering and institutional kitchens that the
    restaurant type contains (schools, care homes, staff canteens, central
    kitchens).
  * An UNTYPED premises (the type field arrived with the 2024 inspections) is
    classified FROM ITS NAME when step 2 passes `name_classified=True`: food
    service first, then food shops; pharmacies never (owner, 2026-09-28: the
    225 recognised by name, last inspected 2022-23, flagged on the map).
"""
import re

FIELD_LABEL = "Verksamhetstyp"
VALUE_COLUMN = "VerksamhetsTyp"
# The premises' name, which classify() reads for the two jobs above.
EXTRA_COLUMNS = ("business_name", "name_classified")

TYPE_TO_BUCKET = {
    "Restaurang-, catering- och barverksamhet": "Food service",
    "Detaljhandel": "Retail",
}
# Every other type on Stockholm's register (the full distinct list, 2026-09-29,
# inspection rows in brackets): production, wholesale, transport and water -
# none a premises a passer-by walks into. A premises that also carries a
# storefront type (a bakery that sells over the counter) is kept by that type.
EXCLUDED_TYPES = {
    "Partihandel",                                            # wholesale (2,810)
    "Transport och lagring",                                  # transport, storage (1,145)
    "Annan livsmedelsframställning",                          # other food production (433)
    "Malet kött, köttberedningar och maskinurbenat kött",     # minced meat production (406)
    "Tillverkning av bageri- och mjölprodukter",              # bakery production (384)
    "Fiskeriprodukter",                                       # fish processing (347)
    "Köttprodukter",                                          # meat products (232)
    "Kött från tama hov- och klövdjur",                       # slaughter, domestic (228)
    "Allmänna verksamhetsanläggningar (kyl- och fryshus, ompaketering och ompaketering av "
    "förpackningar, grossistmarknader, kylfartyg)",           # cold stores, repacking (178)
    "Framställning av drycker",                               # beverage production (161)
    "Anläggningar som producerar material som kommer i kontakt med livsmedel",  # packaging (113)
    "Råmjölk, obehandlad mjölk, råmjölksbaserade produkter och mjölkprodukter",  # dairy (83)
    "Beredning och hållbarhetsbehandling av frukt, bär och grönsaker",  # produce processing (77)
    "Ägg och äggprodukter",                                   # eggs (23)
    "Distributionsnät",                                       # water distribution (12)
    "Huvudkontor dricksvatten",                               # drinking-water head office (12)
    "Kött av frilevande vilt",                                # game meat (9)
    "Vattenverk",                                             # water works (8)
    # "Other" (1,731 rows): a catch-all, read by name before it was excluded -
    # see the note in DECISIONS (2026-09-29).
    "Övrigt",
}
KNOWN_TYPES = set(TYPE_TO_BUCKET) | EXCLUDED_TYPES
SEPARATOR = " | "
# What an untyped premises classified from its name carries in VALUE_COLUMN,
# and so what its pin says.
NAME_CLASSIFIED_VALUE = "No type recorded (classified from its name)"

# Staging's rules, lower-cased names (sthlm_untyped.py, 2026-09-28).
FOOD_NAME = re.compile(
    r"restaurang|restaurant|pizz|sushi|kebab|burger|grill|bistro|brasseri|krog|pub|\bbar\b|bar &|"
    r"vinbar|cafe|café|kafe|coffee|espresso|konditori|bageri|bakery|thai|ramen|noodle|taco|falafel|"
    r"deli|kitchen|kök\b|matsal(?!.*personal)|lunch|dining|trattoria|osteria|tapas|izakaya|poke|"
    r"bowl|juice|glass|gelato|hamburg|wok|dumpling|curry|meze|steakhouse|kafé|hotdog|korv")
SHOP_NAME = re.compile(
    r"\bica\b|coop|hemköp|willys|lidl|city gross|pressbyrån|7-eleven|seven eleven|livs|\bmat\b|"
    r"market|mart\b|supermarket|butik|handel|charkuteri|fisk|ost\b|delikatess|frukt|grönt|"
    r"hälsokost|systembolaget|tobak|kiosk|servicebutik|godis|choklad|te &|kaffe")
PHARMACY_NAME = re.compile(r"apote")
# Staging's rule, with five words bounded at the build (2026-09-29) after its
# 686 matches on typed storefronts were read: "lss" had matched Olsson and
# Karlsson, "sfi" Kungsfisk, "lager" Lagerbaren, "kontor" Restaurang
# Kontoret, and "kyrka" Slaktkyrkan (a bar and club, not a church).
NOT_STOREFRONT_NAME = re.compile(
    r"skola|förskola|skolan|gymnasi|fritids|äldreboende|vårdboende|servicehus|sjukhus|vårdcentral|"
    r"personalmatsal|personalrum|personal|\bkontor\b|\blager\b|distribution|transport|grossist|"
    r"partihandel|produktion|tillverkning|centralkök|tillagningskök|mottagningskök|boende|\blss\b|"
    r"hvb|(?<!slakt)kyrka|församling|förening|idrottsförening|dricksvatten|vattenverk|\bsfi\b|"
    r"universitet|högskola|kårhus|fängelse|anstalt|häkte|kommun|region|stadsdel|ab\b.*huvudkontor|"
    # Added at the build (2026-09-29) from the placed pins' names: home care,
    # day centres and elderly care, Montessori and parent-cooperative
    # preschools.
    r"hemtjänst|dagverksamhet|daglig verksamhet|äldreomsorg|montessori|föräldrakoop")


def name_bucket(name):
    """The bucket a premises' NAME says, or None: 'not a storefront' wins,
    then food service, then food shops; a pharmacy is never a food shop."""
    n = (name or "").lower()
    if NOT_STOREFRONT_NAME.search(n) or PHARMACY_NAME.search(n):
        return None
    if FOOD_NAME.search(n):
        return "Food service"
    if SHOP_NAME.search(n):
        return "Retail"
    return None


def legend_label(bucket):
    return {"Retail": "Food shops"}.get(bucket, bucket)


def classify(row):
    """Bucket for a premises, or None if it is not a tracked storefront."""
    name = row.get("business_name") or ""
    if str(row.get("name_classified", "")).lower() in ("true", "1"):
        return name_bucket(name)
    types = [t for t in (row.get(VALUE_COLUMN) or "").split(SEPARATOR) if t]
    buckets = [TYPE_TO_BUCKET[t] for t in types if t in TYPE_TO_BUCKET]
    if not buckets:
        return None
    n = name.lower()
    # Food service wins over a shop for a premises that is both (a café-bakery).
    if "Food service" in buckets:
        # The restaurant type holds every institutional kitchen: preschools,
        # schools, care homes, staff canteens (665 of 4,967, 2026-09-29).
        return None if NOT_STOREFRONT_NAME.search(n) else "Food service"
    # A SHOP inside an institution is still a shop (Tekniska högskolans
    # Tobak), so the institution test is not applied here; a pharmacy is
    # never a food shop, as for the untyped premises (12 typed).
    return None if PHARMACY_NAME.search(n) else "Retail"


assert not set(TYPE_TO_BUCKET) & EXCLUDED_TYPES
