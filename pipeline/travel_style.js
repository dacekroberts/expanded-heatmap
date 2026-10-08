// THE SHARED TRAVEL STYLE (draft, branch only). One function that turns the
// layer list of @protomaps/basemaps 5.7.2 into the Travel basemap shared by
// the site's Travel view, the full Travel version and transit-globe's
// starting point (owner, 2026-10-08; rules in the drafts file of branch
// claude/epic-neumann-5aa0a6, "The travel app's basemap rules"). Every hex
// value is a draft. pipeline/map_common.py inlines this file into the
// OpenBasemap layer; transit-globe reads it as the reference and records
// its own departures in its own DECISIONS.md.
//
//   travelStyle(layers, {flavor: "light", world: false, variant: "site"})
//
// world: the label-free world map (owner, 2026-10-08): land, sea, country
// borders and disputed lines only; names come from the export, in the
// dot's tooltip and the UI.
// variant: "site" (the site's Travel view, the default) or "full" (the
// offline full version). Precedence (owner, 2026-10-08): the site is senior
// to its Travel view, so a clash with site-only elements such as the
// business pins is settled on the Travel view; the full version, which has
// no business layers, competes with neither and takes only the choices
// that stand on their own merit (the plum station-area border does).
// disputedDash: overrides the disputed lines' dash, for screenshot trials.
// The output is plain style-spec JSON with nothing GL JS-only in it, so a
// build can write it out as style.json for MapLibre Native as well.
var travelStyle = (function () {
  // Light tints, one per category, pale and differing by hue; transit owns
  // the lavender family (platforms, and station areas once drawn from the
  // export, in the platform tint with the plum border #352a4d).
  var TINT = {
    earth: "#e2dfda",
    park: "#a8d5b5",
    wild: "#c2d8b0",
    cemetery: "#cad3c7",
    sand: "#ece3c6",
    natural: "#d9d5cc",
    institution: "#e7dbd7",
    platform: "#c3b8de",
    aerodrome: "#d8dae1",
    runway: "#c3c6cf"
  };
  // Land-use kinds as the builder writes them (protomaps/basemaps Landuse.java,
  // surveyed in the Mendoza pack 2026-10-08). Kinds not listed stay plain:
  // built-up, business, attractions, farmland and `other`. Railway land is
  // not tinted (owner, 2026-10-08): OSM's railway land runs the full length
  // of many lines (the Pisa line over Florence's Cascine park), the lines
  // carry their own colours, and the lavender is meant for station areas
  // and platforms, so no overlap rule is needed.
  var LANDUSE = [
    ["park", ["park", "garden", "golf_course", "playground", "allotments",
              "village_green", "recreation_ground", "dog_park"]],
    ["wild", ["national_park", "nature_reserve", "protected_area", "forest", "wood",
              "scrub", "grassland", "meadow", "wetland", "heath"]],
    ["cemetery", ["cemetery", "grave_yard"]],
    ["sand", ["beach", "sand"]],
    ["natural", ["bare_rock", "glacier", "scree", "shingle"]],
    ["institution", ["hospital", "school", "university", "college", "kindergarten"]],
    ["aerodrome", ["aerodrome"]],
    ["platform", ["platform"]]
  ];
  // 5.7.2's own land-use fills, replaced in the light flavor by LANDUSE and
  // reduced in the others to the kinds the rules keep.
  var STOCK_LANDUSE = ["landuse_park", "landuse_urban_green", "landuse_hospital",
                       "landuse_industrial", "landuse_school", "landuse_beach",
                       "landuse_zoo", "landuse_aerodrome"];
  var STOCK_DROPPED_ANY_FLAVOR = ["landuse_industrial", "landuse_zoo"];
  // Dropped outright: land cover (an empty stand-in in self-built packs),
  // points of interest, road shields and the basemap's own rail (the
  // site's lines are drawn over it).
  var DROP = ["landcover", "pois", "roads_shields", "roads_rail"];
  // Road details the rules drop, matched on kind_detail (Roads.java copies
  // OSM's service=* there).
  var DROP_DETAIL = ["service", "driveway", "parking_aisle", "alley", "track",
                     "drive-through"];
  // Disputed lines (owner, 2026-10-08): one neutral style everywhere, lighter
  // than the settled border and dotted where it is dashed. Width 1.5 px;
  // with round caps a [0, 1.5] dash draws 1.5 px dots 2.25 px apart centre
  // to centre. Owner asked for a tighter dash than [0, 3]; of [0, 3],
  // [0, 2] and [0, 1.5] compared on world-zoom crops (2026-10-08), only
  // [0, 1.5] keeps short segments such as Kashmir's reading as a line.
  // Every unrecognized kind takes the same rule (owner, 2026-10-08).
  var DISPUTED = {color: "#c4c4c4", width: 1.5, dash: [0, 1.5]};
  var UNRECOGNIZED = ["unrecognized_country", "unrecognized_region", "unrecognized_macroregion"];
  // Ferries and aerial lifts are told apart from operators' line colours by
  // pattern first (transit-globe's suggestion, owner, 2026-10-08). Ferries
  // are dashed. Colours measured with pipeline/linecolour (CIE76) on
  // 2026-10-08: on the site, every blue tried sat under 45 from Retail blue
  // or the backup teal, which pins can bring back, so the site variant's
  // ferries are crimson (59 from the border, 63 from violet, 42.8 from
  // Tokyo's Marunouchi red). The full variant has no pins and keeps a
  // ferry blue, at least 50 from everything it draws (51 from the plum
  // border, 57 from the water tint #80deea). Aerial lifts take the
  // cartographic thin dark line with cross ticks: the earlier burnt orange
  // #d84315 sat 8.3 from the tram city-dot colour #c2410c, under the hard
  // floor of 10.
  var FERRY = {site: "#b0004f", full: "#1e88e5", dash: [3, 2]};
  var AERIALWAY = {color: "#444444", tickWidth: 6, tickDash: [0.15, 2.5]};
  var WORLD_KEEP = ["background", "earth", "water", "boundaries_country"];

  // Legacy filters (["==", "kind", "x"]) and expressions (["==", ["get",
  // "kind"], "x"]) cannot be mixed inside one "all", so a clause is added
  // in whichever syntax the layer already uses.
  function isLegacy(f) {
    if (!Array.isArray(f)) return true;
    var op = f[0];
    if (op === "all" || op === "any" || op === "none") return f.slice(1).every(isLegacy);
    if (op === "!") return false;
    return typeof f[1] === "string";
  }
  function andClause(layer, legacy, expression) {
    var f = layer.filter;
    var clause = isLegacy(f) ? legacy : expression;
    layer.filter = f ? ["all", f, clause] : clause;
  }
  function copy(layer) {
    return JSON.parse(JSON.stringify(layer));
  }
  function lineWidth(z) {
    return ["interpolate", ["exponential", 1.6], ["zoom"]].concat(z);
  }

  return function (layers, opts) {
    opts = opts || {};
    var light = (opts.flavor || "light") === "light";
    var variant = opts.variant === "full" ? "full" : "site";
    var src = (layers[0] && layers[0].source) || (layers[1] && layers[1].source) || "protomaps";
    var out = [];
    var landuseDone = false;
    layers.forEach(function (stock) {
      var id = stock.id;
      if (opts.world) {
        if (WORLD_KEEP.indexOf(id) < 0) return;
        if (id === "water" || id === "earth" || id === "background") {
          out.push(copy(stock));
          if (id === "earth" && light) out[out.length - 1].paint["fill-color"] = TINT.earth;
          return;
        }
      }
      if (DROP.indexOf(id) >= 0) return;
      if (STOCK_LANDUSE.indexOf(id) >= 0) {
        if (STOCK_DROPPED_ANY_FLAVOR.indexOf(id) >= 0) return;
        if (!light) { out.push(copy(stock)); return; }
        if (landuseDone) return;
        landuseDone = true;
        LANDUSE.forEach(function (group) {
          out.push({
            id: "travel_landuse_" + group[0], type: "fill", source: src,
            "source-layer": "landuse",
            filter: ["in", "kind"].concat(group[1]),
            paint: {"fill-color": TINT[group[0]]}
          });
        });
        return;
      }
      var layer = copy(stock);
      if (id === "earth" && light) layer.paint["fill-color"] = TINT.earth;
      if (light && (id === "landuse_runway" || id === "roads_runway")) {
        layer.paint[layer.type === "fill" ? "fill-color" : "line-color"] = TINT.runway;
      }
      if (id === "roads_taxiway") layer.paint["line-opacity"] = 0.5;
      if (/^roads_tunnels_/.test(id) && layer.type === "line") layer.paint["line-opacity"] = 0.5;
      // Lines and labels alike: a hidden road kept its name floating over
      // nothing (Florence's Viale del Visarno, a service road, 2026-10-08).
      if (layer["source-layer"] === "roads" && (layer.type === "line" || layer.type === "symbol")) {
        andClause(layer, ["!in", "kind_detail"].concat(DROP_DETAIL),
          ["!", ["in", ["coalesce", ["get", "kind_detail"], ""], ["literal", DROP_DETAIL]]]);
      }
      if (id === "boundaries_country") {
        andClause(layer, ["all", ["!has", "disputed"], ["!in", "kind"].concat(UNRECOGNIZED)],
          ["all", ["!", ["has", "disputed"]],
                  ["!", ["in", ["get", "kind"], ["literal", UNRECOGNIZED]]]]);
        out.push(layer);
        out.push({
          id: "travel_boundaries_disputed", type: "line", source: src,
          "source-layer": "boundaries",
          filter: ["any", ["has", "disputed"], ["in", "kind"].concat(UNRECOGNIZED)],
          layout: {"line-cap": "round", "line-join": "round"},
          paint: {"line-color": DISPUTED.color, "line-width": DISPUTED.width,
                  "line-dasharray": opts.disputedDash || DISPUTED.dash}
        });
        return;
      }
      if (id === "boundaries") {
        // Country and region only; wards come back per city (Tokyo and
        // Seoul first; admin_level 6 is kind county, 7 and 8 locality).
        andClause(layer, ["all", ["in", "kind", "region", "macroregion"], ["!has", "disputed"]],
          ["all", ["in", ["get", "kind"], ["literal", ["region", "macroregion"]]],
                  ["!", ["has", "disputed"]]]);
      }
      out.push(layer);
      if (id === "roads_bridges_highway") {
        out.push({
          id: "travel_ferry", type: "line", source: src, "source-layer": "roads",
          filter: ["==", "kind", "ferry"],
          paint: {"line-color": FERRY[variant], "line-dasharray": FERRY.dash,
                  "line-width": lineWidth([11, 1, 16, 3])}
        });
        out.push({
          id: "travel_aerialway", type: "line", source: src, "source-layer": "roads",
          filter: ["==", "kind", "aerialway"],
          paint: {"line-color": AERIALWAY.color, "line-width": lineWidth([11, 0.8, 16, 1.5])}
        });
        // Cross ticks: a wide line whose dashes are much shorter than it is
        // wide draws short bars across the cable.
        out.push({
          id: "travel_aerialway_ticks", type: "line", source: src, "source-layer": "roads",
          filter: ["==", "kind", "aerialway"], minzoom: 13,
          paint: {"line-color": AERIALWAY.color, "line-width": AERIALWAY.tickWidth,
                  "line-dasharray": AERIALWAY.tickDash}
        });
      }
    });
    return out;
  };
})();
if (typeof module !== "undefined" && module.exports) module.exports = travelStyle;
