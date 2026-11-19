# Recovery Workbench — consolidated business requirements document

## 0. Trace metadata

| Field | Value |
|---|---|
| Project | Recovery Workbench (recovery module of ACE) |
| Document | Consolidated BRD |
| Version | 1.0 |
| Date | 2026-11-04 |
| Source | `docs/brds/` (Lean BRD Epic 1 v2, Lean BRD Epic 2 v2, Business Requirements Program v3, Business Requirements Epic 1 v3, Business Requirements Epic 2 v2) |
| Upstream IDs | CTX-BUSINESS-*, CTX-STAKEHOLDER-*, CTX-FEATURE-*, CTX-RULE-*, CTX-DATA-*, CTX-NFR-*, CTX-COMPLIANCE-*, CTX-DELIVERY-* |
| Generated IDs | BRD-RWB-001 to BRD-RWB-020 |
| Status | Draft for requirements approval |
| Owner | Product Owner (TBC) |

## 1. Purpose

This BRD consolidates the approved Recovery Workbench business requirements into one document that
the intake and specification stages can consume. It states what the Workbench must do, for whom, how
well and under which constraints. It does not replace the detailed module specifications; it indexes
them and preserves their source IDs.

## 2. Business context

The Recovery Workbench is the system that owns every recovery case from 90 days past due to close for
Mortgage, Hire Purchase and SSME. It is built as the recovery module of ACE, the bank's collection
engine, so collection and recovery work in one application with one case view.

The problem is documented in `docs/discovery/project-overview.md` §2:

- Collections and recovery staff use 42 applications; a case's facts are spread across the core bank,
  EFS, LIT, CCMS, SVAF, AMIS and document stores, and no screen shows them together.
- Teams keep their own case lists in Excel and SharePoint, build account plans by hand and approve by
  email. Hand-overs between teams are manual.
- Why a route was chosen, who approved it and on what figures is spread across emails and files.
  Audit findings and fraud cases number 50.
- Turnaround is 21 days for litigation, 23 days for a restructure and 26 days for a deed in lieu.
  The NPA sales cycle is 1,486 days.

The Workbench changes this with one case list reconciled to the core bank, one owner per case by
rule, one decision record, versioned rules and limits, a document hub, partner instructions and one
place for the evidence.

## 3. Scope

### 3.1 In scope

- Every recovery case from 90 days past due to close, for Mortgage, Hire Purchase and SSME.
- Decisions D6–D9 and their sub-decisions; D5 once the restructure programme is live; deviations
  X1–X7 after day 90.
- Partners, documents, the decision log and the interaction ledger.
- The recovery module of ACE, with data through COLLINS and file loads.

### 3.2 Out of scope

| Out of scope | Where it is handled |
|---|---|
| Collections before day 90, decisions D1–D4 | EFS and the ACE collection module |
| Dialer and messaging channels | Existing bank channels through the ACE notification path |
| Core bank booking logic | ALS |
| COLLINS model development | Data and AI |
| Restructure affordability and plan calculation | The ACE restructure calculator |
| Partner systems | Each partner |
| Changes to bank policy | The policy owners |

Source: Business Requirements Program §1.

## 4. Stakeholders and users

| Class | Count | Examples |
|---|---:|---|
| Bank user | 37 | Case owner, team manager, restructuring officer, litigation officer, enforcement owner, sale officer, NPA manager, debt sale officer, write-off team member, Credit Administration officer, guarantee officer, partner and agency manager, capacity planner, product heads, control functions |
| Partner user | 7 | Collection agency, law firm, valuer, auction vendor, debt buyer/AMC, RAMC, Legal Execution Department |
| Customer party | 4 | Borrower, guarantor/co-borrower, heir/estate representative, retail asset bidder |
| Non-human actor | 6 | Case workflow, rules component, data load, OCR, decision log writer, agent platform |

The operating model has product heads, shared operations, centre of excellence and platform, plus
control functions and committees. 1,234 named users; about 410 online in the busiest hour.

