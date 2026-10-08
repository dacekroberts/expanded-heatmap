# Rule history

How each rule in `CLAUDE.md` was learned. This text was moved **verbatim** out
of `CLAUDE.md` on 2026-09-27, when that file was cut from 4,345 words to its
current short form (docs/efficiency_review_2026-09-27.md, finding 3 and
change 3). Each section below is the rule's full original wording, so the story
reads in context; `CLAUDE.md` holds the operative version and links here with
`[#anchor]`. Anchors are stable - rename a heading freely, never an anchor.

Read a section before relaxing or rewording its rule, not before obeying it.
When a rule gains a new incident, add it to `DECISIONS.md` as usual; add it here
only if the rule's short form in `CLAUDE.md` changes because of it.

## Where to start (skill and doc pointers)

<a id="master-list"></a>
### Picking the next city

**Picking the next city? `docs/city_master_list.md`** is the current global
list - candidates banded by what is actually stopping each one, plus the built
cities and the discards with their evidence. It is current state, rewritten as
things change, so **read the counts off that file rather than from here** -
this pointer has gone stale twice by repeating them. `docs/global_country_shortlist.md` is the **evidence trail**
behind it (87 countries, every probe logged); when the two disagree the trail
wins and the list is stale.

<a id="add-country"></a>
### First city in a new country

**Adding a city in a country this project has never built in? Start with
`add-country`** (`.claude/skills/add-country/`) - the national facts that
disqualify every city at once, profiled once instead of per city. Canada is the
worked example; `docs/canada_retrospective.md` is what it cost.
**Three countries have been profiled to that depth and each cost something
different, so read the pair that matches the shape you expect**:
`docs/mexico_retrospective.md` (one national register, bespoke rail - the
second city was cheap) and `docs/spain_retrospective.md` (bespoke per city -
the second city shared a country with the first and almost nothing else).
Spain's is also the one to read before betting on a country because its
language or classification system looks familiar: that reasoning was used to
pick it, and it was half wrong.

<a id="add-city"></a><a id="multi-source"></a>
### Adding a city, build briefs, and multi-source cities

