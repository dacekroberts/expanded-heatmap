"""Check two things about every committed map that no browser script measured,
and that Brazil's deploy check found by reading pixels and markup (2026-09-24).

  A  Every line label is readable in DARK mode - the default theme - at WCAG's
     4.5:1 against its dark halo, after the brightness filter the dark theme
     applies. A colour the filter cannot lift (pure blue, navy) must carry its
     own lighter shade in `--dm-label`, which add_line_label sets. Porto
     Alegre's navy Trensurb label read at 1.91:1 before it did.

  B  The legend's inline `style` attribute is intact. The font stack's double
     quotes once closed it at "Segoe UI", so every legend lost its size, shadow
     and fallback fonts, and every map still looked roughly right.

Light-mode label contrast is REPORTED, not failed: labels there sit on a white
halo, and the owner's call covered dark mode only.

    python scripts/check_map_markup.py [--verbose]
"""
import argparse
import re
import sys
from html import unescape as html_unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.linecolour import (  # noqa: E402
    DARK_LABEL_BRIGHTNESS, LABEL_MIN_CONTRAST, brightened, contrast_ratio)
from pipeline.theme import DARK  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# One label's markup, as folium embeds it in the map's script: the colour, the
# optional dark shade, and the label's own text up to its closing </div>
# (written > ... </div in the escaped string). Read as one match so
# a name can never be paired with a neighbouring label's colour.
LABEL_RE = re.compile(r"hm-line-label[^>]{0,40}?style=.{0,400}?color:\s*(#[0-9a-fA-F]{6});"
                      r"(?:\s*--dm-label:\s*(#[0-9a-fA-F]{6});)?"
                      r"[^<]{0,400}?(?:\\u003e|>)((?:[^<\\]|\\u(?!003[ce])[0-9a-fA-F]{4}){1,120})"
                      r"(?:\\u003c|<)/div", re.S)
LEGEND_RE = re.compile(r'<details open class="map-legend" style="([^"]*)"')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--root", default=str(ROOT), help="repository root whose outputs/ to check")
    args = ap.parse_args()
    problems, light_low, maps, labels = [], [], 0, 0
    for html in sorted((Path(args.root) / "outputs").glob("*/heatmap.html")):
        city = html.parent.name
        doc = html.read_text(encoding="utf-8")
        maps += 1
        found = LABEL_RE.findall(doc)
        for colour, dark, name in found:
            labels += 1
            name = html_unescape(re.sub(r"\\u([0-9a-fA-F]{4})",
                                        lambda m: chr(int(m.group(1), 16)), name.strip()))
            shown = brightened(dark or colour, DARK_LABEL_BRIGHTNESS)
            ratio = contrast_ratio(shown, DARK["page"])
            if ratio < LABEL_MIN_CONTRAST:
                problems.append(f"{city}: '{name}' {colour}"
                                f"{' (dark ' + dark + ')' if dark else ''} reads at "
                                f"{ratio:.2f}:1 in dark mode, under {LABEL_MIN_CONTRAST}:1")
            elif args.verbose and dark:
                print(f"  {city}: '{name}' {colour} -> {dark} in dark mode, {ratio:.2f}:1")
            light = contrast_ratio(colour, "#ffffff")
            if light < LABEL_MIN_CONTRAST:
                light_low.append(f"{city}: '{name}' {colour} {light:.2f}:1 on its white halo")
        m = LEGEND_RE.search(doc)
        if not m:
            problems.append(f"{city}: no map legend found")
        else:
            style = m.group(1)
            for must in ("font-size: 13px", "box-shadow"):
                if must not in style:
                    problems.append(f"{city}: the legend's style attribute ends before "
                                    f"'{must}' - a quote inside it closes it early")
        if not found:
            problems.append(f"{city}: no line labels found")

    print(f"check_map_markup: {maps} maps, {labels} line labels")
    if light_low:
        print(f"\nLight mode, reported not failed ({len(light_low)} labels under "
              f"{LABEL_MIN_CONTRAST}:1 on white):")
        for p in light_low if args.verbose else light_low[:8]:
            print("  " + p)
        if not args.verbose and len(light_low) > 8:
            print(f"  ... {len(light_low) - 8} more; --verbose to list")
    if problems:
        print(f"\nPROBLEMS {len(problems)}:")
        for p in problems:
            print("  " + p)
        return 1
    print("\nPROBLEMS 0 - every line label reads at "
          f"{LABEL_MIN_CONTRAST}:1 in dark mode, and every legend's style is intact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
