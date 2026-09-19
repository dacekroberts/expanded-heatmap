"""Shared heatmap rendering, extracted from the San Diego and San Francisco
step3_map.py files once two cities existed (they had become ~90% identical
copies). A city's step3_map.py now only supplies what is genuinely
city-specific - map center, transit-line specs, station/business data
paths - and calls render_heatmap().

Nothing here may name a specific taxonomy. Category grouping, the tooltip's
field label, and legend text all come from the city's taxonomy module (see
pipeline/taxonomies/__init__.py for the interface), so a non-NAICS city
renders correctly with no changes to this file.

Standing map-build requirement (docs/project_context.md): every transit
line gets BOTH a permanent on-map label (add_line_label) AND a legend
entry (build_legend). render_heatmap does both for every line passed in.
"""

import html
import zipfile

import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from folium.plugins import HeatMap, FastMarkerCluster

from pipeline.taxonomies import CATEGORY_BUCKETS, load_taxonomy_module

HEAT_RADIUS = 8
HEAT_BLUR = 10
HEAT_MIN_OPACITY = 0.35
HEAT_GRADIENT = {0.3: "#fee0d2", 0.5: "#fc9272", 0.7: "#fb6a4a", 0.85: "#de2d26", 1.0: "#a50f15"}

LEGEND_HTML = """
<div style="
    position: fixed; bottom: 24px; right: 24px; z-index: 9999;
    background: white; padding: 10px 14px; border: 1px solid #999;
    border-radius: 4px; font-family: sans-serif; font-size: 13px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
">
  <div style="font-weight: bold; margin-bottom: 6px;">Business Category</div>
  {category_rows}
  <div style="font-weight: bold; margin: 10px 0 6px;">Transit Lines</div>
  {line_rows}
</div>
"""
LEGEND_ROW = """
  <div style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:11px; height:11px;
      border-radius:50%; background:{color}; margin-right:7px;
      border:1px solid rgba(0,0,0,0.3);"></span>{label}
  </div>
"""
# A short colored line swatch, not a dot - distinguishes transit lines from
# business categories at a glance, so a reader isn't relying on the on-map
# line labels alone (automatic placement can land imperfectly).
LEGEND_LINE_ROW = """
  <div style="display:flex; align-items:center; margin:3px 0;">
    <span style="display:inline-block; width:16px; height:3px;
      background:{color}; margin-right:7px;
      border-radius:2px;"></span>{label}
  </div>
"""


def load_line_shapes(gtfs_zip, line_specs, system_name):
    """Real line geometries from GTFS shapes.txt - the actual alignment,
    not straight lines between stations.

    line_specs: {key: (shape_id, color, real-world public name, label
    offset in degrees)}. Returns {key: (coords, color, label, offset)}.
    """
    if not gtfs_zip.exists():
        print(f"No GTFS feed at {gtfs_zip} - skipping the {system_name} line overlay.")
        return {}
    with zipfile.ZipFile(gtfs_zip) as z, z.open("shapes.txt") as f:
        shapes = pd.read_csv(f, dtype=str)
    shapes["shape_pt_sequence"] = shapes["shape_pt_sequence"].astype(int)

    lines = {}
    for key, (shape_id, color, label, offset) in line_specs.items():
        pts = shapes[shapes["shape_id"] == shape_id].sort_values("shape_pt_sequence")
        if pts.empty:
            print(f"WARNING: shape_id {shape_id!r} for the {label} not in this "
                  "GTFS feed - check trips.txt for its current most-used shape_id.")
            continue
        coords = list(zip(pts["shape_pt_lat"].astype(float), pts["shape_pt_lon"].astype(float)))
        lines[key] = (coords, color, label, offset)
    return lines


