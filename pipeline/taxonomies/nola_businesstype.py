"""New Orleans taxonomy - the `businesstype` field of the City's Active
Occupational Licenses (data.nola.gov `iqay-p646`, CC0), not a NAICS code.

ONE LEVEL, 486 VALUES, EACH WITH AN EXPLICIT HOME (premises-taxonomy, measured
2026-09-30 on the full register, 16,521 active licences). The values are
NAICS-era industry TITLES with no codes, often inverted and misspelt ("Clothing
Stores, Other", "Lessors of Residential Bulidings"), plus a dozen of the City's
own permit types ("Flea Market", "Special Events-Other (Vendor)", "Video Draw
Poker Devices"). Only 187 of the 486 match a NAICS 2017 or 2022 title exactly
(6,066 licences); with the inversion and the typos undone, 341. So each value
is mapped here to the NAICS code its title names, and `naics.py` decides the
bucket - the shared carve-outs (caterers, mobile food, parking, the R2
catch-all, non-store sellers) then hold here exactly as in every NAICS city.
Where a value is not a NAICS industry at all, it maps to None with its reason.

THE CATCH-ALL TRAP: "Personal Services, Other" (249) is NAICS's "Other Personal
Services" title, which matches the 4-DIGIT group 8129 - and 8129 is Personal
services, pet care included. It is the 812990 catch-all (R2, owner
2026-09-29), coded so here and asserted below. Catch-all share, declared in
the brief (`new-orleans-catchall-share`): 676 of 16,521 (4.1%), counting the two
"all other" store types NAICS keeps.

CHECKED, OUT, NOT NAICS: the brief's two ("Special Events-Other (Vendor)",
"Home Based-Office Use Only"), the festival and Carnival vendors, "Flea Market"
(stalls at a market, most at the French Market: category_rules R1's "a market
building's stalls and stands are not" kept), street artists, video-poker
devices, short-term rentals. PAWNSHOPS stay Retail (R5) although NAICS files
them as lenders (522298).

Unknown values RAISE: a new type stops step 2 rather than vanishing.
"""

from pipeline.taxonomies.naics import naics_group

FIELD_LABEL = "Business type"
VALUE_COLUMN = "businesstype"

