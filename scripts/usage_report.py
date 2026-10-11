"""Write the datasets behind the Claude Usage Review page, from local session transcripts.

Reads every transcript under ~/.claude/projects/ whose folder starts with the
project prefix (this project, its worktrees and their subagents), counts each
model turn once (a moved or resumed session copies its history into a new
file), and writes one JSON file per dataset into --out:

    headline.json        the page's headline figures, one row per metric
    context_bands.json   turns and usage by context size at each turn
    plan_periods.json    usage a day and the /clear what-if per plan period
    session_peaks.json   sessions grouped by the largest context they reached
    top_sessions.json    the costliest sessions
    exchange_cost.json   what one owner message costs, by context when sent
    tool_output.json     what each tool's results added to main sessions
    concurrency.json     hours by how many main sessions ran in them
    subagent_types.json  subagent runs and usage by agent type
    projects_week.json   every project's share since the last weekly reset

Usage is weighted by API price ratios (input 1, cache write 1.25, cache read
0.1, output 5) as a proxy; the plan's meter does not follow them closely, see
docs/efficiency_review_2026-10-08_context.md, Limits. Any project works:
--prefix names its transcript folder (~/.claude/projects/<prefix>*).

    python scripts/usage_report.py --out <dir> [--prefix <folder prefix>] [--periods "<date>=<plan>,..."] [--baseline YYYY-MM-DD]
"""
import argparse
import collections
import datetime
import glob
import json
import os
import statistics

WEIGHTS = {"inp": 1.0, "cw": 1.25, "cr": 0.1, "out": 5.0}
PROJECTS = os.path.join(os.path.expanduser("~"), ".claude", "projects")
PREFIX = "C--Users-dacek-Documents-Portfolio-expanded-heatmap"
# the owner's plan history (owner, 2026-10-08)
PERIODS = "2026-09-01=Pro,2026-09-20=Max 5x,2026-09-30=Max 20x"
CONTEXT_BANDS = (0, 100_000, 300_000, 600_000)
PEAK_BANDS = (0, 200_000, 500_000, 800_000)
WEEKLY_RESET = (6, 19)  # Sunday, 19:00 UTC


def when(stamp):
    try:
        return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def band_label(value, edges):
    lo = max(e for e in edges if e <= value)
    i = edges.index(lo)
    return f"{lo // 1000}k+" if i == len(edges) - 1 else f"{lo // 1000}-{edges[i + 1] // 1000}k"


def human_text(o):
    """The text of a prompt the owner typed, or None for tool results and harness lines."""
    if o.get("isMeta") or o.get("isCompactSummary"):
        return None
    c = (o.get("message") or {}).get("content")
    if isinstance(c, list):
        if any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c):
            return None
        c = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
    if not isinstance(c, str):
        return None
    if c.startswith(("<command-", "<local-command", "<task-notification", "[Request interrupted", "Caveat:")):
        return None
    if "<system-reminder>" in c[:40]:
        return None
    return c


def result_chars(item):
    c = item.get("content")
    if isinstance(c, str):
        return len(c)
    return sum(len(x.get("text", "")) for x in c or [] if isinstance(x, dict) and x.get("type") == "text")


