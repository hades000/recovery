"""Build '04 User stories/Recovery Workbench Service Epics v1.md' for WP C-EPICS (D-RCV-60).

Reads: the Service Story Catalog v1.xlsx (Epics, Stories sheets), the Microservice Ownership Map v1.xlsx
(Services, Workflows sheets), _work/msr/plan/ownership.json, the Arch v5 text extract.
Writes: the Service Epics v1.md only.
"""
import collections
import json
import re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[4]
CAT = ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx"
MAP = ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx"
ARCH = ROOT / "22 Microservice Realignment" / "Recovery Workbench Architecture v5 Text Extract v1.md"
OWN = ROOT / "_work" / "msr" / "plan" / "ownership.json"
OUT = ROOT / "04 User stories" / "Recovery Workbench Service Epics v1.md"

DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
HEAD = ("SCB Collections and Recovery. Henka Group, 22 November 2026.\n"
        "(C) Siam Commercial Bank and Henka Pte Ltd")

SHORT = {
    "TechX (suggested; any team may pick up this story)": "TechX",
    "ACE team (suggested; any team may pick up this story)": "ACE team",
    "SCB IT infrastructure (suggested; any team may pick up this story)": "SCB IT infrastructure",
    "DevOps team (suggested; any team may pick up this story)": "DevOps team",
    "QA team (suggested; any team may pick up this story)": "QA team",
}
WT_NAME = {"CON": "Contract", "APP": "App development", "DB": "ACE DB", "INF": "Infrastructure",
           "OPS": "DevOps", "ITG": "Integration"}
WT_OWNER = {"CON": "TechX (suggested; any team may pick up this story)",
            "APP": "TechX (suggested; any team may pick up this story)",
            "DB": "ACE team (suggested; any team may pick up this story)",
            "INF": "SCB IT infrastructure (suggested; any team may pick up this story)",
            "OPS": "DevOps team (suggested; any team may pick up this story)",
            "ITG": "TechX (suggested; any team may pick up this story)"}

# §R5.1 order: platform, then the 19 services in code order, then integration.
PLT_ORDER = ["RWB-PLT-TPL", "RWB-PLT-LIB", "RWB-PLT-WF", "RWB-PLT-DB", "RWB-PLT-EVT", "RWB-PLT-EDGE", "RWB-PLT-OBS"]
SVC_ORDER = (["RWB-SVC-P%d" % n for n in range(1, 11)] + ["RWB-SVC-S%d" % n for n in range(1, 10)])
ITG_ORDER = ["RWB-ITG-W1", "RWB-ITG-W2", "RWB-ITG-W3", "RWB-ITG-W4", "RWB-ITG-NFR"]

