# DECISIONS drafts - lane-rail (cleanup batch, 2026-10-03)

Entries for `DECISIONS.md`, newest first, folded by cleanup at the landing.

### 2026-10-03 - Osaka moves to MLIT N02-25: Yumeshima drawn (owner)

- **What.** `pipeline/countries/japan.py` gives Osaka `"n02": "25"`; step 1
  now reads the 2025 edition, which carries the Chūō Line's Yumeshima (C09,
  opened 2025-01-19, regular service since the 2025-10-14 timetable). Osaka
  has 217 stations; gate 3's Chūō count is 13 (C09 to C21). The other
  Japanese cities on N02-24 stay there, one drift check each when they move
  (PLAN, "Japanese cities onto N02-25").
- **Why.** Staging's re-check calendar found the open station missing, which
  contradicted What Is Excluded's "every line with a station in the city is
  drawn"; the owner said "investigate and then draw". With Yumeshima drawn
  the sentence is true again and is unchanged.
- **Verified.** Steps 1 and 3 re-run from the branch (measured peaks 0.15 and
  0.26 GB); Yumeshima in `stations.csv` at 34.6518, 135.3893, line C.

### 2026-10-03 - São Paulo: Linha 17-Ouro drawn; Linha 6 left out for the owner (owner: "investigate and then draw")

- **What.** The monorail is drawn with all eight stations, Morumbi to
  Aeroporto de Congonhas plus Washington Luís (added 2026-06-30), in OSM's
  #DE7C00 (72.1 from the nearest pins, 40.4 from Linha 3, 46.1 from Linha 4;
  3.0:1 on the light page), labeled "Linha 17-Ouro" on the map and in the
  legend. Gate 3 takes Metrô's own eight (`GATE3_ADDED`): GeoSampa's
  operating layer still lacks the line (re-read 2026-10-03). The Washington
  Luís branch is read by relation id from `osm_l17_branch.json`.
- **Why.** Metrô's Linha 17-Ouro page lists the eight stations in service
  since 2026-03-31, fare-free in "operação transitória", 06:00-22:00 Monday
  to Saturday from 2026-09-30 (read 2026-10-03). Carrying passengers on a
  timetable meets the drawing rule.
- **Linha 6-Laranja stays out, for the owner's call.** Its first six
  stations have run a free assisted service on weekdays 10:00-15:00 since
  2026-07-03: a trial, not a timetable. Step 1 still stops the day GeoSampa's
  operating layer lists it.
- **Page and What Is Excluded:** "Eight lines are drawn ... Linhas 15 and 17
  are monorails."; "Linha 17-Ouro has carried passengers since March 2026,
  still fare-free; all eight of its stations are drawn."; "Linha 6-Laranja is
  not drawn: it is still being built, and its first six stations have run
  only a free trial service on weekday middays since July 2026." What Is
  Excluded says the same.
- **Verified.** Steps 1 and 3 re-run (0.01 and 0.23 GB measured): 111
  stations by name, 109 in the city, 219,667 storefronts available.
- **Downstream:** São Paulo's and Osaka's maps, stations and provenance.
