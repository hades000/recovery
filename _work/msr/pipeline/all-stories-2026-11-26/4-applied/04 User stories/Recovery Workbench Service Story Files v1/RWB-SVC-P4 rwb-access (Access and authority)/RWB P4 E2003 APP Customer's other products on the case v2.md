# RWB-P4-E2003-APP Customer's other products on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-P4-AE |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-016, FR-P4-018, FR-P4-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-003 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E2003-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **compliance and PDPA officer (RW-COMPLY), a case owner (RW-CASEOWN), a team manager (RW-TEAMMGR), a phone collector (RW-PHONECOL) and a platform administrator (RW-PLATADM)**, I want **the masking answer for the account number of the customer's other products — field `DF-ACE-281`, `v_ace_party_product.account_no` — held as rows of `masking_rule` at masking version `MASK-2026.12`, clear for the five roles the legacy story names and masked to the last four digits for every other role that holds the Case record right, served inside the authorise answer on `POST /api/recovery/access/v1/authorise` and on `GET /api/recovery/access/v1/masking-policies`, with the Case record R decision for that read refusing a role without it and answering a case outside the caller's scope as not found**, so that **every look at the other products shows the account number the caller's role is entitled to see, the same answer on every screen and to every agent, with one answer per masking version and no account number held anywhere in the access service**.

Inside `rwb-access` this is the access-side capability of legacy RWB-E2-003:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability is the masking answer and the Case record decision for the panel, not the product read: (a) the `masking_rule` rows for `DF-ACE-281` at masking version `MASK-2026.12`, with `unmasked` true for `RW-CASEOWN`, `RW-TEAMMGR`, `RW-RESTRUCT`, `RW-SPECIAL` and `RW-GUARANT` and false for `RW-PHONECOL` and every other role that holds Case record R; (b) the masking answer served per role and per masking version behind `POST /authorise` and `GET /masking-policies`, with the last-four default where no row applies (legacy AC3; FSD P4 AC-EXC-P4-004-05); (c) the Case record R decision for the other-products read, refused with MSG-P4-002 for a role without it (legacy TC-E2-003-07) and answered as not found with MSG-P4-003 for a case outside the scope (legacy AC5).
- The provenance each row carries is the ACE view, the field ID and the classification it masks: `DF-ACE-281` is `account_no` of `recovery.v_ace_party_product` (legacy section 11), and it is personal because the legacy story masks it by role under PDPA (BR4, DL26). `rwb-access` never reads that view and holds no account number: the view is read behind the rwb-source-data contract only (Architecture v5 slides 13 and 45; ADR-010).
- Because DP-03 and DP-09 are not patterns of this story, this slice adds no decision-record relay and no Kafka event. The access entry for the read is the caller's PII access event to ACE Common (legacy BR5, INT-22), written by the rwb-integration slice, and the authorise entry path is RWB-P4-E1037-APP's. This story writes no record, publishes nothing and consumes nothing.

The legacy behaviour carried into the access service is unchanged: the same roster of roles that see the number clear (assumed; DL26), the same last four digits for every other role, the same refusal of a role without Case record R with MSG-P4-002, the same "not in your scope" answer with MSG-P4-003, and the same stale marker MSG-P1-001 shown beside the list, which stays the data product's message and not this service's.

### 2. Business rationale

A case owner deciding a route today looks up the customer's other loans and deposits in other systems. ACE holds the customer product holding it receives from SCBPDM (DL20, INT-04), keyed by `person_key`, and the legacy story reads it for the borrowers and co-borrowers of the case, shows each product with its status and business date, marks the list stale when the holding is older than the expected business date, and masks account numbers by role. Nothing is copied into a Workbench table; the view is the record. It meets REQ-CHO-003 (customer and product facts from the ACE customer profile) and REQ-RDF-010 (access by role and masking under PDPA).

In the target the data stays where it is and the control moves to the service that owns it. Only rwb-source-data reads the thirty `recovery.v_ace_*` views (Architecture v5 slides 13 and 45; ADR-010), so the product holding is read through its contract; rwb-integration composes the panel read and serves it. The roles, the scope, the masking policy and the access log are rwb-access's (Architecture v5 slide 41: "Recovery roles as data, scope, masking policy, DoA table, access log"), and every service asks it before a read (slide 14: `POST /authorise`, cached; `/masking-policies`). So the masking answer behind the other products is a P4 answer, served once for every screen and every agent that shows the panel, and the roster behind it is data, not code.

This story is the rwb-access part of legacy RWB-E2-003. The product read, the endpoint `GET /api/recovery/integration/v1/cases/{caseId}/customer-products`, the freshness marker and the PII access event are the rwb-integration part (RWB-P2-E2003-APP); the ACE views and their grants are rwb-source-data's (RWB-P1-E1069-APP); the end-to-end proof across the services is RWB-ITG-E2003-ITG. This slice delivers the masking rows, the masking answer and the two refusals for that panel — not the read, not the panel and no new REST path.