def line_label_position(coords, offset_deg=0.006):
    """A point just off the line's own path, roughly at its midpoint, to
    anchor a permanent text label - offset perpendicular to the line's
    local direction so the label doesn't sit on the line (or the station
    markers strung along it).

    Automatic rather than hand-picked per line. It won't always find the
    clearest spot - if a rendered map shows a label on a dense cluster or
    another line, override that line's offset (see each city's line specs)
    rather than hand-tuning this function, which must keep working
    unattended for every line and every future city.
    """
    mid = len(coords) // 2
    i1, i2 = max(0, mid - 3), min(len(coords) - 1, mid + 3)
    lat1, lon1 = coords[i1]
    lat2, lon2 = coords[i2]
    dlat, dlon = lat2 - lat1, lon2 - lon1
    perp_lat, perp_lon = -dlon, dlat
    norm = (perp_lat ** 2 + perp_lon ** 2) ** 0.5
    if norm == 0:
        perp_lat, perp_lon, norm = 0.0, 1.0, 1.0
    perp_lat, perp_lon = perp_lat / norm, perp_lon / norm
    mid_lat, mid_lon = coords[mid]
    return mid_lat + perp_lat * offset_deg, mid_lon + perp_lon * offset_deg


def add_line_label(feature_group, coords, label, color, offset_deg=0.006):
    """A permanent, always-visible line-name label - NOT a hover tooltip.
    Use the line's real public-facing name."""
    label_lat, label_lon = line_label_position(coords, offset_deg=offset_deg)
    folium.Marker(
        location=[label_lat, label_lon],
        icon=folium.DivIcon(html=f"""
            <div style="
                font-size: 14px; font-weight: bold; color: {color};
                text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff,
                             -1px 1px 0 #fff, 1px 1px 0 #fff,
                             0 0 6px #fff;
                white-space: nowrap; pointer-events: none;
            ">{html.escape(label)}</div>
        """),
    ).add_to(feature_group)


def nearest_station_and_ring(businesses, stations, crs_geographic, crs_projected,
                             ring_edges_meters, ring_labels):
    """For each business: its nearest station and which ring band that
    distance falls in relative to that station - built only for the pin
    tooltip, separate from any aggregate ring analysis."""
    biz_gdf = gpd.GeoDataFrame(
        businesses,
        geometry=gpd.points_from_xy(businesses["longitude"], businesses["latitude"]),
        crs=crs_geographic,
    ).to_crs(crs_projected)
    sta_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=crs_geographic,
    ).to_crs(crs_projected)

    biz_xy = np.column_stack([biz_gdf.geometry.x, biz_gdf.geometry.y])
    sta_xy = np.column_stack([sta_gdf.geometry.x, sta_gdf.geometry.y])
    dist = np.sqrt(((biz_xy[:, None, :] - sta_xy[None, :, :]) ** 2).sum(axis=2))
    nearest_idx = dist.argmin(axis=1)
    nearest_dist = dist.min(axis=1)

    def band(d):
        for i, ring_label in enumerate(ring_labels):
            if ring_edges_meters[i] <= d < ring_edges_meters[i + 1]:
                return f"Ring {i + 1} ({ring_label})"
        outer_mi = ring_edges_meters[-1] / 1609.344
        return f"Beyond ring {len(ring_labels)} (>{outer_mi:.1f} mi)"

    return sta_gdf["station"].to_numpy()[nearest_idx], [band(d) for d in nearest_dist]


def _esc(value):
    """HTML-escape a value for the tooltip. Business names come from public
    datasets but are still free text - an unescaped '<' or '&' breaks the
    hover text or injects markup."""
    return "" if pd.isna(value) else html.escape(str(value), quote=True)


