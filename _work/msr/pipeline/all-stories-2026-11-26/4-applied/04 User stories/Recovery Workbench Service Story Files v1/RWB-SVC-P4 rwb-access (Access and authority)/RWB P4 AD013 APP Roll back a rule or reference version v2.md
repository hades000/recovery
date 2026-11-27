# RWB-P4-AD013-APP Roll back a rule or reference version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | L-P4-G |
| Ready to start | After RWB-P4-AD012-APP |
| Depends on (build) | RWB-P4-AD013-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P4-AD012-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-013 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator, and the access service that gates every version rollback**, I want **a bad version undone in one action on the administration screen — the previous version restored from an immediate date, by a person other than the one who loaded the bad version, with the withdrawal and the restoration both written to the decision record**, so that **a breach-causing rule or reference value is out of force in minutes without a code release, no single person can undo a change unseen, and the two services that own the tables stay the only writers of them**.

Inside `rwb-access` this is the rollback gate of the legacy story RWB-AD-013:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Service facts of this slice: no topic of its own is published, no workflow is started, no rule table and no reference table is held, and no screen of its own is served — SCR-40 Reference data and SCR-39 Rules and parameters arrive through the gateway-bff composite route of DP-19.
- **The split, stated plainly.** The legacy journey touches two owners. A rule version is restored through `rwb-decision` (P7): `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's under ASM-0069, and the rollback of a package version is `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback` (TSD P4 v3 API-P4-018), P7's under ASM-0040. A reference-data version is restored through `rwb-case` (P3): `reference_row` and `reference_version` are P3's under DP-07, and the rollback of a reference load is `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` (TSD P4 v3 API-P4-010), P3's under ASM-0041. `rwb-access` serves neither table, writes neither version and moves neither state.
- **What this story is**, and all it is: the single rollback gate of SCR-40 Reference data and SCR-39 Rules and parameters, which does four things and nothing else. (a) It validates the request: the target kind, either a rule version or a reference-data version; the identifier of the version in force; the identifier of the previous version to restore; and the effective date, which is read as today, because a back-dated rollback is refused with MSG-GEN-001 naming the field. (b) It enforces the separation of duty: the loader holds Rules and parameters C or Reference data C, the approver holds Rules and parameters A (RW-RISK), and the loader cannot approve — MSG-P7-002, as the legacy criterion's "and the owner approves" requires (GAP-0848; ASM-1549). (c) It writes both changes to the decision record through the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03, H RWB-PLT-E1027-CON): one entry for the withdrawal of the version in force and one for the restoration of the previous version; a decision-record write failure stops the rollback with MSG-P7-003, which is the legacy third test case. (d) It calls the owning contract once, one hop with a 2 s timeout, and answers the rollback id, the restored version, the effective-from time, the two decision-record references and the state `ROLLED_BACK`, with the statement that decisions taken from that time use the previous version.
- **Two operations provided**, and no others: `POST /api/recovery/access/v1/admin/version-rollbacks`, which decides the gate and then calls the one owner; and `GET /api/recovery/access/v1/admin/version-rollbacks/{rollbackId}`, which answers the stored rollback answer and its two record references.
- **Three operations consumed**: the P7 rule-package rollback, the P3 reference-load rollback, and this service's own `POST /api/recovery/access/v1/authorise`.
- The metadata contract-dependency list of this story carries `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON` only, so the P7 rule-package rollback the rule arm calls has no published contract and no fake in the list; the call is built against that contract and its fake and the missing C dependency is raised at D1 — Not specified in the source documents (GAP-0844; ASM-1545).
- No source declares a path of `rwb-access` for a rollback and no source declares a rollback resource that can be read back; the two provided paths above and the read of a rollback are this story's — Not specified in the source documents (GAP-0845; ASM-1546).
- The request itself is not specified: one legacy action covers a rule version and a reference-data version whose restores go to different owners, and no source defines a body that carries the target kind — Not specified in the source documents (GAP-0846; ASM-1547).
- The loader's letter is not fixed in one place: the legacy permission checks say Rules and parameters C for RW-COE, while TSD P4 v3 T6.1 gives RW-COE "C, U" on rule packages and API-P4-018 is authorised by right U — Not specified in the source documents (GAP-0847; ASM-1548).
- The two decision codes of the two entries, and the field set of an entry of a rollback, are not in any source — Not specified in the source documents (GAP-0849; ASM-1550).
- "With an immediate date" is read as today's business date, and a date before today is refused; the reading is this story's — Not specified in the source documents (GAP-0850; ASM-1551).
- The reason a rollback must carry has no length, no coded list and no required flag in either owner's `RollbackRequest` — Not specified in the source documents (GAP-0851; ASM-1552).

### 2. Business rationale

A version in force that causes a breach is the one administration failure that cannot wait for the next release. The FSD states the target plainly: rule and limit changes made without a code release, 100 percent, measured from the decision log and the Workbench records every month (FSD P4 A2.22.1), and the same feature FEAT-ADM-06 asks that any versioned table be returned to its previous version with the rollback recorded. The Temporal and Drools design puts the whole rule lifecycle — authoring, the checks, the four eyes, the effective dating and the audit — in `rwb-decision`, and says the rollback is one call (slide 15). The legacy story served that inside the monolith, where the rule version and the reference version were rows of one module and one endpoint moved both; in the target the two restores belong to two owners and the administration service owns neither table.

What is left for `rwb-access` is the part that must be in front of both: the authority, the separation of duty and the record. The authority is a right in a capability area, read from `role` and `permission` as data. The separation of duty is the legacy criterion's "and the owner approves" made testable: the person who loaded the bad version is not the person who restores the version before it, and a rollback nobody else agreed to is refused with MSG-P7-002, exactly as the approval of a rule version is refused today (TSD P4 v3 T6.3). The record is the reason the control can be audited at all: the withdrawal of the version in force and the restoration of the previous version are two facts, and writing only the second leaves the audit trail claiming that a version was never in force.

The gate is also the only place where the two arms can be made to behave the same. A rule rollback is a decision-centre act on a package version and a reference-data rollback is a data act on a reference load, and their owners answer different shapes; a person on SCR-40 or SCR-39 should not have to know which service holds the table to undo a bad morning. This story accepts one request shape, resolves the target kind, calls one owner once and answers one shape — and it refuses a date in the past for both arms, because a rollback applied retroactively would silently re-decide working that has already been reported.

This story meets REQ-CWC-013 (a rule change goes from a validated load to production with a version stamp and no code release, and rolls back to the previous version by one call), REQ-DRI-010 (a parameter catalog and a configuration service hold every threshold and limit, versioned, changed without a code release) and REQ-ACA-013 (full administration screens for roles, permissions and delegation), and it carries the feature FEAT-ADM-06 Roll back a configuration version. It applies R-UNI-38 at its edge: a new version applies from its effective date and open cases keep the version they were decided under, so the answer states from when the previous version decides and claims nothing about work already decided. It applies R-UNI-39 in full: an action that cannot be recorded does not proceed, which in this story is the rule that a decision-record failure stops the rollback before the owner is called.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD013-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the two provided operations, the `VersionRollback` and `VersionRollbackRequest` schemas, the state set, the error envelope, the consumed-operation list and the contract fakes. This story implements that document and adds no path |
| RWB-P4-AD012-APP (same service, the story before it in the lane) | The approval gate of a rule version: the right model, the separation-of-duty rule and the record appender this story reuses, already built and tested |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the two entries of a rollback |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the reason length and the rollback switch of the gate, read with the version in force |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): the reference-data version, its state and its effective date, behind the reference arm |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): SCR-40 Reference data and SCR-39 Rules and parameters reach the two operations through it, one hop each |
| The `rwb-decision` rule-package contract | The operation the rule arm calls and its fake: the rollback of a package version. It is not in this story's metadata contract-dependency list (GAP-0844; ASM-1545) |
| The `rwb-case` reference-load rollback operation | API-P4-010, P3's under ASM-0041: the rollback of an approved reference load to the version before it |

Business preconditions carried from RWB-AD-013 and the P4 specifications:

- A version is in force and causes a breach; the previous version exists, is readable and carries its own effective dates.
- The loader holds Rules and parameters C or Reference data C; the approver holds Rules and parameters A, which TSD P4 v3 T6.1 gives to RW-RISK, and the loader cannot approve (GAP-0847; ASM-1548; GAP-0848; ASM-1549).
- The effective date of a rollback is today; a date before today is refused (GAP-0850; ASM-1551).
- The version states are the values of LOV-VERSION-STATUS, which carries LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED (TSD P4 v3 T3.2). This story produces `ROLLED_BACK` for the version it withdraws and observes `IN_FORCE` for the version it restores.
- The decision record is the platform library of DP-03 with the shared topic `rwb.decision-record.v1`; the central ledger is `rwb-decision`'s and is not read or written here.
- The administration screens are reached through the gateway-bff composite route; the rollback is offered on SCR-40 Reference data and on SCR-39 Rules and parameters.
- The caller's staff reference and its Entra group resolve through the service's own ACE view `v_ace_iam_group` (DP-05); no personal data is read, held or returned by this story.
- The reason a rollback carries is a free text of 20 to 1000 characters, as the break-glass reason of the same module is, until the owners publish a coded list (GAP-0851; ASM-1552).

### 4. Flow

1. The loader, holding Rules and parameters C or Reference data C, opens SCR-40 Reference data or SCR-39 Rules and parameters through the gateway-bff composite route and chooses the version in force that must go.
2. The screen calls `POST /api/recovery/access/v1/admin/version-rollbacks` with an `Idempotency-Key` and a body of `targetKind` (`RULE` or `REFERENCE`), `targetId` (the package version id or the reference load id), `previousVersionId`, `effectiveDate` and `reason`.
3. `VersionRollbackController` validates the body before anything else: each of the five fields must be present, `targetKind` must be one of the two values, `effectiveDate` must be a date and the reason must be within the length read in step 6. A missing or malformed field is 422 with MSG-GEN-001 naming the field (GAP-0846; ASM-1547).
4. `PermissionReader` calls the service's own authorise operation (`POST /api/recovery/access/v1/authorise`) with the caller's role and scope for the capability area that matches the target kind. A caller without the C or the U letter in that area is refused 403 with MSG-P4-002 and no owner is called; a target outside the caller's scope is refused 404 on the call and MSG-P4-003 on the screen that built it.
5. Where a break-glass grant is active for the caller, the answer carries the warning MSG-P4-004 with the grant reference, and the grant id is recorded with the rollback (FSD P4 v3 A2.9).
6. `ParameterReader` reads the reason length and the rollback switch through the parameters contract of DP-06 with the version in force. No length and no switch is a constant.
7. `EffectiveDateRule` compares `effectiveDate` with the business date of the service. A date before today is refused 422 with MSG-GEN-001 naming `effectiveDate`, and nothing is written and no owner is called: a retroactive rollback would re-decide working that has already been reported (GAP-0850; ASM-1551).
8. `SeparationOfDutyRule` compares the loader reference of the version in force with the caller reference. Where they are the same person, the call is refused 409 with MSG-P7-002 and no entry is written for the withdrawal, because the rollback has not been agreed by a second person (GAP-0848; ASM-1549).
9. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer and stores nothing; the owner is not called a second time.
10. `DecisionRecordWriter` appends the withdrawal entry first, through the local library of DP-03: decision code `VER-WDRW`, the target kind, the version in force, the restored version, the effective date, the loader and approver references and the outcome REQUESTED (GAP-0849; ASM-1550). Where the entry cannot be written, the call stops with 503 and MSG-P7-003 and the owner is never called, so no rule or reference version changes unlogged (R-UNI-39, TC-AD-013-03).
11. `OwnerRollbackClient` calls the one owner that holds the table, once, one hop, with a 2 s timeout and a breaker: `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback` for `targetKind` `RULE`, and `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` for `targetKind` `REFERENCE`, forwarding the reason and the `Idempotency-Key`.
12. The owner withdraws the version in force to `ROLLED_BACK` and puts the previous version in force from the effective date, and answers the restored version, its state and its effective-from time.
13. `DecisionRecordWriter` appends the restoration entry with decision code `VER-RSTR`, the same references, the restored version and the owner's answer reference, and closes the withdrawal entry with outcome DONE. Both entries and the stored answer are written in one local transaction with the outbox row, so the two facts reach `rwb.decision-record.v1` together (BR9).
14. The answer is 201 with `rollbackId`, `targetKind`, `targetId`, `restoredVersion`, `effectiveFrom`, `state` `ROLLED_BACK`, the two decision-record references and the statement that decisions taken from the effective time use the previous version, with the `Location` of the read (BR7, AC6).
15. Where the owner does not answer inside the 2 s budget, the answer is 503 with MSG-P7-003 and the withdrawal entry keeps outcome REQUESTED, so a retry under the same `Idempotency-Key` resumes the owner call instead of writing a second pair of entries.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field of the request is empty, `targetKind` is neither value, or `effectiveDate` is not a date | 422 naming the field, nothing written and no owner called | MSG-GEN-001 | AC2 |
| X2 | `effectiveDate` is before today | 422 naming `effectiveDate`, nothing written, no owner called | MSG-GEN-001 | AC2 |
| X3 | The caller holds neither the C nor the U letter in the area of the target kind | 403, nothing written, no owner called | MSG-P4-002 | AC4 |
| X4 | The caller has no role row at all in `rwb_access` | 403 and no entry, because there is no area to record against | MSG-P4-001 | AC4 |
| X5 | The target is outside the caller's scope | 404 on the call and the scope message on the screen that built it; the target is not named in the refusal | MSG-P4-003 | AC4 |
| X6 | The caller is the loader of the version in force | 409 with MSG-P7-002, no withdrawal entry and no owner call | MSG-P7-002 | AC3 |
| X7 | The withdrawal entry cannot be written | 503 and the owner is never called; no version changes | MSG-P7-003 | AC5 |
| X8 | The restoration entry cannot be written after the owner answered | 503 and the owner's change stands; the withdrawal entry stays open with outcome REQUESTED and the rollback is reported as recorded-in-part to the platform administrator queue, so the gap is visible rather than silent | MSG-P7-003 | AC5 |
| X9 | The owner answers 409 because the version is no longer in force | 409 with MSG-GEN-004 and the owner's code; the withdrawal entry keeps outcome REQUESTED and the screen asks the caller to reload | MSG-GEN-004 | AC4 |
| X10 | The owner does not answer inside the 2 s budget, or the connection fails | 503 with MSG-P7-003; a retry under the same `Idempotency-Key` resumes and cannot create a second pair of entries | MSG-P7-003 | AC6 |
| X11 | The same `Idempotency-Key` arrives twice | The first answer is replayed; the owner is called once and one pair of entries exists | None | AC6 |
| X12 | A break-glass grant is active for the caller | The rollback proceeds and the answer carries the warning and the grant reference | MSG-P4-004 | AC4 |

No exception path of this story writes a rule row, a reference row or a version state. The only writes are the two decision-record entries, their outbox rows and the stored answer; the state of a version is the owner's and is answered, never produced, here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-AD013-CON and its fakes and the two owner rollback contracts; no rule table and no reference table is read or written, and the P7 contract is consumed through its fake |
| Negotiable | The reason length, the switch, the decision codes and the wording of the answer statement are settled with the two owners and the administrators; the gate, the two paths, the state and the record are fixed |
| Valuable | One action undoes a bad rule or reference version in minutes, by a second person, with both changes recorded |
| Estimable | One controller, one validation pass, one date rule, one separation-of-duty rule, one authorise call, one owner client, one record writer and one idempotency store, with their tests |
| Small | Fits two weeks with its tests; it creates no table, starts no workflow and publishes no event of its own |
| Testable | Each of the six criteria has a test case in section 16, and both owners and the record library are stubbed in the fakes |

### 7. Acceptance criteria

```gherkin
Feature: Roll back a rule or reference version

  Background:
    Given the environment is SIT
    Given the business date is 15 December 2026
    Given package "ENTRY" carries version "ENTRY-2026.12" in force from 1 December 2026 and "ENTRY-2026.11" in force until 30 November 2026
    Given list "LOV-ROUTE" carries version "LOV-ROUTE 2026.12" in force from 1 December 2026 and "LOV-ROUTE 2026.11" in force until 30 November 2026
    Given test user "U-7301" holds RW-COE with the C letter in Rules and parameters
    Given test user "U-7302" holds RW-REFADM with the C letter in Reference data
    Given test user "U-7304" holds RW-RISK with the A letter in Rules and parameters
    Given test user "U-7305" holds RW-CASEOWN with the R letter only in Rules and parameters

  Scenario: AC1 Roll back (legacy RWB-AD-013 AC1)
    Given the rwb-decision contract mock returns version "ENTRY-2026.12" withdrawn to state "ROLLED_BACK" with the previous version "ENTRY-2026.11" in force from 15 December 2026
    Given a version in force that causes a breach
    When I load the previous version with an immediate date and the owner approves
    Then decisions from that time use the previous version and both changes are logged

  Scenario: AC2 A rollback dated before today is refused and nothing changes (new, D-RCV-60)
    Given "U-7301" calls POST /api/recovery/access/v1/admin/version-rollbacks with targetKind "RULE", targetId "ENTRY-2026.12", previousVersionId "ENTRY-2026.11", effectiveDate 1 December 2026 and a reason of 64 characters, with Idempotency-Key "k-013-1"
    When the call is made
    Then the response is 422 with message MSG-GEN-001 and its detail names "effectiveDate"
    Then the rwb-decision contract fake records no call and no decision-record entry is written
    Then version "ENTRY-2026.12" is still in force and still decides cases

  Scenario: AC3 The loader cannot approve the rollback of the version it loaded (new, D-RCV-60)
    Given "U-7301" loaded version "ENTRY-2026.12"
    When "U-7301" calls the rollback of "ENTRY-2026.12" to "ENTRY-2026.11" with an immediate date
    Then the response is 409 with message MSG-P7-002
    Then no withdrawal entry and no restoration entry are written and the rwb-decision contract fake records no call
    Then "U-7304", who holds the A letter, may make the same call and it is accepted

  Scenario: AC4 A reference-data version is restored through rwb-case in one hop (new, D-RCV-60)
    Given the rwb-case contract mock returns load "LD-2026-118" with the previous version "LOV-ROUTE 2026.11" in force from 15 December 2026
    Given "U-7302" loaded reference version "LOV-ROUTE 2026.12" and "U-7304" approves the rollback
    When "U-7302" calls the rollback with targetKind "REFERENCE", targetId "LD-2026-118", previousVersionId "LOV-ROUTE 2026.11" and an immediate date, with Idempotency-Key "k-013-2"
    Then the rwb-case contract fake records one call to POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback with the reason and the key, and the rwb-decision contract fake records none
    Then the response is 201 with the rollback id, the restored version "LOV-ROUTE 2026.11", effectiveFrom 15 December 2026 and state "ROLLED_BACK"
    Then test user "U-7305", who holds R only in Reference data, is refused 403 with MSG-P4-002 on the same call and no owner is called

  Scenario: AC5 Both changes are written and a record failure stops the rollback (new, D-RCV-60)
    Given the decision-record store is forced to fail on the withdrawal entry
    When "U-7301" rolls back "ENTRY-2026.12" to "ENTRY-2026.11" with an immediate date
    Then the response is 503 with message MSG-P7-003 and the rwb-decision contract fake records no call
    Then version "ENTRY-2026.12" is still in force
    When the store is restored and the same call is made with the same Idempotency-Key
    Then two decision-record entries exist: one with decision code "VER-WDRW" for the withdrawal of "ENTRY-2026.12" and one with decision code "VER-RSTR" for the restoration of "ENTRY-2026.11"
    Then both carry the loader and approver references, the two version labels and the effective date, and neither carries a name, an e-mail address or a personal field

  Scenario: AC6 One rollback id answers one rollback, twice if asked (new, D-RCV-60)
    Given "U-7301" rolls back "ENTRY-2026.12" to "ENTRY-2026.11" with Idempotency-Key "k-013-3" and the call is accepted
    When the same call is made again with Idempotency-Key "k-013-3"
    Then the first response is 201 with rollbackId, targetKind "RULE", targetId "ENTRY-2026.12", restoredVersion "ENTRY-2026.11", effectiveFrom 15 December 2026, state "ROLLED_BACK" and the two decision-record references
    Then the second response repeats that first answer and the rwb-decision contract fake records one call
    Then GET /api/recovery/access/v1/admin/version-rollbacks/{rollbackId} answers the same seven fields and the statement that decisions taken from 15 December 2026 use version "ENTRY-2026.11"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A rollback is one of two targets and nothing else: a rule package version held by `rwb-decision`, or a reference-data version held by `rwb-case`; `rwb-access` holds neither table and moves neither state | Ownership map (ASM-0069, ASM-0040, ASM-0041); DP-07; GAP-0846; ASM-1547 |
