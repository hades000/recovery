"""Builds the Markdown of Recovery Workbench Story Build Order v4 from the v3 docx and the plan."""
import json, os, sys, collections

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
WORK = os.path.join(ROOT, "_work", "msr")

SERVICE = {
    "P1": "P1 rwb-source-data", "P2": "P2 rwb-integration", "P3": "P3 rwb-case", "P4": "P4 rwb-access",
    "P5": "P5 rwb-document", "P6": "P6 rwb-comms", "P7": "P7 rwb-decision", "P8": "P8 rwb-payment",
    "P9": "P9 rwb-reporting", "P10": "P10 rwb-agent", "S1": "S1 rwb-valuation", "S2": "S2 rwb-treatment",
    "S3": "S3 rwb-guarantee", "S4": "S4 rwb-litigation", "S5": "S5 rwb-asset", "S6": "S6 rwb-debtsale",
    "S7": "S7 rwb-writeoff", "S8": "S8 rwb-deviation", "S9": "S9 rwb-partner", "PLT": "PLT platform",
    "ITG": "ITG integration",
}
WT_NAME = {"CON": "Contract", "APP": "App development", "DB": "ACE DB", "INF": "Infrastructure",
           "OPS": "DevOps", "ITG": "Integration"}
WT_ORDER = {w: i for i, w in enumerate(["CON", "APP", "DB", "INF", "OPS", "ITG"])}
OWNER = {"TechX": "TechX", "ACE": "ACE team", "INFRA": "SCB IT infrastructure", "DEVOPS": "DevOps team",
         "QA": "QA team", "TechX (suggested; any team may pick up this story)": "TechX"}

items = json.load(open(os.path.join(WORK, "docs", "C4-SBO", "items.json"), encoding="utf-8"))
legacy = json.load(open(os.path.join(WORK, "plan", "split_plan.json"), encoding="utf-8"))["legacy"]
frags = {}
for f in os.listdir(os.path.join(WORK, "fragments")):
    d = json.load(open(os.path.join(WORK, "fragments", f), encoding="utf-8"))
    frags[d["id"]] = d
by_legacy = collections.defaultdict(list)
for d in frags.values():
    by_legacy[d["legacy"]].append(d)

def cell(x):
    return str(x).replace("|", "\\|").strip()

def row(*cols):
    return "| " + " | ".join(cell(c) for c in cols) + " |"

def slices(key):
    return sorted(by_legacy[key], key=lambda d: (WT_ORDER[d["wt"]], d["id"]))

RETIRED_NOTE = {
    "RWB-E1-014": "None. Retired in D-RCV-60: there is no data lake and the copy is dropped (DP-17).",
    "RWB-TE-007": "None. Retired in D-RCV-60: the work is RWB-PLT-E1071-CON, Temporal Schedules (DP-10).",
}

wins = [("W1", "Window 1, 2 to 13 November 2026 (tentative)", "Epic 1"),
        ("W2", "Window 2, 16 to 27 November 2026 (tentative)", "Epic 1"),
        ("W3", "Window 3, 30 November to 11 December 2026 (tentative)", "Epic 2"),
        ("W4", "Window 4, 14 to 25 December 2026 (tentative)", "Epic 2"),
        ("E3", "Epic 3, 28 December 2026 to 22 January 2027 (tentative)", "Epic 3")]

L = []
A = L.append

A("SCB Collections and Recovery. Henka Group, 22 November 2026.")
A("(C) Siam Commercial Bank and Henka Pte Ltd")
A("")
A("# Recovery Workbench story build order")
A("")
A("E2E Recovery Workbench. SCB Collections and Recovery. Henka Group, 22 November 2026. v4. "
  "Version 3 of this document is dated 16 November 2026.")
A("")
A("Version 4 keeps the 115 items of version 3 in their five windows, with every key, title, module, "
  "E or S flag, waits-on, item number and date unchanged, and adds the two things the realignment needs: "
  "the parallel lane of every story and its Ready to start position. Each item is shown as the "
  "microservice stories that carry it, with the service of the Ownership Map v1 and the suggested owner "
  "of the work type in Template and Rules §R5.3.")
A("")
A("No approval of this version is recorded, so it is issued as Draft: Not specified in the source "
  "documents (CG-C4-SBO-1; ASM-C4-SBO-1).")
