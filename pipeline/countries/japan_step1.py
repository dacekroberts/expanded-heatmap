"""Step 1 for every Japanese city: stations and line geometry from MLIT N02, cut
at the city line. Built for Kobe (2026-09-27), the first Japanese city, and
written here from the start so Osaka, Sapporo, Fukuoka, Kyoto and Tokyo share
one copy. A city's step 1 calls run(config).

  * Stations: N02's, the Shinkansen dropped (japan.stations(); owner
    2026-09-24) and any config.LEFT_OUT_LINES left out, each station a platform
    centroid. Kept only inside the city line (MLIT N03, the city's wards) -
    which is used to PICK, never drawn (the Survey Act; japan.city_boundary).
  * Collapse on N02's STATION-GROUP CODE (N02_005g), never the name. Measured
    in Kobe: the name joins two 長田 1.5 km apart (the subway's and Kobe
    Electric's) and two 御影 1.1 km apart (Hankyu's and Hanshin's); the group
    code merges only real interchanges (三宮, 新長田, 新開地). A spread check
    stops a group wider than config.COLLAPSE_MAX_SPREAD_M.
  * English names: OpenStreetMap's name:en (N02 carries Japanese only; owner
    2026-09-27, the Seoul/Taichung precedent of English plus native), matched
    on the Japanese name within config.OSM_NAME_MATCH_M of the group. A station
    with no match, or a split vote, STOPS the step - never a guess.
  * Lines: N02 RailroadSection geometry of each drawn line within
    DRAW_BEYOND_M of the city. N02 files a public line under its LEGAL
    sections (Kobe's Seishin-Yamate Line is 山手線 + 西神線 + 西神延伸線), so
    config.LINES maps each drawn line to its (operator, line) pairs. A branch
    with its own public name inside one N02 line (Kobe's Wadamisaki Line in
    JR's 山陽線) is config.BRANCHES, split off by walking the track graph. A
    branch may instead be drawn as another line (`draw_as`) or left out
    (`draw_as: None`) - Osaka's Umeda freight track in 東海道線. A public
    SERVICE that runs over parts of several legal lines, stopping at some of
    their stations (Tokyo's JR East: the Yamanote over 山手線, 東北線 and
    東海道線), is a LINES entry with a `route` (route_sections, below).
  * Excluded: the drawn lines' stations beyond the city line, named by their N03
    municipality. A left-out line's stations are printed, not written there.

Config needs: SLUG, NAME, CITY_BBOX, CRS_*, STATION_OSM_JSON, OSM_NAME_MATCH_M,
COLLAPSE_MAX_SPREAD_M, LEFT_OUT_LINES, LINES, LINE_ORDER, LINE_NAMES, BRANCHES,
GATE3, STATIONS_CSV, EXCLUDED_STATIONS_CSV, LINES_GEOJSON, DATA_PROCESSED,
OUTPUTS. Reads the cache and NEVER fetches.
"""
import collections
import json
import re
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, mapping
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries import japan  # noqa: E402

# Lines are drawn a little past the city line, so a line visibly carries on
# rather than stopping dead at an edge the map does not show.
DRAW_BEYOND_M = 3000
# A branch's junction: track within this of the junction station is where the
# walk from the terminus stops.
JUNCTION_M = 150


def nfkc(s):
    return unicodedata.normalize("NFKC", s or "").strip()


def draw_key(key, b):
    """The drawn line a branch's track belongs to: its own key (Kobe's
    Wadamisaki Line), another line's (`draw_as`: Osaka's Umekita track is drawn
    as the Osaka Higashi Line, whose trains run on it), or None - left out
    (Osaka's Umekita-Fukushima track, limited expresses only)."""
    return b.get("draw_as", key)


def branch_only(config):
    """LINES keys drawn only from a branch walk, never from their N02 line."""
    return {k for k, b in config.BRANCHES.items() if draw_key(k, b) == k}


def left_out(config, op, line, name):
    """A station row on a left-out line, or one of a left-out branch's own."""
    return (op, line) in config.LEFT_OUT_LINES or any(
        (op, line) == b["line"] and draw_key(k, b) is None and name in b["stations"]
        for k, b in config.BRANCHES.items())