Source: Users, Roles and Permissions v3; Target Operating Model v3; Non-Functional Specification §2.

## 5. Business outcomes and measures

| Measure | Today | 2027 target |
|---|---|---|
| Recovery rate on NPL | 66.3% (2026 to date) | 73% |
| Litigation turnaround | 21 days | 6 days |
| Deed in lieu turnaround | 26 days | 12 days |
| Restructure turnaround | 23 days | 5 days |
| Debt sale turnaround | No baseline | 45 days |
| Manual processes removed | Near zero | 80% of the selected list |
| Audit findings and fraud cases | 50 | 13 |
| NPA sales cycle | 1,486 days | 1,095 days |

Each measure is read from the decision log per decision, with the baseline set in Epic 1.

## 6. Process and case model

### 6.1 Six stages

| Stage | What it produces |
|---|---|
| Receive the case | One owner, the history from collections, running deadlines and a deviation screen |
| Choose the route | An approved route with the expected return of each option and the reasons |
| Resolve with the customer | A settlement, deed in lieu, guarantee claim or guarantor agreement, booked and reconciled |
| Enforce | A judgment enforced, a settlement before judgment, or proceeds matched to the case |
| Realise the asset | Cash from the asset or the debt: auction, RAMC, buy-back, rental or debt sale |
| Close | The balance written off and posted, recovery after charge-off, the case closed |

A case can return to the route decision at any stage on a cure, a payment, a deviation or an override.

### 6.2 Decisions

| Decision | What is decided | Owner | Where it runs |
|---|---|---|---|
| D1 | Act on the signal | Product head with the centre of excellence | EFS |
| D2 | Reach the customer | Centre of excellence with Compliance | EFS |
| D3 | Promise kept | Centre of excellence | EFS |
| D4 | Escalate | Product head with the agency unit | EFS |
| D5 | Offer a restructure | Product head with Credit Risk | EFS and ACE |
| D6 | Which route | Recovery Strategy with Risk | Recovery Workbench |
| D7 | Litigate and enforce | Head of Litigation | Recovery Workbench |
| D8 | Dispose assets and sell debt | Head of NPA / Head of Asset Liquidity | Recovery Workbench |
| D9 | Write off and recover after charge-off | Credit Administration with Risk | Recovery Workbench |

Every decision follows five steps: gather and check the information, decide by a rule, a model or an
agent, make the outcome final or send it to the approver, act in the systems, and log the decision
once.

### 6.3 Deviations

X1 complaint or dispute, X2 hardship or vulnerability, X3 deceased customer, X4 fraud, X5 bankruptcy
or external seizure, X6 lost contact, X7 legal hold or other. A deviation stops contact or enforcement
as its rule requires and returns the case when it clears.

### 6.4 Rules

448 rules in ten route sets. Each rule has a rule ID, route set, decision, from state, event,
condition, action, to state, owner, systems and timer. Hit policy is Unique: in a route set, for one
state and one event, one condition holds. 252 rules carry a timer; 366 move the case to a state owned
by a person or partner.

## 7. Business requirements by capability

