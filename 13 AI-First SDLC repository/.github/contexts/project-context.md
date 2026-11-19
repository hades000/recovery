# Recovery Workbench — project context

**Purpose:** canonical business context for every SDLC agent: what the Workbench is, who uses it,
what it must do, the rules it follows, the data it holds and the constraints it works under.
**Scope:** the eight epics from November 2026 to June 2027, with Epic 1 in delivery detail.
**Status:** created from the approved document set on 2026-11-04. Gaps and open decisions are listed
in section 16 and in `requirement/Intake_Gap_Report_RecoveryWorkbench.md`.
**Source register:** section 17. Every statement below cites the document it came from.

> **Evidence rule.** `DOCUMENTED/REQUIRED` means the statement is in an approved project document.
> `ASSUMED` means the build uses the position until the bank decides, and the decision log entry is
> named. `GAP` means no source establishes the fact. No statement is inferred from a template.

## 1. Business overview

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-BUSINESS-001 | The Recovery Workbench owns every recovery case from 90 days past due to close for Mortgage, Hire Purchase and SSME. It is the recovery module of ACE, the bank's collection engine, so collection and recovery work in one application with one case view. | Project Overview §1; Target Architecture §1; ADR-001 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-002 | Collections and recovery staff use 42 applications; case facts are spread across the core bank, EFS, LIT, CCMS, SVAF, AMIS and document stores; teams run cases from Excel and SharePoint; decisions are not recorded in one place; turnaround is 21 days for litigation, 23 days for a restructure and 26 days for a deed in lieu. | Project Overview §2 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-003 | The Workbench replaces team spreadsheets with one case list reconciled to the core bank, gives every case one owner by rule, records every decision once, and makes rules, limits and routes versioned data. | Project Overview §3 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-004 | In scope: every recovery case from 90 days past due to close; decisions D6–D9 and their sub-decisions; D5 once the restructure programme is live; deviations X1–X7 after day 90; partners, documents, the decision log and the interaction ledger; the recovery module of ACE with data through COLLINS and file loads. | Business Requirements Program §1.1 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-005 | Out of scope: collections before day 90 and decisions D1–D4 (EFS and the ACE collection module); dialer and messaging channels; core bank booking logic (ALS); COLLINS model development; restructure affordability and plan calculation (ACE restructure calculator); partner systems; changes to bank policy. | Business Requirements Program §1.2 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-006 | Eight epics, one production release at each month end from November 2026 to June 2027. What slips moves to the next epic; the release date does not move. E1 and E2 are confirmed; E3–E8 are proposed and confirmed one month ahead. | Project Overview §7; Release Plan v3 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-007 | The 2027 benefit targets are: recovery rate on NPL 73% (66.3% today); litigation turnaround 6 days (21); deed in lieu 12 days (26); restructure 5 days (23); debt sale 45 days (no baseline); 80% of selected manual processes removed; audit findings and fraud cases 13 (50); NPA sales cycle 1,095 days (1,486). | Project Overview §8; Business Requirements Program §2 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-008 | The case passes through six stages: receive the case, choose the route, resolve with the customer, enforce, realise the asset, close. It can return to the route decision at any stage on a cure, a payment, a deviation or an override. | Project Overview §4; Business Architecture slide 3 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-009 | The Workbench runs 19 L1 processes, 84 L2 sub-processes and 247 L3 processes. Processes 01–05 run in collections before day 90; the Workbench runs 06–19. | Business Requirements Program §4 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-010 | Every decision follows five steps: gather and check the information, decide by a rule, a model or an agent, make the outcome final or send it to the approver, act in the systems, and log the decision once. Who approves is set by the bank approval authority regulation and the delegation of authority table. | Project Overview §5; Business Architecture slide 7 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-011 | The nine decisions are D1 act on the signal, D2 reach the customer, D3 promise kept, D4 escalate (all on EFS), D5 offer a restructure (EFS and ACE), D6 which route, D7 litigate and enforce, D8 dispose assets and sell debt, D9 write off and recover after charge-off (all in the Workbench). | Business Architecture slide 7 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-012 | Deviations X1–X7 pause the normal route: X1 complaint or dispute, X2 hardship or vulnerability, X3 deceased customer, X4 fraud, X5 bankruptcy or external seizure, X6 lost contact, X7 legal hold or other. A deviation stops contact or enforcement as its rule requires and returns the case when it clears. | Project Overview §4; Business Glossary; Deviation and Exception Catalog v3 | DOCUMENTED/REQUIRED |

## 2. Actors, roles and stakeholders

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-STAKEHOLDER-001 | 54 roles: 37 bank users, 7 partner users, 4 customer parties and 6 non-human actors. Every role is held as data in the roles table, with a role code, permission letters, default scope and first release with real users. | Users, Roles and Permissions v3, Roles sheet | DOCUMENTED/REQUIRED |
| CTX-STAKEHOLDER-002 | The 37 bank roles cover product heads; shared operations (case owner, team manager, phone and field collector, restructuring officer, hardship specialist, complaint officer, litigation officer, enforcement owner, sale officer, NPA and asset manager, debt sale officer, write-off team member, Credit Administration officer, guarantee officer, partner and agency manager, capacity planner, heads of Litigation/NPA/Asset Liquidity); centre of excellence; platform; and control functions and committees. | Users, Roles and Permissions v3; Target Operating Model slide 7 | DOCUMENTED/REQUIRED |
| CTX-STAKEHOLDER-003 | The 7 partner roles are collection agency, law firm, valuer, auction vendor, debt buyer/AMC, RAMC and Legal Execution Department/court officer. The LED has no Workbench login; it is reached by filing and result interfaces. | Users, Roles and Permissions v3 | DOCUMENTED/REQUIRED |
| CTX-STAKEHOLDER-004 | The 4 customer parties are borrower, guarantor/co-borrower, heir/estate representative and retail asset bidder. Customers use existing bank channels (SCB Easy, LINE OA, SMS, branches, HOME.SCB), not a Workbench login. | Users, Roles and Permissions v3; Target Architecture §3 | DOCUMENTED/REQUIRED |
| CTX-STAKEHOLDER-005 | The 6 non-human actors are SY-CASEWF (case workflow), SY-RULES (Drools rule evaluator), SY-DATALOAD (COLLINS and file loads), SY-OCR (OCR and extraction), SY-DECLOG (decision log writer) and SY-AGENT (agent platform). Each runs under its own service identity. | Users, Roles and Permissions v3 | DOCUMENTED/REQUIRED |
| CTX-STAKEHOLDER-006 | The operating model has four groups: product heads (own product outcomes and approve above limits), shared operations (carry out the work), centre of excellence (strategy, rules, analytics, QA) and platform (EFS, ACE, COLLINS, agents, data). Control functions and committees approve within the delegation. | Target Operating Model slide 2; Business Requirements Program §3 | DOCUMENTED/REQUIRED |
| CTX-STAKEHOLDER-007 | 1,234 named users: 466 recovery staff, 448 collections staff reading the case record and 320 partner users. About 410 online in the busiest hour (about 370 bank and 50 partner). | Non-Functional Specification §2 | DOCUMENTED/REQUIRED |

