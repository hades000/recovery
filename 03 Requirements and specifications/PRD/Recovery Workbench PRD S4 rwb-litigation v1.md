SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S4 rwb-litigation v1
description: Product requirements for the Recovery Workbench litigation and enforcement service (S4 rwb-litigation) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S4 Litigation and enforcement v3.md
service: S4 rwb-litigation
epic: RWB-SVC-S4
wave: 3
decision: D-RCV-60
---

# Recovery Workbench PRD S4 rwb-litigation v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S4 rwb-litigation |
| Document ID | S4-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft. The BRD is read as approved for this run and the approval itself is carried as an assumption (ASM-2912; ASM-2913) |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S4 rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 (Epic 5, litigation and enforcement, wave 3) |
| Release | 31 March 2027 (tentative) |
| Schema | `rwb_litigation` |
| REST base | `/api/recovery/litigation/v1` |
| Topic | `rwb.litigation.events.v1` |
| Temporal task queue | `rwb-litigation` |
| Workflow | LitigationWorkflow (runs for years; continues-as-new) |
| Java package | `th.co.scb.ace.workbench.recovery.litigation` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S4 |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epics 3 to 8 v1; FSD S4 Litigation and enforcement v3; Architecture v5; Temporal and Drools Design v1 |
| Upstream requirement IDs | REQ-S4-001 to REQ-S4-010; BR-034, BR-035, BR-036, BR-037, BR-038, BR-039, BR-040, BR-041, BR-042, BR-043; REQ-APD-006; rules R-LIT-01 to R-LIT-79 and R-UNI-31; NFR-001, NFR-003, NFR-004, NFR-007, NFR-008, NFR-009, NFR-010, NFR-011, NFR-013, NFR-014, NFR-015, NFR-020, NFR-021, NFR-022, NFR-023, NFR-024, NFR-025, NFR-026, NFR-027, NFR-028, NFR-029, NFR-031, NFR-033, NFR-034, NFR-035, NFR-037, NFR-039, NFR-040, NFR-042, NFR-043, NFR-045, NFR-046, NFR-047, NFR-049, NFR-050, NFR-051, NFR-052, NFR-053, NFR-054, NFR-055, NFR-057, NFR-059, NFR-060, NFR-061, NFR-064, NFR-067, NFR-068, NFR-072, NFR-076 |
| Upstream acceptance criteria | AC-S4-001-01 to AC-S4-022-01 (main success flow, one per feature); AC-EXC-S4-001-01 to AC-EXC-S4-022-01 (role without the right); AC-EXC-S4-001-02 to AC-EXC-S4-022-02 (decision cannot be recorded). The FSD defines no alternate flow and no system background event for any of the twenty-two features (GAP-1743; ASM-2905) |
| Generated IDs | CAP-S4-001 to CAP-S4-025; FR-S4-001 to FR-S4-057; NFR-S4-001 to NFR-S4-034; AC-S4-001 to AC-S4-040; JRN-S4-01 to JRN-S4-07; ROL-S4-01 to ROL-S4-13; OQ-S4-01 to OQ-S4-17 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S4 Litigation and enforcement v3 (15 November 2026) and Business Requirements Epics 3 to 8 v1, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S4 Litigation and enforcement v3. Its requirement IDs, feature IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the owner of the notice content and proof of delivery, the calls that are Temporal rather than in-process, and the wave in which the notice slice lands, not the requirement substance. The CAP, FR, NFR, AC, journey, role and open-question IDs of this document are new and exist only here (ASM-2917).

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only; legal_action mirrored LIT fields left for DEF-05. Everything else unchanged from v2 |
| 1 and 2 | Not specified in the source documents (GAP-1749; ASM-2911) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey and open-question IDs are new; the FSD requirement IDs (REQ-S4-001 to REQ-S4-010), feature IDs (FEAT-LIT-01 to FEAT-LIT-22), validation rule IDs (VR-S4-001-1 to VR-S4-022-1 and VR-S4-006-2, VR-S4-013-2), business rule IDs (BR-S4-001 to BR-S4-022), acceptance criteria IDs (AC-S4-001-01 to AC-S4-022-01 and their exception rows), rule IDs R-LIT-03 to R-LIT-70, message IDs (MSG-S4-001, MSG-S4-002, MSG-GEN-001, MSG-P1-001, MSG-P4-002, MSG-P7-003), list ID (LOV-LEGAL-TYPE) and screen IDs (SCR-18, SCR-19, SCR-20) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S4-001 to REQ-S4-010 and of the non-functional requirements |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-034 to BR-043, the E5 scope, the measures, the risks and the open questions |
| Recovery Workbench Functional Specifications by Module v6, FSD S4 Litigation and enforcement v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: LitigationWorkflow on `rwb-litigation` running for years and continuing as new, the approval, notice and partner children, the prescription clock and the 79-rule litigation set |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow, table and job named here |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-litigation (S4) is the recovery module's legal action. It turns "notice, pack, firm, court, judgment, enforcement" into a product: a statutory notice that is generated by rule, approved and dispatched, with its period timed from proof of delivery rather than from posting; a litigation pack assembled from the document index and tested against the known defect list before an officer signs it; a law firm chosen from the panel by measured score, capacity, court and conflict, and instructed with the pack through the portal; court dates, hearings, deadlines and fees held on the case instead of in an inbox; a settlement, an appeal and a fee that each carry the approval the limit names; a judgment recorded once, with one named owner from judgment to the end of enforcement; an enforcement that traces an asset, applies for the writ, follows the statutory auction ladder and matches what it recovers to the case; and a prescription clock that never pauses and warns before the claim expires.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-litigation | One deployable with its own API and worker, schema `rwb_litigation`, login, topic `rwb.litigation.events.v1`, task queue `rwb-litigation` and lifecycle | The legal action becomes one owned product with its own release, instead of a screen inside a single deployable |
| LitigationWorkflow | One workflow per legal action, a child of the case workflow, running for years and continuing as new | A court case outlives a workflow history, and a durable timer is the only clock that survives a redeploy |
| The litigation pack as a governed record | The pack as one set, with the documents, their versions, the case facts it was built from and the defect list result | A pack filed with a known defect is the defect rate the programme exists to remove |
| Firm selection and instruction as product behaviour | The panel rule applied on scorecard, capacity, court and conflict, the instruction issued through the partner portal, and a partner clock with a breach path | Firm selection by habit is the largest uncontrolled legal cost |
| The court calendar on the case | Hearings, deadlines and fees tracked, each deadline raised as a task, each fee accrued against the case | Deadlines missed by email reading are the litigation turnaround |
| One enforcement owner | A named role on the case from judgment to the end of enforcement, with a deferral that carries a coded reason and a review date | Enforcement after judgment has no owner today, which is where recovery stops |
| The statutory ladder as product behaviour | The LED auction tracked through 100, 90, 80 and 70 percent of official value with each round, its price basis and its result | The ladder is the statutory price path, and a ladder run by hand is a price run by memory |
| The prescription clock as a durable timer | A clock that is never paused, a warning ahead of the legal deadline, and an escalation at 90 days or less | A missed prescription is a debt that can never be recovered |
| The legal action as an event | LawsuitFiled, JudgmentRecorded and AuctionResult on `rwb.litigation.events.v1`, consumed by rwb-asset and rwb-case | The case and the asset move on the legal step in the same transaction, not on a poll |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion of LIT lawsuit and hearing data and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of every data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract; GAP-1736; ASM-2898) |
| Notice content, merge fields, template versions and proof of delivery | REUSE, elsewhere | P6 rwb-comms (GAP-1740; ASM-2902) |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (LitigationWorkflow is its child workflow) |
| Approval workflow, decision record, hash chain and rule package registry | REUSE | P7 rwb-decision |
| Roles, capability areas, masking policy and the delegation table | REUSE | P4 rwb-access |
| Document hub, custody, write-once container and retention | REUSE | P5 rwb-document (GAP-1737; ASM-2899) |
| Law firm master data, the panel, the portal account and the firm's instruction queue | REUSE, elsewhere | S9 rwb-partner |
| Payment, posting to ALS and the general ledger, and proceeds matching | REUSE | P8 rwb-payment (GAP-1737; ASM-2899) |
| Next-step agent runtime, model endpoint, guardrails and run record | REUSE | P10 rwb-agent (GAP-1737; ASM-2899) |
| Screens and the composite route that serves them | REUSE | Platform edge, gateway-bff (RWB-PLT-EDGE); GAP-1747; ASM-2909 |
| Quartz scheduler and its shared tables | REPLACED | Temporal workflow kit (PLT); ADR-016, DP-10 (GAP-1736; ASM-2898) |
| Embedded Drools with the litigation rule set evaluated in the monolith | MOVED | P7 for governance and versioning; evaluation stays local in this service (ADR-017, DP-04; GAP-1742; ASM-2904) |
| Debt sale lot building and the buyer data room | REUSE, elsewhere | S6 rwb-debtsale (E5 scope, this service is not the owner) |
| Collections before day 90 and decisions D1 to D4 | OUT OF SCOPE | EFS and the ACE collection module |
| Booking in the core bank, ALS posting and credit approval | OUT OF SCOPE | The officer, ALS and the lending system; this service records the result |
| The court's own process, the Legal Execution Department's own process and the firm's internal process | OUT OF SCOPE | The court, the LED and each firm |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 37 and 45).
2. The service writes only schema `rwb_litigation`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. A route service reaches a shared capability through Temporal, never REST; this service's synchronous calls are REST from gateway-bff only (slide 13, ADR-020).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slide 10; slide 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.litigation.events.v1`, key `caseId` (ADR-015, DP-09, DP-14; slides 9 and 11).
6. Temporal namespace `rwb-recovery`, task queue `rwb-litigation`; LitigationWorkflow is a child of the case workflow with parent close policy ABANDON so the stage survives the parent's Continue-As-New; Schedules and durable timers replace Quartz (ADR-016, DP-10, DP-12; slide 19).
7. Rules are versioned data evaluated in process by the embedded Drools kit; authoring, testing and promotion are governed in rwb-decision (ADR-017, DP-04).
8. There is no data lake: litigation measures and reporting read the decision record and the events into rwb-reporting (ADR-018, DP-17).
9. Personal data stays out of events, workflow inputs and logs; masking is by role, using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
10. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the case journey (slide 32).
11. The connection matrix gives this service Temporal calls to rwb-decision, rwb-comms and rwb-partner, and events from rwb-case, rwb-comms and rwb-partner; it gives no cell to rwb-source-data, rwb-document, rwb-payment or rwb-agent (slide 13; GAP-1736 and GAP-1737; ASM-2898 and ASM-2899).

# 3. Personas and roles

Roles only; no person is named anywhere in this document (ASM-2916).

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S4-01 | Litigation officer | A notice that went out, a pack that passes the defect list, and a court calendar that tells them what is due | JRN-S4-01, JRN-S4-02, JRN-S4-03, JRN-S4-04 |
| ROL-S4-02 | Head of Litigation | Substituted service and filing signed off where the law allows, the prescription escalation, and every settlement, appeal and fee inside the limit | JRN-S4-03, JRN-S4-05, JRN-S4-06 |
| ROL-S4-03 | Legal counsel | The pack as it was filed, the notice as it was served, and the judgment and appeal record | JRN-S4-02, JRN-S4-05, JRN-S4-06, JRN-S4-07 |
| ROL-S4-04 | Enforcement owner | One case from judgment to the end of enforcement, the traced assets, the ladder and the deferral with its review date | JRN-S4-06 |
| ROL-S4-05 | Product head (Mortgage, HP, SSME) | Settlements and fees inside the delegation for the product, and the exceptions named | JRN-S4-05 |
| ROL-S4-06 | Credit approval committee member | A settlement or appeal pack that states the amount, the cost, the effect and the recommendation | JRN-S4-05 |
| ROL-S4-07 | Partner and agency manager | The panel, the firm's acceptance, the partner clock and the breach | JRN-S4-03, JRN-S4-04 |
| ROL-S4-08 | Law firm user (external role) | The instruction and the pack, and a place to return the receipt, the court number and the round result | JRN-S4-04, JRN-S4-06 |
| ROL-S4-09 | Credit administration | The enforcement proceeds matched to the case and posted | JRN-S4-06 |
| ROL-S4-10 | Compliance and PDPA officer | Masking by role, an access log that cannot be skipped, write-once legal documents and a legal hold that overrides retention | JRN-S4-07 |
| ROL-S4-11 | Internal audit | A legal action reproducible from the log with its rule version, its approval level and its approver | JRN-S4-07 |
| ROL-S4-12 | Platform administrator | A workflow that reports a breach, an alert with a named owner, and a replay path | JRN-S4-03, JRN-S4-06 |
| ROL-S4-13 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S4-07 |

