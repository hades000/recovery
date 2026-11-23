# RWB-P1-E1017-CON Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1017-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-028) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-017 for rwb-source-data. The retention run is published as a contract of this service so that P5's JOB-17 can start it on Day 1 without this service being built, and so that a held case is answered by rwb-case over an interface with a fake rather than by a read of its table. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the rwb-source-data retention run: an OpenAPI 3.1 document for the start and the run record on `/api/recovery/source-data/v1`, the request and response schemas of a run, the `RetentionRunWorkflow` and activity contract on task queue `rwb-source-data` in namespace `rwb-recovery`, the error envelope and the Idempotency-Key rule, the contract tables of section 12 and the fakes for P5's JOB-17 tests and for the rwb-case legal-hold answer**, so that **rwb-document can schedule and start the retention of the eight P1 tables on Day 1, and the app and operations stories of this legacy key can build and test against a fixed surface without waiting for each other**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020), and a Temporal step in another service is reached only through a typed interface published in a contract jar (Architecture v5 slide 11). The retention rule and the monthly Schedule are rwb-document's (ASM-0076; Architecture v5 slides 16 and 44), so the part of RWB-E1-017 that stays with rwb-source-data is an action that another service starts. That action needs one agreed surface before either side is written: without it, P5 either waits for P1 or reaches into P1's schema, and both defeat the split.