def scan(folders):
    """One pass over the transcripts; returns per-turn and per-session records."""
    seen_turn, seen_line = set(), set()
    turns, sessions, exchanges = [], [], []
    tool = collections.defaultdict(lambda: [0, 0])
    for folder in folders:
        name = os.path.basename(folder)
        for path in glob.glob(os.path.join(folder, "**", "*.jsonl"), recursive=True):
            is_sub = "subagents" in path.replace("\\", "/")
            agent = None
            if is_sub and os.path.exists(path[:-6] + ".meta.json"):
                try:
                    with open(path[:-6] + ".meta.json", encoding="utf-8") as f:
                        agent = json.load(f).get("agentType")
                except (OSError, ValueError):
                    pass
            s = {"name": name, "sub": is_sub, "agent": agent or "unnamed", "cost": 0.0, "turns": 0,
                 "peak": 0, "prompts": 0, "first_ctx": None, "start": None, "end": None}
            names, ex, last_t = {}, None, None
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    try:
                        o = json.loads(line)
                    except ValueError:
                        continue
                    kind = o.get("type")
                    t = when(o.get("timestamp") or "")
                    if kind == "assistant":
                        m = o.get("message") or {}
                        for x in m.get("content") or []:
                            if isinstance(x, dict) and x.get("type") == "tool_use":
                                names[x.get("id")] = x.get("name") or "?"
                        u = m.get("usage")
                        if not u:
                            continue
                        key = (m.get("id"), o.get("requestId"))
                        if key != (None, None):
                            if key in seen_turn:
                                continue
                            seen_turn.add(key)
                        inp = u.get("input_tokens") or 0
                        cw = u.get("cache_creation_input_tokens") or 0
                        cr = u.get("cache_read_input_tokens") or 0
                        out = u.get("output_tokens") or 0
                        ctx = inp + cw + cr
                        cost = inp * WEIGHTS["inp"] + cw * WEIGHTS["cw"] + cr * WEIGHTS["cr"] + out * WEIGHTS["out"]
                        # a large cache write after an hour idle is the whole context written again
                        idle = bool(t and last_t and cw > 50_000 and (t - last_t).total_seconds() >= 3600)
                        turns.append({"t": t, "ctx": ctx, "cost": cost, "input_side": cost - out * WEIGHTS["out"],
                                      "cr": cr * WEIGHTS["cr"], "cw": cw * WEIGHTS["cw"], "out": out * WEIGHTS["out"],
                                      "sub": is_sub, "session": path, "project": name,
                                      "idle_rewrite": cw * WEIGHTS["cw"] if idle and not is_sub else 0.0})
                        if t:
                            last_t = t
                        s["cost"] += cost
                        s["turns"] += 1
                        s["peak"] = max(s["peak"], ctx)
                        if s["first_ctx"] is None:
                            s["first_ctx"] = ctx
                        if t:
                            s["start"] = s["start"] or t
                            s["end"] = t
                        if ex is not None:
                            ex["cost"] += cost
                            if ex["ctx"] is None:
                                ex["ctx"] = ctx
                    elif kind == "user":
                        uid = o.get("uuid")
                        if uid:
                            if uid in seen_line:
                                continue
                            seen_line.add(uid)
                        if is_sub:
                            continue
                        c = (o.get("message") or {}).get("content")
                        if isinstance(c, list):
                            for x in c:
                                if isinstance(x, dict) and x.get("type") == "tool_result":
                                    nm = names.get(x.get("tool_use_id"), "?")
                                    if nm.startswith("mcp__"):
                                        nm = nm.split("__")[-1]
                                    tool[nm][0] += result_chars(x)
                                    tool[nm][1] += 1
                        text = human_text(o)
                        if text is not None:
                            if ex is not None and ex["ctx"] is not None:
                                exchanges.append(ex)
                            ex = {"ctx": None, "cost": 0.0, "short": len(text.strip()) <= 25}
                            s["prompts"] += 1
            if ex is not None and ex["ctx"] is not None:
                exchanges.append(ex)
            if s["turns"]:
                sessions.append(s)
    return turns, sessions, exchanges, tool


def whatif(turns, cap, total):
    """Share of usage a clear at `cap` would have dropped: context above the cap, read from cache."""
    return sum(max(0, x["ctx"] - cap) * WEIGHTS["cr"] for x in turns if not x["sub"]) / total


