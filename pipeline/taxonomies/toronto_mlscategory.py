"""Toronto's Municipal Licensing & Standards `Category` - 92 values.

THE DEFINING FACT: TORONTO LICENSES FOOD AND TRADES, NOT GENERAL RETAIL.
-----------------------------------------------------------------------
This is Boston's and New York's shape, and it is the whole reason Toronto was
the last Canadian city built rather than the first. **MEASURED 2026-09-21**
across the 81,779 storefront rows this module keeps:

    Food service       62,901   76.9%
    Personal services  15,403   18.8%
    Retail              3,475    4.2%

**And the 4.2% is only the REGULATED retail slice.** Second-hand shops, pawn
shops, precious-metal buyers, smoke and vape shops, pet shops and one fireworks
category - the trades a city licenses because it wants to watch them. Toronto
licenses **no grocer, no clothing shop, no pharmacy, no hardware store, no
general merchandise**, so they are simply absent. That is
`multi-source-city`'s "Retail - regulated slice" archetype, and it is a fact
about Toronto's licensing regime rather than about its high streets.

**The bucket is drawn anyway, and disclosed** - the New York treatment, decided
by the owner on 2026-09-21. The rejected alternative was leaving Retail out
entirely and drawing two buckets: it reads as a stronger statement but discards
3,475 real storefronts and would make Toronto the only city whose legend
differs from the other thirteen. The city page and
`docs/excluded_categories.md` both say what the category does and does not
contain, under *missing* rather than *excluded*.

ONE ROW PER LICENCE, AND `Category` IS SINGLE-VALUED
----------------------------------------------------
Unlike Edmonton (`";"`-delimited, one row per premises) and Calgary (`",\\n"`,
one row per category), Toronto writes **one row per licence with one category
in it**. So a restaurant with a patio holds two licences and appears as **two
rows** - which is Calgary's double-counting problem without Calgary's delimiter
to resolve it. Endorsements therefore have to be dropped by category, and step
2 also deduplicates on premises, because two food licences at one address are
one storefront.

BUCKETS ANCHORED ON naics.py, as every non-NAICS city here is:
    Retail             NAICS 44-45, less 454 nonstore
    Food service       NAICS 722
    Personal services  NAICS 812, less 81293 parking

FIVE JUDGMENT CALLS
-------------------
1. **Endorsements are excluded, and they are large.** `SIDEWALK CAFE` (2,473),
   `NOISE EXEMPTION` (4,960), `CURB LANE CAFE` (694), `EXPANDED
   EATING/DRINKING ESTABLISHMENT` (388) and `EXPANDED ENTERTAINMENT PLACE OF
   ASSEMBLY` (44) are permissions a premises holds, not premises. A restaurant
   with a patio and a noise exemption is one restaurant. Same call as Calgary's
   alcohol and patio endorsements and D.C.'s.

2. **`HOLISTIC CENTRE` (2,051) counts as a personal service, and Ontario's
   regulation of massage therapy is why it is not a problem.** Ontario DOES
   regulate massage therapy (the College of Massage Therapists), so registered
   massage therapists are NAICS 621 health care and are licensed by the
   province rather than appearing here. What Toronto licenses as a holistic
   centre is therefore the NON-registered remainder - NAICS 812199 personal
   care. This is the cleaner side of the line Edmonton's `Health Enhancement
   Centre (Accredited)` sits awkwardly across, where Alberta does not regulate
   the profession and the licence class mixes clinics in.

3. **`PET SHOP` (118) is Retail, where Edmonton's `Animal Breeding and Boarding
   Facility` (77) is a Personal service.** Not an inconsistency: a pet shop
   sells animals and supplies, NAICS 459910 retail, while boarding and daycare
   is NAICS 81291 pet CARE. Toronto licenses the shop; Edmonton licensed the
   service.

4. **Adult-services premises are excluded on sensitivity as well as scope** -
   `BODY RUB PARLOUR` (110), `ADULT ENTERTAINMENT CLUB` (51), `BATH HOUSE`
   (14): **175 rows**. The reasoning is Calgary's and Edmonton's, confirmed by
   the owner on 2026-09-21. Mapped to None rather than deleted, so it is one
   line to reverse.

5. **`PERMANENT FIREWORKS VENDOR` (31) counts and the four temporary ones do
   not.** The City marks the distinction in the category name, as Calgary does
   with `- PREMISES`: `TEMPORARY FIREWORKS VENDOR (OVER 25 KG)` (296), `(UNDER
   25 KG)` (167), `TEMPORARY MOBILE` (227) and `TEMPORARY LEASE` (57) are
   seasonal stands, which is NAICS 454 nonstore. Only the permanent one is a
   shop.

Counts are the 2026-09-21 pull of CKAN resource
`169e90ba-3ae0-43dd-8b2f-919e87002f50`, 159,872 rows.
"""

FIELD_LABEL = "Licence category"
VALUE_COLUMN = "mls_category"

