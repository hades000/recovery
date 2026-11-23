"""C-BN1 scratch: write the candidate gap and assumption rows."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"

WP = "C-BN1"
SRC_BN = "04 User stories/Recovery Workbench Build Notes Epic 1 v6.md"
SRC_ARCH = "22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md"
SRC_TD = "22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md"
SRC_RULES = "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md"
SRC_OWN = "_work/msr/plan/ownership.json"

G = []


def gap(n, title, section, description, evidence, typ, area, sev, wave, legacy, role, proposed):
    G.append({
        "id": "CG-BN1-{}".format(n), "title": title, "source": SRC_BN, "section": section,
        "description": description, "evidence": evidence, "type": typ, "area": area,
        "severity": sev, "needed_by_wave": wave, "legacy_ref": legacy, "owner_role": role,
        "asm": "ASM-BN1-{}".format(n), "proposed": proposed, "wp": WP,
    })


gap(1, "No service owns each of the 14 data products, so the freshness stamp has no owner",
    "Freshness",
    "The freshness table names 14 products and their cycles but no source names the service that owns each product. "
    "RWB-E1-015 writes one data_product_load row per product per business date from v_ace_batch_status, which presumes a "
    "single owner for all 14, while D-RCV-60 gives each product's tables to the service that owns them.",
    "Build Notes v6 'Freshness'; Arch v5 slide 15 (GET /freshness, AceDataReady and AceDataLate belong to rwb-source-data); "
    "Ownership Map v1 has no data product rows.",
    "Missing", "Data", "P1", 1, "RWB-E1-015", "Solution architect",
    "Name the owner of DP01 to DP14 in the PRDs and keep the stamp in P1 for Epic 1, or move a product's stamp to its owner "
    "and publish it on the owner's topic.")

gap(2, "The per-service login names are not fixed in any source",
    "The grants",
    "DP-02 and R4 require one login per service, but no source names the logins. The only login in the documents is the "
    "monolith login recovery_svc, which cannot serve 19 services.",
    "Build Notes v6 'The grants'; Template and Rules R4 ('login per service') and DP-02.",
    "Missing", "Security", "P1", 1, "RWB-E1-069", "ACE DB lead",
    "Fix the login naming in the ACE DB stories of RWB-PLT-DB and state it in the Environment and Deployment Design next version.")

gap(3, "The V0002 and V0003 grant block gives one monolith login, not one login per service",
    "RWB-E1-069 Read-only ACE source views, grants and boundary rule",
    "The Grant note of RWB-E1-069 grants USAGE on recovery and SELECT on each view to recovery_svc, and DML on the 92 tables "
    "of schema recovery to the same role. D-RCV-60 replaces recovery_svc with one login per service (DP-02), so the grant "
    "block has to be rewritten per service even though the view list does not change.",
    "Build Notes v6 RWB-E1-069 Grant note; Template and Rules DP-02 and ADR-014.",
    "Conflict", "Security", "P1", 1, "RWB-E1-069", "ACE DB lead",
    "Split the V0002 and V0003 grant block into one grant per service login in RWB-PLT-DB, keeping ace_view_owner and the "
    "30 views with P1.")

gap(4, "The rule tables are described as recovery-schema tables but are owned by rwb-decision",
    "RWB-E1-072 Drools runtime and rule package store",
    "The View note of RWB-E1-072 says the rule tables are in the recovery schema, and RWB-E1-073 stores the workbook, the "
    "generated DRL and the checksum there. The Ownership Map gives rule_package, rule_package_version, rule_row and "
    "rule_test_case to P7 rwb_decision, and the Temporal and Drools design puts governance centrally in rwb-decision with "
    "evaluation local in the owning service.",
    "Build Notes v6 RWB-E1-072 and RWB-E1-073; Ownership Map v1 rule_package ruling (ASM-A6-tables-3); Temporal and Drools "
    "design slide 15.",
    "Conflict", "Data", "P2", 1, "RWB-E1-072", "P7 rule owner",
    "Keep governance, the registry and the test cases in P7 and give each owning service only the evaluated copy (DP-04).")

gap(5, "The retention tables are P1 tables in the story and P5 tables in the Ownership Map",
    "RWB-E1-017 Retention and archive rule for the data store",
    "RWB-E1-017 owns retention_rule and retention_action and applies them to the 92 Workbench tables. The Ownership Map gives "
    "both tables to P5 rwb_document, which also applies retention to the document store.",
    "Build Notes v6 RWB-E1-017; Ownership Map v1 retention_rule ruling (ASM-A6-tables-10).",
    "Conflict", "Data", "P2", 1, "RWB-E1-017", "P5 document owner",
    "Let P5 own both retention tables and the retention Schedule (JOB-17), and let P1 keep only a contract read.")

gap(6, "The role table is loaded by P3 in the story and owned by P4 in the Ownership Map",
    "RWB-E1-019 Roles, teams and queues as data",
    "RWB-E1-019 loads role, queue, queue_member, reference_row and reference_version as reference data. The Ownership Map "
    "gives role to P4 rwb_access and keeps queue, queue_member and the reference tables with P3.",
    "Build Notes v6 RWB-E1-019; Ownership Map v1 role and queue rows; Template and Rules DP-07.",
    "Conflict", "Data", "P2", 1, "RWB-E1-019", "P4 access owner",
    "Load roles in P4 and read them in P3 by contract; keep teams, queues and the reference rows in P3.")

gap(7, "The P2 outbound adapter writes a table owned by rwb-debtsale",
    "RWB-E1-007 Integration adapters for outbound files",
    "RWB-E1-007 writes interface_config, outbound_item, outbox_event, outbox_delivery, processed_event, debt_sale_account and "
    "recovery_case. Under D-RCV-60 debt_sale_account belongs to S6 rwb_debtsale and recovery_case to P3 rwb_case, so the "
    "adapter can no longer write them in its own transaction.",
    "Build Notes v6 RWB-E1-007 View note; Ownership Map v1 debt_sale_account (S6) and recovery_case (P3).",
    "Conflict", "Integration", "P2", 1, "RWB-E1-007", "Integration lead",
    "Keep the file and outbox tables in P2, and let S6 own debt_sale_account with a contract call or an event from P2.")

gap(8, "Feature flags are a P2 module table in the story and a platform library object in the Ownership Map",
    "RWB-E1-047 Feature flags for module release with a removal date",
    "The section header places RWB-E1-047 in Module P2 Integration and the story owns feature_flag and feature_flag_change. "
    "The Ownership Map and the R-PREC default ruling give feature flags to the platform library, and the split plan gives the "
    "work to RWB-PLT-E1047.",
    "Build Notes v6 RWB-E1-047; Ownership Map v1 feature_flag ruling (ASM-A6-tables-7); Template and Rules R3 default ruling.",
    "Conflict", "Architecture", "P2", 1, "RWB-E1-047", "Platform lead",
    "Build the flag tables and the client in the platform library and let P2 serve the admin API against it.")

gap(9, "The case story writes the P1 extension tables",
    "RWB-E1-018 Case ID issuance and case record v1",
    "RWB-E1-018 writes recovery_case, case_account, case_party, case_entry_exclusion, party_ext and account_ext. party_ext and "
    "account_ext are P1 extension tables in the Ownership Map, so a P3 story cannot write them in its own transaction.",
    "Build Notes v6 RWB-E1-018 View note; Ownership Map v1 party_ext and account_ext (P1).",
    "Conflict", "Data", "P2", 1, "RWB-E1-018", "P3 case owner",
    "Keep the case tables in P3, write the extension rows in the P1 story RWB-P1-E1018-APP, and read them back by contract.")

gap(10, "The Temporal platform and the Drools runtime sit in a P3 module in the story and in platform epics in the split plan",
    "RWB-E1-070, RWB-E1-071 and RWB-E1-072",
    "The three configuration notes name Module P3 Case and workflow. The split plan gives their work to platform stories "
    "RWB-PLT-E1070, RWB-PLT-E1071 and RWB-PLT-E1072, in wave 0 lanes, and Arch v5 slides 45 and 16 describe one platform "
    "cluster and one shared kit for all 19 services.",
    "Build Notes v6 RWB-E1-070 to RWB-E1-072; split plan legacy RWB-E1-070, RWB-E1-071 and RWB-E1-072; Arch v5 slide 45.",
    "Conflict", "Architecture", "P3", 0, "RWB-E1-070", "Platform lead",
    "Keep the build order in the notes and read Module P3 as 'consumed by P3' rather than 'owned by P3'.")

gap(11, "The run books are a P2 story in the notes and a platform OPS story in the split plan",
    "RWB-E1-056 Run books and monitoring for every Epic 1 Workbench job",
    "The section header places RWB-E1-056 in Module P2 Integration, and the story reads job_catalog, data_product_load, "
    "case_list_row and reconciliation_result. The split plan gives the work to RWB-PLT-E1056-OPS in a platform lane, and the "
    "jobs it covers belong to nine different services.",
    "Build Notes v6 RWB-E1-056; split plan legacy RWB-E1-056; Ownership Map v1 job_catalog ruling (ASM-A6-tables-9).",
    "Conflict", "Operations", "P3", 1, "RWB-E1-056", "DevOps lead",
    "Publish the run book standard from the platform OPS story and let each service keep its own run book rows in its ops lane.")

gap(12, "The data lake copy note remains in the build notes although the decision retires it",
    "RWB-E1-014 Decision log copy to the data lake",
    "Arch v5 removes the data lake (DP-17), so RWB-E1-014 has no target and lake_copy_watermark is dropped. The note is still "
    "in the build notes and still describes a watermark and a copy step, which no Epic 1 story owns.",
    "Build Notes v6 RWB-E1-014; Template and Rules R6 (Retired); Arch v5 slide 37; Ownership Map v1 lake_copy_watermark.",
    "Outdated", "Data", "P3", 1, "RWB-E1-014", "Solution architect",
    "Keep the note as retired with no target and record the change in the Change Register, as R6 requires.")

gap(13, "The Quartz note remains in the build notes although a Temporal Schedule replaces it",
    "RWB-TE-007 Scheduled jobs on Quartz",
    "D-RCV-60 retires RWB-TE-007 and points its dependencies to RWB-PLT-E1071-CON, but the note still owns a Quartz schedule "
    "and job_catalog, and RWB-E1-030 still describes the JOB-06 chain behind it.",
    "Build Notes v6 RWB-TE-007 and RWB-E1-030; Template and Rules R6 (Retired) and DP-10; Arch v5 slide 44.",
    "Outdated", "Operations", "P3", 1, "RWB-TE-007", "Platform lead",
    "Read JOB-06 and every other Job in the map as a Temporal Schedule in the owning service and keep the retired note for "
    "traceability only.")

gap(14, "The number of Epic 1 rule packages is not reconciled with the phase 1 package list",
    "RWB-E1-072 Drools runtime and rule package store",
    "RWB-E1-072 seeds five Epic 1 package codes, while the Temporal and Drools design names eight phase 1 packages (ENTRY, "
    "EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH). No source says which five are "
    "Epic 1.",
    "Build Notes v6 RWB-E1-072 View note; Temporal and Drools design slide 15 phase 1 packages.",
    "Ambiguous", "Data", "P3", 1, "RWB-E1-072", "P7 rule owner",
    "Name the five Epic 1 packages in the P7 story and let the remaining three arrive with their epics.")

gap(15, "The sandbox story applies three migrations where 19 schemas now need their own sequence",
    "RWB-E1-065 Sandbox database with synthetic recovery data",
    "RWB-E1-065 seeds the ACE schema, applies V0001 to V0003 and fills 88 Workbench tables and four extension tables. Under "
    "DP-15 each service has its own Flyway sequence in its own schema, so a three-migration sandbox cannot produce the 19 "
    "schemas the stories build on.",
    "Build Notes v6 RWB-E1-065; Template and Rules DP-15 and ADR-021.",
    "Outdated", "Data", "P3", 1, "RWB-E1-065", "ACE DB lead",
    "Build the sandbox from the 19 Flyway sequences plus the two view migrations and state the seeding order per schema.")

gap(16, "The reconciliation story writes 'the case exceptions' without naming a table",
    "RWB-E1-011 Reconciliation and data quality report",
    "The View note of RWB-E1-011 writes reconciliation_result, case_list_row and 'the case exceptions'. No table of that name "
    "is in the Ownership Map, so the write cannot be assigned to a service.",
    "Build Notes v6 RWB-E1-011 View note; Ownership Map v1 table list.",
    "Ambiguous", "Data", "P3", 1, "RWB-E1-011", "P1 data owner",
    "Read 'the case exceptions' as the reconciliation breaks in reconciliation_result, or name the P3 case_entry_exclusion if "
    "that is meant.")

gap(17, "The masked copy story writes the tables of three services from one platform story",
    "RWB-TE-004 Masked data in SIT and UAT",
    "RWB-TE-004 loads a masked copy of recovery_case, case_account, case_party, interaction, document_field, party_ext and "
    "contact_point_ext. Those tables belong to P3, P5 and P1, and the split plan gives the work to a platform story that owns "
    "no schema of its own.",
    "Build Notes v6 RWB-TE-004; Ownership Map v1 table owners; split plan legacy RWB-TE-004.",
    "Conflict", "Testing", "P2", 0, "RWB-TE-004", "Platform lead",
    "Let the platform story supply the masking tool and each owning service load its own masked rows in its own story.")

for n, (code, name, wave, epics) in enumerate(
        [("P8", "rwb-payment", 2, "RWB-E1-001"), ("S5", "rwb-asset", 2, "RWB-E1-011"),
         ("S8", "rwb-deviation", 2, "RWB-E1-020, RWB-E1-021, RWB-E1-023, RWB-E1-062, RWB-E1-065"),
         ("S9", "rwb-partner", 4, "RWB-E1-032, RWB-E1-057")], start=18):
    gap(n, "Service {} takes Epic 1 stories in wave 1 although its Arch v5 wave is {}".format(code, wave),
        "Epic 1 and the 19 services",
        "The W-MAP rule puts every EP01 story in wave 1, and the Service Story Catalog places the {} Epic 1 stories in wave 1 "
        "lanes. Arch v5 slide 41 creates {} in wave {}. R5.6 keeps the earlier wave and raises one conflict row per service and "
        "business epic; the build notes have to say so, because the wave column of the story set no longer matches the service "
        "table.".format(code, name, wave),
        "Build Notes v6; Template and Rules R5.6 (W-MAP) and R4; Arch v5 slide 41; Service Story Catalog v1 Stories sheet.",
        "Conflict", "Delivery", "P3", 1, epics.split(",")[0].strip(), "Delivery lead",
        "State the wave 1 delivery of {} in the service epic and the wave plan, and let the {} service wave govern its later "
        "stories.".format(name, name))

with (WORK / "gaps" / "C-BN1.jsonl").open("w", encoding="utf-8", newline="\n") as f:
    for r in G:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

A = []


def asm(n, text, why, read, gap, applied, conf, confirm, impact):
    A.append({"id": "ASM-BN1-{}".format(n), "text": text, "why": why, "read": read, "gap": "CG-BN1-{}".format(gap),
              "applied_in": applied, "confidence": conf, "confirm": confirm, "impact": impact, "wp": WP})


asm(1, "For Epic 1 every one of the 14 data products is stamped by P1 rwb-source-data, which publishes GET /freshness and "
       "AceDataReady, and the owning service of each product is named later in its PRD.",
    "RWB-E1-015 is a P1 story and the freshness contract and events are P1's in Arch v5 slide 15; no source names a product owner.",
    "Build Notes v6 Freshness; Arch v5 slide 15.", 1, "Build Notes v7 Freshness and RWB-E1-015",
    "Medium", "Solution architect", "Names the owner of each product before wave 1 closes.")
asm(2, "Each service gets one login named after its own service short name, set by the ACE DB stories of RWB-PLT-DB, and "
       "recovery_svc is retired at cutover.",
    "DP-02 and R4 require one login per service but no source names it; the short name is the only naming rule the documents fix "
    "for schema, API, topic, queue and package.",
    "Template and Rules R4 and DP-02; Build Notes v6 The grants.", 2, "Build Notes v7 The grants",
    "Medium", "ACE DB lead", "The login naming is fixed before the first service schema is created.")
asm(3, "For Epic 1 the V0002 and V0003 grant block is read as one grant per service login: P1 keeps SELECT on the 30 views and "
       "every other service holds no view privilege.",
    "The view list and the read path do not change with the realignment; only the role that holds the grant changes.",
    "Build Notes v6 RWB-E1-069; Template and Rules DP-02, ADR-014.", 3, "Build Notes v7 The grants and RWB-E1-069",
    "Medium", "ACE DB lead", "The view conformance test runs per service login.")
asm(4, "Rule governance, the rule rows and the test cases are P7 rwb_decision tables for Epic 1, and an owning service holds "
       "only the evaluated copy of a package.",
    "The Ownership Map ruling (ASM-A6-tables-3) and the Temporal and Drools design put governance centrally and evaluation "
    "locally (DP-04).",
    "Ownership Map v1 rule_package ruling; Temporal and Drools design slide 15.", 4,
    "Build Notes v7 RWB-E1-072 and RWB-E1-073", "High", "P7 rule owner", "The registry and the authoring console are P7 work.")
asm(5, "Retention tables and the retention Schedule are P5 rwb_document for Epic 1; P1 keeps no retention table.",
    "The Ownership Map gives retention_rule and retention_action to P5 and Arch v5 slide 44 gives JOB-17 to rwb-document.",
    "Ownership Map v1 retention_rule ruling; Arch v5 slide 44.", 5, "Build Notes v7 RWB-E1-017",
    "High", "P5 document owner", "P1's retention work closes into P5.")
asm(6, "role, permission, role_conflict, masking_rule and delegation_limit are P4 rwb_access; P3 keeps queue, queue_member, "
       "reference_row, reference_version and lov_value.",
    "The Ownership Map gives the role and masking tables to P4 and keeps the reference and queue tables with P3 (DP-07).",
    "Ownership Map v1 role, permission, delegation_limit and lov_value rows.", 6,
    "Build Notes v7 RWB-E1-019, RWB-E1-022, RWB-E1-037 and RWB-E1-038", "High", "P4 access owner",
    "Role data is seeded once, in P4.")
asm(7, "The P2 outbound adapter keeps interface_config, outbound_item and the library outbox and inbox tables, and S6 owns "
       "debt_sale_account and P3 owns recovery_case.",
    "The Ownership Map is the owner of record for a table and a service may not write another service's schema (DP-01).",
    "Ownership Map v1 debt_sale_account and recovery_case; Template and Rules DP-01 and DP-09.", 7,
    "Build Notes v7 RWB-E1-007", "Medium", "Integration lead", "The adapter publishes a file request instead of writing S6.")
asm(8, "Feature flags are platform library objects for Epic 1 and P2 serves the admin API against the library.",
    "The R-PREC default ruling and the Ownership Map put feature flags with the platform library (ASM-A6-tables-7).",
    "Template and Rules R3 default ruling; Ownership Map v1 feature_flag ruling.", 8,
    "Build Notes v7 RWB-E1-047", "High", "Platform lead", "No flag table in any service schema.")
asm(9, "party_ext and account_ext stay with P1, and the P3 case story writes them through the P1 story RWB-P1-E1018-APP.",
    "The Ownership Map gives the four extension tables to P1; the P1 slice of RWB-E1-018 exists in the split plan for that reason.",
    "Ownership Map v1 party_ext and account_ext; split plan legacy RWB-E1-018.", 9,
    "Build Notes v7 RWB-E1-018", "Medium", "P3 case owner", "Case creation makes one extra contract call.")
asm(10, "RWB-E1-070, RWB-E1-071 and RWB-E1-072 are platform stories for Epic 1 and P3 consumes them without owning a cluster.",
    "The split plan gives all three to RWB-PLT-E1070, E1071 and E1072 and Arch v5 slide 45 describes one cluster for all services.",
    "split plan legacy RWB-E1-070 to RWB-E1-072; Arch v5 slide 45.", 10, "Build Notes v7 RWB-E1-070 to RWB-E1-072",
    "High", "Platform lead", "The build order of the four configuration notes still holds.")
asm(11, "Run books for every Workbench job and for the ACE batch record are RWB-PLT-E1056-OPS, and each service keeps its own "
        "run book rows in its ops lane.",
    "The split plan gives E1-056 to the platform OPS epic and the jobs it covers belong to nine services.",
    "split plan legacy RWB-E1-056; Arch v5 slide 44.", 11, "Build Notes v7 RWB-E1-056", "Medium", "DevOps lead",
    "One run book standard, nine service owners.")
asm(12, "RWB-E1-014 has no target and no new story; the note stays in the build notes for traceability and the change is "
        "recorded in the Change Register.",
    "R6 retires E1-014 because Arch v5 has no data lake (DP-17).",
    "Template and Rules R6; Arch v5 slide 37; Ownership Map v1 lake_copy_watermark.", 12,
    "Build Notes v7 RWB-E1-014 and What D-RCV-60 retires", "High", "Solution architect", "No lake copy is built.")
asm(13, "RWB-TE-007 has no new story and every dependency on it points to RWB-PLT-E1071-CON; the JOB-06 chain of RWB-E1-030 runs "
        "as a Temporal Schedule in rwb-case.",
    "R6 retires TE-007 and DP-10 replaces Quartz with a Temporal Schedule in the owning service.",
    "Template and Rules R6 and DP-10; Arch v5 slide 44.", 13, "Build Notes v7 RWB-TE-007 and RWB-E1-030",
    "High", "Platform lead", "No Quartz table in any schema.")
asm(14, "The five Epic 1 rule packages are ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER; RESTRUCTURE, PAYMENT_MATCH and "
        "BOOKING_MATCH arrive with their own epics.",
    "These five are the packages the Epic 1 stories use (case entry, exclusion, allocation, assignment and transfer) and the design "
    "lists all eight as phase 1 without an epic mapping.",
    "Build Notes v6 RWB-E1-072; Temporal and Drools design slide 15.", 14, "Build Notes v7 RWB-E1-072",
    "Low", "P7 rule owner", "The seed list of the Epic 1 packages depends on this.")
asm(15, "The sandbox applies the 19 Flyway sequences plus the V0002 and V0003 view migrations, and V0001 to V0003 is read as the "
        "Epic 1 subset of that order.",
    "DP-15 gives each service its own sequence and the view migrations stay with P1.",
    "Template and Rules DP-15 and ADR-021; Build Notes v6 RWB-E1-065.", 15, "Build Notes v7 RWB-E1-065",
    "Medium", "ACE DB lead", "The sandbox seeding order is fixed before SIT.")
asm(16, "The 'case exceptions' of RWB-E1-011 are the reconciliation breaks held in P1's reconciliation_result; if a separate "
        "table is meant it is P3's case_entry_exclusion.",
    "reconciliation_result is the P1 table the same note writes and case_entry_exclusion is the only P3 exception table in the "
    "Ownership Map.",
    "Build Notes v6 RWB-E1-011; Ownership Map v1 reconciliation_result and case_entry_exclusion.", 16,
    "Build Notes v7 RWB-E1-011", "Low", "P1 data owner", "The P1 story closes without an unowned write.")
asm(17, "RWB-TE-004 is platform tooling and each owning service runs the masked load in its own schema; the platform story does "
        "not write a P3, P5 or P1 table.",
    "A platform story owns no business schema and DP-01 forbids a cross-schema write.",
    "Template and Rules DP-01; Ownership Map v1 table owners; split plan legacy RWB-TE-004.", 17,
    "Build Notes v7 RWB-TE-004", "Medium", "Platform lead", "Three service stories carry their own masked load.")
for n, (code, wave, ep) in enumerate([("P8", 2, "EP01"), ("S5", 2, "EP01"), ("S8", 2, "EP01"), ("S9", 4, "EP01")], start=18):
    asm(n, "{} delivers its {} stories in wave 1 and keeps its Arch v5 wave {} for its later stories.".format(code, ep, wave),
        "R5.6 keeps the earlier W-MAP wave and raises one conflict row per service and business epic.",
        "Template and Rules R5.6; Arch v5 slide 41.", n, "Build Notes v7 Epic 1 and the 19 services",
        "High", "Delivery lead", "The wave plan shows one service delivered in two parts.")

asm(22, "The Epic 1 platform stories sit in wave 0 lanes CG-W0 and L-PLT-* with the business epic EP01 as their tag.",
    "R5.7 rule 6 needs Day-1 work for every team type, and the platform epics are wave 0 in R4.",
    "Template and Rules R4 and R5.7; Service Story Catalog v1 Stories sheet.", 22,
    "Build Notes v7 Epic 1 and the 19 services", "High", "Delivery lead", "Platform work starts on Day 1.")
asm(23, "The build notes v7 follow the story set of Service Story Catalog v1 with no separate approval and stay in Draft status.",
    "The run takes missing approvals as assumptions (D-RCV-60 overlay) and no human verification stop is in scope.",
    "AGENTS.md rule 9; Template and Rules R1 U8.", 23, "Build Notes v7 change log", "Medium", "Delivery lead",
    "The notes are released as Draft.")

with (WORK / "assumptions" / "C-BN1.jsonl").open("w", encoding="utf-8", newline="\n") as f:
    for r in A:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("gaps", len(G), "assumptions", len(A))
