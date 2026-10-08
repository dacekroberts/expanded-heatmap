# Build plan for the A and B cities (owner, 2026-10-07)

The owner lifted the build pause on 2026-10-07 and approved the four changes
below and the usage check-ins. This file holds the order, the rules every build
session follows, and one prompt per session. Staging keeps it current; a
session's prompt is pasted as its first message.

**Scope.** 64 briefed cities (A 32, B 32) and 6 briefed extensions. Phases 0
and 1 landed on 2026-10-07. Phase 2 adds Cluj-Napoca to Kansai-2 (owner, call
222) and Kurashiki, moved to B on its year-end PDF, to Regional-2 (call 226).
Naha (Band C) is not built: it waits on one measurement (Kansai-2 takes it if
BODIK answers). Band D is empty. Seoul, Busan and Daegu (Regional) wait for SEMAS's social-post scope
(call 71).

**What was measured** (staging, 2026-10-06):
- A Japanese city's steps 2-3 take 0.2-1.2 min and 0.16-0.63 GB.
- The Japan drift check (`--jobs 3`) takes 2.1-3.4 min at 5.3 GB.
- The last two Japan build sessions did 12 cities in 2.7 h and 14 in 3.1 h of active time. Their wall time was 4.6 h and 9.3 h, mostly waiting on owner approvals.
- About 0.1M output tokens per city.
- 39 of the 58 Japanese briefs flag shared-code changes, to the same few modules.

The machine (Ryzen 7 5700X, 16 threads, 32 GB) is not the bottleneck. Approvals, shared-module collisions, merge conflicts and the usage pool are.

## The owner's four changes and the usage cap (2026-10-07)

1. **Precedent decides.** A question already answered by the city's brief, a skill, `docs/category_rules.md` or a numbered owner call is applied, and the drafts file names the precedent. Only a question with no precedent stops for the owner.
2. **Unattended mode.**
   - Branches only. Downloads named in the brief are pre-approved; anything else is a parked call.
   - At a new judgment call, park that city: leave it committed and clean, write the call into the drafts file under "Parked calls", with a recommendation and its tradeoff, then move to the next city.
   - Parked calls reach the owner as one numbered list per wave, through Staging. **From phase 2 Staging numbers them S1, S2, S3 and on** (owner, 2026-10-08); a plain number ("call 226") is the old series, which ended at 230. A session's drafts file names its parked calls by city and letter; Staging assigns the S number when it relays them.
3. **One review time per phase.** Landings, re-renders and deploy-verify are batched: after phase 0, after the first Japan trio, and after the second. Only the owner calls review time. App reboots happen once per landing.
4. **Build sessions never edit `docs/city_master_list.md`.** Staging moves a wave's cities to Built in one pass after each landing, and republishes the private pages. A build lands in one push at the end of its batch, after review time; `app/cities.py` conflicts are resolved keep-both.

**Usage check-ins for phase 2 (owner, 2026-10-08):** "let's do a 30% and 60% check in to be light". In the week from the reset of 2026-10-11, every session stops at **30% and 60% weekly usage**, and only there; phase 2 is the last build wave. (Phases 0 and 1 stopped at every multiple of ten.)
- Check `get_usage` between cities.
- At a crossing: finish the current step, commit clean, and stop. Tell the owner in your own chat and send one line to Staging Session. Continue only on the owner's word.
- All sessions share one pool, so one crossing stops every session.
- The 30% and 60% stops are weekly figures, not the 5-hour window ("for weekly not 5hr"); the 5-hour window keeps only its 90% ceiling.

## Order and session plan

At most three build sessions at once (owner, 2026-10-04).

