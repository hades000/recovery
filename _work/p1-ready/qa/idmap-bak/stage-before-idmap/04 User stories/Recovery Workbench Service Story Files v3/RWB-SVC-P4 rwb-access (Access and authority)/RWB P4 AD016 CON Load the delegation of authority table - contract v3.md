# RWB-P4-AD016-CON Load the delegation of authority table

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD016-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-AD016-CON-16); the squad sizes it at refinement |
| Contract version | v1 of the base /api/recovery/access/v1, as set by API Specification v5 (rwb-access.yaml) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-016 for rwb-access, which owns the delegation of authority table. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 17 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the delegation of authority load, its approval and its lookup: an OpenAPI 3.1 document for the four `rwb-access` operations, the `DoaLoad`, `DoaLoadAnswer` and `DoaLimitAnswer` schemas with the `NOT_COVERED` and `RELATED_PARTY` answers, the whole-file refusal and the falling-limit rule stated as contract invariants, the four-eyes and effective-date rules stated as invariants, the `rwb.access.DoaLimitChanged.v1` event, the contract tables of section 12 and the fakes**, so that **RWB-P4-AD016-APP, the SCR-41 route work, the approval router and any later consumer can build on Day 1 against a fixed, testable contract without waiting for `rwb-decision` or for the table to be built**.

