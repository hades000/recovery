# RWB-P4-E1069-APP Read-only ACE source views, grants and boundary rule

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1069-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-069 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP15, DP19 |
| Parallel lane | L-P4-AC |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P4-E1037-CON (rwb-access operations of section 12.1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-RDF-002, REQ-DRI-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-069 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E1069-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 28 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM), a reference data administrator (RW-REFADM) and a compliance and PDPA officer (RW-COMPLY)**, I want **the masking rows for the ACE-sourced personal fields held as data at the masking version in force, the masking answer served on the authorise decision that a source-data read takes before it returns an ACE-sourced field, and boundary rule BND-6 applied to the rwb-access package so that no class of this service names a `v_ace_*` view or a `public` table**, so that **rwb-access enforces the read-only ACE boundary on itself and answers the masking question for every caller while it reads no ACE data at all**.

### 2. Business rationale

Only rwb-source-data reads the 30 read-only `recovery.v_ace_*` views (Architecture v5 slides 8, 9 and 41; ADR-010). Every other service, and every agent, asks for source data through rwb-source-data's contract, so the boundary is enforced in two places: the catalog, where the other 18 logins hold no privilege on the views and nothing in `public`, and the build, where boundary rule BND-6 fails a class that names a `public` table (legacy RWB-E1-069 BR1, BR3 and BR8). rwb-access owns the third piece: Recovery roles as data, scope, the masking policy and the DoA table (Architecture v5 slide 41), and it serves `POST /authorise`, `GET /me/permissions`, `GET /doa-limits` and `/masking-policies` (slide 14). It therefore holds the policy that masks the ACE-sourced personal fields and never the fields themselves: the `masking_rule` rows are keyed by the field IDs of the views, which is metadata about a field, not a read of it. This story is the rwb-access slice of legacy RWB-E1-069.

The legacy story enforces the boundary on one module with two grants and one build rule. In the target, that legacy key splits across five stories. RWB-P1-E1069-DB creates the per-service login, the grants and the four extension tables in the owner's schema; RWB-P1-E1069-APP writes the per-service Flyway sequence that creates the views in rwb-source-data's read path and runs the conformance test; RWB-ITG-E1069-ITG proves the grant model across the 19 logins end to end; and this story carries the policy side plus the boundary applied to rwb-access's own package. This slice re-specifies no view definition, no grant statement and no extension-table column: it keys the masking rows on the field IDs the dictionary publishes, answers the masking question on the authorise contract, and fails its own build on a view read or a `public` read. It meets REQ-RDF-002 (account, arrears and payment facts read from ACE through the views) by making the personal fields of those reads maskable by role, and REQ-DRI-006 (no component calls a system of record directly) by making a direct read in this service impossible to merge.

The policy pack this slice writes is the ACE-sourced slice of the masking version: one `masking_rule` row per field ID and role, `unmasked` true only where a role may see the field, and the last-four answer for every other role. The field IDs the pack must cover, the masking version label and the roster of roles that see a field unmasked are Not specified in the source documents (GAP-0901; ASM-1622), (GAP-0902; ASM-1623) and (GAP-0903; ASM-1624); the story covers `DF-ACE-055` to `DF-ACE-074`, the 20 fields of `v_ace_customer`, at masking version `MASK-2026.12`, and treats an `unmasked` true row as the only allow.

### 3. Preconditions

- RWB-P4-E1037-APP delivered the `rwb_access` baseline: the tables `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` exist with their dictionary rows (DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204, DF-REF-205 to DF-REF-211, DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062), and RWB-P4-E1037-CON published the authorise and masking operations this story answers behind.
- The local decision-record library and the topic `rwb.decision-record.v1` are live (DP-03, EV-08), so the masking answer of an authorised read can be recorded before it is returned.
- The build-rule harness of the service template is in the repository: the target form of legacy RWB-TE-001's `RecoveryBoundaryTest`, which reads its allowed source objects from a module map in the service and runs on every merge.
- The field catalogue exists in P1's dictionary: `sys_objects` and `sys_fields` hold `DF-ACE-055` to `DF-ACE-074` for `v_ace_customer`, with `DF-ACE-073` as `id_no_masked` and `DF-ACE-074` as `id_no_last4`. rwb-access reads neither table and holds no dictionary row of its own (GAP-0905; ASM-1626).
- The masking pack file for version `MASK-2026.12` is prepared by RW-REFADM and approved by RW-SECADM through the load path, and this story's migration applies the rows of its ACE-sourced slice. That the version label is `MASK-2026.12` is Not specified in the source documents (GAP-0902; ASM-1623).
- The roster of roles that see a given field unmasked is not held by any source document; the pack file fixes it as data, and the story treats every role without an `unmasked` true row as masked (GAP-0903; ASM-1624).
- The parameters contract of rwb-case and its client library are live (DP-06), for the feature switch of the masking answer; the reference-data contract of rwb-case is live for LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE (DP-07).
- The login is the rwb-access login (DP-02). The per-service login name is Not specified in the source documents (GAP-0904; ASM-1625).
- The 30 `recovery.v_ace_*` views exist in schema `recovery` and are owned and granted by RWB-P1-E1069-DB; this story neither creates, alters nor grants on them, and it asserts only that its own login holds nothing there.
- The login creation and the per-schema grants are those of RWB-PLT-NF06 (19 schemas and logins) and RWB-PLT-N011 (migrator roles); the legacy placeholders `:recovery_role` and `:ace_view_owner` are not carried as role names (GAP-0111).
- The masking answer for an ACE-sourced field is the rwb-access authorise decision, applied by rwb-source-data; until the Service Contract Catalog records this, the Contract dependencies row stays as the Work Package fixes it (GAP-0554).

