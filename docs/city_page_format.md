# What a new city publishes for the reader

The formats the 2026-10-01 prose and UI pass set (owner), in one place, for
whoever builds the next city. Every city-building skill points here at the
moment it writes reader-facing text; the reasoning is in `DECISIONS.md`
(2026-10-01: "City pages: one format for all 124", "The two reference pages
show one country at a time", "The prose and UI pass: ... internal notes
hidden, US spelling site-wide"). A city reaches the reader in three places:
its own page, its section of What Is Excluded (`docs/excluded_categories.md`)
and its rows on About the Data (`docs/data_sources/<country>.md`).

## 1. The city page

`scripts/scaffold_city.py` writes it in this format; a French tram city's is
written whole by `scripts/france_page.py <slug> --write`. Never start a page by
copying an older one. The order, with nothing added between the parts:

1. `render_city_nav`, then `render_city_title("<Name>")`: the city's name,
   centered, over the subtitle "Transit-centered commercial density
   heatmap". The title is the name alone, as in `app/cities.py`.
2. **The map, directly after the title, no exceptions**:
   `st.iframe(HEATMAP_HTML, width=1000, height=650)`. The OSM credit's
   check depends on that height (`CLAUDE.md`, attribution invariant).
3. **The captions, directly under the map**: the data dates
   (`render_data_age`, or the city's own provenance caption), and any credit
   the city's sources require on its page (French pages: « Source : Insee »,
   check M of `check_provenance.py`).
4. **The prose, as short bullets under bold headings**: **The lines** and
   **The businesses**, plus a third only when the city needs one.
   `app/pages/43_Seoul_Heatmap.py` is the model. A bullet is one claim in
   plain words for a general reader: which lines are drawn (each labeled on
   the map and in the legend), what is not drawn and why, the area covered,
   the source and what it cannot show. Detail a reference page already
   carries stays on that page, linked rather than repeated.
5. `render_map_help("<the page's name for its layers>")`: "Using the map",
   the same on every page. Never write a controls paragraph of your own.
6. `render_excluded_stations("<Name>")`: the stations left out, collapsed,
   from `outputs/<slug>/excluded_stations.csv`. The bullets point to it as
   "listed below".
7. `render_country_links("<Name>")`: What Is Excluded and About the Data,
   opened on the city's country.
8. `render_site_notices()` last, inline, never behind an expander. Omitting
   it is a license breach, not a cosmetic gap.

**Never on a page:** a repository path or file name (`outputs/...`,
`pipeline/...`, a script), a check or skill name, the decision log, a
build brief. The reader cannot open any of them.

`python scripts/check_city_page_format.py` (in `check_all`) fails a page out
of this order, with a part missing, or with a path, script, check or the
decision log in its text. The bullets themselves are for a reader.

## 2. The city's sections in the two reference docs

Both pages show one country at a time. `app/country_sections.py` files a
section under a country when its heading names exactly one country's city (as
`app/cities.py` names it), the country itself, or an alias; a heading naming
none inherits its parent's country; anything unmatched shows for every
country. So:

- **Every heading for a city names the city.** In
  `docs/excluded_categories.md`: `### <City> - <what it leaves out>` under
  "Excluded in one city" (or the rail section's matching heading). In
  `docs/data_sources/<country>.md`: the city's rows and notices in that
  country's file.
- **A city's gaps and limits live in its own section.** What its source
  cannot show ("what is missing rather than excluded") and its own honest
  limits go in the city's section, never in the shared "What is missing
  rather than excluded" or "Honest limits" sections, which hold only what is
  true of every city.
- `check_scope_disclosure.py` still decides that both halves of the city's
  scope (its rail and its businesses) reach the reader.

## 3. Process notes stay off the rendered docs

About the Data and What Is Excluded show no internal maintenance. Write the
city's sections for the reader: the data, its terms, its notices, what is
counted and why. How it was found, checked or decided belongs in
`DECISIONS.md` (through the session's drafts file) and the build brief.

Where a process pointer must sit in a rendered doc, wrap it:
`<!-- internal -->...<!-- /internal -->`. `country_sections.public()`
strips it at render time.

- **Process, so hidden:** check scripts and `scripts/...`, `DECISIONS.md`,
  `PLAN.md`, skill and agent names (`licence-read`, `add-city`, ...), build
  briefs, and internal docs (`docs/category_rules.md`,
  `docs/city_master_list_evidence.md`, ...).
- **Never hidden:** a license verdict, a required notice, a quote of terms,
  a fact about the data, method detail (`pipeline/...` modules, endpoints,
  filters, counts), `docs/licenses/...` links, a heading.
- **Wrap the smallest unit that leaves good prose:** a phrase or
  parenthetical first ("(read 2026-09-24 by the licence-read agent)"), a
  sentence only when all of it is process, a bullet only when all of it is.
- **A marker never contains a `|`** (a table cell boundary) and never
  crosses a blank line, unless it hides a whole passage as a block (the open
  marker at the start of a line, the close at the end of one). Re-read the
  text with the spans deleted: no dangling "and", no empty parentheses.
  `python scripts/check_internal_markers.py` (in `check_all`) checks all of
  this except the reading.

## 4. American spelling

Reader-facing text is American English (owner, 2026-10-01): "license",
"color", "center", "neighborhood", "labeled", "gray", "-ize".
Category labels follow it too: "License category" and "License type" as a
field label, "Gas station", "Liquor store", "Tires", "Watches and jewelry",
"Shopping center".

**Kept as written:** the required notices and license titles ("Open
Government Licence – Vancouver", "Licence Ouverte"), anything quoted, a
register's own category names, official names (stations, Hong Kong's
license types, ANZSIC classes), and code identifiers and file names
(`read-licence`, `PRACTITIONER_ONLY_LICENCES`).

## 5. Names in the docs

A doc, brief or decisions entry never quotes a registrant's own name, even
as an example. Use a placeholder ("SURNAME GIVEN-NAME INITIAL", "(Given-name
Surname)"). A list step 2 uses to withhold names holds keys
(`python pipeline/name_keys.py "NAME"`), never the names;
`check_name_keys.py` fails a plain one. A person's own license to work inside
someone else's shop is left out: San Francisco's practitioner licenses
(`DECISIONS.md`, 2026-10-01) and New York's, Calgary's and Edmonton's chair
renters are the precedents (`docs/category_rules.md`, its own row since
2026-10-02).

## 6. Who approves the words

- A sentence from an approved template (`scaffold_city.py`'s bullets as
  filled in for the city, `france_page.py`, a skill's template section) needs
  no read-back.
- A sentence no template covers is a proposal: flag it in the session's
  drafts file and at review time, and keep building.
- Past a few dozen proposals (a re-review, a batch of cities), collect them
  with `scripts/prose_proposals.py` and give the owner a review page
  (`docs/review_lane_kit.md`, section 6).
