"""The app's list of mapped cities - the single source for the Overview's
macro map, its fallback link list, and every city page's city switcher.

Adding a city means adding its entry here (plus its page under app/pages/).
`page` is relative to the entry script (app/Overview_&_Introduction.py),
which is what st.page_link and st.switch_page expect. `lat`/`lon` place the
city's marker on the macro map; they only need to be a sensible centre of its
mapped area, not the exact centre of the city's own map.

Deliberately app-side and tiny: a fuller per-city registry (map centre,
CRS, taxonomy, data sources) is still open in PLAN.md and would live with
the pipeline, not here - the deployed app must stay free of pipeline
dependencies.

Optional `label` ("top" by default, or "left" / "right") sets which side of
its marker the city's name sits on the macro map; set it only where markers
are close together (the three California cities) so their names don't collide.
"""

CITIES = [
    {
        "name": "San Diego",
        "lat": 32.7157,
        "lon": -117.1611,
        "page": "pages/1_San_Diego_Heatmap.py",
        "blurb": "MTS Trolley (Blue, Orange, Green, Copper, Silver lines)",
        "label": "right",
    },
    {
        "name": "San Francisco",
        "lat": 37.7509,
        "lon": -122.4414,
        "page": "pages/2_San_Francisco_Heatmap.py",
        "blurb": "Muni Metro (J Church, K Ingleside, L Taraval, M Ocean View, N Judah, T Third Street)",
    },
    {
        "name": "Los Angeles",
        "lat": 34.05,
        "lon": -118.31,
        "page": "pages/3_Los_Angeles_Heatmap.py",
        "blurb": "Metro Rail (A, B, C, D, E, K Lines)",
        "label": "left",
    },
    {
        "name": "Chicago",
        "lat": 41.8781,
        "lon": -87.6298,
        "page": "pages/4_Chicago_Heatmap.py",
        "blurb": "CTA 'L' (Red, Blue, Brown, Green, Orange, Pink, Purple Lines)",
    },
]
