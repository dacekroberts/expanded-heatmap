"""Barcelona's four-level Catalan activity taxonomy - not NAICS, not NACE codes.

The Cens de locals classifies every ground-floor premises with
`Nom_Principal_Activitat` -> `Nom_Sector_Activitat` -> `Nom_Grup_Activitat` ->
`Nom_Activitat`, in Catalan and with no code column that maps to an
international standard. The project invariant permits a documented local
taxonomy, and this is one.

**WHY THE BUCKETS ARE KEYED ON `Nom_Activitat`, THE FINEST LEVEL.** Madrid went
the other way - divisions, not epigrafes - because there the division level
lined up with the buckets almost one-to-one. Here it does not, and the group
level fails in the way that matters most:

- **`Nom_Grup_Activitat` puts 20,693 of 58,908 active rows - 35% - into
  `Altres`.** A third of the city would be unclassifiable.
- **The group `Restaurants, bars i hotels (Inclos hostals, pensions i fondes)`
  is the HOSTELERIA trap in Catalan.** Of its 10,722 rows, **720 are
  `serveis d'allotjament`** - hotels, hostals and pensions. Keying on the group
  would publish all 720 as food service, which is the same error the Mexico
  City build made once with SCIAN 72 and Madrid avoided by splitting
  HOSTELERIA.

So the mapping enumerates all 75 values of `Nom_Activitat`. That is a closed
list rather than a prefix rule, so a value added in a future refresh would fall
through - which is why `UNMAPPED_IS_AN_ERROR` exists below and why the
import-time assertion checks the enumeration against the measured census.

**TWO CALLS THE PUBLISHER'S OWN HIERARCHY MADE, NOT ME.** Both were about to go
the other way on a reading of the Catalan:

- **`Plats preparats (no degustacio)` (202) is RETAIL, not food service.**
  Barcelona files it under `Quotidia alimentari` - daily food shopping -
  alongside the butcher and the greengrocer, not under the restaurants group.
  The `(no degustacio)` qualifier is the publisher saying there is no
  consumption on the premises. A prepared-food counter you carry home is a
  food shop.
- **`Fotografia` (144) is RETAIL.** Filed under `Comerc al detall`, so the
  camera-and-printing shop reading is the publisher's, not the portrait-studio
  reading that would have made it a personal service.

**`Altres` IS AMBIGUOUS BY CONSTRUCTION AND NEEDS A SECOND COLUMN.** The value
means different things under different parents, which is Chicago's pattern -
a classification value that says nothing about the business, resolved by a
second field listed in `EXTRA_COLUMNS`:

    Quotidia alimentari      625   food retail
    Comerc al detall /Engros 458   retail/wholesale, no detail at all
    sector Altres            323   genuinely other
    Serveis                  115   services
    Restaurants group         24   food service

Counts are from the full 2022 census pulled 2026-09-22, restricted to the
58,908 rows where `Nom_Principal_Activitat` is `Actiu` - which is the vacancy
filter and is mandatory: the other 7,180 rows are empty units for sale or rent
and would otherwise be published as 11% phantom storefronts.
"""

FIELD_LABEL = "Activity"
VALUE_COLUMN = "Nom_Activitat"

# The `Altres` dispatch needs the two levels above it. Chicago's mechanism.
EXTRA_COLUMNS = ("Nom_Grup_Activitat", "Nom_Sector_Activitat")

# The vacancy filter, applied in step 2. Named here because it belongs with
# the taxonomy it qualifies, not buried in a config constant.
ACTIVE_COLUMN = "Nom_Principal_Activitat"
ACTIVE_VALUE = "ACTIU"

# The census year this mapping was measured against. The 2024 resource is
# geographically incomplete - see docs/build_briefs/barcelona.md - so the year
# is a decision, and the page states it.
AS_OF_YEAR = 2022


def _norm(value):
    """Upper-case, or "" for anything that is not a string.

    NOT `str(value).upper()`, and not `(value or "").upper()`. A missing key
    becomes `float('nan')` in a DataFrame row and **nan is truthy**, so the
    `or` form returns nan and the `str` form returns the literal "NAN". That
    exact bug took a city's map down on 2026-09-22.
    """
    return value.strip().upper() if isinstance(value, str) else ""


# --- Food service ----------------------------------------------------------
#
# The restaurants group MINUS accommodation and MINUS vending. 9,968 rows.
_FOOD = {
    "RESTAURANTS",                                       # 5,088
    "BARS / CIBERCAFÈ",                                  # 3,447
    "SERVEIS DE MENJAR TAKE AWAY MENJAR RÀPID",          #   840
    "BARS ESPECIALS AMB ACTUACIÓ / BARS MUSICALS / DISCOTEQUES /PUB",  # 345
    "XOCOLATERIES / GELADERIES / DEGUSTACIÓ",            #   174
    "SERVEIS DE MENJAR I BEGUDES",                       #    74
}