The baseline also fixes the naming that the checks require: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1` (declared and not used here), task queue `rwb-source-data` in namespace `rwb-recovery`, and Java package `th.co.scb.ace.workbench.recovery.sourcedata`. It carries the legacy values that must not drift: rule version "RET-2026.11", 24 months on `occurred_at`, the run date 2026-12-06, the archive path `retention/YYYY-MM-DD/<table>/`, the manifest with the row count and the SHA-256 per file, and the message IDs MSG-P1-020, MSG-GEN-002, MSG-P1-002, MSG-GEN-006, MSG-P2-006 and MSG-P4-002.

Serves REQ-RDF-013 and its measure of FSD P1 A2.17 (100 percent of the Workbench records past their retention archived or on legal hold each month), with NFR-031, NFR-072 and NFR-074 behind the archive-then-delete order.

The sources disagree on one point this baseline settles. TSD P1 v3 T3.6 still defines `retention_rule` as a table of P1, while the Ownership Map rules `retention_rule` and `retention_action` to P5 and Architecture v5 slide 44 puts JOB-17 in rwb-document; the Ownership Map is applied, so the document declares no rule table and no Schedule of this service, and records the conflict as (GAP-0488; ASM-0680).

### 3. Preconditions

- The service template, the naming library and the contract-test harness are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the paths, the topic and the event names follow the platform rule rather than a local choice.
- The workflow kit and the namespace `rwb-recovery` are available (RWB-PLT-E1071-CON), because the run is a Temporal workflow and the document declares its typed contract.
- The platform error envelope, the CloudEvents 1.0 envelope and the Idempotency-Key rule are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the Ownership Map only: the run start and the run record are this service's, the retention rule and the Schedule are P5's, the legal hold is P3's, and the decision log is P7's.
- The write-once container of RWB-PLT-TE012-APP exists in each environment, so the archive part of the answer has a target to name.
- No build dependency: this story is Day 1 by rule (Template and Rules section R5.7).
- The exact field-level schema of the run request and answer, and the REST path of the legal-hold answer, are Not specified in the source documents (GAP-0489; ASM-0681) and (GAP-0491; ASM-0683); this story fixes them as `POST /retention-runs`, `GET /retention-runs/{runId}` and the named interface operations below.

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two operations on `/api/recovery/source-data/v1`, with the shared components used across the service.
2. Draft the request schema of a run (rule version, run date, rules with product, table, record class, months, age-basis field and end action) and the answer schema (run id, status, counts per table, rule version, archive location, held cases).
3. State the refusal shape: one refused rule set refuses the run in full, with a check name and a message ID, and no row is read.
4. Publish the `RetentionRunWorkflow` and activity contract as a typed interface with its input and output records, and state the task queue, the namespace and the workflow ID rule.
5. State the Idempotency-Key rule for the start and the `409` of a second start for an active run date.
6. Publish the contract tables of section 12 (nine sub-tables) and the four fakes, among them the retention-run fake that P5's JOB-17 tests call.
7. Add the contract tests: schema validation, envelope validation, error mapping, idempotency replay, the workflow input and output round trip and the drift check on every fake.
8. Tag the baseline and hand it to RWB-P1-E1017-APP, RWB-P1-E1017-OPS, RWB-P5-E1017-APP and RWB-ITG-E1017-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A start body fails schema validation | `400` with the error envelope and the failing pointer | MSG-GEN-001 | AC2 |
| X2 | The start has no Idempotency-Key | `400` with the error envelope naming the header | MSG-GEN-001 | AC4 |
| X3 | The same key is replayed with a different body | `422`; the stored answer is not overwritten | MSG-GEN-001 | AC4 |
| X4 | A second start for a run date whose run is active | `409` and the active run id | MSG-P2-006 | AC4 |
| X5 | The rule set is refused at a check | `422`, the check name and MSG-P1-002; nothing is read | MSG-P1-002 | AC5 |
| X6 | The container does not answer during the run | The run fails with MSG-GEN-006; no row is deleted | MSG-GEN-006 | AC7 |
| X7 | A fake drifts from the document or from the typed interface | The contract test fails and the merge is blocked | None | AC8 |
| X8 | A field-level definition is missing from the source material | The field carries the placeholder and one gap row | None | AC1 |

X1 to X4 are the contract-level paths of the start; X5 and X6 are the business failures the schemas must be able to carry; X7 is the drift check; X8 is the honest record of what the sources do not say.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit and the Ownership Map only |
| Negotiable | The field-level detail is settled with rwb-document and the app story; the two paths, the workflow name, the task queue and the rules of the answer are fixed by the target architecture |
| Valuable | Unblocks P5's JOB-17 and this legacy key's app and operations stories on Day 1 |
| Estimable | Two documents, one typed interface, one error mapping, two rules, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Retention run contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the retention rule version in force is "RET-2026.11" with product "DP05", table "interaction", age basis "occurred_at", 24 months

  Scenario: AC1 The OpenAPI 3.1 document describes the retention-run operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-source-data is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/source-data/v1
    Then it declares POST /retention-runs and GET /retention-runs/{runId} with the owner rwb-source-data
    Then every operation names its security right and its error responses 400, 401, 403, 409, 422 and 503

  Scenario: AC2 The run request carries the rule version, the run date and the rules (new, D-RCV-60)
    Given the request schema of a retention run
    When a start is sent with rule version "RET-2026.11", run date 2026-12-06 and a rule for product "DP05", table "interaction", record class, 24 months, age basis "occurred_at" and end action ARCHIVE
    Then the body validates with no error
    Then each rule carries productCode, tableName, recordClass, retentionMonths, ageBasisField and endAction
    Then retentionMonths is bounded to 1 to 600 and endAction to ARCHIVE or REVIEW
    When a start is sent with 0 months
    Then the body answers 422 with MSG-GEN-002 and the field retention_months

  Scenario: AC3 The 202 answer and the run record carry the run facts (new, D-RCV-60)
    Given an accepted start for run date 2026-12-06
    When the service answers the start
    Then the answer is 202 Accepted with a runId and no business count
    When GET /retention-runs/{runId} is read after the run completes
    Then the body carries the status, the counts per table, the rule version "RET-2026.11", the archive location and the held cases
    Then the archive location names the container path retention/2026-12-06/interaction/
    Then the held cases carry the case number and the row count kept and no personal data field

  Scenario: AC4 The start is idempotent and a second active run is refused (new, D-RCV-60)
    Given a start with the header Idempotency-Key "2026-12-06-RET-2026.11"
    When the same key is sent twice with the same body
    Then the second call returns the stored 202 answer and no second run exists
    When the same key is sent with a different body
    Then the service answers 422 with the error envelope
    When a start is posted for a run date whose run is active with a different key
    Then the service answers 409 with MSG-P2-006 and the active run id

  Scenario: AC5 A refused rule set is named at the check that refused it (new, D-RCV-60)
    Given a start whose rules name the table decision_log_entry
    When the run is started
    Then the service answers 422 with MSG-P1-002 and the check "decision_log_entry is not archived by the retention job"
    Then the answer names the rule and the table and no row was read
    When a start names a table that is not one of the eight tables of this service
    Then the service answers 422 with MSG-P1-002 and the check that names the table
    Then no archive is opened and no row is deleted

  Scenario: AC6 The workflow and activity contract is typed and sits on the right queue (new, D-RCV-60)
    Given the contract jar of the service
    When RetentionRunWorkflow is imported by a caller
    Then the interface declares the input rule version, run date and rules, and the output status, counts, rule version, archive location and held cases
    Then the workflow and its activities are declared on task queue rwb-source-data in namespace rwb-recovery
    Then the workflow ID rule is retention-<runDate>-<ruleVersion>
    Then the contract declares no Schedule of its own

  Scenario: AC7 The archive and the legal hold are consumed through published interfaces (new, D-RCV-60)
    Given the contracts the run consumes
    When the contract tables of section 12 are reviewed
    Then the legal-hold answer is the published CaseHoldQuery of rwb-case with casesOnLegalHold and caseNumbers, one hop and a 2 s budget
    Then the archive target is the write-once container of RWB-PLT-TE012-APP under retention/YYYY-MM-DD/<table>/ with a manifest of the row count and the SHA-256 per file
    Then the contract declares no read of a table of another service and no cross-schema key
    Then the document declares no event and no Schedule and states so in 12.3, 12.4 and 12.6

  Scenario: AC8 The nine contract tables are complete and the four fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then the rwb-case legal-hold fake, the write-once container stub, the clock control and the retention-run fake answer the paths and payloads of 12.2 and 12.8
    Then the contract tests compare every fake with the document and with the typed interface, and fail on any drift
    Then the retention-run fake answers a 202, a 409, a 422 and a completed run, so P5's JOB-17 tests run without this service
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/source-data/v1`; the document never declares another service's path | DP-13; Architecture v5 slide 41 notes |
| BR2 | The run start and the run record are this service's; the retention rule, the retention action and the Schedule are rwb-document's and are consumed, never documented as provided | ASM-0076; Ownership Map |
| BR3 | A refused rule set is refused in full, with the check that refused it and one message ID; a partial run is not allowed | BR6 of the app story; CTL-08 |
| BR4 | Every start declares the Idempotency-Key header and stores its answer; a replay with the same body returns the stored answer | Architecture v5 slide 11; DP-09 |
| BR5 | The run answer carries counts, table names, case numbers and hashes only, never a name, an address, an identity number or a contact point | Template and Rules section R7.2 section 17 |
| BR6 | No business value is fixed in the contract: the months, the tables, the age-basis fields and the end action are data in the request | FSD P1 A2.17; BR-P1-017 |
| BR7 | The legal-hold answer is the rwb-case interface with a fake; no case table is read and no cross-schema key exists | DP-01, DP-11; R-UNI-20 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version, and the workflow input and output records are versioned the same way | Architecture v5 slide 42 notes (BACKWARD compatibility) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the typed interface and the four fakes are described | In review |
| In review | Consumer sign-off | rwb-document, the app story and the integration story accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added to the request or the answer within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or the workflow input changes shape | New major version drafted |
| Baselined | Drift in a fake or in the contract jar | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the contract jar and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| rwb-document (P5) | Reviews and signs off the start and the run record it calls |
| rwb-case (P3) | Signs off the legal-hold interface as consumed here |
| Platform library owner | Owns the error envelope, the CloudEvents envelope, the idempotency rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in the answer |