## 3. Process, case and rules model

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-BUSINESS-013 | A case is modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and case file item. The collection module uses the same terms. | Engineering Practices §3; AI Assisted Development Approach §3.1; ADR-011 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-014 | The case state model covers stage, status within stage, route and the deviation flags X1–X7. A case holds exactly one state at a time. Case status values are New, Assigned, In progress, Waiting customer, Waiting partner, Waiting approval, On hold and Closed. | Business Requirements Program REQ-CWC-005; Business Glossary | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-015 | Every account at 90 or more days past due that is not excluded carries one recovery case, created by rule from the daily feed. Exclusions are deceased, fraud, bankruptcy, an active restructure plan and an open dispute, held as data and applied at creation. | REQ-CWC-001, REQ-CWC-004 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-016 | One case covers one customer and one product, with its accounts linked. A case ID is issued in the form RW-YYYY-NNNNNN, once, never reused, and printed on every letter and document. | REQ-CWC-002, REQ-CWC-003 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-017 | Every new case is placed in a queue and assigned to a person by rule. Allocation reads product, region, exposure band, stage, route, deviation flag, customer segment and collateral type, applies first match and always has a default row. Assignment supports round robin, lowest load and named owner for continuity, with a capacity cap and an overflow queue. | REQ-CWC-007 to REQ-CWC-009 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-018 | Cases move between queues and roles by transfer rules on stage change, route decision, timer expiry, deviation raised or cleared, approval needed, document received, payment missed, and manual request with a reason code. | REQ-CWC-010 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-019 | Service levels per queue and status, warning thresholds and escalation targets are held as data. A breach raises an event without moving the case. Prescription dates are set from the legal periods table at case creation and are visible at all times. | REQ-CWC-011, REQ-CWC-012 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-020 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call. Rule loads are validated for schema, overlapping rows, unreachable rows, a missing default and a set of test cases before they take effect. | REQ-CWC-013, REQ-CWC-014 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-021 | The routing logic contains 448 rules in ten route sets. Each rule has a rule ID, route set, decision, from state, event, condition, action, to state, owner, systems and timer. Hit policy is Unique: in a route set, for one state and one event, one condition holds. | Business Rules and Routing Logic v4, Rules sheet | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-022 | 252 of the 448 rules carry a timer; 366 of the 448 move the case to a state owned by a person or partner. | Business Rules and Routing Logic v4, summary | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-023 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it. | REQ-CWC-016 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-024 | A queue accepts a write from an analytical model or an agent, carrying the case, score, priority and reason. The model or agent passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version. | REQ-CWC-017, REQ-CWC-018 | DOCUMENTED/REQUIRED |
| CTX-BUSINESS-025 | Every open case carries one next action: what has to happen, who owns it and the date it is due. It is produced from the rule that moved the case, not entered by hand, and a case with no next action is reported as an exception. | REQ-WKM-012 to REQ-WKM-016 | DOCUMENTED/REQUIRED |

## 4. Functional scope by module

The platform modules P1–P10 and stage modules S1–S9 are the product structure. The requirements
below are representative; the full set is in `docs/brds/business-requirements-program.md` and the
Epic 1 detail in `docs/brds/business-requirements-epic-1.md`.

| ID | Module | What it must do | Key source IDs | First epic |
|---|---|---|---|---|
| CTX-FEATURE-001 | P1 Recovery data engine | Hold 14 data products, load ALS/EFS/CCMS/SVAF and file loads daily, reconcile the case list to ALS, run data quality rules, stamp freshness, control access, publish the baseline measures, keep the interaction ledger. | REQ-RDF-001 to REQ-RDF-014; RWB-E1-001 to RWB-E1-017, RWB-E1-064 to RWB-E1-068 | E1 |
| CTX-FEATURE-002 | P2 Integration | One adapter pattern for file loads and outbound files, with checks, logging, retry and an exception queue; no direct system-of-record call; legacy feed jobs on ADF and Control-M; run books and monitoring. | REQ-DRI-006 to REQ-DRI-013; RWB-E1-007, RWB-E1-051, RWB-E1-056 | E1 |
| CTX-FEATURE-003 | P3 Case and workflow | Case creation, case ID, state model, queues, allocation, assignment, transfer, service levels, timers, prescription dates, rule load and rollback, rebalancing, case list and case record view. | REQ-CWC-001 to REQ-CWC-020; RWB-E1-018 to RWB-E1-031, RWB-E1-042 to RWB-E1-045 | E1 core, E2 screens |
| CTX-FEATURE-004 | P4 Access and administration | Entra ID SSO and MFA, roles and scopes, role-to-permission matrix as data, PDPA masking by role, delegation of authority, access log, break-glass admin, full administration. | REQ-ACA-*; RWB-E1-022, RWB-E1-037 to RWB-E1-039 | E1; E2 partners; E8 full |
| CTX-FEATURE-005 | P5 Document hub | Store documents against the case, index by type/date/source/fields, write-once container for legal types, OCR, classification, field extraction, review queue, custody, retention, virus scan, intake from branches/mailroom/SFTP/email. | REQ-DOC-*; RWB-E1-024 to RWB-E1-026, RWB-E1-032, RWB-E1-033, RWB-E1-040, RWB-E1-041, RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-054, RWB-E1-057 | E1 store and OCR; E2 generation |
| CTX-FEATURE-006 | P6 Communications | Letter and notice templates as versioned data with Legal approval, merge fields, notice generation, dispatch through WIN, proof-of-delivery capture. | REQ-COM-*; RWB-E1-034, RWB-E1-046, RWB-E1-052, RWB-E1-055 | E1 notices; E2 dispatch; E4 self-service |
| CTX-FEATURE-007 | P7 Decision centre and log | Append-only hash-chained decision log, decision log writer, approval routing, decision centre, decision log query and export, approval levels, separation of duty. | REQ-DEC-*; RWB-E1-008, RWB-E1-027 | E1 log; E2 routing; E3 centre |
| CTX-FEATURE-008 | P8 Payments and posting | Match receipts to cases and accounts, exception list, posting of approved bookings, confirmation from the next ALS load. | REQ-PAY-* | E2 matching; E4 full |
| CTX-FEATURE-009 | P9 Reporting | Baseline measures, case list in Power BI, queue measures, steering dashboard, regulatory extracts, benefit tracking. | REQ-RPT-*; RWB-E1-013 | E1 baseline; E2 dashboard |
| CTX-FEATURE-010 | P10 Agent runtime | Agent platform, orchestrator and tool gateway, autonomy L0–L4, shadow runs, evaluations, monitoring, fallback to rules, model endpoint. | REQ-AGT-*; RWB-E1-058 to RWB-E1-063 | E1 shadow; E2 L1 |
| CTX-FEATURE-011 | S1 Valuation and route | Expected return by route, route recommendation with reasons, approval within the delegation, route decision screen. | REQ-ROU-* | E4 |
| CTX-FEATURE-012 | S2 TDR, settlement and deed in lieu | Treatment record, restructure offer, settlement range, deed in lieu readiness, appraisal order, transfer, booking, plan timers. | REQ-TRT-*; RWB-E2-* treatment stories | E2 foundations; E3 |
| CTX-FEATURE-013 | S3 Guarantees and guarantors | TCG and insurer claims, claim deadlines, guarantor pursuit, subrogation. | REQ-GUA-* | E4 |
| CTX-FEATURE-014 | S4 Litigation and enforcement | Notice approval, case pack, law-firm instruction, court dates, hearings, judgment, enforcement, LED auction, proof of delivery. | REQ-LIT-*; RWB-E2-* notice stories | E2 notices; E5 |
| CTX-FEATURE-015 | S5 Assets and auction | Asset take-on, holding cost, stock balance, valuation, floor price, listing on HOME.SCB, auction rounds, RAMC transfer. | REQ-AST-* | E3; E4 |
| CTX-FEATURE-016 | S6 Debt sale | Lot builder, reserve price, buyer qualification, data room, bids, award, data transfer, put-backs. | REQ-DSL-* | E5 data; E6 screens |
| CTX-FEATURE-017 | S7 Write-off and recovery | Monthly write-off scan, eligibility and tax criteria, committee pack, posting, provision release, recovery after charge-off. | REQ-WOF-* | E6 |
| CTX-FEATURE-018 | S8 Deviation handling | X1–X7 end to end: raise, screen, contact stop, route to handler, evidence, return to the same decision. | REQ-DEV-*; RWB-E1-062 | E2 screening; E7 |
| CTX-FEATURE-019 | S9 Partner management | Partner panel, contracts, fees, placement by scorecard, performance, conduct, suspension, field app. | REQ-PRT-* | E6 panel; E7 scoring |
| CTX-FEATURE-020 | Cross-cutting administration | Configuration service, parameter catalogue, reference data service, versioned tables, multi-product parameters, feature flags, migrations, rule change audit. | RWB-E1-042 to RWB-E1-048 | E1 |

