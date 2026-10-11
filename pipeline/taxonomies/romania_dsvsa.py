"""Romania's DSVSA registers - the sanitary-veterinary and food safety
authority's lists of registered food units, one file per unit category - not
NAICS. Bucharest is the first city on it.

**FOOD ONLY.** DSVSA registers food-handling units, so there is no Personal
services bucket, and "Retail" is FOOD retail only; its legend reads "Food
shops" (the Japanese and UK cities' precedent), never "Retail".

THE FILE IS THE CLASSIFICATION. `source_files` carries every file a premises
appears in (a hypermarket's butcher, fishmonger and food counter are three
registrations at one address, merged in step 2), as `A<nn>` for the
animal-origin list and `N<nn>` for the non-animal-origin list:

  Food service: A19 restaurants, cafés and bars; A20 pizzerias; N36 bars and
                cafés; N24 ice-cream makers (gelaterias)
  Food shops:   A01 pork butchers; A02 butchers; A11 fishmongers; A16 honey
                shops; A23 confectioners and pastry shops; A25 food shops;
                A26 supermarkets; N01 bakeries; N02 pastry shops; N03 bakery
                and pastry shops; N33 retail; N42 frozen and chilled counters

A premises in a SHOP file (A25, A26, N33) is a food shop even when it also has
a food-service registration (a supermarket's café); otherwise any food-service
file makes it Food service (a pizzeria that also registered as a pastry shop).

The category text (`Categorie`, free text with spelling variants) decides the
exceptions: kiosk carts (`toneta`), vending machines (`automat`) and pastry
LABS (`laborator`, the owner's exclusion of file 22 applied to the rows filed
elsewhere) are not storefronts. A category the taxonomy has not seen is shown
as registered; the FILE decides its bucket, and step 2 prints every category
per file so a new one is read, not waved through.

EVERY COUNTY AFTER BUCHAREST READS A FILE BY ITS ROLE, NEVER ITS NUMBER
(Cluj-Napoca, 2026-10-11). Each county directorate numbers its files its own
way: Cluj's file 23 is the food shops and its 21 the confectioners, where
Bucharest's 23 is the confectioners and its 25 the food shops, so a Cluj code
read through the sets above would re-bucket food shops silently. A county's
`source_files` codes are written `<A|N><nn>:<role>` ("A23:food_shop"): the
county's own number kept for the record, the role deciding the bucket through
ROLE_BUCKET. `role_for_file()` reads the role from the file's NAME and stops
on a name it cannot read. Bucharest's bare codes (no colon) keep the sets
above, so its outputs cannot move.
"""
import re
import unicodedata

FIELD_LABEL = "Categorie unitate"
VALUE_COLUMN = "Categorie"
EXTRA_COLUMNS = ("source_files",)

FOOD_SERVICE_FILES = {"A19", "A20", "N36", "N24"}
SHOP_FILES = {"A01", "A02", "A11", "A16", "A23", "A25", "A26", "N01", "N02", "N03", "N33", "N42"}
SHOP_FIRST = {"A25", "A26", "N33"}
KNOWN_FILES = FOOD_SERVICE_FILES | SHOP_FILES | {"N34"}   # N34 is empty
# Also the owner's canteen and catering exclusions (files 21 and 31) applied
# to rows filed in file 19: "bufet (de) incinta", an in-house buffet (13), and
# a category that is catering alone (2; "restaurant/catering" stays).
# "rulota" (a trailer) and "unitate mobila" (a mobile unit) joined on
# 2026-09-29: seven fast-food rows in numbered sectors whose category says
# mobile, which step 2's sector and address tests miss (owner, DECISIONS
# "Category check: the owner's calls").
NOT_STOREFRONT_CATEGORY = re.compile(r"toneta|automat|laborator|\blab\b|bufet (de )?incinta|^catering$|"
                                     r"rulota|unitate mobil")

# --- Roles, for every county after Bucharest --------------------------------

