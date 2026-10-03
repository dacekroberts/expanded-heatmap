# DECISIONS drafts - lane-app (`lane-app`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - SFMTA's notice 3 is four sentences plus clause 4's disclaimer, on the cautious reading (owner-approved batch)

- **Re-read** on SFMTA's own page (`sfmta.com/reports/gtfs-transit-data`,
  "updated" 2024-10-01), which matches the stored copy in `docs/licenses/`
  word for word.
- **Clause 12:** "All Data derivative versions prepared by the Licensee shall
  bear the following notice:" is followed by TWO paragraphs before clause 13,
  the second the "does not guarantee ... 'as is'" disclaimer. Nothing marks
  where the notice ends, so on the cautious reading it ends at clause 13, and
  both paragraphs are displayed verbatim. Only the first was shown before.
- **Clause 4:** "The Licensee shall display or include this disclaimer in any
  use agreement for any application of the Data created or provided by
  Licensee." The Visuals session's reading: the duty attaches to a use
  agreement, and the site has none, so licence_positions row 2.16 may have
  overstated it. The sentence parses both ways: "display or include [it] in
  any use agreement", or "display [it], or include it in any use agreement".
  The second is the cautious reading, and costs one sentence; it is taken.
  "This disclaimer" is read as clause 4's own first sentence (clause 3's
  warranty disclaimer is covered in substance by clause 12's second
  paragraph).
- **What the site displays,** on San Francisco's page and the Required notices
  page: clause 12's two paragraphs, then a lead-in of this project's own
  ("SFMTA's license, under which this site is the Licensee, also asks for
  this disclaimer to be displayed:") and clause 4's first sentence in quotes.
- **Rows updated:** data_sources.md item 3, united-states.md's GTFS table,
  licence_positions 2.16 and Appendix A's US-SFMTA entry, and the two flags
  that named the gap.

### 2026-10-03 - Notice 1's rail list gains the UK nine and nine more cities found by a scan (owner-approved batch)

- **The UK nine**, whose rail and boundaries are all OpenStreetMap
  (`docs/data_sources/united-kingdom.md`), added to `_OSM_RAIL` and to notice
  1's sentence as be7d026b added sixteen.
- **A scan of every `docs/data_sources/*.md` table row** naming OpenStreetMap
  or Overpass, against `_OSM_RAIL`, found nine more whose rail or boundary
  comes from OSM: Stockholm (Tunnelbana, kommun boundaries), Bucharest
  (metro, city and sector boundaries), Tbilisi (metro, city boundary), the
  five French cities whose feeds carry no shapes (Montpellier, Strasbourg,
  Le Havre, Caen, Rouen (Regional)), and Philadelphia (one station node,
  11th Street, closed for works; it places a row of the excluded-stations
  file and is not drawn).
- **Left out on reading:** the French GTFS cities whose rows name OSM only as
  gate 3's cross-check; Berlin, Milan, Dublin, Riga and Paris, where OSM is a
  cross-check or explicitly not used; and the twenty Japanese cities, whose
  rail is MLIT N02 and which take only English station names from OSM
  (recorded as "credited by the map's OSM notice"). The Japanese names are an
  open question for the owner: rail data in the loose sense, not geometry or
  a boundary.

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
