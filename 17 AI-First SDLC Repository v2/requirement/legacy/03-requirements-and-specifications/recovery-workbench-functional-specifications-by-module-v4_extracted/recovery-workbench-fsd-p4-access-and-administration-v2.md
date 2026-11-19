<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v4.zip!Recovery Workbench FSD P4 Access and administration v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v4.zip!Recovery Workbench FSD P4 Access and administration v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P4 Access and administration

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P4 Access and administration |
| Document ID | P4-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, P4 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| P4 | Access and administration | E1; E2 partners; E8 full administration |

**Feature scope.** Roles, permissions, scope, masking, delegation of authority table, access log.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P4 Access and administration | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | EXTEND | Users Roles and Permissions | Recovery roles as data on the ACE access check |
| Restructure calculator | REUSE | ACE common module | Not used |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** Roles, permissions, scope, masking, delegation of authority table, access log.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-ACA-01; FEAT-ACA-03; FEAT-ACA-04; FEAT-ACA-05; FEAT-ACA-06; FEAT-ACA-07; FEAT-ACA-07, FEAT-DRI-01; FEAT-ACA-08

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P4 | FEAT-ACA-01 | Sign on through Entra ID with single sign-on | User | Gives every bank user one sign-on to the Workbench through the bank identity provider. | E1 | A2.1 |
| P4 | FEAT-ACA-02 | Enforce multi-factor authentication | System | Requires a second factor on sign-on, under the bank standard. | E1 | A2.2 |
| P4 | FEAT-ACA-03 | Hold roles as data | Admin | Keeps the role list in a versioned table, so a new role is added without a code release. | E1 | A2.3 |
| P4 | FEAT-ACA-04 | Hold the role to permission matrix as data | Admin | Keeps which role may create, read, update, delete and approve in each capability area, as versioned rows. | E1 | A2.4 |
| P4 | FEAT-ACA-05 | Mask PDPA fields by role | System | Hides personal fields from any role whose permission row does not allow them, on every screen and to every agent. | E1 | A2.5 |
| P4 | FEAT-ACA-06 | Hold the delegation of authority table as reference data | Admin | Keeps the approval limit per role and per decision as versioned data that the approval router reads. | E1 | A2.6 |
| P4 | FEAT-ACA-07 | Write every access event to the access log | System | Records who looked at which case, which document and which data product, and when. | E1 | A2.7 |
| P4 | FEAT-ACA-08 | Write the access log into the decision log | System | Puts access events into the same append-only log, so access and decisions are queried together. | E1 | A2.8 |
| P4 | FEAT-ACA-09 | Use break-glass access with an incident reference | Admin | Lets an administrator take emergency access only against a named incident, and logs every use. | E1 | A2.9 |
| P4 | FEAT-ACA-10 | Review break-glass use | Admin | Puts every break-glass use in front of Compliance, and raises any use with no incident reference. | E1 | A2.10 |
| P4 | FEAT-ACA-11 | Show the case record view read only | User | Gives one screen holding the case, its accounts, parties, collateral, documents and history. | E1 | A2.11 |
| P4 | FEAT-ACA-12 | Show the case record view with the history timeline | User | Adds the full event history to the case record view, in time order, with the rule version on each entry. | E1 | A2.12 |
| P4 | FEAT-ACA-13 | Apply joiner, mover and leaver changes to access | Admin | Adds, moves and removes a user's roles when their position changes, and reallocates their open cases. | E1 | A2.13 |
| P4 | FEAT-ACA-14 | Scope a user's cases by team and region | System | Limits what each user sees to the cases their role, team and region permit. | E1 | A2.14 |
| P4 | FEAT-ACA-15 | Run the release checklist, training and go-live readiness | Admin | Works the checklist that says the release can go to production: tests, training, run books, rollback. | E1 | A2.15 |
| P4 | FEAT-ACA-16 | Answer an access audit query | User | Returns who accessed a case or a document over a period, from the access log. | E1 | A2.16 |
| P4 | FEAT-ADM-01 | Run the full administration screens | Admin | Gives administration one place for roles, queues, parameters, templates, panels and autonomy. | E8 | A2.17 |
| P4 | FEAT-ADM-02 | Change a decision rule through the administration screens | Admin | Lets the center of excellence change a rule, test it and put it in force as a new version. | E8 | A2.18 |
| P4 | FEAT-ADM-03 | Move an approval limit | Admin | Changes a delegated limit, with Risk approving and the change versioned. | E8 | A2.19 |
| P4 | FEAT-ADM-04 | Set the treatment policy by product | Admin | Lets the product head set the bands, floors and ranges for their product. | E8 | A2.20 |
| P4 | FEAT-ADM-05 | Add a letter template with Compliance approval | Admin | Adds a new template through the approval path and records who approved it. | E8 | A2.21 |
| P4 | FEAT-ADM-06 | Roll back a configuration version | Admin | Returns any versioned table to its previous version and records the rollback. | E8 | A2.22 |
| P4 | FEAT-ADM-07 | Publish a panel change | Admin | Puts a partner panel change in force with an effective date. | E8 | A2.23 |
| P4 | FEAT-ADM-08 | Run a QA sample against the rule version applied | User | Samples closed decisions and tests each against the rule version that was in force. | E8 | A2.24 |
| P4 | FEAT-ADM-09 | Return a defective pack | System | Sends a pack that fails the check back to its owner with the defects named. | E8 | A2.25 |
| P4 | FEAT-ADM-10 | Detect a broken hash chain in the decision log | System | Tests the log chain and raises a control breach if a record does not verify. | E8 | A2.26 |
| P4 | FEAT-ADM-11 | Handle a data subject request | User | Works a PDPA access, correction or erasure request inside the statutory period. | E8 | A2.27 |
| P4 | FEAT-ADM-12 | Manage an incident | Admin | Runs the incident path: detect, hold, fix, record and report. | E8 | A2.28 |
| P4 | FEAT-ADM-13 | Refer a case to Aric | System | Sends a case to Aric where the fraud rules require it, and takes the result back. | E8 | A2.29 |
| P4 | FEAT-ADM-14 | Control access by role and by agent | Admin | Reviews and sets what each role and each agent may read and do, and reports the matrix. | E8 | A2.30 |

### A1.3 Background

Access, limits and rules live in documents and people's heads; changes need code or manual checks.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Sign on through Entra ID with single sign-on

#### A2.1.1 Intent