**Adding a city? Use the `add-city` skill** (`.claude/skills/add-city/`) -
the process the built cities actually followed - and the `scaffold-city` skill
(`scripts/scaffold_city.py`) to generate its config, map script, page and
`cities.py` entry once Step 0 passes. **If one registry does not cover all
three buckets, use `multi-source-city`** - most large US cities do not license
general retail, so this is the common case rather than the exception (New York
needed four sources; Philadelphia's is 79% landlord registrations).

**Check `docs/build_briefs/<city>.md` first** - if one exists, Step 0's answers
are already banked there (endpoints, columns, CRS, traps, required notices, and
an explicit list of what is still unknown). It is a cache, not a prerequisite:
no brief means `add-city` Step 0 as usual, never waiting for one.

<a id="brief-check"></a>
### Run brief_check.py before any code

**Then run `python scripts/brief_check.py <city>` before writing any code for
it.** A brief caches Step 0's mistakes as confidently as its findings: Edmonton
inherited three wrong claims from its own, each an HTTP call from being caught,
and the MEASURED/ASSERTED labels did not prevent it - by the time a brief
*recommends* something, the label has been reasoned away. The checks live in a
fenced ```brief-checks block beside the prose, so writing a claim and writing
its test are one act. A failing check is a brief to correct, never a check to
relax. If a brief has no checks block, add one for the claims you rely on.

<a id="premises-taxonomy"></a>
### Non-NAICS classification

**The city's classification is not NAICS? Use `premises-taxonomy`**
(`.claude/skills/premises-taxonomy/`) - four cities have needed a local
taxonomy and the deciding measurement is the same every time and skipped every
time: **the catch-all share at each level of the scheme.** Barcelona's group
level puts 35% of active rows in `Altres` and its finest level 2.6%, so it keys
at the finest; Madrid keys near the top of an identically-shaped scheme. Both
are right, which is why there is no default to inherit - measure it with
`brief_check.py`'s `taxonomy_catchall` kind before writing the module.

<a id="address-join"></a>
### Addresses without coordinates

**Does the register have addresses but no coordinates? Use `address-join`**
(`.claude/skills/address-join/`) **before writing any geocoder.** Prague,
Copenhagen, Brazil and Taiwan each looked like a geocoding project and each
turned out to publish an address file that already carries the coordinate,
so the work became a join measured against a control city - or nothing.
Japan is the next one through it. **Hong Kong joined that list too:** its
publisher carried a point per licence on a second portal, found while reading
the geocoder's terms.

<a id="cjk-text"></a>
### Chinese, Japanese and Korean text

**Does the city's data carry Chinese, Japanese or Korean text? Use `cjk-text`**
(`.claude/skills/cjk-text/`) - Hong Kong, the Taiwanese cities, Seoul and
Japan. Hong Kong met all of it at once: Windows consoles crashing on a name,
a BOM in the first header, a bilingual OSM `name`, a privacy heuristic whose
zero means nothing on CJK names, and a font order that draws Chinese in
Japanese glyph forms.

<a id="reprobe-city"></a>
### Re-probing a thin city

**Re-probing a city the screen left thin - an open-gap row, or a one-bucket
city in Band C? Use `reprobe-city`** (`.claude/skills/reprobe-city/`).
Amsterdam went from discard to Band A in one evening on probes the first
screen never ran: the city's own host, its whole catalogue, the scope on a
403, and a second layer in a different shape (a building register's use
class), with that shape's defect measured before the owner was asked.

<a id="country-skills"></a>
### Brazilian and Taiwanese cities

**Building a Brazilian city? Use `brazil-city`** (`.claude/skills/brazil-city/`).
São Paulo built the national CNEFE modules - the free-text classifier, the
reader with its dwelling rule, the município boundaries - so a further city
adds a config, its rail step and three thin steps. The skill carries the
traps São Paulo paid for (a keyword added to the wrong rule list re-routed 238
classified rows; a sample cannot measure the words chosen from it) and the
rail test the owner applies to commuter lines, which
`scripts/measure_rail_backbone.py` half-answers from cached OSM.

**Building a Taiwanese city? Use `taiwan-city`** (`.claude/skills/taiwan-city/`).
Taichung built the national modules (`pipeline/countries/taiwan.py`: the tax
register, the door-plate join, the owner's name and head-office rules), so a
further city adds a config, a door-plate file and its rail leg. The join's
parser has a control - Taipei - and the skill carries the trap Taichung paid
for: a door-plate file that names districts by code while one street name
recurs in several districts.

<a id="osm-rail"></a>
### Rail from OpenStreetMap

**Is the city's rail coming from OpenStreetMap rather than GTFS? Use
`osm-rail`** (`.claude/skills/osm-rail/`). Mexico City and Guadalajara both
needed it - one because every agency host is unreachable, one because the only
feed expired in 2023 and predates a line that now carries passengers - and most
of the remaining shortlist (Taipei, São Paulo, Israel) is not GTFS either. It
also carries the meta-rule that skill exists for: **a lesson written in the
previous city's config does not reach the next city.** Mexico City's config
warns in capitals never to match stations on a network label; Guadalajara's
first query did exactly that and lost a whole line. Put a lesson where the next
city must pass through it - a raising check in shared code, then a skill - not
in a sibling city's comments.

<a id="map-view"></a>
### Map opens at the wrong zoom

**A map opened at the wrong zoom? Use `map-view`** (`.claude/skills/map-view/`).
It happened three times - Edmonton, Paris, Lille - each fixed where it broke,
until a guard in the shared fit script started checking the OUTCOME instead.
`scripts/check_map_view.js` verifies a map's view by reading the map object,
never a screenshot, and on the live app as well as locally.

<a id="session-roles"></a>
### More than one session

**More than one session working at once? Read `docs/session_roles.md`** - which
paths each role owns, and the worktree-per-session split that keeps them from
colliding. A single session does all of it and can ignore that file.

<a id="consistency-sweep"></a>
### Auditing rather than building

**Auditing rather than building? Use `consistency-sweep`**
(`.claude/skills/consistency-sweep/`) - the cleanup role. It sweeps for what
the forward-facing sessions leave behind: prose still written in the future
tense about a present that arrived, hand-kept counts that drifted, references
broken by renumbering, sources in use whose terms were never read, tables that
stopped rendering, branches and worktrees outliving their work. **Its preferred
output is a check rather than a correction**, which is why it owns
`scripts/check_*.py` - `check_provenance.py` was written to close one gap a
reader had already found and immediately found five more.

## Invariants

<a id="live-verify"></a>
### Live-verify the schema

- **Live-verify a city's real data schema before writing any pipeline code
  for it.** Dataset titles and search summaries are not evidence (Denver and
  San Jose both looked viable and had no usable data). See `add-city` Step 0.

<a id="wording"></a>
### Rules whose wording was only tightened

- **Map rendering is shared:** `pipeline/map_common.py`'s
  `render_heatmap()`. City `step3_map.py` files are thin and must not fork
  it. It never names a taxonomy - category grouping, tooltip label and
  legend text come from the taxonomy module.

- **A city's classification need not be NAICS.** A documented local taxonomy
  is fine: see `pipeline/taxonomies/`. Step 2 filters via
  `filter_to_storefront()`, never NAICS prefixes directly.

<a id="line-identity"></a>
### One colour and one name per line, site-wide

**A line drawn on more than one map has one colour and one name everywhere.**
The large review of 2026-10-07 found the JR Kobe Line in five colours across
Kansai, the JR Sanyo Line in four, and the Seibu Haijima Line cyan on two maps
and mauve on a third; a reader moving between neighbouring maps saw one line
change colour. The owner made it a hard line ("any line represented more than
once in city maps gets its own distinct color, even if that means reassigning
other lines' colors to fit"). 48 Japanese lines were unified onto
`pipeline/line_registry.py`, keyed by operator and line rather than display
name ("Tram 1" in Amsterdam and Antwerp are different lines), and
`scripts/check_line_identity.py` fails a line with two colours, and different
lines that meet on neighbouring maps, except the registry's recorded
exceptions. The same review unified the names ("JR Hohi Main Line" on
Kumamoto's map as on Ōita's). The CIE76 20 floor from the pins came with the
olive and violet pin colours, when 32 lines sat closer than that.

<a id="rail-shape"></a>
### Check the rail system's shape

- **Check the rail system's shape before assuming "keep every station."**
  Central-corridor-plus-surface-offshoot systems (San Francisco's Muni
  Metro) need `docs/sub_transit_line_filters.md`; uniformly sparse ones (San
  Diego) don't.

<a id="personal-info"></a>
### Public commercial information, not personal information

- **Publish public commercial information, not personal information.** A trade
  name is fair game; a registrant's own name at what looks like their home is
  not, even from a public registry. Run
  `python scripts/check_personal_exposure.py <city>` before publishing a city
  and after any change to its step 2 or taxonomy, and record the verdict in
  `DECISIONS.md`. Catch-all classification codes are the usual culprit (Los
  Angeles excludes NAICS 812990 for this reason).

<a id="attribution"></a>
### Basemap attribution and required notices

- **Never remove the basemap attribution.** Every rendered map carries
  `© OpenStreetMap contributors` linked to the OSM copyright page; ODbL 1.0
  requires it to stay visible, not hidden behind UI or a toggle. Changing tile
  provider swaps that attribution for the new provider's - it never just
  disappears. **"Visible" is a fact about the RENDER, not about the file**, and
  the two came apart on 2026-09-23: the legend covered the credit completely in
  all 23 cities at any viewport taller than the map, while every map still
  contained it. The published site was compliant only because
  `app/pages/*.py` embeds at exactly the map's own height, clearing it by 10px.
  `scripts/check_provenance.py` (check K) now refuses a map whose legend is not
  clamped against the map's bottom edge, and `scripts/check_map_attribution.js`
  hit-tests a real render at several viewport heights - **run it at more than
  one height, because a single height is what hid this for the life of the
  project.** Three other sources also require specific notices once the site
  is public (Chicago, SFMTA, LA Metro): the exact wording is in
  `docs/data_sources.md`, "Notices this project MUST display when published",
  and those are obligations rather than courtesies.

<a id="no-fetch"></a>
### A pipeline step never fetches

- **A pipeline step never fetches. Downloading lives in
  `pipeline/<city>/fetch_sources.py`**, deliberately not named `step*.py` so
  `drift_check.py` never runs it; the step reads the cache and exits non-zero
  naming that script when it is missing. A cache-guarded download inside a
  step is offline only on a machine that has already run it, so on a fresh
  checkout a drift check silently asks "does the CURRENT UPSTREAM still
  produce the committed output" instead of "does the COMMITTED CODE" - and
  Toronto proved that is not a pedantic difference, producing a map missing a
  storefront while the row-count baseline reported identical. `python
  scripts/check_no_fetch_in_steps.py` decides this, **including through a
  shared `pipeline/*.py` module**, which is how three `step3_geocode.py` files
  turned out to fetch via `census_geocoder.py` without importing an HTTP
  client themselves. Until 2026-10-02 it read only `pipeline/*.py`, one level
  deep; the Seattle (Regional) build found that a helper in a city's own
  folder (`pipeline/seattle/lcb_offpremise.py`) went unread, so it now follows
  a step's imports transitively into every module under `pipeline/`, and the
  one exception is an HTTP import fenced inside a module-level `fetch()` that
  nothing a step reaches calls.

<a id="offline-guard"></a>
### A drift check may never fetch

- **Where a step genuinely cannot stop fetching, guard the drift check instead
  of pretending.** `census_geocoder.py` POSTs a batch of addresses the step
  computes, so there is no URL to hoist into a fetch script. The rule that
  matters is narrower than "a step never fetches": **a step may fetch when a
  person runs it; a drift check may never fetch.** `pipeline/offline.py` is
  that boundary - `drift_check.py` sets `HEATMAP_NO_NETWORK` around every step
  and `refuse_if_offline()` raises rather than requesting. Use it for the next
  such case rather than widening the exception list. `HEATMAP_NO_NETWORK=1
  python pipeline/<city>/step2_clean_businesses.py` also answers "would this
  work on a fresh checkout?" without unplugging anything.

<a id="provenance"></a>
### check_provenance.py after adding a city

- **Run `python scripts/check_provenance.py` after adding a city, and make it
  name that city OK.** `docs/data_sources.md` is the only way a build can be
  reproduced, and the rule to record a city's sources there was followed for
  the US cities and silently skipped for every city that arrived through a
  country profile - Canada's for a day, Mexico's until a script looked.
  The gap is invisible by construction: **a city whose provenance is unrecorded
  looks exactly like a city that was checked**, which is why this is a script
  and not another paragraph. It also checks the notices list against
  `app/components.py`'s `_NOTICES`, which had two item 8s and two item 15s.
  A city under `KNOWN_GAPS` in that script is a dated defect, not a pass.

<a id="scope-twice"></a>
### A city is scoped twice

- **A city is scoped TWICE, and both halves have to reach the reader.** Which
  rail network its map is drawn around is as deliberate as which businesses are
  counted near it, and until 2026-09-23 only the second half was published:
  `docs/excluded_categories.md` was entirely about businesses while commuter
  rail was excluded in every city, silently. The question that exposed it was a
  reader's - "is BART in the San Francisco build?" - and the answer had been
  recorded in `DECISIONS.md` for days. `python
  scripts/check_scope_disclosure.py` decides this: every city in `cities.py`
  must be named in the business half of that document, the station-scope
  section must still exist, and every city's `outputs/<slug>/` must resolve so
  the generated station table has no silently empty row. The same run found
  five cities - Montréal, Madrid, Barcelona, Dublin, Milan - whose business
  exclusions had never been written there at all, each disclosed on its own
  city page and nowhere else.

<a id="support-sources"></a>
### Supporting sources need a row

- **A source that is not a registry, a feed or a boundary still needs a row.**
  The naming layer that says which municipality an excluded station is in, the
  parcel or assessor layer a residence filter joins to, a geocoder. These are
  usually published by a county, a province or a state rather than by the city,
  so they carry their own licence and sometimes their own required notice - the
  Province of British Columbia's is notice 17, and it was missed for a day
  because no per-city checklist had a slot for it.

<a id="licence"></a>
### Record a new source's licence

- **Record a new data source's licence when you add it**, in
  `docs/data_sources.md`, using the **`read-licence` skill**. A government
  open-data portal is a reason to expect permissive terms, not evidence of
  them: LA Metro's GTFS forbids modifying its data while LA's business registry
  is CC0, and New York City's datasets declare no licence at all. The skill
  exists because every licence correction in this project came from not opening
  a page an earlier review had merely cited - and the step most easily skipped
  is checking what a dataset page incorporates **by reference**, which is how
  Philadelphia's prohibition hid behind a licence that forbids nothing.

<a id="removal"></a>
### Removal requests

- **A removal request is honoured, not argued** - from a data publisher, a
  business owner, or anyone raising a privacy concern about a specific pin.
  Take it down first (the layer, or the whole city, as the request requires),
  then record what was removed and who asked in `DECISIONS.md`. Do not ask the
  requester to justify themselves, and do not weigh it against the fact that
  the licence review found nothing forbidding what is published: being
  permitted to display something is not a reason to insist on it. The standing
  commitment is published in `docs/data_sources.md` and
  `docs/excluded_categories.md` - keep those two consistent with each other.

## Working rules

<a id="decisions"></a>
### Log every judgment call

- **Log every judgment call in `DECISIONS.md`** as it's made (the
  `decisions-entry` skill has the format). Never edit an old entry; add a
  new one, then run `python scripts/decisions_index.py` to refresh the
  generated index at the top. That file is 100 entries and ~57k words, and
  `drift_check.py` ends by telling you to find "the latest baseline entry" in
  it - the index is how. `--check` fails if it is stale. Keep
  `docs/project_context.md` to current state, no counts.
- **Since 2026-09-30, build sessions write drafts, and only cleanup writes
  `DECISIONS.md` (owner).** Every branch appended to the same file, so every
  landing batch began with a DECISIONS conflict per branch. That day one was
  committed with its conflict markers in: `merge_append_only.py` hit a
  Windows file lock (Errno 22), and the merge went through anyway. None of
  the 26 checks looked for markers. One drafts file per session
  (`docs/decisions_drafts/`) never conflicts, and one fold by cleanup
  replaces a merge per branch.

<a id="drift-churn"></a>
### Drift check churn in outputs/

- **Run `python pipeline/drift_check.py` after any pipeline change** - then
  **`git checkout -- outputs/` if it leaves files modified but reported no
  drift.** On Windows the regenerated files come back CRLF while the committed
  ones are LF (`.gitattributes` sets `* text=auto eol=lf`), and Folium assigns
  fresh random element ids on every render, so `git status` shows changed
  `outputs/` files after a run that said "zero drift". Verified 2026-09-22:
  three CSVs differed **only** in line endings and three `heatmap.html` files
  showed exactly 6,062 insertions against 6,062 deletions. Committing that
  churn would rewrite files the deployed app reads for no change at all - and
  it is a second reason never to `git add -A`.

<a id="deploy-reboot"></a>
### check_deploy_imports.py and the reboot

- **Run `python scripts/check_deploy_imports.py` before any push that touches
  `app/`**, and **reboot the deployed app after any push that changes a module
  it imports** - `app/cities.py` changes with every city. Streamlit Cloud's
  "Updated app!" re-runs the entry script and leaves imported modules cached,
  so the live site stayed down for over three hours on 2026-09-22 across five
  pulls. Gate item 9 in `docs/data_sources.md` has the detail. `deploy-verify`
  cannot catch either failure: it runs the working tree, and it always starts a
  fresh process.

<a id="publish-city"></a>
### Publishing a city

- **Publishing a city? Use `publish-city`** (`.claude/skills/publish-city/`) -
  the eleven-step gate in order, what each step sees that no other does, and
  the two invisible ones: landing `app/` on master IS deploying, and the reboot
  question must be computed from the WHOLE push's `app/` diff rather than from
  the last few commits, which is how `deploy-verify` can correctly report "no
  reboot needed" about a push that needs one.

<a id="licence-read"></a>
### The licence-read agent

- **Reading a source's terms? The `licence-read` agent** (`.claude/agents/`)
  runs `read-licence` on ONE source and returns a verdict in four shapes, out
  of the main conversation - most of the pages it opens say nothing, and Spain
  alone cost more licence reading than the nine US cities combined.

<a id="deploy-verify"></a>
### The deploy-verify agent and its scopes

- **Verify app changes with the `deploy-verify` agent**, and **always state a
  scope**: `city-added`, `map-chrome`, `app-deps` or `full`. It runs against
  `.venv-lean` (what Streamlit Cloud installs), not the full environment. A
  full sweep costs ~186k tokens and ~27 minutes, so it is reserved for
  before a real deploy, or for clearing a backlog of unverified changes in one
  batch. Skip it entirely for pipeline-only work (taxonomies, step 2 filters,
  exclusions) and doc edits - `drift_check.py`, a grep of `app/` for
  folium/geopandas/shapely/pyproj imports, and one browser render cover those.

<a id="scratch"></a>
### Probe and scratch output

- **Write probe and scratch output to the session scratchpad directory, never
  to the working directory or the home directory.** Step 0 research is mostly
  `curl`/`requests` dumps, and `-o la.json` with no path writes wherever the
  shell happens to be. The 2026-09-18 city screening left eight such files
  (`la.json`, `phila_sample.json`, a saved 404, a 283 KB saved HTML page, a
  file named `.json` that was HTML) sitting in the home directory until
  2026-09-21. Give every probe an explicit path under the scratchpad, or under
  a gitignored `data/<city>/raw/`. Nothing in this category is ever committed:
  the findings belong in `docs/data_sources.md` and `docs/city_shortlist.md`,
  which is where they can be trusted and the raw capture cannot.

<a id="no-escapes"></a>
### No backslash or backtick in a Bash command

- **A backslash or a backtick never goes into a Bash command. Write the
  content to a file with the Write tool and run the file.** A `PreToolUse`
  hook now refuses the combination outright - `.claude/hooks/block_heredoc.py`,
  wired up in `.claude/settings.json` - so this is enforced rather than
  remembered.

  **The rule used to say "write multi-line text with the Write tool", and that
  framing is what let it fail a fourth time.** Two corrections, both learned
  the hard way on 2026-09-22:

  - **It is about ESCAPES, not length.** A one-line regex probe does not feel
    like "multi-line text", so the rule read as not applying. It applied.
    `re.findall(r'Use[s]?:\\s*([^<\\\\]{0,60})', t)` inside a heredoc arrived as
    `[^<\\]` - an unterminated character set.
  - **Quoting the delimiter does NOT save you.** `<<'PYEOF'` should stop shell
    expansion, and the mangling happened anyway, because the rewriting is not
    bash's. Nothing in the old rule said this, so the quoted form looked safe.

  The earlier three, same day: an f-string broken in generated code, every
  backticked phrase silently emptied from a commit message, and a `\n` turned
  into a literal newline mid-string. Four occurrences against a rule that was
  already written down is the argument for a hook: **a lesson in the log
  describes what happened once, a working rule is in hand at the moment of
  typing, and a check is the only one of the three that cannot be read past.**
  Same reasoning as `osm-rail`'s opening section, which exists because a
  warning in one city's config did not reach the next city.

  The guard is deliberately narrow - a heredoc or `-c`/`-e` string AND a
  backslash or backtick. A plain `grep "\.py$"` and every Windows path in this
  repository are untouched, because a guard that cries wolf gets disabled.

  **Narrowed to match the hook, 2026-10-06 (owner, staging's call 94).**
  The rule's first line forbade a backslash in ANY Bash command, while the
  hook enforced only the intersection above, so plain `sed` and `grep`
  escapes passed every day without harm: two city-probe agents and
  Cleanup's own edits that day, all landed intact. A session reading the
  rule took the gap for a broken hook. The wording now says what is
  enforced, plus a backtick inside a double-quoted argument, which the
  shell itself runs as a command.

<a id="fetch-before-push"></a>
### Re-check origin/master at the push

- **Re-check `origin/master` in the same breath as the push, not once at the
  start of the gate.** The pre-deploy checks take minutes - a full
  `drift_check.py --jobs 4` alone re-runs every city - and with several
  sessions live that is long enough for origin to move underneath a tree that
  was up to date when the sweep began. On 2026-09-23 one push needed **two**
  merges: origin gained four commits before the sweep and one more between the
  sweep finishing and `git push`. Neither was a problem, because both were
  caught by `git fetch` immediately before pushing; the failure mode is
  pushing on the strength of a freshness check that has gone stale, getting a
  rejection, and resolving it in a hurry - which is how an append-only file
  gets rebuilt from one side instead of merged. So: `git fetch`, then merge if
  behind, then push, with nothing slow in between. If a gate has to re-run
  after that merge, re-fetch after it too.

<a id="merge-append-only"></a>
### Conflicted append-only files

- **Resolve a conflicted append-only file with
  `python scripts/merge_append_only.py DECISIONS.md`, never by rebuilding it
  from one side.** Two sessions both append to the top of `DECISIONS.md`, so
  every master/staging merge conflicts there and the conflict is never a real
  disagreement. The tempting hand fix - take one side's file, re-append the
  other side's new entries - **silently deletes entries**, because *a conflict
  region shows where the two sides disagreed, not everything the other side
  added*. On 2026-09-22 staging's "Japan is a BUILD" entry sat lower in the
  file with no competing change beside it, so git auto-merged it outside the
  markers and rebuilding from master's stage would have dropped it; an hour
  later the France reversal arrived the same way, with the generated index as
  the *only* conflict. The script edits just the conflict regions of git's own
  merged file, dates each entry by the commit that introduced it so the two
  sides interleave by real time, and refuses to write unless the result equals
  the union of both sides' full stages. Run `scripts/decisions_index.py`
  afterwards.
- **A failed resolution must not be committed.** On 2026-09-30, on
  kitchener-waterloo, the script's write hit a Windows file lock (Errno 22),
  the merge was committed with its markers, and the pre-push hook passed it
  (fixed in 3d93d29). The script now retries once and then stops with a
  message saying the file still holds markers, and
  `scripts/check_conflict_markers.py` fails the hook on any marker in a
  tracked file.

<a id="memory"></a>
### The memory cap

- **Every Python process is capped at 8 GB, 12 GB with its children, and
  one drift check runs on the machine at a time.** On 2026-09-28 a licence
  agent's scratch script decoded a ward's PDF by hand, expanding every
  character range in its font tables into a dict entry and holding every
  stream at once. One `python.exe` reached 47 GB on a 16 GB machine (commit
  limit 29 GB). Windows logged "low virtual memory" at 11:59:37 and closed
  the Claude app a minute later; a second 47 GB process at 12:05:04 closed it
  again, with a four-job drift check, a census join and a `deploy-verify`
  in flight (which of them grew is unproven). Every session lost its turn and the desktop shell had to be
  restarted. `scripts/python_memcap.py`, installed as `usercustomize.py`,
  puts each process in a Windows job object, so a runaway gets a
  `MemoryError` of its own. `drift_check.py` takes an operating-system lock
  in the shared git directory, which dies with the process. The cap does
  not reach `.venv-lean`, which skips the user site.
- **Drift checks run `--jobs 2` at most, and only one heavy job runs at a
  time, announced to every live session.** Measured the same day: Oslo's
  step 2 peaks near 5.4 GB and Paris's step 1 near 2.4 GB, so four cities at
  once can pass the 12 GB tree cap by themselves. The cap stops one runaway;
  it cannot stop two capped jobs from filling the machine, so the
  announcement covers what the cap does not (`docs/session_roles.md`).
- **Since 2026-09-30, two heavy jobs at most, each admitted by
  `scripts/heavy_job.py` against MEASURED available memory (owner).** The
  owner allowed two concurrent jobs "under the memory thresholds". The first
  reading, two jobs whose declared peaks sum to 12 GB, was wrong the same
  hour: psutil showed 15.9 GB total, 2.3 GB available and 1.6 GB of page file
  in use. The apps alone (eight Claude sessions, a browser) held about 8 GB,
  and an orphaned `grep -o` over a licence page's text, its parent session
  gone, held 4.7 GB. So the gate reads available memory at admission,
  reserves what running jobs have yet to claim, keeps a 2 GB margin, and
  records each job's measured peak. The first two measured: France's SIRENE
  step 2 at 0.37 GB (estimated 1.5) and the Czech register control at
  0.37 GB (estimated 2.5), both streamed. A gate was chosen over a monitor
  because a monitor polls all day and reacts after the damage.
- **Since 2026-10-04, three heavy jobs at most (owner: "allow three heavy
  jobs since i have no other open processes").** Three build sessions had
  started at once (Korea, new cities, Belgium). The count was raised, not
  the margin: each job is still admitted against measured available memory
  with 2 GB to spare, and the measured peaks of that week were mostly under
  1.5 GB (a full render-only sweep 2.06 GB, a Japanese multi-city drift
  4.7 GB). The condition is the owner's: no other heavy programs open. If
  they return, `MAX_JOBS` goes back to 2.

## Session roles (`docs/session_roles.md`)

The sections below were moved **verbatim** out of `docs/session_roles.md` on
2026-10-04, when that file was cut to its 3,000-word budget (the third change
of `docs/efficiency_review_2026-10-04.md`). `docs/session_roles.md` holds the
operative rules and points here by anchor. Headings inside a moved section are
demoted so they nest under this one.

<a id="sr-why"></a>
### Why the session split exists

How concurrent Claude sessions divide this repo without colliding. Written
2026-09-21, after a period of two sessions sharing one working tree, which
cost an unreviewed commit (`38d4bd0` swept another session's uncommitted work
into a `git add -A`), an explicit-path staging discipline on every commit, and
several stretches where one session sat idle waiting for the other.

<a id="sr-cleanup"></a>
### The cleanup role's rules, as first written

- **Verify against `origin/master`, never the local tree.** It reports on other
  sessions' work, so it is the role most likely to be reading a stale checkout.
  On 2026-09-22 two of three findings relayed between sessions were stale rather
  than wrong — both described a file that had changed by 339 lines since the
  reporting session branched.

- **Its preferred output is a check, not a correction** — which is why it owns
  `scripts/check_*.py`. A correction fixes one instance; a check keeps finding
  the class after the session ends. `scripts/check_provenance.py` was written
  to close a gap a reader had already found by hand, and immediately found five
  more.

<a id="sr-registry"></a>
### The worktree registry as it stood on 2026-10-04

**The standing assignments** - current state, so update this when one changes:

| Role | Worktree | Branch |
|---|---|---|
| Staging / research | `.claude/worktrees/staging` | `worktree-staging` |
| Cleanup / audit | `.claude/worktrees/cleanup` | `worktree-cleanup` |
| France kit, then the France builds (2026-09-29 kit; builds approved 2026-09-30) | `.claude/worktrees/france-kit` | `worktree-france-kit` for docs, skills and scripts; `france-build` for the builds, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's |
| Czech kit (2026-09-30: `docs/handoff_czech_batch_2026-09-30.md`) | `.claude/worktrees/czech-kit` | `worktree-czech-kit`; `data/` and `.venv-lean` are junctions to the main checkout's |
| UK six builds (released 2026-10-02: `docs/handoff_uk_six_2026-10-01.md`; one lead session with agents; registered 2026-10-02) | `.claude/worktrees/uk-six` | `uk-six-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-02:** pages **156** Manchester (Regional), **157** Birmingham (Regional), **158** Edinburgh, **159** Sheffield, **160** Nottingham (Regional), **161** Blackpool (Regional) (staging's pre-assignment); notices **84-96**, assigned in build order and kept contiguous (`check_provenance.py` D): Manchester 84 (Food Standards Agency) and 85 (Ordnance Survey), 86 NaPTAN for all six, then each city's Food Standards Agency or Food Standards Scotland notice and its Ordnance Survey one where it places at centroids |
| Japan batch builds, twelve cities (released 2026-10-02: `docs/handoff_japan_batch_2026-10-02.md`; one lead session with agents; registered 2026-10-02) | `.claude/worktrees/japan-batch` | `japan-batch-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-02:** pages **162-173** as pre-assigned (Matsuyama 162, Toyama 163, Kumamoto 164, Fukui 165, Nagasaki 166, Utsunomiya 167, Kitakyushu 168, Sakai 169, Hakodate 170, Kagoshima 171, Okayama 172, Kōchi 173); notice numbers **97-108**, one per city in the same order (Matsuyama 97 ... Kōchi 108), each city's list, MHLW where used, and MLIT, as notices 50-56, 75 and 76; claimed after the UK six's 84-96 |
| Seattle (Regional), then Tbilisi (released 2026-10-02: `docs/handoff_seattle_tbilisi_2026-10-02.md`; one lead session, Tbilisi queued) | `.claude/worktrees/seattle-tbilisi` | `seattle-tbilisi-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's |
| Japan wave 2, fourteen cities (**LANDED 2026-10-03**, worktree removed and its handoff note deleted; released 2026-10-02; one lead session with agents; registered 2026-10-03) | `.claude/worktrees/japan-wave2` | `japan-wave2-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-03:** pages **176-189** as pre-assigned (Kawasaki 176, Yokosuka 177, Himeji 178, Nishinomiya 179, Takamatsu 180, Toyota 181, Yokkaichi 182, Ōtsu 183, Nara 184, Hamamatsu 185, Higashiōsaka 186, Kurume 187, Sasebo 188, Shimonoseki 189); notice numbers **115-128**, one per city in the same order (Kawasaki 115 ... Shimonoseki 128), each city's list, MHLW where used, and MLIT, as the Japan batch's 97-108 |
| Four extensions to built cities (**LANDED 2026-10-03**, worktree removed and its handoff note deleted; released 2026-10-02; one lead session; registered 2026-10-03) | `.claude/worktrees/extensions` | `extensions-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-03:** notices **129-136** as pre-assigned, taken in build order as the reads require them (Long Beach's, then New Westminster's, Coquitlam's and Burnaby's OGL statements); no new pages |
| Belgium builds, six pages (**LANDED 2026-10-04**, worktree and branch removed, its handoff note deleted; released 2026-10-03; one lead session with agents; registered 2026-10-04) | `.claude/worktrees/belgium` | `belgium-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-03:** pages **196-201** as pre-assigned (Brussels 196, Antwerp 197, Ghent 198, Charleroi 199, Liège 200, Brussels (Regional) 201); notices **144-152**, one per source as the handoff's table assigns them |
| Other cities: Liverpool (Regional), Tacoma, Mendoza (**LANDED 2026-10-04**, worktree and branch removed, its handoff note deleted; released 2026-10-03; one lead session with agents; registered 2026-10-03) | `.claude/worktrees/new-cities` | `new-cities-build`, no upstream, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-03:** pages **193** Mendoza, **194** Tacoma, **195** Liverpool (Regional); notices **141** Mendoza, **142** Tacoma, **143** Liverpool's Food Standards Agency notice; the Department for Transport, NaPTAN notice 86 reworded, no new notice |
| Korea sweep builds, Daejeon, Gwangju and Gimhae (**LANDED 2026-10-04**, worktree and branch removed, its handoff note deleted; released 2026-10-03; one lead session, sequential; registered 2026-10-03) | `.claude/worktrees/korea-sweep` | `korea-sweep-build`, never pushed to master (app/ lands at review time); `data/` and `.venv-lean` are junctions to the main checkout's. **Claimed 2026-10-03:** pages **190** Daejeon, **191** Gwangju, **192** Gimhae (staging's pre-assignment); no notices (SEMAS's 68 covers all three) |
| Tram kit, the ten other T1 cities (2026-09-30: `docs/handoff_tram_kit_2026-09-30.md`; holding before builds) | `.claude/worktrees/tram-kit` | `worktree-tram-kit`; `data/` and `.venv-lean` are junctions to the main checkout's |
| Build `<city>` | `.claude/worktrees/<city>` | `<city>-build` - the name every build since Dublin has actually used, rather than the `worktree-<role>` form above. Delete the branch when the worktree goes: merged build branches have tended to outlive their worktrees |

<a id="sr-cleanup-move"></a>
### The cleanup role's move to its own worktree (2026-09-23)

**The cleanup role is moving to its row.** Until 2026-09-23 it ran in
`.claude/worktrees/practical-leakey-12a8a2` on `claude/practical-leakey-12a8a2`
- a name the desktop app generates for a session it expects to be short-lived.
That session became the standing role and never got a proper home. The next
cleanup session starts in `.claude/worktrees/cleanup`, created from `master`
with the command above, and the old one is **retired rather than moved**:
Windows refuses to move a directory a running process is using, and a session's
scratchpad and transcript are keyed to its worktree's path. Retire it by
closing that session, then, from the main checkout:

```bash
git pull --ff-only
git worktree remove .claude/worktrees/practical-leakey-12a8a2
git branch -d claude/practical-leakey-12a8a2
```

`-d`, never `-D`: it refuses to delete a branch holding commits that are not in
the branch you are on - `master`, from the main checkout - which makes the
deletion its own check. **Hence the pull first.** The branch has no upstream,
so `-d` compares it with the main checkout's LOCAL `master`, which is often
behind GitHub because sessions push from their worktrees and nobody pulls
there. Without the pull it refuses, correctly - those commits really are not in
that `master` yet - but it reads like a warning of data loss.

<a id="sr-launch-worktree"></a>
### Never remove a session's own launch worktree

**Never remove a session's own launch worktree from inside that session.**
On 2026-09-23 a cleanup session that the app had launched in the wrong
worktree moved itself to `.claude/worktrees/cleanup`, then ran `git worktree
remove` on the worktree it had been launched in. Windows refused to delete the
folder, which the session still held open, but only after git had deleted
everything inside it and unregistered the worktree. A session loads its hooks
and skills from the `.claude/` of the folder it was **launched** in, not the
one it moved to, so that session lost `block_heredoc.py`. Every Bash call
failed from then on, and skills were at risk. Nothing was lost, because the
worktree was clean and at `master`, but the session could not continue.
Remove a launch worktree **after closing its session**, from the main
checkout, with the same commands as above.

<a id="sr-worktree-removal"></a>
### Before removing a worktree, with the incidents behind each step

**Commits survive a removal; gitignored files do not.** Commits live in the
shared object store, so `git merge worktree-<role>` followed by `git worktree
remove` loses no commit. But `git worktree remove` deletes ignored files without
asking, and `data/` is ignored - so a city's cache can exist ONLY in the
worktree that built it. On 2026-09-23 `lille` held the only Rennes and Lille
caches, and Rennes' feed is quota-limited. Before removing a worktree:

1. **Unlink every junction first, on its own, without recursion.** A worktree
   may link `data/<country>/raw` to the one shared national file instead of
   copying gigabytes - `lille`'s `data/france/raw` pointed at the 3 GB SIRENE
   pair in the main checkout. PowerShell 5.1's `Remove-Item -Recurse` can
   follow a junction and empty its TARGET, which here would have deleted the
   file every French city is built from. List them, then remove each link
   alone - `cmd /c rmdir <link>` deletes a junction and never its target:

   ```powershell
   Get-ChildItem -LiteralPath <worktree> -Recurse -Force -Attributes ReparsePoint
   ```

   **The WHOLE worktree, not just `data\`.** On 2026-09-24 five of seven
   retired worktrees also had `.venv-lean` as a junction to the main
   checkout's lean venv - a recursive delete through it would have emptied
   the environment every deploy check runs in. A pre-check that filtered on
   `data\` (or skipped `.venv*` by name) did not see them.

   That day the leftover folder was deleted recursively BEFORE its junction
   was noticed. The target survived - both SIRENE files kept their size and
   timestamps - which was luck, not procedure.
2. **Save the worktree's WHOLE `data/` first - every folder, not only built
   cities.** Copy what the main checkout lacks into the main checkout's
   `data/`, no-clobber (`cp -rn`), then run
   `python scripts/check_worktree_data.py <worktree>` until it passes: it
   refuses while any file is absent from main or has a different size there.
   A research worktree holds caches that no `fetch_sources.py` re-creates:
   national files (`data/japan`, `data/mhlw`), unbuilt cities, one-off probe
   downloads, archive-recovered files and stitched registers. **On
   2026-09-27 the old staging worktree was found gone with ~1.2 GB that
   existed nowhere else** - Japan's city registers, the ISJ/N02/N03/e-Stat
   files, and Helsinki, Tallinn, Vienna and part of Riga. The rule then
   read "any `data/<city>/`", which a national folder does not match.
   Copenhagen's cache (2026-09-24) was saved because someone looked. The
   same applies to a worktree removed by any other route (a session's
   worktree cleanup, a manual delete): run the check first.
3. Then the three commands above. If Windows leaves an empty folder behind,
   re-run step 1's listing on it before deleting it.
4. **`Filename too long` stops `git worktree remove` partway.** A worktree
   with its own `.venv-lean` holds Streamlit template paths over Windows'
   260-character limit, 263 in the first case (2026-09-24). Git unregisters
   the worktree and deletes what it can, then stops. Re-run step 1's listing
   over the WHOLE folder, then delete the rest with the long-path prefix:
   `cmd /c rmdir /s /q "\\?\<full path>"`. **An idle session that is still
   open keeps its launch folder locked**: the contents go and an empty
   folder stays until that session is closed. Leave it, and remove the empty
   folder afterwards.

<a id="sr-numbers"></a>
### Page and notice number blocks, the full paragraph of 2026-10-04

**Page numbers pre-assigned (staging, 2026-10-02)**, so two batches building
at once never take the same "next free" number: the UK six **156–161**
(build order), the Japan batch **162–173** (its kit's table order),
Seattle (Regional) **174** and Tbilisi **175**. Notice numbers are claimed
here, by the session, before one is written; no claims are open;
133–136, released unused by the four extensions on 2026-10-03, stay
unassigned; the next free notice is 154. Every earlier block has landed:
the coverage sweep's on 2026-10-04 (the Korean three, pages 190–192 and no
notices; Mendoza, Tacoma and Liverpool (Regional), pages 193–195 and
notices 141–143 and 153; Belgium, pages 196–201 and notices 144–152);
Japan wave 2's 115–128, the extensions' 129–132 and lane-app's 137–140 on
2026-10-03, and everything up to 114 on 2026-10-02. Pages: Japan wave 2 took
176–189; the extensions took none; the next free page is 202.
Check D of `check_provenance.py` reads every range in that sentence and lets
a branch skip exactly those numbers; any other gap still fails. Keep the
ranges in that one sentence, and delete a batch's range once it lands.
**Scaffold with the reserved number:** `scaffold_city.py ... --page-number
<N>`. Without it the script takes one past the highest page on the session's
own branch, which is the collision. It refuses a number already taken. The
three info pages carry no number since 2026-10-02 (`About_the_Data.py`,
`What_Is_Excluded.py`, `Why_the_Maps_Differ.py`), so no block ever reaches
them.

<a id="sr-shared-files"></a>
### Why DECISIONS.md is written by cleanup only

Why: the same-day `DECISIONS.md` conflicts between branches cost a merge per
branch, and on 2026-09-30 one of them committed conflict markers when the
merge tool hit a Windows file lock. For a conflict that still happens, the
resolution is always **keep both**
(`python scripts/merge_append_only.py DECISIONS.md`).

<a id="sr-heavy-jobs"></a>
### The heavy-job gate: the section as it stood on 2026-10-04 (see also #memory)

#### At most three heavy jobs, each admitted by the gate

Every session shares one 16 GB machine. On 2026-09-28 heavy jobs from several
sessions overlapped, the machine ran out of memory, and Windows closed the
Claude app twice, ending every session's turn (DECISIONS; `CLAUDE.md`
`[#memory]`). The owner's rule of 2026-09-28 was one heavy job at a time,
announced by message. **Since 2026-09-30 (owner) two could run at once, and
since 2026-10-04 three (owner, with no other heavy processes open on the
machine), each admitted by `scripts/heavy_job.py`** against the memory
actually available. The count is a ceiling, not a promise: with three build
sessions running, the memory test is what usually refuses a job. If other
heavy programs come back onto the machine, return `MAX_JOBS` to 2.

- **A heavy job** is anything likely to pass 2 GB or run for minutes: a
  multi-city drift check, a full re-render, `deploy-verify`, a join or read
  of a national or prefecture-wide file, a whole-document PDF extraction,
  and a single city whose step 2 loads a large register (Oslo's peaks near
  5.4 GB). A streamed read is not: France's SIRENE step 2 measured 0.37 GB.
- **Run it through the gate:**
  `python scripts/heavy_job.py run --label "<city> <step>" --peak-gb <N> --session <you> -- <command>`.
  It admits the job only if fewer than three are running and available memory,
  less what running jobs have yet to claim, covers the peak plus 2 GB. It
  removes the entry when the job ends and records the MEASURED peak, so state
  the last measured figure next time (`heavy_job.py status` lists them). An
  unknown peak counts as 8 GB.
- **Why measured, not a fixed budget:** on 2026-09-30 the apps alone (eight
  Claude sessions, a browser) held about 8 GB and an orphaned `grep` 4.7 GB
  more, with 2.3 GB free. A sum of declared peaks would have admitted a job
  into that.
- **Refused?** `--wait <minutes>` retries every 30 s. Tell the other sessions
  you are waiting and on what; `status` names every process over 1.5 GB, which
  is how a stray process gets found. Start and end notices are otherwise no
  longer needed: the gate's ledger (`data/_heavy_jobs.json`, shared through
  the `data/` junction) is the notice.
- **A job you cannot wrap** (a subagent's, a browser run): `heavy_job.py start
  --pid <its pid> ...` before, `end --pid <pid>` after. A dead pid drops off
  on its own, so a crash never blocks anyone.
- `drift_check.py` enforces its own share: one run per machine, `--jobs 2`
  at most. The Python cap (8 GB a process, 12 GB with its children) stays as
  the backstop: it turns a runaway into a `MemoryError` instead of a crash.
- Light work needs no gate: greps, git, `check_all.py`, one small city's
  steps.


**Measured figures are the norm (owner, 2026-10-03).** A measured peak is the
threshold: a job declares its label's last measured peak, which the gate
looks up itself when `--peak-gb` is omitted. A job never measured declares an
estimate scaled from measured ones and says so (`--estimate "scaled from
Kyoto 0.33 GB by raw size"`). In a series of like jobs, run the first alone:
it is the measurement the rest declare from. Run jobs side by side wherever
the measured figures fit; for drift that is one run with `--jobs 2`. Keep
labels stable (`<city> step 2`, `drift <city>`, `drift japan --jobs 2`) so the
lookup finds them. A multi-city run is its own label: on 2026-10-03 two
Japanese drift runs of 20 and 30 cities measured 4.54 and 4.71 GB, far above
any single city's step, so a batch is never declared from one city's figure.

**The machine's RAM speed changed on 2026-10-03 (owner):** D.O.C.P. enabled
in the BIOS, so the memory runs at 3200 MT/s instead of 2100. Capacity is
unchanged (15.9 GB), so every measured peak and the gate's arithmetic still
hold. Speed is the change: a job may finish sooner than its last recorded
duration. A crash with memory available, or a `MemoryError` or corrupted
output with no cap reached, after this date is a reason to suspect the
overclock before the script, and to tell the owner.

<a id="sr-agent-description"></a>
### An agent's description length ceiling, measured

#### An agent's `description` has a length ceiling, and exceeding it fails SILENTLY

**Measured 2026-09-22, by breaking it.** `deploy-verify`'s frontmatter
`description` was extended from **755** characters to **1038**, and the agent
**stopped being offered at all** - no error, no warning, no entry in the
available agent types. It simply was not there, and the thing that was not
there is the publish gate.

Known points: **670 registers** (`licence-read`), **755 registers**
(`deploy-verify` before the edit), **1038 does not**. The exact ceiling is
unknown and is probably 1024.

**Keep a `description` at or under 750 characters**, and put everything else in
the body, which has no such limit. The description exists to help a caller
decide whether to invoke the agent; the reasoning belongs where the agent reads
it, not where the harness parses it.

**And check the agent is still listed after editing one.** A skill that fails
to load is usually noisy; an agent that fails to register is not, and the only
symptom is an absence you have to notice.

<a id="sr-screening"></a>
### Why country screening is not a subagent's job

#### Country screening is NOT one of them, and this is a measured position

It looks like a perfect fan-out — many countries, independent probes, a table
at the end — and it is the wrong shape for three reasons:

1. **It is already a session's standing role.** The staging session owns
   `docs/city_master_list.md` and `docs/global_country_shortlist.md`, and a
   subagent writing the same files is the collision this whole document exists
   to prevent.
2. **Parallel work on the append-only files has a real price.** One afternoon
   in 2026-09-22 cost **three separate `DECISIONS.md` merges** between two
   participants. A fan-out of screeners multiplies that by the fan.
3. **Screening is cumulative, not bounded.** `add-country`'s own discipline is
   that a negative from one method is not a finding, that the exhaustive base
   is built before filtering, and that a discard list names its evidence per
   row. A cold agent cannot know what the previous probe already ruled out, so
   it re-derives — and worse, it re-derives *differently*, which is how the
   same country ended up in two tiers at once.

**The screening work that a subagent CAN take is one probe with a stated
question** — "does this endpoint return premises rows with a street address and
an activity code" — handed back as an answer, with the caller doing the
banding. That is bounded. "Screen these five countries" is not.

<a id="sr-handover"></a>
### Labelling every claim in a handover

#### Handing work over: label every claim

The Canada screen reversed five conclusions, each because something was
asserted from a column's existence, a dataset title or a plausible-looking flag
rather than measured. A receiving session cannot tell the difference by
reading. So state it:

- **MEASURED** — carries a number and the query or command that produced it,
  with the date. Build on it.
- **ASSERTED** — plausible, not checked. **Verify before building on it.**
  Saying so costs nothing; discovering it three files later costs a day.

Anything handed between sessions — a build brief, a status message, a summary —
marks its claims this way, and an "open questions" section is not optional.
A brief with no unknowns listed is a brief that has not been audited.

## Commands

<a id="commands"></a>
### The Commands block with its original comments


```bash
python pipeline/<city_slug>/step1_stations.py
python pipeline/<city_slug>/step2_clean_businesses.py
python pipeline/<city_slug>/step3_map.py
python pipeline/drift_check.py [city_slug] [--jobs N]   # --jobs 2 at most since 2026-09-28's memory crashes; one run per machine
python scripts/brief_check.py [city_slug]               # re-run a brief's claims against live sources
                                                       # (16 kinds; taxonomy_catchall picks a taxonomy's level)
python scripts/check_provenance.py [--strict]           # every built city's sources actually recorded; run after adding a city
python scripts/check_no_fetch_in_steps.py [--list]      # no pipeline step may reach the network
python scripts/check_no_fetch_in_steps_selftest.py      # watch that check fail 12 ways; touches nothing
python scripts/check_scope_disclosure.py                # every city's rail AND business scope reaches the published page
python scripts/check_scope_disclosure_selftest.py       # watch that check fail 8 ways; touches nothing
python scripts/check_inconsistency_list.py              # every city has a row in each table of docs/map_inconsistencies.md; run when a city lands
python scripts/check_stray_downloads.py                 # untracked files at ANY checkout's root - where browser-pane downloads land
python scripts/check_overpass_hosts.py [--live|--selftest]   # every Overpass mirror named anywhere is GLOBAL (no regional extract like overpass.osm.ch)
python scripts/check_worktree_data.py <worktree> [--list]   # before removing a worktree: refuses while its ignored data/ holds files main lacks
python scripts/check_render_current.py                  # every committed map carries the CURRENT renderer's shared blocks; run after merging
python scripts/check_map_markup.py [--verbose]          # every line label reads at 4.5:1 in DARK mode; every legend's inline style intact
python scripts/check_inline_arrays.py [--report|--selftest]   # no map ships an inline JS array literal an iPhone cannot compile; run after any re-render
python scripts/check_city_registry.py                   # app/cities.py: one entry per city page, no dict with a repeated key; run after merging
python scripts/check_plan_done.py [--verbose]           # REPORTS only: PLAN.md's [x] items and which already have their DECISIONS entry
python scripts/check_stale_claims.py                    # REPORTS only: prose that stopped being true (stale tense, drifted counts)
python scripts/check_stale_claims.py --only E           # "the only city"/"no other city" claims: re-read whenever a city lands
python scripts/check_discard_evidence.py [--selftest]   # every discard row carries enough evidence for its kind; run when the discard table changes
python scripts/measure_rail_backbone.py --osm <json> --relation <id> --municipios <json> --codes <ibge> --stations <csv> --crs <epsg>   # a commuter line's spacing + coverage for the rail test; frequency is a cited read
python scripts/check_deploy_imports.py [--ref REF]      # clean clone + lean venv: run before ANY push touching app/
node scripts/profile_zoom.mjs <baseUrl> <city,city> [reps]   # wheel/click/cluster zoom lag, headless Edge, trusted input
node scripts/check_macro_attribution.mjs [baseUrl] [375,768,1200]   # the front page's OSM credit is painted ON TOP of the city dots; live: <app>/~/+
python scripts/decisions_index.py [--check]             # refresh DECISIONS.md's index
python scripts/python_memcap.py [--install|--check|--selftest]   # every Python process capped at 8 GB (12 with children); --install with each Python the sessions use
python scripts/merge_append_only.py DECISIONS.md [--dry-run]   # resolve an append-only merge conflict
python scripts/scaffold_city.py --slug <slug> --name <Name> --system-name <system> --taxonomy <key> --lat <lat> --lon <lon> --region <region> --country <country>   # add --dry-run first
.venv-lean/Scripts/python.exe -m streamlit run "app/Overview.py"
```

