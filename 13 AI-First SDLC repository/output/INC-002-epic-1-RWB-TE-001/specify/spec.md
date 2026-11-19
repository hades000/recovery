# Technical Specification — RWB-TE-001 Recovery module folder and boundary test

| Field | Value |
|---|---|
| Story | RWB-TE-001 — Recovery module folder and boundary test |
| Epic / module | E1 / P2 Integration (technical enabler) |
| RUN_ID | `INC-002-epic-1-RWB-TE-001` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 001 Recovery module folder and boundary test v1.md`; REQ-DRI-006; BRD Program §5.2 and §7 |
| Upstream IDs | REQ-DRI-006; DT07; DT08; ADR-002; ADR-005; DL05; DL07; INT-34 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | TechX tech leads (code owners); ACE team for the common package names (DL05); see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label, state or validation presentation changes. The front-end dependency rule is build configuration. |
| Logic In Scope | `YES` — five build-time boundary rules, the module-map completeness rule and the shared access guard. |
| API In Scope | `NO` — no endpoint or schema change. `RecoveryAccessGuard` is wired to the existing `/api/recovery/v1/**` surface. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | ACE unit-test phase; ACE front-end lint step; `/api/recovery/v1/**` request path; `recovery.integration.adapter` (the only file-client package, RWB-E1-007); agent runtime client for INT-23 (RWB-TE-013); common module access check (INT-34). |
| New Nodes Required | `YES` — 19 module packages with `api` and `internal`; `architecture/recovery-modules.yaml`; `ModuleMapLoader`; `RecoveryBoundaryTest`; boundary fixtures; front-end dependency rule file; `RecoveryAccessGuard`. |
| Inherited Existing Behavior | ACE sign-in and access check (RWB-E1-022); role and permission matrix (RWB-E1-037); integration adapter package (RWB-E1-007); agent runtime client (RWB-TE-013); ACE build and merge pipeline. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | BND-1: recovery classes depend on the collection module only through its published packages. | SPEC-RWB-TE-001-004 | DIRECT | ArchUnit rule built from the module map; `collection..internal..` is forbidden. | COVERED |
| BR2 | BND-2: recovery classes depend on the common module only through its published packages. | SPEC-RWB-TE-001-005 | DIRECT | Published package list is data; default `..common.api..` until ACE names it. | COVERED |
| BR3 | BND-3: a recovery module depends on another recovery module only through a package the map lists as published, or an application event. | SPEC-RWB-TE-001-006 | DIRECT | `recovery.<module>.internal..` is forbidden to every other module. | COVERED |
| BR4 | BND-4: entities and repositories of a module are used only inside that module. | SPEC-RWB-TE-001-007 | DIRECT | Rule matches `..entity..`, `..repository..` and `*Entity`/`*Repository` classes. | COVERED |
| BR5 | BND-5: only the packages the map allows use HTTP, SFTP or file-transfer clients; no recovery class calls a system of record. | SPEC-RWB-TE-001-008 | DIRECT | Allowed: `recovery.integration.adapter` and the agent runtime client; all other packages fail. | COVERED |
| BR6 | Module names, packages and published packages are read from the module map, not written in the test. | SPEC-RWB-TE-001-002, SPEC-RWB-TE-001-003 | DIRECT | `ModuleMapLoader` parses the YAML; the test takes no package literal. | COVERED |
| X1 | A recovery class imports a collection internal class. | SPEC-RWB-TE-001-004, SPEC-RWB-TE-001-013 | DIRECT | Build log names BND-1 and both classes. | COVERED |
| X2 | A recovery module imports another recovery module's internal class. | SPEC-RWB-TE-001-006 | DIRECT | Build log names BND-3. | COVERED |
| X3 | A class uses another module's entity or repository. | SPEC-RWB-TE-001-007 | DIRECT | Build log names BND-4. | COVERED |
| X4 | A class outside the allowed packages uses an HTTP, SFTP or file client. | SPEC-RWB-TE-001-008 | DIRECT | Build log names BND-5. | COVERED |
| X5 | A recovery screen imports a collection screen. | SPEC-RWB-TE-001-009 | DIRECT | Front-end build log names `no-collection-import`. | COVERED |
| X6 | A new package is not in the module map. | SPEC-RWB-TE-001-003 | DIRECT | Build log names the package. | COVERED |
| X7 | A role without the right reaches a recovery endpoint. | SPEC-RWB-TE-001-010 | DIRECT | 403 Problem with `messageCode` MSG-P4-002; access test TC-TE-001-08. | COVERED |
> **AC cleanup (4 November 2026):** all previous acceptance criteria in this story were development-process criteria and were removed from story §7. This engineering enabler has no business acceptance criteria; the coverage table above maps the business rules and exception paths only.

## User story intent interpretation
As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a build-time boundary test**, so that **no module calls the inside of another module and no recovery code calls a system of record directly**.

The story is a repository-skeleton enabler. It creates one package per Workbench module with a published part (`api` or a package the module map lists) and an internal part, and it makes the build refuse a violation. It also wires the common module's access check for the recovery API. It adds no screen and no endpoint. Every later Epic 1 story builds inside this skeleton; a violation is a failed pull request, not a production defect.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | Every pull request build and every build of `main`. |
| Preconditions | Access to the ACE repository for TechX (DL36); DL05 option B applied; ACE names the common and collection published packages; the unit-test phase runs on every pull request. |
| Input | Source and compiled classes; `architecture/recovery-modules.yaml`; the front-end dependency rule file; the existing ACE build pipeline. |
| Output | Pass, or a failed build naming the rule code, the class or file, and the dependency. A build report shows the boundary test ran. |
| Feature flag | None — a build check has no runtime path to switch off. |
## Field-level behaviour matrix
| Entity / artefact | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery-modules.yaml` | `module_code` | Module map, authored by TechX tech leads | Editable by pull request | Must be unique; `P1..P10`, `S1..S9` |
| `recovery-modules.yaml` | `package` | Module map | Editable by pull request | Must be a `recovery.<module>` package that exists |
| `recovery-modules.yaml` | `published_packages` | Module map | Editable by pull request | At least one; every entry must resolve to a package |
| `recovery-modules.yaml` | `allowed_client_libraries` | Module map | Editable by pull request | Only `recovery.integration.adapter` and the agent runtime client in E1 |
| `package-info.java` | `module`, `published` | Generated with the package | Editable by pull request | Matches the map entry |
| `RecoveryAccessGuard` | `capability_area`, `right`, `scope_target` | Endpoint declaration | Not editable at run time | Right comes from the permission matrix; scope is own/team/all |
| Boundary fixture | `rule_code`, `fixture_class`, `expected_outcome` | `src/test` | Test-only | Never ships; one fixture per rule |
| Build report | `rule`, `class`, `dependency`, `result` | Test run | Read-only | No personal data; class names only |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Build passed | A pull request adds a violating dependency | Any BND rule broken | Build failed | Report names the rule, class and dependency; merge blocked |
| Build failed | The developer routes the call through `api` or an application event | No rule broken | Build passed | Merge allowed subject to review |
| PR review required | Code owner approves | Changed paths owned by that team | PR approved | Merge allowed when every owning team approves |
| PR approved | A new commit is pushed | Stale approval dismissed | PR review required | Re-review by the owning team |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Recovery class imports `collection.internal` | Build fails; BND-1 named with both classes | Build log: `boundary rule BND-1 broken` |
| X2 | Recovery module imports another recovery module's internal class | Build fails; BND-3 named | Build log: `boundary rule BND-3 broken` |
| X3 | Class uses another module's entity or repository | Build fails; BND-4 named | Build log: `boundary rule BND-4 broken` |
| X4 | HTTP/SFTP/file client outside an allowed package | Build fails; BND-5 named | Build log: `boundary rule BND-5 broken` |
| X5 | Recovery screen imports a collection screen | Front-end build fails | Build log: `rule no-collection-import broken` |
| X6 | New package absent from the map | Build fails before the rules run | Build log: `package {package} is not in the module map` |
| X7 | Role without the right calls a recovery endpoint | 403 Problem; nothing changes | MSG-P4-002 |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | The guard applies to every existing `/api/recovery/v1/**` operation; no operation is added or changed. |
| Contract delta | None. The guard is an implementation of the access check the API specification already declares per operation. |
| Backward compatibility | Unchanged. A permitted caller sees no difference; a forbidden caller now receives the specified 403. |
| Authorization | Capability area and right declared by each operation; scope own/team/all; 403 with `messageCode` MSG-P4-002. |
| Error behaviour | 401 MSG-P4-001 for no session; 403 MSG-P4-002 for no right; no change on refusal. |
| Versioning | No version change. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | SPEC-RWB-TE-001-009 | No screen, component, route, state or label changes. The front-end dependency rule is a lint rule, proven by a fixture in the lint step, not by a component test. | The existing front-end suite stays green; TC-TE-001-06 proves the rule. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR6; SPEC-RWB-TE-001-001..020 | New `ModuleMapLoader`, `RecoveryBoundaryTest` rule set and `RecoveryAccessGuard`; fixtures for each rule. | Unit tests cover map parse success, missing package, duplicate module, each BND rule pass/fail, guard allow/deny, and the build-report format. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `recovery-modules.yaml` | Rule table | Module code, package, published packages, allowed client libraries. |
| `ModuleMapLoader` | Service | Parses the map; fails when a `recovery.**` package is not listed. |
| `RecoveryBoundaryTest` | Test | ArchUnit rules BND-1 to BND-5 built from the map; no package literal in the test. |
| Boundary fixtures | Test | One class per rule under `src/test`, run in expect-failure mode; one passing common-`api` fixture. |
| `RecoveryAccessGuard` | Service | `require(capabilityArea, right, scopeTarget)` calls the common module access check (INT-34) for every recovery endpoint; throws `AccessDeniedException` mapped to 403 MSG-P4-002. |
| Front-end dependency rule | Rule table | No import from `src/modules/collection`; `src/common` only through its public index. |

### Package and boundaries
Back end root `ace-service/src/main/java/<ACE base package>/recovery/`, one package per module: `dataengine` (P1), `integration` (P2), `casewf` (P3), `access` (P4), `dochub` (P5), `comms` (P6), `decision` (P7), `payments` (P8), `reporting` (P9), `agent` (P10), `valuation` (S1), `treatment` (S2), `guarantee` (S3), `litigation` (S4), `asset` (S5), `debtsale` (S6), `writeoff` (S7), `deviation` (S8), `partner` (S9). Each has `api` for published interfaces and `internal` for the rest. A module that publishes from another package, such as `recovery.casewf.allocation` (RWB-E1-020) or `recovery.decision.writer` (RWB-E1-027), lists that package as published in the map. Front end root `ace-web/src/modules/recovery/`.

### Data and migration
No database object. The boundary test reads source and compiled classes and the YAML map. No business field is read or written. No Flyway migration.

### Rules
1. `ModuleMapLoader` reads `module_code`, `package`, `published_packages` and `allowed_client_libraries`; a missing or duplicate module fails the load.
2. BND-1 and BND-2 compare every recovery class dependency against the collection and common published lists.
3. BND-3 allows a dependency on another recovery module only if the target package is in that module's `published_packages`; otherwise it fails.
4. BND-4 fails a reference to another module's `..entity..`, `..repository..` or `*Entity`/`*Repository` class.
5. BND-5 fails any use of `java.net.http.HttpClient`, an SFTP client or a file-transfer client outside `allowed_client_libraries`.
6. The front-end rule fails an import from `src/modules/collection`; `src/common` is allowed only through its public index.
7. A package on the classpath under `recovery.` that is absent from the map fails before the rules run.

### Transaction and events
None. The check is build-time and holds no state. The same commit always gives the same result; a rerun needs no cleanup.

### Security and authority
| Actor | Right | Scope |
|---|---|---|
| RW-TRIBE, tribe lead, squad members | Create folders, map and tests; open pull requests | Repository |
| TechX tech leads | Approve map and rule changes; code owners (RWB-TE-002) | Recovery folders |
| ACE team | Name the common and collection published packages (DL05) | Common and collection |
| RW-PLATADM | Run the pipeline | Environment |

`RecoveryAccessGuard` is the only recovery-side entry to the common access check. It names the capability area and the right per endpoint; the client never decides access.

### Observability and operations
- Build report lists each rule, the class and the dependency, and pass/fail.
- The measure is boundary violations merged to `main`, target zero.
- The test appears in the unit-test report of `main`; a failing fixture blocks a merge.
- No runtime metric, alert or run book: the control is the pipeline.

### Performance
No runtime path. The only constraint is that the check completes inside the unit-test phase of every pull request; the story sets no numeric target. Record the duration in the build report so a slow rule set is visible.

### Feature flag and rollback
None. A build check has no runtime path. Rollback is a revert of the rule or map change through a pull request, reviewed by the code owners.

### No UI change
No screen. A developer reads the result in the pull request checks and the build log. SCR-02 and SCR-09 are unaffected.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-001-01 | BR1 | System | Fixture importing a collection internal class | Build fails; BND-1, both class names |
| TC-TE-001-02 | BR2 | System | Fixture calling a common published interface | Build passes |
| TC-TE-001-03 | BR3 | System | Fixture importing `recovery.decision.internal`, then `recovery.decision.writer` | First fails BND-3; second passes |
| TC-TE-001-04 | BR4 | System | Fixture using another module's entity | Build fails; BND-4 |
| TC-TE-001-05 | BR5 | System | `HttpClient` in `casewf` and in `integration.adapter` | First fails BND-5; second passes |
| TC-TE-001-06 | Engineering verification | System | Front-end fixture importing a collection component | Front-end build fails; `no-collection-import` |
| TC-TE-001-07 | BR6 | System | Package `recovery.vendorx` absent from the map | Build fails naming the package |
| TC-TE-001-08 | X7 | Security | RW-REFADM calls the test-only Case record R endpoint | 403; MSG-P4-002; nothing changes |
| TC-TE-001-09 | BR1–BR5 | Unit | Map with one module per rule | Each rule passes and fails on the matching fixture |
| TC-TE-001-10 | BR6 | Unit | Map with a duplicate module and a missing package | Loader rejects both with a named error |
| TC-TE-001-11 | Guard | Unit | Allowed and forbidden right/scope pairs | Guard returns or throws; message code is MSG-P4-002 |
## Guardrails
- No business value in code; module names, packages and allowed clients are in the module map.
- No personal data in logs, tests or prompts; fixtures hold class names only.
- No read of another module's tables; this story builds the check that enforces it.
- Breaking fixtures stay in `src/test` and never ship.
- The boundary test never hard-codes a package that the map can change.
## Out of scope
- Code owners for the recovery folders: RWB-TE-002.
- Types and contract tests from the API specification: RWB-TE-003.
- Boundaries inside the common and collection modules: the ACE team under DL05 option A.
- The integration adapter pattern itself: RWB-E1-007.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Program §5.2, §7 | None | All recovery processes | BND-1..BND-5 | TC-TE-001-01..TC-TE-001-11 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2, SPEC-005 | The common module's published packages are not named by the ACE team; the story assumes `..common.api..` (DL05). | If ACE names different packages, the map changes, not the rule. | Use `..common.api..` as the map value until ACE names the packages; the map is the single source. | RESOLVED | SPEC-002, SPEC-005 |
| CLAR-002 | SPEC-003 | How does the loader see a package that is not in the map? | Determines whether the rule is enforceable. | Scan the compiled `recovery.**` packages and compare with the map; fail on any unlisted package. | RESOLVED | SPEC-003 |
| CLAR-003 | SPEC-009 | The front-end dependency tool is not named. | Tool choice only; the rule and the failure code are fixed. | Use the existing ACE front-end lint step with import rules; the tool is build configuration. | RESOLVED | SPEC-009 |
| CLAR-004 | BR1–BR5; SPEC-011 | How are breaking fixtures kept from shipping? | Prevents a deliberate violation from reaching production. | Fixtures live under `src/test` only and run in expect-failure mode. | RESOLVED | SPEC-011 |
| CLAR-005 | §10; SPEC-010 | Does `RecoveryAccessGuard` replace the per-endpoint access check? | Determines whether TE-003's access test still applies. | No — the guard is the shared adapter; every endpoint still declares its capability area and right. | RESOLVED | SPEC-010 |
| CLAR-006 | §4; SPEC-012 | Does the check run on `main` as well as on pull requests? | Determines the evidence for the gate. | Yes — every pull request and every build of `main`. | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, DL05 or the ACE build pattern. No item changes the business outcome.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this repository-enabler story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New build-time module boundary and access-guard enabler; no screen and no API contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: repository skeleton, boundary rules and access guard only]
REQUIREMENT_COVERAGE_SUMMARY: No business acceptance criteria (story §7); all 6 business rules, 7 exception paths and the access path are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
