"""ANZSIC 2006 classes as the City of Sydney's Floor Space and Employment
Survey (FES) publishes them - one class per business establishment, matched on
the 4-digit CLASS CODE, never on its label.

**NAMED FOR THE SOURCE KIND, NOT THE CITY.** ANZSIC is Australia's and New
Zealand's national classification, but what a bucket can hold here is decided
by a floor-space census: every establishment the City's surveyors counted,
with no names or addresses (the publisher strips them). Sydney is the first
city on it (2026-09-28).

**AN EXPLICIT CLASS LIST, NOT PREFIXES.** The storefront divisions are 39-43
(motor vehicle, fuel and store-based retail), 45 (food and beverage services)
and 95 (personal services); every class in them was decided one by one on the
2022 survey (7,497 rows), mirroring pipeline/taxonomies/naics.py where NAICS
has the same line:

  * KEPT - motor vehicle and parts retail (39, NAICS 441) and fuel retail
    (4000, NAICS 447), as every NAICS city keeps them.
  * EXCLUDED, NOT STOREFRONTS - non-store retail (4310) and commission-based
    retail (4320), naics.py's 454; parking (9533), naics.py's 81293.
  * EXCLUDED (owner, 2026-09-28) - brothel keeping (9534, 27 in 2022);
    catering services (4513, 21: the work happens at the event, as the FSA
    cities' "Other catering premises"); funeral, crematorium and cemetery
    services (9520, 7: not storefronts); licensed members' clubs (4530, 27:
    entered by sign-in, not walk-in).
  * EXCLUDED, ORGANISATIONS - religious services (954) and business, labour
    and interest-group associations (955), which NAICS keeps in 813, outside
    its personal services.
  * CATCH-ALLS KEPT (owner, 2026-09-28) - Other Store-Based Retailing n.e.c.
    (4279, 311, 10% of Retail) and Other Personal Services n.e.c. (9539, 254,
    a quarter of Personal services). With no names they cannot be sampled,
    and with no names they expose no one.

A class not listed stops step 2, so a re-published survey with a new class is
decided rather than silently dropped. The label (`ClassificationName`) is the
publisher's own and is what a pin shows.
"""

FIELD_LABEL = "ANZSIC class"
VALUE_COLUMN = "ClassificationName"
EXTRA_COLUMNS = ("ClassificationCode",)

RETAIL = {
    "3911", "3912", "3913", "3921", "3922",          # motor vehicles and parts
    "4000",                                          # fuel
    "4110", "4121", "4122", "4123", "4129",          # food retail
    "4211", "4212", "4213", "4214", "4221", "4222", "4229", "4231", "4232",
    "4241", "4242", "4243", "4244", "4245", "4251", "4252", "4253", "4259",
    "4260", "4271", "4272", "4273", "4274", "4279",
}
FOOD_SERVICE = {"4511", "4512", "4520"}
PERSONAL_SERVICES = {"9511", "9512", "9531", "9532", "9539"}

EXCLUDED = {
    "4310": "Non-Store Retailing",
    "4320": "Retail Commission-Based Buying and/or Selling",
    "4513": "Catering Services (owner, 2026-09-28)",
    "4530": "Clubs (Hospitality) - members' clubs, not walk-in (owner, 2026-09-28)",
    "9520": "Funeral, Crematorium and Cemetery Services (owner, 2026-09-28)",
    "9533": "Parking Services",
    "9534": "Brothel Keeping and Prostitution Services (owner, 2026-09-28)",
    # Groups 954 and 955 are organisations, not services sold over a counter:
    # NAICS keeps them in 813, outside 812.
    "9540": "Religious Services",
    "9551": "Business and Professional Association Services",
    "9552": "Labour Association Services",
    "9559": "Other Interest Group Services n.e.c.",
}
CATCH_ALL_CODES = {"4279", "9539"}

_CODE_BUCKETS = {
    **{c: "Retail" for c in RETAIL},
    **{c: "Food service" for c in FOOD_SERVICE},
    **{c: "Personal services" for c in PERSONAL_SERVICES},
}
# The storefront divisions: a class inside them must be decided (bucketed or
# excluded); step 2 stops on one that is neither.
STOREFRONT_DIVISIONS = ("39", "40", "41", "42", "43", "45", "95")


def normalise_code(value):
    code = str(value or "").strip()
    return code if code.isdigit() else ""


def undecided(code):
    """True for a class inside the storefront divisions that is neither
    bucketed nor excluded - a new class, to decide before trusting a count."""
    code = normalise_code(code)
    return (code.startswith(STOREFRONT_DIVISIONS) and code not in _CODE_BUCKETS
            and code not in EXCLUDED)


def classify(row):
    """Bucket for a row, or None if it is not tracked storefront commerce."""
    return _CODE_BUCKETS.get(normalise_code(row.get("ClassificationCode")))


def legend_label(bucket):
    return bucket


assert not set(_CODE_BUCKETS) & set(EXCLUDED), "a class is both bucketed and excluded"
assert CATCH_ALL_CODES <= set(_CODE_BUCKETS), "a catch-all must be a kept class"
