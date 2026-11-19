<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 019 Partner identities through the external gateway v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 019 Partner identities through the external gateway v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-019 Partner identities through the external gateway

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-019 |
| Epic | E2, release 31 December 2026 |
| Module | P4 Access and administration |
| Feature | FEAT-OCC-13 Give partners identities through the external gateway |
| Requirement IDs | REQ-ACA-012 |
| BRD section | Business Requirements Epic 2, section 3.4; Business Requirements Program, section 5.4 |
| L3 process | 12 Manage partners |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-022, RWB-E1-037, RWB-E1-039 |
| Status | Ready for build |

## 1. Story

As a **partner and agency manager (RW-AGENCYMG)**, I want **law firms, valuers and collection agencies to sign in to the partner portal with partner identities through the external gateway, with multi-factor authentication, one role per partner type and access limited to the work placed with their firm**, so that **partners can work in the Workbench from Epic 5 without SCB accounts, and a firm that leaves the panel loses access the same day**.

## 2. Business rationale

Partners today use separate channels (the LIT lawyer web, the OA portal, SVAF and SFTP), and the bank cannot show one record of what a firm could see. This story gives each partner user a partner identity separate from bank identities, binds it to one firm and one partner role, limits it to cases placed with that firm and to the instruction types of the role, and refuses access when the firm is suspended, exits the panel or reaches its contract end. It meets REQ-ACA-012 and NFR-050. Opening the Workbench to users outside the bank needs the architecture change under DL03, so the story is built and tested in SIT and UAT with the feature off in PROD until DL03 is approved; law firms are first needed at Epic 5 in March 2027.

## 3. Preconditions

- RWB-E1-022, RWB-E1-037 and RWB-E1-039 are done: sessions, the permission matrix with scope, and access events in the decision log.
- The partner role rows PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC are loaded with role class PARTNER_USER and their Entra ID groups, for example RWB-SIT-PT-LAWFIRM (Single sign-on sheet; names DL40). PT-LED has no login.
- The partner identity directory is reachable from the external gateway in SIT and UAT (INT-24); in PROD it waits for DL03.
- The partner table holds the panel firms with partner_type, panel_status and contract_end (S9 Partner management), read through the S9 published interface.
- Parameters in the catalog: rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE; rwb.access.partner.instruction-types.PT-VALUER=APPRAISE; rwb.access.partner.instruction-types.PT-AGENCY=COLLECT (assumed; owner RW-AGENCYMG); rwb.refload.approver.partner_user=RW-SECADM.

## 4. Flow

