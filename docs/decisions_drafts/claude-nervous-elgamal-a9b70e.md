# DECISIONS drafts - CARTO key (`claude/nervous-elgamal-a9b70e`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - The Overview's CARTO basemap sends the project's key on every request; its credit now links CARTO's attribution page, with OpenMapTiles

- **Why.** CARTO's Basemap Terms (2026-09-29, §3.b) allow free use only with
  a CARTO-issued key. The owner holds two (DECISIONS, 2026-10-02): one
  Referer-locked to localhost and 127.0.0.1, one to
  expanded-heatmap-daceroberts.streamlit.app. Both are read only as
  `st.secrets["CARTO_BASEMAP_KEY"]`.
- **The key travels as `?key=`** on every address under basemaps.cartocdn.com
  (carto.com/basemaps/apikey/: "on every tile, style, glyph and sprite URL").
- **The style is a committed copy of CARTO's open-source Positron**
  (`app/assets/carto_positron/style.json`, from CartoDB/basemap-styles
  `mapboxgl/positron.json`, last changed upstream 2019-06-11 at 6f8f933).
  - Its 93 layers equal the served
    basemaps.cartocdn.com/gl/positron-gl-style/style.json, layer for layer
    (compared 2026-10-02). The only upstream difference is CARTO's own
    `{api_key}` placeholder on the source address, which is the key-free
    template.
  - BSD 3-Clause code and CC BY 4.0 design. The upstream LICENSE.md sits
    beside it, as the BSD notice requires.
- **The keyed style reaches the browser as a data: URL, built in memory**
  (`app/basemap.py`). Static serving was the alternative and was not chosen:
  - the key is never written to disk, so no gitignored file can be committed
    by mistake and none outlives a checkout;
  - `.streamlit/config.toml` stays unchanged, with no site-wide static route;
  - no path question on Streamlit Cloud, which serves the app under `/~/+/`.
  - Cost: about 100 KB of base64 in the deck's JSON on each rerun. mapbox-gl
    reloads the style only when the string changes, which it does not.
  - A style dict was not possible: pydeck takes one only with
    `map_provider="mapbox"`, and Streamlit's frontend passes only a string,
    or an array's first item, to the map.
- **CARTO's TileJSON hands back KEYLESS tile URLs** (measured 2026-10-02, with
  the key on the request). So the style's source also lists the four tile
  URLs itself, keyed. mapbox-gl merges a source's own `tiles` and
  `attribution` over the TileJSON's, and still fetches the TileJSON, keyed,
  for its zoom range (0-14) and bounds.
- **No key, no basemap.** A checkout without the secret gets an `st.warning`
  and the dots on a blank ground. `map_provider=None` stops Streamlit from
  substituting keyless CARTO. Verified on a server started with
  `--secrets.files` pointed at a missing file: the warning shows, and there
  are zero requests to CARTO.
- **The credit**, set in the style's source:
  - "© OpenStreetMap contributors, © CARTO, © OpenMapTiles";
  - linked to openstreetmap.org/copyright, carto.com/attribution/ and
    openmaptiles.org (carto.com/attribution/, and the basemap-styles
    licence's OpenMapTiles clause);
  - `fixCredit()` in `app/components.py` also corrects a CARTO href, as a
    guard.
  - The credit wraps to two lines at 375 px (40 px tall).
- **Verified locally**, on the `streamlit-app-lean` preview in exact-size
  frames. Global, Europe and Japan West, at 1200 and 375, light and dark:
  - every CARTO request carried `?key=<key>` and returned 200: TileJSON 1,
    sprite 2, glyphs 1-4, tiles 2-14 per load;
  - no keyless request, and no style request to CARTO (the style is inline);
  - tiles and glyphs inside mapbox-gl's worker were counted by wrapping the
    frame's `Worker`, with the key redacted in the browser.
  - "Looks as today" rests on the identical layers. A keyless before-render
    would itself be outside the terms, so none was made.
  - `check_macro_attribution.mjs`: PROBLEMS 0 at 375, 768 and 1200, light
    and dark. It now also requires the CARTO link to carto.com/attribution/
    and an OpenMapTiles link, and samples both lines of a wrapped credit.
  - The dark theme's filter applies to `.mapboxgl-canvas` only, never to the
    credit.
  - `check_macro_labels.py` PROBLEMS 0; `check_all.py` 45 of 45.
- **New check:** `scripts/check_basemap_key.py`, in `check_all.py`. Offline,
  with a stand-in key and no secret read, it fails:
  - on any cartocdn address without the key;
  - on a source with no keyed tiles of its own;
  - on a credit missing any of the three links;
  - on `app/Overview.py` naming a CARTO style itself.
- **Landing:** an `app/` change plus a new imported module (`app/basemap.py`),
  so the deployed app needs a REBOOT, not "Updated app!". The public key is
  in the app's Secrets as `CARTO_BASEMAP_KEY` (owner, 2026-10-02: "yes, the
  public key is in Secrets"). Without it the live map would show the warning
  and no basemap, which is safe but visible.
- **For the owner (proposals, not written anywhere rendered):**
  - Privacy line (§10 makes the site the controller): "The overview map's
    basemap loads from CARTO, so your browser sends CARTO your IP address and
    browser details with each map request; CARTO processes them for this
    site."
  - The site-notice sentence "The overview map's basemap is © CARTO." could
    become "The overview map's basemap is © CARTO and © OpenMapTiles, from
    OpenStreetMap data." It is optional, since the on-map credit already
    carries all three.
- **For cleanup:** `docs/licence_positions.md` row 1.23 ("keyless, outside
  its terms") and PLAN's "Overview's basemap" item describe the keyless state,
  and both change when this lands. `docs/data_sources.md` gained the CARTO
  section the record lacked; it renders on About the Data, so its prose is
  for review time.
