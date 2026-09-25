"""Check what no browser script measured about every committed map, and what
two deploy checks found by reading pixels and markup (2026-09-24).

  A  Every line label reads at WCAG's 4.5:1 in BOTH themes, against the halo
     the browser actually draws:
       - light: the label's inline colour on its inline text-shadow halo -
         white, or the dark page colour for a colour that reads better there
         (the owner's halo swap; 145 of 235 labels failed on white, Milan's M3
         at 1.08:1);
       - dark (the default): its `--dm-label` colour on the dark page colour.
         Every label must carry one, and the dark rule must put NO filter on
         the label - a brightness() filter once lifted the halo with the text,
         so the figures measured a halo nobody saw.
  B  The legend's inline `style` attribute is intact. The font stack's double
     quotes once closed it at "Segoe UI", and every legend lost its size, its
     shadow and its fallback fonts while still looking roughly right.
  C  No two DIFFERENT lines share a dark-mode label colour. Within one map, two
     labels whose light-theme colours differ (CIE76 >= HARD_FLOOR) must not come
     out within HARD_FLOOR of each other in dark mode. The x1.8 dark rule did
     that 21 times in 10 cities - Paris 1, 9 and 10 all #ffff00 - and no check
     looked (Rotterdam's deploy check, 2026-09-24). Lines an agency coloured
     alike stay alike and are not counted.

    python scripts/check_map_markup.py [--verbose] [--root DIR]
"""
import argparse
import re
import sys
from html import unescape as html_unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.linecolour import HARD_FLOOR, LABEL_MIN_CONTRAST, contrast_ratio, delta_e  # noqa: E402
from pipeline.theme import DARK  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# One label's markup, as folium embeds it in the map's script: its colour, its
# dark shade, its halo, and its own text up to the closing </div> (folium
# escapes the angle brackets as unicode escapes in the string). One match per
# label, so a name can never be paired with a neighbouring label's colour.
LABEL_RE = re.compile(
    r"hm-line-label[^>]{0,40}?style=.{0,400}?color:\s*(#[0-9a-fA-F]{6});"
    r"(?:\s*--dm-label:\s*(#[0-9a-fA-F]{6});)?"
    r".{0,80}?text-shadow:\s*-1px -1px 0 (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})\b"
    r"[^<]{0,400}?(?:\\u003e|>)((?:[^<\\]|\\u(?!003[ce])[0-9a-fA-F]{4}){1,120})"
    r"(?:\\u003c|<)/div", re.S)
DARK_RULE_RE = re.compile(r"\.dark-base \.leaflet-marker-icon div\[style\*=\"text-shadow\"\] \{([^}]*)\}")
LEGEND_RE = re.compile(r'<details open class="map-legend" style="([^"]*)"')


def six(hex_colour):
    h = hex_colour.lstrip("#")
    return "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h)


def name_of(raw):
    return html_unescape(re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)),
                                raw.strip()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--root", default=str(ROOT), help="repository root whose outputs/ to check")
    args = ap.parse_args()
    problems, maps, labels, swapped = [], 0, 0, 0
    for html in sorted((Path(args.root) / "outputs").glob("*/heatmap.html")):
        city = html.parent.name
        doc = html.read_text(encoding="utf-8")
        maps += 1
        found = LABEL_RE.findall(doc)
        if not found:
            problems.append(f"{city}: no line labels found")
        # C: one entry per line name (a name can recur on one map).
        by_name = {}
        for colour, dark, _halo, raw in found:
            by_name.setdefault(name_of(raw), (colour.lower(), (dark or "").lower()))
        named = [(n, c, d) for n, (c, d) in by_name.items() if d]
        for i, (a, ca, da) in enumerate(named):
            for b, cb, db in named[i + 1:]:
                if delta_e(ca, cb) >= HARD_FLOOR and delta_e(da, db) < HARD_FLOOR:
                    problems.append(f"{city}: '{a}' {ca} and '{b}' {cb} are different lines "
                                    f"sharing a dark-mode label colour ({da} / {db}, "
                                    f"CIE76 {delta_e(da, db):.1f})")
        for colour, dark, halo, raw in found:
            labels += 1
            name, halo = name_of(raw), six(halo)
            light_ratio = contrast_ratio(colour, halo)
            if light_ratio < LABEL_MIN_CONTRAST:
                problems.append(f"{city}: '{name}' {colour} on its {halo} halo reads at "
                                f"{light_ratio:.2f}:1 in light mode, under {LABEL_MIN_CONTRAST}:1")
            if halo != "#ffffff":
                swapped += 1
                if args.verbose:
                    print(f"  {city}: '{name}' {colour} on a {halo} halo in light mode, {light_ratio:.2f}:1")
            if not dark:
                problems.append(f"{city}: '{name}' carries no --dm-label, so its dark-mode colour is unset")
                continue
            dark_ratio = contrast_ratio(dark, DARK["page"])
            if dark_ratio < LABEL_MIN_CONTRAST:
                problems.append(f"{city}: '{name}' {dark} reads at {dark_ratio:.2f}:1 in dark mode, "
                                f"under {LABEL_MIN_CONTRAST}:1")
        rule = DARK_RULE_RE.search(doc)
        if rule and "filter" in rule.group(1):
            problems.append(f"{city}: the dark label rule carries a filter, which brightens the halo "
                            f"with the text - every dark-mode figure here would measure the wrong halo")
        m = LEGEND_RE.search(doc)
        if not m:
            problems.append(f"{city}: no map legend found")
        else:
            for must in ("font-size: 13px", "box-shadow"):
                if must not in m.group(1):
                    problems.append(f"{city}: the legend's style attribute ends before "
                                    f"'{must}' - a quote inside it closes it early")

    print(f"check_map_markup: {maps} maps, {labels} line labels; {swapped} on a dark halo in light mode")
    if problems:
        print(f"\nPROBLEMS {len(problems)}:")
        for p in problems if args.verbose else problems[:25]:
            print("  " + p)
        if not args.verbose and len(problems) > 25:
            print(f"  ... {len(problems) - 25} more; --verbose to list")
        return 1
    print(f"\nPROBLEMS 0 - every line label reads at {LABEL_MIN_CONTRAST}:1 in both themes, "
          f"no two different lines share a dark-mode label colour, "
          f"and every legend's style is intact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
