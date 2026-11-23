SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P4 rwb-access
description: Product requirements for the rwb-access microservice (module P4 Access and administration), derived from the program, Epic 1, Epic 2 and Epics 3 to 8 business requirements, the P4 functional specification v3, the P4 technical specification v3 and the Architecture v5 service contract.
status: Draft
brd:
  - 03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx
  - 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v4.docx
  - 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v2.docx
  - 03 Requirements and specifications/Recovery Workbench Epics 3 to 8 Specification v3.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P4 Access and administration v3.md
tsd: 03 Requirements and specifications/Recovery Workbench Technical Specifications by Module v5/Recovery Workbench TSD P4 Access and administration v3.md
architecture: 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md
ownership_map: 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx
decision: D-RCV-60
service: P4 rwb-access
---

# Recovery Workbench PRD P4 rwb-access

## 1. Document control and change log

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P4 rwb-access |
| Document ID | P4-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Date | 22 November 2026 |
| Classification | Confidential |
| Decision | D-RCV-60 (microservice realignment) |
| Service | P4 · rwb-access · schema `rwb_access` · base `/api/recovery/access/v1` · topic `rwb.access.events.v1` · task queue `rwb-access` · wave 1 |
| Service epic | RWB-SVC-P4 |
| Business epics served | EP01, EP02, EP08 |
| Built from | Business Requirements Program v4 (15 November 2026); Business Requirements Epic 1 v4 (15 November 2026, release 30 November 2026); Business Requirements Epic 2 v2 (28 October 2026, release 31 December 2026); Epics 3 to 8 Specification v3; FSD P4 Access and administration v3 (15 November 2026); TSD P4 Access and administration v3 (16 November 2026); Architecture v5; Microservice Ownership Map v1 |
| Product owner | Product owner (to be recorded at approval) |
| Requirements analyst | Business analyst, P4 |
| Approval gate | Requirements approval, by the Product Owner and the FDA |

### 1.1 Change log

| Version | Date | Change | Decision | Tool |
|---|---|---|---|---|
| 1 | 22 November 2026 | First PRD for rwb-access. Turns the P4 business requirements (REQ-ACA-001 to REQ-ACA-013) and the P4 functional specification v3 into 14 capabilities, 38 functional requirements, 20 non-functional requirements and 32 acceptance criteria for one service. Applies the service split of Architecture v5 and the Ownership Map: reference-data load surfaces move to rwb-case, rule package administration moves to rwb-decision, the smoke workflow moves to the platform, `lov_value` stays with rwb-case and `partner_user` with rwb-partner. Dates are unchanged and tentative. | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1.2 Baseline versions carried forward unchanged

| Source | Version and date | Carried into this PRD |
|---|---|---|
| Business Requirements Program | v4, 15 November 2026 | REQ-ACA-001 to REQ-ACA-013, outcomes, user classes |
| Business Requirements Epic 1 | v4, 15 November 2026, release 30 November 2026 | RWB-E1-022, RWB-E1-037, RWB-E1-038, RWB-E1-039 |
| Business Requirements Epic 2 | v2, 28 October 2026, release 31 December 2026 | RWB-E2-019 |
| Epics 3 to 8 Specification | v3 | FEAT-ADM-01 to FEAT-ADM-14 |
| FSD P4 Access and administration | v3, 15 November 2026 | A1.2 features, A2.1 to A2.30 behaviour, REQ-ACA-001 to REQ-ACA-013 |
| TSD P4 Access and administration | v3, 16 November 2026 | T3 tables and DF-REF ids, T3.2 lists, T6.1 matrix, T6.3 audit, T7 NFR references |
| Architecture v5 | v5 | Service contract, schema, topic, queue, wave, JOB-18, events |
| Non-Functional Specification | v3, 15 November 2026 | NFR-001 to NFR-078 values referenced in section 7 |

## 2. Product overview and relationship to ACE

### 2.1 What the product is

rwb-access is the authority of the Recovery Workbench. It answers three questions for every other service and every screen: who is this user, what may they do here, and what may they see. It holds the Recovery roles, the role to permission matrix, the masking policy and the delegation of authority table as versioned data, keeps the access log, and runs the break-glass path. It is a reference-data owner: it publishes access policy changes and consumes no business events.

### 2.2 What is reused from ACE and what is new

| Capability | Verdict | Owning document | What this PRD does with it |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | rwb-access answers the access question; sign-in, the session certificate and the audit and PII log stay ACE |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the rwb-case contract; the case record view screen is rwb-case's |
| Notification path | REUSE | ACE notification path | Not used by this service |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from rwb-case; rwb-access runs no case workflow |
| Decision record and audit trail | REUSE | Audit and Logging Design | Access events are decision records; the central ledger is rwb-decision's |
| Role and permission matrix | EXTEND | Users Roles and Permissions | Recovery roles as data on the ACE access check (new work) |
| Delegation of authority table | EXTEND | Users Roles and Permissions | New versioned table read by the approval router |
| Temporal, outbox, inbox, idempotency | REUSE | Platform library (RWB-PLT) | Constraints only: the service template supplies the outbox, inbox, idempotency and decision-record objects in `rwb_access` |
| Reference data loads, lists of values | REUSE (other service) | rwb-case | Out of this service under the Ownership Map; a dependency |

### 2.3 Confirmed Architecture v5 constraints (constraints, not design)

| Constraint | Value | Source |
|---|---|---|
| Service, schema, topic, queue, wave | rwb-access · `rwb_access` · `rwb.access.events.v1` · `rwb-access` · wave 1 | Architecture v5 slide 41 |
| First API path | `/authorise` | Architecture v5 slide 41 |
| Inputs (IN) | `POST /authorise` (role, scope, DoA) · `GET /me/permissions` · `GET /doa-limits` · `/masking-policies` | Architecture v5 slide 14 |
| Events published | `AccessPolicyChanged`, `DoaLimitChanged` on `rwb.access.events.v1`; consumers refresh their cache | Architecture v5 slides 14 and 43 |
| Events consumed | None: reference-data owner | Architecture v5 slide 14 |
| Scheduled work | One Schedule: access review list, six-monthly (JOB-18) | Architecture v5 slides 14 and 44 |
| Owned data | Recovery roles as data, scope, masking policy, DoA table, access log | Architecture v5 slides 14 and 41 |
| ACE use | ACE Common sign-in and group-to-role through Entra ID | Architecture v5 slide 14 |
| Service template duties | Own schema with outbox, inbox and decision record; publish `DecisionRecorded`; `/health` and `/metrics`; OpenTelemetry | Architecture v5 slide 20 |
| Idempotency | `Idempotency-Key` on every POST, with the stored response | Architecture v5 slide 11 |

### 2.4 What this PRD does not claim

The Ownership Map moves four groups of behaviour out of P4. They stay in scope of the programme but not of this service, and this PRD lists them as dependencies, not requirements:

| Behaviour moved | Owner under the Ownership Map | Reason |
|---|---|---|
| `/admin/lists/{listCode}` and `/admin/reference-loads`, with approve, verify and rollback | P3 rwb-case | Parameters and reference data (E1-042, E1-043) are rwb-case's; P4 keeps only its role, scope, masking and DoA tables |
| Rule package registry, rule rows, rule test cases, the rule-package paths and the change report | P7 rwb-decision | Rule governance is central in rwb-decision; each service holds a local evaluated copy |
| `POST /admin/workflows/smoke` | PLT platform library | The smoke workflow runs on the platform task queue under the platform administrator (`GAP-1566`) |
| `lov_value`, `partner_user`, feature flags, outbox, inbox, idempotency, `decision_record` objects | P3, S9 and PLT | Reference data, partner identities and library objects |

## 3. Personas and roles

### 3.1 Role classes

| Class | Count (BRD Program v4, section 3) | In this PRD |
|---|---|---|
| Bank user | 37 roles | Holds Recovery roles; every access decision is about these |
| Partner user | 7 roles | Reaches the Workbench through the external gateway and rwb-partner; rwb-access answers MFA and scope |
| Customer party | 4 roles | No Workbench access; appears as a masked data subject in a personal field |
| Non-human actor | 6 roles | Service identities for jobs and agents; checked like people |

### 3.2 Roles that interact with rwb-access

Roles and single letters are held as data (TSD P4 T6.1). "R" read, "C" create, "U" update, "D" delete, "A" approve, "-" none.

