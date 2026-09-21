"""Washington D.C.'s `BUSINESSACTIVITY` field, from the Basic Business
License register.

THE FIRST NON-NAICS SOURCE IN THIS PROJECT THAT COVERS ALL THREE BUCKETS ON ITS
OWN. New York needed four registries, Boston three, and Philadelphia and Boston
both ended up with a category missing entirely. D.C. licenses food, retail
trade and personal services in one register, so there is no multi-source
assembly here and no `source` column to dispatch on.

Every one of the 95 `BUSINESSACTIVITY` values present on the active,
in-District, non-rental rows is given a verdict below - mapped or explicitly
excluded, with the reason. Nothing falls through to a default: classify()
raises on a value it has never seen, because a new licence category appearing
upstream is a thing to look at, not to silently drop.

WHERE THE BUCKET BOUNDARIES SIT, AND WHY
----------------------------------------
The mapping is kept consistent with the NAICS cities rather than invented, so
the same kind of business lands in the same bucket whichever city a reader is
looking at. `pipeline/taxonomies/naics.py` counts prefixes 44/45 as Retail
(minus 454 nonstore), 722 as Food service and 812 as Personal services (minus
81293 parking), so:

  - car dealers and tyre shops ARE Retail (NAICS 441), because they are in
    every NAICS city here;
  - auto repair and car washes are NOT (NAICS 811 is repair, not 812), which
    is also why Miami's `SERVICE BUSINESS` was excluded;
  - gyms, pools, cinemas and bowling alleys are NOT anything (NAICS 71), the
    same call Boston made on its Billiards and Bowling Alley licences;
  - hotels and rooming houses are NOT anything (NAICS 721), as in Boston;
  - parking is NOT anything, project-wide, via naics.py's 81293 carve-out;
  - vending machines and street vendors are NOT anything - NAICS itself calls
    these "nonstore", and the 454 carve-out exists for exactly them.

TWO THINGS A READER SHOULD KNOW ABOUT THIS CITY'S CATEGORIES
------------------------------------------------------------
**`Delicatessen` is ambiguous in the source, not in this mapping.** D.C. issues
it to sandwich shops, cafés, bakeries-with-seating AND corner shops: a sampled
25 held Julia's Empanadas and Call Your Mother Deli next to a 7-Eleven, a
Safeway and a convenience store. It is mapped to Food service, which is right
for the plurality, and 184 premises (3.5% of the map) hold it alongside only
retail endorsements, so they could honestly read either way. That is a property
of D.C.'s licence categories and is stated on the city page rather than hidden.

**Three licence types are ENDORSEMENTS, not descriptions.** `Cigarette Sales
(Retail)`, `Patent Medicine` (D.C.'s term for over-the-counter drug sales) and
`Food Products` are held by shops of every kind - the sampled Patent Medicine
rows included CVS, Whole Foods and Safeway, and a sampled Food Products row was
a hardware shop. They are mapped to Retail because holding one means selling
goods over a counter, but they are why premises-level dedup matters here: 812
licensees hold more than one kept licence type, and 121 of them hold exactly
Cigarette Sales + Food Products + Patent Medicine, which is one corner shop and
not three businesses.
"""

# --- Food service --------------------------------------------------------
FOOD_SERVICE = {
    # 2,227 rows. Unambiguous.
    "Restaurant",
    # 1,065 rows. See the docstring - D.C.'s prepared-food catch-all, covering
    # both cafés and corner shops.
    "Delicatessen",
    # 65 rows. NAICS 722320/311811 depending on seating; retail bakeries are
    # 722515 in every NAICS city here.
    "Bakery",
}

