"""Calgary's `licencetypes` - 96 categories, and the only register in this
project that names premises itself.

WHY THIS ONE IS EASIER THAN IT LOOKS
------------------------------------
96 categories sounds like Miami's 150 or Surrey's 210, but Calgary does most of
the classifying for you. It suffixes its own categories with the thing every
other city has to infer:

    - PREMISES          a fixed place the public enters
    - NO PREMISES       no fixed place
    (MOBILE)            travels to the customer
    (HOME BASED)        someone's home
    (MAIL ORDER)        nonstore
    (DIRECT SALES)      nonstore

So `RETAIL DEALER - PREMISES` (7,516) and `RETAIL DEALER - NO PREMISES` (7) are
the same trade, split by the City into the thing this project maps and the
thing it does not. That is why Calgary's published ranking figure was inflated
only 1.4x where Vancouver's was 4.2x - the register was already premises-shaped.

**Every suffix is honoured, including where it contradicts the base
category.** `RETAIL DEALER - PREMISES (MAIL ORDER)` (59) is excluded despite
saying PREMISES, because mail order is NAICS 454 nonstore, which this project
excludes for every city. The suffix nearest the actual trade wins.

BUCKETS ANCHORED ON naics.py, as every non-NAICS city here is:
    Retail             NAICS 44-45, less 454 nonstore
    Food service       NAICS 722
    Personal services  NAICS 812, less 81293 parking

FIVE JUDGMENT CALLS, EACH MET BEFORE IN THIS PROJECT
----------------------------------------------------
1. **`ALCOHOL BEVERAGE SALES (*)` and `OUTDOOR PATIO` are ENDORSEMENTS, not
   businesses** - 2,180 and 937 rows. A premises holding one already holds a
   `FOOD SERVICE - PREMISES` licence, so counting them would count one
   restaurant twice. This is D.C.'s endorsement problem, and it is why
   Calgary's multi-category rows exist at all: 9,136 of 23,203 rows carry more
   than one category, mostly a premises licence plus its endorsements.

2. **`PERSONAL SERVICE (INDEPENDENT CHAIR OPERATOR)` (160) is dropped.** A
   chair renter inside someone else's salon is a person, not a storefront, and
   counting them double-counts the salon. New York drops its NYS
   `DOSAERENTER`/`DOSBARSHOPOWNER` split for exactly this reason.

3. **`MASSAGE CENTRE (COMMERCIAL)` (917) COUNTS, although Vancouver's
   `Massage Therapy (RMT)` does not.** The difference is real and legal:
   massage therapy is a regulated health profession in British Columbia and is
   **not regulated in Alberta**, so Alberta's massage premises are NAICS 812199
   personal care rather than 621 health care. The same rule put Edmonton's
   `Health Enhancement Centre` in Personal services.

4. **`PERSONAL SERVICE (FITNESS CONDITIONING)` (257) is excluded**, as
   Vancouver's `Fitness Centre` was: NAICS 713940, arts/recreation, which is
   not one of the three buckets.

5. **BODY RUB CENTRES AND ESCORT SERVICES ARE EXCLUDED** - `BODY RUB CENTRE`
   (35), `BODY RUB CENTRE (GRANDFATHERED MASSAGE CENTRE COMMERCIAL)` (45),
   `EXOTIC ENTERTAINMENT AGENCY` (8) and `DATING SERVICE OR ESCORT SERVICE`
   (1), 89 rows in total. These ARE licensed commercial premises and a
   NAICS-only reading would keep the first two, so this is a departure. It
   follows Vancouver, where `Adult Services` was excluded on the same
   reasoning: mapping adult-services premises adds sensitivity for the people
   working there without adding anything to the question this project asks.
   **A reversible call** - the categories are listed here, not deleted, so
   flipping them to PERSONAL is a one-line change if the owner prefers.

Measured 2026-09-21 on all 23,203 rows.
"""

FIELD_LABEL = "Licence type"
VALUE_COLUMN = "licencetype"