A("")
A("## How this version is read")
A("")
A("- Lane. A parallel lane is a connected group of non-contract stories joined by a build dependency (H). "
  "A contract story has no build dependency and sits in the contract group CG-W<wave>. A lane is at most "
  "four stories deep: the longest chain of build dependencies inside a lane is four stories, and a deeper "
  "chain is cut so that the later story builds against the earlier story's contract (Template and Rules "
  "§R5.7 rules 1 to 5).")
A("- Ready to start. Day 1 means the story has contract dependencies only, and a contract dependency never "
  "blocks because the application builds against the published contract and its fake. After <story> names "
  "the story in the same lane that it waits for (Template and Rules §R5.7 rule 8, §R5.4).")
A("- Owner. The service of a story is the Ownership Map v1. The team type is the suggested owner of the "
  "work type in Template and Rules §R5.3, and it is a suggestion only: any team may pick up any story "
  "(U3; DL46).")
A("- Legacy key. The key of version 3 is kept beside its new stories, so an item can still be found and "
  "ordered the old way. The waits-on column of version 3 is kept word for word; it names legacy keys, and "
  "the realigned waits of each story are its Ready to start and its lane (CG-C4-SBO-9; ASM-C4-SBO-9).")
A("")
A("The order the 115 items are built in, from Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx. "
  "The story numbers are a catalog, not an order: RWB-E1-001 depends on RWB-E1-043 and RWB-E1-044, which "
  "are built before it. Pull the next item whose dependencies are done. E is an enabler, S is a user story. "
  "Waits on names the items that must finish first, by their number within the same family. RWB-ACE-001 is "
  "the ACE team's delivery and is not pulled by either squad; it gates RWB-E1-069.")
A("")
A("D-RCV-36. This version applies decision D-RCV-36. Temporal runs the case lifecycle from Epic 3, with "
  "case data in the ACE database, and Drools evaluates rules from versioned rule packages. RWB-E1-029, "
  "RWB-TE-005 and RWB-E1-048 are retired; their work moved to RWB-E1-073 and RWB-E2-041. The new "
  "configuration stories are RWB-E1-070 to RWB-E1-073 and RWB-E2-037 to RWB-E2-043.")
A("")
A("Why configuration comes first. The Epic 1 configuration stories RWB-E1-070 to RWB-E1-073 build the "
  "Temporal platform, the worker, the Drools runtime and the rule authoring path before RWB-E1-018, "
  "RWB-E1-020 and RWB-E1-021, because those engines call RuleEvaluator and write the package version to "
  "the decision log. The Epic 2 stories do the same before the engines: RWB-E2-042 loads the RESTRUCTURE, "
  "PAYMENT_MATCH and BOOKING_MATCH packages before RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008 and "
  "RWB-E2-027, and RWB-E2-043 sets the integration pattern before Epic 3.")
A("")
A("D-RCV-60. This version also applies decision D-RCV-60: Architecture v5, 19 services inside ACE, Kafka "
  "with outbox and inbox, a reusable Temporal layer, embedded Drools with the rule registry in "
  "rwb-decision, the edge of gateway-bff and the partner gateway, and no data lake. Every one of the 115 "
  "items is split into the stories that carry it (Template and Rules §R5 and §R6), and each story carries "
  "its own lane and its own Ready to start, so an item is no longer one unit of work: it is the stories "
  "listed against it, and the contract story of the item is pulled before the application stories that "
  "use it. A build dependency points only inside the service or to a platform contract story; a "
  "dependency on another service is a contract dependency and never blocks the build; an integration "
  "dependency sits only on an integration story; external and team-type work is tracked and does not "
  "block. Two items carry no story: RWB-E1-014, the decision log copy to the data lake, because there is "
  "no data lake (DP-17), and RWB-TE-007, the Quartz scheduler, whose work is RWB-PLT-E1071-CON on Temporal "
  "Schedules (DP-10).")
A("")

widths = ["#", "Key", "Title", "Module", "E or S", "Waits on"]
ranks = ["#", "Key", "New story", "Work type", "Service", "Suggested owner", "Parallel lane", "Ready to start"]