# --- Retail ---------------------------------------------------------------
RETAIL = {
    "Cigarette Sales (Retail)",      # 848 - tobacco/vape shops and corner shops
    "Food Products",                 # 656 - packaged-food endorsement
    "Patent Medicine",               # 610 - over-the-counter drugs; pharmacies
    "Grocery Store",                 # 239
    "Gasoline Dealer",               # 102 - NAICS 447, inside the "44" prefix
    "Motor Vehicle Dealer",          # 64  - NAICS 441, as in the NAICS cities
    "Secondhand Dealer (Class A)",   # 16  - antique/used-goods shops
    "New and Used Tire Dealer",      # 14  - NAICS 4413
    "Mattress Sales",                # 5
    "Pet Shop",                      # 5
    "Used Car Lot",                  # 5
    "Marine Food Product (Retail)",  # 5   - fishmongers; retail food
    "Fireworks Sales (Retail)",      # 2
    "Secondhand Dealer (Class B)",   # 1
}

# --- Personal services ---------------------------------------------------
# 575 rows, the thinnest of the three buckets here but genuinely present -
# which is what makes D.C. different from Philadelphia and Boston, where the
# category has no source at all.
PERSONAL_SERVICES = {
    "Beauty Shop",                   # 240
    "Beauty Shop (Nails)",           # 99
    "Barber Shop",                   # 89
    "Beauty Shop (Esthetics)",       # 39
    "Massage Establishment",         # 31 - NAICS 812199
    "Funeral Establishment",         # 29 - NAICS 812210
    "Dry Cleaner",                   # 21 - NAICS 812320
    "Power Laundry",                 # 10 - NAICS 812320/812331
    "Beauty Shop (Braiding)",        # 9
    "Beauty Booth",                  # 6  - a chair rented inside a salon
    "Beauty Shop (Electrology)",     # 2
}

