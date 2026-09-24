"""Denmark: the facts shared by every Danish city, measured 2026-09-24.

Profiled for Copenhagen, the first Danish city, off TWO national registers,
both distributed by Datafordeler under CC BY 4.0 and both reached with ONE
free account and API key - the owner's, read from the environment and never
written anywhere:

  * Businesses - CVR, Det Centrale Virksomhedsregister. **The production unit
    (`Produktionsenhed`, a P-enhed), not the company.** A P-unit is a place
    where business is carried on and has its own `beliggenhedsadresse`,
    distinct from any `postadresse` (2,800,921 rows against 928 nationally).
    That distinction is Denmark's answer to this project's core question, as
    `beliggenhetsadresse` was Norway's.
  * Coordinates - DAR, Danmarks Adresseregister, credit Klimadatastyrelsen.
    **A JOIN, not a geocode.** CVR's `Adressering.Adresse` is a DAR Adresse id
    (199 of 200 sampled resolved as one, 2026-09-24), and DAR carries the
    point two hops away: Adresse -> Husnummer -> Adressepunkt.

**CVR IS NORMALISED: ONE FILE PER ENTITY, JOINED ON `CVREnhedsId`.**
`Produktionsenhed` alone holds a `pNummer` and nothing a map can use; the
address, the activity and the name each live in their own national file. The
join key is `CVREnhedsId`, which `Produktionsenhed` calls `id`. ⚠ `pNummer` is
NOT the key - it appears in no other file, and joining on it fails partially
and silently.

**NOT DAWA.** Denmark's keyless address API closes on 1 October 2026 at
10:00 (Klimadatastyrelsen, notice of 2 July 2026). The brief planned on it;
this module does not.

**The ONLY gated CVR entity is `CVRPerson`**, which needs MitID Erhverv and an
access request. This project never asks for it: the restriction runs with the
privacy invariant, not against it.
"""
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
# ONE CACHE FOR THE COUNTRY, as France's and Norway's: CVR's files are
# national (2.1 GB for the four the join needs) and would otherwise be copied
# per city. DAR's are per kommune but shared too, so a second city whose
# scope overlaps reuses them.
SHARED_RAW = _ROOT / "data" / "denmark" / "raw"
CVR_DIR = SHARED_RAW / "cvr"
DAR_DIR = SHARED_RAW / "dar"
MANIFEST_JSON = SHARED_RAW / "manifest.json"

# --- Datafordeler file download -------------------------------------------
#
# Documented at confluence.kds.dk/x/CVUPCQ, read 2026-09-24. The listing is
# v2.0 and the download v1.0 - that is the documentation's own pairing, not a
# typo. The key is a QUERY PARAMETER, so a built URL is a secret: nothing may
# print one, and an error body is scrubbed of the key before it is shown.
API_KEY_ENV = "DATAFORDELER_API_KEY"
LIST_URL = "https://api.datafordeler.dk/FileDownloads/v2.0/GetAvailableFileDownloads"
GET_URL = "https://api.datafordeler.dk/FileDownloads/v1.0/GetFile"

# ⚠ A GENERATION LIVES SEVEN DAYS. Full downloads are generated weekly, "natten
# til lørdag" 03:00-06:00 Danish time, and kept for 7 days. So the files must
# be fetched as ONE generation: a join across two generations silently loses
# every unit created or closed in between. fetch_sources refuses a mixed set.
# The steps do NOT refuse an old generation - retention is how long the
# publisher keeps a file, not a window in which its content is valid, and an
# expiry check would fail every drift check a week after each fetch.

# --- CVR ------------------------------------------------------------------
CVR_REGISTER = "CVR"
# The four the join needs, and the two the sole-trader guard needs.
CVR_ENTITIES = ("Produktionsenhed", "Adressering", "Branche", "Navn",
                "Virksomhed", "Virksomhedsform")

# Every CVR row is a version. "current" downloads still carry superseded rows
# (CVR inserts, it does not overwrite), so a row counts only while its
# `virkningTil` is empty - Prague's DDATZAN, again.
VALID_TO = "virkningTil"
JOIN_KEY = "CVREnhedsId"
PE_ID = "id"                                   # Produktionsenhed's name for it
PE_PARENT_CVR = "tilknyttetVirksomhedsCVRNummer"
PE_CLOSED = "produktionsenhedOphoersdato"

LOCATION_USE = "beliggenhedsadresse"            # AdresseringAnvendelse
ADR_KOMMUNE = "CVRAdresse_kommunekode"          # unpadded: "101", not "0101"
ADR_DAR_ID = "Adresse"
ADR_COLUMNS = ("AdresseringAnvendelse", JOIN_KEY, ADR_DAR_ID, ADR_KOMMUNE,
               "CVRAdresse_vejnavn", "CVRAdresse_husnummerFra",
               "CVRAdresse_postnummer", "CVRAdresse_etagebetegnelse", VALID_TO)

