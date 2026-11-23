SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P9 rwb-reporting v1
description: Product requirements for the Recovery Workbench reporting service (P9 rwb-reporting) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v5.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.md
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P9 Reporting v3.md
service: P9 rwb-reporting
epic: RWB-SVC-P9
wave: 1
decision: D-RCV-60
---

# Recovery Workbench PRD P9 rwb-reporting v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P9 rwb-reporting |
| Document ID | P9-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | P9 rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 1 |
| Business epics | EP01 (Epic 1, wave 1); EP02 (Epic 2, wave 2); EP06 (Epic 6, wave 4); EP08 (Epic 8, wave 4). Program BRD section 10.2 gives the service the range EP01 to EP08 |
| Schema | `rwb_reporting` |
| REST base | `/api/recovery/reporting/v1` |
| Resources named in Architecture v5 | `GET /dashboards/{id}`, `GET /reports/{id}`, `POST /reports/{id}/run`; `GET /reports/measures` in the Ownership Map and API Specification v4 (GAP-1648) |
| Topic | `rwb.reporting.events.v1`; event `ReportPublished` |
| Temporal task queue | `rwb-reporting`; namespace `rwb-recovery` |
| Java package | `th.co.scb.ace.workbench.recovery.reporting` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Tribe lead for measures; Reporting and BI analyst for the data set; Compliance and PDPA officer for the returns (Program BRD section 5 owners) |
| Decision | D-RCV-60 (microservice realignment); inherits ADR-018 (no data lake; reporting read model from events) and ADR-015, ADR-016, ADR-020 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epic 1 v5; Business Requirements Epic 2 v3; Business Requirements Epics 3 to 8 v1; FSD P9 Reporting v3; Architecture v5; Temporal and Drools Design v1 |
| Upstream requirement IDs | RWB-E1-013 (P9 baseline measures); RWB-E2-009 (steering dashboard v1 data set); BR-061 (benefit realisation); BR-082 (regulatory returns); BR-083 (classification, staging and re-ageing); supporting keys REQ-WKM-009, REQ-WKM-006, REQ-CWC-015; retired key RWB-E1-014; REQ-DRI-009 retired with the data lake (GAP-1650) |
| Upstream feature IDs | FEAT-RPT-01 to FEAT-RPT-10 |
| Upstream acceptance criteria | AC-P9-001-01, AC-ALT-P9-001-01 to -02, AC-EXC-P9-001-01 to -06; AC-P9-002-01, AC-ALT-P9-002-01 to -02, AC-EXC-P9-002-01 to -08; AC-P9-003-01, AC-ALT-P9-003-01 to -02, AC-EXC-P9-003-01 to -04; AC-P9-004-01, AC-ALT-P9-004-01 to -02, AC-EXC-P9-004-01 to -06; AC-P9-005-01, AC-ALT-P9-005-01 to -02, AC-EXC-P9-005-01 to -03; AC-P9-006-01, AC-EXC-P9-006-01 to -02; AC-P9-007-01, AC-EXC-P9-007-01 to -02; AC-P9-008-01, AC-ALT-P9-008-01 to -02, AC-EXC-P9-008-01 to -04; AC-P9-009-01, AC-ALT-P9-009-01 to -02, AC-EXC-P9-009-01 to -03; AC-P9-010-01, AC-EXC-P9-010-01 to -02 |
| Upstream rule and message IDs | VR-P9-001-1 to VR-P9-010-1; BR-P9-001 to BR-P9-010; MSG-GEN-001, MSG-GEN-006, MSG-P1-001, MSG-P1-012, MSG-P1-019, MSG-P2-006, MSG-P3-011, MSG-P3-028, MSG-P3-029, MSG-P4-002, MSG-P7-003, MSG-P9-002, MSG-P9-003 |
| Upstream job, screen and check IDs | JOB-15 (reporting extract, 01:30, rwb-reporting); JOB-13 (decision log copy, retired role); JOB-04 (reconciliation, rwb-source-data); JOB-06 (rebalancing, rwb-case); SCR-37 Steering dashboard; REC-08 |
| Generated IDs | CAP-P9-001 to CAP-P9-014; FR-P9-001 to FR-P9-032; NFR-P9-001 to NFR-P9-024; AC-P9-001 to AC-P9-024; JRN-P9-01 to JRN-P9-06; ROL-P9-01 to ROL-P9-11; OQ-P9-01 to OQ-P9-14 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD P9 Reporting v3 (15 November 2026) and the BRD Program v5, Epic 1 v5, Epic 2 v3 and Epics 3 to 8 v1 (22 November 2026), realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD P9 Reporting v3. Its history, its feature IDs, its acceptance criteria and its rule and message IDs are carried unchanged; the realignment changes the owner, the read path and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010): source data read only through the `recovery.v_ace_*` views and landed by ACE ingestion; no inbound load, load run or data quality exception in the Workbench; reconciliation to `v_ace_account`; the INT-01 and COLLINS load wording removed; `dq_exception` replaced by `reconciliation_result` break rows. Everything else unchanged from v2. |
| 2 | Not specified in the source documents (GAP-1645; ASM-2786) | The FSD v3 change note states that everything else is unchanged from v2 and carries no v2 change note of its own |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey, role and open-question IDs are new; the FSD feature IDs (FEAT-RPT-01 to FEAT-RPT-10), the FSD acceptance criteria IDs (AC-P9-xxx), the validation rule IDs (VR-P9-xxx-y), the business rule IDs (BR-P9-xxx), the open decision IDs (DL10, DL26, DL43), the message IDs, JOB-15, JOB-13, JOB-04, JOB-06, REC-08, SCR-37, the measure codes, the definition version MD-2026.11 and the data product codes (DP01, DP03) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the reporting duties carried in sections 5.3, 5.6 and 5.7, the 78 non-functional requirements and the delivery model |
| Recovery Workbench Business Requirements Epic 1 v5 | BRD | Source of RWB-E1-013 (baseline measures) and the retirement of RWB-E1-014 |
| Recovery Workbench Business Requirements Epic 2 v3 | BRD | Source of RWB-E2-009 (steering dashboard v1 data set) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-061 (benefit realisation), BR-082 (regulatory returns) and BR-083 (classification, staging and re-ageing) |
| Recovery Workbench Functional Specifications by Module v6, FSD P9 Reporting v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, Kafka, Temporal Schedules, the bank Airflow outside the cluster, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: task queue, workflow kit, Schedules and event-started work |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, operation, event, job and workflow; P9 owns `measure_definition`, `measure_snapshot`, `measure_publish`, `GET /reports/measures` and JOB-15 |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

## 1.5 Requirement ID conventions used here

| ID family | Meaning in this document |
|---|---|
| CAP-P9-nnn | A capability: one releasable slice of product behaviour |
| FR-P9-nnn | A functional requirement, specific and testable |
| NFR-P9-nnn | A non-functional requirement with a target |
| AC-P9-nnn | An acceptance criterion in GIVEN/WHEN/THEN form, mapped to FR and NFR rows |
| JRN-P9-nn, ROL-P9-nn, OQ-P9-nn | Journey, role and open question |
| RWB-E1-013, RWB-E2-009, BR-061, BR-082, BR-083 | Business requirement keys, copied unchanged from the BRDs |
| FEAT-RPT-nn, AC-P9-nnn-nn, VR-P9-nnn-n, BR-P9-nnn | FSD keys, copied unchanged; they are the source trace for an FR or an AC row (GAP-1645) |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-reporting (P9) turns the numbers the Recovery programme is judged on into a product: one definition per measure, approved and versioned; one frozen baseline; a snapshot per business date that is published only when the data behind it is fresh and reconciles; the steering dashboard data set; report and regulatory extracts built from the reporting read model and the decision record; and the measures that tell the programme whether the change paid.

