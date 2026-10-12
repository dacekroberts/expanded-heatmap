// Checks that the shared Travel style (pipeline/travel_style.js) hides every
// feature it removes from EVERY layer: no line, casing, label, arrow or fill
// of a hidden feature survives. Owner, 2026-10-08, after a service road's
// name ("Viale del Visarno", Florence) was drawn over a road the style hid.
//
// Each style layer's filter is evaluated against sample features of every
// hidden kind (with bridge, tunnel, one-way, link, shield and name variants)
// and must reject them all; kept kinds must still reach at least one layer.
// Light and dark, city and world, site and full variants are all checked.
// An unknown filter operator fails the check rather than passing silently.
//
//   node scripts/check_travel_style.mjs <@protomaps/basemaps 5.7.2 dist/basemaps.js> [<TravelTrim.java>]
//
// With TravelTrim.java (the builder patch, --travel_trim), its lists must
// equal the style's HIDDEN table, so the packs drop exactly what the style
// hides. The pixel gate (a Travel render of a trimmed and an untrimmed pack
// must match) stays the end-to-end test whenever either side changes.
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";

const [BM, TRIM] = process.argv.slice(2);
if (!BM) {
  console.error("usage: node scripts/check_travel_style.mjs <basemaps.js> [<TravelTrim.java>]");
  process.exit(2);
}
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1")), "..");
const ctx = { window: {}, self: {} };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(readFileSync(BM, "utf8"), ctx);
const bm = ctx.basemaps || ctx.window.basemaps;
const travelStyle = createRequire(import.meta.url)(path.join(ROOT, "pipeline", "travel_style.js"));
const HIDDEN = travelStyle.HIDDEN;

// A small evaluator for the filter forms the style uses, legacy and
// expression. Anything else throws, so a new form cannot pass unchecked.
function ev(f, feat, zoom) {
  if (!Array.isArray(f)) return f;
  const op = f[0];
  const legacy = typeof f[1] === "string";
  const prop = (k) => (k === "$type" ? feat.type : k in feat.props ? feat.props[k] : null);
  switch (op) {
    case "all": return f.slice(1).every((x) => ev(x, feat, zoom));
    case "any": return f.slice(1).some((x) => ev(x, feat, zoom));
    case "none": return !f.slice(1).some((x) => ev(x, feat, zoom));
    case "!": return !ev(f[1], feat, zoom);
    case "has": return f[1] in feat.props;
    case "!has": return !(f[1] in feat.props);
    case "get": return prop(f[1]);
    case "literal": return f[1];
    case "zoom": return zoom;
    case "geometry-type": return feat.type;
    case "coalesce": {
      for (const x of f.slice(1)) { const v = ev(x, feat, zoom); if (v !== null && v !== undefined) return v; }
      return null;
    }
    case "length": { const v = ev(f[1], feat, zoom); return v === null ? 0 : v.length; }
    case "to-string": { const v = ev(f[1], feat, zoom); return v === null ? "" : String(v); }
    case "in":
      if (legacy) return f.slice(2).includes(prop(f[1]));
      { const hay = ev(f[2], feat, zoom); return Array.isArray(hay) || typeof hay === "string" ? hay.includes(ev(f[1], feat, zoom)) : false; }
    case "!in": return !f.slice(2).includes(prop(f[1]));
    case "==": case "!=": case "<": case "<=": case ">": case ">=": {
      const a = legacy ? prop(f[1]) : ev(f[1], feat, zoom);
      const b = legacy ? f[2] : ev(f[2], feat, zoom);
      if (op === "==") return a === b;
      if (op === "!=") return a !== b;
      if (a === null || b === null) return false;
      return op === "<" ? a < b : op === "<=" ? a <= b : op === ">" ? a > b : a >= b;
    }
    default: throw new Error(`unknown filter operator ${JSON.stringify(op)} in ${JSON.stringify(f).slice(0, 120)}`);
  }
}
function draws(layer, feat) {
  if (layer["source-layer"] !== feat.layer) return false;
  if (!layer.filter) return true;
  return [10, 13, 15, 17].some((z) => ev(layer.filter, feat, z));
}

const VARIANTS = [{}, { is_bridge: true }, { is_tunnel: true }, { oneway: "yes" }, { is_link: true },
  { shield_text: "A1", network: "x" }, { name: "Viale del Visarno", "name:en": "Viale del Visarno" }];
const line = (layer, props) => VARIANTS.map((v) => ({ layer, type: "LineString", props: { ...props, ...v } }));
const poly = (layer, props) => [{ layer, type: "Polygon", props: { name: "x", ...props } }];
const point = (layer, props) => [{ layer, type: "Point", props: { name: "x", ...props } }];

