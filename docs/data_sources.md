# Where every piece of this project's data comes from

One row per source, per city. This is the master provenance list: if a map
shows something, its source is named here, with the endpoint it came from and
the filter applied at download.

It exists because the endpoints were previously scattered — some in a city's
`config.py` comment header, some only inside a `step*.py` error message, and
several (San Francisco's boundary layer) nowhere at all. That is a problem for
three reasons: a reader cannot check the work, a dead endpoint is invisible
until a rebuild fails, and the licence question below cannot be answered
source by source if the sources are not listed.

**Every source is a public government dataset.** Nothing here is scraped,
purchased, or behind a login.

## How to keep this current

- **Adding a city adds its rows here, in the same commit** — provenance *and*
  licence together. The `add-city` skill makes both a Step 0 requirement and
  re-checks them at Step 9; a city whose data is mapped but whose terms are
  unrecorded is not finished, because afterwards that gap is invisible — it
  looks exactly like a city that was checked.
- Record the **endpoint**, the **server-side filter** (the download is often
  filtered — that filter is part of the provenance), and the **date retrieved**.
- Record the **licence, and anything the source requires this project to
  display**. Do not infer permissive terms from the fact that a source is
  government open data: the review below found everything from public-domain
  dedications to a feed that forbids modifying its data, and both extremes
  inside one city. Socrata states a licence directly at
  `<domain>/api/views/<id>.json` (`license`, `licenseId`, `attribution`); a
  missing value there means "go read the terms", not "no restrictions".
- **A new required notice goes in the notices section below**, which gates the
  public deploy. A new clause needing a human decision goes to the owner and
  then to `DECISIONS.md` — not resolved by reading it generously.
- When an endpoint dies, leave the old row and mark it dead with the date,
  rather than overwriting it. Dataset IDs get retired: New York's borough
  boundaries moved from `tqmj-j8zm` (now 404) to `gthc-hcne`, and the MTA
  retired its `web.mta.info/developers` GTFS path in favour of an S3 bucket.
  A silently-replaced URL loses that history.
- Raw downloads are **not** committed (`data/<city>/raw/` is gitignored). Only
  the rendered `outputs/` are. So these endpoints plus the recorded filters are
  the only way to reproduce a build.
- **Declare the source encoding.** Every city's `config.py` sets
  `SOURCE_ENCODING` and every raw read passes it, rather than relying on the
  default. pandas defaults to UTF-8 and *raises* on anything else, which is
  safe — but the failure lands on whoever adds the next city, and the tempting
  fix (reach for `latin-1` to make the `UnicodeDecodeError` go away) corrupts
  accented characters **without failing**, so nothing catches it downstream.
  Declaring it makes the choice reviewable and part of the provenance. Every
  built city so far is `utf-8`; this bites on non-US cities, where Quebec data
  in particular is still often published in `latin-1`. Note that mojibake
  in a *terminal* is usually the Windows console codepage, not the file — check
  the bytes before changing the declaration.
- **Read a new city's whole catalogue, do not grep it.** Listing every package
  name and reading them costs about a minute and ~3 KB; keyword-filtering the
  list reintroduces exactly the bias that pulling the full list was meant to
  remove. Montréal proved it on 2026-09-21: `locaux-commerciaux`, a 28,621-row
  agglomeration-wide survey of street-level commerce with NAICS codes and 100%
  coordinates, contains none of the words *business*, *licence*, *permis*,
  *entreprise* or *commerce*, and a keyword scan wrongly concluded the city was
  food-only. Neither does `unités d'évaluation foncière`, its property roll.

## Where each country's sources live

**This file was split by country on 2026-09-27.** It had grown to about 55,000
words, almost all of it per-city and per-country sections, and a session
reading about one city loaded every one of them. Those sections now live in one
file per country under [`data_sources/`](data_sources/), moved verbatim with
their headings: each country's rows of the business, transit, boundary,
geocoding and licence tables, and every section about its cities' sources.
What stays here is what every city shares: the rules above, the notes on the
transit and boundary tables, the basemap, the removal-request commitment, the
obligations that are not notices, the numbered notices gate and the deploy
gate.

**Adding a city adds its rows to its country's file**, under the same headings
used here; a country's first city creates that file and a row in this table.
`scripts/check_provenance.py` reads this file and every file in `data_sources/`
together, so a row in either counts and a row in neither still fails.

| Country | File | Cities |
|---|---|---|
| United States | [`data_sources/united-states.md`](data_sources/united-states.md) | San Diego, San Francisco, Los Angeles, Chicago, New York, Philadelphia, Miami (Regional), Boston, Washington D.C. |
| Canada | [`data_sources/canada.md`](data_sources/canada.md) | Vancouver (Regional), Montréal, Calgary, Edmonton, Toronto |
| Mexico | [`data_sources/mexico.md`](data_sources/mexico.md) | Mexico City, Guadalajara (Regional), Monterrey (Regional) |
| Spain | [`data_sources/spain.md`](data_sources/spain.md) | Madrid, Barcelona |
| Ireland | [`data_sources/ireland.md`](data_sources/ireland.md) | Dublin |
| Italy | [`data_sources/italy.md`](data_sources/italy.md) | Milan, Rome |
| France | [`data_sources/france.md`](data_sources/france.md) | Paris, Marseille, Toulouse, Lille (Regional), Rennes |
| Norway | [`data_sources/norway.md`](data_sources/norway.md) | Oslo |
| Denmark | [`data_sources/denmark.md`](data_sources/denmark.md) | Copenhagen |
| Czechia | [`data_sources/czechia.md`](data_sources/czechia.md) | Prague |
| Netherlands | [`data_sources/netherlands.md`](data_sources/netherlands.md) | Amsterdam, Rotterdam |
| Latvia | [`data_sources/latvia.md`](data_sources/latvia.md) | Riga |
| Brazil | [`data_sources/brazil.md`](data_sources/brazil.md) | São Paulo, Rio de Janeiro, Belo Horizonte, Brasília, Salvador, Fortaleza (Regional), Porto Alegre (Regional), Recife (Regional), Santos (Regional) |
| Hong Kong | [`data_sources/hong-kong.md`](data_sources/hong-kong.md) | Hong Kong |
| South Korea | [`data_sources/south-korea.md`](data_sources/south-korea.md) | Seoul, Daegu, Busan |
| Taiwan | [`data_sources/taiwan.md`](data_sources/taiwan.md) | Taichung, Taoyuan, Taipei (Regional) |
| Japan | [`data_sources/japan.md`](data_sources/japan.md) | candidate cities' licence reads |

## Business registries

The rows are per country: each file in [`data_sources/`](data_sources/)
opens with its own rows of this table, followed by the notes on its cities'
registries (Boston's, Madrid's and Dublin's Step 0 findings among them).

## Transit feeds

**Titled “Transit feeds (GTFS)” until 2026-09-22.** The table immediately below
is still all GTFS and always was; what changed is that the section now also
holds a subsection for rail that is **not** a feed, and a parent heading
claiming GTFS would have misdescribed its own contents. Every row in the first
table is a feed; everything under “Rail geometry that is not a GTFS feed” is
not.

Both tables' rows are in each country's file, under the same headings.

### Rail geometry that is not a GTFS feed

**These cities are kept OUT of the feed table rather than filed under a
heading that would misdescribe them**, because a non-feed source has no
`feed_info.txt`, no validity window and no `route_id` — three of the things
every note in that table turns on — so a row there would have meant empty
columns. Same section, its own subsection, its own columns.

**Two different reasons land here, and they are not the same case.**

- **Mexico City and Guadalajara come from OpenStreetMap via Overpass**, because
  no usable feed exists. An OSM source also has no agency holding the licence:
  both are **ODbL 1.0**, covered by **notice 1**, which since these builds
  covers *data* and not only basemap tiles. See `.claude/skills/osm-rail/`
  before adding another.
- **Madrid comes from CRTM's own ArcGIS feature services**, and there the
  operator's feed exists and downloads cleanly — it is rejected because CRTM's
  licence obliges a reuser to keep displayed information *“siempre
  actualizada”* and that feed has not been refreshed since 2025-05-30. A
  licence consequence rather than an absence, and the licence is CRTM's own,
  not OpenStreetMap's. **Madrid sat under the OpenStreetMap heading for part of
  2026-09-22**, which was wrong in the way this subsection exists to prevent.

**Why three Overpass mirrors, and how one is chosen.** They are tried **in the
configured order**, and the first host returning HTTP 200 with a **non-empty
`elements` list** wins; every other outcome — a non-200, an exception, or a 200
with an empty body — sleeps briefly and advances to the next. Three, because
across these two builds each of the three failed at least once and none failed
consistently: `overpass-api.de` returned 504 several times and 429 once,
`overpass.kumi.systems` 504 several times, and `overpass.osm.ch` **answered 200
with an empty body** — all at different times, for the same query. A failure is
a fact about that host at that moment and not about the city, so one mirror
would make the build's success a coin flip.

**A 200 with no elements is treated as a host FAILURE and is never cached**,
which is the half that is not obvious. `overpass.osm.ch` once returned 272
bytes and an empty element list for the routes query; the fetcher cached it,
and the caller then reported *"every ref has exactly 2 direction relations"* —
**a vacuous truth over an empty set**. Both cities' step 1 now assert
non-emptiness before any check that could pass vacuously. Responses that do
succeed are cached to the gitignored `data/<city>/raw/osm_*.json`, so a re-run
or a drift check never depends on which mirror answered. Guadalajara makes
**two passes** over the host list before giving up where Mexico City makes one,
and sleeps 3 s between hosts where Mexico City sleeps 2.

## Boundary layers

Used to scope stations and businesses to the city. Not optional: San Diego's
Trolley serves six other cities, and 54 of Los Angeles' 110 rail stations lie
in 23 other municipalities.

The rows, and the notes on individual cities' layers, are in each country's
file.

## Geocoding

The rows are in the files of the three countries that use one: the United
States (the Census Bureau's bulk geocoder), Latvia (Riga's address join) and
Hong Kong (the Address Lookup Service cross-check).

## Basemap tiles

Rendered maps use Folium's default OpenStreetMap tiles. Attribution is in the
rendered HTML. Choosing a tile provider deliberately is still open in
`PLAN.md`.

## Licences and terms of use

Reviewed 2026-09-21. This records what each source's own published terms say,
and what could not be established. It is a developer's reading of public
documents, not legal advice, and none of it has been reviewed by a lawyer.

A separate question is already settled: what is *appropriate* to publish,
independent of what is *permitted*. That is in `docs/excluded_categories.md`.

Each source's reading is in its country's file: the rows of the tables
*Explicit and permissive — confirmed* and *Transit feeds (GTFS)*, the sections
on Madrid, Seoul, Daegu and Busan, Brazil, Taiwan, Japan, CRTM and Barcelona,
and the United States' own tables and open questions (*Permissive on reading
the terms themselves*, *Still not established*, the API-account practice, the
agency-branding question). What stays here is what applies to every city.

### Transit feeds (GTFS) — checked 2026-09-21

Line geometry is redrawn from each feed's `shapes.txt` into every map, so these
terms bear directly on what is published. **No feed in this project declares a
licence in `feed_info.txt`** — LA Metro's even includes a `feed_license` column
and leaves it empty, pointing to its developer terms instead. Several feeds ship
no `feed_info.txt` at all (Miami, Calgary, Toronto), and two ship one that
carries a validity window but no licence (Montréal, Vancouver), so in every case
the agency's own terms page is the only source and every row below was read from
one.

The table's rows are in [`united-states.md`](data_sources/united-states.md)
and [`canada.md`](data_sources/canada.md).

**The agreements quoted above are stored locally**, in
[`licenses/`](licenses/) — source URL, retrieval date and SHA-256 for each are
in that directory's `README.md`, **which is the list**; a count kept here said
“six”, then “seven”, while the directory grew past twenty. Every one of them is revocable and amendable
without notice, so the clauses quoted above are checkable against the text that
was actually agreed to rather than against a URL that may have moved on.

### Basemap tiles — one active compliance item

The maps render **OpenStreetMap** tiles, fetched directly from
`https://tile.openstreetmap.org/{z}/{x}/{y}.png`.

- **Data licence: ODbL 1.0.** Attribution is required — credit OpenStreetMap
  and link to the licence, visibly, not "beneath UI, behind toggles, or
  off-screen".
- **This requirement is met.** Every rendered map emits
  `© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>
  contributors` in the map corner, and the link is present in the committed
  HTML.
- **The tile service itself is the open question.** The OSMF Tile Usage Policy
  makes availability "best-effort: there is no SLA or guarantee", forbids
  "bulk downloading … any pre-emptive fetching of tiles other than those a
  user is actively viewing", requires HTTPS (this project uses HTTPS) and a
  caching-respectful client. A portfolio site drawing tiles only for what a
  visitor is looking at is ordinary interactive use, not bulk use — but the
  policy is explicit that there is no guarantee behind it. This is the same
  decision already open in `PLAN.md` as "tile provider"; it should be settled
  deliberately before launch rather than by default.

## Commitment: removal requests are honoured, not argued

Every licence reviewed here enforces the same way. Chicago's terms say the
city "may require a user of this data to terminate any and all display,
distribution or other use"; Open NY says the State may require you, "by
providing you with a notice in writing", to cease using or displaying its
content; LA Metro says that on termination you "shall immediately remove the
Transport Information and all references to it". The remedy contemplated
throughout is a request to stop.

**A second trigger, added 2026-09-21: an unresolved licence position is
enough.** Points 1-5 below all fire on a publisher *asking*. This one fires on
finding out. **It now has exactly one live subject, Philadelphia** - the three
questions this was written for were investigated on 2026-09-21 and two closed:
SEPTA expressly grants the right to use, reproduce and redistribute its
datasets and claims only its Logo as a trademark, and Miami-Dade's own Open
Data Hub Terms of Use turns out to exist and to contain nothing but an accuracy
disclaimer. Philadelphia is different in kind: its dataset page incorporates
the City's Terms of Use, which prohibit republication and modification without
written permission. So the commitment stands and is aimed where it belongs:
**if the City of Philadelphia confirms that those terms govern its datasets,
Philadelphia comes off the site without waiting to be asked.** This is disclosed on the site itself rather than kept
here - `app/components.py`'s `render_site_notices()` carries the same wording
in the footer of every page, beside the required attributions, so a reader
learns it at the same moment they learn where the data came from. Keep those
two wordings and `excluded_categories.md` consistent; all three are one
promise.

**A third trigger, added 2026-09-22: a licence that ENDS BY ITS OWN TERMS.**
The first two fire on a publisher asking and on this project finding out.
This one fires on neither — **Licence Mobilités Art. 11.1 terminates *de plein
droit, sans préavis* on breach**, so the grant can simply stop, with no notice
to receive and nothing to discover. It is the first revocable grant in this
project: CC BY, Licence Ouverte, the PSI licences and ODbL are all perpetual,
and none of them can lapse without someone saying so.

**Owner's decision 2026-09-22: this is ACCEPTED, and Paris is built on it.**
The response is the same as for the other two triggers and is decided in
advance rather than under pressure — **if the grant lapses, Paris is archived:
its page comes off the site and its entry out of `app/cities.py`, while its
pipeline, brief and `DECISIONS.md` record stay in the repository.** That is
the distinction worth keeping: a city coming *down* is not the same as a city
being *deleted*, and the build remains reproducible if the position changes
back. The rejected alternative was declining to build Paris at all, which
would have cost the only national register in the screen that buys six cities,
to avoid a risk that is answerable by taking one page down.

**This project commits, in advance, to honouring such a request.** Stated so
that it is a standing position rather than a decision made under pressure:

1. **If a data publisher asks this project to stop displaying its data, it
   will stop.** The affected layer, or the whole city, comes down. No case
   will be argued first, no justification will be requested, and compliance
   will not be made conditional on the publisher explaining itself.
2. **If a business owner asks for their listing to be removed, it will be
   removed** — see `excluded_categories.md`, which says the same thing to the
   people it concerns. They do not have to give a reason.
3. **If anyone raises a privacy concern about a specific pin**, it is treated
   as a removal request under point 2 and actioned first; any disagreement
   about whether the concern was well-founded is separate from taking the pin
   down.
4. **A request is honoured even if this project believes it is in the right.**
   The licence review found nothing forbidding what is built here, and that
   conclusion does not change the answer to a request. Being permitted to
   display something is not a reason to insist on displaying it.
5. **Removal is the immediate action; the reasoning gets recorded afterwards**
   in `DECISIONS.md`, with what was removed and who asked, so the trail stays
   honest.

This is not a legal position and it does not waive or create anything. It is
a statement of how this project behaves, published because a reader who might
want something removed should be able to see it without asking first.

## Obligations that are NOT notices — four classes, one per publisher

**A notice is text on a page. These are not.** Each was found by reading a
licence that also granted permission freely, which is why they are easy to
miss: the grant is the headline and the obligation is a subordinate clause.

| Class | Who | What it actually requires |
|---|---|---|
| **An act owed to the publisher** | **Barcelona** 🇪🇸 | *"Users are required to inform Barcelona City Council of every project relating to or derived from their use of the data sets."* A message a person sends. Drafted at `docs/notifications/barcelona-city-council.md`, **not yet sent** |
| **A live account that must STAY live** | **WMATA** (Washington D.C.) 🇺🇸 | The terms are an API agreement, so §9(i) ends the grant when the account ends — and what lapses is the right to **publish the page**. Gate item 10 |
| ✅ **A liability ACCEPTED** | **Hong Kong** 🇭🇰 *(candidate)* | **ACCEPTED BY THE OWNER 2026-09-22.** *"you shall **indemnify** the Government and the Relevant Organisations against any allegations or claims of infringement of the rights of any person and all costs, losses, damages and liabilities incurred … which in any case arise **directly or indirectly** in relation to your use, reproduction and/or distribution of the Data"*. See the section below for what the earlier record omitted |
| 🔧 **AN ACCESS A PERSON MUST OBTAIN** | **Copenhagen / Denmark** 🇩🇰 *(candidate)* | **Added 2026-09-23 at the owner's request.** CVR's premises data needs a **Datafordeler account the owner creates by hand**, and the terms pages sit behind a **Cloudflare interactive challenge** this project does not defeat — so both the registration and the reading are **human-only work**. ⚠️ **This is NOT WMATA's class, and the difference matters.** WMATA's terms are an **API agreement**, so §9(i) ends the grant when the account ends. Copenhagen's licence is **CC BY 4.0, which attaches to the DATA and is irrevocable** — so the owner's standing practice (*register, take the data, terminate, revoke*) is **safe here and unsafe there**. ✅ **Close the account freely; the right to publish survives.** The similarity is the registration effort, not the obligation |

**Copenhagen and WMATA look alike at the signup form and diverge immediately after it.** Both made the owner register; only one made the account load-bearing. **The test is what the terms ARE** — an API agreement licenses *you*, so it can be withdrawn from you, while a public licence licenses *the data*, and nothing you do to your account reaches it. Recording the two in one row would have told a later reader to keep a Danish account alive forever, and implied that closing it revokes the right to publish Copenhagen. **Neither is true.**

**Hong Kong's is the one to weigh before building, not after.** Everything
else in `data.gov.hk`'s Terms of Use v1.2 (26 May 2025) is generous — download,
distribution and reproduction are permitted for **commercial and
non-commercial purposes, free of charge**, subject only to identifying the
source, acknowledging Government ownership of the IP, and proper attribution.

**The indemnity is not a notice, not a credit, and not a step in a build.** It
is an open-ended undertaking to cover the Government's costs if a third party
alleges the data infringed their rights. No other source in this project asks
for one. **It is an owner decision, and the right moment to take it is before
35,808 premises are wired into a page**, not once the city is live.

### Hong Kong's indemnity — ACCEPTED 2026-09-22, and what the first record omitted

**The owner accepted this on 2026-09-22, in chat, after the live clause was
re-read.** It is the only uncapped liability in this project. Recorded here
with its reasoning so it is a decision rather than a drift.

**Two things the first record's quote left out**, both found by reading
`https://data.gov.hk/en/terms-and-conditions` (Terms v1.2) rather than the
earlier citation of it — which is the failure mode `read-licence` exists for:

1. **"arise directly or indirectly"** — the earlier quote elided it. Broad
   causation, not just proximate.
2. **There is NO notice-and-defend clause.** The Government need not tell you a
   claim exists, you have no right to control or even join the defence, and
   nothing obliges them to mitigate or to seek your consent before settling.
   Most commercial indemnities temper exposure exactly there. This one does
   not.

**And the pairing is deliberate.** The *Disclaimer and Limitation of Liability*
section expressly disclaims any warranty of **non-infringement** — so the
Government does not promise the Data is clean **and** you indemnify them if it
is not. That section caps **their** liability to you, not yours to them: the
indemnity is one-directional and has no cap.

**What narrows it**, and why acceptance is reasonable rather than reckless: the
scope is **infringement of the rights of any person**, not general liability.
It is not "anything that goes wrong because of the map". A third party must
assert *their rights* against the Government, over this project's use of a
**government public register** republished with the attribution the same
paragraph requires. That is a narrow path, and the project's standing
commitment to **honour removal requests without argument** cuts off the likeliest
escalation before it becomes a claim.

**Probability low, magnitude unbounded** — which is the combination that gets
mis-priced, so it was priced deliberately.

#### THREE CONDITIONS, accepted with it and binding on the build

1. **Display all three required elements exactly** — identify the **source**
   of the Data, **acknowledge the Government's and the Relevant Organisations'
   ownership of the intellectual property** in it, and give **proper
   attribution to the Government, the Relevant Organisations and
   DATA.GOV.HK**. These are the same paragraph as the indemnity, and
   **unattributed use is the most likely way to draw a complaint in the first
   place.** They become numbered notices when Hong Kong is committed, not
   before.
2. **Run `python scripts/check_personal_exposure.py hong-kong` and exclude
   catch-all categories** — the Los Angeles NAICS 812990 precedent. The
   realistic complainant is an individual whose name sits at what looks like a
   home, so the privacy filter is the risk control, not a formality.
3. **This entry is condition three**, dated and reasoned.

**Extended 2026-09-24 to the CSDI Portal's terms.** The build places each licence at FEHD's
own point from the CSDI Portal (`portal.csdi.gov.hk/csdi-webpage/doc/TNC`, read 2026-09-24 by
the licence-read agent): the same shape, the same uncapped indemnity, and one addition - to
*"identify clearly the Government and the CSDI Portal as the source"*, which notice 41 does.
The owner accepted it in chat on 2026-09-24, with the switch from ALS. The privacy condition
was run the same day: FEHD's registers carry the shop sign and no licensee name at all.

#### One consistency note

**Lyon's Grand Lyon CGU 9.4 is the same shape** and was recorded as the
project's second indemnity. Accepting Hong Kong's does **not** automatically
accept Lyon's — Lyon carries two further gates (an account this project does
not create, and a trademark clause that collides with an invariant), so it
stays deferred on those grounds regardless.