# Toronto's Category is single-valued, so this never resolves a multi-category
# row as Calgary's and Edmonton's do. It is kept for the shared interface, and
# step 2 uses it when deduplicating a premises that holds several licences -
# food first, so a cafe that also holds a personal-services licence is a cafe.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]

RETAIL = "Retail"
FOOD = "Food service"
PERSONAL = "Personal services"


def legend_label(bucket: str) -> str:
    return bucket


BUCKETS = {
    # --- Food service (NAICS 722) -----------------------------------------
    "EATING OR DRINKING ESTABLISHMENT": FOOD,            # 36,615
    "TAKE-OUT OR RETAIL FOOD ESTABLISHMENT": FOOD,       # 26,286

    # --- Personal services (NAICS 812, less 81293 parking) ----------------
    "PERSONAL SERVICES SETTINGS": PERSONAL,              # 11,105  salons, barbers, nail, tattoo
    "LAUNDRY PREMISES": PERSONAL,                        #  2,247  NAICS 8123
    "HOLISTIC CENTRE": PERSONAL,                         #  2,051  call 2

    # --- Retail (NAICS 44-45, less 454) - the REGULATED SLICE ONLY --------
    # There is no general-retail licence in Toronto, so this is all of it.
    "SECOND HAND SHOP": RETAIL,                          #  1,806  NAICS 45993
    "VAPOUR PRODUCT RETAILER": RETAIL,                   #    539  NAICS 459991
    "PRECIOUS METAL SHOP": RETAIL,                       #    413  gold buyers, 45993
    "SMOKE SHOP": RETAIL,                                #    317  NAICS 459991
    "PAWN SHOP": RETAIL,                                 #    218  regulated retail slice
    "PET SHOP": RETAIL,                                  #    118  call 3, NAICS 459910
    "SECOND HAND SALVAGE SHOP": RETAIL,                  #     33  a shop, unlike the YARD below
    "PERMANENT FIREWORKS VENDOR": RETAIL,                #     31  call 5

    # --- Endorsements: permissions a premises holds, not premises (call 1) -
    "NOISE EXEMPTION": None,                             #  4,960
    "SIDEWALK CAFE": None,                               #  2,473
    "CURB LANE CAFE": None,                              #    694
    "EXPANDED EATING/DRINKING ESTABLISHMENT": None,      #    388
    "EXPANDED ENTERTAINMENT PLACE OF ASSEMBLY": None,    #     44

    # --- Excluded on sensitivity as well as scope (call 4) ----------------
    "BODY RUB PARLOUR": None,                            #    110
    "ADULT ENTERTAINMENT CLUB": None,                    #     51
    "BATH HOUSE": None,                                  #     14

    # --- NAICS 811 repair and maintenance: not a bucket here -------------
    "PUBLIC GARAGE": None,                               # 11,767
    "AUTO SERVICE STATION": None,                        #      1

    # --- Licences held by a PERSON or a VEHICLE, not a premises -----------
    "TAXICAB OWNER": None,                               #  9,360
    "TOW TRUCK OWNER": None,                             #  4,959
    "DRIVING INSTRUCTOR (V)": None,                      #  3,130
    "LIMOUSINE OWNER": None,                             #  2,329
    "DRIVING SCHOOL OPERATOR (B)": None,                 #    778
    "TORONTO TAXICAB OWNER": None,                       #    738
    "DRIVE-SELF RENTAL OWNER": None,                     #    471
    "AUCTIONEER": None,                                  #    251  a person, as Edmonton's Auction is
    "LIMOUSINE SERVICE COMPANY": None,                   #    239
    "PEDICAB OWNER": None,                               #    267
    "DRIVING SCHOOL OPERATOR (V)": None,                 #    148
    "TAXICAB BROKER": None,                              #    113
    "COLLECTOR OF SECOND HAND GOODS": None,              #     66  collects; does not keep a shop
    "TAXICAB OPERATOR": None,                            #     40
    "PRIVATE TRANSPORTATION COMPANY": None,              #     14
    "BOATS FOR HIRE": None,                              #      3
    "MOTOR VEHICLE RACING": None,                        #      2

    # --- Construction and trades -----------------------------------------
    "BUILDING RENOVATOR": None,                          #  9,065
    "MASTER PLUMBER": None,                              #  3,274
    "PLUMBING CONTRACTOR": None,                         #  2,365
    "MASTER HEATING INSTALLER": None,                    #  1,433
    "HEATING CONTRACTOR": None,                          #    803
    "PLUMBING & HEATING CONTRACTOR": None,               #    423
    "DRIVEWAY PAVING CONTRACTOR": None,                  #    349
    "DRAIN LAYER": None,                                 #    314
    "DRAIN CONTRACTOR": None,                            #    285
    "BUILDING CLEANER": None,                            #     40
    "INSULATION INSTALLER": None,                        #     38
    "CHIMNEY REPAIRMAN": None,                           #     20

    # --- Signage, advertising and collection permits ---------------------
    "TEMPORARY SIGN - MOBILE": None,                     #  4,443
    "CLOTHING DROP BOX LOCATION PERMIT": None,           #  1,246
    "MARKETING DISPLAY": None,                           #    765
    "TEMPORARY SIGN - A-FRAME": None,                    #    460
    "TEMPORARY SIGN - NEW DEVELOPMENT A-FRAME": None,    #    203
    "TEMPORARY SIGN PROVIDER": None,                     #     41
    "CLOTHING DROP BOX OPERATOR": None,                  #     25
    "TEMPORARY SIGN - PORTABLE": None,                   #     25
    "BILL DISTRIBUTOR": None,                            #      9
    "TEMPORARY SIGN - GROUND-MOUNTED": None,             #      3
    "ADVERTISING": None,                                 #      1

    # --- Nonstore, mobile and temporary trade (NAICS 454) ----------------
    "MOTORIZED REFRESHMENT VEHICLE OWNER": None,         #  1,360
    "NON-MOTORIZED REFRESHMENT VEHICLE OWNER": None,     #  1,071
    "MOBILE VENDING (ICE CREAM TRUCK)": None,            #    593
    "HAWKER/PEDLAR ON FOOT": None,                       #    538
    "MOBILE VENDING (FOOD TRUCK)": None,                 #    361
    "TEMPORARY FIREWORKS VENDOR (OVER 25 KG)": None,     #    296  call 5
    "TEMPORARY MOBILE FIREWORKS VENDOR": None,           #    227  call 5
    "SIDEWALK VENDING": None,                            #    212
    "TEMPORARY FIREWORKS VENDOR (UNDER 25 KG)": None,    #    167  call 5
    "HAWKER/PEDLAR WITH MOTOR VEHICLE": None,            #    147
    "HAWKER/PEDLAR WITH PUSH CART": None,                #     95
    "TEMPORARY LEASE FIREWORKS VENDOR": None,            #     57  call 5
    "CURBLANE VENDING": None,                            #     34
    "TRANSIENT TRADER": None,                            #     19

    # --- Parking: NAICS 81293, carved out of the anchor ------------------
    "COMMERCIAL PARKING LOT": None,                      #  2,058
    "PRIVATE PARKING ENFORCEMENT AGENCY": None,          #    190

    # --- Arts, entertainment, recreation (NAICS 71) ----------------------
    "ENTERTAINMENT PLACE OF ASSEMBLY": None,             #    445
    "AMUSEMENT ESTABLISHMENT": None,                     #    437
    "BILLIARD HALL": None,                               #    177
    "ENTERTAINMENT ESTABLISHMENT/NIGHTCLUB": None,       #    170  merged; leads with entertainment
    "THEATRE": None,                                     #     73
    "BOWLING HOUSE": None,                               #     38
    "CARNIVAL": None,                                    #     16
    "CIRCUS": None,                                      #      5
    "SWIMMING POOL": None,                               #      3

    # --- Finance, waste, accommodation, and one data artefact ------------
    "PAYDAY LOAN": None,                                 #    187  NAICS 522291
    "SECOND HAND SALVAGE YARD": None,                    #     68  a yard, not a shop
    "SHORT TERM RENTAL COMPANY": None,                   #      5  NAICS 721
    "** Class record not on file. (138)": None,          #      4  the register's own placeholder
}