### 4. Flow

1. RW-REFADM prepares the masking pack file for version `MASK-2026.12` and RW-SECADM approves it on the load path: one row per field ID and role, `unmasked` true only where a role may see the field, and every other role absent (BR1, BR2).
2. rwb-access: the migration Not specified in the source documents (CG-ALL-5129) writes the rows for the field IDs `DF-ACE-055` to `DF-ACE-074` into `masking_rule` in schema `rwb_access`, each with `masking_version` `MASK-2026.12` and a `valid_from` date; it copies no value of any field and no ACE row (BR3).
3. rwb-access: the version becomes visible to the read that resolves the version in force; a later version is loaded, approved and dated, and the previous rows stay readable with their `valid_to` (BR4). This slice runs no relay: DP-09 is not a pattern of this story (section 12.3).
4. rwb-source-data holds an ACE-sourced field for a caller and calls `POST /api/recovery/access/v1/authorise` with the caller identity from the session, the capability area, the right, the case reference and the field IDs it is about to return (DP-08, DP-11).
5. rwb-access: reads the caller's roles and the letters of the area from `role` and `permission` at the matrix version in force, and applies the scope and default-deny rules of RWB-P4-E1037-APP; no role code, area or letter is written in code (BR5).
6. rwb-access: resolves the masking answer per field ID from `masking_rule` at the masking version in force — `clear` only where a row for a role the caller holds, that field ID and that version says `unmasked` true, `masked` otherwise, including where no row exists (BR6, BR7).
7. rwb-access: the answer names the decision code, the matrix version, the masking version and a marker per field ID; it carries no value, clear or masked, and no last four digits (BR8).
8. rwb-access: the access entry is written through the decision-record library first, in the same transaction as the answer, with the field IDs and the markers only; a write that fails returns 503 MSG-P7-003 and no masking answer (BR9).
9. rwb-source-data returns the field masked or clear as answered; rwb-access has read no view, no `public` table and no other schema at any step of the flow (BR10).
10. Build: boundary rule BND-6 runs over the module map of the service on every merge, and a class of `th.co.scb.ace.workbench.recovery.access` that names a `v_ace_*` view or a `public` table fails the build (BR11).
11. Deploy: the rwb-access login holds no SELECT on any of the 30 views and no privilege of any kind in `public`; the proof across all 19 logins is RWB-ITG-E1069-ITG, and this story asserts the two facts for its own login in its own test (BR12).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A requested field ID has no `masking_rule` row at the version in force | The field is answered masked; the decision itself is unchanged and no value is returned | None | AC4 |
| X2 | The caller holds no Workbench role at all | The call is refused before any masking answer is resolved | MSG-P4-001 | AC6 |
| X3 | The area or the right is absent for the caller's roles | The call is refused and no field ID is answered clear, so no masking version is named | MSG-P4-002 | AC6 |
| X4 | A class of the package names `recovery.v_ace_customer` | The build fails with boundary rule BND-6 and the class is named; nothing merges | Build log | AC7 |
| X5 | A class of the package names `public.customer` | The build fails with boundary rule BND-6 and the class is named; the fix is rwb-source-data's contract | Build log | AC7 |
| X6 | The masking version in force holds a gap for a personal field ID | The field stays masked and the gap is raised to RW-COMPLY naming the field ID and the version | None | AC4 |
| X7 | The access entry cannot be written | The answer is 503 and no masking answer is returned; an incident is raised | MSG-P7-003 | AC5, AC9 |
| X8 | The migration is applied a second time | Flyway reports the version as already applied; no row is written twice and no version is edited in place | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_access` baseline and the RWB-P4-E1037-CON fake; the views, the grants and the dictionary belong to the P1 stories and are not prerequisites of this build |
| Negotiable | The field-ID range, the masking version, the roster of unmasked roles and the feature switch are data rows and parameters; the story fixes the answer rule and the build rule only |
| Valuable | The personal fields of every ACE read are maskable by role from one place, and a direct view read inside this service cannot be merged |
| Estimable | One migration, one masking resolver, one build rule, one module map and one contract-fake path |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test with a synthetic fixture; no ACE data is needed |

### 7. Acceptance criteria

```gherkin
Feature: The ACE-sourced masking pack and the read-only boundary of rwb-access

  Background:
    Given the policy pack version "PM-2026.12" is in force in "permission"
    Given masking version "MASK-2026.12" is in force in "masking_rule"
    Given the field IDs of the ACE-sourced customer view are "DF-ACE-055" to "DF-ACE-074", with "DF-ACE-073" as "id_no_masked" and "DF-ACE-074" as "id_no_last4"

  Scenario: AC1 The masking pack covers the ACE-sourced customer field IDs (new, D-RCV-60)
    Given the masking pack file for version "MASK-2026.12" holds one row per field ID from "DF-ACE-055" to "DF-ACE-074" and per role of the pack
    When the migration "V1069_1__ace_masking_pack.sql" is applied to schema "rwb_access"
    Then "masking_rule" holds one row per field ID and role, each with masking_version "MASK-2026.12", an unmasked flag and a valid_from date
    And every row names a field ID of the customer view and no extension-table field ID "DF-EXT-001" to "DF-EXT-049"
    And the migration writes no value of any field and no copy of an ACE row
    When the same version is applied a second time
    Then Flyway reports it as already applied and no row is written twice

  Scenario: AC2 The last-four default for every role without an allow row (new, D-RCV-60)
    Given the pack holds no row with unmasked "true" for role "RW-CASEOWN" and field "DF-ACE-074"
    When the caller holding only "RW-CASEOWN" asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and field IDs "DF-ACE-073" and "DF-ACE-074"
    Then the answer marks "DF-ACE-073" and "DF-ACE-074" "masked" under masking version "MASK-2026.12"
    And the answer carries no identity number, no last four digits and no value of either field
    And the clear identity number is unreachable from this service, because the view carries "id_no_masked" and "id_no_last4" only

  Scenario: AC3 An allow row makes the field clear for the named role (new, D-RCV-60)
    Given the pack holds unmasked "true" for role "RW-COMPLY" and field "DF-ACE-074" at version "MASK-2026.12"
    When a caller holding "RW-COMPLY" asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and field ID "DF-ACE-074"
    Then the answer marks "DF-ACE-074" "clear" and names masking version "MASK-2026.12"
    And the answer still carries no value; the value is returned by rwb-source-data under its own contract
    When a caller holding only "RW-CASEOWN" asks for the same field
    Then the answer marks "DF-ACE-074" "masked" under the same version, and no other row changes

  Scenario: AC4 A personal field with no masking row is masked (new, D-RCV-60)
    Given no "masking_rule" row covers field "DF-ACE-059" for any role at version "MASK-2026.12"
    When any caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and field ID "DF-ACE-059"
    Then the answer marks "DF-ACE-059" "masked"
    And a gap alert is raised to RW-COMPLY naming field ID "DF-ACE-059" and masking version "MASK-2026.12"
    And no value and no date of birth is returned

  Scenario: AC5 The masking answer names the version and carries no value (new, D-RCV-60)
    Given the caller holds "RW-AUDIT" with scope "ALL"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and field IDs "DF-ACE-073" and "DF-ACE-074"
    Then the answer holds the decision code "AC-READ", matrix version "PM-2026.12", masking version "MASK-2026.12" and one marker per field ID
    And the marker is "masked" or "clear" and is never a value, a masked rendering or a last four digits
    When the access entry cannot be written
    Then the call answers 503 with message MSG-P7-003 and no marker and no version is returned

  Scenario: AC6 A caller with no right is refused before any field is answered (new, D-RCV-60)
    Given the caller holds only "RW-PHONECOL", whose CASE_RECORD letters are "-" in "PM-2026.12"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and field ID "DF-ACE-073"
    Then the call is refused with status 403 and message MSG-P4-002
    And no field ID is answered clear and no masking version is named
    And one access entry is written with decision code "AC-DENY", area "CASE_RECORD", right "R", field ID "DF-ACE-073" and result "REFUSED"

  Scenario: AC7 Boundary rule BND-6 fails the build on a view read and on a public read (new, D-RCV-60)
    Given a fixture class "th.co.scb.ace.workbench.recovery.access.policy.CustomerReader" in the boundary test fixtures only, never in the production build, with a query on "recovery.v_ace_customer"
    When the pipeline runs the boundary rule of the rwb-access build
    Then the build fails with boundary rule BND-6, "CustomerReader" and "recovery.v_ace_customer"
    When the class names "public.customer" instead
    Then the build fails with boundary rule BND-6, "CustomerReader" and "public.customer"
    When the class asks GET /api/recovery/source-data/v1/customers/{id} through the rwb-source-data contract
    Then the build passes
    And the view names the rule allows are read from the module map of the service, not written in the rule
    And the module map of rwb-access holds no allowed source view, because this service reads none

  Scenario: AC8 The rwb-access login holds no view privilege and no privilege in public (new, D-RCV-60)
    Given the rwb-access login exists and the 30 "recovery.v_ace_*" views exist in schema "recovery"
    When a session as the rwb-access login selects from "recovery.v_ace_customer"
    Then the statement fails with SQLSTATE 42501 "permission denied for schema recovery"
    When the same session selects from "public.customer"
    Then the statement fails with SQLSTATE 42501 "permission denied for schema public"
    Then has_table_privilege(login, 'recovery.v_ace_customer', 'SELECT') is false for each of the 30 view names
    Then has_schema_privilege(login, 'public', 'USAGE') is false and has_schema_privilege(login, 'recovery', 'USAGE') is false
    Then the login holds privileges in schema "rwb_access" only

  Scenario: AC9 The access entry names field IDs and no value (new, D-RCV-60)
    Given a caller holding "RW-AUDIT" with scope "ALL" reads a case whose screen names field IDs "DF-ACE-073" and "DF-ACE-074"
    When the masking answer for that read is served
    Then one access entry is written with decision code "AC-READ", the actor, the case ID, area "CASE_RECORD", right "R", field IDs "DF-ACE-073" and "DF-ACE-074", masking version "MASK-2026.12" and decided at
    And the entry holds no identity number, no last four digits, no name, no date of birth and no address, only the IDs and the field IDs
    And the entry is a decision-record entry written through the local decision-record library (EV-08), and this slice publishes no event of its own

  Scenario: AC10 The feature switch off masks every ACE-sourced field, and only the approved pack file sets the roles (new, D-RCV-60)
    Given the feature switch for the ACE-sourced fields is read as a parameter and is off
    And the pack holds unmasked "true" for role "RW-COMPLY" and field "DF-ACE-074" at version "MASK-2026.12"
    When a caller holding "RW-COMPLY" asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and field ID "DF-ACE-074"
    Then the answer marks "DF-ACE-074" "masked" under masking version "MASK-2026.12"
    And no "masking_rule" row is written or changed by this service; the rows arrive by load of the approved pack file only

  Scenario: AC11 A request with no valid session, or to an absent path, is answered 401 or 404 and returns no field (new, D-RCV-60)
    Given a request to POST /api/recovery/access/v1/authorise carries no valid session
    When the request asks for area "CASE_RECORD", right "R" and field ID "DF-ACE-073"
    Then the call answers 401 with message Not specified in the source documents (NEWAC-RWB-P4-E1069-APP-AC11); section 12.1 names MSG-P4-001 only for a caller with no Workbench role
    And no field ID is answered and no masking version is named
    When the caller asks for a path of the rwb-access operations of section 12.1 that does not exist
    Then the call answers 404 with message Not specified in the source documents (NEWAC-RWB-P4-E1069-APP-AC11)
    And no value and no marker is returned
