# Handoff: the Japan batch, twelve cities (2026-10-02)

For the build session that builds the twelve Japanese cities screened on
2026-10-01 and briefed on 2026-10-02. Written by staging; the owner asked for
this kit, its worktree and its prompt the same day.

**✅ RELEASED by the owner, 2026-10-02**, to ONE build session that runs
agents. It works in `.claude/worktrees/japan-batch` on branch
`japan-batch-build`. There, `data/` and `.venv-lean` are junctions to the
main checkout's. The branch has no upstream, so a plain `git push` can never
reach master.

**The UK six build session runs at the same time** (`uk-six-build`,
`docs/handoff_uk_six_2026-10-01.md`). The two batches share almost no code,
but both edit `app/cities.py`'s region list and both claim page and notice
numbers. See "Numbers and the other session" below.

**Delete this file** once all twelve have landed.

---

## The twelve: every call settled

Every brief's checks pass (122 of 122 on 2026-10-02). No 🚨 item is open.
Read each city's brief in full before touching it.

| City | Band | Page | Map mode | Brief |
|---|---|---|---|---|
| Matsuyama | A | Three buckets: the city's lists plus MHLW (own points; notifications as partial retail) | tram | `docs/build_briefs/matsuyama.md` |
| Toyama | A | Three buckets, the city's CKAN | tram | `docs/build_briefs/toyama.md` |
| Kumamoto | A | Three buckets; food retail only from MHLW's slice | tram | `docs/build_briefs/kumamoto.md` |
| Fukui | A | Three buckets, **CC BY-SA 4.0** (`LICENSE` line at build) | tram | `docs/build_briefs/fukui.md` |
| Nagasaki | A | The 2023 BODIK snapshot plus MHLW's current filings (Tokyo's precedent) | tram | `docs/build_briefs/nagasaki.md` |
| Utsunomiya | A | Fukuoka's two-source shape: MHLW plus the old-law list; personal lists | light_rail | `docs/build_briefs/utsunomiya.md` |
| Kitakyushu | A | MHLW plus the old-law list; barber and beauty, no laundry (disclosed) | metro | `docs/build_briefs/kitakyushu.md` |
| Sakai | B | Food only; Midōsuji drawn cut (3 stations) | metro | `docs/build_briefs/sakai.md` |
| Hakodate | B | Personal services only (Yokohama's precedent) | tram | `docs/build_briefs/hakodate.md` |
| Kagoshima | B | Food only: MHLW plus the old-law list | tram | `docs/build_briefs/kagoshima.md` |
| Okayama | B | Food only, MHLW alone (no name rule: Hiroshima's MHLW bullet) | metro | `docs/build_briefs/okayama.md` |
| Kōchi | B | Personal services only (1,415 premises) | tram | `docs/build_briefs/kochi.md` |

**The owner's calls of 2026-10-02**, all recorded in the briefs and in
`docs/decisions_drafts/staging.md`:
- **The minor label tier and a Japan sub-region**, below.
- **Map mode:** Dublin's precedent, so JR drawn beside a tram does not make
  a city `metro`, "unless there is substantial JR, JR reads as metro". JR
  counts as substantial when it is the city's largest network by stations
  inside the city line.
- **Name rule:** where a list names only companies (Toyama, Fukui) or no
  operator at all (Okayama, Nagasaki's MHLW rows), the page carries
  Hiroshima's MHLW-style bullet.

---

## How this session runs: one lead, three agents (staging, 2026-10-02)

**Why one session.** All twelve go through `pipeline/countries/japan_register.py`,
`japan_eigyo` and `japan_step1` / `japan_step2`. Every brief adds column
spellings or an address rule there. Each change must be proven on the
Minato control and the eight built Japanese cities. Two sessions would edit
the same module and fight over it.

**Phase 0: the lead alone, setup.**
1. Confirm the worktree and branch, `git fetch`, merge `origin/master`.
2. Register the session in `docs/session_roles.md`'s table, and claim its
   notice numbers there.
3. Run `python scripts/brief_check.py <slug>` for all twelve. They make no
   Overpass calls.

**Phase 1: the lead alone, shared code in ONE pass.** Collect every
"shared code at build" item from the twelve briefs and make them together:
- **`OPERATOR_COLS`:** 申請者個人名, 開設者氏名, 代表者氏名, and the other
  spellings each brief lists.
- **`ADDR_COLS`:**
  - 所在地＿連結表記 (full-width low line), 施設所在地１, 所在地, 施設住所;
  - 営業所所在地1 (Kumamoto's personal lists read 0 rows without it);
  - 営業所, 施設住所名称.
- **`NAME_COLS`:** 施設名, 営業所名称, 屋号名称, 営業所の名称.
- **The readers:**
  - Toyama's merged headers;
  - Fukui's twelve monthly sheets;
  - a ward-less flag for cities without wards.
- **Address rules:**
  - Sakai's `N丁` without 目 (33.7% to 95.8% at block);
  - Kōchi's 高埇 / 高そね variant.
- **Taxonomy and rail data:**
  - `japan_eigyo`'s short old-law spellings 飲食店 / 喫茶店 (Fukui's 93
    rows);
  - the **N02-25** rail edition where a brief needs it (Kagoshima's 仙巌園,
    Fukui's Hapi-line).

**Then prove it:**
- `python scripts/screen_japan_join.py minato` must reproduce 98.0 / 0.2 /
  1.8.
- The drift checks for the eight built Japanese cities must stay clean
  (`--jobs 2`).
- Add each new city's `CITIES` entry to `screen_japan_join.py` and confirm
  its brief's placement tiers.
- Commit. **Every agent starts from this commit.**

**Phase 2: the lead alone, the pilot, Matsuyama.** Build it end to end,
including its page and gates. It exercises the most paths:
- city lists;
- MHLW as a second source, with `OWN_POINT_FALLBACK` and `SUPERSEDES`;
- notifications as partial retail;
- personal services;
- a tram network.

Read its whole output, then commit.

**Phase 3: three agents in parallel, in this worktree (no `isolation`),**
grouped by shape:
- **MHLW-led:** Utsunomiya, Kitakyushu, Okayama, Kagoshima.
- **City lists with personal services:** Toyama, Fukui, Kumamoto, Nagasaki.
- **One-bucket pages:** Sakai, Hakodate, Kōchi.

The lead first runs each city's OpenStreetMap `name:en` fetch itself, one at
a time, under one-query-per-session.

**An agent owns only its cities' files:**
- `pipeline/<slug>/`;
- `data/<slug>/`;
- `outputs/<slug>/`;
- its claimed `app/pages/` files.

**An agent never queries Overpass, never commits, and never edits a shared
file.** That includes `japan_register` and `japan_eigyo`; a shared-code
need goes back to the lead. It returns its shared-file entries as text:
- the `cities.py` entry, with `label_tier: "minor"` and the mode above;
- the privacy-verdict row;
- the provenance record;
- the What Is Excluded section;
- the licence rows and the notice;
- the inconsistency rows;
- the master-list line;
- drafts entries and prose proposals.

**An agent stops and reports** on:
- a failing brief claim;
- a placement share under its brief's figure;
- a census-control ratio outside the built cities' range without an
  explanation (Matsuyama's 2.78 is flagged);
- any shared-code need.

**Phase 4: the lead, integration in table order.** For each city in turn,
apply its entries, run the gate order below, and commit it on its own. Then:
1. The **Japan sub-region and label pass**, below, done once.
2. One drift check (`--jobs 2`).
3. Merge master, run `check_all.py`, and push `japan-batch-build`.

**Not to master** until the owner's review time.

## The Japan sub-region and the minor label tier (owner, 2026-10-02)

"For this new batch of japanese cities … implemented like france and
czechia where the smallest cities lose their macro-view pills to reduce
clutter". The recipe is the `japan-city` skill's standing calls, on the
France and Czechia mechanism (DECISIONS.md, 2026-09-30, the label tiers'
two slices):
- **A Japan region of its own.** One region or a split, decided by
  `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.
- **Every Japanese city moves into it:** the eight built (Tokyo, Yokohama,
  Osaka, Kyoto, Kobe, Sapporo, Fukuoka, Hiroshima) and the twelve, as Prague
  moved with Czechia.
- **The twelve carry `label_tier: "minor"`.** The eight stay eligible. A
  minor city keeps its dot and tooltip everywhere; its pill shows only in
  its own region.
- **`REGION_LABELS_ALSO["East Asia"]` gains the Japan region,** beside the
  Seoul Capital Area, so East Asia still names the eight. East Asia's frame
  will re-centre; measure, then re-place a label if needed.
- **It lands with the twelve, at review time.** The region move changes
  `app/`.

## Numbers and the other session

- **Page numbers are pre-assigned to avoid a collision:** UK six **156–161**,
  Japan batch **162–173**, in table order (Matsuyama 162 … Kōchi 173).
  Recorded in `docs/session_roles.md`.
- **Notice numbers:** claim them in `docs/session_roles.md` before writing
  one, and re-read the table first. The UK session claims there too.
- **`app/cities.py`'s `REGION_ORDER`:**
  - The UK session adds a UK region; this one adds Japan.
  - Each adds only its own lines.
  - Both branches land at review time, and the merge is a two-line
    conflict at most.

## Page text

Page text follows `docs/city_page_format.md` and the `japan-city` skill's
"The page and the reference docs" section. `scaffold_city.py`'s template is
the new format: run it with the city's `--mode` from the table and
`--region` set to the Japan region once it exists.
- Template prose is pre-permitted (CLAUDE.md, 2026-09-30).
- A sentence specific to one city is a proposal, flagged in the drafts
  file, and does not stop the build.
- US spelling throughout. Japanese names stay as published.

## Gate order (Band B's, `docs/band_b_retrospective.md`)

1. personal exposure, the Japan name pass, and a row in
   `docs/privacy_verdicts.md`;
2. provenance;
3. scope disclosure, the section written to the format;
4. the inconsistency rows and `cities.py` fields;
5. the master list;
6. macro facts and the macro label (the label after the region pass);
7. the decisions entry;
8. commit;
9. the drift check, its baseline and ring shares;
10. merge master, `check_all.py`, and push at 0 behind.

Also at build, per the skill: the Economic Census join control
(`scripts/japan_census_control.py`; the e-Stat download is approved) and OSM
`name:en` for every station.

## Session rules (CLAUDE.md)

- **Decisions go to `docs/decisions_drafts/japan-batch.md`,** never to
  `DECISIONS.md`.
- **Overpass:** one query in flight per session, one per city, and wait
  60 s after a 504 or 429. **Only the lead queries.**
- **`data/` is one shared junction.** Never re-run another city's step from
  this branch. A failing `check_macro_facts` or `check_ring_shares` on a city
  that is not yours goes to Cleanup.
- **Memory:** these are light jobs, apart from drift checks (`--jobs 2`, one
  per machine). Use `heavy_job.py` for anything with an unknown peak.
- **Personal data:**
  - Select columns before printing anything from a register.
  - Never print, store or quote a person's name.
  - Two brief agents slipped on 2026-10-02 (console only); do not repeat
    it.
- **No backslash or backtick in a Bash command.** Write a script file.
- **Downloads** named in a brief or the skill are pre-permitted. Anything
  else goes to the owner.
- **A failing brief claim** goes to the staging session to correct.
