# Ponytail review TE-001

- **Session ID:** `ses_e13a11e21ffe7jFSrRchcn4Zfs`
- **Created:** 2026-11-18 08:56  |  **Last activity:** 2026-11-18 09:25
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `general`
- **Parent session:** Implementation verification (`ses_e13fa37feffeVx4Vlyz4X6NtKl`)
- **Tokens:** 76,794 in / 1,759 out / 3,742 reasoning
- **Messages:** 17

---

### User - 2026-11-18 08:56

You are a subagent spawned by another session.
You are the senior developer performing the **ponytail-review** pre-merge review for story RWB-TE-001.

Read and follow the skill exactly: `C:\Users\SahilMore\.claude\skills\ponytail-review\SKILL.md`. Also read `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\RUN-BRIEF.md`, `AGENTS.md`, and the TE-001 plan at `aisdlc/output/INC-002-epic-1-RWB-TE-001/plan/plan.md` (especially the task and coverage intent).

Review the whole story diff:
`git -C "C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001" diff develop-recovery...feature/RWB-TE-001-module-boundary`
Read the touched code, the tests and the callers. The change relocates 26 main classes and 4 tests into `casewf.*`, `integration.flags`, `dochub.*` and `access.*`, adds 61 package-info files, a module map loader and ArchUnit/Modulith boundary rules, a coverage gate, and a frontend import-boundary test. The expected load is a developer build and CI: thousands of classes scanned per build, one local stack. Judge against that.

Look for real bugs, security/data-loss risks, scale problems at build/test time, missing tests for risky logic, slowness and lean/code-that-should-not-exist. Every finding needs a concrete failing case and the smallest fix. No style taste. If the diff is sound, say so.

Write only `aisdlc/output/INC-002-epic-1-RWB-TE-001/review/ponytail-review.md` in the skill's output format (What this change does; Must fix / Should fix / Nice to have with numbered findings; Verdict; Lean; Not checked). Do not edit code, tests, plans or shared files. Do not ask the user anything.

Report in under 200 words: verdict, counts per group, and the finding headlines.

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

