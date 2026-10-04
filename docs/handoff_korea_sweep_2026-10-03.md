# Handoff: Daejeon, Gwangju and Gimhae (2026-10-03)

For the build session that builds the three Korean cities the coverage sweep
returned to the list. Written by staging; the owner set three build sessions
on 2026-10-03 ("one korean, one belgium, one for the other cities").

**✅ RELEASED by the owner, 2026-10-03** ("if korean and other cities are
ready, give me new worktrees and prompts with handoff files"), to ONE build
session. It works in `.claude/worktrees/korea-sweep` on branch `korea-sweep-build`, cut
from origin/master by staging. There, `data/` and `.venv-lean` are
junctions to the main checkout's. The branch has no upstream, so a plain
`git push` can never reach master. Everything lands at the owner's review
time.

**Two other build sessions may run beside this one:** the other cities
(Mendoza, Tacoma, Liverpool (Regional); `docs/handoff_new_cities_2026-10-03.md`)
and Belgium (its kit follows the KBO measurement). All three edit
`app/cities.py`, `docs/data_sources.md` and `docs/excluded_categories.md` in
their own sections.

**Delete this file** once all three cities have landed.

---

## The three: every call settled

| City | Page | Business leg | Rail | Brief |
|---|---|---|---|---|
| **Daejeon** | 190 | SEMAS, 대전광역시, 시군구코드 30110-30230: **50,939 storefronts** (23,402 / 20,100 / 7,437), 100% placed | METRO: Line 1, 22 stations, every 10 minutes at midday | `docs/build_briefs/daejeon.md` |
| **Gwangju** | 191 | SEMAS, the merged member 전남광주통합특별시, codes **12210, 12240, 12270, 12300, 12330**: **47,214** (20,701 / 18,706 / 7,807), 100% placed | METRO: Line 1, 20 stations, every 10 minutes off-peak; most trains turn short of 녹동 | `docs/build_briefs/gwangju.md` |
| **Gimhae** | 192 | SEMAS, 경상남도, code 48250: **17,879** (8,558 / 6,662 / 2,659), 100% placed | LIGHT RAIL: Busan-Gimhae LRT, 12 stations in Gimhae (9 in Busan, out of scope), every 5-6 minutes all day | `docs/build_briefs/gimhae.md` |

**Owner calls already made (2026-10-03):** all three from Band R to A on
SEMAS's keyless file; **Gimhae is its own page**, not a Busan regional map.
The licence is SEMAS's, already recorded (제한 없음, notice **68**); no new
licence read.

## How this session runs: one lead, sequential

All three use the same modules as Incheon and the Gyeonggi satellites
(`pipeline/countries/korea_sbiz.py`, `pipeline/taxonomies/korea_sbiz.py`,
the cached ZIP `data/korea/raw/sbiz_15083033.zip`, edition 2026-06-30).

**Phase 0, setup.** Confirm the worktree and branch, `git fetch`, merge
`origin/master`, register the session in `docs/session_roles.md`'s table,
and run `python scripts/brief_check.py daejeon gwangju gimhae` (13 checks,
no Overpass).

**Phase 1, the one shared-code change, first and alone.** `korea_sbiz`
filters on a 시군구명 prefix and never reads 시군구코드. Gwangju's districts
share names with districts in other cities (동구, 서구, 남구, 북구), and
경기도 광주시 is another city. Add a code filter to the shared reader once,
keep the name filter for the built cities, and **prove it with
`python pipeline/drift_check.py` over the ten built SEMAS cities: zero
drift** before any new city is scaffolded. A counts-only pass (staging,
2026-10-03) found the code and name filters pick identical rows in all
three new cities today.

**Phase 2, the cities in order:** Daejeon (the simplest: its member is the
whole city), then Gwangju (the merged member, the codes, and its OSM
boundary, which may have changed with the 2026 merger: check by name and
area), then Gimhae (light rail, its own page).

**Per city:** `scaffold_city.py` with the reserved page number, step 1 from
OSM (`osm-rail` skill; one Overpass query in flight, one per city), step 2
through the shared reader, step 3, then the gates below.

## Visuals and analytics: what a build owes them

1. **Native-script names stay in config:** Korea's field is `BOUNDARY_NAME`.
2. **Ring shares and bucket counts come from the gates**, so gate 9's ring
   shares must be recorded (`scripts/check_ring_shares.py --write`).
3. **Every notice is registered where the page lists it** (`city_notices()`
   in `app/components.py`), so a card picks it up.
4. **Record each notice's card face or caption, and any open terms question,
   in the drafts file** (`docs/session_roles.md`, "Downstream sessions").
   **One is open and known:** the Visuals registry
   (`visuals/data/restrictions.json`, 2026-10-02) keeps every SEMAS city off
   the cards while "whether SEMAS's permission reaches social posts" is open.
   These three inherit that hold; say so in the drafts.

**No analysis on any page.** AI-driven deep analysis is private to the owner
and never goes on a page, `outputs/` or a deployed file.

## Numbers

- **Pages: 190 (Daejeon), 191 (Gwangju), 192 (Gimhae)**, claimed in
  `docs/session_roles.md`'s numbers sentence.
- **Notices: none new.** SEMAS's notice 68 covers all three, as it covers
  the ten built SEMAS cities. If a build finds a source that needs a notice,
  it asks staging for a number.

## Gate order (Band A's, per city)

1. personal exposure (the name-withholding step kept) and a row in
   `docs/privacy_verdicts.md`;
2. provenance;
3. scope disclosure, written to `docs/city_page_format.md`;
4. the inconsistency rows and `cities.py` fields;
5. the master list (each city leaves Band A for Built);
6. macro facts and the macro label;
7. the decisions entry;
8. commit;
9. the drift check, its baseline and ring shares;
10. merge master, `check_all.py`, and push at 0 behind (to the build branch).

## Session rules

- Decisions go to `docs/decisions_drafts/korea-sweep.md`.
- Overpass: one query in flight per session, one per city; wait 60 s after a
  504 or 429.
- Memory: every heavy job through `scripts/heavy_job.py run` with a real
  label and `--session korea-sweep`; the owner gives Cleanup and the map-dot
  session priority.
- `data/` is one shared junction. Never re-run another city's step from this
  branch.
- Personal data: select columns before printing anything; never print,
  store or quote a person's name, ID, phone or address.
- No backslash or backtick in a Bash command; write a script file.
- Downloads named in a brief or skill are pre-permitted; anything else goes
  to the owner.
- One browser-using agent at a time: the built-in browser pane is shared.
- A failing brief claim goes to the staging session.