| BR2 | The version in force is withdrawn and the version named as the previous one is restored; both are identified by id and neither is inferred by the gate | Legacy RWB-AD-013 AC1; TSD P4 v3 API-P4-018 and API-P4-010 |
| BR3 | The effective date is today; a rollback dated before today is refused with MSG-GEN-001 naming the field, and nothing is written and no owner is called | Legacy RWB-AD-013 AC1 ("an immediate date"); GAP-0850; ASM-1551 |
| BR4 | The loader holds the C (or the U) letter in the capability area of the target, the approver holds the A letter, and the loader cannot approve; a self-approval is refused with MSG-P7-002 | Legacy RWB-AD-013 AC1 ("and the owner approves"); TSD P4 v3 T6.1 and T6.3; GAP-0847; ASM-1548; GAP-0848; ASM-1549 |
| BR5 | The gate calls exactly one owner, once, one hop, with a 2 s timeout and a breaker, and the arm it calls is chosen by the target kind alone | DP-11; TSD P4 v3 API-P4-018 and API-P4-010 |
| BR6 | The withdrawal of the version in force and the restoration of the previous version are two decision-record entries, not one | Legacy RWB-AD-013 AC1 ("both changes are logged"); DP-03; TSD P4 v3 T6.3 |
| BR7 | The answer carries the rollback id, the target, the restored version, the effective-from time, the state `ROLLED_BACK`, the two record references and the statement that decisions from that time use the previous version | Legacy RWB-AD-013 AC1; R-UNI-38; GAP-0845; ASM-1546 |
| BR8 | The version states are the values of LOV-VERSION-STATUS; this story produces `ROLLED_BACK` and reads the restored version's `IN_FORCE`, and writes no state of its own | TSD P4 v3 T3.2 and T4 |
| BR9 | Two entries and the stored answer are written in one local transaction with the outbox row, so the shared topic sees both facts or neither | DP-03; DP-09; R-UNI-39 |
| BR10 | A decision-record write failure stops the rollback before the owner is called, with MSG-P7-003, and no version changes | Legacy RWB-AD-013 TC-AD-013-03; FSD P4 v3 AC-EXC-P4-022-02; R-UNI-39 |
| BR11 | One `Idempotency-Key` answers one rollback: a repeated call replays the first answer, the owner is called once and one pair of entries exists | Architecture v5 slide 11; DP-09 |
| BR12 | A refusal for an absent letter names the action and the area and never the target; an out-of-scope target is a 404 on the call and MSG-P4-003 on the screen | Legacy RWB-AD-013 permission checks; TSD P4 v3 T6.1 |
| BR13 | The reason is carried to the owner unchanged, is required, and is read as 20 to 1000 characters until a coded list exists | TSD P4 v3 API-P4-018 and API-P4-010 (`RollbackRequest`); GAP-0851; ASM-1552 |
| BR14 | Every rollback records the caller reference and, where a break-glass grant is active, the grant id; the entries carry no name, no e-mail address and no personal field | Legacy RWB-AD-013 MSG-P4-004; FSD P4 v3 A2.9; Principle 5 |
| BR15 | Nothing is published on `rwb.access.events.v1`: a rollback changes no access policy and no delegation limit, so neither of the service's two events is its own | Architecture v5 slides 14 and 43 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is an absence of code: the service has no rule table, no reference table and no repository for either, so a target kind can only be routed to the owner that has one.
- BR2 is the request: both identifiers arrive in the body and are echoed in the answer, so the audit names exactly which version went and which came back.
- BR3 is one comparison against the service's business date, made before the record and before the call; the refusal names the field, so the screen can mark it.
- BR4 is a right and a rule: the letters come from `permission` rows, and the separation of duty compares two references, not two role codes, because one person may hold both roles.
- BR5 is the client: one method per arm, a 2 s budget, a breaker and no retry inside the request; the retry belongs to the caller with the same key.
- BR6 is the writer: two calls to the library, one entry each, and the second entry references the first, so a reader can see that the withdrawal and the restoration belong to one rollback.
- BR7 is the answer shape of the contract, and it is the only place the statement about decisions from that time is made.
- BR8 is a passthrough: `ROLLED_BACK` is the owner's state, echoed in the answer and written in the entry as the state the owner reported.
- BR9 is one transaction: the withdrawal entry, the restoration entry, the stored answer and the outbox rows commit together, and nothing commits if one insert fails.
- BR10 is the order of the flow: the withdrawal entry is written before the client is called, and its failure ends the request.
- BR11 is the idempotency table of the platform library in `rwb_access`, keyed by the caller's key.
- BR12 is the refusal shape: MSG-P4-002 for a letter, MSG-P4-001 for a role, MSG-P4-003 for a scope, and no target detail in any of them.
- BR13 is the parameter read: the length bounds arrive as rows, so a change of the bound is a data change.
- BR14 is the reference in the entry and in the answer, and the grant id where the warning MSG-P4-004 is returned.
- BR15 is a deliberate silence: the record topic carries the two facts, the access topic carries neither.