**Business objective.** Gives every bank user one sign-on to the Workbench through the bank identity provider.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Gives every bank user one sign-on to the Workbench through the bank identity provider.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and sign on through Entra ID with single sign-on | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Entra ID

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-001-1 | Sign-in with no Workbench role | MSG-P4-001 You have no Recovery Workbench role. Ask your team manager to request one. |
| VR-P4-001-2 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| all bank roles | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-001-01 | SSO sign-in | test user "U-1001" is in Entra ID group "RWB-SIT-RW-CASEOWN" | the user opens the Workbench and signs in with password and second factor | the session holds roles "RW-CASEOWN", scope "OWN" and matrix version "PM-2026.11" And GET /me/session returns the line "Case owner. Scope: own cases." And the menu shows the screens of the capability areas where RW-CASEOWN holds R, and no Administration menu | RWB-E1-022 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-001-01 | Role denied | test user "U-1002" holds only RW-PHONECOL, whose Platform administration letter is "-" | the user calls GET /admin/roles | the call is refused with status 403 and message MSG-P4-002 with action "read roles" And one refusal event is written with user "U-1002", area "PLATFORM_ADMINISTRATION", right "R" and result "REFUSED" | RWB-E1-022 |
| AC-ALT-P4-001-02 | Two roles give the permissions of both | test user "U-1005" is in groups "RWB-SIT-RW-LITOFF" and "RWB-SIT-RW-LEGAL" | the user signs in | the session holds roles "RW-LITOFF" and "RW-LEGAL" And the Documents letters are "CRUA", the union of "CRU" and "CRUA" And no permission comes from any role the user does not hold | RWB-E1-022 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-001-01 | Not in group | test user "U-1003" has an Entra ID account and no group whose name starts "RWB-SIT-" | the user opens the Workbench | the access request page shows MSG-P4-001 and no case, queue or reference data And every recovery endpoint returns status 401 for that token And one refusal event is written with reason "NO_ROLE" | RWB-E1-022 |
| AC-EXC-P4-001-02 | Sign-in without a second factor is refused | test user "U-1004" is in group "RWB-SIT-RW-CASEOWN" And the token's amr claim holds "pwd" and not "mfa" | the token reaches the Workbench | the session is refused with status 401 and message MSG-P4-005 And one refusal event is written with reason "NO_MFA" | RWB-E1-022 |
| AC-EXC-P4-001-03 | A conflicting role pair is refused | test user "U-1006" is in groups "RWB-SIT-RW-SECADM" and "RWB-SIT-RW-CASEOWN" And the role conflict table says RW-SECADM may not hold any business role | the user signs in | the session is refused with message MSG-P4-006 naming "RW-SECADM" and "RW-CASEOWN" And an incident is raised to the security administrator queue And one refusal event is written with reason "ROLE_CONFLICT" | RWB-E1-022 |
| AC-EXC-P4-001-04 | An unmapped or inactive group gives no role | test user "U-1008" is in groups "RWB-SIT-RW-CASEOWN" and "RWB-SIT-LEGACY01" And no active role row has entra_group "RWB-SIT-LEGACY01" | the user signs in | the session holds only "RW-CASEOWN" And the unmapped group name is written on the sign-in event | RWB-E1-022 |
| AC-EXC-P4-001-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-001-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Enforce multi-factor authentication

#### A2.2.1 Intent

**Business objective.** Requires a second factor on sign-on, under the bank standard.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Requires a second factor on sign-on, under the bank standard.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Enforce multi-factor authentication | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Entra ID

**Prerequisites.** FEAT-ACA-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-002-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P4-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Security administrator | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-002-01 | SSO sign-in | test user "U-1001" is in Entra ID group "RWB-SIT-RW-CASEOWN" | the user opens the Workbench and signs in with password and second factor | the session holds roles "RW-CASEOWN", scope "OWN" and matrix version "PM-2026.11" And GET /me/session returns the line "Case owner. Scope: own cases." And the menu shows the screens of the capability areas where RW-CASEOWN holds R, and no Administration menu | RWB-E1-022 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-002-01 | Role denied | test user "U-1002" holds only RW-PHONECOL, whose Platform administration letter is "-" | the user calls GET /admin/roles | the call is refused with status 403 and message MSG-P4-002 with action "read roles" And one refusal event is written with user "U-1002", area "PLATFORM_ADMINISTRATION", right "R" and result "REFUSED" | RWB-E1-022 |
| AC-ALT-P4-002-02 | Two roles give the permissions of both | test user "U-1005" is in groups "RWB-SIT-RW-LITOFF" and "RWB-SIT-RW-LEGAL" | the user signs in | the session holds roles "RW-LITOFF" and "RW-LEGAL" And the Documents letters are "CRUA", the union of "CRU" and "CRUA" And no permission comes from any role the user does not hold | RWB-E1-022 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-002-01 | Not in group | test user "U-1003" has an Entra ID account and no group whose name starts "RWB-SIT-" | the user opens the Workbench | the access request page shows MSG-P4-001 and no case, queue or reference data And every recovery endpoint returns status 401 for that token And one refusal event is written with reason "NO_ROLE" | RWB-E1-022 |
| AC-EXC-P4-002-02 | Sign-in without a second factor is refused | test user "U-1004" is in group "RWB-SIT-RW-CASEOWN" And the token's amr claim holds "pwd" and not "mfa" | the token reaches the Workbench | the session is refused with status 401 and message MSG-P4-005 And one refusal event is written with reason "NO_MFA" | RWB-E1-022 |
| AC-EXC-P4-002-03 | A conflicting role pair is refused | test user "U-1006" is in groups "RWB-SIT-RW-SECADM" and "RWB-SIT-RW-CASEOWN" And the role conflict table says RW-SECADM may not hold any business role | the user signs in | the session is refused with message MSG-P4-006 naming "RW-SECADM" and "RW-CASEOWN" And an incident is raised to the security administrator queue And one refusal event is written with reason "ROLE_CONFLICT" | RWB-E1-022 |
| AC-EXC-P4-002-04 | An unmapped or inactive group gives no role | test user "U-1008" is in groups "RWB-SIT-RW-CASEOWN" and "RWB-SIT-LEGACY01" And no active role row has entra_group "RWB-SIT-LEGACY01" | the user signs in | the session holds only "RW-CASEOWN" And the unmapped group name is written on the sign-in event | RWB-E1-022 |
| AC-EXC-P4-002-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-002-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Hold roles as data

#### A2.3.1 Intent

**Business objective.** Keeps the role list in a versioned table, so a new role is added without a code release.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Keeps the role list in a versioned table, so a new role is added without a code release.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Security administrator | Opens the screen and hold roles as data | Checks the role, the capability area and the scope |
| 2 | Security administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-06

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-003-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| Security administrator | Primary |
| Reference data administrator | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-003-01 | Tables loaded | the Queues template with 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams and 48 member rows | the QUEUE and QUEUE_MEMBER sheets are loaded as version 1 with valid from 2026-11-30 and approved | 12 queue rows are in force with table version 1 And each queue holds its team code and the role that works it, for example "LIT-BKK-OFF" with "LIT-BKK" and RW-LITOFF And 48 member rows are in force And the reference version holds the author, the approver and the approval time | RWB-E1-019 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-003-01 | Rollback | QUEUE version 3 is in force with an error in queue "DIL-BKK-CO" And QUEUE version 2 was in force before it | rollback is called once for version 3 | QUEUE version 2 is in force for every queue row And each queue keeps its record ID, so cases in the queue keep their queue And the rollback is recorded with the caller, the time and the reason | RWB-E1-019 |
| AC-ALT-P4-003-02 | Capacity | member U-11 of queue "TDR-BKK-CO" has capacity 40 and holds 40 open cases | a 41st case is offered for U-11 | the capacity service answers "AT_CAP" for U-11 And names the overflow queue "TDR-BKK-OVF" for the case | RWB-E1-019 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-003-01 | Author cannot approve | QUEUE version 4 was loaded by user U-90 | U-90 approves it | the approval is refused with MSG-P7-002 And version 4 stays VALIDATED and is not in force | RWB-E1-019 |
| AC-EXC-P4-003-02 | Rollback with no earlier version | QUEUE version 1 is the only version | rollback is called for version 1 | the call is refused with MSG-P3-015 And version 1 stays in force | RWB-E1-019 |
| AC-EXC-P4-003-03 | Not in group | test user "U-1003" has an Entra ID account and no group whose name starts "RWB-SIT-" | the user opens the Workbench | the access request page shows MSG-P4-001 and no case, queue or reference data And every recovery endpoint returns status 401 for that token And one refusal event is written with reason "NO_ROLE" | RWB-E1-022 |
| AC-EXC-P4-003-04 | Sign-in without a second factor is refused | test user "U-1004" is in group "RWB-SIT-RW-CASEOWN" And the token's amr claim holds "pwd" and not "mfa" | the token reaches the Workbench | the session is refused with status 401 and message MSG-P4-005 And one refusal event is written with reason "NO_MFA" | RWB-E1-022 |
| AC-EXC-P4-003-05 | A conflicting role pair is refused | test user "U-1006" is in groups "RWB-SIT-RW-SECADM" and "RWB-SIT-RW-CASEOWN" And the role conflict table says RW-SECADM may not hold any business role | the user signs in | the session is refused with message MSG-P4-006 naming "RW-SECADM" and "RW-CASEOWN" And an incident is raised to the security administrator queue And one refusal event is written with reason "ROLE_CONFLICT" | RWB-E1-022 |
| AC-EXC-P4-003-06 | An unmapped or inactive group gives no role | test user "U-1008" is in groups "RWB-SIT-RW-CASEOWN" and "RWB-SIT-LEGACY01" And no active role row has entra_group "RWB-SIT-LEGACY01" | the user signs in | the session holds only "RW-CASEOWN" And the unmapped group name is written on the sign-in event | RWB-E1-022 |
| AC-EXC-P4-003-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-003-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Hold the role to permission matrix as data

