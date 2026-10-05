"""Rebuild the census page's Hottest leads section from the master list.

Every open candidate in Bands A-D (rows not marked built) becomes a lead, readiest band first;
the add-ons section's "Potential ... expansions" bullets become the extensions note.
leads_notes.json holds optional one-line summaries keyed by city; a city without one shows
the master list's own cell, cut at its first clause. Run before every census republish.

Usage:
    python scripts/staging_artifacts/leads_build.py <path to the census page HTML>

The page is the published census artifact saved locally (the Artifact tool's read
action names the file); this rewrites only what sits between its leads markers.
"""
import html, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ML = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "city_master_list.md")
if len(sys.argv) != 2:
    sys.exit("Usage: leads_build.py <census page HTML>")
PAGE = sys.argv[1]
NOTES = os.path.join(HERE, "leads_notes.json")
t = open(ML, encoding="utf-8").read()
notes = json.load(open(NOTES, encoding="utf-8")) if os.path.exists(NOTES) else {}
FLAG = re.compile("[\U0001F1E6-\U0001F1FF]{2}")

def section(start_pat):
    m = re.search(start_pat, t, re.M)
    if not m:
        return ""
    nxt = re.search(r"^## ", t[m.end():], re.M)
    return t[m.end(): m.end() + nxt.start()] if nxt else t[m.end():]

# flag -> country name, from the by-country table
names = {}
for line in section(r"^## ✅ Current by country.*$").splitlines():
    m = re.match(r"\|\s*(" + FLAG.pattern + r")\s+([^|]+?)\s*\|", line)
    if m:
        names[m.group(1)] = m.group(2).strip()

def plain(md):
    s = re.sub(r"\*\*|`|\*", "", md)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.strip()

def first_clause(md):
    s = plain(md)
    s = re.split(r"(?<=[a-z0-9)])[.;:](\s|$)", s, maxsplit=1)[0]
    return s if len(s) <= 140 else s[:137].rsplit(" ", 1)[0] + "…"

leads = []
for band in "ABCD":
    body = section(r"^## \S+ Band " + band + r" — .*$")
    for line in body.splitlines():
        if not line.startswith("| **") and not line.startswith("| ✅"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "✅" in cells[0] or "built" in cells[0].lower():
            continue
        city = re.search(r"\*\*(.+?)\*\*", cells[0]).group(1)
        flag = FLAG.search(cells[0])
        country = (flag.group(0) + " " + names.get(flag.group(0), "")).strip() if flag else ""
        left = notes.get(city) or first_clause(cells[-1])
        leads.append((city, country, band, left))

# extensions: bullets under "**Potential ...**" in the add-ons section
ext = []
addons = section(r"^## Add-ons to built cities.*$")
m = re.search(r"^- \*\*Potential[^\n]*\n((?:  - [^\n]*\n)+)", addons, re.M)
if m:
    for b in re.findall(r"^  - (.+)$", m.group(1), re.M):
        if b.startswith("**How"):
            continue
        ext.append(re.match(r"\*\*(.+?)\*\*", b).group(1) if b.startswith("**") else plain(b))
# single-bullet extensions: "- **Potential: <name> + <places>**"
for b in re.findall(r"^- \*\*Potential: (.+?)\*\*", addons, re.M):
    ext.append(b)

countries = sorted({c for _, c, _, _ in leads if c})
rows = "\n".join(
    f'      <tr><td class="c">{html.escape(c)}</td><td>{html.escape(k)}</td><td>{b}</td><td>{html.escape(w)}</td></tr>'
    for c, k, b, w in leads
)
ext_html = ""
if ext:
    ext_html = ('\n  <p class="note col"><strong>Regional extensions</strong> (marked on the master list): '
                + html.escape("; ".join(plain(e) for e in ext)) + ".</p>")
count = f"{len(leads)} cities · {len(countries)} countries" + (f" · {len(ext)} extensions" if ext else "")
block = f"""<!-- leads:start -->
<section>
  <h2><span class="dot d-cand"></span> Hottest leads <span class="count">{count}</span></h2>
  <p class="note col">Every open candidate on the master list, readiest band first: A ready to build, B a narrower page, C one measurement or call away, D waiting on your act. Rebuilt from the master list at each republish, so a city enters the moment it is banded and leaves when it is built or discarded.</p>
  <div class="tablebox"><table>
    <thead><tr><th>City</th><th>Country</th><th>Band</th><th>What's left</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table></div>{ext_html}
</section>
<!-- leads:end -->"""

p = open(PAGE, encoding="utf-8").read()
if "<!-- leads:start -->" in p:
    p = re.sub(r"<!-- leads:start -->.*?<!-- leads:end -->", lambda _: block, p, flags=re.S)
else:
    i = p.index('<section>\n  <h2><span class="dot d-cand"></span> Hottest leads')
    j = p.index("</section>", i) + len("</section>")
    p = p[:i] + block + p[j:]
open(PAGE, "w", encoding="utf-8", newline="\n").write(p)
for l in leads:
    print(*l, sep=" | ")
print("extensions:", ext)
