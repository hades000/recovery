# RWB-P4-AD012-APP Approve a rule version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | L-P4-G |
| Ready to start | After RWB-P4-AD011-APP |
| Depends on (build) | RWB-P4-AD012-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON, RWB-P4-AD011-APP |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-012 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer, and the access service that runs the approval gate in front of a loaded rule version**, I want **the approval of a loaded version decided on its authority, its seven-item change checklist and its separation of duty, recorded in the decision record before it is acknowledged, and then handed to the rule registry as one call**, so that **only a tested and complete change is approved, nobody approves the version they authored, the audit trail names the approver and the version, and the state of the version stays the registry's to change**.

Inside `rwb-access` this is the approval gate of the legacy story RWB-AD-012:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- **The split, stated plainly.** The registry state change — `LOADED` to `APPROVED` and `IN_FORCE` from the valid-from date, the promotion at 00:01, the SHA-256 checksum, the compile, the overlap and default-row checks, the scenario run and the dry run — is P7 `rwb-decision`'s and is out of scope here, exactly as RWB-P4-AD011-APP wrote it in its own out-of-scope list: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's under ASM-0069. This story is the **approval gate and the approval record** that stand in front of that transition: the authority, the checklist, the separation of duty, the decision record and the one call into the registry.
- **Two operations provided**, and no others: `POST /api/recovery/access/v1/admin/rule-version-approvals` decides the gate for one loaded version and then asks the registry to approve it; `GET /api/recovery/access/v1/admin/rule-version-approvals/{versionId}` answers the gate's reading of a version — its label, its valid-from date, its checklist state, its decision-record reference and the registry's state.
- **Three operations consumed**: the registry's `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve`, which moves the version; the registry's `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions`, which returns the version row with its author reference, its status, its checksum, its test result and its `change_checklist` (DF-REF-295); and this service's own `POST /api/recovery/access/v1/authorise`, which answers the A letter in Rules and parameters.
- **Four eyes**: the version's `author` reference — the center of excellence analyst who loaded it under RWB-P4-AD011-APP — is compared with the approver reference of the caller. The authority is the A letter in Rules and parameters, which TSD P4 v3 T6.1 gives to RW-RISK alone among people, and the author holds C and U there, never A, so the author cannot approve (Temporal and Drools Design slide 15).
- **The seven-item checklist** is the one TSD P4 v3 T6.3 writes: request, impact, test result, approver, load, verify and rollback plan, held in `rule_package_version.change_checklist` (DF-REF-295). The version cannot be approved while an item is missing, and the gate refuses with MSG-P3-022 naming the missing item. The shape of the JSON and the evidence each item must carry are Not specified in the source documents (GAP-0828; ASM-1529).
- **The record comes first.** One decision-record entry of the DP-03 library is written, with its outbox row on the shared topic `rwb.decision-record.v1`, before the registry is called and before the approval is acknowledged, so no approval and no refusal exists without a record (R-UNI-39). A forced record failure stops the action with MSG-P7-003, which is what legacy test case TC-AD-012-04 tests.
- **No event on `rwb.access.events.v1`.** This story changes no access policy and no delegation limit, so `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` are not its events; the only payload it emits is the decision record of DP-03.
- **Effective dating.** The approval is followed by the registry's promotion on the valid-from date; a case decided under the previous version keeps the version it was decided under (R-UNI-38, legacy AC2). This service reports that statement on the answer and changes no date.
- The registry's approval contract is not in this story's dependency list, so the call is built against that contract and its fake and the missing C dependency is raised at D1 — Not specified in the source documents (GAP-0826; ASM-1527).
- The API Specification v4 declares no `rwb-access` path for this gate: the two paths above are this story's proposal and are reconciled at contract review — Not specified in the source documents (GAP-0827; ASM-1528).

### 2. Business rationale

A rule change must not need a software release, and it must not become possible for the person who wrote the change to be the person who lets it decide cases. The FSD states the target as a measure: rule and limit changes made without a code release, 100 percent, read from the decision log and the Workbench records every month (FSD P4 v3 A2.17.1 and A2.18.1). The legacy story served that measure inside the monolith, where the rule version, the approval and the screen were rows and a right in one module. In the target the registry is central in `rwb-decision` (Architecture v5 slide 27, which keeps governance central and evaluation local), and the authority to change anything is `rwb-access`'s data (Architecture v5 slide 41: Recovery roles as data, scope, masking policy, DoA table, access log). The approval therefore has two halves that must not be folded back together: the gate, which is a governance act of the access service, and the transition, which is the registry's own state change.

Splitting them is also what makes the gate enforceable. TSD P4 v3 T6.1 refines the three rights columns with a rule-package row of their own: RW-COE holds C and U and may upload, list, dry-run and roll back; RW-RISK holds A and approves; RW-AUDIT holds R; RW-REFADM prepares the change checklist and the load file and holds no upload, no approval and no rollback. Those letters live in `role` and `permission` in `rwb_access`, so the gate can answer "may this caller approve this version" from its own schema in one read, before the registry is asked anything. TSD P4 v3 T6.3 then names the artefact that must exist before the approval: the seven-item change checklist, the checksum, the author and the approver, and the decision-log linkage. The checklist and the separation of duty are the two checks that stop an untested or unexplained change; both are checked here, in front of the registry.

This story meets REQ-CWC-013 on the approval side: a rule change goes from a validated load to production with a version stamp and no code release, and the version stamp is on the record that this gate writes. It meets REQ-DRI-010, because the checklist catalogue and the capability-area letters are versioned rows and not code. It meets REQ-ACA-013, because the administration screens carry the rights that decide who may approve and who may only read. It applies R-UNI-38 — a new rule version applies to decisions taken from its effective date, and open cases keep the version they were decided under — and R-UNI-39, because the gate writes its record in the same local transaction as its answer and never lets an approval proceed unrecorded. Legacy AC2 is R-UNI-38 at this edge: the gate never decides which version a decided case keeps; it states the rule on the answer and the registry and the deciding services enforce it.

