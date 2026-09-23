"""France: the facts shared by every French city, measured 2026-09-22.

Profiled for six metro cities off ONE national register - Paris, Lyon,
Marseille, Toulouse, Lille, Rennes. Only `COMMUNE_CODES` differs between them,
which is Mexico's shape (`DENUE_STATE_CODE`) rather than Spain's.

Sources, all three keyless and all under Licence Ouverte 2.0:

  * Businesses - INSEE SIRENE `StockEtablissement`, 44,064,115 establishments.
    **The etablissement, not the unite legale.** The `StockUniteLegale` file
    in the same dataset is 30,020,346 LEGAL UNITS keyed on `siren`; mapping it
    would produce the registered-office map this project exists not to make.
  * Coordinates - INSEE's separate geolocation file, 37,901,783 rows keyed on
    `siret`. **A JOIN, not a geocode** - no geocoder, no rate limit, no key.
  * Rail - `transport.data.gouv.fr`, France's National Access Point, which
    aggregates every French operator's GTFS. One source for all six cities.

**Prefer the PARQUET distributions over the ZIPs.** Both files publish both.
Parquet is columnar, so a step reads the ten columns it needs instead of
fifty-four, and its footer can be read over HTTP range requests without
downloading the file - which is how every number in this module was measured.
"""

# --- SIRENE: the national establishment register ---------------------------

# Resolved from the data.gouv.fr API rather than hard-coded, because the file
# name carries its own release date ("01 septembre 2026") and changes monthly.
SIRENE_DATASET_SLUG = (
    "base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret"
)
# The resource TITLE to match inside that dataset. The trailing " -" matters:
# without it this also matches `StockEtablissementHistorique` and
# `StockEtablissementLiensSuccession`, which are different files.
SIRENE_RESOURCE_TITLE_PREFIX = "Sirene : Fichier StockEtablissement -"

GEOLOC_DATASET_SLUG = (
    "geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-"
    "etudes-statistiques"
)
GEOLOC_RESOURCE_TITLE_CONTAINS = "géolocalisation établissements"

# The join. One key, both files.
JOIN_KEY = "siret"

# --- the columns, from the real schema (54 in the stock file) ---------------

# ACTIVE is the letter "A". **NOT the label "Actif".** An earlier pass filtered
# on "Actif" and got ZERO rows for all six cities; it was caught only because
# Paris was run first as a control and a known-good number failed to reproduce.
# Keep the control. See DECISIONS.md, 2026-09-22.
STATE_COLUMN = "etatAdministratifEtablissement"
STATE_ACTIVE_VALUE = "A"

COMMUNE_COLUMN = "codeCommuneEtablissement"   # the ONE per-city variable
NAF_COLUMN = "activitePrincipaleEtablissement"
NAF25_COLUMN = "activitePrincipaleNAF25Etablissement"  # NAF 2025, newer scheme

# The trade name, and why there are two of them. See the naming note below.
ENSEIGNE_COLUMNS = ("enseigne1Etablissement", "enseigne2Etablissement",
                    "enseigne3Etablissement")
USUAL_NAME_COLUMN = "denominationUsuelleEtablissement"

# The registered-office flag. 90.8% of active rows in the three buckets are
# sieges, so this does NOT usefully filter premises from offices in France -
# a sole trader's shop is its own siege. Recorded so nobody tries.
SIEGE_COLUMN = "etablissementSiege"

# Employee-count band. "000" means no employees. The Paris measurement used
# this to go from 148,633 to 50,156.
EMPLOYEE_BAND_COLUMN = "trancheEffectifsEtablissement"

# France masks non-diffusible records AT SOURCE - the name, the address and
# the geolocation - so the privacy work is partly done upstream. 13.4% of
# sampled active bucket rows are masked. `read-licence` step 6b.
DIFFUSION_COLUMN = "statutDiffusionEtablissement"
DIFFUSION_PUBLIC_VALUE = "O"

# --- the geolocation file --------------------------------------------------

# It publishes BOTH a projected pair and a WGS84 pair, 100% populated in the
# sampled row group.
GEO_X_COLUMN = "x"
GEO_Y_COLUMN = "y"
GEO_LAT_COLUMN = "y_latitude"
GEO_LON_COLUMN = "x_longitude"

