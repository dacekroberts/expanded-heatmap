"""New York taxonomy - a DISPATCHING taxonomy over four registries, because
New York has no general business licence.

Why this is shaped differently from every other city
----------------------------------------------------
Every city built so far had one registry that answered "what businesses are
here". New York does not. Its DCA/DCWP "Issued Licenses" file (Socrata
`w7w3-xahh`) was the candidate in `docs/city_shortlist.md`, and Step 0
verification (2026-09-21) showed it is a *regulated-activity* licence list,
not a registry: of 35,245 active premises licences, 13,385 are home
improvement contractors, and the file contains **zero** restaurants, zero
grocery stores, zero clothing shops, zero pharmacies and zero salons. Built on
DCA alone the map would have shown ~15k tobacco shops, secondhand dealers and
electronics stores with two of the three legend buckets empty - a false
picture of New York.

So the city's coverage is assembled from four public registries, each the
authoritative source for what it covers, and each mapped into the same shared
buckets:

  source       registry                                    bucket
  -----------  ------------------------------------------  -----------------
  dohmh        DOHMH restaurant inspections (43nn-pn8j)    Food service
  nys_store    NYS Retail Food Stores (9a8c-vfzj)          Retail
  nys_salon    NYS Appearance Enhancement / Barber         Personal services
               *business* licences (y3u4-jbgh)
  dca          DCWP Issued Licenses (w7w3-xahh)            Retail (narrow)

`VALUE_COLUMN` holds each source's own category string (so a tooltip shows
"Pizza", "Retail food store" or "Electronics Store" - the registry's own
words), and `EXTRA_COLUMNS` carries `source` so `classify()` knows which
mapping to apply. That is the whole reason this dispatches: the interface in
`pipeline/taxonomies/__init__.py` already supports a multi-column taxonomy
(Chicago uses it for `business_activity`), so nothing in `map_common.py` needed
to change.

Buckets follow what the NAICS taxonomy counts (44/45 retail, 722 food service,
812 personal services), the same standard `chicago_license.py` sets, so the
cities stay comparable. That standard - not a fresh judgment per category - is
what decided most of the DCA exclusions below.

A site can hold licences in more than one of these registries (a bodega with a
food counter is a DOHMH establishment *and* an NYS retail food store *and*
often a DCA tobacco dealer). Step 2 keeps one row per site by source priority;
see `SOURCE_PRIORITY` and `DCA_ADJUNCT_CATEGORIES` below.

Personal information: this module never reads a registrant's own name. The
salon registry's `license_holder_name` is an individual's name and is dropped
in step 2 before anything is written; only `business_name` (a registered trade
name, blank on 0% and identical to the holder's name on 2 of 6,000 sampled NYC
rows) is ever displayed. See `docs/excluded_categories.md`.
"""

# --------------------------------------------------------------------------
# Source registry keys. Step 2 writes one of these into every row's `source`.
# --------------------------------------------------------------------------
SOURCES = ("dohmh", "nys_store", "nys_salon", "dca")

# Which source wins when the same site appears in several (step 2's dedup).
# A food permit identifies a business most specifically, then a grocery
# licence, then a salon licence; DCA's regulated licences come last because
# they are usually a secondary permit held by a business one of the others
# already names (see DCA_ADJUNCT_CATEGORIES).
SOURCE_PRIORITY = ("dohmh", "nys_store", "nys_salon", "dca")

# --------------------------------------------------------------------------
# DOHMH restaurant inspections -> Food service
# --------------------------------------------------------------------------
# The registry covers food service establishments, so membership *is* the
# classification: every row is Food service regardless of `cuisine_description`
# (91 distinct values, all of them food). `cuisine_description` is kept only as
# the displayed category, and is blank on ~3,800 of 31,319 establishments -
# blank still means "a DOHMH food establishment", so it does not change the
# bucket. Three small values read as retail rather than food service
# (Fruits/Vegetables 8, Nuts/Confectionary 7, Bottled Beverages 107); they are
# left as Food service because the permit they hold is a food-service permit,
# and 122 of 31,319 rows would not move the map.
DOHMH_BUCKET = "Food service"

