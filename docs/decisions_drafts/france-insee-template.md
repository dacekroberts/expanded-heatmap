# DECISIONS drafts - INSEE caption out of the provenance block (`france-insee-template`, cut from `france-build-2`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - The France page template shows « Source : Insee » unconditionally (owner)

- **The INSEE caption moved out of the provenance block in
  `scripts/france_page.py` and in the twenty pages it generated (100-119),
  on the owner's call.** The template nested it inside
  `if PROVENANCE_JSON.exists(): try: ... if _taken:`, so a missing or
  malformed provenance file, or one without `fetched_utc`, dropped INSEE's
  prescribed credit along with the transit snapshot
  (`docs/licenses/france-licence-ouverte-2.0.md`, MUST DISPLAY 1). Only the
  edition depends on that file. `_edition` now starts empty and is read
  right after the file loads. The caption runs after the block, so without
  provenance it reads "Business data: Source : Insee, SIRENE and its
  geolocation file." The visible text with provenance is unchanged.
  Rejected: a second, stripped-down caption in the `except` branch, which
  would still miss the no-file and no-`fetched_utc` cases.
- **The pages were patched with the same exact-match edit, not regenerated.**
  `france_page.py --write` rebuilds the prose from each city's build data,
  so a regeneration could move other sentences. The edit matched exactly
  once in the template and in every page. Afterwards each page's block reads
  line for line as the template's, apart from the city's transit credit.
- **Verified.** The template and all twenty pages compile. Check M (from
  `france-insee-attribution`) prints no nesting note for pages 100-119.
  Le Mans run headless under the lean venv (streamlit AppTest, page links
  stubbed) showed the caption with provenance ("(01 septembre 2026
  edition)") and without it (edition omitted). `deploy-verify` is left to
  the landing group's `city-added` run at review time.
- **Check M's note can now become a failure**, since no French page nests
  the credit any more. That is a change to `france-insee-attribution`,
  queued for the owner.
