# Decisions log

Every judgment call, recorded with the numbers that were true when it was
made. **Append-only**: a superseded decision gets a new entry that says what
changed and why - the old entry stays. `docs/project_context.md` describes
the *current* state and is rewritten as things change; this file is the
trail behind it. Format and voice: see the `decisions-entry` skill (neutral
past tense; entries were reconstructed from session context).

Newest first. Entries run from the project's first working day, 2026-09-18,
onwards; the early ones are split by phase rather than by hour.

---

## Changes

### 2026-09-21 - Licence texts now kept in the repo

- **Started storing licence agreements locally, beginning with MassDOT's.** The
  MassDOT Developers License Agreement (4 pages, dated 2009-11-13, 87 KB) was
  moved from the repository root to `docs/licenses/`. It is the first licence
  text the project stores - `git ls-files "*.pdf"` returned nothing before this,
  and the transit licences in `docs/data_sources.md` were quoted from sources
  the file did not even record: grepping the whole licences section for URLs
  returned **one**, MassDOT's, for six agreements. A quote cannot be re-read
  against a source that changed - still less against one with no address -
  and this agreement's §5.1 lets MassDOT "alter the Terms of this License
  Agreement at any time without notice" while §8 reserves the right to "modify
  or revoke this Agreement at any time" - so the URL alone does not preserve
  what was actually agreed to. Re-fetching is not routine either: `mass.gov`
  returns 403 to automated fetches, which is why reading it needed the browser
  and a local PDF extraction. Rejected leaving it at the repository root, and
  rejected converting it to Markdown, which would make the stored copy a
  transcription rather than the document. Changes no compliance state: the
  MassDOT acknowledgement is still required only if Boston is built (required
  notice 7 in `docs/data_sources.md`), and no Boston pipeline code exists.
- **Stated position on storing third-party licence texts: unaltered,
  non-commercial, for compliance reference.** Decided by the project owner
  2026-09-21, because the grant each agency makes covers *the Data* and says
  nothing about its own agreement document, which is a separate copyrighted
  work - SEPTA's explicitly so ("Licensee may not use SEPTA's trademarks and
  copyrighted materials for any commercial or profit-making use and may not
  alter them in any way"). Keeping an unaltered copy for compliance satisfies
  both halves of that clause, and nothing is republished: the repository is the
  archive, not a distribution channel. Rejected the safer alternative of storing
  only SHA-256 hashes and retrieval dates - it detects that an agreement changed
  but leaves you without the wording you actually agreed to, which is the whole
  point. Hashes are recorded *as well*, in `docs/licenses/README.md`.
