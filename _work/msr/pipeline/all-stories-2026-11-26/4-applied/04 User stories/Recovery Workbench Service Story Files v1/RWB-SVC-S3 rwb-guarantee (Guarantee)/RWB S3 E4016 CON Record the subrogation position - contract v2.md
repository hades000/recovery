# RWB-S3-E4016-CON Record the subrogation position - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S3-E4016-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-016, the baseline the subrogation step of rwb-guarantee builds against on Day 1. The baseline declares the claim-result slice of `PATCH /guarantee-claims/{claimId}` (API-S3-002) on `/api/recovery/guarantee/v1` (DP-13), the subrogation elements of `GuaranteeClaimUpdate` in and `GuaranteeClaim` out, the consumed posted-payment event of rwb-payment with its placeholder name (DP-05), the decision-record element and the library that carries it (DP-03), the elements of `GuaranteeClaimWorkflow` and its three subrogation activities, the right and the error envelope, the subject of SCR-17 through the gateway-bff composite route (DP-19), the fakes and the naming and boundary rule; it publishes no event, because the ownership rows give S3 none. No field, column or element exists for the position or for the guaranteed amount of R-GUA-22 (GAP-2720; ASM-4518); the payment arrives only on the rwb-payment event and its event name is not published (GAP-2721; ASM-4519); no event of this service is authored and no peer event name is published (GAP-2722; ASM-4520); R-GUA-23 and R-GUA-24 are identical and the claim's record status list is not mapped to the GUARANTEE case states (GAP-2723; ASM-4521); the TCG share has no published source (GAP-2724; ASM-4522). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S3-E4016-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-guarantee**, I want **the published contract baseline of the subrogation step of rwb-guarantee, being its claim-update operation, its position element set, its consumed payment event, its record and workflow elements, its right, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the sibling claim stories of this service and the wave 3 harness can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-016. It owns:

- the document that fixes the claim-result slice of `PATCH /guarantee-claims/{claimId}` (API-S3-002) on base `/api/recovery/guarantee/v1`: `GuaranteeClaimUpdate` in, `GuaranteeClaim` out, the `version` check, the right and the error set (DP-13);
- the subrogation element set: the share, its basis, its effective scope, the set-at time, the guaranteed amount the rule compares with the paid amount, and the claim status the record carries, declared as an additive extension of the element set the sibling claim baselines of this service start (GAP-2720);
- the consumed posted-payment event of rwb-payment: its topic, its key, its inbox treatment, its placeholder name and the elements this service reads from it (GAP-2721; GAP-2722);
- the decision-record element, the library that carries it, the transaction it joins and the shared topic it reaches (DP-03);
- the elements of `GuaranteeClaimWorkflow` and the three subrogation activities on task queue `rwb-guarantee`, as a child of `CaseWorkflow`;
- the right of the operation, Treatment and offer U, and the roles that hold it, with the unattended step running under the service identity (GAP-2724);
- the subject of SCR-17 Guarantee claim, one hop through the gateway-bff composite route (DP-19);
- the fakes and their documented answers, and the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no `v_ace_*` grant, no monolith base.

It does not own: the subrogation behaviour, its checks, the claim writes, the case moves and the screen's behaviour, which are RWB-S3-E4016-APP; the claim preparation, submission and tracking baselines of this service; the guarantor notice and negotiation baselines; the close of the guarantee, which is FEAT-GUA-07's; the case of record and its states, which are rwb-case's (P3); the posting, the ledger and the ALS entry, which are rwb-payment's (P8); the rule rows and the package version, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets the slices of one operation start together. Legacy RWB-E4-016 asks the Workbench to record what the guarantor may reclaim after payment, with the rule version on the record, so the step reads a payment fact from another service, applies a rule set of its own and writes a claim row and a record in one transaction. Three sibling claim stories of this service touch the same claim record and the same answer, and without one tagged element set each would invent its own answer at the first integration.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** The payment row names its owner, its key, its inbox treatment and the 2 s rule does not apply to it because it is an event; the event name is not published, so the row carries the placeholder and its gap (GAP-2721; ASM-4519).
- **the position is data, not a number.** The share, its basis and its scope are declared with their source and their version, and the document carries no value, no percentage and no default, because BR-S3-004 forbids a business value in code (GAP-2720; GAP-2724).
- **additive only.** The subrogation elements are a minor version of the element set the sibling claim baselines start: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version and a new document.

