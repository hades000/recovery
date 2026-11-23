# RWB-P4-AD010-CON Approve a reference data load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD010-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-010 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the reference-load approval gate: an OpenAPI 3.1 document for the two `rwb-access` console operations, the `LovLoadApproval` schema, the return request with its coded reason list, the consumed `rwb-case` approve and list reads and the authorise operation, one RFC 9457 error envelope with the message IDs mapped, the four-eyes rule and the effective-from-valid-from rule stated as contract invariants, the contract tables of section 12 and the fakes**, so that **RWB-P4-AD010-APP, the SCR-40 route work and any later consumer can build the gate on Day 1 against a fixed, testable contract without waiting for `rwb-case` or for the access service to be built**.

The baseline fixes the naming the checks require: service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1` (DP-13), topic `rwb.access.events.v1` for the service, the shared `rwb.decision-record.v1` topic for the record (DP-03), task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story approved a reference load by writing an `approved_by` column on the list row, in the monolith, in one transaction, and the permission row behind it said that only a service identity could approve. In the target the store is `rwb-case`'s (`lov_value`, `reference_version`, `reference_row` under ASM-0071, and the approve path under ASM-0041) and the gate is `rwb-access`'s, so the gate needs a document that says exactly four things to the outside: what a refusal looks like, what an approved version looks like, what the gate consumes from the owner, and which two rules the gate will never break — nobody approves what they wrote, and nothing takes effect before its valid-from date.

If that field-level contract is agreed once and faked, the app story builds in parallel with the owner's store, a change in `rwb-case` is caught in a contract test instead of in an integration window, and the two paths that both look like "approve a reference load" (the console's and the owner's) are reconciled in writing rather than in an argument. This story meets REQ-DRI-011 (a versioned table carries its author and its approver), REQ-ACA-003 (the matrix is data and is the only source of what a role may do) and REQ-ACA-013 (the administration screens exist for the security administrator), and it applies R-UNI-38 and R-UNI-39 as contract invariants rather than as implementation notes.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners come from the ownership map only. The version store is P3 `rwb-case`'s under ASM-0071, and the reference-load approve path is P3's under ASM-0041; which path the console uses is Not specified in the source documents (GAP-0816; ASM-1517) and this document fixes the console side only.
- The legacy permission row "Reference data A: Service identities only" contradicts the legacy criterion in which a person approves. The contract takes TSD P4 v3 T6.1 as the source of rights and the legacy permission row as the row under correction (GAP-0817; ASM-1518).
- The effective-date behaviour of an approval given before the valid-from date is not specified in any source, so the contract states the stricter rule and the date is carried as a gap (GAP-0818; ASM-1519). The same holds for a service-identity author (GAP-0819; ASM-1520).
- MSG-P7-002 belongs to the decision centre's message catalogue and the legacy criterion uses it word for word; the contract keeps it and adds it to the P4 catalogue (GAP-0820; ASM-1521).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two console operations under the base `/api/recovery/access/v1`, with the shared components of the service.
2. Agree the `LovLoadApproval` schema, the return request and the coded reason list the return accepts.
3. Agree the three consumed operations with their owner, the one-hop rule, the 2 s budget and the breaker.
4. State the error envelope, the message-ID mapping and the refusal shapes for a self-approval, an absent right, an absent role, a version not in LOADED, an unknown load and an unwritable record.
5. State the two invariants — the four-eyes rule and the effective-from-valid-from rule — as normative clauses of the document, with no list-row write and no version-row write in the gate's own contract.
6. Declare the decision-record message this gate publishes and the absence of any event on `rwb.access.events.v1`.
7. Publish the contract tables of section 12 (nine sub-tables) and the fakes.
8. Add the contract tests: schema validation, error mapping, consumed-operation declarations, invariant clauses, fake drift and the personal-data scan.
9. Tag the baseline and hand it to RWB-P4-AD010-APP, the SCR-40 route work and every later consumer.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails the build; no baseline is tagged | None | AC1 |
| X2 | An operation declares no security right or omits an error response | The document review fails; a consumer cannot know what a refusal means | None | AC1 |
| X3 | A schema, an example or a fake carries a personal field | The personal-data scan fails the build | None | AC2, AC6 |
| X4 | A message id used by a response has no catalogue entry | The error mapping test fails | None | AC3 |
| X5 | A consumed operation is declared as provided, or an owner is missing | The review fails; the document names one owner per operation | None | AC4 |
| X6 | The document declares a write to a list or a version row | The invariant review fails; the gate never writes reference data | None | AC5 |
| X7 | A fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X8 | The coded reason list of the return is empty or unbounded | The review fails; the list is reference data with a version, not a free-text field | None | AC2 |
| X9 | A path or a topic of another service appears as this service's | The document is corrected; one base and one topic per service | None | AC1, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the P3 contract and the existing P4 contracts only |
| Negotiable | The field-level detail of the load answer and the coded reason list are settled with the owner and with data stewardship; the operations, the envelope and the two invariants are fixed by the target architecture |
| Valuable | Unblocks the app story and the SCR-40 route on Day 1, and keeps the reference store out of the access contract |
| Estimable | One document, one schema pair, one error envelope, two invariants, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Reference-load approval contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the approval gate is the authority, the four-eyes rule, the effective date and the record, and the version store is rwb-case's

  Scenario: AC1 The OpenAPI 3.1 document describes the two console operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/lov-loads/{loadId}/approve and POST /admin/lov-loads/{loadId}/return with the owner rwb-access
    Then both operations declare the Reference data right A, the Idempotency-Key header and the error responses 401, 403, 404, 409, 422 and 503
    Then no operation of another service is declared as provided by rwb-access

  Scenario: AC2 The approval answer and the return request carry the agreed fields (new, D-RCV-60)
    Given the LovLoadApproval schema and the return request of the document
    Then LovLoadApproval carries loadId, lovCode, version, state, validFrom, the approver reference and approvedAt
    Then state is one of LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED
    Then the return request carries reasonCode, whose values come from a coded reason list published as reference data with a version
    Then an empty or unknown reasonCode is a 422 response and not a default code
    Then no property of either schema is a name, an e-mail address or a personal field

  Scenario: AC3 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by either operation
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 or MSG-P7-002, 409 carries MSG-GEN-004, 422 carries MSG-GEN-001 and 503 carries MSG-P7-003
    Then every messageId used by the document has an entry in the message catalogue
    Then the response carries the problem media type and the trace identifier

  Scenario: AC4 The three consumed operations are declared as consumed (new, D-RCV-60)
    Given the owner's approve and list reads and this service's authorise operation
    Then each is declared in the consumed section with its owner, P3 rwb-case or P4 rwb-access
    Then each declares one hop and the 2 s client budget with a breaker
    Then the owner's approve path is declared as consumed and never as provided by rwb-access
    Then the document states that the gate calls the owner's approve once per gate decision and after the record is written

  Scenario: AC5 The four-eyes rule and the effective-from rule are contract invariants (new, D-RCV-60)
    Given the normative clauses of the document
    Then the four-eyes clause says the approver reference must differ from the load's author reference, that a service identity may not approve and that a person may approve a load a service identity wrote
    Then the effective-date clause says a version takes effect from its validFrom date only, never retroactively, and that the superseded version keeps validTo set to the day before
    Then the document carries no write to lov_value, reference_version or reference_row and names no table of rwb_case as its own
    Then the authority is declared as the A letter in Reference data read from role and permission, with no hard-coded role name in any example

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of section 12.8
    When the contract tests run
    Then each fake answers the paths and payloads of the document with the declared status codes and message IDs
    Then a drifted fake fails the build
    Then no schema, example or fake carries a name, an e-mail address or a personal field
```

