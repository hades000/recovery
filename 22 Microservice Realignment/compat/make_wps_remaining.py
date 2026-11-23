"""Build the remaining-work queue: one legacy key per story WP, compact context packs, docs interleaved.

Only files that do not exist are written. Completed story files and DONE document WPs are never
included, so this queue can run beside or after the original queue without redoing finished work.
"""
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, STORIES, SERVICES, svc, read_json, write_json, decision
import make_wps as mw

DEC = decision()
STORY_RX = re.compile(r"^B-(P10|P[1-9]|S[1-9]|ITG|PLT)-")
THIN = re.compile(r"^RWB-E[3-8]-")

RULES = """Do, for each story line below (one JSON object per line), write exactly one file at its "file" path:
1. Use the template in Template and Rules v1 §R7: the 19 headings in order, the metadata table rows of §R7.1 in order (never remove a row).
   Copy these values exactly from the JSON: Story key=id, Work type, Suggested owner (fixed phrase for "owner"), Service, Service epic=epic,
   Wave, Business epic, Release (+ " (tentative)"; "None (new story)" when empty), Legacy key, Legacy disposition, Build status,
   Patterns applied, Parallel lane, Ready to start, Depends on (build)=H, Contract dependencies=C, Integration dependencies=I,
   External dependencies=X, PRD reference "Pending (C1)", Status "Draft (realignment v1)".
2. preserved=true: copy legacy §1-11, §14-16, §18 and §19 word for word; keep §12 and §13 under the heading "As built (monolith)".
3. delta=true: describe only the microservice change for that legacy key in Template and Rules §R6.
4. ACs: "acs" lists the legacy AC IDs this story owns. Copy each verbatim with the origin tag "(legacy <legacy> <AC>)".
   An APP AC whose cross-service part can be mocked gets the Given "Given the <service> contract mock returns <x>" (keep every value).
   CON, DB, INF, OPS and new stories: write ACs tagged "(new, {dec})" that test only the deliverable in the title. Never invent business values.
5. TCs: keep the legacy TC IDs of the ACs this story owns; an ITG copy of a TC gets the suffix -ITG. Add the Level column (§R7.2 s16).
6. Apply the DP table (§R5.5) for every pattern in "patterns"; list them in "Patterns applied". The context pack repeats the DP table in short form.
7. Section 12 Contract: tables 12.1-12.9 (or None). Names: topic rwb.<short>.events.v1, event rwb.<short>.<Event>.v1, queue rwb-<short>,
   REST base /api/recovery/<short>/v1, schema rwb_<name>. Owners come from the context pack and the Ownership Map only.
8. Write _work/msr/fragments/<id>.json with keys: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy,
   disposition, H, C, I, X, acs [{"id","origin","text_first_line"}], tcs, reqs, ops_provided, ops_consumed, events_published,
   events_consumed, workflows, prd_ref "Pending (C1)", gaps [CG ids], assumptions [ASM ids], file.
9. A missing value: "Not specified in the source documents (CG-{wp}-<n>; ASM-{wp}-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/{wp}.jsonl and _work/msr/assumptions/{wp}.jsonl.
10. Be concise. Complete all 19 sections, but do not repeat the same background in more than one section. Aim for 20-25 KB per file;
    keep any section that is not a table under 30 lines. The metadata table, the ACs and the §12 contract tables must stay complete and exact.
11. Do not run checks/run_all.py. The coordinator runs checks centrally after the stage. Finish by writing the edit log and replying with the files written.
12. Use the context pack as the authority for service facts. Do not read the full Architecture v5 extract, the Temporal/Drools extract or ownership.json;
    the pack already contains the service row, its ownership rows, the matching slides and the naming rules. Read the legacy story and the module FSD/TSD for business detail.
"""

def src_lines(sl):
    out = []
    for s in sl:
        src = s.get("source")
        if src and f"- {src} (heading {s['legacy']})" not in out:
            out.append(f"- {src} (heading {s['legacy']})")
    return out

def valid_slice(s):
    p = ROOT / s["file"]
    f = WORK / "fragments" / f"{s['id']}.json"
    if not p.exists() or not f.exists():
        return False
    t = p.read_text(encoding="utf-8", errors="replace")
    if not (t.startswith("# RWB-") and "### 19. Out of scope" in t and "| Story key |" in t):
        return False
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return False
    return all(k in d for k in ("id", "epic", "service", "wt", "file"))

