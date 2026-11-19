# Decision register

The single index of decisions that bind this repository. Source decisions come from the
client's Decision Log v10; squad decisions from the recovery tech lead; local build decisions from
the 16 November 2026 re-baseline. Where a later decision conflicts, the later one wins and the
earlier one is marked superseded.

## Numbering and precedence

| Rule | Value |
|---|---|
| Source decisions | `DT01`–`DT22` (programme) and `D-RCV-29`–`D-RCV-36` (client rulings) |
| Squad decisions | `D-RCV-01`–`D-RCV-50`, with `D-RCV-35`→`D-RCV-51` and `D-RCV-36`→`D-RCV-52` |
| Local build decisions | `L-RCV-01` onward, this repository only |
| Precedence | Client Decision Log v10 and the 15–16 Nov change registers > squad decisions > local build decisions |
| Conflict rule | The later dated decision wins; the superseded row stays for history and names its successor |

## Client decisions from Decision Log v10

| ID | Decision | Status |
|---|---|---|
| `DT01` | The foundation spans Epic 1 and Epic 2; DevOps and infrastructure are a Sprint 0 checklist. | Active |
| `DT02` | Every rule, limit, threshold, template, name, queue, role, timer and route is versioned data. | Active; rules now evaluated by Drools (D-RCV-36) |
| `DT03` | Reordered epic plan with litigation earlier; eight monthly releases. | Active |
| `DT04` | Delivery runs as Kanban; the two-point is a sponsor review. | Active |
| `DT05` | Epic design sign-off runs in parallel with the current epic's build. | Active |
| `DT06` | The Workbench builds its own document management; the document hub is the system of record. | Active |
| `DT07` | Build on ACE: one service, one repository, one front end. | Active |
| `DT08` | Modular monolith: collection, recovery and common modules with build-time boundaries. | Active |
| `DT09` | No Temporal. | **Superseded by D-RCV-36 (T1)** |
| `DT10` | CMMN 1.1 is the standard case vocabulary. | Active for terms; Temporal runs the lifecycle |
| `DT11` | Document storage is in scope. | Active |
| `DT12` | Data through COLLINS. | **Superseded by D-RCV-35 (U1)** |
| `DT13`–`DT22` | The remaining programme decisions (release cadence, environments, security, AI governance, data retention, partners, reporting, change control, benefits). | Active unless a D-RCV decision says otherwise |

| ID | Decision | Status |
|---|---|---|
| `D-RCV-29` | Epic 1 baseline V0001 seeds the full recovery dictionary (122 objects, 1,366 fields in Physical Schema v6). | Active |
| `D-RCV-30` | Primary account rule on `case_account.is_primary`. | Active |
| `D-RCV-31` | Legal-document storage after type confirmation. | Active |
| `D-RCV-32` | P9 baseline measure definitions for MD-2026.11. | Active |
| `D-RCV-33` | Intake-agent promotion grammar. | Active |
| `D-RCV-34` | Migration sequence follows the merge-order map; the real sequence is taken at merge. | Active |
| `D-RCV-35` | **ACE DB alignment (U1–U5):** no inbound source loads; ACE owns source data; Workbench extension tables; read-only `recovery.v_ace_*` views; Excel/SharePoint trackers leave scope. | **Active; supersedes D-RCV-03, -17, -47 and DT12** |
| `D-RCV-36` | **Temporal and Drools (T1–T10):** case workflows on Temporal from Epic 3; Quartz/Spring Batch stay for Epic 1–2 jobs; embedded Drools from versioned rule packages; retire E1-029, TE-005, E1-048. | **Active; supersedes ADR-003/004, DT02's mechanism, DT09, DT10's workflow wording** |

## Squad decisions carried from the 4–10 November 2026 register

