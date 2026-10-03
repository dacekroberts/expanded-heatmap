# Where every piece of this project's data comes from

One row per source, per city. This is the master provenance list: if a map
shows something, its source is named here, with the endpoint it came from and
the filter applied at download.

Before this list, the endpoints were scattered: some in a city's `config.py`
comment header, some only inside a `step*.py` error message, and several (San
Francisco's boundary layer among them) nowhere at all. Kept in one place, a
reader can check the work, a dead endpoint shows up before a rebuild fails,
and each source's license can be read one source at a time.

**Every source is public.** Nearly all are government datasets; the main
exception is OpenStreetMap, the volunteer-built map behind the basemap and
many cities' rail lines. Nothing here is scraped or purchased. A few sources
need an account: WMATA's feed (Washington D.C.) an API key, and Denmark's
Datafordeler (Copenhagen) a registration.

## How to keep this current

- **Adding a city adds its rows here, in the same commit** — provenance *and*
  license together<!-- internal -->. The `add-city` skill makes both a Step 0 requirement and
  re-checks them at Step 9<!-- /internal -->; a city whose data is mapped but whose terms are
  unrecorded is not finished, because afterwards that gap is invisible — it
  looks exactly like a city that was checked.
- Record the **endpoint**, the **server-side filter** (the download is often
  filtered — that filter is part of the provenance), and the **date retrieved**.
- Record the **license, and anything the source requires this project to
  display**. Do not infer permissive terms from the fact that a source is
  government open data: the review below found everything from public-domain
  dedications to a feed that forbids modifying its data, and both extremes
  inside one city. Socrata states a license directly at
  `<domain>/api/views/<id>.json` (`license`, `licenseId`, `attribution`); a
  missing value there means "go read the terms", not "no restrictions".
- **A new required notice goes in the notices section below**, which gates the
  public deploy. A new clause needing a human decision goes to the owner<!-- internal --> and
  then to `DECISIONS.md`<!-- /internal --> — not resolved by reading it generously.
- When an endpoint dies, leave the old row and mark it dead with the date,
  rather than overwriting it. Dataset IDs get retired: New York's borough
  boundaries moved from `tqmj-j8zm` (now 404) to `gthc-hcne`, and the MTA
  retired its `web.mta.info/developers` GTFS path in favor of an S3 bucket.
  A silently-replaced URL loses that history.
- Raw downloads are **not** committed (`data/<city>/raw/` is gitignored). Only
  the rendered `outputs/` are. So these endpoints plus the recorded filters are
  the only way to reproduce a build.
- **Declare the source encoding.** Set `SOURCE_ENCODING` in the city's
  `config.py` and pass it to every raw read, rather than relying on the
  default. pandas defaults to UTF-8 and *raises* on anything else, which is
  safe — but the failure lands on whoever adds the next city, and the tempting
  fix (reach for `latin-1` to make the `UnicodeDecodeError` go away) corrupts
  accented characters **without failing**, so nothing catches it downstream.
  Declaring it makes the choice reviewable and part of the provenance. Most
  declared encodings are UTF-8, but the Japanese permit lists also use `cp932`
  and `utf-16`, and Quebec data in particular is still often published in
  `latin-1`. Note that mojibake
  in a *terminal* is usually the Windows console codepage, not the file — check
  the bytes before changing the declaration.
- **Read a new city's whole catalog, do not grep it.** Listing every package
  name and reading them costs about a minute and ~3 KB; keyword-filtering the
  list reintroduces exactly the bias that pulling the full list was meant to
  remove. Montréal proved it on 2026-09-21: `locaux-commerciaux`, a 28,621-row
  agglomeration-wide survey of street-level commerce with NAICS codes and 100%
  coordinates, contains none of the words *business*, *license*, *permis*,
  *entreprise* or *commerce*, and a keyword scan wrongly concluded the city was
  food-only. Neither does `unités d'évaluation foncière`, its property roll.

## Where each country's sources live

**This record was split by country on 2026-09-27**, when it had grown to
about 55,000 words, almost all of them about single cities. Each country's
part now lives in its own file under [`data_sources/`](data_sources/), moved
word for word with its headings: its rows of the business, transit, boundary,
geocoding and license tables, and every section about its cities' sources.
What stays here applies to every city: the rules above, the notes on the
transit and boundary tables, the basemap, the removal-request commitment, the
obligations that are not notices, the numbered notices and the deploy gate.

<!-- internal -->**Adding a city adds its rows to its country's file**, under the same headings
used here; a country's first city creates that file and a row in this table.
`scripts/check_provenance.py` reads this file and every file in `data_sources/`
together, so a row in either counts and a row in neither still fails.<!-- /internal -->

| Country | File | Cities |
|---|---|---|
| United States | [`data_sources/united-states.md`](data_sources/united-states.md) | San Diego, San Francisco, Los Angeles, Chicago, New York, Philadelphia, Miami (Regional), Boston, Washington D.C., Buffalo, Sacramento, Houston, Minneapolis, Pittsburgh, Dallas, Kansas City, Tucson, New Orleans, Seattle (Regional) |
| Canada | [`data_sources/canada.md`](data_sources/canada.md) | Vancouver (Regional), Montréal, Calgary, Edmonton, Toronto, Ottawa, Kitchener–Waterloo (Regional) |
| Mexico | [`data_sources/mexico.md`](data_sources/mexico.md) | Mexico City, Guadalajara (Regional), Monterrey (Regional) |
| Spain | [`data_sources/spain.md`](data_sources/spain.md) | Madrid, Barcelona, Palma |
| Ireland | [`data_sources/ireland.md`](data_sources/ireland.md) | Dublin |
| Italy | [`data_sources/italy.md`](data_sources/italy.md) | Milan, Rome, Florence |
| France | [`data_sources/france.md`](data_sources/france.md) | Paris, Marseille, Toulouse, Lille (Regional), Rennes, Le Mans, Besançon, Avignon, Tours, Dijon, Reims, Orléans, Mulhouse, Brest, Saint-Étienne, Nice, Montpellier, Strasbourg, Le Havre, Caen, Rouen (Regional), Bordeaux (Regional), Nantes (Regional), Grenoble (Regional), Valenciennes (Regional), Angers |
| Norway | [`data_sources/norway.md`](data_sources/norway.md) | Oslo, Bergen |
| Romania | [`data_sources/romania.md`](data_sources/romania.md) | Bucharest |
| Sweden | [`data_sources/sweden.md`](data_sources/sweden.md) | Stockholm, Göteborg |
| Denmark | [`data_sources/denmark.md`](data_sources/denmark.md) | Copenhagen, Aarhus, Odense |
| Czechia | [`data_sources/czechia.md`](data_sources/czechia.md) | Prague, Brno, Plzeň, Olomouc, Ostrava, Liberec (Regional), Most (Regional) |
| Netherlands | [`data_sources/netherlands.md`](data_sources/netherlands.md) | Amsterdam, Rotterdam, Den Haag |
| Latvia | [`data_sources/latvia.md`](data_sources/latvia.md) | Riga, Liepāja, Daugavpils |
| Brazil | [`data_sources/brazil.md`](data_sources/brazil.md) | São Paulo, Rio de Janeiro, Belo Horizonte, Brasília, Salvador, Fortaleza (Regional), Porto Alegre (Regional), Recife (Regional), Santos (Regional) |
| Hong Kong | [`data_sources/hong-kong.md`](data_sources/hong-kong.md) | Hong Kong |
| South Korea | [`data_sources/south-korea.md`](data_sources/south-korea.md) | Seoul, Daegu, Busan, Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang |
| Taiwan | [`data_sources/taiwan.md`](data_sources/taiwan.md) | Taichung, Taoyuan, Taipei (Regional) |
| Japan | [`data_sources/japan.md`](data_sources/japan.md) | Kobe, Osaka, Sapporo, Fukuoka, Kyoto, Tokyo, Yokohama, Hiroshima, Matsuyama, Toyama, Kumamoto, Fukui, Nagasaki, Utsunomiya, Kitakyushu, Sakai, Hakodate, Kagoshima, Okayama, Kōchi |
| Germany | [`data_sources/germany.md`](data_sources/germany.md) | Berlin |
| United Kingdom | [`data_sources/united-kingdom.md`](data_sources/united-kingdom.md) | London, Glasgow, Newcastle (Regional) |
| Argentina | [`data_sources/argentina.md`](data_sources/argentina.md) | Buenos Aires |
| Australia | [`data_sources/australia.md`](data_sources/australia.md) | Sydney, Melbourne |
| Switzerland | [`data_sources/switzerland.md`](data_sources/switzerland.md) | Zurich |
| Georgia | [`data_sources/georgia.md`](data_sources/georgia.md) | Tbilisi |

## Business registries

The rows are per country: each file in [`data_sources/`](data_sources/)
opens with its own rows of this table, followed by the notes on its cities'
registries (Boston's, Madrid's and Dublin's first findings among them).

## Transit feeds

**Titled “Transit feeds (GTFS)” until 2026-09-22.** The first table is all
GTFS feeds and always was; the section now also holds a subsection for rail
that is **not** a feed, so the heading no longer claims GTFS.

Both tables' rows are in each country's file, under the same headings.

### Rail geometry that is not a GTFS feed

**These cities have their own subsection rather than rows in the feed
table.** A source that is not a feed has no `feed_info.txt`, no validity
window and no `route_id`, three things every note in that table turns on, so a
row there would have meant empty columns.

**Two different reasons land here, and they are not the same case.**

- **Mexico City and Guadalajara were the first to come from OpenStreetMap via
  Overpass**, because no usable feed exists; many cities have followed, each
  listed in its country's file. An OSM source also has no agency holding the
  license: all are **ODbL 1.0**, covered by **notice 1**, which since these
  builds covers *data* and not only basemap tiles.
- **Madrid comes from CRTM's own ArcGIS feature services**, and there the
  operator's feed exists and downloads cleanly — it is rejected because CRTM's
  license obliges a reuser to keep displayed information *“siempre
  actualizada”* and that feed has not been refreshed since 2025-05-30. A
  license consequence rather than an absence, and the license is CRTM's own,
  not OpenStreetMap's. **Madrid sat under the OpenStreetMap heading for part of
  2026-09-22**, which was wrong in the way this subsection exists to prevent.

<!-- internal -->**Why more than one Overpass mirror, and how one is chosen.** They are tried
**in the configured order**, and the first host returning HTTP 200 with a
**non-empty `elements` list** wins; any other outcome (a non-200, an
exception, or a 200 with an empty body) moves on to the next. More than one,
because across the two Mexico builds each of the three mirrors then in use
failed at least once and none failed consistently: `overpass-api.de` returned
504 several times and 429 once, `overpass.kumi.systems` 504 several times, and
`overpass.osm.ch` **answered 200 with an empty body**, all at different times,
for the same query. A failure is a fact about that host at that moment and
not about the city, so one mirror would make the build's success a coin flip.
Two global mirrors remain: `overpass.osm.ch` was dropped on 2026-09-27 because
it holds only a Swiss extract and answers 200 with nothing anywhere else.

**A 200 with no elements is treated as a host FAILURE and is never cached**,
which is the half that is not obvious. `overpass.osm.ch` once returned 272
bytes and an empty element list for the routes query; the fetcher cached it,
and the caller then reported *"every ref has exactly 2 direction relations"* —
**a vacuous truth over an empty set**. Both cities' step 1 now assert
non-emptiness before any check that could pass vacuously. Responses that do
succeed are cached to the gitignored `data/<city>/raw/osm_*.json`, so a re-run
or a drift check never depends on which mirror answered. Mexico City makes one
pass over the host list, sleeping 2 s between hosts. Guadalajara now fetches
through the shared OpenStreetMap module, which makes **two passes** before
giving up, pausing 5 s between them, or at least 60 s after a 504, a 429 or a
timeout.<!-- /internal -->

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
rendered HTML. Choosing a tile provider deliberately is still an open
decision (see "Basemap tiles" under the licenses below).

## Licenses and terms of use

Reviewed 2026-09-21. This records what each source's own published terms say,
and what could not be established. It is a developer's reading of public
documents, not legal advice, and none of it has been reviewed by a lawyer.

A separate question is already settled: what is *appropriate* to publish,
independent of what is *permitted*. That is on the companion page, *What is
counted, and what is not*.

Each source's reading is in its country's file: the rows of the tables
*Explicit and permissive — confirmed* and *Transit feeds (GTFS)*, the sections
on Madrid, Seoul, Daegu and Busan, Brazil, Taiwan, Japan, CRTM and Barcelona,
and the United States' own tables and open questions (*Permissive on reading
the terms themselves*, *Still not established*, the API-account practice, the
agency-branding question). What stays here is what applies to every city.

### Transit feeds (GTFS) — checked 2026-09-21

Line geometry is redrawn from each feed's `shapes.txt` into every map, so these
terms bear directly on what is published. **No feed in this project declares a
license in `feed_info.txt`** — LA Metro's even includes a `feed_license` column
and leaves it empty, pointing to its developer terms instead. Several feeds ship
no `feed_info.txt` at all (Miami, Calgary, Toronto), and two ship one that
carries a validity window but no license (Montréal, Vancouver), so in every case
the agency's own terms page is the only source and every row below was read from
one.

The table's rows are in [`united-states.md`](data_sources/united-states.md)
and [`canada.md`](data_sources/canada.md).

**The agreements quoted in that table are stored locally**, in
[`licenses/`](licenses/). That directory's `README.md` is the list, with each
one's source URL, retrieval date and SHA-256; a count kept here went stale as
the directory grew past twenty. Every one of them is revocable and amendable
without notice, so the clauses quoted can be checked against the text that
was actually agreed to rather than against a URL that may have moved on.

### Basemap tiles — one active compliance item

The maps render **OpenStreetMap** tiles, fetched directly from
`https://tile.openstreetmap.org/{z}/{x}/{y}.png`.

- **Data license: ODbL 1.0.** Attribution is required — credit OpenStreetMap
  and link to the license, visibly, not "beneath UI, behind toggles, or
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
  policy is explicit that there is no guarantee behind it. It is the same
  open decision as choosing a tile provider, and it should be settled
  deliberately rather than by default.

## Commitment: removal requests are honored, not argued

Every license reviewed here enforces the same way. Chicago's terms say the
city "may require a user of this data to terminate any and all display,
distribution or other use"; Open NY says the State may require you, "by
providing you with a notice in writing", to cease using or displaying its
content; LA Metro says that on termination you "shall immediately remove the
Transport Information and all references to it". The remedy contemplated
throughout is a request to stop.

**A second trigger, added 2026-09-21 and widened 2026-10-02: a publisher
saying this use is not permitted is enough.** Points 1-5 below fire when a
publisher *asks* for its data to stop being displayed; this one covers the
sources that neither grant nor forbid reuse, which this project reads in its
favor: Philadelphia, whose data carries a City license that grants nothing and
website terms that forbid republication (the City was asked for its position
on 21 September 2026 and has not replied); Miami, Tucson, Dallas, Seattle
(King County, Bellevue and Snohomish County), Amsterdam, Den Haag, Stockholm,
Bucharest and Daegu, whose sources carry no license, or terms written for a
website rather than its data; and Brazil's census addresses, which rest on
federal law rather than a license. **If any of those publishers says this use
is not permitted, its city comes off the site without being asked twice, and
silence is never treated as permission.** Each reading is recorded with its
source below. The same wording is in the footer of every page, beside the
required attributions, so a reader learns it at the same moment they learn
where the data came from. That footer, this paragraph and the *What is
counted, and what is not* page are one promise and are kept consistent.

**A third trigger, added 2026-09-22: a license that ENDS BY ITS OWN TERMS.**
The first two fire on a publisher asking and on this project finding out.
This one fires on neither — **Licence Mobilités Art. 11.1 terminates *de plein
droit, sans préavis* on breach**, so the grant can simply stop, with no notice
to receive and nothing to discover. It is the first revocable grant in this
project: CC BY, Licence Ouverte, the PSI licenses and ODbL are all perpetual,
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

**This project commits, in advance, to honoring such a request.** Stated so
that it is a standing position rather than a decision made under pressure:

1. **If a data publisher asks this project to stop displaying its data, it
   will stop.** The affected layer, or the whole city, comes down. No case
   will be argued first, no justification will be requested, and compliance
   will not be made conditional on the publisher explaining itself.
2. **If a business owner asks for their listing to be removed, it will be
   removed**: the *What is counted, and what is not* page says the same thing
   to the people it concerns. They do not have to give a reason.
3. **If anyone raises a privacy concern about a specific pin**, it is treated
   as a removal request under point 2 and actioned first; any disagreement
   about whether the concern was well-founded is separate from taking the pin
   down.
4. **A request is honored even if this project believes it is in the right.**
   The license review found nothing forbidding what is built here, and that
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
license that also granted permission freely, which is why they are easy to
miss: the grant is the headline and the obligation is a subordinate clause.

| Class | Who | What it actually requires |
|---|---|---|
| **An act owed to the publisher** | **Barcelona** 🇪🇸 | *"Users are required to inform Barcelona City Council of every project relating to or derived from their use of the data sets."* A message a person sends<!-- internal -->. Drafted at `docs/notifications/barcelona-city-council.md`<!-- /internal -->, **not yet sent** |
| **A live account that must STAY live** | **WMATA** (Washington D.C.) 🇺🇸 | The terms are an API agreement, so §9(i) ends the grant when the account ends — and what lapses is the right to **publish the page**. Gate item 10 |
| ✅ **A liability ACCEPTED** | **Hong Kong** 🇭🇰 | **ACCEPTED BY THE OWNER 2026-09-22.** *"you shall **indemnify** the Government and the Relevant Organisations against any allegations or claims of infringement of the rights of any person and all costs, losses, damages and liabilities incurred … which in any case arise **directly or indirectly** in relation to your use, reproduction and/or distribution of the Data"*. See the section below for what the earlier record omitted |
| 🔧 **AN ACCESS A PERSON MUST OBTAIN** | **Copenhagen / Denmark** 🇩🇰 | **Added 2026-09-23 at the owner's request.** CVR's premises data needs a **Datafordeler account the owner creates by hand**, and the terms pages sit behind a **Cloudflare interactive challenge** this project does not defeat — so both the registration and the reading are **human-only work**. Unlike WMATA's API agreement (above), the license here is **CC BY 4.0, which attaches to the DATA and is irrevocable**, so the owner's standing practice (*register, take the data, terminate, revoke*) is safe here and unsafe for WMATA. ✅ **Close the account freely; the right to publish survives.** The similarity is the registration effort, not the obligation (see below) |

**Copenhagen and WMATA look alike at the signup form and diverge immediately after it.** Both made the owner register; only one made the account load-bearing. **The test is what the terms ARE** — an API agreement licenses *you*, so it can be withdrawn from you, while a public license licenses *the data*, and nothing you do to your account reaches it. Recording the two in one row would have told a later reader to keep a Danish account alive forever, and implied that closing it revokes the right to publish Copenhagen. **Neither is true.**

**Hong Kong's was weighed before building, not after.** Everything
else in `data.gov.hk`'s Terms of Use v1.2 (26 May 2025) is generous — download,
distribution and reproduction are permitted for **commercial and
non-commercial purposes, free of charge**, subject only to identifying the
source, acknowledging Government ownership of the IP, and proper attribution.

**The indemnity is not a notice, not a credit, and not a step in a build.** It
is an open-ended undertaking to cover the Government's costs if a third party
alleges the data infringed their rights. Hong Kong was the first source in
this project to ask for one; others have since, among them Sacramento, Palma,
Dallas and San Diego's SanGIS layers (below). **It was an owner decision, taken before the register's
35,808 premises were wired into a page**, not once the city was live.

### Hong Kong's indemnity — ACCEPTED 2026-09-22, and what the first record omitted

**The owner accepted this on 2026-09-22, in chat, after the live clause was
re-read.** It was the first uncapped liability in this project. Recorded here
with its reasoning so it is a decision rather than a drift.

**Two things the first record's quote left out**, both found by reading
`https://data.gov.hk/en/terms-and-conditions` (Terms v1.2) itself rather than
the earlier citation of it:

1. **"arise directly or indirectly"** — the earlier quote elided it. Broad
   causation, not just proximate.
2. **There is NO notice-and-defend clause.** The Government need not tell you a
   claim exists, you have no right to control or even join the defense, and
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
commitment to **honor removal requests without argument** cuts off the likeliest
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
   place.** They are notice 41 (Hong Kong).
2. **<!-- internal -->Run `python scripts/check_personal_exposure.py hong_kong` and <!-- /internal -->exclude
   catch-all categories** — the Los Angeles NAICS 812990 precedent. The
   realistic complainant is an individual whose name sits at what looks like a
   home, so the privacy filter is the risk control, not a formality.
3. **This entry is condition three**, dated and reasoned.

**Extended 2026-09-24 to the CSDI Portal's terms.** The build places each license at FEHD's
own point from the CSDI Portal, whose terms (`portal.csdi.gov.hk/csdi-webpage/doc/TNC`<!-- internal -->, read
2026-09-24 by the license-read agent<!-- /internal -->) have the same shape and the same uncapped indemnity, and
one addition: to *"identify clearly the Government and the CSDI Portal as the source"*, which
notice 41 does. The owner accepted it in chat on 2026-09-24, with the switch from the Address
Lookup Service (ALS). The privacy condition was run the same day: FEHD's registers carry
the shop sign and no licensee name at all.

#### One consistency note

**Lyon's Grand Lyon CGU 9.4 is the same shape** and was recorded as the
project's second indemnity. Accepting Hong Kong's does **not** automatically
accept Lyon's — Lyon carries two further gates (an account this project does
not create, and a trademark clause that collides with an invariant), so it
stays deferred on those grounds regardless.