## Notices this project MUST display when published

This is the operative output of the licence review. As of 2026-09-21, for the
**nine** cities built: **five sources require specific text or
acknowledgement, and one of the five is already satisfied** (OpenStreetMap);
Chicago, SFMTA, LA Metro and — since Boston was built — MassDOT were
outstanding until **2026-09-21, when all five were put on every page**
by `app/components.py`'s `render_site_notices()` — Chicago's and
SFMTA's verbatim, LA Metro's and MassDOT's in this project's own words
because neither prescribes any. They render inline rather than inside a
collapsible: Streamlit keeps a collapsed expander's contents out of the
DOM, and a notice behind a toggle is not displayed. New York adds a conditional identification requirement that is
largely already met, and CTA encourages but does not require credit.
**Building Washington D.C. added no sixth notice**, correcting what an
earlier note in this file predicted: WMATA requires no attribution and no
acknowledgement of any kind. What it did add is a second copy of MTA's
accuracy clause (§6), which is prose work on the city pages rather than a
notice to display — see item 5a below. These are obligations, not courtesies. They belong with the app work that surfaces this
page and `excluded_categories.md` (see `PLAN.md`) — publishing the maps
without them would breach terms this project has now read.

**1. OpenStreetMap — required, and ALREADY SATISFIED.** ODbL 1.0 requires
visible credit and a licence link, "not beneath UI, behind toggles, or
off-screen". Every rendered map emits, in the map corner:

