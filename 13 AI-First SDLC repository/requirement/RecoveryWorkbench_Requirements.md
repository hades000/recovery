# Recovery Workbench Requirements — Epic 1 (Foundation 1)

## 0. Trace metadata

| Field | Value |
|---|---|
| GitHub Issue | N/A (Jira project and keys TBC — CTX-GAP-023) |
| Run ID | pre-specify |
| Branch | N/A |
| Source Commit | N/A (document set, no code repository in this workspace) |
| Upstream Artifact | `requirement/BRD_RecoveryWorkbench.md` |
| Upstream IDs | BRD-RWB-001 to BRD-RWB-020; CTX-BUSINESS-*, CTX-FEATURE-*, CTX-RULE-*, CTX-DATA-*, CTX-NFR-* |
| Generated IDs | FR-RWB-001 to FR-RWB-020; NFR-RWB-001 to NFR-RWB-010; US-RWB-E1-001 to US-RWB-E1-068; AC-RWB-E1-*; BR-RWB-*; INT-RWB-*; ERR-RWB-* |
| Scope | Epic 1 only. Epic 2 is a separate increment (`EPIC-002`); Epics 3–8 are programme-level. |
| Status | Draft for specification |

## 1. Project overview

### Summary

Epic 1, Foundation 1, releases on 30 November 2026. It delivers one case list for every account at
90 days past due or more, reconciled to the core bank; documents found by case; the decision log
store; a read-only case record view; allocation, assignment and transfer by rule; timers and
prescription dates; baseline measures; and the agent runtime in shadow.

### Business context

The Workbench owns every recovery case from 90 days past due to close for Mortgage, Hire Purchase and
SSME. It is the recovery module of ACE. Today, 42 applications hold the facts, teams run cases from
Excel and SharePoint, decisions are spread across email and files, and turnaround is 21 days for
litigation, 23 days for a restructure and 26 days for a deed in lieu. Epic 1 replaces the team lists
with one reconciled case list and starts the decision record that later epics depend on.

### Relationship to existing system

The Workbench is a new module inside the existing ACE service. It reuses ACE sign-in, access control,
audit and PII logging, the shared case view and the common entities. It takes data through COLLINS
and file loads. It does not replace ACE, EFS or the core bank.

## 2. Actors and personas

| Actor | Role code | Access level | Key goals |
|---|---|---|---|
| Case owner | RW-CASEOWN | Own scope | See my cases, the history and the next action; act within my limit |
| Team manager | RW-TEAMMGR | Team scope | Keep queues balanced, see ageing and breaches, reassign with a reason |
| Data steward and data product owner | RW-DATASTEW | All | Trust the load, reconcile to ALS, see data quality breaks |
| Centre of excellence analyst | RW-COE | All | Own the rule tables, parameters and measures |
| Platform administrator | RW-PLADM | All | Run the environment, jobs, interfaces and break-glass |
| Security administrator | RW-SECADM | All | Own the role-to-permission matrix, access log and break-glass approval |
| Compliance and PDPA officer | RW-COMPLY | All | Rule on PDPA, retention, consent and masking |
| Internal audit | RW-AUDIT | All | Query the decision log and sample cases |
| Product owner | — | All | Own the backlog, release and benefit |
| Case workflow module | SY-CASEWF | Service | Hold state, run clocks, move the case by rule |
| Rules component | SY-RULES | Service | Evaluate the versioned rule tables |
| Data load | SY-DATALOAD | Service | Load COLLINS and file loads, write outbound files |
| OCR and extraction | SY-OCR | Service | Classify, extract and attach documents |
| Decision log writer | SY-DECLOG | Service | Write the append-only, hash-chained entry |
| Agent platform | SY-AGENT | Service | Run agents at the approved autonomy level |

## 3. User stories

Epic 1 has 67 requirements and 68 story files (the count includes the technical enablers). The full
per-story detail is in:

- `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-v7.md` (consolidated, canonical narrative)
- `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/` (per-story files; 79 entries)
- `requirement/legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v4-xlsx.md` (pull order and dependencies)

The story groups are:

| Group | Story keys | Module | Count | Representative stories |
|---|---|---|---:|---|
| Data foundation | RWB-E1-001 to 017, 064–068 | P1 | 22 | Recovery tables for the 14 data products; ALS daily extract; case list v1; data quality rules; interaction ledger |
| Integration | RWB-E1-007, 047, 051, 056 | P2 | 4 | Integration adapters; feature flags; ADF/Control-M jobs; run books |
| Case and workflow | RWB-E1-018 to 021, 028–031, 035, 042–045, 048 | P3 | 15 | Case ID and case record; allocation and assignment; transfer; service levels and timers; rule load and rollback |
| Access and administration | RWB-E1-022, 037–039 | P4 | 4 | SSO/MFA; role-to-permission matrix; delegation of authority; access log and break-glass |
| Document hub | RWB-E1-024 to 026, 032–033, 040–041, 049–050, 053–054, 057 | P5 | 13 | Document store and index; document types; attach and search; OCR; classification; field extraction; review queue |
| Communications | RWB-E1-034, 046, 052, 055 | P6 | 4 | Letter template management; merge field catalogue; notice generation; proof of delivery |
| Decision centre and log | RWB-E1-008, 027 | P7 | 2 | Decision log store; decision log writer |
| Reporting | RWB-E1-013 | P9 | 1 | Baseline measures |
| Agent runtime | RWB-E1-058 to 063 | P10 | 6 | Agent platform; case intake agent in shadow; extraction evaluation; deviation screening; monitoring |
| Technical enablers | RWB-TE-001 to 013 | Cross-cutting | 13 | Module folder and boundary test; code owners; contract tests; masked data; rule harness; outbox; Quartz; hash-chain check; PDPA lint; storage; agent client |

Each story is in Connextra form with Given/When/Then acceptance criteria, business rules, state
transitions, authority, contract, validation and messages, screen and states, guardrails, test cases
and out of scope. The worked example is `RWB-E1-020` (allocation and assignment engine).

## 4. Functional requirements