| Phase | Session (worktree) | Cities, in build order | Skills |
|---|---|---|---|
| 0 | **Japan foundation** (`japan-foundation`) | No city: every shared-code rule the briefs name, landed once | japan-city, address-join, cjk-text, pipeline-drift-check |
| 0 | **Abroad** (`abroad-batch`) | Gimpo, Siheung (A); Geneva (A); Thessaloniki, Gelsenkirchen, Bremen (B; Bremen's licence read first); then Anyang, Mexico City, Copenhagen (Regional) | korea-city, tram-city, add-city, osm-rail, regional-extension |
| 1 | **East-1** (`japan-east-1`) | A: Higashiyamato, Nishitōkyō, Tama, Higashimurayama, Ageo (Regional), Sōka, Tokorozawa, Kasukabe. B: Fuchū (Tokyo), Chōfu, Tachikawa, Hino | japan-city |
| 1 | **Kansai-1** (`japan-kansai-1`) | A: Toyonaka, Hirakata, Suita, Itami, Kakogawa, Amagasaki, Uji | japan-city |
| 1 | **Regional-1** (`japan-regional-1`) | A: Maebashi, Fukuyama, Ichinomiya, Tsu, Fukushima, Iwaki, Akita, Ōita, Gifu, Mito, Morioka | japan-city |
| 2 | **East-2** (`japan-east-2`) | A: Koshigaya, Sagamihara, Fujisawa. B: Kawaguchi, Funabashi, Matsudo, Ichikawa, Urayasu, Sakura, Yachiyo, Ichihara | japan-city |
| 2 | **Kansai-2** (`japan-kansai-2`) | B: Ibaraki (Osaka), Minoh, Moriguchi, Kadoma, Neyagawa, Yao, Takatsuki; then Cluj-Napoca (B, food only; owner, call 222); then Naha's measurement if BODIK answers | japan-city; for Cluj-Napoca add-city, osm-rail, address-join, then write the romania-city skill |
| 2 | **Regional-2** (`japan-regional-2`) | B: Shizuoka, Kanazawa, Okazaki, Aomori, Matsue, Fuji, Matsumoto, Tottori, Yamagata, Kure, Kurashiki (owner, call 226) | japan-city |

- **The foundation landed on 2026-10-07 (7ab440f9).** The five one-city address fixes landed the same day (521d28fc): Gifu's bracketed 字, Morioka's 地割, Mito's 宮町/泉町 and Matsumoto's 湯の原 as WAVE5_RULES switches, Matsue's 八雲村 as a config key (its brief says how). A session started before 521d28fc merges origin/master before Gifu, Mito and Morioka.
- **Phase 1 starts when the foundation lands on master.** Until Abroad finishes, only two Japan sessions run at once.
- **Each phase 2 session starts** from master after the phase 1 session in the same group has handed off.
- **BODIK** rate-limits (Naha was blocked after about 100 rapid calls), so every session keeps its calls at least 20 s apart, one city at a time, and never uses datastore_search_sql. brief_check's metadata calls run anywhere; data pulls come from cached Step 0 files where they exist, and a needed fetch is one file at a time. The Kansai sessions, which pull most from BODIK, run one after the other (clarified 2026-10-07, after Regional-1's brief checks: the earlier "Kansai only" wording was broader than its purpose).
- **Licence reads** a brief leaves pending are Staging's: it runs a licence-read agent per source and records the verdict and credit in its drafts file (entry "Licence reads for the Japan builds"); the build session writes its own `docs/data_sources/japan.md` row from it. Until then a session may build the city pipeline-only (steps 1-3, privacy and census checks; no notice, page text or data_sources row), and drops it if the read comes back NOT PERMITTED.
- **Batches are about 12 cities**, the measured size. A session at its batch's end writes its handoff and stops; the next session starts fresh.

## Page and notice numbers

Each session takes its numbers from its own block, recorded in `docs/session_roles.md` (the numbers paragraph), and scaffolds with `scaffold_city.py ... --page-number <N>`. Pages go one per city in the session's build order; notices are claimed from the block as they are written.

| Session | Pages | Notices |
|---|---|---|
| Abroad | 202, 300–304 | 154–156 |
| East-1 | 210–221 | 157–168 |
| Kansai-1 | 222–228 | 169–175 |
| Regional-1 | 229–239 | 176–186 |
| East-2 | 240–250 | 187–197 |
| Kansai-2 | 251–257 and 305 (Cluj-Napoca) | 198–204 and 215 (Cluj-Napoca) |
| Regional-2 | 258–267 and 306 (Kurashiki) | 205–214 and 216 (Kurashiki) |

A session that runs out asks Staging for more. Unused numbers are released when the session lands.

## Rules every build session follows

