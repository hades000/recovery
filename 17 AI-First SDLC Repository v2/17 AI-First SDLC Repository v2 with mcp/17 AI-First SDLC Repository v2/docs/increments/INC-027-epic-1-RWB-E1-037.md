# Increment Card — INC-027-epic-1-RWB-E1-037

**RWB-E1-037 — Role to permission matrix as data and PDPA field masking by role**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-027` |
| Title | Role to permission matrix as data and PDPA field masking by role |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-037` |
| RUN_ID | `INC-027-epic-1-RWB-E1-037` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P4 Access and administration |
| Story type | User story |
| Priority | Must |
| Build order | 27 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-022, RWB-E1-043, RWB-E1-027, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P4 Access and administration.

## Scope

**Story:** As a **product owner**, I want **the mapping of roles to capability areas, the scope of each role and the masking of each personal data field held as versioned tables that every screen and API applies, with the identity number masked inside the ACE view and contact values masked at the API**, so that **a change of rights is a data load with an approver, a person sees only the cases in their scope, and personal data shows unmasked only to roles that need it**.

**Business outcome:** Audit findings record unsuitable user access to EFS and staff sending debtor data outside the bank. Today rights are set inside each system and cannot be shown for a past date. This story holds the permission matrix (54 roles against 14 capability areas), the masking rules and the scope rule as versioned data, applies scope before permission on every request, and ends access at the next request when a person leaves. Under D-RCV-35 there is no load and no tokenization: ACE ingests the source row once, `v_ace_customer` exposes the identity number as `id_no_masked` and `id_no_last4` only, and `v_ace_contact` exposes the full phone, email and address because notices and calls need them. Masking is therefore applied to view columns, not to a token stored at load. It meets REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011 and puts controls CTL-09, CTL-10 and CTL-11 in place. The measure is rule and limit changes made without a code release: target 100 percent (FSD P4 A2.4).

**Main flow:**
1. Reference data administrator (RW-REFADM): prepares the matrix file from the approved workbook, with the application owner's approval reference in the file header, and calls POST /admin/reference-loads with table "permission" and validFrom.
2. Workbench (PermissionMatrixLoader): validates the file whole: every active role once against all 14 capability areas, letters only from C, R, U, D, A in that order or "-", known role codes; stores the rows with status Loaded and the new matrix_version.
3. Security administrator (RW-SECADM): reviews the difference report against the version in force and calls POST /admin/reference-loads/{loadId}/approve.
4. Workbench: checks that the approver holds the role the parameter names for the table and is not the person who loaded it; writes one decision log entry for the approval with decision code AC-VERS and no case; marks the version Approved with its valid from date.
5. Workbench: from the valid from date, every new session resolves the new version (RWB-E1-022 keeps open sessions on their version), and the screens and endpoints of the new letters open with no deployment.
6. Person: requests a list or a record; ScopeService builds the filter from the role's default scope (own, team, region, all) and the person's teams and regions; the owning module applies it in its query.

**Acceptance criteria:**
- AC1: Matrix as data
- AC2: Masking from the view columns
- AC3: Denied action
- AC4: A case outside the scope is not returned
- AC5: A matrix file with an error is refused in full
- AC6: The loader cannot approve
- AC7: An approval that cannot be recorded does not take effect
- AC8: A leaver loses access at the next request
- AC9: A personal field with no masking rule is masked
- AC10: Two approvals of the same load at once
- AC11: The clear identity number never leaves ACE
- AC12: A read of a personal field is audited
- AC13: Only the table's approver role may approve

