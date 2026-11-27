"""Deterministic lint of the directive story copies (D-RCV-60). Compares mp/out/<story>.md with its input.

Checks: table rows with a cell count that differs from their table's header; duplicate or skipped AC IDs in
section 7; duplicate TC IDs in section 16; ACs with no TC row in section 16 (only ACs added by this run);
dates added or removed; person-name patterns; tool or model trailers; 'Not specified' markers with no item ID.

Usage: python -I lint.py [--stories A,B] [--complete-only] [--out mp/lint.jsonl]
Library: lint_story(story) -> list of findings {story, check, line, detail}.
"""
import argparse, json, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent
MP = D / "mp"
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE = re.compile(rf"\b\d{{1,2}} (?:{MONTHS}) \d{{4}}\b|\b20\d\d-\d\d-\d\d\b")
TOOLS = re.compile(r"\b(Claude|Anthropic|Haiku|Sonnet|Opus|ChatGPT|GPT-\d|Gemini|Copilot|Co-Authored-By)\b", re.I)
PERSON = re.compile(r"\b(Mr|Mrs|Ms|Dr|Khun)\.? [A-Z][a-z]+")
NOTSPEC = re.compile(r"Not specified in the source documents(?! \()")
RUN_DATE = "26 November 2026"
STORYKEY = re.compile(r"\bRWB-(?:P\d+|S\d+|PLT|ITG|SVC)-[A-Z]*\d+[A-Z]?-(?:APP|CON|ITG|OPS|INF|DB|NFR|TST)\b")
_KEYS = None


def story_keys():
    global _KEYS
    if _KEYS is None:
        _KEYS = {s for s, _ in json.loads((MP / "stories.json").read_text())}
        cat = D.parents[2] / "04 User stories/Recovery Workbench Service Story Files v1"
        for p in cat.rglob("*.md"):  # stories with no items still exist
            m = re.match(r"RWB (\S+) (\S+) (APP|CON|ITG|OPS|INF|DB|NFR|TST) ", p.name)
            if m:
                _KEYS.add(f"RWB-{m.group(1)}-{m.group(2)}-{m.group(3)}")
    return _KEYS


def cells(row):
    s = row.strip()
    return len(re.split(r"(?<!\\)\|", s[1:-1])) if s.startswith("|") and s.endswith("|") else None


def section(lines, num):
    a = next((i for i, l in enumerate(lines) if re.match(rf"#{{2,4}} {num}\.? ", l)), None)
    if a is None:
        return []
    b = next((i for i in range(a + 1, len(lines)) if re.match(r"#{2,3} \d+\.? ", lines[i])), len(lines))
    return list(range(a, b))


def lint_text(story, before, now):
    out = []
    L = now.split("\n")
    add = lambda check, i, detail: out.append({"story": story, "check": check, "line": i + 1, "detail": detail[:300]})
    # tables: header row followed by a |---| row sets the cell count
    want = None
    for i, l in enumerate(L):
        s = l.strip()
        if not s.startswith("|"):
            want = None
            continue
        if i + 1 < len(L) and re.match(r"^\|\s*:?-{3,}", L[i + 1].strip()):
            want = cells(s)
            continue
        if re.match(r"^\|\s*:?-{3,}", s):
            continue
        c = cells(s)
        if c is None:
            add("table row not closed", i, s[-120:])
        elif want and c != want:
            add("table cell count", i, f"{c} cells, header has {want}: {s[:120]}")
    # AC IDs in section 7
    s7 = section(L, 7)
    acs = [int(m.group(1)) for i in s7 for m in [re.search(r"\bScenario: AC(\d+)\b", L[i])] if m]
    if not acs:
        acs = [int(m.group(1)) for i in s7 for m in [re.match(r"^\|\s*AC(\d+)\s*\|", L[i])] if m]
    seen = set()
    for a in acs:
        if a in seen:
            add("duplicate AC ID", s7[0] if s7 else 0, f"AC{a} appears more than once in section 7")
        seen.add(a)
    if acs:
        miss = sorted(set(range(1, max(acs) + 1)) - set(acs))
        if miss:
            add("skipped AC ID", s7[0], "missing: " + ", ".join(f"AC{x}" for x in miss))
    # TC IDs and coverage in section 16
    s16 = section(L, 16)
    tcs, covers = [], " "
    for i in s16:
        m = re.match(r"^\|\s*(TC[-\w]+)\s*\|([^|]*)\|", L[i])
        if m:
            tcs.append((m.group(1), i))
            covers += m.group(2) + " "
    seen = {}
    for t, i in tcs:
        if t in seen:
            add("duplicate TC ID", i, t)
        seen[t] = i
    before_acs = set(int(x) for x in re.findall(r"\bScenario: AC(\d+)\b", before))
    for a in sorted(set(acs) - before_acs):
        if not re.search(rf"\bAC{a}\b", covers):
            add("new AC without TC row", s16[0] if s16 else 0, f"AC{a} is new and no section 16 row covers it")
    # dates
    db, dn = set(DATE.findall(before)), set(DATE.findall(now))
    for x in sorted(db - dn):
        add("date removed", 0, x)
    for x in sorted(dn - db - {RUN_DATE}):
        add("date added", 0, x)
    # story keys that exist nowhere in the story set (an invented ID)
    known = story_keys()
    for i, l in enumerate(L):
        if l in before:
            continue
        for k in set(STORYKEY.findall(l)):
            if k not in known and k not in before:
                add("unknown story key", i, f"{k} is not a story of the set: {l[:140]}")
    for i, l in enumerate(L):
        if TOOLS.search(l) and not TOOLS.search(before):
            add("tool or model name", i, l[:160])
        elif TOOLS.search(l) and l not in before:
            add("tool or model name", i, l[:160])
        if PERSON.search(l) and l not in before:
            add("person name pattern", i, l[:160])
        if NOTSPEC.search(l) and l not in before:
            add("Not specified without item ID", i, l[:160])
    return out


def lint_story(story):
    meta = json.loads((MP / "chunks" / story / "meta.json").read_text(encoding="utf-8"))
    before = Path(meta["input_file"]).read_text(encoding="utf-8")
    now = (MP / "out" / f"{story}.md").read_text(encoding="utf-8")
    base = lint_text(story, before, before)  # findings already present before the run are not ours
    keys = {(f["check"], f["detail"]) for f in base}
    return [f for f in lint_text(story, before, now) if (f["check"], f["detail"]) not in keys]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stories")
    ap.add_argument("--complete-only", action="store_true")
    ap.add_argument("--out", default=str(MP / "lint.jsonl"))
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    stories = a.stories.split(",") if a.stories else [s for s, _ in json.loads((MP / "stories.json").read_text())]
    if a.complete_only:
        stories = [s for s in stories if len(list((MP / "disp" / s).glob("c*.jsonl"))) >=
                   json.loads((MP / "chunks" / s / "meta.json").read_text())["chunks"]]
    from collections import Counter
    c, n = Counter(), 0
    with open(a.out, "w", encoding="utf-8") as fh:
        for s in stories:
            for f in lint_story(s):
                fh.write(json.dumps(f, ensure_ascii=False) + "\n")
                c[f["check"]] += 1
                n += 1
    print(f"{len(stories)} stories, {n} findings: {dict(c)}")


if __name__ == "__main__":
    main()
