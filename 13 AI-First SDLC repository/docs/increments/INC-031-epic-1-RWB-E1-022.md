# Increment Card — INC-031-epic-1-RWB-E1-022

**RWB-E1-022 — Sign-on with SSO, MFA and the first roles**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-031` |
| Title | Sign-on with SSO, MFA and the first roles |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-022` |
| RUN_ID | `INC-031-epic-1-RWB-E1-022` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P4 Access and administration |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-001, RWB-E1-019 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P4 Access and administration. **Build group:** P4.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **to sign in to the Workbench once through Entra ID with multi-factor authentication and see only the screens and actions my Workbench roles allow**, so that **access is controlled from the first release and nobody holds a Workbench password or a local account**.

**Main flow:**
1. Person: opens the Workbench in the ACE front end.
2. ACE common module: redirects to Entra ID; the person signs in with password and second factor; Entra ID returns an OpenID Connect token with the groups claim and the amr claim.
3. Workbench (SessionResolver): checks that the amr claim contains "mfa".
4. Workbench: maps each group in the groups claim to an active role row by role.entra_group; groups with no active role row are ignored.
5. Workbench: checks the resulting role set against the role conflict table version in force.
6. Workbench: resolves the session: user reference, roles, the permission matrix version in force at that time, and the default scope of each role.

**Out of scope:**
- The permission matrix load, PDPA masking, scope filtering and leaver handling (RWB-E1-037).
- Writing access events into the decision log and break-glass (RWB-E1-039).
- Partner identities through the external gateway (RWB-E2-019).
- Full administration screens for roles and access, SCR-43 (Epic 8, FEAT-ADM-01).
- The request, approval and grant steps themselves, which run in the bank IAM, not in the Workbench.

**Business outcome and value hypothesis:** Access to recovery data today is granted system by system, and the bank cannot show who could see a case on a given date. This story makes Entra ID group membership the only way to hold a Workbench role: one group per role per environment, granted through the bank IAM, read at each sign-in and turned into a session with roles, scope and the permission matrix version in force. It meets REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 and supports control CTL-09 (access by role and scope). The measure is the access test set in section 16 passing for every role with real users at the release (DL39: administration roles at Epic 1).

**Constraints and guardrails:**
- No business value in code: group names, roles, letters, scopes and conflicts are read from tables with their version.
- No personal data in logs, tests or prompts. Access events carry the Entra ID object reference, never the person's name or e-mail.
- No read of another module's tables.
- No local password, local account or role cache that outlives the session.
- Every endpoint declares its capability area and right; an endpoint without one fails the contract test.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 022 Sign on with SSO MFA and the first roles v1.md` |
| Requirement IDs | REQ-ACA-001, REQ-ACA-002, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Program, section 5.4 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
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

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.access.sso-roles`.
- **Critical path:** Yes; **depends on:** RWB-E1-001, RWB-E1-019.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: group names, roles, letters, scopes and conflicts are read from tables with their version.
  - No personal data in logs, tests or prompts. Access events carry the Entra ID object reference, never the person's name or e-mail.
  - No read of another module's tables.
  - No local password, local account or role cache that outlives the session.
  - Every endpoint declares its capability area and right; an endpoint without one fails the contract test.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 022 Sign on with SSO MFA and the first roles v1.md` |
| Specification | `output/INC-031-epic-1-RWB-E1-022/specify/spec.md` |
| Compliance validation | `output/INC-031-epic-1-RWB-E1-022/specify/compliance-validation.md` |
| Agent run log | `output/INC-031-epic-1-RWB-E1-022/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-031-epic-1-RWB-E1-022/plan/` (TBC) |
| Implementation evidence | `output/INC-031-epic-1-RWB-E1-022/implement/` (TBC) |
| API / functional test reports | `output/INC-031-epic-1-RWB-E1-022/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-031-epic-1-RWB-E1-022/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-031-epic-1-RWB-E1-022/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 022 Sign on with SSO MFA and the first roles v1.md` |
| Output run | `output/INC-031-epic-1-RWB-E1-022/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