| ID | Capability | Requirement | Source | Priority |
|---|---|---|---|---|
| BRD-RWB-001 | P1 Recovery data engine | Hold 14 data products, load ALS/EFS/CCMS/SVAF and file loads daily, reconcile the case list to ALS, run data quality rules, stamp freshness, control access, publish baseline measures and keep the interaction ledger. | REQ-RDF-001..014; CTX-FEATURE-001 | Must |
| BRD-RWB-002 | P2 Integration | One adapter pattern for file loads and outbound files with checks, logging, retry and an exception queue; no direct system-of-record call; ADF/Control-M jobs; run books. | REQ-DRI-006..013; CTX-FEATURE-002 | Must |
| BRD-RWB-003 | P3 Case and workflow | Case creation, case ID, state model, queues, allocation, assignment, transfer, service levels, timers, prescription dates, rule load and rollback, rebalancing, case list and case record view. | REQ-CWC-001..020; CTX-FEATURE-003 | Must |
| BRD-RWB-004 | P4 Access and administration | Entra ID SSO/MFA, roles and scopes, role-to-permission matrix as data, PDPA masking, delegation of authority, access log, break-glass admin, full administration. | REQ-ACA-*; RWB-E1-022, 037–039; CTX-FEATURE-004 | Must |
| BRD-RWB-005 | P5 Document hub | Store documents against the case, index by type/date/source/fields, write-once for legal types, OCR, classification, field extraction, review queue, custody, retention, virus scan, intake. | REQ-DOC-*; RWB-E1-024..026, 032–033, 040–041, 049–050, 053–054, 057; CTX-FEATURE-005 | Must |
| BRD-RWB-006 | P6 Communications | Letter and notice templates as versioned data with Legal approval, merge fields, notice generation, dispatch through WIN, proof-of-delivery capture. | REQ-COM-*; RWB-E1-034, 046, 052, 055; CTX-FEATURE-006 | Must |
| BRD-RWB-007 | P7 Decision centre and log | Append-only hash-chained decision log, writer, approval routing, decision centre, query and export, approval levels, separation of duty. | REQ-DEC-*; RWB-E1-008, 027; CTX-FEATURE-007 | Must |
| BRD-RWB-008 | P8 Payments and posting | Match receipts to cases and accounts, exception list, post approved bookings, confirm from the next ALS load. | REQ-PAY-*; CTX-FEATURE-008 | Must |
| BRD-RWB-009 | P9 Reporting | Baseline measures, case list in Power BI, queue measures, steering dashboard, regulatory extracts, benefit tracking. | REQ-RPT-*; RWB-E1-013; CTX-FEATURE-009 | Must |
| BRD-RWB-010 | P10 Agent runtime | Agent platform, orchestrator and tool gateway, autonomy L0–L4, shadow runs, evaluations, monitoring, fallback to rules, model endpoint. | REQ-AGT-*; RWB-E1-058..063; CTX-FEATURE-010 | Must |
| BRD-RWB-011 | S1 Valuation and route | Expected return by route, route recommendation with reasons, approval within the delegation, route decision screen. | REQ-ROU-*; CTX-FEATURE-011 | Must |
| BRD-RWB-012 | S2 TDR, settlement and deed in lieu | Treatment record, restructure offer, settlement range, deed in lieu readiness, appraisal order, transfer, booking, plan timers. | REQ-TRT-*; CTX-FEATURE-012 | Must |
| BRD-RWB-013 | S3 Guarantees and guarantors | TCG and insurer claims, claim deadlines, guarantor pursuit, subrogation. | REQ-GUA-*; CTX-FEATURE-013 | Must |
| BRD-RWB-014 | S4 Litigation and enforcement | Notice approval, case pack, law-firm instruction, court dates, hearings, judgment, enforcement, LED auction, proof of delivery. | REQ-LIT-*; CTX-FEATURE-014 | Must |
| BRD-RWB-015 | S5 Assets and auction | Asset take-on, holding cost, stock balance, valuation, floor price, listing on HOME.SCB, auction rounds, RAMC transfer. | REQ-AST-*; CTX-FEATURE-015 | Must |
| BRD-RWB-016 | S6 Debt sale | Lot builder, reserve price, buyer qualification, data room, bids, award, data transfer, put-backs. | REQ-DSL-*; CTX-FEATURE-016 | Must |
| BRD-RWB-017 | S7 Write-off and recovery | Monthly write-off scan, eligibility and tax criteria, committee pack, posting, provision release, recovery after charge-off. | REQ-WOF-*; CTX-FEATURE-017 | Must |
| BRD-RWB-018 | S8 Deviation handling | X1–X7 end to end: raise, screen, contact stop, route to handler, evidence, return to the same decision. | REQ-DEV-*; CTX-FEATURE-018 | Must |
| BRD-RWB-019 | S9 Partner management | Partner panel, contracts, fees, placement by scorecard, performance, conduct, suspension, field app. | REQ-PRT-*; CTX-FEATURE-019 | Must |
| BRD-RWB-020 | Cross-cutting administration | Configuration service, parameter catalogue, reference data service, versioned tables, multi-product parameters, feature flags, migrations, rule change audit. | RWB-E1-042..048; CTX-FEATURE-020 | Must |