The measure of success is the one the FSD P4 module is measured by: role and limit changes made without a code release at 100 percent, which holds here because the roster, the field ID, the markers and the masking version are rows. Every look at the other products is answered by the rows in force, a role without Case record R is refused with one message, a case outside the scope is not confirmed to exist, and no account number is written in the access service, its answers, its logs or its tests.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| The service contract of this service, in force from wave 1 (RWB-P4-E1037-CON and RWB-P4-E1037-APP, legacy RWB-E1-037) | `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on base `/api/recovery/access/v1`, with the role-to-permission matrix and the masking rows as data. This story implements the masking answer behind those operations for one field ID and adds no operation, so the metadata contract and build dependencies stay None: the contract is this service's own wave-1 baseline, not a dependency of this slice |
| The `rwb_access` baseline of the same wave-1 stories | The tables `role`, `permission` and `masking_rule` with the masking catalogue of TSD P4 T3.1 (DF-REF-198 to DF-REF-204: id, role_code, field_id, unmasked, masking_version, valid_from, valid_to) |
| Masking version `MASK-2026.12` in force for the wave-2 release | The roster of rows this story writes: `unmasked` true for `RW-CASEOWN`, `RW-TEAMMGR`, `RW-RESTRUCT`, `RW-SPECIAL` and `RW-GUARANT` and false for `RW-PHONECOL` and the other roles with Case record R. The roster is an assumption of the legacy story itself ("assumed"; DL26) and no source fixes it (GAP-0910; ASM-1632). The version label is Not specified in the source documents (GAP-0911; ASM-1633) |
| Permission matrix version `PM-2026.12` in force | It gives the Case record right R to the roles that read the panel and none to `RW-REFADM`, which is what legacy TC-E2-003-07 tests. The TSD P4 RBAC matrix has no Case record column, so the letters are read from the pack, as the wave-1 matrix story loads them |
| The field and its provenance | `DF-ACE-281` is `account_no` of `v_ace_party_product` (legacy section 11). The view ships in V0003, the Section B migration (DL43), and is granted to the rwb-source-data login only; `rwb-access` holds no grant on `recovery` and no view (ADR-010) |
| The rwb-integration read of this legacy key, live or mocked | `GET /api/recovery/integration/v1/cases/{caseId}/customer-products` for case `RW-2026-000410` with borrower `C-0410`, other products `A-0411` (`ACTIVE`) and `A-0412` (`DELINQUENT`), synthetic account number `9900015678` and data as of `2026-12-14`, as RWB-P2-E2003-APP serves it. This story calls no rwb-integration operation; the fixture names the values and the field list only |
| The gateway-bff composite route for SCR-03 Case record and its other products panel (DP-19; RWB-PLT-N001-CON) | The route that merges the panel from rwb-integration's read and the masking answer of this service. Its field list is Not specified in the source documents (GAP-0913; ASM-1635) |
| The reference-data contract of rwb-case (DP-07; RWB-PLT-E1043-CON and RWB-P3-E1043-CON) | `CASE_RECORD` read as a value of LOV-CAPABILITY, so no capability area is a Java constant; `lov_value` stays P3's under the ownership map |
| The rwb-access login (DP-02) | The per-service login of the schema. Its name is Not specified in the source documents (GAP-0916; ASM-1638) |
| The platform feature-flag library (R-PREC default ruling) | The switch of this capability, read as a flag and not as a parameter of another service |

### 4. Flow

1. Caller: a person opens SCR-03 Case record and the other products panel for case `RW-2026-000410`. gateway-bff resolves the session and asks the owners of the screen, one hop each.
2. rwb-integration: builds the authorise request from the read it is about to serve — the caller identity from the session, area `CASE_RECORD`, right `R`, the case ID and its owner for the scope test, and the field IDs the panel will show, `DF-ACE-281` among them (DP-11, DP-08).
3. rwb-access: reads the caller's roles and `permission` at the matrix version in force, `PM-2026.12`. No role of the caller holds `CASE_RECORD` R: the answer is 403 with MSG-P4-002 naming the action "read the customer's other products", and no masking answer is returned (BR5, AC5).
4. rwb-access: runs the scope test on the attributes the request carries — the case owner against the caller for scope OWN, the queue's team for TEAM, the region for REGION, no test for ALL. A case outside the scope is answered 404 with MSG-P4-003 and no case data, so the answer never confirms that the case exists (BR6, AC6).
5. rwb-access: reads `masking_rule` for `DF-ACE-281`, the roles the caller holds and the masking version in force: a row with `unmasked` true gives clear, a row with false gives masked to the last four digits, and a field with no covering row is masked (BR1, BR2; FSD P4 AC-EXC-P4-004-05).
6. rwb-access: answers with the field ID, the marker (`clear` or `masked`), the last-four shape where masked and the masking version it answered under. The answer carries no value, because the account number is ACE's and this service never holds it (BR3, AC2, AC3, AC7).
7. rwb-integration: applies the marker to the account number it read through the rwb-source-data contract and returns the panel: the number clear for a clear answer, `XXXXXX5678` for a masked one.
8. rwb-integration: writes the one PII access event for the read through ACE Common on INT-22 (legacy BR5; GAP-0914; ASM-1636). This story writes no decision record and publishes no event, because DP-03 and DP-09 are not its patterns; the authorise entry path is RWB-P4-E1037-APP's (BR10).
9. Masking change: a new masking version is loaded and approved through the load path, the rows of this story's field are added under it, and the next authorise call is answered under the new version with no restart and no event consumed (BR7, AC8).
10. The panel renders the account numbers the answer names. A stale holding shows MSG-P1-001 beside the list; the message is raised by the rwb-source-data and rwb-integration slices and is copied here unchanged, because the panel this answer guards shows it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No `masking_rule` row covers `DF-ACE-281` for any role the caller holds at the masking version in force | The field is answered masked with the last-four shape; the read is otherwise granted, and no error is shown | None | AC4 |
| X2 | No role of the caller holds Case record R | Refused before any masking row is read: 403, and no masking answer, no product and no account number | MSG-P4-002 | AC5 |
| X3 | The case is outside the caller's scope | Not found: 404 with no case data, no product and no account number, and one case ID echoed only as refused | MSG-P4-003 | AC6 |
| X4 | The masking rows cannot be read | Fail closed: every field is answered masked, the read continues, and an incident is raised to the platform administrator queue. No open answer is ever given from a failed read | None | BR2 |
| X5 | A request names a field ID the masking catalogue does not carry | The field ID is echoed and answered masked, and a break is raised to the data steward so the catalogue gains the field; no value is opened | None | BR2 |
| X6 | The feature switch of this capability is off | Every role is answered masked for `DF-ACE-281`, whatever its row says; the refusal paths are unchanged | None | BR9 |

A day on which two masking versions are both valid for the same field is Not specified in the source documents (GAP-0911; ASM-1633); until it is, the version whose `valid_from` is the latest on or before the business date is used, and the answer names the version it used.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against the wave-1 baseline of its own service and the published contract fake; the panel read of rwb-integration is a fixture and no other service is called at run time |
| Negotiable | The roster, the field ID, the markers and the masking version are rows; the story fixes the shape of the answer and the refusal behaviour only |
| Valuable | Every look at the other products shows the account number the caller's role is entitled to see, and no account number is held or logged by the access service |
| Estimable | One field's masking rows, one answer inside two existing operations, two refusals and one migration |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key; no screen, no read of the view, no event and no workflow |
| Testable | Every criterion in section 7 is one automated test against synthetic values; every cross-service answer is a fixture |

### 7. Acceptance criteria

```gherkin
Feature: Customer's other products on the case — the masking answer and the Case record decision of rwb-access

  Background:
    Given masking version "MASK-2026.12" is in force and holds a row for field "DF-ACE-281" with unmasked "true" for "RW-CASEOWN", "RW-TEAMMGR", "RW-RESTRUCT", "RW-SPECIAL" and "RW-GUARANT", and a row with unmasked "false" for "RW-PHONECOL"
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to "RW-CASEOWN", "RW-PHONECOL" and "RW-CONDUCT", and no CASE_RECORD right to "RW-REFADM"
    Given case "RW-2026-000410" has borrower "C-0410" and other products "A-0411" with status "ACTIVE" and "A-0412" with status "DELINQUENT", both with data as of 2026-12-14
    Given the other products of "C-0410" carry the synthetic account number "9900015678"

  Scenario: AC1 The masking rows answer at the masking version in force (new, D-RCV-60)
    When the compliance and PDPA officer reads GET /api/recovery/access/v1/masking-policies for field "DF-ACE-281"
    Then the answer names masking version "MASK-2026.12"
    Then the answer holds one row per role that has a row at that version, and each row names "DF-ACE-281" and its unmasked value
    Then the row for "RW-CASEOWN" is unmasked "true" and the row for "RW-PHONECOL" is unmasked "false"
    Then no row and no field of the answer carries an account number

  Scenario: AC2 A phone collector gets the last four digits (new, D-RCV-60)
    Given the caller holds only role "RW-PHONECOL" and case "RW-2026-000410" is in the caller's scope
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", case "RW-2026-000410" and field "DF-ACE-281"
    Then the answer grants the read, names masking version "MASK-2026.12" and answers "DF-ACE-281" as masked with the last-four shape "XXXXXX5678"
    Then the caller applies that shape to "9900015678" and the panel shows "XXXXXX5678"
    Then the answer carries no account number, and "9900015678" appears in no field of the answer and in no log line of this service

  Scenario: AC3 A case owner gets the account number clear (new, D-RCV-60)
    Given the caller holds only role "RW-CASEOWN" and owns case "RW-2026-000410"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", case "RW-2026-000410" and field "DF-ACE-281"
    Then the answer grants the read, names masking version "MASK-2026.12" and answers "DF-ACE-281" as clear
    Then the answer carries the marker and no value, because the account number is returned by the rwb-integration read and never by rwb-access

  Scenario: AC4 A role with no masking row is masked (new, D-RCV-60)
    Given the caller holds only role "RW-CONDUCT" and case "RW-2026-000410" is in the caller's scope
    Given no masking rule in "MASK-2026.12" covers field "DF-ACE-281" for "RW-CONDUCT"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", case "RW-2026-000410" and field "DF-ACE-281"
    Then the read is granted and "DF-ACE-281" is answered as masked with the last-four shape
    Then the answer names masking version "MASK-2026.12" as the version it answered under

  Scenario: AC5 A role without Case record R is refused (new, D-RCV-60)
    Given the caller holds only role "RW-REFADM", which has no CASE_RECORD right in "PM-2026.12"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", case "RW-2026-000410" and field "DF-ACE-281"
    Then the call is refused with status 403 and message MSG-P4-002 for action "read the customer's other products"
    Then the answer carries no masking answer, no product, no product status and no account number

  Scenario: AC6 A case outside the caller's scope is not found (new, D-RCV-60)
    Given the caller holds only role "RW-CASEOWN" with scope "OWN" and case "RW-2026-000410" belongs to another case owner
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", case "RW-2026-000410" and field "DF-ACE-281"
    Then the answer is status 404 with message MSG-P4-003 and carries no case data
    Then the answer carries no product, no product status and no account number

  Scenario: AC7 The answer names the field ID and its provenance, never the value (new, D-RCV-60)
    Given the caller holds only role "RW-CASEOWN" and owns case "RW-2026-000410"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", case "RW-2026-000410" and fields "DF-ACE-281" and "DF-ACE-284"
    Then the answer names "DF-ACE-281" as the personal field of "v_ace_party_product.account_no" that is masked by role
    Then the answer names "DF-ACE-284" as a field that no masking row of "MASK-2026.12" covers
    Then the answer carries no account number and no product status value, and rwb-access reads no "v_ace_party_product" row for either field

  Scenario: AC8 A masking version change refreshes the answer with no restart (new, D-RCV-60)
    Given "RW-PHONECOL" is answered masked for "DF-ACE-281" under "MASK-2026.12"
    When masking version "MASK-2026.13" is in force with a row for "DF-ACE-281" for "RW-PHONECOL" with unmasked "true"
    Then the next POST /api/recovery/access/v1/authorise for "RW-PHONECOL" and "DF-ACE-281" answers the field clear and names "MASK-2026.13"
    Then the service is not restarted, no event is consumed and no answer taken under "MASK-2026.12" is served after the change