Non-human actors: the case workflow that starts LitigationWorkflow; the approval workflow on rwb-decision; the notice child on rwb-comms; the instruction activity on rwb-partner; the next-step agent on rwb-agent; the outbox relay; the consumers of LawsuitFiled, JudgmentRecorded and AuctionResult. The law firm is reached through the partner gateway at the edge and never by a direct call from this service.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. The notice is produced from a template a person selects, and the notice period is counted from the posting date because nothing records when it was delivered.
2. The litigation pack is assembled by hand from the document store; a missing document is found at filing, and the filing is returned.
3. The law firm is chosen by habit and instructed by email; the firm's progress is not tracked anywhere on the case.
4. Court dates, hearings, deadlines and fees are held in a spreadsheet and in the firm's own system, and read by a person.
5. A judgment is recorded on the case, and enforcement after judgment has no owner, so the case stops.
6. The prescription clock runs in a report, and a claim approaching expiry does not force a review ahead of the other open actions.

Consequence: filing takes 21 days, packs arrive with known defects, and no one can say where a case is in the court process.

## 4.2 Target state (this product)

### JRN-S4-01 Notice from generation to the period expiring (on trigger, litigation officer)

1. The case reaches the litigation route, or a restructure or settlement plan breaks; rwb-case starts LitigationWorkflow on this service.
2. The service reads the template status for the product and the notice type; a current template generates the demand and recall notice, and a withdrawn template holds generation and raises a task to the litigation officer.
3. The notice decision and its approval leave to rwb-comms, which owns the template, the merge fields and the delivery; the case records the template version and the approver.
4. The proof of delivery arrives from rwb-comms as NoticeDelivered; a delivered result attaches the proof and starts the notice period from the delivery date, and any other result marks the notice unserved and queues an alternate service method.
5. The notice period runs as a durable timer in LitigationWorkflow. When it expires with no cure and no dispute, pack assembly opens.

### JRN-S4-02 Pack assembly, the defect check and the missing document (daily, litigation officer and legal counsel)

1. The pack is assembled from the document index through the document contract and from the case facts, and the record states which document version and which case facts it was built from.
2. The pack is tested against the defect list in force; every missing item is named, and the pack cannot go for filing approval while one is open.
3. A document the pack needs and the bank cannot find opens its recovery path on the case, and the pack is re-checked when it is supplied, re-signed or re-created.
4. The litigation officer sees the pack, the defects and the evidence behind each item before signing.

### JRN-S4-03 Verify the pack, approve the filing and instruct the firm (daily, litigation officer and Head of Litigation)

1. The litigation officer verifies the pack; a verification with every defect list item present moves it to verified, and a rejection returns it to its owner with the defects named.
2. Where 90 days or less remain to prescription, the filing waits for the Head of Litigation to approve substituted service or filing, as the law allows.
3. The law firm is selected from the panel by rule on scorecard, capacity, court and conflict; a decline or a silence inside the window re-selects the next firm.
4. The Head of Litigation may nominate a firm or widen the panel with a reason, and the instruction uses that firm.
5. The instruction and the pack leave through the partner portal, and the partner clock starts.

### JRN-S4-04 The court calendar (daily, litigation officer and firm user)

1. The firm returns the filing receipt and the court case number through the portal; the number is written to the legal action and the hearing timers are set.
2. A court that returns the filing for a defect records the defect and returns the pack for rework.
3. Hearings, deadlines and fees are held against the legal action, each deadline raises its task before it falls due, and each fee is accrued to the case.
4. The next litigation step is proposed with its reasons, its cost and its effect, and the officer or the approver decides.

### JRN-S4-05 Settlement, appeal and fees inside the delegation (on trigger, litigation officer and committee)

1. A settlement proposed before judgment goes to the approver named by the limit, with the proposed step, its cost and its effect.
2. An approved settlement inside the D7.4 limit books the treatment and holds the litigation rather than withdrawing it; above the limit the committee approves and its level is recorded.
3. A rejection with a reason continues the case to judgment; a settlement that breaks later resumes the litigation.
4. An appeal records its decision, its grounds and the approval the limit names, and is tracked to its end.
5. A court fee or a legal expense is checked against the fee schedule in force and is paid only on approval, with the schedule version recorded.

### JRN-S4-06 Judgment, enforcement, deferral and proceeds (months or years, enforcement owner and legal counsel)

1. The judgment is recorded with its date and amount, the enforcement task opens, and the enforcement owner role is named on the case from judgment to the end.
2. Assets are traced across the bureau, internal data, the registries and insurers, and the enforcement decision is presented with what was traced.
3. The firm is instructed to apply for the writ and the seizure, and the enforcement auction follows the 100, 90, 80 and 70 percent steps of official value.
4. A step that cannot proceed is deferred only with a coded reason and a review date, and the case returns on that date.
5. A bankruptcy petition goes to the approver at D7.5 when enforcement is exhausted and the test is met, and is filed through the firm.
6. Proceeds are matched to the case and posted, and the enforcement and the case close when the proceeds cover the judgment total and the costs.

### JRN-S4-07 Evidence and measures read later (audit, Compliance and developer)

