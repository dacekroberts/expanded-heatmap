# DECISIONS drafts - visuals (`visual-handoff`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Owner rulings on the visuals' open items; SFMTA disclaimer off the San Francisco card

- **The SFMTA "as is" paragraph was dropped from the San Francisco card
  face** (owner, 2026-10-02: "drop if unneeded"). Clause 4 of the stored
  licence (`docs/licenses/sfmta-transit-data-license-agreement.html`) reads
  "The Licensee shall display or include this disclaimer in any use agreement
  for any application of the Data". A card is not a use agreement, so the
  card carries notice 3 (the permission sentence) alone, the same text the
  site shows. One card face changed (`san_francisco`); its PNG was
  re-rendered and the cards artifact republished. Whether the site itself
  owes the disclaimer stays with `docs/licence_positions.md` row 2.16.
- **The Vancouver (Regional) card keeps the cautious reading** (owner
  confirmed): notices 11, 9, 10 and 17 stay on its face.
- **The held cities stay off the cards and public visuals until each one's
  question is ruled on** (owner: "save these"): Seattle (Regional), Barcelona,
  Los Angeles, Washington D.C., Daegu, Busan and the ten SEMAS-area cities.
- **The two stale docs (`map_inconsistencies` section 6, the New York config
  comment) stay with cleanup** (owner: "sounds good").
- **The sampler was rebuilt from analytics' corrected Paris and Toronto
  results.** A floating-point comparison had counted exact ring 1 and ring 2
  density ties as "against": Paris follows 143 -> 146, against 137 -> 134;
  Toronto follows 62 -> 63, against 46 -> 45. San Diego and Tokyo unchanged.

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