total_items = 0
total_stories = 0
for wkey, wtitle, epic in wins:
    wi = [i for i in items if i["window"] == wkey]
    n = len(wi)
    total_items += n
    stories = sum(len(slices(i["key"])) for i in wi)
    total_stories += stories
    A("## " + wtitle)
    A("")
    A(f"{n} items, releasing in {epic} (tentative).")
    A("")
    A(row(*widths))
    A("|" + "---|" * len(widths))
    for i in wi:
        A(row(i["n"], i["key"], i["title"], i["module"], i["es"], i["waits"]))
    A("")
    A(f"The same {n} items in the same order, as the {stories} microservice stories that carry them. "
      "Inside an item the contract story comes first, then the application, database, infrastructure, "
      "DevOps and integration stories.")
    A("")
    A(row(*ranks))
    A("|" + "---|" * len(ranks))
    for i in wi:
        sl = slices(i["key"])
        if not sl:
            continue
        for d in sl:
            A(row(i["n"], i["key"], d["id"], WT_NAME[d["wt"]], SERVICE[d["id"].split("-")[1]],
                  OWNER[d["owner"]], d["lane"], d["ready"]))
    retired = [i for i in wi if not slices(i["key"])]
    if retired:
        A("")
        note = []
        for i in retired:
            if i["key"] == "RWB-E1-014":
                note.append("item 19 RWB-E1-014, the decision-log copy to the data lake, because there is no "
                            "data lake in D-RCV-60 (DP-17)")
            elif i["key"] == "RWB-TE-007":
                note.append("item 21 RWB-TE-007, the Quartz scheduler, whose work is RWB-PLT-E1071-CON on "
                            "Temporal Schedules (DP-10)")
            else:
                note.append(f"item {i['n']} {i['key']}")
        A(f"No story carries {', and no story carries '.join(note)}. The item keeps its number and its place "
          "in the order of version 3, and a dependency that pointed at RWB-TE-007 now points at "
          "RWB-PLT-E1071-CON (Template and Rules §R6).")
    A("")

# summary
wave_rows = []
for w in [0, 1, 2, 3, 4]:
    ss = [x for x in frags.values() if x["wave"] == w]
    wave_rows.append((w, len(ss), len(set(x["lane"] for x in ss)),
                      sum(1 for x in ss if x["ready"] == "Day 1"),
                      sum(1 for x in ss if x["ready"] != "Day 1"),
                      sum(1 for x in ss if x["wt"] == "CON")))
allss = list(frags.values())
day1 = [x for x in allss if x["ready"] == "Day 1"]
lanes = len(set(x["lane"] for x in allss))
by_team = collections.Counter(OWNER[x["owner"]] for x in day1)

A("## Lanes and Day 1 in this version")
A("")
doc = [d for i in items for d in by_legacy[i["key"]]]
doc_day1 = [d for d in doc if d["ready"] == "Day 1"]
doc_team = collections.Counter(OWNER[d["owner"]] for d in doc_day1)
A(f"This version gives every story its lane and its Day-1 position. The 115 items are carried by "
  f"{len(doc)} stories: {len(doc_day1)} are Day 1 and {len(doc) - len(doc_day1)} wait for a story in "
  f"their own lane, in {len(set(d['lane'] for d in doc))} lanes. The "
  f"{sum(1 for d in doc if d['wt'] == 'CON')} contract stories of these items carry no build dependency "
  "and sit in the contract groups CG-W0 to CG-W4, one per wave; a contract story is always Day 1, and "
  "its fake lets the application story start beside it (Template and Rules §R5.7 rules 1, 2 and 8).")
A("")
A(row("Team type", "Day-1 stories of the 115 items", "Work types"))
A("|---|---|---|")
for team, types in [("TechX", "Contract, App development, Integration"),
                    ("ACE team", "ACE DB"),
                    ("SCB IT infrastructure", "Infrastructure"),
                    ("DevOps team", "DevOps"),
                    ("QA team", "Integration harness and non-functional stories")]:
    A(row(team, doc_team.get(team, 0), types))
A(row("All", len(doc_day1), "All six work types"))
A("")
A("The board limit of a team type, and the number of stories a team type may hold at once, is Not "
  "specified in the source documents (CG-C4-SBO-6; ASM-C4-SBO-6). The board limit per squad of version 3 "
  "is kept unchanged.")