The gate also protects the other eighteen services. A rule version in force reaches every service that evaluates it, and the registry holds the model; the one place where a person with the area right and a complete checklist can stop a change is this gate, and the one place where the approver's name is fixed to the version is the record it writes.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD011-APP (same service, its own story) | A loaded version in state `LOADED`, with its `versionId`, package code, version label, valid-from date, checksum and test result; the outbox and idempotency rows of `rwb_access`; the SCR-39 load list. This story approves that version and creates none |
| RWB-P4-AD012-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the two console operations, the `RuleVersionApproval` and `ChecklistItem` schemas, the error envelope and the fakes this story builds against |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the approval and refusal entries, their hash chain and their outbox rows |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the checklist catalogue with its version in force, and the scope rules of the read |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-39 Rules and parameters to the browser |
| The `rwb-decision` rule-package contract | The approve operation and the version list read this story consumes, with their fake. It is not in this story's dependency list, which is the missing dependency of GAP-0826 and ASM-1527 |
| The `rwb-access` permission data | The `role` and `permission` rows and their matrix version, created and loaded by the service's own access stories; this story reads them and writes none |

Business preconditions carried from RWB-AD-012 and the P4 specifications:

- A version is loaded and waiting: its load, its checks and its scenario run are RWB-P4-AD011-APP's and the registry's, and the state it arrives in is `LOADED` (TSD P4 v3 T4).
- The version states are the values of LOV-VERSION-STATUS: LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED (TSD P4 v3 T3.2).
- The author of a version is RW-COE and the approver is RW-RISK; the author cannot approve (Temporal and Drools Design slide 15; TSD P4 v3 T6.1).
- The checklist is the seven items of TSD P4 v3 T6.3, and an item missing refuses the approval with MSG-P3-022. The message text is Not specified in the source documents (GAP-0829; ASM-1530).
- The checklist catalogue — the seven item codes with their labels and their required flag — is read as a versioned parameter row through DP-06, with the version in force (FSD P4 v3 A2.18.3.1 BR-P4-018). Its parameter key is Not specified in the source documents (GAP-0828; ASM-1529).
- The version is in force from its valid-from date by the registry's promotion at 00:01, and a case decided under the previous version keeps that version (R-UNI-38).
- The administration screen is SCR-39 Rules and parameters, reached through the gateway-bff composite route; the approval is offered on it by this story, and the state transition behind it stays the registry's.
- The approver's staff reference resolves through the service's own ACE view `v_ace_iam_group` (DP-05), and no personal data is read, held, returned or put in an event by this story.

### 4. Flow

1. The approver opens SCR-39 Rules and parameters through the gateway-bff composite route of DP-19. The route calls this service's `GET /api/recovery/access/v1/admin/rule-version-approvals/{versionId}` and the registry's version list (consumed, one hop each, 2 s) and shows the version label, the valid-from date, the row count, the checksum, the test result and the seven checklist items with their state.
2. The approver picks the version waiting in `LOADED` and calls `POST /api/recovery/access/v1/admin/rule-version-approvals` with the version id, an `Idempotency-Key` header and no body.
3. `RuleVersionApprovalController` validates the call: the version id must be present and must be a version the registry read returns; an empty one is 422 with MSG-GEN-001 naming the field. The `Idempotency-Key` is required on every POST, and a key already answered replays that first answer and writes no second record entry (BR10).
4. `PermissionReader` resolves the caller's staff reference and reads the caller's `role` and `permission` rows in `rwb_access` for the capability area RULES_AND_PARAMETERS. A caller with no role row at all is refused 403 with MSG-P4-001 and no entry is written, because there is no area to record against. A caller without the A letter is refused 403 with MSG-P4-002 and one refusal entry is written, and nothing is approved (BR1, BR2).
5. Where a break-glass grant is active for the caller, the answer carries the warning MSG-P4-004 with the grant reference, and the grant id is recorded with the entry (BR12).
6. `RuleVersionReader` reads the version through the registry's version list with the version in force: `versionId`, package code, version label, status, valid-from date, author reference, checksum, test result and `change_checklist`. An unknown version is 404 and nothing is written (BR3).
7. The state check: a version that is not in `LOADED` is refused 409 with MSG-GEN-004, because two approvers, an approval and a rollback or a promotion at 00:01 may have raced, and the approver is told to reload. Nothing is approved and no entry is written (BR4).
8. `FourEyesRule` compares the version's `author` reference with the approver reference. Where they are the same person, the call is refused 409 with MSG-P7-002 and one refusal entry carrying both references is written; nothing is approved and the registry is not called (BR5, AC3).
9. `ChecklistGate` reads the seven items of the checklist — request, impact, test result, approver, load, verify and rollback plan — from `change_checklist` against the checklist catalogue read in step 10. Where an item is missing or empty, the call is refused 409 with MSG-P3-022 naming the missing item, one refusal entry is written, and the registry is not called (BR6, AC4).
10. `ParameterReader` reads the checklist catalogue — the seven item codes with their labels and required flag — through the parameters contract of DP-06 with the version in force on the approval date. No item code, label or flag is a constant, and the parameter key is Not specified in the source documents (GAP-0828; ASM-1529).
11. On pass, `DecisionRecordWriter` appends one decision-record entry of the DP-03 library with the approval decision code, the package code, the version label, the status change `LOADED` to `APPROVED`, the valid-from date, the approver reference and, where one is active, the grant id, with its outbox row and in the same local transaction that stores the answer under the `Idempotency-Key`. The entry carries no name, no e-mail address and no personal field. Where the record cannot be written, the call stops with 503 and MSG-P7-003, the registry is never called and nothing is approved, so no version is approved unlogged (R-UNI-39, AC5).
12. `RulePackageApprovalClient` then calls the registry's `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve`, once, one hop, with a 2 s timeout and a breaker, forwarding the `Idempotency-Key`. The registry re-checks the state, the checklist and the separation of duty in its own transaction and moves the version `LOADED` to `APPROVED`.
13. The registry answers the moved version. This story answers 200 with `versionId`, `packageCode`, `versionLabel`, `validFrom`, `checklistState` (the seven items, each present), `decisionRecordReference`, `decisionRecordState`, the registry's `state`, `approverReference` and `approvedAt`, together with the effective-dating statement that a case decided under the previous version keeps the version it was decided under (BR8, BR9, AC1, AC7).
14. Where the registry does not answer inside the 2 s budget, or answers 503, this story answers 503 and reports that nothing was approved. The record entry stays with outcome `REQUESTED`, so a retry under the same `Idempotency-Key` resumes the call instead of writing a second entry (BR11).
15. `GET /api/recovery/access/v1/admin/rule-version-approvals/{versionId}` answers the same field set for a version: the label, the valid-from date, the checklist state read against the catalogue, the reference and state of the local entry, and the registry's status. The read is a pass-through of the registry's version with the gate's own record reference added, and this service holds no copy of the version (BR3).
16. Nothing in this flow writes a rule table, moves a version state, or edits a checklist: the registry owns the version and the transition, and the author and the change owner prepare the checklist under RWB-P4-AD011-APP and the registry's own screens.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The version id is empty, or the `Idempotency-Key` is missing | 422, the registry is not read and no entry is written | MSG-GEN-001 | AC7 |
| X2 | The caller holds no A letter in Rules and parameters | 403, nothing approved, one refusal entry with the version, the package and the area | MSG-P4-002 | AC6 |
| X3 | The caller holds no role row at all in `rwb_access` | 403 and no entry, because there is no area to record against | MSG-P4-001 | AC6 |
| X4 | The approver is the version's author | 409, nothing approved, one refusal entry carrying both references, the registry not called | MSG-P7-002 | AC3 |
| X5 | An item of the seven-item checklist is missing or empty | 409 naming the missing item, nothing approved, one refusal entry, the registry not called | MSG-P3-022 | AC4 |
| X6 | The version is not in `LOADED` (already approved, in force, superseded, rolled back or refused) | 409, nothing approved, no entry written; the approver reloads SCR-39 | MSG-GEN-004 | AC7 |
| X7 | The decision-record entry cannot be written | 503, the registry is never called, so no version is approved without its record | MSG-P7-003 | AC5 |
| X8 | The registry does not answer inside 2 s, or the connection fails | 503 and nothing reported as approved; the entry keeps outcome `REQUESTED` and a retry resumes | None | AC1, AC7 |
| X9 | The same `Idempotency-Key` arrives twice | The second call answers the stored first answer and writes no second entry; the registry is called once | None | AC7 |
| X10 | A break-glass grant is active for the caller | The approval proceeds and the answer carries the warning and the grant reference, and the grant id is on the entry | MSG-P4-004 | AC1 |
| X11 | The version id is unknown to the registry | 404, nothing written | None | AC7 |

