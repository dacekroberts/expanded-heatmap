"""Edmonton's `business_licence_category` - 60 categories on the Commercial set.

WHY EDMONTON IS THE CHEAPEST CANADIAN REGISTER SO FAR
-----------------------------------------------------
Two things the other five Canadian candidates make you infer, Edmonton states:

1. **`licencetype` says whether a licence is a premises or a person.**
   `Commercial` (25,105) against `Home Based` (14,114), `Non-Resident`
   (2,108), `Massage Practitioner` (1,582) and `Adult Services` (763). That is
   Surrey's shape, so **no residence inference is needed** - the expensive part
   of the Vancouver build. Step 2 keeps `Commercial` and this module is only
   ever asked about those rows.
2. **The publisher redacts individuals' addresses itself.**
   `<REDACTED FOR PRIVACY>` stands in for the address on 4,074 rows (9.3%),
   and on the individual-held licence types it is near total - all 25
   `Health Enhancement Practitioner (Accredited)` rows carry it. That is
   `read-licence` step 6b: the privacy work was done upstream, so those rows
   cannot be mapped rather than needing to be suppressed.

ONE ROW PER PREMISES, SO ENDORSEMENTS CANNOT DOUBLE-COUNT
---------------------------------------------------------
This is the structural difference from Calgary and it makes the endorsement
problem disappear. Calgary emits one row per category, so an alcohol
endorsement is a second row that has to be dropped. **Edmonton emits one row
per licence with a `";"`-delimited category list** - 5,340 of 25,105 carry more
than one - so an endorsement is a second *string* on the same row. The pin
exists once either way; the category list only decides which bucket labels it.

That is why `Alcohol Sales (Consumption On-Premises / *)` is mapped to Food
service here and was mapped to None in Calgary. **MEASURED:** 1,159 of its
1,165 rows also carry another category, 1,034 of them `Restaurant or Food
Service`, which `BUCKET_PRIORITY` resolves to Food service anyway. The 6 rows
that stand alone are real drinking places (NAICS 7224), and mapping the
category rather than dropping it is what keeps them on the map.

The same reasoning covers the adjuncts. `Tobacco and Vaping Product Sales`
(742) co-occurs 489 times with `Retail Sales (Convenience Store)` and 266 with
`Vehicle Wash / Fueling Station`; only 74 rows stand alone, and those are real
vape shops. `Oleoresin Capsicum (OC) Spray Sales` (53) **never** stands alone,
so it is mapped for completeness and is never decisive.

BUCKETS ANCHORED ON naics.py, as every non-NAICS city here is:
    Retail             NAICS 44-45, less 454 nonstore
    Food service       NAICS 722
    Personal services  NAICS 812, less 81293 parking

SIX JUDGMENT CALLS, FOUR OF THEM SETTLED BY SAMPLING RATHER THAN BY RULE
------------------------------------------------------------------------
The merged-category rule this project uses elsewhere - when one category spans
in-scope and out-of-scope trades and cannot be split, leave it out, because the
term nearest the actual trade wins - would have got two of these WRONG. Names
were sampled instead, and the sample overrode the rule twice.

1. **`General Business` (154) is excluded.** The catch-all, and the one value
   that says nothing about the business. **Hand-sampled the 111 rows carrying
   it alone:** parking operators (IMPARK x4, IMPERIAL PARKING, two City Centre
   parkades), coach and scooter fleets (TRAXX COACHLINES, FIRST STUDENT, BIRD
   CANADA, LIME), home-care agencies (HOME INSTEAD, CAREPROS, HARMONY
   CAREGIVING), shelters and churches (EDMONTON WOMEN'S SHELTER, HOPE MISSION),
   daycares (KIDS VILLAGE, BAMBINI) and a market garden (RIVERBEND GARDENS).
   **Zero storefront retail, food or personal services.** Parking is the
   clincher: NAICS 81293 is the one thing explicitly carved OUT of this
   project's personal-services anchor, so the largest identifiable group in the
   catch-all is excluded by the anchor itself.

2. **`Vehicle Wash / Fueling Station` (336) is excluded**, although Vancouver
   counts its `Gas Station` as Retail. Vancouver's category is pure; Edmonton's
   merges a car wash (NAICS 811192, the repair family this project excludes
   everywhere) with a fuel retailer (NAICS 457, which it counts). **Sampled the
   40 rows carrying it alone:** A1A CAR WASH, MILLCREEK CAR WASH, MINT
   SMARTWASH, CLEAN GETAWAY, KINGSWAY, DUGGAN, MINIT, BLUE SKY, KLARITY, ULTRA
   and a truck wash - against two COSTCO GASOLINE and one AFD PETROLEUM. So the
   part that is genuinely retail is almost never alone: 248 of the 336 also
   carry `Retail Sales (Convenience Store)` and keep Retail from that. Cost of
   excluding it: about three fuel sites.

3. **`Animal Breeding and Boarding Facility` (77) COUNTS as a personal
   service, against the merged-category rule.** The rule reads the leading term
   and would exclude it, because animal breeding is NAICS 112 agriculture.
   **The sample says otherwise:** HOLLYWOOF, PAWS AT PLAY DOG DAYCARE, MAPLE'S
   DOGHOUSE, RUFFINGTON'S PALACE, COZY KITTY ACCOMODATIONS, THE PAMPERED PUPPY,
   POSH POOCH HOTEL AND DAYCARE, SEE SPOT RUN DOGGY DAYCARE, PETSMART #1202 -
   pet care storefronts, NAICS 81291, roughly nine in ten. Only SOFINA FOODS (a
   processor) and AMBERLEA MEADOWS (an equestrian property) read as anything
   else. Calgary's `KENNEL SERVICE/PET DEALER` (68) counts for the same reason;
   excluding Edmonton's because its category happens to name breeding first
   would be an artefact of wording, not a difference in the cities.

4. **The `Health Enhancement` family splits four ways, and only the accredited
   CENTRE counts.** Edmonton uses one phrase for four different things, and the
   brief's assumption that all of it was Vancouver's `Health Enhancement
   Services` did not survive sampling:

   - `Health Enhancement Centre (Accredited)` (560) -> **Personal services.**
     **MEASURED** on business names: 34.3% massage, 11.8% spa/nail/hair,
     4.1% acupuncture - but also **26.4% physiotherapy or chiropractic**.
     Counted anyway, for Alberta comparability: Calgary's `MASSAGE CENTRE
     (COMMERCIAL)` (917) counts because massage therapy is **not** a regulated
     health profession in Alberta (it is in British Columbia, which is why
     Vancouver's `Massage Therapy (RMT)` does not count). Excluding Edmonton's
     while counting Calgary's would make the two Alberta cities
     non-comparable for no reason in the data. **The contamination is real and
     disclosed**: roughly 148 rows in this bucket are NAICS 621 health care,
     about 6% of Edmonton's personal-services pins, and `docs/
     excluded_categories.md` and the city page both say so. This is the one
     call here that a reader might reasonably make the other way.
   - `Health Enhancement Centre` (12) -> **None.** The non-accredited variant is
     **pure** NAICS 621: LIFEMARK PHYSIOTHERAPY, PIVOTAL PHYSIOTHERAPY,
     WINDERMERE CHIROPRACTOR, REVIVE SPINE AND SPORT, HERITAGE LANE
     CHIROPRACTIC, STRIDE SPORTS & PHYSIOTHERAPY. Not a personal service under
     the anchor, and nothing in the sample is.
   - `Health Enhancement Centre (Accredited / Independent)` (115) -> **None.** A
     practitioner working inside someone else's centre. Counting them
     double-counts the centre and puts an individual on the map - Calgary's
     `PERSONAL SERVICE (INDEPENDENT CHAIR OPERATOR)` (160) and New York's
     `DOSAERENTER` are dropped for exactly this. The sample supports it: 47% of
     the names read as massage practice and several are personal names
     (JACQUELINE CHALIFOUX BSC RMT), with `<REDACTED FOR PRIVACY>` among them.
   - `Health Enhancement Practitioner (Accredited)` (25) -> **None.** A person,
     not a premises, and **all 25 rows carry `<REDACTED FOR PRIVACY>` as the
     address** - the publisher's own verdict on what these records are.

5. **`Food Processing / Catering Service` (583) stays excluded**, which was the
   open question the build brief flagged as worth the most rows. It merges
   NAICS 311 food manufacturing with 7223 catering and leads with processing,
   so the merged-category rule applies and there is no second field to split it
   on. Vancouver's `Printing Imaging and Photo Services` was left out the same
   way. Reversing it is one line, and would add 583 rows.

6. **Adult services and body rub centres are excluded on sensitivity as well as
   scope** - `Body Rub Centre` (29), `Adult Service` (3), `Erotic
   Entertainment Venue` (3), `Erotic Entertainment Agency` (2), **37 rows**.
   A NAICS-only reading would keep the body rub centres in 812199 beside the
   tattooists this map does count. The reasoning is Calgary's, confirmed by the
   owner on 2026-09-21: mapping adult-services premises adds exposure for the
   people working there without answering the question this project asks. The
   values are mapped to None rather than deleted, so it is one line to reverse.

Counts are the 2026-09-21 pull, `licencetype == 'Commercial'`, split on `";"`.
"""

