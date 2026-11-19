#!/usr/bin/env python3
"""Turn the story blocks in ``source/*.txt`` into one JSON spec per story.

The source blocks are the section 9 content of the plan: prose written for a
reader, not JSON.  This script parses them, applies the field limits (shortening
prose where a trailing clause can go), and writes ``specs/<KEY>.json``.

It never renames a table, view, class, endpoint, event, job or message ID: those
fields are reported, not edited.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source"
SPECS = HERE / "specs"

FIELDS = ("file_stem", "title", "module", "overview_label", "goal", "why",
          "needs", "triggers", "ace", "writes", "reads", "stores", "functions",
          "path", "rules", "risks", "example")

LIMITS = {
    "title": 66, "status_text": 56, "goal": 110, "why": 180,
    "overview_label": 30, "stores": 210,
}

problems: list[str] = []
shortened: list[str] = []


# ------------------------------------------------------------------ parse ---
def split_top(s: str, sep: str = ";") -> list[str]:
    """Split on sep outside double quotes."""
    out, buf, quoted = [], "", False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == '"':
            quoted = not quoted
            buf += ch
            i += 1
        elif not quoted and s.startswith(sep, i):
            out.append(buf)
            buf = ""
            i += len(sep)
        else:
            buf += ch
            i += 1
    out.append(buf)
    return [part.strip() for part in out if part.strip()]


def items_kv(value: str) -> list[dict]:
    out = []
    for part in split_top(value):
        m = re.match(r'^(.*?)\s*"([^"]*)"\s*$', part, re.S)
        if m:
            out.append({"t": m.group(1).strip(), "note": m.group(2).strip()})
        elif part.startswith("(") and part.endswith(")"):
            continue
        else:
            out.append({"t": part.strip(), "note": ""})
    return out


def items_ace(value: str) -> tuple[list[dict], str]:
    if value.strip().startswith("[]"):
        m = re.search(r'ace_note:\s*"([^"]*)"', value)
        return [], (m.group(1).strip() if m else "")
    out = []
    for part in split_top(value):
        m = re.match(r'^(.*?)\s+([AB])\s+"([^"]*)"\s*$', part, re.S)
        if not m:
            problems.append(f"unparsed ace item: {part!r}")
            continue
        out.append({"view": m.group(1).strip(), "section": m.group(2),
                    "note": m.group(3).strip()})
    return out, ""


def items_quoted(value: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r'"([^"]*)"', value)]


def items_trigger(value: str) -> list[list[str]]:
    out = []
    for part in split_top(value):
        m = re.match(r'^([A-Z]+)\s+"([^"]*)"\s*$', part)
        if not m:
            problems.append(f"unparsed trigger: {part!r}")
            continue
        out.append([m.group(1), m.group(2)])
    return out


def items_path(value: str) -> list[dict]:
    out = []
    for part in split_top(value, " > "):
        m = re.match(r'^([a-z]+)\s+"([^"]*)"\s*$', part)
        if not m:
            problems.append(f"unparsed path chip: {part!r}")
            continue
        out.append({"kind": m.group(1), "text": m.group(2)})
    return out


def keys_of(value: str) -> list[str]:
    return re.findall(r'(?:E1|E2|TE)-\d{3}|ACE-\d{3}', value)


def parse_block(key: str, lines: list[str]) -> dict:
    spec: dict = {"key": key}
    for line in lines:
        if not line.startswith("- "):
            if line.strip():
                problems.append(f"{key}: stray line {line!r}")
            continue
        body = line[2:]
        name, _, value = body.partition(":")
        name, value = name.strip(), value.strip()

        if name == "file_stem":
            spec["file_stem"] = value
        elif name == "title":
            spec["title"] = value
        elif name == "module":
            parts = [p.strip() for p in value.split(" | ")]
            spec["module"] = parts[0]
            for part in parts[1:]:
                if part.startswith("flag:"):
                    spec["flag"] = part[5:].strip()
                elif part.startswith("status:"):
                    m = re.match(r'^(READY|PARTIAL|RETIRED)\s+"(.*)"$',
                                 part[7:].strip())
                    if not m:
                        problems.append(f"{key}: bad status {part!r}")
                    else:
                        spec["status"] = m.group(1)
                        spec["status_text"] = m.group(2)
                elif part.startswith("theme:"):
                    spec["theme"] = part[6:].strip()
                else:
                    problems.append(f"{key}: bad module part {part!r}")
        elif name == "overview_label":
            spec["overview_label"] = value
        elif name in ("goal", "why"):
            spec[name] = value
        elif name == "needs":
            left, _, right = value.partition("|")
            spec["needs"] = keys_of(left)
            spec["unblocks"] = keys_of(right)
        elif name == "triggers":
            spec["triggers"] = items_trigger(value)
        elif name == "ace":
            spec["ace"], spec["ace_note"] = items_ace(value)
        elif name in ("writes", "reads"):
            spec[name] = items_kv(value)
        elif name == "stores":
            spec["stores"] = items_quoted(value)[0] if value.startswith('"') \
                else value
        elif name == "functions":
            spec["functions"] = [{"name": i["t"], "does": i["note"]}
                                 for i in items_kv(value)]
        elif name == "path":
            spec["path"] = items_path(value)
        elif name in ("rules", "risks", "example"):
            spec[name] = items_quoted(value)
        else:
            problems.append(f"{key}: unknown field {name!r}")
    return spec


# -------------------------------------------------------------- shortening --
def fit(text: str, limit: int) -> str:
    """Shorten prose by dropping a trailing clause, then trailing words."""
    if len(text) <= limit:
        return text
    best = ""
    for m in re.finditer(r"[;,]\s", text):
        candidate = text[:m.start()].strip()
        if len(candidate) <= limit and len(candidate) >= limit * 0.5:
            best = candidate
    if best:
        return best
    words: list[str] = []
    for word in text.split():
        candidate = " ".join(words + [word])
        if len(candidate) > limit:
            break
        words.append(word)
    return " ".join(words).rstrip(" ,;:-")


def apply_limits(spec: dict) -> None:
    for field, limit in LIMITS.items():
        if field not in spec:
            continue
        original = spec[field]
        spec[field] = fit(original, limit)
        if spec[field] != original:
            shortened.append(f"{spec['key']}.{field}\n    - {original}\n"
                             f"    + {spec[field]}")


# ------------------------------------------------------------------- main ---
def main() -> int:
    SPECS.mkdir(parents=True, exist_ok=True)
    blocks: dict[str, list[str]] = {}
    order: list[str] = []
    for path in sorted(SOURCE.glob("*.txt")):
        current = None
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.startswith("### "):
                current = raw[4:].strip()
                if current in blocks:
                    problems.append(f"duplicate block {current}")
                blocks[current] = []
                order.append(current)
            elif current:
                blocks[current].append(raw)

    specs = []
    for key in order:
        spec = parse_block(key, blocks[key])
        for field in ("file_stem", "title", "module", "overview_label", "goal",
                      "why", "status", "status_text", "theme", "needs",
                      "unblocks", "triggers", "ace", "writes", "reads",
                      "stores", "functions", "path", "rules", "risks",
                      "example"):
            if field not in spec:
                problems.append(f"{key}: missing {field}")
        if "ace" in spec and "ace_note" not in spec:
            spec["ace_note"] = ""
        apply_limits(spec)
        specs.append(spec)

    for spec in specs:
        (SPECS / f"{spec['key']}.json").write_text(
            json.dumps(spec, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8")

    print(f"{len(specs)} specs written")
    if shortened:
        print(f"\n{len(shortened)} field(s) shortened to fit a limit:")
        for item in shortened:
            print("  " + item)
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for item in problems:
            print("  " + item)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
