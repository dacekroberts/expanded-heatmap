"""Los Angeles (Regional): the City of Los Angeles and Long Beach, two
municipal registries dispatched on a `source` column, like Vancouver + Surrey.

WHY A DISPATCHING MODULE. The City of LA's register carries NAICS codes;
Long Beach's "Business Licenses Public View" carries its own licence
categories (`LICCATDESC`, 232 values on the active, in-city, not-home-based
file of 2026-10-03). One map has one `TAXONOMY_SYSTEM`, so `classify()`
dispatches on the source:

    los_angeles   naics.naics_group() on the row's `naics` code - exactly
                  the NAICS city build, the 812990 catch-all still dropped by
                  step 2 (config.NAICS_EXCLUDE_CODES)
    long_beach    LONG_BEACH_BUCKETS below

`VALUE_COLUMN` holds each registry's own words for the tooltip: "NAICS
<code>" for LA (the code the NAICS build showed) and Long Beach's category
string. `FIELD_LABEL` is the shared "Category".

HOW LONG BEACH'S BUCKETS WERE DECIDED. Anchored on naics.py, as Vancouver's
are (Retail NAICS 44-45 less 454, Food service 722, Personal services 812
less 8122, 81293 and the 812990 catch-all), then docs/category_rules.md row
by row. Each value carries its reason. The calls with a precedent outside
NAICS:
  * chair, booth and practitioner licences are out (the shop's own licence
    keeps the shop): Barber/Beauty (booth ), Nails/Manicure -Booth,
    Massage/Body Wrap Tech;
  * cannabis dispensaries are Retail (Boston, Calgary, Edmonton);
  * Business Equipment Sales/Rental and Vehicle Parts with Installation go
    whole to Retail (the mixed-type precedents);
  * event caterers, carts, stands, sidewalk vendors and farmers' markets
    are out (R1, mobile units);
  * "General Services - Other" is the register's catch-all, out (R2).
A value this module has never seen RAISES (dc_businessactivity's
convention): a new Long Beach category is looked at, never guessed.
"""
from pipeline.taxonomies import naics

FIELD_LABEL = "Category"
VALUE_COLUMN = "category"
# `naics` carries LA's code for classify(); `source` picks the registry.
EXTRA_COLUMNS = ("source", "naics")

BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]

RETAIL = "Retail"
FOOD = "Food service"
PERSONAL = "Personal services"


def legend_label(bucket: str) -> str:
    """Taxonomy-module interface: legend text for a bucket. Plain bucket
    names: NAICS's code prefixes would mislabel Long Beach's pins."""
    return bucket