# role -> bucket. "canteen_catering" is the non-animal list's file of
# canteens, catering and vegan restaurants: its catering and canteen rows fall
# to the category rules below, and what is left (fast food) is Food service.
ROLE_BUCKET = {
    "pork_butcher": "Retail", "butcher": "Retail", "fishmonger": "Retail", "honey_shop": "Retail",
    "confectioner": "Retail", "food_shop": "Retail", "supermarket": "Retail", "bakery": "Retail",
    "pastry_shop": "Retail", "bakery_pastry": "Retail", "retail": "Retail", "frozen_counter": "Retail",
    "restaurant": "Food service", "pizzeria": "Food service", "bar": "Food service",
    "ice_cream": "Food service", "canteen_catering": "Food service",
}
# A premises in one of these is a food shop even with a food-service
# registration (SHOP_FIRST's rule).
ROLE_SHOP_FIRST = {"food_shop", "supermarket", "retail"}
# (pattern on the folded file name, role), first match wins, so the longer
# names come first: "paine_prajituri" before "paine" and "prajituri", the
# frozen counters before plain retail, "cantine" before "restaurant".
ROLE_BY_NAME = (
    (r"carmangerie", "pork_butcher"),
    (r"macelarie", "butcher"),
    (r"peste|pescarie", "fishmonger"),
    (r"miere", "honey_shop"),
    (r"cantin|catering", "canteen_catering"),
    (r"restaurant|alimentatie-publica", "restaurant"),
    (r"pizzer", "pizzeria"),
    (r"cofetarie", "confectioner"),
    (r"supermarket|hipermarket", "supermarket"),
    (r"magazin-alimentar", "food_shop"),
    (r"\bbar\b|baruri", "bar"),
    (r"inghetat", "ice_cream"),
    (r"paine.*prajituri|painii.*prajiturilor", "bakery_pastry"),
    (r"prajituri", "pastry_shop"),
    (r"paine|painii", "bakery"),
    (r"congelate", "frozen_counter"),
    (r"comercializ|comert-cu-amanuntul", "retail"),
)
# The owner's exclusions that Bucharest met as whole files it never fetched
# and Cluj-Napoca meets as category text inside the files it reads (the
# brief's calls 7 to 9, each on its precedent, 2026-10-11): pharmacies (a
# food-only register's pharmacies are out, Stockholm's rule), market and
# street stalls ("stand"; a fixed kiosk, "chiosc", stays, Thessaloniki's
# call), canteens, and catering written with other words than the one
# NOT_STOREFRONT_CATEGORY reads; and the mobile, itinerant and temporary
# units that rule's "rulota" and "unitate mobil" do not spell ("bar mobil",
# "cafenea mobila", "bufet ambulant", "bistro temporar": 9 Cluj premises).
# Applied to role-coded rows only.
NOT_STOREFRONT_CATEGORY_ROLES = re.compile(r"farmaci|\bstand(uri)?\b|cantin|^(unitate de )?catering\b(?!\s*[-/])|"
                                           r"\bmobil[ae]?\b|ambulant|temporar")


# THE NAME RULE'S TWO EXTENSIONS, for every county after Bucharest (owner's
# rule, 2026-09-28 and 2026-09-29: the category alone for a sole trader, or
# for a company named only as a person). Bucharest's step 2 holds the rule
# (SOLE_TRADER, is_person_name); a county's step 2 calls it, then
# `name_kind_extended()` on what it let through. Measured on Cluj-Napoca,
# 2026-10-11, counts only: 10 sole traders written with an abbreviated form
# ("Intrepr.Ind.", "Intr.Fam.", "Intreprind.") passed Bucharest's test, and
# its person-name test, built on Romanian given names and surname endings,
# found none of the 24 names that are a given name beside one other word
# (Transylvanian and Hungarian surnames carry no such ending).
SOLE_TRADER_ABBREVIATED = re.compile(
    r"\bintr(epr(ind(ere(a)?)?)?)?\.?\s*(ind(iv(iduala)?)?|fam(iliala)?)\b\.?|\bintreprind\w*\.?\s*$")