> `© OpenStreetMap contributors` — linked to
> `https://www.openstreetmap.org/copyright`

This comes from Folium's default tile attribution and is present in every
committed `heatmap.html`. **Do not remove or restyle it away.** If the tile
provider ever changes, its own attribution replaces this one — it does not
simply disappear.

**2. City of Chicago — required, and DISPLAYED.** Chicago's Data Terms of
Use require any "secondary or derivative application" to carry this disclaimer,
verbatim, "at the site where the software application … can be accessed":

> "This site provides applications using data that has been modified for use
> from its original source, www.cityofchicago.org, the official website of the
> City of Chicago. The City of Chicago makes no claims as to the content,
> accuracy, timeliness, or completeness of any of the data provided at this
> site. The data provided at this site is subject to change at any time. It is
> understood that the data provided at this site is being used at one's own
> risk."

**3. SFMTA — required, and DISPLAYED.** Its transit-data licence requires
derivative works to include:

> "Reproduced with permission granted by the City and County of San Francisco.
> The information has been provided by means of a nonexclusive, limited, and
> revocable license granted by the City and County of San Francisco."

**4. LA Metro — required, and DISPLAYED.** Must acknowledge Metro as the
provider of the transit information and must not claim ownership of it. No
exact wording is prescribed; "Rail alignment data provided by LA Metro" would
meet the stated requirement.

**These three were marked NOT YET DISPLAYED until 2026-09-22, and all three
were displayed.** `app/components.py`'s `_NOTICES` carries Chicago, SFMTA and
LA Metro as its first three entries, and `render_site_notices()` is called from
every page. The labels were written before the footer existed and nothing
brought them forward when it shipped — so the list that GATES THE PUBLIC
DEPLOY understated this project's own compliance, in the direction that makes a
deploy look blocked when it is not. Found by `scripts/check_stale_claims.py` on
its first real run, which is the argument for the tool in one line.

**5. New York City — conditional, and largely already met.** Local Law 11
forbids licence requirements, but the Technical Standards Manual reserves one
condition: "DoITT may require third party entities such as application
developers to explicitly identify the **source, version, and modifications**
made to a public data set" where it is "publicly re-publish[ed] … elsewhere or
incorporate[d] … into an application."

This project already produces all three, which is a good argument for
surfacing both documents rather than only one:

- **source** — this file, with endpoint and download filter per dataset;
- **version** — the retrieval date per source, and `AS_OF_DATE` for the
  snapshot-based feeds;
- **modifications** — `excluded_categories.md`, which is precisely a
  statement of what was removed and why.

**6. CTA — encouraged, not required.** If credited, use one of CTA's own
forms: "Data provided by Chicago Transit Authority", "Data provided by CTA",
or "Powered by CTA data".

**7. MassDOT / MBTA — required, and DISPLAYED.** §4.1 of the MassDOT Developers
License Agreement requires the licensee to "Clearly acknowledge MassDOT as the
provider of the Data". No exact wording is prescribed. Same shape as LA Metro's
obligation. The agreement itself is kept at
`docs/licenses/mbta-massdot-develop-license-agreement.pdf`.

**8. INEGI (Mexico City) — required, and DISPLAYED since 2026-09-22. It is TWO
obligations rather than one.** The Términos de Libre Uso de la Información del
INEGI (`docs/licenses/inegi-terminos-libre-uso-informacion.pdf`, retrieved
2026-09-22) grant more than most sources here — §1(b)-(e) permit publishing,
adapting, extracting and even **commercial** exploitation — in exchange for:

- **§1(f), attribution in a prescribed form:** credit INEGI as author and,
  where technically possible, name the source as *"Fuente: INEGI, nombre del
  producto de donde se extrae la información"* plus the update date. For this
  project that is **"Fuente: INEGI, Directorio Estadístico Nacional de Unidades
  Económicas (DENUE)"** with DENUE's own edition date.
- **§1(g), DISCLOSURE OF TRANSFORMATION, which a source credit does not
  satisfy.** The user must be notified of *"cualquier análisis o transformación
  que haga a la información"*, and the presentation must not suggest INEGI
  performed it. **This project triggers that clause on every map**: ring
  assignment, bucketing into three categories, the storefront filter and the
  `Fijo`-only filter are all transformations. Treat attribution and disclosure
  as two separate duties — the Montréal licence has the same split, and it is
  easy to satisfy the first and miss the second.
- **§1(h), non-endorsement:** the use must not appear to represent an official
  INEGI position, nor to be endorsed, integrated, sponsored or supported by the
  source. The site-wide non-affiliation notice already covers the shape of
  this; INEGI is named explicitly for safety.
- **§1(a)** additionally forbids altering or suppressing the metadata of
  distributed copies. This project distributes no copy of DENUE — only derived
  points — so it does not bite, and is recorded so nobody has to re-derive it.

Note the two-document split: `inegi-terminos-sitio.pdf` governs **inegi.org.mx
as a website** and is NOT the data licence. Both are stored, because reading a
site-terms document as though it governed the data is what made New York look
prohibited.

**Guadalajara (Regional) needed NO new notice, which is a first.** Its
business data is the same register under the same licence, and notice 8 names
INEGI and DENUE rather than a city - so a second Mexican city is covered by the
text already displayed. Its rail credit is OpenStreetMap's, likewise already
displayed. Recorded because every previous city added at least one line to
`render_site_notices()`, and the reason this one does not is that the notice
was written around the SOURCE instead of the city.

**Guadalajara's endpoints, verified 2026-09-22:**

- **Businesses** — INEGI DENUE, entidad federativa **14 (Jalisco)**, keyless
  bulk CSV: `https://www.inegi.org.mx/contenidos/masiva/denue/denue_14_csv.zip`
  (39,432,220 bytes, real ZIP by magic bytes; member
  `conjunto_de_datos/denue_inegi_14_.csv`; **latin-1**). Scoped in step 2 to
  four municipios by DENUE's own `municipio` spelling — note **"San Pedro
  Tlaquepaque"**, not the "Tlaquepaque" SITEUR's prose uses; matching the
  operator's wording would keep zero rows.
- **Rail** — OpenStreetMap via Overpass, route relations tagged
  `network="Mi Tren"`, `route` in (`light_rail`, `subway`). ODbL 1.0.
- **Boundaries** — OpenStreetMap `admin_level=6` municipio relations, bounded
  by bbox. ODbL 1.0.

**A REJECTED SOURCE, recorded with its date because a replaced URL that leaves
no trace hides why:** the only Guadalajara rail feed in the Mobility Database
(mdb **1925**, also contained in **2366**) downloads cleanly and is **not
used**. Its own `feed_info.txt` declares `feed_end_date = **20230128**`, its
`feed_publisher_name` is **Nubenautas** (`gtfs.studio`) rather than SITEUR, and
it carries **three** light-rail routes where SITEUR publishes **four** —
**Línea 4 opened 2025-12-15**, almost three years after the feed stopped.
Using it would have omitted an operating line, 8 stations and 21 km.
`https://www.siteur.gob.mx/` itself answers HTTP 200 and is the source for this
project's gate-3 station counts (Línea 2: 10; Línea 4: 8), but publishes no
GTFS.

**Mexico City's rail geometry is OpenStreetMap, so notice 1 now covers DATA and
not only basemap tiles.** Every `*.cdmx.gob.mx` host is unreachable, so the
lines are drawn from OSM route relations (owner-approved 2026-09-22 as a
per-city exception). ODbL 1.0 attribution was already satisfied for the
basemap; the same credit now also covers line geometry, and notice 1's wording
should not imply it is only about tiles.

**This heading read "NOT YET DISPLAYED" until 2026-09-21 and was stale**, which
is worth leaving a note about because a compliance document that understates
compliance invites someone to re-fix a closed item and to doubt the rest of the
gate. The outstanding part had been that the acknowledgement appeared only on
Boston's own city page rather than "where the *site* is accessed"; that was
closed when `app/components.py`'s `render_site_notices()` began carrying all
five outstanding notices on **every** page, and this heading was not updated
with the others. Verified against `_NOTICES` on 2026-09-21.

Not required by anyone, but good practice and already partly done in the city
pages' prose: naming each business registry's publishing agency.

### What closing this fully requires

1. ~~Read Chicago's data terms of use~~ — **done 2026-09-21**, and it produced
   a mandatory notice (above).
2. ~~Read the Open NY Terms of Use document~~ — **done**, explicitly permissive.
3. ~~Establish the reuse position for NYC Open Data~~ — **done**. Local Law 11
   of 2012 forbids licence requirements and usage restrictions on NYC open
   data, so the missing licence field is compliance, not an omission. One
   condition attaches (identify source, version and modifications), which this
   project already satisfies in substance.
4. ~~Check the five GTFS feeds' terms~~ — **done**, and three of the five carry
   conditions worth acting on.
5. ~~Decide LA Metro's "modification" clause and CTA's purpose limitation~~ —
   **decided 2026-09-21**, see the notes under the GTFS table.
5b. **Decide the three "what does silence mean?" questions** — raised
   2026-09-21, all still open. SEPTA's trademark clause; the City of
   Philadelphia License's rights reservation; and **Miami-Dade's total absence
   of a reuse position** across its business registry, its boundary layer and
   its GTFS (which has no `feed_info.txt`). See the notes under the GTFS table.
   Miami's is the weakest paperwork in the project and should be decided
   first — it is also the only one of the three where no agency document exists
   to read, so settling it may mean asking the County rather than reading
   anything.
5c. **Decide the agency-branding question — official route colours AND the
   line names beside them.** Affects the cities whose agency prescribes a
   palette: San
   Diego (MTS), Los Angeles (LA Metro), Chicago (CTA), New York (MTA),
   Philadelphia (SEPTA) and — since 2026-09-21 — Washington D.C. (WMATA),
   whose wording is the one that names "confusingly similar variants". San Francisco and Miami
   are out of scope, already drawing their own palettes. **MTS's wording is the
   tightest in the project** — its trademarks "may not be used in association
   with GTFS Data", a flat prohibition rather than an application process — so
   start there rather than with MTA's, which merely needs a free application.
   The owner chose on 2026-09-21 to keep the official colours and record this
   rather than pre-emptively substituting palettes. Colours are cheap to
   reverse (one dict per city); **line names are not**, because a standing
   invariant requires every drawn line to carry its real public name. See the
   table under the GTFS notes.
6. **Display the required notices** (above) — the one thing that still blocks
   publishing, and part of the same app job as surfacing this page.
7. **Decide the tile provider deliberately**, given that OSM's tile service is
   explicitly best-effort with no SLA.
8. Optionally, read the Census geocoder's terms, which are still unread - as
   San Diego's municipal-boundary layer's are (see its row). The licence table
   is the list of what is unread; this line used to call the geocoder "the
   only source left unread" while that row said otherwise.
