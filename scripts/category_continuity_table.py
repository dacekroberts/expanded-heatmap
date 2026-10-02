"""The cross-city category table that scripts/check_category_continuity.py runs.

One RULE per trade in docs/category_rules.md, and one COLUMN per taxonomy in
pipeline/taxonomies/: for every rule, the rows that locate the trade in that
register, or a declared reason it is not there.

HOW TO ANSWER A RULE FOR A TAXONOMY (one of these per cell):

  [loc(row, label), ...]     rows in this register that ARE the trade. `row` is
                             the dict classify() receives, or a bare string for
                             {VALUE_COLUMN: string}. Each must give the rule's
                             verdict.
  exception(row, label, result, decision, why[, path, token])
                             a disclosed departure the OWNER decided. `decision`
                             is a substring of a DECISIONS heading; the check
                             fails if it is not one, and fails if the row ever
                             comes back into line (a stale exception). With
                             row=None it is made before classify(), pinned by
                             `token` in `path`, as pending() below.
  pending(row, label, result, since, note[, path, token])
                             a departure this table FOUND and the owner has not
                             ruled on. Passes, but is printed on every run: a
                             dated defect, not a pass (check_provenance.py's
                             KNOWN_GAPS convention). Resolve it into a loc() or
                             an exception() once the owner rules. With row=None
                             it is a departure made before classify() (a step-2
                             filter), pinned by `token` in `path`.
  outside(path, token, what) the trade is decided before classify(), by a city
                             config or a step-2 filter; `token` must stay in
                             `path`. May sit in a list beside loc() rows.
  absent(reason, ignore=())  the register has no such category. The check reads
                             the module's own string constants for the rule's
                             keywords and fails on a hit, so list a string that
                             is not the trade in `ignore`, with why in `reason`.

THREE PER-TAXONOMY HOOKS, below the rules: ROW_KEY (the key a bare-string row
goes under, when classify() reads another column than VALUE_COLUMN - SCIAN
reads the code, not its label), CLASSIFY_VIA (when classify() is not where the
trade is decided - Brazil's step 2 calls classify_description() on free text,
and classify() only reads the stored bucket back), and EXTRA_SOURCES (helper
modules whose string constants count as the taxonomy's vocabulary).

A rule with required=False is a sub-case (funeral-goods shops, tattoo, health
food); a column may leave it out, but only while none of its keywords appears
in the module.

NEVER edit a taxonomy to make this table pass, and never widen a cell to
swallow a failure: a departure goes to the owner with the precedent it breaks
(docs/category_rules.md, "How to use it").
"""

OUT = None


class Rule:
    def __init__(self, verdict, doc_row, precedent, keywords=None, required=True, sub=False):
        self.verdict = verdict        # None (out) or a bucket name
        self.doc_row = doc_row        # the start of its Trade cell in docs/category_rules.md
        self.precedent = precedent    # quoted in a failure
        self.keywords = keywords      # regex over a module's string constants (property F)
        self.required = required      # False: a sub-case a column may leave out
        self.sub = sub                # True: its verdict differs from its doc row's


class _Entry:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)

    def __repr__(self):
        return f"{self.kind}({self.__dict__})"


def loc(row, label):
    return _Entry("loc", row=row, label=label)


def exception(row, label, result, decision, why, path=None, token=None):
    """row=None: an owner-decided departure made before classify(), pinned by `token` in `path`."""
    return _Entry("exception", row=row, label=label, result=result, decision=decision, why=why,
                  path=path, token=token)


def pending(row, label, result, since, note, path=None, token=None):
    """row=None: a departure made before classify(), pinned by `token` in `path`."""
    return _Entry("pending", row=row, label=label, result=result, since=since, note=note,
                  path=path, token=token)


def fixed(row, label, _was_result, fixed_on, note, **_):
    """A pending departure whose fix has landed: a loc(), with its history kept.
    `fixed_on` is the date the owner approved it (the pending row's `since`)."""
    return _Entry("loc", row=row, label=f"{label} [fixed, approved {fixed_on}]", note=note)


def outside(path, token, what):
    return _Entry("outside", path=path, token=token, what=what)


def absent(reason, ignore=()):
    return _Entry("absent", reason=reason, ignore=tuple(ignore))


# ---------------------------------------------------------------------------
# THE RULES - docs/category_rules.md, one per trade. Keywords are for property
# F only: what a module's own code table would say if it had the trade.
# ---------------------------------------------------------------------------
RULES = {
    "funeral": Rule(
        OUT, "Funeral homes", "NAICS 8122, SCIAN 8123, NAF 96.03Z, Rev. 2.1 96.30 (owner, 2026-09-28)",
        r"funeral|funer[aá]ri|crematori|cemeter|cementer|mortuar|undertaker|begrav|bestattung|"
        r"pohřeb|pompes fun|velatorio|sepelio|onoranze|장례|장의|葬|殯"),
    "funeral_goods": Rule(
        "Retail", "Funeral homes", "shops selling funeral goods stay Retail (owner, 2026-09-28)",
        required=False, sub=True),
    "no_counter_food": Rule(
        OUT, "Food with no counter", "R1: Madrid's 1,157 canteens; NAICS 72231-72233 (owner, 2026-09-29)",
        r"cater|canteen|traiteur|comedor|kantin|mensa|jídeln|refeit|仕出|給食|급식|구내식당|"
        r"stall|market vendor|concession"),
    "personal_catchall": Rule(
        OUT, "The \"other personal services\"", "R2: NAICS 812990 in San Diego, Montréal, Mexico, "
        "Madrid, Taiwan (owner, 2026-09-29)",
        r"other personal|miscellaneous personal|otros servicios personales|autres services personnels|"
        r"tarot|astrolog|fortune|psychic|matchmak|marriage intro|wedding|婚|占|결혼"),
    "tattoo": Rule(
        "Personal services", "The \"other personal services\"", "R2: tattoo stays where it has its own code",
        r"tattoo|tatuaj|tatouage|타투|문신|刺青|紋身", required=False, sub=True),
    "adult_hostess": Rule(
        OUT, "Adult and hostess", "R3: Tokyo's cabarets and snack bars, San Diego's massage parlors, "
        "Calgary's body-rub centres, Seoul's 유흥주점 (owner, 2026-09-29)",
        r"adult|cabaret|hostess|body.?rub|strip|erotic|escort|유흥|キャバレー|スナック|有女陪侍|酒家"),
    "korean_karaoke_bar": Rule(
        "Food service", "Korean karaoke bars", "R3: Seoul, Daegu, Busan (owner)",
        r"단란", required=False),
    "sex_shop": Rule(
        "Retail", "Sex shops", "R3 (owner)", r"sex ?shop|sexshop|erotic (store|shop)|adult entertainment store"),
    "massage_commercial": Rule(
        "Personal services", "Commercial massage", "NAICS 812199; D.C., Miami, Chicago, Calgary, Dublin, "
        "Milan, Buenos Aires, Brazil, Korea (owner, 2026-09-29)",
        r"massag|masaj|massaggi|마사지|안마|按摩|マッサージ|shiatsu|reflexolog"),
    "massage_regulated": Rule(
        OUT, "Regulated massage", "Vancouver's and Toronto's RMTs (NAICS 621)",
        r"massage therap|\bRMT\b"),
    "car_dealer": Rule(
        "Retail", "Car dealers", "R4: about 40 cities (owner, 2026-09-29)",
        r"car dealer|auto(mobile)? dealer|motor ?vehicle dealer|vehicle sales|motorcycle|"
        r"autom[oó]viles|autoveicol|kraftwagen|autohandel|자동차 ?판매|자동차 ?매매|汽車|自動車販売"),
    "petrol_station": Rule(
        "Retail", "Car dealers", "R4: petrol and LPG stations kept (owner, 2026-09-29)",
        r"filling station|gas station|service station|fuel|petrol|gasolin|tankst|carburant|"
        r"주유|충전소|加油|ガソリン"),
    "vehicle_repair": Rule(
        OUT, "Repairs", "NAICS 811; vehicle repair and wholesale stay out (R4)",
        r"auto ?repair|vehicle repair|auto body|body shop|car wash|mecánic|autoriparaz|"
        r"funilaria|정비|自動車整備"),
    "gambling": Rule(
        OUT, "Gambling", "R5: Dublin's 176 betting shops (owner, 2026-09-29)",
        r"betting|bookmak|casino|lotter|loter|bingo|gambl|games of chance|apuesta|scommess|"
        r"wett|sázk|복권|彩券|賭"),
    "pawnbroker": Rule(
        "Retail", "Pawnbrokers", "R5: kept; New York and Chicago the disclosed exceptions (owner)",
        r"pawn|empeño|empeno|전당|當鋪|質屋|pfand"),
    "nightclub": Rule(
        "Food service", "Nightclubs", "R5: Toronto and Edmonton aligned (owner, 2026-09-29)",
        r"night ?club|discot|dance club|dancing|nachtclub|boîte de nuit|centros nocturnos|夜店|클럽"),
    "vet": Rule(
        OUT, "Veterinary", "NAICS 541940; six cities (R5)",
        r"veterin|dyrl|동물병원|獸醫|動物病院"),
    "nonstore": Rule(
        OUT, "Nonstore retail", "NAICS 454 in every NAICS city",
        r"nonstore|non-store|e-?commerce|mail.?order|online|direct.?sell|door.to.door|"
        r"통신판매|방문판매|網路|vending"),
    "parking": Rule(
        OUT, "Parking", "NAICS 81293",
        r"parking|estacionamiento|stationnement|parkhaus|주차|停車|駐車"),
    "repair": Rule(
        OUT, "Repairs", "NAICS 811, not 812",
        r"repair|alteration|reparaci|riparaz|réparation|reparatur|수리|修理|修繕"),
    "lodging": Rule(
        OUT, "Lodging", "every city; premises-taxonomy Step 5",
        r"hotel|motel|lodging|hostel|guest ?house|숙박|旅館|民宿|hospedaje|alojamiento|albergh|hébergement"),
    "recreation": Rule(
        OUT, "Recreation", "NAICS 71",
        r"\bgym|fitness|노래연습|pc ?방|cinema|theatre|theater|bowling|billiard|amusement|"
        r"gimnas|palestr|체력단련"),
    "pharmacy": Rule(
        "Retail", "Pharmacies", "NAICS 44-45 in general-retail registers; a food-only register's "
        "pharmacies are out (Stockholm)",
        r"pharmac|drug ?store|farmac|apotek|apothek|lékárn|약국|藥局|薬局|drogar"),
    "pharmacy_food_register": Rule(
        OUT, "Pharmacies", "a food-only register's pharmacies are out: not food shops (Stockholm)",
        required=False, sub=True),
    "optician": Rule(
        "Retail", "Pharmacies", "NAICS 44-45 (opticians)",
        r"optic|optik|óptic|opticien|안경|眼鏡"),
    "health_food": Rule(
        "Retail", "Health-food sellers", "in-store only (Seoul, Daegu, Busan, Incheon)",
        r"health.?food|건강기능|健康食品", required=False),
    "health_food_nonstore": Rule(
        OUT, "Health-food sellers", "e-commerce, door-to-door and multilevel sellers out",
        required=False, sub=True),
    "person_licence": Rule(
        OUT, "A person's own license", "San Francisco's practitioner licenses (owner, 2026-10-01); "
        "New York's, Calgary's and Edmonton's chair renters and practitioners",
        r"(tattoo|piercing|massage|enhancement)\W+practitioner|chair.?rent|booth.?rent|chair operator|"
        r"area renter|beauty booth|working in another's shop",
        required=False),
    "mobile_unit": Rule(
        OUT, "Mobile units", "Bucharest, Seoul (food trucks), Glasgow (mobile caterers)",
        r"mobile|food truck|truck|cart\b|peddl|pedlar|hawker|vendor|ambulant|푸드트럭|屋台|攤販"),
}


# ---------------------------------------------------------------------------
# THE COLUMNS
# ---------------------------------------------------------------------------
R1 = "Funeral exclusions coded; fringe-category audit"       # the R1-R5 entry
FOLLOWUPS = "Exclusions batch: the owner's eight follow-ups"
CONFIRMED = "Category check: three older calls confirmed"   # Berlin tattoo, FSA pharmacies, Melbourne opticians
RULED = "Category check: the owner's calls on the pending departures"

COLUMNS = {}

COLUMNS["naics"] = {
    "funeral": [loc("812210", "funeral homes"), loc("812220", "cemeteries and crematories")],
    "funeral_goods": [loc("453998", "all other misc. store retailers (2017; casket and monument dealers)")],
    "no_counter_food": [
        loc("722310", "food service contractors"), loc("722320", "caterers"),
        loc("72231", "food service contractors, San Diego's five digits"),
        outside("pipeline/san_diego/config.py", '"72234"', "San Diego's cottage-food home kitchens"),
        exception("722300", "special food services (undifferentiated)", "Food service", FOLLOWUPS,
                  "Los Angeles's 722300 mixes caterers and trucks with taquerias and cafés and "
                  "cannot be split; kept whole and disclosed (follow-up 8)")],
    "personal_catchall": [
        loc("812990", "all other personal services"), loc("81299", "the same, San Diego's five digits"),
        outside("pipeline/san_diego/config.py", '"8129"', "San Diego's group-level 8129")],
    "tattoo": [loc("812199", "other personal care services (tattoo parlours)")],
    "adult_hostess": [loc("812193", "San Diego's own MASSAGE PARLORS")],
    "sex_shop": [loc("459999", "all other miscellaneous retailers (sex shops file here)")],
    "massage_commercial": [loc("812199", "other personal care services (massage)"),
                           loc("812198", "San Diego's MASSAGE THERAPY"),
                           loc("812194", "San Diego's MASSAGE TECHNICIAN")],
    "massage_regulated": [loc("621399", "offices of all other health practitioners")],
    "car_dealer": [loc("441110", "new car dealers"), loc("441120", "used car dealers"),
                   loc("441221", "motorcycle dealers (2017)"),
                   loc("441227", "motorcycle, ATV and other vehicle dealers (2022)")],
    "petrol_station": [loc("447110", "gasoline stations with convenience stores (2017)"),
                       loc("447100", "gasoline stations (Los Angeles's four-digit form)"),
                       loc("457110", "gasoline stations with convenience stores (2022)"),
                       loc("457120", "other gasoline stations (2022)")],
    "vehicle_repair": [loc("811111", "general automotive repair"), loc("811121", "auto body"),
                       loc("423110", "automobile wholesale")],
    "gambling": [loc("713210", "casinos"), loc("713290", "other gambling industries"),
                 loc("713200", "gambling industries (Los Angeles's form)")],
    "pawnbroker": absent("no code of its own: NAICS files pawnshops under 522298 / 522299 with every "
                         "other non-bank lender (San Francisco 20, San Diego 10, Los Angeles 6 rows), "
                         "so none can be kept without the rest"),
    "nightclub": [loc("722410", "drinking places (nightclubs file here)")],
    "vet": [loc("541940", "veterinary services")],
    "nonstore": [
        loc("454110", "electronic shopping (2017)"), loc("454210", "vending machine operators (2017)"),
        loc("454310", "fuel dealers (2017)"), loc("454390", "other direct selling (2017)"),
        fixed("445132", "vending machine operators (NAICS 2022)", "Retail", "2026-09-29",
                "NAICS 2022 moved vending-machine operators from 454210 into 445132, inside the "
                "Retail prefix; 454 excludes the 2017 code only. Los Angeles 52, San Francisco 29 "
                "rows in the raw files."),
        fixed("457210", "fuel dealers (NAICS 2022)", "Retail", "2026-09-29",
                "NAICS 2022 moved fuel dealers from 454310 into 457210, inside the Retail prefix. "
                "San Francisco 15, Los Angeles 1 rows in the raw files.")],
    "parking": [loc("812930", "parking lots and garages")],
    "repair": [loc("811210", "electronic equipment repair"), loc("811412", "appliance repair"),
               loc("811490", "other personal goods repair (shoes, alterations)")],
    "lodging": [loc("721110", "hotels and motels"), loc("721191", "bed-and-breakfast inns")],
    "recreation": [loc("713940", "fitness centres"), loc("713120", "amusement arcades"),
                   loc("512131", "cinemas")],
    "pharmacy": [loc("446110", "pharmacies (2017)"), loc("456110", "pharmacies (2022)")],
    "optician": [loc("446130", "optical goods stores (2017)"), loc("456130", "optical goods (2022)")],
    "health_food": [loc("446191", "food (health) supplement stores (2017)"),
                    loc("456191", "food (health) supplement retailers (2022)")],
    "health_food_nonstore": [loc("454390", "other direct selling (health-food MLM sellers)")],
    "mobile_unit": [
        loc("722330", "mobile food services"), loc("72233", "mobile food, San Diego's five digits"),
        loc("454210", "vending machine operators (2017)"),
        outside("pipeline/san_diego/config.py", '"81295"', "San Diego's ecoATM kiosks")],
}

# Montréal is naics.py with its caterers kept; the rest of the column is naics'.
COLUMNS["naics_montreal"] = {
    **COLUMNS["naics"],
    "no_counter_food": [
        loc("722310", "food service contractors"), loc("722330", "mobile food"),
        exception("722320", "caterers", "Food service", FOLLOWUPS,
                  "Montréal's street survey records traiteur shops with a counter, as France's "
                  "56.21Z (follow-up 2)")],
}

COLUMNS["scian"] = {
    "funeral": [loc("812310", "servicios funerarios"), loc("812321", "cementerios privados"),
                loc("812322", "cementerios públicos")],
    "no_counter_food": [loc("722310", "comedor para empresas e instituciones"),
                        loc("722320", "alimentos para ocasiones especiales")],
    "personal_catchall": [loc("812990", "otros servicios personales"),
                          loc("812130", "sanitarios públicos y bolerías")],
    "adult_hostess": absent("no code names adult venues: cabarets file with discos under 722411 "
                            "centros nocturnos"),
    "sex_shop": absent("no code of its own"),
    "massage_commercial": absent("SCIAN has no massage code; parlours file under 812110 salons"),
    "massage_regulated": absent("no massage-therapy code"),
    "car_dealer": [loc("468111", "automóviles y camionetas nuevos"),
                   loc("468112", "automóviles y camionetas usados"),
                   loc("468311", "motocicletas")],
    "petrol_station": [loc("468411", "gasolina y diesel")],
    "vehicle_repair": [loc("811111", "reparación mecánica de automóviles"),
                       loc("811121", "hojalatería y pintura")],
    "gambling": [loc("713291", "billetes de lotería y pronósticos deportivos"),
                 loc("713299", "otros juegos de azar")],
    "pawnbroker": [fixed("522452", "casas de empeño", None, "2026-09-29",
                           "DENUE names pawnshops with a code of their own, in credit (5224), so "
                           "SCIAN's 46 prefix never reaches them: 381 in Mexico City's file. The rule "
                           "keeps pawnbrokers; only New York and Chicago are declared exceptions.")],
    "nightclub": [loc("722411", "centros nocturnos, discotecas y similares"),
                  loc("722412", "bares, cantinas y similares")],
    "vet": [loc("541941", "servicios veterinarios para mascotas (privado)")],
    "nonstore": [loc("469110", "comercio exclusivamente por internet y catálogos")],
    "parking": [loc("812410", "estacionamientos")],
    "repair": [loc("811430", "reparación de calzado"), loc("811492", "reparación de motocicletas")],
    "lodging": [loc("721111", "hoteles con otros servicios")],
    "recreation": absent("no recreation code is keyed; 71 is not a bucket prefix"),
    "pharmacy": [loc("464111", "farmacias sin minisúper"), loc("464112", "farmacias con minisúper")],
    "optician": [loc("464121", "comercio al por menor de lentes")],
    "health_food": [loc("464113", "productos naturistas y complementos alimenticios")],
    "mobile_unit": [loc("722330", "alimentos en unidades móviles")],
}