#### Sacramento's indemnity — ACCEPTED 2026-09-29

The City of Sacramento's **Open Data Terms of Use** (the same text as its Open
Data Policy, pp. 13–18<!-- internal -->; read 2026-09-29 by the license-read agent<!-- /internal -->) govern the
Business Operation Tax layer. They carry the same shape again: the user "will
indemnify, defend at his/her sole cost and expense, and hold harmless the
City … even if the claim may be groundless, false or fraudulent". There is no
cap, and it is **accepted "by machine-consuming, or downloading and using the
Data"**. The staging brief's measurement had already pulled the layer's
24,040 Active rows (never the owner, phone or mailing columns) before the
terms were read. **The owner accepted the indemnity on 2026-09-29 with that
fact stated.** As with Hong Kong, the acceptance covers this one source; it
is not a notice or a build step. The Hub's "Request permission to use" label
on the same dataset was settled the same day: Esri's label for an
empty license field, not a term, since the City's Terms grant use (owner, 2026-09-29<!-- internal -->;
`docs/build_briefs/sacramento.md`<!-- /internal -->). Built on 2026-09-29.

#### Palma's indemnity — ACCEPTED 2026-09-29

GOIB's *Política i termes d'ús*, which govern the Consell de Mallorca's
restaurant register on the Balearic open-data catalog<!-- internal --> (read 2026-09-29 by
the license-read agent)<!-- /internal -->, carry the same shape again. The reuser "accepta
indemnitzar, així com eximir al Govern de les Illes Balears … de qualsevol
responsabilitat … pel mer ús, reproducció, modificació o distribució de la
informació", with no cap. **The owner accepted it on 2026-09-29, for this
one source.** On the same day the owner extended Barcelona's reading of the
"no alteration" condition (Ley 37/2007 art. 8 wording) to this source, and
took the permissive reading of Catastro's INSPIRE terms for the address join<!-- internal -->
(`docs/build_briefs/palma.md`)<!-- /internal -->.

#### Dallas's indemnity — ACCEPTED 2026-09-30

The City of Dallas's **Standard GIS Data Disclaimer of Liability** (2015-12-04; the
linked PDF is dead, and the current copy is ArcGIS item `115c0fe8ed4b4a12a669f5e48dc56d52`)
governs the City's **Address Points** layer (item `0a5c879d970f4b32b744476e29e0e54b`),
which the Dallas build uses only to place the Comptroller's permit addresses.<!-- internal --> It was
read on 2026-09-30 by the license-read agent.<!-- /internal -->

- **The shape:** the same again. The user agrees to "indemnify, defend, and hold
  harmless The City of Dallas" for any liability arising from errors in the data
  or from its use.
- **How it binds:** it is accepted by using the data. There is no cap.
- **Reuse:** nothing grants it and nothing forbids it. The layer is not on
  dallasopendata.com.
- **The owner accepted it on 2026-09-30, for this one source**, after the
  alternative (placing through the Census geocoder) was offered unmeasured. As
  with Hong Kong, it is not a notice or a build step.
- **Prose rule:** never call Dallas's pin locations surveyed or exact.
- **Optional credit:** "City of Dallas Development Services GIS".

#### San Diego's SanGIS indemnity — ACCEPTED 2026-10-02

The **SanGIS GIS Data End User Use Agreement and Disclaimer for Data Released
to the Public** (2015-04-02) governs both SanGIS layers the San Diego build
uses. It sits in each item's own `licenseInfo`.<!-- internal --> It was read on 2026-10-02 by the
license-read agent for the boundaries, confirming the parcels row's
agreement.<!-- /internal -->

- **The layers:**
  - the **countywide tax parcels** (the residence-filter join);
  - the **municipal boundaries**, item `c034e931bd83403892eea61fdae5a6ae` on
    `geo.sandag.org`. SANDAG only hosts them; the owner is SanGIS.

- **The shape:** the same again, plus a release. The user agrees "to
  indemnify, defend, and hold harmless and release SanGIS for any and all
  liability of any nature arising out of or resulting from the lack of
  accuracy or correctness of the data, or the use of the data". The user also
  "expressly waives all rights under Section 1542 of the Civil Code of the
  State of California".
- **How it binds and where:** "Use of the data specifically acknowledges the
  end user's acceptance". There is no cap, and venue is the County of San
  Diego.