# --------------------------------------------------------------------------
# NYS Retail Food Stores -> Retail
# --------------------------------------------------------------------------
# Every NYC row in this registry is `operation_type = 'Store'` AND carries an
# `estab_type` beginning with "A", which the state's own code legend defines as
# "Store" (Article 28-A). So every row is a physical retail food store:
# bodegas, delis, supermarkets, greengrocers. Membership is the classification.
#
# The other letters are additional establishment types at the same site, from
# NYSDAM_RetailFoodStoresEstablishmentTypeCodes.pdf (linked from the dataset's
# `estab_type` column description). Decoded here so a tooltip can say something
# a reader understands instead of "ACHDK".
NYS_STORE_BUCKET = "Retail"
NYS_ESTAB_TYPE_CODES = {
    "A": "Store",
    "B": "Bakery",
    "C": "Food manufacturer",
    "D": "Food warehouse",
    "E": "Beverage plant",
    "G": "Processing plant",
    "H": "Wholesale manufacturer",
    "I": "Refrigerated warehouse",
    "J": "Multiple operations",
    "K": "Vehicle",
    "L": "Produce refrigerated warehouse",
    "M": "Salvage dealer",
    "W": "Farm winery (exempt)",
}


def nys_store_label(estab_type: str) -> str:
    """A human category string for an NYS establishment-type code such as
    "AC" -> "Retail food store (store, food manufacturer)". Unknown letters
    are dropped rather than guessed."""
    letters = [c for c in (estab_type or "").upper() if c in NYS_ESTAB_TYPE_CODES]
    extra = [NYS_ESTAB_TYPE_CODES[c].lower() for c in dict.fromkeys(letters)]
    if not extra:
        return "Retail food store"
    return f"Retail food store ({', '.join(extra)})"


# --------------------------------------------------------------------------
# NYS Appearance Enhancement / Barber -> Personal services
# --------------------------------------------------------------------------
# Hair, nail, skin care, waxing, barbering: NAICS 8121, squarely the Personal
# services bucket and the same activities chicago_license.py counts.
#
# Only the two BUSINESS licence types are kept. The two renter types are
# individuals working a chair or room inside someone else's shop - they are not
# a separate storefront, and counting them would both double-count the shop and
# put an individual on the map. Excluded in step 2 by this table.
NYS_SALON_BUCKET = "Personal services"
NYS_SALON_KEEP_LICENSE_TYPES = {
    "DOSAEBUSINESS": "Appearance enhancement business",
    "DOSBARSHOPOWNER": "Barber shop",
}
NYS_SALON_EXCLUDE_LICENSE_TYPES = {
    "DOSAERENTER": "Appearance enhancement area renter - an individual renting "
                   "space inside another licensee's shop, not its own storefront",
    "DOSBARRENTER": "Barber chair renter - as above",
}

# --------------------------------------------------------------------------
# DCWP Issued Licenses -> Retail (a narrow, regulated slice)
# --------------------------------------------------------------------------
# Two filters are applied in step 2 before this table is consulted:
#   license_status == 'Active'
#   license_type   == 'Premises'
# The second matters most. DCA's 17,179 `Individual` licences (8,854 active)
# are licences held BY A PERSON - sightseeing guides, locksmiths, general
# vendors, pedicab drivers, process servers, tow truck drivers. They are not
# storefronts by their own definition, and their address is frequently the
# licensee's home, so mapping them would publish individuals at their
# residences. Excluded wholesale, the same reasoning that excluded NAICS 454
# nonstore retailers nationally (see naics.py).
DCA_CATEGORY_TO_BUCKET = {
    "ELECTRONICS STORE": "Retail",
    "SECONDHAND DEALER - GENERAL": "Retail",
    "SECONDHAND DEALER - AUTO": "Retail",
    "DEALER IN PRODUCTS FOR THE DISABLED": "Retail",
    "NEWSSTAND": "Retail",
    # Adjunct licences - see DCA_ADJUNCT_CATEGORIES.
    "TOBACCO RETAIL DEALER": "Retail",
    "ELECTRONIC CIGARETTE DEALER": "Retail",
    "STOOP LINE STAND": "Retail",
}

# These three identify a *permission* a business holds, not the business. A
# tobacco or e-cigarette licence is typically held by a bodega or newsstand,
# and a stoop line stand is a licensed sidewalk display outside an existing
# shop. chicago_license.py treats its own TOBACCO licence exactly this way
# ("counts only where a site has no primary license"), and Chicago excludes
# adjunct licences (Outdoor Patio, Late Hour) outright. Here they are mapped to
# Retail but given last priority in step 2, so they add a pin only where no
# other registry already names that site - which is how a bodega ends up
# counted once, as a grocery, rather than three times.
DCA_ADJUNCT_CATEGORIES = frozenset({
    "TOBACCO RETAIL DEALER",
    "ELECTRONIC CIGARETTE DEALER",
    "STOOP LINE STAND",
})

