// THE SHARED TRAVEL STYLE (draft, branch only). One function that turns the
// layer list of @protomaps/basemaps 5.7.2 into the Travel basemap shared by
// the site's Travel view, the full Travel version and transit-globe's
// starting point (owner, 2026-10-08; rules in the drafts file of branch
// claude/epic-neumann-5aa0a6, "The travel app's basemap rules"). Every hex
// value is a draft. pipeline/map_common.py inlines this file into the
// OpenBasemap layer; transit-globe reads it as the reference and records
// its own departures in its own DECISIONS.md.
//
//   travelStyle(layers, {flavor: "light", world: false})
//
// world: the label-free world map (owner, 2026-10-08): land, sea, country
// borders and disputed lines only; names come from the export, in the
// dot's tooltip and the UI.
var travelStyle = (function () {
  // Light tints, one per category, pale and differing by hue; transit owns
  // the lavender family (railway land, platforms).
  var TINT = {
    earth: "#e2dfda",
    park: "#a8d5b5",
    wild: "#c2d8b0",
    cemetery: "#cad3c7",
    sand: "#ece3c6",
    natural: "#d9d5cc",
    institution: "#e7dbd7",
    railway: "#d6cfe8",
    platform: "#c3b8de",
    aerodrome: "#d8dae1",
    runway: "#c3c6cf"
  };
  // Land-use kinds as the builder writes them (protomaps/basemaps Landuse.java,
  // surveyed in the Mendoza pack 2026-10-08). Kinds not listed stay plain:
  // built-up, business, attractions, farmland and `other`.
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
    ["railway", ["railway"]],
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
  // with round caps a [0, 3] dash draws 1.5 px dots 3 px apart.
  var DISPUTED = {color: "#c4c4c4", width: 1.5, dash: [0, 3]};
  // Saturated transit context. Drafts measured with pipeline/linecolour
  // (CIE76) on 2026-10-08: every blue tried sat under 45 from Retail blue
  // or the backup teal, so ferries are crimson (59 from the border, 63
  // from violet) and aerial lifts burnt orange (72 from olive).
  var FERRY = {color: "#b0004f", dash: [3, 2]};
  var AERIALWAY = {color: "#d84315"};
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
      if (layer["source-layer"] === "roads" && layer.type === "line") {
        andClause(layer, ["!in", "kind_detail"].concat(DROP_DETAIL),
          ["!", ["in", ["coalesce", ["get", "kind_detail"], ""], ["literal", DROP_DETAIL]]]);
      }
      if (id === "boundaries_country") {
        andClause(layer, ["all", ["!has", "disputed"], ["!=", "kind", "unrecognized_country"]],
          ["all", ["!", ["has", "disputed"]], ["!=", ["get", "kind"], "unrecognized_country"]]);
        out.push(layer);
        out.push({
          id: "travel_boundaries_disputed", type: "line", source: src,
          "source-layer": "boundaries",
          filter: ["any", ["has", "disputed"], ["==", "kind", "unrecognized_country"]],
          layout: {"line-cap": "round", "line-join": "round"},
          paint: {"line-color": DISPUTED.color, "line-width": DISPUTED.width,
                  "line-dasharray": DISPUTED.dash}
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
          paint: {"line-color": FERRY.color, "line-dasharray": FERRY.dash,
                  "line-width": lineWidth([11, 1, 16, 3])}
        });
        out.push({
          id: "travel_aerialway", type: "line", source: src, "source-layer": "roads",
          filter: ["==", "kind", "aerialway"],
          paint: {"line-color": AERIALWAY.color, "line-width": lineWidth([11, 1, 16, 2.5])}
        });
      }
    });
    return out;
  };
})();
if (typeof module !== "undefined" && module.exports) module.exports = travelStyle;