## 8. Non-functional requirements

| Group | Target | Source |
|---|---|---|
| Volume | 23,600 open cases at go-live; 26,500 at end 2027; 3,110 new accounts/month; 28,119 active accounts at 90+ DPD | NFR-001; Volume Forecast |
| Users | 1,234 named; about 370 staff and 50 partner online in the busiest hour; about 21 requests/second | NFR-002, NFR-003 |
| Response | Screens <2s P95; case record <2s; rule evaluation <300ms; agent <60s then fallback; case search <3s; document search <5s | NFR-008..012 |
| Loads | COLLINS by 07:00; rebalancing by 07:00; daily reconciliation; OCR 500 pages/hour; classification 90% | NFR-013..019 |
| Availability | 99.9% business hours; 99.5% outside; RPO/RTO are the ACE values (open DL11) | NFR-020..023 |
| Resilience | Agent/model outage falls back to rules; outbound queue and retry; three retries then exception; rollback by previous tag | NFR-024..027 |
| Audit | Every decision reproducible with rule/model/agent/prompt versions; every action has a rule version and approver; daily hash-chain check | NFR-033..036 |
| Retention | Retention classes per document type; write-once for legal; decision log and ledger retention by Compliance; legal hold overrides; recorded disposal | NFR-028..032, 072–075 |
| Accessibility | WCAG 2.2 AA; automated and keyboard checks; no A/AA failure | Accessibility Standard; Test Strategy |
| Scale | 5.8 million documents and 2.8 TB by 2031; 36 GB decision log/ledger; case history <2s at that size | NFR-007, 069, 070 |

## 9. Data and integration

### 9.1 Data products

| ID | Data product | System of record | Freshness |
|---|---|---|---|
| DP01 | Account and arrears | Core bank (ALS) via COLLINS | End of day; next morning in the Workbench |
| DP02 | Customer and party | SCBPDM and core bank via COLLINS | End of day; next morning |
| DP03 | Case and ownership | Recovery Workbench | As it changes |
| DP04 | Treatment and offers | Workbench; restructure plans in ACE | As it changes |
| DP05 | Contact and promises | EFS before day 90; Workbench after | End of day for EFS; as it changes after |
| DP06 | Collateral and assets | CCMS, SVAF, AMIS, RPS | Weekly or monthly today |
| DP07 | Legal events and cases | LIT; Workbench for instructions | End of day for LIT status |
| DP08 | Partner performance | Workbench; partner portal | As it changes |
| DP09 | Debt sale | Workbench | As it changes |
| DP10 | Documents and extracted fields | Workbench document hub | As it changes |
| DP11 | Scores and route economics | COLLINS | End of day; monthly for some models |
| DP12 | Decision log | Workbench | As it changes |
| DP13 | Money and closure | Core bank and GL via COLLINS/file | End of day for payments; monthly for GL |
| DP14 | Reference data | Workbench | By versioned load |

### 9.2 Integration rules

- No component calls a system of record directly. Data arrives through COLLINS or a file load and
  leaves through paths ACE already has.
- One adapter pattern for file loads and outbound files, with checks, logging, retry and an exception
  queue.
- Same-day data needs are named under DL06 before an interface is built.
- The API is REST/OpenAPI 3.1; events are AsyncAPI 3.0; outbound work uses an outbox with idempotency.

## 10. Business rules

