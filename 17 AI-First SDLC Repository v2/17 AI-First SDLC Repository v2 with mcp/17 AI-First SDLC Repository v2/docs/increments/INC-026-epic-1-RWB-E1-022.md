# Increment Card — INC-026-epic-1-RWB-E1-022

**RWB-E1-022 — Sign-on with SSO, MFA and the first roles**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-026` |
| Title | Sign-on with SSO, MFA and the first roles |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-022` |
| RUN_ID | `INC-026-epic-1-RWB-E1-022` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P4 Access and administration |
| Story type | User story |
| Priority | Must |
| Build order | 26 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-019 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P4 Access and administration.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **to sign in to the Workbench once through Entra ID with multi-factor authentication and see only the screens and actions my Workbench roles allow**, so that **access is controlled from the first release and nobody holds a Workbench password or a local account**.

**Business outcome:** Access to recovery data today is granted system by system, and the bank cannot show who could see a case on a given date. This story makes Entra ID group membership the only way to hold a Workbench role: one group per role per environment, granted through the bank IAM, read at each sign-in and turned into a session with roles, scope and the permission matrix version in force. It meets REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 and supports control CTL-09 (access by role and scope). The measure is the access test set in section 16 passing for every role with real users at the release (DL39: administration roles at Epic 1).

**Main flow:**
1. Person: opens the Workbench in the ACE front end.
2. ACE common module: redirects to Entra ID; the person signs in with password and second factor; Entra ID returns an OpenID Connect token with the groups claim and the amr claim.
3. Workbench (SessionResolver): checks that the amr claim contains "mfa".
4. Workbench: maps each group in the groups claim to an active role row by role.entra_group; groups with no active role row are ignored.
5. Workbench: checks the resulting role set against the role conflict table version in force.
6. Workbench: resolves the session: user reference, roles, the permission matrix version in force at that time, and the default scope of each role.

**Acceptance criteria:**
- AC1: SSO sign-in
- AC2: Role denied
- AC3: Not in group
- AC4: Sign-in without a second factor is refused
- AC5: Two roles give the permissions of both
- AC6: A conflicting role pair is refused
- AC7: A service identity is checked like a person
- AC8: An unmapped or inactive group gives no role
- AC9: An open session keeps the versions it resolved

**Out of scope:**
- The permission matrix load, PDPA masking, scope filtering and leaver handling (RWB-E1-037).
- Writing access events into the decision log and break-glass (RWB-E1-039).
- Partner identities through the external gateway (RWB-E2-019).
- Full administration screens for roles and access, SCR-43 (Epic 8, FEAT-ADM-01).
- The request, approval and grant steps themselves, which run in the bank IAM, not in the Workbench.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-022-sign-on-with-sso-mfa-and-the-first-roles-v1.md` |
| Requirement IDs | REQ-ACA-001, REQ-ACA-002, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Program, section 5.4 |
| Decision | None |
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
| Line manager (bank IAM, level 4) | Requests a Workbench role for a team member in the bank IAM, naming the person, the role and the reason. May not approve the request they raised |
| Role owner (bank IAM, level 2), the head of the unit whose staff hold the role | Approves or rejects each grant of a role they own after checking the separation of duty table |
| Access administrator (bank IAM, level 3), Chief Debt Recovery Management Office (assumed, DL01) | Adds the person to the Entra ID group of the approved role in each environment requested. Approves no grant |
| Application owner (level 1), Tribe Lead of the Collections and Recovery Tribe (assumed, DL02) | Approves the roles table and each group to role mapping |
| RW-SECADM Security administrator | Maintains the Entra ID groups and the IAM link (DL40); receives the conflict incident in AC6 |
| RW-REFADM Reference data administrator | Loads an approved role or group mapping version. Approves none |
| RW-CASEOWN and every bank role | Signs in and uses the screens of the role |
| RW-PHONECOL Phone collector | Signs in; refused on Platform administration (AC2) |
| SY-RULES and the other service identities | Act under their managed identity and their own role row |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read GET /admin/roles (Platform administration R) |

The four administration levels act in the bank IAM, not in the Workbench. If the bank chooses central administration (DL01), level 3 moves to the central IAM team and nothing in this build changes.

## Contract extract

**GET /api/recovery/v1/admin/roles** (API-P4-007) | Item | Value | |---|---| | Request | None | | Response | Array of Role: id, roleCode, roleName, roleClass, defaultScope, entraGroup | | Errors | 401 no valid session or no role (MSG-P4-001, MSG-P4-005, MSG-P4-006); 403 the session's roles hold no R in Platform administration (MSG-P4-002); 503 the ACE sign-in service is unavailable (MSG-GEN-006) | | Authorization | Platform administration, right R | | Idempotency | Not applicable, read only | **GET /me/session** (new, recorded in the additions file) | Item | Value | |---|---| | Request | None | | Response | Session: userRef, roles (roleCode, roleName, defaultScope), matrixVersion, conflictVersion, scopeLine, resolvedAt, breakGlass (active, endsAt; filled by RWB-E1-039) | | Errors | 401 as above | | Authorization | Any resolved session; no capability area, because the endpoint returns on…

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

- No business value in code: group names, roles, letters, scopes and conflicts are read from tables with their version. - No personal data in logs, tests or prompts. Access events carry the Entra ID object reference, never the person's name or e-mail. - No read of another module's tables. - No local password, local account or role cache that outlives the session. - Every endpoint declares its capability area and right; an endpoint without one fails the contract test.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-022-sign-on-with-sso-mfa-and-the-first-roles-v1.md` |
| Specification | `output/INC-026-epic-1-RWB-E1-022/specify/spec.md` |
| Compliance validation | `output/INC-026-epic-1-RWB-E1-022/specify/compliance-validation.md` |
| Agent run log | `output/INC-026-epic-1-RWB-E1-022/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-026-epic-1-RWB-E1-022/plan/` |
| Implementation evidence | `output/INC-026-epic-1-RWB-E1-022/implement/` |
| API / functional test reports | `output/INC-026-epic-1-RWB-E1-022/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-026-epic-1-RWB-E1-022/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-022-sign-on-with-sso-mfa-and-the-first-roles-v1.md` |
| Output run | `output/INC-026-epic-1-RWB-E1-022/` |

