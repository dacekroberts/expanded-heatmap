"""PreToolUse/Bash guard: refuse a heredoc or `-c` string that carries escapes.

WHY THIS IS A HOOK AND NOT A PARAGRAPH
--------------------------------------
`CLAUDE.md` has carried the rule since 2026-09-22 - "write multi-line text with
the Write tool, never a shell heredoc" - with three dated incidents under it.
It was read at session start and broken again the same day: a probe written as
`re.findall(r'Use[s]?:\\s*([^<\\\\]{0,60})', t)` inside a `python - <<'PYEOF'`
arrived as `[^<\\]`, an unterminated character set. That is four occurrences
against a rule that exists, so the rule is not the missing piece - enforcement
is. This project's own meta-rule says so: put the lesson where the next caller
must pass through it, as a raising check, not as prose.

TWO THINGS THE PROSE RULE GOT WRONG, BOTH FIXED HERE
----------------------------------------------------
1. It reads as being about MULTI-LINE TEXT - "commit messages, DECISIONS.md
   entries, page prose". A one-line regex probe does not feel like that, so the
   rule did not seem to apply. The real trigger is BACKSLASHES AND BACKTICKS,
   at any length.
2. **Quoting the delimiter does not save you.** `<<'PYEOF'` should stop shell
   expansion, and the mangling happened anyway, because the rewriting is not
   bash's. Nothing in the written rule said this.

WHAT IT BLOCKS, AND WHAT IT DELIBERATELY DOES NOT
-------------------------------------------------
Only the intersection: a heredoc or an inline interpreter string (`python -c`,
`perl -e`, `node -e`) AND a backslash or backtick somewhere in the command.

A plain `grep "\\.py$"` is untouched - it is not a heredoc. A heredoc of plain
prose with no escapes is untouched. Blocking every backslash would fire on
every Windows path in this repository, and blocking every heredoc would fire
on cases that have never once gone wrong. A guard that cries wolf gets
disabled, and then it guards nothing.

FAIL-OPEN BY DESIGN. Any error here allows the command. This is a style guard,
not a security control, and a broken guard must not wedge every Bash call.
"""

import json
import re
import sys

# `<<WORD`, `<<'WORD'`, `<<"WORD"`, `<<-WORD`. Not `<<<` (a herestring has no
# body to mangle across lines) and not `<<` inside an obvious shift operator.
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")

# python -c "...", perl -e '...', node -e "...". The interpreter and the flag
# may be separated by other flags (`python -u -c`).
INLINE = re.compile(
    r"\b(?:python3?|perl|node|ruby|php|osascript)\b[^|;&\n]*?\s-(?:c|e)\b"
)

BACKSLASH_OR_BACKTICK = re.compile(r"[\\`]")

REASON = """Blocked: this command combines a {form} with a backslash or backtick.

That exact combination has silently corrupted content four times in this
repository - an f-string in generated code, every backticked phrase in a
commit message, a `\\n` that became a real newline mid-string, and a regex
character class `[^<\\\\]` that arrived as `[^<\\]` and would not compile.
Quoting the heredoc delimiter does NOT prevent it.

Write the content to a file with the Write tool and run that file instead:

    Write  ->  <scratchpad>/probe.py
    Bash   ->  python <scratchpad>/probe.py

Use the session scratchpad directory, per CLAUDE.md. If the command genuinely
needs no escapes, remove the backslash or backtick and it will pass.

(Guard: .claude/hooks/block_heredoc.py)"""


def main():
    raw = sys.stdin.read()
    payload = json.loads(raw)
    command = (payload.get("tool_input") or {}).get("command") or ""

    if not BACKSLASH_OR_BACKTICK.search(command):
        return
    if HEREDOC.search(command):
        form = "heredoc"
    elif INLINE.search(command):
        form = "-c/-e inline interpreter string"
    else:
        return

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": REASON.format(form=form),
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:            # noqa: BLE001 - fail open, never wedge Bash
        pass
