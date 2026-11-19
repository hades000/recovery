# RWB-E1-022 Sign-on with SSO, MFA and the first roles

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-022 |
| Epic | E1, release 30 November 2026 |
| Module | P4 Access and administration |
| Feature | FEAT-ACA-01 Sign on through Entra ID with single sign-on; FEAT-ACA-02 Enforce multi-factor authentication; FEAT-ACA-03 Hold roles as data |
| Requirement IDs | REQ-ACA-001, REQ-ACA-002, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Program, section 5.4 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-019 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **to sign in to the Workbench once through Entra ID with multi-factor authentication and see only the screens and actions my Workbench roles allow**, so that **access is controlled from the first release and nobody holds a Workbench password or a local account**.

## 2. Business rationale

Access to recovery data today is granted system by system, and the bank cannot show who could see a case on a given date. This story makes Entra ID group membership the only way to hold a Workbench role: one group per role per environment, granted through the bank IAM, read at each sign-in and turned into a session with roles, scope and the permission matrix version in force. It meets REQ-ACA-001, REQ-ACA-002 and REQ-ACA-010 and supports control CTL-09 (access by role and scope). The measure is the access test set in section 16 passing for every role with real users at the release (DL39: administration roles at Epic 1).

## 3. Preconditions

- RWB-E1-001 is done: the role and permission tables exist in the recovery schema.
- RWB-E1-019 is done: the 54 role rows are loaded, and each environment's role rows carry that environment's Entra ID group name in role.entra_group, for example RWB-SIT-RW-CASEOWN in SIT (pattern from the Single sign-on sheet; final names DL40).
- Permission matrix version PM-2026.11 is loaded from the Users, roles and permissions workbook (54 roles against 14 capability areas).
- Separation of duty version SOD-2026.11 is loaded into the role conflict table (new, see section 11) from the Separation of duty sheet.
- The ACE common module sign-in is configured for the Workbench application in Entra ID (INT-21), with the bank conditional access policy that requires a second factor.
- The person was added to the Entra ID group for their role through the bank IAM: the line manager requested it, the role owner approved it and the access administrator carried it out (section 10).

## 4. Flow