def line_keys(config, op, line, name):
    """The drawn line(s) a N02 station row belongs to; () for a left-out line."""
    if left_out(config, op, line, name):
        return ()
    branch_keys = set()
    for bkey, b in config.BRANCHES.items():
        draw = draw_key(bkey, b)
        if (op, line) == b["line"] and draw:
            if name in b["stations"]:
                return (draw,)
            # the junction serves both lines; `shared` names every station a
            # branch shares with its N02 line (Osaka's Umekita track: 大阪, 新大阪)
            if name in b.get("shared", (b["junction"],)):
                branch_keys.add(draw)
    keys = tuple(k for k, v in config.LINES.items()
                 if (op, line) in v.get("n02", ()) and k not in branch_only(config))
    keys += tuple(k for k in route_keys(config, op, line, name) if k not in keys)
    return keys + tuple(sorted(branch_keys - set(keys)))


# --- service routes (Tokyo, 2026-09-28) ----------------------------------------
# N02 files JR East under its LEGAL lines, and one legal line carries several
# public services: 東北線 between 田端 and 東京 is the Yamanote's, the
# Keihin-Tōhoku's and (through 上野) the Utsunomiya Line's track; the Chūō-Sōbu
# Line runs over 中央線 and 総武線. BRANCHES only splits one line in two. A
# LINES entry may instead carry a `route`: legs of (operator, legal line,
# [stops in order]), where an entry written "~名" is passed without stopping
# (geometry only). A station row belongs to the line only where it is a listed
# stop; the line is drawn along its legal line's track between consecutive
# entries. A line may carry both `n02` (whole legal lines) and a `route` (Tokyo's
# Fukutoshin Line: its own line, plus the Yūrakuchō's track it shares to 和光市).
# Two services on one track are drawn over one another (owner 2026-09-28: the
# nine JR services in full rather than each track once).

def route_entry(entry):
    """(station name, is a stop) for a route entry: '~名' is passed through."""
    return entry.lstrip("~"), not entry.startswith("~")


def route_keys(config, op, line, name):
    """The LINES keys whose route STOPS at this N02 station row."""
    return tuple(dict.fromkeys(
        k for k, v in config.LINES.items() for rop, rline, entries in v.get("route", ())
        if (rop, rline) == (op, line) and any(route_entry(e) == (name, True) for e in entries)))


def join_groups(config, st):
    """config.GROUP_JOIN = {(operator, line, name): why}: a platform N02 gave
    its own group code although it is part of a station of the same name, joins
    that station's nearest group (Tokyo, 2026-09-28: the Keiyō Line's 東京
    platforms, 424 m from the rest of Tokyo Station; the Fukutoshin's 池袋, 356
    m, one Ikebukuro to Tokyo Metro). Different stations of one name stay apart
    (両国, 早稲田, the TX's 浅草) and take their operators. Changes st in place."""
    for (op, line, name), _why in getattr(config, "GROUP_JOIN", {}).items():
        m = (st["N02_004"] == op) & (st["N02_003"] == line) & (st["N02_005"] == name)
        if not m.any():
            sys.exit(f"GROUP_JOIN: no {name} on {op} {line}")
        others = st[(st["N02_005"] == name) & ~st["N02_005g"].isin(set(st.loc[m, "N02_005g"]))]
        if others.empty:
            sys.exit(f"GROUP_JOIN: no other {name} group for the {line} platform to join")
        p = st.to_crs(config.CRS_PROJECTED).geometry  # distances in metres, never degrees
        here = unary_union(list(p[m])).centroid
        target = min(others.index.groupby(others["N02_005g"]).items(),
                     key=lambda kv: unary_union(list(p[kv[1]])).centroid.distance(here))[0]
        st.loc[m, "N02_005g"] = target
        print(f"  {name} ({line}) joins the {name} group {target}")


def check_routes(config, st):
    """Every route entry names a station of its leg's legal line within the drawn
    area - a typo, or a station on another legal line, stops the step."""
    have = set(zip(st["N02_004"], st["N02_003"], st["N02_005"]))
    bad = [f"{config.LINES[k]['name']}: {e} not on {op} {line}"
           for k, v in config.LINES.items() for op, line, entries in v.get("route", ())
           for e in entries if (op, line, route_entry(e)[0]) not in have]
    if bad:
        sys.exit("route entries naming no N02 station of their leg:\n  " + "\n  ".join(bad))