| Role code | Role | Class | Interaction with rwb-access |
|---|---|---|---|
| RW-CASEOWN | Case owner | Bank user | Signs in; reads cases inside scope; sees masked personal fields |
| RW-TEAMMGR | Team manager | Bank user | Signs in; reads the team's cases; exports a filtered list (logged) |
| RW-PHONECOL | Phone collector | Bank user | Signs in; masked personal fields; no administration menu |
| RW-FIELDCOL | Field collector | Bank user | Signs in; masked personal fields |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | Signs in; approves inside the DoA limit |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | Signs in; masked personal fields |
| RW-COMPLAIN | Complaint officer | Bank user | Signs in |
| RW-FRAUD | Fraud investigator | Bank user | Signs in |
| RW-LITOFF | Litigation officer | Bank user | Signs in; holds two roles in the union case (RW-LITOFF with RW-LEGAL) |
| RW-ENFORCE | Enforcement owner | Bank user | Signs in |
| RW-LEGAL | Legal counsel | Bank user | Signs in; reference data RU |
| RW-SALEOFF | Sale officer | Bank user | Signs in |
| RW-NPAMGR | NPA and asset manager | Bank user | Signs in |
| RW-DEBTSALE | Debt sale officer | Bank user | Signs in |
| RW-WRITEOFF | Write-off team member | Bank user | Signs in |
| RW-CREDITAD | Credit Administration officer | Bank user | Signs in |
| RW-GUARANT | Guarantee officer | Bank user | Signs in |
| RW-AGENCYMG | Partner and agency manager | Bank user | Signs in; partner panel changes (FEAT-ADM-07, rwb-partner) |
| RW-CONDUCT | Conduct and QA officer | Bank user | Signs in; QA sample against the rule version applied |
| RW-CAPACITY | Capacity and workforce planner | Bank user | Signs in |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | Signs in; DoA change consulted |
| RW-HEADLIT | Head of Litigation | Bank user | Signs in |
| RW-HEADNPA | Head of NPA | Bank user | Signs in |
| RW-HEADASL | Head of Asset Liquidity | Bank user | Signs in |
| RW-CREDCOMM | Credit approval committee member | Bank user | Signs in; DoA lookup above the officer's limit |
| RW-WOCOMM | Write-off committee member | Bank user | Signs in; DoA lookup for write-off decisions |
| RW-RISK | Risk and model risk officer | Bank user | Approves a DoA version (author cannot approve); DoA lookup exception queue |
| RW-COE | Center of excellence analyst | Bank user | Rules and reference data CRUD; prepares administrative changes |
| RW-DATASTEW | Data steward and data product owner | Bank user | Platform administration R |
| RW-FINANCE | Finance and CFO delegate | Bank user | Signs in |
| RW-AUDIT | Internal audit | Bank user | Reads the matrix, the access log and the policy versions (R) |
| RW-COMPLY | Compliance and PDPA officer | Bank user | Reviews break-glass use, data subject requests and masked-field coverage |
| RW-PLATADM | Platform administrator | Bank user | Activates break-glass; operates the administration surface (C) |
| RW-REFADM | Reference data administrator | Bank user | Prepares the load file and the change checklist; no approval |
| RW-SECADM | Security administrator | Bank user | Owns roles, permissions, scope and masking; approves a matrix version (A); receives role-conflict incidents |
| RW-BIANAL | Reporting and BI analyst | Bank user | Reads measures; no access administration |
| RW-TRIBE | Tribe lead and squad members | Bank user | Signs in |
| SY-CASEWF | Case workflow module | Non-human actor | Calls the authorise answer; passes scope-filtered reads |
| SY-RULES | Drools evaluator | Non-human actor | Reads the package version in force; no access administration |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | Reference data R |
| SY-OCR | OCR and extraction pipeline | Non-human actor | Documents only |
| SY-AGENT | Agent platform | Non-human actor | Calls the authorise and masking answers for every agent action |

### 3.3 Capability areas used by the matrix

The matrix holds one row per role per capability area, with the letters C, R, U, D and A (TSD P4 T3.2, LOV-CAPABILITY): CASE_RECORD, QUEUE_AND_ALLOCATION, TREATMENT_AND_OFFER, LITIGATION, ASSET_AND_DISPOSAL, DEBT_SALE, WRITE_OFF_AND_POSTING, DOCUMENTS, RULES_AND_PARAMETERS, REFERENCE_DATA, DECISION_LOG, PARTNER_PORTAL, REPORTING, PLATFORM_ADMINISTRATION. Fourteen areas, fixed by the list of values, not by code.

## 4. User journeys

### 4.1 Journey A — sign in and open a case (current versus target)

| Step | Current (today) | Target (rwb-access) |
|---|---|---|
| 1 | A user signs on to several systems with different credentials | One Entra ID sign-on with a second factor through the ACE front end |
| 2 | Rights are held in a spreadsheet and checked by a person | Roles come from Entra groups mapped to versioned role rows; a group with no active role gives no right |
| 3 | A role clash is found in an audit | A conflicting role pair is refused at sign-in, an incident goes to the security administrator and a refusal is logged |
| 4 | Screens show whatever the screen decides | The session carries roles, scope, matrix version and conflict version; every call passes one authorise check |
| 5 | Personal data shows to whoever opens the screen | Personal fields are masked by role and by masking version; a field with no rule is masked |
| 6 | Nothing records that the case was opened | One access event records the actor, the case, the fields returned with a masked marker and the time |

### 4.2 Journey B — change a permission (current versus target)

| Step | Current | Target |
|---|---|---|
| 1 | A change request is raised and a developer edits code | The security administrator prepares a matrix version as a file with a valid-from date |
| 2 | The change waits for a release | The version is validated; a duplicate row or an invalid letter refuses the whole version and the version in force stays |
| 3 | Nobody proves who approved it | The loader cannot approve; the approver of the table approves; the approval is a decision record with the load, the version and the row count |
| 4 | The effect appears at the next deployment | The new letters apply from the valid-from date with no deployment |
| 5 | Other services may hold a stale copy | An `AccessPolicyChanged` event lets every service refresh its cache |

### 4.3 Journey C — read a case under masking (current versus target)

| Step | Current | Target |
|---|---|---|
| 1 | The reader sees the identity number and the phone number | The reader sees `XXXXXXXXX1234` and `XXXXXX5678` |
| 2 | No check that the case is in the reader's scope | A case outside the scope is not returned and reads as not found |
| 3 | No record of the read | An access event records the case, the field IDs returned and which were masked |

### 4.4 Journey D — emergency access (current versus target)

| Step | Current | Target |
|---|---|---|
| 1 | An administrator asks for standing rights or shares a login | An incident is opened; the bank IAM approves a grant for a named group with an end time |
| 2 | The extra access is invisible | The administrator activates break-glass against the incident, area, right, scope and a reason; the duration is the earlier of four hours and the group end |
| 3 | Actions cannot be separated from ordinary work | Every action under the grant carries the grant ID and the incident; at expiry the previous rights apply with no action by anyone |
| 4 | Review happens late, by memory | Compliance sees every grant with its incident, actions and duration; a use with no incident is raised |

### 4.5 Journey E — recertify and audit (current versus target)

| Step | Current | Target |
|---|---|---|
| 1 | Role holder lists are rebuilt by hand | The access review list is produced every six months for recertification |
| 2 | An audit query takes days of file searching | The access log is searched by user, period, event and case, with paging; every export is itself logged |
| 3 | The evidence is a spreadsheet | The access events sit in the same append-only record store as the decisions |

## 5. Capabilities and features