HUNGARIAN_GIVEN_NAMES = set("""istvan laszlo jozsef janos zoltan sandor ferenc gabor attila peter tamas gyula
bela csaba levente zsolt andras imre karoly lajos gyorgy mihaly tibor arpad denes geza balazs botond szabolcs
szilard hunor zsombor lorand lorant ervin erno endre elek kalman marton mate norbert otto pal rudolf vilmos
erzsebet katalin ilona eva zsuzsanna anna margit judit agnes julianna rozalia iren piroska emese eniko reka
timea ildiko kinga noemi melinda edit orsolya csilla aranka gizella terez tunde boglarka hajnal emoke zita
klara magdolna marta monika beata brigitta""".split())
# Words that make a name a business's, not a person's, when they stand beside
# a given name ("Maria Market", "La Mircea"): the name is shown.
BUSINESS_WORDS = set("""la de si cu din pe import export impex com comert prod production trans serv service
services food foods market shop store bar cafe caffe cafenea bistro grill pizza pizzeria restaurant fast
catering casa hanul crama cofetaria patiseria brutaria magazin alimentara fruct legume tour tours travel
group grup holding invest construct design studio media dental farm pharma auto tech soft consulting
distribution trading company international romania transilvania cluj napoca""".split())


def name_kind_extended(name, shown, kind, given_names):
    """Bucharest's verdict on a name, extended: "sole trader" for the
    abbreviated forms, "person-named company" for a shown name that is one or
    two given names (Romanian or Hungarian) beside exactly one other word that
    is no business word. Withholding a brand by mistake shows its category; the
    other mistake shows a person."""
    if kind != "company":
        return kind
    if SOLE_TRADER_ABBREVIATED.search(fold(name)):
        return "sole trader"
    words = [w for w in re.findall(r"[a-z]+", fold(shown)) if len(w) > 1]
    if 2 <= len(words) <= 3:
        given = [w for w in words if w in given_names or w in HUNGARIAN_GIVEN_NAMES]
        rest = [w for w in words if w not in given]
        if given and len(rest) == 1 and len(rest[0]) >= 3 and rest[0] not in BUSINESS_WORDS:
            return "person-named company"
    return kind


def role_for_file(name):
    """The role of a county's file, read from its name; raises on a name no
    pattern reads, so a new kind of file is looked at, not guessed."""
    folded = re.sub(r"[ _.]+", "-", fold(name))
    for pattern, role in ROLE_BY_NAME:
        if re.search(pattern, folded):
            return role
    raise ValueError(f"no DSVSA role reads the file name {name!r} - add it to ROLE_BY_NAME")


def fold(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def legend_label(bucket):
    return {"Retail": "Food shops"}.get(bucket, bucket)


# The layer control names each bucket the way the legend does; until
# 2026-10-07 it said "Retail" beside a legend that says "Food shops".
layer_label = legend_label


# The Retail bucket here is food shops only, so its pins are olive, not retail
# blue (owner, 2026-10-07: one pin colour per meaning; pipeline/taxonomies
# MEANING_COLOURS).
PIN_MEANINGS = {"Retail": "Food shops"}


def classify(row):
    """Bucket for a premises, or None if it is not a tracked storefront."""
    codes = set(filter(None, str(row.get("source_files") or "").split("|")))
    files = {c for c in codes if ":" not in c}
    roles = {c.split(":", 1)[1] for c in codes if ":" in c}
    unknown = (files - KNOWN_FILES) | {c for c in codes if ":" in c and c.split(":", 1)[1] not in ROLE_BUCKET}
    if unknown:
        raise ValueError(f"unknown DSVSA file code(s) {sorted(unknown)}")
    category = fold(row.get(VALUE_COLUMN))
    if NOT_STOREFRONT_CATEGORY.search(category):
        return None
    # A premises is merged from several registrations, its categories joined
    # with " · " (split BEFORE folding, which drops the dot): any one of them
    # naming an excluded kind takes it out.
    if roles and any(NOT_STOREFRONT_CATEGORY_ROLES.search(fold(part))
                     for part in str(row.get(VALUE_COLUMN) or "").split("·")):
        return None
    if files & SHOP_FIRST or roles & ROLE_SHOP_FIRST:
        return "Retail"
    if files & FOOD_SERVICE_FILES or any(ROLE_BUCKET[r] == "Food service" for r in roles):
        return "Food service"
    if files & SHOP_FILES or roles:
        return "Retail"
    return None


assert not FOOD_SERVICE_FILES & SHOP_FILES