def route_sections(config, key, sec, pair, st):
    """Index of the N02 sections a line's route runs over: per leg, the shortest
    path along its legal line's track between each pair of consecutive entries
    (Dijkstra over the sections' end points, in metres)."""
    import heapq
    idx = set()
    for op, line, entries in config.LINES[key].get("route", ()):
        s = sec[pair == (op, line)].to_crs(config.CRS_PROJECTED)
        by_node = collections.defaultdict(list)
        for i, g in zip(s.index, s.geometry):
            a, b = _ends(g)
            by_node[a].append((b, i, g.length))
            by_node[b].append((a, i, g.length))
        # N02's track can arrive in pieces (Tokyo's 東北線: an 8-node piece at
        # 日暮里, 67 m from the rest), so both ends of a hop are taken from the
        # one connected piece that lies closest to both stations
        piece, n_piece = {}, 0
        for n0 in by_node:
            if n0 in piece:
                continue
            todo = [n0]
            while todo:
                n = todo.pop()
                if n not in piece:
                    piece[n] = n_piece
                    todo.extend(m for m, _, _ in by_node[n])
            n_piece += 1
        plat = st[(st["N02_004"] == op) & (st["N02_003"] == line)].to_crs(config.CRS_PROJECTED)

        def at(name):
            return unary_union(list(plat[plat["N02_005"] == route_entry(name)[0]].geometry)).centroid

        def ends_of_hop(p1, p2):
            best = None
            for c in range(n_piece):
                ns = [n for n in by_node if piece[n] == c]
                a = min(ns, key=lambda n: Point(n).distance(p1))
                b = min(ns, key=lambda n: Point(n).distance(p2))
                d = Point(a).distance(p1) + Point(b).distance(p2)
                if best is None or d < best[0]:
                    best = (d, a, b)
            return best[1], best[2]

        for e1, e2 in zip(entries, entries[1:]):
            start, goal = ends_of_hop(at(e1), at(e2))
            dist, prev, todo = {start: 0.0}, {}, [(0.0, start)]
            while todo:
                d, n = heapq.heappop(todo)
                if n == goal:
                    break
                if d > dist[n]:
                    continue
                for m, i, length in by_node[n]:
                    if d + length < dist.get(m, float("inf")):
                        dist[m], prev[m] = d + length, (n, i)
                        heapq.heappush(todo, (d + length, m))
            if goal not in dist:
                sys.exit(f"the {config.LINE_NAMES[key]}: no track on {op} {line} from {e1} to {e2}")
            n = goal
            while n != start:
                n, i = prev[n]
                idx.add(i)
    return idx


def n03_municipalities(config):
    pref = japan.CITIES[config.SLUG]["pref"]
    z = japan.SHARED_RAW / japan.N03_ZIP_TEMPLATE.format(pref=pref)
    n03 = japan._read_geojson(z, z.name.replace("_GML.zip", ".geojson")).to_crs(config.CRS_GEOGRAPHIC)
    n03["muni"] = n03["N03_004"].fillna("") + n03["N03_005"].fillna("")
    return n03.dissolve("muni").reset_index()[["muni", "geometry"]]


def no_data_ward_polygons(config, nodata):
    """[(English ward name, polygon)] for config.NO_DATA_WARDS, from N03 read
    once - which ward a hollow station's tooltip names."""
    pref = japan.CITIES[config.SLUG]["pref"]
    z = japan.SHARED_RAW / japan.N03_ZIP_TEMPLATE.format(pref=pref)
    n03 = japan._read_geojson(z, z.name.replace("_GML.zip", ".geojson")).to_crs(config.CRS_GEOGRAPHIC)
    n03 = n03[n03["N03_007"].isin(list(nodata))].dissolve("N03_007")
    missing = set(nodata) - set(n03.index)
    if missing:
        sys.exit(f"NO_DATA_WARDS names ward code(s) N03 does not have: {sorted(missing)}")
    return [(nodata[code], geom) for code, geom in zip(n03.index, n03.geometry)]


