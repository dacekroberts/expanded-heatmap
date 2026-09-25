# Global city master list — CURRENT STATE

**This is the operative list: which cities this project could build next, and
what is stopping each one.** It is rewritten as things change, like
`docs/project_context.md` and unlike `DECISIONS.md`.

**The evidence lives in [`docs/global_country_shortlist.md`](global_country_shortlist.md)** —
87 countries screened, every probe logged, every negative with the measurement
behind it. That file is the trail; this file is the answer. When they disagree,
the trail wins and this file is stale.

**Drift-corrected 2026-09-23**, after Marseille was built: counts, the band
table, Marseille's row, Hong Kong's geocode rate, Göteborg's row count, Cairo
(moved out of the discards onto the open screening gap, by this file's own
rule) and the by-country view, which had stopped being current a day earlier.

Last reordered **2026-09-22**, after the browser sweep — Tier 5 closed
(7 negatives, no survivors), Tier 6 reached for the first time, and three
food-authority probes run. **Stockholm** and **Bucharest** were promoted out
of the band that used to read *"never actually reached"*; five cities moved to
discarded on measurement.

**The method that produced all of it:** open the portal in a real browser
*before* concluding anything about it, then enumerate providers rather than
search keywords. Both are written up in `.claude/skills/add-country/`
(§3 and §2) and `add-city` Step 0.

---

> ## ✅ Settled state — 2026-09-22
>
> **Every candidate on this list has a measured business leg, a named next
> step, and no unexamined route.** Nothing here is carried on a guess, a
> search result, or a host that was never asked properly.
>
> | | |
> |---|---|
> | **Built** | **44** across 16 countries *(Seoul and Taichung, 2026-09-25; Riga, Hong Kong and Rotterdam, 2026-09-24; Toulouse, Lille (Regional) and Rennes, 2026-09-23; Oslo, Copenhagen, Prague, Amsterdam and Rome, 2026-09-24; Brazil's nine cities as one batch, 2026-09-24)* |
> | **Candidates** | **22**, all at least partially viable — A 8 · B 0 (closed) · C 7 · D 7 *(**Seoul and Taichung built 2026-09-25**, leaving Band A; **the open gap emptied 2026-09-24 after a final re-probe, owner's calls**: Riga to A (tram rings, scoped vacancy disclosure), Yokohama to C (personal services only, no page for now), Lisbon, Helsinki and Tallinn to D, Vienna, Santiago and Nagoya to the discards; **Hong Kong, Rotterdam and Brazil's nine built 2026-09-24**, leaving Band A by being built; Kyoto from the open gap to A 2026-09-24 — its register rebuilt from the permit stream, owner's call; **Japan re-banded 2026-09-24 and the geocoding band closed** — Tokyo (8 wards), Osaka, Kobe, Sapporo and Fukuoka to A, Hiroshima to C, Sendai to D, Yokohama, Nagoya and Kyoto to the open gap; Rotterdam from the open gap to A; all owner's calls; Warsaw and Hyderabad to D 2026-09-24 from the open gap, owner's calls — each geo-blocked before measurement; Copenhagen, Prague, Amsterdam and Rome built 2026-09-24; Amsterdam to A 2026-09-24 — permits + BAG shop units, both licences read, owner's call; Amsterdam from the discards to C earlier the same night; Rome to A 2026-09-24 — SUAP premises joined to ANNCSU, owner's call with a build check; Prague back to A 2026-09-24 on open data — ROS02 establishments + RES; Kaohsiung moved from B to a reopened access-blocked band D 2026-09-23, owner's call; Brazil re-screened 2026-09-23: +7 cities, and São Paulo and Rio moved from B to A; Taipei (Regional), Taoyuan and Taichung moved from B to A the same evening; Rennes built; Prague paused to the open gap 2026-09-24)* |
> | **Open screening gap** | **0** — **emptied 2026-09-24** by a final re-probe of its last eight, each given a verdict (owner's calls) *(before that: Kyoto out again to A later the same day, on a rebuilt register; Yokohama, Nagoya and Kyoto in, Rotterdam out to A, 2026-09-24; ten left 2026-09-24 on the owner's calls after their re-probes: eight to the discards, Warsaw and Hyderabad to D)* |
> | **Discarded** | **27**, each naming its evidence *(Vienna, Santiago and Nagoya from the open gap 2026-09-24 after the final re-probe, owner's calls; Kuala Lumpur, Athens, Poznań, Bratislava, Hamburg, Naples, Lima and Messina from the open gap 2026-09-24, owner's calls after their re-probes; an audit moved 12 single-method rows to the open gap and Amsterdam to Band C, 2026-09-24; the evidence check moved 5 more the same night)* |
>
> *Counts corrected 2026-09-23. This box had read 20 / 33 / 30 since
> 2026-09-22 while the sections below moved on — **the hand-kept summary is
> the first thing to drift, which is why the band sections are the ones to
> trust.***
>
> **What this day changed.** Four bands closed because their condition stopped
> being true of their members. **Seven cities were reached by going to a
> different HOST rather than a different network** — Sofia, Sevilla, Tel Aviv,
> Tallinn, Prague, Dublin and Hong Kong — and *unreachable* turned out to mean
> *not yet asked properly* in every single case.
>
> **Three recorded negatives turned out to be statements about a SEARCH rather
> than about the data**: Stockholm's register is called `Tillsynsverksamheter`,
> a word no query contained; Zurich's catalogue was matched over 938 of 1,128
> names; Hong Kong's bulk export was on `data.gov.hk` the whole time and the
> dataset list had never been requested. **Each cost one HTTP call to
> disprove.** India was then swept in full — 288,011 titles — specifically so
> it would not become the fourth.
>
> **This claim is dated because it will stop being true.** The next probe, the
> next build, or the next licence read changes it, and the counts in the table
> below are the ones to trust over any prose that repeats them.

## Built — 44

| Country | Cities |
|---|---|
| **United States** (9) | San Diego · San Francisco · Los Angeles · Chicago · New York · Philadelphia · Miami · Boston · Washington D.C. |
| **Canada** (5, complete) | Vancouver *(with Surrey)* · Montréal · Calgary · Edmonton · Toronto |
| **Mexico** (2) ✅ | **Mexico City** · **Guadalajara (Regional)** — built 2026-09-22, live in the app |
| **Europe** (16) ✅ | 🇱🇻 **Riga** — **built 2026-09-24**, Latvia's first (`pages/42_Riga_Heatmap.py`; **6,730 storefronts, 108 stations**, Rīgas satiksme's seven tram routes): food from the State Revenue Service's excise-licence register, joined to the city's own address points (96.8%), and shops and services from the cadastre's trade premise groups at their building footprints (99.4%); the vacancy disclosure scoped to the historic centre, and a Europe view that keeps its zoom with Riga a pan away on phones (owner). · 🇪🇸 **Madrid** · **Barcelona** · 🇮🇪 **Dublin (Regional)** · 🇮🇹 **Milan** · **Rome** · 🇫🇷 **Paris** · **Marseille** · **Toulouse** · **Lille (Regional)** · **Rennes** · 🇳🇴 **Oslo** · 🇩🇰 **Copenhagen** · 🇨🇿 **Prague** · 🇳🇱 **Amsterdam** · **Rotterdam** — **Rotterdam built 2026-09-24**, the Netherlands' second (`pages/40_Rotterdam_Heatmap.py`; **7,520 storefronts, 132 stations**, RET metro A–E and trams 1–8 and 11, gemeente only): Amsterdam's shape with the food layer REBUILT from the permit decisions Rotterdam publishes in its Gemeenteblad (1,939 premises), BAG shop units for the rest, and the metro and tram network measured on the timetable after a works period whose temporary trams 14 and 18 had looked like permanent lines. **Rome built 2026-09-24**, Italy's second (`pages/30_Rome_Heatmap.py`; **98,897 storefronts, 87 stations**, Metro A, B, B1 and C and the Roma–Viterbo urban service, comune only): Roma Capitale's SUAP premises register JOINED to ANNCSU house numbers at 95.7%, no names, and the food layer stated as an upper bound (2.67x OSM, no closing dates). **Amsterdam built 2026-09-24**, the Netherlands' first (`pages/29_Amsterdam_Heatmap.py`; **13,238 storefronts, 144 stations**, GVB metro 50–54 and 16 tram lines, gemeente only): the city's live hospitality-permit register for food, the BAG's shop-class units for everything else - one "Shops and services" category, because a building register cannot tell a hairdresser from a clothes shop - de-duplicated by address, and trams thinned with the sub-transit-line filters. **Prague built 2026-09-24**, Czechia's first (`pages/28_Prague_Heatmap.py`; **25,275 storefronts, 58 stations**, metro A, B and C): ROS02's establishments where they trade, the owner's activity from RES's CZ-NACE 2025, a RUIAN join for the point, and every natural person's or partnership's name replaced by its address - their premises at the owner's own seat left off. **Copenhagen built 2026-09-24**, Denmark's first (`pages/27_Copenhagen_Heatmap.py`; **14,978 storefronts, 64 stations**, Metro and S-tog, Copenhagen with Frederiksberg): CVR production units joined across six national files, coordinates JOINED to DAR, and every personally owned business shown by its address. **Oslo built 2026-09-24**, Norway's first city (`pages/26_Oslo_Heatmap.py`; **10,718 storefronts, 155 stations**, T-bane and trams, kommune only): an establishment register keyed on the PHYSICAL location address, coordinates JOINED to Kartverket's bulk address file, and every sole trader's name replaced by its address. the first four built and deployed 2026-09-22, Paris deployed 2026-09-23, **Marseille built and deployed the same day** (`pages/22_Marseille_Heatmap.py`; **18,177 storefronts, 66 stations**), **Toulouse** likewise (`pages/23_Toulouse_Heatmap.py`; **8,635 storefronts, 48 stations**), **Lille (Regional)** likewise (`pages/24_Lille_Heatmap.py`; **11,833 storefronts, 91 stations**) — **the first French city scoped regionally**, to the eleven communes its network serves, because the commune alone would have drawn the tram as a three-stop stub — and **Rennes built and deployed the same day** (`pages/25_Rennes_Heatmap.py`; **3,479 storefronts, 24 stations**), commune-only because its worst line keeps 11 of 15 stations, **which completes France at five cities**. **France is the first country here where the second city was materially cheaper than the first**: Marseille inherited the national register, the NAF taxonomy, the parquet cache and the Lambert-93 grid, and its own work was the scope measurement and the rail leg. That is Mexico's retrospective repeating, and the opposite of Spain's. **Toulouse made the third city cheaper again**: it downloaded nothing at all, because the 3 GB national parquet pair was already cached for the country, and its own work was one scope decision, one owner call, and a gate-3 run that matched the operator exactly on all four lines. It is also the first city anywhere here to draw a **non-rail mode** — the Téléo cable car — which was the owner's call after the brief's stated precedent for it turned out not to exist. **One macro-map region, not one per country**: Spain, Ireland and Italy were three regions holding four cities until they were collapsed the same day, which is what let France join without adding a sixth region. Spain is complete at two cities, Ireland at one, and Italy is a Milan-only country — so the countries are still the research unit, and only the MAP groups them. ⚠️ **France's own viability figure was corrected on the day Paris was built**: the recorded "50,156 storefronts, 92.5% of OSM" is not reproducible and the real ratio is about 1.78× — see `docs/build_briefs/paris.md`. France remains a build; `docs/global_country_shortlist.md`'s France row still carries the old number |
| **South America** (9) ✅ | 🇧🇷 **São Paulo** · **Rio de Janeiro** · **Belo Horizonte** · **Brasília** · **Salvador** · **Fortaleza (Regional)** · **Porto Alegre (Regional)** · **Recife (Regional)** · **Santos (Regional)** — **built 2026-09-24 as one batch** (`pages/31`–`39`; **617,188 storefronts, 363 stations**), the first country built that way: every city to drafts, one review of all the text, one deploy check and one push. One national source, IBGE's CNEFE 2022 - the census's walk of every block, each establishment with the enumerator's description and a coordinate - read by a free-text classifier (`pipeline/taxonomies/brazil_cnefe.py`); unreadable descriptions dropped and disclosed, and only the category shown at an address that is also a home. Commuter lines went through the three-part rail test: São Paulo's CPTM Linha 9 and Rio's SuperVia Deodoro and Saracuruna drawn, the rest out. The macro map's **South America** region |
| **East Asia** (3) ✅ | 🇹🇼 **Taichung** — **built 2026-09-25**, Taiwan's first (`pages/44_Taichung_Heatmap.py`; **66,115 storefronts, 18 stations**, Taichung Metro's Green Line): the national business tax register joined to the city's door plates (92.2%), keyed by district because one street name recurs across districts; office-like company head offices dropped and unmarked sole proprietors shown by their line of business (owner's rules). The national modules and the `taiwan-city` skill came out of it. · 🇰🇷 **Seoul** — **built 2026-09-25**, South Korea's first (`pages/43_Seoul_Heatmap.py`; **239,410 storefronts, 308 stations**, Lines 1–9, Shinbundang, Ui LRT, Sillim and three Korail lines): seventeen of Seoul's citywide permit registers, each premises at its own building point or at another permit's at the same building (98% placed), one pin per premises with the five convenience-store chains matched by brand, and a Korean personal-name pass that withholds 138 names at home addresses. Rail from OpenStreetMap, since Korea's station dataset has no lines. · 🇭🇰 **Hong Kong** — **built 2026-09-24** (`pages/41_Hong_Kong_Heatmap.py`; **21,135 storefronts, 141 stations**, MTR's eight urban lines and the Light Rail): FEHD's three licence registers, each licence at FEHD's own point from the same registers on the CSDI Portal - the brief's address geocode was never needed - and a map that is mostly restaurants, because Hong Kong licenses food and not general retail. Rail from OpenStreetMap, since MTR publishes no geometry; gate 3 exact against MTR's own station lists. The macro map's **East Asia** region, named for the Taiwanese, Korean and Japanese cities behind it |

✅ **Mexico is the first country built outside North America's anglophone
pair**, and the first where the rail leg came from **OpenStreetMap** rather
than an agency feed — the per-city exception approved for CDMX, which
validated at 195/195 stops exact.

✅ **Spain is the first country in EUROPE**, and the first where the two cities
did not generalise to each other in any leg. Different rail sources (Madrid
takes CRTM's own ArcGIS layers, Barcelona OpenStreetMap), different projected
CRS (25830 against 25831), different taxonomy LEVELS of similar four-level
schemes — Madrid keys on its division, Barcelona on its finest level, and each
for a measured reason. Both carry the same accommodation trap and it bites at a
different depth in each. Barcelona is also the first source in the project to
impose an obligation that is **an act rather than a notice**: its terms require
the City Council to be informed of every derived project.

## Candidates — 22

Re-tiered 2026-09-22 after the browser sweep closed Tier 5 and reached Tier 6.
**Eight cities moved to discarded on measurement** and **two were upgraded**.

**Four of those were sitting in Band D as "unreachable", and all four were
reached by going to a different HOST rather than a different network** —
Sofia via `data.europa.eu`, Sevilla and Tel Aviv via the ArcGIS service host
behind a walled portal, Tallinn via a bulk export its catalogue entry named.
Three then measured negative and **one, Tel Aviv, is now the strongest
unbuilt candidate outside Band A.** *Unreachable* turned out to mean *not yet
asked properly* in every single case.

**Re-banded 2026-09-22 so that every caption names the kind of work that
unblocks its cities**, after an audit found five rows whose text named a
blocker their band did not. Band D dissolved: its two live sub-tiers were
about different things and were siblings only because both arrived through
the same screen.

**The one-bucket band (now D) was added the same day** for a state the scheme
could not express: a city whose screening is **complete and successful** but
which yields only one bucket. Those two were sitting in "a decision to make"
beside a city waiting on a licence read, which conflated *we have not looked
yet* with *we looked at everything and this is what is there*.

| Band | What these cities ARE | Cities |
|---|---|---|
| 🟢 **A** | **Ready to build.** Register measured, licence read, coordinates answered, rail answered — every remaining question is answerable inside the build | **10** *(+ 28 built)* |
| ~~🟠 **B**~~ | ~~**Geocoding at national scale.**~~ **CLOSED 2026-09-24**: Japan's address work was a join, so the condition stopped being true of all ten | **0** |
| 🟣 **C** | **One bucket only.** Screening complete and successful; the map would be narrower than the others | **7** |
| 🔴 **D** | **Access blocked by the publisher.** Screening complete, the file exists and is measured; the publisher's own access control is the only thing stopping it, so it is unblocked by ASKING, not by probing *(Warsaw and Hyderabad, 2026-09-24: blocked before measurement — a read from inside the country first; Sendai, 2026-09-24: the city's permission; Lisbon, Helsinki and Tallinn, 2026-09-24: a free account, and two geo-blocks)* | **7** |
| | **Candidates** | **24** |
| *Open gap* | Unscreened — a row resting on an absence, so not a discard | *0 (emptied 2026-09-24)* |
| *Discarded* | Measured negative, evidence named | *27* |

*Band A's caption briefly said "brief written" (2026-09-23, morning). That was
wrong by `CLAUDE.md`'s own rule — **a brief is a cache, not a prerequisite** —
and it was removed the same day, when nine Brazilian cities met every other
condition without one.*

⚠️ **This table read A 9 / B 10 / C 12 / D 2 until 2026-09-23** — the
pre-renumber counts, left standing under two renumbers that each updated the
section headings below and not this summary. **The headings were right; the
table summarising them was not.**

**Renumbered 2026-09-22 to close the gaps left by four band closures.** The
live set is now contiguous, and **the closed bands have lost their letters
rather than keeping them** — a closed band's letter was never the interesting
part of it, the condition that stopped being true is.

| Old letter | Now | Why it changed |
|---|---|---|
| A | **A** | unchanged |
| **C** | **B** → *(2026-09-23: absorbed into A)* | Hong Kong, Prague, Taiwan ×4, Bucharest, Singapore, Oslo, Copenhagen |
| **E** | **C** → **B** *(2026-09-23)* | Brazil ×2, Japan ×10 |
| **F** | **D** → **C** *(2026-09-23)* | Stockholm, Zurich |
| B | *(closed)* | **awaiting permission** — Tel Aviv, discarded on terms |
| D | *(closed)* | **coordinates and unfinished screening** — Bucharest finished its screening |
| G | *(closed)* → **D** *(2026-09-23, reopened)* | **access blocked** — Hong Kong left upward, Hyderabad and Kochi measured out; **the condition came back true of Kaohsiung**, so it is a live band again under the next free letter |

**Rule this renumber established: a LETTER is for a heading, a CONDITION is
for a sentence.** Prose that says *"moved to the coordinates band"* survives
any renumber; prose that says *"moved to Band C"* does not, and four such
sentences went stale the moment the letters shifted. They have been rewritten
to name conditions.

**Renumbered again 2026-09-23, and this time a band closed by SUCCEEDING.**
The coordinates band existed to hold cities whose coordinate route was
unmeasured. All four of its last members ended up with the route measured AND
a brief written, so the condition stopped being true of every one of them and
the band was absorbed into **A** rather than re-captioned. `C` and `D` moved
up to `B` and `C` behind it.

⚠️ **Several sentences written on 2026-09-23 named LETTERS and went
stale within hours of being written** — including two in the Bucharest and
Singapore sections added that same day. They have been rewritten to name
conditions. **The rule above is easy to agree with and easy to break in the
next paragraph.**

⚠️ **`DECISIONS.md` is append-only and names bands by their letter at the time
of writing.** Those entries remain true of the moment they describe; this
table is how a reader resolves them. **Nothing in the log was edited.**

**Re-banded 2026-09-22 so each caption describes what its cities ARE**, not
how they were found. The previous Band C had grown to 21 cities whose only
shared property was "needs coordinates" — while the **cost** of that step
ranges from Prague's RÚIAN lookup to Japan's chōme/ban/gō. That is the
largest single ranking fact in this list, and one band was hiding it.

**Band D held Bucharest alone** while its business leg was unfinished. On
2026-09-22 it finished — **rail counted (12 relations, M1–M5), licence read
(SILENT), Romania's catalogue enumerated (4,693 datasets, no second
bucket)** — so the city moved to C and the band closed. **A band whose
condition stops being true of its last member should close, not be
re-captioned around the occupant.**

**A caption names a blocker, never a date or a status.** `D-a` was briefly
captioned *"all four PROBED 2026-09-22"*, which reads as progress and is
unauditable — Rio's misfiling was caught only because the sub-tier beside it
still declared what it was *for*.

✅ **Guadalajara and Mexico City left Band A by being built**, not by being
ruled out. Their rows are kept below, marked, because a built city's Band A
entry is the only place the screening promise and the delivered build sit
side by side.

**Net: the screen got smaller and more honest.** Nothing was lost that was
ever measured as viable — the five drops were all cities whose business leg
had never been tested, and testing it is what removed them.

**Two cities were promoted the same day**, both by the same method and both
out of the band that used to read "never actually reached": **Stockholm** to B
and **Bucharest** to C. The tier that looked deadest produced the two best new
results in the sweep.

---

## 🟢 Band A — ready to build (10 ready + 28 ✅ BUILT)

