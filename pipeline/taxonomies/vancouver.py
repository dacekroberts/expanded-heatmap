"""Vancouver + Surrey: two municipal registries dispatched on a `source`
column, like New York's four and Boston's three.

WHY A DISPATCHING MODULE RATHER THAN TWO
----------------------------------------
This is a regional build (see pipeline/vancouver/config.py). The two cities
publish different classification fields with no shared vocabulary -
Vancouver's `businesstype` (89 values reaching the map, single-valued) and
Surrey's `BusinessCategory` (210 values, NEWLINE-separated, several per row).
A module per source would mean two `TAXONOMY_SYSTEM` values for one map, which
`map_common.render_heatmap` has no concept of. So `classify()` dispatches on
the source, `VALUE_COLUMN` holds each registry's OWN category string - a
tooltip shows Vancouver's "Limited Service Food Establishment" or Surrey's
"Food Primary-Class B Dining Lounge", the words the city itself uses - and
`FIELD_LABEL` is the generic "Category" because it is shared.

HOW THE BUCKETS WERE DECIDED
----------------------------
Not invented here. Anchored on `naics.py`, so this city stays comparable with
the five NAICS cities rather than drawing its own line:

    Retail             NAICS 44-45, LESS 454 "nonstore retailers"
    Food service       NAICS 722
    Personal services  NAICS 812, LESS 81293 parking

Everything else is None - not a privacy carve-out but a statement about what
"storefront commercial density" means. That deliberately excludes, exactly as
it does for the NAICS cities: professional services (54), health care (62),
finance and insurance (52), real estate (53), education (61), arts/
entertainment/recreation (71), accommodation (721), wholesale (42),
manufacturing (31-33), construction (23), transport (48-49), administrative
support (56), and repair and maintenance (811).

That last one is worth naming because it is counter-intuitive and it is
consistent: NAICS puts **repair** in 811 and **personal care** in 812, and
only 812 is a bucket here. So a hairdresser counts and a shoe repairer does
not; Surrey's Tailor, Dressmaker, Upholstery, Locksmith, Sharpening Service
and Repair Service are all None, matching Vancouver's own "General Repair and
Maintenance".

FIVE JUDGMENT CALLS, RECORDED RATHER THAN BURIED
------------------------------------------------
1. **Mobile trade is not a storefront.** Vancouver's `Street Vendor` (116
   mappable rows), Surrey's `Portable Food Vendor` (9), `Catering/Coffee
   Truck` (3), `Vending Machine` (40), `Mail Order` (24) and `Pedlar` are all
   excluded. This follows the project-wide exclusion of NAICS 454, whose
   stated reason is that NAICS itself calls those "nonstore". Street Vendor is
   the largest single row-count sacrificed to consistency here, and the
   category is also genuinely mixed - Vancouver licenses food carts and
   merchandise vendors under one label with no subtype to split them.

2. **Surrey's two Inter-Municipal Business Licences are the city's catch-all
   and are excluded** - 1,473 of its 13,066 Commercial/Industrial rows
   (11.3%). An IMBL is a permission to TRADE ACROSS Metro Vancouver or the
   Fraser Valley, held mostly by contractors; the address on it is the
   holder's base, not a shop. This is Chicago's "Limited Business License"
   problem and is treated the same way.

3. **BC-regulated health professions are health care; unregulated body-care
   services are personal services.** Surrey's `Massage Therapy (RMT)` (155)
   and `Acupuncture` (56) are regulated professions in British Columbia, so
   they sit with the Professional Practitioners at None. `Holistic Health
   Care` (58), `Reflexology` (4), `Acupressure` (3), `Shiatsu Massage` (2),
   `Tanning Salon` (10) and `Tattoo Parlour` (13) are not, and read as NAICS
   812199, so they count. Vancouver draws the same line itself, between
   `Health Care Professionals and Services` (None) and `Health Enhancement
   Services` (Personal services).

4. **A funeral parlour is a storefront; a cemetery is not.** Both are NAICS
   812, so the anchor alone would keep both. Surrey's `Funeral Parlour` (4) is
   a walk-in commercial premises and counts; `Cemetery` (2) is land, and is
   excluded as a departure from the prefix on storefront grounds.

5. **Vancouver's `businesssubtype` was TESTED as a disambiguator and
   REJECTED.** It looked like Chicago's `business_activity`. It is empty on
   every row of the largest categories - all 4,544 Health Care, all 651 Retail
   Dealer - Food, all 116 Street Vendor - and splits only `Limited Service
   Food Establishment` into With/Without Liquor, which does not change a
   bucket. So bucketing reads `businesstype` alone.

Measured 2026-09-21 on current-year Issued rows with coordinates. Counts in
comments are from that set, which is the set that reaches the map.
"""