| ID | Requirement | Derived from | Priority | Acceptance criteria |
|---|---|---|---|---|
| FR-RWB-001 | The Workbench shall hold 14 data products in the ACE database, each with one system of record, one owner, one way in and one freshness stamp. | BRD-RWB-001; REQ-RDF-001..014 | Must | AC-RWB-001 |
| FR-RWB-002 | The Workbench shall load ALS, EFS, CCMS, SVAF and inventoried files daily, run data quality rules and reconcile the case list to ALS with no unexplained variance (DL25). | BRD-RWB-001; RWB-E1-001..017 | Must | AC-RWB-002 |
| FR-RWB-003 | The Workbench shall use one adapter pattern for file loads and outbound files, with checks, logging, retry and an exception queue; no component shall call a system of record directly. | BRD-RWB-002; REQ-DRI-006..013 | Must | AC-RWB-003 |
| FR-RWB-004 | The Workbench shall create one recovery case per account at 90+ days past due that is not excluded, with a case ID RW-YYYY-NNNNNN, a stage, a status and linked accounts. | BRD-RWB-003; REQ-CWC-001..005 | Must | AC-RWB-004 |
| FR-RWB-005 | The Workbench shall place every new case in a queue and assign an owner by rule, with first match, a default row, a capacity cap and an overflow queue. | BRD-RWB-003; REQ-CWC-006..009 | Must | AC-RWB-005 |
| FR-RWB-006 | The Workbench shall move cases between queues and roles by transfer rule on stage, route, timer, deviation, approval, document, payment or manual request with a reason code. | BRD-RWB-003; REQ-CWC-010 | Must | AC-RWB-006 |
| FR-RWB-007 | The Workbench shall hold service levels, warning thresholds, escalation targets and prescription dates as versioned data and raise an event on breach without moving the case. | BRD-RWB-003; REQ-CWC-011..012 | Must | AC-RWB-007 |
| FR-RWB-008 | The Workbench shall load rule tables from a validated Excel template with schema, overlap, unreachable-row, missing-default and 50-test-case checks; a load shall carry a version and roll back by one call. | BRD-RWB-003, BRD-RWB-020; REQ-CWC-013..014; RWB-E1-029 | Must | AC-RWB-008 |
| FR-RWB-009 | The Workbench shall provide a case list with case ID, account, product, stage, status, owner, queue, route, balance and days past due, refreshed daily and available in Power BI. | BRD-RWB-003, BRD-RWB-009; RWB-E1-002 | Must | AC-RWB-009 |
| FR-RWB-010 | The Workbench shall provide a read-only case record view with accounts, arrears, owner, queue, stage, status, contact history, documents and a timeline. | BRD-RWB-003; RWB-E1-023, RWB-E1-035 | Must | AC-RWB-010 |
| FR-RWB-011 | The Workbench shall sign users in through Entra ID SSO with MFA and show only the screens and data their roles and scope allow. | BRD-RWB-004; RWB-E1-022 | Must | AC-RWB-011 |
| FR-RWB-012 | The Workbench shall hold the role-to-permission matrix, delegation of authority, queues, service levels, document types, templates, legal periods and holidays as versioned reference data. | BRD-RWB-004, BRD-RWB-020; RWB-E1-037..038, RWB-E1-043 | Must | AC-RWB-012 |
| FR-RWB-013 | The Workbench shall mask personal data by role, log every read of a personal field through PII Kafka, and record every access and export in the access log. | BRD-RWB-004; RWB-E1-037, RWB-E1-039; PDPA Design | Must | AC-RWB-013 |
| FR-RWB-014 | The Workbench shall store documents against the case, index them by type, date, source and extracted fields, and use a write-once container for legal types. | BRD-RWB-005; RWB-E1-024..026 | Must | AC-RWB-014 |
| FR-RWB-015 | The Workbench shall OCR, classify and extract the six agreed document types, send low-confidence results to a review queue, and attach documents from branch, mailroom, partner SFTP and email intake. | BRD-RWB-005; RWB-E1-049..054, RWB-E1-057 | Must | AC-RWB-015 |
| FR-RWB-016 | The Workbench shall hold letter and notice templates and merge fields as versioned data with Legal approval, generate notices from approved templates and capture proof of delivery from WIN. | BRD-RWB-006; RWB-E1-034, 046, 052, 055 | Must | AC-RWB-016 |
| FR-RWB-017 | The Workbench shall write an append-only, hash-chained decision log entry for every decision and every change to a case, with the rule ID and version used; an action that cannot be logged shall not proceed. | BRD-RWB-007; RWB-E1-008, RWB-E1-027; ADR-009 | Must | AC-RWB-017 |
| FR-RWB-018 | The Workbench shall publish the Epic 1 baseline measures: cases by route, age and queue, realised recovery, time in stage and turnaround per route, with definitions agreed with the Tribe. | BRD-RWB-009; RWB-E1-013 | Must | AC-RWB-018 |
| FR-RWB-019 | The Workbench shall run the agent platform, the case intake agent and the deviation screening agent in shadow, with a 60-second answer target and fallback to the rule result. | BRD-RWB-010; RWB-E1-058..063 | Must | AC-RWB-019 |
| FR-RWB-020 | The Workbench shall provide a configuration service, a parameter catalogue, multi-product parameters, feature flags and versioned database migrations with no hard-coded business values. | BRD-RWB-020; RWB-E1-042..048 | Must | AC-RWB-020 |

## 5. Non-functional requirements

| ID | Category | Requirement | Target | Derived from |
|---|---|---|---|---|
| NFR-RWB-001 | Capacity | The case store holds one case per customer and product for every account at 90+ DPD. | 23,600 open cases at go-live; 26,500 at end 2027; 3,110 new accounts/month | NFR-001; CTX-NFR-001 |
| NFR-RWB-002 | Concurrency | The system supports the peak number of staff and partner users online. | About 370 staff and 50 partner users; 1,234 named; 21 requests/second | NFR-002, 003; CTX-NFR-002 |
| NFR-RWB-003 | Response time | Screens, case record, rule evaluation, agent answer, case search and document search meet their targets. | <2s screens; <2s case record; <300ms rule; <60s agent then fallback; <3s case search; <5s document search | NFR-008..012; CTX-NFR-003 |
| NFR-RWB-004 | Batch | The COLLINS load and the rebalancing job complete before the working day; reconciliation runs daily. | By 07:00; no unexplained variance | NFR-013..019; CTX-NFR-004 |
| NFR-RWB-005 | Availability | The Workbench is available in and outside business hours. | 99.9% business hours; 99.5% outside; RPO/RTO are the ACE values (DL11) | NFR-020..023; CTX-NFR-005 |
| NFR-RWB-006 | Resilience | An agent/model outage falls back to rules; an outbound action is queued and retried; a release rolls back by the previous tag. | Fallback always; three retries then exception; rollback by tag | NFR-024..027; CTX-NFR-006 |
| NFR-RWB-007 | Auditability | Every decision is reproducible from the log; every action carries the rule version and approver; the hash chain is checked daily. | Every decision; daily check; same-day report | NFR-033..036; CTX-NFR-007 |
| NFR-RWB-008 | Retention | Every document type has a retention class; legal documents are write-once; legal hold overrides retention; disposal is recorded. | Retention classes; write-once; recorded disposal | NFR-028..032, 072–075; CTX-NFR-008 |
| NFR-RWB-009 | Accessibility | Every screen meets WCAG 2.2 AA and passes an automated and keyboard check. | No A/AA failure | Accessibility Standard; CTX-NFR-009 |
| NFR-RWB-010 | Scale | The document estate, decision log and ledger are sized for growth and read within the user wait. | 5.8M documents/2.8TB by 2031; 36GB log/ledger; case history <2s | NFR-007, 069, 070; CTX-NFR-010 |