| Rule family | What it decides | Source |
|---|---|---|
| Entry and exclusion | Whether an account at 90 DPD becomes a case; deceased, fraud, bankruptcy, active restructure and open dispute are excluded | R-UNI-16, R-UNI-17 |
| Allocation | Which queue a new case enters by product, region, exposure band, stage, route, deviation, segment and collateral | R-UNI-18, R-UNI-19 |
| Assignment | Which owner receives the case by round robin, lowest load or continuity, within the cap and overflow | R-UNI-18, R-UNI-19 |
| Transfer | When a case moves queue or role on stage, route, timer, deviation, approval, document, payment or manual request | R-UNI-20..24 |
| Service level and escalation | When a warning or breach fires and who is escalated, without moving the case | R-UNI-31, R-LIT-11 |
| Route decision | Which route is recommended and approved; cure, payment, deviation, override | R-RES-01..23, R-SET-* |
| Restructure and settlement | Offer range, floor, approval level, booking, plan timers | R-RES-01..23, R-SET-01.. |
| Guarantee claim | Claim deadline, checklist, submission and result | R-GUA-01.. |
| Litigation and notice | Template, approval, dispatch, proof of delivery, filing, hearing, judgment | R-LIT-01.. |
| Asset disposal | Take-on, valuation age, floor, listing, auction round, RAMC transfer | R-DIS-01.. |
| Debt sale | Lot eligibility, reserve, buyer qualification, data room, bid, award | R-DS-01.. |
| Write-off | Eligibility, tax criteria, committee, posting, recovery after charge-off | R-WO-01.. |
| Deviation | X1–X7 raise, contact stop, handler, evidence, return | R-UNI-04..11, R-DEV-01 |
| Partner | Panel selection, placement, fees, scorecard, conduct, suspension | R-UNI-25..30, R-LIT-23..28 |
| Approval and separation of duty | Who may approve what, at which level, within which limit; preparer cannot approve | R-UNI-14, R-UNI-15, R-SET-05, R-WO-12 |
| Data quality and reconciliation | Load checks, control totals, key and reference checks, reconciliation tolerance | R-UNI-39; CTL-02 |

## 11. Compliance and controls

- Thai PDPA B.E. 2562; lawful bases proposed and confirmed by Compliance under DL26.
- 42 controls in the Controls Catalog, each with an owner, evidence and test.
- Regulatory requirements map links each obligation to the process step, rule and control.
- Audit findings response map links each open finding to the change that closes it.
- Records retention and archiving sets how long each record and document is held.
- No production data in prompts, tests or logs; DEV synthetic, SIT/UAT masked.

## 12. Delivery

| Epic | Release | Theme | What the business gets |
|---|---|---|---|
| E1 | 30 Nov 2026 | Foundation 1 | One case list, documents by case, decision log store, read-only case record view, allocation/assignment/transfer by rule, timers and prescription dates, baseline measures, agent runtime in shadow |
| E2 | 31 Dec 2026 | Foundation 2 | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | 31 Jan 2027 | Settle, deed in lieu, assets | Settlements and deeds in lieu end to end to booking; asset record, floor price and listing on HOME.SCB |
| E4 | 28 Feb 2027 | Route decision | Route recommended with reasons and approved within the delegation; guarantee and TCG claims; auction rounds and RAMC transfer |
| E5 | 31 Mar 2027 | Litigation | Litigation instructed and tracked end to end; law firms through the partner portal; debt sale lot data and buyer data room |
| E6 | 30 Apr 2027 | Debt sale and write-off | Debt sale screens and award; write-off committee; partner panel, allocation and fees |
| E7 | 31 May 2027 | Deviations and partners | Deviations X1–X7 end to end; partner scoring, conduct and field app |
| E8 | 30 Jun 2027 | Administration and hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |

Six gates: G1 design signed, G2 ready to pull, G3 SIT exit, G4 UAT exit, G5 go decision, G6 benefit
check. A story that misses a gate stays behind its flag and moves to the next release.

## 13. Risks, assumptions and dependencies

### 13.1 Risks