PLT_REF = {
    "RWB-PLT-TPL": "§R5.1 (service template and repositories); §R4 (schema, login, REST base, topic and epic naming per service); DP-15 (per-service Flyway sequence, H `RWB-PLT-E1044-CON`)",
    "RWB-PLT-LIB": "§R5.1 (shared libraries); DP-03 (decision record), DP-04 (embedded Drools), DP-06 (parameters), DP-07 (reference data), DP-08 (authorise guard), DP-09 (outbox and inbox), DP-14 (topic naming library)",
    "RWB-PLT-WF": "§R5.1 (Temporal workflow platform); §R4 (Temporal namespace `rwb-recovery`, task queue `rwb-<short>`); DP-10 (Quartz replacement, H `RWB-PLT-E1071-CON`); DP-12 (parent and child workflows)",
    "RWB-PLT-DB": "§R5.1 (ACE DB schemas and logins); §R4 (schema `rwb_<short with _>`, login per service); DP-01, DP-02 (own schema, own login); DP-15 (migration ownership)",
    "RWB-PLT-EVT": "§R5.1 (Kafka event platform); §R4 (topic `rwb.<short>.events.v1` with retry and `.dlt`, shared topic `rwb.decision-record.v1`); DP-09 (outbox and inbox, CloudEvents)",
    "RWB-PLT-EDGE": "§R5.1 (edge and gateway); §R4 (gateway-bff with the Redis session store, partner gateway in the DMZ); DP-13 (REST base), DP-19 (composite route, H `RWB-PLT-N001-CON`)",
    "RWB-PLT-OBS": "§R5.1 (observability); ADR-023 (observability per service), allocated in §R8.4",
}
PLT_KEY = {
    "RWB-PLT-TPL": "`RWB-PLT-E1044-CON` Database migrations versioned with parameterized schema names (DP-15)",
    "RWB-PLT-LIB": "`RWB-PLT-E1027-CON` Decision log writer v1 (DP-03) · `RWB-PLT-E1072-CON` Drools runtime and rule package store (DP-04) · `RWB-PLT-E1042-CON` Central configuration service and parameter catalog (DP-06) · `RWB-PLT-E1043-CON` Reference data service with versioned tables (DP-07) · `RWB-PLT-E1037-CON` Role to permission matrix as data and PDPA field masking by role (DP-08) · `RWB-PLT-TE006-CON` Outbox and retry for outbound work (DP-09) · `RWB-PLT-E1047-CON` Feature flags for module release with a removal date (DP-14) · `RWB-PLT-N009-CON` RFC 9457 problem and Idempotency-Key helpers - interface and fake",
    "RWB-PLT-WF": "`RWB-PLT-E1071-CON` Temporal worker and SDK in the recovery module (DP-10) · `RWB-PLT-N010-CON` Workflow kit templates - interface and fake",
    "RWB-PLT-DB": "`RWB-PLT-NF06-DB` Create the 19 rwb_* schemas and logins · `RWB-PLT-N011-DB` PgBouncer pools, migrator role and grant check",
    "RWB-PLT-EVT": "`RWB-PLT-N002-INF` Kafka topics, retry and dead-letter topics and ACLs · `RWB-PLT-N008-INF` Schema registry with BACKWARD compatibility · `RWB-PLT-N012-INF` Blob, Key Vault and MFT/SFTP standard resources",
    "RWB-PLT-EDGE": "`RWB-PLT-N001-CON` gateway-bff route contract (DP-19) · `RWB-PLT-N001-APP` gateway-bff routes and composite screens · `RWB-PLT-N006-INF` Redis session store for gateway-bff · `RWB-PLT-N007-INF` Partner gateway in the DMZ (FAPI 2.0)",
    "RWB-PLT-OBS": "`RWB-PLT-N005-OPS` Platform dashboards and alerts baseline · `RWB-PLT-E1056-OPS` Run books and monitoring for every Epic 1 Workbench job",
}


def esc(s):
    return str(s if s is not None else "").replace("|", ";").strip()


def load():
    wb = openpyxl.load_workbook(CAT)
    epics = {}
    for r in wb["Epics"].iter_rows(min_row=2, values_only=True):
        epics[r[0]] = {"name": r[1], "stories": r[2], "lanes": r[3], "day1": r[4], "wave": r[5]}
    stories = list(wb["Stories"].iter_rows(min_row=2, values_only=True))
    per = collections.defaultdict(lambda: {"rel": collections.Counter(), "cg": set(), "be": collections.Counter(),
                                           "wt": collections.Counter(), "ow": collections.Counter(),
                                           "prd": set(), "lanes": set()})
    for r in stories:
        p = per[r[5]]
        p["rel"][r[8] or "None (new story)"] += 1
        p["lanes"].add(r[11])
        if str(r[11]).startswith("CG"):
            p["cg"].add(r[11])
        p["be"][r[7]] += 1
        p["wt"][r[2]] += 1
        p["ow"][r[3]] += 1
        p["prd"].add(str(r[13]).split(" (")[0])
    mapwb = openpyxl.load_workbook(MAP)
    svc = {}
    for r in mapwb["Services"].iter_rows(min_row=2, values_only=True):
        svc[r[0]] = {"short": r[1], "name": r[2], "wave": r[3], "schema": r[4], "base": r[5], "topic": r[6], "queue": r[7]}
    wf = collections.defaultdict(list)
    for r in mapwb["Workflows and activities"].iter_rows(min_row=2, values_only=True):
        wf[r[1]].append(r[0])
    own = json.loads(OWN.read_text(encoding="utf-8"))
    tabs = collections.Counter(t["owner"] for t in own["tables"].values())
    api = collections.Counter(v["owner"] for v in own["api"].values())
    ev = collections.Counter(v["owner"] for v in own["events"].values())
    # Arch v5 IN/OUT lines, one per service short.
    arch = ARCH.read_text(encoding="utf-8").splitlines()
    io = {}
    for i, line in enumerate(arch):
        m = re.match(r"^rwb-([a-z-]+) \(([PS]\d+), (.+)\)$", line)
        if m and i + 2 < len(arch) and arch[i + 1].startswith("IN: ") and arch[i + 2].startswith("OUT: "):
            io[m.group(1)] = {"code": m.group(2), "title": m.group(3),
                              "in": arch[i + 1][4:], "out": arch[i + 2][5:]}
    return epics, per, svc, wf, tabs, api, ev, io


