# GTBA | The whole project: retrospective (2026-10-16)

Written 2026-10-16 from the record; committed 2026-10-17 on the owner's word.

The project ran from its first commit on 2026-09-18 to 2026-10-16, when the
owner closed it to maintenance with no more cities for now. It is the Global
Transit-Business Atlas: 237 maps of storefront density around rapid-transit
stations. The country and batch retrospectives in `docs/` are pointed to, not
repeated. Every figure names its file, DECISIONS entry or commit; nothing was
checked on the live site.

## The short answer

**What was built.** 237 city pages in 27 countries (`app/cities.py`, 237
entries; Hong Kong counts as its own entry). Japan has 94 of them, France 26,
the United States 20 and South Korea 18 (same file). Every map has place
search (commit 3e16745d, 2026-10-13). The screen behind it covered 87
countries (`docs/global_country_shortlist.md`).

**What it cost.** The repository holds 3,570 commits over 26 active days,
2026-09-18 to 2026-10-16 (`git rev-list --count HEAD` at ff29d056). Of these,
652 are merges (`git rev-list --count --merges HEAD`). The decisions log holds
1,376 entries across the live file and four weekly archives (generated index
counts). No per-city record of hours or tokens exists (DECISIONS 2026-10-12,
"Phase 2 landed"); measured usage is under "Costs and efficiency".

**The choices that mattered most:**

1. **Verify a city's real data live, and accept a register that is not
   NAICS.** The US addendum calls the second "the single highest-leverage
   decision in the project" (`docs/us_build_retrospective_addendum.md`, via
   `docs/city_master_list_history.md` section 1). The global screen was
   built on both.