- **The owner accepted it on 2026-10-02, for these two SanGIS layers** ("Sangis
  indemnity okay"). It was not recorded as accepted when the parcels were
  first wired in. As with Hong Kong, it is not a notice or a build step.
- **Unchanged by the acceptance:**
  - **SanGIS is still never credited at map scale** (finer than 1:24,000,
    the agreement's attribution prohibition).
  - The layers are never presented as an original SanGIS product.
  - They are never called legal or surveyed boundaries.
- **SANDAG's own Data Terms of Use** ("should not be redistributed", plus a
  SANDAG indemnity) defer to a third party's terms where the source is not
  SANDAG. The SanGIS agreement is the one read as governing.

## Notices this project MUST display when published

This is the operative output of the license review. As of 2026-09-21, for the
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
page and `excluded_categories.md`<!-- internal --> (see `PLAN.md`)<!-- /internal --> — publishing the maps
without them would breach terms this project has now read.

Not required by anyone, but good practice and already partly done in the city
pages' prose: naming each business registry's publishing agency.

**1. OpenStreetMap — required, and ALREADY SATISFIED.** ODbL 1.0 requires
visible credit and a license link, "not beneath UI, behind toggles, or
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
deploy look blocked when it is not.<!-- internal --> Found by `scripts/check_stale_claims.py` on
its first real run, which is the argument for the tool in one line.<!-- /internal -->

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

**This heading read "NOT YET DISPLAYED" until 2026-09-21 and was stale**, which
is worth leaving a note about because a compliance document that understates
compliance invites someone to re-fix a closed item and to doubt the rest of the
gate. The outstanding part had been that the acknowledgement appeared only on
Boston's own city page rather than "where the *site* is accessed"; that was
closed when `app/components.py`'s `render_site_notices()` began carrying all
five outstanding notices on **every** page, and this heading was not updated
with the others. Verified against `_NOTICES` on 2026-09-21.

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

<!-- internal -->### What closing this fully requires

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
   first. It is also the only one of the three with no agency document to
   read, so settling it may mean asking the County instead.
5c. **Decide the agency-branding question: official route colours AND the
   line names beside them.** It affects the cities whose agency prescribes a
   palette: San Diego (MTS), Los Angeles (LA Metro), Chicago (CTA), New York
   (MTA), Philadelphia (SEPTA) and, since 2026-09-21, Washington D.C. (WMATA),
   whose wording names "confusingly similar variants". San Francisco and Miami
   are out of scope, since they already draw their own palettes. **MTS's wording
   is the tightest in the project**: its trademarks "may not be used in
   association with GTFS Data", a flat prohibition rather than an application
   process, so start there rather than with MTA's, which needs only a free
   application. On 2026-09-21 the owner chose to keep the official colours and
   record this rather than switch palettes in advance. Colours are cheap to
   reverse (one setting per city); **line names are not**, because a standing
   rule requires every drawn line to carry its real public name. See the table
   under the GTFS notes.
6. **Display the required notices** (above) — the one thing that still blocks
   publishing, and part of the same app job as surfacing this page.
7. **Decide the tile provider deliberately**, given that OSM's tile service is
   explicitly best-effort with no SLA.
8. Optionally, read the Census geocoder's terms, which are still unread, as
   are San Diego's municipal-boundary layer's (see its row). The licence table
   is the list of what is unread.
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

   The log that proves it, since the symptom is confusing: the traceback
   printed the **old** one-line
   `from cities import CITIES, IN_DEFAULT_VIEW, MAP_ONLY_NAV`, which does not
   mention `DEFAULT_REGION` at all, above an error naming `DEFAULT_REGION`.
   Python shows traceback source by re-reading the file from disk while it
   runs a cached copy of the code, so the file on disk and the code running
   were different versions. Five pulls and five "Updated app!" across three
   hours never cleared it; only **Manage app → ⋮ → Reboot app** does.

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
    for as long as the D.C. page is published. It is a gate item because
    **nothing in the codebase can check it**: verifying an account means
    holding its key, and this project never handles one. That makes it a human
    step, the kind that gets skipped.
    WMATA's terms are an **API agreement**, so §9(i) terminates the grant the
    moment the account goes — and the right that lapses is the right to
    *publish the page*, not merely to store a file. **Re-confirmed live by the
    owner on 2026-09-22.** If it ever lapses, D.C. comes down until a new
    account is registered. The full reasoning is under the WMATA entry above;
    the standing list of items like this is `docs/gated_access.md`.

**Where this leaves the project:** nothing found anywhere forbids what this
project does. The first US cities needed **five mandatory notices**; the
numbered list has grown with every country since. Neither Philadelphia nor
Miami added one, because SEPTA, the City of Philadelphia License and
Miami-Dade all require no attribution at all. The fifth was **MassDOT's
acknowledgement, active since Boston was built on 2026-09-21**. WMATA added
none either, although this paragraph once predicted a sixth from it: its terms
require no attribution and no acknowledgement. Its constraints are on what may
be SAID (§6 accuracy, §9 deletion on termination, the trademark clause), not
on what must be shown.

What has grown instead is the pile of **permission questions**, now four: three
"what does silence mean?" calls and the route-colour one, the only questions of
that kind outstanding. Two sources' positions remain formally unestablished:
the Census geocoder, whose terms are simply unread, and **Miami-Dade, whose
terms do not address reuse at all.** One is a document nobody has opened; the
other is a document that does not exist.<!-- /internal -->

**9. City of Vancouver — required, and DISPLAYED.** The Open Government
Licence – Vancouver requires this exact sentence wherever its information is
used:

> `Contains information licensed under the Open Government Licence – Vancouver.`

Note the British spelling "Licence" and the EN DASH. This licence
**terminates automatically on breach** — "if you fail to comply with any of
them, the rights granted to you under this licence… will end automatically" —
so the notice is not cosmetic. It has been on the site since 2026-09-21, when
Vancouver was built.

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
Legend** (met: this project draws its own lines from the feed's `shapes.txt`
and reproduces no roundel), and **answering TransLink if it asks who is using
the data**, read as a duty to respond rather than a condition of use (decided
2026-09-21).

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
interpretations drawn**. Measuring density in rings, sorting businesses into
categories and keeping only storefronts are all interpretations, so **a bare
source credit does not comply**; the displayed notice says the data is
modified and interpreted, and what was done. The other two conditions: no
indicating or suggesting that the
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
It is not: that document is written entirely in **web-page** language (page,
site, navigation, hyperlien) and contains **no data language at all** - no
"données ouvertes", "jeu de données", "redistribuer", "base de données" or
"réutiliser" - and its operative sentences name montreal.ca's own contents and
photos. The open data is governed by the separate licence page above. Same
shape as nyc.gov's "All Rights Reserved" footer and Philadelphia's terms of
use: a website's terms are not its datasets' terms.

**14. City of Calgary — required, and DISPLAYED. One notice covers BOTH the
business data and the transit data**, which no other Canadian city manages:

> `Contains information licensed under the Open Government Licence – City of Calgary.`

En dash, British "Licence" — Surrey's sibling notice uses a hyphen and
"License" and the two are not interchangeable. Like Toronto's, Vancouver's and
Surrey's, this licence **terminates automatically on breach**. The Socrata
`license` field on the business register reads `See Terms of Use`, a pointer
rather than a licence: the OGL is the document it points to, stored in
`docs/licenses/calgary-open-government-licence.txt`.

**15. City of Edmonton — required, and DISPLAYED. It was recorded as needing
NOTHING, and that was wrong.** One notice covers both the business register and
ETS's GTFS, as Calgary's does, because the feed is published through the same
Open Data Catalogue.

Edmonton's Terms of Use say credit is "not required" but "encouraged", and
this project's Canada profile<!-- internal --> and Edmonton build brief both<!-- /internal --> concluded from that
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
its marks, which the site's standing non-affiliation line covers.

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
deploy.<!-- internal --> `scripts/check_provenance.py` now asserts the relationship instead:
every entry in `app/components.py`'s `_NOTICES` has a numbered item here, every
numbered item has an entry there, and the numbers are unique and contiguous.
Run it rather than counting.<!-- /internal -->

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
wrong lesson from it.<!-- internal --> `scripts/check_provenance.py` now fails when any source
in the three provenance tables has no licence position recorded, which is the
check that would have caught it on the day.<!-- /internal -->

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
does not sponsor or endorse the map. **MUST DO:** a check that the published
data carries no personal information, run 2026-09-25.

Read 2026-09-22, before the build. All eight `인허가 정보`
datasets are **공공누리 제1유형 (KOGL Type 1)**, and it is a **one-notice
country on current evidence** — every dataset carries the same licence, the
same 저작권자 and `제3저작권자: 없음`, so one notice covers the whole city
however many business types it ends up using. The Korean pattern is therefore
the US one, not the Canadian one.

Three things it requires, from `kogl.or.kr`'s own text rather than the label on
the dataset page:

- **Attribution naming institution, year, KOGL type and dataset title, with a
  hyperlink.** KOGL says a link *must* be provided where providing one is
  possible online, which it is here. It is shaped like ODbL's attribution, so
  it belongs with the site's notices, and a bare source string does not
  discharge it.
- **A non-affiliation line.** Covered by the site's standing one, first
  written for Edmonton and Toronto: no new text needed.
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

**20 amended in the same change.** Its text now reads "Metro de Madrid and Metro
Ligero", and its "datos explotados" disclosure adds "of Metro Ligero only line ML1
drawn": ML1 comes from CRTM's `M10_Red` (same licence, same 5 June 2026 edit date).
"Powered by CRTM" stays verbatim.

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
gate. **It is an owner action, outstanding**<!-- internal -->; the draft is at
`docs/notifications/barcelona-city-council.md`<!-- /internal -->.

**The displayed notice now reports that act's status**, added 2026-09-22 on the
owner's call: *"That notification is written and not yet delivered: on 22
September 2026 the portal's own contact form stalled, and the enquiry channel
the terms themselves name did not respond. It will be sent when that service is
reachable again."* It is worded as a **status report and never as though it
performed the act** — text on this project's own page is precisely what does
not discharge a duty owed to the publisher, and a sentence that blurred the two
would be worse than no sentence. When the notification is sent, that wording
and the attempt log in the notifications file change together.

**The live terms were read on 2026-09-22**, by the owner, in a browser, past
the hCaptcha. That met a condition this file had carried since the licence
review, one Barcelona had been published without. Stored at
`docs/licenses/barcelona-condicions-us-live.txt`. Three things changed, none of
them adverse:

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

**22. Tailte Éireann — required, and DISPLAYED.** Written before the build
began, so the obligation existed before the city did, and on the site since
Dublin was published on 2026-09-22. The valuation register declares
`CC-BY-4.0` on `data.gov.ie`
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
statistics return is owed: a search of every document read for any such duty
found none. **This is the opposite of Barcelona's finding**, recorded so it is
not re-opened. Channels exist anyway for corrections:
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
The build must drop it on loading, so it never reaches a processed file.

One page that reads alarmingly and does not apply:
`tailte.ie/map-shop/map-licences-and-copyright/` requires "prior permission"
for reproducing Tailte **surveying** material. It mentions valuation, open
data, API, Eircode, PSI and Creative Commons **zero times each** and governs
the paid Map Shop products. Read and inapplicable — recorded so the next
reader does not re-establish it.

**23. Comune di Milano — required, and DISPLAYED.**

Recorded at build time, so the obligation existed before the city went live.
**This item is a deploy blocker for Milan specifically**, not an outstanding
defect on the cities now published. All six premises registers and all three
ATM rail layers declare **CC BY 4.0**.

⚠️ **The version is invisible where anyone would look.** CKAN's `package_show`
reports `license_id: cc-by` with **no version at all**, and its `license_url`
points at opendefinition's version-less register entry. Three independent
sources give 4.0: the portal's **DCAT-AP_IT** serialisation
(`owl:versionInfo "4.0"`), the portal footer, and the national catalogue
`dati.gov.it`. This project's automated re-check of Milan's licence therefore
reads the DCAT-AP_IT file (`.ttl`) rather than `package_show`, which cannot
see the version it is meant to guard.

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

Recorded when the city's build began, so the obligation existed before the
city did, then **missed anyway**: the map rendered, the gate was run, and the
notice was still absent from every page. A verification pass on 2026-09-23
found it missing from the Paris page, whose notices block listed 21 sources
and not one of them French. It was added to the site's notices the same day.

<!-- internal -->⚠️ **Nothing automated caught it.** At the time, `check_provenance.py` only
printed `notices: 24 numbered, 21 displayed` as a line of output and passed
regardless. It now fails unless every numbered notice here is displayed and
every displayed notice is numbered.<!-- /internal -->

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
licence text. No other notice in this file constrains markup, so the site
cannot show this one as plain text the way it shows LA Metro's.

⚠️ **Two obligation shapes this project has never carried**, both from Art. 5.7,
which forbids use misleading « quant … à sa date de mise à jour »: the **date
the data was last updated**, and its **update interval**. A pre-rendered static
map built from a frozen snapshot is misleading on that score unless the
snapshot date is shown. Because the feed has no `feed_info.txt`, **neither
value exists inside the downloaded data**, so both must be recorded at download
time or they cannot be displayed honestly.

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

⚠️ **The OpenStreetMap notice at item 1 does NOT discharge this.** Both sources
are ODbL, so one credit looks as if it should cover both, but §4.3 requires the
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
that must carry the notice is unresolved. ⚠️ **Corrected 2026-09-29:** this
entry first said that, unlike Paris, there was **no publisher gloss** to lean
on; there is one, since the National Access Point's Conditions Particulières
apply to every ODbL dataset it lists (`docs/licenses/odbl-toulouse-rennes.md`).
**Cheap discharge: put the ODbL notice on the station CSV** rather than try to
win the argument.

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
naming *STAR* on the map is not barred. An automated check re-reads the terms
for changes (`star-cgu-still-clean`).

⚠️ **OPEN — the station CSV under §4.4**, exactly as for Tisséo:
`outputs/rennes/excluded_stations.csv` is left in the same state as Toulouse's,
and the same cheap discharge is available if the question is ever pressed.

**27. Brønnøysundregistrene (Oslo, Bergen) — required, and DISPLAYED.**

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

**28. Kartverket (Oslo, Bergen) — required, and DISPLAYED.**

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

**29. Entur (Oslo, Bergen) — required, and DISPLAYED, with its logo.** Bergen (2026-09-29) adds Skyss's feed through the same host and licence, and its page shows the same logo beside the same credit.

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

**30. Det Centrale Virksomhedsregister (Copenhagen, Aarhus, Odense) — required, and DISPLAYED.** Aarhus (2026-09-29) reads the same download (generation 505) and Odense (2026-09-30) reads the register too, so the credit names both; the owner approved each widening, Odense's on 2026-09-30.

**CC BY 4.0**, from CVR's own terms on Datafordeler
(`datafordeler.dk/vejledning/brugervilkaar/det-centrale-virksomhedsregister-cvr/`,
read 2026-09-23): *"Du skal kreditere Det Centrale Virksomhedsregister (CVR) på
et passende sted."* The name is prescribed and the wording is not, so the
notice is this project's own, approved by the owner 2026-09-24; its second
sentence is CC BY 4.0 3(a)(1)'s duty to indicate modification. Only the entity
`CVRPerson` is access-restricted and this project never asks for it. **MUST
DO: nothing** - no notification, no registration of the reuse. The account is
the owner's and closes after Copenhagen publishes<!-- internal --> (`docs/gated_access.md` item
3)<!-- /internal -->; closing is licence-safe, since the grant attaches to the data.

**31. Klimadatastyrelsen (Copenhagen, Aarhus, Odense) — required, and DISPLAYED.** Aarhus (2026-09-29) reads DAR's Adresse and Husnummer (generation 761) and takes each point from OpenStreetMap's copy, so the notice also names OpenStreetMap's points for Aarhus, owner-approved. Odense (2026-09-30) is placed the same way and the notice names it, approved by the owner 2026-09-30.

**CC BY 4.0**, from DAR's terms on Datafordeler
(`datafordeler.dk/vejledning/brugervilkaar/danmarks-adresseregister-dar/`,
"Vilkår for brug af Danmarks Adresseregister (DAR) - (16.05.2024)", read
2026-09-24): free to fetch, share and adapt, with
credit to **Klimadatastyrelsen**. Klimadatastyrelsen's own terms page lets the
reuser choose the form of the credit; the notice names the register as well,
because Datafordeler's general terms ask for "the responsible register". The
2022 SDFI terms PDF still linked from Dataforsyningen's product cards
prescribed a dated credit sentence and is SUPERSEDED for data fetched after 16
May 2024 - not to be followed. **MUST DO: nothing.**

**32. Czech Statistical Office (Prague, Brno, Plzeň, Olomouc, Ostrava, Liberec, Most) — required, and DISPLAYED.**

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

**33. ČÚZK (Prague, Brno, Plzeň, Olomouc, Ostrava, Liberec, Most) — required, and DISPLAYED.**

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

**40. CBS (Rotterdam, Den Haag) — required, and DISPLAYED.**

**CC BY 4.0** (`cbs.nl/nl-nl/over-ons/website/copyright`, read 2026-09-24): credit
CBS, link the licence, and say when a figure is recalculated. Rotterdam's page
quotes the shop-vacancy share from the Landelijke Monitor Leegstand 2025, table 1
(430 of 6,060 shop units, 1 January 2025), as "about one in fourteen" - a rounding
of CBS's counts, which the notice says. **MUST NOT SAY**: that CBS produced or
endorses the map; no CBS logo. KOOP's notices (Auteurswet art. 11, CC0 declared),
the BAG (Public Domain Mark) and the national feed (CC0) need no notice. Wording
approved by the owner 2026-09-24. **MUST DO: nothing.**
- **Den Haag (added with the tram cities, 2026-09-30)**: its page quotes the same table (180 of 4,480 shop units, GM0518, 1 January 2025) as "about one in twenty-five"; the displayed notice names both cities.

**41. FEHD / DATA.GOV.HK / CSDI (Hong Kong) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** The registers under DATA.GOV.HK's Terms of Use v1.2 (read
2026-09-22), FEHD's points under the CSDI Portal's terms (read 2026-09-24): identify the
source, acknowledge the Government's and FEHD's intellectual property, attribute the
Government, FEHD and DATA.GOV.HK, and name the CSDI Portal as a source - one paragraph. Both
carry the uncapped indemnity the owner accepted (see "Hong Kong's indemnity"). Wording
approved by the owner 2026-09-24. <!-- internal -->**MUST DO:** `check_personal_exposure.py hong_kong`, run
2026-09-24 (the verdict is in `DECISIONS.md`).<!-- /internal --> MTR's station lists (used only to check the
station count) and the Address Lookup Service (ALS, a cross-check) are not published and need no notice.

**42. VZD (Riga, Liepāja, Daugavpils) — required, and DISPLAYED.** Liepāja and Daugavpils (added with the tram cities, 2026-09-30) each use their own cadastral map and VZD's State Address Register (`aw_eka.csv`). The notice names both, with VZD's own source wording for the address register ("Izmantoti Valsts adrešu reģistra informācijas sistēmas dati, 2026. gads") and the changes made; approved by the owner 2026-09-30.

**PERMITTED WITH CONDITIONS.** CC BY 4.0, adopted by VZD's own data-use rules
(`vzd.gov.lv/lv/par-datu-izmantosanas-noteikumiem`<!-- internal -->, read 2026-09-24 by the licence-read
agent<!-- /internal -->): credit the source, link the licence, and describe the changes made - VZD asks
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
a condition of the licence (§三(二)), in the annex's prescribed form, plus the FIA's own declaration: cite
the source, no emblems, no implied endorsement, and do not present the filtered points as the
register - the notice says what was selected and changed. **National**: each Taiwanese city
adds its name to this notice rather than a second one. Wording approved by the owner
2026-09-25. <!-- internal -->**MUST DO:** `check_personal_exposure.py taichung` (the name-rule test), run
2026-09-25 (the verdict is in `DECISIONS.md`).<!-- /internal -->