def rel_text(counter):
    order = ["30 November 2026 (tentative)", "31 December 2026 (tentative)", "31 January 2027 (tentative)",
             "28 February 2027 (tentative)", "31 March 2027 (tentative)", "30 April 2027 (tentative)",
             "31 May 2027 (tentative)", "30 June 2027 (tentative)", "None (new story)"]
    parts = [f"{k} — {counter[k]}" for k in order if counter.get(k)]
    parts += [f"{k} — {v}" for k, v in sorted(counter.items()) if k not in order and v]
    return " · ".join(parts)


WT_CODE = {"Contract": "CON", "App development": "APP", "ACE DB": "DB", "Infrastructure": "INF",
           "DevOps": "OPS", "Integration": "ITG"}
WT_ORDER = {k: i for i, k in enumerate(WT_CODE)}
OW_ORDER = ["TechX (suggested; any team may pick up this story)",
            "ACE team (suggested; any team may pick up this story)",
            "SCB IT infrastructure (suggested; any team may pick up this story)",
            "DevOps team (suggested; any team may pick up this story)",
            "QA team (suggested; any team may pick up this story)"]


def owner_of(p):
    """§R5.3: the suggested owner most of the epic's stories carry; ties go to the contract-first owner order."""
    best = max(p["ow"].items(), key=lambda kv: (kv[1], -OW_ORDER.index(kv[0]) if kv[0] in OW_ORDER else -99))
    return best[0]


def wt_text(counter):
    order = ["Contract", "App development", "ACE DB", "Infrastructure", "DevOps", "Integration"]
    return " · ".join(f"{k} {counter[k]}" for k in order if counter.get(k))


def ow_text(counter):
    order = ["TechX (suggested; any team may pick up this story)",
             "ACE team (suggested; any team may pick up this story)",
             "SCB IT infrastructure (suggested; any team may pick up this story)",
             "DevOps team (suggested; any team may pick up this story)",
             "QA team (suggested; any team may pick up this story)"]
    parts = [f"{SHORT[k]} {counter[k]}" for k in order if counter.get(k)]
    parts += [f"{SHORT.get(k, k)} {v}" for k, v in sorted(counter.items()) if k not in order and v]
    return " · ".join(parts)


def scope_of(epic):
    if epic.startswith("RWB-PLT"):
        return "PLT"
    if epic.startswith("RWB-ITG"):
        return "ITG"
    return epic.replace("RWB-SVC-", "")


def short_of(epic):
    return epic.replace("RWB-SVC-", "").replace("RWB-PLT-", "PLT-").replace("RWB-ITG-", "ITG-")