### 9. State transitions

This service holds no version state. It produces one state on the owner's table by calling the owner, and it reports what the owner answers.

| From | Event | Condition | To |
|---|---|---|---|
| `IN_FORCE` | A rollback is accepted on the gate | The caller may roll back, the date is today, the caller is not the loader, the record is written | `ROLLED_BACK`, with the previous version `IN_FORCE` from the effective date |
| `IN_FORCE` | A rollback is refused on the gate | A missing field, a past date, an absent letter, a self-approval or a record failure | `IN_FORCE`, unchanged, with the owner never called |
| `IN_FORCE` | The owner answers 409 | The version is no longer in force because another rollback or a promotion won the race | Unchanged, and the caller is told to reload |
| `ROLLED_BACK` | A later rollback names it as the previous version | It is still readable and carries its own dates | `IN_FORCE` again from the new effective date |

| Command | Condition | Outcome |
|---|---|---|
| Roll back a version | A letter in the area, today's date, a second person, the record written, the owner answers | 201 with `ROLLED_BACK` and the restored version |
| Roll back a version | A missing field, a past date or a reason outside its bounds | 422 with MSG-GEN-001; nothing written |
| Roll back a version | No C or U letter, or no role at all | 403 with MSG-P4-002 or MSG-P4-001; nothing written |
| Roll back a version | The caller loaded the version in force | 409 with MSG-P7-002; nothing written |
| Roll back a version | The record cannot be written | 503 with MSG-P7-003; the owner is not called |
| Roll back a version | The owner 409s, times out or is unavailable | 409 with MSG-GEN-004, or 503 with MSG-P7-003 and the withdrawal entry open |
| Read a rollback | Rules and parameters R, or Reference data R | 200 with the stored answer and its two record references |

