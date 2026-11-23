# RWB-P3-E1073-CON Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1073-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-073 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-011, FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-073 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-case side of the rule change seam fixed as one contract: the five rwb-decision authoring operations this service consumes with their paths, rights, answers and error codes, the model and catalog reads, the `RulePackageInForce` consumption contract on `rwb.decision.events.v1`, the `EvaluateRules` activity contract with `RuleResult` and `NoPackageInForce`, the cache and atomic-swap rules, the 2 s one-hop budget, the message set and the contract fakes**, so that **the app, infrastructure and test stories of this legacy key build on Day 1 against one agreed, testable shape without waiting for rwb-decision to be built, and no registry row, workbook object or promotion is claimed by rwb-case**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020), and rule governance central in rwb-decision with local evaluation is the rules decision (Arch v5 slide 27; Temporal and Drools design slides 15 and 16; D-RCV-36 T3 to T6; ADR-017). Both only work if the seam is written once. Here the seam is small and load-bearing: a load that refuses a bad workbook whole, an approval that the author cannot give, a rollback in one call, a dry run the approver reads, a model whose SHA-256 proves which table decided, and a result that names the rule ID and the version so the case pin is never a guess.

If the shape is agreed and faked on Day 1, four teams move at once. The app story builds the fact mapping, the pin and the scenario gate against the fake; the infrastructure story sizes the heap and opens one egress path against the same element names; the test stories of the case epics read one catalog; and the integration harness proves the same journey against the real service. Without it, every team reads a version list in its own way and the checksum, which is the only proof that a decision came from an approved table, becomes decoration.