## 5. Data requirements

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-DATA-001 | 14 data products, each with one named system of record, one way in and one freshness: DP01 account and arrears, DP02 customer and party, DP03 case and ownership, DP04 treatment and offers, DP05 contact and promises, DP06 collateral and assets, DP07 legal events and cases, DP08 partner performance, DP09 debt sale, DP10 documents and extracted fields, DP11 scores and route economics, DP12 decision log, DP13 money and closure, DP14 reference data. | Conceptual Data Model v5, Data products sheet | DOCUMENTED/REQUIRED |
| CTX-DATA-002 | 108 entities across 17 subject areas. Each entity has a subject area, data product, system of record, what it takes from ACE and a field count. | Conceptual Data Model v5, Entities sheet; Logical Data Model v6 | DOCUMENTED/REQUIRED |
| CTX-DATA-003 | The logical data model holds every field with name, type, length, mandatory, default, list of values, key and source system. The physical schema is PostgreSQL create statements with indexes, constraints and seed reference data. | Logical Data Model v6; Physical Schema v4 | DOCUMENTED/REQUIRED |
| CTX-DATA-004 | Every data product carries a freshness stamp (source extract time and load time). Every decision records the freshness of the data it used. | REQ-RDF-009; RWB-E1-015 | DOCUMENTED/REQUIRED |
| CTX-DATA-005 | Data quality rules run on every load; every failed row carries a reason code visible to the data product owner. The case list reconciles daily to the ALS count of accounts at 90+ days past due with no unexplained variance (DL25). | REQ-RDF-007, REQ-RDF-008; RWB-E1-006, RWB-E1-011 | DOCUMENTED/REQUIRED |
| CTX-DATA-006 | Retention and archive rules are held per data product and table, applied by a job that archives rows past their rule and logs the action. Every document type carries a retention class; legal documents are write-once. | REQ-RDF-013; NFR-028 to NFR-032; RWB-E1-017 | DOCUMENTED/REQUIRED |
| CTX-DATA-007 | Personal data is classified restricted, confidential or internal. National ID and passport numbers are tokenized at load; the clear value is not stored. Each role has a masking profile; every read of a personal field is logged through PII Kafka. | Personal Data Protection Design §1, §4, §5 | DOCUMENTED/REQUIRED |

## 6. Integration points

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-TECH-001 | Data from other systems arrives by the COLLINS daily batch or a file load. No component calls a system of record directly. Data leaves through paths ACE already has. | REQ-DRI-006, REQ-DRI-008; ADR-005; Target Architecture §2–3 | DOCUMENTED/REQUIRED |
| CTX-TECH-002 | COLLINS brings core bank (ALS), EFS, UDP, SCBPDM, AAL, LIT status and scores. File loads bring CCMS, SVAF, AMIS, RPS, WIN and GL. | Target Architecture §3; Data products sheet | DOCUMENTED/REQUIRED |
| CTX-TECH-003 | Outbound paths are core bank bookings by the officer, WIN files, NSS and LINE OA, the data lake for Power BI and COLLINS, partners and debt buyers. | Target Architecture §3 | DOCUMENTED/REQUIRED |
| CTX-TECH-004 | The integration adapters log every file in and out, retry on a defined schedule, and place anything that fails after the retry limit in an exception queue with a task for a named owner. | REQ-DRI-007; NFR-026 | DOCUMENTED/REQUIRED |
| CTX-TECH-005 | The API is REST/OpenAPI 3.1 and covers cases, timelines, accounts, parties, transfers, deviations, tasks, queues, timers, recommendations, approvals, decision log, treatments, route, guarantee claims, notices, legal actions, assets, listings, debt sale, write-offs, proceeds, documents, interactions, partners, administration and reports. | API Specification v2; Interface Specifications v2 | DOCUMENTED/REQUIRED |
| CTX-TECH-006 | Events are described in AsyncAPI 3.0. Outbound work uses an outbox with retry and idempotency; a duplicate delivery does not repeat the action. | Event and Messaging Design v2; TE-006 | DOCUMENTED/REQUIRED |
| CTX-TECH-007 | Same-day data needs are named under DL06 before any interface is built. The current position is end-of-day data, available in the Workbench the next morning. | REQ-DRI-008; NFR-015 | ASSUMED (DL06) |

