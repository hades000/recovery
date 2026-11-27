# RWB-P3-E2042-CON Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2042-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P3-E2042-CON-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None; H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E2041-CON (C); RWB-P7-E1073-CON (C, rule-model contract of rwb-decision); RWB-P3-E1042-CON (C); RWB-P3-E1043-CON (C); RWB-P4-E1037-CON (C) |
| Contract version | /v1 path of rwb-decision, API Specification v5 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-008 |

**Version 3 changes.**

- RD-P1-008: the event type of DecisionRecorded reads `rwb.decision.DecisionRecorded.v1` (events section); the topic `rwb.decision-record.v1` is unchanged.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-042 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 37 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3 aligns the story with RD-P1-008. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **tribe lead and squad member (RW-TRIBE)**, I want **the rwb-case side of the Epic 2 rule packages fixed as a contract: the Rows and Tests schema of a workbook, the Blob object naming and metadata that make a workbook write-once and checksum-addressable, the five rwb-decision operations this service consumes, the RulePackageInForce consumption contract, the EvaluateRules activity contract with `RuleResult` and `NoPackageInForce`, the cache and swap rules, and the contract fakes for rwb-decision and rwb-access**, so that **the app, infrastructure, operations and test stories of this legacy key build on Day 1 against one agreed, testable shape without waiting for rwb-decision to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling rule (DP-11, ADR-020), and rule governance central in rwb-decision with local evaluation is the rules decision (Arch v5 slide 27; D-RCV-36 T3 to T6; ADR-017). Both only work if the seam is written down once. The seam here is small and load-bearing: a workbook that compiles deterministically to one checksum, a model operation that returns that checksum, a swap rule that never leaves the service without a working model, and a catalog read that answers action_text, owner_role, timer_spec and outputs by rule ID and package version.

If the shape is agreed and faked on Day 1, four teams can move at once. The app story builds the cache and the swap against the P7 fakes; the infrastructure story provisions the container and the identity against the metadata keys; the operations story wires the consumer group, the readiness signal and the alerts against the event contract; the test stories of RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027 and RWB-E2-035 read one catalog. Without it, every team reads a workbook in its own way and the checksum, which is the only proof that a decision came from an approved table, becomes decoration.