## 6. Data requirements

| Entity / data product | Key fields | Classification | Source | Retention | Notes |
|---|---|---|---|---|---|
| DP01 Account and arrears | account_no, product_code, days_past_due, classification, balances, payments | [CONFIDENTIAL] / [SENSITIVE_FINANCIAL] | Core bank (ALS) via COLLINS | Per retention rule (DL26) | Freshness stamp on every row |
| DP02 Customer and party | party_id, role, tokenized national ID, contact points, consent, vulnerability/death/bankruptcy flags | [PII] / [RESTRICTED] | SCBPDM and core bank via COLLINS | Per retention rule (DL26) | National ID tokenized at load |
| DP03 Case and ownership | case_no, customer, product, stage, status, route, owner, queue, exposure band, deviation flags | [CONFIDENTIAL] | Workbench | Per retention rule (DL26) | Case ID RW-YYYY-NNNNNN |
| DP04 Treatment and offers | treatment_type, terms, approval level, outcome | [CONFIDENTIAL] | Workbench; ACE for plans | Per retention rule (DL26) | Plan timers |
| DP05 Contact and promises | interaction, channel, outcome, promise, consent | [PII] / [CONFIDENTIAL] | EFS before day 90; Workbench after | Per retention rule (DL26) | Ordered ledger |
| DP06 Collateral and assets | collateral, valuation, asset, listing, sale | [CONFIDENTIAL] | CCMS, SVAF, AMIS, RPS | Per retention rule (DL26) | Weekly/monthly today |
| DP07 Legal events and cases | notice, legal action, hearing, judgment, enforcement | [CONFIDENTIAL] | LIT; Workbench for instructions | Per retention rule (DL26) | Proof of delivery |
| DP08 Partner performance | partner, instruction, result, fee, scorecard | [CONFIDENTIAL] | Workbench; partner portal | Per retention rule (DL26) | Panel and conduct |
| DP09 Debt sale | lot, accounts, buyer, bid, award | [CONFIDENTIAL] | Workbench | Per retention rule (DL26) | Masked tape |
| DP10 Documents and extracted fields | document, type, fields, confidence, custody, retention | [PII] / [CONFIDENTIAL] | Workbench document hub | Per document retention class | Write-once for legal |
| DP11 Scores and route economics | score, expected return, sale price, success rate | [CONFIDENTIAL] | COLLINS | Per retention rule (DL26) | Model version |
| DP12 Decision log | decision, rule/model/agent/prompt versions, inputs, recommendation, approval, outcome | [CONFIDENTIAL] | Workbench | Per Compliance (DL26) | Append-only, hash-chained |
| DP13 Money and closure | payment, proceeds, write-off, post charge-off | [SENSITIVE_FINANCIAL] | Core bank/GL via COLLINS/file | Per retention rule (DL26) | Match and reconcile |
| DP14 Reference data | rules, limits, lists, roles, permissions, templates | [INTERNAL] | Workbench | Version history | Valid-from/valid-to |

## 7. Integration points