```

The eight criteria above are new and test only this deliverable: the masking rows of one field, the masking answer at the masking version in force, and the two refusals of the other-products read. The legacy criteria of RWB-E2-003 are owned elsewhere: AC1, AC2, AC4 and AC6 of the legacy story are carried by rwb-integration (RWB-P2-E2003-APP) and rwb-source-data (RWB-P1-E1069-APP); the legacy exception X6 and legacy test case TC-E2-003-07 (a role without the Case record right is refused with MSG-P4-002) are answered here by AC5, and legacy AC3 is answered here by AC2, AC3 and AC4 and applied by the panel on the P2 side. AC7 is the criterion that keeps the provenance: the answer names the view and the field ID and never the value, so a clear answer opens the number in the caller and not in the access service. AC8 is the criterion that makes the roster a data change rather than a release.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The masking roster for `DF-ACE-281` is rows of `masking_rule` with `role_code`, `field_id`, `unmasked`, `masking_version` and their validity dates; no roster, marker or version is written in code | FSD P4 A2.5; BR-P4-005; TSD P4 T3.1 (DF-REF-198 to DF-REF-204); principle 1 |
| BR2 | A personal field is answered clear only where a `masking_rule` row for a role the caller holds and that field says `unmasked` true at the masking version in force; with no covering row the field is answered masked to the last four digits | FSD P4 A2.5 AC-EXC-P4-004-05; NFR-039; NFR-040; legacy AC3 |
| BR3 | The answer carries the field ID, the marker, the last-four shape and the masking version, and never a value; rwb-access holds no account number and no product row | DP-01; DP-05; NFR-039; NFR-040 |
| BR4 | The caller's roles are unioned, as the permission letters are: one clear row for any role the caller holds makes the field clear for that caller | FSD P4 AC-ALT-P4-001-02 (two roles give the permissions of both); FSD P4 A2.4 |
| BR5 | The Case record right is decided before the masking answer: no `CASE_RECORD` R for any role the caller holds is refused with MSG-P4-002 and no masking answer | FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.1; legacy TC-E2-003-07 |
| BR6 | A case outside the caller's scope is answered as not found with MSG-P4-003 and returns no case data, no product and no account number | FSD P4 A2.14 VR-P4-014-1; legacy AC5 |
| BR7 | The masking version in force is the latest `valid_from` on or before the business date; the answer names the version it used, so a new version changes the answer with no restart and no deployment | TSD P4 T3.1 (`masking_version`, `valid_from`, `valid_to`); FSD P4 AC-EXC-P4-004-05 |
| BR8 | The provenance of the field is recorded with its row: `DF-ACE-281` is `account_no` of `v_ace_party_product`, personal under DL26 and PDPA; the other fields of the view are named as identifiers only | Legacy section 11; REQ-RDF-010; DL26 |
| BR9 | The service reads no ACE view, no other service's schema and no `recovery` table; the account number is read by rwb-source-data and composed by rwb-integration | Architecture v5 slides 13 and 45; ADR-010; DP-01; DP-05 |
| BR10 | This slice writes no decision record and publishes no event: DP-03 and DP-09 are not its patterns; the access entry of the read is the caller's PII access event to ACE Common (INT-22) and the authorise entry path is RWB-P4-E1037-APP's | Legacy BR5; INT-22; Architecture v5 slide 14 (P4 events: the two policy events only); DP-03, DP-09 |

Target-service statements that make the rules hold in `rwb_access`:

- BR1 is a read of `masking_rule` by `field_id`, `role_code` and `masking_version`, and a write of rows only through this story's migration for the field it owns. The rows are versioned by `masking_version` with `valid_from` and `valid_to`, and a version is never edited in place: a new version is added and the next answer uses it.
- BR2 is a read that returns markers, never values, so no personal data crosses the service boundary in either direction. The last-four shape is a presentation rule named by the answer; the value it is applied to never enters this service.
- BR3 and BR8 keep the answer to identifiers: `field_id`, `unmasked`, `masking_version` and the marker. The view name and the personal classification are carried as catalogue provenance on the row and in the answer, and no row of `v_ace_party_product` is read to answer.
- BR4 is the union of the caller's roles, the same rule the letters of a capability area follow. Which marker wins when two rows of the same version cover the same role and field is Not specified in the source documents; this story reads the latest `valid_from` of the two and records the choice in the review.
- BR5 and BR6 are decided before the masking read, so a refused caller learns nothing about the field and nothing about the case; the refusal names the action and never a case fact.
- BR7 is the whole of the change mechanism of this slice: the masking version in force is read on each answer, so an approved version changes the answer with no restart, and no event is needed to invalidate a cache.
- BR9 and BR10 are visible in the code review and in the boundary test: no `recovery.` query, no `rwb_case`, `rwb_source_data` or `rwb_integration` table, no outbox row, no decision record and no topic name in this story.
- The feature switch of BR9 in section 13 is the only runtime branch: off answers masked for every role and leaves both refusals as they were.

### 9. State transitions

None for the case. This story changes no case status, no product, no holding and no policy version's lifecycle: the case and its products are rwb-case's and ACE's, and the load and approval of a masking profile are the load path's (RWB-P4-AD004-APP) and the wave-1 matrix story's.

The only states this story has are the states of its answer:

| Answer state | When | What the caller gets | Written by this story |
|---|---|---|---|
| Clear | A row for a role the caller holds says `unmasked` true at the masking version in force | The field ID with the marker `clear` and the version | No record and no event (BR10) |
| Masked | A row says `unmasked` false, or no row covers the field | The field ID with the marker `masked`, the last-four shape and the version | No record and no event (BR10) |
| Refused, no right | No role of the caller holds Case record R | 403 MSG-P4-002, no masking answer | No record and no event (BR10) |
| Not found | The caller holds the right and the case is outside the scope | 404 MSG-P4-003, no case data | No record and no event (BR10) |

A masking version moves from loaded to approved to in force to superseded or rolled back in the load path, on the version rows it owns; this story reads the version in force, adds its field's rows under it, and holds no state of its own between calls.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record R: is answered the account number of the other products clear, as the legacy roster assumes |
| RW-TEAMMGR, team manager | Case record R: clear, as the roster assumes |
| RW-RESTRUCT, restructuring officer | Case record R: clear, as the roster assumes |
| RW-SPECIAL, hardship and vulnerability specialist | Case record R: clear, as the roster assumes |
| RW-GUARANT, guarantee officer | Case record R: clear, as the roster assumes |
| RW-PHONECOL, phone collector | Case record R, account number masked to the last four digits |
| RW-CONDUCT and every other role that holds Case record R | Case record R, account number masked; a role with no row is masked by default |
| RW-REFADM, reference data administrator | No Case record right in the matrix: the other-products read is refused with MSG-P4-002 |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rows and reads them through `GET /masking-policies`; this story writes the rows for one field only, and every later change goes through the load path |
| RW-DATASTEW, data steward and data product owner | Owns the field catalogue the provenance comes from; receives the break of X5 when a field ID is not covered |
| RW-PLATADM, platform administrator | Receives the incident of X4 and operates the switch of X6 |
| The rwb-access service identity (the rwb-access login, DP-02) | Reads `role`, `permission` and `masking_rule`, writes the rows of its own migration, and serves the answer |
| The rwb-integration service identity | Asks the authorise decision for the panel read and applies the marker it is given; it holds no masking row of its own |

The roster above is the assumption of the legacy story (GAP-0910; ASM-1632) and is data: no role code appears in Java. The login name is Not specified in the source documents (GAP-0916; ASM-1638); the story says "the rwb-access login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Write the rows of `DF-ACE-281` in this story's migration; read at every answer |
| DF-REF-199 | `masking_rule` | role_code | Write and read |
| DF-REF-200 | `masking_rule` | field_id (`DF-ACE-281`) | Write and read |
| DF-REF-201 | `masking_rule` | unmasked | Write and read |
| DF-REF-202 to DF-REF-204 | `masking_rule` | masking_version, valid_from, valid_to | Write and read |
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-CAPABILITY, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-ACE-281 | `v_ace_party_product` (ACE, behind the rwb-source-data contract) | account_no: named in `masking_rule.field_id` and in the answer, never read and never copied | Named only |
| DF-ACE-280, DF-ACE-282 to DF-ACE-285 | `v_ace_party_product` (ACE) | person_key, account_key, product_type, product_status, data_as_of: the other fields of the panel, named as identifiers only | Named only; no masking row covers them |

The provenance of the row is the whole of the field's treatment in this service: `DF-ACE-281` is `account_no` of `recovery.v_ace_party_product`, personal under DL26 and REQ-RDF-010, and the rows that mask it are the only record of it here. No account number, product status or person key enters `rwb_access`, the answer or a log line: markers, field IDs and version labels are the whole payload (NFR-039, NFR-040). Field IDs are those in the Logical Data Model and Data Dictionary v9, and the panel's field list is the one legacy section 11 names.

Whether `DF-ACE-281` is the only personal field of the panel, and whether the other six fields need a row or an explicit `unmasked` false, is Not specified in the source documents (GAP-0912; ASM-1634); this story writes rows for `DF-ACE-281` only and answers the other fields as covered by no row.

### 12. Contract

#### 12.1 REST operations provided

None new. The masking answer is served inside the operations of the service contract already in force from wave 1 (RWB-P4-E1037-CON), on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Operation | Path | What this story answers behind it |
|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The Case record right, the scope result and the masking answer for field `DF-ACE-281` and the caller's roles at the masking version in force, with the marker and the last-four shape. Errors 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003) |
| GET | `/api/recovery/access/v1/masking-policies` | The masking version in force and the rows this story holds for `DF-ACE-281`, per role, with `unmasked` and the validity dates |

`GET /me/permissions` is the same contract and is not used by this story; `GET /doa-limits` belongs to the delegation slice (RWB-P4-E2013-APP) and is not read here.

The field names of the masking answer — the per-role rows of `/masking-policies`, the marker and the last-four shape inside `/authorise` — are Not specified in the source documents (GAP-0915; ASM-1637); they are fixed by RWB-P4-E1037-CON at build time and the story keeps the names that contract publishes.

#### 12.2 REST operations consumed

None. This story consumes no operation at run time: the caller carries the case attributes the scope test needs inside the authorise request, and the panel read of rwb-integration (`GET /api/recovery/integration/v1/cases/{caseId}/customer-products`) is a fixture of the tests and the alignment reference of the build, not a call of this service. One hop and the 2 s budget of DP-11 apply to the inbound call.

#### 12.3 Events published

None. DP-03 and DP-09 are not patterns of this story: there is no decision-record relay, no outbox row and no topic of its own. `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` announces a new policy version and belongs to the wave-1 matrix story (RWB-P4-E1037-APP) and the load path (RWB-P4-AD002-APP, RWB-P4-AD004-APP); `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` carries the access entries, and the authorise entry path is RWB-P4-E1037-APP's. The access entry of the other-products read is the PII access event the caller writes to ACE Common on INT-22.

#### 12.4 Events consumed

None. The service listens to no topic for this capability: the masking version in force is read on each answer, so a new version needs no message, no cache drop and no restart.

#### 12.5 Workflows and activities

None. The answer is a synchronous REST call in the caller's thread; this story runs no Temporal workflow and registers no activity on `rwb-access`.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Schedule of this service and its story is RWB-P4-AD008-APP; this story starts no Schedule.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `masking_rule` | P4 (`rwb_access`) | The rows for `DF-ACE-281` written by this story's migration, and read at every answer |
| `role` | P4 (`rwb_access`) | The caller's roles and their `default_scope` |

No other table is written by this story. `permission` is read for the Case record letter and belongs to the wave-1 matrix story, which writes it; `lov_value`, `reference_row` and `reference_version` stay P3's and are read through the reference-data contract; `delegation_limit` is the delegation slice's; `outbox_event`, `processed_event` and `idempotency_key` are library objects of `rwb_access` and this story writes none of them, because it publishes no event and consumes none (DP-09 is not applied here).

No table of `rwb_case`, `rwb_integration`, `rwb_source_data` or `recovery` is read, and `v_ace_party_product` is never queried (DP-01, DP-05). The provenance of the field is a catalogue fact carried on the row, not a join.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| the rwb-integration read fixture of this legacy key | RWB-P2-E2003-APP's operation, as it publishes it | Case `RW-2026-000410`, borrower `C-0410`, other products `A-0411` (`ACTIVE`) and `A-0412` (`DELINQUENT`), synthetic account number `9900015678`, data as of `2026-12-14`, and the last-four shape `XXXXXX5678`; carried as the values the answer is asserted against, never called |
| RWB-P4-E1037-CON fake | The authorise and masking operations of this service | A granted case, a refused role, an out-of-scope case, and the masking-policy read at `MASK-2026.12` and at `MASK-2026.13` |
| masking catalogue fixture | This story's own rows | The five clear roles, the masked `RW-PHONECOL`, a role with no row (`RW-CONDUCT`), and a field with no row (`DF-ACE-284`) |
| reference-data fake | RWB-P3-E1043-CON (DP-07) | LOV-CAPABILITY with `CASE_RECORD`, and the unavailable-list case of X4 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (2 existing operations of RWB-P4-E1037-CON implemented for this field), consumed 0 | Base `/api/recovery/access/v1`; one hop and 2 s on the inbound call, and no outbound call |
| Kafka | None | No topic published and none consumed; the access entry is the caller's PII event on INT-22 |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` for this capability |
| File | None | No file input, no file output and no export |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `masking`, Java package `th.co.scb.ace.workbench.recovery.access.masking`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This secondary slice adds no new build dependency of its own: metadata "Depends on (build)" and "Contract dependencies" stay exactly as the Work Package fixes them (both None), the platform contract libraries the DP rows name arrive with the baseline of the service lane, and DP-08's contract is delivered by that baseline and RWB-P4-E1037-CON, which is this service's own wave-1 story rather than a dependency of this slice.