These six criteria test the artefact only. This story owns no legacy acceptance criterion: the two legacy criteria of RWB-AD-010 belong to RWB-P4-AD010-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path as its own | DP-13; Architecture v5 slide 41 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1; ASM-0041 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR4 | The approver reference must differ from the load's author reference; a service identity may not approve and a person may approve a load a service identity wrote | Legacy RWB-AD-010 AC2; MSG-P7-002; ASM-1520 |
| BR5 | A version takes effect from its `validFrom` date only and never retroactively; the superseded version keeps `validTo` on the day before | Legacy RWB-AD-010 AC1; TSD P4 v3 T4; R-UNI-38; ASM-1519 |
| BR6 | The gate writes no list row and no version row; the version transition is the owner's and is consumed, not defined | DP-01; ASM-0071 |
| BR7 | Every operation that changes a decision carries `Idempotency-Key`, and a repeat answers the stored answer | Architecture v5 slide 11 |
| BR8 | The authority is the A letter in Reference data, resolved from the `role` and `permission` rows; no role name is a constant in the document, an example or a fake | REQ-ACA-003; TSD P4 v3 T6.1; ASM-1518 |
| BR9 | A schema change is additive within a major version; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |
| BR10 | No schema, example or fake carries personal data; staff references, codes, dates and states only | Requirement NFR-040; DP-05 |