def build_story_wps(plan):
    missing = defaultdict(list)
    for s in plan["slices"]:
        if not valid_slice(s):
            missing[(s["epic"], s["legacy"])].append(s)
    counters = Counter()
    out = []
    for (epic, key), sl in sorted(missing.items(),
                                  key=lambda kv: (kv[0][0], min(x.get("lane") or "" for x in kv[1]), kv[0][1])):
        code = epic.replace("RWB-SVC-", "").replace("RWB-", "")
        counters[epic] += 1
        wp = f"B2-{code}-{counters[epic]:03d}"
        scopes = sorted({s["scope"] for s in sl})
        reads = [f"- {mw.TPL} (read fully first)"]
        reads += [f"- _work/msr/context/{sc}.md" for sc in scopes if (WORK / "context" / f"{sc}.md").exists()]
        reads += src_lines(sl)
        mods = [sc for sc in scopes if sc not in ("PLT", "ITG")]
        for sc in mods:
            reads.append(f"- _work/msr/extract/ files of the FSD and TSD folders whose name contains \"{sc}\" (module {svc(sc)['name']})")
        if THIN.match(key):
            reads.append("- Thin story: _work/msr/extract/Recovery Workbench Business Epics 3 to 8 Specification v3.md and "
                         "_work/msr/extract/Recovery Workbench Business Rules and Routing Logic v4.md (fill order Template and Rules §R7.3)")
        outs = [s["file"] for s in sl] + [f"_work/msr/fragments/{s['id']}.json" for s in sl]
        text = (f"# WP {wp} — {epic}: legacy {key}\n"
                + mw.HEADER.format(agent="aisdlc-msr-worker", fanout=0)
                + "Read only:\n" + "\n".join(reads) + "\nWrite only:\n" + "\n".join(f"- {o}" for o in outs)
                + f"\n- _work/msr/gaps/{wp}.jsonl\n- _work/msr/assumptions/{wp}.jsonl\n- _work/msr/editlog/{wp}.md\n"
                + RULES.replace("{wp}", wp).replace("{dec}", DEC) + "Stories:\n"
                + "\n".join(json.dumps({k: s.get(k) for k in mw.KEEP}, ensure_ascii=False) for s in sl) + "\n"
                + f"Finish: write _work/msr/editlog/{wp}.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; reply with the list of files written.\n")
        text = text.replace("\ufffd", "-")
        out.append({"wp": wp, "keys": [key], "text": text, "expect": outs + [f"_work/msr/editlog/{wp}.md"],
                    "fanout": False, "agent": "aisdlc-msr-worker", "category": "story",
                    "scope": scopes[0] if len(scopes) == 1 else "+".join(scopes)})
    return out

def build_docs(queue, status):
    out = []
    for item in queue:
        if STORY_RX.match(item["wp"]):
            continue
        if status.get(item["wp"], {}).get("state") == "DONE":
            continue
        out.append(item)
    return out

def interleave(stories, docs):
    q, si, di = [], 0, 0
    while si < len(stories) or di < len(docs):
        for _ in range(2):
            if si < len(stories):
                q.append(stories[si]); si += 1
        if di < len(docs):
            q.append(docs[di]); di += 1
    return q

def main():
    plan = read_json(WORK / "plan" / "split_plan.json")
    status = read_json(WORK / "status.json", {}) or {}
    queue = read_json(WORK / "wp" / "queue-B.json", []) or []
    stories = build_story_wps(plan)
    docs = build_docs(queue, status)
    for w in stories:
        p = WORK / "wp" / f"{w['wp']}.md"
        p.write_text(w["text"], encoding="utf-8")
    q = interleave(stories, docs)
    items = [{"wp": w["wp"], "agent": w["agent"], "file": str((WORK / "wp" / f"{w['wp']}.md").relative_to(ROOT)).replace("\\", "/"),
              "fanout": False, "expect": w["expect"]} for w in q]
    write_json(WORK / "wp" / "queue-B2.json", items)
    write_json(WORK / "plan" / "queue-B2-summary.json", {
        "story_wps": len(stories), "doc_wps": len(docs), "total": len(items),
        "story_files_missing": sum(1 for w in stories for e in w["expect"] if e.startswith("04 User stories")),
        "by_epic": dict(sorted(Counter(w["wp"].split("-")[1] for w in stories).items())),
        "context_packs": sorted(p.name for p in (WORK / "context").glob("*.md")),
    })
    print("B2 OK", {"story_wps": len(stories), "doc_wps": len(docs), "total": len(items)})

if __name__ == "__main__":
    main()