# Toronto marks nonstore and temporary trade in the category name, as Calgary
# and Edmonton do. Asserted at import so a future category using this
# vocabulary cannot be bucketed by reflex.
_NONSTORE_MARKERS = ("TEMPORARY ", "MOBILE", "HAWKER", "PEDLAR", "VENDING",
                     "TRANSIENT", "REFRESHMENT VEHICLE")
_bucketed_nonstore = sorted(
    name for name, bucket in BUCKETS.items()
    if bucket is not None and any(m in name for m in _NONSTORE_MARKERS))
if _bucketed_nonstore:
    raise AssertionError(
        "Toronto: these categories name mobile, temporary or nonstore trade "
        f"and must not carry a bucket: {_bucketed_nonstore}. This project "
        "excludes nonstore retail (NAICS 454) in every city."
    )

# The 2026-09-21 pull found exactly 92 categories. classify() raises on a NEW
# one; this catches the quieter case of a category being RETIRED, which no
# runtime path would notice. The country profile and this city's own brief both
# recorded 72, which was never measured.
_MEASURED_CATEGORY_COUNT = 92
if len(BUCKETS) != _MEASURED_CATEGORY_COUNT:
    raise AssertionError(
        f"Toronto: this module maps {len(BUCKETS)} categories but the "
        f"2026-09-21 measurement found {_MEASURED_CATEGORY_COUNT}. Re-pull "
        "`Category`'s distinct values and reconcile before trusting the map."
    )


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).

    RAISES on an unknown category rather than returning None: a value this
    module has never seen is a data change to look at, not something to drop
    silently from the map. Same convention as calgary_licencetype,
    edmonton_licencecategory, dc_businessactivity and
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
            f"Toronto: licence category {value!r} is not in this module's "
            f"mapping. Add it with a bucket or an explicit None (and a comment "
            f"saying why) rather than letting an unreviewed category onto the "
            f"map."
        )
    return BUCKETS[value]