# **THE CRS IS PER ROW, NOT PER FILE.** The file carries an `epsg` column, and
# a sampled row group held four values: 2154 (Lambert-93, metropolitan France)
# on 99.3%, plus 2975 (Reunion), 5490 (Antilles) and 2972 (Guyane). All six
# cities profiled here are metropolitan and therefore uniformly 2154 - but a
# pipeline that hard-codes 2154 and is later pointed at Fort-de-France would
# put every pin in the sea without erroring. Read the column.
GEO_EPSG_COLUMN = "epsg"
METROPOLITAN_EPSG = 2154

# INSEE's own positional quality code, sampled: 11 (62.5%), 33 (17.6%),
# 12 (15.9%), 22, 21. Lower is better; 33 is commune-centroid class. This is a
# source that reports its own confidence, like Denmark's DAWA `kategori` and
# Hong Kong's ALS `Score` - use it, do not average over it.
GEO_QUALITY_COLUMN = "qualite_xy"
GEO_PRECISION_COLUMN = "distance_precision"

# --- THE NAMING PROBLEM, measured before it could become a build surprise ---
#
# Across 20,103 ACTIVE rows in NAF 47/56/96 sampled from four row groups spread
# through the file:
#
#     enseigne1Etablissement             29.1%
#     enseigne2Etablissement             13.4%
#     denominationUsuelleEtablissement   34.2%
#     EITHER an enseigne or a usual name 42.9%
#     ...of Paris (751xx) rows           38.4%
#
# So roughly SIX IN TEN French storefronts publish no name at the premises
# level. This is Milan's `insegna` trap in another language, and it is recorded
# here rather than discovered at step 2 with a taxonomy already written.
#
# **There is a third file that would close the gap, and it must NOT be used
# blindly.** `StockUniteLegale`, joined on `siren`, carries
# `denominationUniteLegale` for companies - but for a sole trader it carries
# `nomUniteLegale` and `prenomUsuelUniteLegale`, which are A PERSON'S NAME.
# The project's standing invariant is that a trade name is fair game and a
# registrant's own name is not. So: fall back to the legal name ONLY where the
# legal form is a company, never for a natural person, and run
# `scripts/check_personal_exposure.py` before publishing any French city.
NAMING_FILL_MEASURED = {
    "sample_rows": 20103,
    "enseigne1": 0.291,
    "denomination_usuelle": 0.342,
    "any_premises_name": 0.429,
    "paris_any_name": 0.384,
}

# --- the six cities --------------------------------------------------------
#
# `COMMUNE_CODES` is the ONLY field that differs between them. Paris, Lyon and
# Marseille are subdivided into arrondissements, each with its own INSEE
# commune code, so those three are prefix matches rather than single codes.
#
# **VALIDATED 2026-09-22, not asserted.** A wrong prefix returns zero rows and
# fails silently - the same shape as the `"Actif"` bug - so all six were
# counted across 14 row groups (1,735,429 rows, 3.9% of the file) with Paris
# as the control. Every prefix returned non-zero, and Paris scaled to 136,400
# against its independently measured 148,633. The ~8% shortfall is sample
# bias, not prefix error: active bucket rows get denser through the file
# (row group 325 contributed ~12x row group 0), because siret is assigned by
# seniority.
CITY_COMMUNE_PREFIXES = {
    "paris": ("751",),        # 75101-75120
    "lyon": ("6938",),        # 69381-69389
    "marseille": ("132",),    # 13201-13216
    "toulouse": ("31555",),
    "lille": ("59350",),
    "rennes": ("35238",),
}

# Scaled estimates from that same sample, and the per-city naming rate. These
# are ESTIMATES for ordering, not build numbers - each city's Step 0 measures
# its own total. The naming column is the one that matters:
#
# **PARIS IS THE WORST-NAMED OF THE SIX.** The five follower cities all carry
# a premises name on 45-54% of rows against Paris's 42.9%, so the cheap cities
# are also the better data - which inverts the usual assumption that the
# flagship city is the strongest one.
CITY_ESTIMATES = {
    "paris":     {"bucket_rows_est": 136_400, "named": 0.429},
    "marseille": {"bucket_rows_est": 26_940, "named": 0.458},
    "lyon":      {"bucket_rows_est": 19_449, "named": 0.525},
    "toulouse":  {"bucket_rows_est": 12_873, "named": 0.519},
    "lille":     {"bucket_rows_est": 10_461, "named": 0.507},
    "rennes":    {"bucket_rows_est": 5_002, "named": 0.543},
}