- **All six texts retrieved and stored the same day, and three retrieval facts
  were wrong in `docs/data_sources.md`.** `docs/licenses/` now holds MassDOT
  (PDF, 87 KB), SFMTA, LA Metro, CTA and SEPTA (whole HTML pages, 37-233 KB)
  and MTA (4.6 KB rendered text). Corrections found in the process: **SEPTA's
  host really is `wwww.septa.org` with four w's** - not the repo README's typo
  the file called it, since `www` and `wwww` each return 200 independently with
  no redirect between them; **SFMTA's licence page is `/reports/gtfs-transit-
  data`**, with the agreement inline above the download link and no separate
  document (`/reports-documents/...` is a 404); and **`mta.info` returns 403 to
  curl even with full browser headers**, so its terms were captured from the
  browser pane as text, the same way the MassDOT PDF needed the browser.
- **The exercise immediately paid for itself: MTA's actual terms had never been
  read, and they are not permissive.** `docs/data_sources.md` recorded New York
  as "Our data feeds are free to use ... Not specified for the GTFS data",
  which is the blurb on `mta.info/developers` - not the agreement at
  `/developers/terms-and-conditions`, which was never opened. That agreement
  carries real obligations, including **"You will not modify or delete any of
  the data"** - the same shape as LA Metro's clause, the one the project treated
  as its tightest - plus "You will not state or imply that the data is accurate,
  complete, or timely" and a prohibition on implying MTA licensed the app. New
  York is a **built** city, so this is not hypothetical. Recorded as an open
  decision in `PLAN.md` rather than settled here; the fact that the terms say
  what they say is not a judgment call, but whether this project satisfies them
  is.

### 2026-09-21 - Transit geometry no longer rounded; the clause it was meant to satisfy turned out to be moot

- **Where this came from.** A concurrent session read MTA's actual terms and
  found **"You will not modify or delete any of the data"** (with a carve-out:
  "You may, however, create an app that uses some but not all of the data") -
  where this project had previously recorded only the "free to use" line from
  MTA's landing page. That raised a real question, because
  `map_common.COORD_DP` rounded **every** coordinate to 6 decimal places
  (0.11 m) before it reached the HTML, transit geometry included.
- **The question was wider than MTA.** The same rounding applied to **LA
  Metro's** `shapes.txt`, and LA Metro's clause is the tighter one - "not
  change, tamper, dismantle, augment, misrepresent or otherwise modify the
  Transport Information". The verdict recorded earlier on 2026-09-21 said the
  project "does not modify it" because "the rail alignment is drawn from the
  feed's own `shapes.txt` geometry and displayed as that line", and rounding
  would have made that sentence true only with an asterisk.
- **Decision: stop rounding transit coordinates; keep rounding business
  coordinates.** Station points, ring centres, line-label anchors and every
  `shapes.txt` vertex now go out at full source precision, via a
  `_transit_coord()` helper that exists so the reason sits at each call site
  rather than only in a comment. `COORD_DP` still applies to business pins and
  both heat layers, which is where the size saving actually is: heat layers are
  33-57% of a rendered map, line geometry 4-6%.
- **MTA's clause, which prompted all of this, turned out to be moot - and a
  first measurement of LA Metro's was wrong in the other direction.** An
  initial check sampled the first few thousand characters of each city's line
  geometry and concluded that MTA, LA Metro, SFMTA and SEPTA all published at
  6 dp, making the rounding a no-op for every restrictive feed. Measuring
  **every vertex** instead:

  | Feed | Max dp | Coords over 6 dp | Was the rounding altering it? |
  |---|---|---|---|
  | **LA Metro** | **10** | **2,606 of 12,426 (21.0%)** | **Yes** |
  | MTS (San Diego) | 8 | 2,499 of 2,518 (99.2%) | Yes |
  | CTA (Chicago) | 8 | 6,359 of 6,410 (99.2%) | Yes |
  | MTA (New York) | 6 | 0 (0.0%) | No - no-op |
  | SFMTA | 6 | 0 (0.0%) | No - no-op |
  | SEPTA | 6 | 0 (0.0%) | No - no-op |

  **So the change was necessary rather than merely prudent, for LA Metro
  specifically** - the tightest licence in the project, being altered on a
  fifth of its vertices. The recorded LA Metro verdict was *not* literally true
  before this; it is now. MTA's feed is genuinely already 6 dp, so the clause
  that triggered the investigation never bit. MTS and CTA were being altered
  too, and neither restricts modification - CTA expressly permits "create
  derivative works" and MTS has no modification clause.
- **Sampling is what produced the wrong first answer, and it is worth naming:**
  LA Metro's feed is mixed-precision, 6 dp for the first stretch of its
  geometry and up to 10 dp later, so any check that reads the beginning of the
  file gets a clean-looking result. The same trap as Philadelphia's "100%
  geometry" reading, which counted non-null values and missed 218 empty ones.
- **Scope was corrected mid-implementation, after the first attempt exempted
  too much.** Exempting *station* coordinates as well made them emit **15
  decimal places** of floating-point noise - because most cities derive a
  station's position by averaging its platform stops
  (`.agg(latitude=("stop_lat", "mean"))`), so those are the project's own
  computed values, not agency data. Station points, ring centres and line
  labels are therefore still rounded; **only the `shapes.txt` vertices are
  exempt**, which is the one place an agency's data is reproduced verbatim.
  That narrowing also removed most of the size cost.
- **Cost, measured after the correction: +23,788 bytes across 16.5 MB
  (0.14%).** New York, San Francisco and Philadelphia are **byte-identical**
  to before; San Diego +5,012, Chicago +12,879, Los Angeles +5,897.
- **Verified before and after implementing, as the owner required:** visually a
  no-op (0.11 m is half a pixel at OSM zoom 19), and structurally a no-op - the
  unrounded vertices also feed the label-placement geometry, where a 0.11 m
  perturbation cannot flip a tail-end choice between line ends kilometres
  apart. Every city re-rendered with **identical row counts and station
  counts**, so only coordinate precision moved. All six committed outputs were
  re-baselined.
- **Also keeps a future foot-gun closed.** `PLAN.md` carries a live
  optimisation for New York's oversized map: "rounding coordinates to 5 dp
  saves 1.4 MB". At 5 dp the old behaviour would have begun altering MTA's
  geometry too, silently, as a side effect of a size tweak by someone not
  thinking about licences. With the exemption in place that optimisation is
  safe to adopt for business points only.
- **One incidental discovery while checking the diffs:** the five
  `excluded_stations.csv` files show as modified in `git status` after a
  re-render but have **zero content change** - it is purely CRLF-vs-LF, which
  git normalises on commit. `drift_check.py` already handles both that and
  Folium's random 32-hex element ids (which change every save, and are why a
  raw diff of `heatmap.html` is meaningless). Neither is drift.
- **The route-colour question is recorded as OPEN, by the owner's decision**,
  rather than resolved by substituting a palette. Three agencies' terms bear on
  it: MTA ("logos, maps and symbols need a separate licence application", free
  but must be applied for), SEPTA (the trademark clause already open), and -
  for a future D.C. - WMATA ("prohibited from using WMATA Intellectual
  Property, including any confusingly similar variants, in association with the
  Transit Data or API unless you have entered into a separate, written license
  agreement"). The project currently uses each agency's own `route_color`
  values for line strokes and labels, with one deliberate exception already
  recorded: Staten Island Railway, lightened for contrast. It joins the
  pre-deploy licence list rather than blocking anything now.

### 2026-09-21 - WMATA's licence read: it does not rule out D.C., but it does rule out the mirror

- **Why it was read now.** WMATA is the first transit feed in the project that
  cannot simply be downloaded - `api.wmata.com/gtfs/rail-gtfs-static.zip`
  returns **401** without a registered key - and the owner asked whether the
  licence might disqualify D.C. on its own before any effort went into getting
  access.
- **It does not. It is more permissive than LA Metro's on the point that
  matters most.** The grant is "a limited, non-exclusive, non-assignable,
  non-transferrable, non-sublicensable, revocable license to download, use,
  reproduce, and redistribute WMATA's Transit Data within your Application",
  there is **no modification clause at all**, and **no attribution is
  required** - unlike MassDOT, SFMTA and LA Metro.
- **But it rules out the Mobility Database mirror, which reverses the easier of
  the two options originally offered.** Redistribution is restricted:
  "prohibited from: sharing (except with your Application's users),
  transferring, sublicensing, selling or leasing any Transit Data, directly or
  indirectly...to any other person", with an exception needing prior written
  authorisation and data "inseparably commingled" with your own. Publishing a
  map to the site's own visitors is sharing with the Application's users and is
  fine. Taking the feed from a third-party mirror is not the safe shortcut it
  looked like: it relies on a redistribution the terms appear to prohibit, and
  it means obtaining the data **outside** the licence rather than accepting it.
  **The key is the correct route; the mirror is the worse one.**
- **The "secret in the pipeline" objection was overstated and is withdrawn.**
  GTFS fetching already lives in non-`step*.py` scripts so that
  `drift_check.py` stays offline and deterministic, so a WMATA key would be a
  local environment variable used for an occasional manual refresh. It never
  reaches Streamlit Cloud, which only reads `outputs/`. That is a much smaller
  change than first described.
- **What remains true and worth knowing:** keys "remain WMATA's property and
  may be revoked or otherwise limited at any time", cannot be sold,
  transferred or sublicensed, and "enable WMATA to associate your API activity
  with your Application". Registration is the owner's action - an account
  cannot be created on their behalf.

### 2026-09-21 - Screened every remaining candidate city, and found three the shortlist never had

- **Why this happened before the next build**, rather than building Boston: the
  owner chose to screen the whole remaining list for licensing and viability
  dealbreakers first, then decide which cities to build and which to exclude.
  That ordering paid for itself immediately - Dallas fell, and three candidates
  appeared that were not on the list at all.
- **Washington D.C. is the strongest remaining candidate, and the first
  non-NAICS city with all three buckets from one registry.** 76,107 active
  licences: Food Services 4,901, Beauty and Grooming 486, and ~1,550 real
  retail once the catch-all is removed. Three findings decide how it must be
  built, and all three came from the distribution check the 2026-09-18 pass
  never ran:
  - **`BUSINESSACTIVITY = 'General Business'` (14,770 rows) is an
    office/professional catch-all and must be excluded.** Sampled 40 rows:
    Nossaman LLP, Gannett Fleming Engineers and Architects, Voith & Mactavish
    Architects, Brown and Caldwell, consultancies, investment and tech firms.
    It is 14,729 of the 16,282 rows in "General Sales and Services", so
    including it would have inflated D.C.'s retail roughly tenfold with law
    offices. Same role as Los Angeles' NAICS 812990.
  - **49% of active rows are residential rentals** - One Family Rental 25,587,
    Apartment 6,106, Two Family Rental 2,560, Short Term Rental 2,197, Vacation
    Rental 803. Philadelphia's landlord-registration pattern, at half the share.
  - **The recorded "truncated to whole degrees" caveat is worse than recorded,
    and also harmless.** `LATITUDE` is literally `39` and `LONGITUDE` `-77` on
    every row: **0 of 76,107 fall inside D.C.** But `X_COORDINATE`/
    `Y_COORDINATE` are real, present on 77% of storefront rows, and are
    **EPSG:26985** - verified by transforming 312 Pennsylvania Ave SE to
    (38.88715, -77.00153), with the three plausible datum variants agreeing to
    sub-metre. `MAR_ID` should recover the remaining 23% without the Census
    geocoder, so the old caveat's "use address geocoding" is now the fallback
    rather than the plan.
  - Also measured: trade name missing on **49%** of storefront rows (the Los
    Angeles trap at half severity), `PREMISEINDC='Yes'` on 61,329 rows as a
    better in-city marker than `WARD` (null on 16,806 and mixing "Ward 2" with
    "2"), `SSL` parcel IDs on 45,476 for the residence check, and
    `BUSINESSOWNER*`/`AGENT*` person-name columns on ~34k rows that must never
    be published.
- **WMATA is the first transit feed in the project that cannot simply be
  downloaded.** `api.wmata.com/gtfs/rail-gtfs-static.zip` returns **401**
  without a registered API key. That is an access question rather than a
  licence one, and it has two answers: a free key from
  `developer.wmata.com/signup` (which would put a secret in the pipeline,
  something no other city needs) or the keyless Mobility Database mirror. Not
  decided here. `developer.wmata.com/license` is **unread**, and transit terms
  have been the loosest end of every licence review, so it is flagged rather
  than assumed.
- **Dallas ruled out, on currency rather than schema - a different reason from
  the one recorded on 2026-09-18.** Its only source with a classification, a
  business name and coordinates (`9qet-qt9e`, PDDL, 23,731 rows, `land_use`) is
  frozen: `date_issued` spans 2018-01-02 to **2022-11-15**, rows last changed
  2022-11-16. `ync5-xnfn`, the dashboard `PLAN.md` told us to check for
  something fresher, **is not a dataset** - HTTP 403 "no row or column access
  to non-tabular tables", 0 columns - which closes that open question with a
  negative. The fresher food file (`dri5-wcct`) is named "October 2016 to
  January 2024", declares no licence, and has no business-name column. Of 1,087
  assets on the domain, nothing business-classified is current. Texas requires
  no general city business licence, so the certificate of occupancy *is*
  Dallas's registry and it stopped publishing. **Reasoning: a four-year-old
  snapshot beside six current cities is a worse comparability problem than any
  thinness**, and unlike thinness it cannot be disclosed away on a city page.
  Houston fails the same way and for the same structural reason (zero results).
- **Three candidates found that were never on the list**, all from widening the
  screen past the "25 largest cities" frame to rail cities of any size:
  - **Miami** - Miami-Dade "Local Business Tax" ArcGIS layer, **194,099 rows**,
    `ACCSTATUS`, NAICS via `BUSNAICSCD` (so no new taxonomy module), real
    `LAT`/`LON`, `FOLIO` parcel IDs, and `MUNBUSLOC` to cut county data down to
    "01 - MIAMI". Needs a real Step 0.
  - **New Orleans** - `iqay-p646` "Active Occupational Licenses", 16,396 rows,
    and **CC0 1.0, the cleanest declared licence of any candidate**. Rail is
    streetcar-only, which is a scope question for the owner rather than a data
    one.
  - **Kansas City** - explicitly PUBLIC_DOMAIN, 15,895 rows, geocoded, all
    three buckets in readable categories (Beauty Salons 662, Barber Shops 146,
    Clothing Retailers 192, Supermarkets 154): the best data-to-effort ratio
    found. **Recommended for exclusion on rail, not data** - one short
    streetcar line, well under the bar every built city meets. Recorded that
    way deliberately, because "no usable data" and "not enough rail" are
    different verdicts and only one of them can be reversed by a better dataset.
- **Recorded fifteen cities as "screened and not found", explicitly NOT as
  disqualified.** Atlanta, Baltimore, Portland OR, Phoenix, Minneapolis, St.
  Louis, Cleveland, Pittsburgh, Detroit, Jersey City, Tucson, Sacramento, Salt
  Lake City, Honolulu and Buffalo. Twelve of those domains returned HTTP 404
  from Socrata's discovery API, which means **"not a Socrata domain", not "no
  data"**, and the ArcGIS pass searched dataset titles only. **Seattle is the
  proof that the distinction matters**: it returned "no matching datasets" on
  Socrata and then turned out to have an official 54,604-row active
  business-licence layer on ArcGIS. This is the Denver and San Jose lesson
  pointing the other way - a shallow check is as unreliable for ruling a city
  *out* as for ruling one *in* - so the list is kept as a to-check queue rather
  than a rejection pile.
- **Method note worth keeping: Socrata's cross-domain discovery API
  (`api.us.socrata.com/api/catalog/v1`) answers "does any public portal publish
  this" in one request**, including the declared licence and the last-updated
  date. It is what established that no Massachusetts salon source exists
  anywhere, and what surfaced New Orleans and Kansas City. Its blind spot is
  everything not on Socrata - which is most cities, and which is why the ArcGIS
  Online search API (`arcgis.com/sharing/rest/search`) is a necessary second
  pass.

### 2026-09-21 - Seattle: deferred, then scoped as the first multi-municipality city

- **Sequence, because it changed twice in one session.** Seattle was first
  "ignored" during the candidate screen, then clarified to "we will return to
  implementing Seattle later on", then scoped by the owner as the project's
  first test of merging several jurisdictions' business data into one map, with
  **full line coverage** of Link's 1 and 2 Lines. Its own registry findings
  were kept rather than discarded, so returning to it costs no re-probe.
- **This supersedes the standing rule that stations in another city are a new
  project rather than a config change.** That rule was set when San Diego
  dropped 16 Trolley stations in neighbouring cities, on the grounds that
  including them would need those cities' own business data sourced and
  verified separately. The rule stands for every other city - Seattle is an
  owner-decided exception, and the deliberate test of whether the multi-source
  idea works.
- **The jurisdiction list is wider than the seven named**, which is a sizing
  fact rather than a change of intent. The owner named Seattle, Shoreline,
  Lynnwood, Tukwila, Federal Way, Bellevue and Redmond. Link also stops in
  **Mountlake Terrace** and **SeaTac** on the 1 Line and **Mercer Island** on
  the 2 Line, and a Federal Way scope brings the extension through **Des
  Moines** and **Kent** - about **ten to twelve** jurisdictions. To be settled
  from the real GTFS stop set against a Washington municipal boundary layer
  rather than from memory, which is the discipline that caught San Diego's 16
  and Los Angeles' 54. The corrected list is written into the probe script so
  it is not re-derived.
- **What the architecture already supports, and what it does not.** Supported:
  per-jurisdiction taxonomy modules mapping into the shared three buckets,
  because `map_common.py` never names a taxonomy; if several Washington cities
  use NAICS they share the existing module. Not yet existing: multi-polygon
  scope (`CITY_KEEP` and the boundary filter assume one city),
  per-jurisdiction provenance on each business row (so the map can say which
  registry a pin came from, and so one city's data going stale is visible), and
  a cross-registry dedup rule for businesses licensed in more than one
  jurisdiction.
- **Two risks recorded now.** A jurisdiction with no usable registry would
  render as an empty suburb rather than an unsurveyed one - the same failure
  that made Boston's `Business Inventory` unusable as a heat layer, so decide
  up front what the map does where data is missing. And the page name needs a
  decision: the project is never named after a city, and a map spanning twelve
  of them is honestly "Link light rail" rather than "Seattle".

### 2026-09-21 - Boston Step 0: passed, and narrower than the shortlist assumed

- **Verdict: viable, two buckets, not built.** Boston passes all three Step 0
  requirements - business data, transit, boundary - and is the thinnest and
  narrowest candidate the project has evaluated. Recorded rather than built:
  the project owner chose to probe the remaining candidates (D.C., Dallas and
  the rest of the list) for licensing and viability dealbreakers first, then
  decide which to build and which to exclude. No pipeline code was written.
- **The whole catalogue matters, not the search hits.** Seven search terms
  against CKAN's `package_search` returned 48 packages; `package_list` returns
  **247**. The extra 199 held the city boundary layer, the SAM address points
  and the Property Assessment roll - all three directly relevant, none of them
  surfaced by the obvious queries. Pull the full list.
- **Boston licenses food and alcohol, and no other trade.** Inspectional
  Services covers food; the Licensing Board covers alcohol, lodging, billiards
  and bowling. Deduplicated to premises: Food service 2,237, Retail 385
  unambiguous (`RF`-only), plus 306 package stores and 43 cannabis shops that
  *overlap* the `RF` set. So a "commercial density" map of Boston built from
  licences is really a **food density** map - a narrowing of the project's
  premise that had to be named rather than absorbed.
- **The official "Active" extract is the wrong file, and the reason is a
  silently missing category.** `Active Food Establishment Licenses` (3,345
  rows) is exactly `FS` 1,762 + `FT` 1,583 licences and contains no `RF`
  (Retail Food) at all - which would have made Boston a **one-bucket** city and
  probably disqualified it. The 902,651-row inspections history carries the
  same `licensecat` field including `RF`'s 504 active premises, and has better
  coordinates too: 99.9% of active premises versus 93.8%. Found by asking the
  history for `SELECT DISTINCT licensecat` rather than trusting the extract's
  own two values - the same move that filled Philadelphia's taxonomy.
- **Personal services is absent, not thin - and that was verified, not
  inferred.** Massachusetts licenses cosmetology and barbering at state level
  and publishes no address-bearing export; its register is a per-licence
  ePLACE/MADOL lookup. Checked three independent ways: Socrata's cross-domain
  discovery API returns **no Massachusetts source** for cosmetology, barber,
  salon, hair, nail salon, body art or tattoo (the only MA domains indexed are
  an education portal and state spending); `data.mass.gov` is not a data portal
  at all, returning HTML 404 from both Socrata and CKAN entry points; and
  `opendata.mass.gov` does not resolve. Same structural cause as Philadelphia,
  and the second city where a bucket has no source in the entire jurisdiction.
- **Rejected the one source that would have made Boston a three-bucket city,
  on coverage grounds.** `Business Inventory` is a summer-2025 field census
  with almost exactly this project's taxonomy - `Beauty_Services` 243
  (Hair_Salon 101, Barber_Shop 46, Nail_Salon 32), Clothing_Store,
  Jewelry_Store, Laundry, Tailor - carrying WGS84 coordinates on 99.8% of rows
  and even a vacancy flag. Its own notes state the limit: "every storefront in
  downtown Boston, as well as comprehensive data on 3 major commercial
  corridors in Mattapan, Jamaica Plain, and Allston." Measured: 37 occupied
  0.01-degree cells, 18 ZIPs, 14 rows in Brookline. **A heat surface built on a
  partial survey shows where surveyors walked, not where commerce is**, and
  mixing it into the heat layer would make four areas read as three-bucket and
  the rest as two. Recorded in `docs/data_sources.md` as available and
  deliberately unused, with the trigger for revisiting it (a city-wide survey).
  It is also the only dataset on the portal whose licence is `notspecified`, so
  using it would require establishing terms first.
- **Trade-name convention is inverted here, which would have broken a copied
  step 2 quietly.** In the food data `dbaname` is blank on **99.0%** of rows
  while `businessname` is never blank and holds the trade name. Every built
  city prefers the `dba` column, so a copied step 2 would have fallen back to
  near-nothing rather than failing loudly. Measured because the `add-city`
  skill requires checking the trade-name blank rate - the check that caught Los
  Angeles' 68% and ~4,000 individuals' names. (The Licensing Board sets use the
  normal convention, so the two cannot share one rule.)
- **CRS verified by transformation, not by inspection.** `gpsx`/`gpsy` look
  like Massachusetts State Plane and are: EPSG:2249 puts Copley Square at
  (42.3486, -71.0788) and Brighton Avenue in Allston, while EPSG:26986 - the
  metre-based sibling of the same state plane, the plausible wrong answer -
  lands everything near 60 degrees north. Boston's own projected CRS would be
  EPSG:32619 (UTM 19N), derived from longitude rather than copied.
- **71 of 125 rapid-transit stations are inside Boston.** The other 54 lie in
  Brookline, Cambridge, Somerville, Newton, Medford, Malden, Quincy, Revere and
  Milton - the entire Green Line C corridor is Brookline. Consistent with San
  Diego's 16 of 63 and Los Angeles' 54 of 110: the boundary filter is not
  optional. Four stations fall marginally outside because the boundary layer
  excludes water, and they do not all resolve the same way - Boston College at
  6.7 m is genuinely a Boston station, Central Avenue at 29.7 m is genuinely
  Milton - so a distance tolerance cannot separate them and a MassGIS multi-town
  layer is needed to name the municipality. Green Line is four street-running
  branches on a shared central subway: San Francisco's shape, so
  `docs/sub_transit_line_filters.md` would apply. The 14 `CR-*` Regional Rail
  lines would be excluded, as commuter rail has been in every built city.
- **Licences: the cleanest city so far, with one obligation.** Every source
  used is **ODC-PDDL**, a public-domain dedication declared per dataset. The
  MBTA feed declares no licence in `feed_info.txt`, so the MassDOT Developers
  License Agreement was read in full: it grants use, reproduction and
  redistribution, **expressly permits combining the data with other data**
  (§4.2), and contains **no restriction on modification** - the direct opposite
  of LA Metro's clause, the tightest in the project. It requires one notice,
  "Clearly acknowledge MassDOT as the provider of the Data" (§4.1), and forbids
  reproducing MBTA logos or trademarks, which this project satisfies by
  construction since it draws its own geometry and reproduces no roundel. Added
  to the required-notices list as conditional on Boston actually being built,
  so it is not mistaken for an outstanding compliance item today. Reading it
  needed the browser and then a local PDF extraction, because `mass.gov`
  returns 403 to automated fetches and the agreement is a PDF the browser
  downloads rather than renders.
- **Corrected a stale count in `docs/data_sources.md`.** The required-notices
  preamble said "three sources require specific text, and one of the three is
  already satisfied", which had not matched its own list since LA Metro was
  added as item 4. Now states four required with one satisfied, and separates
  the conditional ones (New York, MassDOT) from the encouraged one (CTA).

### 2026-09-21 - San Diego, done properly: 315 pins, not 42

- **The 42 was a method artifact, as suspected, and the corrected figure is
  315 (2.80%)** - 7.5x higher, and in line with San Francisco's 1.19% and Los
  Angeles' 2.05% for a city that is far more suburban and single-family than
  either.
- **The right question here is "which parcel is NEAREST", not "which parcel
  contains this point".** San Diego's business coordinates sit 5-15 m outside
  their own lot - placed at the street frontage, and SanGIS parcels exclude
  road right-of-way - so a point-in-parcel test matched 1 of 30 sampled pins.
  The earlier filter fell back to "every parcel within 25 m must be
  residential and owner-occupied", which is a different question and clears
  any home with a rental next door.
- **Two wrong turns before the working method, both recorded in
  `fetch_parcels.py` so they are not retried.** `PLAN.md`'s own advice - bulk
  download the parcel centroids - was wrong in practice: `orderByFields`
  sorts 664,662 rows and `resultOffset` deep-pages through them, costing ~26 s
  per 2,000-row page, about two hours. Abandoned at 2.7%. The advice has been
  corrected in place rather than left to mislead.
- **What works: `returnCentroid=true` on a per-point BUFFERED query.** This
  layer supports centroid-only responses, so one request per point returns the
  candidate parcels' centroids and the nearest is chosen locally - true
  nearest semantics in 2,463 requests rather than ~5,000, with no deep paging.
  95.5% found a parcel, zero failures.
- **Checked the obvious flaw in that shortcut rather than assuming it away.**
  The query buffer measures to the parcel BOUNDARY while ranking uses the
  CENTROID, so a large parcel whose edge is within 25 m can have a centroid
  hundreds of metres away - which could misattribute a business to a small
  neighbouring house. Measured: every one of the 315 flagged rows has its
  chosen centroid within **39.1 m** (mean 22.2, median 21.6), because
  single-family lots are small. The 1,406 m outlier in the overall
  distribution belongs to *unflagged* rows on large non-residential parcels -
  the harmless direction.
- **The removed rows validate the filter by their own classifications**, which
  is stronger evidence than any distance statistic: 286 of 315 carry no
  suite or unit, and the NAICS descriptions include **23 "COTTAGE FOOD
  OPERATOR"** - California's licence category for food produced in a *home
  kitchen*, definitionally a home business - plus 20 "BEAUTY SHOPS - BOOTH
  RENTAL" (a chair renter, not a premises, the same pattern the
  `multi-source-city` skill flags for New York's `DOSAERENTER`), 66 "other
  personal services" and 20 beauty salons.
- **Rate limit measured rather than guessed.** SANDAG's gateway sustains
  roughly 2 requests/second for a run this long: ~7 req/s completed once, a
  marginally faster attempt was refused after ~500. The script now defaults to
  1 worker at 0.4 s (~20 minutes) and **aborts after 25 refusals writing
  nothing** - which it did, once, costing only time. A partial cache is the
  one outcome worth avoiding, because it filters only where the lookup
  happened to succeed.
- **Reintroduced and then re-fixed the prefilter bug**, an hour after fixing
  it in Los Angeles. When the bulk fetcher stopped reading business data the
  prefilter snapshot looked like dead code and was deleted; the per-point
  version then read step 2's *filtered* output, on the reasoning that "the
  filter only removes rows, so the candidate set can only shrink". True, and
  beside the point: the shrinkage is exactly the rows that must stay removed,
  and without cache entries they return. Restored, with the reason stated in
  all three files.
- **No apartment rule for this city**, stated in the code rather than left
  looking like an omission: that rule reads a dwelling-unit designator out of
  the address, and this registry's `address_suite` holds bare values ("A",
  "101") with no APT/UNIT token. Residual: 1 pin (0.04%).

### 2026-09-21 - Los Angeles filtered; two of my own bugs, and a WAF block

- **Los Angeles: 1,252 pins removed** (61,208 -> 59,956, 2.05%), the largest of
  the three. NAICS 453990 misc retail (120), 452000 general merchandise (87),
  812112 beauty (86), 812111 barber (75), 812190 other personal care (72).
  Lookup coverage 99.9%, zero request failures.
- **Bug 1: a buffer changed the question, not just the coverage.** An exact
  point-in-parcel test matches only 49% of LA's pins, because the 9% of
  coordinates recovered by Census geocoding land on street centrelines. I
  buffered to 25 m to fix that - but a buffer returns SEVERAL parcels, and
  requiring all of them to be owner-occupied means one rented neighbour clears
  a genuine home. It removed **95** rows where the exact test implied ~1,000.
  Corrected to use the containing parcel where there is one (8,433 pins) and
  the buffer only otherwise (6,474), which is 1,252. **Caught only because the
  sample measurement and the implementation disagreed tenfold** - which is the
  argument for measuring before building, not after.
- **Bug 2: the fetcher read its own consumer's output.** It loaded step 3's
  filtered file, so the cache would have omitted the rows already removed and
  they would have silently returned on the next run. Step 3 now always writes
  an unfiltered `businesses_geocoded_prefilter.csv` that the fetcher reads, so
  the two cannot get out of order whatever someone runs first. Same pattern
  added to San Diego.
- **A real bug in `scripts/check_personal_exposure.py`, corrected.** Its
  residential/commercial unit lists contradicted their own source write-up,
  `docs/passover_name_filtering_skill.md`, on three designators: FL/FLOOR and
  RM/ROOM were residential here and commercial there, and SPC was reversed. An
  office floor is not a dwelling, so **every city's residential share was
  overstated in the same direction**. Corrected shares: LA 5.81%, SF 1.55%,
  Chicago 0.20%, NY 0.09%, San Diego 0.04%, Philadelphia 0.00%. A bare `LOT`
  is deliberately NOT adopted as residential despite the source listing it: in
  these registries it is at least as likely to be a parking lot, and it could
  not be verified either way, so adopting it would trade a known error for an
  unknown one.
- **San Diego: blocked by SANDAG's WAF, and nothing was shipped.** An 8-worker
  run drew HTTP 403 from an Azure Application Gateway after ~750 requests. The
  lookup swallowed every exception alike, so it reported "1,706 failures"
  rather than "we are blocked", and wrote a 757-row cache covering 31% of the
  population. **That cache was discarded rather than used**: a filter built on
  it would have removed home businesses only where the lookup happened to
  succeed - the same partial-coverage error already rejected for San
  Francisco's 43.8% address join. The fetcher now treats 403/429 as their own
  signal, defaults to 2 workers with a delay, and aborts after 25 refusals
  writing nothing. San Diego's map is unchanged and its filter is inert until
  a complete lookup exists.
- **Still outstanding: the apartment population.** The parcel filters catch
  people at *houses*. A person-like name at an APT/UNIT address in a
  multi-family building is a different population the single-family test
  cannot reach, and after the parcel filters it is still 844 pins in Los
  Angeles (5.81%) and 194 in San Francisco (1.55%).

### 2026-09-21 - Home-business filters built, starting with San Francisco

- **Decided to fix the already-mapped cities before adding Boston**, at the
  project owner's direction, rather than carry a known live exposure on a
  public repository while the city list grows.
- **San Francisco: 217 pins removed** (18,242 -> 18,025), exactly matching the
  measurement. A person-like displayed name at a parcel the Assessor calls
  Single Family Residential which also claims a homeowner's exemption. Mostly
  NAICS 722320 caterers, 812112 beauty, 812910 pet care, 458110 clothing.
- **Shared logic now lives in `pipeline/residence.py`** rather than being
  written three times. It holds the person-name test - which was already
  duplicated between Philadelphia's step 2 and
  `scripts/check_personal_exposure.py` - plus `flag_home_based()`, which takes
  each city's own residential / owner-occupied / individual columns and
  requires all supplied conditions together. The module docstring carries the
  measured counts from every city, because the mistake it exists to prevent
  (treating land use alone as a privacy signal) is the one a future reader is
  most likely to make.
- **Each city's property download lives in a non-`step*.py` script** writing
  into gitignored `raw/`, so `drift_check.py` stays offline and deterministic.
  San Francisco's `fetch_sources.py` deliberately fetches ONLY the new
  Assessor roll: re-downloading its business export would change every count
  recorded in this file and should be a deliberate act, not a side effect.
- **Two things recorded so they are not rediscovered.** San Francisco's roll
  must be fetched from `data.sf.gov` - `data.sfgov.org` returns 403 on
  `/resource/` while `/api/views/` succeeds, which makes the dataset look
  unavailable. And the join must be spatial: an address join reaches 43.8%,
  which was rejected outright rather than used, because a filter running off a
  partial join removes home businesses only where the address text happened to
  match - arbitrary while appearing complete.

### 2026-09-21 - The California cities have a systemic home-business exposure

- **Los Angeles is worse than San Francisco, and this is now a workstream
  rather than a footnote.** A random sample of 400 of its person-like pins
  (seed 20260921) put **7.2% on a Residential parcel claiming a homeowner's
  exemption**, which extrapolates to **~1,081 of 14,921 person-like pins
  (~1.77% of 61,208)**. Only 53.2% of the sample matched a parcel at all, and
  among those that did the rate is 13.6%, so the honest range is **~1,000-2,000
  pins**. The unmatched are expected to be the ~9% of LA coordinates recovered
  by Census geocoding, which land on street centrelines rather than inside a
  parcel.
- **The same signature as San Francisco**: NAICS 812111/812112 barber and
  beauty, 812910 pet care, 812190, 722320 caterers, 453220 gift shops, 452000
  general merchandise - with `UseDescription` "Single" on 27 of the 29 hits.
- **Both cities already excluded NAICS 812990 on 2026-09-21 for this exact
  reason.** That exclusion worked on the code that *names* itself a catch-all;
  what is left is the same home-based pattern hiding under codes that are
  entirely legitimate for a real storefront, which is why no blanket NAICS
  exclusion can reach it and a property join is the only way to see it.
- **So the unit-indicator test was not slightly optimistic, it was blind in the
  two largest NAICS cities.** Philadelphia's 8 pins made this look like a
  rounding error; California's two cities put it at four orders of magnitude
  more. San Diego - also California, also NAICS, with 24,974 SOLE
  proprietorships and no residence signal of any kind - is now the most likely
  to be worse still, and remains unmeasured.
- **Recommended sequencing change: fix these before adding Boston.** Each new
  city otherwise adds to a known, live exposure on a public repository, and the
  method is now proven on three cities. Raised for the project owner rather
  than acted on, because it re-orders the agreed roadmap.

### 2026-09-21 - San Francisco has a real home-business exposure: 217 pins

- **Checked San Francisco "just to be sure" and it is the one city where the
  answer changed.** 217 pins (1.19% of 18,242) display a person-like name at a
  parcel the Assessor classifies **Single Family Residential** *and* which
  claims a **homeowner's exemption** - California's homestead analogue, granted
  only on an owner-occupied primary residence. That is 27x Philadelphia's 8,
  and the largest personal-data exposure found anywhere in this project.
- **What they are leaves little doubt**, from the NAICS of the affected rows:
  722320 caterers (16), 812112 beauty salons (15), 812910 pet care (10),
  812199 other personal care (8), 458110 clothing (11), 722511 restaurants
  (11). Home caterers, home hairdressers, home nail technicians - exactly the
  pattern that got NAICS 812990 excluded in this city and in Los Angeles on
  2026-09-21, reappearing under codes that are perfectly legitimate for a
  storefront and so were never candidates for a blanket exclusion.
- **The measurement took three attempts, and the first two were wrong in ways
  worth recording.** v1 joined on `data.sfgov.org`, which returns 403 on
  `/resource/` while `/api/views/` works - it looked as though the datasets
  were unavailable when the project's own recorded domain is `data.sf.gov`. v2
  joined by address and reached only 43.8%, because the Assessor's
  `property_location` is a **fixed-width composite**
  (`'0000 2801 LEAVENWORTH         ST0000'` is
  `<secondary> <house no> <padded street> <type><4 digits>`), and because
  stripping direction words destroyed "North Point" and "South Van Ness" on
  both sides. v3 abandoned addresses entirely: the roll carries `the_geom` as a
  **point**, so a nearest-parcel join in EPSG:32610 matched **93.4% at a median
  distance of 1.4 m**.
- **43.8% was not good enough to filter on, and that mattered.** A filter
  running off a partial address join would have removed home businesses only
  where the address text happened to match - arbitrary in a way that is worse
  than not filtering, because it looks complete.
- **The mixed-use lesson held for a third city.** San Francisco's largest
  category under its pins is **Multi-Family Residential at 5,733** - ground-
  floor retail in residential buildings - so it is excluded from the filter
  exactly as Philadelphia's `APARTMENTS > 4 UNITS` and New York's
  `Multi-Family` were.
- **Not yet filtered.** The fix needs the Assessor roll added as a San
  Francisco source and a spatial join in its step 2, which is a real change to
  a built city rather than a line of config. Raised with the measured numbers
  rather than actioned in passing; see `PLAN.md`.

### 2026-09-21 - Residence exposure checked across all six cities

- **Philadelphia's finding made every other city's residence figure suspect, so
  all five were checked before moving on.** Result: **three are now settled and
  need nothing, and none of the three needed a filter except Philadelphia.** The
  work was worth doing mainly for what it ruled out.
- **New York: measured 0.02%, no filter needed.** Two of its four registries
  carry `bbl` (NYC's tax-lot id) - DOHMH on 99.4% of rows, DCWP on 80.8% - so
  PLUTO (`64uk-42ks`, 858,284 lots) joins **by key rather than spatially**,
  which is far cheaper than Philadelphia's. 62.6% of mapped rows joined (the
  two NYS state registries carry no BBL). Of 62,444 rows, only **115 sit on a
  "One & Two Family" lot (0.18%)**, and just **10 of those display a
  person-like name (0.02%)** - all with `units_res=2` and all ordinary trades
  (Pizza, Coffee/Tea, Caribbean, Electronics Store, Secondhand Dealer), i.e.
  shops in two-family rowhouses.
- **That also turned the decision to keep New York's 161 surname-first DCWP
  names from a precedent-based call into an evidence-based one: exactly ONE of
  them is on a residential lot.** The earlier entry justified keeping them by
  analogy to San Diego; this measures it.
- **The mixed-use trap reproduced at scale.** New York's single largest
  land-use category is `4 Mixed Residential & Commercial` with **20,257 pins**,
  ahead of `5 Commercial & Office` at 14,251. Had the Philadelphia filter used
  land use alone, or counted mixed use as residential, it would have removed a
  third of New York's map.
- **Chicago: already clean, and the recorded claim verified.** Its
  `business_activity` field marks home-based businesses explicitly ("Other Home
  Based Businesses", "Home Repair Services (Home Based Business)" - 4,207 raw
  rows mention home or residential), and **zero** survive into
  `businesses_clean.csv`: the `chicago_license` taxonomy already drops them.
  The 20 residual mentions are "Home Repair Services" as a *service offered* by
  merchandise retailers, which are real storefronts.
- **Signals found but not yet built, with endpoints recorded** so the work is
  scoped rather than researched again:
  - **San Francisco** - "Assessor Historical Secured Property Tax Rolls"
    (`wv5m-vpq2`, PDDL) carries `use_definition`, `property_class_code`,
    `number_of_units` and `exemption_code_definition`, the homeowner's
    exemption that is California's homestead analogue. Its registry has no
    block/lot, so it needs a spatial join via Parcels (`acdm-wktn`, PDDL)
    first. The standalone Land Use layer (`fdfd-xptc`) is **[ARCHIVED]** and
    should not be the primary source.
  - **Los Angeles** - `public.gis.lacounty.gov/public/rest/services/
    LACounty_Cache/LACounty_Parcel/MapServer/0` exposes AIN/APN and address but
    not owner data (restricted by California Government Code s7928.205), and
    the use-type attribute lives in the separate Assessor Parcels tabular
    dataset, joinable by AIN. Two steps, so medium effort.
  - **San Diego** - the weakest position and the one with no signal at all
    today. SANDAG/SanGIS parcels carry `ASR_LANDUSE` (91 types) and
    `NUCLEUS_USE_CD` (225 types), but the hosted layers are split
    geographically (`Parcels_South` and siblings) and the registry has no
    parcel id, so it needs a spatial join across several layers.
- **Decided: leave those three to the pre-deploy batch, San Diego first.** The
  measured prior across the three cities that could be checked is 0.02%, 0.00%
  and 8 pins, so the expected exposure elsewhere is small - but San Diego is
  ranked first because its residence figure is not merely low, it is
  **unmeasurable**: its `address_suite` holds bare values ("A", "101") with no
  APT/STE token, and 903 of its pins display a name identical to the owner's.
  A low number and no number are different things, and only San Diego has the
  latter.

### 2026-09-21 - Testing the residence signals: one works, one is worthless

- **Tested the two signals the previous entry proposed, instead of trusting
  them.** The unit-indicator residence test can only fire on an
  `APT`/`FL`/`RM`/`#`, so a sole trader at a detached house reads as clean -
  which is why Philadelphia measured 0.00%. Both candidates were checked
  against the City's own property register (`opa_properties_public`, 583,779
  rows, joined on `opa_account_num`, matching 94% of licences).
- **A mailing address matching the premises is worthless as a signal: 41.9% of
  mapped pins.** A shop's mailing address is normally its own premises. It was
  removed from `PLAN.md` as a thing to build rather than left there to mislead
  someone later, and Philadelphia's pipeline downloads no mailing address at
  all.