```

The eleven criteria above are new and test only this deliverable: the masking rows of the ACE-sourced fields, the masking answer on the authorise decision, and the boundary of this service. The legacy criteria of RWB-E1-069 are owned elsewhere: AC1 to AC3 (the 16 and 14 view sets and their compilation) by RWB-P1-E1069-DB and RWB-P1-E1069-APP, AC4 and AC7 (the constraint rule and the four extension tables) by RWB-P1-E1069-DB, AC5 and AC6 (the dictionary rows and the delay-day mapping) by RWB-P1-E1069-APP, and AC8 (the boundary test) here and in RWB-ITG-E1069-ITG. No legacy criterion text is copied into this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The masking rows are data with a version: one row per field ID and role, `unmasked` true only where a role may see the field. No role code, field ID or masking version is written in Java | FSD P4 A2.5; BR-P4-005; TSD P4 T3.1 (`masking_rule`) |
| BR2 | Which roles see a given field unmasked is set by the pack owner, not by this story; the rows arrive by load and by this story's migration of the approved file | FSD P4 A2.5; TSD P4 T3.1 |
| BR3 | A `masking_rule` row names a field ID and the masking version; it never carries a value, a rendering of a value or a copy of an ACE row | TSD P4 T3.1 (DF-REF-198 to DF-REF-204); FSD P1 BR-P1-001-6 |
| BR4 | A version is never edited in place: a change is a new masking version with its `valid_from`, and the previous rows stay readable with their `valid_to` | FSD P4 A2.4 AC-EXC-P4-004-02; TSD P4 T3.2 (LOV-VERSION-STATUS) |
| BR5 | The decision is refused before any masking answer where the caller holds no role, or where the area or the right is absent (default deny) | FSD P4 A2.4; VR-P4-004-1; MSG-P4-001 and MSG-P4-002 |
| BR6 | A field is `clear` only where a `masking_rule` row for a role the caller holds, that field ID and the masking version in force says `unmasked` true; the union of the caller's roles applies | FSD P4 A2.5; TSD P4 T3.1 |
| BR7 | A personal field with no covering row is `masked`, never `clear`; a gap in the pack masks and is alerted, and never opens a field | FSD P4 AC-EXC-P4-004-05; NFR-039 |
| BR8 | The answer carries a marker, the matrix version and the masking version; it never carries a value, a masked rendering or the last four digits of a field | FSD P4 A2.5; NFR-039; NFR-040 |
| BR9 | The access entry is written first, in the same transaction as the answer, through the local decision-record library; a failed write means 503 and no answer | FSD P4 A2.7 AC-EXC-P4-007-03; R-UNI-39; DP-03 |
| BR10 | rwb-access reads no ACE table, no `v_ace_*` view and no other service's schema: the field IDs are keys into its own policy, and the values are returned by rwb-source-data | Architecture v5 slides 8, 9 and 41; DP-01; DP-05 |
| BR11 | Boundary rule BND-6 fails the build in two parts: no class of `th.co.scb.ace.workbench.recovery.access` names schema `public`, and no class of that package names a `v_ace_*` view or another service's schema; the allowed object list is read from the module map, and it is empty for this service | Legacy RWB-E1-069 BR8 and AC8; REQ-DRI-006; RWB-TE-001 |
| BR12 | The rwb-access login holds no SELECT on any of the 30 views and no privilege of any kind in `public`; PUBLIC holds nothing on the views. Its login name is Not specified in the source documents (GAP-0377), to be taken from Environment and Deployment Design when issued | Legacy RWB-E1-069 BR3; ADR-010; DP-02 |
| BR13 | The clear identity number never leaves ACE: the customer view returns `id_no_masked` (`DF-ACE-073`) and `id_no_last4` (`DF-ACE-074`), so no masking row of this pack can open it | FSD P1 BR-P1-001-6; TSD P1 T3.1 (DF-ACE-073, DF-ACE-074) |
| BR14 | The feature switch is read as a parameter; off means every ACE-sourced field is answered masked, never clear | FSD P4 A2.5; DP-06 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| masking rows of a version in force | a new masking version is loaded, approved and in force | The pack is approved and carries a later `valid_from` | The new version is in force; the previous rows stay readable with their `valid_to` |
| a personal field ID with no covering row | an authorise request | Any role, any masking version | The field stays `masked`; the pack gap is alerted |
| a class of the service naming a `v_ace_*` view or a `public` table | the build | The rule sees the reference | The build fails with BND-6; no artifact is produced |

rwb-access holds no case state machine of its own (TSD P4 T4): the case, the treatment and the task states move in rwb-case and rwb-treatment, and this story neither reads nor writes them. The masking version moves from LOADED to APPROVED to IN_FORCE to SUPERSEDED or ROLLED_BACK on the load path (TSD P4 T3.2 LOV-VERSION-STATUS); this story reads the version in force and writes the rows of its own approved slice.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Serves the masking answer, writes the pack rows by migration, runs the boundary rule and writes the access entry |
| RW-REFADM, reference data administrator | Prepares the masking pack file for a version; no approval, no upload into another service and no rollback |
| RW-SECADM, security administrator | Approves a masking version; holds CRUDA in Platform administration (TSD P4 T6.1) |
| RW-COMPLY, Compliance and PDPA officer | Reads which masking version is in force and which field IDs it covers, through `GET /masking-policies`; receives the pack-gap alert |
| RW-AUDIT, internal audit | Reads the masking version, the rows and the access entries |
| RW-CASEOWN, RW-PHONECOL and every other business role | Reads the masked or clear marker of a field they are entitled to ask about; may not change a row, a version or the roster |
| ACE view owner and ACE DBA | Not this story: the views and the grants stay with RWB-P1-E1069-DB and RWB-ACE-001 |
| No approval level from the delegation of authority applies | The story takes no business decision |

The per-service login name is Not specified in the source documents (GAP-0904; ASM-1625); the story names it "the rwb-access login (DP-02)" until the platform DB story fixes it. The roles above are rows of the pack and of `role`; no role grants itself a row, and no role code is fixed in code.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Write (the rows of this story's migration); Read |
| DF-REF-034 to DF-REF-039 | `role` | role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | role_code, conflicts_with, conflict_version | Read; no row changes here |
| DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | `delegation_limit` | decision_code, approval_level, limit_version | Read; no row changes here |
| DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | access entry (local decision record) | decision code, actor, case ID, actions, decided at, hash chain, idempotency key | Write |
| DF-DEC-014 | access entry (local decision record) | actions (area, right, field IDs, marker, masking version) | Write |
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` (keyed by field ID, never read) | `cif_no` to `id_no_last4`, 20 fields | Not read and not written; named as `field_id` keys only |
| DF-ACE-073 and DF-ACE-074 | `v_ace_customer` (keyed by field ID, never read) | `id_no_masked`, `id_no_last4` | Not read and not written; the pair that means the clear identity number is unreachable |
| DF-ACE-059 | `v_ace_customer` (keyed by field ID, never read) | `date_of_birth` | Not read and not written; the no-row case of AC4 |