#### A2.4.1 Intent

**Business objective.** Keeps which role may create, read, update, delete and approve in each capability area, as versioned rows.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Keeps which role may create, read, update, delete and approve in each capability area, as versioned rows.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Security administrator | Opens the screen and hold the role to permission matrix as data | Checks the role, the capability area and the scope |
| 2 | Security administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-03

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-004-1 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| VR-P4-004-2 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| BR-P4-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| Security administrator | Primary |
| Compliance and PDPA officer, Internal audit | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-004-01 | Matrix as data | test user "U-2101" holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01" And the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11" And test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | test user "U-2103" holding RW-LEGAL signs in on 1 December 2026 and calls GET /queues | the call returns status 200, where under "PM-2026.11" it returned 403, with no deployment And one decision log entry exists with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102" | RWB-E1-037 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-004-01 | Masking | test user "U-2104" holds only RW-PHONECOL | the user opens case "RW-2026-000123" in the case record view | the borrower's identity number shows as "XXXXXXXXX1234" and the phone number as "XXXXXX5678" And no request is made to the ACE PII service for clear values And the view is written to the access event stream with the case ID and the fields shown masked | RWB-E1-037 |
| AC-ALT-P4-004-02 | Denied action | test user "U-2105" holds only RW-CASEOWN, whose Queue and allocation letter is "R" | the user calls POST /cases/{caseId}/transfer for case "RW-2026-000123" | the call is refused with status 403 and message MSG-P4-002 before the handler runs And the case owner and queue are unchanged And one refusal event is written with area "QUEUE_AND_ALLOCATION" and right "U" | RWB-E1-037 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-004-01 | A case outside the scope is not returned | test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases And case "RW-2026-000456" belongs to team "MTG-NE" and another owner | the user calls GET /cases | 12 cases return and the total is 12 And GET /cases/{caseId} for "RW-2026-000456" returns status 404 with message MSG-P4-003 | RWB-E1-037 |
| AC-EXC-P4-004-02 | A matrix file with an error is refused whole | matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting | test user "U-2101" loads it | the load is refused with message MSG-P1-002 naming the duplicate row and the invalid letters And no row of "PM-2026.13" is stored and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-004-03 | The loader cannot approve, and only the table's approver role may | load "PM-2026.12" was loaded by test user "U-2101" | "U-2101" calls approve on that load | the call is refused with message MSG-P7-002 and the load stays "Loaded" And when test user "U-2106" holding RW-COE calls approve on that load the call is refused with status 403 and message MSG-P4-002 | RWB-E1-037 |
| AC-EXC-P4-004-04 | An approval that cannot be recorded does not take effect | the decision log store is unavailable | test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | the call returns status 503 with message MSG-P7-003 And the load stays "Loaded" and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-004-05 | A personal field with no masking rule is masked | no masking rule in "MASK-SIT-01" covers party.date_of_birth for any role | test user "U-2105" holding RW-CASEOWN opens case "RW-2026-000123" | the date of birth shows masked as "XXXX-XX-XX" | RWB-E1-037 |
| AC-EXC-P4-004-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-004-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Mask PDPA fields by role

#### A2.5.1 Intent

**Business objective.** Hides personal fields from any role whose permission row does not allow them, on every screen and to every agent.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Hides personal fields from any role whose permission row does not allow them, on every screen and to every agent.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Mask PDPA fields by role | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-04

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-005-1 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| VR-P4-005-2 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| VR-P4-005-3 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| BR-P4-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Compliance and PDPA officer | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-005-01 | Matrix as data | test user "U-2101" holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01" And the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11" And test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | test user "U-2103" holding RW-LEGAL signs in on 1 December 2026 and calls GET /queues | the call returns status 200, where under "PM-2026.11" it returned 403, with no deployment And one decision log entry exists with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102" | RWB-E1-037 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-005-01 | Masking | test user "U-2104" holds only RW-PHONECOL | the user opens case "RW-2026-000123" in the case record view | the borrower's identity number shows as "XXXXXXXXX1234" and the phone number as "XXXXXX5678" And no request is made to the ACE PII service for clear values And the view is written to the access event stream with the case ID and the fields shown masked | RWB-E1-037 |
| AC-ALT-P4-005-02 | Denied action | test user "U-2105" holds only RW-CASEOWN, whose Queue and allocation letter is "R" | the user calls POST /cases/{caseId}/transfer for case "RW-2026-000123" | the call is refused with status 403 and message MSG-P4-002 before the handler runs And the case owner and queue are unchanged And one refusal event is written with area "QUEUE_AND_ALLOCATION" and right "U" | RWB-E1-037 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-005-01 | A case outside the scope is not returned | test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases And case "RW-2026-000456" belongs to team "MTG-NE" and another owner | the user calls GET /cases | 12 cases return and the total is 12 And GET /cases/{caseId} for "RW-2026-000456" returns status 404 with message MSG-P4-003 | RWB-E1-037 |
| AC-EXC-P4-005-02 | A matrix file with an error is refused whole | matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting | test user "U-2101" loads it | the load is refused with message MSG-P1-002 naming the duplicate row and the invalid letters And no row of "PM-2026.13" is stored and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-005-03 | The loader cannot approve, and only the table's approver role may | load "PM-2026.12" was loaded by test user "U-2101" | "U-2101" calls approve on that load | the call is refused with message MSG-P7-002 and the load stays "Loaded" And when test user "U-2106" holding RW-COE calls approve on that load the call is refused with status 403 and message MSG-P4-002 | RWB-E1-037 |
| AC-EXC-P4-005-04 | An approval that cannot be recorded does not take effect | the decision log store is unavailable | test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | the call returns status 503 with message MSG-P7-003 And the load stays "Loaded" and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-005-05 | A personal field with no masking rule is masked | no masking rule in "MASK-SIT-01" covers party.date_of_birth for any role | test user "U-2105" holding RW-CASEOWN opens case "RW-2026-000123" | the date of birth shows masked as "XXXX-XX-XX" | RWB-E1-037 |
| AC-EXC-P4-005-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-005-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Hold the delegation of authority table as reference data

#### A2.6.1 Intent