A("")
A(f"The whole story set of this run, which carries the later epics and the new platform and harness "
  f"stories beside the 115 items, has {len(allss)} stories in {lanes} lanes, of which {len(day1)} are "
  "Day 1. Its position by wave:")
A("")
A(row("Wave", "Stories", "Lanes used", "Contract group", "Day 1", "Waits for a story in its lane"))
A("|---|---|---|---|---|---|")
for w, n, ln, d1, wt_, con in wave_rows:
    A(row(f"Wave {w}", n, ln, f"CG-W{w}", d1, wt_))
A(row("All", len(allss), lanes, "CG-W0 to CG-W4", len(day1), len(allss) - len(day1)))
A("")
A("Every service has at least one contract story, and every team type has Day-1 work (Template and Rules "
  "§R5.7 rules 6 and 7). A lane is named after the service that owns it and a letter, for example L-P3-F "
  "for rwb-case; a lane of the platform epics is L-PLT-<epic>-<letter> and a lane of the integration "
  "epics is L-ITG-W<n>, with L-ITG-NFR for the non-functional stories. The longest chain of build "
  "dependencies inside any lane of the set is four stories.")
A("")

# new stories
new_keys = ["N%03d" % i for i in range(1, 13)] + ["W1J01", "W1J02", "W2J01", "W3J01", "W4J01"]
new = [x for x in frags.values() if x["legacy"] in new_keys]
A("## Day-1 work that is new in this version")
A("")
A("These stories carry no item of version 3 and they are all Day 1. N001 to N012 are the platform stories "
  "of wave 0, and W1J01 to W4J01 are the integration harness and journey stories, one pair per wave. They "
  "are what makes sure every team type has Day-1 work: the infrastructure stories for SCB IT "
  "infrastructure, the DevOps stories for the DevOps team, the ACE DB story for the ACE team, and W1J01 "
  "with the harness stories for QA (Template and Rules §R5.7 rule 6). They sit before the five windows of "
  "this document, because wave 0 is not a release (CG-C4-SBO-8; ASM-C4-SBO-8).")
A("")
A(row("Legacy key", "New story", "Work type", "Service", "Suggested owner", "Parallel lane", "Ready to start"))
A("|---|---|---|---|---|---|---|")
for d in sorted(new, key=lambda x: (x["legacy"], WT_ORDER[x["wt"]])):
    A(row(d["legacy"], d["id"], WT_NAME[d["wt"]], SERVICE[d["id"].split("-")[1]], OWNER[d["owner"]],
          d["lane"], d["ready"]))
A("")

A("## How to use it")
A("")
A("Take the next item in order whose dependencies are done. Work in progress per squad stays within the "
  "board limit. An item on the critical path is taken before any other item. An item that will miss its "
  "release stays behind its flag and moves to the next release. The two squads agree the split at the "
  "daily board; the product owner settles a disagreement the same day.")
A("")
A("The critical path starts outside the squads. RWB-ACE-001, the ACE team's 14 tables, 12 columns and read "
  "grant, is due on 21 November under DL43 and gates RWB-E1-069, the 30 read-only views. RWB-E1-069 gates "
  "RWB-E1-018 and RWB-E1-002, the case record and the case list. RWB-E1-072 and RWB-E1-073 gate RWB-E1-018, "
  "so the four configuration stories RWB-E1-070 to RWB-E1-073 sit on the chain. From RWB-E1-020 the chain "
  "runs RWB-E1-028, RWB-E1-030, RWB-E1-059, RWB-E1-061 and RWB-E1-063, then RWB-E2-031, RWB-E2-028 and "
  "RWB-E2-029: 17 items end to end. A day lost on RWB-ACE-001, on RWB-E1-069 or on the Temporal and Drools "
  "configuration moves the 30 November release.")
A("")
A("In this version the two squads are the five team types: TechX, ACE team, SCB IT infrastructure, DevOps "
  "team and QA team. The daily board agrees the item order as before, and the product owner settles a "
  "disagreement the same day; no source states how a team type is assigned to an item before the board "
  "meets (CG-C4-SBO-3; ASM-C4-SBO-3).")