No ACE row, no view column and no other service's row is copied into `rwb_access`: a `masking_rule` row names a field ID and a version, and nothing else. The clear identity number never leaves ACE, because the view returns `id_no_masked` and `id_no_last4` and no masking row of this pack can open it (BR13). The field-ID range the pack must cover, and whether rwb-access may hold rows that reference the P1 field catalogue at all, are Not specified in the source documents (GAP-0901; ASM-1622) and (GAP-0905; ASM-1626); the story keys its rows on the field IDs and holds no dictionary row. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The three operations of RWB-P4-E1037-CON (contract version Not specified in the source documents (DOR-RWB-P4-E1069-APP-23)) on base `/api/recovery/access/v1` are served by this service, and this slice delivers the masking resolution behind two of them. It adds no path, no query parameter and no response field:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/authorise` | Decide a role's read or action for a capability area, a case and a field list, and answer the mask of each field ID with the masking version | Any authenticated caller with a Workbench role | Idempotent by identity, area, right, case reference and field list within the cache window |
| GET | `/me/permissions` | The caller's resolved roles, scope, matrix version and masking version | Authenticated caller, own record only | Not applicable |
| GET | `/masking-policies` | The masking rows in force for a role and a field list: the marker per field ID and the version | Authenticated caller | Not applicable |

