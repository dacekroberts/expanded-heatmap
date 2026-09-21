"""Boston taxonomy - three registries, dispatched on a `source` column, not
NAICS and not one classification field.

Boston licenses food and alcohol and essentially no other trade, so coverage
has to be assembled and it still reaches only two buckets:

  source            registry                                    bucket(s)
  ---------------------------------------------------------------------------
  isd_food          Inspectional Services food establishments   Food service,
                    (CKAN 4582bec6, the 902,651-row inspection   Retail
                    history, filtered to active and collapsed
                    to one row per property_id)
  licensing_board   Licensing Board Licenses (CKAN 04dc653b)     Retail
                    - package stores only
  cannabis          Cannabis Active Licenses (CKAN e395fd88)     Retail

TWO BUCKETS, AND THE MISSING ONE IS ABSENT RATHER THAN THIN. There is no
personal-service licence in Boston at any level of government reachable as
data: Massachusetts licenses cosmetology and barbering at STATE level through
the Board of Registration of Cosmetology and Barbering, and publishes no
address-bearing export - its register is the ePLACE/MADOL portal, a per-licence
lookup with no bulk download. Verified three independent ways on 2026-09-21:
Socrata's cross-domain discovery API returns no Massachusetts source for
cosmetology, barber, salon, hair, nail salon, body art or tattoo; data.mass.gov
is not a data portal at all (HTML 404 from both the Socrata and CKAN entry
points); and opendata.mass.gov does not resolve. Same structural cause as
Philadelphia, which is the only other two-bucket city here. Recorded in
docs/excluded_categories.md under what is MISSING rather than excluded,
because everything else there was a choice and this was not.

THE ONE TRAP THAT WOULD HAVE MADE THIS A ONE-BUCKET CITY. Boston publishes an
"Active Food Establishment Licenses" extract (CKAN f1e13724, 3,345 rows) that
looks like the obvious source and is not: its rows are exactly FS 1,762 + FT
1,583 licences and it contains **no RF (Retail Food) at all**, which is the
entire Retail bucket. The 902,651-row inspection history carries the same
`licensecat` field including RF's 504 active premises, and has better
coordinates too - 99.9% of active premises against 93.8%. Use the history.

A SECOND TRAP, in the names. In the ISD data `dbaname` is blank on 99.0% of
rows while `businessname` is never blank and holds the trade name - the reverse
of every other city in this project. A step 2 copied from elsewhere, preferring
the dba column, would produce almost nothing without failing. The Licensing
Board sets use the normal convention (`dba_name` trades, `business_name` is the
legal entity).
"""

# Source registry keys. Step 2 writes one of these into every row's `source`.
SOURCES = ("isd_food", "licensing_board", "cannabis")

# Which source wins when the same premises appears in several, and which bucket
# wins with it. Package stores are the overlap that matters: a shop holding
# both an RF food licence and a "Retail All Alc." licence is one premises, and
# on 2026-09-21 "Go Fresh 365 / Ming's Supermarket" held both at 1102
# Washington St. ISD first because it has real coordinates in the file rather
# than state-plane values needing reprojection.
SOURCE_PRIORITY = ("isd_food", "licensing_board", "cannabis")

# --- isd_food -------------------------------------------------------------
# `licensecat`, with the `descript` the city pairs with it. All four values
# active on 2026-09-21 carry an explicit verdict.
ISD_BUCKETS = {
    "FS": "Food service",    # "Eating & Drinking"              1,368 premises
    "FT": "Food service",    # "Eating & Drinking w/ Take Out"   1,007 premises
    "RF": "Retail",          # "Retail Food"                       504 premises
    # Mobile Food Walk On - a cart or truck, not a premises. Excluded on the
    # same rule as every other city: permanent fixed premises only. Only 10
    # active premises anyway, and their coordinates are a depot or a permit
    # address rather than where the cart trades.
    "MFW": None,             # "Mobile Food Walk On"                10 premises
}

# --- licensing_board ------------------------------------------------------
# This registry is used for ONE thing: package stores, which is the only part
# of it that is storefront retail and not already covered by ISD.
#
# Only three of its 57 active licence types are kept, so they are listed
# explicitly rather than mapped one-by-one - the rule is "the retail
# off-premises types", not a per-type judgment.
LICENSING_BOARD_KEPT = {
    "Retail All Alc.": "Retail",      # 238 - package stores
    "Retail Malt Wine": "Retail",     #  68 - beer and wine shops
    "Druggist": "Retail",             #   1 - a pharmacy licence under MGL 138
}

