"""Document-level pass (D-RCV-60): write accepted changes into target documents as next versions.

Work units: one target document, up to 12 items per session. Items come from
  nostory   the register gaps with no story (mp/nostory.json), mapped to their source document
  cross     the Cross-document dispositions of finished stories (mp/targets/by_target.jsonl)
Sonnet 5.5 (medium) reads the document through docview.py (read-only, capped) and returns fix records; docwriter
applies them to the staged next version, all or none. Failures are retried with the error (3 tries), then the
unit goes to Opus 5.5 (3 tries) when --opus, else to mp/esc/opus_queue.jsonl. Units of one document run in order.

Results: mp/docpass/<doc id>/<unit>.json and mp/docpass/dispositions.jsonl
  {"item": GAP id or ruling, "story": "", "target": file, "status": "Resolved|Not applied|Already present|
   Belongs elsewhere", "note": ..., "model": ...}
Usage: python -I docpass.py nostory|cross [--jobs 4] [--opus] [--docs <substring>] [--limit N] [--dry-run]
"""
import argparse, hashlib, json, re, sys, threading, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import esc, docwriter, targets  # noqa: E402

ROOT, MP = esc.ROOT, esc.MP
STAGE = D / "stage"
OUT = MP / "docpass"
BATCH = 12
lock = threading.Lock()
VIEW = f'python -I "{D / "docview.py"}"'

SYSTEM = """You write accepted changes into one target document of the Recovery Workbench document set (decision
D-RCV-60). A programme directive (26 November 2026) accepts the recommended resolution of every listed gap or
change request. You produce exact fix records; a script writes them into the next version of the document.

Look at the document only through these read-only commands (Bash), and keep each output small:
  {view} info  "<file>"                      structure: sheets/tables/headings and headers
  {view} find  "<file>" "<text>" ["<text>"]  rows/paragraphs/lines containing all the texts
  {view} rows  "<file>" "<sheet or table index>" <from> <n>
  {view} lines "<file>" <from> <n>
You may also Grep or Read other project files read-only to find a value an item cites (small reads only).

Fix record formats (every record has "fix_id": "F1", "F2", ... and "finding": the item ID it serves):
  text files (.md .yaml .csv .txt .json):
    {{"op": "replace", "old": "<exact text, occurs once>", "new": "..."}}
    {{"op": "insert_after", "old": "<one full existing line, exact>", "new": "<one or more new lines>"}}
  workbooks (.xlsx):
    {{"op": "xlsx_append", "sheet": "...", "header_row_hint": "<a header cell value>", "key": "<header whose values must be new>", "rows": [{{"<header>": "<value>", ...}}]}}
    {{"op": "xlsx_set", "sheet": "...", "key_header": "...", "key": "<key value of the row>", "header": "<column>", "old": "<exact current value>", "new": "..."}}
  Word documents (.docx):
    {{"op": "docx_replace", "old": "<exact text inside one paragraph or table cell, occurs once>", "new": "..."}}
    {{"op": "docx_insert_after", "old": "<exact full text of an existing paragraph>", "new": "<new paragraph text>"}}
    {{"op": "docx_table_append", "header_has": "<text of the first header cell of the table>", "values": ["<one value per column>"]}}

Rules
- Make the smallest change that carries the accepted resolution into this document. Keep the document's style,
  IDs and numbering. A new row follows the columns of its sheet or table exactly.
- Never invent a value (number, threshold, code, ID, role code, field name, payload, path). Use what the item,
  this document or a cited source gives; otherwise write 'Not specified in the source documents (<item ID>)'.
- If the document already holds the change, status 'Already present'. If the change belongs to another
  document, status 'Belongs elsewhere' and name it in note. 'Not applied' only when it would need an invented
  value or a business decision.
- Several items may ask for the same change: write it once, and give each item its own disposition row.
- Never change dates, release dates, decision IDs or Tool lines. No people's names. No tool or model trailers.
Reply with ONE JSON object and nothing else:
{{"fixes": [...], "disposition": [{{"item": "<item ID as given>", "status": "Resolved|Already present|Belongs elsewhere|Not applied", "fix_ids": ["F1"], "note": "under 200 characters"}}]}}
""".format(view=VIEW)


def doc_id(rel):
    return re.sub(r"[^A-Za-z0-9]+", "-", Path(rel).stem)[:60] + "-" + hashlib.md5(rel.encode()).hexdigest()[:6]


def load_map():
    p = MP / "targets/model_map.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def to_file(key, mm):
    targets.resolve_files() if not targets.FILES else None
    if key.startswith("OTHER:"):
        v = mm.get(key[6:], {})
        f = str(v.get("file", "NONE"))
        if f == "NONE" or f.startswith("STORY:") or not (ROOT / f.rstrip("/")).exists() or f.endswith("/"):
            return None
        return f
    if key.startswith("API:"):
        return targets.FILES.get(key)
    return targets.FILES.get(key)