The business outcome the baseline protects is the one FEAT-GUA-04, FSD S3 A2.4 and REQ-S3-003 state: a guarantee payment that clears the balance records the subrogation position, so the position is not lost for later recoveries. The baseline states no outcome and no business value of its own, and no criterion here asserts that a payment is full, that a share applies or that a case moves.

### 3. Preconditions

- The Ownership Map rows for S3 are in force: the table `guarantee_claim`, the operations `PATCH /guarantee-claims/{claimId}` and `POST /cases/{caseId}/guarantee-claims`, no event, no job, and one workflow, `GuaranteeClaimWorkflow`. Only the claim update belongs to this baseline.
- The service naming is fixed: schema `rwb_guarantee`, one login of its own, base `/api/recovery/guarantee/v1`, topic `rwb.guarantee.events.v1` with `.retry` and `.dlt`, task queue `rwb-guarantee` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.guarantee`.
- TSD S3 is the shape of record for the service: T-A.1 gives API-S3-002 with right Treatment and offer U; T-A.2 gives `GuaranteeClaimUpdate` in, `GuaranteeClaim` out, errors 401, 403, 404, 409, 422 and 503, and idempotency "Not applicable"; T3.0 gives the optimistic `version`; T3.1 gives the eight fields of `guarantee_claim`; T3.2 gives `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS`; T4 gives the GUARANTEE state set; T6.1 gives the capability area and its rights.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The element lists of `GuaranteeClaimUpdate` and `GuaranteeClaim` are Not specified in the source documents beyond the two type names of T-A.2 (GAP-2720; ASM-4518); the baseline declares the elements the requirements name and marks the rest open.
- The posted-payment event of rwb-payment is Not specified in the source documents: neither its name, its key nor its elements are published, and the ownership rows give this service no event of its own (GAP-2721; GAP-2722; ASM-4519; ASM-4520).
- The eight fields of `guarantee_claim` end at DF-TRT-022, and no field, column or code holds the subrogation position or the guaranteed amount of R-GUA-22 (GAP-2720; ASM-4518).
- R-GUA-23 and R-GUA-24 carry the same action and differ only in their from-state, and no source maps `LOV-CLAIM-STATUS` to the GUARANTEE case states (GAP-2723; ASM-4521).
- TSD S3 T5.1 records INT-29, the Thai Credit Guarantee Corporation, as "Not available today; entered and filed by the guarantee officer", so no interface, file or endpoint of TCG is declared (GAP-2724; ASM-4522).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S3 T-A.1, T-A.2, T3.0 to T3.3 and T6.1, the FSD S3 A2.4 rules and roles, the three GUA rows of the routing logic and the DP table.
2. The provided operation is declared with its method, path, request, documented answer, right, `version` check and error set.
3. The position element set is declared with its type, its nullability and its source, and marked as an additive minor version of the element set the sibling claim baselines of the service start.
4. The guaranteed amount and the claim status elements are declared as values the rule reads, with no number, no percentage and no default written.
5. The consumed payment event is declared with its owner, its topic, its key, its inbox treatment and a placeholder where the element or the name is not published.
6. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins, and the position is declared as an element of the record and of the claim answer and not as a new table.
7. The workflow and its three subrogation activities are declared with their input, their signal and their outcome elements.
8. The right is declared per operation, with right U for the four officer roles and the service identity for the unattended step, and the error set is declared in one envelope.
9. The fakes are declared with their documented answers: one for the payment event, one for the decision-record library, one for the composite route and one for the claim answer.
10. The compatibility check runs on the draft against the previous tag of the element set: a breaking change fails it, an additive one passes as a minor version.
11. The document goes to review as Draft; the reviewers are the owners of the consumed event, the owners of the sibling claim baselines and the tech lead of the service.
12. On the review's close the document is tagged; the application story, the harness and the sibling slices start against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row or the element carries the placeholder and its gap; no path, no field and no event name is invented | C3, C7 |
| X2 | A change removes, renames, retypes or newly requires an element of the shared answer | The compatibility check fails and the change needs a new major version of the element set | C1 |
| X3 | A declared operation or element reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C6 |
| X4 | The consumed event has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C5 |
| X5 | The right of the operation is not a row of the access matrix, or the unattended step has no identity | The operation is not declared and the error set stays incomplete | C4 |
| X6 | An owner changes its documented answer after the tag, or publishes the event name or the position field | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2 |
| X7 | Two documents or two slices claim a different element of the same path, or the same base, topic or queue | The owner named in the baseline keeps the element, the other slice extends it additively, and the naming rule decides the rest | C6, C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 the paths of a baseline moving under a build, and X7 is the boundary between the claim slices of one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the path, the request, the answer, the right, the position elements and the error set are fixed by TSD S3 and FSD S3 |
| Valuable | Three claim stories and one harness build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation, one consumed event, one element set of five position elements, one record element, one workflow with three activities, one subject of SCR-17 and four fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the subrogation step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The operation and the position elements are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When PATCH /guarantee-claims/{claimId} on /api/recovery/guarantee/v1 is read
    Then it names GuaranteeClaimUpdate in, GuaranteeClaim out, the version check and the scope rule of T-A.2
    And the position elements name the share, its basis, its effective scope, the set-at time, the guaranteed amount and the claim status

  Scenario: C3 The consumed payment event carries its owner, its key and its placeholder (new, D-RCV-60)
    Given the consumed event table of the baseline
    When the row of rwb-payment is read
    Then it names the owner, the topic rwb.payment.events.v1, the key, the inbox treatment and the elements this service reads
    And where the event name or an element is not published the row carries the placeholder and the gap identifier and no invented name

  Scenario: C4 The right and the error envelope are declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the right and the error set of the operation are read
    Then right U of Treatment and offer is declared for RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL and RW-GUARANT, and the service identity for the unattended step
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409 on a stale version, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: C5 The decision-record element, the workflow elements and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the workflow table and the fake table are read
    Then the element names RWB-PLT-E1027-CON as its library, the shared topic, the transaction it joins and the position as an element of the record
    And GuaranteeClaimWorkflow and its three subrogation activities name their input, their signal and their task queue
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub

  Scenario: C6 The position is governed data and the naming boundary holds (new, D-RCV-60)
    Given the position elements, the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the value rule, the naming rule and the event list
    Then the share, its basis and its scope carry their source and their version, and no value, percentage or default appears
    And one base, one topic, one queue and one login are declared, with no monolith base, no foreign topic, no v_ace_* grant and no published event

  Scenario: C7 The two subrogation paths share one element set and one operation (new, D-RCV-60)
    Given the element list of the claim answer and the rule rows R-GUA-23 and R-GUA-24
    When the two paths are compared element by element
    Then both are carried by one claim-update element set, with no second operation, event, table or state name
    And a slice that redefines or duplicates an element fails the review and the compatibility check
```

