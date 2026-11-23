"""Write every WP file and the queues. All WPs in a queue are independent (single-writer rule)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, SERVICES, STORIES, latest_path, versions, next_version, read_json, write_json, svc, decision

DEC = decision()

TPL = "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md"
OFFICE = "22 Microservice Realignment/compat/office_write.py"
CONVERT = "22 Microservice Realignment/compat/convert_sources.py"
V5 = "22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md"
TD = "22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md"
OWN = "_work/msr/plan/ownership.json"
HEADER = "Tool rules: AGENTS.md (root) rules 1-14. Agent: {agent}. fanout: {fanout}\n"
FINISH = ("Finish: run python -I \"22 Microservice Realignment/checks/run_all.py\" --wp {wp} --quick ; fix every failure ; "
          "write _work/msr/editlog/{wp}.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; "
          "reply with the list of files written.\n")
KEEP = ("id", "title", "wt", "epic", "service", "lane", "ready", "owner", "wave", "business_epic", "release", "legacy",
        "disposition", "build_status", "patterns", "H", "C", "I", "X", "acs", "tcs_legacy", "reqs", "preserved", "delta",
        "secondary", "new", "file", "source")

STORY_RULES = """Do, for each story line below (one JSON object per line), write exactly one file at its "file" path:
1. Use the template in Template and Rules v1 §R7: the 19 headings in order, the metadata table rows of §R7.1 in order (never remove a row).
   Copy these values exactly from the JSON: Story key=id, Work type, Suggested owner (fixed phrase for "owner"), Service, Service epic=epic,
   Wave, Business epic, Release (+ " (tentative)"; "None (new story)" when empty), Legacy key, Legacy disposition, Build status,
   Patterns applied, Parallel lane, Ready to start, Depends on (build)=H, Contract dependencies=C, Integration dependencies=I,
   External dependencies=X, PRD reference "Pending (C1)", Status "Draft (realignment v1)".
2. preserved=true: copy legacy §1-11, §14-16, §18 and §19 word for word; keep §12 and §13 under the heading "As built (monolith)".
3. delta=true: describe only the microservice change for that legacy key in Template and Rules §R6.
4. ACs: "acs" lists the legacy AC IDs this story owns. Copy each verbatim with the origin tag "(legacy <legacy> <AC>)".
   An APP AC whose cross-service part can be mocked gets the Given "Given the <service> contract mock returns <x>" (keep every value).
   CON, DB, INF, OPS and new stories: write ACs tagged "(new, D-RCV-53)" that test only the deliverable in the title. Never invent business values.
5. TCs: keep the legacy TC IDs of the ACs this story owns; an ITG copy of a TC gets the suffix -ITG. Add the Level column (§R7.2 s16).
6. Apply the DP table (§R5.5) for every pattern in "patterns"; list them in "Patterns applied".
7. Section 12 Contract: tables 12.1-12.9 (or None). Names: topic rwb.<short>.events.v1, event rwb.<short>.<Event>.v1, queue rwb-<short>,
   REST base /api/recovery/<short>/v1, schema rwb_<name>. Owners come from the Ownership Map only.
8. Write _work/msr/fragments/<id>.json with keys: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy,
   disposition, H, C, I, X, acs [{"id","origin","text_first_line"}], tcs, reqs, ops_provided, ops_consumed, events_published,
   events_consumed, workflows, prd_ref "Pending (C1)", gaps [CG ids], assumptions [ASM ids], file.