The per-service login behind the document's security scheme is Not specified in the source documents (GAP-0489; ASM-0681); the document names it "the rwb-source-data login (DP-02)" and never a literal credential.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Run start request | `ruleVersion`, `runDate`, `rules[]`; each rule `productCode`, `tableName`, `recordClass`, `retentionMonths`, `ageBasisField`, `endAction`; the `Idempotency-Key` header |
| Run start answer | `202 Accepted`, `runId`, `acceptedAt`; no business count |
| Run record | `runId`, `status` (RUNNING, COMPLETE, FAILED), `ruleVersion`, `runDate`, `counts[]` per table (selected, archived, deleted, keptOnHold), `archiveLocation`, `heldCases[]` (caseNumber, rowsKept), `checks[]` for a refused rule set |
| Tables in scope | `interaction`, `case_list_row`, `reconciliation_result`, `data_product_load`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`, named in the rule validation and never joined |
| Refusal | `check` name, the rule and table it refused, the message ID and the text |
| Excluded by rule | `decision_log_entry` (P7) and `retention_rule` (P5) are named as refused, never as archived |

The exact field-level detail of the request and the answer (types, lengths, required flags, the page shape of the counts and the problem body) is Not specified in the source documents (GAP-0489; ASM-0681), and the archive contract of the container (its own request, its credential scope and its manifest schema) is Not specified in the source documents (GAP-0490; ASM-0682); this story fixes the field names above, the path `retention/YYYY-MM-DD/<table>/` and the manifest content as a row count and a SHA-256 per file, and leaves the rest to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/retention-runs` | Rule version, run date and rules in; `202` with the run id out; `409` for an active run; `422` for a refused rule set | Platform administration U, or the rwb-document service identity with the same right |
| GET | `/retention-runs/{runId}` | Status, counts per table, rule version, archive location and held cases | Platform administration R |

