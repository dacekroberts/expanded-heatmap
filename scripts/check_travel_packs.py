"""The Travel table (pipeline/travel_packs.py) against the built maps.

    python scripts/check_travel_packs.py

Fails when a city in LOCAL_LANG or ROUTES has no outputs/<city>/heatmap.html
(a typo would silently leave that city without its language pill), when a
language is not one @protomaps/basemaps 5.7.2 carries, when a route kind is
unknown, or when a committed map carries the Travel switch while PACK_HOST is
None (or lacks it while a host is set): the table and the maps must agree.
A built city must be in exactly one of LOCAL_LANG and ENGLISH_ONLY: a city
that lands later fails here until it is placed, which is also the reminder
that it needs a pack.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline import travel_packs as tp  # noqa: E402

# The `lang` values of @protomaps/basemaps 5.7.2 (read from its dist file,
# 2026-10-11). Re-read if the pinned version in map_common.py changes.
STYLE_LANGS = {"ar", "bg", "cs", "da", "de", "el", "en", "es", "et", "fa", "fi", "fr", "ga", "he",
               "hi", "hr", "hu", "id", "it", "ja", "ko", "lt", "lv", "mr", "mt", "ne", "nl", "no",
               "pl", "pt", "ro", "ru", "sk", "sl", "sv", "tr", "uk", "ur", "vi", "zh-Hans",
               "zh-Hant"}
MARK = b"expanded-heatmap-basemap"   # TRAVEL_MODE_SCRIPT's storage key

built = sorted(p.name for p in (ROOT / "outputs").iterdir() if (p / "heatmap.html").exists())
problems = []
for code, cities in tp.LOCAL_LANG.items():
    if code not in STYLE_LANGS:
        problems.append(f"LOCAL_LANG: {code!r} is not a language of the pinned style")
    problems += [f"LOCAL_LANG[{code!r}]: no built map for {c!r}" for c in cities if c not in built]
for city, routes in tp.ROUTES.items():
    if city not in built:
        problems.append(f"ROUTES: no built map for {city!r}")
    problems += [f"ROUTES[{city!r}]: unknown kind {k!r}" for k, _name in routes
                 if k not in ("ferry", "aerialway")]
on = bool(tp.PACK_HOST)
if on and (not tp.PACK_HOST.startswith("https://") or tp.PACK_HOST.endswith("/")):
    problems.append(f"PACK_HOST {tp.PACK_HOST!r}: https, no trailing slash")
wrong = [c for c in built if (MARK in (ROOT / "outputs" / c / "heatmap.html").read_bytes()) != on]
if wrong:
    problems.append(f"{len(wrong)} committed map(s) {'lack' if on else 'carry'} the Travel switch while "
                    f"PACK_HOST is {'set' if on else 'None'}: {', '.join(wrong[:8])}"
                    + (" ..." if len(wrong) > 8 else ""))

listed = [c for cities in tp.LOCAL_LANG.values() for c in cities]
english = list(tp.ENGLISH_ONLY)
problems += [f"ENGLISH_ONLY: no built map for {c!r}" for c in english if c not in built]
both = sorted(c for c in set(listed + english) if (listed + english).count(c) > 1)
if both:
    problems.append(f"listed more than once: {', '.join(both)}")
unplaced = [c for c in built if c not in listed and c not in english]
if unplaced:
    problems.append(f"{len(unplaced)} built map(s) in neither LOCAL_LANG nor ENGLISH_ONLY "
                    f"(place each and build its pack, docs/travel_packs.md): {', '.join(unplaced)}")
if problems:
    print("\n".join("FAIL " + p for p in problems))
    sys.exit(1)
print(f"OK - Travel table matches {len(built)} built maps: switch {'ON at ' + tp.PACK_HOST if on else 'off'}, "
      f"{len(listed)} cities with a local label language, {len(english)} English-only, "
      f"{sum(len(r) for r in tp.ROUTES.values())} legend route(s).")