The service publishes and nothing else acts on its output. It is the one place where a recovery number is defined, so that the Tribe, the steering committee, Finance and the regulator read the same value.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-reporting | One deployable with its own API and worker, schema `rwb_reporting`, login, topic `rwb.reporting.events.v1`, task queue `rwb-reporting` and lifecycle | Reporting becomes one owned contract instead of a set of extracts inside a single deployable |
| A measure catalog with an approved version | Six definitions with formula, data product, unit and an approval, in force as MD-2026.11 from its valid-from date | A number nobody approved is a number nobody can defend |
| The reporting read model built from events | Projections from the business events and the decision record, held in `rwb_reporting` | The data lake is gone (ADR-018); the read model is the reporting store |
| The frozen baseline | One baseline per business date, marked baseline and never restated | Every later epic is measured against the same baseline (RWB-E1-013) |
| Publication gated on freshness and reconciliation | A snapshot that does not reconcile to the case list is not published, and the last good date stays visible | A number that is stale or short is worse than no number |
| Report and extract runs on request | `POST /reports/{id}/run` for a business date, with a rerun and a backfill | The extract is a dated, repeatable run, not an overnight side effect |
| The regulatory extract as a delivered file | Built from the read model and the decision record, handed to rwb-integration for delivery | The return must agree with the decision record, not with a separate count (BR-082) |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| Sign-in, access check, role matrix, masking policy, delegation of authority, access log | REUSE | P4 rwb-access; ACE common sign-in |
| Decision record, audit trail, hash chain, central ledger | REUSE | P7 rwb-decision through the local decision-record library and `rwb.decision-record.v1` |
| Case list rows, data products, freshness stamp, reconciliation results | REUSE | P1 rwb-source-data; the numbers are read through P1's contract, never recomputed here |
| Case, queue, owner, ageing and service level facts | REUSE | P3 rwb-case, including `queue_measure` |
| Parameters, reference data and the measure thresholds a person may change | REUSE | P3 rwb-case (default ruling of R-PREC) |
| File delivery and the file manifest | REUSE | P2 rwb-integration, `deliverFile` |
| Documents, notices, payments, treatments, guarantee claims, write-off approval, debt sale | REUSE | P5, P6, P8, S2, S3, S7, S6, through their events and their projections |
| Data lake and the Power BI connection (INT-19, INT-20) | REMOVED | None. ADR-018, DP-17 (GAP-1646) |
| Decision log copy to the data lake (JOB-13, FEAT-RDF-20, RWB-E1-014) | RETIRED | None. Decision-log ingest is continuous from Kafka in P7; the projection here reads DecisionRecorded (GAP-1650) |
| Case count reconciliation and the data quality break record (FEAT-RPT-05, FEAT-RPT-09) | REUSE, elsewhere | P1 rwb-source-data owns `reconciliation_result` and JOB-04; the report and the break list are read here (GAP-1651) |
| Queue depth and ageing computation (FEAT-RPT-02) | REUSE, elsewhere | P3 rwb-case owns `queue_measure` and JOB-06; the measures are published here (GAP-1652) |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; this service writes only `rwb_reporting` and reads no ACE view and no other service's table (ADR-014, ADR-010, DP-01, DP-05).
2. Reporting builds its read model from events and its own projections; heavy reporting runs from `rwb_reporting`, not from ACE tables (ADR-018, DP-17).
3. REST is one hop from gateway-bff, with a 2 s timeout; anything longer is a workflow or an activity (ADR-020, DP-11).
4. Events are CloudEvents on Kafka with outbox and inbox; topic `rwb.reporting.events.v1`; retry and `.dlt` topics (ADR-015, DP-09, DP-14).
5. Temporal namespace `rwb-recovery`, task queue `rwb-reporting`; Schedules replace Quartz; `rwb-source-data`'s `snapshot(page)` activity feeds the measures (ADR-016, DP-10, DP-12).
6. The bank scheduler sits outside the cluster and calls APIs only; it triggers the report extract (Arch v5 slide 31 note 3) (GAP-1647).
7. No data lake and no Power BI connection: the dashboard and the measures are served by this service on the gateway-bff composite route (ADR-018, DP-19) (GAP-1646; ASM-2788).
8. Personal data stays out of events, workflow inputs and measure rows; a report that returns a personal field is masked by role and logged (Arch v5 slide 45; NFR-039, NFR-042).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-P9-01 | Tribe lead | A definition per measure, approved and versioned, and one baseline every later epic is measured against | JRN-P9-01, JRN-P9-02 |
| ROL-P9-02 | Reporting and BI analyst | A data set per business date with a freshness stamp, and a clear statement when a date is not published | JRN-P9-02, JRN-P9-05 |
| ROL-P9-03 | Program manager | The same numbers the teams work with, by stage, queue, age and agent version | JRN-P9-02 |
| ROL-P9-04 | Team manager | Queue depth, ageing and owner spread that reconcile to the case list | JRN-P9-03 |
| ROL-P9-05 | Data steward and data product owner | A held publication with its reason, its difference and its owner, and a break worked to closure | JRN-P9-03, JRN-P9-05 |
| ROL-P9-06 | Finance and CFO delegate | Benefit realisation against the baseline, monthly, with no target invented | JRN-P9-06 |
| ROL-P9-07 | Compliance and PDPA officer | Returns built from the data products and the decision record, and a masked report read | JRN-P9-04, JRN-P9-05 |
| ROL-P9-08 | Internal audit | A measure traceable to the record it was counted from, and a reproducible published value | JRN-P9-04 |
| ROL-P9-09 | Platform administrator | A run per business date, a rerun and a backfill, and an alert when a run fails | JRN-P9-01, JRN-P9-05 |
| ROL-P9-10 | Risk and model risk officer | Agent acceptance and override per agent and version, on the same record as the decision | JRN-P9-02, JRN-P9-05 |
| ROL-P9-11 | Solution architect | One contract per resource, one schedule per report, and no read of ACE or of another service's schema | JRN-P9-04 |

Non-human actors: the bank scheduler (Airflow) calling `POST /reports/{id}/run`; the outbox relay; the Temporal worker running the measure schedule and the extract activity; the consumers of ReportPublished. The bank Airflow sits outside the 19 services and calls APIs only (Arch v5 slide 31, note 3).

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. Measures are counted by hand from spreadsheets at month end (FSD P9 A1.3).
2. The decision log is copied to the data lake each night and reporting reads the copy; a copy that does not match delays the number.
3. The baseline is restated whenever a definition changes, so two months are never measured the same way.
4. Queue depth is reported from one query and the case list from another, and the difference is found in the meeting.
5. A measure with no definition still produces a number, because the extract configuration is not checked against the catalog.

Consequence: two numbers for one question, no approval behind either, and a programme that cannot say whether it worked.

## 4.2 Target state (this product)

### JRN-P9-01 Measure definitions and the baseline (on change, then once)

1. The Tribe lead agrees six definitions: code, name, the formula in plain terms, the data product it reads, the unit, the definition version and the approval.
2. The Reporting and BI analyst loads them; a row without a formula, a product or a unit refuses the load whole with MSG-GEN-001 naming the field, and no version is put in force.
3. With a complete load, the version MD-2026.11 is in force from 2026-11-21 with approver TRB-0001 and its approval date 2026-11-20.
4. The measure catalog returns each measure with its data product and its formula, so the definition behind a number is readable without asking.

### JRN-P9-02 The measure refresh and the steering dashboard (daily 01:30, read monthly)

1. The bank scheduler calls the run operation for the reporting extract at 01:30, or the schedule fires at 01:30, for the business date (GAP-1647).
2. Every data product the measures read must be complete for the business date; otherwise the run records the product and the last completed date (MSG-P1-001) and writes no rows for that date.
3. The measures are computed from the read model, one row per measure per business date, stamped with the definition version in force.
4. The snapshot is checked against the case list at the same time: a queue whose depth differs from the case list count is not published (MSG-P3-029), and a dashboard total that differs from the case list holds the whole date (MSG-P9-002).
5. A published date carries its freshness stamp and starts the day's dashboard read; the sums by stage equal the case list and the decisions logged equal the decision records of that day.
6. Agent acceptance and override are published per agent and version; a version with no recommendations shows "No runs" rather than zero.

### JRN-P9-03 Queue and ageing measures (daily, team manager)

1. The team manager opens the queue measures for their team: depth, unassigned, average age and owner spread per queue.
2. Each queue's depth equals the case list count for that queue at the snapshot time; a queue with no capacity cap is still reported.
3. A breach recorded on a case appears in the next snapshot as one more breach for that queue.

### JRN-P9-04 Report and regulatory extract run (on request, wave 4)

1. A report has an id, a name, the data products it reads, the definition version in force and an owner role.
2. The bank scheduler or the platform administrator requests a run for a business date; a run already in progress refuses the second request with status 409 and MSG-P2-006.
3. The extract is built and handed to rwb-integration for delivery, with the freshness stamp and the record count in its trailer; a delivery that fails holds the extract and alerts the operations channel with MSG-GEN-006 naming the target.
4. A copy that does not match the projection is not published: the check fails with REC-08 and MSG-P1-019 and the watermark stays where it was.
5. A regulator's request is answered from the published extract and the decision record, never from the live log store.

### JRN-P9-05 A date that cannot be published (data steward)

1. The steward receives the hold with the check, the difference in count and percent, and the business date.
2. The cause is fixed where it belongs: the case list in P1, the queue measure in P3, the stale product in ACE through P1's freshness stamp.
3. A rerun for the same business date writes no duplicates; a run that succeeds publishes and the previous held date is released.
4. The dashboard shows the last published date while a date is held, so a reader never sees a partial number.

### JRN-P9-06 Benefit realisation (monthly, wave 4)