# --- Interface --------------------------------------------------------------

FIELD_LABEL = "Category"
VALUE_COLUMN = "category"
# classify() needs to know which registry a row came from.
EXTRA_COLUMNS = ("source",)

# A Surrey premises can hold several categories at once (4,837 rows do), so one
# has to win. Most specific first, most generic last: "Retail Merchant" is
# Surrey's broadest label and behaves like an adjunct licence, so it loses to a
# restaurant or a salon at the same address. Same order as Miami's.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]

RETAIL = "Retail"
FOOD = "Food service"
PERSONAL = "Personal services"


def legend_label(bucket: str) -> str:
    """Taxonomy-module interface: legend text for a bucket. A local taxonomy
    returns the bucket name unchanged - there is no prefix list to append, and
    the two registries' own words appear in the tooltip instead."""
    return bucket


# --- Vancouver: `businesstype`, 89 values on the mappable set ---------------
# Single-valued, so no splitting. None = not a storefront.

VANCOUVER_BUCKETS = {
    # Retail (NAICS 44-45)
    "Retail Dealer": RETAIL,                          # 2,034
    "Retail Dealer - Food": RETAIL,                   #   651  food/beverage shops
    "Pharmacy": RETAIL,                               #   176
    "Retail Dealer - Used Goods": RETAIL,             #   137
    "Liquor Retail Store": RETAIL,                    #   103
    "Retail Dealer - Cannabis": RETAIL,               #    81
    "Grocery Store": RETAIL,                          #    77
    "Gas Station": RETAIL,                            #    58  NAICS 457
    "Food Market": RETAIL,                            #     3
    "Marine Service Station": RETAIL,                 #     1  retail fuel

    # Food service (NAICS 722)
    "Restaurant": FOOD,                               # 1,663
    "Limited Service Food Establishment": FOOD,       # 1,297
    "Liquor Establishment": FOOD,                     #   190  drinking places
    "Caterer": FOOD,                                  #   154

    # Personal services (NAICS 812)
    "Beauty Services": PERSONAL,                      # 1,396
    "Animal Services": PERSONAL,                      #   115  NAICS 812910
    "Health Enhancement Services": PERSONAL,          #   111  non-clinical
    "Personal Services": PERSONAL,                    #    93
    "Laundry Services": PERSONAL,                     #    75

    # --- Not storefronts ---------------------------------------------------
    # Professional, clinical and office activity - the bulk of the registry.
    "Health Care Professionals and Services": None,   # 4,544  NAICS 621
    "Legal Services": None,                           # 1,796
    "Business Support Services": None,                #   993
    "Financial Services": None,                       #   858
    "Consulting and Management Services": None,       #   797
    "Real Estate Services": None,                     #   678
    "Information Communication Technology": None,     #   590
    "Health Care Facility": None,                     #   418  NAICS 622
    "Architectural and Engineering Services": None,   #   339
    "Insurance Services": None,                       #   206
    "Mining Services": None,                          #   204
    "Financial Institution": None,                    #   166  bank branches, 522
    "Brokerage Services": None,                       #   151
    "Tourism Services": None,                         #   145
    "Design Services": None,                          #   124
    "Money Services": None,                           #   124
    "Marketing Public Relations Advertising and Event Promotion Services": None,  # 90
    "Laboratory Services": None,                      #    85
    "Publishing and Journalism Services": None,       #    20
    "Photography Production and Rehearsal Studio": None,  # 232  NAICS 5419
    "Printing Imaging and Photo Services": None,      #    80  see note below
    "Digital Entertainment and Interactive Technology": None,  # 84
    "Security Services": None,                        #    39

    # Residential tenancy - the Philadelphia `Rental` shape. 3,451 mappable
    # rows, and the single largest non-storefront category after health care.
    "Long-term Rental": None,                         # 3,451

    # Construction and trades.
    "General Contractor": None,                       #   633
    "Trade Contractor": None,                         #   148
    "General Repair and Maintenance": None,           #   114  NAICS 811
    "Building Repair and Maintenance": None,          #    69
    "Vehicle Repair Detailing and Washing Services": None,  # 304  NAICS 811

    # Wholesale, manufacturing, logistics.
    "Wholesale Dealer - Non-Food": None,              #   485
    "Non-Food Manufacturer Assembler and Processor": None,  # 330
    "Food Manufacturer Assembler and Processor": None,      # 282
    "Wholesale Dealer - Food": None,                  #   111
    "Logistics Services": None,                       #    64
    "Warehouse Operator - Non-Food": None,            #    52
    "Transportation and Support Services": None,      #    16
    "Warehouse Operator - Food": None,                #     9
    "Creative Products Manufacturer": None,           #     6
    "Oil Gas and Other Fuels": None,                  #     1  fuel dealer/wholesale

    # Parking - excluded for every city in this project (NAICS 81293).
    "Parking Area / Garage": None,                    #   423

    # Education and instruction (NAICS 61).
    "Arts and Creative Instruction": None,            #   174
    "Business - Vocational Instruction": None,        #   122
    "Sport and Fitness Instruction": None,            #    72
    "Private School or College": None,                #    66

    # Arts, entertainment, recreation (NAICS 71) and accommodation (721).
    "Fitness Centre": None,                           #   215  NAICS 713940
    "Hotel or Motel": None,                           #    96  NAICS 721
    "Marina Operator": None,                          #    90
    "Artist Studio": None,                            #    70
    "Venue": None,                                    #    29
    "Hall / Spectator Sports Venue": None,            #    26
    "Entertainment Facility": None,                   #    25
    "Theatre": None,                                  #    21
    "Artist Agency": None,                            #    17
    "Artist": None,                                   #    16
    "Special Events": None,                           #    11
    "Bingo Hall / Casino / Horse Racing": None,       #     3
    "Exhibition Centre": None,                        #     2
    "Amusement Park": None,                           #     1

    # Mobile trade - see judgment call 1.
    "Street Vendor": None,                            #   116

    # Organisations (NAICS 813, not 812).
    "Association or Society": None,                   #   589
    "Soliciting For Charity": None,                   #     1

    # Rental and leasing of goods (NAICS 532, not 44-45).
    "Rental Services": None,                          #   106

    # Waste and resources (NAICS 562), agriculture (11).
    "Recycling and Resource Recovery Services": None,  #   15
    "Waste Collection and Hauling Services": None,    #    12
    "Forestry Services": None,                        #     6
    "Urban Farm Class B": None,                       #     1

    # Administrative artefacts, not businesses: a licence APPLICATION row.
    "Liquor License Application": None,               #    50
    "Temp Liquor Licence Amendment": None,            #    30
    "Cannabis Licence Application": None,             #     1

    # Excluded on privacy grounds as well as scope - a sole operator's
    # premises, and a category where a name at an address is sensitive.
    "Adult Services": None,                           #     1
}

