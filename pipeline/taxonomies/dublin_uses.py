"""Dublin: Tailte Eireann's `Uses` field, the Irish rateable valuation register.

WHY `Uses` AND NOT `Category`. The register carries both. `Category` is 13
values with a 3.2% catch-all; `Uses` is 963 values with 16.4%. Dublin keys on
the level with the LARGER catch-all, which inverts Barcelona's rule, because
catch-all share is a tiebreaker and separability is the criterion: `Category`
puts 1,483 of 2,335 food-service rows and 677 of 744 personal-service rows
inside `RETAIL (SHOPS)`, so all three buckets collapse into one. Measured
2026-09-22; see docs/build_briefs/dublin.md.

WHY SEGMENTS AND NOT WHOLE STRINGS. `Uses` is multi-valued: comma-separated,
with `-` as a null placeholder ("SHOP, -", "-, RESTAURANT", "STORE, YARD").
963 distinct strings reduce to **318 distinct segments**, and mapping segments
means a combination this project has never seen still classifies. 1,869 rows
carry two real uses; in `ValuationReport`, "STORE, YARD" resolves to floors
STORE and YARD, so these are genuine mixed-use premises, not a formatting
artefact.

BUCKET BOUNDARIES ARE NAICS', NOT THIS MODULE'S. The twelve NAICS and
NAICS-like cities use Retail = 44/45, Food service = 722, Personal services =
812, so Dublin follows the same lines rather than inventing its own. Every
judgment call where the Irish vocabulary does not map cleanly is named below,
because a bucket call that is not written down is indistinguishable from an
oversight.
"""

FIELD_LABEL = "Use"
VALUE_COLUMN = "Uses"

# `Category` is carried through step 2 to disambiguate the two generic
# segments below - the Chicago EXTRA_COLUMNS mechanism, used for the one job
# `Category` is actually good at.
EXTRA_COLUMNS = ("Category",)

SEPARATOR = ","
NULL_SEGMENT = "-"

# --- Retail: NAICS 44/45 equivalents ---------------------------------------
#
# Food SHOPS are retail (NAICS 445), not food service - a butcher, greengrocer
# or bakery sells goods; a cafe sells a sitting. The line is consumption on the
# premises, which is also where NAICS draws it.
_RETAIL = {
    "CLOTHES SHOP", "SHOP (OFFICES)", "KIOSK", "PHARMACY",
    "CONVENIENCE STORE [<200 SQ. M.]", "NEWSAGENT", "OFF-LICENCE", "JEWELLERS",
    "BUTCHER", "BUTCHERS / FISH MONGERS", "DEPARTMENT STORE", "SHOE SHOP",
    "ETHNIC FOOD SHOP", "FURNISHINGS", "CHARITY SHOP", "FLORIST", "BOOKSHOP",
    "GREENGROCER", "PHONE SHOP", "OPTICIAN", "SPORTS SHOP", "DELICATESSEN",
    "FURNITURE", "HOUSEHOLD GOODS", "CONFECTIONERY", "FASHION ACCESSORY",
    "HEALTH FOOD SHOP", "ANTIQUE SHOP", "CYCLE SHOP", "CRAFT SHOP",
    "CARD / STATIONERY / PRINT", "OFFICE SUPPLIES", "DISCOUNT STORE",
    "DISCOUNT", "PET SHOP", "COMPUTER SHOP", "COSMETIC SHOP", "GARDEN CENTRE",
    "GARDEN SHOP", "VIDEO SHOP", "MUSIC-INSTRUMENTS",
    "MUSIC-RECORDS / DVDS / VIDEOS", "BAKERY", "GAME SHOP", "TOY SHOP",
    "BRIDAL / FORMAL WEAR", "ADULT SHOP", "TILE", "TILE SHOP", "HARDWARE",
    "HARDWARE / DIY", "DIY SUPERSTORE", "ADVENTURE / ARMY / CAMPING",
    "LIGHTING / LAMP", "FIREPLACES", "PEN SHOP", "ELECTRICAL / ELECTRONIC",
    "MOTOR ACCESSORIES", "SUPERMARKET", "SUPERMARKET 1 [200-500 SQ. M.]",
    "SUPERMARKET 2 [500-2500 SQ. M.]", "SUPERMARKET 3 [> 2500 SQ. M.]",
    "RETAIL WAREHOUSE", "NURSERY (MOTHERCARE)",
    "NURSERY  (MOTHERCARE)",   # the register carries both spacings
    # NAICS 441 motor vehicle dealers and 457 fuel stations both sit inside
    # retail trade, so these follow rather than being carved out by taste.
    # GARAGE and MOTOR WASH do NOT - they are repair (811), excluded below.
    "MOTOR SHOWROOM", "SERVICE STATION", "MOTORWAY SERVICE STATION",
    "MOTOR FUEL SALES",
}