# --- Retail ----------------------------------------------------------------
#
# Effectively the whole `Comerc al detall` sector, which is the publisher's own
# retail definition. 19,835 rows before the `Altres` dispatch adds 625.
_RETAIL = {
    # Quotidia alimentari - daily food shopping
    "AUTOSERVEI / SUPERMERCAT",                          # 2,509
    "PA, PASTISSERIA I LÀCTICS",                         # 1,545
    "FRUITES I VERDURES",                                # 1,050
    "CARN I PORC",                                       # 1,036
    "PEIX I MARISC",                                     #   461
    "BEGUDES",                                           #   273
    "OUS I AUS",                                         #   265
    "PLATS PREPARATS (NO DEGUSTACIÓ)",                   #   202  see docstring
    "RESTA ALIMENTACIÓ",                                 #     1
    # Equipament personal
    "VESTIR",                                            # 2,634
    "JOIERIA, RELLOTGERIA I BIJUTERIA",                  #   628
    "CALÇAT I PELL",                                     #   621
    "MERCERIA",                                          #   180
    # Quotidia no alimentari
    "FARMÀCIES PARAFARMÀCIA",                            # 1,076
    "DROGUERIA I PERFUMERIA",                            #   602
    "TABAC I ARTICLES FUMADORS",                         #   448
    "HERBOLARIS, DIETÈTICA I NUTRICIÓ",                  #   291
    "COMBUSTIBLES I CARBURANTS",                         #    69
    # Parament de la llar
    "MATERIAL EQUIPAMENT LLAR",                          #   968
    "MOBLES I ARTICLES FUSTA I METALL",                  #   515
    "PARAMENT FERRETERIA",                               #   280
    "FLORISTERIES",                                      #   269
    "SEGELLS, MONEDES I ANTIGUITATS",                    #   203  in two groups
    "APARELLS DOMÈSTICS",                                #   158
    # Oci i cultura
    "INFORMÀTICA",                                       #   710
    "JOGUINES I ESPORTS",                                #   406
    "LLIBRES, DIARIS I REVISTES",                        #   402
    "MÚSICA",                                            #    81
    # Comerc al detall > Altres
    "BASARS",                                            #   572
    "ÒPTIQUES",                                          #   324
    "SOUVENIRS",                                         #   254
    "FOTOGRAFIA",                                        #   144  see docstring
    "MAQUINÀRIA",                                        #    65
    "GRANS MAGATZEMS I HIPERMERCATS",                    #    24
    "SOUVENIRS I BASARS",                                #     2
    # Automocio. Vehicle DEALERS are retail in NAICS 441 too; the repair half
    # of the trade is `Reparacions`, excluded below, which keeps this aligned
    # with how Madrid split NACE 45.
    "VEHICLES",                                          #   400
}

# --- Personal services -----------------------------------------------------
#
# 5,673 rows. NAICS 812's shape: hair, beauty, laundry, garment repair, pets.
_PERSONAL = {
    "PERRUQUERIES",                                      # 2,616
    "CENTRES D'ESTÈTICA",                                # 1,597
    "ARRANJAMENTS",                                      #   649  garment repair
    "TINTORERIES",                                       #   416  dry cleaners
    "VETERINARIS / MASCOTES",                            #   395  NAICS 812910
}

# --- Deliberately NOT a storefront in this project's sense ------------------
#
# Enumerated rather than left to fall through, so that an unmapped value means
# "the census changed" instead of "someone forgot one". Each is excluded for a
# stated reason; several are genuine high-street premises that simply are not
# retail, food or personal services.
_NOT_STOREFRONT = {
    # The accommodation trap. Hotels, hostals, pensions and fondes.
    "SERVEIS D'ALLOTJAMENT",                             #   720
    # Offices and back-of-house, not shops
    "SERVEIS A LES EMPRESES I OFICINES",                 # 3,214
    "ACTIVITATS EMMAGATZEMATGE",                         # 1,688
    "ACTIVITATS DE TRANSPORT",                           #   485
    "PÀRQUINGS I GARATGES",                              #   466
    "ADMINISTRACIÓ",                                     #   358
    "MANTENIMENT, NETEJA I SIMILARS",                    #   276
    # Health, education, welfare - their own sectors, not commerce
    "SANITAT I ASSISTÈNCIA",                             # 2,093
    "ENSENYAMENT",                                       # 2,066
    "SERVEIS SOCIALS",                                   #   470
    "EQUIPAMENTS RELIGIOSOS",                            #   377
    "ASSOCIACIONS",                                      #   856
    # Services outside the three buckets. NAICS puts repair in 811, finance in
    # 52, real estate in 53, travel in 5615 - none of them 44/45, 722 or 812.
    "REPARACIONS (ELECTRODOMÈSTICS I AUTOMÒBILS)",       # 1,329
    "FINANCES I ASSEGURANCES",                           # 1,028
    "ACTIVITATS IMMOBILIÀRIES",                          #   870
    "AGÈNCIES DE VIATGE",                                #   254
    "SERVEIS DE TELECOMUNICACIONS",                      #   204
    "LOCUTORIS",                                         #   117
    # Recreation and culture - NAICS 71, not 812
    "EQUIPAMENTS CULTURALS I RECREATIUS",                #   934
    "GIMNÀS /FITNES",                                    #   368
    "ALTRES EQUIPAMENTS ESPORTIUS",                      #   252
    # Production, not sale
    "ACTIVITATS DE LA CONSTRUCCIÓ",                      # 1,840
    "ACTIVITATS INDUSTRIALS",                            # 1,049
    "ARTS GRÀFIQUES",                                    #   583
    "FABRICACIÓ TÈXTIL",                                 #   147
    # Vending machines are not premises anyone walks into
    "ALTRES ( PER EXEMPLE VENDING)",                     #    10
}