The seven criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the consumed event, the right, the envelope, the record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts that a payment is full, that a share applies or that a claim status changes.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, element, event and table: the baseline declares the claim update that the Ownership Map gives S3, names the consumed event with its owner, and claims no other surface | Ownership Map rows of S3; TSD S3 T-A.1 |
| BR2 | A consumed event whose name or element is not published carries the placeholder and its gap and never an invented name, an invented key or an invented payload | Template and Rules v1 §R9; GAP-2721; GAP-2722 |
| BR3 | The baseline is additive against the element set the sibling claim slices start: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; s9 |
| BR4 | The share, its basis and its effective scope are declared as elements of governed data with their source and their version; their values, percentages and defaults are never written | FSD S3 A2.4.3.1 BR-S3-004; GAP-2724 |
| BR5 | The payment arrives on the rwb-payment event and not on a table: the baseline declares no `v_ace_*` grant, no ACE view read and no direct call to the payment service | DP-05; Arch v5 slide 8 and slide 13 |
| BR6 | No event is published by this baseline: the ownership rows give S3 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S3 ownership rows; ASM-4520 |
| BR7 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before the claim moves, and the position is an element of that record and of the claim answer and not a new table | DP-03; R-UNI-39; GAP-2720 |
| BR8 | No business value is declared in the baseline: the claim types, the claim statuses, the share and the case states are referenced with their identifier, their list or their version | TSD S3 T3.2; FSD S3 A2.4.3.1 BR-S3-004 |
| BR9 | The right is declared once: Treatment and offer U for the four officer roles of the legacy permission table, and the service identity for the unattended step; no wider role is invented | TSD S3 T6.1; legacy permission table; GAP-2724 |
| BR10 | No personal data in any element, fake, example or log of the baseline | Template and Rules v1 §R7.2 (s17) |
| BR11 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, element, event, right, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the consumed event and of the sibling baselines are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story and the harness |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional position element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the slices are notified |
| Baselined | An owner publishes the event name or names the position field | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed event has no published name | X1 | The row carries the placeholder and the gap, and the draft continues |
| In review | A row or an element reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| Ready to tag | The consumed event has no fake, or a sibling slice redefines an element | X4, X7 | Not tagged, and the review reopens |