# --- Food service: NAICS 722 ------------------------------------------------
_FOOD = {
    "RESTAURANT", "RESTAURANT (DRIVE THRU)", "PUB", "CAFE", "COFFEE SHOP",
    "TAKE AWAY", "INDIAN TAKE AWAY", "SANDWICH / JUICE BAR",
    # INTERNET CAFE left on 2026-09-29: a PC room, which is recreation in every
    # city (owner, DECISIONS "Category check: the owner's calls").
    # NAICS 7224 drinking places. A nightclub sells drink on the premises;
    # CASINO does not and is excluded below as NAICS 713 gambling.
    "NIGHT CLUB / DISCOTHEQUE",
}

# --- Personal services: NAICS 812 -------------------------------------------
#
# 812 is services performed on a person or their personal effects: 8121
# personal care, 8122 death care, 8123 laundry, 8129 other (incl. pet care and
# photofinishing). 8122 is carved out, as naics.py does: funeral services off
# every map (owner, 2026-09-28).
#
# SHOE REPAIR / KEY CUT, ALTERATIONS and TAILORING were a deliberate departure
# until 2026-09-29, counted as personal services "toward the everyday meaning
# of a high street". They are NAICS 811 repair, and repairs are out in every
# city (owner, 2026-09-29, DECISIONS "Category check: the owner's calls"), so
# they are now listed with the repair uses below.
# KENNELS is 812910 pet care and included; PET SHOP is 453910 and retail.
_PERSONAL = {
    "HAIRDRESSING SALON", "BARBER", "BEAUTY SALON / MASSAGE", "TATTOO PARLOUR",
    "DRY CLEANERS / LAUNDERETTE", "LAUNDRY",
    "PHOTO PROCESSING SHOP", "KENNELS",
}

# --- The two generic segments, resolved by `Category` -----------------------
#
# SHOP (5,827 rows) and STORE (909) say nothing on their own, and they do not
# mean the same thing: in this register a STORE is usually a storage building,
# sitting beside WAREHOUSE and YARD under INDUSTRIAL USES. `Category` is the
# one field that separates them reliably, so it is used here and only here.
_GENERIC = {"SHOP", "STORE"}
_RETAIL_CATEGORIES = {"RETAIL (SHOPS)", "RETAIL (WAREHOUSE)"}