9. **REBOOT THE APP AFTER ANY PUSH THAT CHANGES A MODULE THE APP IMPORTS** —
   `app/cities.py`, `app/components.py`, or anything under `pipeline/` that
   `app/` pulls in. This is an operational step, not a courtesy, and it is in
   this gate because the live site spent **over three hours down** on
   2026-09-22 for want of it.

   **Streamlit Cloud's "🔄 Updated app!" re-runs the ENTRY SCRIPT only.** It
   pulls the new files and re-executes `app/Overview.py`, but every module
   already in `sys.modules` — `cities`, `components`, every `pipeline` config —
   stays as it was when the process started. So a push that adds a name to
   `cities.py` and imports it from `Overview.py` leaves the running process
   with the new script and the old module, and every page load raises
   `ImportError: cannot import name 'DEFAULT_REGION' from 'cities'`.

   The log that proves it, because the symptom is confusing enough to send
   anyone hunting a phantom: the traceback printed the **old** one-line
   `from cities import CITIES, IN_DEFAULT_VIEW, MAP_ONLY_NAV` — which does not
   mention `DEFAULT_REGION` at all — above an error naming `DEFAULT_REGION`.
   Python renders traceback source by re-reading the file from disk while
   executing a cached code object, so disk and runtime were different
   versions. Five pulls and five "Updated app!" across three hours never
   cleared it; only **Manage app → ⋮ → Reboot app** does.

   **Two routes reach that reboot, and only one works reliably on a phone.**
   In the app, **Manage app** sits in the lower-right corner - but only in a
   browser signed in to Streamlit as the app's owner. Signed out, the same
   corner shows Community Cloud's red "Hosted with Streamlit" badge and a
   round creator avatar instead, so there is no button to find, and on a
   phone that corner is exactly where one gets looked for. The dashboard
   route never touches the app page: **share.streamlit.io → sign in → the ⋮
   beside `expanded-heatmap` → Reboot**. Use it on mobile. Neither the badge
   nor the avatar is this project's - both are the host's chrome around the
   app, which app code cannot move. Recorded 2026-09-23, after the owner hit
   it on a phone for the second time.

   **`app/cities.py` changes every time a city is added**, so every future city
   carries this exact risk. Treat the reboot as the last step of adding a city,
   alongside the drift check and the `DECISIONS.md` entry.

   Before the push, run **`python scripts/check_deploy_imports.py`**, which
   tests a clean clone under `.venv-lean` — the closest local approximation of
   what the deploy pulls. It catches the mismatched-export case and the
   missing-`label_offset` case that crashed the Overview the same day. It
   cannot catch the stale-module case: nothing local can, because a fresh
   process is the one thing the live app does not do.

10. **CONFIRM THE WMATA ACCOUNT IS STILL LIVE** — before every public deploy,
    for as long as the D.C. page is published. This is a gate item rather
    than a note because **nothing in the codebase can check it**: verifying an
    account means holding its key, and this project never handles one. It is
    a human step by construction, which is exactly the kind that gets skipped.
    WMATA's terms are an **API agreement**, so §9(i) terminates the grant the
    moment the account goes — and the right that lapses is the right to
    *publish the page*, not merely to store a file. **Re-confirmed live by the
    owner on 2026-09-22.** If it ever lapses, D.C. comes down until a new
    account is registered. The full reasoning is under the WMATA entry above;
    the standing list of items like this is `docs/gated_access.md`.

**Where this leaves the project:** nothing found anywhere forbids what this
project does, and the count of **mandatory notices to display is five**.
Neither Philadelphia nor Miami added one, because SEPTA, the City of
Philadelphia License and Miami-Dade all require no attribution at all. The
fifth is **MassDOT's acknowledgement, active since Boston was built on
2026-09-21**. This paragraph also predicted a sixth from WMATA once D.C. was
built: **that was wrong, and D.C. is now built.** WMATA's terms require no
attribution and no acknowledgement — its constraints are on what may be SAID
(§6 accuracy, §9 deletion on termination, the trademark clause), not on what
must be shown.

**9. City of Vancouver — required, and DISPLAYED.** The Open Government
Licence – Vancouver requires this exact sentence wherever its information is
used:

> `Contains information licensed under the Open Government Licence – Vancouver.`

Note the British spelling "Licence" and the EN DASH. This licence
**terminates automatically on breach** — "if you fail to comply with any of
them, the rights granted to you under this licence… will end automatically" —
so the notice is not cosmetic. In `app/components.py`'s `_NOTICES` since
2026-09-21, when Vancouver was built.

**10. City of Surrey — required, and DISPLAYED.** The same OGL template, with
Surrey's own wording, which is **not interchangeable with Vancouver's**:

> `Contains information licensed under the Open Government License - City of Surrey.`

Note the American spelling "License" and the HYPHEN. Surrey's OGL also
terminates automatically on breach. Required because the Vancouver map is
regional and includes Surrey's own business licences.

**11. TransLink — required, and DISPLAYED. Its wording is a TRAP.** The GTFS
Static Terms of Use require the Legend to be "prominently displayed" in
exactly this text:

> "Route and arrival data used in this product or service is provided by
> permission of TransLink. TransLink assumes no responsibility for the accuracy
> or currency of the Data used in this product or service."

**TransLink mandates TWO different legends and this is the GTFS STATIC one.**
Its Open API terms mandate a different text beginning "Some of the data used in
this product or service…", which would **not** satisfy the GTFS terms. This
project uses static GTFS, so the "Route and arrival data" wording is the
correct one. Both texts are stored in `docs/licenses/`;
`translink-gtfs-static-terms-of-use.txt` is the operative file and
`translink-open-api-terms-of-use.txt` is kept only because it looks like it
governs and does not.

One Legend covers both cities: Surrey has no rail of its own, so the regional
build inherits TransLink's terms once rather than twice. Two further
obligations come with it and are not notices: **no TransLink marks beyond the
Legend** (satisfied by construction — this project draws its own geometry from
`shapes.txt` and reproduces no roundel), and **responsiveness if TransLink asks
who is using the data**, which was read as an obligation to answer rather than
a precondition of use (`DECISIONS.md`, 2026-09-21).

**12. Ville de Montréal — required, and DISPLAYED. Its condition is BROADER
than standard CC-BY, and this project triggers the broad part every time.**
`locaux-commerciaux` is CC-BY 4.0 (`license_id: cc-by`, confirmed from CKAN
`package_show`). The City's own licence page,
`donnees.montreal.ca/pages/licence-d-utilisation`, adds three conditions, read
2026-09-21:

> "Vous devez créditer les données et les contenus que vous utilisez et
> **préciser si des modifications ont été effectuées ou si des interprétations
> en ont été tirées**."

— credit the data **and state whether modifications were made or
interpretations drawn**. Ring density, category bucketing and storefront
filtering are all interpretations, so **a bare source credit does not
comply**; the displayed notice says the data is modified and interpreted, and
what was done. The other two conditions: no indicating or suggesting that the
City "vous soutient ou endosse votre usage" (explicitly extending to
integrating its data into a database you own), and no restricting access to the
originals "sous la forme de conditions légales ou de mesures techniques".

**13. Société de transport de Montréal — required, and DISPLAYED.** The Métro
geometry is a SEPARATE owner from the business data, though both sit on the
City's portal. The STM dataset's own note:

> "Le présent ensemble de données est la propriété de la Société de transport
> de Montréal. Conséquemment, selon la clause d'attribution de la licence
> Creative Commons 4.0, la paternité des données doit être attribuée à la
> Société de transport de Montréal."

So credit **STM**, not the City, for the lines and stations. Its note confirms
the coverage extends to "les tracés des lignes de bus et de métro", which is
exactly what this project redraws.

**A trap avoided, and it is the New York footer for the third time.** The
City's licence page points at `montreal.ca/articles/mentions-legales-2654`,
which states "L'ensemble des contenus de montreal.ca est la propriété exclusive
de la Ville de Montréal, **tous droits réservés**" and forbids reproducing "les
images du site" commercially. Read alone, that makes Montréal look prohibited.
It is not: applying `read-licence` step 4, that document is written entirely in
**web-page** language (page, site, navigation, hyperlien) and contains **no
data language at all** — no "données ouvertes", "jeu de données",
"redistribuer", "base de données" or "réutiliser" — and its operative sentences
name montreal.ca's own contents and photos. The open data is governed by the
separate licence page above. Same shape as nyc.gov's "All Rights Reserved"
footer and Philadelphia's terms-of-use, and the reason step 4 exists.

**14. City of Calgary — required, and DISPLAYED. One notice covers BOTH the
business data and the transit data**, which no other Canadian city manages:

> `Contains information licensed under the Open Government Licence – City of Calgary.`

En dash, British "Licence" — Surrey's sibling notice uses a hyphen and
"License" and the two are not interchangeable. Like Toronto's, Vancouver's and
Surrey's, this licence **terminates automatically on breach**. The Socrata
`license` field on the business register reads `See Terms of Use`, which is the
`SEE_TERMS_OF_USE` marker `read-licence` step 1 flags: the OGL is the document
it points at, and it is stored in `docs/licenses/calgary-open-government-licence.txt`.

**15. City of Edmonton — required, and DISPLAYED. It was recorded as needing
NOTHING, and that was wrong.** One notice covers both the business register and
ETS's GTFS, as Calgary's does, because the feed is published through the same
Open Data Catalogue.

Edmonton's Terms of Use say credit is "not required" but "encouraged", and both
the Canada profile and `docs/build_briefs/edmonton.md` concluded from that
sentence that Edmonton was the one Canadian city with no display obligation.
**The obligation is in a different clause and it is not about credit:**

> If you distribute or provide access to the datasets to any other person,
> whether in original or modified form, you agree to include a copy of, or this
> Uniform Resource Locator (URL) for, these Terms of Use and to ensure any such
> person agrees to, and is bound by, them **without introducing any further
> restrictions of any kind**.

`outputs/edmonton/` is committed to a public repository and carries the
register's business names, categories and coordinates — that is the dataset in
modified form, so the clause engages. What it requires is **the URL**, which is
now displayed:

> `https://www.edmonton.ca/sites/default/files/public-files/documents/Web-version2.1-OpenDataAgreement.pdf`

The second half, "without introducing any further restrictions", is already
satisfied and was before this was noticed: the repository's own `LICENSE`
disclaims MIT over everything under `outputs/` and points here. That was written
for a different reason and turns out to discharge this clause.

**Two things about reading this licence at all.** The portal's own copy is now
behind a SIGN-IN — `data.edmonton.ca/stories/s/Open-Data-Terms-of-Use/msh4-e6be/`
redirects to a login page, in a browser as well as to `curl`. The readable copy
is the PDF above, and `docs/licenses/edmonton-open-data-terms-of-use.pdf` is a
verified capture of it (SHA-256 in that directory's README, re-checked
2026-09-21). A licence that cannot be read at the URL its dataset points at is
a reason to keep the local copy, not a reason to trust a summary of it.

Unlike Toronto's, Vancouver's, Surrey's and Calgary's, this licence does **not**
terminate automatically on breach — the City may cancel access "at any time for
any reason, in its sole discretion", which is discretionary rather than
automatic. It also bars implying City endorsement or affiliation and bars use of
its marks, which `render_site_notices()`'s standing non-affiliation line covers.

**16. City of Toronto — required, and DISPLAYED. ONE notice covers BOTH the
business register and the TTC's GTFS**, as Calgary's does, because both are City
of Toronto CKAN resources under the same licence:

> `Contains information licensed under the Open Government Licence – Toronto.`

En dash, British "Licence". Like Vancouver's, Surrey's and Calgary's, this
licence **terminates automatically on breach**. Both datasets declare "License
not specified" at dataset level, which is why the licence text was captured from
`open.toronto.ca/open-data-licence/` and stored at
`docs/licenses/toronto-open-government-licence.txt` rather than read from a
field.

**The counts that used to sit here are gone, and their going is the point.**
This paragraph asserted "fourteen cities" and "thirteen sources" and was wrong
on both by the time anyone read it — two cities and three notices had been
added without it being touched, and the sentence disagreed with itself
("thirteen sources", then "six of the twelve"). A hand-maintained tally beside
a hand-maintained list drifts, silently, in the one section that gates a public
deploy. `scripts/check_provenance.py` now asserts the relationship instead:
every entry in `app/components.py`'s `_NOTICES` has a numbered item here, every
numbered item has an entry there, and the numbers are unique and contiguous.
Run it rather than counting.

What does not drift is the shape, and it is worth stating for the next country:

- **The US sources mostly prescribed no wording; the Canadian ones almost all
  prescribe their own.** Budget a notice per SOURCE, not per city.
- **Vancouver added three at once** — the first city to add more than one —
  because it is regional across two municipalities and each Open Government
  Licence prescribes its own sentence. It later added a fourth, the Province's.