- **Parcel land use works, but is NOT a privacy signal on its own, and this is
  the generalisable part.** In a dense city, shops sit inside residential
  buildings: "purely residential parcel" flags 7.95% of pins, including **147
  thirty-plus-seat restaurants on `APARTMENTS > 4 UNITS` parcels** and 92 on
  `MULTI FAMILY`. Acting on land use alone would have deleted hundreds of real
  storefronts to remove a few dozen homes.
- **The best signal was one not proposed: the homestead exemption**, which
  Philadelphia grants only on an owner's primary residence - a claim the owner
  made to the City, not an inference. It also over-fires alone (2.22% of pins,
  of which 162 are `MIXED USE`).
- **So 0.00% was a false negative, and the corrected figure is ~0.1-0.5%.** The
  model's *conclusion* survived - the exposure is still negligible and every
  affected row is a licensed food premises - but its *precision* did not, and
  the number it reported was wrong.
- **Filtered the narrow, defensible set: 8 pins.** A person-like displayed name
  AND an `Individual` entity AND a parcel the City classifies as purely
  residential. All 8 are `SINGLE FAMILY`; 5 are "Food Preparing and Serving"
  and 2 are caterers, i.e. home kitchens. Framed as **scope first** - a food
  licence at a house the owner lives in is not a storefront - which is the same
  framing as `Rental` and the project-wide NAICS 454 exclusion.
- **Reversed course on including the homestead exemption as a filter
  condition.** An earlier version used it as an alternative to the land-use
  test and removed 17 rows - but 8 of those sat on `MIXED USE` parcels, the
  rowhouse with a shop below and the owner's flat above, which is a real
  storefront and arguably Philadelphia's most characteristic one. Deleting
  those contradicted both the filter's own justification and the reasoning that
  kept San Diego's sole proprietorships. The exemption is now **reported by
  `check_personal_exposure.py`, not acted on**: it names 11 person-like pins on
  owner-occupied parcels and says in the output why they are kept.
- **`MIXED USE` and `APARTMENTS > 4 UNITS` are deliberately absent from
  `PARCEL_RESIDENTIAL`**, with the counts that justify it in the config
  comment, because that is the mistake a future reader is most likely to
  "correct".
- **Written into the `add-city` skill's Step 0**, since it applies to every
  city: check for a joinable property register, and pair an occupancy signal
  with a name or entity-type test rather than acting on either alone.

### 2026-09-21 - One published email address, and a gap in the exposure check

- **Found exactly one email address published across all six maps**, in New
  York: a DCWP "Tobacco Retail Dealer" pin whose registered business name *is*
  a personal Gmail address, displayed at a mapped coordinate. Found while
  grepping the repo for an unrelated reason, not by any check the project runs.
- **`scripts/check_personal_exposure.py` could not have caught it.** It tests
  whether a displayed name looks like a *person's name* and whether the address
  carries a unit indicator. An email address matches neither test: it fails the
  `PERSON` regex and contains an `@`, which `NOT_A_NAME` does not list. So the
  check reported this city as clean on its own terms and was right to - the
  terms were incomplete. Contact details are a different exposure from names,
  and arguably a worse one: a name at a commercial address identifies a
  business, while an email address is a direct line to a person.
- **Counted first, across every city, before deciding anything**: 1 email and
  0 phone numbers in 91,000 pins. So this is one row, not a pattern - which is
  why it is recorded as its own decision rather than folded into a sweep.
- **Decided: scrub contact details in shared code.** A displayed name holding
  an email address or phone number is treated as a row with no usable public
  trade name and dropped, the way a blank one would be - masking to
  `JO***@GMAIL.COM` would still leak a partial. Implemented as
  `drop_contact_details()` in `pipeline/map_common.py` and applied inside
  `render_heatmap`, deliberately **not** in the step 2 of the city that
  happened to have the problem: that is the one place every city's pins pass
  through, so a city added later cannot reintroduce it by forgetting.
- **It was 3 rows, not 1.** The first count came from scanning the rendered
  pin arrays, which hold only the within-ring layer; two more sat in the
  all-city toggle set. New York went from 44,361 to 44,360 within-ring pins and
  62,444 to 62,441 available. Every other city dropped nothing, so the
  shared-code placement cost five cities a re-render and changed none of them.
- **Decided: keep New York's 161 surname-first names.** They are DCWP licence
  holders - Newsstand 92, Tobacco Retail Dealer 35, Secondhand Dealer 16 -
  trading at licensed commercial premises where the registry holds no separate
  trade name, which is the situation San Diego's 903 sole proprietorships were
  kept for. Removing them would delete real licensed businesses from an
  already-thin Retail category. Recorded rather than actioned.
- **Extended `scripts/check_personal_exposure.py` to screen four things it
  could not see before**, at the project owner's instruction: contact details
  (email, phone), surname-first names, a person's name followed by a trade name
  in brackets, and `ATTN:`/`c/o` markers naming a person. Each is reported as
  its own line rather than folded into the existing person-name percentage, so
  the figures quoted in earlier entries stay comparable.
- **The first version of the `c/o` pattern was wrong, and measuring caught
  it.** `\bC[/.]?O\b` makes the separator optional, so it matched the bare
  abbreviation "CO" and flagged 567 company names across five cities
  ("ROMANIAN KOSHER SAUSAGE CO", "GRAMERCY TYPEWRITER CO"). Requiring the
  separator took it to 6 genuine hits. A privacy check that cries wolf 567
  times is worse than none, because the real hit is unfindable in the noise.

### 2026-09-21 - Philadelphia built: two buckets, one registry, two station rules

- **Built Philadelphia as the sixth city, and the first with only two of the
  three buckets.** One registry (L&I Business Licenses via the Carto SQL API),
  94 in-city SEPTA Metro stations across 4 drawn lines, 8,512 mapped sites -
  Food service 7,485 and Retail 1,715 - from 9,200 downloaded rows. Rendered
  map 1.19 MB.
- **Personal services is absent, and no source exists to add.** Philadelphia
  licenses no salon, barber, nail, cosmetology, massage or laundry business:
  an `ILIKE` sweep across both Carto licence tables returns nothing.
  Pennsylvania publishes professional licensees only as county aggregates
  (`fwj2-whnj`, no addresses) and its PALS system answers one licence at a time
  with no bulk export. **Decided: build the city and state the gap** on its
  page and in `docs/excluded_categories.md` under what is *missing* rather than
  *excluded*, because everything else on that page was a choice and this was
  not. The alternative considered and rejected was skipping the city to keep
  every built city at three buckets.
- **The multi-source approach was attempted and failed, which is the finding.**
  All four candidates were checked live and each is recorded in
  `docs/data_sources.md` so the search is not repeated: PA Agriculture's food
  inspections relay the city's own data (`organization_name` is "City of
  Philadelphia"); the Commercial Activity License file - the general licence
  every city business needs - has **0 of 528,413 active rows with geometry**,
  no business address, and `licensetype` fixed at the single value "Activity";
  `li_business_licenses` is a stale copy of the registry used (360,192 rows vs
  435,143). So the `multi-source-city` skill's conclusion for this city was
  "there is no second source", which is a valid answer to its Step 1.
- **Two licence types were misread from their names, and sampling caught both.**
  `Vendor - Motor Vehicle Sales` is not car dealers - it licenses vending
  *from* a vehicle, and its holders are food trucks ("CHA CHA LUNCH TRUCK",
  "FOOD TRUCK COLLECTIVE LLC"), so it is excluded as mobile rather than counted
  as Retail. Conversely `Food Establishment, Retail Perm Location (Large)` is
  not supermarkets only but the general-retail tier - Target, CVS, Dollar Tree,
  Staples, Ross Dress For Less - which hold a food licence because they sell
  packaged food, and are the only way this city's data sees a chain clothing or
  office-supply store at all. All 50 active types now carry an explicit verdict
  in `pipeline/taxonomies/phl_licensetype.py`.
- **Excluded `Rental`, 79% of the file, as a scope error first.** 93,471
  residential landlord registrations, on which the registry's business-name
  field holds the owner's own name at their property with
  `legalentitytype='Individual'`. Mapping active licences unfiltered would have
  published ~94,000 individuals at their homes. Framed as scope (not
  businesses, not storefronts) because that is the easier call to justify and
  it fixes the privacy problem as a consequence - the same shape as the
  project-wide NAICS 454 exclusion. `Limited Lodging Operator` (589) went with
  it.
- **Corrected a Step 0 measurement error: coverage is 97.6%, not 100%.** The
  probe counted `the_geom IS NOT NULL` and got every row, but 218 rows hold an
  *empty* point geometry, on which `ST_X`/`ST_Y` return NULL. **Decided: drop
  them without a geocoding step.** The loss is not uniform - it takes 61 of the
  75 newsstands - but geocoding cannot fix that bias, because 60 of those 61
  carry no street address either; the 79 rows that are recoverable are 0.86% of
  the file, which does not justify a geocoder, a cache and a step renumber.
  Step 2 prints the drop by licence type so the bias is visible in every run
  rather than only in this entry.
- **Line scope: L, B, T and G; Regional Rail excluded.** M1 (Norristown High
  Speed Line) and D1/D2 (routes 101/102) needed no decision - both begin at
  69th Street in Upper Darby and have **zero** in-city stops. Regional Rail has
  52 well-spaced in-city stations (857 m median) and was still excluded, to
  match Chicago leaving out Metra and New York leaving out the LIRR and
  Metro-North; SEPTA's own branding separates it from SEPTA Metro. It is the
  obvious later addition, and needs no thinning if that call changes. The
  rejected alternative was L + B alone (47 stations), which would have drawn
  only two lines and left West Philadelphia and Girard Avenue blank.
- **First city needing two station rules at once.** L and B are grade-separated
  at 711 m and 681 m median spacing, so every in-city station is kept, as in
  San Diego. T (five trolley branches) and G (Girard) are street-running at
  134-137 m median with a 10th percentile of 17-19 m - San Francisco's shape -
  so they take the four-filter thinning in `docs/sub_transit_line_filters.md`.
  Result: 261 trolley stops to 90, T1-T5 keeping 13/14/15/16/17 of 38/29/39/46/42
  and G 15 of 57. All 167 cut or out-of-city stops are documented in
  `outputs/philadelphia/excluded_stations.csv`.
- **Generalised filter 4 from routes to line groups, which changed the
  result.** San Francisco's version force-keeps any stop shared by 2+ routes as
  a transfer point; there, every route was its own line, so the two readings
  were identical. In Philadelphia all five T branches share the Center City
  tunnel and T4/T5 additionally share the whole Woodland Avenue segment, so the
  route-level reading force-kept five consecutive stops inside 400 m and
  quietly defeated the thinning. Group-level interchange (2+ of L/B/T/G) gives
  6 real transfer points and drops T4/T5 from 20/21 kept to 16/17.
- **The near-duplicate distance check earned its place.** It flagged
  `Girard Av & Front St` 6.7 m from `Front-Girard` and `Girard Av & Broad St`
  18.4 m from `Broad-Girard` - a trolley stop sitting on top of the
  rapid-transit station it interchanges with, under names sharing no detectable
  suffix pattern. Both are now hand-curated aliases, exactly the residue
  `docs/sub_transit_line_filters.md` predicted would be left after the regex
  pass.
- **Deduplicated on address AND name, adjunct licences ranked last.** One
  storefront can hold several licences, so there is one row per normalised
  address + business name with the most specific licence deciding: 8,982 rows
  to 8,512 sites. Of 317 adjunct rows (sidewalk cafe, streetery, outdoor
  seating), 243 collapsed into the restaurant that also holds a primary licence
  and 74 survive as the only licence at their site. All 8,512 fall inside the
  city polygon.
- **Display the trading name, not the licence holder.** This registry formats
  `business_name` as "LEGAL NAME (TRADE NAME)", so where the legal entity is an
  individual the raw field publishes their own name in full: "BRIAN WANG (FOUR
  SEASON JUICE BAR #89)", "Andrew Polhemus (Molto Bene Ravioli Co)", and
  "CVS PHARMACY INC (ATTN: JOANNE P. AMITRANO)" naming a corporate employee.
  Step 2 now chooses the displayed name instead of copying it: prefer a
  bracketed name that is neither a contact nor a person, else the text outside
  the brackets, else the registered name as it stands. Rewrote 2,900 of 8,512
  rows, **456 of which removed a licence holder's own name from a pin.** It is
  also the better label - "AZAAN GROCERY STORE" beats "A AND A II INC" - which
  is why the bracket is preferred rather than merely stripped.
  - **A bare personal name with no alternative is still published** ("Amanda
    Girard"): that is the trade name the owner registered, a deliberate public
    commercial act, per the San Diego reasoning in `naics.py`.
  - **The person-shape regex alone was not enough**, and getting it wrong was
    instructive: "STARBUCKS CORPORATION" is two alphabetic words, so without an
    organisation-token guard the rule classed it a person and preferred the
    bracket. That inflated the rewrite rate before the guard was added.
- **Privacy verdict: publish.** `scripts/check_personal_exposure.py` (with
  Philadelphia added, and extended to read a structured entity-type column):
  4,958 pins, no registrant-name fallback *possible* - six name-bearing columns
  are never downloaded and step 2 asserts their absence, and `business_name` is
  never blank in this registry. 296 pins (6.0%) read as a person's name and
  **all sit in food-service categories**, i.e. premises that must be inspected,
  with no catch-all sweeping in home-based sole traders. 1,270 of 8,512 rows
  are `legalentitytype='Individual'` (14.9%), 190 pins are both Individual and
  person-like (3.83%), and **0.00% sit at a residential unit indicator**.
- **That person-like count went UP after the rename, from 207 to 296, and the
  increase is honest rather than a regression.** A composite string like
  "Brian Wang (…)" always displayed a person's name; the bracket simply
  defeated the heuristic, which rejects any string containing punctuation.
  Removing the bracket let the check see what was already on the map. The
  measured exposure rose because the measurement improved, and the structural
  facts did not move: no residential units, no registrant fallback, all
  inspected premises.
- **One blind spot named rather than closed:** the residence test only fires on
  an `APT`/`FL`/`RM`/`#` indicator, so a sole trader at a *detached house* reads
  as clean - which is part of why this city scores 0.00%. Two unused signals
  could close it, both available here: `business_mailing_address` matching the
  premises address (not currently downloaded), and parcel land-use via
  `opa_account_num`. Logged as future work, not claimed as done.
- **Wired `legalentitytype` into the exposure check as a general mechanism.**
  Philadelphia is the first city whose registry records entity type
  structurally, so for it the name heuristic is the cross-check and the
  publisher's own field is the measure - the reverse of every city before it.
  Added as `entity_type`/`entity_individual` keys in `REGISTRIES` so a later
  city with the same signal needs no new code.
- **Two licence questions raised and left open**, per the `multi-source-city`
  skill's instruction not to read a clause generously: SEPTA's bar on using its
  "trademarks and copyrighted materials for any commercial or profit-making
  use" (the map uses its real line names and official `route_color` values, and
  no logo or route-bullet artwork), and the "City of Philadelphia License",
  which reserves all database rights, grants nothing explicitly, forbids
  nothing explicitly and requires no notice. Neither blocks the build; both
  should be settled before the public deploy. Philadelphia added **no new
  mandatory notice**, so that count stays at four.

### 2026-09-21 - Probe output belongs in the scratchpad, not the home directory

- **Deleted eight Step 0 research captures from the home directory**, left
  there by the 2026-09-18 city screening: `la.json`, `la_sample.json`,
  `phila_sample.json` (raw WKB hex for geometry that turned out not to need
  parsing), `phila_tables.json` (41 bytes of
  `{"error":["system tables are forbidden"]}`), `phila_search.json` (HTML under
  a `.json` name), and three saved OpenDataPhilly pages including a 404 and a
  283 KB dataset listing.
- **Decided not to integrate them into the repo.** They are raw API and HTML
  captures - the category this project already gitignores as
  `data/<city>/raw/` - and every finding in them is superseded and now recorded
  properly in `docs/data_sources.md` and `docs/city_shortlist.md`. Committing a
  saved 404 and a misnamed file to a public repository would be worse than
  having nothing.
- **Added the rule that prevents a repeat** to `CLAUDE.md`'s working rules and
  the `add-city` skill's Step 0: every probe gets an explicit output path under
  the session scratchpad or a gitignored raw folder, because `curl -o la.json`
  writes wherever the shell happens to be. Two unrelated personal files in the
  same directory were identified, left untouched, and deliberately not read.

### 2026-09-21 - Overview colour sweep: one real fix, two non-defects

- **Swept the last hardcoded colours in `app/`.** All seven literals in
  `Overview_&_Introduction.py` now derive from `pipeline/theme.py` via a new
  `rgb_list()` helper (pydeck takes channel lists, not CSS), so the macro map
  cannot drift from the rest of the chrome. The only literal deliberately left
  outside the palette is the amber hover highlight, which exists to differ from
  both the teal marker and the category colours.
- **One real inconsistency fixed: the macro map's tooltip.** It was baked at
  `#1c2b2a` on white - the light theme's *text* colour used as a background -
  so in dark mode it stayed green-grey while every city map's tooltip was
  slate. It is the one macro-map element CSS can reach, because deck.gl renders
  it as an HTML overlay (`.deck-tooltip`) rather than in WebGL, so
  `app/components.py` now overrides it under `body.dark-base`. Verified it
  beats pydeck's inline styles: measured `#131C2E` / `#E6EDF7` / `#23304A`
  against a synthetic tooltip carrying the inline values.
- **The constraint that shapes the whole macro map, now written down.** Marker
  and label layers are WebGL, so CSS cannot restyle them, and one colour set
  must serve both basemaps. The light basemap's land is `#f2efe9` and the
  inverted dark one `#191c22` - opposite ends of the luminance range - so **no
  single colour can clear 3:1 against both.** That is why each city name gets
  an opaque pill: the pill supplies its own background, and the text only needs
  contrast against the pill (14.7:1). It is a design answer to a hard limit,
  not a stylistic choice, and it should not be "simplified" away.
- **Two flagged failures were my measurement criterion being wrong, and are
  recorded so a later pass does not chase them.** The pill reads 1.15 against
  the light basemap, but a text background does not need to contrast with what
  is behind it - its text does. The marker's white ring is likewise decorative
  on the light basemap and load-bearing on the dark one, with the marker
  discernible either way through its fill. Checking contrast numerically was
  right; applying a text criterion to a background was not.
- **One accepted weakness, stated rather than hidden:** the amber hover
  highlight is 1.45 against the light basemap. Unfixable within a single colour
  set for the reason above, and hover also enlarges the marker and opens a
  tooltip, with amber differing from teal by hue rather than luminance - which
  a WCAG ratio does not capture.
- **What to re-check if the palette ever changes:** the teal marker fill is the
  only element that clears 3:1 on both basemaps (3.26 light, 4.56 dark), and
  its margin on the light side is thin. A darker or lighter teal breaks one end.

### 2026-09-21 - Maps follow the page's theme; an explicit click still wins