# A premises holding several categories - 9,136 of 23,203 rows - resolves to
# one. Most specific first, most generic last: `RETAIL DEALER - PREMISES` is
# Calgary's broadest storefront label and behaves like a default, so a
# restaurant or a salon at the same address wins over it.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]

RETAIL = "Retail"
FOOD = "Food service"
PERSONAL = "Personal services"


def legend_label(bucket: str) -> str:
    """Taxonomy-module interface: legend text for a bucket. A local taxonomy
    returns the bucket name unchanged - there is no prefix list to append, and
    the registry's own wording appears in the tooltip instead."""
    return bucket


BUCKETS = {
    # --- Retail (NAICS 44-45) ---------------------------------------------
    "RETAIL DEALER - PREMISES": RETAIL,                 # 7,516
    "TOBACCO RETAILER": RETAIL,                         #   913
    "VAPE RETAILER": RETAIL,                            #   653
    "MOTOR VEHICLE DEALER - PREMISES": RETAIL,          #   540
    "LIQUOR STORE": RETAIL,                             #   429
    "SECONDHAND DEALER": RETAIL,                        #   349
    "FUEL SALES/STORAGE": RETAIL,                       #   300  NAICS 457
    "CANNABIS STORE": RETAIL,                           #   187
    "MARKET": RETAIL,                                   #    54
    "PAWNBROKER": RETAIL,                               #     7  regulated slice
    "PAWNBROKER (GRANDFATHERED)": RETAIL,               #     7
    "RETAIL DEALER - FIREARMS/AMMUNITION": RETAIL,      #     7

    # --- Food service (NAICS 722) -----------------------------------------
    "FOOD SERVICE - PREMISES (SEATING)": FOOD,          # 3,539
    "FOOD SERVICE - PREMISES": FOOD,                    # 2,591
    "FOOD SERVICE - PREMISES (NO SEATING)": FOOD,       # 1,058

    # --- Personal services (NAICS 812) ------------------------------------
    "PERSONAL SERVICE": PERSONAL,                       # 2,103
    "MASSAGE CENTRE (COMMERCIAL)": PERSONAL,            #   917  call 3
    "PERSONAL SERVICE (TATTOO)": PERSONAL,              #   234
    "PERSONAL SERVICE (MICROBLADING)": PERSONAL,        #    97
    "FABRIC CLEANING": PERSONAL,                        #    81  NAICS 81232
    "KENNEL SERVICE/PET DEALER": PERSONAL,              #    68  NAICS 81291
    "PERSONAL SERVICE (PIERCING) (TATTOO)": PERSONAL,   #    23
    "PERSONAL SERVICE (PIERCING)": PERSONAL,            #    11

    # --- Endorsements, not businesses (call 1) ----------------------------
    "ALCOHOL BEVERAGE SALES (RESTAURANT)": None,            # 1,527
    "OUTDOOR PATIO": None,                                  #   937
    "ALCOHOL BEVERAGE SALES (DRINKING EST/RESTAURANT)": None,  # 446
    "ALCOHOL BEVERAGE SALES (ACCESSORY)": None,             #   171
    "ALCOHOL BEVERAGE SALES (DRINKING ESTABLISHMENT)": None,  #  36

    # --- Wholesale, manufacturing, warehousing, distribution --------------
    "WHOLESALER": None,                                 # 2,025
    "MANUFACTURER": None,                               # 1,640
    "WAREHOUSING": None,                                #   364
    "DISTRIBUTION MANAGER": None,                       #   107
    "ALCOHOL BEVERAGE MANUFACTURER": None,              #    67  NAICS 312
    "SALVAGE YARD/AUTO WRECKER": None,                  #    64
    "SALVAGE COLLECTOR (NO SALVAGE STORAGE WITHIN CALGARY)": None,  # 52
    "CONTAINER DEPOT": None,                            #    27
    "DISTRIBUTION MANAGER (FOOD PRODUCTS)": None,       #    21
    "DISTRIBUTION MANAGER (DIRECT SALES)": None,        #    20
    "CANNABIS FACILITY": None,                          #     9  production
    "WHOLESALER - FIREARMS/AMMUNITION": None,           #     6
    "DISTRIBUTION MANAGER (FOOD PRODUCTS) (DIRECT SALES)": None,  # 3
    "MANUFACTURER - FIREARMS/AMMUNITION": None,         #     2

    # --- Construction and trades (NAICS 23) -------------------------------
    "CONTRACTOR (NO PROVINCIAL LICENCE REQUIRED)": None,  # 1,617
    "CONTRACTOR": None,                                 # 1,072

    # --- Repair and maintenance (NAICS 811, NOT 812) ----------------------
    # The same line Vancouver and Surrey draw: a hairdresser counts and a
    # vehicle repairer does not, because NAICS separates 811 repair from 812
    # personal care and only 812 is a bucket here.
    "MOTOR VEHICLE REPAIR AND SERVICE (1)": None,       # 1,189
    "AUTO BODY SHOP": None,                             #   229
    "MOTOR VEHICLE REPAIR AND SERVICE (2-PROV N/R)": None,  # 211
    "FURNITURE REFINISHING": None,                      #    17
    "MOTOR VEHICLE REPAIR AND SERVICE (MOBILE) (HOME BASED)": None,  # 4
    "MOTOR VEHICLE REPAIR AND SERVICE (MOBILE WASH)": None,  #  3
    "AUTO BODY SHOP (MOBILE PAINT REPAIR)": None,       #     2
    "AUTO BODY SHOP (MOBILE DENT REPAIR)": None,        #     1

    # --- Residential tenancy and lodging (NAICS 531 / 721) ----------------
    "APARTMENT BUILDING OPERATOR (1 TO 3 STOREYS)": None,   # 890
    "APARTMENT BUILDING OPERATOR (4 OR MORE STOREYS)": None,  # 379
    "HOTEL/MOTEL": None,                                #    98  NAICS 721
    "LODGING HOUSE": None,                              #    33

    # --- Education (NAICS 61) ---------------------------------------------
    "SCHOOL (PROV. NOT REQUIRED)": None,                #   421
    "SCHOOL (PROV. APPROVED)": None,                    #    57
    "SCHOOL (DRIVER EDUCATION)": None,                  #    42

    # --- Arts, entertainment, recreation (NAICS 71) -----------------------
    "ENTERTAINMENT ESTABLISHMENT": None,                #   458
    "PERSONAL SERVICE (FITNESS CONDITIONING)": None,    #   257  call 4
    "AMUSEMENT ARCADE": None,                           #    74
    "TRADE SHOW (FACILITY)": None,                      #    22
    "CINEMA": None,                                     #    13
    "CONCERT FACILITY": None,                           #     2
    "PERSONAL SERVICE (MOBILE) (FITNESS CONDITIONING)": None,  # 3

    # --- Services that travel to the customer, or have no premises --------
    # Calgary states this itself; the project excludes nonstore trade for
    # every city on the NAICS 454 reasoning.
    "CLEANING SERVICE (COMMERCIAL & RESIDENTIAL)": None,  # 108
    "CLEANING SERVICE (COMMERCIAL ONLY)": None,         #    67
    "RETAIL DEALER - PREMISES (MAIL ORDER)": None,      #    59  see docstring
    "FULL SERVICE FOOD VEHICLE": None,                  #    50
    "MOTOR VEHICLE DEALER - NO PREMISES": None,         #    42
    "FOOD SERVICE - NO PREMISES": None,                 #    27
    "CLEANING SERVICE (RESIDENTIAL ONLY)": None,        #    18
    "ADVERTISER CANVASSER OR DISTRIBUTOR": None,        #     9
    "RETAIL DEALER - NO PREMISES": None,                #     7
    "CLEANING SERVICE (COMMERCIAL & RESIDENTIAL) (DIRECT SALES)": None,  # 6
    "FULL SERVICE FOOD VEHICLE (PRIVATE PROPERTY)": None,  #  4
    "CLEANING SERVICE (COMMERCIAL & RESIDENTIAL) (PRESSURE WASHING)": None,  # 4
    "MASSAGE CENTRE (HOME BASED)": None,                #     3
    "PERSONAL SERVICE (MOBILE)": None,                  #     3
    "BICYCLE COURIER AGENCY": None,                     #     3
    "CLEANING SERVICE (RESIDENTIAL ONLY) (DIRECT SALES)": None,  # 2
    "CLEANING SERVICE (RESIDENTIAL ONLY) (PRESSURE WASHING)": None,  # 1
    "FOOD SERVICE - NO PREMISES (NON-RES)": None,       #     1

    # --- Professional, financial, security, organisations -----------------
    "CHARITABLE ORGANIZATION": None,                    #   370  NAICS 813
    "ALARM AGENCY": None,                               #   116
    "PHOTOGRAPHER": None,                               #    76  NAICS 5419
    "PAYDAY LENDER (GRANDFATHERED)": None,              #    15  NAICS 522
    "SECURITY CONSULTING AGENCY": None,                 #     8
    "PAYDAY LENDER": None,                              #     3
    "PSYCHIC PRACTITIONER": None,                       #     4

    # --- Excluded on sensitivity as well as scope (call 5) ----------------
    "BODY RUB CENTRE (GRANDFATHERED MASSAGE CENTRE COMMERCIAL)": None,  # 45
    "BODY RUB CENTRE": None,                            #    35
    "EXOTIC ENTERTAINMENT AGENCY": None,                #     8
    "DATING SERVICE OR ESCORT SERVICE": None,           #     1

    # --- The chair renter (call 2) ----------------------------------------
    "PERSONAL SERVICE (INDEPENDENT CHAIR OPERATOR)": None,  # 160
}


