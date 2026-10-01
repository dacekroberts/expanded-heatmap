# The site-wide prose and UI pass (owner, 2026-10-01)

Five agent sessions, each in its own worktree on its own branch, all made from
`origin/master` at 88315b12 (the Global label competition). The cleanup session
(**Cleanup session [f2d0ed]** in `ListAgents`; the id changes on restart)
merges and lands. Kit: `docs/review_lane_kit.md`. The UK builds are held until
this pass is deployed; afterwards the city-building and page skills are
reworked to the new formats.

| Agent | Worktree (`.claude/worktrees/...`) | Branch | Streamlit / static / capture `--cdp` | Review folder |
|---|---|---|---|---|
| 1 Neutral comments | `prose-1-comments` | `prose-1-comments` | 8831 / 8832 / 9331 | `data/_review/prose-1-comments/` |
| 2 What Is Excluded + About the Data | `prose-2-excluded-sources` | `prose-2-excluded-sources` | 8841 / 8842 / 9341 | `data/_review/prose-2-excluded-sources/` |
| 3 Overview city list | `prose-3-city-list` | `prose-3-city-list` | 8851 / 8852 / 9351 | `data/_review/prose-3-city-list/` |
| 4 City pages | `prose-4-city-pages` | `prose-4-city-pages` | 8861 / 8862 / 9361 | `data/_review/prose-4-city-pages/` |
| 5 Audit and shorten | `prose-5-audit` | `prose-5-audit` | 8871 / 8872 / 9371 | `data/_review/prose-5-audit/` |

**Order.** Agents 1-4 start at once: their files do not overlap (each prompt
names its own). Agent 1 runs a pilot past the owner before rolling out.
Agent 4 shows the owner sample pages before rolling out. Cleanup merges 1-4
into one integration branch as each finishes; agent 5 starts on that merge.
One landing, one reboot, one `deploy-verify scope: full`.

**File ownership** (no agent edits another's files; ask cleanup if a change is
needed elsewhere):