No exception path of this story writes a rule row, a version row or a checklist item. The only writes are the decision-record entry, its outbox row and the stored answer, and the only state change is the registry's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-AD012-CON and its fakes, the service's own authorise operation and the registry contract it consumes through its fake; the load is RWB-P4-AD011-APP's and the version is the registry's |
| Negotiable | The checklist catalogue, the capability area and the decision codes are versioned rows and list values; the operations, the two refusals and the record-before-answer rule are fixed |
| Valuable | One gate that refuses a self-approval and an incomplete checklist before the registry is called, and one record that names the approver and the version |
| Estimable | Two operations, one authority read, one checklist gate, one four-eyes rule, one record appender, one registry client, one parameters reader and an idempotency lookup |
| Small | Fits two weeks with its tests; it creates no table, starts no workflow and publishes no access event |
| Testable | Each owned criterion has a test case in section 16, and the registry transition and the record failure are stubbed in the fakes |

### 7. Acceptance criteria

```gherkin
Feature: Approve a rule version

  Background:
    Given the environment is SIT
    Given the run date is 15 December 2026
    Given the permission matrix version in force gives Rules and parameters A to RW-RISK only
    Given the version states are the values of LOV-VERSION-STATUS
    Given the checklist catalogue holds the seven items request, impact, test result, approver, load, verify and rollback plan, all required
    Given test user "U-7101" holds RW-COE with the C and U letters in Rules and parameters
    Given test user "U-7103" holds RW-RISK with the A letter in Rules and parameters
    Given test user "U-7110" holds RW-CASEOWN with the R letter only in Rules and parameters
    Given test user "U-7112" holds RW-REFADM with the R letter only in Rules and parameters
    Given test user "U-7114" holds RW-AUDIT with the R letter only in Rules and parameters

  Scenario: AC1 Approve (legacy RWB-AD-012 AC1)
    Given the rwb-decision contract mock returns version "ENTRY-2027.01" in state "APPROVED" with validFrom 2027-01-01, all seven checklist items present and the SIT test result "PASS"
    Given a version with every test passed
    When I approve it
    Then it applies to decisions from its valid from date

  Scenario: AC2 Open cases keep their version (legacy RWB-AD-012 AC2)
    Given a case decided under the previous version
    When the new version takes effect
    Then the decided case keeps the version it was decided under (R-UNI-38)

  Scenario: AC3 The author of a version cannot approve it (new, D-RCV-60)
    Given "U-7101" loaded version "ENTRY-2027.01" of package "ENTRY" and is recorded as its author
    When "U-7101" calls POST /api/recovery/access/v1/admin/rule-version-approvals for "ENTRY-2027.01" with Idempotency-Key "k-012-1"
    Then the response is 409 with message MSG-P7-002 and nothing is approved
    Then one decision-record entry is written carrying the version label, the status change "LOADED to APPROVED" refused, the author reference and the approver reference
    Then the rwb-decision approval fake records no call and the version stays "LOADED"

  Scenario: AC4 An incomplete change checklist refuses the approval and names the missing item (new, D-RCV-60)
    Given version "ENTRY-2027.02" is in "LOADED" with six of the seven checklist items present and no rollback plan
    When "U-7103" calls POST /api/recovery/access/v1/admin/rule-version-approvals for "ENTRY-2027.02" with Idempotency-Key "k-012-2"
    Then the response is 409 with message MSG-P3-022, and its detail names "rollback plan"
    Then the rwb-decision approval fake records no call and the version stays "LOADED"
    Then the record entry of the refusal carries the checklist state with the missing item named

  Scenario: AC5 A failed decision-record write stops the approval before the registry is called (new, D-RCV-60)
    Given version "ENTRY-2027.01" is in "LOADED" with all seven checklist items present and author "U-7101"
    Given the decision-record library is forced to fail its append
    When "U-7103" calls POST /api/recovery/access/v1/admin/rule-version-approvals for "ENTRY-2027.01" with Idempotency-Key "k-012-3"
    Then the response is 503 with message MSG-P7-003 and nothing is approved
    Then the rwb-decision approval fake records no call and the version stays "LOADED"

  Scenario: AC6 An approver without the A letter is refused and the refusal is recorded (new, D-RCV-60)
    Given "U-7110" and "U-7112" hold the R letter only in Rules and parameters
    When "U-7110" calls POST /api/recovery/access/v1/admin/rule-version-approvals for "ENTRY-2027.01" with Idempotency-Key "k-012-4"
    Then the response is 403 with message MSG-P4-002 and nothing is approved
    Then one decision-record entry is written with the version, the package and the capability area, and no personal data
    Then a caller with no role row is refused 403 with message MSG-P4-001 and no entry is written

  Scenario: AC7 The approval answer carries the version, the checklist state and the record, and one key answers once (new, D-RCV-60)
    Given version "ENTRY-2027.01" is in "LOADED", valid from 2027-01-01, with all seven checklist items present and author "U-7101"
    Given the rwb-decision contract mock returns the same version in state "APPROVED" with approvedAt 2026-12-15 and the approver reference "U-7103"
    When "U-7103" calls POST /api/recovery/access/v1/admin/rule-version-approvals with Idempotency-Key "k-012-5"
    Then the response is 200 with versionLabel "ENTRY-2027.01", validFrom 2027-01-01, checklistState of seven present items, decisionRecordReference, decisionRecordState and state "APPROVED"
    Then the answer states that a case decided under the previous version keeps that version
    Then the same call repeated with Idempotency-Key "k-012-5" replays the first answer, writes no second record entry and the rwb-decision fake records one call
    Then GET /api/recovery/access/v1/admin/rule-version-approvals/{versionId} answers the same fields with the entry reference and the registry's state
    Then a version not in "LOADED" is refused 409 with message MSG-GEN-004
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller who holds the A letter in Rules and parameters may approve a rule version; the letter is read from the `role` and `permission` rows of `rwb_access` and never from a role name in code | REQ-ACA-003; TSD P4 v3 T6.1; legacy permission row Rules and parameters A: RW-RISK |
| BR2 | A caller with no A letter is refused with MSG-P4-002 and the refusal is recorded as one refusal entry; a caller with no role row is refused with MSG-P4-001 and nothing is recorded | REQ-ACA-007; FSD P4 v3 A2.17 exception flow AC-EXC-P4-017-01 |
| BR3 | The version, its author reference, its status, its valid-from date and its checklist are read from the registry through its own contract; this service holds no copy of the version | DP-01; ASM-0069 |
| BR4 | A version is approved only while it is in `LOADED`; any other state is 409 with MSG-GEN-004 and nothing changes | TSD P4 v3 T4; LOV-VERSION-STATUS |
| BR5 | The approver must not be the version's author; the comparison is on references, and a refusal is 409 with MSG-P7-002 | Temporal and Drools Design slide 15; TSD P4 v3 T6.1; TSD P4 v3 T6.3; legacy MSG-P7-002 |
| BR6 | The seven items of the change checklist must all be present before the approval; a missing item refuses the approval with MSG-P3-022 naming it | TSD P4 v3 T6.3, DF-REF-295; FSD P4 v3 A2.18 |
| BR7 | The checklist catalogue — the seven item codes, their labels and their required flag — is a versioned parameter row read through DP-06; no item code, label or flag is a constant | FSD P4 v3 A2.18.3.1 BR-P4-018; DP-06; GAP-0828 |
| BR8 | Every approval and every refusal appends exactly one decision-record entry of the DP-03 library with its outbox row on `rwb.decision-record.v1`, and the entry carries the version label, the status change, the approver reference and the time, with no personal data | DP-03; R-UNI-39; TSD P4 v3 T6.3 |
| BR9 | No action proceeds unlogged: where the record cannot be written the call is 503 with MSG-P7-003 and the registry is never asked to move the version | R-UNI-39; FSD P4 v3 A2.18 exception flow AC-EXC-P4-018-02 |
| BR10 | A repeated approval with the same `Idempotency-Key` answers the first answer and writes no second entry, and the registry is called once | Architecture v5 slide 11; DP-09 |
| BR11 | The registry's transition is asked for once, one hop, with a 2 s budget; a timeout answers 503 with nothing approved and leaves the entry at outcome `REQUESTED` so a retry resumes | DP-11; DP-20 one-hop rule; Architecture v5 slide 11 |
| BR12 | The approval is effective from the version's valid-from date by the registry's promotion, and a case decided under the previous version keeps that version; this story states the rule and changes no date | Legacy RWB-AD-012 AC1 and AC2; R-UNI-38; TSD P4 v3 T4 |
| BR13 | Every approved and every refused gate decision records the caller reference and, where a break-glass grant is active, the grant id; the record carries no personal data | Legacy RWB-AD-012 MSG-P4-004; Principle 5 |
| BR14 | This story writes no rule row and no version state: the state change is the registry's, and the decision code of the record is a list value whose value is Not specified in the source documents (GAP-0830; ASM-1531) | ASM-0069; ASM-0040 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of two rows of the service's own schema; RULES_AND_PARAMETERS is a value of LOV-CAPABILITY, so a renamed area is a row and not a build.
- BR2 is the record appender called on the refusal path, so the audit sees a refused attempt as plainly as an approval; the no-role case records nothing because there is no area to record against.
- BR3 is the pass-through of the registry read: the version, its author, its state and its checklist are the registry's fields, and this service keeps no copy that could drift from them.
- BR4 is the state the registry read returned; the registry re-checks it inside its own transaction, so a race answers the registry's own refusal rather than a silent second approval.
- BR5 is one comparison of two references, made before the registry is called, so a self-approval never reaches the version and never leaves an approver on it.
- BR6 and BR7 are the checklist gate over the registry's `change_checklist` and the catalogue read through DP-06; the item codes are TSD P4 v3 T6.3's list, and their labels and required flags are rows.
- BR8 and BR9 are the record appender of DP-03 inside the local transaction that stores the answer, before the registry call; the registry's transaction is its own and is not held open by this service.
- BR10 is the idempotency table of the platform library in `rwb_access`, written with the answer, so a double click, a retry or a gateway repeat cannot approve twice or write two entries.
- BR11 is the one-hop client with its 2 s budget and its breaker; a timeout is a 503 that says nothing was approved, never a silent success.
- BR12 is a statement on the answer and not an action: this service publishes no version state and knows no case.
- BR13 is the caller reference in the entry and the grant id where MSG-P4-004 is returned; no name and no e-mail address is held anywhere.
- BR14 is a deliberate absence: the service has no write method for `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case`, so a gate decision cannot move a version by itself.

### 9. State transitions

This service holds no version state of its own. It holds the gate's outcome and the record of it; the version lifecycle is the registry's and is the one TSD P4 v3 T4 defines.

| From | Event | Condition | To |
|---|---|---|---|
| `LOADED` | Approve, approver holds A, is not the author and the checklist is complete | The record is written, then the registry accepts the approval | `APPROVED`, then `IN_FORCE` on the valid-from date by the promotion at 00:01 |
| `LOADED` | Approve, approver is the author | None | `LOADED`, refused 409 with MSG-P7-002, one refusal entry, the registry not called |
| `LOADED` | Approve, an item of the checklist is missing | None | `LOADED`, refused 409 with MSG-P3-022 naming the item, one refusal entry, the registry not called |
| `LOADED` | Approve, the caller holds no A letter | None | `LOADED`, refused 403 with MSG-P4-002, one refusal entry, the registry not called |
| `LOADED` | Approve, the record cannot be written | None | `LOADED`, 503 with MSG-P7-003, the registry not called |
| `LOADED` | Approve, the registry does not answer | None | `LOADED`, 503, the entry keeps outcome `REQUESTED` |
| `APPROVED` | The valid-from date arrives | The registry's promotion at 00:01 | `IN_FORCE` |
| `IN_FORCE` | The next version is promoted | None | `SUPERSEDED`, readable for its own dates |
| `IN_FORCE` | A rollback | The rollback is RWB-P4-AD013-APP's and the registry's | `ROLLED_BACK` |

| Command | Condition | Outcome |
|---|---|---|
| Approve | A letter in Rules and parameters, not the author, checklist complete, `LOADED`, record written, registry accepts | 200 with the version fields, the checklist state, the record reference and state `APPROVED` |
| Approve | No A letter | 403 with MSG-P4-002, one refusal entry, no registry call |
| Approve | Approver is the author | 409 with MSG-P7-002, one refusal entry, no registry call |
| Approve | A checklist item is missing | 409 with MSG-P3-022 naming it, one refusal entry, no registry call |
| Approve | The version is not `LOADED` | 409 with MSG-GEN-004, no entry, no registry call |
| Approve | The record cannot be written | 503 with MSG-P7-003, no registry call |
| Read | Rules and parameters R | 200 with the version, its checklist state and the local entry reference |

The registry owns the lifecycle of a version (TSD P4 v3 T4); this story observes two of its states and changes none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RISK Risk and model risk officer | Holds Rules and parameters A and approves a loaded version. TSD P4 v3 T6.1 gives the A letter in the rule-package column to this role alone among people |
| RW-COE Center of excellence analyst | Holds Rules and parameters C and U: uploads, lists, dry-runs and rolls a version back under RWB-P4-AD011-APP and RWB-P4-AD013-APP, and therefore may not approve. When the caller is also the version's author the refusal is MSG-P7-002 whatever the letters say |
| RW-AUDIT Internal audit | Holds Rules and parameters R and reads the versions, the checklist state, the test result and the record; it calls the approve operation of this story and is refused with MSG-P4-002 |
| RW-REFADM Reference data administrator | Prepares the change checklist and the load file and holds no upload, no approval and no rollback; an approve call is refused with MSG-P4-002 |
| RW-PLATADM, RW-SECADM | Hold Rules and parameters R only in TSD P4 v3 T6.1; they read a version and approve none |
| The `rwb-decision` service identity | Answers the approve operation and the version list; it calls nothing of this story |
| `rwb-access` itself | Reads `role`, `permission` and its own `v_ace_iam_group` view, and writes only its decision-record entry, its outbox row and the stored answer |

The refusal shape is an RFC 9457 problem response with `messageId` set: MSG-P4-002 for an absent letter, MSG-P4-001 for an absent role, MSG-P7-002 for a self-approval, MSG-P3-022 for an incomplete checklist, MSG-GEN-004 for a version that is no longer `LOADED`, and MSG-P7-003 for a record that cannot be written. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-AD012-CON together with the rest of this gate's contract.

### 11. Data

| BR Field ID | Table | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` in `rwb_access` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` in `rwb_access` | id, role_id, capability_area, letters, matrix_version | Read |
| (ACE view) | `v_ace_iam_group` (ACE `iam_group`) | the entra_group of the calling staff reference | Read through the service's own ACE view (DP-05) |
| DF-REF-274 to DF-REF-278 | `rule_package` of `rwb_decision` | package code, title, owner role, hit policy | Returned in the registry's answer; not read from the schema |
| DF-REF-279 to DF-REF-295 | `rule_package_version` of `rwb_decision` | version id, version label, status, checksum, valid-from, author, approver, loaded and approved times, test result, dry-run counts and `change_checklist` | Returned through the contract; handed back by the approve call |
| DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054, DF-REF-296 to DF-REF-298 | `rule_row` of `rwb_decision` | none in this story | None: no rule row is read or written here |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the approval and the refusal entry of a gate decision | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and its `DecisionRecorded` message | Write |
| (idempotency) | `idempotency_key` in `rwb_access` | the stored answer of each approve call | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No rule table exists in `rwb_access` and none is created: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s under ASM-0069, and their fields arrive in the contract, not by a schema read (DP-01). No row of `decision_log_entry` is read or written either: the local entry goes on `rwb.decision-record.v1` and the central ledger is `rwb-decision`'s. The checklist is the registry's `change_checklist` column, read through the contract and never copied here; the gate reports its state and refuses it, and it edits none of it. `lov_value` is reference data of P3 under the ownership ruling and is read through DP-07 by the services that hold lists, not from `rwb_access`. Field IDs are those of the Logical Data Model and Data Dictionary v8.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1` (DP-13). Owner P4 `rwb-access`.

