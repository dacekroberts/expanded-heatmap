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

# NAF 2025, the newer scheme - PRESENT, AND DELIBERATELY NOT USED.
#
# This was a bare constant with a one-line comment until 2026-09-23, which is
# how a real question hid in plain sight: `pipeline/taxonomies/france_naf.py`
# keys entirely on rev. 2, so if SIRENE had migrated, the taxonomy was built on
# the wrong column. Measured over HTTP range requests against the September 2026
# release - 6 requests, 2.6 MB, no 2.2 GB download:
#
#     column                                  whole row group   active Paris
#     activitePrincipaleEtablissement                  100.0%         100.0%
#     activitePrincipaleNAF25Etablissement              37.5%         100.0%
#
# THE CODES ARE NOT INTERCHANGEABLE. The sous-classe letter differs - rev. 2
# writes `01.11Z` where NAF 2025 writes `01.11Y` - so france_naf.py's 64
# mappings would match nothing and `classify()` would return None for every
# row, emptying the map rather than raising.
#
# Rev. 2 wins on three counts: it is 100% populated everywhere rather than only
# on the active slice, it is what INSEE's published label file
# (`int_courts_naf_rev_2.xls`) covers, and it is what the taxonomy's deciding
# catch-all measurement (19.3% at sous-classe) was taken against.
#
# ⚠ WATCH ITEM, not an action: if INSEE deprecates rev. 2 in a future monthly
# release, this decision reverses and france_naf.py needs a NAF 2025 mapping
# built from INSEE's 2025 label file. The 37.5% figure is the thing to re-read -
# it rising toward 100% is the migration happening.
NAF25_COLUMN = "activitePrincipaleNAF25Etablissement"
NAF25_IN_USE = False
NAF25_POPULATED_MEASURED = {"all_rows": 0.375, "active_paris": 1.000}

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
#     enseigne1Etablissement             29.1%   <- NATIONAL
#     enseigne2Etablissement             13.4%   <- NATIONAL
#     denominationUsuelleEtablissement   34.2%   <- NATIONAL
#     EITHER an enseigne or a usual name 42.9%   <- NATIONAL, NOT PARIS
#     ...of Paris (751xx) rows           38.4%   <- Paris, superseded by 39.6%
#
# ** READ THE LABELS. 42.9% IS FRANCE, NOT PARIS.** Paris's own brief imported
# that national figure into a Paris table and captioned it "Paris is the
# worst-named of the six" - drawing the right conclusion from the wrong number,
# while the Paris-specific 38.4% sat five lines above it. Corrected 2026-09-23;
# the 12.6% one-pass scan puts Paris at **39.6%**, which agrees with 38.4% and
# never agreed with 42.9%. A country profile's national aggregate and a city's
# own rate are two different numbers, and the city one is in CITY_ESTIMATES.
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
# THE GUARD, and it is load-bearing rather than a formality. Measured
# 2026-09-22 via recherche-entreprises.api.gouv.fr (official, no key), 750
# active Paris rows: **8.7% of storefront rows are natural persons**, and of
# the UNNAMED rows **9.4%** are. So ~nine in ten unnamed rows are companies and
# the fallback is worth building - but applied blindly across Paris's ~148,600
# bucket rows it would publish on the order of TEN THOUSAND individuals' names,
# against the ~4,000 Los Angeles nearly shipped.
#
# The field lives on the UNITE LEGALE, joined on siren.
LEGAL_FORM_COLUMN = "categorieJuridiqueUniteLegale"
NATURAL_PERSON_CODE = "1000"          # personne physique - SUPPRESS the name
LEGAL_NAME_COLUMN = "denominationUniteLegale"

# Both figures are LOWER BOUNDS: the API used exposes `liste_enseignes` and
# `nom_commercial` but not `denominationUsuelleEtablissement`, which the
# national 42.9% above came from, so rows counted unnamed there are
# disproportionately companies. Direction is unaffected.
#
# TRAP, and it produced a wrong answer before it was caught: that API's
# `total_results` SATURATES AT 10,000. Every bucket returned exactly 10,000 and
# two reported "100% personne physique", which is plainly false for Paris
# retail. The control had checked the filter was VALIDATED (a nonsense value
# 400s), not that the count was TRUTHFUL. **A cap is a plausible number.**
# Take shares from sampled records, never from that API's counts.
NATURAL_PERSON_SHARE = {"all_storefront": 0.087, "of_unnamed": 0.094}

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

