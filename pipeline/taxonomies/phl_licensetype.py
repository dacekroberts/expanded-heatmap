"""Philadelphia taxonomy - the `licensetype` field from L&I's business
license data, not NAICS.

Source: "Licenses and Inspections Business Licenses" (Carto SQL API,
phl.carto.com, table `business_licenses`). No NAICS field exists anywhere in
its 48 columns; the classification field is `licensetype`.

VERIFIED 2026-09-21 against the full distinct-value pull (all 50 licence types
active at that date, not a sample). Every type below carries an explicit
verdict - a bucket or None - so a later reader can tell "checked, not a match"
from "not yet checked". Unknown types classify as None, and step 2 prints any
it meets, so an upstream rename surfaces instead of silently dropping rows.

TWO BUCKETS, NOT THREE. Philadelphia licenses no personal-service business:
an ILIKE sweep for hair / barber / salon / nail / cosmet / massage / tattoo /
laundry across this table and the older `li_business_licenses` returns nothing,
Pennsylvania publishes professional licensees only as county aggregates
(data.pa.gov fwj2-whnj, no addresses), and the state board's PALS system is a
per-licence lookup with no bulk export. So Personal services is **absent, not
thin** - there is no source to add. That is a fact about Philadelphia's
licensing, and the city page and docs/excluded_categories.md say so under what
is *missing* rather than *excluded*, because everything else was a choice and
this was not. See docs/city_shortlist.md and the `multi-source-city` skill,
whose Step 2 archetypes all failed here.

Two findings from hand-sampling that a licence type's NAME does not give you,
both of which had my first guess backwards:

  "Vendor - Motor Vehicle Sales" is NOT car dealers. It licenses vending FROM
  a motor vehicle: the sampled holders are "CHA CHA LUNCH TRUCK", "FOOD TRUCK
  COLLECTIVE LLC", "Saijai Thai Food LLC". Mobile, so excluded - not Retail.

  "Food Establishment, Retail Perm Location (Large)" is the general-retail
  tier, not supermarkets only: Target, CVS, Dollar Tree, Staples, Ross Dress
  For Less. They hold a food licence because they sell packaged food, and it
  is the only way this city's data sees a chain clothing or office-supply
  store at all.
"""