# businesstype (exact, stripped) -> the NAICS code its title names, or None
# where it is not a NAICS industry this project counts (reason beside it).
# Grouped by the bucket naics.py gives the code; counts are active licences,
# 2026-09-30.
TYPE_TO_NAICS = {
    # --- Food service (5 types, 1,808 licences) ----------
    'Full Service Restaurants(table service available)': '722511',  # 983
    'Drinking Places(Alcoholic Beverages)': '722410',  # 410
    'Limited Service Restaurants(no table service available)': '722513',  # 364
    'Snack & Nonalcoholic Beverage Bars': '722515',  # 37
    'Cafeterias': '722514',  # 14
    # --- Retail (63 types, 2,452 licences) ----------
    'Miscellaneous Store Retailers(except Tobacco), All Other': '453998',  # 290
    'Art Dealers': '453920',  # 185
    'Convenience Stores': '445120',  # 168
    'Clothing Stores, Other': '448190',  # 156
    'General Merchandise Stores, All Other': '452319',  # 137
    'Supermarket & Other Grocery(except Convenience) Stores': '445110',  # 119
    'Gift, Novelty & Souvenir Stores': '453220',  # 116
    'Cosmetics, Beauty Supplies & Perfume Stores': '446120',  # 100
    'Gasoline Stations with Convenience Stores': '447110',  # 76
    "Women's Clothing Stores": '448120',  # 75
    'Jewelry Stores': '448310',  # 72
    'Pharmacies & Drug Stores': '446110',  # 62
    'Baked Goods Stores': '445291',  # 56
    'Home Furnishing Stores, All Other': '442299',  # 53
    'Clothing Accessories Stores': '448150',  # 50
    'Family Clothing Stores': '448140',  # 46
    'Furniture Stores': '442110',  # 39
    'Tobacco Stores': '453991',  # 38
    'Florists': '453110',  # 36
    'Book Stores': '451211',  # 35
    'Used Merchandise Stores': '453310',  # 32
    'Automotive Parts & Accessories Stores': '441310',  # 30
    'Confectionery & Nut Stores': '445292',  # 29
    'Radio, TV & Other Electronics Stores': '443142',  # 29
    'Specialty Food Stores, All Other': '445299',  # 28
    'Beer, Wine & Liquor Stores': '445310',  # 27
    'Shoe Stores': '448210',  # 26
    'Health & Personal Care Stores, All Other': '446199',  # 23
    'Tire Dealers': '441320',  # 23
    'Building Material Dealers, Other': '444190',  # 21
    'Used Car Dealers': '441120',  # 18
    "Men's Clothing Stores": '448110',  # 16
    'Pet & Pet Supplies Stores': '453910',  # 15
    'Sporting Goods Stores': '451110',  # 15
    'Boat Dealers & Marine Supplies': '441222',  # 14
    'Sewing, Needlework & Piece Goods Stores': '451130',  # 14
    'Nursery & Garden Centers': '444220',  # 13
    'Fish & Seafood Markets': '445220',  # 12
    'Computer & Software Stores': '443142',  # 11
    "Children's & Infants' Clothing Stores": '448130',  # 10
    'Fruit & Vegetable Markets': '445230',  # 10
    'Hardware Stores': '444130',  # 10
    'Optical Goods Stores': '446130',  # 10
    'Gasoline Stations, Other': '447190',  # 9
    'Hobby, Toy & Game Stores': '451120',  # 9
    'Meat Markets': '445210',  # 9
    'Food(Health) Supplement Stores': '446191',  # 8
    'Office Supplies & Stationery Stores': '453210',  # 8
    'Paint & Wallpaper Stores': '444120',  # 8
    'Musical Instrument & Supplies Stores': '451140',  # 7
    'Pawnshops': '522298',  # 7 - R5: pawnbrokers kept Retail where the register names them (NAICS files them as lenders)
    'Motor Vehicle Dealers, All Other': '441228',  # 6
    'Prerecorded Tape, CD & Record Stores': '451220',  # 6
    'Camera & Photographic Supplies Stores': '443130',  # 5
    'Household Appliance Stores': '443141',  # 5
    'New Car Dealers': '441110',  # 5
    'Floor Covering Stores': '442210',  # 3
    'Luggage & Leather Goods Stores': '448320',  # 3
    'Motorcycle Dealers': '441221',  # 3
    'Department Stores': '452210',  # 2
    'Outdoor Power Equipment Stores': '444210',  # 2
    'Home Centers': '444110',  # 1
    'Window Treatment Stores': '442291',  # 1
    # --- Personal services (8 types, 710 licences) ----------
    'Beauty Salons': '812112',  # 278
    'Personal Care Services, Other': '812199',  # 129
    'Nail Salons': '812113',  # 113
    'Barber Shops': '812111',  # 105
    'Coin-Operated Laundries & Drycleaners': '812310',  # 35
    'Drycleaning & Laundry Services(except Coin-Operated)': '812320',  # 27
    'Pet Care (except Veteinerary) Services': '812910',  # 21
    'Diet & Weight Reducing Centers': '812191',  # 2
    # --- Not a storefront bucket (410 types, 11,551 licences) ----------
    'Special Events-Other (Vendor)': None,  # 1,264 - a vendor's permit for one event, not a premises (the brief)
    'Taxi Service': '485310',  # 674
    'Home Based-Office Use Only': None,  # 357 - an office in a home, not a storefront (the brief)
    'Offices of Lawyers': '541110',  # 349
    'Flea Market': None,  # 344 - a stall at a market, not a shop of its own (category_rules R1: a market building's stalls and stands are out); 344 licences, most at the French Market's 1200 N Peters St
    'Hotels(except Casino Hotels) & Motels': '721110',  # 294
    'Limousine Service': '485320',  # 291
    'Artist-Painting on Streets': None,  # 281 - a street artist's permit, no premises (mobile units out)
    'Video Draw Poker Devices': None,  # 261 - gambling devices (R5)
    'Personal Services, Other': '812990',  # 249
    'Parking Lots & Garages': '812930',  # 203
    'Administrative Management & General Management Consulting Services': '541611',  # 199
    'Social Advocacy Organizations, Other': '813319',  # 196
    'Special Trade Contractors, All Other': None,  # 194 - construction (NAICS 23)
    'Offices of Physicians(except Mental Health Specialists)': '621111',  # 143
    'Offices of Mental Health Practitioners(except Physicians), Other': None,  # 132 - health and social care (NAICS 62)
    'Electrical Contractors': None,  # 130 - construction (NAICS 23)
    'Caterers': '722320',  # 116
    'Bed & Breakfast Inns': '721191',  # 111
    'Management Consulting Services, Other': '541618',  # 108
    'Child Day Care Services': '624410',  # 107
    'Lessors of Residential Bulidings & Dwellings': '531110',  # 104
    'Tour Operators': '561520',  # 102
    'Real Estate Agents and Brokers': None,  # 91 - finance and real estate (NAICS 52-53)
    'Plumbing, Heating and Air-Conditioning Contractors': '238220',  # 90
    'Janitorial Services': '561720',  # 89
    'Fitness & Recreational Sports Centers': '713940',  # 88
    'Food Service Contractors': '722310',  # 88
    'Special Events-Jazz Fest (Vendor)': None,  # 88 - a vendor's permit for one festival, not a premises
    'Architectural Services': '541310',  # 85
    'Offices of Dentists': '621210',  # 83
    'Real Estate, Other Activities Related to': '531390',  # 82
    'Transit & Ground Passenger Transportation, All Other': '485999',  # 80
    'Landscaping Services': '561730',  # 79
    'Offices of Health Practitioners, All Other Miscellaneous': None,  # 79 - health and social care (NAICS 62)
    'Electronic Shopping & Mail-Order Houses': '454110',  # 76
    'Interior Design Services': '541410',  # 76
    'Engineering Services': '541330',  # 75
    'Mobile Food Services': '722330',  # 68
    'Commercial and Institutional Building Construction': '236220',  # 67
    'Educational Support Services': '611710',  # 65
    'Civic & Social Organizations': '813410',  # 64
    'Single Family Housing Construction': None,  # 62 - construction (NAICS 23)
    'Automotive Repair & Maintenance, All Other': '811198',  # 61
    'Special Needs Transportation': '485991',  # 58
    'Tax Preparation Services': '541213',  # 58
    'Independent Artists, Writers & Performers': '711510',  # 57
    'Marketing Consulting Services': '541613',  # 56
    'Security Guards & Patrol Services': '561612',  # 56
    'Accounting Services, Other': '541219',  # 53
    'Offices of Physical, Occupational & Speech Therapists & Audiologists': '621340',  # 48
    'Schools & Instruction, All Other Miscellaneous': '611699',  # 48
    'Offices of Physicians, Mental Health Specialists': '621112',  # 46
    'Reception hall rental or leasing': None,  # 45 - venue rental (NAICS 53)
    'Legal Services, All Other': '541199',  # 43
    'Cellular & Other Wireless Telecommunications': None,  # 42 - information (NAICS 51)
    'Office Administration Services': None,  # 42 - professional and business services (NAICS 54-56)
    'Scientific & Technical Consulting Services, Other': '541690',  # 42
    'Motor Vehicle Towing': '488410',  # 41
    'Individual & Family Services, Other': '624190',  # 40
    'Motion Picture & Video Production': '512110',  # 40
    'Carpentry Contractors': None,  # 39 - construction (NAICS 23)
    'Lessors of Nonresidential Bulidings(except Miniwarehouses)': '531120',  # 39
    'Photography Studios, Portrait': '541921',  # 38
    'Car Washes': '811192',  # 36
    'Lessors of Other Real Estate Property': '531190',  # 33
    'Residential Property Managers': '531311',  # 33
    'Home Health Care Services': '621610',  # 32
    'General Automotive Repair': '811111',  # 31
    'Graphic Design Services': '541430',  # 31
    'General Freight Trucking': '4841',  # 30
    'General Warehousing & Storage': '493110',  # 30
    'Special Events-Essence Fest (Vendor)': None,  # 30 - a vendor's permit for one festival, not a premises
    'Automotive Mechanical & Electrical Repair & Maintenance, Other': '811118',  # 29
    'Elementary & Secondary Schools': '611110',  # 29
    'Museums': '712110',  # 29
    'Promoters of Performing Arts, Sports & Similar Events': '7113',  # 29
    'Employment Placement Agencies': '561311',  # 28
    'Veterinary Services': '541940',  # 28
    'Child & Youth Services': '624110',  # 27
    'Professional, Scientific & Technical Services, All Other': '541990',  # 27
    'Specialized Design Services, Other': '541490',  # 27
    'Durable Goods Wholesalers, Other Miscellaneous': None,  # 26 - wholesale (NAICS 42)
    'Commercial Photography': '541922',  # 25
    'Insurance Agencies & Brokerages': '524210',  # 25
    'Offices of Certified Public Accountants': '541211',  # 25
    'Offices of Chiropractors': '621310',  # 25
    'Outpatient Mental Health & Substance Abuse Centers': '621420',  # 25
    'Religious Organizations': '813110',  # 25
    'Amusement & Recreation Industries, All Other': '713990',  # 24
    'Automotive Body, Paint & Interior Repair & Maintenance': '811121',  # 24
    'Outpatient Care Centers, All Other': '621498',  # 24
    'All Other Miscellaneous Manufacturing': '339999',  # 22
    'Computer Systems Design Services': '541512',  # 22
    'Custom Computer Programming Services': '541511',  # 22
    'Environmental Consulting Services': '541620',  # 22
    'General Medical & Surgical Hospitals': '622110',  # 22
    'Musical Groups & Artists': '711130',  # 21
    'Roofing, Siding and Sheet Metal Contractors': None,  # 21 - construction (NAICS 23)
    'Travel Arrangement & Reservation Services, All Other': '561599',  # 21
    'Charter Bus Industry': '485510',  # 20
    'Investment Advice': '523930',  # 20
    'Passenger Car Rental': '532111',  # 20
    'Personal & Household Goods Repair & Maintenance, Other': '811490',  # 20
    'Sports & Recreation Instruction': '611620',  # 20
    'Consumer Lending': '522291',  # 19
    'Nonresidential Property Managers': '531312',  # 19
    'Services for Elderly & Disabled Persons': None,  # 19 - health and social care (NAICS 62)
    'Funeral Homes & Funeral Services': '812210',  # 18
    'Nondurable Goods Wholesalers, Other Miscellaneous': None,  # 18 - wholesale (NAICS 42)
    'Investigation Services': '561611',  # 17
    'Offices of Optometrists': '621320',  # 17
    'Travel Agencies': '561510',  # 17
    'Vending Machine Operators': '454210',  # 17
    'Community Housing Services, Other': '624229',  # 16
    'Electric Bulk Power Transmission and Control': '221121',  # 16
    'Medical Laboratories': '621511',  # 16
    'Professional & Management Development Training': '611430',  # 16
    'Wine & Distilled Alcoholic Beverage Wholesalers': None,  # 16 - wholesale (NAICS 42)
    'Business Service Centers(including Copy Shops), Other': '561439',  # 15
    'Commercial & Industrial Machinery & Equipment Rental & Leasing, Other': '532490',  # 15
    'Dance Companies': '711120',  # 15
    'Insurance Related Activities, All Other': '524298',  # 15
    'Painting and Wall Covering Contractors': '238320',  # 15
    'Residential Care Facilities, Other': '623990',  # 15
    'Technical & Trade Schools, Other': '611519',  # 14
    'Commercial Printing': '323111',  # 13
    'Commission Agents and Brokers': None,  # 13 - finance and real estate (NAICS 52-53)
    'Concrete Contractors': None,  # 13 - construction (NAICS 23)
    'Direct Selling Establishments, Other': '454390',  # 13
    'Fine Arts Schools': '611610',  # 13
    'Human Resources & Executive Search Consulting Services': None,  # 13 - professional and business services (NAICS 54-56)
    'Kidney Dialysis Centers': '621492',  # 13
    'Process, Physical Distribution & Logistics Consulting Services': '541614',  # 13
    'Services to Buildings & Dwellings, Other': '561790',  # 13
    'Support Services, All Other': '561990',  # 13
    'Tiltle Abstract & Settlement Offices': '541191',  # 13
    'Advertising Agencies': '541810',  # 12
    'Book Publishers': '511130',  # 12
    'Exterminating & Pest Control Services': '561710',  # 12
    'Heavy Construction, All Other': None,  # 12 - construction (NAICS 23)
    'Public Relations Agencies': '541820',  # 12
    'Recreational Goods Rental': '532284',  # 12
    'Rooming & Boarding Houses': '721310',  # 12
    'Testing Laboratories': '541380',  # 12
    'Theater Companies & Dinner Theaters': '711110',  # 12
    'Truck, Utility Trailer & RV (Recreational Vehicle) Rental & Leasing': '532120',  # 12
    'Waste Management, All Other Miscellaneous': None,  # 12 - not a storefront trade
    'Automobile and Other Motor Vehicle Wholesalers': None,  # 11 - wholesale (NAICS 42)
    'Drywall, Plastering, Acoustical and Insulation Contractors': None,  # 11 - construction (NAICS 23)
    'Grocery and Related Products Wholesalers, Other': None,  # 11 - wholesale (NAICS 42)
    'Landscape Architectural Services': '541320',  # 11
    'Passenger Car Leasing': '532112',  # 11
    'Security Systems Services(except Locksmiths)': '561621',  # 11
    'Consumer Goods Rental, All Other': '532289',  # 10
    'General Rental Centers': '532310',  # 10
    'Industrial Supplies Wholesalers': None,  # 10 - wholesale (NAICS 42)
    'Lessors of Miniwarehouses & Self Storage Units': '531130',  # 10
    'Medical, Dental & Hospital Equipment & Supplies Wholesalers': None,  # 10 - wholesale (NAICS 42)
    'Reupholstery & Furniture Repair': '811420',  # 10
    'Similar Organizations (exc Business, Professional, Labor & Political)': None,  # 10 - not a storefront trade
    'Agents & Mgrs for Artists, Athletes, Entertainers & Other Public Figures': None,  # 9 - professional and business services (NAICS 54-56)
    'Automobile Driving Schools': '611692',  # 9
    'Coffee and Tea Manufacturing': '311920',  # 9
    'Construction Material Wholesalers, Other': None,  # 9 - wholesale (NAICS 42)
    'Fish & Seafood Wholesalers': None,  # 9 - wholesale (NAICS 42)
    'Floor Laying and Other Floor Contractors': None,  # 9 - construction (NAICS 23)
    'Lumber, Plywood, Millwork & Wood Panel Wholesalers': None,  # 9 - wholesale (NAICS 42)
    'Mardi Gras - Fixed Locations': None,  # 9 - a Carnival-season stand, not a premises
    'Marinas': '713930',  # 9
    'Offices of Real Estate Appraisers': '531320',  # 9
    'Pay Day Loans': None,  # 9 - lending (NAICS 52)
    'Publishers, All Other': '511199',  # 9
    'Racetracks': '711212',  # 9
    'Residential Mental Health & Substance Abuse Facilities': '623220',  # 9
    'Scenic & Sightseeing Transportation, Land': '487110',  # 9
    'Scenic & Sightseeing Transportation, Other': '487990',  # 9
    'Ambulatory Health Care Services,All Other Miscellaneous': '621999',  # 8
    'Automotive Oil Change & Lubrication Shops': '811191',  # 8
    'Brick, Stone and Related Construction Materials Wholesalers': None,  # 8 - wholesale (NAICS 42)
    'Building Equipment and Other Machinery Installation Contractors': None,  # 8 - construction (NAICS 23)
    'Carpet & Upholstery Cleaning Services': '561740',  # 8
    'Cemeteries & Crematories': '812220',  # 8
    'Commercial Screen Printing': '323113',  # 8
    'Computer & Office Machine Repair & Maintenance': '811212',  # 8
    'Convention & Trade Show Organizers': '561920',  # 8
    'Couriers': None,  # 8 - transport (NAICS 48-49)
    'Financial Transactions Processing, Reserve & Clearinghouse Activities': '522320',  # 8
    'Freight Transportation Arrangement': '488510',  # 8
    'Investment Banking': None,  # 8 - finance and real estate (NAICS 52-53)
    'Multifamily Housing Construction': None,  # 8 - construction (NAICS 23)
    'RV( Recreational Vehicle) Parks & Campgrounds': '721211',  # 8
    'Real Estate Investment Trusts': None,  # 8 - finance and real estate (NAICS 52-53)
    'Research & Development in Physical, Engineering & Life Sciences': None,  # 8 - professional and business services (NAICS 54-56)
    'Securities Brokerage': '523120',  # 8
    'Voluntary Health Organizations': '813212',  # 8
    'Advertising, Other Services Related to': '541890',  # 7
    'Air Transportation Support Activitites, Other': None,  # 7 - transport (NAICS 48-49)
    'Building Inspection Services': '541350',  # 7
    'Computer Facilities Management Services': '541513',  # 7
    'Computer and Computer Peripheral Equipment and Software Wholesalers': None,  # 7 - wholesale (NAICS 42)
    'Digital Printing': None,  # 7 - manufacturing (NAICS 31-33)
    'Document Preparation Services': '561410',  # 7
    'Electronic Parts & Equipment Wholesalers, Other': None,  # 7 - wholesale (NAICS 42)
    'Glass and Glazing Contractors': '238150',  # 7
    'Home Furnishing Wholesalers': None,  # 7 - wholesale (NAICS 42)
    'Mortgage & Nonmortgage Loan Brokers': '522310',  # 7
    'Offices of Notaries': '541120',  # 7
    'Road Transportation Support Activities, Other': None,  # 7 - transport (NAICS 48-49)
    'Temporary Help Services': '561320',  # 7
    'Used Household & Office Goods Moving': '484210',  # 7
    'Waste Collection, Other': '562119',  # 7
    'Water Transportation Support Activities, Other': None,  # 7 - transport (NAICS 48-49)
    'Appliance Repair & Maintenance': '811412',  # 6
    'Community Food Services': '624210',  # 6
    'Electrical Apparatus and Eqpt,Wiring  Supp & Construction Mtrl Wholesalers': None,  # 6 - wholesale (NAICS 42)
    'Equipment & Supplies Wholesalers, Other Professional': None,  # 6 - wholesale (NAICS 42)
    'Exam Preparation & Tutoring': '611691',  # 6
    'Grantmaking & Giving Services, Other': '813219',  # 6
    'Music Publishers': '512230',  # 6
    'Office Machinery & Equipment Rental & Leasing': '532420',  # 6
    'Paint, Varnish and Supplies Wholesalers': None,  # 6 - wholesale (NAICS 42)
    'Performing Arts Companies, Other': '711190',  # 6
    'Professional Organizations': '813920',  # 6
    'Recyclable Material Wholesalers': None,  # 6 - wholesale (NAICS 42)
    'Research & Development in Social Sciences & Humanities': None,  # 6 - professional and business services (NAICS 54-56)
    'Scenic & Sightseeing Transportation, Water': '487210',  # 6
    'Specialized Freight(except Used) Trucking': '4842',  # 6
    'Transportation Equipment & Supplies(except Motor Vehicles) Wholesalers': None,  # 6 - wholesale (NAICS 42)
    'Video Tape & Disk Rental': '532282',  # 6
    'Wrecking and Demolition Contractors': None,  # 6 - construction (NAICS 23)
    '': None,  # 5 - no type given
    'Breweries': '312120',  # 5
    'Coin - Operated Amusement Devices, All Other': None,  # 5 - amusement devices (recreation, NAICS 71)
    'Continuing Care Retirement Communities': '623311',  # 5
    'Credit Intermediation, Other Activities Related to': '522390',  # 5
    'Data Processing Services': None,  # 5 - manufacturing (NAICS 31-33)
    'Electronic & Precision Equipment Repair & Maintenance, Other': '811219',  # 5
    'Freestanding Ambulatory Surgical & Emergency Centers': '621493',  # 5
    'Jewelry, Watch, Precious Stone & Precious Metal Wholesalers': None,  # 5 - wholesale (NAICS 42)
    'Land Subdivision and Land Development': None,  # 5 - construction (NAICS 23)
    'Locksmiths': '561622',  # 5
    'Masonry and Stone Contractors': None,  # 5 - construction (NAICS 23)
    'Nursing Care Facilities': '623110',  # 5
    'Offices of Podiatrists': '621391',  # 5
    'Power and Communication Transmission Line Construction': None,  # 5 - construction (NAICS 23)
    'Private Mail Centers': '561431',  # 5
    'Short Term Rentals/Residential Properties': None,  # 5 - lodging
    'Sound Recording Studios': '512240',  # 5
    'Specialty (except Pyschiatric & Substance Abuse) Hospitals': '622310',  # 5
    'Sports Teams & Clubs': '711211',  # 5
    "Women's, Children's & Infants' Clothing & Accessories Wholesalers": None,  # 5 - wholesale (NAICS 42)
    'Advertising Material Distribution Services': '541870',  # 4
    'Automotive Glass Replacement Shops': '811122',  # 4
    'Business Associations': '813910',  # 4
    'Commercial Equipment Wholesalers, Other': None,  # 4 - wholesale (NAICS 42)
    'Construction, Mining & Forestry Machinery & Equipment Rental & Leasing': '532412',  # 4
    'Convention & Visitors Bureaus': '561591',  # 4
    'Custom Architectural Woodwork and Millwork Manufacturing': '337212',  # 4
    'Display Advertising': None,  # 4 - professional and business services (NAICS 54-56)
    'Emergency & Other Relief Services': '624230',  # 4
    'Facilities Support Services': '561210',  # 4
    'Farm Supplies Wholesalers': None,  # 4 - wholesale (NAICS 42)
    'Footwear & Leather Goods Repair': '811430',  # 4
    'Fresh Fruit & Vegetable Wholesalers': None,  # 4 - wholesale (NAICS 42)
    'Golf Courses & Country Clubs': '713910',  # 4
    'Grantmaking Foundations': '813211',  # 4
    'Lessors of Nonfinancial Intangible Assets(except Copyrights)': '533110',  # 4
    'Mardi Gras - Walkers': None,  # 4 - a Carnival-season walking vendor
    'Marine Cargo Handling': '488320',  # 4
    'Navigational Services to Shipping': '488330',  # 4
    'Plumbing & Heating Equipment Supplies(Hydronics) Wholesalers': None,  # 4 - wholesale (NAICS 42)
    'Record Production': None,  # 4 - manufacturing (NAICS 31-33)
    'Tile, Marble, Terrazz and Mosaic Contractors': None,  # 4 - construction (NAICS 23)
    'Bread Manufacturing': '311812',  # 3
    'Confectionery Wholesalers': None,  # 3 - wholesale (NAICS 42)
    'Consumer Electronics & Appliances Rental': '532210',  # 3
    'Dental Laboratories': '339116',  # 3
    'Drafting Services': '541340',  # 3
    'Environment & Wildlife Organizations': None,  # 3 - not a storefront trade
    'Farm Product Warehousing & Storage': '493130',  # 3
    'Flight Training': '611512',  # 3
    'Frozen Cakes, Pies and Other Pastries Manufacturing': '311813',  # 3
    'Highway and Street Construction': None,  # 3 - construction (NAICS 23)
    'Homes for the Elderly': None,  # 3 - health and social care (NAICS 62)
    'Integrated Record Production/ Distribution': None,  # 3 - wholesale (NAICS 42)
    'Jewelry(except costume) Manufacturing': None,  # 3 - manufacturing (NAICS 31-33)
    'Manufacturing and Industrial Building Construction': None,  # 3 - construction (NAICS 23)
    'Marketing Research & Public Opinion Polling': '541910',  # 3
    'Motion Picture Theaters(except Drive-Ins)': '512131',  # 3
    'Motor Vehicle Supplies & New Parts Wholesalers': None,  # 3 - wholesale (NAICS 42)
    'Natural Gas Distribution': '221210',  # 3
    'Perishable Prepared Food Manufacturing': '311991',  # 3
    'Portfolio Management': '523920',  # 3
    'Residential Mental Retardation Facilities': None,  # 3 - health and social care (NAICS 62)
    'Stationery & Office Supplies Wholesalers': None,  # 3 - wholesale (NAICS 42)
    'Support Activities for Oil and Gas Operations': '213112',  # 3
    'Telecommunications Resellers': '517911',  # 3
    'Temporary Shelters': '624221',  # 3
    'Traveler Accommodation, All Other': '721199',  # 3
    'Video Games/ Pinball / Flipper Devices': None,  # 3 - amusement devices (recreation, NAICS 71)
    'Vocational Rehabilitation Services': '624310',  # 3
    'Ambulance Services': '621910',  # 2
    'Apparel Accessories and Apparel Manufacturing, Other': None,  # 2 - manufacturing (NAICS 31-33)
    'Automotive Transmission Repair': '811113',  # 2
    'Beer and Ale Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Cable Networks': None,  # 2 - information (NAICS 51)
    'Casino Hotels': '721120',  # 2
    'Casinos(except Hotel Casinos)': '713210',  # 2
    'Claims Adjusting': '524291',  # 2
    'Commercial & Industrial Machinery & Eqpt(except Auto & Electronic) R&M': '811310',  # 2
    'Commercial Air, Rail & Water Transportation Equipment Rental & Leasing': '532411',  # 2
    'Computer Training': '611420',  # 2
    'Consumer Electronics Repair & Maintenance': '811211',  # 2
    'Cosmetology & Barber Schools': '611511',  # 2
    'Court Reporting & Stenotype Services': '561492',  # 2
    'Dairy Product(except Dried or Canned)Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Diagnostic Imaging  Centers': '621512',  # 2
    "Drugs and Druggists' Sundries Wholesalers": None,  # 2 - wholesale (NAICS 42)
    'Gambling Industries, Other': '713290',  # 2
    'Historical Sites': '712120',  # 2
    'Ice Cream and Frozen Dessert Manufacturing': '311520',  # 2
    'Linen Supplies': None,  # 2 - not a storefront trade
    'Local Messengers & Local Delivery': '492210',  # 2
    'Meat and Meat Products Wholesalers': None,  # 2 - wholesale (NAICS 42)
    "Men's and Boys' Clothing & Furnishings Wholesalers": None,  # 2 - wholesale (NAICS 42)
    'Millwork(including Flooring), Other': '321918',  # 2
    'Nonscheduled Chartered Passenger Air Transportation': '481211',  # 2
    'Office Equipment Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Ornamental and Architectural Metal Wok Manufacturing': None,  # 2 - manufacturing (NAICS 31-33)
    'Packaged Frozen Food Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Packaging & Labeling Services': '561910',  # 2
    'Periodical Publishers': '511120',  # 2
    'Piece Goods, Notions & Other Dry Goods Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Plastics Materials & Basic Forms & Shapes Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Port & Harbor Operations': '488310',  # 2
    'Rail Transportation Support Activities': None,  # 2 - transport (NAICS 48-49)
    'Real Estate Credit': '522292',  # 2
    'Refrigerated Warehousing & Storage': '493120',  # 2
    'Remediation Services': '562910',  # 2
    'Sales Financing': '522220',  # 2
    'Scheduled Passenger Air Transportation': '481111',  # 2
    'Selling Stocks or Bonds as Principal': None,  # 2 - finance and real estate (NAICS 52-53)
    'Service Establishment Equipment & Supplies Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Sheet Metal Work Manufacturing': '332322',  # 2
    'Soap and Other Detergent Manufacturing': '325611',  # 2
    'Solid Waste Collection': '562111',  # 2
    'Structural Steel Erection Contractors': None,  # 2 - construction (NAICS 23)
    'Television Broadcasting': '515120',  # 2
    'Tobacco & Tobacco Product Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Trust, Fiduciary & Custody Activities': '523991',  # 2
    'Warm Air Heating & A/C Equipment & Supplies Wholesalers': None,  # 2 - wholesale (NAICS 42)
    'Wood Kitchen Cabinet and Countertop Manufacturing': '337110',  # 2
    'Amusement & Theme Parks': '713110',  # 1
    'Armored Car Services': '561613',  # 1
    'Asphalt Paving Mixture and Block Manufacturing': '324121',  # 1
    'Automotive  Exhaust System Repair': '811112',  # 1
    'Blood & Organ Banks': '621991',  # 1
    'Books Printing': '323117',  # 1
    'Cement Manufacturing': '327310',  # 1
    'Chemical and Allied Products Wholesalers, Other': None,  # 1 - wholesale (NAICS 42)
    'Collection Agencies': '561440',  # 1
    'Colleges, Universities & Professional Schools': '611310',  # 1
    'Commercial Banking': '522110',  # 1
    'Commodity Contracts Dealing': '523130',  # 1
    'Construction and Mining(except Oil Well)Machinery & Eqpt Wholesalers': None,  # 1 - wholesale (NAICS 42)
    'Cookie and Cracker Manufacturing': '311821',  # 1
    'Costume Jewelry and Novelty Manufacturing': None,  # 1 - manufacturing (NAICS 31-33)
    'Database & Directory Publishers': None,  # 1 - information (NAICS 51)
    'Deep Sea Passenger & Freight Transportation': None,  # 1 - transport (NAICS 48-49)
    'Drilling Oil and Gas Wells': '213111',  # 1
    'Employee Leasing Services': None,  # 1 - professional and business services (NAICS 54-56)
    'Excavation Contractors': None,  # 1 - construction (NAICS 23)
    'Family Planning Centers': '621410',  # 1
    "Flower, Nursery Stock & Florists' Supplies Wholesalers": None,  # 1 - wholesale (NAICS 42)
    'Formal Wear & Costume Rental': '532281',  # 1
    'Fresh and Frozen Seafood Processing': None,  # 1 - manufacturing (NAICS 31-33)
    'Fuel Dealers, Other': '454319',  # 1
    'Hazardous Waste Treatment & Disposal': '562211',  # 1
    'Household Furniture(except Wood & Metal) Manufacturing': '337125',  # 1
    'Industrial Machinery and Equipment Wholesalers': None,  # 1 - wholesale (NAICS 42)
    'Industrial and Personal Service Paper Wholesalers': None,  # 1 - wholesale (NAICS 42)
    'Manifold Business  Forms Printing': None,  # 1 - manufacturing (NAICS 31-33)
    'Media Buying Agencies': '541830',  # 1
    'Media Representatives': '541840',  # 1
    'Metal Service Centers & Offices': None,  # 1 - not a storefront trade
    'Nature Parks & Other Similar Institutions': '712190',  # 1
    'News Syndicates': '519110',  # 1
    'Newspaper Publishers': '511110',  # 1
    'Nonchocolate Confectionery Manufacturing': '311340',  # 1
    'On-Line Information Services': None,  # 1 - information (NAICS 51)
    'Open-End Investment Funds': '525910',  # 1
    'Paging': None,  # 1 - information (NAICS 51)
    'Payroll Services': '541214',  # 1
    'Petroleum & Petroleum Product Wholesalers(exc Bulk Station & Terminal)': None,  # 1 - wholesale (NAICS 42)
    'Photographic Equipment & Supplies Wholesalers': None,  # 1 - wholesale (NAICS 42)
    'Pipeline Transportation of Crude Oil': '486110',  # 1
    'Prefabricated Metal Building and Component Manufacturing': '332311',  # 1
    'Printing & Writing Paper Wholesalers': None,  # 1 - wholesale (NAICS 42)
    'Psychiatric & Substance Abuse Hospitals': '622210',  # 1
    'Radio Networks': '515111',  # 1
    'Refrigeration Equipment & Supplies Wholesalers': None,  # 1 - wholesale (NAICS 42)
    'Satellite Telecommunications': '517410',  # 1
    'Seafood Canning': None,  # 1 - manufacturing (NAICS 31-33)
    'Spectator Sports, Other': '711219',  # 1
    'Spice and Extract Manufacturing': '311942',  # 1
    'Surveying & Mapping(except Geophysical) Services': '541370',  # 1
    'Translation & Interpretation Services': '541930',  # 1
    'Wineries': '312130',  # 1
    'Wired Telecommunications Carriers': '517311',  # 1
}