DP-01 is the reason the answer is built from the service's own rows: `v_ace_party_product` is behind the rwb-source-data contract and no query of this service touches `recovery`. DP-05 applies as a prohibition and as provenance: the field the row masks is named by its ACE view and field ID, and the view is never read, because only rwb-source-data reads the thirty `recovery.v_ace_*` views (Architecture v5 slides 13 and 45; ADR-010). DP-07 supplies `CASE_RECORD` as a value of LOV-CAPABILITY, so no capability area is a Java constant. DP-08 is the authorise answer this masking answer is served inside, with the cached permission read of the caller; this story adds the masking part of that answer and nothing else. DP-11 is the caller-facing boundary: one hop, 2 s, and the answer must hold inside it. DP-15 is this story's migration in the per-service Flyway sequence. DP-19 is the route that renders the answer: SCR-03 and its other products panel are composed at the edge by gateway-bff, which calls rwb-integration for the read and this service for the answer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| MaskingPolicyController | Controller | Serves `GET /masking-policies` for a field list and the caller's roles, and the masking part of the problem responses of the contract |
| AuthoriseMaskingContributor | Service | Supplies the masking answer inside `POST /authorise`: the field ID, the marker, the last-four shape and the masking version |
| MaskingAnswerService | Service | Unions the caller's roles, reads the rows at the masking version in force, resolves clear or masked per field, and answers markers only |
| MaskingRuleRepository | Repository | Reads and writes `masking_rule` in `rwb_access` by `field_id`, `role_code` and `masking_version`; reads no foreign table |
| RoleResolver | Service | Resolves the caller's roles and their `default_scope` from `role`; refuses an answer with no role (MSG-P4-001) |
| CaseRecordDecision | Service | The `CASE_RECORD` right from `permission` at the matrix version in force, and the scope test on the attributes the request carries; MSG-P4-002 and MSG-P4-003 before any masking row is read |
| FieldCatalogue | Service | The provenance of a field ID: the ACE view, the entity field and the personal classification carried on the row and named in the answer |
| MaskingVersionResolver | Service | The masking version in force for the business date, with the latest `valid_from` rule; no cache held across versions |
| MaskingCatalogueMigration | Migration | Writes the rows of `DF-ACE-281` at `MASK-2026.12` and the index behind the two reads |

