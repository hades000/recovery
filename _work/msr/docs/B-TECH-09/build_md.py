"""Write the full text of the Observability and Monitoring Design v4 as Markdown.

Every per-service row is generated from the Ownership Map v1 Services sheet, so the code,
service, wave, schema, topic and task queue of each of the 19 rows are copied, not typed.
"""
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[4]
MAP = ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx"
OUT = Path(__file__).resolve().parent / "Recovery Workbench Observability and Monitoring Design v4.md"

wb = openpyxl.load_workbook(MAP, read_only=True)
rows = list(wb["Services"].iter_rows(values_only=True))
HEAD = rows[0]
SERVICES = [dict(zip(HEAD, r)) for r in rows[1:] if r[0]]
assert len(SERVICES) == 19, len(SERVICES)


def code(s):
    return s["Code"]


def name(s):
    return s["Service"]


def owner(s):
    return f'{s["Code"]} {s["Service"]}'


COMMON = "Service, Outbox, Decision log, Temporal, Rules"

# panels that only the service that owns the object carries (source section 1 areas)
EXTRA = {"P1": "Loads, Data", "P3": "Cases", "P10": "Agents"}


def table(header, body):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in body]
    return "\n".join(out)


L = []
A = L.append

A("SCB Collections and Recovery. Henka Group, 22 November 2026.")
A("(C) Siam Commercial Bank and Henka Pte Ltd")
A("")
A("Recovery Workbench")
A("")
A("Observability and monitoring design")
A("")
A(table(["Item", "Detail"], [
    ["Document", "Recovery Workbench observability and monitoring design"],
    ["Version", "4"],
    ["Date", "22 November 2026"],
    ["Change", "4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    ["Prepared by", "Henka Group"],
    ["Structure", "arc42 crosscutting concepts"],
    ["Supersedes", "3, 16 November 2026"],
    ["Source version", "3, 16 November 2026"],
    ["Decision", "D-RCV-60 microservice realignment; ADR-023 observability per service"],
    ["Tool", "T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60"],
    ["Status", "Draft. No approval is recorded for this version (ASM-B-TECH-09-10)"],
]))
A("")
A("# Change log")
A("")
A(table(["Version", "Date", "Change"], [
    ["4", "22 November 2026",
     "4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. "
     "One dashboard and one alert set per service, 19 of each, with one row per service for the measures, the "
     "alerts, the dashboards and the run books. Every section, ID, number and date of version 3 is kept"],
    ["3", "16 November 2026",
     "v3, 16 November 2026, D-RCV-36: Temporal server and worker metrics, a workflow dashboard, three workflow "
     "alerts with run books, and Drools rule package metrics (E2-037)"],
]))
A("")
A("# 1. What is measured")
A("")
A(table(["Area", "Measures", "Source"], [
    ["Service", "Request rate, errors, latency at the 50th and 95th percentile per endpoint",
     "Traces and metrics in Log Analytics"],
    ["Loads", "Start, end, rows, checks passed and failed, business date", "Job monitor"],
    ["Jobs", "Runs, duration, missed runs", "Quartz job table"],
    ["Outbox", "Items waiting, oldest item, retries, exception queue size", "Outbox table"],
    ["Decision log", "Entries a day, write failures, chain check result", "Decision log"],
    ["Agents", "Calls, latency, fallbacks, guardrail failures, cost", "Agent runs"],
    ["Cases", "Open cases, cases in exception queues, breached service levels", "Workbench"],
    ["Data", "Stale data products, reconciliation breaks", "Data quality console"],
    ["Temporal", "Workflow failed count, workflow task timeouts, schedule-to-start latency, activity failures "
     "and worker poll failures", "Temporal server and worker metrics in Prometheus"],
    ["Rules", "KieBase compile count, evaluation count and latency, cache hit ratio, NoPackageInForce count",
     "Drools runtime metrics in Prometheus"],
    ["Kafka", "Consumer lag per consumer group and partition, retry and dead-letter depth, outbox items "
     "waiting and oldest item, per service", "Kafka and Prometheus metrics; the outbox table of each service"],
]))
A("")
A("The Kafka row is the only area version 4 adds to this table, because the target architecture has one topic "
  "per service (Architecture v5 slides 9, 21 and 41; ADR-015; DP-09). The ten rows of version 3 are unchanged.")
A("")
A("In version 4 every row is read with the service as the unit. The Workbench is 19 services inside the ACE "
  "platform (Architecture v5 slides 5, 33 and 41; ADR-013), and each one has an api deployment, a worker "
  "deployment, its own schema and login, its own topic rwb.<short>.events.v1, its own task queue rwb-<short> "
  "and its own embedded Drools engine (Architecture v5 slides 29, 33 and 41; Temporal and Drools design slide "
  "11). A measure that version 3 takes once for the whole Workbench is therefore taken once per service. A "
  "measure whose object only one service owns stays single and sits on that service: Cases on P3 rwb-case, "
  "Agents on P10 rwb-agent, Data on P1 rwb-source-data. The measures themselves, their "
  "names and their sources do not change.")
A("")
A("## 1.1 The 19 measured units")
A("")
A("The 19 rows are the Ownership Map v1 Services sheet; code, service, wave, schema, topic and task queue are "
  "copied from it. The owner of every measure of a service is that service.")
A("")
A(table(["Code", "Service", "Wave", "Schema", "Topic", "Task queue", "Owner of its measures"],
        [[code(s), name(s), s["Wave"], s["Schema"], s["Topic"], s["Queue"], owner(s)] for s in SERVICES]))
A("")
A("The namespace is rwb-recovery for all 19 task queues, and the REST base of a service is "
  "/api/recovery/<short>/v1 behind gateway-bff (Architecture v5 slides 8 and 41; Rules v1 R4). The platform "
  "parts that are not one of the 19 - gateway-bff and its Redis session, the Temporal cluster, Kafka, the "
  "bank Airflow, the observability stack - keep one measurement each and are owned by the platform team, not "
  "by a service (Architecture v5 slides 4 and 41).")
A("")
A("## 1.2 What each area covers after the split")
A("")
A(table(["Area", "Version 3", "Version 4", "Read from"], [
    ["Service", "The Workbench API, per endpoint",
     "The api deployment and the worker deployment of each of the 19 services",
     "Traces and metrics in Log Analytics, labelled with the service"],
    ["Loads", "The Workbench load, start to end",
     "P1 rwb-source-data only: readiness of the ACE data of the business date. Recovery loads no source data "
     "(Architecture v5 slide 30), so there is no Workbench load to measure",
     "P1 job run log and freshness; AceDataReady and AceDataLate (Architecture v5 slide 31)"],
    ["Jobs", "Runs, duration and missed runs of the Quartz jobs",
     "The Temporal Schedules and event-started workflows of the owning service; JOB-05 is retired and there "
     "is no shared Quartz table (Architecture v5 slide 44; ADR-016; DP-10)",
     "Temporal metrics and the job catalogue of P2 rwb-integration"],
    ["Outbox", "One outbox for the Workbench",
     "The outbox of each service's own schema, and the topic of that service",
     "The outbox table of rwb_<schema>; Kafka consumer lag"],
    ["Decision log", "One decision log",
     "The local decision record of each service, then the central ledger of P7 rwb-decision "
     "(Architecture v5 slide 28; ADR-022; DP-03)",
     "decision_record of each rwb_<schema>; rwb_decision for the ledger"],
    ["Agents", "Agent runs of the Workbench", "P10 rwb-agent only", "rwb_agent"],
    ["Cases", "The Workbench case list", "P3 rwb-case only", "rwb_case"],
    ["Data", "The data quality console",
     "P1 rwb-source-data for the data products, freshness and reconciliation",
     "rwb_source_data"],
    ["Temporal", "Server and worker metrics of one runtime",
     "The metrics of task queue rwb-<short> of each service, in one shared cluster and namespace "
     "(Architecture v5 slide 24; ADR-016)",
     "Temporal server and worker metrics in Prometheus"],
    ["Rules", "One Drools runtime",
     "The embedded engine of each service, with the registry and the approval in P7 rwb-decision "
     "(Architecture v5 slide 27; ADR-017; DP-04)",
     "Drools runtime metrics in Prometheus, per service"],
    ["Kafka", "Not measured in version 3",
     "The topic, the consumer group and the retry and dead-letter topics of each service",
     "Kafka metrics; the outbox of the producing service"],
]))
A("")
A("# 2. Alerts")
A("")
A(table(["Alert", "Raised when", "Goes to", "Within"], [
    ["Load failed", "A check refuses a load", "Data steward, platform administrator", "15 minutes"],
    ["Load late", "The load has not arrived by 07:00", "Data steward", "15 minutes"],
    ["Decision log write failed", "Any failure", "Platform administrator; incident", "Immediately"],
    ["Hash chain break", "Daily check fails", "Compliance, internal audit", "Same day"],
    ["Exception queue growing", "More than 50 items or older than one day", "Platform administrator", "1 hour"],
    ["Error rate", "5xx above 1 percent for 5 minutes", "Platform administrator, tech leads", "5 minutes"],
    ["Latency", "95th percentile above 2 seconds for 15 minutes", "Platform administrator", "15 minutes"],
    ["Agent fallbacks", "Above 10 percent of calls in an hour", "Risk and model risk officer", "1 hour"],
    ["Reconciliation break", "Any account at 90 days past due without a case", "Data steward", "Next morning"],
    ["Failed workflow", "A workflow execution is failed (MSG-P3-037)", "Platform administrator", "5 minutes"],
    ["Stuck workflow", "A workflow has no progress for temporal.stuck.hours (=24)", "Platform administrator",
     "1 hour"],
    ["Schedule-to-start latency", "Above its threshold for 15 minutes", "Platform administrator", "15 minutes"],
    ["Rule package compile failed", "A rule package load fails the compile check (MSG-P3-027 with check compile)",
     "Center of excellence analyst, platform administrator", "15 minutes"],
]))
A("")
A("Alert thresholds are reference data and change by load. Each alert names one owner; the owner's backup "
  "receives it when the owner is absent.")
A("")
A("## 2.1 The 13 alerts read per service")
A("")
A("The 13 alerts and their thresholds and windows are unchanged. What changes is the unit they are evaluated "
  "on: the metric is read with the service as the unit and the alert names the service, so the Workbench gets "
  "19 instances of each alert whose object every service has, and one instance of each alert whose object only "
  "one service owns. The owner of an alert is the service that owns the signal, taken from the Ownership Map "
  "v1; the recipient roles of the source stay as they are.")
A("")
A(table(["Alert", "Read per service as", "Owner", "Within"], [
    ["Error rate", "5xx above 1 percent for 5 minutes on the service's own API and its consumers",
     "The service that raises it (2.2)", "5 minutes"],
    ["Latency", "95th percentile above 2 seconds for 15 minutes on the service's own API",
     "The service that raises it (2.2)", "15 minutes"],
    ["Exception queue growing",
     "More than 50 items or older than one day in the service's outbox, retry topic or dead-letter topic",
     "The service that raises it (2.2)", "1 hour"],
    ["Decision log write failed", "Any failure writing the local decision record of the service",
     "The service; P7 rwb-decision for the central ledger", "Immediately"],
    ["Hash chain break", "The daily check fails on the local chain of the service",
     "The service; P7 rwb-decision for the central ledger", "Same day"],
    ["Failed workflow", "A workflow execution on task queue rwb-<short> is failed (MSG-P3-037)",
     "The service that owns the queue", "5 minutes"],
    ["Stuck workflow", "A workflow on task queue rwb-<short> has no progress for temporal.stuck.hours (=24)",
     "The service that owns the queue", "1 hour"],
    ["Schedule-to-start latency", "Above its threshold for 15 minutes on task queue rwb-<short>",
     "The service that owns the Schedule", "15 minutes"],
    ["Rule package compile failed",
     "A rule package load fails the compile check in the owning service (MSG-P3-027 with check compile)",
     "The service that loads the package; P7 rwb-decision for the registry", "15 minutes"],
    ["Load failed", "A check refuses the ACE data product of the business date", "P1 rwb-source-data", "15 minutes"],
    ["Load late", "The ACE data product has not arrived by 07:00", "P1 rwb-source-data", "15 minutes"],
    ["Reconciliation break", "Any account at 90 days past due without a case", "P1 rwb-source-data", "Next morning"],
    ["Agent fallbacks", "Above 10 percent of calls in an hour on P10 rwb-agent", "P10 rwb-agent", "1 hour"],
]))
A("")
A("Not every alert has an instance in every service. Load failed, Load late and Reconciliation break have "
  "an instance only in P1 rwb-source-data, because the ACE data product, its freshness and the reconciliation "
  "are P1's (Architecture v5 slides 15 and 41). Agent fallbacks has an instance only in P10 rwb-agent. "
  "Schedule-to-start latency has an instance only where the service owns a Temporal Schedule in the job map: "
  "P3 rwb-case (JOB-06), P4 rwb-access (JOB-18), P5 rwb-document (JOB-17), P7 rwb-decision (JOB-14 and "
  "JOB-20), S5 rwb-asset (JOB-19) and S7 rwb-writeoff (JOB-16) (Architecture v5 slide 44).")
A("")
A("## 2.2 Alert ownership and routing")
A("")
A("The owner of an alert is the service that owns the signal. The recipient roles of section 2 do not change "
  "and are not replaced: the platform administrator stays the first recipient of a service-health alert, the "
  "data steward of a data alert, the risk and model risk officer of the agent alert, compliance and internal "
  "audit of a chain break, and the center of excellence analyst of a rule package alert. No source maps those "
  "role names to a role code; the only role codes in the source are RW-PLATADM and RW-COE, on the workflow "
  "dashboard row of section 3 (CG-B-TECH-09-6; ASM-B-TECH-09-6).")
A("")
A(table(["Alert scope", "Alerts", "Owner", "Escalation"], [
    ["Every service (19)", "Error rate, Latency, Exception queue growing, Decision log write failed, "
     "Hash chain break, Failed workflow, Stuck workflow, Rule package compile failed",
     "The service code of the Ownership Map v1", "Platform administrator; the run book names the next step"],
    ["Services with a Temporal Schedule", "Schedule-to-start latency (P3, P4, P5, P7, S5, S7)",
     "The service that owns the Schedule", "Platform administrator"],
    ["P1 rwb-source-data only", "Load failed, Load late, Reconciliation break", "P1 rwb-source-data",
     "Data steward; platform administrator"],
    ["P10 rwb-agent only", "Agent fallbacks", "P10 rwb-agent", "Risk and model risk officer"],
    ["P7 rwb-decision, as the second instance", "Decision log write failed, Hash chain break on the central "
     "ledger", "P7 rwb-decision", "Compliance, internal audit"],
]))
A("")
A("An alert names one service and one signal, so the same threshold crossing in two services opens two "
  "incidents, one per service, and never one incident for the Workbench.")
A("")
A("# 3. Dashboards")
A("")
A(table(["Dashboard", "For", "Shows"], [
    ["Service health", "Platform administrator, ACE team", "Availability, errors, latency, saturation"],
    ["Data health", "Data steward", "Loads, freshness, breaks, exceptions"],
    ["Work health", "Team managers", "Queues, caps, breached service levels, exception queues"],
    ["Agent health", "Risk and model risk officer", "Calls, fallbacks, acceptance, cost"],
    ["Workflow health (Grafana)", "Platform administrator, RW-PLATADM, RW-COE",
     "Temporal workflows by type and status; failed, stuck, schedule-to-start latency, activity failures and "
     "worker poll failures; KieBase compile count, evaluation count and latency, cache hit ratio and "
     "NoPackageInForce count. No personal data."],
]))
A("")
A("The workflow health dashboard is a Grafana dashboard fed by Prometheus. It shows counts and durations by "
  "workflow type and status, never a case identifier, account number, name or national ID. The same panels "
  "carry the Drools signals, so a rule package that fails to compile is visible next to the workflow that "
  "depends on it.")
A("")
A("## 3.1 One Service health dashboard per service")
A("")
A("The first row of the table above is the row that changes. Service health is not one dashboard for the "
  "Workbench: it is one dashboard per service, 19 in all, each reading only the metrics, traces and logs of "
  "that service and the numbers of the objects it owns (Architecture v5 slides 33 and 41; ADR-023). The four "
  "other dashboards stay as they are; each of their panels names the service that owns the number, so Work "
  "health reads the queue measures of P3 rwb-case, Data health reads the data products and the reconciliation "
  "result of P1 rwb-source-data, Agent health reads the runs of P10 rwb-agent and Workflow health reads one "
  "task queue per service.")
A("")
A("The panels of a per-service dashboard are the rows of section 1 that the service owns. Every one of the 19 "
  "has the same shape (Architecture v5 slide 33; Temporal and Drools design slide 11), so every one carries "
  "the five panel groups Service, Outbox, Decision log, Temporal and Rules; three objects sit on one service "
  "each and add their panel group there: Loads and Data on P1, Cases on P3 and Agents on P10. "
  "The dashboard name, the panel order, the refresh interval and the "
  "saved query of a per-service dashboard are not fixed by any source (CG-B-TECH-09-1; CG-B-TECH-09-3; "
  "ASM-B-TECH-09-1), so this document fixes the panels and leaves the presentation to the dashboard baseline "
  "of RWB-PLT-N005-OPS.")
A("")
A(table(["Code", "Service", "Wave", "Panels of its dashboard", "Owner"],
        [[code(s), name(s), s["Wave"],
          COMMON + (", " + EXTRA[code(s)] if code(s) in EXTRA else ""), owner(s)] for s in SERVICES]))
A("")
A("No per-service dashboard shows a case identifier, account number, name or national ID. A panel that needs "
  "to follow one case uses the Temporal workflow ID, and the payload stays encrypted (Architecture v5 slide "
  "35; E2-038).")
A("")
A("# 4. Run books")
A("")
A("Every job, load and alert has a run book: what it does, how to check it, how to rerun it and who to call. "
  "Run books are written with the story that builds the job (RWB-E1-056).")
A("")
A("Each of the four new alerts has a run book: failed workflow, stuck workflow, schedule-to-start latency and "
  "rule package compile failure. A run book names the check, the query or link, the action, the escalation "
  "and the owner, and it is written with the story that builds the signal (RWB-E2-037).")
A("")
A("The Temporal server and worker run books are owned by RWB-E1-070 and RWB-E2-037. The rule package run book "
  "(compile failure at load and no package in force) is owned by RWB-E1-073.")
A("")
A("A workflow run book starts from the Temporal Web UI behind Entra ID, reads the history summary and the "
  "worker build ID, and never decodes a payload outside a break-glass session (RWB-E2-038).")
A("")
A("## 4.1 Which run book belongs to which service")
A("")
A("The four paragraphs above keep their ownership. The realignment adds the per-service split: because an "
  "alert now names a service, its run book does too, and the service that owns the signal is the owner of the "
  "run book. The DevOps team is the suggested owner of that work, and any team may pick up the story "
  "(Rules v1 R5.3).")
A("")
A(table(["Signal", "Run book", "Owner of the run book", "Story that writes it"], [
    ["Every alert of section 2.1, for one service", "The service run book of that service",
     "The service code of the Ownership Map v1; DevOps team suggested", "RWB-PLT-N005-OPS for the baseline, "
     "then the service's own OPS story"],
    ["Temporal server and worker signals: failed, stuck and schedule-to-start", "Temporal server and worker "
     "run books", "Platform team; P7 rwb-decision for the ledger instances",
     "RWB-PLT-E2037-APP; RWB-PLT-E2038-APP for the workflow run book steps (RWB-E2-038)"],
    ["Rule package compile failure and no package in force", "Rule package run book",
     "P7 rwb-decision, with the service that loads the package",
     "RWB-P7-E1073-APP, RWB-P3-E1073-APP, RWB-P6-E1073-APP, RWB-P2-E1073-APP (RWB-E1-073)"],
    ["Job and load signals, JOB-02 to JOB-22", "One run book per job",
     "The service that owns the job (Architecture v5 slide 44)",
     "RWB-PLT-E1056-OPS, then the service's own OPS story (RWB-E1-056)"],
    ["Workflow run book steps: Temporal Web UI, history summary, worker build ID, no decode outside break-glass",
     "Workflow run book", "Platform team", "RWB-PLT-E2038-APP (RWB-E2-038)"],
]))
A("")
A("# 5. Open points")
A("")
A(table(["Point", "Where it bites", "Row"], [
    ["The per-service dashboard name, panel order, refresh interval and saved query are not specified",
     "Section 3.1; built by RWB-PLT-N005-OPS", "CG-B-TECH-09-1, CG-B-TECH-09-3; ASM-B-TECH-09-1, "
     "ASM-B-TECH-09-3"],
    ["No source names the owner of a per-service dashboard or alert rule as a team", "Sections 2.2, 3.1, 4.1",
     "CG-B-TECH-09-2; ASM-B-TECH-09-2"],
    ["Metric and span names, labels, retention, sampling and the alert delivery channel are not specified",
     "Sections 1, 2.2, 3.1", "CG-B-TECH-09-3; ASM-B-TECH-09-3"],
    ["The Jobs row still reads the Quartz job table", "Sections 1.2, 2.1", "CG-B-TECH-09-4; ASM-B-TECH-09-4"],
    ["The decision log is local first and central second", "Sections 1.2, 2.1", "CG-B-TECH-09-5; "
     "ASM-B-TECH-09-5"],
    ["The alert recipient role names are not all mapped to a role code", "Section 2.2",
     "CG-B-TECH-09-6; ASM-B-TECH-09-6"],
    ["The rule package compile check names P3 while the registry is P7", "Section 2.1", "CG-B-TECH-09-7; "
     "ASM-B-TECH-09-7"],
    ["The Data health and Work health panels read objects of P1 and P3", "Section 3, 3.1",
     "CG-B-TECH-09-8; ASM-B-TECH-09-8"],
    ["The hash chain check now spans 19 local chains and one central ledger", "Section 2.1", "CG-B-TECH-09-9; "
     "ASM-B-TECH-09-9"],
]))
A("")
A("# Realignment changes in version 4 (D-RCV-60)")
A("")
A("The table records what version 4 changes, where, why and under which decision. Every other statement, "
  "table, ID, number and date of version 3 is unchanged.")
A("")
A(table(["#", "Section", "Version 3", "Version 4", "Decision and pattern"], [
    ["1", "1, 1.1, 1.2", "One set of measures for the Workbench",
     "The same 11 areas, read with each of the 19 services as the unit; one row per service", "ADR-013, ADR-023"],
    ["2", "1, 1.2", "No Kafka measure",
     "Kafka consumer lag, retry and dead-letter depth and outbox backlog per service", "ADR-015; DP-09"],
    ["3", "1.2", "Jobs measured from the Quartz job table",
     "Temporal Schedules and event-started workflows of the owning service; JOB-05 retired", "ADR-016; DP-10"],
    ["4", "1.2", "One decision log for the Workbench",
     "Local decision record in each service's schema, then the central ledger of P7 rwb-decision",
     "ADR-022; DP-03"],
    ["5", "2, 2.1", "13 alerts for the Workbench",
     "The same 13 alerts, each read per service, with the thresholds and windows of version 3 unchanged",
     "ADR-023"],
    ["6", "2.2", "One recipient list per alert",
     "The owner of the signal is the service code of the Ownership Map v1; the recipient roles stay as they are",
     "Rules v1 R5.3"],
    ["7", "3, 3.1", "One Service health dashboard",
     "One Service health dashboard per service, 19 in all; the four other dashboards stay and name the owning "
     "service on each panel", "ADR-023"],
    ["8", "3.1", "One dashboard for the whole Workbench",
     "The panels of a per-service dashboard are the section 1 areas its service owns: Loads and Data on P1, "
     "Cases on P3, Agents on P10", "ADR-013, ADR-023"],
    ["9", "4.1", "One set of run books for the Workbench",
     "One run book per alert and job of each service; RWB-E1-056, RWB-E1-070, RWB-E1-073, RWB-E2-037 and "
     "RWB-E2-038 keep their ownership", "ADR-023"],
    ["10", "Metadata", "Version 3, 16 November 2026, D-RCV-36",
     "Version 4, 22 November 2026, D-RCV-60; ADR-023 cited; status Draft (ASM-B-TECH-09-10)",
     "D-RCV-60; Rules v1 R8.1"],
]))
A("")
A("End of document. Version 4, 22 November 2026, D-RCV-60, T3 Code / OpenCode / DeepSeek v4.1 Flash.")

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("WROTE", OUT, len(L), "lines")