The contract also states what rwb-case does not own: the registry rows, the workbook object, the load, the approval, the promotion at 00:01 and the rollback are rwb-decision's (ASM-0069; Arch v5 slides 27, 41 and 44), which is the ruling this contract rests on and the conflict the legacy story leaves open (GAP-0699; ASM-1246). This story therefore defines the consumed side and never restates another service's operation as its own.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the REST base, the topic and the event names follow the platform rule rather than a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The embedded Drools kit contract is available (RWB-PLT-E1072-CON, DP-04): one KieBase per package version, first-match semantics, the cache bound, the checksum check and the `NoPackageInForce` outcome are its elements and this story reuses them rather than redefining them.
- The local decision-record library and the shared topic `rwb.decision-record.v1` are available (RWB-PLT-E1027-CON, DP-03).
- The rwb-decision operations exist as published by the rwb-decision stories: the model and catalog reads and the five authoring operations. This story consumes them and fakes them; it defines none of them.
- The five package codes of the case side are the agreed values of 16 November 2026: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (TSD P3 v3 T2.2), and the legacy version labels "ALLOC-2026.11", "ALLOC-2026.12", "ALLOC-2026.13", "ALLOC-2026.14" and "TRF-2026.11" are used as fixtures with their values unchanged.
- `rules.testcases.min` = 50 and `drools.kiebase.cache.max` = 20 are parameters read through the parameters contract (DP-06); the contract declares their names and never their values as constants.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the consumed operation set: the load, the version list, the approve, the rollback and the dry run, each with method, path, purpose, rights, request, answer and every error code, and each attributed to rwb-decision.
2. Add the model and the catalog read, with the elements the evaluation and the case pin need: package code, version label, checksum, valid-from date, rule ID, action text, owner role, timer spec, target queue code and outputs.
3. Publish the `RulePackageInForce` consumption contract: envelope, key, payload, dedupe rule, and what the consumer does with the checksum.
4. Publish the `EvaluateRules` activity contract: the input, the `RuleResult` output, the `NoPackageInForce` outcome and the rule that an evaluation runs only inside an activity.
5. State the cache and swap contract: one KieBase per package version, at most 20 versions, least-recently-used eviction that never evicts a version in force, an atomic swap and the last-good-model rule on failure.
6. Fix the budget and the failure behaviour: one hop, a 2 s client budget, a breaker per operation, and the mapping from every downstream status to the message of section 14.
7. Publish the contract tables of section 12 and the contract fakes.
8. Add the contract tests: the operation shapes, the error codes, the event envelope, the activity input and output, the cache bound and a drift test between each fake and this document.
9. Tag the baseline and hand it to the app, infrastructure and test stories of this key and to RWB-ITG-E1073-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumed operation is declared as provided by rwb-case, or a registry table or workbook object is claimed by this service | The review fails the document; the element is moved to its owner | None | AC1, AC7 |
| X2 | A consumed operation is called with a shape, a path or a query this document does not declare | The contract test fails and the merge is blocked | None | AC1, AC2, AC8 |
| X3 | A fake drifts from this document | The drift test fails and the merge is blocked | None | AC8 |
| X4 | A consumer receives `RulePackageInForce` without a checksum, or with a package code this service does not hold | The consumer schema validation refuses the event and routes it to `.dlt` with an alert; no refresh is started | None | AC3 |
| X5 | A refresh of the same package code and version arrives twice | The inbox drops the second event; no second fetch and no second build | None | AC3 |
| X6 | No version of the package is in force on the business date | `EvaluateRules` raises `NoPackageInForce`, which is non-retryable, and the caller reports MSG-P3-027 | MSG-P3-027 | AC4, AC5 |
| X7 | A fetched model does not verify against the announced checksum, or does not build | The KieBase is not used, the atomic swap does not happen and the last good model stays in force; the condition is counted and alerted | None | AC4 |
| X8 | The cache holds 20 versions and a further version is requested | The least recently used version that is not in force is evicted; a version in force is never evicted | None | AC4 |
| X9 | A downstream answers outside the 2 s budget or answers 5xx | The breaker opens for that operation, the call answers 503 to the reader, and the evaluation retries on the activity policy with the model already cached | None | AC6 |
| X10 | A field-level detail of a consumed operation is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the embedded Drools kit contract, the decision-record library and the rwb-decision operations as published |
| Negotiable | Field-level detail of the consumed resources is settled with their owner; the operation set, the event contract, the activity contract and the cache rules are fixed by this realignment |
| Valuable | Unblocks the app, infrastructure and test stories of this key and the integration harness with one agreed seam |
| Estimable | Seven consumed operations, one event contract, one activity contract, one cache rule set, nine tables and two fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the document, the schema file, the fake — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Rule change contract baseline for rwb-case

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the embedded Drools kit contract of RWB-PLT-E1072-CON is in force
    Given the five package codes of the case side are ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER

  Scenario: AC1 The five authoring operations are consumed as published (new, D-RCV-60)
    Given the contract tables of section 12
    When the consumed authoring operations are reviewed
    Then the load, the version list, the approve, the rollback and the dry run are each described with method, path, purpose, rights, request, answer and every error code
    Then every one of them is attributed to rwb-decision and none is declared as provided by rwb-case
    Then the load answers 201 with the version in LOADED, 409 for a version label already loaded and 422 for a failed check, an empty file or a date order
    Then the approve answers 200 with APPROVED and refuses the author with 409, and the rollback answers 200 with the version now in force and refuses with 409 when no earlier version exists
    Then the dry run answers the counts by product, queue and rule, and refuses a version with no report with 409
    Then the rwb-decision WireMock answers every one of the five paths with the shapes of this document

  Scenario: AC2 The model and catalog reads are consumed under declared shapes (new, D-RCV-60)
    Given the contract tables of sections 11 and 12
    When the two read resources are reviewed
    Then the model resource carries packageCode, versionLabel, checksum (SHA-256), the model content, its compiler version and the valid-from date
    Then the catalog resource carries ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code and outputs
    Then a checksum mismatch between the fetched model and the announced checksum stops the swap and keeps the last good model
    Then the property types, lengths and required flags of both resources are Not specified in the source documents (GAP-0700; ASM-1247)
    Then the rwb-decision WireMock answers both paths, one with a wrong checksum and one with 404

  Scenario: AC3 RulePackageInForce is consumed under one contract (new, D-RCV-60)
    Given a RulePackageInForce message on rwb.decision.events.v1
    When the consumer validates it
    Then it carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype
    Then its payload carries the package code, the version label, the checksum and the valid-from date, and no personal data
    Then it is keyed by the package code and deduplicated through the inbox, so a repeat starts no second fetch and no second build
    Then a message without a checksum, or with a package code this service does not hold, is refused and routed to .dlt with an alert

  Scenario: AC4 The EvaluateRules activity and the cache rules are fixed (new, D-RCV-60)
    Given the activity contract of this story
    When EvaluateRules is called with a package code, the facts and the business date
    Then it returns RuleResult with packageCode, packageVersion, ruleId and outputs
    Then it raises NoPackageInForce when no version is in force, and that outcome is non-retryable
    Then one KieBase is built per package version and at most 20 versions are held, evicted least-recently-used and never evicting a version in force
    Then the swap of a new version is atomic, and a checksum mismatch or a failed build leaves the last good model in force
    Then the embedded Drools kit is called from activity code only, and no service code reads a workbook, a DRL source or a rule table

  Scenario: AC5 The message set of the seam is fixed and mapped to the answers (new, D-RCV-60)
    Given the messages of section 14
    When the consumed answers are mapped to them
    Then MSG-P3-027 carries the check and the detail for a refused version and for no version in force
    Then MSG-P3-015 carries the package code for a rollback with no earlier version
    Then MSG-P7-002 carries the refusal of an author who approves, and the version stays LOADED
    Then MSG-GEN-001 carries the empty field or the missing rollback reason, MSG-GEN-003 carries the refused date order and MSG-GEN-004 carries the version label already loaded
    Then no message text is added or changed by this contract, and no caller composes a text of its own

  Scenario: AC6 Every consumed operation is one hop inside the 2 s budget (new, D-RCV-60)
    Given the seven consumed operations of section 12.2
    When each call is made
    Then it is one hop to rwb-decision with a 2 s client budget and a breaker per operation
    Then no caller chains two services to answer one request
    Then a slow or failed answer returns 503 to the reader, and the evaluation keeps the model it already holds
    Then the budget and the breaker are configuration values and never code constants

  Scenario: AC7 The nine contract tables are complete and name their owners (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1, 12.3 and 12.6 are None, and 12.7 names only rwb-case tables and the platform library objects
    Then rwb-case holds no rule_package, rule_package_version, rule_row or rule_test_case row, no workbook object, no job_catalog row and no Schedule
    Then every table, topic, queue and base in the document follows the naming rule of the service

  Scenario: AC8 The contract fakes answer every path and the drift test blocks a change (new, D-RCV-60)
    Given the rwb-decision and rwb-access fakes of section 12.8
    When each consumed path and payload is called against its fake
    Then every path of section 12.2 answers with the status, the body and the error code this document declares
    Then a field added, removed or retyped in this document without the fake fails the drift test
    Then the six contract tests pass and the baseline is tagged for the app, infrastructure and test stories
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The registry, the workbook object, the load, the approval, the promotion at 00:01 and the rollback belong to rwb-decision; rwb-case consumes them and provides no package operation of its own | ASM-0069; Arch v5 slides 27, 41 and 44 |
| BR2 | The consumed operations are fixed at seven: the load, the version list, the approve, the rollback, the dry run, the model read and the catalog read | Arch v5 slide 14 (P7 IN: POST /rule-models, GET /rule-models/{n}/{v}); legacy RWB-E1-073 section 12 |
| BR3 | The SHA-256 in the model answer and the checksum in the event are the same value; a fetched model is used only when they match | Arch v5 slide 27; Temporal and Drools design slide 15 |
| BR4 | An evaluation runs only inside the `EvaluateRules` activity, on the version in force for the business date, and returns the rule ID and the package version to the caller | D-RCV-36 T5, T7; Arch v5 slide 27 |
| BR5 | One KieBase per package version, at most 20 in the cache, an atomic swap and the last good model kept on failure | Arch v5 slide 27; Temporal and Drools design slide 16 |
| BR6 | One REST base and one topic per service: this contract declares `/api/recovery/case/v1` for rwb-case and consumes the rwb-decision base; it never declares another service's path as provided | DP-13; DP-14; Ownership Map v1 |
| BR7 | Every call is one hop with a 2 s budget and a breaker per operation, and no caller chains two services | DP-11; ADR-020 |
| BR8 | The message set of the seam is the legacy set: MSG-P3-027, MSG-P3-015, MSG-P7-002, MSG-GEN-001, MSG-GEN-003, MSG-GEN-004, with the legacy texts unchanged | Legacy RWB-E1-073 section 14 |
| BR9 | `NoPackageInForce` is an outcome, not an error to retry: the activity fails once and the caller reports MSG-P3-027 | Temporal and Drools design slide 14 and slide 28 |
| BR10 | No business value appears in this contract: rows, scenarios, tolerances, action text, owner roles, timers and queue codes are data of the workbooks and the registry | Template and Rules §R7.2 s17 |
| BR11 | rwb-case writes no registry row and holds no workbook object; the registry is read only through the consumed operations | ASM-0069; DP-01 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation set, the event, the activity contract and the cache rules are described | In review |
| In review | Consumer sign-off | The app, infrastructure and test stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field, a status or an element is added without removing one | Baselined |
| Baselined | Breaking change to a consumed operation | rwb-decision removes, renames or retypes an element this contract consumes | In review, with the owner of that operation |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A package version becomes in force | rwb-decision announces it and the service refreshes its evaluated copy | Baselined (new version in force) |

The package version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are rwb-decision's and are read through the version list; this contract fixes what rwb-case observes of them and nothing about how they are reached.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the consumed contract, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the consumed contract and any change to the cache or budget rule |
| The rwb-decision owner | Owns the seven consumed operations and signs off the shapes taken from its document |
| The rwb-case app, infrastructure and test stories | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the embedded Drools kit and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in the event, the activity input or an example |

The deployment identity that calls rwb-decision is the rwb-case workload identity of DP-02; its name and its Key Vault entries are Not specified in the source documents (GAP-0702; ASM-1249) and are fixed in RWB-P3-E1073-INF.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Load request | multipart/form-data: the workbook file (xlsx with a Rows and a Tests tab), `validFrom` as a date; the version label is a cell of the workbook |
| Load answer | versionId, packageCode, versionLabel, status LOADED, validFrom, validTo, author, checksum, testResult {total, passed, failed, failedScenarioIds}, dryRunCounts {openCases, changedCases, byProduct, byQueue} |
| Version list answer | versionId, versionLabel, status, validFrom, validTo, author, approver, checksum, testResult, dryRunCounts |
| Approve answer | the version with status APPROVED, approver and approvedAt |
| Rollback request and answer | body { reason } required; the answer is the version now in force |
| Dry-run answer | packageCode, versionLabel, evaluatedAt, openCases, changedCases, byProduct, byQueue, byRule |
| Model resource | packageCode, versionLabel, checksum (SHA-256), the model content and its compiler version, the valid-from date |
| Catalog resource | ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code, outputs |
| Event payload | package code, version label, checksum, valid-from date, published at; identifiers and business facts only |
| Activity input and output | package code, facts reference, business date in; packageCode, packageVersion, ruleId, outputs out |
| Cache entry | package code, version label, checksum, the KieBase reference, loaded at, hit count, last used at |

The request and answer bodies above are taken from the legacy story's endpoint shapes and re-based on `/api/recovery/decision/v1`. The property types, lengths, required flags and the compiler-version element of the model and catalog resources are Not specified in the source documents (GAP-0700; ASM-1247); this story fixes the element names above and leaves the types to the review with the rwb-decision owner. The operational values of the deployment story — the heap, the ports, the certificate subject and the alert defaults — are Not specified in the source documents (GAP-0701; ASM-1248) (GAP-0702; ASM-1249) and are fixed in RWB-P3-E1073-INF.

### 12. Contract

#### 12.1 REST operations provided

None. This contract serves no business operation: the case fact mapping is internal, the version pin is a column of the case and of the record, and the scenario gate runs in the pipeline. The case read that shows the pinned version is `GET /api/recovery/case/v1/cases/{caseId}` of RWB-P3-E1023-CON and is unchanged by this story.

#### 12.2 REST operations consumed

Base `/api/recovery/decision/v1`; owner P7 rwb-decision for every row. One hop and a 2 s client budget (DP-11, ADR-020).

| Method | Path | Rights | Answer |
|---|---|---|---|
| POST | `/admin/rule-packages/{packageCode}/versions` | Rules and parameters C | 201 the version in LOADED; 403 MSG-P4-002; 404 unknown package code; 409 MSG-GEN-004; 422 MSG-P3-027, MSG-GEN-001 or MSG-GEN-003; 401; 503 |
| GET | `/admin/rule-packages/{packageCode}/versions` | Rules and parameters R | 200 the version list; 403 MSG-P4-002; 404; 401; 503 |
| POST | `/admin/rule-package-versions/{versionId}/approve` | Rules and parameters A | 200 APPROVED with approver and approvedAt; 403 MSG-P4-002; 404; 409 MSG-P7-002 or MSG-GEN-004; 401; 503 |
| POST | `/admin/rule-package-versions/{versionId}/rollback` | Rules and parameters U | 200 the version now in force; 403 MSG-P4-002; 404; 409 MSG-P3-015; 422 MSG-GEN-001 for a missing reason; 401; 503 |
| GET | `/admin/rule-package-versions/{versionId}/dry-run` | Rules and parameters R | 200 the dry-run report; 403 MSG-P4-002; 404; 409 no report exists; 401; 503 |
| GET | `/rule-models/{packageCode}/{version}` | service identity | 200 the model with its checksum and valid-from date; 403; 404; 401; 503 |
| GET | `/rule-catalog/{ruleId}?packageVersion=` | service identity | 200 the catalog row; 403; 404 for an unknown rule ID or version; 401; 503 |

Every operation is attributed to rwb-decision and none is declared as provided by rwb-case. The five authoring operations are called by RW-COE, RW-RISK and RW-AUDIT through the Workbench and never from a workflow; the two reads are called by the service identity inside an activity. The field-level shape of the two reads is carried under GAP-0700.

#### 12.3 Events published

None. This contract publishes no event type. The shared ledger event `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library of DP-03 when a decision is taken in rwb-case; its schema is unchanged by this story and is the one declared in RWB-P3-E1018-CON.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | CloudEvents 1.0; key = package code; payload = package code, version label, checksum, valid-from date, published at; inbox dedupe; starts one refresh of the evaluated copy and nothing else |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Input: package code, facts reference, business date. Output: `RuleResult(packageCode, packageVersion, ruleId, outputs)`; raises `NoPackageInForce`, which is non-retryable |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Input: the decision record with its rule ID and package version, the state change and the outbox rows; one transaction and no partial write |
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Asks the rules at each decision and carries the pinned version on the case; calls the two activities only |

The workflow interface, the `CaseEvent` signal and the retry policy are RWB-P3-E2043-CON; the model refresh workflow `RuleModelSwap` and its activity are RWB-P3-E2042-CON. This contract fixes the rule-evaluation element of `EvaluateRules` and the record element its caller relies on, so that the catalogue read and the evaluation name the same package version, and adds no fourth element.

#### 12.6 Schedules

None. The 00:01 promotion is the Temporal Schedule JOB-20 in rwb-decision, owned there and announced as RulePackageInForce (Arch v5 slide 44; DP-10). rwb-case registers no Schedule and holds no `job_catalog` row for a rule package.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case header, its facts and `rule_version` (DF-CAS-021), the pinned package version of the decision in force |
| queue | P3 (rwb_case) | The queue code a row names and the case sits in |
| case_account | P3 (rwb_case) | The account link of a case, read by the fact mapping |
| case_entry_exclusion | P3 (rwb_case) | The rule ID and rule version of an exclusion, read for the gate fixture |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The outbox, inbox and idempotency envelope of the consumer (DP-09) |

No other table is named. `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `approval` and `decision_log_entry` are rwb-decision's and are never read directly (ASM-0069; DP-01). No workbook object and no `job_catalog` row belongs to this service.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock — authoring | The load of ALLOCATION "ALLOC-2026.12" answering 201 with 26 rows and 50 passing scenarios, then 409 for a repeated label and 422 for a failed check, an empty file and a past valid-from date; the version list with "ALLOC-2026.11" in force, "ALLOC-2026.13" and "ALLOC-2026.14"; the approve answering 200, 403 and 409 with MSG-P7-002; the rollback answering 200 and 409 with MSG-P3-015; the dry run answering the counts and 409 with no report | App story, contract tests |
| rwb-decision WireMock — models and catalog | The model for ALLOC-2026.11, ALLOC-2026.12 and ALLOC-2026.13 with their SHA-256 and valid-from dates, one wrong checksum, one 404 and one slow answer; the catalog for R-ALLOC-014 and the route-set rows, with a 404 for an unknown rule ID | App story, contract tests |
| rwb-access WireMock | `POST /authorise` granting Rules and parameters CRUD to RW-COE, A to RW-RISK and R to RW-AUDIT, and refusing a role without the right with MSG-P4-002 | App story, contract tests |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 7 consumed | The five authoring operations and the two reads of rwb-decision; one hop, 2 s budget, a breaker per operation |
| Kafka | None published, 1 consumed | `rwb.decision.events.v1` for RulePackageInForce |
| Temporal | 1 workflow, 2 activities | CaseWorkflow; EvaluateRules and RecordAndApply, declared here for the rule element and defined by RWB-P3-E2043-CON |
| File | None | No file is exchanged by the seam; the workbook is a request body of the load operation, not a file this service stores |

### 13. Solution plan

**Deliverables.** `contract/rule-package-consumed.yaml` (the seven consumed operations with their rights, answers and error codes), `contract/rule-model-catalog.yaml` (the two read resources and their elements), `contract/rule-package-in-force.md` (the event contract), `contract/evaluate-rules.yaml` (the activity input, `RuleResult`, `NoPackageInForce` and the cache rules), `contract/rule-seam-messages.md` (the message set of section 14 and its mapping), and the three WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-04, DP-10 and DP-11 are the patterns this contract serves: the registry and the promotion are rwb-decision's, the evaluated copy is local, and every call across the seam is one hop with a budget.

**Build steps**

1. Write the seven consumed operations from the legacy endpoint shapes and the rwb-decision documents, re-based on `/api/recovery/decision/v1`, with the rights, the answers and every error code; the model and catalog elements are agreed under GAP-0700.
2. Write the `RulePackageInForce` contract: envelope, key, payload, dedupe and the `.dlt` rule.
3. Write the activity contract: the input, `RuleResult`, `NoPackageInForce`, the cache bound, the atomic swap and the last-good-model rule.
4. Write the message set and the mapping from every downstream status to a message.
5. Write the budget and breaker rule: 2 s, one hop, no chaining, configuration not code.
6. Build the three WireMock mapping sets and their fixtures.
7. Add the eight contract tests, including the drift test between each fake and this document.
8. Tag the baseline and collect the sign-off of the app, infrastructure and test stories.

**Done when.** The five contract files validate in the pipeline, the eight contract tests pass, the three fakes answer every consumed path and payload, and the app, infrastructure and test stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A package version check fails, or no version is in force for a package | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | An empty workbook, an empty required cell or a missing rollback reason | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | The version label is already loaded, or the version is not LOADED | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without the right calls a package operation | You cannot {action} here. Your role does not include it. |

The texts are the agreed texts of the legacy story and of the message catalogue; this contract adds no message and changes no text. The `{check}` value is compile, schema, overlap, unreachable row, default row, scenario or package in force, and the `{detail}` names rows, cells, scenario IDs, rule IDs, package codes and version labels only, never a case fact or a person. For MSG-P3-015 the `{table}` value is the package code. A checksum mismatch, a failed build and an open breaker are operator conditions: they carry the package code, the version label and the expected and computed checksum to the log and the dashboard and produce no user-facing message.

### 15. Screens and states

None in this story. The contract serves the version list that SCR-39 Rules and parameters shows in Epic 8 and the pinned version a case carries, only through the answers of the consumed operations. The cache states of section 12.5 are internal to rwb-case and are exposed as the readiness signal and the metrics of the deployment story, not as a screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1073-CON-01 | AC1, BR1, BR2 | Contract | The five authoring operations documented and faked; one call per path with its success and its refusal |
| TC-P3-E1073-CON-02 | AC2, BR3 | Contract | The model and catalog resources; one correct checksum, one wrong checksum and one 404 |
| TC-P3-E1073-CON-03 | AC3 | Component | A valid, a duplicate, a checksum-less and an unknown-package RulePackageInForce message |
| TC-P3-E1073-CON-04 | AC4, BR4, BR5, BR9 | Component | EvaluateRules returning RuleResult; NoPackageInForce non-retryable; the cache bound, the eviction and the atomic swap exercised |
| TC-P3-E1073-CON-05 | AC5, BR8 | Contract | Each message of section 14 mapped to the status that produces it |
| TC-P3-E1073-CON-06 | AC6, BR7 | NFR | A slow answer per consumed operation; the breaker opens, 503 is returned and the cached model is kept |
| TC-P3-E1073-CON-07 | AC7, BR6, BR11 | Contract | The nine sub-tables complete; 12.1, 12.3 and 12.6 None; no registry table, workbook object, job row or Schedule claimed |
| TC-P3-E1073-CON-08 | AC8 | Contract | The three fakes answering every path; one field added to the document without the fake fails the drift test |

### 17. Guardrails

- No business value in the contract: rows, scenarios, tolerances, action text, owner roles, timers and queue codes stay data of the workbooks and the registry.
- No personal data in an event, an activity input, an example or a fake: identifiers and business facts only.
- The contract names only rwb-case tables and only rwb-case elements as provided; the seven rwb-decision operations are consumed and never restated as this service's (DP-01, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- No registry row, no workbook object, no `job_catalog` row and no Schedule is claimed by this service (ASM-0069; Arch v5 slide 44).
- Every example and fixture is synthetic; no production workbook, payload or checksum is copied into a schema or a fake.
- The envelope, the naming rule, the embedded Drools kit elements and the decision-record library come from the platform library; this story narrows them but never redefines them.
- One hop and one budget: a document that lets a caller chain two services, or that hides a call in a workflow, fails the review (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | The load, version-list, approve, rollback and dry-run operations; the RulePackageInForce contract | TC-P3-E1073-CON-01, TC-P3-E1073-CON-03, TC-P3-E1073-CON-05 |
| REQ-CWC-014 | Schema, overlap, unreachable, default, compile and scenario checks before a version takes effect | The refusal answers of the load and the message set | TC-P3-E1073-CON-01, TC-P3-E1073-CON-05 |
| REQ-DRI-004 | Epic 1 records use versioned rules | The `RuleResult` element and the record element that carries the rule ID and version | TC-P3-E1073-CON-04 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | The catalog element and the default-row element of the load answer | TC-P3-E1073-CON-01, TC-P3-E1073-CON-02 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The consumed model and catalog reads, the cache rules and the activity contract | TC-P3-E1073-CON-02, TC-P3-E1073-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed operations with the 2 s budget and the breaker | TC-P3-E1073-CON-01, TC-P3-E1073-CON-06 |

### 19. Out of scope

- The implementation of the fact mapping, the version pin and the scenario gate (RWB-P3-E1073-APP).
- The registry rows, the workbook object, the five authoring operations as built, the approval, the promotion Schedule JOB-20 and the rollback (RWB-P7-E1073-APP; ASM-0069).
- The model cache of the Epic 2 packages, its swap workflow and its activity (RWB-P3-E2042-CON, RWB-P3-E2042-APP).
- The workflow interface, the `CaseEvent` signal and the retry policy (RWB-P3-E2043-CON).
- The case record view and the case list that show the pinned version (RWB-P3-E1023-CON, RWB-P3-E2011-CON).
- The base image, the heap, the egress path, the certificate and the readiness signal (RWB-P3-E1073-INF).
- The real cross-service proof of the load, the approval, the promotion, the pin and the rollback (RWB-ITG-E1073-ITG).
- The field-level types of the model and catalog resources (GAP-0700) and the operational values of the deployment story (GAP-0701, GAP-0702).