**45. Taichung City Government and Taichung MRT (Taichung) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS.** OGDL v1 on both<!-- internal --> (read 2026-09-25 by the `licence-read`
agent)<!-- /internal -->: the door plates' 提供機關 is 臺中市政府數位發展局 (renamed from 數位治理局 in
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
2026-09-27. <!-- internal -->**MUST DO:** `check_personal_exposure.py daegu`, run 2026-09-27 (the verdict is in
`DECISIONS.md`).<!-- /internal --> **If Daegu objects, the page comes down.**

**49. Busan Metropolitan City (Busan) — required, and DISPLAYED.**

**PERMITTED WITH CONDITIONS** (read 2026-09-27; the reasoning is under "Daegu and Busan"
above): a reasonable source credit under the portal's own 공공데이터 이용정책 (저작권법 제37조, no
wording prescribed), and good-faith use. The terms' 제14조 is read as covering only works the
platform itself authored (owner-accepted). The credit names the Ministry's local-government
licensing data as the source, Big-데이터웨이브 (linked) and its 구군 인허가포털 Open API as the
channel, the fourteen permit types and **the frozen snapshot's date (2026-04-15)**, with Seoul's
describe-the-changes line and a non-endorsement line. Wording approved by the owner 2026-09-27.
**MUST DO:** never read or publish `sitetel`, the telephone field (the build refuses to load it)<!-- internal -->;
`check_personal_exposure.py busan`, run 2026-09-27 (the verdict is in `DECISIONS.md`)<!-- /internal -->. Any
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
owner 2026-09-27. <!-- internal -->**MUST DO:** `check_personal_exposure.py kobe` with its Japan pass (the
operator's own name is never shown as a trade name), run 2026-09-27; the verdict is in
`DECISIONS.md`.<!-- /internal -->

**51. Réseau express métropolitain (Montréal) — required, and DISPLAYED** (written
into `render_site_notices()` 2026-09-27, wording approved by the owner; displayed
since the tram batch landed, as the REM maps are).
Added 2026-09-27 with the tram rescope, which draws the REM from its own GTFS.
**PERMITTED WITH CONDITIONS** (CC BY 4.0, from the licence file bundled in the feed;
the reasoning is in `docs/data_sources/canada.md`): credit **Réseau express
métropolitain (REM)**, state that the data was modified, link the CC BY 4.0 licence; no
wording prescribed. **MUST NOT:** imply endorsement or official status (§2(a)(6)); use the
REM logo (§2(b)(2)). Remove the credit if the REM asks (§3(a)(3)). The displayed credit
does all three, naming the three modifications (services drawn as one line, stations
outside the agglomeration removed, two merged with same-named Métro stations), and
disclaims endorsement. The STM credit beside it (13) still reads "Métro
route geometry", which stays true.

**52. Osaka City and MLIT (Osaka) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since Osaka landed, after Kobe).

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
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py osaka` with its Japan pass, run
  2026-09-27: 0 operator names shown, 9 withheld. The verdict is in
  `DECISIONS.md`.<!-- /internal -->

**53. Sapporo City and MLIT (Sapporo) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since Sapporo landed).

- **PERMITTED WITH CONDITIONS** (read 2026-09-24; the registers' package re-read
  2026-09-28; the Japan rows in [`data_sources/japan.md`](data_sources/japan.md)).
- **Sapporo City's two datasets are CC BY 4.0** (`package_show`: CC-BY-4.0 on
  both). The platform is the city's own (`data.pf-sapporo.jp/tos/`, in force
  2024-06-01) and defers to each dataset's licence; its 第9条3 compensation
  clause was accepted by the owner 2026-09-24.
- **The credit**: 札幌市, both dataset titles and URLs, the licence link and that
  the data was processed (no wording is prescribed<!-- internal -->; the brief's example form<!-- /internal -->),
  with every URL an explicit link.
- **MLIT's 位置参照情報 and N02** are PDL 1.0, credited as in 50. N03 (CC BY
  4.0) only picks stations and is **never drawn**.
- **MUST NOT**: imply endorsement; use city logos (第4条); call the pins
  operating businesses. **Fetch from `ckan.pf-sapporo.jp` only.**
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py sapporo` with its Japan pass, run
  2026-09-28: 0 operator names shown, 6 withheld (7 pins). The verdict is in
  `DECISIONS.md`.<!-- /internal -->

**54. Fukuoka City, MHLW and MLIT (Fukuoka) — required, and DISPLAYED** (written
into `render_site_notices()`; displayed since Fukuoka landed).

- **PERMITTED WITH CONDITIONS**, two licences (read 2026-09-24; BODIK's
  `package_show` re-read 2026-09-28; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)).
- **The city's four lists on BODIK are CC BY 4.0** through the city's own terms
  (`https://odcs.bodik.jp/401307/tos/` 第１条; `package_show` records `cc-by`).
  **MUST DISPLAY (第７条)**: each dataset's 作成者 as recorded (food 保健医療局
  食品安全推進課; barber and beauty 福岡市保健福祉局; laundry 保健福祉局 生活衛生課),
  the resource name with its date, the resource URL, the licence link and that
  the data was modified. The resource names come from `config.RESOURCE_NAMES`,
  the files used.
- **MHLW's open data is PDL 1.0** (the system's site terms §2). **MUST DISPLAY**
  the source, that it was processed and by whom and how (重要情報 1.1), linking
  the top page only. **MUST NOT** present it as MHLW's own, use its logo, claim
  the list complete, or imply accuracy: the notice says it holds only filings
  whose applicants agreed to publish them. The minor 2)ウ point stays open (the
  project is non-commercial, fine under both readings).
- **MLIT's 位置参照情報 and N02** are PDL 1.0, credited as in 50. N03 (CC BY
  4.0) only picks stations and is **never drawn**.
- Both cost clauses are the fault-based class the owner accepted 2026-09-24.
- **MUST NOT**: imply endorsement; use city or ministry logos; call the pins
  operating businesses.
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py fukuoka` with its Japan pass, run
  2026-09-28: 0 operator names shown; 4 trade names that are the operator's
  own name, shown by permit type on 5 pins. MHLW's rows cannot be tested (no
  individual-operator column; owner accepted 2026-09-28). The verdict is in
  `DECISIONS.md`.<!-- /internal -->

**55. Kyoto City and MLIT (Kyoto) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since Kyoto landed).

- **PERMITTED WITH CONDITIONS** (read 2026-09-24; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)).
- **The City's three datasets (00414, 00541, 00530) are CC BY 4.0**, 著作権者
  京都市, on every dataset and resource page; the portal's 京都市オープンデータ利用規約
  (第3版) applies each dataset's own licence. No click-through.
- **MUST DISPLAY**: 京都市 as the creator; the name **京都市オープンデータ**, which
  the portal asks for (binding through CC §3(a)(1)(A)(i)); the dataset names
  and URLs; CC BY 4.0 linked; that the data was processed - here, a register
  REBUILT from the monthly lists, pinned at 2026-07-31.
- **MLIT's 位置参照情報 and N02** are PDL 1.0, credited as in 50. N03 (CC BY
  4.0) only picks stations and is **never drawn**.
- **MUST NOT**: imply the City's endorsement; use its emblem or logos; describe
  the pins as operating businesses - closures are invisible in a rebuilt
  register, and the page says it is an upper bound. **Fetch from
  `data.city.kyoto.lg.jp` only.**
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py kyoto` with its Japan pass, run
  2026-09-28: 0 operator names shown; 21 trade names that are the operator's
  own name in the raw lists, 8 pins showing their permit type. The verdict is
  in `DECISIONS.md`.<!-- /internal -->

**56. Tokyo's wards, MHLW and MLIT (Tokyo) — required, and DISPLAYED** (written
into `render_site_notices()`, its businesses part BUILT from
`pipeline/tokyo/credits.py`; displayed since Tokyo landed).

- **PERMITTED WITH CONDITIONS** (read 2026-09-24; the Tokyo rows in
  [`data_sources/japan.md`](data_sources/japan.md)). Eight wards, each its own
  publisher, and each credited in the form its own terms prescribe:
  - **the Tokyo catalogue's ward files** (Chuo, Minato, Shinjuku and Koto's
    food lists; Minato's, Taito's and Shibuya's barber, beauty and laundry
    registers): ONE combined notice with each ward, the catalogue, each
    dataset title and URL, the **date of use**, that the data was processed,
    and CC BY 4.0 linked (Tokyo Open Data Terms §2);
  - **Shibuya's food list**: 渋谷区オープンデータ利用規約 §2's pattern for
    modified use, CC BY 4.0 linked;
  - **Taito's food list**: the ward's four elements - 台東区, CC-BY表示4.0国際
    linked, 本作品の内容について、台東区は一切保証しないものとする。, the page URL -
    plus that it was modified; the link says it goes to 台東区公式ホームページ;
  - **Setagaya's food list**: the §2 「…改変して利用しています」 form, with the
    page URL;
  - **Meguro's food lists and registers**: each resource title with its date,
    目黒区, CC BY 4.0, that it was modified, and the catalogue link labelled
    目黒区オープンデータカタログサイト;
  - **MHLW's open data** for Chuo, Minato, Shinjuku and Koto: PDL 1.0, as in
    54 (the source, processed, the top page only, no completeness claim).
- **Every file the roster reads has a credit**<!-- internal -->: `check_provenance.py` refuses a
  file in `pipeline/tokyo/wards.py` without an entry in `credits.py`, so a ward
  switched on later cannot reach the page uncredited<!-- /internal -->.
- **MLIT's 位置参照情報 and N02** are PDL 1.0, credited as in 50. N03 (CC BY
  4.0) only picks stations and is **never drawn**.
- **MUST NOT**: imply any ward's, the Tokyo Metropolitan Government's, MHLW's
  or MLIT's endorsement; use a ward logo; describe the pins as operating
  businesses. Shinjuku: never link its PDF list (the site's linking rule; the
  credit links the catalogue page). Shibuya: re-read its terms before each
  republish (they may change without notice).
- Cost clauses: Tokyo §6, Setagaya §4, Meguro 第8項, Taito's through Tokyo §6 -
  the fault-based class the owner accepted 2026-09-24. Shibuya has none.
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py tokyo` with its Japan pass, run
  2026-09-28: 0 operator names shown; 4 trade names that are the operator's
  own name in the raw lists, 2 pins showing their permit type. The lists
  without an individual-operator column cannot be tested (owner accepted
  2026-09-28, disclosed on the page). The verdict is in `DECISIONS.md`.<!-- /internal -->

**57. VBB Verkehrsverbund Berlin-Brandenburg (Berlin) — required, and DISPLAYED**
(written into `render_site_notices()`; displayed since Berlin landed).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-28; <!-- /internal -->the Berlin rows in
  [`data_sources/germany.md`](data_sources/germany.md)). VBB's GTFS is CC BY
  4.0 per VBB's own dataset page (`unternehmen.vbb.de/digitale-services/
  datensaetze/`; Berlin's CKAN says an unversioned `cc-by`). The credit VBB
  requests is "VBB Verkehrsverbund Berlin-Brandenburg GmbH" (CKAN's
  `attribution_text`); CC BY 4.0 adds the licence link, a statement of
  modification and a reference to the disclaimer VBB supplies ("kann Fehler
  enthalten und/oder unvollständig sein").
- **MUST NOT**: imply the map is official VBB information or endorsed by VBB
  (§2(a)(6)); use VBB's, BVG's or S-Bahn Berlin's logos or line signets
  (trademarks, not licensed). VBB's website terms (private use only) govern its
  web pages, not the datasets, and nothing from those pages is reproduced.
- **IHK Berlin's register needs no notice**: CC0 1.0 on the CSV channel used
  (dl-de/zero-2.0 on the WFS), neither with any condition. The page carries a
  courtesy credit, "Business data: IHK Berlin (CC0)" (owner, 2026-09-28), and
  no IHK logo (CC0 §4(a) releases no trademark).
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py berlin`, run 2026-09-28: the
  register has no name column of any kind, so 0 pins can show a person's name;
  every pin's title is one of 208 IHK branch labels. The verdict is in
  `DECISIONS.md`.<!-- /internal -->

