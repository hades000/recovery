# RWB-PLT-NF05-OPS Quality gates baseline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF05-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | NF |
| Release | None (new story) |
| Legacy key | NF-05 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-TPL-E |
| Ready to start | Day 1 |
| Size | Not sized; the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | Not specified in the source documents (DOR-RWB-PLT-NF05-OPS-21) |
| Contract version | Not specified in the source documents (DOR-RWB-PLT-NF05-OPS-23); contract tests use OpenAPI 3.1 and AsyncAPI 3.0 (BR3) |
| Integration dependencies | None |
| Team handles and ruleset | One handle @scb-ace/<team-handle> per owning team (not specified in the source documents; GAP-1432). One ruleset per repository on the protected branch; its name is not specified in the source documents (GAP-1432). Required checks in order: the quality gates of RWB-PLT-NF05-OPS, then the module boundary test of RWB-PLT-TE001-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: platform story for legacy NF-05 (moved, no impact), the quality-gates baseline — one gate set, one promotion rule, one time-boxed exception rule and one reporting surface, established once in the service template and the golden pipeline in wave 0 and inherited unchanged by the 19 services and the platform epics. The legacy NF-05 story text is not in the source set (title only), so the baseline is derived from Arch v5 slides 11, 20, 29, 35, 38 and 47 and consumes the secret, personal-data and dependency gate of RWB-PLT-NF04-OPS rather than restating it. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 5 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer of the platform**, I want **one quality-gate set — unit and component tests with a coverage floor, contract tests from the published OpenAPI, AsyncAPI and activity contracts, the module boundary test, the migration lint and drift gate, the secret and personal-data scan, the approved-dependency and licence check, the image and image-history scan, and static analysis — defined once in the service template and the golden pipeline in wave 0, with one promotion rule, one time-boxed exception rule and one reporting surface for the platform administrator**, so that **a release is published only when every gate has passed for every changed service, the build record keeps the gate-set version and every result, and no service can quietly weaken, skip or re-implement a gate**.

The legacy story text for NF-05 is not in the source set: the NF-05 row of the legacy index holds the title "Quality gates baseline" and no sections, no acceptance criteria, no test cases and no requirements (`_work/msr/plan/legacy_index.json`, NF-05 entry, all other fields empty). The baseline in this story is therefore derived from the architecture slides named in section 2 and section 18, it inherits no legacy criterion, and it is not copied from a legacy narrative. The legacy title is kept word for word as the story title.

### 2. Business rationale

Arch v5 slide 11 makes the contract the first artefact of every service: "Every service publishes its contracts (OpenAPI, AsyncAPI, activity jar) before code; contract tests run in every build." The same slide fixes the typed activity and workflow interface as a contract jar and the AsyncAPI 3.0 topic contract with a backward-compatible schema registry, so a contract test has something exact to check and a build has a reason to run it. Slide 20 gives every service the same block from the service template and the shared libraries — its own schema with outbox and inbox, its own task queue, `contract tests` among the template's parts and `/health` and `/metrics` for the platform — so a gate set that lives in the template reaches every service without a per-service decision. Slide 29 states the data rule and the way it is kept: one schema and one login per service, no cross-schema join or key, "Checked in every build — boundary test fails on a cross-schema reference". Slide 35 places the pipeline itself under a standard: zero trust per NIST SP 800-204, with 800-204C and 800-204D informing the DevSecOps pipeline and the supply-chain controls. Slide 38 makes the golden pipeline one of the wave-0 platform pieces built once, next to the service template and the one Helm chart. Slide 47 records why that matters: the risk "Schema rules broken over time" has "Hidden coupling between services" as its impact and "Database grants per schema; boundary test in every build; review of every new grant" as its mitigation, owned by Architecture.

Without this baseline each of those statements is a good intention held by a different person. There are 19 services, 4 delivery waves, 4 environments and two teams' worth of habits. A coverage floor that each service team picks for itself is 19 floors and no floor; a contract test that is skipped on a Friday because the contract repository was slow is a contract test that does not exist; a boundary test that runs in one service's build and not in another's lets the coupling back in through the service that does not run it. A developer who is short of time removes a failing gate, raises a threshold in a local file, marks a test ignored, or publishes an image built from a branch where the gates were not reached. None of those events fails a release unless the gate set is the same for everyone, is versioned, and is checked for having been changed.

The remedy is one gate set, stated once and inherited, plus the three rules that make it hold: a promotion rule (a release is published only when every gate passed for every changed service, and the build record keeps the gate-set version and the results), an exception rule (time-boxed, owned by a role, recorded, expiring into a failure) and one reporting surface the platform administrator reads. The gate set is a Day-1 platform enabler with no build dependency. Every service story from wave 0 onwards consumes it and none of them may establish a gate of its own. NF-05 carries no legacy build impact, which is why it is Moved (no impact): no built code changes, and the gate set is in force before the first new service exists.