LBL = "Limited Business License"
COLUMNS["chicago_license"] = {
    "funeral": absent("no funeral licence type; about 63 funeral-named pins sit under general "
                      "licences and stay, disclosed (owner)"),
    "no_counter_food": [loc("Shared Kitchen User (Long Term)", "shared kitchens and caterers")],
    "personal_catchall": [loc({"license_description": LBL,
                               "business_activity": "Miscellaneous Personal Services"},
                              "the catch-all activity on its own")],
    "tattoo": [loc({"license_description": LBL, "business_activity": "Tattoo and Body Piercing"},
                   "tattoo activity")],
    "adult_hostess": absent("no licence type or activity names adult venues"),
    "sex_shop": absent("no type of its own; a sex shop is a retail-sales activity"),
    "massage_commercial": [loc({"license_description": LBL, "business_activity": "Massage Services"},
                               "massage activity")],
    "massage_regulated": absent("Illinois licenses massage therapists at state level"),
    "car_dealer": [loc({"license_description": LBL,
                        "business_activity": "Sales / Rental / Lease of Motorized Vehicles"},
                       "vehicle sales activity")],
    "petrol_station": [loc("FILLING STATION", "filling station")],
    "vehicle_repair": [loc("Motor Vehicle Services License", "motor vehicle services")],
    "gambling": absent("gambling is licensed by the state; no betting or lottery type"),
    "pawnbroker": [exception("PAWNBROKER", "pawnbroker", None, R1,
                             "R5: pawnbrokers kept, with New York and Chicago the disclosed exceptions")],
    "nightclub": [loc("TAVERN", "tavern (bars and nightclubs)")],
    "vet": [loc({"license_description": "ANIMAL CARE LICENSE", "business_activity": "Veterinary Hospital"},
                "veterinary hospital")],
    "nonstore": [loc({"license_description": LBL,
                      "business_activity": "Retail Sales of General Merchandise (Home Based Business)"},
                     "home-based retail")],
    "parking": [loc("Public Garage", "commercial garage")],
    "repair": [
        loc({"license_description": LBL, "business_activity": "Repair of Electronics"},
            "an unmatched repair activity"),
        fixed({"license_description": LBL, "business_activity": "Clothing Alterations"},
                "clothing alterations", "Personal services", "2026-09-29",
                "approved as a personal service before the build (2026-09-19); the repairs rule "
                "(NAICS 811, alterations included) came later, and the owner chose to align")],
    "lodging": [loc("Hotel", "hotel")],
    "recreation": [loc({"license_description": LBL, "business_activity": "Gym / Fitness Classes"},
                       "gyms and fitness classes")],
    "pharmacy": [loc({"license_description": LBL, "business_activity": "Retail Sales of Pharmaceuticals"},
                     "retail-sales activity")],
    "optician": [loc({"license_description": LBL, "business_activity": "Retail Sales of Optical Goods"},
                     "retail-sales activity")],
    "mobile_unit": [loc("Mobile Food License", "mobile food"), loc("Peddler, non-food", "peddler")],
}

COLUMNS["phl_licensetype"] = {
    "funeral": absent("no funeral licence type"),
    "no_counter_food": [loc("FOOD CATERER", "event caterer"), loc("CURB MARKET", "curb market stalls"),
                        loc("FOOD ESTAB, RETAIL NON-PERMANENT LOCATION (EVENT)", "event stalls")],
    "personal_catchall": absent("Philadelphia licenses no personal service at all"),
    "adult_hostess": absent("no adult-venue type"),
    "sex_shop": absent("no type of its own"),
    "massage_commercial": absent("no personal-services source; massage is not licensed here"),
    "massage_regulated": absent("no personal-services source"),
    "car_dealer": absent("no car-dealer type: 'Vendor - Motor Vehicle Sales' is food trucks",
                         ignore=("VENDOR - MOTOR VEHICLE SALES",)),
    "petrol_station": [exception("MOTOR VEHICLE REPAIR / FUEL DISPENSING", "repair and fuel merged",
                                 None, RULED,
                                 "one type merges auto repair (NAICS 811, out) with fuel dispensing "
                                 "(NAICS 457, kept), sampled mostly as repair shops, and goes whole, "
                                 "as Edmonton's merged type does")],
    "vehicle_repair": [loc("AUTO WRECKING / WASTE HANDLING", "auto wrecking"),
                       loc("TOW TRUCK", "tow truck")],
    "gambling": [loc("ANNUAL SMALL GAMES OF CHANCE", "small games of chance"), loc("BINGO", "bingo")],
    "pawnbroker": [loc("PAWN SHOP", "pawn shop")],
    "nightclub": [loc("FOOD PREPARING AND SERVING (30+ SEATS)", "bars and clubs hold the food licence")],
    "vet": absent("no veterinary type"),
    "nonstore": [loc("HONOR BOX", "vending boxes"), loc("HANDBILL DISTRIBUTION", "handbills")],
    "parking": [loc("PUBLIC GARAGE / PARKING LOT", "public garage or parking lot")],
    "repair": absent("no repair type other than vehicles (the merged vehicle type is under "
                     "petrol_station)", ignore=("MOTOR VEHICLE REPAIR / FUEL DISPENSING",)),
    "lodging": [loc("LIMITED LODGING OPERATOR", "short-let hosts")],
    "recreation": [loc("SPECIAL ASSEMBLY OCCUPANCY", "venues")],
    "pharmacy": [loc("FOOD ESTABLISHMENT, RETAIL PERM LOCATION (LARGE)", "chain pharmacies hold it")],
    "optician": absent("no general-retail type"),
    "mobile_unit": [loc("VENDOR - MOTOR VEHICLE SALES", "food trucks"),
                    loc("VENDOR - PUSHCART", "pushcart"), loc("VENDOR - SIDEWALK SALES", "sidewalk")],
}

COLUMNS["new_york"] = {
    "person_licence": [outside("pipeline/new_york/step2_clean_businesses.py",
                               "NYS_SALON_EXCLUDE_LICENSE_TYPES",
                               "area and barber chair renters dropped in step 2 by license type")],
    "funeral": absent("none of the four registries licenses funeral services"),
    "no_counter_food": absent("DOHMH membership is Food service whatever the cuisine; no caterer or "
                              "canteen type separates them"),
    "personal_catchall": absent("the salon registry licenses appearance enhancement and barbering only"),
    "adult_hostess": absent("no adult-venue type in any of the four"),
    "sex_shop": absent("no type of its own"),
    "massage_commercial": absent("no registry licenses massage premises with addresses"),
    "massage_regulated": absent("massage therapists are a state profession with no address export"),
    "car_dealer": [loc({"source": "dca", "business_category": "SECONDHAND DEALER - AUTO"},
                       "used-car dealer")],
    "petrol_station": absent("no fuel-retail type in any of the four"),
    "vehicle_repair": [loc({"source": "dca", "business_category": "TOW TRUCK COMPANY"}, "tow trucks")],
    "gambling": [loc({"source": "dca", "business_category": "BINGO GAME OPERATOR"}, "bingo"),
                 loc({"source": "dca", "business_category": "GAMES OF CHANCE - BELL JAR"}, "games of chance")],
    "pawnbroker": [exception({"source": "dca", "business_category": "PAWNBROKER"}, "pawnbroker", None, R1,
                             "R5: pawnbrokers kept, with New York and Chicago the disclosed exceptions")],
    "nightclub": [loc({"source": "dohmh", "business_category": "American"},
                      "a DOHMH food-service permit (bars and clubs serving food)")],
    "vet": absent("no veterinary source"),
    "nonstore": [loc({"source": "dca", "business_category": "THIRD PARTY FOOD DELIVERY SERVICE"},
                     "food delivery"),
                 loc({"source": "dca", "business_category": "HOME IMPROVEMENT CONTRACTOR"},
                     "works at the customer's door")],
    "parking": [loc({"source": "dca", "business_category": "GARAGE & PARKING LOT"}, "garage and parking")],
    "repair": [loc({"source": "dca", "business_category": "ELECTRONIC & HOME APPLIANCE SERVICE DEALER"},
                   "appliance repair")],
    "lodging": [loc({"source": "dca", "business_category": "HOTEL"}, "hotel")],
    "recreation": [loc({"source": "dca", "business_category": "TICKET SELLER BUSINESS"}, "event ticketing")],
    "pharmacy": [loc({"source": "nys_store", "business_category": "Retail food store"},
                     "an NYS retail food store (chain pharmacies hold one)")],
    "optician": absent("no general-retail source"),
    "mobile_unit": [outside("pipeline/new_york/step2_clean_businesses.py", "Premises",
                            "DCA's Individual licences (general vendors) dropped before classify()")],
}

COLUMNS["vancouver"] = {
    "funeral": [loc({"source": "surrey", "category": "Funeral Parlour"}, "Surrey funeral parlour"),
                loc({"source": "surrey", "category": "Cemetery"}, "Surrey cemetery")],
    "no_counter_food": [loc({"source": "vancouver", "category": "Caterer"}, "Vancouver caterer"),
                        loc({"source": "surrey", "category": "Caterer"}, "Surrey caterer"),
                        loc({"source": "surrey", "category": "Concession Stand"}, "Surrey concession stand"),
                        loc({"source": "surrey", "category": "Flea Market"}, "Surrey flea market")],
    "personal_catchall": [loc({"source": "surrey", "category": "Party/Wedding Consultant"},
                              "Surrey party and wedding consultant"),
                          loc({"source": "surrey", "category": "Miscellaneous"}, "Surrey catch-all")],
    "tattoo": [loc({"source": "surrey", "category": "Tattoo Parlour"}, "Surrey tattoo parlour")],
    "adult_hostess": [loc({"source": "vancouver", "category": "Adult Services"}, "Vancouver adult services")],
    "sex_shop": [loc({"source": "surrey", "category": "Adult Entertainment Store"}, "Surrey sex shop")],
    "massage_commercial": [
        loc({"source": "vancouver", "category": "Health Enhancement Services"}, "Vancouver body care"),
        loc({"source": "surrey", "category": "Shiatsu Massage"}, "Surrey shiatsu"),
        loc({"source": "surrey", "category": "Reflexology"}, "Surrey reflexology")],
    "massage_regulated": [loc({"source": "surrey", "category": "Massage Therapy (RMT)"}, "Surrey RMT"),
                          loc({"source": "vancouver", "category": "Health Care Professionals and Services"},
                              "Vancouver health professions (RMTs)")],
    "car_dealer": [loc({"source": "surrey", "category": "Automobile Dealer/Rebuilder"}, "Surrey dealer")],
    "petrol_station": [loc({"source": "vancouver", "category": "Gas Station"}, "Vancouver gas station"),
                       loc({"source": "surrey", "category": "Gas Station"}, "Surrey gas station")],
    "vehicle_repair": [
        loc({"source": "vancouver", "category": "Vehicle Repair Detailing and Washing Services"},
            "Vancouver vehicle repair"),
        loc({"source": "surrey", "category": "Automotive Repair Service"}, "Surrey auto repair"),
        loc({"source": "surrey", "category": "Auto Body/Painting"}, "Surrey auto body")],
    "gambling": [loc({"source": "vancouver", "category": "Bingo Hall / Casino / Horse Racing"},
                     "Vancouver bingo and casino"),
                 loc({"source": "surrey", "category": "Casino"}, "Surrey casino"),
                 loc({"source": "surrey", "category": "Arcade"}, "Surrey arcade")],
    "pawnbroker": [loc({"source": "surrey", "category": "Pawn Broker"}, "Surrey pawnbroker")],
    "nightclub": [loc({"source": "vancouver", "category": "Liquor Establishment"},
                      "Vancouver liquor establishment (nightclubs)")],
    "vet": [loc({"source": "surrey", "category": "Professional Practitioner-Veterinarian"}, "Surrey vet")],
    "nonstore": [loc({"source": "surrey", "category": "Mail Order"}, "Surrey mail order"),
                 loc({"source": "surrey", "category": "Petroleum Product Distributor"}, "Surrey fuel dealer"),
                 loc({"source": "vancouver", "category": "Oil Gas and Other Fuels"}, "Vancouver fuel dealer"),
                 outside("pipeline/vancouver/config.py", "SURREY_LICENSE_TYPE_KEEP",
                         "Surrey's Home Occupation rows dropped before classify()")],
    "parking": [loc({"source": "vancouver", "category": "Parking Area / Garage"}, "Vancouver parking"),
                loc({"source": "surrey", "category": "Parking Lot"}, "Surrey parking lot")],
    "repair": [loc({"source": "vancouver", "category": "General Repair and Maintenance"}, "Vancouver repair"),
               loc({"source": "surrey", "category": "Repair Service"}, "Surrey repair"),
               loc({"source": "surrey", "category": "Tailor"}, "Surrey tailor (alterations)")],
    "lodging": [loc({"source": "vancouver", "category": "Hotel or Motel"}, "Vancouver hotel"),
                loc({"source": "surrey", "category": "Bed & Breakfast"}, "Surrey B&B"),
                loc({"source": "surrey", "category": "Short-Term Rentals"}, "Surrey short-term rentals")],
    "recreation": [loc({"source": "vancouver", "category": "Fitness Centre"}, "Vancouver fitness"),
                   loc({"source": "vancouver", "category": "Theatre"}, "Vancouver theatre"),
                   loc({"source": "surrey", "category": "Bowling Alley"}, "Surrey bowling")],
    "pharmacy": [loc({"source": "vancouver", "category": "Pharmacy"}, "Vancouver pharmacy")],
    "optician": absent("neither source has an optical-shop type; Surrey's Optometrist is a practitioner"),
    "mobile_unit": [loc({"source": "vancouver", "category": "Street Vendor"}, "Vancouver street vendor"),
                    loc({"source": "surrey", "category": "Portable Food Vendor"}, "Surrey food vendor"),
                    loc({"source": "surrey", "category": "Catering/Coffee Truck"}, "Surrey coffee truck"),
                    loc({"source": "surrey", "category": "Vending Machine"}, "Surrey vending machine"),
                    loc({"source": "surrey", "category": "Pedlar"}, "Surrey pedlar")],
}

COLUMNS["calgary_licencetype"] = {
    "person_licence": [loc("PERSONAL SERVICE (INDEPENDENT CHAIR OPERATOR)", "independent chair operator")],
    "funeral": absent("no funeral, crematorium or cemetery type among its licence types"),
    "no_counter_food": [loc("MARKET", "market of stalls"),
                        loc("FOOD SERVICE - NO PREMISES", "food service with no premises")],
    "personal_catchall": [loc("PSYCHIC PRACTITIONER", "psychic practitioner")],
    "tattoo": [loc("PERSONAL SERVICE (TATTOO)", "tattoo")],
    "adult_hostess": [loc("BODY RUB CENTRE", "body rub centre"),
                      loc("EXOTIC ENTERTAINMENT AGENCY", "exotic entertainment agency"),
                      loc("DATING SERVICE OR ESCORT SERVICE", "escort service")],
    "sex_shop": absent("no type of its own; under RETAIL DEALER - PREMISES"),
    "massage_commercial": [loc("MASSAGE CENTRE (COMMERCIAL)", "commercial massage centre")],
    "massage_regulated": absent("massage therapy is not regulated in Alberta"),
    "car_dealer": [loc("MOTOR VEHICLE DEALER - PREMISES", "motor vehicle dealer")],
    "petrol_station": [loc("FUEL SALES/STORAGE", "fuel sales")],
    "vehicle_repair": [loc("MOTOR VEHICLE REPAIR AND SERVICE (1)", "vehicle repair"),
                       loc("AUTO BODY SHOP", "auto body")],
    "gambling": [loc("AMUSEMENT ARCADE", "amusement arcade")],
    "pawnbroker": [loc("PAWNBROKER", "pawnbroker"), loc("PAWNBROKER (GRANDFATHERED)", "pawnbroker")],
    "nightclub": absent("no nightclub type: drinking places hold FOOD SERVICE - PREMISES"),
    "vet": absent("no veterinary type"),
    "nonstore": [loc("RETAIL DEALER - PREMISES (MAIL ORDER)", "mail order"),
                 loc("RETAIL DEALER - NO PREMISES", "retail with no premises"),
                 loc("DISTRIBUTION MANAGER (DIRECT SALES)", "direct sales")],
    "parking": absent("no parking type"),
    "repair": [loc("FURNITURE REFINISHING", "furniture refinishing")],
    "lodging": [loc("HOTEL/MOTEL", "hotel"), loc("LODGING HOUSE", "lodging house")],
    "recreation": [loc("PERSONAL SERVICE (FITNESS CONDITIONING)", "fitness"), loc("CINEMA", "cinema")],
    "pharmacy": absent("no pharmacy type; under RETAIL DEALER - PREMISES"),
    "optician": absent("no optician type"),
    "health_food_nonstore": [loc("DISTRIBUTION MANAGER (FOOD PRODUCTS) (DIRECT SALES)",
                                 "food-products direct sales")],
    "mobile_unit": [loc("FULL SERVICE FOOD VEHICLE", "food truck"), loc("PERSONAL SERVICE (MOBILE)", "mobile")],
}