## 7. Non-functional requirements

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-NFR-001 | Volume: about 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month. 28,119 active accounts at 90+ days past due. | NFR-001; Volume and Scale Forecast v2 | DOCUMENTED/REQUIRED |
| CTX-NFR-002 | Users: about 370 staff and 50 partner users online in the busiest hour; 1,234 named users; about 21 requests a second. | NFR-002, NFR-003; Non-Functional Specification §2 | DOCUMENTED/REQUIRED |
| CTX-NFR-003 | Response: screens under 2 seconds at the 95th percentile; case record with 50 documents under 2 seconds; rule evaluation under 300 ms; agent answer under 60 seconds, then the rule result is used; case search under 3 seconds; document search under 5 seconds. | NFR-008 to NFR-012 | DOCUMENTED/REQUIRED |
| CTX-NFR-004 | Loads: COLLINS load complete by 07:00; daily rebalancing by 07:00; case list reconciled daily; OCR 500 pages an hour; classification 90% correct. | NFR-013 to NFR-019 | DOCUMENTED/REQUIRED |
| CTX-NFR-005 | Availability: 99.9% in business hours; 99.5% outside business hours, excluding the change window. RPO and RTO are the ACE values; open under DL11. | NFR-020 to NFR-023 | DOCUMENTED/REQUIRED / OPEN |
| CTX-NFR-006 | Resilience: an agent or model outage falls back to the rule result; a system-of-record outage queues the outbound action and retries; after three retries the item goes to the exception queue; a release rolls back by redeploying the previous tag. | NFR-024 to NFR-027 | DOCUMENTED/REQUIRED |
| CTX-NFR-007 | Audit: every decision is reproducible from the log with rule, model, agent and prompt versions and inputs; every action carries the rule version and approver; the hash chain is checked daily and a break is reported to Compliance the same day. | NFR-033 to NFR-036 | DOCUMENTED/REQUIRED |
| CTX-NFR-008 | Retention: retention classes per document type; write-once for legal types; decision log and interaction ledger retention set by Compliance; legal hold overrides retention; disposal is recorded, never silent. | NFR-028 to NFR-032, NFR-072 to NFR-075 | DOCUMENTED/REQUIRED / OPEN (DL26) |
| CTX-NFR-009 | Accessibility: WCAG 2.2 AA; automated scan and keyboard checks on each screen; no level A or AA failure. | Accessibility Standard v2; Test Strategy §1 | DOCUMENTED/REQUIRED |
| CTX-NFR-010 | Scale: about 5.8 million documents and 2.8 TB by 2031; about 36 GB for the decision log and interaction ledger; a single case history query under 2 seconds at that size. | NFR-007, NFR-069, NFR-070 | DOCUMENTED/REQUIRED |

## 8. Compliance, controls and policy

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-COMPLIANCE-001 | Thai PDPA B.E. 2562 applies. Lawful bases are proposed: contract for debt recovery; legal obligation for statutory notices, regulatory reporting and court filings; legal claims/explicit consent for sensitive flags; consent for optional channels; legitimate interest for fraud prevention; employment/contract for staff and partner data. Compliance confirms the bases under DL26. | Personal Data Protection Design §2 | DOCUMENTED/REQUIRED |
| CTX-COMPLIANCE-002 | 42 controls cover the recovery process: what each checks, who performs it, the evidence it produces and how it is tested. Each answers an audit finding or a regulatory obligation. | Controls Catalog v2 | DOCUMENTED/REQUIRED |
| CTX-COMPLIANCE-003 | The regulatory requirements map links each obligation to the process step, rule and control. Key obligations include BOT debt collection conduct, PDPA, litigation procedure, TCG claims, asset disposal, debt sale and write-off. | Regulatory Requirements Map v2; Controls Catalog v2 | DOCUMENTED/REQUIRED |
| CTX-COMPLIANCE-004 | The audit findings response map links each open audit finding to the change that closes it. The programme targets a reduction from 50 audit findings and fraud cases to 13 by 2027. | Audit Findings Response Map v2; Project Overview §8 | DOCUMENTED/REQUIRED |
| CTX-COMPLIANCE-005 | Records retention and archiving sets how long each record and document is held, where it moves and when it is destroyed. | Records Retention and Archiving v2 | DOCUMENTED/REQUIRED |

## 9. Delivery model

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-DELIVERY-001 | Eight monthly releases: E1 Foundation 1 (30 Nov 2026), E2 Foundation 2 (31 Dec 2026), E3 Settle/deed in lieu/assets (31 Jan 2027), E4 Route decision (28 Feb 2027), E5 Litigation (31 Mar 2027), E6 Debt sale and write-off (30 Apr 2027), E7 Deviations and partners (31 May 2027), E8 Administration and hardening (30 Jun 2027). | Release Plan v3; Project Overview §7 | DOCUMENTED/REQUIRED |
| CTX-DELIVERY-002 | Delivery runs as Kanban. Items are pulled in the build sequence order as capacity frees up; the two-week windows are sponsor review points, not sprint boundaries. 115 items across Epic 1 and Epic 2. | Build Sequence v4; Engineering Practices §4 | DOCUMENTED/REQUIRED |
| CTX-DELIVERY-003 | Six release gates: G1 design signed, G2 ready to pull, G3 SIT exit, G4 UAT exit, G5 go decision, G6 benefit check. A story that misses a gate stays behind its flag and moves to the next release. | Release Plan v3, Gates sheet | DOCUMENTED/REQUIRED |
| CTX-DELIVERY-004 | Engineering practices: one ACE service/repository/front end; modular monolith with boundary test; trunk-based branching, merge at least daily; AI first-pass review then one named human reviewer; tests before code; feature flags; nine pipeline checks; monthly release. | Engineering Practices v4 §1–§4 | DOCUMENTED/REQUIRED |
| CTX-DELIVERY-005 | The TechX squad shape is a tech lead, three back-end developers, one front-end developer and one QA (A-09/DL36). The ACE team owns the common module and the release decision. | Risks, Assumptions, Issues and Dependencies v2, A-09; Engineering Practices §1 | ASSUMED (DL36) |
| CTX-DELIVERY-006 | Twelve risks are open, including late data (R-01), weekly/monthly collateral data (R-02), cross-squad release contention (R-03), partner external access (R-06), Epic 3 builder (R-07), deployment slots (R-08), holidays in test weeks (R-09), business tester availability (R-10), Thai wording (R-11) and model endpoint approval (R-12). | Risks, Assumptions, Issues and Dependencies v2 | DOCUMENTED/REQUIRED |
| CTX-DELIVERY-007 | Key dependencies are on the ACE team (module folder, code owners, deployment slots, common services, release window, restructure calculator), the collection squad (EFS hand-over, shared Epic 2 items, TDR/DIL split), the architecture team (partner access, model endpoint, NFR targets) and data engineering (COLLINS feeds). | Risks, Assumptions, Issues and Dependencies v2, Dependencies sheet | DOCUMENTED/REQUIRED |

