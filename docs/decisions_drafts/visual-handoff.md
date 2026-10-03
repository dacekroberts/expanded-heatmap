# DECISIONS drafts - visuals (`visual-handoff`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - City card captions regenerated from the landed notices; no card face changed

- **The 129 city cards and their captions were regenerated from master at
  `b31a65df`**, after `claude/nice-boyd-51dea8` landed. City notices now come
  from the landed `app/components.py` `city_notices()`, not a copy from the
  branch.
- **Only notice 1 changed for any city**: the OpenStreetMap rail-geometry
  text, in 68 cities' captions. It now names the 16 cities `be7d026b` added
  to `_OSM_RAIL`. The card generator added those 16 by hand before; it now
  only asserts they are in the landed list.
- **No card face changed.** All 129 faces were compared before and after, so
  the card images in `visuals/cards/` stand. Captions, the cards artifact
  and `visuals/captions/` were refreshed.
- **The maps on master were all re-rendered (map chrome only).** Their pin
  data was spot-checked unchanged on San Diego, and `app/ring_shares.json`,
  `app/macro_facts.json` and `app/cities.py` are unchanged since `13dceb1d`.
  So every figure on every visual stands.
- The CARTO credit and privacy line now ending the site-wide basemap notice
  cover the overview map's basemap only. No visual draws a CARTO basemap, so
  no caption carries it.
