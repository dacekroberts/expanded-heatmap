"""Miami taxonomy - the `CATGRYNAME` field from Miami-Dade County's Local
Business Tax file, not NAICS.

Source: "Local Business Tax" (ArcGIS FeatureServer, Miami-Dade County ITD
Geospatial Infrastructure Support Group). The file HAS a `BUSNAICSCD` column
and it is **NULL on all 194,099 rows** - checked county-wide, not sampled - so
NAICS is unavailable here despite appearing in the schema. `CATGRYNAME` (150
active values) is the usable classification; `CLASSDESC` (35 values) is the
coarser Florida statutory grouping above it, and `OCCDESC` is free text.

VERIFIED 2026-09-21 against the full distinct-value pull - all 150 values
active at that date, county-wide, not a sample. Every value below carries an
explicit verdict, a bucket or None, so a later reader can tell "checked, not a
match" from "not yet checked". Unknown values classify as None and step 2
prints any it meets, so an upstream rename surfaces instead of silently
dropping rows.

Buckets mean the same thing as in the NAICS cities (see naics.py):
    Retail        = NAICS 44/45 minus 454 nonstore
    Food service  = NAICS 722
    Personal services = NAICS 812
Permanent fixed premises only; mobile and itinerant vending is excluded, as it
is in every other city.

FIVE FINDINGS FROM HAND-SAMPLING, none of which the category name gives you:

  "SERVICE BUSINESS" (28,010 county / 4,900 city) is this file's biggest
  category and is NOT storefront services. Sampled: paralegals, management
  consultancies, media and tech agencies, tour guides, dispatch services, plus
  some genuine trade repair. It also holds COTTAGE FOOD operators working from
  apartments - the same home-kitchen pattern San Diego's filter caught. Same
  role as Los Angeles' NAICS 812990 and D.C.'s "General Business", and excluded
  for the same reason. This is the largest single judgment call in this module:
  it certainly discards some real storefront repair shops, and the honest
  alternative - classifying 28,010 rows of free-text OCCDESC - is a project of
  its own. Recorded in docs/excluded_categories.md.

  "DANCING OR ENTERTAINMENT" is not venues, it is BARS AND RESTAURANTS holding
  an entertainment endorsement. Sampled: Gramps, Neme Gastro Bar, Biscayne Bay
  Brewing, Meson Ria de Vigo, "BAR WITH ENTERTAINMENT", Baires Grill. Food
  service - and note it overlaps EATING ESTABLISHMENT heavily, which the
  premises-level dedup in step 2 resolves.

  "LAUNDRY MACHINE" is a MACHINE licence, not a laundromat. Sampled holders
  include Paradise Apartments, Camelot Court Apartments ("LAUNDRY ROOM") and
  Parque Apartments ("10 WASHERS / 10 DRYERS") alongside real coin laundries.
  Counting it would put pins on apartment buildings, so it is excluded;
  CLEANER/LAUNDRY/ALTERATIONS covers the actual premises.

  "TANGIBLE PERSONAL PROP DLR" (12,623 / 1,956) reads like retail and is not.
  Sampled: "WHOLESALE DISTRIBUTOR", "EXPORT/IMPORT", "ONLINE SALES", many at
  apartment addresses. Wholesale and nonstore, so NAICS 454 territory.

  "UNCLASSIFIED BUSINESS" is infrastructure, not shops: Crown Castle and
  Pinnacle Towers cell sites, Verisign, with OCCDESC "OTHER MEMO".

ONE CATEGORY KEPT ON A CROSS-PROJECT CONSISTENCY ARGUMENT RATHER THAN A LOCAL
ONE: "AUTO / TRUCK / VAN SALES" (car dealers - sampled: Braman Cadillac, used
car lots). A car lot is not a storefront in the walkable sense this map is
about, but NAICS 441 sits inside the 44/45 range every NAICS city here counts
as Retail, so excluding it in Miami alone would make the buckets mean different
things in different cities. Kept, and flagged here so the choice is visible.
"""

