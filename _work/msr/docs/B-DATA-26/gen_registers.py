"""Write the candidate gap and assumption rows for B-DATA-26 (renumbering is step D1)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GAPS = ROOT / "_work" / "msr" / "gaps" / "B-DATA-26.jsonl"
ASSUM = ROOT / "_work" / "msr" / "assumptions" / "B-DATA-26.jsonl"
SRC = "06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx"

gaps = [
    dict(
        id="CG-B-DATA-26-1",
        title="The forecast is written for one monolith and has no per-service volumes",
        source=SRC,
        section="All eight sheets (there is no service, topic or queue anywhere)",
        description=(
            "Version 3 measures one Workbench: one read path, one set of scheduled jobs and one database. Arch v5 cuts "
            "Recovery into 19 services, each with its own schema, REST base, Kafka topic and Temporal task queue, so the "
            "capacity plan needs a volume per service. The source has no such split and no service owner."),
        evidence=(
            "v3 Read path!A2 and C15 (the Workbench reads the views; three Workbench jobs); v3 has no column named "
            "service, topic or queue on any sheet. Recovery Workbench Architecture v5 Text Extract v1 line 45 (own "
            "schema, topic and task queue each), line 69 (19 services, own topic and queue), line 703 (topic per "
            "service) and lines 2880 to 2898 (slide 41 service catalogue); Architecture v5 slide 48 (A8) lines 3127 "
            "to 3179 (volumes and what needs to scale); ADR-013; ADR-014; DP-01; DP-14."),
        type="Conflict", area="Forecast and capacity", severity="P2", needed_by_wave="1",
        legacy_ref="NF-03; RWB-TE-009", owner_role="Data architecture team", asm="ASM-B-DATA-26-1",
        proposed=(
            "A new sheet, Service volumes, gives one row for each of the 19 services with its driver, the 2027 volume "
            "taken by formula from the existing sheets, the unit, the basis cell, its topic, its task queue and its "
            "consumers; the totals on Inputs, Monthly, Five years and Route activity do not change."),
        wp="B-DATA-26"),
    dict(
        id="CG-B-DATA-26-2",
        title="The read path gives every Workbench screen the recovery.v_ace_* views",
        source=SRC,
        section="Read path (A2, C16); Inputs!G7; Key (View read)",
        description=(
            "Version 3 says the Workbench reads ACE through recovery.v_ace_* views and that a view read is a SELECT by "
            "a screen or by the lake refresh. Arch v5 gives the 30 views to rwb-source-data alone, read-only, and makes "
            "every other service ask it; the lake refresh no longer exists. The four cells and the Key row therefore "
            "name the wrong reader."),
        evidence=(
            "v3 Read path!A2 (The Workbench reads ACE through recovery.v_ace_* views), Read path!C16 (data_product_load "
            "read through v_ace_batch_status), Inputs!G7 (read through v_ace_account) and Key!C10 (a SELECT by a screen "
            "or by the lake refresh). Recovery Workbench Architecture v5 Text Extract v1 line 707 (only rwb-source-data "
            "reads the 30 recovery.v_ace_* views) and lines 1113 to 1115 (P1 SQL: SELECT recovery.v_ace_*, 30 views); "
            "ADR-010; DP-05."),
        type="Conflict", area="Data access", severity="P2", needed_by_wave="1",
        legacy_ref="RWB-TE-009", owner_role="Data architecture team", asm="ASM-B-DATA-26-2",
        proposed=(
            "The four cells and the Key row say that rwb-source-data holds the one grant and reads the views on behalf "
            "of the screens and the workflows; the headline figures of the read path do not change."),
        wp="B-DATA-26"),
    dict(
        id="CG-B-DATA-26-3",
        title="The three scheduled Workbench jobs include a lake refresh that the target removes",
        source=SRC,
        section="Read path (row 15, Scheduled Workbench jobs)",
        description=(
            "Version 3 counts three scheduled Workbench jobs: outbound queue dispatch, lake refresh and case list "
            "reconciliation. Arch v5 removes the data lake, retires the shared Quartz tables and runs every job as a "
            "Temporal Schedule or an event-started workflow in the owning service, so the lake refresh has no "
            "replacement and the three jobs belong to three different services."),
        evidence=(
            "v3 Read path!B15 and C15 (3; outbound queue dispatch, lake refresh and case list reconciliation). "
            "Architecture v5 Text Extract v1 line 513 (no data lake or Power BI connection, INT-19/20 removed), line "
            "2296 (Temporal Schedules: rule promotion, measures, hash-chain check, smoke, rebalancing, WIN letters; the "
            "ACE shared Quartz tables are no longer used) and lines 2978 to 3002 (slide 44 job map: JOB-02, JOB-03, "
            "JOB-04, JOB-10); DP-10; DP-17; ADR-016."),
        type="Outdated", area="Scheduling", severity="P3", needed_by_wave="1",
        legacy_ref="NF-08; RWB-TE-009", owner_role="Solution architecture team", asm="ASM-B-DATA-26-3",
        proposed=(
            "The note names three jobs that exist in the target: case creation and allocation (JOB-02, JOB-03), "
            "reconciliation (JOB-04) and the WIN notice file (JOB-10), each a Schedule or an event-started workflow in "
            "its own service; the count of three and every figure stay as they are."),
        wp="B-DATA-26"),
    dict(
        id="CG-B-DATA-26-4",
        title="The forecast carries no Kafka topic, partition, retention or consumer figures",
        source=SRC,
        section="Whole workbook (no messaging sheet)",
        description=(
            "The source is a capacity forecast with no messaging content: no topic, partition count, replication "
            "factor, retention, record key, consumer group, retry or dead-letter setting, and no task queue. Arch v5 "
            "sets all of them, one topic and one queue per service plus the shared decision-record topic, so the "
            "document has to carry a second table that it never had. The event catalogue also names no consumer for "
            "ReportPublished."),
        evidence=(
            "v3 has eight sheets and none of them names a topic or a queue. Architecture v5 Text Extract v1 line 703 "
            "(12 partitions, replication factor 3, 7 days, key caseId, CloudEvents binary, outbox and inbox, retry "
            "1 min, 10 min, 1 h then .dlt), lines 245 to 246 (topic rwb.<name>.events.v1, task queue rwb-<name>), "
            "lines 2911 to 2963 (event catalogue) and line 1544 (tens of thousands of events a day); Temporal and "
            "Drools Design Text Extract v1 line 478 (one queue per service, 19) and line 520 (namespace rwb-recovery, "
            "KEDA on backlog); ADR-015; ADR-016; DP-09; DP-14."),
        type="Missing", area="Messaging", severity="P2", needed_by_wave="1",
        legacy_ref="NF-08", owner_role="DevOps team", asm="ASM-B-DATA-26-4",
        proposed=(
            "A new sheet, Topics and queues, lists the 19 service topics and the shared rwb.decision-record.v1 with "
            "partitions, replication, retention, record key, consumer groups, retry and dead letter, then the 19 task "
            "queues with their workflows, activities and Schedules, then the platform settings; the missing consumer of "
            "ReportPublished is carried as the placeholder."),
        wp="B-DATA-26"),
    dict(
        id="CG-B-DATA-26-5",
        title="No demand figure exists for payments, guarantee claims, partner instructions, the report read volume, the lots or the deviation share",
        source=SRC,
        section="Inputs (I01 to I34); Route activity",
        description=(
            "Several services own a driver that the forecast never counts. There is no payment count (rwb-payment), no "
            "guarantee or insurance claim count (rwb-guarantee), no partner instruction or result count (rwb-partner), "
            "no dashboard or report read count (rwb-reporting), no number of debt-sale lots (only accounts sold) and no "
            "share of cases that raise a deviation (rwb-deviation). Their per-service volumes cannot be calculated from "
            "the source without inventing one."),
        evidence=(
            "v3 Inputs rows I01 to I34 and Route activity rows 5 to 9 contain no such figure; the source counts cases, "
            "documents, interactions, decisions, rule evaluations, lawsuits, repossessions, letters, NPA sales, "
            "debt-sale accounts and users only. Architecture v5 Text Extract v1 lines 1236 to 1250 (P8 and S9 "
            "contracts), lines 1322 to 1332 (S3), lines 1397 to 1408 (S6 lots) and lines 1057 to 1063 (S8 screening)."),
        type="Missing", area="Forecast and capacity", severity="P2", needed_by_wave="2",
        legacy_ref="RWB-TE-009", owner_role="Data architecture team", asm="ASM-B-DATA-26-5",
        proposed=(
            "The row carries the §R9 placeholder instead of a figure, and the basis column states what the source does "
            "give: the run cadence (one per business day), the lot-based cadence, or the named stock."),
        wp="B-DATA-26"),
    dict(
        id="CG-B-DATA-26-6",
        title="Arch v5 states 3,110 new cases a month; the forecast divides the account inflow by 1.2",
        source=SRC,
        section="Inputs (I08 to I11); Monthly (column C); Five years (column C)",
        description=(
            "Arch v5 slide 48 and its notes state about 3,110 new cases a month, 64-74k documents a month and 283-318k "
            "rule evaluations a month. The forecast divides new accounts by the accounts-per-case assumption of 1.2, "
            "which gives about 2,980 cases a month, so its documents sit inside the slide's range while its decision "
            "entries and rule evaluations run slightly above it. The two sources do not agree on the case inflow."),
        evidence=(
            "v3 Inputs!I08 (accounts per case 1.2), Monthly!C5 (new accounts divided by Inputs!C12) and Five years!C5. "
            "Architecture v5 Text Extract v1 line 2433 (about 23,600 open cases today, 47,389 by 2031; 64-74k "
            "documents a month; 283-318k rule evaluations a month) and lines 3131 to 3144 (3,110 new cases a month; "
            "64-74k; 283-318k). R-PREC ranks the Arch v5 narrative above the data documents, but the forecast is the "
            "one artefact that holds the drivers."),
        type="Conflict", area="Forecast and capacity", severity="P3", needed_by_wave="1",
        legacy_ref="RWB-TE-009", owner_role="Data architecture team", asm="ASM-B-DATA-26-6",
        proposed=(
            "The forecast keeps its own formula and its own figures; the per-service rows and the cross-check block cite "
            "the slide 48 figure and state that it is rounded up, so a reader sees both numbers in one place."),
        wp="B-DATA-26"),
    dict(
        id="CG-B-DATA-26-7",
        title="Three scheduled Workbench jobs in the forecast against 21 jobs in the Arch v5 job map",
        source=SRC,
        section="Read path (row 15)",
        description=(
            "Version 3 counts three scheduled Workbench jobs. The Arch v5 job map runs JOB-02 to JOB-22 across the "
            "platform and the services, of which JOB-05 is retired; the two counts describe different things (jobs "
            "inside the Workbench then, jobs across 19 services and Airflow now) and the forecast does not say which "
            "scope its three belong to."),
        evidence=(
            "v3 Read path!B15 (3) and C15. Architecture v5 Text Extract v1 lines 2978 to 2997 (slide 44 job map, "
            "JOB-02 to JOB-22, JOB-05 retired, JOB-11 in every service, JOB-21 and JOB-22 on the platform), line 2296 "
            "and lines 3002 (each job in its owning service; Airflow owns only the cross-system edges)."),
        type="Ambiguous", area="Scheduling", severity="P3", needed_by_wave="1",
        legacy_ref="NF-08", owner_role="Solution architecture team", asm="ASM-B-DATA-26-7",
        proposed=(
            "The count of three stays as the number of Workbench-side jobs of v3, and the note names which three they "
            "are in the target; the full job map stays in the Batch and Scheduling and Temporal catalogues."),
        wp="B-DATA-26"),
]

assumptions = [
    dict(
        id="ASM-B-DATA-26-1",
        text=(
            "The capacity forecast is read per owning service: each driver on Inputs, Monthly, Five years and Route "
            "activity belongs to exactly one service, and the per-service volume is that driver taken by formula, so "
            "the totals of the forecast do not move and no driver is split between two services."),
        why=(
            "Arch v5 splits Recovery into 19 services with their own topic and queue, so a capacity plan that stays at "
            "the Workbench level cannot size a service; taking the driver by formula keeps every existing figure intact."),
        read=(
            "Recovery Workbench Architecture v5 Text Extract v1 lines 45, 69, 703 and 2880 to 2898; ADR-013; ADR-014; "
            "DP-01; DP-14; Recovery Workbench Microservice Ownership Map v1 sheet Services."),
        gap="CG-B-DATA-26-1",
        applied_in="06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx, sheet Service volumes, rows 5 to 23",
        confidence="High",
        confirm="Data architecture team confirms which service owns each driver at the wave 1 gate.",
        impact=(
            "Every service gets a volume row with a basis cell; Inputs, Monthly, Five years and Route activity keep "
            "every value and formula."),
        wp="B-DATA-26"),
    dict(
        id="ASM-B-DATA-26-2",
        text=(
            "Only rwb-source-data holds the grant on the 30 recovery.v_ace_* views and reads them on behalf of a screen "
            "or a workflow; every other service asks it, so a view read is a P1 SELECT and never a read by the whole "
            "Workbench or by a lake refresh."),
        why=(
            "Arch v5 gives the 30 views to rwb-source-data alone and makes the ACE read a contract call, so a document "
            "that names the Workbench or a lake refresh as the reader contradicts the architecture."),
        read=(
            "Recovery Workbench Architecture v5 Text Extract v1 line 707 and lines 1113 to 1115; ADR-010; DP-05; "
            "Recovery Workbench Microservice Ownership Map v1 sheet Tables rows account_ext, party_ext and data_product "
            "(P1)."),
        gap="CG-B-DATA-26-2",
        applied_in=(
            "06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx, Read path!A2, Read path!C16, Inputs!G7 and "
            "Key!C10"),
        confidence="High",
        confirm="P1 owner confirms GET /freshness and the snapshot(page) result carry the reads the screens need.",
        impact=(
            "The read path keeps its figures; the reader is named as one service and no other service holds a view "
            "grant."),
        wp="B-DATA-26"),
    dict(
        id="ASM-B-DATA-26-3",
        text=(
            "The three scheduled Workbench jobs of v3 become case creation and allocation (JOB-02 and JOB-03), "
            "reconciliation (JOB-04) and the WIN notice file (JOB-10); the lake refresh is retired with the lake and no "
            "Quartz job runs inside Recovery."),
        why=(
            "Arch v5 removes the data lake, retires the shared Quartz tables and runs each job in its owning service, "
            "so a lake refresh has no target and the count of three needs three real replacements."),
        read=(
            "Recovery Workbench Architecture v5 Text Extract v1 line 513, line 2296 and lines 2978 to 3002; DP-10; "
            "DP-17; ADR-016."),
        gap="CG-B-DATA-26-3",
        applied_in="06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx, Read path!C15",
        confidence="High",
        confirm="Solution architecture team confirms the three named jobs at the wave 1 gate.",
        impact=(
            "The cell changes; B15 stays 3 and no other read-path figure moves. JOB-05 and the lake copy are dropped "
            "from the plan."),
        wp="B-DATA-26"),
    dict(
        id="ASM-B-DATA-26-4",
        text=(
            "Every topic is rwb.<name>.events.v1 with 12 partitions, replication factor 3, seven-day retention, key "
            "caseId, CloudEvents 1.0 binary envelope, retry after 1 min, 10 min and 1 h and a .dlt topic; every "
            "service polls one task queue rwb-<name> in namespace rwb-recovery, and the decision record uses the shared "
            "topic rwb.decision-record.v1."),
        why=(
            "The forecast has no messaging content at all, so the settings can only come from the architecture; taking "
            "them once for all 19 services keeps the new sheet consistent with the topic library and the AC."),
        read=(
            "Recovery Workbench Architecture v5 Text Extract v1 line 703, lines 245 to 246 and lines 2911 to 2963; "
            "Temporal and Drools Design Text Extract v1 lines 444 to 483 and line 520; ADR-015; ADR-016; DP-03; DP-09; "
            "DP-14."),
        gap="CG-B-DATA-26-4",
        applied_in=(
            "06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx, sheet Topics and queues, rows 6 to 25 and 29 "
            "to 47, and the platform settings rows 51 to 61"),
        confidence="High",
        confirm="ACE platform team confirms the partition count, retention and quota for the Recovery topics.",
        impact=(
            "20 topic rows and 19 queue rows are added; ReportPublished, FileDelivered and FileFailed carry a named "
            "consumer or the placeholder."),
        wp="B-DATA-26"),
    dict(
        id="ASM-B-DATA-26-5",
        text=(
            "Where the source counts no demand for a service, the sheet carries the placeholder and states the cadence "
            "it does know (one run per business day for payment matching and booking, per lot for debt sale, one "
            "screening per new case for deviation) instead of a derived number."),
        why=(
            "A capacity figure that the source does not hold would be invented; the cadence is stated in the "
            "architecture and is enough to size a queue and a worker pool until the volume is measured."),
        read=(
            "06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx Inputs rows I01 to I34 and Route activity; "
            "Recovery Workbench Architecture v5 Text Extract v1 lines 1236 to 1250, 1322 to 1332, 1397 to 1408 and "
            "1057 to 1063; Template and Rules §R9."),
        gap="CG-B-DATA-26-5",
        applied_in=(
            "06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx, sheet Service volumes, rows for P8 and S3, "
            "and the basis notes for P9, S6, S8 and S9"),
        confidence="Medium",
        confirm="Data architecture team supplies the payment, claim, instruction and lot counts at the wave 2 gate.",
        impact=(
            "Two cells carry the placeholder and four basis notes state what is missing; no figure is invented and no "
            "total changes."),
        wp="B-DATA-26"),
    dict(
        id="ASM-B-DATA-26-6",
        text=(
            "The forecast keeps its own case inflow (new accounts divided by the accounts-per-case assumption of 1.2) "
            "and cites the Arch v5 slide 48 figure of 3,110 new cases a month beside it; no formula and no figure on "
            "Monthly or Five years is changed."),
        why=(
            "The forecast is the one artefact that holds the drivers and the assumption, and a document that silently "
            "swaps its inflow would break its own arithmetic; the conflict is recorded instead, in line with the rule "
            "that no number is invented or quietly replaced."),
        read=(
            "06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx Inputs!C12, Inputs!C13, Inputs!C9 to C11, "
            "Monthly!C5 and Five years!C5; Recovery Workbench Architecture v5 Text Extract v1 line 2433 and lines 3131 "
            "to 3144."),
        gap="CG-B-DATA-26-6",
        applied_in=(
            "06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx, sheet Service volumes, the cross-check rows 27 "
            "to 30"),
        confidence="Medium",
        confirm="Data architecture team decides which inflow the NFR sizing uses at the wave 1 gate.",
        impact=(
            "Every forecast figure stays as it is; the reader sees the slide 48 range next to the computed one."),
        wp="B-DATA-26"),
    dict(
        id="ASM-B-DATA-26-7",
        text=(
            "The three scheduled jobs of v3 are read as the Workbench-side jobs only, not as the whole platform job "
            "map; the number three is kept and the 21-job map of Arch v5 stays with the Batch and Scheduling and "
            "Temporal catalogues."),
        why=(
            "The two counts answer different questions and the source does not name its scope; keeping three as the "
            "Workbench-side count preserves the source while the job map lives in its own document."),
        read=(
            "06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx Read path!B15 and C15; Recovery Workbench "
            "Architecture v5 Text Extract v1 lines 2978 to 3002."),
        gap="CG-B-DATA-26-7",
        applied_in="06 Data/Recovery Workbench Volume and Scale Forecast v4.xlsx, Read path!C15",
        confidence="Medium",
        confirm="Solution architecture team confirms the scope of the three-job count.",
        impact="No figure changes; the note names which three jobs the count refers to.",
        wp="B-DATA-26"),
]

with GAPS.open("w", encoding="utf-8", newline="\n") as f:
    for g in gaps:
        f.write(json.dumps(g, ensure_ascii=False) + "\n")
with ASSUM.open("w", encoding="utf-8", newline="\n") as f:
    for a in assumptions:
        f.write(json.dumps(a, ensure_ascii=False) + "\n")
print("gaps", len(gaps), "assumptions", len(assumptions))