- **The macro map's region views are Cleanup's** (owner, call 198, 2026-10-07: "198 yes, cleanup builds them"). Cleanup builds Japan's eight regions plus Osaka Prefecture on its own branch at the phase 1 review time, and Europe West, Europe East, Germany and Benelux are on its europe-split branch (call 197). Build sessions never add or change region views, REGION_LABELS_ALSO, label tiers or macro label offsets. This overrides the japan-city skill's "made by the first wave-4 city to land". A check_macro_labels failure only for new cities labelled in no view goes in the batch report and is left.
- Read CLAUDE.md, `docs/session_roles.md` and the session's skills.
- Run `python scripts/brief_check.py <city>` before any code; a failing check is a brief to correct.
- Apply each brief's "Answered by the owner" calls as written, and log every judgment call in `docs/decisions_drafts/<branch>.md`.
- **Parallel work.** Up to three subagents may build cities in parallel, each in its own `pipeline/<city>/` and data directory.
  - The lead session alone edits shared files: `app/cities.py`, `app/pages/`, `docs/data_sources*`, `docs/excluded_categories.md` and the macro facts.
  - No worktree switch while a subagent runs.
- Overpass: one query in flight per session.
- Heavy jobs go through the `heavy_job.py` gate.
- Run `check_personal_exposure.py`, `check_provenance.py` and `check_scope_disclosure.py` per city, and `check_all.py` before the batch report.
- **At the batch's end:** every check green, drift clean, everything committed on the branch, nothing pushed. Send Staging Session one message: the cities ready, the parked calls (numbered, with recommendations), and any slip. Staging relays them to the owner.

## Session prompts

Start each session in the main checkout, not in the app's worktree mode, which gives a random name. Each prompt's first line has the session enter its own named worktree and fast-forward it to origin/master (the main checkout runs behind), which makes `.claude/worktrees/<name>` on branch `worktree-<name>`, as staging and cleanup did.

### Japan foundation

```
First, enter a new worktree named japan-foundation (use the EnterWorktree tool), then bring it up to date: git fetch origin, then git merge --ff-only origin/master. Then continue.

You are the Japan foundation session for expanded-heatmap (worktree japan-foundation). Read docs/build_plan_2026-10-07.md first: its rules and usage check-ins bind you. No city is built here.

1. Compile the checklist. Take every "⚠️ Shared code" item in the Japanese briefs under docs/build_briefs/ for the cities in the plan's table. Add the owner's rules in docs/decisions_drafts/staging.md:
   - calls 158, 161, 162 and 172;
   - 自動車以外 is not a vehicle;
   - an asterisk-only address is withheld;
   - 未選択 is no address;
   - 露天 is a temporary word;
   - 自動車 in a permit condition marks a vehicle.
   Merge duplicates and write the list into your drafts file, each item naming its briefs.
2. Implement each in the shared Japanese modules (japan_step2, the japan_eigyo taxonomy, the readers and column lists), never city-locally.
   - After each small group: run the Minato control (screen_japan_join.py minato, expect 98.0 / 0.2 / 1.8), then `python pipeline/drift_check.py` over the built Japanese cities with --jobs 3 (measured 2-3.4 min).
3. Built maps must not change. A rule that would change a built city's output is switched on per city in config, defaulting on for new cities and off for built ones. List each affected built city and the size of the change in your drafts file as a review-time re-render proposal.
4. Put each rule where the next city passes through it: a raising check in shared code, then a line in .claude/skills/japan-city/SKILL.md.
5. When check_all.py is green and the drift check reports zero changes on every built city: fetch, merge if behind and push (pipeline and skill only; no app/ file). Then message Staging Session that the foundation has landed, with the commit, the rules, and any parked call.
```

### Abroad

```
First, enter a new worktree named abroad-batch (use the EnterWorktree tool), then bring it up to date: git fetch origin, then git merge --ff-only origin/master. Then continue.

You are the Abroad build session for expanded-heatmap (worktree abroad-batch). Read docs/build_plan_2026-10-07.md first: its rules and usage check-ins bind you.

Build, in this order, from each city's brief in docs/build_briefs/:
- Gimpo, Siheung (korea-city);
- Geneva (tram-city);
- Thessaloniki (add-city);
- Gelsenkirchen (tram-city);
- Bremen (tram-city; its licence read comes first, by the licence-read agent; its CC BY is stated, not yet read in full);
- then the extensions (regional-extension): Anyang (Regional), Mexico City (Regional), Copenhagen (Regional).

Seoul, Busan and Daegu (Regional) are NOT built: they wait for SEMAS's social-post scope (call 71).

At the batch's end, report to Staging Session as the plan says.
```