**Business objective.** Keeps the approval limit per role and per decision as versioned data that the approval router reads.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Keeps the approval limit per role and per decision as versioned data that the approval router reads.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Security administrator | Opens the screen and hold the delegation of authority table as reference data | Checks the role, the capability area and the scope |
| 2 | Security administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-23

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-006-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Security administrator | Primary |
| Product head (Mortgage, HP, SSME), Risk and model risk officer | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-006-01 | Table loaded | the delegation of authority file "DOA-2026.11" built from Regulation กกค.540031 as amended by กกค.690070, with 95 limits | "U-3101" loads it with table "delegation_limit" and validFrom "2026-11-30" and "U-3102" approves it | 218 rows are stored: 109 decision and limit rows for MORTGAGE and 109 for SSME And every row has a decision code, an approval level and a product, and no two rows repeat the same decision, regulation item, product, level and limits And item 2.1.1 at level L4 is stored as two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit | RWB-E1-038 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-006-01 | Lookup | "DOA-2026.11" is in force | the router asks who may approve decision D6.4, item 2.1.1, product MORTGAGE, principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00 on 15 December 2026 | the lookup returns level L6, the row ID of item 2.1.1 at L6 and version "DOA-2026.11" | RWB-E1-038 |
| AC-ALT-P4-006-02 | Change | "DOA-2026.11" is in force And file "DOA-2027.01" adds a row for item 2.1.5 at level L5 with principal up to 10,000,000.00, validFrom "2027-01-01" | "U-3101" loads it and "U-3102" approves it | the rows of "DOA-2026.11" stay readable with valid_to "2026-12-31" And a lookup for D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 2 January 2027 returns L5 and version "DOA-2027.01" And one decision log entry records the approval of "DOA-2027.01" with its valid from date | RWB-E1-038 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-006-01 | A file with an error is refused whole | file "DOA-2026.12" gives item 2.1.1 at L5 a principal limit of 400,000,000.00, above the 300,000,000.00 of L4 And it gives one row the decision code "D6.9" | "U-3101" loads it | the load is refused with message MSG-P1-002 naming the falling limit and the unknown decision code And no row of "DOA-2026.12" is stored and "DOA-2026.11" stays in force | RWB-E1-038 |
| AC-EXC-P4-006-02 | The loader cannot approve and only Risk may | load "DOA-2027.01" was loaded by "U-3101" | "U-3101" calls approve on it | the call is refused with message MSG-P7-002 And when test user "U-3103" holding RW-PRODHEAD calls approve on it the call is refused with status 403 and message MSG-P4-002 | RWB-E1-038 |
| AC-EXC-P4-006-03 | An approval that cannot be recorded does not take effect | the decision log store is unavailable | "U-3102" approves load "DOA-2027.01" | the call returns status 503 with message MSG-P7-003 and the load stays "Loaded" | RWB-E1-038 |
| AC-EXC-P4-006-04 | No limit covers the request | "DOA-2026.11" holds no row for product HIRE_PURCHASE | the router asks who may approve decision D6.4, item 2.1.1, for HIRE_PURCHASE, principal 900,000.00 | the lookup returns "NOT_COVERED" And an incident is raised to the RW-RISK queue with message MSG-P7-010 naming D6.4 and HIRE_PURCHASE | RWB-E1-038 |
| AC-EXC-P4-006-05 | A write-off for a related party goes to the Board | "DOA-2026.11" is in force | the router asks who may approve decision D9.2, item 2.1.10, criteria met, product SSME, principal 300,000.00, with related party flag true | the lookup returns level L1 with reason "RELATED_PARTY" | RWB-E1-038 |
| AC-EXC-P4-006-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-006-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Write every access event to the access log

#### A2.7.1 Intent

**Business objective.** Records who looked at which case, which document and which data product, and when.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Records who looked at which case, which document and which data product, and when.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Write every access event to the access log | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** None

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-007-1 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Security administrator, Compliance and PDPA officer | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-007-01 | Read logged | test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026 | the case record view loads | one decision log entry is written with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15 And its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked" | RWB-E1-039 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-007-01 | Break-glass granted | incident "INC0004521" is open And the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00 | "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters | the grant is active until 14:30, the earlier of 4 hours and the group end And the banner shows MSG-P4-004 with time "14:30" And every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521" And at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" is allowed and marked with the grant And at 14:31 the same call is refused with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone | RWB-E1-039 |
| AC-ALT-P4-007-02 | Export logged | test user "U-4103" holding RW-TEAMMGR filters the case list by status "ASSIGNED" and product "MORTGAGE" and gets 37 rows | the user exports the list | one decision log entry is written with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID | RWB-E1-039 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-007-01 | Break-glass without an IAM grant is refused | test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with incident "INC0004521" | the call is refused with status 403 and message MSG-P4-007 And one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written | RWB-E1-039 |
| AC-EXC-P4-007-02 | Break-glass with a missing incident or a short reason is refused | test user "U-4102" is in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with no incident reference | the call is refused with status 422 and message MSG-GEN-001 for field "incidentReference" And when the user calls it with incident "INC0004521" and a reason of 12 characters the call is refused with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000 | RWB-E1-039 |
| AC-EXC-P4-007-03 | A read that cannot be logged returns nothing | the decision log store is unavailable | test user "U-4101" opens case "RW-2026-000123" | the call returns status 503 with message MSG-P7-003 and no case data And an incident is raised to the platform administrator queue | RWB-E1-039 |
| AC-EXC-P4-007-04 | Refusals are written to the decision log | test user "U-4106" holds only RW-PHONECOL | the user calls GET /admin/roles | the call is refused with MSG-P4-002 And one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written | RWB-E1-039 |
| AC-EXC-P4-007-05 | A repeated activation does not open a second grant | "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001" | the user sends the same request again with key "k-001" at 10:31 | the first response returns and no new entry is written And when the user sends a request with key "k-002" at 10:32 the call returns status 409 with message MSG-GEN-004 | RWB-E1-039 |
| AC-EXC-P4-007-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-007-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Write the access log into the decision log

#### A2.8.1 Intent

**Business objective.** Puts access events into the same append-only log, so access and decisions are queried together.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Puts access events into the same append-only log, so access and decisions are queried together.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Write the access log into the decision log | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-07, FEAT-DRI-01

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-008-1 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-008-01 | Read logged | test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026 | the case record view loads | one decision log entry is written with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15 And its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked" | RWB-E1-039 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-008-01 | Break-glass granted | incident "INC0004521" is open And the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00 | "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters | the grant is active until 14:30, the earlier of 4 hours and the group end And the banner shows MSG-P4-004 with time "14:30" And every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521" And at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" is allowed and marked with the grant And at 14:31 the same call is refused with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone | RWB-E1-039 |
| AC-ALT-P4-008-02 | Export logged | test user "U-4103" holding RW-TEAMMGR filters the case list by status "ASSIGNED" and product "MORTGAGE" and gets 37 rows | the user exports the list | one decision log entry is written with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID | RWB-E1-039 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-008-01 | Break-glass without an IAM grant is refused | test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with incident "INC0004521" | the call is refused with status 403 and message MSG-P4-007 And one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written | RWB-E1-039 |
| AC-EXC-P4-008-02 | Break-glass with a missing incident or a short reason is refused | test user "U-4102" is in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with no incident reference | the call is refused with status 422 and message MSG-GEN-001 for field "incidentReference" And when the user calls it with incident "INC0004521" and a reason of 12 characters the call is refused with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000 | RWB-E1-039 |
| AC-EXC-P4-008-03 | A read that cannot be logged returns nothing | the decision log store is unavailable | test user "U-4101" opens case "RW-2026-000123" | the call returns status 503 with message MSG-P7-003 and no case data And an incident is raised to the platform administrator queue | RWB-E1-039 |
| AC-EXC-P4-008-04 | Refusals are written to the decision log | test user "U-4106" holds only RW-PHONECOL | the user calls GET /admin/roles | the call is refused with MSG-P4-002 And one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written | RWB-E1-039 |
| AC-EXC-P4-008-05 | A repeated activation does not open a second grant | "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001" | the user sends the same request again with key "k-001" at 10:31 | the first response returns and no new entry is written And when the user sends a request with key "k-002" at 10:32 the call returns status 409 with message MSG-GEN-004 | RWB-E1-039 |
| AC-EXC-P4-008-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-008-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Use break-glass access with an incident reference

#### A2.9.1 Intent

**Business objective.** Lets an administrator take emergency access only against a named incident, and logs every use.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Lets an administrator take emergency access only against a named incident, and logs every use.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and use break-glass access with an incident reference | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Entra ID