**Database and migrations**

- No new table: `masking_rule`, `role` and `permission` exist from the wave-1 baseline behind RWB-P4-E1037-CON.
- One migration in the per-service Flyway sequence of DP-15: `V2003_1__other_products_masking.sql` writes the rows of `DF-ACE-281` for the roster at `MASK-2026.12` with `valid_from` on the wave-2 release date and no `valid_to`, and adds `ix_masking_rule_role_field` on `masking_rule (role_code, field_id, masking_version)` so the answer is one index read inside the 2 s budget of DP-11.
- The rows are data, not constants: a later roster or version is added as new rows by the load path of RWB-P4-AD004-APP and this migration is never edited. Whether the roster is the five clear roles and every other role masked is the assumption of ASM-1632.

**Configuration and reference data**

- The masking version in force is data: the latest `valid_from` on or before the business date, read from `masking_rule.masking_version`. The label of the wave-2 version is `MASK-2026.12` by assumption (GAP-0911; ASM-1633).
- The roster of rows is data (ASM-1632). No role code, field ID, marker or version appears in Java (BR1).
- LOV-CAPABILITY comes through the reference-data contract of DP-07 (RWB-P3-E1043-CON), so `CASE_RECORD` is a list value.
- The database login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0916; ASM-1638).

**Build steps**