# --- Excluded, with the reason -------------------------------------------
# Every remaining value, so that nothing is excluded by omission. The counts
# are the active, in-District rows as measured 2026-09-21.
EXCLUDED = {
    # THE CATCH-ALL. 11,074 rows, 46% of the download and the single biggest
    # exclusion in the project. Sampled twice: it is the office and
    # professional-services default - law firms (Lewis Brisbois, Nossaman),
    # engineers, architects, developers (Skanska, Hoffman & Associates),
    # healthcare and home-care agencies, consultancies, a locksmith, a police
    # relief association. Same role as Los Angeles' NAICS 812990 and Chicago's
    # "Limited Business License".
    #
    # It does contain some real storefronts - the sample held a Wawa and a Cava
    # - so the exclusion was checked rather than assumed: 692 of its rows (6%)
    # share a licensee with a kept storefront licence and 2,975 (27%) share a
    # MAR_ID, so a shop that landed here keeps its pin through its real
    # activity licence. What the exclusion removes is offices.
    "General Business": "office/professional catch-all - see the note above",

    # Charity and membership bodies - not commercial premises.
    "Charitable Solicitation": "fundraising permit, not a storefront (1,683)",
    "Charitable Exempt": "charity exemption, not a storefront (440)",
    "Cooperative Association": "member association, not a storefront (176)",
    "Solicitor": "door-to-door solicitation permit (1)",

    # Construction and trades - NAICS 23, in no bucket in any city here.
    "General Contractor/Construction Manager (A, B, C,":
        "construction, NAICS 23 (991)",
    "Home Improvement Salesperson": "construction sales, and an INDIVIDUAL "
                                    "licence rather than a premises (320)",
    "Home Improvement Contractor": "construction, NAICS 23 (152)",
    "Asbestos Abatement Business": "construction/remediation (15)",

    # Vehicular - NAICS 811 (repair), 532 (rental) and 81293 (parking). Parking
    # is excluded project-wide by naics.py's 81293 carve-out: a parking trip is
    # planned, not incidental station footfall.
    "Motor Vehicle Salesperson": "individual licence, not a premises (263)",
    "Parking Facility": "parking, excluded project-wide (263)",
    "Consumer Goods (Auto Repair)": "auto repair, NAICS 811 not 812 (78)",
    "Tow Truck": "towing, NAICS 4885 (69)",
    "Tow Truck Storage Lot": "towing yard (62)",
    "Tow Truck Business": "towing (60)",
    "Parking Facility Attendant": "parking, and an individual licence (40)",
    "Valet Parking": "parking (19)",
    "Auto Rental": "vehicle rental, NAICS 532 (17)",
    "Auto Wash": "car wash, NAICS 8111 (17)",
    "Driving School": "instruction, NAICS 6116 (4)",
    "Automobile Repossessor - Business": "repossession service (2)",
    "Used Car Buyer Seller": "dealing without a lot - no premises implied (2)",

    # Recreation and entertainment - NAICS 71. `Health Spa` is D.C.'s licence
    # for gyms: the sample was VIDA Fitness, Equinox, Gold's Gym, Solidcore,
    # CrossFit and New York Sports Club, so it is NAICS 713940, not 812.
    "Swimming Pool": "recreation, NAICS 713940 (165)",
    "Swimming Pool (DC)": "recreation, and municipally operated (32)",
    "Health Spa": "gyms - NAICS 713940, not a personal-care service (22)",
    "Health Spa Sales": "selling gym memberships (22)",
    "Public Hall": "assembly venue, NAICS 71 (18)",
    "Mechanical Amusement Machine": "machines sited inside other premises (14)",
    "Theater (Live)": "NAICS 7111 (11)",
    "Movie Theater": "NAICS 512131 (5)",
    "Billiard Parlor": "NAICS 713990, as Boston's Billiards licence (4)",
    "Skating Rink": "NAICS 713940 (2)",
    "Bowling Alley": "NAICS 713950, as Boston's (1)",
    "Athletic Exhibition": "event permit (1)",

    # Lodging - NAICS 721. Excluded as in Boston, where the Licensing Board's
    # Inn and Clb licences were dropped for the same reason.
    "Hotel": "lodging, NAICS 721 (141)",
    "Bed and Breakfast": "lodging (88)",
    "Inn and Motel": "lodging (46)",
    "Rooming House": "residential lodging (46)",
    "Boarding House": "residential lodging (19)",
    "Short Term Vacation Rental Exemption": "residential rental (13)",

    # Food-adjacent but NOT a storefront: production, institutional catering,
    # mobile and unattended trade.
    #
    # `School Cafeteria (DC)` is 242 rows and every sampled one is a school -
    # Janney, Marie Reed Elementary, a dozen charter schools. A cafeteria
    # behind a school's doors is not premises a passer-by can walk into, and
    # including it would put a food-service pin on every school in the
    # District. Only 3% of its rows share an address with a kept storefront,
    # so these are 242 distinct school sites rather than shops seen twice.
    #
    # `Caterers` is the closer call. 279 rows, and the sample mixed real
    # restaurants (Panera, Ruta Ukrainian) with commissary-kitchen tenants -
    # four separate licensees at 2800 10th St NE alone. Measured: 54 (19%)
    # share a licensee with a kept storefront licence and stay on the map
    # through it; 65% share an address. The rest are production kitchens with
    # no counter, so they go the way mobile food goes in every other city.
    "School Cafeteria (DC)": "institutional, inside a school (242)",
    "Street Vending Business": "mobile trade, as Boston's MFW (273)",
    "Caterers": "production kitchen, no walk-in counter - see above (279)",
    "Food Vending Machine": "unattended, NAICS 454 nonstore (60)",
    "School Cafeteria": "institutional, inside a school (5)",
    "Ice Cream Manufacturer": "manufacturing, NAICS 311520 (3)",
    "Mobile Delicatessen": "mobile trade (1)",
    "Candy Manufacturer": "manufacturing, NAICS 311352 (1)",
    "Farmer's Market Manager License": "market operator, not a shop (1)",

    # Wholesale - NAICS 42, in no bucket in any city here.
    "Cigarette Sales (Wholesale)": "wholesale, NAICS 42 (6)",
    "Marine Food Product (Wholesale)": "wholesale (2)",
    "Fireworks Sales (Wholesale)": "wholesale (1)",

    # Business and professional services - NAICS 56, 52, 484.
    "Employer-Paid Personnel Service": "staffing, NAICS 5613 (105)",
    "Solid Waste Vehicle": "waste collection, NAICS 562 (87)",
    "Employment Agency": "staffing, NAICS 5613 (30)",
    "Security Alarm Agent": "individual licence, NAICS 5616 (20)",
    "Moving and Storage": "NAICS 484/493 (14)",
    "Security Alarm Dealer": "NAICS 5616 (14)",
    "Solid Waste Collector": "waste collection (14)",
    "Auctioneer": "individual licence, no premises (15)",
    "Auction Sales": "auction house, not walk-in retail (6)",
    "Security Agency": "NAICS 5616 (5)",
    "Pawnbroker": "NAICS 522299 - lending, as in the NAICS cities (4)",
    "Detective Agency": "NAICS 5616 (3)",
    "Tour Guide": "individual licence, NAICS 5615 (3)",
    "Employment Counseling": "NAICS 5613 (2)",
    "Special Event": "one-off event permit (1)",
}