The contract also states what rwb-case does not own: the registry rows, the load and approve operations, the four-eyes approval and the 00:01 promotion are rwb-decision's (ASM-0069). This story therefore defines the consumed side and never restates another service's operation as its own.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the REST base, the topic and the event names follow the platform rule and not a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The embedded Drools kit contract is available (RWB-PLT-E1072-CON, DP-04): one KieBase per package version, first-match semantics, the cache bound, the checksum check and the `NoPackageInForce` outcome are its elements, and this story reuses them rather than redefining them.
- The rwb-decision operations exist as published by the rwb-decision stories: the model and catalog reads (RWB-P7-E1073-CON) and the admin load, list and approve operations (RWB-P7-E2042-APP). This story consumes them and fakes them; it defines none of them.
- The three package codes and the three version labels are the agreed values of 16 November 2026: RESTRUCTURE "RES-2026.12", PAYMENT_MATCH "PMT-2026.12" and BOOKING_MATCH "BKG-2026.12".
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the workbook authoring contract: the Rows tab (RuleSet = package code, NAME = rule ID, the condition columns, the output columns, the default row last) and the Tests tab (one row per scenario, with the rule_test_case columns of DF-REF-186 to DF-REF-197).
2. Fix the Blob object naming and the metadata keys that make a workbook write-once and checksum-addressable, and the rule that no service reads a workbook at run time.
3. Publish the five consumed rwb-decision operations with their shapes, error codes, rights and the 2 s client budget.
4. Publish the RulePackageInForce consumption contract: the envelope, the key, the payload fields, the dedupe rule and what the consumer does with the checksum.
5. Publish the EvaluateRules activity contract: the input, the `RuleResult` output, the `NoPackageInForce` outcome and the rule that an evaluation runs only inside an activity.
6. State the cache contract: one KieBase per package version, at most 20 versions, least-recently-used eviction that never evicts a version in force, an atomic swap and the last-good-model rule on failure.
7. Publish the contract tables of section 12 and the two contract fakes.
8. Add the contract tests: the workbook schema, the metadata keys, the operation shapes, the event envelope, the activity input and output, and a drift test between each fake and this document.
9. Tag the baseline and hand it to the app, infrastructure, operations and test stories of this key and to RWB-ITG-E2042-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A workbook does not follow the Rows schema (RuleSet not the package code, NAME not the rule ID, no default row last) | The load is refused by the authoring pipeline before it reaches rwb-decision; the row and the cell are named | MSG-P3-027 | AC1 |
| X2 | A Tests tab row lacks an expected column the harness needs | The load is refused at the schema check of the tests tab; the test_case_id is named | MSG-P3-027 | AC1 |
| X3 | A Blob object is written without the checksum metadata, or a second write is attempted | The write-once policy refuses the overwrite, and the verification step refuses a model whose metadata checksum is missing | None | AC2 |
| X4 | A fake drifts from the document, or the model operation is called with a shape this document does not declare | The contract test fails and the merge is blocked | None | AC3, AC6 |
| X5 | A consumer receives RulePackageInForce without a checksum, or with a package code this service does not hold | The event is refused by the consumer schema validation and routed to `.dlt`; no swap is started | None | AC4 |
| X6 | Service code calls the embedded Drools kit outside the EvaluateRules activity, or reads a workbook, a DRL or a rule table | The architecture boundary test fails the build | None | AC5 |
| X7 | A field-level detail of a consumed operation is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the embedded Drools kit contract and the rwb-decision operations as published |
| Negotiable | Field-level detail of the consumed operations is settled with their owner; the authoring schema, the swap rule and the activity contract are fixed by this realignment |
| Valuable | Unblocks the app, infrastructure, operations and test stories of this key and the six Epic 2 engine stories that read the catalog |
| Estimable | One authoring schema, one metadata list, five consumed operations, one event contract, one activity contract, nine tables and two fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema file, the metadata keys, the fake, the document — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule package contract baseline for rwb-case

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the embedded Drools kit contract of RWB-PLT-E1072-CON is in force
    Given the three package codes are RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH, read through the contract as the fixture set of this key

  Scenario: AC1 The workbook Rows and Tests schema is fixed (new, D-RCV-60)
    Given the workbook authoring contract of this story
    When a workbook is validated against it
    Then the Rows tab declares RuleSet equal to the package code
    Then every row names the rule ID in NAME and the default row is last
    Then the Tests tab carries one row per scenario with test_case_id, route_set, rule_version, rule_id, from_state, event_code, facts, expected_to_state, expected_owner_role, expected_timer_spec, result and result_detail
    Then a workbook whose RuleSet is not the package code, whose NAME is not the rule ID, or whose last row is not the default row is refused with MSG-P3-027 naming the row and the cell
    Then RESTRUCTURE declares 38 rows and 62 scenarios, PAYMENT_MATCH 3 rows and 58 scenarios, BOOKING_MATCH 21 rows and 54 scenarios, and every package is at or above rules.testcases.min

  Scenario: AC2 The Blob object naming and metadata make a workbook write-once (new, D-RCV-60)
    Given the Blob container rule-packages and the authoring contract
    When a workbook is stored
    Then its path is <PACKAGE_CODE>/<VERSION_LABEL>.xlsx under the container
    Then the object metadata carries the package code, the version label, the SHA-256 of the workbook and the author role
    Then a second write to the same path is refused by the write-once policy
    Then no run-time code path reads a workbook, a DRL source or a rule table

  Scenario: AC3 The five rwb-decision operations are consumed as published (new, D-RCV-60)
    Given the contract tables of section 12
    When the consumed operations are reviewed
    Then the model read, the catalog read, the version list, the load and the approve operation are each described with method, path, purpose, rights and the 2 s client budget
    Then every operation is attributed to rwb-decision and none is declared as provided by rwb-case
    Then the rwb-decision WireMock answers every consumed path with the shapes of this document
    Then a drift between the fake and the document fails the contract test

  Scenario: AC4 RulePackageInForce is consumed under one contract (new, D-RCV-60)
    Given a RulePackageInForce message on rwb.decision.events.v1
    When the consumer validates it
    Then it carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype
    Then its payload carries the package code, the version label, the checksum and the valid-from date, and no personal data
    Then it is keyed by the package code and deduplicated through the inbox, so a repeat starts no second swap
    Then a message without a checksum, or with a package code this service does not hold, is refused and routed to .dlt with an alert

  Scenario: AC5 The EvaluateRules activity contract and the cache rules are fixed (new, D-RCV-60)
    Given the activity contract of this story
    When EvaluateRules is called with a package code, the facts and the business date
    Then it returns RuleResult with packageCode, packageVersion, ruleId and outputs
    Then it raises NoPackageInForce when no version is in force, and that outcome is non-retryable
    Then a KieBase is built once per package version and at most 20 versions are held, evicted least-recently-used and never evicting a version in force
    Then the swap of a new version is atomic, and a checksum mismatch or a failed build leaves the last good model in force
    Then the embedded Drools kit is called from activity code only

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1 and 12.3 are None, 12.6 is None, and 12.7 names only rwb-case tables and the library objects
    Then rwb-case holds no table and no column for payment_match_rule
    Then the rwb-decision and rwb-access fakes answer the consumed paths and payloads, and the contract tests fail on any drift

  Scenario: AC7 Each business rule of section 8 has a check in the contract (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When the contract is reviewed against them
    Then each of BR1 to BR10 has one check in section 16 and its source named in section 8
    Then a rule without a check fails the review

  Scenario: AC8 A consumed call that fails or gets no answer is reported, not hidden (new, D-RCV-60)
    Given a consumed rwb-decision operation of section 12
    When the call fails or gets no answer within the 2 s client budget
    Then the failure is reported to the caller with the operation name
    Then the last good model stays in force and no partial result is returned
    Then a failed call starts no package swap
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One authoring form for every Epic 2 package: the Drools XLS decision table, RuleSet = the package code, NAME = the rule ID, the default row last | D-RCV-36 T5; TSD P3 v3 T2.2 |
| BR2 | The package code and the version label are the only identity of a workbook, and the version labels are RES-, PMT- and BKG-yyyy.MM | D-RCV-36 T5; the agreed labels of 16 November 2026 |
| BR3 | A workbook is write-once: a change is a new object and a new version, never an overwrite | Arch v5 slide 27 (the model in force is dated and never edited); DP-04 |
| BR4 | The SHA-256 in the object metadata and the checksum in rwb-decision are the same value; a fetched model is used only when they match | Arch v5 slide 27; Temporal and Drools slide 15 |
| BR5 | The registry rows and the load, list, approve and rollback operations belong to rwb-decision; rwb-case consumes them and provides no package operation of its own | ASM-0069; Arch v5 slides 27 and 41 |
| BR6 | An evaluation runs only inside the EvaluateRules activity, on the version in force for the business date, and returns the rule ID and the package version to the caller | D-RCV-36 T5, T7; Arch v5 slide 27 |
| BR7 | One KieBase per package version, at most 20 in the cache, an atomic swap and the last good model kept on failure | Arch v5 slide 27; Temporal and Drools slide 16 |
| BR8 | One REST base and one topic per service: this contract declares `/api/recovery/case/v1` for rwb-case and consumes the rwb-decision base; it never declares another service's path as provided | DP-13; DP-14; Ownership Map v1 |
| BR9 | No business value in the contract: rows, tolerances, windows, action text, owner roles and timers are data of the workbooks and the registry | Template and Rules §R7.2 s17 |
| BR10 | `payment_match_rule` and DF-REF-261 to DF-REF-273 are retired: no table, no column and no field appears in the contract | D-RCV-36 T10 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The authoring schema, the metadata keys, the five operations, the event and the activity contract are described | In review |
| In review | Consumer sign-off | The app, infrastructure, operations and test stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A metadata key, a payload field or an output is added without removing one | Baselined |
| Baselined | Breaking change to a consumed operation | rwb-decision removes, renames or retypes an element this contract consumes | In review, with the owner of that operation |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A package version becomes in force | rwb-decision announces it and this service swaps the cached model | Baselined (new version in force) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the authoring schema, the metadata keys, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the consumed contract and any change to the swap rule |
| The rwb-decision owner | Owns the five consumed operations and signs off the shapes taken from its document |
| The rwb-case app, infrastructure, operations and test stories | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule and the embedded Drools kit contract this document reuses |
| Data steward | Confirms that no personal data field is declared in the event or in the activity input |

The deployment identity that reads the container and calls rwb-decision is Not specified in the source documents (GAP-0722; ASM-1269); the document names it "the rwb-case workload identity (DP-02)" and leaves the name to RWB-P3-E2042-INF.

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Workbook Rows tab | RuleSet = package code; NAME = rule ID; the condition columns of the package; the output columns action_text, owner_role, timer_spec, target_queue_code and outputs (DF-REF-008, DF-REF-010, DF-REF-011, DF-REF-052 to DF-REF-054, DF-REF-298); default row last | Not specified in the source documents (DOR-RWB-P3-E2042-CON-7) |
| Workbook Tests tab | test_case_id, route_set, rule_version, rule_id, from_state, event_code, facts, expected_to_state, expected_owner_role, expected_timer_spec, result, result_detail (DF-REF-186 to DF-REF-197) | Not specified in the source documents (DOR-RWB-P3-E2042-CON-7) |
| Blob object metadata | package code, version label, SHA-256 of the workbook, author role, authored date, environment | Not specified in the source documents (DOR-RWB-P3-E2042-CON-7) |
| Model resource | packageCode, versionLabel, checksum (SHA-256), the model content and its compiler version, the valid-from date | Not specified in the source documents (DOR-RWB-P3-E2042-CON-7) |
| Catalog resource | ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code, outputs | Not specified in the source documents (DOR-RWB-P3-E2042-CON-7) |
| Event payload | package code, version label, checksum, valid-from date, published at; identifiers and business facts only | Not specified in the source documents (DOR-RWB-P3-E2042-CON-7) |
| Activity input and output | package code, facts reference, business date in; packageCode, packageVersion, ruleId, outputs out | Not specified in the source documents (DOR-RWB-P3-E2042-CON-7) |

The field-level detail of the model and catalog resources — property types, lengths, required flags and the compiler-version element — is Not specified in the source documents (GAP-0722; ASM-1269); this story fixes the element names above and leaves the types to the review with the rwb-decision owner. The Blob retention and immutability period are likewise Not specified in the source documents (GAP-0723; ASM-1270) and are fixed in RWB-P3-E2042-INF.

### 12. Contract

Rule-model read (GAP-0722): GET /rule-models/{packageCode}/{version} answers packageCode, versionLabel, checksum (SHA-256), model content, compiler version and valid-from date. Property types, lengths and required flags stay open with the rwb-decision owner; the WireMock fake carries these element names as assumed shapes.

Rule-catalog read (GAP-2405, GAP-0722): GET /rule-catalog/{ruleId}?packageVersion= answers 200 with ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code and outputs. An unknown rule or version answers 404 with a not-found message that is Not specified in the source documents (GAP-2405); a malformed packageVersion parameter answers 422 with MSG-GEN-001.

#### 12.1 REST operations provided

None. The rwb-case side of the three Epic 2 packages serves no new business operation. The model cache is internal, the packages are read from rwb-decision, and the case reads that carry a rule outcome are the operations of their own stories (`GET /api/recovery/case/v1/cases/{caseId}` and the case read surface of RWB-P3-E1023-CON). This baseline declares no cache read: a cache inspection path would be an operator concern and is carried by RWB-P3-E2042-OPS as a metric, not as an operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The compiled model, its version label and its SHA-256; faked with one correct checksum and one wrong checksum |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | P7 rwb-decision | action_text, owner_role, timer_spec and outputs of one rule row; faked for R-RES-04 and the route-set rows |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The version list, the status of each version and the checksum of the one in force; faked |
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The multipart load of a workbook with validFrom; faked with 201, 409 and 422 |
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | P7 rwb-decision | The four-eyes approval; faked with 200, 403 and 409 |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020). The load and approve operations are called by the center of excellence analyst and the risk officer through the Workbench; rwb-case never calls them from a workflow.

