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


def fold(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def legend_label(bucket):
    return {"Retail": "Food shops"}.get(bucket, bucket)


def classify(row):
    """Bucket for a premises, or None if it is not a tracked storefront."""
    files = set(filter(None, str(row.get("source_files") or "").split("|")))
    unknown = files - KNOWN_FILES
    if unknown:
        raise ValueError(f"unknown DSVSA file code(s) {sorted(unknown)}")
    if NOT_STOREFRONT_CATEGORY.search(fold(row.get(VALUE_COLUMN))):
        return None
    if files & SHOP_FIRST:
        return "Retail"
    if files & FOOD_SERVICE_FILES:
        return "Food service"
    if files & SHOP_FILES:
        return "Retail"
    return None


assert not FOOD_SERVICE_FILES & SHOP_FILES
