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
the NAICS cities rather than drawing its own line:

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

The last is counter-intuitive but consistent: NAICS puts **repair** in 811
and **personal care** in 812, and only 812 is a bucket here. So a hairdresser
counts and a shoe repairer does not; Surrey's Tailor, Dressmaker, Upholstery,
Locksmith, Sharpening Service and Repair Service are all None, matching
Vancouver's own "General Repair and Maintenance".

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
   Extended 2026-09-29 (owner, food with no counter of its own): both
   registries' `Caterer`, Surrey's `Concession Stand` and `Flea Market`.

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

4. **Neither a funeral parlour nor a cemetery is a storefront.** Both are
   NAICS 812 (8122), so the anchor alone would keep both. `Cemetery` (2) is
   land, and was excluded from the start. Surrey's `Funeral Parlour` (4) was
   first counted as a walk-in premises; funeral services off every map
   (owner, 2026-09-28) took it out too, as naics.py now carves out 8122.

5. **Vancouver's `businesssubtype` was TESTED as a disambiguator and
   REJECTED.** It looked like Chicago's `business_activity`. It is empty on
   every row of the largest categories - all 4,544 Health Care, all 651 Retail
   Dealer - Food, all 116 Street Vendor - and splits only `Limited Service
   Food Establishment` into With/Without Liquor, which does not change a
   bucket. So bucketing reads `businesstype` alone.