The baseline fixes the naming the checks require: service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1` (DP-13), topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, the shared `rwb.decision-record.v1` topic for the record (DP-03), task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The delegation of authority is the one table whose answer another service must be able to trust at a date: a router asks who may approve a settlement, a write-off or a debt sale, and the answer has to name the level, the row and the version that applied on that date, or refuse with a named decision and product. In the monolith the answer came from an in-process call, so nothing outside the monolith could ask it and nothing fixed what a refusal looked like.

This story pins the four things a consumer needs and cannot get from a story file: what a load answers and what a refused load answers, what the approval requires and refuses, what the lookup answers when a limit exists and when none does, and which two invariants the service will never break — a refused file stores nothing, and an approval never takes effect without its record. Once that is agreed and faked, the app story builds in parallel with the table, `rwb-decision` can build its routing against the answer, and a change of the table's shape is caught in a contract test instead of in an integration window.

This story meets REQ-ACA-004 (the delegation of authority table held as reference data, setting every approval limit), REQ-DRI-010 (thresholds, limits and names are configuration rows with a version, changed without a code release) and REQ-ACA-013 (the administration screens for roles, permissions and delegation exist), and it states R-UNI-38 and R-UNI-39 as contract invariants rather than as implementation notes.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners come from the ownership map only: `GET /doa-limits` is P4's, the reference lists and the parameters are P3 `rwb-case`'s and are consumed through RWB-P3-E1043-CON and RWB-P3-E1042-CON, and the decision-record message is the PLT library's.
- The table `delegation_limit` is RWB-P4-E1038-APP's, with its columns DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062; this document declares the shapes of the operations on it and no column of its own.
- No approved source gives a DoA-specific load or approval path: the legacy story names the generic reference-load and rule-version paths, and the ownership map rules the generic paths P3's (GAP-0833; ASM-1534). The document fixes the console side only.
- Which right gates the approval is stated twice in the sources: the legacy permission row and the FSD's 403 give it to the A letter in Rules and parameters, while TSD P4 appendix T-A declares right A in Reference data for the generic approve path (GAP-0836; ASM-1537).
- The incident of a `NOT_COVERED` answer is stated by the FSD but not owned by a source (GAP-0838; ASM-1539).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the four operations under the base `/api/recovery/access/v1`, with the shared components of the service.
2. Agree the `DoaLoad` answer, the `DoaLoadAnswer`, the `DoaLimitAnswer` and the difference report, with `NOT_COVERED` and `RELATED_PARTY` as declared answers rather than error strings.
3. Agree the three consumed operations with their owners, the one-hop rule, the 2 s budget and the breaker.
4. State the error envelope, the message-ID mapping and the refusal shapes for a refused file, an absent right, the loader, a version label that exists, a load that is not `LOADED` and an unwritable record.
5. State the invariants — whole file or nothing, no falling limit, the four-eyes rule with the two letters, the effective-from-valid-from rule, and an answer that always names its version — as normative clauses.
6. Declare the `rwb.access.DoaLimitChanged.v1` event with its key, its payload and its publish-after-commit rule.
7. Publish the contract tables of section 12 (nine sub-tables) and the fakes.
8. Add the contract tests: schema validation, error mapping, consumed-operation declarations, invariant clauses, fake drift, the event shape and the personal-data scan.
9. Tag the baseline and hand it to RWB-P4-AD016-APP, the SCR-41 route work, the routing work and every later consumer.
10. Re-baseline additively when a list value or a parameter row is added; a removed or retyped field is a new major version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails the build; no baseline is tagged | None | AC1 |
| X2 | An operation declares no security right or omits an error response | The document review fails; a consumer cannot know what a refusal means | None | AC1, AC3 |
| X3 | A schema, an example or a fake carries a personal field | The personal-data scan fails the build | None | AC2, AC6 |
| X4 | A message id used by a response has no catalogue entry | The error mapping test fails | None | AC3 |
| X5 | A consumed operation is declared as provided, or an owner is missing | The review fails; the document names one owner per operation | None | AC4 |
| X6 | The document lets a refused file answer with a stored row, or a load answer a partial row count | The invariant review fails; a load is whole or not at all | None | AC5 |
| X7 | The lookup answer omits the level, the row id or the version | The invariant review fails; an answer without its version cannot be audited | None | AC5 |
| X8 | A fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X9 | The event is declared as published before the commit, or carries a personal field | The review fails; the outbox rule is stated and the payload carries no personal data | None | AC6 |
| X10 | A path or a topic of another service appears as this service's | The document is corrected; one base and one topic per service | None | AC1, AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the P3 contracts and the table's field list only |
| Negotiable | The field-level detail of the answers, the list of query parameters of the lookup and the event payload are settled with the consumers and with data stewardship; the operations, the envelope and the invariants are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-41 route and the routing work on Day 1, and keeps one owner for the table and one for the answer |
| Estimable | One document, three schema groups, one error envelope, five invariants, nine contract tables, six fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Delegation of authority contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the delegation of authority table is rwb-access's and the reference lists and parameters are rwb-case's

  Scenario: AC1 The OpenAPI 3.1 document describes the four operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/doa-loads, POST /admin/doa-loads/{loadId}/approve, GET /admin/doa-loads/{loadId} and GET /doa-limits with the owner rwb-access
    Then POST /admin/doa-loads declares the multipart file, the query table fixed to "delegation_limit", the query validFrom and the Idempotency-Key header
    Then every write operation declares 401, 403, 404 or 409, 422 and 503 as its error responses
    Then no operation of another service is declared as provided by rwb-access
    Then GET /doa-limits is declared once as the single path of the lookup, the answer over the DoA table belongs to RWB-P4-AD016-APP, and RWB-P4-E2013-APP is named only as its consumer

  Scenario: AC2 The answers carry the agreed fields and the two named refusals (new, D-RCV-60)
    Given the DoaLoad, DoaLoadAnswer and DoaLimitAnswer schemas of the document
    When the contract review checks the three schemas against the field lists below
    Then DoaLoad carries loadId, table, limitVersion, validFrom, state, rowCount and the difference report
    Then DoaLoadAnswer carries loadId, limitVersion, validFrom, state, rowCount, the author reference and the approver reference
    Then DoaLimitAnswer carries status, approvalLevel, delegationLimitId, limitVersion, reason, incidentReference and asOf
    Then status is one of COVERED and NOT_COVERED, and reason is present only with the RELATED_PARTY answer
    Then approvalLevel is one of L1, L2, L3, L4, L5 and L6, and limitVersion is mandatory whenever status is COVERED
    Then no property of any schema is a name, an e-mail address or a personal field

  Scenario: AC3 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by any operation
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 or MSG-P7-002, 404 carries MSG-P4-003, 409 carries MSG-GEN-004, 422 carries MSG-P1-002 or MSG-GEN-001 and 503 carries MSG-P7-003 or MSG-GEN-006
    Then every messageId used by the document has an entry in the message catalogue
    Then MSG-P1-002 and MSG-P7-010 are kept word for word as shared entries of the P4 message catalogue
    Then the response carries the problem media type and the trace identifier

  Scenario: AC4 The three consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the reference list read and the parameter read
    When the contract review checks the consumed section of the document against its owners
    Then each is declared in the consumed section with its owner, P4 rwb-access or P3 rwb-case
    Then each declares one hop and the 2 s client budget with a breaker
    Then the P3 list and parameter reads are declared as consumed and never as provided by rwb-access
    Then the document states that no table of rwb_case is named as this service's own

  Scenario: AC5 The five invariants are normative clauses of the document (new, D-RCV-60)
    Given the normative clauses of the document
    When the contract review checks the normative clauses of the document
    Then the whole-file clause says a load is stored entirely or not at all and that a refused file leaves the version in force unchanged
    Then the falling-limit clause says a level's principal limit must not rise above the principal limit of the level beneath it, and that an unknown decision code, level or product is refused with a 422 response
    Then the four-eyes clause says the approver reference must differ from the load's author reference, and that the load needs the C letter in Reference data while the approval needs the A letter in Rules and parameters
    Then the effective-date clause says a version takes effect from its validFrom date and that the version before keeps validTo set to the day before validFrom and stays readable
    Then the answer clause says an answer that is COVERED carries its level, its delegationLimitId and its limitVersion, and that NOT_COVERED is answered with HTTP 200 carrying MSG-P7-010 naming the decision and the product with an incidentReference
    Then the document carries no second writer of delegation_limit and names no table of rwb_case as its own

  Scenario: AC6 The event and the fakes match the document and carry no personal data (new, D-RCV-60)
    Given the six contract fakes of section 12.8 and the event declaration of section 12.3
    When the contract tests run
    Then each fake answers the paths and payloads of the document with the declared status codes and message IDs
    Then the event declaration fixes rwb.access.DoaLimitChanged.v1 on rwb.access.events.v1, keyed on limitVersion, published after the commit and carrying no personal data
    Then a drifted fake or a changed event key fails the build
    Then no schema, example, fake or event payload carries a name, an e-mail address or a personal field
```