**58. Food Standards Agency (London) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since London landed).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-28; <!-- /internal -->the London rows in
  [`data_sources/united-kingdom.md`](data_sources/united-kingdom.md)). The FSA's
  terms put its FHRS data under the **Open Government Licence v3**: the OGL
  statement ("Contains public sector information licensed under the Open
  Government Licence v3.0.") with a link to the licence; the date the
  information was updated (each borough's extract date, 2026-09-09 to
  2026-09-16 at the first fetch, on the page and in the notice). No rating,
  score, FSA imagery or logo is shown, so the imagery conditions do not reach
  the map. **Credit wording (owner, 2026-09-28)**: "Food Standards Agency, UK
  food hygiene rating data" - "the FHRS name" may not be used outside its
  imagery without permission.
- **Personal data (owner, 2026-09-28)**: the FSA's privacy notice treats a
  business's name and address as personal data and the OGL does not license
  it; the project's existing rule applies - home and mobile caterers are out by
  type, a private-address record (no point, outward postcode only) is never
  placed, a trading-as name shows the name on the shop.
- **MUST NOT**: imply official status or FSA endorsement (OGL); use the FSA
  logo; display a rating.
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py london`, run 2026-09-28: no fallback
  name exists, 0 contact details; the verdict is in `DECISIONS.md`.<!-- /internal -->
- **London's rail is OpenStreetMap data** (ODbL, notice 1): the basemap credit
  covers its stations and track too.

**59. Ordnance Survey (London) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since London landed).

- **PERMITTED WITH CONDITIONS**<!-- internal --> (`licence-read` 2026-09-28)<!-- /internal -->: OS Code-Point Open
  under the **Open Government Licence v3**; the licence file shipped in the zip
  (`Doc/licence.txt`) redirects to OGL v3 and carries the statements OS's terms
  name as required: "Contains Ordnance Survey data © Crown copyright and
  database right 2026." "Contains Royal Mail data © Royal Mail copyright and
  database right 2026." "Contains National Statistics data © Crown copyright
  and database right 2026." OS says derived data (a premises placed at a
  postcode centroid) is credited. OGL link; no endorsement.
- **Used for** 2,349 London food storefronts the FSA lists with a full postcode
  and no point (3.9% of storefront rows); never a private address.
- **MUST NOT**: imply OS endorsement; use the OS logo; use "Code-Point" (a
  registered OS mark - trademarks are outside the OGL) in the credit.
- **The repository carries the credit too** (owner, 2026-09-28): committed
  `outputs/london/` republishes the derived locations, so README's credits and
  `data_sources/united-kingdom.md` state the three lines. OS's 48 MB third-party
  style guide was not read (owner: skip); the notice displays inline and
  legibly on every page, as every credited source's does.
- Wording approved by the owner 2026-09-28.

**60. Gobierno de la Ciudad de Buenos Aires (Buenos Aires) — required, and
DISPLAYED** (written into `render_site_notices()`; displayed since Buenos Aires
landed).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-28 for the survey and
  Parcelas; <!-- /internal -->the SBASE dataset page read 2026-09-28 declares the same
  CC-BY-2.5-AR; the Buenos Aires rows in
  [`data_sources/argentina.md`](data_sources/argentina.md)). **Creative Commons
  Attribution 2.5 Argentina**: credit to the Gobierno de la Ciudad de Buenos
  Aires / BA Data and each author unit (DG Antropología Urbana, Subsecretaría de
  Planeamiento; Subsecretaría de Registro, Interpretación y Catastro;
  Subterráneos de Buenos Aires, SBASE), each dataset's title and URI, the
  licence URI, and a sentence on how the data was changed.
- **Versions disagree** (the datasets say 2.5 AR, the survey's resources an
  unversioned `cc-by`, Parcelas' resources 4.0): the one credit satisfies 2.5 AR
  and 4.0 both, and the data is never described as "CC BY 4.0" alone.
- **MUST NOT**: use a GCBA or BA Data logo; imply endorsement. If the city asks
  for its credit to be removed, remove it (s.4(a)).<!-- internal -->
- **MUST DO:** `check_personal_exposure.py buenos_aires`, run 2026-09-28: the
  survey carries no name column; pins read as the street address (owner); the
  verdict is in `DECISIONS.md`.<!-- /internal -->
- **Station names follow OpenStreetMap** (ODbL, notice 1), matched to SBASE's
  points; the credit says so.
- Wording approved by the owner 2026-09-28.

**61. Food Standards Scotland (Glasgow) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since Glasgow landed).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-28; <!-- /internal -->the Glasgow rows in
  [`data_sources/united-kingdom.md`](data_sources/united-kingdom.md)). Glasgow
  City Council runs Scotland's **Food Hygiene Information Scheme** (FHIS), not
  England's FHRS. The FSA's terms put the whole open-data file, FHIS records
  included, under the **Open Government Licence**, and Food Standards Scotland
  publishes the same council's data itself under "Open Government Licence
  (v3)". The OGL statement with a link to the licence; the date the information
  was updated (the file's extract date, 2026-09-14). No result ("Pass",
  "Improvement Required"), logo or imagery is shown.
- **Credit wording (owner, 2026-09-28)**: "Food Standards Scotland, Food Hygiene
  Information Scheme data, via the Food Standards Agency" - FSS runs the scheme
  and licenses its own copy, the FSA distributes the file this project reads.
  **Never "FHRS"** for Scotland: it is a different scheme, and the FSA's terms
  bar "the FHRS name" outside its imagery.
- **Personal data (owner, 2026-09-28)**: FSS's FHIS privacy notice counts the
  operator's name and address as personal information, and the OGL does not
  license it. Glasgow City lists home bakers and cooks as cafés at their flat,
  with a point, so two rules were added to London's: a storefront at a "Flat"
  address is never placed (185), nor one named as a childminder (5).
- **MUST NOT**: imply official status or endorsement by FSS or the FSA (OGL);
  use either body's logo; display a result.
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py glasgow`, run 2026-09-28: no
  fallback name exists, 0 contact details; the verdict is in `DECISIONS.md`.<!-- /internal -->
- **Glasgow's rail is OpenStreetMap data** (ODbL, notice 1).

**58 (Food Standards Agency, London) amended the same day (owner, 2026-09-28)**: its "Modified by this project"
adds "premises at a flat address left out" - London's map applies the flat rule
(98 storefronts).

**62. Food Standards Agency (Newcastle) — required, and DISPLAYED** (written
into `render_site_notices()`; displayed since Newcastle landed).

- **PERMITTED WITH CONDITIONS**, London's reading (notice 58<!-- internal -->, the
  `licence-read` of 2026-09-28<!-- /internal -->): the five Tyne and Wear councils are on
  England's FHRS, under the **Open Government Licence v3** with the FSA's
  conditions. The OGL statement linked; each council's extract date
  (2026-09-09 to 2026-09-16); no rating, logo or imagery. **Credit (owner,
  2026-09-28)**: London's, "Food Standards Agency, UK food hygiene rating
  data", as a notice of its own rather than by extending 58.
- **Personal data**: the project's rule as for London: home and mobile
  caterers out by type, a private address never placed, a storefront at a
  "Flat" address (5) or named as a childminder (0) never placed, the trade name
  shown after "trading as".
- **MUST NOT**: imply official status or FSA endorsement (OGL); use the FSA
  logo; display a rating.
- Wording approved by the owner 2026-09-28.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py newcastle`, run 2026-09-28: no
  fallback name exists, 0 contact details; the verdict is in `DECISIONS.md`.<!-- /internal -->
- **Newcastle's rail is OpenStreetMap data** (ODbL, notice 1).

**63. Ordnance Survey (Newcastle) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since Newcastle landed).

- **PERMITTED WITH CONDITIONS**<!-- internal -->, London's `licence-read`<!-- /internal --> (notice 59): the same
  Code-Point Open file and edition (2026-08), copied from London's cache, not
  downloaded again. The three statements verbatim, the OGL link, no
  endorsement, the product's registered name not used.
- **Used for** 634 Newcastle food storefronts the FSA lists with a full
  postcode and no point (9.5% of storefront rows); never a private address.
  Units kept to the five districts' GSS codes.
- **The repository carries the credit too**, as for London: committed
  `outputs/newcastle/` republishes the derived locations (README's credits).
- Wording approved by the owner 2026-09-28.

**64. City of Sydney (Sydney) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since Sydney landed).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-28; <!-- /internal -->the Sydney rows in
  [`data_sources/australia.md`](data_sources/australia.md)): the FES item's
  `licenseInfo` links **CC BY 4.0**, credit "City of Sydney"; the data hub's
  disclaimer says data products carry the licence named in their description.
  Data.NSW's harvested copy says "License Not Specified", a harvester failure;
  the publisher's item governs.
- **MUST DISPLAY** (CC BY §3(a)(1)): the City of Sydney as creator and
  copyright holder, the licence linked, the dataset linked, that the data was
  modified, and the warranty disclaimer. No wording is prescribed; the
  licence read's draft, approved by the owner 2026-09-28, with the survey year.
- **MUST NOT**: imply endorsement or official status (§2(a)(6)); present the
  data as accurate, current or complete on the City's authority.
- **Noted, not a blocker (owner, 2026-09-28)**: the City's main website terms
  (`cityofsydney.nsw.gov.au/terms-conditions`) bar republishing its content
  without written authorisation; the read judged them written for that site's
  pages and not incorporated by the data hub, where Creative Commons governs.
- **MUST DO:** nothing to the publisher. <!-- internal -->`check_personal_exposure.py sydney`,
  run 2026-09-28: the survey has no names, so no pin can show one; the verdict
  is in `DECISIONS.md`.<!-- /internal -->
- **Sydney's rail is OpenStreetMap data** (ODbL, notice 1).

**65. City of Melbourne (Melbourne) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed since Melbourne landed).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-28; <!-- /internal -->the Melbourne rows
  in [`data_sources/australia.md`](data_sources/australia.md)): the portal's
  "About our data" puts its open data under CC BY 4.0, and the dataset's
  metadata declares `license: "CC BY"` with the 4.0 legal code. DataVic's
  "other-open" is CKAN's generic bucket and carries the same CC BY text; the
  council's portal governs. Nothing is incorporated by reference (the portal's
  terms page is undefined; `melbourne.vic.gov.au/copyright` covers the website).
- **MUST DISPLAY** (CC BY §3(a)): a credit, the licence linked, the dataset
  linked, a note that the data was modified. No wording is prescribed; the
  licence read's draft, approved by the owner 2026-09-28, with the census year.
- **MUST NOT**: imply endorsement (§2(a)(6)); use DataVic's "© Copyright State
  Government of Victoria" (DataVic's own material).
- **MUST DO:** nothing to the publisher ("#melbdata" is an invitation).
  Privacy is not licensed (§2(b)(1))<!-- internal -->: `check_personal_exposure.py melbourne`,
  run 2026-09-28, finds only trading names and no fallback; the verdict is in
  `DECISIONS.md`<!-- /internal -->.
- **Melbourne's rail is OpenStreetMap data** (ODbL, notice 1).

**66. Stockholms stad (Stockholm) — displayed by choice, not required**
(written into `render_site_notices()`; displayed since Stockholm landed).

- **SILENT, with the pages named** (resolved 2026-09-22; the Stockholm rows in
  [`data_sources/sweden.md`](data_sources/sweden.md)): the ArcGIS item's
  `licenseInfo` is empty and it serves without credentials; `dataportal.se`
  says "Begränsad" but is a harvester; the publisher's own Hub DCAT feed says
  `accessLevel: public` on all 109 datasets and carries CC0 on 8 of them, not
  this one. Where a catalogue and its publisher disagree, the publisher's word
  decides<!-- internal --> (this project's licence-reading rule)<!-- /internal -->.
- **MUST DISPLAY**: nothing is prescribed. The notice credits the publisher,
  says no licence is stated, names the changes and disclaims endorsement,
  without claiming a licence the city did not grant (Amsterdam's SILENT
  register was displayed as CC BY by the owner's choice; this one is not).
  Wording approved by the owner 2026-09-29.
- **MUST NOT**: present the map as the official register, or imply Stockholms
  stad produced or endorses it.
- **MUST DO**: nothing. <!-- internal -->`brief_check.py stockholm` re-reads the Hub feed; if it
  changes, the verdict is re-argued.<!-- /internal --> <!-- internal -->Privacy: `check_personal_exposure.py
  stockholm`, run 2026-09-29, finds only premises names and no fallback; the
  verdict is in `DECISIONS.md`.<!-- /internal -->
- **Stockholm's rail, boundary and naming layer are OpenStreetMap data** (ODbL,
  notice 1).

**67. DSVSA București (Bucharest) — displayed by choice, not required**
(written into `render_site_notices()`; displayed since Bucharest landed).

- **SILENT, with the pages named** (read in the browser 2026-09-23; the
  Bucharest rows in [`data_sources/romania.md`](data_sources/romania.md)):
  `bucuresti.dsvsa.ro` has no terms-of-use page, only cookie and privacy
  pages; the privacy policy says nothing of reuse; DSVSA's data is not on
  `data.gov.ro`. The ANSVSA footer "Toate drepturile rezervate" is a website
  footer, which governs site content, not the data (the New York situation).
- **MUST DISPLAY**: nothing is prescribed. The notice credits the publisher,
  says no licence is stated, names the changes (including the name rule and
  the address placement) and disclaims endorsement. Wording approved by the
  owner 2026-09-29.
- **MUST NOT**: present the map as the official register, or imply DSVSA or
  ANSVSA produced or endorses it.
- **MUST DO**: nothing to the publisher. The owner downloads the files in
  their own browser (a condition of the city's screening memo); the clearance
  cookie the site's browser check sets is never reused by a script. <!-- internal -->Privacy:
  `check_personal_exposure.py bucharest`, run 2026-09-29; the verdict is in
  `DECISIONS.md`.<!-- /internal -->
- **Bucharest's rail, boundary, sectors and address points are OpenStreetMap
  data** (ODbL, notice 1).

**68. Small Enterprise and Market Service (Incheon, Goyang, Seongnam, Yongin, Suwon, Bucheon, Namyangju, Ansan, Uijeongbu, Anyang) — required, and DISPLAYED**
(written into `render_site_notices()`; displayed since Incheon landed).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-29; <!-- /internal -->the rows in
  [`data_sources/south-korea.md`](data_sources/south-korea.md)): data.go.kr
  15083033 declares 이용허락범위 제한 없음 in the page, Schema.org and DCAT, set
  by SEMAS as provider, and SEMAS names data.go.kr as its release channel.
  data.go.kr's FAQs 210 and 186: commercial use and processing allowed; the
  factual content must not be falsified or distorted.
- **Reasoned position (owner, 2026-09-29), as for Daegu**: SEMAS's website
  copyright policy asks for a consultation before using material without a
  KOGL mark; read as covering the homepage's content, since the dataset carries
  the publisher's own no-restriction label. Any objection is honoured. The
  소상공인365 notices the listing cites are unread (IP-blocked from here).
- **MUST DISPLAY**: a source credit, no wording prescribed; the categories and
  counts stated as this project's (FAQ 186).
- **MUST NOT**: present the counts as SEMAS's figures, or the data as accurate
  or complete on SEMAS's behalf (its legal notice disclaims both).
- **MUST DO**: nothing.

**69. TaM (Montpellier) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on France's National Access Point for "Réseau
urbain TaM" (Montpellier Méditerranée Métropole), under the NAP's Conditions
Particulières (DECISIONS "French tram feeds read", 2026-09-29).

**MUST DISPLAY**, verbatim - ODbL §4.3's own template with the database named:

> Contains information from Réseau urbain TAM, which is made available here
> under the Open Database License (ODbL).

(as written in `render_site_notices()`, "Réseau urbain TaM"). It names only the
stations: the feed has no `shapes.txt`, so the line geometry is OpenStreetMap's,
under notice 1. **MUST DO**: keep the station table a pure extract (the owner's
rule, 2026-09-29); §4.6 is met by the linked public repository. **MUST NOT**:
use the TaM logo.

**70. M réso (Grenoble) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on the NAP for "Réseau urbain TAG", published
by the SMMAG ("M", the Syndicat Mixte des Mobilités de l'Aire Grenobloise), under
the NAP's Conditions Particulières; the SMMAG adopted the same narrowing on its
own licence page (read from its Wayback copy of 2025-03-15, as its live copy is
empty). **MUST DISPLAY**, verbatim - §4.3 with the database named:

> Contains information from Réseau urbain TAG, which is made available here
> under the Open Database License (ODbL).

It names the stations and the line geometry, both redrawn from the feed. **MUST
DO**: the station table stays a pure extract; §4.6 by the repository.

**71. LiA (Le Havre) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on the NAP for "Réseau urbain LiA" (Le Havre
Seine Métropole), under the NAP's Conditions Particulières. **MUST DISPLAY**,
verbatim - §4.3 with the database named:

> Contains information from Réseau urbain LiA, which is made available here
> under the Open Database License (ODbL).

It names only the stations. The feed has no shapes and no colours: the line
geometry is OpenStreetMap's (notice 1), and the colours are the project's own,
since LiA's website terms claim its colour scheme (licence read 2026-09-29). The
Normandie aggregate's LiA shapes, stop-to-stop lines, are not used, so the
aggregate's licence question for LiA's data does not arise<!-- internal --> (`DECISIONS.md`,
the France build entries)<!-- /internal -->. **MUST DO**: a pure-extract station
table; §4.6 by the repository.

**72. City of Ottawa (Ottawa) — required, and DISPLAYED**
(written into `render_site_notices()`; displayed, landed 2026-09-30).

- **PERMITTED WITH CONDITIONS** (read 2026-09-29; the Ottawa rows in
  [`data_sources/canada.md`](data_sources/canada.md)): Ottawa Public Health's
  inspection feed and the City's 2022-2026 wards both carry the Open Government
  Licence – City of Ottawa v2.0 in their `licenseInfo`.
- **MUST DISPLAY**, verbatim and linked to the licence: "Contains information
  licensed under the Open Government Licence – City of Ottawa." The notice also
  credits Ottawa Public Health / City of Ottawa and states the changes.
- **MUST NOT**: suggest official status or endorsement, or use the City's or
  OPH's names as marks. Personal information is outside the grant (MFIPPA)<!-- internal -->:
  `check_personal_exposure.py ottawa`, run 2026-09-29, finds premises names only;
  the verdict is in `DECISIONS.md`<!-- /internal -->.
- **MUST DO**: nothing. The item says the feed "will be retired in Q1 2026";
  the cached copy stays licensed as accessed.
- **Ottawa's rail is OpenStreetMap data** (ODbL, notice 1).

**73. Region of Waterloo (Kitchener–Waterloo) — displayed by choice, not required**
(written into `render_site_notices()`; displayed, landed 2026-09-30).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-30; <!-- /internal -->the
  Kitchener–Waterloo rows in [`data_sources/canada.md`](data_sources/canada.md)):
  the food and personal-services inspection layers (items
  `61a7a8d8775e4da381d9718658c0d842`, `d96eeb0cd02e4b45ba52bc1a918c6218`) and the
  Cities and Towns layer (`369f39237bf844e3abcf39d71947ee49`) name the **Region of
  Waterloo Open Data Licence** in their `licenseInfo` (heading "v.2.0"; its body
  says "version 1.0"; undated; OGL-UK via British Columbia's). The cited URL,
  `https://www.regionofwaterloo.ca/en/regional-government/open-data.aspx#Open-Data-Licence`,
  now answers 404; the licence is at `https://www.regionofwaterloo.ca/government-and-council/transparency-and-accountability/open-data/`, and a Wayback copy of the old URL
  (2026-04-14) diffs identical.