Request for `/authorise`: the caller identity from the session, the capability area, the right, the case reference and the field IDs. Answer: the decision code (`AC-READ` or `AC-DENY`), the matrix version, the masking version and a marker per field ID (`masked` or `clear`); the response field names are Not specified in the source documents (GAP-0901; ASM-1622). Errors: 401 no Workbench role (MSG-P4-001), 403 no letter for the area or right (MSG-P4-002), 404 case absent or out of scope (message ID Not specified in the source documents (CG-ALL-5123)), 503 access entry unwritable (MSG-P7-003).

The role read, the session read, the access-log search, the DoA read and the load paths are P4 surface delivered by other P4 stories (RWB-P4-E1037-APP, RWB-P4-E1039-APP, RWB-P4-E2013-APP, RWB-P4-AD002-APP); this story adds none of them.

#### 12.2 REST operations consumed

None. At run time rwb-access calls no service: the caller's identity arrives in the session, the case attributes for the scope test arrive in the request, and the parameters and reference-data values reach it through the client libraries of rwb-case (DP-06, DP-07). The one hop and the 2 s budget of DP-11 apply to the inbound call.

#### 12.3 Events published

None. This slice applies no DP-09 pattern and holds no relay of its own: the masking answer of an authorised read is a decision-record entry written through the local decision-record library (DP-03), whose payload is EV-08 on `rwb.decision-record.v1` and which the library publishes. This story adds no event, no topic and no outbox row of its own, and the access log is never a Kafka event of this service.

#### 12.4 Events consumed

None. The masking version in force is read from `rwb_access` on each call; no topic is consumed here.

#### 12.5 Workflows and activities