This story consumes four sibling baselines and duplicates none of them: the repository and pipeline baseline of RWB-PLT-NF01-OPS supplies the stages and the build record the gate set writes to; the service pipeline template and Helm chart of RWB-PLT-N004-OPS supply the template a new service is created from; the secret, configuration and pipeline-gate rules of RWB-PLT-NF04-OPS supply the secret scan, the personal-data pattern check, the approved-dependency entry point and the image scan that NFR-052 and NFR-054 require; and the migration lint and drift gate of RWB-PLT-E1044-OPS supplies the migration check (DP-15).

### 3. Preconditions

- The repository and pipeline baseline of RWB-PLT-NF01-OPS exists: one repository per service, one pipeline per repository, the stages in a fixed order, and the build record that a gate can join and write to.
- The service pipeline template and the Helm chart of RWB-PLT-N004-OPS exist, because the inheritance rule of this story is a rule about that template and that chart, and because the promotion rule acts after the deploy stage of that pipeline.
- The secret, configuration and gate rules of RWB-PLT-NF04-OPS exist: the secret scan, the personal-data pattern check, the approved-dependency entry point and the image and image-history scan are its rules, and this story places them in the gate set as gates and adds no second scanner of the same kind (NFR-052, NFR-054).
- The migration lint and drift gate of RWB-PLT-E1044-OPS exists as the migration check of the pipeline, because the gate set runs it and does not write it (DP-15; Arch v5 slide 29).
- The module boundary test of the delta story RWB-PLT-TE001-APP-2 and the contract tests of the delta story RWB-PLT-TE003-APP-2 exist as runnable test targets, because the gate runs them and does not write them (Arch v5 slides 11 and 29).
- Every service publishes its OpenAPI 3.1 document, its AsyncAPI 3.0 document and its typed activity contract jar before code, so that the contract gate has a published contract to check against and not a copy of the code (Arch v5 slide 11).
- The message catalogue exists, so that the one runtime alert this baseline raises carries an existing message ID and invents none.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The coverage floor, the duplication limit and the severity cut-off of static analysis, the tool products behind each gate, the length of the exception box, the expiry behaviour of an exception and the name and form of the reporting surface are Not specified in the source documents (GAP-1428; ASM-2507).

### 4. Flow

1. Publish the gate set as code in the platform repository of RWB-PLT-NF01-OPS: one gate definition per gate, one gate-set version, one owner role, and a change to it only through a reviewed change that produces the next version.
2. Place the eight gates in the golden pipeline at the same points for every service of the 19-service list and for the platform epics: unit and component tests with a coverage floor; contract tests from the published contracts; the module boundary test; the migration lint and drift gate; the secret and personal-data scan; the approved-dependency and licence check; the image and image-history scan; static analysis. A gate is invoked by the gate set and not by a pipeline parameter, so a service cannot skip one by setting a variable.
3. Fix the promotion rule: a release is published only when every gate passed for every changed service of that release; a gate that did not run is a failure and never a pass; the build record keeps the gate-set version, the commit, the image digest and one result per gate for that service.
4. Consume, and do not duplicate, the four sibling baselines: the stages and the build record of RWB-PLT-NF01-OPS, the template and the chart of RWB-PLT-N004-OPS, the secret, personal-data and dependency rules of RWB-PLT-NF04-OPS, and the migration lint and drift gate of RWB-PLT-E1044-OPS.
5. Fix the exception rule: an exception names the gate, the service, the commit or image digest, the owner role, the reason, the expiry date and the approver role; it is recorded in the exception register as a reviewed change; it is time-boxed; it expires into a failure without a further action; and a gate that the gate set marks non-waivable cannot be excepted at all.
6. Provide the reporting surface: one release report per release, one row per changed service and gate, with the state, the gate-set version, the build record reference and the exception in force; the platform administrator and the release manager read it, and no one writes a result into it by hand.
7. Prove the gate set in a clone of the template repository: one planted change per gate, each blocked and named by its gate, the file and the rule; a gate removed from the set, a gate disabled in a local file, and a per-service override are each refused by the inheritance check.
8. Prove the promotion rule, the exception rule and the reporting surface in DEV and then in SIT, publish the gate set and the operating note, and hand it to the service teams, which inherit it and add nothing to it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A gate fails on a changed service | The release is not published; the finding names the gate, the file and the rule and never the value it found; the other services of the release keep their own results | None (release error with an exit code and a job log line) | AC2, AC3 |
| X2 | A gate did not run, was skipped, or reported no result | Treated as a failure; the release is not published and the gate is named as not run | None (release error with an exit code and a job log line) | AC3 |
| X3 | A service edits, removes or overrides a gate locally | The inheritance check fails the change, names the service and the gate, and the release is not published | None (release error with an exit code and a job log line) | AC1, AC5 |
| X4 | A gate result is missing from the build record | The promotion rule refuses the release, because a release is published only on a complete record | None (release error with an exit code and a job log line) | AC3 |
| X5 | An exception is requested for a failing gate | The exception is recorded with its gate, service, commit or image digest, owner role, reason, expiry date and approver role; the release may be published only inside the box and only for a gate that is waivable | None | AC4 |
| X6 | An exception reaches its expiry date | The exception is expired by the pipeline itself and the gate returns to a failure on the next release; no renewal happens without a new recorded exception | None (release error with an exit code and a job log line) | AC4 |
| X7 | An exception has no owner role, no expiry date or no approver role | The exception register refuses the record and the gate stays a failure | MSG-P4-002 | AC4 |
| X8 | A gate job or the gate set fails, or runs past its threshold | The release is not published, the failure is alerted to the platform owner role through the observability baseline, and the gate is recorded as failed and not as passed | MSG-P2-004 | AC2, AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 19-service list, the four sibling baselines, the published contracts and the message catalogue only; the service stories consume the gate set and do not change it |
| Negotiable | The thresholds, the tool products, the exception box length and the reporting surface are agreed with the solution architect, the security architect and the release manager; the eight gates, the promotion rule, the time-boxed exception and the fail-closed behaviour are fixed by Arch v5 slides 11, 20, 29, 35, 38 and 47 and by NFR-052 and NFR-054 |
| Valuable | Gives every service and platform story from wave 0 onwards one gate set that cannot be weakened locally, and makes the contract test, the boundary test and the security gate enforce themselves instead of depending on a team's habit |
| Estimable | One gate set with eight gate definitions, one promotion rule, one exception register, one reporting view and one inheritance check; five acceptance criteria and five test cases |
| Small | Fits one sprint with the gate set, the promotion rule, the exception rule, the reporting view and the proof; the gate implementations and the tests the gates run stay with their own stories |
| Testable | Every criterion is tested in a clone of the template with one planted change per gate, with a local edit of the gate set, with a release of two changed services, and with an exception that is recorded, used and expired |