const hiddenSamples = [
  ...HIDDEN.roads.kind_detail.flatMap((d) => line("roads", { kind: d === "track" ? "path" : "minor_road", kind_detail: d })),
  ...line("roads", { kind: "other", kind_detail: "alley" }),
  ...HIDDEN.roads.kind.flatMap((k) => line("roads", { kind: k, kind_detail: k })),
  ...HIDDEN.boundaries.kind.flatMap((k) => [...line("boundaries", { kind: k, kind_detail: 6 }),
                                            ...line("boundaries", { kind: k, kind_detail: 8, disputed: true })]),
  ...["residential", "grass", "farmland", "industrial", "commercial", "retail", "military", "railway", "pitch",
      "other", "zoo", "parking", "construction"].flatMap((k) => poly("landuse", { kind: k })),
  ...HIDDEN.dropLayers.flatMap((l) => [...point(l, { kind: "cafe" }), ...poly(l, { kind: "forest" })]),
];
const keptSamples = [
  ...line("roads", { kind: "minor_road", kind_detail: "residential", name: "Via X" }),
  ...line("roads", { kind: "major_road", kind_detail: "primary", name: "Viale Y" }),
  ...line("roads", { kind: "ferry" }),
  ...line("roads", { kind: "aerialway", kind_detail: "cable_car" }),
  ...line("boundaries", { kind: "country", kind_detail: 2 }),
  ...line("boundaries", { kind: "country", kind_detail: 2, disputed: true }),
  ...line("boundaries", { kind: "region", kind_detail: 4 }),
  ...HIDDEN.landuse.keepOnlyKind.flatMap((k) => poly("landuse", { kind: k })),
];

let fails = 0;
const fail = (msg) => { fails++; if (fails <= 40) console.log("FAIL", msg); };
for (const flavor of ["light", "dark"]) {
  const stock = bm.layers("protomaps", bm.namedFlavor(flavor), { lang: "en" });
  for (const world of [false, true]) {
    for (const variant of ["site", "full"]) {
      const tag = `${flavor}${world ? " world" : ""} ${variant}`;
      let layers;
      try { layers = travelStyle(stock, { flavor, world, variant }); } catch (e) { fail(`${tag}: style threw ${e}`); continue; }
      for (const s of hiddenSamples) {
        for (const l of layers) {
          try {
            if (draws(l, s)) fail(`${tag}: layer ${l.id} draws hidden ${s.layer} ${JSON.stringify(s.props)}`);
          } catch (e) { fail(`${tag}: ${l.id}: ${e.message}`); }
        }
      }
      for (const l of layers) {
        const uses = JSON.stringify([(l.layout || {})["icon-image"], (l.paint || {})["fill-pattern"],
                                     (l.paint || {})["line-pattern"]]);
        if (uses !== "[null,null,null]" && uses !== "[]" && !/^\[(null,?)*\]$/.test(uses)) {
          fail(`${tag}: layer ${l.id} uses a sprite image; the Travel style ships none`);
        }
      }
      const kept = world ? keptSamples.filter((s) => s.layer === "boundaries" && s.props.kind === "country") : keptSamples;
      for (const s of kept) {
        if (!layers.some((l) => draws(l, s))) fail(`${tag}: nothing draws kept ${s.layer} ${JSON.stringify(s.props)}`);
      }
    }
  }
}

if (TRIM) {
  const java = readFileSync(TRIM, "utf8");
  const set = (name) => {
    const m = java.match(new RegExp(`${name} = Set\\.of\\(([^;]*)\\);`));
    return m ? new Set([...m[1].matchAll(/"([^"]+)"/g)].map((x) => x[1])) : null;
  };
  const same = (a, b) => a && a.size === b.length && b.every((x) => a.has(x));
  if (!same(set("LANDUSE_DRAWN"), HIDDEN.landuse.keepOnlyKind)) fail("TravelTrim.LANDUSE_DRAWN differs from HIDDEN.landuse.keepOnlyKind");
  if (!same(set("ROAD_DETAIL_DROPPED"), HIDDEN.roads.kind_detail)) fail("TravelTrim.ROAD_DETAIL_DROPPED differs from HIDDEN.roads.kind_detail");
  for (const k of HIDDEN.roads.kind) if (!java.includes(`"${k}".equals(kind)`)) fail(`TravelTrim does not drop road kind ${k}`);
  for (const k of HIDDEN.boundaries.kind) if (!java.includes(`"${k}".equals(kind)`)) fail(`TravelTrim does not drop boundary kind ${k}`);
}

console.log(fails ? `FAIL: ${fails} problem(s)` : `OK: ${hiddenSamples.length} hidden samples rejected by every layer, ${keptSamples.length} kept samples drawn, in 8 style variants${TRIM ? "; builder trim lists match" : ""}`);
process.exit(fails ? 1 : 0);