The lifecycle of a version is the owner's (TSD P4 v3 T4 for a rule package version; the reference-data lifecycle is `rwb-case`'s under DP-07). This story holds no copy of it and changes none of its states by itself.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE Center of excellence analyst | Holds Rules and parameters C and, in the technical specification, U on rule packages: rolls back a rule version. Cannot approve its own rollback |
| RW-REFADM Reference data administrator | Holds Reference data C: rolls back a reference-data version. Holds R in Rules and parameters, so it may read a rule rollback and not make one |
| RW-RISK Risk and model risk officer | Holds Rules and parameters A: approves a rollback. The technical specification gives this role RA on Rules and parameters |
| RW-AUDIT Internal audit | Holds Rules and parameters R and Reference data R: reads a rollback, its two entries and its effective date |
| RW-PLATADM Platform administrator | Holds R in both areas: reads a rollback and operates the screens; makes none |
| RW-SECADM Security administrator | Holds R in both areas and decodes payloads under break-glass; makes no rollback |
| RW-CASEOWN and the other case roles | Hold R in both areas: they see that a version was rolled back and read nothing else of this story |
| The `rwb-decision` and `rwb-case` service identities | Answer the one rollback call each; they call nothing of this story |
| `rwb-access` itself | Reads `role`, `permission` and its own `v_ace_iam_group` ACE view, and writes the two record entries, their outbox rows and the stored answer |