2. **Pre-render static maps from an offline pipeline.** The deployed app only
   reads `outputs/` (DECISIONS archive 2026-09-13, "Project origin and
   architecture"). The deploy stayed lean from 3 cities to 237.
3. **Decide before code.** Later batches made their calls, briefs and skills
   before the first build. The tram kit took ten cities to zero drift in
   under four hours and redid none (`docs/tram_kit_retrospective.md`). The
   first US batch made "nine method changes in nine cities".

## Timeline

City counts are the entries in `app/cities.py` at the last first-parent
commit of each day. A city built on a branch counts only when it landed.

| Date | What happened | Cities |
|---|---|---|
| 2026-09-18 | First commit; San Diego, San Francisco, Los Angeles | 3 |
| 09-20 | Chicago; New York from four registries | 5 |
| 09-21 | Philadelphia, Miami, Boston, Washington D.C.; the pre-deploy gate (47d893a5) and the live URL (48f6e296); Canada's five in about seven hours; the global screen begins | 14 |
| 09-22 | Mexico City, Guadalajara, Madrid, Barcelona, Dublin, Milan | 20 |
| 09-23 | France's first five, Oslo, Copenhagen | 27 |
| 09-24 | Brazil's nine as one batch; Hong Kong, Riga, Rotterdam, Prague, Amsterdam, Rome | 42 |
| 09-25 | Seoul and Taiwan's three | 46 |
| 09-27 | Monterrey, Daegu, Busan, Kobe; the first efficiency review | 50 |
| 09-28 | Twelve landed, five Japanese and seven from the transit-gap re-screen | 62 |
| 09-29 | Trams-only maps approved (7a8de9b5); the light-rail test; Stockholm, Bucharest, Incheon | 75 |
| 09-30 | The mega-review landed: France's 21 tram cities, Czechia's six, the tram kit's ten, Band B's twelve | 124 |
| 10-01 | The master list rebuilt fresh; the review lane kit | 124 |
| 10-02 | Ridership made a hard line; the UK six, Seattle (Regional), Tbilisi built | 144 |
| 10-03 | Regional extensions; Belgium out of Band R | 158 |
| 10-04 | Tacoma, Liverpool, Mendoza, three Korean cities; the second efficiency review | 170 |
| 10-07 | The large review landed; the line identity hard line; place search piloted on Kyoto (b2e4a8a4) | 206 |
| 10-12 | Phase 2, the last build wave, landed: 30 Japanese cities and Cluj-Napoca (f89bb728) | 237 |
| 10-13 | Place search on all 237 maps (3e16745d); trams added to Toronto, Milan and Prague | 237 |
| 10-16 | All 237 re-rendered (559bf919); the rename landed (65351d01); closed to maintenance | 237 |

Events: `docs/city_master_list_history.md` section 12, the commits named and
the DECISIONS index. No commits exist on 09-26, 10-09 or 10-10.

## How the scope grew

**The project started as one city and widened in four steps.**

- **A Seattle prototype came first:** one city, Link light rail, 11,409
  points. Its concept carried over, but not its ridership axis or findings
  pages (DECISIONS archive 2026-09-13, "Project origin and architecture").
  Seattle returned as Seattle (Regional) on 2026-10-02, from five publishers.
- **Then the US, then country by country.** The first screen took the 25
  largest US cities down to 10 (`docs/us_build_retrospective_addendum.md`).
  Canada was the first whole country, on 2026-09-21, and the worldwide screen
  began that afternoon (`docs/city_master_list_history.md` section 2).
- **Regional extensions** carried 34 pages past their core city
  (`docs/city_master_list.md`, "Regional extensions").
- **Trams-only maps** were approved on 2026-09-29 (7a8de9b5). They brought
  France's 21-city tram batch, Czechia's six and the tram kit's ten, all on
  2026-09-30. On 2026-10-13, trams were added to Toronto, Milan and Prague,
  which had been built without them (DECISIONS index, "Tram rescope").

**Phase 2 was the last build wave.** It landed 31 cities on 2026-10-12, which
left no candidate in Bands A to D (DECISIONS 2026-10-12, "Phase 2 landed").
Place search, piloted on Kyoto on 2026-10-07, reached every map the next
day; its own retrospective is listed in `PLAN.md`.

**The site was renamed at the end.** "Storefronts Near Transit" became
"Global Transit-Business Atlas" (owner, 2026-10-14; landed in 65351d01).
"Index" was set aside because it reads as a ranking, which the site
disclaims (DECISIONS 2026-10-16).

## The screening funnel

**Most cities that were screened were not built.** The final counts are
generated from the rows by `scripts/check_master_list_counts.py`
(`docs/city_master_list.md`, "Final state, 2026-10-12"):

| Outcome | Cities | What it means |
|---|---|---|
| Built | 237 | on the site |
| Band R | 91 | needs access the project does not use, or a request only the owner sends |
| Open screening gap | 10 | the city's own host never answered |
| Discarded | 329 | each naming its evidence |

`scripts/check_discard_evidence.py` checks each discard's evidence. Band R
stays a band but is left out of candidate counts (owner, 2026-10-02).

**The filter order flipped once, on 2026-09-21.** Rail removed 6 of Canada's
13 candidates, but outside North America it "barely discriminates"
(`docs/city_master_list_history.md` section 2). After that, premises-level
business data came first and the transit feed was a confirmation. A company
register was a category error: a chain appears there once, at its head office.

**Most overturned negatives were about a search, not the data.** The history
names four methods that reversed verdicts: a real browser, the whole catalog,
a different host, and an address file before any geocoder (same file, "The
short version"). The `reprobe-city` and `address-join` skills hold them.

At close, 430 unbuilt cities with rail went to transit-globe as a list, with
no business data (DECISIONS 2026-10-16, "The project closed to maintenance").

## The hard lines, and why each exists

**Most hard lines trace to a named incident; ridership traces to a data
limit.** The stories are in `docs/rule_history.md` at each anchor.

- **Public commercial information, not personal information**
  [#personal-info]. A pin is a name at a point, so a register with no trade
  name would publish a person's own name at what may be their home. San
  Diego's removals went from 42 pins to 315 after the build, and Los Angeles
  removed 1,252 (`docs/tram_kit_retrospective.md`). One email address among
  91,000 pins, unseen by the exposure check, led to contact details being
  dropped in shared code (DECISIONS archive 2026-09-20). Every city now has a
  verdict row (`docs/privacy_verdicts.md`, `check_privacy_verdicts.py`).
- **Licenses read and recorded, notices displayed** [#licence]. A government
  portal is a reason to expect open terms, not evidence. LA Metro's feed
  forbids modifying its data; Philadelphia's prohibition hid behind a
  license, by reference. `app/components.py` holds 214 `Notice(` lines.
- **Basemap attribution stays visible** [#attribution]. On 2026-09-23 the
  legend covered the OpenStreetMap credit in all 23 cities at viewports
  taller than the map, though every file held it. The check now tests a
  real render at more than one height.
- **Ridership is out of scope** [#ridership], set on 2026-10-02 "since the
  data cannot be had for every city". Only the owner can open a subset.
- **One line, one color and one name, site-wide** [#line-identity]. The
  2026-10-07 review found the JR Kobe Line in five colors across Kansai; 48
  Japanese lines moved onto `pipeline/line_registry.py`, with a check.
- **A pipeline step never fetches** [#no-fetch]. A fetching drift check
  tests the upstream, not the committed code: Toronto's map lost a storefront
  while its row-count baseline read identical.
- **A removal request is honored, not argued** [#removal], a commitment
  since 2026-09-21. No outside request was found in the files read.

## How the work was organized

**Most process rules arrived after a failure, and many became checks.**

- **DECISIONS and PLAN.** Every judgment call went into the append-only log.
  Since 2026-09-30, build sessions write a drafts file per branch that Cleanup
  folds in. Merges conflicting on DECISIONS.md fell from 144 (09-27 to 09-30)
  to zero after 10-01 (`docs/efficiency_review_2026-10-04.md`).
- **A skill per country after its first city.** Brazil, Taiwan, Japan,
  Korea, France, Czechia and Romania each have one: 31 skill folders and 5
  agents in all. The `osm-rail` meta-rule says why: a warning in Mexico
  City's config did not stop Guadalajara losing Línea 4.
- **Briefs and brief checks.** A brief caches a city's Step 0
  (`docs/build_briefs/`, 229 files), and `scripts/brief_check.py` tests its
  claims before code. The tram kit still found a fault in nine of ten briefs
  whose checks passed.
- **Sessions by role.** Staging, build, app and Cleanup own different paths
  (`docs/session_roles.md`). The split followed a `git add -A` that swept up
  another session's uncommitted work (`docs/rule_history.md`, #sr-why).
- **Review lanes.** The 2026-09-30 mega-review split about 120 cities across
  four lanes on one pinned commit (`docs/review_lanes_2026-09-30.md`). Its
  lessons became `docs/review_lane_kit.md`, used again on 2026-10-07.
- **The heavy-job gate.** On 2026-09-28 one Python process reached 47 GB on a
  16 GB machine and closed the Claude app twice (`docs/rule_history.md`,
  #memory). A per-process cap followed, then `scripts/heavy_job.py`.
- **Batched review time.** On 2026-09-27 the owner chose one review a day and
  one `app/` push per batch. By 10-04, deploy windows had fallen from 9.6 a
  day to 5.9 (`docs/efficiency_review_2026-10-04.md`).
- **Checks before push.** `scripts/check_all.py` is the pre-push hook. It
  passed 57 of 57 at the phase 2 landing (DECISIONS 2026-10-12).

## Costs and efficiency

**Most of the usage went to re-reading long conversations.** The context
review measured 68 sessions, 750 subagent runs and 86,083 model turns to
2026-10-08 (`docs/efficiency_review_2026-10-08_context.md`). Re-reading the
conversation each turn was 80% of price-weighted usage. Two sessions that ran
task after task were 29% of it. By that file's what-if, clearing at task
boundaries would have saved roughly a third.

**The plan upgrades came while sessions ran to the ceiling.** The owner moved
to Max 5x on 2026-09-20 and Max 20x on 2026-09-30. Daily weighted usage was
about flat across the second move: 156M a day, then 144M (same file).

**The two process reviews found the same pressure from two sides:**

- **2026-09-27.** Catch-up merges outnumbered landings, and `app/` landed 9
  to 25 times a day (`docs/efficiency_review_2026-09-27.md`). The weekly
  limit stood at 93% on 09-22; the empty 09-26 "suggests the limit ran out".
- **2026-10-04.** Generated and counted files conflicted on most build
  merges; the master list alone conflicted 57 times that week. The overall
  conflict rate fell from 65% of merges to 25%, while catch-up merges rose
  from 21 a day to 28 (`docs/efficiency_review_2026-10-04.md`).

**The trims held unevenly.** CLAUDE.md went from 4,345 words to 1,685, regrew
to 2,797 by 10-04, and is 1,922 now (`wc -w`). The decisions log, live and
archived, is 674,272 words today (`wc -w`).

## What went wrong, and how it was caught

**Early defects were mostly measurement errors; later ones were framing and
process errors.** That is Band B's reading (`docs/band_b_retrospective.md`,
quoted in `docs/city_master_list_history.md` section 11).

| What went wrong | How it was caught | What changed |
|---|---|---|
| Home businesses published in the first US cities (San Diego 42 to 315 pins) | after the build, by measurement | `check_personal_exposure.py`; a verdict per city |
| Commuter rail left out in every city without saying so | a reader asked whether BART was in | `check_scope_disclosure.py` [#scope-twice] |
| The legend hid the OpenStreetMap credit in 23 cities | a render, not the file | check K and `check_map_attribution.js` |
| A drift check fetched, so Toronto lost a storefront unseen | the baseline said identical | `check_no_fetch_in_steps.py`, `pipeline/offline.py` |
| Canada's and Mexico's sources went unrecorded | a reader, then a script that found five more | `check_provenance.py` [#provenance] |
| iPhones showed blank maps | the owner's phone | a per-literal compile limit found; data shipped as `JSON.parse` (DECISIONS archive 2026-09-27) |
| A 47 GB process closed the app twice | Windows logged low memory | the memory cap and the heavy-job gate |
| A brief swapped Kansas City's name columns | the build re-derived it | three mandatory brief claims proposed (`tram_kit_retrospective.md`, lesson 2; adoption UNVERIFIED) |
| The operator count ran in one tram city of ten | the tram kit's retrospective | gate 3 required in `tram-city` |
| One Kansai line in five colors | the 2026-10-07 review | the line registry and its check |
| Bucharest showed 127 person-named companies by name | a measurement on 2026-10-11 | the name rule extended at the phase 2 landing |
| Mendoza's search index reached 522.2 km out | after the scope check had passed it | rule D, a 25 km reach limit (DECISIONS 2026-10-13) |
| Browser user-agent strings in five probe files | a probe slip on 2026-10-04 | removed; every host serves the project's own agent |

The US retrospective found the asserted version wrong about a third of the
time (`docs/us_build_retrospective.md`); many fixes became a failing script.

## The smaller countries

**Each lesson below is from that country's first build.** The fuller story
sits in the file or skill named.

- **United Kingdom (10).** The Food Standards Agency's register is food only,
  placed at its own point or a postcode center. A private address has
  neither, which keeps home caterers off the map. TfL publishes no GTFS, so
  rail came from OpenStreetMap (`docs/project_context.md`, "London"). The UK
  six then shared one set of steps.
- **Brazil (9).** IBGE's census address file carried a coordinate for every
  establishment, so no geocoder was needed and nine cities shipped as one
  batch. The free-text descriptions needed their own classifier. See
  `docs/geocoding_retrospective.md` and the `brazil-city` skill.
- **Czechia (7).** The register Prague started from records where a company
  is seated, not where it trades. The open-data establishments, from a
  different register, gave the premises. Its lessons are in the
  `czech-tram-city` skill; it wrote no retrospective.
- **The Nordics (Norway 2, Denmark 3, Sweden 2).** Oslo was the first city
  built on a register of premises, not companies. A bulk address register
  replaced about 13,000 planned geocoder calls. Copenhagen's register is a
  join of six national files. Stockholm and Göteborg are food only.
- **Italy (3).** Italy is bespoke per city. Milan keys its taxonomy on which
  of six registers a row came from, because every classification field was
  unusable. Rome joins its premises to the national house-number archive
  and states its food layer as an upper bound.
- **Romania (2).** The county food lists are saved by the owner in a browser,
  and each file is read by its role. A city passes at about 70% placed (the
  `romania-city` skill). Bucharest's name repair is in the table above.
- **Georgia (1).** Tbilisi's register has one row per business, so chains
  are undercounted, as the page discloses. The API has no column selection,
  so personal fields are dropped in memory before anything is saved.
- **Benelux (Netherlands 3, Belgium 6).** Amsterdam set the two-layer shape:
  a hospitality permit register plus the national buildings register's shop
  units. Belgium left Band R on 2026-10-03. The "bulk access paid" verdict
  rested on one national method, and each city had its own layer.
- **Germany (3).** Berlin's register is a chamber of commerce's membership,
  with no names or street addresses. Personal services there are partial.
  `docs/project_context.md` still calls Berlin "Germany's first and only
  city", which is stale since Gelsenkirchen and Bremen landed on 2026-10-07.
- **The rest.** Dublin's register carries no name at all, so the exposure
  check measures nothing there. Riga was the first city whose map changed
  another region's zoom. Hong Kong needed no geocoder, because the license
  read turned up the agency's own points. Buenos Aires places a land-use
  survey by parcel. Sydney and Melbourne use their cities' floor-space
  surveys. Zurich needed a national grid added to the provenance check.

Japan, South Korea and Taiwan are left to the East Asia retrospective named
in `PLAN.md`. Countries with their own files: [US](us_build_retrospective.md)
and its [addendum](us_build_retrospective_addendum.md),
[Canada](canada_retrospective.md), [Mexico](mexico_retrospective.md),
[Spain](spain_retrospective.md), [France](france_batch_retrospective.md),
[Band B](band_b_retrospective.md), [the tram kit](tram_kit_retrospective.md),
[geocoding](geocoding_retrospective.md).

## What is left

**The open work is small and mostly dated.** `PLAN.md` lists five items due
now, among them Sacramento's Green Line frequency and Yamagata's newer food
list. `docs/recheck_calendar.md` runs from Milan's tram timetables on
2026-10-19 to a global re-probe around 2027-10. PLAN.md also holds data
refreshes, eleven known faults and the calls waiting on the owner.

## Lessons

What to do differently on the next project of this kind:

1. **Decide before code from the first city.** Write the briefs, the owner
   calls and a skill before the build, as the tram kit did. The early cities
   will still cost more, because they build the tools.
2. **Make privacy and licenses part of the design, not a repair.** Read the
   terms and drop personal columns before the first pin is drawn, unlike San
   Diego and Los Angeles.
3. **Write a check, not a paragraph.** Provenance and scope disclosure were
   written rules that went unfollowed until a script decided them. Test the
   render where the reader sees it, at more than one size.
4. **Run fewer sessions at once, and regenerate generated files.** Catch-up
   merges and conflicts on counted files ranked first in the two process
   reviews.
5. **Clear context at task boundaries from day one,** worth roughly a third
   of all usage by the context review's what-if.
6. **Batch approvals and deploys from the start.** Batching came in on
   2026-09-27, after `app/` had landed 9 to 25 times a day.
7. **Give briefs mandatory claims:** the name columns, the current routing
   and the projected CRS. A brief check passes only what it is asked.
8. **Gate the machine before running work in parallel.** The memory cap came
   after the app had closed twice.

## What this does not show

- **No cost per city.** No per-city record of hours or tokens exists, and
  commit counts measure cadence, not effort.
- **Usage figures are proxies,** weighted by API price ratios and running
  only to 2026-10-08. They do not convert into plan percentages.
- **Associations, not causes.** DECISIONS conflicts fell when the drafts rule
  came in, but other changes ran at the same time.
- **Nothing was checked live.** This draft reads the repository only, so it
  does not show that the deployed site matches master.
- **Daily counts are first-parent counts:** a city appears on the day it
  landed, not the day it was built.
- **Japan, Korea, Taiwan, place search and the transit layer** are covered
  only in outline, pending their own retrospectives.
- **UNVERIFIED:** why no commits exist on 2026-10-09 and 10-10; whether any
  outside removal request was ever received; whether the tram kit's
  mandatory brief claims were adopted.
