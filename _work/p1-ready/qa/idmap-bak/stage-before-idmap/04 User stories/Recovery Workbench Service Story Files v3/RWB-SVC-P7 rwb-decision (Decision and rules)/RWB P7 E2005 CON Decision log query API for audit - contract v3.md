# RWB-P7-E2005-CON Decision log query API for audit - contract

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E2-005 for rwb-decision. The audit read contract is published on Day 1; the implementation is RWB-P7-E2005-APP and the end-to-end proof is RWB-ITG-E2005-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 9 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E2005-CON |
| Work type | CON (Contract) |
| Size | Not specified in the source documents (DOR-RWB-P7-E2005-CON-16); the squad sizes it at refinement |
| Contract version | v1 (base path /api/recovery/decision/v1) |
| Readiness decisions | RD-P1-004 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Open decisions | DL10 (open); assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 confirmed by the programme directive |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-003, FR-P7-004, FR-P7-012, FR-P7-013, FR-P7-014, FR-P7-015, FR-P7-016, FR-P7-036) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **tech lead of rwb-decision**, I want **the published contract baseline of the two audit reads of the central decision ledger — `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/decision-log/{entryId}` on base `/api/recovery/decision/v1` — with their query parameters, the paging shape, the answer resource, the read-only rule, the authorisation element, the error envelope and its message IDs, the access-record envelope, the fakes and the drift test**, so that **the app story of this key and the audit consumers build on Day 1 against one fixed, testable read contract, and a filter, a field, a hash column or a message code can never drift between rwb-decision, rwb-access, rwb-case and the audit screens without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The audit read shows why the baseline has to be fixed before the build. One question reaches three owners: rwb-access for the right and the scope that decide which entries may be returned at all, rwb-case for the two limits and the three lists that decide what a valid filter is, and rwb-case's rule change audit report for the figure the answer is reconciled to. One answer carries eleven elements that the screen, the CSV export, the incident of a chain mismatch and the access log of rwb-access all read, and the two of them that make the answer trustworthy — the previous hash and the entry hash — have to mean the same thing in the contract as they do in the store.

The baseline also fixes the naming the checks require: schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` for the service's own events, task queue `rwb-decision` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.decision`. It records that the two reads are the only write-free capability of the service, that the access record of a query leaves through the shared topic `rwb.decision-record.v1` and not through the service's own topic, and that the ingest of that topic into the ledger is a different story.

Three prohibitions are as much part of the baseline as the shapes. The read never changes an entry: `decision_log_entry` is append-only, the service login holds SELECT on it, and no operation of this contract offers a write, a correction or a delete — a correction is a new record that names the one it corrects (REQ-DRI-002). The read never hides an entry: an entry that fails the chain check is returned with `chainVerified` false and the warning, because an audit answer that drops the one row that matters is worse than an answer that flags it (NFR-035). And the read never reaches the data lake: the legacy analysis of the lake copy is retired under DP-17 and the reporting read model takes the events instead (GAP-1244).

The legacy acceptance criteria are not copied here. AC1 to AC10 of RWB-E2-005 stay with RWB-P7-E2005-APP, which owns the behaviour, and their end-to-end copies belong to RWB-ITG-E2005-ITG; every criterion in section 7 is new (D-RCV-60) and tests only the artefact in this title. The fakes are the Day-1 unblocker: the app story and the harness build the query, the scope refusal, the chain verdict, the export and the empty page before the ledger holds a single migrated row (Template and Rules §R5.4 class C).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the schema, topic, event and path names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The operations and their owners come from the Ownership Map only: `GET /decision-log` and `GET /decision-log/{entryId}` are P7's, and `POST /authorise` of rwb-access, the parameter and list reads of rwb-case and the rule change audit read are consumed and never declared as provided.
- The ledger store baseline of RWB-P7-E1008-CON and RWB-P7-E1008-APP fixes the table `decision_log_entry`, the canonical form and the three chain columns; this contract reads them and changes none of them.
- The decision-record library contract of RWB-PLT-E1027-CON fixes the access-event shape this baseline uses for the AC-READ and AC-EXPT record, and the shared topic `rwb.decision-record.v1`.
- The two limits are parameters and the three lists are reference rows: the contract refers to them and holds no value of its own (DP-06, DP-07).
- The field list of the answer beyond the legacy names, the element that carries the warning and the two message identifiers of the paths the legacy story leaves unnamed are Not specified in the source documents (GAP-1248; ASM-2212).
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).
- No production data is used in any example, schema or fake: every case number, user identifier, rule version and hash is synthetic.

### 4. Flow

