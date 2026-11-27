"""Cross-document Change Register v1 and one review pack per service (D-RCV-60 directive run).

  register  <stage>/23 Document Gaps/Recovery Workbench Cross-document Change Register v1.{md,xlsx}
            every Cross-document disposition (story pass) plus the no-story and cross document-pass items that
            were not written, one row each, CDC-nnnnn, with the normalised target document
  packs     <stage>/23 Document Gaps/Recovery Workbench Service Review Packs v1/<service folder>/
              <service> - review pack.md      stories, open business decisions, not applied, cross-document
                                              changes by target, gap and assumption status, lint findings
              <service> - resolved items.md   every item resolved inside the stories (to spot-check the fixes)
            plus "Programme-wide (no story)" for register gaps and assumptions with no story, and README.md

Usage: python -I review_packs.py --stage <dir>
Reads only scratch outputs, the rulings v4 workbook and the staged registers v2. Writes only under --stage.
"""
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
MP = D / "mp"
ROOT = D.parents[2]
sys.path.insert(0, str(D))
import esc  # noqa: E402
import targets  # noqa: E402

DATE = "26 November 2026"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
RULINGS = ROOT / "_work/msr/rulings/All stories rulings v4.xlsx"
CDC = "Recovery Workbench Cross-document Change Register v1"
PACKS = "Recovery Workbench Service Review Packs v1"
NOSTORY = "Programme-wide (no story)"
PENDING = "Pending: listed for the target document; the cross-document pass has not run"


def cell(x, n=None):
    s = " ".join(str(x if x is not None else "").split()).replace("|", "\\|")
    return s if n is None or len(s) <= n else s[:n - 1] + "…"


def table(hdr, rows):
    out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return out


