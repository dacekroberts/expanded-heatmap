# Coverage sweep: the rail-city universe (2026-10-03, re-matched 2026-10-04)

**What this folder is.** The record of the coverage sweep that compared every
city in the world with a metro, light rail or tram against the master list,
kept so the far-future re-probe in `docs/recheck_calendar.md` ("The screen
itself", about 2027-10) can start from it instead of from nothing. The
rail-city listing closed on 2026-10-04 (owner); the master list's
"Pre-verdicts" section says what can reopen it.

**The universe.** Wikipedia's "List of metro systems" and "List of tram and
light rail transit systems", read as wikitext on 2026-10-03, plus openings
found by search and the satellite towns each system serves (one row per city
served). Japan's universe is staging's scoping of 2026-10-02: every
designated and core city, every city of 200,000 or more, and every
municipality with a subway, tram, monorail or AGT station, with MHLW's FY2024
food-permit counts and N02 station groups.

| File | What it holds |
|---|---|
| `europe.md` | The Europe report (Türkiye, the Caucasus, Russia, Ukraine and Belarus included; Belgium screened apart), 343 rows classified |
| `europe_classified.json` | The same 343 rows as data: city, country, system, status at 2026-10-03, pointer, note |
| `americas_oceania.md` | The Americas and Oceania report, with its ranked never-recorded list |
| `asia_mideast_africa.md` | Asia (Japan apart), the Middle East and Africa |
| `japan_scope.md`, `japan_universe_mhlw.csv` | Japan's scoping (114 uncovered municipalities as of 2026-10-02), names in kanji |

The reports' pointers (`ML:572` and the like) are line numbers in the docs as
they stood on 2026-10-03 and have drifted since; the statuses are a snapshot,
and the master list wins.

**The scripts** (`scripts/coverage_sweep/`, usage in `docs/commands.md`):
- `universe_europe.py`, `universe_france.py`: the curated Europe and France
  rows with name aliases (Köln, Koeln and Cologne).
- `parse_wiki_tram.py`: turns a saved copy of the tram list's wikitext into
  rows, the starting point for curating a new universe.
- `recount.py`: re-matches the universe against `docs/city_master_list.md`
  and prints which cities the list does not name. Coarse by design (about 10%
  either way): a name on the list is not proof of a verdict.

**To refresh the universe** (the re-probe's first step): save each list's
wikitext through the MediaWiki parse API
(`https://en.wikipedia.org/w/api.php?action=parse&page=<title>&prop=wikitext&format=json`;
the rendered page truncates) into `data/_coverage_sweep/` with curl's own
user agent, run `parse_wiki_tram.py`, add new systems and satellites to the
universe files and reports, search for openings since the last read, then run
`recount.py`. The wikitext itself is not committed (Wikipedia's text is
CC BY-SA and re-fetchable).