The refusal shape is an RFC 9457 problem response with `messageId` set: MSG-P4-002 for an absent letter, MSG-P4-001 for an absent role, MSG-P4-003 for a target outside the scope, MSG-P7-002 for a self-approval and MSG-GEN-001 for a missing or out-of-range field. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-AD013-CON together with the rest of the service's contract.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| (ACE view) | `v_ace_iam_group` (ACE `iam_group`, RWB-ACE-001) | entra_group of the calling staff reference | Read through the service's own ACE view (DP-05) |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the withdrawal entry and the restoration entry of one rollback | Write |
| (outbox) | `outbox_event`, `processed_event` | the two entries and their `DecisionRecorded` message; no inbox row, because no event is consumed | Write and none |
| (idempotency) | `idempotency_key` | the request and the stored answer of a rollback, and the `rollbackId` that indexes them | Write (DP-09; ASM-0074) |
| DF-REF-274 to DF-REF-295 | `rule_package_version` of `rwb_decision` | the version label, the status, the effective dates, the author and approver, and `rollback_of` (DF-REF-294) | Returned through the contract; not read |
| DF-REF-001 to DF-REF-015 | `rule_row` of `rwb_decision` | none: the rows of a version are the registry's | None |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb_case` | the version, its state, its author, its effective dates | Returned through DP-07; not read |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | the version states of LOV-VERSION-STATUS | Returned through DP-07; not read |

No rule table and no reference table exists in `rwb_access`, and none is created: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s under ASM-0069, and `reference_row`, `reference_version` and `lov_value` are `rwb-case`'s under ASM-0071 and DP-07. Their fields arrive in the two contracts, not by a schema read (DP-01). The rollback record itself is the stored answer under the platform idempotency table plus the two decision-record entries; this story creates no table of its own, and the `rollbackId` it issues indexes that stored answer so the read can answer without a second call. No row of `decision_log_entry` (P7) is read or written, because the local record travels on `rwb.decision-record.v1` and the central ledger is `rwb-decision`'s. No row of `recovery_case`, `task` or `assignment` is read: the legacy data row of the story lists them for the monolith's benefit, and an administration gate reads no case.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1` (DP-13). Owner P4 `rwb-access`.

| Method | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/admin/version-rollbacks` | `VersionRollbackRequest`: `targetKind` (`RULE` or `REFERENCE`), `targetId`, `previousVersionId`, `effectiveDate`, `reason` | `VersionRollback`: `rollbackId`, `targetKind`, `targetId`, `restoredVersion`, `effectiveFrom`, `state`, `decisionRecordRefs[]`, `statement`, with the `Location` of the read | 401 MSG-P4-001; 403 MSG-P4-002 or MSG-P7-002 or MSG-P4-003; 404 unknown target; 409 MSG-GEN-004; 422 MSG-GEN-001; 503 MSG-P7-003 | Rules and parameters C or U for a rule version; Reference data C or U for a reference-data version; scope applied | `Idempotency-Key` required; a repeat answers the stored answer |
| GET | `/admin/version-rollbacks/{rollbackId}` | None | The same eight fields, with the two record references and the time the answer was stored | 401 MSG-P4-001; 403 MSG-P4-002; 404 unknown rollback | Rules and parameters R, or Reference data R | Not applicable, read only |

Both operations sit under the base `/api/recovery/access/v1` of DP-13. No source declares them: the legacy story named the rule-version load and approve paths of the monolith, TSD P4 v3 declares the two owner rollback paths (API-P4-018 and API-P4-010) and no administration path of its own, and the API Specification v4 declares no `rwb-access` rollback path at all — Not specified in the source documents (GAP-0845; ASM-1546). `version-rollbacks` is chosen because the gate's object is the act of rolling back, not the version, and the `rollbackId` is the handle the two record entries and the screen share.

The read is served from the stored answer of the accepted call and its two entries, not from the owner: neither owner publishes a rollback resource, and asking the owner again would let the read disagree with the record (GAP-0845; ASM-1546).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback` | P7 `rwb-decision` | The rule arm: withdraw the version in force to `ROLLED_BACK` and put the version before it in force from the effective date, with the reason |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | P3 `rwb-case` | The reference-data arm: the same move on a reference-data version, with the reason |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (this service) | The C or U check in the area of the target, and the A check of the approver, under the guard library of DP-08 |

