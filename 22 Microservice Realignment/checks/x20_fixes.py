"""Version-reference fixes for story files (X20; sandbox prototype, D-RCV-60).

For every story file, each line that names a document at a version lower than the highest in the
Document Index gets one exact replace record: the whole line, with each old 'Name vN' set to the
highest version. The longest document name wins where two names overlap ('Case and Workflow Model'
before 'Workflow Model'). Lines that are history are held, never rewritten:
  - change-log lines ('**Change log.**') and lines that say a version was superseded or replaced;
  - a line whose text also occurs inside such a history line (an exact replace would reach it).
Usage: python -I x20_fixes.py --root <ROOT> --out <dir> [--story <path> ... | --all]
Writes only under --out: fixes.jsonl, held.jsonl, summary.md. Apply with apply_fixes.py.
"""
import argparse, json, re, sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rwbsrc  # noqa: E402

HISTORY = re.compile(r"^\*\*Change log\.\*\*|supersed|replac(es|ed|ing)\b|was renamed|carried forward", re.I)
# a sentence that says what a particular version holds or lacks: moving it to a new version is a claim nobody checked
CLAIM = re.compile(r"\b(only|as held|as written|as found|declares no|names no|has no|holds no|gives no|does not|"
                   r"is not|are not|no such|not in|nowhere|not specified|not stated|not named|missing|absent|lacks?)\b", re.I)
EXT = re.compile(r"\.(xlsx|docx|sql|md|yaml|csv|pptx|pdf|txt)\b", re.I)


def sentence(line, s, e):
    """The table cell or sentence around [s, e) of the line."""
    st = max(line.rfind(x, 0, s) for x in ("|", ". ", "; ")) + 1
    ends = [i for i in (line.find(x, e) for x in ("|", ". ", "; ")) if i >= 0]
    return line[st:min(ends) if ends else len(line)]


def plan_line(line, pats, files=None):
    """Return (new line, [(old, new)]) with the longest non-overlapping name matches replaced.
    `pats` is (one regex of every name, longest first, {name: highest version}). The longest name is
    consumed even when its version is current, so a shorter name inside it is never rewritten."""
    rx, best = pats
    if " v" not in line:
        return line, [], []
    keep, risky = [], []
    for m in rx.finditer(line):  # alternation tries the longest name first at each position
        name, ov = m.group(1), int(m.group(2))
        if ov >= best[name]:
            continue
        pair = (f"{name} v{ov}", f"{name} v{best[name]}")
        x = EXT.match(line, m.end())
        if x and files is not None and f"recovery workbench {name} v{best[name]}{x.group(0)}".lower() not in files:
            risky.append((pair, f"file reference: no file 'Recovery Workbench {name} v{best[name]}{x.group(0)}' exists"))
            continue
        if CLAIM.search(sentence(line, m.start(), m.end())):
            risky.append((pair, "claim about what this version holds or lacks: the owner checks it against the new version"))
            continue
        keep.append((m.start(), m.end(), name, ov, best[name]))
    if not keep:
        return line, [], risky
    out, pos, pairs = [], 0, []
    for s, e, name, ov, nv in keep:
        out += [line[pos:s], f"{name} v{nv}"]
        pairs.append((f"{name} v{ov}", f"{name} v{nv}"))
        pos = e
    out.append(line[pos:])
    return "".join(out), pairs, risky


def make_pats(best):
    """One regex of every document name, longest first, with the highest version of each."""
    names = sorted(best, key=len, reverse=True)
    return (re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, names)) + r") v(\d+)\b"), best)


def files_on_disk(root):
    import os
    return {f.lower() for d, ds, fs in os.walk(root) if ".git" not in Path(d).parts for f in fs + ds}