# --- Uses that OVERRIDE the generic SHOP / STORE ----------------------------
#
# Retail until 2026-09-29, when two owner rules took them off every map:
#   - Gambling (owner, 2026-09-29): BETTING SHOP (176 rows), and CASINO,
#     AMUSEMENT CENTRE and BINGO HALL, which were already excluded on their
#     own but still reached the map as Retail through a "SHOP" segment beside
#     them ("SHOP, CASINO", "AMUSEMENT CENTRE, SHOP").
#   - Street and market stalls (owner, 2026-09-29): MARKET.
# KIOSK stays Retail (owner, 2026-09-29): a kiosk is a small walk-in shop, as
# a newsstand is.
# The generic segment is the unit's TYPE, not its trade, so "SHOP, BETTING
# SHOP" is a betting shop and must not come back as Retail through "SHOP".
# A second SPECIFIC use still classifies ("AMUSEMENT CENTRE, ELECTRICAL /
# ELECTRONIC" is an electronics shop) - the module's own rule that the
# specific activity wins.
#   - Recreation and repair (owner, 2026-09-29, DECISIONS "Category check: the
#     owner's calls"): a gym, snooker hall or repair shop beside a generic
#     SHOP segment is still a gym, snooker hall or repair shop.
_OVERRIDES_GENERIC = {
    "BETTING SHOP", "CASINO", "AMUSEMENT CENTRE", "BINGO HALL",   # (owner, 2026-09-29) R5
    "MARKET",                                                    # (owner, 2026-09-29) R1
    "GYMNASIUM / FITNESS CENTRE", "SNOOKER HALL", "BOWLING-ALLEY", "SQUASH COURT",
    "SWIMMING POOL", "SPORTS & LEISURE CENTRE", "CINEMA", "DANCE STUDIO",
    "INTERNET CAFE",                                             # recreation
    "REPAIRS", "SHOE REPAIR / KEY CUT", "ALTERATIONS", "TAILORING",   # repair
}

