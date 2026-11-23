# RWB-P3-E1035-CON Case record view v1.1 with documents and history timeline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1035-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP14, DP15, DP18, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-013, FR-P3-019, FR-P3-020, FR-P3-021, FR-P3-030, FR-P3-031) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-035 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As **TechX (any team may pick up this story)**, I want **the v1.1 timeline contract of rwb-case: the item shape with its type, summary, actor and reference plus the transfer detail fields, the paged envelope with the total, the per-section state that lets one failed source degrade one section, and the nine contract tables**, so that **rwb-case, gateway-bff and the three owner services build the timeline panel against one published document on Day 1**.

The document is an additive minor version of the timeline operation first published by RWB-P3-E1023-CON: same path, same query parameters, same status codes, one new item shape, one new section state, one new page field. Nothing in the baseline is removed or renamed, so no consumer has to change (ASM-3636).

This story fixes the shape the APP story builds against and generates its fakes. It carries no build dependency and is Day-1 work.

### 2. Business rationale

The timeline is the only screen of the case record that merges four owners at once: rwb-case for the assignments, transfers and state, rwb-decision for the decision records, rwb-source-data for the contact ledger, rwb-document for the documents. Unless the merge shape, the order rule inputs, the actor field, the transfer detail and the partial-failure behaviour are fixed before the panel work starts, each caller invents a different item and the merge in gateway-bff breaks at every change.

The legacy contract carried the whole timeline in one class with a `by` string and no section state, because one module read four of its own tables. In the target three of the four sources are another service's contract, so the item must say what it could not read and the page must say which section failed. That is the whole change: a section state on the page, and the transfer detail fields the legacy story added for RWB-E2-016.

The document fixes no business value: the type order, the section timeout and the labels are named as parameters and reference data of rwb-case, so a change is data, not a new version.

### 3. Preconditions

- The service naming of Template and Rules §R4 is fixed for rwb-case: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The baseline of RWB-P3-E1023-CON is published: the timeline path, the query parameters `type`, `from`, `to`, `page` and `size`, the status codes and the shared error envelope.
- The legacy contract of RWB-E1-035 §12 and endpoint API-P3-003 of TSD P3 v3 Appendix T-A are the source of the operation and the item fields.
- The decision-record query of C RWB-P7-E1027-CON is named as the hook that fills the decision items. Its path and its field list are Not specified in the source documents (GAP-2211; ASM-3635).
- The interaction read and the paging of the ledger are Not specified in the source documents (GAP-0695; ASM-1242).
- The rwb-case login (DP-02) will exist with SELECT on schema `rwb_case`. The login name is Not specified in the source documents (GAP-0692; ASM-1239).
- No build dependency. Day 1.

### 4. Flow

1. TechX: takes the operation, the item fields and the detail fields from §12.1 and the legacy contract, and names the operation `getCaseTimeline`.
2. TechX: writes the `TimelineItem`, `TimelinePage` and `TimelineSection` schemas and keeps every baseline field name unchanged.
3. TechX: fixes the actor rule: `by` carries either a person reference or a rule ID with its version, and `actorType` says which.
4. TechX: fixes the section state: one entry per section with its state and, when failed, the MSG code; the page stays 200.
5. TechX: names the parameter and reference sources for the type order, the timeout, the page size and the labels, and fixes none of their values.
6. TechX: runs the OpenAPI 3.1 validator, the compatibility check against the baseline checksum and the contract linter.
7. TechX: generates the fakes of 12.8 and publishes them with the checksum to RWB-P3-E1035-APP and gateway-bff.
8. TechX: records the acknowledgements of gateway-bff, rwb-decision, rwb-source-data and rwb-document against the checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field of the item has no source value | The document carries the placeholder Not specified in the source documents (GAP-2211; ASM-3635) for the decision-record query and (GAP-0695; ASM-1242) for the ledger read; no value is invented | None | AC2, AC4 |
| X2 | The document removes or renames a baseline field | The compatibility check against the RWB-P3-E1023-CON checksum fails and the document is not published | None | AC5 |
| X3 | The document declares a write operation on the timeline path | The linter fails and the document is not published | None | AC5 |
| X4 | The section state is modelled as an error response | The linter fails: a failed section is a 200 with a section state, never a 4xx or 5xx for one source | None | AC3 |
| X5 | A consumer builds against a superseded checksum | The consumer fails the compatibility check against the published checksum | None | AC5 |
| X6 | The rwb-document or rwb-decision contract changes shape after publication | A new minor version is raised and the hook is re-pointed; the APP story is not changed in place | None | AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency and no table; it fixes the shape the panel and the edge build against |
| Negotiable | Schema names and field order are design choices; no business value is fixed here |
| Valuable | One published item and section shape removes the guesswork from the panel, the edge and the three clients |
| Estimable | One document, one operation, three schemas, one section state, five fakes |
| Small | Fits one sprint with its contract tests |
| Testable | The document is the test object; every criterion is checked by a linter or a contract test |