| Method | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/admin/rule-version-approvals` | Path or query `versionId`; no body | `RuleVersionApproval`: `versionId`, `packageCode`, `versionLabel`, `validFrom`, `checklistState`, `decisionRecordReference`, `decisionRecordState`, `state`, `approverReference`, `approvedAt`, and the effective-dating statement | 401 MSG-P4-001; 403 MSG-P4-002; 404 unknown version; 409 MSG-P7-002, MSG-P3-022 or MSG-GEN-004; 422 MSG-GEN-001; 503 MSG-P7-003 or registry unavailable | Rules and parameters A, scope applied | `Idempotency-Key` required; a repeat replays the stored answer |
| GET | `/admin/rule-version-approvals/{versionId}` | None | `RuleVersionApproval` with the checklist state, the local entry reference and the registry's status | 401 MSG-P4-001; 403 MSG-P4-002; 404 unknown version; 503 registry unavailable | Rules and parameters R, scope applied | Not applicable, read only |

The legacy story names the approval as one path under the single monolith base that DP-13 replaces, with the right Rules and parameters A; TSD P4 v3 appendix T-A carries it as API-P4-017 `POST /admin/rule-package-versions/{versionId}/approve`, and the ownership map rules that path P7 `rwb-decision`'s under ASM-0040, because the version is the registry's row. This story therefore keeps the gate under its own base and calls the registry's operation as a consumer, and the two provided paths above are its proposal: the API Specification v4 declares no `rwb-access` path for this gate, which is Not specified in the source documents (GAP-0827; ASM-1528). The contract review freezes the two paths and their field names before either is built against.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | P7 `rwb-decision` | Moves the version `LOADED` to `APPROVED` after its own re-checks, and answers the moved version. It is the operation named API-P4-017, owned P7 under ASM-0040 |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 `rwb-decision` | The version row with its status, checksum, author, approver, test result and `change_checklist`, for the gate and for the read |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (this service) | The Rules and parameters A or R check behind both operations, under the guard library of DP-08 |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The checklist catalogue with its version in force (DP-06) |

None of the four is declared as provided by this story except the authorise operation, which is this service's own. The two `rwb-decision` operations are the registry half and are consumed with their fake; their contract is not in this story's dependency list, which is the missing dependency of GAP-0826 and ASM-1527.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of an approval or a refusal: the decision code, the package, the version label, the status change, the valid-from date, the approver reference, the grant id where one is active, and the outcome |

Nothing is published on `rwb.access.events.v1`. This story changes no access policy and no delegation limit, so `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` are not its events; the version's own state is the registry's and travels on the registry's topic.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, whose event list is none, and this story adds no subscription. The promotion at 00:01 and the `RulePackageInForce` event of the registry are not this service's to consume.

#### 12.5 Workflows and activities

None. The approval is one synchronous command with one downstream call; there is no long-running wait, no timer and no activity on the `rwb-access` queue.

#### 12.6 Schedules

None. A load and an approval are request-driven, and the only Schedule in the version lifecycle is the registry's promotion at 00:01.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the caller's role and its class |
| `permission` | P4 (`rwb_access`) | Read only: the A or R letter of the caller's role in Rules and parameters |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_access` | The outbox row of the record and the stored answer of each call; no inbox row is written because no event is consumed (DP-09) |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written: the version, its checklist and its states are the registry's (ASM-0069) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the local entry goes on `rwb.decision-record.v1` and the central ledger is the registry's |
| `case`, `task` | P3 (`rwb_case`) | Not read: this story knows no case |