The claim states of the GUARANTEE set are the rows of TSD S3 T4, and `LOV-CLAIM-STATUS` is the row of T3.2; this baseline names them as values the elements carry and maps neither list beyond the one step that GAP-2723 records (ASM-4521).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-guarantee | Authors the baseline, resolves the shape of the service's own operation, the position elements and the decision-record element, and signs the tag |
| Owner of rwb-payment (P8) | Reviews the consumed payment event, publishes its name and its elements when they exist, and confirms the posting is not this service's |
| Owner of rwb-case (P3) | Reviews the case-move answers and the GUARANTEE state names of the D6.5 stage |
| Owner of rwb-decision (P7) | Reviews the rule rows of the GUARANTEE set, the package version and the element that carries the resolution |
| Owner of rwb-access (P4) | Reviews the capability area, the right U and the roles that hold it, and the identity of the unattended step |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Owner of the sibling claim baselines | Reviews the additive extension of the shared claim-answer element set and confirms that no element is redefined |
| Guarantee officer role holder | Confirms that the declared position elements are the ones the officer needs to record and to be audited |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The claim elements of `guarantee_claim` (DF-TRT-015 to DF-TRT-022) | S3 (`rwb_guarantee`) | The claim reference, the claim type, the claimed amount, the paid amount, the status and the optimistic `version`; referenced, not redefined | Read and written |
| The subrogation position (no Field ID published) | The claim's own fact; its field is Not specified in the source documents (GAP-2720; ASM-4518) | The share, its basis, its effective scope and the set-at time, declared with their source and no value | Written as an element of the claim answer and of the record |
| The guaranteed amount of R-GUA-22 (no Field ID published) | The same open point (GAP-2720) | The amount the full payment is compared with, declared as an element and no number | Consumed from the claim or the rule row |
| The posted payment (no Field ID published, event element) | P8 (`rwb_payment`) | The case, the payment reference, the amount, the posting date and the channel; declared with a placeholder where the element is not published (GAP-2721) | Consumed on the event |
| The case elements of `recovery_case` (DF-CAS-001 to DF-CAS-023) | P3 (`rwb_case`) | The case reference and the states `CLAIM_SUBMITTED`, `CLAIM_PAID`, `CLAIM_PART_PAID` and `SUBROGATION_POSITION`; referenced, not redefined | Reported, not written |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_guarantee` | The decision code, the rule id, the rule version, the inputs reference, the claim, the payment reference, the share and the decider's role | Written through the library |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | rule_id, rule_version and the GUARANTEE set; referenced, not redefined | Consumed as a row in force |

The baseline declares one table, `guarantee_claim`, because it is the one table the Ownership Map gives S3, and it declares no column and no migration: `rwb_guarantee` and its login arrive with the DB story of this service, and the record and the idempotency key are library objects created in it by the library's migration (DP-03). It enumerates no business value: every list, code, share and state is referenced with its identifier and its version. **No personal data** appears in any element, fake or example, every fixture identifier is synthetic, and the officer is a role and never a person.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). This is the operation the legacy story names in its Endpoints table for the claim result, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` in and `GuaranteeClaim` out, carrying the claim result and the subrogation position with its share, its basis, its effective scope, the set-at time, the guaranteed amount and the claim status (API-S3-002) | Treatment and offer, right U, scope applied; the unattended step runs under the service identity | Not applicable in TSD S3 T-A.2; the answer carries the optimistic `version` and a stale value is refused with 409 |

