# DECISIONS drafts - INSEE attribution on the five French pages (`france-insee-attribution`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - « Source : Insee » on Paris, Marseille, Toulouse, Lille and Rennes; check M refuses a French page without it

- **The five built French pages now display INSEE's prescribed credit.**
  `docs/licenses/france-licence-ouverte-2.0.md`, MUST DISPLAY 1: INSEE permits
  reuse « sous réserve de mentionner la source sous la forme « Source : Insee » »,
  the only prescribed string among the French sources, covering SIRENE and the
  geolocation file. All five pages named SIRENE and INSEE in prose and none
  carried the string; neither did `app/components.py`'s `_NOTICES`. Each page
  (`app/pages/21_Paris_Heatmap.py` to `25_Rennes_Heatmap.py`) gains, under its
  transit caption, the France batch's line: "Business data: Source : Insee,
  SIRENE (01 septembre 2026 edition) and its geolocation file." The edition
  is written the way the batch template renders it
  (`scripts/france_page.py` on `france-build`), so all French pages read
  alike.
- **The edition comes from the record of the shared cache, and is hardcoded in
  the page.** `outputs/<city>/provenance.json` does not record it for any of
  the five. `data/paris/raw/provenance.json`, written by the run that
  downloaded `data/france/raw/` on 2026-09-23 (file times match to the
  minute), records "Sirene : Fichier StockEtablissement - 01 septembre 2026"
  and "Fichier géolocalisation établissements - septembre 2026". All five
  configs import that national cache. The claim holds even for Paris, whose
  `data_age` says "fetched 2026-09-22": the stock resource is dated 09-01 and
  the geoloc 09-21, so any fetch from 09-21 to 09-30 got the same pair.
  Rejected: adding `sirene_etab_title` to the five outputs provenance files by
  hand. `fetch_sources.py` rewrites that file from scratch and records the
  SIRENE keys only when it downloads the parquet, which is why they are
  missing now, so the next run with a cached parquet would drop them again.
  Also rejected: a fetch-date wording, because the title names the edition
  directly. **Cost: the page line has to change with the next SIRENE
  refetch.** Each page's comment says so.
- **The line sits outside the provenance block, unlike the batch template.**
  Le Mans's template nests the INSEE caption inside
  `if PROVENANCE_JSON.exists(): try: ... if _taken:`, so a missing or
  malformed provenance file drops a licence obligation along with the transit
  snapshot. On the five built pages it is unconditional.
- **Check M added to `scripts/check_provenance.py`: a credit a licence
  prescribes word for word must be on every page of that country.**
  `PRESCRIBED_CREDITS` maps France to "Source : Insee" and its evidence. The
  check parses each page and accepts only a string literal passed to an `st.*`
  call, so a comment quoting the string (each of the five pages now has one)
  does not count. It accepts a no-break space before the colon. It fails when
  no city has the country, so it cannot pass by checking nothing. It already
  runs from `check_all.py` and at publish-city step 4, so it needed no new
  registration. Tested against the old pages (all five refused, by name) and
  synthetic pages (comment-only refused, no-break space accepted, Le Mans
  passes with a note). Rejected: a standalone French-only script, because the
  table is where the next prescribed string goes, whatever the country.
- **Owner call open, recommended: move the INSEE line out of the provenance
  block in the batch template** (`scripts/france_page.py`, and the generated
  pages 100-110 on `france-build`). Check M passes those pages but prints a
  note for each, "shows 'Source : Insee' only inside a conditional block". It
  is a note and not a failure so the batch is not held up by this branch. Once
  the template moves the line out, the note can become a failure.
- **Verified at 7bbab98.** `check_provenance.py` reported "All recorded",
  with check M OK for the five. `check_deploy_imports.py --ref 7bbab98` (run
  from the main checkout, because this worktree has no `.venv-lean`) reported
  PROBLEMS 0. A `deploy-verify` run (scope `map-chrome`) passed all five
  pages:
  - The caption reads verbatim, once, between the transit caption and the
    map. On Lille it follows the MEL/Ilévia provenance caption, because Lille
    has no "Transit data ©" line.
  - No exceptions; the maps render; the notices block is present.
  - `check_map_attribution.js` found the credit uncovered on Paris and
    Rennes at 1000x650, 1024x768 and 375x812.
  - Madrid, the control, was unchanged.

  **No reboot is needed for this change alone**: page files only, and no
  module Overview.py imports. At review time the reboot question is still
  computed from the whole push's `app/` diff.