**Prerequisites.** FEAT-ACA-07

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-009-1 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |
| Security administrator | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-009-01 | Read logged | test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026 | the case record view loads | one decision log entry is written with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15 And its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked" | RWB-E1-039 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-009-01 | Break-glass granted | incident "INC0004521" is open And the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00 | "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters | the grant is active until 14:30, the earlier of 4 hours and the group end And the banner shows MSG-P4-004 with time "14:30" And every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521" And at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" is allowed and marked with the grant And at 14:31 the same call is refused with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone | RWB-E1-039 |
| AC-ALT-P4-009-02 | Export logged | test user "U-4103" holding RW-TEAMMGR filters the case list by status "ASSIGNED" and product "MORTGAGE" and gets 37 rows | the user exports the list | one decision log entry is written with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID | RWB-E1-039 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-009-01 | Break-glass without an IAM grant is refused | test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with incident "INC0004521" | the call is refused with status 403 and message MSG-P4-007 And one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written | RWB-E1-039 |
| AC-EXC-P4-009-02 | Break-glass with a missing incident or a short reason is refused | test user "U-4102" is in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with no incident reference | the call is refused with status 422 and message MSG-GEN-001 for field "incidentReference" And when the user calls it with incident "INC0004521" and a reason of 12 characters the call is refused with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000 | RWB-E1-039 |
| AC-EXC-P4-009-03 | A read that cannot be logged returns nothing | the decision log store is unavailable | test user "U-4101" opens case "RW-2026-000123" | the call returns status 503 with message MSG-P7-003 and no case data And an incident is raised to the platform administrator queue | RWB-E1-039 |
| AC-EXC-P4-009-04 | Refusals are written to the decision log | test user "U-4106" holds only RW-PHONECOL | the user calls GET /admin/roles | the call is refused with MSG-P4-002 And one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written | RWB-E1-039 |
| AC-EXC-P4-009-05 | A repeated activation does not open a second grant | "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001" | the user sends the same request again with key "k-001" at 10:31 | the first response returns and no new entry is written And when the user sends a request with key "k-002" at 10:32 the call returns status 409 with message MSG-GEN-004 | RWB-E1-039 |
| AC-EXC-P4-009-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-009-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Review break-glass use

#### A2.10.1 Intent

**Business objective.** Puts every break-glass use in front of Compliance, and raises any use with no incident reference.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Puts every break-glass use in front of Compliance, and raises any use with no incident reference.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Compliance and PDPA officer | Opens the screen and review break-glass use | Checks the role, the capability area and the scope |
| 2 | Compliance and PDPA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-09

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-010-1 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| Compliance and PDPA officer | Primary |
| Security administrator, Internal audit | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-010-01 | Read logged | test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026 | the case record view loads | one decision log entry is written with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15 And its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked" | RWB-E1-039 |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-010-01 | Break-glass granted | incident "INC0004521" is open And the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00 | "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters | the grant is active until 14:30, the earlier of 4 hours and the group end And the banner shows MSG-P4-004 with time "14:30" And every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521" And at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" is allowed and marked with the grant And at 14:31 the same call is refused with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone | RWB-E1-039 |
| AC-ALT-P4-010-02 | Export logged | test user "U-4103" holding RW-TEAMMGR filters the case list by status "ASSIGNED" and product "MORTGAGE" and gets 37 rows | the user exports the list | one decision log entry is written with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID | RWB-E1-039 |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-010-01 | Break-glass without an IAM grant is refused | test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with incident "INC0004521" | the call is refused with status 403 and message MSG-P4-007 And one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written | RWB-E1-039 |
| AC-EXC-P4-010-02 | Break-glass with a missing incident or a short reason is refused | test user "U-4102" is in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with no incident reference | the call is refused with status 422 and message MSG-GEN-001 for field "incidentReference" And when the user calls it with incident "INC0004521" and a reason of 12 characters the call is refused with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000 | RWB-E1-039 |
| AC-EXC-P4-010-03 | A read that cannot be logged returns nothing | the decision log store is unavailable | test user "U-4101" opens case "RW-2026-000123" | the call returns status 503 with message MSG-P7-003 and no case data And an incident is raised to the platform administrator queue | RWB-E1-039 |
| AC-EXC-P4-010-04 | Refusals are written to the decision log | test user "U-4106" holds only RW-PHONECOL | the user calls GET /admin/roles | the call is refused with MSG-P4-002 And one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written | RWB-E1-039 |
| AC-EXC-P4-010-05 | A repeated activation does not open a second grant | "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001" | the user sends the same request again with key "k-001" at 10:31 | the first response returns and no new entry is written And when the user sends a request with key "k-002" at 10:32 the call returns status 409 with message MSG-GEN-004 | RWB-E1-039 |
| AC-EXC-P4-010-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-010-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Show the case record view read only

#### A2.11.1 Intent

**Business objective.** Gives one screen holding the case, its accounts, parties, collateral, documents and history.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Gives one screen holding the case, its accounts, parties, collateral, documents and history.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show the case record view read only | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-02

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-011-1 | A record outside the role's scope | MSG-P4-003 This case is not in your scope. |
| BR-P4-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Phone collector, Conduct and QA officer | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-011-01 | Loads fast | case RW-2026-000701 has 50 documents and 120 contact history entries | U-81 opens the case record view | the header, accounts, parties, contact history and the first page of documents show in under 2 seconds at the 95th percentile over 50 openings | RWB-E1-023 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-011-01 | Data from products | the account data product for 2026-12-02 holds days past due 97 and total balance THB 206,175.00 for account A-7001 | the view opens | the Accounts section shows 97 days past due and THB 206,175.00 for A-7001 And the section shows business date 2026-12-02 And the header shows queue "TDR-BKK-CO", owner U-81, status "IN_PROGRESS" and entry date 2026-11-30 | RWB-E1-023 |
| AC-ALT-P4-011-02 | Customer facts from the load | the customer profile for the borrower arrived in the COLLINS load of 2026-12-02 | the view opens | the Parties section shows the borrower with role "BORROWER", segment "RETAIL" and business date 2026-12-02 And the contact history shows the EFS entries with channel, direction, result and time | RWB-E1-023 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-011-01 | Document hub unavailable | the document hub does not answer within 3 seconds | U-81 opens the view | the Documents section shows MSG-P3-023 for "Documents" And the header, accounts, parties and contact history show | RWB-E1-023 |
| AC-EXC-P4-011-02 | Personal data access log unavailable | the personal data access log cannot be written | U-81 opens the view | the borrower's name and customer number show masked And the Parties section shows MSG-P3-023 for "Personal details" | RWB-E1-023 |
| AC-EXC-P4-011-03 | No documents and no contact history | case RW-2026-000703 has no documents and no contact history | its owner opens the view | the Documents and Contact history sections each show MSG-P3-024 | RWB-E1-023 |
| AC-EXC-P4-011-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-011-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Show the case record view with the history timeline

#### A2.12.1 Intent

**Business objective.** Adds the full event history to the case record view, in time order, with the rule version on each entry.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Adds the full event history to the case record view, in time order, with the rule version on each entry.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and show the case record view with the history timeline | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-012-1 | A record outside the role's scope | MSG-P4-003 This case is not in your scope. |
| BR-P4-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Conduct and QA officer, Internal audit | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-012-01 | Timeline order | case RW-2026-000801 has a rule transfer at 2026-12-02 08:10 by row "TRF-007" version "TRF-2026.11" And documents "Demand letter" stored at 2026-12-02 10:30 and "Title deed" at 2026-12-03 09:00 And a status change from "ASSIGNED" to "IN_PROGRESS" at 2026-12-03 11:15 by U-81 | the timeline opens | the four events show in the order transfer, demand letter, title deed, status change And the transfer shows "TRF-007" with version "TRF-2026.11" and the status change shows U-81 | RWB-E1-035 |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-012-01 | Transfer reason | a manual transfer at 2026-12-04 14:00 by team manager U-71 with transfer reason "R04" | the event is opened | the reason "R04 Owner absent", the from owner, the to owner and the rule version "TRF-2026.11" are shown | RWB-E1-035 |
| AC-ALT-P4-012-02 | A new case shows only its creation | case RW-2026-000802 was created on 2026-12-02 and its only record is the creation entry in the decision log | the timeline opens | one item shows with type "Case created", time 2026-12-02 and the entry rule version | RWB-E1-035 |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-012-01 | Decision log unavailable | the decision log query does not answer within 3 seconds | the timeline opens | the interactions, documents and assignments show in time order And the panel shows MSG-P3-023 for "Decisions" | RWB-E1-035 |
| AC-EXC-P4-012-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-012-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Apply joiner, mover and leaver changes to access