def english_names(config, groups):
    # the station query's file, and - in a city with a tram - the tram-stop
    # query's (Osaka's Hankai stops; japan.osm_tram_stop_query)
    paths = [config.STATION_OSM_JSON] + ([config.TRAM_OSM_JSON] if hasattr(config, "TRAM_OSM_JSON") else [])
    rows = []
    for path in paths:
        if not path.exists():
            sys.exit(f"missing {path}\nRun: python pipeline/{config.SLUG}/fetch_sources.py osm")
        for el in json.loads(path.read_text(encoding="utf-8"))["elements"]:
            t = el.get("tags") or {}
            lat, lon = (el["lat"], el["lon"]) if el["type"] == "node" else (el["center"]["lat"], el["center"]["lon"])
            rows.append({"name": nfkc(t.get("name")), "en": (t.get("name:en") or "").strip(),
                         "geometry": Point(lon, lat)})
    osm = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    osm = osm[osm["en"] != ""]
    g = groups.to_crs(config.CRS_PROJECTED)
    aliases = getattr(config, "OSM_NAME_ALIASES", {})
    # Where OSM's object has no name:en at all, the city's config may name it,
    # explicitly and with its evidence (Osaka's JR 平野); used ONLY when no
    # object in range carries a name:en.
    no_en = getattr(config, "OSM_NAME_EN_MISSING", {})
    out, missing, filled = {}, [], []
    for gid, name, pt in zip(g["group"], g["name_ja"], g.geometry):
        want = nfkc(aliases.get(name, name))
        near = osm[(osm["name"] == want) & (osm.distance(pt) <= config.OSM_NAME_MATCH_M)]
        votes = collections.Counter(near["en"])
        if not votes and name in no_en:
            out[gid] = no_en[name]
            filled.append(f"{name} -> {no_en[name]}")
            continue
        if not votes:
            missing.append(f"{name} (group {gid})")
            continue
        (en, n), *rest = votes.most_common()
        if rest and rest[0][1] == n:
            # A tie is settled only by the city's config, naming the spelling it
            # chose and why (Kobe: Hankyu's and Hanshin's 神戸三宮 objects).
            chosen = getattr(config, "OSM_NAME_EN_TIES", {}).get(name)
            if chosen not in votes:
                sys.exit(f"{name}: OSM's name:en is split {dict(votes)} - settle it in "
                         "config.OSM_NAME_EN_TIES with one of these spellings")
            en = chosen
        out[gid] = en
    if missing:
        sys.exit(f"no OSM name:en within {config.OSM_NAME_MATCH_M} m for: {', '.join(missing)}")
    if filled:
        print(f"  English names from config.OSM_NAME_EN_MISSING (OSM has none): {', '.join(filled)}")
    # The city's cited overrides of OSM's spelling (Sapporo's spelled-out
    # "Kita juhachi jo" for 北18条; owner 2026-09-28): each replaces what OSM
    # gave, and one naming no station here is a typo, so it stops.
    overrides = getattr(config, "OSM_NAME_EN_OVERRIDES", {})
    by_name = dict(zip(g["group"], g["name_ja"]))
    unknown = sorted(set(overrides) - set(by_name.values()))
    if unknown:
        sys.exit(f"config.OSM_NAME_EN_OVERRIDES names no station in the city: {', '.join(unknown)}")
    changed = []
    for gid, name in by_name.items():
        if name in overrides and out.get(gid) != overrides[name]:
            changed.append(f"{name}: {out.get(gid)!r} -> {overrides[name]!r}")
            out[gid] = overrides[name]
    if changed:
        print(f"  {len(changed)} English names from config.OSM_NAME_EN_OVERRIDES:")
        for c in changed:
            print(f"    {c}")
    # Numerals as figures (owner 2026-09-28, every Japanese city): a number
    # before 丁目 in the Japanese name, in digits or kanji, appears as that
    # figure in the English one ("Nishi-11-Chome", never "Nishi juitchome").
    # Before 条 only where the city's 条 is a numbered street grid, declared
    # as config.JO_IS_GRID (Sapporo's 北18条 -> Kita-18-Jo); elsewhere 条 is
    # part of a name and keeps its signed word (Osaka's Kujō and Nishikujō,
    # Kyoto's Shijō, Tokyo's Jūjō; owner 2026-09-28).
    jo_grid = getattr(config, "JO_IS_GRID", False)
    bad = [f"{by_name[gid]} -> {en!r} (needs {', '.join(map(str, nums))})"
           for gid, en in out.items()
           if (nums := block_numbers(by_name[gid], jo_grid))
           and not all(re.search(rf"(?<!\d){n}(?!\d)", en) for n in nums)]
    if bad:
        sys.exit("English names must write a 丁目 / 条 number as a figure (owner 2026-09-28); "
                 "add config.OSM_NAME_EN_OVERRIDES for:\n  " + "\n  ".join(bad))
    return out


