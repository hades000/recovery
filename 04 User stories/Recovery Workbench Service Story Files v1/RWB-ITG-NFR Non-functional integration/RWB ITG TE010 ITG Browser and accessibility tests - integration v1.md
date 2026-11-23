# RWB-ITG-TE010-ITG Browser and accessibility tests

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE010-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-ITG-NFR |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-TE-010 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP07, DP19 |
| Parallel lane | L-ITG-NFR |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-030, FR-PLT-031, FR-PLT-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: moved from RWB-TE-010 into the RWB-ITG-NFR epic as the integration harness story for the browser and accessibility stage. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **browser tests and an accessibility scan on the main recovery screens, on the browsers the bank supports and in Thai and English, in every pipeline run**, so that **screens work for every user on the bank's browsers**.

### 2. Business rationale

Recovery staff work on Microsoft Edge and Google Chrome, some with screen readers or keyboard only, and in Thai or English. A screen that passes on one developer's browser can fail on the previous browser version or for a keyboard user, and that is found in UAT or by users. The browser runner tests the six main screens on four browser configurations and scans them for WCAG 2.1 AA errors in both languages before merge. It proves the case record view (REQ-OCC-007) and my queue (REQ-WKM-001) against NFR-060, NFR-061 and NFR-059. The measure is the count of accessibility and browser defects found in UAT, with a target of zero.

In the target the screens are served by the gateway-bff composite route (DP-19), and labels and reference values come from the rwb-case reference-data contract (DP-07). The stage therefore tests the same route and the same label source that production uses, not a local build of the screen.

### 3. Preconditions

- RWB-TE-003 is done: the front end uses the generated types and client.
- The browser test runner sits in the ACE pipeline before the first SIT run.
- The runner image holds Chrome and Edge at the current and previous major versions, listed in `browsers.json` (NFR-061).
- A test deployment with the synthetic data set and test users per role.
- Screen labels exist in Thai and English in the label tables; Thai labels may show "Pending" until approved (DL10).
- The scan engine and its WCAG 2.1 A and AA rule tags are fixed in the scan profile.
- The gateway-bff route specification and the label source are not specified in the source documents (GAP-0331; ASM-0424; ASM-0425).

### 4. Flow

1. Pipeline: starts the browser stage after the front-end build on each pull request, and nightly against SIT.
2. Runner: reads `browsers.json` and refuses to start when a listed browser is missing.
3. Runner: signs in the test user of each role in the screen list.
4. Runner: opens each main screen (SCR-02, SCR-03, SCR-04, SCR-05, SCR-07, SCR-09) in each listed state and runs its functional test on each browser.
5. Runner: runs the accessibility scan with the WCAG 2.1 A and AA rule tags on each screen and state, in Thai and in English.
6. Runner: runs the keyboard test: every primary action is reachable and usable by keyboard with a visible focus.
7. Runner: compares each violation with the exception list; an entry past its expiry date does not excuse the violation.
8. Runner: retries a failed functional test once and lists a test that passes only on retry as flaky.
9. Pipeline: fails the stage on any violation, functional failure or missing browser, and attaches the report.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A listed browser or version is missing from the runner image | The stage fails before any test runs; the report names the browser and the version | `browser not available: {browser} {version}` | AC1 |
| X2 | A WCAG 2.1 A or AA violation on a screen and state | The stage fails; the report names the screen, the state, the language, the rule and the element | `accessibility violation: {screen} {state} {language} {rule} {element}` | AC2 |
| X3 | An exception entry past its expiry date matches the violation | The violation is not excused and the stage fails; the report names the entry's expiry date | `exception expired: {screen} {rule} since {date}` | AC3 |
| X4 | A primary action is not reachable or not usable by keyboard | The stage fails; the report names the screen and the action | `keyboard access: {screen} action {action}` | AC4 |
| X5 | A screen shows a raw label key instead of a label | The stage fails; the report names the screen and the key | `missing label: {screen} {key}` | AC7 |
| X6 | A functional test fails on the first attempt and again on the single retry | The stage fails; the report holds the two attempts | None | AC6 |
| X7 | A test user whose role does not include the action opens the screen in the state that offers it | The refusal is shown and no control for the action is rendered | MSG-P4-002 | AC5 |