COLUMNS["edmonton_licencecategory"] = {
    "person_licence": [loc("Health Enhancement Practitioner (Accredited)", "accredited practitioner (a person)"),
                       outside("pipeline/edmonton/config.py", "LICENCE_TYPE_KEEP",
                               "'Massage Practitioner' licences (a person) dropped before classify()")],
    "funeral": [loc("Funeral, Cremation, and Cemetery Service", "funeral, cremation and cemetery")],
    "no_counter_food": [loc("Food Processing / Catering Service", "catering (merged with processing)"),
                        loc("Public Market Vendor", "market stall vendor"),
                        loc("Farmers' Market", "farmers' market")],
    "personal_catchall": absent("no 812990-style category; the register-wide 'General Business' "
                                "is out anyway"),
    "adult_hostess": [loc("Body Rub Centre", "body rub centre"), loc("Adult Service", "adult service"),
                      loc("Erotic Entertainment Venue", "erotic entertainment venue")],
    "sex_shop": absent("no type of its own; under Retail Sales"),
    "massage_commercial": [loc("Health Enhancement Centre (Accredited)", "accredited massage centre")],
    "massage_regulated": [loc("Health Enhancement Centre", "physio and chiropractic (NAICS 621)"),
                          outside("pipeline/edmonton/config.py", "LICENCE_TYPE_KEEP",
                                  "'Massage Practitioner' licences (a person) dropped before classify()")],
    "car_dealer": [loc("Vehicle Sales and Rental", "vehicle sales")],
    "petrol_station": [exception("Vehicle Wash / Fueling Station", "car wash and fuel merged", None,
                                 "Edmonton built: 30 stations, not 33",
                                 "sampled as car washes (40 alone) against about three fuel sites; "
                                 "248 of 336 co-hold a convenience-store Retail licence")],
    "vehicle_repair": [loc("Vehicle Repair, Maintenance, and Modification", "vehicle repair")],
    "gambling": [loc("Bingo / Casino", "bingo and casino"), loc("Amusement Establishment", "amusements")],
    "pawnbroker": [loc("Pawnbroker", "pawnbroker")],
    "nightclub": [loc("After Hours Dance Club", "after-hours dance club"),
                  loc("Alcohol Sales (Consumption On-Premises / Minors Prohibited)", "drinking places")],
    "vet": absent("no veterinary category"),
    "nonstore": [loc("Travelling or Temporary Sales", "travelling sales")],
    "parking": [loc("General Business", "the catch-all, sampled as parking operators")],
    "repair": [loc("Light Duty Repair Service", "light-duty repair")],
    "lodging": [loc("Hotel / Motel", "hotel"),
                loc("Residential Rental Accommodation (Short-Term)", "short-term rental")],
    "recreation": [loc("Participant Recreation Service", "fitness"), loc("Spectator Entertainment", "venues")],
    "pharmacy": absent("no pharmacy category; under Retail Sales"),
    "optician": absent("no optician category"),
    "mobile_unit": [loc("Food Truck / Food Cart", "food truck")],
}

COLUMNS["toronto_mlscategory"] = {
    "funeral": absent("funeral services are provincially regulated, not in this register"),
    "no_counter_food": [loc("SIDEWALK VENDING", "sidewalk vending"), loc("CURBLANE VENDING", "curb-lane vending")],
    "personal_catchall": absent("no 812990-style category"),
    "adult_hostess": [loc("BODY RUB PARLOUR", "body rub parlour"),
                      loc("ADULT ENTERTAINMENT CLUB", "adult entertainment club"),
                      loc("BATH HOUSE", "bath house")],
    "sex_shop": absent("no general-retail licence"),
    "massage_commercial": [loc("HOLISTIC CENTRE", "holistic centre")],
    "massage_regulated": absent("RMTs are licensed by the Ontario College, not here"),
    "car_dealer": absent("no vehicle-dealer licence"),
    "petrol_station": absent("no fuel-retail licence; its one AUTO SERVICE STATION is filed as repair",
                             ignore=("AUTO SERVICE STATION",)),
    "vehicle_repair": [loc("PUBLIC GARAGE", "public garage")],
    "gambling": [loc("AMUSEMENT ESTABLISHMENT", "amusement establishment")],
    "pawnbroker": [loc("PAWN SHOP", "pawn shop")],
    "nightclub": [loc("ENTERTAINMENT ESTABLISHMENT/NIGHTCLUB", "nightclub")],
    "vet": absent("no veterinary licence"),
    "nonstore": [loc("TRANSIENT TRADER", "transient trader"),
                 loc("COLLECTOR OF SECOND HAND GOODS", "collector, no shop")],
    "parking": [loc("COMMERCIAL PARKING LOT", "commercial parking")],
    "repair": absent("no repair licence: CHIMNEY REPAIRMAN is a building trade",
                     ignore=("CHIMNEY REPAIRMAN",)),
    "lodging": [loc("SHORT TERM RENTAL COMPANY", "short-term rentals")],
    "recreation": [loc("BILLIARD HALL", "billiards"), loc("BOWLING HOUSE", "bowling"), loc("THEATRE", "theatre")],
    "pharmacy": absent("pharmacies are provincially licensed; no general-retail licence"),
    "optician": absent("no general-retail licence"),
    "mobile_unit": [loc("MOBILE VENDING (FOOD TRUCK)", "food truck"),
                    loc("HAWKER/PEDLAR WITH PUSH CART", "pedlar")],
}


COLUMNS["dc_businessactivity"] = {
    "person_licence": [pending("Beauty Booth", "a chair rented inside a salon (6)", "Personal services",
                               "2026-10-02", "kept as Personal services; the rule takes a renter's "
                               "own license out (San Francisco, New York, Calgary, Edmonton)")],
    "funeral": [loc("Funeral Establishment", "funeral establishment")],
    "no_counter_food": [loc("Caterers", "caterers"), loc("School Cafeteria", "school cafeteria"),
                        loc("Farmer's Market Manager License", "farmers' market")],
    "personal_catchall": [loc("General Business", "the office and professional catch-all")],
    "adult_hostess": absent("no adult, cabaret or hostess type among its values"),
    "sex_shop": absent("no type of its own"),
    "massage_commercial": [loc("Massage Establishment", "massage establishment")],
    "massage_regulated": absent("no therapist licence; only the establishment"),
    "car_dealer": [loc("Motor Vehicle Dealer", "motor vehicle dealer"), loc("Used Car Lot", "used car lot")],
    "petrol_station": [loc("Gasoline Dealer", "gasoline dealer")],
    "vehicle_repair": [loc("Consumer Goods (Auto Repair)", "auto repair"), loc("Auto Wash", "car wash")],
    "gambling": absent("no betting, lottery, casino or bingo type"),
    "pawnbroker": [fixed("Pawnbroker", "pawnbroker", None, "2026-09-29",
                           "left out as 'NAICS 522299 lending, as in the NAICS cities'; the rule keeps "
                           "pawnbrokers and names only New York and Chicago as exceptions")],
    "nightclub": absent("no nightclub type: nightlife is alcohol-licensed outside this register"),
    "vet": absent("no veterinary type"),
    "nonstore": [loc("Food Vending Machine", "vending machine"), loc("Solicitor", "door-to-door")],
    "parking": [loc("Parking Facility", "parking facility"), loc("Valet Parking", "valet parking")],
    "repair": absent("no repair type other than vehicles (auto repair is under vehicle_repair)",
                     ignore=("Consumer Goods (Auto Repair)", "auto repair, NAICS 811 not 812 (78)")),
    "lodging": [loc("Hotel", "hotel"), loc("Inn and Motel", "inn and motel"),
                loc("Bed and Breakfast", "bed and breakfast"),
                outside("pipeline/washington_dc/config.py", "BUSINESS_RENTAL_ACTIVITIES",
                        "short-term and vacation rentals left out at download")],
    "recreation": [loc("Health Spa", "D.C.'s gym licence"), loc("Movie Theater", "cinema"),
                   loc("Bowling Alley", "bowling")],
    "pharmacy": [loc("Patent Medicine", "over-the-counter drug endorsement (pharmacies)")],
    "optician": absent("no optician type"),
    "mobile_unit": [loc("Street Vending Business", "street vending"),
                    loc("Mobile Delicatessen", "mobile deli")],
}

COLUMNS["miami_catgryname"] = {
    "funeral": [loc("FUNERAL HOME", "funeral home"), loc("CEMETERY / CREMATORIES, ETC.", "cemetery")],
    "no_counter_food": [loc("CATERING BUSINESS", "caterer"), loc("FLEA MARKET", "flea market"),
                        loc("FARMERS MARKET", "farmers market")],
    "personal_catchall": [loc("FORTUNETELLER", "fortune teller"), loc("HALL FOR HIRE", "hall for hire")],
    "tattoo": [loc("TATTOO STUDIO", "tattoo studio")],
    "adult_hostess": [loc("DATING / ESCORT BUSINESS", "dating and escort business")],
    "sex_shop": absent("no type of its own; under RETAIL SALES"),
    "massage_commercial": [loc("MASSAGE ESTABLISHMENT", "massage establishment")],
    "massage_regulated": absent("one massage type only, the establishment"),
    "car_dealer": [loc("AUTO / TRUCK / VAN SALES", "car dealers")],
    "petrol_station": absent("no gas-station type: stations hold RETAIL SALES. LPG TANK EXCHANGE / "
                             "REFILL is a tank cage at another shop, left out as a fuel trade",
                             ignore=("LPG TANK EXCHANGE / REFILL",)),
    "vehicle_repair": [loc("AUTO / TRUCK / VAN SERVICE", "auto service"),
                       loc("BODY / PAINT / REPAIR SHOP", "body shop")],
    "gambling": [loc("PARI-MUTUEL WAGERING", "pari-mutuel wagering"), loc("BINGO OPERATOR", "bingo"),
                 loc("SERVICE / AMUSEMENT MACHINE", "coin amusement machines")],
    "pawnbroker": [loc("PAWNBROKER", "pawnbroker")],
    "nightclub": [loc("NIGHT CLUB", "night club"), loc("DANCING OR ENTERTAINMENT", "dancing licence")],
    "vet": [loc("VETERINARY CLINIC", "veterinary clinic")],
    "nonstore": [loc("VENDING MACHINE", "vending machine"), loc("TELEMARKETING", "telemarketing"),
                 loc("LPG DEALER / MFG", "LPG dealer")],
    "parking": [loc("PARKING FACILITY", "parking facility")],
    # CLEANER/LAUNDRY/ALTERATIONS is a dry-cleaning type that alterations ride with: not located here.
    "repair": [loc("SERVICE BUSINESS", "service catch-all, trade repair"),
               loc("LOCKSMITH SERVICE", "locksmith")],
    "lodging": [loc("HOTEL/MOTEL/ BOARDING HOUSE", "hotel"), loc("TIME SHARE PROPERTY", "timeshare")],
    "recreation": [loc("FITNESS CENTER (MEMBERSHIP)", "gym"), loc("MOVIE / MULTI THEATRE", "cinema")],
    "pharmacy": [loc("PHARMACY", "pharmacy")],
    "optician": absent("no optician type"),
    "mobile_unit": [loc("LUNCH WAGON / TRUCK", "food truck"), loc("ICE CREAM VENDOR", "ice-cream vendor"),
                    loc("PEDDLER", "peddler")],
}

COLUMNS["boston_licensecat"] = {
    "funeral": absent("food, alcohol and cannabis registers only"),
    "no_counter_food": absent("the food permit types are FS, FT, RF and MFW; no caterer or canteen type"),
    "personal_catchall": [loc({"source": "licensing_board", "business_category": "Fortune Teller"},
                              "fortune teller")],
    "adult_hostess": absent("no adult or cabaret type in any source"),
    "sex_shop": absent("no general-retail source"),
    "massage_commercial": absent("no personal-services source: Massachusetts licenses at state level"),
    "massage_regulated": absent("no personal-services source"),
    "car_dealer": absent("no general-retail source"),
    "petrol_station": absent("no general-retail source"),
    "vehicle_repair": absent("not in these registers"),
    "gambling": absent("no betting, lottery or casino type"),
    "pawnbroker": absent("no general-retail source"),
    "nightclub": [loc({"source": "isd_food", "business_category": "FS"},
                      "eating and drinking permit, where a club with food lands"),
                  exception({"source": "licensing_board", "business_category": "GOP All Alc."},
                            "General On Premise all-alcohol licence (bars and clubs)", None,
                            "Four continuity departures kept out and disclosed",
                            "kept out, disclosed: of 17 licensees 10 are on the map through an ISD "
                            "food permit; the 7 left are 1 bar (The Spud Bar), theatres, a college "
                            "and institutions, so the licence type would add mostly non-bars")],
    "vet": absent("not in these registers"),
    "nonstore": [loc({"source": "cannabis", "business_category": "Delivery (operator)"}, "delivery")],
    "parking": absent("not in these registers"),
    "repair": absent("not in these registers"),
    "lodging": [loc({"source": "licensing_board", "business_category": "Innholder No Liquor"}, "innholder")],
    "recreation": [loc({"source": "licensing_board", "business_category": "Bowling Alley"}, "bowling")],
    "pharmacy": [loc({"source": "licensing_board", "business_category": "Druggist"}, "druggist licence")],
    "optician": absent("no general-retail source"),
    "mobile_unit": [loc({"source": "isd_food", "business_category": "MFW"}, "mobile food walk-on")],
}


def _buf(descript, source="city"):
    return {"source": source, "business_category": descript}


# Buffalo: the City's 46 licence codes (read from the portal 2026-09-29) and
# two State registers, NYS retail food stores (every row Retail) and NYS salon
# business licences (every row Personal services).
COLUMNS["buffalo"] = {
    "funeral": absent("no funeral type among the City's 46 licence codes; the State registers are "
                      "food stores and salons"),
    "no_counter_food": [loc(_buf("Caterer"), "caterer"), loc(_buf("Flea Market"), "flea market")],
    "personal_catchall": absent("no personal-services catch-all: the City's codes are regulated "
                                "activities, and the State's salon register is one trade"),
    "adult_hostess": [loc(_buf("Go-Go Dancers"), "go-go dancers")],
    "sex_shop": absent("no type of its own"),
    "massage_commercial": absent("no massage type: New York licenses massage at state level, in no "
                                 "register used here"),
    "massage_regulated": absent("no massage type in these registers"),
    "car_dealer": [loc(_buf("Used Car Dealer"), "used car dealer")],
    "petrol_station": [
        loc(_buf("GAS & GO EXPRESS", "nys_store"),
            "a station with a shop holds a State food-store licence (44 such names, Joe's Kwik Marts)"),
        exception(_buf("Cert. Operation Fuel Device"), "certificate of operation for a fuel device (1,182)",
                  None, "Four continuity departures kept out and disclosed",
                  "closed: not a pump register. The holders are apartments, churches, colleges and "
                  "factories (fuel-burning equipment); the only petrol retailers among them, three "
                  "7-Elevens, are already mapped through the State food-store licence")],
    "vehicle_repair": absent("no repair or car-wash code; Tire Handler is a scrap-tire permit"),
    "gambling": absent("no betting, lottery, bingo or casino code; Coin-controlled Amusements are "
                       "arcade machines (recreation)"),
    "pawnbroker": [loc(_buf("Pawnbroker"), "pawnbroker")],
    "nightclub": [
        loc(_buf("Restaurant / Dance"), "restaurant licensed for dancing"),
        exception(_buf("Dance Hall"), "dance hall (24)", None, "Four continuity departures kept out and disclosed",
                  "kept out, disclosed: of 7 current sites 3 are mapped and 4 are community or "
                  "banquet halls far from any station; 5 club-like licences near stations have "
                  "lapsed - re-check at Buffalo's next refresh")],
    "vet": absent("no veterinary code"),
    "nonstore": [loc(_buf("Vending Machine"), "vending machine")],
    "parking": [loc(_buf("Parking Lot"), "parking lot"),
                loc(_buf("Parking Garage Structure"), "parking garage")],
    "repair": absent("no repair code"),
    "lodging": [loc(_buf("Lodging House"), "lodging house"),
                loc(_buf("Short Term Rental Dwelling"), "short-term rental")],
    "recreation": [loc(_buf("Amusement Shows"), "amusement shows"), loc(_buf("Arcade"), "arcade"),
                   loc(_buf("Bowling Alley"), "bowling"), loc(_buf("Billiard Parlor"), "billiards"),
                   loc(_buf("Skating Rink"), "skating rink")],
    "pharmacy": [loc(_buf("CVS PHARMACY", "nys_store"),
                     "drugstore chains holding a State food-store licence (CVS, Rite Aid: 17)")],
    "optician": absent("no optician type"),
    "mobile_unit": [loc(_buf("Stationary Peddler"), "peddler at a fixed spot")],
}

# Sacramento: the City's Business_Description, 148 values (read 2026-09-29).
COLUMNS["sacramento"] = {
    "person_licence": [loc("BEAUTY - INDEPENDENT STYLIST", "independent stylist in another's shop"),
                       loc("MASSAGE - TECHNICIAN", "massage technician (a person)")],
    "funeral": [loc("FUNERAL HOME & CREMATORY", "funeral home"),
                loc("PET CREMATION SERVICES", "pet cremation")],
    "no_counter_food": [loc("CATERING", "caterer"), loc("COTTAGE FOOD OPERATION", "home kitchen"),
                        loc("SIDEWALK VENDOR - FOOD", "street food stall")],
    "personal_catchall": [loc("SERVICE - GENERAL", "the general service catch-all"),
                          loc("OTHER", "the whole-register catch-all")],
    "tattoo": [loc("TATTOO PARLOR/ARTIST", "tattoo parlour")],
    "adult_hostess": [loc("ADULT ENTERTAINMENT", "adult entertainment")],
    "sex_shop": absent("no type of its own; under RETAIL SALES - GENERAL"),
    "massage_commercial": [loc("MASSAGE - ESTABLISHMENT", "massage establishment")],
    # Confirmed by the owner (2026-09-30) as a PRIVACY exclusion, not as
    # regulated massage: California's certificate is not a health licence, but
    # each one names a person rather than a premises.
    "massage_regulated": [loc("MASSAGE - TECHNICIAN", "certified massage technician: a licence "
                                                      "naming a person, out for privacy (owner)")],
    "car_dealer": [loc("AUTOMOBILE DEALERS - NEW / USED", "car dealers"),
                   loc("AUTOMOBILE DEALERS - USED", "used car dealers")],
    "petrol_station": [loc("SERVICE STATIONS", "service stations")],
    "vehicle_repair": [loc("AUTOMOTIVE - REPAIR", "auto repair"),
                       loc("AUTOMOTIVE - WRECKING", "auto wrecking")],
    "gambling": [loc("CARDROOMS", "card rooms"), loc("AMUSEMENT - BINGO", "bingo")],
    "pawnbroker": [loc("PAWNBROKERS", "pawnbroker")],
    "nightclub": [
        loc("BARS - TAVERNS", "bars and taverns, where a club with a bar licence files"),
        exception("ENTERTAINMENT", "entertainment (41 current)", None, "Four continuity departures kept out and disclosed",
                  "kept out, disclosed: about 2 are clubs with a public floor (Channel 24, La "
                  "Kalle); 3 are adult venues (rule R3); the rest are DJs, bands, media and event "
                  "services")],
    "vet": [loc("VETERINARIANS", "veterinarians")],
    "nonstore": [loc("RETAIL SALES - ONLINE", "online retail"), loc("VENDING MACHINES", "vending")],
    "parking": [loc("PARKING LOTS/SERVICES", "parking")],
    "repair": [loc("SERVICE - REPAIRS", "repairs"), loc("ELECTRONICS & REPAIRS", "electronics repair"),
               loc("CLOTHING ALTERATIONS, &TAILORS SHOPS", "alterations")],
    "lodging": [loc("HOTELS & MOTELS", "hotels"), loc("SHORT-TERM RENTAL", "short-term rental")],
    "recreation": [loc("FITNESS/PERSONAL TRAINER", "fitness"), loc("THEATRES", "theatres"),
                   loc("AMUSEMENT - ARCADES", "arcades"), loc("AMUSEMENT - OTHER", "amusements")],
    "pharmacy": [loc("DRUGS STORES & PHARMACIES", "pharmacies")],
    "optician": absent("no optician type: OPTOMETRISTS are eye doctors' offices (NAICS 621320, "
                       "health care, out as in the NAICS cities); optical shops file under "
                       "RETAIL SALES - GENERAL; confirmed by the owner 2026-09-30"),
    "mobile_unit": [loc("MOBILE VENDOR - FOOD", "food truck"),
                    loc("MOBILE VENDOR - ICE CREAM", "ice-cream vendor"),
                    loc("SIDEWALK VENDOR - MERCHANDISE", "street merchandise stall")],
}