| ID | Risk | Impact | Likelihood | Action | Owner |
|---|---|---|---|---|---|
| R-01 | Data arrives a day late for decisions that need today's position | High | Medium | Officers confirm payoff figures in the core; same-day triggers named under DL06 | Solution architect |
| R-02 | Collateral, appraisals and assets arrive weekly or monthly | Medium | High | Age limits on decision inputs; batch feeds requested under DL12 | Data lead |
| R-03 | One squad's change holds the other's release | Medium | Medium | Feature flags, code owners and the module boundary test | Tech leads |
| R-04 | Rules component is new to ACE | Medium | Medium | Decision table evaluator in the recovery module, tested rule by rule | Solution architect |
| R-05 | Volume grows faster than forecast | Medium | Low | Sized at 15% inflow growth; reviewed each quarter | Data lead |
| R-06 | Partner access from outside the bank takes one to three months | High | High | Change raised in November; law firms first needed at Epic 5 | Product owner |
| R-07 | Epic 3 has no confirmed builder for TDR and DIL | High | Medium | Decision DL14 by 6 Nov | IT lead |
| R-08 | Deployment slots limit parallel testing | Medium | High | One DEV and one SIT slot shared until DL35 | ACE team |
| R-09 | Songkran and Chakri Day fall in Epic 6 test weeks | Medium | High | Release window confirmed under DL34; testers booked early | Program manager |
| R-10 | Business testers not available during the build | High | Medium | Testers named under DL09; scripts prepared with analysts | Business lead |
| R-11 | Thai wording not ready for Epic 2 screens and letters | Medium | Medium | English release with Thai labels loaded as reference data when supplied | Business lead |
| R-12 | Agent model endpoint not approved | Medium | Medium | Agents run in shadow; rules decide | CTO with Enterprise AI |

### 13.2 Assumptions

Entry at 90 DPD (DL16); one case per customer per product (DL17); application owner administers access
(DL01); customer facts from SCBPDM and the core through COLLINS (DL20); provisional delegation limits
(DL18); service level and caseload placeholders (DL22, DL23); current bank templates as version 1
(DL28); inventory counts and 15% growth (DL15); TechX squad shape (DL36); monthly release in the last
week (DL34).

### 13.3 Dependencies

ACE team: module folder, code owners, deployment slots, common services, release window, restructure
calculator. Collection squad: EFS hand-over, shared Epic 2 items, TDR/DIL split. Architecture team:
partner access, model endpoint, NFR targets. Data engineering: COLLINS feeds.

## 14. Open decisions

DL01 access owner; DL02 application owner; DL03 partner access; DL04 merge owner; DL05 module folder;
DL06 same-day interfaces; DL09 business testers; DL10 Thai wording; DL11 availability/RPO/RTO; DL12
legacy systems; DL13 requirement template; DL14 Epic 3 builder; DL15 volume; DL16 entry at 90/91;
DL17 one case; DL18 delegation; DL20 customer facts; DL22 service levels; DL23 caseload; DL25
reconciliation tolerance; DL26 retention and PDPA; DL27 storage; DL28 templates; DL29 EFS hand-over;
DL30 shared Epic 2 items; DL32 coding tool; DL33 model endpoint; DL34 release window; DL35 deployment
slots; DL36 squad shape; DL37 code owners. Full text in the Decision Log v8.

## 15. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Product Owner | TBC | | |
| Forward Deployed Architect | TBC | | |
| Business lead | TBC | | |
| Compliance and PDPA officer | TBC | | |

## 16. Traceability summary

```text
CTX-BUSINESS-* / CTX-STAKEHOLDER-* / CTX-FEATURE-* / CTX-RULE-* / CTX-DATA-* / CTX-NFR-*
  -> BRD-RWB-001..020
  -> FR-RWB-* / NFR-RWB-*
  -> US-RWB-E1-* / US-RWB-E2-*
  -> SPEC-*
  -> TASK-* -> CODE-* -> APT-* / FT-* -> TEST-* -> REVIEW-* -> DOC-*
```

The detailed matrix is `requirement/Traceability_Matrix.md`. The source-ID crosswalk preserves
`REQ-*`, `RWB-E*`, `BR-*`, `MSG-*`, `DF-*` and `TC-*` without renumbering the source documents.