NOSTORY_MAP_SYSTEM = """You decide where the accepted resolution of each listed gap must be written in a project's document
set. For each numbered gap, choose the ONE catalog document that should carry the resolution (the document the
resolution changes or adds to, not merely the document where the gap was found; a text extract of slides is never
the target when a decision record, design document or register can carry it). Copy the path exactly; add the file
name inside a folder entry. Answer NONE when the resolution only needs a business decision, a meeting, or a
document that is not in the catalog. Reply with ONE JSON object and nothing else:
{"map": {"<number>": {"file": "<catalog path or NONE>", "why": "under 80 characters"}}}"""


def map_nostory(jobs=4):
    import targets_model
    p = OUT / "nostory_targets.json"
    known = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    items = [i for i in json.loads((MP / "nostory.json").read_text(encoding="utf-8")) if i["Item ID"] not in known]
    cat = "\n".join(targets_model.catalog())
    batches = [items[i:i + 40] for i in range(0, len(items), 40)]

    def one(b):
        prompt = "## Catalog\n" + cat + "\n\n## Gaps\n" + "\n".join(
            f"{k}. {it['Item ID']}: {it.get('Title', '')} | resolution: {it.get('Proposed fix', '')} | "
            f"evidence: {str(it.get('Evidence', ''))[:200]}" for k, it in enumerate(b, 1))
        for _ in range(3):
            text, cost, err = esc.call(*esc.SONNET, NOSTORY_MAP_SYSTEM, prompt)
            if err:
                continue
            try:
                m = esc.parse(text)["map"]
                return {b[int(k) - 1]["Item ID"]: v for k, v in m.items() if k.isdigit() and 0 < int(k) <= len(b)}
            except Exception:
                continue
        return {}

    OUT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(jobs) as ex:
        for res in ex.map(one, batches):
            known.update(res)
            p.write_text(json.dumps(known, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"nostory targets mapped: {len(known)} | cost ${esc.stats['cost']:.2f}", flush=True)


def units_nostory():
    """Register gaps with no story, grouped by the target document Sonnet chose for their resolution."""
    tm = json.loads((OUT / "nostory_targets.json").read_text(encoding="utf-8")) if (OUT / "nostory_targets.json").exists() else {}
    mm = load_map()
    reg = {}
    for line in (ROOT / "23 Document Gaps/Recovery Workbench Gap Register v1.md").open(encoding="utf-8"):
        if line.startswith("| GAP-"):
            c = [x.strip() for x in line.split("|")]
            reg[c[1]] = c
    items = json.loads((MP / "nostory.json").read_text(encoding="utf-8"))
    by, unmapped = defaultdict(list), []
    for it in items:
        c = reg.get(it["Item ID"])
        src = c[3] if c else ""
        f = str(tm.get(it["Item ID"], {}).get("file", "")) or None
        if f in ("NONE", "None") or (f and (f.endswith("/") or not (ROOT / f).exists())):
            f = None
        if not f:
            unmapped.append(it["Item ID"])
            continue
        by[f].append({"item": it["Item ID"], "story": "", "text": "\n".join(
            [f"## {it['Item ID']} ({it.get('Severity', '')})", f"- Title: {it.get('Title', '')}",
             f"- Source: {src}", f"- Section: {c[4] if c else ''}", f"- Description: {it.get('Detail', '')}",
             f"- Evidence: {it.get('Evidence', '')}", f"- Accepted resolution: {it.get('Proposed fix', '')}",
             f"- Owner role: {it.get('Owner role', '')}"])})
    return by, unmapped


READY_ALL = False


def units_cross(ready_only=True):
    mm = load_map()
    by, unmapped, notready = defaultdict(list), [], set()
    p = MP / "targets/by_target.jsonl"
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []
    for r in rows:
        f = None
        for k in r["keys"]:
            if k.startswith("STORY:"):
                continue
            f = to_file(k, mm)
            if f:
                break
        if not f:
            unmapped.append(r["ruling"])
            continue
        if not r.get("final"):
            notready.add(f)
        by[f].append({"item": r["ruling"], "story": r["story"], "text": "\n".join(
            [f"## {r['ruling']} (item {r.get('item')}, from story {r['story']})",
             f"- Change the story asks of this document: {r.get('change', '')}",
             f"- Target as written: {r.get('target', '')}", f"- Note: {r.get('note', '')}"])})
    if not READY_ALL:  # a document waits until every story citing it is reviewed
        for f in notready:
            by.pop(f, None)
    return by, unmapped


def run_unit(rel, unit_items, uid, use_opus):
    need = {u["item"] for u in unit_items}
    info_rc = __import__("subprocess").run([sys.executable, "-I", str(D / "docview.py"), "info", rel],
                                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    base = (f"# Target document: {rel}\n\n## Structure now\n{info_rc.stdout[:6000]}\n\n## Items ({len(unit_items)})\n"
            + "\n\n".join(u["text"] for u in unit_items))
    rec = {"target": rel, "unit": uid, "items": sorted(need), "steps": []}
    models = [esc.SONNET] + ([esc.OPUS] if use_opus else [])
    for model, effort in models:
        step = {"model": model, "tries": [], "applied": False}
        err = ""
        for k in range(3):
            prompt = base if not err else base + "\n\n=== YOUR PREVIOUS REPLY FAILED ===\n" + err + \
                "\nReply again with the whole corrected JSON object."
            text, cost, cerr = esc.call(model, effort, SYSTEM, prompt, tools="docview", timeout=1500)
            if cerr:
                err = cerr
                step["tries"].append({"error": cerr})
                continue
            try:
                j = esc.parse(text)
            except Exception as e:
                err = f"not one valid JSON object: {e}"
                step["tries"].append({"error": err})
                continue
            got = {d.get("item") for d in j.get("disposition", [])}
            if need - got:
                err = f"DISPOSITION INCOMPLETE: no row for {sorted(need - got)}"
                step["tries"].append({"error": err})
                continue
            fixes = j.get("fixes", [])
            for f in fixes:
                f["fix_id"] = f"{uid}-{f.get('fix_id', 'F')}"
            try:
                with lock:
                    if fixes:
                        docwriter.write_next(rel, fixes, STAGE)
                step.update(applied=True, fixes=fixes, disposition=j["disposition"])
                step["tries"].append({"ok": True, "fixes": len(fixes)})
                break
            except (docwriter.WriteError, Exception) as e:
                err = f"WRITE FAILED (nothing was written): {e}"
                step["tries"].append({"error": err[:500]})
        rec["steps"].append(step)
        if step["applied"]:
            break
    last = rec["steps"][-1]
    if not last["applied"] and not use_opus:
        esc.queue_opus("docpass", "", f"{rel}#{uid}", "Sonnet failed 3 tries: " + err[:200], need)
    out = OUT / doc_id(rel)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{uid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    with lock, (OUT / "dispositions.jsonl").open("a", encoding="utf-8") as fh:
        st = {u["item"]: u["story"] for u in unit_items}
        for d in (last.get("disposition") or [{"item": i, "status": "Not applied", "note": "write failed: " + err[:150]}
                                              for i in need]):
            fh.write(json.dumps({"item": d["item"], "story": st.get(d["item"], ""), "target": rel,
                                 "status": d.get("status"), "note": d.get("note", ""), "fix_ids": d.get("fix_ids", []),
                                 "model": last["model"], "unit": uid}, ensure_ascii=False) + "\n")
    return last["applied"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", choices=["nostory", "cross", "map-nostory"])
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--opus", action="store_true")
    ap.add_argument("--backend", choices=["claude", "haiku"], default="claude")
    ap.add_argument("--all-ready", action="store_true", help="ignore readiness (testing only)")
    ap.add_argument("--docs")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    targets.resolve_files()
    if a.backend == "haiku":
        esc.SONNET = esc.OPUS = ("claude-haiku-5-5", "medium")
    if a.source == "map-nostory":
        return map_nostory(a.jobs)
    by, unmapped = units_nostory() if a.source == "nostory" else units_cross()
    docs = sorted(by, key=lambda f: -len(by[f]))
    if a.docs:
        docs = [d for d in docs if a.docs.lower() in d.lower()]
    if a.limit:
        docs = docs[:a.limit]
    print(f"{a.source}: {sum(len(by[d]) for d in docs)} items over {len(docs)} documents; {len(unmapped)} unmapped",
          flush=True)
    for d in docs[:40]:
        print(f"  {len(by[d])} {d}", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"unmapped-{a.source}.json").write_text(json.dumps(unmapped), encoding="utf-8")
    if a.dry_run:
        return
    prefix = "N" if a.source == "nostory" else "X"

    done_keys = set()
    dp = OUT / "dispositions.jsonl"
    if dp.exists():
        for l in dp.read_text(encoding="utf-8").splitlines():
            if l.strip():
                x = json.loads(l)
                done_keys.add((x["item"], x.get("story", ""), x["target"]))

    def one_doc(rel):
        # skip items already handled for this document; new units are numbered after the existing ones
        its = [u for u in by[rel] if (u["item"], u["story"], rel) not in done_keys]
        have = [int(p.stem[1:]) for p in (OUT / doc_id(rel)).glob(f"{prefix}*.json")] if (OUT / doc_id(rel)).exists() else []
        start = max(have, default=0)
        for k in range(0, len(its), BATCH):
            uid = f"{prefix}{start + k // BATCH + 1:03d}"
            if (MP / "STOP_DOC").exists():
                continue
            ok = run_unit(rel, its[k:k + BATCH], uid, a.opus)
            print(f"{time.strftime('%H:%M:%S')} {Path(rel).name} {uid} {'OK' if ok else 'QUEUED FOR OPUS'} | "
                  f"cost ${esc.stats['cost']:.2f}", flush=True)

    with ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(one_doc, docs))
    print(f"END docpass {a.source} | {json.dumps(esc.stats)}", flush=True)


if __name__ == "__main__":
    main()