| ID | System | Type | Direction | Protocol | Timeout | Fallback | Derived from |
|---|---|---|---|---|---|---|---|
| INT-RWB-001 | COLLINS | Batch | Inbound | Daily file/ETL | Complete by 07:00 | Alert; case list marked stale; do not use stale data for a same-day decision | FR-RWB-002; NFR-013 |
| INT-RWB-002 | CCMS | File | Inbound | File load | Per load window | Age limit on valuation; exception queue | FR-RWB-002; R-02 |
| INT-RWB-003 | SVAF | File | Inbound | File load | Per load window | Age limit; exception queue | FR-RWB-002; R-02 |
| INT-RWB-004 | AMIS / RPS | File | Inbound | File load | Per load window | Exception queue | FR-RWB-002 |
| INT-RWB-005 | WIN | File | Outbound/inbound | File exchange | Per notice | Queue and retry; exception queue; proof missing blocks the period | FR-RWB-016; CTL-15 |
| INT-RWB-006 | Core bank (ALS) | Booking | Outbound | Officer action; next load confirms | Next load | Exception list; no silent booking | FR-RWB-002 |
| INT-RWB-007 | NSS / LINE OA | Message | Outbound | ACE notification path | Per send | Queue and retry; contact stop wins | FR-RWB-016 |
| INT-RWB-008 | Power BI / data lake | Batch | Outbound | Daily batch | Daily | Retry; stale report warning | FR-RWB-018 |
| INT-RWB-009 | Enterprise AI platform | API | Outbound | Private endpoint via tool gateway | 60s | Rule result; log fallback | FR-RWB-019; NFR-010 |

## 8. Business rules

| ID | Rule | Derived from | Applies to |
|---|---|---|---|
| BR-RWB-001 | An account at 90+ DPD that is not deceased, fraud, bankruptcy, an active restructure or an open dispute MUST become one recovery case. | R-UNI-16, R-UNI-17 | FR-RWB-004 |
| BR-RWB-002 | A case MUST have exactly one owner from allocation and one queue; a manual allocation is an exception with a reason. | R-UNI-18, R-UNI-19 | FR-RWB-005 |
| BR-RWB-003 | Allocation MUST use first match and MUST have a default row; a case with no matching row goes to the exception queue with a rule gap. | R-UNI-18, R-UNI-19 | FR-RWB-005 |
| BR-RWB-004 | Assignment MUST respect the caseload cap; when every owner is at the cap, the case goes to the overflow queue. | R-UNI-18, R-UNI-19 | FR-RWB-005 |
| BR-RWB-005 | A transfer MUST carry a reason code from the agreed list and MUST be logged with the rule ID and version. | R-UNI-20..24 | FR-RWB-006 |
| BR-RWB-006 | A service-level breach MUST raise an event and MUST NOT move the case by itself. | R-UNI-31 | FR-RWB-007 |
| BR-RWB-007 | A rule change MUST be validated, versioned and approved before it takes effect; rollback MUST restore the previous version. | R-UNI-38 | FR-RWB-008 |
| BR-RWB-008 | No action on a case MUST proceed unless its decision log entry is written. | R-UNI-39 | FR-RWB-017 |
| BR-RWB-009 | A personal field MUST be masked unless the role's masking profile allows it; every read MUST be logged. | PDPA Design | FR-RWB-013 |
| BR-RWB-010 | A legal document MUST be write-once inside its retention period; a new version is added instead of changing the old one. | CTL-12 | FR-RWB-014 |
| BR-RWB-011 | A notice period MUST start only from the proof-of-delivery date. | R-LIT-07, R-LIT-08; CTL-15 | FR-RWB-016 |
| BR-RWB-012 | A contact MUST NOT be made while a contact stop is in force; statutory notices continue. | R-UNI-04, R-UNI-10; CTL-16 | FR-RWB-016 |
| BR-RWB-013 | An agent or model write MUST pass the same permission checks as a person and MUST be logged with its version. | REQ-CWC-018; NFR-078 | FR-RWB-019 |
| BR-RWB-014 | A hard-coded threshold, limit, timer, queue, role, template or route is prohibited; the value MUST come from versioned reference data. | AGENTS.md §3 | FR-RWB-020 |
| BR-RWB-015 | The preparer of a decision MUST NOT approve it. | CTL-05 | FR-RWB-012 |
| BR-RWB-016 | A case MUST have one next action with an owner and a due date; a case with no next action is an exception. | REQ-WKM-012..016 | FR-RWB-010 |

## 9. Acceptance criteria

The full criteria are in the story files. The worked example `RWB-E1-020` (allocation and assignment
engine) is reproduced here as the pattern.

### AC-RWB-E1-020-1 — A new case is placed in the queue its row names

```gherkin
GIVEN a new case RW-2026-000201 with status "NEW", product group "MORTGAGE", region "BKK" and exposure band "B2"
AND allocation row "ALLOC-014" matches product group "MORTGAGE", region "BKK" and any exposure band, with target queue "MTG-BKK-CO"
WHEN the morning allocation run starts
THEN the system places the case in queue "MTG-BKK-CO"
AND the case team is "MTG-BKK" and the region is "BKK"
```