def read_xlsx(path, sheet, key):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True)[sheet]
    it = ws.iter_rows(values_only=True)
    h = list(next(it))
    return {str(r[h.index(key)]): dict(zip(h, r)) for r in it if r[h.index(key)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    stage = Path(a.stage).resolve()
    out23 = stage / "23 Document Gaps"
    targets.resolve_files()

    # stories -> service folder and staged file
    stories = [s for s, _ in json.loads((MP / "stories.json").read_text())]
    svc_of, staged_of = {}, {}
    sroot = stage / "04 User stories/Recovery Workbench Service Story Files v2"
    for s in stories:
        meta = json.loads((MP / "chunks" / s / "meta.json").read_text(encoding="utf-8"))
        pf = Path(meta["project_file"])
        svc_of[s] = pf.parts[2]
        m = re.search(r" v(\d+)\.md$", pf.name)
        name = pf.name[:m.start()] + f" v{int(m.group(1)) + 1}.md"
        staged_of[s] = (Path("04 User stories/Recovery Workbench Service Story Files v2") / pf.parts[2] / name).as_posix()
        assert (sroot / pf.parts[2] / name).exists(), staged_of[s]

    rul = read_xlsx(RULINGS, "Rulings", "Ruling ID")
    gaps2 = read_xlsx(out23 / "Recovery Workbench Gap Register v2.xlsx", "Gaps", "GAP ID")
    asm2 = read_xlsx(out23 / "Recovery Workbench Assumptions Register v2.xlsx", "Assumptions", "ASM ID") \
        if True else {}
    lint = defaultdict(list)
    for l in (MP / "lint-final.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            x = json.loads(l)
            lint[x["story"]].append(x)

    # item -> stories (rulings), and per-story dispositions
    item_stories = defaultdict(set)
    for r in rul.values():
        for s in re.split(r"[,;]\s*", str(r.get("Story") or "")):
            if s.strip() in svc_of:
                item_stories[str(r["Item ID"])].add(s.strip())
    disp = {s: esc.merged_dispositions(s) for s in stories}

    # ---- Cross-document Change Register
    cdc = []
    for s in stories:
        for rid, d in sorted(disp[s].items()):
            if d["status"] != "Cross-document":
                continue
            keys = targets.normalise(d.get("target", ""))
            docs = "; ".join(targets.FILES.get(k) or (k[6:] if k.startswith("STORY:") else k) or k for k in keys)
            cdc.append(dict(story=s, service=svc_of[s], ruling=rid, item=d.get("item", ""), section=d.get("section", ""),
                            target=d.get("target", ""), doc=docs, change=d.get("change", ""), note=d.get("note", ""),
                            status=PENDING, source="story pass"))
    dp = MP / "docpass/dispositions.jsonl"
    if dp.exists():
        for l in dp.read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            x = json.loads(l)
            if x.get("status") == "Resolved":
                continue
            s = x.get("story") or ""
            cdc.append(dict(story=s, service=svc_of.get(s, NOSTORY), ruling="", item=x.get("item", ""), section="",
                            target=x.get("target", ""), doc=x.get("target", ""), change=x.get("change", ""),
                            note=x.get("note", ""), status=f"Document pass: {x.get('status', '')}",
                            source="document pass"))
    for i, r in enumerate(cdc, 1):
        r["id"] = f"CDC-{i:05d}"
    hdr = ["CDC ID", "Service", "Story", "Ruling", "Item", "Section", "Target (as written)", "Target document",
           "Change", "Note", "Status", "Source"]
    keys = ["id", "service", "story", "ruling", "item", "section", "target", "doc", "change", "note", "status", "source"]
    out23.mkdir(parents=True, exist_ok=True)
    md = [f"# {CDC}", "", f"Decision: D-RCV-60. Date: {DATE}. Status: Draft (directive resolutions). Tool: {TOOL}.", "",
          "Every change that a story fix needs in another document. The directive run did not edit those documents "
          "(the cross-document pass was stopped), so each row is pending for the owner of the target document. "
          "Gap Register v2 status 'change listed in the Cross-document Change Register v1' points here.", "",
          f"Rows: {len(cdc)}.", ""]
    md += table(hdr, [[r[k] for k in keys] for r in cdc])
    (out23 / f"{CDC}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    rm = wb.active
    rm.title = "Read me"
    for line in md[:7]:
        rm.append([line])
    ws = wb.create_sheet("Changes")
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in cdc:
        ws.append([r[k] for k in keys])
    ws.auto_filter.ref = ws.dimensions
    ws.freeze_panes = "A2"
    wb.save(out23 / f"{CDC}.xlsx")
    cdc_by = defaultdict(list)
    for r in cdc:
        cdc_by[r["service"]].append(r)

    # ---- packs
    pk = out23 / PACKS
    services = sorted(set(svc_of.values())) + [NOSTORY]
    by_svc = defaultdict(list)
    for s in stories:
        by_svc[svc_of[s]].append(s)
    deferred = [(rid, r, [x for x in re.split(r"[,;]\s*", str(r.get("Story") or "")) if x in svc_of])
                for rid, r in rul.items() if r.get("Decision") == "Deferred"]
    index = []
    LIMIT = 150 * 1024

    def render(svc, ss, label=""):
        sset = set(ss)
        cdc_rows = [r for r in cdc_by.get(svc, []) if svc == NOSTORY or r["story"] in sset]
        svc_items = set()
        for s in ss:
            svc_items |= {str(rul[r]["Item ID"]) for r in disp[s] if r in rul}
        if svc == NOSTORY:
            svc_items = {i for i in list(gaps2) + list(asm2) if not item_stories.get(i)}
        biz, notapp, resolved = [], [], []
        counts = Counter()
        for s in ss:
            for rid, d in sorted(disp[s].items()):
                counts[d["status"]] += 1
                r = rul.get(rid, {})
                row = [s, rid, d.get("item", ""), d.get("section", ""), r.get("Title", "")]
                if d["status"] == "Not applied":
                    notapp.append(row + [d.get("note", "") or d.get("change", "")])
                elif d["status"] == "Resolved":
                    resolved.append(row + [d.get("change", "") or d.get("note", "")])
        # business decisions: deferred rulings of these stories (they have no disposition)
        for rid, r, st in deferred:
            if (svc == NOSTORY and not st) or (svc != NOSTORY and any(x in sset for x in st)):
                biz.append([", ".join(st) or "-", rid, r["Item ID"], r.get("Kind", ""), r.get("Owner role", ""),
                            r.get("Title", ""), r.get("Proposed fix", "")])
        gap_rows = [[g, gaps2[g].get("Title", ""), gaps2[g].get("Owner role", ""), gaps2[g].get("Status", "")]
                    for g in sorted(svc_items) if g in gaps2]
        asm_rows = [[x, asm2[x].get("Title", "") or asm2[x].get("Assumption", ""), asm2[x].get("Status", "")]
                    for x in sorted(svc_items) if x in asm2 and "Unconfirmed" in str(asm2[x].get("Status", ""))]
        L = [f"# {svc} - review pack{label}", "",
             f"Decision: D-RCV-60. Date: {DATE}. Status: Draft (directive resolutions). Tool: {TOOL}.", "",
             "Directive run result for this service: every gap and assumption was resolved with the recommended "
             "resolution, except business decisions. Review this pack, then the staged story files it lists. "
             "Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.", "",
             "## 1. Summary", ""]
        L += table(["Measure", "Count"], [["Stories", len(ss)], ["Resolved in the stories", counts["Resolved"]],
                                          ["Cross-document (pending in another document)", len(cdc_rows)],
                                          ["Not applied (value not in the sources)", len(notapp)],
                                          ["Open business decisions", len(biz)], ["Register gaps linked", len(gap_rows)],
                                          ["Unconfirmed assumptions", len(asm_rows)],
                                          ["Lint findings", sum(len(lint[s]) for s in ss)]])
        if ss:
            L += ["", "## 2. Stories (staged next version)", ""]
            L += table(["Story", "Resolved", "Cross-document", "Not applied", "File"],
                       [[s, sum(d["status"] == "Resolved" for d in disp[s].values()),
                         sum(d["status"] == "Cross-document" for d in disp[s].values()),
                         sum(d["status"] == "Not applied" for d in disp[s].values()), staged_of[s]] for s in ss])
        L += ["", "## 3. Open business decisions (not resolved; owner decides)", ""]
        L += table(["Story", "Ruling", "Item", "Kind", "Owner role", "Title", "Proposed resolution"], biz) if biz else ["None."]
        L += ["", "## 4. Not applied (the value is not in the source documents)", ""]
        L += table(["Story", "Ruling", "Item", "Section", "Title", "Reason"], notapp) if notapp else ["None."]
        L += ["", "## 5. Cross-document changes (pending in the target document)", ""]
        grp = defaultdict(list)
        for r in cdc_rows:
            grp[r["doc"] or "(target not named)"].append(r)
        if not grp:
            L += ["None."]
        for doc, rs in sorted(grp.items(), key=lambda x: -len(x[1])):
            L += ["", f"### {doc} ({len(rs)})", ""]
            L += table(["CDC ID", "Story", "Item", "Section", "Change"],
                       [[r["id"], r["story"], r["item"], r["section"], r["change"] or r["note"]] for r in rs])
        L += ["", "## 6. Register gaps linked to this service (Gap Register v2 status)", ""]
        L += table(["GAP ID", "Title", "Owner role", "Status"], gap_rows) if gap_rows else ["None."]
        L += ["", "## 7. Unconfirmed assumptions (tied to a business decision)", ""]
        L += table(["ASM ID", "Assumption", "Status"], asm_rows) if asm_rows else ["None."]
        L += ["", "## 8. Lint findings on the staged stories", ""]
        lr = [[x["story"], x["check"], x["line"], x["detail"]] for s in ss for x in lint[s]]
        L += table(["Story", "Check", "Line", "Detail"], lr) if lr else ["None."]
        R = ([f"# {svc} - resolved items{label}", "", f"Decision: D-RCV-60. Date: {DATE}. Tool: {TOOL}.", "",
              "Every item resolved inside these stories, to spot-check the fixes against the staged files.", ""]
             + table(["Story", "Ruling", "Item", "Section", "Title", "Change made"], resolved)) if resolved else None
        stats = [len(ss), counts["Resolved"], len(cdc_rows), len(notapp), len(biz), sum(len(lint[s]) for s in ss)]
        return L, R, stats

    for svc in services:
        ss = by_svc.get(svc, [])
        name = svc.split(" ")[0]
        folder = pk / svc
        folder.mkdir(parents=True, exist_ok=True)
        L, R, st = render(svc, ss)
        groups = [ss]
        if len("\n".join(L).encode()) > LIMIT and len(ss) > 1:
            per = {s: len("\n".join(render(svc, [s])[0]).encode()) for s in ss}
            groups, cur, size = [], [], 0
            for s in ss:
                if cur and size + per[s] > LIMIT:
                    groups.append(cur); cur, size = [], 0
                cur.append(s); size += per[s]
            groups.append(cur)
        n = len(groups)
        for k, g in enumerate(groups, 1):
            tag = f" part {k} of {n}" if n > 1 else ""
            label = f", part {k} of {n} ({g[0]} to {g[-1]})" if n > 1 else ""
            L, R, st = render(svc, g, label)
            f = folder / f"{name} - review pack{tag}.md"
            f.write_text("\n".join(L) + "\n", encoding="utf-8")
            if R:
                (folder / f"{name} - resolved items{tag}.md").write_text("\n".join(R) + "\n", encoding="utf-8")
            index.append([svc + (f" (part {k} of {n})" if n > 1 else "")] + st + [f"{f.stat().st_size // 1024} KB"])
            print(index[-1], flush=True)
    RM = [f"# {PACKS}", "", f"Decision: D-RCV-60. Date: {DATE}. Status: Draft (directive resolutions). Tool: {TOOL}.", "",
          "One folder per service. Run the reviewer prompt on one service at a time: give it the service's review "
          "pack, its resolved-items file and the staged story files listed in section 2 of the pack, together with "
          "the documents the stories cite. Fix the findings in the next version of the files, then move on.", "",
          "Master records: Gap Register v2, Assumptions Register v2 and Cross-document Change Register v1 "
          "(23 Document Gaps).", ""]
    RM += table(["Service", "Stories", "Resolved", "Cross-document", "Not applied", "Business decisions", "Lint",
                 "Pack size"], index)
    RM += ["", "A service with a large pack is split into parts by story; review the parts one prompt at a time."]
    (pk / "README.md").write_text("\n".join(RM) + "\n", encoding="utf-8")
    print(f"CDC rows {len(cdc)}; packs {len(index)}")


if __name__ == "__main__":
    main()
