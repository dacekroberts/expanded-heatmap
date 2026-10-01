# How the city list was made, 18–30 September 2026

**A history of `docs/city_master_list.md`, from the first screen of US cities
to the list as it stood after the review landed on 2026-09-30:**

- 124 cities built, in 24 countries;
- 18 candidates, every one of them in Band R;
- 100 discards, each naming its evidence.

This file explains how the list got there: the band scheme, the methods that
changed verdicts, the rules that let cities in or kept them out, and what each
country's first build taught the next. Written 2026-10-01 (staging; owner's
outline, 2026-09-30).

**How to read it.** The list itself is current state, and its evidence trail
is `docs/global_country_shortlist.md` and `docs/city_master_list_evidence.md`.
This file is neither: it is a narrative over them, and **every count in it is
dated**. Citations name a file and section, or a decision-log entry by its
date and heading:

- **DECISIONS** is `DECISIONS.md`, the current week.
- **[09-20 week]** is `docs/decisions/2026-09-20.md`.
- **[09-13 week]** is `docs/decisions/2026-09-13.md`.

Times are the project's local commit times (UTC−7).

**The list was rebuilt fresh on 2026-10-01**, after this history was written.
Every citation of `city_master_list.md` here refers to the list as it stood on
2026-09-30, archived word for word at `docs/city_master_list_2026-09-30.md`. That is why an entry
dated 09-24 in the log can carry a commit on the evening of 09-23.

---

## The short version

1. **The list began as a US shortlist and became global in a day.**
   - The first screen (09-18) took the 25 largest US cities down to 10.
   - Canada (09-21) took 13 candidates down to 6, and built five of them in
     about seven hours.
   - The worldwide screen started the same afternoon: 87 countries.
2. **The band scheme was rebuilt many times, and it settled when the bands
   came to name the kind of work that unblocks a city.** Tiers ranked
   countries; bands rank blockers. Two rules held through every renumber:
   - "a letter is for a heading, a condition for a sentence";
   - a band whose condition stops being true closes; it is not re-captioned
     around whoever is left.
3. **Most negatives that were overturned were statements about a search, a
   host or a tool, not about the data.** The methods that overturned them:
   - open the portal in a real browser first;
   - enumerate the whole catalogue instead of searching it;
   - ask a different host, not a different network;
   - look for an address file before writing a geocoder.
4. **The rules that keep cities out arrived as named cases, and most of
   them in the last three days:**
   - the reduced-bucket bar;
   - one clock for currency;
   - the light-rail test;
   - the stub test;
   - about 70% placed.
