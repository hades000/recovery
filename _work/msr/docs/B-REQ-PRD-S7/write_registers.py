"""Write the B-REQ-PRD-S7 candidate gap and assumption registers once (scratch tooling)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
WP = "B-REQ-PRD-S7"
SRC_FSD = "Recovery Workbench FSD S7 Write-off and recovery v3 (03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6)"
SRC_ARCH = "Recovery Workbench Architecture v5 Text Extract v1"
SRC_MAP = "Recovery Workbench Microservice Ownership Map v1"
SRC_E38 = "Recovery Workbench Business Requirements Epics 3 to 8 v1"
SRC_PROG = "Recovery Workbench Business Requirements Program v5"
SRC_RULES = "Recovery Workbench Microservice Story Template and Rules v1"
SRC_BR = "Recovery Workbench Business Rules and Routing Logic v4"
SRC_LDM = "Recovery Workbench Logical Data Model and Data Dictionary v8"
SRC_TMP = "Recovery Workbench Temporal and Drools Design Text Extract v1"

G = []


def gap(n, title, source, section, description, evidence, typ, area, severity, legacy_ref, owner_role, proposed):
    G.append({
        "id": f"CG-{WP}-{n}", "title": title, "source": source, "section": section,
        "description": description, "evidence": evidence, "type": typ, "area": area,
        "severity": severity, "needed_by_wave": "4", "legacy_ref": legacy_ref,
        "owner_role": owner_role, "asm": f"ASM-{WP}-{n}", "proposed": proposed, "wp": WP,
    })


gap(1,
    "The FSD reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them",
    f"{SRC_FSD}; {SRC_ARCH} slides 37 and 45; {SRC_MAP}; {SRC_RULES} DP-05",
    "A1.1 constraints; A2.1, A2.5, A2.11 and A2.15 validation rules; A2.12 and A2.16 integration points",
    "The FSD constraint says source data is read only from the ACE database through the SELECT-only recovery.v_ace_* views, and rules R-WO-01, R-WO-05, R-WO-21, R-WO-37 and R-WO-42 name the ALS and GL systems as the systems the module touches. VR-S7-005-1, VR-S7-011-1 and VR-S7-015-1 read freshness from v_ace_batch_status, and the module needs the GL write-off posting that v_ace_write_off holds. Architecture v5 slide 37 changes 'the 30 views read by any module (ADR-010)' to 'the views read only by rwb-source-data', slide 45 answers who reads ACE data with rwb-source-data alone, and slide 13 gives the S7 row a single REST call, to P1, with an event subscription to P1. The Ownership Map records no view as S7's. The read path of the whole module is therefore undefined in the FSD.",
    f"FSD S7 A1.1 constraints; VR-S7-005-1, VR-S7-011-1, VR-S7-015-1; R-WO-01 (ALS load complete), R-WO-21 (ALS and GL return a reference); {SRC_ARCH} slide 37 (views read only by rwb-source-data), slide 45 (only rwb-source-data reads the 30 views; everyone else asks it through REST or a Temporal activity), slide 13 (S7 row: T to P7, T E to P8, R E to P1); {SRC_MAP} Tables (no S7 view) and Rulings.",
    "Conflict", "Data read path", "P1", "RWB-E6-013, RWB-E6-014, RWB-E6-021",
    "Solution architect",
    "Carry the FSD field names as the source field names that the rwb-source-data contract returns, and build every scan, decision and posting on that contract; no view and no ACE table is read by this service. Confirm the contract fields and the freshness response with P1 before wave 4 system test.")

gap(2,
    "The FSD posts to ALS and the general ledger from this module, while Architecture v5 gives the posting to rwb-payment",
    f"{SRC_FSD}; {SRC_ARCH} slides 13, 20 and 28; {SRC_MAP} endpoints; {SRC_TMP} slide 23",
    "A2.9 Post an approved write-off; A2.10 Send provision inputs to Finance; A2.11 Reconcile",
    "FSD A2.9 states that the module posts the write-off to ALS and the general ledger and releases the provision, and R-WO-21 to R-WO-24 give the module the ALS reference, the rejection, the retry and the retry limit. Architecture v5 slide 20 gives rwb-writeoff 'OUT: TMP Decision: child: committee approval - Payment: postProceeds', so the posting is a step on rwb-payment's queue, and 'REST Source data: GL outcome' for the result read back. The connection matrix gives the S7 row no cell to ALS, the general ledger, P2 or P8 for a REST call, and slide 28 makes the write-off posting one of the four irreversible steps that wait for the ledger. The FSD therefore holds a posting capability that v5 places in another service, and the point of no return has two candidate owners.",
    f"FSD S7 A2.9 description and steps; R-WO-20 to R-WO-25; {SRC_ARCH} slide 20 (S7 OUT: Payment: postProceeds, REST Source data: GL outcome), slide 13 (S7 row), slide 28 (strict mode at write-off posting); {SRC_MAP} Endpoints (no posting operation owned by S7); {SRC_TMP} slide 23 (posting is the point of no return; re-post, rescan or committee on failure).",
    "Conflict", "Integration and posting", "P1", "RWB-E6-021, RWB-E6-022",
    "Solution architect with the P8 owner",
    "Keep the posting decision, the reference, the rejection, the retry and the re-post as this product's behaviour, and obtain the posting itself as a step on rwb-payment's queue with the GL outcome read back through P1; this service writes no posting entry and calls ALS or the general ledger on no path. Confirm the split with the P8 owner before wave 4 system test.")

gap(3,
    "The Ownership Map lists one table for rwb-writeoff, while Architecture v5 gives the schema four entity groups",
    f"{SRC_ARCH} slides 20, 29 and 41; {SRC_MAP} tables; {SRC_LDM} write_off; Recovery Workbench Physical Schema v6.sql",
    "Service contract, rwb-writeoff OUT DB",
    "Architecture v5 slide 20 states that rwb-writeoff 'writes schema rwb_writeoff: eligibility, committee, posting, recovery after charge-off', and slide 41 repeats the four things the service owns. The Ownership Map Tables sheet holds exactly one row for S7, write_off, and the Logical Data Model holds the same one table with eleven fields. The scan result, the committee decision per account, the posting attempts and the recovery, placement and closure records therefore have no table, no field list and no key in the register that every story's section 12.7 and every DB story is written from.",
    f"{SRC_ARCH} slide 20 (DB writes schema rwb_writeoff: four entity groups), slide 41 (S7 owns eligibility, committee, posting, recovery after charge-off), slide 29 (one schema and login per service); {SRC_MAP} Tables: one S7 row, write_off; {SRC_LDM} write_off DF-FIN-010 to DF-FIN-020 only.",
    "Missing", "Data model", "P2", "RWB-E6-013 to RWB-E6-028",
    "Data architect",
    "State the four entity groups with the key fields the rules require, fix the physical name of write_off as the one table the map holds, and write the remaining table set with the S7 DB story. Add the missing rows to the Ownership Map in the same change.")

gap(4,
    "Slide 20 names write-off collection operations that neither the Ownership Map nor the API specification holds",
    f"{SRC_ARCH} slides 20 and 41; {SRC_MAP} endpoints; Recovery Workbench API Specification v4",
    "Service contract, rwb-writeoff IN",
    "Architecture v5 slide 20 gives the service 'IN: REST GET/POST /write-offs; POST /write-offs/{id}/submit', and slide 41 gives it the first API path /write-offs. The Ownership Map endpoints sheet holds only POST /write-off-scans and POST /write-offs/{writeOffId}/committee-decision for S7, and the API specification v4 holds the same two paths with x-module S7. The read of a write-off, the creation of a proposal and the submission of a pack to the committee therefore have no published operation, which is what the screen and the committee workflow call.",
    f"{SRC_ARCH} slide 20 (S7 IN REST), slide 41 (first API path /write-offs); {SRC_MAP} Endpoints: two S7 rows only; API Specification v4: /write-off-scans and /write-offs/{{writeOffId}}/committee-decision only, both x-module S7.",
    "Missing", "API contract", "P2", "RWB-E6-015, RWB-E6-017, RWB-E6-018",
    "Solution architect",
    "Publish the collection operations the screen and the committee need under /api/recovery/writeoff/v1 before the contract story closes, and add them to the Ownership Map and the API specification in the same change; the existing two operations keep their paths.")

gap(5,
    "The Finance provision feed has no interface path: P2 is outbound-only and the matrix gives S7 no cell to it",
    f"{SRC_FSD} A2.10; {SRC_BR} R-WO-26 to R-WO-28; {SRC_ARCH} slides 13 and 20; {SRC_PROG} section 5.2 (P2 outbound only)",
    "A2.10 Send provision inputs to Finance",
    "R-WO-26 sends the provision inputs and the tax file to Finance on the month-end close, R-WO-27 retries a rejected file and R-WO-28 records the tax file reference. The FSD lists 'ALS and GL' as the integration point of A2.10. The program BRD makes P2 rwb-integration outbound-only and gives it the file windows and the GL write-off event, but the connection matrix gives the S7 row no cell to P2, and the Ownership Map holds no interface row for this service. The feed that Finance waits for at the month end therefore has no owned path.",
    f"FSD S7 A2.10 integration points; {SRC_BR} R-WO-26, R-WO-27, R-WO-28; {SRC_ARCH} slide 13 (S7 row: no P2 cell), slide 20 (S7 contract: no FILE line); {SRC_PROG} section 5.2 and the outbound-only statement for P2; {SRC_MAP} Interfaces: no S7 row.",
    "Conflict", "Integration contract", "P2", "RWB-E6-022",
    "Solution architect with the integration lead",
    "Carry the Finance feed as a product requirement with the retry and the task after the retry limit, and take the path as an open question with a named owner: a P2 interface, or an activity on another service's queue. Nothing in this document designs the file.")

gap(6,
    "The committee pack is a document in the document hub, and the matrix connects S7 to P5 on no path",
    f"{SRC_FSD} A2.3, A2.5, A2.9; {SRC_BR} R-WO-05, R-WO-09, R-WO-10; {SRC_ARCH} slide 13; {SRC_MAP}",
    "A2.3 Prepare the write-off pack; A2.5 Route the population; A2.10",
    "R-WO-05 has the write-off agent prepare the pack including the route history, the legal and asset state and the residual; R-WO-09 holds a pack whose pack_document_id is absent and R-WO-10 routes it once the provision carried and the pack document are present. The FSD names 'the Workbench document hub' as the integration point of A2.3. The document hub is P5, whose capability is metadata, custody, retention and the retention job JOB-17, but the connection matrix gives the S7 row no P5 cell and no Temporal or REST path, so neither the pack document nor its retention class has an owned path.",
    f"FSD S7 A2.3 integration points and steps; {SRC_BR} R-WO-05 (pack document), R-WO-09 (pack_document_id absent), R-WO-10, R-WO-47 to R-WO-48 (retention class); {SRC_ARCH} slide 13 (S7 row: no P5 cell), slide 44 (JOB-17 retention on rwb-document); {SRC_MAP} Workflows, Events and Jobs: no S7 to P5 row.",
    "Missing", "Integration contract", "P2", "RWB-E6-015, RWB-E6-025",
    "Solution architect with the P5 owner",
    "Hold the pack document in the document hub and carry its reference and its retention class here; state the call type as an open question with the P5 owner, because the matrix shows none.")

gap(7,
    "Agency placement, result and recall run through the partner portal, which is S9 and is created in the same wave",
    f"{SRC_FSD} A2.15, A2.16; {SRC_BR} R-WO-30, R-WO-33, R-WO-34, R-WO-35; {SRC_ARCH} slide 13; {SRC_MAP}; {SRC_PROG} section 10.2",
    "A2.15 Record a customer payment after charge-off; A2.16 Sell a post charge-off population",
    "R-WO-30 places the account with the agency chosen on measured return and sends the instruction 'same day on the portal', R-WO-33 attaches the result reported on the portal the same day, R-WO-34 recalls a placement on measured return or conduct, and R-WO-35 replaces it. The FSD names the partner portal as the integration point of A2.16. The partner service is S9 rwb-partner, which the program BRD places in wave 4, the same wave as this service, and the connection matrix gives the S7 row no S9 cell. Placement, result and recall therefore cannot be demonstrated until the partner contract exists, inside the same release.",
    f"FSD S7 A2.15 and A2.16 integration points; {SRC_BR} R-WO-30, R-WO-33, R-WO-34, R-WO-35; {SRC_ARCH} slide 13 (S7 row: no S9 cell); {SRC_PROG} section 10.2 (RWB-SVC-S7 and RWB-SVC-S9 both wave 4); {SRC_MAP} Services: S9 rwb-partner wave 4.",
    "Missing", "Integration and sequencing", "P2", "RWB-E6-027, RWB-E6-034",
    "Partner and agency manager with S9",
    "Carry the placement, the result and the recall as product behaviour, hold every placement decision until the partner contract is published in the same wave, and sequence the placement slice last inside wave 4.")

gap(8,
    "A charged-off population is handed to the debt sale route, and neither service's matrix row shows the other",
    f"{SRC_FSD} A2.16; {SRC_BR} R-WO-32, R-WO-50, R-WO-51; {SRC_ARCH} slide 13; {SRC_MAP}; {SRC_PROG} section 10.2",
    "A2.16 Sell a post charge-off population",
    "R-WO-32 hands a charged-off population to the debt sale route where the placement type is sale, and R-WO-50 closes the case when the buyer settles and the data transfer completes, with R-WO-51 closing the item on the buyer's remittance. The debt sale route is S6 rwb-debtsale, created in wave 3, one wave before this service. The connection matrix gives the S7 row no S6 cell and the S6 row no S7 cell, so the hand-over that starts the sale of a charged-off book has no owned path and no direction.",
    f"FSD S7 A2.16 integration points and prerequisites; {SRC_BR} R-WO-32, R-WO-40, R-WO-50, R-WO-51; {SRC_ARCH} slide 13 (S7 row: no S6 cell; S6 row: no S7 cell); {SRC_PROG} section 10.2 (S6 wave 3, S7 wave 4).",
    "Missing", "Integration contract", "P2", "RWB-E6-028, RWB-E6-034",
    "Solution architect with the S6 owner",
    "Carry the hand-over as product behaviour with the population, the route and the approval recorded here, and take the call type and the direction as an open question with the S6 owner before wave 4 system test.")

gap(9,
    "The FSD routing rules move the case through twenty states, while Architecture v5 gives the case state to rwb-case",
    f"{SRC_FSD}; {SRC_BR} R-WO-01 to R-WO-51; {SRC_ARCH} slides 13, 20 and 25; {SRC_MAP} workflows",
    "A2.1 to A2.16 business rules; the states SCAN_DUE to CASE_CLOSED",
    "Every write-off rule names a source state and a target state: SCAN_DUE, MONTHLY_SCAN_STARTED, SCAN_HELD, POPULATION_PROPOSED, PACK_PREPARED, PACK_INCOMPLETE, CASE_REMOVED_BY_TEAM, WITH_COMMITTEE, ESCALATED_TO_CREDIT_COMMITTEE, APPROVED, RETURNED_TO_PURSUE, DEFERRED, POSTING_PENDING, POSTED, POSTING_REJECTED, PROVISION_RELEASED, FINANCE_FEED_SENT, FINANCE_FEED_REJECTED, PLACEMENT_DECIDED, PLACED_WITH_AGENCY, PLACEMENT_RECALLED, SOLD_POST_CHARGEOFF, PAYMENT_MATCHED, PAYMENT_EXCEPTION, REMITTED_TO_BUYER, WRITEOFF_EXCEPTION, RETENTION_RUNNING and CASE_CLOSED. Architecture v5 gives the case, the CMMN state, the queues, the tasks, the timers and the parent CaseWorkflow to rwb-case, and gives this service one published event, WriteOffApproved. Which service holds which of the twenty-eight states, and which one moves the case to closed, is therefore not stated.",
    f"{SRC_BR} R-WO-01 to R-WO-51, source and target state columns; {SRC_ARCH} slide 13 (P3 row: T E to S7), slide 20 (S7 OUT: WriteOffApproved only), slide 25 (CaseWorkflow parent, a child workflow per stage); {SRC_MAP} Workflows: WriteOffWorkflow owned by S7, CaseWorkflow owned by P3.",
    "Conflict", "Case state and workflow", "P2", "RWB-E6-013 to RWB-E6-028",
    "Solution architect with the P3 owner",
    "Keep the write-off states as the stage's own record inside WriteOffWorkflow, publish the outcome and let rwb-case move the case state; state the split as an open question with the P3 owner so that no state has two writers.")

gap(10,
    "The sources disagree on what starts the monthly scan: a Schedule, the ACE batch, or Quartz",
    f"{SRC_ARCH} slide 44; {SRC_TMP} slides 12 and 23; Recovery Workbench Batch and Scheduling Design v4 JOB-16; {SRC_MAP} rulings",
    "A2.1 description and system background event; A2.2",
    "Architecture v5 slide 44 makes JOB-16 a Temporal Schedule in rwb-writeoff on the 3rd working day, and the Temporal and Drools design makes it a Schedule started on the 3rd working day after AceDataReady. The Batch and Scheduling Design v4 starts JOB-16 on the ACE batch-complete record, and the design's Phase 1 note T2 keeps Quartz. The FSD says only that the feature receives its trigger and runs monthly. The Ownership Map ruling on JOB-16 resolves the conflict in favour of the Architecture v5 catalogue and records ASM-A6-flows-12; this document carries that ruling and does not reopen it.",
    f"{SRC_ARCH} slide 44 (JOB-16 monthly, 3rd working day, rwb-writeoff, Schedule), slide 20 (Schedule: scan, 3rd working day); {SRC_TMP} slide 12 (Scheduled job for JOB-16), slide 23 (starts when JOB-16 runs on the 3rd working day after EV-26 AceDataReady), and the Phase 2 item on Quartz; {SRC_MAP} Rulings: JOB-16, ASM-A6-flows-12.",
    "Conflict", "Scheduling", "P3", "RWB-E6-013, RWB-E6-014",
    "Solution architect",
    "Run the scan as a Temporal Schedule on the 3rd working day that also tests the ALS batch, so both the date and the data condition are met, and no Quartz table, connection or job is used; the ruling of ASM-A6-flows-12 stands.")

gap(11,
    "The fifty-one write-off rules exist but their package has no owner and no version in force",
    f"{SRC_BR} R-WO-01 to R-WO-51; {SRC_TMP} the rule package item; {SRC_ARCH} slide 27; {SRC_MAP} rulings",
    "A2.1 to A2.16 validation rules; BR-S7-001 to BR-S7-016",
    "Every feature of this module applies a rule, and R-WO-01 to R-WO-51 carry the transitions. The Temporal and Drools design states that package codes are Phase 2 and that each of S1 and S3 to S9 needs one owning service for its route set, naming rwb-writeoff among them. No source read here states the package code, the version label in force, the owner of the package or the date it is promoted, so no scan can state which package it evaluated.",
    f"{SRC_BR} R-WO-01 to R-WO-51; {SRC_TMP} slide 15 (rule governance and versioning) and the Phase 2 item 3 naming rwb-writeoff among the route sets without a package; {SRC_ARCH} slide 27 (rule governance); {SRC_MAP} Rulings (no write-off package row).",
    "Missing", "Rules", "P2", "RWB-E6-013, RWB-E6-014, RWB-E6-026",
    "Center of excellence analyst with P7",
    "Read the criteria and the rules from a governed package through the rwb-decision contract, record the package and rule version on every scan and decision, and take the package code and its promotion date as an open question.")

gap(12,
    "No source states the write-off tax criteria, the meaning of the two tracks, or the criteria version in force",
    f"{SRC_FSD} A2.2; {SRC_E38} Q-006 and ASM-013; {SRC_BR} R-WO-01, R-WO-03",
    "A2.1 and A2.2 validation rules",
    "R-WO-01 tests every open case against the eligibility rule on both tracks and against the tax criteria, R-WO-03 holds the scan where the tax criteria version is absent, and VR-S7-001-1 and VR-S7-002-1 show MSG-S7-001 until Finance publishes it. No source read here defines the criteria, names the two tracks, or states who publishes the version, and the epic BRD carries the same gap as Q-006 with ASM-013.",
    f"FSD S7 A2.2 validation rules and message MSG-S7-001; {SRC_E38} Q-006 (what are the tax criteria and the two tracks) and ASM-013 (held as a versioned rule package); {SRC_BR} R-WO-01, R-WO-03.",
    "Missing", "Business rules", "P2", "RWB-E6-013, RWB-E6-014",
    "Write-off committee member",
    "Hold the criteria as a versioned package read at run time, record the version on every account, and open the scan only on a published version; no criterion and no track name is asserted here.")

gap(13,
    "The write-off exception loop has no named owner, no time limit and no field to hold either",
    f"{SRC_FSD} A2.12; {SRC_E38} Q-007 and ASM-014; {SRC_BR} R-WO-24, R-WO-43",
    "A2.12 Work the write-off exception loop",
    "The FSD states that this loop has no owner today, R-WO-24 and R-WO-43 name the exception owner only as 'Owner to confirm with C&R', and the service level column of both rules reads 'to confirm with Credit Administration'. The epic BRD carries Q-007 and ASM-014, which reads the loop as owned by the write-off team until a named owner is decided. No source gives the time limit, and the FSD field catalog holds no field for the owner or the limit.",
    f"FSD S7 A2.12 intent ('This loop has no owner today') and roles; {SRC_BR} R-WO-24 and R-WO-43 (owner 'to confirm with C&R', service level 'to confirm with Credit Administration'); {SRC_E38} Q-007, ASM-014, RISK-004.",
    "Missing", "Business rules", "P2", "RWB-E6-024",
    "Head of recovery",
    "Carry one named owner role and one time limit as required product properties, hold the owner as the write-off team until decided under ASM-014, and take the value as an open question so that the exception can be built and cannot be released without it.")

gap(14,
    "The write-off cap the epic BRD's risk names has no requirement, no rule and no value",
    f"{SRC_E38} RISK-004; {SRC_BR} R-WO-01 to R-WO-51; {SRC_FSD}",
    "A2.1 eligibility; A2.11 reconciliation",
    "RISK-004 of the epic BRD says that the write-off cap, the tax criteria and the exception ownership may stay undecided and the population cannot be defended, and its mitigation is to hold the criteria as a package and reconcile approved to posted. No requirement, no rule of R-WO-01 to R-WO-51 and no field of this module names a cap, its basis, its period or what it applies to, and the only limit the rules carry is the write-off committee limit of R-WO-11 and R-WO-12.",
    f"{SRC_E38} section 11.4 RISK-004; {SRC_BR} R-WO-11 and R-WO-12 (committee limit only); FSD S7 A2.1 to A2.16 (no cap).",
    "Ambiguous", "Business rules", "P2", "RWB-E6-013, RWB-E6-023",
    "Head of Asset Liquidity with Risk",
    "Report the population against the cap once the cap exists, and take the cap, its basis and its period as an open question; no value is asserted here and no cap is enforced in this release.")

gap(15,
    "The committee that decides a write-off above the limit, and the delegation behind it, are not defined",
    f"{SRC_BR} R-WO-12, R-WO-13, R-WO-15; {SRC_E38} BR-053 and Q-001; {SRC_PROG} section 9 DL18; {SRC_ARCH} slide 20",
    "A2.5 and A2.6 validation rules; the committee roles",
    "R-WO-12 routes a pack above the write-off committee limit to the credit approval committee chaired by the product head with Risk, and R-WO-13 approves it 'inside the delegation with Risk'. The FSD gives the roles Write-off committee member and Finance and CFO delegate, and gives no further definition of who chairs, who votes or what the substitute is. The limits themselves are DL18 in the program BRD, and Q-001 of the epic BRD asks for the limit by decision, product and amount with the substitute for each. Architecture v5 makes the approval an ApprovalWorkflow child on rwb-decision with the DoA lookup as a parameter, which needs the table to exist.",
    f"{SRC_BR} R-WO-11 to R-WO-16; {SRC_E38} BR-053, Q-001; {SRC_PROG} section 9 DL18 (load the regulation's levels now, add names and substitutes when signed); {SRC_ARCH} slide 20 (TMP Decision: child: committee approval), slide 16 (approval and DoA).",
    "Ambiguous", "Authority", "P2", "RWB-E6-018, RWB-E6-019, RWB-E6-020",
    "Risk with the product heads",
    "Take the approval through the approval workflow with the limit read from the delegation table at run time, record the level applied and the approver role, and take the level values and the committee composition as an open question under DL18 and Q-001.")

gap(16,
    "The FSD has no wait for the ledger acknowledgement that strict mode requires before a posting",
    f"{SRC_ARCH} slide 28; {SRC_TMP} slide 23; {SRC_FSD} A2.9; {SRC_BR} R-WO-20 to R-WO-25",
    "A2.9 Post an approved write-off",
    "Architecture v5 slide 28 makes debt transfer, write-off posting, auction sale and title transfer wait until the central ledger confirms the decision record, and the Temporal design repeats that the write-off posting waits for the ledger. The FSD gives the posting task, the reference, the rejection, the retry and the provision release, and names no wait on any acknowledgement, so a build against the FSD alone would post on an unconfirmed record — on the one step the architecture calls irreversible.",
    f"{SRC_ARCH} slide 28 (strict mode; irreversible steps wait for the ledger acknowledgement), slide 27 (decision record and hash chain); {SRC_TMP} slide 23 note (write-off posting waits for the central ledger); FSD S7 A2.9 and R-WO-20 to R-WO-25 (no acknowledgement step).",
    "Conflict", "Resilience and audit", "P2", "RWB-E6-021",
    "Solution architect",
    "Hold the posting until rwb-decision confirms the decision record in the central ledger, proceed only on that acknowledgement, and raise an alert where the ledger is late; the wait is a product requirement of this service, not a design of the ledger.")

gap(17,
    "The case closes after a retention period that is not set, and the retention class behind a closure is not defined",
    f"{SRC_PROG} NFR-028, NFR-031 and DL26; {SRC_E38} Q-012; {SRC_FSD} A2.13; {SRC_BR} R-WO-47, R-WO-48",
    "A2.13 Close the case after the retention period",
    "R-WO-47 closes the case only with a retention class on every document, and R-WO-48 holds the closure and raises a document task where a class is missing. NFR-031 states that case records carry a retention and archive rule by record class and that the case closes after its retention period, with the target 'Not set', and NFR-028 leaves the periods open under DL26. No source gives a period, a class list or a disposal rule for a write-off record.",
    f"{SRC_PROG} NFR-028 (retention classes defined per type; periods not set), NFR-031 (target Not set), DL26; {SRC_E38} Q-012; FSD S7 A2.13; {SRC_BR} R-WO-47, R-WO-48.",
    "Ambiguous", "Retention", "P3", "RWB-E6-025",
    "Compliance and PDPA officer",
    "Hold the closure on a retention class and a recorded period, make the period a versioned data row, and take the periods and the class list as an open question under DL26 and Q-012; no period is asserted here.")

gap(18,
    "The FSD defers the mirrored GL fields of write_off to DEF-05, which no source read here defines",
    f"{SRC_FSD} change note; {SRC_LDM} write_off DF-FIN-013 to DF-FIN-020; Recovery Workbench Physical Schema v6.sql",
    "Document control, change note v3; A2.4, A2.6, A2.7, A2.8, A2.12, A2.14 and A2.16 field catalog",
    "The FSD v3 change note states that the write_off mirrored GL fields are left for DEF-05. The FSD field catalog lists eight fields of write_off, the Logical Data Model holds eleven, and three of them are mirrored from the general ledger: responsibility_center, cost_center and gl_product, with amount and posted_date also sourced from GL. No source read here contains DEF-05, its scope or its date, so the field set of the table cannot be closed from the sources.",
    f"FSD S7 document control, change note v3 (write_off mirrored GL fields left for DEF-05); FSD S7 A2.4.3.2 field catalog (eight fields); {SRC_LDM} DF-FIN-010 to DF-FIN-020 (eleven fields, three sourced 'GL'); Physical Schema v6.sql write_off and its comments.",
    "Missing", "Data model", "P3", "RWB-E6-021, RWB-E6-022",
    "Data architect",
    "Carry the eleven model fields as the field set of write_off, mark the three GL-sourced ones as mirrored and never re-keyed, and take DEF-05 as an open question so that no field is invented and none is dropped.")

gap(19,
    "The rules require a removal reason, a review date and a pack reference that no field of the module holds",
    f"{SRC_BR} R-WO-07, R-WO-09, R-WO-17, R-WO-18; {SRC_FSD} field catalog; {SRC_LDM} write_off",
    "A2.4, A2.5, A2.8, A2.12 field catalog",
    "R-WO-07 removes a case on removal_reason, R-WO-09 holds a pack on pack_document_id, R-WO-17 defers on review_date and R-WO-18 refuses a decision on decision_reason and review_date. The FSD field catalog repeats the same eight write_off fields in seven sections and holds none of those four, and the Logical Data Model's write_off holds none of them either. The behaviour the committee and the team exercise therefore has nowhere stated to be recorded.",
    f"{SRC_BR} R-WO-07, R-WO-09, R-WO-17, R-WO-18; FSD S7 A2.4.3.2, A2.6.3.2, A2.7.3.2, A2.8.3.2, A2.12.3.2, A2.14.3.2, A2.16.3.2 field catalog (case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center); {SRC_LDM} write_off DF-FIN-010 to DF-FIN-020.",
    "Missing", "Data model", "P2", "RWB-E6-016, RWB-E6-018, RWB-E6-020",
    "Data architect",
    "Hold the removal reason, the review date, the decision reason and the pack reference as required fields of the committee and eligibility records, and fix their physical names with the DB story.")

gap(20,
    "The pack is prepared by the write-off agent, and the matrix gives S7 no path to the agent service",
    f"{SRC_FSD} A2.3; {SRC_BR} R-WO-05; {SRC_ARCH} slides 13 and 20; {SRC_MAP}; {SRC_RULES} DP-20",
    "A2.3 Prepare the write-off pack",
    "R-WO-05 has the write-off agent prepare the pack from the balance, the provision carried, the route history, the legal and asset state and the residual, and the FSD names the agent as the actor. The agent runtime is P10 rwb-agent, with its policies, prompts, runs and guardrails. The connection matrix gives the S7 row no P10 cell and the S7 service contract on slide 20 names no agent call, so the capability the pack depends on has no owned path, and no source states what the pack holds when the agent is unavailable.",
    f"FSD S7 A2.3 intent and steps (write-off agent); {SRC_BR} R-WO-05 (owner column 'Agent Runtime, Document Hub'); {SRC_ARCH} slide 13 (S7 row: no P10 cell), slide 20 (S7 OUT: Decision, Payment only); {SRC_MAP} no S7 agent row; {SRC_RULES} DP-20 (agent client to the rwb-agent contract).",
    "Missing", "Integration contract", "P2", "RWB-E6-015",
    "Solution architect with the P10 owner",
    "Carry the pack as product behaviour that the agent drafts under its contract with a template fallback inside 60 seconds, and take the call type as an open question; the pack, not the agent, is the product requirement.")

gap(21,
    "Payment matching after charge-off is given to this module, while P8 owns payment and proceeds matching",
    f"{SRC_FSD} A2.15; {SRC_BR} R-WO-37, R-WO-38, R-WO-39, R-WO-49; {SRC_ARCH} slides 13, 40 and 44",
    "A2.15 Record a customer payment after charge-off",
    "R-WO-37 posts a post charge-off payment as income and calculates the agency fee once the payment matches the case and the placement, R-WO-38 sends a payment that matches nothing to the exception list and R-WO-39 matches it later. Payment and proceeds matching, fees and posting are P8 rwb-payment's own capability, with JOB-07 payment matching run there on AceDataReady, and ProceedsMatched (EV-25) is published to rwb-writeoff. Two services therefore appear to match the same payment.",
    f"FSD S7 A2.15 and R-WO-37 to R-WO-39; {SRC_ARCH} slide 40 (P8 owns payment and proceeds matching, fees, bookings, posting files), slide 44 (JOB-07 payment matching on rwb-payment), slide 43 (EV-25 ProceedsMatched, consumer rwb-writeoff).",
    "Conflict", "Integration and rules", "P2", "RWB-E6-027, RWB-E6-028",
    "Solution architect with the P8 owner",
    "Consume ProceedsMatched as the match and record the recovery, the income and the agency fee here, hold the unmatched payment in the exception list this module shows, and take the ownership of the initial match as an open question with the P8 owner.")

gap(22,
    "Completeness is published to a channel the sources remove",
    f"{SRC_BR} R-WO-42; {SRC_ARCH} slide 45 and ADR-018; {SRC_FSD} A2.11",
    "A2.11 Reconcile the approved and posted populations",
    "R-WO-42 publishes completeness and names Power BI among its systems, and the FSD describes completeness as published from the reconciled populations. Architecture v5 removes the data lake and the Power BI extract (ADR-018) and gives reporting the read model it builds from events and the decision record. No source states where completeness is published after the removal.",
    f"{SRC_BR} R-WO-42 (systems 'Rules component, Power BI, Workbench scheduler'), R-WO-43; {SRC_ARCH} slide 45 and ADR-018 (no data lake; reporting from events), slide 41 (P9 owns measures and regulatory reports); FSD S7 A2.11.",
    "Conflict", "Reporting", "P2", "RWB-E6-023",
    "Solution architect",
    "Publish completeness from rwb-reporting, fed by the decision record and WriteOffApproved, and keep the reconciliation itself here; no extract to a data lake and no Power BI copy is created.")

gap(23,
    "The write-off proposal screen has no stated owner and no stated route through the gateway",
    f"{SRC_FSD} Screens; {SRC_ARCH} slide 41 and DP-19; {SRC_MAP} endpoints",
    "Screens: SCR-27 Write-off proposal",
    "The FSD names one screen, SCR-27 Write-off proposal, for the monthly population, the pack per case and the removals with reasons. No source read here states which service owns the screen, and Architecture v5 gives every staff screen to gateway-bff as a composite route with one hop and a 2 s timeout. The composite route for SCR-27 is therefore undefined, and its data comes from this service, rwb-case and rwb-document.",
    f"FSD S7 Screens (SCR-27 only); {SRC_ARCH} slide 20 (gateway-bff: the only entry for staff screens; composes at most a few parallel calls), slide 41; {SRC_RULES} DP-19 (screen to gateway-bff composite route); {SRC_MAP} Endpoints (no screen row).",
    "Missing", "Screen and edge", "P3", "RWB-E6-016",
    "Solution architect",
    "Serve SCR-27 through a gateway-bff composite route that joins this service's population and pack answer with the case and the document, and take the ownership of the screen as an open question so that no service is named as its owner by invention.")

gap(24,
    "No approval is recorded for the BRD or the FSD this PRD is built from, and this version is Draft",
    f"{SRC_FSD} document control; {SRC_E38} section 13; {SRC_PROG}",
    "Document control; section 13 Approval",
    "The FSD's document control shows Status 'In review' and its sign-off table is empty, and the epic BRD's governance table is the only approval record in the sources read. No Product Owner decision and no FDA decision exists for either document in this run, so the PRD cannot inherit an approved baseline and cannot be approved in this run.",
    f"FSD S7 document control (Status: In review) and Document sign-off (four empty rows); {SRC_E38} section 13 (governance and approval); {SRC_PROG} section 1.",
    "Missing", "Governance", "P3", "RWB-E6-013 to RWB-E6-037",
    "Product Owner",
    "Carry the PRD as Draft, leave the approval table empty, and record the missing approval as an assumption so that no approval is claimed for a document nobody signed.")

# Assumptions
A = []


def asm(n, text, why, read, applied_in, confidence, confirm, impact, gap=None):
    A.append({
        "id": f"ASM-{WP}-{n}", "text": text, "why": why, "read": read,
        "gap": (f"CG-{WP}-{n}" if gap is None else (f"CG-{WP}-{gap}" if gap else "")), "applied_in": applied_in, "confidence": confidence,
        "confirm": confirm, "impact": impact, "wp": WP,
    })


asm(1,
    "This service reads the GL write-off outcome, the balance facts and the freshness of each data product only through the rwb-source-data contract, publishes nothing it read from a view, and keeps the FSD field names as the source field names that contract returns.",
    "Architecture v5 (higher in precedence) makes the 30 views readable by rwb-source-data alone and gives the S7 row one REST call, to P1.",
    "FSD S7 validation rules and integration points as a statement of which facts the scan, the decision and the posting need, not of how they are read.",
    "Section 2.4 constraint 1; Section 6 FR-S7-001, FR-S7-002; Section 8.2; Section 9; Section 12 OQ-S7-01",
    "High", "Solution architect with P1, before wave 4 system test",
    "If a view stays readable by this service, the boundary test and the freshness guarantee would each need a second owner.")

asm(2,
    "The posting decision, the posting reference, the rejection, the retry and the re-post are this service's behaviour, and the posting itself is obtained as a step on rwb-payment's queue with the GL outcome read back through the source-data contract; this service writes no posting entry and calls ALS or the general ledger on no path.",
    "Architecture v5 slide 20 puts postProceeds in S7's OUT as a payment child and gives S7 the GL outcome by REST from P1, and slide 28 makes the write-off posting wait for the ledger.",
    "FSD A2.9 as the posting behaviour the business needs, with the posting execution read as P8's capability.",
    "Section 2.3; Section 5 CAP-S7-009; Section 6 FR-S7-023, FR-S7-029; Section 9; Section 12 OQ-S7-02",
    "Medium", "Solution architect with the P8 owner, before wave 4 system test",
    "Two writers of one posting would make the approved-against-posted reconciliation meaningless.")

asm(3,
    "This service owns the four entity groups Architecture v5 names (eligibility, committee, posting, recovery after charge-off) in schema rwb_writeoff, the table write_off keeps the name and the eleven fields the Ownership Map and the Logical Data Model give it, and no other physical table name is stated because the map lists none.",
    "Architecture v5 slides 20 and 41 give the schema and the four groups; the map and the model hold one table.",
    "Architecture v5's list of what the schema holds as the entity set, with the physical names of the other three left to the DB story.",
    "Section 8.1; Section 10.4; Section 12 OQ-S7-03",
    "Medium", "Data architect, before the S7 DB story",
    "The migration and the boundary test cannot be written until the table set exists; the story that creates it is not blocked.")

asm(4,
    "The write-off collection operations are published under /api/recovery/writeoff/v1, the two operations the Ownership Map holds keep their paths, and the collection paths slide 20 names are added to the contract before the contract story closes.",
    "Slide 20 and slide 41 name the collection paths; the map and the API specification hold only the scan and the committee-decision operations.",
    "Slide 20's IN line as the operation set the screen and the committee need, with the register entries to follow.",
    "Section 9; Section 12 OQ-S7-04",
    "Medium", "Solution architect, before the S7 contract story closes",
    "Without the collection operations the screen has nothing to call and the committee has nothing to submit to.")

asm(5,
    "The provision inputs and the tax file reach Finance through the rwb-integration contract, with the retry and the task after the retry limit held here; no file is produced or delivered by this document's design.",
    "The program BRD makes P2 outbound-only and gives it the file windows, and the FSD requires the feed on the month-end close.",
    "FSD A2.10 and R-WO-26 to R-WO-28 as the feed the business needs, with the delivery read as P2's interface.",
    "Section 5 CAP-S7-010; Section 6 FR-S7-027; Section 9; Section 12 OQ-S7-05",
    "Medium", "Solution architect with the integration lead, before wave 4 system test",
    "Finance cannot close the month on a feed with no owned path, so the release is blocked, not the build.")

asm(6,
    "The pack document is held in the document hub and this service holds its reference and its retention class, read and written through the P5 contract; the closure test on a missing retention class is answered by that contract.",
    "The document hub is the system of record for recovery documents and carries JOB-17 retention, and the FSD names it as the integration point of the pack.",
    "FSD A2.3 as a requirement on the pack's content and evidence, with the storage read as P5's capability.",
    "Section 5 CAP-S7-003, CAP-S7-013; Section 6 FR-S7-010, FR-S7-039; Section 9; Section 12 OQ-S7-06",
    "Medium", "Solution architect with the P5 owner, before wave 4 system test",
    "A pack held in two places would let the committee approve one document and the retention test check another.")

asm(7,
    "The agency instruction, the result, the recall and the replacement travel through the rwb-partner contract and the partner portal, and the placement slices are sequenced last inside wave 4 because S9 is created in the same wave.",
    "R-WO-30 to R-WO-35 name the portal for the instruction, the result and the recall, and the program BRD places S9 in wave 4.",
    "FSD A2.15 and A2.16 as the placement behaviour the business needs, with the channel read as S9's portal.",
    "Section 5 CAP-S7-015; Section 6 FR-S7-033, FR-S7-034; Section 9; Section 10.3; Section 12 OQ-S7-07",
    "Medium", "Partner and agency manager with S9, before wave 4 system test",
    "If the portal is not ready inside the wave, the placement is demonstrated last and the rest of the release is unaffected.")

asm(8,
    "A charged-off population is handed to the debt sale route of rwb-debtsale with the population, the route and the approval recorded here, and the case closes when the buyer settles and the data transfer completes.",
    "R-WO-32, R-WO-50 and R-WO-51 give this module the hand-over and the closure on the buyer's settlement and remittance, and S6 owns the lot, the award and the transfer.",
    "FSD A2.16 as the sale behaviour the business needs, with the lot and the award read as S6's capability.",
    "Section 5 CAP-S7-016; Section 6 FR-S7-035, FR-S7-038; Section 9; Section 12 OQ-S7-08",
    "Medium", "Solution architect with the S6 owner, before wave 4 system test",
    "A sale with no recorded hand-over cannot be reconciled to the book it removes.")

asm(9,
    "The write-off states are held as the stage's own record inside WriteOffWorkflow, this service publishes the outcome on rwb.writeoff.events.v1, and rwb-case moves the case state because it owns the case and the parent workflow.",
    "Architecture v5 gives the case state and the parent CaseWorkflow to rwb-case and gives this service one published event.",
    "FSD and Business Rules S7 state machine as the stage's decision record, with the case state read as P3's.",
    "Section 5 CAP-S7-013; Section 6 FR-S7-040; Section 9; Section 12 OQ-S7-09",
    "Medium", "Solution architect with the P3 owner, before wave 4 system test",
    "Two writers of the case state would make the closure and the reopening control unprovable.")

asm(10,
    "JOB-16 runs as a Temporal Schedule in rwb-writeoff on the 3rd working day that also tests that the ALS batch is complete, and no Quartz table, connection or job is used; the Ownership Map ruling on JOB-16 (ASM-A6-flows-12) is carried, not reopened.",
    "Architecture v5 slide 44 and the Temporal design make it a Schedule; the Batch and Scheduling Design starts it on the batch record and the design's Phase 1 note keeps Quartz.",
    "Both conditions as one product requirement: the date the business runs on and the data the rules require.",
    "Section 2.4 constraint 6; Section 6 FR-S7-003; Section 9; Section 12 (no open question; ruled)",
    "High", "Solution architect, before wave 4 system test",
    "A scan that runs on a date without a complete batch would propose a population on stale data.")

asm(11,
    "The eligibility and tax rules are read from a governed package through the rwb-decision contract, the package and rule version are recorded on every scan and decision, and the package code and promotion date are taken as open because they are Phase 2.",
    "All fifty-one rules are versioned data evaluated in process, and the design states that the package codes are Phase 2 with this service as one owner.",
    "R-WO-01 to R-WO-51 as the rule set, with the package identity read as P7's governance.",
    "Section 2.4 constraint 7; Section 5 CAP-S7-014; Section 6 FR-S7-007; Section 10.4; Section 12 OQ-S7-14",
    "Medium", "Center of excellence analyst with P7, before wave 4 release",
    "A scan that cannot name its package cannot be defended to tax or to audit.")

asm(12,
    "The tax criteria and the two tracks are held as a versioned package read at run time, the version is recorded per account, and the scan is held on a published version only; no criterion and no track name is asserted here.",
    "No source read defines the criteria, and the epic BRD carries the same gap as Q-006 with ASM-013.",
    "FSD A2.2 as a requirement that the criteria exist as data with a version, with the values left to their owner.",
    "Section 5 CAP-S7-002; Section 6 FR-S7-004, FR-S7-005, FR-S7-006; Section 12 OQ-S7-10",
    "Medium", "Write-off committee member, before wave 4 release",
    "The scan can be built and tested against a test package; the release is blocked until the real one is published.")

asm(13,
    "The write-off exception loop is owned by the write-off team role until a named owner is decided, and it carries one time limit as a data row rather than a code constant.",
    "The FSD states the loop has no owner today and the epic BRD carries Q-007 with ASM-014 reading it as the write-off team.",
    "ASM-014 as the interim owner, with the time limit as a value nobody has stated.",
    "Section 5 CAP-S7-012; Section 6 FR-S7-030; Section 12 OQ-S7-11",
    "Low", "Head of recovery, before wave 4 release",
    "Without an owner and a limit the loop repeats the finding that its cases do not close.")

asm(14,
    "No write-off cap value, basis or period is asserted, and the population is reported against the cap only once the cap exists; the committee limit of R-WO-11 and R-WO-12 is the only limit this release enforces.",
    "RISK-004 names the cap as undecided and no requirement, rule or field carries it.",
    "The risk as a statement that a cap is expected, not as a value.",
    "Section 6 FR-S7-007; Section 10.4; Section 12 OQ-S7-12",
    "Medium", "Head of Asset Liquidity with Risk, before wave 4 release",
    "Enforcing a guessed cap would hold a population the policy does not require and misstate the headroom.")

asm(15,
    "The committee approval is taken through the approval workflow on rwb-decision, the limit is read from the delegation table at run time, and the level applied and the approver role are recorded; the level values are loaded from the regulation under DL18 and the committee composition is taken as open under Q-001.",
    "Architecture v5 makes the approval an ApprovalWorkflow child with the DoA lookup as a parameter, and the limits are DL18.",
    "FSD A2.5 and A2.6 as the decision the business needs, with the level values read as policy data.",
    "Section 5 CAP-S7-005, CAP-S7-006; Section 6 FR-S7-015, FR-S7-016, FR-S7-020; Section 12 OQ-S7-13",
    "High", "Risk with the product heads, before wave 4 release",
    "A decision taken at the wrong level is an authority breach that the record would then prove.")

asm(16,
    "The write-off posting is a point of no return under strict mode: it waits for rwb-decision to confirm the decision record in the central ledger, proceeds only on that acknowledgement, and raises an alert where the ledger is late.",
    "Architecture v5 slide 28 lists the write-off posting among the four irreversible steps, and the Temporal design repeats it.",
    "FSD A2.9 as the posting behaviour, with the ledger acknowledgement added from the higher-ranked architecture.",
    "Section 2.4 constraint 9; Section 6 FR-S7-029; Section 11 AC-S7-015; Section 12 (no open question; constrained)",
    "High", "Solution architect, before wave 4 system test",
    "A posting on an unconfirmed record is the one error an auditor cannot unwind.")

asm(17,
    "A retention class and a retention period are held as data on every document and every record this service closes on, the closure is held when a class is missing, and the periods themselves stay open under DL26 and Q-012.",
    "NFR-031 sets the closure after the retention period with the target not set, and NFR-028 leaves the periods open.",
    "The closure control as a requirement, with the period read as Compliance's data.",
    "Section 7 NFR-S7-014 to NFR-S7-018; Section 6 FR-S7-039; Section 12 OQ-S7-15",
    "Medium", "Compliance and PDPA officer, before wave 4 release",
    "A closure with no period recorded cannot be defended at a data subject request or a disposal audit.")

asm(18,
    "write_off carries the eleven fields of the Logical Data Model, the three GL-sourced ones are marked as mirrored and never re-keyed, and DEF-05 is taken as open because no source read defines it.",
    "The FSD defers the mirrored GL fields to DEF-05 and lists eight fields; the model holds eleven.",
    "The model as the field set, with the FSD's eight as the subset the screen needs.",
    "Section 8.1; Section 12 OQ-S7-17",
    "Low", "Data architect, before the S7 DB story",
    "A missing field would either re-key the GL coding or lose the recovery position.")

asm(19,
    "The removal reason, the review date, the decision reason and the pack reference are required fields of the eligibility and committee records, held with the physical names the DB story fixes.",
    "Four rules act on those values and neither the FSD catalog nor the model holds them.",
    "The rules as the source of the fields the behaviour needs.",
    "Section 8.1; Section 6 FR-S7-011, FR-S7-018, FR-S7-019; Section 12 (carried in OQ-S7-03)",
    "Medium", "Data architect, before the S7 DB story",
    "Without the fields the removal, the deferral and the refusal cannot be recorded or proved.")

asm(20,
    "The pack is drafted by the write-off agent through the rwb-agent contract under the agent-run template with a 60-second limit and the template pack as the fallback, and the pack itself is the product requirement rather than the agent.",
    "R-WO-05 names the write-off agent, the agent runtime is P10, and the matrix gives S7 no P10 cell.",
    "FSD A2.3 as a requirement on the pack's content, with the draft read as P10's capability.",
    "Section 5 CAP-S7-003; Section 6 FR-S7-009; Section 9; Section 12 (carried in OQ-S7-01 and OQ-S7-06)",
    "Medium", "Solution architect with the P10 owner, before wave 4 system test",
    "A pack that depends on an agent with no fallback stops the committee when the agent is slow.")

asm(21,
    "A payment after charge-off is matched by rwb-payment and reaches this service as ProceedsMatched; this service records the recovery, the income and the agency fee, and shows a payment that matches nothing in its own exception list.",
    "P8 owns payment and proceeds matching and publishes ProceedsMatched to rwb-writeoff, while R-WO-37 to R-WO-39 give the matching to this module.",
    "FSD A2.15 as the recovery behaviour the business needs, with the initial match read as P8's capability.",
    "Section 5 CAP-S7-015; Section 6 FR-S7-036, FR-S7-037; Section 9; Section 12 (carried in OQ-S7-02)",
    "Medium", "Solution architect with the P8 owner, before wave 4 system test",
    "Two matchers of one payment would double-count a recovery or leave it unmatched.")

asm(22,
    "Completeness is published from rwb-reporting, fed by the decision record and WriteOffApproved, and the reconciliation itself stays in this service; no extract to a data lake and no Power BI copy is created.",
    "R-WO-42 names Power BI and Architecture v5 removes the data lake and the extract (ADR-018).",
    "The completeness control as a requirement, with the channel read as P9's read model.",
    "Section 5 CAP-S7-011; Section 6 FR-S7-028; Section 9; Section 12 (carried in OQ-S7-02)",
    "High", "Solution architect, before wave 4 system test",
    "A control published nowhere is a control nobody reads.")

asm(23,
    "SCR-27 is served through a gateway-bff composite route that joins this service's population and pack answer with the case and the document, and no service is named as the screen's owner in this document.",
    "Architecture v5 makes gateway-bff the only entry for staff screens and DP-19 makes the screen a composite route.",
    "FSD Screens as the screen the business needs, with its ownership read as the edge's.",
    "Section 9; Section 12 (carried in OQ-S7-04)",
    "Medium", "Solution architect, before wave 4 release",
    "A screen owned by nobody has no release, no test and no accessibility sign-off.")

asm(24,
    "This version is Draft and its approval table stays empty: no Product Owner decision and no FDA decision exists for the BRD or the FSD this PRD is built from, so no approval is claimed.",
    "The FSD is 'In review' with an empty sign-off table, and no approval record for either document was found in the sources read.",
    "A Draft PRD is a reviewable document; an approval recorded without a decision would be a false record.",
    "Section 1.1; Section 13",
    "Medium", "Product Owner, before the requirements gate",
    "The gate stays open until both roles decide, and every downstream stage inherits the open status.")

asm(25,
    "All release dates are copied unchanged and marked tentative: E3 31 January 2027, E4 28 February 2027, E5 31 March 2027, E6 30 April 2027, E7 31 May 2027 and E8 30 June 2027, with wave 4 covering EP06 to EP08.",
    "U7 and DL48 fix the dates as unchanged and tentative, and a date is never raised as a gap.",
    "The program release plan and the wave map as the schedule, with no date computed here.",
    "Section 1.1; Section 10; Section 11.3",
    "High", "Product Owner, at each release planning point",
    "If a date moves, the slices of section 10 are re-cut and no requirement changes.", gap=0)

asm(26,
    "Every owner named in this document is a role or a service code from the Ownership Map or the BRD; no person is named, and the owners in the delegate tables are roles to be filled.",
    "Rule 4 of the run and U3 of the story rules forbid the name of a person anywhere.",
    "The BRD role list and the Ownership Map service codes as the only owner vocabulary.",
    "Section 3; Section 9; Section 11.3; Section 13",
    "High", "Product Owner, before the requirements gate",
    "A named person in a document is a maintenance defect the moment that person changes role.", gap=0)

def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{path}: {len(rows)} rows")


write(WORK / "gaps" / f"{WP}.jsonl", G)
write(WORK / "assumptions" / f"{WP}.jsonl", A)