The report text is for developers and is not part of the message standard; only MSG-P4-002 is a business message.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the generated client of RWB-TE-003 and the runner configuration; it reads the deployed SIT screens, so it waits for no service story of its own |
| Negotiable | Browser versions, screens, states, roles and exceptions are configuration files |
| Valuable | Users on every bank browser and with assistive technology can use the screens, and a regression is caught before merge |
| Estimable | One test suite, one scan helper, one keyboard check, one report writer and three configuration files |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion uses one fixture screen or one browser setting, and the report is the evidence |

### 7. Acceptance criteria

```gherkin
Feature: Browser and accessibility stage for the recovery screens

  Background:
    Given the browser stage runs after the front-end build on every pull request and nightly against SIT
    Given browsers.json lists the current and previous major versions of Microsoft Edge and Google Chrome
    Given screens.json lists SCR-02, SCR-03, SCR-04, SCR-05, SCR-07 and SCR-09 with their states, roles and primary actions
    Given the screens are reached through the gateway-bff composite routes

  Scenario: AC1 The functional suite passes on every listed browser and a missing browser fails the stage (new, D-RCV-60)
    Given the runner reads browsers.json
    When a listed browser or version is missing from the runner image
    Then the stage fails and the report names the browser and version
    When every listed browser is present
    Then each screen in each listed state passes its functional test on each browser

  Scenario: AC2 The WCAG 2.1 A and AA scan reports zero violations in Thai and in English (new, D-RCV-60)
    Given the accessibility scan runs with the WCAG 2.1 A and AA rule tags
    When each screen and state is scanned in Thai and in English
    Then every violation with a rule tag WCAG 2.1 A or AA fails the stage
    Then the report names the screen, the state, the language, the rule and the element

  Scenario: AC3 An exception entry excuses a violation only until its expiry date (new, D-RCV-60)
    Given an exception entry with an owner, an expiry date and a reason
    When the entry has not expired and matches the screen and the rule
    Then the violation is excused and listed in the report
    When the entry has expired
    Then the violation fails the stage and the report says "exception expired"

  Scenario: AC4 Every primary action is reachable and usable by keyboard (new, D-RCV-60)
    Given a screen and state in screens.json with its primary actions
    When the keyboard check tabs through the screen
    Then every primary action is reachable and usable with a visible focus
    Then a failure names the screen and the action

  Scenario: AC5 A role without the right sees the refusal and no control (new, D-RCV-60)
    Given a test user whose role does not include the action
    When the user opens the screen in the state that offers the action
    Then the screen shows MSG-P4-002 and no control for the action

  Scenario: AC6 A failed functional test is retried once and a pass on retry is listed as flaky (new, D-RCV-60)
    Given a functional test that fails on the first attempt
    When it passes on the single retry
    Then the stage result counts it as a pass and lists it as flaky in the report
    When it fails again
    Then the stage fails

  Scenario: AC7 A raw label key on a screen fails the stage (new, D-RCV-60)
    Given a screen rendered in Thai or in English
    When the screen shows a raw label key instead of a label
    Then the stage fails and the report names the screen and the key

  Scenario: AC8 The six main screens are covered in both languages (new, D-RCV-60)
    Given the screen list of this story
    When the stage runs
    Then SCR-02, SCR-03, SCR-04, SCR-05, SCR-07 and SCR-09 are each tested in every listed state, on every listed browser and in both languages
    Then the report holds one row per screen, state, language and browser
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every main screen meets WCAG 2.1 level AA; any violation tagged WCAG 2.1 A or AA fails | NFR-060 |
| BR2 | Screens work on the current and previous major versions of Microsoft Edge and Google Chrome | NFR-061 |
| BR3 | Every screen is checked in Thai and in English | NFR-059 |
| BR4 | A violation is excused only by an exception list entry with an owner and an expiry date not yet passed | Principle 1 applied to test configuration |
| BR5 | A missing browser is a failure, never a skip | DL37 |
| BR6 | A failed functional test is retried once; a pass on retry is listed as flaky | Engineering practice |
| BR7 | A role without the right sees the refusal MSG-P4-002 and no control for the action | CTL-09 |
| BR8 | Labels in Thai and English are read through the rwb-case reference-data contract and screens through the gateway-bff composite route | DP-07; DP-19; ASM-0424 |

### 9. State transitions

| From | To | Trigger |
|---|---|---|
| Not started | Running | The pipeline starts the browser stage |
| Running | Passed | No violation, no functional failure and no missing browser |
| Running | Failed | Any violation, any functional failure after the retry, or a missing browser |
| Failed | Running | Rerun of the same commit and the same configuration |

This story changes the state of the browser stage only. It never changes a case status: the runner holds no case and writes no service table.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the stage, add screens to the list, request an exception entry |
| TechX tech leads (code owners, RWB-TE-002) | Approve changes to the screen list, the browser list and the exception list |
| QA lead | Owns the runner configuration |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-PLATADM and RW-PHONECOL | Open the screens with their own rights |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-030 | lov_value | label_en | Read |
| DF-REF-031 | lov_value | label_th | Read |

The runner reads the synthetic data through the screens only. Labels and role codes are read through the rwb-case reference-data contract (P3, DP-07) and role codes come from rwb-access (P4). The runner owns no schema and reads no service table.

### 12. Contract

#### 12.1 REST operations provided

None. The functional suite is a pipeline stage and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | /api/recovery/case/v1/cases | P3 rwb-case | SCR-02 Case list |
| GET | /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | SCR-03 Case record |
| GET | /api/recovery/case/v1/cases/{caseId}/timeline | P3 rwb-case | SCR-04 Case timeline |
| POST | /api/recovery/case/v1/cases/{caseId}/transfer | P3 rwb-case | SCR-05 Transfer case |
| GET | /api/recovery/case/v1/queues | P3 rwb-case | SCR-07 Team queues |
| GET | /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | SCR-07 Team queues and SCR-09 Exception queue |

Every call goes through the gateway-bff composite route (DP-19). The runner provides no operation and calls no service directly.

#### 12.3 Events published

None.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None. There is no Temporal workflow or activity; the runner is a pipeline stage.

#### 12.6 Schedules

None. The pipeline schedule starts the stage (each pull request and nightly against SIT); it is not a Temporal Schedule.

#### 12.7 Tables owned

None. The runner owns no table and reads no service table; labels and role codes arrive over the rwb-case reference-data contract.

#### 12.8 Contract fakes

None. The runner tests the deployed SIT screens and their real contracts; contract fakes are not used at this level.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6, through gateway-bff | One hop, 2 s timeout (ADR-020) |
| Kafka | None | None | The stage publishes and consumes no event |
| Temporal | None | None | No workflow, activity or schedule |
| File | None | None | The report is a pipeline artefact |

### 13. Solution plan

**Package.** Deliverable folder `ace-web/e2e/recovery` in TypeScript, with the configuration in `ace-web/e2e/recovery/config`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| screens.json | Rule table | Screens, states, roles and primary actions |
| browsers.json | Rule table | Browser names and versions |
| a11y-exceptions.json | Rule table | Excused violations with owner and expiry |
| BrowserGuard | Service | Fails the stage when a listed browser is missing |
| ScreenSuite | Service | Functional tests per screen and state on each browser |
| AccessibilityScan | Service | Scan per screen, state and language with the WCAG 2.1 A and AA tags |
| KeyboardCheck | Service | Tab order and focus on each primary action |
| ReportWriter | Service | Stage report and flaky list |

**Database.** None.

**Configuration and reference data**

- The three configuration files: `screens.json`, `browsers.json` and `a11y-exceptions.json`, owned by the TechX tech leads.
- Browser versions as installed in the runner image.
- Labels in Thai and English through the rwb-case reference-data contract (DP-07).
- Screen routes from the gateway-bff route list (DP-19).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The story carries no H, C, I or X dependency because the runner runs against the deployed SIT screens and published contracts, and the DP-07 and DP-19 build dependencies stay with the screens and the platform edge.

**Build steps**

1. BrowserGuard and `browsers.json`, with a missing version failing the stage.
2. Functional tests for the six screens from `screens.json` on the four browser configurations.
3. AccessibilityScan for both languages, including the missing-label check.
4. Exception list handling with expiry.
5. KeyboardCheck for the primary actions.
6. The single retry and the flaky list.
7. The refusal test for RW-PHONECOL on SCR-05, and the stage added to the pipeline.

**Done when.** The tests in section 16 pass and the pipeline shows the browser stage on every front-end pull request.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | A violation | accessibility violation: {screen} {state} {language} {rule} {element} |
| Report | A missing browser | browser not available: {browser} {version} |
| Report | An expired exception | exception expired: {screen} {rule} since {date} |
| Report | A raw label key | missing label: {screen} {key} |
| Report | A keyboard failure | keyboard access: {screen} action {action} |
| MSG-P4-002 | The refusal shown to a role without the right | You cannot {action} here. Your role does not include it. |

Report text is for developers and is not part of the message standard. Only MSG-P4-002 is a business message, and it is unchanged from the legacy set.

### 15. Screens and states

| Screen | States |
|---|---|
| SCR-02 Case list | Loading, Empty, List, Filtered |
| SCR-03 Case record | Loading, Read only, Editable, On hold |
| SCR-04 Case timeline | Loading, Filtered |
| SCR-05 Transfer case | Form, At cap warning, Saved |
| SCR-07 Team queues | Loading, List |
| SCR-09 Exception queue | Loading, List |

Each screen is reached through the gateway-bff composite route; the route specification is not specified in the source documents (GAP-0331; ASM-0425). Developers read the report in the pipeline.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-ITG-TE010-ITG-01 | AC1, BR2, BR5 | Integration | Four browser configurations present pass; one missing fails |
| TC-ITG-TE010-ITG-02 | AC2, BR1, BR3 | NFR | Fixture screen with one WCAG 2.1 AA violation fails in Thai and in English |
| TC-ITG-TE010-ITG-03 | AC3, BR4 | Component | Exception entry valid excuses; expired fails |
| TC-ITG-TE010-ITG-04 | AC4 | Component | Fixture screen with one primary action reachable only by mouse fails |
| TC-ITG-TE010-ITG-05 | AC5, BR7 | Component | RW-PHONECOL on SCR-05 shows MSG-P4-002 and no control |
| TC-ITG-TE010-ITG-06 | AC6, BR6 | Component | A test failing once then passing is listed flaky; failing twice fails the stage |
| TC-ITG-TE010-ITG-07 | AC7 | Component | A screen showing a raw label key fails the stage |
| TC-ITG-TE010-ITG-08 | AC8, BR1, BR3 | End to end | Six screens, their states, four browser configurations and two languages all reported |

### 17. Guardrails

- No business value in code: screens, browsers and exceptions are configuration files.
- No personal data in logs, tests or prompts: the synthetic data set only, and screenshots show synthetic data only.
- No read of another service's tables: the runner uses the screens only.
- An exception entry always has an owner and an expiry date.
- A missing browser is never skipped and a missing label is never tolerated.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | GET case operations and SCR-03 | TC-ITG-TE010-ITG-01, TC-ITG-TE010-ITG-02 |
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | GET /queues and /queues/{queueId}/cases and SCR-07 | TC-ITG-TE010-ITG-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | gateway-bff one hop for every screen route | TC-ITG-TE010-ITG-01 |

### 19. Out of scope

- Partner portal screens and tablets (NFR-063): the partner portal stories.
- Thai label approval.
- Response times under load (RWB-TE-009).
- Screen design and layout.
- The gateway-bff route specification (platform edge story).