1. Partner and agency manager (RW-AGENCYMG): requests a partner user in the bank IAM, naming the firm, the partner role and the person's business e-mail at the firm.
2. Role owner: approves the request; access administrator creates the partner identity in the partner directory and adds it to the group of the partner role.
3. Reference data administrator (RW-REFADM): loads the partner user binding (partner identity, partner ID, role, valid from, valid to) with POST /admin/reference-loads table "partner_user"; RW-SECADM approves it.
4. Partner user: opens the partner portal through the external gateway and signs in with password and second factor.
5. Workbench (SessionResolver): checks the token comes from the partner directory, holds "mfa" in the amr claim and maps to exactly one partner role; finds the active binding for the identity.
6. Workbench (PartnerAccessService): asks the S9 interface for the firm's panel status and contract end; refuses the session unless the status is ACTIVE or ON_NOTICE and the contract end is today or later.
7. Workbench: resolves the session with scope PLACED, the partner ID and the instruction types of the role; writes an AC-SIGN entry.
8. Partner portal PRT-01 Partner home: lists the open instructions through GET /partner/instructions; the S9 handler applies the PLACED scope filter, so only instructions of the partner's firm and of the role's instruction types return.
9. Workbench: on each request, checks the binding and the firm status again (refreshed at most every 5 minutes, assumed; DL38) and ends the session when either has ended.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The firm is suspended or has exited the panel, or its contract end has passed | Sign-in refused; an open session ends at the next request; refusal logged | MSG-P4-008 | AC3 |
| X2 | The partner identity has no active binding to a firm | Session refused with 401; refusal logged | MSG-P4-001 | AC4 |
| X3 | The token has no second factor | Session refused with 401 | MSG-P4-005 | AC5 |
| X4 | A partner requests an instruction placed with another firm | Refused with 404; nothing returned | MSG-P4-003 | AC6 |
| X5 | A partner identity is in two partner role groups, or in a bank role group | Session refused; incident raised to the security administrator | MSG-P4-006 | AC7 |
| X6 | A partner calls an endpoint outside the partner role's letters, for example the case list | Refused with 403 | MSG-P4-002 | AC8 |
| X7 | A bank identity tries to sign in through the external gateway | Refused; bank users sign in only through the bank route | MSG-P4-001 | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the session, the matrix and the access log from Epic 1; the partner instruction endpoints are S9's |
| Negotiable | Partner roles, instruction types and the binding are data; the PROD date follows DL03 |
| Valuable | One controlled way for partners into the Workbench, ready for law firms at Epic 5 |
| Estimable | One binding table, one partner check in the resolver, one scope type |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Partner identities through the external gateway

  Background:
    Given the environment is UAT and feature "rwb.access.partner-signin" is on
    Given partner "LF-0012" is a LAW_FIRM with panel status "ACTIVE" and contract end 30 June 2027
    Given partner "LF-0019" is a LAW_FIRM with panel status "ACTIVE"
    Given partner "VL-0004" is a VALUER with panel status "ACTIVE"

  Scenario: AC1 Partner sign-in
    Given partner identity "P-5101" is in group "RWB-UAT-PT-LAWFIRM" and bound to "LF-0012"
    Given 5 open instructions are placed with "LF-0012" and 3 with "LF-0019"
    When "P-5101" signs in through the external gateway with password and second factor
    Then the session holds role "PT-LAWFIRM", scope "PLACED" and partner "LF-0012"
    Then PRT-01 Partner home lists the 5 instructions of "LF-0012" and none of "LF-0019"
    Then one entry with decision code "AC-SIGN" and actor "P-5101" is written

  Scenario: AC2 Role per partner
    Given partner identity "P-5102" is in group "RWB-UAT-PT-VALUER" and bound to "VL-0004"
    Given "VL-0004" holds 2 instructions of type "APPRAISE" and 1 of type "LIST"
    When "P-5102" signs in
    Then PRT-01 Partner home lists the 2 "APPRAISE" instructions only

  Scenario: AC3 Revoked
    Given partner identity "P-5101" is bound to "LF-0012"
    Given "LF-0012" moves to panel status "EXITED" at 11:00 on 4 January 2027
    When "P-5101" tries to sign in at 11:20
    Then the system refuses access with message MSG-P4-008
    Then one entry with decision code "AC-DENY" and reason "PARTNER_NOT_ACTIVE" is written
    Then the system ends a session of "P-5101" opened at 10:00 at its first request after 11:05

  Scenario: AC4 A partner identity with no binding is refused
    Given partner identity "P-5103" is in group "RWB-UAT-PT-LAWFIRM" and has no active binding
    When "P-5103" signs in
    Then the system refuses the session with status 401 and message MSG-P4-001
    Then one entry with decision code "AC-DENY" and reason "NO_PARTNER_BINDING" is written

  Scenario: AC5 A partner without a second factor is refused
    Given partner identity "P-5101" signs in with a token whose amr claim holds "pwd" only
    When the token reaches the Workbench
    Then the system refuses the session with status 401 and message MSG-P4-005

  Scenario: AC6 An instruction of another firm is not returned
    Given "P-5101" is signed in for "LF-0012"
    When "P-5101" requests instruction "INS-2027-000431" placed with "LF-0019"
    Then the call returns status 404 with message MSG-P4-003 and no instruction data

  Scenario: AC7 Two partner roles or a bank role are refused
    Given partner identity "P-5104" is in groups "RWB-UAT-PT-LAWFIRM" and "RWB-UAT-PT-VALUER"
    When "P-5104" signs in
    Then the system refuses the session with message MSG-P4-006 and an incident is raised to the security administrator queue

  Scenario: AC8 A partner cannot reach bank screens
    Given "P-5101" is signed in with role "PT-LAWFIRM", whose Queue and allocation letter is "-"
    When "P-5101" calls GET /queues
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC9 A bank identity cannot use the external gateway
    Given test user "U-5105" holds RW-LITOFF with a bank identity
    When "U-5105" signs in through the external gateway
    Then the system refuses the session with message MSG-P4-001
    Then one entry with decision code "AC-DENY" and reason "BANK_IDENTITY_ON_PARTNER_ROUTE" is written
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A partner user holds a partner identity separate from bank identities, signs in only through the external gateway and only with multi-factor authentication | NFR-050; INT-24; Admin and access model, section 8.1; REQ-ACA-012 |
| BR2 | A partner user holds exactly one partner role and is bound to exactly one firm | Partner binding table (new); separation of duty |
| BR3 | A partner user sees only cases and instructions placed with their firm (scope PLACED) | Key sheet, roles.txt, scope "Placed cases" |
| BR4 | A partner role sees only the instruction types named for it | Parameters rwb.access.partner.instruction-types.*; LOV-INSTRUCTION |
| BR5 | Access ends when the firm's panel status is SUSPENDED or EXITED, or its contract end has passed | partner.panel_status (DF-PRT-005), partner.contract_end (DF-PRT-006); LOV-PANEL; R-UNI-26 |
| BR6 | The permission matrix, masking and the access log apply to partner users as to bank users | Admin and access model, section 8.1 |
| BR7 | No partner reaches the Workbench in PROD until the architecture change for external access is approved | DL03 |
| BR8 | Partner users are requested by the partner and agency manager, approved by the role owner and created by the access administrator | Admin and access model, section 8.1 |