1. `MaskingRuleRepository` and `MaskingVersionResolver` over `masking_rule`, with the latest-`valid_from` rule and the version named in every answer; tests for AC1 and AC8.
2. `MaskingAnswerService` with the role union, the covering row and the default masked case; tests for AC2, AC3 and AC4, and a test that a new roster row changes the answer with no code change.
3. `CaseRecordDecision` with the right read before the masking read, the scope test on the request attributes and the two refusals; tests for AC5 and AC6.
4. `FieldCatalogue` with the provenance of `DF-ACE-281` and a field with no row; test for AC7.
5. `AuthoriseMaskingContributor` and `MaskingPolicyController` so the same answer is served inside `/authorise` and on `/masking-policies`; a contract test that the two agree for the same role and version.
6. The migration of the rows and the index, and a timing test that one answer stays inside the 2 s budget on a masking catalogue of the loaded size.
7. The contract-fake run of the whole capability against the RWB-P4-E1037-CON fake and the rwb-integration fixture, so the story builds before the panel read is live in the environment.
8. A guardrail test that no account number, no product row and no `recovery.` query exists in the module.

**Feature switch.** `rwb.access.other-products-masking`, read from the platform feature-flag library (R-PREC default ruling; not a parameter of rwb-case, because DP-06 is not a pattern of this story). Off: every role is answered masked for `DF-ACE-281` whatever its row says, the refusal paths are unchanged and no schema change is needed — so a switch that fails leaves the account number closed, never open.

