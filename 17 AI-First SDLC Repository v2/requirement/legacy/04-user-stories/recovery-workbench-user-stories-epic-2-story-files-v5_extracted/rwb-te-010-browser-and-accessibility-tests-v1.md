<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB TE 010 Browser and accessibility tests v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB TE 010 Browser and accessibility tests v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-010 Browser and accessibility tests

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-010 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-OCC-007, REQ-WKM-001 |
| BRD section | Business Requirements Program, section 6.10 and section 6.11 |
| L3 process | All recovery processes |
| Decision | DL37 |
| Priority | Must |
| Depends on | RWB-TE-003 |
| Status | Ready for build |

## 1. Story

As a **squad member (RW-TRIBE)**, I want **browser tests and an accessibility scan on the main recovery screens, on the browsers the bank supports and in Thai and English, in every pipeline run**, so that **screens work for every user on the bank's browsers**.

## 2. Business rationale

Recovery staff work on Microsoft Edge and Google Chrome, some with screen readers or keyboard only, and in Thai or English. A screen that passes on one developer's browser can fail on the previous browser version or for a keyboard user, and that is found in UAT or by users. The browser runner tests the main screens on four browsers and scans them for WCAG 2.1 AA errors in both languages before merge. It proves the case record view (REQ-OCC-007) and my queue (REQ-WKM-001) against NFR-060, NFR-061 and NFR-059. The measure is the count of accessibility and browser defects found in UAT, with a target of zero.

## 3. Preconditions

- RWB-TE-003 is done: the front end uses the generated types and client.
- The browser test runner is in the ACE pipeline before the first SIT run (DL37).
- The runner image holds Chrome and Edge at the current and previous major versions, listed in `browsers.json` (NFR-061; DL11).
- A test deployment with the synthetic data set of RWB-E1-065 and test users per role.
- Screen labels exist in Thai and English in the message and label tables (DL10; Thai labels may show "Pending" until approved).

## 4. Flow

1. Pipeline: starts the browser stage after the front end build on each pull request, and nightly against SIT.
2. Runner: reads `browsers.json` and refuses to start when a listed browser is missing.
3. Runner: signs in the test user of each role in the screen list.
4. Runner: opens each main screen (SCR-02, SCR-03, SCR-04, SCR-05, SCR-07, SCR-09) in each listed state and runs its functional test on each browser.
5. Runner: runs the accessibility scan with the WCAG 2.1 A and AA rule tags on each screen and state, in Thai and in English.
6. Runner: runs the keyboard test: every primary action is reachable and usable by keyboard with a visible focus.
7. Runner: compares each violation with the exception list; an entry past its expiry date does not excuse the violation.
8. Runner: retries a failed functional test once and lists a test that passes only on retry as flaky.
9. Pipeline: fails the stage on any violation, functional failure or missing browser, and attaches the report.

## 5. Exception paths

None.

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the generated client of RWB-TE-003 and the runner of DL37 |
| Negotiable | Browser versions, screens and exceptions are configuration files |
| Valuable | Users on every bank browser and with assistive technology can use the screens |
| Estimable | One test suite, one scan helper, two configuration files |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below uses one fixture screen or one browser setting |

## 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every main screen meets WCAG 2.1 level AA; any violation tagged WCAG 2.1 A or AA fails | NFR-060 |
| BR2 | Screens work on the current and previous major versions of Microsoft Edge and Google Chrome | NFR-061 |
| BR3 | Every screen is checked in Thai and in English | NFR-059; DL10 |
| BR4 | A violation is excused only by an exception list entry with an owner and an expiry date not yet passed | Principle 1 applied to test configuration |
| BR5 | A missing browser is a failure, never a skip | DL37 |
| BR6 | A failed functional test is retried once; a pass on retry is listed as flaky | Engineering practice |
| BR7 | A role without the right sees the refusal and no control for the action | CTL-09; MSG-P4-002 |

## 9. State transitions

None. This story does not change a case status. It changes the state of the browser stage: running, passed or failed.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the stage, add screens to the list, request an exception entry |
| TechX tech leads (code owners, RWB-TE-002) | Approve changes to the screen list, the browser list and the exception list |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-PLATADM and RW-PHONECOL | Open the screens with their own rights |
| No approval level from the delegation of authority applies | The story takes no business decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-030 | lov_value | label_en | Read |
| DF-REF-031 | lov_value | label_th | Read |

