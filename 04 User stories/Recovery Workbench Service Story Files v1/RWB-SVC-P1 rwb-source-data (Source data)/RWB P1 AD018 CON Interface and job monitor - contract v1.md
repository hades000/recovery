# RWB-P1-AD018-CON Interface and job monitor

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-AD018-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the monitor capability of rwb-source-data — `GET /api/recovery/source-data/v1/admin/jobs`, `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` and the freshness answer, the `Job` and `DataProductFreshness` resources with the run-log element, the error envelope with the two 409 conditions, the Idempotency-Key rule, the nine contract tables and the four fakes**, so that **the app, operations and test stories of this legacy key build on Day 1 against one fixed and testable contract and a run column, a status code or a check result can never drift between rwb-source-data, gateway-bff and rwb-integration without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The monitor is the one screen an operator reads before 09:00, and it is the only reader of the run record: if the status vocabulary or the two 409 conditions are left to the implementation, a WAITING job can be shown as failed and a permitted rerun can be refused, or worse, a rerun can be accepted while the ACE batch is late. The baseline fixes the vocabulary, the four status codes and the meaning of "last complete ACE business date" once.

The baseline also fixes the naming the checks rely on: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-13, DP-14). It declares no event of its own: the two ACE batch events of the service stay with RWB-P1-E1015-CON and RWB-P1-E1015-APP.