### AC-RWB-E1-020-4 — Every owner is at the cap

```gherkin
GIVEN U-01, U-02 and U-03 each hold 150 open cases
WHEN case RW-2026-000203 is placed in queue "MTG-BKK-CO"
THEN the system places the case in the overflow queue "MTG-BKK-OVF"
AND the case status stays "NEW" and no owner is set
AND the team manager of "MTG-BKK" receives the allocation summary with MSG-P3-011 and count 1
```

### AC-RWB-E1-020-5 — No allocation row matches

```gherkin
GIVEN a new case RW-2026-000204 with product group "SSME" and region "NE3" that matches no allocation row
WHEN the morning allocation run starts
THEN the system places the case in the exception queue "RWB-EXC"
AND the case status stays "NEW"
AND the system writes a decision log entry with final call "RULE_GAP"
AND the system publishes caseAllocationFailed with reason "NO_ROW_MATCHED"
AND the allocation summary carries MSG-P3-012 with count 1
```

### AC-RWB-E1-020-6 — Every allocation is logged

```gherkin
GIVEN case RW-2026-000205 matches row "ALLOC-014" and owner U-02 is below the cap
WHEN the case is placed in the queue and given an owner
THEN the system writes one decision log entry with rule ID "ALLOC-014", rule version "ALLOC-2026.11", queue "MTG-BKK-CO", owner U-02 and the inputs used
AND if the decision log write fails, the allocation is not made and the case stays "NEW" with no queue
```

### AC-RWB-E1-020-7 — A case with an open deviation is not allocated to a case owner

```gherkin
GIVEN a new case RW-2026-000206 with deviation_open = true
WHEN the morning allocation run starts
THEN the system places the case in the deviation handler queue "DEV-HANDLER" named by rule R-DEV-01
AND the system sets no case owner and the status stays "NEW"
```

## 10. Error handling

| Error ID | Scenario | Trigger | System behavior | User message | HTTP status |
|---|---|---|---|---|---|
| ERR-RWB-001 | A required load fails its control total | COLLINS/file load | Refuse the whole file; keep the previous data; alert; do not reconcile | MSG-P1-001 | N/A (batch) |
| ERR-RWB-002 | A case has no matching allocation row | Allocation | Exception queue; rule gap logged; `CaseAllocationFailed` | MSG-P3-012 | 200 with exception status |
| ERR-RWB-003 | Every owner is at the cap | Assignment | Overflow queue; no owner; summary | MSG-P3-011 | 200 |
| ERR-RWB-004 | Decision log write fails | Any action | Roll back the action; retry; alert | MSG-P7-001 | 503 |
| ERR-RWB-005 | A user requests a case outside their scope | Access check | Refuse; log; no data returned | MSG-P4-003 | 403 |
| ERR-RWB-006 | A personal field is requested without the masking right | Access check | Return masked; log | MSG-P4-004 | 200 masked |
| ERR-RWB-007 | A notice template is withdrawn | Notice generation | Hold generation; route to Legal | MSG-P6-003 | 409 |
| ERR-RWB-008 | A notice has no proof of delivery | Notice period | Do not start the period; task the owner | MSG-P6-004 | 200 with hold |
| ERR-RWB-009 | An agent does not answer in 60 seconds | Agent run | Use the rule result; log fallback | N/A | 200 |
| ERR-RWB-010 | A duplicate event or file arrives | Outbox/load | Idempotency key rejects the repeat; no double action | N/A | 200 |

The full message catalogue is the Error and Message Standard v3. Every validation returns the message
ID; do not invent wording.

## 11. Out of scope

- Collections before day 90 and decisions D1–D4.
- E2 queue and transfer screens, approval routing, steering dashboard, treatment record, notice
  approval and live deviation screening.
- E3–E8 settlement/deed in lieu booking, route decision, guarantees, litigation full, assets, debt
  sale, write-off and full administration.
- Partner portal full screens beyond the identities needed for later epics.
- Any change to ACE common module internals.

## 12. Open questions