The rest of the service's surface, among them the reconciliation results, the data products, the dictionary, the contracts and the freshness reads, is published in the service API file by the stories that own it; this baseline documents the two operations the retention action needs and keeps the shared components reusable.

#### 12.2 REST operations consumed

| Interface | Operation | Owner | Use in the baseline |
|---|---|---|---|
| `CaseHoldQuery` | `casesOnLegalHold()` | P3 rwb-case | The case IDs whose every row is kept, once per run, faked |
| `CaseHoldQuery` | `caseNumbers(Set<UUID> caseIds)` | P3 rwb-case | The case numbers of the held cases for the hold report, faked |
| Write-once container (Blob) | Put file set and manifest; get manifest and files | RWB-PLT-TE012-APP | The archive under `retention/YYYY-MM-DD/<table>/` and its read-back check, stubbed |

The legal-hold interface has no REST path in the sources; the pair of operations is fixed as above and recorded as (GAP-0491; ASM-0683). The container is outside the bank's services and is named by its container and path, with its own credential scope; the detail of its contract is (GAP-0490; ASM-0682).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14); its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP. The baseline declares the topic and publishes no message on it.

#### 12.4 Events consumed

None. The run is started by the P5 Schedule and its contract call, not by an event, and Architecture v5 slide 15 gives the service no consumed event.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RetentionRunWorkflow` | Workflow, one run per run date and rule version | `rwb-source-data`, namespace `rwb-recovery` | Typed input (rule version, run date, rules) and output (status, counts, rule version, archive location, held cases); workflow ID `retention-<runDate>-<ruleVersion>` |
| `validateRules` | Activity | `rwb-source-data` | Rules in; accepted set or refused check out |
| `casesOnLegalHold`, `caseNumbers` | Activities | `rwb-source-data` | Documented as the consumer side of the rwb-case interface |
| `selectRows(page)`, `archiveTable`, `verifyManifest`, `deleteArchivedRows`, `recordRun` | Activities | `rwb-source-data` | Page size 5000; manifest with row count and SHA-256 per file; delete per table and rule after the check |

The interface is published in the contract jar of the service; a caller imports the interface and starts the workflow on the owner's queue (Architecture v5 slide 11). The retry policy and the non-retryable failures of a unit are declared with the interface, so a caller knows that a failed unit is repeated by a rerun and not by a silent retry.

#### 12.6 Schedules

None. JOB-17 (retention, monthly, first Sunday) is a Temporal Schedule of rwb-document on queue `rwb-document` (Architecture v5 slide 44; ASM-0076); this contract declares no Schedule and no cron.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `interaction`, `case_list_row`, `reconciliation_result`, `data_product_load`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | P1 (rwb_source_data) | The tables a rule may name; selected, archived and deleted by the run |
| `data_product`, `sys_objects`, `sys_fields` | P1 (rwb_source_data) | Read to validate a rule set; never written by the run |
| `retention_rule`, `retention_action` | P5 (rwb_document) | Named as refused if a run presents them; never read or written |
| `decision_log_entry` | P7 (rwb_decision) | Named as refused; never archived |

No other table is named in the contract, no table of another service is read and no cross-schema key exists (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data retention-run WireMock | `POST /retention-runs` with a `202` and a run id, a `409` for an active run, a `422` for refused rules; `GET /retention-runs/{runId}` with a completed run, its counts, archive location and held cases | P5's JOB-17 tests, contract tests |
| rwb-case `CaseHoldQuery` fake | No case on hold; one case on hold with 40 rows; a timeout; a case-number list | App story, contract tests |
| Write-once container stub | A writable container, a container refusing writes, a manifest whose count or hash differs | App story, contract tests |
| Clock control | Run dates 2026-12-06 and 2027-01-03; a row at exactly 24 months | App story, contract tests |

The first fake is the reason this story is Day 1: it lets rwb-document prove its Schedule and its start before rwb-source-data is built.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 interface consumed | The run start and the run record; the legal-hold answer; one hop, 2 s timeout (DP-11) |
| Kafka | None declared | The topic `rwb.source-data.events.v1` is declared and no message is published by this capability |
| Temporal | 1 workflow, 8 activities, no Schedule | `RetentionRunWorkflow` on `rwb-source-data` in `rwb-recovery`; the Schedule is P5's |
| File | 1 archive target | `retention/YYYY-MM-DD/<table>/` with a manifest of the row count and the SHA-256 per file, in the container of RWB-PLT-TE012-APP |

### 13. Solution plan

**Deliverables.** `openapi/rwb-source-data-v1.yaml` (OpenAPI 3.1) with the two retention-run operations and the shared components, `contract/retention-run.yaml` for the request and answer schemas, the contract jar with `RetentionRunWorkflow` and its activity interfaces, the error and idempotency rules in the contract README, and the four fake mappings.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is the reason the interface is typed rather than scheduled: the Schedule is P5's and the workflow here is started by a call. DP-11 is the pattern of the legal-hold answer, with the fake that makes the criterion testable. DP-01 and DP-13 fix the naming the document is checked against.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The two operations with the request and answer schemas of section 11; the field-level detail is agreed under GAP-0489.
3. The contract jar: `RetentionRunWorkflow` input and output records, the eight activity interfaces, the workflow ID rule and the retry policy.
4. Error envelope and the message-ID mapping, the legacy texts copied unchanged.
5. Idempotency-Key rule, the stored answer, the `409` of an active run and the versioning rule.
6. The four fakes and their stub fixtures, with the retention-run fake first because P5 depends on it.
7. The seven contract tests, including the drift check between the fakes, the document and the contract jar.
8. Baseline tag and the consumer sign-off note from rwb-document, rwb-case and the integration story.

**Done when.** The OpenAPI document validates in the pipeline, the contract jar imports cleanly in a consumer test, the seven contract tests pass, the four fakes answer every consumed path, and rwb-document has accepted the start and the run record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | The start body or a query fails validation | The request is not valid: {detail}. |
| MSG-GEN-002 | `retention_months` outside 1 to 600 | {field} must be between {min} and {max}. |
| MSG-P1-002 | The rule set is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | The container does not answer during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | A start for a run date whose run is active | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P1-020 | The run summary to Compliance | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. |
| MSG-P4-002 | A caller without the right on the run surface | You cannot {action} here. Your role does not include it. |

The message IDs are contract elements; the text is the agreed legacy text, unchanged, and Thai text follows decision DL10.

### 15. Screens and states

The contract serves no screen of its own: the run is read on the platform administration surface that another P1 story owns, and the Compliance summary arrives as the MSG-P1-020 alert. The retention classes that the rule refers to show on SCR-47 Personal data from Epic 8. The gateway-bff composite route (DP-19) is not on this path, because the start is a service-to-service call.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-017-01 | AC1, AC2, AC3 | Contract | The document validates; the start carries rule version "RET-2026.11", run date 2026-12-06 and the DP05 interaction rule at 24 months; the answer carries the path retention/2026-12-06/interaction/ |
| TC-E1-017-02 | AC2, AC3 | Contract | A second version "RET-2027.01" at 36 months on run date 2027-01-03 validates against the same schema |
| TC-E1-017-03 | AC3, AC7 | Contract | The held case "RW-2024-000311" with 40 rows appears in the answer as a case number and a count only |
| TC-E1-017-04 | AC2, AC5 | Contract | A rule with 0 months, and a rule naming `decision_log_entry`, are refused with MSG-GEN-002 and MSG-P1-002 |
| TC-E1-017-05 | AC7 | Contract | The container stub refuses a write; the answer schema still carries the FAILED status and MSG-GEN-006 |
| TC-E1-017-06 | AC4 | Contract | One key replayed with the same body and with a different body; a second key for an active run date answers 409 |
| TC-E1-017-07 | AC2, AC3 | Contract | A row at exactly 24 months on 2026-12-06 is reported as kept, not archived |
| TC-E1-017-08 | AC5, AC7 | Contract | A rule naming `decision_log_entry` is refused at the named check, and no rule may name a P5 or P7 table |
| TC-E1-017-09 | AC4, AC6 | Contract | A start during an active run answers 409 with MSG-P2-006; the workflow ID rule names the run date and the rule version |
| TC-E1-017-10 | AC1, AC8 | Contract | A caller without the run right is documented as 403 with MSG-P4-002; every fake matches the document |

The legacy test case IDs of RWB-E1-017 are kept in order, and each one now covers the contract element that carries its behaviour, because the behaviour itself is built in RWB-P1-E1017-APP and the rule in RWB-P5-E1017-APP. The legacy level "System" and "Access" map to "Contract" at this baseline. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the months, the tables, the age-basis fields, the end action and the archive path are data or configuration, never constants in a schema.
- No personal data in an event schema, an example, an answer or a fake: counts, table names, case numbers and hashes only.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: this contract declares neither a view nor a `public` table, and a rule naming one is refused.
- No cross-schema read and no cross-schema key: the legal hold comes over the rwb-case interface, and the run touches only `rwb_source_data`.
- The contract names only operations owned by rwb-source-data; `retention_rule`, `retention_action` and the Schedule are P5's and are never documented as provided here (ASM-0076).
- Every example is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this document narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | Run start request and run record; the rule fields and the archive location | TC-E1-017-01, TC-E1-017-02, TC-E1-017-03 |
| NFR-031 | Personal data is kept no longer than its policy allows | The rule set, the refusal and the counts of the run record | TC-E1-017-04, TC-E1-017-08 |
| NFR-072 | A case under legal hold keeps every row | The legal-hold answer in 12.2 and the held cases in the run record | TC-E1-017-03 |
| NFR-074 | No row is removed before its archive copy is checked | The archive location, the manifest and the FAILED status | TC-E1-017-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed interface and the client budget in 12.2 | TC-E1-017-09, TC-E1-017-10 |
| ASM-0076 | Retention is rwb-document's; P1 keeps the ledger | The absent rule table and the absent Schedule in 12.6 and 12.7 | TC-E1-017-08, TC-E1-017-09 |

### 19. Out of scope

- The implementation of the run, the selection, the archive writer, the manifest check and the delete (RWB-P1-E1017-APP).
- The deployment, the container mount and credential, the KEDA scaling, the dashboards and the runbook (RWB-P1-E1017-OPS).
- The retention rule, the retention action table, their load and approval and the monthly Schedule (RWB-P5-E1017-APP).
- The legal hold itself and the case number (rwb-case, P3); this baseline consumes the interface and fakes it.
- The write-once container's own contract, its immutability policy and its credential scope (RWB-PLT-TE012-APP; GAP-0490).
- The decision log retention (rwb-decision, P7).
- The cross-service proof of the rule, the hold and the archive (RWB-ITG-E1017-ITG).
- The field-level completeness of the request and answer schemas (GAP-0489).
