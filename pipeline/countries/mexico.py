"""Mexico: the facts shared by every Mexican city, measured across two.

Everything here was verified identical for Ciudad de México (entidad 09,
462,732 units) and Jalisco (entidad 14, 401,813). Nothing here is asserted from
one city - that was the point of waiting for the second.

Sources, both keyless:
  * Businesses - INEGI DENUE, bulk CSV per entidad federativa. No token, no
    CAPTCHA, no rate gate. The DENUE *API* at /app/api/denue/v1/consulta/ 404s
    without a token and is less complete, so it is not used.
  * Rail - OpenStreetMap via Overpass, because neither Mexican city has a
    usable agency feed: Mexico City's hosts are unreachable and Guadalajara's
    only feed expired 2023-01-28 and predates Línea 4. See
    .claude/skills/osm-rail/ before adding a third.
"""

# --- DENUE: the national business register ---------------------------------

# Per entidad federativa. `state_code` is the two-digit INEGI key - 09 Ciudad
# de México, 14 Jalisco, 19 Nuevo León - and is the ONE part of the download
# that is per city.
DENUE_URL_TEMPLATE = (
    "https://www.inegi.org.mx/contenidos/masiva/denue/denue_{state_code}_csv.zip"
)
# The member inside the ZIP. Note the trailing underscore before `.csv`: it is
# in INEGI's own naming and is not a typo.
#
# THE ZIP ALSO CONTAINS A PLAUSIBLE NEAR-MISS. `diccionario_de_datos/
# denue_diccionario_de_datos.csv` parses cleanly as CSV and returns 43 rows of
# column documentation - which looks like a very small city rather than an
# error. Name the member explicitly; never take the first .csv in the archive.
DENUE_MEMBER_TEMPLATE = "conjunto_de_datos/denue_inegi_{state_code}_.csv"

# LATIN-1, NOT UTF-8. A UTF-8 decode raises on both states. Declared rather
# than sniffed, per add-city.
SOURCE_ENCODING = "latin-1"

# DENUE's own column names, identical across entidades.
DENUE_NAME_COLUMN = "nom_estab"        # the exterior sign - see the note below
DENUE_ACTIVITY_COLUMN = "nombre_act"   # -> the taxonomy's VALUE_COLUMN
DENUE_CODE_COLUMN = "codigo_act"       # -> `scian`, what classify() reads
DENUE_STATE_COLUMN = "cve_ent"
DENUE_MUNICIPIO_COLUMN = "municipio"

# SCIAN, via pipeline/taxonomies/scian.py. NOT naics.py: SCIAN numbers retail
# 46 where NAICS uses 44-45, so naics.py would match nothing under 44/45 and
# leave ~46% of a DENUE file unclassified.
TAXONOMY_SYSTEM = "scian"
RAW_CLASSIFICATION_COLUMN = "scian_actividad"

# --- Premises type: a filter no non-Mexican city here has needed ------------
#
# DENUE distinguishes `Fijo` from `Semifijo` - a semi-fixed stall or street
# post rather than a storefront. Measured: Ciudad de México 95.55% Fijo,
# Jalisco 97.94%. This project maps storefronts, so Semifijo is excluded on the
# same reasoning that excludes nonstore retail everywhere - a scope decision,
# stated on each city page and in docs/excluded_categories.md rather than
# applied silently, because street commerce is a real part of Mexican retail
# and this map does not show it.
PREMISES_TYPE_COLUMN = "tipoUniEco"
PREMISES_TYPE_KEEP = "Fijo"

# --- Privacy: INEGI did the work, and this is why the claim is structural ---
#
# NEVER LOADED, and each city's step 2 asserts they never arrive - New York's
# pattern, which is what lets a city claim structurally that no pin can be a
# registrant's name.
#
#   telefono    35.6% populated in CDMX - a phone number at a sole trader's
#               premises
#   correoelec  22.6% - likewise an email
#   www         10.6%
#   raz_social  25.9% - the legal entity name. INEGI ALREADY omits it when the
#               owner is a persona física, and says so in its own data
#               dictionary: "el dato no se incluye para proteger la
#               confidencialidad de la información". So what remains is
#               corporate. It is still not loaded, because `nom_estab` is
#               populated on 99.95% of rows and is defined as the name
#               "visible y escrito en rótulos, fachadas o anuncios luminosos"
#               - the shopfront sign. Los Angeles published ~4,000
#               individuals' names by falling back to an owner column when a
#               trade name was blank; forbidding the column removes the
#               mechanism rather than relying on the fallback never firing.
FORBIDDEN_COLUMNS = ("telefono", "correoelec", "www", "raz_social")

# Structured interior/unit number. Loaded and MEASURED by each city's step 2,
# and deliberately NOT written to the output: publishing a unit number in order
# to check for unit numbers would defeat the purpose. Measured 13.4% in Ciudad
# de México, 7.1% in the Guadalajara region. scripts/check_personal_exposure.py
# therefore records both cities' residence check as a GAP, the way San Diego's
# and Boston's are recorded, rather than as a pass.
DENUE_INTERIOR_COLUMN = "numero_int"

# --- OpenStreetMap ----------------------------------------------------------
#
# More than one host, tried in order. Measured over this build: overpass-api.de
# returned 504 on several requests and 429 on one, kumi.systems 504 on several,
# osm.ch answered 200 with an EMPTY body once - all at different times, for the
# same query. A failure is a fact about that host, not about the city, so a
# caller must try the others and must not cache an empty 200.
OVERPASS_HOSTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
)
OVERPASS_USER_AGENT = (
    "expanded-heatmap city profiling (github.com/dacekroberts/expanded-heatmap)"
)

# Entrances are never stations - 447 of them against 184 stations in Mexico
# City, 114 in Guadalajara. Proposed and construction are never stations
# either, and `prpopsed` is in this list because five real OSM nodes are
# spelled that way: a blacklist misses a typo, which is why each city's step 1
# WHITELISTS what it wants and this tuple exists only to be printed as a
# record of what was dropped.
OSM_NEVER_A_STATION = ("subway_entrance", "proposed", "construction", "prpopsed")


def denue_url(state_code):
    """Bulk DENUE download URL for an entidad federativa."""
    return DENUE_URL_TEMPLATE.format(state_code=state_code)


def denue_member(state_code):
    """The data member inside that entidad's ZIP."""
    return DENUE_MEMBER_TEMPLATE.format(state_code=state_code)


# --- Required notices, for docs/data_sources.md's gate ----------------------
#
# INEGI's Términos de Libre Uso permit publishing, adapting, extracting and
# COMMERCIAL use (§1b-e) in exchange for three things, and the second is the
# one a source credit does not discharge:
#
#   §1(f)  prescribed attribution: "Fuente: INEGI, <product>" plus the update
#          date.
#   §1(g)  DISCLOSURE of any analysis or transformation, and it must not be
#          presented as INEGI's. This project triggers it on every map - ring
#          assignment, bucketing and the storefront and Fijo filters are all
#          transformations.
#   §1(h)  non-endorsement.
#
# The displayed text lives in app/components.py's _NOTICES, keyed on INEGI
# rather than on a city - which is why Guadalajara became the first city here
# to need no new notice entry at all.
LICENCE_NAME = "Términos de Libre Uso de la Información del INEGI"
LICENCE_STORED_AT = "docs/licenses/inegi-terminos-libre-uso-informacion.pdf"
ATTRIBUTION_PRODUCT = (
    "Fuente: INEGI, Directorio Estadístico Nacional de Unidades Económicas (DENUE)"
)