The element lists of `GuaranteeClaimUpdate` and `GuaranteeClaim` are not published beyond the two type names of T-A.2, so the baseline declares the compact of the slices: the claim preparation, the submission and tracking and this subrogation step each add their own optional elements, and none redefines another's (GAP-2720; ASM-4518; C7). Opening a claim on `POST /cases/{caseId}/guarantee-claims` (API-S3-001) is the claim-preparation baseline of this service and is not declared here.

The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope claim, 409 on a stale `version`, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

None. The call matrix of Architecture v5 slide 13 gives S3 no REST edge, and route services reach shared capabilities through Temporal, never REST. The baseline therefore declares no consumed operation, no 2 s budget and no breaker, and the payment, the rules and the case arrive as an event fact, a rule row in force and a parent workflow state.

#### 12.3 Events published

None. The ownership rows give rwb-guarantee no event: the topic `rwb.guarantee.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it (GAP-2722; ASM-4520). The only publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

| Event | Topic | Owner | Declared elements | Used by |
|---|---|---|---|---|
| The posted-payment event (name Not specified in the source documents (GAP-2722; ASM-4520)) | `rwb.payment.events.v1`, with `.retry` and `.dlt` | P8 rwb-payment | The case reference, the payment reference, the payment amount, the posting date and the channel, with a placeholder where an element is not published (GAP-2721) | C3, C5 |

One subscription with the inbox of the platform event library: the event is stored once by its key and the repeat is ignored (R-UNI-40). The baseline declares no second subscription, because slide 13 gives S3 an event subscription from P8 and from no other service, and it declares no polling, no file and no batch read of the payment.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` | Workflow, one child execution per case per guarantee stage, child of `CaseWorkflow`, continues-as-new | `rwb-guarantee` in namespace `rwb-recovery` | Input: the case, the claim and the rule version in force; signal: the posted-payment fact; the stage outcome and the two case moves reported to the parent; carries the subrogation step |
| `matchFullPayment` | Activity | `rwb-guarantee` | The case, the claim and the payment fact in; the matched payment, the paid amount, the guaranteed amount and the full-payment flag out |
| `evaluateSubrogationRules` | Activity | `rwb-guarantee` | The claim state, the payment result and the business date in; the rule row that fired, its version, the share and the basis and the target state out |
| `recordAndApply` | Activity | `rwb-guarantee` | The claim update and the position in; the claim row, the decision record and the outbox row out, in one transaction, plus the reported case moves |