| CAP | Capability | What it delivers | BR | FSD features | MoSCoW |
|---|---|---|---|---|---|
| CAP-P4-01 | Identity and session | Entra ID single sign-on with a second factor, a resolved session (roles, scope, matrix version, conflict version, partner state, break-glass state), and the role-conflict refusal at sign-in | REQ-ACA-001; REQ-ACA-002; REQ-ACA-003 | FEAT-ACA-01; FEAT-ACA-02; FEAT-ACA-03 | Must |
| CAP-P4-02 | Roles as data | The role list as versioned rows with role class and default scope, added or changed without a code release, mapped to Entra groups | REQ-ACA-002 | FEAT-ACA-03 | Must |
| CAP-P4-03 | Permission matrix as data | The C/R/U/D/A letters per role and capability area as versioned rows; the only source of what a role may see and do; a bad version refused whole | REQ-ACA-003; REQ-ACA-007 | FEAT-ACA-04 | Must |
| CAP-P4-04 | Authorisation answer | One answer for a requested area, right, scope and case: decision, matrix version, masking markers; cached and refreshed on a policy change | REQ-ACA-003; REQ-ACA-007; REQ-CWC-018 | FEAT-ACA-04; FEAT-ACA-14; FEAT-ADM-14 | Must |
| CAP-P4-05 | Scope enforcement | Own, team, region or all; lists, reads and exports return only the cases the scope permits and never reveal that a case exists outside it | REQ-ACA-009 | FEAT-ACA-14 | Must |
| CAP-P4-06 | Masking by role | Personal fields masked per role and masking version on every screen and every agent call; a field with no rule is masked; no clear value is fetched for a masked caller | REQ-ACA-005; REQ-RDF-010 | FEAT-ACA-05 | Must |
| CAP-P4-07 | Delegation of authority | The approval limit per decision, approval level, product and amount as versioned rows; the lookup the approval router calls, including `NOT_COVERED` and the related-party case | REQ-ACA-004 | FEAT-ACA-06; FEAT-ADM-03 | Must |
| CAP-P4-08 | Access log | Every read of a case, a document or a data product, and every export, written to the record store with actor, target, fields, masked marker and time, and searchable | REQ-ACA-006 | FEAT-ACA-07; FEAT-ACA-08; FEAT-ACA-16 | Must |
| CAP-P4-09 | Break-glass | Emergency access only against an open incident and an IAM-approved grant, time-boxed, marked on every action, and reviewed by Compliance | REQ-ACA-008 | FEAT-ACA-09; FEAT-ACA-10 | Must |
| CAP-P4-10 | Joiner, mover, leaver and access review | Access follows the organisation when a person joins, moves or leaves, and the role holder list is produced for recertification | REQ-ACA-011; REQ-ACA-002 | FEAT-ACA-13; JOB-18 access review list | Must |
| CAP-P4-11 | Partner identity boundary | Partner identities reach the Workbench only through the external gateway with a second factor, scoped to their own cases; rwb-access answers the check, rwb-partner holds the identity | REQ-ACA-012 | RWB-E2-019 (no FSD feature code) | Must |
| CAP-P4-12 | Agents and service identities | Agents, jobs and other services run under service identities and pass the same matrix and scope checks as people, with the model or agent version on the record | REQ-ACA-010; REQ-CWC-018 | FEAT-ADM-14 | Must |
| CAP-P4-13 | Access administration | One administration surface for roles, permissions, scope, masking and the DoA table, with the matrix report and rollback of a policy version | REQ-ACA-013 | FEAT-ADM-01; FEAT-ADM-06; FEAT-ADM-14 | Should |
| CAP-P4-14 | Access policy change publication | A change to any access policy version is published so that every service refreshes its cached answer | REQ-ACA-003; REQ-ACA-004 | FEAT-ACA-03; FEAT-ACA-04; FEAT-ACA-06 | Must |

### 5.1 Feature to capability map (FSD P4 A1.2)

| FSD feature | Name | CAP | In this PRD |
|---|---|---|---|
| FEAT-ACA-01 | Sign on through Entra ID with single sign-on | CAP-P4-01 | Yes |
| FEAT-ACA-02 | Enforce multi-factor authentication | CAP-P4-01 | Yes |
| FEAT-ACA-03 | Hold roles as data | CAP-P4-02 | Yes |
| FEAT-ACA-04 | Hold the role to permission matrix as data | CAP-P4-03 | Yes |
| FEAT-ACA-05 | Mask PDPA fields by role | CAP-P4-06 | Yes |
| FEAT-ACA-06 | Hold the delegation of authority table as reference data | CAP-P4-07 | Yes |
| FEAT-ACA-07 | Write every access event to the access log | CAP-P4-08 | Yes |
| FEAT-ACA-08 | Write the access log into the decision log | CAP-P4-08 | Yes, with rwb-decision owning the central ledger |
| FEAT-ACA-09 | Use break-glass access with an incident reference | CAP-P4-09 | Yes |
| FEAT-ACA-10 | Review break-glass use | CAP-P4-09 | Yes |
| FEAT-ACA-11 | Show the case record view read only | — | No: the screen is rwb-case's (`GAP-1577`) |
| FEAT-ACA-12 | Show the case record view with the history timeline | — | No: the screen is rwb-case's (`GAP-1577`) |
| FEAT-ACA-13 | Apply joiner, mover and leaver changes to access | CAP-P4-10 | Yes, with rwb-case performing the reallocation |
| FEAT-ACA-14 | Scope a user's cases by team and region | CAP-P4-05 | Yes |
| FEAT-ACA-15 | Run the release checklist, training and go-live readiness | — | No: a delivery activity, not product behaviour (`GAP-1578`) |
| FEAT-ACA-16 | Answer an access audit query | CAP-P4-08 | Yes |
| FEAT-ADM-01 | Run the full administration screens | CAP-P4-13 | Yes, for access administration only |
| FEAT-ADM-02 | Change a decision rule through the administration screens | — | No: rule packages are rwb-decision's (`GAP-1565`) |
| FEAT-ADM-03 | Move an approval limit | CAP-P4-07 | Yes |
| FEAT-ADM-04 | Set the treatment policy by product | — | No: parameters are rwb-case's (`GAP-1564`) |
| FEAT-ADM-05 | Add a letter template with Compliance approval | — | No: templates are rwb-comms' |
| FEAT-ADM-06 | Roll back a configuration version | CAP-P4-13 | Yes, for the access policy versions of this service |
| FEAT-ADM-07 | Publish a panel change | — | No: the panel is rwb-partner's |
| FEAT-ADM-08 | Run a QA sample against the rule version applied | — | No: it reads the decision ledger, rwb-decision's |
| FEAT-ADM-09 | Return a defective pack | — | No: the pack is rwb-litigation's |
| FEAT-ADM-10 | Detect a broken hash chain in the decision log | — | No: the daily chain check is rwb-decision's (JOB-14) |
| FEAT-ADM-11 | Handle a data subject request | CAP-P4-06 | Partly: rwb-access supplies the masked field list and the access history; the request itself is worked by Compliance across the case, document and ledger (see section 12) |
| FEAT-ADM-12 | Manage an incident | — | No: an operations process across services |
| FEAT-ADM-13 | Refer a case to Aric | — | No: rwb-deviation's |
| FEAT-ADM-14 | Control access by role and by agent | CAP-P4-04; CAP-P4-12; CAP-P4-13 | Yes |

## 6. Functional requirements

Each requirement is one testable statement. "FSD requirement" is the requirement the P4 functional specification v3 serves and the map between this PRD and the source. Priority uses MoSCoW. Wave is the delivery wave of the business epic that first needs it.