## 10. AI and agents

| ID | Statement | Evidence | Status |
|---|---|---|---|
| CTX-AI-001 | Agents prepare and recommend through one runtime; they start in shadow, then recommend to a person, and move up only on evidence. If an agent does not answer in 60 seconds or fails a guardrail, the rule result is used. | Agent Catalog v2; AI Assisted Development Approach §1 | DOCUMENTED/REQUIRED |
| CTX-AI-002 | Autonomy runs from L0 to L4. Each agent has a specification: what it watches, what it does, inputs, what it may call, output, what it may decide alone, escalation, measures, shadow release and live release. | Agent Catalog v2 | DOCUMENTED/REQUIRED |
| CTX-AI-003 | The decision log records the model, agent and prompt versions, the inputs, the recommendation, the approver and the outcome for every automated or AI-assisted decision. An action that cannot be logged does not proceed. | AI Decision Governance v2; NFR-033; ADR-009 | DOCUMENTED/REQUIRED |
| CTX-AI-004 | The model endpoint is a private endpoint in the SCB tenant, approved under DL33. The agent runtime calls models through the tool gateway; no agent calls a system of record directly. | Model Integration Design v2; Target Architecture §3; DEP-11 | ASSUMED (DL33) |
| CTX-AI-005 | AI-assisted delivery drafts stories, acceptance criteria, edge cases, test cases, UAT scripts, Thai messages, release notes and status packs; a person corrects, decides and signs each one. | AI Assisted Development Approach §1, §8 | DOCUMENTED/REQUIRED |
| CTX-AI-006 | AI-assisted engineering proposes the plan, writes tests and code, and reviews pull requests first; a developer reads every line, the tech lead approves the plan, and a named reviewer approves the merge. | AI Assisted Development Approach §1, §6 | DOCUMENTED/REQUIRED |

## 11. Constraints

| ID | Constraint | Source |
|---|---|---|
| CTX-CONSTRAINT-001 | Built on ACE: one service, one repository, one front end; recovery code in the recovery module folder. | ADR-001, ADR-002; Engineering Practices §2 |
| CTX-CONSTRAINT-002 | Modular monolith with common, collection and recovery modules; boundaries checked at build time. | ADR-002; Engineering Practices §2.2 |
| CTX-CONSTRAINT-003 | Case workflows run on Temporal from Epic 3, one workflow per case. Temporal is self-hosted on the ACE AKS clusters in the ACE namespace, with namespace rwb-recovery and task queues rwb-case, rwb-integration and rwb-platform. Case data stays the system of record in the ACE DB recovery schema; Temporal holds no case of record. Quartz and Spring Batch keep every Epic 1 and Epic 2 job. | ADR-011; D-RCV-36 |
| CTX-CONSTRAINT-004 | Rules are versioned packages, not code, evaluated by Drools embedded in the recovery module (KIE runtime libraries only). Rule packages and their versions are held in rule_package and rule_package_version; a rule change needs no release and no rule literal sits in code. | ADR-012; D-RCV-36 |
| CTX-CONSTRAINT-005 | Data through COLLINS and file loads; no direct system-of-record call; no real-time feed today. | ADR-005; REQ-DRI-006 |
| CTX-CONSTRAINT-006 | PostgreSQL; schema changes by versioned migration only; one migration per story; forward-only in production. | Engineering Practices §2.3; AI Assisted Development Approach §3.2 |
| CTX-CONSTRAINT-007 | Trunk-based development; short-lived branches; merge at least once a working day; feature flags for unfinished work. | ADR-008; Engineering Practices §4 |
| CTX-CONSTRAINT-008 | One production release a month, shared with the collection squad. | Release Plan v3; Engineering Practices §1 |
| CTX-CONSTRAINT-009 | Partner access from outside the bank is not in place; it is needed by E5 and tracked under DL03. | R-06; DEP-10 |
| CTX-CONSTRAINT-010 | No production data in prompts, tests or logs; DEV synthetic, SIT/UAT masked. | Test Strategy §4; Personal Data Protection Design §4 |

## 12. Assumptions and open decisions

The build proceeds on the recommended answer until the bank decides. The full decision log is
`requirement/legacy/01-decisions-and-governance/recovery-workbench-decision-log-v8-xlsx.md`.

| ID | Assumption / open decision | Decision log | Status |
|---|---|---|---|
| CTX-GAP-001 | Entry at 90 days past due. | DL16 | Open |
| CTX-GAP-002 | One case per customer per product. | DL17 | Open |
| CTX-GAP-003 | Application owner administers access. | DL01 | Open |
| CTX-GAP-004 | Customer facts from SCBPDM and the core bank through COLLINS. | DL20 | Open |
| CTX-GAP-005 | Provisional delegation limits from the approval authority regulation. | DL18 | Open |
| CTX-GAP-006 | Service level and caseload values are placeholders. | DL22, DL23 | Open |
| CTX-GAP-007 | Current bank letter templates are version 1. | DL28 | Open |
| CTX-GAP-008 | Inventory counts and 15% growth used for sizing. | DL15 | Open |
| CTX-GAP-009 | Monthly release in the last week of each month. | DL34 | Open |
| CTX-GAP-010 | Which interfaces need real-time data. | DL06 | Open |
| CTX-GAP-011 | Availability, RPO and RTO targets. | DL11 | Open |
| CTX-GAP-012 | Retention periods for documents, decision log and ledger. | DL26 | Open |
| CTX-GAP-013 | Partner access through the external gateway. | DL03 | Open |
| CTX-GAP-014 | Model endpoint and coding tool. | DL32, DL33 | Open |
| CTX-GAP-015 | Epic 3 builder for TDR and DIL. | DL14 | Open |

## 13. Feature catalogue

Every discovered capability has an entry. `DOCUMENTED` means a source requirement exists;
`GAP` means the source is silent or contradictory. Counts are from the source documents, not
inferred from this table.