No table of another service is read and no foreign key crosses a schema (DP-01). The ACE data this story touches is its own `v_ace_iam_group` view (DP-05), which carries group names and no personal field.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision rule-package WireMock | the P7 rule-package contract (GAP-0826; ASM-1527) | `POST /admin/rule-package-versions/{versionId}/approve` answering version "ENTRY-2027.01" in state `APPROVED` with approvedAt 2026-12-15 and approver reference "U-7103"; a version in `LOADED` with author "U-7101" and all seven checklist items; a version in `LOADED` with six items and no rollback plan; a version in `IN_FORCE` for the conflict of X6; a 404; and a 503 and a timeout for X8; `GET /admin/rule-packages/{packageCode}/versions` answering the same versions with their status, author, checksum, test result and `change_checklist` |
| parameters fake | RWB-P3-E1042-CON | `GET /api/recovery/case/v1/admin/parameters` answering the checklist catalogue of seven items, all required, with the version in force on 15 December 2026, and the scope rules |
| decision-record fake | RWB-PLT-E1027-CON | The append of the approval and refusal entries, the hash-chain check, the outbox row and the forced failure of X7 |
| authorise and guard fake | RWB-P4-AD012-CON, RWB-P4-E1037-CON | A granted answer for RW-RISK with A in Rules and parameters, a refused answer with MSG-P4-002 for RW-COE, RW-CASEOWN, RW-REFADM and RW-AUDIT, and a no-role answer with MSG-P4-001 |
| gateway-bff composite route fake | RWB-PLT-N001-CON | The SCR-39 route that calls the read and the approve and merges the version fields with the checklist state and the record reference |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2; consumed 4 | Two console operations on `/api/recovery/access/v1`; two registry operations, this service's own authorise operation and the `rwb-case` parameters read; one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.DecisionRecorded.v1` through the DP-03 library; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | No workflow and no timer in the gate; the 00:01 promotion is the registry's |
| File | None | The workbook is RWB-P4-AD011-APP's and the registry's; this story reads no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/ruleversionapproval`, Java package `th.co.scb.ace.workbench.recovery.access.ruleversionapproval`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process approval method of the monolith's rule module (DP-11: one REST contract with a mock, one hop and a 2 s timeout), the write of the approver and the approved time straight into the version row (DP-03: the local decision record, with the version row left to the registry), the read of the monolith permission table (DP-05: the service's own `role` and `permission` rows plus `v_ace_iam_group` for the group mapping), the checklist read from `casewf.config` (DP-06: the parameters contract of `rwb-case` with the version in force), the monolith base (DP-13), and the ace-web screen (DP-19: the SCR-39 composite route). There is no DP-04 in this story's pattern set on purpose: the Drools kit, the compile and the evaluation are the registry's and the model-owning services', and this gate claims none of them.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleVersionApprovalController | Controller | The two operations, the `Idempotency-Key` check, the RFC 9457 error mapping and `messageId` on every refusal |
| RuleVersionApprovalService | Service | The gate: authority, state, separation of duty, checklist, the registry call, the answer and the record |
| PermissionReader | Service | The caller's `role` and `permission` rows in `rwb_access` and the A letter in RULES_AND_PARAMETERS |
| RuleVersionReader | Client | The registry's version list read: status, label, valid-from, author, checksum, test result and `change_checklist`, one hop and 2 s |
| ChecklistGate | Service | The seven items of TSD P4 v3 T6.3 against the catalogue from DP-06, with the missing item named |
| FourEyesRule | Service | The author reference against the approver reference, decided before the registry is called |
| RulePackageApprovalClient | Client | The registry's approve operation, once per gate decision, with the breaker and the resume path |
| DecisionRecordWriter | Service | The approval and refusal entries in the transaction that stores the answer, with the outbox row |
| ParameterReader | Service | The checklist catalogue through the parameters contract of DP-06, with the version in force |
| IdempotencyStore | Service | The stored answer per `Idempotency-Key`, so a repeat answers the first call and writes no second entry |

**Database and migrations**

- This story creates no table of its own. `role` and `permission` are created and loaded by the service's own access stories, and the outbox, inbox and idempotency rows are created in the `rwb_access` baseline by the service's migration in the per-service Flyway sequence of DP-15.
- The only writes are the decision-record row, its outbox row and the `idempotency_key` row, in one local transaction. Nothing writes `rule_package_version`, `rule_package`, `rule_row` or `rule_test_case`.
- No column is added to `rwb_access` for the checklist: the checklist is the registry's `change_checklist` (DF-REF-295) and this service reads it through the contract.

**Configuration and reference data**

- The checklist catalogue — the seven item codes of TSD P4 v3 T6.3 with their labels and required flag — is a parameter row read through DP-06 with the version in force; its key is Not specified in the source documents (GAP-0828; ASM-1529). A new label or a changed flag is a data change with no build.
- RULES_AND_PARAMETERS is a value of LOV-CAPABILITY, and the A and R letters are `permission` rows with a matrix version; no area, letter or role name is a Java constant (BR1, BR7).
- The decision code of the record entry is a list value of the DP-03 library; its value for a rule-version approval is Not specified in the source documents (GAP-0830; ASM-1531).
- The version, its label and its dates belong to the registry; this service stores none of them and keeps none in a cache beyond the request.

**Build steps**

1. `RuleVersionApprovalController` with the two paths, the `Idempotency-Key` requirement and the error envelope; contract test against RWB-P4-AD012-CON.
2. `PermissionReader` and the A letter in RULES_AND_PARAMETERS: the granted answer for RW-RISK, the refusals with MSG-P4-002 for RW-COE, RW-CASEOWN, RW-REFADM and RW-AUDIT, and the no-role answer with MSG-P4-001; tests for AC6 and X3.
3. `RuleVersionReader` over the registry's version list, with the one-hop client and the 2 s budget; tests for the 404 and for a version read in each of `LOADED`, `IN_FORCE`, `SUPERSEDED` and `REFUSED`.
4. `FourEyesRule`: the author refused with MSG-P7-002 and one refusal entry; test for AC3.
5. `ChecklistGate` and `ParameterReader`: the complete checklist passes, the missing rollback plan refuses with MSG-P3-022 naming it, and a changed catalogue changes the outcome with no build; test for AC4.
6. The state check and its 409 with MSG-GEN-004 for a version that is no longer `LOADED`.
7. `DecisionRecordWriter` and `IdempotencyStore`: one entry per gate decision, the stored answer, the forced failure of X7 and the repeated key of X9; tests for AC5 and AC7.
8. `RulePackageApprovalClient` and the resume path: a timeout answers 503 with nothing approved, and the retry under the same key resumes without a second entry.
9. The read operation against the same fake, with the entry reference and each registry state.
10. The SCR-39 composite route against the gateway-bff fake, with the states waiting, checklist incomplete, approved, refused and record failed.

**Feature switch.** The gate is not behind a flag: an approval that could skip the authority, the separation of duty or the checklist would be the defect this story exists to close. The service-level feature flag of the service baseline governs the administration surface, and this story adds no flag of its own.

**Done when.** The tests in section 16 pass; a version with every test passed and a complete checklist is approved by RW-RISK and answers the version label, the valid-from date, the checklist state and the record reference; the author is refused with MSG-P7-002, a role without the A letter with MSG-P4-002 and an incomplete checklist with MSG-P3-022 naming the missing item, each with one record entry and no registry call; a version not in `LOADED` is refused with MSG-GEN-004; a repeated key answers once; and a forced record failure stops the action with MSG-P7-003 before the registry is called.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller holds no Recovery Workbench role row | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no A letter in Rules and parameters | You cannot {action} here. Your role does not include it. | This story, on the approve operation, from the authorise answer |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the answer, with the grant id recorded |
| MSG-GEN-001 | The version id is empty or the `Idempotency-Key` is missing | Enter {field}. | This story, on the approve operation |
| MSG-GEN-004 | The version is not in `LOADED` when the call arrives | Someone else changed this record. Reload it to see their change. | This story, from the registry's status |
| MSG-P3-022 | An item of the seven-item change checklist is missing or empty | Not specified in the source documents (GAP-0829; ASM-1530) | This story, from the checklist gate; the detail names the missing item |
| MSG-P7-002 | The approver is the version's author | You prepared this decision, so you cannot approve it. | This story, from the separation-of-duty rule |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The checklist refusal also carries the missing item codes, so the screen can name each one without a second call.

MSG-P7-002 is a message of the decision centre's catalogue, where the same separation-of-duty rule refuses an approver who prepared the decision; the sources use that id for the author-cannot-approve rule in the rule-package column (TSD P4 v3 T6.3) and in the registry's own approval description, so this gate reuses it rather than renumbering it. MSG-P3-022 is the checklist message of the P3 catalogue, cited by TSD P4 v3 T6.3 for exactly this refusal; only its id is given in the sources, so the text stays with the catalogue owner and is carried here as the placeholder (GAP-0829; ASM-1530).

### 15. Screens and states

One screen, SCR-39 Rules and parameters, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON). The route calls this service's read and approve and the registry's version operations, one hop each, and merges the answers; the browser calls no service directly and holds no right of its own.

| Screen | State | What the screen shows |
|---|---|---|
| SCR-39 Rules and parameters | Empty | No version is listed for the package yet: an empty list with a total of 0 and no error |
| SCR-39 Rules and parameters | Loaded, waiting for approval | State `LOADED` with the version label, the valid-from date, the row count, the checksum and the test result, and the seven checklist items with their state |
| SCR-39 Rules and parameters | Checklist incomplete | The version with the missing item named: the approval control is offered and the refusal MSG-P3-022 is shown with the item when it is tried, or the screen marks the item before the try |
| SCR-39 Rules and parameters | Approved | State `APPROVED` with the approver reference, the approved time, the decision-record reference and the statement that the version applies from its valid-from date, and that a case decided under the previous version keeps that version |
| SCR-39 Rules and parameters | Refused | MSG-P7-002 for the author, MSG-P4-002 for a role without the letter, MSG-P3-022 with its item, or MSG-GEN-004 for a version that moved: nothing changed and the record reference is shown |
| SCR-39 Rules and parameters | Record failed | MSG-P7-003 with the statement that nothing was approved and the registry was not asked; the version stays `LOADED` |

The legacy story also lists SCR-47 Personal data with the states Loading and list. That screen is not this slice: it belongs to the masking capability of `rwb-access`, and this story serves no field of it and reads no personal data. The approval is offered on SCR-39 by this story; the transition behind it is the registry's, so the screen shows the state the registry returns and never a state this service set. The gateway-bff composite route specification, the screen field list and the masking of any field are the platform story's (RWB-PLT-N001-CON); this story fixes the two operations the route calls.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-012-01 | AC1, BR1, BR5, BR8, BR12 | Contract | Version "ENTRY-2027.01" in `LOADED` with author "U-7101" and all seven checklist items; approved by "U-7103" holding RW-RISK with A; the registry fake answers `APPROVED` with validFrom 2027-01-01 and approvedAt 2026-12-15; one approval entry is written before the answer |
| TC-AD-012-02 | AC2, BR12 | Component | A case decided under "ENTRY-2026.12" while "ENTRY-2027.01" is promoted on its valid-from date: the answer states that the decided case keeps its version, and no date and no case record is touched |
| TC-AD-012-03 | AC6, BR1, BR2 | Component | "U-7110" with RW-CASEOWN and R only, and "U-7112" with RW-REFADM and R only, each refused 403 with MSG-P4-002 and one refusal entry; a caller with no role row refused 403 with MSG-P4-001 and no entry |
| TC-AD-012-04 | AC5, BR9 | NFR | The decision-record append forced to fail during an approval with a complete checklist; 503 with MSG-P7-003, the registry fake records no call, the version stays `LOADED` and no answer is stored |
| TC-AD-012-05 | AC4, BR6, BR7 | Component | Version "ENTRY-2027.02" in `LOADED` with six items and no rollback plan; 409 with MSG-P3-022 naming "rollback plan", one refusal entry with the checklist state, and no registry call; a changed catalogue row changes the outcome with no build |
| TC-AD-012-06 | AC3, AC7, BR5, BR10, BR11 | Component | "U-7101" approving the version it authored: 409 with MSG-P7-002 and no registry call; the happy path answering the version label, validFrom, the seven present items, the record reference and `APPROVED`; the same key twice answering once and the registry fake recording one call; a version in `IN_FORCE` refused 409 with MSG-GEN-004 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Contract and the Access level to Component, as the rows show. TC-AD-012-01 and TC-AD-012-02 keep their legacy coverage, TC-AD-012-03 the access refusal and TC-AD-012-04 the forced record failure that the legacy key carries as its Principle 5 case. No ITG story is split from this legacy key, so no `-ITG` copy of a test case is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the checklist catalogue, the capability area, the letters and the decision code are parameter rows, reference values and list values, read with the version in force (BR1, BR7). A test proves that a new label, a changed flag or a new area needs no build.
- No personal data anywhere: the version label, the package code, the dates, the checklist items and the approver reference are the whole payload; the record entry, the outbox message and every log line carry no name, no e-mail address and no personal field, and the staff reference resolves through `v_ace_iam_group` only for the authority check (DP-05).
- No read of another service's tables (DP-01): `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s and are read through its contract; `decision_log_entry` is not read at all.
- One writer per fact: the registry writes the version and its state, the author writes the checklist through the load and the registry's screens, and this service writes only its record. A gate decision therefore cannot move a version or edit a checklist by itself (BR14).
- No approval without its record: the entry commits before the registry is called, and a failed write answers MSG-P7-003 with nothing approved and the registry never asked (BR9).
- No approval by the author and none without the letter: both refusals are decided before the registry is called, so a refused attempt costs no registry transaction and leaves one record that an auditor can read (BR2, BR5).
- The gate is idempotent: the stored answer under the `Idempotency-Key` means a double click, a retry or a gateway repeat cannot approve twice or write two entries (BR10).
- A refusal tells the caller what it may know and nothing more: no other version, no other package and no role name is returned, so a refusal cannot be used to map the rule registry or the permission matrix.
- The screen is served through the gateway-bff route of DP-19 and calls no service directly; the browser holds no token with a Rules and parameters right of its own.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated load to production with a version stamp and no code release, and rolls back by one call | Epic 8; Program 5.4 rules | FEAT-ADM-02 | All recovery processes | BR4, BR6, BR8, BR12 | TC-AD-012-01, TC-AD-012-05 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold and limit, versioned | Epic 8; Program 5.4 rules | FEAT-ADM-02 | All recovery processes | BR7, BR14 | TC-AD-012-05, TC-AD-012-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available, with their rights | Epic 8; Program 5.1 access | FEAT-ADM-01 | All recovery processes | BR1, BR2 | TC-AD-012-03, TC-AD-012-06 |