# Retail by R5 (pawnbrokers kept), though the code is a lender's.
RETAIL_BY_RULE = frozenset({"Pawnshops"})


def bucket_of(value):
    v = value.strip() if isinstance(value, str) else ""
    if v not in TYPE_TO_NAICS:
        raise KeyError(f"New Orleans businesstype {v!r} has no home in nola_businesstype.py - "
                       f"map it (a NAICS code or None with a reason) before step 2 runs")
    if v in RETAIL_BY_RULE:
        return "Retail"
    code = TYPE_TO_NAICS[v]
    return naics_group(code) if code else None


def classify(row: dict):
    """Taxonomy-module interface: `row` carries `businesstype`."""
    return bucket_of(row.get(VALUE_COLUMN))


def legend_label(bucket: str) -> str:
    return bucket


# The findings that were expensive, asserted where the mapping is edited.
assert bucket_of("Personal Services, Other") is None, "the R2 catch-all must stay out"
assert bucket_of("Personal Care Services, Other") == "Personal services"
assert bucket_of("Pet Care (except Veteinerary) Services") == "Personal services"
assert bucket_of("Hotels(except Casino Hotels) & Motels") is None, "lodging is out"
assert bucket_of("Full Service Restaurants(table service available)") == "Food service"
assert bucket_of("Drinking Places(Alcoholic Beverages)") == "Food service"
assert bucket_of("Caterers") is None and bucket_of("Mobile Food Services") is None
assert bucket_of("Pawnshops") == "Retail"
assert bucket_of("Flea Market") is None
assert bucket_of("Special Events-Other (Vendor)") is None
assert bucket_of("Home Based-Office Use Only") is None