def plan_file(text, rel, key, pats, on_disk, finding=None, source="Document Index v14 (highest version of each document)"):
    """Exact whole-line replace records for one file, and the lines held. Returns (fixes, held, pairs)."""
    lines = text.split("\n")
    hist = [l for l in lines if HISTORY.search(l)]
    fixes, held, per_pair = [], [], Counter()
    done, cand = set(), []
    for i, l in enumerate(lines):
        if l in done:
            continue
        new, pairs, risky = plan_line(l, pats, on_disk)
        if risky and not HISTORY.search(l):
            for pair, why in risky:
                held.append(OrderedDict(story=key, file=rel, line=i + 1, text=l[:300], reason=why, pairs=[pair]))
        if not pairs:
            if risky and HISTORY.search(l):
                held.append(OrderedDict(story=key, file=rel, line=i + 1, text=l[:300],
                                        reason="history line (change log, superseded or replaced): the older version is kept",
                                        pairs=sorted({p for p, _ in risky})))
            continue
        why = None
        if HISTORY.search(l):
            why = "history line (change log, superseded or replaced): the older version is kept"
        elif l.strip() and any(l in h for h in hist if h != l):
            why = "the line also occurs inside a history line, so an exact replace would rewrite history"
        elif not l.strip():
            why = "empty line"
        if why:
            held.append(OrderedDict(story=key, file=rel, line=i + 1, text=l[:300], reason=why, pairs=sorted(set(pairs))))
            continue
        done.add(l)
        cand.append((l, new, pairs))
    # apply longest lines first on a working copy, so a line inside a longer one gets the count left after it
    work = text
    for l, new, pairs in sorted(cand, key=lambda c: -len(c[0])):
        c = work.count(l)
        if not c:
            continue  # fully covered by a longer line's fix
        work = work.replace(l, new)
        fixes.append(OrderedDict(fix_id="", finding=finding or f"X20 {key}", file=rel, op="replace", old=l, new=new,
                                 count=c, source=source))
        for pr in pairs:
            per_pair[pr] += 1
    return fixes, held, per_pair


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--story", nargs="+")
    g.add_argument("--story-list", help="a text file with one story path per line")
    a = ap.parse_args(argv)
    root, out = Path(a.root).resolve(), Path(a.out).resolve()
    if out == root or root in out.parents:
        sys.exit("--out must be outside ROOT (sandbox only)")
    src = rwbsrc.Sources(root, out / "_cache")
    pats = make_pats(src.doc_versions())
    on_disk = files_on_disk(root)
    if a.story_list:
        a.story = [l.strip() for l in Path(a.story_list).read_text(encoding="utf-8").splitlines() if l.strip()]
    if a.story:
        paths = [Path(p) for p in a.story]
    else:
        paths = sorted(p for p in (root / rwbsrc.TEXT["stories"]).rglob("*.md") if rwbsrc.story_key_from_name(p.name))
    fixes, held, per_pair, files = [], [], Counter(), 0
    for p in paths:
        text = p.read_text(encoding="utf-8", errors="replace")
        rel = str(p.resolve().relative_to(root)).replace("\\", "/")
        fx, hd, pp = plan_file(text, rel, rwbsrc.story_key_from_name(p.name), pats, on_disk)
        fixes += fx
        held += hd
        per_pair.update(pp)
        files += bool(fx)
    for i, f in enumerate(fixes, 1):
        f["fix_id"] = f"FX20-{i:05d}"
    out.mkdir(parents=True, exist_ok=True)
    for name, data in (("fixes.jsonl", fixes), ("held.jsonl", held)):
        with (out / name).open("w", encoding="utf-8") as f:
            for r in data:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    lines = ["# Version-reference fixes (X20)", "", f"Stories read: {len(paths)}. Files with fixes: {files}. "
             f"Line fixes: {len(fixes)}. Lines held: {len(held)}.", "", "| Old | New | Lines |", "|---|---|---|"]
    lines += [f"| {o} | {n} | {c} |" for (o, n), c in per_pair.most_common()]
    lines += ["", "## Held lines by reason", ""]
    lines += [f"- {r}: {c}" for r, c in Counter(h["reason"] for h in held).most_common()]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(paths)} stories, {files} files with fixes, {len(fixes)} line fixes, {len(held)} held -> {out}")


if __name__ == "__main__":
    main()
