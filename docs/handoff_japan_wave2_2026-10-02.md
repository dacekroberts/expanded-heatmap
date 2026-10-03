# Handoff: Japan wave 2, fourteen cities (2026-10-02)

For the build session that builds the second wave of Japanese cities, scoped
and briefed on 2026-10-02. Written by staging; the owner asked for "the kit,
worktree and prompt for wave 2" the same day.

**✅ RELEASED by the owner, 2026-10-02**, to ONE build session that runs
agents. It works in `.claude/worktrees/japan-wave2` on branch
`japan-wave2-build`. There, `data/` and `.venv-lean` are junctions to the
main checkout's. The branch has no upstream, so a plain `git push` can never
reach master.

**One other build session runs at the same time:** the four extensions
(`extensions-build`, `docs/handoff_extensions_2026-10-02.md`). It touches
Brazil's, Los Angeles's and Vancouver's code, not Japan's. Both sessions edit
`app/cities.py`, `docs/data_sources.md` and `docs/excluded_categories.md` in
their own sections, and both land at review time.

**Delete this file** once all fourteen have landed.

---

## The fourteen: every call settled

Every brief's checks pass; staging re-ran all of them on 2026-10-02. No 🚨 is
open. Each brief opens with a "✅ Owner's calls" block. Read each city's brief
in full before touching it. Wakayama was discarded, and Chiba is in Band R
(not built).

