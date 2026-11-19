# Increment Card — INC-036-epic-1-RWB-E1-072

**RWB-E1-072 — Drools runtime and rule package store**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-036` |
| Title | Drools runtime and rule package store |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-072` |
| RUN_ID | `INC-036-epic-1-RWB-E1-072` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 36 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-044, RWB-E1-043, RWB-E1-027 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the recovery module to evaluate rules with embedded Drools from versioned rule packages held in the database**, so that **every engine uses one evaluator and every decision names the rule and the package version that made it**.

**Business outcome:** ADR-012 replaces ADR-004 and keeps its principle that rules are versioned data. The home-built decision-table component has no standard compile check, no first-match guarantee that a reviewer can see and no single place where the version in force is chosen. A rule change in one engine can therefore behave differently from the same rows in another engine, and a decision cannot always name the row and version behind it.

**Main flow:**
1. Deployment: Flyway migration V072_1__rule_package.sql creates rule_package and rule_package_version, adds DF-REF-296 to DF-REF-298 to rule_row and DF-REF-299 to rule_test_case, and seeds the five Epic 1 package codes.
2. Caller (for example the allocation engine): builds the facts object from its own data and calls RuleEvaluator.evaluate("ALLOCATION", facts, businessDate).
3. RuleEvaluatorImpl: reads the versions of ALLOCATION and selects the one with status IN_FORCE and valid_from <= businessDate <= valid_to.
4. RuleEvaluatorImpl: asks KieBaseRegistry for the KieBase of that package version.
5. KieBaseRegistry: on a cache miss, recomputes the SHA-256 of drl_source, compares it with rule_package_version.checksum and compiles the DRL into a KieBase; on a mismatch it refuses the version, raises an incident and does not cache it.
6. RuleEvaluatorImpl: inserts the facts, fires the package, and the agenda listener records the Drools rule name of the one rule that fired.

**Acceptance criteria:**
- AC1: Evaluation returns the rule and the package version
- AC2: The date picks the right version
- AC3: No version in force
- AC4: Exactly one rule fires
- AC5: The cache is reused
- AC6: Checksum mismatch
- AC7: The catalog returns the row fields

**Out of scope:**
- Upload, compile check at load, scenarios, approval and rollback (RWB-E1-073).
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (RWB-E2-042).
- The change checklist and the rule change audit report (RWB-E2-041).
- The decision log store and the writer (RWB-E1-008, RWB-E1-027).
- The admin screen for rules (Epic 8, FEAT-ADM-02).
- The Temporal cluster and worker (RWB-E1-070, RWB-E1-071).
- The other 448 routing rules and the UNIVERSAL package (later epics; DL24).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-072-drools-runtime-and-rule-package-store-v1.md` |
| Requirement IDs | REQ-CWC-016, REQ-DRI-001, REQ-DRI-004, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| Decision | D-RCV-36 (T3, T5, T6, T7); ADR-012 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Reads packages, versions and the catalog (Rules and parameters R) |
| RW-RISK | Reads packages and versions before approval (Rules and parameters R) |
| RW-AUDIT | Reads packages, versions and checksums (Rules and parameters R) |
| RW-PLATADM | Receives the cache and checksum incidents; operates the service |
| SY-RULES | Evaluates packages and serves the catalog; no endpoint right |
| SY-CASEWF | Calls the evaluator from an activity and writes the result to the decision log |
| RW-REFADM | Reads the package list; may not change a version |
| No delegation of authority level applies | A rule evaluation is not a credit decision |

## Contract extract

**GET /api/recovery/v1/admin/rule-packages** (P3/P4 endpoint; the tables are P4, the evaluator is P3) | Item | Value | |---|---| | Request | Query: packageCode (optional), status (optional; IN_FORCE by default) | | Response | 200 RulePackage[]: packageCode, title, ownerRole, hitPolicy and versionInForce with versionId, versionLabel, validFrom, checksum; versionInForce is null when no version is in force | | Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 404 unknown packageCode; 503 | | Authorization | Rules and parameters, right R | | Idempotency | Read only | **Published interfaces** (package recovery.casewf.rules): ```java public interface RuleEvaluator { RuleResult evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce } public record RuleResult(String packageCode, String packageVersion, String ruleId, Map<String, Object> outp…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: packages, rows, salience, conditions and outputs are data in the database and the workbook. - No personal data in logs, tests, workflow history or prompts: facts are codes and numbers, and the result holds codes only. - No read of another module's tables; ACE data only through recovery.v_ace_* views: the evaluator receives facts from the caller and reads no case or ACE table. - A Temporal workflow calls Drools only inside an activity; no workflow class calls RuleEvaluator (T7). - No cache of a version whose checksum fails, and no silent fallback to an earlier version. - No second evaluator: every engine and the test runner calls RuleEvaluator, and no engine reads drl_source. - No edit of a package version in place; a correction is a new version.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-072-drools-runtime-and-rule-package-store-v1.md` |
| Specification | `output/INC-036-epic-1-RWB-E1-072/specify/spec.md` |
| Compliance validation | `output/INC-036-epic-1-RWB-E1-072/specify/compliance-validation.md` |
| Agent run log | `output/INC-036-epic-1-RWB-E1-072/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-036-epic-1-RWB-E1-072/plan/` |
| Implementation evidence | `output/INC-036-epic-1-RWB-E1-072/implement/` |
| API / functional test reports | `output/INC-036-epic-1-RWB-E1-072/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-036-epic-1-RWB-E1-072/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-072-drools-runtime-and-rule-package-store-v1.md` |
| Output run | `output/INC-036-epic-1-RWB-E1-072/` |