These six criteria test the artefact only. This story owns no legacy acceptance criterion: the two legacy criteria of RWB-AD-016 belong to RWB-P4-AD016-APP.

### 8. Business rules

| ID | Rule | Source | Covered by | Test cases |
|---|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path as its own | DP-13; Architecture v5 slide 41 | AC1 | TC-AD-016-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC4 | TC-AD-016-CON-04 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story and the FSD | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC3 | TC-AD-016-CON-03 |
| BR4 | The load path accepts one table only, `delegation_limit`, and the document states the whole-file rule: every code from its list in force, no repeated tuple, no falling limit, nothing stored on a refusal | Legacy RWB-AD-016; FSD P4 v3 A2.6 AC-P4-006-01 and AC-EXC-P4-006-01 | AC5 | TC-AD-016-CON-05 |
| BR5 | The load needs the C letter in Reference data and the approval needs the A letter in Rules and parameters; the approver reference must differ from the load's author reference | Legacy RWB-AD-016 Permission checks; TSD P4 v3 T6.1; MSG-P7-002; ASM-1537 | AC5 | TC-AD-016-CON-05 |
| BR6 | An approved version takes effect from its `validFrom` date; the version before keeps `validTo` on the day before and stays readable | Legacy RWB-AD-016 AC1; FSD P4 v3 A2.6 AC-ALT-P4-006-02; R-UNI-38 | AC5 | TC-AD-016-CON-05 |
| BR7 | The lookup answers the level, the row id and the limit version, or `NOT_COVERED` answered with HTTP 200, the message MSG-P7-010 naming the decision and the product, and an `incidentReference`, or L1 with the coded reason `RELATED_PARTY` read from the related-party row, the condition text staying in that row | Legacy RWB-AD-016 AC2; FSD P4 v3 A2.6 AC-ALT-P4-006-01, AC-EXC-P4-006-04 and AC-EXC-P4-006-05 | AC2, AC5 | TC-AD-016-CON-02, TC-AD-016-CON-05 |
| BR8 | No approval takes effect without its record, and the document states the 503 with MSG-P7-003 on an unwritable record | R-UNI-39; FSD P4 v3 A2.6 AC-EXC-P4-006-03 | AC3, AC5 | TC-AD-016-CON-03, TC-AD-016-CON-05 |
| BR9 | Every write operation carries `Idempotency-Key`, and a repeat answers the stored answer | Architecture v5 slide 11 | AC1 | TC-AD-016-CON-01 |
| BR10 | The event `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1` is published after the commit through the outbox, is keyed on `limitVersion`, carries `limitVersion`, `table`, change kind, `validFrom`, `validTo` and `rowCount` in a CloudEvents 1.0 envelope, and carries no personal data | Architecture v5 slide 43; DP-09; GAP-0841 | AC6 | TC-AD-016-CON-06 |
| BR11 | A schema change is additive within a major version; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC1 | TC-AD-016-CON-01 |
| BR12 | No schema, example, fake or event payload carries personal data; user references, codes, dates and amounts only | Requirement NFR-040; DP-05 | AC2, AC6 | TC-AD-016-CON-02, TC-AD-016-CON-06 |

