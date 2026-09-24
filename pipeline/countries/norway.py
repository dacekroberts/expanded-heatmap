"""Norway: the facts shared by every Norwegian city, measured 2026-09-24.

Profiled for Oslo, the first Norwegian city, off ONE national register - the
Brønnøysund Register Centre's Enhetsregisteret. A second city changes only its
kommune number and its address file, which is France's and Mexico's shape.

Sources, all keyless:

  * Businesses - Enhetsregisteret's SUB-UNITS (`underenheter`), 864,903
    establishments nationally, **NLOD** (Norsk lisens for offentlige data).
    **The sub-unit, not the main unit.** A sub-unit is a place of business and
    carries `beliggenhetsadresse`, its PHYSICAL location, kept deliberately
    distinct from the main unit's registered `forretningsadresse` - that
    distinction is Norway's answer to this project's core question, and the
    reason Norway passed the screen where Czechia's RES did not.
  * Parents - the MAIN UNITS (`enheter`), joined on `overordnetEnhet`, read for
    ONE purpose: the legal form, which is where a sole trader (`ENK`) shows.
  * Coordinates - Kartverket's Matrikkelen Adresse, per kommune, CC BY 4.0.
    **A JOIN, not a geocode.** The brief planned ~13,000 calls to Kartverket's
    search API; the bulk file makes it a dictionary lookup, deterministic
    across drift checks, with no `fuzzy=true` trap to fall into.

**The CSV distributions, not the JSON.** Brønnøysund publishes both; the CSV
is 61 MB against the JSON's 89 MB for sub-units, and pandas reads only the
columns a step names - which is how the contact columns below are never loaded.
"""
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
# ONE CACHE FOR THE COUNTRY, as France's: the two register files are national
# (61 MB and 155 MB gzipped) and would otherwise be duplicated per city.
SHARED_RAW = _ROOT / "data" / "norway" / "raw"
SUBUNITS_CSV_GZ = SHARED_RAW / "underenheter.csv.gz"
UNITS_CSV_GZ = SHARED_RAW / "enheter.csv.gz"

SUBUNITS_URL = "https://data.brreg.no/enhetsregisteret/api/underenheter/lastned/csv"
UNITS_URL = "https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv"

# Kartverket's address file, per kommune. `{code}` and `{name}` are the
# kommune's number and name as Geonorge spells them (`0301`, `Oslo`).
# EPSG 4258 is ETRS89 geographic: within a metre of WGS84 at this latitude,
# so its Nord/Øst are read as lat/lon directly.
ADDRESS_URL_TEMPLATE = (
    "https://nedlasting.geonorge.no/geonorge/Basisdata/MatrikkelenAdresse/CSV/"
    "Basisdata_{code}_{name}_4258_MatrikkelenAdresse_CSV.zip")

# Kartverket's municipal boundary, one kommune per call, GeoJSON geometry -
# dataset "Administrative enheter kommuner", CC BY 4.0. api.kartverket.no is
# the endpoint Kartverket recommends since December 2023; the older
# ws.geonorge.no path is kept "inntil videre" as a proxy. Compared 2026-09-24
# for 0301 and 3201: identical geometry, zero symmetric difference.
KOMMUNE_BOUNDARY_URL_TEMPLATE = (
    "https://api.kartverket.no/kommuneinfo/v1/kommuner/{code}/omrade")

# --- The sub-unit columns a step may read ----------------------------------
#
# ⚠ NEVER epostadresse, telefon or mobil. The CSV carries all three, and a
# contact detail on a public pin is a worse exposure than a name - a direct
# line to a person (the 2026-09-21 finding, a New York licence registered under
# a Gmail address). Step 2 reads by `usecols` and ASSERTS none of them arrived.
SUB_ID = "organisasjonsnummer"
SUB_NAME = "navn"
SUB_CODE = "naeringskode1.kode"
SUB_LABEL = "naeringskode1.beskrivelse"
SUB_EMPLOYEES_FLAG = "harRegistrertAntallAnsatte"
SUB_ADDRESS = "beliggenhetsadresse.adresse"
SUB_POSTCODE = "beliggenhetsadresse.postnummer"
SUB_KOMMUNE = "beliggenhetsadresse.kommunenummer"   # the per-city variable
SUB_PARENT = "overordnetEnhet"
SUB_CLOSED = "nedleggelsesdato"
SUB_COLUMNS = (SUB_ID, SUB_NAME, SUB_CODE, SUB_LABEL, SUB_EMPLOYEES_FLAG,
               SUB_ADDRESS, SUB_POSTCODE, SUB_KOMMUNE, SUB_PARENT, SUB_CLOSED)
FORBIDDEN_COLUMNS = ("epostadresse", "telefon", "mobil", "hjemmeside",
                     "postadresse.adresse")

# ⚠ THE FILTER IS THE LOCATION ADDRESS'S KOMMUNE, NEVER THE API'S. The paged
# API's `?kommunenummer=0301` does not constrain `beliggenhetsadresse` - its
# misses included Bergen, Copenhagen, Paris and Malmö (the brief's correction).

# --- The main-unit columns -------------------------------------------------
UNIT_ID = "organisasjonsnummer"
UNIT_FORM = "organisasjonsform.kode"
UNIT_BANKRUPT = "konkurs"
UNIT_WINDING_UP = "underAvvikling"
UNIT_FORCED_WINDING_UP = "underTvangsavviklingEllerTvangsopplosning"
UNIT_COLUMNS = (UNIT_ID, UNIT_FORM, UNIT_BANKRUPT, UNIT_WINDING_UP,
                UNIT_FORCED_WINDING_UP)

# ⚠ THE PRIVACY GUARD LIVES ON THE PARENT. A sub-unit's own
# `organisasjonsform` is BEDR or AAFY on 100% of rows and NEVER ENK, because
# those are sub-unit forms - a complete, populated field that answers a
# different question. The sole trader is visible only on the main unit: the
# same shape as France, where `categorieJuridiqueUniteLegale` lives on the
# unité légale and never on the établissement.
SOLE_TRADER_FORM = "ENK"   # enkeltpersonforetak - SUPPRESS the name

# Legal-form tails stripped from a displayed trade name: "1 ØRE AS" is a
# perfectly good trade name once the "AS" goes. Only as a WHOLE final token.
LEGAL_FORM_SUFFIXES = ("AS", "ASA", "ANS", "DA", "SA", "NUF", "BA", "KS",
                       "SE", "IKS", "FLI", "STI")

# Address lines that are not a street address. `beliggenhetsadresse.adresse`
# is a LIST, flattened with newlines in the CSV, whose first line is often a
# c/o or a building name ("Røa Senter", "Steen & Strøm Magasin").
NON_STREET_PREFIXES = ("c/o", "co ", "postboks", "pb ", "pb.")