| FR | Requirement | CAP | BR | FSD requirement | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-P4-001 | A user signs on through Entra ID single sign-on from the ACE front end; the session is accepted only when the token proves a second factor. | CAP-P4-01 | REQ-ACA-001 | REQ-ACA-001 | Must | 1 |
| FR-P4-002 | A token whose `amr` claim carries `pwd` and not `mfa` is refused with status 401 and message MSG-P4-005, and one refusal is recorded with reason `NO_MFA`. | CAP-P4-01 | REQ-ACA-001 | REQ-ACA-001 | Must | 1 |
| FR-P4-003 | A user whose Entra groups map to no active Recovery role sees the access request page with MSG-P4-001, receives status 401 on every recovery endpoint, and one refusal is recorded with reason `NO_ROLE`. | CAP-P4-01; CAP-P4-02 | REQ-ACA-001; REQ-ACA-007 | REQ-ACA-001 | Must | 1 |
| FR-P4-004 | Roles are resolved from Entra groups through the versioned role rows; a group with no mapping, or mapped to an inactive role, gives no permission and its name is recorded on the sign-in event. | CAP-P4-02 | REQ-ACA-002 | REQ-ACA-002 | Must | 1 |
| FR-P4-005 | A user holding a conflicting role pair is refused at sign-in with message MSG-P4-006 naming both role codes, an incident is raised to the security administrator queue, and one refusal is recorded with reason `ROLE_CONFLICT`. | CAP-P4-01 | REQ-ACA-003 | REQ-ACA-003 | Must | 1 |
| FR-P4-006 | The resolved session states the user's roles, the scope, the matrix version, the conflict version, the partner identity state where the caller is a partner user, and the break-glass state with its end time where a grant is active. | CAP-P4-01 | REQ-ACA-001; REQ-ACA-009 | REQ-ACA-003 | Must | 1 |
| FR-P4-007 | A role is a versioned row carrying a role code, a name, a role class from LOV-ROLE-CLASS and a default scope from LOV-SCOPE; a role is added, renamed or retired without a code release. | CAP-P4-02 | REQ-ACA-002 | REQ-ACA-002 | Must | 1 |
| FR-P4-008 | A permission row carries a role, one of the 14 capability areas, the letters C, R, U, D and A or a dash, and the matrix version; the letters a user holds in an area are the union of the letters of their roles and of no other role. | CAP-P4-03 | REQ-ACA-003 | REQ-ACA-003 | Must | 1 |
| FR-P4-009 | A matrix version that repeats a role and area row, or carries a letter outside C, R, U, D, A and dash, is refused whole with message MSG-P1-002 naming the offending row, and the version in force stays in force. | CAP-P4-03 | REQ-ACA-003 | REQ-ACA-007 | Must | 1 |
| FR-P4-010 | The permission matrix is the only source of what a role may see and do: every operation declares its capability area and the right it needs, and no operation grants a right that the matrix does not. | CAP-P4-03 | REQ-ACA-003; REQ-ACA-007 | REQ-ACA-003 | Must | 1 |
| FR-P4-011 | The authorise answer returns the decision (allowed or refused), the capability area, the right asked, the scope applied, the matrix version and, when a case is named, the masking marker per personal field ID. | CAP-P4-04 | REQ-ACA-003 | REQ-ACA-003; REQ-ACA-007 | Must | 1 |
| FR-P4-012 | The authorise answer is served from a cache that is refreshed when an `AccessPolicyChanged` or `DoaLimitChanged` event arrives, so a policy change applies with no deployment and no service restart; the refresh window is `Not specified in the source documents (GAP-1568; ASM-2702)`. | CAP-P4-04; CAP-P4-14 | REQ-ACA-003; REQ-ACA-004 | REQ-ACA-003 | Must | 1 |
| FR-P4-013 | A request outside the matrix is refused with status 403 and message MSG-P4-002 before the handler runs, nothing changes, and one refusal is recorded with decision code `AC-DENY`, the capability area, the right asked and no case ID. | CAP-P4-04 | REQ-ACA-007 | REQ-ACA-007 | Must | 1 |
| FR-P4-014 | A list, a read or an export returns only the cases the caller's scope allows: scope `OWN` returns the cases the caller owns, `TEAM` the team's, `REGION` the region's and `ALL` every case the role permits, and the total returned counts only those cases. | CAP-P4-05 | REQ-ACA-009 | REQ-ACA-009 | Must | 1 |
| FR-P4-015 | A case outside the caller's scope reads as not found (status 404, message MSG-P4-003) and never as a refusal, so the caller cannot tell an out-of-scope case from a missing one. | CAP-P4-05 | REQ-ACA-009 | REQ-ACA-009 | Must | 1 |
| FR-P4-016 | A personal field is shown masked unless a masking row for the caller's role and that field ID says unmasked under the masking version in force; no client renders a personal field itself. | CAP-P4-06 | REQ-ACA-005; REQ-RDF-010 | REQ-ACA-005 | Must | 1 |
| FR-P4-017 | A personal field with no masking row for any role is masked for every role. | CAP-P4-06 | REQ-ACA-005 | REQ-ACA-005 | Must | 1 |
| FR-P4-018 | A masked caller never causes a clear value to be fetched: no request is made to the ACE PII path for a masked field, and the rendering follows the masked form of the field (`XXXX-XX-XX` for a date, `XXXXXXXXX1234` for an identity number, `XXXXXX5678` for a phone number). | CAP-P4-06 | REQ-ACA-005; REQ-RDF-010 | REQ-ACA-005 | Must | 1 |
| FR-P4-019 | An agent or a model call receives the same masked answer as the person on whose behalf it runs, and only the personal fields the screen or the agent needs. | CAP-P4-06; CAP-P4-12 | REQ-ACA-005; REQ-ACA-010; REQ-CWC-018 | REQ-ACA-005; REQ-ACA-010 | Must | 1 |
| FR-P4-020 | The delegation of authority table holds, per row, a decision code, an approval level from L1 to L6, a product group, the principal limit, the loss percentage and amount limits, the minimum price or received percentage, the maximum term, the regulation item, the holder and substitute, the valid-from and valid-to dates and the limit version. | CAP-P4-07 | REQ-ACA-004 | REQ-ACA-004 | Must | 1 |
| FR-P4-021 | The DoA lookup answers, for a decision, regulation item, product, principal, loss and business date, the approval level, the row that allowed it and the limit version in force; where no row covers the request it answers `NOT_COVERED` and raises an incident to the risk officer queue with message MSG-P7-010; a related-party write-off is answered at the level the table gives for a related party with reason `RELATED_PARTY`. | CAP-P4-07 | REQ-ACA-004 | REQ-ACA-004 | Must | 1 |
| FR-P4-022 | A DoA version whose limit falls below the level above it, or which names an unknown decision code, is refused whole; the previous version stays readable with its valid-to date and stays in force; the person who loaded a version cannot approve it and only the approving role may approve. | CAP-P4-07 | REQ-ACA-004 | REQ-ACA-004 | Must | 1 |
| FR-P4-023 | Every read of a case, a document or a data product writes one access event with the actor, the case or document reference, the field IDs returned with a `masked` or `clear` marker, and the time; the event is written even when the answer is a refusal. | CAP-P4-08 | REQ-ACA-006; REQ-RDF-010 | REQ-ACA-006 | Must | 1 |
| FR-P4-024 | Every export of a list writes one access event with the actor, the filter used, the row count and no case ID. | CAP-P4-08 | REQ-ACA-006 | REQ-ACA-006 | Must | 1 |
| FR-P4-025 | A read that cannot be logged returns status 503 with message MSG-P7-003 and no data, and raises an incident to the platform administrator queue; a silent unlogged read is never allowed. | CAP-P4-08 | REQ-ACA-006 | REQ-ACA-006 | Must | 1 |
| FR-P4-026 | The access log is queried by user, period, event and case with paging, returns the actor, the target, the decision code, the rights and the time for each entry, and is readable only by the roles the matrix gives `DECISION_LOG` or `PLATFORM_ADMINISTRATION` right to. | CAP-P4-08 | REQ-ACA-006 | REQ-ACA-006 | Must | 1 |
| FR-P4-027 | Access events are published as decision records to the central ledger, so an access question and a decision question are answered from one history; the central ledger, its ingest and its daily chain check stay with rwb-decision. | CAP-P4-08 | REQ-ACA-006; REQ-ACA-008 | REQ-ACA-006 | Must | 1 |
| FR-P4-028 | Break-glass is activated only for an open incident, an IAM-approved grant, a capability area, a right, a scope and a reason of 20 to 1000 characters; the grant lasts until the earlier of four hours and the end of the IAM group, and while it is active the user sees message MSG-P4-004 with its end time. Both numbers are the placeholder values the P4 acceptance criteria carry until the access timers are set (`GAP-1571`; ASM-2703). | CAP-P4-09 | REQ-ACA-008 | REQ-ACA-008 | Must | 1 |
| FR-P4-029 | Every record written while a grant is active carries the grant ID and the incident reference; at the end time the rights held before the grant apply again with no action by any person. | CAP-P4-09 | REQ-ACA-008 | REQ-ACA-008 | Must | 1 |
| FR-P4-030 | An activation without an IAM grant is refused with status 403 and message MSG-P4-007 and recorded with decision code `AC-DENY` and reason `NO_BREAKGLASS_GRANT`; a repeated activation with the same idempotency key returns the first response and writes nothing new; a second activation with a new key while one is active is refused with status 409 and message MSG-GEN-004. | CAP-P4-09 | REQ-ACA-008 | REQ-ACA-008 | Must | 1 |
| FR-P4-031 | Every break-glass use is presented to Compliance with its incident, actor, area, right, scope, duration and the actions taken, and a use with no incident reference is raised as an exception. | CAP-P4-09 | REQ-ACA-008 | REQ-ACA-008 | Must | 1 |
| FR-P4-032 | A joiner, a mover or a leaver changes access through the mapped Entra groups: a leaver's roles end, a mover's matrix answer changes, and the cases of a leaver are reallocated inside the team by rwb-case within the leaver response time, which is `Not specified in the source documents (GAP-1573; ASM-2705)`. | CAP-P4-10 | REQ-ACA-011 | REQ-ACA-011 | Must | 2 |
| FR-P4-033 | The access review list is produced every six months as a role holder list for recertification, showing for each role the holders, their scope and the date their access was granted; the review date convention, the file layout and its interface row are `Not specified in the source documents (GAP-1572; ASM-2704)`. | CAP-P4-10 | REQ-ACA-011; REQ-ACA-002 | REQ-ACA-011 | Must | 4 |
| FR-P4-034 | A partner identity is accepted only when it arrives through the external partner gateway with a second factor, and its answer is scoped to the partner's own cases; the partner identity rows and the partner portal belong to rwb-partner, and rwb-access answers the check. | CAP-P4-11 | REQ-ACA-012 | REQ-ACA-012 | Must | 2 |
| FR-P4-035 | A job, an agent or another service calls the authorise answer under its own service identity, is subject to the same matrix and scope checks as a person, and its write is recorded with the model or agent version. | CAP-P4-12 | REQ-ACA-010; REQ-CWC-018 | REQ-ACA-010 | Must | 1 |
| FR-P4-036 | One administration surface lets the security administrator read and prepare changes to roles, permissions, scope, masking and the DoA table, and shows the matrix as a report; a change is prepared, validated and approved, and is never typed into code. | CAP-P4-13 | REQ-ACA-013 | REQ-ACA-013 | Should | 4 |
| FR-P4-037 | A policy version of this service is rolled back to the version before it in one call with a reason, and the rollback is recorded with the caller, the time and the reason. | CAP-P4-13 | REQ-ACA-013; REQ-ACA-002 | REQ-ACA-013 | Should | 4 |
| FR-P4-038 | A change to a role, permission, masking or DoA version publishes `AccessPolicyChanged` or `DoaLimitChanged` with the version label and the effective date, so every consumer refreshes its cache. | CAP-P4-14 | REQ-ACA-003; REQ-ACA-004 | REQ-ACA-003; REQ-ACA-004 | Must | 1 |