def add_pin_layer(m, rows, group_name, color, tooltip_field_label, value_column, show=True):
    """One toggleable, clustered, coloured pin layer for a category bucket.
    Returns the number of points (0 = nothing added)."""
    data = [
        [row.latitude, row.longitude, _esc(row.business_name),
         _esc(getattr(row, value_column)), _esc(row.nearest_station), _esc(row.ring_band)]
        for row in rows.itertuples()
    ]
    if not data:
        return 0
    callback = f"""
        function (row) {{
            var marker = L.circleMarker(new L.LatLng(row[0], row[1]), {{
                radius: 5, color: '{color}', fillColor: '{color}',
                fillOpacity: 0.85, weight: 1
            }});
            var html = '<b>' + row[2] + '</b><br>' +
                '{tooltip_field_label}: ' + row[3] + '<br>' +
                'Nearest station: ' + row[4] + '<br>' +
                row[5];
            marker.bindTooltip(html, {{sticky: true}});
            return marker;
        }}
    """
    # Leaflet.markercluster's default cluster icon is a fixed 40x40px no
    # matter the count, so a small cluster's oversized hit area blocks
    # hover on the lone dot beside it. Scale icon size with child count.
    icon_create_function = f"""
        function (cluster) {{
            var count = cluster.getChildCount();
            var size = count <= 3 ? 18 : count <= 10 ? 26 : count <= 50 ? 34 : 42;
            var fontSize = Math.max(9, Math.round(size * 0.42));
            return new L.DivIcon({{
                html: '<div style="width:100%; height:100%; border-radius:50%; ' +
                    'background:{color}; opacity:0.85; ' +
                    'border:1px solid rgba(0,0,0,0.4); display:flex; ' +
                    'align-items:center; justify-content:center; color:#fff; ' +
                    'font-size:' + fontSize + 'px; font-weight:600;">' +
                    count + '</div>',
                className: 'business-cluster-icon',
                iconSize: new L.Point(size, size)
            }});
        }}
    """
    # FastMarkerCluster's own `show` parameter is NOT reliable for hiding
    # it at load. Wrap it in a FeatureGroup, which does respect show=.
    # Do not "simplify" this back to FastMarkerCluster(show=...).
    fg = folium.FeatureGroup(name=f"<b>Businesses: {group_name} ({len(data):,})</b>", show=show)
    FastMarkerCluster(data, callback=callback, icon_create_function=icon_create_function).add_to(fg)
    fg.add_to(m)
    return len(data)


def build_legend(bucket_colors, legend_label, lines):
    """Fixed-position legend generated from the buckets actually present
    and the taxonomy's own legend text - nothing taxonomy-specific here.

    bucket_colors: [(bucket name, color)]; legend_label: bucket -> text;
    lines: {key: (coords, color, label, offset)}.
    """
    return LEGEND_HTML.format(
        category_rows="".join(
            LEGEND_ROW.format(color=color, label=html.escape(legend_label(name)))
            for name, color in bucket_colors
        ),
        line_rows="".join(
            LEGEND_LINE_ROW.format(color=color, label=html.escape(label))
            for _coords, color, label, _offset in lines.values()
        ),
    )


