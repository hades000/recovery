# RWB-ITG-E2019-ITG Partner identities through the external gateway

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2019-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E2019-APP, RWB-S9-E2019-APP, RWB-P7-E2019-APP (none done yet) |
| Contract dependencies | None |
| Integration dependencies | RWB-P4-E2019-APP, RWB-S9-E2019-APP, RWB-P7-E2019-APP |
| External dependencies | None |
| Open decisions | DL03 (ASM-0189, ASM-0193, ASM-0578, ASM-2567); DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863) |
| Partner gateway test route and harness | Not specified in the source documents (GAP-0403) |
| Partner identity resolution | POST /partner-identities/resolve on /api/recovery/access/v1; publishes no event and consumes none |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-E2019-ITG-14) |
| Size | Not specified in the source documents (DOR-RWB-ITG-E2019-ITG-16) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-ITG-E2019-ITG-22) |
| Contract version built against | Not specified in the source documents (DOR-RWB-ITG-E2019-ITG-23); paths carry /v1 |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-030, FR-PLT-031, FR-PLT-032) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-019 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 17 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **one repeatable cross-service harness that drives partner identities through the external gateway against rwb-access, rwb-partner and rwb-decision and writes one evidence report per run**, so that **a partner session is proved to hold exactly one partner role bound to one firm, to be scoped to the work placed with that firm, to be refused when the firm or the identity is not active, and to be refused a bank role, a second role, a missing second factor or a bank screen — across services, before partners work live at Epic 5 and on every release after**.

The harness builds no production screen, endpoint or table: the partner portal screen, the partner instruction endpoints and the access events belong to the app stories of this legacy key (RWB-P4-E2019-APP, RWB-S9-E2019-APP and RWB-P7-E2019-APP). This story builds the harness, the fakes, the seeds and the evidence, and owns the ten acceptance criteria listed in section 7.

### 2. Business rationale

Partners today use separate channels (the LIT lawyer web, the OA portal, SVAF and SFTP), and the bank cannot show one record of what a firm could see. The legacy story gave each partner user a partner identity separate from bank identities, bound it to one firm and one partner role, limited it to cases placed with that firm and to the instruction types of the role, and refused access when the firm is suspended, exits the panel or reaches its contract end. In the target architecture that one journey is served by three services: rwb-access resolves the session, the role and the scope; rwb-partner holds the panel status, the contract end and the instructions; rwb-decision holds the access events and the central ledger. A defect at any seam — the wrong scope filter, a stale panel status, a missing decision code — would only appear when a real firm signs in, unless the journey is exercised across the three services as one flow.

This story is that exercise. It runs the partner sign-in journey from the external gateway through the fakes and then through the real services as their app stories land, reproduces every refusal the legacy story defined in the same run, and attaches one evidence report per run keyed by story and business date, so the partner route can be shown to hold before it is switched on and after every change.

It meets REQ-ACA-012 and NFR-050. Opening the Workbench to users outside the bank needs the architecture change under DL03, so the harness runs in SIT and UAT with `rwb.access.partner-signin` off in PROD until DL03 is approved; law firms are first needed at Epic 5 in March 2027. The partner gateway test route, the directory test tenant and the evidence format are not specified in the source documents (GAP-0403; ASM-0578).

### 3. Preconditions