COLUMNS["nola_businesstype"] = {
    "funeral": [loc("Funeral Homes & Funeral Services", "funeral homes"),
                loc("Cemeteries & Crematories", "cemeteries and crematories")],
    "no_counter_food": [loc("Caterers", "caterers"), loc("Food Service Contractors", "food contractors"),
                        loc("Special Events-Jazz Fest (Vendor)", "festival food and craft vendors")],
    "personal_catchall": [loc("Personal Services, Other", "other personal services (812990)")],
    "adult_hostess": absent("no type of its own: no adult-entertainment or massage-parlour type "
                            "in the 486 values"),
    "sex_shop": absent("no type of its own; under the all-other store retailers"),
    "massage_commercial": [loc("Personal Care Services, Other", "other personal care (massage)")],
    "massage_regulated": [loc("Offices of Health Practitioners, All Other Miscellaneous",
                              "offices of other health practitioners")],
    "car_dealer": [loc("New Car Dealers", "new car dealers"), loc("Used Car Dealers", "used car dealers"),
                   loc("Motorcycle Dealers", "motorcycle dealers")],
    "petrol_station": [loc("Gasoline Stations with Convenience Stores", "gas stations with stores"),
                       loc("Gasoline Stations, Other", "other gas stations")],
    "vehicle_repair": [loc("General Automotive Repair", "general auto repair"),
                       loc("Automotive Body, Paint & Interior Repair & Maintenance", "auto body")],
    "gambling": [loc("Video Draw Poker Devices", "video-poker devices"),
                 loc("Casinos(except Hotel Casinos)", "casinos")],
    "pawnbroker": [loc("Pawnshops", "pawnshops, Retail by R5 though NAICS calls them lenders")],
    "nightclub": [loc("Drinking Places(Alcoholic Beverages)", "drinking places (clubs file here)")],
    "vet": [loc("Veterinary Services", "veterinary services")],
    "nonstore": [loc("Electronic Shopping & Mail-Order Houses", "online and mail order"),
                 loc("Direct Selling Establishments, Other", "direct sellers"),
                 loc("Vending Machine Operators", "vending")],
    "parking": [loc("Parking Lots & Garages", "parking")],
    "repair": [loc("Personal & Household Goods Repair & Maintenance, Other", "household goods repair"),
               loc("Appliance Repair & Maintenance", "appliance repair")],
    "lodging": [loc("Hotels(except Casino Hotels) & Motels", "hotels"),
                loc("Bed & Breakfast Inns", "bed and breakfasts"),
                loc("Short Term Rentals/Residential Properties", "short-term rentals")],
    "recreation": [loc("Fitness & Recreational Sports Centers", "fitness"), loc("Museums", "museums"),
                   loc("Motion Picture Theaters(except Drive-Ins)", "cinemas")],
    "pharmacy": [loc("Pharmacies & Drug Stores", "pharmacies")],
    "optician": [loc("Optical Goods Stores", "optical goods stores")],
    "health_food": [loc("Food(Health) Supplement Stores", "health-food stores")],
    "mobile_unit": [loc("Mobile Food Services", "food trucks"),
                    loc("Artist-Painting on Streets", "street artists"),
                    loc("Flea Market", "market stalls (R1: a market's stalls are not shops)")],
}


def _fi(source, t):
    return {"source": source, "tipologiaattivita": t}


COLUMNS["florence_attivita"] = {
    "funeral": absent("no layer for funeral services: the Comune publishes shops, food service, "
                      "beauty and laundries only"),
    "no_counter_food": [loc(_fi("pubblici_esercizi", "56.21.01R - CATERING"), "catering"),
                        loc(_fi("pubblici_esercizi", "56.10.01R - HOME RESTAURANT"), "home restaurant")],
    "personal_catchall": absent("no catch-all: the beauty layer lists hair, beauty, tattoo and piercing"),
    "tattoo": [loc(_fi("estetiche", "96.09.02 - TATUAGGI"), "tattoo")],
    "adult_hostess": absent("no such type in the four layers"),
    "sex_shop": absent("no type of its own; under the shop type (esercizio di vicinato)"),
    "massage_commercial": [loc(_fi("estetiche", "96.02.02R - ESTETISTI"),
                               "beauticians, whose trade includes aesthetic massage")],
    "massage_regulated": absent("health massage is not in the Comune's activity layers"),
    "car_dealer": absent("no type of its own; under the shop type"),
    "petrol_station": absent("fuel stations are licensed outside these four layers"),
    "vehicle_repair": absent("no repair layer"),
    "gambling": absent("no gaming layer"),
    "pawnbroker": absent("no type of its own"),
    "nightclub": [loc(_fi("pubblici_esercizi", "56.10.01R - SOMMINISTRAZIONE DI ALIMENTI E BEVANDE"),
                      "food and drink service (bars and clubs file here)")],
    "vet": absent("no veterinary layer"),
    "nonstore": [loc(_fi("commercio", "47.91.01R - FORMA SPECIALE (COMMERCIO ELETTRONICO)"), "online"),
                 loc(_fi("commercio", "47.99.02R - FORMA SPECIALE (DISTRIBUTORI AUTOMATICI)"), "vending"),
                 loc(_fi("commercio", "47.99.01R - FORMA SPECIALE (DOMICILIO DEL CONSUMATORE)"), "door to door")],
    "parking": absent("no parking layer"),
    "repair": absent("no repair layer"),
    "lodging": [loc(_fi("pubblici_esercizi", "56.10.01R - RISTORANTE ALBERGO"),
                    "restaurants inside hotels, out with lodging (premises-taxonomy step 5)")],
    "recreation": [loc(_fi("pubblici_esercizi", "56.20.01R - SOMMINISTRAZIONE IN IMPIANTI SPORTIVI COMUNALI"),
                       "bars in the Comune's sports grounds")],
    "pharmacy": absent("pharmacies are licensed outside these four layers"),
    "optician": absent("no type of its own; under the shop type"),
    "mobile_unit": [loc(_fi("pubblici_esercizi", "SOMMINISTRAZIONE TEMPORANEA - art. 52"),
                        "temporary service at events")],
}

SHOP = "RETAIL (SHOPS)"


def _dub(uses, category=SHOP):
    return {"Uses": uses, "Category": category}


COLUMNS["dublin_uses"] = {
    "funeral": [loc(_dub("-, FUNERAL HOME"), "funeral home"),
                loc(_dub("CEMETERY OR CREMATORIUM", "MISCELLANEOUS"), "cemetery"),
                exception(_dub("SHOP, FUNERAL HOME"), "funeral home beside a shop use", "Retail", R1,
                          "the owner accepted Dublin's six 'shop, funeral home' premises staying "
                          "Retail through their shop use")],
    "no_counter_food": [loc(_dub("-, MARKET"), "market"), loc(_dub("SHOP, MARKET"), "market in a shop unit")],
    "personal_catchall": absent("no 812990-style use; OTHER and MISCELLANEOUS are generic and out"),
    "tattoo": [loc(_dub("-, TATTOO PARLOUR"), "tattoo parlour")],
    "adult_hostess": absent("no adult-venue use; ADULT SHOP is the sex shop",
                            ignore=("ADULT SHOP", "-, ADULT SHOP")),
    "sex_shop": [loc(_dub("-, ADULT SHOP"), "adult shop")],
    "massage_commercial": [loc(_dub("-, BEAUTY SALON / MASSAGE"), "beauty salon and massage")],
    "massage_regulated": absent("no therapist use"),
    "car_dealer": [loc(_dub("-, MOTOR SHOWROOM"), "motor showroom")],
    "petrol_station": [loc(_dub("-, SERVICE STATION"), "service station"),
                       loc(_dub("-, MOTOR FUEL SALES"), "motor fuel sales"),
                       exception(_dub("-, SERVICE STATION (NO SHOP)"), "forecourt with no shop", None,
                                 RULED, "a forecourt with no shop has nothing to walk into")],
    "vehicle_repair": [loc(_dub("-, GARAGE"), "garage"), loc(_dub("-, MOTOR WASH"), "car wash")],
    "gambling": [loc(_dub("-, BETTING SHOP"), "betting shop"), loc(_dub("SHOP, BETTING SHOP"), "betting shop"),
                 loc(_dub("SHOP, CASINO"), "casino"), loc(_dub("-, BINGO HALL"), "bingo hall")],
    "pawnbroker": absent("no pawnbroker use"),
    "nightclub": [loc(_dub("-, NIGHT CLUB / DISCOTHEQUE"), "night club")],
    "vet": absent("no veterinary use"),
    "nonstore": absent("a valuation register lists rated premises only"),
    "parking": [loc(_dub("CAR PARK", "MISCELLANEOUS"), "car park")],
    "repair": [loc(_dub("-, REPAIRS"), "repairs"),
               fixed(_dub("-, SHOE REPAIR / KEY CUT"), "shoe repair and key cutting",
                       "Personal services", "2026-09-29",
                       "'Dublin's two departures' (shoe repair and key cutting, garment alterations), "
                       "which Buenos Aires followed; the owner chose to align with the repairs rule"),
               fixed(_dub("-, ALTERATIONS"), "alterations", "Personal services", "2026-09-29",
                       "as shoe repair"),
               fixed(_dub("-, TAILORING"), "tailoring", "Personal services", "2026-09-29",
                       "as shoe repair")],
    "lodging": [loc(_dub("HOTEL", "HOSPITALITY"), "hotel"), loc(_dub("-, GUESTHOUSE"), "guesthouse")],
    "recreation": [loc(_dub("-, GYMNASIUM / FITNESS CENTRE"), "gym"), loc(_dub("-, CINEMA"), "cinema"),
                   fixed(_dub("GYMNASIUM / FITNESS CENTRE, SHOP"), "gym beside a generic shop use",
                           "Retail", "2026-09-29",
                           "a generic SHOP segment rescues any use the override list does not name "
                           "(4 gyms and 1 snooker hall on the map); betting, casino, amusement, bingo "
                           "and market are named, recreation is not"),
                   fixed(_dub("INTERNET CAFE, -"), "internet cafe", "Food service", "2026-09-29",
                           "a PC room by another name (27 pins); the rule puts PC rooms in recreation, "
                           "and the module gives no reason")],
    "pharmacy": [loc(_dub("-, PHARMACY"), "pharmacy")],
    "optician": [loc(_dub("-, OPTICIAN"), "optician")],
    "health_food": [loc(_dub("-, HEALTH FOOD SHOP"), "health food shop")],
    "mobile_unit": [loc(_dub("-, RIGHT OF TRADING"), "right of trading"),
                    exception(_dub("-, KIOSK"), "kiosk", "Retail", FOLLOWUPS,
                              "Dublin's kiosks kept as small walk-in shops (follow-up 4)")],
}

BA_FILTER = "df[TAX.TYPE_COLUMN].isin(TAX.STOREFRONT_TYPE_VALUES)"
BA_STEP2 = "pipeline/buenos_aires/step2_clean_businesses.py"
COLUMNS["ba_usos_suelo"] = {
    "funeral": [loc("SEPELIOS", "funeral services"), loc("VELATORIO", "wake parlour"),
                loc("FUNERARIA", "funeral home")],
    "no_counter_food": [loc("SERVICIO DE CATTERING", "catering"),
                        outside(BA_STEP2, BA_FILTER, "markets (MULTICOMERCIAL) dropped before classify()")],
    "personal_catchall": [loc("TAROT", "tarot"), loc("ASTROLOGIA", "astrology"),
                          loc("SALON DE FIESTAS", "party hall")],
    "tattoo": [loc("TATUAJES", "tattoo")],
    "adult_hostess": [outside(BA_STEP2, BA_FILTER, "by-the-hour hotels (EQUIPAMIENTO) dropped before classify()")],
    "sex_shop": [loc("SEX SHOP", "sex shop")],
    "massage_commercial": [loc("MASAJES", "massage")],
    "massage_regulated": [loc("KINESIOLOGIA", "physiotherapy")],
    "car_dealer": [loc("CONCESIONARIA AUTOMOTORES", "car dealership"),
                   loc("MOTOS, REPUESTOS Y ACCESORIOS", "motorcycles")],
    "petrol_station": [loc("ESTACION DE SERVICIO", "service stations, their own survey type (266) "
                           "[fixed, approved 2026-09-29]"),
                       outside(BA_STEP2, "TAX.STATION_TYPE_VALUE",
                               "step 2 admits the station type and names its use for classify()")],
    "vehicle_repair": [loc("TALLER MECANICO DE AUTOMOTORES", "car workshop"), loc("LAVADERO DE AUTOS", "car wash")],
    "gambling": [loc("LOTERIA", "lottery agency"), loc("SALON DE JUEGOS RECREATIVOS", "arcade")],
    "pawnbroker": absent("no pawnbroker subtype"),
    "nightclub": [loc("DISCOTECA", "discotheque")],
    "vet": [loc("VETERINARIA (ATENCION)", "veterinary clinic")],
    "nonstore": [loc("CENTRO DE DISTRIBUCION Y RETIRO E-COMMERCE", "e-commerce pickup")],
    "parking": [loc("DEPOSITO AUTOMOTORES", "vehicle storage"),
                outside(BA_STEP2, BA_FILTER, "commercial garages (GARAGE COMERCIAL) dropped before classify()")],
    "repair": [loc("REPARACION CELULARES", "phone repair"),
               loc("REPARACION DE ELECTRODOMESTICOS", "appliance repair"),
               fixed("COMPOSTURA DE CALZADO", "shoe repair", "Personal services", "2026-09-29",
                       "Dublin's two departures, followed; the owner chose to align with the repairs rule"),
               fixed("ARREGLO DE ROPA", "clothing alterations", "Personal services", "2026-09-29",
                       "as shoe repair"),
               fixed("SASTRERIA", "tailor", "Personal services", "2026-09-29", "as shoe repair"),
               fixed("CERRAJERIA", "locksmith and key cutting", "Personal services", "2026-09-29",
                       "as Dublin's key cutting (owner, 2026-09-29)")],
    "lodging": [outside(BA_STEP2, BA_FILTER, "hotels (EQUIPAMIENTO) dropped before classify()")],
    "recreation": [loc("GIMNASIO", "gym"), loc("SALON DE BAILE", "dance hall")],
    "pharmacy": [loc("FARMACIA Y PERFUMERIA", "pharmacy")],
    "optician": [loc("OPTICA", "optician")],
    "health_food": [loc("DIETETICA", "health-food shop")],
    "mobile_unit": absent("the survey records fixed ground-floor uses only; KIOSCO is a fixed kiosk shop"),
}


def _br(text):
    return {"DSC_ESTABELECIMENTO": text}


BR_TRUCKS = ("Brazil's trucks and kiosks disclosed, not excluded: the census cannot tell a "
             "trailer parked for years from a mobile one (follow-up 8)")
COLUMNS["brazil_cnefe"] = {
    "funeral": [loc(_br("FUNERARIA"), "funeral home"), loc(_br("VELORIO MUNICIPAL"), "wake"),
                loc(_br("CREMATORIO"), "crematorium"), loc(_br("CEMITERIO"), "cemetery")],
    "funeral_goods": [loc(_br("ARTIGOS FUNERARIOS"), "funeral goods")],
    "no_counter_food": [
        loc(_br("BUFFET INFANTIL"), "party buffet"), loc(_br("EVENTOS"), "events"),
        loc(_br("REFEITORIO"), "refectory"), loc(_br("FEIRA"), "street market"),
        exception(_br("BARRACA DE PASTEL"), "pastry stall", "Food service", FOLLOWUPS, BR_TRUCKS),
        fixed(_br("CANTINA ESCOLAR"), "school canteen", "Food service", "2026-09-29",
                "the head noun CANTINA is a Food service word; the rule takes canteens out where "
                "the register names them. Not measured."),
        fixed(_br("RESTAURANTE INDUSTRIAL"), "staff canteen", "Food service", "2026-09-29",
                "an industrial restaurant is a staff canteen; RESTAURANTE wins as the head noun. "
                "Not measured.")],
    "personal_catchall": [loc(_br("SALAO DE FESTAS"), "party hall"), loc(_br("CARTOMANTE"), "card reader"),
                          loc(_br("AGENCIA DE CASAMENTO"), "marriage agency")],
    "tattoo": [loc(_br("TATUAGEM"), "tattoo"), loc(_br("STUDIO DE TATUAGEM"), "tattoo studio"),
               fixed(_br("ESTUDIO DE TATUAGEM"), "tattoo studio, Portuguese spelling", None, "2026-09-29",
                       "the civic rule's ESTUDIO has no tattoo lookahead, where STUDIO has one; "
                       "looks unintended. Not measured.")],
    "adult_hostess": [loc(_br("PRIVE"), "privé"), loc(_br("CASA NOTURNA"), "night house")],
    "sex_shop": [loc(_br("SEX SHOP"), "sex shop")],
    "massage_commercial": [loc(_br("MASSAGEM"), "massage"), loc(_br("CASA DE MASSAGEM"), "massage house")],
    "massage_regulated": [loc(_br("FISIOTERAPIA"), "physiotherapy"), loc(_br("MASSOTERAPIA"), "massage therapy")],
    "car_dealer": [loc(_br("CONCESSIONARIA"), "dealership"), loc(_br("COMERCIO DE VEICULOS"), "vehicle sales"),
                   loc(_br("LOJA DE MOTOS"), "motorcycle shop")],
    "petrol_station": [loc(_br("POSTO DE GASOLINA"), "petrol station"),
                       loc(_br("POSTO DE COMBUSTIVEL"), "fuel station"), loc(_br("POSTO SHELL"), "branded station")],
    "vehicle_repair": [loc(_br("OFICINA MECANICA"), "workshop"), loc(_br("FUNILARIA"), "body shop"),
                       loc(_br("LAVA JATO"), "car wash")],
    "gambling": [loc(_br("LOTERICA"), "lottery agency"), loc(_br("JOGO DO BICHO"), "jogo do bicho"),
                 loc(_br("CASA DE APOSTAS"), "betting house")],
    "pawnbroker": absent("pawn lending is Caixa Econômica Federal's monopoly; no pawnshop trade"),
    "nightclub": [fixed(_br("BOATE"), "nightclub", None, "2026-09-29",
                          "filed with CASA DE SHOW under public and civic, with no reason given; the "
                          "rule keeps nightclubs as Food service. Not measured.")],
    "vet": [loc(_br("CLINICA VETERINARIA"), "veterinary clinic")],
    "nonstore": [loc(_br("DISTRIBUIDORA DE GAS"), "bottled-gas dealer"), loc(_br("REVENDA DE GAS"), "gas reseller"),
                 fixed(_br("LOJA VIRTUAL"), "online shop", "Retail", "2026-09-29",
                         "the LOJA pattern takes it as a shop; an online shop is nonstore. Not measured.")],
    "parking": [loc(_br("ESTACIONAMENTO"), "car park")],
    "repair": [loc(_br("ASSISTENCIA TECNICA"), "repair service"), loc(_br("SAPATEIRO"), "cobbler"),
               loc(_br("COSTUREIRA"), "seamstress (alterations)")],
    "lodging": [loc(_br("HOTEL"), "hotel"), loc(_br("POUSADA"), "guest house")],
    "recreation": [loc(_br("ACADEMIA"), "gym"), loc(_br("LAN HOUSE"), "PC room"), loc(_br("CINEMA"), "cinema")],
    "pharmacy": [loc(_br("FARMACIA"), "pharmacy"), loc(_br("DROGARIA"), "drugstore")],
    "optician": [loc(_br("OTICA"), "optician")],
    "health_food": [loc(_br("LOJA DE PRODUTOS NATURAIS"), "health-food shop")],
    "mobile_unit": [loc(_br("AMBULANTE"), "street vendor"), loc(_br("CAMELO"), "street trader"),
                    exception(_br("TRAILER DE LANCHES"), "snack trailer", "Food service", FOLLOWUPS, BR_TRUCKS),
                    exception(_br("FOOD TRUCK"), "food truck", "Food service", FOLLOWUPS, BR_TRUCKS)],
}