# `Printing Imaging and Photo Services` is the least comfortable None here. It
# spans NAICS 323 printing (manufacturing) and 812921 photofinishing (personal
# services), and the label leads with the manufacturing reading. 80 rows. Left
# out rather than split on a guess; revisit if the City ever publishes a
# subtype for it.


# --- Surrey: `BusinessCategory`, 210 values, newline-separated -------------
# Step 2 splits on "\n" before calling classify(), so the keys here are single
# categories. All 210 are mapped, not just the 198 that appear on
# Commercial/Industrial rows, so classify() cannot raise merely because step
# 2's filter order changed.

SURREY_BUCKETS = {
    # Retail (NAICS 44-45). Surrey bands retail by headcount; all bands are
    # the same bucket, and the band is preserved in the tooltip.
    "Retail Merchant - 0 to 2 Employees": RETAIL,     # 592
    "Retail Merchant - 3 to 5 Employees": RETAIL,     # 353
    "Retail Merchant - 10 to 19 Employees": RETAIL,   # 158
    "Retail Merchant - 20 or More Employees": RETAIL,  # 157
    "Retail Merchant - 6 to 9 Employees": RETAIL,     # 149
    "Automobile Dealer/Rebuilder": RETAIL,            # 287  NAICS 441
    "Gas Station": RETAIL,                            #  71
    "Liquor Licensee Retail Store": RETAIL,           #  41
    "Bakery": RETAIL,                                 #  40  baked-goods shop
    "Nursery": RETAIL,                                #  27  garden centre, 44424
    "Farm Produce Sales": RETAIL,                     #  14
    "Second Hand Dealer": RETAIL,                     #  13  NAICS 4533
    "Lumber Yard/Building Material Yard": RETAIL,     #   5  NAICS 4441
    "Pawn Broker": RETAIL,                            #   4  regulated retail slice
    "Flea Market": RETAIL,                            #   1
    "Adult Entertainment Store": RETAIL,              #   1
    "Pepper Spray Vendor": RETAIL,                    #   1

    # Food service (NAICS 722)
    "Restaurant - No Alcohol": FOOD,                  # 838
    "Food Primary-Class B Dining Lounge": FOOD,       # 149
    "Food Primary-Class B Dining Room": FOOD,         # 116
    "Caterer": FOOD,                                  #  62
    "Liquor Primary - Class A Pub": FOOD,             #  18
    "Liquor Primary-Class D Neighbourhood Pub": FOOD,  # 16
    "Concession Stand": FOOD,                         #   6
    "Liquor Primary-Class E Stadium": FOOD,           #   3
    "Liquor Primary-Class F Marine Pub": FOOD,        #   1

    # Personal services (NAICS 812)
    "Hair Salon/Barber": PERSONAL,                    # 320
    "Esthetician": PERSONAL,                          # 296
    "Holistic Health Care": PERSONAL,                 #  58  unregulated - call 3
    "Laundromat": PERSONAL,                           #  32
    "Dog Grooming": PERSONAL,                         #  19  NAICS 812910
    "Dry Cleaner/Laundry Service": PERSONAL,          #  19
    "Tattoo Parlour": PERSONAL,                       #  13
    "Tanning Salon": PERSONAL,                        #  10
    "Commercial Kennel": PERSONAL,                    #   7
    "Animal Sitting": PERSONAL,                       #   5
    "Funeral Parlour": PERSONAL,                      #   4  a storefront - call 4
    "Reflexology": PERSONAL,                          #   4
    "Acupressure": PERSONAL,                          #   3
    "Shiatsu Massage": PERSONAL,                      #   2

    # --- Not storefronts ---------------------------------------------------
    # Surrey's catch-all: a permission to trade across the region - call 2.
    "Inter-Municipal Business License Metro": None,   # 758
    "Inter-Municipal Business License FV": None,      # 715

    # Manufacturing, wholesale, warehousing.
    "Manufacturer/Machine Shop": None,                # 803
    "Wholesale": None,                                # 577
    "Warehouse": None,                                # 303
    "Sign Painter/Manufacturer/Installations": None,  #  36
    "Import/Export": None,                            #  24
    "Machinery/Heavy Equipment Dealer": None,         #  19  NAICS 423 wholesale
    "Welding": None,                                  #  18
    "Manufacturer's Agent": None,                     #   9
    "Petroleum Product Distributor": None,            #   4
    "Recycling Plant": None,                          #   2
    "Salvage Yard": None,                             #   1
    "Scrap Dealer": None,
    "Ship Agency/Chandler": None,

    # Residential tenancy and residential care.
    "Short-Term Rentals": None,                       # 639
    "Apartment/Townhouse Rental": None,               #  84
    "Alcohol & Drug Recovery House": None,            #  23  NAICS 623
    "Mobile Home Park": None,                         #  11
    "Secondary Suite": None,

    # Clinical and regulated health professions - call 3.
    "Professional Practitioner-Medical": None,        # 588
    "Professional Practitioner-Dentist": None,        # 229
    "Massage Therapy (RMT)": None,                    # 155  BC-regulated
    "Professional Practitioner-Lawyer": None,         # 185
    "Professional Practitioner-Accountant": None,     # 146
    "Counselling Service": None,                      # 149
    "Health Care Consultant": None,                   # 108
    "Professional Practitioner-Chiropractor": None,   #  75
    "Professional Practitioner-Engineer": None,       #  64
    "Acupuncture": None,                              #  56  BC-regulated
    "Professional Practitioner-Optometrist": None,    #  47
    "Professional Practitioner-Veterinarian": None,   #  43
    "Professional Practitioner-Notary": None,         #  30
    "Part Time Medical Practitioner": None,           #  17
    "Medical Laboratory": None,                       #  15
    "Dental Lab": None,                               #  15
    "Professional Practitioner-Architect": None,      #  13
    "Professional Practitioner-Land Surveyor": None,  #  13
    "Denture Clinic": None,                           #  12
    "Professional Practitioner-Psychiatry": None,     #  10
    "Methadone Dispensary": None,                     #   1

    # Offices, consultancies, agencies (NAICS 54/56).
    "Immigration Consultant": None,                   # 271
    "Administration Office": None,                    # 218
    "Consultant": None,                               # 172
    "Financial Planning/Consultant": None,            # 129
    "Miscellaneous": None,                            # 127  unusable catch-all
    "Software Design/Consultant": None,               #  75
    "Janitorial Service": None,                       #  71
    "Travel Agency": None,                            #  71
    "Employment Agency/Recruiting Service": None,     #  59
    "Bookkeeping": None,                              #  53
    "Security Service": None,                         #  46
    "Property Management": None,                      #  46
    "Sales/Marketing Office": None,                   #  37
    "Printer/Publisher": None,                        #  39
    "Currency Exchange": None,                        #  31
    "Financial Agent": None,                          #  29
    "Photographer/Videographer": None,                #  26
    "Construction Management": None,                  #  26
    "Land Development": None,                         #  26
    "Drafting/Design Service": None,                  #  24
    "Income Tax Service/Buyer": None,                 #  23
    "Business Services Office": None,                 #  23
    "Computer Consulting/Repair/Design": None,        #  21
    "Investment Consultant": None,                    #  14
    "Traffic Control": None,                          #  13
    "General Business Office": None,                   #  10
    "Customs Broker": None,                           #   9
    "Project Management": None,                       #   8
    "Media/Public Relations": None,                   #   5
    "Interior Decorating/Design": None,               #   5
    "Real Estate Appraisal/Building Insp Serv": None,  #  5
    "Insurance Adjuster": None,                       #   4
    "Party/Wedding Consultant": None,                 #   3
    "Bankruptcy Trustee": None,                       #   3
    "Advertising": None,                              #   3
    "Private Investigator": None,                     #   2
    "Parking Lot Enforcement": None,                  #   2
    "Tour Consultant/Operator": None,                 #   1
    "Employment Consultant": None,                    #   1
    "Internet Services": None,                        #   1
    "Planning Consultant": None,                      #   1
    "Mediation Services": None,
    "Desktop Publishing": None,

    # Finance and insurance (NAICS 52).
    "Automated Teller Machine": None,                 #  94
    "Bank": None,                                     #  90
    "Insurance Agent": None,                          # 140
    "Cheque Cashing Centre": None,                    #   8

    # Real estate (NAICS 53), banded by headcount like retail.
    "Real Estate - 0 to 5 Employees": None,           #  77
    "Real Estate - 6 to 10 Employees": None,          #  10
    "Real Estate - 26 to 50 Employees": None,         #   5
    "Real Estate - 51 to 100 Employees": None,        #   4
    "Real Estate - 16 to 25 Employees": None,         #   2
    "Real Estate - 11 to 15 Employees": None,         #   1

    # Construction trades (NAICS 23).
    "Contractor - Miscellaneous": None,               # 337
    "Contractor - General": None,                     # 282
    "Contractor - Electrical": None,                  #  90
    "Contractor - Plumbing/Heating": None,            #  62
    "Contractor - Masonry/Drywall": None,             #  34
    "Contractor - Landscaping/Excavating": None,      #  30
    "Contractor - Painting": None,                    #  22
    "Contractor - Roofing/Insulation": None,          #  21
    "Contractor - Alarm Installation": None,          #  18
    "Contractor - Fire Protection": None,             #  12
    "Contractor - Paving": None,                      #   6
    "Contractor - With Storage": None,                #   4
    "Contractor - Sewer/Septic": None,                #   3
    "Contractor - Demolition": None,                  #   2
    "Glass Installations/Sales": None,                #  35  installer, not a shop

    # Repair and maintenance (NAICS 811) - NOT 812. See the module docstring.
    "Automotive Repair Service": None,                # 336
    "Auto Body/Painting": None,                       # 117
    "Repair Service": None,                           #  84
    "Automobile Cleaning/Car Wash/Detailing": None,   #  56
    "Locksmith": None,                                #   8
    "Upholstery": None,                               #   8
    "Tailor": None,                                   #   9
    "Dressmaker": None,                               #   3
    "Sharpening Service": None,                       #   2
    "Automobile Wrecker": None,                       #   7
    "Fashion Design": None,

    # Transport and couriers (NAICS 48-49).
    "Trucking & Cartage": None,                       # 171
    "Towing - No Storage": None,                      #  19
    "Courier Service": None,                          #  16
    "Truck Parking": None,                            #  16
    "Automobile/Truck Rental": None,                  #  21  NAICS 532
    "Rental Service": None,                           #  31  NAICS 532
    "Taxi Service": None,                             #   6
    "Trucking & Cartage - 1 Vehicle Only": None,      #   5
    "Limousine Service": None,                        #   5
    "Towing - Storage": None,                         #   3
    "Bus Service": None,                              #   3
    "Boat Bldg/Sales/Rental/Service/Marina": None,    #   1

    # Parking - excluded for every city (NAICS 81293).
    "Parking Lot": None,                              # 103

    # Education (NAICS 61).
    "Business School": None,                          # 119
    "Tutoring": None,                                 #  95
    "Trade School": None,                             #  42
    "Driving School": None,                           #  26
    "Education Service": None,                        #  18

    # Arts, entertainment, recreation (NAICS 71) and accommodation (721).
    "Recreational Facility": None,                    # 167
    "Bed & Breakfast": None,                          #  53  NAICS 721
    "Hotel/Motel": None,                              #  23
    "Golf Course/Driving Range/Par 3 Course": None,   #  12
    "Tourist Trailer Park/Campsite": None,            #   8
    "Theatre": None,                                  #   3
    "Carnival": None,                                 #   3
    "Arcade": None,                                   #   2
    "Bowling Alley": None,                            #   2
    "Casino": None,                                   #   1
    "Circus": None,                                   #   1
    "Theatre 2": None,                                #   1

    # Organisations (NAICS 813), utilities, land.
    "Charitable Society/Organization": None,          # 240
    "Social Club": None,                              #   3
    "Public Utility Company": None,                   #   3
    "Cemetery": None,                                 #   2  not a storefront - call 4
    "Fitness Personal Trainer": None,                 #  18  travels to the client
    "Recycling Depot": None,                          #  27
    "U-Brew Premise": None,                           #   2

    # Mobile trade - call 1.
    "Vending Machine": None,                          #  40
    "Mail Order": None,                               #  24
    "Portable Food Vendor": None,                     #   9
    "Post Box Rental Agency": None,                   #   6
    "Catering/Coffee Truck": None,                    #   3
    "Auction/Auctioneer": None,                       #   1
    "Mail Drop Service": None,                        #   1
    "Pedlar": None,
    "Ice Cream Vendor": None,

    # Home-occupation-only categories. None appears on a Commercial/Industrial
    # row, so none reaches the map, but all are mapped so classify() cannot
    # raise if step 2's filter order ever changes.
    "Home Crafts": None,
    "Hobby Kennel - 3 Dogs": None,
    "Hobby Kennel - 4 to 6 Dogs": None,
    "Cat Boarding": None,
}

BUCKETS_BY_SOURCE = {
    "vancouver": VANCOUVER_BUCKETS,
    "surrey": SURREY_BUCKETS,
}


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).

    `row` must carry `category` (one registry's own single category string)
    and `source` (which registry). RAISES on an unknown category rather than
    returning None: a value this module has never seen is a data change that
    must be looked at, not silently dropped from the map. That is the
    project's convention - see dc_businessactivity.classify.
    """
    source = row.get("source")
    if source not in BUCKETS_BY_SOURCE:
        raise KeyError(
            f"unknown source {source!r}; expected one of "
            f"{sorted(BUCKETS_BY_SOURCE)}. classify() dispatches on the "
            f"`source` column declared in EXTRA_COLUMNS."
        )
    table = BUCKETS_BY_SOURCE[source]
    value = row.get(VALUE_COLUMN)
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    if value not in table:
        raise KeyError(
            f"{source}: category {value!r} is not in this module's mapping. "
            f"Add it with a bucket or an explicit None (and a comment saying "
            f"why) rather than letting an unreviewed category onto the map. "
            f"Note Surrey's column is newline-separated - if this value looks "
            f"like several categories at once, step 2 failed to split it."
        )
    return table[value]
