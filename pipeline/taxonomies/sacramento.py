"""Sacramento taxonomy - the City's own Business_Description (Business
Operation Tax register), mapped by hand against docs/category_rules.md.

148 descriptions exist; the in-city, Active, unexpired rows use 141 (read
2026-09-29). Values not listed here are excluded (classify() returns None):
offices, professions, contractors, wholesale, health care, lodging,
recreation, vehicles and the rest are outside the three buckets. The
exclusions that are storefront-shaped, and why, are EXCLUDED below and in
docs/excluded_categories.md.
"""

VALUE_TO_BUCKET = {
    # Retail (NAICS 44-45 in substance)
    "RETAIL SALES - GENERAL": "Retail",
    "CONVENIENCE STORE": "Retail",
    "GROCERY STORE/SUPERMARKETS": "Retail",
    "LIQUOR STORE": "Retail",
    "TOBACCO PRODUCTS": "Retail",
    "DRUGS STORES & PHARMACIES": "Retail",
    "SECONDHAND DEALERS & STORES": "Retail",
    "DEPARTMENT STORE": "Retail",
    "PAWNBROKERS": "Retail",                     # category_rules R5
    "AUTOMOBILE DEALERS - NEW / USED": "Retail",  # R4
    "AUTOMOBILE DEALERS - USED": "Retail",       # R4
    "AUTOMOTIVE - PARTS": "Retail",              # parts stores, NAICS 441330
    "SERVICE STATIONS": "Retail",                # petrol stations, R4
    "CANNABIS - DISPENSARY": "Retail",           # Boston's cannabis retail precedent
    "FIREARMS SALES": "Retail",
    "ART DEALER - STUDIO": "Retail",             # NAICS 459920 art dealers
    # Food service (NAICS 722)
    "RESTAURANTS": "Food service",
    "CAFES": "Food service",
    "BARS - TAVERNS": "Food service",
    "BAKERY": "Food service",
    # A catch-all inside food, hand-sampled 2026-09-29: coffee roasters, pho,
    # doughnuts, juice bars, franchise pizza and sandwiches - kept as food.
    "FOOD - OTHER": "Food service",
    # Personal services (NAICS 812)
    "BEAUTY - PARLORS & SHOPS": "Personal services",
    "BARBERSHOPS": "Personal services",
    "MASSAGE - ESTABLISHMENT": "Personal services",   # commercial massage, kept
    "TATTOO PARLOR/ARTIST": "Personal services",      # tattoo has its own code here
    "LAUNDRY SERVICES": "Personal services",
    "LAUNDROMATS - SELF SERVICE": "Personal services",
    # Groomers, daycares and pet shops (hand-sampled): NAICS 812910 pet care.
    "PET CARE/GROOMING/BOARDING/SUPPLIES": "Personal services",
}

# Storefront-shaped descriptions left out, with the rule that decides each.
EXCLUDED = {
    "SERVICE - GENERAL": "catch-all, no bucket (656 in-city rows)",
    "OTHER": "catch-all, no bucket (345)",
    "CATERING": "food with no counter of its own (category_rules R1)",
    "MOBILE VENDOR - FOOD": "mobile unit",
    "MOBILE VENDOR - ICE CREAM": "mobile unit",
    "SIDEWALK VENDOR - FOOD": "street stall",
    "SIDEWALK VENDOR - MERCHANDISE": "street stall",
    "COTTAGE FOOD OPERATION": "a home kitchen",
    "RETAIL SALES - ONLINE": "nonstore retail (NAICS 454)",
    "VENDING MACHINES": "nonstore retail",
    "BEAUTY - INDEPENDENT STYLIST": "a person working in another's shop (New York's renter rule)",
    "MASSAGE - TECHNICIAN": "a person, not a premises (as above)",
    "CLOTHING ALTERATIONS, &TAILORS SHOPS": "repairs (NAICS 811, not 812)",
    "DRESSMAKING & SEWING": "repairs and custom work (NAICS 811)",
    "ELECTRONICS & REPAIRS": "repairs (NAICS 811)",
    "APPLIANCES, SALES & SERVICE": "repairs (NAICS 811)",
    "OFFICE SUPPLIES": "business-to-business (hand-sampled: IBM, Xerox, office systems)",
    "MEDICAL SUPPLIES": "business-to-business and health care (hand-sampled)",
    "ADULT ENTERTAINMENT": "adult venues (R3)",
    "ENTERTAINMENT": "recreation and events (NAICS 71)",
    "LIVE ENTERTAINMENT": "recreation (NAICS 71)",
    "FUNERAL HOME & CREMATORY": "funeral services",
    "PET CREMATION SERVICES": "funeral services",
    "SEASONAL LOTS": "a temporary lot, not a premises",
    "CARDROOMS": "gambling (R5)",
    "PARKING LOTS/SERVICES": "parking",
}

FIELD_LABEL = "Business description"
VALUE_COLUMN = "business_category"


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    value = (row.get(VALUE_COLUMN) or "").strip().upper()
    if not value:
        return None
    return VALUE_TO_BUCKET.get(value)