I'll start by reading the skill and the project context files.

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\.claude\\skills\\ponytail-review\\SKILL.md"}
```

```text
Read file C:\Users\SahilMore\.claude\skills\ponytail-review\SKILL.md, lines 1-101
1: ---
2: name: ponytail-review
3: description: >
4:   Quality review of a change: is the logic right, is it safe, does it hold
5:   under real load, is risky code tested, is it fast enough, and is every line
6:   needed. Reads the connected code, not only the diff. Each finding is
7:   explained in plain English. Use for "review this", "code review", "review
8:   the last commit", "review my PR", "is this over-engineered", /ponytail-review.
9: ---
10: 
11: Review a change like the senior developer who will be paged when it breaks.
12: Order of importance: correct, safe, holds under load, tested, fast, lean.
13: Lean still matters: every extra line must be read, tested and fixed later.
14: This is a report the user asked for, so give it in full.
15: 
16: ## 1. Understand first
17: 
18: - Review what the user names: uncommitted or staged changes, a branch, a PR
19:   link, or files. Nothing named: the uncommitted changes, or the last commit
20:   if there are none.
21: - Read the diff, then the code it touches: callers of every changed function,
22:   the functions it calls, the tests, the README.
23: - Trace the real flow: where data comes in, what is stored, what goes out.
24: - A change can break code it does not touch. When a signature, return value
25:   or behavior changes, grep every caller.
26: - Find the expected load in the repo (README, deploy config): one person
27:   running a script, or many users and processes at once. Judge scale against
28:   that, and say which load you assumed.
29: 
30: ## 2. Look for
31: 
32: 1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item,
33:    rounding, time zones), a caller broken by the change, a fix applied in one
34:    caller while the shared function stays broken.
35: 2. **Risk:** security holes (injection, weak randomness, secrets, missing
36:    checks on input from users), data loss (errors swallowed, writes in the
37:    wrong order, no transaction).
38: 3. **Scale:** fine for one user, wrong for many: check-then-write races, the
39:    same work done by every process, memory or lists that only grow, a query
40:    per item, O(n^2) on big input, per-process state that must be shared.
41: 4. **Missing test:** risky new logic (a branch, a parser, money, security,
42:    data writes, a bug fix) with no test that fails when it breaks. One good
43:    test, not coverage.
44: 5. **Speed:** big slowdowns are
... truncated (5,621 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\RUN-BRIEF.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\RUN-BRIEF.md, lines 1-97
1: # Run brief for every lifecycle agent in this repository
2: 
3: Read this before you start. It adapts the AISDLC v2 agent instructions to this repository's layout.
4: It does not change any gate, rule or output name in your instructions.
5: 
6: ## Paths
7: 
8: | Name in your instructions | Path here |
9: |---|---|
10: | Workspace root (`.github/`, `docs/`, `requirement/`, `output/`) | `<repo>/aisdlc/` |
11: | ACE monorepo / code repository / `ace-monorepo/` | `<repo>/` (this repository's root; local stand-in for ACE) |
12: | `ace-monorepo/AGENTS.md`, coding standard | `<repo>/AGENTS.md`, `<repo>/aisdlc/.github/contexts/backend-standards.md`, `frontend-standards.md` |
13: | `requirement/legacy/` (the converted document set v14) | `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` (read only) |
14: | Story file paths in the increment cards | relative to `<docset>/17 AI-First SDLC Repository v2/` |
15: | Earlier v2 artefacts for your story, if any | `<repo>/aisdlc/output/<RUN_ID>/_v2-baseline/` (history: reuse what is still correct, never overwrite) |
16: 
17: `<repo>` is `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench`.
18: `<docset>` is `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14`.
19: 
20: ## Hard rules for this run
21: 
22: 1. **Never change anything in `<docset>` outside `<repo>`.** The document set is read only. A
23:    document that is wrong or silent is recorded as a gap (below), never edited.
24: 2. **Write only to your own stage folder**, `aisdlc/output/<RUN_ID>/<stage>/`. The Implementation Builder
25:    also writes code, and only in the git worktree it is given.
26: 3. **Shared files are not yours.** Do not edit `aisdlc/docs/open-items.md`,
27:    `aisdlc/requirement/Traceability_Matrix.md`, `aisdlc/docs/increments/INDEX.md`, the increment cards
28:    or `aisdlc/DOCUMENT-GAPS.md`. Agents run in parallel. Write the rows you would add to
29:    `aisdlc/output/<RUN_ID>/<stage>/shared-updates.md`, and the orchestrator applies them in order.
30:    The Traceability Manager is the exception: it may edit `Traceability_Matrix.md`.
31: 4. **No question to the user** (L-RCV-03). Record assumptions in your stage's `assumptions.md`.
32: 5. **No Jira, Confluence, GitLab or Figma MCP is connected.** Follow your instructions' fallback
33:    pa
... truncated (7,401 chars total)
```

> **Synthetic** - 2026-11-18 08:56

Instructions from: C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\AGENTS.md
# Recovery Workbench — AI engineering standards (v2)

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Baseline:** document set v14, 16 November 2026. The implementation evidence from 10 November 2026
(`RWB-E1-042`, `RWB-TE-001`) is preserved; both are re-specified against this baseline.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`.

## 1. The seven working rules

1. The person who merges a change owns it, whoever or whatever wrote it.
2. The agent works from files: the standards file, the story file and the plan file. Anything the
   agent needs is in one of the three.
3. The tests and the acceptance criteria exist before the code is generated.
4. Every line that reaches production is read by a person.
5. An AI error found by a reviewer is written into this file, so the agent is told not to repeat it.
6. No personal data or production data goes into a prompt, a test or a log.
7. The unit of work is one story. Work is merged at least once a working day.

## 2. Structure and stack

- The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
- Back end: Spring Boot (Java 21), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL, schema `recovery` in the ACE database, referenced only as
  `${recoverySchema}` and fixed to `recovery` in every environment (D-RCV-28). Schema changes use
  versioned migrations, one migration per story, forward-only. Files are named
  `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence taken in merge order and line 1
  is `-- Story: <story key>`.
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. From Epic 3 the case lifecycle runs on Temporal; case data stays in the recovery
  schema (D-RCV-36, ADR-011).
- Rules are versioned data, authored as Drools XLS decision-table packages and evaluated by embedded
  Drools (D-RCV-36, ADR-012).
- Hosting: the ACE namespace on the shared ACE AKS clusters; Temporal is self-hosted in the same
  namespace.

## 3. The agent must

1. Put recovery code in the recovery module folder only. Change the common or collection module only
   where the story file names it.
2. Read every threshold, limit, timer, queue, role, template and route from its versioned reference
   table. Never write one as a literal in code.
3. Put a Spring Security method check on every endpoint, naming the capability area and the operation.
4. Write a decision record entry for every change to a case and every decision, with the rule ID and
   version used.
5. Use the names in the business glossary for classes, fields, tables and endpoints.
6. Return each validation message from the message table by its rule ID.
7. Make database changes by migration script only, one script per story. Name it
   `V<seq>__<story>_<name>.sql`; line 1 is `-- Story: <story key>`. A corrective script takes the
   next sequence, keeps the original story key and adds line 2 `-- Fix: <reason>` (D-RCV-28).
8. Use Spring Batch and Quartz for every Epic 1...

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Let me read the plan and then the diff.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\output\\INC-002-epic-1-RWB-TE-001\\plan\\plan.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\output\INC-002-epic-1-RWB-TE-001\plan\plan.md, lines 1-364
1: ---
2: title: "Implementation Plan: RWB-TE-001 Recovery module folder and boundary test"
3: run_id: "INC-002-epic-1-RWB-TE-001"
4: story: "RWB-TE-001"
5: epic: "EPIC-001"
6: status: "SUCCESS"
7: revision: "v7 (18 Nov 2026): plan gate round 6 findings PLAN-023..024 fixed (v6 kept as plan.run6.md); round 5 findings PLAN-021..022 fixed and the one-module reading settled by D-RUN-21 in v6 (v5 kept as plan.run5.md, v4 as plan.run4.md, v3 as plan.run3.md, v2 as plan.run2.md, v1 as plan.run1.md). Planned against spec v4 (spec gate round 5 PASS)"
8: prepared: "2026-11-18"
9: ---
10: 
11: # Implementation Plan: RWB-TE-001 Recovery module folder and boundary test
12: 
13: Design Source: `NOT_REQUIRED` (UI In Scope: NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` in spec.md).
14: 
15: | Field | Value |
16: |---|---|
17: | Spec | `../specify/spec.md` v4. Spec gate round 5: `PASS` 0/0/0/0 (`../review/spec-gate-review-5.md`). `Status: SUCCESS`; `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [MISSING_RULES: 0] [CONTRADICTIONS: 0]`. |
18: | Carried plan inputs | Spec gate round 3 "Plan inputs" 1–6 and round 2 plan inputs 1–5 and 7 (table "Carried plan inputs" below). Round-1 plan inputs 1–11 are already in the spec; the relevant ones are applied again where they name a file. |
19: | Code base | This repository as read on 18 Nov 2026 (`backend/`, `frontend/`, `scripts/dev.ps1`, `.gitlab-ci.yml`). No git run, no file outside `plan/` and `review/` written. |
20: | Builder | Implementation Builder, in its own git worktree on `feature/RWB-TE-001-module-boundary` from `develop-recovery`; commits `RWB-TE-001: <summary>` with the `AISDLC-Run` and `AISDLC-Plan` trailers (CLAUDE.md). |
21: | Smallest change | Extend `RecoveryBoundaryTest` and keep `ModulithTest` unchanged; one tooling package (three test-scope classes); move classes without behaviour change; one shared file edited (`backend/build.gradle.kts`); one frontend test file. No new dependency, endpoint, migration, pipeline, script or frontend config change. |
22: 
23: ## Upstream readiness
24: 
25: | Check | Result |
26: |---|---|
27: | Spec status | `SUCCESS` (spec front matter and "Status reporting") |
28: | Spec gate | `PASS` round 5, no open finding |
29: | `REQUIREMENT_COVERAGE_RESULT` | `MISSING_RULES: 0`, `CONTRADICTIONS: 0` |
30: | Clarificat
... truncated (52,829 chars total)
```

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Now let me look at the worktree and the diff.

</details>

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" rev-parse --abbrev-ref HEAD; git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" log --oneline develop-recovery..feature/RWB-TE-001-module-boundary"}
```

```text
feature/RWB-TE-001-module-boundary
473f0af RWB-TE-001: frontend import boundary test, green (TASK-15, TASK-16)
8bad2e7 RWB-TE-001: coverage tests for the relocated classes, gate passes (TASK-12)
5df3097 RWB-TE-001: module skeleton, relocation and property split, green (TASK-11)
220138d RWB-TE-001: Modulith fixture proof, real-code boundary test and binding tests, red (TASK-08, TASK-09, TASK-10)
e34f42a RWB-TE-001: map-driven boundary rules, green (TASK-07)
c4a6ae4 RWB-TE-001: boundary rule tests, red (TASK-06)
53510fb RWB-TE-001: boundary fixture worlds and fixture maps (TASK-05)
e04fce3 RWB-TE-001: module map loader and model, green (TASK-04)
440b3c6 RWB-TE-001: module map and loader tests, red (TASK-02, TASK-03)
fe88d50 RWB-TE-001: coverage gate at 80% on four counters, tooling measured (TASK-01, red)

```

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff --stat develop-recovery...feature/RWB-TE-001-module-boundary"}
```

```text
 backend/build.gradle.kts                           |  24 +-
 .../{platform => access}/api/ApiError.java         |  10 +-
 .../api/ApiProblemException.java                   |   2 +-
 .../ace/demo/recovery/access/api/package-info.java |   3 +
 .../internal/ApiExceptionHandler.java              |   8 +-
 .../internal/ProblemFactory.java                   |   4 +-
 .../internal/RecoverySecurityProperties.java       |  14 +
 .../internal/SecurityConfig.java                   |  18 +-
 .../recovery/access/internal/package-info.java     |   2 +
 .../scb/ace/demo/recovery/access/package-info.java |   3 +
 .../ace/demo/recovery/agent/api/package-info.java  |   3 +
 .../demo/recovery/agent/internal/package-info.java |   2 +
 .../scb/ace/demo/recovery/agent/package-info.java  |   3 +
 .../ace/demo/recovery/asset/api/package-info.java  |   3 +
 .../demo/recovery/asset/internal/package-info.java |   2 +
 .../scb/ace/demo/recovery/asset/package-info.java  |   3 +
 .../admin}/TemporalAdminController.java            |  12 +-
 .../ace/demo/recovery/casewf/api/package-info.java |   3 +
 .../recovery/casewf/internal/package-info.java     |   2 +
 .../migration}/RecoveryFlywayConfig.java           |   8 +-
 .../migration/RecoveryMigrationProperties.java     |  15 +
 .../scb/ace/demo/recovery/casewf/package-info.java |   3 +
 .../api => casewf/rules}/CompiledRulePackage.java  |   2 +-
 .../rules}/DroolsProperties.java                   |   2 +-
 .../rules}/DroolsRuleEngine.java                   |  14 +-
 .../{rules/api => casewf/rules}/RuleEngine.java    |   2 +-
 .../{rules/api => casewf/rules}/RuleInput.java     |   2 +-
 .../{rules/api => casewf/rules}/RuleOutcome.java   |   2 +-
 .../{rules/api => casewf/rules}/RuleResult.java    |   2 +-
 .../demo/recovery/casewf/rules/package-info.java   |   3 +
 .../api => casewf/timers}/TimerScheduler.java      |   2 +-
 .../timers}/internal/QuartzTimerScheduler.java     |   4 +-
 .../demo/recovery/casewf/timers/package-info.java  |   3 +
 .../api => casewf/workflow}/WorkflowIds.java       |   2 +-
 .../workflow/internal/PdpaPayloadCodec.java        |   6 +-
 .../workflow/internal/PlatformSmokeWorkflow.java   |   2 +-
 .../workflow/internal/TemporalConfig.java          |   4 +-
 .../workflow/internal/TemporalProperties.java      |   4 +-
 .../recovery/casewf/workflow/package-info.java     |   3 +
 .../ace/demo/recovery/comms/api/package-info.java  |   3 +
 .../demo/recovery/comms/internal/package-info.java |   2 +
 .../scb/ace/demo/