The two owner operations are declared as consumed, never as provided, and each is called at most once in one rollback. The `rwb-decision` operation is P7's under ASM-0040 and is not in this story's metadata contract-dependency list, which is the missing contract of GAP-0844 and ASM-1545; the `rwb-case` operation is API-P4-010, P3's under ASM-0041.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 and P9 | entryId | two entries per rollback: `VER-WDRW` for the withdrawal of the version in force and `VER-RSTR` for the restoration of the previous version, each with the target kind, the two version labels, the effective date, the loader and approver references and the outcome |

Nothing is published on `rwb.access.events.v1`. That topic carries `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` only (Architecture v5 slides 14 and 43), and a rollback is neither an access policy change nor a delegation-limit change; the rule-version event `rwb.decision.RulePackageInForce.v1` (EV-30) is `rwb-decision`'s and is not published here either.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this story subscribes to nothing: the gate answers a request and calls an owner, and a promotion or a rollback by someone else is read from the owner's screen, not from an event.

#### 12.5 Workflows and activities

None. A rollback is one synchronous command with one downstream call; there is no long-running wait, no timer, no compensation and no activity on the `rwb-access` queue. The rule promotion at 00:01 (JOB-20) and the chain check at 02:00 (JOB-14) are `rwb-decision`'s Schedules.

#### 12.6 Schedules

