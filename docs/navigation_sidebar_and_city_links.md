# Navigation: the sidebar and city links (kept, switched off in the map-only pilot)

The app has two ways of moving between pages. The **map-only pilot** (started
2026-09-20) turns the first two below off so the macro map is the only
navigation. Nothing was deleted: `MAP_ONLY_NAV` in `app/cities.py` switches
between the two modes, so restoring the older navigation is a one-line change.

| | Sidebar page list | City switcher row | Macro map + "Global View" button |
|---|---|---|---|
| `MAP_ONLY_NAV = True` (now) | hidden | not shown | the way in, out, and between cities |
| `MAP_ONLY_NAV = False` | shown | shown on every city page | still there, alongside |

## What the sidebar is

Streamlit's automatic multipage navigation. Every file in `app/pages/` becomes
a sidebar entry, ordered by its numeric prefix and labelled from its file name
(`1_San_Diego_Heatmap.py` -> "San Diego Heatmap"), under the entry script
"Overview & Introduction". There is no code for it in this repo: it is
Streamlit's default, and adding a city (a file in `app/pages/`) adds an entry.
The pilot hides it with CSS (`_MAP_ONLY_CSS` in `app/components.py`, emitted
by `set_base_font()`: `[data-testid="stSidebar"]` and its expand control get
`display: none`). Hiding it, rather than turning navigation off in
`.streamlit/config.toml`, keeps the Overview link in the page for the back
button and makes the change reversible from Python alone.

## What the city links are

1. **The switcher row** on each city page, `components.render_city_nav(current)`:
   a link back to the map, then every city, the current one as plain bold text.
   The original code (still in `app/components.py`, after the map-only early
   return):

   ```python
   def render_city_nav(current: str):
       # A horizontal container sizes each item to its content and wraps onto a
       # second line when the row is too narrow; fixed-width columns clipped the
       # longer city names once a fourth city was added.
       with st.container(horizontal=True, gap="medium", vertical_alignment="center"):
           st.page_link(OVERVIEW_PAGE, label="← Global View")
           for city in CITIES:
               if city["name"] == current:
                   st.markdown(f"**{city['name']}**")
               else:
                   st.page_link(city["page"], label=city["name"])
   ```

   It reads the city list from `app/cities.py` (`CITIES`), the single source
   also used by the macro map. Each city page calls it once, right after
   `set_base_font()`, with its own display name.
2. **The fallback list** under the macro map on the Overview ("Or pick a city
   from the list", a `st.page_link` plus a caption per city). This is **kept in
   the pilot** on purpose: it is the keyboard and screen-reader route to a city
   and the route if the map fails to load (see the "Macro map and city
   navigation" entry in `DECISIONS.md`). Decided 2026-09-21: keep it.
3. **The intro sentence** on the Overview, which mentions the switcher; it now
   reads "each city map has a 'Global View' button to come back here" while
   `MAP_ONLY_NAV` is on.

## How map-only navigation works

- **In:** clicking a city marker on the macro map opens that city's page
  (`st.switch_page`; works without a sidebar).
- **Out:** each city map has a **"Global View"** button, top-right, left of the
  Dark Mode button (all the top-right controls live in `THEME_TOGGLE_HTML` in
  `pipeline/map_common.py`, so every city gets them from the shared renderer).
- **Between cities:** a **"Cities" dropdown** (a native `<select>`, so it works
  with a keyboard and gets the phone's own picker) at the left of that group. It
  lists the other cities, leaving out the one you are on, and picking one opens
  it in place. It reads the city names from the hidden links below, so adding a
  city to `app/cities.py` adds it to every menu with no map to regenerate. The
  current city is worked out from the page URL (`/<Name>_Heatmap`), so a city
  page file must keep that naming. The button only appears when
  the map is embedded in the app (`window.parent !== window`); a map opened on
  its own has nowhere to go back to, so it is hidden.
- **The button navigates by clicking a link on the page.** The map is a
  sandboxed iframe (Streamlit's `st.iframe` allows scripts and same-origin
  access but not top-level navigation), so it cannot set the parent's location.
  Clicking the parent page's own link to the Overview works, and Streamlit then
  navigates in place, with no reload (checked: the browser window object
  survives the click). The link is found by its text (the hidden link keeps "All cities", the
  switcher's reads "Global View"), falling
  back to the link whose path is the app's root.
- **Those links must exist on every city page.** With the switcher off,
  `render_city_nav()` still renders a link to the Overview and one per city inside a
  `st.container(key="map-only-nav")` that CSS hides. Do not remove that call
  from a city page in map-only mode, or the button and menu will do nothing.
  (The scaffold template already includes the call.)
- **The light/dark choice travels with it.** Both directions share one
  `localStorage` key, and the button also saves the current mode before it
  navigates, so the macro map opens in the mode the city map was in, and a city
  map opens in the mode the macro map was in.

## Restoring the sidebar and switcher

Set `MAP_ONLY_NAV = False` in `app/cities.py`. That un-hides the sidebar,
brings back the switcher row on every city page, and restores the intro
sentence. The "Global View" button stays (it finds the switcher's "← Global View"
link). Restart Streamlit after the change (it serves an edited
`components.py` from cache otherwise), then check every city page.

## Open questions and known gaps in the pilot

- **The Overview's fallback link list is kept** (decided 2026-09-21, after
  viewing the pilot). For a pure map-only site it would be the one remaining list
  of city links; dropping it later removes the keyboard and no-map route.
- **Hopping between cities** was a gap (two steps through the macro map); the
  "Cities" dropdown closes it (added 2026-09-21). A visitor who lands on a city
  page by URL now has the dropdown and the "Global View" button.
- **Deep links still work:** a city page's URL opens it directly.
- **A missing link means a dead control:** the buttons do nothing, and the
  dropdown stays hidden or empty, if the hidden links were not rendered.
- **`deploy-verify`** checks the switcher on each city page; in map-only mode
  it should check the button instead (its instructions say so).