### 7. Acceptance criteria

```gherkin
Feature: Quality gates baseline inherited by the 19 services and the platform epics

  Background:
    Given the repository and pipeline baseline of RWB-PLT-NF01-OPS with its stages and its build record
    Given the service pipeline template and the Helm chart of RWB-PLT-N004-OPS
    Given the secret, personal-data and dependency gate rules of RWB-PLT-NF04-OPS and the migration lint and drift gate of RWB-PLT-E1044-OPS
    Given every service publishes its OpenAPI 3.1, AsyncAPI 3.0 and activity contracts before code

  Scenario: AC1 The gate set is defined once, in the service template and the golden pipeline, and covers the eight gates at one version (new, D-RCV-60)
    Given the gate set of the platform repository, with one gate-set version
    When the gate set is inspected
    Then it holds exactly these eight gates: unit and component tests with a coverage floor, contract tests from the published contracts, the module boundary test, the migration lint and drift gate, the secret and personal-data scan, the approved-dependency and licence check, the image and image-history scan, and static analysis
    And each gate is invoked by the gate set and not by a pipeline parameter
    And a service of the 19-service list and a platform epic resolve to the same gate set and the same version
    And the gate set records its version and each result in the build record
    When a gate is removed from the set, or disabled in a local file, or replaced by a per-service override
    Then the inheritance check refuses the change and names the service and the gate

  Scenario: AC2 Each gate blocks a planted change and names the gate, the file and the rule (new, D-RCV-60)
    Given a clone of the template repository
    When a unit or component test below the coverage floor is planted
    Then the coverage gate blocks the change
    When a client is changed against the published OpenAPI, AsyncAPI or activity contract
    Then the contract gate blocks the change and names the contract and the element
    When a cross-schema reference or a join to another service's schema is planted
    Then the boundary gate fails on it, as Arch v5 slide 29 requires in every build
    When a migration that fails the lint, or that the drift check does not reproduce, is planted
    Then the migration gate blocks the change
    When a literal secret or a personal-data field is planted
    Then the secret and personal-data gate blocks the change
    When a dependency that is not approved, or a licence outside the policy, is added
    Then the dependency and licence gate blocks the change and names the dependency
    When an image with a secret or a personal-data pattern in its history is built
    Then the image and image-history gate stops its publication
    When a change carries a finding above the severity cut-off of static analysis
    Then the static-analysis gate blocks the change
    And every finding names the gate, the file, the line and the rule and never repeats the value it found

  Scenario: AC3 A release is published only when every gate passed for every changed service, and the build record keeps the gate-set version and the results (new, D-RCV-60)
    Given a release that changes two services
    When one gate of one service fails, or a gate did not run, or a gate result is missing from the build record
    Then the release is not published and the cause is named per service and per gate
    When every gate passes for both services
    Then the release is published
    And the build record of each service keeps the gate-set version, the commit, the image digest and one result per gate
    And the platform administrator reads the result of each service and each gate, and the gate-set version, on the reporting surface of that release
    And no result on the reporting surface is written by hand

  Scenario: AC4 An exception is time-boxed, owned by a role, recorded, and expires into a failure (new, D-RCV-60)
    Given a gate that is waivable in the gate set
    When an exception is requested for a failing gate
    Then the record names the gate, the service, the commit or image digest, the owner role, the reason, the expiry date and the approver role
    And the release is published inside the box and the exception is shown on the reporting surface
    When the expiry date is reached
    Then the exception is expired by the pipeline itself and the gate returns to a failure
    And no renewal happens without a new recorded exception
    When an exception has no owner role, no expiry date or no approver role
    Then the register refuses the record, names the missing field, and the gate result is a failure
    When an exception is requested for a gate the gate set marks non-waivable
    Then the request is refused and the gate result stays a failure

  Scenario: AC5 A new service created from the template inherits the gate set with no local edit (new, D-RCV-60)
    Given a new repository created from the service template of RWB-PLT-N004-OPS
    When its first build runs with no gate change in the new repository
    Then the same eight gates run at the same gate-set version as every other service
    And the build record of the new service carries that gate-set version and one result per gate
    When the new repository edits a gate, adds a gate, or suppresses a finding of a gate
    Then the inheritance check fails the build and names the gate and the local change
    And the service is not released until the local change is removed

  Scenario: AC6 Every rule of section 8 is enforced by a criterion, a guardrail or a test, and no rule is left without one (new, D-RCV-60)
    Given the business rules BR1 to BR11 of section 8
    When the gate set, a gate that errors or times out, a non-waivable gate, a sibling baseline, a gate finding and a log are checked against those rules
    Then the gate set holds exactly the eight gates of BR2 at one version for every service and platform epic (BR1, BR2)
    And contract tests run in every build against OpenAPI 3.1, AsyncAPI 3.0 and the activity contract jar (BR3)
    And the module boundary test fails a cross-schema reference in every build (BR4)
    And a release with a gate that did not run or left no result is not published (BR5)
    And the build record keeps the gate-set version, the commit, the image digest and one result per gate (BR6)
    And an exception expires into a failure and names its gate, service, commit or image digest and approver role (BR7)
    And a gate on the non-waivable list is not weakened by an exception (BR8)
    And a gate that errors, times out or cannot reach its tool fails the release and is alerted (BR9)
    And no second scanner exists outside the rules of RWB-PLT-NF04-OPS, RWB-PLT-NF01-OPS, RWB-PLT-N004-OPS and RWB-PLT-E1044-OPS (BR10)
    And no business value and no personal data appears in the gate configuration, a test fixture, a gate finding or a log (BR11)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One gate set, defined once in the service template and the golden pipeline and versioned as a whole; a service of the 19-service list and a platform epic run the same gates at the same version and hold no gate of their own | Arch v5 slides 20 and 38; this story |
| BR2 | The gate set is exactly eight gates: unit and component tests with a coverage floor, contract tests from the published OpenAPI, AsyncAPI and activity contracts, the module boundary test, the migration lint and drift gate, the secret and personal-data scan, the approved-dependency and licence check, the image and image-history scan, and static analysis | Arch v5 slides 11, 29 and 35; NFR-052; NFR-054 |
| BR3 | Contract tests run in every build against the contracts a service publishes before code: OpenAPI 3.1, AsyncAPI 3.0 and the typed activity contract jar | Arch v5 slide 11 |
| BR4 | The module boundary test fails on a cross-schema reference and runs in every build, as the mitigation of the risk "Schema rules broken over time" | Arch v5 slides 29 and 47 |
| BR5 | A release is published only when every gate passed for every changed service; a gate that did not run, or whose result is missing from the build record, is a failure and never a pass | NFR-054; this story |
| BR6 | The build record of each service keeps the gate-set version, the commit, the image digest and one result per gate, and the platform administrator reads them on the reporting surface of the release | this story |
| BR7 | An exception is time-boxed, owned by a role, recorded in the exception register with its gate, service, commit or image digest, reason, expiry date and approver role, and it expires into a failure without a further action | this story |
| BR8 | A gate that the gate set marks non-waivable cannot be excepted; the secret, personal-data and unapproved-dependency gates of NFR-054 are blocking by their source and are not weakened by an exception | NFR-054 |
| BR9 | A gate fails closed: a gate that errors, times out or cannot reach its tool fails the release instead of passing it, and the failure is alerted | Arch v5 slide 35 (DevSecOps and supply chain under NIST SP 800-204C/204D) |
| BR10 | The gate set consumes the rules of its sibling baselines and writes no second scanner: the secret, personal-data and dependency rules belong to RWB-PLT-NF04-OPS, the stages and the build record to RWB-PLT-NF01-OPS, the template and the chart to RWB-PLT-N004-OPS, and the migration lint and drift gate to RWB-PLT-E1044-OPS | this story; Template and Rules §R5.5 DP-15 |
| BR11 | No business value and no personal data in the gate configuration, a test fixture, a gate finding or a log; every test value is synthetic | Template and Rules §R7.2 s17; Arch v5 slide 35 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not evaluated | The pipeline reaches the gate | The gate set invokes the gate | Running |
| Running | The gate completes | No finding, or every finding below the severity cut-off of the gate | Passed |
| Running | The gate completes with a finding | The finding is above the cut-off, or the gate errored, timed out or could not reach its tool | Failed |
| Running | The gate does not complete | The job is cancelled, skipped or produces no result | Failed (treated as not run) |
| Failed | A recorded exception is in force | The gate is waivable, the box is open and the approver role is recorded | Waived |
| Waived | The expiry date is reached | No new recorded exception exists | Expired (treated as Failed) |
| Passed, Waived or Failed | The promotion rule runs | Every gate of every changed service is Passed, or Waived inside its box | Published (when all pass) or Blocked (when any fails, expires or did not run) |
| Blocked | A fix is built | The fix is a new commit and a new image digest | Running |
| Expired | A fix is built inside or after the box | The change removes the finding | Running |

The lifecycle above is the lifecycle of a gate result and of a release, not a state of a case; no case status changes in this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns this story, the gate set, the golden pipeline wiring, the promotion rule, the exception register and the reporting view; changes them through the platform repository only, as a reviewed change that produces the next gate-set version |
| Platform administrator | Reads the release report, the gate results and the exception register for operations; opens an exception request in the register; holds no right to write a gate result and no right to bypass a gate |
| Solution architect | Owns NFR-052 and NFR-054; approves the gate set, the thresholds and the exception rule, and owns the risk "Schema rules broken over time" that the boundary gate mitigates |
| Security architect | Approves the scan rule sets, the severity cut-off of static analysis, the personal-data patterns and the licence policy of the dependency gate |
| Release manager | Reads the release report and the build record; publishes a release only on a complete passing record |
| QA lead | Owns the test levels of the gate set — unit, component, contract, integration and end to end — and the coverage floor as a value of the gate set |
| Service team | Reads the gate set and its own results; adds no gate, changes no threshold and suppresses no finding in its own repository; requests an exception through the register |
| RW-PLATADM | Reads the gate results, the gate-set version and the exception register of a release; holds no write right on the baseline |
| RW-SECADM | Reads the findings of the security gates and the exception register; writes nothing in the baseline |
| RW-AUDIT | Reads the build records and the exception register of a release; writes nothing |

The platform stories carry no service short name, schema, topic or task queue in the §R4 service table, because that table has 19 service rows and no platform row. Where a service identity would be named for this story, it is Not specified in the source documents (GAP-1428; ASM-2507); the gate set runs in the platform pipeline of RWB-PLT-NF01-OPS under the platform identity in the `rwb-recovery` namespace, and each service's gates run in that service's own pipeline.

### 11. Data

**Value classes and their source**

| Value class | Examples | Source of the value | Where the value is held | BR Field ID |
|---|---|---|---|---|
| Gate-set version | One version per reviewed change of the gate set | The gate set of the platform repository | The gate-set file, as a value, and a copy of it in the build record of each service | BR1, BR6 |
| Gate definition and rule | The eight gates of BR2, each with its rule set and its severity cut-off | Arch v5 slides 11, 29 and 35; NFR-052; NFR-054; the sibling baselines | The gate set, as code and configuration, never in a service repository | BR2 |
| Threshold | The coverage floor, the duplication limit and the severity cut-off of static analysis | Not specified in the source documents (GAP-1428; ASM-2507) | The gate set, as values of the gate-set version | BR2 |
| Gate result | Passed, Failed, Waived inside its box, Expired | The gate run | The build record of the service, one row per gate | BR5, BR6 |
| Exception record | Gate, service, commit or image digest, owner role, reason, expiry date, approver role | The exception register | The platform repository, as a reviewed change with the approval recorded | BR7 |
| Release state | Blocked or Published, with the changed services and their gate results | The promotion rule | The release report and the build records it reads | BR5 |

**Naming and values not in the source set**

| Value | Status | BR Field ID |
|---|---|---|
| Coverage floor of the unit and component gate | Not specified in the source documents (GAP-1428; ASM-2507) | BR2 |
| Duplication limit and severity cut-off of static analysis | Not specified in the source documents (GAP-1428; ASM-2507) | BR2 |
| Tool product behind each gate, and the commercial licence policy of the dependency gate | Not specified in the source documents (GAP-1428; ASM-2508) | BR2 |
| Length of the exception box, the approver role of an exception and the set of non-waivable gates beyond the blocking gates of NFR-054 | Not specified in the source documents (GAP-1428; ASM-2509) | BR7, BR8 |
| Name and form of the reporting surface for the platform administrator | Not specified in the source documents (GAP-1428; ASM-2508) | BR6 |

The baseline holds gate definitions, rules, thresholds, results references and exception records only. Each open value in the two tables above is carried as a value of the gate-set version and is published at the wave 0 exit check; closing it produces one new gate-set version and needs no code change. It holds no business value, no personal data and no secret: a business value belongs to the parameter catalog or the reference data, and a personal value belongs to the owning service, masked (Arch v5 slide 35; Template and Rules §R7.2 s17). Every test value that a planted change uses is generated for the test and is not a copy of a real record, a real credential or a real personal datum.

### 12. Contract

This story provides no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table and no schema. It is a platform baseline and a set of gates.

#### 12.1 REST operations provided

None. The gate set exposes no REST surface of its own. The platform administrator reads a release through the reporting surface of RWB-PLT-NF01-OPS, and a service team reads its own results in its own pipeline; neither reads a service of this story.

#### 12.2 REST operations consumed

None as a REST path. The gate set calls no service at run time: it runs tests, linters and scanners against the changed service's own artefacts, and the contract gate compares code with the contract documents the service publishes (OpenAPI 3.1, AsyncAPI 3.0 and the activity contract jar), which are artefacts of the owning service and not a call of this story. The paths and versions of no contract are repeated here; they belong to the contract stories that publish them.

#### 12.3 Events published

None. The gate set publishes no business event; a gate result is a build record row and a release state, and neither is a Kafka event.

#### 12.4 Events consumed

None. The gate set subscribes to no business event. It is started by the pipeline of the service, not by a message.

#### 12.5 Workflows and activities

None. A gate is a pipeline job and not a Temporal workflow or activity; the Temporal contract gates check the typed activity contract jar of a service but run no workflow.

#### 12.6 Schedules

None. The gate set runs inside the pipeline of each service and creates no Temporal Schedule; a scheduled security or licence refresh, if one is added later, belongs to RWB-PLT-NF04-OPS and to the platform pipeline.

#### 12.7 Tables owned

None. The baseline owns no table and no schema; the gate definitions live as code and configuration in the platform repository, the gate results live in the build record of RWB-PLT-NF01-OPS, and the exception register is a reviewed file in the same repository.

#### 12.8 Contract fakes

None. This story calls no contract at run time, so it needs no fake. The contract gate reads the published contract documents of the changed service; it does not stand in for an owner, and the fakes that a service's own tests use are provided by the contract stories of that service.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | The gate set provides no REST operation and calls none |
| Kafka | None | The gate set publishes no event and consumes none |
| Temporal | None | The gate set runs no workflow, no activity and no Schedule; it checks a service's typed activity contract |
| File | None as a call | The gate set reads the changed service's artefacts — its source, its contract documents, its migration files, its image and its build record — from the pipeline workspace |

None: the baseline is configuration and pipeline jobs; no REST, Kafka, Temporal or File call of its own.

### 13. Solution plan

**Artefacts.** All paths are relative to the platform repository of RWB-PLT-NF01-OPS.

| Path | Artefact | What it holds |
|---|---|---|
| `platform/pipeline/gates/gate-set.yaml` | The gate set and its version | The eight gates, the order and the pipeline point of each, the version of the whole set and the owner role |
| `platform/pipeline/gates/<gate>/` | One directory per gate | The rule set of the gate, its threshold values and the artefact types it refuses |
| `platform/pipeline/gates/inherit-check.yaml` | The inheritance check | The comparison of a service repository's gate configuration with the gate set, and the refusal of a local edit, an added gate, a removed gate or a suppressed finding |
| `platform/pipeline/promotion.yaml` | The promotion rule | The rule that a release is published only when every gate passed for every changed service, with the build-record fields it requires |
| `platform/pipeline/record/build-record.schema.json` | The build record schema | The gate-set version, the commit, the image digest and one result per gate, as the fields the promotion rule reads |
| `platform/pipeline/exceptions/register.yaml` | The exception register | One record per exception: gate, service, commit or image digest, owner role, reason, expiry date, approver role, and the non-waivable gate list |
| `platform/pipeline/report/release-report.md` | The reporting surface definition | One report per release: each changed service, each gate, its state, the gate-set version, the build record reference and the exception in force |
| `platform/pipeline/gates/README` | The operating note | How to read a finding, how to request and approve an exception, how an expiry behaves, and the escalation path |

**Pattern application.** The metadata `Patterns applied` row stays None: this story carries no legacy table, no legacy login, no legacy topic name and no legacy call, so no DP row is applied to code here. Three DP rows are nevertheless the reason three of the gates exist: DP-01 (the owner's schema and never another service's tables) is what the module boundary test enforces, DP-15 (per-service Flyway in the service's own schema) is what the migration lint and drift gate enforces, and DP-09 (outbox, inbox and CloudEvents) is what the contract gate checks on the event side through the AsyncAPI document.

**Build steps**

1. Write the gate set with its eight gate definitions, its pipeline points and its version, and give each gate its rule set and its threshold values as configuration.
2. Wire the gates into the pipeline of RWB-PLT-NF01-OPS at the same points for every service, invoked by the gate set and not by a pipeline parameter.
3. Write the promotion rule and the build-record schema: the gate-set version, the commit, the image digest and one result per gate, with a missing result treated as a failure.
4. Write the exception register and its validation: gate, service, commit or image digest, owner role, reason, expiry date, approver role, the non-waivable gate list, and the expiry that turns an exception into a failure without an action.
5. Write the inheritance check, so that a new repository created from the template of RWB-PLT-N004-OPS inherits the gate set and a local edit, an added gate, a removed gate or a suppressed finding fails the build.
6. Write the release report definition and hand it to RWB-PLT-NF01-OPS, so that the platform administrator and the release manager read one surface per release and no result is written by hand.
7. Prove the gate set in a clone of the template repository with one planted change per gate, and prove the inherit check with a local edit, an added gate, a removed gate and a suppressed finding.
8. Prove the promotion rule with a release of two changed services, one failing and one passing, then both passing; prove the exception rule with a recorded exception, a publication inside the box, and an expiry that returns the gate to a failure.
9. Publish the gate set, its version and the operating note, and hand it to the service teams and to the platform epics.

**Done when.** Each of the eight gates blocks its planted change and names the gate, the file, the line and the rule without repeating the value it found; a gate that did not run, or a result missing from the build record, blocks the release; a release of two services is published only when both have passed every gate, and the build record of each carries the gate-set version and one result per gate; a recorded exception allows one publication inside its box and its expiry returns the gate to a failure; a new repository created from the template runs the same eight gates at the same version with no local edit, and a local edit of the gate set fails the build.

The coverage floor, the duplication limit, the severity cut-off, the tool products, the length of the exception box, the approver role of an exception and the name and form of the reporting surface are Not specified in the source documents (GAP-1428; ASM-2507). The thresholds are ASM-2507, the tool products and the reporting surface are ASM-2508, and the exception box and its approver role are ASM-2509.

### 14. Validation and messages

| Message ID | When | Message |
|---|---|---|
| MSG-P2-004 | A gate job, the gate set or the inheritance check fails, or runs past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P4-002 | A role without the right to approve an exception records one, or a role without the right tries to bypass a gate | You cannot {action} here. Your role does not include it. |

The baseline invents no message ID. The two IDs above already exist in the message catalogue: MSG-P2-004 for a scheduled job or step that fails or runs past its threshold, and MSG-P4-002 for an action the role does not include. Their wording is quoted from the catalogue and is not rewritten here. A gate finding is not a catalogue message and not a screen message: it is a release error with an exit code and a job log line naming the gate, the file, the line, the rule and the gate-set version, and it is never shown to a case user and never repeats the value it found.

### 15. Screens and states

No new Workbench screen and no screen state. The surface this story uses is the release report: one report per release, one row per changed service and gate, with the state of section 9 (Passed, Failed, Waived inside its box, Expired), the gate-set version, the build record reference and the exception in force. The platform administrator and the release manager read it; no one writes a result into it by hand, and it is not shown to a case user. The name and form of that surface are Not specified in the source documents (GAP-1428; ASM-2508), and the gate-result states of section 9 are states of a release and not screen states of the Workbench.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF05-OPS-01 | AC1 | Component | The gate set of the platform repository: the eight gates of BR2 in the recorded order, invoked by the gate set and not by a parameter; a service of the 19-service list and a platform epic resolve to the same gate set and the same version; the version and one result per gate appear in the build record; a removed gate, a gate disabled in a local file and a per-service override each fail the inheritance check and name the service and the gate |
| TC-PLT-NF05-OPS-02 | AC2 | Component | A clone of the template repository with one planted change per gate: a unit or component test below the coverage floor, a client changed against the published OpenAPI, AsyncAPI and activity contract, a cross-schema reference and a join to another service's schema, a migration that fails the lint and a migration the drift check does not reproduce, a literal secret and a personal-data field, an unapproved dependency and a licence outside the policy, an image with a secret or a personal-data pattern in its history, and a static-analysis finding above the severity cut-off; every finding names the gate, the file, the line and the rule and repeats no value |
| TC-PLT-NF05-OPS-03 | AC3 | End to end | A release of two changed services: one gate of one service fails, then a gate is skipped, then a result is missing from the build record, and each of the three leaves the release unpublished with the cause named per service and per gate; when every gate passes for both services the release is published, the build record of each service carries the gate-set version, the commit, the image digest and one result per gate, and the release report shows the same values with no hand-written result |
| TC-PLT-NF05-OPS-04 | AC4 | Component | The exception register: a record with gate, service, commit or image digest, owner role, reason, expiry date and approver role allows one publication inside the box and the exception is shown on the release report; the expiry date returns the gate to a failure with no action; a record without an owner role, an expiry date or an approver role is refused; an exception for a gate on the non-waivable list is refused |
| TC-PLT-NF05-OPS-05 | AC5 | End to end | A new repository created from the template of RWB-PLT-N004-OPS with no gate change: the first build runs the eight gates at the same gate-set version as every other service and its build record carries that version and one result per gate; a local edit of a gate, an added gate, a removed gate and a suppressed finding each fail the build with the gate and the local change named, and the service is not released until the local change is removed |
| TC-PLT-NF05-OPS-06 | AC6 | Component | One check per rule of section 8: the eight gates of BR2 at one version (BR1, BR2); the OpenAPI 3.1, AsyncAPI 3.0 and activity contract checks (BR3); a planted cross-schema reference (BR4); a gate that did not run or left no result (BR5); the build record fields (BR6); an expired exception with its named fields (BR7); a request to except a non-waivable gate (BR8); a gate that errors or times out (BR9); a planted second scanner (BR10); a planted personal-data value in a fixture, a finding or a log (BR11) |

### 17. Guardrails

- One gate set and one gate-set version for the 19 services and the platform epics: no service adds, removes, weakens or suppresses a gate, and the inheritance check fails a local change (BR1).
- A gate that did not run, errored, timed out or left no result is a failure and never a pass; a gate fails closed (BR5, BR9).
- No release without a complete passing build record: the gate-set version, the commit, the image digest and one result per gate for every changed service (BR6).
- An exception is time-boxed, owned by a role, recorded with an approver role, and expires into a failure; a gate marked non-waivable is never excepted (BR7, BR8).
- No business value in the gate configuration or in a test fixture, and no personal data in a test, a finding or a log; every planted value is synthetic (BR11).
- No secret in the gate configuration, a pipeline file, a test fixture or a finding: the gate names the file, the line and the rule and never the value, and the secret and personal-data gate is the rule of RWB-PLT-NF04-OPS (NFR-052, NFR-054).
- The security gates follow NIST SP 800-204C and 800-204D for the DevSecOps pipeline and the supply chain, so the approved-dependency, licence and image-history checks are part of the gate set and not an optional extra (Arch v5 slide 35).
- ACE data only through the owner's contract or the `v_ace_*` views: the gate set reads no ACE data at all, and the boundary gate fails a cross-schema reference before such a read could ship (Arch v5 slide 29).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| NF-05 (legacy key, Moved (no impact)) | Legacy title "Quality gates baseline"; no legacy story text, no legacy criterion and no legacy test case in the source set | The whole gate-set baseline; no built code changes | TC-PLT-NF05-OPS-01, TC-PLT-NF05-OPS-02, TC-PLT-NF05-OPS-03, TC-PLT-NF05-OPS-04, TC-PLT-NF05-OPS-05 |
| Arch v5 slide 11 | Every service publishes OpenAPI 3.1, AsyncAPI 3.0 and its typed activity contract before code, and contract tests run in every build | The contract gate and its place in the gate set | TC-PLT-NF05-OPS-01, TC-PLT-NF05-OPS-02 |
| Arch v5 slide 20 | Every service comes from the service template and the shared libraries, with its own schema, its own task queue, contract tests and the `/health` and `/metrics` endpoints | The inheritance rule: one template, one gate set, no per-service gate | TC-PLT-NF05-OPS-05 |
| Arch v5 slide 29 | One schema and one login per service, no cross-schema join or key, and the boundary test fails on a cross-schema reference, checked in every build | The boundary gate and the migration lint and drift gate | TC-PLT-NF05-OPS-02 |
| Arch v5 slide 35 | Zero trust per NIST SP 800-204, with 800-204C and 800-204D informing the DevSecOps pipeline and the supply-chain controls | The secret and personal-data gate, the approved-dependency and licence gate and the image and image-history gate | TC-PLT-NF05-OPS-02 |
| Arch v5 slide 38 | Wave 0 builds the service template, one Helm chart and the golden pipeline once | The gate set defined once in the template and the golden pipeline | TC-PLT-NF05-OPS-01, TC-PLT-NF05-OPS-05 |
| Arch v5 slide 47 | Risk "Schema rules broken over time", mitigated by the database grants per schema and the boundary test in every build, owned by Architecture | The boundary gate as a mandatory gate of the set | TC-PLT-NF05-OPS-02 |
| NFR-052 (consumed; owned by RWB-PLT-NF04-OPS) | Secrets are held in the key store and never in code, configuration files or prompts | The secret scan of RWB-PLT-NF04-OPS placed in the gate set | TC-PLT-NF05-OPS-02 |
| NFR-054 (consumed; owned by RWB-PLT-NF04-OPS) | The build pipeline blocks a change that carries a secret, personal data or an unapproved dependency | The gate set, the promotion rule and the build record | TC-PLT-NF05-OPS-02, TC-PLT-NF05-OPS-03 |
| Published contracts per service (OpenAPI 3.1, AsyncAPI 3.0, activity contract jar) | The contract documents a service publishes before code | The contract gate | TC-PLT-NF05-OPS-02, TC-PLT-NF05-OPS-05 |

### 19. Out of scope

- The pipeline stages, the repository baseline, the build triggers and the build record format: RWB-PLT-NF01-OPS owns them; this story adds the gate set that runs inside those stages and the fields the record must carry.
- The service pipeline template and the Helm chart: RWB-PLT-N004-OPS owns them; this story states what the template inherits and nothing about the chart.
- The secret scan, the personal-data pattern check, the approved-dependency rules and the image scan themselves: RWB-PLT-NF04-OPS owns them; this story consumes them as gates in the set and writes no second scanner.
- The migrations, the migration lint and the drift gate: RWB-PLT-E1044-OPS and the per-service DB stories own them; this story runs the gate and owns none of its rules.
- The writing of the contract tests and of the module boundary test: RWB-PLT-TE003-APP-2 and RWB-PLT-TE001-APP-2 own them; this story decides that they run as gates for every changed service.
- The observability stack, the dashboards and the alert routing beyond the one gate-job alert: RWB-PLT-OBS owns them.
- The coverage floor, the duplication limit, the severity cut-off, the tool products behind each gate, the length of the exception box and the expiry behaviour of an exception: the gap GAP-1428, for the solution architect and the DevOps lead to close before the gate set is Published.