The boundary with the sibling contract story is explicit: **RWB-P1-E1015-CON owns the `DataProductFreshness` resource and its freshness semantics**; this document declares the answer as served and fixes only the stale flag and the ACE date the monitor shows, and it never restates the stamp fields. **RWB-P1-E1069-CON** owns the ACE read path; this document names `v_ace_batch_status` as a consumed element and defines no view.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the topic and the event names follow the platform rule.
- The platform error envelope, the CloudEvents 1.0 envelope, the retry and `.dlt` topic convention and the Idempotency-Key rule are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- RWB-P1-E1015-CON is published or in review, so the freshness resource is referenced and not redefined.
- RWB-PLT-E1056-OPS loads the catalogue baseline as data, so the catalogue fields of the `Job` resource are the catalogue columns and not a document invention.
- The run-log table has no name and no field list in the logical model: its shape is Not specified in the source documents (GAP-2163; ASM-3464) and this baseline fixes the names it declares.
- The outbound-action answer of rwb-integration has no operation row in the sources (GAP-2163; ASM-3465); it is declared as consumed and faked, never as provided.
- The right enforcement path (platform session or rwb-access authorise) is not a listed dependency of this legacy key (GAP-2163; ASM-3466); the document names the right, not the mechanism.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document: the `Job` resource with its run element and its checks, the `DataProductFreshness` answer, and the error envelope of the three operations.
2. Fix the status vocabulary of a run (PENDING, RUNNING, COMPLETE, FAILED, WAITING) and the meaning of each date field, so no consumer computes a duration or a wait state on its own.
3. Fix the two 409 conditions of the rerun and the Idempotency-Key rule in the same document, with one example each.
4. Record the consumed element of rwb-integration with its owner, its use, the 2 s budget and the empty-column behaviour, and the ACE read element of the service's own view path.
5. Record the freshness answer as served here and owned by RWB-P1-E1015-CON, with the stale flag and the ACE date only.
6. Publish the nine contract tables of section 12 and the four fakes.
7. Add the contract tests: schema validation, the status vocabulary, the additive rule, the error mapping, the 409 rules, the drift between a fake and the document.
8. Tag the baseline and hand it to RWB-P1-AD018-APP, RWB-P1-AD018-OPS, RWB-P1-E1015-CON and the wave 4 harness RWB-ITG-AD018-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed, retyped or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | The status vocabulary drifts from the five run states | The vocabulary test fails the build | None | AC2 |
| X4 | A 409 is documented without its condition, or a condition without its code | The error-mapping test fails | None | AC3 |
| X5 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X6 | The freshness answer is redefined here, or the sibling document changes it | The boundary test fails and the field is fixed in one document only | None | AC6 |
| X7 | A consumed path has no Ownership Map row | The row carries the placeholder, the gap and the assumption, and the fake is derived from the owner's published document | None | AC4 |
| X8 | A personal field appears in a resource, an example or a fake | The PII lint fails the build | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reuses the platform envelopes, the Ownership Map and the published document of rwb-source-data and its siblings |
| Negotiable | Field lengths and examples are settled in the baseline review; the operations, the status vocabulary and the two 409 conditions are fixed by the target |
| Valuable | Unblocks the app, operations and test stories and fixes the meaning of a wait state for the operator |
| Estimable | Two artefacts' worth of document, two resources, one consumed row, nine contract tables, four fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the interface and job monitor

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-source-data base is /api/recovery/source-data/v1 and the schema is rwb_source_data
    Given the monitor story RWB-P1-AD018-APP is the writer this baseline serves

  Scenario: AC1 The OpenAPI document declares the three operations and the Job resource (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /admin/jobs, POST /admin/jobs/{jobId}/rerun and GET /data-products/freshness under the base /api/recovery/source-data/v1 and owned by rwb-source-data
    Then the Job resource carries jobId, jobName, ownerRole, scheduleText, expectedMinutes, alertAfterMinutes, firstRelease, businessDate, runNo, status, startedAt, finishedAt, durationMinutes, lastAceBusinessDate and the check array
    Then each check element carries its code, its result and its count
    Then status is one of PENDING, RUNNING, COMPLETE, FAILED and WAITING and is a closed list in the document
    Then lastAceBusinessDate is optional and is defined as the last complete business date of the source in v_ace_batch_status
    Then the rerun operation requires an Idempotency-Key and the two reads declare none
    Then every property is additive within major version 1

  Scenario: AC2 The run states and the dates have one meaning for every consumer (new, D-RCV-60)
    Given the Job resource and its status list
    When each state is reviewed against the monitor behaviour
    Then PENDING means accepted and not started, RUNNING means started with startedAt, COMPLETE means finished with finishedAt and durationMinutes
    Then FAILED means finished with a failed check and its message ID, and WAITING means not started because the source batch is not complete
    Then WAITING is never reported as FAILED and never carries finishedAt
    Then durationMinutes is present only for COMPLETE and FAILED
    Then runNo starts at 1 and increases by one per attempt of the same job and business date, so a rerun adds a run and never replaces one
    Then no consumer is required to compute a duration or a wait state from the other fields

  Scenario: AC3 The error envelope and the two 409 conditions are fixed (new, D-RCV-60)
    Given the error responses of the three operations
    When they are reviewed against the message register and the run states
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 with the Platform administration right, 404 carries MSG-GEN-001 for an unknown job and 503 carries the platform unavailable text
    Then 409 is declared for a rerun asked while a run of the job is RUNNING and for a business date no source row of v_ace_batch_status shows complete
    Then the 409 answer carries MSG-P1-001 with the product and its last complete date for the incomplete date case
    Then 400 is declared for a malformed query parameter
    Then MSG-P1-001, MSG-GEN-001 and MSG-P4-002 are copied unchanged from the legacy story
    Then no error answer carries a customer field, an amount or an internal identifier of another service

  Scenario: AC4 The consumed elements carry their owner and the placeholder where the source is silent (new, D-RCV-60)
    Given the consumed elements of the document
    When they are compared with the Ownership Map
    Then the outbound-action answer names P2 rwb-integration as its owner and its path carries the placeholder Not specified in the source documents (GAP-2163; ASM-3465)
    Then the answer is declared as consumed, one hop, 2 s, GET retried once with jitter, and as empty with its own marker when it fails
    Then v_ace_batch_status is declared as read through the service's own recovery.v_ace_* path and never as a public table
    Then the freshness element is declared as owned by RWB-P1-E1015-CON and is not restated field by field
    Then the run-log element carries the placeholder of its table name and field list (GAP-2163; ASM-3464)
    Then the right is named as a right and the enforcement mechanism is not fixed by this document (GAP-2163; ASM-3466)

  Scenario: AC5 The four contract fakes match the document and drift fails the build (new, D-RCV-60)
    Given the four fakes of section 12.8
    When the drift test compares each fake with the document
    Then the rwb-integration fake answers a COMPLETE and a FAILED outbound action for 2026-11-30, and a delayed answer beyond 2 s
    Then the view fixture answers a complete source, a source with no complete row, a FAILED source and an unavailable answer
    Then the session fake answers the R right, the U right and a refused right
    Then the run-log fixture answers a FAILED run with its check and a run log that refuses its write
    Then a changed field, a changed status code, a changed status value or a changed payload in any fake fails the build

  Scenario: AC6 The nine contract tables are complete and the retired elements are absent (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.3 and 12.4 record None and name the two ACE batch events as owned by RWB-P1-E1015-APP
    Then 12.6 records None and names JOB-01 and JOB-09 as retired
    Then the document declares no operation that starts, stops or reruns an ACE batch, a feed or a file
    Then no personal data field is declared in a resource, an example or a fake
```

These six criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P1-AD018-APP. The wave 4 harness RWB-ITG-AD018-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; the document never declares another service's path as provided | DP-13; Template and Rules §R4 |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`; this document declares no event of its own | DP-14; RWB-P1-E1015-CON |
| BR3 | A read declares no Idempotency-Key; the rerun declares one and stores its answer | TSD API-P1-002; DP-09 |
| BR4 | One error envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Template and Rules §R7.2 s14 |
| BR5 | The run status is a closed list of five values and WAITING is distinct from FAILED | RWB-AD-018 AC3; RWB-P1-AD018-APP BR3 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-source-data; the freshness resource stays owned by RWB-P1-E1015-CON | Ownership Map v1; DP-01 |
| BR8 | No operation starts, stops or reruns an ACE batch, a feed or a file | RWB-AD-018 guardrail; NFR-015 |
| BR9 | No business value is fixed in the contract: job names, cadences, expected durations, alert minutes and thresholds stay catalogue or values rows | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the two resources and the run states are described | In review |
| In review | Consumer sign-off | The app, operations and test stories, RWB-P1-E1015-CON and RWB-PLT-N001-CON accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or the status list changes | New major version drafted |
| Baselined | Drift in a fake | The drift test of AC5 fails | In review |
| Baselined | Retired element reappears | The absence test of AC6 fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the OpenAPI document and the four fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the field-level detail of the run log |
| Consuming teams (app, operations, test, the P2, P4 and P1 sibling owners, RWB-PLT-N001-CON) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the CloudEvents envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer or a fake |

The per-service login behind the security scheme is not part of this baseline; the document names the scheme "the rwb-source-data login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Job resource | `jobId`, `jobName`, `ownerRole`, `scheduleText`, `expectedMinutes`, `alertAfterMinutes`, `firstRelease` from `job_catalog` DF-OPS-225 to DF-OPS-232 |
| Run element | `businessDate`, `runNo`, `status`, `startedAt`, `finishedAt`, `durationMinutes`, the check array and `messageId`; the table name and field list are Not specified in the source documents (GAP-2163; ASM-3464) |
| ACE date element | `lastAceBusinessDate` and `sourceSystem`, from `v_ace_batch_status` DF-ACE-178 to DF-ACE-186, read through the service's own view path |
| Freshness answer | `productCode`, `businessDate`, `status`, `sourceSystem`, `sourceExtractedAt`, `staleFlaggedAt`; owned by RWB-P1-E1015-CON, referenced here and not restated |
| Consumed answer | The outbound actions of P2; only IDs, codes, dates and counts are declared |

This story fixes the names, the types and the meaning of the run element only. Nothing in the document carries a customer identifier, an amount or a name.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/jobs` | `Job[]` with the catalogue fields, the latest run, its checks and `lastAceBusinessDate`; query `jobCode`, `status`, `from`, `to` | Platform administration R, scope applied |
| POST | `/admin/jobs/{jobId}/rerun` | `Job` of the new run with `runNo` increased by one; Idempotency-Key required | Platform administration U, scope applied |
| GET | `/data-products/freshness` | `DataProductFreshness[]` with the stale flag and the ACE completion time; query `product`, `asOf` | Platform administration R in this story; the resource is owned by RWB-P1-E1015-CON |

All three answer 401, 403, 503 and 400 for a malformed query; the rerun adds 404 and the two 409 conditions of AC3. The freshness resource is declared as served and not redefined: RWB-P1-E1015-CON owns its fields and its semantics.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | Not specified in the source documents (GAP-2163; ASM-3465) | P2 rwb-integration | The outbound actions of the business date with their status, duration and checks; one hop, 2 s, faked, and empty with its own marker when it fails |

The row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream, and it is not a build dependency of any story of this legacy key. The Platform administration right is taken from the platform session and is not declared as a consumed operation here (GAP-2163; ASM-3466).

#### 12.3 Events published

None. This baseline declares no event: `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` are owned by RWB-P1-E1015-CON and are referenced there, and the monitor publishes nothing.

#### 12.4 Events consumed

None. The wait state is read from `v_ace_batch_status` in-service, not from a consumed event; the two ACE batch events of the service are consumed by RWB-P1-E1015-APP and are not consumed here.

#### 12.5 Workflows and activities

None declared. The rerun starts the owning job of the service, for example `ReconciliationWorkflow` of RWB-P1-E1011-APP on task queue `rwb-source-data`; the baseline names it as the started workflow and fixes no activity of its own.

#### 12.6 Schedules

None. The baseline registers no Schedule and no Quartz trigger; JOB-04 and the case-list steps start on the ACE batch record, and `JOB-01` and `JOB-09` stay retired (FSD P1 v3). The absence test fails a document that declares a monitor Schedule or a monitor job.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| job_catalog | P1 (rwb_source_data) | The catalogue fields of the `Job` resource |
| run log (name pending, GAP-2163) | P1 (rwb_source_data) | The run element, its checks and `runNo` |
| data_product_load | P1 (rwb_source_data) | The freshness answer, served here and stamped by RWB-P1-E1015-APP |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_source_data | The Idempotency-Key of the rerun |

`v_ace_batch_status` is an ACE view read only through `recovery.v_ace_*`; the document declares no foreign key into another schema and no second service's table (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-integration outbound-action fake | A COMPLETE and a FAILED outbound action for 2026-11-30 with their checks, and a delayed answer beyond 2 s | App story, operations smoke profile, contract tests |
| `v_ace_batch_status` fixture | Sources complete for 2026-11-30, a source with no complete row, a FAILED source and an unavailable answer | App story, contract tests |
| Session and role fake | The R right granted, the U right granted and the U right refused | App story, operations smoke profile, contract tests |
| Run-log fixture | A FAILED run with its check and message ID, a COMPLETE run, and a store that refuses its write | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 1 consumed as a fake | The two admin operations and the freshness answer; the outbound actions of P2, one hop, 2 s |
| Kafka | None | No event declared here; the two ACE batch events stay with RWB-P1-E1015-CON |
| Temporal | 1 workflow named as started, no Schedule | The owning job's workflow on `rwb-source-data` |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The change to `openapi/rwb-source-data-v1.yaml` with the `Job` resource, the run element and the two admin operations, the README rows for the status vocabulary and the two 409 conditions, the boundary note with RWB-P1-E1015-CON and RWB-P1-E1069-CON, and the four fake assets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/source-data/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | none for this document; H RWB-PLT-N001-CON in the app story |

The rows record what the baseline has to describe; no dependency is a build dependency of this story, which is Day 1 by rule.

**Build steps**

1. Add the `Job` resource, the run element and the check array, with the five status values as a closed list and the optionality of `lastAceBusinessDate`.
2. Add the two admin operations with their query parameters, their security right and their Idempotency-Key rule; declare the freshness answer as served.
3. Write the status-vocabulary test and the duration rule of AC2, and the additive test of AC1.
4. Write the error map of AC3, including the two 409 conditions and their message IDs.
5. Record the consumed row with its owner and its placeholder, the ACE read element and the run-log placeholder of AC4.
6. Publish the four fakes and the six contract tests; a drift between a fake and the document fails the build.
7. Add the absence test for a monitor Schedule, a monitor job and an ACE rerun operation, and the PII lint of AC6.
8. Baseline tag and the consumer sign-off note, including RWB-P1-E1015-CON, RWB-PLT-N001-CON and the wave 4 harness.

**Done when.** The OpenAPI artefact validates in the pipeline, the six contract tests pass, the four fakes answer every consumed path and the drift test is green, and the app, operations and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The freshness stamp is stale, or the business date is not complete | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A required field is missing, or the job code is unknown | Enter {field}. |
| MSG-P4-002 | The role lacks Platform administration R or U | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No session on a read or a rerun | Your session has ended. Sign in again. |

The three legacy texts are copied unchanged; MSG-P4-001 is the platform envelope text. Thai text follows DL10. This document adds no message ID.

### 15. Screens and states

The contract serves SCR-44 Interface and job monitor in its four states — Running, failed, waiting for the ACE batch, complete — through the gateway-bff composite route (DP-19). It fixes the three answers and the status vocabulary only: the screen composition and the field list belong to RWB-PLT-N001-CON, and the panels are built by RWB-P1-AD018-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-AD018-CON-01 | AC1 | Contract | The document validates; three operations; the `Job` fields; the closed status list; the Idempotency-Key rule |
| TC-P1-AD018-CON-02 | AC2 | Contract | The five states with their dates and durations; `runNo` 1 then 2; WAITING never FAILED |
| TC-P1-AD018-CON-03 | AC3 | Component | 400, 401, 403, 404, 409 twice and 503 with their message IDs; the two 409 conditions |
| TC-P1-AD018-CON-04 | AC4 | Component | One consumed row with its owner and placeholder; the ACE read element; the freshness boundary; two placeholders |
| TC-P1-AD018-CON-05 | AC5 | Component | Four fakes compared with the document; a changed field, code, status value or payload fails the build |
| TC-P1-AD018-CON-06 | AC6 | Component | The nine sub-tables with owners; 12.3, 12.4 and 12.6 None; no ACE rerun operation; the PII lint |

The four legacy test cases TC-AD-018-01 to TC-AD-018-04 are owned by RWB-P1-AD018-APP and RWB-ITG-AD018-ITG, which copies them with the `-ITG` suffix; a contract story owns no business outcome and therefore no legacy test case.

### 17. Guardrails

- No business value in the contract: job names, cadences, expected durations, alert minutes and thresholds stay catalogue or values rows.
- No personal data in a schema, an example or a fake: IDs, codes, dates and counts only.
- The contract names only rwb-source-data tables and only operations owned by rwb-source-data; the freshness resource is referenced, the outbound actions are consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document naming another service's base or topic as its own fails the review (DP-13, DP-14).
- ACE data is reached only through the service's own `recovery.v_ace_*` path; no `public` table and no cross-schema join is declared.
- No retired element is reintroduced: the absence test of AC6 fails a document that declares a monitor Schedule, a monitor job or an ACE rerun operation.
- Every example is synthetic; no production payload is copied into a schema, an example or a fake.
- The error envelope and the naming rule come from the platform library; this story narrows them and never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel | The `Job` resource with `runbookPath` and the run element | TC-P1-AD018-CON-01, TC-P1-AD018-CON-02 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | The FAILED state, its message ID and the alert minutes of the catalogue | TC-P1-AD018-CON-02, TC-P1-AD018-CON-03 |
| REQ-DRI-007 | Every outbound file is logged, retried and placed in a named exception queue on failure | The consumed outbound-action row and its empty-column marker | TC-P1-AD018-CON-02, TC-P1-AD018-CON-04 |
| REQ-DRI-008 | The Workbench runs no inbound batch; work starts when ACE records the batch complete | `lastAceBusinessDate`, the WAITING state and the absence of an ACE rerun operation | TC-P1-AD018-CON-02, TC-P1-AD018-CON-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed row with its budget, retry and breaker | TC-P1-AD018-CON-04 |

### 19. Out of scope

- The implementation of the two reads, the rerun and the run log (RWB-P1-AD018-APP).
- The deployment, the migration, the dashboards, the alerts and the run books (RWB-P1-AD018-OPS, RWB-PLT-E1056-OPS).
- The freshness resource and its stamp semantics (RWB-P1-E1015-CON, RWB-P1-E1015-APP) and the ACE read path (RWB-P1-E1069-CON).
- The screen field list and the composite route (RWB-PLT-N001-CON).
- The P2 outbound-action contract itself: consumed and faked, never defined here; the real journey is RWB-ITG-AD018-ITG.
- The Platform administration roles and their assignment (RWB-P4-AD001 to RWB-P4-AD016).