1. Finance and the Reporting and BI analyst open the benefit view: each measure against its baseline, month by month, with the definition version used.
2. Where the benefit model sets no measure and no target, the view states that, and no value is invented (BRD Epics 3 to 8 Q-020).
3. The monthly view is itself a publication, with a decision record and a hash-chained entry.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD; a capability whose requirement sits in another service is stated here as a read, never as an owner.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-P9-001 | Measure catalog with an approved definition version | Every number has a formula, a data product, a unit and an approval, and the version that produced it is readable | RWB-E1-013 | Must | 1 | FEAT-RPT-01 (A2.1) |
| CAP-P9-002 | Frozen baseline per business date | The programme is measured against one agreed set, not against last month's restatement | RWB-E1-013 | Must | 1 | FEAT-RPT-01 (A2.1) |
| CAP-P9-003 | Measure refresh on the business date | A dated, repeatable run instead of a month-end count by hand | RWB-E1-013, REQ-WKM-009 | Must | 1 | FEAT-RPT-08 (A2.8) |
| CAP-P9-004 | Freshness stamp on every measure, snapshot and extract | A reader knows the business date and the source data behind the number | RWB-E1-013 | Must | 1 | FEAT-RPT-08 (A2.8) |
| CAP-P9-005 | Publication gate: no publish from stale, short or unreconciled data | A number that does not reconcile never reaches the dashboard, and the last good date stays visible | RWB-E1-013, REQ-WKM-006 | Must | 1 | FEAT-RPT-08 (A2.8) |
| CAP-P9-006 | Queue depth, ageing and owner spread | Teams see the same queue position that the case list holds | REQ-CWC-015, REQ-WKM-006 | Must | 1 | FEAT-RPT-02 (A2.2) |
| CAP-P9-007 | Steering dashboard data set (SCR-37) | The steering committee reads volume, ageing, route mix, turnaround, recovery and decision quality in one set | RWB-E2-009, REQ-WKM-009 | Should | 2 | FEAT-RPT-03 (A2.3) |
| CAP-P9-008 | Agent acceptance and override measures | An agent version is judged on the decisions it recommended and how often people changed them | RWB-E2-009 | Should | 2 | FEAT-RPT-03 (A2.3) |
| CAP-P9-009 | Operations reporting from the decision record | Reporting and audit read the same record, without touching the live log store | RWB-E2-009 | Must | 2 | FEAT-RPT-04 (A2.4) |
| CAP-P9-010 | Report and extract run on request, with rerun and backfill | A dated run that can be repeated for any business date, refused twice at once | RWB-E1-013 | Must | 1 | FEAT-RPT-08 (A2.8) |
| CAP-P9-011 | Reconciliation and data quality break view | A break is seen with its difference, its owner and its date, and closed with evidence | REQ-WKM-006 | Must | 2 | FEAT-RPT-05 (A2.5); FEAT-RPT-09 (A2.9) |
| CAP-P9-012 | Regulatory returns | A return built from the data products and the decision record and delivered as a dated file | BR-082 | Must | 4 | FEAT-RPT-07 (A2.7) |
| CAP-P9-013 | Benefit realisation against the baseline | The programme reports what it earned, month by month, against the frozen baseline | BR-061 | Must | 4 | FEAT-RPT-06 (A2.6) |
| CAP-P9-014 | Classification, staging and re-ageing applied and the segment recomputed | A stale classification cannot misstate the book, and a rule change takes effect from its valid-from date | BR-083 | Must | 4 | FEAT-RPT-10 (A2.10) |

## 5.1 Capabilities not carried into this service

| Capability | Status | Later home |
|---|---|---|
| Copy the decision log to the data lake daily and match row counts (FEAT-RDF-20, JOB-13, RWB-E1-014) | Retired | None. Decision-log ingest is continuous from Kafka in rwb-decision; the projection here reads DecisionRecorded (GAP-1650) |
| Publish the measure set to the data lake and the Power BI data set (INT-19, INT-20) | Removed | None. ADR-018 removes both; the dashboard and the measures are served by this service (GAP-1646) |
| Reconcile the case list to `v_ace_account` and hold the publish (FEAT-RDF-11, FEAT-RDF-13, JOB-04) | Reuse, elsewhere | P1 rwb-source-data owns the reconciliation and the hold; this service reads the results (GAP-1651) |
| Compute queue depth and rebalance the queues (FEAT-CWC-18, JOB-06) | Reuse, elsewhere | P3 rwb-case; this service publishes the measures (GAP-1652) |
| Load and version parameters, reference data and the measure thresholds | Reuse, elsewhere | P3 rwb-case (default ruling of R-PREC) |
| Serve the queue and case list screens | Reuse, elsewhere | P3 rwb-case behind the gateway-bff composite route (DP-19) |
| Serve the report and dashboard screens themselves | Out of scope | The edge composite route and the Design System; this service serves the resource (GAP-1658) |

# 6. Functional requirements

Every requirement is specific and testable. A requirement whose subject belongs to another service is written as a read of that service's contract. The FSD source column carries the feature and acceptance criterion the requirement comes from, because FSD P9 has no requirement IDs of its own (GAP-1645).

