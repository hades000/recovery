"""Opus 5.5 review of the 1,591 script fixes from rulings.py apply (apply-v4) and of Decision Log v12 (D-RCV-60).

Each fix is shown as a compact word diff (changed spans with context). Opus, in fresh sessions with no tools,
returns only the fixes that are wrong or unsure. Results: mp/review_fixes/b<NN>.json; non-ok fixes are added to
mp/esc/opus_queue.jsonl (stage scriptfix) for rework on the story copies.

Usage: python -I review_fixes.py --jobs 4 [--batch 80] [--limit N]
"""
import argparse, difflib, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import esc  # noqa: E402

APPLY = esc.SCRATCH / "apply-v4"
OUT = esc.MP / "review_fixes"
SYSTEM = """You review mechanical fixes made by scripts to the Recovery Workbench document set (decision D-RCV-60).
Most fixes replace a cited older document version with the current one (for example 'Logical Data Model and
Data Dictionary v8' -> 'v9'). A version reference must NOT be changed when the sentence is history (what an
older version said or held), a claim about what a specific version contains, or a file name that does not exist
in the new version. Other fixes apply a ruling value or add a Decision Log pointer column.

For each fix decide: ok, wrong (the change is incorrect or harmful), or unsure (needs an owner's check).
Reply with ONE JSON object and nothing else:
{"verdicts": [{"fix_id": "...", "verdict": "wrong|unsure", "issue": "under 200 characters", "suggest": "the correct text or action"}]}
List only wrong and unsure fixes; an empty list means every fix in the batch is ok."""


def wdiff(old, new, ctx=200):
    a, b = re.split(r"(\s+)", old), re.split(r"(\s+)", new)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        pre = "".join(a[max(0, i1 - 40):i1])[-ctx:]
        post = "".join(a[i2:i2 + 40])[:ctx]
        out.append(f"...{pre}[-{''.join(a[i1:i2])}-][+{''.join(b[j1:j2])}+]{post}...")
    return " | ".join(out)[:1500] or "(no visible change)"


def entries():
    fx = [json.loads(l) for l in (APPLY / "2-fixes/fixes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    out = []
    for f in fx:
        name = Path(f["file"]).name
        if f["op"] == "replace":
            body = wdiff(f.get("old", ""), f.get("new", ""))
        else:
            body = json.dumps({k: v for k, v in f.items() if k not in ("fix_id", "file", "finding")},
                              ensure_ascii=False)[:1200]
        out.append(f"### {f['fix_id']} ({f.get('finding', '')}) in {name} [{f['op']}]\n{body}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--batch", type=int, default=80)
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    es = entries()
    batches = [es[i:i + a.batch] for i in range(0, len(es), a.batch)]
    if a.limit:
        batches = batches[:a.limit]
    print(f"{len(es)} fixes in {len(batches)} batches", flush=True)

    def one(k):
        p = OUT / f"b{k + 1:02d}.json"
        if p.exists():
            return
        prompt = f"# Batch {k + 1} of {len(batches)}\n\n" + "\n\n".join(batches[k])
        err, res = "", None
        for t in range(3):
            text, cost, cerr = esc.call(*esc.OPUS, SYSTEM, prompt if not err else prompt + "\n\nPREVIOUS REPLY FAILED: "
                                        + err + "\nReply again with the JSON object.")
            if cerr:
                err = cerr
                time.sleep(10)
                continue
            try:
                res = esc.parse(text)
                break
            except (ValueError, json.JSONDecodeError) as e:
                err = str(e)
        rec = {"batch": k + 1, "fixes": [b.split(" ", 2)[1] for b in batches[k]], "result": res, "error": err if res is None else ""}
        p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        for v in (res or {}).get("verdicts", []):
            esc.queue_opus("scriptfix", "", v.get("fix_id", ""), f"{v.get('verdict')}: {v.get('issue', '')} | suggest: "
                           f"{v.get('suggest', '')}"[:600])
        print(f"{time.strftime('%H:%M:%S')} batch {k + 1}: {'ERROR ' + err if res is None else len(res.get('verdicts', []))} "
              f"flagged | cost ${esc.stats['cost']:.2f}", flush=True)

    with ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(one, range(len(batches))))


if __name__ == "__main__":
    main()
