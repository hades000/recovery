"""Light model check of the cross-document targets the rules could not map (D-RCV-60).

Builds a catalog of the latest version of every document in folders 01-12 and 22 (plus folder-versioned sets
such as API Specification v5 and Functional Specifications by Module v7), then asks Sonnet 5.5 (medium, no
tools) to map each unknown target text to one catalog entry, a story key, or NONE. Result: mp/targets/model_map.json
{text: {"file": <ROOT-relative path or STORY:key or NONE>, "why": ...}}; targets.py uses it on the next run.

Usage: python -I targets_model.py [--batch 120] [--jobs 6]
"""
import argparse, json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import esc  # noqa: E402

ROOT, MP = esc.ROOT, esc.MP
SYSTEM = """You map free-text names of target documents to the exact document in a catalog of a project's
document set. For each numbered target text, answer with one catalog path copied exactly, or STORY:<story key>
when the text names a user story (keys look like RWB-P4-E1037-CON), or NONE when no catalog entry fits.
Prefer the catalog entry whose document type matches (FSD = Functional Specifications by Module, TSD = Technical
Specification, ERD = Entity Relationship Diagram, RTM = Requirements Traceability Matrix). A folder entry stands
for every file inside it; add the file name inside the folder when the text names one (for example
'.../Recovery Workbench API Specification v5/rwb-access.yaml').
Reply with ONE JSON object and nothing else: {"map": {"<number>": {"file": "...", "why": "under 80 characters"}}}"""


def catalog():
    out = set()
    folders = [p for p in ROOT.iterdir() if p.is_dir() and re.match(r"(0\d|1[0-2]|22) ", p.name)]
    for f in folders:
        for p in f.rglob("*"):
            if any(x in p.parts for x in ("aisdlc", "checks", "compat", "_work")) or p.suffix.lower() == ".zip":
                continue
            rel = p.relative_to(ROOT)
            # a versioned folder stands for its files; list the folder and its direct files
            m = re.search(r" v(\d+)$", p.stem if p.is_file() else p.name)
            if p.is_dir() and m:
                out.add(rel.as_posix() + "/")
            elif p.is_file() and m and not any(re.search(r" v\d+$", q) for q in rel.parts[:-1]):
                out.add(rel.as_posix())
            elif p.is_file() and any(re.search(r" v\d+$", q) for q in rel.parts[:-1]) and len(rel.parts) <= 4:
                out.add(rel.as_posix())
    # keep the latest version of each stem
    best = {}
    for r in out:
        key = re.sub(r" v\d+(?=/|\.\w+$|$)", "", r)
        v = [int(x) for x in re.findall(r" v(\d+)(?=/|\.\w+$|$)", r)] or [0]
        if key not in best or v > best[key][0]:
            best[key] = (v, r)
    keep = [r for _, r in best.values() if "Story Files" not in r and not r.endswith((".png", ".svg", ".excalidraw", ".html"))]
    return sorted(keep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=120)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--backend", choices=["claude", "haiku"], default="claude")
    a = ap.parse_args()
    if a.backend == "haiku":
        esc.SONNET = ("claude-haiku-5-5", "medium")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cat = catalog()
    unk = [u["key"][6:] for u in json.loads((MP / "targets/unknown.json").read_text(encoding="utf-8"))]
    mp = MP / "targets/model_map.json"
    known = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
    todo = [u for u in unk if u not in known]
    print(f"catalog {len(cat)} entries; {len(todo)} texts to map", flush=True)
    cat_txt = "\n".join(cat)
    batches = [todo[i:i + a.batch] for i in range(0, len(todo), a.batch)]

    def one(b):
        prompt = ("## Catalog\n" + cat_txt + "\n\n## Target texts\n" +
                  "\n".join(f"{i}. {t}" for i, t in enumerate(b, 1)))
        for _ in range(3):
            text, cost, err = esc.call(*esc.SONNET, SYSTEM, prompt)
            if err:
                continue
            try:
                m = esc.parse(text)["map"]
                return {b[int(k) - 1]: v for k, v in m.items() if k.isdigit() and 0 < int(k) <= len(b)}
            except Exception:
                continue
        return {}

    with ThreadPoolExecutor(a.jobs) as ex:
        for res in ex.map(one, batches):
            known.update(res)
            mp.write_text(json.dumps(known, ensure_ascii=False, indent=0), encoding="utf-8")
            print(f"mapped {len(known)} | cost ${esc.stats['cost']:.2f}", flush=True)
    bad = {k: v for k, v in known.items() if v.get("file") not in ("NONE",) and not str(v.get("file", "")).startswith("STORY:")
           and not (ROOT / str(v.get("file", "")).rstrip("/")).exists()}
    print(f"done; {len(bad)} answers name a path that does not exist (treated as NONE)")


if __name__ == "__main__":
    main()
