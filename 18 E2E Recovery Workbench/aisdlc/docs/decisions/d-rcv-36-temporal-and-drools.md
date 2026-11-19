<!-- working-copy-of: requirement/legacy/16-temporal-and-drools-adoption/recovery-workbench-temporal-and-drools-change-register-v1.md -->
> **Working copy.** Canonical source: `requirement/legacy/16-temporal-and-drools-adoption/recovery-workbench-temporal-and-drools-change-register-v1.md`. Edit the source, not this copy.

# Recovery Workbench Temporal and Drools change register

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Document | Recovery Workbench Temporal and Drools Change Register v1 |
| Purpose | The decision record and the edit plan for running the case lifecycle on Temporal and evaluating rules with embedded Drools from versioned rule packages |
| Status | Signed off on 16 November 2026 (T1 to T10). Phase 1 in delivery |
| Decisions | T1 to T10, recorded as D-RCV-36 |
| Decision owner | Recovery tech lead with the solution architect; SCB IT and the ACE team for the Temporal platform |
| Supersedes | ADR-003 (by ADR-011) and ADR-004 (by ADR-012); DT02, DT09 and DT10 |
| Scope | 11 new stories, 3 retired stories, 13 rewritten stories, 8 stories with a reference update, 2 ADRs, 1 decision, 3 messages, 26 new field IDs, 7 new endpoints |
| Sources examined | ADR v2; Decision Log v9; Epic 1 v8.md; Epic 2 v6.md; Technical Enabler Stories v6.md; Administration Stories v3.md; Rules Engine Design v2; Workflow Engine Design v2; Batch and Scheduling Design v3; API Specification v3; Physical Schema v5; LDM v7; Error and Message Standard v3; the three retired story files |

**Phase 1: Epic 1 and Epic 2 only.** Epics 3 to 8 are phase 2, and nothing in this register builds them.

## 1. Why this change

The design runs the case lifecycle in code and holds the rules as rows in five rule tables. ADR-003 said no workflow engine and named Temporal as out of scope. ADR-004 said no rules engine, with a home-built decision-table component.

Three things changed.

- **The waits.** A recovery case lives for months or years and waits on people, partners and courts. 366 of the 448 routing rules move a case to a state that a person or a partner owns. The timers, retries and multi-step chains that move it are built by hand: rows in `timer`, JOB-05 to check them, Spring Batch chains and an outbox. Every one of them is code the squads maintain.
- **The rules.** RW-COE authors rules in an Excel template that the Workbench parses into `rule_row`, then checks, tests and rolls back with a home-built loader. Each new shape of condition or output is a code change, and the evaluator, the load checks and the rule tests are all built by the squads.
- **The platform.** SCB IT has accepted a self-hosted Temporal cluster on the ACE AKS clusters, and Drools is approved as an embedded library. The Workbench can use both without leaving ACE, and both are open source with a pinned version.

D-RCV-36 records the change. ADR-011 supersedes ADR-003, and ADR-012 supersedes ADR-004 and keeps its principle that rules are versioned data.

What stays:

| Thing | Where it stays |
|---|---|
| Case data | The ACE database recovery schema. Temporal holds no case of record |
| Rules as versioned data | A rule package version is a row with a workbook, the generated DRL, a checksum and a valid-from date |
| Quartz and Spring Batch | Every Epic 1 and Epic 2 scheduled job, including JOB-05 behind the TimerScheduler port |
| One service, one repository | The recovery module of ACE (ADR-001, ADR-002) |
| The decision log | One entry per decision, with rule ID and package version, written before the action |

What changes:

| Thing | From | To |
|---|---|---|
| Case lifecycle | Code, `timer` rows, JOB-05 | Temporal, one workflow per case, from Epic 3 |
| Rule authoring | Excel template parsed into `rule_row` | Drools XLS workbook compiled to a KieBase and stored as a package version |
| Rule evaluation | Home-built decision-table component | Embedded Drools through `RuleEvaluator` |
| Rule change | Load, approve, rollback by call | Upload, compile, check, scenarios, approve, dated start, rollback by one call |
| Payment matching | `payment_match_rule` | Package PAYMENT_MATCH |

## 2. The ten decisions T1 to T10