| Page | City | Band | Shape | Mode | Brief |
|---|---|---|---|---|---|
| 176 | Kawasaki | A | The city's monthly lists, all three buckets; two private lines drawn cut | metro | `docs/build_briefs/kawasaki.md` |
| 177 | Yokosuka | A | BODIK lists, all three buckets | metro | `docs/build_briefs/yokosuka.md` |
| 178 | Himeji | A | City CKAN, all three buckets | metro | `docs/build_briefs/himeji.md` |
| 179 | Nishinomiya | A | City portal, all three; laundry 62% disclosed; three lines drawn cut | metro | `docs/build_briefs/nishinomiya.md` |
| 180 | Takamatsu | A | City lists, all three buckets | metro | `docs/build_briefs/takamatsu.md` |
| 181 | Toyota | A | BODIK lists (food 75% of in force, stalls out); two lines drawn cut | metro | `docs/build_briefs/toyota.md` |
| 182 | Yokkaichi | A | Five BODIK lists | metro | `docs/build_briefs/yokkaichi.md` |
| 183 | Ōtsu | A | The city's monthly food list plus BODIK registers | light_rail | `docs/build_briefs/otsu.md` |
| 184 | Nara | A | MHLW plus the pre-2021 list; registers; thin rail, built anyway | metro | `docs/build_briefs/nara.md` |
| 185 | Hamamatsu | B | Personal services only (Hakodate's shape) | metro | `docs/build_briefs/hamamatsu.md` |
| 186 | Higashiōsaka | B | Food only: the BODIK full list plus monthly permits; Chūō Line drawn cut | metro | `docs/build_briefs/higashiosaka.md` |
| 187 | Kurume | B | Food only, MHLW (Okayama's shape) | metro | `docs/build_briefs/kurume.md` |
| 188 | Sasebo | B | Food only, MHLW plus the old-law list | metro | `docs/build_briefs/sasebo.md` |
| 189 | Shimonoseki | B | Food only, MHLW; the San'in Line drawn to 小串, 14 stations ringed | metro | `docs/build_briefs/shimonoseki.md` |

**Standing calls that apply to all fourteen:** the `japan-city` skill's
owner's calls, the minor label tier, and the mode rule. A city is `metro`
where JR is its largest network or a subway is drawn.

---

## How this session runs: one lead, three agents (as wave 1)

**Phase 0, the lead alone: setup.**
1. Confirm the worktree and branch, `git fetch`, and merge `origin/master`.
2. Register the session in `docs/session_roles.md`'s table.
3. Run `python scripts/brief_check.py <slug>` for all fourteen. They make no
   Overpass calls.

**Phase 1, the lead alone: every shared-code item in ONE pass.** Wave 1's
pass landed the ward-less flag, N02-25, the MHLW default-point guard and
many spellings. Each wave-2 brief lists only what is new. Collect them all:
- **`OPERATOR_COLS`:**
  - 営業者氏名（法人のみ）, 営業者氏名・法人名称, 氏名;
  - 開設者申請者名, 開設者代表者名, 営業者申請者名, 営業者代表者名;
  - 申請者_氏名, 申請者代表者名, 開設者氏名（法人）, 開設者代表者.
- **`ADDR_COLS`:** 施設_所在地, 営業施設住所, 営業所_住所１, 理容所所在地,
  美容所所在地, クリーニング所在地.
- **`NAME_COLS`:** 施設_名称, 営業施設屋号, 理容所名称, 美容所名称,
  クリーニング名称.
- **`TYPE_COLS`:** 営業種目 (Kawasaki); 区分 (Yokkaichi's no-shop pick-up
  rows); 詳細業種 read as the 業態 form (Yokosuka).
- **`japan_eigyo`:**
  - Kawasaki's 飲食店（…）spelling, with carve-outs for 給食施設, まあじゃん
    and 短期;
  - そうざい店 to Retail;
  - 複合型そうざい製造業;
  - Nara's old-law restaurant sub-types (軽飲食, 一般食堂, 居酒屋 and
    others: 455 restaurants) and 簡易菓子製造業.
- **Readers and dates:**
  - `wareki_date` reads `R 8. 5.31` (Sasebo: 0 of 607 today);
  - Nishinomiya's two-sheet workbooks are already covered by
    `xlsx_rows`.
- **Address rules (`norm_town`):**
  - a leading 大字 is ignored (Yokkaichi, Shimonoseki);
  - 字甲/乙/丙 is read as 甲/乙/丙, and Himeji's 甲/乙/丙 地番 rule;
  - a 丁目 missing from MLIT falls back to the 大字 centroid (Toyota's
    浄水町, 52 rows);
  - Nara's ケ/ヶ and missing-町 town fixes.
- **Not premises:** an address of only "<city>内" (Kurume: 1,022 rows on
  one point, which the default-point guard misses).
- **Fetches:**
  - month-renamed files read from the page (Kawasaki, Ōtsu);
  - Higashiōsaka's full-list-plus-months rebuild through
    `config.source_rows`;
  - `OWN_POINT_FALLBACK` for Hamamatsu's chōme-tier rows;
  - a Tokyo-Datum guard, used only if Higashiōsaka's own points ever are.
- **`japan.CITIES` entries for all fourteen** (ward-less where the brief
  says so, on N02-25), and Hamamatsu's 2024 ward codes (22138–22140).

**Then prove it:**
- `python scripts/screen_japan_join.py minato` must reproduce its control.
- The drift checks of the 20 built Japanese cities must stay clean
  (`--jobs 2`).
- Add each new city's `CITIES` entry to `screen_japan_join.py` and confirm
  its brief's placement tiers.
- Commit. Every agent starts from this commit.

**Phase 2, the lead alone: the pilot, Kawasaki.** It exercises the most new
paths: a monthly renamed file, the new type column and spelling, cut private
lines, and `GROUP_JOIN` for 武蔵小杉. Build it end to end, read its whole
output, and commit.

**Phase 3: three agents in parallel, in this worktree (no `isolation`),**
grouped by shape:
- **City lists, three buckets:** Yokosuka, Himeji, Nishinomiya, Takamatsu,
  Toyota.
- **Mixed and MHLW:** Yokkaichi, Ōtsu, Nara, Kurume, Sasebo.
- **One-bucket and rebuilt:** Hamamatsu, Higashiōsaka, Shimonoseki.

The lead runs each city's OpenStreetMap `name:en` fetch itself, one at a
time. An agent owns only `pipeline/<slug>/`, `data/<slug>/`,
`outputs/<slug>/` and its claimed page. It never queries Overpass, commits
or edits a shared file; a shared-code need goes back to the lead. It returns
its shared-file entries as text:
- the `cities.py` entry, with `label_tier: "minor"`, the mode above and the
  Japan region;
- the privacy-verdict row;
- the provenance record;
- the What Is Excluded section;
- the licence rows and notice;
- the inconsistency rows;
- the master-list line;
- its drafts entries.

It stops and reports on a failing brief claim, a placement share under its
brief's figure, a census ratio outside the expected band without its
brief's explanation, or a shared-code need.

**Phase 4, the lead: integrate in page order.** For each city, apply its
entries, run the gate order, and commit it on its own. Then:
1. The **label pass:** each city goes into Japan West or Japan East by the
   split the first batch set (`app/cities.py`). Measure it with
   `check_macro_labels.py`, PROBLEMS 0 at 375, 768 and 1200, re-placing a
   label where the measurement says.
2. One drift check (`--jobs 2`).
3. Merge master, run `check_all.py`, and push `japan-wave2-build`.

**Not to master** until the owner's review time.

## Visuals and analytics: what a build owes them (staging, 2026-10-02)

The visuals session is drafting presentation pieces on `visual-handoff`, not
yet on master: city cards, a title card, explainers. They are generated from
published files, so a city feeds them with nothing extra, as long as the
build keeps three things true:
1. **Native-script names stay in config.** The cards read each city's own
   name from its config: `MUNICIPALITY` (Japan), `BOUNDARY_NAME` (Korea),
   `CITY_NAME_ZH` (Taiwan). Keep the field the city's country uses; do not
   drop it as unused.
2. **Ring shares and bucket counts come from the gates.** Every card checks
   its pins against `app/ring_shares.json` and its layer counts against the
   bucket counts, so gate 9's ring shares must be recorded for the city.
3. **Every notice is registered where the page lists it.** Card credits are
   built from the per-page notice plan (`city_notices()`, on Cleanup's
   prose-pass branch, landing at review time). Register each new notice the
   same way as the city's other notices, so the card picks it up once both
   land.

**No analysis on any page.** AI-driven deep analysis is now permitted, but
it is private to the owner and always carries an AI-generated
acknowledgement. The rule is on `visual-handoff`, coming to `CLAUDE.md`. It
never goes on a city page, `outputs/` or any deployed file, so a build writes
none.

## Numbers

- **Pages:** 176–189, in the table above.
- **Notices:** **115–128**, pre-assigned by staging. The extensions session
  holds 129–136. Record the range in `docs/session_roles.md`'s numbers
  sentence; check D of `check_provenance.py` reads it.

## Gate order (Band B's)

1. personal exposure, the Japan name pass, and a row in
   `docs/privacy_verdicts.md`;
2. provenance;
3. scope disclosure, written to `docs/city_page_format.md`;
4. the inconsistency rows and `cities.py` fields;
5. the master list (each city leaves Band A or B for Built);
6. macro facts and the macro label;
7. the decisions entry;
8. commit;
9. the drift check, its baseline and ring shares;
10. merge master, `check_all.py`, and push at 0 behind.

Also at build, as the skill says: the Economic Census join control (Yokosuka,
Ōtsu and Higashiōsaka run high, and their briefs explain why) and OSM
`name:en` for every station.

## Session rules

- Decisions go to `docs/decisions_drafts/japan-wave2.md`.
- Overpass: one query in flight per session, one per city; wait 60 s after a
  504 or 429. Only the lead queries.
- `data/` is one shared junction. Never re-run another city's step from this
  branch. A failing `check_macro_facts` or `check_ring_shares` on a city
  that is not yours goes to Cleanup.
- Personal data:
  - Select columns before printing anything from a register.
  - Never print, store or quote a person's name, ID, phone or address.
  - Brief agents slipped twice on 2026-10-02 (console only).
- No backslash or backtick in a Bash command. Write a script file.
- Downloads named in a brief or the skill are pre-permitted. Anything else
  goes to the owner.
- A failing brief claim goes to the staging session.