# --- Explicitly not storefront ---------------------------------------------
#
# Recorded rather than left to fall through, because an unmapped segment and a
# deliberately excluded one look identical at the point of use. Step 2 prints
# any segment that is neither mapped nor listed here, so this list is what
# keeps that report meaningful.
#
# ADVERTISING STATION and every SHEET * value are advertising hoardings -
# "48 sheet", "6 sheet" and "96 sheet" are billboard sizes, not premises. They
# would otherwise have read as some kind of retail unit.
_NOT_STOREFRONT_PREFIXES = (
    "OFFICE", "WAREHOUSE", "WORKSHOP", "FACTORY", "YARD", "CAR PARK",
    "SHEET", "SURGERY", "CRECHE", "CLUB HOUSE", "STADIUM", "NETWORK",
    "PLANT/OTHER", "SHOWROOM", "BUS ", "AIRPORT", "TRAINING CEN",
)
_NOT_STOREFRONT = {
    "ADVERTISING STATION", "NO USE SELECTED", "NO USE SELETCED", "OTHER",
    "MISCELLANEOUS", "VACANT", "DEMOLISHED / INCAPABLE OF USE", "DOMESTIC",
    "HOUSE", "RIGHT OF TRADING", "ATM", "POST BOX", "MAST", "MAST/ANTENNA",
    # 8122 death care: funeral services off every map (owner, 2026-09-28).
    # CEMETERY OR CREMATORIUM is further down, with the leisure uses.
    "FUNERAL HOME",
    # Gambling, and markets (owner, 2026-09-29): see _OVERRIDES_GENERIC
    # above. CASINO, AMUSEMENT CENTRE and BINGO HALL are listed with the
    # leisure uses further down.
    "BETTING SHOP", "MARKET",
    # Accommodation is not one of this project's buckets. The
    # premises-taxonomy skill flags it specifically because it hides inside
    # food service in three other countries; here it is its own vocabulary.
    "HOTEL", "APART / HOTEL", "GUESTHOUSE", "GUEST ACCOMMODATION", "HOSTEL",
    "CARAVAN PARK", "HOLIDAY COMPLEX", "CENTRE FOR ASYLUM SEEKERS",
    # Finance, property and travel are storefronts but are NAICS 52/53/56,
    # outside all three buckets - the same reason a bank is absent from every
    # NAICS city here.
    "BANK", "CREDIT UNION", "BUILDING SOCIETY", "AUCTIONEER", "TRAVEL AGENCY",
    "TAXI OFFICE", "TOURIST OFFICE", "POST OFFICE",
    # Health and care: NAICS 62, not 812.
    "CLINIC", "MEDICAL CENTRE", "MEDICAL CLINIC", "HEALTH CENTRE", "HOSPITAL",
    "PRIMARY CARE CENTRE", "NURSING HOME", "RESIDENTIAL CARE HOME",
    "DENTAL WORKSHOP", "DAY CARE CENTRE", "LABORATORY", "HEALTH FARM",
    # Education, culture, sport, leisure: NAICS 61/71.
    "SCHOOL", "COLLEGE", "MONTESSORI", "MUSEUM", "ART GALLERY", "THEATRE",
    "CINEMA", "LIBRARY", "GYMNASIUM / FITNESS CENTRE", "SWIMMING POOL",
    "SPORTS & LEISURE CENTRE", "SPORTS GROUNDS", "SNOOKER HALL", "BINGO HALL",
    "BOWLING-ALLEY", "SQUASH COURT", "AMUSEMENT CENTRE", "CASINO",
    "DANCE STUDIO", "STUDIO", "ACTIVITY CENTRE", "OUTDOOR ACTIVITY CENTRE",
    "GOLF DRIVING RANGE", "EQUESTRIAN CENTRE", "RACE TRACK (HORSES)",
    "MARINA", "CONFERENCE CENTRE", "EVENT SPACE", "COMMUNITY CENTRE",
    "COMMUNITY HALL", "HALL", "PASTORAL CENTER", "VISITOR CENTRE",
    "HERITAGE / INTERPRETATIVE CENTRE", "CEMETERY OR CREMATORIUM",
    # Repair, industry, utilities, infrastructure.
    "GARAGE", "MOTOR WASH", "VEHICLE TEST CENTRE", "VEHICLE HIRE", "REPAIRS",
    "SHOE REPAIR / KEY CUT", "ALTERATIONS", "TAILORING",   # (owner, 2026-09-29) repairs out
    "INTERNET CAFE",                                        # (owner, 2026-09-29) a PC room
    "CAR VALET AREA (NO BUILDINGS)", "SERVICE STATION (NO SHOP)",
    "DATA CENTRE", "PRINTING WORKS", "CONCRETE WORKS", "ASHPHALT PLANT",
    "DISTILLERY", "BREWERY", "FOOD PREPARATION", "COLD STORE", "CHILL STORE",
    "BULK STORES", "GRAIN STORES", "PROVENDER MILL / FLOUR MILL",
    "DISTRIBUTION CENTRE", "DEPOT", "OIL / FUEL DEPOT", "AVIATION FUEL DEPOT",
    "HANGAR", "APRON", "TERMINAL", "PORT", "QUARRY", "LANDFILL SITE",
    "RECYCLING CENTRE", "INCINERATOR", "EFFLUENT TREATMENT WORKS",
    "WATERWORKS", "GENERATING STATION", "TRANSMISSION STATION", "SOLAR FARM",
    "WIND FARM", "ELECTRICITY", "PUBLIC UTILITY", "PIPELINE", "CANAL",
    "TOLLS", "WEIGHBRIDGE", "TANK", "FISHERY", "STABLE", "SECURITY BUILDING",
    "FIRE STATION", "SORTING OFFICE", "RAILWAY STATION", "TAXI SHELTER",
    "BIKE STATIONS", "ELECTRIC VEHICLE (EV) CHARGING STATION",
    "CABLE LANDING STATION", "AERODROME", "WAREHOUSE CASH &CARRY",
}


def _segments(value):
    """Split `Uses` into real segments, dropping the `-` placeholder."""
    out = []
    for part in str(value or "").split(SEPARATOR):
        part = part.strip()
        if part and part != NULL_SEGMENT and part not in out:
            out.append(part)
    return out


def display_value(value):
    """What the map tooltip should SHOW for this row's `Uses`.

    OPTIONAL TAXONOMY HOOK - `pipeline/map_common.py` uses it when a taxonomy
    defines one and falls back to the raw column otherwise.

    The register stores a fixed number of use slots per premises and fills the
    unused ones with `-`, so the raw string reads "-, SHOP". `_segments()`
    drops that placeholder for CLASSIFICATION; this drops it for the tooltip.
    On the committed map of 2026-09-22, **6,750 of 7,595 pins (88.9%)
    displayed a `-` segment** and **none was entirely blank**, which is why
    the placeholder can be dropped outright rather than merely sorted last.

    Falls back to the raw value if nothing survives, rather than rendering an
    empty field: that cannot happen with today's data, and if the register
    ever changes shape, showing what it said beats showing nothing.
    """
    parts = _segments(value)
    return ", ".join(parts) if parts else str(value or "").strip()