_BUCKETS = {}
_BUCKETS.update({a: "Food service" for a in FOOD_SERVICE})
_BUCKETS.update({a: "Retail" for a in RETAIL})
_BUCKETS.update({a: "Personal services" for a in PERSONAL_SERVICES})

_overlap = set(EXCLUDED) & set(_BUCKETS)
if _overlap:
    raise AssertionError(f"activity both mapped and excluded: {sorted(_overlap)}")

# Every value seen in the register on 2026-09-21, so classify() can tell "a
# category I decided to exclude" from "a category that did not exist when this
# was written". The second is worth a look; the first is not.
SEEN = frozenset(_BUCKETS) | frozenset(EXCLUDED)

FIELD_LABEL = "D.C. licence category"
VALUE_COLUMN = "business_category"

# When one licensee holds several kept licence types at one address, which
# bucket does the premises get? 812 of 5,215 licensees do, but only 368 of them
# cross a bucket boundary, and every one of those 368 crosses Food service <->
# Retail: no licensee anywhere in the register mixes Personal services with
# another bucket, so this list's third entry never decides anything.
#
# Food service first, consistent with Boston. Checked against the alternative
# rather than assumed: a more elaborate rule that ranks a licence naming what
# the premises IS ("Restaurant", "Grocery Store") above an endorsement it
# merely holds ("Cigarette Sales", "Patent Medicine") produces an IDENTICAL
# split - Retail 1,355, Food service 3,322, Personal services 538 - so the
# simple rule costs nothing. Retail-first would move 368 premises (7%).
BUCKET_PRIORITY = ["Food service", "Retail", "Personal services"]


def legend_label(bucket: str) -> str:
    """Taxonomy-module interface: legend text for a bucket."""
    return bucket


def classify(row: dict):
    """Taxonomy-module interface. `row` must carry `business_category` - the
    register's BUSINESSACTIVITY, renamed by step 2."""
    value = row.get(VALUE_COLUMN)
    if value is None or str(value).strip() in ("", "nan", "None"):
        return None
    activity = str(value).strip()
    if activity in _BUCKETS:
        return _BUCKETS[activity]
    if activity in EXCLUDED:
        return None
    raise KeyError(
        f"BUSINESSACTIVITY {activity!r} is not in this taxonomy. All 95 values "
        f"present on 2026-09-21 are given a verdict in "
        f"pipeline/taxonomies/dc_businessactivity.py, so this is a category "
        f"D.C. has added since. Sample it, decide, and add it to FOOD_SERVICE, "
        f"RETAIL, PERSONAL_SERVICES or EXCLUDED - do not let it fall through.")