1. An auditor reads one legal action: the notice and its proof, the pack and its defect result, the firm and the instruction, each deadline and fee, the settlement or appeal with its level and approver, the judgment, each enforcement step and each deferral, and the rule version applied at each step.
2. Compliance reads the masking matrix, the access log per personal field, and the write-once and legal hold state of every legal document.
3. The business reads the litigation turnaround from the decision log rather than from a separate count.
4. A developer builds against the published contract and its fake; a build that reads an ACE view or an ACE table directly fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic. No capability of this module is Should.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S4-001 | Demand and recall notice generated by rule and approved | A notice goes out from the approved template for the product and the notice type, and a withdrawn template blocks it with a task | BR-034 | Must | 2 | FEAT-LIT-01 (A2.1) |
| CAP-S4-002 | Proof of delivery and the service result | The notice period starts from delivery, and a refused, returned or undeliverable notice opens an alternate service path | BR-034 | Must | 2 | FEAT-LIT-02 (A2.2) |
| CAP-S4-003 | Notice period as a durable timer | The statutory period is a clock the workflow holds, and it expires into pack assembly | BR-034 | Must | 2 | FEAT-LIT-03 (A2.3) |
| CAP-S4-004 | Litigation pack assembly | The pack exists as one set with its documents, their versions and the case facts behind it | BR-035 | Must | 3 | FEAT-LIT-04 (A2.4) |
| CAP-S4-005 | Defect list check | Each missing item is named before the pack reaches an officer, and the pack is re-checked after a correction | BR-035 | Must | 3 | FEAT-LIT-05 (A2.5) |
| CAP-S4-006 | Missing or lost document recovery | A document the pack needs and the bank cannot find has a path, an owner and a result on the case | BR-035 | Must | 3 | FEAT-LIT-06 (A2.6) |
| CAP-S4-007 | Pack verification and filing approval | The officer's signature is given against a checked pack, and a rejected pack returns with the defects named | BR-036 | Must | 3 | FEAT-LIT-07 (A2.7) |
| CAP-S4-008 | Law firm selected from the panel by rule | The firm is chosen on scorecard, capacity, court and conflict, and a decline re-selects | BR-037 | Must | 3 | FEAT-LIT-08 (A2.8) |
| CAP-S4-009 | Firm instruction through the portal with a partner clock | The instruction and the pack reach the firm on the case, and a firm that does not file is breached and replaced | BR-037 | Must | 3 | FEAT-LIT-09 (A2.9) |
| CAP-S4-010 | Court filing and receipt | The court number and the receipt are on the case, and a returned filing comes back with its defect | BR-038 | Must | 3 | FEAT-LIT-10 (A2.10) |
| CAP-S4-011 | Hearings, deadlines and fees on the case | Every court date and deadline raises its task, and every fee accrues against the case | BR-039 | Must | 3 | FEAT-LIT-11 (A2.11) |
| CAP-S4-012 | Next litigation step recommended with reasons | The officer and the approver see why a step is proposed, what it costs and what it changes | BR-039 | Must | 3 | FEAT-LIT-12 (A2.12) |
| CAP-S4-013 | Settlement before judgment inside the delegation | A settlement at court goes to the limit that applies, holds the litigation rather than withdrawing it, and resumes it when it breaks | BR-040 | Must | 3 | FEAT-LIT-13 (A2.13) |
| CAP-S4-014 | Appeal decided, approved and tracked | The appeal carries its grounds and its approval, and is followed to its end | BR-040 | Must | 3 | FEAT-LIT-14 (A2.14) |
| CAP-S4-015 | Court fees and legal expenses paid on approval | A fee is checked against the schedule and paid only on the approval the limit names | BR-040 | Must | 3 | FEAT-LIT-15 (A2.15) |
| CAP-S4-016 | Judgment recorded and enforcement opened with one owner | The judgment date and amount are on the case, and one role owns enforcement from judgment to the end | BR-041 | Must | 3 | FEAT-LIT-16 (A2.16) |
| CAP-S4-017 | Assets traced for enforcement | The bureau, internal data, the registries and the insurers are searched, and the result is presented before an action | BR-042 | Must | 3 | FEAT-LIT-17 (A2.17) |
| CAP-S4-018 | Writ and seizure applied for through the firm | The writ and the seizure are instructed and tracked to execution | BR-042 | Must | 3 | FEAT-LIT-18 (A2.18) |
| CAP-S4-019 | LED auction ladder | The enforcement auction follows 100, 90, 80 and 70 percent of official value, and a round with no bid is referred | BR-042 | Must | 3 | FEAT-LIT-19 (A2.19) |
| CAP-S4-020 | Enforcement deferral with a coded reason and a review date | A step that cannot proceed is deferred on purpose and comes back on its date | BR-041 | Must | 3 | FEAT-LIT-20 (A2.20) |
| CAP-S4-021 | Bankruptcy petition through the approver and the firm | An exhausted enforcement with a met test goes to D7.5 and is filed | BR-042 | Must | 3 | FEAT-LIT-21 (A2.21) |
| CAP-S4-022 | Enforcement proceeds matched, posted and closed | Money from the LED or the firm reaches the case, the enforcement closes and the record is retained | BR-043 | Must | 3 | FEAT-LIT-22 (A2.22) |
| CAP-S4-023 | Prescription watch ahead of every other action | The legal deadline never pauses, warns before it falls due and escalates at 90 days or less | BR-034 | Must | 3 | A2.3 (VR-S4-003-1); A2.7 (R-LIT-11); A2.13 (VR-S4-013-2) |
| CAP-S4-024 | Data date and freshness at every step | Every step states how old its data is, and a stale product is seen rather than assumed | BR-039 | Must | 3 | VR-S4-001-1 to VR-S4-022-1 |
| CAP-S4-025 | One litigation decision record per step | Each step answers an audit question with its rule version, its inputs, its approval and its approver | BR-036, BR-041 | Must | 3 | A2.1 to A2.22 (the decision log entry of every step) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE lawsuit, hearing and batch-status data | Not carried | rwb-source-data's contract (GAP-1736; ASM-2898) |
| Notice content, merge fields, template versions and proof of delivery | Not carried | P6 rwb-comms (GAP-1740; ASM-2902) |
| Document custody, the write-once container and retention | Reused, elsewhere | P5 rwb-document (GAP-1737; ASM-2899) |
| Firm master data, the panel, the portal account and the firm's queue | Reused, elsewhere | S9 rwb-partner |
| Payment, ALS and general ledger posting, and proceeds reconciliation | Reused, elsewhere | P8 rwb-payment (GAP-1737; ASM-2899) |
| Next-step agent runtime, model endpoint and guardrails | Reused, elsewhere | P10 rwb-agent (GAP-1737; ASM-2899) |
| Quartz scheduling of the notice period and the hearing timers | Replaced | Durable timers in LitigationWorkflow through the workflow kit (GAP-1736; ASM-2898; DP-10) |
| The litigation rules as Excel decision tables in the monolith | Moved | Governance in P7 rwb-decision; evaluation local, litigation package in Phase 2 (GAP-1742; ASM-2904) |
| Debt sale lot building and the buyer data room | Reused, elsewhere | S6 rwb-debtsale (E5 scope, not this service) |
| The court's process, the LED's process and the firm's internal process | Out of scope | The court, the LED and each firm |
| Booking in the core bank and credit approval | Out of scope | The officer, ALS and the lending system |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the source requirement row of the FSD; where the FSD serves a BRD requirement through features with no REQ row of their own, the column says so and the BR column carries the trace. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-S4-001 | The service SHALL generate the demand and recall notice from the Legal-approved template when the template status is current for the product and the notice type (R-LIT-03), and SHALL move the case to NOTICE_DISPATCHED. | CAP-S4-001 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-002 | The service SHALL hold generation and raise a task to the litigation officer when the template status is withdrawn (R-LIT-04), SHALL move the case to NOTICE_BLOCKED, and SHALL let no notice leave the bank from a withdrawn template. | CAP-S4-001 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-003 | The service SHALL issue the notice decision and its approval to the comms child on rwb-comms, and SHALL record on the case the template version, the notice type and the approver the notice left on; the notice content, the merge fields and the delivery are rwb-comms's (GAP-1740; ASM-2902). | CAP-S4-001 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-004 | The service SHALL record the approval of a generated notice with the approving role before dispatch, and SHALL refuse dispatch of a notice with no approval on the record. | CAP-S4-001 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-005 | The service SHALL attach the proof of delivery and start the notice period from the delivery date when the served result is delivered (R-LIT-07), and SHALL move the case to WITH_CUSTOMER_NOTICE_PERIOD. | CAP-S4-002 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-006 | The service SHALL mark the notice unserved and start no notice period when no proof returns inside the proof window (R-LIT-08), SHALL move the case to NOTICE_UNSERVED, and SHALL show the window that was applied. | CAP-S4-002 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-007 | The service SHALL record the served result and queue an alternate service method when the served result is refused, returned or undeliverable (R-LIT-09), and SHALL move the case to NOTICE_UNSERVED. | CAP-S4-002 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-008 | The service SHALL open pack assembly when the notice period expires with no cure and no dispute (R-LIT-15), and SHALL move the case to PACK_ASSEMBLY. | CAP-S4-003 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-009 | The service SHALL hold the notice period as a durable timer inside LitigationWorkflow through the workflow kit, SHALL resume the timer where it stopped after a restart, and SHALL use no Quartz table, connection or job (GAP-1736; ASM-2898; DP-10). | CAP-S4-003 | BR-034 | REQ-S4-001 | Must | 2 |
| FR-S4-010 | The service SHALL assemble the litigation pack from the document index through the document contract and from the case facts, and SHALL record the pack with the document versions and the case facts it was built from. | CAP-S4-004 | BR-035 | REQ-S4-002 | Must | 3 |
| FR-S4-011 | The service SHALL re-run the defect list check when a missing item is supplied, re-signed or re-created (R-LIT-18), and SHALL return the case to PACK_ASSEMBLY with the check result. | CAP-S4-004 | BR-035 | REQ-S4-002 | Must | 3 |
| FR-S4-012 | The service SHALL test the pack against the defect list in force, SHALL name every missing item with MSG-S4-001 (VR-S4-005-1), and SHALL not present a pack to filing approval while an item is open. | CAP-S4-005 | BR-035 | REQ-S4-002 | Must | 3 |
| FR-S4-013 | The service SHALL re-run the defect list check and re-file when the defect is corrected (R-LIT-32), and SHALL return the case to PACK_ASSEMBLY with the corrected result. | CAP-S4-005 | BR-035 | REQ-S4-002 | Must | 3 |
| FR-S4-014 | The service SHALL open the recovery path for a document the pack needs and the bank cannot find, through the document contract, and SHALL record the request, its owner role and its result on the case. | CAP-S4-006 | BR-035 | REQ-S4-002 | Must | 3 |
| FR-S4-015 | The service SHALL refuse any action of this module with MSG-P4-002 where the user's role lacks the capability area (VR-S4-006-2), and SHALL change nothing on the case, the pack or the legal action on a refusal. | CAP-S4-006 | BR-036 | REQ-S4-002 | Must | 3 |
| FR-S4-016 | The service SHALL present the pack to the litigation officer and SHALL move the case to PACK_VERIFIED only when the officer verifies it and every defect list item is present (R-LIT-16). | CAP-S4-007 | BR-036 | REQ-S4-003 | Must | 3 |
| FR-S4-017 | The service SHALL return the pack to its owner for rework with the named defects when the officer rejects it at verification (R-LIT-21), and SHALL return the case to PACK_ASSEMBLY. | CAP-S4-007 | BR-036 | REQ-S4-003 | Must | 3 |
| FR-S4-018 | The service SHALL hold the filing where 90 days or less remain to prescription until the Head of Litigation approves substituted service or filing as the law allows (R-LIT-11), and SHALL record the approval with its reason. | CAP-S4-007 | BR-036 | REQ-S4-003 | Must | 3 |
| FR-S4-019 | The service SHALL select the law firm by rule from the panel on scorecard, capacity, court region, case type and conflict when the pack is verified (R-LIT-23), and SHALL move the case to FIRM_SELECTION. | CAP-S4-008 | BR-037 | REQ-S4-004 | Must | 3 |
| FR-S4-020 | The service SHALL record a decline and re-select the next firm on the scorecard when the firm declines or does not accept inside the window (R-LIT-27), and SHALL move the case to FIRM_DECLINED with the reason. | CAP-S4-008 | BR-037 | REQ-S4-004 | Must | 3 |
| FR-S4-021 | The service SHALL record a firm nominated or a panel widened by the Head of Litigation with the role, the reason and the date, and SHALL use that firm for the instruction (R-LIT-26). | CAP-S4-008 | BR-037 | REQ-S4-004 | Must | 3 |
| FR-S4-022 | The service SHALL issue the instruction and the pack through the partner portal contract when the panel firm covers the court region and the case type and passes the conflict check (R-LIT-24), and SHALL move the case to FIRM_INSTRUCTED. | CAP-S4-009 | BR-037 | REQ-S4-004 | Must | 3 |
| FR-S4-023 | The service SHALL start the partner clock with the instruction, and SHALL mark the instruction breached, notify the partner manager and re-select when it is past due with no filing (R-LIT-28), moving the case to FIRM_DECLINED. | CAP-S4-009 | BR-037 | REQ-S4-004 | Must | 3 |
| FR-S4-024 | The service SHALL write the court case number and the filing receipt to the legal action and set the hearing timers when the firm submits the receipt and the court case number (R-LIT-30), and SHALL move the case to FILED_IN_COURT. | CAP-S4-010 | BR-038 | No REQ row; BR-038 serves FEAT-LIT-10 | Must | 3 |
| FR-S4-025 | The service SHALL record the defect and return the pack for rework when the court returns the filing for a defect (R-LIT-31), and SHALL move the case to FILING_REJECTED. | CAP-S4-010 | BR-038 | No REQ row; BR-038 serves FEAT-LIT-10 | Must | 3 |
| FR-S4-026 | The service SHALL match the court case number the firm submits to the lawsuit record ACE ingests from LIT, and SHALL raise a difference for a person rather than overwrite either record. | CAP-S4-010 | BR-038 | No REQ row; BR-038 serves FEAT-LIT-10 | Must | 3 |
| FR-S4-027 | The service SHALL track every hearing date, deadline and fee against the legal action, SHALL raise a task ahead of each deadline, and SHALL accrue each fee to the case with its source. | CAP-S4-011 | BR-039 | REQ-S4-005 | Must | 3 |
| FR-S4-028 | The service SHALL hold the hearing data read from LIT and the hearing data entered by the firm as two records of one hearing, and SHALL show which of the two a hearing, a date and a fee came from. | CAP-S4-011 | BR-039 | REQ-S4-005 | Must | 3 |
| FR-S4-029 | The service SHALL recommend the next litigation step with its reasons, its cost and its effect through the agent contract, SHALL wait at most 60 seconds for the answer, and where the answer is late or fails its schema check SHALL use the rule result and still present a step. | CAP-S4-012 | BR-039 | REQ-S4-005 | Must | 3 |
| FR-S4-030 | The service SHALL route a settlement proposed before judgment to the approver named by the limit, with the proposed step, its cost and its effect (R-LIT-36), and SHALL move the case to SETTLEMENT_OFFERED_AT_COURT. | CAP-S4-013 | BR-040 | REQ-S4-006 | Must | 3 |
| FR-S4-031 | The service SHALL book the treatment and hold the litigation rather than withdraw it when the settlement is inside the D7.4 limit or the committee approves above it (R-LIT-37), and SHALL move the case to LITIGATION_HELD. | CAP-S4-013 | BR-040 | REQ-S4-006 | Must | 3 |
| FR-S4-032 | The service SHALL continue the case to judgment, recording the reason, when the approver rejects the settlement (R-LIT-38), and SHALL move the case to IN_HEARING. | CAP-S4-013 | BR-040 | REQ-S4-006 | Must | 3 |
| FR-S4-033 | The service SHALL resume the litigation when a settlement reached at court breaks (R-LIT-40), SHALL keep the judgment path open, and SHALL record the rule that resumed it. | CAP-S4-013 | BR-040 | REQ-S4-006 | Must | 3 |
| FR-S4-034 | The service SHALL record the appeal decision, its grounds and the approval the limit names (VR-S4-014-1), and SHALL track the appeal to its end with its own timers. | CAP-S4-014 | BR-040 | REQ-S4-006 | Must | 3 |
| FR-S4-035 | The service SHALL apply the appeal outcome to the legal action and the judgment position, and SHALL keep the earlier judgment and its evidence readable. | CAP-S4-014 | BR-040 | REQ-S4-006 | Must | 3 |
| FR-S4-036 | The service SHALL check each court fee and legal expense against the fee schedule in force, SHALL pay it on approval through the payment contract with the amount and the schedule version recorded, and SHALL hold a fee outside the schedule rather than pay it. | CAP-S4-015 | BR-040 | REQ-S4-006 | Must | 3 |
| FR-S4-037 | The service SHALL record the judgment date and amount and open the enforcement task when the judgment type is full, partial or default (R-LIT-44), and SHALL move the case to JUDGMENT_RECORDED. | CAP-S4-016 | BR-041 | REQ-S4-007 | Must | 3 |
| FR-S4-038 | The service SHALL record a dismissal and open the appeal window when the judgment type is dismissed (R-LIT-45), and SHALL move the case to JUDGMENT_DISMISSED. | CAP-S4-016 | BR-041 | REQ-S4-007 | Must | 3 |
| FR-S4-039 | The service SHALL name the enforcement owner role on the case from judgment to the end of enforcement, and SHALL show that role and its tasks at every enforcement step. | CAP-S4-016 | BR-041 | REQ-S4-007 | Must | 3 |
| FR-S4-040 | The service SHALL publish JudgmentRecorded on `rwb.litigation.events.v1` keyed by the case for rwb-asset and rwb-case, in the same transaction as the judgment record. | CAP-S4-016 | BR-041 | REQ-S4-007 | Must | 3 |
| FR-S4-041 | The service SHALL trace assets across the bureau, internal data, the registries and the insurers when a judgment is recorded (R-LIT-50), SHALL move the case to ASSET_TRACE, and SHALL record each source searched and its date. | CAP-S4-017 | BR-042 | No REQ row; BR-042 serves FEAT-LIT-17 to FEAT-LIT-21 | Must | 3 |
| FR-S4-042 | The service SHALL present the enforcement decision with the traced assets when one or more assets are traced (R-LIT-52), and where no asset is traced SHALL close the enforcement with a recorded reason rather than leave the case open. | CAP-S4-017 | BR-042 | No REQ row; BR-042 serves FEAT-LIT-17 to FEAT-LIT-21 | Must | 3 |
| FR-S4-043 | The service SHALL instruct the firm to apply for the writ and the seizure when an asset is traced and enforcement is economic (R-LIT-54), SHALL move the case to WRIT_AND_SEIZURE, and SHALL track it to execution. | CAP-S4-018 | BR-042 | No REQ row; BR-042 serves FEAT-LIT-17 to FEAT-LIT-21 | Must | 3 |
| FR-S4-044 | The service SHALL follow the enforcement auction through the 100, 90, 80 and 70 percent steps of official value, SHALL record each round with its price basis and its result, and SHALL refuse a price step outside the ladder. | CAP-S4-019 | BR-042 | No REQ row; BR-042 serves FEAT-LIT-17 to FEAT-LIT-21 | Must | 3 |
| FR-S4-045 | The service SHALL record the unsold result and refer it to the enforcement owner when a round draws no bid at 70 percent of official value (R-LIT-67), and SHALL move the case to NO_BID_AT_70. | CAP-S4-019 | BR-042 | No REQ row; BR-042 serves FEAT-LIT-17 to FEAT-LIT-21 | Must | 3 |
| FR-S4-046 | The service SHALL record an enforcement deferral only when a coded reason and a review date are both present (R-LIT-55), SHALL move the case to DEFERRAL_RECORDED, and SHALL re-queue the case on the review date. | CAP-S4-020 | BR-041 | REQ-S4-008 | Must | 3 |
| FR-S4-047 | The service SHALL route the bankruptcy petition to the approver at D7.5 when enforcement is exhausted and the bankruptcy test is met (R-LIT-58), SHALL move the case to BANKRUPTCY_PETITION, and SHALL file it through the firm. | CAP-S4-021 | BR-042 | No REQ row; BR-042 serves FEAT-LIT-17 to FEAT-LIT-21 | Must | 3 |
| FR-S4-048 | The service SHALL match the proceeds to the case when a round is sold at 100, 90, 80 or 70 percent of official value (R-LIT-65), SHALL move the case to PROCEEDS_MATCHED, and SHALL post them through the payment contract. | CAP-S4-022 | BR-043 | REQ-S4-010 | Must | 3 |
| FR-S4-049 | The service SHALL close the enforcement and the case, retaining the record after close, when the proceeds cover the judgment total and the costs (R-LIT-70), and SHALL close on a payment after judgment that covers the balance and the costs (R-LIT-51). | CAP-S4-022 | BR-043 | REQ-S4-010 | Must | 3 |
| FR-S4-050 | The service SHALL publish AuctionResult when a round is settled and LawsuitFiled when the filing is recorded, both on `rwb.litigation.events.v1` keyed by the case (GAP-1744; ASM-2906). | CAP-S4-022 | BR-043 | REQ-S4-010 | Must | 3 |
| FR-S4-051 | The service SHALL hold the prescription clock as a durable timer that is never paused, SHALL raise MSG-S4-002 with the expiry date at the warning point ahead of the legal deadline (VR-S4-003-1), and SHALL show the expiry date on the legal action. | CAP-S4-023 | BR-034 | REQ-S4-009 | Must | 3 |
| FR-S4-052 | The service SHALL escalate to the Head of Litigation when 90 days or less remain to prescription (R-LIT-11, R-LIT-20), and SHALL force a litigation review ahead of every other open action on the case (R-UNI-31; VR-S4-013-2). | CAP-S4-023 | BR-034 | REQ-S4-009 | Must | 3 |
| FR-S4-053 | The service SHALL obtain every lawsuit, hearing, balance and batch-status fact it needs through the rwb-source-data contract; a read of a `recovery.v_ace_*` view, a read of an ACE table, and a constraint in schema `rwb_litigation` that references a table outside it, SHALL fail the build and the boundary test (GAP-1736; ASM-2898). | CAP-S4-024 | BR-039 | REQ-S4-005 | Must | 3 |
| FR-S4-054 | The service SHALL hold a step where a data product it needs is stale at the business date, SHALL show the stale product with its date and MSG-P1-001 (VR-S4-001-1 to VR-S4-022-1), and SHALL record the business date and load time it used. | CAP-S4-024 | BR-039 | REQ-S4-005 | Must | 3 |
| FR-S4-055 | The service SHALL read every period, threshold, panel criterion, fee, ladder step and template status from versioned reference data, and a change SHALL take effect from its valid-from date without a code release (BR-S4-001 to BR-S4-022). | CAP-S4-001 | BR-034, BR-037, BR-040 | REQ-S4-001 | Must | 3 |
| FR-S4-056 | The service SHALL hold one litigation decision record per step carrying the rule version, the inputs snapshot, the recommendation, the approval, the level applied and the outcome, and where the record cannot be written SHALL change nothing, show MSG-P7-003 and raise an incident. | CAP-S4-025 | BR-036, BR-041 | REQ-S4-003 | Must | 3 |
| FR-S4-057 | The service SHALL record on each settlement, appeal, fee, deferral and bankruptcy approval the level applied, the approver role and the rule version, read from the delegation table in force at run time through the access contract. | CAP-S4-025 | BR-040, BR-041 | REQ-S4-006 | Must | 3 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-S4-001 | The litigation workspace, the enforcement workspace and the notice approval screen respond inside the user's wait under the busiest-hour load. | Under 2 seconds at the 95th percentile | NFR-008 | Must | Performance test in SIT |
| NFR-S4-002 | The pack view loads for a case with 50 documents and its defect list, with the document contract in the path. | Under 2 seconds | NFR-009 | Must | Performance test with a 50-document case |
| NFR-S4-003 | A rule evaluation at a litigation step completes inside the user's wait. | Under 300 milliseconds at the 95th percentile | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S4-004 | The next-step agent answers inside its target; after that the rule result is used and a step is still presented. | Under 60 seconds, then the rule result | NFR-010, NFR-024 | Must | Agent timeout drill |
| NFR-S4-005 | The service carries the stated partner and staff population and the case load of the recovery inventory. | About 50 partner users online in the busiest hour of about 320 named users across 11 to 12 law firms; about 370 staff online of 914 named users; about 23,600 open cases at go-live and 26,500 at the end of 2027 | NFR-003, NFR-002, NFR-001 | Must | Volume test at the stated population; the litigation share of the case load is open (GAP-1749; ASM-2911) |
| NFR-S4-006 | The decision log holds one record for every step on every legal action for the full retention period without degrading query time. | About 36 GB by the end of 2031; a single case history query under 2 seconds at that size | NFR-007 | Must | Query timing at the 2031 size |
| NFR-S4-007 | Every step states the business date and load time of the data products it read. | Every step | NFR-013 | Must | Decision record inspection |
| NFR-S4-008 | A missing, failed or late ACE batch is visible at the step and alerts the data steward. | Visible at the step; alert to the steward | NFR-014 | Must | Hold an ACE batch in SIT |
| NFR-S4-009 | The service holds no load window, no staging table and no catch-up job: a late ACE batch holds the step and raises an alert. | No load, no staging, no catch-up | NFR-015 | Must | Hold and release the batch |
| NFR-S4-010 | The service is available during business hours and outside them, when the notice, hearing and enforcement timers run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S4-011 | The service inherits the ACE recovery point and recovery time, and a running legal action resumes where it stopped, including across a Continue-As-New of a workflow that runs for years. | The ACE recovery point objective and recovery time objective; workflow history preserved | NFR-022, NFR-023 | Must | Failover, restore and worker-restart test before the first release |
| NFR-S4-012 | Every litigation step is reproducible from the log, including the rule, model and prompt versions and the inputs used. | Every step reproducible | NFR-033 | Must | Re-run a sample of steps from the log |
| NFR-S4-013 | Every action carries the rule version applied and the approver who allowed it. | Every action | NFR-034 | Must | Decision record inspection |
| NFR-S4-014 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-S4-015 | Every legal document this service causes to be filed or produced is held write-once and cannot be altered or deleted inside its retention period. | Write-once for legal types | NFR-029 | Must | Attempt an alteration and a deletion in the test environment |
| NFR-S4-016 | A legal hold stops deletion and expiry for the case or document it covers, for as long as it is in place, overriding the retention class. | Hold overrides retention | NFR-072 | Must | Place a hold across a retention boundary |
| NFR-S4-017 | A document produced from the hub carries its origin, the date it entered the hub, whether it has been altered since, and who has read it. | Every document produced | NFR-076 | Must | Produce a pack and inspect its provenance |
| NFR-S4-018 | Every document type the pack uses carries a retention class that sets how long it is kept. | Retention class per type; periods open (DL26) | NFR-028, NFR-031 | Must | Retention class review |
| NFR-S4-019 | A data subject access, correction or erasure request is worked inside the statutory period. | Statutory period | NFR-043 | Must | Data subject request drill |
| NFR-S4-020 | Party identifiers are masked at rest and on every screen and agent call, by role. | Masked at rest and in use | NFR-039 | Must | Masking matrix test across roles |
| NFR-S4-021 | Each screen, each partner view and each agent receives only the personal data it needs. | Data minimisation per screen and per agent | NFR-040 | Must | Contract review per screen and per agent |
| NFR-S4-022 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S4-023 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-S4-024 | Every data product and record this service holds carries a data classification that sets its handling. | Classification applied per record | NFR-047 | Must | Classification review |
| NFR-S4-025 | Recovery data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | NFR-046 | Must | Tenancy review |
| NFR-S4-026 | Staff authenticate with single sign-on and multi-factor authentication; a partner account uses multi-factor and is scoped to its own cases; agents run under service identities subject to the same role checks. | Entra ID single sign-on with multi-factor; partner accounts multi-factor and scoped; service identities | NFR-049, NFR-050, NFR-051 | Must | Sign-in, partner scope and identity test |
| NFR-S4-027 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-S4-028 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency, and every agent output is schema checked with the rule fallback. | Pipeline checks pass; schema check on every agent output | NFR-054, NFR-055 | Must | Pipeline run with a seeded violation; agent output with a bad schema |
| NFR-S4-029 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English, and document text is read and extracted in Thai and in English. | Every label and message in Thai and English; Thai and English extraction | NFR-059, NFR-057 | Must | Label, message and extraction review |
| NFR-S4-030 | Logs, traces and metrics are produced for the notice, the pack, the firm, the court calendar, the judgment and the enforcement; every triggered job has a run book; a failure alerts a named owner. | Every job covered; alert within 15 minutes to the named owner | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-S4-031 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter with replay | NFR-025, NFR-026 | Must | Failure injection |
| NFR-S4-032 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_litigation`. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-S4-033 | The three screens meet the bank's accessibility standard and work on the browsers the bank supports. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome | NFR-060, NFR-061 | Must | Accessibility scan and browser test |
| NFR-S4-034 | A closed case pack is right first time on the QA sample, tested against the rule version that was in force when the pack was taken. | 90 percent | NFR-037 | Must | QA sample of closed packs |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_litigation`. Every table carries the record columns of the platform library. The Ownership Map fixes two table names for this service (`legal_action` and `hearing`) and none for the judgments, the enforcement record, the LED auction rounds, the notice state or the enforcement deferral that Architecture v5 names as the schema's content, so those four are named as entity groups and the physical names are written with the DB story (GAP-1738; ASM-2900). Retention is stated by class; the periods are open (GAP-1749; ASM-2911; DL26).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `legal_action` | Owned table (Ownership Map) | `case_id` (business key, `varchar(255)`; GAP-1739; ASM-2901), `law_firm_id`, `action_type` from LOV-LEGAL-TYPE, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, the state (NOTICE_BLOCKED, NOTICE_DISPATCHED, WITH_CUSTOMER_NOTICE_PERIOD, NOTICE_UNSERVED, PACK_ASSEMBLY, PACK_VERIFIED, FIRM_SELECTION, FIRM_DECLINED, FIRM_INSTRUCTED, FILED_IN_COURT, FILING_REJECTED, SETTLEMENT_OFFERED_AT_COURT, LITIGATION_HELD, IN_HEARING, JUDGMENT_RECORDED, JUDGMENT_DISMISSED, ASSET_TRACE, ENFORCEMENT_DECISION, WRIT_AND_SEIZURE, NO_BID_AT_70, DEFERRAL_RECORDED, BANKRUPTCY_PETITION, PROCEEDS_MATCHED, CASE_CLOSED), the prescription date, the enforcement owner role | [SENSITIVE_FINANCIAL] | Workbench record; the lawsuit and the hearing facts arrive from LIT through the source-data contract | Workbench record class; period open |
| `hearing` | Owned table (Ownership Map) | `legal_action_id`, `case_id`, the hearing date, the hearing type, the court, the source of the entry (LIT read or firm entry), the result, the deadline raised, the fee accrued | [CONFIDENTIAL] | LIT through the source-data contract, and the firm's entry through the partner contract | Workbench record class; period open |
| `judgment` (entity group) | Owned record, one per judgment per legal action | The judgment date, the judgment type (full, partial, default, dismissed), the judgment amount, the red case number, the appeal window, the appeal decision, the grounds and the appeal approval | [SENSITIVE_FINANCIAL] | The firm's entry and the court filing through the partner contract | Workbench record class; period open |
| `enforcement` (entity group) | Owned record, one per enforcement per legal action | The enforcement owner role, the asset-trace result and its sources, the writ and seizure dates, the enforcement decision, the deferral with its coded reason and review date, the bankruptcy test result and the petition approval | [SENSITIVE_FINANCIAL] | Workbench record; the trace sources are external systems through the integration contract | Workbench record class; period open |
| `auction_round` (entity group) | Owned record, one per round per enforcement | The round number, the price basis (100, 90, 80 or 70 percent of official value), the official value, the round date, the result (sold or no bid), the proceeds and the match reference | [SENSITIVE_FINANCIAL] | The LED and the firm through the partner contract | Workbench record class; period open |
| `litigation_pack` (entity group) | Owned record, one per pack per filing attempt | The pack reference, the document versions in it, the case facts used, the defect list version, the defect result, the verifying role and the verification date | [CONFIDENTIAL] | Workbench record; the documents are read through the document contract | Workbench record class; period open |
| `litigation_decision` (entity group) | Owned record, one per step per legal action | The step, the rule version, the inputs snapshot, the recommendation, the approval, the level applied, the approver role, the outcome, the business date and the load time used, the decided at | [SENSITIVE_FINANCIAL] | Workbench decision; the position it rests on is read through contracts | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT; ASM-0074) |