#### A2.13.1 Intent

**Business objective.** Adds, moves and removes a user's roles when their position changes, and reallocates their open cases.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Adds, moves and removes a user's roles when their position changes, and reallocates their open cases.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Security administrator | Opens the screen and apply joiner, mover and leaver changes to access | Checks the role, the capability area and the scope |
| 2 | Security administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Entra ID, Workbench

**Prerequisites.** FEAT-ACA-04

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-013-1 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| Security administrator | Primary |
| Team manager | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-013-01 | Matrix as data | test user "U-2101" holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01" And the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11" And test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | test user "U-2103" holding RW-LEGAL signs in on 1 December 2026 and calls GET /queues | the call returns status 200, where under "PM-2026.11" it returned 403, with no deployment And one decision log entry exists with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102" | RWB-E1-037 |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-013-01 | Masking | test user "U-2104" holds only RW-PHONECOL | the user opens case "RW-2026-000123" in the case record view | the borrower's identity number shows as "XXXXXXXXX1234" and the phone number as "XXXXXX5678" And no request is made to the ACE PII service for clear values And the view is written to the access event stream with the case ID and the fields shown masked | RWB-E1-037 |
| AC-ALT-P4-013-02 | Denied action | test user "U-2105" holds only RW-CASEOWN, whose Queue and allocation letter is "R" | the user calls POST /cases/{caseId}/transfer for case "RW-2026-000123" | the call is refused with status 403 and message MSG-P4-002 before the handler runs And the case owner and queue are unchanged And one refusal event is written with area "QUEUE_AND_ALLOCATION" and right "U" | RWB-E1-037 |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-013-01 | A case outside the scope is not returned | test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases And case "RW-2026-000456" belongs to team "MTG-NE" and another owner | the user calls GET /cases | 12 cases return and the total is 12 And GET /cases/{caseId} for "RW-2026-000456" returns status 404 with message MSG-P4-003 | RWB-E1-037 |
| AC-EXC-P4-013-02 | A matrix file with an error is refused whole | matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting | test user "U-2101" loads it | the load is refused with message MSG-P1-002 naming the duplicate row and the invalid letters And no row of "PM-2026.13" is stored and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-013-03 | The loader cannot approve, and only the table's approver role may | load "PM-2026.12" was loaded by test user "U-2101" | "U-2101" calls approve on that load | the call is refused with message MSG-P7-002 and the load stays "Loaded" And when test user "U-2106" holding RW-COE calls approve on that load the call is refused with status 403 and message MSG-P4-002 | RWB-E1-037 |
| AC-EXC-P4-013-04 | An approval that cannot be recorded does not take effect | the decision log store is unavailable | test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | the call returns status 503 with message MSG-P7-003 And the load stays "Loaded" and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-013-05 | A personal field with no masking rule is masked | no masking rule in "MASK-SIT-01" covers party.date_of_birth for any role | test user "U-2105" holding RW-CASEOWN opens case "RW-2026-000123" | the date of birth shows masked as "XXXX-XX-XX" | RWB-E1-037 |
| AC-EXC-P4-013-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-013-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Scope a user's cases by team and region

#### A2.14.1 Intent

**Business objective.** Limits what each user sees to the cases their role, team and region permit.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Limits what each user sees to the cases their role, team and region permit.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Scope a user's cases by team and region | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-04

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-014-1 | A record outside the role's scope | MSG-P4-003 This case is not in your scope. |
| BR-P4-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Security administrator | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-014-01 | Matrix as data | test user "U-2101" holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01" And the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11" And test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | test user "U-2103" holding RW-LEGAL signs in on 1 December 2026 and calls GET /queues | the call returns status 200, where under "PM-2026.11" it returned 403, with no deployment And one decision log entry exists with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102" | RWB-E1-037 |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-014-01 | Masking | test user "U-2104" holds only RW-PHONECOL | the user opens case "RW-2026-000123" in the case record view | the borrower's identity number shows as "XXXXXXXXX1234" and the phone number as "XXXXXX5678" And no request is made to the ACE PII service for clear values And the view is written to the access event stream with the case ID and the fields shown masked | RWB-E1-037 |
| AC-ALT-P4-014-02 | Denied action | test user "U-2105" holds only RW-CASEOWN, whose Queue and allocation letter is "R" | the user calls POST /cases/{caseId}/transfer for case "RW-2026-000123" | the call is refused with status 403 and message MSG-P4-002 before the handler runs And the case owner and queue are unchanged And one refusal event is written with area "QUEUE_AND_ALLOCATION" and right "U" | RWB-E1-037 |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-014-01 | A case outside the scope is not returned | test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases And case "RW-2026-000456" belongs to team "MTG-NE" and another owner | the user calls GET /cases | 12 cases return and the total is 12 And GET /cases/{caseId} for "RW-2026-000456" returns status 404 with message MSG-P4-003 | RWB-E1-037 |
| AC-EXC-P4-014-02 | A matrix file with an error is refused whole | matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting | test user "U-2101" loads it | the load is refused with message MSG-P1-002 naming the duplicate row and the invalid letters And no row of "PM-2026.13" is stored and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-014-03 | The loader cannot approve, and only the table's approver role may | load "PM-2026.12" was loaded by test user "U-2101" | "U-2101" calls approve on that load | the call is refused with message MSG-P7-002 and the load stays "Loaded" And when test user "U-2106" holding RW-COE calls approve on that load the call is refused with status 403 and message MSG-P4-002 | RWB-E1-037 |
| AC-EXC-P4-014-04 | An approval that cannot be recorded does not take effect | the decision log store is unavailable | test user "U-2102" holding RW-SECADM approves load "PM-2026.12" | the call returns status 503 with message MSG-P7-003 And the load stays "Loaded" and "PM-2026.11" stays in force | RWB-E1-037 |
| AC-EXC-P4-014-05 | A personal field with no masking rule is masked | no masking rule in "MASK-SIT-01" covers party.date_of_birth for any role | test user "U-2105" holding RW-CASEOWN opens case "RW-2026-000123" | the date of birth shows masked as "XXXX-XX-XX" | RWB-E1-037 |
| AC-EXC-P4-014-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-014-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Run the release checklist, training and go-live readiness

#### A2.15.1 Intent

**Business objective.** Works the checklist that says the release can go to production: tests, training, run books, rollback.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Works the checklist that says the release can go to production: tests, training, run books, rollback.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Tribe lead and squad members | Opens the screen and run the release checklist, training and go-live readiness | Checks the role, the capability area and the scope |
| 2 | Tribe lead and squad members | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** None

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-015-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Tribe lead and squad members | Primary |
| Platform administrator, Team manager | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-015-01 | Run the release checklist, training and go-live readiness | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.16 Answer an access audit query

#### A2.16.1 Intent