_KANJI_DIGIT = dict(zip("〇一二三四五六七八九", range(10)))


def kanji_number(s):
    """A kanji numeral up to 99 (十八, 二十四, 九) as an int; digits pass through."""
    if s.isdigit():
        return int(s)
    tens, _, ones = s.partition("十")
    if "十" not in s:
        return _KANJI_DIGIT[s] if len(s) == 1 else int("".join(str(_KANJI_DIGIT[c]) for c in s))
    return (_KANJI_DIGIT[tens] if tens else 1) * 10 + (_KANJI_DIGIT[ones] if ones else 0)


def block_numbers(name, jo_grid=False):
    """The block numbers a Japanese station name carries: before 丁目 always
    (天神橋筋六丁目 -> [6]), before 条 only on a numbered street grid
    (Sapporo's 北18条 -> [18]). A place name that merely contains a numeral
    (二十四軒, or Osaka's 九条 off a grid) has none."""
    marker = "丁目|条" if jo_grid else "丁目"
    return [kanji_number(m) for m in re.findall(rf"(\d+|[〇一二三四五六七八九十]+)(?={marker})", nfkc(name))]


assert block_numbers("北18条", jo_grid=True) == [18] and block_numbers("天神橋筋六丁目") == [6]
assert block_numbers("二十四軒") == [] and block_numbers("南郷十三丁目") == [13]
assert block_numbers("西線9条旭山公園通", jo_grid=True) == [9] and kanji_number("二十四") == 24
assert block_numbers("西九条") == [] and block_numbers("四条") == []


def _ends(g):
    c = list(g.coords) if g.geom_type == "LineString" else [p for part in g.geoms for p in part.coords]
    return (round(c[0][0]), round(c[0][1])), (round(c[-1][0]), round(c[-1][1]))


def _platform_at(config, st, name, at):
    """A named platform's point: the only one, or - where N02 has several under
    one name (Osaka's 大阪: four main-line platforms and the Umekita one) - the
    one within 50 m of `at` (lat, lon), which the config takes from N02."""
    rows = st[st["N02_005"] == name]
    if at is None:
        return rows.geometry.iloc[0]
    p = gpd.GeoSeries([Point(at[1], at[0])], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).iloc[0]
    d = rows.distance(p)
    if not len(d) or d.min() > 50:
        sys.exit(f"no {name} platform within 50 m of {at}")
    return p


def branch_split(config, key, sections, claimed=()):
    """Index of the N02 sections reachable from the branch's terminus without
    passing its junction station. Sections an earlier branch `claimed` are not
    walked, so BRANCHES' ORDER matters (Osaka: the left-out Umekita-Fukushima
    track first, then the Umekita track the Osaka Higashi Line runs on)."""
    b = config.BRANCHES[key]
    st = japan.stations(slug=config.SLUG)
    st = st[(st["N02_004"] == b["line"][0]) & (st["N02_003"] == b["line"][1])].to_crs(config.CRS_PROJECTED)
    term = _platform_at(config, st, b["terminus"], b.get("terminus_at"))
    if "junction_at" in b:
        junc = _platform_at(config, st, b["junction"], b["junction_at"])
    else:
        junc = unary_union(list(st[st["N02_005"] == b["junction"]].geometry)).centroid
    junction_m = b.get("junction_m", JUNCTION_M)
    sec = sections.drop(index=list(claimed), errors="ignore").to_crs(config.CRS_PROJECTED)
    by_node = collections.defaultdict(set)
    for i, g in zip(sec.index, sec.geometry):
        for n in _ends(g):
            by_node[n].add(i)
    seen, todo = set(), [min(sec.index, key=lambda i: sec.geometry[i].distance(term))]
    while todo:
        i = todo.pop()
        if i in seen:
            continue
        seen.add(i)
        for n in _ends(sec.geometry[i]):
            if Point(n).distance(junc) > junction_m:
                todo.extend(by_node[n] - seen)
    length = sum(sec.geometry[i].length for i in seen)
    lo, hi = b["length_m"]
    label = b.get("label") or config.LINE_NAMES[key]
    if not lo <= length <= hi:
        sys.exit(f"the {label} walked to {length:.0f} m of track, outside {lo}-{hi} m - read the section graph")
    draw = draw_key(key, b)
    how = "left out" if draw is None else ("drawn as the " + config.LINE_NAMES[draw]) if draw != key else "drawn"
    print(f"  {label}: {len(seen)} N02 sections, {length:.0f} m, split off {b['line'][1]}; {how}")
    return sorted(seen)