`GuaranteeClaimWorkflow` is the one workflow the ownership rows give S3. This baseline fixes its input, its one signal and the three activities of the subrogation step; the remaining activities of the claim are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S3 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. The step runs from the payment fact inside the workflow, and the claim deadline clock is FEAT-GUA-03's and is a workflow timer there (ASM-4523).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `guarantee_claim` | S3, in `rwb_guarantee` | The claim of record: the claim type, the deadline, the claimed and paid amounts, the status and the optimistic `version` (DF-TRT-015 to DF-TRT-022) |
| decision_record | PLT library, created in `rwb_guarantee` | The local hash-linked decision-record element of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_guarantee` | The key of the repeated fact and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `case_party`, `assignment`, `task` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8), `document` (P5), `deviation` (S8) and every `v_ace_*` view (P1) are named with their owner and never declared here. The position is not a table: it is an element of the record and of the claim answer until the data owner names the field (GAP-2720; ASM-4518).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment payment-event fake | A posted full payment for claim `CLM-2027-000416`: the case, the payment reference, the amount and the posting date; the same event replayed; a partial payment; an event with an unknown reference | C3, C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain; a record with and without the position element | C5 |
| rwb-guarantee claim-update fake | The claim answer in claim status `FILED` and `PAID`, with and without a position, and a stale `version` | C2, C4 |
| gateway-bff composite route fake | The merged SCR-17 answer for the claim, with the deadline, the payment, the position and its share read once | C2, C5 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The consumed event name is not published, so the row is stubbed from the documents and carries the placeholder until its owner confirms it (GAP-2721; GAP-2722; ASM-4519).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 0 consumed | `PATCH /guarantee-claims/{claimId}` on `/api/recovery/guarantee/v1`; the call matrix gives S3 no REST edge |
| Kafka | 0 published, 1 consumed | One subscription from rwb-payment on `rwb.payment.events.v1`, with the inbox key; no event of this service; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 3 activities | `GuaranteeClaimWorkflow`, `matchFullPayment`, `evaluateSubrogationRules` and `recordAndApply` on `rwb-guarantee`, as a child of `CaseWorkflow`; no Schedule, one durable wait |
| File | None declared | The step writes no file and calls no external system; INT-29 is not declared (GAP-2724) |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S3 rwb-guarantee (Guarantee)/RWB S3 E4016 CON Record the subrogation position - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S3-E4016.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied by retirement rather than by a call: the baseline declares no `v_ace_*` element and no ACE view grant, and the payment arrives on the event, so neither the rwb-source-data contract nor the own-view alternative is declared and no dependency is added.

**Sections and owners of the review.** The document is written in nine parts: the provided operation, the position elements, the consumed event, the guaranteed amount and the claim status, the record element, the workflow and its activities, the right and the envelope, the fakes, and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag of the element set, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3). The check also compares the two subrogation paths element by element (C7).

**Fakes.** One per consumed row plus the claim answer and the composite route, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C5).

**Done when.** The seven criteria pass, the reviewers have closed their comments, the compatibility check passes on the tag and against the sibling element sets, the four fakes are published with their documented answers, and RWB-S3-E4016-APP and the wave 3 harness can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without right U of the declared operation calls it | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `GuaranteeClaimUpdate` or of the position is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check, or a slice redefines an element of another slice | A breaking change needs a new major version. |
| Document rule | A consumed event has no published name, or the position has no published field | Not specified in the source documents (GAP-2720; GAP-2722; ASM-4518; ASM-4520). |

The three message IDs are the rows of the legacy Validation and messages table of this key, copied unchanged. The two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-17 Guarantee claim through the gateway-bff composite route (DP-19). What this story fixes is the position element list of the claim answer and the states the screen can show from this step.

| Screen | States | What the screen reads on this step |
|---|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused | The claim, its deadline, the posted payment, the position with its share, its basis and its scope, the claim status and the decision record with its rule version; plus the held and not-recorded states of the step |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The position is shown inside the legacy "paid" state and the baseline declares no sixth state (GAP-2720). The screen itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-016-01 | C2, C7: the position elements of the claim answer, their nullability, and the two subrogation paths carrying one element set | Contract | The published schema, the element list, and the recorded answers of claim `CLM-2027-000416` with and without a position |
| TC-E4-016-02 | C2, C5: the operation, the `version` check and the decision-record element | Contract | One request per rule path, a stale `version`, and a healthy and a stopped record stub |
| TC-E4-016-03 | C4: the right and the error envelope of the declared operation | Contract | One request per role, one request from the service identity, and one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-016-04 | C1, C6: the boundary, the empty publication and the additive rule | Contract | The base, the topic, the queue and the schema; an outbox declaration that must stay empty; an additive and a breaking draft |
| TC-E4-016-05 | C4: the access path of the baseline | Contract | A role without U of Treatment and offer, and an out-of-scope claim, answered with MSG-P4-002 |
| TC-E4-016-06 | C5, C6: the stopped record chain and the value rule | Contract | A forced record failure, and a share element carrying a value or a default, which must fail the check |
| TC-S3-E4016-CON-01 | C3: the placeholder and the gap of the consumed event, its topic, its key and its inbox treatment | Contract | The payment row with and without a published name; an event with no fake |
| TC-S3-E4016-CON-02 | C2, C6: the guaranteed amount and the claim status elements, and the one base, topic, queue and login | Contract | The element list of the claim answer, and a draft naming a foreign base or topic |
| TC-S3-E4016-CON-03 | C7: the two subrogation paths | Contract | The two rule rows, one element declaration with a redefined element and one with a duplicate |

The six legacy case IDs are the legacy test cases of RWB-E4-016 in their legacy order, mapped onto this contract deliverable: the four criteria (01 to 04), the access path (05) and the principle-5 record failure (06). The three `TC-S3-E4016-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness, RWB-ITG-W3J01.