# ⚠ NEVER `coNavn`. Adressering carries a c/o name on 25% of Copenhagen's
# storefront rows - a person, usually, and in no other city's register, so no
# existing check would notice it. Step 2 reads by `usecols` and ASSERTS it
# never arrived. The contact entities (Telefonnummer, e-mailadresse,
# Telefaxnummer) are never downloaded at all.
FORBIDDEN_COLUMNS = ("coNavn",)

# The hovedbranche is `sekvens` 0. A unit carries up to four branches; any
# other sekvens counts a multi-branche premises more than once.
MAIN_BRANCH_SEQ = "0"

# ⚠ THE PRIVACY GUARD LIVES ON THE PARENT COMPANY, as in France and Norway. A
# production unit has no legal form of its own; its parent's `Virksomhedsform`
# says whether it is a person trading. Codes read off the file 2026-09-24,
# with their share of Copenhagen's 15,847 storefronts:
#
#     10  Enkeltmandsvirksomhed               5,424  34.2%   a person
#     15  Personligt ejet Mindre Virksomhed     692   4.4%   a person
#     80  Anpartsselskab                      7,821  49.4%
#     60  Aktieselskab                        1,224   7.7%
#     30  Interessentskab                       334   2.1%   partners liable
#                                                            personally
#
# ✅ INTERESSENTSKAB IS IN TOO - owner's call 2026-09-24, and a deliberate
# difference from Norway, whose guard is ENK alone. An I/S's partners are
# liable personally and without limit, and of Copenhagen's 326 I/S
# storefronts about 105 display names that could be the partners' own - full
# personal names joined by "&", or a bar's name followed by its partners'.
# Cost: ~300 more pins show an address, some of them ordinary shop names.
SOLE_TRADER_FORMS = ("10", "15", "30")

# Denmark's sole-trader MARKER in a name: "v/" - "ved", by - followed by the
# person ("FISKEFORRETNINGEN V/LARS ..."). A second guard, applied whatever the
# parent's form: 7.3% of Copenhagen's storefront names carry it, nearly all on
# form 10, and the rest on partnerships and foreign firms the form test misses.
SOLE_TRADER_MARKER = r"(?i)(?:^|[\s,])v/"

# Legal-form tails stripped from a displayed trade name ("PAW SOCIETY ApS" ->
# "PAW SOCIETY"). Only as a WHOLE final token.
LEGAL_FORM_SUFFIXES = ("APS", "A/S", "I/S", "IVS", "K/S", "P/S", "SMBA", "AMBA",
                       "FMBA", "S.M.B.A", "A.M.B.A", "F.M.B.A")

# --- DAR ------------------------------------------------------------------
DAR_REGISTER = "DAR"
DAR_ENTITIES = ("Adresse", "Husnummer", "Adressepunkt")
# The columns, read off the files 2026-09-24. Every DAR object is keyed on
# `id_lokalId`; a row counts only while BOTH `registreringTil` and
# `virkningTil` are empty (DAR is bitemporal even in a "current" download).
DAR_ID = "id_lokalId"
DAR_STATUS = "status"
DAR_REG_TO = "registreringTil"
DAR_VALID_TO = "virkningTil"
DAR_ADRESSE_HUSNUMMER = "husnummer"       # Adresse -> Husnummer
DAR_HUSNUMMER_POINT = "adgangspunkt"      # Husnummer -> Adressepunkt
DAR_POSITION = "position"                 # Adressepunkt's WKT point
# DAR's status codes: 3 gældende (in force) first, then 2 foreløbig
# (provisional); 4 nedlagt and 5 henlagt only if nothing better exists.
DAR_STATUS_RANK = {"3": 0, "2": 1, "4": 2, "5": 3}

# DAR ships ETRS89 / UTM 32N NATIONALLY, Copenhagen included, though the city
# lies in zone 33 - the object catalogue's example is POINT(552412.26
# 6179535.68). Read the CRS off the data, never off the city's zone.
DAR_CRS = "EPSG:25832"

# --- OSM kommune boundaries ------------------------------------------------
# Danish kommuner are admin_level 7 in OSM and carry the kommunekode as `ref`,
# unpadded ("101"), measured 2026-09-24 on all 35 in the capital-region bbox.
# Swedish kommuner in the same bbox carry `ref:scb` as well, which is how they
# are told apart.
OSM_KOMMUNE_LEVEL = "7"