- **The bulk tables (`Inspections.zip`, `Inspections_PS.zip`; items
  `b79414c31d93490c811c5a9979634fec`, `beb380d01149451dad08a04ebf19fdc3`) name no
  licence**: `licenseInfo` null, and the Hub shows Esri's "No License Provided /
  Request permission to use". **Owner's reading, 2026-09-30:** the Region's own
  open-data page says "By downloading the data on the portal, you are agreeing to
  the Open Data License below", which covers every portal download, so the
  tables are used under the same licence. Any objection from the Region is
  honoured.
- **MUST DISPLAY**: nothing. Credit is optional, but the licence prescribes the
  sentence if one is given, and it is displayed verbatim: "Contains information
  provided by the Regional Municipality of Waterloo under licence".
- **MUST NOT**: suggest official status or endorsement, or misrepresent the data
  or its source. The layers' descriptions add that the results are what an
  inspector observed on the day and that no endorsement of any premises is
  implied, so the page shows no results and says a pin is not a rating.
  Personal information is outside the grant (MFIPPA)<!-- internal -->:
  `check_personal_exposure.py kitchener_waterloo`, run 2026-09-30, finds 0
  person-like names at a residential unit; the verdict is in `DECISIONS.md`<!-- /internal -->.
- **MUST DO**: nothing.
- **Kitchener–Waterloo's rail is OpenStreetMap data** (ODbL, notice 1).

**74. Govern de les Illes Balears and Dirección General del Catastro (Palma) — required, and DISPLAYED**
(written into `render_site_notices()`; displayed, landed 2026-09-30).

- **PERMITTED WITH CONDITIONS** (read 2026-09-29, the owner's three calls; the
  Palma rows in [`data_sources/spain.md`](data_sources/spain.md)): the
  Consell de Mallorca's register on the GOIB catalogue (`cc-by`; GOIB's terms,
  CC BY 3.0 ES) and Catastro's INSPIRE Addresses for Palma (CC BY 4.0 DG
  Catastro).
- **MUST DISPLAY**: "Font de les dades: Govern de les Illes Balears", the
  author, the title, the licence link, the dataset URI, the register's last
  update (2026-09-07) and that the data were modified; Catastro named as
  author and owner, CC BY 4.0 linked, the join stated, the access date.
- **MUST NOT**: imply that GOIB, the Consell or Catastro endorses the map, or
  present it as Catastro information. <!-- internal -->`check_personal_exposure.py palma`, run
  2026-09-30: trade names only (`Explotador/s` never read); the verdict is in
  `DECISIONS.md`.<!-- /internal -->