### 17. Guardrails

- No business value in the baseline: the claim types of `LOV-CLAIM-TYPE`, the claim statuses of `LOV-CLAIM-STATUS`, the share and the case states are referenced with their identifier, list or version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and versions only, and the officer is a role and never a person.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the retired `v_ace_payment` read is not declared (DP-05).
- The case stays with rwb-case and the money with rwb-payment: no `recovery_case` element, no `proceeds` element and no posting element is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no Schedule, no foreign schema and no event published by this baseline.
- Additive only: the claim slices extend one element set, a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3, C7).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-016, disposition Split (rework); AC1 to AC4 are owned by RWB-S3-E4016-APP; this story carries no legacy criterion and fixes the surface that story touches | 1, 11, 12, 16 |
| Feature | FEAT-GUA-04 Record the subrogation position, module S3, epic E4, runs unattended, systems ALS and GL and Workbench, depends on FEAT-GUA-03 | 1, 2, 3 |
| FSD S3 v3 | A1.4 preconditions; A2.4.2 steps and integration points; A2.4.3.1 VR-S3-004-1 and BR-S3-004; A2.4.3.3 roles; requirements REQ-S3-001 to REQ-S3-007, REQ-S3-003 in particular; SCR-17 | 2, 3, 8, 12, 14, 15 |
| TSD S3 v2 | T2 components; T3.0 standard columns; T3.1 `guarantee_claim`; T3.2 `LOV-CLAIM-TYPE` and `LOV-CLAIM-STATUS`; T3.3 relationships; T4 GUARANTEE state machine; T5.1 INT-29; T5.3 no event; T6.1 rights; T-A.1 and T-A.2 API-S3-002 | 3, 9, 10, 11, 12, 16 |
| Business rules | R-GUA-22, R-GUA-23 and R-GUA-24 of the Guarantee claim route set; R-GUA-25 and R-GUA-26 as the follow-on rows | 9, 12, 13 |
| Logical data model | DF-TRT-015 to DF-TRT-022, DF-CAS-001 to DF-CAS-023, DF-REF-001 to DF-REF-015 and DF-DEC-001 to DF-DEC-018 | 11 |
| Epics 3 to 8 Specification v3 | The feature row of FEAT-GUA-04 with its unattended role, its systems and its dependency on FEAT-GUA-03 | 1, 2 |
| Architecture v5 | Slide 3, the guarantee claim route; slide 8, the schema, base, topic and queue of the service and the ACE views closed to it; slide 13, S3 temporal to P7 and subscriptions from P6 and P8; slide 12 and 13 of the Temporal design, the child-per-stage model and the kit | 2, 3, 12 |
| Sibling baselines | The claim preparation, submission and tracking baselines of this service, which start the element set this one extends | 1, 2, 3, 12, 13, 16 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2720 to -5; ASM-4518 to -6 | 1, 3, 8, 11, 12, 13, 14, 15, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The subrogation behaviour, the claim writes, the case moves and the screen behaviour: RWB-S3-E4016-APP.
- The claim preparation, submission and tracking baselines of this service, and their element sets: the sibling CON stories.
- The close of the guarantee, the residual return and the case close, R-GUA-25 and R-GUA-26: FEAT-GUA-07.
- The posting, the ALS and GL entries, the `proceeds` row and the payment event's own shape: rwb-payment (P8) (GAP-2721).
- Where the position and the guaranteed amount are stored as a field: their data owner (GAP-2720). The source of the share and the INT-29 interface: GAP-2724.
- The case of record, its states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-17: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON. The deployment, the flag, the dashboards, the alerts and the runbook: the operations story of this legacy key.