9. A missing value: "Not specified in the source documents (CG-{wp}-<n>; ASM-{wp}-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/{wp}.jsonl and _work/msr/assumptions/{wp}.jsonl.
"""

def _src_lines(sl):
    out = []
    for s in sl:
        src = s.get("source")
        if src and f"- {src} (heading {s['legacy']})" not in out:
            out.append(f"- {src} (heading {s['legacy']})")
    return out

def story_wps(plan, fanout=5):
    groups = {}
    for s in plan["slices"]:
        groups.setdefault(s["epic"], {}).setdefault(s["legacy"], []).append(s)
    wps = []
    for epic, by_leg in sorted(groups.items()):
        keys = sorted(by_leg, key=lambda k: (min(x.get("lane", "") for x in by_leg[k]), k))
        code = epic.replace("RWB-SVC-", "").replace("RWB-", "")
        for n in range(0, len(keys), 5):
            chunk = keys[n:n + 5]; sl = [s for k in chunk for s in by_leg[k]]
            wp = f"B-{code}-{n // 5 + 1:02d}"
            mod = sl[0].get("scope") if sl[0].get("scope") not in ("PLT", "ITG") else None
            reads = [f"- {TPL} (read fully first)", f"- {OWN}", f"- {V5}", f"- {TD}"] + _src_lines(sl)
            if mod:
                reads.append(f"- _work/msr/extract/ files of the FSD and TSD folders whose name contains \"{mod}\" (module {svc(mod)['name']})")
            reads.append("- Thin stories only: _work/msr/extract/Recovery Workbench Business Requirements Program v4.md, Epic 1 v4, Epic 2 v2, "
                         "Epics 3 to 8 Specification v3, Business Rules and Routing Logic (fill order Template and Rules §R7.3)")
            outs = [s["file"] for s in sl] + [f"_work/msr/fragments/{s['id']}.json" for s in sl]
            f = len(chunk) > 1
            text = (f"# WP {wp} — {epic}: legacy {', '.join(chunk)}\n" + HEADER.format(agent="aisdlc-msr-worker", fanout=fanout if f else 0)
                    + "Read only:\n" + "\n".join(reads) + "\nWrite only:\n" + "\n".join(f"- {o}" for o in outs)
                    + f"\n- _work/msr/gaps/{wp}.jsonl\n- _work/msr/assumptions/{wp}.jsonl\n- _work/msr/editlog/{wp}.md\n"
                    + STORY_RULES.replace("{wp}", wp) + "Stories:\n"
                    + "\n".join(json.dumps({k: s.get(k) for k in KEEP}, ensure_ascii=False) for s in sl) + "\n"
                    + (f"Parallel: give each legacy key to its own task subagent (aisdlc-msr-worker) in ONE message, up to {fanout} at once; "
                       "each subagent writes only that key's files and its own jsonl rows with ids CG-" + wp + "-<key>-<n>.\n" if f else "")
                    + FINISH.format(wp=wp))
            wps.append({"wp": wp, "keys": chunk, "text": text, "expect": outs + [f"_work/msr/editlog/{wp}.md"], "fanout": f,
                        "agent": "aisdlc-msr-worker"})
    return wps

DOCS = [  # track, folder, family stem, what changes (Appendix R8.6)
    ("TECH", "05 Technical architecture", "Recovery Workbench ACE Architecture Decision", "19 services inside ACE; supersedes the single-service decision"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Target Architecture", "v5 target: 19 services, Kafka, Temporal layer, edge, no data lake"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Technical Specifications by Module", "add a T0 Service section per module; rewrite T5.2 as contracts"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Interface Specifications", "remove INT-19 and INT-20 (no data lake); per-service owners"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Environment and Deployment Design", "per-service deployments; environment names are a gap"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Workflow Engine Design", "workflow kit, child workflow per stage, Schedules"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Rules Engine Design", "embedded Drools per service; registry in rwb-decision"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Security and Access Design", "login per service, workload identity, authorise contract"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Observability and Monitoring Design", "per-service dashboards and alerts"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Error Handling and Resilience Standard", "2 s timeout, one REST hop, retry and .dlt rules"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Availability Performance and Recovery Design", "per-service targets; RPO and RTO are a gap"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Audit and Logging Design", "local decision record plus central ledger"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Document Management Design", "owned by rwb-document"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Notification and Correspondence Design", "owned by rwb-comms"),
    ("TECH", "05 Technical architecture", "Recovery Workbench Information Flow", "flows between the 19 services"),
    ("TECH", "05 Technical architecture", "Recovery Workbench System Disposition and Integration Inventory", "add Service column"),
    ("DATA", "06 Data", "Recovery Workbench Conceptual Data Model", "add owning service per entity"),
    ("DATA", "06 Data", "Recovery Workbench Source to Target Mapping", "target schema rwb_<name>"),
    ("DATA", "06 Data", "Recovery Workbench Reference Data and Lists of Values", "refdata starter; shared lists via rwb-case"),
    ("DATA", "06 Data", "Recovery Workbench Data Ownership and Stewardship", "owner service per data set"),
    ("DATA", "06 Data", "Recovery Workbench Data Migration Approach", "migration per schema"),
    ("DATA", "06 Data", "Recovery Workbench Party and Customer Master Data Design", "read only through rwb-source-data"),
    ("DATA", "06 Data", "Recovery Workbench Reporting and Analytics Data Model", "no data lake; rwb-reporting read model from events"),
    ("DATA", "06 Data", "Recovery Workbench Data Classification and Personal Data Inventory", "no PII in events, workflow inputs or logs"),
    ("DATA", "06 Data", "Recovery Workbench Data Quality and Reconciliation Rules", "per-service reconciliation"),
    ("DATA", "06 Data", "Recovery Workbench Volume and Scale Forecast", "per-service volumes, topics and queues"),
    ("REQ-SPEC", "03 Requirements and specifications", "Recovery Workbench Functional Specifications by Module", "add only a Service line and a v5 note per module"),
    ("REQ-SPEC", "03 Requirements and specifications", "Recovery Workbench Non Functional Specification", "2 s timeout, one-hop REST; gaps for RPO/RTO and 'weeks vs 28 days'"),
    ("AI", "08 AI and agents", "Recovery Workbench AI and Agent Architecture", "rwb-agent service; AgentRunWorkflow child, 60 s fallback"),
    ("AI", "08 AI and agents", "Recovery Workbench Model Integration Design", "model calls only from rwb-agent activities"),
    ("AI", "08 AI and agents", "Recovery Workbench Agent Catalog and Specifications", "owning service per agent"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Controls Catalog", "control owner service"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Records Retention and Archiving", "retention per schema"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Personal Data Protection Design", "PII boundaries per service and in events"),
    ("CTRL", "10 Policy, controls and compliance", "Recovery Workbench Regulatory Requirements Map", "regulation to service"),
    ("BIZ", "02 Business architecture and process", "Recovery Workbench Feature List", "add Service and Service epic columns"),
    ("BIZ", "02 Business architecture and process", "Recovery Workbench Case and Workflow Model", "CaseWorkflow parent with child per stage"),
    ("BIZ", "02 Business architecture and process", "Recovery Workbench Users Roles and Permissions", "authorise contract of rwb-access"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Test Strategy", "contract tests, component tests with mocks, ITG per wave"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Non Functional Test Plan", "per-service and journey NFR tests"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Test Data Plan", "synthetic data per schema; contract mocks"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Definition of Ready and Done", "Ready = contract published; Done = contract and boundary tests green"),
    ("TESTDOC", "09 Testing and quality", "Recovery Workbench Integration Test Plan", "NEW v1: ITG-W1..W4 and NFR epics, harness RWB-ITG-W1J01-ITG"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Engineering Practices", "repo per service, contract-first, per-service Flyway"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Release Plan", "waves within the 8-month horizon; dates unchanged and tentative"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Cutover and Go Live Plan", "cutover per wave"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Run Operating Model", "run book per service"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Risks Assumptions Issues and Dependencies", "add realignment risks R1-R9; point to the Assumptions Register"),
    ("DELIVDOC", "11 Delivery and operations", "Recovery Workbench Resource Plan and Team Structure", "suggested ownership by team type; no names"),
]
ARCH = [  # wp, title, sources (folder, stem), outputs (folder, stem, ext or 'dir' or 'new:<name>'), note
    ("B-ARCH-ADR", "ADR v-next with ADR-013..023", [("05 Technical architecture", "Recovery Workbench Architecture Decision Records")],
     [("05 Technical architecture", "Recovery Workbench Architecture Decision Records", ".md")], "Appendix R §R8.4 row ADR"),
    ("B-ARCH-DL", "Decision Log v-next", [("01 Decisions and governance", "Recovery Workbench Decision Log")],
     [("01 Decisions and governance", "Recovery Workbench Decision Log", ".xlsx")], "add D-RCV-53 and DL44-49; mark D-RCV-36 T1 and T2 amended"),
    ("B-ARCH-SVC", "Service Catalog v1 and Service Template Specification v1", [],
     [("05 Technical architecture", "Recovery Workbench Service Catalog", ".md"), ("05 Technical architecture", "Recovery Workbench Service Catalog", ".xlsx"),
      ("05 Technical architecture", "Recovery Workbench Service Template Specification", ".md")], "19 services, resources per service, template"),
    ("B-ARCH-API", "API Specification folder v-next split into 19 files", [("05 Technical architecture", "Recovery Workbench API Specification")],
     [("05 Technical architecture", "Recovery Workbench API Specification", "dir")], "split by x-module + ownership.json api; each operation in exactly one file; gateway-bff and index; asyncapi/"),
    ("B-ARCH-EVT", "Event and Messaging v-next and Kafka Topic and Event Catalog v1", [("05 Technical architecture", "Recovery Workbench Event and Messaging Design")],
     [("05 Technical architecture", "Recovery Workbench Event and Messaging Design", None), ("05 Technical architecture", "Recovery Workbench Kafka Topic and Event Catalog", ".xlsx")], "19 topics + rwb.decision-record.v1, .dlt, outbox/inbox, CloudEvents"),
    ("B-ARCH-WF", "Batch and Scheduling v-next and Temporal Workflow and Activity Catalog v1", [("05 Technical architecture", "Recovery Workbench Batch and Scheduling Design")],
     [("05 Technical architecture", "Recovery Workbench Batch and Scheduling Design", None), ("05 Technical architecture", "Recovery Workbench Temporal Workflow and Activity Catalog", ".xlsx")], "Quartz retired; each JOB to a Schedule or event-started workflow (ownership.json jobs)"),
    ("B-ARCH-DB", "Physical Schema folder v-next, LDM v-next, ERD v-next", [("06 Data", "Recovery Workbench Physical Schema"), ("06 Data", "Recovery Workbench Logical Data Model and Data Dictionary"), ("06 Data", "Recovery Workbench Entity Relationship Diagram")],
     [("06 Data", "Recovery Workbench Physical Schema", "dir"), ("06 Data", "Recovery Workbench Logical Data Model and Data Dictionary", None), ("06 Data", "Recovery Workbench Entity Relationship Diagram", None)], "19 rwb_<name>.sql + recovery_views.sql + README; FK cuts from the Ownership Map sheet"),
    ("B-ARCH-CON", "Service Contract Catalog v1", [], [("05 Technical architecture", "Recovery Workbench Service Contract Catalog", ".md"), ("05 Technical architecture", "Recovery Workbench Service Contract Catalog", ".xlsx")], "from ownership.json; include the v5 slide 13 call-type matrix"),
]

def out_path(folder, stem, ext):
    d = ROOT / folder; n = next_version(d, stem)
    if ext == "dir":
        return f"{folder}/{stem} v{n}"
    if ext is None:
        lp = latest_path(d, stem)
        ext = lp.suffix if lp and lp.is_file() else ".md"
        if ext.lower() in (".pdf", ".html", ".htm"):
            ext = ".md"
    return f"{folder}/{stem} v{n}{ext}"

def src_path(folder, stem):
    lp = latest_path(ROOT / folder, stem)
    return str(lp.relative_to(ROOT)) if lp else None

DOC_RULES = """Do: produce the next version of each output. Keep every section, ID, number and date of the source; release dates get "(tentative)".
Change only what the realignment needs: {note}. Use the Ownership Map for every owner. New decisions use the IDs in _work/msr/plan/ids.json.
First two lines are the header in Template and Rules §R8.1. Add a change-log row "<version>, 22 November 2026, D-RCV-53 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash".
How to write each format (never edit the source):
- .md: write the new file directly.
- .docx: write the full text to _work/msr/docs/{wp}/<name>.md, then: python -I "{office}" md-docx "<that md>" "<output .docx>" --template "<source .docx>"
- .xlsx: python -I "{office}" copy "<source>" "<output>" ; then add sheets/rows with: python -I "{office}" xlsx-append "<output>" "<sheet>" "<rows.json>"
- .pptx: python -I "{office}" copy "<source>" "<output>" ; then python -I "{office}" pptx-append "<output>" "<slides.md>"
- folder family: python -I "{office}" copy "<source folder>" "<output folder>" ; then for each file that changes, write its next version inside the new folder.
Never invent values: placeholders and jsonl rows as Template and Rules §R9.
"""

def doc_wp(wp, title, srcs, outs, note, agent="aisdlc-msr-worker"):
    reads = [f"- {s}" for s in srcs if s] + [f"- converted text under _work/msr/extract/ (or convert with: python -I \"{CONVERT}\" <file> _work/msr/extract/{wp})",
             f"- {TPL} (§R1, §R3, §R5, §R8, §R9)", f"- {OWN} and 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
             f"- {V5}", f"- {TD}", "- _work/msr/plan/split_plan.json (\"stats\" and \"legacy\" only)", "- _work/msr/plan/ids.json"]
    text = (f"# WP {wp} — {title}\n" + HEADER.format(agent=agent, fanout=0) + "Read only:\n" + "\n".join(reads)
            + "\nWrite only:\n" + "\n".join(f"- {o}" for o in outs)
            + f"\n- _work/msr/docs/{wp}/ (scratch)\n- _work/msr/gaps/{wp}.jsonl\n- _work/msr/assumptions/{wp}.jsonl\n- _work/msr/editlog/{wp}.md\n"
            + DOC_RULES.format(note=note, wp=wp, office=OFFICE) + FINISH.format(wp=wp))
    return {"wp": wp, "text": text, "expect": list(outs) + [f"_work/msr/editlog/{wp}.md"], "fanout": False, "agent": agent}

def req_wps():
    f3 = "03 Requirements and specifications"; out = []
    rt = read_json(WORK / "plan" / "runtime.json", {}) or {}
    brd_agent = "aisdlc-msr-worker" if rt.get("brd_fallback") else "aisdlc-brd-builder"
    prd_agent = "aisdlc-msr-worker" if rt.get("brd_fallback") else "aisdlc-prd-builder"
    for key, stem in [("PROG", "Recovery Workbench Business Requirements Program"), ("E1", "Recovery Workbench Business Requirements Epic 1"),
                      ("E2", "Recovery Workbench Business Requirements Epic 2")]:
        md = out_path(f3, stem, ".md"); docxp = md[:-3] + ".docx"
        out.append(doc_wp(f"B-REQ-BRD-{key}", f"{stem} next version (BRD Builder)", [src_path(f3, stem), "22 Microservice Realignment/aisdlc/docs/brds/"],
                          [md, docxp], "BR IDs stable, business content unchanged; add a section 'Delivery model' (19 service epics, waves, contract-first) and a BR -> service epic -> business epic trace table", brd_agent))
    stem = "Recovery Workbench Business Requirements Epics 3 to 8"
    out.append(doc_wp("B-REQ-BRD-E38", "New BRD Epics 3 to 8 v1 (BRD Builder)", [src_path(f3, "Recovery Workbench Epics 3 to 8 Specification"),
                      "17 AI-First SDLC Repository v2/docs/prds/epics-3-to-8-specification.md", "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"],
                      [f"{f3}/{stem} v1.md", f"{f3}/{stem} v1.docx"], "fill business gaps of the thin stories; every missing value becomes a Q- item (-> gap row) and an ASM- item (-> assumption row)", brd_agent))
    for s in SERVICES + [{"code": "PLT", "service": "Platform", "name": "Platform"}]:
        name = f"Recovery Workbench PRD {s['code']} {s['service']} v1.md" if s["code"] != "PLT" else "Recovery Workbench PRD PLT Platform v1.md"
        out.append(doc_wp(f"B-REQ-PRD-{s['code']}", f"PRD {s['code']} {s['service']} v1 (PRD Builder)",
                          ["03 Requirements and specifications BRDs (latest versions) and their converted text in _work/msr/extract/",
                           f"FSD v6 file for module {s['code']} in _work/msr/extract/", f"Arch v5 slides for {s['service']}"],
                          [f"{f3}/PRD/{name}"], f"PRD for {s['service']}: CAP-/FR-/NFR-/AC- IDs, FR-{s['code']}-nnn mapped to the FSD REQ IDs, release slicing by wave, no design beyond confirmed v5 constraints, status Draft, empty approval table", prd_agent))
    return out

def main():
    plan = read_json(WORK / "plan" / "split_plan.json"); cap = read_json(WORK / "plan" / "capacity.json", {}) or {}
    fan = cap.get("fanout", 5)
    q = {"A10": [], "B": [], "C": [], "D": []}
    for w in story_wps(plan, fan):
        q["B"].append(w)
    q["B"] += req_wps()
    for wp, title, srcs, outs, note in ARCH:
        q["B"].append(doc_wp(wp, title, [src_path(f, s) for f, s in srcs], [out_path(f, s, e) for f, s, e in outs], note))
    docs = []
    for i, (track, folder, stem, note) in enumerate(DOCS, 1):
        src = src_path(folder, stem); out = out_path(folder, stem, None if src else ".docx")
        if src and (ROOT / src).is_dir():
            out = out_path(folder, stem, "dir")
        docs.append({"track": track, "source": src, "output": out, "note": note})
        q["B"].append(doc_wp(f"B-{track}-{i:02d}", f"{stem} next version", [src], [out], note))
    write_json(WORK / "plan" / "docs.json", docs)
    q["A10"].append(doc_wp("A10-CTX", "Update AI-SDLC workspace contexts to Arch v5 (context-updater)",
                           ["22 Microservice Realignment/aisdlc/.github/contexts/"], ["22 Microservice Realignment/aisdlc/.github/contexts/realignment-v5-context.md"],
                           "write the new context file realignment-v5-context.md and add it to context-manifest.json copy in the workspace only (the workspace is a copy, so editing its files is allowed)", "aisdlc-context-updater"))
    f4, f9, f11 = "04 User stories", "09 Testing and quality", "11 Delivery and operations"
    cat = f"{f4}/Recovery Workbench Service Story Catalog v1.xlsx"
    c_items = [
        ("C2-RTM", "RTM next version (Traceability Manager)", [src_path(f9, "Recovery Workbench Requirements Traceability Matrix"), cat], [out_path(f9, "Recovery Workbench Requirements Traceability Matrix", ".xlsx")], "all 235 requirements -> legacy key -> new story IDs -> PRD FR IDs (fragments)", "aisdlc-traceability-manager"),
        ("C3-TC", "Test Cases next version and Regression Suite next version (QA Test Case Generator)", [src_path(f9, "Recovery Workbench Test Cases"), src_path(f9, "Recovery Workbench Regression Suite"), cat], [out_path(f9, "Recovery Workbench Test Cases", ".xlsx"), out_path(f9, "Recovery Workbench Regression Suite", ".xlsx")], "add Story, Service, Level columns; -ITG copies; draft TCs only for slices with no legacy TC, tagged (new, D-RCV-53)", "aisdlc-qa-test-case-generator"),
        ("C4-BSEQ", "Build Sequence next version", [src_path(f11, "Recovery Workbench Build Sequence Epic 1 and Epic 2"), cat], [out_path(f11, "Recovery Workbench Build Sequence Epic 1 and Epic 2", None)], "by service and lane; Day 1 first", "aisdlc-msr-worker"),
        ("C4-SBO", "Story Build Order next version", [src_path(f11, "Recovery Workbench Story Build Order"), cat], [out_path(f11, "Recovery Workbench Story Build Order", None)], "lanes and Ready to start", "aisdlc-msr-worker"),
        ("C4-DEP", "Dependency Map next version", [src_path(f11, "Recovery Workbench Dependency Map"), cat], [out_path(f11, "Recovery Workbench Dependency Map", None)], "H/C/I/X classes", "aisdlc-msr-worker"),
        ("C-EPICS", "Service Epics v1", [cat], [f"{f4}/Recovery Workbench Service Epics v1.md"], "31 epics: scope, wave, suggested owner, lanes, Day-1 stories", "aisdlc-technical-documenter"),
        ("C-DEF", "Story Defects next version", [src_path(f4, "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers"), cat], [out_path(f4, "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers", ".xlsx")], "map each open defect to the new story IDs", "aisdlc-msr-worker"),
        ("C-WEX", "Worked Example next version (E1-018)", [src_path(f4, "Recovery Workbench User Story Worked Example"), cat], [out_path(f4, "Recovery Workbench User Story Worked Example", ".md")], "use Template and Rules §R7.3", "aisdlc-msr-worker"),
        ("C-ACG", "Acceptance Criteria Glossary next version", [src_path(f4, "Recovery Workbench Acceptance Criteria Glossary")], [out_path(f4, "Recovery Workbench Acceptance Criteria Glossary", ".xlsx")], "add origin tag, contract mock Given, -ITG", "aisdlc-msr-worker"),
        ("C-HTR", "How To Read The Acceptance Criteria next version", [src_path(f4, "Recovery Workbench How To Read The Acceptance Criteria")], [out_path(f4, "Recovery Workbench How To Read The Acceptance Criteria", ".docx")], "explain slices and origin tags", "aisdlc-msr-worker"),
        ("C-BN1", "Build Notes Epic 1 next version", [src_path(f4, "Recovery Workbench Build Notes Epic 1"), cat], [out_path(f4, "Recovery Workbench Build Notes Epic 1", ".md")], "per service and lane", "aisdlc-msr-worker"),
        ("C-BN2", "Build Notes Epic 2 next version", [src_path(f4, "Recovery Workbench Build Notes Epic 2"), cat], [out_path(f4, "Recovery Workbench Build Notes Epic 2", ".md")], "per service and lane", "aisdlc-msr-worker"),
        ("C-BNT", "Build Notes Technical Enablers next version", [src_path(f4, "Recovery Workbench Build Notes Technical Enablers"), cat], [out_path(f4, "Recovery Workbench Build Notes Technical Enablers", ".md")], "PLT epics", "aisdlc-msr-worker"),
    ]
    for wp, title, srcs, outs, note, agent in c_items:
        q["C"].append(doc_wp(wp, title, srcs, outs, note, agent))
    f12 = "12 Project communication"
    for wp, stem, note in [("D2-IDX", "Recovery Workbench Document Index", "new sections 'Microservice realignment' and 'Document gaps'; list every new file from all edit logs"),
                           ("D2-CTL", "Recovery Workbench Document Control Sheet", "one row per new file, label 'Document set v15'"),
                           ("D2-HUB", "Recovery Workbench Project Hub", "links to the new files; label 'Document set v15'"),
                           ("D2-TSP", "Recovery Workbench Team Start Pack", "Day-1 Work Allocation per team type; no names"),
                           ("D2-CTO", "Recovery Workbench Executive Presentation CTO", "diagram-led slides: services, waves, Day-1, gaps"),
                           ("D2-OVR", "Recovery Workbench Project Overview", "realignment summary")]:
        q["D"].append(doc_wp(wp, f"{stem} next version", [src_path(f12, stem), "_work/msr/editlog/"], [out_path(f12, stem, None)], note))
    for name, items in q.items():
        out = []
        for w in items:
            w["text"] = w["text"].replace("D-RCV-53", DEC)
            p = WORK / "wp" / f"{w['wp']}.md"; p.write_text(w["text"], encoding="utf-8")
            out.append({"wp": w["wp"], "agent": w["agent"], "file": str(p.relative_to(ROOT)), "fanout": w["fanout"], "expect": w["expect"]})
        write_json(WORK / "wp" / f"queue-{name}.json", out)
    print("A7b OK", {k: len(v) for k, v in q.items()})

if __name__ == "__main__":
    main()