**Done when.** The tests in section 16 pass; in SIT a case owner is answered `DF-ACE-281` clear, `RW-PHONECOL` and a role with no row are answered masked with the last-four shape and see `XXXXXX5678` for `9900015678`, `RW-REFADM` is refused with MSG-P4-002, a case outside the scope is answered 404 with MSG-P4-003, and a new masking version changes the answer with no restart; and no account number, product row or person key is held by `rwb-access`, its answers, its logs or its tests.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role | You have no Recovery Workbench role. Ask your team manager to request one. | The access check before this story's answer |
| MSG-P4-002 | No role of the caller holds Case record R for the other-products read | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR5; {action} is "read the customer's other products" |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR6 |
| MSG-P1-001 | The customer product holding is older than the expected business date, shown beside the panel this answer guards | {product} is from {date}. Today's load has not arrived. | The rwb-source-data and rwb-integration slices of this legacy key; copied here unchanged because the panel shows it |

For MSG-P4-002 the {action} value names the action the caller attempted and never a case fact; for MSG-P4-003 no case fact is echoed, because the message must not confirm that a case exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10. This story adds no message of its own: a default-masked field is not an error and raises none.

### 15. Screens and states

This story builds no screen. SCR-03 Case record and its other products panel are served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), which calls rwb-integration for the product read, rwb-case for the case facts and this service for the masking answer, one hop each, and merges the answers into the screen model. The route's field list and its masking step are Not specified in the source documents (GAP-0913; ASM-1635).

What this story decides for the panel is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03, other products panel | Loading, then read only | The products of the case arrive from rwb-integration; each account number is shown as this answer names it, clear or masked |
| SCR-03, other products panel | Granted, clear | The account number is shown as the caller is entitled to see it; the panel holds no masking rule of its own |
| SCR-03, other products panel | Granted, masked | The account number is shown as `XXXXXX5678` for `9900015678`; the last four digits only |
| SCR-03, other products panel | Granted, field with no row | The account number is masked by default, with no message and no gap on the screen |
| SCR-03, other products panel | Stale holding | The list shows with the stale banner MSG-P1-001; the masking answer is unchanged |
| SCR-03, other products panel | Empty list | No product shows and the panel's empty state is the rwb-integration slice's; the masking answer is unchanged |
| SCR-03 | Refused | The page shows MSG-P4-002 and no product and no case fact |
| SCR-03 | Not found | The page shows MSG-P4-003 and no product and no case fact |

A screen that renders an account number clear because a client cached an older answer is a defect of the screen, not of the answer: the answer always names the masking version it used, and a field is clear only where a row of that version says so.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-003-07 | AC5, BR5 | Component | `RW-REFADM` (no Case record right) asks the authorise decision for the other-products read of case `RW-2026-000410`; refused with MSG-P4-002 and no masking answer |
| TC-E2-003-01 | AC1, AC3, AC7, BR1, BR2, BR3, BR8 | End to end | Synthetic customer `C-0410` with two other products `A-0411` (`ACTIVE`) and `A-0412` (`DELINQUENT`) of case `RW-2026-000410`, read by `RW-CASEOWN`; both show, and `DF-ACE-281` is answered clear with its provenance |
| TC-E2-003-02 | AC1, BR7 | End to end | Holding last loaded `2026-12-13` against the expected business date `2026-12-14`; the panel shows MSG-P1-001 and the masking answer is unchanged |
| TC-E2-003-03 | AC2, AC3, AC4, BR2, BR4 | End to end | `RW-PHONECOL` and `RW-CASEOWN` read the same case `RW-2026-000410` with account number `9900015678`: `XXXXXX5678` for one, clear for the other, masked for `RW-CONDUCT` with no row |
| TC-E2-003-04 | AC1, BR2 | End to end | Customer `C-0420` with no other product: the empty list changes no masking row and no answer |
| TC-E2-003-05 | AC6, BR6 | End to end | Case owner with scope `OWN` and case `RW-2026-000410` of another owner; 404 with MSG-P4-003 and no case data |
| TC-E2-003-06 | X4, BR3, BR10 | NFR | The ACE PII logging stub refuses the access event; the read of the other products fails with MSG-GEN-006 and no masking answer, no account number and no field value is written by `rwb-access` |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. Every legacy test case of this key is listed above with the slice this story answers: TC-E2-003-07 is the refusal this story owns whole; TC-E2-003-01 and TC-E2-003-04 assert the answer under which the panel read is served and leave the products, the freshness and the empty state to rwb-integration; TC-E2-003-02 owns only the invariance of the masking answer when the holding is stale, because the stale marker and MSG-P1-001 are the data product's; TC-E2-003-03 is the masking case this story answers from end to end; TC-E2-003-05 is the out-of-scope refusal; and TC-E2-003-06 is proved here only as the statement that nothing of this service is written or opened when the PII event fails, because the event itself is rwb-integration's and ACE Common's. The `-ITG` copies of these cases are not here: they belong to RWB-ITG-E2003-ITG, which proves the same values across rwb-integration, rwb-source-data and rwb-access end to end.