def block(epic, epics, per, svc, wf, tabs, api, ev, io):
    e = epics[epic]
    p = per[epic]
    scope = scope_of(epic)
    owner = owner_of(p)
    mix = ow_text(p["ow"])
    total = sum(p["ow"].values())
    lines = [f"### {epic} — {e['name']}", "", "| Item | Value |", "|---|---|"]
    lines.append(f"| Epic | {epic} |")
    lines.append(f"| Scope | {scope} |")
    if epic.startswith("RWB-SVC-"):
        s = svc[scope]
        lines.append(f"| Service | `{s['short']}` ({e['name'].split('(')[1].rstrip(')').strip()}) |")
        lines.append(f"| Epic wave | {e['wave']} |")
        lines.append(f"| Arch v5 service wave | {s['wave']} |")
    elif epic.startswith("RWB-PLT-"):
        lines.append("| Service | platform |")
        lines.append(f"| Epic wave | {e['wave']} |")
    else:
        lines.append("| Service | integration |")
        lines.append(f"| Epic wave | {e['wave']} |")
    lines.append(f"| Suggested owner | {owner} |")
    lines.append(f"| Owner basis | {SHORT.get(owner, owner)} {p['ow'].get(owner, 0)} of {total} stories carry this suggestion; work-type mix: {wt_text(p['wt'])} (§R5.3) |")
    lines.append(f"| Owner mix of the stories | {mix} |")
    lines.append(f"| Stories | {e['stories']} |")
    cg = ", ".join(sorted(p["cg"])) if p["cg"] else ""
    lines.append(f"| Lanes | {e['lanes']} ({'contract groups: ' + cg if cg else 'no contract group'}) |")
    lines.append(f"| Day-1 stories | {e['day1']} |")
    lines.append(f"| Business-epic tags | {', '.join(sorted(p['be']))} |")
    lines.append(f"| Releases | {rel_text(p['rel'])} |")
    prd = " · ".join(f"`{x}`" for x in sorted(p["prd"]))
    lines.append(f"| PRD | {prd} |")
    if epic.startswith("RWB-SVC-"):
        s = svc[scope]
        wfs = ", ".join(sorted(wf.get(scope, []))) or "None in the Ownership Map"
        lines.append(f"| Schema | `{s['schema']}` |")
        lines.append(f"| REST base | `{s['base']}` |")
        lines.append(f"| Topic | `{s['topic']}` |")
        lines.append(f"| Temporal task queue | `{s['queue']}` |")
        lines.append(f"| Workflows owned | {wfs} |")
        lines.append(f"| Tables in the Ownership Map | {tabs.get(scope, 0)} |")
        lines.append(f"| REST operations in the Ownership Map | {api.get(scope, 0)} |")
        lines.append(f"| Events published in the Ownership Map | {ev.get(scope, 0)} |")
        lines.append(f"| Rule references | §R4 (naming per service); DP table of §R5.5 |")
        d = io.get(s["short"].replace("rwb-", ""))
        if d:
            lines.append("")
            lines.append(f"**Contract in Arch v5 (slides 14–20).**")
            lines.append("")
            lines.append(f"- In: {esc(d['in'])}")
            lines.append(f"- Out: {esc(d['out'])}")
    else:
        key = PLT_KEY.get(epic) if epic.startswith("RWB-PLT-") else ITG_KEY.get(epic)
        ref = PLT_REF.get(epic) if epic.startswith("RWB-PLT-") else ITG_REF.get(epic, "")
        lines.append(f"| Key stories | {key or 'None'} |")
        lines.append(f"| Rule references | {ref or 'None'} |")
    return "\n".join(lines)