### 9. State transitions

The document is the object with a lifecycle; the version states it declares are the table's.

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four operations, the three consumed operations and the five invariants are described | In review |
| In review | Consumer sign-off | The app story, the SCR-41 route work and the routing work accept the document and the fakes | Baselined |
| Baselined | Additive change | A field or a declared list value is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or an answer shape changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A message ID change | A catalogue entry is renamed | Rejected: a message ID is stable once published |
| Baselined | An event key or payload change | The key or a payload field changes | New event major version |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the error envelope, the event declaration and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Tech lead of rwb-case (P3) | Reviews the two consumed reads, the list values of LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT and the parameter, and owns their definitions |
| Tech lead of rwb-decision (P7) | Reviews the lookup answer, the `NOT_COVERED` shape, the incident reference and the event, as the consumer that routes approvals |
| Security administrator role owner | Confirms that the C letter in Reference data and the A letter in Rules and parameters are the declared authorities |
| Data steward | Confirms that no personal data field is declared in a schema, an example, a fake or the event payload |
| QA and the integration team | Review the contract tests and the drift rule |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Load request | Multipart file; query `table` fixed to `delegation_limit` and `validFrom`; the version label; `Idempotency-Key` | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |
| Load answer | `loadId`, `table`, `limitVersion`, `validFrom`, `state`, `rowCount`, the difference report against the version in force | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |
| Approval answer | `limitVersion`, `validFrom`, `validTo`, `state`, `rowCount`, `approverReference`; `state` one of `LOADED`, `APPROVED` | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |
| Lookup request | `decisionCode`, `regulationItem`, `productGroup`, `principal`, `lossPct`, `lossAmount`, `asOf` | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |
| Lookup answer | `status` (`COVERED` or `NOT_COVERED`), `approvalLevel` (L1 to L6), `delegationLimitId`, `limitVersion`, `reason` (`RELATED_PARTY`), `incidentReference`, `asOf` | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |
| Record entry | The decision code `AC-VERS` or `AC-DENY`; the version, the `validFrom`, the caller reference and the outcome | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |
| Authority input | The caller's `permission` row with `capability_area` REFERENCE_DATA or RULES_AND_PARAMETERS and its `letters` (DF-REF-042, DF-REF-043) | DF-REF-042, DF-REF-043 |
| Row shape | The `delegation_limit` columns of DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062, as RWB-P4-E1038-APP declares them | DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 |
| Event payload | `limitVersion`, the table `delegation_limit`, the change kind, `validFrom`, `validTo`, `rowCount`; CloudEvents 1.0 envelope; no personal field | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |
| Refusals | `messageId` MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P7-002, MSG-P7-003, MSG-P1-002, MSG-GEN-001, MSG-GEN-004 or MSG-GEN-006 with the field list | Not specified in the source documents (DOR-RWB-P4-AD016-CON-7) |