A("")
A("An item is pulled by its stories, in the order contract, application, database, infrastructure, DevOps "
  "and integration. A Day-1 story may be pulled at once by any team type. A story that is not Day 1 is "
  "pulled when the story named in its Ready to start is done, and it never waits for a story of another "
  "service: a contract dependency is answered by the published contract and its fake, an integration "
  "dependency sits only on an integration story, and external or team-type work is tracked and does not "
  "block the build (Template and Rules §R5.4 and §R5.7).")
A("")
A("The critical path in the lane terms of this version: RWB-ACE-001 is lane L-P1-A as RWB-P1-ACE001-DB; "
  "RWB-E1-069 is lane L-P1-R; RWB-E1-018 is lane L-P3-F; the four configuration stories RWB-E1-070 to "
  "RWB-E1-073 are lanes L-PLT-WF-D, L-PLT-WF-E, L-PLT-LIB-I and L-P3-W; RWB-E1-020 and RWB-E1-028 are "
  "lanes L-P3-F and L-P3-K; RWB-E1-030 is lane L-P3-L; RWB-E1-059, RWB-E1-061 and RWB-E1-063 are lane "
  "L-P10-A; RWB-E2-031 is lane L-P10-F and RWB-E2-028 is lane L-P10-E, with RWB-E2-029 in L-S8-I beside "
  "them. RWB-E1-072 is the platform contract RWB-PLT-E1072-CON, so the Drools runtime reaches RWB-E1-018 "
  "through that contract and its fake and the chain is not blocked by the platform epic.")
A("")
A("Every release date in this document is unchanged and tentative (U7; DL48). Version 3 names no release "
  "date for an item: it names the epic a window releases in, and this version keeps that statement as it "
  "stands, marked tentative (CG-C4-SBO-7; ASM-C4-SBO-7). The window dates above are the dates of "
  "version 3 and are not moved by the realignment.")
A("")

A("## Assumptions and gaps")
A("")
A("Open points of this document, each carried as a gap row and an assumption row:")
A("")
A("- The approval and the status of version 4 (CG-C4-SBO-1; ASM-C4-SBO-1).")
A("- The change log of version 3, which the source does not carry (CG-C4-SBO-2; ASM-C4-SBO-2).")
A("- The two squads of version 3 against the five team types of this version (CG-C4-SBO-3; ASM-C4-SBO-3).")
A("- One module per item against the several services each split story belongs to (CG-C4-SBO-4; ASM-C4-SBO-4).")
A("- The two items that version 3 still lists and D-RCV-60 retires, RWB-E1-014 and RWB-TE-007 "
  "(CG-C4-SBO-5; ASM-C4-SBO-5).")
A("- The board limit of a team type (CG-C4-SBO-6; ASM-C4-SBO-6).")
A("- The release date of an item, which version 3 gives only as the epic it releases in (CG-C4-SBO-7; "
  "ASM-C4-SBO-7).")
A("- The platform and harness stories N001 to N012 and W1J01 to W4J01, which sit in no window of version 3 "
  "(CG-C4-SBO-8; ASM-C4-SBO-8).")
A("- The waits-on column of version 3, which names legacy keys and not the stories that now carry them "
  "(CG-C4-SBO-9; ASM-C4-SBO-9).")
A("")
A("## Change log")
A("")
A(row("Version", "Date", "Change", "Tool"))
A("|---|---|---|---|")
A(row("3", "16 November 2026",
      "Source version. It carries no change-log row of its own; the realignment records that as a gap "
      "and an assumption (CG-C4-SBO-2; ASM-C4-SBO-2).",
      "Not specified in the source documents (CG-C4-SBO-2; ASM-C4-SBO-2)"))
A(row("4", "22 November 2026",
      "D-RCV-60 microservice realignment: the 115 items kept in their five windows with every key, title, "
      "module, E or S flag, waits-on, item number and date, and each item split into its microservice "
      "stories with the service of the Ownership Map v1, the suggested owner of the work type, the "
      "parallel lane and the Ready to start of every story; the two retired items carry no story; the "
      "Day-1 summary and the new platform and harness stories added.",
      "T3 Code / OpenCode / DeepSeek v4.1 Flash"))
A("")

md = "\n".join(L) + "\n"
out = os.path.join(WORK, "docs", "C4-SBO", "Recovery Workbench Story Build Order v4.md")
open(out, "w", encoding="utf-8", newline="\n").write(md)
print("WROTE", out, len(md), "chars", total_items, "items", total_stories, "story rows")