def last_reset(now):
    days = (now.weekday() - WEEKLY_RESET[0]) % 7
    r = (now - datetime.timedelta(days=days)).replace(hour=WEEKLY_RESET[1], minute=0, second=0, microsecond=0)
    return r if r <= now else r - datetime.timedelta(days=7)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", default=PREFIX)
    ap.add_argument("--periods", default=PERIODS)
    ap.add_argument("--baseline", default="2026-10-05", help="extra row from this date on (YYYY-MM-DD)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    turns, sessions, exchanges, tool = scan(glob.glob(os.path.join(PROJECTS, args.prefix + "*")))
    if not turns:
        raise SystemExit("no turns found")
    total = sum(x["cost"] for x in turns)
    main_sessions = [s for s in sessions if not s["sub"]]
    subs = [s for s in sessions if s["sub"]]
    input_side = sum(x["input_side"] for x in turns)
    stamps = [x["t"] for x in turns if x["t"]]

    def write(name, rows):
        with open(os.path.join(args.out, name + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows, f, indent=1)

    # every project on the machine since the last weekly reset, for the allowance guide
    now = datetime.datetime.now(datetime.timezone.utc)
    since = last_reset(now)
    week = collections.Counter()
    all_turns, _, _, _ = scan(glob.glob(os.path.join(PROJECTS, "*")))
    # the previous full week, all projects: the evidence that the meter does not follow these weights
    prev_week_all = sum(x["cost"] for x in all_turns if x["t"] and since - datetime.timedelta(days=7) <= x["t"] < since)
    for x in all_turns:
        if x["t"] and x["t"] >= since:
            label = "this project" if x["project"].startswith(args.prefix) else x["project"].split("-Portfolio-")[-1].split("--claude-worktrees")[0]
            week[label] += x["cost"]
    week_total = sum(week.values()) or 1
    write("projects_week", [{"project": p, "share": round(c / week_total, 4)} for p, c in week.most_common()])

    this_week = [x for x in turns if x["t"] and x["t"] >= since]
    week_cost = sum(x["cost"] for x in this_week)
    big = [x for x in turns if x["ctx"] >= 300_000]
    firsts = sorted(s["first_ctx"] for s in main_sessions if s["start"] and s["start"] >= now - datetime.timedelta(days=14))
    short_peak = [s for s in main_sessions if s["peak"] < 500_000]
    mid = [e["cost"] for e in exchanges if 100_000 <= e["ctx"] < 300_000]
    huge = [e["cost"] for e in exchanges if e["ctx"] >= 600_000]
    gp = [s for s in subs if s["agent"] == "general-purpose"]
    write("headline", [
        {"metric": "turns", "label": "Model turns measured", "value": len(turns)},
        {"metric": "sessions", "label": "Sessions", "value": len(main_sessions)},
        {"metric": "subagent_runs", "label": "Subagent runs", "value": len(subs)},
        {"metric": "first_day", "label": "First transcript", "value": min(stamps).strftime("%Y-%m-%d")},
        {"metric": "last_day", "label": "Last transcript", "value": max(stamps).strftime("%Y-%m-%d")},
        {"metric": "reread_share", "label": "Re-reading the conversation", "value": round(sum(x["cr"] for x in turns) / total, 4)},
        {"metric": "write_share", "label": "New context", "value": round(sum(x["cw"] for x in turns) / total, 4)},
        {"metric": "output_share", "label": "Output", "value": round(sum(x["out"] for x in turns) / total, 4)},
        {"metric": "subagent_share", "label": "Subagents", "value": round(sum(s["cost"] for s in subs) / total, 4)},
        {"metric": "over_300k_share", "label": "Input-side usage at 300k+ context", "value": round(sum(x["input_side"] for x in big) / input_side, 4)},
        {"metric": "whatif_120k", "label": "Clearing past 120k would have saved", "value": round(whatif(turns, 120_000, total), 4)},
        {"metric": "whatif_200k", "label": "Clearing past 200k would have saved", "value": round(whatif(turns, 200_000, total), 4)},
        {"metric": "fresh_floor_k", "label": "A fresh session's first turn (median, last 14 days)", "value": round(statistics.median(firsts) / 1000) if firsts else None},
        {"metric": "under_500k_share", "label": "Usage from sessions that stayed under 500k", "value": round(sum(s["cost"] for s in short_peak) / total, 4)},
        {"metric": "exchange_ratio", "label": "A message at 600k+ against one at 100-300k (median cost)", "value": round(statistics.median(huge) / statistics.median(mid), 1) if huge and mid else None},
        {"metric": "gp_share", "label": "General-purpose subagents", "value": round(sum(s["cost"] for s in gp) / total, 4)},
        {"metric": "idle_rewrite_share", "label": "Resuming a session after an hour idle", "value": round(sum(x["idle_rewrite"] for x in turns) / total, 4)},
        {"metric": "short_reply_share", "label": "Re-reads caused by short replies alone", "value": round(sum(e["ctx"] * WEIGHTS["cr"] for e in exchanges if e["short"]) / total, 4)},
        {"metric": "this_week_all_m", "label": "This week so far, all projects (M)", "value": round(sum(week.values()) / 1e6)},
        {"metric": "prev_week_all_m", "label": "The previous full week, all projects (M)", "value": round(prev_week_all / 1e6)},
        {"metric": "prev_week_ratio", "label": "Previous week against this week so far", "value": round(prev_week_all / sum(week.values()), 1) if week else None},
        {"metric": "project_week_share", "label": "This project's share of the machine this week", "value": round(week["this project"] / week_total, 4)},
        {"metric": "week_whatif_120k", "label": "This week: clearing past 120k would have saved", "value": round(whatif(this_week, 120_000, week_cost), 4) if week_cost else None},
        # assumes the plan meter weighs tokens like the API price ratios (unverified)
        {"metric": "allowance_guide", "label": "Weekly allowance a clear at 120k would have freed (assumption)", "value": round(whatif(this_week, 120_000, week_cost) * week["this project"] / week_total, 4) if week_cost else None},
    ])

    bands = collections.defaultdict(lambda: [0, 0.0])
    for x in turns:
        b = band_label(x["ctx"], CONTEXT_BANDS)
        bands[b][0] += 1
        bands[b][1] += x["input_side"]
    write("context_bands", [{"band": b, "order": i, "turns": bands[b][0], "share": round(bands[b][1] / input_side, 4)}
                            for i, b in enumerate(band_label(e, CONTEXT_BANDS) for e in CONTEXT_BANDS)])

    def period_row(plan, sel):
        cost = sum(x["cost"] for x in sel)
        days = len({x["t"].strftime("%Y-%m-%d") for x in sel})
        return {"plan": plan, "from": min(x["t"] for x in sel).strftime("%Y-%m-%d"),
                "to": max(x["t"] for x in sel).strftime("%Y-%m-%d"), "days": days,
                "per_day_m": round(cost / days / 1e6), "whatif_120k": round(whatif(sel, 120_000, cost), 4),
                "subagent_share": round(sum(x["cost"] for x in sel if x["sub"]) / cost, 4)}

    periods = [(p.split("=")[0], p.split("=")[1]) for p in args.periods.split(",")]
    rows = []
    for i, (start, plan) in enumerate(periods):
        end = periods[i + 1][0] if i + 1 < len(periods) else "9999"
        sel = [x for x in turns if x["t"] and start <= x["t"].strftime("%Y-%m-%d") < end]
        if sel:
            rows.append(period_row(plan, sel))
    # the baseline the habits of 2026-10-09 are measured against: the stretch after the
    # 2026-10-04 efficiency review, inside the last plan period
    sel = [x for x in turns if x["t"] and args.baseline <= x["t"].strftime("%Y-%m-%d")]
    if sel:
        rows.append(period_row(f"{periods[-1][1]}, from {args.baseline}", sel))
    write("plan_periods", rows)

    peaks = collections.defaultdict(list)
    for s in main_sessions:
        peaks[band_label(s["peak"], PEAK_BANDS)].append(s)
    write("session_peaks", [{"peak": b, "order": i, "sessions": len(peaks[b]),
                             "share": round(sum(s["cost"] for s in peaks[b]) / total, 4),
                             "median_turns": statistics.median([s["turns"] for s in peaks[b]]) if peaks[b] else 0}
                            for i, b in enumerate(band_label(e, PEAK_BANDS) for e in PEAK_BANDS)])

    top = sorted(main_sessions, key=lambda s: -s["cost"])[:8]
    write("top_sessions", [{"rank": i + 1, "session": s["name"][len(args.prefix):].replace("--claude-worktrees-", "") or "main checkout",
                            "share": round(s["cost"] / total, 4), "turns": s["turns"], "prompts": s["prompts"],
                            "peak_k": round(s["peak"] / 1000), "days": round((s["end"] - s["start"]).total_seconds() / 86400, 1) if s["start"] else None}
                           for i, s in enumerate(top)])

    ex_bands = collections.defaultdict(list)
    for e in exchanges:
        ex_bands[band_label(e["ctx"], CONTEXT_BANDS)].append(e["cost"])
    write("exchange_cost", [{"band": b, "order": i, "exchanges": len(ex_bands[b]),
                             "median_m": round(statistics.median(ex_bands[b]) / 1e6, 2) if ex_bands[b] else None,
                             "share": round(sum(ex_bands[b]) / total, 4)}
                            for i, b in enumerate(band_label(e, CONTEXT_BANDS) for e in CONTEXT_BANDS)])

    chars = sum(v[0] for v in tool.values()) or 1
    write("tool_output", [{"tool": k, "chars_m": round(v[0] / 1e6, 1), "share": round(v[0] / chars, 4), "calls": v[1],
                           "avg_k": round(v[0] / v[1] / 1000, 1)}
                          for k, v in sorted(tool.items(), key=lambda kv: -kv[1][0])[:8]])

    hours = collections.defaultdict(set)
    for x in turns:
        if x["t"] and not x["sub"]:
            hours[x["t"].strftime("%Y-%m-%d %H")].add(x["session"])
    at_once = collections.Counter(min(len(v), 6) for v in hours.values())
    write("concurrency", [{"at_once": f"{k}+" if k == 6 else str(k), "order": k, "hours": at_once[k]} for k in range(1, 7)])

    agents = collections.defaultdict(list)
    for s in subs:
        agents[s["agent"]].append(s["cost"])
    write("subagent_types", [{"agent": a, "runs": len(c), "share": round(sum(c) / total, 4),
                              "mean_m": round(statistics.mean(c) / 1e6, 2)}
                             for a, c in sorted(agents.items(), key=lambda kv: -sum(kv[1]))[:7]])
    print(f"wrote 10 datasets to {args.out} ({len(turns):,} turns)")


if __name__ == "__main__":
    main()