- **Montréal added two**, because its business data and its transit data have
  different owners; and Montréal's is the first attribution here that has to
  describe what this project **did to** the data rather than merely name its
  source. INEGI's and CRTM's are the same family.
- **A notice can come from a publisher that is not a city at all.** The
  Province of British Columbia (item 17) is the first, and it arrived through
  the naming layer rather than through any of the three provenance tables —
  which is why the check looks at sources, not at cities.

**17. Province of British Columbia — required, and DISPLAYED since 2026-09-22.
It is the first PROVINCIAL or STATE publisher in this project**, and neither
Vancouver's nor Surrey's municipal licence reaches it:

> `Contains information licensed under the Open Government Licence – British Columbia.`

En dash, British "Licence" — the third notice in this list with that exact
shape, after Vancouver's and Calgary's, and still not interchangeable with
Surrey's hyphen-and-"License". Like the four municipal OGLs it **terminates
automatically on breach**. Read 2026-09-22 and stored at
`docs/licenses/bc-open-government-licence.txt` (version 2.0, last updated
2025-04-11).

**What engages it:** the BC ABMS municipalities layer, read over WFS from
`openmaps.gov.bc.ca`, is what NAMES the 30 SkyTrain stations lying outside
Vancouver and Surrey. `outputs/vancouver/excluded_stations.csv` is committed to
a public repository and carries those names, so the Information is distributed
and the attribution clause engages — the same reasoning that turned Edmonton
from "no obligation" into item 15.

**Why it was missed for a day.** It is not a business registry, not a transit
feed and not the city boundary: it is the **naming layer**, a fourth kind of
input that no per-city checklist had a slot for. D.C.'s Census TIGERweb states
layer is the same role and needed no notice only because US federal works carry
no copyright — so this project had met the category once and drawn exactly the
wrong lesson from it. `scripts/check_provenance.py` now fails when any source
in the three provenance tables has no licence position recorded, which is the
check that would have caught it on the day.

**Two pointers were followed and both mattered.** The licence page opens "as
per B.C. Government Copyright, the following licence only applies to records in
the B.C. Data Catalogue that specify it" — so the catalogue record is the
authority, and it declares OGL-BC. And the page links a **second** document,
"API Terms of Use for OGL Information", which applies here because this project
reads a WFS rather than downloading a file. Read 2026-09-22: it adds
operational conditions (limits "without notice", credentials revocable if
misused, terms changeable without notice, automatic termination) and **no new
notice**. That is TransLink's two-documents shape with the opposite answer —
TransLink's two documents mandate *different legends*, BC's second mandates
none.

