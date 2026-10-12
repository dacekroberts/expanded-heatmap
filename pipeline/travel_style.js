// THE SHARED TRAVEL STYLE (draft, branch only). One function that turns the
// layer list of @protomaps/basemaps 5.7.2 into the Travel basemap shared by
// the site's Travel view and the full Travel version (owner, 2026-10-08;
// rules in DECISIONS.md, the basemap entries of that date). Every hex
// value is a draft. pipeline/map_common.py inlines this file into the
// OpenBasemap layer, so it is the one reference for the style.
//
//   travelStyle(layers, {flavor: "light", world: false, variant: "site", lang: "en"})
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
  // Dark: INTERIM, until the dark tints are drafted. The same
  // categories as light (scripts/check_travel_style.mjs found gardens,
  // meadows and platforms undrawn in dark when it kept 5.7.2's own fills),
  // in 5.7.2's dark flavor colours; platforms take a dark lavender.
  var TINT_DARK = {
    earth: null,
    park: "#192a24",
    wild: "#202121",
    cemetery: "#1c2421",
    sand: "#28282a",
    natural: "#1c1c1c",
    institution: "#252424",
    platform: "#2b2838",
    aerodrome: "#1e1e1e",
    runway: null
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
  // 5.7.2's own land-use fills, replaced in every flavor by LANDUSE.
  var STOCK_LANDUSE = ["landuse_park", "landuse_urban_green", "landuse_hospital",
                       "landuse_industrial", "landuse_school", "landuse_beach",
                       "landuse_zoo", "landuse_aerodrome"];
  // Dropped outright: land cover (an empty stand-in in self-built packs),
  // points of interest, road shields and the basemap's own rail (the
  // site's lines are drawn over it).
  // One-way arrows too: driving detail, and with the town dot and capital
  // star stripped below they were the last sprite icons, so the Travel
  // style needs no sprite sheet and no icon licence (owner, 2026-10-08).
  var DROP = ["landcover", "pois", "roads_shields", "roads_rail", "roads_oneway"];
  // Road details the rules drop, matched on kind_detail (Roads.java copies
  // OSM's service=* there).
  var DROP_DETAIL = ["service", "driveway", "parking_aisle", "alley", "track",
                     "drive-through"];
  // WHAT THE TRAVEL MAP HIDES, per source layer, applied to EVERY style
  // layer that reads that source layer (lines, casings, labels, arrows,
  // fills), so a hidden feature leaves nothing behind: a service road's
  // name once floated over nothing (Florence's Viale del Visarno,
  // 2026-10-08; owner asked for a check, scripts/check_travel_style.mjs).
  // The build-time trim (--travel_trim, TravelTrim.java in the builder
  // patch) drops the same features from the packs; a Travel render of a
  // trimmed and an untrimmed pack must match to the pixel.
  var KEPT_LANDUSE = LANDUSE.reduce(function (all, g) { return all.concat(g[1]); }, [])
    .concat(["pedestrian", "dam", "pier", "runway", "taxiway"]);
  var HIDDEN = {
    dropLayers: ["pois", "landcover"],
    roads: {kind: ["rail"], kind_detail: DROP_DETAIL},
    boundaries: {kind: ["county", "locality"]},
    landuse: {keepOnlyKind: KEPT_LANDUSE}
  };
  // Disputed lines (owner, 2026-10-08): one neutral style everywhere, lighter
  // than the settled border and dotted where it is dashed. Width 1.5 px;
  // with round caps a [0, 1.5] dash draws 1.5 px dots 2.25 px apart centre
  // to centre. Owner asked for a tighter dash than [0, 3]; of [0, 3],
  // [0, 2] and [0, 1.5] compared on world-zoom crops (2026-10-08), only
  // [0, 1.5] keeps short segments such as Kashmir's reading as a line.
  // Every unrecognized kind takes the same rule (owner, 2026-10-08).
  // Dark (owner approved, 2026-10-11): as faint against the dark land as the light
  // one is against the light land, and below the settled border #5b6374.
  var DISPUTED = {color: "#c4c4c4", colorDark: "#4a4f5a", width: 1.5, dash: [0, 1.5]};
  var UNRECOGNIZED = ["unrecognized_country", "unrecognized_region", "unrecognized_macroregion"];
  // Ferries and aerial lifts are told apart from operators' line colours by
  // pattern first (owner, 2026-10-08). Ferries
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
  // Dark flavor (owner approved; measured 2026-10-11 against 5.7.2's dark water
  // #31353f and land #1f1f1f): the light colours read 1.7:1 (crimson) and
  // 1.3:1 (lift grey) on the dark water, so each takes a lighter form of
  // the same hue: pink 4.0:1 on water and 47 from Marunouchi red, blue
  // 4.6:1, lift grey 7.3:1. Re-measure if the dark flavor's water or land
  // colour changes.
  var FERRY = {site: "#b0004f", full: "#1e88e5", siteDark: "#f06292", fullDark: "#42a5f5",
               dash: [3, 2]};
  var AERIALWAY = {color: "#444444", colorDark: "#c8c8c8", tickWidth: 6, tickDash: [0.15, 2.5]};
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
  // The HIDDEN rule for one layer, in its own filter syntax; null when the
  // layer reads nothing HIDDEN covers.
  function hideClause(layer) {
    var sl = layer["source-layer"];
    var get = function (k) { return ["coalesce", ["get", k], ""]; };
    if (sl === "roads") {
      return [["all", ["!in", "kind"].concat(HIDDEN.roads.kind),
                      ["!in", "kind_detail"].concat(HIDDEN.roads.kind_detail)],
              ["all", ["!", ["in", get("kind"), ["literal", HIDDEN.roads.kind]]],
                      ["!", ["in", get("kind_detail"), ["literal", HIDDEN.roads.kind_detail]]]]];
    }
    if (sl === "boundaries") {
      return [["!in", "kind"].concat(HIDDEN.boundaries.kind),
              ["!", ["in", get("kind"), ["literal", HIDDEN.boundaries.kind]]]];
    }
    if (sl === "landuse") {
      return [["in", "kind"].concat(HIDDEN.landuse.keepOnlyKind),
              ["in", get("kind"), ["literal", HIDDEN.landuse.keepOnlyKind]]];
    }
    return null;
  }
  function lineWidth(z) {
    return ["interpolate", ["exponential", 1.6], ["zoom"]].concat(z);
  }

  function style(layers, opts) {
    opts = opts || {};
    var light = (opts.flavor || "light") === "light";
    var variant = opts.variant === "full" ? "full" : "site";
    var ferry = FERRY[variant + (light ? "" : "Dark")];
    var lift = light ? AERIALWAY.color : AERIALWAY.colorDark;
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
        if (landuseDone) return;
        landuseDone = true;
        LANDUSE.forEach(function (group) {
          out.push({
            id: "travel_landuse_" + group[0], type: "fill", source: src,
            "source-layer": "landuse",
            filter: ["in", "kind"].concat(group[1]),
            paint: {"fill-color": (light ? TINT : TINT_DARK)[group[0]]}
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
          paint: {"line-color": light ? DISPUTED.color : DISPUTED.colorDark, "line-width": DISPUTED.width,
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
          paint: {"line-color": ferry, "line-dasharray": FERRY.dash,
                  "line-width": lineWidth([11, 1, 16, 3])}
        });
        out.push({
          id: "travel_aerialway", type: "line", source: src, "source-layer": "roads",
          filter: ["==", "kind", "aerialway"],
          paint: {"line-color": lift, "line-width": lineWidth([11, 0.8, 16, 1.5])}
        });
        // Cross ticks: a wide line whose dashes are much shorter than it is
        // wide draws short bars across the cable.
        out.push({
          id: "travel_aerialway_ticks", type: "line", source: src, "source-layer": "roads",
          filter: ["==", "kind", "aerialway"], minzoom: 13,
          paint: {"line-color": lift, "line-width": AERIALWAY.tickWidth,
                  "line-dasharray": AERIALWAY.tickDash}
        });
      }
      if (id === "roads_labels_major") {
        // Ferry and lift routes are named along the line in their own
        // colour, since a crimson or blue dash stands out and needs saying
        // what it is (owner, 2026-10-08; "Arno Boat" in Florence, "Bac du
        // Rocher des Doms" in Avignon). The label language follows the pill.
        var name = ["coalesce", ["get", "name:" + (opts.lang || "en")], ["get", "name"]];
        [["ferry", ferry], ["aerialway", lift]].forEach(function (k) {
          out.push({
            id: "travel_" + k[0] + "_label", type: "symbol", source: src, "source-layer": "roads",
            filter: ["==", "kind", k[0]], minzoom: 12,
            layout: {"symbol-placement": "line", "text-field": name, "text-font": ["Noto Sans Italic"],
                     "text-size": 12, "text-letter-spacing": 0.05},
            paint: {"text-color": k[1], "text-halo-color": light ? "#ffffff" : "#1f1f1f",
                    "text-halo-width": 1.5}
          });
        });
      }
    });
    // Last, so no layer added above or by a later edit escapes it.
    out = out.filter(function (l) { return HIDDEN.dropLayers.indexOf(l["source-layer"]) < 0; });
    // No sprite images anywhere (places_locality's town dot and capital
    // star below z8 are the only ones left after DROP).
    out.forEach(function (l) {
      if (l.layout) delete l.layout["icon-image"];
    });
    out.forEach(function (l) {
      var c = hideClause(l);
      if (c) andClause(l, c[0], c[1]);
    });
    return out;
  }
  style.HIDDEN = HIDDEN;
  return style;
})();
if (typeof module !== "undefined" && module.exports) module.exports = travelStyle;