The field lists of the judgment, the enforcement, the auction round, the pack and the decision record are open: the FSD's field catalog for every feature repeats the eight `legal_action` columns and names no other table (GAP-1738; ASM-2900). No copy of an ACE column is held and no foreign key leaves the schema.

## 8.2 Data read but not owned

| Data | Read through | Views behind it | Classification of the data read |
|---|---|---|---|
| Lawsuit, court and hearing data from LIT | rwb-source-data contract (REST and activity) | `v_ace_legal_action` and the LIT views behind it (the exact view names are not in the sources read; GAP-1736; ASM-2898) | [SENSITIVE_FINANCIAL] |
| Balance and payment position for the proceeds match and the close | rwb-source-data contract (REST) | `v_ace_account`, `v_ace_payment` | [SENSITIVE_FINANCIAL] |
| Freshness of each data product | rwb-source-data contract (REST) | `v_ace_batch_status` | [CONFIDENTIAL] |
| Case, party, stage, queue and timers | rwb-case contract (Temporal activity and REST) | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Documents, their versions, custody and the write-once state | rwb-document contract (REST and activity) | none (document schema) | [CONFIDENTIAL], [PII] |
| The firm, its panel position, scorecard and capacity | rwb-partner contract (Temporal activity and event) | none (partner schema) | [CONFIDENTIAL] |
| Notice content, template version and proof of delivery | rwb-comms contract (Temporal child and event EV-15) | none (comms schema) | [CONFIDENTIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| Rule packages and the version in force | rwb-decision contract and events | none (decision schema) | [CONFIDENTIAL] |
| LOV-LEGAL-TYPE and other reference data | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |
| Payment and posting status of a fee or a matched proceed | rwb-payment contract | none (payment schema) | [SENSITIVE_FINANCIAL] |

Counts are not stated: the FSD gives no field count for this module beyond the eight `legal_action` columns, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

The FSD marks all eight `legal_action` catalog fields as not personal data. The fields below reach the screen, the partner view or the agent through the contracts this service calls, and are handled as personal or financial data by this document.

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| Claim amount and judgment amount | What the bank sues for and what the court awarded | [SENSITIVE_FINANCIAL] | Read access by role; no amount in an event, a workflow input or a log; JudgmentRecorded carries the case, the type and the date, not the amount |
| Enforcement proceeds and fee amounts | What was recovered and what the bank paid | [SENSITIVE_FINANCIAL] | Served on the enforcement workspace only; not carried in AuctionResult |
| Court name, black case number, red case number, lawsuit number | The identity of the case in the court | [CONFIDENTIAL] | Shown by role; the black and red case numbers are the court's own public identifiers and are not masked |
| Law firm identifier and firm user | The firm instructed and the person acting for it | [CONFIDENTIAL] | Read by role; the firm user is an external role reached through the partner gateway, scoped to its own cases (NFR-050) |
| Customer identification number and name, where the workspace shows the case party | The party the claim is against | [PII] | Masked by role; the identification number never leaves in clear; every read logged |
| Customer address and contact value, where a notice is dispatched | Where the notice went | [PII] | Masked by default, full only where a masking row for the role allows it; the notice body and its merge fields belong to rwb-comms |
| Document content of the pack | The evidence filed | [CONFIDENTIAL], [PII] | Read through the document contract only; write-once inside retention; no document content in a log or an event |
| Asset-trace result naming a third party | What the bureau, a registry or an insurer returned | [PII], [CONFIDENTIAL] | Held on the enforcement record; masked by role; never in an event |
| Next-step agent output and its prompt | The recommended step and the material it was given | [CONFIDENTIAL] | No personal data in the prompt, the output or the log (NFR-040) |

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the statutory notice periods, the proof window, the prescription warning point and the 90-day escalation, the defect list, the panel criteria and scorecard weights, the fee schedule, the auction ladder, the enforcement-economics test, the approval levels and the deferral reasons (BR-S4-001 to BR-S4-022; RULE-001).
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through the source-data contract only (GAP-1736; ASM-2898).
3. A link to an ACE record is a business-key column of type `varchar(255)` with no foreign key; this applies to `legal_action.case_id`, which the FSD types as `uuid` (GAP-1739; ASM-2901).
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; LawsuitFiled, JudgmentRecorded and AuctionResult carry the case, the step, the outcome and the versions, not the amounts, the parties or the documents.
6. A legal document is write-once inside its retention period, and a legal hold overrides the retention class (NFR-029, NFR-072).
7. ACE data is retained by ACE, and the archive of a Workbench record belongs to rwb-document.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | Out and in | REST, one hop, 2 s timeout, GET retried once with jitter; activity inside a workflow | P1 | The only path to lawsuit, hearing, balance and freshness facts; this service reads no view and no ACE table. The slide 13 matrix gives the S4 row no cell to P1, so the path is carried as open (GAP-1736; ASM-2898) |
| ACE database, tables behind the 30 views, LIT | Not read | None | ACE team | Read only through the P1 contract. No direct `public` read and no DML from this service |
| rwb-case (P3) | In and out | Temporal child workflow (LitigationWorkflow, parent close policy ABANDON) and REST; events listened to | P3 | The case starts the legal action and owns the parent workflow, the queues, the tasks and the case timers; this service publishes LawsuitFiled, JudgmentRecorded and AuctionResult for it |
| rwb-decision (P7) | Out and in | Temporal activity and child workflow (ApprovalWorkflow); events listened to (RulePackageInForce) | P7 | Approval routing on the delegation for the settlement, the appeal, the fee, the deferral, the bankruptcy petition and the delay of action; rule package governance; the decision record and the hash chain. Slide 13 S4 row: T to P7 |
| rwb-comms (P6) | Out and in | Temporal child workflow (demand notice) and events listened to (EV-15 NoticeDelivered) | P6 | Notice content, templates, merge fields and proof of delivery; this service decides that a notice is due and approves it. Slide 13 S4 row: T and E to P6 |
| rwb-partner (S9) | Out and in | Temporal activity (issueInstruction) and events listened to (EV-21 PartnerResultSubmitted) | S9 | The law firm master data, the panel, the portal account, the instruction, the receipt, the court number and the round result. Slide 13 S4 row: T and E to S9 |
| rwb-document (P5) | Out | REST and activity per the document contract | P5 | The document index, the pack documents and their versions, custody, the write-once container and retention. The slide 13 matrix gives the S4 row no cell to P5 (GAP-1737; ASM-2899) |
| rwb-payment (P8) | Out | REST or an activity per the payment contract | P8 | Court fees and legal expenses, and the posting of matched enforcement proceeds to ALS and the general ledger. The slide 13 matrix gives the S4 row no cell to P8 (GAP-1737; ASM-2899) |
| rwb-agent (P10) | Out | Temporal, child workflow and activity | P10 | The next-step agent under its contract, 60 s then the rule result (DP-20). The slide 13 matrix gives the S4 row no cell to P10 (GAP-1737; ASM-2899) |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, capability areas, masking policy and the delegation table |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | SCR-18 notice approval, SCR-19 litigation workspace and SCR-20 enforcement workspace; the composite route joins this service's answer with rwb-case and rwb-document (GAP-1747; ASM-2909) |
| Kafka topic `rwb.litigation.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | LawsuitFiled, JudgmentRecorded and AuctionResult; consumers rwb-asset and rwb-case. The three events have no EV number in the catalogue (GAP-1744; ASM-2906) |
| Kafka topic EV-15 (rwb.comms.events.v1) | In | CloudEvents 1.0, inbox | P6 | NoticeDelivered |
| Kafka topic EV-21 (rwb.partner.events.v1) | In | CloudEvents 1.0, inbox | S9 | PartnerResultSubmitted |
| Shared topic `rwb.decision-record.v1` | Out | CloudEvents 1.0 | P7 | Each local decision record, collected into the central ledger |
| rwb-reporting (P9) | Out | Events and the decision record | P9 | The litigation turnaround measure (KPI-002) and the pack first-time-right measure (KPI-009), produced from the decision log and not from a separate count |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| NCB, the registries, the insurers, CCMS and the LED portal | Out and in | Through rwb-integration and the partner gateway, not by direct call | P2 with the external system | The asset trace, the enforcement notice and the round result (GAP-1737; ASM-2899) |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which path carries the LIT lawsuit and hearing data into this service, given that the slide 13 matrix gives the S4 row no cell to rwb-source-data and the FSD reads the ACE views directly? | Solution architect with P1 | The read path of every step depends on it, and the boundary test cannot be written until it is fixed (GAP-1736; ASM-2898) |
| Who carries the pack, the fee and the agent call, given that the matrix gives this service no cell to rwb-document, rwb-payment or rwb-agent while the FSD names the document hub, ALS and GL and the model gateway? | Solution architect with P5, P8 and P10 | Three edges of the product are undefined, and each one is a contract dependency on another service's CON story (GAP-1737; ASM-2899) |
| Does this service generate the notice and prove its delivery, or does rwb-comms, and which service holds the notice state and the served result? | Solution architect with P6 | The notice capability is split across two services and the Ownership Map gives one of its three paths to each (GAP-1740; ASM-2902) |
| Which applies to the notice slice: the E2 release (31 December 2026 (tentative)) it is first needed in, or the S4 wave-3 release? | Solution architect with the programme manager | The wave map keeps EP02 at wave 2, which puts notice stories before the service exists (GAP-1741; ASM-2903) |
| Does the notice approval route stay `POST /notices/{noticeId}/approve` on this service while `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` sit on rwb-comms? | Solution architect | Two owners of one notice resource fix the gateway route and the screen client before SCR-18 is built (GAP-1740; ASM-2902) |
| Which service owns the three screens SCR-18, SCR-19 and SCR-20, and where does each cell in the screen matrix route from? | Solution architect | The composite route and the screen's client depend on it (GAP-1747; ASM-2909) |

# 10. Release slicing proposal

The service is wave 3: it is created with Epic 5 (release 31 March 2027 (tentative); ASM-2915). The notice capability is first needed one release earlier, in Epic 2, so one contract slice sits before wave 3. Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit with the approval and partner children and the durable timer, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Before wave 3 — the notice slice Epic 2 needs (release 31 December 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Published notice contract and fake | CAP-S4-001, CAP-S4-002, CAP-S4-003 | Epic 2 releases the notice approval screen and the notice period, and the FSD gives module S4 "E2 notices; E5" while the service is created in wave 3. The contract, its fake and its schema are published first, and the notice stories keep the wave 2 that the wave map gives EP02 (GAP-1741; ASM-2903) |
| 2.2 Notice generation, approval and the period | CAP-S4-001, CAP-S4-002, CAP-S4-003 | The notice is the legal step that starts everything after it, and a notice period counted from posting instead of delivery is a period the bank cannot prove |

Rationale: contract-first is the only way to keep the E2 release date while the service that owns the capability is created in wave 3; the fake is what rwb-comms, rwb-case and the screen test against until wave 3 lands. The rule in R5.6 applies: a story whose wave map wave is earlier than its service's Arch v5 wave keeps the wave map wave.

## 10.3 Wave 3 — Epic 5 (release 31 March 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Contract baseline and the record | CAP-S4-025 | Every later slice writes a decision record, and the boundary test must fail the build on a direct ACE read from the first story |
| 3.2 Read path and freshness | CAP-S4-024, CAP-S4-023 | A step decided on stale data or on an expired claim is a step that cannot be defended, and the prescription clock must exist before any filing is approved |
| 3.3 Pack assembly and the defect check | CAP-S4-004, CAP-S4-005, CAP-S4-006 | A pack filed with a known defect is the defect rate the programme exists to remove |
| 3.4 Verification and filing approval | CAP-S4-007 | The officer's signature is the control, and it must be given against a checked pack |
| 3.5 Firm selection and instruction | CAP-S4-008, CAP-S4-009 | Firm selection by habit is the largest uncontrolled legal cost, and the partner clock is what makes a late firm visible |
| 3.6 Filing, court calendar and the next step | CAP-S4-010, CAP-S4-011, CAP-S4-012 | A court number held only by the firm is a case the bank cannot trace, and a deadline read from an email is the turnaround |
| 3.7 Settlement, appeal and fees | CAP-S4-013, CAP-S4-014, CAP-S4-015 | Money leaving the bank in a legal case leaves on an approval, not on a request |
| 3.8 Judgment and the enforcement owner | CAP-S4-016 | Enforcement after judgment has no owner today, which is where recovery stops |
| 3.9 Asset trace, writ and the ladder | CAP-S4-017, CAP-S4-018, CAP-S4-019 | Enforcement only pays if there is an asset, and the ladder is the statutory price path |
| 3.10 Deferral, bankruptcy and proceeds | CAP-S4-020, CAP-S4-021, CAP-S4-022 | A step that cannot proceed needs a home, and enforcement money that is not matched is money in suspense |

Rationale: the wave-3 slice is the smallest set that delivers the Epic 5 outcome, and each slice is independently demonstrable. Every capability of this module is Must, so no slice may slip without holding the release. The service wave (3) and the business epic wave of E5 (3) are the same, so no wave conflict is raised for E5 (ASM-2914).

## 10.4 Later increments

| Increment | What unlocks it |
|---|---|
| The litigation rule set as a governed package | Phase 2 of the Drools design, with the 79-rule set, its version label and its owner in rwb-decision. The FSD names 32 of the 79 rules, so the package is authored from the routing logic, not from this PRD (GAP-1742; ASM-2904) |
| Substituted service and filing where the law allows, at full width | The Head of Litigation approval route at D7.4 to D7.5 and the limits in force (GAP-1746 and BRD Q-001) |
| Collection agencies, auction vendors and valuers through the same partner instruction | The partner portal live at the edge, first needed for law firms at Epic 5 (Non-functional specification v3 section 4) |
| Litigation measures and the pack first-time-right measure at full width | The rwb-reporting read model, fed by the decision record and the events (ADR-018) |
| The debt sale lot building that shares the E5 release | S6 rwb-debtsale, which owns it; nothing in this service builds a lot or a data room |
| The S4 table set in the Ownership Map and the physical schema | The data architect's table list, added with the DB story (GAP-1738; ASM-2900) |
| The three events with their EV numbers | The event catalogue row that slide 43 leaves as a "+" row (GAP-1744; ASM-2906) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used. The FSD's own acceptance criteria are one generic statement per feature (GAP-1743; ASM-2905), so each criterion below is a product-level statement of the rule that feature names.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S4-001 | FR-S4-001, FR-S4-003, FR-S4-004, FR-S4-005 | a current Legal-approved template for the product and the notice type, and a case at the litigation route | the notice is generated, approved and dispatched, and the proof arrives as delivered | the case is at NOTICE_DISPATCHED with the template version and the approver recorded, then at WITH_CUSTOMER_NOTICE_PERIOD with the period started from the delivery date | AC-S4-001-01; R-LIT-03, R-LIT-07 |
| AC-S4-002 | FR-S4-002, FR-S4-004 | a template withdrawn for the product and the notice type | generation is attempted | the case is at NOTICE_BLOCKED with a task to the litigation officer and no notice leaves the bank; no dispatch is possible without an approval | AC-S4-002-01; AC-EXC-S4-001-01; R-LIT-04 |
| AC-S4-003 | FR-S4-006 | a notice dispatched and no proof returned inside the proof window | the window passes | the notice is unserved, the case is at NOTICE_UNSERVED, no period has started, and the window that was applied is shown | AC-S4-002-01; R-LIT-08 |
| AC-S4-004 | FR-S4-007 | a served result of refused, then returned, then undeliverable | each result is recorded | the result is recorded and an alternate service method is queued for each; the case stays at NOTICE_UNSERVED | AC-S4-002-01; R-LIT-09 |
| AC-S4-005 | FR-S4-008, FR-S4-009, NFR-S4-011 | a notice period running and a worker stopped across the period | the worker restarts and the period expires with no cure and no dispute | the timer resumes where it stopped, the case is at PACK_ASSEMBLY, and no Quartz table, connection or job exists | AC-S4-003-01; Arch v5 slide 19; DP-10 |
| AC-S4-006 | FR-S4-010, FR-S4-011 | a document index of a case and a set of case facts | the pack is assembled and a document is then re-created | the pack records the document versions and the case facts it was built from, and the defect check re-runs on the re-created document | AC-S4-004-01; R-LIT-18 |
| AC-S4-007 | FR-S4-012, FR-S4-013 | a pack missing three items on the defect list in force | filing approval is attempted, and the three items are then supplied | every missing item is named with MSG-S4-001 and the pack cannot go to filing approval; after the supply the check re-runs and the pack moves forward | AC-S4-005-01; VR-S4-005-1; R-LIT-32 |
| AC-S4-008 | FR-S4-014, FR-S4-015 | a document the pack needs that the bank cannot find, and a user whose role lacks the capability area | the recovery path is opened, then the same action is attempted by the user without the right | the request, its owner role and its result are on the case; the second attempt is refused with MSG-P4-002 and nothing changes | AC-S4-006-01; AC-EXC-S4-006-01; VR-S4-006-2 |
| AC-S4-009 | FR-S4-016, FR-S4-017 | a pack with every defect list item present | the officer verifies it, then a second pack is rejected at verification | the first moves the case to PACK_VERIFIED with the verifying role and date; the second returns to PACK_ASSEMBLY with the defects named | AC-S4-007-01; R-LIT-16, R-LIT-21 |
| AC-S4-010 | FR-S4-018, FR-S4-051, FR-S4-052 | 90 days or less remaining to prescription, and a warning point reached earlier | substituted service is attempted, then the clock is read at the warning point | the substitution waits for the Head of Litigation and records the approval with its reason; the warning raises MSG-S4-002 with the expiry date and forces a litigation review ahead of the other open actions | AC-S4-007-01; AC-S4-003-01; VR-S4-003-1; R-LIT-11, R-LIT-20, R-UNI-31 |
| AC-S4-011 | FR-S4-019, FR-S4-020 | a verified pack and a panel of firms with a scorecard, a capacity and a court coverage per firm | the firm is selected, and the first firm then declines | the selection follows the panel rule and records the score, the capacity, the court and the conflict result; the decline records its reason and re-selects the next firm, moving to FIRM_DECLINED | AC-S4-008-01; R-LIT-23, R-LIT-27 |
| AC-S4-012 | FR-S4-021 | a Head of Litigation who nominates a firm outside the panel result | the instruction is issued | the nomination is recorded with the role, the reason and the date, and the instruction uses that firm | AC-S4-008-01; R-LIT-26 |
| AC-S4-013 | FR-S4-022 | a selected firm that covers the court region and the case type and passes the conflict check | the instruction is issued | the instruction and the pack reach the firm through the partner portal, the case is at FIRM_INSTRUCTED, and the partner clock has started | AC-S4-009-01; R-LIT-24 |
| AC-S4-014 | FR-S4-023 | an instructed firm past the partner clock with no filing | the clock is read | the instruction is at breach, the partner manager is notified, and the next firm is selected with the case at FIRM_DECLINED | AC-S4-009-01; R-LIT-28 |
| AC-S4-015 | FR-S4-024 | a firm that submits the filing receipt and the court case number | the submission arrives as PartnerResultSubmitted | the court case number and the receipt are on the legal action, the hearing timers are set, and the case is at FILED_IN_COURT | AC-S4-010-01; R-LIT-30; EV-21 |
| AC-S4-016 | FR-S4-025 | a court that returns the filing for a defect | the return is recorded | the defect is recorded, the pack returns for rework, and the case is at FILING_REJECTED | AC-S4-010-01; R-LIT-31 |
| AC-S4-017 | FR-S4-026 | a court case number the firm submits that differs from the lawsuit ACE ingests from LIT | the match runs | the difference is raised for a person and neither record is overwritten | AC-S4-010-01; BR-038 |
| AC-S4-018 | FR-S4-027, NFR-S4-002 | a legal action with hearings, deadlines and fees and a case with 50 documents | the workspace is opened ahead of a deadline | each deadline raises its task before it falls due, each fee is accrued to the case, and the view loads under 2 seconds | AC-S4-011-01; NFR-009 |
| AC-S4-019 | FR-S4-028 | one hearing held in LIT and entered by the firm with a different date | the legal action is read | both records are shown with their source, and the difference is visible rather than merged | AC-S4-011-01; BR-039 |
| AC-S4-020 | FR-S4-029, NFR-S4-004 | the next-step agent answering inside 60 seconds, then a run that does not answer at all | the step is recommended in both cases | the recommendation carries its reasons, its cost and its effect with the agent, model and prompt versions; the second presents the rule result and still offers a step | AC-S4-012-01; NFR-010, NFR-024, NFR-055 |
| AC-S4-021 | FR-S4-030, FR-S4-031 | a settlement proposed before judgment, first inside the D7.4 limit and then above it | each is approved | the first books the treatment and holds the litigation at LITIGATION_HELD; the second records the committee approval with its level, and neither withdraws the litigation | AC-S4-013-01; R-LIT-36, R-LIT-37 |
| AC-S4-022 | FR-S4-032, FR-S4-033 | a settlement rejected with a reason, and a settlement reached at court that later breaks | each is recorded | the first records the reason and returns the case to IN_HEARING; the second resumes the litigation, keeps the judgment path open and records the rule that resumed it | AC-S4-013-01; R-LIT-38, R-LIT-40 |
| AC-S4-023 | FR-S4-034, FR-S4-035 | a judgment and an appeal decision with its grounds | the appeal is recorded and then decided | the decision, the grounds and the approval with its level are recorded, the appeal is tracked to its end with its own timers, and the earlier judgment stays readable | AC-S4-014-01; VR-S4-014-1 |
| AC-S4-024 | FR-S4-036 | a fee inside the fee schedule and a fee outside it | each is submitted for payment | the first is paid on approval with the amount and the schedule version recorded; the second is held rather than paid | AC-S4-015-01; BR-040 |
| AC-S4-025 | FR-S4-037, FR-S4-039, FR-S4-040, NFR-S4-012 | a judgment of type full | the judgment is recorded | the judgment date and amount are on the legal action, the enforcement owner role is named from judgment to the end, and JudgmentRecorded is in the outbox keyed by the case in the same transaction | AC-S4-016-01; R-LIT-44; Arch v5 slide 19 |
| AC-S4-026 | FR-S4-038 | a judgment of type dismissed | the judgment is recorded | the dismissal is recorded, the appeal window opens, and the case is at JUDGMENT_DISMISSED | AC-S4-016-01; R-LIT-45 |
| AC-S4-027 | FR-S4-041, FR-S4-042, FR-S4-044, FR-S4-045 | a judgment recorded and an asset traced at each of the four ladder steps, then a round with no bid at 70 percent | the enforcement runs | each source searched and its date is recorded, the enforcement decision is presented with the traced assets, each round records its price basis and result, and the no-bid round is referred to the enforcement owner at NO_BID_AT_70 | AC-S4-017-01, AC-S4-019-01; R-LIT-50, R-LIT-52, R-LIT-67 |
| AC-S4-028 | FR-S4-043 | an asset traced and enforcement economic | the writ and the seizure are instructed | the firm is instructed, the case is at WRIT_AND_SEIZURE, and the instruction is tracked to execution | AC-S4-018-01; R-LIT-54 |
| AC-S4-029 | FR-S4-046 | an enforcement step that cannot proceed | the deferral is submitted first with no coded reason, then with a reason and no review date, then with both | the first two are refused with MSG-GEN-001 and nothing changes; the third is recorded at DEFERRAL_RECORDED and the case returns on the review date | AC-S4-020-01; VR-S4-020-1; R-LIT-55 |
| AC-S4-030 | FR-S4-047 | enforcement exhausted and the bankruptcy test met | the petition is routed | the approver at D7.5 records the decision with its level, the case is at BANKRUPTCY_PETITION, and the petition is filed through the firm | AC-S4-021-01; R-LIT-58 |
| AC-S4-031 | FR-S4-048, FR-S4-049, FR-S4-050 | a round sold at 80 percent of official value, the proceeds matching the judgment total and the costs | the round is settled | the proceeds are matched, posted through the payment contract, the enforcement and the case close with the record retained, and AuctionResult is in the outbox keyed by the case | AC-S4-022-01; R-LIT-65, R-LIT-70; Arch v5 slide 19 |
| AC-S4-032 | FR-S4-044 | a round proposed at 85 percent of official value | the round is recorded | the step is refused as outside the ladder and no round is written | AC-S4-019-01; R-LIT-63 to R-LIT-67 |
| AC-S4-033 | FR-S4-053, FR-S4-054, NFR-S4-007, NFR-S4-008 | a branch that reads `recovery.v_ace_legal_action` directly, a schema constraint that references an ACE table, and a data product that is stale at the business date | the pipeline and the boundary test run, then a step is attempted | the build fails naming the view read and the cross-schema constraint; the step is held, the stale product is shown with its date and MSG-P1-001, and the business date and load time used are recorded | AC-S4-001-01; VR-S4-001-1; Arch v5 slides 37 and 45; GAP-1736; ASM-2898 |
| AC-S4-034 | FR-S4-055 | the statutory notice period, the proof window, the defect list, the fee schedule and the ladder in force | each is changed in reference data with a valid-from date | the next step uses the new value from its valid-from date with no code release, and the version applied is on the record | AC-S4-001-01; BR-S4-001 to BR-S4-022; RULE-001 |
| AC-S4-035 | FR-S4-056, FR-S4-057, NFR-S4-013, NFR-S4-014 | a settlement approval and a judgment recorded, and then a decision log store that rejects every write | each step is taken | the record carries the rule version, the inputs snapshot, the recommendation, the approval, the level applied and the approver; with the store rejecting, nothing changes, MSG-P7-003 is shown, an incident is raised, and the daily hash-chain check reports the gap the same day | AC-EXC-S4-013-02, AC-EXC-S4-016-02; NFR-035; RULE-002 |
| AC-S4-036 | FR-S4-015 | a user without the capability area, signed in with single sign-on | they try the notice approval, the pack verification and the deferral | each is refused with MSG-P4-002 and nothing changes on the case, the pack or the legal action | AC-EXC-S4-001-01, AC-EXC-S4-007-01, AC-EXC-S4-020-01; VR-S4-006-2 |
| AC-S4-037 | NFR-S4-015, NFR-S4-016, NFR-S4-017, NFR-S4-018, NFR-S4-019 | a filed pack inside its retention period | an alteration and a deletion are attempted, a legal hold is placed and a data subject request is raised | the alteration and the deletion are refused, the hold overrides the retention class, the produced pack carries its origin, entry date, alteration state and readers, and the request is answered inside the statutory period | NFR-029, NFR-072, NFR-076, NFR-028, NFR-043 |
| AC-S4-038 | NFR-S4-020, NFR-S4-021, NFR-S4-022 | the same legal action read by each role in the masking matrix | each screen, partner view and agent call is made | party identifiers are masked as the matrix says, each view receives only the fields it needs, and every read of a personal field is logged; with the log unwritable the field is refused rather than returned | NFR-039, NFR-040, NFR-042 |
| AC-S4-039 | NFR-S4-005, NFR-S4-006, NFR-S4-010 | the stated partner and staff population and the case load, and a decision log at its 2031 size | the service runs at the busiest hour and a case history is read | the service holds the population without breaching the response targets, a case history reads under 2 seconds, and availability reads 99.9 percent in business hours and 99.5 percent outside them | NFR-001, NFR-002, NFR-003, NFR-007, NFR-020, NFR-021; GAP-1749; ASM-2911 |
| AC-S4-040 | NFR-S4-034 | a QA sample of closed case packs | each is tested against the rule version in force when it was taken | 90 percent of the sample is right first time, and every failure names the defect and the rule that missed it | NFR-037; KPI-009 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| BR-034 (REQ-S4-001) | CAP-S4-001, CAP-S4-002, CAP-S4-003 | FR-S4-001, FR-S4-002, FR-S4-003, FR-S4-004, FR-S4-005, FR-S4-006, FR-S4-007, FR-S4-008, FR-S4-009, FR-S4-055 | NFR-S4-008, NFR-S4-009, NFR-S4-025, NFR-S4-029, NFR-S4-031 | AC-S4-001, AC-S4-002, AC-S4-003, AC-S4-004, AC-S4-005, AC-S4-033, AC-S4-034 |
| BR-035 (REQ-S4-002) | CAP-S4-004, CAP-S4-005, CAP-S4-006 | FR-S4-010, FR-S4-011, FR-S4-012, FR-S4-013, FR-S4-014, FR-S4-015 | NFR-S4-002, NFR-S4-005, NFR-S4-017, NFR-S4-018, NFR-S4-020, NFR-S4-021 | AC-S4-006, AC-S4-007, AC-S4-008, AC-S4-018, AC-S4-036, AC-S4-037 |
| BR-036 (REQ-S4-003) | CAP-S4-007, CAP-S4-025 | FR-S4-016, FR-S4-017, FR-S4-018, FR-S4-056 | NFR-S4-012, NFR-S4-013, NFR-S4-014, NFR-S4-022, NFR-S4-034 | AC-S4-009, AC-S4-010, AC-S4-035, AC-S4-038, AC-S4-040 |
| BR-037 (REQ-S4-004) | CAP-S4-008, CAP-S4-009 | FR-S4-019, FR-S4-020, FR-S4-021, FR-S4-022, FR-S4-023 | NFR-S4-005, NFR-S4-026, NFR-S4-031 | AC-S4-011, AC-S4-012, AC-S4-013, AC-S4-014, AC-S4-039 |
| BR-038 (no program REQ) | CAP-S4-010 | FR-S4-024, FR-S4-025, FR-S4-026 | NFR-S4-011, NFR-S4-030 | AC-S4-015, AC-S4-016, AC-S4-017 |
| BR-039 (REQ-S4-005) | CAP-S4-011, CAP-S4-012, CAP-S4-024 | FR-S4-027, FR-S4-028, FR-S4-029, FR-S4-053, FR-S4-054 | NFR-S4-001, NFR-S4-002, NFR-S4-003, NFR-S4-004, NFR-S4-007, NFR-S4-008 | AC-S4-018, AC-S4-019, AC-S4-020, AC-S4-033 |
| BR-040 (REQ-S4-006) | CAP-S4-013, CAP-S4-014, CAP-S4-015 | FR-S4-030, FR-S4-031, FR-S4-032, FR-S4-033, FR-S4-034, FR-S4-035, FR-S4-036, FR-S4-055, FR-S4-057 | NFR-S4-013, NFR-S4-026, NFR-S4-030, NFR-S4-031 | AC-S4-021, AC-S4-022, AC-S4-023, AC-S4-024, AC-S4-034, AC-S4-035 |
| BR-041 (REQ-S4-007, REQ-S4-008) | CAP-S4-016, CAP-S4-020, CAP-S4-025 | FR-S4-037, FR-S4-038, FR-S4-039, FR-S4-040, FR-S4-046, FR-S4-056, FR-S4-057 | NFR-S4-011, NFR-S4-012, NFR-S4-024, NFR-S4-030 | AC-S4-025, AC-S4-026, AC-S4-029, AC-S4-035 |
| BR-042 (no program REQ) | CAP-S4-017, CAP-S4-018, CAP-S4-019, CAP-S4-021 | FR-S4-041, FR-S4-042, FR-S4-043, FR-S4-044, FR-S4-045, FR-S4-047 | NFR-S4-003, NFR-S4-012, NFR-S4-023, NFR-S4-027 | AC-S4-027, AC-S4-028, AC-S4-030, AC-S4-032 |
| BR-043 (REQ-S4-010) | CAP-S4-022 | FR-S4-048, FR-S4-049, FR-S4-050 | NFR-S4-006, NFR-S4-024, NFR-S4-031, NFR-S4-032 | AC-S4-031, AC-S4-039 |
| REQ-S4-009 (no BR row; GAP-1746) | CAP-S4-023 | FR-S4-051, FR-S4-052 | NFR-S4-011, NFR-S4-030 | AC-S4-010 |

BR coverage: 10 of the 10 BRD requirements of E5 that name this service (BR-034 to BR-043) are covered by at least one functional requirement, and every functional requirement traces to one of them. Two programs requirements have no BRD requirement row of their own: REQ-S4-009 is carried by FR-S4-051 and FR-S4-052 under BR-034 and is recorded as a coverage gap (GAP-1746), and BR-038 and BR-042 carry no program requirement ID in the BRD and are traced here from the FSD features and the RWB-E5 story keys (ASM-2908). No BRD requirement of this module is left without a functional requirement.

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S4-053, NFR-S4-028 | Developer with the security administrator |
| Contract test against the source-data, document, partner, comms and payment contracts and their fakes | FR-S4-003, FR-S4-010, FR-S4-022, FR-S4-027, FR-S4-036, FR-S4-048, FR-S4-053 | Developer with P1, P5, P6, P8 and S9 |
| Notice drill: a current template, a withdrawn template, no proof, and each served result | FR-S4-001 to FR-S4-008, NFR-S4-031 | Litigation officer with the QA team |
| Notice period and prescription drill, including a worker restart across the period and the 90-day escalation | FR-S4-008, FR-S4-009, FR-S4-051, FR-S4-052, NFR-S4-011 | QA team with the Head of Litigation |
| Pack assembly, defect list and missing document drill | FR-S4-010 to FR-S4-015, NFR-S4-002, NFR-S4-017 | Litigation officer with the QA team |
| Verification, filing approval and the substituted-service path | FR-S4-016, FR-S4-017, FR-S4-018 | Head of Litigation with the QA team |
| Firm selection, decline, nomination, instruction and partner-clock breach | FR-S4-019 to FR-S4-023, NFR-S4-026 | Partner and agency manager with the QA team |
| Filing, court number match and returned filing | FR-S4-024, FR-S4-025, FR-S4-026 | Litigation officer with the QA team |
| Court calendar, deadline task and fee accrual | FR-S4-027, FR-S4-028, FR-S4-036 | Litigation officer with the QA team |
| Next-step recommendation with an agent timeout and a failed schema check | FR-S4-029, NFR-S4-004, NFR-S4-028 | QA team with the model risk officer |
| Settlement, appeal and fee approval matrix across the delegation levels and the committee path | FR-S4-030 to FR-S4-036, FR-S4-057 | Product head with the QA team |
| Judgment, dismissal, enforcement owner and JudgmentRecorded | FR-S4-037 to FR-S4-040, NFR-S4-012 | Enforcement owner with the QA team |
| Asset trace, writ, the four ladder steps, the no-bid round and the deferral | FR-S4-041 to FR-S4-046 | Enforcement owner with the Legal Execution Department liaison role |
| Bankruptcy petition and the proceeds match, post and close | FR-S4-047, FR-S4-048, FR-S4-049, FR-S4-050 | Credit administration with the QA team |
| Write-once, legal hold, document provenance and the data subject request | NFR-S4-015 to NFR-S4-019 | Compliance and PDPA officer |
| Masking matrix, access log reconciliation and classification review | NFR-S4-020 to NFR-S4-025 | Compliance and PDPA officer |
| Performance and volume test at the stated population and case load | NFR-S4-001, NFR-S4-002, NFR-S4-003, NFR-S4-005 | QA team |
| Decision reproducibility and QA sample of closed packs | FR-S4-056, NFR-S4-012, NFR-S4-034 | Internal audit with the conduct and QA officer |

# 12. Open questions

The BRD's open questions are carried forward with their IDs where they name this module. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S4-01 | Does this service read lawsuit, hearing and balance facts through the source-data contract, and who confirms the contract fields and the freshness response, given that the slide 13 matrix gives the S4 row no cell to P1? | Solution architect with P1 | Before wave 3 system test | CAP-S4-011, CAP-S4-024 | GAP-1736; ASM-2898; Arch v5 slides 37 and 45 |
| OQ-S4-02 | Which carrier is used for the pack document, the court fee and the next-step agent, given that the matrix gives this service no cell to rwb-document, rwb-payment or rwb-agent? | Solution architect with P5, P8 and P10 | Before the S4 contract story closes | CAP-S4-004, CAP-S4-012, CAP-S4-015 | GAP-1737; ASM-2899 |
| OQ-S4-03 | Which tables hold the judgment, the enforcement record, the auction rounds, the pack, the notice state, the deferral and the decision record in schema `rwb_litigation`, given that the Ownership Map lists two tables? | Data architect | Before the S4 DB story | CAP-S4-001, CAP-S4-016 to CAP-S4-025 | GAP-1738; ASM-2900 |
| OQ-S4-04 | Is `legal_action.case_id` a `uuid` as the FSD types it, or a `varchar(255)` business key with no foreign key as ADR-014 requires? | Data architect | Before the S4 DB story | CAP-S4-001, CAP-S4-025 | GAP-1739; ASM-2901 |
| OQ-S4-05 | Does this service own the notice and its served result, or does rwb-comms, and which of the three notice paths moves? | Solution architect with P6 | Before the notice contract story closes | CAP-S4-001, CAP-S4-002, CAP-S4-003 | GAP-1740; ASM-2902 |
| OQ-S4-06 | Does the notice slice release with E2 (31 December 2026 (tentative)) or with S4 in wave 3, and who owns the published contract and its fake until then? | Solution architect with the programme manager | Before E2 system test | CAP-S4-001, CAP-S4-002, CAP-S4-003 | GAP-1741; ASM-2903 |
| OQ-S4-07 | Which 47 of the 79 litigation rules have no row in the FSD, who authors them, and when does the package reach Phase 2? | Center of excellence analyst with P7 | Before wave 3 release | CAP-S4-004 to CAP-S4-023 | GAP-1742; ASM-2904 |
| OQ-S4-08 | Why is every FSD acceptance criterion the same generic statement, and who writes the step-specific criteria before the stories are cut? | Business analyst, S4 | Before wave 3 story writing | All capabilities | GAP-1743; ASM-2905 |
| OQ-S4-09 | Do LawsuitFiled, JudgmentRecorded and AuctionResult get EV numbers and catalogue rows, and which service consumes each besides rwb-asset and rwb-case? | Solution architect | Before wave 3 system test | CAP-S4-016, CAP-S4-022 | GAP-1744; ASM-2906 |
| OQ-S4-10 | What is the route numbering? R-LIT-01 starts litigation on route R4, while the case journeys call R4 the guarantee claim and R5 litigation | Business analyst, S4 with P7 | Before wave 3 system test | CAP-S4-001, CAP-S4-025 | GAP-1745; ASM-2907 |
| OQ-S4-11 | Which BRD requirement carries REQ-S4-009 (prescription warnings), which has no BR row in the E5 requirement set? | Product Owner with the business analyst | Before wave 3 release | CAP-S4-023 | GAP-1746; ASM-2908 |
| OQ-S4-12 | Which service owns SCR-18, SCR-19 and SCR-20, and where does each cell in the screen matrix route from? | Solution architect | Before wave 3 release | CAP-S4-001, CAP-S4-004, CAP-S4-016, CAP-S4-019 | GAP-1747; ASM-2909; Arch v5 slide 41; DP-19 |
| OQ-S4-13 | Which role owns enforcement after judgment, and which role owns the eviction of a held property (BRD Q-008, DL18, DL22)? | Head of Litigation | Before wave 3 release | CAP-S4-016, CAP-S4-020 | BRD Q-008; ASM-2576 |
| OQ-S4-14 | What is each approval limit, by decision, product and amount, and who is the substitute for each, for the settlement, the appeal, the fee, the deferral, the bankruptcy petition and the delay of action (DL18)? | Risk with the product heads | Before wave 3 release | CAP-S4-013 to CAP-S4-015, CAP-S4-020, CAP-S4-021 | BRD Q-001; GAP-1464; ASM-2569 |
| OQ-S4-15 | What are the statutory notice periods, the proof window, the prescription warning point and the service level of each litigation step (BRD Q-004)? | Legal counsel | Before wave 2 system test | CAP-S4-001, CAP-S4-002, CAP-S4-003, CAP-S4-023 | BRD Q-004; GAP-1467; ASM-2572 |
| OQ-S4-16 | What classification and what retention period apply to the legal action, the pack, the judgment and the enforcement record (DL26, BRD Q-012)? | Compliance and PDPA officer | Before wave 3 release | CAP-S4-016 to CAP-S4-025 | BRD Q-012; GAP-1475; ASM-2580; GAP-1749; ASM-2911 |
| OQ-S4-17 | Who owns the wording of MSG-S4-001, MSG-S4-002 and the reused MSG-GEN-001, MSG-P1-001, MSG-P4-002 and MSG-P7-003 in this service's steps, and who approves the Thai and English versions (DL10)? | Business analyst, S4 with Legal counsel and Compliance | Before wave 2 release | CAP-S4-001, CAP-S4-005, CAP-S4-020, CAP-S4-024 | GAP-1748; ASM-2910; DL10 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (ASM-2912).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 2 (business outcomes and the litigation turnaround measure), 5.11 (S4 requirements, REQ-S4-001 to REQ-S4-010), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan, E2 and E5), 9 (open decisions incl. DL18, DL22, DL26), 10.1 and 10.2 (the service epic RWB-SVC-S4, schema and wave) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 7.1 to 7.3 (E5 scope, services and waves), 8.3 (BR-034 to BR-043), 9 (RULE-001, RULE-002, RULE-025, RULE-026), 10 (KPI-002, KPI-009), 11.1 to 11.4 (ASM-015, CON-001 to CON-012, DEP-004, DEP-007, DEP-009, RISK-001 to RISK-003), 12 (Q-001, Q-004, Q-008, Q-012), 13 (governance) |
| Recovery Workbench FSD S4 Litigation and enforcement v3 | Document control, Existing capability check, A1.1 to A1.4 (scope, the 22 features, background, preconditions), A2.1 to A2.22 (functional decomposition with validation rules, business rules, field catalog, roles and acceptance criteria), Requirements served (REQ-S4-001 to REQ-S4-010), Screens (SCR-18 to SCR-20), Appendix A and B |
| Recovery Workbench Architecture v5 | Slides 4 (19 modules), 9 to 13 (call types, timeouts, retry, the connection matrix and the S4 row), 19 (the S4 service contract), 27 (rule governance), 30 (19 schemas), 37 (what changes and why), 38 (waves), 41 (service catalogue), 42 and 43 (event catalogue), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slides 5 and 8 (the prescription clock and the deviation that pauses one clock and not the other), 13 (one workflow per stage, LitigationWorkflow), 20 (S4 from notice to enforcement: steps, clocks, what Drools decides, who approves), 15 (rule governance and versioning), 16 (decision record), 24 (the agent run with rule fallback) |
| Recovery Workbench Microservice Ownership Map v1 | Services (S4 row), Endpoints (the five S4 paths and the two P6 notice paths), Workflows (LitigationWorkflow), Events (EV-15, EV-21), Tables (`legal_action`, `hearing`), Jobs (none owned by S4) and Rulings |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency, incl. NFR-003 partner users), 3.1 to 3.12 (requirements by quality characteristic, incl. write-once, legal hold and provenance), 4 (partner access, law firms first needed at Epic 5) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure, DP table, wave map), R8 (outputs), R9 (gaps and assumptions) |