# --- Long Beach: LICCATDESC, every value on the 2026-10-03 file -------------
# Count is that file's rows (active, in-city, not home-based), before any
# placement or de-duplication.
LONG_BEACH_BUCKETS = {
    'Accounting': None,                                    #    57  professional or health (NAICS 54/62)
    'Acupuncture': None,                                   #    35  professional or health (NAICS 54/62)
    'Adult-Use Cannabis Cultivation': None,                #    77  not NAICS 812 retail-facing
    'Adult-Use Cannabis Cultivation Equity': None,         #     3  not NAICS 812 retail-facing
    'Adult-Use Cannabis Dispensary': RETAIL,               #    96  cannabis stores Retail (Boston, Calgary, Edmonton; NAICS 459991)
    'Adult-Use Cannabis Dispensary Equity': RETAIL,        #     9  cannabis stores Retail (as above); the City's equity-programme licence
    'Adult-Use Cannabis Distribution': None,               #    85  not NAICS 812 retail-facing
    'Adult-Use Cannabis Distribution Equity': None,        #     1  not NAICS 812 retail-facing
    'Adult-Use Cannabis Manufacturing': None,              #    84  not NAICS 812 retail-facing
    'Advertising': None,                                   #    15  not NAICS 812 retail-facing
    'Aesthetician': PERSONAL,                              #    41  NAICS 812112; estheticians kept (Vancouver, D.C., Kitchener-Waterloo); no booth type exists for it, unlike barbers' and nails'
    'Aircraft Rental': None,                               #     5  not NAICS 812 retail-facing
    'Aircraft Repair/Repair': None,                        #     9  not NAICS 812 retail-facing
    'Aircraft Sales': RETAIL,                              #     1  vehicle dealers kept (R4), NAICS 441228
    'Alarm Installation/Sales': None,                      #     1  not NAICS 812 retail-facing
    'Amusement Machines': None,                            #     3  vending/amusement machines out
    'Antique Store': RETAIL,                               #     8  NAICS 459510
    'Apartment House': None,                               #  6612  real estate (NAICS 53)
    'Appliance Repair - Small / Electronics': None,        #     7  repair (811210)
    'Appliance Repair – Major': None,                      #     1  repair (811412)
    'Appliance Sales - Major Household': RETAIL,           #     3  NAICS 449210
    'Arcade': None,                                        #     4  recreation (71)
    'Architecture': None,                                  #    48  professional or health (NAICS 54/62)
    'Art Restoration': None,                               #     1  not NAICS 812 retail-facing
    'Artist Studio (Comml)': None,                         #    10  not a storefront trade
    'Attorney': None,                                      #   287  professional or health (NAICS 54/62)
    'Auto Detailing': None,                                #     8  not NAICS 812 retail-facing
    'Auto Repair - Minor, Tune-Up, Smog Test': None,       #   103  not NAICS 812 retail-facing
    'Auto Repair – General': None,                         #   163  not NAICS 812 retail-facing
    'Auto Wrecking/Salvage': None,                         #     1  not NAICS 812 retail-facing
    'Auto/Boat Sales': RETAIL,                             #    48  car dealers kept (R4)
    'Bar, Tavern, Lounge': FOOD,                           #    77  NAICS 722410
    'Barber/Beauty (booth )': None,                        #   232  a chair renter's licence; the shop's own keeps the shop
    'Barber/Beauty Shop Owner': PERSONAL,                  #   445  NAICS 812111/812112; the shop's own licence
    'Bed & Breakfast': None,                               #     2  not NAICS 812 retail-facing
    'Bingo': None,                                         #    10  gambling out (R5)
    'Boat Cleaning/Repair (Mobile Service)': None,         #     6  mobile service
    'Boat Repair': None,                                   #     2  not NAICS 812 retail-facing
    'Boats - Charter/Cruise/Taxi': None,                   #    21  not NAICS 812 retail-facing
    'Bookkeeping': None,                                   #     9  not NAICS 812 retail-facing
    'Business Equipment Repair': None,                     #     4  repair (811310)
    'Business Equipment Sales/Rental': RETAIL,             #     8  mixed sale and rental, kept whole as Retail (Vancouver's RETAIL SALE, RENTAL & REPAIR, owner 2026-10-02)
    'Business Office': None,                               #   670  not NAICS 812 retail-facing
    'Business/Professional School': None,                  #    29  not NAICS 812 retail-facing
    'Car Wash': None,                                      #    45  not NAICS 812 retail-facing
    'Carpet/Drapery Cleaning': None,                       #     4  mobile service
    'Catering/Party Consulting': None,                     #    97  event caterers out (R1), as Vancouver's Caterer
    'Check Cashing': None,                                 #    15  not NAICS 812 retail-facing
    'Chiropractics': None,                                 #    55  professional or health (NAICS 54/62)
    'Cleaning Agency': None,                               #    14  not NAICS 812 retail-facing
    'Commercial/Industrial Space  Rental': None,           #  2782  real estate (NAICS 53)
    'Communication Facility - Cell Site': None,            #   166  not NAICS 812 retail-facing
    'Computer Programming/Consulting': None,               #    23  not NAICS 812 retail-facing
    'Consulting': None,                                    #   201  not NAICS 812 retail-facing
    'Contracting - Misc.': None,                           #    47  construction (NAICS 23)
    'Contracting - Security Alarms': None,                 #     1  construction (NAICS 23)
    'Contracting – Building': None,                        #    77  construction (NAICS 23)
    'Contracting – Cement': None,                          #     3  construction (NAICS 23)
    'Contracting – Electrical': None,                      #    16  construction (NAICS 23)
    'Contracting – Engineering': None,                     #    42  construction (NAICS 23)
    'Contracting – Lathing': None,                         #     1  construction (NAICS 23)
    'Contracting – Masonry': None,                         #     1  construction (NAICS 23)
    'Contracting – Painting': None,                        #     1  construction (NAICS 23)
    'Contracting – Plumbing': None,                        #    18  construction (NAICS 23)
    'Contracting – Refrigeration': None,                   #     2  construction (NAICS 23)
    'Contracting – Roofing': None,                         #     4  construction (NAICS 23)
    'Contracting – Sewer': None,                           #     2  construction (NAICS 23)
    'Convalescent Hospital or Home': None,                 #    35  not NAICS 812 retail-facing
    'Dance Studio': None,                                  #    13  not NAICS 812 retail-facing
    'Day Care/Adult': None,                                #    15  not NAICS 812 retail-facing
    'Day Care/Preschool': None,                            #    68  not NAICS 812 retail-facing
    'Dental Office': None,                                 #   115  professional or health (NAICS 54/62)
    'Dentist': None,                                       #    82  professional or health (NAICS 54/62)
    'Direct Sales Product Distribution': None,             #     3  nonstore (NAICS 454)
    'Drafting/Graphics Design': None,                      #    22  not NAICS 812 retail-facing
    'Dry Cleaner': PERSONAL,                               #    20  NAICS 812320
    'Dry Cleaning Plant': PERSONAL,                        #    22  NAICS 812320 (no precedent names a plant; anchored on the code)
    'Elementary/Secondary School': None,                   #    13  not NAICS 812 retail-facing
    'Employment Agency': None,                             #    47  not NAICS 812 retail-facing
    'Employment Agent': None,                              #     3  not NAICS 812 retail-facing
    'Engineering': None,                                   #    34  professional or health (NAICS 54/62)
    'Escrow Company': None,                                #     8  not NAICS 812 retail-facing
    'Farmers Market': None,                                #     7  market stalls out (R1)
    'Financial Institutions': None,                        #    13  finance (52)
    'Financial Services – Other': None,                    #    61  not NAICS 812 retail-facing
    'Fitness Center/Health Club': None,                    #   112  not NAICS 812 retail-facing
    'Flower Shop': RETAIL,                                 #    34  NAICS 459310
    'Flower/Newspaper Stand': None,                        #     2  a kiosk stand, out
    'Food Delivery': None,                                 #     1  no counter (R1)
    'Food Processing': None,                               #    22  manufacturing (31-33)
    'Food Retail Store': RETAIL,                           #   244  NAICS 445
    'Food Retail Store w/ Alcohol': RETAIL,                #   218  NAICS 445
    'Food Vending Carts': None,                            #     4  kiosk carts out
    'Freight Forwarding': None,                            #     8  not NAICS 812 retail-facing
    'Gardening/Landscape Maint.': None,                    #     9  mobile service
    'Gas Station': RETAIL,                                 #    96  petrol stations kept (R4)
    'General Services – Other': None,                      #   314  the register's services catch-all, out (R2)
    'Hall Rental': None,                                   #    18  not NAICS 812 retail-facing
    'Handyman': None,                                      #     8  mobile service
    'Hardware Store with Building Materials': RETAIL,      #     5  NAICS 444
    'Hardware Store without Building Materials': RETAIL,   #     2  NAICS 444140
    'Heavy Equipment Repair': None,                        #     4  not NAICS 812 retail-facing
    'Horse Stable/Riding Academy': None,                   #     4  not NAICS 812 retail-facing
    'Hospital': None,                                      #     8  not NAICS 812 retail-facing
    'Hotel': None,                                         #    32  not NAICS 812 retail-facing
    'Import/Export - Office Use': None,                    #    19  not NAICS 812 retail-facing
    'Instructor/Personal Trainer': None,                   #    60  not NAICS 812 retail-facing
    'Insurance Broker': None,                              #    76  not NAICS 812 retail-facing
    'Insurance Companies': None,                           #    18  finance (52)
    'Interior Design': None,                               #     4  not NAICS 812 retail-facing
    'Internet Sales/Service': None,                        #    18  nonstore (NAICS 454)
    'Itinerant Vendor': None,                              #     2  mobile trade, out
    'Janitorial Service': None,                            #    12  mobile service
    'Jewelry Repair': None,                                #     1  repair (811490)
    'Jewelry Store': RETAIL,                               #    14  NAICS 458310
    'Kennel - Boarding Only': PERSONAL,                    #    14  NAICS 812910 pet care (Calgary, Edmonton, Dublin)
    'Laboratory - Medical/Dental': None,                   #    20  not NAICS 812 retail-facing
    'Laboratory – Other': None,                            #     6  not NAICS 812 retail-facing
    'Laundromat': PERSONAL,                                #    81  NAICS 812310
    'Laundry - CommercialCustomers': None,                 #     1  not NAICS 812 retail-facing
    'Laundry Service': PERSONAL,                           #     2  NAICS 812320
    'Locksmith': None,                                     #     6  NAICS 561622
    'Machine Shop/Welding': None,                          #    11  manufacturing (31-33)
    'Mail Order': None,                                    #     1  nonstore (NAICS 454)
    'Mailbox Rental': None,                                #    17  not NAICS 812 retail-facing
    'Manufacturing': None,                                 #   127  manufacturing (31-33)
    'Marketing': None,                                     #    21  not NAICS 812 retail-facing
    'Martial Arts Studio': None,                           #    19  not NAICS 812 retail-facing
    'Massage/Body Wrap Estab': PERSONAL,                   #    44  commercial massage kept (category_rules); the establishment's licence
    'Massage/Body Wrap Tech': None,                        #    25  a practitioner's licence; the establishment's keeps the shop
    'Medical Cannabis Cultivation': None,                  #    56  not NAICS 812 retail-facing
    'Medical Cannabis Delivery': None,                     #     2  delivery, nonstore
    'Medical Cannabis Dispensary': RETAIL,                 #   100  cannabis stores Retail (as above)
    'Medical Cannabis DispensaryEquity': RETAIL,           #     9  cannabis stores Retail (as above); the City's equity-programme licence
    'Medical Cannabis Distribution': None,                 #    82  not NAICS 812 retail-facing
    'Medical Cannabis Lab Testing': None,                  #     5  not NAICS 812 retail-facing
    'Medical Cannabis Manufacturing': None,                #    72  not NAICS 812 retail-facing
    'Medical Office/Clinic': None,                         #   346  professional or health (NAICS 54/62)
    'Medical Transportation -Ambulance': None,             #     2  not a storefront trade
    'Medical Transportation -Wheelchair/Gurney': None,     #     1  not a storefront trade
    'Mobile Food Vending': None,                           #    33  mobile units out
    'Mobile Home Park': None,                              #    14  not NAICS 812 retail-facing
    'Mobile Services - Misc.': None,                       #    19  mobile service
    'Mortuary': None,                                      #    10  funeral (8122) out
    'Motel': None,                                         #    85  not NAICS 812 retail-facing
    'Motorcycle/Jet Ski Repair': None,                     #     2  not NAICS 812 retail-facing
    'Motorcycle/Jet Ski Sales': RETAIL,                    #     2  vehicle dealers kept (R4), NAICS 441228
    'Movie / Live Theater': None,                          #     6  not a storefront trade
    'Museum': None,                                        #     4  not NAICS 812 retail-facing
    'Nails/Manicure -Booth': None,                         #     9  a booth renter's licence
    'Nails/Manicure Shop': PERSONAL,                       #   142  NAICS 812113; the shop's own licence
    'Nursery': RETAIL,                                     #     4  NAICS 444240 garden centre
    'Nursery-Wholesale': None,                             #     3  wholesale (42)
    'Nurses Registry': None,                               #     6  not NAICS 812 retail-facing
    'Ophthalmologist': None,                               #     9  professional or health (NAICS 54/62)
    'Optician': RETAIL,                                    #     3  NAICS 456130; opticians kept (category_rules)
    'Optometry': None,                                     #    31  professional or health (NAICS 54/62)
    'Parking Service Lot': None,                           #   107  parking out
    'Pawn Shop': RETAIL,                                   #     5  pawnbrokers kept (category_rules R5)
    'Pest Control': None,                                  #     2  not NAICS 812 retail-facing
    'Pet Grooming': PERSONAL,                              #    36  NAICS 812910
    'Pet Shop': RETAIL,                                    #    10  NAICS 459910
    'Pet Sitting': None,                                   #     2  mobile service
    'Pharmacy': RETAIL,                                    #    58  NAICS 456110; pharmacies kept (category_rules)
    'Photocopying': None,                                  #     3  not NAICS 812 retail-facing
    'Photography Studio': None,                            #     3  not NAICS 812 retail-facing
    'Photography – Freelance': None,                       #     1  not NAICS 812 retail-facing
    'Physical Therapy': None,                              #    38  professional or health (NAICS 54/62)
    'Physician/Surgeon': None,                             #   161  professional or health (NAICS 54/62)
    'PIA Only': None,                                      #    25  not a trade (an administrative licence type)
    'Podiatry': None,                                      #     9  professional or health (NAICS 54/62)
    'Printing – Offset': None,                             #     9  not NAICS 812 retail-facing
    'Private Patrol Operator': None,                       #    10  not NAICS 812 retail-facing
    'Private Waste Collection – Health': None,             #     1  not NAICS 812 retail-facing
    'Professional Services - Other': None,                 #   195  professional or health (NAICS 54/62)
    'Promoting': None,                                     #    22  not NAICS 812 retail-facing
    'Property Management': None,                           #    81  not NAICS 812 retail-facing
    'Psychiatry': None,                                    #    26  professional or health (NAICS 54/62)
    'Psychology': None,                                    #   102  professional or health (NAICS 54/62)
    'Real Estate Agent': None,                             #     1  not NAICS 812 retail-facing
    'Real Estate Office': None,                            #    81  not NAICS 812 retail-facing
    'Recreation - Misc.': None,                            #    12  recreation (71)
    'Recreational Vehicle Storage': None,                  #     1  not NAICS 812 retail-facing
    'Recycling Center': None,                              #     1  not NAICS 812 retail-facing
    'Recycling Processor': None,                           #     6  not NAICS 812 retail-facing
    'Rentals - Misc.': None,                               #    34  not NAICS 812 retail-facing
    'Residential Care Facility': None,                     #    33  not NAICS 812 retail-facing
    'Restaurant & Ready to Eat Foods': FOOD,               #   949  NAICS 7225
    'Restaurant & Ready to Eat Foods with Alcohol': FOOD,  #   433  NAICS 7225
    'Retail Sales': RETAIL,                                #   623  NAICS 44-45
    'Retail Sales – Used Merchandise': RETAIL,             #    42  NAICS 459510
    'Sales Representative': None,                          #    11  not NAICS 812 retail-facing
    'Seasonal Sales': None,                                #     1  a temporary lot, out
    'Self Storage': None,                                  #    19  not NAICS 812 retail-facing
    'Shelter': None,                                       #     5  not NAICS 812 retail-facing
    'Shoe Repair': None,                                   #     2  repair (NAICS 811430)
    'Sidewalk Vending - Food': None,                       #    18  street stalls out (R1)
    'Sidewalk Vending - Merchandise': None,                #    27  street stalls out
    'Social Club': None,                                   #    10  recreation (71)
    'Social Service with Food Distribution': None,         #    17  not NAICS 812 retail-facing
    'Social Service without Food Distribution': None,      #    26  not NAICS 812 retail-facing
    'Soliciting': None,                                    #     4  door-to-door, nonstore (NAICS 454)
    'Stocks & Bonds Broker': None,                         #    12  not NAICS 812 retail-facing
    'Swimming Pool Cleaning': None,                        #     1  mobile service
    'Tailoring': None,                                     #    10  alterations (NAICS 811490)
    'Tanning Salon': PERSONAL,                             #     4  NAICS 812199
    'Tattoos/Body Piercing': PERSONAL,                     #    65  tattoo kept where it has its own type (R2)
    'Tax Preparation': None,                               #    77  not NAICS 812 retail-facing
    'Ticket Office': None,                                 #     5  not NAICS 812 retail-facing
    'Tire Store': RETAIL,                                  #    16  NAICS 441340
    'Towing': None,                                        #     5  not NAICS 812 retail-facing
    'Towing (Out of Town)': None,                          #     1  mobile service
    'Towing with Impound': None,                           #    11  not NAICS 812 retail-facing
    'Transfer Station': None,                              #     1  not NAICS 812 retail-facing
    'Transportation Facility (Fleet Facility)': None,      #    20  not NAICS 812 retail-facing
    'Travel Agency': None,                                 #    12  not NAICS 812 retail-facing
    'Upholstery Svc – Furn/Auto': None,                    #     6  repair (811420)
    'Utilities': None,                                     #     2  not NAICS 812 retail-facing
    'Valet Service': None,                                 #     6  not NAICS 812 retail-facing
    'Vehicle for Hire -(PUC-Regulated)': None,             #     1  not a storefront trade
    'Vehicle Parts with Installation': RETAIL,             #    15  a type merging parts sales with fitting goes whole as Retail (R4: Edmonton, Philadelphia)
    'Vehicle Parts without Installation': RETAIL,          #    25  NAICS 441330
    'Vehicle Rental Agency': None,                         #    24  not a storefront trade
    'Vending Machines': None,                              #    14  vending machines out
    'Veterinarian': None,                                  #     8  professional or health (NAICS 54/62)
    'Veterinary Clinic with Boarding': None,               #     4  professional or health (NAICS 54/62)
    'Veterinary Clinic without Boarding': None,            #    25  professional or health (NAICS 54/62)
    'Warehousing': None,                                   #    70  real estate (NAICS 53)
    'Watch Repair': None,                                  #     1  repair (811490)
    'Water Retail': RETAIL,                                #     5  NAICS 445298 water stores
    'Wholesale': None,                                     #   134  wholesale (42)
    'Writing': None,                                       #     2  not NAICS 812 retail-facing
}


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py).

    `row` carries `source`, `category` and, for LA's rows, `naics`. RAISES on
    an unknown source or Long Beach category."""
    source = row.get("source")
    if source == "los_angeles":
        code = row.get("naics")
        return naics.naics_group(code) if code else None
    if source != "long_beach":
        raise KeyError(f"unknown source {source!r}; expected 'los_angeles' or 'long_beach'")
    value = row.get(VALUE_COLUMN)
    if value is None or not str(value).strip():
        return None
    value = str(value).strip()
    if value not in LONG_BEACH_BUCKETS:
        raise KeyError(f"long_beach: category {value!r} is not in this module's mapping. Add it "
                       f"with a bucket or an explicit None and a reason.")
    return LONG_BEACH_BUCKETS[value]