... truncated (13,756 chars total)
```

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Let's read the key files. Start with the tooling: ModuleMapLoader, BoundaryRules, ModuleMap, RecoveryBoundaryTest, build.gradle.kts changes, the frontend test, and the module map yaml.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\boundary\\ModuleMapLoader.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\boundary\ModuleMapLoader.java, lines 1-240
1: package th.co.scb.ace.demo.recovery.architecture.boundary;
2: 
3: import java.io.IOException;
4: import java.nio.file.Files;
5: import java.nio.file.Path;
6: import java.util.ArrayList;
7: import java.util.LinkedHashMap;
8: import java.util.LinkedHashSet;
9: import java.util.List;
10: import java.util.Map;
11: import java.util.Set;
12: import java.util.regex.Pattern;
13: 
14: import org.yaml.snakeyaml.LoaderOptions;
15: import org.yaml.snakeyaml.Yaml;
16: import org.yaml.snakeyaml.constructor.SafeConstructor;
17: import org.yaml.snakeyaml.error.YAMLException;
18: 
19: /**
20:  * RWB-TE-001 SPEC-003 (BR6): reads the module map into {@link ModuleMap}. Every malformed map is
21:  * refused with {@code <file>: <field path>: <problem>}; the optional {@code sourceViews} key is
22:  * carried unvalidated for RWB-E1-069. No package literal: the root comes from the map.
23:  */
24: public final class ModuleMapLoader {
25: 
26: 	private static final Pattern CODE = Pattern.compile("^(P([1-9]|10)|S[1-9])$");
27: 
28: 	private static final Pattern NAME = Pattern.compile("^[a-z][a-z0-9]*$");
29: 
30: 	private static final Pattern PACKAGE = Pattern.compile("^[a-z][a-z0-9]*(\\.[a-z][a-z0-9]*)*$");
31: 
32: 	private static final Pattern JAVA_NAME = Pattern.compile("^[A-Za-z_$][A-Za-z0-9_$]*(\\.[A-Za-z_$][A-Za-z0-9_$]*)*$");
33: 
34: 	private static final Set<String> TOP_LEVEL_KEYS = Set.of("rootPackage", "modules", "external", "clientLibraries",
35: 			"sourceViews");
36: 
37: 	private static final Set<String> MODULE_KEYS = Set.of("code", "name", "published", "clientPackages");
38: 
39: 	private static final Set<String> EXTERNAL_KEYS = Set.of("name", "rootPackage", "published");
40: 
41: 	private static final Set<String> EXTERNAL_NAMES = Set.of("common", "collection");
42: 
43: 	private ModuleMapLoader() {
44: 	}
45: 
46: 	public static ModuleMap load(Path file) {
47: 		String source = file.getFileName().toString();
48: 		Map<String, Object> root = mapping(parse(source, file), "$", source);
49: 
50: 		for (String key : root.keySet()) {
51: 			if (!TOP_LEVEL_KEYS.contains(key)) {
52: 				throw fail(source, key, "unknown key");
53: 			}
54: 		}
55: 
56: 		String rootPackage = requiredString(root, "rootPackage", "rootPackage", source);
57: 		if (!PACKAGE.matcher(rootPackage).
... truncated (10,324 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\boundary\\ModuleMap.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\boundary\ModuleMap.java, lines 1-47
1: package th.co.scb.ace.demo.recovery.architecture.boundary;
2: 
3: import java.util.List;
4: import java.util.Optional;
5: 
6: /**
7:  * RWB-TE-001 SPEC-002, SPEC-003 (BR6): immutable model of the module map. The map is the only
8:  * source of module names, packages, published packages, client packages and client libraries.
9:  */
10: public record ModuleMap(String source, String rootPackage, List<Module> modules, List<External> external,
11: 		List<String> clientLibraries, Object sourceViews) {
12: 
13: 	public ModuleMap {
14: 		modules = List.copyOf(modules);
15: 		external = List.copyOf(external);
16: 		clientLibraries = List.copyOf(clientLibraries);
17: 	}
18: 
19: 	/** One nested design module of the recovery module (P1..P10, S1..S9). */
20: 	public record Module(String code, String name, List<String> published, List<String> clientPackages) {
21: 
22: 		public Module {
23: 			published = List.copyOf(published);
24: 			clientPackages = List.copyOf(clientPackages);
25: 		}
26: 	}
27: 
28: 	/** One module outside the recovery root whose published packages may be used. */
29: 	public record External(String name, String rootPackage, List<String> published) {
30: 
31: 		public External {
32: 			published = List.copyOf(published);
33: 		}
34: 	}
35: 
36: 	public String modulePackage(Module module) {
37: 		return rootPackage + "." + module.name();
38: 	}
39: 
40: 	/** The module whose package equals {@code packageName} or is a prefix of it. */
41: 	public Optional<Module> moduleOf(String packageName) {
42: 		return modules.stream()
43: 			.filter(module -> packageName.equals(modulePackage(module))
44: 					|| packageName.startsWith(modulePackage(module) + "."))
45: 			.findFirst();
46: 	}
47: }
```

> **Synthetic** - 2026-11-18 08:56

Instructions from: C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\AGENTS.md
# Recovery Workbench — AI engineering standards (v2)

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Baseline:** document set v14, 16 November 2026. The implementation evidence from 10 November 2026
(`RWB-E1-042`, `RWB-TE-001`) is preserved; both are re-specified against this baseline.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`.

## 1. The seven working rules

1. The person who merges a change owns it, whoever or whatever wrote it.
2. The agent works from files: the standards file, the story file and the plan file. Anything the
   agent needs is in one of the three.
3. The tests and the acceptance criteria exist before the code is generated.
4. Every line that reaches production is read by a person.
5. An AI error found by a reviewer is written into this file, so the agent is told not to repeat it.
6. No personal data or production data goes into a prompt, a test or a log.
7. The unit of work is one story. Work is merged at least once a working day.

## 2. Structure and stack

- The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
- Back end: Spring Boot (Java 21), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL, schema `recovery` in the ACE database, referenced only as
  `${recoverySchema}` and fixed to `recovery` in every environment (D-RCV-28). Schema changes use
  versioned migrations, one migration per story, forward-only. Files are named
  `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence taken in merge order and line 1
  is `-- Story: <story key>`.
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. From Epic 3 the case lifecycle runs on Temporal; case data stays in the recovery
  schema (D-RCV-36, ADR-011).
- Rules are versioned data, authored as Drools XLS decision-table packages and evaluated by embedded
  Drools (D-RCV-36, ADR-012).