**A near miss worth recording.** Three BC layers carry near-identical names and
**two are licensed "Access Only"**, which does not permit redistribution:
`tantalis-municipalities` and `legally-defined-administrative-areas-of-bc`.
Only `municipalities-legally-defined-administrative-areas-of-bc` is OGL-BC. The
build is on the right one — confirmed not by its name but because that
package's own metadata names the exact `openmaps.gov.bc.ca/geo/pub/…
ABMS_MUNICIPALITIES_SP/ows` endpoint the config calls, and because TANTALIS
describes itself as superseded: "[Replacement Dataset: ABMS_MUNICIPALITIES_SP]".
Calgary's two-boundary trap, with a licence consequence instead of a geometry
one.

**18. Seoul Metropolitan Government — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** Displayed since the Seoul build (2026-09-25), wording
approved by the owner: it names the institution, the year, the licence type (linked to
`kogl.or.kr`) and the sixteen dataset titles used, links Seoul Open Data Plaza, describes
the changes, and says the categories and counts are this project's own and that Seoul
does not sponsor or endorse the map. **MUST DO:** `check_personal_exposure.py seoul`,
run 2026-09-25 (the verdict is in `DECISIONS.md`).

Read 2026-09-22 and recorded here so the cost was known
before the build rather than discovered during it. All eight `인허가 정보`
datasets are **공공누리 제1유형 (KOGL Type 1)**, and it is a **one-notice
country on current evidence** — every dataset carries the same licence, the
same 저작권자 and `제3저작권자: 없음`, so one notice covers the whole city
however many business types it ends up using. The Korean pattern is therefore
the US one, not the Canadian one.

Three things it will require, from `kogl.or.kr`'s own text rather than the
label on the dataset page:

- **Attribution naming institution, year, KOGL type and dataset title — with a
  hyperlink.** KOGL says a link *must* be provided where providing one is
  possible online, which it is here. This is ODbL-shaped, so
  `render_site_notices()` is the right home and a bare source string will not
  discharge it.
- **A non-affiliation line.** Already covered by the standing one that
  `render_site_notices()` emits for Edmonton and Toronto — no new text needed.
- **A statement that the per-station counts are this project's derivation, not
  Seoul's published figures.** KOGL's moral-rights clause names misleading
  modification of statistics specifically. This is the **third** source to
  impose a describe-what-you-did-to-the-data duty, after INEGI and Montréal,
  which is now enough of a pattern to expect it rather than be surprised:
  budget it for any national statistical or licensing register.

Nothing was displayed for this until Seoul was built — displaying a notice for
data the site did not carry would itself have been misleading.

**19. Ayuntamiento de Madrid — required, and DISPLAYED.** The Censo de locales
declares CC BY 4.0, which the *Condiciones generales de reutilización* then
extend by conduct rather than by agreement: *"la mera obtención o el uso de los
documentos sometidos a estas condiciones supone la aceptación"*. Two of those
conditions bear on what is shown, and neither is satisfied by a bare credit:

> **Source and date.** *"Se deberá citar como fuente al Ayuntamiento de
> Madrid"*, together with *"la fecha de la última actualización"* of the
> documents reused.
>
> **Non-distortion.** *"No se desnaturalice el sentido de la información"*, and
> the reuser must not suggest the Ayuntamiento participates in or endorses the
> reuse.

The displayed text therefore names the Ayuntamiento, carries the census date,
states that the ring density, storefront filtering and three-category grouping
are this project's work rather than the city's, and disclaims endorsement.

**20. CRTM (Consorcio Regional de Transportes de Madrid) — required, and
DISPLAYED.** Its *licencia de uso* prescribes the wording, and this is the only
notice in the project whose exact string the publisher dictates:

> **"Powered by CRTM - www.crtm.es"**

Two further conditions travel with it. The reuser must disclose whether the
data is shown *en bruto* or *explotados* — raw or worked — and this project's
is emphatically the latter, so the notice says so. And CRTM's *"siempre
actualizada"* clause requires the displayed data to carry its update date; that
clause was raised as an owner decision and resolved on 2026-09-22 (see above)
as a misrepresentation rule rather than a liveness requirement, discharged by
naming CRTM's own last-update date beside the map.

**21. Ajuntament de Barcelona — required, and DISPLAYED.** The Cens de locals
declares CC BY 4.0, and the Open Data BCN *terms of use* — incorporated by the
legal notice, and read from the Internet Archive because the live pages serve
hCaptcha — prescribe the wording:

> **"Source of the data: Barcelona City Council"**

and require, separately, that **modifications be identified at the point of
distribution**: *"Any amendment or change made to the data sets … shall be
identified as such at the time of their distribution."* That is the
disclosure-of-transformation family for the fourth time, after Montréal, INEGI
and Madrid, and a source credit alone does not discharge it — so the displayed
text names the survey year, states that the vacancy filter, storefront
filtering, three-category grouping and ring measurement are this project's
work, and disclaims endorsement.

⚠️ **A fourth obligation is NOT a notice and is not discharged by this page.**
The same terms require the reuser to *inform Barcelona City Council of every
project* derived from the data — an affirmative act owed to the publisher
rather than text on a page, and the first of its kind in this project. The
clause's own tail gives its purpose: *"so that they are open to the public for
the purpose of encouraging policies for reusing information from the public
sector"*, which makes it a reuse-showcase notification rather than a permission
gate. **It is an owner action, outstanding**; the draft is at
`docs/notifications/barcelona-city-council.md`.

**The displayed notice now reports that act's status**, added 2026-09-22 on the
owner's call: *"That notification is written and not yet delivered: on 22
September 2026 the portal's own contact form stalled, and the enquiry channel
the terms themselves name did not respond. It will be sent when that service is
reachable again."* It is worded as a **status report and never as though it
performed the act** — text on this project's own page is precisely what does
not discharge a duty owed to the publisher, and a sentence that blurred the two
would be worse than no sentence. When the notification is sent, that wording
and the attempt log in the notifications file change together.

**The live terms were read on 2026-09-22** — by the owner, in a browser, past
the hCaptcha — which closes the precondition this file had carried since the
licence review and which Barcelona was published without. Stored at
`licenses/barcelona-condicions-us-live.txt`. Three things changed, none of them
adverse:

- **The notification clause is unchanged, word for word**, so the obligation is
  current and not an artefact of an eighteen-month-old snapshot.
- **The terms name the channel**, which no earlier reading had established:
  *"Any doubts or comments on these Terms of use may be forwarded to the
  following link"* → `bcn.cat/cgi-bin/consultesIRIS?id=241`, which redirects
  to the Council's online enquiry service pre-categorised to city data
  (`atencioenlinia.ajuntament.barcelona.cat`, `origen=DADES_CIUTAT`). **That
  settles a question this project could not answer**: the portal publishes no
  contact email — the dataset's CKAN metadata carries no `maintainer_email` or
  `author_email`, `datos.gob.es` names a web form and no address, and the
  portal's own contact page is behind the same CAPTCHA — so any email address
  would have been invented.
- **A CC BY-ND clause exists and does not apply.** *"any data involving
  third-party participation may be reused under a Creative Commons
  Attribution-NoDerivs (CC BY-ND 4.0) licence"*. ND would forbid this project
  outright, every map being a derivative. It does not bind, because *"Every
  data set that is offered in the Open Data BCN service states its relevant
  Terms of use"* and the Cens de locals declares `CC-BY-4.0` in its own CKAN
  metadata — verified live through `package_show` on 2026-09-22, an endpoint
  that needs no CAPTCHA. Recorded because a clause that would have sunk the
  city deserves to be on the record as checked, not as unnoticed.

⚠️ **Article 8's "content may not be altered" is a DISCLOSED POSITION, not a
resolved one.** The terms import Spanish Act 37/2007 Article 8 — *"the content
of the information may not be altered"*, *"the meaning of the information may
not be distorted"* — and this project filters 10,722 premises rows to three
categories and derives ring density from them. Read literally, that is
alteration. Read in context, the same document permits data *"to provide the
basis for derived works as a result of their analysis or study"*, permits it
*"to be amended, changed and adapted"*, and requires that *"Any amendment or
change … shall be identified as such at the time of their distribution"* — a
requirement that is incoherent if amendment were forbidden. Article 8 is
standard Spanish PSI wording and reads as barring misrepresentation rather than
analysis.

**Owner's decision 2026-09-22: publish on the second reading, stated openly**,
which is Philadelphia's shape. Every transformation is disclosed on the city
page and itemised in the notification, which is what the identify-amendments
clause asks for. The rejected alternatives were asking the Council to confirm
it — inviting a "no" to a question nobody had asked — and holding a finished
city indefinitely on a body under no obligation to reply. **If the Council
reads it the other way, Barcelona comes down**: the standing removal commitment
below covers this without needing to be invoked.

**22. Tailte Éireann — required, and DISPLAYED.** Written at Step 0 so the
obligation existed before the city did, and wired into
`app/components.py`'s `_NOTICES` when Dublin was published on 2026-09-22. The valuation register declares `CC-BY-4.0` on `data.gov.ie`
(`package_show`, verified 2026-09-22), and the licence is Circular 12/2016
Annex 1, which Tailte's own open-data page links. Four obligations converge and
one paragraph discharges all four — the PSI attribution string, Tailte's own
requirement to be named as content creator, **CC BY 4.0 §3(a)(1)'s duty to
indicate modification**, and non-endorsement:

> Contains Irish Public Sector Information licensed under a Creative Commons
> Attribution 4.0 International (CC BY 4.0) licence. Source: Tailte Éireann
> valuation data, via the Tailte Éireann Valuation open API. This map filters,
> re-categorises and aggregates that data into density measures; the filtering,
> categories and densities are this project's own interpretation and are not
> produced or endorsed by Tailte Éireann. The data is published "as is"; Tailte
> Éireann gives no warranty as to its accuracy, completeness or currency.

That is the **disclosure-of-transformation family for the fifth time**, after
Montréal, INEGI, Madrid and Barcelona — a bare source credit does not discharge
it.

⚠️ **Three different attribution strings are live on Irish government sites**,
differing in one word: Circular 12/2016 says *"Irish Public Sector
Information"*, `data.gov.ie/license` says *"Irish Public Sector Data"*, and
`data.gov.ie/technical-framework` says *"Irish Government Data"*. No document
ranks them. The wording above follows the **Circular**, because it is the
instrument Tailte's own page points to and the only one of the three that is a
licence rather than guidance. **Recorded as a disclosed position**, not as a
settled fact.

**Nothing must be DONE.** No registration, notification, permission request or
statistics return is owed — swept for the full affirmative-obligation phrase
set across every document read, with zero hits. **This is explicitly the
opposite of Barcelona's finding** and is recorded positively so it is not
re-opened. Channels exist anyway for corrections:
`opendataofficer@tailte.ie` and `opendata@tailte.ie`, both live, neither
CAPTCHA-walled.

**What must NOT be said**: nothing implying official status or Tailte
endorsement; **no claim the data is accurate, complete or current** (Tailte
disclaims all three, and `tailte.ie/home/api/` states the API "is not
guaranteed to be complete") — the MTA/WMATA prose rule again; and no Tailte
logo, crest or official symbol, which the PSI licence excludes and CC BY 4.0
§2(b) does not license.

✅ **The `Eircode` column is DROPPED — owner's call, 2026-09-22.** The Eircode
database is third-party IP (An Post / OSi via GeoDirectory, licensed through
Capita), and both the PSI licence and `data.gov.ie/license` carve out
third-party database rights the Information Provider is not authorised to
license. Tailte publishes Eircodes inside a dataset it declares CC BY 4.0,
which is an argument that it holds the right to; republishing ~38,000 of them
is a substantial extraction from a database whose *sui generis* right belongs
to someone else, which is an argument that it does not.

**The decision does not resolve that — it removes it.** The build has
`Xitm`/`Yitm` and five address lines and never reads `Eircode`, so dropping the
column costs the map nothing and leaves the source with no third-party-rights
exposure at all. The rejected alternative was publishing on the permissive
reading with the position disclosed, which is what Philadelphia and Barcelona
do — declined because **those two had no cheaper option and this one does.**
Step 2 must drop it at load so it never reaches a processed file.

One page that reads alarmingly and does not apply:
`tailte.ie/map-shop/map-licences-and-copyright/` requires "prior permission"
for reproducing Tailte **surveying** material. It mentions valuation, open
data, API, Eircode, PSI and Creative Commons **zero times each** and governs
the paid Map Shop products. Read and inapplicable — recorded so the next
reader does not re-establish it.

**23. Comune di Milano — required, and DISPLAYED.**

This took the wrong number for an hour. The Tailte Éireann item immediately
above had already reached master with Dublin's *brief* commit, which is
docs-only, while Dublin's build sat on a branch — so the next free number read
one lower than it was. `check_provenance.py` caught the duplicate within the
same session, then caught the stale citation left behind by fixing it. It is
the check that once found two item 8s and two item 15s, and this is the third
time it has earned its place. Recorded at build time so the obligation exists
before the city is live; **this item is a deploy blocker for Milan
specifically**, not an outstanding defect on the cities now published. All six
premises registers and all three ATM rail layers declare **CC BY 4.0**.

⚠️ **The version is invisible where anyone would look.** CKAN's `package_show`
reports `license_id: cc-by` with **no version at all**, and its `license_url`
points at opendefinition's version-less register entry. Three independent
sources give 4.0: the portal's **DCAT-AP_IT** serialisation
(`owl:versionInfo "4.0"`), the portal footer, and the national catalogue
`dati.gov.it`. `scripts/brief_check.py` gained an `http_contains` kind for
exactly this, and Milan's brief pins its licence claim to the `.ttl` rather
than to `package_show` — a check that cannot see the thing it guards is the
failure shape this project keeps writing scripts against.

**No wording is prescribed**, so CC BY 4.0 §3(a)(2) applies ("any reasonable
manner"). The components are still mandatory, and one of them is work:

> Contains data from the Comune di Milano, licensed under a Creative Commons
> Attribution 4.0 International (CC BY 4.0) licence. This map filters,
> re-categorises and aggregates that data into density measures; the
> filtering, categories and densities are this project's own and are not
> produced or endorsed by the Comune di Milano.

That discharges attribution, **CC BY 4.0 §3(a)(1)'s duty to indicate
modification** — the disclosure-of-transformation family for the **sixth**
time, after Montréal, INEGI, Madrid, Barcelona and Tailte Éireann — and the
§2(a)(5)(C) non-endorsement clause. Note it is the *weaker* form of the
disclosure duty: CC BY 4.0 requires disclosing **modification** and says
nothing about interpretation, where Montréal's licence names both.

**MUST DO: nothing.** The Italian trigger phrases (`informare`, `comunicare
al`, `registraz`, `previa autorizzazione`, `obbligo di`) return **zero** across
the dataset pages and the portal's `/about`. A channel exists if the project
ever wants to notify voluntarily: `opendatamilano@comune.milano.it`, consistent
across three sources.

⚠️ **Do not generalise this licence to the portal.** Neighbouring datasets in
the same searches carry `other-at` and `cc-zero`; any further Milan dataset
needs its own `package_show`. Two decoys, both real and both about something
else: the portal footer's `CC-BY 3.0` link is attribution the portal owes
**upstream** for its theme icons, and `comune.milano.it`'s *Note Legali*
licenses **the institutional website** under CC BY 3.0 IT — that page names
*"il sito ufficiale"* and self-defers with *"salvo dove è diversamente
specificato"*.

**Prudential, not an obligation:** the publisher's own description warns the
register is not internally consistent — *"le informazioni contenute nel dataset
non sono necessariamente omogenee, perché riferite al momento dell'ultima
comunicazione"*. Nothing forbids calling the data current; the publisher's own
statement makes it unwise.

**24. Île-de-France Mobilités — required, and DISPLAYED.**

Recorded at scaffold time so the obligation existed before the city did, then
**missed anyway**: the map rendered, the gate was run, and the notice was still
absent from every page. A verification pass on 2026-09-23 found
`verbatimIDFMNotice: false` on `/Paris_Heatmap` with 21 sources in the notices
block and not one of them French. Added to `app/components.py`'s `_NOTICES` the
same day.

⚠️ **Nothing automated caught it, and that is the more useful finding.**
`check_provenance.py` checks these notices in bijection with `_NOTICES` and
prints `notices: 24 numbered, 21 displayed` — as a line of output, passing
regardless. A required notice that is documented, numbered, called a deploy
blocker in this very entry, and simply not rendered is exactly the gap this
file's own reasoning says a script should close rather than a paragraph.

**This is the first notice here whose licence is not a standard public one.**
`mobility-licence` covers exactly **2 of 799** NAP datasets, there is no
government-hosted text, and the authoritative document is a 14-page PDF behind
a community wiki. It is ODbL-*derived* but **not ODbL-compatible**, so nothing
in the OpenStreetMap posture transfers to it. Art. 3.1 grants worldwide, free,
commercial use including **« l'affichage public »** — redrawing is permitted.

**MUST DISPLAY**, verbatim:

> Contient des informations de Réseaux urbains et interurbains d'Île-de-France
> Mobilités (IDFM), présentement mises à disposition aux conditions de la
> « Licence Mobilités »

⚠️ **Art. 5.4(a) prescribes the LINKING as well as the words** — the database
name must hyperlink to the dataset URI, and « Licence Mobilités » to the
licence text. No other notice in this file constrains markup, so
`render_site_notices()` cannot carry this one as plain text the way it carries
LA Metro's.

⚠️ **Two obligation shapes this project has never carried**, both from Art. 5.7,
which forbids use misleading « quant … à sa date de mise à jour »: the **date
the data was last updated**, and its **update interval**. A pre-rendered static
map built from a frozen snapshot is exactly that unless the snapshot date is
shown. This is where the missing `feed_info.txt` becomes a compliance problem
rather than a curiosity — **neither value exists inside the artifact**, so both
must be captured at fetch time or they cannot be displayed honestly.

**MUST DO**, three things, none of them a permission gate:

- **Report source errors** to `contact-prim@iledefrance-mobilites.fr` « sans
  délai ». A data-quality duty.
- **Supply modifications to recipients** (Art. 5.8). A public repository
  carrying the pipeline code and the derived CSVs, linked from the site,
  satisfies it — which this project already does for every other city.
- **Republish the derived station table on the NAP** as a *ressource
  communautaire* (Art. 5.6(b)). Arguably not owed: that article says a rendered
  map is a *Création Produite* rather than a Derivative Database, and the NAP's
  own published example — *"Calcul de la distance à l'arrêt de bus le plus
  proche pour une liste de commerces"*, which is close to this project's exact
  shape — is filed under **"Non"**. But this project commits `outputs/<city>/`,
  so the derived table is published either way and **one upload moots the
  argument** rather than requiring it to be won.

**MUST NOT:** Art. 5.7's duty is the *inverse* of MTA's and WMATA's. Where those
forbid claiming accuracy, this one requires currency and
« l'**exhaustivité** des données disponibles », with a relevance proviso that
covers deliberate exclusions. **So the page should state what was excluded
rather than leave it implicit** — commuter rail, tram, and the 77 out-of-commune
métro stations.

⚠️ **REVOCABLE.** Art. 11.1 terminates *de plein droit, sans préavis* on
breach. Unlike Licence Ouverte this is a revocable grant, and the owner
accepted it on 2026-09-22 with the response decided in advance — see the
removal-commitment section above, where the archive-not-delete posture is
recorded.

⚠️ **IDFM's own licences page contradicts the NAP**, saying its *tracés du
réseau ferré* are Licence **Ouverte**, reserving Licence Mobilités for
timetables this project does not publish. **The stricter reading was adopted
deliberately.** If the looser one were ever relied on, this entire item is
replaced by an Etalab attribution — which is a reason to keep the contradiction
recorded rather than resolve it silently in the project's favour.

**25. Tisséo (Toulouse) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on France's National Access Point. The full
reading is at `docs/licenses/odbl-toulouse-rennes.md`, which also governs
Rennes — hence the filename covering both.

**MUST DISPLAY**, verbatim. This is ODbL §4.3's own notice template with the
database named, so the wording is the licence's rather than this project's:

> Contains information from Réseau urbain Tisséo, which is made available
> here under the Open Database License (ODbL).

⚠️ **The OpenStreetMap notice at item 1 does NOT discharge this**, and that is
worth stating because the opposite is the natural assumption. Both sources are
ODbL, so one credit looks like it ought to cover both — but §4.3 requires the
notice to name *which* database, and "© OpenStreetMap contributors" names
OSM's. **Two ODbL sources need two notices.**

**MUST DO — §4.6.** Offer the Derivative Database, or the method. The public
repository carries the pipeline code and the derived CSVs and satisfies it,
**provided it stays linked from the site** — the same standing condition
IDFM's Art. 5.8 already imposes at item 24, so nothing new is owed as an act.

**✅ The publisher's own CGU adds nothing harmful.** Read 2026-09-23 at
`data.toulouse-metropole.fr/terms/terms-and-conditions/`:

- **No indemnity clause**, unlike Grand Lyon's CGU 9.4.
- **The marks clause is Opendatasoft's own**, and it expressly excludes
  « les données publiées sur le DOMAINE ». ✅ So naming *Tisséo* on the map is
  not barred — which was the specific risk here, since Grand Lyon's equivalent
  clause is the reason Lyon is deferred rather than built.
- The express extraction bar applies only « en dehors d'une LICENCE
  consentie », and this project is inside one.

⚠️ **OPEN — the station CSV under §4.4.** Whether the derived station table and
`outputs/toulouse/excluded_stations.csv` are themselves a Derivative Database
that must carry the notice is unresolved, and unlike Paris there is **no
publisher gloss** to lean on. **Cheap discharge: put the ODbL notice on the
station CSV** rather than try to win the argument.

**26. STAR (Rennes) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on France's National Access Point, read in
`docs/licenses/odbl-toulouse-rennes.md` alongside Tisséo's.

**MUST DISPLAY**, verbatim - ODbL §4.3's own notice template with the database
named:

> Contains information from Réseau urbain STAR, which is made available
> here under the Open Database License (ODbL).

⚠️ **Neither the OpenStreetMap notice (1) nor Tisséo's (25) discharges this.**
Three ODbL sources now, and §4.3 asks each notice to name its own database.

**MUST DO — §4.6**, as for Tisséo: the linked public repository offers the
method, and satisfies it while it stays linked.

**✅ The publisher's CGU adds nothing harmful**, read 2026-09-23 at
`data.explore.star.fr/terms/terms-and-conditions/` - the same Opendatasoft
template as Toulouse Métropole's: no indemnity, and a marks clause that is
Opendatasoft's own with « les données publiées sur le DOMAINE » excluded, so
naming *STAR* on the map is not barred. Watched by the brief check
`star-cgu-still-clean`.

⚠️ **OPEN — the station CSV under §4.4**, exactly as for Tisséo:
`outputs/rennes/excluded_stations.csv` is left in the same state as Toulouse's,
and the same cheap discharge is available if the question is ever pressed.

**27. Brønnøysundregistrene (Oslo) — required, and DISPLAYED.**

**NLOD 2.0**, declared in the Enhetsregisteret API documentation's header
("License: Norsk lisens for offentlige data (NLOD)"). §5: *"The licensee shall
attribute the licensor as specified by the licensor and include a reference to
this licence."* Brønnøysund specifies nothing further (read 2026-09-24), so the
notice is §5's own default sentence, verbatim:

> Contains data under the Norwegian licence for Open Government data (NLOD)
> distributed by Brønnøysundregistrene

with the licence linked, and §5's second duty - *"If the information has been
changed, the licensee must clearly indicate that changes have been made by the
licensee"* - met in the notice's next sentence. **MUST DO: nothing.**

**28. Kartverket (Oslo) — required, and DISPLAYED.**

**CC BY 4.0**, for both Kartverket datasets Oslo reads - the address register
(the coordinate join) and the kommune boundaries (scope and naming). Kartverket's
terms, which expressly cover its APIs, prescribe **`© Kartverket`** and a link;
CC BY 4.0 §3(a) adds the licence link and a statement of modification. One line
covers both, since licensor and licence are the same. The boundaries'
municipality names come from SSR, whose rule asks for *"SSR ©Kartverket"* -
one name on twelve rows is probably not "systematic use", but the line costs
nothing, so it is included rather than argued. ⚠️ The API's own 2019 service
record says "no conditions apply"; the dataset record and the terms page say
CC BY 4.0, and the stricter reading governs.

**29. Entur (Oslo) — required, and DISPLAYED, with its logo.**

**NLOD 2.0**: *"Data provided by Entur AS from API or published data files can be
used under the Norwegian Licence for Open Government Data (NLOD)"*
(developer.entur.org). **Entur SPECIFIES its credit**: *"Entur should be credited
as the source with the text: Data made available by Entur + (logo)"*. The new
developer portal says only "License: NLOD" and neither repeats nor withdraws the
logo, so it is treated as owed while the old page is live (**owner's call
2026-09-24**): Entur's own unaltered primary logo,
`app/assets/entur/Enturlogo_Blue_RGB.svg` (SHA-256
`0fece3cb112ed0d82ef0aea473b2528ee7821d19e57864702fa19c7f6cf8f0ea`, from
`Entur_logo_RGB.zip` at `cdn.sanity.io`, linked from
`linje.entur.no/identitet/verktoykassen/logo/`), shown beside the credit on the
Oslo page, on a white chip and at least 20 px as Entur's rules require. The
changes (lines selected, limited to Oslo kommune, redrawn; colours not from
this data) are stated in the notice. **MUST NOT**: use Entur's, Ruter's or
Sporveien's names to endorse anything (NLOD §6), or present the data
misleadingly. **MUST DO: nothing** - no key for the static file, and Entur asks
for no more than one download a day.

**30. Det Centrale Virksomhedsregister (Copenhagen) — required, and DISPLAYED.**

**CC BY 4.0**, from CVR's own terms on Datafordeler
(`datafordeler.dk/vejledning/brugervilkaar/det-centrale-virksomhedsregister-cvr/`,
read 2026-09-23): *"Du skal kreditere Det Centrale Virksomhedsregister (CVR) på
et passende sted."* The name is prescribed and the wording is not, so the
notice is this project's own, approved by the owner 2026-09-24; its second
sentence is CC BY 4.0 3(a)(1)'s duty to indicate modification. Only the entity
`CVRPerson` is access-restricted and this project never asks for it. **MUST
DO: nothing** - no notification, no registration of the reuse. The account is
the owner's and closes after Copenhagen publishes (`docs/gated_access.md` item
3); closing is licence-safe, since the grant attaches to the data.

**31. Klimadatastyrelsen (Copenhagen) — required, and DISPLAYED.**

**CC BY 4.0**, from DAR's terms on Datafordeler
(`datafordeler.dk/vejledning/brugervilkaar/danmarks-adresseregister-dar/`,
"Vilkår for brug af Danmarks Adresseregister (DAR) - (16.05.2024)", read
2026-09-24 by the `licence-read` agent): free to fetch, share and adapt, with
credit to **Klimadatastyrelsen**. Klimadatastyrelsen's own terms page lets the
reuser choose the form of the credit; the notice names the register as well,
because Datafordeler's general terms ask for "the responsible register". The
2022 SDFI terms PDF still linked from Dataforsyningen's product cards
prescribed a dated credit sentence and is SUPERSEDED for data fetched after 16
May 2024 - not to be followed. **MUST DO: nothing.**

**32. Czech Statistical Office (Prague) — required, and DISPLAYED.**

**CC BY 4.0**, from ČSÚ's own conditions page
(`csu.gov.cz/podminky_pro_vyuzivani_a_dalsi_zverejnovani_statistickych_udaju_csu`,
read 2026-09-23 and re-confirmed 2026-09-24). ⚠️ **The CC BY sentence governs
the WEB PAGES; the data conditions follow it under "Další podmínky použití dat
ČSÚ"**, and they impose two duties this build triggers: *"v případě šíření dat
ČSÚ vzniká povinnost uvést podmínky této licence, nejlépe přímým odkazem"* -
state the conditions, preferably by a direct link, which the notice does - and
modified or derived data must be marked as such and not presented as unchanged
official statistics, which its second sentence does. **MUST NOT SAY**: that the
map is official Czech statistics. Wording approved by the owner 2026-09-24.
**MUST DO: nothing.**

**33. ČÚZK (Prague) — required, and DISPLAYED.**

**CC BY 4.0**, from ČÚZK's spatial-data conditions
(`www.cuzk.gov.cz/Predpisy/Podminky-poskytovani-prostor-dat-a-sitovych-sluzeb/Podminky-poskytovani-prostorovych-dat-CUZK.aspx`,
updated 30.06.2023, read 2026-09-23), whose first bullet names RUIAN's exchange
format. **The credit FORMAT is prescribed**: *"ČÚZK, [rok]"* - the file's year,
so **ČÚZK, 2026** - plus a link to the conditions and a description of the
modification, all three in the notice. ⚠️ The English page (v1.0, 2016)
prescribes a different string and never mentions CC BY; the Czech one
governs. ⚠️ The ATOM feed's own `<rights>žádné podmínky neplatí</rights>` is
INSPIRE boilerplate and is NOT relied on. Wording approved by the owner
2026-09-24. **MUST DO: nothing.**

**34. ROPID (Prague) — required, and DISPLAYED.**

**CC BY**, from PID's open-data page (`pid.cz/o-systemu/opendata/`, read
2026-09-24): *"Data, která lze stáhnout přímo zde z webu, jsou ... opatřena
licencí CC-BY, tedy je lze dále šířit, avšak je nutné uvést autora a případné
provedené změny"* - name the author (ROPID) and the changes, which the notice
lists (lines selected and redrawn, stations reduced to points, Flora added
while closed, line A lightened). **MUST NOT**: the PID, ROPID and IDSK logos
(*"je nutný vždy souhlas organizace ROPID"*), or any implied endorsement.
Wording approved by the owner 2026-09-24. **MUST DO: nothing** -
`opendata@pid.cz`'s invitation to write is not a condition.

**35. Gemeente Amsterdam (Amsterdam) — required, and DISPLAYED.**

The hospitality-permit register's licence is **SILENT** - `Licentie: -` on the
live dataset, no `license` key in its schema, and a retired 2022 catalogue that
said CC BY (read 2026-09-24). **Displayed as CC BY 4.0 on the owner's choice of
2026-09-24**, which satisfies both readings: it credits the Gemeente, links the
licence and states the changes (filtered to restaurants, cafés, takeaways,
coffeeshops and nightclubs, grouped into one category, matched to the BAG by
address, mapped by distance to stops). **MUST NOT SAY**: that the map is the
official permit record, or that the Gemeente produced or endorses it. The BAG
(Public Domain Mark) and GVB's data (CC0) require no notice. Wording approved by
the owner 2026-09-24. **MUST DO: nothing** - the city's API is to require a key
on an unset date, and registering is the owner's act.

**36. Roma Capitale (Rome) — required, and DISPLAYED.**

**CC BY 4.0**, from the portal's *Licenze* page and the resource's own
`license_type` `A21_CCBY40` (read 2026-09-24): credit Roma Capitale, link the
licence, state the modification. The notice names the changes - filtered to
shops, food and drink and personal services, sorted into three categories,
placed at house-number level, mapped by distance to stations. **MUST NOT SAY**:
that Roma Capitale produced or endorses the map. Wording approved by the owner
2026-09-24. **MUST DO: nothing.**

**37. ANNCSU (Rome) — required, and DISPLAYED.**

**CC BY 4.0**, on dati.gov.it (read 2026-09-24; the EU high-value-datasets
regulation requires CC BY 4.0 or looser for addresses): credit the Agenzia delle
Entrate and ISTAT, link the licence, and say what the coordinates are used for -
placing another register's premises. Wording approved by the owner 2026-09-24.
**MUST DO: nothing.**

**38. IBGE (Brazil) — required, and DISPLAYED.**

**Free use by federal law** (Decree 8.777/2016 art. 4, Lei 14.129/2021 art. 29),
*"limitando-se a creditar a autoria ou a fonte"*; no IBGE licence document
exists and no wording is prescribed (read 2026-09-23, the Brazil section above).
One notice covers all nine Brazilian cities. It carries IBGE's own citation form
(`Fonte: IBGE, Cadastro Nacional de Endereços para Fins Estatísticos (CNEFE),
Censo Demográfico 2022.`) and names the changes - descriptions sorted into three
categories, unreadable ones left out, only the category at an address that is
also a home, the rest mapped by distance to stations. **MUST NOT SAY**: that the
categories are IBGE's, that the names were verified, or that IBGE produced or
endorses the map. Wording approved by the owner 2026-09-24 with São Paulo's
page. **MUST DO: nothing.**

**39. IPP / DATA.RIO (Rio) — required, and DISPLAYED.**

**CC BY 4.0**, declared at service level on the IPP's `Transporte_publico`
MapServer and on all four Data.Rio rail items (read 2026-09-23): credit
*"Prefeitura da Cidade do Rio de Janeiro / Instituto Pereira Passos (IPP)"*,
link the licence and the data, and **state that the data was modified** - CC BY
4.0 §3(a)(1)(B), required rather than optional. Covers the metro stations and
lines (layers 19 and 18) only; the VLT and SuperVia are OpenStreetMap's, under
notice 1. The SIURB terms' liability clause was accepted by the owner
2026-09-23. Wording approved by the owner 2026-09-24. **MUST DO: nothing.**

**40. CBS (Rotterdam) — required, and DISPLAYED.**

**CC BY 4.0** (`cbs.nl/nl-nl/over-ons/website/copyright`, read 2026-09-24): credit
CBS, link the licence, and say when a figure is recalculated. Rotterdam's page
quotes the shop-vacancy share from the Landelijke Monitor Leegstand 2025, table 1
(430 of 6,060 shop units, 1 January 2025), as "about one in fourteen" - a rounding
of CBS's counts, which the notice says. **MUST NOT SAY**: that CBS produced or
endorses the map; no CBS logo. KOOP's notices (Auteurswet art. 11, CC0 declared),
the BAG (Public Domain Mark) and the national feed (CC0) need no notice. Wording
approved by the owner 2026-09-24. **MUST DO: nothing.**

**41. FEHD / DATA.GOV.HK / CSDI (Hong Kong) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** The registers under DATA.GOV.HK's Terms of Use v1.2 (read
2026-09-22), FEHD's points under the CSDI Portal's terms (read 2026-09-24): identify the
source, acknowledge the Government's and FEHD's intellectual property, attribute the
Government, FEHD and DATA.GOV.HK, and name the CSDI Portal as a source - one paragraph. Both
carry the uncapped indemnity the owner accepted (see "Hong Kong's indemnity"). Wording
approved by the owner 2026-09-24. **MUST DO:** `check_personal_exposure.py hong_kong`, run
2026-09-24 (the verdict is in `DECISIONS.md`). MTR's station lists (gate 3) and ALS (a
cross-check) are not published and need no notice.

**42. VZD (Riga) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** CC BY 4.0, adopted by VZD's own data-use rules
(`vzd.gov.lv/lv/par-datu-izmantosanas-noteikumiem`, read 2026-09-24 by the licence-read
agent): credit the source, link the licence, and describe the changes made - VZD asks
for the changes, not a bare "modified". **MUST NOT SAY** that VZD approved the changes
or the map; no logo. Wording approved by the owner 2026-09-24. **MUST DO: nothing.**

**43. Riga municipality (Riga) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** CC BY 4.0 on GEO RĪGA's open-data page and each dataset
(read 2026-09-24): credit Rīgas valstspilsētas pašvaldība, link the licence, state the
changes. **MUST NOT SAY** that the merged neighbourhood outline is Riga's administrative
boundary (the publisher's own warning), or that the municipality endorses the map.
Wording approved by the owner 2026-09-24. **MUST DO: nothing.** The VID excise register
and Rīgas satiksme's GTFS are CC0 (read 2026-09-24) and need no notice.

**44. Fiscal Information Agency (Taiwan) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** OGDL v1 (read 2026-09-23), whose attribution statement is
load-bearing (§三(二)), in the annex's prescribed form, plus the FIA's own declaration: cite
the source, no emblems, no implied endorsement, and do not present the filtered points as the
register - the notice says what was selected and changed. **National**: each Taiwanese city
adds its name to this notice rather than a second one. Wording approved by the owner
2026-09-25. **MUST DO:** `check_personal_exposure.py taichung` (the name-rule test), run
2026-09-25 (the verdict is in `DECISIONS.md`).

**45. Taichung City Government and Taichung MRT (Taichung) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** OGDL v1 on both (read 2026-09-25 by the `licence-read`
agent): the door plates' 提供機關 is 臺中市政府數位發展局 (renamed from 數位治理局 in
2025-01), dataset 臺中市115年1月至各月份GIS門牌資料, read off its own portal page (the portal
exposes no machine-readable licence field); the station table's is 臺中捷運股份有限公司,
dataset 臺中捷運綠線車站資訊 (data.gov.tw 144164, `license: "1"`). One statement each, in
the prescribed form. Wording approved by the owner 2026-09-25. **MUST DO: nothing.**

**46. Taoyuan City Government, NLSC and Taoyuan Metro (Taoyuan) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** OGDL v1 on all three (read 2026-09-25): the door plates'
提供機關 is 桃園市政府民政局 (桃園市門牌位置坐標資料, data.gov.tw 157689); the station layer's
內政部國土測繪中心 (捷運車站, 73233, `license: "1"`); the station list's 桃園捷運公司, as the
publisher's own portal names it (the national catalogue says 桃園市政府桃園捷運公司; owner:
the publisher's form). **One condition outside the licence, ACCEPTED by the owner
2026-09-25**: Taoyuan's portal FAQ (關於平台 → 常見問答, "資料在使用時有什麼需要注意的嗎？",
dated 2024-01-05) says value-added use must not *"有誤導社會大眾、有意或無意侵害本府利益之虞"* -
mislead the public, or intentionally or unintentionally jeopardise the City Government's
interests. Neither is defined; the map is attributed, says its counts are its own and states
its limits, and removal requests are honoured. Wording approved by the owner 2026-09-25.
**MUST DO: nothing.**

**47. Taipei and New Taipei City Governments and Taipei Metro (Taipei (Regional)) — required,
and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** OGDL v1 on all three (read 2026-09-23 and 2026-09-25): Taipei's
door plates (臺北市政府民政局), New Taipei's (新北市政府民政局, whose portal FAQ adds nothing), and
Taipei Metro's station list (臺北大眾捷運股份有限公司, the full legal name). **Taipei Metro's
own 政府網站資料開放宣告 adds, ACCEPTED by the owner 2026-09-25**: cite the source; no patent,
trademark or company logo is licensed; the grant implies no endorsement of a derivative; and
whoever *maliciously* alters the data so that it misrepresents the original bears civil and
criminal liability. Wording approved by the owner 2026-09-25. **MUST DO: nothing.**

**48. Daegu Metropolitan City (Daegu) — required, and DISPLAYED.**

**A DISCLOSED REASONED POSITION** (owner, 2026-09-27; the reasoning is under "Daegu and
Busan" above). D-데이터허브's files declare no licence; the permission rests on the portal's own
공공데이터 이용정책 and the Public Data Act, and the City's copyright guide's request to consult
before using unmarked material is recorded, not adopted. The credit is the suggested one - Daegu
Metropolitan City, D-데이터허브 (linked), originally 한국지역정보개발원 - with the fourteen permit
types, the edition and **the rows' real date (2025-09-02; the edition is named August 2026)**,
Seoul's describe-the-changes line and a non-endorsement line. Wording approved by the owner
2026-09-27. **MUST DO:** `check_personal_exposure.py daegu`, run 2026-09-27 (the verdict is in
`DECISIONS.md`). **If Daegu objects, the page comes down.**

**49. Busan Metropolitan City (Busan) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS** (read 2026-09-27; the reasoning is under "Daegu and Busan"
above): a reasonable source credit under the portal's own 공공데이터 이용정책 (저작권법 제37조, no
wording prescribed), and good-faith use. The terms' 제14조 is read as covering only works the
platform itself authored (owner-accepted). The credit names the Ministry's local-government
licensing data as the source, Big-데이터웨이브 (linked) and its 구군 인허가포털 Open API as the
channel, the fourteen permit types and **the frozen snapshot's date (2026-04-15)**, with Seoul's
describe-the-changes line and a non-endorsement line. Wording approved by the owner 2026-09-27.
**MUST DO:** never read or publish `sitetel` (asserted in step 2);
`check_personal_exposure.py busan`, run 2026-09-27 (the verdict is in `DECISIONS.md`). Any
objection from Busan is honoured, not argued.

**50. City of Kobe and MLIT (Kobe) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS** (read 2026-09-24; the Japan rows in
[`data_sources/japan.md`](data_sources/japan.md)). Kobe City's lists are **CC BY 2.1 JP**:
the prescribed `出典：「生活衛生関係許可施設等の情報提供」（神戸市）（https://www.city.kobe.lg.jp/a99427/kenko/health/hygiene/dataset.html）`,
`…を加工して作成`, the licence link and © City of Kobe. MLIT's 位置参照情報 and N02 are **PDL
1.0**, each with its own credit line. N03 (CC BY 4.0) is credited although it is only used to
pick stations and is **never drawn** (the Survey Act). **MUST NOT**: look as if the city made the
map; use city logos; say the pins are businesses open now (the city's page warns closed premises
remain). **If the city asks, remove its credit** (CC BY 2.1 JP art. 5). Wording approved by the
owner 2026-09-27. **MUST DO:** `check_personal_exposure.py kobe` with its Japan pass (the
operator's own name is never shown as a trade name), run 2026-09-27; the verdict is in
`DECISIONS.md`.

**51. Réseau express métropolitain (Montréal) — required, and DISPLAYED with the
tram batch** (written into `render_site_notices()` 2026-09-27, wording approved
by the owner; displayed once the batch lands, as the REM maps are).
Added 2026-09-27 with the tram rescope, which draws the REM from its own GTFS.
**PERMITTED WITH CONDITIONS** (CC BY 4.0, from the licence file bundled in the feed;
the reasoning is in `docs/data_sources/canada.md`): credit **Réseau express
métropolitain (REM)**, state that the data was modified, link the CC BY 4.0 licence; no
wording prescribed. **MUST NOT:** imply endorsement or official status (§2(a)(6)); use the
REM logo (§2(b)(2)). Remove the credit if the REM asks (§3(a)(3)). The credit names
the REM, links CC BY 4.0, states the three modifications (services drawn as one line,
stations outside the agglomeration removed, two merged with same-named Métro
stations) and disclaims endorsement. The STM credit beside it (13) still reads "Métro
route geometry", which stays true.

**52. Osaka City and MLIT (Osaka) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed once Osaka lands, after Kobe).