def write_lines(config, near, st):
    _, zp, _, member = japan.n02(config.SLUG)
    sec = japan._read_geojson(zp, member).to_crs(config.CRS_GEOGRAPHIC)
    sec = sec[sec["N02_002"] != japan.SHINKANSEN]
    sec = sec[sec.geometry.intersects(near)]
    pair = pd.Series(list(zip(sec["N02_004"], sec["N02_003"])), index=sec.index)
    branch, in_branch = {}, set()
    for k, b in config.BRANCHES.items():
        branch[k] = branch_split(config, k, sec[pair == b["line"]], in_branch)
        in_branch |= set(branch[k])
    only = branch_only(config)
    feats = []
    for key, spec in config.LINES.items():
        if key in only:
            idx = set(branch[key])
        else:
            idx = set(sec.index[pair.isin(spec.get("n02", [])) & ~sec.index.isin(in_branch)])
        # a branch drawn as this line (Osaka's Umekita track, the Osaka Higashi Line's)
        idx |= {i for k, b in config.BRANCHES.items() if k not in only and draw_key(k, b) == key for i in branch[k]}
        if "route" in spec:
            idx |= route_sections(config, key, sec, pair, st)
        parts = sec.loc[sorted(idx)]
        if parts.empty:
            sys.exit(f"no N02 track for the {spec['name']}")
        feats.append({"type": "Feature", "properties": {"line": key},
                      "geometry": mapping(unary_union(list(parts.geometry)))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")
    print(f"  line geometry -> {config.LINES_GEOJSON.name} ({len(feats)} lines)")


def run(config):
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    # Wards with NO business data (config.NO_DATA_WARDS, {code: English name};
    # Tokyo's, owner 2026-09-28): inside the city line, so their stations are
    # drawn, but hollow and ringless (map_common). Without it the city is the
    # data's wards and nothing here changes.
    nodata = dict(getattr(config, "NO_DATA_WARDS", {}))
    active = japan.city_boundary(config.SLUG)
    city = (japan.city_boundary(config.SLUG, wards=[*japan.CITIES[config.SLUG]["wards"], *nodata])
            if nodata else active)
    minx, miny, maxx, maxy = city.bounds
    bb = config.CITY_BBOX
    if not (bb["lon_min"] < minx and maxx < bb["lon_max"] and bb["lat_min"] < miny and maxy < bb["lat_max"]):
        sys.exit(f"the city's N03 extent {city.bounds} is not inside CITY_BBOX {bb}")
    near = gpd.GeoSeries([city], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).buffer(DRAW_BEYOND_M)
    near = near.to_crs(config.CRS_GEOGRAPHIC).iloc[0]

    st = japan.stations(slug=config.SLUG)
    st = st[st.geometry.within(near)].copy()
    check_routes(config, st)
    join_groups(config, st)
    all_near = st.copy()
    st["inside"] = st.geometry.within(city)
    st["active"] = st.geometry.within(active) if nodata else st["inside"]
    st["keys"] = [line_keys(config, o, ln, nm) for o, ln, nm in zip(st["N02_004"], st["N02_003"], st["N02_005"])]
    left = pd.Series([left_out(config, o, ln, nm) for o, ln, nm in zip(st["N02_004"], st["N02_003"], st["N02_005"])],
                     index=st.index)
    unnamed = st[(st["keys"].map(len) == 0) & ~left & st["inside"]]
    if len(unnamed):
        sys.exit("N02 lines with stations in the city that config.LINES does not name: "
                 f"{sorted(set(zip(unnamed['N02_004'], unnamed['N02_003'])))}")
    gone = st[left & st["inside"]]
    print(f"  left out inside the city: {len(gone)} station rows of {sorted(set(gone['N02_003']))}")
    st = st[st["keys"].map(len) > 0].copy()

    # --- collapse on the station-group code ------------------------------------
    rows = st.explode("keys").rename(columns={"keys": "line", "N02_005g": "group", "N02_005": "name_ja"})
    names = rows.groupby("group")["name_ja"].agg(lambda s: sorted(set(s)))
    if (names.map(len) > 1).any():
        sys.exit(f"a station group with several names: {names[names.map(len) > 1].to_dict()}")
    platforms = rows.drop_duplicates(["group", "N02_004", "N02_003"]).to_crs(config.CRS_PROJECTED)
    spread = platforms.groupby("group").geometry.agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    too_far = spread[spread > config.COLLAPSE_MAX_SPREAD_M]
    if len(too_far):
        sys.exit(f"groups wider than {config.COLLAPSE_MAX_SPREAD_M} m: {too_far.round().to_dict()}")
    cent = platforms.groupby("group").geometry.agg(lambda s: unary_union(list(s)).centroid)
    groups = gpd.GeoDataFrame({"group": cent.index, "geometry": list(cent.values)},
                              crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC)
    groups["name_ja"] = groups["group"].map(names.map(lambda v: v[0]))
    groups["lines"] = groups["group"].map(rows.groupby("group")["line"].agg(
        lambda s: " ".join(k for k in config.LINE_ORDER if k in set(s))))
    # A station counts when ANY of its platforms is inside the city line, not
    # its centroid: Osaka's 太子橋今市 has its Tanimachi platform in Asahi-ku
    # and its Imazatosuji platform in Moriguchi, and the centroid falls outside
    # (owner 2026-09-27: keep it). Kobe has no such station.
    groups["inside"] = groups["group"].map(platforms.groupby("group")["inside"].any())
    lines_of = groups.set_index("group")["lines"]
    print(f"\n  {len(platforms)} line-station rows within {DRAW_BEYOND_M / 1000:.0f} km -> "
          f"{len(groups)} stations by group code; widest:")
    for gid in spread.sort_values(ascending=False).head(6).index:
        print(f"    {names[gid][0]:<10} {spread[gid]:>5.0f} m  [{lines_of[gid]}]")

    en = english_names(config, groups[groups["inside"]])
    groups["station"] = groups["group"].map(en)
    groups["latitude"], groups["longitude"] = groups.geometry.y, groups.geometry.x
    keep = groups[groups["inside"]].copy()
    per_line = {k: int(sum(1 for v in keep["lines"] if k in v.split())) for k in config.LINE_ORDER}
    print("\n  stations inside the city, per line:")
    for k in config.LINE_ORDER:
        print(f"    {k:<3} {config.LINE_NAMES[k]:<24} {per_line[k]:>3}")
    in_plat = platforms[platforms["group"].isin(keep["group"])].to_crs(config.CRS_GEOGRAPHIC)
    in_plat = in_plat.assign(latitude=in_plat.geometry.y, longitude=in_plat.geometry.x)
    print()
    # Gate 1's floor: 400 m by default; a city whose stations are mostly tram
    # stops sets config.SPACING_MIN_M (Hiroshima's Hiroden, 2026-09-30: 200 m,
    # the value Paris, Marseille, Amsterdam and Riga take).
    station_gates.verify_stations(
        city=config.NAME, platforms=in_plat, stations=keep, crs_projected=config.CRS_PROJECTED,
        spacing_min=getattr(config, "SPACING_MIN_M", station_gates.STATION_SPACING_MEDIAN_M_MIN),
        expected_per_line={config.LINE_NAMES[k]: n for k, n in config.GATE3["lines"].items()},
        actual_per_line={config.LINE_NAMES[k]: per_line[k] for k in config.GATE3["lines"]})
    print(f"    gate 3 source: {config.GATE3['source']}")

    # --- excluded ---------------------------------------------------------------
    munis = n03_municipalities(config)
    excluded = []
    for _, r in groups[~groups["inside"]].iterrows():
        hit = munis[munis.contains(r.geometry)]
        where = hit.iloc[0]["muni"] if len(hit) == 1 else "another prefecture"
        excluded.append({"station": r["name_ja"], "lines": r["lines"],
                         "reason": f"in {where}, outside {japan.CITIES[config.SLUG]['name']} "
                                   "(the permit list covers the city only)",
                         "latitude": r["latitude"], "longitude": r["longitude"]})
    # A left-out LINE's stations are not written here: the file records stations
    # cut from a network that IS mapped (app/station_scope.py reads only
    # boundary and spacing reasons), as Taipei's undrawn Maokong Gondola is not
    # in its file. The page and docs/excluded_categories.md disclose the line.
    ex = pd.DataFrame(excluded, columns=["station", "lines", "reason", "latitude", "longitude"])
    ex = ex.drop_duplicates(["station", "lines"]).sort_values(["reason", "station"])
    ex.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    where = ex["reason"].str.extract(r"^in (\S+), outside")[0].value_counts()
    print(f"\n  scope: {len(keep)} stations inside the city; {len(ex)} excluded -> "
          f"{config.EXCLUDED_STATIONS_CSV.name}\n    beyond the line: "
          + ", ".join(f"{m} {n}" for m, n in where.items()))

    # Different stations under one name are real (Hankyu's and Hanshin's 御影,
    # 1.1 km apart): only where English names collide, each takes its lines'
    # operators, as config.LINES' `short` spells them - Mikage (Hankyu).
    dup = keep["station"].duplicated(keep=False)
    shorts = keep["lines"].map(lambda v: "/".join(dict.fromkeys(config.LINES[k]["short"] for k in v.split())))
    keep.loc[dup, "station"] = keep.loc[dup, "station"] + " (" + shorts[dup] + ")"
    print(f"  {int(dup.sum())} stations sharing an English name take their operators: "
          + ", ".join(sorted(keep.loc[dup, "station"])))
    kp = keep.to_crs(config.CRS_PROJECTED)
    close = [(a, b, kp.geometry.iloc[i].distance(kp.geometry.iloc[j]))
             for i, a in enumerate(keep["station"]) for j, b in enumerate(keep["station"]) if i < j]
    close = sorted((c for c in close if c[2] < 200), key=lambda c: c[2])
    print(f"  {len(close)} station pairs under 200 m apart (read them: one station under two names?):")
    for a, b, d in close:
        print(f"    {d:>5.0f} m  {a}  /  {b}")

    cols = ["station", "name_ja", "latitude", "longitude", "lines"]
    if nodata:
        # A station with ANY platform in a ward that has data keeps its rings
        # (the 太子橋今市 rule, above); the rest are hollow, each naming its ward.
        has_data = keep["group"].map(platforms.groupby("group")["active"].any()).fillna(False).astype(bool)
        keep["no_data"] = ~has_data
        wards = no_data_ward_polygons(config, nodata)
        keep["no_data_reason"] = [
            "" if not nd else "No business data: " + next(
                (name for name, poly in wards if poly.contains(g)), "this ward") + " publishes no usable food-permit list"
            for nd, g in zip(keep["no_data"], keep.geometry)]
        cols += ["no_data", "no_data_reason"]
        by_ward = collections.Counter(r for r in keep.loc[keep["no_data"], "no_data_reason"])
        print(f"  {int(keep['no_data'].sum())} stations in wards with no business data (hollow, no rings):")
        for reason, n in by_ward.most_common():
            print(f"    {n:>4}  {reason}")
        emit("stations_no_data", int(keep["no_data"].sum()))
    keep = keep[cols].sort_values("station")
    dup = keep["station"].duplicated(keep=False)
    if dup.any():
        sys.exit(f"two stations share an English name: {keep[dup].to_dict('records')}")
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep)} stations -> {config.STATIONS_CSV.name}")

    write_lines(config, near, all_near)
    emit("line_station_rows", len(platforms))
    emit("stations_collapsed", len(groups))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(ex))
    return keep