1. Person: opens the Workbench in the ACE front end.
2. ACE common module: redirects to Entra ID; the person signs in with password and second factor; Entra ID returns an OpenID Connect token with the groups claim and the amr claim.
3. Workbench (SessionResolver): checks that the amr claim contains "mfa".
4. Workbench: maps each group in the groups claim to an active role row by role.entra_group; groups with no active role row are ignored.
5. Workbench: checks the resulting role set against the role conflict table version in force.
6. Workbench: resolves the session: user reference, roles, the permission matrix version in force at that time, and the default scope of each role.
7. Workbench: writes the sign-in event through the AccessEventPublisher (ACE audit log and SOC log through INT-22).
8. ACE front end: calls GET /me/session and shows the first screen with one line naming the roles and the scope, for example "Case owner. Scope: own cases.", and a menu holding only screens whose capability area has R for at least one role.
9. Person: calls any endpoint; AccessCheck evaluates the capability area and right the endpoint declares against the session's matrix version and allows or refuses the call.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right calls an endpoint, for example the admin API | Refused with 403; the refusal is written to the access event stream with the area and right | MSG-P4-002 | AC2 |
| X2 | The person is in no Workbench group | Session refused with 401; the access request page shows the message and no data | MSG-P4-001 | AC3 |
| X3 | The token has no second factor in the amr claim | Session refused with 401; the refusal is logged | MSG-P4-005 | AC4 |
| X4 | The groups give a role pair listed in the role conflict table | Session refused; an incident is raised to the security administrator; the refusal is logged | MSG-P4-006 | AC6 |
| X5 | A service identity calls an area its role does not hold | Refused with 403, exactly as for a person | MSG-P4-002 | AC7 |
| X6 | A group maps to no active role row | The group is ignored; if no other group maps, X2 applies | MSG-P4-001 | AC8 |
| X7 | A new matrix version takes effect while a session is open | The open session keeps the version it resolved; the next session uses the new one | None | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the tables (RWB-E1-001) and the role rows (RWB-E1-019). The decision log write of access events is added in RWB-E1-039 |
| Negotiable | Group names, roles, conflicts and permissions are data. The story fixes the behavior, not the values |
| Valuable | Every Epic 1 administration user signs in with one bank identity and sees only what the role allows |
| Estimable | One resolver, one access check, one session endpoint, no business screen |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Sign-on with SSO, MFA and the first roles

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.11" is in force from 30 November 2026
    Given separation of duty version "SOD-2026.11" is in force
    Given role RW-CASEOWN has entra_group "RWB-SIT-RW-CASEOWN" and default scope "OWN"

  Scenario: AC1 SSO sign-in
    Given test user "U-1001" is in Entra ID group "RWB-SIT-RW-CASEOWN"
    When the user opens the Workbench and signs in with password and second factor
    Then the session holds roles "RW-CASEOWN", scope "OWN" and matrix version "PM-2026.11"
    Then GET /me/session returns the line "Case owner. Scope: own cases."
    Then the menu shows the screens of the capability areas where RW-CASEOWN holds R, and no Administration menu

  Scenario: AC2 Role denied
    Given test user "U-1002" holds only RW-PHONECOL, whose Platform administration letter is "-"
    When the user calls GET /admin/roles
    Then the system refuses the call with status 403 and message MSG-P4-002 with action "read roles"
    Then the system writes one refusal event with user "U-1002", area "PLATFORM_ADMINISTRATION", right "R" and result "REFUSED"

  Scenario: AC3 Not in group
    Given test user "U-1003" has an Entra ID account and no group whose name starts "RWB-SIT-"
    When the user opens the Workbench
    Then the access request page shows MSG-P4-001 and no case, queue or reference data
    Then every recovery endpoint returns status 401 for that token
    Then the system writes one refusal event with reason "NO_ROLE"

  Scenario: AC4 Sign-in without a second factor is refused
    Given test user "U-1004" is in group "RWB-SIT-RW-CASEOWN"
    Given the token's amr claim holds "pwd" and not "mfa"
    When the token reaches the Workbench
    Then the system refuses the session with status 401 and message MSG-P4-005
    Then the system writes one refusal event with reason "NO_MFA"

  Scenario: AC5 Two roles give the permissions of both
    Given test user "U-1005" is in groups "RWB-SIT-RW-LITOFF" and "RWB-SIT-RW-LEGAL"
    When the user signs in
    Then the session holds roles "RW-LITOFF" and "RW-LEGAL"
    Then the Documents letters are "CRUA", the union of "CRU" and "CRUA"
    Then no permission comes from any role the user does not hold

  Scenario: AC6 A conflicting role pair is refused
    Given test user "U-1006" is in groups "RWB-SIT-RW-SECADM" and "RWB-SIT-RW-CASEOWN"
    Given the role conflict table says RW-SECADM may not hold any business role
    When the user signs in
    Then the system refuses the session with message MSG-P4-006 naming "RW-SECADM" and "RW-CASEOWN"
    Then the system raises an incident to the security administrator queue
    Then the system writes one refusal event with reason "ROLE_CONFLICT"

  Scenario: AC7 A service identity is checked like a person
    Given managed identity "SY-RULES" is in group "RWB-SIT-SY-RULES"
    When it calls GET /admin/roles
    Then the system refuses the call with status 403 and message MSG-P4-002
    Then the system writes one refusal event with user "SY-RULES"

  Scenario: AC8 An unmapped or inactive group gives no role
    Given test user "U-1008" is in groups "RWB-SIT-RW-CASEOWN" and "RWB-SIT-LEGACY01"
    Given no active role row has entra_group "RWB-SIT-LEGACY01"
    When the user signs in
    Then the session holds only "RW-CASEOWN"
    Then the system writes the unmapped group name on the sign-in event

  Scenario: AC9 An open session keeps the versions it resolved
    Given test user "U-1009" signed in at 09:00 on 1 December 2026 under matrix version "PM-2026.11"
    Given matrix version "PM-2026.12" takes effect at 10:00 on 1 December 2026 and removes R in Reporting from RW-CASEOWN
    When the user calls GET /reports/measures at 10:30 in the same session
    Then the system checks the call against "PM-2026.11" and allowed
    Then after the user signs in again at 11:00 the same call is refused with MSG-P4-002
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Membership of the Entra ID group mapped to a role is the only way to hold the role. The Workbench holds no password and no local account | role.entra_group (DF-REF-039); DT07; Admin and access model, section 4.2 |
| BR2 | A session is refused unless the token carries a second factor | NFR-049; FEAT-ACA-02 |
| BR3 | No role inherits from another. A person with two roles holds the union of both roles' letters | permission.letters (DF-REF-043) |
| BR4 | A capability area with no letter for any of the session's roles refuses every action in that area | Permission matrix; CTL-09 |
| BR5 | A role pair listed in the role conflict table may not be held in one session | Separation of duty sheet, roles.txt; role conflict table (new) |
| BR6 | A service identity holds a role in the same table and is checked the same way as a person | REQ-ACA-010; NFR-051 |
| BR7 | A session keeps the matrix and conflict versions it resolved at sign-in until it ends | Admin and access model, section 4.2 |
| BR8 | Group names, roles, letters and conflicts are data rows with a version; none is written in code | Principle 1; DT02 |