# --- rail ------------------------------------------------------------------
#
# `transport.data.gouv.fr/api/datasets` returns 799 datasets, 489 of them
# type `public-transit`, each with GTFS and usually NeTEx.
TRANSPORT_NAP_API = "https://transport.data.gouv.fr/api/datasets"

# Matched on the dataset's OWN title and covered area, never by substring over
# the whole JSON blob: `star` (Rennes), `mel` (Lille) and `tcl` (Lyon) are all
# short enough to match unrelated text, and a first attempt scored Rennes at
# 489 of 799 datasets for exactly that reason.
#
# **AND THE CITY'S NAME IS NOT ENOUGH.** Lille's match also returns "Navettes
# Aeroport de Lille", an airport shuttle - the same wrong-feed trap that had
# Dublin tested against airport coaches. Name the urban operator.
CITY_RAIL_DATASET = {
    "paris": "Réseaux urbains et interurbains d'Île-de-France "
             "Mobilités (IDFM)",
    "lyon": "Réseau urbain TCL",
    "marseille": "Réseaux urbains de la Métropole "
                 "Aix-Marseille-Provence",
    "toulouse": "Réseau urbain Tisséo",
    "lille": "Réseau urbain ilévia",
    "rennes": "Réseau urbain STAR",
}

# --- licence ---------------------------------------------------------------
#
# Both SIRENE files and the geolocation file declare `lov2` - Licence Ouverte
# 2.0 - on data.gouv.fr. Per-operator GTFS licences are NOT inherited from the
# portal and must be read individually before any city ships; that is the
# standing rule that LA Metro's CC0-registry/restrictive-GTFS pair exists to
# enforce.
SIRENE_LICENCE = "Licence Ouverte 2.0"

# READ 2026-09-22, all six. They are NOT the same, and two of them are the two
# cities this project wants first. Full write-up, including the required
# notices and the acts no notice discharges, in
# `docs/licenses/france-required-notices.md`.
#
# `mobility-licence` covers exactly 2 of 799 datasets on the entire National
# Access Point - and they are Paris and Lyon. It is ODbL-DERIVED but NOT
# ODbL-COMPATIBLE: Art. 5.5(a)(iii) allows "une licence compatible" and no
# compatible list or proxy was ever published, so share-alike cannot be
# discharged by relicensing under ODbL. There is no government-hosted text;
# the authoritative document is a 14-page PDF, "Version au 03.02.2021".
GTFS_LICENCE = {
    "paris": "mobility-licence",      # PERMITTED WITH CONDITIONS
    "lyon": "mobility-licence",       # + account, trademark and indemnity gates
    "marseille": "lov2",
    "lille": "lov2",
    "toulouse": "odc-odbl",           # share-alike
    "rennes": "odc-odbl",             # share-alike
}

# Art. 5.4 notice text, and Art. 5.4(a) requires the database name to hyperlink
# to the dataset URI and the licence name to the licence text.
MOBILITY_LICENCE_NOTICE = (
    "Contient des informations de {dataset}, présentement mises à "
    "disposition aux conditions de la « Licence Mobilités »"
)

# TWO OBLIGATION SHAPES THIS PROJECT HAS NEVER CARRIED, both from Art. 5.7 and
# the MMTIS reglement: the DATE the reused data was last updated, and its
# UPDATE INTERVAL. Art. 5.7 forbids use that misleads "quant au contenu de
# l'information et a sa date de mise a jour" - and a pre-rendered static map
# built from a frozen snapshot is exactly what that describes unless the
# snapshot date is shown. Substantive, not a courtesy.
REQUIRES_SNAPSHOT_DATE = True
REQUIRES_UPDATE_INTERVAL = True

# Lyon cannot be fetched without an account on data.grandlyon.com, which this
# project does not create - the owner must register. Its NAP copy is NOT a
# fallback: 0% availability, last modified 2022-04-14, against a source portal
# current to 2026-09-22. Gate items 17-19 in `docs/gated_access.md`.
LYON_REQUIRES_ACCOUNT = True

# UNRESOLVED: the NAP API lists three GTFS resources for IDFM - its own via
# eu.ftp.opendatasoft.com, an ITO World mirror, and a Google-published "GTFS
# modifie" from an Apigee URL - while the licence review reports no OFFICIAL
# GTFS at all, only NeTEx and SIRI Lite. Settle which before fetching; building
# Paris from a third party's modified copy is not acceptable.
PARIS_GTFS_PROVENANCE_RESOLVED = False

SOURCE_ENCODING = "utf-8"
