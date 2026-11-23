"""Build the Service Catalog v1 .md and the markdown source of the .xlsx (WP B-ARCH-SVC)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import data as D

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench Service Catalog v1.md"
XMD = Path(__file__).resolve().parent / "catalog_xlsx.md"

HDR = "SCB Collections and Recovery. Henka Group, 22 November 2026.\n(C) Siam Commercial Bank and Henka Pte Ltd\n"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"


def retry(topic):
    return f"{topic}.retry.1m, {topic}.retry.10m, {topic}.retry.1h, {topic}.dlt"


def tbl(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def resources(code):
    raw = D.TABLES.get(code, "")
    return [t.strip() for t in raw.split(",") if t.strip()]


def provided(s):
    return [f"{k}: {v}" for k, v in s["tmp"] if k != "Out"]


def outward(s):
    return [v for k, v in s["tmp"] if k == "Out"]


# ---------------------------------------------------------------- markdown document
L = []
a = L.append

a(HDR)
a("# Recovery Workbench Service Catalog v1")
a("")
a(tbl(["Item", "Value"], [
    ["Document", "Recovery Workbench Service Catalog"],
    ["Version", "1"],
    ["Date", "22 November 2026"],
    ["Decision", "D-RCV-60 microservice realignment"],
    ["Tool", TOOL],
    ["Status", "Draft"],
    ["Owner role", "Solution architect"],
    ["Services in scope", "19: P1 to P10 and S1 to S9, plus the shared platform (PLT)"],
    ["Source of record", "Recovery Workbench Architecture v5 Text Extract v1 (slides 13 to 20 and 41 to 44); "
                         "Recovery Workbench Microservice Ownership Map v1; Recovery Workbench Temporal and Drools "
                         "Design Text Extract v1"],
    ["Change log", "below"],
]))
a("")
a(tbl(["Version", "Date", "Change", "Detail"], [
    ["1", "22 November 2026", f"D-RCV-60 microservice realignment, {TOOL}",
     "First Service Catalog. The 19 services, the resources each one owns, the provider and consumer contracts, "
     "the waves and the conformance rules are taken from Architecture v5 and the Ownership Map v1. No earlier "
     "version of this family exists (CG-B-ARCH-SVC-9; ASM-B-ARCH-SVC-9)."],
]))
a("")

a("# 1. Purpose and scope")
a("")
a("This catalogue is the single list of the 19 Recovery services. For each service it states the code, the name, "
  "the wave, the service epic, the schema and login, the REST base, the Kafka topic with its retry and dead-letter "
  "topics, the Temporal task queue, the Java package, the resources the service owns, and what it provides to and "
  "consumes from the other services.")
a("")
a("It is the reference for four groups of readers:")
a("")
a("- architects, who check that a call crosses exactly one boundary and in the right call type;")
a("- the service teams, who build one service from the template in the Service Template Specification v1;")
a("- ACE DB, who creates one schema, one login and one connection pool per service;")
a("- the platform team, who creates the topics, the queues, the Helm releases and the dashboards.")
a("")
a("What this catalogue does not contain: the request and response schemas (API Specification v5), the event "
  "payloads (Kafka Topic and Event Catalog v1), the workflow steps (Temporal Workflow and Activity Catalog v1), "
  "the table columns (Logical Data Model and Physical Schema) and the story-level build order (Build Sequence).")
a("")

a("# 2. How this catalogue is built")
a("")
a("## 2.1 Precedence")
a("")
a("Where two sources disagree, the higher one wins and the loser is recorded as a gap and an assumption "
  "(Template and Rules §R3). The order used here is:")
a("")
a("1. the Arch v5 catalogue slides 13 to 20 and 41 to 44, for services, resources, call types and jobs;")
a("2. the Recovery Temporal and Drools Design v1, for the workflow split and the rules placement;")
a("3. the Arch v5 narrative slides, for the standards that every service follows;")
a("4. the Recovery Workbench Microservice Ownership Map v1, for the owner of every table, endpoint, event and "
  "workflow;")
a("5. the current architecture documents (Decision Log, ADRs, TSDs, FSDs, LDM), which the realignment rewrites.")
a("")
a("The Ownership Map is used for every owner in this catalogue. Its Services sheet is the source of the code, the "
  "service name, the wave, the schema, the REST base, the topic and the task queue; its Tables, Endpoints, Events, "
  "Workflows and activities and Jobs sheets are the source of the ownership of every resource named below.")
a("")
a("## 2.2 What changed in this version")
a("")
a("- The single recovery service and the single recovery schema of the earlier documents become 19 services with "
  "19 schemas, 19 logins, 19 topics and 19 task queues (Arch v5 slide 41; ADR-013 and ADR-014).")
a("- Every service is named and packaged by the rules in Template and Rules §R4, and is listed with the same field "
  "set so that the API, event, workflow, data and story documents can point at one row.")
a("- The resources are the tables of the Ownership Map v1. The current recovery schema is split across the 19 "
  "schemas; the outbox, inbox and idempotency tables are library tables created in every service schema.")
a("- No service and no call type is added or removed against Architecture v5. Two resource lists that Arch v5 "
  "names but the Ownership Map does not yet hold are recorded as gaps (CG-B-ARCH-SVC-1 and CG-B-ARCH-SVC-2).")
a("")

a("# 3. The 19 services at a glance")
a("")
a("Order is the Ownership Map order: platform services P1 to P10, then the route services S1 to S9.")
a("")
rows = []
for s in D.SVC:
    rows.append([s["code"], "rwb-" + s["short"], s["name"], s["wave"], f"RWB-SVC-{s['code']}",
                 s["schema"], s["base"], s["topic"], s["queue"], s["pkg"]])
a(tbl(["Code", "Service", "Name", "Wave", "Service epic", "Schema and login", "REST base", "Kafka topic",
       "Task queue", "Java package"], rows))
a("")
a(tbl(["Item", "Value"], [
    ["Services", "19"],
    ["Platform services (P1 to P10)", "10"],
    ["Route services (S1 to S9)", "9"],
    ["Services in wave 1", "9: P1, P2, P3, P4, P5, P6, P7, P9, P10"],
    ["Services in wave 2", "4: P8, S2, S5, S8"],
    ["Services in wave 3", "4: S1, S3, S4, S6"],
    ["Services in wave 4", "2: S7, S9"],
    ["Shared topic", "rwb.decision-record.v1 (producer: all 19; central ledger: rwb-decision)"],
    ["Temporal namespace", "rwb-recovery"],
    ["Platform task queue", "rwb-platform (platform jobs JOB-21 and JOB-22)"],
    ["Shared platform tables per service", f"{len(resources('PLT'))}: " + ", ".join(resources("PLT"))],
]))
a("")

a("# 4. Waves and service epics")
a("")
a("A service is created when its first epic starts, so nothing is built twice (Arch v5 slide 38). Wave 0 builds "
  "the template once: the service template with the outbox, the inbox, the Temporal worker, the codec and "
  "OpenTelemetry, one Helm chart, the golden pipeline, the contract libraries, the workflow kit, the 19 schemas and "
  "logins, the Kafka topics and ACLs, and Temporal 1.30 or later.")
a("")
a(tbl(["Wave", "Services", "Service epics", "Built in the wave", "Gate"], [
    ["0", "None (platform only)", "RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, "
     "RWB-PLT-OBS", "Service template, Helm chart, golden pipeline, contract libraries, workflow kit, 19 schemas and "
     "logins, topics and ACLs", "Template accepted; 19 logins created; topics exist"],
    ["1", "P1, P2, P3, P4, P5, P6, P7, P9, P10", "RWB-SVC-P1 to RWB-SVC-P7, RWB-SVC-P9, RWB-SVC-P10",
     "9 services, each an API deployment and a worker deployment", "BOT approval before Wave 1 go-live, if "
     "required (FPG 19/2560 cl. 5.5; up to 30 business days)"],
    ["2", "P8, S2, S5, S8", "RWB-SVC-P8, RWB-SVC-S2, RWB-SVC-S5, RWB-SVC-S8", "4 services", "Wave 1 in production"],
    ["3", "S1, S3, S4, S6", "RWB-SVC-S1, RWB-SVC-S3, RWB-SVC-S4, RWB-SVC-S6", "4 services", "Wave 2 in production"],
    ["4", "S7, S9", "RWB-SVC-S7, RWB-SVC-S9", "2 services", "Wave 3 in production"],
]))
a("")
a("No service in this catalogue carries a release date. Release dates are held in the Release Plan and are "
  "tentative (Decision U7 and DL48).")
a("")

a("# 5. Naming, packaging and identifiers")
a("")
a("Every service follows one set of rules (Template and Rules §R4). Nothing in this table is optional; the "
  "conformance rules in section 9 test it.")
a("")
a(tbl(["Element", "Rule", "Example (P3)", "Example (S6)"], [
    ["Service code", "P1 to P10, S1 to S9", "P3", "S6"],
    ["Service name", "`rwb-<short>`", "rwb-case", "rwb-debtsale"],
    ["Schema and login", "`rwb_<short with _>`; one login per service, the same name as the schema", "rwb_case",
     "rwb_debtsale"],
    ["REST base", "`/api/recovery/<short>/v1` behind gateway-bff", "/api/recovery/case/v1",
     "/api/recovery/debtsale/v1"],
    ["Kafka topic", "`rwb.<short>.events.v1`", "rwb.case.events.v1", "rwb.debtsale.events.v1"],
    ["Retry and dead-letter topics", "`rwb.<short>.events.v1` plus `.retry.1m`, `.retry.10m`, `.retry.1h` and "
     "`.dlt`", "rwb.case.events.v1.dlt", "rwb.debtsale.events.v1.dlt"],
    ["Event names", "`rwb.<short>.<Event>.v1`", "rwb.case.CaseCreated.v1", "rwb.debtsale.LotAwarded.v1"],
    ["Temporal task queue", "`rwb-<short>` in namespace rwb-recovery", "rwb-case", "rwb-debtsale"],
    ["Java package", "`th.co.scb.ace.workbench.recovery.<short without hyphen>`",
     "th.co.scb.ace.workbench.recovery.case", "th.co.scb.ace.workbench.recovery.debtsale"],
    ["Service epic", "`RWB-SVC-<code>`", "RWB-SVC-P3", "RWB-SVC-S6"],
    ["Story scope", "The service code prefixes every story ID", "RWB-P3-E1018-APP", "RWB-S6-E4011-APP"],
    ["Decision record", "Local record in the service schema plus DecisionRecorded on rwb.decision-record.v1",
     "same", "same"],
]))
a("")
a("The event name pattern in the table is the documented rule; the event catalogue continues to name events by "
  "short name (CaseCreated, LotAwarded) and the topic carries the version. Both forms appear in this catalogue, and "
  "the topic is always named.")
a("")

a("# 6. Service detail")
a("")
a("One section per service, in Ownership Map order. Each section has the identity table, the contract table by "
  "call type, and the resources the service owns in its own schema. A row marked Out under Temporal is a call the "
  "service makes to another service on that service's queue.")
a("")

n = 0
for s in D.SVC:
    n += 1
    a(f"## 6.{n} {s['code']} rwb-{s['short']} — {s['name']}")
    a("")
    a(tbl(["Item", "Value"], [
        ["Service code", s["code"]],
        ["Service", "rwb-" + s["short"]],
        ["Service name", s["name"]],
        ["Wave (Arch v5)", s["wave"]],
        ["Service epic", f"RWB-SVC-{s['code']}"],
        ["Schema", s["schema"]],
        ["Login", s["schema"]],
        ["REST base", s["base"]],
        ["Kafka topic", s["topic"]],
        ["Retry and dead-letter topics", retry(s["topic"])],
        ["Temporal task queue", s["queue"]],
        ["Java package", s["pkg"]],
        ["Owns (Arch v5 slide 41)", s["owns"]],
        ["First API path (Arch v5 slide 41)", s["first"]],
        ["Status", "Draft"],
    ]))
    a("")
    a("**Contract by call type**")
    a("")
    rest_in = "; ".join(s["rest_in"]) if s["rest_in"] else "None."
    rest_out = "; ".join(f"{k}: {v}" for k, v in s["rest_out"]) if s["rest_out"] else "None."
    pub = "; ".join(s["pub"] + ["DecisionRecorded (rwb.decision-record.v1)"])
    con = "; ".join(s["con"]) if s["con"] else "None."
    tmp_in = "; ".join(provided(s)) if provided(s) else "None."
    tmp_out = "; ".join(outward(s)) if outward(s) else "None."
    a(tbl(["Call type", "Provided", "Consumed"], [
        ["REST", rest_in, rest_out],
        ["Kafka", pub, con],
        ["Temporal", tmp_in, tmp_out],
        ["File", s["files"], "None."],
        ["SQL view", "None.", "30 recovery.v_ace_* views, SELECT only." if s["code"] == "P1" else "None."],
    ]))
    a("")
    a("**Resources owned in " + s["schema"] + "**")
    a("")
    rs = resources(s["code"])
    if rs:
        a(tbl(["Table", "Ownership basis"], [[t, D.RULED.get(t, "Ownership Map v1, Tables sheet")] for t in rs]))
    else:
        a(f"The Ownership Map v1 holds no table for this service, although Architecture v5 slide 41 names "
          f"\"{s['owns']}\". TSD S1 Valuation and route v2 T3.1 names one table for these resources, `valuation` "
          f"(NEW); neither the Ownership Map v1 nor the Physical Schema v6 has such a table. " + D.PH[1] + ".")
    a("")
    if s["code"] == "P8":
        a("The Ownership Map v1 holds one table for P8 (`proceeds`). Architecture v5 slide 41 also names fees, "
          "bookings and posting files, and TSD P8 Payments and posting v2 T3.1 names `payment_match_rule` (NEW); "
          "none of these has a row in the Ownership Map v1 or a table in the Physical Schema v6. " + D.PH[2] + ".")
        a("")
    a("**Notes**")
    a("")
    a("- " + s["extra"])
    if s["code"] == "P7":
        a("- `ApprovalDecided` is published on rwb.decision.events.v1; the Architecture v5 event catalogue names no "
          "consumer for it. " + D.PH[6] + ".")
    if s["code"] == "P9":
        a("- `ReportPublished` is published on rwb.reporting.events.v1; the Architecture v5 event catalogue names "
          "no consumer for it. " + D.PH[6] + ".")
    a("")

a("# 7. Resource ownership")
a("")
a("The tables of the current recovery schema are split across the 19 service schemas. The Ownership Map v1 "
  "assigns every table, and the counts below are the rows of its Tables sheet. Six further tables are library "
  "objects that the template creates in every service schema, so they are owned once by the platform library "
  "(PLT) and instantiated 19 times.")
a("")
rows = []
for s in D.SVC:
    rs = resources(s["code"])
    rows.append([s["code"], "rwb-" + s["short"], s["schema"], len(rs),
                 ", ".join(rs) if rs else D.PH[1]])
rows.append(["PLT", "platform library", "every rwb_* schema", len(resources("PLT")), ", ".join(resources("PLT"))])
a(tbl(["Code", "Service", "Schema", "Tables", "Tables owned"], rows))
a("")
a(f"Totals: {sum(len(resources(s['code'])) for s in D.SVC)} business tables across the 19 services, "
  f"{len(resources('PLT'))} library tables instantiated in every schema, and one schema and login per service.")
a("")
a("Rules that hold for every table (Arch v5 slide 29):")
a("")
a("- A service writes only its own schema and has no grant on any other schema.")
a("- No cross-schema joins, views or foreign keys. Services hold each other's IDs and use contracts for "
  "everything else.")
a("- Each service runs its own Flyway migrations in its own pipeline; a boundary test in every build fails on any "
  "cross-schema reference.")
a("- Each login goes through its own PgBouncer pool with a connection cap and a statement timeout.")
a("- Only rwb_source_data has SELECT on the 30 recovery.v_ace_* views.")
a("")

a("# 8. Service-to-service call summary")
a("")
a("The call types below are the engineering standards of Architecture v5 slides 10 to 12, applied to every "
  "service in section 6. A service never mixes them: a REST call answers a person, an event announces a fact, a "
  "Temporal call commands a step, a file moves bulk data, and only rwb-source-data reads the ACE views.")
a("")
a(tbl(["Call type", "Where it is used", "Contract", "Failure handling", "Source"], [
    ["REST", "A person waits for the answer: gateway-bff to the owner, one hop, in parallel for composite screens",
     "OpenAPI 3.1, /v1 in the path", "2 s timeout, one GET retry with jitter, circuit breaker and bulkhead per "
     "downstream, RFC 9457 problem details", "Arch v5 slides 10, 11, 13"],
    ["Kafka event", "A fact others may react to; never a command", "AsyncAPI 3.0, CloudEvents 1.0 binary mode, JSON "
     "Schema registry BACKWARD", "Outbox, inbox dedupe, retry 1 min, 10 min, 1 h then .dlt with an alert and a "
     "replay tool", "Arch v5 slides 11, 22, 42, 43"],
    ["Temporal", "A step in another service or a long process; a child workflow per stage",
     "Typed activity and workflow interface in a contract jar on queue `rwb-<svc>`", "Typed failures, non-retryable "
     "list, start-to-close per activity, saga undo before the pivot", "Arch v5 slides 11, 23, 24, 25, 26"],
    ["File", "Bulk data or a party outside the bank", "Manifest: fileId, batchId, sha256, record count; SAS link "
     "open for 15 minutes", "FileFailed event, operator retry, checksum on receipt", "Arch v5 slide 11"],
    ["SQL view", "Reading ACE data, rwb-source-data only", "30 recovery.v_ace_* views (ADR-010)",
     "5 s statement timeout; mapped to domain errors by P1", "Arch v5 slides 11 and 29"],
]))
a("")
a("Rules that the call types enforce (Arch v5 slide 13): route services reach the shared capabilities through "
  "Temporal, never REST; only rwb-source-data touches ACE's tables; rwb-decision and rwb-reporting listen widely "
  "and call almost nobody; the case router in rwb-case turns events into signals and never calls another service "
  "directly for a business step.")
a("")

a("# 9. What every service must provide")
a("")
a("A service is conformant when all of the following are true. The same list is the Definition of Done in the "
  "Service Template Specification v1.")
a("")
a(tbl(["#", "Conformance rule", "Tested by"], [
    ["1", "Code, name, schema, login, REST base, topic, retry and dead-letter topics, task queue and Java package "
          "follow section 5 exactly", "Template conformance test in the build"],
    ["2", "The service is built from the service template and the shared libraries: Spring Boot, outbox relay, "
          "inbox, Temporal worker, payload codec, OpenTelemetry, contract tests", "Pipeline gate"],
    ["3", "The OpenAPI 3.1 contract, the AsyncAPI 3.0 contract and the activity contract jar are published before "
          "the code", "Contract test in every build"],
    ["4", "Every write and the event it produces are one local transaction in the service's own schema",
     "Outbox test"],
    ["5", "Every consumed event is deduplicated through processed_event in the same transaction as the change",
     "Inbox test"],
    ["6", "The boundary test fails on any cross-schema reference", "Architecture test"],
    ["7", "Every decision writes a local, hash-linked decision record and publishes DecisionRecorded",
     "Decision record test"],
    ["8", "Rules are evaluated in an activity, under 300 ms, with the package version in the record", "Rules test"],
    ["9", "Traces, metrics and logs go to OpenTelemetry; /health and /metrics exist", "Platform check"],
    ["10", "The service owns a contract story (CON) in its service epic before any build story starts",
     "Story set check"],
]))
a("")

a("# 10. Open points")
a("")
a(tbl(["ID", "Point", "Effect in this catalogue", "Owner role"], [
    ["CG-B-ARCH-SVC-1", "The Ownership Map v1 holds no table for rwb-valuation although Architecture v5 names "
     "valuations, the D6 route decision and the route agent output; TSD S1 v2 names table valuation (NEW)",
     "Section 6.11 carries the placeholder", "Solution architect"],
    ["CG-B-ARCH-SVC-2", "The Ownership Map v1 holds only proceeds for rwb-payment although Architecture v5 names "
     "fees, bookings and posting files; TSD P8 v2 names payment_match_rule (NEW)",
     "Section 6.8 carries the placeholder", "Solution architect"],
    ["CG-B-ARCH-SVC-6", "The event catalogue does not name the consumers of ApprovalDecided or ReportPublished",
     "Section 6.6 and 6.9 carry the placeholder", "Solution architect"],
    ["CG-B-ARCH-SVC-9", "No earlier Service Catalog exists, so v1 carries no inherited IDs, numbers or dates",
     "Version 1, status Draft; the change log row is the first", "Delivery lead"],
    ["CG-B-ARCH-SVC-10", "The API Specification v4 paths are the monolith paths, while this catalogue states the "
     "per-service base; the per-service operations are rewritten in API Specification v5",
     "Section 6 states the Architecture v5 contract and the map's ownership; the operation list is left to API "
     "Specification v5", "Solution architect"],
]))
a("")
a("The five open points on the template side are in the Service Template Specification v1 §21: CG-B-ARCH-SVC-3 "
  "(stack versions), CG-B-ARCH-SVC-4 (repository name and location), CG-B-ARCH-SVC-5 (chart, release and "
  "registry), CG-B-ARCH-SVC-7 (decision_record in every schema) and CG-B-ARCH-SVC-8 (pipeline tool).")
a("")
a("The full text of every gap and assumption is in the Gap Register and the Assumptions Register (folder 23). "
  "Candidate rows are in `_work/msr/gaps/B-ARCH-SVC.jsonl` and `_work/msr/assumptions/B-ARCH-SVC.jsonl`.")
a("")

a("# 11. Change log")
a("")
a(tbl(["Version", "Date", "Change", "Detail"], [
    ["1", "22 November 2026", f"D-RCV-60 microservice realignment, {TOOL}",
     "First Service Catalog: 19 services, 19 schemas and logins, 19 topics with retry and dead-letter topics, 19 "
     "task queues, the resources of the Ownership Map v1, and the per-service contract by call type."],
]))
a("")

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("WROTE", OUT, len(L), "blocks")

# ---------------------------------------------------------------- workbook source (md -> xlsx)
X = []
x = X.append


def xtbl(head, rows):
    X.extend(tbl(head, rows).splitlines())


x("## Read me")
x("")
xtbl(["Item", "Value"], [
    [HDR.splitlines()[0], ""],
    [HDR.splitlines()[1], ""],
    ["Document", "Recovery Workbench Service Catalog v1"],
    ["Version", "1"],
    ["Date", "22 November 2026"],
    ["Decision", "D-RCV-60 microservice realignment"],
    ["Tool", TOOL],
    ["Status", "Draft"],
    ["Change log", f"1, 22 November 2026, D-RCV-60 microservice realignment, {TOOL}"],
    ["Sheets", "Services; Resources; REST operations; Events published; Events consumed; Workflows and schedules; "
               "Naming; Waves; Call types"],
    ["Source of record", "Recovery Workbench Architecture v5 Text Extract v1 (slides 13 to 20 and 41 to 44); "
                         "Recovery Workbench Microservice Ownership Map v1; Recovery Workbench Temporal and Drools "
                         "Design Text Extract v1"],
])
x("")
x("## Services")
x("")
xtbl(["Code", "Service", "Name", "Wave", "Service epic", "Schema", "Login", "REST base", "Kafka topic",
      "Retry and DLT topics", "Task queue", "Java package", "First API path", "Owns (Arch v5 slide 41)", "Status"],
     [[s["code"], "rwb-" + s["short"], s["name"], s["wave"], f"RWB-SVC-{s['code']}", s["schema"], s["schema"],
       s["base"], s["topic"], retry(s["topic"]), s["queue"], s["pkg"], s["first"], s["owns"], "Draft"]
      for s in D.SVC])
x("")

x("## Resources")
x("")
res_rows = []
for s in D.SVC:
    for t in resources(s["code"]):
        res_rows.append([s["code"], "rwb-" + s["short"], s["schema"], t,
                         D.RULED.get(t, "Ownership Map v1, Tables sheet")])
res_rows.append(["S1", "rwb-valuation", "rwb_valuation", D.PH[1],
                 "Architecture v5 slide 41 names valuations, the D6 route decision and the route agent output; the "
                 "Ownership Map v1 has no row and the Physical Schema v6 has no table"])
res_rows.append(["P8", "rwb-payment", "rwb_payment", D.PH[2],
                 "Architecture v5 slide 41 names fees, bookings and posting files; TSD P8 v2 names "
                 "payment_match_rule; neither source has a row in the Ownership Map v1"])
for t in resources("PLT"):
    res_rows.append(["PLT", "platform library", "every rwb_* schema", t,
                     D.RULED.get(t, "Ownership Map v1, Tables sheet")])
xtbl(["Code", "Service", "Schema", "Table", "Ownership basis"], res_rows)
x("")

x("## REST operations")
x("")
x("Operations provided by each service, as named in Architecture v5 slides 14 to 20, with the per-service base of "
  "Template and Rules §R4. The paths in API Specification v4 are the monolith paths; the per-service operation "
  "list is rewritten in API Specification v5 (CG-B-ARCH-SVC-10).")
x("")
rest_rows = []
for s in D.SVC:
    for op in s["rest_in"]:
        m, _, p = op.partition(" ")
        bare = p.split(" (")[0]
        full = (s["base"] + bare) if bare.startswith("/") and not bare.startswith("/partner/") else bare
        rest_rows.append([s["code"], "rwb-" + s["short"], m, p, full, "Architecture v5 slides 14 to 20"])
xtbl(["Code", "Service", "Method", "Path (Arch v5)", "Full path", "Source"], rest_rows)
x("")

x("## Events published")
x("")
ev_rows = []
for s in D.SVC:
    for e in s["pub"] + ["DecisionRecorded"]:
        prod, topic = D.EV_TOPIC[e]
        cons = D.CONSUMERS.get(e) or D.PH[6]
        ev_rows.append([s["code"], "rwb-" + s["short"], e, topic, cons, prod])
xtbl(["Code", "Service", "Event", "Topic", "Consumers", "Producer (catalogue)"], ev_rows)
x("")

x("## Events consumed")
x("")
con_rows = []
for s in D.SVC:
    for e in s["con"]:
        if e.startswith("All business"):
            con_rows.append([s["code"], "rwb-" + s["short"], e, "all business-event topics", "all 19"])
        else:
            prod, topic = D.EV_TOPIC.get(e, ("not named", ""))
            con_rows.append([s["code"], "rwb-" + s["short"], e, topic or D.PH[6], prod])
xtbl(["Code", "Service", "Event", "Producer topic", "Producer"], con_rows)
x("")

x("## Workflows and schedules")
x("")
wf_rows = []
for s in D.SVC:
    for kind, note in s["tmp"]:
        wf_rows.append([s["code"], "rwb-" + s["short"], "Outward call" if kind == "Out" else kind, note, s["queue"],
                        "Architecture v5 slides 14 to 20 and 44"])
wf_rows.append(["PLT", "platform", "Schedule", "Stuck workflow scan every 5 minutes (JOB-21); platform smoke 06:00 "
                "(JOB-22), starts PlatformSmokeWorkflow", "rwb-platform", "Architecture v5 slide 44"])
wf_rows.append(["PLT", "platform", "Library", "Outbox relay every minute (JOB-11) in every service; durable timers "
                "replace the 5-minute timer check (JOB-05, retired)", "every rwb-<svc>",
                "Architecture v5 slide 44; Ownership Map v1, Jobs sheet"])
xtbl(["Code", "Service", "Type", "Item", "Task queue", "Source"], wf_rows)
x("")

x("## Naming")
x("")
xtbl(["Element", "Rule", "Example"], [
    ["Service code", "P1 to P10, S1 to S9", "P3"],
    ["Service name", "rwb-<short>", "rwb-case"],
    ["Schema and login", "rwb_<short with _>", "rwb_case"],
    ["REST base", "/api/recovery/<short>/v1", "/api/recovery/case/v1"],
    ["Kafka topic", "rwb.<short>.events.v1", "rwb.case.events.v1"],
    ["Retry and dead-letter topics", "rwb.<short>.events.v1.retry.1m, .retry.10m, .retry.1h, .dlt",
     "rwb.case.events.v1.dlt"],
    ["Event names", "rwb.<short>.<Event>.v1", "rwb.case.CaseCreated.v1"],
    ["Temporal task queue", "rwb-<short>", "rwb-case"],
    ["Java package", "th.co.scb.ace.workbench.recovery.<short without hyphen>",
     "th.co.scb.ace.workbench.recovery.case"],
    ["Service epic", "RWB-SVC-<code>", "RWB-SVC-P3"],
])
x("")

x("## Waves")
x("")
xtbl(["Wave", "Services", "Service epics", "Gate"], [
    ["0", "None (platform only)", "RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, "
     "RWB-PLT-OBS", "Template accepted; 19 logins created; topics exist"],
    ["1", "P1, P2, P3, P4, P5, P6, P7, P9, P10", "RWB-SVC-P1 to RWB-SVC-P7, RWB-SVC-P9, RWB-SVC-P10",
     "BOT approval before Wave 1 go-live, if required (FPG 19/2560 cl. 5.5)"],
    ["2", "P8, S2, S5, S8", "RWB-SVC-P8, RWB-SVC-S2, RWB-SVC-S5, RWB-SVC-S8", "Wave 1 in production"],
    ["3", "S1, S3, S4, S6", "RWB-SVC-S1, RWB-SVC-S3, RWB-SVC-S4, RWB-SVC-S6", "Wave 2 in production"],
    ["4", "S7, S9", "RWB-SVC-S7, RWB-SVC-S9", "Wave 3 in production"],
])
x("")

x("## Call types")
x("")
xtbl(["Call type", "Use when", "Contract", "Failure handling", "Source"], [
    ["REST", "A person waits for the answer", "OpenAPI 3.1, /v1 in the path",
     "2 s timeout, one GET retry with jitter, circuit breaker and bulkhead, RFC 9457 problem details",
     "Architecture v5 slides 10, 11"],
    ["Kafka event", "A fact others may react to", "AsyncAPI 3.0, CloudEvents 1.0 binary mode, JSON Schema BACKWARD",
     "Outbox, inbox dedupe, retry 1 min, 10 min, 1 h then .dlt, replay tool", "Architecture v5 slides 11, 22"],
    ["Temporal", "A step in another service, or a long process",
     "Typed activity and workflow interface in a contract jar", "Typed failures, non-retryable list, saga undo",
     "Architecture v5 slides 11, 23 to 26"],
    ["File", "Bulk data, or a party outside the bank", "Manifest: fileId, batchId, sha256, record count",
     "FileFailed event, operator retry, checksum", "Architecture v5 slide 11"],
    ["SQL view", "Reading ACE data, rwb-source-data only", "30 recovery.v_ace_* views (ADR-010)",
     "5 s statement timeout", "Architecture v5 slides 11, 29"],
])
x("")

XMD.write_text("\n".join(X) + "\n", encoding="utf-8")
print("WROTE", XMD, len(X), "blocks")