| Legacy reference | Where it is kept |
|---|---|
| AC1: a version with every test passed applies to decisions from its valid-from date | Sections 1, 2, 4, 7, 8, 9, 12.2 |
| AC2: a case decided under the previous version keeps that version (R-UNI-38) | Sections 1, 2, 4, 7, 8, 15 |
| The rule_package_version fields DF-REF-279 to DF-REF-295, the change checklist among them | Sections 8, 11, 12.1, 12.2 |
| The permission rows Rules and parameters A for RW-RISK and R for the case roles | Sections 8, 10, 12.1, 16 |
| MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 | Section 14 and the exception paths of section 5 |
| MSG-P7-002 for the author who cannot approve, and MSG-P3-022 for the incomplete checklist | Sections 8, 14, 16 |
| Screens SCR-39 and SCR-47 and their states | Sections 15, 19 |
| Test cases TC-AD-012-01 to TC-AD-012-04, with TC-AD-012-05 and TC-AD-012-06 added | Section 16 |
| Rule IDs R-UNI-38 and R-UNI-39 | Sections 2, 8, 9, 14, 17 |
| Field IDs DF-REF-034 to DF-REF-044 and DF-REF-274 to DF-REF-295 | Section 11 |

### 19. Out of scope

- The registry half under `rwb-decision` (P7, ASM-0069): the state change `LOADED` to `APPROVED` and `IN_FORCE`, the promotion at 00:01 with `RulePackageInForce`, the SHA-256 checksum and its verification, the compile and the KieBase, the overlap, unreachable-row and default-row checks, the scenario run, the dry run, the change report and the one-call rollback (RWB-P4-AD013-APP and the registry).
- The workbook load, its row gate and its SIT result: RWB-P4-AD011-APP. This story approves a loaded version and never loads, edits or re-tests one.
- The `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables and their migrations; they are `rwb-decision`'s, and the checklist is its column.
- The authoring of the change checklist: the request, impact and rollback plan are prepared by the change owner and the reference data administrator (TSD P4 v3 T6.1) through the load and the registry's screens. This story reads the checklist and refuses it; it writes none of it.
- The Drools kit and any evaluation of a rule: the model-owning services fetch the version, verify the checksum and swap it in (DP-04), and this story embeds no Drools kit.
- The QA sample against the rule version applied (FSD P4 v3 A2.24) and the change report: they read the versions and the decision log in `rwb-decision` and add no operation here.
- SCR-47 Personal data and the masking capability of `rwb-access`; this story reads and serves no personal field.
- The delegations of authority table and its approval path (RWB-P4-E1038-APP); the parameters read here is the checklist catalogue only.
- The integration harness of the rule-version journey: no ITG story is split from this legacy key, so the `-ITG` copies of the test cases are not written here.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