| FR ID | Requirement | CAP | BR | FSD source | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-P9-001 | The service SHALL hold each measure as one row of a versioned definition set, carrying measure code, name, the formula in plain terms, the data product it reads, the unit, the definition version, the approver and the approval time. | CAP-P9-001 | RWB-E1-013 | FEAT-RPT-01; measure_definition field catalog | Must | 1 |
| FR-P9-002 | The service SHALL refuse a definition load whole when a row has no formula, no data product or no unit, SHALL name the offending field with MSG-GEN-001, and SHALL leave the version in force unchanged. | CAP-P9-001 | RWB-E1-013 | AC-EXC-P9-001-01; VR-P9-003-1 | Must | 1 |
| FR-P9-003 | The service SHALL put a loaded definition set in force from its valid-from date as one version, and SHALL return every measure of the version in force with its data product and its formula through the measure catalog. | CAP-P9-001 | RWB-E1-013 | AC-P9-001-01 | Must | 1 |
| FR-P9-004 | The service SHALL write one snapshot row per measure per business date, marked baseline and frozen for the first published business date, and SHALL never restate a frozen baseline row. | CAP-P9-002 | RWB-E1-013 | AC-ALT-P9-001-01 | Must | 1 |
| FR-P9-005 | The service SHALL write no measure row for a business date while any data product the measure reads is not complete for that date in the source-data freshness contract, SHALL record the product and the last completed date with MSG-P1-001, and SHALL publish the date at the first run after the product is complete. | CAP-P9-004 | RWB-E1-013 | AC-EXC-P9-001-02; VR-P9-001-1 | Must | 1 |
| FR-P9-006 | The service SHALL carry the business date, the definition version and the freshness stamp of the data products read on every snapshot row and every published extract. | CAP-P9-004 | RWB-E1-013 | AC-P9-003-01; AC-ALT-P9-001-02 | Must | 1 |
| FR-P9-007 | The service SHALL answer a measure read for a period with a value for each measure of the version in force and the period it belongs to, and SHALL serve the read inside the user wait. | CAP-P9-003 | RWB-E1-013, REQ-WKM-009 | AC-P9-003-01; AC-P9-008-01 | Must | 1 |
| FR-P9-008 | The service SHALL write no value and SHALL record MSG-P9-003 naming the measure when the extract lists a measure with no definition in force. | CAP-P9-001 | RWB-E1-013 | AC-EXC-P9-001-04 | Must | 1 |
| FR-P9-009 | The service SHALL publish queue depth, unassigned count, average age and owner spread per queue for the business date, and each queue's depth SHALL equal the case list count for that queue at the snapshot time. | CAP-P9-006 | REQ-CWC-015, REQ-WKM-006 | AC-ALT-P9-002-01; FEAT-RPT-02 | Must | 1 |
| FR-P9-010 | The service SHALL hold the publication of a snapshot when a queue's depth differs from the case list count at the snapshot time, and SHALL notify the data steward with MSG-P3-029 naming the check "queue depth against case list". | CAP-P9-005 | REQ-WKM-006 | AC-ALT-P9-002-02 | Must | 1 |
| FR-P9-011 | The service SHALL hold the publication of a business date when the case facts counted for the dashboard differ from the case list count, SHALL publish no snapshot rows and no extract for that date, SHALL state both numbers and the date with MSG-P9-002, and SHALL keep the last published date visible on SCR-37. | CAP-P9-005 | RWB-E2-009, REQ-WKM-006 | AC-EXC-P9-003-01; AC-EXC-P9-008-01 | Must | 2 |
| FR-P9-012 | The service SHALL publish the sum of the cases by stage for a business date equal to the open case count of the case list at the cut-off, and the count of decisions logged equal to the decision records decided that day. | CAP-P9-007, CAP-P9-009 | RWB-E2-009, REQ-WKM-009 | AC-ALT-P9-003-01; AC-ALT-P9-008-01 | Should | 2 |
| FR-P9-013 | The service SHALL publish agent acceptance and agent override as percentages of the recommendations made by each agent and version for the business date, and SHALL show both rates by agent. | CAP-P9-008 | RWB-E2-009 | AC-ALT-P9-003-02 | Should | 2 |
| FR-P9-014 | The service SHALL write no agent measure for an agent and version with no recommendations on the business date and SHALL show "No runs" for it rather than a zero. | CAP-P9-008 | RWB-E2-009 | AC-EXC-P9-003-02; AC-EXC-P9-008-02 | Should | 2 |
| FR-P9-015 | The service SHALL build the operational and decision measures from the decision record it receives, and SHALL never read the live decision-log store for a measure. | CAP-P9-009 | RWB-E2-009 | FEAT-RPT-04; ADR-018; GAP-1650; ASM-2792 | Must | 2 |
| FR-P9-016 | The service SHALL expose a run operation per report for a business date, SHALL accept a rerun for any business date and a backfill over a range, and SHALL answer the request before the run completes. | CAP-P9-010 | RWB-E1-013 | FEAT-RPT-08; Arch v5 slide 31 | Must | 1 |
| FR-P9-017 | The service SHALL refuse a second run for a report that is already running with status 409 and MSG-P2-006, and SHALL let one run continue. | CAP-P9-010 | RWB-E1-013 | AC-ALT-P9-004-02 | Must | 1 |
| FR-P9-018 | The service SHALL write no duplicate row for a business date on a rerun: a repeated run for a date leaves that date's rows as one set with one value per measure. | CAP-P9-010 | RWB-E1-013 | AC-EXC-P9-004-02 (carried; the lake element is removed) | Must | 1 |
| FR-P9-019 | The service SHALL start the reporting extract of a business date at 01:30 through its run operation and SHALL record the run with its report id, business date, row count, start and end time. | CAP-P9-003 | RWB-E1-013 | JOB-15; Arch v5 slide 44 | Must | 1 |
| FR-P9-020 | The service SHALL hand the regulatory extract to rwb-integration for delivery with the freshness stamp and the record count in its trailer, and SHALL publish nothing until the delivery is acknowledged. | CAP-P9-012 | BR-082 | AC-P9-004-01 (carried; the lake target is replaced by file delivery); Arch v5 slide 15 | Must | 4 |
| FR-P9-021 | The service SHALL hold the extract and alert the operations channel with MSG-GEN-006 naming the target when delivery does not answer, SHALL keep the rows it wrote, and SHALL send the held extract on the next run for that date. | CAP-P9-012 | BR-082 | AC-EXC-P9-001-03 (carried; the lake is replaced by the delivery target); ASM-2799 | Must | 4 |
| FR-P9-022 | The service SHALL compare a delivered extract with the projection it was built from, SHALL not mark it delivered when the record count or the last hash differ, SHALL fail check REC-08 with MSG-P1-019, and SHALL leave the watermark unchanged. | CAP-P9-012 | BR-082 | AC-EXC-P9-004-01 (carried; check REC-08 kept) | Must | 4 |
| FR-P9-023 | The service SHALL publish ReportPublished on `rwb.reporting.events.v1` for each published report, carrying the report id, the business date, the definition version and the row count, and no personal data. | CAP-P9-003 | RWB-E1-013 | Arch v5 slide 15 (OUT topic) | Must | 1 |
| FR-P9-024 | The service SHALL report benefit realisation monthly as each measure of the benefit model against its baseline, with the definition version used, and SHALL state where the benefit model sets no measure or no target rather than compute one. | CAP-P9-013 | BR-061 | FEAT-RPT-06; RWB-E6-037 | Must | 4 |
| FR-P9-025 | The service SHALL produce each regulatory return from the data products and the decision record, one row per return item for the stated period, with the rule and definition versions applied. | CAP-P9-012 | BR-082 | FEAT-RPT-07; RWB-E8-001 | Must | 4 |
| FR-P9-026 | The service SHALL apply the classification, staging and re-ageing rules from the version in force, and SHALL recompute the segment when a rule version changes from its valid-from date without a code release. | CAP-P9-014 | BR-083 | FEAT-RPT-10; RWB-E8-002 | Must | 4 |
| FR-P9-027 | The service SHALL show each open data quality break with its check, its business date, its difference, its owner role and its due date, SHALL read the break from the reconciliation result of rwb-source-data, and SHALL close a break only with a closing note and a decision record. | CAP-P9-011 | REQ-WKM-006 | FEAT-RPT-09; FEAT-RPT-05; GAP-1651; ASM-2793 | Must | 2 |
| FR-P9-028 | The service SHALL control read access to each report and dashboard by role, SHALL return a personal field masked where the role has no unmasked masking row, and SHALL refuse the read with MSG-P4-002 where the role holds no right. | CAP-P9-007 | RWB-E2-009 | AC-EXC-P9-003-03; AC-EXC-P9-001-05; NFR-039; NFR-040 | Must | 1 |
| FR-P9-029 | The service SHALL write one access log entry per report read that returns a personal field, and SHALL refuse the read rather than return the field when the entry cannot be written. | CAP-P9-007 | RWB-E2-009 | NFR-042; REQ-ACA-006 | Must | 1 |
| FR-P9-030 | The service SHALL hold no personal data in a measure row, an extract row or an event: every measure is a count, a sum, a duration or a percentage. | CAP-P9-003 | RWB-E1-013 | Arch v5 slide 42 note; NFR-040 | Must | 1 |
| FR-P9-031 | The service SHALL write a decision record for every publication, run, hold and break closure, and SHALL complete no such action when the record cannot be written (MSG-P7-003, incident raised). | CAP-P9-003 | RWB-E1-013 | AC-EXC-P9-003-04; AC-EXC-P9-001-06; DP-03 | Must | 1 |
| FR-P9-032 | The service SHALL hold every value a business person may change, including a tolerance, a threshold, a cut-off and a report definition, as a versioned data row read at run time, and SHALL apply it from its valid-from date without a code release. | CAP-P9-001 | RWB-E1-013 | BR-P9-001 to BR-P9-010 | Must | 1 |

## 6.1 Business rules that qualify the requirements