**Business objective.** Returns who accessed a case or a document over a period, from the access log.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Returns who accessed a case or a document over a period, from the access log.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Internal audit | Opens the screen and answer an access audit query | Checks the role, the capability area and the scope |
| 2 | Internal audit | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-08

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-016-1 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Internal audit | Primary |
| Compliance and PDPA officer, Security administrator | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-016-01 | Read logged | test user "U-4101" holding RW-CASEOWN opens case "RW-2026-000123" at 10:15 on 3 December 2026 | the case record view loads | one decision log entry is written with decision code "AC-READ", actor "U-4101", the case ID and decided at 10:15 And its actions list the field IDs returned, with DF-PTY-007 and DF-PTY-016 marked "masked" | RWB-E1-039 |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P4-016-01 | Break-glass granted | incident "INC0004521" is open And the security administrator approved IAM request "IAM-778812" and the IAM added test user "U-4102" holding RW-PLATADM to group "RWB-SIT-BREAKGLASS" until 18:00 | "U-4102" calls POST /admin/break-glass at 10:30 with incident "INC0004521", request "IAM-778812", area "CASE_RECORD", right "U", scope "ALL" and a reason of 46 characters | the grant is active until 14:30, the earlier of 4 hours and the group end And the banner shows MSG-P4-004 with time "14:30" And every entry written for "U-4102" until 14:30 carries the grant ID and incident "INC0004521" And at 14:20 PATCH /tasks/{taskId} on case "RW-2026-000123" by "U-4102" is allowed and marked with the grant And at 14:31 the same call is refused with MSG-P4-002, because RW-PLATADM holds only "R" in Case record, with no action by anyone | RWB-E1-039 |
| AC-ALT-P4-016-02 | Export logged | test user "U-4103" holding RW-TEAMMGR filters the case list by status "ASSIGNED" and product "MORTGAGE" and gets 37 rows | the user exports the list | one decision log entry is written with decision code "AC-EXPT", actor "U-4103", the filter, row count 37 and no case ID | RWB-E1-039 |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-016-01 | Break-glass without an IAM grant is refused | test user "U-4104" holds RW-PLATADM and is not in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with incident "INC0004521" | the call is refused with status 403 and message MSG-P4-007 And one entry with decision code "AC-DENY" and reason "NO_BREAKGLASS_GRANT" is written | RWB-E1-039 |
| AC-EXC-P4-016-02 | Break-glass with a missing incident or a short reason is refused | test user "U-4102" is in group "RWB-SIT-BREAKGLASS" | the user calls POST /admin/break-glass with no incident reference | the call is refused with status 422 and message MSG-GEN-001 for field "incidentReference" And when the user calls it with incident "INC0004521" and a reason of 12 characters the call is refused with status 422 and message MSG-GEN-002 for field "reason" with min 20 and max 1000 | RWB-E1-039 |
| AC-EXC-P4-016-03 | A read that cannot be logged returns nothing | the decision log store is unavailable | test user "U-4101" opens case "RW-2026-000123" | the call returns status 503 with message MSG-P7-003 and no case data And an incident is raised to the platform administrator queue | RWB-E1-039 |
| AC-EXC-P4-016-04 | Refusals are written to the decision log | test user "U-4106" holds only RW-PHONECOL | the user calls GET /admin/roles | the call is refused with MSG-P4-002 And one entry with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "R" and no case ID is written | RWB-E1-039 |
| AC-EXC-P4-016-05 | A repeated activation does not open a second grant | "U-4102" activated break-glass at 10:30 with Idempotency-Key "k-001" | the user sends the same request again with key "k-001" at 10:31 | the first response returns and no new entry is written And when the user sends a request with key "k-002" at 10:32 the call returns status 409 with message MSG-GEN-004 | RWB-E1-039 |
| AC-EXC-P4-016-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-016-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.17 Run the full administration screens

#### A2.17.1 Intent

**Business objective.** Gives administration one place for roles, queues, parameters, templates, panels and autonomy.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Gives administration one place for roles, queues, parameters, templates, panels and autonomy.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and run the full administration screens | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-22

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-017-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |
| Center of excellence analyst, Security administrator | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-017-01 | Run the full administration screens | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-017-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-017-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.18 Change a decision rule through the administration screens

#### A2.18.1 Intent

**Business objective.** Lets the center of excellence change a rule, test it and put it in force as a new version.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Lets the center of excellence change a rule, test it and put it in force as a new version.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and change a decision rule through the administration screens | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Rules component

**Prerequisites.** FEAT-CWC-14

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-018-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Risk and model risk officer | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-018-01 | Change a decision rule through the administration screens | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-018-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-018-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.19 Move an approval limit

#### A2.19.1 Intent

**Business objective.** Changes a delegated limit, with Risk approving and the change versioned.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Changes a delegated limit, with Risk approving and the change versioned.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and move an approval limit | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-06

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-019-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Risk and model risk officer, Security administrator | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-019-01 | Move an approval limit | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-019-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-019-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.20 Set the treatment policy by product

#### A2.20.1 Intent

**Business objective.** Lets the product head set the bands, floors and ranges for their product.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Lets the product head set the bands, floors and ranges for their product.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Product head (Mortgage, HP, SSME) | Opens the screen and set the treatment policy by product | Checks the role, the capability area and the scope |
| 2 | Product head (Mortgage, HP, SSME) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-25

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-020-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| Product head (Mortgage, HP, SSME) | Primary |
| Center of excellence analyst | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-020-01 | Set the treatment policy by product | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-020-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-020-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.21 Add a letter template with Compliance approval

#### A2.21.1 Intent

**Business objective.** Adds a new template through the approval path and records who approved it.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Adds a new template through the approval path and records who approved it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and add a letter template with Compliance approval | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-15

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-021-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Compliance and PDPA officer, Legal counsel | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-021-01 | Add a letter template with Compliance approval | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-021-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-021-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.22 Roll back a configuration version

#### A2.22.1 Intent

**Business objective.** Returns any versioned table to its previous version and records the rollback.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.22.2 Description

**Functional overview.** Returns any versioned table to its previous version and records the rollback.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and roll back a configuration version | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-15

#### A2.22.3 Business rules and structure

##### A2.22.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-022-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-022 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.22.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.22.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |
| Center of excellence analyst | Also uses |

#### A2.22.4 Acceptance criteria

##### A2.22.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-022-01 | Roll back a configuration version | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.22.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.22.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-022-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-022-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.22.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.23 Publish a panel change

#### A2.23.1 Intent

**Business objective.** Puts a partner panel change in force with an effective date.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.23.2 Description

**Functional overview.** Puts a partner panel change in force with an effective date.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Partner and agency manager | Opens the screen and publish a panel change | Checks the role, the capability area and the scope |
| 2 | Partner and agency manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Partner portal

**Prerequisites.** FEAT-PRM-02

#### A2.23.3 Business rules and structure

##### A2.23.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-023-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-023 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.23.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.23.3.3 Roles and permissions

| Role | Use |
|---|---|
| Partner and agency manager | Primary |
| Reference data administrator | Also uses |

#### A2.23.4 Acceptance criteria

##### A2.23.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-023-01 | Publish a panel change | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.23.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.23.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-023-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-023-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.23.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.24 Run a QA sample against the rule version applied

#### A2.24.1 Intent

**Business objective.** Samples closed decisions and tests each against the rule version that was in force.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.24.2 Description

**Functional overview.** Samples closed decisions and tests each against the rule version that was in force.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Conduct and QA officer | Opens the screen and run a QA sample against the rule version applied | Checks the role, the capability area and the scope |
| 2 | Conduct and QA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-03

#### A2.24.3 Business rules and structure

##### A2.24.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-024-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P4-024 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.24.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.24.3.3 Roles and permissions

| Role | Use |
|---|---|
| Conduct and QA officer | Primary |
| Center of excellence analyst, Internal audit | Also uses |

#### A2.24.4 Acceptance criteria

##### A2.24.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-024-01 | Run a QA sample against the rule version applied | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.24.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.24.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-024-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-024-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.24.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.25 Return a defective pack

#### A2.25.1 Intent

**Business objective.** Sends a pack that fails the check back to its owner with the defects named.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.25.2 Description

