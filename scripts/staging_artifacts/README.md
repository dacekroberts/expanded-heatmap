# Staging's private artifacts: the master list page and the country census

Tooling for two private pages the owner reads on claude.ai, never for the
site. Neither page is in the repo: the published artifact is the source of
truth, and each update starts from it.

| Page | Link | What it shows |
|---|---|---|
| City master list | https://claude.ai/artifact/LTzi7Vj5emzHnb3zAZy4Vn | The bands, Band R, the open gap, the pre-verdicts, the commuter-rail tier, next actions |
| Country census | https://claude.ai/artifact/CKCadsYtUhbWwWKzV9sDeD | Every country by coverage state, the watch categories, Hottest leads, how far the screen has come |

**To update either page:**
1. Read it with the Artifact tool (`action: "read"`, the link above). For the
   owner's own artifact the result names the saved file holding the full page.
2. Edit that file: the counts come from `docs/city_master_list.md` (its
   generated summary rows), never from memory.
3. For the census, rebuild Hottest leads from the master list:
   `python scripts/staging_artifacts/leads_build.py <saved census file>`.
   It rewrites only the block between the page's `leads` markers; one-line
   notes per city live in `leads_notes.json` beside it, and a city without one
   shows its master-list cell cut at the first clause.
4. Publish with the Artifact tool, passing the same link as `url`, so the
   link the owner has keeps working.

`country_census.py` prints each country's built, candidate, Band R and discard
counts from the master list (read-only), the input for the census's country
groups. The untouched and no-rail groups are a desk census, not master-list
data: edit them on the page.

**Rules:** both pages are private; anything that would mislead if shared
(imitating a real organization, a person's details) never goes on them. The
master list wins over either page when they disagree.