- **Closes the two-controls gap** opened by giving the page a theme. Chosen
  from three options (recorded in the previous entry's `PLAN.md` note):
  **maps default to the ambient theme, a manual click wins from then on.**
  - Rejected **(B)**, letting our button drive the page and styling Streamlit's
    chrome from `body.dark-base`: it means overriding framework widget colours
    by hand, which is exactly the cost the handoff measured as the real work,
    and it would have meant throwing away the theme chooser we had just
    recovered.
  - Rejected **(C)**, removing the in-map button when embedded: conceptually
    the cleanest - one control per context - but it discards the in-map toggle
    the `#map-actions` group is built around, and standalone maps would still
    need their own, so the mechanism was needed either way.
- **Detection reads the host page's background brightness, not a framework
  API, because there is no API.** Streamlit exposes no theme signal: no
  `data-theme` on `<html>` or `<body>`, no CSS custom property. The page
  background does reflect whichever of System / Light / Dark the visitor chose,
  and a map iframe is same-origin with its host, so one luminance read covers
  all three. `prefers-color-scheme` alone was rejected as the primary signal -
  it only matches the default System case and is wrong the moment someone picks
  Light or Dark explicitly - but it is the fallback for a standalone map, which
  has no host to read.
- **The rule lives once**, as `AMBIENT_THEME_JS` in `pipeline/theme.py`, used
  by both the city maps and the macro map, consistent with that module already
  being the single source for colours.
- **Verified all three behaviours**, not just the happy path: with no stored
  choice on a dark page the embedded map opens dark and its body background
  matches the page exactly (`#0B1220`, `storedTheme: null`); a click stores
  `light` and flips the map; and after a reload on a still-dark page the map
  stays light. The macro map behaves the same way from its 1px script frame.
- **A debugging lesson worth more than the feature.** The first test showed the
  code apparently not working - maps stayed light on a dark page. The code was
  correct; **Streamlit was serving a cached `components.py`**, and the live
  iframe's `srcdoc` did not contain the new function at all. Editing an
  imported module and reloading the page is not enough: stop the server, clear
  `__pycache__`, restart. The `deploy-verify` agent's procedure already says
  this, which is why it clears caches at step 1 - the instruction existed and
  was not followed. Now also in `docs/theming.md`, with the two-second check
  that would have caught it immediately: assert the injected script is present
  in the rendered `srcdoc` before debugging its behaviour.

### 2026-09-21 - Midnight slate: page themed, palette unified, one gap left

- **The page theme is in, and Streamlit's theme chooser is back.** Verified
  empirically rather than assumed, because the handoff's warning was written
  about another project: with the previous bare `[theme]` block the main menu
  offered only Rerun / Auto rerun / Clear cache / Print / Record screen - **no
  Settings item at all**, so the old comment in `config.toml` claiming visitors
  could switch via the hamburger menu was **already false before this change**,
  not made false by it. Defining `[theme.light]` and `[theme.dark]` restored a
  System / Light / Dark chooser, and the page now renders `#0B1220`.
- **The palette had a second, undocumented home.** `app/components.py` carried
  its own literal copies of `#182322`, `#e6efee`, `#2e403e`, `#1f2d2c`,
  `#8fa3a1`, `#5eead4` and `rgba(15,23,22,0.8)` for the macro map's chrome,
  mirroring `map_common.py` with no shared source - so a reskin of one would
  have produced a navy city map beside a teal macro map. Found by grepping for
  hardcoded colour before editing, which is what the handoff said the real work
  would be.
- **`pipeline/theme.py` is now the single source** for every chrome colour,
  light and dark. It imports nothing, so `app/` can read it under the lean
  deploy venv, the same rule the city pages' config imports already follow.
  Both the map CSS and the macro-map CSS build from it, with an assertion that
  no placeholder is left unresolved. Business-category and transit-line colours
  are deliberately NOT in it: those are data, not chrome.
- **Two selector traps made structurally impossible.** The dark rules match on
  `[stroke="#2c3e50"]` (rings) and `[stroke="#1a5490"]` (stations), which only
  works because each colour is used nowhere else - and `docs/theming.md`
  records that changing either light value silently breaks its dark rule. The
  selector and the drawing code now read the same `LIGHT` entry, so they cannot
  drift. The dark label halo and attribution strip also stopped re-typing the
  page colour as literal channel values (`rgba(15,23,22,0.8)`); they derive it.
- **`scripts/check_theme_sync.py`** exists because TOML cannot import, making
  `.streamlit/config.toml` the one unavoidable duplicate. It compares both
  variants against `pipeline/theme.py` and fails on a mismatch, a missing
  variant, or a colour set on the bare `[theme]` table where it would silently
  apply to both. Currently: 10 values in sync.
- **The gap, stated plainly: there are now two independent theme controls on
  one page.** Streamlit's chooser drives the page; our own button drives the
  maps. Measured immediately after the change: page background `#0B1220`
  (dark), `body.dark-base` absent (maps light), and a white map button on a
  dark page. Nothing is broken - no error blocks - but it is visibly
  incoherent, and it is a direct consequence of giving the page a theme at all.
  Options and a recommendation are in `PLAN.md`; not resolved unilaterally
  because it changes visitor-facing behaviour.
- Useful finding for whichever option is chosen: **Streamlit exposes no theme
  signal** - no `data-theme` attribute on `<html>` or `<body>`, no CSS custom
  property. But the page background reflects whichever of System / Light / Dark
  the visitor picked, and the map iframes are same-origin, so a luminance read
  of the parent's background detects all three. `prefers-color-scheme` alone
  would only match the default System case.

### 2026-09-21 - Two theme handoffs merged into docs/theming.md

- **Decision: one theming document, not two.** `dark_mode_handoff.md` and
  `midnight_slate_theme_handoff.md` described the same surface from different
  moments and disagreed in places - the older one still specified a
  base-layer-radio toggle that was never built, while the newer one referenced
  its `--dm-*` table as if it were current. That is the same
  two-sources-of-truth failure that left San Francisco's boundary endpoint
  recorded nowhere: harmless until someone needs it, then actively misleading.
- **`docs/theming.md` is now the single reference**, ordered by usefulness
  rather than chronology: current implemented state, the decided palette,
  what is not yet built, the traps, the verification checklist, and
  superseded designs last and explicitly labelled "provenance only, do not
  implement".
- **The superseded design is summarised, not deleted, and its code is not
  reproduced.** The base-layer approach and *why the fixed button beat it* are
  worth keeping - the map is 1000px wide while Streamlit's column is often
  narrower, so a control anchored to Leaflet's top-right corner can sit
  off-screen, which is the same root cause as the legend and phone-width work.
  The code itself lives in git history rather than in a file that reads like
  instructions.
- **What the merge preserved from the older document**, because it was still
  true and would have been lost: `dark-base` belongs on `<body>` not the map
  container (the legend is outside it); the legend's light styling is inline so
  dark rules need `!important`; ring outlines are the only `#2c3e50` and
  station dots the only `#1a5490`, which is what makes the attribute selectors
  work and means changing either light colour silently breaks its dark rule;
  and the script-ordering trap - Folium renders body HTML before the figure's
  script block, so a script added there runs before the map object exists. That
  last one is the same class of bug as this session's `toggle`-event defect and
  is why `PHONE_FIT_SCRIPT` polls.
- **Both originals were committed before being merged** (`d4c3095`), so the
  received form of the midnight-slate handoff is in history exactly as handed
  over, including the two corrections made on receipt.
- **Also confirmed:** the three post-`map-chrome` fixes are verified by
  screenshot on four cities but not by an agent pass. Rather than spend another
  scoped run, they fold into the mandatory `full` run before deploy - which is
  the batching the scope policy was written to encourage.

### 2026-09-21 - Staying on Streamlit, and theming it as one palette

- **Decision: keep Streamlit.** The question was raised because a theme
  implementation was wanted and Streamlit looked like the obstacle - the
  page-level dark mode has been deferred in `PLAN.md` precisely because of it.
  Three things settled it:
  - The handoff's item 1, which it marks as *tested rather than assumed*:
    separate `[theme.light]` and `[theme.dark]` blocks keep Streamlit's own
    toggle. So an explicit theme does NOT force the site dark-only, which was
    the assumed penalty.
  - The biggest trap the handoff names - "a light Folium map on a slate page is
    a white box" - is already solved here. The maps carry their own theme and
    share one `localStorage` key.
  - Three of its seven implementation notes are already closed in this project
    (the `st.components.v1.html` migration, the `streamlit>=1.64,<2` bound, and
    the map-iframe problem above).
- **Rejected for now: replacing Streamlit with a static site.** Measured
  coupling is small - `app/` is 693 lines including comments, the API surface
  is `st.iframe`/`markdown`/`title`/`page_link`/`switch_page`/`pydeck_chart`,
  and the pipeline imports Streamlit zero times. The maps are pre-rendered
  standalone HTML and were tested all session on a plain `http.server` with no
  Streamlit running. So the rewrite is feasible and its only real work is the
  pydeck macro map. It was rejected because **it is not required for the
  theme**, and because the dependency runs one way only - the app reads
  `outputs/`, `outputs/` depends on nothing - so going static later costs
  exactly what going static now costs. No lock-in was accepted by deciding
  this way.
- **The evidence that redirected the work.** Rendering the candidate palette on
  New York and comparing it against the current one from an identical view
  showed the difference is confined to the legend, buttons, controls and the
  background strip. The map body is essentially unchanged, for structural
  reasons: the dark basemap comes from a CSS filter
  (`invert(1) hue-rotate(180deg)`) that no `--dm-*` variable touches, and the
  pin and line colours are fixed category values deliberately outside the
  theme. The eleven variables drive roughly 15% of a city page's pixels.
  **So a map-chrome reskin on its own is not worth doing**, and the payoff is
  page-level - which is the tier that needs Streamlit.
- **Therefore: one palette, landed together.** `.streamlit/config.toml` with
  both light and dark blocks, and the map's `--dm-*` values swapped to the
  matching slate values in the same change. An earlier framing offered "map
  palette now, or wait for the page" as a choice; that was wrong. The handoff
  supplies both sets from a single palette, `#0B1220` page against `#131C2E`
  surface is a designed relationship, and the map surface can only be judged
  against the page behind it. Page first, so there is something to match.
- **Two deviations from the handoff, both measured rather than preferred:**
  - **Keep our teal accent `#5eead4`** (12.7:1 on the new page) rather than its
    `#4C9AFF`, which the file itself calls a placeholder that "reads as another
    project's look".
  - **Do not use `#4A5A78` for `--dm-disabled-text`** - it measures 2.7:1 on
    page and 2.5:1 on surface, below the 3:1 non-text floor. It is one of the
    four values the file marked "(suggested)" rather than designed, so its own
    caveat flagged the right one. The preview used `#5A6B8C`.
  - Every contrast figure the handoff states was recomputed and matched to the
    stated decimal, which is why its untested palette was trusted this far.
- **Still to decide when this is built:** whether to follow the visitor's
  system theme (`prefers-color-scheme`) with a manual override winning once
  used, which the handoff reports as implemented and verified elsewhere. This
  project is manual-only today. Its trap comes free with it: devtools
  colour-scheme emulation updates `matchMedia().matches` without dispatching
  `change` inside an iframe, so it cannot be tested that way.

### 2026-09-21 - Three fixes from a scoped verify, and a measurement lesson

- **The legend breakpoint was broken on a wide load - my bug, found by the
  first scoped `map-chrome` run.** Chrome queues a `toggle` event for a
  `<details open>` element that lands *after* an inline script attaches its
  listener. On a narrow load `fit()` had already set the guard flag, so the
  stray event was consumed; on a wide load `fit()` returned early without
  setting it, the stray event hit the "user touched it" branch, and the
  breakpoint was dead for the life of the page. A reader who loaded wide and
  then narrowed still got four of New York's labels covered - the original
  defect, reachable by a different route.
  **Fix:** detect reader ownership from a `click` on the `<summary>`, not from
  `toggle`. `toggle` fires for programmatic changes too, which was the whole
  ambiguity; a click is unambiguous and keyboard activation dispatches one.
  Verified: load at 1200 (legend open, 403px) -> narrow to 854 -> collapsed to
  37px, zero labels under it.
- **The container landed ~15px short of the frame.** At load the 1000px map
  forces a horizontal scrollbar, which costs enough height to force a vertical
  one, so `clientWidth` reads short - and nothing dispatches a resize event
  afterwards to correct it once the scrollbars go away. Fixed by applying the
  fit more than once (rAF plus 120/400/1200ms); `apply()` returns immediately
  when the width already matches, so the extra passes cost nothing. Container
  now reaches the full frame width on every city.
- **Line labels were cropped off narrow frames because the fit used STATION
  bounds.** A label sits beyond its line's tip, outside those bounds.
  `_choose_view` already fits the desktop view to stations *and* labels
  together; the phone fit now does the same, with padding raised to [26, 18]
  because the emitted bounds hold label anchors and a label's text box extends
  past its anchor.
- **The measurement lesson, which is the most reusable part.**
  `getBoundingClientRect()` on a line label is unreliable in the browser pane
  and produces convincing false failures: a marker element reported a rect at
  x=490 while its own `style.transform` said 212px, with the map pane at
  identity and no page scaling. The scoped run reported "three of San
  Francisco's six labels entirely off screen" and "two of Los Angeles' six" on
  that basis; screenshots of the same frames show **every** label on every
  city rendered and legible, a few clipped at an edge. The rects were stale
  because the pane was not compositing.
  So: screenshots are the authority for label geometry, rect-derived counts are
  a hint, and properties (`details.open`, computed colour, `style.width`,
  cluster leaf counts) are reliable where a check can be expressed that way.
  Written into the `deploy-verify` agent, because it is the opposite of that
  file's usual DOM-over-screenshots advice and would otherwise keep generating
  false findings. It also means the earlier "1 of 11 visible" reading that
  nearly went into a report was the same artifact twice over.

### 2026-09-21 - Phone-width maps fixed by resizing after init, not before

- **The problem `deploy-verify` found:** at 375px the iframe showed a ~343px
  slice of a 1000px map, so the reader had to scroll inside the iframe to find
  anything. 1 of New York's 11 line labels was visible, 0 of Chicago's 7.
- **The fixed 1000px width could not simply be dropped** - it is what avoids
  Leaflet.heat's uncaught `IndexSizeError` on init with an unresolved container
  size, which silently kills every layer added afterwards. The insight is that
  the bug is about an *unresolved* size at construction, not a *small* one: the
  container can keep its fixed size through initialisation and be resized
  immediately afterwards via Leaflet's own `invalidateSize()`, then re-fitted to
  the station bounds. Prototyped in the browser on a rendered map before writing
  any code, which is how the approach was confirmed rather than assumed.
- **Result at 375px:** New York 1 -> **9 of 11 labels fully visible, 0
  off-screen**; Chicago 0 -> 6 of 7; horizontal scroll inside the iframe gone;
  heat layer intact. Desktop unchanged - at 1200px the container is still
  1000px, the view is the original, and all 11 labels show. The station bounds
  come from Python rather than the script sniffing marker colours.
- **What it does not fix, stated rather than glossed:** `_layout_labels` picks
  label positions server-side against a 1000x650 canvas, so at phone width
  labels can crowd each other and the cluster badges, and one or two clip at an
  edge. Correct phone layout needs a second render at phone dimensions, which
  would roughly double `outputs/` and render time - logged in `PLAN.md`, not
  started, and worth doing only if phone traffic matters.
- A measurement note, since it nearly produced a wrong report: label counts
  taken in the same batch as the page load read 1 of 11, because the fit script
  polls and had not settled. The settled figure is 9. Measure after the state
  settles, not in the same round trip.

### 2026-09-21 - Licence checking is now part of adding a city

- **The review was retrospective; this makes it routine.** Recording endpoints
  was already an `add-city` Step 0 requirement, but recording *licences* was
  not, so the next city would have repeated the same gap the 2026-09-21 review
  had to close for five cities at once.
- Step 0 gained a fourth item covering, per source: the declared licence (and
  where Socrata exposes it), the governing terms when none is declared, the
  transit feed's terms *separately* (they were the loosest end of the review,
  and `feed_info.txt` almost never carries a licence), anything the project
  must display, and anything needing a human decision. Step 9 re-checks that
  the rows actually landed.
- Two traps from the review are written into the skill so they are not
  repeated: a missing Socrata `license` field does not mean permissive, and a
  parent site's general footer is not the data's terms - reading nyc.gov's
  "All Rights Reserved" as governing NYC Open Data produced exactly the wrong
  conclusion, when Local Law 11 in fact forbids the city from imposing a
  licence at all.
- The standing removal-request commitment covers new cities automatically, and
  the skill says not to weaken it for a source with tighter terms: the answer
  to tight terms is to record and comply, not to hedge the commitment.

### 2026-09-21 - A standing commitment to honour removal requests

- **Checked whether the agencies showcase third-party work, and they do not.**
  The idea was to find positive precedent for how publishers interpret their
  own terms - stronger evidence than the absence of takedowns, which proves
  nothing because every licence here enforces by private written notice and
  small projects do not publicise receiving one. It was close to a dead end:
  the MTA's apps page lists only its own two apps, LA Metro's developer site
  shows only its own experimental tools, and CTA has no gallery. What the
  search did yield is each agency's own framing of intent - Metro "invite[s]
  you to use this information to help us improve *your* system"; CTA's
  Developer Center launch describes enabling third parties to build
  applications "designed to improve travel". Supportive context, not evidence,
  and recorded as such.
- **The useful conclusion was about the shape of the risk, not the precedent.**
  Every licence reviewed contemplates the same remedy: a request to stop
  displaying the data. Not damages - removal. That bounds the realistic
  downside of this project to an email asking for a layer to come down.
- **So the protection is a commitment rather than a search for reassurance.**
  Published in `docs/data_sources.md` and, in the form that speaks to business
  owners, in `docs/excluded_categories.md`: a removal request from a
  publisher, a business owner, or anyone raising a privacy concern about a
  specific pin is honoured without argument and without the requester having
  to give a reason; the pin, layer or city comes down first and the reasoning
  is recorded afterwards. Explicitly including the case where the project
  believes it is in the right - "being permitted to display something is not a
  reason to insist on displaying it" - because that is the case where a
  commitment made in advance actually does work. Also a `CLAUDE.md` invariant,
  so it binds future sessions rather than living only in published prose.

### 2026-09-21 - Licence review closed: every source established but one

- **Source-by-source review of all 19 inputs** (8 business registries, 5 GTFS
  feeds, 5 boundary layers, the geocoder) recorded in
  `docs/data_sources.md`. The working assumption going in - that a government
  open-data portal implies permissive terms - did not survive: terms ranged
  from public-domain dedications to a feed that forbids modifying its data,
  and the two extremes are the *same city* (Los Angeles' business registry is
  CC0; its GTFS is the tightest licence in the project).
- **New York City: the absent licence is required by law, not an oversight.**
  Its three datasets declare no licence, and the only terms link on the portal
  points at the general nyc.gov footer, which reserves all rights - so the
  first reading was that no reuse grant existed. The primary source settles it
  the other way: NYC's Open Data Technical Standards Manual states that Local
  Law 11 of 2012 "requires that data sets must be available without
  registration requirement, license requirement, or usage restrictions". The
  city cannot attach a licence. The nyc.gov "All Rights Reserved" notice
  covers that website's own content, not datasets published under the Open
  Data Law. One condition does attach: DoITT "may require third party entities
  such as application developers to explicitly identify the source, version,
  and modifications made to a public data set" when republishing - which this
  project already produces (`data_sources.md` for source and version,
  `excluded_categories.md` for modifications).
- **Two clauses were judgment calls, decided by the project owner** after
  being raised rather than read generously:
  - **LA Metro forbids modifying the "Transport Information".** Decided: this
    project does not modify it. The alignment is drawn from the feed's own
    `shapes.txt` and displayed as that line; nothing is altered, augmented or
    misrepresented, and the clause reads as protecting against passing off
    changed route or schedule data as Metro's. Revisit if Metro clarifies.
  - **CTA licenses its data to "assist mass transit riders or promote public
    transportation".** Decided: the project falls within that purpose - it
    shows people what businesses are near their station, which is
    rider-facing information about using the system. It is also not sold, not
    advertising, and claims no affiliation, which are the clauses the purpose
    limitation sits beside.
- **The operative finding is four notices the site must display**, now listed
  with exact wording in `docs/data_sources.md`. OpenStreetMap's is already
  satisfied by the maps' tile attribution; Chicago's verbatim disclaimer,
  SFMTA's permission notice and an acknowledgement of LA Metro as provider are
  not yet shown. Keeping the OSM attribution is now a `CLAUDE.md` invariant,
  including the point that changing tile provider swaps that attribution
  rather than removing it.
- **Only the Census geocoder's terms remain unread**, and it is used only to
  derive coordinates into this project's own outputs.
- **What this changes about the deploy:** the remaining licence work is no
  longer a permission question but an implementation one - display four
  notices - which is why it was folded into the same deferred app job as
  surfacing `excluded_categories.md` and `data_sources.md`.

### 2026-09-21 - The legend collapses itself when the frame is too narrow for the map

- **Found by the `deploy-verify` agent**, not by looking at a map at desktop
  width. Below roughly a 1130 px browser window the legend slid over the map
  and covered line labels: at a 1024 px window the app's column gives the
  iframe 854 px, and at that width four of New York's eleven labels were
  hidden (Flushing, Shuttles, Nassau St, 14 St-Canarsie).
- **The cause is the interaction of two earlier decisions, each still right.**
  The map lays out at a fixed 1000 px because Leaflet.heat throws an uncaught
  `IndexSizeError` when its container size is unresolved
  (github.com/Leaflet/Leaflet.heat/issues/95), which silently kills every
  later layer. The overlay controls are `position: fixed` so they stay visible
  while the map scrolls inside its iframe. But "fixed" anchors to the frame's
  *visible* width, whereas `_layout_labels` reserves the legend's obstacle at
  the bottom-right of the full 1000 px. Narrow the frame and the legend moves
  off the space reserved for it and onto space given to labels.
- **Fix: collapse the legend exactly when the frame is narrower than the map**
  (`LEGEND_AUTOFIT_SCRIPT`, threshold read from `_MAP_W` so there is one
  source of truth). Collapsed it is a 76x37 px "Legend" tab that covers
  nothing and is one click from open. Chosen over the alternatives: making the
  legend `position: absolute` would put it back in its reserved corner but
  require scrolling right to see it at all on a narrow frame; widening the
  label obstacle to cover every possible legend position would permanently
  spend space that is only contested sometimes.
- **A reader who opens or closes the legend owns it from then on** - the
  breakpoint stops adjusting it, so it never fights a deliberate click.
- **Verified at three widths, on two cities, and for the manual override.**
  At an 839 px frame: New York's legend auto-collapses to 37 px and covers
  **0** labels (was 4), Chicago's likewise with its 7 labels. At 1200 px it is
  open at its full 403 px and covers 0. After a hand-close at a wide width it
  stays closed across a resize event. Label positions are untouched - the
  Python-side obstacle maths did not change - so this is a script-only change
  to the rendered HTML.
- Still open, and NOT addressed here: at phone width the frame shows ~343 px of
  the 1000 px map, so most labels start outside the visible area and the reader
  must scroll inside the iframe. That is the same fixed-width cause but needs a
  deliberate mobile approach, not a breakpoint (`PLAN.md`).
- Also noted while in this code, not changed: the label layout treats only the
  legend and the top-LEFT zoom/layer controls as obstacles. The top-RIGHT
  button group (Cities / All cities / theme) is not an obstacle, so a label
  could in principle land under it; no rendered map currently shows this, and
  adding it would move labels in all five cities.

### 2026-09-21 - Staten Island Railway drawn in a lighter blue than the MTA's own

- **The one line on any city map not using its agency's official colour.**
  Every other New York trunk uses the MTA's `route_color` from the feed, which
  is the project's rule because those colours are unambiguous and what riders
  recognise. SIR's is `#08179C`, a navy at roughly L* 17. Because a line's
  permanent on-map label takes the line's own colour, that made the "Staten
  Island Railway" label hard to read on the light basemap and nearly invisible
  in dark mode, where the basemap inverts and the label does not.
- **Changed to `#4358D4`**, lightened within the same navy family so it still
  reads as SIR rather than becoming a different line. Kept violet enough to
  separate from 8 Av's azure `#0062CF` in the legend, where the two sit near
  each other; on the map itself they never appear together, Staten Island being
  a physically separate system. Checked rendered in both themes before
  committing.
- Alternatives considered and rejected: giving the label its own colour
  independent of the line (keeps MTA's navy authentic, but adds a second
  colour concept to `map_common.py` for one line), and moving SIR to a
  distinct hue such as teal (too close to the Personal services bucket's
  `#1baf7a`).

### 2026-09-21 - Map files cut ~28% by removing emitted waste, not content