### 6.1 Functional requirement to FSD requirement map

| FSD requirement | Text (BRD Program v4, section 5.4) | FRs |
|---|---|---|
| REQ-ACA-001 | Every user signs on through Entra ID single sign-on with multi-factor authentication. | FR-P4-001, 002, 003, 006 |
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release. | FR-P4-004, 007, 037 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do. | FR-P4-005, 008, 009, 010, 011, 012, 038 |
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit. | FR-P4-020, 021, 022, 038 |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call. | FR-P4-016, 017, 018, 019 |
| REQ-ACA-006 | Every read of the case store, the document store and the data lake copy is written to the access log. | FR-P4-023, 024, 025, 026, 027 |
| REQ-ACA-007 | Access requested outside the authority matrix is refused and the refusal is recorded. | FR-P4-003, 009, 010, 013 |
| REQ-ACA-008 | A break-glass path exists for an emergency, needs its own approval, and writes to the access log. | FR-P4-027, 028, 029, 030, 031 |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow. | FR-P4-006, 014, 015 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people. | FR-P4-019, 035 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench so that access matches the current organization. | FR-P4-032, 033 |
| REQ-ACA-012 | Partner users reach the Workbench only through the external gateway, with multi-factor authentication, scoped to their own cases. | FR-P4-034 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator. | FR-P4-036, 037 |

BR coverage: all thirteen program requirements of P4 are served. No P4 requirement is left without a functional requirement. The requirements of other modules that rwb-access helps serve are named in section 6.2 and are not coverage gaps of this PRD.

### 6.2 Requirements of other modules that this service helps serve

| BR | Requirement | This PRD's part | Owner of the whole |
|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, queue membership and capacity held as versioned reference data | The role and permission rows only | P3 rwb-case (queues, membership, capacity) |
| REQ-CWC-018 | A model or agent writing to a queue passes the same checks as a person, under a service identity, logged with its version | The authorise and masking answers | P3 rwb-case |
| REQ-RDF-010 | Access to each data product is controlled per role, with personal data masked by role under PDPA | The per-role data product check and the masking answer | P1 rwb-source-data (data products, catalog) |

## 7. Non-functional requirements

Every value below is taken from the Non-Functional Specification v3 or the TSD P4 T7; nothing is set by this PRD. Where a value is open under a decision, it is named.

| NFR | Requirement | Target | Source | BR | Wave |
|---|---|---|---|---|---|
| NFR-P4-001 | The authorise, session and masking answers do not add to the screen budget: a screen that calls them stays inside the screen target, and a rule evaluation inside the wait stays inside its own target. | Under 2 seconds per screen at the 95th percentile; under 300 milliseconds per rule evaluation at the 95th percentile. No separate authorise target is set: `Not specified in the source documents (GAP-1579; ASM-2709)`, open under DL11 | NFR-008, NFR-011 | REQ-ACA-003; REQ-ACA-007 | 1 |
| NFR-P4-002 | Every request from every signed-on user passes one authorisation check at the busiest-hour load. | About 410 users online of 1,234 named, about 21 requests a second | NFR-002, NFR-003; NFR volume table | REQ-ACA-001; REQ-ACA-009 | 1 |
| NFR-P4-003 | The service is available when people are working, and a failure never becomes an allow. | 99.9 percent in business hours; 99.5 percent outside; an unavailable policy store refuses rather than permits (status 503, MSG-P7-003) | NFR-020, NFR-021; FSD P4 AC-EXC-P4-009-03 | REQ-ACA-003; REQ-ACA-007 | 1 |
| NFR-P4-004 | Staff and partner users authenticate with a second factor, and only through the approved path. | Entra ID single sign-on with multi-factor for staff; multi-factor and own-case scope for partner accounts | NFR-049, NFR-050; BRD Program section 4 | REQ-ACA-001; REQ-ACA-012 | 1 |
| NFR-P4-005 | Secrets are held in the key store and never in code, configuration files or prompts. | No secret in code or prompt | NFR-052 | REQ-ACA-001 | 1 |
| NFR-P4-006 | Access policy data and access events are encrypted at rest and in transit. | Encrypted | NFR-053 | REQ-ACA-006 | 1 |
| NFR-P4-007 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | NFR-054 | REQ-ACA-005 | 1 |
| NFR-P4-008 | Personal data is masked at rest and in use, and each screen and each agent receives only the personal data it needs. | Masked at rest and in use; data minimisation per screen and per agent | NFR-039, NFR-040 | REQ-ACA-005 | 1 |
| NFR-P4-009 | Every read of the case store, the document store and a data product is logged. | Every read | NFR-042 | REQ-ACA-006 | 1 |
| NFR-P4-010 | A data subject access, correction or erasure request is answered inside the statutory period. | Statutory period; not set as a working service level, open under DL26 | NFR-043 | REQ-ACA-005 | 4 |
| NFR-P4-011 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | REQ-ACA-005 | 1 |
| NFR-P4-012 | Access policy data stays in the bank's tenancy in the agreed region, and every policy artefact carries a classification that sets its handling. | SCB Azure, Southeast Asia; classification scheme applied, scheme open under DL26 | NFR-046, NFR-047 | REQ-ACA-006 | 1 |
| NFR-P4-013 | Every access decision and every policy change is reproducible from the record, with the matrix, masking, conflict and DoA versions in force, and the access history reads inside the user wait at its 2031 size. | Every decision reproducible; access and decision history under 2 seconds with about 36 GB of log and ledger by the end of 2031 | NFR-033, NFR-034, NFR-007 | REQ-ACA-006; REQ-ACA-008 | 1 |
| NFR-P4-014 | The daily hash-chain check of the record store is run, and a break is reported to Compliance the same day. | Daily check, same-day report (the check and the seal stay with rwb-decision, JOB-14) | NFR-035 | REQ-ACA-006 | 1 |
| NFR-P4-015 | The service produces logs, traces and metrics, every scheduled job has a run book, and a failing job, interface or agent raises an alert to a named owner. | Across the service; alert within 15 minutes to the named owner | NFR-064, NFR-067, NFR-068 | REQ-ACA-008 | 1 |
| NFR-P4-016 | Screen labels, validation messages and error messages are available in Thai and in English. | Every screen, label and message in Thai and English | NFR-059 | REQ-ACA-013 | 4 |
| NFR-P4-017 | Screens meet the bank accessibility standard and run on the supported browsers. | WCAG 2.1 level AA; current and previous major versions of Edge and Chrome | NFR-060, NFR-061 | REQ-ACA-013 | 4 |
| NFR-P4-018 | An outage or a failed call queues the work and retries on a schedule, and an interface that fails after the retry limit goes to an exception queue with a task for a named owner. | Queue and retry; three retries per item, then the exception queue | NFR-025, NFR-026 | REQ-ACA-008 | 2 |
| NFR-P4-019 | Agents run under service identities and are subject to the same role checks as people. | Service identities | NFR-051 | REQ-ACA-010 | 1 |
| NFR-P4-020 | A penetration test and a security review are completed before the first production release and before the partner portal opens to users outside the bank. | Before the first production release and before the partner portal opens | NFR-056 | REQ-ACA-008; REQ-ACA-012 | 2 |

### 7.1 Operational requirements