JP_SEOUL = "Seoul's Step 0 completed: 17 registers"
COLUMNS["japan_eigyo"] = {
    "funeral": absent("food-hygiene and barber, beauty and laundry registers only"),
    "no_counter_food": [
        loc({"permit_type": "㉖ 集団給食施設"}, "institutional catering"),
        loc({"permit_type": "飲食店営業（仕出し）"}, "caterer (仕出し)"),
        loc({"permit_type": "飲食臨時"}, "temporary permit"),
        loc({"permit_type": "① 飲食店営業", "form": "社員食堂"}, "staff canteen (業態)"),
        exception({"permit_type": "① 飲食店営業", "form": "ろ店"}, "Fukuoka's yatai", "Food service",
                  "Fukuoka steps 1-2: the first two-source Japanese city",
                  "Fukuoka's yatai count: 81 fixed stalls under the city's yatai ordinance (owner)"),
        fixed({"permit_type": "① 飲食店営業", "form": "露店"}, "street stall (露店) as a 業態",
                "Food service", "2026-09-29",
                "the form rules' temporary words miss 露店, so a restaurant permit with that form "
                "stays Food service (about 34 rows across the MHLW, Fukuoka and Tokyo files); the "
                "2026-09-28 entry says the 露店 exclusion was meant for festival stalls")],
    "personal_catchall": absent("personal services come only from the barber, beauty and laundry registers"),
    "adult_hostess": [loc({"permit_type": "飲食店営業（バー・キャバレー）"}, "bars and cabarets"),
                      loc({"permit_type": "飲食店営業（一般・スナック）"}, "snack bars"),
                      loc({"permit_type": "① 飲食店営業", "form": "スナック、バー"}, "snack bar (業態)")],
    "sex_shop": absent("food-only Retail"),
    "massage_commercial": absent("no massage register among the sources"),
    "massage_regulated": absent("あん摩マッサージ licences are not a source"),
    "car_dealer": absent("food-only Retail"),
    "petrol_station": absent("food-only Retail"),
    "vehicle_repair": absent("not a food or 生活衛生 trade"),
    "gambling": absent("no gambling register"),
    "pawnbroker": absent("food-only Retail"),
    "nightclub": [loc({"permit_type": "① 飲食店営業", "form": "クラブ"}, "club (MHLW 業態)")],
    "vet": absent("not a food or 生活衛生 trade"),
    "nonstore": [loc({"permit_type": "⑨ 通信販売・訪問販売による販売業"}, "mail order"),
                 loc({"permit_type": "② 調理機能を有する自動販売機（要許可）"}, "vending machine")],
    "parking": absent("not a food or 生活衛生 trade"),
    "repair": absent("no repair register"),
    "lodging": [loc({"permit_type": "飲食店営業（旅館・ホテル）"}, "restaurant inside a hotel")],
    "recreation": [loc({"permit_type": "飲食店営業（一般・カラオケ）"}, "karaoke"),
                   loc({"permit_type": "① 飲食店営業", "form": "カラオケボックス"}, "karaoke box")],
    "pharmacy": absent("food-only Retail: a pharmacy is not a food shop (Stockholm's rule)"),
    "optician": absent("food-only Retail"),
    "mobile_unit": [loc({"permit_type": "㉕ 行商"}, "peddler"), loc({"permit_type": "飲食自動車"}, "vehicle"),
                    loc({"permit_type": "① 飲食店営業", "form": "キッチンカー"}, "kitchen car (業態)"),
                    loc({"permit_type": "移動美容室", "source": "beauty"}, "mobile salon"),
                    outside("pipeline/countries/japan_step2.py", "df = df[~mobile].copy()",
                            "mobile rows flagged by type or address, dropped before classify()")],
}

COLUMNS["korea_localdata"] = {
    "funeral": absent("none of the loaded permit files is funeral"),
    "no_counter_food": [loc({"oa": "OA-16094", "subtype": "출장조리"}, "catering"),
                        exception({"oa": "OA-16096", "subtype": "시장"}, "traditional market (대규모점포)",
                                  "Retail", RULED,
                                  "a registered market building holds fixed shops, not stalls")],
    "personal_catchall": absent("the files are named permit types, with no catch-all"),
    "adult_hostess": [loc({"oa": "OA-16090", "subtype": "룸살롱"}, "room salon (유흥주점)"),
                      loc({"oa": "OA-16090", "subtype": "카바레"}, "cabaret (유흥주점)")],
    "korean_karaoke_bar": [loc({"oa": "OA-16089", "subtype": "단란주점"}, "단란주점"),
                           loc({"oa": "단란주점영업", "subtype": "단란주점"}, "단란주점, by permit name")],
    "sex_shop": absent("no general-retail file"),
    "massage_commercial": absent("no massage file loaded"),
    "massage_regulated": absent("the 안마시술소 file is not loaded"),
    "car_dealer": absent("no vehicle-sales permit"),
    "petrol_station": absent("no fuel permit"),
    "vehicle_repair": absent("no repair permit"),
    "gambling": absent("no gambling file"),
    "pawnbroker": absent("no pawn file"),
    "nightclub": [loc({"oa": "OA-16094", "subtype": "감성주점"}, "bar under a general restaurant permit"),
                  exception({"oa": "OA-16090", "subtype": "고고(디스코)클럽"}, "disco club (유흥주점)", None,
                            JP_SEOUL, "유흥주점 out whole (the adult-services rule, owner 2026-09-21), "
                            "which R3 names; its disco clubs have no sub-type carve-out")],
    "vet": [loc({"oa": "OA-16007", "subtype": ""}, "animal hospital")],
    "nonstore": [loc({"oa": "OA-16070", "subtype": "자동판매기판매"}, "vending-machine health food")],
    "parking": absent("no parking file"),
    "repair": absent("no repair file"),
    "lodging": [loc({"oa": "OA-16044", "subtype": "여관업"}, "inn")],
    "recreation": absent("the 노래연습장, PC방 and gym files are not loaded"),
    "pharmacy": absent("no pharmacy file"),
    "optician": absent("no optician file"),
    "health_food": [loc({"oa": "OA-16070", "subtype": "영업장판매"}, "in-store health food")],
    "health_food_nonstore": [loc({"oa": "OA-16070", "subtype": "전자상거래(통신판매업)"}, "e-commerce"),
                             loc({"oa": "OA-16070", "subtype": "방문판매"}, "door-to-door"),
                             loc({"oa": "OA-16070", "subtype": "다단계판매"}, "multilevel")],
    "mobile_unit": [loc({"oa": "OA-16094", "subtype": "푸드트럭"}, "food truck"),
                    loc({"oa": "OA-16094", "subtype": "이동조리"}, "mobile cooking")],
}

KR_INCHEON = "Incheon built on SEMAS's national storefront register"
COLUMNS["korea_sbiz"] = {
    "funeral": [loc({"group": "장례식장", "category": "장례식장"}, "funeral hall"),
                loc({"group": "장례식장 ", "category": "화장터/묘지/납골당"}, "crematoria and cemeteries")],
    "no_counter_food": [loc({"group": "구내식당·뷔페", "category": "구내식당"}, "staff canteen")],
    "personal_catchall": [loc({"group": "기타 개인", "category": "예식장업"}, "wedding hall"),
                          loc({"group": "기타 개인", "category": "결혼 상담 서비스업"}, "matchmaking")],
    "adult_hostess": [loc({"group": "주점", "category": "일반 유흥 주점"}, "hostess bar")],
    "sex_shop": absent("no 소분류 of its own"),
    "massage_commercial": [loc({"group": "욕탕·신체관리", "category": "마사지/안마"}, "massage")],
    "massage_regulated": [loc({"group": "기타 보건", "category": "유사 의료업"}, "quasi-medical")],
    "car_dealer": [loc({"group": "모터사이클 소매", "category": "모터사이클 및 부품 소매업"}, "motorcycles")],
    "petrol_station": [loc({"group": "연료 소매", "category": "주유소"}, "petrol station"),
                       loc({"group": "연료 소매", "category": "가스 충전소"}, "LPG station")],
    "vehicle_repair": [loc({"group": "자동차 수리·세차", "category": "자동차 정비소"}, "car repair")],
    "gambling": [loc({"group": "유원지·오락", "category": "복권 발행/판매업"}, "lottery"),
                 loc({"group": "유원지·오락", "category": "전자 게임장"}, "game arcade")],
    "pawnbroker": absent("no pawn 소분류"),
    "nightclub": [exception({"group": "주점", "category": "무도 유흥 주점"}, "dance hall (유흥)", None,
                            KR_INCHEON, "dance halls left out under the adult-services rule, as "
                            "유흥 (owner, 2026-09-29)")],
    "vet": [loc({"group": "수의", "category": "동물병원"}, "animal hospital")],
    "nonstore": [loc({"group": "연료 소매", "category": "가정용 연료 소매업"}, "household fuel dealer")],
    "parking": absent("no parking 중분류"),
    "repair": [loc({"group": "가전제품 수리", "category": "가전제품 수리업"}, "appliance repair"),
               loc({"group": "기타 가정용품 수리", "category": "의류/이불 수선업"}, "clothing alterations")],
    "lodging": [loc({"group": "일반 숙박", "category": "호텔/리조트"}, "hotel")],
    "recreation": [loc({"group": "스포츠 서비스", "category": "헬스장"}, "gym"),
                   loc({"group": "유원지·오락", "category": "노래방"}, "karaoke room"),
                   loc({"group": "유원지·오락", "category": "PC방"}, "PC room")],
    "pharmacy": [loc({"group": "의약·화장품 소매", "category": "약국"}, "pharmacy")],
    "optician": [loc({"group": "안경·정밀기기 소매", "category": "안경렌즈 소매업"}, "optician")],
    "health_food": [loc({"group": "식료품 소매", "category": "건강보조식품 소매업"}, "health food")],
    "mobile_unit": absent("SEMAS lists active storefronts only: no vending, truck or stall class"),
}

COLUMNS["taiwan_fia"] = {
    "funeral": [loc("963011", "墓地經營 cemeteries"), loc("963012", "殯儀館經營 funeral parlours"),
                loc("963015", "殯葬禮儀服務 funeral services")],
    "funeral_goods": [loc("485212", "宗教、喪葬用品零售 religious and funeral goods")],
    "no_counter_food": [loc("562011", "外燴 catering"), loc("562012", "團膳 contract catering"),
                        loc("561200", "餐食攤販 food stalls"), loc("486111", "食品零售攤販 food retail stalls")],
    "personal_catchall": [loc("969099", "未分類其他個人服務"), loc("969019", "算命卜卦 fortune-telling"),
                          loc("969023", "婚姻介紹服務 marriage introduction"),
                          fixed("969014", "擦皮鞋 shoe-shine", "Personal services", "2026-09-29",
                                  "the rule's catch-all row names shoe-shine stands (Mexico's 812130 went "
                                  "out); Taiwan's own code for them stays Personal services, unaddressed")],
    "tattoo": [loc("969017", "紋身、紋眉服務 tattoo")],
    "adult_hostess": [loc("932311", "有侍者陪伴之茶室"), loc("932313", "有侍者陪伴之酒家、酒吧"),
                      loc("932316", "有侍者陪伴之夜總會")],
    "sex_shop": absent("no code of its own among the register's codes"),
    "massage_commercial": [loc("969015", "推拿按摩服務 massage")],
    "massage_regulated": [loc("869919", "國術推拿服務 (health, division 86)")],
    "car_dealer": [loc("484111", "全新汽車零售 new cars"), loc("484112", "中古汽車零售 used cars"),
                   loc("484211", "全新機車零售 new motorcycles")],
    "petrol_station": [loc("482111", "汽油零售 petrol"), loc("482113", "液化石油氣零售 LPG")],
    "vehicle_repair": [loc("951199", "其他汽車維修 car repair"), loc("465111", "全新汽車批發 wholesale")],
    "gambling": [loc("920011", "彩券銷售 lottery"), loc("920012", "博弈場經營 casinos"),
                 loc("932412", "小鋼珠店 pachinko")],
    "pawnbroker": [fixed("649611", "典當服務 pawnbrokers", None, "2026-09-29",
                           "division 64 (finance) is not bucketed, so pawnbrokers are off the map with "
                           "no stated reason; the rule keeps them")],
    "nightclub": [fixed("932918", "夜店 nightclubs", None, "2026-09-29",
                          "division 93 (recreation) is not bucketed; the rule keeps non-adult "
                          "nightclubs as Food service (Toronto and Edmonton aligned)"),
                  fixed("932917", "無侍者陪伴之舞場 dance halls without hostesses", None, "2026-09-29",
                          "as 夜店")],
    "vet": [loc("750000", "獸醫服務 veterinary")],
    "nonstore": [loc("487111", "經營郵購 mail order"), loc("487911", "自動販賣機 vending"),
                 fixed("482912", "桶裝瓦斯零售 bottled-gas retail", "Retail", "2026-09-29",
                         "cylinder-gas dealers deliver from a shop; Korea (가정용 연료 소매업) and Brazil "
                         "(DISTRIBUIDORA DE GAS) take the same trade out as nonstore fuel dealers"),
                 fixed("482911", "煤油零售 kerosene retail", "Retail", "2026-09-29", "as bottled gas")],
    "parking": [loc("524100", "停車場管理 parking")],
    "repair": [loc("952312", "家用電器維修 appliance repair"), loc("959913", "鞋、皮革品修理 shoe repair"),
               loc("959916", "衣服修改 alterations")],
    "lodging": [loc("551012", "旅館 hotels"), loc("551013", "民宿 guest houses")],
    "recreation": [loc("931219", "健身中心 gyms"), loc("932211", "KTV"), loc("932915", "上網專門店 PC rooms")],
    "pharmacy": [loc("475112", "西藥零售 pharmacies")],
    "optician": [loc("474412", "眼鏡零售 opticians")],
    "health_food": [loc("472933", "保健營養食品零售 health food")],
    "health_food_nonstore": [loc("487114", "網路購物（食品）online food"), loc("487212", "多層次傳銷 multilevel")],
    "mobile_unit": [loc("486112", "飲料零售攤販 drink stalls"), loc("487911", "自動販賣機 vending")],
}

COLUMNS["hong_kong_fehd"] = {
    "funeral": [loc("TU", "Undertaker's Licence"), loc("TF", "Funeral Parlour Licence")],
    "no_counter_food": [loc("FE", "Factory Canteen Licence")],
    "personal_catchall": absent("only TC Commercial Bathhouse is Personal services"),
    "adult_hostess": absent("no FEHD licence names adult or hostess premises"),
    "sex_shop": absent("no general-retail licence"),
    "massage_commercial": absent("not an FEHD licence"),
    "massage_regulated": absent("not an FEHD licence"),
    "car_dealer": absent("no general-retail licence"),
    "petrol_station": absent("no general-retail licence"),
    "vehicle_repair": absent("not an FEHD licence"),
    "gambling": absent("licensed outside FEHD"),
    "pawnbroker": absent("not an FEHD licence"),
    "nightclub": absent("nightclubs hold a General Restaurant Licence; no code of their own"),
    "vet": absent("not an FEHD licence"),
    "nonstore": absent("premises licences only"),
    "parking": absent("not an FEHD licence"),
    "repair": absent("not an FEHD licence"),
    "lodging": absent("not an FEHD licence"),
    "recreation": [loc("KE", "Karaoke Establishment Permit"), loc("PC", "cinema and theatre")],
    "pharmacy": absent("no general-retail licence"),
    "optician": absent("no general-retail licence"),
    "mobile_unit": [outside("pipeline/hong_kong/step2_clean_businesses.py", "FOOD_TRUCK_DISTRICT",
                            "food trucks, filed under their own district, dropped before classify()")],
}


PAWN_MIXED = ("no code of its own: pawnshops file under 64.92 other credit granting with every "
              "other lender, so none can be kept without the rest")
FUEL_DEALERS = ("heating-fuel dealers kept as Retail with no stated reason; Korea (가정용 연료 소매업), "
                "Brazil (DISTRIBUIDORA DE GAS) and NAICS 454310 take the same trade out as nonstore")