ITG_KEY = {
    "RWB-ITG-W1": "`RWB-ITG-W1J01-ITG` Contract-test harness and synthetic test data (§R5.7 rule 6) · `RWB-ITG-W1J02-ITG` Wave 1 v5 journey end to end",
    "RWB-ITG-W2": "`RWB-ITG-W2J01-ITG` Wave 2 journey end to end",
    "RWB-ITG-W3": "`RWB-ITG-W3J01-ITG` Wave 3 journey end to end",
    "RWB-ITG-W4": "`RWB-ITG-W4J01-ITG` Wave 4 journey end to end",
    "RWB-ITG-NFR": "`RWB-ITG-TE009-ITG` Performance test harness · `RWB-ITG-TE010-ITG` Browser and accessibility tests",
}
ITG_REF = {
    "RWB-ITG-W1": "§R5.1 (one integration epic per wave); §R5.5 DP-11 and DP-16 (REST one hop, 2 s timeout; rwb-integration contract); §R5.7 rule 6 (the harness makes QA Day-1 work)",
    "RWB-ITG-W2": "§R5.1 (one integration epic per wave); §R5.4 class I (real cross-service behaviour, ITG stories only); §R5.7 rule 4",
    "RWB-ITG-W3": "§R5.1 (one integration epic per wave); §R5.4 class I (real cross-service behaviour, ITG stories only); §R5.7 rule 4",
    "RWB-ITG-W4": "§R5.1 (one integration epic per wave); §R5.4 class I (real cross-service behaviour, ITG stories only); §R5.7 rule 4",
    "RWB-ITG-NFR": "§R5.3 (harness and NFR stories: QA team); §R5.1 (non-functional integration epic); §R5.6 (W-MAP wave of the EP01-TE stories)",
}