| Area | Requirement |
|---|---|
| Scheduled work | One Schedule only: the access review list, six-monthly, in the owning service on task queue `rwb-access` (Architecture v5 slides 14 and 44, JOB-18). No shared scheduler table. |
| Batch and freshness | This service reads no ACE source data except the group mapping; a late ACE batch does not delay an access decision. |
| Support and monitoring | `/health` and `/metrics` on every instance; the Schedule has a run book, monitoring and an alert to the operations channel (NFR-067, NFR-068). |
| Release | A failed release rolls back by redeploying the previous tag (NFR-027). A policy version rolls back by one call (FR-P4-037). |
| Idempotency | Every POST accepts `Idempotency-Key` and stores the response; a repeat returns the stored response and a conflicting key is refused with status 409 and MSG-GEN-004 (Architecture v5 slide 11). |
| Data residency | SCB Azure, Southeast Asia (NFR-046). |

## 8. Data requirements

Classification uses `[PII]`, `[SENSITIVE_FINANCIAL]`, `[CONFIDENTIAL]` and `[PUBLIC]`. A retention period that no source sets is marked.

| Entity | Owner | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `role` | P4 rwb-access | role code (DF-REF-035), name, role class (LOV-ROLE-CLASS), default scope (LOV-SCOPE), Entra group (DF-REF-039) | `[CONFIDENTIAL]` | Workbench (seeded at baseline) | Not set (DL26) |
| `permission` | P4 rwb-access | role, capability area (LOV-CAPABILITY), letters (DF-REF-043), matrix version (DF-REF-044) | `[CONFIDENTIAL]` | Workbench | Every version kept; period not set (DL26) |
| `masking_rule` | P4 rwb-access | role code, field ID (DF-REF-200), unmasked flag (DF-REF-201), masking version (DF-REF-202), valid-from and valid-to | `[CONFIDENTIAL]` | Workbench | Every version kept; period not set (DL26) |
| `role_conflict` | P4 rwb-access | role code, conflicts-with, reason, conflict version, valid-from and valid-to | `[CONFIDENTIAL]` | Workbench | Every version kept; period not set (DL26) |
| `delegation_limit` | P4 rwb-access | decision code, approval level, product group, principal and loss limits, minimum price and received percentage, maximum term, regulation item, holder and substitute user, limit version, valid-from and valid-to | `[CONFIDENTIAL]`; `holder_user_id` and `substitute_user_id` are `[PII]` | Workbench (loaded as DOA-2026.11 through E1-043 per D-RCV-29) | Every version kept; period not set (DL26) |
| Access event (a decision record with decision code `AC-READ`, `AC-EXPT` or `AC-DENY`) | Record object: PLT library, one copy in `rwb_access`; content: P4 | actor, case or document ID, field IDs with masked or clear marker, capability area, right, grant ID and incident where a grant is active, time | `[PII]` (actor and case) and `[CONFIDENTIAL]` | Workbench; ledger copy in rwb-decision | Log retention set by Compliance; not set (NFR-030, DL26) |
| Access review list (output) | P4 rwb-access | role, holder, scope, date access granted, review date | `[PII]` (holder) | Generated from `role` and the session history | Not set (DL26) |
| `lov_value` (referenced) | P3 rwb-case | list code, value code, label English and Thai, sort order, valid-from | `[PUBLIC]` for the codes; `[CONFIDENTIAL]` for the version | rwb-case contract | Not set (DL26) |
| `partner_user` (referenced) | S9 rwb-partner | identity reference, partner, role code, valid-from and valid-to | `[PII]` | rwb-partner contract | Not set (DL26) |
| `queue`, `queue_member` (referenced for scope) | P3 rwb-case | queue code, team code, role that works it, member and capacity | `[CONFIDENTIAL]` | rwb-case contract | Not set (DL26) |

### 8.1 Classification rules applied

- A personal field is identified by its field ID (for example DF-PTY-007 and DF-PTY-016) so that the masking answer names a field, never a rendering.
- The access log carries personal data of the actor and a case reference; it is `[PII]` and is never published on a Kafka topic. Events carry IDs and facts only (Architecture v5 slide 42 notes).
- No production data in development; masked copies in user acceptance (NFR-045).

## 9. Integration points

Owners follow the Microservice Ownership Map v1. Protocol is stated only where Architecture v5 confirms it.

| System or service | Direction | Purpose | Protocol | Owner | Confirmed by |
|---|---|---|---|---|---|
| ACE Common sign-in and bank IAM through Entra ID (INT-21) | In | Sign-in, the token, the group list and the group end time for a break-glass grant | ACE sign-in at each sign-in | ACE team | Architecture v5 slide 14; TSD P4 T5.1 |
| ACE Common audit, PII and SOC logging (INT-22) | Out | The audit and PII log of the platform | ACE logging as events happen | ACE team | TSD P4 T5.1 |
| rwb-case (P3) | In and out | The case reference, owner, queue, team and region travel in the authorise request; the queue and membership data used for scope come from rwb-case; reference-data loads and lists of values are rwb-case's | REST, one hop, 2-second timeout | P3 rwb-case | Architecture v5 slides 14 and 20; Ownership Map |
| rwb-decision (P7) | Out and in | Access events reach the central ledger; the approval router calls the DoA lookup; rule packages and the change report are rwb-decision's | Kafka `rwb.decision-record.v1`; REST for the DoA lookup | P7 rwb-decision | Architecture v5 slides 14, 42 and 43; Ownership Map |
| rwb-document (P5) | Out and in | A document read needs an access answer and a masking answer | REST, one hop | P5 rwb-document | Architecture v5 slide 20 |
| rwb-partner (S9) | In and out | Partner identities and the partner portal are rwb-partner's; rwb-access answers the second-factor and scope check | REST through the partner gateway in the DMZ | S9 rwb-partner | Architecture v5 slides 14 and 20; Ownership Map |
| rwb-integration (P2) | Out | The six-monthly access review file is delivered by `deliverFile(manifest)`; `FileDelivered` and `FileFailed` return to the requesting service | Temporal activity on queue `rwb-integration`; Kafka events | P2 rwb-integration | Architecture v5 slides 16 and 44 |
| gateway-bff | In | The only entry for staff screens; an opaque session cookie with a 15-minute idle timeout; a short-lived user token | REST through the App Gateway; Redis for sessions only | Platform (PLT-EDGE) | Architecture v5 slide 20 |
| Platform library (PLT) | In | Outbox, inbox, idempotency and decision-record objects in `rwb_access`; OpenTelemetry | Library and template | PLT | Architecture v5 slides 11 and 20; DP-09 |
| Every consumer of the policy cache | Out | `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`, all services refresh | Kafka, CloudEvents | P4 rwb-access publishes; all consume | Architecture v5 slides 14 and 43 |
| `POST /admin/workflows/smoke` | — | Not this service: the smoke workflow is platform | — | PLT | Ownership Map |

### 9.1 Unknowns carried as questions

| Item | State | Question |
|---|---|---|
| Authorise, `/me/permissions`, `/doa-limits` and `/masking-policies` schemas | Named in Architecture v5, absent from the API Specification v4 and TSD P4 appendix T-A | Q-P4-01 (`GAP-1568`) |
| Event payloads and keys of `AccessPolicyChanged` and `DoaLimitChanged` | Named in Architecture v5 slide 43, absent from the Event and Messaging Design v4 | Q-P4-02 (`GAP-1569`) |
| Reference-data load surface for the DoA table and the matrix | Endpoints are rwb-case's; the tables and their validation rules are P4's | Q-P4-03 (`GAP-1564`) |
| Partner identity record attributes | `partner_user` is rwb-partner's; the attributes rwb-access needs are not listed | Q-P4-09 (`GAP-1567`) |
| Group mapping read path | `v_ace_iam_group` supplies the group; the mapping to a role is a `role` column | Q-P4-10 (`GAP-1568`) |

## 10. Release slicing proposal

Waves follow the W-MAP of the Template and Rules (R5.6) and the ownership map. The service is wave 1 (Architecture v5 slide 41); the stories of a business epic keep the wave of that epic where it is later. All dates are unchanged and tentative.

### 10.1 Increment 1 — wave 1, EP01, release 30 November 2026 (tentative)