#### 12.3 Events published

None. This contract publishes no event type. The shared ledger event `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library of DP-03 when a decision is taken in rwb-case; its schema is unchanged by this story and is the one declared in RWB-P3-E1018-CON.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 | CloudEvents 1.0; key = package code; payload = package code, version label, checksum, valid-from date, published at; inbox dedupe; starts one model swap and nothing else |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| RuleModelSwap | Workflow started by RulePackageInForce | `rwb-case` | Input: package code, version label, checksum, valid-from date. One execution per package code and version label |
| swapRuleModel | Activity | `rwb-case` | Input: package code, version label, checksum. Output: the cached version, the built KieBase reference and the outcome loaded, unchanged or refused |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Input: package code, facts, business date. Output: `RuleResult(packageCode, packageVersion, ruleId, outputs)`; raises `NoPackageInForce`, which is non-retryable |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Input: the decision record, the state change and the outbox rows; one transaction, and no partial write |

The swap contract is the only one this story adds: the evaluation contract is the kit's and is restated here so that the catalogue read and the evaluation name the same package version.

#### 12.6 Schedules

None. The 00:01 promotion is the Temporal Schedule JOB-20 in rwb-decision, owned there and announced as RulePackageInForce (Arch v5 slide 44). rwb-case registers no Schedule for a rule package.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case facts an evaluation reads; no column added |
| timer | P3 (rwb_case) | The due date a route-set row sets; no column added |
| queue | P3 (rwb_case) | The target queue a rule row names; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The outbox, inbox and idempotency envelope of the consumer (DP-09) |

No other table is named in the contract. The four registry tables are rwb-decision's and are never read directly (ASM-0069; DP-01). `payment_match_rule` does not exist.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock — models | `GET /rule-models/{packageCode}/{version}` for RES-2026.12, PMT-2026.12 and BKG-2026.12 with their SHA-256, one wrong checksum, one 404 and one slow answer | App story, contract tests |
| rwb-decision WireMock — catalog | `GET /rule-catalog/{ruleId}?packageVersion=` for R-RES-04 and the route-set rows, with a 404 answer for an unknown rule ID | App story, contract tests |
| rwb-decision WireMock — versions | The version list, the load answers 201, 409 and 422, and the approve answers 200, 403 and 409 | App story, test stories |
| rwb-access WireMock | `POST /authorise` granting Rules and parameters to RW-COE and RW-RISK and refusing a role without the right | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 5 consumed | The model, catalog, version list, load and approve operations of rwb-decision; one hop, 2 s timeout |
| Kafka | None published, 1 consumed | `rwb.decision.events.v1` for RulePackageInForce |
| Temporal | 1 workflow, 1 added activity | RuleModelSwap and swapRuleModel; EvaluateRules and RecordAndApply are the kit's |
| File | 3 workbooks | The three xlsx configuration workbooks, uploaded once per version through the rwb-decision load; no runtime file exchange |

### 13. Solution plan

**Deliverables.** `contract/rule-package-workbook-schema.yaml` (the Rows and Tests schema of a workbook, with the package code as RuleSet and the rule ID in NAME; the package version names its format, an XLS decision table or a DMN 1.6 model, and which format the load checks, the checksum and the model fetch accept is set by the ADR-017 ruling), `contract/rule-package-blob.md` (the object naming and the metadata keys), `contract/rule-model-consumed.yaml` (the five consumed rwb-decision operations), `contract/rule-package-in-force.md` (the event contract), `contract/evaluate-rules.yaml` (the activity input, `RuleResult` and `NoPackageInForce`), and the three WireMock mappings.

Not specified in the source documents (GAP-1302): the title text of each package row (DF-REF-276), the breakdown of dry_run_counts (DF-REF-293), the text of MSG-P3-015, the rollback answer beyond the two version states and the answer of the three admin operations when the legacy flag is off. The tests assert presence and stability only.

**Registry scope.** The four rule registry tables are owned by rwb-decision in its own schema, and this story builds no P3 or P4 declaration of them (GAP-1301). The registry, the seeding, the admin operations, the approval, the rollback and JOB-20 stay in RWB-P7-E2042-APP (ASM-A6-tables-3). This story keeps the workbook authoring, the Blob object, the model cache, the checksum check, the atomic swap, the catalog read and the schema assertion, and proves AC1 to AC3 against the rwb-decision contract mock here; the real-service proof is in RWB-ITG-E2042-ITG (GAP-0721).

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
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Write the workbook schema: the Rows tab with RuleSet and NAME, the condition and output columns per package, the default row last, and the Tests tab with the twelve rule_test_case columns; add a schema lint to the pipeline.
2. Write the Blob contract: the `<PACKAGE_CODE>/<VERSION_LABEL>.xlsx` path, the write-once rule and the metadata keys, and hand it to RWB-P3-E2042-INF.
3. Document the five consumed operations from the rwb-decision documents, with the 2 s budget and the error codes; the model and catalog elements are agreed under GAP-0722.
4. Write the RulePackageInForce contract: envelope, key, payload, dedupe and the `.dlt` rule.
5. Write the activity contract: the input, `RuleResult`, `NoPackageInForce`, the cache bound, the atomic swap and the last-good-model rule.
6. Build the four WireMock mappings and their fixtures.
7. Add the six contract tests, including the drift test between each fake and this document.
8. Tag the baseline and collect the sign-off of the app, infrastructure, operations and test stories.

**Done when.** The five contract files validate in the pipeline, the six contract tests pass, the four fakes answer every consumed path and payload, and the app, infrastructure, operations and test stories of this legacy key have accepted the baseline.

**Harness.** The harness repository, the SIT environment, the seeding set for the three package versions and the two payment cases, the per-run evidence format and retention, the pass or fail gate and the fake response bodies are agreed at the wave 2 entry check with rwb-decision, rwb-payment and QA, and held as data in the harness pack, not in this story (GAP-0421).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A workbook fails the authoring schema or the tests-tab schema | The {table} load was refused: {check}. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | An empty workbook or an empty required cell | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without Rules and parameters calls a package operation | You cannot {action} here. Your role does not include it. |

The texts are the agreed texts of the legacy story and of the platform catalogue; this contract adds no message. The `{check}` value is compile, schema, overlap, unreachable row, default row or scenario, and the `{table}` names rows, cells, rule IDs, package codes and version labels only.

### 15. Screens and states

None in this story. For SCR-39 Rules and parameters the empty, loading, error and no access states are Not specified in the source documents (CG-ALL-4407). The contract serves the version list that SCR-39 Rules and parameters shows in Epic 8 and the package columns of the case screens only indirectly, through the rule outcome a decision carries. The cache states are internal to rwb-case and are exposed as the readiness signal and the metrics of RWB-P3-E2042-OPS, not as a screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2042-CON-01 | AC1 | Contract | Three workbooks validated against the Rows and Tests schema; a wrong RuleSet, a wrong NAME and a missing default row are each refused |
| TC-P3-E2042-CON-02 | AC2 | Contract | The metadata keys are present on all three objects; a second write is refused; no run-time workbook read exists |
| TC-P3-E2042-CON-03 | AC3 | Contract | The five consumed operations are documented with method, path, purpose, rights and budget; the fake answers each path |
| TC-P3-E2042-CON-04 | AC4 | Component | A valid, a duplicate, a checksum-less and an unknown-package RulePackageInForce message |
| TC-P3-E2042-CON-05 | AC5 | Component | EvaluateRules returns RuleResult; NoPackageInForce is non-retryable; the cache bound, the eviction and the swap are exercised |
| TC-P3-E2042-CON-06 | AC6 | Component | The nine sub-tables are complete; 12.1, 12.3 and 12.6 are None; the fakes match the document; no payment_match_rule element exists |
| TC-P3-E2042-CON-07 | AC6 | Contract | Boundary of 12.7: the four tables are the only tables named; each table row names an owner and a contracted use; payment_match_rule is absent |
| TC-P3-E2042-CON-08 | BR1 to BR10 | Contract | One check per rule of section 8: authoring form, identity, write-once, checksum match, registry ownership, evaluation inside the activity, cache bound, REST base, no business value, retired payment_match_rule |
| TC-P3-E2042-CON-09 | AC7 | Contract | Each of BR1 to BR10 has one check and its source named in section 8; a rule without a check fails the review |
| TC-P3-E2042-CON-10 | AC8 | Component | A consumed call that times out and one that returns an error from the rwb-decision fake; each is reported, and the last good model stays in force |

### 17. Guardrails

- No business value in the contract: rows, tolerances, windows, action text, owner roles, timers and queue codes stay data of the workbooks and the registry.
- No personal data in an event, an activity input, an example or a fake: identifiers and business facts only.
- The contract names only rwb-case tables and only rwb-case operations as provided; the five rwb-decision operations are consumed and never restated as this service's (DP-01, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- `payment_match_rule` and DF-REF-261 to DF-REF-273 appear nowhere as an element of the contract.
- Every example and fixture is synthetic; no production workbook, payload or checksum is copied into a schema or a fake.
- The envelope, the naming rule and the embedded Drools kit elements come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | The load, version-list and approve operations; the RulePackageInForce contract; the Blob metadata | TC-P3-E2042-CON-02, TC-P3-E2042-CON-03, TC-P3-E2042-CON-04 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | The Rows and Tests schema, the scenario count and the refusal rule | TC-P3-E2042-CON-01 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The consumed model and catalog operations, the cache rules and the activity contract | TC-P3-E2042-CON-03, TC-P3-E2042-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed operations with the 2 s client budget | TC-P3-E2042-CON-03 |
| D-RCV-36 T10 | `payment_match_rule` is retired | The absence rule in 12.7 and the retired field IDs | TC-P3-E2042-CON-06 |

### 19. Out of scope

- The implementation of the cache, the swap, the catalog client and the schema gate (RWB-P3-E2042-APP).
- The registry rows, the three seed rows, the load and approve operations, the approval, the rollback and JOB-20 (RWB-P7-E2042-APP; ASM-0069).
- The Blob container, the identity, the certificate and the sizing (RWB-P3-E2042-INF).
- The Helm values, the consumer group, the dashboards, the alerts and the runbook (RWB-P3-E2042-OPS).
- The evaluation of the three packages in the stories that own those decisions (RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008, RWB-E2-027, RWB-E2-035).
- The real cross-service proof of the load, the approval, the promotion and the swap (RWB-ITG-E2042-ITG).
- The field-level completeness of the model and catalog resources (GAP-0722) and the Blob retention period (GAP-0723).