- Agent 1: every tracked `.py` file EXCEPT `app/Overview.py`,
  `app/components.py`, `app/pages/*`, `scripts/france_page.py`,
  `scripts/scaffold_city.py`, `scripts/scaffold_france_batch.py`, and the
  per-city folders `pipeline/<city>/` (phase 2, the owner's call later).
- Agent 2: `app/pages/200_About_the_Data.py`, `app/pages/201_What_Is_Excluded.py`,
  a new `app/country_sections.py` if needed, and the STRUCTURE (not the
  wording) of `docs/excluded_categories.md`, `docs/data_sources.md` and
  `docs/data_sources/*.md`.
- Agent 3: `app/Overview.py`'s city list (not the map, the competition or the
  region selector's behaviour), and a new `app/city_list.py` if needed.
- Agent 4: `app/pages/*_Heatmap.py`, `app/components.py`,
  `scripts/france_page.py`, `scripts/scaffold_city.py`,
  `scripts/scaffold_france_batch.py`.
- Agent 5: nothing but proposals and its report.

**The deep-link contract between agents 2 and 4**: a city page links to
`What_Is_Excluded?country=<country>` and `About_the_Data?country=<country>`,
where `<country>` is the city's `country` value in `app/cities.py`,
URL-encoded. Agent 2's pages open on that country when the parameter is
present; agent 4's pages emit the links.

---

## Shared rules (every prompt includes them by reference)

1. Read `CLAUDE.md` and obey it. In particular: **no backslash or backtick in
   any Bash command** (write a file, run it); never `git add -A`; any heavy
   run goes through `scripts/heavy_job.py` (a page capture declares 1.5 GB);
   probe and scratch output goes to your session scratchpad or your review
   folder, never the repo.
2. Work only in your worktree, only on your branch, only on your files.
   **Commit on your branch as you go; never push, never merge, never touch
   master.** Cleanup merges and lands.
3. Judgment calls go to your drafts file `docs/decisions_drafts/<your
   branch>.md` in the `decisions-entry` format, never to `DECISIONS.md`.
4. **Interpretive prose is the owner's.** New or changed reader-facing
   sentences you write yourself go through `scripts/prose_proposals.py`
   (format in its docstring; your proposals file is
   `data/_review/<your branch>/proposals.md`) unless the owner approved the
   format or template they come from in your session. UI labels (a selector's
   label, a heading) you may write, and list in your report.
5. Comments in the files you edit follow the neutral comment style
   (`neutral-comment-style.md` at the main checkout's root, sections 2 and 9):
   neutral voice, keep every measured value and re-check warning, at most one
   line of how it was found, no em dashes in comments.
6. Before reporting done: `python scripts/check_all.py` passes in your
   worktree; for any `app/` change, `python scripts/check_deploy_imports.py`
   on your committed branch (`--ref HEAD`), and a capture of every page you
   changed with `scripts/capture_pages.mjs` against your own Streamlit port
   (start it with `preview_start` using your worktree's `streamlit-app-lean`
   configuration), at 375, 768 and 1200, light and dark. Look at the
   captures.
7. Report to cleanup by message (`SendMessage` to the cleanup session's
   `ListAgents` name) and in `data/_review/<your branch>/report.md`: what
   changed, commits, checks, captures folder, open questions for the owner.

---

## Prompt 1 - Neutral code comments

> You are agent 1 of the site-wide prose and UI pass for the expanded-heatmap
> project. Work in `C:\Users\dacek\Documents\Portfolio\expanded-heatmap\.claude\worktrees\prose-1-comments`
> on branch `prose-1-comments`. Read `docs/prose_pass_2026-10-01.md` there
> (the shared rules and your file ownership) and the handoff
> `C:\Users\dacek\Documents\Portfolio\expanded-heatmap\neutral-comment-style.md`
> in full before editing anything.
>
> Goal: roll the neutral comment style out across this repo's code comments
> and docstrings, comments only, without changing a line of code or any
> visible text. The owner has already chosen the style (neutral voice; audience
> both a reader of the repo and whoever changes the code next; verification
> history one line at most; no em dashes in comments). This repo has about
> 44,000 comment and docstring lines; your scope is phase 1: every tracked
> `.py` file except the ones the plan gives to agents 2-4 and the per-city
> folders `pipeline/<city>/`. That is the shared pipeline (`pipeline/*.py`,
> `pipeline/countries/`, `pipeline/taxonomies/`), `scripts/`, and the app
> modules `app/cities.py`, `app/station_scope.py`, `app/label_competition.py`.
>
> Follow the handoff's process (its section 5):
> 1. Measure (counts by file, first person, narration, em dashes).
> 2. Pilot `scripts/check_provenance.py` (404 comment lines, all four kinds).
>    Verify it comments-only with the handoff's `verify_comments_only.py` (keep
>    that script in your scratchpad), show the owner in this session what you
>    REMOVED, not only what you kept, and wait for the owner's approval before
>    any rollout. Commit the pilot on approval.
> 3. Add `scripts/check_no_em_dashes.py` from the handoff, adapted (`git
>    ls-files`, visible text exempt), watch it fail on planted em dashes in a
>    temp copy first, then add it to `scripts/check_all.py`, and add the
>    handoff's section 8 snippet to `CLAUDE.md` (with the pilot as the
>    reference example). Fix the four em dashes in comments it finds in your
>    files; report any in files you do not own.
> 4. Roll out with subagents split by disjoint file sets (shared pipeline;
>    taxonomies; countries; scripts in two halves; the three app modules).
>    Each must pass `verify_comments_only.py` (IDENTICAL) on its files and
>    report three before/after pairs and anything kept long on purpose. Sweep
>    their work yourself afterwards.
> 5. **This project's lessons are load-bearing.** Many comments record why a
>    value is what it is, a measured failure (Toronto's 118 stations, the
>    Guadalajara pill), or a rule a check enforces. Keep every number, every
>    re-measure warning and every pointer to `DECISIONS.md`,
>    `docs/rule_history.md` or a skill; cut the narration around them. The
>    long `WHY` blocks in `pipeline/map_common.py` and `app/cities.py` keep
>    their substance. Do not touch dated log text, verbatim licence quotes, or
>    any string that renders.
> 6. **Comments inside strings that ship in the maps** (the CSS and JS
>    `pipeline/map_common.py` embeds in every `heatmap.html`) are out of scope:
>    rewording them would change all 124 committed maps. Leave them, and list
>    the em dashes among them in your report.
> 7. `check_all.py` must pass, and `pipeline/drift_check.py --render-only
>    --jobs 2` through the memory gate must show no map drift (comments in
>    `map_common.py` outside strings do not reach the maps; prove it).
>
> Commit by path on your branch in sensible units. Report as the shared rules
> say, with lines before and after per area.

## Prompt 2 - What Is Excluded and Where this data comes from