COLUMNS["france_naf"] = {
    "funeral": [loc("96.03Z", "services funéraires")],
    "funeral_goods": [loc("47.78C", "autres commerces de détail spécialisés divers (funeral goods)")],
    "no_counter_food": [
        loc("56.29A", "restauration collective sous contrat"),
        loc("47.81Z", "alimentaire sur éventaires et marchés"), loc("47.89Z", "autres, sur marchés"),
        outside("pipeline/paris/config.py", '"56.29B"', "56.29B other food service n.c.a. dropped in step 2"),
        exception("56.21Z", "services des traiteurs", "Food service", R1,
                  "R1: France's traiteurs kept, recorded as usually a shop")],
    "personal_catchall": [outside("pipeline/paris/config.py", 'CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")',
                                  "96.09Z autres services personnels dropped in step 2, every French city")],
    "tattoo": absent("no code of its own: tattooists sit in 96.09Z, the dropped catch-all"),
    "adult_hostess": absent("NAF names nothing as adult"),
    "sex_shop": absent("no code of its own; filed by product, as Retail"),
    "massage_commercial": [loc("96.04Z", "entretien corporel (non-medical massage)")],
    "massage_regulated": [loc("86.90E", "rééducation (masseurs-kinésithérapeutes)")],
    "car_dealer": [
        exception("45.11Z", "commerce de voitures", None, FOLLOWUPS,
                  "France's car dealers reversed: mostly one-person traders probably registered at "
                  "home (follow-up 1)"),
        exception("45.19Z", "autres véhicules automobiles", None, FOLLOWUPS, "follow-up 1"),
        exception("45.40Z", "motocycles", None, FOLLOWUPS, "follow-up 1")],
    "petrol_station": [loc("47.30Z", "carburants en magasin spécialisé")],
    "vehicle_repair": [loc("45.20A", "entretien et réparation de véhicules"), loc("45.31Z", "gros d'équipements")],
    "gambling": [loc("92.00Z", "jeux de hasard et d'argent")],
    "pawnbroker": absent(PAWN_MIXED),
    "nightclub": [loc("56.30Z", "débits de boissons (drink-led discothèques)")],
    "vet": [loc("75.00Z", "activités vétérinaires")],
    "nonstore": [loc("47.91A", "vente à distance, catalogue général"), loc("47.99A", "vente à domicile"),
                 loc("47.99B", "vente par automates"),
                 fixed("47.78B", "commerces de charbons et combustibles", "Retail", "2026-09-29", FUEL_DEALERS)],
    "parking": [loc("52.21Z", "services auxiliaires des transports terrestres")],
    "repair": [loc("95.12Z", "réparation d'équipements de communication"),
               loc("95.23Z", "réparation de chaussures"), loc("95.29Z", "retouches")],
    "lodging": [loc("55.10Z", "hôtels"), loc("55.20Z", "hébergement de courte durée")],
    "recreation": [loc("93.13Z", "centres de culture physique"), loc("59.14Z", "cinémas")],
    "pharmacy": [loc("47.73Z", "produits pharmaceutiques")],
    "optician": [loc("47.78A", "optique")],
    "health_food": [loc("47.29Z", "autres commerces alimentaires en magasin")],
    "health_food_nonstore": [loc("47.99A", "vente à domicile")],
    "mobile_unit": [loc("47.99B", "automates et hors magasin")],
}


def _rev21(code_of, catch_all_path, catch_all_token, city):
    """The shared shape of the three NACE Rev. 2.1 national registers."""
    c = code_of
    return {
        "funeral": [loc(c("96.30"), "funeral services")],
        "no_counter_food": [loc(c("56.21"), "event catering"), loc(c("56.22"), "contract catering and canteens"),
                            loc(c("56.12"), "mobile food")],
        "personal_catchall": [outside(catch_all_path, catch_all_token,
                                      f"96.99 other personal services dropped in step 2 ({city})")],
        "tattoo": absent("no code of its own in Rev. 2.1: tattoo sits in 96.99, the dropped catch-all"),
        "adult_hostess": absent("Rev. 2.1 names nothing as adult"),
        "sex_shop": absent("no code of its own; filed by product, as Retail"),
        "massage_commercial": [loc(c("96.23"), "day spas, saunas and steam baths (massage)")],
        "massage_regulated": [loc(c("86.95"), "physiotherapy")],
        "car_dealer": [loc(c("47.81"), "motor vehicles"), loc(c("47.83"), "motorcycles")],
        "petrol_station": [loc(c("47.30"), "automotive fuel")],
        "vehicle_repair": [loc(c("95.31"), "motor vehicle repair"), loc(c("46.71"), "motor vehicle wholesale")],
        "gambling": [loc(c("92.00"), "gambling and betting")],
        "pawnbroker": absent(PAWN_MIXED),
        "nightclub": [loc(c("56.30"), "beverage serving")],
        "vet": [loc(c("75.00"), "veterinary activities")],
        "nonstore": [loc(c("47.91"), "retail intermediation"), loc(c("47.92"), "retail intermediation, specialised")],
        "parking": [loc(c("52.21"), "land-transport support incl. parking")],
        "repair": [loc(c("95.10"), "computer and phone repair"), loc(c("95.23"), "footwear repair"),
                   loc(c("95.29"), "other personal goods (alterations)")],
        "lodging": [loc(c("55.10"), "hotels"), loc(c("55.20"), "short-stay accommodation")],
        "recreation": [loc(c("93.13"), "fitness centres"), loc(c("59.14"), "cinemas")],
        "pharmacy": [loc(c("47.73"), "pharmaceutical retail")],
        "optician": [loc(c("47.74"), "medical and orthopaedic goods (opticians)")],
        "health_food": [loc(c("47.27"), "other food retail")],
        "mobile_unit": [loc(c("56.12"), "mobile food")],
    }


COLUMNS["norway_sn2025"] = _rev21(lambda d: d + "0", "pipeline/oslo/config.py",
                                  'CATCH_ALL_EXCLUDE = ("96.990",)', "Oslo")
COLUMNS["denmark_db25"] = _rev21(lambda d: d.replace(".", "") + "00", "pipeline/copenhagen/config.py",
                                 'CATCH_ALL_EXCLUDE = ("969900",)', "Copenhagen")
COLUMNS["czech_nace2025"] = _rev21(lambda d: d.replace(".", "") + "0", "pipeline/prague/config.py",
                                   'CATCH_ALL_EXCLUDE = ("96990", "969")', "Prague")
COLUMNS["czech_nace2025"]["personal_catchall"] = [
    outside("pipeline/prague/config.py", 'CATCH_ALL_EXCLUDE = ("96990", "969")',
            "96990 and the bare 969 group (21 rows, the ragged register) dropped in step 2 "
            "[the 969 row fixed, approved 2026-09-29]")]

BERLIN_CFG = "pipeline/berlin/config.py"
BERLIN_969 = '"nace_id": ("969",)'


def _ihk(nace, branch):
    return {"nace_id": nace, "ihk_branch_id": branch}


COLUMNS["ihk_wz2025"] = {
    "funeral": [loc(_ihk("9630", "96301"), "Bestattungsinstitute"),
                loc(_ihk("9630", "96302"), "Friedhöfe und Krematorien")],
    "no_counter_food": [loc(_ihk("5621", "56210"), "Event-Caterer"), loc(_ihk("5622", "562202"), "Kantinen")],
    "personal_catchall": [outside(BERLIN_CFG, BERLIN_969, "9699 and bare 969 dropped by prefix in step 2")],
    "tattoo": [exception(None, "Tätowier- und Piercingstudios (96991, 1,262)", None, CONFIRMED,
                         "tattoo has its own IHK branch code but goes with the 969 prefix: the "
                         "owner's 2026-09-28 call, confirmed after R2 (2026-09-29)",
                         path=BERLIN_CFG, token=BERLIN_969)],
    "adult_hostess": [outside(BERLIN_CFG, BERLIN_969,
                              "prostitution (96992) and escort services (969992) go with the 969 prefix")],
    "sex_shop": [loc(_ihk("4712", "471212"), "Einzelhandel mit Erotikartikeln")],
    "massage_commercial": [loc(_ihk("9623", "962302"), "Massage (nicht medizinisch)")],
    "massage_regulated": [loc(_ihk("8695", "86951"), "physiotherapeutische Dienstleistungen")],
    "car_dealer": [loc(_ihk("4781", "47811"), "Kraftwagen bis 3,5 t"), loc(_ihk("4783", "47830"), "Krafträder")],
    "petrol_station": [loc(_ihk("4730", "47301"), "Agenturtankstelle"), loc(_ihk("4730", "473012"), "Gastankstelle")],
    "vehicle_repair": [loc(_ihk("9531", "95313"), "Reparatur von Kraftwagen"),
                       loc(_ihk("4671", "46711"), "Großhandel mit Kraftwagen")],
    "gambling": [loc(_ihk("9200", "920042"), "Wettbüro"), loc(_ihk("9200", "920041"), "Lotto-Annahmestelle"),
                 loc(_ihk("9200", "920011"), "Spielhallen")],
    "pawnbroker": [fixed(_ihk("6492", "64922"), "Leihhäuser (35)", None, "2026-09-29",
                           "pawnshops have their own IHK branch, but classify() reads the 4-digit class, "
                           "credit granting, which is not a bucket; the rule keeps pawnbrokers")],
    "nightclub": [loc(_ihk("5630", "56302"), "Diskotheken und Tanzlokale")],
    "vet": [loc(_ihk("7500", "75001"), "Tierärztliche Praxen")],
    "nonstore": [loc(_ihk("4791", "47911"), "Versteigerungsgewerbe"), loc(_ihk("4792", "47922"), "Vermittlung"),
                 outside(BERLIN_CFG, '"ihk_branch_id": ("47122", "477893")',
                         "general non-food retail with no premises (47122) and Einzelhandel mit "
                         "Brennstoffen (477893, 36; fixed, approved 2026-09-29) dropped in step 2")],
    "parking": [loc(_ihk("5221", "52211"), "Parkhäuser und Parkplätze")],
    "repair": [loc(_ihk("9510", "95102"), "Reparatur von Telekommunikationsgeräten"),
               loc(_ihk("9523", "95230"), "Schuhreparatur"), loc(_ihk("9529", "952903"), "Änderungsschneiderei")],
    "lodging": [loc(_ihk("5510", "55101"), "Hotels"), loc(_ihk("5520", "55202"), "Ferienwohnungen")],
    "recreation": [loc(_ihk("9313", "93130"), "Fitnesszentren"), loc(_ihk("5914", "59140"), "Kinos")],
    "pharmacy": [loc(_ihk("4773", "477301"), "Apotheken")],
    "optician": [loc(_ihk("4774", "47741"), "Brillen und Kontaktlinsen")],
    "health_food": [loc(_ihk("4727", "472704"), "Reformwaren")],
    "mobile_unit": [loc(_ihk("5612", "56121"), "mobile Gastronomie")],
}

RETAIL_DIV = "COMERCIO AL POR MENOR, EXCEPTO DE VEHÍCULOS DE MOTOR Y MOTOCICLETAS"
FOOD_DIV = "SERVICIOS DE COMIDAS Y BEBIDAS"
REC_DIV = "ACTIVIDADES DEPORTIVAS, RECREATIVAS Y DE ENTRETENIMIENTO"
VEH_DIV = "VENTA Y REPARACIÓN DE VEHÍCULOS DE MOTOR Y MOTOCICLETAS"
REP_DIV = "REPARACIÓN DE ORDENADORES, EFECTOS PERSONALES Y ARTÍCULOS DE USO DOMÉSTICO"


def _mad(div, epi):
    return {"desc_division": div, "desc_epigrafe": epi}


MAD_MOBILE = ("the R1 carve-out lists canteens, hospital catering and banquets; mobile food and "
              "situados (street pitches) are not mentioned and stay on the map")
COLUMNS["madrid_epigrafe"] = {
    "funeral": [loc(_mad("OTROS SERVICIOS PERSONALES", "POMPAS FUNEBRES Y ACTIVIDADES RELACIONADAS"),
                    "pompas fúnebres")],
    "no_counter_food": [
        loc(_mad(FOOD_DIV, "SERVICIOS DE COMEDOR EN CENTROS EDUCATIVOS Y CENTROS DE CUIDADO INFANTIL"),
            "school canteens"),
        loc(_mad(FOOD_DIV, "SALONES DE BANQUETES Y PROVISION COMIDAS PARA EVENTOS"), "banquets and caterers"),
        loc(_mad(RETAIL_DIV, "COMERCIO AL POR MENOR EN PUESTOS DE VENTA Y EN MERCADILLOS"), "market stalls"),
        fixed(_mad(RETAIL_DIV, "SITUADOS: CHURROS Y FREIDURIAS SIN NINGIN TIPO DE RELLENO"),
                "street pitch (situado), churros", "Retail", "2026-09-29",
                MAD_MOBILE + " (about 163 situados in all)")],
    "personal_catchall": [loc(_mad("OTROS SERVICIOS PERSONALES",
                                   "OTRAS SERVICIOS PERSONALES (ASTROLOGIA, AGENCIAS DE CONTACTOS) N.C.O.P."),
                              "the catch-all")],
    "tattoo": [loc(_mad("OTROS SERVICIOS PERSONALES", "CENTROS DE TATUAJE Y/O ANILLADO"), "tattoo")],
    "adult_hostess": [loc(_mad("ACTIVIDADES DE CREACIÓN, ARTÍSTICAS Y ESPECTÁCULOS", "LOCALES DE EXHIBICIONES EROTICAS"),
                          "erotic exhibition venues")],
    "sex_shop": [loc(_mad(RETAIL_DIV, "SEX-SHOP"), "sex shop")],
    "massage_commercial": [loc(_mad("OTROS SERVICIOS PERSONALES", "BALNEARIOS Y SPA URBANOS"), "urban spas")],
    "massage_regulated": [loc(_mad("ACTIVIDADES SANITARIAS", "DESPACHO DE FISIOTERAPEUTAS"), "physiotherapists")],
    "car_dealer": [loc(_mad(VEH_DIV, "COMERCIO DE VEHICULOS DE MOTOR NUEVOS"), "new vehicles"),
                   loc(_mad(VEH_DIV, "COMERCIO DE VEHICULOS DE MOTOR USADOS"), "used vehicles"),
                   loc(_mad(VEH_DIV, "VENTA DE MOTOCICLETAS"), "motorcycles")],
    "petrol_station": [loc(_mad(RETAIL_DIV, "COMERCIO AL POR MENOR DE COMBUSTIBLE PARA LA AUTOMOCION EN "
                                            "ESTABLECIMIENTOS ESPECIALIZADOS"), "automotive fuel")],
    "vehicle_repair": [loc(_mad(VEH_DIV, "TALLER DE REPARACION DE AUTOMOVILES ESPECIALIZADO EN MECANICA Y "
                                         "ELECTRICIDAD"), "car repair")],
    "gambling": [loc(_mad("ACTIVIDADES DE JUEGOS DE AZAR Y APUESTAS",
                          "JUEGOS DE AZAR Y APUESTAS DE GESTION PRIVADA (BINGOS, CASINOS, MAQUINAS TRAGAPERRAS)"),
                     "bingos and casinos")],
    "pawnbroker": absent("no pawnbroker epígrafe: pawnshops sit with other lenders or second-hand shops"),
    "nightclub": [loc(_mad(FOOD_DIV, "BAR ESPECIAL CON ACTUACIONES"), "late bar with acts"),
                  fixed(_mad(REC_DIV, "DISCOTECAS Y SALAS DE BAILE"), "discos and dance halls (233)",
                          None, "2026-09-29",
                          "their division is recreation, which is not a bucket; the rule keeps "
                          "non-adult nightclubs as Food service (Toronto and Edmonton aligned)")],
    "vet": [loc(_mad("ACTIVIDADES VETERINARIAS", "CLINICA VETERINARIA CON TRATAMIENTO HIGIENICO"), "vet clinic")],
    "nonstore": [loc(_mad(RETAIL_DIV, "COMERCIO AL POR MENOR POR CORRESPONDENCIA, INTERNET, A DOMICILIO"),
                     "mail order, internet, door-to-door"),
                 loc(_mad(RETAIL_DIV, "COMERCIO AL POR MENOR CON MAQUINAS EXPENDEDORAS"), "vending machines")],
    "parking": [loc(_mad("ALMACENAMIENTO Y ACTIVIDADES ANEXAS AL TRANSPORTE", "APARCAMIENTOS PUBLICOS"), "car parks")],
    "repair": [loc(_mad(REP_DIV, "ARREGLO DE ROPA"), "alterations"), loc(_mad(REP_DIV, "REPARACION DE CALZADO"), "shoes")],
    "lodging": [loc(_mad("SERVICIOS DE ALOJAMIENTO", "HOSTALES"), "hostales")],
    "recreation": [loc(_mad(REC_DIV, "ACTIVIDADES DE LOS GIMNASIOS"), "gyms")],
    "pharmacy": [loc(_mad(RETAIL_DIV, "FARMACIA"), "pharmacy")],
    "optician": [loc(_mad(RETAIL_DIV, "COMERCIO AL POR MENOR DE MATERIAL DE OPTICA"), "optical goods")],
    "health_food": [loc(_mad(RETAIL_DIV, "COMERCIO AL POR MENOR DE PRODUCTOS DE HERBOLARIO"), "herbalist")],
    "mobile_unit": [fixed(_mad(FOOD_DIV, "ESTABLECIMIENTO DE RESTAURACION MOVIL"), "mobile food outlet (18)",
                            "Food service", "2026-09-29", MAD_MOBILE),
                    fixed(_mad(FOOD_DIV, "VENDEDOR AMBULANTE DE ALIMENTOS PREPARADOS PARA SU CONSUMO INMEDIATO"),
                            "street food vendor (3)", "Food service", "2026-09-29", MAD_MOBILE)],
}


def _bcn(act, grp, sec):
    return {"Nom_Activitat": act, "Nom_Grup_Activitat": grp, "Nom_Sector_Activitat": sec}


BCN_REST = "Restaurants, bars i hotels (Inclòs hostals, pensions i fondes)"
COLUMNS["barcelona_activitat"] = {
    "funeral": absent("the census has no funeral value"),
    "no_counter_food": absent("no canteen, caterer or stall value: ground-floor premises only"),
    "personal_catchall": [loc(_bcn("Altres", "Altres", "Serveis"), "the services residual")],
    "adult_hostess": absent("no value names adult venues"),
    "sex_shop": absent("no value of its own"),
    "massage_commercial": absent("no massage value"),
    "massage_regulated": [loc(_bcn("Sanitat i assistència", "Sanitat i assistència", "Serveis"), "health and care")],
    "car_dealer": [loc(_bcn("Vehicles", "Automoció", "Comerç al detall"), "vehicles")],
    "petrol_station": [loc(_bcn("Combustibles i carburants", "Quotidià no alimentari", "Comerç al detall"), "fuels")],
    "vehicle_repair": [loc(_bcn("Reparacions (Electrodomèstics i automòbils)",
                                "Reparacions (Electrodomèstics i automòbils)", "Serveis"), "appliance and car repair")],
    "gambling": absent("no gambling value"),
    "pawnbroker": absent("no value of its own"),
    "nightclub": [loc(_bcn("Bars especials amb actuació / Bars musicals / Discoteques /PUB", BCN_REST, "Serveis"),
                      "music bars and discos")],
    "vet": [exception(_bcn("Veterinaris / Mascotes", "Altres", "Serveis"), "vets and pet services (395)",
                      "Personal services", FOLLOWUPS,
                      "one value mixes about 160 vet clinics with pet shops and groomers; left in and "
                      "disclosed (follow-up 5)")],
    "nonstore": [loc(_bcn("Altres ( per exemple VENDING)", BCN_REST, "Serveis"), "vending")],
    "parking": [loc(_bcn("Pàrquings i garatges", "Altres", "Serveis"), "car parks")],
    "repair": [loc(_bcn("Reparacions (Electrodomèstics i automòbils)",
                        "Reparacions (Electrodomèstics i automòbils)", "Serveis"), "appliance repair"),
               fixed(_bcn("Arranjaments", "Altres", "Serveis"), "garment repair and alterations (649)",
                       "Personal services", "2026-09-29",
                       "counted as a personal service ('NAICS 812's shape') with no DECISIONS entry; "
                       "the repairs rule names clothing alterations as out")],
    "lodging": [loc(_bcn("serveis d'allotjament", BCN_REST, "Serveis"), "hotels")],
    "recreation": [loc(_bcn("Gimnàs /fitnes", "Altres", "Altres"), "gyms")],
    "pharmacy": [loc(_bcn("Farmàcies PARAFARMÀCIA", "Quotidià no alimentari", "Comerç al detall"), "pharmacies")],
    "optician": [loc(_bcn("Òptiques", "Altres", "Comerç al detall"), "opticians")],
    "health_food": [loc(_bcn("Herbolaris, dietètica i NUTRICIÓ", "Quotidià no alimentari", "Comerç al detall"),
                        "herbalists")],
    "mobile_unit": [loc(_bcn("Altres ( per exemple VENDING)", BCN_REST, "Serveis"), "vending")],
}