### 9. State transitions

The document is the object with a lifecycle; the version states it declares are the owner's.

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the three consumed operations and the two invariants are described | In review |
| In review | Consumer sign-off | The app story and the SCR-40 route work accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A message ID change | A catalogue entry is renamed | Rejected: a message ID is stable once published |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the error envelope and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Tech lead of rwb-case (P3) | Reviews the two consumed operations, the version states, the author and approver references and the coded reason list; owns their definitions |
| Security administrator role owner | Confirms that the A letter in Reference data is the declared authority and that the legacy permission row is corrected |
| Data steward | Confirms that no personal data field is declared in a schema, an example or a fake |
| QA and the integration team | Review the contract tests and the drift rule |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Approval answer | `loadId`, `lovCode`, `version`, `state`, `validFrom`, `approverReference`, `approvedAt`; `state` one of the TSD P4 v3 T4 values LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED |
| Return request | `reasonCode`, from the coded reason list published as reference data with a version |
| Return answer | The approval answer with `state` LOADED and `reasonCode` |
| Record entry | The decision code REF-APPR, REF-DENY or REF-RTRN; the load, the list, the version, the effective date, the approver reference and the outcome |
| Authority input | The caller's `permission` row with `capability_area` REFERENCE_DATA and its `letters` (DF-REF-042, DF-REF-043) |
| Load read | The version, its `lovCode`, its `author` reference, its `state`, its `validFrom` and `validTo`, from `reference_version` of `rwb-case` (DF-REF-159 to DF-REF-184) |
| Event payload | The record entry, CloudEvents 1.0 envelope, no personal field |
| Refusals | `messageId` MSG-P4-001, MSG-P4-002, MSG-P7-002, MSG-GEN-004 or MSG-P7-003 with the field list |

The exact field-level schema of the approval answer — string lengths, the maximum page of the list read and the members of the coded reason list — is Not specified in the source documents (GAP-0816; ASM-1517). This baseline fixes the field names above and leaves the field-level detail, the reason list members and the number of reason codes to the review; the load data itself is declared only as consumed and never as owned.

### 12. Contract

#### 12.1 REST operations provided