None. The masking answer is a synchronous REST answer in the caller's thread. The six-monthly access review list (JOB-18) belongs to RWB-P4-AD008-APP (Architecture v5 slide 44), and this story starts no workflow and no activity.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `role` | P4 (`rwb_access`) | Recovery roles as data; read here, no row written |
| `permission` | P4 (`rwb_access`) | Capability area, letters and matrix version; read here, no row written |
| `masking_rule` | P4 (`rwb_access`) | Which role sees which personal field unmasked, by masking version; the rows of the ACE-sourced slice are written by this story's migration |
| `role_conflict` | P4 (`rwb_access`) | Conflicting role pairs; read, no row written |
| `delegation_limit` | P4 (`rwb_access`) | DoA limits; read, no row written |
| access entry (local decision record) | P4 rows in `rwb_access`, written through the P7 decision-record library | The `AC-READ` and `AC-DENY` entries with the field IDs and the markers (DP-03) |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09); this slice writes none of them |

No table of another service and no `v_ace_*` view is read and no foreign key crosses a schema (DP-01). The dictionary rows (`sys_objects`, `sys_fields`) stay with P1, and no `v_ace_*` object is created, altered or granted here.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P4-E1037-CON fake | The authorise and masking operations | A granted read, a refused read and a no-row field, each with the masking answer |
| field-ID catalogue fixture | The P1 dictionary (`DF-ACE-055` to `DF-ACE-074`) | The 20 field IDs of `v_ace_customer` with `DF-ACE-073` as `id_no_masked` and `DF-ACE-074` as `id_no_last4`; no value and no row of ACE data |
| decision-record library stub | DP-03 | A healthy chain and a stopped chain for the 503 path |
| parameters and reference-data fakes | DP-06, DP-07 | The feature switch and LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE |
| rwb-source-data contract fake | ACE-sourced field values returned by rwb-source-data (BR10) | Not specified in the source documents (CG-ALL-5130) |

The request and answer field names of `/authorise` are stubbed from the published fixture of RWB-P4-E1037-CON; their list is Not specified in the source documents (GAP-0901; ASM-1622).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 new provided, 0 consumed | The masking answer is served on the three RWB-P4-E1037-CON operations on `/api/recovery/access/v1`; no path is added and no outbound call is made |
| Kafka | 0 published, 0 consumed | DP-09 is not applied; the access entry is a decision-record library write (EV-08) and no topic is added or consumed here |
| Temporal | None | No workflow and no activity |
| File | None | The pack file is read at load time by the load path, not at run time here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.policy`, module `policy`, in the service root `th.co.scb.ace.workbench.recovery.access`. The boundary rule lives in the test source tree of the same service, beside the template harness.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own, and the metadata rows "Depends on (build)" and "Contract dependencies" stay exactly as this Work Package fixes them, with the platform contract libraries and DP-08's `RWB-PLT-E1037-CON` and `RWB-P4-E1037-CON` arriving with the baseline and its contract story. DP-05 applies as a prohibition for this service (no ACE view is read here, and the boundary rule enforces it), DP-11 as the inbound budget of the authorise call, and DP-19 as the screen route behind SCR-43 and SCR-47, which this story does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V1069_1__ace_masking_pack.sql` | Migration | Writes the `masking_rule` rows of the ACE-sourced field IDs at `MASK-2026.12`; copies no value |
| MaskingRepository | Repository | Reads `masking_rule` by `field_id`, `role_code` and `masking_version`; reads no other schema |
| MaskingAnswerResolver | Service | Unions the caller's roles, answers `clear` only on an `unmasked` true row and `masked` otherwise, and names the version |
| MaskingControllerPart | Controller contribution | Wires the resolver behind `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` of RWB-P4-E1037-CON; adds no path |
| PackGapAlerter | Service | Raises the gap alert to RW-COMPLY for a personal field ID with no covering row |
| AccessEntryWriter | Service | Writes the access entry with the field IDs and the markers, first in the transaction, through the decision-record library |
| AceBoundaryRule | ArchUnit rule in the test source | BND-6 over the module map: a class of the package names no `v_ace_*` view and no `public` table |
| `access-modules.yaml` | Rule table | The package name and the allowed source object list, which is empty for this service |

**Database and migrations**

- Reads `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` in schema `rwb_access`; writes the access entry of the decision-record library.
- Migration in this story: `V1069_1__ace_masking_pack.sql` writes the rows for `DF-ACE-055` to `DF-ACE-074` at masking version `MASK-2026.12`. It adds no index: the read is covered by the baseline index on `masking_rule (role_code, field_id, masking_version)`, and this story repeats it in no table.
- The tables arrive with the `rwb_access` baseline, and no column is added. No row of `role`, `permission`, `role_conflict` or `delegation_limit` is written by this story; the matrix is loaded by RWB-P4-AD002-APP and the DoA rows by RWB-P4-E2013-APP.
- No `v_ace_*` object and no `public` object is created, altered or granted: the tables and grants of the legacy key belong to RWB-P1-E1069-DB, and the migration text belongs to RWB-P1-E1069-APP.

**Configuration and reference data**

- The masking version in force: `MASK-2026.12`, the label this Work Package fixes. That no source names the label is Not specified in the source documents (GAP-0902; ASM-1623).
- The covered field IDs: `DF-ACE-055` to `DF-ACE-074`. Which ACE view fields the pack must cover is Not specified in the source documents (GAP-0901; ASM-1622).
- The roster of unmasked roles: set by the pack owner in the pack file, with no row meaning masked. That no source holds the roster is Not specified in the source documents (GAP-0903; ASM-1624).
- The allowed source object list of `access-modules.yaml` is empty for this service, and the 30 view names are not copied into it. A class may name rwb-source-data's contract only.
- The feature switch is `rwb.access.ace-masking-answer`, read as a parameter through the parameters contract (DP-06): off answers every ACE-sourced field masked and allows nothing clear.
- The login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0904; ASM-1625).

