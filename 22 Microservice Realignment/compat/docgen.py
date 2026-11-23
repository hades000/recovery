"""Run documents for D-RCV-53. Never overwrites: v1 files are kept if present; the Tracker gets a new version each call."""
import argparse, collections, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, R23, WORK, SERVICES, OWNER, header, next_version, read_json, read_jsonl, decision

PLAN = ROOT / "2026-11-22-recovery-microservice-realignment-implementation-plan.md"
DEC = decision()
TOOL = f"Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision {DEC}."
REASON = {
    "RWB-E1-014": "Decision log copy to the data lake. Arch v5 has no data lake (ADR-018); reporting reads events into the rwb-reporting read model.",
    "RWB-TE-007": "Quartz scheduler. Retired by Arch v5; Temporal Schedules through the workflow kit replace it (RWB-PLT-E1071-CON, ADR-016).",
    "RWB-E1-001": ("In build: creates the single recovery schema (92 tables, 14 data products, dictionary). Arch v5 needs one rwb_<name> schema per "
                   "service. The built migration is kept unchanged; the split is new work in RWB-PLT-NF06-DB and the per-service DB stories, "
                   "and each table moves to its owner schema by the Ownership Map. Only change if absolutely needed (U2)."),
}
DISP_TEXT = {
    f"Retired ({DEC})": "Retired by the realignment.",
    "Already retired": "Already cancelled before the realignment; no new story.",
    "Preserved + delta": "Built or in build. As-built story kept word for word; the microservice change is a separate delta story.",
    "Must change": "In build and must change to fit Arch v5.",
    "Moved (no impact)": "Moved to its service epic; content unchanged.",
    "Split (rework)": "Split into linked stories by service and team type.",
    "New": "New story created by the realignment.",
}
# Only the impact file written by jira() may name the issue tracker (check C13); the Template and Rules must not.
TPL_FIX = ("- Jira Impact and Follow-up v1", "- Issue-tracker impact and follow-up v1")

def blocks(text, name):
    found = re.findall(r"<!-- " + re.escape(name) + r"-BEGIN -->\n(.*?)<!-- " + re.escape(name) + r"-END -->", text, re.S)
    if not found:
        raise SystemExit(f"markers {name} not found")
    return "\n".join(b.strip() + "\n" for b in found)

def _write_once(path, text):
    if path.exists():
        print("KEPT", path.name); return path
    path.write_text(text, encoding="utf-8"); print("WROTE", path.name); return path

def template():
    body = blocks(PLAN.read_text(encoding="utf-8"), "R-TEMPLATE").replace(*TPL_FIX).replace("D-RCV-53", DEC)
    return _write_once(R22 / "Recovery Workbench Microservice Story Template and Rules v1.md",
                       f"# Recovery Workbench Microservice Story Template and Rules v1\n\n{header()}\n{TOOL}\n\n{body}")

def _plan():
    return read_json(WORK / "plan" / "split_plan.json"), {r["key"]: r for r in read_json(WORK / "plan" / "legacy_index.json")}

def change_register():
    plan, idx = _plan(); s = {x["id"]: x for x in plan["slices"]}
    lines = [f"# Recovery Workbench Microservice Change Register v1\n\n{header()}\n{TOOL}\n",
             "One row per legacy story. Built and in-build Epic 1 work is not changed unless absolutely needed (U2).\n",
             "## Summary\n", "| Disposition | Legacy stories | Meaning |", "|---|---|---|"]
    cnt = collections.Counter(v["disposition"] for v in plan["legacy"].values())
    lines += [f"| {d} | {n} | {DISP_TEXT.get(d, '')} |" for d, n in sorted(cnt.items())]
    lines += ["\n## Stories\n", "| Legacy key | Title | Disposition | Build status | New stories | Reason |", "|---|---|---|---|---|---|"]
    for k, v in sorted(plan["legacy"].items()):
        title = idx.get(k, {}).get("title") or (s[v["slices"][0]]["title"] if v["slices"] else "")
        bs = s[v["slices"][0]]["build_status"] if v["slices"] else ("Built" if k in REASON else "Not started")
        lines.append(f"| {k} | {title.replace('|', '/')} | {v['disposition']} | {bs} | {', '.join(v['slices']) or 'None'} | "
                     f"{REASON.get(k, DISP_TEXT.get(v['disposition'], ''))} |")
    return _write_once(R22 / "Recovery Workbench Microservice Change Register v1.md", "\n".join(lines) + "\n")

def jira_rows(legacy):
    rows = []
    for k, v in sorted(legacy.items()):
        d, n = v["disposition"], len(v["slices"])
        if d.startswith("Retired"):
            act, new = f"Close the issue as won't do (retired by {DEC}); no new issues", 0
        elif d == "Already retired":
            act, new = "No change (already cancelled)", 0
        elif d in ("Preserved + delta", "Must change"):
            act, new = "Keep the issue and its status; link the new delta and contract issues", max(0, n - 1)
        elif d == "Moved (no impact)":
            act, new = "Keep the issue; change its epic link to the service epic", max(0, n - 1)
        elif d == "New":
            act, new = "Create the issue in its service, platform or integration epic", n
        else:
            act, new = "Keep the issue as the main APP story; create the linked split issues; move it to the service epic", max(0, n - 1)
        rows.append([k, d, act, new, ", ".join(v["slices"])])
    return rows