> You are agent 2 of the site-wide prose and UI pass for the expanded-heatmap
> project. Work in `C:\Users\dacek\Documents\Portfolio\expanded-heatmap\.claude\worktrees\prose-2-excluded-sources`
> on branch `prose-2-excluded-sources`. Read `docs/prose_pass_2026-10-01.md`
> there first (shared rules, your file ownership, and the deep-link contract
> with agent 4).
>
> Goal: the two long reference pages - **What is counted, and what is not**
> (`app/pages/201_What_Is_Excluded.py`, which renders
> `docs/excluded_categories.md` and every city's
> `outputs/<slug>/excluded_stations.csv` via `app/station_scope.py`) and
> **Where this data comes from** (`app/pages/200_About_the_Data.py`, which
> renders `docs/data_sources.md` and each `docs/data_sources/<country>.md`) -
> stop being one long scroll. The owner chose option B: keep both as their own
> pages, linked as now, but rebuild them as a streamlined, selectable layout:
> a country selector (or country labels across the top, like the map's region
> selector or the Cities dropdown) that shows one country's section at a time,
> plus the shared, all-city material where a reader expects it.
>
> Requirements:
> - **Deep link** (the contract): `?country=<country>` (the `country` value in
>   `app/cities.py`, URL-encoded) opens the page on that country; without it,
>   a sensible default (say which and why in your report). Unknown values fall
>   back to the default without an error.
> - **Nothing is lost.** Every section, every table row and every sentence the
>   pages render today still renders for its country or in the shared part.
>   Prove it: capture both pages before your change (all text, every country)
>   and after, and diff the text in your review folder.
> - **The required source notices stay inline and visible** on both pages
>   (`components.render_site_notices`; never behind an expander, tab or
>   toggle - see that function's comment on Chicago's terms). Do not edit
>   `app/components.py` (agent 4 owns it); if you need a hook there, say so.
> - **Checks that read these docs keep passing**: `check_scope_disclosure.py`,
>   `check_provenance.py` (its citation and notice checks), `check_barred_marks.py`,
>   `rendered_surfaces.py --check` (regenerate with `--write` if your pages'
>   doc paths change), `check_stray_bullets.py`. If a check reads a structure
>   you change, adapt the structure, not the check, unless the check is
>   reading layout rather than content; then say so to cleanup first.
> - Restructuring the docs (headings, a per-country split of
>   `docs/excluded_categories.md` if it helps) is yours; rewording their
>   sentences is not - prose changes go through proposals. Agent 5 shortens.
> - Mobile first: the selector must work at 375 px. Both themes.
> - Show the owner, in this session, a capture of each page at 375 and 1200
>   before you finish, and ask about anything that is a matter of taste (where
>   the shared material sits, the default country).
>
> Report as the shared rules say.

## Prompt 3 - The Overview's city list

> You are agent 3 of the site-wide prose and UI pass for the expanded-heatmap
> project. Work in `C:\Users\dacek\Documents\Portfolio\expanded-heatmap\.claude\worktrees\prose-3-city-list`
> on branch `prose-3-city-list`. Read `docs/prose_pass_2026-10-01.md` there
> first (shared rules and your file ownership).
>
> Goal: recreate the city list under the macro map on the front page
> (`app/Overview.py`) so it is fluid instead of one long list (it runs to
> dozens of phone screens at 124 cities). The owner's idea: a dynamic table
> organised by region - region headers or a region selector, and that region's
> cities beneath. **The map's existing region selector drives it**: choosing a
> region on the map shows that region's cities in the list; Global shows every
> region in its own section (or the most useful equivalent - propose it). One
> control, not two.
>
> Requirements:
> - Keep what each row tells a reader today (read the current list and
>   `app/cities.py`'s fields it uses: name, mode, coverage, data age,
>   storefront count and so on) and each row's link to the city page. If you
>   would drop a column, ask the owner.
> - Do NOT change the macro map, its layers, the Global label competition
>   (`app/label_competition.py`), or how the region selector behaves for the
>   map. `scripts/check_macro_labels.py` and `check_deploy_imports.py` must
>   pass unchanged.
> - The caption arithmetic ("every city is on the map", the per-region counts
>   in `cities.elsewhere_counts`) must stay true: `check_macro_labels.py`'s
>   caption check.
> - Streamlit only, no new dependency (`requirements.txt` stays lean:
>   streamlit and pandas). Mobile first (375 px), both themes. It must render
>   fast: the Overview is the landing page.
> - Show the owner a capture at 375 and 1200 in this session before you
>   finish; layout choices are the owner's.
>
> Report as the shared rules say.

## Prompt 4 - City pages

