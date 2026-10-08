# Commands

Every project script's usage line, moved out of `CLAUDE.md` on 2026-10-04 to
keep it inside its word budget (`scripts/check_word_budgets.py`; owner, the
efficiency review's third change). Each script's own docstring is the full
reference; `python scripts/check_all.py --list` lists the pass/fail checks.

```bash
python pipeline/<city_slug>/step1_stations.py
python pipeline/<city_slug>/step2_clean_businesses.py
python pipeline/<city_slug>/step3_map.py
python pipeline/drift_check.py [city_slug] [--jobs N]   # every city; --jobs 3 at most, one run per machine
python pipeline/drift_check.py --render-only [--jobs N] # map step only, against data/<city>/processed/ as it stands; never the pre-deploy gate
python scripts/drift_check_selftest.py                  # touches nothing
python scripts/brief_check.py [city_slug]               # re-run a brief's claims live
python scripts/check_all.py [--list]                    # every pass/fail check, ~30s; the pre-push hook runs it
git config core.hooksPath .githooks                     # once per clone: turns that hook on
python scripts/check_provenance.py [--strict]           # after adding a city
python scripts/check_no_fetch_in_steps.py [--list]
python scripts/check_no_fetch_in_steps_selftest.py      # touches nothing
python scripts/check_scope_disclosure.py
python scripts/check_scope_disclosure_selftest.py       # touches nothing
python scripts/check_inconsistency_list.py              # when a city lands
python scripts/check_stray_downloads.py                 # untracked files at any checkout's root
python scripts/check_overpass_hosts.py [--live|--selftest]   # every Overpass mirror is global
python scripts/check_worktree_data.py <worktree> [--list]   # before removing a worktree
python scripts/check_render_current.py                  # after merging
python scripts/check_map_markup.py [--verbose]          # dark-mode label contrast, legend styles
python scripts/check_line_identity.py [--rendered|--neighbours|--verbose]   # one colour per line across maps (pipeline/line_registry.py)
python scripts/check_no_em_dashes.py                    # no em dash in any comment or docstring
python scripts/check_name_keys.py [--selftest]          # withheld-name lists hold keys, not names
python scripts/check_internal_markers.py [--selftest]   # every <!-- internal --> span closed, contained, clean
python scripts/check_internal_prose.py [--counts|--surface S|--kind K]   # REPORTS only: note-like prose a reader can see
python scripts/check_city_page_format.py [--selftest]   # every city page: title, map, ..., notices last; no repo path in its text
python pipeline/name_keys.py "NAME" ["NAME" ...]        # the key to list for a name read as a person's own
python scripts/check_inline_arrays.py [--report|--selftest]   # no JS array an iPhone cannot compile; after any re-render
python scripts/check_html_lang.py [--selftest]          # every map's <html lang> matches its map step; after any re-render
python scripts/check_city_registry.py                   # after merging
python scripts/check_conflict_markers.py [--file PATH]  # after merging; a marker git left in any tracked file
python scripts/check_conflict_markers_selftest.py       # touches nothing
python scripts/check_plan_done.py [--verbose]           # REPORTS only
python scripts/check_stale_claims.py                    # REPORTS only
python scripts/check_stale_claims.py --only E           # "only city" claims; when a city lands
python scripts/check_discard_evidence.py [--selftest]   # when the discard table changes
python scripts/measure_rail_backbone.py --osm <json> --relation <id> --municipios <json> --codes <ibge> --stations <csv> --crs <epsg>   # commuter-line rail test
python scripts/check_deploy_imports.py [--ref REF]      # before ANY push touching app/
node scripts/profile_zoom.mjs <baseUrl> <city,city> [reps]   # zoom lag
node scripts/check_macro_attribution.mjs [baseUrl] [375,768,1200]   # front page OSM credit; live: <app>/~/+
python scripts/decisions_index.py [--check]
python scripts/rendered_surfaces.py [--write|--check]   # every surface the app renders -> docs/rendered_surfaces.md
python scripts/downstream_changes.py <old> [<new>]       # after every push: what to tell Visuals and Analytics
python scripts/review_lanes.py create --sha <commit> --lanes <n> | list | remove   # review-lane worktrees
node scripts/capture_pages.mjs --out <dir> [--base URL] [--pages all|cities|Name,Name] [--widths ...] [--themes light,dark] [--cdp N]   # one browser; --peak-gb 2.5
python scripts/prose_proposals.py collate | apply --ids <id,id> | --selftest   # lanes' prose proposals -> the owner's list
python scripts/proposals_page.py --out <html> --commit <sha> [--sets json]   # the owner's review page for a long proposals list
python scripts/python_memcap.py [--install|--check|--selftest]   # per-process memory cap; --install with each Python
python scripts/heavy_job.py run --label <job> [--peak-gb <N> --estimate <basis>] --session <you> [--wait <min>] -- <command>   # the heavy-job gate; `status` shows who holds memory
python scripts/archive_decisions.py [--dry-run]          # start of each week: older entries -> docs/decisions/
python scripts/merge_append_only.py DECISIONS.md [--dry-run]   # archived entries count as present
python scripts/push_docs.py [--dry-run]                  # a docs-only session's push ritual; refuses app/, outputs/, pipeline/
python scripts/staging_artifacts/leads_build.py <census page HTML>   # rebuild the private census's Hottest leads (README beside it)
python scripts/staging_artifacts/country_census.py      # per-country counts from the master list, read-only
python scripts/coverage_sweep/recount.py [--gaps-only]   # rail-city universe vs the master list (docs/coverage_sweep/); coarse, reads only
python scripts/coverage_sweep/parse_wiki_tram.py [--wiki PATH] [--out PATH]   # saved tram-list wikitext -> rows, for a new universe
python scripts/staged_cities_build.py                    # ranked unbuilt cities -> docs/staged_cities.json (pipeline env, cached N02/N03)
python scripts/stress_overview.py [--scenario now|six|eight|eight_osaka|pref] [--compete REGION] [--country-view COUNTRY] [--group "NAME=C1,C2"] [--keep DIR]   # the macro map with the staged cities added, in a temporary copy of app/
python scripts/scaffold_city.py --slug <slug> --name <Name> --system-name <system> --taxonomy <key> --lat <lat> --lon <lon> --region <region> --country <country> --mode <metro|light_rail|tram>   # add --dry-run first
.venv-lean/Scripts/python.exe -m streamlit run "app/Overview.py"
```

New since the move: `python scripts/regen_generated.py [--install]` after a
merge (generated files), `python scripts/merge_conflict_stats.py --since <date>`
and `python scripts/check_word_budgets.py [--report]`.
Authorship marks: `python scripts/fingerprint.py init|table|coverage|verify <file or URL>` (the key lives in `~/.ehm/`, never in the repo).
