"""Every check that passes or fails, in one run - what the pre-push hook calls.

    python scripts/check_all.py          # run them all, in parallel
    python scripts/check_all.py --list   # name them and exit

Exits non-zero if any check fails, printing that check's own output. Offline:
every check runs under HEATMAP_NO_NETWORK=1. Wired as `.githooks/pre-push`
(enable once per clone with `git config core.hooksPath .githooks`).

WHY. None of the project's checks ran unless a session remembered to run it,
and a city landing needed five of them by name (docs/efficiency_review_2026-09-27.md,
finding 6). A hook is the only form of a rule that cannot be read past.

WHAT IS LEFT OUT, and why:
  - drift_check.py, check_deploy_imports.py: minutes each (a full re-render; a
    clean clone into a lean venv). Still manual gates, named in publish-city.
  - check_stray_downloads.py: it inspects EVERY checkout's root, so one
    session's stray file would block another session's push.
  - check_personal_exposure.py, check_worktree_data.py: take an argument.
  - check_plan_done.py, check_stale_claims.py: report only, never fail.
  - check_stray_bullets.py --all: docs the app does not render; a report.
  - the .js/.mjs checks: they need a browser and a running server.

It checks the working tree, not the commits being pushed. Push from a clean
tree and the two are the same.
"""
import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHECKS = [
    ["scripts/check_barred_marks.py"],
    ["scripts/check_barred_marks.py", "--selftest"],
    ["scripts/check_basemap_key.py"],
    ["scripts/check_category_continuity.py"],
    ["scripts/check_category_continuity.py", "--selftest"],
    ["scripts/check_city_registry.py"],
    ["scripts/check_conflict_markers.py"],
    ["scripts/check_conflict_markers_selftest.py"],
    ["scripts/check_discard_evidence.py"],
    ["scripts/check_html_lang.py"],
    ["scripts/check_html_lang.py", "--selftest"],
    ["scripts/check_word_budgets.py"],
    ["scripts/fingerprint.py", "coverage"],
    ["scripts/check_inconsistency_list.py"],
    ["scripts/check_inline_arrays.py"],
    ["scripts/check_macro_facts.py"],
    ["scripts/check_macro_labels.py"],
    ["scripts/check_line_identity.py"],
    ["scripts/check_map_markup.py"],
    ["scripts/check_master_list_counts.py"],
    ["scripts/check_master_list_counts_selftest.py"],
    ["scripts/check_no_em_dashes.py"],
    ["scripts/check_name_keys.py"],
    ["scripts/check_name_keys.py", "--selftest"],
    ["pipeline/name_keys.py", "--selftest"],
    ["scripts/check_internal_markers.py"],
    ["scripts/check_internal_markers.py", "--selftest"],
    ["scripts/check_city_page_format.py"],
    ["scripts/check_city_page_format.py", "--selftest"],
    ["scripts/check_no_fetch_in_steps.py"],
    ["scripts/check_no_fetch_in_steps_selftest.py"],
    ["scripts/check_overpass_hosts.py"],
    ["scripts/check_place_search.py"],
    ["scripts/check_place_search.py", "--selftest"],
    ["pipeline/place_index_fetch.py", "--selftest"],
    ["scripts/place_search_fetch_queue.py", "--selftest"],
    ["scripts/place_search_scaffold.py", "--selftest"],
    ["scripts/place_search_area_lookup.py", "--selftest"],
    ["scripts/place_search_night.py", "--selftest"],
    ["scripts/check_place_index_drift.py", "--selftest"],
    ["scripts/check_place_scope.py"],
    ["scripts/check_place_scope.py", "--selftest"],
    ["scripts/check_place_unopened.py"],
    ["scripts/check_place_unopened.py", "--selftest"],
    ["scripts/check_privacy_verdicts.py"],
    ["scripts/check_provenance.py"],
    ["scripts/check_render_current.py"],
    ["scripts/check_ring_shares.py"],
    ["scripts/check_scope_disclosure.py"],
    ["scripts/check_scope_disclosure_selftest.py"],
    ["scripts/check_stray_bullets.py"],
    ["scripts/check_stray_bullets_selftest.py"],
    ["scripts/check_theme_sync.py"],
    ["scripts/check_travel_packs.py"],
    ["scripts/decisions_index.py", "--check"],
    ["scripts/downstream_changes.py", "--selftest"],
    ["scripts/drift_check_selftest.py"],
    ["scripts/heavy_job.py", "--selftest"],
    ["scripts/python_memcap.py", "--check"],
    ["scripts/readme_cities.py", "--check"],
    ["scripts/rendered_surfaces.py", "--check"],
    ["scripts/prose_proposals.py", "--selftest"],
    ["scripts/proposals_page.py", "--selftest"],
    ["scripts/commercial_use_sources.py", "--selftest"],
    ["scripts/commercial_use_quote_check.py", "--selftest"],
    ["scripts/licence_renderings.py"],
    ["scripts/licence_renderings.py", "--selftest"],
    ["scripts/archive_decisions_selftest.py"],
    ["scripts/rule_breaks.py", "--selftest"],
    ["scripts/place_name_net.py", "--selftest"],
]


def run(argv):
    # Drop git's hook variables (GIT_DIR, GIT_INDEX_FILE, ...): as the pre-push
    # hook they point at the real repository, and a check that builds a
    # throwaway repo would write to ours instead. On 2026-09-27 that flipped
    # core.bare to true and overwrote user.name in the shared .git/config. Each
    # check runs with cwd=ROOT, so git still finds this repository on its own.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(HEATMAP_NO_NETWORK="1", PYTHONIOENCODING="utf-8")
    start = time.monotonic()
    proc = subprocess.run([sys.executable, *argv], cwd=ROOT, env=env,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    return argv, proc.returncode, time.monotonic() - start, proc.stdout + proc.stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--list", action="store_true", help="name the checks and exit")
    ap.add_argument("--only", nargs="+", metavar="TEXT",
                    help="run only the checks whose command line holds one of these texts; "
                         "never the pre-push gate, which runs them all")
    args = ap.parse_args()
    if args.list:
        for argv in CHECKS:
            print(" ".join(argv))
        return 0
    checks = CHECKS
    if args.only:
        # For a session writing one script (its own selftest, the em-dash
        # check) while others run the suite: under four concurrent suites
        # single checks took 140 s (2026-10-12). A text that matches nothing
        # is an error, so a typo cannot read as a pass.
        unmatched = [t for t in args.only if not any(t in " ".join(c) for c in CHECKS)]
        if unmatched:
            print(f"--only: no check's command line holds {unmatched}; --list names them")
            return 1
        checks = [c for c in CHECKS if any(t in " ".join(c) for t in args.only)]

    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as pool:
        results = list(pool.map(run, checks))

    failed = []
    for argv, rc, secs, out in results:
        last = (out.strip().splitlines() or [""])[-1][:80]
        print(f"{'ok  ' if rc == 0 else 'FAIL'} {secs:5.1f}s  {' '.join(argv):48} {last}")
        if rc != 0:
            failed.append((argv, out))

    for argv, out in failed:
        print(f"\n--- {' '.join(argv)} ---")
        print("\n".join(out.strip().splitlines()[-25:]))

    print(f"\n{len(checks) - len(failed)} of {len(checks)} checks passed "
          f"in {time.monotonic() - start:.1f}s."
          + (f" PARTIAL RUN: {len(CHECKS) - len(checks)} checks not run (--only)." if args.only else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