5. **What one country's first build left behind set the price of its second
   city.** One national register (Mexico, France, Brazil, Korea's SEMAS)
   made the next city a config. A bespoke city (Spain) taught that the next
   one costs nearly full price.

---

## 1. Before there was a list (09-18 to 09-21)

**The first screen was American and had three criteria:**
- expansive rail;
- transit open data;
- business-licence data with a classification and an address or geometry.

Of the 25 largest US cities, 10 were shortlisted. Seattle, the prototype's
city, was swapped out for Washington D.C. [09-13 week, "City selection, live
verification, taxonomy plurality"; `us_build_retrospective_addendum.md` §1].

**Two rules came out of it on contact with the data:**
- **Verify a city's schema live before writing any code.** Denver's "Active
  Business Licenses" had no address, classification or geometry. San Jose
  had no bulk source.
- **A register need not use NAICS.** The addendum calls this "the single
  highest-leverage decision in the project": "It reclassified three of the
  four largest cities from fail to pass" [`us_build_retrospective_addendum.md`].

Dallas was kept on 09-18 as "marginal" and ruled out on currency on 09-21. Its
certificate-of-occupancy file had stopped on 2022-11-15 [09-13 week, "Live
check of Dallas, Austin, Charlotte and Fort Worth"; 09-20 week, "Screened every
remaining candidate city…"]. It is the longest-running case in this history
(§9).

**Canada was the first whole country** [`canada_retrospective.md`]:
- **Rail first.** 13 candidates went to 6 "before a data catalogue was
  opened".
- **Five cities were built from 14:19 to 21:24 on 09-21**, about seven hours.
- **The lesson that shaped everything after:** "Depth per country beats
  breadth across countries". Six cities needed four portal types, so six
  integrations.
- **Rankings moved during the builds.** Three of six storefront-per-station
  figures moved, two by more than 1.8×. The country's ranking was not a
  measurement until the builds made it one.

## 2. The global screen (09-21)

**The screen started from an exhaustive base, not a list of likely
places** [`global_country_shortlist.md`, header]:
- every country in the Mobility Database catalogue: **87 countries, 2,476
  static GTFS feeds**;
- the US and Canada left out, as already screened.

**The filter order was flipped the same day** ["The filter order, and two that
were dropped"]. Rail had removed 6 of Canada's 13, but outside North America it
"barely discriminates". The new order:
1. premises-level business data, the discriminator;
2. the licence and privacy regime;
3. a readable transit feed, as a confirmation only;
4. map coverage, which is free.

**The business test asked whether a country records PREMISES or only
registered offices.** Four shapes qualify:
- a municipal licence register (US, Canada, Korea);
- a national establishment register (France's SIRET, Mexico's DENUE);
- a field survey of commercial premises (Montréal, Barcelona);
- a sector inspection register (the UK's FSA, one bucket).

A company register is a category error, because a chain appears once, at its
head office ["The sharper form of the business-data question"].

**Countries were ranked in tiers by cities gained per unit of work.**
- Tier 1 had both legs measured; lower tiers left one leg or both open.
- Tiers 5 and 6, added later, were "needs the browser".

The tier view is kept as evidence [`city_master_list_evidence.md`, "The
2026-09-22 tier view"]. Its two lasting calls:
- **France rose to Tier 2** once SIRENE's geolocation was measured above
  99.7% in all six cities.
- **Japan was "a BUILD, and it goes last"**, so that the geocoding machinery
  could accumulate first [09-20 week, "Japan is a BUILD, and it goes last;
  the master list becomes its own file"].

## 3. Tiers became bands (09-22 and 09-23)

**The list became its own file at 00:46 on 09-22, with 14 built, 48
candidates and 14 discards**, banded A–D by what blocks each city [git
03e6d5ab; 09-20 week, "Japan is a BUILD…"]. The tiers "had stopped
discriminating" [09-20 week, "Master city list rebanded, and eleven cities were
discarded on a reason this project's own file contradicts"].

**That first day the bands churned.** By 20:17 the scheme read:
- A ready;
- B awaiting permission;
- C coordinates cheap;
- D coordinates plus unfinished screening;
- E geocoding at national scale;
- F one bucket;
- G access blocked.

Bands then closed one after another as their condition stopped being true
[09-20 week, "Sofia settled by enumerating Bulgaria's catalogue…", which
gathers the day's band entries]:
- B when Tel Aviv was discarded on terms;
- D when Bucharest finished its screening;
- G when India was swept.

**Two rules came out of the churn and held through every later change**
[`city_master_list.md`, the band table's notes]:
- **"A LETTER is for a heading, a CONDITION is for a sentence."** Four
  sentences went stale the moment the letters shifted, and more went stale
  within hours of the next renumber. The list's own warning: "easy to agree
  with and easy to break in the next paragraph".
- **"A band whose condition stops being true of its last member should
  close, not be re-captioned around the occupant."** Its companion: a
  caption names a blocker, never a date or a status.

**On 09-23 a band closed by succeeding.** Every member of the coordinates band
had its route measured and a brief written, so the band was absorbed into A
[git 0953ffdb]. The access-blocked condition came back true of Kaohsiung, so
it reopened under the next free letter [09-20 week, "Kaohsiung moves to a
reopened access-blocked band (D)…"].

**The summary drifted, and that produced a check.** On 09-23 the summary box
read 20 / 33 / 30 while the band sections said 22 / 29 / 32. The list's
verdict: "the hand-kept summary is the first thing to drift, which is why the
band sections are the ones to trust" [09-20 week, "The master list's
summaries drifted…"]. Counts are now enforced by
`scripts/check_master_list_counts.py`.

## 4. Rules about evidence (09-21 to 09-24)

**"A row reading 'not reached', 'unprobed' or a regional pattern is not a
discard."** On the evening of 09-21, eleven discards were found resting on
exactly that, against evidence in the same document: Berlin, Hamburg,
Stockholm, Budapest, Naples, Messina, Hyderabad, Kochi, Tallinn, Zagreb and
Santiago. They moved back into the bands [09-20 week, "Master city list
rebanded, and eleven cities were discarded…"]. Stockholm and Berlin were later
built. Berlin was back in the discards before the list had its own file, on one
keyword search (`Gaststätten` → 0), which is how it stayed until 09-28 (§9).

**"A country ruling needs two cities measured, not one asserted onto a
region"** (09-24). Eight countries left the ruled-out list with the discard
audit: Germany, Austria, the Netherlands, Greece, Portugal, Poland, Latvia and
Slovakia, each resting on one national-level method. The Netherlands' Amsterdam
was built the same day; Latvia's Riga, Liepāja and Daugavpils followed
[`city_master_list.md`, "Countries ruled out" and "Five rules"].

**The discard audit.** On the night of 09-23 to 09-24, every discard row was
read against the probe log:
- 12 single-method rows went to a new **open screening gap**, then 5 more;
- the table gained columns for the kind of evidence, the methods used and
  whether the city's own host was asked;
- `scripts/check_discard_evidence.py` decides whether a row's evidence is
  enough, and **a failing row moves to the gap; the rule is not relaxed**.

[09-20 week, "Discard audit…" and "Discard table gets evidence columns…"; git
e57c062c, 2650b486]

The gap was emptied by the evening of 09-24, after a re-probe of every row, on
the owner's calls [09-20 week, "The open gap emptied…"].

## 5. The methods that changed verdicts

**Open the portal in a real browser first.** The 09-22 browser sweep closed
Tier 5. Its record: the browser's answer "differed from the guessed one every
time" [09-20 week, "Tier 5 closed by browser navigation"]. Examples:
- Medellín's hub turned out to be private;
- Peru's portal showed itself as DKAN, and its dataset list returned 4,687
  entries;
- Jakarta's API was read off the browser's network panel.

**Enumerate a catalogue rather than search it.** On 09-22, three recorded
negatives "turned out to be statements about a SEARCH rather than about the
data", and "each cost one HTTP call to disprove" [`city_master_list.md`,
"What this day changed"]:
- Stockholm's register is called `Tillsynsverksamheter`, "a word no query
  contained";
- Zurich's catalogue had been matched over 938 of 1,128 names;
- Hong Kong's bulk export had been on `data.gov.hk` all along, and its
  dataset list (3,821) had never been requested.

India was then swept in full, 288,011 titles, "so it would not become the
fourth". The same lesson brought Berlin back on 09-28: enumerating 2,626
packages found IHK Berlin's premises register, 367,575 points
[`global_country_shortlist.md`, the Germany row].

**Ask a different HOST, not a different network.** Seven cities were reached
that way on 09-22: Sofia, Sevilla, Tel Aviv, Tallinn, Prague, Dublin and Hong
Kong. "*Unreachable* turned out to mean *not yet asked properly* in every
single case" [`city_master_list.md`, "What this day changed"]. Reaching a city
is not passing it: Sofia, Sevilla and Tallinn then measured negative, and Tel
Aviv was discarded on its terms.

**Send a nonsense term before trusting a search.** Several search endpoints
ignore the query entirely:
- Seoul's search returned byte-identical pages;
- Singapore's and `api.data.gov.in`'s searches were inert;
- `data.go.jp` "ignores `q`".

A result count means nothing until a nonsense query returns zero
[`global_country_shortlist.md`; `add-country`, "Evidence discipline"].

**Find an address file before writing a geocoder.** The national-geocoding
band was meant to hold the expensive countries. Each, when probed, already
published an address file with coordinates. The `address-join` skill is that
method, written down [`geocoding_retrospective.md`, "Four for four"; 09-20
week, "Japan re-banded and the geocoding band closed"].

| Country | Placed by a join |
|---|---|
| Prague | 99.8% |
| Copenhagen | 96.9% |
| Brazil (enumerators' points) | 95.1–99.9% |
| Taiwan | 92.4–95.5% |
| Japan | block-level join; its band closed 09-24 |

**Re-probe a thin city the same way** (`reprobe-city`, from Amsterdam on
09-24):
1. ask the city's own host;
2. enumerate with a nonsense control;
3. read who a 403 is for;
4. look for a second layer of a different shape;
5. control each layer.

Amsterdam went from the discards to Band A in one evening.

**The limit the methods could not cross is a refusal at the IP level.** A
browser on the same machine is refused too. The project uses no VPN, proxy or
account, so those cities became Band R (§7), where every one of the 18
remaining candidates sits.

## 6. Widening the list (09-27 and 09-28)

**By 09-25 the list had nearly run dry**: 46 built, 20 candidates, 27 discards
(the first-parent count, §12). Three re-screens refilled it:

- **Wave 1, the second-city screens of built countries (09-27).**
  - Korea, Taiwan, Hong Kong, France, Czechia, Norway, Denmark, the
    Netherlands and Latvia were screened.
  - It added 43 candidates, **32 of them trams-only** (France 21, Czechia 6,
    Denmark 2, Latvia 2, Norway 1).
  - Daegu and Busan were reopened on their own cities' portals and built the
    same day [DECISIONS, "Wave-1 second-city screens banded…"].
- **Wave 2 (09-27 and 09-28).**
  - Canada, Brazil and Ireland; then Spain and Italy; then the US.
  - It sent Kitchener–Waterloo, Florence, Santa Cruz–La Laguna and seven US
    cities to the trams band, and Palma and Baltimore to C.
  - It discarded 40, and left nine cities not reached because their portals
    refuse scripts.
  - Its load came to about 44% of one five-hour window, against an estimate
    of 80–130% [`PLAN.md`, wave 2].
- **The transit-gap re-screen (09-28).**
  - **Its start list:** once Sapporo, Fukuoka and Kyoto were live, "every
    city within the original candidate specs is built or banded". The
    owner's ask was every large network the specs, or an old negative,
    still kept out [`global_transit_gap.md`].
  - **What it reversed:**
    - London's "ruled out" (the UK's stated reason was wrong);
    - Berlin's search negative;
    - Manila's and Dubai's "no feed" reasons, obsolete once rail came from
      OpenStreetMap;
    - Algiers' "no urban rail" misfiling.
  - **What was built the same day:** London, Berlin, Buenos Aires, Glasgow,
    Newcastle, Sydney and Melbourne [`city_master_list.md`, the Built
    table].

**Candidates peaked at 87 on 09-28**, after the transit-gap screen
[DECISIONS, "Bands restructured…"]. Every build after that drew the number
down.

## 7. The scheme settles (09-27 to 09-30)

| Date | Change | Source |
|---|---|---|
| 09-27 | **Band T created** ("trams only"), and **first blocker wins** made universal: access, then buckets, then trams. The same evening, renamed "Contingent on trams" and the order amended to **access → trams → buckets** | DECISIONS, "Trams count; Band T (trams only) created…" and "Band T renamed…" |
| 09-27 | **Band C widened** to "one bucket only, or buckets with a measured gap" | DECISIONS, "Wave-1 second-city screens banded…" |
| 09-28 | **C's last five given verdicts and C closed; B reopened** as "Passed: narrower pages"; **Band N** ("no page for now") created | DECISIONS, "Band C's last five get verdicts…" |
| 09-28 | **N retooled as C, "closer to a page"; D split** into D (a CAPTCHA or a free account the owner can clear alone) and **R** (restricted) | DECISIONS, "Bands restructured…" |
| 09-28 | **R renamed "restricted or request only"**; Kaohsiung, Tallinn and Sendai into it. Every future request-only city goes there | DECISIONS, "Request-only cities move to Band R…" |
| 09-29 | **Band T audited and moved to its own file**, `docs/tram_city_list.md`, in tiers T1 and T2; **ten cities left it on the light-rail test** | DECISIONS, "Band T audited…" |
| 09-29 | **Trams-only maps approved** | DECISIONS, "Yes to trams-only maps (owner)…" |
| 09-29 | **C closed again**: eight to B on the reduced-bucket bar, its last five (Singapore, Istanbul, Ankara, Perth, Ho Chi Minh City) to the discards | DECISIONS, "Band C closed: its last five to the discards (owner)" |
| 09-30 | **T2 closed**: Zurich, Göteborg and Den Haag to T1; Utrecht to R; Santa Cruz–La Laguna, Rijswijk and Delft to the discards | DECISIONS, "T2 closed…" |
| 09-30 | **Review time lands every build**: A, B and T empty | `city_master_list.md`, summary box |

**The scheme that came out of it** [`city_master_list.md`, "Five rules"]:
- **A city sits in the band of its FIRST blocker**, with every other blocker
  noted beside it, and is never listed in two bands.
- **The blockers are taken in order:**
  1. access (D or R): can the data be reached at all?
  2. trams (T): does the build need a yes on trams-only maps?
  3. buckets (C): does it yield two or more, without a measured gap?
- **Light rail is not a trams question.** A city that passes the light-rail
  test goes to the band of its next blocker (owner, 09-29).
- **The same rule governs the Japan list** and every republish in chat.

## 8. The filters, each with the case that set it

**The reduced-bucket bar** (owner, 09-29). It was drawn from the pages already
built on fewer than three buckets: Stockholm, Bucharest, London, Glasgow,
Newcastle, Hong Kong and Incheon [`city_master_list.md`, "The Band C audit's
bar"; DECISIONS, "The Band C audit: a reduced-bucket bar…"]. A page passes
with:
1. **at least one full bucket at register quality.** This was "food" until
   Yokohama, whose only full bucket is personal services, amended it the same
   day;
2. **a source current under the one-clock rule;**
3. **a register of premises,** not a curated guide;
4. **size and in-ring share disclosed on the page, never a gate.** This was
   relaxed from a floor once Houston would map at about 7% in a ring;
5. **about 70% or more placed** (Incheon's 71.3%);
6. **rail that passes**: the light-rail test, and not a stub.

**One clock for currency** (owner, 09-29). A rule by kind of source was
committed at 02:43: five years for a census, 18 months for a register, a
closure field for event streams. At 02:58 it was replaced by one rule for every
source. The owner had asked why the periods differed, and the answer was that
they were fitted to earlier calls rather than derived [DECISIONS, "A currency
rule by kind of source…" and "The currency rule rewritten as one clock…";
`city_master_list.md`, "Five rules"]. The one rule:
1. **The source must be able to drop closed businesses.** Dallas's
   certificates of occupancy and Santa Cruz–La Laguna's directory record
   openings only, and fail at any age.
2. **Its age is read in the rows, never the catalogue.** Stockholm's layer
   read "daily" while frozen; Tenerife's catalogue was re-stamped with no row
   changed.
3. **The ceiling is five years, with the date on the page.**
   - Stockholm, Kansas City and Atlanta pass on age.
   - Hamburg's 2016 survey fails.
   - Baltimore, every row edited in 2008, went to the discards. Its lesson:
     a currency check belongs before a band move [DECISIONS, "Baltimore to
     the discards on currency…"].

**The light-rail test** (owner, 09-29). San Diego, Calgary and Edmonton were
built on light rail with no trams decision ever made, so light rail passes on
precedent and only street trams waited on the trams call
[`tram_city_list.md`, "The light-rail test"]. Three parts, read against those
three precedents:
- **track:** tunnel and bridge share, and how OSM maps the line;
- **frequency, 15 minutes by day:** a gate only on converted railway
  (Aarhus's L1). On purpose-built track a slower timetable is disclosed
  (Buffalo's flat 20 minutes);
- **spacing:** supporting evidence, never the gate.

Ten cities left the trams band on it in one day.

**The stub test.** A city scoped to its own boundary must not cut a line down
to a stub:
- **France's rule:** under half of a worst line's stations inside the commune
  means a regional scope. Lille went regional; Toulouse, at 52%, stayed
  commune-only [`city_master_list.md`, the Built table, Europe].
- **Monterrey stayed regional** because city-only cut Línea 2 to 8 of 13
  (62%), below Rennes' 73% [DECISIONS, "Monterrey (Regional) screened into
  Band A…"].
- **The owner accepted 42%** for Minneapolis's and Pittsburgh's worst lines
  rather than hold them to Toulouse's 52% [DECISIONS, "Minneapolis and
  Pittsburgh to B…"].

**About 70% placed.**
- **Pass:** Incheon set the mark at 71.3%. Palma passed at 74.0% on a
  Catastro join.
- **Santa Cruz–La Laguna** was discarded at 57.7% [DECISIONS, "T2 closed…"].
- **Zaragoza** was discarded because only about 36% of its addresses carry a
  house number (61% are a bare street), so the bar was out of reach before
  any join [`city_master_list.md`, Zaragoza's discard row].

**Licences, read before building.** The `read-licence` method returns one of
four verdicts: PERMITTED, WITH CONDITIONS, SILENT, NOT PERMITTED. The last is
never resolved in the project's favour.
- Tel Aviv was discarded on its terms ("creating a database").
- Barcelona's terms were the first that oblige an act rather than a notice.
- Spain alone cost more licence reading than the nine US cities combined
  [`spain_retrospective.md`].

**Personal information.** "Publish public commercial information, not personal
information" dates from Los Angeles's catch-all code on 09-21 [09-20 week,
"Privacy line…"]. It shaped what a register can be used for:
- a trade name, never a registrant's own name at a home;
- the Japanese, Korean and Taiwanese name rules;
- a verdict from `check_personal_exposure.py` for every city before it
  publishes.

## 9. Reversals, and why each one turned

| City | From | To | What changed |
|---|---|---|---|
| **Dallas** | candidate (09-18); discarded on currency (09-21) | Band A (09-30); built the same day | The Texas Comptroller's sales-tax permit file, a register that drops closures, replaced the frozen occupancy certificates: 19,557 storefronts at the screen, 90.0% placed [DECISIONS, "Wave-2 follow-ups: Dallas to Band A…"] |
| **Berlin** | discarded on one search (`Gaststätten` → 0) | Band B (09-28); built the same day | Enumerating 2,626 packages found IHK Berlin's premises register; the gap became "only hairdressers and laundries" [DECISIONS, "Berlin from the discards to Band B…"] |
| **Kansas City** | out on rail (09-21) | trams band (09-27); built 09-30 | Streetcars counted once trams did; the line passed the stub test |
| **Monterrey** | "measured negative at the publisher" (09-22) | Band A (09-27); built the same day | Its only negative was the agency's missing feed, obsolete once OSM rail was approved for Mexico City (195/195 stops exact) |
| **Hiroshima** | C, then trams band | out of trams (09-29); built 09-30 | MLIT's rail layer puts the Astram Line and JR inside the city, so trams were never its first blocker |
| **Yokohama** | 17,408 personal-services premises | 7,896; built 09-30 | A recount at the source; the 17,408 could not be traced. The brief was corrected, not the code [DECISIONS, "The Band C measurements…"; `band_b_retrospective.md`] |
| **Singapore** | "passes", about 41,600 premises (09-22) | discarded (09-29) | NEA's food register ends 2016-09-06: two buckets on paper, one on current data |
| **Paris** | Band A | out and back within the hour (09-22) | Demoted, then restored on a filter measured against OSM (50,156 against 54,198) |
| **Amsterdam** | discarded, "aggregate" on one search | Band A (09-24); built the same day | The city's own API: hospitality permits plus the BAG's shop units |
| **The UK, Australia** | ruled out as countries | London, Glasgow, Newcastle, Sydney, Melbourne built (09-28) | "NNDR has no category" and "licensing is not municipal" were both wrong |

**The common thread is in the list's own words**: "Nothing was lost that was
ever measured as viable — the five drops were all cities whose business leg had
never been tested, and testing it is what removed them" [`city_master_list.md`,
the 09-22 re-band notes]. A reversal turned on a measurement every time, never
on a change of mind.

## 10. What each first build taught the next

**Mexico: one national register, so the second city was a config.** DENUE has
a coordinate on every row. Guadalajara's config differed from Mexico City's by
one line (`DENUE_STATE_CODE`) [`city_cost_order.md`]. The rail leg was the
expensive one, which left the rule "Budget the rail leg. Assume the business
leg is solved" [`mexico_retrospective.md`]. It also produced the `osm-rail`
meta-rule: put a lesson where the next city must pass through it. A warning in
Mexico City's config did not stop Guadalajara losing Línea 4.

**Spain: bespoke per city, so six candidates were two.**
- Valencia, Bilbao and Málaga measured negative.
- Barcelona inherited "the accent-and-encoding discipline and essentially
  nothing else".
- "Linguistic adjacency is not data adjacency"; a third Spanish city costs
  "nearly full price" [`spain_retrospective.md`].
- Palma, built 09-30, bore that out: it needed a new shared Catastro join.

**France: the second city cheaper, the third cheaper again.**
- **The first five.** Marseille inherited the register, the taxonomy, the
  cache and the grid. Toulouse "downloaded nothing at all"
  [`city_master_list.md`, the Built table].
- **The 21-city tram batch** took about an hour for twenty cities after its
  shared module, and Angers about a quarter of an hour.
- **Quantity changed the kind of mistake, not its rate.** City-specific
  traps ran at about one per city, as in single builds. Generator defects
  were fewer than ten but each reached 10 to 20 files
  [`france_batch_retrospective.md`].

**Brazil, Taiwan and Japan: a join, not a geocoder.**
- **Brazil** was picked to go first in the geocoding band "and turned out to
  need no geocoder": IBGE's census address file carries a coordinate for
  every establishment, so nine cities shipped as one batch.
- **Taiwan's** first probe found the same, a door-plate file per city.
- **Japan** joined at block level.

The country the plan had placed last, by decision, was built in two days
[`city_master_list.md`, "The order, as decided"; `geocoding_retrospective.md`].

**Czechia: a register's premises may be published by a different agency.**
Prague paused on RES, which records an owner's registered seat. ROS02's
establishments gave the premises, and the six tram cities then cost "its tram
leg, a scope call and its notices" [`czech-tram-city` skill §1]. The Czech kit
wrote no retrospective; its lessons are in that skill and its drafts file.

**Korea: the city's own portal, then a national storefront register.**
- Busan and Daegu, "closed" on 09-22, were reopened on their own portals
  [DECISIONS, "Wave-1 second-city screens banded…"].
- Incheon's SEMAS register (keyless, every storefront with a point) made the
  Gyeonggi satellites a generator's work.

## 11. What the last three batches taught (09-29 and 09-30)

Three build sessions wrote retrospectives before the review landed. They agree
on the shape of the change:

- **Decisions moved ahead of code.**
  - The US batch made "nine method changes in nine cities".
  - The tram kit had ten briefs, a skill and 28 owner calls before its first
    build. It took ten cities to zero drift in under four hours and redid
    none [`tram_kit_retrospective.md`].
- **Templates replaced first principles.** "Ten of the twelve Band B cities
  were an existing template with a config" [`band_b_retrospective.md`].
- **The mistakes changed kind.** In Band B's words: "The early builds'
  mistakes were measurement mistakes … Band B's were framing and process
  mistakes". That is the signature of a pipeline whose measurements are
  guarded and whose remaining risk sits in the human steps around it.
- **A brief is a cache of Step 0, mistakes included.**
  - The tram kit found a discrepancy in nine of ten briefs, every one with a
    passing check. `brief_check.py` checks the claims a brief makes, not the
    ones it should have made.
  - The operator's station count (gate 3) ran in one city of ten, because
    the skill never asked for it. It is now required, with a back-fill of 25
    cities in `PLAN.md` [`tram_kit_retrospective.md`, "Lessons"].

## 12. The numbers over time

At the end of each day on master's first-parent history, read from the list's
own section headings:

| Date | Built | Candidates | Discards | What moved them |
|---|---|---|---|---|
| 09-22, first version | 14 | 48 | 14 | the list becomes its own file |
| 09-22 | 20 | 31 | 30 | Mexico City, Guadalajara, Madrid, Barcelona, Dublin and Milan built; the browser sweep; Spain to two cities |
| 09-23 | 27 | 33 | 16 | France's five, Oslo and Copenhagen built; the discard audit |
| 09-24 | 42 | 24 | 27 | Brazil's nine, Hong Kong, Riga, Rotterdam, Prague, Amsterdam and Rome built; the open gap emptied |
| 09-25 | 46 | 20 | 27 | Seoul and Taiwan's three built |
| 09-27 | 50 | 63 | 51 | wave 1 (+43, 32 trams-only); Monterrey, Daegu, Busan and Kobe built |
| 09-28 | 62 | 80 | 91 | wave 2 and the transit-gap re-screen; twelve landed, five Japanese and seven from the re-screen |
| 09-29 | 75 | 66 | 97 | the light-rail test; C closed; Stockholm, Bucharest, Incheon, five satellites and the five light-rail cities built |
| 09-30, before landing | 75 | 64 | 100 | T2 closed; Dallas to A |
| **09-30, after landing** | **124** | **18** | **100** | review time: the France, Czech and tram batches and Band B |

**What the series shows:**
- **Built counts move only when a city lands on master.** Builds on branches
  waited for review time, which is why 49 arrived in one evening.
- **Within a day the counts were not monotone.** Branches carried their own
  counts and were reconciled at each merge.
- **Candidates peaked at 87 during 09-28.**
- **Discards rose most when a screen widened, not when a rule tightened.**
  Wave 2 alone discarded 40.

## 13. Where it stands, 2026-09-30 after the review

**Every candidate the screens found buildable has been built.** Bands A, B, C,
D and T are empty. The 18 candidates left are all in **Band R**: geo-blocked
(ten), behind a residency wall (two), request only (Kaohsiung, Tallinn,
Sendai), a restricted CAPTCHA (Delhi), institutional accounts only (Lisbon),
or a portal that refuses a browser too (Utrecht). None of them moves without
access the project does not use, or a request only the owner sends
[`city_master_list.md`, "Band R"].

**The list's next growth is screening, not building.** The staging handoff
holds a ranked list of probes. Among them are groups no screen ever reached:
- the UK's tram and light-rail cities, on the food register three built UK
  cities already use;
- Japan's tram cities, outside the ten subway cities the Japan screen
  covered;
- countries ruled out on "no urban rail", which their own screen said to
  revisit if trams-only maps were ever approved.

[`handoff_staging_2026-09-30.md`, "Ranked list"]
