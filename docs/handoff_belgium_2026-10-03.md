# Handoff: Belgium, six pages (2026-10-03)

For the build session that builds Belgium's first six pages, found by the
coverage sweep and screened, licence-read and banded on the owner's calls of
2026-10-03. Written by staging; the owner set three build sessions the same
day ("one korean, one belgium, one for the other cities").

**✅ RELEASED by the owner, 2026-10-03** ("create the belgium kit as soon
as ready"), to ONE build session. It works in `.claude/worktrees/belgium`
on branch `belgium-build`, cut from origin/master by staging. There,
`data/` and `.venv-lean` are junctions to the main checkout's. The branch
has no upstream, so a plain `git push` can never reach master. Everything
lands at the owner's review time. **One call is open at release:** how
pages use the "TEC" name (below, Notices); ask staging before writing
Charleroi's or Liège's page text.

**Two other build sessions run beside this one:** Korea
(`docs/handoff_korea_sweep_2026-10-03.md`) and the other cities
(`docs/handoff_new_cities_2026-10-03.md`). All three edit `app/cities.py`,
`docs/data_sources.md` and `docs/excluded_categories.md` in their own
sections. Belgium is a new country: it needs its own
`docs/data_sources/belgium.md` and a country row wherever the built
countries are listed (the `add-country` skill's checklist).

**Delete this file** once all six pages have landed.

## SAVEPOINT 2026-10-04, second (all six built; four owner calls open)

Branch `belgium-build`, merged with origin/master at 888bdbd9; nothing pushed.
Decisions in `docs/decisions_drafts/belgium.md`, newest first.

- **All six pages built and committed**: Brussels (196), Antwerp (197),
  Ghent (198), Charleroi (199), Liège (200), Brussels (Regional) (201):
  steps 1-3, maps, pages, city entries, notices 144-152, source rows,
  What Is Excluded sections, privacy rows, map_inconsistencies rows (tables
  A-D), ring shares, macro facts, the master list (Built 164, Europe 29,
  Bands A 5 and B 1), README and rendered surfaces regenerated (only the
  six added; nothing else moved).
- **Applied from the six approved calls**: the cafeteria exception; the
  Brussels, Charleroi and Liège privacy rows (`publish`); the Belgium macro
  view (Czechia's mechanism); the KBO control re-based on `brussels_hub` at
  a 1-point tolerance (owner, after the diagnostic confirmed only Retail's
  half); step 2 for Brussels (Regional) then ran green (13,680 storefronts).
- **`check_all.py`**: every check passes except `check_macro_labels.py`
  (9 problems, below). Not yet run: `drift_check.py` (heavy; one job) and
  the merge with origin/master.

**Open for the owner (recommendation, then the tradeoff):**

1. **Brussels (Regional)'s privacy verdict** (row `pending`): 1 pin has a
   person-like company name at an address the exposure check reads as a
   residential unit. Recommended: withhold that one name by key (the pin
   shows its type), not read by eye. Alternative: publish all, resting on
   every name being a legal person's.
2. **The Brussels and Brussels (Regional) dots sit 2.4 px apart** in the
   Belgium view (both near central Brussels), so their pills overlap at
   every width. Recommended: move Brussels (Regional)'s dot to a point
   inside its 18 communes clear of the City (Ixelles or Etterbeek), then
   place the two labels on opposite sides. Alternative: list the pair in
   `KNOWN_STACKED` for the UI pass, as Kobe and Osaka are.
3. **Rotterdam's Europe label covers Liège's (unlabelled) dot.** No
   offset clears it: ten tried, each trades Liège for Den Haag, Amsterdam,
   London or the UK dots. Recommended: give Den Haag and Rotterdam's pair
   one more placement pass together (taste, so the owner's); alternative:
   accept Liège's dot under the pill until the UI pass.
4. **Antwerp's left bank**: the approved Overpass query (tram route
   relations 3, 9 and 15, `fetch_sources.py --left-bank-trams`) found no
   such relations on overpass-api.de (an empty answer, twice) and timed out
   on kumi.systems; the one retry after the minute did the same (drafts).
   A broader query (every tram route in the box) is a new query: the owner's call; else De Lijn's notice,
   which the build cannot republish.

**Still to do after those**: the drift check; merge origin/master and
`check_all.py`; `docs/project_context.md`'s current state; the downstream
note to Visuals and Analytics after the push (every notice caption-only;
open terms questions: hub.brussels's "Google Maps" credit, KBO's declared
purpose).

---

## The five

| City | Page | Band | Business leg | Rail | Brief |
|---|---|---|---|---|---|
| **Brussels** (the City, the commune) | 196 | A | hub.brussels's shop inventory on opendata.brussels.be: **6,880 rows, all placed**, 2025-10-17; food 1,908, retail 2,459, personal 508; 1,068 vacant out. CC BY 4.0 | `metro`: **25 metro and premetro stations** kept by name (3 are tram-served in the premetro), trams drawn and thinned; **STIB's GTFS** | `docs/build_briefs/brussels.md` |
| **Antwerp** | 197 | B | FAVV's operator list on Flanders' VKBO points: **3,100 of 3,231 food premises placed (95.9%)**; 1,764 food shops as a Retail partial | `tram` (premetro trams in tunnels): De Lijn trams 1, 2, 4, 6, 7, 8, 10, 11, 12, 24, A3, A9; **163 stations (148 inside)**, median 279 m, halved rings, **no thinning**; lines 3, 5, 9, 15 absent from the current feed (closed-for-works rule); **scope includes Borsbeek** | `docs/build_briefs/antwerp.md` |
| **Ghent** | 198 | B | As Antwerp: **1,810 of 1,905 (95.0%)**; 932 food shops | `tram`: De Lijn T1, T2, T4 (no T3); **51 stations (50 inside)**, median 272 m, halved rings | `docs/build_briefs/ghent.md` |
| **Charleroi** | 199 | B | Wallonia's LoGIC 2024 survey (the downloaded GeoPackage only): retail 980, horeca 450; horeca **53%** of FAVV's count (commercial perimeters only), disclosed | `light_rail`: TEC M2, M3, M4 (M1 absent from the feed); **48 stations (38 inside)**, median 385 m; **M2 drawn to Anderlues** (10 outside listed); the project's own palette (one feed color for three lines) | `docs/build_briefs/charleroi.md` |
| **Liège** | 200 | B | LoGIC: retail 1,477, horeca 868 (**68%**), disclosed | `tram`: TEC T1, Coronmeuse - Standard, **23 stops**, every 6 minutes, median 351 m; the two-parent stop merged | `docs/build_briefs/liege.md` |
| **Brussels (Regional)** (the other 18 communes) | 201 | B | KBO Open Data (the owner's account), **companies' units only**, joined to BeST-Address Brussels (**96.8% placed at a number**), four filter rules: **Retail 9,124, Food 5,209**; personal services off; the page states its different method and the measured agreement with hub.brussels (about four in five pins) | `metro`: STIB beyond the City, trams thinned as the City's | `docs/build_briefs/brussels_regional.md` (4 of 4 checks) |

## Every owner call already made (2026-10-03)

- Belgium off "Countries ruled out"; the five banded as above.
- **Brussels:** hub.brussels kept (KBO only a cross-check); drop the
  `google_maps` and `google_street_view` columns, never link a pin to
  Google, name the publisher's listed contributors (hub.brussels and "Google
  Maps") in the credit; no City logo or BXL mark. **STIB's GTFS is the rail
  source**, and the owner approved accepting the Belgian Mobility Company
  portal's terms (a consent box) at the build's first fetch; a re-fetch after
  the terms change goes back to the owner. The page is named **"Brussels"**;
  its text says it covers the City of Brussels, the commune.
- **Antwerp and Ghent stay B** (food, food shops as a partial); KBO's layers
  are not added. Caterers out (the category rules). **FAVV is credited
  through its home page only** (a deep link asks for the webmaster's say),
  and its "prior approval for downloadable documents" clause is read as the
  Dutch text limits it, to brochures. VKBO's prescribed Dutch credit line
  plus the extract date.
- **Charleroi and Liège stay B with the gap disclosed**; measure LoGIC's
  coverage inside the station rings first, and bring the figure to the owner
  if it is far below the city-wide share.
- **Each source keeps its own sole-trader rule:** FAVV's list carries no
  names and its points come from VKBO, so the FAVV route places every food
  premises; KBO (not used by these five) would take companies only.
- **Brussels (Regional) from C to B** (owner): Retail and Food full, Personal
  services off, companies only (KBO's licence), a different method from the
  City's said on the page. **Build it last**, after Brussels.
- **The twelve build calls (owner, "i say yes to all")**: the De Lijn and
  TEC feeds already fetched are ratified (the same portal terms as STIB's);
  rail from De Lijn's and TEC's feeds, subject to their licence reads
  (`docs/decisions_drafts/staging.md`; OSM if either is restrictive); the
  modes in the table; no thinning in Antwerp; platform names merged where the
  feed has no parent station, and Liège's two-parent stop merged;
  "complementary retail" (FAVV PL29 with AC95) out; Charleroi's M2 drawn to
  Anderlues; Charleroi in the project's palette; hotels inside LoGIC's
  HoReCa disclosed, not split; the shop sign (`ENSEIGNE`) as the dot's name
  in Charleroi and Liège, a sign read as a person's own name withheld;
  Antwerp with Borsbeek.

## Notices (the reads' verdicts are in `docs/decisions_drafts/staging.md`)

| Notice | Source | Display |
|---|---|---|
| **144** | hub.brussels inventory (City of Brussels portal), CC BY 4.0 | Credit, licence link, modification statement, the publisher's listed contributors |
| **145** | FAVV/AFSCA operator list, CC BY 4.0 | Credit with the extract date, the home-page link, licence link, modification statement, no endorsement |
| **146** | VKBO (Digitaal Vlaanderen), Modellicentie gratis hergebruik v1.0 | The prescribed Dutch line "publieke KBO gegevens, verrijkt met adressen uit het Vlaamse Adressenregister." plus the extract date |
| **147** | SPW LoGIC 2024, CC BY 4.0 | The SPW citation verbatim, the working catalogue link beside its 404 URI, a modification statement |
| **148** | STIB-MIVB GTFS (Belgian Mobility Company portal), CC BY 4.0 | "Source: STIB-MIVB – Open Data – [feed date]", the modified-data line, the portal |
| **149** | De Lijn GTFS (Belgian Mobility Company portal); read 2026-10-04: permitted with conditions | "Source: De Lijn – Open Data – [feed date]", the modified-data line, the portal, the CC BY 4.0 title and link; no delijn.be link |
| **150** | TEC GTFS (Belgian Mobility Company portal); read 2026-10-04: permitted with conditions (CC BY 4.0; TEC's national-access-point entry says CC0, and complying with CC BY satisfies both) | "Source: LETEC – Open Data – [date of dataset update]" (the update date, not the fetch date), the modified-data line, the CC BY 4.0 title and link, the portal; no TEC logo. **Open for the owner:** TEC's website terms claim the "TEC" name; staging recommends crediting "LETEC" (the name the portal and the feed's agency use) and labelling lines by their public names (M2, M3, M4, T1) without "TEC" in legends or prose |
| **151** | KBO/BCE Open Data (FPS Economy), Brussels (Regional) only | Source and the update date, not presented as a guarantee; companies only |
| **152** | BeST-Address Brussels (FPS BOSA), Brussels (Regional) only | CC BY 4.0, BOSA and the Brussels address register, a statement that business addresses were matched to the points |

## How this session runs: one lead, agents for self-contained legs

**Phase 0, setup.** Confirm the worktree and branch, `git fetch`, merge
`origin/master`, register the session in `docs/session_roles.md`'s table,
and run `python scripts/brief_check.py brussels antwerp ghent charleroi
liege brussels_regional` (no Overpass).

**Phase 1, the country.** `docs/data_sources/belgium.md` and the five
sources' licence rows (and any GTFS's); a shared Belgian module only where
two cities truly share a leg: `pipeline/countries/belgium_favv.py` for the
FAVV-on-VKBO join (Antwerp and Ghent) and a LoGIC reader (Charleroi and
Liège). Cached: `data/belgium/raw/` (the FAVV CSV, the LoGIC GeoPackage,
each with a meta JSON).

**Phase 2, the cities:** Brussels first (the A, a new taxonomy on
hub.brussels's types with the `premises-taxonomy` skill: art galleries to
Retail by precedent; 160 rows typed in two buckets need a rule), then
Antwerp and Ghent together, then Charleroi and Liège together, then
Brussels (Regional) last (KBO on BeST-Address, the four filter rules).

**Build traps the briefs record:**
- VKBO's OGC API ignores field selection and returns names: use the WFS
  with field selection (number and point only); drop (0,0) placeholders.
- FAVV's "_EN" file has French descriptions.
- LoGIC: never the MapServer (SPW's services terms forbid altering served
  data); the GeoPackage only.
- BOSA's files move from Lambert 72 to Lambert 2008 on 2026-10-11 (not
  used by these five, recorded for Brussels (Regional)).
- De Lijn's feed has no `parent_station`: merge platform names ("perron N",
  "Metro Perron X") into one station (owner). Antwerp's Borsbeek: VKBO files
  1,701 rows under Antwerp's code and 175 under the old one; FAVV in its
  postcode adds 27 food premises and 24 food shops, not yet joined.
- **delijn.be's website terms are private use only** (and a link to its
  pages asks for the webmaster's say): no delijn.be link in a notice and no
  delijn.be content (logo, network maps, line-page text) on a page. Its line
  pages may be consulted privately for gate 3; nothing from them is
  republished.
- TEC's `feed_info.txt` dates carry a leading space, which crashes
  `brief_check.py`'s `gtfs_feed_window`; read `calendar_dates` instead.
- The De Lijn and TEC feeds are cached in `data/_brief_check/raw/` (307 MB,
  fetched 2026-10-03, ratified by the owner); a re-fetch after the portal's
  terms change goes back to the owner.
- KBO (Brussels (Regional)): never read `denomination.csv` or `contact.csv`
  except through a step that withholds every natural person; 36% of
  establishments list five or more unordered MAIN codes ("any MAIN code in a
  bucket", food over retail over personal); download at least yearly or the
  contract lapses.

## Visuals and analytics: what a build owes them

1. **Native-language names stay in config** where the country uses a field
   for them (Belgium is bilingual: keep the FR and NL names the sources give).
2. **Ring shares and bucket counts come from the gates**: record gate 9's
   ring shares (`scripts/check_ring_shares.py --write`).
3. **Every notice is registered where the page lists it** (`city_notices()`
   in `app/components.py`).
4. **Record each notice's card face or caption, and any open terms question,
   in the drafts file** (`docs/session_roles.md`, "Downstream sessions").
   Known: what hub.brussels's "Google Maps" credit covers is the publisher's
   unstated point (the read found it is the portal's link columns).

**No analysis on any page.**

## Numbers

- **Pages: 196 (Brussels), 197 (Antwerp), 198 (Ghent), 199 (Charleroi),
  200 (Liège), 201 (Brussels (Regional))**, claimed in `docs/session_roles.md`'s
  numbers sentence.
- **Notices: 144–152**, claimed there too.

## Gate order (Band A's and B's, per city)

1. personal exposure and a row in `docs/privacy_verdicts.md`;
2. provenance;
3. scope disclosure, written to `docs/city_page_format.md`;
4. the inconsistency rows and `cities.py` fields;
5. the master list (each city leaves its band for Built);
6. macro facts and the macro label (a new country: a new region dot may be
   needed; run `check_macro_labels.py` at 375, 768 and 1200);
7. the decisions entry;
8. commit;
9. the drift check, its baseline and ring shares;
10. merge master, `check_all.py`, and push at 0 behind (to the build branch).

## Session rules

- Decisions go to `docs/decisions_drafts/belgium.md`.
- Overpass: one query in flight per session, one per city; wait 60 s after a
  504 or 429. Only the lead queries.
- Memory: every heavy job through `scripts/heavy_job.py run` with a real
  label and `--session belgium`; the owner gives Cleanup and the map-dot
  session priority.
- `data/` is one shared junction. Never re-run another city's step from this
  branch.
- Personal data: FAVV and VKBO name sole traders' enterprises; select
  columns before printing anything; never print, store or quote a person's
  name, ID, phone or address.
- No backslash or backtick in a Bash command; write a script file.
- Downloads named in a brief or skill are pre-permitted; anything else goes
  to the owner. Accepting a portal's terms is the owner's act (STIB's is
  approved for the first fetch).
- One browser-using agent at a time: the built-in browser pane is shared.
- A failing brief claim goes to the staging session.