> You are agent 4 of the site-wide prose and UI pass for the expanded-heatmap
> project. Work in `C:\Users\dacek\Documents\Portfolio\expanded-heatmap\.claude\worktrees\prose-4-city-pages`
> on branch `prose-4-city-pages`. Read `docs/prose_pass_2026-10-01.md` there
> first (shared rules, your file ownership, and the deep-link contract with
> agent 2).
>
> Goal: every city page (`app/pages/*_Heatmap.py`, 124 pages) in one new
> format the owner set:
> 1. **Title, centred**: the city's name as the title, with the subtitle
>    "Transit-centered commercial density heatmap" (the owner chose title plus
>    subtitle over one long title, which wraps badly on a phone for names like
>    "Kitchener–Waterloo (Regional)").
> 2. **The map comes next, with no exceptions**: nothing between the title
>    block and the map. A reader arriving from the macro map must not scroll
>    to reach it. The caption with the data dates goes directly under the map.
>    Keep the map's embed height (`st.iframe(..., height=650)`) - the OSM
>    attribution check depends on it (`CLAUDE.md`, attribution invariant);
>    re-run `scripts/check_map_attribution.js` on a sample if anything around
>    the map changes.
> 3. **Then the required notices.** The full site notice list
>    (`components.render_site_notices`) must stay inline on every page (never
>    behind an expander: Chicago's terms). The owner's direction: notices
>    immediately after the map if needed, or after the bullets. Recommended:
>    the city's own required credits (the notices for its sources, and any
>    credit its page must show, e.g. « Source : Insee » on French pages, which
>    check M of `check_provenance.py` enforces) directly under the map, and
>    the full site list where it is now, in the footer. Confirm with the owner.
> 4. **Then the prose, as bullets or short sentence lists.** The long
>    explanations belong on the reference pages (What is counted, Where this
>    data comes from, Why the maps differ). Each page links to What Is
>    Excluded and About the Data with its country preselected
>    (`?country=<country>`, the contract).
>
> How:
> - **Template families.** The 21 French pages are generated by
>   `scripts/france_page.py` (change the template and regenerate); the other
>   103 were scaffolded by `scripts/scaffold_city.py` and hand-edited since.
>   Write a restructuring script for the layout (title, map, caption, notices,
>   prose order) that works on every page's shared skeleton, and verify it by
>   capture. The bullets are writing work: split it by family (country or
>   build kit: France; Czechia; the tram kit; Japan; Korea; Taiwan; Brazil;
>   the US cities; and so on) across subagents with disjoint pages.
> - **Samples first.** Before any rollout, convert two or three pages from
>   different families (suggest one French, one US, one Asian) and show the
>   owner captures at 375 and 1200. The bullet format is approved on those
>   samples; after that, conversions that follow the approved format need no
>   per-sentence approval. A sentence that adds or changes a claim is a
>   proposal (`scripts/prose_proposals.py`).
> - **No fact is lost.** Every claim a page makes today (scope, exclusions,
>   caveats, data dates, closures, privacy rules) survives in a bullet or is
>   already on a reference page the page links to; if you move a claim off a
>   page, list it in your report. Checks that read page text must pass:
>   `check_scope_disclosure.py`, `check_provenance.py` (check M and the
>   citation checks), `check_barred_marks.py` (Angers is mark-free),
>   `rendered_surfaces.py --check`.
> - **Update the templates** so a new page is born in the new format:
>   `scripts/scaffold_city.py`'s page template, `scripts/france_page.py`,
>   `scripts/scaffold_france_batch.py`. (Rewriting the city-building skills is
>   after the pass, by cleanup.)
> - Mobile first, both themes, captures of every page at 375 and 1200 (light
>   and dark) in your review folder; `errors.json` empty.
>
> Report as the shared rules say, with the list of claims moved off pages.

## Prompt 5 - Audit and shorten (start when cleanup says the merge is ready)

> You are agent 5 of the site-wide prose and UI pass for the expanded-heatmap
> project. Work in `C:\Users\dacek\Documents\Portfolio\expanded-heatmap\.claude\worktrees\prose-5-audit`
> on branch `prose-5-audit`. Read `docs/prose_pass_2026-10-01.md` there first.
> **Wait for cleanup's message that agents 1-4 are merged**, then merge the
> integration branch it names into your branch and begin.
>
> Goal: audit what agents 1-4 changed, and make a final pass at shortening
> prose where it helps a general reader. You edit nothing but your proposals
> and your report.
>
> 1. **Audit**: `python scripts/check_all.py`; `check_deploy_imports.py`;
>    capture every page (`node scripts/capture_pages.mjs --pages all`, 375,
>    768 and 1200, light and dark, through the memory gate at 1.5 GB, `--cdp
>    9371`) and look at them: the map first on every city page, titles centred,
>    notices present and inline, both reference pages' selectors and deep
>    links (`?country=`), the Overview's city list per region, no console
>    errors. Compare with `docs/rendered_surfaces.md` so no surface is missed.
>    Check the comment rollout's sample (`check_no_em_dashes.py`, a spot read of
>    ten files against the handoff's rules).
> 2. **Shorten**: read every page's prose and the reference pages; propose
>    cuts and rewrites that keep every fact, in plain words for a general
>    audience. Each is a proposal in `data/_review/prose-5-audit/proposals.md`
>    (format in `scripts/prose_proposals.py`), `kind: fix` for a factual error
>    and `kind: proposal` for wording. Then run `python
>    scripts/prose_proposals.py collate` so the owner gets one numbered list
>    (`data/_review/proposals_all.md`).
> 3. Findings that are not prose (layout, a check, a broken link): list them in
>    your report with page, width, theme, and whether they block the landing.
>
> Report as the shared rules say.