**Build steps**

1. Migration `V1069_1__ace_masking_pack.sql` with the rows of the ACE-sourced slice and a failing fixture for a duplicated field ID and role; tests for AC1.
2. MaskingRepository and MaskingAnswerResolver with the union of the caller's roles and the no-row default; tests for AC2 and AC3.
3. The no-row path with the gap alert, and the refusal paths (no role, no letter) ordered before any masking answer; tests for AC4 and AC6.
4. The answer shape with the version and the marker only, and the 503 when the entry cannot be written; tests for AC5.
5. AccessEntryWriter with the field IDs and the markers on the entry, and no value; tests for AC9.
6. AceBoundaryRule and `access-modules.yaml` with a fixture class on `recovery.v_ace_customer`, the same class on `public.customer`, and the same class on the rwb-source-data contract; tests for AC7.
7. The privilege test of AC8 as a container test with a session as the rwb-access login against the 30 view names.
8. A contract-fake run of the whole path, so the story builds before rwb-source-data and the load path are live.

**Feature switch.** `rwb.access.ace-masking-answer`, read as a parameter; off answers every ACE-sourced field masked and still fails the build on a view or `public` read.

**Done when.** The tests in section 16 pass, `masking_rule` holds the rows of `MASK-2026.12`, the authorise answer names the masking version for every field ID, the build is green and red on the two fixtures of the boundary rule, and a session as the rwb-access login holds no privilege on any of the 30 views and none in `public`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | The token holds no Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | The area or the right is absent for the caller's roles | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Build log | A class names a `v_ace_*` view or a `public` table | Boundary rule BND-6 broken: {class} names {object}. A recovery class names no ACE view and no public table. |
| Privacy Kafka | A pack fails its scope check; no value and no identity number is carried | ACE PII logging path (INT-22) |

For MSG-P4-002 in this story, {action} names the action the caller tried — for example "read the customer identity number" — and never a case fact or a field value. The build-log wording is Not specified in the source documents (GAP-0906; ASM-1627); the rule fails the build on the class and the object either way. No `MSG-` ID applies to the masking answer itself: it returns a marker and a version, never text.

### 15. Screens and states

No screen is built by this story. SCR-47 Personal data shows the masking versions and the field IDs they cover, and the Compliance and PDPA officer and the security administrator read it there. The loading state of SCR-47 is as in Screen Specifications v1 section SCR-47; its empty, error and no access states are Not specified in the source documents (CG-ALL-5132). SCR-43 Roles and access shows the roles, the permissions and the scope. The empty, loading, error and no access states of SCR-43 are Not specified in the source documents (CG-ALL-5131). Both screens are served by the gateway-bff composite route (DP-19), which calls rwb-access for the policy and rwb-source-data for any value, one hop each. The rendering of a masked field on a screen belongs to the screen owner, not here: this story returns the marker and the version, and no rendering. The screen fields and the field-level masking of the composite route are Not specified in the source documents (GAP-0901; ASM-1622).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-069-01 | AC1, BR1, BR3 | End to end | Synthetic masking pack file for `MASK-2026.12` with the 20 field IDs of `v_ace_customer` and two roles; one repeated migration run |
| TC-E1-069-02 | AC2, BR12 | Component | Two sessions in a container: the rwb-access login and a role with no grant, against the 30 view names and `public.customer` |
| TC-E1-069-03 | AC3, BR4 | End to end | Pack file whose second half names the field IDs of a Section B view (`DF-ACE-187` to `DF-ACE-195`), loaded with no view present |
| TC-E1-069-04 | AC7, BR11 | End to end | Fixture class on `public.customer` in the package, and the same class on the rwb-source-data contract |
| TC-E1-069-05 | AC5, BR3 | End to end | Pack rows of 20 field IDs; an access entry naming `DF-ACE-073` and `DF-ACE-074` with the markers |
| TC-E1-069-06 | AC6, BR7 | End to end | Field `DF-ACE-018` (`days_past_due`) asked for with no row; the field is not personal and no masking row is expected for it |
| TC-E1-069-07 | AC7, BR3 | End to end | The extension-table field IDs `DF-EXT-001` to `DF-EXT-049`; a pack row naming one is refused by the fixture |
| TC-E1-069-08 | AC8, BR8, BR11 | End to end | Fixture class on `recovery.v_ace_customer` and on `public.customer`; the passing class on the rwb-source-data contract |
| TC-E1-069-09 | AC2 | Component | Pack with no unmasked row for RW-CASEOWN and DF-ACE-074; caller holding only RW-CASEOWN asks for DF-ACE-073 and DF-ACE-074 at MASK-2026.12 |
| TC-E1-069-10 | AC3 | Component | Pack with unmasked true for RW-COMPLY and DF-ACE-074 at MASK-2026.12; caller holding RW-COMPLY, then a caller holding only RW-CASEOWN |
| TC-E1-069-11 | AC5 | Component | Caller holding RW-AUDIT with scope ALL; healthy and stopped decision-record chain for the 503 path |
| TC-E1-069-12 | AC6 | Component | Caller holding only RW-PHONECOL, whose CASE_RECORD letters are '-' in PM-2026.12; field ID DF-ACE-073 |
| TC-E1-069-13 | Section 12 operations, events and activities | Contract | Not specified in the source documents (DOR-RWB-P4-E1069-APP-12) |
| TC-E1-069-14 | Section 12.7 tables | Component | Not specified in the source documents (DOR-RWB-P4-E1069-APP-12) |
| TC-E1-069-15 | AC10, BR2, BR14 | Component | Feature switch read as a parameter and set to off; caller holding RW-COMPLY; pack with unmasked true for RW-COMPLY and DF-ACE-074 at MASK-2026.12 |
| TC-E1-069-16 | AC11 | Component | Request to POST /api/recovery/access/v1/authorise with no valid session; request to a path of the section 12.1 operations that does not exist |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR; the masking answer itself is tested at Component level inside AC1 to AC6 and AC9. Every legacy test case of this key is listed above with the slice of the behaviour this story answers: TC-E1-069-01 and TC-E1-069-03 answer the view sets through RWB-P1-E1069-DB and RWB-P1-E1069-APP, and here only the field IDs the pack keys on; TC-E1-069-02 answers the grant model through RWB-P1-E1069-DB, and here the two facts about this service's own login; TC-E1-069-04 answers the constraint rule through RWB-P1-E1069-DB, and here the equivalent prohibition inside the package; TC-E1-069-05 answers the dictionary rows through RWB-P1-E1069-APP, and here the masking rows keyed by those field IDs; TC-E1-069-06 answers the delay-day mapping through RWB-P1-E1069-APP only, because the field is not personal; TC-E1-069-07 answers the extension tables through RWB-P1-E1069-DB only, because those tables are the Workbench's own; and TC-E1-069-08 answers boundary rule BND-6, which this slice applies to its own package; BND-6 is the per-service cross-schema check that fails the build on any cross-schema reference here, and the view conformance test 'Read-only ACE grant' stays with RWB-P1-E1069-DB, the only holder of the grant. The -ITG copies of these cases are not here — they belong to the integration slice RWB-ITG-E1069-ITG, which proves the grants across the 19 logins end to end.