**Out of scope:**
- Reallocation of a leaver's or mover's open cases (RWB-E1-030 daily rebalancing; R-UNI-18 and R-UNI-19 in Epic 2).
- Administration screens SCR-43 and SCR-47 (Epic 8, FEAT-ADM-01 and FEAT-ADM-14).
- Masking values for each role and field (Compliance, DL26).
- Access per data product in the data lake copy (RWB-E1-016).
- The six-monthly access review list (JOB-18, Epic 2 control CTL-10).
- The shape of the mask itself, which is the view function `recovery.ace_mask_value` and the ACE team's definition.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-037-role-to-permission-matrix-as-data-and-pdpa-field-masking-by-role-v1.md` |
| Requirement IDs | REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009, REQ-ACA-011 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Epic 2, section 3.4 (REQ-ACA-011); Business Requirements Program, section 5.4 |
| Decision | D-RCV-35 (U1, U4); ADR-010 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| Application owner (level 1, assumed DL02) | Approves each permission matrix version outside the Workbench; the approval reference is carried in the load file |
| Role owners (level 2) | Request matrix changes for the roles they own |
| RW-REFADM Reference data administrator | Loads a matrix or masking version (Reference data C). Approves none |
| RW-COE Center of excellence analyst | Holds Reference data C and may load; may not approve |
| RW-SECADM Security administrator | Approves a permission or role conflict version (approver role for the table, parameter) |
| RW-COMPLY Compliance and PDPA officer | Sets the masking rules and approves each masking version (approver role for the table, parameter) |
| RW-AUDIT Internal audit | Reads every version and the approval entries; changes nothing |
| Access administrator (level 3, bank IAM) | Removes leavers and movers from Entra ID groups |
| Line manager (level 4, bank IAM) | Starts mover and leaver changes |
| Every bank role | Sees cases inside the default scope of its roles, with fields masked per the masking rules |
| ACE team lead | Owns the ACE tables and columns behind `v_ace_customer` and `v_ace_contact` |

## Contract extract

**POST /api/recovery/v1/admin/reference-loads** (API-P4-005) | Item | Value | |---|---| | Request | Multipart: file (xlsx or csv), table ("permission" or "masking_rule"), validFrom (date) | | Response | 201 ReferenceLoad: id, table, validFrom, status "Loaded", rows | | Errors | 401 no session; 403 no Reference data C (MSG-P4-002); 409 a version with the same name exists (MSG-GEN-004); 422 validation failed (MSG-P1-002, with the failed check in detail); 503 store unavailable (MSG-GEN-006) | | Authorization | Reference data, right C | | Idempotency | Idempotency-Key header; the same key returns the first response | **POST /admin/reference-loads/{loadId}/approve** (API-P4-006) | Item | Value | |---|---| | Request | None | | Response | 200 ReferenceLoad with status "Approved" | | Errors | 401; 403 caller does not hold the approver role for the table (MSG-P4-002); 404 no such load (MSG-P4-00…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: letters, scopes, masking positions, approver roles and the refresh interval are data or parameters. - No personal data in logs, tests or prompts. Tests use synthetic values; the access event lists field IDs and their masked flag, never values. - ACE data only through the `recovery.v_ace_*` views: identity, name, date of birth and contact values come from `v_ace_customer` and `v_ace_contact`. The recovery schema holds no foreign key into a `public` table. - No tokenization and no token store. The clear identity number never leaves ACE, and no Workbench column, service or rule returns it. - An unmasked contact value is read from `v_ace_contact.contact_value` only where the masking rule allows it, and every such read is audited. - A field with no masking rule is masked.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-037-role-to-permission-matrix-as-data-and-pdpa-field-masking-by-role-v1.md` |
| Specification | `output/INC-027-epic-1-RWB-E1-037/specify/spec.md` |
| Compliance validation | `output/INC-027-epic-1-RWB-E1-037/specify/compliance-validation.md` |
| Agent run log | `output/INC-027-epic-1-RWB-E1-037/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-027-epic-1-RWB-E1-037/plan/` |
| Implementation evidence | `output/INC-027-epic-1-RWB-E1-037/implement/` |
| API / functional test reports | `output/INC-027-epic-1-RWB-E1-037/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-027-epic-1-RWB-E1-037/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 13 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-037-role-to-permission-matrix-as-data-and-pdpa-field-masking-by-role-v1.md` |
| Output run | `output/INC-027-epic-1-RWB-E1-037/` |