## 9. State transitions

None. This story does not change a case status. A partner session moves from Resolved to Ended when the firm's status or the binding ends.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG Partner and agency manager | Requests partner users in the bank IAM; sets the firm's panel status in S9 |
| Role owner (bank IAM, level 2) | Approves each partner user request |
| Access administrator (bank IAM, level 3) | Creates the partner identity and adds it to the partner role group |
| RW-REFADM Reference data administrator | Loads the partner user binding (Reference data C) |
| RW-SECADM Security administrator | Approves the binding version; maintains the partner role groups; receives conflict incidents |
| PT-LAWFIRM, PT-VALUER, PT-AGENCY | Sign in and work their firm's instructions with the letters of their role (Partner portal RU) |
| Architecture team | Approves external access before PROD (DL03) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-213 | partner_user | identity_ref | Write, read |
| DF-REF-214 | partner_user | partner_id | Write, read |
| DF-REF-215 | partner_user | role_code | Write, read |
| DF-REF-216 | partner_user | valid_from | Write, read |
| DF-REF-217 | partner_user | valid_to | Write, read |
| DF-PRT-001 | partner | id | Read through the S9 published interface |
| DF-PRT-004 | partner | partner_type | Read through the S9 published interface |
| DF-PRT-005 | partner | panel_status | Read through the S9 published interface |
| DF-PRT-006 | partner | contract_end | Read through the S9 published interface |
| DF-PRT-010 | partner_instruction | partner_id | Read by the S9 repository applying the PLACED scope filter |
| DF-PRT-011 | partner_instruction | instruction_type | Read by the S9 repository applying the PLACED scope filter |
| DF-REF-035 | role | role_code | Read |
| DF-REF-037 | role | role_class | Read |
| DF-REF-039 | role | entra_group | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (sign-in and refusal access events) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/partner/instructions** (owned by S9; this story supplies the scope filter)

| Item | Value |
|---|---|
| Request | Query: status, page, size |
| Response | InstructionPage of PartnerInstruction |
| Errors | 401 no session or partner not active (MSG-P4-001, MSG-P4-008); 403 role without Partner portal R (MSG-P4-002); 503 (MSG-GEN-006) |
| Authorization | Partner portal, right R, scope PLACED |
| Idempotency | Not applicable, read only |

**POST /api/recovery/v1/admin/reference-loads** (API-P4-005) with table "partner_user"; Reference data C; Idempotency-Key header. Approve with POST /admin/reference-loads/{loadId}/approve by RW-SECADM (approver role for the table).

**GET /api/recovery/v1/me/session** (new in RWB-E1-022) returns partnerId and scope PLACED for a partner session.

**Published interfaces**

```java
// P4, package recovery.access.partner
ScopeFilter scopeFor(SessionContext session); // type PLACED, partnerId, instructionTypes
// S9, called by P4
PartnerStatus partnerStatus(UUID partnerId);  // panelStatus, contractEnd
```

## 13. Solution plan

- Package: folder `recovery/access/partner` in the recovery module; Java package `recovery.access.partner`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| AccessAndAdministrationController | Controller | Reference load for table partner_user (shared load endpoint) |
| PartnerAccessService | Service | Checks token issuer and route, one partner role, active binding and firm status; builds the PLACED scope |
| PartnerUserLoader | Service | Validates a binding file: known partner IDs through S9, partner role codes only, no identity bound twice in one period |
| PartnerSessionRevalidation | Service | Rechecks binding and firm status on each request after the refresh interval |
| PartnerUserRepository | Repository | Reads and writes partner_user rows |
| PartnerUser | Entity | Maps the new partner_user table |
| PartnerSignInPage | React component | Partner sign-in entry in the partner portal with MSG-P4-008 and MSG-P4-001 states |

