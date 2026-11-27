# RWB-P3-E1023-CON Case record view v1, read only

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004; requests F09-affected-0189.

| Item | Value |
|---|---|
| Story key | RWB-P3-E1023-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E1023-CON-16) |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP18, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (OpenAPI 3.1 document, path /api/recovery/case/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-019, FR-P3-020, FR-P3-021) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-009, RD-P1-011, RD-P1-023 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-023 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1023-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (9 resolved, 20 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As **TechX (any team may pick up this story)**, I want **one OpenAPI 3.1 document for the read-only case record operations of rwb-case, with the composed response schemas, the read-only rule, the masking and scope hooks, the error envelope, the version and the nine contract tables**, so that **rwb-case, gateway-bff, rwb-access, rwb-source-data and every later consumer build the case record view against one published read contract on Day 1**.

The document covers the five read operations the view needs: `GET /api/recovery/case/v1/cases/{caseId}`, `/accounts`, `/parties`, `/timeline` and `/timers`. It is the baseline for the contract fake that RWB-P3-E1023-APP builds against; it starts no build dependency.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the engineering standard (ADR-020, DP-11). The case record view is a composite: gateway-bff calls rwb-case and rwb-source-data in parallel and merges the answers. Unless the read shape, the field masking markers, the scope behaviour and the error envelope are fixed before the screen work starts, each caller invents its own shape and the merge in gateway-bff breaks at every change.

This story fixes that shape on Day 1: the operations, the response schema that composes the case, account, party, timeline and timer blocks, the read-only rule, the masking and scope hooks, the error envelope, the version and the nine tables of §12. It also fixes the fakes for rwb-source-data, rwb-access and the masking contract so the screen story and the vehicle tests can run without the live services.

The contract carries no business value of its own: every label, mask rule, timeout and page size comes from the owning service or from a parameter, so a change is data, not a new version of the contract.

### 3. Preconditions

- The service naming of Template and Rules §R4 is fixed for rwb-case: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The legacy contract of RWB-E1-023 §12 and the endpoint inventory API-P3-002, API-P3-003, API-P3-004, API-P3-005 and API-P3-013 of TSD P3 v3 Appendix T-A are the source of the operation list.
- The table ownership of `_work/msr/plan/ownership.json` is accepted: rwb-case owns `rwb_case`; rwb-source-data owns the interaction ledger and the ACE views.
- The rwb-case login (DP-02) will exist with SELECT on schema `rwb_case`. The login name is Not specified in the source documents (GAP-0692; ASM-1239).
- The masking contract of rwb-access is published as C RWB-P4-E1039-CON. The exact shape of the field masking contract is Not specified in the source documents (GAP-0694; ASM-1241).
- The platform contract RWB-PLT-N001-CON will publish the gateway-bff composite route. The exact route specification is Not specified in the source documents (GAP-0693; ASM-1240).
- The timeline page size and the interaction read operation are Not specified in the source documents (GAP-0695; ASM-1242).
- No build dependency. Day 1.

### 4. Flow

1. TechX: takes the operation list from §12.1 and the legacy contract, and names each operation with an `operationId` in the service package.
2. TechX: writes the response schemas for the case block, the account block, the party block with its contact points, the timeline page and the timer block, and one composed schema that holds all five blocks for the composite route.
3. TechX: marks every personal field with its masking hook (masked or clear source, personal-data flag) and every operation with its scope hook (Case record R, scope applied).
4. TechX: writes the error envelope once and references it from every operation with the status codes 401, 403, 404 and 503 and the MSG codes of §14.
5. TechX: fixes the version `v1` in the path, the media type, the identifier format and the read-only rule, then runs the OpenAPI 3.1 linter and the review checklist.
6. TechX: generates the contract fake from the document and publishes it, with the fakes for rwb-source-data, rwb-access and rwb-document, to RWB-P3-E1023-APP and to gateway-bff.
7. TechX: records the consumer acknowledgements of gateway-bff, rwb-access and rwb-source-data against the document checksum.
8. Every consumer: builds against the fake; a change to the document is a new version and a new checksum.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or response field has no source value | The document carries the placeholder Not specified in the source documents (GAP-0692; ASM-1239) for the login name, (GAP-0693; ASM-1240) for the composite route, (GAP-0694; ASM-1241) for the masking shape and (GAP-0695; ASM-1242) for the ledger read and paging; no value is invented | None | AC1, AC4 |
| X2 | The document declares a write operation on a read path | The linter fails and the document is not published | None | AC3 |
| X3 | The document fails OpenAPI 3.1 validation | The document is not published and the checksum is not issued | None | AC1 |
| X4 | A consumer builds against a superseded checksum | The consumer fails the compatibility check against the published checksum | None | AC5 |
| X5 | The rwb-access masking contract changes shape after publication | A new version of the document is raised and the masking hook is re-pointed; the screen story is not changed in place | None | AC4 |
| X6 | The gateway-bff composite route is published with a different merge shape | The contract keeps the five read operations and adds the route mapping; the difference is recorded as GAP-0693 | None | AC2, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency and no table; it fixes the shape other stories build against |
| Negotiable | Schema names and block order are design choices; no business value is fixed here |
| Valuable | One published read contract removes the guesswork from the screen, the edge and the masking work |
| Estimable | One document, five operations, one composed schema, one error envelope, four fakes |
| Small | Fits one sprint with its contract tests |
| Testable | The document itself is the test object; every criterion is checked by a linter or a contract test |

### 7. Acceptance criteria

```gherkin
Feature: Case record read contract v1

  Background:
    Given the contract baseline of rwb-case read-only case record operations under /api/recovery/case/v1

  Scenario: AC1 The OpenAPI 3.1 document for the five read operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document is generated from the contract baseline
    When the document is validated with an OpenAPI 3.1 validator and the contract linter
    Then it validates with no error
    Then it declares GET operations for /cases/{caseId}, /cases/{caseId}/accounts, /cases/{caseId}/parties, /cases/{caseId}/timeline and /cases/{caseId}/timers
    Then every operation carries an operationId, a summary, the 200 response, the error responses and the Case record R security requirement

  Scenario: AC2 The composed response schema (new, D-RCV-60)
    Given the document is published
    When a consumer resolves the composed case record schema
    Then it holds a case block with the header fields, an accounts array, a parties array with the contact points, a timeline page and a timers array
    Then each block names its owning service and the business date it carries
    Then the composed schema is the one gateway-bff uses for the SCR-03 screen model
    Then the timeline addition is published as v1.1, an additive minor version inside major version 1 of this contract, and its item detail fields, its section state and its page total are Not specified in the source documents (GAP-2211)
    Then the timeline type order, the section timeout and the page size are parameters of rwb-case and carry no value in this contract

  Scenario: AC3 The read-only rule (new, D-RCV-60)
    Given the document is published
    When every path and operation in the document is listed
    Then the five read paths carry GET only
    Then the document declares no POST, PUT, PATCH or DELETE operation on a case record path
    Then the transfer, legal-hold, task and placement operations are absent from this document

  Scenario: AC4 The masking and scope hooks (new, D-RCV-60)
    Given the document is published
    When every personal field of the party and contact blocks is inspected
    Then each one names its masked source and its personal-data flag
    Then each operation states the Case record R right and the scope filter
    Then a field whose masking rule is unavailable is described as Not specified in the source documents (GAP-0694; ASM-1241)
    Then the authorise request attribute set for the CASE_RECORD area is Not specified in the source documents (GAP-0989)
    Then the policy version labels in force, and the way a later version reaches the answer, are Not specified in the source documents (GAP-0989)
    Then the field-ID roster of the read-only case record view is Not specified in the source documents (GAP-0989)

  Scenario: AC5 The error envelope, version and fakes (new, D-RCV-60)
    Given the document is published with version v1 in the path
    When a caller sends a request outside the caller's scope or without the right
    Then the documented answer is 404 with MSG-P4-003 and 403 with MSG-P4-002 in the same error envelope
    Then the envelope carries a code, a message and a trace identifier and is shared by every operation
    Then the fakes for rwb-source-data, rwb-access and the masking contract are generated from the same document and published with its checksum

  Scenario: AC6 The nine contract tables (new, D-RCV-60)
    Given the document is published
    When its §12 tables are compared with the service facts
    Then tables 12.1 to 12.9 are all present and none is empty
    Then the schema, REST base, topic and task queue match Template and Rules §R4 for rwb-case
    Then every table named in 12.7 is owned by P3 in the ownership map

  Scenario: AC7 The provided operations answer 401 in the shared error envelope (new, D-RCV-60)
    Given the document is published
    When a request reaches any of the five read operations without valid credentials
    Then the documented answer is 401 in the same error envelope
    Then the 401 answer is listed among the error responses of every operation
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| CB1 | The document follows OpenAPI 3.1 and the service naming of Template and Rules §R4: base `/api/recovery/case/v1`, schema `rwb_case`, topic `rwb.case.events.v1`, queue `rwb-case`, package `th.co.scb.ace.workbench.recovery.case` | R4; ADR-020 |
| CB2 | The five read operations are the only operations in this document; every other rwb-case operation belongs to its own story | §12.1; BR11 of RWB-P3-E1023-APP |
| CB3 | Every personal field names its masked source and its personal-data flag, and every operation states its right and its scope | RWB-P4-E1039-CON; DP-08 |
| CB4 | One error envelope serves every operation, with the MSG codes of §14 and the status codes 401, 403, 404 and 503 | TSD P3 v3 T2.1; §14 |
| CB5 | The version sits in the path; a change is a new version and a new checksum, never an edit in place | ADR-020; R8.2 of the Template and Rules |
| CB6 | Every value that a source does not give is a placeholder with its gap and assumption, never an invented value | Template and Rules §R9; GAP-0695; ASM-1242 |

### 9. State transitions

None. A contract has versions, not case state. This story changes no case status and writes no row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX contract owner | Drafts and publishes the document, the fakes and the checksum |
| rwb-case service owner (P3) | Owns the document as the service contract; approves the operation set |
| rwb-access owner (P4) | Owns the masking contract and the access-log hook that the document references |
| rwb-source-data owner (P1) | Owns the customer, account, freshness and interaction operations the document consumes |
| gateway-bff owner (RWB-PLT-N001-CON) | Owns the composite route and acknowledges the composed schema |
| Solution architect | Approves the read-only rule and the versioning rule |
| Test and QA lead | Runs the contract tests and the consumer compatibility check |

### 11. Data

The document fixes shapes, not values. The schemas carry these fields, with the field IDs of the Logical Data Model and Data Dictionary v9:

| Block | Fields | Table or contract behind it | Owner |
|---|---|---|---|
| case | case_no, product_group, status, stage_code, route_code, owner_user_id, queue_id, entry_date, prescription_date, deviation_open, legal_hold | recovery_case, queue | P3 |
| accounts | account_key, is_primary, accountNo, daysPastDue, totalBalance, dataAsOf | case_account plus the rwb-source-data account contract | P3 for the link, P1 for the facts |
| parties | person_key, party_role, displayName, customerNo, idNo or idNoLast4, category, contacts with contactType, contactKey, contactValue, dataAsOf | case_party plus the rwb-source-data customer and contact contract | P3 for the link, P1 for the facts |
| timeline | occurredAt, channel, contactResult, sourceSystem, actionCode, actionCodeName, contactAt, promiseStatus, page, size | the rwb-source-data 5.1.0 interaction read and its published paging | P1 |
| timers | timer type, started_at, expires_at, warn_at, paused, status | timer | P3 |

No row is read or written by this story. The response shapes copy the field names of the legacy contract of RWB-E1-023 §12 unchanged, and the field IDs of section 11 of that story.

### 12. Contract

#### 12.1 REST operations provided

| Operation | operationId | Request | Response | Errors |
|---|---|---|---|---|
| GET /api/recovery/case/v1/cases/{caseId} | getCase | Path caseId | Case | 401, 403, 404, 503 |
| GET /api/recovery/case/v1/cases/{caseId}/accounts | listCaseAccounts | Path caseId | CaseAccount[] with accountNo, daysPastDue, totalBalance, dataAsOf | 401, 403, 404, 503 |
| GET /api/recovery/case/v1/cases/{caseId}/parties | listCaseParties | Path caseId | CasePartyView[] with personKey, partyRole, displayName, customerNo, idNo or idNoLast4, category, contacts[] and dataAsOf | 401, 403, 404, 503 |
| GET /api/recovery/case/v1/cases/{caseId}/timeline | getCaseTimeline | Path caseId; query type, from, to, page, size | TimelinePage ordered by time, each row with sourceSystem | 401, 403, 404, 503 |
| GET /api/recovery/case/v1/cases/{caseId}/timers | listCaseTimers | Path caseId | Timer[] | 401, 403, 404, 503 |

The page size and the ordered paging of the timeline are Not specified in the source documents (GAP-0695; ASM-1242). Every operation states Case record R and scope applied.

#### 12.2 REST operations consumed

| Operation | Owner | In the document as |
|---|---|---|
| GET /api/recovery/source-data/v1/customers/{id} | rwb-source-data (P1) | The customer block of the composed schema |
| GET /api/recovery/source-data/v1/accounts/{id} | rwb-source-data (P1) | The account facts of the accounts block |
| GET /api/recovery/source-data/v1/freshness | rwb-source-data (P1) | The business date of each block |
| GET /api/recovery/source-data/v1/cases/{caseId}/interactions | rwb-source-data (P1), RWB-P1-E1066-CON 5.1.0 | Case UUID, provider paging, masked summaries. The ledger supplies all contact-history rows. |
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | Scope hook. Send UUID Idempotency-Key, caseId (UUID) and case number to the P4 fake. Assert allow/deny and Problem.messageCode. Remaining request and answer fields are Pending (GAP-3322). |
| GET /api/recovery/access/v1/masking-policies | rwb-access (P4) | The masking hook of every personal field |
| GET /api/recovery/document/v1/cases/{id}/documents | rwb-document (P5) | The documents panel of the screen model, outside this document |

#### 12.3 Events published

None. A read contract publishes no event; the AC-READ access record goes to the rwb-access access log through its contract.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None. The document describes synchronous reads only; CaseWorkflow on queue `rwb-case` is out of its scope.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

| Table | Schema | Owner | In the document |
|---|---|---|---|
| recovery_case | rwb_case | P3 | The case block |
| case_account | rwb_case | P3 | The account links |
| case_party | rwb_case | P3 | The party links |
| queue | rwb_case | P3 | queueCode and queueName in the header |
| timer | rwb_case | P3 | The timer block |
| lov_value | rwb_case | P3 | Labels for the coded values |
| reference_row | rwb_case | P3 | LOV-ACTION-CODE, LOV-CONTACT-RESULT, LOV-CHANNEL, LOV-CONTACT-TYPE, LOV-PARTY-ROLE |
| reference_version | rwb_case | P3 | The version in force on the read date |
| parameter_catalog | rwb_case | P3 | `caserecord.section.timeout.ms` |
| parameter_value | rwb_case | P3 | The value in force on the read date |

The service also owns case_entry_exclusion, queue_member, queue_measure, task and assignment, which this document does not describe.

#### 12.8 Contract fakes

| Fake | Generated from | Owner | Used by |
|---|---|---|---|
| rwb-case read fake | This document, with its checksum | P3 | RWB-P3-E1023-APP, gateway-bff |
| rwb-source-data fake | The P1 contract line for customers, accounts, freshness and interactions | P1 | The schema examples and the composed response tests |
| rwb-access fake | The authorise, masking-policy and access-log contract of C RWB-P4-E1037-CON | P4 | The scope and masking tests |
| The masking and customer/account read fake | C RWB-P4-E1039-CON; the exact shape is Not specified in the source documents (GAP-0694; ASM-1241) | P4 | AC4, AC5 |
| gateway-bff composite route stub | RWB-PLT-N001-CON; the exact route specification is Not specified in the source documents (GAP-0693; ASM-1240) | edge | AC2, AC5 |

#### 12.9 Call-type summary

| Call type | In this contract |
|---|---|
| REST | Yes. Five GET operations provided under `/api/recovery/case/v1`; the consumed operations of 12.2 are declared as hooks; one hop, 2 s timeout |
| Kafka | None |
| Temporal | None |
| File | None |

### 13. Solution plan

**Package.** The document is held with the service contract of rwb-case, under Java package `th.co.scb.ace.workbench.recovery.case`; it is the input to the code generator of the platform contract library.

**Deliverables**

| Deliverable | Content |
|---|---|
| OpenAPI 3.1 document | The five read operations, the schemas, the security scheme, the error envelope and version v1 |
| Composed schema | case, accounts, parties, timeline and timers in one screen model for gateway-bff |
| Contract linter rules | Read-only rule, operationId naming, personal-field flags, the nine tables present |
| Fakes | The rwb-case read fake plus the four fakes of 12.8 |
| Checksum register | The published document with its checksum and the consumer acknowledgements |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

As a CON story it carries no build dependency: the H rows above are the pattern rows of the vehicle, recorded here for the trace, and they are taken by the APP story that builds.

**Build steps**

1. Fix the operation list and the operationIds from 12.1; check the legacy contract for every request and response field.
2. Write the five block schemas and the composed schema; check every field name against section 11.
3. Add the masking hook to every personal field and the scope hook to every operation.
4. Write the error envelope once and reference it from every operation with the MSG codes.
5. Fix version v1, the media type, the identifier format and the read-only rule.
6. Run the OpenAPI 3.1 validator and the contract linter; a write operation on a read path fails the build.
7. Generate the fakes of 12.8 and publish them with the checksum.
8. Collect the gateway-bff, rwb-access and rwb-source-data acknowledgements.

**Done when.** The document validates, the linter passes, the fakes are published with the checksum and the three consumer acknowledgements are recorded.

**Contract tests.** Schema validity and compatibility with the previous checksum, the read-only rule, the error envelope on all four status codes, the masking flags on every personal field and the completeness of the nine tables.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, an expired session, or a read operation called without valid credentials (status 401 on every operation) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P3-023 | A section cannot be shown | {section} cannot be shown now. The rest of the case is shown. |
| MSG-P7-003 | The access record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The case record screen (SCR-03) shows its loading, error and no-access states in RWB-P3-E1023-APP. This document supplies the codes: the error state uses the envelope of this section and MSG-P3-023 for a section that cannot be shown; the no-access state uses MSG-P4-002 and MSG-P4-003. The loading state has no contract code.

Validation rules the document must satisfy: OpenAPI 3.1 valid; every operation has an operationId in the service namespace; every path is under `/api/recovery/case/v1`; no write method on a case record path; every personal field carries a personal-data flag and a masked source; every operation declares 401, 403, 404 and 503 with the shared envelope; the envelope carries a code, a message and a trace identifier. The envelope body shape follows the problem response of TSD P3 v3 T2.1 and its field names are fixed by this document, not by a caller.

### 15. Screens and states

None. This story delivers no screen. It fixes the data the SCR-03 screen consumes in each state: Loading (the composed schema with empty blocks), Read only (the five blocks with their business dates), On hold (the hold flag and the prescription date in the case block), Stale input (the business date and batch state per block, so the stale banner can be driven), Error (the shared envelope with the MSG code for the section that failed). No access: Not specified in the source documents (CG-ALL-3599). The screen itself is built by RWB-P3-E1023-APP and served as the gateway-bff composite route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1023-CON-01 | AC1 | Contract | The OpenAPI 3.1 document, validated by the OpenAPI validator and the linter |
| TC-P3-E1023-CON-02 | AC2 | Contract | The composed schema and the five blocks, resolved with the fake |
| TC-P3-E1023-CON-03 | AC3 | Contract | The full path and operation list, scanned for write methods |
| TC-P3-E1023-CON-04 | AC4 | Contract | Every personal field and every operation, checked for the masking and scope hooks |
| TC-P3-E1023-CON-05 | AC5 | Contract | A request without the right and a request out of scope, answered from the fake |
| TC-P3-E1023-CON-06 | AC6 | Component | The nine tables against Template and Rules §R4 and the ownership map |
| TC-P3-E1023-CON-07 | AC6 | Component | Each table of §12.7 at its boundary values, empty and populated, checked against its owner and schema |
| TC-P3-E1023-CON-08 | AC7 | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1023-CON-AC7) |

### 17. Guardrails

- No business value in the document: labels, mask rules, timeouts and page sizes are named as sources, never fixed here.
- No personal data in the document examples: every example party is synthetic and no example carries a clear identity number or contact value.
- No PII in events, workflow inputs or logs, and none in the contract examples.
- rwb-case reads only schema `rwb_case`; the document declares no foreign table and no cross-schema read (DP-01).
- ACE data is declared only through the rwb-source-data contract, never as a view or a table of rwb-case (DP-05).
- The interaction ledger is declared through its owner's read, never as a table (DP-18).
- The document states Case record R and the scope on every operation; a hook that hides the scope fails the linter (DP-08).
- No write operation on a case record path in this document.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Story | Test cases |
|---|---|---|---|---|---|
| REQ-OCC-007 | Case record view with account, arrears, owner, queue, stage, status, contact history and documents | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-11 | RWB-P3-E1023-CON | TC-P3-E1023-CON-01, TC-P3-E1023-CON-02 |
| REQ-RDF-009 | Every data product carries a freshness stamp | Epic 1, 3.1; Program, 5.1 | FEAT-ACA-11 | RWB-P3-E1023-CON | TC-P3-E1023-CON-02 |
| REQ-ACA-005 | Personal data masked by role | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | RWB-P3-E1023-CON | TC-P3-E1023-CON-04 |
| REQ-ACA-006 | Every read of the case store written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | RWB-P3-E1023-CON | TC-P3-E1023-CON-04, TC-P3-E1023-CON-05 |
| REQ-ACA-009 | Only cases in the caller's scope are visible | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-11 | RWB-P3-E1023-CON | TC-P3-E1023-CON-05 |

| Trace | Reference |
|---|---|
| Legacy key | RWB-E1-023, disposition Split (rework) |
| Legacy contract source | RWB-E1-023 §12; TSD P3 v3 Appendix T-A (API-P3-002, API-P3-003, API-P3-004, API-P3-005, API-P3-013) |
| Consumed by | RWB-P3-E1023-APP (the case record view), gateway-bff composite route (RWB-PLT-N001-CON) |
| Contract dependencies | None. The P4 and P1 contracts are referenced, not depended on for the build |
| Pattern rows | DP-01, DP-02, DP-03, DP-05, DP-06, DP-07, DP-08, DP-11, DP-13, DP-14, DP-15, DP-18, DP-19 |

### 19. Out of scope

- The case record view implementation and its screen states (RWB-P3-E1023-APP).
- The write operations of rwb-case: transfer, legal hold, task update, queue placements and reference loads.
- The case list, the task list and the queue operations of the service.
- The SCIM or Entra group-to-role mapping, which belongs to rwb-access and ACE Common.
- The physical schema and the Flyway migration, which belong to the DB stories and RWB-PLT-E1044-CON.
- The gateway-bff composite route itself, which belongs to RWB-PLT-N001-CON.