# RE-MEASURED 2026-09-23. All six cities scanned in ONE pass over 12.6% of the
# file, replacing a 3.9% scan. These are ESTIMATES for ordering, not build
# numbers - each city's Step 0 measures its own total. The naming column is the
# one that matters:
#
# **PARIS IS THE WORST-NAMED OF THE SIX, and the gap WIDENED on re-measurement.**
# The five follower cities carry a premises name on 43.4-53.5% of rows against
# Paris's 39.6%, so the cheap cities are also the better data - which inverts
# the usual assumption that the flagship city is the strongest one.
#
# **Every city except Toulouse came in LOWER by 1-3 points**, so the 3.9%
# figures were uniformly optimistic. The ranking survived unchanged.
#
# ONE SAMPLE, DELIBERATELY. A single row of this table may never be refreshed
# on its own: on 2026-09-23 Lyon's row was updated alone during its discard and
# left the other five on the old scan, which is the same
# comparison-across-samples error that produced a false "correction" to
# Marseille's figure hours earlier. Refresh all six or none.
#
# `bucket_rows_est` is SCALED and is a FLOOR - active bucket rows get denser
# through a file ordered by `siret`, which is seniority. Paris scales to 117,730
# against an independently measured **148,633**, so scaling understates by ~21%.
# The scaled value is kept here so the six stay comparable; the measured one is
# the build number.
PARIS_BUCKET_ROWS_MEASURED = 148_633   # use THIS for Paris, not the scaled est.
CITY_ESTIMATES = {
    "paris":     {"bucket_rows_est": 117_730, "named": 0.396},
    "marseille": {"bucket_rows_est": 25_430, "named": 0.434},
    "lyon":      {"bucket_rows_est": 18_082, "named": 0.514},  # DISCARDED
    "toulouse":  {"bucket_rows_est": 12_853, "named": 0.528},
    "lille":     {"bucket_rows_est": 8_076, "named": 0.475},
    "rennes":    {"bucket_rows_est": 4_833, "named": 0.535},
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

# --- the build sequence -----------------------------------------------------
#
# **LYON IS DROPPED FROM THE FOLLOWER SEQUENCE, 2026-09-22.** Not discarded as
# a city - its data is fine and its 19,449 estimated bucket rows are the third
# largest of the six - but it is no longer a cheap follower, and the whole
# argument for building France first was that the followers are cheap. Three
# independent gates, any one of which would be enough:
#
#   1. an account on data.grandlyon.com is required before ANY download, and
#      this project does not create accounts - the owner must register;
#   2. Grand Lyon CGU Art. 6.2 bars the producers' *signes distinctifs*
#      "associes ou non a l'utilisation des donnees", which collides head-on
#      with the invariant that every drawn line carries its real public name -
#      Lyon's being TCL;
#   3. CGU 9.4 is an open-ended indemnity, this project's SECOND after Hong
#      Kong's.
#
# And its NAP copy is not a fallback: 0% availability, last modified
# 2022-04-14, against a source portal current to 2026-09-22.
#
# **Marseille replaces it as the first follower** - `lov2`, no account, no
# trademark clause, no indemnity, and at 26,940 estimated bucket rows it is the
# largest follower anyway. Gate items 17-19 in `docs/gated_access.md`.
# Every French city tags "region": "Europe" in app/cities.py - NOT "France".
# Owner's decision 2026-09-22: ten European countries are on the remaining
# screen and they describe one readable view between them, so a region per
# country means ten entries to create, order and later merge. See
# docs/scaling_thresholds.md, "EVERY EUROPEAN CITY TAGS ONE REGION".
MAP_REGION = "Europe"

BUILD_SEQUENCE = ("paris", "marseille", "toulouse", "lille", "rennes")
# DISCARDED 2026-09-23 on four independent blockers - see
# docs/city_master_list.md and DECISIONS.md. Kept here because the DATA
# is fine (51.4% named, better than Paris), so a reinstatement would not
# need to re-measure the business leg.
DISCARDED = {"lyon": "account + CGU 9.4 indemnity + CGU 6.2 trademark + dead NAP feed"}

# RESOLVED 2026-09-22. The two readings disagreed because the NAP API's
# `resources` array INCLUDES the entries that also appear in
# `community_resources` - so a naive count sees three GTFS and concludes they
# are all official, while a reading that notices the community array concludes
# there is no official one. Subtracting the two arrays gives the answer:
#
#   eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip   OFFICIAL, IDFM's own
#   gtech-transit-prod.apigee.net/.../odbl/...        community (Google)
#   opendata.itoworld.com/fr/paris/...                community (ITO World)
#
# Exactly ONE official feed, and the choice is not close: IDFM's was updated
# 2026-09-22, the Google copy last in 2023-11-17, and the ITO World copy
# reports `is_available: False`. **Both third-party copies are stale or dead.**
PARIS_GTFS_PROVENANCE_RESOLVED = True
PARIS_GTFS_URL = "https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip"

# ⚠ CORRECTED 2026-09-23. This said True, and it was wrong.
#
# `add-country`'s rule is that a feed is trusted when THE ARTIFACT self-attests
# to its own freshness. This one does not: `brief_check.py`'s
# `idfm-gtfs-has-shapes-and-no-feed-info` measured **14 files and NO
# feed_info.txt**, so the zip declares no validity window at all. The
# `end_date` of 2026-10-21 is real but it is `transport.data.gouv.fr`'s
# metadata ABOUT the feed - the NAP's assertion, not the file's - and that is
# precisely the weaker thing `add-country` tells these two apart for: *a mirror
# is usable when the artifact self-attests, and is not when you must take the
# mirror's word.*
#
# The feed is still the right one; provenance was never the question, since the
# host is IDFM's own (`stif/` on Opendatasoft). What changes is HOW STALENESS
# IS DETECTED - from the NAP metadata or a content hash, never from the zip -
# and it changes a COMPLIANCE item, which is why this constant matters beyond
# bookkeeping: notice 24 (Licence Mobilites Art. 5.7) requires this project to
# DISPLAY the data's last-updated date and its update interval, and neither
# value exists inside the artifact. `fetch_sources.py` must capture both at
# download time or they cannot be shown honestly.
#
# The `features` and `modes` declarations quoted in the old comment are real,
# but they are NAP metadata too - they describe the feed, they do not date it.
PARIS_GTFS_SELF_ATTESTS = False

# Where the two Art. 5.7 values actually come from, since the artifact has
# neither. Recorded here rather than in Paris's config because all five cities
# of BUILD_SEQUENCE read this feed's publisher under the same licence.
PARIS_GTFS_FRESHNESS_SOURCE = "transport.data.gouv.fr NAP metadata, not the zip"

SOURCE_ENCODING = "utf-8"