None. A rollback is request-driven; the only Schedule in the version lifecycle is `rwb-decision`'s 00:01 promotion, and the six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the caller's role and its class |
| `permission` | P4 (`rwb_access`) | Read only: the C, U, A or R letter of the caller in the two areas |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_access` | The outbox rows of the two entries and the stored answer of each call; no inbox row is written because no event is consumed (DP-09) |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written: the rule version is the registry's (ASM-0069) |
| `reference_row`, `reference_version`, `lov_value` | P3 (`rwb_case`) | Not read from the schema: read through the reference-data contract of DP-07 (ASM-0071) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is `rwb-decision`'s |
| `recovery_case`, `task`, `assignment` | P3 (`rwb_case`) | Not read: an administration gate reads no case |

No table of another service is read and no foreign key crosses a schema (DP-01). The ACE data this story touches is its own `v_ace_iam_group` view (DP-05), which carries group names and no personal field.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision rule-package WireMock | the P7 rule-package contract (GAP-0844; ASM-1545) | `POST /admin/rule-package-versions/{versionId}/rollback` answering "ENTRY-2026.12" withdrawn to `ROLLED_BACK` with "ENTRY-2026.11" in force from 15 December 2026, for AC1, AC5 and AC6; a 409 for a version no longer in force, for X9; a 503 and a timeout for X10 |
| rwb-case reference-data WireMock | RWB-P3-E1043-CON and ASM-0041 | `POST /admin/reference-loads/{loadId}/rollback` answering load "LD-2026-118" restored to "LOV-ROUTE 2026.11" in force from 15 December 2026, for AC4; the load read of the same version, its state and its effective dates |
| parameters fake | RWB-P3-E1042-CON | The reason length of 20 to 1000 and the rollback switch, read with the version in force on 15 December 2026 |
| decision-record fake | RWB-PLT-E1027-CON | The append of the two entries, the reference they return, the hash-chain check and the forced failure of AC5 and X7 |
| authorise and guard fake | RWB-P4-AD013-CON, RWB-P4-E1037-CON | The C and U letters for RW-COE and RW-REFADM, the A letter for RW-RISK, R only for RW-CASEOWN and RW-AUDIT, and the no-role answer with MSG-P4-001 |
| gateway-bff composite route fake | RWB-PLT-N001-CON | The SCR-40 and SCR-39 routes that offer the rollback on the version in force, one hop each, and merge the answer with the version list |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 new; consumed 3 | Base `/api/recovery/access/v1`; the two owner rollback operations and the own authorise operation, one hop and 2 s each |
| Kafka | Published 1 event type on the shared record topic; consumed 0 | `rwb.decision-record.DecisionRecorded.v1` through the DP-03 library, twice per rollback; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | The promotion and the chain check are `rwb-decision`'s Schedules |
| File | None | A rollback reads no file: the workbook and the load file belong to the load stories |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/versionrollback`, Java package `th.co.scb.ace.workbench.recovery.access.versionrollback`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module rollback method that moved a rule version and a reference version through one service call (DP-11 and DP-13: two published contracts, one hop and a 2 s timeout, each under its owner's base), the direct read of the monolith's `rule_row` and `lov_value` (DP-01 and DP-07: the owners' contracts and no table read), the in-module decision log write (DP-03: the record library and the shared topic, twice per rollback), the `casewf.config` read of the reason length and the switch (DP-06: the parameters contract with the version in force), the `AceSourceQuery` call that resolved the caller's group (DP-05: the service's own `v_ace_iam_group` view), and the ace-web screens (DP-19: the SCR-40 and SCR-39 composite routes). There is no DP-04 in this story's pattern set on purpose: `rwb-access` embeds no Drools kit, evaluates no rule, and evaluates nothing about the rollback beyond the date and the two references.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| VersionRollbackController | Controller | The two operations: body validation, the `Idempotency-Key` requirement, RFC 9457 error mapping, `Location` on an accepted rollback |
| VersionRollbackService | Service | The gate: the order of the checks, the one owner call, the two record entries and the answer |
| PermissionReader | Service | The caller's `role` and `permission` rows in `rwb_access` and the letters of both areas, behind the authorise operation |
| StaffGroupReader | Service | The caller's staff reference and Entra group through `v_ace_iam_group`, with no personal field read |
| EffectiveDateRule | Service | BR3: today's date against the requested date, and the field name in the refusal |
| SeparationOfDutyRule | Service | BR4: the loader reference of the version in force against the caller reference, and the A letter of the approver |
| OwnerRollbackClient | Client | One method per arm, chosen by the target kind: one hop, 2 s, breaker, the `Idempotency-Key` forwarded, a 409 mapped to MSG-GEN-004 and a timeout to 503 |
| DecisionRecordWriter | Service | The `VER-WDRW` and `VER-RSTR` entries, their outbox rows and the reference they return, in the transaction that stores the answer |
| ParameterReader | Service | The reason length and the rollback switch through the parameters contract of DP-06, with the version in force |
| IdempotencyStore | Service | The `Idempotency-Key` lookup, the stored answer and the `rollbackId` index of the read |

**Database and migrations**

- This story creates no table of its own. The `role` and `permission` tables are created and loaded by the service's own stories, and the `outbox_event`, `processed_event` and `idempotency_key` tables are platform library objects created in `rwb_access` by the service's DB story in the per-service Flyway sequence of DP-15; this story only uses them.
- No rule table and no reference table is created here and no column is added to `rwb_access` for either: the registry holds the rule version, `rwb-case` holds the reference version, and the rollback record is the stored answer plus the two entries.
- No write statement touches `role` or `permission`, so a rollback can never grant itself a right.

**Configuration and reference data**

- The reason length of 20 to 1000 characters and the rollback switch are parameter rows of `rwb-case`, read through the parameters contract of DP-06 with the version in force (RWB-P3-E1042-CON); no threshold is a constant (BR13).
- LOV-VERSION-STATUS, LOV-CAPABILITY and the two target kinds are values read with the version in force; a new state or a new area is a row and a list value, and the build changes nothing (BR8).
- The decision codes of the two entries are proposed values pending the decision-code list, and they are carried as a gap: a change of code is a data and catalogue change, not a code change (GAP-0849; ASM-1550).

**Build steps**

1. `VersionRollbackController` with the two paths, the body validation and the error envelope; contract test against RWB-P4-AD013-CON.
2. `PermissionReader` and the letters of the two areas: the allowed answers for RW-COE, RW-REFADM and RW-RISK, and the refusals with MSG-P4-002 and MSG-P4-001; tests for AC4 and X3 to X5.
3. `EffectiveDateRule` on a fixed clock: today accepted, yesterday refused with MSG-GEN-001 naming `effectiveDate`, and no owner call; test for AC2.
4. `SeparationOfDutyRule`: the loader refused with MSG-P7-002 and a second person accepted; test for AC3.
5. `DecisionRecordWriter` and `IdempotencyStore`: the two entries of AC5, the reference they return, the forced failure of X7 and X8, and the replay of AC6 with one owner call.
6. `OwnerRollbackClient` against the two fakes: the rule arm of AC1 and AC6, the reference arm of AC4 with the `rwb-decision` fake recording no call, and the 409 and timeout of X9 and X10.
7. The resume path: a timeout answers 503 with the withdrawal entry open, and the retry under the same key resumes without a second pair of entries.
8. The read of AC6 over the stored answer and its two references, including the 404 of an unknown `rollbackId`.
9. The break-glass warning and the grant id of X12, and the reason bounds of BR13 read from the parameters fake.
10. The SCR-40 and SCR-39 composite routes through the gateway-bff fake, with the rollback offered on the version in force and the answer merged with the version list.

**Feature switch.** The gate is not behind a flag of its own: a rollback path that could be switched off would leave a breach-causing version in force exactly when it must go, which is the failure the story exists to prevent. The one switch that changes its behaviour is the parameter row of DP-06, and the contract keeps the gate as an invariant so that a switch turned off is a deliberate, recorded data change.

**Done when.** The tests in section 16 pass; a rule version and a reference-data version are each rolled back in one action by a second person with an immediate date; a past date is refused with MSG-GEN-001 naming the field and nothing changes; the loader is refused with MSG-P7-002; two entries exist for every accepted rollback and a record failure stops it with MSG-P7-003; and one `Idempotency-Key` answers one rollback however often it is sent.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-GEN-001 | A required field of the request is empty, `targetKind` is neither value, `effectiveDate` is not a date or is before today, or the reason is outside its bounds | Enter {field}. | This story, on the rollback; the detail names the field, and `effectiveDate` for a past date |
| MSG-P4-001 | The caller has no role row in `rwb_access` | You have no Recovery Workbench role. Ask your team manager to request one. | This story, from the authorise answer |
| MSG-P4-002 | The caller holds neither the C nor the U letter in the area of the target, or no A where the approver is checked | You cannot {action} here. Your role does not include it. | This story, from the authorise answer |
| MSG-P4-003 | The target is outside the caller's scope | This case is not in your scope. | This story, on the screen route that built the list; the target is not named in the refusal |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the answer, with the grant id recorded |
| MSG-P7-002 | The caller is the loader of the version in force | Not specified in the source documents (GAP-0848; ASM-1549); the text is the decision centre's and is kept verbatim | This story, on the separation-of-duty refusal, with the message id the technical specification names for a refused author approval |
| MSG-P7-003 | The decision record cannot be written, or the owner cannot be reached inside the 2 s budget | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on X7, X8 and X10; the owner's own 503 is passed through unchanged |
| MSG-GEN-004 | The owner answers that the version is no longer in force, or the same key arrives with a different body | Someone else changed this record. Reload it to see their change. | This story maps the owner's 409 onto this message; `detail` carries the owner's code |

The text of MSG-P7-002 is the one message of this story that the P4 module does not define: TSD P4 v3 T6.3 names the message for a refused author approval but carries no text, so the text is taken verbatim from the decision centre's catalogue and must be confirmed with that owner before the contract is frozen — Not specified in the source documents (GAP-0848; ASM-1549). The status of that refusal is the second open point of the same row: this story answers 409, because the rollback is a state the record already knows rather than a missing right, while the P4 approval story answers 403 (GAP-0848; ASM-1549). Every other error of this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request.

### 15. Screens and states

SCR-40 Reference data and SCR-39 Rules and parameters are the administration screens, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), which calls the version list of the owner and the two operations of this service, one hop each, and merges the answers. This story serves the rollback action and the state it produces and builds no screen surface of its own.

| Screen | State | What the screen shows |
|---|---|---|
| SCR-40 Reference data | Version in force | The version, its label, its effective-from date and the actions it permits: load, and roll back |
| SCR-40 Reference data | Rollback form | The target kind REFERENCE, the load, the previous version offered from the version list, the effective date defaulted to today, and the reason |
| SCR-40 Reference data | Refused | The 422 naming the field, the 403 with MSG-P4-002, the 409 with MSG-P7-002, or the 503 with MSG-P7-003 and the statement that nothing changed |
| SCR-40 Reference data | Rolled back | The restored version in force from today, the withdrawn version in `ROLLED_BACK`, the rollback id and the two decision-record references |
| SCR-39 Rules and parameters | Version in force | The version label, its valid-from date and the rollback action; the approval and promotion states are shown as the registry reports them |
| SCR-39 Rules and parameters | Rollback form | The target kind RULE, the package version, the previous version and the effective date defaulted to today |
| SCR-39 Rules and parameters | Refused | The same four refusals as SCR-40, with the owner's check where the registry refused the move |
| SCR-39 Rules and parameters | Rolled back | The restored version in force from today, the withdrawn version in `ROLLED_BACK`, the rollback id and the two decision-record references |

The legacy story lists SCR-40 Reference data with the states Versions and load. This story adds the rollback states to the same screen and adds the same action to SCR-39 for a rule version; the load and approval states of both screens belong to the load and approval stories of the same legacy family. The two screens show the rollback only where the caller holds the letter, so a reader never sees an action that would be refused.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-013-01 | AC1, BR2, BR6, BR7 | Contract | The `rwb-decision` fake: version "ENTRY-2026.12" withdrawn to `ROLLED_BACK`, "ENTRY-2026.11" in force from 15 December 2026, both entries present |
| TC-AD-013-02 | AC4, BR4, BR12 | Component | RW-CASEOWN with R only in Reference data on the rollback call: 403 with MSG-P4-002, the owner fake records no call |
| TC-AD-013-03 | AC5, BR9, BR10 | Contract | The record fake forced to fail on the withdrawal entry: 503 with MSG-P7-003, the owner fake records no call, the version stays in force |
| TC-AD-013-04 | AC2, BR3 | Component | `effectiveDate` 1 December 2026 against the business date 15 December 2026: 422 naming `effectiveDate`, no entry and no owner call |
| TC-AD-013-05 | AC3, BR4 | Component | RW-COE rolling back the version it loaded: 409 with MSG-P7-002, no entry, and the same call accepted for RW-RISK |
| TC-AD-013-06 | AC4, BR5 | Contract | The `rwb-case` fake: load "LD-2026-118" restored to "LOV-ROUTE 2026.11", one call to the reference-load rollback and none to the registry |
| TC-AD-013-07 | AC6, BR11 | Component | The same call twice with `Idempotency-Key` "k-013-3": one owner call, one pair of entries, the first answer replayed, and the read answering the same eight fields |
| TC-AD-013-08 | AC5, BR6, BR14 | Component | Two entries of one rollback: `VER-WDRW` and `VER-RSTR` with the two labels, the effective date and the two references, and no personal field in either |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the three legacy test cases TC-AD-013-01, TC-AD-013-02 and TC-AD-013-03 keep their ids and take the levels above. The legacy level System maps to Contract and Access to Component as the rows show. No ITG story is split from this legacy key, so no `-ITG` copy of a test case is written here.

### 17. Guardrails

- No business value in code: the reason length, the switch, the version states, the capability areas and the two target kinds are parameter rows and list values with versions (BR8, BR13). A test proves that a changed bound or a new state needs no build.
- No personal data anywhere: a rollback carries codes, version labels, dates, a reason and two user references, and the entries and the answer carry no name, no e-mail address and no personal field. No test data or prompt holds one.
- No read of another service's tables (DP-01): the rule version is `rwb-decision`'s and the reference version is `rwb-case`'s, and no foreign key crosses a schema.
- ACE data only through the owner's contract or its own `v_ace_*` views: the caller's group is read through `v_ace_iam_group` (DP-05), which carries no personal field.
- One writer per table: only `rwb-decision` moves a rule version and only `rwb-case` moves a reference version. This story holds no table of either, so a rollback cannot produce a state that the owner did not set.
- Four eyes on the undo: the loader of the version in force may not roll it back, and the refusal is MSG-P7-002 with nothing written (BR4).
- No retroactive rollback: a date before today is refused, so no reported working is re-decided by an administration action (BR3).
- No record, no rollback: the withdrawal entry is written before the owner is called and its failure ends the request, so no version changes unlogged (BR9, BR10, R-UNI-39).
- One key, one rollback: the `Idempotency-Key` is stored with the answer and the two entries, so a retry after a timeout cannot withdraw a version twice (BR11).
- Silence on the access topic: nothing is published on `rwb.access.events.v1`, so a cache refresh of the access policy is never triggered by a rollback (BR15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call | Epic 8 | FEAT-ADM-06 | All recovery processes | BR1, BR2, BR5, BR7 | TC-AD-013-01, TC-AD-013-06 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | Epic 8 | FEAT-ADM-06 | All recovery processes | BR8, BR13 | TC-AD-013-04, TC-AD-013-08 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 | FEAT-ADM-06 | All recovery processes | BR4, BR12 | TC-AD-013-02, TC-AD-013-05 |
| R-UNI-38 | A new rule version applies from its effective date and open cases keep the version they were decided under | Business Rules and Routing Logic v4 | FEAT-ADM-06 | All recovery processes | BR3, BR7 | TC-AD-013-01, TC-AD-013-04 |
| R-UNI-39 | An action whose decision record cannot be written does not proceed | Business Rules and Routing Logic v4 | FEAT-ADM-06 | All recovery processes | BR9, BR10 | TC-AD-013-03, TC-AD-013-08 |

| Legacy reference | Where it is kept |
|---|---|
| AC1: a version in force that causes a breach, the previous version loaded with an immediate date and the owner approving, decisions from that time on the previous version and both changes logged | Sections 1, 4, 7, 8, 9, 12.1, 12.2, 14 |
| Legacy test cases TC-AD-013-01, TC-AD-013-02 and TC-AD-013-03 (roll back, access, principle 5) | Section 16, exception paths X3 and X7 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-004, MSG-GEN-001, MSG-P7-002, MSG-P7-003 | Section 14, exception paths |
| Screens SCR-40 Reference data and SCR-39 Rules and parameters and their states | Sections 15, 19 |
| Permission checks: Rules and parameters C for RW-COE and A for RW-RISK | Sections 10, 12.1, 16 |
| Field IDs DF-REF-274 to DF-REF-295 of `rule_package_version`, `rollback_of` DF-REF-294 among them | Sections 11, 12.7 |
| Legacy key RWB-AD-013, story RWB-P4-AD013-APP, contract RWB-P4-AD013-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The two owner halves: the withdrawal and restoration of a rule package version in `rwb-decision` (P7, ASM-0069, API-P4-018) and of a reference-data version in `rwb-case` (P3, DP-07, ASM-0041, API-P4-010), including their states, their effective dating, their own change log entries and their own events.
- The load, the approval and the promotion of a version: RWB-P4-AD011-APP, RWB-P4-AD012-APP, RWB-P4-AD009-APP and RWB-P4-AD010-APP own those gates; this story is the undo only.
- The `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `reference_row`, `reference_version` and `lov_value` tables and their migrations.
- The Drools kit, the compile and the evaluation: this story evaluates nothing and swaps nothing in; the model-owning services fetch the version and verify the checksum (DP-04).
- The rule change report and the dry run (API-P4-019 and API-P4-020), which are `rwb-decision`'s and belong to the audit story of the same family.
- SCR-39's approval surface and SCR-47 Personal data; this story serves neither.
- The integration harness of the rollback journey: no ITG story is split from this legacy key, so the `-ITG` copies of the test cases are not written here.
- The Helm chart, the topic subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