### 7. Acceptance criteria

```gherkin
Feature: Case timeline contract v1.1

  Background:
    Given the baseline timeline contract of rwb-case published by RWB-P3-E1023-CON with its checksum

  Scenario: AC1 The v1.1 document for the timeline operation (new, D-RCV-60)
    Given the OpenAPI 3.1 document is generated from the timeline baseline
    When the document is validated with an OpenAPI 3.1 validator and the contract linter
    Then it validates with no error
    Then it declares GET /api/recovery/case/v1/cases/{caseId}/timeline with operationId getCaseTimeline
    Then the operation carries the query parameters type, from, to, page and size, the 200 response, the error responses and the Case record R security requirement

  Scenario: AC2 The item and page schemas (new, D-RCV-60)
    Given the document is published with version v1.1
    When a consumer resolves TimelineItem
    Then it holds at, type, summary, by, actorType, reference and the transfer detail fields reasonCode, fromQueueCode, toQueueCode and ruleId
    Then actorType distinguishes a person from a rule, and a rule item carries its ruleId and the rule version in by
    Then TimelinePage holds the items, the page, the size and the total of the merged set
    Then every baseline field of RWB-P3-E1023-CON is present with the same name and type

  Scenario: AC3 The partial-result section state (new, D-RCV-60)
    Given the document is published
    When a section source fails or exceeds its budget
    Then the response is 200 with the items of the other sections and one TimelineSection entry per section
    Then the failed section entry carries the state failed and the MSG code MSG-P3-023 with the section name
    Then no field of a failed section carries an invented value

  Scenario: AC4 Values as data: the order, the timeout and the labels (new, D-RCV-60)
    Given the document is published
    When the type order, the section timeout, the page size and the transfer reason labels are looked up
    Then the document names parameter timeline.type.order, parameter caserecord.section.timeout.ms, the page size parameter and LOV-TRANSFER-REASON, LOV-DOC-TYPE and LOV-CHANNEL of rwb-case
    Then the document fixes no value for any of them

  Scenario: AC5 The read-only rule, versioning and checksum (new, D-RCV-60)
    Given the document is published
    When its path list is compared with the baseline and the compatibility check is run
    Then the timeline path carries GET only and no POST, PUT, PATCH or DELETE appears
    Then the version is v1.1 in the document and v1 in the path, and the change is additive against the baseline checksum
    Then the document carries its own checksum and the four consumer acknowledgements

  Scenario: AC6 The nine contract tables and the consumed hooks (new, D-RCV-60)
    Given the document is published
    When its §12 tables are compared with the service facts
    Then tables 12.1 to 12.9 are all present and none is empty
    Then the schema, REST base, topic and task queue match Template and Rules §R4 for rwb-case
    Then the decision-record, ledger and document hooks name their owner service, and every table named in 12.7 is owned by P3
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| CB1 | The document follows OpenAPI 3.1 and the naming of Template and Rules §R4: base `/api/recovery/case/v1`, schema `rwb_case`, topic `rwb.case.events.v1`, queue `rwb-case`, package `th.co.scb.ace.workbench.recovery.case` | R4; ADR-020 |
| CB2 | The document is additive over the RWB-P3-E1023-CON baseline: no field is removed or renamed, and the version 1.1 is a minor version inside major version 1 | ADR-020; §R8.2 |
| CB3 | One item shape serves every type; the type is a coded value and the order between types is a parameter, never a field of the schema | BR1 of RWB-P3-E1035-APP; DP-06 |
| CB4 | A failed section is data in a 200 response, never an error status; the section entry names the section and the MSG code | MSG-P3-023; §R7.2 s14 |
| CB5 | Every personal field of a contact item names its masking hook, and the operation states Case record R and the scope filter | CTL-09; the authorise guard of the service template |
| CB6 | The document fixes no business value: the order, the timeout, the page size and the labels are named as parameters and reference data of rwb-case | DP-06; DP-07 |
| CB7 | Every value a source does not give is a placeholder with its gap and assumption, never an invented value | Template and Rules §R9; GAP-2211 |

### 9. State transitions

None. A contract has versions, not case state. This story changes no case status and writes no row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX contract owner | Drafts and publishes the document, the fakes and the checksum |
| rwb-case service owner (P3) | Owns the document as the service contract; approves the operation and the item shape |
| rwb-decision owner (P7) | Owns the decision-record query the document consumes (C RWB-P7-E1027-CON) |
| rwb-source-data owner (P1) | Owns the interaction read the document consumes (DP-18) |
| rwb-document owner (P5) | Owns the documents-by-case operation the document consumes |
| gateway-bff owner (RWB-PLT-N001-CON) | Owns the composite route and acknowledges the page shape |
| Solution architect | Approves the additive versioning rule and the partial-result rule |
| Test and QA lead | Runs the contract tests and the baseline compatibility check |

### 11. Data

The document fixes shapes, not values. The schemas carry these fields, with the field IDs of the Logical Data Model and Data Dictionary v7:

| Block | Fields | Table or contract behind it | Owner |
|---|---|---|---|
| item | at, type, summary, by, actorType, reference, reasonCode, fromQueueCode, toQueueCode, ruleId | assignment and decision record, or the ledger, document and decision hooks | P3, P1, P5, P7 |
| item, assignment and transfer | assignee, assignedAt, endedAt, reason, ruleId, queueCode, transferReasonCode (DF-WRK-012 to DF-WRK-016, DF-WRK-039, DF-WRK-040) | assignment, queue | P3 |
| item, decision | decisionCode, ruleId, ruleVersion, approverUserId, finalCall, decidedAt (DF-DEC-003 to DF-DEC-005, DF-DEC-010, DF-DEC-012, DF-DEC-016) | the rwb-decision decision-record query | P7 |
| item, contact | occurredAt, channel, direction, contactResult, summary (DF-INT-004 to DF-INT-011) | the rwb-source-data interaction read | P1 |
| item, document | documentId, documentType, source (DF-DOC-001, DF-DOC-004, DF-DOC-005) | the rwb-document documents-by-case operation | P5 |
| page | items, page, size, total, sections | composed in rwb-case | P3 |
| section | name, state, messageCode | composed in rwb-case from the section outcomes | P3 |

No row is read or written by this story. The item field names of the legacy contract of RWB-E1-035 §12 (`at`, `type`, `summary`, `by`, `reference` and the added `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId`) are kept unchanged.

### 12. Contract

#### 12.1 REST operations provided

| Operation | operationId | Request | Response | Errors |
|---|---|---|---|---|
| GET /api/recovery/case/v1/cases/{caseId}/timeline | getCaseTimeline | Path caseId; query type, from, to, page, size | TimelinePage: items[], page, size, total, sections[] | 400, 401, 403, 404, 503 |

`TimelineItem` holds `at`, `type`, `summary`, `by`, `actorType`, `reference`, `reasonCode`, `fromQueueCode`, `toQueueCode` and `ruleId`; `TimelineSection` holds `name`, `state` (ok, failed, empty) and `messageCode`. The type order, the section timeout and the page size are parameters of rwb-case and the document fixes none of their values (AC4). Every operation states Case record R and scope applied.

#### 12.2 REST operations consumed

| Operation | Owner | In the document as |
|---|---|---|
| The decision-record query of the rwb-decision contract (C RWB-P7-E1027-CON) | rwb-decision (P7) | The decision and state-change items and the creation item. Path and field list Not specified in the source documents (GAP-2211; ASM-3635) |
| The interaction read of the rwb-source-data contract (DP-18) | rwb-source-data (P1) | The contact items. Path and paging Not specified in the source documents (GAP-0695; ASM-1242) |
| GET /api/recovery/document/v1/cases/{id}/documents | rwb-document (P5) | The document items |
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | The scope hook of the operation |

#### 12.3 Events published

None. A read contract publishes no event; the AC-READ access record goes to the rwb-access access log through its contract.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None. The document describes a synchronous read only; CaseWorkflow on task queue `rwb-case` is out of its scope.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table | Schema | Owner | In the document |
|---|---|---|---|
| assignment | rwb_case | P3 | The assignment and transfer items and their detail fields |
| recovery_case | rwb_case | P3 | case_no and the current status in the item reference |
| queue | rwb_case | P3 | fromQueueCode and toQueueCode |
| lov_value | rwb_case | P3 | The labels of the coded item values |
| reference_row | rwb_case | P3 | LOV-TRANSFER-REASON, LOV-DOC-TYPE, LOV-CHANNEL |
| reference_version | rwb_case | P3 | The version in force on the read date |
| parameter_catalog | rwb_case | P3 | timeline.type.order, caserecord.section.timeout.ms, the page size |
| parameter_value | rwb_case | P3 | The values in force on the read date |

The service also owns case_account, case_party, case_entry_exclusion, task, queue_member and queue_measure, which this document does not describe.

#### 12.8 Contract fakes

| Fake | Generated from | Owner | Used by |
|---|---|---|---|
| rwb-case timeline fake | This document, with its checksum | P3 | RWB-P3-E1035-APP, gateway-bff |
| rwb-decision fake | The decision-record query of C RWB-P7-E1027-CON; path Not specified in the source documents (GAP-2211; ASM-3635) | P7 | AC2, AC3, AC6 |
| rwb-source-data fake | The interaction read line of the P1 contract; path Not specified in the source documents (GAP-0695; ASM-1242) | P1 | AC3, AC6 |
| rwb-document fake | The documents-by-case operation of the P5 contract | P5 | AC2, AC3 |
| rwb-access fake | The authorise and masking contract | P4 | AC5 |

#### 12.9 Call-type summary

| Call type | In this contract |
|---|---|
| REST | Yes. One GET operation provided under `/api/recovery/case/v1`; the consumed operations of 12.2 are declared as hooks; one hop, 2 s timeout |
| Kafka | None |
| Temporal | None |
| File | None |

### 13. Solution plan

**Package.** The document is held with the service contract of rwb-case, under Java package `th.co.scb.ace.workbench.recovery.case`; it is the input to the code generator of the platform contract library.

**Deliverables**

| Deliverable | Content |
|---|---|
| OpenAPI 3.1 document v1.1 | The timeline operation, the three schemas, the security scheme and the shared error envelope |
| Compatibility baseline | The RWB-P3-E1023-CON checksum and the additive-diff report |
| Contract linter rules | Read-only rule, additive-only fields, the section state as a 200, the nine tables present |
| Fakes | The rwb-case timeline fake plus the four fakes of 12.8 |
| Checksum register | The published document with its checksum and the four consumer acknowledgements |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

As a CON story it carries no build dependency: the H rows above are the pattern rows of the vehicle, recorded here for the trace, and they are taken by the APP story that builds.

**Build steps**

1. Fix the operation and the operationId from 12.1; diff every field against the baseline document.
2. Write `TimelineItem`, `TimelinePage` and `TimelineSection`; check every field name against section 11 and the legacy contract.
3. Add the actor rule, the transfer detail fields and the section state; add the masking hook to every contact item field.
4. Name the parameter and reference sources and fix no value.
5. Fix version v1.1, the media type, the identifier format and the read-only rule.
6. Run the validator, the linter and the additive compatibility check; a removed baseline field or a write operation fails the build.
7. Generate the fakes of 12.8 and publish them with the checksum.
8. Collect the gateway-bff, rwb-decision, rwb-source-data and rwb-document acknowledgements.

**Done when.** The document validates, the linter and the additive check pass, the fakes are published with the checksum and the four acknowledgements are recorded.

**Contract tests.** Schema validity, the additive diff against the baseline checksum, the section state on a 200, the error envelope on every status code, the masking flag on every contact field and the completeness of the nine tables.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session or an expired session | You are not signed in. Sign in to continue. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P3-023 | One source does not answer | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P3-024 | The panel has nothing to show | Nothing is recorded in {section} yet. |

Validation rules the document must satisfy: OpenAPI 3.1 valid; the operation has an operationId in the service namespace; the path is under `/api/recovery/case/v1` and carries GET only; every contact field carries a personal-data flag and a masked source; every error response carries the shared envelope with a code, a message and a trace identifier; `page` is 0 or more and `size` 1 to 100, and a value outside the range is 400; a failed section is a section state on a 200 and never an error status.

### 15. Screens and states

None. This story delivers no screen. It fixes the data the SCR-03 timeline panel shows in each state: Loading (the page shape with empty item and section arrays), Read only (items in time order with actor and reference; a new case shows its creation item), Empty (a section with no item and MSG-P3-024), Error (the section entry with state failed and MSG-P3-023 while the page stays 200, MSG-P4-003 out of scope, MSG-P4-002 without the right). The screen is built by RWB-P3-E1035-APP as the gateway-bff composite route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1035-CON-01 | AC1 | Contract | The OpenAPI 3.1 document, validated by the OpenAPI validator and the linter |
| TC-P3-E1035-CON-02 | AC2 | Contract | The three schemas resolved with the fake, and the baseline field diff |
| TC-P3-E1035-CON-03 | AC3 | Contract | One source timing out and one source failing, answered from the fake |
| TC-P3-E1035-CON-04 | AC4 | Component | The parameter and reference names, checked for an absent literal value |
| TC-P3-E1035-CON-05 | AC5 | Contract | The path list scanned for write methods, and the additive check against the baseline checksum |
| TC-P3-E1035-CON-06 | AC6 | Component | The nine tables, the four consumed hooks and the service naming of §R4 |

### 17. Guardrails

- No business value in the document: the type order, the timeout, the page size and the labels are named as sources, never fixed here.
- No personal data in the examples: every example party is synthetic and no example carries a clear contact value.
- No PII in events, workflow inputs or logs, and none in the contract examples.
- The document declares no foreign table and no cross-schema read; ACE data behind the contact items is named only through the rwb-source-data contract (DP-01, DP-18).
- The ledger is declared through its owner's read, never as a table (DP-18).
- The operation states Case record R and the scope; a hook that hides the scope fails the linter.
- A failed section is data on a 200 response, never an error status that would hide the rest of the page.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | Story | Test cases |
|---|---|---|---|---|
| REQ-CWC-016 | Every workflow event with its rule ID and version | FEAT-ACA-12 | RWB-P3-E1035-CON | TC-P3-E1035-CON-02, TC-P3-E1035-CON-03 |
| REQ-OCC-007 | Contact history and documents on the case view | FEAT-ACA-12 | RWB-P3-E1035-CON | TC-P3-E1035-CON-02, TC-P3-E1035-CON-06 |
| REQ-WKM-003 | A manual transfer carries its reason | FEAT-ACA-12 | RWB-P3-E1035-CON | TC-P3-E1035-CON-02, TC-P3-E1035-CON-04 |
| REQ-ACA-005 | Personal data masked by role | FEAT-ACA-12 | RWB-P3-E1035-CON | TC-P3-E1035-CON-05 |

| Trace | Reference |
|---|---|
| Legacy key | RWB-E1-035, disposition Split (rework) |
| Baseline | RWB-P3-E1023-CON (timeline operation, page and size, error envelope) |
| Legacy contract source | RWB-E1-035 §12; TSD P3 v3 Appendix T-A API-P3-003 |
| Consumed by | RWB-P3-E1035-APP, gateway-bff composite route (RWB-PLT-N001-CON) |
| Contract dependencies | None. The P7, P1, P5 and P4 contracts are referenced, not depended on for the build |
| Pattern rows | DP-01, DP-03, DP-06, DP-07, DP-11, DP-13, DP-14, DP-15, DP-18, DP-19 |
| Gaps and assumptions | GAP-2211, GAP-0692, GAP-0695; ASM-3635, ASM-3636, ASM-1239, ASM-1242 |

### 19. Out of scope

- The timeline panel implementation and its screen states (RWB-P3-E1035-APP).
- The full timeline screen SCR-04 with filters and queue history (RWB-P3-E2016-APP).
- The read-only case header, the accounts, the parties and the contact history block (RWB-P3-E1023-CON).
- The write operations of rwb-case: transfer, legal hold, task update, queue placements and reference loads.
- The decision-record query itself, which belongs to rwb-decision (C RWB-P7-E1027-CON).
- The physical schema and the Flyway migration, which belong to the DB stories and RWB-PLT-E1044-CON.
- The gateway-bff composite route itself, which belongs to RWB-PLT-N001-CON.