1. Draft the rwb-decision OpenAPI 3.1 fragment of the two audit reads and the `DecisionLogEntry` and `DecisionLogPage` components, under the base `/api/recovery/decision/v1`.
2. Fix the ten query parameters and their validation, the two limits as parameters and the three lists as reference rows, so the contract names them and holds no value.
3. Fix the answer resource element by element, with the eleven core elements of AC2 and the legacy elements the criteria of the app story read.
4. Fix the read-only rule: the two operations are the only two, no write operation is declared, and the store contract behind them offers SELECT only.
5. Fix the authorisation element: the Decision log right R with the scope applied, the authorise contract of rwb-access behind it and the refusal path of the AC-DENY record.
6. Map every failure to the error envelope and one message ID, one condition per row, including the warning that travels with a 200 answer.
7. Record the access-record envelope this capability declares and the two consumed lists and report it relies on, and record that the contract declares no workflow and no Schedule.
8. Publish the contract fakes of section 12.8 and the drift test that fails a build in which a fake and the document disagree.
9. Tag the baseline and hand it to RWB-P7-E2005-APP, the audit consumers named in AC5 and the harness RWB-ITG-E2005-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A shape is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC7 |
| X2 | A filter is added, removed or re-typed, or the paging shape changes | The contract test fails and the change is a new major version of the read | None | AC3, AC7 |
| X3 | A write operation, a correction operation or a delete appears on the audit base | The absence test fails the build; the read is read-only | None | AC4 |
| X4 | The authorisation element is dropped, or a read is declared without the scope applied | The security lint fails the build and names the operation | MSG-P4-002 | AC5 |
| X5 | A condition maps to two message IDs, or a message ID is reworded | The mapping test fails the build | None | AC6 |
| X6 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |
| X7 | A personal value appears in an example, an answer or a fake | The scanner fails the build and names the field | None | AC9 |
| X8 | An element is named by no source — the field list beyond the legacy names, the warning element or the two unnamed message paths | The element is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1248; ASM-2212) | AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the store contract of the same service, the library contract of the platform and the Ownership Map only |
| Negotiable | The element list beyond the legacy names and the two unnamed message paths are settled with the consumers; the two operations, the filters, the paging shape, the read-only rule and the message IDs are fixed by the target architecture and the legacy story |
| Valuable | Unblocks the app story of this key, the audit screens and the harness on Day 1, and freezes what an audit answer means before a row is migrated |
| Estimable | One document fragment, two operations, two components, nine contract tables, six fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: contract baseline of the audit reads of the central decision ledger

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-decision REST base is /api/recovery/decision/v1 and its own topic is rwb.decision.events.v1
    Given no production data is used in any example, schema or fake

  Scenario: AC1 The OpenAPI document declares the two audit reads and nothing else (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-decision is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /decision-log with no request body and the DecisionLogPage answer, answering 200
    Then it declares GET /decision-log/{entryId} with no request body and the DecisionLogEntry answer, answering 200 and 404
    Then both operations sit under the base /api/recovery/decision/v1 and name rwb-decision as their owner
    Then neither operation declares an Idempotency-Key header, because both are reads
    Then the fragment declares no POST, no PUT, no PATCH and no DELETE under the audit base

  Scenario: AC2 The answer resource carries the eleven audit elements and the legacy elements (new, D-RCV-60)
    Given the DecisionLogEntry component declared in the document
    When its properties are compared with the ledger table of the service
    Then it carries the entry id, the decision code, the rule and the rule version, the case, the subject reference, the data date, the actor role, the previous hash, the entry hash, the sequence and the created time
    Then it carries the legacy elements the criteria of RWB-E2-005 read: approverUserId, approvalLevel, finalCall, inputsRef, chainVerified and the message codes
    Then entryId, decisionCode, caseId, chainSeq, prevHash, entryHash and decidedAt are required, and the other elements are optional because an access event has no case and no approver
    Then chainVerified is required on every returned entry and is never null
    Then a hash element is a 64-character hexadecimal string, and the contract states that the first entry of the chain carries 64 zeros as its previous hash
    Then the subject reference is the case ID where the entry has a case and the filter reference where it does not
    Then the resource carries no ledger row body, no inputs snapshot, no rule source, no approver name and no free text that is not masked
    Then the actions and outcome columns of a hand-over entry carry their history items in a fixed order, and the tests assert the counts, the source system and the action codes only (GAP-2462)

  Scenario: AC3 The filters, the paging shape and the export media type are fixed (new, D-RCV-60)
    Given the query parameters declared on GET /decision-log
    When they are compared with RWB-P7-E2005-APP and with the owners of the two limits and of the three lists, rwb-case
    Then the parameters are caseId, caseIds, decision, ruleId, ruleVersion, approver, from, to, page and size
    
    Then caseIds is a comma-separated list of at most rwb.decision.query.max-cases identifiers and the parameter is read, never written in code
    Then size is an integer from 1 to rwb.decision.query.max-size and page starts at 1, and both limits are parameters of rwb-case
    Then from and to are business dates and a from after a to is refused with 422 and MSG-GEN-003 naming from
    Then decision is an element of LOV-DECISION, approvalLevel of LOV-APPROVAL-LEVEL and the scope of LOV-SCOPE, each read as reference data
    Then the answer carries items, page, size, total and messageCodes, and total counts only the entries the caller may see
    Then the same operation declares the media type text/csv for the export of the full result with a header row and chainVerified on every row
    Then the document states that the page order is Not specified in the source documents (GAP-2464) and that a population of cases is grouped by case and ordered by chain_seq inside each case

  Scenario: AC4 The audit read is read-only and no operation can change an entry (new, D-RCV-60)
    Given the operations, the store contract and the security element of the document
    When the read-only rule is reviewed against the ledger
    Then the document declares exactly two operations, both GET, and no operation that writes, corrects, re-seals or deletes an entry
    Then it states that the service login holds SELECT on decision_log_entry and no write grant
    Then it states that a correction is a new record naming the entry it corrects, written through the decision ledger of the owning service and never through this contract
    Then it states that a read changes no entry, no chain sequence and no hash, and that the append-only rule of the store is never disabled by a reader
    Then the absence test fails a build that adds a write operation to the audit base

  Scenario: AC5 The authorisation element names the right, the scope and the authorise contract (new, D-RCV-60)
    Given the security section of the two operations
    When it is compared with the authorise contract of rwb-access
    Then both operations declare the Decision log capability area with right R and the scope applied, and the right is called the right of the read, with both names recorded: Rules and parameters R (TSD) and Platform administration R (legacy story)
    Then the document names the authorise contract RWB-P4-E1037-CON behind the guard library RWB-PLT-E1037-CON as the only source of the right and the scope
    Then the document states that the scope is applied to the case of each entry inside the query, so no entry outside the scope is returned or counted
    Then the authorise answer carries the scope kind and the case-scope predicate
    Then a caller without the right is refused with 403 and MSG-P4-002, and the refusal is recorded with decision code AC-DENY, area DECISION_LOG and right R
    Then no role name and no scope value is written in the document as a constant
    Then the AC-DENY record is written locally through the decision-record library and relayed on rwb.decision-record.v1, which the access log of rwb-access (RWB-P4-E1039-CON) reads for its view, and no read path of this contract calls rwb-access to write (GAP-1250; ASM-2214)

  Scenario: AC6 The error envelope maps one message ID per condition (new, D-RCV-60)
    Given the error responses declared for the two operations
    When each condition is compared with the message catalogue
    Then the envelope is the platform error envelope with the status, the message ID and the message text, and no second envelope is introduced
    Then 403 answers MSG-P4-002, 404 answers MSG-P4-003 for an entry that is absent or outside the scope, and 422 answers MSG-GEN-003 for a reversed period and MSG-GEN-002 for a size or a case list outside its limit
    Then 503 answers MSG-P7-003 when the access record cannot be written and MSG-GEN-006 when the ledger does not answer
    Then an entry that fails the chain check is not an error: the answer is 200 with chainVerified false and MSG-P7-012 in messageCodes
    Then the chain mismatch incident goes to the Compliance queue, which is read from platform configuration
    Then the status for a caller with no session is 401 and its message identifier is the platform one, which no source read here names (GAP-1249; ASM-2213)
    Then no condition maps to two message IDs and no message ID is reworded

  Scenario: AC7 Additive change stays in major version 1 and a breaking change raises version 2 (new, D-RCV-60)
    Given the versioning rule of the document
    When a change is proposed to a published element
    Then an added optional element, an added optional filter and an added message code keep major version 1 and are accepted by the registry in BACKWARD mode
    Then a removed, renamed or retyped element, a changed paging shape, a removed filter or a changed meaning of a hash element raises major version 2 and a new path version
    Then v1 is never edited in place and stays readable for the consumers that pin it
    Then a consuming service pins a published version and raises a change request rather than a private variant
    Then the document states that the ledger store and the canonical form behind the hashes are not versioned by this contract and are pinned by RWB-P7-E1008-CON

  Scenario: AC8 The six fakes answer the document and the drift test fails a build on any difference (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the six fakes against the two operations
    Then the authorise fake answers RW-AUDIT with scope ALL, RW-CASEOWN with scope OWN and a refusal with MSG-P4-002
    Then the ledger fixture answers the six entries of case RW-2026-000123 at chain_seq 101, 155, 160, 230, 231 and 402, one entry with chainVerified false for chain_seq 230, and an empty page
    Then the parameters and reference-data fakes answer max-size 500, max-cases 500, LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-SCOPE
    Then the rwb-case fake answers the three cases of the OWN caller, the rule change audit report with 200 decisions for LIT-2026.12 and a case outside the caller's scope
    Then the access-log fake answers the AC-READ and AC-EXPT records with their filter reference and row count
    Then the decision-record fake answers a healthy access record, a refusal with MSG-P7-009 and an unavailable store
    Then the drift test of the app story fails on any difference from sections 12 and 13

  Scenario: AC9 A personal value in an example, an answer or a fake fails the build (new, D-RCV-60)
    Given the examples, the answers and the fakes of the document
    When the personal-value scanner runs over them
    Then any personal value found fails the build and the scanner names the field
    Then no production data is used in any example, schema or fake

  Scenario: AC10 An element named by no source is published as the working read of its assumption (new, D-RCV-60)
    Given an element that no source names
    When the document is reviewed against the sources
    Then the element is published as the working read of its assumption and the gap stays open
    Then the document marks the element with its gap and its assumption and with no other status

  Scenario: AC11 Event names follow the service rule and the access record is local (new, D-RCV-60)
    Given the event names and the access record of the document
    When they are compared with the naming rule and the shared decision-record topic
    Then the service's own event names are rwb.<short>.<Event>.v1 on rwb.<short>.events.v1, with retry and .dlt topics
    Then the access record of a query and of an export is written by the local decision-record library on rwb.decision-record.v1 and is never a new event of this service

  Scenario: AC12 The ledger is owned by P7 and no data-lake or reporting copy is declared (new, D-RCV-60)
    Given the tables and copies named by the document
    When they are compared with the Ownership Map rows
    Then decision_log_entry in rwb_decision is declared as the P7 ledger and no other owner's table is declared as created here
    Then no data-lake copy and no reporting copy is declared, and the reporting read model takes the events

  Scenario: AC13 No business value is fixed in the contract (new, D-RCV-60)
    Given the limits, the decision codes, the approval levels, the scope values and the performance target
    When the document is reviewed for fixed values
    Then the limits, the decision codes, the approval levels, the scope values and the performance target are data or service configuration and the contract holds no value for them; the first-page target is carried as a service configuration parameter whose value is Not specified in the source documents (GAP-1247), tested in SIT, and DL11 confirms it before the wave 2 exit
```

These thirteen criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P7-E2005-APP. The legacy criteria of RWB-E2-005 are owned elsewhere: AC1 to AC10 by RWB-P7-E2005-APP, with their end-to-end copies in RWB-ITG-E2005-ITG. Every identifier in the criteria — the base, the two paths, the two limits, the message IDs, the codes and the chain values — comes from the legacy story, the Ownership Map or the architecture, character for character. Per-run evidence for the decision-log audit query harness is one report per story and business date, with one row per criterion, seam, answering service or fake, observed value and result, kept to the release record. The integration lead agrees the harness repository, the SIT and UAT environments and the seeding order with QA; the gate accepts a wave when every owned criterion is green with the three I stories in place; the platform edge owner publishes the gateway-bff composite query route path and merge order before section 15 runs (ASM-B-ITG-W2-01-E2005-1).

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/decision/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes | AC1 |
| BR2 | The service's own event names are `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`, with retry and `.dlt` topics; the shared decision-record topic is named only as the library's | DP-14; Template and Rules §R4 | AC11 |
| BR3 | The two audit reads are the only operations of this contract, both GET, both read-only, and no write, correction or delete is declared on the audit base | REQ-DRI-002; ADR-009; FSD P7 A2.1 | AC1, AC4 |
| BR4 | The answer carries the eleven audit elements and the legacy elements, and an entry that fails the chain check is returned flagged with MSG-P7-012 and never dropped | REQ-DRI-003; NFR-035; legacy AC5 | AC2, AC6 |
| BR5 | The right and the scope are read from the authorise contract of rwb-access through the guard library, and the scope is applied to the case of each entry | DP-08; RWB-P4-E1037-CON; legacy BR2 | AC5 |
| BR6 | The two limits are parameters and the three lists are reference rows of rwb-case; the contract names them and holds no value | DP-06; DP-07; RWB-P3-E1042-CON; RWB-P3-E1043-CON | AC3 |
| BR7 | Error responses use one envelope and one message ID per condition; the message texts of the legacy story are copied unchanged | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC6 |
| BR8 | A schema change is additive within a major version, and a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) | AC7 |
| BR9 | The access record of a query and of an export is a local decision record on `rwb.decision-record.v1`; it is never a new event of this service | DP-03; RWB-PLT-E1027-CON | AC11, AC5 |
| BR10 | The ledger is `decision_log_entry` in `rwb_decision` and it is P7's; `delegation_limit` is P4's, `parameter_catalog` and `reference_row` are P3's, and none of them is declared as created here | DP-01; Ownership Map rows | AC12 |
| BR11 | No data-lake copy and no reporting copy is declared: the legacy lake analysis is retired and the reporting read model takes the events | DP-17; ADR-018; GAP-1244 | AC12 |
| BR12 | No business value is fixed in the contract: the limits, the decision codes, the approval levels, the scope values and the performance target stay data or service configuration | Template and Rules §R7.2 s17 | AC13 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the answer resource, the filters and the error mapping are described | In review |
| In review | Consumer sign-off | The app story of this key, the harness and the rwb-access and rwb-case owners accept the document and the fakes | Baselined |
| Baselined | Additive change | An optional element, an optional filter or a message code is added within major version 1 | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, or the paging shape changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A write operation appears on the audit base | The absence test of AC4 fails | In review |

The ledger itself has no state this contract can move: an entry is appended by its writer and sealed by the daily check, and a reader changes neither. The chain verdict of an answer — verified or flagged — is computed per answer and never stored (BR4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-decision | Owns the OpenAPI fragment and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the correction of an Ownership Map row |
| Consuming teams (the app story of this key, the harness, the audit screens and the rwb-access and rwb-case owners) | Review and sign off the parts they consume |
| RW-AUDIT, internal audit | The role the baseline names on both reads: Decision log R with scope ALL |
| RW-COMPLY, Compliance and PDPA officer | A reading role with scope ALL and the receiver of the chain-mismatch incident |
| RW-CASEOWN and other roles holding Decision log R | A reading role limited to the cases in their scope |
| RW-PHONECOL and roles without Decision log R | Refused by the contract, with MSG-P4-002 |
| Platform library owner | Owns the CloudEvents envelope, the error envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data element is declared in an answer or a fake |

The per-service login behind the security scheme is not part of this baseline; the document names the scheme "the rwb-decision login (DP-02)". The authorisation decision itself is enforced at gateway-bff under RWB-PLT-N001-CON and the authorise contract of RWB-P4-E1037-CON, and is not implemented here. No personal name, no e-mail address and no credential appears in the document, an example or a fake: where a caller must be named, the example uses a user identifier only.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Query parameters | Not specified in the source documents (DOR-RWB-P7-E2005-CON-7) | `caseId`, `caseIds`, `decision`, `ruleId`, `ruleVersion`, `approver`, `from`, `to`, `page`, `size`; the two limits are parameters and the three lists are reference rows, never constants (GAP-1248; ASM-2212) |
| DecisionLogEntry | DF-DEC-001 to DF-DEC-018, DF-DEC-028, DF-DEC-029 and DF-DEC-030 | entryId, decisionCode, ruleId, ruleVersion, caseId, subjectRef, dataDate, actorRole, prevHash, entryHash, chainSeq, decidedAt, approverUserId, approvalLevel, finalCall, inputsRef, chainVerified, messageCodes; the fields behind them are DF-DEC-001 to DF-DEC-018, DF-DEC-028, DF-DEC-029 and DF-DEC-030 |
| DecisionLogPage | Not specified in the source documents (DOR-RWB-P7-E2005-CON-7) | items, page, size, total, messageCodes; `total` counts only the entries inside the caller's scope |
| Export | Not specified in the source documents (DOR-RWB-P7-E2005-CON-7) | The same rows as `text/csv` with a header row and `chainVerified` on every row; the file name, the encoding and the column order are Not specified in the source documents (GAP-1242; ASM-2206) |
| Access record | Not specified in the source documents (DOR-RWB-P7-E2005-CON-7) | Decision code AC-READ or AC-EXPT, the filter reference, the row count, the actor reference, the decided-at time, the chain sequence and the entry hash (RWB-PLT-E1027-CON) |
| Error body | Not specified in the source documents (DOR-RWB-P7-E2005-CON-7) | The status, the message ID and the message text of the platform envelope; no case fact and no entry body |
| Personal data | Not specified in the source documents (DOR-RWB-P7-E2005-CON-7) | None in the answer as a declared element: a user identifier, a case identifier, a code, a version, a hash and a date. The legacy free-text fields `recommendation`, `actions` and `override_reason` are declared as masked-before-return and never as raw text |

The record shape is the one place where a ledger value could leak into the contract, so the document fixes that an answer carries codes, identifiers, versions, hashes and dates, and never the inputs snapshot, the rule source or an unmasked free-text field.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-decision (P7); base `/api/recovery/decision/v1`.

| ID | Method | Path | Documented shape | Access |
|---|---|---|---|---|
| API-P7-006 | GET | `/decision-log` | Query parameters of AC3; answer 200 with DecisionLogPage; media type text/csv for the export; errors 401, 403, 422, 503 | Decision log R, scope applied; no Idempotency-Key |
| API-P7-007 | GET | `/decision-log/{entryId}` | No request body; answer 200 with DecisionLogEntry; errors 401, 403, 404, 503 | Decision log R, scope applied; no Idempotency-Key |

The answer carries `chainVerified` on every entry and `messageCodes` on the page, which is where MSG-P7-012 travels with a 200 status. The field list beyond the elements of AC2 and the legacy names, the CSV column order and the page-size default are Not specified in the source documents (GAP-1248; ASM-2212).

#### 12.2 REST operations consumed

| Method and path | Owner | Contract | Use in the baseline |
|---|---|---|---|
| POST authorise read (role, scope, DoA) | P4 rwb-access | RWB-P4-E1037-CON, through the guard library RWB-PLT-E1037-CON | The Decision log right R and the scope of every read (AC5, DP-08) |
| GET parameter read | P3 rwb-case | RWB-P3-E1042-CON | `rwb.decision.query.max-size` and `rwb.decision.query.max-cases` of AC3 (DP-06) |
| GET reference-data read | P3 rwb-case | RWB-P3-E1043-CON | LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-SCOPE of AC3 (DP-07) |
| GET case read with owner and queue | P3 rwb-case | RWB-P3-E2041-CON; faked | The case facts of the scope test of AC8; the shape of this read is Not specified in the source documents (GAP-1245; ASM-2209) |
| GET the rule change audit report | P3 rwb-case | RWB-P3-E2041-CON; faked | The count per rule package version the answer of AC8 reconciles to |
| GET the access-log read | P4 rwb-access | RWB-P4-E1039-CON; faked | The read-back of the AC-READ and AC-EXPT records in the contract tests |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (AC6, DP-11, ADR-020). This baseline declares the six rows because the answer depends on them; the implementation and its errors belong to RWB-P7-E2005-APP.

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` (shared topic) | P7 rwb-decision, written by the local library | decision code AC-READ or AC-EXPT, filter reference, row count, actor reference, decided-at time, chain sequence, entry hash; key is the entry id because an access record has no case |

This baseline declares the envelope because the capability depends on it; it publishes nothing itself. The read path publishes no event of `rwb.decision.events.v1`, because a read produces no business fact, and the ingest of the shared topic into the ledger is RWB-P7-E1027-APP and not this contract.

#### 12.4 Events consumed

None. The audit read is answered from the ledger the service owns and from the six contracts of 12.2; a subscription would add a second, stale copy of the facts that the read can see at the moment of the question. The service's own consumers of `rwb.decision-record.v1`, `rwb.decision.NoticeGenerated.v1` and `rwb.agent.AgentRunCompleted.v1` belong to the ledger, approval and registry stories and are declared there.

#### 12.5 Workflows and activities

None. Both operations are synchronous reads with a 2 s budget: no long-running step, no wait for a human, no durable timer and no compensation, so no workflow and no activity is declared. The daily chain check and the ingest are Schedules of other stories, named in section 19.

#### 12.6 Schedules

None. JOB-13 (continuous ingest) and JOB-14 (chain check at 02:00 with the daily WORM seal) belong to RWB-P7-E1008-APP and RWB-P7-E1027-APP. This baseline declares no Schedule, no cron entry and no job name, and reads no shared scheduler table (DP-10 not claimed).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| decision_log_entry | P7 (rwb_decision) | Read only: the answer elements, the three chain columns `chain_seq`, `prev_hash` and `entry_hash`, and the indexes behind the filters. Created by RWB-P7-E1008-APP and RWB-P7-E1008-DB; declared here and not created |
| decision record (local) | P7 rows in `rwb_decision`, written through the decision-record library | The AC-READ and AC-EXPT record of every query and export (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | The outbox row of the access record and the library objects the template creates |

`delegation_limit` is P4 rwb-access's; `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value` are P3 rwb-case's; `recovery_case`, `case_party`, `task` and `timer` are P3 rwb-case's; `approval` is P7's but belongs to the approval story. None of them is created or read directly by this contract, and no foreign key crosses a service boundary (DP-01, BR10).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access authorise fake | RW-AUDIT "U-8101" with Decision log R and scope ALL; RW-CASEOWN "U-8104" with scope OWN; RW-PHONECOL "U-8102" refused with MSG-P4-002; a delayed answer beyond 2 s | App story, contract tests, harness |
| Ledger and chain fixture | Case "RW-2026-000123" with six entries at chain_seq 101, 155, 160, 230, 231 and 402; 200 entries under rule R-LIT-03 version "LIT-2026.12"; three cases with 6, 2 and 4 entries; one entry of chain_seq 230 with chainVerified false; an empty page with total 0 | App story, contract tests, harness |
| rwb-case parameters fake | max-size 500 and max-cases 500 as parameter rows, and a changed value so no test depends on the code | App story, contract tests |
| rwb-case reference-data fake | LOV-DECISION with D5.1 to D9.3 and the access codes AC-READ, AC-EXPT and AC-DENY; LOV-APPROVAL-LEVEL; LOV-SCOPE with ALL and OWN | App story, contract tests |
| rwb-case case and rule-change fake | Case "RW-2026-000123" and its owner; the three cases of "U-8104" under "LIT-2026.12"; the rule change audit report with 200 decisions for "LIT-2026.12"; a case outside the caller's scope | App story, contract tests, harness |
| rwb-access access-log fake | One AC-READ record with the filter reference and the row count 200; one AC-EXPT record with the same filter and the row count 200 | App story, contract tests |

The values are the legacy values of RWB-E2-005 section 7 and section 16, kept unchanged so the component and the contract assertions read the same fixtures. The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | API-P7-006 and API-P7-007 provided; the six rows of 12.2 consumed; one hop, 2 s |
| Kafka | 1 declared as published by its owner, 0 consumed | `DecisionRecorded` on the shared topic through the library |
| Temporal | None | No workflow, no activity and no Schedule in this baseline |
| File | None | The export is a response body with the media type text/csv, not a file interface |

### 13. Solution plan

**Deliverables.** The additive change to the rwb-decision OpenAPI 3.1 document, the `DecisionLogEntry` and `DecisionLogPage` components, the query-parameter and export declarations, the error mapping rows, the read-only and authorisation sections, and the six WireMock mapping sets of 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | referred to; the app story carries the dependency |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the access record is declared on it | referred to; the app story carries the dependency |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the two limits are parameters | referred to; the app story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the three lists are reference rows | referred to; the app story carries the dependency |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library; the right and the scope are declared here | referred to; the app story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | referred to; the app story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the approver index is an app-story migration | referred to; the app story carries the dependency |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); the legacy lake analysis is retired and no copy is declared | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the audit screens read these two operations through it | referred to; the app story carries the dependency |

No pattern is claimed for DP-02 (the login is the service's and is not declared as a contract element here), DP-04 (no rule is evaluated), DP-05 (no ACE view is read), DP-09 (the outbox is the library's, declared by RWB-PLT-E1027-CON), DP-10 (no job), DP-12 (no case workflow), DP-14 (no topic of this capability is renamed), DP-16 (no integration adapter), DP-18 (no interaction ledger) or DP-20 (no agent client).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionLogQueryContract | Document | The two operations, the ten query parameters, the paging shape, the export media type and the error mapping (AC1, AC3, AC6) |
| DecisionLogEntrySchema | Schema component | The eleven audit elements, the legacy elements, the required set and the hash format (AC2) |
| ReadOnlyRule | Document section | The two-operation rule, the SELECT grant and the correction path of the store (AC4) |
| AuthorisationSection | Document section | The right, the scope, the authorise contract and the AC-DENY refusal (AC5) |
| VersioningRule | Document section | Major version 1, the additive and breaking examples and the pinning rule (AC7) |
| Fake set and fixtures | Test asset | The six fakes of 12.8, used by the app story and the harness (AC8) |

**Build steps**

1. Add the two operations and the two components to the OpenAPI document; validate the additive rule and the absence test of AC1 in the pipeline.
2. Write the answer resource with the eleven audit elements and the legacy elements; assert the required set, the hash format and the masked-free-text rule (AC2).
3. Write the filters, the paging shape and the export media type; assert the two limits as parameters and the three lists as reference rows (AC3).
4. Write the read-only section and the absence test that fails a build adding a write operation (AC4).
5. Write the authorisation section and the refusal row; assert that no role name and no scope value is a constant (AC5).
6. Write the error mapping as one row per condition and assert that no condition carries two message IDs (AC6).
7. Write the versioning section with the compatible and the breaking example (AC7).
8. Publish the six fakes and the drift test; a disagreement between a fake and the document fails the build (AC8).
9. Baseline tag and the consumer sign-off note, including the app story of this key, the harness, the audit screens and the two consumed owners.

**Done when.** The OpenAPI artefact validates in the pipeline, the eight contract tests pass, the six fakes answer every consumed path and the drift test is green on the build of this story and of RWB-P7-E2005-APP, no personal value appears in an example or a fake, and the app story has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-012 | A returned entry does not match the chain, carried with a 200 answer | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. |
| MSG-P4-002 | The role lacks Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The entry is absent or its case is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-002 | The size or the case list is outside the limit | {field} must be between {min} and {max}. |
| MSG-GEN-003 | The from date is after the to date | {field} cannot be before {other}. |
| MSG-P7-003 | The access record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The access record is refused by the decision-record library | Not specified in the source documents (DOR-RWB-P7-E2005-CON-9) |
| MSG-GEN-006 | The ledger does not answer inside the budget | {system} is not available. Try again in a few minutes. |
| 401 message | A caller with no session | Not specified in the source documents (GAP-1249; ASM-2213) |

MSG-P7-012, MSG-P4-002, MSG-GEN-002, MSG-GEN-003 and MSG-P7-003 are copied unchanged from RWB-E2-005 section 14; MSG-P4-003 and MSG-GEN-006 are the platform messages of the access and unavailable paths. The message identifiers are contract elements. Thai text follows decision DL10, as the legacy story states. The identifier of the no-session answer is not given by any source read here, so the placeholder stands until the platform catalogue publishes it.

### 15. Screens and states

The baseline serves the answer that the audit screens read through the gateway-bff composite route (DP-19):

| Screen | What it reads from this contract | State |
|---|---|---|
| SCR-38 Decision log query | The page of entries with the `chainVerified` column and the `messageCodes` of the page carrying MSG-P7-012 for a failing entry; element names beyond the published set, CSV column order and page-size default: working read of ASM-B-P7-01-E2005-8 | Loading, Results, Refused; Empty, Error and No access: Not specified in the source documents (CG-ALL-7076) |
| SCR-38 Decision log query, export | The same rows as `text/csv`, streamed within the 2 s budget, with the row count the AC-EXPT record holds; export size cap, column order and file name: Not specified in the source documents (GAP-1242) | Export |

The composite route, its field list, its masking rules and its timeout budget belong to RWB-PLT-N001-CON and are not fixed here. The screen itself is built by RWB-P7-E2005-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E2005-CON-01 | AC1, AC4 | Contract | The OpenAPI fragment validated; the two GET operations; the absence of any write operation on the audit base |
| TC-P7-E2005-CON-02 | AC2 | Contract | The answer resource compared with `decision_log_entry`; the eleven audit elements and the legacy elements; the required set; the 64-character hash and the 64 zeros of the first entry; the masked-free-text rule |
| TC-P7-E2005-CON-03 | AC3 | Contract | The ten query parameters; max-size 500 and max-cases 500 read as parameters; LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-SCOPE as reference rows; the paging shape with page starting at 1 and size read as a parameter; the text/csv export |
| TC-P7-E2005-CON-04 | AC5 | Component | The authorise fake answering ALL, OWN and a refusal with MSG-P4-002; the scope applied to the case of each entry; the AC-DENY record named with its area and right |
| TC-P7-E2005-CON-05 | AC6 | Contract | One row per condition; 403, 404, 422, 503 and the 200 with the warning; the 401 asserted by status only with the placeholder identifier; the RFC 9457 problem body with type, title, status, detail and the message identifier |
| TC-P7-E2005-CON-06 | AC7 | Contract | A compatible change and a breaking change to the document; the pinned version of the app story |
| TC-P7-E2005-CON-07 | AC8 | Component | The six fakes answering every fixture of section 12.8, including the failing entry of chain_seq 230, the empty page and the refused authorise call |
| TC-P7-E2005-CON-08 | AC8 | Contract | The drift test run against one deliberate difference between a fake and section 12; the build fails |
| TC-P7-E2005-CON-09 | §12.7 (ASM-3438) | Contract | The owned tables of 12.7 read only; the not-owned tables and any foreign key across a service boundary absent; the boundary of each table list tested |
| TC-P7-E2005-CON-10 | AC9 | Contract | The personal-value scanner run over the examples, answers and fakes; a value found fails the build and names the field; no production data in any example, schema or fake |
| TC-P7-E2005-CON-11 | AC10 | Contract | An element named by no source checked against the sources; published as the working read with its gap and assumption and no other status |
| TC-P7-E2005-CON-12 | AC11 | Contract | Event names checked against rwb.<short>.<Event>.v1 and rwb.<short>.events.v1; the access record on rwb.decision-record.v1 written locally and never a new event of this service |
| TC-P7-E2005-CON-13 | AC12 | Contract | decision_log_entry declared as the P7 ledger; no other owner's table declared as created here; no data-lake or reporting copy declared |
| TC-P7-E2005-CON-14 | AC13 | Contract | The limits, decision codes, approval levels, scope values and performance target checked for fixed values; the first-page target held as a service configuration parameter |

The legacy test case set of RWB-E2-005 — TC-E2-005-01 to TC-E2-005-12 — is carried by RWB-P7-E2005-APP and RWB-ITG-E2005-ITG; these eight are the contract's own tests and no legacy identifier is renumbered.

### 17. Guardrails

- No business value in the contract: the two limits, the three lists, the decision codes, the approval levels and the performance target stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: user identifiers, case identifiers, codes, versions, hashes and dates only, and the three legacy free-text elements are declared as masked before return.
- The contract names only rwb-decision tables and only operations owned by rwb-decision; the access, case and report operations are consumed and faked, never declared as provided (DP-01, BR10).
- One REST base and one own topic per service; the shared decision-record topic is named as the library's and never as this service's own (DP-13, DP-14).
- The audit read is read-only: the absence test fails a build that adds a write, a correction or a delete on the audit base (BR3).
- An entry that fails the chain check is shown and never dropped: the warning travels with a 200 answer, not with an error (BR4).
- ACE data is reached only through the owner's contract; this document declares no ACE view and no cross-schema join.
- No data lake and no reporting copy is declared, because the lake is removed and the reporting read model takes the events (DP-17, BR11).
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.
- Every example is synthetic; no production ledger row is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-012 | Audit queries the ledger for a population of cases with inputs, versions, approver and final call | API-P7-006, API-P7-007, the DecisionLogEntry and DecisionLogPage components, the filters and the paging shape | TC-P7-E2005-CON-01 to TC-P7-E2005-CON-08 |
| REQ-DRI-003 | The ledger is hash chained and the chain integrity is checked | The prevHash and entryHash elements, `chainVerified` and the MSG-P7-012 warning | TC-P7-E2005-CON-02, TC-P7-E2005-CON-05, TC-P7-E2005-CON-07 |
| REQ-ACA-006 | Every read of the case and document stores is written to the access log | The AC-READ and AC-EXPT access record of 12.3 and the access-log read of 12.2 | TC-P7-E2005-CON-04, TC-P7-E2005-CON-07 |
| REQ-DRI-002 | The ledger is append only and a correction is a new record naming the one it corrects | The read-only rule of AC4 and the correction path of the store | TC-P7-E2005-CON-01 |
| RWB-E2-005 | The legacy key whose read contract this baseline fixes | The eight criteria of section 7 | TC-P7-E2005-CON-01 to TC-P7-E2005-CON-08 |
| DP-01, DP-13 | Owner's schema and per-service base | The owned and not-owned lists of 12.7 and the base `/api/recovery/decision/v1` | TC-P7-E2005-CON-01, TC-P7-E2005-CON-03, TC-P7-E2005-CON-09 |
| DP-03 | Local decision record and the shared topic | The `DecisionRecorded` row of 12.3 | TC-P7-E2005-CON-04 |
| DP-06, DP-07 | Parameters and reference data through rwb-case | The two parameter rows and the two reference-data rows of 12.2, and the enumerated lists of AC3 | TC-P7-E2005-CON-03 |
| DP-08 | Authorise contract and the guard library | The authorisation element of AC5 | TC-P7-E2005-CON-04 |
| DP-11 | REST contract with mock, one hop, 2 s | The six consumed rows and the six fakes of 12.8 | TC-P7-E2005-CON-05, TC-P7-E2005-CON-07 |
| DP-17 | No data lake | The absence of any lake copy in 12.3 and 12.4 | TC-P7-E2005-CON-01 |
| DP-19 | Screen through gateway-bff | The two screen reads of section 15 | TC-P7-E2005-CON-02 |
| ADR-009, ADR-022 | Append-only log; local record plus central ledger | The read-only rule and the access-record envelope | TC-P7-E2005-CON-01, TC-P7-E2005-CON-04 |

### 19. Out of scope

- The implementation of the two reads, the filter validation, the scope application, the chain check, the notifier, the export and the access recorder: RWB-P7-E2005-APP.
- The end-to-end journey on the real services: `RWB-ITG-E2005-ITG`.
- The ledger store, the canonical form, the append-only rule, the verifier, the daily chain check of JOB-14 and the WORM seal: RWB-P7-E1008-CON, RWB-P7-E1008-APP and RWB-P7-E1008-DB.
- The continuous ingest of JOB-13 and the completeness boundary: RWB-P7-E1027-CON and RWB-P7-E1027-APP.
- The approval operations, the approval queue and the D7.1 screen: RWB-P7-E2013-APP and RWB-P7-E2014-APP.
- The access log, the break-glass path and the role model behind the right: P4 rwb-access, RWB-P4-E1037-CON and RWB-P4-E1039-CON.
- The two limits, the three lists and the rule change audit report: P3 rwb-case, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P3-E2041-CON.
- The gateway-bff composite route, its masking and its timeout budget: RWB-PLT-N001-CON.
- The retired data-lake copy of the ledger and the analysis that used it: RWB-E1-014, no target path under DP-17.
- The deployment, the consumer groups, the dashboards and the runbook of the read capability: no operations story is allocated to this key in the plan.