- Hosting: the ACE namespace on the shared ACE AKS clusters; Temporal is self-hosted in the same
  namespace.

## 3. The agent must

1. Put recovery code in the recovery module folder only. Change the common or collection module only
   where the story file names it.
2. Read every threshold, limit, timer, queue, role, template and route from its versioned reference
   table. Never write one as a literal in code.
3. Put a Spring Security method check on every endpoint, naming the capability area and the operation.
4. Write a decision record entry for every change to a case and every decision, with the rule ID and
   version used.
5. Use the names in the business glossary for classes, fields, tables and endpoints.
6. Return each validation message from the message table by its rule ID.
7. Make database changes by migration script only, one script per story. Name it
   `V<seq>__<story>_<name>.sql`; line 1 is `-- Story: <story key>`. A corrective script takes the
   next sequence, keeps the original story key and adds line 2 `-- Fix: <reason>` (D-RCV-28).
8. Use Spring Batch and Quartz for every Epic 1 and Epi...

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\boundary\\BoundaryRules.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\boundary\BoundaryRules.java, lines 1-314
1: package th.co.scb.ace.demo.recovery.architecture.boundary;
2: 
3: import java.util.ArrayList;
4: import java.util.LinkedHashSet;
5: import java.util.List;
6: import java.util.Optional;
7: import java.util.Set;
8: 
9: import com.tngtech.archunit.core.domain.Dependency;
10: import com.tngtech.archunit.core.domain.JavaClass;
11: import com.tngtech.archunit.core.domain.JavaModifier;
12: import com.tngtech.archunit.core.domain.JavaPackage;
13: import com.tngtech.archunit.lang.ArchCondition;
14: import com.tngtech.archunit.lang.ArchRule;
15: import com.tngtech.archunit.lang.ConditionEvents;
16: import com.tngtech.archunit.lang.SimpleConditionEvent;
17: import com.tngtech.archunit.lang.syntax.ArchRuleDefinition;
18: import jakarta.persistence.Entity;
19: import org.springframework.data.repository.Repository;
20: import org.springframework.modulith.NamedInterface;
21: 
22: /**
23:  * RWB-TE-001 SPEC-004..-010 (BR1..BR6): the map-driven boundary rules. Every rule reports one line
24:  * per distinct violation with the SPEC-010 text; the map is the only source of module names,
25:  * packages, published packages, client packages and client libraries.
26:  */
27: public final class BoundaryRules {
28: 
29: 	private static final String TEMPLATE = "Rule %s broken: %s depends on %s. Use %s.api or an application event.";
30: 
31: 	private BoundaryRules() {
32: 	}
33: 
34: 	public static List<ArchRule> all(ModuleMap map) {
35: 		return List.of(moduleMap(map), bnd1(map), bnd2(map), bnd4(map), bnd5(map));
36: 	}
37: 
38: 	public static ArchRule moduleMap(ModuleMap map) {
39: 		return rule(new ModuleMapCondition(map));
40: 	}
41: 
42: 	public static ArchRule bnd1(ModuleMap map) {
43: 		return rule(new ExternalCondition(map, "BND-1", external(map, "collection"))).allowEmptyShould(true);
44: 	}
45: 
46: 	public static ArchRule bnd2(ModuleMap map) {
47: 		return rule(new ExternalCondition(map, "BND-2", external(map, "common"))).allowEmptyShould(true);
48: 	}
49: 
50: 	public static ArchRule bnd4(ModuleMap map) {
51: 		return rule(new EntityCondition(map));
52: 	}
53: 
54: 	public static ArchRule bnd5(ModuleMap map) {
55: 		return rule(new ClientLibraryCondition(map));
56: 	}
57: 
58: 	/** A dependency matches when it equals the entry or starts past its dot or dollar boundary. */

... truncated (12,678 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Now let's look at ModuleMapLoader tests, BoundaryRulesTest, RecoveryBoundaryTest, the module map yaml, and the build.gradle changes.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\RecoveryBoundaryTest.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\RecoveryBoundaryTest.java, lines 1-204
1: package th.co.scb.ace.demo.recovery.architecture;
2: 
3: import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
4: import static org.assertj.core.api.Assertions.assertThat;
5: 
6: import java.io.IOException;
7: import java.nio.file.Files;
8: import java.nio.file.Path;
9: import java.util.ArrayList;
10: import java.util.List;
11: import java.util.Map;
12: import java.util.Set;
13: import java.util.TreeMap;
14: import java.util.regex.Pattern;
15: import java.util.stream.Stream;
16: 
17: import com.tngtech.archunit.core.domain.JavaClass;
18: import com.tngtech.archunit.core.domain.JavaClasses;
19: import com.tngtech.archunit.core.domain.JavaModifier;
20: import com.tngtech.archunit.core.importer.ClassFileImporter;
21: import com.tngtech.archunit.core.importer.ImportOption;
22: import com.tngtech.archunit.lang.ArchRule;
23: import org.junit.jupiter.api.Test;
24: import org.springframework.modulith.core.ApplicationModule;
25: import org.springframework.modulith.core.ApplicationModules;
26: import org.springframework.modulith.core.NamedInterface;
27: 
28: import th.co.scb.ace.demo.AceRecoveryApplication;
29: import th.co.scb.ace.demo.recovery.architecture.boundary.BoundaryRules;
30: import th.co.scb.ace.demo.recovery.architecture.boundary.ModuleMap;
31: import th.co.scb.ace.demo.recovery.architecture.boundary.ModuleMapLoader;
32: 
33: /**
34:  * Recovery boundary rules that Spring Modulith does not cover (RWB-TE-001 SPEC-004..-010, -025,
35:  * -026). The rules read the module map; the published surface and package skeleton are asserted
36:  * against the real main classes.
37:  */
38: class RecoveryBoundaryTest {
39: 
40: 	private static final ModuleMap MAP = ModuleMapLoader
41: 		.load(Path.of("src/test/resources/architecture/recovery-modules.yaml"));
42: 
43: 	private static final Path SOURCES = Path
44: 		.of("src/main/java", MAP.rootPackage().replace('.', '/'));
45: 
46: 	private static final Set<String> PUBLISHED_PACKAGES = Set.of("casewf.rules", "casewf.timers",
47: 			"casewf.workflow", "integration.flags.api", "access.api", "dochub.api");
48: 
49: 	private final JavaClasses classes = new ClassFileImporter()
50: 		.withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
51: 		.importPackages(MAP.rootPackage());
52: 
53: 	/** MAP:
... truncated (9,848 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\resources\\architecture\\recovery-modules.yaml"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\resources\architecture\recovery-modules.yaml, lines 1-44
1: # Recovery module map (RWB-TE-001, D-RCV-37). The only source of module names, packages,
2: # published packages, client packages and client libraries for the boundary rules (BR6).
3: # Change by merge request, with code-owner approval once RWB-TE-002 lands (D-RCV-21).
4: rootPackage: th.co.scb.ace.demo.recovery
5: modules:
6:   - { code: P1, name: dataengine, published: [api], clientPackages: [] }
7:   - { code: P2, name: integration, published: [api, flags.api], clientPackages: [adapter] }
8:   - { code: P3, name: casewf, published: [api, rules, timers, workflow], clientPackages: [] }
9:   - { code: P4, name: access, published: [api], clientPackages: [] }
10:   - { code: P5, name: dochub, published: [api], clientPackages: [storage] }
11:   - { code: P6, name: comms, published: [api], clientPackages: [] }
12:   - { code: P7, name: decision, published: [api], clientPackages: [] }
13:   - { code: P8, name: payments, published: [api], clientPackages: [] }
14:   - { code: P9, name: reporting, published: [api], clientPackages: [] }
15:   - { code: P10, name: agent, published: [api], clientPackages: [client] }
16:   - { code: S1, name: valuation, published: [api], clientPackages: [] }
17:   - { code: S2, name: treatment, published: [api], clientPackages: [] }
18:   - { code: S3, name: guarantee, published: [api], clientPackages: [] }
19:   - { code: S4, name: litigation, published: [api], clientPackages: [] }
20:   - { code: S5, name: asset, published: [api], clientPackages: [] }
21:   - { code: S6, name: debtsale, published: [api], clientPackages: [] }
22:   - { code: S7, name: writeoff, published: [api], clientPackages: [] }
23:   - { code: S8, name: deviation, published: [api], clientPackages: [] }
24:   - { code: S9, name: partner, published: [api], clientPackages: [] }
25: external:
26:   - { name: common, rootPackage: th.co.scb.ace.demo.common, published: [api] }
27:   - { name: collection, rootPackage: th.co.scb.ace.demo.collection, published: [api] }
28: clientLibraries:
29:   - java.net.http
30:   - java.net.HttpURLConnection
31:   - java.net.Socket
32:   - java.net.URL
33:   - org.springframework.web.client
34:   - org.springframework.web.reactive.function.client
35:   - org.apache.hc
36:   - org.apache.http
37:   - okhttp3
38:   - com.jcraft.jsch
39:   - org.apache.sshd
40:   - net
... truncated (2,629 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Interesting things to check:

1. `PUBLISHED_PACKAGES` in RecoveryBoundaryTest is a hardcoded set which duplicates the map's published list. That's a duplication: the map already has published packages; the test hardcodes them separately. If the map gets a new published package, the published-surface test would silently skip it (not fail). That's "duplication that must change together" — a Should fix. Actually the published surface test only iterates over PUBLISHED_PACKAGES, so if the map declares a new published package, `actual` won't include it, and `containsExactlyInAnyOrderEntriesOf` compares only entries present... wait — it asserts actual equals the map of 6 entries. If a new published package appears in the map and has classes under it, but is not in PUBLISHED_PACKAGES, the actual map won't include it, so the assertion still passes — the new published type isn't checked. But the module map rule plus the Modulith test... The published surface test is meant to be an exact allow-list of published types, but coverage follows a hardcoded set, not the map. This is a real gap: a module could publish a new package with types and the published-surface test would not see it. However, `casewfNamedInterfacesAreTheSpecifiedBoundedSet` checks casewf's named interfaces are within a set, but only casewf. Still, that's a duplication issue, "must change together". Worth a Should fix with a concrete case: adding `comms.events` to the map's published list for a later story — the published surface test passes without listing its types.

Actually wait, would it fail? assertThat(actual).containsExactlyInAnyOrderEntriesOf(expected) — actual keys only from PUBLISHED_PACKAGES. If communication new package is not in PUBLISHED_PACKAGES, actual has no entry. Expected has none. Passes. So yes: a new published package's public types are never asserted. Hmm, but "publishedSurfaceIsExactlyTheSpecifiedTypes" name promises exactness. That's a real test gap with a concrete failing case (a leaked internal type in a new published package would not fail). But the module map rule would report if `@NamedInterface` present but not in published list — true, the moduleMap rule catches a published package not listed in the map. And if map lists it, moduleMap rule requires @NamedInterface. But the exact type list is not enforced for new packages. So a later story adding `comms.api` types wouldn't be caught by published-surface test unless they update the hardcoded set. It's a maintenance hazard

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff develop-recovery...feature/RWB-TE-001-module-boundary -- backend/build.gradle.kts"}
```

```text
diff --git a/backend/build.gradle.kts b/backend/build.gradle.kts
index 9c61bb3..7c4fd28 100644
--- a/backend/build.gradle.kts
+++ b/backend/build.gradle.kts
@@ -127,17 +127,25 @@ val e2eTest by tasks.registering(Test::class) {
 	systemProperty("rwb.e2e.oidcUrl", System.getenv("RWB_E2E_OIDC_URL") ?: "http://localhost:8090/entra")
 }
 
-// Coverage on recovery packages only, 80% line and branch (BS-7.2)
+// Coverage on recovery packages plus the test-scope boundary tooling, 80% on four counters
+// (BS-7.2; RWB-TE-001 SPEC-020). Fixtures and *Test classes are not measured.
 val recoveryClasses = files(sourceSets.main.get().output.classesDirs.map {
 	fileTree(it) { include("th/co/scb/ace/demo/recovery/**") }
 })
 
+val boundaryToolingClasses = files(sourceSets.test.get().output.classesDirs.map {
+	fileTree(it) {
+		include("th/co/scb/ace/demo/recovery/architecture/boundary/**")
+		exclude("**/*Test.class", "**/*Test$*.class")
+	}
+})
+
 val recoveryCoverageReport by tasks.registering(JacocoReport::class) {
-	description = "JaCoCo report for th.co.scb.ace.demo.recovery."
+	description = "JaCoCo report for th.co.scb.ace.demo.recovery and the boundary tooling."
 	group = "verification"
 	executionData(tasks.named("test").get())
-	classDirectories.setFrom(recoveryClasses)
-	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs)
+	classDirectories.setFrom(recoveryClasses, boundaryToolingClasses)
+	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs, sourceSets.test.get().java.srcDirs)
 	reports {
 		xml.required = true
 		xml.outputLocation = layout.buildDirectory.file("reports/jacoco/recoveryCoverageReport.xml")
@@ -146,15 +154,17 @@ val recoveryCoverageReport by tasks.registering(JacocoReport::class) {
 }
 
 val recoveryCoverageVerification by tasks.registering(JacocoCoverageVerification::class) {
-	description = "Fails below 80% line or branch coverage on recovery packages."
+	description = "Fails below 80% line, instruction, branch or method coverage on recovery packages and the boundary tooling."
 	group = "verification"
 	executionData(tasks.named("test").get())
-	classDirectories.setFrom(recoveryClasses)
-	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs)
+	classDirectories.setFrom(recoveryClasses, boundaryToolingClasses)
+	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs, sourceSets.test.get().java.srcDirs)
 	violationRules {
 		rule {
 			limit { counter = "LINE"; minimum = "0.80".toBigDecimal() 
... truncated (2,717 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\frontend\\src\\modules\\recovery\\__tests__\\importBoundary.test.ts"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\frontend\src\modules\recovery\__tests__\importBoundary.test.ts, lines 1-58
1: // @vitest-environment node
2: import { fileURLToPath } from "node:url";
3: import path from "node:path";
4: import { describe, it, expect, beforeAll } from "vitest";
5: import { ESLint } from "eslint";
6: 
7: // RWB-TE-001 SPEC-015, AC6 (T-TE001-07): the D-RCV-39 import allow-list lives in the real
8: // eslint.config.js. Each fixture is an in-memory source file under src/modules/recovery/, so the
9: // recovery block applies; no fixture file is written to disk.
10: const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../..");
11: const fixturePath = "src/modules/recovery/caselist/BoundaryFixture.tsx";
12: 
13: const rejected = [
14:   "@/modules/collection/worklist/WorkList",
15:   "../../collection/worklist/WorkList",
16:   "@/hooks/cfsc/x",
17:   "@/api/tdr/config",
18:   "@/pages/x",
19:   "@/utils/cfscCaseList",
20:   "@/modules/other/x",
21:   "../x",
22: ];
23: 
24: const allowed = [
25:   "@/components/ui/button",
26:   "@/lib/utils",
27:   "@/utils/date",
28:   "@/contexts/ApiClientContext",
29:   "@/api/schema",
30:   "@/modules/recovery/casewf/x",
31:   "./sibling",
32: ];
33: 
34: let eslint: ESLint;
35: 
36: async function restrictedMessages(specifier: string): Promise<number> {
37:   const source = `import value from "${specifier}";\nexport const used = value;\n`;
38:   const results = await eslint.lintText(source, { filePath: fixturePath });
39:   const result = results[0];
40:   if (!result) {
41:     throw new Error(`ESLint returned no result for ${specifier}`);
42:   }
43:   return result.messages.filter((message) => message.ruleId === "no-restricted-imports").length;
44: }
45: 
46: describe("D-RCV-39 import boundary", () => {
47:   beforeAll(() => {
48:     eslint = new ESLint({ cwd: frontendRoot });
49:   }, 30_000);
50: 
51:   it.each(rejected)("rejects %s", async (specifier) => {
52:     expect(await restrictedMessages(specifier)).toBe(1);
53:   });
54: 
55:   it.each(allowed)("allows %s", async (specifier) => {
56:     expect(await restrictedMessages(specifier)).toBe(0);
57:   });
58: }, 30_000);
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Notice `boundaryToolingClasses` excludes `**/*Test.class` and `**/*Test$*.class`, but the boundary package also contains `ModuleMap.class`, `ModuleMap$Module.class`, `ModuleMap$External.class`, `ModuleMapLoader.class`, `BoundaryRules.class` and many nested condition classes `BoundaryRules$...`. Those are measured. Good.

But wait — `boundaryToolingClasses` also picks up any class in that package that is test-scope but not `*Test` names. That's the tooling. Fine.

Potential issue: `boundaryToolingClasses` uses sourceSets.test output which includes the compiled test classes including fixture-generated? no, fixture package is different. Good.

However: coverage gate at 80% METHOD over main classes + tooling. Test time. Does the sourceDirectories addition of test sources affect anything? Only report source display.

A significant scale concern: importing all recovery classes once per test class instance. `RecoveryBoundaryTest` has `private final JavaClasses classes = ... importPackages(...)`. JUnit creates a new test instance per test method (default lifecycle PER_METHOD). This test class has 9 test methods; each creates a new instance → imports the recovery classes 9 times. ArchUnit import of a few hundred classes is maybe 100-300ms each; 9 × is ~1-3s. Not terrible, but there's also `ApplicationModules.of(...)` in one test. This is existing pattern? The original test may have had the same field; let me check the old version. Also `ModulithTest` separately. Not a "big slowdown" probably. But 9 imports per build vs 1 — a small win; "Nice to have". Let's see the original file.

Also check `ApplicationModules.of(AceRecoveryApplication.class)` in `casewfNamedInterfacesAreTheSpecifiedBoundedSet`: Modulith's automatic scanning of the whole `th.co.scb.ace.demo` application package requires scanning all classes including common/collection? It's already done in ModulithTest. Fine.

Let me read the whole BoundaryRulesTest, ModuleMapLoaderTest, and ModulithFixtureTest.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\boundary\\BoundaryRulesTest.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\boundary\BoundaryRulesTest.java, lines 1-261
1: package th.co.scb.ace.demo.recovery.architecture.boundary;
2: 
3: import static org.assertj.core.api.Assertions.assertThat;
4: 
5: import java.io.IOException;
6: import java.nio.file.Files;
7: import java.nio.file.Path;
8: import java.util.ArrayList;
9: import java.util.List;
10: import java.util.stream.Stream;
11: 
12: import com.tngtech.archunit.core.domain.JavaClass;
13: import com.tngtech.archunit.core.domain.JavaClasses;
14: import com.tngtech.archunit.core.importer.ClassFileImporter;
15: import com.tngtech.archunit.lang.ArchRule;
16: import com.tngtech.archunit.lang.EvaluationResult;
17: import org.junit.jupiter.api.Test;
18: 
19: /**
20:  * RWB-TE-001 T-TE001-02..-04, -09, -15 (SPEC-004..-010, BR1..BR6): every rule of the map-driven
21:  * boundary test fails on its breaking fixture world and passes on its passing fixture world.
22:  */
23: class BoundaryRulesTest {
24: 
25: 	private static final Path FIXTURES = Path.of("src/test/resources/architecture/fixtures");
26: 
27: 	private static final Path TOOLING = Path.of("src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary");
28: 
29: 	private static final String FIXTURE_ROOT = "th.co.scb.ace.boundaryfixture";
30: 
31: 	private static final String TOOLING_PACKAGE_LITERAL = "th.co.scb.ace.demo.recovery";
32: 
33: 	private static ModuleMap map(String name) {
34: 		return ModuleMapLoader.load(FIXTURES.resolve(name));
35: 	}
36: 
37: 	private static JavaClasses classes(String world) {
38: 		return new ClassFileImporter().importPackages(FIXTURE_ROOT + "." + world);
39: 	}
40: 
41: 	private static List<String> violations(ArchRule rule, String world) {
42: 		EvaluationResult result = rule.evaluate(classes(world));
43: 		return result.getFailureReport().getDetails();
44: 	}
45: 
46: 	private static String line(String code, String origin, String dependency, String module) {
47: 		return "Rule " + code + " broken: " + origin + " depends on " + dependency + ". Use " + module
48: 				+ ".api or an application event.";
49: 	}
50: 
51: 	@Test
52: 	void collectionInternalDependencyBreaksBnd1() {
53: 		List<String> lines = violations(BoundaryRules.bnd1(map("bnd1.yaml")), "bnd1");
54: 
55: 		assertThat(lines).containsExactlyInAnyOrder(
56: 				line("BND-1", "th.co.scb.ace.boundaryfixture.bnd1.recovery.case
... truncated (13,368 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Interesting: `toolingHoldsNoRecoveryPackageLiteral` scans only files directly in TOOLING dir, excluding names ending in "Test.java". BoundaryRulesTest is `*Test.java` excluded; ModuleMapLoaderTest excluded; BoundaryRules excluded. It would catch package literals in BoundaryRules.java and ModuleMap.java/Loader. Good.

Now the `mapViolationsAreAllReported` expects 8 lines exactly, including no violation for `casewf.events.CaseEvent` (public type in published...). Let's inspect fixture mapbad: `casewf` published includes `[api, events]`, and `events` has package-info with no @NamedInterface? The expected includes "published package ...casewf.events of module casewf has no @NamedInterface". But also events package has public types CaseEvent and CaseEventType moving? The module-map condition for published package `events` which has no @NamedInterface: it reports the "published package ... has no @NamedInterface" once. Then for CaseEvent (public type in events, not base package) no report. And `casewf.spi` has @NamedInterface but not in published → report; `casewf.timers` @NamedInterface propagate=true → report. Good.

Wait — the ordering of `report` dedupes with a Set; fine.

An important potential bug in ModuleMapCondition: `@NamedInterface` annotation on a package — `javaPackage.tryGetAnnotationOfType(NamedInterface.class)`. But `NamedInterface` is `@Target({ElementType.TYPE, ElementType.PACKAGE})`? In Spring Modulith 2.1.1, NamedInterface has `@Target({ ElementType.TYPE, ElementType.PACKAGE })` probably. For `package-info.java`, `@NamedInterface` on package, ArchUnit reads it. OK; tests pass in evidence presumably.

Now, the module map rule only checks that every *direct child* package of the root is a module base; it does not check that a module's subpackages are only api/internal or published. Not required.

Potential real bug: `ModuleMapCondition` reports "package X is not in the module map" based on direct child of root. But the root package `th.co.scb.ace.demo.recovery.architecture` — the tooling is test scope, imports DO_NOT_INCLUDE_TESTS in RecoveryBoundaryTest, so no. Fine.

Now, a key thing the prompt says: "thousands of classes scanned per build". The main risk is `RecoveryBoundaryTest` constructs `classes` per test method. Let me check the original file before the change to compare. Also check `ModulithTest`.

Next, examine relocation correctness: property split, PlatformConfig, SecurityConfig, RecoveryFlywayConfig, etc. Since these are behavior-p

_[truncated]_

</details>

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff develop-recovery...feature/RWB-TE-001-module-boundary -- \"backend/src/main/java/th/co/scb/ace/demo/recovery/integration\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/access\""}
```

```text
diff --git a/backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java b/backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java
new file mode 100644
index 0000000..2204bf2
--- /dev/null
+++ b/backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java
@@ -0,0 +1,71 @@
+package th.co.scb.ace.demo.recovery.access.api;
+
+import java.util.Map;
+
+/**
+ * Messages the platform raises itself, with the English and Thai text of the Error and Message
+ * Standard v4 section 4. The message table (reference data) is the source of record; story code
+ * reads its messages from there. These few are held here only because the platform must answer
+ * before any reference data is reachable (sign-in, permission, Temporal down).
+ *
+ * <p>Errors go out as {@code application/problem+json} with the API Specification v4
+ * {@code Problem} fields: type, title, status, detail, messageCode, messageTh, field, traceId.
+ */
+public enum ApiError {
+
+	/** E401: no valid session, or the person holds no Workbench role. */
+	NO_ROLE("MSG-P4-001", 401,
+			"You have no Recovery Workbench role. Ask your team manager to request one.",
+			"à¸„à¸¸à¸“à¸¢à¸±à¸‡à¹„à¸¡à¹ˆà¸¡à¸µà¸ªà¸´à¸—à¸˜à¸´à¹Œà¹ƒà¸Šà¹‰à¸‡à¸²à¸™ Recovery Workbench à¸à¸£à¸¸à¸“à¸²à¸•à¸´à¸”à¸•à¹ˆà¸­à¸œà¸¹à¹‰à¸ˆà¸±à¸”à¸à¸²à¸£à¸—à¸µà¸¡à¹€à¸žà¸·à¹ˆà¸­à¸‚à¸­à¸ªà¸´à¸—à¸˜à¸´à¹Œ"),
+
+	/** E403: the role lacks the right in the capability area. Placeholder {action}. */
+	NOT_PERMITTED("MSG-P4-002", 403,
+			"You cannot {action} here. Your role does not include it.",
+			"à¸„à¸¸à¸“à¹„à¸¡à¹ˆà¸ªà¸²à¸¡à¸²à¸£à¸–{action}à¹„à¸”à¹‰ à¹€à¸™à¸·à¹ˆà¸­à¸‡à¸ˆà¸²à¸à¸šà¸—à¸šà¸²à¸—à¸‚à¸­à¸‡à¸„à¸¸à¸“à¹„à¸¡à¹ˆà¸¡à¸µà¸ªà¸´à¸—à¸˜à¸´à¹Œà¸™à¸µà¹‰"),
+
+	/** E404: the record does not exist or is outside the caller's scope. */
+	NOT_IN_SCOPE("MSG-P4-003", 404,
+			"This case is not in your scope.",
+			"à¸à¸£à¸“à¸µà¸™à¸µà¹‰à¹„à¸¡à¹ˆà¸­à¸¢à¸¹à¹ˆà¹ƒà¸™à¸‚à¸­à¸šà¹€à¸‚à¸•à¸‡à¸²à¸™à¸‚à¸­à¸‡à¸„à¸¸à¸“"),
+
+	/** E503: the Temporal frontend is unreachable (RWB-E1-071). */
+	WORKFLOW_UNAVAILABLE("MSG-P3-036", 503,
+			"The workflow service is not available. Try again in a few minutes.",
+			"à¸£à¸°à¸šà¸šà¹€à¸§à¸´à¸£à¹Œà¸à¹‚à¸Ÿà¸¥à¸§à¹Œà¹„à¸¡à¹ˆà¸žà¸£à¹‰à¸­à¸¡à¹ƒà¸Šà¹‰à¸‡à¸²à¸™ à¸à¸£à¸¸à¸“à¸²à¸¥à¸­à¸‡à¹ƒà¸«à¸¡à¹ˆà¹ƒà¸™à¸­à¸µà¸à¹„à¸¡à¹ˆà¸à¸µà¹ˆà¸™à¸²à¸—à¸µ");
+
+	private final String messageCode;
+	private final int status;
+	private final String english;
+	private final String thai;
+
+	ApiError(String mess
... truncated (27,006 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Wait: the diff shows "new file" for these, meaning git didn't detect the rename in this filtered diff (filtering by path confuses rename detection). Fine.

Interesting: `SecurityConfig` moves `RecoverySecurityProperties` into `access.internal` and `SecurityConfig` is package-private. It references `ProblemFactory` which is package-private too. OK, same package.

But note SecurityConfig's `recoverySecurity` bean references `ProblemFactory` in signature — fine within same package.

Potential real issue: `ApiExceptionHandler` is package-private `@RestControllerAdvice`; previously also package-private in `platform.internal`. Component scan from `AceRecoveryApplication` in `th.co.scb.ace.demo` still finds package-private classes? Yes, Spring scans non-public classes? Spring's ClassPathScanningCandidateComponentProvider includes independent (non-static nested) concrete classes regardless of visibility, so package-private works.

Now, ApiExceptionHandler `forbidden` uses `Map.of("action", "do this")` — unchanged from before presumably.

Since this is a relocation, the diff mostly renames. What I need to verify is behavioral change in the moves and property split. Let's look at the diff for the workflow/config/migration files.

</details>

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff develop-recovery...feature/RWB-TE-001-module-boundary -- \"backend/src/main/java/th/co/scb/ace/demo/recovery/casewf\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/dochub\""}
```

```text
.function.Supplier;
+
+import io.grpc.Status;
+import io.grpc.StatusRuntimeException;
+import io.temporal.api.enums.v1.TaskQueueType;
+import io.temporal.api.taskqueue.v1.TaskQueue;
+import io.temporal.api.workflowservice.v1.DescribeNamespaceRequest;
+import io.temporal.api.workflowservice.v1.DescribeNamespaceResponse;
+import io.temporal.api.workflowservice.v1.DescribeTaskQueueRequest;
+import io.temporal.client.WorkflowClient;
+import io.temporal.client.WorkflowExecutionAlreadyStarted;
+import io.temporal.client.WorkflowOptions;
+import io.temporal.client.WorkflowServiceException;
+import io.temporal.serviceclient.WorkflowServiceStubs;
+import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
+import org.springframework.http.HttpStatus;
+import org.springframework.security.access.prepost.PreAuthorize;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.ResponseStatus;
+import org.springframework.web.bind.annotation.RestController;
+
+import th.co.scb.ace.demo.recovery.access.api.ApiError;
+import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
+import th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow;
+import th.co.scb.ace.demo.recovery.casewf.workflow.internal.TemporalProperties;
+import th.co.scb.ace.demo.recovery.casewf.workflow.WorkflowIds;
+
+/**
+ * Temporal operations, capability area Platform administration (module P3). Operational only: the
+ * case API never exposes workflow internals. Not registered when {@code rwb.p3.temporal} is off, so
+ * both paths return 404 (API Specification v4).
+ */
+@RestController
+@RequestMapping("/api/recovery/v1/admin")
+@ConditionalOnProperty(name = "rwb.p3.temporal", havingValue = "true")
+class TemporalAdminController {
+
+	private static final List<String> QUEUES = List.of(WorkflowIds.QUEUE_CASE, WorkflowIds.QUEUE_INTEGRATION,
+			WorkflowIds.QUEUE_PLATFORM);
+	private static final ZoneId BANK_ZONE = ZoneId.of("Asia/Bangkok");
+	private static final DateTimeFormatter YYYYMMDD = DateTimeFormatter.BASIC_ISO_DATE;
+
+	private final WorkflowServiceStubs stubs;
+	private final WorkflowClient client;
+	private final TemporalProperties properties;
+	private final Clock clock;
+
+	TemporalAdminController(WorkflowServiceStubs stubs, WorkflowClient client, TemporalProperties propert
... truncated (51,373 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

The diff was filtered and treated as new files, so I can't see what changed relative to old. Let me use `git diff -M` (rename detection is default on by default for full diff; but restricting pathspec caused only one side). Better: use `git diff --find-renames develop-recovery...feature -- <old path new path>`. Or `git show develop-recovery:path` compare. Let me look at the actual changed lines in key moved files using `git diff -M --stat` overall. Or use `git diff -M develop...feature` with no pathspec, then grep for changed chunks that are not pure renames.

Let me get the diff with rename detection and only show modified hunks. `git diff -M --diff-filter=M`.

</details>

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff -M --diff-filter=MR --stat develop-recovery...feature/RWB-TE-001-module-boundary -- \"backend/src/main/java\""}
```

```text
 .../recovery/{platform => access}/api/ApiError.java    | 10 +++++-----
 .../{platform => access}/api/ApiProblemException.java  |  2 +-
 .../internal/ApiExceptionHandler.java                  |  8 ++++----
 .../{platform => access}/internal/ProblemFactory.java  |  4 ++--
 .../{platform => access}/internal/SecurityConfig.java  | 18 ++++++++++--------
 .../admin}/TemporalAdminController.java                | 12 +++++++-----
 .../migration}/RecoveryFlywayConfig.java               |  8 +++++---
 .../api => casewf/rules}/CompiledRulePackage.java      |  2 +-
 .../internal => casewf/rules}/DroolsProperties.java    |  2 +-
 .../internal => casewf/rules}/DroolsRuleEngine.java    | 14 +++++++-------
 .../{rules/api => casewf/rules}/RuleEngine.java        |  2 +-
 .../{rules/api => casewf/rules}/RuleInput.java         |  2 +-
 .../{rules/api => casewf/rules}/RuleOutcome.java       |  2 +-
 .../{rules/api => casewf/rules}/RuleResult.java        |  2 +-
 .../api => casewf/timers}/TimerScheduler.java          |  2 +-
 .../timers}/internal/QuartzTimerScheduler.java         |  4 ++--
 .../{workflow/api => casewf/workflow}/WorkflowIds.java |  2 +-
 .../workflow/internal/PdpaPayloadCodec.java            |  6 +++---
 .../workflow/internal/PlatformSmokeWorkflow.java       |  2 +-
 .../{ => casewf}/workflow/internal/TemporalConfig.java |  4 ++--
 .../workflow/internal/TemporalProperties.java          |  4 ++--
 .../{documents => dochub}/api/DocumentStore.java       |  2 +-
 .../internal => dochub/storage}/BlobDocumentStore.java |  4 ++--
 .../flags}/api/RecoveryFlags.java                      |  2 +-
 .../internal/PlatformInfoController.java               | 15 +++++++++++----
 25 files changed, 74 insertions(+), 61 deletions(-)

```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff -M develop-recovery...feature/RWB-TE-001-module-boundary -- \"backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/ApiExceptionHandler.java\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/SecurityConfig.java\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/admin/TemporalAdminController.java\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/integration/internal/PlatformInfoController.java\""}
```

```text
diff --git a/backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java b/backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java
new file mode 100644
index 0000000..2204bf2
--- /dev/null
+++ b/backend/src/main/java/th/co/scb/ace/demo/recovery/access/api/ApiError.java
@@ -0,0 +1,71 @@
+package th.co.scb.ace.demo.recovery.access.api;
+
+import java.util.Map;
+
+/**
+ * Messages the platform raises itself, with the English and Thai text of the Error and Message
+ * Standard v4 section 4. The message table (reference data) is the source of record; story code
+ * reads its messages from there. These few are held here only because the platform must answer
+ * before any reference data is reachable (sign-in, permission, Temporal down).
+ *
+ * <p>Errors go out as {@code application/problem+json} with the API Specification v4
+ * {@code Problem} fields: type, title, status, detail, messageCode, messageTh, field, traceId.
+ */
+public enum ApiError {
+
+	/** E401: no valid session, or the person holds no Workbench role. */
+	NO_ROLE("MSG-P4-001", 401,
+			"You have no Recovery Workbench role. Ask your team manager to request one.",
+			"à¸„à¸¸à¸“à¸¢à¸±à¸‡à¹„à¸¡à¹ˆà¸¡à¸µà¸ªà¸´à¸—à¸˜à¸´à¹Œà¹ƒà¸Šà¹‰à¸‡à¸²à¸™ Recovery Workbench à¸à¸£à¸¸à¸“à¸²à¸•à¸´à¸”à¸•à¹ˆà¸­à¸œà¸¹à¹‰à¸ˆà¸±à¸”à¸à¸²à¸£à¸—à¸µà¸¡à¹€à¸žà¸·à¹ˆà¸­à¸‚à¸­à¸ªà¸´à¸—à¸˜à¸´à¹Œ"),
+
+	/** E403: the role lacks the right in the capability area. Placeholder {action}. */
+	NOT_PERMITTED("MSG-P4-002", 403,
+			"You cannot {action} here. Your role does not include it.",
+			"à¸„à¸¸à¸“à¹„à¸¡à¹ˆà¸ªà¸²à¸¡à¸²à¸£à¸–{action}à¹„à¸”à¹‰ à¹€à¸™à¸·à¹ˆà¸­à¸‡à¸ˆà¸²à¸à¸šà¸—à¸šà¸²à¸—à¸‚à¸­à¸‡à¸„à¸¸à¸“à¹„à¸¡à¹ˆà¸¡à¸µà¸ªà¸´à¸—à¸˜à¸´à¹Œà¸™à¸µà¹‰"),
+
+	/** E404: the record does not exist or is outside the caller's scope. */
+	NOT_IN_SCOPE("MSG-P4-003", 404,
+			"This case is not in your scope.",
+			"à¸à¸£à¸“à¸µà¸™à¸µà¹‰à¹„à¸¡à¹ˆà¸­à¸¢à¸¹à¹ˆà¹ƒà¸™à¸‚à¸­à¸šà¹€à¸‚à¸•à¸‡à¸²à¸™à¸‚à¸­à¸‡à¸„à¸¸à¸“"),
+
+	/** E503: the Temporal frontend is unreachable (RWB-E1-071). */
+	WORKFLOW_UNAVAILABLE("MSG-P3-036", 503,
+			"The workflow service is not available. Try again in a few minutes.",
+			"à¸£à¸°à¸šà¸šà¹€à¸§à¸´à¸£à¹Œà¸à¹‚à¸Ÿà¸¥à¸§à¹Œà¹„à¸¡à¹ˆà¸žà¸£à¹‰à¸­à¸¡à¹ƒà¸Šà¹‰à¸‡à¸²à¸™ à¸à¸£à¸¸à¸“à¸²à¸¥à¸­à¸‡à¹ƒà¸«à¸¡à¹ˆà¹ƒà¸™à¸­à¸µà¸à¹„à¸¡à¹ˆà¸à¸µà¹ˆà¸™à¸²à¸—à¸µ");
+
+	private final String messageCode;
+	private final int status;
+	private final String english;
+	private final String thai;
+
+	ApiError(String mess
... truncated (22,006 chars total)
```

### Assistant - 2026-11-18 09:25 | opencode-go/deepseek-v4.1-flash | general