The runner reads the synthetic data through the screens only. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

| Item | Value |
|---|---|
| Trigger | The browser stage on each pull request that changes the front end; nightly against SIT |
| Input | `browsers.json`, `screens.json` (screen ID, route, states, roles, primary actions), `a11y-exceptions.json` (screen, rule, owner, expiry, reason) |
| Output | Report per screen, state, language and browser: functional result, violations with rule and element, keyboard result, flaky list |
| Scan rules | WCAG 2.1 A and AA rule tags of the scan engine |
| Idempotency | The same commit and configuration give the same result, apart from tests listed as flaky |
| Restart | Rerun the stage; it holds no state |

This is a pipeline stage, not a scheduled Workbench job.

## 13. Solution plan

**Package.** Folder `ace-web/e2e/recovery` in TypeScript; configuration in `ace-web/e2e/recovery/config`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| screens.json | Rule table | Screens, states, roles and primary actions under test |
| browsers.json | Rule table | Browser names and versions (BR2) |
| a11y-exceptions.json | Rule table | Excused violations with owner and expiry (BR4) |
| BrowserGuard | Service | Fails the stage when a listed browser is missing (BR5) |
| ScreenSuite | Service | Functional tests per screen and state, on each browser |
| AccessibilityScan | Service | Scan per screen, state and language with the WCAG 2.1 A and AA tags (BR1, BR3) |
| KeyboardCheck | Service | Tab order and focus on each primary action |
| ReportWriter | Service | The stage report and the flaky list (BR6) |

**Database.** None.

**Configuration and reference data.** The three configuration files, owned by the TechX tech leads; browser versions as listed in the runner image (DL37, DL11); labels in Thai and English from the label tables (DL10).

**Build steps**

1. Write BrowserGuard and browsers.json; prove a missing version fails (AC5).
2. Write the functional tests for the 6 screens from screens.json on the 4 browsers (AC3).
3. Write AccessibilityScan for both languages and the missing label check (AC1, AC2, AC4, AC7).
4. Write the exception list handling with expiry (AC6).
5. Write KeyboardCheck for the primary actions (AC8).
6. Add the single retry and the flaky list (AC9).
7. Add the refusal test for RW-PHONECOL on SCR-05 (access test) and add the stage to the pipeline.

**Feature flag.** None. The tests run in the pipeline and do not ship in the service.

**Done when.** The tests in section 16 pass and the pipeline shows the browser stage on every front end pull request.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | A violation | accessibility violation: {screen} {state} {language} {rule} {element} |
| Report | A missing browser | browser not available: {browser} {version} |
| Report | An expired exception | exception expired: {screen} {rule} since {date} |
| Report | A raw label key | missing label: {screen} {key} |
| Report | A keyboard failure | keyboard access: {screen} action {action} |
| MSG-P4-002 | The refusal shown to a role without the right | You cannot {action} here. Your role does not include it. |

Report text is for developers and is not part of the message standard.

## 15. Screens and states

Screens under test: SCR-02 Case list (Loading, Empty, List, Filtered), SCR-03 Case record (Loading, Read only, Editable, On hold), SCR-04 Case timeline (Loading, Filtered), SCR-05 Transfer case (Form, At cap warning, Saved), SCR-07 Team queues (Loading, List) and SCR-09 Exception queue (Loading, List). Developers read the report in the pipeline.

## 16. Test cases

None.

## 17. Guardrails

- No business value in code; screens, browsers and exceptions are configuration files.
- No personal data in logs, tests or prompts; tests use the synthetic data set and screenshots in the report show synthetic data only.
- No read of another module's tables; the runner uses the screens only.
- An exception entry always has an owner and an expiry date.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | Business Requirements Program, section 6.11 | None | All recovery processes | None | None |
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | Business Requirements Program, section 6.10 and section 6.11 | None | All recovery processes | None | None |

## 19. Out of scope

- Partner portal screens and tablets (NFR-063): the partner portal stories from RWB-E2-019.
- Thai label approval: DL10.
- Response times under load: RWB-TE-009.
- Screen design and layout: DL31.
