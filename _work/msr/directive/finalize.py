"""Assemble the directive run outputs (D-RCV-60, 26 November 2026).

  stories   mp/out/<story>.md (script fixes + model edits) -> change log line and Status row, staged as the next
            version of the project file, under <stage>/04 User stories/Recovery Workbench Service Story Files v2/...
  summary   counts of dispositions; cross-document changes grouped by target document (jsonl + md)

Usage: python -I finalize.py --stage <dir outside or inside _work> [--only-complete]
Writes only under --stage. Never writes a project file (promotion is a separate copy step).
"""
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
MP = D / "mp"
ROOT = D.parents[2]
sys.path.insert(0, str(D))
import esc  # noqa: E402
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
DATE = "26 November 2026"


def bump(name):
    m = re.search(r" v(\d+)\.md$", name)
    return name[:m.start()] + f" v{int(m.group(1)) + 1}.md"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--verified-only", action="store_true")
    a = ap.parse_args()
    stage = Path(a.stage).resolve()
    stories = [s for s, _ in json.loads((MP / "stories.json").read_text())]
    tot, cross, notdone, problems = Counter(), [], [], []
    staged, tagfix = [], [0]
    for s in stories:
        meta = json.loads((MP / "chunks" / s / "meta.json").read_text(encoding="utf-8"))
        n = meta["chunks"]
        if len(list((MP / "disp" / s).glob("c*.jsonl"))) < n or (a.verified_only and not esc.verified(s)):
            notdone.append(s)
            continue
        disp = list(esc.merged_dispositions(s).values())
        c = Counter(d["status"] for d in disp)
        tot.update(c)
        for d in disp:
            d["story"] = s
            if d["status"] == "Cross-document":
                cross.append(d)
        t = (MP / "out" / f"{s}.md").read_text(encoding="utf-8")
        line = (f"**Change log.** D-RCV-60, {DATE}: directive resolutions under the programme directive "
                f"({c['Resolved']} resolved, {c['Cross-document']} cross-document, {c['Not applied']} not applied). "
                f"Tool: {TOOL}.")
        logs = [m for m in re.finditer(r"^\*\*Change log\.\*\*.*$", t, re.M)]
        if logs:
            e = logs[-1].end()
            t = t[:e] + "\n\n" + line + t[e:]
        else:
            problems.append(f"{s}: no change log line; added after the header table")
            m = re.search(r"^\| Status \|.*$", t, re.M)
            e = m.end() if m else 0
            t = t[:e] + "\n\n" + line + t[e:]
        # origin tag of new ACs (run_all C05): every Scenario line this run added ends with (new, D-RCV-60)
        before = Path(meta["input_file"]).read_text(encoding="utf-8")
        old_lines = set(before.split("\n"))
        fixed = []
        for ln in t.split("\n"):
            if (re.match(r"^\s*Scenario:\s*AC\d+", ln) and ln not in old_lines and
                    not re.search(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, D-RCV-60)\)", ln)):
                ln2 = re.sub(r"\s*\(new[^)]*\)\s*$", "", ln.rstrip())
                ln = ln2 + " (new, D-RCV-60)"
                tagfix[0] += 1
            fixed.append(ln)
        t = "\n".join(fixed)
        t2, k = re.subn(r"^\| Status \| [^|]*\|", "| Status | Draft (directive resolutions) |", t, count=1, flags=re.M)
        if not k:
            problems.append(f"{s}: no Status row")
        pf = Path(meta["project_file"])
        parts = list(pf.parts)
        parts[1] = parts[1].replace("Service Story Files v1", "Service Story Files v2")
        dest = stage / Path(*parts[:-1]) / bump(pf.name)
        if (ROOT / Path(*parts[:-1]) / bump(pf.name)).exists():
            problems.append(f"{s}: {dest.name} already exists in the project; not staged")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(t2, encoding="utf-8")
        staged.append(str(dest.relative_to(stage)))
    # cross-document register
    by = defaultdict(list)
    for d in cross:
        for tg in re.split(r";\s*", d.get("target") or "Not named"):
            by[tg.strip() or "Not named"].append(d)
    (stage / "_directive").mkdir(parents=True, exist_ok=True)
    with (stage / "_directive/cross_document.jsonl").open("w", encoding="utf-8") as fh:
        for d in cross:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    summ = {"stories_staged": len(staged), "stories_not_done": len(notdone), "dispositions": dict(tot),
            "cross_targets": len(by), "ac_tags_fixed": tagfix[0], "problems": problems[:200]}
    (stage / "_directive/summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1), encoding="utf-8")
    (stage / "_directive/targets.json").write_text(
        json.dumps(sorted(((k, len(v)) for k, v in by.items()), key=lambda x: -x[1]), ensure_ascii=False, indent=0),
        encoding="utf-8")
    print(json.dumps({k: v for k, v in summ.items() if k != "problems"}), "problems", len(problems))


if __name__ == "__main__":
    main()