| Feature / CTX ID | Actor and purpose | Entry or trigger | Business behaviour and outcome | Evidence status | Source |
|---|---|---|---|---|---|
| CTX-FEATURE-001 Recovery data engine | Data steward, case owner | Daily COLLINS and file loads | 14 data products loaded, checked, reconciled and freshness-stamped; case list reconciled to ALS | DOCUMENTED | REQ-RDF-001..014 |
| CTX-FEATURE-002 Integration | Platform administrator | File in/out, scheduled job | One adapter pattern with checks, logging, retry and exception queue | DOCUMENTED | REQ-DRI-006..013 |
| CTX-FEATURE-003 Case and workflow | Case owner, team manager | Account reaches 90 DPD; event on case | Case created, owned, queued, timed, transferred by rule; case list and record view | DOCUMENTED | REQ-CWC-001..020 |
| CTX-FEATURE-004 Access and administration | Security administrator, application owner | Sign-in; access request | SSO/MFA, role and scope, permission matrix, masking, delegation, access log, break-glass | DOCUMENTED | RWB-E1-022, 037-039 |
| CTX-FEATURE-005 Document hub | Case owner, litigation officer | Document arrives; OCR intake | Store, index, classify, extract, review, custody, retention, virus scan | DOCUMENTED | RWB-E1-024..026, 032-033, 040-041, 049-050, 053-054, 057 |
| CTX-FEATURE-006 Communications | Litigation officer, legal counsel | Notice or letter required | Template version, merge fields, generate, approve, dispatch, proof of delivery | DOCUMENTED | RWB-E1-034, 046, 052, 055 |
| CTX-FEATURE-007 Decision centre and log | Approver, internal audit | Decision or approval | Append-only hash-chained log; approval routing; query and export | DOCUMENTED | RWB-E1-008, 027; REQ-DEC-* |
| CTX-FEATURE-008 Payments and posting | Credit Administration officer | Receipt or approved booking | Match receipt to case/account; post booking; confirm from next ALS load | DOCUMENTED | REQ-PAY-* |
| CTX-FEATURE-009 Reporting | Product head, tribe lead | Daily/periodic | Baseline measures, case list, queue measures, steering dashboard, regulatory extracts | DOCUMENTED | RWB-E1-013; REQ-RPT-* |
| CTX-FEATURE-010 Agent runtime | AI product owner, risk | Agent run | Orchestrator, tool gateway, autonomy L0–L4, shadow, evaluation, fallback | DOCUMENTED | RWB-E1-058..063; Agent Catalog |
| CTX-FEATURE-011 Valuation and route | Case owner, approver | Route decision | Expected return by route, recommendation with reasons, approval within delegation | DOCUMENTED | REQ-ROU-*; S1 FSD/TSD |
| CTX-FEATURE-012 TDR, settlement, deed in lieu | Restructuring officer, case owner | Route approved | Treatment record, offer, settlement range, DIL readiness, booking, plan timers | DOCUMENTED | REQ-TRT-*; S2 FSD/TSD |
| CTX-FEATURE-013 Guarantees and guarantors | Guarantee officer | Default conditions met | TCG/insurer claim, deadline, checklist, result, subrogation | DOCUMENTED | REQ-GUA-*; S3 FSD/TSD |
| CTX-FEATURE-014 Litigation and enforcement | Litigation officer, enforcement owner | Notice approved; judgment | Case pack, law-firm instruction, court dates, judgment, enforcement, LED auction | DOCUMENTED | REQ-LIT-*; S4 FSD/TSD |
| CTX-FEATURE-015 Assets and auction | Sale officer, NPA manager | Asset taken on; ready to sell | Asset record, holding cost, valuation, floor, listing, auction rounds, RAMC | DOCUMENTED | REQ-AST-*; S5 FSD/TSD |
| CTX-FEATURE-016 Debt sale | Debt sale officer | Lot approved | Lot builder, reserve, buyer qualification, data room, bids, award, transfer | DOCUMENTED | REQ-DSL-*; S6 FSD/TSD |
| CTX-FEATURE-017 Write-off and recovery | Write-off team, Credit Administration | Monthly scan | Eligibility, tax criteria, committee pack, posting, provision release, post charge-off | DOCUMENTED | REQ-WOF-*; S7 FSD/TSD |
| CTX-FEATURE-018 Deviation handling | Case owner, specialist, complaint, fraud, legal | Deviation signal | X1–X7 raise, screen, contact stop, route, evidence, return | DOCUMENTED | REQ-DEV-*; S8 FSD/TSD |
| CTX-FEATURE-019 Partner management | Partner and agency manager | Placement or review | Panel, contract, fees, placement by scorecard, performance, conduct, suspension | DOCUMENTED | REQ-PRT-*; S9 FSD/TSD |
| CTX-FEATURE-020 Cross-cutting administration | Reference data administrator, platform administrator | Configuration or release | Configuration service, parameter catalogue, reference data, feature flags, migrations | DOCUMENTED | RWB-E1-042..048 |

## 14. Business rule catalogue

The full rule table is 448 rows. These are the rule families an agent must recognise; the exact row
IDs are in `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-rules-and-routing-logic-v4-xlsx.md`.

