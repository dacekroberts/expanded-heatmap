"""Per-country census from the master list: built, candidates, R, discards (by flag). Read-only."""
import collections, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "city_master_list.md")
t = open(p, encoding="utf-8").read()
FLAG = re.compile("[\U0001F1E6-\U0001F1FF]{2}")
def iso(f):
    return "".join(chr(ord(c) - 0x1F1E6 + 65) for c in f)

def section(start, end):
    i = t.index(start); j = t.index(end, i)
    return t[i:j]

out = collections.defaultdict(lambda: collections.Counter())
# by-country table
bc = section("## ✅ Current by country", "## Countries ruled out")
for line in bc.splitlines():
    m = FLAG.search(line)
    if not line.startswith("| ") or not m:
        continue
    cells = [c.strip() for c in line.strip("|").split("|")]
    def num(c):
        m2 = re.search(r"\*\*(\d+)\*\*", c)
        return int(m2.group(1)) if m2 else 0
    code = iso(m.group(0))
    out[code]["built"] = num(cells[1]); out[code]["cand"] = num(cells[2]); out[code]["R"] = num(cells[3])
    out[code]["name"] = 0
    out[code + "_name"] = cells[0]
# discards by flag
disc = section("## DISCARDED", "## Commuter-rail revisit group")
for line in disc.splitlines():
    if line.startswith("| **"):
        m = FLAG.search(line.split("|")[1])
        if m:
            out[iso(m.group(0))]["disc"] += 1
# ruled out
ro = section("## Countries ruled out", "## Five rules")
print("RULED OUT:", sorted(set(iso(f) for f in FLAG.findall(ro))))
rows = []
for k, v in out.items():
    if k.endswith("_name"):
        continue
    rows.append((k, v["built"], v["cand"], v["R"], v["disc"]))
for r in sorted(rows):
    print(*r, sep="\t")
