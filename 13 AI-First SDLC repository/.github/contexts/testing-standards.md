# Recovery Workbench — testing standards

**Purpose:** the test levels, environments, data rules, gates and evidence an agent must plan for.
**Source:** `requirement/legacy/09-testing-and-quality/recovery-workbench-test-strategy-v2-docx.md`,
`Recovery Workbench Definition of Ready and Done v3`, `Recovery Workbench Test Data Plan v2`,
`Recovery Workbench Defect Management Process v2`, `Recovery Workbench Non Functional Test Plan v2`,
`Recovery Workbench Regression Suite v5`, `Recovery Workbench Requirements Traceability Matrix v4`.

## 1. Test levels

| Level | What it covers | Who | Where | When | Exit |
|---|---|---|---|---|---|
| Unit | Every service method and rule evaluation | Developer | DEV and pipeline | Every commit | 80% line coverage on new code |
| Rule table | Each rule row against its test case | Developer with analyst | Pipeline | Every commit and every rule version | Every row passes |
| Integration | Modules with a real PostgreSQL database | Developer | Pipeline | Every pull request | All pass |
| API contract | Requests and responses against the OpenAPI file | Developer | Pipeline | Every pull request | All pass |
| System | Stories end to end against SCB test systems | QA engineer | SIT | Rolling, then SIT week | Every test case for the release passes; no open severity 1 or 2 |
| Regression | The regression suite | QA engineer | SIT | Each release | All pass |
| Non-functional | Performance, resilience, security | QA with SCB IT | SIT | Before each release | Targets in the NFR specification |
| Accessibility | Automated scan and keyboard checks | QA engineer | SIT | Each screen | No level A or AA failure |
| User acceptance | Business scripts | Business testers | UAT | UAT week | Scripts signed by the business lead |

## 2. Environments and data

| Environment | Data | Use |
|---|---|---|
| DEV | Synthetic only | Developer and rule tests |
| SIT | Masked copies from the PII service | System, regression, non-functional |
| UAT | Masked copies | Business acceptance |
| PROD | Production | No test data; no production data in a prompt, test or log |

Rules:

- No production data below production.
- No personal data in a prompt, fixture, test log or screenshot.
- The synthetic data generator is the source of DEV data.
- The test data plan sets the data each test needs; a test that needs data the plan does not cover is
  a gap, not an excuse to use production data.

## 3. Gates

| Gate | Entry | Exit |
|---|---|---|
| SIT | Release tag built; stories done in DEV; test data loaded | Every test case passes; no open severity 1 or 2; severity 3 with an agreed fix date |
| UAT | SIT exit met; scripts walked through with the testers | Scripts signed by the business lead; open defects accepted or behind a flag |
| Release | SIT and UAT exits | Go decision by the release owner |
| Quality and security | Spec, plan, code and test evidence complete | Compliance Reviewer findings resolved or explicitly accepted; independent hard gates pass |

## 4. Coverage and evidence

- 80% line coverage on new code for every supported metric. Coverage is measured, not claimed.
- Every acceptance criterion has at least one test case. Every rule row has a test case.
- Every test case names its story and acceptance criterion or its rule ID.
- Every test result is stored under `output/<RUN_ID>/`:
  - `api-tests/attempt-<n>/`
  - `functional-tests/attempt-<n>/`
  - `implement/` for unit-test evidence
  - `review/` for Compliance Reviewer findings
- Attempt directories are never overwritten; a re-run creates `attempt-<n+1>/`.
- A `NOT_APPLICABLE` result is allowed only with evidence that the surface is out of scope.

## 5. Traceability

The required chain is:

```text
CTX -> BRD -> FR/NFR -> US -> SPEC -> TASK -> CODE -> APT/FT/TEST -> REVIEW -> DOC
```

The matrix is `requirement/Traceability_Matrix.md`. Flag:

- requirements without specs;
- specs without tasks;
- tasks without code;
- APIs in scope without an `APT-*` result or explicit blocker;
- UI behaviour in scope without an `FT-*` result or explicit blocker;
- requirements without tests;
- compliance requirements without review evidence.

## 6. Defects

- Severity 1: production or SIT stop, data loss, security or personal data exposure. Fix immediately;
  no release.
- Severity 2: a core journey blocked or a major requirement unmet. Fix before release; no open
  severity 2 at SIT exit.
- Severity 3: a workaround exists. Fix by the agreed date or carry with acceptance.
- Severity 4: cosmetic. Carry with acceptance.
- Every defect has an owner, a severity, a fix, a retest and a link to the story or rule.
- A defect traced to AI-written code is tagged and the standards file is updated before the fix is
  merged.

## 7. Non-functional testing

| Area | What is tested | Pass mark |
|---|---|---|
| Performance | Busiest-hour load; screen, search, rule and agent response | NFR-008..012 |
| Volume | 23,600 open cases at go-live, 26,500 at end 2027; 5.8 million documents by 2031 | NFR-001, NFR-069 |
| Resilience | Failover, restore, system-of-record outage, agent outage | NFR-020..027 |
| Security | Penetration test before the partner portal opens; access tests per role | Test Strategy §5; CTL-09..11 |
| Accessibility | Automated scan and keyboard checks on each screen | WCAG 2.2 AA; NFR-009 |
| Audit | Re-run a sample of decisions from the log; hash-chain check | NFR-033..035 |

## 8. Definition of ready and done

A story is ready when:

- every section of the story file is complete;
- each acceptance criterion can be tested;
- every rule ID, field and message ID exists in its source document;
- the design evidence is available for a UI story;
- the dependencies are done or the story is behind a flag.

A story is done when:

- the code is merged and the pipeline checks pass;
- the tests are written from the acceptance criteria and pass;
- the unit coverage is at least 80% on new code;
- the decision log entry is written;
- the access check and PDPA masking are in place;
- the story is demonstrated and accepted at the gate;
- the traceability matrix is updated.

Source: Definition of Ready and Done v3; AI Assisted Development Approach §7; toolkit
`implementation-execution-gates.md`.

## 9. Test agents in this repository

| Agent | Scope | Output |
|---|---|---|
| API Tester | Every API in `spec.md` when `API In Scope: YES` | `output/<RUN_ID>/api-tests/attempt-<n>/` |
| Functional Automation Test | Every UI behaviour in `spec.md` when `UI In Scope: YES` | `output/<RUN_ID>/functional-tests/attempt-<n>/` |
| QA Test Case Generator | Manual test cases to Jira | `output/test-cases/<story-key>/` |
| Compliance Reviewer | Spec, plan and code gates | `REVIEW-*` findings |

The API and functional testers must not fabricate results. A `NOT_APPLICABLE` result needs evidence.
A blocked test is reported as blocked, not passed.