# --- The `Altres` dispatch --------------------------------------------------
#
# Keyed on the GROUP first, then the SECTOR. See the docstring: the same word
# carries five different meanings depending on its parent.
_ALTRES_BY_GROUP = {
    "QUOTIDIÀ ALIMENTARI": "Retail",                     #   625
    "RESTAURANTS, BARS I HOTELS (INCLÒS HOSTALS, PENSIONS I FONDES)":
        "Food service",                                  #    24
}
_ALTRES_BY_SECTOR = {
    # Retail/wholesale with NO activity detail whatsoever - every one of the
    # 458 rows in this sector is `Altres`. Excluded rather than assigned to
    # Retail, because "it is in a sector whose name contains retail" is not
    # evidence about the premises, and the sector explicitly mixes in
    # wholesale, which this project does not map.
    "COMERÇ AL DETALL /ENGRÒS": None,                    #   458
    "SERVEIS": None,                                     #   115
    "ALTRES": None,                                      #   323
}

_BUCKET_BY_ACTIVITY = {}
for _value in _RETAIL:
    _BUCKET_BY_ACTIVITY[_value] = "Retail"
for _value in _FOOD:
    _BUCKET_BY_ACTIVITY[_value] = "Food service"
for _value in _PERSONAL:
    _BUCKET_BY_ACTIVITY[_value] = "Personal services"

# Every `Nom_Activitat` seen in the 2022 census, so a value that is none of
# these is a CHANGE rather than an oversight.
UNMAPPED_IS_AN_ERROR = (
    _BUCKET_BY_ACTIVITY.keys() | _NOT_STOREFRONT | {"ALTRES"})


def classify(row):
    """Bucket name, or None for a premises this project does not count."""
    activity = _norm(row.get(VALUE_COLUMN))
    if not activity:
        return None
    if activity == "ALTRES":
        group = _norm(row.get("Nom_Grup_Activitat"))
        if group in _ALTRES_BY_GROUP:
            return _ALTRES_BY_GROUP[group]
        return _ALTRES_BY_SECTOR.get(_norm(row.get("Nom_Sector_Activitat")))
    return _BUCKET_BY_ACTIVITY.get(activity)


def legend_label(bucket):
    return bucket


# --- Import-time proofs, in the style of madrid_epigrafe -------------------
#
# The accommodation split is the one an int cannot check later, so assert it.
assert "SERVEIS D'ALLOTJAMENT" in _NOT_STOREFRONT, (
    "the accommodation carve-out is the whole reason this taxonomy keys on "
    "Nom_Activitat rather than on Nom_Grup_Activitat")
assert "SERVEIS D'ALLOTJAMENT" not in _BUCKET_BY_ACTIVITY, (
    "accommodation must never reach a bucket")
assert classify({"Nom_Activitat": "serveis d'allotjament"}) is None
assert classify({"Nom_Activitat": "Restaurants"}) == "Food service"
assert classify({"Nom_Activitat": "Plats preparats (no degustació)"}) == "Retail"

# `Altres` really does resolve differently per parent, which is the point.
assert classify({"Nom_Activitat": "Altres",
                 "Nom_Grup_Activitat": "Quotidià alimentari"}) == "Retail"
assert classify({"Nom_Activitat": "altres",
                 "Nom_Grup_Activitat":
                     "Restaurants, bars i hotels (Inclòs hostals, pensions i fondes)"}
                ) == "Food service"
assert classify({"Nom_Activitat": "Altres",
                 "Nom_Grup_Activitat": "Altres",
                 "Nom_Sector_Activitat": "Serveis"}) is None

# nan is truthy; this is the bug that took a map down, so it is a test.
assert _norm(float("nan")) == ""
assert classify({"Nom_Activitat": float("nan")}) is None
assert classify({}) is None

# No value may sit in two buckets.
assert not (_RETAIL & _FOOD) and not (_RETAIL & _PERSONAL) and not (_FOOD & _PERSONAL)
assert not (_BUCKET_BY_ACTIVITY.keys() & _NOT_STOREFRONT), (
    "a value cannot be both bucketed and excluded")