# THE STRUCTURAL PRIVACY CLAIM, ENFORCED RATHER THAN ASSERTED.
#
# Every category this module buckets is one the City itself marks as having
# premises - either explicitly (`- PREMISES`, `(COMMERCIAL)`) or by having its
# mobile/home-based/nonstore variant exist SEPARATELY and be excluded
# (`PERSONAL SERVICE` is bucketed; `PERSONAL SERVICE (MOBILE)` and `MASSAGE
# CENTRE (HOME BASED)` are not). So no mapped pin can sit in a category
# Calgary describes as operating from a home or a vehicle.
#
# That matters because `scripts/check_personal_exposure.py` reports 0.00% "at a
# residential unit" for this city, and that figure is a MEASUREMENT GAP -
# Calgary's `address` carries no unit designators to match, exactly as Boston's
# and Montréal's do not. What limits the real exposure is this guard, not that
# reading. Boston makes the same argument from its licence types; Calgary can
# make it from the category strings themselves.
_NONSTORE_MARKERS = ("NO PREMISES", "(MOBILE)", "(HOME BASED)",
                     "(MAIL ORDER)", "(DIRECT SALES)")
_bucketed_nonstore = sorted(
    name for name, bucket in BUCKETS.items()
    if bucket is not None and any(m in name for m in _NONSTORE_MARKERS)
)
if _bucketed_nonstore:
    raise AssertionError(
        f"These categories are bucketed but the City marks them as not having "
        f"premises: {_bucketed_nonstore}. Either the suffix means something "
        f"else here, or a verdict is wrong - decide explicitly, because the "
        f"city page and DECISIONS.md both rest on no mapped pin being "
        f"home-based or mobile."
    )


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).

    `row` must carry a `licencetype` key holding ONE of Calgary's categories.
    Step 2 splits the raw `",\\n"`-delimited `licencetypes` and resolves to a
    single winner before calling this.

    RAISES on an unknown category rather than returning None: a value this
    module has never seen is a data change to look at, not something to drop
    silently from the map. Same convention as dc_businessactivity and
    pipeline/taxonomies/vancouver.
    """
    value = row.get(VALUE_COLUMN)
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    if value not in BUCKETS:
        raise KeyError(
            f"Calgary: licence type {value!r} is not in this module's mapping. "
            f"Add it with a bucket or an explicit None (and a comment saying "
            f"why) rather than letting an unreviewed category onto the map. "
            f"Note the raw column is ',\\n'-delimited - if this value looks "
            f"like several categories at once, step 2 failed to split it."
        )
    return BUCKETS[value]