| ID | Decision | Status |
|---|---|---|
| `D-RCV-01` | Recovery API follows API Specification v2 (`/api/recovery/v1`, plain JSON, uuid, MSG codes) as an exception to the ACE HAL rule | Active |
| `D-RCV-02` | One Spring Modulith application module `recovery` (`th.co.scb.ace.demo.recovery`); the 19 design modules are nested application modules with `api` / `internal` packages per the RWB-TE-001 module map | Active |
| `D-RCV-03` | Own database schema `recovery`, referenced only through `${recoverySchema}` | Superseded by D-RCV-35 / ADR-010 |
| `D-RCV-04` | DL42 option A: `V<epic>_<story>__<name>.sql` with `${recoverySchema}`, in `backend/src/main/resources/db/modulemigration/recovery/` with the module's own Flyway bean and history table; RWB-E1-044 adjusted to match | Active |
| `D-RCV-05` | Gap report #30–32: no pipeline change. Migration lint, module boundary and module-map checks run as unit tests in the existing build; the drift check against real environments moves to the parking lot | Active |
| `D-RCV-06` | Coverage: JaCoCo for recovery backend packages and Vitest + Testing Library for the recovery frontend folder, 80% gate on recovery code only | Active |
| `D-RCV-07` | Recovery integration and migration tests use Testcontainers PostgreSQL; existing ACE tests keep H2 | Active |
| `D-RCV-08` | Recovery screens use the ACE design system (components and tokens); Henka Screen Specifications give layout, content, labels and behaviour | Active |
| `D-RCV-09` | Playwright MCP allowed origins follow ACE local ports: frontend 5173, backend 8080 | Active |
| `D-RCV-10` | Recovery frontend folder `frontend/src/modules/recovery/` | Active |
| `D-RCV-11` | RWB-TE-001 boundary rules: Spring Modulith `verify()` for nested modules plus ArchUnit for BND-4, BND-5 and the module-map check (test dependency) | Active |
| `D-RCV-12` | (Re-confirmed by the squad 2026-11-05, question A9.) RWB-E1-044 parts that need P1 job store and monitor (`MigrationRunRecorder`, `GET /api/recovery/v1/admin/jobs`, SCR-44) are deferred to the story that builds the job monitor | Active |
| `D-RCV-13` | Recovery UI supports Thai and English through i18next; default language Thai. Decided by FDA, 2026-11-05 | Active |
| `D-RCV-14` | Sending SCB documents and ACE source code to the approved AI service (Claude), and keeping the converted corpus in the shared `ace-aisdlc` repository, is permitted. Approved by Pongchai Charoenrungrodkun, 2026-11-05 | Active |
| `D-RCV-15` | Jesniphat Pukkham approves the FDE/FDA gates (context readiness, design and architecture, plan, task, PR, release readiness) for EPIC-001, INC-001 and INC-002 on behalf of the squad. Product Owner gates (intake, requirements, backlog and specification, depl... | Active |
| `D-RCV-16` | Acceptance for RWB-E1-044 and RWB-TE-001, whose acceptance criteria BA removed on 4 Nov 2026, is the story business rules (BR*) plus the test cases left in each story file | Active |
| `D-RCV-17` | Superseded by D-RCV-47. Recovery schema is `recovery` in every environment, always referenced through `${recoverySchema}`. Decided by Jesniphat Pukkham, recovery tech lead, 2026-11-05 | Superseded by D-RCV-47, then by D-RCV-35 |
| `D-RCV-18` | DL42 option A confirmed for the recovery module: `V<epic>_<story>__<name>.sql`, `${recoverySchema}`, `backend/src/main/resources/db/modulemigration/recovery/`, the module's own Flyway bean and history table following ACE `samplemodule`; ACE core Flyway (`Ap... | Active |
| `D-RCV-19` | RWB-TE-001 boundary rules are named BND-1..BND-5 (not R-BND). BND-1 and BND-2 (`collection`, `common`) are written now as ArchUnit rules with `allowEmptyShould(true)` so they pass until those packages exist and fail as soon as a violation appears. Decided b... | Active |
| `D-RCV-20` | Cross-module calls inside recovery go through the callee's published interface (gateway) in its `api` package, injected by interface type; a module never injects or calls another module's `internal` class, entity or repository. Application events are not th... | Active |
| `D-RCV-21` | Code owners of `th.co.scb.ace.demo.recovery` and `frontend/src/modules/recovery/` are the recovery tech lead plus the squad developers, set up in RWB-TE-002. Decided by Jesniphat Pukkham, recovery tech lead, 2026-11-05 | Active |
| `D-RCV-22` | Recovery screens live under the route prefix `/recovery/*` with one "Recovery" menu group in `AceLayout`; the `App.tsx` / `AceLayout.tsx` edits are shared-file changes announced to the ACE team. Decided by Jesniphat Pukkham, recovery tech lead, 2026-11-05 | Active |
| `D-RCV-23` | Frontend cross-area imports are blocked with ESLint `no-restricted-imports` scoped to `frontend/src/modules/recovery/`; functional UI tests use Playwright (toolkit Functional Automation Test); ACE's existing Selenium + Cucumber suite is left as is. Decided... | Active |
| `D-RCV-24` | Superseded by D-RCV-28. The recovery Flyway bean runs with `outOfOrder(true)` (recovery bean only; ACE core unchanged), because option A versions follow story numbers while the build order does not (e.g. E1-042 before E1-001). Duplicate versions are caught... | Superseded by D-RCV-28 |
| `D-RCV-25` | Superseded by D-RCV-28. A migration file name that breaks option A is reported by the lint test but does not fail the build. The epic number for RWB-TE-* migrations is still open. Decided by Jesniphat Pukkham, recovery tech lead, 2026-11-05 | Superseded by D-RCV-28 |
| `D-RCV-26` | Superseded by D-RCV-28. The literal-schema lint is a unit test that scans `db/modulemigration/recovery/*.sql` with a regex: no `recovery.`, `"recovery".`, `rwb_case.` or `public.` prefixes; `${recoverySchema}` is required. No database is needed. Decided by... | Superseded by D-RCV-28 |
| `D-RCV-27` | Superseded by D-RCV-28. Recovery Testcontainers tests use `@Testcontainers(disabledWithoutDocker = true)`: they are skipped where Docker is missing, so the shared ACE build stays green, and they run wherever Docker exists. Whether the build agents have Dock... | Superseded by D-RCV-28 |
| `D-RCV-28` | RWB-E1-044 spec gate rulings (supersede D-RCV-24, the file-name part of D-RCV-18 and D-RCV-25, D-RCV-26, D-RCV-27). (1) Migration file names are `V<seq>__<story>_<name>.sql`: `<seq>` a 4-digit zero-padded sequence in merge order (renumber before merge on a... | Active |
| `D-RCV-34` | Recovery migration sequence numbers follow the build order in `docs/architecture/migration-merge-order-map.md` (Build Sequence Epic 1 and Epic 2 v4). RWB-E1-042 (build order 3) takes `V0001` and `V0002`; RWB-E1-001 (build order 10) takes `V0003__rwb_e1_001_... | Active |
| `D-RCV-51` | The canonical version of each story is the most recently issued one by issue or edit date, not the highest version number. Under the v2 baseline the current sets are Epic 1 story files v7 and Epic 2 v5. | Active |
| `D-RCV-52` | RWB-TE-001 builds only the recovery module skeleton and the build-time boundary checks; it ships no runtime code. `RecoveryAccessGuard` (the common access check INT-34, 403 MSG-P4-002) and TC-TE-001-08 move to RWB-E1-022. | Active |
| `D-RCV-37` | The recovery module map is `backend/src/test/resources/architecture/recovery-modules.yaml` in the ACE repository: read only by the boundary tests, not packaged in the deployed jar. Decided by Jesniphat Pukkham, recovery tech lead, 2026-11-09 | Active |
| `D-RCV-38` | Boundary rule BND-4: a recovery class may use only its own module's entities (`@Entity`) and repositories (Spring Data `Repository` subtypes). Every other entity and repository is forbidden, ACE's `th.co.scb.ace.demo.model..` and `..repository..` included;... | Active |
| `D-RCV-39` | Frontend import rule for `frontend/src/modules/recovery/` (ESLint `no-restricted-imports`, matched on import text). Allowed outside the folder: `@/components/ui/` (D-RCV-08), `@/lib/utils`, top-level `@/utils/*` except `cfsc*`, `@/contexts/ApiClientContext`... | Active |
| `D-RCV-40` | Unit-test coverage for RWB-TE-001 is measured natively. Frontend: Vitest with an ESLint Node-API fixture test, `@vitest/coverage-v8` on `src/modules/recovery/` at 80%; a `test` target joins frontend `check` (wiring per D-RCV-43). Backend: JaCoCo recovery-on... | Active |
| `D-RCV-41` | Module map values until the ACE team names them: collection root `th.co.scb.ace.demo.collection`, published `[api]` (common stays as story §3). Client libraries for BND-5: `java.net.http`, `java.net.HttpURLConnection`, `java.net.Socket`, `java.net.URL`, `or... | Active |
| `D-RCV-42` | BND-3 (recovery module to recovery module) is enforced by Spring Modulith `verify()` in the existing `ModulithTest`, with Modulith's own failure text (accepted deviation from story §14) and its cycle check. The module-map rule keeps `@NamedInterface` on `pa... | Active |
| `D-RCV-43` | RWB-TE-001 coverage wiring. (1) ACE runs Nx 24.0.3, where `@nx/vite/plugin` infers no `test` target; the frontend `test` target (`vitest run --coverage`) is hand-defined in `frontend/package.json` `nx.targets` and added to `check`; `@nx/vitest` is not regis... | Active |
| `D-RCV-44` | Recovery Testcontainers tests (`@Tag("recovery-it")`) stay in `recoveryIntegrationTest`, outside `check` (no pipeline change, D-RCV-05). They must run before every MR that touches recovery migrations (`db/modulemigration/recovery/`) or `RecoveryFlywayConfig... | Active |
| `D-RCV-45` | The recovery Flyway bean is disabled whenever profile `db-migrate` is active without `db-migrate-recovery`, whatever `spring.flyway.enabled` says, so the core `db-migrate` Jenkins step never runs recovery migrations or creates schema `recovery`; a test prov... | Active |
| `D-RCV-46` | Chitchaya Muanchonchana (Internal PO TechX) is the Product Owner for Recovery stories in Jira `TB0001` and holds the Product Owner gates (intake, requirements, backlog and specification, deployment). Decided by Jesniphat Pukkham, recovery tech lead, 2026-11-09 | Active |
| `D-RCV-47` | Recovery tables live in the ACE schema `ace` (the connection's `currentSchema`), not in a schema of their own, following the ACE sample-module pattern: own Flyway bean, own folder `db/modulemigration/recovery/`, own history table `flyway_schema_history_reco... | **Superseded by D-RCV-35 / ADR-010** |
| `D-RCV-48` | The recovery Flyway bean sets `baselineVersion("0")` and `baselineOnMigrate(true)`, as ACE `SampleModuleConfig`, because schema `ace` is not empty (ACE core tables and history tables): the first recovery migrate finds no `flyway_schema_history_recovery` on... | Active |
| `D-RCV-49` | RWB-E1-044 plan preconditions PRE-3 and PRE-4 are approved by the recovery tech lead and do not wait for an ACE reply. PRE-3 (OPEN-030): the new test dependency `org.testcontainers:testcontainers-postgresql` (Spring Boot 4.2.0-M2 BOM, 2.0.5), the test-scope... | Active |
| `D-RCV-50` | Recovery code in ACE goes through the integration branch `develop-recovery`, agreed with the ACE team: story branches `feature/<JIRA-KEY>-<slug>` are cut from `develop-recovery`, and story MRs target `develop-recovery`; the recovery tech lead approves and m... | Active |

## Local build decisions (16 November 2026)

| ID | Decision | Rationale |
|---|---|---|
| `L-RCV-01` | A new repository `17 AI-First SDLC Repository v2` is built from document set v14; the old `13 AI-First SDLC repository` is not edited. | The document set changed materially; a side-by-side baseline keeps the old evidence readable. |
| `L-RCV-02` | The new repository uses the toolkit's generated Claude Code subagents in `.claude/agents/` plus the requirement commands. | The user asked for the new AISDLC Claude agents; generated files stay in sync with `.github/agents/`. |
| `L-RCV-03` | No stage asks the user a question during this rebuild. Ambiguities are resolved with the most defensible default and logged in the run's `assumptions.md`. | The user asked for no questions in the context, specify and plan phases. |
| `L-RCV-04` | `RWB-E1-042` and `RWB-TE-001` are the preserved implemented stories. Their code/evidence is carried forward and their spec/plan are re-run against the new baseline. | They are the two stories with implementation evidence in the current workstream. |
| `L-RCV-05` | `RWB-E1-044` and `RWB-E1-043` keep their 10 November specs and plans as historical artefacts; they are marked for re-baseline before build. | Their schema basis changed under D-RCV-35; silently editing them would hide the change. |
| `L-RCV-06` | The 10 removed/retired stories are recorded, not rebuilt. Their old specs move to `output/_archive/` with a retirement note. | D-RCV-35 and D-RCV-36 retire the work; keeping it as current output would mislead the build. |
| `L-RCV-07` | The schema is `recovery`, referenced only as `${recoverySchema}`; migration names follow D-RCV-28. | Physical Schema v6 and E1-069 are the current source; D-RCV-47 is superseded. |
| `L-RCV-08` | Temporal and Drools are allowed only as ADR-011/ADR-012 define them, behind flags `rwb.p3.temporal` and `rwb.p3.drools`. | D-RCV-36 and `AGENTS.md`. |
| `L-RCV-09` | The specification and plan runs are `RWB-E1-042` (INC-003) and `RWB-TE-001` (INC-002); `RWB-E1-069` and `RWB-E1-044` get a specification-readiness note, not a full spec, in this run. | Scope control: the two implemented stories are the ones the user asked to preserve and run. |
| `L-RCV-10` | Story cards are numbered by Build Sequence v6 order, 1–72. | One stable mapping from card to run and build order. |

## Supersession map

| Superseded | By |
|---|---|
| ADR-003 (no workflow engine) | ADR-011 (Temporal) |
| ADR-004 (rules as rows) | ADR-012 (embedded Drools packages; principle of versioned rules kept) |
| DT09 (no Temporal) | D-RCV-36 T1 |
| DT12 (COLLINS batch load) | D-RCV-35 U1 |
| D-RCV-03 / D-RCV-17 / D-RCV-47 (schema `ace`, `rwb_` prefix) | D-RCV-35 U3 + ADR-010 (schema `recovery`, `${recoverySchema}`) |
| D-RCV-24–27 (early Flyway rulings) | D-RCV-28 |
| `RWB-E1-029`, `RWB-TE-005`, `RWB-E1-048` | `RWB-E1-073`, `RWB-E2-041` (D-RCV-36 T8) |

## Detailed decision text

- Squad decisions, full text: `docs/decisions/INC-001-decisions.md`.
- Client Decision Log v10: `docs/decisions/source-decision-log.md` and the CSV extracts in `requirement/legacy/01-decisions-and-governance/_csv/`.
- ACE DB alignment register: `docs/decisions/d-rcv-35-ace-db-alignment.md`.
- Temporal and Drools register: `docs/decisions/d-rcv-36-temporal-and-drools.md`.
- API style exception: `docs/architecture/decisions/ADR-RCV-001-recovery-api-style.md`.