- **Every city's map shrank, and no city lost anything from it.** New York's
  10.33 MB was the trigger (44,361 pins, because dense stations put 71% of its
  businesses inside a ring against Los Angeles' 24%), but both fixes were
  waste in the shared renderer rather than anything New York-specific:
  New York 10.33 -> **7.42 MB**, Los Angeles 3.49 -> **2.79**, Chicago
  2.90 -> **2.14**, San Francisco 2.40 -> **1.74**, San Diego 0.90 -> **0.69**.
- **Coordinates are rounded before they reach the HTML** (`COORD_DP` in
  `map_common.py`). Folium emits a float's full repr - `40.76248502732357`, 17
  significant digits - for something drawn as a 5-pixel dot, once per pin, per
  heat point, per ring and per line vertex. **Six** decimal places, not the
  five originally proposed: six is 0.11 m, half a pixel at OpenStreetMap's
  deepest zoom (19), so nothing is visibly moved, whereas five is 1.1 m and
  about 5 px there - a pin could sit visibly off its building. The extra digit
  costs ~0.2 MB and makes "loses nothing" literally true.
- **Station and ring-band strings are emitted once and referenced by index.**
  They repeated per pin: 44,361 pins over 496 stations and 4 bands in New
  York. The callback became an IIFE returning the marker function, so the two
  lookup tables are built once at `var callback = ...` rather than once per
  pin - FastMarkerCluster injects the callback as a statement and then calls
  it in a loop, so a naive array literal inside the function would have been
  re-evaluated 44,361 times. The business name is deliberately NOT indexed:
  at 38,167 distinct values of 44,361 a lookup table would just add a second
  copy. The raw category also stays a string, because
  `scripts/check_personal_exposure.py` parses these arrays out of the rendered
  HTML and reads that field directly.
- **Verified rather than assumed.** After the change New York's map reports 3
  cluster layers and exactly 44,361 pins with no console errors, a sampled
  tooltip resolves its station and ring correctly through the index tables,
  and the exposure check re-parses the rewritten arrays to the same numbers
  (7,431 person-like names, 84 at a residential unit, 0.19%).
- **The committed outputs of all five cities were re-baselined** in one
  commit, since the renderer is shared. The all-city heat layer was kept: it
  would have saved another 2.0 MB but is a feature the other cities have.
  Further size work, if New York still loads slowly on the deploy, would have
  to reduce what is shown rather than how it is written.

### 2026-09-21 - New York added: the first city assembled from four registries

- **Step 0 disproved the plan's premise for this city.** `PLAN.md` and
  `docs/city_shortlist.md` both had New York down as "needs `nyc_dca` filled
  (Socrata `w7w3-xahh`, `business_category`)". Live verification showed DCWP's
  "Issued Licenses" file is a **regulated-activity licence list, not a business
  registry**: of 35,245 active premises licences, 13,385 (38%) are home
  improvement contractors, and the file contains zero restaurants, zero grocery
  stores, zero clothing shops, zero pharmacies and zero salons. New York City
  has no general business licence, so there is nothing for a
  one-registry pipeline to read. Built on DCA alone the map would have shown
  ~15k tobacco shops, secondhand dealers and electronics stores with two of the
  three legend buckets empty. The `nyc_dca` taxonomy skeleton was retired
  (removed from `TAXONOMY_MODULES`; it had never been used by a build).
- **Coverage is assembled from four public registries**, each authoritative for
  one bucket, live-verified the same day: DOHMH restaurant inspections
  (`43nn-pn8j`) for Food service; NYS Retail Food Stores (`9a8c-vfzj`) for
  grocery Retail; NYS Appearance Enhancement & Barber *business* licences
  (`y3u4-jbgh`) for Personal services; and DCWP premises licences for a narrow
  regulated Retail slice. Rejected alternatives: two registries only (drops
  Personal services entirely), and DCA alone (a misleading map of New York).
- **The architecture absorbed this without touching the shared map code.**
  `pipeline/taxonomies/new_york.py` dispatches `classify()` on a `source`
  column carried through `EXTRA_COLUMNS` - the same mechanism Chicago already
  used for `business_activity` - so `map_common.py` needed no change for
  multi-source. Category verdicts followed `chicago_license.py`'s stated
  standard (buckets track NAICS 44/45, 722, 812, so cities stay comparable)
  rather than fresh per-category judgment: that is what excluded pawnbrokers,
  appliance repair, car washes and hotels, each of which Chicago already
  excludes by name.
- **DCA's 8,854 active `Individual` licences are excluded wholesale** by
  filtering to `license_type='Premises'`. They are licences held by a person -
  sightseeing guides, locksmiths, pedicab drivers, process servers - not
  storefronts, and frequently at the licensee's home. Same reasoning as the
  national NAICS 454 exclusion. The three DCA adjunct categories (tobacco,
  e-cigarette, stoop line stand) are a permission a business holds rather than
  the business, so they are ranked last in the dedup and add a pin only where
  no other registry names that site - the treatment Chicago gives its own
  TOBACCO licence.
- **Lines, not services, and the legend obstacle forced it.** The feed carries
  29 routes, which are service patterns over ~11 physical lines. The label
  layout treats the legend as an obstacle `178 + 19*n_lines` px tall in a 650 px
  map, so 29 lines gives a 729 px obstacle - taller than the map, leaving no
  clear space, and every label collides. MTA's own `route_color` groups the 29
  into exactly the trunks it signs and prints, which is both the fix and the
  more honest geography (the 4, 5 and 6 are one line up Lexington Avenue).
  11 entries -> a 387 px obstacle, and all 11 labels placed without collision
  on the first render. Two deliberate departures from the colour grouping: the
  L is split from the three shuttles (MTA paints all four grey, but the
  14 St-Canarsie line is a full line), and the shuttles share one entry rather
  than three legend rows for 2, 4 and 5 stations.
- **One shared-code change**, generic rather than New York-specific: a line's
  geometry may now be several polylines under one label, colour and legend
  entry (`load_line_shapes` accepts a tuple of shape_ids and returns segments,
  longest first; the label anchors to the longest). A trunk is one line through
  the core and branches outside it. All four existing cities re-rendered
  **byte-identical**, which is how the change was verified non-breaking.
- **New York is the only city that does not use the shared ring edges.**
  Stations sit a median 482 m apart - almost exactly the 0.6 mi outer ring used
  elsewhere - so those rings would reach past the next two stations in every
  direction. Edges halved to `[0, 0.05, 0.1, 0.2, 0.3]` mi, which is what the
  add-city skill's "unless station spacing is meaningfully different" clause
  was written for. Stations were **not** thinned: unlike San Francisco's
  street-running Muni stops, every NYC subway station is a full station, so the
  sub-transit-line filters do not apply.
- **Rings start switched off here, rather than being removed.** Even halved,
  253 of 496 stations are closer together than the outer ring, and a rendered
  check showed the rings merging into an indistinct wash over Manhattan - but
  reading cleanly around the outer-borough and Staten Island stations. So
  `render_heatmap` gained a `rings_shown` flag (default True, False for New
  York) and the rings stay in the layer control. Preferred over dropping them,
  which would have lost real information for ~243 stations.
- **Staten Island Railway included**, on the condition that it be properly
  covered by data: it is, across all four registries (1,114 DOHMH
  establishments, 2,078 DCA premises licences, 654 salon licences, 520 retail
  food stores - more businesses than San Diego's entire mapped set), with 21
  clean GTFS stations and full shape geometry.
- **Two coordinate problems that looked like one.** 16,692 rows had source
  coordinates outside the city's bounding box, and the first pass wrongly sent
  all of them to the geocoder. They are two populations: 16,073 are valid New
  York State points that are simply not in the city (15,387 of them upstate
  salons in Watertown, Buffalo, Utica - the two NYS registries are statewide
  and carry no NYC marker), and 619 are not valid New York points at all, 409
  of them exactly (0,0), belonging to real New York businesses. The first are
  dropped as out of scope; only the second are geocoded. Conflating them would
  have wasted ~16k geocoder calls and risked placing an upstate salon back
  inside the city on a same-named street. `NY_STATE_BBOX` is the discriminator.
- **Cross-source dedup merges on address AND name, not address alone.** One
  New York address routinely holds many distinct storefronts, so address-only
  merging would delete real businesses; 14,830 rows share an address with
  another row. Keying on address plus a normalised name under-merges instead -
  a spelling difference between two registries leaves a business counted twice -
  which inflates density slightly rather than erasing storefronts. Both numbers
  are printed by step 2 so the trade-off stays visible, and the city page says
  so.
- **Counts.** 104,366 rows across four registries -> 84,331 storefront rows
  with a name -> 15,454 dropped as out of scope -> 64,092 after one-row-per-site
  -> 63,311 inside the borough polygons. Step 3 recovered 582 of 1,449 missing
  coordinates by Census geocoding (57.6% match rate on 1,390 geocodable rows,
  161 rejected as out of bounds, 57 more dropped as outside the boroughs) and
  lost 867 rows (1.4%), spread evenly across sources (0.3%-2.2%) and all three
  buckets - no systematic bias. Final: **62,444 businesses, 44,361 pins within
  a ring, 496 stations, 11 trunk lines, 24 shapes drawn.** Buckets: Food
  service 29,910, Retail 22,614, Personal services 10,787.
- **Exposure check: the cleanest large city so far, and the first where the
  measurement is real.** `scripts/check_personal_exposure.py` reports 84 pins
  (0.19%) with a person-like name at a residential unit, against Los Angeles
  5.67%, San Francisco 1.95%, Chicago 0.09%. Two reasons, both structural
  rather than lucky: **no registrant-name column is ever loaded** (the salon
  registry's `license_holder_name` is not even downloaded, and step 2 asserts
  it never arrives), so no pin can be one; and DCA supplies a **structured**
  `unit_type` (APT, STE, FL, RM as separate values), which is carried into the
  processed file as a `unit` column. That last point matters because San
  Diego's 0.04% was a measurement gap - its unit values are bare ("A", "101")
  with no token to match - whereas New York's number is measured. The 16.8%
  person-like-name rate sits at the documented false-positive floor and is
  concentrated in restaurants, coffee shops and grocers: the benign shape.
  The exposure script also now reports residential and commercial unit
  designators separately for every city, which revised the recorded figures
  slightly (Los Angeles 5.49% -> 5.67%, San Francisco 1.48% -> 1.95%) because
  FL/RM/PH/BSMT had not previously been counted as residential; the ranking is
  unchanged and the script's output is now the canonical measure.
- **Stated as a limitation on the city's page, not buried: New York's Retail
  bucket is less complete than the other cities'.** A clothing shop or bookshop
  needs no licence from any of the four registries and is therefore absent,
  while restaurants are close to fully covered because every one is inspected.
  The balance between categories here is a fact about New York's licensing, not
  about its high streets.
- **`docs/data_sources.md` created** as the master provenance list for all five
  cities - 8 business registries, 5 GTFS feeds, 5 boundary layers and the
  geocoder, each with its endpoint, download filter and retrieval date - and
  recording sources was added to the `add-city` skill. Two findings from
  writing it: `tqmj-j8zm`, the New York borough-boundary dataset ID in wide
  circulation, now returns 404 (`gthc-hcne` is live), and MTA's
  `web.mta.info/developers` GTFS path is dead (an S3 bucket replaced it). It
  also surfaced that **San Francisco's boundary layer has no recorded endpoint
  anywhere**, so that city cannot currently be rebuilt from scratch; logged as
  a gap in that file.

### 2026-09-21 - Legend stays broad; the exclusions page carries the detail

- **The map legends keep their broad labels** ("Retail - NAICS Code: 44/45",
  "Personal services - NAICS Code: 812") even though `454` and `81293` are now
  carved out of those prefixes. Precise labels were drafted and rejected as
  clutter on the map itself: "Retail - NAICS 44/45 (excl. 454 nonstore)" reads
  badly in a legend and would need re-editing every time a verdict changes.
- **`docs/excluded_categories.md` is the single place the detail lives**, and it
  is written to be published as prose. Surfacing it in the app (a page, or a
  link from each city page) is deliberately deferred - open in `PLAN.md`.
- **The gap this leaves, stated plainly:** until that page is surfaced in the
  app, a visitor reading the legend would infer the map covers all of NAICS
  44/45 and 812, which it no longer does. That is acceptable while the site is
  unpublished and is a blocker for the public deploy, not for development.

### 2026-09-21 - Nonstore retailers and parking excluded everywhere; solo massage in SF

- **A full sweep of every city's mapped categories found the remaining problem
  was definitional, not a privacy carve-out.** Ranking every classification by
  personal-name-plus-residential-address signal (rather than only checking the
  three codes already named) surfaced NAICS **454 "Nonstore retailers"** -
  electronic shopping, mail-order, direct selling, vending operators, fuel
  dealers. NAICS itself calls these nonstore; the `45` retail prefix in
  `NAICS_GROUPS` had been pulling in the whole family. They were 10.1% of Los
  Angeles's pins, 9.0% of San Diego's and 1.7% of San Francisco's, and `454390`
  (direct selling) was the largest remaining group of mapped personal names at
  residential addresses. Excluding it makes the project more correct about its
  own subject and removes the exposure as a side effect - an easier thing to
  justify than a privacy exception.
- **Two national exclusions, as `NAICS_EXCLUDE_PREFIXES` in `naics.py`, applied
  inside `naics_group()` so they win over `NAICS_GROUPS`:** `454` (above) and
  `81293` parking lots and garages. Parking was a **scope** call, not a privacy
  one (~4% residential): a parking trip is planned rather than incidental
  station foot traffic, so it sits outside this project's question. A sibling
  project had already excluded parking on the same reasoning, which the user
  confirmed. It was 888 pins in Los Angeles, 637 in San Francisco, 104 in San
  Diego.
- **San Francisco: 812990 excluded** (`NAICS_EXCLUDE_CODES` in its config, same
  printed-filter pattern as Los Angeles). Same code number as LA's exclusion but
  a different decision: San Francisco's licence data labels it "SOLO MASSAGE
  ESTABLISHMENT", not the generic "All Other Personal Services". 414 mapped
  pins, 31 (7%) with a person-like name at a residential address - the highest
  residential share of any category there, and a sensitive category (a sole
  operator working from home). Small share of the total, so the loss is marginal.
- **Counts after the rebuild.** San Diego 12,886 -> 11,270 available,
  2,971 -> 2,600 pins, map 1.0 -> 0.9 MB. San Francisco 20,067 -> 18,242
  available, 13,874 -> 12,625 pins, map 2.6 -> 2.4 MB. Los Angeles 70,168 ->
  61,208 available, 17,257 -> 14,632 pins, map 4.0 -> 3.5 MB (5.6 MB before any
  of this work, so the open map-size item is largely resolved). Chicago is
  untouched: it uses its own licence taxonomy. Los Angeles geocoding re-ran on
  4,594 addresses, 98.6% matched, 77 unrecovered (0.1%).
- **Exposure after:** person-like name at a residential address fell to 850
  (5.49% of mapped rows) in Los Angeles from 1,070, and to 201 (1.48%) in San
  Francisco from 249. Chicago 12 (0.09%) and San Diego 1 unchanged. The residual
  is now spread thinly across ordinary storefront categories (general
  merchandise, restaurants, beauty salons) rather than concentrated in one code,
  which is the shape expected from sole traders legitimately trading under their
  own names.
- **Two measurement corrections worth recording, because the first pass was
  wrong.** (1) The "looks like a person" regex flags 17-23% of pins in *every*
  city and *every* category, including full-service restaurants and taverns -
  that is the heuristic's false-positive floor (trade names that read like
  people), not exposure, and it must only be used intersected with a residential
  signal. (2) The residential test originally counted `STE`/`SUITE` alongside
  `APT`, which reported Los Angeles jewellery stores at 42% "residential"; they
  are downtown suites in the jewellery district. Splitting commercial from
  residential indicators dropped that category to 6% and moved the real offender
  to the top of the list.
- **San Diego, checked as asked and left in.** Its address text cannot carry the
  signal: `address_suite` is populated on 1,356 of 3,117 mapped rows but holds
  bare values ("A", "101") with no APT/STE token, so the 0.04% reading is a
  measurement gap, not a clean bill of health. Its better signal is
  `ownership_type`: 1,298 of 3,117 mapped rows are SOLE proprietorships, and 903
  (29%) display a name identical to the owner's. That is materially different
  from Los Angeles: San Diego's `dba_name` is never blank, so nothing was
  substituted by the pipeline - those owners chose to register their own name as
  the trading name, a deliberate public commercial act. Left in on that basis;
  revisit if a better residence signal appears.
- **`docs/excluded_categories.md`** now lists every exclusion, per city, in
  plain prose written to be published alongside the maps, including what is kept
  and why, the honest limits of the method, and an offer to remove a listing on
  the owner's request. Still open: the dataset licences and terms of use.

### 2026-09-21 - Privacy line: excluded NAICS 812990 in Los Angeles, and a standing exposure check

- **The principle, decided here and standing for every city: publish public
  commercial information, not personal information.** A trade name someone chose
  for their shop is commercial and deliberately public, and mapping it is the
  point of this project. A registrant's own name at what looks like their home is
  not, even when the registry that holds it is public. "It is in a public dataset"
  settles the licence question, not the publishing question: this project
  re-publishes the data in a new, more usable form (a searchable map pin at a
  precise coordinate), which is a different act from the registry's own listing.
  Where the two conflict, the map loses the row.
- **Why it came up.** A verification pass over the committed
  `outputs/<city>/heatmap.html` files (they are committed to a public repository
  and meant to be served publicly) measured what each pin actually exposes: a
  business NAME at a mapped COORDINATE. Los Angeles was the outlier. 68.1% of its
  raw rows carry no `dba_name`, so `step2_clean_businesses.py` fell back to the
  registry's `business_name` (the registrant) for 12,465 of 23,839 pins (52.3%);
  about 3,998 of those matched a conservative personal-name pattern, and 37% of
  the sampled rows had an APT/UNIT/STE/# in the street address. San Diego (0
  fallback pins), San Francisco (7) and Chicago (3) had no equivalent problem -
  their registries almost always carry a trade name.
- **The mechanism was already designed, and this is its first use.**
  `pipeline/taxonomies/naics.py` had recorded since the start that 812990 "All
  Other Personal Services" is a national catch-all, that a prior single-city
  hand-sample found **~90% non-storefront (home-based sole proprietors)**, that the
  verdict must be re-sampled per city, and that a city's verdict belongs in its
  own step 2. The privacy finding and that open data-quality item turned out to be
  the same rows: 812990 supplied 2,255 of the ~4,100 person-like pins. So one
  exclusion fixes both.
- **The change.** `NAICS_EXCLUDE_CODES = {"812990"}` in
  `pipeline/los_angeles/config.py`, applied as its own printed filter in that
  city's step 2 (visible in the run output, not hidden inside `classify()`), with
  the reasoning and sample recorded beside it and in `naics.py`. Scoped to Los
  Angeles: San Diego and San Francisco keep 812990 (unsampled; San Diego's codes
  are variable length, so a check there must match the `81299` prefix, not the
  6-digit code), and Chicago uses its own license taxonomy. Rejected as heavier
  than needed: dropping the registrant fallback everywhere (loses real storefronts
  whose registry simply has no dba), and removing names from tooltips entirely
  (guts the map's usefulness).
- **Effect, re-run 2026-09-21.** Step 2: 463,356 in-city rows -> 101,436
  storefront -> **70,257 after the exclusion (31,179 rows, 30.7%, removed)**.
  Geocoding: 5,986 addresses to recover (was 9,166), 5,910 matched (98.7%), 5,897
  inside the bounds, 89 unrecovered and dropped (0.1%; 0.2% among businesses
  started 2020 or later - the residual bias). Final: 70,168 rows available,
  **17,257 within-ring pins (was 23,839)**, map **4.0 MB (was 5.6 MB)**, which also
  reduces the open map-size item. Exposure: person-like pins traceable to the
  fallback **3,998 -> 1,803**; person-like pins overall **6,436 -> 3,948**; the
  APT/UNIT share of those 37.0% -> 33.9%. The other three cities are untouched and
  byte-identical (drift check re-run).
- **A standing check, not a one-off:** `scripts/check_personal_exposure.py` runs
  over any city's rendered map and reports the fallback-only pins (joined back to
  the raw trade-name column - the authoritative measure), the person-like names (a
  heuristic), their classifications, and how many sit at an address with a unit
  indicator. A new city must be added to its `REGISTRIES` table. It is wired into
  `add-city` and `CLAUDE.md` as a pre-publish gate. It deliberately prints numbers
  rather than a pass/fail: the judgment is per city and belongs in this log.
- **Honest limits of what was done.** The personal-name test is a regex heuristic:
  it flags "Jane Smith" and misses "J Smith Consulting", and it cannot tell a sole
  proprietor trading under their own name (a real storefront) from a registrant at
  home. The APT/UNIT indicator is a proxy for a residence, not proof. No row was
  individually verified against any other source, and no individual was contacted.
  The dataset licences and terms of use are **still unread** (open in `PLAN.md`) -
  this entry is about what is appropriate to publish, not about what the licences
  permit.
- **Left open, and now visible.** After the exclusion, Los Angeles's largest
  person-like group is NAICS **454390 "Other Direct Selling Establishments" (419
  pins)** - direct selling is inherently not a storefront and often home-based, so
  it is the obvious next candidate, along with the still-unsampled 812930 (parking)
  and 459999. San Francisco retains 113 person-like 812990 pins and a 14.7%
  unit-indicator share; San Diego 27 (`81299` prefix) and 0.1%. Chicago's
  person-like pins are trade names in storefront license types (Retail Food
  Establishment, Tavern) with a 0.8% unit share, which is the benign shape.

### 2026-09-21 - A "Cities" dropdown on each city map (closing the hop gap)

- **Added a city menu next to the "All cities" button on every city map, so a
  visitor can go straight from one city to another.** Decided with the user from
  the options laid out for the pilot's one recorded gap (two steps through the
  macro map to change city): a small dropdown, top-right, listing the other
  cities, keeping the map-only look. Alternatives not taken: previous/next arrows
  (an arbitrary order) and restoring the switcher on city pages (brings back the
  city links the pilot removes).
- **Built as a native `<select>`** in the shared renderer's control group
  (`THEME_TOGGLE_HTML`), so it is keyboard-accessible and uses the phone's own
  picker; a placeholder "Cities" is shown until one is chosen. It lists the
  other three cities and leaves out the current one, and it is hidden outside the
  app like the "All cities" button.
- **The city names come from the page, not the map.** The city page's hidden
  container (`map-only-nav`, renamed from `map-only-back-link`) now holds a link to
  the Overview and one per city, all generated from `app/cities.py`; the menu
  reads those links and clicks the chosen one, exactly as "All cities" does.
  Because the static map HTML does not embed the city list, **adding a city
  needs no map regenerated to appear in every menu**. The current city is worked
  out from the page URL (`/Chicago_Heatmap` -> Chicago), which relies on the
  `<Name>_Heatmap` page naming already used by every city and the scaffold. The
  menu is filled when the map loads, again after 0.8 s and 2.5 s (the page's links
  can render just after the frame), and when it is opened.
- **Light/dark travels with it**, as with the back button: the current mode is
  saved before navigating.
- **Layout.** The three controls form one right-aligned group that wraps and is
  capped to leave the zoom control clear (`max-width: calc(100% - 56px)`); at
  480 px or narrower the buttons are a little smaller.