BAG_LUMPED = ("the permit layer is hospitality permits only, and the building register's shop units "
              "carry no activity, so any such trade in a shop unit is 'Shops and services' and cannot "
              "be separated (owner, 2026-09-24; funeral disclosed 2026-09-29)")


def _ams(cat, spec=None, source="permit"):
    return {"source": source, "zaak_categorie": cat, "zaak_specificatie": spec}


COLUMNS["amsterdam_source"] = {
    **{rid: absent(BAG_LUMPED) for rid in (
        "funeral", "sex_shop", "massage_commercial", "massage_regulated", "car_dealer", "petrol_station",
        "vehicle_repair", "gambling", "pawnbroker", "vet", "nonstore", "parking", "repair", "pharmacy",
        "optician")},
    "no_counter_food": [loc(_ams("Additionele horeca"), "catering inside non-commercial venues")],
    "personal_catchall": [loc(_ams("Zalenverhuur"), "hall hire")],
    "adult_hostess": absent("sex businesses hold a separate licence that is not fetched"),
    "nightclub": [loc(_ams("Nachtzaak"), "night venue"), loc(_ams("Onbekend", "Discotheek"), "disco")],
    "lodging": [loc(_ams("Hotel"), "hotel")],
    "recreation": [loc(_ams("Culturele horeca"), "cultural venues' horeca"),
                   loc(_ams("Onbekend", "Sporthal"), "sports hall")],
    "mobile_unit": absent("a permit is for a fixed premises; no mobile or stall category"),
}

COLUMNS["anzsic_fes"] = {
    "funeral": [loc("9520", "funeral, crematorium and cemetery services")],
    "no_counter_food": [loc("4513", "catering services")],
    "personal_catchall": [loc("9539", "other personal services n.e.c.")],
    "tattoo": absent("no class of its own: tattoo studios fall in 9539, the catch-all"),
    "adult_hostess": [loc("9534", "brothel keeping")],
    "sex_shop": [loc("4279", "other store-based retailing (adult shops file here)")],
    "massage_commercial": [loc("9511", "hairdressing and beauty (massage names)")],
    "massage_regulated": [loc("8539", "other allied health")],
    "car_dealer": [loc("3911", "car retailing"), loc("3912", "motor cycle retailing")],
    "petrol_station": [loc("4000", "fuel retailing")],
    "vehicle_repair": [loc("9419", "automotive repair"), loc("3501", "car wholesaling")],
    "gambling": [loc("9201", "casino"), loc("9202", "lottery"), loc("9209", "other gambling")],
    "pawnbroker": [loc("4273", "antique and used goods (pawnbrokers file here)")],
    "nightclub": [loc("4520", "pubs, taverns and bars (nightclubs)")],
    "vet": [loc("6970", "veterinary services")],
    "nonstore": [loc("4310", "non-store retailing"), loc("4320", "commission-based retailing")],
    "parking": [loc("9533", "parking services")],
    "repair": [loc("9491", "clothing and footwear repair"), loc("9421", "appliance repair")],
    "lodging": [loc("4400", "accommodation")],
    "recreation": [loc("9111", "gyms"), loc("5513", "cinemas"), loc("9139", "karaoke rooms")],
    "pharmacy": [loc("4271", "pharmaceutical and toiletry retailing")],
    "optician": [exception("8532", "optometry and optical dispensing (Specsavers; 33 in Melbourne)", None,
                           CONFIRMED, "ANZSIC files optical shops with optometry in health "
                           "(division 85), not a storefront division; left out (owner)")],
    "health_food": [loc("4129", "other specialised food retailing")],
    "mobile_unit": absent("no mobile class: vending is in 4310, out"),
}

COLUMNS["fsa_businesstype"] = {
    **{rid: absent("a food-hygiene register: food businesses only") for rid in (
        "funeral", "personal_catchall", "adult_hostess", "sex_shop", "massage_commercial", "massage_regulated",
        "car_dealer", "vehicle_repair", "gambling", "pawnbroker", "vet", "parking", "repair", "recreation",
        "optician")},
    "no_counter_food": [
        loc("Other catering premises", "home, event and contract caterers"),
        loc("Hospitals/Childcare/Caring Premises", "institutional kitchens"),
        loc("School/college/university", "school kitchens"),
        exception("Restaurant/Cafe/Canteen", "restaurants, cafés and workplace canteens", "Food service",
                  FOLLOWUPS, "the food-register cities' canteens disclosed, not separable (follow-up 8): "
                  "a workplace canteen registered as a restaurant or café may appear")],
    "petrol_station": [loc("Retailers - other", "other retailers (forecourt shops)")],
    "nightclub": [loc("Pub/bar/nightclub", "pub, bar or nightclub")],
    "nonstore": [loc("Distributors/Transporters", "distributors")],
    "lodging": [loc("Hotel/bed & breakfast/guest house", "hotels")],
    "pharmacy_food_register": [
        exception("Retailers - other", "other retailers (about 489 pharmacy names in London)",
                  "Retail", CONFIRMED,
                  "the FSA cities keep their pharmacies under 'Retailers - other', unlike "
                  "Stockholm's name filter (owner)")],
    "pharmacy": absent("a food-only register: its pharmacies fall under pharmacy_food_register"),
    "health_food": [loc("Retailers - other", "other retailers (health-food chains)")],
    "mobile_unit": [loc("Mobile caterer", "mobile caterer")],
}

COLUMNS["milan_source"] = {
    **{rid: absent("six fixed-premises registers; the bucket is the register, with no field for "
                   "this trade") for rid in (
        "personal_catchall", "adult_hostess", "sex_shop", "massage_regulated", "car_dealer", "vehicle_repair",
        "gambling", "pawnbroker", "vet", "nonstore", "parking", "repair", "lodging", "recreation", "optician",
        "mobile_unit")},
    "funeral": absent("no register for it; about 29 funeral names reach the shop register, disclosed "
                      "(a name filter was rejected, owner)"),
    "no_counter_food": [outside("pipeline/milan/config.py", "FUORI_PIANO_EXCLUDE",
                                "canteens (mensa) and private clubs dropped by label before classify()")],
    "tattoo": [loc({"source": "servizi_persona"}, "personal-services register (tattoo)")],
    "massage_commercial": [loc({"source": "servizi_persona"}, "personal-services register (massage centres)")],
    "petrol_station": [loc({"source": "vicinato"}, "neighbourhood shops (fuel table)")],
    "nightclub": [loc({"source": "pe_fuori_piano"}, "public premises (discos)")],
    "pharmacy": [loc({"source": "vicinato"}, "neighbourhood shops (pharmacy table)")],
}

RIGA_CFG = "pipeline/riga/config.py"
COLUMNS["riga_source"] = {
    **{rid: absent("a building register of shop units named by their occupants; this trade has no "
                   "name rule and is dropped unmatched") for rid in (
        "funeral", "personal_catchall", "adult_hostess", "massage_regulated", "vet", "nonstore", "parking",
        "lodging", "recreation")},
    "no_counter_food": [exception(None, "market pavilions kept as shops ('tirgus', 'paviljon')", "Retail",
                                  RULED, "a market pavilion is a building of fixed shops, not stalls",
                                  path=RIGA_CFG, token="tirgus"),
                        outside(RIGA_CFG, '("stall", r"stends|^lete")',
                                "stands dropped by name, as stalls [fixed, approved 2026-09-29]")],
    "sex_shop": [outside(RIGA_CFG, "veikal", "sex shops kept as shops by name")],
    "massage_commercial": [outside(RIGA_CFG, "masāž", "massage kept as a personal service by name")],
    "car_dealer": [outside(RIGA_CFG, "autosalon", "car showrooms kept as shops by name")],
    "petrol_station": [outside(RIGA_CFG, 'NAME_KEEP = ("shop_retail", "personal_service", "fuel")',
                               "fuel stations kept by name [fixed, approved 2026-09-29]")],
    "vehicle_repair": [outside(RIGA_CFG, '("repair", r"šūšan|remont|darbnīc|apavu|atslēg")',
                               "workshops dropped by name [fixed, approved 2026-09-29]")],
    "repair": [outside(RIGA_CFG, '("repair", r"šūšan|remont|darbnīc|apavu|atslēg")',
                       "shoe, sewing and key repair dropped by name [fixed, approved 2026-09-29]")],
    "gambling": [outside(RIGA_CFG, '("gambling", r"', "gambling premises dropped by name")],
    "pawnbroker": [outside(RIGA_CFG, "lombard", "pawnbrokers kept by name")],
    "nightclub": [outside(RIGA_CFG, "FOOD_RE", "excise-register clubs kept as food service")],
    "pharmacy": [outside(RIGA_CFG, "aptiek", "pharmacies kept as shops by name")],
    "optician": [outside(RIGA_CFG, "optik", "opticians kept as shops by name")],
    "health_food": absent("not separable by name"),
    "mobile_unit": [exception({"source": "cadastre", "activity": "Shop"}, "kiosks and pavilions ('kiosk')",
                              "Retail", FOLLOWUPS, "kiosks are small walk-in shops, as Dublin's (follow-up 4)")],
}


def _ro(cat, files="A19"):
    return {"Categorie": cat, "source_files": files}


COLUMNS["romania_dsvsa"] = {
    **{rid: absent("a food-only register of registered food units") for rid in (
        "funeral", "personal_catchall", "adult_hostess", "sex_shop", "massage_commercial", "massage_regulated",
        "car_dealer", "petrol_station", "vehicle_repair", "gambling", "pawnbroker", "vet", "parking", "repair",
        "lodging", "recreation", "pharmacy", "optician")},
    "no_counter_food": [loc(_ro("catering"), "catering"), loc(_ro("bufet incinta"), "in-house buffet"),
                        outside("pipeline/bucharest/config.py", "ANIMAL_FILES",
                                "the canteen and catering files are not fetched (owner, 2026-09-28)")],
    "nightclub": [loc(_ro("bar", "N36"), "bar")],
    "nonstore": absent("registered food units only; internet-sales units are shops that also sell online",
                       ignore=()),
    "mobile_unit": [loc(_ro("toneta", "A25"), "kiosk cart"), loc(_ro("automat inghetata", "N24"), "vending"),
                    fixed(_ro("fast food (rulota)"), "fast food in a trailer", "Food service", "2026-09-29",
                            "seven A19 units whose category says trailer or mobile unit stay Food service; "
                            "neither the category rule nor step 2's sector test catches 'rulota'")],
}


def _rome(desc, spec=None):
    return {"descrizione": desc, "specializzazione": spec}


LAB = "Laboratorio Artigianale e non"
VIC = "Esercizio di Vicinato"
COLUMNS["rome_suap"] = {
    "funeral": absent("no authorisation type or specialisation for funeral services"),
    "no_counter_food": [loc(_rome(LAB, "GASTRONOMIA PER SERVIZIO CATERING"), "catering kitchen"),
                        loc(_rome("Spacci Interni"), "internal company outlets"),
                        loc(_rome("Somministrazione di alimenti e bevande in occasione di sagre"), "festival stalls")],
    "personal_catchall": [loc(_rome(LAB), "workshop catch-all, blank specialisation")],
    "tattoo": [loc(_rome(LAB, "TATUAGGIO"), "tattoo")],
    "adult_hostess": absent("no adult authorisation type"),
    "sex_shop": absent("no value of its own; inside neighbourhood shops"),
    "massage_commercial": [loc(_rome("Acconciatori ed Estetisti", "ESTETISTA"), "beauticians (massage)")],
    "massage_regulated": absent("not in the register"),
    "car_dealer": absent("no vehicle-sales value; dealers sit undistinguished among shops"),
    "petrol_station": [loc(_rome(VIC, "DISTRIBUTORI DI CARBURANTI"), "fuel distributors")],
    "vehicle_repair": [loc(_rome(LAB, "AUTOFFICINA"), "car workshop"), loc(_rome(LAB, "CARROZZERIA"), "body shop")],
    "gambling": [loc(_rome("Sala Giochi"), "gaming hall"), loc(_rome("Apparecchi e Congegni Automatici"), "machines")],
    "pawnbroker": absent("no value of its own"),
    "nightclub": [loc(_rome("Somministrazione Attività Trattenimento e Svago (EX ART. 13 C. 1 Reg)"),
                      "bars and clubs with entertainment")],
    "vet": absent("not in the register"),
    "nonstore": [loc(_rome("Commercio Elettronico"), "e-commerce"), loc(_rome("Vendita per Corrispondenza"), "mail order"),
                 loc(_rome("Vendita Presso il Domicilio dei Consumatori"), "door-to-door")],
    "parking": [loc(_rome("Rimessa di veicoli"), "vehicle garage")],
    "repair": [loc(_rome(LAB, "RIPARAZIONE CALZATURE"), "shoe repair"), loc(_rome(LAB, "SARTORIA"), "tailoring")],
    "lodging": [loc(_rome("Agriturismo"), "farm stay")],
    "recreation": [loc(_rome("Phone Center - Internet Point"), "internet point")],
    "pharmacy": [loc(_rome(VIC, "FARMACIE"), "pharmacy")],
    "optician": [loc(_rome(VIC, "ALTRI ESERCIZI SPECIALIZZATI NON ALIMENTARI (MACCHINE E ATTREZZATURE PER UFFICIO,"
                                "OTTICA, FOTOGRAFIA, GIOIELLERIA, GIOCATTOLI, ARTICOLI SPORTIVI, ARTICOLI DA "
                                "REGALO,COMBUSTIBILE, NATANTI, ALTRO"), "other non-food shops, optics included")],
    "health_food": [loc(_rome(VIC, "ERBORISTERIA"), "herbalist")],
    "health_food_nonstore": [loc(_rome("Commercio Elettronico", "ERBORISTERIA"), "online herbalist")],
    "mobile_unit": [loc(_rome("Commercio Prodotti per mezzo di apparecchi automatici"), "vending machines")],
}

RTM_STEP2 = "pipeline/rotterdam/step2_clean_businesses.py"
COLUMNS["rotterdam_source"] = {
    **{rid: absent(BAG_LUMPED) for rid in (
        "funeral", "personal_catchall", "sex_shop", "massage_commercial", "massage_regulated", "car_dealer",
        "petrol_station", "vehicle_repair", "pawnbroker", "vet", "nonstore", "parking", "repair", "lodging",
        "recreation", "pharmacy", "optician", "mobile_unit")},
    "no_counter_food": [outside(RTM_STEP2, '("event", r"kortlopende")', "short-term event permits never kept")],
    "adult_hostess": [outside(RTM_STEP2, '("sex business",', "sex-business notices never kept")],
    "gambling": [outside(RTM_STEP2, '("gaming",', "gaming-machine notices never kept")],
    "nightclub": [loc({"source": "permit", "notice_kind": "exploitatie"}, "exploitation permit (all horeca)")],
}

STOCKHOLM = "Stockholm built on its frozen food inspection register"
REST = "Restaurang-, catering- och barverksamhet"
CATERING_BRANCH = ("owner-approved (R1) and waiting on branch stockholm-catering, which adds a caterer "
                   "and mobile-unit name filter; when it lands this row is stale and must become a loc()")


def _se(typ, name, name_classified=None):
    row = {"VerksamhetsTyp": typ, "business_name": name}
    if name_classified is not None:
        row["name_classified"] = name_classified
    return row


KW_TYPE, KW_CAT = "Type not a storefront", "Institutional, mobile or processing category"
COLUMNS["kitchener_waterloo_inspection"] = {
    **{rid: absent("food and personal-services inspection registers: no such type, and none "
                   "found by name at the build") for rid in (
        "funeral", "personal_catchall", "adult_hostess", "sex_shop", "massage_regulated",
        "car_dealer", "vehicle_repair", "gambling", "pawnbroker", "vet", "parking", "repair",
        "optician")},
    "no_counter_food": [
        loc(KW_TYPE, "caterers and commissaries, community, church and serving kitchens, school "
                     "and workplace cafeterias, food banks, banquet halls, by type"),
        loc(KW_CAT, "the Institutional category (childcare, schools' programmes, care homes, "
                    "hospitals), by type"),
        loc("Institutional kitchen or service", "campus and hospital outlets, church and "
                                                "community-centre cafes, caterers with no counter, "
                                                "by name"),
        loc("Market stall", "the Kitchener Market's Saturday stalls, by name")],
    "tattoo": [loc("Personal services", "Tattooing / Micropigmentation, its own type")],
    "massage_commercial": [loc("Personal services", "Massage, its own type")],
    "petrol_station": [loc("Food shop", "forecourt shops typed as convenience stores "
                                        "(AM 2 PM Express Market / Petro Canada)")],
    "nightclub": [loc("Restaurant or bar", "Cocktail Bar/ Nightclub, its own type")],
    "nonstore": [loc(KW_TYPE, "Food Vending Facility, by type")],
    "lodging": [loc("Hotel back of house", "hotels' breakfast rooms and serveries and bare hotel "
                                           "names, by name"),
                loc(KW_CAT, "group and lodging homes (Institutional category), by type")],
    "recreation": [loc("Recreation venue or club", "the Aud's stands, arenas, golf and other "
                                                   "clubs, lanes, cinemas, theatres, play venues, "
                                                   "gyms, by name")],
    "pharmacy": absent("a food and personal-services register: its pharmacies fall under "
                       "pharmacy_food_register, which is where the module's pharmacy strings are "
                       "located", ignore=("Pharmacy", "PHARMAC", "PHARMACY")),
    "pharmacy_food_register": [loc("Pharmacy", "Shoppers Drug Mart and Rexall, typed as "
                                               "convenience stores, by name")],
    "health_food": [loc("Food shop", "health-food shops typed as supermarkets or convenience "
                                     "stores (Goodness Me!)")],
    "mobile_unit": [loc("Mobile or at-home unit", "mobile and at-home units, by name"),
                    loc(KW_CAT, "the Mobile Vendor category (preparation premises, carts, "
                                "catering vehicles), by type")],
}