- The wave 2 harness pack exists in the integration repository with its runner, its seed files and its report publisher; the harness environment is not specified in the source documents (GAP-0403; ASM-0578).
- The partner gateway test route to rwb-partner is reachable in SIT and UAT, and the partner directory test tenant can issue a token with the `amr` claim. The route definition and the FAPI 2.0 profile of that test route are not specified in the source documents (GAP-0403; ASM-0578).
- WireMock fakes for rwb-access, rwb-partner, rwb-decision and rwb-case are published from their OpenAPI contracts, so the journey runs on Day 1 before any app story lands.
- The synthetic seeds of the legacy story exist: partner "LF-0012" is a LAW_FIRM with panel status "ACTIVE" and contract end 30 June 2027, partner "LF-0019" is a LAW_FIRM with panel status "ACTIVE", partner "VL-0004" is a VALUER with panel status "ACTIVE", and partner identities P-5101, P-5102, P-5103 and P-5104 and test user U-5105 are seeded in the partner role groups of the legacy Background.
- The partner role rows PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER and PT-RAMC are loaded with role class PARTNER_USER and their groups, for example RWB-SIT-PT-LAWFIRM; PT-LED has no login.
- The parameter values of the legacy story are loaded: `rwb.access.partner.instruction-types.PT-LAWFIRM=FILE_SUIT,ENFORCE`, `rwb.access.partner.instruction-types.PT-VALUER=APPRAISE`, `rwb.access.partner.instruction-types.PT-AGENCY=COLLECT` and `rwb.refload.approver.partner_user=RW-SECADM`.
- Feature `rwb.access.partner-signin` is on in the harness environment and off in PROD.
- No build dependency: the harness starts on Day 1 against the fakes, and each fake is replaced by the real service as its I story lands (RWB-P4-E2019-APP, RWB-S9-E2019-APP, RWB-P7-E2019-APP).

### 4. Flow

1. Harness: starts a run for the story and the business date, takes the run lock and records the build under test, the pack version and the fake or real mode of each of the four services.
2. Harness: seeds the run — the three firms, the partner identities, the bindings, the eight instructions (5 placed with LF-0012, 3 with LF-0019) and the 2 APPRAISE and 1 LIST instruction of VL-0004 — through the contract of the owning service, or through the fake in fake mode. Data seeding is not specified in the source documents (GAP-0403; ASM-0578).
3. Harness: signs P-5101 in through the partner gateway test route with password and second factor, then reads the resolved session from `GET /api/recovery/access/v1/me/session` and asserts role PT-LAWFIRM, scope PLACED and partner LF-0012.
4. Harness: reads the PRT-01 list through `GET /api/recovery/partner/v1/partner/instructions` and asserts the 5 instructions of LF-0012 and none of LF-0019.
5. Harness: reads `GET /api/recovery/access/v1/admin/access-log` and `GET /api/recovery/decision/v1/decision-log` and asserts the AC-SIGN entry with actor P-5101 and the matching decision record on `rwb.decision-record.v1`.
6. Harness: repeats the sign-in for P-5102 bound to VL-0004 and asserts the 2 APPRAISE instructions only, and no LIST instruction.
7. Harness: moves LF-0012 to panel status EXITED at 11:00 on 4 January 2027, tries the sign-in of P-5101 at 11:20 and asserts MSG-P4-008 and an AC-DENY entry with reason PARTNER_NOT_ACTIVE; then asserts that a session opened at 10:00 ends at its first request after 11:05.
8. Harness: signs in P-5103 with no active binding and asserts 401 with MSG-P4-001 and an AC-DENY entry with reason NO_PARTNER_BINDING (AC4), and signs in a token whose `amr` claim holds "pwd" only and asserts 401 with MSG-P4-005 (AC5).
9. Harness: signs in P-5104 placed in the PT-LAWFIRM and the PT-VALUER groups and asserts refusal with MSG-P4-006 and an incident on the security administrator queue (AC7).
10. Harness: with P-5101 signed in, calls `GET /api/recovery/case/v1/queues` and asserts 403 with MSG-P4-002 (AC8).
11. Harness: drives the two journeys owned by the app stories inside the same run — instruction INS-2027-000431 placed with LF-0019 returns 404 with MSG-P4-003 (AC6), and a bank identity on the partner route is refused with MSG-P4-001 and an AC-DENY entry with reason BANK_IDENTITY_ON_PARTNER_ROUTE (AC9) — and records them as cited, not as criteria of this story.
12. Harness: publishes the evidence report keyed by story id and business date with one row per criterion, the seam each row exercised, the service or fake that answered, the entry or record observed and the pass or fail result; the evidence format and retention are not specified in the source documents (GAP-0403; ASM-0578).
13. Harness: releases the run lock and, on any failed criterion, fails the run and names the criterion, the seam and the observed value.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The firm is suspended or has exited the panel, or its contract end has passed | Sign-in refused; an open session ends at the next request; refusal logged | MSG-P4-008 | AC3 |
| X2 | The partner identity has no active binding to a firm | Session refused with 401; refusal logged | MSG-P4-001 | AC4 |
| X3 | The token has no second factor | Session refused with 401 | MSG-P4-005 | AC5 |
| X4 | A partner requests an instruction placed with another firm | Refused with 404; nothing returned | MSG-P4-003 | AC6 |
| X5 | A partner identity is in two partner role groups, or in a bank role group | Session refused; incident raised to the security administrator | MSG-P4-006 | AC7 |
| X6 | A partner calls an endpoint outside the partner role's letters, for example the case list | Refused with 403 | MSG-P4-002 | AC8 |
| X7 | A bank identity tries to sign in through the external gateway | Refused; bank users sign in only through the bank route | MSG-P4-001 | AC9 |