# Every other active DCA premises category, with why it is not on the map.
# Kept as data, not prose, so docs/excluded_categories.md can be generated
# from it and nothing is quietly dropped. Counts are active premises rows at
# the 2026-09-21 pull.
DCA_EXCLUDED_CATEGORIES = {
    "HOME IMPROVEMENT CONTRACTOR": (
        13385, "Works at the customer's premises; there is no shop to walk "
               "into. Same reasoning as NAICS 454 nonstore retailers."),
    "GARAGE & PARKING LOT": (
        1761, "Parking. A planned trip, not incidental station foot traffic - "
              "excluded in every city (NAICS 81293)."),
    "DEBT COLLECTION AGENCY": (
        1354, "A back office with no walk-in trade (financial services)."),
    "ELECTRONIC & HOME APPLIANCE SERVICE DEALER": (
        1447, "A repair trade (NAICS 811), which none of the three buckets "
              "covers; Chicago excludes vehicle repair on the same basis."),
    "HOTEL": (
        420, "Accommodation (NAICS 721), outside the counted groups; Chicago "
             "excludes hotels."),
    "PAWNBROKER": (
        272, "Nondepository credit (NAICS 522298), not retail; Chicago "
             "excludes pawnbrokers explicitly."),
    "SELF-STORAGE FACILITY": (
        242, "A planned trip to stored goods, not station foot traffic."),
    "EMPLOYMENT AGENCY": (
        238, "Staffing services, outside the counted groups."),
    "TOW TRUCK COMPANY": (202, "Dispatched vehicle service, not a storefront."),
    "CAR WASH": (
        176, "A vehicle trip, on the same reasoning as parking; Chicago "
             "excludes car washes."),
    "PROCESS SERVING AGENCY": (110, "An office; administrative services."),
    "SCRAP METAL PROCESSOR": (79, "Industrial."),
    "HORSE DRAWN CAB OWNER": (68, "Transport, not premises trade."),
    "INDUSTRIAL LAUNDRY": (
        41, "Business-to-business laundry. A consumer laundromat would count "
            "as Personal services; an industrial plant is not a storefront."),
    "STORAGE WAREHOUSE": (35, "Industrial."),
    "THIRD PARTY FOOD DELIVERY SERVICE": (
        34, "Nonstore by definition - the NAICS 454 reasoning."),
    "INDUSTRIAL LAUNDRY DELIVERY": (29, "As industrial laundry, and delivery."),
    "SCALE DEALER/REPAIRER": (28, "Business-to-business equipment service."),
    "CONSTRUCTION LABOR PROVIDER": (26, "Labour supply, not a storefront."),
    "BINGO GAME OPERATOR": (
        24, "Amusements (NAICS 71), outside the counted groups; Chicago "
            "excludes amusements."),
    "GAMES OF CHANCE - RAFFLE WITH NET PROCEEDS UNDER $30,000": (11, "Amusements."),
    "GAMES OF CHANCE - RAFFLE WITH NET PROCEEDS OVER $30,000": (9, "Amusements."),
    "TICKET SELLER BUSINESS": (10, "Event ticketing (NAICS 71)."),
    "GAMES OF CHANCE - BELL JAR": (8, "Amusements."),
    "BOOTING COMPANY": (8, "Vehicle enforcement, not a storefront."),
    "SIGHTSEEING BUS": (7, "Transport."),
    "COMMERCIAL LESSOR - BINGO": (3, "Amusements."),
    "PEDICAB BUSINESS": (3, "Transport."),
    "GAMES OF CHANCE - LAS VEGAS / CASINO NIGHTS": (2, "Amusements."),
    "GENERAL VENDOR DISTRIBUTOR": (1, "Wholesale distribution, nonstore."),
}

# --------------------------------------------------------------------------
# Taxonomy-module interface (see pipeline/taxonomies/__init__.py)
# --------------------------------------------------------------------------
FIELD_LABEL = "Category"
VALUE_COLUMN = "business_category"
# filter_to_storefront() and map_common pass these to classify() as well.
EXTRA_COLUMNS = ("source",)


def legend_label(bucket: str) -> str:
    """The legend stays broad: four registries feed these buckets and no short
    label could name them all honestly. docs/excluded_categories.md carries
    the detail (decided 2026-09-21)."""
    return bucket


def classify(row: dict):
    """Dispatch on `source` to that registry's mapping.

    `row` carries `business_category` (the registry's own category string, as
    step 2 normalised it) and `source` (one of SOURCES). An unknown source is
    a step 2 bug, not a data condition, so it raises rather than silently
    dropping rows.
    """
    source = (row.get("source") or "").strip()
    if not source:
        return None
    if source == "dohmh":
        return DOHMH_BUCKET
    if source == "nys_store":
        return NYS_STORE_BUCKET
    if source == "nys_salon":
        return NYS_SALON_BUCKET
    if source == "dca":
        category = (row.get("business_category") or "").strip().upper()
        return DCA_CATEGORY_TO_BUCKET.get(category)
    raise ValueError(
        f"Unknown New York source {source!r}; expected one of {SOURCES}. "
        "Step 2 sets this column."
    )