## 9. State transitions

None. This story does not change a case status. It creates a session with the states Resolved and Refused, and the session ends at sign-out or token expiry.

## 10. Authority

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

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | role | id | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-036 | role | role_name | Read |
| DF-REF-037 | role | role_class | Read |
| DF-REF-038 | role | default_scope | Read |
| DF-REF-039 | role | entra_group | Read |
| DF-REF-041 | permission | role_id | Read |
| DF-REF-042 | permission | capability_area | Read |
| DF-REF-043 | permission | letters | Read |
| DF-REF-044 | permission | matrix_version | Read |
| DF-REF-206 | role_conflict | role_code | Read |
| DF-REF-207 | role_conflict | conflicts_with | Read |
| DF-REF-209 | role_conflict | conflict_version | Read |
| DF-REF-210 | role_conflict | valid_from | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/admin/roles** (API-P4-007)

| Item | Value |
|---|---|
| Request | None |
| Response | Array of Role: id, roleCode, roleName, roleClass, defaultScope, entraGroup |
| Errors | 401 no valid session or no role (MSG-P4-001, MSG-P4-005, MSG-P4-006); 403 the session's roles hold no R in Platform administration (MSG-P4-002); 503 the ACE sign-in service is unavailable (MSG-GEN-006) |
| Authorization | Platform administration, right R |
| Idempotency | Not applicable, read only |

**GET /me/session** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | None |
| Response | Session: userRef, roles (roleCode, roleName, defaultScope), matrixVersion, conflictVersion, scopeLine, resolvedAt, breakGlass (active, endsAt; filled by RWB-E1-039) |
| Errors | 401 as above |
| Authorization | Any resolved session; no capability area, because the endpoint returns only the caller's own session |
| Idempotency | Not applicable, read only |

**Published interface AccessCheck** (package recovery.access.signin), called by every module's controller through a Spring method interceptor:

```java
AccessDecision check(SessionContext session, CapabilityArea area, Right right);
SessionContext resolve(VerifiedToken token); // throws SessionRefusedException(reasonCode, messageId)
```

**Published interface AccessEventPublisher** (package recovery.access.signin):

```java
void publish(AccessEvent event); // E1: ACE audit and SOC log through INT-22; RWB-E1-039 adds the decision log
```

## 13. Solution plan

- Package: folder `recovery/access/signin` in the recovery module; Java package `recovery.access.signin`. Front end: `recovery/access` folder in the ACE front end.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| AccessAndAdministrationController | Controller | GET /admin/roles and GET /me/session; maps refusals to problem responses with messageCode |
| SessionResolver | Service | Checks the amr claim, maps groups to role rows, applies the conflict check, builds SessionContext |
| AccessCheckService | Published interface | Implements AccessCheck: unions the letters of the session's roles in the area and tests the right |
| AccessCheckInterceptor | Service | Reads the capability area and right declared on each endpoint (x-capability) and calls AccessCheck before the handler |
| AccessEventPublisher | Published interface | Writes sign-in and refusal events to the ACE audit and SOC log |
| AccessAndAdministrationRepository | Repository | Reads role, permission and role_conflict rows in force |
| RoleConflict | Entity | Maps the new role_conflict table |
| SessionBanner | React component | Shows the one-line roles and scope from GET /me/session |
| AccessRequestPage | React component | Shows MSG-P4-001 and no data when the session is refused with NO_ROLE |