X4 and X7 are cited in this table and driven inside the same run, but AC6 and AC9 are owned by the app stories of this legacy key: the instruction filter by RWB-S9-E2019-APP and the route separation by RWB-P4-E2019-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the published contracts, the fakes and the partner gateway test route; no build dependency and no work order inside another team's lane |
| Negotiable | The seeds, the route and the threshold of each assertion are configuration and data; the criteria are the legacy ones |
| Valuable | The partner route is proved across three services before a firm signs in, and stays proved each release |
| Estimable | One runner, four fakes, one seed set, one report publisher and one gate |
| Small | Fits in two weeks with its tests, alongside the app stories it waits for |
| Testable | Each of the eleven `-ITG` test cases is one run of the harness and one row of the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: Partner identities through the external gateway

  Background:
    Given the environment is UAT and feature "rwb.access.partner-signin" is on
    Given partner "LF-0012" is a LAW_FIRM with panel status "ACTIVE" and contract end 30 June 2027
    Given partner "LF-0019" is a LAW_FIRM with panel status "ACTIVE"
    Given partner "VL-0004" is a VALUER with panel status "ACTIVE"

  Scenario: AC1 Partner sign-in (legacy RWB-E2-019 AC1)
    Given partner identity "P-5101" is in group "RWB-UAT-PT-LAWFIRM" and bound to "LF-0012"
    Given 5 open instructions are placed with "LF-0012" and 3 with "LF-0019"
    When "P-5101" signs in through the external gateway with password and second factor
    Then the session holds role "PT-LAWFIRM", scope "PLACED" and partner "LF-0012"
    Then PRT-01 Partner home lists the 5 instructions of "LF-0012" and none of "LF-0019"
    Then one entry with decision code "AC-SIGN" and actor "P-5101" is written

  Scenario: AC2 Role per partner (legacy RWB-E2-019 AC2)
    Given partner identity "P-5102" is in group "RWB-UAT-PT-VALUER" and bound to "VL-0004"
    Given "VL-0004" holds 2 instructions of type "APPRAISE" and 1 of type "LIST"
    When "P-5102" signs in
    Then PRT-01 Partner home lists the 2 "APPRAISE" instructions only

  Scenario: AC3 Revoked (legacy RWB-E2-019 AC3)
    Given partner identity "P-5101" is bound to "LF-0012"
    Given "LF-0012" moves to panel status "EXITED" at 11:00 on 4 January 2027
    When "P-5101" tries to sign in at 11:20
    Then the system refuses access with message MSG-P4-008
    Then one entry with decision code "AC-DENY" and reason "PARTNER_NOT_ACTIVE" is written
    Then the system ends a session of "P-5101" opened at 10:00 at its first request after 11:05

  Scenario: AC4 A partner identity with no binding is refused (legacy RWB-E2-019 AC4)
    Given partner identity "P-5103" is in group "RWB-UAT-PT-LAWFIRM" and has no active binding
    When "P-5103" signs in
    Then the system refuses the session with status 401 and message MSG-P4-001
    Then one entry with decision code "AC-DENY" and reason "NO_PARTNER_BINDING" is written

  Scenario: AC5 A partner without a second factor is refused (legacy RWB-E2-019 AC5)
    Given partner identity "P-5101" signs in with a token whose amr claim holds "pwd" only
    When the token reaches the Workbench
    Then the system refuses the session with status 401 and message MSG-P4-005

  Scenario: AC7 Two partner roles or a bank role are refused (legacy RWB-E2-019 AC7)
    Given partner identity "P-5104" is in groups "RWB-UAT-PT-LAWFIRM" and "RWB-UAT-PT-VALUER"
    When "P-5104" signs in
    Then the system refuses the session with message MSG-P4-006 and an incident is raised to the security administrator queue

  Scenario: AC8 A partner cannot reach bank screens (legacy RWB-E2-019 AC8)
    Given "P-5101" is signed in with role "PT-LAWFIRM", whose Queue and allocation letter is "-"
    When "P-5101" calls GET /queues
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC10 A partner user is created only after request and approval, and no partner reaches PROD before the architecture change is approved (BR7, BR8) (new, D-RCV-60)
    Given the environment is PROD and the architecture change for external access is not approved
    When a partner user is requested by the partner and agency manager and approved by the role owner
    Then the access administrator creates the partner user and the partner still cannot sign in in PROD

  Scenario: AC11 A redelivered decision record event is not counted twice (new, D-RCV-60)
    Given the sign-in of "P-5101" has written one entry with decision code "AC-SIGN" and the harness has consumed its rwb.decision.DecisionRecorded.v1 event
    When the same event is delivered a second time on rwb.decision-record.v1
    Then GET /api/recovery/decision/v1/decision-log still returns one entry with decision code "AC-SIGN" and actor "P-5101" for that sign-in
    And the result of the harness assertion is the same as after the first delivery

  Scenario: AC12 A consumed call fails or does not answer (new, D-RCV-60)
    Given partner identity "P-5101" is bound to "LF-0012"
    When "P-5101" signs in and the call to POST /partner-identities/resolve fails or does not answer
    Then the system refuses the session with message Not specified in the source documents (NEWAC-RWB-ITG-E2019-ITG-AC12) and grants no partner role