- Database: creates table partner_user (id uuid, identity_ref varchar(64), partner_id uuid, role_code varchar(20), valid_from date, valid_to date, plus the standard columns) with Flyway migration V_E2_019__partner_user.sql; unique index on (identity_ref, valid_from); no foreign key to partner, which is S9's table.
- Configuration and reference data: partner role rows and groups (DL40); the binding version (RW-REFADM loads, RW-SECADM approves); instruction types per partner role (parameters, owner RW-AGENCYMG); rwb.access.membership-refresh-minutes=5 (assumed, DL38); external gateway route for the partner portal (INT-24, DL03).
- Build steps:
  1. Create the partner_user migration, entity and loader with validation.
  2. Extend SessionResolver to tell the partner route from the bank route and to refuse a bank identity on the partner route (AC9) and a partner identity on the bank route.
  3. Build PartnerAccessService with the binding and the S9 status call; tests for AC1, AC3, AC4, AC7.
  4. Add scope type PLACED with partner ID and instruction types to ScopeFilter; give S9 a repository test for AC1, AC2 and AC6.
  5. Build PartnerSessionRevalidation; test the session end in AC3.
  6. Confirm AC5 and AC8 through the RWB-E1-022 checks with partner tokens.
  7. Put the partner route behind the feature flag, off in PROD until DL03.
- Feature flag: `rwb.access.partner-signin`.
- Done when: the tests in section 16 pass in UAT through the external gateway test route, and the flag is off in PROD.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-008 | The firm is suspended, exited or past its contract end (new) | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. |
| MSG-P4-001 | No binding, or a bank identity on the partner route | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-005 | No second factor | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Two partner roles, or a partner and a bank role | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-P4-003 | An instruction of another firm | This case is not in your scope. |
| MSG-P4-002 | An endpoint outside the partner role's letters | You cannot {action} here. Your role does not include it. |

Thai text for each message follows DL10; proposed Thai for MSG-P4-008 is in the additions file.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| PRT-01 Partner home | Loading | Waits while the firm's open instructions load |
| PRT-01 Partner home | List | Sees only the firm's instructions of the role's types, with due dates |

A refused partner sees the partner sign-in page with MSG-P4-008 or MSG-P4-001 and no data.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-01 | AC1, BR1, BR3 | System | Synthetic firms LF-0012 and LF-0019 with 5 and 3 instructions |
| TC-E2-019-02 | AC2, BR4 | System | Valuer VL-0004 with APPRAISE and LIST instructions |
| TC-E2-019-03 | AC3, BR5 | System | Firm moved to EXITED during an open session |
| TC-E2-019-04 | AC4, BR2 | System | Partner identity with no binding |
| TC-E2-019-05 | AC5, BR1 | System | Partner token without a second factor |
| TC-E2-019-06 | AC6, BR3 | System | Instruction of another firm |
| TC-E2-019-07 | AC7, BR2 | System | Partner identity in two partner role groups |
| TC-E2-019-08 | AC8, BR6 | System | Partner calling GET /queues |
| TC-E2-019-09 | AC9, BR1 | System | Bank test user on the partner route |
| TC-E2-019-10 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E2-019-11 | Principle 5 | Resilience | The decision log write forced to fail during a partner sign-in |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: partner roles, instruction types, the binding and the refresh interval are data.
- No personal data in logs, tests or prompts; partner identities are referenced by their directory ID, never by e-mail or name.
- No read of another module's tables: partner status comes from the S9 interface and the instruction filter is applied by the S9 repository.
- No partner route in PROD while DL03 is open.
- A partner session never holds a bank role.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partners only through the external gateway, with MFA, scoped to their own cases | Epic 2, 3.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR8 | TC-E2-019-01 to TC-E2-019-11 |

## 19. Out of scope

- The architecture change that makes the partner portal reachable from outside the bank (DL03).
- Partner work screens PRT-02 to PRT-06 and the instruction endpoints (Epic 4 to Epic 6, S9 and S6 stories).
- Partner panel management, contracts and scorecards (SCR-34 in Epic 2 for identities; Epic 6 for the full panel).
- Customers, guarantors, heirs and bidders, who do not sign in to the Workbench.