### 17. Guardrails

- No business value in code: the roster of roles, the field ID `DF-ACE-281`, the marker names, the masking version and the validity dates are rows of `masking_rule` and values of LOV-CAPABILITY read through DP-07. No role code, field ID or version appears in Java (BR1).
- No personal data in events, logs, tests or prompts. This story answers field IDs, markers and version labels, and it writes no record and no event; test data is synthetic (`RW-2026-000410`, `C-0410`, `9900015678`, `XXXXXX5678`) and staff appear as user references only.
- ACE data only through the owner's contract or the owner's `v_ace_*` views — and this story reads neither: `rwb-access` holds no grant on `recovery`, reads no `v_ace_party_product` row and holds no account number, and the product read stays with rwb-source-data and rwb-integration (BR3, BR9).
- No cross-schema read: `rwb_access` holds no foreign key into another schema and no copy of a case, product or ACE row (DP-01).
- The refusal comes before the masking answer, so a refused caller learns nothing about the field and nothing about the case (BR5, BR6).
- The switch fails closed: off answers masked for every role and never opens a field, and it needs no schema rollback.
- One writer for the masking catalogue: this story writes the rows of its own field through its migration, and every later roster or version change goes through the load path of RWB-P4-AD004-APP, so an answer and the rows it names cannot disagree.
- Not an event, not a record: the access entry of the read is the caller's PII access event to ACE Common on INT-22, and this service publishes and consumes nothing for this capability (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-003 | Customer, product and account facts reach the case from ACE, read through `v_ace_customer`, `v_ace_party_product` and `v_ace_account` (DL20 as amended by D-RCV-35) | Program 5.3; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | BR8, BR9 | TC-E2-003-01, TC-E2-003-04 |
| REQ-RDF-010 | Access to each data product is controlled per role, and personal data is masked by role in line with PDPA | Program 5.1; Epic 2 3.2 | FEAT-CHO-03; FEAT-ACA-05 | 06 Take over and own the case | BR1, BR2, BR3, BR4, BR5 | TC-E2-003-03, TC-E2-003-07 |
| REQ-RDF-009 | Every data product carries a freshness stamp, and every decision records the freshness of the data it used | Program 5.1; Epic 2 3.2 | FEAT-CHO-03 | 06 Take over and own the case | BR7 | TC-E2-003-02 |
| REQ-CHO-010 | A duplicate case for the same customer and product merges into the earlier case, carrying its documents and decision log | Program 5.3; Epic 2 3.2 | None in this slice | 06 Take over and own the case | None | None; carried by the legacy key and out of scope (section 19) |

The supporting features of this slice are FEAT-ACA-05 (mask PDPA fields by role) and FEAT-ACA-07 (every access event to the access log), which the FSD P4 module pairs with RWB-E1-037 and RWB-E1-039; this slice answers FEAT-ACA-05 for one field of one panel and changes neither the matrix design nor the access-log design.

| Legacy reference | Where it is kept |
|---|---|
| The roster of clear roles and the last-four default, marked "assumed; DL26" | Sections 1, 3, 8, 10, 13; ASM-1632 |
| Account number masking (legacy AC3) and the product fields of section 11 | Sections 7, 8, 11 |
| The refusal of a role without the Case record right (legacy TC-E2-003-07) and the out-of-scope answer (legacy AC5) | Sections 4, 5, 7, 14 |
| MSG-P1-001, MSG-P4-002, MSG-P4-003 | Section 14 and the exception paths |
| The PII access event of BR5 and INT-22 | Sections 1, 4, 8, 12, 17 |
| Legacy key RWB-E2-003, story RWB-P4-E2003-APP, contract RWB-P4-E1037-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The rwb-integration slice of this legacy key, RWB-P2-E2003-APP: the endpoint `GET /api/recovery/integration/v1/cases/{caseId}/customer-products`, the product read, the exclusion of the accounts already on the case, the freshness check, the stale marker MSG-P1-001, the empty state MSG-P2-017 and the PII access event on INT-22.
- The ACE views behind the read, the grants and the boundary rule: RWB-P1-E1069-APP, with `v_ace_party_product` in V0003 (DL43) and the thirty `recovery.v_ace_*` views of ADR-010.
- The parties of the case and the accounts linked to it: rwb-case, read through its contract by RWB-P2-E2003-APP and never from `recovery_case` or `case_account`.
- SCR-03 Case record, the other products panel, its layout, its loading, stale and empty states, and the gateway-bff composite route's field list: RWB-P3-E1023-APP, RWB-P2-E2003-APP and RWB-PLT-N001-CON.
- The end-to-end proof of these values across rwb-integration, rwb-source-data and rwb-access: RWB-ITG-E2003-ITG.
- Loading, approving and rolling back a masking profile through the administration screens and the reference loads: RWB-P4-AD004-APP and RWB-P4-AD002-APP; the matrix as a whole and its masking design: RWB-P4-E1037-APP.
- The decision-record path of an authorise call, the access-log search and export, the break-glass grant and the access review list: RWB-P4-E1037-APP, RWB-P4-E1039-APP, RWB-P4-AD006-APP to RWB-P4-AD008-APP.
- The delegation of authority table and its lookup (RWB-P4-E2013-APP), the DoA-limits operation and `rwb.access.DoALimitChanged.v1`.
- Merging a duplicate case for the same customer and product (REQ-CHO-010, R-UNI-17): Epic 3 backlog.
- Balances of the other products: the customer product holding carries the product type and status only (DL20).
- The `rwb_access` schema baseline, the topic and queue provisioning, the Helm chart, the metrics, the alerts and the runbook of this capability.