| # | Decision |
|---|---|
| T1 | Temporal, hybrid. Case data stays the system of record in the ACE DB recovery schema. Temporal runs the case lifecycle from Epic 3: one workflow per case, plus durable timers, retries and automated multi-step chains. Self-hosted on the shared ACE AKS clusters in the ACE namespace. |
| T2 | Quartz and Spring Batch stay for every Epic 1 and Epic 2 scheduled job (JOB-03 allocation, JOB-04 reconciliation, JOB-05 timer check, JOB-06 rebalance, JOB-07, JOB-08 and the rest). JOB-05 runs behind a new TimerScheduler port so that Epic 3 can swap in Temporal durable timers without changing callers. Temporal Schedules are not used in Epics 1 and 2. |
| T3 | Drools is embedded in the recovery module (KIE runtime libraries only: drools-engine, drools-mvel, drools-decisiontables, drools-xml-support). There is no KIE Server, no Business Central and no KJAR in Maven. |
| T4 | No release for a rule change. RW-COE writes each rule package as an Excel workbook in Drools XLS decision-table format. On upload the workbook is compiled to a KieBase, checked and run against scenarios, then stored as a rule_package_version row with the workbook, the generated DRL and a checksum. RW-RISK approves it, and the author cannot approve. It is in force from its valid-from date, and rollback is one call. |
| T5 | First match semantics are kept. Each decision table has RuleSet = package code. Each row is one rule whose NAME is the rule ID (for example ALLOC-031). Rows share one activation-group, and salience is derived from row order, so exactly one row decides. The default row is last. The decision log records rule ID = Drools rule name and rule version = package version label. The existing decision_log_entry.rule_id / rule_version columns are kept, with no schema change. |
| T6 | rule_row stays as the rule catalog: the parsed, queryable copy of each row, linked to its package version, with outputs jsonb. Stories read action_text, owner_role, timer_spec and target_queue_code from the catalog by rule ID and version. They do not read the package source. |
| T7 | Determinism. Temporal workflows call Drools only inside an activity. The rule package version is chosen at evaluation time, returned in the result, and written to the decision log. |
| T8 | Retire RWB-E1-029, RWB-TE-005 and RWB-E1-048. Their new homes are E1-073 (for E1-029 and TE-005) and E2-041 (for E1-048). |
| T9 | Rewrite the stories whose behaviour or design changes. Give a reference update to stories that only cite a retired story, the "rules component" or Quartz in wording (section 4). |
| T10 | payment_match_rule is dropped. Payment matching becomes Drools package PAYMENT_MATCH, whose rows carry match type, tolerance, window, grace and partial floor as decision-table columns. |

## 3. Target runtime

### 3.1 Temporal platform facts

| Item | Value |
|---|---|
| Clusters | One Temporal cluster per environment (DEV, SIT, UAT, PROD), on the ACE AKS clusters, deployed with the official Temporal Helm chart. Server and Java SDK versions are pinned to the release SCB IT approves at build; the approved version is recorded in Environment and Deployment Design v4. |
| Persistence | Databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server, owned by role temporal_svc. temporal_svc has no grant on the ACE database, and recovery_svc has no grant on the Temporal databases. |
| Namespace | rwb-recovery in each cluster (ace-collection reserved for the ACE team). |
| Task queues | rwb-case (case workflows, Epic 3+), rwb-integration (multi-step outbound chains, Epic 3+), rwb-platform (smoke and health workflows, Epic 1). |
| Workflow IDs | case-{caseId} (for example case-RW-2026-000123); platform-smoke-{yyyymmdd}. |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode (Keyword). No personal data. |
| Payloads | Encrypted by the PdpaPayloadCodec (AES-GCM, key in Azure Key Vault). History never holds clear personal data. |
| Retention | 30 days for closed workflows (assumed; confirmed with DL26). Archive to Blob in E2-039. |
| Access | Temporal Web UI behind Entra ID OIDC: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode through the codec server (break-glass, logged). mTLS between worker, frontend and internal services. |
| Worker identity | SY-CASEWF (case workflows), SY-RULES (Drools evaluator). |
| Feature flags | rwb.p3.temporal (worker on or off), rwb.p3.drools (rule package endpoints). With either flag off, the endpoints return 404 and nothing else changes. |
| Parameters (through RWB-E1-042) | temporal.target, temporal.namespace, temporal.taskqueue.platform, temporal.retention.days=30, drools.kiebase.cache.max=20, rules.testcases.min=50. |

### 3.2 Packages in Phase 1

The `rule_package.package_code` values:

| Epic | Package | Rules | Used by |
|---|---|---|---|
| 1 | ENTRY, EXCLUSION | entry and exclusion rows (DL24) | E1-018 |
| 1 | ALLOCATION, ASSIGNMENT | allocation and assignment rows (DL24) | E1-020, E1-030 |
| 1 | TRANSFER | transfer rows (DL24) | E1-021, E2-012 |
| 2 | RESTRUCTURE | R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31, R-LIT-02, and the route-set rows with action_text, owner_role and timer_spec that E2-035 reads | E2-002, E2-004, E2-035 |
| 2 | PAYMENT_MATCH | EXACT, PARTIAL, WINDOW (R-RES-26) | E2-008, E2-027 |
| 2 | BOOKING_MATCH | booking match rows (today's BookingMatchRules) | E2-007 |

Eight package codes across the six rows. The R-UNI-xx rules that Epic 1 cites (R-UNI-19, 30, 38, 40, 43 and others) stay as coded behaviour and are cited by ID as today. They move into a UNIVERSAL package in Epic 3 (phase 2).

### 3.3 Published interfaces

These names are used in every story, design and test. There are no other new interfaces.

```java
// P3, package recovery.casewf.rules (published)
public interface RuleEvaluator {
    RuleResult evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
}
public record RuleResult(String packageCode, String packageVersion, String ruleId, Map<String,Object> outputs) {}
public interface RuleCatalog { RuleRow row(String ruleId, String packageVersion); }
// P3, package recovery.casewf.timers (published)
public interface TimerScheduler { void schedule(TimerSpec t); void cancel(UUID timerId); void pause(UUID timerId); void resume(UUID timerId); }
// P3, package recovery.casewf.workflow (published, Epic 1)
public interface WorkflowGateway { String start(String workflowType, String workflowId, Object input); void signal(String workflowId, String signal, Object payload); }
```

`RuleTableReader` (from E1-029) no longer exists. Every mention of it becomes `RuleEvaluator` or `RuleCatalog`.

## 4. Story dispositions

### 4.1 Retire

| Story | Title | New home | In-flight work |
|---|---|---|---|
| RWB-E1-029 | Rule load, validation and rollback | RWB-E1-073 | INC-019 (In delivery) cancelled |
| RWB-TE-005 | Rule table test harness | RWB-E1-073 (scenarios, build gate) | INC-006 (has build output) cancelled |
| RWB-E1-048 | Rule change audit report | RWB-E2-041 | none |

The full record, with the original sections, is `16 Temporal and Drools Adoption/Recovery Workbench Rule Story Retirements v1.md`. The three keys do not appear in Epic 1 v9, Epic 2 v7 or TE v7.

### 4.2 Rewrite

Each line is the full change list for that story.

| Story | Title | What changes |
|---|---|---|
| RWB-E1-018 | Case ID issuance and case record | Entry and exclusion come from `RuleEvaluator.evaluate("EXCLUSION"/"ENTRY", facts, businessDate)`; EntryRuleEvaluator is removed; `case_entry_exclusion` stores the rule ID and the package version; preconditions cite E1-073; depends on adds E1-072 and E1-073; one new AC for no EXCLUSION package in force (MSG-P3-027) with its test |
| RWB-E1-020 | Allocation and assignment engine | ALLOCATION and ASSIGNMENT through RuleEvaluator, first match per T5, the default row check cited from E1-073; JOB-03 stays on Quartz; RuleTableReader and the decision-table-evaluator components are removed; AllocationFacts is added; the decision log carries rule ID and package version; depends on adds E1-072 and E1-073 |
| RWB-E1-021 | Transfer rules and engine | TRANSFER package through RuleEvaluator; the eight triggers become a TransferTrigger fact; the manual transfer API is unchanged; out of scope adds "From Epic 3 the trigger arrives as a Temporal signal"; depends on adds E1-072 and E1-073 |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | Timers stay rows in `timer`; TimerCheckJob (JOB-05, Quartz) implements TimerScheduler and every caller schedules, pauses, resumes and cancels through it; one BR with an AC and a test; out of scope adds Temporal durable timers in Epic 3 (ADR-011) |
| RWB-E1-043 | Reference data service with versioned tables | Rule tables are no longer reference tables; the reference data service holds reference tables only; the rollback line points at E1-073 for rule packages; SY-RULES reads reference values as Drools facts; the rule-table schema rows leave ReferenceTableSchemas |
| RWB-TE-007 | Scheduled jobs on Quartz | Quartz is kept for every Epic 1 and 2 job; JOB-05 is the Quartz implementation of TimerScheduler; one BR says no new Quartz job may hold a case wait; out of scope adds Temporal Schedules (Epic 3+); one fragment serves both Epic 1 and TE |
| RWB-E2-002 | ACE plan status on the case | R-RES-29, 30, 31 and R-LIT-02 are evaluated through RuleEvaluator("RESTRUCTURE") and the data reads the rule catalog; depends on adds E1-072 and E2-042 |
| RWB-E2-004 | Treatment entity and plan timers data model | R-RES-25 and R-RES-27 go through RuleEvaluator("RESTRUCTURE"); plan timers are scheduled through TimerScheduler, with JOB-05 still Quartz; depends on adds E1-072 and E2-042 |
| RWB-E2-007 | Booking confirmation from the ALS load | BookingMatchRules becomes package BOOKING_MATCH and the comparison evaluator is removed; depends on adds E1-072 and E2-042 |
| RWB-E2-008 | Payment matching with the missed payment event | `payment_match_rule` is replaced by package PAYMENT_MATCH (T10); DF-REF-261 to 273 become DF-REF-002, 003 and 296 to 298; the decision log records R-RES-26 with the package version; depends on adds E1-072 and E2-042 |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | Manual transfer is evaluated by RuleEvaluator("TRANSFER") and the refusing rule ID is shown (MSG-P3-033); depends on adds E1-072 |
| RWB-E2-027 | Payment matching rules with the data team | PARTIAL and WINDOW become rows of PAYMENT_MATCH loaded through `POST /admin/rule-packages/PAYMENT_MATCH/versions`, not through reference loads; the precondition names the PAYMENT_MATCH version with the EXACT row in force; depends on adds E2-042 |
| RWB-E2-035 | Next action on the case | SY-RULES evaluates the package for the case state and event through RuleEvaluator; action text, owner role and timer spec come from `RuleCatalog.row(ruleId, packageVersion)`; the precondition cites E1-073 and E2-042; JOB-05 stays (T2); depends on adds E1-072 and E2-042 |

### 4.3 Reference update

Wording or dependencies only. Nothing else in these stories is touched.

| Story | Title | Reference update |
|---|---|---|
| RWB-E1-013 | Baseline measures | Depends on RWB-E1-029, RWB-E1-018 becomes RWB-E1-043, RWB-E1-018; the precondition names RWB-E1-043 |
| RWB-E1-038 | Delegation of authority table as reference data | Depends on RWB-E1-043, RWB-E1-029, RWB-E1-027 becomes RWB-E1-043, RWB-E1-027; the precondition and the load reference name the versioned reference load (E1-043) |
| RWB-E1-027 | Decision log writer | "rules component" becomes "Drools evaluator (RuleEvaluator, RWB-E1-072)"; one sentence says the rule version is the rule package version label (D-RCV-36) |
| RWB-E1-062 | Deviation screening agent in shadow [E2b] | The owner role is read from the rule catalog (RuleCatalog, RWB-E1-072) |
| RWB-TE-013 | Agent runtime client with fallback | "evaluates its rule and builds the rule result" becomes "evaluates its rule package through RuleEvaluator and builds the rule result", in Epic 1 and TE |
| RWB-E1-056 | Run books and monitoring for every Epic 1 Workbench job | One run-book catalog note: the Temporal server and worker run books are owned by RWB-E1-070 and RWB-E2-037 |
| RWB-E2-005 | Decision log query API for audit | The E1-048 precondition and dependency become E2-041, and the report gives the count of decisions per rule package version |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | "JOB-05 Timer check (RWB-E1-028)" becomes "JOB-05 Timer check behind TimerScheduler (RWB-E1-028)" |

Every live Epic 1, Epic 2 and TE section also takes one global replacement outside fenced gherkin blocks: "rules component" becomes "Drools evaluator".

### 4.4 New stories

| Story | Title | Epic and release | Feature |
|---|---|---|---|
| RWB-E1-070 | Temporal platform on the ACE AKS clusters | E1, 30 November 2026 | None (platform enabler) |
| RWB-E1-071 | Temporal worker and SDK in the recovery module | E1, 30 November 2026 | None (platform enabler) |
| RWB-E1-072 | Drools runtime and rule package store | E1, 30 November 2026 | FEAT-DRI-07 |
| RWB-E1-073 | Rule authoring, validation, test scenarios, approval and rollback in Drools | E1, 30 November 2026 | FEAT-CWC-14, FEAT-CWC-15 |
| RWB-E2-037 | Temporal observability and run books | E2, 31 December 2026 | None (platform enabler) |
| RWB-E2-038 | Temporal security, codec server and admin audit | E2, 31 December 2026 | None (platform enabler) |
| RWB-E2-039 | Temporal resilience: backup, failover, upgrade and archive | E2, 31 December 2026 | None (platform enabler) |
| RWB-E2-040 | Workflow versioning and replay test gate | E2, 31 December 2026 | None (platform enabler) |
| RWB-E2-041 | Rule change governance and audit report | E2, 31 December 2026 | FEAT-CWC-16 (carried from E1-048) |
| RWB-E2-042 | Epic 2 rule packages in Drools | E2, 31 December 2026 | FEAT-DRI-07 |
| RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow | E2, 31 December 2026 | None (platform enabler) |

Thirty-five story keys carry a change in Phase 1: 11 new, 3 retired, 13 rewritten and 8 with a reference update.

## 5. The document edit list

The target is the next version beside the current one, and the old version stays until sign-off. A document not in this table is not edited by this change. One writer owns each file and returns an edit log.

### 5.1 Governance and technical documents

| # | Folder | Current file | New file | Size | Wave | Owning agent | What changes |
|---|---|---|---|---|---|---|---|
| 1 | 01 Decisions and governance | Recovery Workbench Decision Log v9.xlsx | Recovery Workbench Decision Log v10.xlsx | M | W1 | W1 governance agent | D-RCV-36 row; DT02, DT09 and DT10 marked superseded; the count in A2 |
| 2 | 05 Technical architecture | Recovery Workbench Architecture Decision Records v2.md | Recovery Workbench Architecture Decision Records v3.md | M | W2 | W2 architecture agent | ADR-011 and ADR-012 added; ADR-003 and ADR-004 marked superseded; the index |
| 3 | 05 Technical architecture | Recovery Workbench Rules Engine Design v2.docx | Recovery Workbench Rules Engine Design v3.docx | L | W2 | W2 rules agent | Embedded Drools, XLS packages, the rule package store, first match, catalog, dry run, no release, payment matching |
| 4 | 05 Technical architecture | Recovery Workbench Workflow Engine Design v2.docx | Recovery Workbench Workflow Engine Design v3.docx | L | W2 | W2 workflow agent | Temporal hybrid, workflow IDs, task queues, durable timers, retries, replay, codec, case data in the ACE DB |
| 5 | 05 Technical architecture | Recovery Workbench Batch and Scheduling Design v3.docx | Recovery Workbench Batch and Scheduling Design v4.docx | L | W2 | W2 batch agent | Quartz kept; JOB-05 behind TimerScheduler; RulePackageEffectiveDateJob, PlatformSmokeWorkflow and StuckWorkflowScanner; Temporal Schedules out of Epics 1 and 2 |
| 6 | 05 Technical architecture | Recovery Workbench Batch and Scheduling Design v3.xlsx | Recovery Workbench Batch and Scheduling Design v4.xlsx | L | W2 | W2 batch agent | The job list mirror of row 5 |
| 7 | 05 Technical architecture | Recovery Workbench API Specification v3.yaml | Recovery Workbench API Specification v4.yaml | M | W2 | W2 API agent | 3 rule-version endpoints removed, 7 rule package endpoints added, the published interfaces |
| 8 | 05 Technical architecture | Recovery Workbench API Specification v3.html | Recovery Workbench API Specification v4.html | M | W2 | W2 API agent | The rendered API specification of row 7 |
| 9 | 05 Technical architecture | Recovery Workbench Environment and Deployment Design v3.docx | Recovery Workbench Environment and Deployment Design v4.docx | S | W2 | W2 environment agent | Temporal Helm release, namespace, databases and roles, mTLS, OIDC, pinned versions, the two flags |
| 10 | 05 Technical architecture | Recovery Workbench Target Architecture v5.docx | Recovery Workbench Target Architecture v6.docx | L | W2 | W2 architecture agent | The workflow layer and the rules layer on ACE |
| 11 | 05 Technical architecture | Recovery Workbench Target Architecture v5.pptx | Recovery Workbench Target Architecture v6.pptx | L | W2 | W2 architecture agent | The same two layers in the deck |
| 12 | 05 Technical architecture | Recovery Workbench Error Handling and Resilience Standard v2.docx | Recovery Workbench Error Handling and Resilience Standard v3.docx | S | W2 | W2 resilience agent | Activity retry policy, idempotency, NoPackageInForce as non-retryable, MSG-P3-036 to 038 |
| 13 | 05 Technical architecture | Recovery Workbench Observability and Monitoring Design v2.docx | Recovery Workbench Observability and Monitoring Design v3.docx | S | W2 | W2 observability agent | Temporal metrics, failed and stuck workflow alerts, the dashboard |
| 14 | 05 Technical architecture | Recovery Workbench Security and Access Design v3.docx | Recovery Workbench Security and Access Design v4.docx | S | W2 | W2 security agent | Codec server, break-glass decode, mTLS, the Temporal authorizer, admin audit |
| 15 | 05 Technical architecture | Recovery Workbench ACE Architecture Decision v3.docx | Recovery Workbench ACE Architecture Decision v4.docx | M | W2 | W2 architecture agent | The workflow and rules sections, with the superseded decisions noted |
| 16 | 05 Technical architecture | Recovery Workbench Technical Specifications by Module v4.zip | Recovery Workbench Technical Specifications by Module v5.zip | L | W2 | W2 TSD agent | TSD P3 for workflow and rules, P2 for the Temporal client, P4 for package admin and the codec |
| 17 | 06 Data | Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx | Recovery Workbench Logical Data Model and Data Dictionary v8.xlsx | L | W2 | W2 data agent | DF-REF-274 to 299 added; DF-REF-261 to 273 retired |
| 18 | 06 Data | Recovery Workbench Physical Schema v5.sql | Recovery Workbench Physical Schema v6.sql | L | W2 | W2 data agent | rule_package and rule_package_version added, payment_match_rule dropped, 4 columns added, 93 tables |
| 19 | 06 Data | Recovery Workbench Entity Relationship Diagram v4.html | Recovery Workbench Entity Relationship Diagram v5.html | M | W2 | W2 data agent | The three rule entities and their relationships |
| 20 | 06 Data | Recovery Workbench Entity Relationship Diagram v4.pdf | Recovery Workbench Entity Relationship Diagram v5.pdf | M | W2 | W2 data agent | The rendered diagram of row 19 |
| 21 | 07 Screens and experience | Recovery Workbench Error and Message Standard v3.docx | Recovery Workbench Error and Message Standard v4.docx | S | W2 | W2 message agent | MSG-P3-036, MSG-P3-037 and MSG-P3-038; MSG-P3-022 moves to E2-041 |

### 5.2 Story documents

| # | Folder | Current file | New file | Size | Wave | Owning agent | What changes |
|---|---|---|---|---|---|---|---|
| 22 | 04 User stories | Recovery Workbench User Stories Epic 1 v8.md | Recovery Workbench User Stories Epic 1 v9.md | L | W3 | W3 Epic 1 agent | E1-018, 020, 021, 028 and 043 rewritten; 5 reference updates; E1-029 and E1-048 retired; E1-070 to E1-073 added |
| 23 | 04 User stories | Recovery Workbench User Stories Epic 1 v8.xlsx | Recovery Workbench User Stories Epic 1 v9.xlsx | L | W3 | W3 workbook agent | The same changes in the workbook, with the story tabs and the index |
| 24 | 04 User stories | Recovery Workbench User Stories Epic 2 v6.md | Recovery Workbench User Stories Epic 2 v7.md | M | W3 | W3 Epic 2 agent | E2-002, 004, 007, 008, 012, 027 and 035 rewritten; E2-005 and E2-015 reference updates; E2-037 to E2-043 added |
| 25 | 04 User stories | Recovery Workbench User Stories Epic 2 v6.xlsx | Recovery Workbench User Stories Epic 2 v7.xlsx | M | W3 | W3 workbook agent | The same changes in the workbook |
| 26 | 04 User stories | Recovery Workbench Technical Enabler Stories v6.md | Recovery Workbench Technical Enabler Stories v7.md | S | W3 | W3 TE agent | TE-007 rewritten; TE-013 reference update; TE-005 retired |
| 27 | 04 User stories | Recovery Workbench Technical Enabler Stories v6.xlsx | Recovery Workbench Technical Enabler Stories v7.xlsx | S | W3 | W3 workbook agent | The same three changes in the workbook |
| 28 | 04 User stories | Recovery Workbench User Stories Epic 1 Story Files v6.zip | Recovery Workbench User Stories Epic 1 Story Files v7.zip | M | W3 | W3 story file agent | 3 files removed, 7 replaced, 4 added: E1-070 to E1-073 |
| 29 | 04 User stories | Recovery Workbench User Stories Epic 2 Story Files v4.zip | Recovery Workbench User Stories Epic 2 Story Files v5.zip | M | W3 | W3 story file agent | 9 files replaced, 7 added: E2-037 to E2-043 |
| 30 | 04 User stories | Recovery Workbench Build Notes Epic 1 v5.md | Recovery Workbench Build Notes Epic 1 v6.md | M | W3 | W3 build notes agent | Notes for the 5 rewrites and the 4 new stories; the E1-029 note is withdrawn |
| 31 | 04 User stories | Recovery Workbench Build Notes Epic 2 v2.md | Recovery Workbench Build Notes Epic 2 v3.md | S | W3 | W3 build notes agent | Notes for the 7 rewrites and the 7 new stories |
| 32 | 04 User stories | Recovery Workbench Build Notes Technical Enablers v1.md | Recovery Workbench Build Notes Technical Enablers v2.md | S | W3 | W3 build notes agent | TE-007 rewritten; TE-005 withdrawn |
| 33 | 14 Story Updates | (new) | Recovery Workbench Rule Story Retirements v1.md | M | W3 | W3 removals agent | The three retired stories and their original sections |

### 5.3 Test and delivery documents

| # | Folder | Current file | New file | Size | Wave | Owning agent | What changes |
|---|---|---|---|---|---|---|---|
| 34 | 09 Testing and quality | Recovery Workbench Test Cases v6.xlsx | Recovery Workbench Test Cases v7.xlsx | L | W4 | W4 test agent | The test sets of the 3 retired stories removed; tests for the 11 new and 13 rewritten stories |
| 35 | 09 Testing and quality | Recovery Workbench Requirements Traceability Matrix v5.xlsx | Recovery Workbench Requirements Traceability Matrix v6.xlsx | M | W4 | W4 test agent | REQ-CWC-004, 007 to 011, 013, 014 and 016 and REQ-DRI-001, 004, 005, 007, 010 and 011 point at the live tests |
| 36 | 09 Testing and quality | Recovery Workbench Regression Suite v6.xlsx | Recovery Workbench Regression Suite v7.xlsx | M | W4 | W4 test agent | Retired cases leave the suite; the Temporal smoke and the rule scenario gate join it |
| 37 | 09 Testing and quality | Recovery Workbench Non Functional Test Plan v2.docx | Recovery Workbench Non Functional Test Plan v3.docx | S | W4 | W4 test agent | Workflow durability, activity retry, the replay gate and rule evaluation latency; the phase 2 measures follow section 6.5 |
| 38 | 04 User stories | Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v3.xlsx | Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v4.xlsx | S | W4 | W4 defects agent | Rows for E1-029, TE-005 and E1-048 closed; new contradictions found in the rewrite raised |
| 39 | 11 Delivery and operations | Recovery Workbench Build Sequence Epic 1 and Epic 2 v5.xlsx | Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx | L | W4 | W4 delivery agent | The 11 new stories and the new order |
| 40 | 11 Delivery and operations | Recovery Workbench Story Build Order v2.docx | Recovery Workbench Story Build Order v3.docx | L | W4 | W4 delivery agent | The 11 new stories and the critical path through E1-072 and E1-073 |
| 41 | 11 Delivery and operations | Recovery Workbench Dependency Map v3.xlsx | Recovery Workbench Dependency Map v4.xlsx | M | W4 | W4 delivery agent | The Temporal cluster and the ACE AKS dependency |
| 42 | 11 Delivery and operations | Recovery Workbench Risks Assumptions Issues and Dependencies v3.xlsx | Recovery Workbench Risks Assumptions Issues and Dependencies v4.xlsx | M | W4 | W4 delivery agent | Temporal operations load, Epic 1 date, Drools upgrade, XLS authoring skill |
| 43 | 11 Delivery and operations | Recovery Workbench Release Plan v4.xlsx | Recovery Workbench Release Plan v5.xlsx | S | W4 | W4 delivery agent | The two Epic 1 platform stories and the two Epic 2 rule stories |
| 44 | 11 Delivery and operations | Recovery Workbench Release Plan v4.pptx | Recovery Workbench Release Plan v5.pptx | S | W4 | W4 delivery agent | The same two releases in the deck |
| 45 | 11 Delivery and operations | Recovery Workbench Engineering Practices v4.docx | Recovery Workbench Engineering Practices v5.docx | M | W4 | W4 delivery agent | Pipeline gate 10 for replay; the rule scenario build gate; the Drools library upgrade duty |
| 46 | 11 Delivery and operations | Recovery Workbench Run Operating Model v2.docx | Recovery Workbench Run Operating Model v3.docx | M | W4 | W4 delivery agent | RW-PLATADM runs four Temporal clusters; on-call, backup and upgrade |
| 47 | 11 Delivery and operations | Recovery Workbench Training and Change Plan v2.docx | Recovery Workbench Training and Change Plan v3.docx | S | W4 | W4 delivery agent | RW-COE training in XLS authoring; RW-PLATADM training in Temporal operations |
| 48 | 10 Policy, controls and compliance | Recovery Workbench Controls Catalog v3.xlsx | Recovery Workbench Controls Catalog v4.xlsx | S | W4 | W4 controls agent | The package approval control and the replay gate control |

### 5.4 Pack

| # | Folder | Current file | New file | Size | Wave | Owning agent | What changes |
|---|---|---|---|---|---|---|---|
| 49 | 12 Project communication | Recovery Workbench Document Index v12.md | Recovery Workbench Document Index v13.md | M | W5 | W5 index agent | The 3 new files and every new version |
| 50 | 12 Project communication | Recovery Workbench Document Control Sheet v11.xlsx | Recovery Workbench Document Control Sheet v12.xlsx | M | W5 | W5 control sheet agent | The same rows with owner, reviewer and status |
| 51 | 14 Story Updates | Recovery Workbench Project Hub v16.html | Recovery Workbench Project Hub v17.html | L | W5 | W5 hub agent | The 11 new and 13 rewritten stories, the three retirements and the new technical text |

The three story workbooks (Epic 1 v9.xlsx, Epic 2 v7.xlsx and TE v7.xlsx) carry the same story text as the markdown files. The markdown file is the master; the workbook is generated from it and checked against it.

## 6. Phase 2 scope

Phase 2 is Epics 3 to 8. Nothing below is built in Phase 1, and nothing below is added to the Epic 1 or Epic 2 releases.

### 6.1 Epics 3 to 8

- One case workflow per case on `rwb-case`, with durable timers, retries and the multi-step outbound chains on `rwb-integration`.
- Case events arrive as signals. E1-021 out of scope already says the transfer trigger becomes a Temporal signal in Epic 3.
- The reference case workflow (E2-043) is the pattern every Epic 3 workflow copies.
- The worker swap for JOB-05: a Temporal implementation of TimerScheduler replaces the Quartz implementation. No caller changes.
- Administration screens for rule packages and workflow operations (SCR-39 and the Epic 8 administration screens).

### 6.2 Administration stories

`04 User stories/Recovery Workbench Administration Stories v3.md` cites RWB-E1-029 three times and RWB-E1-048 once:

| Where | Line | What it says today | Phase 2 edit |
|---|---|---|---|
| The story index table | 22 | RWB-E1-029 Rule load, validation and rollback, P3, E1 | Remove the row; the work is E1-073 |
| The story index table | 29 | RWB-E1-048 Rule change audit report, P3, E1 | Remove the row; the work is E2-041 |
| The RWB-AD-011 dependency row | 46 | Load a rule version, P4, E8, depends on RWB-E1-029 | Depend on RWB-E1-073 and read packages, not rule versions |
| The RWB-AD-011 metadata table | 911 | Depends on RWB-E1-029 | Depends on RWB-E1-073 |

The story key RWB-AD-011 and its intent do not change: an administrator loads a rule package version, and the center of excellence authors it.

### 6.3 The UNIVERSAL package

The R-UNI-xx rules that Epic 1 cites (R-UNI-19, 30, 38, 40, 43 and others) stay as coded behaviour in Phase 1 and are cited by ID as today. In Epic 3 they move into a UNIVERSAL package, authored in the Drools XLS template, and are evaluated through RuleEvaluator like every other package. Until then no story may claim they are rows in `rule_row`.

### 6.4 JOB-05

In Epics 1 and 2, JOB-05 is the Quartz implementation of TimerScheduler: it reads due rows, fires the timer path and writes the outcome. In Epic 3 a Temporal implementation registers on the same port and JOB-05 stops holding case waits. Timer rows stay as the case's own record either way, because they are read by the case record view and by E2-015.

### 6.5 Non-functional additions

The phase 2 document pass adds these measures to the Non Functional Specification. No NFR ID is allocated in this pack, and a writer must use the IDs the specification already holds.

| Area | Addition |
|---|---|
| Availability | The Temporal cluster meets the ACE availability target per environment; a workflow history write is not lost on a frontend pod restart |
| Recovery | Point-in-time restore of `temporal` and `temporal_visibility`; a zone failover completes an in-flight smoke workflow |
| Durability | A 30-day timer fires once after a deploy, a restart and an upgrade |
| Upgrade | One minor Temporal version per upgrade, tested in SIT with no lost workflow |
| Performance | Rule evaluation p95 within the decision path budget; a KieBase is not recompiled per call |
| Retention | Workflow history 30 days, then archived to Blob with no clear personal data |
| Security | Every decode through the codec server is break-glass and logged |
| Test | Replay gate on every workflow change; rule scenarios on every build |

## 7. Counts

| Item | Count |
|---|---|
| Decisions | 1 (D-RCV-36, T1 to T10) |
| ADRs added | 2 (ADR-011, ADR-012) |
| ADRs superseded | 2 (ADR-003, ADR-004) |
| Stories new | 11 (E1-070 to E1-073, E2-037 to E2-043) |
| Stories retired | 3 (E1-029, TE-005, E1-048) |
| Stories rewritten | 13 |
| Stories with a reference update | 8, plus one global wording replacement |
| Messages added | 3 (MSG-P3-036 to MSG-P3-038) |
| Field IDs added | 26 (DF-REF-274 to DF-REF-299) |
| Field IDs retired | 13 (DF-REF-261 to DF-REF-273) |
| Endpoints removed | 3 |
| Endpoints added | 7 |
| Rule package codes in Phase 1 | 8 |
| Tables in Physical Schema v6 | 93 |
| Documents in this edit list | 51 |

## Appendix A - allocated IDs

These are the only IDs this change allocates. **Do not invent any other ID.** Any other ID a document cites is an existing ID, used as it stands.

### A.1 Decision

| ID | Text |
|---|---|
| D-RCV-36 | The decision that records T1 to T10. |

### A.2 ADRs

| ID | Title | Relation |
|---|---|---|
| ADR-011 | Run case workflows on Temporal, with case data in the ACE database | Accepted 16 November 2026; supersedes ADR-003 |
| ADR-012 | Evaluate rules with embedded Drools from versioned rule packages | Accepted 16 November 2026; supersedes ADR-004 and keeps its principle of rules as versioned data |

### A.3 Stories

| ID | Title |
|---|---|
| RWB-E1-070 | Temporal platform on the ACE AKS clusters |
| RWB-E1-071 | Temporal worker and SDK in the recovery module |
| RWB-E1-072 | Drools runtime and rule package store |
| RWB-E1-073 | Rule authoring, validation, test scenarios, approval and rollback in Drools |
| RWB-E2-037 | Temporal observability and run books |
| RWB-E2-038 | Temporal security, codec server and admin audit |
| RWB-E2-039 | Temporal resilience: backup, failover, upgrade and archive |
| RWB-E2-040 | Workflow versioning and replay test gate |
| RWB-E2-041 | Rule change governance and audit report |
| RWB-E2-042 | Epic 2 rule packages in Drools |
| RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow |

### A.4 Messages

| ID | Type | Text | Used by |
|---|---|---|---|
| MSG-P3-036 | Error | The workflow service is not available. Try again in a few minutes. | E1-071, E2-043 |
| MSG-P3-037 | Warning | Workflow {workflowId} has failed or has not moved for {hours} hours. | E2-037 |
| MSG-P3-038 | Error | The workflow change fails the replay test against recorded histories: {detail}. | E2-040 |

Reuse MSG-P3-027 with {check} = compile for a Drools compile failure. MSG-P3-022 (missing checklist) moves from E1-048 to E2-041. Every other message is one that already exists in the Error and Message Standard.

### A.5 Field IDs

| Entity | Field IDs | Fields |
|---|---|---|
| rule_package | DF-REF-274 to DF-REF-278 | id, package_code, title, owner_role, hit_policy |
| rule_package_version | DF-REF-279 to DF-REF-295 | id, package_id, version_label, status, source_blob_ref, drl_source, checksum, valid_from, valid_to, author, approver, loaded_at, approved_at, test_result, dry_run_counts (jsonb), rollback_of, change_checklist (jsonb) |
| rule_row additions | DF-REF-296 to DF-REF-298 | package_version_id, drools_rule_name, outputs (jsonb) |
| rule_test_case addition | DF-REF-299 | package_version_id |
| Retired | DF-REF-261 to DF-REF-273 | the payment_match_rule fields |

### A.6 Endpoints (API v4)

Remove:

| Method | Path |
|---|---|
| GET | /admin/rule-versions |
| POST | /admin/rule-versions/{versionId}/approve |
| POST | /admin/rule-versions/{versionId}/rollback |

Add:

| Method | Path | Used by |
|---|---|---|
| GET | /admin/rule-packages | E1-072, E1-073 |
| POST | /admin/rule-packages/{packageCode}/versions (multipart xlsx, validFrom) | E1-073, E2-027 |
| GET | /admin/rule-packages/{packageCode}/versions | E1-073 |
| POST | /admin/rule-package-versions/{versionId}/approve | E1-073 |
| POST | /admin/rule-package-versions/{versionId}/rollback (body reason, Idempotency-Key) | E1-073 |
| GET | /admin/rule-package-versions/{versionId}/dry-run | E1-073 |
| GET | /admin/rule-packages/change-report | E2-041 |

### A.7 Tables

Physical Schema v6 is 92 + rule_package + rule_package_version - payment_match_rule = 93 tables. Temporal's own tables are not in the Physical Schema.

### A.8 Requirements

Existing IDs only. No new REQ ID is allocated.

- REQ-CWC-004, 007 to 011, 013, 014 and 016
- REQ-DRI-001, 004, 005, 007, 010 and 011

### A.9 Roles

Existing codes only. No new role code is allocated.

RW-COE, RW-RISK, RW-AUDIT, RW-REFADM, RW-PLATADM, RW-SECADM, RW-TEAMMGR, SY-RULES, SY-CASEWF.

## Appendix B - what this pack contains

| File | What it is |
|---|---|
| `16 Temporal and Drools Adoption/Recovery Workbench Temporal and Drools Change Register v1.md` | This document |
| `16 Temporal and Drools Adoption/Recovery Workbench Rule Story Retirements v1.md` | The three retired stories, their new homes and their original sections |
| `05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md` | ADR v3, with ADR-011 and ADR-012 |
| `01 Decisions and governance/Recovery Workbench Decision Log v10.xlsx` | The decision log with D-RCV-36 |
