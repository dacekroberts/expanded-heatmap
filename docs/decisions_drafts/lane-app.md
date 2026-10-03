# DECISIONS drafts - lane-app (`lane-app`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - Check C checks both directions with no exemption; New York's notice 5 displayed (owner-approved batch)

- **The gap:** check C already failed a numbered notice no `_NOTICES` entry
  carried, but `NOT_DISPLAYED` exempted New York's 5 as "met by the About the
  Data and What Is Excluded pages", so a numbered notice the site did not
  display passed.
- **The fix:** `check_notice_bijection()` holds both directions with no
  exemption list. Its four cases (complete, a numbered notice displayed
  nowhere, a displayed notice not numbered, a displayed notice under another
  publisher's number) run before every check and alone with `--selftest`.
  `check_all.py` is not this lane's file, so the cases ride on the run it
  already makes.
- **Notice 5 displayed** on New York's page and the Required notices page, in
  this project's own words: the Technical Standards Manual reserves the
  right to require source, version and modifications, and prescribes no
  sentence. Version is the fetch date the city entry records (2026-09-21).