### Japan build sessions (East-1, Kansai-1, Regional-1, East-2, Kansai-2, Regional-2)

```
First, enter a new worktree named <WORKTREE> (use the EnterWorktree tool), then bring it up to date: git fetch origin, then git merge --ff-only origin/master. Then continue.

You are the <NAME> build session for expanded-heatmap (worktree <WORKTREE>). Read docs/build_plan_2026-10-07.md first: its rules and usage check-ins bind you. Start from origin/master, which holds the Japan foundation's shared-code rules.

Build, in this order, from each city's brief in docs/build_briefs/ and the japan-city skill: <CITIES FROM THE PLAN'S TABLE>.

The briefs' shared-code items are already in shared code (the foundation, 7ab440f9 and 521d28fc; the japan-city skill's foundation section names each rule). If one is missing, it is a parked call, not a city-local fix. Leave "rules" out of each japan.CITIES entry: the new rules are on by default for new cities, and japan.py refuses an entry that names WAVE2_RULES. A zipped register (Maebashi's, Sagamihara's) needs a city source_rows.

<KANSAI ONLY: You pull the most from BODIK; keep calls at least 20 s apart, one city at a time, and never use datastore_search_sql.>
<KANSAI-2 ONLY: After the Japanese cities, build Cluj-Napoca (owner, call 222) from docs/build_briefs/cluj_napoca.md with add-city, osm-rail and address-join, on page 305 and notice 215: food only, the unplaced share stated, placement by the OSM address join with the brief's three repairs plus the nearest same-side house-number tier (Palma's code, at most 6 numbers away), the owner's DSVSA files already in data/cluj_napoca/raw/. At that build, write the romania-city skill (each county numbers its files differently, so map files to roles by name; canteens, catering, trailers and stands out; the OSM join plus the tier; the 70% bar). Then take Naha's one measurement from its master-list row, if BODIK answers without a block; otherwise record the refusal and stop.>

At the batch's end, report to Staging Session as the plan says, and write a handoff note for the next session in your group.
```

## Phase 2 prompts, ready to paste (prepared 2026-10-08 for a start on Sunday 2026-10-11)

The template above, filled in. Start each in the main checkout, one message each, after the owner's go; the weekly pool resets 2026-10-11 19:00 UTC. All three may run at once (at most three build sessions); Kansai-2 is the slowest (BODIK spacing, then Cluj-Napoca and Naha).

### East-2

```
First, enter a new worktree named japan-east-2 (use the EnterWorktree tool), then bring it up to date: git fetch origin, then git merge --ff-only origin/master. Then continue.

You are the East-2 build session for expanded-heatmap (worktree japan-east-2). Read docs/build_plan_2026-10-07.md first: its rules and usage check-ins bind you. Start from origin/master, which holds the Japan foundation's shared-code rules and the wave 2 rules (the japan-city skill's "After the large review (2026-10-07)" section: one colour per line site-wide from pipeline/line_registry.py, checked by scripts/check_line_identity.py).

Build, in this order, from each city's brief in docs/build_briefs/ and the japan-city skill, on pages 240-250 and notices 187-197 in build order: Koshigaya, Sagamihara, Fujisawa (A); Kawaguchi, Funabashi, Matsudo, Ichikawa, Urayasu, Sakura, Yachiyo, Ichihara (B).

The briefs' shared-code items are already in shared code (the foundation, 7ab440f9 and 521d28fc; the japan-city skill's foundation section names each rule). If one is missing, it is a parked call, not a city-local fix. Leave "rules" out of each japan.CITIES entry: the new rules are on by default for new cities, and japan.py refuses an entry that names WAVE2_RULES. A zipped register (Sagamihara's) needs a city source_rows.

Licence calls already answered (docs/decisions_drafts/staging.md, "Licence reads for the Japan builds"): Kawaguchi's 「データ利用のみ自由です」 is read permissively, its licence CC BY 2.1 JP (call 208); Fujisawa's individual-operator file goes through the name rule. Merge notes: keep both sides at japan_register.OPERATOR_COLS_WAVE5 and at the WAVE5 switches (name_city, default_joined).

At the batch's end, report to Staging Session as the plan says, and write a handoff note for the next session in your group.
```

### Kansai-2