- **Checked in a browser** (lean venv, clean tree). Chicago's menu lists San Diego,
  San Francisco and Los Angeles; the three controls sit side by side without
  overlapping (x 690-774, 782-878, 886-990 in a 1000 px frame). With Chicago in
  dark, choosing San Francisco opened it in place (the browser window object
  survived) and in dark, with a menu of the other three including Chicago; light
  from there to Los Angeles, then "All cities", stayed in place and in light. At
  375 px (343 px frame): one row at x 75-333, clear of the zoom control at
  x 10-44, no sideways scroll. All four standalone maps: no label problems, the
  menu hidden, no console errors. The closed dropdown is dark in dark mode (its
  computed colours and colour scheme); the open native list was not inspected.
- **A slip fixed on the way.** My first edit script updated the map renderer but
  aborted before the app page (a comment I matched had been wrapped differently),
  so for a moment the maps carried a menu with no links to read. Caught because
  I tested the running app before anything was committed; the page edit was then
  redone against the exact text.
- **Known gaps.** The open dropdown list is the browser's native one, so its look
  varies by browser (Opera GX, not tested, should match Chromium). If the app's
  page ever renders the hidden links late, the menu waits for them (2.5 s) and
  otherwise stays hidden. `deploy-verify` was not run.

### 2026-09-21 - Keep the Overview's fallback link list in the map-only pilot

- **Decided to keep the list of city links under the macro map for now.** It was
  the one open question from the map-only pilot (see the previous entry). The
  user viewed the running build (`8c59cb4`, `MAP_ONLY_NAV` on) and judged the
  list worth keeping. It stays the keyboard and screen-reader route to a city,
  and the route if the map fails to load.
- **Still open:** the pilot's overall go/no-go and whether visitors need a way to
  hop from one city to another without returning to the map. The list can be
  revisited (it is one block at the bottom of the Overview page) if the pilot
  is judged on how intuitive the map alone is.

### 2026-09-20 - "All cities" button and a map-only navigation pilot

- **Added an "All cities" button to every city map, and started a pilot that makes
  the macro map the only navigation.** The button (top-right, left of the Dark
  Mode button, in the shared renderer `pipeline/map_common.py`) takes a visitor
  back to the macro map. With it in place, the sidebar page list and the city
  switcher are hidden on every city page (`MAP_ONLY_NAV = True` in
  `app/cities.py`). Requested by the user, who wants to see whether a map-only
  site can work ("more novel"); the sidebar and city-link code is **kept** and
  documented in `docs/navigation_sidebar_and_city_links.md`, so reverting is one
  line.
- **How the button navigates.** The map is a sandboxed `st.iframe` (scripts and
  same-origin access allowed, top-level navigation not), so it cannot set the
  parent's location. It clicks the parent page's own link to the Overview, and
  Streamlit navigates in place. In map-only mode `render_city_nav()` therefore
  still renders that one link, inside a CSS-hidden `st.container(key=...)`; the
  sidebar is hidden with CSS rather than switched off in `config.toml`, so the
  link stays reachable and the change stays reversible from Python. The button
  shows only when the map is embedded (`window.parent !== window`), so a map
  opened on its own has no dead button.
- **The light/dark mode travels both ways.** The shared `localStorage` key
  already carried it; the button also saves the current mode before navigating.
  Checked: Dark on a city map, then "All cities", opens the macro map dark;
  from the dark macro map, a real click on the Chicago marker opens Chicago dark,
  Light there, then "All cities", opens the macro map light.
- **Kept: the Overview's fallback link list** (one link per city under the map).
  It is the keyboard and no-map route to a city (see the "Macro map and city
  navigation" entry). "Only keeping the main page" could also mean dropping it;
  that is left as an open question for the user rather than assumed.
- **Checked in a browser** (lean venv, clean tree). City page at 1024 px: sidebar
  hidden (`display: none`), no visible switcher, the two buttons side by side
  inside the map iframe with no overlap; navigating with the button left the
  browser window object intact (in-place, no reload) and the Overview showed the
  updated intro sentence. At 375 px: both buttons fit inside the 343 px frame
  (x 125-221 and 229-333), no sideways page scroll, sidebar hidden. All four
  standalone maps: `problems` empty, the back button hidden, no console errors.
  Not run: the independent `deploy-verify` agent (the user chose not to for now).
- **A slip fixed on the way:** the map-only CSS was first appended inside the
  existing indented Markdown block, where it rendered as a code block and hid
  nothing; it is now emitted in its own `st.markdown` call. And a JS regex in the
  button script used `\/` inside a non-raw Python string (an invalid escape
  warning); rewritten with string methods.
- **Known gaps.** A visitor arriving by URL sees only the map's button, with no
  way to hop city to city except through the macro map. The button does nothing
  if the hidden link was not rendered (the scaffold template includes the call).
  `deploy-verify`'s switcher check applies only when `MAP_ONLY_NAV` is False; its
  instructions now say what to check instead.

### 2026-09-20 - Migrated from st.components.v1.html to st.iframe

- **Replaced the deprecated `st.components.v1.html` with `st.iframe` in all four
  city pages, the macro map's Dark Mode script and the scaffold template.** The
  deploy-verify startup log had flagged that `components.v1.html` is deprecated
  in favor of `st.iframe` with a removal date (2026-06-01) already past; it still
  worked in Streamlit 1.64 and only logged a warning, but `requirements.txt` had
  no upper bound, so Streamlit Cloud installing a newer release could have removed
  it and broken every city page at deploy time. The dependency predated the Dark
  Mode work.
- **What `st.iframe` does, read from the installed source (1.64).** An HTML string
  or a `.html` `Path` is embedded as a same-origin iframe that allows scripts (the
  sandbox includes `allow-same-origin` and `allow-scripts`), read as UTF-8, and
  always scrollable. That is exactly what the pages needed, so each page now
  passes the map's `Path` (`st.iframe(HEATMAP_HTML, width=1000, height=650)`)
  and the manual `read_text(encoding="utf-8")` is gone. A fixed width is capped
  to the column, as before. The one difference: `st.iframe` rejects a height of 0,
  so the macro map's script-only frame is 1 px tall (it renders with a 1 px
  element container, no border).
- **Also added an upper bound: `streamlit>=1.64,<2`.** A cheap guard against a
  major release; it does not protect against a minor release removing an API
  (that is what the migration is for), so `deploy-verify` should still be run on
  each Streamlit upgrade.
- **A slip while migrating:** one script edit matched three pages but not San
  Diego's (its comments differ), so that page was briefly left calling the
  removed import; caught by grepping for leftovers before the first run and
  fixed by hand.
