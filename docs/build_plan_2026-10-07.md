# Build plan for the A and B cities (owner, 2026-10-07)

The owner lifted the build pause on 2026-10-07 and approved the four changes
below and the usage check-ins. This file holds the order, the rules every build
session follows, and one prompt per session. Staging keeps it current; a
session's prompt is pasted as its first message.

**Scope.** 64 briefed cities (A 32, B 32) and 6 briefed extensions. Kurashiki
and Naha (Band C) are not built: Kurashiki waits on an owner call, and Naha on
one measurement (Kansai-2 takes it if BODIK answers). Band D waits for the
owner. Seoul, Busan and Daegu (Regional) wait for SEMAS's social-post scope
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
   - Parked calls reach the owner as one numbered list per wave, through Staging.
3. **One review time per phase.** Landings, re-renders and deploy-verify are batched: after phase 0, after the first Japan trio, and after the second. Only the owner calls review time. App reboots happen once per landing.
4. **Build sessions never edit `docs/city_master_list.md`.** Staging moves a wave's cities to Built in one pass after each landing, and republishes the private pages. A build lands in one push at the end of its batch, after review time; `app/cities.py` conflicts are resolved keep-both.

**Usage check-ins (owner):** "pause and check in with me (here or in cleanup) before continuing when weekly usage hits a multiple of ten."
- Check `get_usage` between cities. The weekly read 42% on 2026-10-07, so the next stop is 50%, then 60%, and so on.
- At a crossing: finish the current step, commit clean, and stop. Tell the owner in your own chat and send one line to Staging Session. Continue only on the owner's word.
- All sessions share one pool, so one crossing stops every session.
- The 5-hour window's 90% ceiling still applies.

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
| 2 | **Kansai-2** (`japan-kansai-2`) | B: Ibaraki (Osaka), Minoh, Moriguchi, Kadoma, Neyagawa, Yao, Takatsuki; then Naha's measurement if BODIK answers | japan-city |
| 2 | **Regional-2** (`japan-regional-2`) | B: Shizuoka, Kanazawa, Okazaki, Aomori, Matsue, Fuji, Matsumoto, Tottori, Yamagata, Kure | japan-city |

- **Phase 1 starts when the foundation lands on master.** Until Abroad finishes, only two Japan sessions run at once.
- **Each phase 2 session starts** from master after the phase 1 session in the same group has handed off.
- **BODIK:** the Kansai sessions are the only sessions that call it, at least 20 s apart. They run one after the other.
- **Batches are about 12 cities**, the measured size. A session at its batch's end writes its handoff and stops; the next session starts fresh.

## Rules every build session follows

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

The briefs' shared-code items are already in shared code. If one is missing, it is a parked call, not a city-local fix.

<KANSAI ONLY: You are the only session calling BODIK; keep calls at least 20 s apart and never use datastore_search_sql.>
<KANSAI-2 ONLY: After the cities, take Naha's one measurement from its master-list row, if BODIK answers without a block; otherwise record the refusal and stop.>

At the batch's end, report to Staging Session as the plan says, and write a handoff note for the next session in your group.
```