| Item | Value |
|---|---|
| Capabilities | CAP-P4-01, CAP-P4-02, CAP-P4-03, CAP-P4-04, CAP-P4-05, CAP-P4-06, CAP-P4-07, CAP-P4-08, CAP-P4-09, CAP-P4-12, CAP-P4-14 |
| Functional requirements | FR-P4-001 to FR-P4-031, FR-P4-035, FR-P4-038 |
| Non-functional requirements | NFR-P4-001 to NFR-P4-009, NFR-P4-011 to NFR-P4-015, NFR-P4-019 |
| Why | No case can open, no screen can render and no decision can be approved without an answer to who, what and what may be seen. The Epic 1 stories RWB-E1-022, RWB-E1-037, RWB-E1-038 and RWB-E1-039 and the roles-as-data story RWB-E1-019 are all wave 1, and the P4 data in TSD P4 T3.1 is the Epic 1 baseline seed (D-RCV-29). |
| Policy administration in this increment | Load-based through the rwb-case reference-load surface, with the P4 validation rules: the matrix and DoA versions are prepared by RW-REFADM, approved by RW-SECADM or RW-RISK, and applied from a valid-from date. |
| Not in this increment | The E8 administration screens, the access review cycle, the joiner-mover-leaver path, the partner boundary. |

### 10.2 Increment 2 — wave 2, EP02, release 31 December 2026 (tentative)

| Item | Value |
|---|---|
| Capabilities | CAP-P4-10 (joiner, mover, leaver), CAP-P4-11 |
| Functional requirements | FR-P4-032, FR-P4-034 |
| Non-functional requirements | NFR-P4-018, NFR-P4-020 |
| Why | Epic 2 brings partners into the Workbench (RWB-E2-019) and a changing organisation; the partner boundary and the joiner-mover-leaver path are the Epic 2 parts of REQ-ACA-011 and REQ-ACA-012. |

### 10.3 Increment 3 — wave 4, EP08, release 30 June 2027 (tentative)

| Item | Value |
|---|---|
| Capabilities | CAP-P4-10 (access review), CAP-P4-13 |
| Functional requirements | FR-P4-033, FR-P4-036, FR-P4-037 |
| Non-functional requirements | NFR-P4-010, NFR-P4-016, NFR-P4-017 |
| Why | The full administration screens (FEAT-ADM-01, FEAT-ADM-14), the access review list (JOB-18) and the rollback of a policy version are Epic 8 work: REQ-ACA-013 is a Should, and the access review cycle is a six-monthly control that needs a settled role set first. |

### 10.4 Slicing rules applied

- A capability whose requirement is Must and whose absence stops a wave is in the earliest wave that needs it, not in the wave of its feature code.
- A capability that another service could fake is not moved earlier than the wave that must use it; CAP-P4-11 and CAP-P4-13 therefore sit in their own epic waves.
- No increment carries a capability of another service: the reference-data load surface, the rule package registry, the smoke workflow and the partner identity rows are outside every increment of this PRD.

## 11. Acceptance criteria and validation evidence

Each criterion is testable and maps to the requirement it proves. Evidence names the source criterion where one exists.

| AC | Proves | Acceptance criterion | Validation evidence |
|---|---|---|---|
| AC-P4-001 | FR-P4-001, FR-P4-006 | A test user in the mapped Entra group signs in with password and second factor and the session holds the role, the scope and the matrix version. | FSD P4 AC-P4-001-01; TSD P4 TC-E1-022-01 |
| AC-P4-002 | FR-P4-002 | A token whose `amr` claim holds `pwd` and not `mfa` is refused with 401 and MSG-P4-005 and a `NO_MFA` refusal is recorded. | FSD P4 AC-EXC-P4-001-02 |
| AC-P4-003 | FR-P4-003 | A user in no mapped group sees MSG-P4-001 and gets 401 on every recovery endpoint, and one `NO_ROLE` refusal is recorded. | FSD P4 AC-EXC-P4-001-01 |
| AC-P4-004 | FR-P4-004 | A user in a mapped group and an unmapped group holds only the mapped role, and the unmapped group name is on the sign-in event. | FSD P4 AC-EXC-P4-001-04 |
| AC-P4-005 | FR-P4-005 | A user holding RW-SECADM and RW-CASEOWN is refused with MSG-P4-006 naming both codes, an incident is raised and a `ROLE_CONFLICT` refusal is recorded. | FSD P4 AC-EXC-P4-001-03 |
| AC-P4-006 | FR-P4-008 | A user with two roles holds the union of their letters in an area and no letter from a role they do not hold. | FSD P4 AC-ALT-P4-001-02 |
| AC-P4-007 | FR-P4-009 | A matrix file that repeats a role and area row or carries an invalid letter is refused whole with MSG-P1-002, no row is stored and the matrix in force stays. | FSD P4 AC-EXC-P4-005-02 |
| AC-P4-008 | FR-P4-010, FR-P4-013 | A user without the right in an area is refused with 403 and MSG-P4-002 before the handler runs, the data is unchanged and an `AC-DENY` entry names the area and the right. | FSD P4 AC-ALT-P4-005-02; AC-EXC-P4-009-04 |
| AC-P4-009 | FR-P4-011, FR-P4-012 | A matrix version taking effect on its valid-from date grants a new right with no deployment, and the change is a decision record with the load, the version and the row count. | FSD P4 AC-P4-005-01 |
| AC-P4-010 | FR-P4-014 | A user with scope OWN and 12 owned cases gets 12 cases and a total of 12 from a list. | FSD P4 AC-EXC-P4-005-01 |
| AC-P4-011 | FR-P4-015 | A case outside the scope returns 404 with MSG-P4-003 and is indistinguishable from a missing case. | FSD P4 AC-EXC-P4-005-01 |
| AC-P4-012 | FR-P4-016 | A caller whose role has no permission in an area sees the personal fields of a case masked, in the field's masked form. | FSD P4 AC-ALT-P4-005-01 |
| AC-P4-013 | FR-P4-017 | A personal field with no masking row for any role is masked for every role. | FSD P4 AC-EXC-P4-005-05 |
| AC-P4-014 | FR-P4-018 | No request reaches the ACE PII path for a masked field, and the access event marks the field masked. | FSD P4 AC-ALT-P4-005-01 |
| AC-P4-015 | FR-P4-019 | An agent call receives the same masked answer as the person and only the fields it needs. | NFR-P4-008 (masking review); agent run evidence |
| AC-P4-016 | FR-P4-020 | A DoA file of 95 limits loads as 218 stored rows with a decision, a level, a product and no duplicate key. | FSD P4 AC-P4-006-01 |
| AC-P4-017 | FR-P4-021 | A lookup for a decision, item, product, principal, loss and date returns the level, the row and the version; an uncovered product returns `NOT_COVERED` with an incident to the risk officer queue. | FSD P4 AC-ALT-P4-006-01; AC-EXC-P4-006-04 |
| AC-P4-018 | FR-P4-021 | A related-party write-off is answered at the related-party level with reason `RELATED_PARTY`. | FSD P4 AC-EXC-P4-006-05 |
| AC-P4-019 | FR-P4-022 | A DoA file with a falling limit or an unknown decision code is refused whole, the previous version keeps its valid-to date and stays in force, and the loader cannot approve. | FSD P4 AC-EXC-P4-006-01; AC-EXC-P4-006-02 |
| AC-P4-020 | FR-P4-023 | Opening a case writes one access event with the actor, the case, the field IDs returned and their masked marker, and the time. | FSD P4 AC-P4-009-01 |
| AC-P4-021 | FR-P4-024 | Exporting a filtered list writes one event with the filter, the row count and no case ID. | FSD P4 AC-ALT-P4-009-02 |
| AC-P4-022 | FR-P4-025 | A read taken while the record store is unavailable returns 503 and MSG-P7-003 with no data and raises an incident. | FSD P4 AC-EXC-P4-009-03 |
| AC-P4-023 | FR-P4-026 | An audit query by user, period and case returns the matching entries with paging, and a role without the right is refused. | FSD P4 A2.16; TSD P4 API-P4-008 |
| AC-P4-024 | FR-P4-028 | An activation with an open incident and an IAM grant is active until the earlier of four hours and the group end, and the banner shows MSG-P4-004 with that time. | FSD P4 AC-ALT-P4-009-01 |
| AC-P4-025 | FR-P4-029 | An action inside a granted area at 14:20 is allowed and marked with the grant and the incident; the same call at 14:31 is refused with MSG-P4-002 with no action by anyone. | FSD P4 AC-ALT-P4-009-01 |
| AC-P4-026 | FR-P4-030 | An activation without an IAM grant is refused with 403 and MSG-P4-007 and recorded as `NO_BREAKGLASS_GRANT`; a repeat with the same key returns the first response; a short reason or a missing incident is refused with 422; a second key while a grant is active is refused with 409. | FSD P4 AC-EXC-P4-009-01, -02, -05 |
| AC-P4-027 | FR-P4-031 | Every grant appears in the Compliance review with its incident, actor, area, right, scope, duration and actions, and a grant with no incident is raised. | FSD P4 A2.10; TSD P4 T6.3 |
| AC-P4-028 | FR-P4-032 | A leaver's roles end through the group mapping, and the cases are reallocated inside the team by rwb-case; the leaver response time is `Not specified in the source documents (GAP-1573; ASM-2705)`. | Requirement-level test with the rwb-case reallocation scenario |
| AC-P4-029 | FR-P4-033 | The six-monthly run produces a role holder list per role with holder, scope and grant date, delivered through rwb-integration; the review date convention is `Not specified in the source documents (GAP-1572; ASM-2704)`. | JOB-18 run evidence; delivery events |
| AC-P4-030 | FR-P4-034 | A partner identity without a second factor is refused, and a partner answer names only the partner's own cases. | NFR-050; penetration test before the portal opens (NFR-056) |
| AC-P4-031 | FR-P4-035 | A job or agent call passes the same matrix and scope checks as a person and is recorded with the service identity and the model or agent version. | NFR-051; NFR-078 |
| AC-P4-032 | FR-P4-036, FR-P4-037, FR-P4-038 | A policy version is prepared, validated, approved, applied and rolled back from one surface, and each change publishes its event with the version label and effective date. | FEAT-ADM-06 scenario; cache refresh observed on a consumer |