def jira():
    plan, _ = _plan(); rows = jira_rows(plan["legacy"])
    body = blocks(PLAN.read_text(encoding="utf-8"), "R-JIRA").replace("D-RCV-53", DEC)
    epics = collections.Counter(x["epic"] for x in plan["slices"])
    scale = collections.Counter(r[1] for r in rows); new_total = sum(r[3] for r in rows)
    t = [f"# Recovery Workbench Jira Impact and Follow-up v1\n\n{header()}\n{TOOL}\n", body,
         "\n## Scale\n", f"- Epics to create: {len(epics)} (7 platform, 19 service, 5 integration).",
         f"- Issues to create: {new_total}. Issues to close: {scale.get(f'Retired ({DEC})', 0)}.", "",
         "| Disposition | Legacy issues |", "|---|---|"] + [f"| {d} | {n} |" for d, n in sorted(scale.items())]
    t += ["\n## Epics\n", "| Epic | Stories |", "|---|---|"] + [f"| {e} | {n} |" for e, n in sorted(epics.items())]
    t += ["\n## Per legacy issue\n", "| Legacy key | Disposition | Follow-up action | New issues | New story IDs |", "|---|---|---|---|---|"]
    t += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
    return _write_once(R22 / "Recovery Workbench Jira Impact and Follow-up v1.md", "\n".join(t) + "\n")

def tracker():
    from xlsx_write import write_book
    plan, idx = _plan(); docs = read_json(WORK / "plan" / "docs.json", []) or []
    ids = read_json(WORK / "plan" / "ids.json", {}) or {}; own = read_json(WORK / "plan" / "ownership.json", {}) or {}
    st = read_json(WORK / "status.json", {}) or {}
    logs = sorted((WORK / "editlog").glob("*.md"))
    defects = read_jsonl(WORK / "plan" / "defects.jsonl")
    sheets = {
        "Documents": (["Track", "Source", "Output", "Change"], [[d["track"], d["source"], d["output"], d["note"]] for d in docs]),
        "Stories": (["Story", "Title", "Work type", "Epic", "Lane", "Ready", "Suggested owner", "Wave", "Business epic", "Legacy", "File"],
                    [[x["id"], x["title"], x["wt"], x["epic"], x.get("lane"), x["ready"], OWNER[x["owner"]], x["wave"], x["business_epic"], x["legacy"], x["file"]] for x in plan["slices"]]),
        "Story split": (["Legacy key", "Title", "Disposition", "New stories"], [[k, idx.get(k, {}).get("title", ""), v["disposition"], v["slices"]] for k, v in sorted(plan["legacy"].items())]),
        "Decisions": (["Item", "Value"], [["Realignment decision", ids.get("realignment_decision")], ["ADRs", ids.get("adrs")], ["Decision log rows", ids.get("dl")]]),
        "Rulings": (["Item", "Owner", "Ruling", "Assumption"], own.get("rulings", [])),
        "Defects": (["Defect", "Legacy story", "New story", "Note"], [[d.get("id"), d.get("legacy"), d.get("story"), d.get("note")] for d in defects]),
        "Edit log": (["WP", "File"], [[p.stem, str(p.relative_to(ROOT))] for p in logs]),
        "WP status": (["WP", "State", "Tries"], [[k, v.get("state"), v.get("tries")] for k, v in sorted(st.items())]),
    }
    n = next_version(R22, "Recovery Workbench Microservice Realignment Tracker")
    out = R22 / f"Recovery Workbench Microservice Realignment Tracker v{n}.xlsx"
    write_book(out, sheets, read_me=header() + f"\nRecovery Workbench Microservice Realignment Tracker v{n}\n{TOOL}\nStatus at generation time; regenerate for a new version.")
    print("WROTE", out.name); return out

def summary():
    plan, _ = _plan(); st = read_json(WORK / "status.json", {}) or {}; cap = read_json(WORK / "plan" / "capacity.json", {}) or {}
    states = collections.Counter(v.get("state") for v in st.values())
    rep = sorted((R22 / "checks" / "reports").glob("full-*.md"))
    gaps = sorted(R23.glob("Recovery Workbench Gap Register v*.md")); asms = sorted(R23.glob("Recovery Workbench Assumptions Register v*.md"))
    t = [f"# Recovery Workbench Realignment Run Summary v1\n\n{header()}\n{TOOL}\n",
         "## Capacity used\n", f"- Budget (live model sessions): {cap.get('budget')}; fanout per story WP: {cap.get('fanout')}; probe process max: {cap.get('process_max')}; subagents per session: {cap.get('session_subagent_max')}.",
         "\n## Work packages\n"] + [f"- {k}: {v}" for k, v in sorted(states.items(), key=lambda kv: str(kv[0]))]
    t += ["\n## Stories\n", f"- Stories: {plan['stats']['slices']}; legacy keys: {plan['stats']['legacy']}; Day-1 stories: {plan['stats']['day1']}; lanes: {plan['stats']['lanes']}.",
          f"- Team types with Day-1 work: {', '.join(plan['stats']['day1_teams'])}.",
          "\n## Registers\n", f"- Gap Register: {gaps[-1].name if gaps else 'not written'}", f"- Assumptions Register: {asms[-1].name if asms else 'not written'}",
          "\n## Checks\n", f"- Last full report: {rep[-1].name if rep else 'not run'}",
          "\n## Next\n", "- The verification loop is a separate, later activity (U8). This run made no human stops."]
    return _write_once(R22 / "Recovery Workbench Realignment Run Summary v1.md", "\n".join(t) + "\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["template", "change", "jira", "tracker", "summary", "a8"]); a = ap.parse_args()
    if a.cmd == "a8":
        template(); change_register(); jira(); tracker()
    else:
        {"template": template, "change": change_register, "jira": jira, "tracker": tracker, "summary": summary}[a.cmd]()
