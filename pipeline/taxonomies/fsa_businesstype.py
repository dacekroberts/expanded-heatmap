"""The UK Food Standards Agency's FHRS business types - the food-hygiene
register's own classification, not NAICS. London is the first city on it.

**ONE REGISTER, FOOD ONLY.** Every row is a food business the local authority
inspects, so there is no Personal services bucket, and "Retail" here is FOOD
retail only (grocers, off-licences, bakers, butchers, newsagents with food,
supermarkets). Its legend reads "Food shops", the Japanese cities' precedent
for a food-only retail layer (owner, 2026-09-27), never "Retail" or "Shops".

**FOURTEEN TYPES, ALL MAPPED** - the full distinct list, measured on London's
33 authority files 2026-09-28 (81,529 rows). Five are storefronts; nine are
not premises a passer-by walks into, or are premises of another kind:

  Restaurant/Cafe/Canteen 27,262 · Takeaway/sandwich shop 9,430 ·
  Pub/bar/nightclub 3,866                          -> Food service
  Retailers - other 16,733 · Retailers - supermarkets/hypermarkets 2,319
                                                   -> Retail ("Food shops")
  Other catering premises 8,053 (home caterers, event and contract kitchens;
  35.6% placed) · Mobile caterer 2,595 · Hospitals/Childcare/Caring 4,682 ·
  School/college/university 3,501 · Hotel/bed & breakfast/guest house 972 ·
  Manufacturers/packers 1,136 · Distributors/Transporters 669 ·
  Importers/Exporters 278 · Farmers/growers 33      -> excluded

"Other catering premises" and "Mobile caterer" are also where home-based
businesses sit - the owner's rule (2026-09-28): a trade name is shown, never a
person's own name at what looks like their home.

`Restaurant/Cafe/Canteen` includes workplace and institutional canteens
(at least 2.5% by name); that is a per-city question for step 2, not a
classification one.
"""

FIELD_LABEL = "FSA business type"
VALUE_COLUMN = "BusinessType"

VALUE_TO_BUCKET = {
    "Restaurant/Cafe/Canteen": "Food service",
    "Takeaway/sandwich shop": "Food service",
    "Pub/bar/nightclub": "Food service",
    "Retailers - other": "Retail",
    "Retailers - supermarkets/hypermarkets": "Retail",
}

# Every other type the register uses, so a NEW type fails loudly in step 2
# rather than being dropped as "not a storefront" without anyone reading it.
EXCLUDED_TYPES = {
    "Other catering premises",
    "Mobile caterer",
    "Hospitals/Childcare/Caring Premises",
    "School/college/university",
    "Hotel/bed & breakfast/guest house",
    "Manufacturers/packers",
    "Distributors/Transporters",
    "Importers/Exporters",
    "Farmers/growers",
}
KNOWN_TYPES = set(VALUE_TO_BUCKET) | EXCLUDED_TYPES


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
    """Bucket for a row, or None if it is not a tracked storefront."""
    return VALUE_TO_BUCKET.get((row.get(VALUE_COLUMN) or "").strip())


assert not set(VALUE_TO_BUCKET) & EXCLUDED_TYPES