FIELD_LABEL = "Licence category"
VALUE_COLUMN = "business_licence_category"

# A premises holding several categories gets ONE pin, and this decides its
# bucket. Food first: a restaurant that also holds an alcohol endorsement and a
# tobacco licence is a restaurant. Same order as Calgary, so the two Alberta
# cities resolve multi-category rows identically.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]

RETAIL = "Retail"
FOOD = "Food service"
PERSONAL = "Personal services"


def legend_label(bucket: str) -> str:
    return bucket


# Every category measured on the Commercial set, with its row count. A value
# mapped to None was reviewed and left off; classify() RAISES on anything not
# listed at all, so a new category is a thing to look at rather than a silent
# omission.
BUCKETS = {
    # --- Food service (NAICS 722) -----------------------------------------
    "Restaurant or Food Service": FOOD,                        # 3,518
    "Alcohol Sales (Consumption On-Premises / Minors Allowed)": FOOD,    # 1,165  endorsement on 1,034 restaurants; 6 alone
    "Alcohol Sales (Consumption On-Premises / Minors Prohibited)": FOOD,  # 255   endorsement on 244; 2 alone

    # --- Retail (NAICS 44-45, less 454 nonstore) --------------------------
    "Retail Sales (Minor)": RETAIL,                            # 3,506
    "Retail Sales (Major)": RETAIL,                            # 1,035
    "Retail Sales (Convenience Store)": RETAIL,                #   519
    "Tobacco and Vaping Product Sales": RETAIL,                #   742  adjunct; 74 alone
    "Alcohol Sales (Consumption Off-Premises)": RETAIL,        #   393  NAICS 4453; 302 alone
    "Cannabis Retail Sales": RETAIL,                           #   191  NAICS 459993
    "Second Hand Dealer": RETAIL,                              #   213  NAICS 45993
    "Vehicle Sales and Rental": RETAIL,                        #   528  NAICS 441, as Calgary's MOTOR VEHICLE DEALER - PREMISES
    "Firearm and Ammunition Sales, Service, and Manufacturing": RETAIL,  # 26  NAICS 459110
    "Oleoresin Capsicum (OC) Spray Sales": RETAIL,             #    53  adjunct; NEVER alone
    "Pawnbroker": RETAIL,                                      #    23  the regulated retail slice

    # --- Personal services (NAICS 812, less 81293 parking) ----------------
    "Personal Service": PERSONAL,                              # 1,649  57% spa/nail/hair - the core of NAICS 8121
    "Health Enhancement Centre (Accredited)": PERSONAL,        #   560  call 4; 26% is NAICS 621 and disclosed
    "Animal Breeding and Boarding Facility": PERSONAL,         #    77  call 3; NAICS 81291 pet care
    "Funeral, Cremation, and Cemetery Service": PERSONAL,      #    24  NAICS 8122; a funeral home is a storefront

    # --- People and renters, not premises ---------------------------------
    "Health Enhancement Centre (Accredited / Independent)": None,  # 115  call 4
    "Health Enhancement Practitioner (Accredited)": None,      #    25  call 4; 25/25 address-redacted

    # --- Excluded on sensitivity as well as scope (call 6) ----------------
    "Body Rub Centre": None,                                   #    29
    "Adult Service": None,                                     #     3
    "Erotic Entertainment Venue": None,                        #     3
    "Erotic Entertainment Agency": None,                       #     2

    # --- NAICS 811 repair and maintenance: not a bucket here --------------
    "Vehicle Repair, Maintenance, and Modification": None,     # 1,174
    "Light Duty Repair Service": None,                         #   205
    "Vehicle Wash / Fueling Station": None,                    #   336  call 2
    "Industrial Equipment Sales, Rental, and Repair": None,    #   373  NAICS 423/532, trade not consumer

    # --- Nonstore, mobile and temporary (the NAICS 454 reasoning) ---------
    "Public Market Vendor": None,                              #   143
    "Food Truck / Food Cart": None,                            #    71
    "Travelling or Temporary Sales": None,                     #    38
    "Public Market Organizer": None,                           #    32  runs the market, is not a stall
    "Farmers' Market": None,                                   #     8  the market, not its vendors
    "Designated Driver Service": None,                         #     1

    # --- Merged, and the out-of-scope trade leads (call 5) ----------------
    "Food Processing / Catering Service": None,                #   583
    "Health Enhancement Centre": None,                         #    12  call 4; pure NAICS 621

    # --- Health care (NAICS 621), not a personal service ------------------
    "Independent Laboratory": None,                            #    69

    # --- Offices, trades, housing, wholesale, manufacturing ---------------
    "Administration Office / Professional Service": None,      # 2,701
    "Construction, Contracting, and Labour Service": None,     # 2,635
    "Residential Rental Accommodation (Long-Term)": None,      # 2,484  Philadelphia's Rental
    "Residential Rental Accommodation (Short-Term)": None,     # 1,703
    "Wholesale, Warehouse, and Storage": None,                 # 1,518
    "Manufacturer": None,                                      # 1,385
    "Delivery and Logistic Service": None,                     #   510
    "Financial Service": None,                                 #   503  NAICS 52, as Vancouver's Financial Institution
    "Commercial School": None,                                 #   428  NAICS 611
    "Scrap Metal Dealer and Recycler": None,                   #    52  NAICS 423930 wholesale/waste
    "Auction": None,                                           #    14  NAICS 425 agents and brokers; sample is livestock and salvage
    "Cannabis Processing Facility": None,                      #     6  manufacturing
    "Cannabis Cultivation Facility": None,                     #     3  agriculture
    "General Business": None,                                  #   154  call 1, the catch-all
    "Hotel / Motel": None,                                     #    98  NAICS 721, not 722

    # --- Arts, entertainment, recreation (NAICS 71) -----------------------
    "Participant Recreation Service": None,                    #   450  NAICS 713940, as Vancouver's Fitness Centre
    "Exhibition Hall": None,                                   #   183
    "Spectator Entertainment": None,                           #   148
    "Amusement Establishment": None,                           #   116
    "Bingo / Casino": None,                                    #    11  NAICS 7132
    "Event Production": None,                                  #     3
    "Carnival / Amusement Park": None,                         #     2
    "After Hours Dance Club": None,                            #     1  an entertainment venue; holds no alcohol category
}