✅ **Riga BUILT 2026-09-24** (6,730 storefronts, 108 stations). ▲ **Riga 🇱🇻 joined 2026-09-24 from the open gap (owner's call)**, the eleventh. Amsterdam's
two-layer shape:
- **Food**: the State Revenue Service's excise-licence register, 1,596 premises, 96.2% joined to
  Riga's address points, CC0.
- **Shops**: the cadastre's class-1230 premise groups, 4,816 named shops, 99.5% on building
  outlines, CC BY 4.0.
- **Rail**: all 7 Rīgas satiksme tram routes (GTFS, CC0; 125 stations, every one inside the city;
  5–10 minute headways on routes 1, 7 and 11). Colours come from the operator's route maps,
  because OSM and the GTFS give every route the same red. The rings hold 78.5% of the shops and
  82.6% of the food premises. All five Vivi suburban corridors are out on frequency (15–30
  minutes at best).
- **The page carries the scoped vacancy disclosure**: 20.4% of 2,324 centre premises (2024), 15%
  in the Old Town (2025), and not measured elsewhere, about 62% of in-ring shops. Quote the
  municipal report's own definitions: its headline is 73% occupied.
- ✅ **Brief written 2026-09-24**: `docs/build_briefs/riga.md` (4/4). **Builds next, before
  Taiwan** (owner's call, 2026-09-24): a small build that fits the week's remaining budget.
- ⚠️ **Its licences are NOT yet read**: the excise register and the Rīgas satiksme GTFS (both
  declared CC0 on `data.gov.lv`), the VZD cadastre (declared CC BY 4.0), and the address points.
  None has a row in `docs/data_sources.md`, so Band A's "licence read" condition is not met
  yet. Corrected 2026-09-24, the same evening it moved here. Run the reads before the build.

**The ten:** ~~Seoul~~ ✅ **built 2026-09-25** · ~~Hong Kong~~ ✅ **built 2026-09-24** — **each with a brief** in `docs/build_briefs/` — ✅ ~~nine
Brazilian cities~~ **built 2026-09-24** (below) — **three Taiwanese cities**: Taipei (Regional) (6/6) ·
~~Taichung~~ ✅ **built 2026-09-25** · Taoyuan (3/3) — ▲ **and seven more on 2026-09-24**: **six Japanese cities**, Tokyo (8 wards) (7/7) ·
Osaka · Kobe · Sapporo · Fukuoka (4/4 each) · Kyoto (8/8), and ~~Rotterdam~~ ✅ **built 2026-09-24**. ✅ **Every Band A city has a brief** (Riga's written 2026-09-24), and
every brief's checks pass live *(Fukuoka's BODIK host is flaky — re-run before correcting)*.

### ▲▲ Taiwan — three cities, one tax register, a door-plate JOIN (2026-09-23)

**Taiwan left the geocoding band the same way Brazil did: the address file
already carries the coordinate.** Each city publishes a keyless monthly
**door-plate coordinate file** (`門牌位置數值資料`), and the national **business
tax register** (Fiscal Information Agency, daily, one row per trading
location, branches as their own rows) joins to it by parsed street / lane /
alley / number. Full evidence: `global_country_shortlist.md`, "Taiwan
finished".

| City | Storefronts | **Joined** | Rail — keyless agency data |
|---|---|---|---|
| **Taipei (Regional)** — Taipei + New Taipei | **152,839** (76,519 + 76,320) | **93.9%** (92.4% · **95.5%**) | Taipei's network map (GeoJSON line geometry, `RouteName`) and station points; Taipei Metro's station tables |
| **Taichung** | **73,227** | **92.7%** | Taichung Metro Green Line stations (lat/lon); lines from OSM |
| **Taoyuan** | **49,282** | **94.0%** | Taoyuan Metro network XML; the national `捷運車站` layer (the railway bureau's own airport-MRT file is behind an Incapsula challenge — not worked around) |

**Taipei is REGIONAL, like Dublin and Lille:** New Taipei completely surrounds
it and the metro crosses the boundary on several lines, so a Taipei-only page
would cut the network where no rider notices.

**Decided by the owner, 2026-09-23:**
- **OGDL v1's fault-based liability clause — ACCEPTED for all of Taiwan** (one
  decision covers the door plates, the tax register and the agency rail).
- **Names: shown only when they are a TRADE name** — for companies and
  branches, and for sole proprietors only when the name carries a business
  marker (行/店/社/館/坊…); otherwise the category. The FIA itself refuses to
  publish owners' names, and for 4.9% of Taipei's storefronts the business
  name reads as the owner's.
- **The attribution statement is load-bearing**: OGDL v1 §三(二) voids the
  grant retroactively without it.

**For the build, measured, not decided:** company head-office rows — **38.7%
of Taipei's company rows sit on a 3rd floor or higher or carry a room
number**, against 7.1% of sole proprietors; market stalls — genuine premises
with no door plate, most of Taipei's retail misses; and **TDX is not used**
(key-gated since at least 2026-09-23; registration wants a Taiwanese mobile
number).

### ▲▲ Brazil — nine cities, one census file, no geocoder (2026-09-23)

✅ **ALL NINE BUILT 2026-09-24, as one batch** - see the Built table above and
`DECISIONS.md`. The screening figures below are the screen's, kept beside the
build as the promise it was measured against; the built counts differ because
the build added the rules-version-2 fallback, placement and scope.

**Brazil left the geocoding band by not needing a geocoder.** It was carried as
*"CNPJ plus geocoding past Toronto's scale"*. Two measurements replaced that:

- **CNPJ is unreachable from outside Brazil.** Receita moved it to a Nextcloud
  share in early 2026 and the host resets every non-Brazilian connection —
  **16 check nodes, the Brazilian one 200, the other 15 in 11 countries
  reset.** A publisher's access control, so this project does not route
  around it.
- **IBGE's CNEFE 2022 is a premises field survey.** The census address file
  records, for every non-residential address, `DSC_ESTABELECIMENTO` — the
  enumerator's identification of the establishment — with a **coordinate
  taken at the address**. National, keyless, one schema. Licence: **free use
  by federal law** (Decree 8.777 art. 4, Lei 14.129 art. 29), credit required,
  LGPD applies — see `docs/data_sources.md`.

Both cities' own portals were enumerated first and are **measured negative**:
São Paulo's 483 CKAN packages and 483 GeoSampa layers hold no business
register; Rio's `Estabelecimentos Abertos` is the **aggregate trap** — counts
per street × activity group × year of concession.

**Screened with `scripts/screen_cnefe.py`**, which classifies the free text
into the NAICS-bounded buckets (head-noun rules plus an edit-distance pass for
enumerator misspellings). Every figure is from the city's own file:

| City | Mapped storefronts | Retail / Food / Personal | Dropped as unclassifiable | Enumerator's own coordinate | Rail (OSM) — what the build must settle |
|---|---|---|---|---|---|
| **São Paulo** | **216,037** | 108,265 / 66,467 / 41,305 | 19.7% — **13% periphery → 31% Pinheiros** | 98.5% | GeoSampa WFS, 94 stations / 6 lines, EPSG:31983 |
| **Rio de Janeiro** | **105,350** | 50,423 / 35,509 / 19,418 | 20.0% — 15% → **36% Barra da Tijuca** | 95.1% | 20 relations, all named and coloured |
| **Salvador** | **52,258** | 25,890 / 17,186 / 9,182 | 21.6% — 15% → 29% | 97.3% | L1 + L2, **0 of 4 relations coloured** — colours from the operator. No public agency layer (SEMOB's folder is token-gated). **20 of 21 stations in the city** |
| **Fortaleza (Regional)** | **62,792** (city 49,503) | 29,239 / 11,470 / 8,794 | 25.9% — 20% → **43% Meireles** | 98.5% | Sul (metro) + Oeste, Parangaba–Mucuripe (light rail), all coloured. No agency layer reachable (Metrofor's certificate expired). 31 of 41 stations in the city — **regional, decided 2026-09-23**: + Caucaia, Maracanaú, Pacatuba |
| **Belo Horizonte** | **44,923** | 22,518 / 13,127 / 9,278 | 22.8% — 22% → 30% | 98.8% | L1 + **Linha 2, opened 2026-07-03 with two stations — OSM lists exactly those two**. Agency lines (2022, pre-L2), no agency stations |
| **Brasília** | **35,824** | 19,706 / 9,164 / 6,954 | 26.7% — 16% → **48% Asa Sul** | 99.9% | Metrô-DF Verde + Laranja, coloured. **Agency stations + lines with status** (IPEDF GeoServer; **public domain, READ 2026-09-24**, backed by DF decree 38.354/2017) |
| **Recife (Regional)** | **43,518** (city 25,212) | 14,968 / 5,622 / 4,622 | 29.2% — 19% → 32% | 99.0% | Centro 1 & 2 + Sul, coloured; plus a diesel VLT to Cabo. **CBTU file: 36 stations + lines** (ODbL, READ 2026-09-24 — as a cross-check it carries no obligations). 19 of 36 stations in the city — **regional, decided 2026-09-23**: + Jaboatão, Cabo, Camaragibe |
| **Porto Alegre (Regional)** | **35,688** (city 18,798) | 10,576 / 4,599 / 3,623 | 27.9% — 23% → 40% | 98.1% | Trensurb, coloured. No agency layer. Only 7 of 23 stations in the city — **regional, decided 2026-09-23**: + the Trensurb corridor to Novo Hamburgo |
| **Santos (Regional)** | **11,691** (city 6,021) | 3,322 / 1,769 / 930 | 25.0% | 98.1% | VLT L1 + L2, coloured; tourist tram excluded. Stops layer of unconfirmed ownership. 17 of 25 stops in Santos — **regional, decided 2026-09-23**: + São Vicente |

**Four decisions taken by the owner the same day**, recorded in `DECISIONS.md`:
proceed on the federal-law grant with four restrictive readings recorded; at
any address that also holds a **dwelling, show the category, never the
description text**; accept the **2022 vintage** and disclose it (Barcelona's
precedent); and disclose that a **shopping centre collapses to one to a few
rows** (0.1–0.2% of mapped rows stand for more than 10 establishments).

⚠️ **The dropped share is not uniform, and every page must say so.** Bare
trade names with no category word (`MUNDO VERDE`, `RED CELL`) cannot be
bucketed honestly and are dropped — and **affluent commercial districts use
them far more**. The map therefore **under-draws its richest districts**, worst
in **Brasília's Asa Sul (48%)** and **Fortaleza's Meireles (43%)**. That is a
bias to state on the page, or to reduce with a better classifier; it is not a
reason to key everything to Retail, which is the guess `premises-taxonomy`
forbids.

⚠️ **Brasília's addresses name a block, not a door — MEASURED 2026-09-23.**
The 89.7% of its storefronts that "share an address with a dwelling" is the
key's artefact: 98.5% of those rows have no door number, and the unit is the
`LOTE` complement. **Keyed on the lot: 58.0%. On the identical coordinate:
18.8%** (Recife 20.3%);
**decided by the owner 2026-09-23: key on the lot where the number is blank** —
now in `screen_cnefe.py`, **68.9%**. **9%** of rows still stand for more than
one establishment.

**Not carried forward:** Teresina, Maceió, João Pessoa and Natal have rail in
OSM, but it is single diesel lines or CBTU suburban trains tagged
`light_rail` — the commuter shape this project excludes everywhere. **Not
downloaded, not discarded:** ASSERTED from the rail screen, and one download
each settles it. **Cuiabá** returned 0 relations (its VLT was abandoned) and
**Curitiba**, the negative control, returned only a tourist train.

**Every question these cities carry is answerable inside the build**, not
before it. Nothing here needs a probe, a document or a decision first.

**▲ France's other five cities were added on 2026-09-22.** The Tier view had
said *"France — 6 cities"* since the country was resolved, while the band
view showed only Paris — **so this list understated France by five cities for
as long as both views existed.** They share one national register, one
licence and one filter with Paris, and their geolocation was measured per
commune rather than inherited.

> ⚠️ **Dublin's row was wrong in four places until 2026-09-22**, corrected
> from `docs/build_briefs/dublin.md` after Step 0 measured it live. All four
> errors share one root: **the screening probe reported the slice it happened
> to query as if it were the whole.** It queried **one** authority and **six**
> categories, then quoted the total as Dublin's; it quoted the length of the
> *national* category list as the number present in Dublin; it computed 100%
> coordinates over only the rows it had pulled; and it counted colours across
> all 42 OSM relations including the Commuter and InterCity services a build
> would drop. **Every number was true of the query and false of the city.**

Ordered by how little stands in the way. **Built cities keep their row**,
struck through and marked ✅, so the band still shows what screening promised
and whether it held.

| # | City | Business leg | What remains |
|---|---|---|---|
| ✅ | ~~**Guadalajara**~~ 🇲🇽 | DENUE, SCIAN = NAICS, INEGI licence cleared | **BUILT 2026-09-22** — `pages/16_Guadalajara_Heatmap.py`, region *Mexico*. Screening said "nothing outstanding" and that held |
| ✅ | ~~**Madrid**~~ 🇪🇸 | **53,355 clean storefront rows** — retail 36,224 · food 18,194 · personal 9,974 (from 225,660 join rows → 159,787 open → filtered). Three-level taxonomy on `division`, EPSG:25830, CC BY 4.0 | **BUILT 2026-09-22** — `pages/17_Madrid_Heatmap.py`, region *Spain*. Rail from **CRTM's feature layers**: 13 lines, 293 station-line records, 49 stations excluded, 0 filter disagreements. Screening said the rail leg was the open question and CRTM answered it |
| ✅ | ~~**Dublin**~~ 🇮🇪 ▲▲ **REGIONAL** | **38,265 rateable rows across FOUR local authorities → 13,945 storefront** (Dublin City alone: 19,810 → **8,016**). **13 use categories region-wide, 12 in Dublin City.** **99.87% carry `Xitm`/`Yitm`** — Irish TM, already in metres; 51 of 38,265 missing, **46 of them pubs**. Per-row `Category` **and** `Uses`, plus `ValuationReport[].FloorUse`. `Eircode`. **CC BY 4.0, no key** | **No geocoding leg.** Build is the **Vancouver + Surrey shape** — four authorities, not one city. Rail: the three drawn lines (**Luas Red, Luas Green, DART**) all already carry an OSM colour; Commuter and InterCity are **dropped**. ⚠️ **36% of its storefronts are near no rail of any kind** — a scope fact to state on the page, not a defect. Brief: `docs/build_briefs/dublin.md`, **6/6**  — **✅ BUILT 2026-09-22** — the regional shape (four local authorities) held |
| ✅ | ~~**Seoul**~~ 🇰🇷 | **17 citywide permit registers**, all 25 gu, EPSG:5174, KOGL Type 1 on all 17: about **157,000 food, 53,000 retail and 40,000 personal-services premises** | ✅ **STEP 0 COMPLETE 2026-09-24** (`docs/build_briefs/seoul.md`, 4/4 checks). Nine retail and bar registers were found by an OA-id sweep. Restaurant coordinates go from 90.7% to **97.7%** by borrowing points from the register's own rows at the same building (control: median 0 m). The Korean exposure check is sized at 113 premises. Rail: 369 stations, 3 light-rail lines; the earlier "0" was a failed query. ✅ **Owner's four calls decided 2026-09-24**: the buckets (karaoke bars in Food service), 경의·중앙, 수인·분당 and 경춘 drawn, stations inside Seoul only, and the East Asia region Hong Kong creates. **Ready to build** — **✅ BUILT 2026-09-25** (`pages/43_Seoul_Heatmap.py`, region *East Asia*) |
| ✅ | ~~**Milan**~~ 🇮🇹 | **Three layers, one per bucket — the bucket comes from WHICH LAYER a row is in, not from a code.** `ds49` **28,131** retail · `ds59` **3,799** food service · `ds62` **5,732** personal services. All three **CC-BY**, all updated **2026-08-31**, all with `LONG_X_4326`/`LAT_Y_4326` | **Schemas captured 2026-09-22 — and the fill rates correct this row's old claim.** Coordinates are excellent (99.1% / 92.2% / 98.8%) and location is complete (`Ubicazione` 100%). **But the columns that were cited as making this the richest source in the screen are mostly EMPTY**: `insegna` **17.6%** on retail and **9.1%** on food, `codice_ateco` **7.1%**, and `ds62` has **no name field at all**. `settore_merceologico` is 99.5% but binary — *alimentare / non alimentare*; `tipologia` is 100% and single-valued. **Owner decision: a map where ~82% of retail pins carry no trade name.** Not a blocker — bucketing works by layer, and fewer published names is a privacy asset — but it is a choice, not a detail — **✅ BUILT 2026-09-22** |
| ✅ | ~~**Mexico City**~~ 🇲🇽 | Same DENUE. **Rail from OSM** — 195/195 stops exact, 6,468 geometry points | **BUILT 2026-09-22** — `pages/15_Mexico_City_Heatmap.py`. The ODbL share-alike decision was taken during the build; see `DECISIONS.md` |
| ✅ | ~~**Paris**~~ 🇫🇷 | SIRENE établissement-level, **Licence Ouverte 2.0**, **99.96% already geolocated**. Built storefronts **87,164** from **149,166** active bucket rows | **BUILT 2026-09-23 — the 21st city, and the first in France.** 🚨 **Its screening figures did NOT survive the build.** This row read *"50,156 rows vs OSM's 54,198, and on one class 10,595 vs 10,642"*, attributed to an **employee filter**. **There is no employee filter**: `trancheEffectifs` is `NN` on 77.3% of rows and only 1,425 record `00`, so SIRENE codes a sole trader as `NN` — that band holds every owner-run shop, and the largest cut the column can make falls **16,000 short** of 50,156. Re-established: **87,164 SIRENE vs 48,973 OSM = 1.78×**; on restaurants the **OSM side reproduced** (9,058 vs a recorded 10,642) and the **SIRENE side did not** (16,280 vs a recorded 10,595). **When one side of a comparison reproduces and the other does not, the non-reproducing side is where the tuning happened.** France remains a build; the 92.5% claim does not |
| ✅ | ~~**Marseille**~~ 🇫🇷 | The same SIRENE, estimated at **25,430** bucket rows | **BUILT 2026-09-23 — the 22nd city, and France's second.** `pages/22_Marseille_Heatmap.py`. **18,177 storefronts, 66 stations.** Scope was **measured rather than inherited from Paris**: all five RTM lines sit 100% inside commune 13055, so the commune costs it nothing; Aubagne's tram excludes itself by having zero stations inside; ferries dropped by owner's decision and recorded as revisitable. See `DECISIONS.md`, *"Marseille built, and a region now labels only its own cities"* |
| ✅ | ~~**Toulouse**~~ 🇫🇷 | The same SIRENE | **BUILT 2026-09-23 — the 23rd city and the third French one. 8,635 storefronts, 48 stations**, 64.3% of storefronts within a station ring, 0 person-like names at a residential unit. See `DECISIONS.md`, *"Toulouse built: 8,635 storefronts, 48 stations, and the first non-rail mode"* |
| ✅ | ~~**Lille (Regional)**~~ 🇫🇷 ▲▲ **REGIONAL** | The same SIRENE, estimated at **8,076** bucket rows for the commune alone | **BUILT 2026-09-23 — the 24th city, France's fourth, and its first regional one.** `pages/24_Lille_Heatmap.py`. **11,833 storefronts, 91 stations**, eleven communes. Both owner calls in the brief dissolved: métro geometry from OSM, everything else first-party from MEL, and ilévia's GTFS never read. See `DECISIONS.md` |
| ✅ | ~~**Rennes**~~ 🇫🇷 | The same SIRENE, estimated at **4,833** bucket rows (measured at the build: **5,451**, so the estimate was the floor it said it was) | **BUILT 2026-09-23 — the 25th city and France's fifth and last.** `pages/25_Rennes_Heatmap.py`. **3,479 storefronts, 24 stations**, 68.0% of storefronts within a station ring, 0 person-like names at a residential unit. **The brief's "the métro is city-contained" was half wrong**: Métro b keeps 11 of 15 stations inside commune 35238 and loses both termini; commune-only by owner's call, since its worst line survives better than Toulouse's T1. See `DECISIONS.md` |
| ✅ | ~~**Oslo**~~ 🇳🇴 | Enhetsregisteret SUB-UNITS on `beliggenhetsadresse`, measured at the brief's **13,458** bucket rows exactly | **BUILT 2026-09-24 — the 26th city and Norway's first.** `pages/26_Oslo_Heatmap.py`. **10,718 storefronts, 155 stations**, 75.6% within a ring, 0 sole-trader names shown. **Three brief claims corrected at the build**: the register is SN2025 (NACE Rev. 2.1) not SN2007; coordinates are a JOIN on Kartverket's bulk address file (96.8%) not a geocode; OSM's relations are too partial for gate 3. Kommune only, trams drawn, ferries excluded - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Copenhagen**~~ 🇩🇰 | CVR PRODUCTION UNITS on `beliggenhedsadresse`, measured at the brief's **14,887** Kobenhavn bucket rows exactly | **BUILT 2026-09-24 — the 27th city and Denmark's first.** `pages/27_Copenhagen_Heatmap.py`. **14,978 storefronts, 64 stations** (Kobenhavn and Frederiksberg), 94.5% within a ring, 4 person-like names at a residential unit (0.03%). **Three brief claims corrected at the build**: the codes are DB25 (NACE Rev. 2.1) not DB07; DAWA closes 1 October 2026, so coordinates join DAR on Datafordeler; the Letbane is open. Frederiksberg in, S-tog drawn, sole traders and partnerships shown by address, 969900 excluded, rail from OSM rather than Rejseplanen's GTFS - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Prague**~~ 🇨🇿 | ROS02 ESTABLISHMENTS where they trade, with the owner's activity from RES - measured at the build as 27,327 in the buckets against the brief's 27,065 on the older NACE column | **BUILT 2026-09-24 — the 28th city and Czechia's first.** `pages/28_Prague_Heatmap.py`. **25,275 storefronts, 58 stations**, 69.8% within a ring, restaurant control 1.59x OSM like-for-like, 1 person-like name at a residential unit (0.01%). Keyed on RES's `NACE2025` (NACE Rev. 2.1), matched on PREFIX for its ragged depth; metro from PID's own GTFS with Flora added while closed. Natural persons and partnerships shown by address, and a natural person's premises at their own seat left off - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Amsterdam**~~ 🇳🇱 | Two layers from the city's own API: the live hospitality-permit register (the brief's 4,092) and the BAG's shop-class units in use (the brief's 10,898) | **BUILT 2026-09-24 — the 29th city and the Netherlands' first.** `pages/29_Amsterdam_Heatmap.py`. **13,238 storefronts (3,583 permits, 9,655 shop units), 144 stations**, 95.5% within a ring. Metro 50–54 and 16 tram lines (owner's call), from OVapi's CC0 national GTFS; stations are each line's REGULAR route, trams thinned by the sub-transit-line filters; gate 3 exact on the metro. Tram colours read from GVB's own map. Gemeente only though tram 6 keeps 5 of its 16 stops, and shipped with 11 line-label overlaps at phone width, the phone layout handed to the cleanup role - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Rome**~~ 🇮🇹 | SUAP premises (the brief's 95,493 joined) placed on ANNCSU house numbers | **BUILT 2026-09-24 — the 30th city and Italy's second.** `pages/30_Rome_Heatmap.py`. **98,897 storefronts, 87 stations**, 53.5% within a ring, no names in the register at all. Rail from OpenStreetMap (the agency GTFS is ambiguous); the Roma–Viterbo urban service DRAWN and Metromare left out, measured against the DART / S-tog test; the food layer's 2.67x over OSM stated rather than cut - owner's calls. See `DECISIONS.md` |
| ✅ | ~~**Barcelona**~~ 🇪🇸 | **58,908 active premises** (2022 census — the 2024 one is geographically incomplete), 0.00% bad coordinates, CC-BY-4.0. Build brief, 9/9 | **BUILT 2026-09-22** — `pages/18_Barcelona_Heatmap.py`. All four owner decisions were settled before the build: census year **2022**, drawn scope **16 lines** (14 metro refs + funiculars FM and FV, decided on the operators' own `network` tag), mall and market interiors **kept**, and the brief's OSM breakdown corrected to tram 20 / funicular 6. ⚠️ **The duty to notify the Council is still OUTSTANDING** — see `docs/gated_access.md` item 2 |

⇄ **Paris left Band A and came back the same day, measured both times.**
The demotion was right on the evidence then available (86.6% of the bucket are
sièges, i.e. largely home addresses); the return is right on evidence that did
not exist yet — an **OSM composition comparison**. ⚠️ **That comparison was later re-established and its headline figure withdrawn** (see Paris's row): the reversal was right, the number supporting it was not. The
reversal is recorded rather than tidied away, because the thing that changed
was the measurement, not the opinion. See "Paris / SIRENE" below. The architecture question it was holding ("national register vs
per-city") turned out to be **closed already**: Mexico shipped two cities from
the national DENUE on the same day, so `pipeline/countries/` is the answer and
national registers are fine. What fails is **SIRENE's composition**, which is
a different objection and a measured one.

▶ **Madrid's pipeline is DONE and on master; only its app wiring is held.**
As of 2026-09-22 `pipeline/madrid/`, `outputs/madrid/`, its taxonomy module and
its provenance rows are all merged, and `scripts/check_provenance.py` reports
it ready. What is not merged is `app/cities.py` and its page, deliberately:
they sit on `spain-app-wiring`, because Streamlit Cloud pulls master
automatically and landing an imported module there would publish the city and
serve it broken until a reboot. **It waits for Barcelona so the two ship
together** — see that branch's own commit message, which is the authority on
the hold.

So the next *unstarted* city is the question.
**Barcelona** is the obvious answer — same country, brief done, licence read,
and only owner decisions left. After that the screen has no city whose
"what remains" column is empty.

### ▲ 🇮🇹 Rome — a premises register joined to Italy's house-number archive (2026-09-24)

**The open screening gap's last row, screened in one evening.** Roma Capitale's
SUAP register records **premises** — 155,448 establishments keyed on (office,
number), with the city's street code, civic number and an activity class — and
**ANNCSU**, the national house-number archive, carries the same street code
with WGS84 coordinates for all 516,337 of Roma's civic numbers. **No geocoder:
a join, 95.7% at civic level.** Brief: `docs/build_briefs/rome.md` (6/6).

| City | Storefront establishments | **Joined** (civic level) | Rail | Licences |
|---|---|---|---|---|
| **Rome** | **95,493** — retail 65,107 · food 19,223 · personal 11,163 (+ food and personal trades inside the *Laboratorio* catch-all) | **95.7%** (92.0% exact), every municipio ≥ 90.9%, 0.2% unmatched | OSM Metro A, B/B1, C (+ Metromare, owner's call); **exclude the phantom Metro D**; Roma Mobilità GTFS live | SUAP and ANNCSU both **CC BY 4.0**, READ — credit, link, state the modification |

🚩 **Owner's call, 2026-09-24: Band A WITH A BUILD CHECK.** The food-and-drink
control reads **2.60×** OSM (19,223 vs 7,405), above France's 1.26–1.80× and
Prague's 1.63×, and cannot be sharpened (restaurants and bars are not
separated). The register has **no closure date**. The build compares SUAP with
OSM street by street, splits the excess by start year, and either sets an age
cut-off or states the over-count on the page.

### ▲ 🇳🇱 Amsterdam — two layers from the city's own API (2026-09-24)

**Moved here from Band C on 2026-09-24 (owner's call)**, the night it left the
discards. The BAG's **10,898 shop-class units in use** became a second layer
beside the **4,092 hospitality permits**, with the **4.6%** vacancy rate
disclosed on the page and retail and personal services in one category. Both
licences read: **BAG PERMITTED** (Kadaster, Public Domain Mark); **the permits
SILENT**, credited as **CC BY 4.0** on the owner's choice because that
satisfies both readings. Brief: `docs/build_briefs/amsterdam.md`, **8/8
checks**. Build-time calls: trams in or out, four permit categories, 1,061
mixed-use units, de-duplication by address.

#### From the discards to Band C, 2026-09-24 — the screening, as written

**Its discard rested on the top hits of one national search** (*"Aantal
vestigingen per buurt"* — neighbourhood counts). **The city's own API was
never asked**, and it answers: `api.data.amsterdam.nl/v1/` lists **100 datasets**
*(recorded as 383 at first — that was dataset and table paths, not datasets)*.

| | |
|---|---|
| **The full register** | 🚧 `hr_kvk` (the KvK Handelsregister, incl. `vestigingen`) and `standbedrijven` answer **HTTP 403** — authorised users only, not worked around. The published schema names the scopes: `hr_kvk` **`FP/MDW`** and **`HR/R`**, `standbedrijven` **`BSK/BEDRIJVEN`** — city-staff scopes, so asking for access is unlikely to land. KvK's own HVD open dataset (CC BY 4.0) **cuts every address to the first two postcode digits** and drops names and numbers — activities without a location, Colombia's shape |
| **The one bucket** | ✅ `horeca/exploitatievergunning` — **4,094 hospitality operating permits**, all granted, **every end date in 2026–2031 (a live register: expired permits leave it)**, 96.7% with a point (RD New). Restaurant 1,702 · café 870 · alcohol-free 327 · fast food 231 · coffeeshop 126 · eethuis 93 · hotels 72 (out) |
| **Control** | **0.89×** OSM restaurants (1,806 vs 2,040) and **0.95×** all food and drink — close to complete; **fast food is thin** (231 vs 712), probably exempt |
| **Licence** | **SILENT — read 2026-09-24.** The live API declares none (`license: null`, *"Licentie: -"*); a 2022 harvest of the city's retired catalogue on `data.overheid.nl` said CC BY 4.0 — **a conflict flagged, not resolved in the project's favour** |
| **Names** | trade names (*"Taco Lindo Albert Cuyp B.V."*) |
| **Rail** | 14 subway and 46 tram relations |
| **A second layer? (probed 2026-09-24)** | **BAG on the same API**: **10,898** units whose use class is *winkelfunctie* (shop) and whose status is *in gebruik*, all with a point, **90% shop-only** (9,837), the rest mixed. **1.77×** OSM's 6,150 shops (nonsense-term control: 0). But BAG records what a unit is **for**, not what is there: **no name, no activity, and `feitelijkGebruik` (actual use) empty on all 10,898** — a vacant shop counts, and so does a hairdresser. Restaurants and cafés sit mostly under *bijeenkomstfunctie* (6,717 units), which the permits already cover better. **Licence not read** |
| **How many are empty? (measured 2026-09-24)** | **No open source marks a unit empty** — the property snapshot (`standvastgoed`, 134 fields per address) has no occupancy field, energy use is published per neighbourhood only, and the per-unit sources (Locatus, KvK) are paid or staff-only. **But the rate is published**: the city's statistics (`bbga`, source **Locatus**, 1 January 2026) count **660 vacant of 14,314 sales points — 4.6%**, 0–7% by district, with a rate for all 110 *wijken* and 465 of 545 *buurten*. So empty shops are about one in twenty: disclosable, not filterable |
| **Nothing else** | The other 97 datasets were listed in full: shopping-area polygons (`winkelgebieden`, 142), terrace tariff zones (11), B&B and mooring permits, city-owned property — **none premises-shaped** |

**One bucket, and the best-maintained one in this band** — the only register
here that drops premises when their permit ends. It joined Stockholm, Göteborg
and Zurich under the same owner question — until the BAG gave it a second layer.

**✅ DECIDED (owner, 2026-09-24): BAG becomes the second layer**, with the
vacancy rate disclosed on the page (**4.6%** city-wide, Locatus via the city's
statistics — no open source filters it per unit). Retail and personal services
share one category, which the page says; takeaways that are both shop-class and
permit holders are de-duplicated by address at build. **Conditional on two
licence reads** (BAG; the permits' SILENT-with-conflict position) — if both
pass, a build brief follows and the band question returns to the owner. The
same answer carries to Rotterdam's re-probe, since BAG is national.

### ▲▲ 🇯🇵 Japan — six cities, a block-level JOIN, not a geocoder (2026-09-24)

**Moved here from the geocoding band on 2026-09-24 (owner's calls), which then
closed.** Japan's coordinate step was a JOIN: the permit lists spell the
address, and MLIT's 位置参照情報 publishes a point per block (街区).
`scripts/screen_japan_join.py` measures it, with Minato as the control at
**99.8%** re-run after every rule. Rail for every city is MLIT N02, **JR and the
private railways included** (owner). **No general retail anywhere**: Japan's
ceiling, stated on each page. The food control is the Economic Census's 飲食店
count, not OSM (owner).

| City | Food premises (fixed) | **Joined** (block) | Independent check | Personal services | Licences (all READ) |
|---|---|---|---|---|---|
| **Tokyo (8 wards)** | **≈59,400** permit rows — Chūō, Minato, Shinjuku (2023, disclosed), Kōtō, Shibuya, Taitō, Setagaya, Meguro. ⚠️ **Against Tokyo's yearbook count, only Shibuya's list is essentially complete (98%)** (measured 2026-09-24). The others hold 9–84%: consent-filtered exports, opt-outs, and snapshots never updated. Filling them takes requests to the wards (`gated_access.md` 29–32) | **99.1–100%** | the wards' own coordinates, median **22–43 m** | 生活衛生 registers, 11 wards (16,299; Meguro's 1,412 added 2026-09-24) | Tokyo Open Data Terms / ward CC BY 4.0; §6 cost clause accepted |
| **Osaka** | **61,752**. ⚠️ **67% of the official restaurant count** (MHLW 衛生行政報告例, FY2024: 54,289 of 81,418), where the other designated cities read 93–101%. **About two-thirds of the gap is expired permits still in the official count** (probed 2026-09-24): the old-law count exceeds what can exist by about 12,000, and the list is even across wards against the Economic Census. **The other third is undetermined**: e-Stat's flow tables show about 9,000 revised-law restaurant permits that the city counts as live and has never listed, some of them short-lived event stalls. The page discloses it; the build is not blocked | **99.1%** | the city's own (mislabelled) coordinates, median **38 m** | 15,775 | CC BY 4.0 / 政府標準利用規約 2.0 |
| **Kobe** | **24,761** | **97.1%** | — | 4,993 | CC BY 2.1 JP |
| **Sapporo** | **24,257** | **84.7%** + 15.2% chōme | — | 5,993 | CC BY 4.0; 第9条3 accepted |
| **Fukuoka** | 3,231 (own list, pre-2021) + **21,088** restaurants from MHLW | **98.1% / 96.8%** | MHLW's own coordinates, median **36 m** | 5,846 (99.2%) | BODIK CC BY 4.0 + MHLW PDL 1.0 |
| **Kyoto** ▲ | **22,259** restaurants, a register **rebuilt** from the permit stream (an upper bound: closures unseen) | **92.7%** | GSI on the stripped address, 0–1 m (12 of 12) | 5,828 (94.4%) | CC BY 4.0 (京都市オープンデータ) |

- **Tokyo**: 🚩 the owner requests **Chiyoda's** ledger (即時公開請求, a CD-R for
  ¥100) to fill the centre. Until then the page names the wards with no
  published list, Chiyoda, Toshima and Bunkyō among them. Nakano (stale) and
  the partial Shinagawa and Itabashi lists stay off (owner).
- **Fukuoka**: ⚠️ about **20% of restaurants withheld their address** in MHLW's
  per-field consent, so the page discloses an undercount. The two sources
  overlap by 1.3% (measured at block level).
- **The other five**: Hiroshima to the one-bucket band (no personal-services
  list), Sendai to the access-blocked band (the city's permission), and
  Yokohama and Nagoya to the open gap (no current food list). Kyoto went there
  too, and came back the same day on a rebuilt register.
- **Kyoto** ▲ *from the open gap 2026-09-24 (owner's call)*: no full list since
  the 2021 reform, so the register is **rebuilt**: the 2021-03-31 list plus
  every monthly list, kept while each permit's term runs
  (`japan_register.kyoto_permit_stream`, Rotterdam's method). 15.5 restaurants
  per 1,000, inside the yardstick. ⚠️ Closures are invisible, so the count is
  an upper bound and the page says so. Rail (owner): Keihan Keishin passes the
  stub test, the two funiculars are drawn, the Sagano scenic line is out.
- Briefs: `docs/build_briefs/{tokyo,osaka,kobe,sapporo,fukuoka,kyoto}.md`.
- **Every Japanese city, ward by ward: `docs/japan_city_list.md`**, generated by
  `python scripts/japan_ward_table.py --write`. It is republished on its own
  (owner, 2026-09-24).

### ▲ 🇳🇱 Rotterdam — Amsterdam's shape, the food layer rebuilt (2026-09-24)

✅ **BUILT 2026-09-24** - 1,939 rebuilt permit premises (the brief's 1,937) and 5,581 BAG shop units, 132 stations. See the Built table and `DECISIONS.md`.

**Moved here from the open gap on 2026-09-24 (owner's call), after two licence
reads.** Rotterdam publishes no hospitality register, so the food layer is
**rebuilt from its Gemeenteblad exploitation-permit notices** (KOOP's SRU API,
a point on 99.75%). Permits run five years, so the grants since 2021-09-24 give
**1,937 premises**. The method recovers **97%** of Amsterdam's live register
and overcounts about 1.15×. Shops and services come from the BAG's **6,170**
shop-class units in use (2.16× OSM shops). Vacancy is disclosed: **about 7% of
shop units registered as vacant (CBS, 1 January 2025)**. Licences: the notices
**PERMITTED WITH CONDITIONS** (Auteurswet art. 11 and CC0; the conditions are
on the harvest only); CBS **PERMITTED WITH CONDITIONS** (CC BY 4.0); BAG Public
Domain Mark. Brief: `docs/build_briefs/rotterdam.md`, **6/6**. Build-time
calls: coffeeshop and sex-business permits inside the notices; RET metro and
Line E's scope.

<details><summary>Its open-gap row, kept</summary>

| What it rested on | Next probe, and the re-probes |
|---|---|
| One search of `data.overheid.nl` (top hits were neighbourhood counts). Amsterdam's own API later showed the KvK register gated (403) and KvK's open dataset cuts locations to two postcode digits | Rotterdam's own portal for a hospitality-permit register like Amsterdam's ▶ **Re-probed 2026-09-24 — PARTIAL: Amsterdam's second layer, not its first.** BAG via PDOK: **6,170 shop-class units in use** in 0599 (98.6% shop-only; the same query reproduces Amsterdam within 1.5%), **2.16× OSM shops**, Public Domain Mark. **No current hospitality register** on any city host (data.rotterdam.nl 1,434 datasets — its `q=` is silently ignored; the ArcGIS server's 1,104 layers; 2,741 public ArcGIS Online items) — only staff layers built from the city's business register (horeca 2,072 rows from 2018; all buckets 5,942 from 2020, names blank, licence field empty). The Locatus vacancy figures (`rotterdam.incijfers.nl`) are **geo-blocked** (NL and DE only). **RECOMMEND: leave in the gap** — a shops-only BAG map is weaker than any built city ▶ **Second re-probe 2026-09-24 (owner's call) — NEW FINDS: Amsterdam's shape is now reachable.** A hospitality layer REBUILT from the city's own permit notices: every exploitation-permit decision is published in the Gemeenteblad, and the national official-publications API (KOOP, CC0 declared) returns them with a point (99.75%); 6,045 notices since 2021 give **1,937 distinct premises** (permits run five years, read in 48 sampled notices). **Validated on Amsterdam**: the same method finds 97% of Amsterdam's live register within 10 m and overcounts about 1.15×. 1.12× OSM food (about 0.98× after that surplus; Amsterdam's register is 0.95×); 76% of OSM hospitality features have a permit premises within 25 m. No names, no sub-category, and closed premises stay until expiry. **Vacancy replaced**: CBS's 2025 vacancy monitor counts **7.1%** of Rotterdam's 6,060 shop units empty (CC BY 4.0; the same table gives Amsterdam 4.4% against its brief's 4.6% Locatus). Personal-service permits are almost absent, so retail and personal services stay one BAG category, as in Amsterdam. **RECOMMEND (owner): Band A as an Amsterdam-shaped city**, after two licence reads (KOOP notices, CBS) |

</details>

### ▲ Four cities joined this band 2026-09-23, when the coordinates band closed

**Their coordinate route was the thing being measured, and all four now have it MEASURED and a brief written** — Prague 5/5, Oslo 5/5, Hong Kong 8/8, and Copenhagen's data in hand with its licence read. **A band whose condition stops being true of every member should close, not be re-captioned around them** — the same reasoning that closed the old Band D when Bucharest finished screening.

**Every route in this band was probed on 2026-09-22 and answered.** The band
used to say the method was "identified and cheap", which is a description of a
plan rather than of a measurement. It is now a hit rate per city, taken against
each register's **own** addresses rather than hand-typed landmarks.

**The band splits in two, and the split is the useful thing:**

- **A JOIN** — the whole address table downloads, and coordinates come from a
  dict lookup. No per-row requests, no rate limit, no geocoder to be wrong.
  **Prague and Copenhagen.**
- **A GEOCODE** — one request per distinct address, against a service that
  answers. **Oslo and Hong Kong**, both keyless. *(Singapore's geocode was
  measured here too, at 98.8%, before the city moved to the one-bucket band.)*

**Taiwan left this band** for the national-geocoding band: its route was the one claim here that did
**not** survive probing. **Bucharest's primary is down** but its fallback is
measured.

| Cities | Country | The coordinate step — MEASURED | Rate |
|---|---|---|---|
| **Prague** ▲▲ *(1)* | 🇨🇿 | ▶ **BACK IN THIS BAND 2026-09-24, on a new business leg**: paused the same day because RES is a seat register, then answered with **ROS02** — open-data *active establishments* with RÚIAN codes — joined to RES for activity. **27,065** storefront establishments, **restaurant control 1.63x** like-for-like (the paused 8.02x compared all of NACE 5610 with OSM restaurants alone; like-for-like, RES's seats read 4.48x). ROS02's terms **PERMITTED**, nothing to display. ARES/RŽP rejected on a 2019 ÚOOÚ GDPR fine, not on § 60(6), which Parliament narrowed. One owner call at build: sole traders (1,429 at their own seat). Brief: `docs/build_briefs/prague.md`. **The coordinate step, as measured before:** **A JOIN, confirmed.** RÚIAN's Praha export is **3.4 MB zipped, keyless** (`vdp.cuzk.gov.cz`; the old `cuzk.cz` redirects rather than dying) and holds **134,627 addresses, every one a unique `Kód ADM`, 99.99% carrying coordinates**. Measured on **6,000 active Praha rows** in CZ-NACE 47/56/96 streamed from RES | **99.8%** — 99.9% carry a code, 100.0% of those resolve |
| **Copenhagen** *(1)* | 🇩🇰 | **A JOIN, confirmed — and the account gate was on the wrong leg.** DAWA (`api.dataforsyningen.dk`) is **keyless**; the `distribution.virk.dk` 401 gates the BUSINESS register only. The whole city downloads as CSV: **85,351 access addresses, 100% with WGS84**, joinable on `vejnavn` + `husnr`. ⚠️ **Frederiksberg (0147) is a separate kommune entirely surrounded by Copenhagen** — scope to 0101 alone and the map has a hole in its middle; its 9,584 addresses come from the same call | **100%** of addresses carry coordinates ✅ **BRIEF WRITTEN 2026-09-23, 4/4 — `docs/build_briefs/copenhagen.md`.** **14,887 storefront rows** (retail 6,689 / food 5,163 / personal 3,035) at **100.0% named**, measured from the real 2.00 GB download rather than from metadata. **96.9% carry a DAR address UUID**, so coordinates are a JOIN. ⚠️ **Four files joined on `CVREnhedsId`** — `Produktionsenhed` alone is almost empty. 🚨 **`v/` marks a sole trader: 7.2%, a FLOOR**; `coNavn` is a second exposure at 26.0%. ⚠️ **Rail: M1–M4 only** — this list's "tram 4" was WRONG, Copenhagen has no tram |
| **Hong Kong** ▲▲▲ *(1)* | 🇭🇰 | ✅ **BUILT 2026-09-24 WITHOUT THE GEOCODE** - FEHD publishes the same registers with its own point per licence on the CSDI Portal, found by the ALS licence read; 21,137 of 21,165 placed, and the ALS hits this build would have accepted sit a median 12 m from FEHD's. Recorded as found: **A GEOCODE, confirmed keyless.** The government **Address Lookup Service** (`als.gov.hk/lookup`) answers without a key and returns **lat/long AND HK1980 Grid easting/northing AND a confidence `Score`** (76.15, 88.75, 97.69 on three test premises). ✅ **INDEMNITY ACCEPTED by the owner 2026-09-22** — the project's only uncapped liability, priced deliberately. Three conditions bind the build: display source + Government IP acknowledgement + DATA.GOV.HK attribution exactly; run `check_personal_exposure.py` and exclude catch-alls; the dated record in `data_sources.md`. ⚠️ Re-reading the live clause corrected this project's OWN earlier quote twice: it arises **directly or indirectly**, and there is **no notice-and-defend right** | ✅ **100.0% — RE-MEASURED 2026-09-23 on 200 random register rows, as a TWO-STAGE lookup.** This cell read *"per-row rate not yet measured"* for a day after the brief measured it. **Brief 8/8 — `docs/build_briefs/hong-kong.md`** |
| **Oslo** *(1)* | 🇳🇴 | **A GEOCODE, keyless — with two traps.** Kartverket (`ws.geonorge.no/adresser`) answers and returns `representasjonspunkt`. ⚠️ **`fuzzy=true` MUST NOT BE USED**: it "rescued" `Karenslyst allé 8B` as **`allé 1B`** — a different building — and turned `7-Eleven` into `Ellen Gleditsch' vei 7`. It returns plausible coordinates for the wrong place. ⚠️ The API caps at **10,000 rows** (offset 9,900 works, 15,000 returns nothing), so it cannot enumerate the city | **97.8%** via two stages: exact `adressetekst`, then plain `sok`. Never fuzzy |

**⚠️ Two facts here that are NOT about coordinates and change build scope:**

- **Oslo's register is not filtered by the address you read.** Bronnoysund's
  `?kommunenummer=0301` does **not** guarantee `beliggenhetsadresse` is in
  Oslo — a sample turned up Bergen, Copenhagen, Paris and Malmö, and
  `adresse` is a **list** whose first line is sometimes `c/o Osnordic AS`.
  **This is the registered-office trap in a third costume**, after ONRC, ACRA
  and SIRENE's *sièges*. The generalisation worth keeping: **a filter
  parameter and the field you read are two different addresses until proven
  otherwise.** How much of Oslo's 152,128 is physically in Oslo is **still
  unmeasured** — brreg's API stops paging past ~10,000, so both samples came
  from the alphabetical head and disagreed (24.5% vs 4.3%). **Settle it with
  the bulk download at build time, not with the API.**
- **Three of these services report their own confidence; Oslo's does not.**
  DAWA returns a `kategori` (A exact / B normalised / C ambiguous — it
  returned **B** for `Raadhuspladsen 1 1550 Kobenhavn` with the diacritics
  stripped, and **C with 30 results** for an ambiguous one) plus a
  per-address `nøjagtighed`; ALS returns a `Score`. **A geocoder that says
  when it is guessing is worth more than one with a higher raw hit rate** —
  which is exactly what Oslo's `fuzzy` lacked.

## ✗ Band B — CLOSED 2026-09-24: Japan's coordinate step was a join (0 cities)

**Closed by succeeding, like the coordinates band before it (owner's calls, 2026-09-24).** Its caption was *geocoding at national scale*, and Japan's address work turned out to be a block-level join to MLIT's 位置参照情報 at 95–100%, so the condition stopped being true of all ten. **Where they went**: Band A takes Tokyo (8 wards), Osaka, Kobe, Sapporo and Fukuoka; the one-bucket band takes Hiroshima; the access-blocked band takes Sendai (the city's permission); the open gap takes Yokohama, Nagoya and Kyoto (no current food list). **Everything below is kept as evidence.**

**The investment tier.** These share one property that separates them from
the buildable band: the address work is a project rather than a step, and it is worth
doing only because the machinery, once written, is reused across many
cities. **Japan is ten cities from one schema, and since 2026-09-23 it is
the whole band.** Kaohsiung left for the access-blocked band (D) the same
night: it needs no geocoder, only a publisher who opens its file.

▲ **São Paulo and Rio left this band on 2026-09-23 — upward, to A — by not
needing a geocoder at all.** Brazil's census address file turned out to carry
every establishment with its own coordinate (see the Brazil section in Band
A). **The lesson for the two countries still here: before building a geocoder,
look for an address file that already carries the coordinate** — Prague's
RÚIAN, Copenhagen's DAWA and now Brazil's CNEFE were each that, and each
turned "a geocoding project" into a join or into nothing.

| Cities | Country | Business leg | The coordinate step |
|---|---|---|---|
| **Tokyo**, Osaka, Nagoya, Yokohama, Sapporo, Fukuoka, Kyoto, Kobe, Sendai, Hiroshima *(10)* | 🇯🇵 | Premises-level food permits, CC BY declared, one national schema; **personal services from the 生活衛生 registers (11 Tokyo wards)**; food retail only where a ward publishes 届出. No general retail | ✅ **SOLVED 2026-09-24 — a JOIN, not a geocode**: MLIT 位置参照情報, **99.3% at block level on 24,297 Tokyo food premises** (Minato control 99.8%), personal services 98.8–99.8%; independent check against publishers' own coordinates median 22–43 m. ⚠️ **What stops Japan now is COVERAGE**: food files for **4 of 23** Tokyo wards; central Chiyoda, Shibuya, Toshima absent from Tokyo's catalogue (one method — their own sites next). **RECOMMEND (owner's call):** this band's caption no longer describes Japan; re-band on coverage once the nine cities and the ward second pass are in |


*(A paragraph here said Bucharest's rail was uncounted and its licence unread.
**Both were done on 2026-09-22/23** — 13 relations counted, licence SILENT —
and Bucharest now sits in the one-bucket band, where its full record is. The
paragraph was removed from this band on 2026-09-23 because Bucharest is not
in it.)*

**Brazil was chosen as the next geocoding work on 2026-09-23 and left the band
the same afternoon** — CNPJ is geo-blocked, and CNEFE made the geocoder
unnecessary. **Taiwan was next, and its first probe the same evening found it
is a JOIN too** (Taipei 92.5%, see its row). If the other three cities
confirm, **this band will hold only Japan** — and Japan's own address
registries are the next thing to look for.

**Japan is ten cities from one schema** — the best marginal-city cost in the
screen — against the worst geocoding problem and a two-bucket ceiling.
**Still the biggest open decision in this list**, and a judgment call rather
than a probe.

📘 **Before starting Japan, read `docs/geocoding_retrospective.md`** (written
2026-09-23). Brazil and Taiwan both left this band because the address file
already carried the coordinate. **The retrospective predicts Japan is a
block-level JOIN too** — the permits split the address into municipality /
町字 / 番地以下 on 98% of rows, and MLIT's 位置参照情報 publishes those
components with a coordinate per block — **ASSERTED, not measured**, with the
order of work to test it.

## ⚠️ OPEN SCREENING GAP — rows that rest on an absence (0 cities — EMPTIED 2026-09-24)

✅ **Emptied 2026-09-24 (evening) by a final re-probe of its last eight, each given a
verdict on the owner's calls.** The owner asked for "an exhaustive final search on all open gap
cities" and "a definitive verdict on each". Four agents tried only the methods not yet tried:
- **Riga → Band A**: its rail was measured (trams pass; suburban rail fails on frequency), and
  the owner accepted the scoped vacancy disclosure.
- **Yokohama → Band C**: personal services only, and no page for now.
- **Lisbon → Band D**: DGAE's register needs a free account.
- **Helsinki and Tallinn → Band D**: geo-blocked. Their lookup-page harvests were declined.
- **Vienna, Santiago and Nagoya → the discards.**

**The rows below are kept as the evidence each verdict rests on**, not as a queue. A city
enters this section again only on a row resting on an absence.

**Not candidates yet and not discards — unscreened.** `global_country_shortlist.md`
records *"Italy stays a Milan-only country"*, but that rests on **Naples** and
**Messina** measuring out. **Rome and Turin appear nowhere in any list**, which
`add-country` is explicit about: a row whose reason is "not reached" is not a
discard.

**Run each re-probe through the `reprobe-city` skill** — the process that took
Amsterdam from a discard to Band A in one evening.

**▼ 2026-09-24 — twelve rows back from the discards**, in re-probe order (biggest
rail and clearest next probe first). Each rested on ONE method, and
Amsterdam — the same shape — turned out to have a current premises register
on its own host the night it was re-probed. The evidence each carried is kept.

**▼ 2026-09-24 — five more, when the discard table got evidence columns**
(owner's call). `scripts/check_discard_evidence.py` refused them: Naples and
Messina rested on one search; Santiago's and Lima's coverage verdicts never
asked the missing districts' own sites; Hyderabad's own host was blocked and
never diagnosed from inside India. They sit below the twelve, cheapest probe
first.

**▼ 2026-09-24 (morning) — six rows left on the owner's calls after their re-probes.** Kuala Lumpur, Athens, Poznań and Bratislava went to the discards (negative on two methods, the city's own host asked), and Hamburg too, on currency (a 2016 retail survey and nothing else). Warsaw went to Band D (its own catalogue is geo-blocked to Poland). **Vienna stays**, owner's call, although its two-method negative would pass the discard check.

**▼ Later the same morning, four more on the owner's calls after the last re-probe batch**: Naples, Lima and Messina to the discards, and Hyderabad to Band D (its own site is geo-blocked to India).

**▼ 2026-09-24 (late morning) — Rotterdam left for Band A, and Yokohama, Nagoya and Kyoto arrived from the closed Japan band** (owner's calls). Riga stays partial: its only vacancy figure covers about a third of the mapped shops (owner).

| City | What it rested on | Next probe |
|---|---|---|
| **Vienna 🇦🇹** ▼ *from the discards 2026-09-24* | GISA (national, 1,032,283 trade licences) strips the street address by design — national only | Enumerate `data.wien.gv.at` for a city-run premises / Gastgewerbe dataset. **Rail is the deepest in the screen: 35 subway and 185 tram relations** ▶ **Re-probed 2026-09-24 — PARTIAL (weak); no general register on the city's hosts, now on two methods.** City WFS enumerated (377 layers) and data.gv.at (Stadt Wien 781 / 2,296); the only premises rows are **outdoor-seating permits** (Schanigärten, 3,165 approved at 2,745 addresses, CC BY 4.0) — no name, no activity, **0.42× OSM food**. The BEV address register's building use class is whole-building (2,434 retail buildings, 0.19× OSM shops) — not a shop layer. **RECOMMEND (owner): discard as a general register** (the two-method rule now passes); the seating permits are not worth building on. Side find: Linz publishes trade licences (unprobed) |
| **Helsinki 🇫🇮** ▼ *from the discards 2026-09-24* | The national PRH register, a 500-company sample: 89.8% addressed, but 53% real estate and 4.8% retail — national only | Helsinki Region Infoshare (`hri.fi`) for a municipal food-control or premises register ▶ **Re-probed 2026-09-24 — PARTIAL; the city's catalogue is GEO-BLOCKED outside Europe.** `hri.fi` and `avoindata.fi` answer Finland and Germany, 403 to the US — so the city's own catalogue is still unasked. **Lead: Oiva**, the national food-inspection register — premises rows with name, sector, address; reached only through its site search (300-result cap, no count); its open channel is a Qlik dashboard; licence unknown; joinable to the city's 58,307 address points. The building register counts premises per building (30,759 in 7,220) but gives no use class per premises. **Next: two reads from inside Europe** (HRI's catalogue; whether Oiva is a bulk file on avoindata.fi) — cannot be discarded ▶ **Low-cost probe 2026-09-24 — still needs a read from inside Europe.** The national portal's new domain (`avoindata.suomi.fi`) is also 403 from here, the same block as `avoindata.fi`, and was not routed around. The Food Authority's own open-data pages answer, but their only surveillance-data link is the analytics portal (the Qlik dashboard found before). No bulk Oiva file is reachable from outside Europe. **Next unchanged: a read from inside Europe** (HRI's catalogue; whether Oiva is a bulk file on the national portal) |
| **Lisbon 🇵🇹** ▼ *from the discards 2026-09-24* | `dados.gov.pt`: 430 hits for *estabelecimentos*, all aggregate hotel statistics — national only | Lisboa Aberta, the city's own portal, for licensed establishments ▶ **Re-probed 2026-09-24 — PARTIAL (stale): the right data, last surveyed 2010.** The city's **commercial census** (Recenseamento Comercial, 14 waves 1991–2010): the 2010 wave has **17,200 rows** — 11,395 retail, 5,654 food and drink — with name, 154 activity types, address and a point; CC0; no personal services; some rows carry private individuals' names. Retail **2.0×** and food **1.22×** OSM. The city's CKAN (`dados.cm-lisboa.pt`) is behind a **Cloudflare challenge for every automated client** (not bypassed); its ArcGIS Hub (75) and Online (743) were enumerated, and the national portal holds 316 of the city's ~530 datasets. **Next (owner): ask the city whether the census continued or its licensing register can be published; or a person browses the CKAN** ▶ **Low-cost probe 2026-09-24 — a NATIONAL, GEOLOCATED establishment register exists, behind a free account.** The RJACSR law created DGAE's *cadastro comercial*, a database of commerce, services and restaurant establishments, and its public app **Mapa do Comércio, Serviços e Restauração** (`mapadocomercio.dgae.gov.pt`) places them on a map, searchable by area, sector and CAE code. The app's API (`cadastro.dgae.gov.pt/api`) has `/estabelecimentos` and `/estabelecimentos/exportar`, but **both return 401 anonymously**, and the app offers login through Autenticação.gov or a user registration. Only aggregate indicators and settings answer without one. **Not worked around**: no token requested, and a CMS key embedded in the app's JavaScript was not used. The France/Mexico shape (one national register for every city), so it would serve **Porto** too. Licence and row count unknown until someone logs in. **Next (owner): whether to register a free account** (`docs/gated_access.md` item 28), then measure rows, CAE fill, coordinates and terms |
| **Tallinn 🇪🇪** ▼ *from the discards 2026-09-24* | The national MTR downloaded whole (102 MB): full activity, no location field — national only | Tallinn's own open data for a premises register. Trams only ▶ **Re-probed 2026-09-24 — STILL THIN.** City's own host asked: `www.tallinn.ee` behind a Cloudflare challenge (not bypassed); the city's 49 datasets on andmed.eesti.ee (filter confirmed, nonsense 0) hold no premises register. **Two national candidates**: the food-handlers register (`Toidukaitlejad.xml`, daily, CC BY-SA 3.0) is **geo-blocked** — `avaandmed.agri.ee` answers Estonia and Germany, times out from the US and here, while `www.agri.ee` answers everywhere; and the **building register (EHR)** has unit use classes for all three buckets (12131 restaurant … 12331 personal services) but its data comes by `POST /reports` with an **e-mail address — the owner's act**. OSM: 1,255 food, 3,532 shops, 511 personal services. **Next (owner): one EHR order for Tallinn (`ehitis_kaos`)** |
| **Riga 🇱🇻** ▼ *from the discards 2026-09-24* | The national company register (`data.gov.lv`, 21 fields): addressed, no activity column, 60% terminated — national only | Riga's own portal for a premises or food register ▶ **Re-probed 2026-09-24 — PARTIAL: a real premises register, alcohol and tobacco only.** The State Revenue Service's excise-licence register (data.gov.lv, CC0, daily; latest 2026-09-22): **2,898 current Riga premises** at 2,193 addresses, with location and a type field (shop, café, bar, restaurant…) and opening hours — **food service 1,596 (1.10× OSM)**; retail 746, alcohol/tobacco sellers only (0.14× OSM shops); no personal services. Joined to Riga's own address points: **96.2%** exact. **Second shape**: the cadastre's premise groups (VZD, CC BY 4.0) — 7,169 retail/wholesale (1.32× OSM shops) and 5,207 hotel/catering, but only 35–41% carry an address code (placement via the building cadastre number unmeasured; vacancy, wholesale and hotels mixed in). The food-safety agency's register (`pakalpojumi.pvd.gov.lv`) is **geo-blocked** (LV and DE only). The city's own host `opendata.riga.lv` does not resolve; its 79 datasets on data.gov.lv hold no premises. **Next: place the premise groups through the building cadastre number, find a vacancy rate, then read three licences** ▶ **Follow-up 2026-09-24 (owner's call) — AMSTERDAM'S TWO-LAYER SHAPE, with a heavy vacancy caveat.** The cadastre premise groups place through the building cadastre number: retail/wholesale 7,133 of 7,169 (99.5%) on building outlines, catering class 100%; a second route (the building-address link to the address register) agrees at a median 3.6 m. Class 1230 by name: 4,816 named shops (67%, 84% on the ground floor; 0.93× OSM shops including hair and beauty), only 3.8% wholesale, storage or offices; 62% last surveyed before 2010. Class 1211 is 81% hotel rooms, so the excise register stays the food layer. **Vacancy: 20.4%** of 2,324 street-front ground-floor premises, from a 2024 municipal field survey of the historic centre only; no citywide figure (Amsterdam's 4.6% was citywide). **RECOMMEND (owner): Band A only if a centre-only 20% vacancy is accepted as the disclosure; otherwise keep it partial.** Rail not yet examined (trams, suburban rail) ▶ **Vacancy investigation 2026-09-24 (owner's call) — only a SCOPED disclosure is workable.** No citywide rate exists: CSP has no non-residential vacancy table, none of the cadastre's 57 building or 13 premise-group fields records occupancy, and market reports are silent, from 2012, or 403 (Colliers, left alone). A second municipal figure: the Old Town re-survey of summer 2025, 87 of 573 premises vacant (15%). An occupancy proxy (OSM or excise licences on the same building) matches the centre's overall level (64–68% against the survey's 67.4% occupied) but cannot rank streets (Spearman 0.23), so it stays internal. The cadastre does count the same premises the survey counts (street-by-street Spearman 0.96). **In the station rings (966 m, 243 tram stops, 39 rail stations): about 36% of named shops are on the surveyed streets (20.4% vacant, 2024), about 6% in the Old Town (15%, 2025), and about 64% are not measured.** Side find: 208 named shops (4.3%) sit in buildings the city lists as degrading (CC BY 4.0), and can be dropped. **Owner's call: publish the scoped disclosure (both figures, their areas and dates, 'not measured elsewhere'), or keep partial** |
| **Santiago 🇨🇱** ▼ *from the discards 2026-09-24, on the evidence check* | `datos.gob.cl`, searched and its 272 publishers enumerated: 5 of ~33 Metro comunas publish patentes. The Santiago comuna is not on the portal, and its own site was never asked | The Santiago, Providencia and Las Condes municipalities' own sites for a patentes register — the comunas the Metro converges on ▶ **Re-probed 2026-09-24 — STILL THIN on coverage; Providencia found.** Providencia publishes its current commercial licences monthly under the transparency law (`transparencia.providencia.cl`, a 31/08/2026 XLSX of 74,712 rows; name, address and activity text 100% filled; about 78% offices or tax addresses, and a first keyword pass leaves at least 6,309 storefronts: 2,034 food, 2,533 retail, 1,742 personal services; 2.07× OSM food, 2.56× shops) — no coordinates, no named address file, no licence declared. The Santiago comuna publishes patentes only as 2016–2019 lists and, since 2020, as decrees; its file host `transparencia.munistgo.cl` returns 403 to everyone, Chilean probes included; its observatory shows 2019 density classes only. Las Condes marks its Maestro Patentes unpublished. Coverage is now 6 of about 33 comunas, downtown still missing. **Next (owner): a transparency-law request to the Santiago comuna (a form with a name, so the owner's act); for Providencia, an address file and a licence read** ▶ **Downtown probe 2026-09-24 (owner's call) — PARTIAL, alcohol licences only; STAYS IN THE GAP.** The comuna's own document site (`documentos.munistgo.cl`, never asked before; its sitemap lists 396 posts, 37 on patentes) carries the semester decrees renewing ALCOHOL licences with full lists: Decreto N° 330, 1st semester 2025, 1,832 rows (about 2,084 across the semester's group decrees), with name, street address and licence class (restaurants day and night, cantinas, liquor stores, beer sellers). But they are scanned PDFs with no text layer, about 20 months old, food and liquor only — and the later decrees sit on `transparencia.munistgo.cl`, still 403 to everyone. Individuals appear by name and RUT (never published). A placement route exists: the comuna's own ArcGIS Enterprise (`gis.munistgo.cl`) has street centrelines with address ranges (3,967 of 4,479) and 74,506 house numbers — no licence declared, join unmeasured. Other routes negative: the transparency council's catalogue (8 datasets), the comuna's 429 ArcGIS Online items, its observatory hub, `datos.gob.cl` (neither the comuna nor the SII publishes there); the SII's property file with use classes is behind a taxpayer login. OSM (comuna): food 1,092, shops 3,400. **Next (owner's act only): a Ley 20.285 transparency request for the current commercial-licence list** |
| **Yokohama 🇯🇵** ▼ *from the Japan band 2026-09-24 (owner's call)* | The overnight screen found **no current food list** on the city's own hosts: city lists stop at the 2021 food-hygiene reform, which moved filing to MHLW's 食品衛生申請等システム. That system's open data is an **opt-in slice of online filings**: 2,912 restaurants here, and 1.9–8.1% of the restaurants on the complete lists it was measured against. The coordinate step is solved (the Japanese join), so only the list is missing | A `reprobe-city` pass of the city's own hosts and catalogue for a current list, or a request to the city — Fukuoka and Hiroshima show the own-list-plus-MHLW shape works where the city keeps its counter filings ▶ **Low-cost probe 2026-09-24 — food NEGATIVE on two methods; personal services only.** The city's CKAN (`data.city.yokohama.lg.jp`) has no food-permit dataset: 食品 returns 11 newsletters and statistics, 営業許可 6 statistics, nonsense 0. The overnight screen found no list on the city's own pages. Personal services are complete: 環境衛生関係施設一覧, barber, beauty and cleaning ZIPs split per ward, as of 2026-04-01, CC BY. MHLW's opt-in slice holds 2,912 restaurants. **A one-bucket city whose one bucket is personal services**, a shape no band holds yet. **RECOMMEND: stays in the gap**; a request to the city for its food list is the next step, and the owner's act |
| **Nagoya 🇯🇵** ▼ *from the Japan band 2026-09-24 (owner's call)* | The overnight screen found **no current food list** on the city's own hosts: city lists stop at the 2021 food-hygiene reform, which moved filing to MHLW's 食品衛生申請等システム. That system's open data is an **opt-in slice of online filings**: 1,058 restaurants here, and 1.9–8.1% of the restaurants on the complete lists it was measured against. The coordinate step is solved (the Japanese join), so only the list is missing | A `reprobe-city` pass of the city's own hosts and catalogue for a current list, or a request to the city — Fukuoka and Hiroshima show the own-list-plus-MHLW shape works where the city keeps its counter filings ▶ **Noted 2026-09-24 — not rebuildable.** BODIK keeps only 12 rolling months of new food permits (2025-09 to 2026-08), and the city publishes no full standing list, so Kyoto's stitch cannot be done. The beauty-salon list is current (city page, as of 2026-08-31, CC BY 4.0). **Next: a request to the city for its full list (the owner's act), or older monthly files from an archive** |

*▲ **Rome left this gap on 2026-09-24 for Band A** — see its section there.*

*▲ **Kyoto left this gap on 2026-09-24 for Band A**, its register rebuilt from the permit stream — see the Japan section there.*

*▼ **Turin and Cairo left this gap on 2026-09-24 for the discard table**, each measured by two methods — see there.*

*▲ **Prague left this gap on 2026-09-24, back to Band A**, the same day it arrived: the premises source it lacked turned out to be published as open data (ROS02). Its row is in Band A.*

**Neither Italian city changes the Italy profile answer** — Italy is bespoke per city, so
each would be its own Step 0 regardless. See `DECISIONS.md`, 2026-09-22.

### The sweep, 2026-09-23 — what else rests on an absence

**Audited the whole discard record** for rows whose stated reason is *"not
reached"*, *"unprobed"*, *ASSERTED*, or a regional pattern. `add-country` is
explicit that such a row **is not a discard**, and records that exact error
happening twice — once to a group including **Italy, which then passed**.

| Row | What its reason actually was | Probed 2026-09-23 |
|---|---|---|
| **Göteborg** 🇸🇪 | *"Unprobed candidate"* — named twice in this file and **placed in no band at all** | ✅ **REAL, and it is a candidate.** `catalog.goteborg.se/store/search?type=solr` — EntryStore, the same platform as Stockholm's. **`Livsmedelsverksamheter`** is *"Alla aktiva livsmedelsverksamheter"* — **active food BUSINESSES, not inspections**, so no dedupe, where Stockholm's 8,146 premises had to be distilled from 289,742 inspection rows. **`Restauranger med serveringstillstånd`** declares **CC ZERO** — stronger than Stockholm's SILENT. Rail is trams, not a metro: **better data, weaker map** |
| **Lisbon** 🇵🇹 | On *"Countries ruled out"* with **no parenthetical evidence at all** | ⚠️ **Discard now EVIDENCED, and it holds.** `dados.gov.pt` returns 430 for *estabelecimentos*, but they are **aggregate hotel statistics** (*"Proporção de estabelecimentos hoteleiros que utilizam computador (%)"*) and prison establishments. The aggregate trap |
| **Warsaw** 🇵🇱 | Same — **no evidence** | ⚠️ **Discard now EVIDENCED, and it mostly holds.** Control passes (`zzqqxx` → 0, so the search filters). `CEIDG` is company-level, as recorded elsewhere. **One premises-shaped lead survives**: *Wykaz punktów sprzedaży napojów alkoholowych* — licensed alcohol sales POINTS, the Singapore-tobacco shape. One bucket at best |
| **Cairo** 🇪🇬 | Same — **no evidence** | ⛔ **STILL UNPROBED.** Recorded as an absence rather than a finding — ▼ **and on 2026-09-23 moved OUT of the discard table onto the open screening gap**, where this finding says it belongs |
| **Zagreb** 🇭🇷 | *"identical 1,291-byte SPA shell at four paths"* | ~~⛔ **Confirmed BLOCKED, not negative.** Three more paths tried 2026-09-23, all shells~~ ⚠️ **SUPERSEDED — this row contradicted the discard table, and the discard is the measured one.** `data.gov.hr`'s CKAN lives at **`/ckan/api/3/...`**, not at the paths tried here; through it Grad Zagreb's **210 datasets** were enumerated on 2026-09-22 and the only commercial one is a grants list. **Three more shells at the wrong paths are not evidence of a block** — the discard stands |

**The generalisable result: a "ruled out" list is only as good as its weakest
row, and three of this one's rows carried no reason at all.** Two of those now
do. Göteborg was never ruled out — it was simply never placed anywhere, which
is how a candidate disappears without anyone deciding to drop it.

## 🟣 Band C — one bucket only: complete, but narrower than the others (7 cities)

▼ **Yokohama 🇯🇵 joined 2026-09-24 from the open gap (owner's call): personal services only, and
no page for now.**
- **Personal services**: complete, 17,408 premises as of 2026-04-01, declared CC BY (barbers
  3,380, beauty 11,062, cleaning 2,966). Also a pharmacy list (1,719) and a drug-store list (611),
  whose licence page is unread.
- **Food: none in any era.** Four places were checked:
  - the city's catalogue, listed in full (649 packages);
  - the web archive of the catalogue and the food-safety pages;
  - a live crawl of all 18 ward sites;
  - the prefecture, which holds no Yokohama permits.
  MHLW's opt-in slice is 9.9% of the official 29,358.
- **Why no page**: a map without its roughly 29,000 restaurants would read its stations as
  emptier than Tokyo's or Osaka's, because of what is published, not what is there.
- **What would change it**: the city publishing its food register (only by request, the last
  resort), or MHLW's online system covering most permits as they renew online.

**Screening is COMPLETE for all five, and all five passed.** Each has a real
premises-level register with coordinates, current data and a usable licence.
What none of them has is a **second bucket** — and the owner's bar is that two
is acceptable and one is not. **Göteborg joined Stockholm and Zurich here on
2026-09-23**, probed to the same depth, which is why this caption no longer
says "both".

**▶ A second source in a different shape is still open for each** — a
building register's use class gave Amsterdam its shop layer on 2026-09-24,
which is how it left this band. `reprobe-city` Step 4 names the per-country
targets (ASSERTED, unprobed).

**This is not "we could not find a second register".** All these negatives were
re-established on 2026-09-22 by **enumerating the whole catalogue** rather
than searching it, because the original negatives rested on keyword searches
and that is the method that has failed this project most often — Stockholm's
own food register is called *Tillsynsverksamheter*, "supervision activities",
which matches neither `restaurang` nor `livsmedel`.

| | Stockholm 🇸🇪 | Zurich 🇨🇭 |
|---|---|---|
| **Catalogue enumerated** | **309 datasets** (Entryscape, by resource-URI prefix) | **1,128 dataset names** (CKAN `package_list`) |
| **The one register** | `Tillsynsverksamheter - Livsmedel` — **8,146 distinct premises** from 289,742 inspection rows, 100% trade names, 96.9% addresses, daily from Ecos 2 | `Gastwirtschaftsbetriebe` — licensed by the city police's *Bewilligung Gastro* unit |
| **Licence** | **SILENT** — the publisher's own feed says `accessLevel: public` on all 109 of its datasets | ✅ **CC0** |
| **What a second bucket would have been** | `Salutorg`, `Torghandelsplats` — **polygons**, *"i form av ytor"*: zones where trading is permitted, not traders | `geo_bauernhofladen` — **not shops**: *"Betriebszentren von Haupterwerbslandwirten"*, farmers' operating centres |
| **Everything else that matched** | 3 × social care (`Daglig verksamhet`), 1 utility service area | `standorte` of counting stations, contaminated sites, historic cinemas, tram ticket offices |

**Why neither is discarded.** Nothing here is unresolved or unreachable —
the work is done and the answer is *one bucket*. That is a **product
judgement**, not a data defect, and it can change: a second source may
appear, or a food-density page may become worth shipping. **A discard would
throw away two complete screenings to record a preference.**

**Both countries are structurally one-bucket, which is why no further probe
helps.** Sweden has **no general business licence** at all, so retail and
personal services have no municipal source to find; Switzerland's national
**STATENT is aggregate**. This is the Hong Kong distinction inverted — there
the register exists and we cannot reach it; here we have reached everything
and only one register exists.

**If one is ever taken, take Stockholm first on size, and Göteborg or Zurich
first on licence** — Stockholm's **8,146** premises against Göteborg's
**5,063** and Zurich's **3,488**; Göteborg and Zurich are both CC0 against
Stockholm's silence. *(Updated 2026-09-23, when Göteborg joined this band and
all three were measured.)* **One owner decision moves all three**: does a
food-density page belong in a project whose other cities carry three buckets?


---

*▲ **Amsterdam left this band on 2026-09-24 for Band A** — the BAG gave it a
second layer. Its section is there.*

### 🇸🇬 Singapore — moved here from the coordinates band 2026-09-23

**Two buckets on paper, ONE on current data.** Four keyless premises registers
exist and the licence permits everything this project does — but **the big
one is a 2016 snapshot.**

| Register | Coverage | Rows | |
|---|---|---|---|
| **NEA Licensed Eating Establishments** | 2015-06-11 → **2016-09-06** | **36,687** | ⛔ **TEN YEARS STALE** |
| **List of Supermarket Licences** | **2016-06-26 only — a single day** | 478 | ⛔ stale |
| **Licensed Tobacco Retailers** | updated **2026-08-07** | **4,235** | ✅ current |
| **Listing of Licensed Pharmacies** | updated **2026-08-07** | **243** | ✅ current |

**The ROWS confirm the metadata rather than merely repeating it**, which is
what makes this solid rather than a metadata artefact: the only dated column in
the eating-establishments file, `suspension_start_date`, returns **2016-02-21**
and **2016-04-13**, while tobacco's `ValidPeriod` returns **2025 / 2026 /
2027**. **Two files a decade apart in the data itself.**

⚠️ **`lastUpdatedAt` says 2024-06-06 for both stale files and it is a
METADATA TOUCH, not a data refresh.** Reading that field alone would have
recorded Singapore as two years old rather than ten. **`coverageEnd` is the
honest field and the rows are the honest check.**

**So the current position is ~4,478 rows, all RETAIL** — comparable to
Göteborg's volume and narrower than Stockholm's. **This is Turin's shape,
four years worse**: Turin sits in the open screening gap for a series that
stops in 2019, *"six years stale against a project mapping CURRENT density."*

✅ **The licence is NOT the problem and was read in full 2026-09-23** —
**Singapore Open Data Licence v1.0, PERMITTED WITH CONDITIONS.** Grant is
*"worldwide, perpetual, royalty-free"* covering *"modify and adapt ... or any
derived analyses"*, commercially. ⚠️ **It carries an INDEMNITY of
Hong Kong's class and wider** — its third limb reaches *"any claim made by
a third party in connection with the third party's Use of ... any derived
analyses or applications which you have provided"*, and it **survives
termination**. **That decision is HELD, not taken**: there is no reason to
accept an open-ended liability for a city whose main register is from 2016.

🚨 **`Listing of Licensed Pharmacies` carries `Pharmacistincharge`, a
named individual on all 243 rows**, and the licence expressly grants **no
rights over** *"any personal data in the dataset"* — so publishing it would
be outside the licence, not merely against project policy.

⚠️ **Provenance decides the terms: take these ONLY from
`data.gov.sg`.** HSA's and NEA's own site terms restrict commercial reuse of
their sites' contents, and both HSA datasets point at HSA's InfoSearch page.
**The same rows from the agency's own site would carry different terms.**

**Rail was counted 2026-09-23 and carries three traps** — recorded because
they would each have surfaced mid-build: **MRT 21 relations, 21 named, only 16
coloured** (the **`JRL` Jurong Regional Line has NO colour** across all 5 of its
relations — Bucharest's `Extensie M4` in a second city, the same day); **only
ONE of three LRT lines** appears under `route=light_rail`, Sengkang, so Bukit
Panjang and Punggol are tagged some other way; and **the station counts do not
reconcile** — MRT 54 + LRT 13 against 90 rail stations total, so 23 are
tagged as neither and the naive query undercounts badly.

**Reinstatement is cheap and well-defined: if NEA refreshes the eating-
establishment register, Singapore returns to the buildable band immediately.** Everything
else about it is already done — licence read, geocode measured at 98.8%,
rail counted, registers enumerated. **It is parked on ONE fact.**

### 🇷🇴 Bucharest — moved here from the coordinates band 2026-09-23

**Nothing about Bucharest got worse. The band it was in was measuring the
wrong thing.** The band it sat in described a **measured coordinate route**, and Bucharest's is
genuinely measured. This band describes the **one-bucket ceiling**, and
Bucharest has one. **Where both are true, the ceiling is what is actually
stopping the city** — which is what these bands exist to say.

⚠️ **This project had already recorded the finding and left the row
where it was.** The 2026-09-22 entry that closed Bucharest's screening states
that **Romania's national catalogue holds no second bucket**: 4,693 datasets
enumerated from the Internet Archive, and the only commercial register in them
is ~40 dated snapshots of ONRC's **company** register. **It has been in the
wrong band since its own screening finished.**

| | |
|---|---|
| **The one bucket** | **DSVSA** — the sanitary-veterinary authority, so its **31,299 rows are FOOD**. `bucuresti.dsvsa.ro` |
| **Licence** | **SILENT**, and established rather than assumed — no terms page exists at all; the footer's *"Toate drepturile rezervate"* is a **website** footer, the New York situation |
| **Coordinates** | **OSM fallback, re-measured 2026-09-23: 146,228 addressed objects** in relation 377733 (132,478 nodes + 13,750 ways), within 112 of the earlier figure |
| **Rail** ✅ | **RE-COUNTED 2026-09-23: 13 subway route relations, 13 named, 12 coloured**, refs M1–M5, and **64 station nodes** against the *"~63 claimed, unverified"* this list carried |
| ⚠️ **The 13th relation** | **`Extensie M4` carries NO `ref` and NO `colour`.** A build keying on `ref` silently drops it; a build keying on relation count draws a line it cannot label |
| ⚠️ **Fetch is browser-assisted by necessity** | Plain curl against the XLSX returns **503 with the challenge interstitial**; the same URL **inside the browser that legitimately passed the challenge** returns 200 and real `PK` magic bytes. Never a replayed clearance cookie |
| ⚠️ **Primary portal still dead** | `data.gov.ro` resolves to 85.120.75.35 and **blackholes on 443 and 80**, now **two days running** — which weakens the original "outage, not refusal" reading. Its catalogue was read from the Internet Archive instead |

**Bucharest is the strongest-RAILED city in this band** — a real five-line
metro against Stockholm's, Zurich's and Göteborg's trams — and the
weakest on access. **The opposite trade from Göteborg**, which has the best
licence and the weakest map.

### 🇸🇪 Göteborg — promoted into this band 2026-09-23

**It was never ruled out. It was never PLACED.** The master list named it
twice — *"Unprobed candidate"*, *"Better data, weaker map"* — and put it in no
band, which is how a candidate disappears without anyone deciding to drop it.
Probed to the same depth as Stockholm and Zurich on 2026-09-23.

| | |
|---|---|
| **Catalogue** | **EntryStore**, `catalog.goteborg.se/store/search?type=solr` — the same platform as Stockholm's. Three guessed CKAN bases returned a 662-byte HTML shell first: **a wrong endpoint, not a verdict** |
| **The one bucket** | ✅ **FOOD ONLY, and the control proves it.** `livsmedel` → 1, `restaurang` → 6, but **`handel` → 0, `butik` → 0, `företag` → 0, `detaljhandel` → 0, `frisör` → 0.** The search filters, so these are real absences |
| **`Restauranger med serveringstillstånd`** | **1,043 rows**, **CC ZERO**. Carries `Namn` (trade name) and **`Besöksadress`** — the *visiting* address, kept distinct from `Fakturaadress`, the invoice address. **That is the location split done right**, the same distinction that made Norway pass |
| **`Livsmedelsverksamheter`** | *"Alla aktiva livsmedelsverksamheter"* — **active food BUSINESSES, not inspections**, so no dedupe, where Stockholm's 8,146 premises had to be distilled from **289,742** inspection rows. `accrualPeriodicity: DAILY` |
| ✅ **Row count MEASURED 2026-09-23: 5,063** | The `accessURL` **was on the DISTRIBUTION, not the dataset** — in DCAT the property you want is on the child, and the licence (**CC0 1.0**) was there too. ⚠️ **Take the CSV** (`utf-8-sig`, `;`): the rowstore JSON returns **4,786** — it drops the 279 blank-`typ` rows, swaps x and y, and BOM-mangles `namn`. Brief **2/2 — `docs/build_briefs/goteborg.md`** |
| **Rail** | **Trams, no metro — INHERITED, not measured.** It comes from the same screen that gave Copenhagen a tram it does not have and Stockholm 21 trams against a measured 6. **Verify before building.** Better data on a weaker map — the trade Toronto lost on |

**Göteborg does NOT displace Stockholm, and now that is measured**: **5,063
against 8,146**. Its advantages are structural — businesses rather than
inspections (no dedupe), CC0 rather than SILENT — and they are real, but the
count settles the size question in Stockholm's favour. *(This paragraph read
"the count that would settle it has not been taken" until 2026-09-23.)*

### 🇯🇵 Hiroshima — moved here from the Japan band 2026-09-24 (owner's call)

| | |
|---|---|
| **The one bucket (food)** | Two lists that split by filing channel: the city's counter applications (**7,479** restaurants) and MHLW's open data for online filings (**5,195**, 66% addressed), overlapping by 1.2% at block level. **10.7 restaurants per 1,000 residents** (9.2 placeable), beside Sendai's 9.5 |
| **Joined** | own list **96.0%**, MHLW **95.0%** block; MHLW's own coordinates median **35 m** |
| **Why one bucket** | **no personal-services list**: new openings are published as PDFs only. Food retail exists only as MHLW's partial, opt-in notifications |
| **Licences** | both **PERMITTED WITH CONDITIONS**: the city's list under PDL 1.0 (the dataset-level declaration accepted for the full-list file, owner 2026-09-24) and MHLW's PDL 1.0 |
| **Brief** | `docs/build_briefs/hiroshima.md` (4/4). Hiroden's streetcars are the network's backbone, and whether trams count is the owner's call |

### Stockholm and Zurich in full

**▲ Stockholm** 🇸🇪 — **upgraded from D-c on 2026-09-22.** Screening is
DONE: a public ArcGIS FeatureServer carrying **8,146 distinct food premises**
with WGS84 points, 100% trade names and 96.9% addresses, updated daily. It
carried two questions; **the licence one was answered on 2026-09-22 — SILENT,
see item 2** — so **one remains, and it is an owner decision rather than a
probe**. ⚠️ **Item 2's text went stale the day it was answered and sat
contradicting this very sentence until 2026-09-23**, so a reader arriving at
the list saw "one remains" above a list of two. It is struck through rather
than deleted, because the superseded reasoning is what makes the resolution
legible:

✅ **RAIL COUNTED 2026-09-23, and this list's figure was wrong.** It carried *"metro 7, tram 21"*. Measured inside **Stockholms kommun** (OSM rel 398021): **subway 15 relations / 8 refs**, all named and all coloured; **tram 6 relations / 4 refs**, only **4 of 6 coloured**; **light_rail 6** (refs 21, 30, 31); **92 rail station nodes**. ⚠️ **One subway relation and one tram relation carry NO `ref`** — a `ref`-keyed build drops them silently. ⚠️ The boundary lookup matched nothing on `name=Stockholm` because the kommun is **`Stockholms kommun`**, and widening it returned **two US "Stockholm Township" relations at the same admin_level**.

1. **Scope.** It is **one bucket** — food. Stockholms stad has 291 datasets
   and exactly one commercial register; `restaurang` and `företag` both
   return **0** inside its own catalogue, and Sweden has no general business
   licence. A Stockholm page would be a food-density map.
2. ~~**Licence.**~~ ✅ **RESOLVED 2026-09-22 — SILENT, and this item
   was left standing after its own intro said it was answered.** The
   superseded text read: *"`dataportal.se` says `Åtkomsträttigheter:
   Begränsad`; the ArcGIS item says `access: public`... ambiguous in a way
   that matters, so it needs the publisher asked."* **It does not.**
   `dataportal.se` is a **HARVESTER, not the publisher** — `read-licence`
   step 5 — and the miljöförvaltning's **own** Hub DCAT feed
   (`open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json`, **109
   datasets**) declares **`accessLevel: public` on all 109**, with `license`
   **CC0 on 8** and blank on the rest. **Step 5 decides a contradiction in
   favour of the publisher, and the publisher says public.** 💡 **And
   the blank is meaningful precisely BECAUSE 8 of 109 carry CC0**: a missing
   licence field can mean *"no mechanism"* or *"declined to license"*, and here
   the mechanism is demonstrably in use.

**▲ Zurich** 🇨🇭 — **moved here on 2026-09-22 out of the one-probe-each
band, and it is the same decision as Stockholm's.** It sat in the probe band while its open item
was described as "no second bucket found". That is now **measured absent**,
which is an answer rather than a question:

✅ **RAIL COUNTED 2026-09-23 — ZURICH HAS NO METRO, AND THAT IS NOT A BLOCKER.** Zero `route=subway` relations inside the Stadt boundary (OSM rel 1682248); its network is **42 tram relations across 18 refs, all named and ALL COLOURED**, plus **4 `light_rail`, ref S18** (the Forchbahn). ⚠️ **An earlier version of this row said Zurich therefore had "no drawable network at all". That was WRONG** — asserted from prose, corrected against the code. **`route_type 0` is DRAWN in at least seven built cities**: San Diego, San Francisco, Los Angeles, Edmonton, Calgary, Miami and Dublin. **Every tram EXCLUSION is a city that also has a metro**, where the trams are a dense street-running overlay — Milan's config calls its own exclusion *"a costed extension, not a discard"* and *"reversible"*. **Zurich has no metro for a tram to overlay, so its trams ARE the rapid-transit system**, and all 42 carrying a colour removes Milan's invented-palette objection. **The live question is the Muni Metro SPACING test** — are stops one or two blocks apart, needing `docs/sub_transit_line_filters.md`? **A cost, not a disqualification.**

| Term searched on `data.stadt-zuerich.ch` | Hits | What they actually are |
|---|---|---|
| `zzqqxxnonsense` **(control)** | **0** | the filter is real |
| `detailhandel` | **1** | a **traffic count** |
| `verkauf` | 12 | tram ticket offices, apartment sale prices |
| `laden` | 31 | a farm shop, population surveys, tariffs |
| `gewerbe` | 28 | zoning land, 3D roof models |
| `firmen` | 16 | **every one a `Firmenbefragung`** — a company *survey*, 2005–2025 |

Only **`Gastwirtschaftsbetriebe`** is a register: premises-level, GeoJSON,
food. The national STATENT is aggregate. **So Zurich is a one-bucket food
city, exactly Stockholm's shape**, and the question it now carries is the
same one — *does a food-density page belong in a project whose other cities
carry three buckets?* **Answer it once and two cities move together.**

---

## 🔴 Band D — access blocked by the publisher (7 cities)

▼ **Lisbon, Helsinki and Tallinn joined 2026-09-24 from the open gap (owner's calls)**, after a
final re-probe. **Lisbon** waits on a free account. **Helsinki and Tallinn** are in Warsaw's
weaker form: each one's bulk file sits behind a geo-block.

**The rejected route, recorded so nobody takes it.** The re-probe reached both through the back
ends of public lookup pages:
- **Oiva's search API**: 3,424 Helsinki premises, pulled in 217 queries to get past a 300-result
  cap. No licence is declared for per-premises results.
- **Tallinn's food-register public view**: 5,131 premises, pulled by sending back the page's
  own session token. Its responses carried operators' ID codes and birth dates, which were
  dropped.

The owner declined to rely on either (2026-09-24), and the harvested files were deleted. **A
lookup page's back end is not a substitute for a geo-blocked bulk file.**

**Reopened 2026-09-23 (owner's call) for a condition the other bands cannot
say**: screening is COMPLETE and passed, the file exists and is measured, and
the one thing stopping the city is **the publisher's own access control**.
▼ **Sendai joined 2026-09-24 in the full form** (screened, joined, only permission missing). ▼ **Warsaw and Hyderabad joined 2026-09-24 in a weaker form (owner's calls)**: blocked BEFORE
anything was measured, so the first step is a read from inside the country, and only then asking.
**What unblocks it is asking, not probing** — which is the difference from
the closed band below, whose members were *not yet reached properly* and all
left it once they were.

| City | Screened and passed | What blocks it — MEASURED | The way through |
|---|---|---|---|
| **Kaohsiung** 🇹🇼 | **72,550 storefronts** in the national tax register; OGDL v1 read and accepted (the same decision as Taiwan's other cities); the door-plate file exists in a **2026 edition** (`高雄市115年門牌坐標資料-TWD97`, updated 2026-06-25) with the same columns the three joined cities used (**92.7–95.5%**) | 🚧 **Geo-blocked to Taiwan**: `data.kcg.gov.tw` answers **HTTP 200 to 3 of 3 Taiwanese probes** (two networks) and times out from Japan and the US; `www.kcg.gov.tw` on the same network answers everywhere. The national catalogue lists **no other host** for any of 3,342 Kaohsiung datasets. **Not routed around** — no proxy, no VPN | **A request to 高雄市政府民政局** to publish the file on data.gov.tw or lift the filter for it — an owner action. Nothing sent |
| **Warsaw** 🇵🇱 | ⚠️ **NOT screened behind the block — a weaker shape than Kaohsiung's (owner's call 2026-09-24).** Nothing behind the block has been read. The city's own catalogue is the one place a premises register could be; every reachable route is negative (the city's 21 datasets on `dane.gov.pl`; the map portal's layers, markets and café terraces only; CEIDG is company-level; the alcohol-sales-points lead was Gdańsk's) | 🚧 **Geo-blocked to Poland**: `api.um.warszawa.pl` / `dane.um.warszawa.pl` answer only from Poland (2 of 2 probes) and time out from Germany and the US, while `mapa.um.warszawa.pl` answers everywhere; the API is also key-gated. **Not routed around** | **A read from inside Poland first** (the catalogue listing — does a premises dataset exist?), and only then a request to the city for access. An owner action. Nothing sent |
| **Hyderabad** 🇮🇳 | ⚠️ **NOT screened behind the block — Warsaw's shape (owner's call 2026-09-24).** India's national catalogue was walked in full (288,011 titles: trade-licence counts, never premises); GHMC's archived URL names show trade-licence status and lookup forms, no bulk register named. Nothing behind the block has been read | 🚧 **Geo-blocked to India**: GHMC's own site answers 3 of 3 Globalping probes inside India (Mumbai, Bengaluru, Hyderabad) and returns 403 at its F5 edge to 9 of 9 from the US, Germany and Singapore, and from here; Telangana's portal (`data.telangana.gov.in`) the same. **Not routed around** | **A read from inside India first** (does GHMC publish a trade-licence register as a file?), then a request. An owner action. Nothing sent |
| **Lisbon** 🇵🇹 | ⚠️ **The city side is negative on three methods** (2026-09-24): its catalogue as mirrored on `dados.gov.pt` (220 of 316 datasets link to its ArcGIS services, which answer); its ArcGIS services directory (102) and org (nonsense control 0); and the archive's index of the challenged CKAN (1,966 dataset names). What exists: kiosks (373, CC0), markets, the stale 2010 commercial census, and a 2020 COVID "Estamos Abertos" layer marked internal use | 🚫 **A free account**: DGAE's national *cadastro comercial* (`cadastro.dgae.gov.pt/api/estabelecimentos`) returns 401 logged out, and a CMS key in the app's JavaScript was NOT used. Row count, activity codes, coordinates and terms are all unmeasured | Register the account (the owner's act, `docs/gated_access.md` item 28), then measure. With activity codes, points and reusable terms, **Lisbon and Porto** both go to A. Without them, a discard |
| **Helsinki** 🇫🇮 | ⚠️ **Reachable hosts all negative for retail and personal services** (2026-09-24): the city catalogue, enumerated through `data.europa.eu`'s copy (373 datasets, 6 Helsinki publishers, nonsense publisher 0); `kartta.hel.fi` WMS (485 layers) and WFS (terraces, parklets); HSY's WFS (397 layers, jobs grid only); `api.hel.fi` servicemap (public services, and its search is inert). Food exists in Oiva (national inspections, current) but only behind a search API, which is not used (above). The city's own food-control CSV is frozen at 2019 | 🚧 **Geo-blocked**: `hri.fi`, `avoindata.fi` and `avoindata.suomi.fi` answer 403 outside Finland and Germany. The bulk files behind them (the city catalogue; Valvira/LVV's alcohol-premises register, CC BY 4.0; any Oiva release) are unread | A read from inside Europe, by a person there (no proxy or VPN), of HRI's catalogue and of whether Oiva or the alcohol register is a bulk file. Then asking Ruokavirasto, the last resort |
| **Tallinn** 🇪🇪 | ⚠️ **A second layer is reachable, the first is not** (2026-09-24). Building-register use classes per building part come on a public WFS (`gsavalik.envir.ee`, `etak_ehr_hooned`; Maa- ja Ruumiamet, CC BY 4.0 equivalent): 2,077 commercial buildings; parts: food 1,496, retail 2,773 (0.79× OSM shops), personal services 342 plus 765 "other service". But these are registered use, not occupancy, with no names; 14% of lists are cut at 200 characters. It is not a premises register alone (Vienna's lesson). The city's GIS (1,173 layers) holds markets and malls only | 🚧 **Geo-blocked**: the food-handlers register `Toidukaitlejad.xml` (`avaandmed.agri.ee`, CC BY-SA 3.0) answers Estonia and Germany only. The public-view route is not used (above). The building register's full data needs an order carrying an e-mail (the owner's act, gated item 23). `www.tallinn.ee` is behind a Cloudflare challenge | A read of the food XML from inside the EU (no proxy or VPN), or the owner's EHR order. Then the Amsterdam shape: food register plus building-use layer, with a vacancy rate found and the trams-only call (5 lines; GTFS expired 2026-08-31, so OSM) |
| **Sendai** 🇯🇵 | ✅ **Screened and joined**: 12,627 permanent food premises, **95.1%** block, GSI check median 34 m; personal services 3,378 at 96.5% (`docs/build_briefs/sendai.md`, 4/4) | 🚫 **The city's permission**: its site terms default to 「無断で複製・転用することはできません」 and neither list page overrides it; the lists carry no per-file CC BY badge and are not in the city's 5,907-row open-data catalogue | **A written request to 健康福祉局生活衛生課**, drafted in formal Japanese for the owner to send (2026-09-24). Nothing sent yet |

<details><summary>Kaohsiung's full record while it sat in Band B (kept)</summary>

| Cities | Country | Business leg | The coordinate step |
|---|---|---|---|
| **Kaohsiung** *(1)* | 🇹🇼 | ▼ **The one Taiwanese city left here, 2026-09-23 — Taipei (Regional), Taoyuan and Taichung moved to Band A.** Kaohsiung's business side is measured (**72,550** storefronts in the national tax register) and its licence is the same OGDL v1; **its door-plate file (the 2026 edition, `高雄市115年門牌坐標資料-TWD97`, updated 2026-06-25) and its own metro station files sit on `data.kcg.gov.tw` / `openapi.kcg.gov.tw` / `api.kcg.gov.tw`.** 🚧 **GEO-BLOCKED, MEASURED 2026-09-23 (night)**: `data.kcg.gov.tw` answers **HTTP 200 to 3 of 3 Taiwanese probes** (two networks) and times out from Japan and the US, while `www.kcg.gov.tw` on the same network answers from everywhere — **a foreign-address filter on the data hosts, the publisher's access control, NOT routed around.** The national catalogue lists **no other host** for any Kaohsiung file. Moves to A only if the publisher opens it or publishes elsewhere — **the way through is asking the publisher**, an owner action. **The history of this row, kept:** ▲▲▲ **FINISHED 2026-09-23 (evening) — see "Taiwan finished" in `global_country_shortlist.md`.** Joins **Taipei 92.4% · Taoyuan 94.0% · Taichung 92.7%**; Kaohsiung's door-plate host unreachable, its business side measured at 72,550. **Rail needs no TDX** (now key-gated, and a Taiwanese mobile number to register): the agencies publish stations everywhere and Taipei's line geometry, keyless, under OGDL v1. **Taipei's door-plate licence: PERMITTED WITH CONDITIONS** (OGDL v1 — a prescribed attribution statement whose absence voids the grant, and a fault-based liability clause). **Head-office trap measured**: 38.7% of company rows look like offices, against 7.1% of sole proprietors. ⚠️ **Scope question: New Taipei** (76,320 storefronts) surrounds Taipei and its metro crosses the boundary — the Dublin/Lille regional shape. **The rows below are the earlier readings of the same day.** ▲▲ **2026-09-23: the national BUSINESS TAX REGISTER** (`全國營業(稅籍)登記資料集`, Fiscal Information Agency) — keyless, **refreshed daily**, one row per trading location with `營業地址` (the business address), a parent ID so **branches are their own rows**, a trade name, and a 6-digit industry code whose **47/48 · 56 · 96** are retail · food · personal services. **No personal-name column.** Taipei: **76,519 storefronts** after excluding 4,954 online-shopping rows (code 487, NAICS 454's twin) | ▲▲ **A JOIN, not a geocoder — MEASURED 2026-09-23 in Taipei at 92.5%** (food 95.1%, personal 99.0%, retail 90.0%) against the city's **door-plate coordinate file** (`門牌位置數值資料`, monthly, keyless, Open Government Data License v1.0). **Door-plate files exist for all four cities** on the national catalogue, which **exports whole and keyless** — the `ER0001` key error was one API endpoint, not the portal. Retail's misses are mostly **market stalls and under-viaduct stalls** with no door plate. ⚠️ **Still open before Band A:** the other three cities' joins (Kaohsiung's portal timed out from six nodes in five countries), the licence read, and whether company rows in the storefront codes are shops or head offices (Taipei's register is 104,489 有限公司 and 56,483 股份有限公司 against 69,156 sole proprietors). **Rail is NOT open**: TDX's metro endpoints answered unauthenticated on 2026-09-21 — 122 Taipei stations, line shapes and `LineColor` (see `global_country_shortlist.md`); re-verify at build. **The record below is the 2026-09-22 reading, superseded:** ⚠️ **MOVED HERE FROM BAND B 2026-09-22, on a probe rather than on a resemblance.** The row used to read *"moderate — NLSC's geocoder is keyless"*, and **that claim did not survive**: NLSC's API is alive and keyless, but the keyless endpoint is **reverse** geocoding (point → 村里) and administrative lists, not forward geocoding, and **no bulk 門牌 address-point file was reached**. `data.gov.tw`'s dataset API **requires an API key** (`ER0001:API Key錯誤`); its web pages are reachable, and `addr.tgos.tw` answers but has historically required registration. **Blocked, not negative** — and the Prague-shaped bulk join is still the thing to look for |

</details>

## ✗ Closed bands — kept in full as evidence, not as candidates

### ✗ CLOSED — access blocked (formerly Band G)

*▲ The condition is live again as **Band D** above since 2026-09-23 — Kaohsiung. This record is the band as it closed on 2026-09-22.*

**The band's premise was that the register exists and we cannot reach it, so
none of its members was a data negative.** That premise was correct and all
three left it in different directions. **Hong Kong** left upward: its bulk
export had been published on `data.gov.hk` all along and one `package_list`
call found it. **Hyderabad and Kochi** left downward: India's entire national
catalogue — **288,011 titles** — was walked, and every trade-licence dataset
in it is an aggregate. **A band for unreachable registers is only honest
while the reaching has not been exhausted.**

#### The band as it stood — access blocked, the register exists and we cannot reach it (2 cities)

> ⚠️ **▲▲▲ Hong Kong left this band on 2026-09-22, and it was never
> actually blocked.** It was recorded here as *"the portal is a measured
> negative (statistics only), but FEHD's register exists and is queryable —
> no bulk export found"*, and described as **the single most valuable open
> thread in the screen**. It was. **`data.gov.hk`'s CKAN `package_list`
> returns 3,821 datasets and nobody had pulled it** — the recorded negative
> was a search result. Enumerating found FEHD's own licensing system
> published as bulk XML: `LP_Restaurants_EN.XML`, `LP_OtherFood_EN.XML` and
> `LP_NonFood_EN.XML`, regenerated daily. **A negative from search is a
> statement about the search**, which Stockholm demonstrated the same morning
> and which cost this city several sessions of being called unreachable.

**None of these is a data negative, and the distinction is the whole point of
the band.** Rail is answered for all three. What is missing is a route to a
register that is known to exist — which is a different thing from a register
that was looked for and was not there.

**Five cities left this sub-tier on 2026-09-22** — Santiago, Kuala Lumpur,
Jakarta, Medellín and Lima — all to *discarded*, each with a measured reason.
What remains is the set whose business leg is genuinely still open.

⚠️ **Rio de Janeiro left too, and it was a FILING error rather than a new
measurement.** Its row read *"CNPJ, no coordinates → geocoding at São Paulo's
scale"* — which describes a **geocoding** blocker, while this sub-tier means
*the business leg is the blocker*. Rio's business leg is **CNPJ, the same
national register as São Paulo**, which sits in the coordinates band as
viable, and the Tier
view already paired them. **Rio had been banded by how it was DISCOVERED — the
OSM rail screen, which is what populated D-b — rather than by what is stopping
it**, and was never re-filed once the business leg resolved. That is the one
thing this band exists to encode, so the row was moved to the coordinates
band.

Rail screened via OSM. **Relation counts are upper bounds** — see the caveat
below.

> ⚠️ **None of these five is a discard candidate, and two rows were wrong.**
> Checked 2026-09-22 by fetching each host *and* asking the Internet Archive
> whether it has seen it recently — a recent snapshot behind a failing fetch
> means **the site is alive and the failure is ours**. That test has corrected
> this project three times in one session (Sevilla, Sofia, Bulgaria's 403).
> Here it found Hyderabad's portal recorded as "dead" when it is alive,
> Kochi's row describing a **live lead nobody had followed**, and Tel Aviv's
> city portal alive behind a block aimed at us. **Unreachable is not a
> finding.**

| City | Rail (OSM) | Business leg |
|---|---|---|
| ▲▲ **Tel Aviv** 🇮🇱 | *(later discarded — see the closed awaiting-permission band)* | **PROMOTED OUT OF BAND D 2026-09-22 — to Band B. Both legs measured.** The WAF-blocked portal was never the only host: `gisn.tel-aviv.gov.il` answers, and carries **22,176 licensed businesses** with activity *and* location. See the closed awaiting-permission band below |
| **Hyderabad** 🇮🇳 | 6 rel, all named + coloured | ⚠️ **RE-PROBED 2026-09-22; every remaining route is now closed too.** `ghmc.gov.in` — the licensing body — returns **403 in a real browser**, an F5 WAF page that names itself. `data.telangana.gov.in` resolves but is unroutable for us; it runs **DKAN**, and **the Archive holds ~200 URLs but not the dataset-list endpoint**, so the route that enumerated Romania does not work here. `tgbpass` is a false friend — *building* permits. And **`api.data.gov.in`'s `q` parameter is INERT**: `Telangana` and `zzqqxxnonsense` both return the identical **288,011**, so the national API cannot be filtered at all — only its website search can, and that was already measured negative. **Blocked, not negative** |
| **Kochi** 🇮🇳 | 2 rel, named + coloured | ⚠️ **PROBED 2026-09-22, and the lead was a FALSE FRIEND.** `go.lsgkerala.gov.in/pages/query.php?t=establishment` is a **Government Orders and Circulars search** — "establishment" matches 6,526 orders about *staffing*; Kochi's own `/establishment/396` is ജീവനക്കാര്യം, its **personnel** page. In Indian government usage "establishment" means staff posts, not premises. The real route is **K-SMART** (`tax.lsgkerala.gov.in` redirects to `ksmart.lsgkerala.gov.in`) and **Sanchaya** — both live, both **transactional citizen portals** for paying tax and renewing licences, **no bulk export found**. Kerala's local bodies do issue the licences, so the register exists. **The Hong Kong shape: blocked, not negative** |

#### Paris / SIRENE — the measurement, 2026-09-22

**The architecture question was answered by Mexico, not by argument.**
`pipeline/countries/mexico.py` holds the national facts and the two city
configs differ by one line (`DENUE_STATE_CODE`). Milan is already in Band A on
`codice_ateco`, the same NACE family as France's NAF. So "a national register
is not the shape this project is built around" is **no longer true**, and the
France entry had been carrying an objection the project had outgrown.

**What Mexico does NOT answer is the kind of source.** DENUE is a **field
survey** — INEGI enumerators visit, so a row is a place that exists. SIRENE is
an **administrative register** — a row is a declaration. Measured on Paris
(commune codes 751xx, `etatadministratifetablissement = Actif`), via the
uncapped SIRENE v3 établissement stock (43,896,818 rows):

| | |
|---|---|
| All active établissements | **1,335,566** — one per 1.6 residents. Not premises |
| ...of which **sièges** | **1,231,822 (92.2%)** |
| NAF 47+56+96 buckets | **148,633** |
| ...of which sièges | **128,655 (86.6%)** |
| ...non-siège secondary premises | **19,978** |
| NAF **47.91B**, online retail | **20,542** — 24% of the whole retail division |
| Masked (`statut P`) | **176,404 (13.2%)** |

**The 148,633 is a trap.** It sits almost exactly on Madrid's 148,814, which
makes it read as a pass — but that is a coincidence of magnitude, not of
shape. 86.6% of it is sièges, and this project's invariant is explicit that
*a registrant's own name at what looks like their home* is not publishable
**even from a public registry**. This is the registered-office trap that
disqualified Germany, Austria, Latvia and Slovakia, arriving through a source
that passes every legal and access test.

**Paris has no municipal premises survey to substitute.** `opendata.paris.fr`
enumerated in full — **490 datasets** — and the closest things to a commerce
layer are `terrasses-autorisations` (24,287 terrace and display permits),
`commerces-eau-de-paris` (1,500 shops stocking the water utility's product),
`commerces-semaest` (311 units owned by a city property company) and
`plub_protcom` (5,107 **zoning** protections on commercial frontages). None is
a register of businesses. Note `marchés` here is a false friend — it means
public procurement.

**UNRESOLVED, and recorded as such:** whether APUR's **BDCom** — the Paris
commercial-premises survey, the Montréal `locaux-commerciaux` shape — is
published anywhere. `apur.org`'s site search **silently ignores the query
term**: `BDCom` returns **131 pages** of unrelated studies. So this is "could
not confirm", not "absent". It is no longer needed, but it would still be a
better source than a filtered register if it exists.

#### ✅ RESOLVED the same day: the filter works, and Paris is back in Band A

**The question was "can a NAF + siège + employee filter produce a defensible
storefront layer without mapping homes?" The answer is yes — and the siège
half of that question was the wrong lever.**

| Candidate filter, Paris NAF 47/56/96 | Rows |
|---|---|
| base | 148,633 |
| minus 47.91 online retail | 115,889 |
| **non-siège only** | **19,978 — far too aggressive** |
| not a sole trader, minus online | 79,359 |
| **A: `caractereemployeuretablissement = "Oui"`, minus online** | **50,156** |
| both employee and not-sole-trader | 47,833 |

**Filtering on siège is wrong and would have been a quiet disaster.** An
independent shop *is* its company's siège, so "non-siège only" keeps chain
branches and discards every independent — the exact inverse of what this map
is for. The **employee** filter is the right one: it keeps the boulangerie run
as an *entreprise individuelle* with staff, and drops the consultant
registered at home.

**Validated against OpenStreetMap**, which has no relationship to SIRENE:

| | OSM | SIRENE filtered | |
|---|---|---|---|
| One class — restaurants | **10,642** (`amenity=restaurant`) | **10,595** (56.10A + employer) | **0.4% apart** |
| Whole layer | **54,198** (`shop=*` 34,801 + food amenities 19,397) | **50,156** (candidate A) | **92.5% of OSM** |

Landing just *under* a volunteer map in a city as well-mapped as Paris is
where a register-derived layer should sit. The ~4,000 gap is the price of
dropping genuine zero-employee shops, and it is small next to the 65,733 rows
the filter removes.

**And there is no geocoding leg.** **148,576 of 148,633 (99.96%)** carry
`geolocetablissement` coordinates. France was being priced as if addresses
needed geocoding; they do not.

**What is still owed, and it is not a formality.** `employer = Oui` removes
home registrations **by proxy, not by proof** — a home-based business can
employ someone. So `check_personal_exposure.py` is load-bearing for Paris in a
way it is not for a municipal licence register, and a residential-address
check belongs in its Step 2. Separately, the Opendatasoft mirror used here
omits `enseigne1Etablissement` and `denominationusuelleEtablissement` — the
shop-sign fields, which are the strongest storefront signal available. INSEE's
own file carries them and would improve the filter further.

> **The relation counts are upper bounds.** The construction filter flagged
> unbuilt routes in Jakarta but returned **zero** for Tel Aviv, Bogotá and Rio —
> and Tel Aviv proves zero does not mean zero: its Green and Purple lines are
> under construction and OSM carries them as plain `light_rail` with no status
> marker. **A filter returning zero can mean "nothing to flag" or "this
> convention is not used here", and the result alone cannot tell you which.**


### ✗ CLOSED — awaiting permission (formerly Band B; Tel Aviv, discarded on terms)

**Band B held cities whose blocker was answerable at a desk.** Its last
member's desk work was done — the licence was read — and the answer was a
prohibition, which is not a desk problem. **The owner's call, 2026-09-22: a
written request made in advance and against explicit restrictive clauses is
not worth the effort.** That is a judgement about cost and likelihood, not
about the data, and the full measurement is kept below precisely so the
distinction survives.

**▲▲ Tel Aviv** 🇮🇱 — **promoted from Band D-b on 2026-09-22, and it is the
strongest unbuilt result outside Band A.** It had been carried as
*unreachable*: `opendata.tel-aviv.gov.il` and `www.tel-aviv.gov.il` both
return **HTTP 472**, Imperva's block code, and an earlier pass recorded the
host printing our own IP back — the one unambiguous IP-level refusal in this
project.

**The portal was never the only host.** `gisn.tel-aviv.gov.il` answers us
normally and serves `IView2`, the city's public map viewer — **254 layers**,
no key, no account. Third city in one day where the portal was walled and the
GIS service host was not.

| Layer | Rows | |
|---|---|---|
| **[964] `מאגר עסקים ברשיון או בהיתר`** | **22,176** | businesses holding a licence or permit — **the candidate** |
| [925] `עסקים` | **37,392** | businesses, with street + house number and floor area |
| [433] `רישיונות בביצוע` | 2,466 | licences in progress |
| [679] `מתחמי רישוי עסקים` | 29 | licensing zones (polygons) |

**Both halves of the location/activity split are present**, which is what
disqualified Tallinn, Colombia and Jakarta:

- **Activity** — `t_hesber_mahut_esek` in plain Hebrew (*grocery*, *building
  materials and paints*, *baking powder and pudding*) **plus** `mahuiot`,
  the numeric licensing-item code (406300, 407202, 1007200…).
- **Location** — `shem_rechov` (street), `ms_koma` (floor), and **point
  geometry in `wkid=2039`, Israeli TM — already projected in metres**, so
  no reprojection guesswork and no EPSG:4326 buffering trap.
- **Freshness** — `date_import` reads **20/09/2026**, two days old.

**Two questions, and both are owner decisions rather than probes:**

1. **Which business layer, and a privacy check.** [925] is larger (37,392)
   but carries **`shem_machzik_rashi` — "name of main holder"**, which is
   squarely the *registrant's own name* category this project's invariant
   excludes. [964] carries `t_shem_esek`, a **trade name**, which is the
   safe field. Recommendation: **build on [964]** and treat [925] as a
   cross-check only. `check_personal_exposure.py` must run either way.
2. **Licence — READ 2026-09-22, and it is the opposite of what "unread"
   suggested.** This was recorded as a gap to fill. It is filled, and what
   was behind it is a **prohibition**, not a silence.

   Read from the Internet Archive, because every page that carries terms is
   on the 472-blocked host — the same route that read Barcelona's and
   Sevilla's licences.

   | Source | What it says |
   |---|---|
   | **Municipal Terms of Use** (`/About/Pages/TermsofService.aspx`, captured 2026-04-21) | *"**אין להעתיק, לשחזר, לשנות, לעבד… להפיץ, לשכפל… לפרסם ו/או לאחסן את תוכן האתר**"* — do not copy, reproduce, modify, process, distribute, duplicate, publish and/or store the site's content |
   | The same document | *"**אין להשתמש בתוכן האתר ליצירת מאגר מידע ו/או לקט**"* — **do not use the content to create a database or compilation** |
   | The same document | forbids use on **other websites**, for any purpose, ***בין מסחרית ובין שאינה מסחרית*** — whether commercial or non-commercial — **without explicit prior written consent** |
   | Its definition of *"contents"* | explicitly includes **`מאגר נתונים`** — a database |
   | **`opendata.tel-aviv.gov.il`** footer (captured 2019-10-14) | ***כל הזכויות שמורות לעיריית תל-אביב-יפו*** — **All rights reserved** |
   | `data.gov.il` | Tel Aviv is **not** among its four municipal publishers — nothing to inherit |
   | ArcGIS server root, `/rest/info`, service | **no `licenseInfo`, no `copyrightText`** at any level |

   **The counter-reading, stated rather than resolved.** The Terms are titled
   *terms of use of the **website***, say *"תוכן האתר"* throughout, and the
   data sits on a **different host** (`gisn.tel-aviv.gov.il`). That is the
   **New York** situation from `read-licence`: an "All Rights Reserved"
   footer covering site content while the data itself was unrestricted.

   **But New York had an affirmative law — Local Law 11 of 2012 — forbidding
   the City to attach restrictions to its open data. Nothing equivalent is
   established for Tel Aviv**, the Terms explicitly name databases, and the
   open-data portal **asserts** rights rather than granting them. On the
   evidence the restrictive reading is materially stronger, and
   `read-licence` step 8 forbids resolving it in this project's favour.

   ⛔ **So Tel Aviv is not buildable on what is known.** The remedy is not
   more reading — it is **explicit prior written consent from the
   Municipality**, which the Terms name as the route. That is the
   **Philadelphia shape**, with one difference that matters: Philadelphia was
   already built and stands on a disclosed reasoned position, while Tel Aviv
   **has not been built and should not be** until permission exists. Tracked
   as `docs/gated_access.md` item 8.

**Rail is present but needs a scope decision, not a probe.** The city
publishes its own: Red Line stations **12**, Green **33**, Purple **19**,
with alignments. **Green and Purple are still under construction** — drawing
them would map lines that carry no passengers, the inverse of the
Guadalajara problem. Red is the operating line, and its 12 stations are the
in-city segment of a 34-station route that runs to Petah Tikva and Bat Yam,
so a boundary decision is needed too.

▼ **Valencia, Bilbao and Málaga left this band on 2026-09-22** — all three
probed, all three measured negative, all three now in *Discarded*. The
reasoning that put them here was *"two of the three Spanish cities probed have
had a register, which raises the prior sharply."* **The prior was wrong.**
Madrid and Barcelona are the exceptions in Spain, not the rule — see
"Spain is a two-city country" below.


**These two were sub-tiers of the former Band D**, which dissolved on
2026-09-22 when its live halves became Bands D and E. Both closed the same
day, and their contents are the evidence behind three discards — **Tallinn,
Sofia and Sevilla**. Kept whole, including the parts that turned out to be
wrong, because a superseded reading is how the corrected one gets checked.

### Former D-c — ✗ CLOSED (Tallinn and Sofia, both measured out)

**Finalised 2026-09-22.** These were "genuinely unreached, no finding either
way". All six are now reached and the sub-tier is closed out:

| | |
|---|---|
| ▲ **Stockholm** | promoted out — **now in the one-bucket band** |
| ▲ **Bucharest** | promoted out — **now in the coordinates band** |
| ✗ **Budapest** | **discarded** — both routes measured closed |
| ✗ **Zagreb** | **discarded** — 210 Grad Zagreb datasets, one commercial, and it is a grants list |
| ✗ **Sofia** | **discarded** — the block was routed around, and Sofia publishes no premises register |
| **Tallinn** | **parked on value**, with the äriregister half now measured |

**Sofia was the load-bearing example of "unreachable is not a negative" — and
it stopped being one.** Going around the 403 via the EU portal's SPARQL
endpoint turned it into a firm data negative, which is the outcome that
distinction exists to make possible: *reach it, then judge it.* **Tallinn is
now the only genuinely-unjudged city left in this band.**

| City | What the host actually does |
|---|---|
| ✗ **Tallinn** 🇪🇪 | **DISCARDED 2026-09-22 — MTR reached, downloaded whole, and measured.** No longer parked: the register that was going to be Tallinn's route has **no location data of any kind.** See below |
| ✗ **Sofia** 🇧🇬 | **DISCARDED 2026-09-22 — and on data, not on the block.** See the section below: the entire Bulgarian catalogue was enumerated from outside, and **Sofia does not publish a commercial-premises register.** The 403 was never what stopped it |

#### 🇪🇪 Tallinn: MTR reached and measured — 2026-09-22

The äriregister was already known to be company-shaped. **MTR**
(Majandustegevuse register) was the remaining hope, recorded as *"live HTML
with no API found, so it needs the browser"*. It needed no browser. Its
`andmed.eesti.ee` catalogue entry names a bulk export outright —
`mtr.ttja.ee/opendata/avaandmed_ettevotjad.xml`, `access: PUBLIC`,
`accrualPeriodicity: DAILY`, `applicableLegislation: ODD_LEGAL_ACT`.

**Note the recorded blocker was also wrong.** The search API was filed as
*"contract unpinned — 400 on empty `search` and on `limit=1000`"*.
`search=<term>&limit=5&page=1` answers fine; the contract simply rejects an
*empty* term. A parameter that refuses one value is not an unpinnable API.

The export is **102 MB**. It was downloaded in full and every element name
counted, rather than sampled — the head of the file is unrepresentative
(the first records are French and Polish cross-border filings, which would
have no Estonian premises anyway, and reading those two would have produced
the right answer by the wrong method).

| | |
|---|---|
| Undertakings | **56,401** |
| Licences | **100,431** |
| Estonian | **97.8%** (55,184) |
| Distinct element names in the whole file | **17** |
| **Elements naming a place** | **ZERO** |

The complete tag census is `ettevotja · registrikood · nimi · riik_kood ·
url · load · luba · tyyp · number · staatus · valdkond · tegevusala ·
emtak · emtak2025 · kood · kehtiv_alates · kehtiv_kuni`. No address, no
tegevuskoht, no coordinates. *(`vald` appears only inside `valdkond` —
a substring, not a field.)*

**This is the pure Colombia-RUES shape**: complete activity classification
(114 distinct `tegevusala`, plus EMTAK 2008 and 2025 codes) attached to no
location at all. And it fails the composition test independently — the
largest category is **`Teenindajakaart`, 25,130 service-worker cards**,
followed by freight-transport community licences and taxi vehicle cards.
**Personal and vehicle certifications, not premises.** Only `Toitlustamine`
(5,576) and `Jaekaubandus` (4,120) are storefront-shaped, and those are
Estonia-wide, not Tallinn.

Tallinn was parked on *value* — trams only, ~450k, the thinnest map in the
screen. It is now closed on *data*, which is the better reason.

#### 🇧🇬 Sofia resolved by going around the 403 entirely — 2026-09-22

`data.egov.bg` returns **403 in the browser as well as to curl**, resolves
fine via DoH (213.91.191.234), and the Internet Archive holds a 2026-04-02
snapshot — so the host is up and the refusal is **aimed at us**. That was
where this sat: *blocked, nothing learned.*

**`data.europa.eu`'s SPARQL endpoint harvests `data.egov.bg`, and it is a
different host.** Querying it recovered **11,635 Bulgarian datasets**
(ids 3–23,557) without ever touching the blocked origin. What they contain
settles Bulgaria:

| | Found | |
|---|---|---|
| `Регистър на търговските обекти` — commercial premises | **141** | across ~50 municipalities: Враца, Мадан, Костинброд, Карлово, Дупница, Тервел, Етрополе, Драгоман, Ихтиман… |
| `заведения за хранене и развлечения` — food & entertainment | **72** | the same shape again |
| **Столична община (Sofia)** | **76 datasets** | **neither register among them** |

Sofia publishes budgets, school and kindergarten lists, parking and
**taxi permits**, dams, war memorials, donations, municipal enterprises.
**No premises register of any kind.**

**So Bulgaria fails structurally, not administratively.** Its municipalities
publish exactly the register this project needs — routinely, ~50 of them —
but every one is a small town. **Sofia is the only Bulgarian city with a
metro.** The data exists where there is no rail; the rail exists where there
is no data. No amount of access changes that, which is why this is a
discard rather than a park.

**One limit on the technique, measured rather than assumed:** **0 of 20**
sampled records carry any `dcat:distribution`. The harvest is
**metadata-only** — titles and descriptions, no download URLs. The EU portal
is a **catalogue, not a bypass**: it can tell you what exists anywhere in the
EU, and the files stay behind whatever wall they were behind. That is enough
to *screen* a blocked country, and not enough to *build* one.

### Former D-d — ✗ CLOSED (Sevilla, reached and discarded)

**The whole sub-tier is closed.** Its single city was reached, measured and
discarded on the same day it was written up as unreachable. Read the section
below top-to-bottom: it is kept in full *because* the first two thirds are
wrong, and the correction at the end is the only part that stands.

▼ **Sevilla** 🇪🇸 — **downgraded 2026-09-22.** The rail half is unchanged
and still cheap: Spain's National Access Point answers **401**, the WMATA
shape, a free account. **The business half got worse.** Every route into the
city's own data failed:

| Route | Result |
|---|---|
| `www.sevilla.org`, `sevilla.org` | **do not resolve** — curl *and* browser |
| `datosabiertos.sevilla.org`, `.es` | do not resolve |
| `sevilla-ayuntamientodesevilla.opendata.arcgis.com` | live, but **"Can't access this content … Sign In"** — the Medellín shape |
| `datos.gob.es` federated catalogue | **no Ayuntamiento de Sevilla publisher exists.** The publishers returned for "Sevilla" are CIS (opinion surveys), **IGME (geological maps)** and the Junta de Andalucía |

**⚠️ DNS-over-HTTPS, 2026-09-22 — and it splits the failure in two:**

| Host | Cloudflare DoH | Meaning |
|---|---|---|
| `www.sevilla.org` / `sevilla.org` | **resolves → 94.198.88.169** | The host exists. Our 000 is a **routing failure on our side**, not DNS |
| **`datosabiertos.sevilla.org`** | **NXDOMAIN** | **The open-data subdomain genuinely no longer exists — for anyone.** The 521-dataset portal at that address has been retired |

**So Sevilla is two problems, not one.** The city's main site is reachable in
principle and blocked only to us; the open-data portal we were trying to reach
is **actually gone**. Whatever replaced it has not been found — and the ArcGIS
Hub, which is the obvious successor, is the sign-in-walled one. **That is the
thread to pull**, not the dead subdomain.

> ### ✅ RESOLVED 2026-09-22 — the thread was pulled, and it led all the way
>
> **Sevilla is now a measured negative on the business leg and a SOLVED rail
> leg.** Both halves above are superseded. How it opened:
>
> The last Archive capture of the dead portal (2024-04-25, already serving
> **503**) contains, in its own JavaScript, a KML link to
> `sevilla.idesevilla.opendata.arcgis.com/datasets/5df7320…_0.kml`. **A dead
> page named its successor** — that is the general lesson, and it cost one
> CDX query.
>
> **The sign-in wall was the HUB, not the DATA, and that reading was wrong.**
> Recorded above as "the Medellín shape", i.e. genuinely private. In fact
> `www.arcgis.com/sharing/rest` serves the city's public items **anonymously**,
> from org **`hcmP7kr0Cx3AcTJk`** on `services1.arcgis.com` — a host that
> answers us, while every `sevilla.org` address is retired or unroutable.
> Enumerating by owner returned **1,260 public items, 413 Feature Services.**
>
> **🚇 The rail leg is SOLVED, and the 401 is now irrelevant.** The city
> publishes its own metro:
>
> | Layer | Rows | |
> |---|---|---|
> | `METRO_Estacion` | **21** | `NOMBRE` — Ciudad Expo, Cavaleri, San Juan Alto… real named stations |
> | `METRO_Linea` | **20** | polylines with `ID_EST_INI`/`ID_EST_FIN` segment topology |
>
> No account, no NAP, no OSM. **Spain's National Access Point and its 401 are
> not on Sevilla's critical path at all.**
>
> **✗ The business leg is a firm negative**, and `Locales` is a **false
> friend** — the same trap as Kochi's "establishment", caught the same way,
> by opening it:
>
> | Layer | Rows | What it actually is |
> |---|---|---|
> | `Locales` + 10 district copies | **150** | `USO = VACÍO`, `ENTIDAD_CESIÓN_USO`, `ADSCRITO_A`, `Editor = 6_Empleo` — the city's own **vacant municipally-owned units offered for assignment**, published by the Employment directorate |
> | `BIENES INMUEBLES` × 11 districts, `Naves Industriales` | — | municipal **property holdings**, same family |
> | `APP_Mercados` / `Centros_Comerciales` | 18 / 120 | market *buildings* and shopping centres — **the Málaga shape**, `equipamientos` facility layers |
> | `Veladores_2023` | **389** licences (2,897 furniture items) | pavement-terrace occupation, EPSG:25830 |
>
> **Row count is what caught it.** `Locales` returns 150 city-wide and **1 for
> Triana**; Madrid's censo has 225,660. A name that matches Madrid's word for
> the right dataset, at 0.07% of the scale.
>
> All 413 Feature Services were scanned by title, not just keyword-filtered —
> the Bulgarian sweep's lesson about partial scopes applied to my own work.
> Nothing else is business-shaped. **Sevilla is DISCARDED on data.** The one
> real premises signal, 389 terrace licences, is a single narrow bucket far
> below Stockholm's 8,146 food premises, which is itself only a one-bucket
> city.

**And the Internet Archive confirms the portal was real while it lasted:**

| | |
|---|---|
| `www.sevilla.org` snapshot | **2026-09-12** — ten days old. **The site is alive** |
| `datosabiertos.sevilla.org` snapshot (2023) | **521 datasets, 1,345 distributions** — a real municipal portal |
| Enumerable from the archive? | **No.** The crawl is 347 URLs deep, 11 of them datasets, none commercial |

**This is unreachable, not a measured negative**, and the distinction is the
one this list's maintenance rule exists to protect. **Discarding Sevilla would
mean throwing away an unexamined 521-dataset catalogue because of our own
DNS.** Nothing has been learned about whether Sevilla licenses premises; only
that every route to asking is blocked on this side. **One attempt from a
different network settles it.**

**↑ That paragraph was right to refuse the discard and wrong about what it
would take.** It concluded a different *network* was needed; what it actually
took was a different *host* — `services1.arcgis.com`, reachable all along.
The rule held and protected the city from a premature discard; the cost
estimate attached to it was guesswork. **See the resolution above.**

## DISCARDED — 27 cities, each naming its evidence

▼ **2026-09-24 (evening) — the open gap's last three discards, on the owner's calls after a final re-probe**: Vienna (absence, now on the city's own hosts twice over), Santiago (coverage: four central comunas publish no current list) and Nagoya (the published permit stream carries only half the permits issued, so no rebuild can work).

▼ **2026-09-24 (morning) — five rows arrived from the open gap on the owner's calls**, each after its re-probe: Kuala Lumpur, Athens, Poznań and Bratislava on two-method negatives with the city's own host asked, and Hamburg on currency. Vienna, whose negative would also pass, stays in the gap by the owner's choice. **Naples, Lima and Messina followed later the same morning**, after the last re-probe batch.

▼ **2026-09-24 — thirteen rows left this table on an audit.** Every row was read
against the probe log and sorted by the kind of evidence behind it. **Twelve
rested on ONE method** — a national portal only, the city's own host never
asked, or the top hits of one search — which `add-country` says is an
ASSERTED negative, not a finding; they are in the open screening gap as a
re-probe queue (owner's call). **Amsterdam** went further: its own API
carries a current hospitality register, and it is in Band C. The 21 left
each rest on two methods, a measured register, or its terms.

▼ **Five of those 21 left the same night** (owner's call), when the columns
below were added and the check read them: Hyderabad, Naples, Santiago, Lima
and Messina. **The audit had sorted on the rows' wording again** — the very
failure it named — and the columns are what caught it.

**Every row carries its evidence as columns since 2026-09-24**, and
`scripts/check_discard_evidence.py` reads them. *Kind* says what the discard
claims; *Methods* lists each probe by its shape (`search`, `enumerated`,
`measured`, `read`, or `blocked`, which counts for nothing). An **absence** or
**coverage** row — one resting on something NOT being found — needs the city's
own host asked and two methods, or one that read the whole catalogue or
measured a register. A one-search negative cannot be added here without the
check refusing it. **Turin** and **Cairo**, the last two rows, came from the
open screening gap on 2026-09-24, each measured by two methods.

▼ **Cairo left this table on 2026-09-23** for the open screening gap. Its row
read *"No open-data infrastructure"*, which rests on one probe of one national
host, and the file's own sweep had already recorded it as unprobed. **A discard
row has to survive being read against the probe log; that one did not.**


▼ **Lisbon and Warsaw — added here by the 2026-09-23 sweep — left on
2026-09-24** with ten other single-method rows: see the note above the
open screening gap's table.

| City | Kind | Methods | City host asked? | Why |
|---|---|---|---|---|
| **Lyon** 🇫🇷 | terms | measured the data (~18,082 bucket rows) · read Grand Lyon's CGU · measured its National Access Point feed (dead since 2022-04-14) | yes — `data.grandlyon.com`, behind an account | **DISCARDED 2026-09-23 on FOUR independent blockers, not one.** Its DATA is fine — ~18,082 bucket rows, **51.4% named**, better than Paris — which is why this is a discard on terms and access rather than on data. **(1)** An account on `data.grandlyon.com` is required before any download, and this project does not create accounts. **(2)** Grand Lyon CGU **9.4** is an open-ended indemnity. **(3)** CGU **6.2** bars the producers' *signes distinctifs* *« associés ou non à l'utilisation des données »* — which collides with the invariant that every drawn line carries its real public name, Lyon's being **TCL**. **(4)** Its National Access Point feed is **DEAD since 2022-04-14** (0% availability) while the source portal is current, so even with the account the rail must come from behind it. ⚠️ **Toulouse's and Rennes' CGU were read 2026-09-23 and are CLEAN** — Opendatasoft template, no indemnity, marks clause excluding the data — so **Lyon's clauses are Grand Lyon's own, not a French pattern.** **Reinstatement template in `DECISIONS.md`, 2026-09-23** |
| **Tel Aviv** 🇮🇱 | terms | measured the register (22,176 rows) · read the municipal Terms of Use | yes | **DISCARDED ON TERMS, NOT ON DATA — owner's decision 2026-09-22.** The data is the strongest of any unbuilt city: **22,176 licensed businesses** with activity *and* location, **EPSG:2039 already in metres**, refreshed within two days. **The municipal Terms forbid it** — no copying, distributing or publishing, **no using the content to create a database**, extending to other websites and to non-commercial use, and requiring **explicit prior written consent**; the open-data portal's footer reads *all rights reserved*. The only remedy was a written request, made **in advance and against explicit prohibitions** — judged not worth the effort against its likelihood. **Not a data negative**, and the full measurement is retained below |
| **Kochi** 🇮🇳 | absence | enumerated the national catalogue · read K-SMART and Sanchaya (one licence at a time, no bulk export) · search `?t=establishment` (staff posts) | yes — K-SMART, which issues the Corporation's licences | **Same national sweep, same result** — India publishes trade-licence **counts**, never premises. Kerala's own route is transactional: K-SMART and Sanchaya renew licences one at a time with no bulk export, and the `?t=establishment` lead was a **false friend** — in Indian government usage *establishment* means **staff posts**, and that search returns 6,526 orders about staffing |
| **Sofia** 🇧🇬 | absence | enumerated `data.europa.eu`'s harvest of `data.egov.bg` (11,635 datasets) · blocked `data.egov.bg` (403 aimed at us) | yes — Столична община's own 76 datasets, read in full; `www.sofia.bg` not read | **11,635 Bulgarian datasets enumerated via `data.europa.eu`'s SPARQL endpoint, around a 403 aimed at us.** 141 municipal premises registers exist nationally; **Sofia's 76 datasets include none.** Its registers are all small towns — Sofia is Bulgaria's only metro city |
| **Sevilla** 🇪🇸 | absence | read the dead portal's last Archive capture · enumerated the city's ArcGIS org (1,260 items) | yes | **1,260 public ArcGIS items / 413 Feature Services enumerated** from org `hcmP7kr0Cx3AcTJk` after the dead portal's last Archive capture named its successor. **Rail is solved** (`METRO_Estacion` 21, `METRO_Linea` 20, no account). **No premises register**: `Locales` is 150 *vacant municipally-owned units*, the rest are property holdings and facility layers |
| **Berlin** 🇩🇪 | absence | search `datenregister.berlin.de` (three terms, control 0) · search `ckan.govdata.de` | yes | `Gaststätten` → 0 on `datenregister.berlin.de`; the Gewerberegister is not open data |
| **Bogotá** 🇨🇴 | rail | read its OSM relation (no ref, no colour) · measured the TransMilenio hub (153 BRT stations) | yes | **Fails on rail** — one unnamed-ref, zero-colour relation; its only mass transit is BRT |
| **Medellín** 🇨🇴 ↓ | measured | measured RUES (6,369,877 rows, no location column) · read the chamber's comuna×CIIU crosstabs · read the city's ArcGIS Hub (credential wall) | yes — behind a credential wall | **Three closed doors.** The city's ArcGIS Hub is **credential-walled**; the chamber of commerce publishes comuna×CIIU **crosstabs**; RUES has **6,369,877** premises rows and **no address, municipality or city column at all** |
| **Jakarta** 🇮🇩 ↓ | measured | measured the OSS register (53,827 rows, 9 columns, checked against the portal's component list) | yes | **No activity field.** The live OSS register has 53,827 rows and full street addresses across **exactly 9 columns**; the two that look like classification are legal form and business size |
| **Valencia** 🇪🇸 ↓ | absence | enumerated `opendata.vlci.valencia.es` (290 packages) | yes | **No premises register.** `opendata.vlci.valencia.es` is CKAN with **290 packages**, read in full. The only commercial-adjacent names are container locations, noise-monitoring stations and *zones d'activitats* — zoning polygons, not businesses |
| **Málaga** 🇪🇸 ↓ | absence | enumerated `datosabiertos.malaga.eu` (1,377 packages) | yes | **Business parks and facility layers only.** `datosabiertos.malaga.eu` is CKAN with **1,377 packages**. `empresas-y-sectores` is explicitly *"empresas que se encuentran en **parques empresariales**"*; `centros-comerciales` and `mercados` are `equipamientos` layers — a handful of malls and municipal markets. Licence is CC **BY-SA** |
| **Budapest** 🇭🇺 ↓ | absence | read `kozadat.hu` (an inventory search tool) · read Nébih's FELIR (CAPTCHA-gated lookup) and its two establishment PDFs · read `budapest.hu` (two data-ish links) | yes — `budapest.hu`; `opendata.` and `adatportal.budapest.hu` do not resolve | **Both routes closed.** Portal: `kozadat.hu` is a search tool over data inventories, not a data portal. Food authority: Nébih's FELIR is **CAPTCHA-gated** and is a one-customer lookup, not a register; its *Approved Establishments* holding is **two PDFs of processing plants** — slaughterhouses, dairies, egg packers, cold stores. Retail and catering are only *registered*, by county offices, unpublished |
| **Zagreb** 🇭🇷 ↓ | absence | enumerated `data.gov.hr` (3,889 packages; Grad Zagreb's 210) | yes — Grad Zagreb's own publisher account, read in full | **210 datasets, one commercial, and it is a grant list.** `data.gov.hr`'s CKAN lives at **`/ckan/api/3/...`**, not `/api/3/...` — 3,889 packages once found. **Grad Zagreb** publishes 210 of them; the only commercial one is *Lista za dodjelu potpora … obrtničke djelatnosti*, a grants register. Croatia devolves to municipalities and the only business databases belong to villages — `baza-poduzetnika-i-obrtnika` is **Grad Ivanec** (pop. 13,000) and carries `adresu sjedišta`, the **registered office** |
| **Bilbao** 🇪🇸 ↓ | absence | read the city's portal (344 datasets, no search) · enumerated `datos.gob.es` publisher `A16003011` (600 datasets) | yes | **Aggregate barometers only.** Its own portal holds 344 datasets behind a paginated list with **no search** (its one form control is a sort order). Enumerated instead via `datos.gob.es`: **600 datasets** under publisher `A16003011`, whose entire commercial holding is *"Barómetro del comercio minorista"* — retail-trade survey aggregates by employment stratum, sector and territory |
| **Turin** 🇮🇹 | absence | search `aperto.comune.torino.it` (control 0) · search `dati.gov.it` (control 0) | yes | **Stale, and nothing replaced it.** The city's CKAN (`aperto.comune.torino.it`, nonsense control 0) holds *"Attività commerciali presenti 2019"* as its newest premises stock; every later commerce dataset is the statistical yearbook (aggregate). Italy's national catalogue (`dati.gov.it`, control 0) finds for Turin only animal-food processing plants, a regional summary and a 2009 survey. A map of 2019 premises is not a map of current density |
| **Cairo** 🇪🇬 | absence | read `cairo.gov.eg` · read CAPMAS (HTML only) | yes | **No register at any level.** The Governorate's own site (`cairo.gov.eg`, reached 2026-09-24) has no open-data section: a services portal, a population dashboard, a government-services map, and a **tourism guide of ~220 restaurants and ~50 malls** — a curated list for a city of 10 million, the Kuala Lumpur coverage trap. Nationally, CAPMAS serves HTML only |
| **Kuala Lumpur** 🇲🇾 | absence | enumerated DBKL's open-data page (10 datasets) · enumerated DBKL's ArcGIS server (two folders token-gated; `Hosted/LESEN_AKTIF` is 102 rows beside 42 CCTV points and 73 lamps) · enumerated `data.gov.my` (292 datasets, none from a local authority) · measured DOSM's `lookup_premise` (372 KL rows) | yes — DBKL's open-data page and ArcGIS server | **No register at any level, on three methods — moved here 2026-09-24 (owner's call) after its re-probe.** DBKL's licensing register exists only internally; the one public licence layer is a 102-row dashboard mock-up, and DOSM's premises table is a price-survey frame (the coverage trap `add-country` names) |
| **Athens** 🇬🇷 | absence | enumerated the city's CKAN `opendata.cityofathens.gr` (464 datasets, nonsense control 0) · enumerated its GeoServer (60 layers) · enumerated `data.gov.gr` (22,591 datasets) · blocked `geodata.gov.gr` (times out from GR and DE) · blocked `www.cityofathens.gr` (a Cloudflare challenge, not bypassed) | yes — its CKAN and GeoServer | **No premises register on the city's hosts or nationally — moved here 2026-09-24 (owner's call) after its re-probe.** The national business-notification list is 72,378 rows from 2018 with no address and no municipality |
| **Poznań** 🇵🇱 | absence | enumerated the city portal `www.poznan.pl/opendata` (66 datasets; GraphQL, read-only POST queries; nonsense control 0) · enumerated the city's 35 datasets on `dane.gov.pl` · enumerated its feature server (35 layers), map POIs (156 categories) and GIS portal (30 services) | yes — the city portal and its GIS | **No premises register — moved here 2026-09-24 (owner's call) after its re-probe.** Alcohol permits are published only as aggregates (e.g. 840 category-A food-service permits). Side find, kept: the city portal carries a **tram GTFS modified 2026-09-18** |
| **Bratislava** 🇸🇰 | absence | enumerated the city's ArcGIS Hub `data.bratislava.sk` (680 items) · enumerated its ArcGIS Online org (2,093 items) · enumerated the geoportal server (724 of 1,023 services opened; 299 judged by name) · enumerated `data.slovensko.sk` over SPARQL (22,559 datasets) | yes — its Hub, ArcGIS org and geoportal | **No premises, food-service or opening-hours register — moved here 2026-09-24 (owner's call) after its re-probe.** The only use-class layer is a national 1.7M-point address layer whose category is the building's and partly OSM-sourced |
| **Hamburg** 🇩🇪 | absence | measured the city's 2016 retail survey (`api.hamburg.de/datasets/v1/einzelhandel`, 9,916 points, 1.17× OSM retail) · enumerated the transparency portal (521 map-service titles read) · enumerated the city API (411 datasets) | yes — `api.hamburg.de` and the transparency portal | **Stale, one bucket, and nothing replaced it — discarded on currency 2026-09-24 (owner's call).** A ten-year-old retail survey would misstate today's high streets; no food or personal-services register exists in either catalogue, and ALKIS building functions are whole buildings. Turin's shape. **Germany is again a two-city negative** (Berlin, Hamburg), each on its own hosts |
| **Naples** 🇮🇹 | absence | enumerated the city's CKAN `dati.comune.napoli.it` (37 datasets, nonsense control 0) · enumerated `dati.gov.it` for the Comune (36), the Città Metropolitana (96), Regione Campania (368) and every Napoli hit (182) · read the SUAP (on the national impresainungiorno platform; publishes no register) | yes — its CKAN and its SUAP | **No premises register — moved here 2026-09-24 (owner's call) after its re-probe.** Commerce appears only as 2014 counts per procedure and district; the national catalogue's only premises lists are pharmacies, parafarmacie and historic shops; the SUAP's only lists are 2018–2019 outdoor-seating concessions. Italy's cadastral shop category is not open data, so there is no second layer. **Italy stays a Milan-and-Rome country** |
| **Lima** 🇵🇪 | coverage | enumerated `www.datosabiertos.gob.pe`'s 78 licence datasets (1 of Línea 1's 9 districts publishes: La Victoria) · read five districts' own sites (Villa El Salvador, Villa María del Triunfo, San Juan de Miraflores, San Borja, El Agustino — forms, procedure pages, login-only systems) · search gob.pe per district · blocked the Municipalidad Metropolitana, Surco and San Juan de Lurigancho (answer from Peru only) | yes — five districts' own sites | **Coverage fails on measurement — moved here 2026-09-24 (owner's call) after its re-probe.** Licensing is per district; five of Línea 1's districts, including the whole southern arm, are confirmed to publish nothing, so the line cannot be covered even if the three geo-blocked districts publish |
| **Messina** 🇮🇹 | absence | enumerated the city's catalogue (113 datasets) · enumerated `dati.gov.it` (113 for the Comune, 140 text hits) · measured the chamber's business list (18,467 rows, head offices only, 2022) | yes — its catalogue; the licensing office is behind SPID login | **No premises register — moved here 2026-09-24 (owner's call) after its re-probe.** The chamber's list is company-level with no local units; SCIA/DIA is a 2021 flow with no activity field; a 1,531-point POI sample is not a register |
| **Vienna** 🇦🇹 | absence | enumerated the city's WFS (377 layers; the market layers are 550 unnamed stand outlines, and the only business list is 9 opt-in takeaways) · enumerated `data.gv.at` through its hub API (Stadt Wien 781 datasets; nonsense control 0) · read the national registers (GISA strips street addresses; Statistik Austria's company-to-activity file has no address; AGWR allows no public access to individual records) | yes — `data.wien.gv.at` and the city's map service, twice | **No premises register at any level.** The only premises rows on the city's hosts are outdoor-seating permits (no name, no activity, 0.42× OSM food) and market stands; the building use class is whole-building (0.19× OSM shops). The company register would give registered offices, not shops, and needs a ministry token. Re-probed twice (2026-09-24); the owner had held it in the gap after the first |
| **Santiago** 🇨🇱 | coverage | enumerated `datos.gob.cl` (272 publishers: 5 Metro comunas publish patentes) · measured Providencia's register (74,712 rows) · enumerated the comuna's GIS server (15 services; no licence or activity layer) · read `documentos.munistgo.cl` (scanned alcohol decrees only) · read the web archive's index of `transparencia.munistgo.cl` (no licence list after 2014) · blocked `transparencia.munistgo.cl` (403 to everyone) · read Las Condes, Ñuñoa, Estación Central, Macul, Maipú, Puente Alto and San Ramón's own sites | yes — every central comuna's own site | **Coverage fails downtown: Daegu's shape.** About 6 of ~33 Metro comunas publish a current list, and the four the network converges on (Santiago, Las Condes, Ñuñoa, Estación Central) publish none. The fix would take at least four transparency requests, each the owner's act and the last resort |
| **Nagoya** 🇯🇵 | absence | enumerated BODIK's food package and its full history (137 events, 61 resources: rolling 12 months of new permits) · read the web archive of the city's permit page (15 captures, 2019–2025: no standing list ever) · measured a Kyoto-style stitch against e-Stat's permits issued (new files carry 44–49% of issued, against Kyoto's 98–102%) | yes — the city's page and its catalogue | **No list, and none can be rebuilt.** The city never published a standing register, and its monthly files omit renewals, so a complete stream would reach at most about 54% of the official count, all opened since 2021. The recovered files reach 20.9%. Personal services: beauty salons only |

Plus the no-urban-rail set (Winnipeg, Hamilton, Québec City, Halifax,
Mississauga, Ottawa, ~30 single-feed countries) and access-not-data
(Russia, Ukraine).

~~**Germany is a country-level negative**, on two cities measured independently
at two different portal hosts.~~ ▼ **Not any more (2026-09-24)**: Hamburg's row
rested on one search term and is back in the open gap; Berlin's stands.
▼ **Hamburg returned the same day (morning), owner's call**: re-probed on two
methods, and discarded on currency, not on one search.

**The five added on 2026-09-22 each failed differently**, which is the useful
part: coverage (Santiago, Lima), sampling (Kuala Lumpur), no location column
(Medellín), no activity column (Jakarta). Four distinct ways for a
premises-shaped table to be unusable, and **not one of them is visible from a
dataset title**.

---

---

# BY COUNTRY — for country-by-country implementation

## ✅ Current by country — 2026-09-23

**This table is current. The Tier sections below it are the 2026-09-22 view,
retained as evidence and NOT current** — they still say Spain is in progress,
that Taiwan's geocoder is keyless, and that Hong Kong is blocked, all of which
changed. When a tier below disagrees with this table or with the bands above,
the tier is stale.

| Country | Built | Candidates | Band | What stands between it and the next city |
|---|---|---|---|---|
| 🇺🇸 United States | **9** | — | — | Complete for now |
| 🇨🇦 Canada | **5** | — | — | **Complete** — the rest have no urban rail |
| 🇲🇽 Mexico | **2** | — | — | Complete |
| 🇪🇸 Spain | **2** | — | — | **Complete** — Valencia, Bilbao, Málaga, Sevilla measured out |
| 🇮🇪 Ireland | **1** | — | — | Complete |
| 🇮🇹 Italy | **2** | — | — | **Rome built 2026-09-24**, beside Milan; bespoke per city (a SUAP premises register and the national ANNCSU join). Turin discarded (its series stops in 2019); Naples and Messina in the open gap |
| 🇫🇷 France | **5** | — | — | **Complete** — Rennes built 2026-09-23. Lyon discarded |
| 🇨🇿 Czechia | **1** | — | — | **Prague built 2026-09-24**; the national modules (ROS02, RES, the CZ-NACE 2025 prefix taxonomy, the RUIAN join) are ready for a second city |
| 🇩🇰 Denmark | **1** | — | — | **Copenhagen built 2026-09-24**; the national modules are ready for a second city. ✅ **Closed out**: published, and the Datafordeler account closed after publish (2026-09-24) |
| 🇭🇰 Hong Kong | **1** | — | ✅ | Built 2026-09-24: FEHD's registers at FEHD's own CSDI points; the East Asia region |
| 🇳🇴 Norway | **1** | — | — | **Oslo built 2026-09-24**; the national modules are ready for a second city |
| 🇰🇷 South Korea | **1** | — | ✅ | Built 2026-09-25: seventeen citywide permit registers, the register's own building points, a Korean personal-name pass (`seoul.md`) |
| 🇧🇷 Brazil | — | **9** — São Paulo, Rio, Salvador, Fortaleza, Belo Horizonte, Brasília, Recife, Porto Alegre, Santos | A | **Nothing but the builds** — one national source (IBGE CNEFE 2022), no geocoder. Briefs next, São Paulo and Rio first |
| 🇹🇼 Taiwan | **1** | **3** — Taipei (Regional), Taoyuan · Kaohsiung | A · D | **Taichung built 2026-09-25** (the national modules, the `taiwan-city` skill). **No geocoder** — a door-plate JOIN at 92.2–95.5%. Two cities build-ready; **Kaohsiung's address file is geo-blocked to Taiwan** |
| 🇯🇵 Japan | — | **10** | B | The hardest geocode; **decided: last** |
| 🇸🇪 Sweden | — | **2** — Stockholm, Göteborg | C | One owner decision (food-only pages) |
| 🇨🇭 Switzerland | — | **1** — Zurich | C | The same decision |
| 🇷🇴 Romania | — | **1** — Bucharest | C | The same decision, plus a browser-assisted fetch |
| 🇸🇬 Singapore | — | **1** | C | **Parked on one fact** — NEA refreshing its 2016 register; indemnity held |
| 🇳🇱 Netherlands | **1** | — | — | **Amsterdam built 2026-09-24** on the city's own API (permits + BAG shop units); a second Dutch city needs its own permit register - the BAG layer is national, the food layer is municipal |
| 🇪🇬 Egypt | — | — | — | Cairo discarded 2026-09-24: no register at any level |
| 🇵🇱 Poland | — | **1** — Warsaw | D | Geo-blocked before measurement; a read from inside Poland first (owner's call 2026-09-24) |
| 🇮🇳 India | — | **1** — Hyderabad | D | Geo-blocked before measurement (owner's call 2026-09-24) |
| 🇱🇻 Latvia | **1** — Riga | — | ✅ | Built 2026-09-24: excise food layer, cadastre shops and services, 7 tram routes, scoped vacancy disclosure; Europe keeps its zoom (owner) |
| 🇵🇹 Portugal | — | **1** — Lisbon | D | The DGAE account (gated item 28); Porto would follow |
| 🇫🇮 Finland | — | **1** — Helsinki | D | Geo-blocked; a read from inside Europe |
| 🇪🇪 Estonia | — | **1** — Tallinn | D | Food register geo-blocked; the EHR order (gated item 23) |
| 🇦🇹 Austria | — | — | — | Vienna discarded 2026-09-24 (no premises register at any level) |
| 🇨🇱 Chile | — | — | — | Santiago discarded 2026-09-24 (coverage fails downtown) |
| **Total** | **30** | **32** | | *(the open gap emptied 2026-09-24. ⚠️ Several rows above predate that day's builds and re-bands, Brazil and Japan among them, so this table is for the consistency sweep to refresh: trust the bands)* |

---

## The 2026-09-22 tier view — RETAINED AS EVIDENCE, NOT CURRENT

The same 48 candidates, cut the other way. **Ordered by cities gained per unit
of work**, because that is what country-by-country optimises for, and it
reorders things sharply: Japan is mid-table by city and near the top by
country.

"Missing link" = the single thing that would move the country up a tier.

## Tier 1 — build now, nothing to discover (3 countries, 4 cities ready; ✅ Mexico DONE)

| Country | Cities | Source shape | Missing link |
|---|---|---|---|
| 🇲🇽 **Mexico** ✅ **COMPLETE** | **2** — Mexico City, Guadalajara (Regional) | **DENUE**, national, coordinates, SCIAN **is** NAICS — and the taxonomy **did** transfer from the US builds | **Nothing. Both cities are built and live in the app** (`pages/15_`, `pages/16_`, region *Mexico*), 2026-09-22. The ODbL share-alike decision was taken during the build |
| 🇪🇸 **Spain** ▶ **IN PROGRESS** | **2, not 6** — Madrid building now, Barcelona next | Bespoke **per city**, and the bespoke-ness cuts both ways | **Re-scoped 2026-09-22.** Valencia, Bilbao and Málaga all probed and all measured negative. Sevilla is unreachable. **Nothing left to find; Spain is a two-city country.** Both remaining cities have briefs and 9/9 checks |
| 🇰🇷 **South Korea** ✅ **BUILT 2026-09-25** | **1** — Seoul | 17 datasets, EPSG:5174, KOGL Type 1, daily | **Built.** Were build items, not probes: the register's own building points fill restaurants to 97.7%; a Korean-aware `check_personal_exposure.py` (113 premises sized). Owner's calls decided 2026-09-24 (`seoul.md`) |
| 🇮🇹 **Italy** | **1** — Milan | Bespoke per city. Naples and Messina measured out | **Step 0 schemas** for the two newly found Milan layers. Nothing to discover |

## Tier 2 — ⇄ France: demoted and restored the same day, measured both times (1 country)

| Country | Cities | Missing link |
|---|---|---|
| 🇫🇷 **France** ▲ | **6 cities, all six now MEASURED** — Paris, Lyon, Marseille, Toulouse, Lille, Rennes | **RESOLVED 2026-09-22, and it went in favour.** Mexico closed the architecture half; the composition half was closed by an **employee filter validated against OpenStreetMap** — 50,156 rows vs OSM's 54,198, and 10,595 vs 10,642 on restaurants alone. **No geocoding leg in any of the six** — see the per-city table below. Owed: `check_personal_exposure.py` is load-bearing here, since the filter removes homes by proxy, not proof |

#### 🇫🇷 The five non-Paris cities, measured 2026-09-22

The list had been carrying *"the filter is national, so it carries to all six
cities"*. **That was an inference from a one-city sample** — and it is the
same shape as the claim that collapsed Spain from six cities to two
(*"two of the three probed had a register, which raises the prior sharply"*).
France's risk was genuinely lower, because one national register covers every
commune where Spain was bespoke per city, but lower risk is not a measurement.

Source: `economicref-france-sirene-v3` on `public.opendatasoft.com` —
**43,896,818 records**, the same uncapped v3 stock this file already cites.
**Paris was run as a control first**, because a per-city rate from a query
that cannot reproduce a known answer only looks like evidence.

| City | Active | Geolocated | **Rate** | **Storefront layer** |
|---|---|---|---|---|
| **Paris** *(control)* | 1,335,566 | 1,335,333 | **99.98%** | **50,156** ✅ |
| **Marseille** | 239,997 | 239,781 | 99.91% | **8,065** |
| **Lyon** | 190,995 | 190,941 | 99.97% | **7,354** |
| **Toulouse** | 153,407 | 153,179 | 99.85% | **4,833** |
| **Lille** | 77,416 | 77,190 | **99.71%** | **3,272** |
| **Rennes** | 64,973 | 64,906 | 99.90% | **2,089** |

**The control reproduces the recorded 50,156 exactly**, so the storefront
column is the project's own filter (NAF 47/56/96, employer, minus 47.91
online) and the six numbers are directly comparable.

**Verdict: the inference held.** No city falls below **99.71%** geolocated,
so **France genuinely has no geocoding leg in any of its six cities** and
keeps its cities-per-unit-of-work ranking. Two caveats that are now visible
only because the cities were measured separately:

- **The OSM composition validation is still Paris-only.** Geolocation is
  confirmed everywhere; that the employee filter selects the *right rows* was
  checked against OpenStreetMap in Paris alone. Cheap to repeat per city, and
  worth doing for the first non-Paris build rather than all five.
- **Rennes at 2,089 and Lille at 3,272 are thin.** Not disqualifying — Rennes
  has a two-line metro and the density question is what the map exists to
  show — but these are an order of magnitude below Paris, and whether a
  ~2,000-point city earns a page is a scope call, not a data problem.

## Tier 3 — a geocoding leg buys several cities (5 countries, 18 cities)

The investment tier. Each needs pipeline work written once, then cities are
cheap.

| Country | Cities | Business leg | Missing link |
|---|---|---|---|
| 🇯🇵 **Japan** ⏸ **DECIDED — BUILD, BUT LAST** | **10** | Food permits, CC BY, **one national schema** | **Verdict taken 2026-09-22: do the hard geocode, but not yet.** Build the easier geocoding countries first and let the shared machinery accumulate. Its own obstacles are unchanged — chōme/ban/gō, full-width numerals, `町字ID` 0% populated, and a **two-bucket ceiling** with no general retail |
| 🇹🇼 **Taiwan** | **4** | 商業登記, per-category assembly | A geocoding pass. **NLSC's geocoder is keyless**, so this is the cheapest Tier 3 entry |
| 🇧🇷 **Brazil** | **2** — São Paulo, Rio | CNPJ, no coordinates | Geocoding **past Toronto's scale**. Rio's rail is confirmed (20 relations, all named and coloured) |
| 🇳🇴 **Norway** | **1** — Oslo | 152,060 sub-units, `beliggenhetsadresse`, open API no key | A geocoding pass. Nothing else |
| 🇩🇰 **Denmark** | **1** — Copenhagen | CVR **P-enheder** with their own address + `industrycode` | A geocoding pass **and a free account** (`distribution.virk.dk` 401) |

**If you write one geocoder, write Taiwan's** — keyless, systematic addresses,
four cities. Japan's is a research project by comparison.

### Japan's cost is not fixed — it falls as the others are built

**Decided 2026-09-22: Japan gets built, and it goes last.** The reasoning is
not "postpone the hard thing", it is that **the hard thing gets cheaper while
you do the others**, so the same work costs less later.

Geocoding machinery this project already owns, from **Toronto**
(`pipeline/toronto/step3_geocode.py`) — the only Canadian city of six that
needed it, because its register carries no coordinate field and **Canada has no
national bulk geocoder**:

- a geocode step that sits between clean and map, with its own processed output
- the join-against-a-published-address-layer pattern, used instead of a geocoder
- **match-rate measurement by row type**, which is what caught the brief's
  71.4% being the wrong denominator: storefront rows matched **92.8%** while
  person-held licences dragged the all-rows figure to 73.1%
- the lesson that **the normalisation that matters is rarely street
  normalisation** — Toronto's real obstacle was units written into the address
  line (`"280 SPADINA AVE, #308"`), not abbreviations

Each Tier 3 country adds to that pool before Japan needs it:

| Build | What it contributes to Japan |
|---|---|
| **Taiwan** | A **keyless third-party geocoder** integration — request shaping, caching, rate limiting, failure handling. Japan's GSI geocoder is the same shape |
| **Norway / Denmark** | European street addresses at national scale, and the **free-account** pattern for Denmark's CVR |
| **Brazil** | **Scale** — CNPJ is ~72M rows, well past anything attempted so far |

By the time Japan is reached, what is left that is genuinely Japan-specific is
**block-address parsing** (chōme/ban/gō), **NFKC normalisation** of full-width
numerals, and the **join on `町字` by name** because the `町字ID` that exists to
make it machine-clean is 0% populated. That is a real problem, but it is a
smaller one than "write geocoding for this project".

**The risk to watch:** deferring is only cheaper if the machinery is actually
built *shared* rather than per-city. Toronto's step is city-specific today. If
Taiwan, Norway and Brazil each grow their own private copy, Japan inherits
nothing and the argument collapses. **Whoever builds the second geocoding city
should lift the common parts into `pipeline/` rather than copying Toronto's
file** — that is the decision that makes this ordering pay.

## Tier 4 — all four probed 2026-09-22; **Ireland passes** (4 countries, 4 cities)

| Country | City | State after the probe |
|---|---|---|
| 🇨🇿 **Czechia** ▲ | Prague | **Still the best probe left, and both its hosts had MOVED.** `rzp.cz` is 000 but **`www.rzp.cz` redirects to `rzp.gov.cz`**, which answers; `opendata.praha.eu` redirects to **`lkod.cz/catalog/praha`**. Two successor moves nobody had followed. **`data.gov.cz/sparql` answers SPARQL** — the Bulgarian technique applies directly. Next: enumerate for *provozovny* (premises) |
| 🇮🇪 **Ireland** ▲▲ **PASSES** | Dublin | **The probe was run on 2026-09-22 and Ireland passed — Dublin is now Band A.** `valoff.ie` was not down but **RETIRED**, and `api.valoff.ie` is **NXDOMAIN**; the API had moved twice, ending at **`opendata.tailte.ie`**, named on the *Valuation API Explorer* page and found by watching that JS page load its own link. **The deciding question is answered YES: the rateable register carries 16 use categories**, including `RETAIL (SHOPS)` and `HOSPITALITY`, plus a finer `Uses` string and `FloorUse` per floor. **Ireland is not the UK** — the NNDR's missing use category was never a property of rateable registers as such. Dublin City Council: **7,207 shops, 735 hospitality, 100% carrying Irish Transverse Mercator coordinates**, CC BY 4.0, no key |
| 🇨🇭 **Switzerland** ✗ | Zurich | **The second bucket is MEASURED ABSENT.** Control passes (`zzqqxxnonsense` → 0). Every commerce term returns noise or surveys: `detailhandel` **1** (a traffic count), `verkauf` 12 (tram ticket offices, apartment prices), `laden` 31 (a farm shop, population surveys), `gewerbe` 28 (zoning land, 3D roof models), `firmen` 16 — all **Firmenbefragung**, company *surveys* 2005–2025. Only `Gastwirtschaftsbetriebe` is real. **Zurich is a one-bucket food city — the Stockholm shape**, and it inherits Stockholm's open scope question rather than a data one |
| 🇸🇬 **Singapore** ⚠️ | Singapore | **The recorded description understated it: the search is not loose, it is INERT.** `zzqqxxnonsense` returns the **identical 10 datasets** as `licence`, `food establishment` and `business` — the query parameter is ignored entirely, and only the nonsense control tells that apart from a loose search. The catalogue is **4,628 datasets over 463 pages** and does page properly, so the route is **enumeration, not search** — the Montréal lesson, forced. Not yet done |

**Three of today's four probes hit the same thing: a host that had moved.**
`rzp.cz` → `rzp.gov.cz`, `opendata.praha.eu` → `lkod.cz`, `valoff.ie` →
`tailte.ie` — on top of Sevilla's `datosabiertos.sevilla.org` → an ArcGIS org.
**A 000 or a 404 is a question about the address, not an answer about the
data**, and this project has now spent retries on four corpses in one day.

## Tier 5 — 🇸🇪 Sweden: screening done, two owner decisions (1 country, 1–2 cities)

**New tier, 2026-09-22.** Sweden was in the old Tier 6 ("never actually
reached"). It is the only country that came out of that sweep alive, and it
sits here rather than higher because what it yields is **one city with one
bucket** — not because anything remains to probe.

| Country | City | Rail | State |
|---|---|---|---|
| 🇸🇪 **Sweden** ▲ | **Stockholm** | T-bana, ~100 stations — the strongest rail in the unbuilt set after Hong Kong | **Screening COMPLETE.** Public ArcGIS FeatureServer, **8,146 distinct food premises**, WGS84 points, trade names 100%, addresses 96.9%, daily refresh |
| 🇸🇪 Sweden | *Göteborg* | Trams | **Unprobed candidate.** Publishes **two** registers to Stockholm's one — `Livsmedelsverksamheter` (businesses, not inspections, so no dedupe) and `Restauranger med serveringstillstånd`. Better data, weaker map |

**Neither remaining question is a probe.** (1) **Scope** — food only; Sweden
has no general business licence and Stockholms stad's own catalogue returns 0
for `restaurang` and `företag`. (2) **Licence** — `dataportal.se` says
`Begränsad`, ArcGIS says `access: public`, `licenseInfo` is empty; ambiguous
in a way that matters, so the publisher gets asked.

**Cost per marginal city is poor** — one city, maybe two, and the second needs
its own probe. Ranked below Tier 4 for that reason, despite being further
along than any of Tier 4's four.

## Tier 6 — reached; one promoted out, two closed, two left (4 countries, 4 cities)

Reached 2026-09-22; what each host actually does is recorded in Band D-c
above. **Bulgaria has since become a data finding** — enumerated around its
403 via the EU portal — so the "no finding either way" caveat now covers only
Estonia and Croatia.

| Country | City | Host state |
|---|---|---|
| 🇪🇪 **Estonia** | Tallinn | API found (`andmed.eesti.ee/api/datasets/search`), contract unpinned — **400** on empty `search` and on `limit=1000`. **MTR** is the likely real route, unprobed |
| 🇭🇷 **Croatia** | Zagreb | `data.gov.hr` — **identical 1,291-byte SPA shell** at four paths incl. `data.json` |
| 🇭🇺 **Hungary** ✗ **CLOSED** | Budapest | **Firm negative on both routes.** Portal: `kozadat.hu` is a search tool over data inventories. Food authority: FELIR is CAPTCHA-gated and lookup-only; approved-establishment lists are PDFs of processing plants |
| 🇧🇬 **Bulgaria** ✗ **CLOSED** | Sofia | **Firm negative, reached around the 403.** `data.europa.eu`'s SPARQL endpoint harvests `data.egov.bg`; **11,635** Bulgarian datasets enumerated from outside. **141** municipal premises registers exist — none of them Sofia's **76**. Bulgaria's registers are all small towns; Sofia is its only metro city |

## CLOSED — the former Tier 5 (8 countries, 9 cities)

**Kept in full below as evidence, not as candidates.** This was "rail is
answered, the business leg is the hunt". The hunt finished on 2026-09-22:
**seven firm negatives, one blocked, one unreachable, no survivors.**

| | Country | Outcome |
|---|---|---|
| ⏸ | 🇭🇰 **Hong Kong** | **BLOCKED, not negative** — FEHD's register exists and is queryable, no bulk export found. **The one worth returning to** |
| ✗ | 🇨🇱 **Chile** | Coverage — 5 of ~33 comunas, Santiago absent |
| ✗ | 🇮🇳 **India** | 288,011 resources searched; nothing premises-level. GHMC and Kochi Municipal Corporation unprobed |
| ✗ | 🇲🇾 **Malaysia** | Sample, not register — 372 rows in KL |
| ✗ | 🇨🇴 **Colombia** | Hub credential-walled; crosstabs; 6.4M rows with no address column |
| ✗ | 🇵🇪 **Peru** | Coverage — 1 of Línea 1's 9 districts |
| ✗ | 🇮🇩 **Indonesia** | No activity field in a 53,827-row addressed register |
| — | 🇮🇱 **Israel** | Unreachable — IP-level refusal, browser shares the block |

The full evidence for each is below and in
`docs/global_country_shortlist.md`.

### The evidence — retained

| Country | City | Rail | Missing link |
|---|---|---|---|
| 🇭🇰 **Hong Kong** | Hong Kong | **126 relations**, 125 named | **The register EXISTS and is queryable — but no bulk export found.** See below |
| 🇨🇱 **Chile** ↓ **FAILS** | Santiago | **30 relations**, all named + coloured | **Coverage failure, measured.** Chile licenses per *comuna*; only **5 of ~33** Metro comunas publish patentes, and **the Santiago comuna itself is not on the portal at all**. See below |
| 🇲🇾 **Malaysia** ↓ **FAILS** | Kuala Lumpur | 14 relations, all named + coloured | **Sample, not register.** `lookup_premise` is a genuine premises table with **372 rows in KL** — it serves a price survey. See below |
| 🇮🇩 **Indonesia** ↓ **FAILS** | Jakarta | 9 operating of 11 | **No activity field.** The live OSS register has 53,827 rows and full addresses across exactly 9 columns, none of which says what a business sells. See below |
| 🇨🇴 **Colombia** ↓ **FAILS** | Medellín | 6 relations, **only 2 coloured** | **Three closed doors:** the city's Hub requires credentials, the chamber publishes comuna×CIIU crosstabs, and the 6.4M-row national register has **no address column**. See below |
| 🇮🇳 **India** ↓ | Hyderabad, Kochi | 6 and 2 relations | **National portal measured negative** — 288,011 resources searched, nothing premises-level. Municipal corporations (GHMC, Kochi) unprobed. See below |
| 🇵🇪 **Peru** ↓ **FAILS** | Lima | 4 relations, all named + coloured | **Coverage, not existence.** 78 licence datasets under ODC-BY, but licensing is per *distrito* and **1 of Línea 1's 9** publishes usable data. See below |
| 🇮🇱 **Israel** | Tel Aviv | 6 relations but **realistically 1** — Green and Purple are under construction | **Two problems:** the city portal returns **HTTP 472**, the documented IP-level refusal, and one operating line is thin for this project |

### Hong Kong, chased to the department — 2026-09-22

The furthest any Tier 5 city has been taken, and the verdict changed twice.

**1. `data.gov.hk` is a measured negative, by the strongest available check.**
Keyword search had returned statistics tables, which proves little. The
provider route is decisive: `organization_list` shows **129 organisations and
`hk-fehd` is one of them**, and `organization_show?id=hk-fehd` returns
**`package_count: 1`** — a single dataset, *"Products exempted from nutrition
labelling"*. So the licensed-premises register is **definitively not on the
open-data portal**. Searching by *provider* rather than *keyword* is the
generalisable move here: a keyword search cannot distinguish "absent" from
"named differently", and an org listing can.

**2. The register does exist, on FEHD's own site.**
`fehd.gov.hk/english/licensing/list_licensed_premises.html` →
**Lists of Licensed / Permitted Premises**, and it covers **two buckets**:

- **Food premises** — searchable by Shopsign/Address and by Licence/Permit Type
- **Non-food premises** — the same two routes. This is the **Personal services**
  bucket, which the earlier "food-only ceiling" claim said did not exist

The by-type form carries exactly the selectors a bulk extract needs:
`Licence Type` (General Restaurants · Light Refreshment · Marine · Factory
Canteens), `Special Endorsement` including **"All Licensed General
Restaurants"**, and **`District` including "- All districts -"** across all 19.

**3. But it is a QUERY INTERFACE, not a download.** No CSV, XLS, PDF or JSON
link exists anywhere on those pages — checked. Extraction would mean iterating
the form across licence types and districts and **scraping HTML**.

**So the honest verdict is neither "no data" nor "buildable".** It is: *a real
two-bucket premises register, publicly queryable, with no bulk route found.*
That is the **Seoul shape** — Seoul's food register also looked closed until the
page's own JS revealed a keyless POST — so the next step is to watch what the
form actually submits rather than to conclude from the absence of a download
link. Not yet done: the submit is JS-driven and did not navigate on click.

**This upgrades Hong Kong's prior considerably.** It has the largest rail
system in Tier 5 by a wide margin (126 relations, 125 named, 117 coloured) and
now a confirmed two-bucket register. What it lacks is a *route*, which is a
smaller problem than lacking data.

### Santiago — the Daegu failure, third occurrence — 2026-09-22

Provider enumeration settled this outright, and it took one pass. Chile issues
commercial licences (`patentes comerciales`) **per comuna**, so the question was
never "does Chile publish" but "how many of the ~33 comunas the Metro serves do".

`datos.gob.cl` lists **272 organisations, 67 of them municipalities**. Of those,
**15 are Metro-area comunas**, and asking each what it holds:

| | |
|---|---|
| Publish patentes | **5** — Independencia, La Florida, La Reina, Pedro Aguirre Cerda, Peñalolén |
| Present but publish none | Maipú, Puente Alto (245 datasets, no patentes), Recoleta, San Bernardo, Pudahuel, Huechuraba |
| Present with **zero** datasets | El Bosque, Ñuñoa, Quinta Normal, San Miguel |
| **Absent from the portal entirely** | **Santiago comuna itself** — the downtown — plus Providencia, Las Condes, Estación Central |

**5 of ~33, and the central comuna is missing.** Santiago's Metro converges on
the Santiago and Providencia comunas; a commercial-density map without them is
not a map of Santiago.

**This is the third time this exact shape has appeared** — Busan (4 of 16
districts), Daegu (4 of 9, with 중구 the downtown absent), now Santiago. The
generalisable rule is already in `add-country` and this confirms it: **where
licensing is devolved below the city, ask how many sub-units publish AND
whether the central one is among them, before believing a country count.** The
capital-aggregates case — Seoul, 25 of 25 — is the exception, not the rule.

### The Tier 5 remainder — where each one now stands, 2026-09-22

| Country | Method that worked | Result |
|---|---|---|
| 🇮🇳 **India** | `api.data.gov.in/lists` **enumerates — 288,011 resources** | **MEASURED NEGATIVE.** Searched properly: `trade licence` 209, `shops and establishment` 112,346, `commercial establishment` 316, **`Kochi` 1** (port exports). Every premises-shaped hit is either **one city that is not ours** (*Shops And Establishment Licence : **Ahmedabad***) or **aggregate** (*Vyapar **District wise ULB wise** Trade License Details*). Hyderabad's 192 hits are all census tables. **The national portal does not carry it**; GHMC and Kochi Municipal Corporation are the remaining route |
| 🇲🇾 **Malaysia** ↓ | Catalogue read in the browser — 292 datasets | **MEASURED NEGATIVE, and a new trap.** `lookup_premise` is a *genuine* premises table — `premise`, `address`, `premise_type`, `state`, `district`, **100% populated**, direct CSV, no auth. And it holds **3,916 rows nationally, 372 in Kuala Lumpur.** See below |
| 🇨🇴 **Colombia** (Medellín) ↓ | Browser, then provider enumeration on `www.datos.gov.co` | **MEASURED NEGATIVE, and a new trap.** The Hub is **private** — it renders *"Please sign in. This site requires credentials to access."*, which is why `data.json` 404'd and `api/search/v1` 401'd. The register-holder publishes **crosstabs**; the national register has **no address column at all**. See below |
| 🇵🇪 **Peru** (Lima) ↓ | Browser identified **DKAN**; `package_list` enumerated 4,687 datasets | **MEASURED NEGATIVE on coverage — the Daegu shape, 4th occurrence.** 78 licence datasets exist, keyless CSV, **ODC-BY**. But licensing is per *distrito*, and of Línea 1's **nine** districts exactly **one** publishes usable data. See below |
| 🇮🇩 **Indonesia** (Jakarta) ↓ | Browser read its own API off the network panel | **MEASURED NEGATIVE, and the other half of the new trap.** The live OSS register has **53,827 rows and full street addresses** — and **no activity field**, so there is nothing to filter storefronts on. See below |
| 🇮🇱 **Israel** (Tel Aviv) | — | **Not reachable by either method.** HTTP 472 and the host printed our own IP back — an IP-level refusal, so the browser shares the blocked address |

**Tier 5 is now closed: seven firm negatives, one unreachable, zero survivors.**

> **NEW TRAP — a real premises table can still be a SAMPLE, not a register.**
> Malaysia's `lookup_premise` passes every structural test this project
> applies: rows are individual premises, not aggregates; `premise`, `address`,
> `premise_type`, `state` and `district` are **100% populated**; it downloads
> as CSV with no account. It is nonetheless unusable, because it exists to
> support **PriceCatcher**, a price-monitoring programme — so it lists the
> premises whose prices are *surveyed*, and there are **372 in Kuala Lumpur**.
>
> For scale, this project's built and Band A cities carry 80,110 (Toronto,
> storefront rows), 148,814 (Madrid) and 197,276 (Seoul). **372 is three
> orders of magnitude short.**
>
> This is not the aggregate trap — the rows genuinely are premises. It is a
> **coverage** trap: the right shape at the wrong scale, and **only the row
> count reveals it**. Schema inspection passes it cleanly. The check that
> catches it is the one this project already runs for a different reason —
> *count the rows and compare against the city's plausible premises count*
> — which until now was about spotting truncation. Add sampling to what that
> check is for. Malaysia's composition also gives it away on a second look:
> 131 supermarkets and 69 mini-markets in a city of 1.8 million.

> **NEW TRAP, second half — a located register with nothing to classify, and
> a classified register with nothing to locate.** A premises table needs *two*
> columns to be a map: **where** and **what**. Both halves failed on the same
> day, in different countries, and each looked like a pass right up to the
> column list:
>
> | | Rows | Location | Activity |
> |---|---|---|---|
> | Colombia, RUES `nb3d-v3n7` | **6,369,877** | **nothing** — not even a city | CIIU codes |
> | Jakarta, OSS register | 53,827 | full street `ALAMAT` | **nothing** usable |
>
> Colombia's is the harder one to catch, because *6.4 million premises* reads
> as a decisive pass. The rows are the right entity — `ESTABLECIMIENTO DE
> COMERCIO`, the shop, expressly distinct from the company that owns it — and
> there is no address, no municipality, no city name. The finest unit in the
> file is `camara_comercio`, a chamber-of-commerce region spanning provinces.
> (It also carries owner `CEDULA DE CIUDADANIA` numbers, which this project
> would not publish in any case.)
>
> Jakarta's has exactly **9 columns**, checked against the portal's own
> component list rather than the rendered table: `periode_data`, `wilayah`,
> `kecamatan`, `kelurahan`, `nama_perusahaan`, `alamat`, `nib`,
> `uraian_jenis_perusahaan`, `skala_perusahaan`. The last two are **legal
> form** (KOPERASI, PT) and **size** (USAHA MIKRO) — neither says what the
> business sells, so `filter_to_storefront()` has nothing to act on.
>
> **Ask the two questions separately.** "Is it premises-level?" does not imply
> either one.

#### Colombia — three doors, all closed

1. **GeoMedellín's ArcGIS Hub is private.** The browser settled in one load
   what two HTTP codes had left ambiguous. No path exists to find, and this
   project does not create accounts.
2. **The register-holder publishes crosstabs.** The *Cámara de Comercio de
   Medellín para Antioquia* has nine distinct datasets on `datos.gov.co` and
   every commercial one is an *Estructura empresarial* table with the **16
   comunas as columns** and CIIU as rows — 2,349 rows of counts. Textbook
   aggregate, and CC BY-**SA** into the bargain.
3. **The national register has no location.** RUES, above.

No *Alcaldía de Medellín* business-licence dataset exists on the national
portal, which is where Ley 1712 requires publication.

#### Peru — excellent data, in one district out of nine

Peru's portal is the best-run of the group: **4,687 datasets**, keyless CSVs,
**ODC-BY** (attribution only, no share-alike). **78** carry *licencia* or
*funcionamiento*. It fails on coverage alone.

| Línea 1 district | State |
|---|---|
| **La Victoria** | **135,982 rows**, `Direccion` **100%** populated, `Giros` 54.3%, licence type and status. A genuine register — and the Gamarra garment district shows plainly in its composition |
| Cercado de Lima (Mun. Metropolitana) | 5,613 rows — **no address column, no trade name**. Administrative fields only |
| San Borja | Publishes a **metadata sheet**, not data: 20 rows × 3 columns |
| Surco · S.J. de Miraflores · V.M. del Triunfo · Villa El Salvador · El Agustino · San Juan de Lurigancho | **Nothing** |

**One of nine.** The southern four districts and the northern two — more than
half the line's stations — would be blank. Chorrillos does publish a good file
(9,767 rows, addresses) and Ate publishes a poor one (1,546 rows, no address),
but neither is on Línea 1.

Two notes for any future attempt: the CSVs are **double-quoted with `;;`
record terminators**, needing a two-stage parse; and `Nombre` carries
**sole traders' personal names**, so the project's personal-exposure check
would be load-bearing here rather than a formality.

**The method is doing its job, and the honest summary is that it mostly
closes things.** All eight Tier 5 countries are now settled: **seven firm
negatives** — Hong Kong's portal, Chile, India, Malaysia, Colombia, Peru,
Indonesia — **one upgrade** (Hong Kong's department, which turned out to have
*two* buckets but no bulk route), and **one unreachable** (Tel Aviv).
**No survivors.**

**A parameter-encoding note that cost a pass:** India's API ignores
`filters[title]=x` with literal brackets and honours `filters%5Btitle%5D=x`.
The unencoded form returns **HTTP 200 with the full unfiltered 288,011** and no
error — the same silent-ignore failure as `data.seoul.go.kr`, and the reason a
control term is not optional. The first search read as "no results" when it was
actually "no filter".

### The old Tier 6, reached — the evidence, 2026-09-22

**This is the evidence behind the new Tier 5 (Sweden) and Tier 6 (host
failures) above**, retained in full. It was "never actually reached"; the
browser sweep reached all six. One is a **partial pass** and was promoted; the
rest are host failures of varying finality.

| Country | City | State after the browser |
|---|---|---|
| 🇸🇪 **Sweden** ▲ | **Stockholm** | **PARTIAL PASS — best unbuilt result outside Band A.** A public ArcGIS FeatureServer with **8,146 distinct food premises**, real WGS84 coordinates, trade names, addresses and a usable activity field. **One bucket only** (food), and one licence conflict to resolve. See below |
| 🇪🇪 **Estonia** | Tallinn | API **found** — `andmed.eesti.ee/api/datasets/search?page&limit&search&type&sortBy&sortOrder&lang` — but it rejects an empty `search` and a large `limit` with **HTTP 400**, so the parameter contract is not pinned. `toitlustus` returns 16 datasets, all school-catering statistics. The real route is almost certainly **MTR** (Majandustegevuse register), which is unprobed. Lowest-value city in the tier: trams only, ~450k |
| 🇭🇷 **Croatia** | Zagreb | `data.gov.hr` answers 200 at **every** path with the **identical 1,291-byte** body — an SPA shell. Confirmed by four paths including `data.json`. **Still needs the browser** |
| 🇭🇺 **Hungary** | Budapest | **Misidentified until now.** `kozadat.hu` is not a data portal — it is a *search tool over public bodies' data inventories*. `budapest.hu` loads 425 KB with **two** data-ish links, one of them a privacy PDF. No catalogue found |
| 🇷🇴 **Romania** | Bucharest | `data.gov.ro` **times out** at the connection (21 s, both root and API); `portal.onrc.ro` does not resolve; `www.pmb.ro` is a 2,483-byte shell |
| 🇧🇬 **Bulgaria** | Sofia | **CORRECTION: the browser fails too.** `data.egov.bg` returns the same **403** in a real browser as to curl, so the earlier reading — that a stock Apache page implied a *client-signature* refusal worth retrying — was wrong. `data.sofia.bg` and `opendata.sofia.bg` **do not resolve**. `www.sofia.bg` and `portal.registryagency.bg` are live and unprobed |

### 🇪🇸 Spain is a TWO-city country — measured 2026-09-22

Spain had been carried as *"2 now, 6 total"* on the reasoning that it licenses
bespoke per city and **two of the three cities probed had a premises census**,
which *"raises the prior sharply"*. That prior is now measured, and it was
wrong: **Madrid and Barcelona are the exceptions, not the rule.**

| City | Portal | Enumerated | Verdict |
|---|---|---|---|
| **Valencia** | `opendata.vlci.valencia.es` (CKAN) | **290 packages** | ✗ The only commercial-adjacent names are container locations, noise stations, and *zones d'activitats* — **zoning polygons, not businesses** |
| **Málaga** | `datosabiertos.malaga.eu` (CKAN) | **1,377 packages** | ✗ `empresas-y-sectores` is explicitly businesses **in business parks**; `centros-comerciales` and `mercados` are `equipamientos` facility layers. CC **BY-SA** |
| **Bilbao** | own portal + `datos.gob.es` | 344 own / **600 federated** | ✗ Entire commercial holding is **"Barómetro del comercio minorista"** — retail-trade survey aggregates by employment stratum, sector, territory |
| **Sevilla** | ArcGIS org `hcmP7kr0Cx3AcTJk` | **1,260 items / 413 Feature Services** | ✗ **Measured negative** (was "unreachable" — the Hub's sign-in wall hid nothing; `sharing/rest` is public). `Locales` is **150 vacant municipally-owned units**, not businesses. Rail *is* solved: `METRO_Estacion` 21, `METRO_Linea` 20 |

**A method note worth carrying.** Bilbao's own portal holds 344 datasets across
35 pages and offers **no search** — its only form control is a sort order. Paging
it 35 times would have been the obvious move and the wrong one. Spain federates
every municipal portal into **`datos.gob.es`**, which speaks DCAT over a
documented API, so one publisher enumeration (`/catalog/dataset/publisher/<id>`)
covers any Spanish city at once. That is the primitive to reach for next time a
Spanish city comes up.

**And a caution about the national catalogue**: searching it by *title* returns
almost entirely **INE** (publisher `EA0042823`) aggregate statistical tables —
*Locales por provincia y condición jurídica*, hotel occupancy, and so on. Those
look like premises data and are not. Enumerate by **publisher**, not by title.

### 🇸🇪 Stockholm — a real register, found four hops deep

The route is the argument for navigating rather than guessing; no step of it
was predictable from the outside:

`dataportal.se` → organisation **Stockholms stad** (291 datasets, 101 open,
190 *skyddade*) → the **one** commercial hit, *Tillsynsverksamheter -
Livsmedel* → its page links the miljöförvaltning's ArcGIS Hub → the Hub item
id resolves through `arcgis.com/sharing/rest` to a **public** FeatureServer.

| Measured | |
|---|---|
| Rows | **289,742** — but a row is an **inspection**, carrying `TillsynsDatum` and `Anmarkning`. "Nyko Kitchen, Nybrogatan 61" repeats across dozens |
| **Distinct premises** (`ObjektId`) | **8,146** |
| Geometry | `esriGeometryPoint`, real WGS84 — `(18.0804, 59.3388)` — plus SWEREF99 northings/eastings |
| `Adress` | 280,760 of 289,742 rows non-empty (**96.9%**) |
| `AnlaggningsNamn` | **100%** — trade names |
| `VerksamhetsTyp` | 22 values, **29.5%** of rows non-null: *Restaurang-, catering- och barverksamhet* 65,858 · *Detaljhandel* 11,103 · *Partihandel* 2,810 |
| `AnlaggningsTyp` | **0% — entirely `'None'`.** The field exists and is empty |
| Update | daily/weekly, from Ecos 2 |

**The row-count discipline cuts both ways.** Malaysia's count was too *small*
to be a register; Stockholm's is too *large*. Both are answered by asking what
a row **is** before trusting the number — and here the answer is good news,
because 8,146 premises with coordinates is a real city leg.

**The activity field is recoverable but not free.** `VerksamhetsTyp` is null on
70.5% of rows because it describes the *inspection*, not the premises — so it
has to be lifted to premises level by taking any non-null value per `ObjektId`
during dedupe. That is ordinary work, not a blocker, but it is work, and it is
the difference between this and Jakarta, where no activity field existed at all.

**Two open questions before Stockholm could be built:**

1. **One bucket.** This is food only. Stockholms stad has **291 datasets and
   exactly one** commercial register — `restaurang` and `företag` both return
   **0** within its catalogue. Sweden has no general business licence, so
   retail and personal services have no municipal source to find. This is the
   Hong Kong shape, improved: a real bulk route exists, but a Stockholm page
   would be a **food-density map**, not the three-bucket map the built cities
   carry. That is a scope call, not a data problem, and it belongs to the
   owner. `multi-source-city` is the relevant process if a second source is
   ever found.
2. **A licence conflict that must not be resolved in this project's favour.**
   The `dataportal.se` metadata record says `Åtkomsträttigheter: **Begränsad**`
   (restricted); the ArcGIS item says `access: **public**` and serves the data
   without credentials. `licenseInfo` is **empty**; `accessInformation` reads
   only *"Stockholms stad, miljöförvaltningen"*. Per `read-licence` step 8 this
   is **ambiguous in a way that matters** and needs the publisher asked — the
   fact that it fetches is not a finding that it is licensed.

   > **⚠️ SUPERSEDED 2026-09-22 — the pointers were followed, and the conflict
   > mostly dissolves.** The paragraph above jumped to step 8 ("ask the
   > publisher") while steps 2, 3 and 5 were still undone: it treated a
   > **harvester's** metadata field as the last word and never opened the
   > documents that record names. What reading found:
   >
   > | Source | Says | Weight |
   > |---|---|---|
   > | `dataportal.se` (the **harvester**) | `accessRights: RESTRICTED`; `license:` the category **`otherlicense`**, not a licence | weakest — a third-party catalogue |
   > | **Miljöförvaltningen's own Hub DCAT feed** — `open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json`, **109 datasets** | **`accessLevel: public` on all 109**; `license` **CC0 on 8**, blank on 101 incl. this one | **strongest — the publisher asserting** |
   > | ArcGIS item `8447f7af…` | `access: public`; **no `licenseInfo` field at all** | publisher |
   > | FeatureServer root | `copyrightText: "Stockholms stad, miljöförvaltningen"`; `licenseInfo` empty | publisher |
   > | `dataportalen.stockholm.se` deep link | redirects to **`catalog.signin`** — walled, and this project does not create accounts | unread |
   >
   > **`read-licence` step 5 decides the contradiction: the publisher outranks
   > the catalogue**, and the publisher says *public* on all 109 datasets.
   > That the publisher **declares CC0 on 8 of them** matters too — it shows
   > the licence field is one they use and chose not to fill here, so the
   > blank is a genuine silence rather than a missing capability. Those 8 are
   > a single thematic cluster (ArtArken, biotopes, substrates, landscape),
   > which reads as one team licensing its own outputs.
   >
   > **One tempting over-reach, declined.** Stockholm's traffic office states
   > at `openstreetgs.stockholm.se`: *"Datainnehåll i dessa tjänster får
   > vidareutnyttjas fritt och tillhandahållas **'Licensfritt'** om inget
   > annat anges"* — freely reusable, licence-free unless otherwise stated.
   > **That is Trafikkontoret's statement about *dessa tjänster*, its own
   > services — not miljöförvaltningen's**, and extending one department's
   > terms to another's data is exactly the move this skill exists to stop.
   > It is evidence about the city's posture, not a licence for this dataset.
   >
   > **Position now: SILENT, not restricted** — the Miami-Dade shape, where
   > the authoritative pages were read and impose no reuse position. Still
   > genuinely unread: the **walled GeoNetwork record** (try the Internet
   > Archive, as Barcelona's and Sevilla's were read) and any city-wide open
   > data policy page. **A letter is no longer the next step, and never was
   > the first one.**

**A second Swedish city worth noting:** `dataportal.se` shows **Göteborgs
stad** publishing *both* `Livsmedelsverksamheter` ("alla aktiva
livsmedelsverksamheter", JSON + CSV) and `Restauranger med serveringstillstånd`
(CSV) — i.e. **two** food-adjacent registers where Stockholm has one, and
`Livsmedelsverksamheter` is a register of *businesses* rather than of
inspections, so it needs no dedupe. Gothenburg's rail is trams rather than a
metro, so it is a weaker map for a stronger dataset. Unprobed.

## Countries ruled out

*▼ **2026-09-24 — eight countries left this list** with the discard audit:
Germany, Austria, the Netherlands, Greece, Portugal, Poland, Latvia and
Slovakia each rested on one national-level method, and their cities are in
the open gap (the Netherlands' Amsterdam now in Band A). A country is not ruled
out by its national portal's first page.*

🇬🇧 **UK** *(NNDR is a tax register with no category)* ·
🇦🇺 **Australia**, 🇳🇿 **New Zealand** *(licensing is not municipal)* ·
🇧🇪 **Belgium** *(bulk access paid)* · 🇦🇪 **Dubai** *(no agency feed)*

*🇪🇬 **Egypt left this list on 2026-09-23** with Cairo: one probe of CAPMAS is
not a country ruling. See the open screening gap.*

## The order, as decided

> **Current position, 2026-09-23.** Mexico, Spain, Ireland and Italy's Milan
> are built; France is **complete at five** (Paris, Marseille, Toulouse, Lille, Rennes).
> **The seventeen Band A cities are build-ready now**, nine of them Brazilian
> and three Taiwanese. **Brazil was
> picked to go first in the geocoding band and turned out to need no geocoder**
> (IBGE's census address file carries every establishment's coordinate), so
> **Taiwan was next in that band — and its first probe found the same thing**:
> every city publishes a keyless door-plate coordinate file, and Taipei's tax
> register joins to it at 92.5%. **Japan stays last**, and is the one country
> left whose address file has not been looked for. The numbered order below is the 2026-09-22 plan, kept because its
> reasoning (lift shared geocoding machinery into `pipeline/`, let Japan
> inherit it) still holds even though the country it named first changed.

1. ✅ **Mexico** — **DONE, 2026-09-22.** Two cities from one source, as
   predicted. It was also the project's first country outside anglophone North
   America and its first OSM-sourced rail leg, so it proved two things the
   screen had only asserted.
2. ▶ **Spain — NEXT, and it is exactly two cities.** Madrid and Barcelona are
   ready now, each with a build brief whose claims re-run green. The "other
   three likely rather than speculative" line was wrong: Valencia, Bilbao and
   Málaga were probed on 2026-09-22 and are measured negatives, and Sevilla is
   unreachable. **Plan Spain as two cities, not six.**
3. **Korea** and **Italy** — one city each, nothing to discover, both with
   named build work rather than open questions.
4. **Taiwan** — the first geocoding build, chosen because it is the cheapest:
   keyless geocoder, systematic addresses, four cities. **Lift the shared parts
   into `pipeline/` here**, not later.
5. **Norway**, **Denmark**, **Brazil** — the rest of Tier 3, in rising
   difficulty.
6. ⏸ **Japan** — **last, by decision.** Ten cities, and by then the geocoding
   machinery is built.

**France no longer sits outside this order awaiting a decision** — it was
made on 2026-09-22 and, after one reversal, went **in favour**. The employee
filter yields a defensible storefront layer, validated against OpenStreetMap,
and SIRENE arrives geolocated. That makes France **six cities on one national
integration with no geocoding leg** — on cities-per-unit-of-work, the
strongest unbuilt country in this screen. It belongs in the order, and where
it goes is the owner's call.

Tier 4's four probes (**Czechia** strongest) are cheap enough to run alongside
any of the above rather than competing with them.

**Sweden sits outside the numbered order too**, for the opposite reason to
France: its work is not architecture but a **scope call** — whether a
one-bucket, food-only city page belongs in this project at all. Settle that and
Stockholm is close to ready; leave it unsettled and there is nothing to build.
**Hong Kong is the one closed country worth reopening**, since its register is
known to exist and only the bulk route is missing.

---

## Two rules this list is maintained by

**A row reading "not reached", "unprobed" or a regional pattern is not a
discard.** Eleven cities were once sitting in the discard list on exactly those
grounds, against evidence in the same document. Every discard row above names
the finding that disqualified it, so a contradiction is visible rather than
inferable.

**A country ruling needs two cities measured, not one asserted onto a region.**
Germany no longer qualifies (2026-09-24): Hamburg's row rested on one search
term and is back in the open gap, leaving Berlin alone. Italy does not fail
merely because Naples did — Milan is built and Rome is in Band A.

**A discard states its kind, its methods and whether the city's own host was
asked, as columns — and `python scripts/check_discard_evidence.py` decides
whether that is enough.** Run it whenever the discard table changes. A
failing row moves to the open gap; the rule is not relaxed to keep it.

## Before building any city on this list

**Check `docs/commuter_rail_list.md`** — which cities have commuter rail, the
two built maps that draw it (Dublin's DART, Copenhagen's S-tog), and the
candidates whose build must decide it (Japan, Seoul, Hong Kong, São Paulo).

- `docs/build_briefs/<city>.md` if one exists, then
  `python scripts/brief_check.py <city>` — a brief caches Step 0's mistakes as
  confidently as its findings.
- **A city outside every existing region needs one added.** `app/cities.py`
  raises on a city whose region is not a leaf of `REGION_ORDER`. **Europe is
  already ONE region**, so a new European country (Czechia, Denmark, Norway,
  Sweden, Switzerland, Romania) does not add one; **Seoul, Hong Kong, Brazil,
  Taiwan, Japan and Singapore each would**, and `check_macro_labels.py` is the
  measurement for whether a region frames its cities. *(This bullet said
  `REGION_ORDER` was still `["United States", "Canada"]` until 2026-09-23 — it
  now holds seven entries.)*
- `add-country` first for any country this project has never built in — every
  candidate country except France.