| ID | Question | Owner | Needed by | Impact if unanswered |
|---|---|---|---|---|
| Q-RWB-001 | Is entry at 90 or 91 days past due? (DL16) | Risk with the ACE team | Before case creation | Entry rule and counts change. |
| Q-RWB-002 | Is one case per customer per product confirmed? (DL17) | Business lead | Before case creation | Case count and link model change. |
| Q-RWB-003 | Who owns the application and grants access? (DL01, DL02) | Product owner | Before access build | Access request and admin model change. |
| Q-RWB-004 | Which interfaces need same-day data? (DL06) | Solution architect | Before integration build | End-of-day default may not meet the need. |
| Q-RWB-005 | What are the availability, RPO and RTO targets? (DL11) | IT lead with Operational Risk | Before NFR test plan | Resilience tests cannot be baselined. |
| Q-RWB-006 | What are the retention periods? (DL26) | Compliance | Before retention build | Retention classes have no periods. |
| Q-RWB-007 | Which Jira project and issue keys? (CTX-GAP-023) | Product owner | Before backlog import | Traceability Jira column stays blank. |
| Q-RWB-008 | Are the Epic 1 story files v5 or the consolidated v7 canonical? (CTX-GAP-017) | Business analyst | Before per-story specification | A story-level run may use an older story. |
| Q-RWB-009 | Are the Thai labels approved? (DL10) | Business lead | Before E2 | English ships first. |
| Q-RWB-010 | Is the model endpoint approved? (DL33) | CTO with Enterprise AI | Before live agent | Agents stay in shadow. |

## 13. Traceability summary

| BRD ID | FR/NFR ID | US ID | AC ID | BR ID | Integration ID | Error ID | Status |
|---|---|---|---|---|---|---|---|
| BRD-RWB-001 | FR-RWB-001, FR-RWB-002, NFR-RWB-001, NFR-RWB-004 | RWB-E1-001..017, 064–068 | AC-RWB-001, 002 | BR-RWB-001 | INT-RWB-001..004 | ERR-RWB-001 | Draft |
| BRD-RWB-002 | FR-RWB-003, NFR-RWB-006 | RWB-E1-007, 047, 051, 056 | AC-RWB-003 | BR-RWB-014 | INT-RWB-001..009 | ERR-RWB-001, 010 | Draft |
| BRD-RWB-003 | FR-RWB-004..010, NFR-RWB-003, NFR-RWB-004 | RWB-E1-018..021, 028–031, 035, 042–045, 048 | AC-RWB-004..010 | BR-RWB-001..006 | INT-RWB-001 | ERR-RWB-002..004 | Draft |
| BRD-RWB-004 | FR-RWB-011..013, NFR-RWB-009 | RWB-E1-022, 037–039 | AC-RWB-011..013 | BR-RWB-009, 015 | — | ERR-RWB-005, 006 | Draft |
| BRD-RWB-005 | FR-RWB-014, FR-RWB-015, NFR-RWB-008, NFR-RWB-010 | RWB-E1-024..026, 032–033, 040–041, 049–050, 053–054, 057 | AC-RWB-014, 015 | BR-RWB-010 | INT-RWB-002..004 | ERR-RWB-001 | Draft |
| BRD-RWB-006 | FR-RWB-016 | RWB-E1-034, 046, 052, 055 | AC-RWB-016 | BR-RWB-011, 012 | INT-RWB-005, 007 | ERR-RWB-007, 008 | Draft |
| BRD-RWB-007 | FR-RWB-017, NFR-RWB-007 | RWB-E1-008, 027 | AC-RWB-017 | BR-RWB-008 | — | ERR-RWB-004 | Draft |
| BRD-RWB-008 | FR-RWB-002, FR-RWB-003 | RWB-E1-007, 056 | AC-RWB-003 | BR-RWB-014 | INT-RWB-006 | ERR-RWB-001 | Draft |
| BRD-RWB-009 | FR-RWB-018, NFR-RWB-003 | RWB-E1-013 | AC-RWB-018 | — | INT-RWB-008 | — | Draft |
| BRD-RWB-010 | FR-RWB-019, NFR-RWB-006 | RWB-E1-058..063 | AC-RWB-019 | BR-RWB-013 | INT-RWB-009 | ERR-RWB-009 | Draft |
| BRD-RWB-011..020 | FR-RWB-020, NFR-RWB-001..010 | E2–E8 stories (separate increments) | — | BR-RWB-014 | — | — | Programme-level; not in Epic 1 specification |

The full matrix, including the Epic 1 story crosswalk and the source-ID crosswalk, is
`requirement/Traceability_Matrix.md`.