Measured 2026-09-21 on current-year Issued rows with coordinates. Counts in
comments are from that set, which is the set that reaches the map.
"""
import re

from pipeline.taxonomies import naics

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
    # Food with no counter of its own (owner, 2026-09-29): an event caterer
    # cooks for the event (NAICS 722320). Food service until then.
    "Caterer": None,                                  #   154

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
    "Adult Entertainment Store": RETAIL,              #   1  a sex shop - retail, kept (owner, 2026-09-29)
    "Pepper Spray Vendor": RETAIL,                    #   1

    # Food service (NAICS 722)
    "Restaurant - No Alcohol": FOOD,                  # 838
    "Food Primary-Class B Dining Lounge": FOOD,       # 149
    "Food Primary-Class B Dining Room": FOOD,         # 116
    "Liquor Primary - Class A Pub": FOOD,             #  18
    "Liquor Primary-Class D Neighbourhood Pub": FOOD,  # 16
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
    "Funeral Parlour": None,                          #   4  funeral services off every map (owner, 2026-09-28) - call 4
    "Fitness Personal Trainer": None,                 #  18  travels to the client
    "Recycling Depot": None,                          #  27
    "U-Brew Premise": None,                           #   2

    # Mobile trade - call 1.
    "Vending Machine": None,                          #  40
    "Mail Order": None,                               #  24
    "Portable Food Vendor": None,                     #   9
    "Post Box Rental Agency": None,                   #   6
    "Catering/Coffee Truck": None,                    #   3
    # Food with no counter of its own, street and market stalls (owner,
    # 2026-09-29): an event caterer (NAICS 722320), a concession stand and a
    # flea market's stalls. Food service / Retail until then.
    "Caterer": None,                                  #  62
    "Concession Stand": None,                         #   6
    "Flea Market": None,                              #   1
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

# --- Burnaby: `LICENCE_TYPE_NAME`, 142 values (regional extension, 2026-10-03)
# Decided by docs/category_rules.md, then the NAICS anchor above, following
# VANCOUVER_BUCKETS and SURREY_BUCKETS for the same trade. Counts are rows in
# the 2026-10-02 layer (20,054), before de-duplication. RETAIL SALE, RENTAL &
# REPAIR is Retail, kept whole (owner, 2026-10-02).
BURNABY_BUCKETS = {
    # --- Retail (NAICS 44-45) --------------------------------------------
    "RETAIL TRADER - GENERAL 1 - 10 PERSONS": RETAIL,  # 514  general retail, banded by headcount like Surrey's
    "RETAIL TRADER - FOOD 1 - 10 PERSONS": RETAIL,  # 195  food shops (Vancouver Retail Dealer - Food)
    "CAR DEALER - NEW & USED": RETAIL,  # 71  car dealers Retail (R4)
    "RETAIL TRADER - GENERAL 11 - 50 PERSONS": RETAIL,  # 61  general retail
    "RETAIL SALE, RENTAL & REPAIR": RETAIL,  # 32  owner call 2026-10-02: Retail, kept whole
    "GAS SERVICE STATION": RETAIL,  # 31  petrol stations Retail (R4)
    "LIQUOR ESTABLISHMENT - BEER & WINE STORE": RETAIL,  # 18  liquor store (Vancouver Liquor Retail Store)
    "RETAIL TRADER - FOOD 11 - 50 PERSONS": RETAIL,  # 16  food shops
    "RETAIL TRADER - FOOD 51+ PERSONS": RETAIL,  # 10  supermarkets
    "NURSERY": RETAIL,  # 10  garden centre, NAICS 44424 (Surrey Nursery)
    "RETAIL TRADER - GENERAL 51+ PERSONS": RETAIL,  # 8  general retail
    "LUMBER YARD": RETAIL,  # 2  NAICS 4441 (Surrey Lumber Yard/Building Material Yard)
    "PAWNBROKER": RETAIL,  # 1  pawnbrokers Retail (R5)
    "SECOND HAND DEALER": RETAIL,  # 1  used goods, NAICS 4533 (Surrey Second Hand Dealer)

    # --- Food service (NAICS 722) ----------------------------------------
    "RESTAURANT 11 - 50 SEATS": FOOD,  # 309  restaurant
    "RESTAURANT - TAKE OUT": FOOD,  # 178  limited-service restaurant, NAICS 722513
    "RESTAURANT 1 - 10 SEATS": FOOD,  # 112  restaurant
    "RESTAURANT 51 - 150 SEATS": FOOD,  # 102  restaurant
    "RESTAURANT 151 & OVER SEATS": FOOD,  # 45  restaurant
    "LIQUOR ESTABLISHMENT - CLASS D NEIGHBOURHOOD PUB": FOOD,  # 9  pub (Surrey Liquor Primary-Class D Neighbourhood Pub)
    "LIQUOR ESTABLISHMENT - CLASS A HOTEL": FOOD,  # 4  liquor-primary lounge or pub in a hotel (Surrey Liquor Primary - Class A Pub); the licence is the bar, not the rooms

    # --- Personal services (NAICS 812) -----------------------------------
    "PERSONAL SERVICE ESTABLISHMENT": PERSONAL,  # 402  salons, barbers, aesthetics, tattoo, commercial massage
    "LAUNDRY PLANT/LAUNDROMAT": PERSONAL,  # 17  dry cleaners, laundromats, linen supply, all NAICS 8123 (Surrey Laundromat)
    "ANIMAL SERVICES": PERSONAL,  # 15  pet grooming and daycare, NAICS 812910 (Vancouver Animal Services)
    "LAUNDRY & / OR DRY CLEANING OFFICE": PERSONAL,  # 6  dry-cleaning depots, NAICS 8123 (Surrey Dry Cleaner/Laundry Service)

    # --- Not storefronts -------------------------------------------------
    # Home-based, residential tenancy and rental licences.
    "HOUSE RENTAL LICENCE": None,  # 4338  residential tenancy (Vancouver Long-term Rental)
    "HOME-BASED BUSINESS - GENERAL": None,  # 1602  home-based out
    "HOME-BASED BUSINESS - CONTRACTOR": None,  # 1297  home-based out
    "SHORT TERM RENTAL LICENCE": None,  # 439  residential tenancy (Surrey Short-Term Rentals)
    "APARTMENT - PER DWELLING UNIT": None,  # 330  residential tenancy (Surrey Apartment/Townhouse Rental)
    "HOME-BASED BUSINESS - CRAFT": None,  # 47  home-based out (Surrey Home Crafts)
    "MISCELLANEOUS RESIDENT": None,  # 116  catch-all, mostly packaged-food makers (Surrey Miscellaneous)

    # Regional catch-all and offices.
    "INTER-MUNICIPAL BUSINESS LICENCE (IMBL)": None,  # 1183  regional trading permit, held by contractors (Surrey IMBL)
    "OFFICE - GENERAL": None,  # 1065  office, NAICS 54/56
    "NOT FOR PROFIT": None,  # 326  organisations, NAICS 813
    "REAL ESTATE OR INSURANCE OFFICE": None,  # 150  NAICS 52/53
    "OFFICE - ACCOUNTANT": None,  # 127  NAICS 5412
    "OFFICE - ENGINEER": None,  # 93  NAICS 5413
    "FINANCIAL SERVICES - GENERAL": None,  # 71  NAICS 52
    "COMPUTER SERVICES - GENERAL": None,  # 67  NAICS 5415
    "OFFICE - BARRISTER & SOLICITOR": None,  # 60  NAICS 5411
    "BANK": None,  # 41  NAICS 522 (Surrey Bank)
    "TRAVEL AGENT": None,  # 33  NAICS 5615 (Surrey Travel Agency)
    "OFFICE - CARTAGE / EXPRESS": None,  # 35  transport office, NAICS 48-49
    "OFFICE - ARCHITECT": None,  # 13  NAICS 5413
    "CREDIT UNION": None,  # 10  NAICS 522
    "OFFICE - MANUFACTURER'S AGENT": None,  # 8  NAICS 4251 (Surrey Manufacturer's Agent)
    "PRIVATE PATROL AGENCY OFFICE": None,  # 6  NAICS 5616 (Surrey Security Service)
    "LUMBER BROKER - OFFICE": None,  # 1  wholesale agent, NAICS 4251
    "ADVERTISING AGENT - OFFICE": None,  # 1  NAICS 5418
    "RESEARCH/DEVELOPMENT/LAB": None,  # 85  NAICS 5417
    "PHOTOGRAPHER - STUDIO & OFFICE": None,  # 7  NAICS 5419 (Vancouver Photography Production and Rehearsal Studio)
    "PHOTOGRAPHER - MOBILE": None,  # 2  NAICS 5419, mobile
    "PRINTER": None,  # 39  NAICS 323 (Surrey Printer/Publisher)
    "TV, RADIO &/OR PRODUCTION STUDIO 1 - 50 PERSONS": None,  # 24  NAICS 512/515
    "TV, RADIO &/OR PRODUCTION STUDIO 51 - 150 PERSONS": None,  # 4  NAICS 512/515
    "TV, RADIO &/OR PRODUCTION STUDIO 151+ PERSONS": None,  # 3  NAICS 512/515
    "FILM LOCATION": None,  # 17  temporary film permit, not a premises

    # Health care and social assistance (NAICS 62).
    "HEALTH SERVICES - THERAPIST (REG'D)": None,  # 1039  RMTs, physiotherapists, counsellors: regulated health care out
    "HEALTH SERVICES - DENTIST/DENTAL SERV.": None,  # 213  NAICS 6212
    "HEALTH SERVICES - ACUPUNCTURE": None,  # 205  BC-regulated (Surrey Acupuncture)
    "HEALTH SERVICES - GENERAL": None,  # 183  clinics, naturopaths, hearing clinics, NAICS 621
    "HEALTH SERVICES - PHYSICIAN & SURGEON": None,  # 171  NAICS 6211
    "HEALTH SERVICES - CHIROPRACTOR": None,  # 100  NAICS 6213 (Surrey Professional Practitioner-Chiropractor)
    "HEALTH SERVICES - OPTOMETRIST/OPTICIAN": None,  # 39  filed under HEALTH SERVICES, mostly optometrists: out, as Surrey's Optometrist and Melbourne's opticians (filed in health); pending in the continuity table for the owner
    "HEALTH SERVICES - LABORATORY": None,  # 14  NAICS 6215 (Surrey Medical Laboratory)
    "PERSONAL CARE FACILITY - (DAYCARE - CHILDREN)": None,  # 58  child care, NAICS 6244
    "PERSONAL CARE FACILITY (ADULT NURSING HOME & SUPPORTIVE HOUSING FACILITY)": None,  # 8  NAICS 623
    "VETERINARIAN": None,  # 15  vets out (NAICS 541940)
    "ADULT SERVICES - BODY RUB PREMISES": None,  # 4  adult venue out (R3)

    # Construction trades (NAICS 23).
    "CONTRACTOR - BUILDING": None,  # 512  NAICS 23, placeholder point
    "CONTRACTOR - MISC.": None,  # 417  NAICS 23
    "CONTRACTOR - ELECTRICAL": None,  # 394  NAICS 23
    "CONTRACTOR'S SHOP AND YARD": None,  # 232  NAICS 23 base
    "CONTRACTOR - PLUMBING": None,  # 212  NAICS 23
    "CONTRACTOR - HEATING": None,  # 100  NAICS 23
    "CONTRACTOR - LANDSCAPING": None,  # 63  NAICS 5617
    "CONTRACTOR - EXCAVATING": None,  # 48  NAICS 23
    "CONTRACTOR - ROAD BUILDING": None,  # 15  NAICS 23
    "CONTRACTOR - PAINTING": None,  # 15  NAICS 23
    "CONTRACTOR - SANITARY": None,  # 8  NAICS 23/562
    "CONTRACTOR - MOVING": None,  # 4  NAICS 4842
    "CONTRACTOR - WRECKING": None,  # 3  NAICS 23

    # Wholesale, manufacturing, warehousing, fuel.
    "WAREHOUSE - GENERAL 1 - 50 PERSONS": None,  # 297  NAICS 493
    "WHOLESALER - GENERAL 1 - 50 PERSONS": None,  # 291  NAICS 42
    "MANUFACTURER - GENERAL 1 - 50 PERSONS": None,  # 253  NAICS 31-33
    "MANUFACTURER - PROCESSING FOOD 1 - 50 PERSONS": None,  # 74  NAICS 311
    "WHOLESALER - CHEMICALS, FLAMMABLES & FOOD 1 - 50 PERSONS": None,  # 63  NAICS 42
    "WAREHOUSE - CHEMICALS, FLAMMABLES & FOOD 1 - 50 PERSONS": None,  # 37  NAICS 493
    "MANUFACTURER - PROCESSING CHEMICALS OR FLAMMABLES 1 - 50 PERSONS": None,  # 16  NAICS 325
    "MANUFACTURER - GENERAL 151+ PERSONS": None,  # 10  NAICS 31-33
    "MANUFACTURER - GENERAL 51 - 150 PERSONS": None,  # 10  NAICS 31-33
    "WHOLESALER - GENERAL 51 - 150 PERSONS": None,  # 9  NAICS 42
    "OIL STORAGE PLANT & DISTRIBUTION": None,  # 9  NAICS 4247 (Surrey Petroleum Product Distributor)
    "WAREHOUSE - GENERAL 51 - 150 PERSONS": None,  # 8  NAICS 493
    "WHOLESALER - CHEMICALS, FLAMMABLES & FOOD 51 - 150 PERSONS": None,  # 7  NAICS 42
    "MANUFACTURER - PROCESSING FOOD 51 - 150 PERSONS": None,  # 5  NAICS 311
    "MANUFACTURER - PROCESSING CHEMICALS OR FLAMMABLES 51 - 150 PERSONS": None,  # 3  NAICS 325
    "MANUFACTURER - PROCESSING CHEMICALS OR FLAMMABLES 151+ PERSONS": None,  # 2  NAICS 325
    "WAREHOUSE - CHEMICALS, FLAMMABLES & FOOD 51 - 150 PERSONS": None,  # 2  NAICS 493
    "WAREHOUSE - CHEMICALS, FLAMMABLES & FOOD 151+ PERSONS": None,  # 1  NAICS 493
    "CONSTRUCTION OR EQUIPMENT DEALER": None,  # 2  NAICS 4238 (Surrey Machinery/Heavy Equipment Dealer)
    "JUNK DEALER": None,  # 8  auto wreckers and scrap, NAICS 4239 (Surrey Scrap Dealer, Automobile Wrecker)
    "OIL REFINERY": None,  # 1  NAICS 324
    "FUEL DEALER": None,  # 1  nonstore fuel dealer out (NAICS 454)
    "BEVERAGE CONTAINER RETURN CENTRE": None,  # 5  recycling depot (Surrey Recycling Depot)
    "BEER & WINE MAKING": None,  # 2  U-brew (Surrey U-Brew Premise)

    # Repair and maintenance (NAICS 811), vehicle services, rental.
    "AUTO REPAIR SHOP": None,  # 135  repairs out (NAICS 811)
    "AUTO BODY REPAIR & PAINTING": None,  # 58  repairs out (NAICS 811)
    "CAR WASH/DETAILING": None,  # 22  NAICS 811192 (Surrey Automobile Cleaning/Car Wash/Detailing)
    "TAILOR/SEAMSTRESS": None,  # 15  tailoring and alterations out (repairs rule)
    "SHOE REPAIRER": None,  # 2  shoe repair out (repairs rule)
    "UPHOLSTERER": None,  # 1  NAICS 811420 (Surrey Upholstery)
    "CAR/TRUCK RENTAL": None,  # 12  NAICS 532 (Surrey Automobile/Truck Rental)
    "AUTO TOWING/STORAGE": None,  # 5  NAICS 4884 (Surrey Towing - Storage)
    "AUTO TOW SERVICE": None,  # 3  NAICS 4884

    # Transport (NAICS 48-49).
    "PASSENGER DIRECTED VEHICLE - PER STANDARD VEHICLE": None,  # 132  taxi and ride-hail vehicles
    "PASSENGER DIRECTED VEHICLE - PER ACCESSIBLE VEHICLE": None,  # 26  taxi vehicles
    "PASSENGER DIRECTED VEHICLE OR DRIVING INSTRUCTION BUSINESS": None,  # 8  taxi firm or driving school
    "TRUCK FREIGHT COMPANY": None,  # 2  NAICS 484
    "PARKING LOT": None,  # 61  parking out (NAICS 81293)

    # Education (NAICS 61).
    "PRIVATE SCHOOL": None,  # 103  NAICS 611

    # Recreation (NAICS 71), lodging (721), halls, gambling.
    "EXERCISE STUDIO / GYM": None,  # 43  recreation out (NAICS 713940)
    "PUBLIC HALL": None,  # 13  venue (Vancouver Hall / Spectator Sports Venue)
    "HOTEL/MOTEL/AUTO COURT - PER SUITE": None,  # 11  lodging out
    "TRAILER CAMP/COURT": None,  # 1  lodging out (Surrey Tourist Trailer Park/Campsite)
    "ARCADE": None,  # 5  recreation out (Surrey Arcade)
    "THEATRE - INDOOR": None,  # 2  NAICS 711/512 (Vancouver Theatre)
    "BOWLING ALLEY": None,  # 1  recreation out
    "CURLING RINK / ICE RINK": None,  # 1  recreation out
    "CYBER CENTRES": None,  # 1  PC rooms out (recreation rule)
    "POOL HALL": None,  # 1  recreation out
    "COIN AND/OR NOTE OPERATED MACHINES": None,  # 44  vending and amusement machines out
    "VENDING MACHINE (ANY TYPE) USING A CREDIT CARD": None,  # 13  vending machines out
    "VENDING MACHINE (AMUSEMENT OR RECREATION)": None,  # 7  vending machines out

    # Mobile trade, carts and stalls.
    "MOBILE BUSINESS": None,  # 193  mobile units out, placeholder point
    "PEDDLER - FOOD": None,  # 118  mobile food out (R1)
    "PEDDLER - GENERAL (MOBILE)": None,  # 2  mobile units out (Surrey Pedlar)
    "PRIVATE PATROL & GUARD SERVICE (MOBILE)": None,  # 5  NAICS 5616, mobile
    "CART": None,  # 5  mall kiosk carts out (kiosk rule; Coquitlam mall kiosks out, owner 2026-10-02)

    # Funeral, cemetery.
    "FUNERAL SERVICES": None,  # 4  funeral out
    "CEMETERY": None,  # 2  funeral out
}

# --- Coquitlam: `U_SUBCODEDESC` (regional extension, 2026-10-03) -----------
# Every subtype on the Issued and Renewal rows (64 values; the blank subtype on
# Sidewalk Use Permits returns None). Counts are licences after collapsing the
# layer's double listing. Coquitlam licenses home occupations under their own
# subtypes, so the kept subtypes are premises licences. Name-level carve-outs
# inside a kept subtype (caterers, a mobile hairdresser) and the mall kiosk
# with a "Kiosk" unit are in pipeline/vancouver/coquitlam.py. Mall kiosks are
# out (owner, 2026-10-02).
COQUITLAM_BUCKETS = {
    # --- Retail (NAICS 44-45) ---------------------------------------------
    "Retail Sales": RETAIL,                     # 389  general retail, the Sales licence type
    "Motor Vehicle Sales": RETAIL,              #  39  car dealers, R4 (Surrey's Automobile Dealer kept whole); a few brokers and wholesalers inside, kept whole
    "Auto Service Station": RETAIL,             #  21  petrol stations, R4; 4 are lube or car-wash bays, and a type that merges fuel with repair or a wash goes whole (Edmonton, Philadelphia)
    "Cannabis Retail Business": RETAIL,         #   6  cannabis stores (Vancouver's Retail Dealer - Cannabis)

    # Mall kiosks: LEFT OUT (owner, 2026-10-02, Vancouver (Regional) brief
    # call 3). Four of the nine are lottery counters, out anyway under R5.
    "Retail Sales - Kiosk": None,               #   9  owner call: mall kiosks out

    # --- Food service (NAICS 722) -----------------------------------------
    "Restaurant Sales": FOOD,                   # 339  restaurants, cafes, pubs; 7 contract-caterer licences carved out by name in the loader (R1)

    # --- Personal services (NAICS 812) ------------------------------------
    "Personal Grooming Services": PERSONAL,     # 233  salons, barbers, nails, estheticians, laser and skin clinics (812199); 1 mobile hairdresser carved out in the loader
    "Cleaning/Dying/Laundry Plant": PERSONAL,   #   8  dry cleaners and laundries (Vancouver's Laundry Services, Surrey's Dry Cleaner/Laundry Service)

    # --- Catch-alls and a high-impact licence: out, by precedent ----------
    # A fee-level catch-all inside General Services, alongside the older
    # named subtypes (not a replacement scheme: both are issued in 2025-26).
    # Holds storefronts (a furniture superstore, two pet-supply chains, pet
    # and people groomers, a nail lounge, bakeries, a bubble-tea shop, a
    # courier counter, petrol stations already licensed under Auto Service
    # Station) mixed with driving schools, movers, accountants, caterers,
    # dog walkers, bottle depots and care agencies. Out whole, the catch-all
    # precedent (Surrey's Miscellaneous and its IMBLs, R2); no built city
    # dispatches a catch-all by name.
    "Level 2": None,                            # 176  catch-all, out (R2)
    # Same fee-level scheme, smallest tier: mostly residential addresses
    # (a home-based shape), with a barber and a trading-card shop. Out, as
    # Level 2.
    "Level 1": None,                            #  35  catch-all, out (R2)
    # Its own licence type, "High Impact Businesses", separate from Personal
    # Grooming where ordinary spas sit. category_rules.md keeps commercial
    # massage (Personal services) but leaves out premises the register names
    # as adult or body-rub (R3; San Diego's "massage parlors", Calgary's
    # body-rub centres). The register says "high impact", not "adult".
    # Out, following San Diego's own "massage parlors" type (R3).
    "Massage (non-registered) Parlours": None,  #   1  R3, San Diego's massage parlors

    # --- Not storefronts ----------------------------------------------------
    # Fee-level tier 3: kinesiologists and other health practitioners, many
    # under a person's own name in a shared clinic (NAICS 621, and a
    # practitioner's own licence, category_rules.md).
    "Level 3": None,                            #  64  health practitioners, 621

    # Professional, office and finance (NAICS 52-56).
    "Professional": None,                       # 1345  professional offices
    "Consultants - Without Commercial Office": None,  # 243  no premises
    "Consultants - With Commercial Office": None,     #  36  NAICS 541
    "Business Office": None,                    #  71  offices
    "Real Estate/Insurance Office": None,       #  66  NAICS 52-53
    "Travel Agency": None,                      #  18  NAICS 5615 (Surrey's Travel Agency None)
    "General": None,                            #  84  banks and currency exchanges (Financial Institutions) and industrial general; NAICS 52
    "Professional - Other": None,               #   1  professional office
    "Professionals - Engineer": None,           #   1  NAICS 5413
    "Film Production Company": None,            #   3  NAICS 512
    "Patrol Service/Security Service": None,    #   2  NAICS 5616
    "Building Mgmt - Commercial (Bus. Lic.)": None,   # 4  NAICS 531
    "Building Mgmt - Residential (Bus. Lic.)": None,  # 3  NAICS 531
    "Photographic Studio": None,                #  11  NAICS 5419 (Vancouver's Photography Studio None)
    "Photographic/Mobile": None,                #  15  mobile photographers, 5419

    # Home occupations, residential care and lodging.
    "Home Occupation - Level 1": None,          # 428  home-based, not a storefront
    "Home Occupation - Level 2": None,          #  62  home-based, not a storefront
    "Day Care Centre - Residential(Bus. Lic.)": None,  # 160  home day care, NAICS 624
    "Day Care Centre - Commercial (Bus. Lic.)": None,  #  74  NAICS 624
    "Bed & Breakfast": None,                    # 217  lodging, out
    "Room Rentals": None,                       #  83  residential tenancy and lodging
    "Trailer Courts": None,                     #   3  lodging and residential land
    "Hospital": None,                           #   4  care homes, NAICS 623

    # Construction, manufacturing, wholesale, warehousing, resources.
    "Contractor Licence -Without Comm. Office": None,  # 770  NAICS 23, no premises
    "Contractor Licence -With Comm. Office": None,     # 217  NAICS 23
    "Manufacturer": None,                       # 139  NAICS 31-33
    "Warehouse": None,                          # 136  NAICS 493
    "Wholesale Sales": None,                    #  75  NAICS 42
    "Quarry/Gravel Pit": None,                  #   5  NAICS 212
    "Cannabis Manufacturer": None,              #   2  NAICS 31-33

    # Repair and maintenance (NAICS 811, not 812).
    "Repair Shop/Mobile Repair": None,          # 102  repairs out
    "Service Repair Person": None,              #  11  repairs out
    "Auto Wrecker": None,                       #   1  NAICS 4231 / 811

    # Transport, towing, rentals and parking.
    "Towing - Without Storage": None,           #   7  NAICS 4884
    "Towing - With Storage": None,              #   3  NAICS 4884
    "For Hire": None,                           #   4  taxis and limousines, 485
    "Rental Vehicles": None,                    #   5  NAICS 532
    "Equipment/Personal Property Rentals": None,  # 11  NAICS 532 (Vancouver's Rental Services None)
    "Auto Parking Lot": None,                   #  14  parking out

    # Education (NAICS 61).
    "Commercial School": None,                  #  53  NAICS 611
    "Private Teacher": None,                    #  45  NAICS 611
    "Private Teacher - Tutoring": None,         #   2  NAICS 611

    # Recreation (NAICS 71) and gambling.
    "Recreation/Entertainment/Health/Wellness Service or Facility": None,  # 92  gyms, martial arts, yoga, pilates, dance, rinks, play centres; recreation out
    "Golf Course": None,                        #   3  recreation out
    "Billiard Room": None,                      #   1  recreation out
    "Bowling Alley": None,                      #   1  recreation out
    "Theatre/Concert Hall": None,               #   1  recreation out
    "Casino": None,                             #   1  gambling out, R5

    # Mobile trade, vending and machines.
    "Vending - Miscellaneous": None,            #  26  vending machines out
    "Vending - ATM": None,                      #  10  machines out
    "Private Property - Annual": None,          #   6  food trucks and carts on private land (Vehicle Vendor type), mobile out
    "Special Event Vending": None,              #   2  event stalls out, R1
}

BUCKETS_BY_SOURCE = {
    "vancouver": VANCOUVER_BUCKETS,
    "surrey": SURREY_BUCKETS,
    "burnaby": BURNABY_BUCKETS,
    "coquitlam": COQUITLAM_BUCKETS,
}
# New Westminster classifies by NAICS (its licences carry the code), shown as
# "NAICS <code>" in the tooltip: classify() reads the code back.
NAICS_SOURCES = ("new_westminster",)
_NAICS_VALUE = re.compile(r"^NAICS (\d+)$")


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).

    `row` must carry `category` (one registry's own single category string)
    and `source` (which registry). RAISES on an unknown category rather than
    returning None: a value this module has never seen is a data change that
    must be looked at, not silently dropped from the map. That is the
    project's convention - see dc_businessactivity.classify.
    """
    source = row.get("source")
    if source in NAICS_SOURCES:
        m = _NAICS_VALUE.match(str(row.get(VALUE_COLUMN) or "").strip())
        return naics.naics_group(m.group(1)) if m else None
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