The exact field-level schema of the three answers — string lengths, the number and names of the difference report fields, the page of the version read and the maximum length of the incident reference — is Not specified in the source documents (GAP-0840; ASM-1541). This baseline fixes the field names above and leaves the field-level detail to the review; the rows themselves are declared only as owned and never as values.

### 12. Contract

#### 12.1 REST operations provided

Owner P4 `rwb-access`; base `/api/recovery/access/v1` (DP-13).

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/doa-loads` | Multipart: file; query `table` = `delegation_limit`, `validFrom`, version label; `DoaLoad` answer | Reference data, right C, scope applied; `Idempotency-Key` required |
| POST | `/admin/doa-loads/{loadId}/approve` | No request body; `DoaVersion` answer with the version, the window, the state, the row count and the approver reference | Rules and parameters, right A, scope applied; `Idempotency-Key` required |
| GET | `/admin/doa-loads/{loadId}` | `DoaLoadAnswer` with the load, the version label, `validFrom`, the state, the row count and the two references | Reference data, right R, scope applied |
| GET | `/doa-limits` | Query: `decisionCode`, `regulationItem`, `productGroup`, `principal`, `lossPct`, `lossAmount`, `asOf`; `DoaLimitAnswer` | Reference data, right R, scope applied |

Errors: 401 no session (MSG-P4-001); 403 no right or the loader (MSG-P4-002, MSG-P7-002); 404 unknown load (MSG-P4-003); 409 an existing version label or a load not `LOADED` (MSG-GEN-004); 422 a refused file (MSG-P1-002) or an empty field (MSG-GEN-001); 503 an unavailable read (MSG-GEN-006) or an unwritable record (MSG-P7-003). The refusal that is a refused file carries `code` FILE_REFUSED and `messageId` MSG-P1-002 with the check and the row in `field`, so a consumer can show the offending row without reading the text.

The legacy story named the generic reference-load and rule-version paths under the single monolith base that DP-13 replaces; TSD P4 v3 appendix T-A carries the generic reference-load paths as API-P4-005 and API-P4-006, and the ownership map rules them P3 `rwb-case`'s because the reference store is P3's (ASM-0041). The DoA paths are therefore the ones RWB-P4-E1038-APP introduces and this document fixes, with one controller and one owner per path; the generic reference-load and rule-version paths stay P3's and P7's and are not reused for the DoA table (GAP-0833; ASM-1534). The approval is gated by right A in Rules and parameters read from the permission rows (GAP-0836). The service-level gate keeps the Rules and parameters letters: C for the load, held by RW-COE, and A for the approval, held by RW-RISK (GAP-2276). `GET /doa-limits` is the ownership map's P4 operation (GAP-0842; ASM-1543).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own) | The C letter in Reference data and the A letter in Rules and parameters, with the MSG-P4-002 refusal shape |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT with the version in force |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The approver-role parameter, read with the version in force |

None of the three is declared as provided by this story, and none is called twice in one load or one approval.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | Key `limitVersion`; the version, the table `delegation_limit`, the change kind, `validFrom`, `validTo` and the row count; CloudEvents 1.0 envelope; published by the outbox relay after the commit; no personal field |

The key and the payload are proposed by this document and confirmed at contract review (GAP-0841; ASM-1542). The service also appends a decision-record entry of the DP-03 library, whose `DecisionRecorded` message travels on the shared topic `rwb.decision-record.v1`; that message belongs to the library and is declared as such, not as this service's event.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this contract adds no subscription.

#### 12.5 Workflows and activities

None. The load and the approval are two synchronous commands with a human decision between them, and the lookup is one read; the document declares no workflow ID, no activity name and no task-queue registration.

#### 12.6 Schedules

None. The six-monthly access review Schedule belongs to another capability of the service and is not part of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `delegation_limit` | P4 (`rwb_access`) | The rows and the window the four operations read and write; created and migrated by RWB-P4-E1038-APP, declared here by its columns DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 |
| `role`, `permission` | P4 (`rwb_access`) | The caller's C letter in Reference data and A letter in Rules and parameters (DF-REF-042, DF-REF-043) |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_access` | The record and event outbox rows and the stored answer of each write; no inbox row, because no event is consumed (DP-09) |
| decision record (local library objects) | PLT library, created in `rwb_access` | The `AC-VERS` and `AC-DENY` entries and their hash chain (DP-03) |