Owner P4 `rwb-access`; base `/api/recovery/access/v1` (DP-13).

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/lov-loads/{loadId}/approve` | No request body; `LovLoadApproval` answer: `loadId`, `lovCode`, `version`, `state`, `validFrom`, `approverReference`, `approvedAt` | Reference data A, scope applied; `Idempotency-Key` required |
| POST | `/admin/lov-loads/{loadId}/return` | `ReturnRequest`: `reasonCode` from the coded reason list; `LovLoadApproval` answer with `state` LOADED and `reasonCode` | Reference data A, scope applied; `Idempotency-Key` required |

Errors for both: 401 no session (MSG-P4-001), 403 no right or a self-approval (MSG-P4-002, MSG-P7-002), 404 unknown load, 409 version not in LOADED (MSG-GEN-004), 422 empty or unknown field (MSG-GEN-001), 503 owner unavailable or record not written (MSG-P7-003). The 403 that is a self-approval carries `code` SELF_APPROVAL and `messageId` MSG-P7-002, so a consumer can tell it apart from an absent right without reading the text.

The legacy path of the approval was `/admin/reference-loads/{loadId}/approve` under the single monolith base that DP-13 replaces, with the right "Reference data A"; it is TSD P4 v3 appendix T-A endpoint API-P4-006 under the per-service base of DP-13. The ownership map rules that path P3 `rwb-case`'s under ASM-0041 because the version store is the reference-data store, so the document keeps a console path under this service's base and declares the owner's path as consumed. Which path the console uses is Not specified in the source documents (GAP-0816; ASM-1517).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 `rwb-case` | The version transition LOADED to APPROVED and to IN_FORCE from `validFrom`; answers the moved version; called once per gate decision, after the record is written |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | The version, its author reference, its state, its `validFrom` and `validTo`, and the coded return reasons |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own) | The A letter in Reference data, with the MSG-P4-002 refusal shape |

None of the three is declared as provided by this story, and none is called twice in one gate decision.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The record entry with the decision code, the load, the list, the version, the effective date, the approver reference and the outcome; CloudEvents 1.0 envelope; no personal field |

Nothing is published on `rwb.access.events.v1` by this story. `AccessPolicyChanged` and `DoaLimitChanged` are events of other capabilities of the service, and the reference-data change is `rwb-case`'s to publish.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this contract adds no subscription.

#### 12.5 Workflows and activities

None. The gate is one synchronous command with one downstream call; the document declares no workflow ID, no activity name and no task-queue registration.

#### 12.6 Schedules

None. The six-monthly access review Schedule belongs to another capability of the service and is not part of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's role and class, behind the authority answer |
| `permission` | P4 (`rwb_access`) | The A letter in REFERENCE_DATA (DF-REF-042, DF-REF-043) |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_access` | The record outbox row and the stored answer of each call; no inbox row, because no event is consumed (DP-09) |