- Database: reads role (id, role_code, role_name, role_class, default_scope, entra_group, is_active), permission (role_id, capability_area, letters, matrix_version, is_active). Creates table role_conflict (id uuid, role_code varchar(20), conflicts_with varchar(30), reason varchar(200), conflict_version varchar(20), valid_from date, valid_to date, plus the standard columns) with Flyway migration V_E1_022__role_conflict.sql; conflicts_with holds a role code or the class values ANY_BUSINESS_ROLE and ANY_OTHER_ROLE. Index ix_role_entra_group on role (entra_group) where is_active.
- Configuration and reference data: role rows and group names (loaded by RW-REFADM after RWB-E1-019; names DL40); permission matrix PM-2026.11 (loaded by RW-REFADM, approved per RWB-E1-037); role conflict version SOD-2026.11 (loaded by RW-REFADM from the Separation of duty sheet); LOV-CAPABILITY and LOV-SCOPE; scope line wording from labels per DL10. Property `rwb.access.required-amr=mfa`.
- Build steps:
  1. Create the role_conflict migration and entity; load SOD-2026.11 into SIT with six rows from the Separation of duty sheet that name Workbench roles.
  2. Build SessionResolver: amr check, group to role mapping on active rows, conflict check, SessionContext with versions; unit tests for AC1, AC4, AC5, AC6, AC8.
  3. Build AccessCheckService with letter union per area; unit tests for every letter and the dash.
  4. Build AccessCheckInterceptor reading the declared area and right; contract test that every operation in api.yaml has one.
  5. Build AccessEventPublisher to the ACE audit and SOC log; refusal reason codes NO_ROLE, NO_MFA, ROLE_CONFLICT, NO_RIGHT.
  6. Build GET /admin/roles and GET /me/session with problem responses.
  7. Build SessionBanner, menu filtering by capability area and AccessRequestPage.
  8. Hold the resolved versions on the session and test AC9 with two matrix versions.
- Feature flag: `rwb.access.sso-roles`.
- Done when: the tests in section 16 pass, a test user per Epic 1 administration role signs in with MFA in SIT, and the contract test finds no endpoint without a declared capability area.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-005 | Token without a second factor (new) | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Conflicting role pair at sign-in (new) | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-GEN-006 | ACE sign-in service unavailable | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows DL10; proposed Thai for the new messages is in the additions file.

## 15. Screens and states

No screen in this story. The ACE front end shell shows the session line from GET /me/session at the top of every page and hides menu entries whose capability area the session cannot read. A person with no role sees the access request page with MSG-P4-001 and no data. Epic 1 has no business screens (DL39); RW-CASEOWN test users exist in SIT and UAT only.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-022-01 | AC1, BR1 | System | Test user in RWB-SIT-RW-CASEOWN with MFA |
| TC-E1-022-02 | AC2, BR4 | System | Test user holding RW-PHONECOL only |
| TC-E1-022-03 | AC3, BR1 | System | Entra ID test account with no RWB-SIT group |
| TC-E1-022-04 | AC4, BR2 | System | Token with amr "pwd" only |
| TC-E1-022-05 | AC5, BR3 | System | Test user in the RW-LITOFF and RW-LEGAL groups |
| TC-E1-022-06 | AC6, BR5 | System | Test user in the RW-SECADM and RW-CASEOWN groups |
| TC-E1-022-07 | AC7, BR6 | System | Managed identity SY-RULES |
| TC-E1-022-08 | AC8, BR8 | System | One mapped and one unmapped group |
| TC-E1-022-09 | AC9, BR7 | System | Matrix versions PM-2026.11 and PM-2026.12 with effective times one hour apart |
| TC-E1-022-10 | Access | Access | A role without the right is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: group names, roles, letters, scopes and conflicts are read from tables with their version.
- No personal data in logs, tests or prompts. Access events carry the Entra ID object reference, never the person's name or e-mail.
- No read of another module's tables.
- No local password, local account or role cache that outlives the session.
- Every endpoint declares its capability area and right; an endpoint without one fails the contract test.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-001 | Single sign-on through Entra ID with MFA | Epic 1, 3.4 | FEAT-ACA-01, FEAT-ACA-02 | All recovery processes | BR1, BR2 | TC-E1-022-01, TC-E1-022-03, TC-E1-022-04 |
| REQ-ACA-002 | Roles as data, changed without a code release | Epic 1, 3.4 | FEAT-ACA-03 | All recovery processes | BR3, BR7, BR8 | TC-E1-022-05, TC-E1-022-08, TC-E1-022-09 |
| REQ-ACA-010 | Service identities under the same role checks | Epic 1, 3.4 | FEAT-ACA-02 | All recovery processes | BR4, BR5, BR6 | TC-E1-022-02, TC-E1-022-06, TC-E1-022-07, TC-E1-022-10 |

## 19. Out of scope

- The permission matrix load, PDPA masking, scope filtering and leaver handling (RWB-E1-037).
- Writing access events into the decision log and break-glass (RWB-E1-039).
- Partner identities through the external gateway (RWB-E2-019).
- Full administration screens for roles and access, SCR-43 (Epic 8, FEAT-ADM-01).
- The request, approval and grant steps themselves, which run in the bank IAM, not in the Workbench.
