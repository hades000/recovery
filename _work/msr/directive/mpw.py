"""Worker helper for the directive model pass (D-RCV-60). Keeps the model's context small.

  python -I mpw.py show  <story>            next undone chunk: items + current text of the sections they touch
  python -I mpw.py apply <story> <cNN>      apply mp/tmp/<story>-<cNN>.json to the story copy, write the disposition
  python -I mpw.py next  <story> [<story>..] first story in the list with an undone chunk (or ALL DONE)

The JSON written by the worker:
  {"edits": [{"old": "exact current text", "new": "replacement"}, ...],
   "disposition": [{"ruling": "R-..", "item": "..", "status": "Resolved|Cross-document|Not applied",
                    "section": "7", "target": "", "change": "", "note": ".."}]}
Every 'old' must occur exactly once in the story copy (after the earlier edits of the same file). All edits
apply or none do. Writes only mp/out/<story>.md and mp/disp/<story>/<cNN>.jsonl.
"""
import json, re, sys
from pathlib import Path

MP = Path(__file__).resolve().parent / "mp"
MAXL = 140


def chunks(story):
    return sorted((MP / "chunks" / story).glob("c*.md"))


def undone(story):
    return [c for c in chunks(story) if not (MP / "disp" / story / (c.stem + ".jsonl")).exists()]


def sec_ranges(lines):
    heads = [(i, l) for i, l in enumerate(lines) if re.match(r"#{2,4} ", l)]
    out = {}
    for k, (i, l) in enumerate(heads):
        m = re.match(r"#{2,4} (\d+(?:\.\d+)?)\.? ", l)
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        if m:
            out[m.group(1)] = (i, end)
    return out


def show(story):
    u = undone(story)
    if not u:
        print(f"{story}: ALL CHUNKS DONE")
        return
    c = u[0]
    text = c.read_text(encoding="utf-8")
    print(text)
    lines = (MP / "out" / f"{story}.md").read_text(encoding="utf-8").split("\n")
    rng = sec_ranges(lines)
    want = set()
    for s in re.findall(r"sections: ([^)]*)\)", text):
        for x in s.split(", "):
            x = x.strip()
            if x and x != "find it":
                want.add(x)
                if x not in rng and x.split(".")[0] in rng:
                    want.add(x.split(".")[0])
    shown = []
    # header table always (status, dependencies, PRD)
    print("=" * 30, "CURRENT STORY TEXT (only these parts; copy 'old' text from here exactly)", "=" * 30)
    first = min((a for a, _ in rng.values()), default=len(lines))
    print(f"--- header, lines 1-{min(first, 32)} ---")
    print("\n".join(lines[:min(first, 32)]))
    for key in sorted(want, key=lambda x: [int(p) for p in x.split(".")]):
        if key not in rng:
            continue
        a, b = rng[key]
        if any(a >= x and b <= y for x, y in shown):
            continue
        shown.append((a, b))
        seg = lines[a:b]
        print(f"--- section {key}, lines {a + 1}-{b} ---")
        print("\n".join(seg[:MAXL]))
        if len(seg) > MAXL:
            print(f"[... {len(seg) - MAXL} more lines in this section not shown]")
    # 'find it' items: lines quoted in the evidence
    quotes = re.findall(r"'([^']{12,})'", text) + re.findall(r"`([^`]{8,})`", text)
    hits = set()
    for q in quotes:
        key = q.split("...")[0].strip()[:40]
        for i, l in enumerate(lines):
            if key and key in l and not any(a <= i < b for a, b in shown):
                hits.add(i)
    for m in re.findall(r"line (\d+)", text):
        i = int(m) - 1
        if 0 <= i < len(lines) and not any(a <= i < b for a, b in shown):
            hits.add(i)
    if hits:
        print("--- other lines the items point at ---")
        for i in sorted(hits)[:40]:
            print(f"L{i + 1}: {lines[i]}")
    print("--- all section headings ---")
    print(" | ".join(f"{k}@L{a + 1}" for k, (a, _) in rng.items()))
    print(f"\nWrite your JSON to: {MP / 'tmp' / f'{story}-{c.stem}.json'}")
    print(f"Then run: python -I \"{Path(__file__).resolve()}\" apply {story} {c.stem}")


def apply(story, cid):
    j = json.loads((MP / "tmp" / f"{story}-{cid}.json").read_text(encoding="utf-8"))
    f = MP / "out" / f"{story}.md"
    t = f.read_text(encoding="utf-8")
    for n, e in enumerate(j.get("edits", []), 1):
        old, new = e["old"], e["new"]
        for ln in new.split("\n"):
            s = ln.strip()
            if s.startswith("|") and not s.endswith("|"):
                sys.exit(f"EDIT {n} FAILED: table row does not end with '|': {s[-80:]!r}. Nothing was applied.")
        k = t.count(old)
        if k != 1:
            sys.exit(f"EDIT {n} FAILED: 'old' occurs {k} times (must be exactly 1). Nothing was applied. "
                     f"Copy a longer exact piece of the current text and write the JSON again. old starts: {old[:80]!r}")
        t = t.replace(old, new, 1)
    items = {re.search(r"; ruling (R-\d+);", l).group(1) for l in
             (MP / "chunks" / story / f"{cid}.md").read_text(encoding="utf-8").splitlines() if "; ruling R-" in l}
    disp = j.get("disposition", [])
    got = {d.get("ruling") for d in disp}
    if items - got:
        sys.exit(f"DISPOSITION INCOMPLETE: no row for {sorted(items - got)}. Nothing was applied.")
    bad = [d for d in disp if d.get("status") not in ("Resolved", "Cross-document", "Not applied")]
    if bad:
        sys.exit(f"BAD STATUS in {bad[0]}. Nothing was applied.")
    f.write_text(t, encoding="utf-8")
    d = MP / "disp" / story
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{cid}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in disp), encoding="utf-8")
    left = len(undone(story))
    print(f"OK {story} {cid}: {len(j.get('edits', []))} edits applied; {left} chunk(s) left for this story")


def nxt(stories):
    for s in stories:
        if undone(s):
            print(s)
            return
    print("ALL DONE")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    (MP / "tmp").mkdir(exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "show":
        show(sys.argv[2])
    elif cmd == "apply":
        apply(sys.argv[2], sys.argv[3])
    elif cmd == "next":
        nxt(sys.argv[2:])
