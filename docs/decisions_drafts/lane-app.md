# DECISIONS drafts - lane-app (`lane-app`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