No table of another service is named as this service's: `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value` are P3 `rwb_case`'s and appear only as consumed shapes, and `decision_log_entry` is P7's (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| parameters fake | The approver-role parameter with the version in force, and a 503 for the unavailable case (DP-06) | App story, contract tests |
| reference-data fake | LOV-DECISION with "D6.9" absent and D6.4, D6.6 and D9.2 present; LOV-APPROVAL-LEVEL L1 to L6; LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, each with its version | App story, contract tests |
| decision-record fake | The `AC-VERS` and `AC-DENY` append, the hash-chain check and a forced failure | App story, contract tests |
| authorise fake | The C letter for "U-3101", the A letter for "U-3102", the MSG-P4-002 refusal for "U-3103" and the MSG-P4-001 answer for a caller with no role | App story, contract tests |
| table fixture fake | The rows of "DOA-2026.11" seeded for the lookup and for the difference report, and the "DOA-2027.01" fixture of the change | App story, contract tests, the routing work |
| approval-router and gateway-bff fakes | The router's `GET /doa-limits` requests of section 12.8 and the SCR-41 composite route with the four states | App story, the routing work, the SCR-41 route work |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed | Four operations on `/api/recovery/access/v1`; the authorise call, the list read and the parameter read; one hop, 2 s timeout |
| Kafka | 1 published type, 0 consumed | `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`, plus the library's `DecisionRecorded` message on `rwb.decision-record.v1` |
| Temporal | 0 workflows, 0 activities | No workflow in the load, the approval or the lookup |
| File | 1 inbound | The delegation of authority file, declared as the multipart part of `POST /admin/doa-loads`; no file output |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-doa-v1.yaml` (OpenAPI 3.1) with the four operations and the shared components, `contract/error-envelope.yaml` with the message-ID map, `contract/doa-load.yaml`, `contract/doa-limit-answer.yaml`, the normative clause file with the five invariants, `asyncapi/rwb-access-doa-event-v1.yaml` with the event, the contract README with the idempotency and versioning rules, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 appears in the contract as one rule: the caller's staff reference and group resolve through `v_ace_iam_group` inside the service, and no schema, example or fake carries a name or an e-mail address that could have come from it. DP-06 and DP-07 appear as declarations that the approver role and the three lists are rows with a version, so a change is a data change and the contract declares no default value for either.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the shared components and the error responses; schema lint in the pipeline.
2. The four operations with the shapes of section 11 and the `Idempotency-Key` header on the two writes.
3. The three consumed operations with their owners, the one-hop rule, the 2 s budget and the once-per-call clause.
4. The error envelope and the message-ID map, with the texts of section 14 copied unchanged.
5. The five normative clauses of AC5, each written as a numbered clause a test can read.
6. The `rwb.access.DoaLimitChanged.v1` declaration with its key, its payload and the publish-after-commit rule.
7. The six fakes and their stub fixtures of section 12.8.
8. The six contract tests, including the personal-data scan, the event-key test and the drift test.
9. Baseline tag and the consumer sign-off note from the app story, the SCR-41 route work and the routing work.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD016-APP | The four provided operations, the three answer schemas, the invariants and all six fakes |
| The SCR-41 route work (RWB-PLT-N001-CON) | The states waiting, approved, refused and not covered, and the operations the route calls |
| The routing work (RWB-P4-E2013-APP) | The lookup answer with `COVERED`, `NOT_COVERED` and `RELATED_PARTY`, the incident reference and the event |
| The integration harness of wave 4 | The four operations, the message IDs, the event key and the fakes |

**Feature switch.** The table is behind `rwb.access.delegation-table`, owned by RWB-P4-E1038-APP; the contract declares the switch and no default value for it, and it declares that the lookup is not behind a second flag, because an answer that could be switched off would leave every approval route with no limit to check.

**Done when.** The OpenAPI document validates in the pipeline, the six contract tests pass, the six fakes answer every consumed path, the five invariants are stated as normative clauses, the event is declared with its key and payload, and the app story, the SCR-41 route work and the routing work have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, or a caller with no role row | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without the C letter in Reference data, or without the A letter in Rules and parameters | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The load reference is unknown or outside the caller's scope | This case is not in your scope. |
| MSG-GEN-001 | A required field is empty or a value is outside its list | Enter {field}. |
| MSG-GEN-004 | The version label exists, or the load is not `LOADED` | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The reference-data read, the parameter read or the store is unavailable | The service is busy. Try again in a few minutes. |
| MSG-P1-002 | The delegation file fails a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P7-002 | The approver is the load's author | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-010 | No limit covers the decision and the product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. |

The message IDs are contract elements, and each one the document uses has a catalogue entry, which the mapping test checks. The texts are the agreed texts: MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001 and MSG-P7-003 come from the legacy story, MSG-P1-002, MSG-P7-002 and MSG-P7-010 are kept from the source-data and decision catalogues rather than renumbered, and MSG-GEN-004 and MSG-GEN-006 are the service's generic state and availability messages (GAP-0837; ASM-1538).

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-41 Delegation of authority | Waiting | A load in `LOADED` with its row count, version label and valid-from date, from the load read |
| SCR-41 Delegation of authority | Approved | The answer of the approve operation: `APPROVED` from the valid-from date, the approver reference and the time |
| SCR-41 Delegation of authority | Refused | The 422 with MSG-P1-002 and its named row, the 403 with MSG-P7-002 and MSG-P4-002, and the 409 with MSG-GEN-004, each with its envelope |
| SCR-41 Delegation of authority | Not covered | The `NOT_COVERED` answer with MSG-P7-010 naming the decision and the product, and the `incidentReference`; rwb-decision raises the incident on the routing side and this service produces the answer and the reference only |
| SCR-41 Delegation of authority | Empty | Not specified in the source documents (CG-ALL-4836) |
| SCR-41 Delegation of authority | Loading | Not specified in the source documents (CG-ALL-4836) |
| SCR-41 Delegation of authority | Error | Not specified in the source documents (CG-ALL-4836) |
| SCR-41 Delegation of authority | No access | Not specified in the source documents (CG-ALL-4836) |

The screen is served by the gateway-bff composite route of DP-19, which calls the version read and this service's operations in one hop each and merges the answers. The composite route specification, the screen field list and the masking of any field on SCR-41 are the platform story's (RWB-PLT-N001-CON); this document fixes the access side of the merge only. SCR-39 Rules and parameters is not part of this contract: the rule-version approval is RWB-AD-011's. Its states are empty, loading, error and no access, each Not specified in the source documents (CG-ALL-4835).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-016-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the base, the four operations, the query `table` fixed to `delegation_limit`, the `Idempotency-Key` header and the error responses are present; the field formats are Not specified in the source documents (GAP-0840) |
| TC-AD-016-CON-02 | AC2 | Contract | `DoaLoad`, `DoaLoadAnswer` and `DoaLimitAnswer` carry their declared fields; `COVERED` and `NOT_COVERED`; L1 to L6; `RELATED_PARTY`; `limitVersion` mandatory with `COVERED`; the regulation item is free text of up to ten characters, checked for a repeated tuple, not against a list |
| TC-AD-016-CON-03 | AC3 | Contract | The 401, 403, 404, 409, 422 and 503 responses carry one envelope with MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P7-002, MSG-P7-003, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006, MSG-P1-002 and MSG-P7-010, each with a catalogue entry |
| TC-AD-016-CON-04 | AC4 | Contract | The three consumed operations carry their owner, one hop, the 2 s budget and the once-per-call clause; no P3 read is declared as provided |
| TC-AD-016-CON-05 | AC5 | Contract | The five clause sets: whole file or nothing, the falling limit, the two letters and the four eyes, the effective date with the readable older version, and the answer that names its version |
| TC-AD-016-CON-06 | AC6 | Component | The six fakes answer the documented paths and message IDs; the event key is `limitVersion`; an injected drift fails the build; the personal-data scan finds nothing |
| TC-AD-016-CON-07 | AC2, AC5 | Contract | Boundary of the tables of section 12.7: the `delegation_limit` columns DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 and the letters DF-REF-042 and DF-REF-043 at their declared edges, checked against the row shape and the authority input |

The seven cases test the baseline and only the baseline. The legacy test cases of this key, TC-AD-016-01 to TC-AD-016-04, and the five new application cases TC-AD-016-05 to TC-AD-016-09, are owned by RWB-P4-AD016-APP and are not repeated here.

### 17. Guardrails

- No business value in the contract: levels, limits, products, regulation items and version labels stay rows, the three lists stay reference data with a version, and the approver stays a right and a parameter row.
- No personal data in a schema, an example, a fake or the event payload: load references, codes, version labels, dates, amounts and user references only.
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the P3 list and parameter reads are consumed and documented as consumed (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- One writer of the table: the document declares no second insert path and no edit of an approved version, so two services can never own one limit.
- Whole file or nothing is an invariant, not a configuration: a load that could be stored in part would let an approval be routed by half a version.
- The four-eyes rule and the effective-date rule are invariants; the only switch the document names is the table's own feature switch, and it has no default value here.
- Every example in the document is synthetic; no production payload and no production limit is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit | The `DoaLoad`, `DoaLoadAnswer` and `DoaLimitAnswer` schemas; the query `table` fixed to `delegation_limit`; the whole-file and falling-limit clauses; the row shape of section 11 | TC-AD-016-CON-01, TC-AD-016-CON-02, TC-AD-016-CON-05, TC-AD-016-CON-07 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | The consumed list and parameter reads, the declared version labels of `limitVersion`, and the rule that no value is fixed in an example | TC-AD-016-CON-02, TC-AD-016-CON-04, TC-AD-016-CON-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The SCR-41 contract elements and the four states the route consumes, and the two letters behind the operations | TC-AD-016-CON-01, TC-AD-016-CON-03, TC-AD-016-CON-05 |

| Legacy reference | Where it is kept |
|---|---|
| The load of limits by decision, level, product and amount, and the approval by Risk | Sections 1, 7, 8, 12.1, 12.3 |
| The missing limit that goes to the next level up with an incident naming it | Sections 7, 8, 11, 12.1 |
| The whole-file refusal with MSG-P1-002, the falling limit and the unknown decision code | Sections 3, 7, 8, 12.1, 14 |
| The loader cannot approve, MSG-P7-002, and the 403 with MSG-P4-002 | Sections 3, 7, 8, 14 |
| The decision log entry of an approval, and the 503 with MSG-P7-003 | Sections 5, 7, 8, 12.1, 14 |
| SCR-41 Delegation of authority and SCR-39 Rules and parameters | Section 15 |
| The permission checks of the legacy story, with the two letters declared as the authorities | Sections 8, 10, 12.1, 14 |
| Legacy MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001 and MSG-P7-003 | Section 14 |
| Rule IDs R-UNI-38 and R-UNI-39 | Sections 2, 8, 17 |
| Field IDs DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062, DF-REF-042, DF-REF-043 | Sections 11, 12.7 |

### 19. Out of scope

- The implementation of the load, the approval, the load read and the lookup (RWB-P4-AD016-APP).
- The table `delegation_limit`, its migration, its index, the version window, the difference report, the rollback and the version read (RWB-P4-E1038-APP).
- The routing of an approval, its record and the central decision log entry (P7 `rwb-decision`), and the case status and decision task (P3 `rwb-case`).
- The router side of the lookup and the story that owns the routing journey (RWB-P4-E2013-APP, legacy RWB-E2-013); this contract fixes the answer it consumes.
- The rule-version load, its approval and the SCR-39 screen (RWB-AD-011).
- The reference-data and parameter store itself, its lists and their versions (P3 through DP-06 and DP-07).
- The gateway-bff composite route specification and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence; no `-ITG` story is split from this legacy key here.
- The deployment of this capability: the Helm values, the topics, the dashboards and the runbook.