def main():
    epics, per, svc, wf, tabs, api, ev, io = load()
    out = [HEAD, "", "# Recovery Workbench Service Epics v1", "",
           f"Tool: {TOOL}. Decision {DEC}.", "",
           "Source (read-only): `04 User stories/Recovery Workbench Service Story Catalog v1.xlsx` (Epics and Stories sheets), "
           "`22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` (Services and Workflows and activities sheets), "
           "`22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 14–20) and "
           "`22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` §R1, §R3, §R5, §R8 and §R9.", ""]

    out += ["## Change log", "", "| Version | Date | Decision | Tool | Change |", "|---|---|---|---|---|",
            f"| v1 | 22 November 2026 | {DEC} microservice realignment | {TOOL} | First issue of the Service Epics file: the 31 epics with scope, wave, suggested owner, lanes and Day-1 stories, taken from the Service Story Catalog v1 and the Microservice Ownership Map v1. |",
            ""]

    out += ["## 1. What this file is", "",
            "One block and one summary row for each of the 31 epics of the realignment: 19 service epics, 7 platform epics and 5 integration epics "
            "(`RWB-SVC-P1`…`RWB-SVC-S9`, `RWB-PLT-TPL`…`RWB-PLT-OBS`, `RWB-ITG-W1`…`RWB-ITG-NFR`; Template and Rules §R5.1 and user decision U1). "
            "Every story also carries its business epic (EP01–EP08) as a tag, so the service view and the business view of the same backlog stay in step.", "",
            "The numbers are the Service Story Catalog v1 numbers: stories, lanes and Day-1 stories per epic, and the wave. This file adds the two values the catalog stores nowhere at epic level — "
            "the scope of the epic and its suggested owner — using the epic ID pattern of §R5.2, the Microservice Ownership Map v1 and the fixed owner phrases of Template and Rules §R5.3. "
            "No story is changed here: the story files are the record, and this file is the overview.", "",
            "No conflict on the R-PREC list (§R3) had to be resolved in this file. The three values that had to be derived are stated in §10 with their gap and assumption rows (Template and Rules §R9).", "",
            "The Epics sheet of the catalog is reproduced here in full, with the scope and the suggested owner added. The Stories, Legacy map, Dependencies and Contracts sheets stay in the catalog: "
            "they are the source of the story files and of the Day-1 Work Allocation v1.", "",
            "**How to read it.**", "",
            "- **Scope.** `PLT` is a platform epic, `ITG` an integration epic, `P1`–`P10` a platform service and `S1`–`S9` a route service (naming pattern of §R5.2).",
            "- **Epic wave.** The wave at which the epic starts: the earliest wave carried by its stories. A story keeps its W-MAP wave when that is earlier than its service's Arch v5 wave (§R5.6), "
            "so for a service epic the Arch v5 service wave from the Ownership Map is shown next to the epic wave where the two differ.",
            "- **Suggested owner.** A suggestion only; any team may pick up any story (U3). The owner of an epic is the §R5.3 owner phrase that most of its stories carry "
            "(so the harness and NFR stories of `RWB-ITG-NFR` make QA team the owner of that epic), and the full fixed phrase is written in each block. The summary table uses the short team name.",
            "- **Lanes.** A lane is a connected group of non-CON stories linked by H dependencies; its depth is at most 4 (§R5.7 rule 5). A contract story is always Day 1 and sits in contract group `CG-W<wave>`, "
            "so a contract group is shared by every epic of its wave.",
            "- **Day-1 stories.** The count of stories whose Ready to start is \"Day 1\": contract stories, and stories whose only build dependencies are contract stories (§R5.7 rules 1 and 8).",
            "- **Releases.** Every date is copied unchanged and marked (tentative). A story that carries no legacy date is counted as \"None (new story)\", the wording the story files use.",
            ""]

    out += ["## 2. The 31 epics", "",
            "| Epic | Scope | Name | Epic wave | Arch v5 wave | Suggested owner | Stories | Lanes | Day-1 stories |",
            "|---|---|---|---|---|---|---|---|---|"]
    for epic in PLT_ORDER + SVC_ORDER + ITG_ORDER:
        e = epics[epic]
        scope = scope_of(epic)
        archwave = svc[scope]["wave"] if epic.startswith("RWB-SVC-") else ("0 (platform)" if epic.startswith("RWB-PLT-") else "—")
        own = SHORT[owner_of(per[epic])]
        out.append(f"| {epic} | {scope} | {esc(e['name'])} | {e['wave']} | {archwave} | {own} | {e['stories']} | {e['lanes']} | {e['day1']} |")
    tot = collections.Counter()
    for epic in PLT_ORDER + SVC_ORDER + ITG_ORDER:
        tot["stories"] += epics[epic]["stories"]
        tot["lanes"] += epics[epic]["lanes"]
        tot["day1"] += epics[epic]["day1"]
    out += ["", f"Totals: 31 epics · {tot['stories']} stories · {tot['day1']} Day-1 stories · {tot['lanes']} epic-lane memberships "
                f"(510 distinct lane IDs; a contract group is counted once per epic, see §8).", ""]

    out += ["## 3. Platform epics (7, wave 0)", "",
            "The platform epics carry the work every service needs before its own code starts: the service template, the shared libraries, the Temporal layer, the ACE schemas and logins, "
            "the Kafka and event platform, the edge and the observability baseline (§R5.1, §R4). They are wave 0: a platform contract story H dependency is what lets a service lane start on Day 1 (§R5.7 rules 1–3).", ""]
    for epic in PLT_ORDER:
        out += [block(epic, epics, per, svc, wf, tabs, api, ev, io), ""]

    out += ["## 4. Service epics (19)", "",
            "One epic per service, in service code order (§R4, U1). Each epic owns its schema, its login, its REST base, its topic and its Temporal task queue, "
            "and it may read another service's data only through that service's contract or through its own `v_ace_*` views (DP-01, DP-02, DP-05, §R7.2 s17).", "",
            "The table, operation and event counts of a block are the counts of the Ownership Map (its machine form `_work/msr/plan/ownership.json`). "
            "Where a count is 0 the map assigns none to that service; the named lists and the rulings behind them are in the map and its Rulings sheet.", ""]
    for epic in SVC_ORDER:
        out += [block(epic, epics, per, svc, wf, tabs, api, ev, io), ""]

    out += ["## 5. Integration epics (5)", "",
            "One integration epic per wave plus the non-functional epic (§R5.1). Integration stories are the only stories allowed to carry I dependencies (real cross-service behaviour, §R5.4 and §R5.7 rule 4), "
            "and the contract-test harness `RWB-ITG-W1J01-ITG` is what makes QA Day-1 work in wave 1 (§R5.7 rule 6).", ""]
    for epic in ITG_ORDER:
        out += [block(epic, epics, per, svc, wf, tabs, api, ev, io), ""]

    # §6 Day-1 by team type
    out += ["## 6. Day-1 work by team type", "",
            "Every team type has Day-1 work (§R5.7 rule 6). Counted from the Stories sheet of the catalog:", "",
            "| Team type | §R5.3 work types | Day-1 stories | Epics with Day-1 work |", "|---|---|---|---|"]
    team_wt = {"TechX (suggested; any team may pick up this story)": "CON, APP, ITG",
               "ACE team (suggested; any team may pick up this story)": "DB",
               "SCB IT infrastructure (suggested; any team may pick up this story)": "INF",
               "DevOps team (suggested; any team may pick up this story)": "OPS",
               "QA team (suggested; any team may pick up this story)": "ITG (harness and NFR)"}
    day1 = collections.Counter()
    day1_epics = collections.defaultdict(set)
    wb = openpyxl.load_workbook(CAT)
    for r in wb["Stories"].iter_rows(min_row=2, values_only=True):
        if r[12] == "Day 1":
            day1[r[3]] += 1
            day1_epics[r[3]].add(r[5])
    for k in team_wt:
        out.append(f"| {SHORT[k]} | {team_wt[k]} | {day1[k]} | {len(day1_epics[k])} |")
    out += ["", f"Total Day-1 stories: {sum(day1.values())}.", ""]

    # §7 waves
    out += ["## 7. Epics per wave", "", "| Wave | Platform epics | Service epics | Integration epics | Stories |", "|---|---|---|---|---|"]
    for w in range(0, 5):
        pl = [e for e in PLT_ORDER if epics[e]["wave"] == w]
        sv = [e for e in SVC_ORDER if epics[e]["wave"] == w]
        it = [e for e in ITG_ORDER if epics[e]["wave"] == w]
        n = sum(epics[e]["stories"] for e in pl + sv + it)
        out.append(f"| {w} | {len(pl)} | {len(sv)} | {len(it)} | {n} |")
    out += ["", "A service epic sits in the wave of its earliest story, so seven service epics start before their service's Arch v5 wave: "
                "`RWB-SVC-S3` (epic wave 2, Arch v5 wave 3), `RWB-SVC-S4` (2 / 3), `RWB-SVC-S5` (1 / 2), `RWB-SVC-S6` (3 / 4), `RWB-SVC-S8` (1 / 2), `RWB-SVC-S9` (1 / 4) and `RWB-SVC-P8` (1 / 2). "
                "The other twelve service epics start in their service's own wave (`RWB-SVC-S1` 3, `RWB-SVC-S2` 2, `RWB-SVC-S7` 4, and `RWB-SVC-P1`–`RWB-SVC-P7`, `RWB-SVC-P9` and `RWB-SVC-P10` at 1). "
                "The story-level conflict is raised once per service and business epic by the story work packages (§R5.6).", ""]

    # §8 lanes
    out += ["## 8. Lanes and contract groups", "",
            "| Contract group | Wave | Stories in the group | Epics that use it |", "|---|---|---|---|"]
    for cg in ["CG-W0", "CG-W1", "CG-W2", "CG-W3", "CG-W4"]:
        n = sum(1 for r in wb["Stories"].iter_rows(min_row=2, values_only=True) if r[11] == cg)
        ep = sorted({r[5] for r in wb["Stories"].iter_rows(min_row=2, values_only=True) if r[11] == cg})
        out.append(f"| {cg} | {cg[-1]} | {n} | {len(ep)} |")
    out += ["", "A contract group is one lane shared by every epic of its wave, so the per-epic lane counts in §2 add to 547 while the programme has 510 distinct lanes. "
                "The other lanes are per-epic work lanes `L-<scope>-<n>` and the integration lanes `L-ITG-W<n>`.", ""]

    # §9 reconciliation
    out += ["## 9. Totals and reconciliation", "", "| Measure | Value | Source |", "|---|---|---|",
            "| Epics | 31 (19 service, 7 platform, 5 integration) | Catalog Epics sheet; §R5.1 |",
            f"| Stories | {tot['stories']} | Catalog Epics sheet; `split_plan.json` stats slices |",
            f"| Day-1 stories | {tot['day1']} | Catalog Epics sheet; `split_plan.json` stats day1 |",
            "| Legacy stories mapped | 358 | `split_plan.json` stats legacy |",
            "| Distinct lanes | 510 | `split_plan.json` stats lanes |",
            "| Epic-lane memberships | 547 | Catalog Epics sheet (a shared contract group is counted per epic) |",
            "| Release dates | unchanged, every one marked (tentative) | Catalog Stories sheet |", ""]

    # §10 open items
    out += ["## 10. Open items", "",
            "Three documentation values are not carried by the source catalog and are resolved as recorded: they do not change a story, a lane or a date.", "",
            "| ID | What is open | Resolution used here | Severity |", "|---|---|---|---|",
            "| CG-C-EPICS-1 | The catalog has no epic-level scope or owner column. | Scope from the epic ID pattern (§R5.2); owner from the Ownership Map and the work-type owner table (§R5.3). Assumption ASM-C-EPICS-1. | P3 |",
            "| CG-C-EPICS-2 | The catalog Epics sheet gives a wave but no rule for it, and §R5.6 also puts \"NF\" work at wave 0. | Epic wave = earliest wave among its stories; the Arch v5 service wave is shown beside it. Assumption ASM-C-EPICS-2. | P3 |",
            "| CG-C-EPICS-3 | Per-epic lane counts add to 547, the distinct lane count is 510. | A shared contract group `CG-W<n>` is counted in every epic that uses it; both numbers are shown. Assumption ASM-C-EPICS-3. | P3 |", ""]

    # §11 traceability
    out += ["## 11. Traceability", "",
            "| DOC ID | Part of this file | Source | Decision |", "|---|---|---|---|",
            "| DOC-EPICS-01 | §1 and §2, the 31 epics and their scope | Catalog Epics sheet; §R5.1, §R5.2, U1 | D-RCV-60 |",
            "| DOC-EPICS-02 | §2 and §3–§5, wave per epic | Catalog Stories sheet waves; §R5.6 | D-RCV-60 |",
            "| DOC-EPICS-03 | §2 and §3–§5, suggested owner per epic | Ownership Map Services sheet; §R5.3, U3 | D-RCV-60 |",
            "| DOC-EPICS-04 | §4, the service runtime facts (schema, REST base, topic, queue, workflows, tables, operations, events) | Ownership Map Services and Workflows and activities sheets; `ownership.json` | D-RCV-60 |",
            "| DOC-EPICS-05 | §4, the IN and OUT contract lines | Arch v5 Text Extract v1 slides 14–20 | D-RCV-60 |",
            "| DOC-EPICS-06 | §6–§9, Day-1 work, waves, lanes and totals | Catalog Stories and Epics sheets; `split_plan.json` stats; §R5.7 | D-RCV-60 |", ""]

    # §12 out of scope
    out += ["## 12. Out of scope", "",
            "- The story content itself: each story file carries its own 20 metadata rows and 19 sections, and its acceptance criteria.",
            "- The Day-1 Work Allocation v1 (capacity per lane) and the epic overview per epic folder, which are separate files of the Service Story Catalog v1 set (§R8.7).",
            "- The build order, dependency map and RTM, which are their own next versions (§R8.7).",
            "- Anything outside the Recovery Workbench: no data lake (DP-17), no tracker update (U6).", ""]

    doc = "\n".join(out)
    doc = re.sub(r"\n{3,}", "\n\n", doc)
    doc = doc.replace("slides 14\u201320", "slides 14-20").replace("\u2014", "—")
    OUT.write_text(doc, encoding="utf-8")
    print("WROTE", OUT)
    print("lines", len(doc.splitlines()))


if __name__ == "__main__":
    main()