| CTX ID | Rule family | What it decides | Example source IDs | Applies to |
|---|---|---|---|---|
| CTX-RULE-001 | Entry and exclusion | Whether an account at 90 DPD becomes a case; deceased, fraud, bankruptcy, active restructure and open dispute are excluded | R-UNI-16, R-UNI-17 | Case creation |
| CTX-RULE-002 | Allocation | Which queue a new case enters by product, region, exposure band, stage, route, deviation, segment and collateral | R-UNI-18, R-UNI-19 | P3 |
| CTX-RULE-003 | Assignment | Which owner receives the case by round robin, lowest load or continuity, within the cap and overflow | R-UNI-18, R-UNI-19 | P3 |
| CTX-RULE-004 | Transfer | When a case moves queue or role on stage change, route, timer, deviation, approval, document, payment or manual request | R-UNI-20..24 | P3 |
| CTX-RULE-005 | Service level and escalation | When a warning or breach fires and who is escalated, without moving the case | R-UNI-31, R-LIT-11 | P3 |
| CTX-RULE-006 | Route decision | Which route is recommended and approved, and what happens on cure, payment, deviation or override | R-RES-01..23, R-SET-* | S1, P7 |
| CTX-RULE-007 | Restructure and settlement | Offer range, floor, approval level, booking and plan timers | R-RES-01..23, R-SET-01.. | S2 |
| CTX-RULE-008 | Guarantee claim | Claim deadline, checklist, submission and result | R-GUA-01.. | S3 |
| CTX-RULE-009 | Litigation and notice | Notice template, approval, dispatch, proof of delivery, filing, hearing and judgment | R-LIT-01.. | S4, P6 |
| CTX-RULE-010 | Asset disposal | Take-on, valuation age, floor, listing, auction round, RAMC transfer | R-DIS-01.. | S5 |
| CTX-RULE-011 | Debt sale | Lot eligibility, reserve, buyer qualification, data room, bid and award | R-DS-01.. | S6 |
| CTX-RULE-012 | Write-off | Eligibility, tax criteria, committee, posting and recovery after charge-off | R-WO-01.. | S7 |
| CTX-RULE-013 | Deviation | X1–X7 raise, contact stop, handler, evidence, return to the same decision | R-UNI-04..11, R-DEV-01 | S8 |
| CTX-RULE-014 | Partner | Panel selection, placement, fees, scorecard, conduct and suspension | R-UNI-25..30, R-LIT-23..28 | S9 |
| CTX-RULE-015 | Approval and separation of duty | Who may approve what, at which level, within which limit; preparer cannot approve | R-UNI-14, R-UNI-15, R-SET-05, R-WO-12 | P7, P4 |
| CTX-RULE-016 | Data quality and reconciliation | Load checks, control totals, key and reference checks, reconciliation tolerance | R-UNI-39; CTL-02 | P1 |

## 15. Feature coverage reconciliation

| Source entry point | Feature / rule reference | Disposition | Evidence or gap |
|---|---|---|---|
| Project Overview §7 (eight epics) | CTX-BUSINESS-006, CTX-DELIVERY-001 | Covered | Release Plan v3 confirms E1/E2, proposes E3–E8 |
| Business Requirements Program §5 (231 requirements) | CTX-FEATURE-001..020 | Covered at programme level | Epic 1 detail in Business Requirements Epic 1 v3; E3–E8 at architecture level |
| Business Requirements Epic 1 §3 (67 requirements) | CTX-FEATURE-001..010 | Covered | 57 Must, 10 Should; story files exist for 68 items |
| Business Rules and Routing Logic v4 (448 rules) | CTX-RULE-001..016 | Covered by family | Full row-level mapping belongs to the rule-table tests; not reproduced here |
| Case and Workflow Model v5 | CTX-BUSINESS-013..025 | Covered | State machine and sentries in the model workbook |
| Users, Roles and Permissions v3 (54 roles) | CTX-STAKEHOLDER-001..005 | Covered | Permission matrix and scope in the workbook |
| Logical Data Model v6 (108 entities) | CTX-DATA-001..007 | Covered | Field-level detail in the data dictionary; data classification workbook |
| Non-Functional Specification v2 (78 NFRs) | CTX-NFR-001..010 | Covered by group | Full NFR table remains the source; targets marked Proposed/Open |
| Controls Catalog v2 (42 controls) | CTX-COMPLIANCE-002 | Covered | Control-to-rule-to-obligation mapping in the workbook |
| Agent Catalog v2 | CTX-AI-001..006 | Covered | Agent-by-agent specification; autonomy levels L0–L4 |
| Screen Inventory v2 (53 screens) | CTX-FEATURE-003..019 | Covered | Screen-to-module-to-role mapping; screen specifications and prototype exist |
| Test Strategy v2 | CTX-NFR-009, testing-standards.md | Covered | Levels, environments, entry/exit, data, traceability |
| Release Plan v3 / Build Sequence v4 | CTX-DELIVERY-001..007 | Covered | 8 releases, 6 gates, 115 build items |
| Decision Log v8 | CTX-GAP-001..015 | Partially covered | 15 open decisions extracted; full log has more rows |
| Project Hub v14 | Reference only | Indexed, not converted | 26 MB generated app; not an intake source |

## 16. Gaps and contradictions

| ID | Gap | Impact | Owner | Needed by |
|---|---|---|---|---|
| CTX-GAP-016 | Filename versions and internal document versions disagree (e.g. Project Overview file v4, document says version 3; Target Architecture file v4, document says version 2). | Agents may cite the wrong version. The filename is treated as the set version; the internal version is recorded in the map. | Document owner | Before requirements approval |
| CTX-GAP-017 | Epic 1 consolidated user stories are v7, but the per-story files are v5 and the extracted folder has 69 of 79 files. | A story-level run may use an older story than the consolidated file. The consolidated v7 is canonical until the story files are reissued. | Business analyst | Before Epic 1 specification |
| CTX-GAP-018 | Epic 2 consolidated user stories are v5, per-story files v4. | Same risk as CTX-GAP-017. | Business analyst | Before Epic 2 specification |
| CTX-GAP-019 | No Figma file or live design link is in the set. Design evidence is the screen inventory, screen specifications, design system and prototype. | The Technical Specifier must use `DESIGN_EVIDENCE_STATUS: AVAILABLE` with `SOURCE: LOCAL_ARTIFACTS`, not Figma. | Front-end lead | Before first UI story |
| CTX-GAP-020 | No ACE source code is in this workspace. | Context Builder can document the intended stack from documents but cannot verify implemented behaviour. Implement/API/functional test stages need the ACE repository. | FDE | Before build |
| CTX-GAP-021 | Thai labels and messages are proposed, not approved (DL10). | UI and notice stories may ship with English labels until Thai is supplied. | Business lead | E2 |
| CTX-GAP-022 | Retention periods, RPO/RTO and availability targets are open (DL11, DL26). | NFR tests cannot be baselined; documents say "the ACE value" or "not set". | Compliance / IT lead | Before NFR test plan |
| CTX-GAP-023 | The Jira project and issue keys are not in the set. Story keys are `RWB-E1-xxx`; Jira keys are not assigned. | Traceability uses the RWB keys; the Jira column stays blank until the backlog is imported. | Product owner | Before backlog import |
| CTX-GAP-024 | The document set contains duplicate formats (md/xlsx/zip/html) with different versions. | The map marks canonical, data, reference and superseded copies. The canonical rule is in `requirement/legacy/README.md`. | Document owner | Done in this pass |
| CTX-GAP-025 | Some screens are first delivered in E8 (administration), while the underlying data can be loaded by file before then. | Do not specify an E8 screen for an E1 story; use the file-load path and record the screen as later. | Front-end lead | Before first UI story |

## 17. Source register