PAL_VENUE = "Recreation venue, club or gaming"
COLUMNS["palma_restauracio"] = {
    **{rid: absent("a restaurant and entertainment register: food premises only") for rid in (
        "funeral", "personal_catchall", "sex_shop", "massage_commercial", "massage_regulated",
        "car_dealer", "petrol_station", "vehicle_repair", "pawnbroker", "vet", "parking",
        "repair", "optician", "health_food", "nonstore", "mobile_unit")},
    "no_counter_food": [
        loc("Catering (no counter)", "the register's Catering type (R1), by type"),
        loc("Institutional canteen", "parish and school bars, clinics' cafeterias, a community "
                                     "centre's canteen, by name")],
    "adult_hostess": [loc("Adult venue", "a whiskeria or a table dance, by name")],
    "gambling": [loc(PAL_VENUE, "bingo halls and casinos, by name")],
    "nightclub": [loc("Bar, café or restaurant", "Discoteca, Sala de festes and Sala de ball, "
                                                 "by type")],
    "lodging": [loc("Hotel", "a bare hotel name, by name")],
    "recreation": [loc(PAL_VENUE, "sports, tennis, padel, riding, golf and nautical clubs, "
                                  "sports centres, pool bars and cinemas, by name")],
    "pharmacy": absent("a restaurant and entertainment register: no pharmacies"),
    "pharmacy_food_register": absent("a restaurant and entertainment register: no pharmacies"),
}


COLUMNS["sweden_livsmedel"] = {
    **{rid: absent("a food-control register: food premises only") for rid in (
        "funeral", "personal_catchall", "adult_hostess", "sex_shop", "massage_commercial", "massage_regulated",
        "car_dealer", "vehicle_repair", "pawnbroker", "vet", "parking", "repair", "optician",
        "gambling", "lodging")},
    # Vending machines out by name in the module since 2026-10-01 (owner, call
    # C2; Göteborg's 24Seven Vending and SmartVend 24/7).
    "nonstore": [loc(_se("Detaljhandel", "SmartVend 24/7"), "vending machine, by name")],
    "recreation": absent("a food-control register; 'gymnasi' in its name filter is a secondary school",
                         ignore=("skola|förskola|skolan|gymnasi|fritids|äl",)),
    "pharmacy": absent("a food-only register: its pharmacies fall under pharmacy_food_register"),
    "no_counter_food": [
        loc(_se(REST, "Axfood personalmatsal"), "staff canteen, by name"),
        loc(_se(REST, "Engelbrektsskolan"), "school kitchen, by name"),
        fixed(_se(REST, "Westers Catering"), "caterer typed as a restaurant", "Food service", "2026-09-29",
                CATERING_BRANCH),
        pending(_se("Detaljhandel", "Likajs Frukt & Grönt, torghandel"), "market-square stall", "Retail",
                "2026-09-29", "a torghandel stall stays Retail; the rule takes street and market stalls out")],
    "nightclub": absent("no separate type: clubs' bars are typed as restaurants"),
    "petrol_station": [loc(_se("Detaljhandel", "Circle K Roslagstull"), "forecourt shop")],
    "pharmacy_food_register": [loc(_se("Detaljhandel", "Kronans Apotek Järva"), "pharmacy, by name")],
    "health_food": [loc(_se("Detaljhandel", "Hälsokosten Vällingby"), "health-food shop")],
    "mobile_unit": [fixed(_se(REST, "Tommys Farstaplan, Food truck"), "food truck typed as a restaurant",
                          "Food service", "2026-09-29", CATERING_BRANCH)],
}

OTTAWA = "Ottawa built on Ottawa Public Health's inspection feed"
OTTAWA_ONE_LAYER = ("the feed has no type field, so food shops share the one Food service layer, "
                    "labelled 'Restaurants and food shops' (owner, 2026-09-29): kept, not out")
COLUMNS["ottawa_inspection"] = {
    **{rid: absent("a food-safety inspection register: food premises only") for rid in (
        "personal_catchall", "adult_hostess", "sex_shop", "massage_commercial", "massage_regulated",
        "car_dealer", "vehicle_repair", "gambling", "pawnbroker", "vet", "nonstore", "parking", "repair",
        "optician")},
    "funeral": [loc("Lodging or funeral home", "funeral homes, by name")],
    "no_counter_food": [
        loc("Institutional kitchen", "schools, care homes, staff cafeterias, contract and event caterers, "
                                     "by name")],
    "mobile_unit": [loc("Mobile or event vendor", "food trucks and special-event vendors")],
    "lodging": [loc("Lodging or funeral home", "hotels' breakfast rooms and banquet kitchens, B&Bs")],
    "recreation": [loc("Club or recreation venue", "golf, curling and yacht clubs, Legion halls, arenas")],
    "nightclub": [loc("Food premises", "bars and clubs inspected for food")],
    "petrol_station": [exception("Food premises", "forecourt shops inspected for food (Petro-Canada, "
                                 "Shell Select)", "Food service", OTTAWA, OTTAWA_ONE_LAYER)],
    "pharmacy_food_register": [exception("Food premises", "pharmacies inspected for food (Shoppers Drug "
                                         "Mart, Rexall)", "Food service", OTTAWA, OTTAWA_ONE_LAYER)],
    "pharmacy": absent("a food-only register: its pharmacies fall under pharmacy_food_register"),
    "health_food": [exception("Food premises", "health-food and bulk shops inspected for food",
                              "Food service", OTTAWA, OTTAWA_ONE_LAYER)],
}


def _sea(naics_code, source="seattle"):
    return {"source": source, "naics": naics_code}


def _kc(category, source="kc_food"):
    return {"source": source, "business_category": category}


# Seattle (Regional): Seattle's and Bellevue's registers on NAICS 2022 (codes
# read from Seattle's layer 2026-10-02), King County food by classification
# and name kind, the Liquor Board's off-premise privileges.
COLUMNS["seattle"] = {
    "funeral": [loc(_sea("812210"), "funeral homes"), loc(_sea("812220"), "cemeteries")],
    "funeral_goods": [loc(_sea("459999"), "all other miscellaneous retailers (monument dealers)")],
    "no_counter_food": [loc(_sea("722310"), "food service contractors"),
                        loc(_sea("722320"), "caterers"),
                        loc(_kc("Catering Operation"), "King County catering operations"),
                        loc(_kc("School Lunch Program"), "school kitchens"),
                        loc(_kc("Institutional kitchen"), "workplace cafeterias, contract caterers, "
                                                          "hospital and campus dining, by name")],
    "personal_catchall": [loc(_sea("812990"), "all other personal services")],
    "tattoo": [loc(_sea("812199"), "other personal care services (tattoo parlours)")],
    "adult_hostess": [loc(_kc("Adult venue"), "a food premises the register's name calls a cabaret")],
    "korean_karaoke_bar": absent("no such trade in these registers"),
    "sex_shop": [loc(_sea("459999"), "all other miscellaneous retailers (sex shops file here)")],
    "massage_commercial": [loc(_sea("812199"), "other personal care services (massage)")],
    "massage_regulated": [loc(_sea("621399"), "offices of all other health practitioners")],
    "car_dealer": [loc(_sea("441110"), "new car dealers"), loc(_sea("441120"), "used car dealers")],
    "petrol_station": [loc(_sea("457110"), "gasoline stations with convenience stores"),
                       loc(_kc("GROCERY STORE - BEER/WINE", "lcb_retail"),
                           "a forecourt shop holding the Liquor Board's grocery privilege")],
    "vehicle_repair": [loc(_sea("811111"), "general automotive repair")],
    "gambling": [loc(_sea("713290"), "other gambling industries")],
    "pawnbroker": absent("no code of its own: NAICS files pawnshops under 522299 with every other "
                         "non-bank lender, as in every NAICS city"),
    "nightclub": [loc(_sea("722410"), "drinking places (nightclubs file here)")],
    "vet": [loc(_sea("541940"), "veterinary services")],
    "nonstore": [loc(_sea("445132"), "vending machine operators (NAICS 2022)"),
                 loc(_sea("457210"), "fuel dealers (NAICS 2022)"),
                 loc(_kc("Vending"), "vending routes and workplace micro-markets, by name")],
    "parking": [loc(_sea("812930"), "parking lots and garages")],
    "repair": [loc(_sea("811210"), "electronic equipment repair")],
    "lodging": [loc(_sea("721110"), "hotels and motels"),
                loc(_kc("Hotel"), "hotels' kitchens, by name"),
                loc(_kc("Bed and Breakfast Operation"), "King County bed and breakfasts")],
    "recreation": [loc(_sea("713940"), "fitness centres"),
                   loc(_kc("Recreation venue or club"), "theatres, cinemas, members' clubs and "
                                                        "airline lounges, by name")],
    "pharmacy": [loc(_sea("456110"), "pharmacies and drug retailers")],
    "pharmacy_food_register": [loc(_kc("Pharmacy"), "pharmacies holding a food permit, by name")],
    "optician": [loc(_sea("456130"), "optical goods retailers")],
    "health_food": [loc(_sea("456191"), "food (health) supplement retailers")],
    "person_licence": absent("no person-held licence type: Seattle and Bellevue license "
                             "businesses, and no personal-services register is used elsewhere"),
    "mobile_unit": [loc(_sea("722330"), "mobile food services"),
                    loc(_kc("Mobile Food Unit"), "King County mobile food units")],
}


COLUMNS["minneapolis_inspection"] = {
    **{rid: absent("a food-inspection register: food facilities only") for rid in (
        "funeral", "personal_catchall", "sex_shop", "massage_commercial", "massage_regulated",
        "car_dealer", "vehicle_repair", "gambling", "pawnbroker", "vet", "parking", "repair",
        "optician")},
    "no_counter_food": [
        loc("CATERER", "caterers, by the register's own type"),
        loc("INSTITUTION", "schools, childcare and care homes, by type"),
        loc("Institutional kitchen", "contract caterers' workplace cafes, hospital, school, church and "
                                     "campus dining, event caterers, commissary kitchens, by name")],
    "adult_hostess": [loc("Adult venue", "venues the register's own name calls a cabaret")],
    "petrol_station": [loc("GROCERY", "forecourt shops licensed as groceries (Holiday Stationstore)")],
    "nightclub": [loc("RESTAURANT", "bars and clubs licensed for food")],
    "nonstore": [loc("Vending", "vending routes (Canteen Vending), by name")],
    "lodging": [loc("Hotel", "hotels' kitchens and pantry shops, by name"),
                loc("BOARD AND LODGING", "board and lodging houses, by type")],
    "recreation": [loc("Recreation venue or club", "theatre, cinema, arena and bowling concessions, "
                                                   "event centres, gyms, private clubs, by name")],
    "pharmacy": absent("a food-only register: its pharmacies fall under pharmacy_food_register, "
                       "which is where the module's pharmacy strings are located",
                       ignore=("Pharmacy", r"\bPHARMACY\b")),
    "pharmacy_food_register": [loc("Pharmacy", "pharmacies licensed as groceries, by name")],
    "health_food": [loc("GROCERY", "health-food shops licensed as groceries (General Nutrition Center)")],
    "mobile_unit": [loc("FOOD TRUCK", "food trucks"), loc("FOOD CART", "food carts"),
                    loc("LIMITED MOBILE", "limited mobile units"),
                    loc("MRKTVENDOR", "a farmers' market vendor"), loc("VENDOR", "vendors")],
}


PGH_VENUE, PGH_OTHER = "Recreation venue, casino or club", "OTHER CATEGORY"
COLUMNS["pittsburgh_inspection"] = {
    **{rid: absent("a food-facility register: food premises only") for rid in (
        "funeral", "personal_catchall", "sex_shop", "massage_commercial", "massage_regulated",
        "car_dealer", "vehicle_repair", "pawnbroker", "vet", "parking", "repair", "optician")},
    "no_counter_food": [
        loc(PGH_OTHER, "caterers and transient caterers (100, 101), institutional kitchens (4xx), "
                       "school kitchens (6xx), commissaries (120, 121), by type"),
        loc("Institutional kitchen", "workplace micro-markets (Market C), contract caterers, hospital "
                                     "and campus outlets, employee cafeterias, by name")],
    "adult_hostess": [loc("Adult venue", "a '... Cabaret' that is not a theatre, a gentlemen's club, "
                                         "by name")],
    "gambling": [loc(PGH_VENUE, "Rivers Casino's outlets, by name")],
    "petrol_station": [loc("FOOD SHOP", "forecourt shops (Sunoco, GetGo) licensed as convenience stores")],
    "nightclub": [loc("RESTAURANT", "bars and clubs licensed as restaurants with liquor")],
    "nonstore": [loc("Nonstore or vending", "delivery-only stores (goPuff, DashMart) and vending, by name")],
    "lodging": [loc("Hotel back of house", "hotels' main and banquet kitchens, employee cafes, club "
                                           "lounges, by name"),
                loc(PGH_OTHER, "rooming and boarding houses with guest food service (3xx), by type")],
    "recreation": [loc(PGH_VENUE, "stadium, arena, events-centre, zoo, museum, theatre, cinema, "
                                  "bowling and golf outlets, by name"),
                   loc(PGH_OTHER, "social clubs (250) and pool snack bars (708), by type")],
    "pharmacy": absent("a food-only register: its pharmacies fall under pharmacy_food_register, "
                       "which is where the module's pharmacy strings are located",
                       ignore=("Pharmacy", "PHARMAC", "PHAMAC", r"^RITE AID\b", r"^CVS\b",
                               r"^WALGREENS\b")),
    "pharmacy_food_register": [loc("Pharmacy", "pharmacies licensed as packaged-food shops, by name")],
    "health_food": [loc("FOOD SHOP", "health-food shops licensed as packaged food (GNC)")],
    "mobile_unit": [loc(PGH_OTHER, "mobile tiers I and II (119, 123), by type")],
}


# ---------------------------------------------------------------------------
def _dh(type_bedrijf, source="permit"):
    return {"source": source, "type_bedrijf": type_bedrijf}


COLUMNS["den_haag_source"] = {
    **{rid: absent(BAG_LUMPED) for rid in (
        "sex_shop", "massage_commercial", "massage_regulated", "car_dealer", "petrol_station",
        "vehicle_repair", "pawnbroker", "vet", "nonstore", "parking", "repair", "pharmacy",
        "optician", "mobile_unit")},
    "funeral": [loc(_dh("begraafplaats en crematorium"), "a cemetery and crematorium's horeca")],
    "no_counter_food": [loc(_dh("kantine"), "staff and care-home canteens"),
                        loc(_dh("sportkantine"), "sports-club canteens"),
                        loc(_dh("cateringsbedrijf"), "caterers")],
    "personal_catchall": [loc(_dh("zalenverhuur"), "hall hire"),
                          loc(_dh("partycentrum"), "party centres")],
    "adult_hostess": [loc(_dh("seksinrichting"), "sex businesses the register names")],
    "gambling": [loc(_dh("casino"), "casino"), loc(_dh("speelautomatenhal"), "gaming-machine hall")],
    "nightclub": [loc(_dh("discotheek"), "disco"), loc(_dh("nachtclub"), "nightclub"),
                  loc(_dh("café-discotheek"), "café with a dance floor")],
    "lodging": [loc(_dh("hotel"), "hotel"), loc(_dh("hotel-restaurant"), "a hotel's restaurant"),
                loc(_dh("bed & breakfast"), "bed and breakfast")],
    "recreation": [loc(_dh("theaterfoyer"), "theatre foyers"),
                   loc(_dh("bowlingcentrum"), "bowling"), loc(_dh("amusementshal"), "amusement hall"),
                   loc(_dh("poolbiljart"), "pool hall"), loc(_dh("sportschool"), "gym")],
}


ZURICH_REGISTER = "a register of food-and-drink and alcohol-retail licences: no such licence type"
COLUMNS["zurich_gastwirtschaft"] = {
    **{rid: absent(ZURICH_REGISTER) for rid in (
        "funeral", "personal_catchall", "sex_shop", "massage_commercial", "massage_regulated", "car_dealer",
        "vehicle_repair", "gambling", "pawnbroker", "vet", "nonstore", "parking", "repair", "lodging",
        "recreation", "pharmacy", "optician")},
    "no_counter_food": [loc("Kantine / Mensa", "staff and institutional canteens"),
                        loc("Ausgabestelle", "food stands, caterers and food trucks (the city's own gloss)")],
    "adult_hostess": [loc("Cabaret / Nachtclub", "cabarets, named as such by the register")],
    "nightclub": [loc("Dancing / Disco", "clubs and discos")],
    "petrol_station": [loc("Tankstelle", "petrol-station shops licensed to sell alcohol")],
    "mobile_unit": [loc("Ausgabestelle", "food trucks, filed with stands and caterers")],
}


# PENDING, BY STATE. The owner ruled on the 2026-09-29 list: every pending row
# is an approved fix queued for one batch (docs/handoff_category_fixes_2026-09-29.md),
# except the cells below, which still wait on the owner. A queued row turns stale
# (and fails) when its fix lands: make it a loc() in the same change.
# ---------------------------------------------------------------------------
# Empty since 2026-09-30: the owner ruled on the last four (Boston's GOP
# licences, Buffalo's fuel devices and dance halls, Sacramento's ENTERTAINMENT)
# after they were counted - each is now an exception() with its reason.
# D.C.'s Beauty Booth: found when the person_licence rule was added (2026-10-02).
AWAITING_OWNER = {("dc_businessactivity", "person_licence")}
QUEUED = "fix approved (owner, 2026-09-29), queued: docs/handoff_category_fixes_2026-09-29.md"
QUEUED_ELSEWHERE = {
    ("sweden_livsmedel", "no_counter_food"): "the torghandel stall: a name rule, now that "
                                             "stockholm-catering has landed",
}
for _system, _col in COLUMNS.items():
    for _rid, _cell in _col.items():
        for _e in (_cell if isinstance(_cell, list) else [_cell]):
            if _e.kind == "pending":
                _e.queued = (None if (_system, _rid) in AWAITING_OWNER
                             else QUEUED_ELSEWHERE.get((_system, _rid), QUEUED))


# ---------------------------------------------------------------------------
# PER-TAXONOMY HOOKS
# ---------------------------------------------------------------------------
# The key a bare-string row goes under, where classify() reads a code column
# rather than VALUE_COLUMN's display label.
ROW_KEY = {
    "scian": "scian",
    "france_naf": "naf_code",
    "norway_sn2025": "sn2025_code",
    "denmark_db25": "db25_code",
    "czech_nace2025": "nace2025_code",
    "taiwan_fia": "industry_code",
    "hong_kong_fehd": "licence_code",
    "anzsic_fes": "ClassificationCode",
}

# Brazil's step 2 classifies the free-text description; classify() reads back the stored bucket.
CLASSIFY_VIA = {
    "brazil_cnefe": lambda mod, row: mod.classify_description(row["DSC_ESTABELECIMENTO"])[1],
}

# Helper modules whose string constants are the taxonomy's vocabulary (property F).
EXTRA_SOURCES = {
    "taiwan_fia": ("pipeline/countries/taiwan.py",),
}


def resolved_columns():
    """COLUMNS with every bare cell wrapped in a list - what the check reads."""
    out = {}
    for system, col in COLUMNS.items():
        out[system] = {rid: (cell if isinstance(cell, list) else [cell]) for rid, cell in col.items()}
    return out