- **MUST DO**: nothing required; GOIB "urges" projects to tell it (not done:
  a courtesy, like Barcelona's, recorded).
- **Palma's rail is OpenStreetMap data** (ODbL, notice 1).

**75. Yokohama City and MLIT (Yokohama) — required, and DISPLAYED** (written
into `render_site_notices()` 2026-09-30, after Tokyo's; displayed, landed
2026-09-30).

- **PERMITTED WITH CONDITIONS** (<!-- internal -->`licence-read` 2026-09-30; <!-- /internal -->the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's barber, beauty
  and laundry registers are **CC BY 4.0**, declared on the dataset page
  (`https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/seikatsu/kaiteki/kankyodata.html`)
  and through the city's open-data terms. MLIT's 位置参照情報 and N02 are **PDL
  1.0**, each with its own credit line, as in Kobe's (50). N03 (CC BY 4.0) is
  credited although it only picks stations and is **never drawn** (the Survey
  Act).
- **MUST DISPLAY**: the city's own form for a modified work -
  `この地図は、以下の著作物を改変して利用しています。環境衛生関係施設一覧（理容所・美容所・クリーニング所施設一覧、令和８年４月１日現在）、神奈川県横浜市、クリエイティブ・コモンズ・ライセンス 表示4.0 国際（https://creativecommons.org/licenses/by/4.0/deed.ja）`
  - with an English gloss saying what was modified, and the dataset page linked.
  - **As rendered** (owner, 2026-09-30, call B5): the site places the dataset
    page's URL in brackets after 神奈川県横浜市, inside the prescribed sentence.
    Accepted as displayed: the link adds to the credit and changes none of
    its words.
- **MUST NOT**: present the map as the city's work; imply its endorsement; say
  the pins are businesses open now (the registers record no closures).
- <!-- internal -->**MUST DO:** `check_personal_exposure.py yokohama` with its Japan pass (the
  operator's own name is never shown as a trade name), run 2026-09-30; the
  verdict is in `DECISIONS.md` ("Yokohama built", 2026-09-30).<!-- /internal --> Contact for removals: ir-seikatsueisei@city.yokohama.lg.jp.

**76. Hiroshima City, MHLW and MLIT (Hiroshima) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-09-30, after Tokyo's; displayed,
landed 2026-09-30).

- **PERMITTED WITH CONDITIONS** (read 2026-09-24; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's full list is
  **PDL 1.0** through the city's open-data list (DataEye dataset 5672), and the
  website terms give way to it; the owner accepted that reading for the
  full-list file on 2026-09-24. MHLW's open data is **PDL 1.0**, as in
  Fukuoka's (54). MLIT's 位置参照情報 and N02 (the 2025 edition) are **PDL 1.0**,
  as in Kobe's (50). N03 (CC BY 4.0) only picks stations and is **never
  drawn** (the Survey Act).
- **MUST DISPLAY**: DataEye's pattern,
  `出典：「食品営業許可一覧」（広島広域都市圏・広島県オープンデータポータルサイト）（https://hiroshima-opendata.dataeye.jp/datasets/5672）を加工して作成`,
  and who did the processing (PDL 1.0); MHLW's source and processed-by credit,
  linking its top page only; MLIT's credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos; claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py hiroshima` with its Japan pass (the
  operator's own name is never shown as a trade name), run 2026-09-30; the
  verdict is in `DECISIONS.md` ("Hiroshima built", 2026-09-30).<!-- /internal -->

**77. Angers Loire Métropole (Angers) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on the NAP for Angers Loire Métropole's
network dataset (`6178cee254e3b3f0744a1318`), under the NAP's Conditions
Particulières (DECISIONS "French tram feeds read", 2026-09-29). **Built
MARK-FREE** (owner, 2026-09-30): the Métropole's terms say its network's marks
"and any other mark" of the service may not be used or mentioned in anything
built from the data without its prior agreement, and ODbL §2.3(c) leaves marks
outside the licence. The dataset's NAP title carries that brand, so the notice
names the database by its producer and its NAP id, which §4.3 permits (a notice
"reasonably calculated" to make the reader aware of the source). **MUST
DISPLAY**:

> Contains information from Angers Loire Métropole's public transport
> timetable database (transport.data.gouv.fr dataset
> 6178cee254e3b3f0744a1318), which is made available here under the Open
> Database License (ODbL).

It names the stations and the line geometry, both from the feed's own
`shapes.txt`. **MUST DO**: a pure-extract station table; §4.6 by the
repository. **MUST NOT**: show the network brand anywhere on the page, the
macro map, the caption or this notice (the feed's `feed_publisher_name` and
`agency_name` carry it). If the Métropole objects, the removal rule applies.

**78. KORDIS JMK (Brno) — required, and DISPLAYED** (written into
`render_site_notices()`; displayed, landed 2026-09-30).

- **PERMITTED WITH CONDITIONS, CC BY 4.0** (read 2026-09-30, the rows in
  [`data_sources/czechia.md`](data_sources/czechia.md)): KORDIS's own "Otevřená
  data (GTFS)" block on `idsjmk.cz/a/kontakty.html` grants CC BY 4.0, and
  data.brno.cz lists the byte-identical file as CC-BY-4.0. idsjmk.cz's BY-NC-SA
  footer covers only its web pages. The file is fetched from `kordis-jmk.cz`
  (owner, 2026-09-30), under KORDIS's own grant.
- **MUST DISPLAY**: KORDIS JMK, a.s. and DPMB, as the feed's `agency.txt`
  credits them ("IDS JMK (Data from: KORDIS JMK, DPMB)", which CC BY
  §3(a)(1)(A) says to retain); data.brno.cz (the Statutory City of Brno) as the
  distributor; CC BY 4.0, linked; a link to the feed; the changes. The wording
  was approved by the owner on 2026-09-30, word for word.
- **MUST NOT**: imply endorsement, or use the IDS JMK, KORDIS or DPMB logos.
- **MUST DO**: nothing.

**79. PMDP (Plzeň) — displayed on the stricter reading** (written into
`render_site_notices()`; displayed, landed 2026-09-30).

- **PERMITTED** (read 2026-09-30): PMDP's GTFS record contradicts itself, CC BY
  in the description against no-rights terms on the distribution, and either
  permits use. **Used only to check the stop list** - the stop names each tram
  line serves on an ordinary weekday; nothing from it is drawn.
- **MUST DISPLAY (stricter reading)**: the credit<!-- internal --> from the city's build brief<!-- /internal -->,
  "Plzeňské městské dopravní podniky, a.s. (PMDP), GTFS published by the
  Statutory City of Plzeň at opendata.plzen.eu, CC BY 4.0, modified by this
  project"; the sentence around it is the build's own wording, flagged for the
  owner's review.
- **MUST NOT**: the city's coat of arms or PMDP's logo; any implied endorsement.
- **MUST DO**: nothing.

**32 and 33 widened in the same change.** The ČSÚ and ČÚZK notices' text names
no city, so their titles list each Czech city as it lands (owner, 2026-09-30),
as Norway's and Denmark's do. Their text is unchanged.

**80. City of Kansas City, Missouri (Kansas City) — required, and DISPLAYED**
(written into `render_site_notices()` with the tram cities, 2026-09-30, first as
69 and renumbered 80 in landing order; displayed, landed 2026-09-30.)

- **PERMITTED WITH CONDITIONS, and one owner decision** (<!-- internal -->`licence-read`
  2026-09-30; <!-- /internal -->the rows in [`data_sources/united-states.md`](data_sources/united-states.md)).
  KCMO Code § 2-2134(a) (Ord. 150865, 2015) requires every portal dataset to be
  "explicitly placed into the public domain, thereby ensuring that there are no
  restrictions or requirements placed on use", and `kkhs-93m4` and its parent
  `pnm4-68wg` both declare Public Domain - the City's choice, not a portal
  default (142 of the portal's 202 datasets carry no licence).
- **MUST DISPLAY**: the portal's Data Terms of Use (`data.kcmo.org/terms`,
  undated) prescribe a disclaimer paragraph "at the site where the software
  application ... can be accessed" - Chicago's wording on the same portal
  template, so it is displayed site-wide, as Chicago's is. Reproduced word for
  word, including `www.data.kcmo.gov`, a host that does not resolve (the
  portal is data.kcmo.org). Displayed whichever document controls: it costs
  nothing.
- **The indemnity - DECIDED by the owner (2026-09-30): the ordinance
  controls.** The same terms say any user "shall indemnify and hold harmless the
  City from any claim ... that arises directly or indirectly ... from that
  user's use of this data". The owner took the reading that KCMO Code
  § 2-2134(a)'s "no restrictions or requirements placed on use" overrides the
  undated terms page (the dataset is declared public domain, the ordinance backs
  it, and no step asks for acceptance), so it binds nothing here - unlike
  RideKC's GTFS, whose terms the site itself imposes. Kansas City is cleared to
  land. The disclaimer above is displayed regardless.
- **MUST NOT**: use City marks (the terms reserve them); present the data as
  the City's current or accurate record (the disclaimer above says otherwise,
  and the register is frozen at 2026-01-15).
- **MUST DO**: check for Finance-department data terms before a republish
  (the terms incorporate them; none found).

**81. City of Tucson (Tucson) — required, and DISPLAYED** (written into
`render_site_notices()` with the tram cities, 2026-09-30, first as 70 and
renumbered 81 in landing order; displayed, landed 2026-09-30.)

- **SILENT, read as permitted by the owner (2026-09-30)**: the BUSLIC layer's
  `licenseInfo` is an accuracy disclaimer only - nothing grants and nothing
  restricts - and the hub invites building applications. The owner took the
  permissive reading over two sibling City disclaimers (DTM Map Center, PDSD
  PRO) that add "for your personal use", which the item does not incorporate.
  Rows in [`data_sources/united-states.md`](data_sources/united-states.md).
- **MUST DISPLAY**: "Business licence data: City of Tucson." (the owner's
  wording, the condition of the permissive reading).
- **MUST NOT**: present the pins as complete - the layer's own words, "should
  not be considered a complete listing of all active businesses in Tucson".
  The page quotes it.
- **MUST DO**: nothing. A.R.S. 39-121.03 (commercial use of public records)
  does not reach a non-commercial portfolio; it would if the project became
  commercial.

**82. Comune di Firenze (Florence) — required, and DISPLAYED** (written into
`render_site_notices()` with the tram cities, 2026-09-30, first as 71 and
renumbered 82 in landing order; displayed, landed 2026-09-30.)

- **PERMITTED WITH CONDITIONS, CC BY 4.0**<!-- internal --> (the brief's licence read,
  2026-09-30)<!-- /internal -->: the Comune's own Note legali ("I materiali Open data sono
  liberamente riutilizzabili...") and CC BY 4.0 on every dataset and
  distribution. The Regione's dati.toscana.it only harvests the layers and is
  owed nothing. Rows in [`data_sources/italy.md`](data_sources/italy.md).
- **MUST DISPLAY**: credit the Comune di Firenze (Direzione Attività Economiche
  e Turismo), link CC BY 4.0, and state the changes (filtered, categorised,
  aggregated) - no wording prescribed; Milan's notice 23 (Comune di Milano) is the model.
- **MUST NOT**: imply the Comune's endorsement, or use its logo or the giglio.
- **MUST DO**: nothing. The Comune's footer ties reuse of personal data to
  d.lgs. 36/2006; the layers carry no name or address.

**83. Gemeente Den Haag (Den Haag) — required, and DISPLAYED** (written into
`render_site_notices()` with the tram cities, 2026-09-30, first as 72 and
renumbered 83 in landing order; displayed, landed 2026-09-30.)

- **SILENT and ambiguous; the owner proceeds on Amsterdam's precedent
  (2026-09-30).** Databankenwet art. 8(2): a public body's database is
  unprotected unless the right is expressly reserved, and nothing on the layer,
  its web map or app reserves it; against that, denhaag.nl's site terms name
  database rights. Rows in [`data_sources/netherlands.md`](data_sources/netherlands.md).
- **MUST DISPLAY**: the credit "Gemeente Den Haag" (the owner's condition).
  The notice text was approved by the owner 2026-09-30 (call C1).
- **MUST NOT**: call the layer current or complete (the page gives its last
  edit, 23 May 2025); imply the city's endorsement.
- **MUST DO**: never download `AANVRAGER`, `KVKNUMMER` or `RECHTSVORM` -
  `fetch_sources.py` names its fields and stops if one arrives.

**84. Food Standards Agency (Manchester) — required, and DISPLAYED** (written
into `render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS**, London's reading (notice 58): the seven
  Metrolink districts' councils are on England's FHRS, under the **Open
  Government Licence v3** with the FSA's conditions. The OGL statement linked;
  each council's extract date (2026-10-02); no rating, logo or imagery. The
  credit is London's and Newcastle's, "Food Standards Agency, UK food hygiene
  rating data", as a notice of its own (Newcastle's precedent, notice 62).
- **Personal data**: the project's rule as for London: home and mobile
  caterers out by type, a private address never placed, a storefront at a
  "Flat" address (10) or named as a childminder (0) never placed, the trade
  name shown after "trading as".
- **MUST NOT**: imply official status or FSA endorsement (OGL); use the FSA
  logo; display a rating.
- Wording: Newcastle's Food Standards Agency notice 62, with the city and
  date changed.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py manchester`, run 2026-10-02: no
  fallback name exists, 0 contact details; the verdict is in the session's
  drafts file, `docs/decisions_drafts/uk-six.md`.<!-- /internal -->
- **Manchester's rail is OpenStreetMap data** (ODbL, notice 1).

**85. Ordnance Survey (Manchester) — required, and DISPLAYED** (written into
`render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS** (notice 59): the same Code-Point Open file and
  edition (2026-08), copied from London's cache, not downloaded again. The
  three statements verbatim, the OGL link, no endorsement, the product's
  registered name not used.
- **Used for** 673 Manchester food storefronts the FSA lists with a full
  postcode and no point (5.4% of storefront rows); never a private address.
  Units kept to the seven districts' GSS codes.
- **The repository carries the credit too**, as for London: committed
  `outputs/manchester/` republishes the derived locations (README's credits).
- Wording: Newcastle's Ordnance Survey notice 63, with the city changed.

**86. Department for Transport, NaPTAN (United Kingdom) — required, and
DISPLAYED** (written into `render_site_notices()` with the UK six,
2026-10-02.)

- **PERMITTED WITH CONDITIONS**<!-- internal --> (`licence-read`, 2026-10-02)<!-- /internal -->: NaPTAN, the
  National Public Transport Access Nodes dataset, is published under the
  **Open Government Licence v3.0** (the publisher's own terms page,
  `beta-naptan.dft.gov.uk/terms-conditions`; data.gov.uk's record says the
  same). No separate terms on the API (`naptan.api.dft.gov.uk`), and no
  attribution of the Department's own, so the OGL's default applies.
- **Used for** gate 3 of the UK tram and light-rail cities: each map's stops
  are matched name by name against NaPTAN's active stop areas (stop type MET,
  ATCO area 940) inside its scope. Nothing from NaPTAN is drawn on a map.
- **MUST DISPLAY**: "Contains public sector information licensed under the
  Open Government Licence v3.0.", with the licence linked. Whether a count
  checked against the data needs the credit at all is arguable; displaying it
  is the cautious reading.
- **MUST NOT**: imply the Department's endorsement (OGL); use a DfT logo or
  the Royal Arms; present NaPTAN as complete.
- Wording approved by the owner 2026-10-02.

**87. Food Standards Agency (Birmingham) — required, and DISPLAYED** (written
into `render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS**, London's reading (notice 58): the three
  councils West Midlands Metro serves are on England's FHRS, under the **Open
  Government Licence v3** with the FSA's conditions. The OGL statement linked;
  each council's extract date (2026-10-02); no rating, logo or imagery. The
  credit is London's and Newcastle's, "Food Standards Agency, UK food hygiene
  rating data", as a notice of its own (Newcastle's precedent, notice 62).
- **Personal data**: the project's rule as for London: home and mobile
  caterers out by type, a private address never placed, a storefront at a
  "Flat" address (53) or named as a childminder (0) never placed, the trade
  name shown after "trading as".
- **MUST NOT**: imply official status or FSA endorsement (OGL); use the FSA
  logo; display a rating.
- Wording: Newcastle's Food Standards Agency notice 62, with the city and
  date changed.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py birmingham`, run 2026-10-02: no
  fallback name exists, 0 emails or phone numbers; the verdict is in the
  session's drafts file, `docs/decisions_drafts/uk-six.md`.<!-- /internal -->
- **Birmingham's rail is OpenStreetMap data** (ODbL, notice 1).

**88. Ordnance Survey (Birmingham) — required, and DISPLAYED** (written into
`render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS** (notice 59): the same Code-Point Open file and
  edition (2026-08), copied from London's cache, not downloaded again. The
  three statements verbatim, the OGL link, no endorsement, the product's
  registered name not used.
- **Used for** 433 Birmingham food storefronts the FSA lists with a full
  postcode and no point (4.4% of storefront rows); never a private address.
  Units kept to the three districts' GSS codes.
- **The repository carries the credit too**, as for London: committed
  `outputs/birmingham/` republishes the derived locations (README's credits).
- Wording: Newcastle's Ordnance Survey notice 63, with the city changed.

**89. Food Standards Scotland (Edinburgh) — required, and DISPLAYED** (written
into `render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS**, Glasgow's reading (notice 61): the City of
  Edinburgh Council runs Scotland's **Food Hygiene Information Scheme** (FHIS),
  not England's FHRS. The FSA's terms put the whole open-data file, FHIS records
  included, under the **Open Government Licence**, and Food Standards Scotland
  publishes the same council's data itself under "Open Government Licence
  (v3)". The OGL statement with a link to the licence; the date the information
  was updated (the file's extract date, 2026-10-02). No result ("Pass",
  "Improvement Required"), logo or imagery is shown.
- **Credit wording**: Glasgow's, "Food Standards Scotland, Food Hygiene
  Information Scheme data, via the Food Standards Agency". **Never "FHRS"** for
  Scotland.
- **Personal data**: Glasgow's rules: home and mobile caterers out by type, a
  private address never placed, a storefront at a "Flat" address (0) or named
  as a childminder (0) never placed, the trade name shown after "trading as".
- **MUST NOT**: imply official status or endorsement by FSS or the FSA (OGL);
  use either body's logo; display a result.
- Wording: Glasgow's Food Standards Scotland notice 61, with the city and date
  changed and the centroid clause of Manchester's Food Standards Agency
  notice 84 added.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py edinburgh`, run 2026-10-02: no
  fallback name exists, 0 contact details; the verdict is in the session's
  drafts file, `docs/decisions_drafts/uk-six.md`.<!-- /internal -->
- **Edinburgh's rail is OpenStreetMap data** (ODbL, notice 1).

**90. Ordnance Survey (Edinburgh) — required, and DISPLAYED** (written into
`render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS** (notice 59): the same Code-Point Open file and
  edition (2026-08), copied from London's cache, not downloaded again. The
  three statements verbatim, the OGL link, no endorsement, the product's
  registered name not used.
- **Used for** 57 Edinburgh food storefronts the FSA lists with a full
  postcode and no point (1.4% of storefront rows); never a private address.
  Units kept to the City of Edinburgh's GSS code (S12000036).
- **The repository carries the credit too**, as for London: committed
  `outputs/edinburgh/` republishes the derived locations (README's credits).
- Wording: Newcastle's Ordnance Survey notice 63, with the city changed.<!-- internal -->
- **Kept by the owner (2026-10-02):** Edinburgh keeps the centroid tier, the
  kit's rule, over Glasgow's precedent of none.<!-- /internal -->

**91. Food Standards Agency (Sheffield) — required, and DISPLAYED** (written
into `render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS**, London's reading (notice 58): Sheffield City
  Council is on England's FHRS, under the **Open Government Licence v3** with
  the FSA's conditions. The OGL statement linked; the council's extract date
  (2026-10-02); no rating, logo or imagery. The credit is London's and
  Newcastle's, "Food Standards Agency, UK food hygiene rating data", as a
  notice of its own (Newcastle's precedent, notice 62).
- **Personal data**: the project's rule as for London: home and mobile
  caterers out by type, a private address never placed, a storefront at a
  "Flat" address (4) or named as a childminder (0) never placed, the trade
  name shown after "trading as".
- **MUST NOT**: imply official status or FSA endorsement (OGL); use the FSA
  logo; display a rating.
- Wording: Newcastle's Food Standards Agency notice 62, with the city and
  date changed.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py sheffield`, run 2026-10-02: no
  fallback name exists, 0 contact details; the verdict is in the session's
  drafts file, `docs/decisions_drafts/uk-six.md`.<!-- /internal -->
- **Sheffield's rail is OpenStreetMap data** (ODbL, notice 1).

**92. Ordnance Survey (Sheffield) — required, and DISPLAYED** (written into
`render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS** (notice 59): the same Code-Point Open file and
  edition (2026-08), copied from London's cache, not downloaded again. The
  three statements verbatim, the OGL link, no endorsement, the product's
  registered name not used.
- **Used for** 70 Sheffield food storefronts the FSA lists with a full
  postcode and no point (2.0% of storefront rows); never a private address.
  Units kept to the city's GSS code (E08000039).
- **The repository carries the credit too**, as for London: committed
  `outputs/sheffield/` republishes the derived locations (README's credits).
- Wording: Newcastle's Ordnance Survey notice 63, with the city changed.

**93. Food Standards Agency (Nottingham) — required, and DISPLAYED** (written
into `render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS**, London's reading (notice 58): the four
  councils NET serves (the City of Nottingham, Broxtowe, Rushcliffe and
  Ashfield) are on England's FHRS, under the **Open Government Licence v3**
  with the FSA's conditions. The OGL statement linked; each council's extract
  date (2026-10-01 to 2026-10-02); no rating, logo or imagery. The credit is
  London's and Newcastle's, "Food Standards Agency, UK food hygiene rating
  data", as a notice of its own (Newcastle's precedent, notice 62).
- **Personal data**: the project's rule as for London: home and mobile
  caterers out by type, a private address never placed, a storefront at a
  "Flat" address (4) or named as a childminder (1) never placed, the trade
  name shown after "trading as".
- **MUST NOT**: imply official status or FSA endorsement (OGL); use the FSA
  logo; display a rating.
- Wording: Newcastle's Food Standards Agency notice 62, with the city and
  date changed.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py nottingham`, run 2026-10-02: no
  fallback name exists, 0 contact details; the verdict is in the session's
  drafts file, `docs/decisions_drafts/uk-six.md`.<!-- /internal -->
- **Nottingham's rail is OpenStreetMap data** (ODbL, notice 1).

**94. Ordnance Survey (Nottingham) — required, and DISPLAYED** (written into
`render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS** (notice 59): the same Code-Point Open file and
  edition (2026-08), copied from London's cache, not downloaded again. The
  three statements verbatim, the OGL link, no endorsement, the product's
  registered name not used.
- **Used for** 97 Nottingham food storefronts the FSA lists with a full
  postcode and no point (2.6% of storefront rows); never a private address.
  Units kept to the four council areas' GSS codes.
- **The repository carries the credit too**, as for London: committed
  `outputs/nottingham/` republishes the derived locations (README's credits).
- Wording: Newcastle's Ordnance Survey notice 63, with the city changed.

**95. Food Standards Agency (Blackpool) — required, and DISPLAYED** (written
into `render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS**, London's reading (notice 58): Blackpool's
  and Wyre's councils are on England's FHRS, under the **Open Government
  Licence v3** with the FSA's conditions. The OGL statement linked; each
  council's extract date (2026-10-02); no rating, logo or imagery. The credit
  is London's and Newcastle's, "Food Standards Agency, UK food hygiene rating
  data", as a notice of its own (Newcastle's precedent, notice 62).
- **Personal data**: the project's rule as for London: home and mobile
  caterers out by type, a private address never placed, a storefront at a
  "Flat" address (4) or named as a childminder (0) never placed, the trade
  name shown after "trading as".
- **MUST NOT**: imply official status or FSA endorsement (OGL); use the FSA
  logo; display a rating.
- Wording: Newcastle's Food Standards Agency notice 62, with the city and
  date changed.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py blackpool`, run 2026-10-02: no
  fallback name exists, 0 contact details; the verdict is in the session's
  drafts file, `docs/decisions_drafts/uk-six.md`.<!-- /internal -->
- **Blackpool's rail is OpenStreetMap data** (ODbL, notice 1).

**96. Ordnance Survey (Blackpool) — required, and DISPLAYED** (written into
`render_site_notices()` with the UK six, 2026-10-02.)

- **PERMITTED WITH CONDITIONS** (notice 59): the same Code-Point Open file and
  edition (2026-08), copied from London's cache, not downloaded again. The
  three statements verbatim, the OGL link, no endorsement, the product's
  registered name not used.
- **Used for** 67 Blackpool and Wyre food storefronts the FSA lists with a
  full postcode and no point (3.8% of storefront rows); never a private
  address. Units kept to the two councils' GSS codes.
- **The repository carries the credit too**, as for London: committed
  `outputs/blackpool/` republishes the derived locations (README's credits).
- Wording: Newcastle's Ordnance Survey notice 63, with the city changed.

**97. Matsuyama City, MHLW and MLIT (Matsuyama) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's five lists are
  **CC BY 4.0** through its open-data site's terms (第2条). MHLW's open data is
  **PDL 1.0**, as in Fukuoka's (54). MLIT's 位置参照情報 and N02 (the 2025
  edition) are **PDL 1.0**, as in Kobe's (50). N03 (CC BY 4.0) only picks
  stations and is **never drawn** (the Survey Act).
- **MUST DISPLAY**: the city's form for a modified work,
  `この地図は以下の著作物を改変して利用しています。食品営業許可全施設一覧、理容所全施設一覧、美容所全施設一覧、クリーニング所全施設一覧、松山市、クリエイティブ・コモンズ・ライセンス 表示 4.0（https://creativecommons.org/licenses/by/4.0/）`
  (the city's open-data logo may not stand in for it); MHLW's source and
  processed-by credit, linking its top page only; MLIT's credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos; claim MHLW's list is complete or accurate; uses against
  public order or national security (the city's 第4条).<!-- internal -->
- **MUST DO:** `check_personal_exposure.py matsuyama` with its Japan pass,
  run 2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Matsuyama built", 2026-10-02).<!-- /internal -->


**98. Toyama City, MHLW and MLIT (Toyama) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's four lists are
  **CC BY 4.0** through its CKAN's terms (第１条１). MHLW's open data is
  **PDL 1.0**, as in Fukuoka's (54), and is used for its points only. MLIT's
  位置参照情報 and N02 (the 2025 edition) are **PDL 1.0**, as in Kobe's (50). N03
  (CC BY 4.0) only picks stations and is **never drawn** (the Survey Act).
- **MUST DISPLAY**: the portal's form for edited content,
  `この地図は以下の著作物を改変して利用しています。食品営業許可施設、理容営業許可施設、美容営業許可施設、クリーニング営業許可施設、富山市、クリエイティブ・コモンズ・ライセンス 表示4.0国際（https://creativecommons.org/licenses/by/4.0/）`;
  MHLW's source and processed-by credit, linking its top page only; MLIT's
  credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos (第３条); claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py toyama` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Toyama built", 2026-10-02).<!-- /internal -->

**99. Kumamoto City, MHLW and MLIT (Kumamoto) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The restaurant list is
  **PDL 1.0** under the city's catalogue terms; the barber, beauty and laundry
  lists are **CC BY 4.0** on their pages and PDL 1.0 on BODIK. MHLW's open data
  is **PDL 1.0**, as in Fukuoka's (54). MLIT's 位置参照情報 and N02 (the 2025
  edition) are **PDL 1.0**, as in Kobe's (50). N03 (CC BY 4.0) only picks
  stations and is **never drawn** (the Survey Act).
- **MUST DISPLAY**: the catalogue's form,
  `「熊本市_食品衛生法に基づく飲食店営業許可施設一覧」（熊本市オープンデータカタログサイト）をもとに作成`, and
  likewise the three lists, with who processed them and the CC BY 4.0 link;
  MHLW's source and processed-by credit, linking its top page only; MLIT's
  credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos; claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py kumamoto` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Kumamoto built", 2026-10-02).<!-- /internal -->

**100. Fukui City and MLIT (Fukui) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-01 and 2026-10-02; the Japan rows
  in [`data_sources/japan.md`](data_sources/japan.md)). The city's lists are
  **CC BY-SA** (the site policy's default, no version named). **Share-alike
  accepted (owner, 2026-10-01): `outputs/fukui/` is offered under CC BY-SA 4.0**
  (`LICENSE`). MLIT's 位置参照情報 and N02 (the 2025 edition) are **PDL 1.0**, as
  in Kobe's (50). N03 (CC BY 4.0) only picks stations and is **never drawn**.
  No MHLW credit: its file is not used.
- **MUST DISPLAY**: 福井市, both list titles with their page URLs, CC BY-SA,
  and that the data was processed; the offer of the Fukui outputs under CC
  BY-SA 4.0; MLIT's credit lines.
- **MUST NOT**: imply the city's endorsement; claim accuracy on the city's
  authority.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py fukui` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Fukui built", 2026-10-02).<!-- /internal -->

**101. Nagasaki City, MHLW and MLIT (Nagasaki) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's four BODIK
  lists are **CC BY 4.0** under its catalogue terms. MHLW's open data is
  **PDL 1.0**, as in Fukuoka's (54). MLIT's 位置参照情報 and N02 (the 2025
  edition) are **PDL 1.0**, as in Kobe's (50). N03 (CC BY 4.0) only picks
  stations and is **never drawn** (the Survey Act).
- **MUST DISPLAY**: CC BY 4.0's attribution for the four lists (each title,
  長崎市, the licence link, the URL, processed); MHLW's source and
  processed-by credit, linking its top page only; MLIT's credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use the
  city's logo alone; claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py nagasaki` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Nagasaki built", 2026-10-02).<!-- /internal -->

**102. Utsunomiya City, MHLW and MLIT (Utsunomiya) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's five lists are
  **CC BY** (no version) on the catalogue and **PDL 1.0** under the portal's
  terms, either of which permits this use. MHLW's open data is **PDL 1.0**, as
  in Fukuoka's (54). MLIT's 位置参照情報 and N02 (the 2025 edition) are **PDL
  1.0**, as in Kobe's (50). N03 (CC BY 4.0) only picks stations and is **never
  drawn** (the Survey Act).
- **MUST DISPLAY**: the portal's pattern for each list,
  `「食品営業許可施設一覧」（宇都宮市）（<dataset URL>）を加工して作成`, likewise
  理容所一覧, 美容所一覧, クリ－ニング(取次)一覧 and クリ－ニング(一般)一覧, with who
  processed them; MHLW's source and processed-by credit, linking its top page
  only; MLIT's credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos; claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py utsunomiya` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Utsunomiya built", 2026-10-02).<!-- /internal -->

**103. Kitakyushu City, MHLW and MLIT (Kitakyushu) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's three BODIK
  lists are **CC BY 4.0** under its catalogue terms (第1条). MHLW's open data is
  **PDL 1.0**, as in Fukuoka's (54). MLIT's 位置参照情報 and N02 (the 2025
  edition) are **PDL 1.0**, as in Kobe's (50). N03 (CC BY 4.0) only picks
  stations and is **never drawn** (the Survey Act).
- **MUST DISPLAY** (第6条): each list's organisation, its resource name and URL,
  the licence link, and that it was processed; MHLW's source and processed-by
  credit, linking its top page only; MLIT's credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos; claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py kitakyushu` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Kitakyushu built", 2026-10-02).<!-- /internal -->

**104. Sakai City, MHLW and MLIT (Sakai) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's food-permit
  list and its monthly files are **CC BY 4.0** through the 堺市オープンデータ利用規約
  (3-2). MHLW's open data is **PDL 1.0**, as in Fukuoka's (54). MLIT's 位置参照情報
  and N02 (the 2025 edition) are **PDL 1.0**, as in Kobe's (50). N03 (CC BY 4.0)
  only picks stations and is **never drawn** (the Survey Act).
- **MUST DISPLAY**: the city's form for a modified work (3-3),
  `この地図は以下の著作物を改変して利用しています。堺市 食品営業許可施設一覧（令和8年4月1日現在、令和8年4月分から8月分の許可施設及び廃業施設）、堺市、クリエイティブ・コモンズ・ライセンス 表示 4.0 国際（https://creativecommons.org/licenses/by/4.0/deed.ja）`;
  MHLW's source and processed-by credit, linking its top page only; MLIT's
  credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos; claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py sakai` with its Japan pass,
  run 2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Sakai built", 2026-10-02).<!-- /internal -->

**105. Hakodate City and MLIT (Hakodate) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's registers are
  **CC BY 2.1 JP**, declared on the list page. MLIT's 位置参照情報 and N02 (the
  2025 edition) are **PDL 1.0**, as in Kobe's (50). N03 (CC BY 4.0) only picks
  stations and is **never drawn** (the Survey Act). e-Stat's 衛生行政報告例 was
  used as a measurement only and is not drawn.
- **MUST DISPLAY**: `出典：「環境衛生関係施設等の情報」（函館市）（https://www.city.hakodate.hokkaido.jp/docs/2019072900024/）を加工して作成`,
  © Hakodate City and the CC BY 2.1 JP link; MLIT's credit lines.
- **MUST NOT**: present the map as the city's work; imply its endorsement; say
  the pins are businesses open now. **If the city asks, remove its credit**
  (CC BY 2.1 JP art. 5).<!-- internal -->
- **MUST DO:** `check_personal_exposure.py hakodate` with its Japan pass,
  run 2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Hakodate built", 2026-10-02).<!-- /internal -->

**106. Kagoshima City, MHLW and MLIT (Kagoshima) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's old-law list is
  **CC BY 4.0** under its open-data terms. MHLW's open data is **PDL 1.0**, as
  in Fukuoka's (54). MLIT's 位置参照情報 and N02 (the 2025 edition) are **PDL
  1.0**, as in Kobe's (50). N03 (CC BY 4.0) only picks stations and is **never
  drawn** (the Survey Act).
- **MUST DISPLAY**: the city's prescribed credit for a processed work,
  `この地図は以下の著作物を改変して利用しています。「食品営業許可全施設一覧」、鹿児島市、CCBY4.0（https://creativecommons.org/licenses/by/4.0/deed.ja）`;
  MHLW's source and processed-by credit, linking its top page only; MLIT's
  credit lines.
- **MUST NOT**: present processed data as the city's or MHLW's own; use city or
  ministry logos; claim MHLW's list is complete or accurate.<!-- internal -->
- **MUST DO:** `check_personal_exposure.py kagoshima` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Kagoshima built", 2026-10-02).<!-- /internal -->

**107. MHLW and MLIT (Okayama) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). Okayama's businesses come
  from MHLW's open data alone, **PDL 1.0**, as in Fukuoka's (54). MLIT's
  位置参照情報 and N02 (the 2025 edition) are **PDL 1.0**, as in Kobe's (50).
  N03 (CC BY 4.0) only picks stations and is **never drawn** (the Survey Act).
  The city's own pages are not used (their default reserves reuse).
- **MUST DISPLAY**: MHLW's source and processed-by credit, linking its top
  page only; MLIT's credit lines.
- **MUST NOT**: present processed data as MHLW's own; use the ministry's logo;
  claim its list is complete or accurate (its fields are opt-in).<!-- internal -->
- **MUST DO:** `check_personal_exposure.py okayama` with its Japan pass, run
  2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Okayama built", 2026-10-02).<!-- /internal -->

**108. Kōchi City and MLIT (Kōchi) — required, and DISPLAYED**
(written into `render_site_notices()` 2026-10-02; lands with the Japan batch
at review time).

- **PERMITTED WITH CONDITIONS** (read 2026-10-02; the Japan rows in
  [`data_sources/japan.md`](data_sources/japan.md)). The city's lists are **CC BY
  4.0** through the page's open-data rule and the 高知市オープンデータ利用規約.
  MLIT's 位置参照情報 and N02 (the 2025 edition) are **PDL 1.0**, as in Kobe's
  (50). N03 (CC BY 4.0) only picks stations and is **never drawn** (the Survey
  Act).
- **MUST DISPLAY**: `出典：「理容所一覧」「美容所一覧」（高知市）（https://www.city.kochi.kochi.jp/soshiki/36/opendata.html）を加工して作成`,
  with who processed it and the CC BY 4.0 link; MLIT's credit lines.
- **MUST NOT**: present processed data as if the city made it; use the city's
  symbols, logos or characters; say the pins are businesses open now (closures
  since March are not published).<!-- internal -->
- **MUST DO:** `check_personal_exposure.py kochi` with its Japan pass,
  run 2026-10-02; the verdict is in `docs/decisions_drafts/japan-batch.md`
  ("Kōchi built", 2026-10-02).<!-- /internal -->
**109. Public Health – Seattle & King County (Seattle (Regional)) — required, and DISPLAYED**
(written into `render_site_notices()` with Seattle (Regional), 2026-10-02; the
session's claimed block, 109–116.)

- **Read as permitted by the owner (2026-10-01, option 1)**: the inspection
  dataset (`r878-4sxa`) is declared Public Domain and the portal's Open Data
  terms (archived 2023) granted reuse; the live site-wide kingcounty.gov terms
  forbid publishing without written permission. Rows in
  [`data_sources/united-states.md`](data_sources/united-states.md).
- **MUST DISPLAY**: the publisher's attribution "Public Health – Seattle & King
  County", and the Open Data terms' legend "Data provided by permission of King
  County", since the permissive reading rests on those terms.
- **MUST NOT**: use King County's logo or marks, or imply endorsement; take
  `CTYNAME`, `POSTALCTYNAME` or the ZIP fields from the County's address points
  (they come from the USPS ZIP+4 product).
- **MUST DO**: nothing further. The removal rule is the safety net.

**110. Washington State Liquor and Cannabis Board (Seattle (Regional)) — required, and DISPLAYED**
(written into `render_site_notices()` with Seattle (Regional), 2026-10-02.)

- **PERMITTED WITH CONDITIONS**: no license and no terms of use exist; the
  lists page notes that records received through the Public Records Act "may
  not be used for commercial purposes" (RCW 42.56.070(8)). This project is
  non-commercial (owner, 2026-10-02).
- **MUST DISPLAY**: the list's date, and, while it stands on the Board's lists
  page, the Board's notice that its list reports "contain possible errors due
  to a known data transfer issue" (owner, 2026-10-02: "yes").
- **MUST NOT**: call the list complete or current; publish `Licensee`, phone or
  mailing columns.
- **MUST DO**: at each refresh, check whether the data-transfer notice is still
  on the lists page, and drop it from the notice when the Board removes it.
  Removal contact: publicrecords@lcb.wa.gov.

**111. Snohomish County (Seattle (Regional)) — required, and DISPLAYED**
(written into `render_site_notices()` with Seattle (Regional), 2026-10-02.)

- **SILENT, read permissively by the owner (2026-10-02)**: the "Food Service
  Establishments (2025)" item states no license; the County's GIS Terms of Use
  and Data Disclaimer are read as its governing position.
- **MUST DISPLAY**: the credit "Snohomish County, Food Service Establishments
  (2025)" (the owner's wording), never the health department, whose authorship
  is unconfirmed.
- **MUST NOT**: call the layer current, complete or official; its data are no
  newer than 2025-11-19.
- **MUST DO**: nothing. The removal rule is the safety net.

**112. City of Bellevue (Seattle (Regional)) — required, and DISPLAYED**
(written into `render_site_notices()` with Seattle (Regional), 2026-10-02.)

- **Read as permitted by the owner (2026-10-01, option 1)**: the data's own
  license field bars only commercial use or sale without written
  authorization; the portal's site terms are narrower.
- **MUST DISPLAY**: credit the City of Bellevue (the condition of the owner's
  reading; no wording prescribed, so this is the project's own).
- **MUST NOT**: use the data commercially; publish a registrant's legal name
  (never downloaded).
- **MUST DO**: take the layer down first if Bellevue objects.

**113. City of Seattle (Seattle (Regional)) — displayed by choice, not required**
(written into `render_site_notices()` with Seattle (Regional), 2026-10-02.)

- **PERMITTED WITH CONDITIONS**: the City's Open Data Terms of Use and Open
  Data Policy V1.0; no attribution is required, and crediting "City of Seattle"
  is recommended, so it is displayed.
- **MUST NOT**: use the data for a commercial purpose (data configurable as "a
  list of individuals"); publish contact names, phones, mailing addresses or
  person-named trade names.
- **MUST DO**: nothing.

**114. Geostat (Tbilisi) — required, and DISPLAYED**
(written into `render_site_notices()` with Tbilisi, 2026-10-02.)

- **PERMITTED WITH CONDITIONS**: Geostat's Terms of Use
  (`https://www.geostat.ge/en/page/monacemta-gamoyenebis-pirobebi`, linked
  from the register's own footer as "Terms of Data Usage") allow any use,
  "including commercial and non-commercial use, without restriction ...
  without prior permission". Third-party copyright and Geostat's logos and
  trademarks are outside the grant. Rows in
  [`data_sources/georgia.md`](data_sources/georgia.md).
- **MUST DISPLAY**: Geostat as the source: "Users should indicate Geostat as a
  source of information when using data of GEOSTAT" (also Article 43(6) of
  Georgia's Law on Official Statistics).
- **MUST NOT**: use Geostat's logo; imply Geostat's endorsement.
- **MUST DO**: nothing further. Individual entrepreneurs' names and personal
  numbers are never written to disk; the removal rule is the safety net.


## Gaps

- ~~San Francisco's boundary layer endpoint is not recorded anywhere.~~
  **Closed 2026-09-21:** identified as `wamw-vt4s` and confirmed byte-for-byte
  against the raw file. Every built city can now be rebuilt from scratch from
  this record and its country files alone<!-- internal -->, which `scripts/check_provenance.py`
  checks rather than this sentence claiming it<!-- /internal -->.
- Retrieval dates marked ≈ are inferred from commit history, not recorded at
  download time. Dates for cities added from now on are recorded exactly.
- Licences, as above — the one substantive gap left.