### 11.1 Validation evidence standard

| Level | Evidence |
|---|---|
| Unit | A rule, a union, a masked field, a lookup answer |
| Component | The authorise answer, the session, the access log query, the break-glass grant |
| Contract | The authorise, session, DoA and masking answers against the published contract and the fake of each consumer |
| Integration | A policy change applied end to end from the load to a consumer's refreshed answer |
| End to end | Sign-in, case read under masking, refusal, export and audit query on one case |
| Non-functional | The screen and rule targets of NFR-P4-001 at the load of NFR-P4-002; the fail-closed behaviour of NFR-P4-003; the penetration test of NFR-P4-020 |

## 12. Open questions

Unresolved decisions and questions carried from the business requirements, plus the product questions this PRD raises. Decision identifiers are the Decision Log's; product questions are this PRD's.

| Q | Question | Owner role | Decision or gap | Blocks |
|---|---|---|---|---|
| Q-P4-01 | What are the request and answer schemas of the authorise, `/me/permissions`, `/doa-limits` and `/masking-policies` operations, including the field list of the answer and the masking part? | Solution architect | `GAP-1568`; ASM-2700 | The authorise contract and every consumer fake (wave 1) |
| Q-P4-02 | What are the payload, the key and the topic of `AccessPolicyChanged` and `DoaLimitChanged`, and what is the intended cache refresh window? | Solution architect with the platform event owner | `GAP-1569`; ASM-2702 | The cache refresh requirement FR-P4-012 and FR-P4-038 (wave 1) |
| Q-P4-03 | Which service owns the load, verify, approve and rollback of the permission matrix and the DoA table, given that the load surface is rwb-case's and the tables and their validation rules are rwb-access's? | Solution architect with the P3 contract owner | `GAP-1564`; ASM-2699 | The Epic 1 policy load path (wave 1) |
| Q-P4-04 | Is the access log retention the decision log retention, and what is that period? Who may read the access log across services? | Compliance | DL26; NFR-030; `GAP-1570` | The access log data requirement (wave 1) |
| Q-P4-05 | What are the access review interval, the leaver response time and the break-glass review window? | SCB IT security | DL38; `GAP-1573`; `GAP-1571` | FR-P4-032, FR-P4-033 (waves 2 and 4) and the break-glass placeholder values of FR-P4-028 (wave 1) |
| Q-P4-06 | Which roles receive real users at each release, and which Entra group names and IAM entries map to them? | Business lead; SCB IT security | DL39; DL40 | The role seed of each release |
| Q-P4-07 | Is access granted centrally by an IAM team or by the application owner, and who reviews it? | IT security with the product owner | DL01 | The joiner-mover-leaver and access review capability (wave 2) |
| Q-P4-08 | How do partners reach the Workbench from outside the bank, given the one-to-three-month lead time? | Architecture team | DL03 | CAP-P4-11 (wave 2) |
| Q-P4-09 | Which attributes of a partner identity does the authorise answer need, and who holds them? | Solution architect with the rwb-partner contract owner | `GAP-1567` | FR-P4-034 (wave 2) |
| Q-P4-10 | How is an Entra group mapped to a role at run time, and what happens to a mapping when a role is retired? | Security administrator | `GAP-1568` | FR-P4-004 (wave 1) |
| Q-P4-11 | Which personal field IDs must the masking policy cover, and what does each masking version contain? | Compliance with the solution architect | `GAP-1575` | FR-P4-016 and FR-P4-017 (wave 1) |
| Q-P4-12 | What is the full list of role pairs that may not be held together, and how many roles and permission rows does a version hold? | Security administrator with the reference data administrator | `GAP-1574` | FR-P4-005 and the matrix seed (wave 1) |
| Q-P4-13 | What is the authorise answer time target at the busiest hour? | Solution architect with Risk | DL11; `GAP-1579` | NFR-P4-001 (wave 1) |
| Q-P4-14 | What is the classification scheme for access policy data and access events? | Compliance with Security | DL26; NFR-047; `GAP-1570` | The classification column of section 8 (wave 1) |
| Q-P4-15 | Is REQ-ACA-006's "data lake copy" replaced by "the data products", since the data lake is removed? | Compliance with the solution architect | `GAP-1576`; ASM-2710 | The wording of FR-P4-023 (wave 1) |
| Q-P4-16 | Who owns the case record view and its history timeline for the purposes of P4 acceptance, since the screen is rwb-case's while the FSD lists it under P4? | Business analyst with the P3 product owner | `GAP-1577` | The P4 acceptance set (wave 1) |
| Q-P4-17 | Where does the release checklist, training and go-live readiness feature live, given that it is a delivery activity and not product behaviour? | Product owner | `GAP-1578` | The P4 scope statement |

### 12.1 Assumptions this PRD is written under

| ASM | Assumption |
|---|---|
| ASM-2697 | The four business requirement documents are treated as the approved baseline; no governance signature is present in the source documents, so this PRD is Draft. |
| ASM-2698 | Where sources disagree, the Ownership Map ruling and the R-PREC precedence of the Template and Rules apply, and the loser is recorded as a gap. |
| ASM-2699 | rwb-access keeps identity, roles, permissions, scope, masking, the DoA table, the access log and break-glass; the reference-data load surface, the rule package registry, the smoke workflow and the partner identity rows belong to rwb-case, rwb-decision, the platform and rwb-partner. |
| ASM-2700 | The authorise request carries the case reference, owner, queue, team and region, and the answer carries the decision, the area, the right, the scope applied, the matrix version and a masked or clear marker per field ID. |
| ASM-2701 | The masking answer names a field ID with `masked` or `clear`, never a rendering, and a masked caller never causes a clear value to be fetched. |
| ASM-2702 | The policy cache is refreshed when a change event arrives, with a short time to live; the time to live value is not set by any source. |
| ASM-2703 | A break-glass grant lasts until the earlier of four hours and the end of the IAM group, and the reason is 20 to 1000 characters, as the P4 acceptance criteria state. |
| ASM-2704 | The access review list is a role holder list produced six-monthly and delivered as a file through rwb-integration. |
| ASM-2705 | The leaver response time and the access review interval are read from the bank IAM standard when DL38 is answered, and are not set by this PRD. |
| ASM-2706 | Wave 1 administers the matrix and the DoA table by load; the E8 screens add the self-service surface without changing the data model. |
| ASM-2707 | Release dates are the source dates, unchanged and tentative (DL48). |
| ASM-2708 | rwb-access enforces the second factor and the scope for a partner identity; the partner identity rows and the portal are rwb-partner's. |
| ASM-2709 | The targets of the Non-Functional Specification v3 are the Proposed values used until DL11 confirms them. |
| ASM-2710 | The "data lake copy" of REQ-ACA-006 is read as the data products, because Architecture v5 removes the data lake (DP-17). |

## 13. Approval

The requirements approval gate is by the Product Owner and the FDA. This table is left empty; no approval is recorded in this run (ASM-2697).

| Role | Name | Decision | Date | Signature |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

### 13.1 Next step

1. The Product Owner and the FDA approve this PRD.
2. `/clear`, then `/context-updater` adds the business context from the business requirement documents and this PRD.
3. `/clear`, then `/backlog-builder` drafts the backlog from this PRD.