def bucket_for_segment(segment, category=None):
    """One segment -> a bucket, or None. Exposed so step 2 can report."""
    if segment in _FOOD:
        return "Food service"
    if segment in _PERSONAL:
        return "Personal services"
    if segment in _RETAIL:
        return "Retail"
    if segment in _GENERIC:
        # Generic on its own; `Category` is what separates a retail shop from
        # an industrial store.
        return "Retail" if category in _RETAIL_CATEGORIES else None
    return None


def is_known(segment):
    """Whether a segment has been looked at, mapped or not.

    Step 2 uses this to report segments that are NEITHER classified NOR
    deliberately excluded - the ones a new register refresh would introduce.
    """
    if segment in _FOOD or segment in _PERSONAL or segment in _RETAIL:
        return True
    if segment in _GENERIC or segment in _NOT_STOREFRONT:
        return True
    return segment.startswith(_NOT_STOREFRONT_PREFIXES)


# When one premises carries uses in two different buckets, the more specific
# activity wins over the residual one. Retail is the residual here - "SHOP,
# HAIRDRESSING SALON" is a salon, and a premises that is both a cafe and a
# bookshop is a cafe on this map. Food service is ordered ahead of personal
# services only to make the tie deterministic; step 2 prints how often the two
# actually collide, and it is a handful of rows.
_PRIORITY = ("Food service", "Personal services", "Retail")


def classify(row):
    """A register row -> a bucket name, or None if it is not a storefront."""
    category = row.get("Category")
    segments = _segments(row.get(VALUE_COLUMN))
    if any(s in _OVERRIDES_GENERIC for s in segments):
        # (owner, 2026-09-29) the generic unit type does not rescue a betting
        # shop, a casino or a market stall.
        segments = [s for s in segments if s not in _GENERIC]
    found = {bucket_for_segment(s, category) for s in segments}
    found.discard(None)
    for bucket in _PRIORITY:
        if bucket in found:
            return bucket
    return None


def legend_label(bucket):
    return bucket


_SHOPS = "RETAIL (SHOPS)"
for _uses, _want in [("-, BETTING SHOP", None), ("SHOP, BETTING SHOP", None),
                     ("SHOP, CASINO", None), ("AMUSEMENT CENTRE, SHOP", None),
                     ("MARKET", None), ("SHOP, MARKET", None),
                     ("-, KIOSK", "Retail"), ("SHOP, KIOSK", "Retail"),
                     ("AMUSEMENT CENTRE, ELECTRICAL / ELECTRONIC", "Retail"),
                     ("PHOTO PROCESSING SHOP, KIOSK", "Personal services"),
                     ("-, NEWSAGENT", "Retail"), ("SHOP, -", "Retail"),
                     ("-, ADULT SHOP", "Retail"),
                     ("NIGHT CLUB / DISCOTHEQUE", "Food service"),
                     ("GYMNASIUM / FITNESS CENTRE, SHOP", None), ("SHOP, SNOOKER HALL", None),
                     ("INTERNET CAFE, -", None), ("-, SHOE REPAIR / KEY CUT", None),
                     ("-, TAILORING, ALTERATIONS, REPAIRS", None),
                     ("SHOP, FUNERAL HOME", "Retail"),      # owner-accepted edge case
                     ("DRY CLEANERS / LAUNDERETTE, ALTERATIONS", "Personal services")]:
    assert classify({VALUE_COLUMN: _uses, "Category": _SHOPS}) == _want, (_uses, _want)
for _s in _OVERRIDES_GENERIC:
    assert is_known(_s) and bucket_for_segment(_s, _SHOPS) is None, _s