```

AC6 and AC9 are cited in the flow and exception table but are owned by the app stories of this legacy key (RWB-P4-E2019-APP and RWB-S9-E2019-APP); the ten criteria above are the ones this ITG story owns.

### 8. Business rules

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

### 9. State transitions

None. This story does not change a case status. A partner session moves from Resolved to Ended when the firm's status or the binding ends.

The harness adds no state transition of its own: it observes the session moving from Resolved to Ended at the first request after the refresh interval and records the observation as the AC3 row of the evidence report.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AGENCYMG Partner and agency manager | Requests partner users in the bank IAM; sets the firm's panel status in S9 |
| Role owner (bank IAM, level 2) | Approves each partner user request |
| Access administrator (bank IAM, level 3) | Creates the partner identity and adds it to the partner role group |
| RW-REFADM Reference data administrator | Loads the partner user binding (Reference data C) |
| RW-SECADM Security administrator | Approves the binding version; maintains the partner role groups; receives conflict incidents |
| PT-LAWFIRM, PT-VALUER, PT-AGENCY | Sign in and work their firm's instructions with the letters of their role (Partner portal RU) |
| Architecture team | Approves external access before PROD (DL03) |
| QA lead | Owns the harness pack, the seeds and the evidence format |
| Platform edge owner | Owns the partner gateway test route and its FAPI 2.0 profile in SIT and UAT |
| No approval level from the delegation of authority applies | The harness takes no business decision; it asserts the refusals of the app stories |

### 11. Data

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
| DF-ACE-301 | v_ace_iam_group | entra_group | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (sign-in and refusal access events) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

The harness itself owns no table and writes no row (DP-01): it reads every value through the owning service's contract and asserts it, and the writes listed above are performed by the app stories of this legacy key when the harness drives them. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | PRT-01 list for the signed-in partner; the S9 handler applies the PLACED scope filter and the instruction types of the role (AC1, AC2, AC6) |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | Panel status, partner type and contract end of the signed-in partner's firm (AC1, AC3) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | Resolved session: partner id, role, scope PLACED and instruction types (AC1, AC2, AC3, AC5, AC7) |
| GET | `/api/recovery/access/v1/admin/access-log` | P4 rwb-access | AC-SIGN and AC-DENY entries with decision code, actor and reason (AC1, AC3, AC4, AC9) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision record collected on `rwb.decision-record.v1` into the central ledger (AC1, AC3, AC4) |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | The expected refusal of AC8: a partner role without the Queue and allocation letter gets 403 with MSG-P4-002 |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout and idempotency keys only where a POST is made (DP-11, DP-13); the harness makes no POST. It reads the session the gateway resolved rather than calling authorise itself, so AC1, AC2, AC5 and AC7 are asserted on `/me/session` and on the access-log entries. No operation is called on another service's base and no service is asked to call a second service.

#### 12.3 Events published

None. The harness publishes no Kafka event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | All 19 services; in this journey the access event is written by P4 rwb-access and sealed by P7 rwb-decision | The access event written by the sign-in or the refusal is asserted on the ledger after the record is collected (AC1, AC3, AC4); a redelivered event is asserted not to count twice (AC11) |

The harness consumes the topic as a test consumer with its own group and asserts the record through `GET /api/recovery/decision/v1/decision-log`; it holds no inbox table of its own and gets no record of production data.

#### 12.5 Workflows and activities

None. The harness starts no Temporal workflow and calls no activity; the partner session is resolved inside one REST hop on each request, so no queue `rwb-<short>` is used.

#### 12.6 Schedules

None. The harness runs from the pipeline or by hand for a story and a business date, and creates no Temporal Schedule.

#### 12.7 Tables owned

None. The harness owns no table and no schema (DP-01); it seeds and reads through the owning services' contracts only.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-access (WireMock, from its OpenAPI) | `GET /api/recovery/access/v1/me/session` and `GET /api/recovery/access/v1/admin/access-log`, plus the authorise call the gateway makes before a session is resolved | AC1, AC2, AC4, AC5, AC7; TC-E2-019-10-ITG |
| rwb-partner (WireMock, from its OpenAPI) | `GET /api/recovery/partner/v1/partners` and `GET /api/recovery/partner/v1/partner/instructions`, with the PLACED scope filter and the panel status fixtures | AC1, AC2, AC3, AC6 |
| rwb-decision (WireMock, from its OpenAPI) | `GET /api/recovery/decision/v1/decision-log` and the `rwb.decision-record.v1` consumer feed | AC1, AC3, AC4; TC-E2-019-11-ITG |
| rwb-case (WireMock, from its OpenAPI) | `GET /api/recovery/case/v1/queues` as the refusal the partner role must receive | AC8 |
| External partner gateway test route | The route that fronts rwb-partner: sign-in with password and second factor, the `amr` claim, the token issuer, and the refusal of a bank identity | every scenario |

The fakes are generated from the published OpenAPI documents of the four services and are versioned with the harness pack. The partner gateway test route and its FAPI 2.0 profile are not specified in the source documents (GAP-0403; ASM-0578).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, each one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s timeout (DP-11, DP-13) |
| Kafka | 0 published, 1 consumed: `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | None: no workflow, no activity, no queue |
| File | None |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named in the table (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H column; DP-15 resolves to "no migration", because the harness owns no schema. The blocking dependencies of this story are the three I stories, RWB-P4-E2019-APP, RWB-S9-E2019-APP and RWB-P7-E2019-APP, which replace the fakes with the real behaviour; they gate the done state, not the Day-1 start.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| PartnerJourneyRunner | Job | Runs the eleven `-ITG` cases in one run, in fake mode or in real mode per service |
| PartnerGatewayClient | Client | Signs in through the partner gateway test route and carries the token with its `amr` claim |
| FakeRegistry | Configuration | Publishes and selects the rwb-access, rwb-partner, rwb-decision and rwb-case WireMock fakes and their mode per run |
| PartnerSeedLoader | Service | Seeds the three firms, the four partner identities, the bindings and the eight instructions through the owner's contract or the fake |
| SessionAsserter | Service | Asserts role, scope PLACED, partner id and instruction types from `/me/session` and the PRT-01 list |
| AccessEvidenceAsserter | Service | Asserts the AC-SIGN and AC-DENY entries, their reasons and the decision record |
| RefusalAsserter | Service | Asserts the status and the message of each refusal: 401, 403 and 404 with MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-005, MSG-P4-006 and MSG-P4-008 |
| RunLock | Service | One run at a time in the harness environment |
| EvidenceReportPublisher | Service | Writes the per-run evidence report keyed by story id and business date and attaches it to the release record |
| JourneyGate | Service | Passes the run only when every owned criterion passes; fails and names the criterion, the seam and the observed value otherwise |

**Database.** None. The harness owns no schema, runs no Flyway migration and holds no table; seeds and assertions go through the contracts (DP-01, DP-15).

**Environment and test data.** SIT for the run of record and UAT for the acceptance run, with `rwb.access.partner-signin` on in both and off in PROD. The data are the synthetic seeds of the legacy story: LF-0012 with panel status ACTIVE and contract end 30 June 2027 and 5 open instructions, LF-0019 with 3 instructions, VL-0004 with 2 APPRAISE and 1 LIST instruction, partner identities P-5101, P-5102, P-5103 and P-5104, test user U-5105 holding RW-LITOFF, and instruction INS-2027-000431 placed with LF-0019. The harness environment, its seeding and the evidence format and retention are not specified in the source documents (GAP-0403; ASM-0578).

**Build steps**

1. Publish the four fakes from the OpenAPI documents of rwb-access, rwb-partner, rwb-decision and rwb-case and version them with the pack.
2. Write PartnerGatewayClient against the partner gateway test route, with a recorded token fixture for the no-second-factor case.
3. Write PartnerSeedLoader and the seed files, with the run lock and the fake or real mode per service.
4. Write SessionAsserter, AccessEvidenceAsserter and RefusalAsserter, with unit tests on fixtures for every status and message of the legacy table.
5. Write JourneyGate and EvidenceReportPublisher, and attach the report to the release record for the build under test.
6. Run the eleven `-ITG` cases in fake mode in SIT and record the first report.
7. Replace each fake with the real service as its I story lands, in the order rwb-access, rwb-partner, rwb-decision, and rerun in UAT.
8. Keep the partner route behind the feature switch, off in PROD until DL03 is approved.

**Feature switch.** `rwb.access.partner-signin`, the legacy switch of this story: on in SIT and UAT, off in PROD while DL03 is open.

**Done when.** The `-ITG` test cases of section 16 pass in SIT and UAT through the partner gateway test route with the three I stories in place and not only against the fakes; the evidence report for the run is attached to the release record with the ten owned criteria green; and the flag is off in PROD.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-008 | The firm is suspended, exited or past its contract end (new) | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. |
| MSG-P4-001 | No binding, or a bank identity on the partner route | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-005 | No second factor | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Two partner roles, or a partner and a bank role | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-P4-003 | An instruction of another firm | This case is not in your scope. |
| MSG-P4-002 | An endpoint outside the partner role's letters | You cannot {action} here. Your role does not include it. |

Thai text for each message follows DL10; proposed Thai for MSG-P4-008 is in the additions file. The harness asserts the message id and the rendered text of each row and never rewrites the text.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| PRT-01 Partner home | Loading | Waits while the firm's open instructions load |
| PRT-01 Partner home | List | Sees only the firm's instructions of the role's types, with due dates |

A refused partner sees the partner sign-in page with MSG-P4-008 or MSG-P4-001 and no data.

The harness builds no screen: it drives the PRT-01 states through `GET /api/recovery/partner/v1/partner/instructions` and asserts the Loading state on the first call of a run and the List state with the 5 instructions of LF-0012 and none of LF-0019. The partner sign-in page and the PRT-02 to PRT-06 work screens belong to the app stories and to Epic 4 to Epic 6; the evidence format and retention are not specified in the source documents (GAP-0403; ASM-0578).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-01-ITG | AC1, BR1, BR3 | Integration | Synthetic firms LF-0012 and LF-0019 with 5 and 3 instructions |
| TC-E2-019-02-ITG | AC2, BR4 | Integration | Valuer VL-0004 with APPRAISE and LIST instructions |
| TC-E2-019-03-ITG | AC3, BR5 | Integration | Firm moved to EXITED during an open session |
| TC-E2-019-04-ITG | AC4, BR2 | Integration | Partner identity with no binding |
| TC-E2-019-05-ITG | AC5, BR1 | Integration | Partner token without a second factor |
| TC-E2-019-06-ITG | AC6, BR3 (run by RWB-P4-E2019-APP or RWB-S9-E2019-APP) | Integration | Instruction of another firm |
| TC-E2-019-07-ITG | AC7, BR2 | Integration | Partner identity in two partner role groups |
| TC-E2-019-08-ITG | AC8, BR6 | Integration | Partner calling GET /queues |
| TC-E2-019-09-ITG | AC9, BR1 (run by RWB-P4-E2019-APP or RWB-S9-E2019-APP) | Integration | Bank test user on the partner route |
| TC-E2-019-10-ITG | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-019-11-ITG | Principle 5 | NFR | The decision log write forced to fail during a partner sign-in |
| TC-E2-019-12-ITG | AC10, BR7, BR8 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2019-ITG-AC10) |
| TC-E2-019-13-ITG | AC12 | Integration | Partner identity P-5101 bound to LF-0012 with the resolve call failing or not answering |
| TC-E2-019-14-ITG | AC11 | Integration | The rwb.decision.DecisionRecorded.v1 event of the P-5101 sign-in delivered twice on rwb.decision-record.v1 |