| Rule | Statement | Source |
|---|---|---|
| No value in code | A value a business person may change is a versioned reference row read at run time | BR-P9-001 to BR-P9-010 |
| One definition per measure per version | A measure has exactly one definition in a version, and one version in force at a time | AC-P9-001-01, AC-EXC-P9-001-01 |
| No publish without freshness | A data product that is not complete for the business date stops the rows for that date | VR-P9-001-1 to VR-P9-008-1 |
| No publish without reconciliation | A count difference between the snapshot and the case list holds the date | AC-ALT-P9-002-02, AC-EXC-P9-003-01 |
| Decisions from the record | A decision measure is counted from the decision record, never from a separate count | NFR-065; FEAT-RPT-04 |
| Reads, not ownership | The case list, the queue measure and the reconciliation result are read from their owners, never recomputed here | Ownership Map; GAP-1651; GAP-1652 |
| No restatement | A frozen baseline row is never changed; a corrected definition is a new version | AC-ALT-P9-001-01 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-P9-001 | A dashboard, measure or report read by a user answers inside the user's wait under the busiest-hour load. | Under 2 seconds | NFR-008 | Must | Performance test in SIT at the busiest-hour load |
| NFR-P9-002 | The measure set and the extract of a business date are published before the working day's first read. | Extract run at 01:30; published before the 07:30 refresh | NFR-013, NFR-019 | Must | Run the schedule against a completed batch and read the publication time |
| NFR-P9-003 | The service is available in business hours and outside them, when the runs and the extracts happen. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-P9-004 | The service inherits the ACE recovery point and recovery time for the read model and the snapshots. | The ACE recovery point objective and recovery time objective | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-P9-005 | The read model and the snapshot history carry the case population and its growth for the whole programme. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts a month; one snapshot row per measure per business date | NFR-001 | Must | Volume test with data at the stated volume |
| NFR-P9-006 | A measure, a snapshot or an extract is published only on a business date whose data products are complete, and a stale product is visible on the report. | No publication from a stale product; the last completed date shown | NFR-013, NFR-014 | Must | Hold an ACE batch and read the report |
| NFR-P9-007 | A decision measure is produced from the decision record and never from a separate count. | From the record | NFR-065 | Must | Compare the measure with the record for one day |
| NFR-P9-008 | Agent acceptance, override, latency and cost are measured per agent and version. | Measured per agent and version; no threshold is set (GAP-1659; ASM-2803) | NFR-066 | Must | Agent measure review per version |
| NFR-P9-009 | Every published value is reproducible from the definition version and the record it was counted from. | Every value reproducible | NFR-033, NFR-034 | Must | Re-run a published date and compare |
| NFR-P9-010 | Every publication, run, hold and closure writes a decision record, and a failed write stops the action. | Every action; no silent publication | NFR-033, NFR-035 | Must | Fail the decision-record write on a publish |
| NFR-P9-011 | A report or dashboard read returns a personal field masked by role, and a role with no unmasked row never sees it. | Masked by default; data minimized per report | NFR-039, NFR-040 | Must | Masking matrix test across roles |
| NFR-P9-012 | Every read of a personal field in a report is logged. | 100 percent of such reads | NFR-042 | Must | Access log reconciliation against reads |
| NFR-P9-013 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-P9-014 | Staff authenticate with single sign-on and multi-factor authentication; non-human callers use their own service identity. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-P9-015 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; an event that cannot be processed goes to the dead-letter topic and is replayed. | One hop; 2 s timeout; three retries then the exception queue | NFR-025, NFR-026 | Must | Failure injection |
| NFR-P9-016 | Logs, traces and metrics are produced for every run, publication, hold and delivery, and every schedule has a run book, monitoring and an alert. | Every schedule and run covered | NFR-064, NFR-067 | Must | Observability review |
| NFR-P9-017 | A failing run, delivery or agent measure raises an alert to a named owner. | Within 15 minutes | NFR-068 | Must | Alert drill |
| NFR-P9-018 | Screen labels, validation messages and error messages served with this service's reads and runs are available in Thai and in English. | Every label and message in Thai and English | NFR-059 | Must | Label and message review |
| NFR-P9-019 | The dashboard and report screens meet the bank's accessibility standard on the supported browsers. | WCAG 2.1 level AA; current and previous major versions of Edge and Chrome | NFR-060, NFR-061 | Must | Accessibility and browser review |
| NFR-P9-020 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in its own schema. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-P9-021 | A snapshot, an extract and a report run are retained by class, and a disposal is a recorded decision. | Class declared per entity; periods open (DL26) | NFR-030, NFR-031 | Must | Retention review (GAP-1655; ASM-2797) |
| NFR-P9-022 | No production data is used in development, and user acceptance uses masked copies; the test extract volume is synthetic. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-P9-023 | The read model, the snapshots and the extracts stay in the bank's own cloud tenancy in the agreed region, and every report carries a classification. | SCB Azure, Southeast Asia; classification per report | NFR-046, NFR-047 | Must | Tenancy and classification review |
| NFR-P9-024 | An audit or regulatory request is answered from a published extract and the decision record inside the requester's deadline. | Inside the deadline set by the requester | NFR-036 | Must | Request drill with a fixed population |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_reporting`. Every table carries the seven standard record columns of the platform library. Retention is stated by class; the periods are open (GAP-1655; ASM-2797).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `measure_definition` | Versioned reference | `measure_code`; name, formula, `data_product`, unit, `definition_version`, `approved_by`, `approved_at`. The field catalog of FSD P9 A2.3 and A2.6 lists exactly these eight fields | [CONFIDENTIAL] | Workbench reference data, loaded by the Reporting and BI analyst and approved by the Tribe lead | Versioned; superseded versions kept |
| `measure_snapshot` | Transaction (one row per measure per business date) | `measure_code`, `business_date`, `definition_version`, value, unit, baseline flag, freshness stamp. Remaining fields: Not specified in the source documents (GAP-1654; ASM-2796) | [CONFIDENTIAL] | Built from the read model; the case facts through rwb-source-data's `snapshot(page)` activity | By class; period open (DL26) |
| `measure_publish` | Transaction (publication per report and business date) | `report_id`, `business_date`, `definition_version`, publication status, freshness stamp, row count. Remaining fields: Not specified in the source documents (GAP-1654; ASM-2796) | [CONFIDENTIAL] | Workbench computation | By class; period open (DL26) |
| Report and return definitions | Versioned reference | Report id, name, the data products read, the definition version, the owner role, the schedule. Fields: Not specified in the source documents (GAP-1654; ASM-2796) | [CONFIDENTIAL] | Workbench reference data | Versioned; superseded versions kept |
| Extract run record | Transaction | `report_id`, `business_date`, start time, end time, row count, status, watermark | [CONFIDENTIAL] | Workbench computation | By class; period open (DL26) |
| Break view entry | Read-through view over the reconciliation result of rwb-source-data | Check code (REC-01, REC-02, REC-05), business date, difference, difference percent, owner role, due date, closing note. Fields: Not specified in the source documents (GAP-1654; ASM-2796) | [CONFIDENTIAL] | rwb-source-data `reconciliation_result` through its contract; never owned here | Not held here; the break record stays with P1 |
| Read-model projections | Projection | The case, queue, decision, treatment, guarantee, comms, write-off and debt sale facts the measures count, one projection per event family. Fields: Not specified in the source documents (GAP-1654; ASM-2796) | [CONFIDENTIAL]; [SENSITIVE_FINANCIAL] where an amount is carried | Business events on Kafka, with the inbox for deduplication | By class; period open (DL26) |

Not carried: `lake_copy_watermark` and the lake partitions of the decision-log copy. They are legacy objects with no target: the data lake is removed and the copy is retired (GAP-1650).

## 8.2 Data read but not owned

| Data | Owner | Path | Classification of the data read |
|---|---|---|---|
| Case list rows, case counts and the open case population | P1 rwb-source-data | Temporal activity `snapshot(page)` and its REST contract | [SENSITIVE_FINANCIAL] |
| Freshness stamp per data product and business date | P1 rwb-source-data | REST through the freshness contract | [CONFIDENTIAL] |
| Reconciliation results and break rows (REC-01, REC-02, REC-05) | P1 rwb-source-data | REST through its contract | [CONFIDENTIAL] |
| Queue depth, unassigned count, average age and owner spread | P3 rwb-case (`queue_measure`) | REST through its contract | [CONFIDENTIAL] |
| Case, allocation, transfer and state events | P3 rwb-case | Kafka `rwb.case.events.v1` (EV-01, EV-02, EV-04, EV-05) | [CONFIDENTIAL] |
| Decision record | P7 rwb-decision and every producer | Kafka `rwb.decision-record.v1` (EV-08) | [CONFIDENTIAL] |
| Notice dispatched | P6 rwb-comms | Kafka `rwb.comms.events.v1` (EV-14) | [CONFIDENTIAL] |
| Treatment closed, guarantee claim, accounts transferred | S2, S3, S6 | Their topics, per the event catalogue | [SENSITIVE_FINANCIAL] |
| Write-off approved | S7 rwb-writeoff | Kafka `rwb.writeoff.events.v1` (EV-24) | [SENSITIVE_FINANCIAL] |
| Role, masking policy and access log | P4 rwb-access | REST, cached | [CONFIDENTIAL] |
| Parameters, reference data and thresholds | P3 rwb-case | REST through its contract | [CONFIDENTIAL] |

## 8.3 Field-level requirements for personal and financial data