# The other 54 types, by why they are out. Enumerated as GROUPS rather than
# individually because they are excluded for four reasons and the reasons are
# what matter; the counts are active licences on 2026-09-21.
#
#   Common Victualler (2,578, 23 variants: "Common Victualler", "CV7 All Alc.",
#     "CV7 Malt Wine Liq.", the Zip/Neighborhood/Airport/South Bay restricted
#     forms, "BYOB")  - these ARE restaurants, and every one of them is already
#     in the ISD food data. Keeping them would double-count the same premises
#     from a second source, which is the whole reason SOURCE_PRIORITY exists.
#   Residential (436: "Dormitory" 282, "Lodging Houses (Frat/Dorm)" 154) - not
#     businesses. The same category of row that is 79% of Philadelphia's
#     register and 49% of D.C.'s.
#   Lodging and clubs (204: "Inn. All Alc.", "Innholder No Liquor", "Clb. All
#     Alc.", the Vet./Airport variants) - hotels and members' clubs, excluded
#     as lodging is in every other city.
#   Recreation, production and the rest (~90: "Billiards/Sippio" 38, "Bowling
#     Alley" 10, the seven Farmer Brewery/Winery/Distillery pouring licences,
#     "Tavern Licenses", "General on Premise" and its variants, "SPCMWA", and
#     "Fortune Teller" 5) - NAICS 713/312 territory, which no bucket covers in
#     any city here.
#
# Kept as a set so step 2 can report any type it has never seen: a new retail
# type added upstream would otherwise be silently dropped.
LICENSING_BOARD_SEEN = frozenset({
    "Common Victualler", "CV7 All Alc.", "CV7 Malt Wine Liq.", "CV7 Malt Wine",
    "CV7 All Alc. Airp.", "CV7ALN - Neighborhood Restricted",
    "CV7 All Alc by Zip Restricted", "CV7 Malt Wine by Zip Restricted",
    "CV7 All Alc. Restrict.", "CV7 Malt Wine Restrict.",
    "CV7 Malt Wine Liq. Restrict.", "CV7 All Alc. (Special Legislation)",
    "CV7 Malt Wine Liq by Zip Restricted", "CV7MWN - Neighborhood Restricted",
    "CV7 All Alc. South Bay Restricted", "BYOB Bring Your Own Bottle",
    "CV7MWLN - Neighborhood Restricted", "CV & All Alc Oak Sq Restricted",
    "CV7 All Alc Comm Spaces Restricted", "CV7 Malt Wine Airp.",
    "Common Victualler 7 Day All-Alcohol Bolling Building Restricted",
    "CV7 All Alc Unrestricted 2024",
    "Common Victualler 7 Day Malt & Wine (South Bay Restricted)",
    "Dormitory", "Lodging Houses (Frat/Dorm)",
    "Retail All Alc.", "Retail Malt Wine", "Druggist",
    "Billiards/Sippio", "Bowling Alley", "Fortune Teller",
    "Famer-Brewery Pouring", "Farmer Brewery,Winery & Distillery License",
    "Farmer Brewery and Winery", "Farmer Distillery Pouring License",
    "Farmer Brewery Distillery Pouring License", "Farmer-Winery Pouring",
    "Tavern Licenses", "SPCMWA",
    "Inn. All Alc.", "Innholder No Liquor", "Inn. All Alc. Restrict.",
    "Innholder Malt & Wine", "INNALN - Neighborhood Restricted",
    "Clb. All Alc.", "Clb. All Alc. Vet.", "Clb. All Alc. Airport",
    "Club Malt, Wine & Liqueur", "Club Malt & Wine",
    "GOP All Alc.", "General On Premise Comm Spaces Restricted",
    "GOP Malt Wine Liq.", "GOP Malt Wine", "Gen Prem All Alcohol Rest",
    "GOPALN - Neighborhood Restricted", "GOP All Alcohol Airport",
})

# --- cannabis -------------------------------------------------------------
CANNABIS_BUCKETS = {
    "Recreational Retail Cannabis Dispensary": "Retail",                  # 34
    "Co-located Recreational and Medical Cannabis Dispensary": "Retail",   #  8
    # A delivery operator has no shopfront - same rule as the mobile food
    # licences above.
    "Delivery (operator)": None,                                          #  1
}

FIELD_LABEL = "Licence category"
VALUE_COLUMN = "business_category"
EXTRA_COLUMNS = ("source",)

# A premises can hold licences in both buckets: 55 hold FS+RF, 31 hold FT+RF
# and 31 hold FS+FT+RF. Food service wins, and the tradeoff is worth stating
# because the sample does not settle it cleanly - the FT+RF group contains
# both eateries ("Bostonian Pizza", "Charley's Philly Steaks") and genuine
# grocers with a hot counter ("Shaw's Supermarkets No. 1208", "Jhade
# Supermarket", "Ramirez Grocery"). FS/FT is a prepared-food licence, so a
# premises holding one is serving food to the public, which is what this
# bucket means. The consequence, stated rather than hidden: **Retail is
# slightly undercounted**, by roughly the number of supermarkets that also
# run a kitchen.
BUCKET_PRIORITY = ["Food service", "Retail"]


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Dispatch on `source` to that registry's mapping.

    Expects `business_category` (each source's own category string, normalised
    by step 2) and `source` (one of SOURCES). An unknown source returns None
    rather than guessing, and step 2 reports it.
    """
    source = (row.get("source") or "").strip()
    raw = row.get(VALUE_COLUMN)
    if not source or raw is None:
        return None
    value = str(raw).strip()
    if source == "isd_food":
        return ISD_BUCKETS.get(value.upper())
    if source == "licensing_board":
        return LICENSING_BOARD_KEPT.get(value)
    if source == "cannabis":
        return CANNABIS_BUCKETS.get(value)
    return None