No list table is owned and no version table is named as this service's: `lov_value`, `reference_version` and `reference_row` are P3 `rwb_case`'s under ASM-0071 and appear only as consumed shapes, and `decision_log_entry` is P7's (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case reference-data WireMock | `GET /admin/lists/{listCode}`: version "LOV-ROUTE 2027.01" in force from 1 January 2027, author "U-4101", approver "U-4201", at least one version in each of the six states, a version in LOADED with author "U-4211", the coded reason list with "REF-RSN-03", a 404 for an unknown load and a 503 for the unavailable case | App story, contract tests, SCR-40 route work |
| rwb-case approve fake | `POST /admin/reference-loads/{loadId}/approve`: the moved version in APPROVED and in IN_FORCE from 1 January 2027; a 409 when the version is no longer LOADED; a timeout beyond 2 s | App story, contract tests |
| parameters fake | The four-eyes switch row on and the approval-limit rows of the load, read with the version in force (DP-06) | App story, contract tests |
| decision-record fake | The record append for REF-APPR, REF-DENY and REF-RTRN, the hash-chain check and a forced failure | App story, contract tests |
| authorise and gateway-bff fakes | The authorise answer with the A letter for RW-REFADM, the MSG-P4-002 refusal for RW-RISK, the MSG-P4-001 answer for no role, and the SCR-40 composite route with the four states | App story, SCR-40 route work |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | Two console operations on `/api/recovery/access/v1`; the owner's approve and list reads, and this service's own authorise operation; one hop, 2 s timeout |
| Kafka | 1 published type, 0 consumed | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | 0 workflows, 0 activities | No workflow in the gate |
| File | None | The load file is not part of this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-referenceload-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml` with the message-ID map, `contract/lov-load-approval.yaml` with the answer and the return request, the normative clause file with the four-eyes and effective-date invariants, the coded reason list declaration, the contract README with the idempotency and versioning rules, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 appears in the contract as one rule: the approver's staff reference and group resolve through `v_ace_iam_group` inside the service, and no schema, example or fake carries a name or an e-mail address that could have come from it. DP-06 appears as the declaration that the four-eyes switch and the approval limits are parameter rows with a version, so a switch change is a data change and the contract declares no default value for it.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the shared components and the error responses; schema lint in the pipeline.
2. The two console operations with the shapes of section 11 and the `Idempotency-Key` header on both.
3. The three consumed operations with their owners, the one-hop rule, the 2 s budget and the once-per-decision clause.
4. The error envelope and the message-ID map, with the texts of section 14 copied unchanged.
5. The `LovLoadApproval` schema, the return request and the coded reason list declaration.
6. The two normative clauses: the four-eyes rule with its service-identity case, and the effective-from-valid-from rule with the superseded `validTo` on the day before.
7. The five fakes and their stub fixtures of section 12.8.
8. The six contract tests, including the personal-data scan and the drift test.
9. Baseline tag and the consumer sign-off note from the app story, the SCR-40 route work and the P3 owner.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD010-APP | The two provided operations, the answer schema, the reason list and all five fakes |
| The SCR-40 route work (RWB-PLT-N001-CON) | The states waiting, approved, refused and returned, and the two operations the route calls |
| RWB-P3-E1043-CON owner (P3 rwb-case) | That the owner's approve and list reads are declared as consumed and that no version state is defined here |
| The integration harness of wave 4 | The two operations, the message IDs and the fakes |

**Feature switch.** The gate is not behind a flag in this contract: an approval path that could be switched off would leave reference data with no owner. The four-eyes switch is a parameter row and is declared as such, with the rule kept as an invariant so that turning it off is a recorded data change and not a silent fallback.

**Done when.** The OpenAPI document validates in the pipeline, the six contract tests pass, the five fakes answer every consumed path, the two invariants are stated as normative clauses, and the app story, the SCR-40 route work and the P3 owner have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, or a caller with no role row | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the A letter in Reference data | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The load's list is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-001 | A required field is empty or a code is not in its list | Enter {field}. |
| MSG-GEN-004 | The version is not in LOADED | Someone else changed this record. Reload it to see their change. |
| MSG-P7-002 | The approver is the load's author | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The decision record could not be written, or the owner did not answer | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements, and each one the document uses has a catalogue entry, which the mapping test checks. The texts are the agreed texts taken from the legacy story where the message already existed.

MSG-P7-002 is a decision-centre message: the same separation-of-duty rule refuses an approver who prepared the decision, and the legacy criterion of RWB-AD-010 uses that id word for word. The contract therefore reuses it rather than renumbering the refusal, and the catalogue carries it for both places (GAP-0820; ASM-1521). Two ids for one rule would let an approver read the same refusal as two different things.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-40 Reference data | Waiting | The versions in LOADED with their author reference and valid-from date, from the owner's list read, and the approve operation |
| SCR-40 Reference data | Approved | The answer of the approve operation: state IN_FORCE from the valid-from date, the approver reference and the time |
| SCR-40 Reference data | Refused | The 403 refusals with MSG-P7-002 and MSG-P4-002, and the 409 with MSG-GEN-004, each with its envelope |
| SCR-40 Reference data | Returned | The answer of the return operation: state LOADED with the reason code shown to the author |

The screen is served by the gateway-bff composite route of DP-19, which calls the owner's list read and this service's operations in one hop each and merges the answers. The composite route specification, the screen field list and the masking of any field on SCR-40 are the platform story's (RWB-PLT-N001-CON); this document fixes the access side of the merge only. SCR-39 Rules and parameters is not part of this contract: the rule-version approval is RWB-AD-011's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-010-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the base, the two operations, right A, the `Idempotency-Key` header and the six error responses are present |
| TC-AD-010-CON-02 | AC2 | Contract | `LovLoadApproval` and the return request carry their declared fields; the six states; the coded reason list; a 422 for an empty or unknown code |
| TC-AD-010-CON-03 | AC3 | Contract | The 401, 403, 404, 409, 422 and 503 responses carry one envelope with MSG-P4-001, MSG-P4-002, MSG-P7-002, MSG-GEN-004, MSG-GEN-001 and MSG-P7-003, each with a catalogue entry |
| TC-AD-010-CON-04 | AC4 | Contract | The three consumed operations carry their owner, one hop, the 2 s budget and the once-per-decision clause; no owner path is declared as provided |
| TC-AD-010-CON-05 | AC5 | Contract | The four-eyes clause with its service-identity case, the effective-from-valid-from clause, no list or version write, and no hard-coded role name |
| TC-AD-010-CON-06 | AC6 | Component | The five fakes answer the documented paths and message IDs; an injected drift fails the build; the personal-data scan finds nothing |

### 17. Guardrails

- No business value in the contract: the reason codes, the capability area, the four-eyes switch and the approval limits stay data in the reference and parameter rows, read with the version in force.
- No personal data in a schema, an example or a fake: load references, list codes, version labels, dates, states and staff references only.
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the owner's approve and list reads are consumed and documented as consumed (DP-01, ASM-0071, ASM-0041).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- Every example in the document is synthetic; no production payload and no production list value is copied into a schema or a fake.
- The gate declares no write to reference data: a contract that let the gate move a version would put two writers on one table (BR6).
- The four-eyes rule and the effective-date rule are invariants, not configuration: the parameter switch may turn the rule off only as a recorded data change, and the contract says so.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-011 | Versioned reference data with valid-from and valid-to dates, author and approver | The `LovLoadApproval` fields `version`, `state`, `validFrom` and the approver reference; the consumed list read with the author; the effective-date invariant; the record entry | TC-AD-010-CON-02, TC-AD-010-CON-04, TC-AD-010-CON-05 |
| REQ-ACA-003 | The role to permission matrix is data and the only source of what a role may do | Right A in Reference data on both operations, resolved through the authorise operation; no role name in the document | TC-AD-010-CON-01, TC-AD-010-CON-03, TC-AD-010-CON-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation for the security administrator | The SCR-40 contract elements and the four states the route consumes | TC-AD-010-CON-02, TC-AD-010-CON-06 |

| Legacy reference | Where it is kept |
|---|---|
| The approval of a loaded version, effective from its valid-from date, and the logged approval | Sections 1, 5, 7, 8, 12.1, 12.3, 14 |
| The maker may not approve, refused with MSG-P7-002 | Sections 3, 7, 8, 14 |
| The reference-data approve path of TSD P4 appendix T-A, API-P4-006, now P3's | Sections 3, 12.1, 12.2 |
| SCR-40 Reference data and its four states | Section 15 |
| The permission checks of the legacy story, with the Reference data row corrected | Sections 8, 10, 12.1, 14 |
| Legacy MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | Section 14 |
| Rule IDs R-UNI-38 and R-UNI-39 | Sections 2, 8, 17 |
| Field IDs DF-REF-042, DF-REF-043, DF-REF-159 to DF-REF-184, DF-DEC-001 to DF-DEC-018 | Section 11 |

### 19. Out of scope

- The implementation of the gate, its four-eyes rule, its record and its screen calls (RWB-P4-AD010-APP).
- Loading a list of values version, the file, the row checks and the version store (RWB-P4-AD009-APP with `rwb-case`).
- The version transition and the six version states, which are `rwb-case`'s under ASM-0071 and ASM-0041; this contract consumes them and defines none of them.
- The rule-version load and approval and the SCR-39 screen (RWB-AD-011).
- The delegation of authority table and its approval path (RWB-P4-E1038-APP).
- The service baseline contract of `rwb-access`: the authorise operation, the session read, the masking policies and the access log are RWB-P4-E1037-CON's and are consumed here.
- The gateway-bff composite route specification and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence; no `-ITG` story is split from this legacy key.
- The deployment of this capability: the Helm values, the topics, the dashboards and the runbook.