| Source | Path | Used for |
|---|---|---|
| Project Overview v4 | `requirement/legacy/12-project-communication/recovery-workbench-project-overview-v4-docx.md` | Business overview, problem, change, stages, plan, benefits |
| Business Architecture v4 | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-architecture-v4-pptx.md` | Actors, value stream, capability map, decisions |
| Target Operating Model v3 | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-target-operating-model-v3-pptx.md` | Organisation, roles, decision rights |
| Business Requirements Program v3 | `requirement/legacy/03-requirements-and-specifications/recovery-workbench-business-requirements-program-v3-docx.md` | Scope, outcomes, users, process architecture, 231 requirements |
| Business Requirements Epic 1 v3 | `requirement/legacy/03-requirements-and-specifications/recovery-workbench-business-requirements-epic-1-v3-docx.md` | 67 Epic 1 requirements |
| Business Requirements Epic 2 v2 | `requirement/legacy/03-requirements-and-specifications/recovery-workbench-business-requirements-epic-2-v2-docx.md` | Epic 2 requirements |
| Non-Functional Specification v2 | `requirement/legacy/03-requirements-and-specifications/recovery-workbench-non-functional-specification-v2-docx.md` | 78 NFRs, volumes, targets |
| Business Rules and Routing Logic v4 | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-rules-and-routing-logic-v4-xlsx.md` | 448 rules, 10 route sets |
| Case and Workflow Model v5 | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-case-and-workflow-model-v5-xlsx.md` | Stages, tasks, sentries, state machine |
| Users, Roles and Permissions v3 | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v3-xlsx.md` | 54 roles, permission matrix |
| Conceptual Data Model v5 | `requirement/legacy/06-data/recovery-workbench-conceptual-data-model-v5-xlsx.md` | 14 data products, 17 subject areas, 108 entities |
| Logical Data Model and Data Dictionary v6 | `requirement/legacy/06-data/recovery-workbench-logical-data-model-and-data-dictionary-v6-xlsx.md` | Field-level data dictionary |
| Physical Schema v4 | `requirement/legacy/06-data/recovery-workbench-physical-schema-v4.sql` | PostgreSQL schema |
| API Specification v2 | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` | REST/OpenAPI 3.1 paths |
| Interface Specifications v2 | `requirement/legacy/05-technical-architecture/recovery-workbench-interface-specifications-v2.md` | Interface contracts |
| Event and Messaging Design v2 | `requirement/legacy/05-technical-architecture/recovery-workbench-event-and-messaging-design-v2.md` | AsyncAPI events, outbox |
| Target Architecture v4 | `requirement/legacy/05-technical-architecture/recovery-workbench-target-architecture-v4-docx.md` | Architecture, constraints, context |
| ADR-001..009, ADR-011, ADR-012 | `docs/architecture/decisions/` | Architecture decisions |
| Engineering Practices v4 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md` | Stack, branching, tests, flags, pipeline |
| AI Assisted Development Approach v1 | `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md` | AI rules, story format, plan, review, gates |
| Agent Catalog v2 | `requirement/legacy/08-ai-and-agents/recovery-workbench-agent-catalog-and-specifications-v2.md` | Agent specifications, autonomy |
| AI Decision Governance v2 | `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-decision-governance-v2-docx.md` | Decision record, challenge, reversal |
| Model Integration Design v2 | `requirement/legacy/08-ai-and-agents/recovery-workbench-model-integration-design-v2-docx.md` | Model endpoint, inputs, change without release |
| Test Strategy v2 | `requirement/legacy/09-testing-and-quality/recovery-workbench-test-strategy-v2-docx.md` | Test levels, environments, gates |
| Definition of Ready and Done v3 | `requirement/legacy/09-testing-and-quality/recovery-workbench-definition-of-ready-and-done-v3-docx.md` | Story readiness and acceptance |
| Personal Data Protection Design v2 | `requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-personal-data-protection-design-v2-docx.md` | PDPA, lawful basis, masking, access |
| Controls Catalog v2 | `requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-controls-catalog-v2-xlsx.md` | 42 controls |
| Regulatory Requirements Map v2 | `requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-regulatory-requirements-map-v2-xlsx.md` | Obligation-to-control mapping |
| Release Plan v3 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-release-plan-v3-xlsx.md` | 8 releases, 6 gates |
| Build Sequence Epic 1 and Epic 2 v4 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v4-xlsx.md` | 115 build items, dependencies, critical path |
| Risks, Assumptions, Issues and Dependencies v2 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-risks-assumptions-issues-and-dependencies-v2-xlsx.md` | 12 risks, 10 assumptions, 3 issues, dependencies |
| Screen Inventory and Navigation v2 | `requirement/legacy/07-screens-and-experience/recovery-workbench-screen-inventory-and-navigation-v2-xlsx.md` | 53 screens |
| Screen Specifications v1 | `requirement/legacy/07-screens-and-experience/recovery-workbench-screen-specifications-v1.md` | Screen fields, states, validation |
| Design System and Component Library v1 | `requirement/legacy/07-screens-and-experience/recovery-workbench-design-system-and-component-library-v1-html.md` | Components, tokens, accessibility |
| Error and Message Standard v3 | `requirement/legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v3-docx.md` | Message IDs and wording |
| Business Glossary v2 | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-glossary-v2-xlsx.md` | 98 terms and Thai equivalents |
| Document Index v11 | `requirement/legacy/12-project-communication/recovery-workbench-document-index-v11.md` | Document numbers and readers |
| Decision Log v8 | `requirement/legacy/01-decisions-and-governance/recovery-workbench-decision-log-v8-xlsx.md` | Open decisions DL01–DL35 |

## 18. Required guidance for SDD agents

1. Read this file, `domain-context.md`, `frontend-context.md`, `backend-context.md` and
   `testing-standards.md` before producing a specification, plan or code.
2. Use the business glossary names for classes, fields, tables and endpoints. Do not invent synonyms.
3. Read thresholds, limits, timers, queues, roles, templates and routes from the versioned reference
   tables. Never hard-code them.
4. Treat the requirements in `docs/brds/` and the module specifications in `docs/prds/` as the
   approved source. If they conflict, stop and record a `CLAR-*` item; do not choose silently.
5. Record every decision and every change to a case in the decision log with the rule ID and version.
6. Apply PDPA masking and access checks on every endpoint and screen. Never put personal data in
   prompts, tests, fixtures or logs.
7. Use the story file format in `AGENTS.md` section 6 and the plan file in section 7.
8. Mark every unverified statement as `GAP` or `ASSUMED` and name the decision log entry.
9. Keep the traceability chain: `CTX -> BRD -> FR/NFR -> US -> SPEC -> TASK -> CODE -> APT/FT/TEST ->
   REVIEW -> DOC`.
10. The first increment is Epic 1. Do not specify Epic 2 or later work without an approved increment
    card and a named `RUN_ID`.