- **Checked in a browser** (lean venv, clean tree): all four city pages show the
  map in a 554x650 iframe (the column's width; fixed 1000 px map inside, as
  before), same-origin access holds, the maps and their Dark Mode buttons are
  present (line labels 5, 6, 6 and Chicago's page loads; no exception blocks);
  the macro map's button works from the 1 px iframe; Dark on the macro map opens
  Chicago dark, and Light on Chicago's map makes the macro map open light; the
  server log shows no deprecation warning on any page.

### 2026-09-20 - Dark Mode on the macro map

- **Added Dark Mode to the macro map, sharing the city maps' choice.** Decided
  with the user after a side-by-side comparison (real deck.gl renders of the
  four cities, opened in the browser pane): the button top-right, offset left of
  the zoom controls; a white pill behind each city name; and the same filtered
  basemap look as the city maps rather than Carto's native dark style.
  `components.render_macro_map_theme()` is called once from the Overview page.
- **Mechanism.** The pydeck chart is two canvases (`.mapboxgl-canvas`, the
  basemap, and `#deckgl-overlay`, the markers and labels), so the same dark
  filter is applied to the basemap canvas only, by page CSS scoped to the chart
  (`body.dark-base [data-testid="stDeckGlJsonChart"] ...`). A small script, run
  from a zero-height `components.html` iframe, adds the button to the chart's
  frame and toggles `dark-base` on the page `<body>`; a MutationObserver re-adds
  the button if Streamlit re-renders the chart. The choice is stored under the
  same `localStorage` key as the city maps (all are same-origin), so it works in
  both directions: verified that Dark on the macro map opens Chicago's map dark,
  and Light on Chicago's map makes the macro map open light. If the chart
  container is missing there is no button and the map stays light. It depends on
  Streamlit's `stDeckGlJsonChart` test id (stable in 1.64, an internal name), so
  re-check with `deploy-verify` on a Streamlit upgrade.
- **Findings from the comparison and testing.** A white halo around the labels
  (my first pick) smeared the letters at 14 px; the pill was crisp on both
  themes, so it was used, with slightly larger label offsets so pills do not
  touch their markers. Inverting only the zoom buttons' icon also inverted their
  background (the glyph is the button's own image), so the whole zoom group is
  inverted instead. At phone width the west-side "Los Angeles" pill was clipped,
  so the fitted view is padded 12% on the west. `components.py` is served
  stale by a running Streamlit after an edit (a known issue), so the server was
  restarted from a clean tree before each check.
- **Checked in a browser.** Desktop: the button is inside the frame with a 10 px
  gap to the zoom controls; clicking flips the class, label, `aria-pressed`,
  stored value, basemap filter and zoom styling, and does not touch the marker
  canvas; the choice survives a reload; a real marker click in dark mode still
  opens the city. Phone width (375 px): everything fits, no sideways scroll, all
  four names fully visible. No exception on the page.
- **Not done / limitations.** The surrounding Streamlit page stays light (deferred
  while a custom theme is considered). The page keeps the `dark-base` class on
  `<body>` after navigating to a city page (harmless: nothing there uses it) and
  resets it when the macro page loads again. Not tested: widths between 375 and
  1024 px, and the (i) attribution icon is only lightly restyled.

### 2026-09-20 - Dark Mode on the city maps (top-right button, persisted)

- **Added a Dark Mode toggle to every city map, through the shared renderer
  (`THEME_TOGGLE_HTML` in `pipeline/map_common.py`); all four maps
  regenerated.** Decided with the user: a separate top-right button (not the
  layer control), remembered between maps, city maps first. The macro map and
  the surrounding Streamlit page are not done (see below).
- **Why the button is `position: fixed`, not a Leaflet control.** The map is a
  fixed 1000 px wide (the Leaflet.heat init workaround) and Streamlit's content
  area is often narrower, which pushes anything anchored to the map's own
  corners off-screen. Measured in the running app: at 1024 px the iframe is 554
  px wide and Leaflet's top-right corner sits at x=1000, off-screen; a fixed
  element stays inside the visible frame, as the legend already does. At 375 px
  (iframe 343 px) the button spans x=293-333, visible. This is why an earlier
  sister project's top-right placement had been avoided.
- **Mechanism.** A `<button>` toggles a `dark-base` class on `<body>`; the
  choice is saved in `localStorage` under one key, so it carries from one city
  to another (the embedded map iframes share the app's origin; checked:
  opening San Francisco after choosing Dark on Chicago came up dark with no
  click, and switching back restored every style). Only the tile pane is
  filtered (`invert` plus `hue-rotate`, so water stays blue), so no second base
  layer and no new tile provider or key. Recoloured: legend, zoom and layer
  controls, attribution, tooltips, ring outlines (lightened), station dots
  (lightened), transit lines (brightened), line-name labels (brightened, with
  a dark halo) and the legend's line swatches. The palette is one CSS
  variable block, tinted toward the teal theme. The legend gained a
  `map-legend` class.
- **Checked in a browser.** In the embedded Chicago map at 1024 px: the button
  is visible in the narrow iframe; clicking flips the class, label,
  `aria-pressed`, stored value, legend, tiles, rings, station dots and the
  button itself. All four standalone maps pass `scripts/check_map_labels.js`
  in light mode (labels in view, no overlaps, none under the legend or the
  button); Chicago and Los Angeles were also viewed in dark; no console
  errors. Not viewed in dark: San Diego and San Francisco (same code).
- **Known limitations.** The Brown and Purple lines are brightened, not
  swapped for a dark-mode palette, so they read but are not ideal. The
  legend's category dots keep their light-mode colours. The toggle does not
  follow the operating system's dark preference (every visitor starts light
  until they choose). The button text is not translated or localized. The
  macro map (pydeck) and the Streamlit page stay light: the map's basemap has
  a `dark` style but the choice would have to be shared between Streamlit's
  Python state and the browser's `localStorage`, which needs its own design;
  the page chrome is deferred because a custom theme may replace it.
- **Verification script.** `scripts/check_map_labels.js` now also checks the
  button is in view, not over a label, and flips and restores the theme.

### 2026-09-20 - City scaffolding skill built

- **Built `scripts/scaffold_city.py` and the `scaffold-city` skill.** This was
  deferred until after Chicago so the shared fields could be chosen with a
  local-taxonomy city in hand (see "City scaffolding: threshold met, build
  deferred"). The script writes what is identical in every built city: the
  `pipeline/<slug>/` package with `config.py` and the map script, the
  `data/` and `outputs/` folders, the app page (next free number), and the
  `app/cities.py` entry. The projected CRS is derived from the marker longitude
  and its derivation written into the config (Dallas 32614, New York 32618,
  Boston 32619 in tests; Chicago's 32616 matches). Every value only the city's
  data can supply is a `TODO`, including the page prose and the blurb, and the
  map script refuses to run while `LINE_SHAPES` is empty, so a drawn line cannot
  lack a label and legend entry.
- **Custom taxonomies are handled three ways.** A NAICS city leaves the raw
  column as a `TODO`. A built local taxonomy is reused: the config takes its
  `VALUE_COLUMN` and, if it defines `EXTRA_COLUMNS`, notes that those columns
  must survive step 2. A new local taxonomy is scaffolded with `--new-taxonomy`
  as an empty, registered skeleton module. What Chicago showed to be
  taxonomy-specific rather than universal (a second classifying field,
  one-row-per-site with a license priority list, a dated snapshot of a term
  history) is written up in the skill as guidance, not generated.
- **Scope, as planned: not steps 1 and 2.** `step1_stations.py` and
  `step2_clean_businesses.py` differ per city (a spatial boundary filter,
  sub-transit-line filters, a cities-boundary join plus geocoding, per-site
  logic) and hold most of the effort, so the skill maps each situation to the
  built city to copy (San Diego, Los Angeles, San Francisco, Chicago) rather
  than generating a stub that would be mostly rewritten.
- **Shared `data/registry.yaml` still not built.** The scaffold delivers what
  the registry was for (one place a new city's shared fields come from) as
  generated files, so nothing needs a runtime loader; the deployed app must
  stay free of pipeline dependencies, and a loader would have meant rewriting
  four cities' configs. Revisit only if something has to read city settings at
  run time.
- **Tested against a scratch copy of the repo structure, not the real repo.**
  Dry run, real run and re-run (a first version created a duplicate page on
  re-run; fixed so an existing city's page is kept); a two-word name with
  `--map-step 4`; a reused local taxonomy with `EXTRA_COLUMNS`; a new
  taxonomy skeleton, importable and registered; an unknown taxonomy is
  refused; all generated files compile and every generated `config.py`
  imports; the map script exits with its message while `LINE_SHAPES` is empty.
  A dry run against the real repo for Chicago skips every existing file.
  Not tested: a full city built end to end from the scaffold (the next
  city build is that test).
- **Saving.** Expected to be modest, roughly 10% of a city's cost (an estimate,
  not measured); the next city build should record whether it held.

### 2026-09-20 - Macro map and switcher adjusted for a fourth, distant city

- **Adding Chicago broke the macro map on a phone and clipped the switcher; both
  fixed.** The `deploy-verify` run on the Chicago commit found: (1) at 375 px
  wide, San Francisco and Chicago fell outside the map, because the fitted
  view's zoom floor (3.0) was tighter than the 2.3 that Chicago plus California
  need; (2) at the fitted zoom the Los Angeles and San Diego markers, about 180
  km apart, touched, and their names collided; (3) at 1024 px wide the city
  switcher's fixed columns clipped "San Francisco" and "Los Angeles".
- **Changes.** The zoom floor is now 1.0 and the fit assumes a 320 px canvas.
  Markers shrank from radius 11 to 6 pixels. Each city may set an optional
  `label` side in `app/cities.py` ("top" by default; San Diego "right", Los
  Angeles "left"), so the three California names read cleanly. The switcher is
  a wrapping horizontal container (`st.container(horizontal=True)`, available
  in the minimum Streamlit, 1.64) instead of fixed columns, so a long name
  wraps to a second line instead of being cut.
- **Checked in a browser** (lean venv): all four cities visible and named on
  desktop and at 375 px; real clicks on the San Diego, San Francisco, Los
  Angeles and Chicago markers each open their own page; no switcher item clipped
  at 1024 px (Chicago wraps to a second line).
- **Known limitation.** On a phone-width map the Los Angeles and San Diego dots
  still touch (about 7 px apart), so tapping the right one is fiddly; the
  fallback link list below the map is the reliable route. Grouping nearby
  cities on the macro map (already in `PLAN.md` under "Later") would remove it.
  The dark theme and widths between 375 and 1024 px were not tested.

### 2026-09-20 - Chicago built

- **Added Chicago: the CTA 'L', City of Chicago stations only, on the city's
  own license taxonomy.** Pipeline `pipeline/chicago/` (config, step 1
  stations, step 2 clean businesses, step 3 map), page `app/pages/
  4_Chicago_Heatmap.py`, `app/cities.py` entry, and `outputs/chicago/`.
  Verified in a browser: 7 line labels in view with none overlapping, legend
  collapses, no console errors. Baseline counts, run 2026-09-20 against the
  raw snapshot taken that day:
  - Step 1: 141 stations across the seven lines; 123 in the city, 18
    suburban stops excluded (Austin, Cicero, Davis, Dempster, Forest Park,
    Foster, both Harlems, Central, Linden, Main, Noyes, both Oak Parks,
    Ridgeland, Rosemont, South Boulevard, 54th/Cermak), listed in
    `excluded_stations.csv` as "Outside Chicago city limits" (the boundary
    layer holds Chicago only, so the suburb is not named). In-city stations
    per line: Red 33, Brown 26, Blue 28, Green 27, Pink 19, Purple 17, Orange
    15. Spacing: median nearest-neighbour distance 740 m, 10th percentile 284
    m, minimum 137 m; 11 stations are within 250 m of another (the Loop area).
  - Step 2: 53,039 active rows (server-filtered, snapshot 2026-09-20) ->
    49,066 with `city = CHICAGO` -> 24,612 storefront -> 24,504 with
    coordinates (108 without, none of them redacted) -> 24,504 inside the
    bounding box -> 20,686 after one row per site. Boundary cross-check:
    20,671 of the 20,686 fall inside the Chicago polygon (15 outside, kept).
    Buckets: Retail 10,321, Food service 6,573, Personal services 3,792.
  - Step 3: 123 stations; 11,796 businesses within a ring, 8,890 beyond; map
    file about 3.0 MB.
- **Transit scope, as decided: CTA only, Metra deferred** (see the "Chicago
  transit scope" entry). Yellow Line dropped, following the chopping-block
  rule: it has 3 stations and its only in-city one, Howard, is also served by
  Red and Purple.
- **Corrections to the earlier expectations, from the GTFS.** Purple is not a
  near-empty line: it has 17 in-city stations (its rush-hour Loop express runs
  on Brown's stations). But its most-used trip shapes are the Linden-Howard
  stub in Evanston (1% inside the city), so the drawn shape is the Loop-express
  shape (shape 309200024, 58 trips, 40% inside), the only one reaching the
  city; it overlaps Red and Brown between Howard and the Loop. Every other
  line uses its single most-used shape. The feed has 143 parent stations
  against CTA's stated 145. There are only 55 active license descriptions,
  not the 150 in the full history.
- **'L' shape: uniformly sparse, so no spacing filter,** as expected. The
  Loop and Loop subway are the exception: Jackson and Monroe each have a Blue
  and a Red station about 140 m apart, and LaSalle and LaSalle/Van Buren are
  137 m apart. CTA counts them as separate stations and they were kept as CTA
  counts them; their rings overlap, a conscious choice (each business is
  assigned to its nearest station, so nothing is double-counted). A station
  is a GTFS parent station, so no name-alias list was needed.
- **Full license mapping** (approved before writing; `pipeline/taxonomies/
  chicago_license.py`, 21 test cases pass). Direct: Tavern is Food service;
  Package Goods, Filling Station, Secondhand Dealer and Tobacco are Retail.
  By business activity: Limited and Regulated Business License (rules in the
  "catch-all license types" entry); Retail Food Establishment (11,100 active
  rows) is Food service when any part prepares or serves food (6,295) and
  Retail otherwise (4,802), and the 949 mixed rows (a grocery with a deli) go
  to Food service, a rule that does not depend on the order the city lists
  activities; Animal Care License (395) is Personal services for grooming and
  Retail for retail sales, with veterinary hospitals, boarding and shelters
  excluded. Excluded outright: the adjunct licenses Consumption on Premises
  (2,820 rows), Outdoor Patio (731), Late Hour (119) and Music and Dance (46),
  because they attach to a business already counted (only 110, 15, 3 and 3
  sites respectively have no primary license, a trivial loss); Motor Vehicle
  Services (1,536, body and repair shops) and Commercial Garage (581, parking
  operators); and Pawnbroker, Pop-Up Retail User, shared kitchens, mobile and
  event food, Peddler, Public Place of Amusement, Children's Services,
  Manufacturing, Wholesale Food, Raffles, Valet, Shared Housing and the
  remaining long tail.
- **One row per site, primary license first.** A site (account number plus
  site number) can hold several licenses, so after classification the rows
  are reduced to one per site, taking the license earliest in
  `LICENSE_PRIORITY` (Retail Food Establishment, Tavern, Limited, Regulated,
  Package Goods, Filling Station, Secondhand Dealer, Tobacco). This collapsed
  24,504 rows to 20,686. Tobacco therefore counts only where a site has no
  primary license: 222 sites, real smoke shops and dollar stores.
- **No geocoding step.** Coordinates are valid (all 48,614 active in-city rows
  with coordinates were inside the bounding box, unlike Los Angeles), and 108
  storefront rows (0.4%) have none; their addresses are not redacted. That
  loss is small, but its bias was not analyzed (by start year, category or
  area), so the loss is recorded as a known limitation and not dismissed. If
  it matters later, add a Census-geocoding step as Los Angeles did.
- **Shared-code change.** `pipeline/map_common.py` now passes a taxonomy's
  `EXTRA_COLUMNS` to `classify()` when grouping pins by category, as
  `filter_to_storefront()` already did; without it Chicago's activity-classified
  rows would have matched no bucket. Drift check on San Diego, San Francisco
  and Los Angeles: zero drift.
- **Known limitations.** The `raw` file is a dated snapshot (`AS_OF_DATE` in
  config), and re-downloading it changes the counts. Chicago's Retail and Food
  service buckets come from local license types and activity text, so they
  are comparable to the NAICS cities' 44/45 and 722 only approximately; the
  mixed grocery-with-deli rule and the exclusion of gyms and fitness (NAICS
  713940 and 611620 are outside the three buckets) are the main judgment
  calls. Home-based businesses are excluded as not being storefronts. Tooltips
  show the license type ("Retail Food Establishment"), not the activity.

### 2026-09-19 - Pin line endings with .gitattributes

- **Added `.gitattributes` (`* text=auto eol=lf`) to stop the recurring
  "LF will be replaced by CRLF" warnings.** The repository already stores LF
  in every tracked file; the warnings came from `core.autocrlf=true` on the
  Windows machine converting to CRLF in the working copy (37 tracked files
  were CRLF on disk). Pinning LF removes the mismatch without changing what
  is committed. Checked: `git status` showed only the new file, and the drift
  check across the three cities still shows zero drift (it already normalizes
  CRLF to LF at byte level, so it was unaffected either way). Git config was
  not touched.

### 2026-09-19 - Chicago transit scope: CTA only, Metra deferred

- **The first Chicago build maps the CTA 'L' only; Metra is recorded as a
  possible later addition.** Each built city maps one agency's rail-transit
  system (the San Diego Trolley without the Coaster or Sprinter, Muni Metro
  without Caltrain or BART, LA Metro Rail without Metrolink), and Metra would
  break that. It would also add a second agency and feed, 11 more lines (about
  19 in the legend and label layout), low-frequency and rush-hour-only
  stations, and Metra Electric's closely spaced South Side stops, which could
  reopen the spacing-filter question. The extra effort was estimated at
  roughly 40-50% (a guess).
- **Expected 'L' shape (from general knowledge, not yet checked against the
  GTFS): uniformly sparse, so no San Francisco-style spacing filter.** All
  lines are grade-separated with stops roughly a half to a mile apart and no
  street-level streetcar offshoots. Instead, five lines share the downtown
  Loop (their polylines overlap and the station rings overlap heavily there),
  and the Purple and Yellow lines run mostly outside Chicago (Evanston,
  Wilmette, Skokie), as do stops on Green, Pink and Blue (Oak Park, Cicero,
  Forest Park). To be verified in the build by computing stop spacing per
  line and counting stations inside the city boundary.
- **Chopping-block order if the map is too much:** Yellow and possibly Purple
  first (a line with essentially no in-city stations is dropped rather than
  drawn, since every drawn line needs a label and a legend entry), then
  suburban stops (removed automatically by the boundary filter). The core six
  lines (Red, Blue, Brown, Green, Orange, Pink) stay.

### 2026-09-19 - Chicago catch-all license types classified by activity

- **Classified Chicago's two catch-all license types by `business_activity`,
  in `pipeline/taxonomies/chicago_license.py`.** "Limited Business License"
  and "Regulated Business License" (about 39% of active licenses) say nothing
  about the business, so they use the activity text. Rules, approved before
  writing: Retail = retail sales activities (general merchandise, clothing,
  jewelry, cell phones, flowers, furniture, art, vehicle parts, funeral items)
  plus vehicle sales; Personal services = hair, nail, skincare, waxing, massage,
  tattoo, laundromat, dry-cleaning drop-off, clothing alterations and
  "Miscellaneous Personal Services". The buckets follow what the `naics`
  taxonomy counts (44/45 and 812), so cities stay comparable. A multi-activity
  value (parts joined by " | ") takes the first part that matches a bucket.
- **Exclusions and the calls behind them.** Anything marked "(Home Based
  Business)" is excluded (not a storefront). A catch-all row with no activity
  (2,678 rows) is excluded: nothing shows what it is. Gyms, yoga and fitness
  classes are excluded because NAICS puts them outside the three buckets
  (713940, 611620), though they are visible storefronts. Also excluded:
  administrative and financial offices, consulting, tax preparation,
  wholesale, staffing, travel, shipping and printing, car washes, hotels and
  vacation rentals, hazardous-materials storage, scavenger vehicles, and
  "Miscellaneous Commercial Services". The activity rules apply to both
  catch-alls, so the Regulated bucket keeps its few storefront services
  (massage, tattoo, laundromat, alterations) instead of being dropped whole.
- **Checked against live data.** Applied to the 20,727 active Chicago
  catch-all rows with coordinates (pulled 2026-09-19): 3,739 Personal
  services, 5,104 Retail, 11,884 excluded (Limited: 2,916 / 4,837 / 7,419;
  Regulated: 823 / 267 / 4,465). The largest excluded activities were the
  null activity, administrative offices (1,098), "Miscellaneous Commercial
  Services" (721), home-based businesses, and tax preparation (309), as
  intended. Nine spot cases (multi-activity, null, home-based, health club)
  all classified as expected.
- **The taxonomy is still incomplete.** The other ~148 `license_description`
  values (Retail Food Establishment, Tavern, Tobacco, Package Goods and the
  rest) are unmapped and still need their own mapping before Chicago is built.
  Revisit as part of the Chicago build.
- **Shared-code change.** `filter_to_storefront()` now also passes any
  columns a taxonomy lists in an optional `EXTRA_COLUMNS` attribute to
  `classify()`, because Chicago's rule needs two fields; single-column
  taxonomies (`naics`) are unaffected. Drift check across San Diego, San
  Francisco and Los Angeles: zero drift.

### 2026-09-19 - Chicago Step 0 probe (schema and counts only; no pipeline code)

- **Ran the Step 0 live check on Chicago's Business Licenses (Socrata
  `r5kz-chrr`, `data.cityofchicago.org`), capped at schema, null rates and
  category counts, to lower the cost of the build.** Nothing was built.
- **The dataset is every license term since 2002, not a current registry.**
  1,207,156 rows, `date_issued` 2002-01-02 to 2026-09-18, and
  `expiration_date` values that include junk (year 0206 and 9999). Of those,
  1,126,817 have status `AAI` (issued). Filtering to status `AAI` with
  `expiration_date` on or after 2026-09-19 leaves 53,043 rows; with
  `city = 'CHICAGO'` and coordinates present, 48,617. Those 53,043-row
  filters were checked with counts only; the expiration junk still has to be
  handled in the real filter. One account can hold several licenses at a
  site (32,875 distinct active accounts in the city against 48,617 rows),
  so the build must dedupe by account and site, as the earlier cities
  deduped.
- **Coordinates and city.** 93,098 of the 1,207,156 rows (about 8%) have a
  null `latitude`. 1,116,247 rows say `CHICAGO`; the rest are suburbs
  (Cicero, Skokie, Des Plaines and others), so the `city` field is usable
  as a first filter. Addresses are redacted (`[REDACTED FOR PRIVACY]`) on
  2,417 active Chicago rows (home-based licenses). Not yet checked, per the
  Los Angeles lesson: whether coordinates are corrupt (bounding-box test)
  and whether any in-city rows carry a different `city` value.
- **Classification is the hard part, and it is smaller than feared but
  trickier.** There are 150 distinct `license_description` values and 4,120
  distinct `business_activity` values. The biggest active buckets are
  "Limited Business License" (15,245), "Retail Food Establishment" (11,150),
  "Regulated Business License" (5,573), "Consumption on Premises - Incidental
  Activity" (2,845), "Tobacco" (1,834), and "Motor Vehicle Services License"
  (1,537). "Limited Business License" and "Regulated Business License" are
  catch-alls, together about 39% of active rows, so `license_description`
  alone would misclassify the largest groups; the `chicago_license`
  mapping will need `business_activity` for those two, with a hand-sample.
  Many other descriptions (Peddler, Raffles, Valet Parking Operator,
  Pharmaceutical Representative, Shared Housing Unit Operator) are not
  storefronts and will be excluded.
- **Transit data.** CTA's GTFS downloads (HTTP 200, 68.7 MB). Metra's feed
  did not respond at `gtfs.metrarail.com` but downloads at
  `schedules.metrarail.com/gtfs/schedule.zip` (HTTP 200, 705 KB); it was not
  opened. Whether to include Metra, and whether the 'L' (145 stations, 8
  lines) has a central-plus-offshoot shape, are still decisions for the
  build. The city boundary is Socrata "Boundaries - City - Map" (`ewy2-6yfk`),
  not yet downloaded or checked.
- **Not done:** the `chicago_license` mapping, any pipeline code, station
  selection, and the coordinate-quality check.

### 2026-09-18 - City scaffolding: threshold met, build deferred

- **The rule-of-three condition for a shared config loader is met, but the
  scaffold is deferred until after the first non-NAICS city (Chicago).** The
  earlier deferral in `PLAN.md` was "until more than two cities show the
  common shape"; three cities now exist. Comparing them: `config.py`, the
  map script and the app wiring share a shape (paths, CRS, rings, taxonomy
  name, thin call into `render_heatmap()`, a `cities.py` entry and page),
  while `step1_stations.py` (spatial filter, sub-line spacing filter, or
  cities-boundary join plus Census geocoding) and `step2_clean_businesses.py`
  differ per city and hold most of the per-city effort.
- **Why wait rather than build now.** All three built cities have GTFS and
  NAICS, so the shared fields were drawn from cases that resemble each
  other; Chicago is the first with a local taxonomy and possibly commuter
  rail, and would show which config fields are truly universal. Building it
  also needed budget that was not available in the session. Expected saving
  is modest, roughly 10% of a city's cost (an estimate, not measured), so it
  is medium priority. Scope is config, the map script and app wiring only,
  not steps 1 and 2.

### 2026-09-18 - San Diego excluded-stations audit file

- **San Diego now writes `outputs/san_diego/excluded_stations.csv`, as San
  Francisco and Los Angeles already did.** It lists the 16 Trolley stations
  outside city limits with the municipality each is in (La Mesa 5, Chula
  Vista 3, El Cajon 3, Lemon Grove 2, National City 2, Santee 1). The city
  filter now joins against every municipality in the SANDAG layer once, so
  the same join both keeps San Diego and labels the excluded stations; the
  kept set is unchanged (47 of 63). Drift check: only the new file differs.
  The file has the same columns as Los Angeles's (`station`, `latitude`,
  `longitude`, `located_in`).

### 2026-09-18 - Live check of Dallas, Austin, Charlotte and Fort Worth

- **Checked the four cities left "not yet live-verified" against their real
  APIs, to widen the pool beyond the ranked list.** Search summaries were not
  treated as evidence (the Denver and San Jose lesson); schemas, counts,
  date ranges and null rates were pulled directly.
- **Dallas: marginal, kept as an unranked candidate.** Certificates of
  Occupancy (Socrata `9qet-qt9e`) has a real classification (`land_use`, 143
  values, plus an `occupancy` code), business names, and coordinates (2 of
  23,731 rows null), and DART's GTFS downloads. But the data ends 2022-11-15
  and covers only certificates issued 2018-2022, so it shows new occupancies,
  not a registry; a city page would have to say so. This corrects the earlier
  search-level note that the dataset lacked a classification field. Its
  effort rank sits after Boston (needs a new taxonomy module) and would be
  set when it is built.
- **Fort Worth: ruled out on rail, though the data is workable.** The
  certificate table (72,065 rows since ~2002, `JobUse` with 48 values,
  coordinates, current through 2026) has ~19% of rows without coordinates,
  null city and address fields on most rows, and repeats a business when it
  relocates. With only TEXRail and the Trinity Railway Express, the map would
  have few stations. Revisit if rail expands.
- **Austin: ruled out.** The dataset named "Certificates Of Occupancy" is
  291,759 construction permits with a yes/no flag and no business name or
  classification; the business datasets found are small (64-row credit-access
  list, vendor lists). One MetroRail line.
- **Charlotte: ruled out.** The city hub has no business or license dataset
  (zoning, permit-review, and hand-curated grocery/pharmacy/medical points
  only), and Mecklenburg County's GIS page listed none. Rail is small.
- **Not checked:** Dallas's Commercial Permits Activity Dashboard
  (`ync5-xnfn`), and Trinity Metro, Austin and Charlotte GTFS. The Austin and
  Charlotte rail sizes are from memory.

### 2026-09-18 - Line labels at tail ends, auto-fitted view, collapsible legend

- **Line labels now sit at each line's tail end, chosen automatically.** The
  end used is the one farthest from every other line, measured on the stretch
  inside the city (`label_focus`, now passed by all three cities). This
  replaced the per-line degree offsets (San Diego's Silver Line at 0.016, Los
  Angeles's D Line at -0.012), which had been hand-tuned against one rendering
  each and could not be reused for a new city. The label is offset in pixels
  by its own box size along the line's outward direction, so it clears the
  line at any angle and stays put at any zoom. The line spec's fourth element
  changed from an offset to a label end (`None` = automatic, or `"start"` /
  `"end"` to force).
- **Labels that would land on the same spot disperse along their lines.**
  The first version put Muni's J Church, K Ingleside and M Ocean View at the
  same south end, where they overlapped. A layout pass now tries, per label,
  the tail tip pointing out (and swung up to 80 degrees either way), then
  spots further along the line from that tail with the label beside the line,
  taking the first that clears the other labels, the open legend, the map
  controls and the map edge. Longest names are placed first.
- **The default view is now fitted rather than hand-picked.** The same layout
  pass picks centre and zoom to show every station and every label, zooming
  out in quarter steps and shifting away from the legend only if labels
  cannot otherwise be separated. Hand-picked centre/zoom constants were
  removed from the three city scripts; `center`/`zoom` can still be passed to
  override. Checked on all three maps in a browser: no line label overlaps
  another, hides under the legend, or falls out of view (labels do draw over
  cluster badges by design).
- **The legend is collapsible.** It is a native `<details open>`, so it
  starts open, collapses to a small "Legend" tab with a click, and needs no
  script. Rejected: a custom JavaScript toggle (more code, no benefit).

### 2026-09-18 - Macro map and city navigation

- **Built the macro map: the Overview is now a clickable map of every mapped
  city, and clicking a marker opens that city's page.** This is the
  area-selector macro level of the hybrid architecture (see the "Project
  origin" entry), built now that three cities exist. It uses `st.pydeck_chart`
  with `on_select="rerun"` and `st.switch_page`. pydeck ships with Streamlit,
  so it adds no dependency and keeps folium out of the deployed runtime, the
  same constraint that ruled out `streamlit-folium`. Rejected alternatives:
  a pre-rendered static folium map with links (a click would have to
  navigate the parent page from inside the sandboxed iframe, causing a full
  reload and losing the session) and keeping the plain `st.map` (no
  click-to-navigate). Markers have permanent name labels, a hover tooltip
  with the city's line names, and a plain list of page links below the map as
  a fallback (keyboard access, or if the map fails to load).
- **Added a city switcher to every city page** (`components.render_city_nav`):
  a link back to the map, then every city, with the current one shown as
  plain bold text, so a visitor can hop city to city without returning to
  the map. On a phone-width screen the row stacks vertically.
- **Moved the city list to `app/cities.py`, one source for the map, the
  fallback list and every switcher.** It had been inline on the Overview
  page; with the switcher it had three consumers. Adding a city now means
  one entry there plus its page. It stays app-side and tiny on purpose: the
  fuller per-city registry (map centre, CRS, taxonomy, data sources) is still
  open in `PLAN.md` and would live with the pipeline, since the deployed app
  must not depend on pipeline code.
- **Fixed three real bugs found by looking at the running map, not by
  reading the code.** (1) pydeck serialized `radius_units="pixels"` as the
  expression `"@@=pixels"` (an undefined variable), so markers rendered as a
  wrong-sized fill across the map; passing `pdk.types.String("pixels")`
  fixes it (the same applies to the label font). (2) pydeck's `compute_view`
  chose a zoom that cropped San Diego and San Francisco out of the same view;
  replaced with a small Web-Mercator fit (`fit_view`) that works for any
  number of cities, and corrected it once for 512 px world tiles (the first
  version was one zoom level too tight). (3) On a 375 px viewport the map
  cropped the outer cities and the fallback links were clipped; the fit is now
  sized for a phone width and city descriptions are wrapping captions.
- **Raised the tested minimum to `streamlit>=1.64`.** Click selection and
  `switch_page` exist in 1.40 (checked in a clean venv), but 1.40 needs the
  now-deprecated `use_container_width` for full width, which Streamlit
  warns will be removed; 1.64 defaults to full width, so the argument is
  dropped instead.
- **Verified against the lean venv, desktop and phone width.** A real click
  on the San Diego marker navigated to its page; the switcher moved San Diego
  to Los Angeles; the map link returned to the Overview and stayed there over
  8 seconds with an empty selection (no bounce back from a stale click); no
  sideways scroll at 375 px. Two earlier failed click attempts were my own
  pixel-mapping errors (the screenshot is scaled relative to the page), not
  app bugs: a synthetic hover at the computed position showed the correct
  tooltip.
- **Basemap: Carto's public vector style (`positron`) for the macro map.**
  pydeck's default style needs a Mapbox token. This adds Carto's tile
  service to the tile-provider decision already open in `PLAN.md` (the
  per-city maps use OpenStreetMap's raster tiles).

### 2026-09-18 - Remote

- **Pointed the repository at https://github.com/dacekroberts/expanded-heatmap
  (`origin`) and pushed all seven existing commits on `master`.** The
  remote was empty, so nothing was overwritten. This confirms the GitHub
  account behind the commit identity (`dacekroberts`, noreply address)
  chosen earlier; the branch was kept as `master` rather than renamed to
  `main`. Future commits go to this remote.

### 2026-09-18 - Los Angeles (third city)

- **Added Los Angeles: 565,498 raw rows with coordinates -> 463,356 in-city
  -> 101,436 storefront -> 92,270 with usable coordinates + 9,166 flagged
  -> 9,039 recovered by geocoding -> 101,309 final (127 dropped); 56
  stations; 23,839 of 101,309 businesses within a ring.** Source: LA Office
  of Finance "Listing of Active Businesses" (Socrata `6rrh-rzua`,
  `data.lacity.org`), downloaded server-filtered to rows with coordinates
  and only the columns step 2 uses, ordered by `location_account` so the
  file is reproducible (the full dataset is 631,925 rows). About 9% of rows
  carry no NAICS code and so are excluded from the storefront filter - a
  floor on density, like San Francisco's.
- **Found that ~9% of in-city storefront rows have corrupt coordinates,
  that the loss is heavily biased toward recent registrations, and
  recovered nearly all of them by geocoding instead of dropping them.** The
  first version of step 2 dropped everything outside the city's coordinate
  bounds and lost 9,166 of 101,436 rows (9.0%) - too many to accept
  unexamined. They were: 8,657 rows whose longitude is a copy of the
  latitude (e.g. 34.0468, 34.0468), 470 at (0, 0) or whole-degree
  placeholders, and 39 elsewhere outside the city. The loss is even across
  council districts (8.2-9.9%) and moderately uneven across categories
  (Retail 8.4%, Personal services 9.0%, Food service 11.4%), but very
  uneven by age: 22.5% of businesses that started in 2020 or later were
  affected versus 0.7-1.5% of older ones, so dropping them would have
  systematically under-counted new openings. Each row still has a street
  address, so step 2 now flags them (`coord_status = needs_geocode`,
  coordinates blanked) and a new step 3 geocodes them with the Census
  bulk geocoder: 9,066 of 9,166 matched (98.9%; 4,869 exact, 4,197
  non-exact), 27 rejected for landing outside the city's bounds, and 99.5%
  of the 9,039 accepted points fall inside the City of LA polygon.
  Residual loss is 127 rows (0.1%), 80 of them among the 37,066 businesses
  started 2020+ (0.2%). Every output row records its source
  (`geocode_source` = source | census). Rejected alternative: keep dropping
  them and document the bias - a 9% loss concentrated in new businesses is
  too large and too systematic to leave in.
- **Identified in-city businesses by `council_district` 1-15, not by the
  `city` field.** `city` holds postal community names (Van Nuys, North
  Hollywood, San Pedro, ...), all part of the City of LA; only 295,738 of
  631,925 rows say "LOS ANGELES", so an exact match would have kept about
  half the city. `council_district` is the city's own field: 1-15 are the
  council districts and 0 (151,427 rows) marks businesses registered with
  LA but located elsewhere. Independent check against the boundary
  polygon: 99.9% (92,169 of 92,270) of source-coordinate points fall inside.
- **Inserted geocoding as step 3, making the map step 4, and built
  `pipeline/census_geocoder.py` as a shared module.** This is the renumbering
  the `add-city` skill describes; `drift_check.py` needed no change. The
  module caches Census responses under `data/<city>/raw/geocode_cache/`
  keyed by a hash of each batch's contents (not just the batch number), so a
  changed input can never be served a stale answer and re-runs (and drift
  checks) stay deterministic and off the network. `requests` returned to
  `requirements-pipeline.txt`. First tested on 200 rows (95% matched)
  before the full run.
- **Kept every in-city station; the sub-transit-line filters were not
  needed.** Median spacing between in-city stations is ~0.55 mi with no
  dense street-running offshoots (unlike Muni Metro), measured before
  collapsing duplicate complex names.
- **Scoped to the City of LA: 56 of 110 stations kept, 54 excluded across 23
  other places.** Metro Rail serves Long Beach (8 stations), Pasadena (6),
  El Segundo, Hawthorne, Inglewood and Santa Monica (3 each), Azusa and
  Compton (2 each), 15 more cities with 1 each, and 10 stations in
  unincorporated areas. Covering them would need those cities' own business
  registries, sourced and verified separately - a new project, not a
  config change. All 54 are listed with the city they are in in
  `outputs/los_angeles/excluded_stations.csv`. Four per-line complex names
  (8 feed names) were collapsed into single stations after a pairwise
  distance check (Metro Center, Union Station, Expo/Crenshaw,
  Willowbrook/Rosa Parks): 114 feed names -> 110 stations.
- **Used LA County Planning's incorporated-city boundary layer and Metro's
  own rail GTFS.** The City of LA's own boundary service (`maps.lacity.org`)
  was unreachable from this environment (connection failure, other hosts
  fine), so the county layer on `services.arcgis.com` (88 incorporated
  cities, LA = the `LOS ANGELES` record) was used; it also let step 1 name
  the city of every excluded station. The GTFS is Metro's official
  rail-only feed (gitlab.com/LACMTA/gtfs_rail), current as of this run
  (calendar to 2026-10-02; includes the 2026 D Line extension shape).
- **Named lines by Metro's letters (A, B, C, D, E, K Line) and used Metro's
  official colours from the feed's `route_color`.** Names verified against
  Metro's own line-letters post and Wikipedia; the feed's "Metro A Line" has
  the brand prefix dropped, as San Diego's "Blue Line" lacks "MTS". Unlike
  San Francisco's, LA's official colours are unambiguous, so they are used.
- **Fixed line labels being hidden under big cluster badges, in the shared
  code.** Downtown LA's clusters (3,796 and 5,222 businesses) were drawn over
  the B and D Line labels, defeating a "permanent" label; San Diego's Silver
  Line had hit the same problem earlier and was worked around with a larger
  offset. Root-cause fix: label markers get `zIndexOffset=1000` in
  `map_common.add_line_label`. San Diego and San Francisco were regenerated
  (only the z-index and Folium IDs changed).
- **Added `label_focus` to `render_heatmap` so labels anchor on the in-city
  stretch of each line.** LA's lines run far beyond the city (the A Line to
  Azusa and Long Beach), so the midpoint of the whole route would fall
  off-screen in the default view. Other cities pass nothing and are
  unchanged. The B and D Lines share a subway corridor, so their labels
  landed 9 px apart; the D Line's label takes a -0.012 offset to the other
  side of the track (now 32 px apart).
- **Centred the default view on the in-city station spread at zoom 11**
  (34.05, -118.31): LA is huge and mostly not on a rail line.
- **Known limitations:** the source rounds coordinates to 4 decimals (~11 m),
  fine for ring bands of 160 m and up; recovered points are Census
  interpolations (about half non-exact); ~9% of rows have no NAICS and are
  invisible to the storefront filter; the LA map is 5.8 MB (San Francisco
  2.6 MB) - it embeds and renders correctly under the lean venv but is worth
  watching before deployment (open in `PLAN.md`).
- **Ran the drift check across all three cities after committing: zero
  drift, every count unchanged** (San Diego and San Francisco exactly as in
  the earlier baseline entry below; Los Angeles as listed above). LA's
  geocoding step replayed from its content-hash cache rather than the
  network, and the excluded-stations files were byte-identical. All three
  `heatmap.html` files differed from HEAD only in Folium's random IDs, and
  those cosmetic diffs were reverted. This is the current three-city
  baseline.
- **Verified all three cities against the lean venv:** Overview lists all
  three; each city page loads its map iframe with Leaflet, that city's full
  legend and every line label, no Streamlit exception blocks, clean console.

### 2026-09-18 - Hygiene: shared modules, tooling, and making the project standalone

- **Ran the full pipeline from scratch for both cities against the first
  commit: zero drift. This is the row-count baseline for
  `pipeline/drift_check.py`.** San Diego: 59,684 raw -> 43,563 in-city ->
  12,988 storefront -> 12,886 with coordinates -> 12,886 after bounds ->
  12,886 after dedup; 47 stations; 2,971 of 12,886 businesses within a ring.
  San Francisco: 295,151 raw -> 260,103 active -> 20,562 storefront ->
  20,093 with coordinates -> 20,067 after bounds -> 20,067 after dedup (8
  blank business names filled from the owner name); 147 line-stops thinned
  to 49 stations (J 12 of 23, K 14 of 20, L 14 of 24, M 16 of 26, N 15 of
  32, T 11 of 22 kept), 65 stops cut; 13,874 of 20,067 businesses within a
  ring. Both raw inputs were unchanged since download (2026-09-18), so
  this is a code-drift result. Both `heatmap.html` files differed only in
  Folium's random element IDs; those cosmetic diffs were reverted rather
  than committed.
- **Fixed a false positive in the new drift check: line endings.** The first
  run flagged `excluded_stations.csv` as drift. Cause: on Windows with
  `core.autocrlf=true`, pandas writes CRLF while git stores LF, so a
  regenerated CSV always differed from `HEAD` - confirmed by comparing 66
  CRLFs on disk against 0 in `HEAD` and byte-identical content after
  normalizing. `drift_check.py` now normalizes CRLF to LF at byte level on
  both sides, matching what git does on commit; still never decodes text.
  The check earned its keep on its first run by finding a real
  environment-dependent bug in itself.
- **Made the repo standalone: nothing depends on, or needs to be read
  alongside, the earlier prototype.** Removed
  `docs/starting_briefing.md` (the hand-off document; its architecture
  tradeoff reasoning is preserved in the "Project origin" entry below, its
  lessons in `project_context.md`), `pipeline/map_helpers.py` (a hand-off
  from the prototype's window that duplicated `map_common.py`; its one
  non-duplicate, the Leaflet.heat fixed-pixel-size explanation, moved into
  `map_common.py` as a comment), and the `docs/seattle_skills_for_review/`
  staging copies (byte-identical to the originals). Reworded every code,
  config and doc comment that said "the source project" to say what it
  means directly; the only remaining mentions of Seattle are as evidence
  (the catch-all NAICS hand-sample in `naics.py`, this log). Also removed:
  unused pipeline requirements (`usaddress`, `rapidfuzz`, `jupyterlab`,
  `requests`) and `altair` from the deploy requirements (the app draws no
  charts), the Altair-only CSS reset in `components.py`, the redundant
  `NAICS_STOREFRONT_PREFIXES` (duplicated `NAICS_GROUPS`) and the unused
  `load_taxonomy()` wrapper. A scan found no unused config constants or
  imports. `docs/city_shortlist.md` was rewritten as current state (its
  "update" paragraphs and struck-through table are history that lives
  here). Session tags ("Session 2") were stripped from code comments.
- **Committed skills and the subagent to the repo, and gitignored
  `.claude/launch.json` and `.venv-lean/`.** The prototype kept all of
  `.claude/` out of git as local workflow tooling. Here `CLAUDE.md` and
  `PLAN.md` name the skills and agent as part of the documented process,
  so they are committed; `launch.json` holds machine-specific ports and
  paths, so it is not (the `deploy-verify` agent recreates it).
- **Created the first git commits.** No git identity was configured
  (neither global nor repo-local), so commits pass the identity per command
  rather than writing config: `dacekroberts` /
  `49654908+dacekroberts@users.noreply.github.com`, the identity the
  owner's earlier project documented for the same GitHub account. Change it
  if that is wrong.
- **Named the log `DECISIONS.md` (uppercase), matching `CLAUDE.md` and
  `PLAN.md`,** rather than the lowercase `decisions.md` used in the
  request; case matters in git and the adopted skill refers to the
  uppercase name.

- **Split documentation three ways: `docs/project_context.md` (current
  state, rewritten in place), `DECISIONS.md` (this file, append-only),
  `PLAN.md` (open work).** Previously `project_context.md` carried all
  three, including "updated ... superseded same day" notes and per-run row
  counts inline, which made the current state hard to read and the history
  easy to lose. The layout follows the earlier single-city prototype's
  briefing / plan / decisions split. Superseded reasoning and every count
  moved here; nothing was dropped.
- **Renamed each city's `step5_map.py` to `step3_map.py`.** The `5` was a
  leftover from the prototype's pipeline, which ran two further analysis
  steps (ring/chain/ridership statistics) before rendering the map. Those
  analyses are out of this project's scope, so a city's steps are now
  1 stations, 2 clean businesses, 3 map. A city that needs an extra step
  (geocoding, say) inserts it and renumbers; `pipeline/drift_check.py`
  globs `step*.py` in sorted order, so nothing else hardcodes the numbers.
- **Decoupled step 2 from NAICS.** Both cities' `step2_clean_businesses.py`
  filtered on NAICS prefixes directly, which would have forced a rewrite
  for New York, Chicago and Philadelphia. Added
  `pipeline.taxonomies.filter_to_storefront()` (keeps rows where the
  taxonomy's `classify()` is not None); each city's config now names only
  its raw classification column (`RAW_CLASSIFICATION_COLUMN`), which step 2
  renames to the taxonomy's `VALUE_COLUMN` before filtering. Verified
  neutral: San Diego 43,563 -> 12,988 and San Francisco 260,103 -> 20,562
  storefront rows as before, and both `businesses_clean.csv` files
  byte-identical to the pre-change versions.
- **Extracted `pipeline/map_common.py` from the two near-identical city map
  scripts** (~90% duplicated once the second city existed). Fixed while
  extracting: the legend text, tooltip label ("NAICS code:") and category
  grouping were hard-wired to NAICS, so a local-taxonomy city would have
  shown wrong labels - taxonomy modules now expose `FIELD_LABEL`,
  `VALUE_COLUMN` and `legend_label()`, and a synthetic Philadelphia-style
  render contained no "NAICS" text; business and station names went into
  tooltip HTML unescaped (`<`/`&` broke or injected markup; "Park & Market"
  was affected in both cities) - now escaped; the reason for wrapping
  `FastMarkerCluster` in a `FeatureGroup` (its own `show=` doesn't hide at
  load) is commented in code. Verified by a normalized-Folium-ID diff
  against the old maps: only the escaped names and re-indented templates
  differed; point counts unchanged; browser render identical, no console
  errors.
- **Reviewed the earlier prototype's four skills and one subagent and
  adopted three, folded one, skipped one.** Adopted, adapted:
  `deploy-verify` (agent), `pipeline-drift-check` (skill, backed by a new
  `pipeline/drift_check.py`), `decisions-entry` (skill). Folded three ideas
  from `new-transit-line` into `add-city` instead of adopting it (check how
  close stations sit relative to the outer ring; grep city pages for
  hardcoded prose like "six lines"; stations excluded for lying in other
  cities are a new data-sourcing project, not a config change), because
  `add-city` already covers the same ground for this project's per-city
  layout. Skipped `safe-rename` for now (no README/devcontainer/deployment
  for it to keep in sync), leaving a one-line note in `add-city` about
  updating the Overview's `CITIES` page path on a rename.
- **Adapted the drift check for live data.** The prototype's check assumed
  a static raw snapshot. Here raw files come from live portals (the San
  Francisco dataset carries a daily `data_as_of`), so `drift_check.py`
  re-runs against the raw files on disk without re-downloading and prints
  each raw input's size and modified time, letting a reader separate code
  drift from source drift. The Folium random-ID normalization is kept.
- **Verified the app against a lean venv for the first time.** All earlier
  browser checks ran under a global Python that had folium and geopandas
  installed - exactly what a lean check exists to avoid. Built
  `.venv-lean` from `requirements.txt` alone (streamlit 1.64.0, pandas
  3.0.6; confirmed `import folium` and `import geopandas` fail there) and
  ran the `deploy-verify` procedure by hand against it: the server started
  with a clean log; the Overview listed both cities; both city pages loaded
  their map iframe with Leaflet present, all of that city's transit lines in
  the legend, and no Streamlit exception blocks; the console was clean
  except for two 404s on a *direct URL* load of a city page, which are
  Streamlit's own `_stcore/health` and `host-config` probes at the
  page-relative path (they succeed at the root path) - framework behaviour,
  not app code, and absent when navigating in-app.

### 2026-09-18 - San Francisco (second city)

- **Added San Francisco: 295,151 rows -> 260,103 active -> 20,562 storefront
  -> 20,093 with coordinates -> 20,067 after bounds/dedup; 49 stations.**
  Source: DataSF Registered Business Locations (`data.sf.gov`, Socrata id
  `g8m3-pdis`), downloaded pre-filtered server-side to
  `city='San Francisco'` (the full dataset is ~356k rows including
  out-of-city registrants). Pre-geocoded via a WKT `location` point, so no
  geocoding step. Active = `administratively_closed` blank. Only ~37% of
  San Francisco rows carry a NAICS code (self-reported), so density is a
  floor, not a count.
- **Scoped rail to Muni Metro (J/K/L/M/N/T, route_type 0); excluded the F
  heritage streetcar, the cable cars, and BART.** F is a separately
  branded service with different rolling stock; cable cars are a different
  mode; BART is regional and crosses county lines, which would have
  reintroduced the cross-boundary scoping problem San Diego needed.
- **Thinned Muni Metro's stations from 147 stops to 49 using four ordered
  filters** ("sub-transit-line filters", `docs/sub_transit_line_filters.md`):
  subway stations always kept; each line's two terminals always kept;
  surface stops thinned to ~1 per 0.5 mi measured along the line's real
  stop-to-stop path from the most recently kept stop; stops shared by 2+
  lines force-kept. Rejected: keeping all 147 (rings overlap continuously,
  flattening the distance gradient) and subway-only (~12 stations; a real
  check found 74% of the 125 surface stops are more than 0.6 mi - the
  outermost ring - from the nearest subway station, median just over 1 mi,
  so it would have dropped the Sunset, Bayview/Visitacion Valley and
  Ingleside districts entirely). The four-filter design was specified by
  the owner. 65 cut stops are documented (line, reason, nearest kept
  station, distance) in `outputs/san_francisco/excluded_stations.csv`.
- **Hand-curated 4 station-name aliases after the direction-suffix regex.**
  A pairwise physical-distance check of the selected stations found four
  pairs under 200 ft apart that the regex could not merge because
  different lines' trips named the same platform inconsistently ("Van Ness
  Station" vs "Metro Van Ness Station", "Church St & Market St" vs "Metro
  Church Station", "Forest Hill Station" vs "Metro Forest Hill Station",
  "King St & 4th St" vs "4th St & King St"). 53 stations before, 49 after.
- **Used the mirror `muni-gtfs.apps.sfmta.com` for the GTFS feed.**
  `gtfs.sfmta.com` timed out at TCP connect from this environment (other
  hosts fine, DNS resolved); the mirror is linked from sfmta.com's own GTFS
  page.
- **Used this project's own six-colour line palette, not SFMTA's.**
  SFMTA's map colours have changed across revisions and some lines
  currently share a colour to signal combined service, which defeats a map
  needing six distinct lines; the palette also stays clear of the
  blue/orange/green business-category colours.
- **Centered the default map view on the station centroid at zoom 13**
  (37.7509, -122.4414) rather than the city's geographic centre; the
  city's compact diagonal shape left too much open water at zoom 12.

### 2026-09-18 - San Diego (first city) and the app

- **Ruled out Denver, then built San Diego first.** See the city-selection
  entries below for why; San Diego ranked easiest of the verified cities.
- **Added San Diego: 59,684 rows -> 43,563 in-city -> 12,988 storefront ->
  12,886 with valid coordinates (0 dropped on bounds, 0 duplicates);
  47 stations.** Source: City of San Diego Business Tax Certificates
  (`seshat.datasd.org`, active file). Pre-geocoded (`lat`/`lng`, 98.4%
  populated), so no geocoding step.
- **Filtered Trolley stations to city limits with a real boundary polygon
  (SANDAG `Municipal_Boundaries.geojson`), not a hand-curated name list.**
  63 distinct station names collapsed to 47 in San Diego, 16 outside
  (El Cajon, La Mesa, Lemon Grove, Santee, National City, Chula Vista).
  Several were not guessable by name - 24th Street and 8th Street Stations
  are in National City; Palm Avenue and Beyer Blvd are in San Diego.
  One alias was needed ("12th & Imperial Station (Bayside)" merged into
  its twin); the MTG Event Line shuttle was excluded as non-regular
  service.
- **Matched businesses with an exact `address_city == "SAN DIEGO"`.**
  Known limitation: neighbourhoods recorded under their own name (La Jolla
  foremost) are undercounted. Kept exact-match for consistency with the
  prototype's approach; recorded as open work in `PLAN.md`.
- **Made permanent on-map line labels AND legend entries a standing
  requirement for every transit line in every city.** Labels use the
  line's real public name, verified rather than taken from GTFS
  (`route_short_name` "Blue" vs the real "Blue Line"). Placement is
  automatic (perpendicular offset from the line's shape midpoint) with a
  per-line override; the legend entry exists so line identification
  survives an imperfectly placed label. San Diego's Silver Line needed a
  larger offset (0.016 vs 0.006 deg) to clear the dense downtown cluster.
  In-ring plotting: 2,971 of 12,886 businesses fall within a 0.6 mi ring
  and are plotted by default.
- **Embedded maps as pre-rendered static HTML (`st.components.v1.html`),
  not `streamlit-folium`.** `streamlit-folium` would put folium into the
  deployed runtime, which the lean/heavy requirements split exists to
  avoid. This resolved a question that had been open since the start.
  The Overview picker uses Streamlit's native `st.map` plus `st.page_link`
  buttons - one picker feel with no folium and no bidirectional component.
- **Gave the app a UI scheme deliberately different from the prototype's:**
  light base, teal accent `#0d9488` (`.streamlit/config.toml`), Space
  Grotesk (`app/components.py`), versus the prototype's dark theme, default
  red accent and Inter - so the two portfolio projects read as distinct
  products.
- **Decided the project is never named after a city.** "Expanded Heatmap"
  (a placeholder until a proper name is chosen) is the only macro-level
  identity; a city name labels only that city's own page. Matches the
  hybrid architecture: an area-selector page, then per-city renders.
- **Created the `add-city` skill and a root `CLAUDE.md`** from what actually
  worked for San Diego, so later cities follow a process rather than
  re-deriving it.

### 2026-09-18 - City selection, live verification, taxonomy plurality

- **Researched the 25 largest US cities against three criteria and
  shortlisted 10.** Criteria: expansive rail transit; public transit open
  data; public business-license data with a classification field plus
  address/geometry. Initial ranking: New York, Chicago, Los Angeles,
  Philadelphia, San Diego, San Francisco, San Jose, Denver, Boston,
  Washington D.C. Seattle - the prototype's city and the only one with a
  known-good pipeline - was swapped out for D.C. by explicit decision, and
  D.C. placed 10th; Seattle's code patterns carry over but its dataset does
  not. Full rationale and per-city findings: `docs/city_shortlist.md`.
- **Ruled out Denver on live-verified data, not the shortlist pass.** Its
  "Active Business Licenses" dataset (checked on both the Denver ArcGIS hub
  and the Colorado Information Marketplace mirror) has no address, no
  classification and no geometry - only `License_Num, License_Type,
  License_Sub_Type, License_Status, Entity_Name, Trade_Name,
  Expiration_Date`. All 347 datasets in Denver's catalog were searched for
  an alternative; none qualified. A "Business License Data Explorer" the
  first-pass research cited turned out to be Anaheim's (owner account and
  map extent), not Denver's. **Lesson made a rule (CLAUDE.md, `add-city`
  Step 0): live-verify a city's actual field schema before any pipeline
  work; dataset titles and search summaries are not evidence.**
- **Re-verified all 10 shortlisted cities live (schema pulls plus sample
  rows).** Against the original NAICS-required criterion: pass - Los
  Angeles, San Diego, San Francisco; pass with caveats - Boston (its only
  NAICS+address dataset is a 978-row certified-vendor directory, not a
  general registry) and Washington D.C. (no NAICS, and its lat/long
  fields are truncated to whole degrees, so it needs address geocoding);
  fail on NAICS alone - New York, Chicago, Philadelphia (each has real
  geocoded license data under its own taxonomy); fail outright - San Jose
  (no bulk business-tax dataset on either official portal; the only source
  is a third-party lookup tool with no export) and Denver.
- **Dropped the requirement that a city's classification be NAICS
  ("taxonomy plurality"). Supersedes the same-day plan to use NAICS as the
  single shared national classification layer.** That plan assumed every US
  city self-reports NAICS at licensing; verification showed three of ten do
  not. Rather than disqualify real cities over a naming difference, each
  city now names a taxonomy system and a module in `pipeline/taxonomies/`
  maps it into the shared buckets (Retail / Food service / Personal
  services). This also sets up non-US cities (the EU's NACE was the
  concrete example) as one more module rather than a rewrite. The
  bucket-based design from the superseded plan survived intact - it is why
  adding taxonomies was cheap. The three local modules (`nyc_dca`,
  `chicago_license`, `phl_licensetype`) are skeletons mapping only values
  seen in sample rows; each needs a full `SELECT DISTINCT` pull before use.
  Reclassified New York, Chicago and Philadelphia from fail to pass.
- **Ranked passing cities by ease of implementation: San Diego, San
  Francisco, Los Angeles, Chicago, New York, Philadelphia; Boston and
  D.C. caveated.** Factors: taxonomy already built (NAICS) vs skeleton,
  API simplicity, geocoding completeness, size of the rail system
  (station-scope decision), Philadelphia's Carto API and WKB geometry.
  Continue down this order.

### 2026-09-18 - Project origin and architecture

- **Scope: the heatmap only, commercial density only.** Generalized from an
  earlier single-city prototype (Seattle's Link light rail). Carried over
  the heatmap page's concept and lessons; not its Findings/Methodology
  pages and not its ridership axis. Priority is map coverage and user
  functionality. Ridership and deep interpretive analysis are out of scope
  until asked.
- **Chose a hybrid map architecture: an area-selector macro page routing
  to independent per-city detail maps.** Option A (one global map with
  city checkpoints) risks a real performance ceiling - the prototype needed
  marker clustering for 11,409 points in one city, plus a custom
  cluster-icon fix and a fixed-pixel map to work around a Leaflet.heat init
  bug (Leaflet.heat issue 95: an uncaught IndexSizeError on init when the
  container size isn't resolved silently stops every later `.addTo(map)`),
  and those problems would compound across cities in one instance.
  Option B (independent maps only) is the mechanical extension but has no
  "zoom out and see everything" feel. The hybrid gives the single-map
  navigation feel without loading more than one city's business points at
  once. Each city map is its own Leaflet instance with its own bounds.
- **Kept the pipeline/app split: a heavy offline pipeline writes small
  static files; the deployed app only reads `outputs/`.** Geopandas can't
  be a runtime dependency on Streamlit Cloud. `requirements.txt` stays
  lean (streamlit, pandas, altair); geo dependencies live in
  `requirements-pipeline.txt`.
- **Per-city folders and per-city config instead of a shared registry
  loader, for now.** `data/<city>/{raw,processed}` (gitignored),
  `outputs/<city>/` (committed), `pipeline/<city>/`. A shared
  `data/registry.yaml` was deliberately not built with one, or even two,
  cities - generalize once the common shape is visible (open in `PLAN.md`).
- **Made the projected CRS a per-city value.** The prototype hardcoded UTM
  10N; a wrong zone is the degrees-vs-metres bug one level deeper. San
  Diego is EPSG:32611 (11N); San Francisco EPSG:32610 (10N), independently
  derived from longitude, not copied.