**Functional overview.** Sends a pack that fails the check back to its owner with the defects named.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Return a defective pack | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-LIT-05

#### A2.25.3 Business rules and structure

##### A2.25.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-025-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P4-025 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.25.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.25.4 Acceptance criteria

##### A2.25.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-025-01 | Return a defective pack | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.25.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.25.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-025-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-025-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.25.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.26 Detect a broken hash chain in the decision log

#### A2.26.1 Intent

**Business objective.** Tests the log chain and raises a control breach if a record does not verify.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.26.2 Description

**Functional overview.** Tests the log chain and raises a control breach if a record does not verify.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Detect a broken hash chain in the decision log | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-01

#### A2.26.3 Business rules and structure

##### A2.26.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-026-1 | A record outside the role's scope | MSG-P4-003 This case is not in your scope. |
| BR-P4-026 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.26.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit | Also uses |

#### A2.26.4 Acceptance criteria

##### A2.26.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-026-01 | Detect a broken hash chain in the decision log | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.26.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.26.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-026-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-026-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.26.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.27 Handle a data subject request

#### A2.27.1 Intent

**Business objective.** Works a PDPA access, correction or erasure request inside the statutory period.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.27.2 Description

**Functional overview.** Works a PDPA access, correction or erasure request inside the statutory period.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Compliance and PDPA officer | Opens the screen and handle a data subject request | Checks the role, the capability area and the scope |
| 2 | Compliance and PDPA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-05

#### A2.27.3 Business rules and structure

##### A2.27.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-027-1 | Sign-in with no Workbench role | MSG-P4-001 You have no Recovery Workbench role. Ask your team manager to request one. |
| VR-P4-027-2 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-027 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.27.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.27.3.3 Roles and permissions

| Role | Use |
|---|---|
| Compliance and PDPA officer | Primary |
| Security administrator | Also uses |

#### A2.27.4 Acceptance criteria

##### A2.27.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-027-01 | Handle a data subject request | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.27.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.27.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-027-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-027-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.27.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.28 Manage an incident

#### A2.28.1 Intent

**Business objective.** Runs the incident path: detect, hold, fix, record and report.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.28.2 Description

**Functional overview.** Runs the incident path: detect, hold, fix, record and report.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and manage an incident | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Log Analytics, Workbench

**Prerequisites.** FEAT-DRI-18

#### A2.28.3 Business rules and structure

##### A2.28.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-028-1 | A record outside the role's scope | MSG-P4-003 This case is not in your scope. |
| BR-P4-028 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.28.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.28.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |
| Tribe lead and squad members | Also uses |

#### A2.28.4 Acceptance criteria

##### A2.28.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-028-01 | Manage an incident | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.28.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.28.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-028-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-028-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.28.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.29 Refer a case to Aric

#### A2.29.1 Intent

**Business objective.** Sends a case to Aric where the fraud rules require it, and takes the result back.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.29.2 Description

**Functional overview.** Sends a case to Aric where the fraud rules require it, and takes the result back.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Refer a case to Aric | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Aric

**Prerequisites.** FEAT-DVF-04

#### A2.29.3 Business rules and structure

##### A2.29.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-029-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P4-029 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.29.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Fraud investigator | Also uses |

#### A2.29.4 Acceptance criteria

##### A2.29.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-029-01 | Refer a case to Aric | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.29.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.29.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-029-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-029-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.29.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.30 Control access by role and by agent

#### A2.30.1 Intent

**Business objective.** Reviews and sets what each role and each agent may read and do, and reports the matrix.

**Problem.** Access, limits and rules live in documents and people's heads; changes need code or manual checks.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Rule and limit changes made without a code release | 100 percent | Decision log and Workbench records | Monthly |

#### A2.30.2 Description

**Functional overview.** Reviews and sets what each role and each agent may read and do, and reports the matrix.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Security administrator | Opens the screen and control access by role and by agent | Checks the role, the capability area and the scope |
| 2 | Security administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Entra ID

**Prerequisites.** FEAT-ACA-04

#### A2.30.3 Business rules and structure

##### A2.30.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P4-030-1 | Break-glass access is active | MSG-P4-004 Emergency access is on until {time}. Every action is recorded. |
| BR-P4-030 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.30.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | No |
| role.role_name | Role name | varchar(80) | Yes | None | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | No |
| permission.role_id | The role this record belongs to | uuid | Yes | None | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | No |

##### A2.30.3.3 Roles and permissions

| Role | Use |
|---|---|
| Security administrator | Primary |
| Compliance and PDPA officer, Risk and model risk officer | Also uses |

#### A2.30.4 Acceptance criteria

##### A2.30.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P4-030-01 | Control access by role and by agent | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.30.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.30.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P4-030-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P4-030-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.30.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-ACA-001 | Every user signs on through Entra ID single sign-on with multi-factor authentication. | Must | E1 |
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release. | Must | E1 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do. | Must | E1 |
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit. | Must | E1 |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call. | Must | E1 |
| REQ-ACA-006 | Every read of the case store, the document store and the data lake copy is written to the access log. | Must | E1 |
| REQ-ACA-007 | Access requested outside the authority matrix is refused and the refusal is recorded. | Must | E1 |
| REQ-ACA-008 | A break-glass path exists for an emergency, needs its own approval, and writes to the access log. | Must | E1 |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow. | Must | E1 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people. | Must | E1 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench so that access matches the current organization. | Must | E2 |
| REQ-ACA-012 | Partner users reach the Workbench only through the external gateway, with multi-factor authentication, scoped to their own cases. | Must | E2 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator. | Should | E8 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-39 Rules and parameters | Rule versions, route sets, thresholds and timers, with the load and approval | E8; by file load before |
| SCR-40 Reference data | Lists of values and reference tables with versions | E8; by file load before |
| SCR-41 Delegation of authority | Approval levels, holders, limits and substitutes | E8; by file load before |
| SCR-42 Queues and service levels | Queues, caps, overflow and service levels per state | E8; by file load before |
| SCR-43 Roles and access | Roles, permissions, scope and the group mapping, with the access log | E8; by file load before |
| SCR-47 Personal data | Retention classes, masking rules, consent log and data subject requests | E8; by file load before |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| FSD owner, business analyst | | | |
| Business owner | | | |
| Solution architect | | | |
| QA lead | | | |

## Appendix A. Business glossary

Terms follow the Recovery Workbench Business Glossary.

| Term | Thai | Meaning |
|---|---|---|
| Case owner | ผู้รับผิดชอบกรณี | The person who holds the case from day 90 to close and answers for its outcome |
| Sentry | เงื่อนไขเปิดปิดขั้นตอน | A rule that lets a stage, task or milestone start or finish when an event occurs and its condition holds |
| Approval level | ระดับอำนาจอนุมัติ | One of the six levels of the bank approval authority regulation that may approve a decision |
| Delegation of authority table | ตารางมอบอำนาจอนุมัติ | The limits each approval level may approve, by decision, product and amount |
| Rule | กฎ | One row of a decision table: from state, event and condition in; action, next state, owner and timer out |
| Rule version | ฉบับของกฎ | The version of a rule in force when a decision was made |
| Agent | เอเจนต์ | An AI component that prepares and recommends through the tool gateway |
| Borrower | ผู้กู้ | The party the loan was made to |
| Co-borrower | ผู้กู้ร่วม | A party who borrowed jointly with the borrower |
| Guarantor | ผู้ค้ำประกัน | A party who guaranteed the loan |
| Heir | ทายาท | A party who represents a deceased borrower's estate |
| Legal Execution Department | กรมบังคับคดี | The government department that runs enforcement auctions |
| Role | บทบาท | A job function with the permissions it needs |
| Permission | สิทธิ์ | A letter C, R, U, D or A in one capability area |
| Scope | ขอบเขตการเข้าถึง | Which cases a role sees: own, team, region or all |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