- **PERMITTED WITH CONDITIONS** (read 2026-09-24; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)).
- **Osaka City's lists are CC BY 4.0.** Each of the three source pages says
  「CC-BY4.0で提供いたします。」, re-read 2026-09-27. The city's terms are
  政府標準利用規約 2.0, usable equally under CC BY 4.0.
- **The credit** uses the city's example form, one title per page:
  `「食品営業許可施設一覧」（大阪市）（…/0000575579.html）`,
  `「理容所及び美容所の開設施設一覧」（大阪市）（…/0000431136.html）` and
  `「クリーニング所の開設施設一覧」（大阪市）（…/0000552712.html）`, then
  `を加工して作成`, with the licence linked.
- **MLIT's 位置参照情報 and N02** are PDL 1.0, credited as in 50. N03 (CC BY
  4.0) only picks stations and is **never drawn**.
- **MUST NOT**: present the map as the city's own; use city logos; say the pins
  are businesses open now.
- Wording approved by the owner 2026-09-28.
- **MUST DO:** `check_personal_exposure.py osaka` with its Japan pass, run
  2026-09-27: 0 operator names shown, 9 withheld. The verdict is in
  `DECISIONS.md`.

**20 amended in the same change.** Its text now reads "Metro de Madrid and Metro
Ligero", and its "datos explotados" disclosure adds "of Metro Ligero only line ML1
drawn": ML1 comes from CRTM's `M10_Red` (same licence, same 5 June 2026 edit date).
"Powered by CRTM" stays verbatim.

What has grown instead is the pile of **permission questions**, now four: three
"what does silence mean?" calls and the route-colour one. They are questions
about permission rather than implementation, and they are the only items of
that kind outstanding. Two sources' positions remain formally unestablished —
the Census geocoder, whose terms are simply unread, and **Miami-Dade, whose
terms do not address reuse at all.** Those two are different in kind: one is a
document nobody has opened, the other is a document that does not exist.

## Gaps

- ~~San Francisco's boundary layer endpoint is not recorded anywhere.~~
  **Closed 2026-09-21:** identified as `wamw-vt4s` and confirmed byte-for-byte
  against the raw file. Every built city can now be rebuilt from scratch from
  this document alone, which `scripts/check_provenance.py` asserts rather than
  this sentence claiming it — it said “all five cities” until 2026-09-22, long
  after there were sixteen.
- Retrieval dates marked ≈ are inferred from commit history, not recorded at
  download time. Dates for cities added from now on are recorded exactly.
- Licences, as above — the one substantive gap left.