The `-ITG` cases assert the same behaviour as the legacy test cases under the same base id and add the seam each one exercises across services; the legacy test cases remain the record of the app stories.

### 17. Guardrails

- No business value in code: partner roles, instruction types, the binding and the refresh interval are data.
- No personal data in logs, tests or prompts; partner identities are referenced by their directory ID, never by e-mail or name.
- No read of another module's tables: partner status comes from the S9 interface and the instruction filter is applied by the S9 repository.
- No partner route in PROD while DL03 is open.
- A partner session never holds a bank role.
- The harness holds no production data and no copied extract: it seeds synthetic firms and identities only, and the evidence report carries story ids, criterion ids, decision codes, statuses and counts, never a personal value.
- The harness never calls a service's schema and never calls a second hop: every assertion is made on a contract response or on the `rwb.decision-record.v1` record.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partner users reach the Workbench only through the external gateway, with multi-factor authentication, scoped to their own cases | Business Requirements Epic 2, section 3.4; Business Requirements Program, section 5.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR8 | TC-E2-019-01-ITG to TC-E2-019-14-ITG |

### 19. Out of scope

- The architecture change that makes the partner portal reachable from outside the bank (DL03).
- Partner work screens PRT-02 to PRT-06 and the instruction endpoints (Epic 4 to Epic 6, S9 and S6 stories).
- Partner panel management, contracts and scorecards (SCR-34 in Epic 2 for identities; Epic 6 for the full panel).
- Customers, guarantors, heirs and bidders, who do not sign in to the Workbench.