# The register's own mobile and nonstore wording, asserted at import the way
# Calgary's "NO PREMISES"/"(MOBILE)" markers are. Edmonton states nonstore
# trade in the category name too, and a future category using this vocabulary
# must not be bucketed by reflex.
_NONSTORE_MARKERS = ("Food Truck", "Food Cart", "Travelling", "Temporary Sales",
                     "Market Vendor", "Designated Driver")
_bucketed_nonstore = sorted(
    name for name, bucket in BUCKETS.items()
    if bucket is not None and any(m in name for m in _NONSTORE_MARKERS))
if _bucketed_nonstore:
    raise AssertionError(
        "Edmonton: these categories name mobile or nonstore trade and must not "
        f"carry a bucket: {_bucketed_nonstore}. This project excludes nonstore "
        "retail (NAICS 454) in every city."
    )

# The 2026-09-21 pull found exactly 60 categories on the Commercial set. If the
# register grows one, classify() will raise on it - this catches the quieter
# case where a category is RETIRED, which no runtime path would notice.
_MEASURED_CATEGORY_COUNT = 60
if len(BUCKETS) != _MEASURED_CATEGORY_COUNT:
    raise AssertionError(
        f"Edmonton: this module maps {len(BUCKETS)} categories but the "
        f"2026-09-21 measurement found {_MEASURED_CATEGORY_COUNT}. Re-pull the "
        "distinct values (licencetype == 'Commercial', split on ';') and "
        "reconcile before trusting the map."
    )


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).

    `row` must carry a `business_licence_category` key holding ONE of
    Edmonton's categories. Step 2 splits the raw `";"`-delimited value and
    resolves the several-category rows through BUCKET_PRIORITY before getting
    here.

    RAISES on an unknown category rather than returning None: a value this
    module has never seen is a data change to look at, not something to drop
    silently from the map. Same convention as calgary_licencetype,
    dc_businessactivity and pipeline/taxonomies/vancouver.
    """
    value = row.get(VALUE_COLUMN)
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    if value not in BUCKETS:
        raise KeyError(
            f"Edmonton: licence category {value!r} is not in this module's "
            f"mapping. Add it with a bucket or an explicit None (and a comment "
            f"saying why) rather than letting an unreviewed category onto the "
            f"map. Note the raw column is ';'-delimited - if this value looks "
            f"like several categories at once, step 2 failed to split it."
        )
    return BUCKETS[value]