```
First, enter a new worktree named japan-kansai-2 (use the EnterWorktree tool), then bring it up to date: git fetch origin, then git merge --ff-only origin/master. Then continue.

You are the Kansai-2 build session for expanded-heatmap (worktree japan-kansai-2). Read docs/build_plan_2026-10-07.md first: its rules and usage check-ins bind you. Start from origin/master, which holds the Japan foundation's shared-code rules and the wave 2 rules (the japan-city skill's "After the large review (2026-10-07)" section: one colour per line site-wide from pipeline/line_registry.py, checked by scripts/check_line_identity.py).

Build, in this order, from each city's brief in docs/build_briefs/ and the japan-city skill, on pages 251-257 and notices 198-204 in build order: Ibaraki (Osaka), Minoh, Moriguchi, Kadoma, Neyagawa, Yao, Takatsuki (B). Moriguchi is counted first at its brief against Settsu's too-thin test.

The briefs' shared-code items are already in shared code (the foundation, 7ab440f9 and 521d28fc; the japan-city skill's foundation section names each rule). If one is missing, it is a parked call, not a city-local fix. Leave "rules" out of each japan.CITIES entry: the new rules are on by default for new cities, and japan.py refuses an entry that names WAVE2_RULES.

You pull the most from BODIK; keep calls at least 20 s apart, one city at a time, and never use datastore_search_sql. Merge notes: keep both sides at japan_register.OPERATOR_COLS_WAVE5 and at the WAVE5 switches (name_city, default_joined).

After the Japanese cities, build Cluj-Napoca (owner, call 222) from docs/build_briefs/cluj_napoca.md with add-city, osm-rail and address-join, on page 305 and notice 215: food only, the unplaced share stated, placement by the OSM address join with the brief's three repairs plus the nearest same-side house-number tier (Palma's code, at most 6 numbers away), the owner's DSVSA files already in data/cluj_napoca/raw/. Overpass: one query in flight. At that build, write the romania-city skill (each county numbers its files differently, so map files to roles by name; canteens, catering, trailers and stands out; the OSM join plus the tier; the 70% bar).

Then take Naha's one measurement from its master-list row, if BODIK answers without a block; otherwise record the refusal and stop.

At the batch's end, report to Staging Session as the plan says, and write a handoff note for the next session in your group.
```

### Regional-2

```
First, enter a new worktree named japan-regional-2 (use the EnterWorktree tool), then bring it up to date: git fetch origin, then git merge --ff-only origin/master. Then continue.

You are the Regional-2 build session for expanded-heatmap (worktree japan-regional-2). Read docs/build_plan_2026-10-07.md first: its rules and usage check-ins bind you. Start from origin/master, which holds the Japan foundation's shared-code rules and the wave 2 rules (the japan-city skill's "After the large review (2026-10-07)" section: one colour per line site-wide from pipeline/line_registry.py, checked by scripts/check_line_identity.py).

Build, in this order, from each city's brief in docs/build_briefs/ and the japan-city skill, on pages 258-267 and notices 205-214 in build order: Shizuoka, Kanazawa, Okazaki, Aomori, Matsue, Fuji, Matsumoto, Tottori, Yamagata, Kure (B); then Kurashiki (B, owner call 226) on page 306 and notice 216, from its year-end PDF of permits in force (pdftotext or pypdf, never a hand-written decoder).

The briefs' shared-code items are already in shared code (the foundation, 7ab440f9 and 521d28fc; the japan-city skill's foundation section names each rule). If one is missing, it is a parked call, not a city-local fix. Leave "rules" out of each japan.CITIES entry: the new rules are on by default for new cities, and japan.py refuses an entry that names WAVE2_RULES.

Licence calls already answered (docs/decisions_drafts/staging.md, "Licence reads for the Japan builds" and the 2026-10-08 Kurashiki entries): Yamagata §4, a use-triggered reimbursement, accepted (call 206); Matsumoto's two use-triggered clauses accepted, the credit naming CC BY 4.0 in the city's format plus LinkData's CC BY 3.0 mark (call 207); Okazaki 5(5), use-triggered, accepted (call 214); Kurashiki's barber and beauty lists stay out (call 225). Matsue's 八雲村 is a config key (its brief says how). Keep BODIK calls at least 20 s apart. Merge notes: keep both sides at japan_register.OPERATOR_COLS_WAVE5 and at the WAVE5 switches (name_city, default_joined).

At the batch's end, report to Staging Session as the plan says, and write a handoff note for the next session in your group.
```