def render_heatmap(*, output_path, center, zoom, map_title, city_name, system_name,
                   stations, businesses, taxonomy_system, lines,
                   crs_geographic, crs_projected, ring_edges_meters, ring_labels):
    """Render one city's heatmap to a standalone HTML file.

    stations: DataFrame(station, latitude, longitude). businesses: the
    city's businesses_clean.csv as a DataFrame (needs latitude, longitude,
    business_name and the taxonomy's VALUE_COLUMN). lines: output of
    load_line_shapes. system_name prefixes each line's layer name (e.g.
    "Trolley", "Muni Metro").
    """
    taxonomy = load_taxonomy_module(taxonomy_system)
    bucket_colors = dict(CATEGORY_BUCKETS)

    businesses = businesses.dropna(subset=["latitude", "longitude"]).copy()
    businesses["nearest_station"], businesses["ring_band"] = nearest_station_and_ring(
        businesses, stations, crs_geographic, crs_projected, ring_edges_meters, ring_labels
    )
    in_rings = businesses[~businesses["ring_band"].str.startswith("Beyond")].copy()
    print(f"{len(businesses) - len(in_rings):,} of {len(businesses):,} businesses fall "
          f"outside every station's ring ({len(in_rings):,} remain within a ring).")

    # Fixed pixel width/height, NOT percentage sizing: Leaflet.heat has a
    # known open bug (github.com/Leaflet/Leaflet.heat/issues/95) where an
    # uncaught IndexSizeError fires on init if the container's size isn't
    # resolved yet, which silently stops every later .addTo(map) call in the
    # generated script - rings, markers and the layer control never render,
    # with no visible console error. The app pages embed the map at this
    # same fixed size; change them together.
    m = folium.Map(location=center, zoom_start=zoom, tiles=None, width=1000, height=650)
    folium.TileLayer(tiles="OpenStreetMap", name=map_title).add_to(m)

    # Two heat layers, same tuning, different universe: within-rings is the
    # default; the whole-city one is an opt-in for context.
    HeatMap(in_rings[["latitude", "longitude"]].values.tolist(),
            radius=HEAT_RADIUS, blur=HEAT_BLUR, min_opacity=HEAT_MIN_OPACITY,
            gradient=HEAT_GRADIENT, name="Commercial Density (Within Station Proximity)",
            show=True).add_to(m)
    HeatMap(businesses[["latitude", "longitude"]].values.tolist(),
            radius=HEAT_RADIUS, blur=HEAT_BLUR, min_opacity=HEAT_MIN_OPACITY,
            gradient=HEAT_GRADIENT, name=f"Commercial Density (All {city_name} Businesses)",
            show=False).add_to(m)

    for i, label in enumerate(ring_labels):
        layer = folium.FeatureGroup(name=f"Concentric Ring {i + 1}: {label}", show=True)
        for _, station in stations.iterrows():
            folium.Circle(
                location=[station["latitude"], station["longitude"]],
                radius=ring_edges_meters[i + 1],
                color="#2c3e50", weight=1, fill=False, opacity=0.5,
            ).add_to(layer)
        layer.add_to(m)

    station_layer = folium.FeatureGroup(name="Stations", control=False)
    for _, station in stations.iterrows():
        folium.CircleMarker(
            location=[station["latitude"], station["longitude"]],
            radius=5, color="#1a5490", fill=True, fill_opacity=0.9,
            tooltip=folium.Tooltip(f"<b>{html.escape(station['station'])}</b>", sticky=True),
        ).add_to(station_layer)
    station_layer.add_to(m)

    # Transit lines: always-on context, permanent label + legend entry each.
    for _key, (coords, color, label, offset) in lines.items():
        rail_layer = folium.FeatureGroup(name=f"{system_name}: {label}", show=True, control=False)
        folium.PolyLine(coords, color=color, weight=4, opacity=0.85).add_to(rail_layer)
        add_line_label(rail_layer, coords, label, color, offset_deg=offset)
        rail_layer.add_to(m)

    # Category grouping via the city's own taxonomy, never a hardcoded one.
    in_rings["_bucket"] = in_rings.apply(
        lambda r: taxonomy.classify({taxonomy.VALUE_COLUMN: r[taxonomy.VALUE_COLUMN]}), axis=1
    )
    unmatched = in_rings["_bucket"].isna().sum()
    if unmatched:
        print(f"WARNING: {unmatched} businesses matched no category bucket.")

    present = []
    for name, color in CATEGORY_BUCKETS:
        rows = in_rings[in_rings["_bucket"] == name]
        if add_pin_layer(m, rows, name, color, taxonomy.FIELD_LABEL, taxonomy.VALUE_COLUMN):
            present.append((name, color))

    m.get_root().html.add_child(folium.Element(
        build_legend(present, taxonomy.legend_label, lines)
    ))

    # Collapsed by default: many toggleable layers would otherwise cover a
    # large share of the map. Top-left, not Leaflet's top-right default -
    # the map has a fixed 1000px width and a top-right control can be
    # pushed off the visible edge when Streamlit's content area is narrower.
    folium.LayerControl(collapsed=True, position="topleft").add_to(m)
    m.get_root().html.add_child(folium.Element("""
        <style>
            .leaflet-control-layers-expanded {
                max-height: 480px;
                overflow-y: auto;
            }
        </style>
    """))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))
    print(f"Wrote {output_path}")
    print(f"{len(in_rings):,} points plotted (within-ring default) / "
          f"{len(businesses):,} available (all-{city_name} toggle), across {len(stations)} stations")