### 17. Guardrails

- No business value in code: the roles, capability areas, letters, field IDs, masking rows and masking version are data rows read with the version in force. No role code, area, letter or field-ID list appears in Java, and the boundary rule reads its allowed object list from the module map.
- No personal data in events, logs, workflow inputs, tests or prompts: the answer carries a marker and a version only, the access entry carries IDs and field IDs only, and every test row is synthetic (`DF-ACE-073` and `DF-ACE-074` are named, never rendered).
- The clear identity number stays in ACE: the customer view returns `id_no_masked` and `id_no_last4`, this service never reads them and no pack row can open them.
- ACE data only through the owner's contract or `v_ace_*` views — and this service reads neither: a class that names a view fails the build, and the pointer to the value is rwb-source-data's contract.
- No cross-schema read and no cross-schema key: `rwb_access` holds no foreign key into another schema and no copy of a case, customer or ACE row (DP-01). The dictionary stays with P1.
- The access entry is written first, in the same transaction as the answer, through the decision-record library; a failed write means 503 and no answer (BR9).
- A missing row, a missing permission row and a missing role all resolve to masked or refused, never to clear and never to allow (BR5, BR7, BR14).
- One migration per story in the service's own Flyway sequence (DP-15); an applied version is never edited, and a change is a new version with a later `valid_from`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through `v_ace_account` and `v_ace_payment`, current to the previous working day, with the personal fields of the read maskable by role | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-01; FEAT-ACA-05 | All recovery processes | BR-P4-005; BR-P1-001-6; NFR-039; NFR-040 | TC-E1-069-01, TC-E1-069-03, TC-E1-069-05, TC-E1-069-06 |
| REQ-DRI-006 | No component calls a system of record directly; source data is read from the ACE database through the read-only `recovery.v_ace_*` views and leaves through paths ACE already has | Business Requirements Program, sections 5.2 and 7 | FEAT-RDF-01; FEAT-ACA-04 | All recovery processes | ADR-010; DL43; BND-6 | TC-E1-069-02, TC-E1-069-04, TC-E1-069-07, TC-E1-069-08, TC-E1-069-13, TC-E1-069-14 |

The supporting features of this slice are FEAT-ACA-05 (mask PDPA fields by role) and FEAT-ACA-04 (role to permission matrix as data), which the FSD P4 module pairs with RWB-E1-037 and RWB-E1-039; this slice answers them only for the ACE-sourced fields and changes neither the matrix design nor the access-log design. The -ITG copies of the test cases are carried by RWB-ITG-E1069-ITG.

### 19. Out of scope

- The view SQL of the 16 Section A and 14 Section B views, and the per-service Flyway sequence that creates them: RWB-P1-E1069-APP.
- The grant block, the per-service login and the four extension tables: RWB-P1-E1069-DB; the end-to-end grant proof across the 19 logins: RWB-ITG-E1069-ITG.
- The conformance test of the legacy key and the 30-view list, which stays frozen in the ACE Data Tier Map v1 and is changed only by the data architect and the recovery tech lead.
- The dictionary rows of the views (`sys_objects`, `sys_fields`) and the field catalogue: rwb-source-data, with the view set in RWB-P1-E1069-APP.
- The read of an ACE-sourced field and its masked rendering on a screen: rwb-source-data (RWB-P1-E1069-APP and its read contract) and gateway-bff (DP-19).
- The permission matrix as a whole, the role model, the DoA table and the access-log search: RWB-P4-E1037-APP, RWB-P4-E1022-APP, RWB-P4-E2013-APP and RWB-P4-E1039-APP.
- The load path that prepares and approves a masking pack file: RWB-P4-AD002-APP and RWB-P4-AD004-APP; the access review list (JOB-18): RWB-P4-AD008-APP.
- The `rwb_access` schema baseline, the topic and queue provisioning, the dashboards and the runbook of this service.