| Field or measure | Meaning | Classification | Requirement |
|---|---|---|---|
| Any account number or customer identifier in a report row | An account or customer the report names | [PII] | Masked unless the role holds an unmasked masking row; every read logged (FR-P9-028, FR-P9-029) |
| Case, queue and stage counts in a measure | Portfolio position at a business date | [CONFIDENTIAL] | Aggregate only; never a person or an account |
| Amounts in `REALIZED_RECOVERY`, a return item or a benefit row | Money recovered or reported | [SENSITIVE_FINANCIAL] | Read access by role; no amount in an event |
| `measure_definition.formula`, `unit`, `definition_version` | How a number is made | [CONFIDENTIAL] | Versioned; a change is a new version, never an edit |
| Agent acceptance and override per version | How a model performed | [CONFIDENTIAL] | Per agent and version only; never per officer |
| Definition approver and approval time | Who approved a definition, by role | [CONFIDENTIAL] | Role identifiers only; no person is named in this document |

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code.
2. A measure is a count, a sum, a duration or a percentage; no measure row and no extract row carries a person or an account.
3. The case list, the queue measure and the reconciliation result are read through their owner's contract, never from another service's table.
4. A frozen baseline row is never changed; a corrected definition is a new version.
5. A publication is written with the definition version and the freshness stamp that produced it, so the value can be reproduced.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| gateway-bff | In | REST composite route, one hop, 2 s timeout: `GET /dashboards/{id}`, `GET /reports/{id}`, `GET /reports/measures` | Platform edge (RWB-PLT-EDGE) | The composite route joins this service's answer with the case and queue facts of rwb-case (GAP-1648) |
| Bank scheduler (Airflow) | In | REST `POST /reports/{id}/run`, one hop, mutual TLS with client credentials | Bank platform team or Recovery (open: GAP-1647; ASM-2789) | JOB-15 at 01:30, a rerun for any business date and a backfill; the scheduler never reads a schema |
| rwb-source-data (P1) | Out | Temporal activity `snapshot(page)`; REST for freshness and reconciliation results | P1 | The case facts behind the measures, the freshness stamp and the break rows |
| rwb-case (P3) | Out | REST for queue measures and case counts | P3 | `queue_measure` and the case list count at the snapshot time |
| rwb-integration (P2) | Out | Temporal activity `deliverFile` | P2 | The regulatory extract and its manifest; delivery result and evidence of receipt |
| rwb-access (P4) | In | REST, cached | P4 | Authorise, role scope and field masking policy |
| rwb-decision (P7) | Out | Kafka, decision-record library and `rwb.decision-record.v1` | P7 | One record per publication, run, hold and closure |
| `rwb.reporting.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and `.dlt` topics, keyed by report and business date | This service | ReportPublished; consumers notified per the event catalogue |
| `rwb.case.events.v1`, `rwb.decision-record.v1`, `rwb.comms.events.v1`, `rwb.treatment.events.v1`, `rwb.writeoff.events.v1`, `rwb.debtsale.events.v1` and the guarantee topic | In | Kafka, inbox deduplication | P3, P7, P6, S2, S7, S6, S3 | The projections the measures count |
| Agent run facts | In | Not fixed in v5 | P10 | The agent measures need a source; the event catalogue lists rwb-decision, rwb-document and rwb-deviation as the consumers of AgentRunCompleted, and the consumer matrix gives this service no dependency on P10 (GAP-1663; ASM-2801) |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5; no measure and no extract leaves the read model except as a delivered file (GAP-1646, GAP-1662; ASM-2788) |
| Decision log copy (JOB-13) | Removed | None | None | Retired with the data lake; the projection reads DecisionRecorded (GAP-1650) |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Who owns the bank scheduler's DAGs, where does it run, and does the measure run stay a Temporal Schedule at 01:30 while the extract is called through the run operation? | Solution architect with the bank platform team | Two mechanisms for one job are named in v5; a build needs one (GAP-1647; ASM-2789) |
| Which identifier does `GET /reports/{id}` and `POST /reports/{id}/run` take, and does the measure read stay `GET /reports/measures`? | Solution architect with the API owner | The published contract cannot carry both without a decision (GAP-1648; ASM-2790) |
| What is the source of the agent acceptance and override measures, given that the event catalogue does not list this service as a consumer of AgentRunCompleted? | Solution architect with the AI product owner | The agent measures of RWB-E2-009 cannot be built without a source (GAP-1663; ASM-2801) |
| Is SCR-37 served by this service on the dashboard resource, or composed by the edge from the case and queue views? | Solution architect | Decides whether the screen is a capability of this service (GAP-1658; ASM-2800) |

# 10. Release slicing proposal

The service is created in wave 1 with Epic 1 (release 30 November 2026 (tentative)) and then serves Epic 2, Epic 6 and Epic 8 from its existing read model. Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library and the decision-record library, the Temporal workflow kit, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 1 — Epic 1, release 30 November 2026 (tentative)

| Slice | Capabilities | Why now |
|---|---|---|
| 1.1 Measure catalog and definition version | CAP-P9-001 | Nothing can be published until a measure is defined, approved and versioned; the catalog is also the gate for the extract configuration |
| 1.2 Baseline | CAP-P9-002 | The baseline is taken once and frozen, and every later epic is measured against it (RWB-E1-013) |
| 1.3 Refresh, run and rerun | CAP-P9-003, CAP-P9-010 | A dated run with a rerun and a backfill is the difference between a number and an overnight side effect |
| 1.4 Freshness and the publication gate | CAP-P9-004, CAP-P9-005 | A stale or short number reaching the steering committee is the failure this service exists to prevent |
| 1.5 Queue and ageing measures | CAP-P9-006 | The team manager's daily question is answered from the same list the teams work |

Rationale: the wave-1 slice is the smallest set that makes the Epic 1 baseline defensible: a definition, a frozen baseline, a dated run, a freshness stamp and a gate. The dashboard, the agent measures, the operations reporting and the break view need the Epic 2 case facts and follow in wave 2 (GAP-1644; ASM-2787).

## 10.3 Wave 2 — Epic 2, release 31 December 2026 (tentative)

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Steering dashboard data set | CAP-P9-007 | The steering committee reads the same numbers the teams work with (RWB-E2-009) |
| 2.2 Agent acceptance and override | CAP-P9-008 | An agent at L1 is judged on evidence from the day the case facts are reported (GAP-1663) |
| 2.3 Operations reporting from the decision record | CAP-P9-009 | Reporting and audit read one record, and the retired copy leaves this as the only path (GAP-1650) |
| 2.4 Break view and closure | CAP-P9-011 | The steward works the break that holds the publication, with an owner and a date |

Rationale: Epic 2 puts one owner and a timer on every case and adds the steering dashboard; these four slices are what that release needs from this service, and each is demonstrable on its own.

## 10.4 Wave 4 — Epic 6 and Epic 8, releases 30 April 2027 (tentative) and 30 June 2027 (tentative)

| Slice | Capabilities | Why now |
|---|---|---|
| 4.1 Benefit realisation | CAP-P9-013 | Benefit realisation is an Epic 6 requirement (BR-061) and reads the baseline taken in wave 1 |
| 4.2 Regulatory returns and their delivery | CAP-P9-012 | The returns are an Epic 8 requirement and a delivered file (BR-082) |
| 4.3 Classification, staging and re-ageing | CAP-P9-014 | The segment is recomputed when the rules change (BR-083) |

Rationale: these three slices are business-epic work that lands after the case, treatment and write-off facts exist to report on. The service is already built, so each slice is a new report over the same read model.

## 10.5 Later increments

| Increment | What unlocks it |
|---|---|
| Agent measures on a fixed source | The event source of the agent measures agreed; today the catalogue does not carry it (GAP-1663; ASM-2801) |
| Benefit realisation against targets | The benefit model measures, baselines and targets set (BRD Epics 3 to 8 Q-020; GAP-1656; ASM-2798) |
| Regulatory extract from a stated source | The question of where the return reads from answered; BRD Epics 3 to 8 Q-018 (GAP-1657; ASM-2799) |
| Retention and disposal in force | The retention class and period per entity set (DL26; GAP-1655; ASM-2797) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-P9-001 | FR-P9-001, FR-P9-003 | a definition file of 6 rows for "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE", each naming its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20 | it is loaded with valid from 2026-11-21 | definition version "MD-2026.11" is in force with 6 measures, and each measure returns its data product and formula through the measure catalog | AC-P9-001-01 |
| AC-P9-002 | FR-P9-002 | a definition file whose row "TIME_IN_STAGE" has no formula | it is loaded | the load is refused whole with MSG-GEN-001 naming "formula", and no definition version is put in force | AC-EXC-P9-001-01 |
| AC-P9-003 | FR-P9-004, FR-P9-006 | the ACE batches of business date 2026-11-27 are COMPLETED in the batch-status view | the reporting extract runs at 01:30 on 2026-11-28 | the snapshot holds rows for 2026-11-27 marked baseline and frozen with definition version "MD-2026.11"; "CASES_BY_ROUTE" totals 120 cases, of which 60 are Mortgage; "REALIZED_RECOVERY" equals 4,350,000.00 THB from the synthetic payments since entry | AC-ALT-P9-001-01 |
| AC-P9-004 | FR-P9-005, NFR-P9-006 | the ACE batch for business date 2026-11-27 is not COMPLETED | the reporting extract runs at 01:30 on 2026-11-28 | no baseline rows are written for 2026-11-27; the run record shows MSG-P1-001 naming "DP03 Case" and 2026-11-26; the baseline is published by the first run after the batch of 2026-11-27 completes | AC-EXC-P9-001-02 |
| AC-P9-005 | FR-P9-008, FR-P9-032 | the extract configuration lists measure "COST_PER_CASE" with no definition in force | the extract runs | no value for "COST_PER_CASE" is written, and the run record shows MSG-P9-003 naming "COST_PER_CASE" | AC-EXC-P9-001-04 |
| AC-P9-006 | FR-P9-009, FR-P9-012 | the snapshot is taken at 2026-12-02 06:52 and queue "TDR-BKK-CO" holds 296 open cases with none unassigned and an average age of 41 days | the queue measures are read | the depth of each queue equals the case list count for that queue at 06:52, and "TDR-BKK-CO" shows depth 296, unassigned 0 and average age 41 days | AC-ALT-P9-002-01 |
| AC-P9-007 | FR-P9-010, FR-P9-027 | the snapshot depth for "DIL-BKK-CO" is 88 and the case list count at the same time is 87 | the snapshot is checked | it is not published, and the data steward receives MSG-P3-029 with check "queue depth against case list"; the break is open with an owner and a date | AC-ALT-P9-002-02 |
| AC-P9-008 | FR-P9-007, FR-P9-019 | the ACE batches of business date 2026-12-15 are COMPLETED | the reporting extract runs at 01:30 on 2026-12-16 | the measure read for 2026-12-15 returns a value for each of the 7 measures with period "2026-12-15", and the extract for 2026-12-15 carries freshness stamp 2026-12-15 for the 07:30 refresh | AC-P9-003-01, AC-P9-008-01 |
| AC-P9-009 | FR-P9-012, NFR-P9-007 | the case list shows 240 open cases at the 2026-12-15 cut-off and 1,412 decision records were decided that day | the extract runs on 2026-12-16 | the sum of "CASES_BY_STAGE" for 2026-12-15 is 240 and "DECISIONS_LOGGED" for 2026-12-15 is 1,412 | AC-ALT-P9-003-01, AC-ALT-P9-008-01 |
| AC-P9-010 | FR-P9-013, NFR-P9-008 | agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason | the extract runs on 2026-12-16 | "AGENT_ACCEPTANCE" for that agent and version is 85.0 percent and "AGENT_OVERRIDE" is 15.0 percent, and the dashboard shows both rates by agent | AC-ALT-P9-003-02, AC-ALT-P9-008-02 |
| AC-P9-011 | FR-P9-011, NFR-P9-006 | the case list shows 240 open cases at the 2026-12-15 cut-off and the case facts counted for the dashboard total 239 | the extract runs on 2026-12-16 | no snapshot rows and no extract are published for 2026-12-15; the dashboard shows 2026-12-14 as the latest published day with MSG-P9-002 naming 239, 240 and 2026-12-15; an alert reaches the Reporting and BI analyst and the data steward | AC-EXC-P9-003-01, AC-EXC-P9-008-01 |
| AC-P9-012 | FR-P9-014 | agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15 | the extract runs on 2026-12-16 | no "AGENT_ACCEPTANCE" value is written for it on 2026-12-15, and the dashboard shows "No runs" | AC-EXC-P9-003-02, AC-EXC-P9-008-02 |
| AC-P9-013 | FR-P9-017 | the extract for 2026-11-30 is running | the platform administrator posts a rerun of the same report for the same date | the rerun is refused with status 409 and MSG-P2-006, and one run continues | AC-ALT-P9-004-02 |
| AC-P9-014 | FR-P9-018 | the extract for 2026-11-30 completed with 380 rows | it is rerun for the same date | the rows for 2026-11-30 remain one set with one value per measure, and no duplicate row exists | AC-EXC-P9-004-02 (carried; the partition and cumulative-count wording is replaced by the snapshot rows) |
| AC-P9-015 | FR-P9-020, FR-P9-021 | the delivery target for the extract does not answer | the extract runs | the snapshot rows for the business date are written; the extract is held and an alert reaches the operations channel with MSG-GEN-006 naming the target; the extract is sent by the next run | AC-EXC-P9-001-03 (carried; the lake is replaced by the delivery target) |
| AC-P9-016 | FR-P9-022 | the delivery stops after 379 of 380 rows | the reconciliation step compares the delivered extract with the projection | the extract is not marked delivered; the run shows check "REC-08" failed with MSG-P1-019, and the watermark stays where it was | AC-EXC-P9-004-01 (carried; the lake copy becomes the delivered extract) |
| AC-P9-017 | FR-P9-027, FR-P9-012 | the accounts at 90 or more days past due less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, and the case list rows match per product with equal balance sums | the reconciliation step runs and the report is read | six reconciliation result rows are written, REC-01 and REC-02 for each product, each with variance zero and PASS; the case list for 2026-11-30 is released; the report shows all three products green | AC-P9-005-01, AC-P9-009-01 |
| AC-P9-018 | FR-P9-027, FR-P9-011 | the source count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 or more days past due, a variance of 12 accounts and 0.41 percent | the reconciliation step runs | the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41; 12 break rows carry check code "REC-01" and the account numbers; the publish for 2026-11-30 is held; the data steward, platform administrator and team manager groups receive MSG-P1-012; the report shows SSME red and the other two green | AC-ALT-P9-005-01, AC-ALT-P9-009-01 |
| AC-P9-019 | FR-P9-005, FR-P9-011 | the ACE batch for source ALS for 2026-11-30 is LATE and not COMPLETED | the reconciliation step is reached | no reconciliation result for 2026-11-30 is written; the publish for 2026-11-30 is held; the report shows every product as not run with the reason "DP01 is from 2026-11-27" | AC-EXC-P9-005-01, AC-EXC-P9-009-01 |
| AC-P9-020 | FR-P9-028, NFR-P9-011 | a user whose role holds no right in the capability area, and a role with no unmasked masking row | each reads the dashboard and a report row carrying a customer identifier | the first is refused with MSG-P4-002 and nothing changes; the second receives the identifier masked; no response field holds it in clear | AC-EXC-P9-003-03, AC-EXC-P9-001-05 |
| AC-P9-021 | FR-P9-029, NFR-P9-012 | the access log rejects every write and a role reads a report row carrying a personal field | the read is attempted | the read is refused with the standard system message for the access log and no personal field is returned | NFR-042; REQ-ACA-006 (new, D-RCV-60) |
| AC-P9-022 | FR-P9-016, FR-P9-031 | a business date for which the extract ran is held, and the decision record cannot be written | a rerun is requested | the rerun for the held date is accepted and the publication completes only when the decision record is written; with the record unwritable nothing is published and MSG-P7-003 is raised with an incident | AC-EXC-P9-003-04, AC-EXC-P9-001-06 |
| AC-P9-023 | FR-P9-024 | the baseline of 2026-11-27 is frozen and six monthly dates have published measures | Finance reads the benefit view | each measure is shown against its baseline with the definition version used, and where the benefit model sets no measure or no target the view says so and no value is computed | BR-061; BRD Epics 3 to 8 Q-020 (new, D-RCV-60) |
| AC-P9-024 | FR-P9-025, FR-P9-026 | the data products of the return period are complete and the classification rule version changes from 2027-05-01 | the return runs and the rule version takes effect | the return carries one row per return item with the definition and rule versions applied, and the segment is recomputed from 2027-05-01 without a code release | BR-082, BR-083; RWB-E8-001, RWB-E8-002 (new, D-RCV-60) |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| RWB-E1-013 | CAP-P9-001, CAP-P9-002, CAP-P9-003, CAP-P9-004, CAP-P9-005, CAP-P9-010 | FR-P9-001 to FR-P9-008, FR-P9-016 to FR-P9-019, FR-P9-023, FR-P9-030 to FR-P9-032 | NFR-P9-001, NFR-P9-002, NFR-P9-005, NFR-P9-006, NFR-P9-009, NFR-P9-010 | AC-P9-001 to AC-P9-005, AC-P9-008, AC-P9-013, AC-P9-014, AC-P9-022 |
| RWB-E2-009 | CAP-P9-007, CAP-P9-008, CAP-P9-009, CAP-P9-011 | FR-P9-011 to FR-P9-015, FR-P9-027, FR-P9-028, FR-P9-029 | NFR-P9-007, NFR-P9-008, NFR-P9-011, NFR-P9-012 | AC-P9-010 to AC-P9-012, AC-P9-020, AC-P9-021 |
| REQ-WKM-009 | CAP-P9-003, CAP-P9-007 | FR-P9-007, FR-P9-012 | NFR-P9-001 | AC-P9-008, AC-P9-009 |
| REQ-WKM-006 | CAP-P9-005, CAP-P9-006, CAP-P9-011 | FR-P9-009, FR-P9-010, FR-P9-011, FR-P9-027 | NFR-P9-006 | AC-P9-006, AC-P9-007, AC-P9-017, AC-P9-018 |
| REQ-CWC-015 | CAP-P9-006 | FR-P9-009 | NFR-P9-002 | AC-P9-006 |
| BR-061 | CAP-P9-013 | FR-P9-024 | NFR-P9-009, NFR-P9-024 | AC-P9-023 |
| BR-082 | CAP-P9-012 | FR-P9-020, FR-P9-021, FR-P9-022, FR-P9-025 | NFR-P9-017, NFR-P9-024 | AC-P9-015, AC-P9-016, AC-P9-024 |
| BR-083 | CAP-P9-014 | FR-P9-026 | NFR-P9-009 | AC-P9-024 |
| REQ-DRI-009 | Not carried as a requirement: retired with the data lake | None | None | None |
| RWB-E1-014 | Not carried: retired by D-RCV-60 | None | None | None |
| RWB-E1-011 | Supporting key: the reconciliation is P1's, the report surface is here | FR-P9-027 | NFR-P9-006 | AC-P9-017, AC-P9-018, AC-P9-019 |
| RWB-E1-030 | Supporting key: the queue measures are P3's, the publication is here | FR-P9-009, FR-P9-010 | NFR-P9-002 | AC-P9-006, AC-P9-007 |

BR coverage: 5 of the 5 live P9 requirement keys (RWB-E1-013, RWB-E2-009, BR-061, BR-082, BR-083) are covered by at least one functional requirement. The 3 supporting program keys (REQ-WKM-009, REQ-WKM-006, REQ-CWC-015) are covered as reads and publications. RWB-E1-014 and REQ-DRI-009 have no functional requirement by design: the data lake is removed and the copy is retired (GAP-1650). RWB-E1-011 and RWB-E1-030 have no functional requirement of their own because the reconciliation belongs to P1 and the queue measure to P3; this service reads them and publishes them.

No BR is left without a requirement. The program BRD carries no requirement section for P9 at all, so the coverage above is against the keys that name reporting duties in sections 5.3, 5.6 and 5.7 and in the three business-epic BRDs (GAP-1644).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Definition load and refusal output with MSG-GEN-001, and the measure catalog read | FR-P9-001, FR-P9-002, FR-P9-003, FR-P9-008 | Reporting and BI analyst |
| Baseline run on a completed batch, with the frozen flag and the definition version | FR-P9-004, FR-P9-006, NFR-P9-009 | Reporting and BI analyst with the QA team |
| Holder drill: a stale product, a short queue and a short dashboard total | FR-P9-005, FR-P9-010, FR-P9-011, NFR-P9-006 | Data steward with the QA team |
| Queue measure reconciliation to the case list, and the break closure | FR-P9-009, FR-P9-027 | Team manager with the data steward |
| Dashboard and agent measure read, including "No runs" | FR-P9-012, FR-P9-013, FR-P9-014, NFR-P9-007, NFR-P9-008 | Reporting and BI analyst |
| Run, rerun, backfill and the 409 refusal | FR-P9-016, FR-P9-017, FR-P9-018, FR-P9-019 | Platform administrator |
| Extract delivery, held delivery and the REC-08 mismatch | FR-P9-020, FR-P9-021, FR-P9-022, NFR-P9-017 | Platform administrator with the QA team |
| Masking matrix, access log reconciliation and a refused read | FR-P9-028, FR-P9-029, NFR-P9-011, NFR-P9-012 | Compliance and PDPA officer |
| Benefit realisation and the return against the frozen baseline | FR-P9-024, FR-P9-025, FR-P9-026 | Finance and CFO delegate with the Compliance and PDPA officer |
| Performance and volume test at the stated case population | NFR-P9-001, NFR-P9-005 | QA team |

# 12. Open questions

FSD P9 carries no open question section of its own, so nothing is carried from it by ID. The questions below are the BRD questions that touch this service, carried with their IDs, and the product-level questions this PRD raises. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-P9-01 | Where do the regulatory extracts read from now that the data lake is removed: the read model, the data products, or the decision record? | Solution architect | Before wave 4 | CAP-P9-012, FR-P9-025 | BRD Epics 3 to 8 Q-018; GAP-1657; ASM-2799 |
| OQ-P9-02 | What benefit model measures, baselines and targets does benefit realisation report against? | Finance and CFO delegate | Before wave 4 | CAP-P9-013, FR-P9-024 | BRD Epics 3 to 8 Q-020; GAP-1656; ASM-2798 |
| OQ-P9-03 | Which seventh measure makes up the set that the dashboard refresh returns, and is it "DECISIONS_LOGGED" or "CASES_BY_STAGE" or both? The definition set names six and the refresh check counts seven. | Tribe lead with the Reporting and BI analyst | Before wave 2 | CAP-P9-007, FR-P9-012 | AC-P9-001-01, AC-P9-003-01; GAP-1649; ASM-2791 |
| OQ-P9-04 | Which identifier does `GET /reports/{id}` and `POST /reports/{id}/run` take, and does the measure read keep the path `GET /reports/measures`? | Solution architect with the API owner | Before wave 1 contract | CAP-P9-010, FR-P9-016 | Arch v5 slide 15 and slide 41; Ownership Map; GAP-1648; ASM-2790 |
| OQ-P9-05 | Is the measure run a Temporal Schedule at 01:30, or a call from the bank scheduler, or both with the schedule as the fallback? | Solution architect with the bank platform team | Before wave 1 system test | CAP-P9-003, FR-P9-019 | Arch v5 slide 15 and slide 44; GAP-1647; ASM-2789 |
| OQ-P9-06 | Who owns the data quality break record that the break view reads, and where is a closure written now that P1 holds the reconciliation result? | Data steward and data product owner with P1 | Before wave 2 | CAP-P9-011, FR-P9-027 | GAP-1651; ASM-2793 |
| OQ-P9-07 | Does the queue measure stay computed in P3 and only published here, or does this service compute the measure from the case list? Two capabilities with one name is a defect by design. | Solution architect with P3 | Before wave 1 system test | CAP-P9-006, FR-P9-009 | GAP-1652; ASM-2794 |
| OQ-P9-08 | Which service applies the classification, staging and re-ageing rules, given that Architecture v5 lists only measures, snapshots, the dashboard and regulatory reports for rwb-reporting? | Solution architect | Before wave 4 | CAP-P9-014, FR-P9-026 | Arch v5 slide 41; GAP-1653; ASM-2795 |
| OQ-P9-09 | What is the source of the agent acceptance and override measures, given that the event catalogue does not list this service as a consumer of AgentRunCompleted? | Solution architect with the AI product owner | Before wave 2 | CAP-P9-008, FR-P9-013 | Arch v5 slides 42 and 43 and the consumer matrix; GAP-1663; ASM-2801 |
| OQ-P9-10 | Is SCR-37 served by this service, or composed by the edge from the case and queue views? | Solution architect | Before wave 2 | CAP-P9-007, FR-P9-028 | GAP-1658; ASM-2800 |
| OQ-P9-11 | Do the message IDs of this service keep the module prefixes of the messages they reuse (MSG-P1-001, MSG-P1-012, MSG-P3-029, MSG-P2-006), or are new IDs issued? | Business analyst, P9 | Before wave 1 release | All messages | GAP-1660; ASM-2802 |
| OQ-P9-12 | What are the field lists of the snapshot, the publication, the report definition, the extract run and the projections? Only the measure definition has a field catalog today. | Data architect | Before wave 1 system test | CAP-P9-002, CAP-P9-004 | GAP-1654; ASM-2796 |
| OQ-P9-13 | Which retention class and period apply to a snapshot, a published extract, a run record and a report read, under DL26? | Compliance and PDPA officer | Before wave 1 release | CAP-P9-003, NFR-P9-021 | DL26; GAP-1655; ASM-2797 |
| OQ-P9-14 | What are the Thai names for the measure labels, the unit names and the messages, under DL10? | Business lead with Legal and Compliance | Before wave 1 release | CAP-P9-007, NFR-P9-018 | DL10; NFR-059 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1661; ASM-2785).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 2 (business outcomes), 5.3 and 5.6 and 5.7 (the reporting duties and the owner of the queue, case and decision facts), 6.1 to 6.12 (NFR-001 to NFR-078), 8 (release plan), 9 (open decisions), 10 (delivery model, service epics and waves), 11 (requirement trace), 12 (gaps and assumptions) |
| Recovery Workbench Business Requirements Epic 1 v5 | 3.8 (RWB-E1-013), 4 (program requirements met, REQ-CWC-015 and REQ-DRI-009), 7 (open decisions), 8 (delivery model and requirement trace) |
| Recovery Workbench Business Requirements Epic 2 v3 | 3.9 (RWB-E2-009), 4 (REQ-WKM-006 and REQ-WKM-009), 8 (delivery model), 9 (requirement to service epic traceability) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 4 (objectives and outcomes), 8.4 and 8.6 (BR-061, BR-082, BR-083), 10 (success measures), 11 (dependencies, DEP-010), 12 (open questions Q-018 and Q-020) |
| Recovery Workbench FSD P9 Reporting v3 | Document control, existing capability check, A1 (context and scope), A2.1 to A2.10 (functional decomposition, field catalogs, rules, acceptance criteria), Requirements served, Screens (SCR-37) |
| Recovery Workbench Architecture v5 | Slides 13 (call-type matrix), 15 (rwb-reporting contract), 31 and 32 (the bank scheduler and the report extract), 37 (no data lake), 41 (service catalogue), 42 and 43 (event catalogue), 44 (job map, JOB-15), 45 (architect questions), 47 (protecting ACE) |
| Recovery Workbench Temporal and Drools Design v1 | Task queue and workflow kit, the schedule as the event-started work |
| Recovery Workbench Microservice Ownership Map v1 | Services, tables (`measure_definition`, `measure_snapshot`, `measure_publish`), operations (`GET /reports/measures`), job JOB-15, and the rulings on JOB-15 and the reporting extract |
| Recovery Workbench Non Functional Specification v3 | 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R4 (services and naming), R5 (target structure), R8 (outputs), R9 (gaps and assumptions) |