# CATGRYNAME (exact string as the county publishes it) -> bucket name from
# pipeline.taxonomies.CATEGORY_BUCKETS, or None for "checked, not storefront
# commercial for this project's purposes".
#
# Counts in comments are active rows at 2026-09-21, county-wide / City of
# Miami, and exist to show what each verdict is worth rather than as data.
CATEGORY_BUCKETS_BY_NAME = {
    # ---- Food service (NAICS 722) --------------------------------------
    "EATING ESTABLISHMENT": "Food service",            # 7,876 / 1,907
    "DANCING OR ENTERTAINMENT": "Food service",        #   293 /   128  bars
    "CATERING BUSINESS": "Food service",               #   282 /    70
    "NIGHT CLUB": "Food service",                      #    14 /     1

    # ---- Retail (NAICS 44/45) ------------------------------------------
    "RETAIL SALES": "Retail",                          # 15,049 / 3,054
    "PHARMACY": "Retail",                              #   532 /    88
    "AUTO / TRUCK / VAN SALES": "Retail",              # 1,366 /   195  see above
    "USED MOTOR VEHICLE PARTS DLR": "Retail",          #   436 /    21
    "PAWNBROKER": "Retail",                            #   279 /    93
    "FIREARMS SALES": "Retail",                        #    63 /    12

    # ---- Personal services (NAICS 812) ---------------------------------
    "BARBER / BEAUTY SHOP /SERVICE": "Personal services",   # 5,111 / 846
    "CLEANER/LAUNDRY/ALTERATIONS": "Personal services",     #   415 /  74
    "MASSAGE ESTABLISHMENT": "Personal services",           #   305 /  59
    "TATTOO STUDIO": "Personal services",                   #   235 /  56
    "ELECTROLYSIS SERVICE": "Personal services",            #    80 /  14
    "FUNERAL HOME": "Personal services",                    #    62 /  13

    # ---- Catch-alls: checked, excluded, reasons in the docstring --------
    "SERVICE BUSINESS": None,                          # 28,010 / 4,900
    "MULTIPLE SERVICE BUSINESS (3 +)": None,           #   739 /   129
    "TANGIBLE PERSONAL PROP DLR": None,                # 12,623 / 1,956
    "UNCLASSIFIED BUSINESS": None,                     #   238 /    41

    # ---- Offices and professional practice -----------------------------
    "PROFESSIONAL": None,                              # 22,512 / 3,875
    "P.A./CORP/PARTNERSHIP/FIRM": None,                # 13,421 / 2,692
    "ATTORNEY": None,                                  # 9,358 / 4,770
    "ATTORNEY (BRANCH OFFICE)": None,
    "CONSULTANT": None,                                # 4,221 / 1,003
    "FINANCE/INVESTMENT/HOLDING CO": None,
    "REAL ESTATE FIRM": None,
    "REAL ESTATE BRANCH OFFICE": None,
    "ADMIN OFFICE/OPERATION CTR": None,
    "INSURANCE ADJUSTER": None,
    "TITLE INSURANCE / ABSTRACT CO": None,
    "MORTGAGE BROKERAGE BUSINESS": None,
    "BANK / SAVINGS / TRUST CO": None,
    "BANKING FACILITY": None,
    "DEALER IN INTANGIBLE P P": None,
    "COLLECTION / CREDIT SERVICE": None,
    "BAIL BOND BUSINESS": None,
    "PRIVATE INVESTIGATIVE AGENCY": None,
    "GUARD PATROL AGENCY": None,
    "SECURITY SYSTEMS MONITORING": None,
    "TEMPORARY EMPLOYMENT AGENCY": None,
    "EMPLOYEE LEASING SERVICE": None,
    "PROMOTER / COORDINATOR": None,
    "TELEMARKETING": None,
    "HANDWRITING ANALYST": None,
    "AUCTIONEERING SERVICE": None,
    "SELLER OF TRAVEL": None,
    "ADVERTISING SPACE RENTAL": None,

    # ---- Residential and lodging: not commercial premises --------------
    "APARTMENTS": None,                                # 5,815 / 2,684
    "HOTEL/MOTEL/ BOARDING HOUSE": None,
    "MOBILE HOME PARK / CAMPGROUND": None,
    "TIME SHARE PROPERTY": None,
    "COMMERCL/INDUST/OFFICE SPACE": None,
    "SELF STORAGE": None,
    "PARKING FACILITY": None,
    "HALL FOR HIRE": None,

    # ---- Construction and trades ---------------------------------------
    "GENERAL BUILDING CONTRACTOR": None,
    "SPECIALTY BUILDING CONTRACTOR": None,
    "SUB-GENERAL BLDG CONTRACTOR": None,
    "SUB-BUILDING CONTRACTOR": None,
    "ELECTRICAL CONTRACTOR": None,
    "SPEC ELECTRICAL CONTRACTOR": None,
    "PLUMBING CONTRACTOR": None,
    "SPECIALTY PLUMBING CONTRACTOR": None,
    "GENERAL MECHANICAL CONTRACTOR": None,
    "SPEC MECHANICAL CONTRACTOR": None,
    "GENERAL ENGINEERING CONTRACTOR": None,
    "SPECIALTY ENGINEERING CONTRACT": None,
    "DEALER/DISTR/INSTALLATION": None,
    "PEST CONTROL SERVICE": None,
    "LOCKSMITH SERVICE": None,                # NAICS 561622, not 812
    "MOVING SERVICE (LOCAL)": None,
    "REPOSSESSING SERVICE": None,

    # ---- Automotive service (NAICS 811, not 812) -----------------------
    "AUTO / TRUCK / VAN SERVICE": None,
    "BODY / PAINT / REPAIR SHOP": None,
    "TOWING TRUCK": None,
    "AUTO TAG BRANCH AGENCY": None,

    # ---- Health and care -----------------------------------------------
    "CLINIC/MEDICAL CTR/DIALYSIS": None,
    "HOSPITAL / EMERGENCY ROOM": None,
    "PHYSICAL/OCCUP THERAPY CTR": None,
    "HEALTH TESTING NON-INVASIVE": None,
    "HEALTH TESTING INVASIVE": None,
    "HEALTH/DENTAL/MAINTN ORG": None,
    "DENTAL LAB": None,
    "DENTAL LAB SCHOOL": None,
    "BLOOD BANK CENTER": None,
    "VETERINARY CLINIC": None,
    "ASSISTED LIVING FACILITY": None,
    "NURSING / CONVALESCENT HOME": None,
    "HOME HEALTH CARE AGENCY": None,
    "HOME HEALTH CARE PROVIDER": None,
    "ADULT DAY CARE CENTER": None,
    "CHILD DAY CARE FACILITY": None,
    "HYPNOTHERAPIST": None,
    "PRESCRIPTION DRUG WHOLESALER": None,

    # ---- Education -----------------------------------------------------
    "EDUCATIONAL/TRAINING INST": None,
    "BARBER OR BEAUTY SCHOOL": None,
    "REAL ESTATE SCHOOL": None,

    # ---- Manufacturing, wholesale, industrial --------------------------
    "MFG/RECYCLING/PROCESSING": None,
    "FOOD PRODUCTS MFG / PROCESS": None,
    "PACKING / PROCESSING PRODUCE": None,
    "SLAUGHTER HOUSE": None,
    "SCRAP METAL PROCESSING": None,
    "JUNK DEALER / JUNK YARD": None,
    "LANDFILL / GARBAGE DUMP": None,
    "LPG TANK EXCHANGE / REFILL": None,
    "LPG INSTALLER": None,
    "LPG DEALER / MFG": None,
    "GAS PLANT": None,
    "ELECTRIC PLANT FRANCHISE": None,
    "RAILROAD": None,

    # ---- Mobile, itinerant and machine licences ------------------------
    # Excluded on the same rule as every other city: permanent fixed
    # premises only. A machine or a truck has no storefront to be near.
    "LUNCH WAGON / TRUCK": None,                       #   213 /    71
    "ICE CREAM VENDOR": None,
    "PEDDLER": None,
    "TRAVELING JUNK DEALER": None,
    "CARNIVAL - SPONSORED": None,
    "FLEA MARKET": None,
    "FARMERS MARKET": None,
    "A T M / POINT OF SALE": None,                     # 1,353 /   248
    "VENDING MACHINE": None,
    "LAUNDRY MACHINE": None,                           #   424 /    91  see above
    "SERVICE / AMUSEMENT MACHINE": None,
    "BULK MDS VEND (UP TO 9 UNITS)": None,
    "COURIER DROP BOX": None,
    "PAY TELEPHONE PROVIDER": None,

    # ---- Recreation, entertainment venues, media -----------------------
    # NAICS 713/711, which no bucket covers in any city here.
    "FITNESS CENTER (MEMBERSHIP)": None,
    "FITNESS CENTER (NON MEMBER)": None,
    "AMUSMNT FACILITY/DEV (NONCOIN)": None,
    "MOVIE / MULTI THEATRE": None,
    "AUDITORIUM/PLAYHOUSE/STADIUM": None,
    "PERMANENT EXHIBIT / ADMISSION": None,
    "PROFESSIONAL SPORTS TEAM": None,
    "PRODUCER / RECORDING STUDIO": None,
    "FILM INDUSTRY": None,
    "CRUISE LINES / DINNER CRUISE": None,
    "PARI-MUTUEL WAGERING": None,
    "BINGO OPERATOR": None,
    "BINGO LESSOR": None,
    "DATING / ESCORT BUSINESS": None,
    "FORTUNETELLER": None,

    # ---- Communications and utilities ----------------------------------
    "COMMUNICATION BUSINESS": None,
    "NON VOCAL COMMUNICATIONS": None,
    "LOCAL EXCHANGE TELECOMMUNIC": None,
    "RESALE OF COMM TIME": None,
    "CABLE TV FRANCHISE": None,

    # ---- Other -------------------------------------------------------
    "NON-PROFIT CHAR / REL / EDUC": None,
    "MEMBERSHIP ORGANIZATION": None,
    "PASSENGER TRANSPORTATION SERV": None,
    "CEMETERY / CREMATORIES, ETC.": None,
    "OCCASIONAL SALES - EXEMPT": None,
}

FIELD_LABEL = "Business category"
VALUE_COLUMN = "catgryname"

# Read by step 2's dedup: when one premises holds licences in several buckets,
# which bucket wins. 477 of 6,128 City of Miami premises (7.2%) hold more than
# one - "KIKI ON THE RIVER" holds Dancing + Eating + Retail, pharmacies hold
# Pharmacy + Retail Sales, jewellers hold Pawnbroker + Retail Sales.
#
# Retail loses on purpose: RETAIL SALES is the category a premises picks up
# SECONDARILY (a restaurant selling merchandise, a salon selling product), so
# letting it win would relabel restaurants and salons as shops. Between the
# other two, Food service wins because an eating place that also cuts hair is
# vanishingly rare while the reverse - a salon holding a food licence for
# retail drinks - is not.
BUCKET_PRIORITY = ["Food service", "Personal services", "Retail"]


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """CATGRYNAME -> bucket, or None. Unknown values return None; step 2
    reports them so an upstream rename is visible rather than silent."""
    raw = row.get(VALUE_COLUMN)
    if raw is None:
        return None
    return CATEGORY_BUCKETS_BY_NAME.get(str(raw).strip().upper())