# licensetype (exact string, uppercased) -> bucket name from
# pipeline.taxonomies.CATEGORY_BUCKETS, or None for "checked, not storefront
# commercial for this project's purposes".
#
# The grouping follows the same lines the NAICS cities use, so the buckets mean
# the same thing across the project (see naics.py's NAICS_GROUPS):
#   Retail        = NAICS 44/45 minus 454 nonstore
#   Food service  = NAICS 722
#   permanent, fixed premises only - mobile and sidewalk retail is NAICS 454,
#   which every city here excludes, and auto repair is NAICS 811, which no
#   city here maps.
LICENSETYPE_TO_BUCKET = {
    # --- Food service -----------------------------------------------------
    "FOOD PREPARING AND SERVING": "Food service",              # 4,277
    "FOOD PREPARING AND SERVING (30+ SEATS)": "Food service",  # 2,656
    "FOOD CATERER": "Food service",                            # 229
    # Adjunct: held BY a restaurant that already holds a primary food licence
    # at the same address, so step 2's one-row-per-site collapse ranks these
    # last (LICENSE_PRIORITY in config.py) and they add a pin only where no
    # primary licence names the site. Same idea as Chicago's TOBACCO licence.
    "SIDEWALK CAFE": "Food service",                           # 284
    "STREETERY LICENSE": "Food service",                       # 32
    "FOOD ESTABLISHMENT, OUTDOOR": "Food service",             # 7

    # --- Retail -----------------------------------------------------------
    # Philadelphia splits food PREPARING (restaurants, above) from food
    # ESTABLISHMENT, RETAIL (shops that sell food), which is the grocery slice
    # New York needed a separate state registry for. Sampled holders are
    # bodegas, mini-markets, beer distributors and live-poultry shops.
    "FOOD ESTABLISHMENT, RETAIL PERMANENT LOCATION": "Retail",      # 1,052
    "FOOD ESTABLISHMENT, RETAIL PERM LOCATION (LARGE)": "Retail",   # 385
    "CURB MARKET": "Retail",                                        # 31
    "VENDOR - NEWSSTAND": "Retail",                                 # 75
    "TIRE DEALER": "Retail",                                        # 83
    "PRECIOUS METAL DEALER": "Retail",                              # 78
    "PAWN SHOP": "Retail",                                          # 11

    # --- Checked, deliberately NOT mapped ---------------------------------
    # Residential registrations. The largest type in the file by far and the
    # reason an unfiltered map of "active licences" would be wrong: on these
    # rows business_name holds the OWNER'S OWN NAME at their property
    # ("ROY E EGNER", "PETER MIRABELLI"), with legalentitytype='Individual'.
    # Mapping them would publish ~94k individuals at their addresses. Excluded
    # as a scope error first - they are not businesses and not storefronts -
    # which is the easier call to justify and fixes the privacy problem too.
    "RENTAL": None,                                     # 93,471
    "LIMITED LODGING OPERATOR": None,                   # 589 (short-let hosts)
    "LIMITED LODGING AND HOTELS BOOKING AGENT": None,   # 4
    "RESIDENTIAL PROPERTY WHOLESALER": None,            # 13
    "VACANT RESIDENTIAL PROPERTY / LOT": None,          # 1,801
    "VACANT COMMERCIAL PROPERTY": None,                 # 24 (a vacancy, not a business)

    # Mobile / sidewalk trade. NAICS 454 nonstore, which is excluded for every
    # city in this project (see naics.py) - a cart is not a storefront. Note
    # that mobile FOOD is here too, despite NAICS 722330 sitting inside the
    # Food service prefix, because "permanent premises" is the line this city's
    # data actually lets us draw and the licence types name it explicitly.
    "FOOD ESTAB, RETAIL NON-PERMANENT LOCATION (ANNUAL)": None,  # 689
    "FOOD ESTAB, RETAIL NON-PERMANENT LOCATION (EVENT)": None,   # 21
    "VENDOR - MOTOR VEHICLE SALES": None,               # 279 (food trucks - see docstring)
    "VENDOR - SIDEWALK SALES": None,                    # 283
    "VENDOR - CENTER CITY VENDOR": None,                # 77
    "VENDOR - NEIGHBORHOOD VENDING DISTRICT": None,     # 54
    "VENDOR - SPECIAL VENDING": None,                   # 8
    "VENDOR - PUSHCART": None,                          # 7
    "VENDOR - ON FOOT": None,                           # 7
    "HONOR BOX": None,                                  # 19 (vending machines, NAICS 454210)

    # Vehicle repair and trade. NAICS 811, which no city here maps. The
    # sampled holders are auto body and repair shops ("KONNY'S AUTO BODY",
    # "DON'S AUTO & TRUCK REPAIRS"); the type conflates them with fuel
    # dispensing (NAICS 447, Retail) and the data cannot separate the two, so
    # the whole type goes rather than guessing.
    "MOTOR VEHICLE REPAIR / FUEL DISPENSING": None,     # 1,116
    "AUTO WRECKING / WASTE HANDLING": None,             # 83
    "TOW TRUCK": None,                                  # 378
    "TOW COMPANY": None,                                # 102
    "PUBLIC GARAGE / PARKING LOT": None,                # 168 (NAICS 81293, excluded project-wide)

    # A permission a site holds, not a business at it. Excluded outright
    # rather than ranked adjunct, because unlike a sidewalk cafe these do not
    # imply any storefront: a dumpster permit attaches to a building.
    "DUMPSTER LICENSE - PRIVATE PROPERTY": None,        # 8,389
    "DUMPSTER LICENSE - PUBLIC ROW": None,              # 182
    "DUMPSTER LICENSE - CONSTRUCTION": None,            # 21
    "HAZARDOUS MATERIALS": None,                        # 460
    "HIGH RISE": None,                                  # 329
    "HOT WORK": None,                                   # 38
    "SPECIAL PERMIT": None,                             # 10
    "OUTDOOR ADVERTISING SIGN": None,                   # 6

    # Not retail, food service or personal services under any of the three
    # buckets' NAICS definitions.
    "FOOD MANUFACTURER / WHOLESALER": None,             # 141 (NAICS 311/424)
    "CHILD CARE FACILITY": None,                        # 205 (NAICS 6244)
    "SPECIAL ASSEMBLY OCCUPANCY": None,                 # 126 (venues, NAICS 71)
    "HANDBILL DISTRIBUTION": None,                      # 129 (an activity)
    "PROMOTER REGISTRATION": None,                      # 11
    "ANNUAL SMALL GAMES OF CHANCE": None,               # 75 (held by clubs and bars)
    "MONTHLY SMALL GAMES OF CHANCE": None,              # 1
    "BINGO": None,                                      # 19
}

# Licence types that are a permission held BY an already-licensed business at
# the same address rather than a business in their own right. Step 2 ranks
# these last when collapsing to one row per site, so a restaurant with a
# sidewalk cafe is counted once, as a restaurant. Exposed here rather than in
# config.py because which types are adjunct is a property of the taxonomy.
ADJUNCT_LICENSETYPES = frozenset({
    "SIDEWALK CAFE",
    "STREETERY LICENSE",
    "FOOD ESTABLISHMENT, OUTDOOR",
})

FIELD_LABEL = "License type"
VALUE_COLUMN = "licensetype"


def legend_label(bucket: str) -> str:
    return bucket


def is_adjunct(license_type: str) -> bool:
    return (license_type or "").strip().upper() in ADJUNCT_LICENSETYPES


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).
    `row` must carry a `licensetype` key."""
    license_type = (row.get("licensetype") or "").strip().upper()
    if not license_type:
        return None
    return LICENSETYPE_TO_BUCKET.get(license_type)
