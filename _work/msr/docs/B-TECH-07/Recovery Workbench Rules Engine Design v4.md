SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# Rules engine design

| Item | Detail |
|---|---|
| Document | Recovery Workbench rules engine design |
| Version | 4 |
| Date | 22 November 2026 |
| Supersedes | Version 3, 16 November 2026 |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Change, version 3 | v3, 16 November 2026, D-RCV-36: rules run on embedded Drools from versioned XLS rule packages, first match by activation-group, approval by Risk and rollback by one call (ADR-012) |
| Decision | D-RCV-60 adopt Architecture v5. ADR-017: embedded Drools in each of the 19 services, with the rule package registry in rwb-decision; it amends ADR-012 and D-RCV-36 T1 and T2 |
| Prepared by | Henka Group |
| Structure | Drools XLS decision tables, arc42 crosscutting concepts |
| Status | Draft |

# 1. The design on one page

Rules are evaluated by Drools embedded in each of the 19 Recovery services, in the service that owns the decision the rules make. Each service carries the KIE runtime libraries only: drools-engine, drools-mvel, drools-decisiontables and drools-xml-support. There is no KIE Server, no Business Central and no KJAR in Maven. A rule package is an Excel workbook in Drools XLS decision-table format, uploaded as a file to the registry in rwb-decision, compiled to a KieBase, checked, run against its scenarios, approved by Risk and stored as a version. A change takes effect on a date, not on a release, and a rollback is one call. ADR-012 records the decision and replaces ADR-004 while keeping its principle that rules are versioned data; ADR-017 places the evaluation in each service and the registry in rwb-decision (DP-04; ASM-B-TECH-07-1).

| Element | Design |
|---|---|
| What it is | Embedded Drools in each of the 19 services, in the service that owns the decision, with KIE runtime libraries only. No KIE Server, no Business Central and no KJAR. |
| What it holds | Rule packages and their versions: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER in Phase 1; RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH in Epic 2; UNIVERSAL in Epic 3. |
| Where it runs | The evaluation in the owning service's worker, on its own task queue rwb-<service>; the registry, the approval and the version store in rwb-decision (P7). |
| Table form | Drools XLS decision table: one workbook per package, a Rows tab and a Tests tab. First match, not a decision-tree language. |
| Rule semantics | RuleSet = package code; each row is one rule with NAME = rule ID; one activation-group per package; salience from row order; the default row is last. |
| Authoring | RW-COE writes the workbook and its scenarios; RW-REFADM prepares the load file. The workbook is the source, and the generated DRL is stored with it. |
| Testing | At least rules.testcases.min (50) scenarios on the Tests tab run through the same RuleEvaluator as production, plus a dry run over open cases. |
| Approval | RW-RISK approves; the author cannot approve. A version takes effect on its valid-from date after approval. |
| Rollback | One call returns the previous version in one transaction; the reason is recorded. |
| Record | Every decision names the rule ID and the package version in decision_log_entry. Under ADR-022 the owning service writes its own decision record in its own schema in the same transaction as its change, and rwb-decision collects it into the central ledger; the rule_row catalog carries the action text, owner role, timer and outputs. |
| Decision | ADR-012, which supersedes ADR-004. D-RCV-36 T3, T4, T5, T6 and T7 apply. ADR-017 amends ADR-012: embedded Drools per service, registry in rwb-decision. |

## 1.1 What version 4 changes, and the decision behind each change

Nothing in this table removes a rule, a package, a check or a control of version 3. Each row names the version 3 statement that the realignment replaces and the record that replaces it.

| # | Version 3 | Version 4 | Decision |
|---|---|---|---|
| 1 | Rules are evaluated by Drools embedded in the recovery module | Rules are evaluated by Drools embedded in each of the 19 services, in the service that owns the decision (CG-B-TECH-07-1; ASM-B-TECH-07-1) | ADR-017; DP-04 |
| 2 | The package, its versions and its governance sit with the module | The registry, the versions, the scenarios, the dry run and the four-eyes approval sit in rwb-decision (P7), under REST base /api/recovery/decision/v1 | ADR-017; R-PREC default ruling (rule package registry) |
| 3 | A caller inside the module asks the evaluator | Each owning service loads the version it is told is in force: GET /rule-models/{n}/{v}, checksum verified, atomic swap, last good model kept on failure (CG-B-TECH-07-5; ASM-B-TECH-07-5) | ADR-017; Architecture v5 slide 27 |
| 4 | RulePackageEffectiveDateJob, a Quartz job at 00:01 owned by RW-COE | The JOB-20 Temporal Schedule rule promote at 00:01 in rwb-decision, which publishes RulePackageInForce (EV-30) (CG-B-TECH-07-7; ASM-B-TECH-07-8) | ADR-016; Architecture v5 slide 44 |
| 5 | The rule store sits in the single recovery schema | rule_package, rule_package_version, rule_row and rule_test_case sit in schema rwb_decision with login rwb_decision; each service writes its own decision records in its own schema (CG-B-TECH-07-9; ASM-B-TECH-07-9) | ADR-014; ADR-022 |
| 6 | One decision_log_entry per decision, written by a log activity | The decision record, the state change and the outbox row in one transaction in the owning service, then DecisionRecorded to rwb.decision-record.v1 and the central ledger in rwb-decision (CG-B-TECH-07-8; ASM-B-TECH-07-7) | ADR-022 |
| 7 | Each package has one owner role, RW-COE | Each package also has one owning service, which evaluates it (§2); the registry stays P7 for all of them | DP-04; Ownership Map v1 |
| 8 | UNIVERSAL arrives in Epic 3 for the module | UNIVERSAL arrives in Epic 3 and is evaluated in every service, with governance in rwb-decision (CG-B-TECH-07-10; ASM-B-TECH-07-10) | ADR-017; Temporal and Drools design slide 13 |

# 2. Route sets to packages

The ten route sets of v2 remain the business view of the 448 routing rules. Phase 1 does not load all of them: five package codes cover the Epic 1 engines, three more cover Epic 2, and the remaining route sets wait for their epics. The Package column names the rule_package.package_code that holds the route set; where no Phase 1 package exists, the row says so. The Owning service column names the one service that evaluates the package (DP-04; ASM-B-TECH-07-15).

| Route set | Rules | Decision | Package | Owning service |
|---|---|---|---|---|
| Restructure | 37 | D5, D6 | RESTRUCTURE | S2 rwb-treatment |
| Settlement | 27 | D6.4 | Not in Phase 1 | S2 rwb-treatment |
| Deed in lieu | 37 | D6.4 | Not in Phase 1 | S2 rwb-treatment |
| Guarantee claim | 32 | D6.5, D6.6 | Not in Phase 1 | S3 rwb-guarantee |
| Litigation | 79 | D7 | Not in Phase 1 | S4 rwb-litigation |
| Asset disposal | 72 | D8.1 to D8.3 | Not in Phase 1 | S5 rwb-asset |
| Debt sale | 41 | D8.4 | Not in Phase 1 | S6 rwb-debtsale |
| Write-off | 51 | D9 | Not in Phase 1 | S7 rwb-writeoff |
| Deviations | 22 | X1 to X7 | Not in Phase 1 | S8 rwb-deviation |
| Universal rules | 50 | All | UNIVERSAL (Epic 3) | every service; registry P7 |
| Total | 448 |  | 8 Phase 1 packages | 19 services |

The Phase 1 package list is fixed by DL24 and the Epic 2 scope. Each package has one owner role, RW-COE, one hit policy, FIRST_MATCH, and one owning service. A package code is never reused for a different route set: the code is the RuleSet cell of every workbook row that belongs to it.

| Epic | Package | Rules | Used by | Owning service |
|---|---|---|---|---|
| 1 | ENTRY, EXCLUSION | Entry and exclusion rows (DL24) | RWB-E1-018 | P3 rwb-case |
| 1 | ALLOCATION, ASSIGNMENT | Allocation and assignment rows (DL24) | RWB-E1-020, RWB-E1-030 | P3 rwb-case |
| 1 | TRANSFER | Transfer rows (DL24) | RWB-E1-021, RWB-E2-012 | P3 rwb-case |
| 2 | RESTRUCTURE | R-RES-25, R-RES-27, R-RES-29, R-RES-30, R-RES-31, R-LIT-02, and the route-set rows with action_text, owner_role and timer_spec that E2-035 reads | RWB-E2-002, RWB-E2-004, RWB-E2-035 | S2 rwb-treatment |
| 2 | PAYMENT_MATCH | EXACT, PARTIAL and WINDOW rows (R-RES-26); replaces payment_match_rule | RWB-E2-008, RWB-E2-027 | S2 rwb-treatment, called from the matchPayments activity of P8 rwb-payment (CG-B-TECH-07-2; ASM-B-TECH-07-2) |
| 2 | BOOKING_MATCH | Booking match rows (today's BookingMatchRules) | RWB-E2-007 | S2 rwb-treatment |

The R-UNI-xx rules that Epic 1 cites stay coded behaviour in Phase 1 and move into the UNIVERSAL package in Epic 3. No package is edited in place: a rule change is a new package version, and the version in force keeps serving every caller that does not ask for the new one.

Ownership follows the decision, not the caller. A service that needs a decision asks the owning service for it through the owner's contract and never evaluates another service's package in its own worker (DP-11; Architecture v5 slide 13). The registry holds every package, whichever service evaluates it: rule_package, rule_package_version, rule_row and rule_test_case are P7 tables of the Ownership Map v1, in schema rwb_decision (ASM-B-TECH-07-3).

# 3. The rule row and its Drools decision-table columns

A package workbook has two tabs. Rows holds the decision table and Tests holds the scenarios. The header block names the package and the fact type the conditions read; the column headers are the Drools decision-table columns. Every data row is one rule, and its NAME is the rule ID the decision log records.

| Column | ALLOC-031 | Meaning |
|---|---|---|
| RuleSet | ALLOCATION | The package code. Every row of the workbook belongs to one package. |
| Import | recovery.casewf.rules.facts.AllocationFacts | The fact class the conditions and actions read. A package imports one fact type. |
| RuleTable | Allocation | The generated rule-table name; it appears in the DRL and in the agenda listener output. |
| CONDITION | productGroup == "MORTGAGE" | First condition column: the product group of the case. |
| CONDITION | regionCode == "BKK" | Second condition column: the region of the case. |
| CONDITION | exposureBand >= 3 | Third condition column: a numeric band, so the row holds for band 3 and above. |
| ACTION | setTargetQueueCode("MTG-BKK-CO"); setOwnerRole("RW-CASEOWN"); setTimerSpec("3d") | What the row decides: the target queue, the owner role of the next state and the timer. |
| PRIORITY | 988 | The salience the parser generates from the row position: 1000 minus position 12. A higher value fires earlier. |
| NAME | ALLOC-031 | The Drools rule name and the rule ID written to the decision log. |

Read as one row: for a MORTGAGE case in region BKK with exposure band 3 or above, ALLOC-031 assigns queue MTG-BKK-CO, owner role RW-CASEOWN and a 3-day timer. The decision log records ALLOC-031 and the package version label, for example ALLOC-2026.12.

The Import line names the fact class of the owning service. In version 3 the fact classes sat in the single recovery module, at recovery.casewf.rules.facts.AllocationFacts and its neighbours. In the target each service carries its own fact class in its own Java package, th.co.scb.ace.workbench.recovery.<short without hyphen> of Rules R4; the exact class names of the 448 rules are Not specified in the source documents (CG-B-TECH-07-4; ASM-B-TECH-07-4). The workbook is unchanged by this: the Import line is the only cell that names the class.

Row order is the only priority an author sets. The parser writes salience from the row position: 1000 minus the position, so an earlier row fires before a later one. All rows of a package share one activation-group, the package code: when the first row fires, Drools cancels the rest of the group and exactly one row decides, even when several sets of conditions hold. The default row is last, its condition cells are blank so it matches any case, its action carries the fallback queue from DL24 and its salience is 0. ALLOCATION always has a default row; a load without one is refused.

The CONDITION cells read the facts object; they never read a table. ACTION cells set fields on the same fact object, and the caller maps those fields to the state service. This keeps the package free of SQL, of module classes and of personal data. The Import line names one fact class, and a package may not import a second.

# 4. Version lifecycle

A rule package version moves through six states, held in rule_package_version.status (DF-REF-282). The transitions are the control: nothing reaches IN_FORCE without an approval, and nothing leaves IN_FORCE without a rollback or a successor. The effective-date step is RulePackageEffectiveDateJob, at 00:01, which in the target runs as the JOB-20 Temporal Schedule rule promote in rwb-decision (P7) instead of a Quartz job in the module (ADR-016; CG-B-TECH-07-7; ASM-B-TECH-07-8).

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every load check passes | LOADED |
| None | Load | Any check fails: compile, schema, overlap, unreachable row, default row or scenario | REFUSED |
| LOADED | Approve | The approver is not the author and the change checklist is complete (E2-041) | APPROVED |
| APPROVED | RULE_PACKAGE_EFFECTIVE | RulePackageEffectiveDateJob at 00:01 finds valid_from <= today | IN_FORCE; the previous IN_FORCE version becomes SUPERSEDED in the same transaction |
| IN_FORCE | Rollback | An earlier version exists and a reason is given | ROLLED_BACK; the earlier version becomes IN_FORCE in the same transaction |
| IN_FORCE | RULE_PACKAGE_EFFECTIVE (successor) | A later approved version reaches its valid_from | SUPERSEDED; the successor becomes IN_FORCE |

The job is idempotent: a second run at 00:01 changes nothing, and an approved version with a future valid_from stays APPROVED until its date. A rollback is one call and one transaction: the version in force becomes ROLLED_BACK, the previous version becomes IN_FORCE, and the change log records the caller, the time and the reason. A version is never edited in place; its workbook, generated DRL, checksum and test result stay as loaded. SUPERSEDED and ROLLED_BACK versions remain readable for audit and for RuleCatalog, which serves the version a decision was made under.

A state change in the registry is not the end of the step. When JOB-20 promotes a version, rwb-decision publishes RulePackageInForce (EV-30) on rwb.decision.events.v1; each owning service consumes it, fetches the version, verifies the checksum and swaps it in. Until that swap the service keeps serving the version it already holds, and a refused version never replaces one that works (Architecture v5 slides 27 and 43; §6).

# 5. Checks at load

Every upload runs the same ordered set of checks before a version row is written. The order matters: the compile check runs first because no other check can read the table until the DRL compiles. The checks run in the registry, rwb-decision, on the workbook as uploaded; the owning service repeats the checksum check when it builds the KieBase (§6).

| Check | What it proves | On failure |
|---|---|---|
| Compile | The generated DRL compiles at the pinned Drools version; an error names the row and the cell. | Refused, MSG-P3-027 with check compile. |
| Schema | Every value in a list column exists in the LOV in force, every required column is present and no unknown column is used. | Refused, check schema, row and column named. |
| Overlap | No two rows in the package can match the same facts at the same priority. | Refused, check overlap, both rule IDs named. |
| Unreachable rows | No row is fully covered by an earlier row, so every row can fire. | Refused, check unreachable row, row named. |
| Default row | ALLOCATION has a last row with blank conditions that matches every case. | Refused, check default row. |
| Scenarios | At least rules.testcases.min (50) scenarios on the Tests tab pass, each through the same RuleEvaluator as production. | Refused, check scenario, failing scenario IDs named. |
| Dry run | The draft is evaluated against every open case and the cases whose result would change are counted by product, queue and rule. | Recorded in DF-REF-293 and shown to the approver; it does not block the load. |
| Checksum | The SHA-256 of the workbook and the generated DRL is stored and verified on every KieBase build. | Refused at cache build on a mismatch; incident to RW-PLATADM. |

A load that fails any blocking check is refused whole. No partial version is stored, no rule_package_version row is written, no Blob object is kept, and the error names every failed row, cell or scenario. The scenario runner calls the published RuleEvaluator, not a second engine, so a scenario that passes proves the production path. The dry run reports counts only: no case identifier, no fact and no person appears in it. The checksum is the link between the workbook in Blob, the DRL in the database and the version that serves decisions.

The dry run reads the open cases through the contracts of their owners: the registry holds no case facts of its own (ADR-014; DP-11). It is a read-only evaluation and writes neither a decision record nor an outbox row.

# 6. Runtime

The runtime is embedded Drools inside each of the 19 services, with the registry in rwb-decision. A caller passes a package code, a facts object and a business date and receives one RuleResult; it never receives a KieBase, a KieSession or any other Drools type. The package version is chosen at evaluation time, from the caller's date, and is returned in the result. Inside a service the caller is its own Temporal activity; from another service the caller asks that service, one hop, and never runs its package (Architecture v5 slides 13 and 24; DP-11).

| Component | Responsibility |
|---|---|
| KieBaseRegistry | Builds one KieBase from drl_source per package version, verifies the checksum, caches up to drools.kiebase.cache.max = 20 and evicts the least recently used entry. |
| RuleEvaluator | Published interface. Selects the IN_FORCE version for the date, inserts the facts, fires the package and returns RuleResult(packageCode, packageVersion, ruleId, outputs). Throws NoPackageInForce. |
| RuleCatalog | Published interface. RuleCatalog.row(ruleId, packageVersion) returns action_text, owner_role, timer_spec and outputs from rule_row only. |
| DecisionLogAgendaListener | Agenda event listener. Captures the Drools rule name of the one rule that fired and hands it to the evaluator. |
| NoPackageInForce | Checked exception with messageId MSG-P3-027. There is no default decision and no silent fallback. |
| RulePackageRepository | Reads rule_package and rule_package_version; selects the version by status and date. |

Where each part runs decides who owns what. KieBaseRegistry, RuleEvaluator, DecisionLogAgendaListener and NoPackageInForce are embedded in each of the 19 services, inside its worker, on its own task queue rwb-<service>; the evaluator is reached only through an activity, never from workflow code (T7; §7). RuleCatalog, RulePackageRepository, rule_package, rule_package_version, rule_row and rule_test_case sit in rwb-decision (P7); an owning service that needs the catalog asks rwb-decision through its published contract (CG-B-TECH-07-3; ASM-B-TECH-07-3).

The cache is keyed by package version, not by package. A new version builds its own KieBase on first use; the previous version stays cached while a caller still asks for it, and the least recently used entry is evicted when the cache reaches drools.kiebase.cache.max = 20. The metric drools_kiebase_builds_total counts builds, so a compile on every call is visible. A checksum mismatch refuses the version at load into the cache and raises an incident; the previous version keeps serving and the evaluator never falls back silently.

Loading a version is a contract of the registry. On RulePackageInForce (EV-30), or on first use after a start, the owning service calls GET /rule-models/{n}/{v} on rwb-decision, verifies the checksum, swaps the model in atomically and keeps the last good model if the new one fails to load (Architecture v5 slide 27). The published name and path of that operation are Not specified in the source documents beyond the Architecture v5 wording (CG-B-TECH-07-5; ASM-B-TECH-07-5).

RuleCatalog is the read path for callers that need the action text, the owner role, the timer or the outputs without evaluating: it reads rule_row by rule ID and package version and never reads drl_source or the workbook. RuleEvaluator is the only write path into Drools. NoPackageInForce is a checked refusal with MSG-P3-027: there is no default decision and no silent fallback to an earlier version.

# 7. Use from Temporal

Temporal workflow code is deterministic and replays. Drools is not deterministic from the workflow's point of view: it reads the database, builds or reads a KieBase and fires rules. It therefore sits behind an activity boundary and never runs in workflow code (T7).

- A CaseEvent signal arrives at the case router in rwb-case, which turns the Kafka event into a signalWithStart on the CaseWorkflow and forwards it to the stage child that owns the decision; the child runs on the owning service's queue rwb-<service> (Temporal and Drools design slide 14).

- The workflow calls EvaluateRulesActivity with the package code, the facts and the business date.

- The activity calls RuleEvaluator.evaluate. Drools runs in the activity thread, on the worker, outside the workflow.

- The activity returns RuleResult with packageCode, packageVersion, ruleId and outputs. Temporal records the result in the workflow history.

- The workflow calls RecordAndApplyActivity with the rule ID and the package version; the activity writes the decision record, the state change and the outbox row in one transaction in the owning service's schema, and the outbox publishes DecisionRecorded to rwb.decision-record.v1 (ADR-022).

- On replay, the workflow reads the recorded activity result and never calls RuleEvaluator again. A package version that takes effect later does not change the path or the recorded decision.

Version 3 wrote the log and applied the state in two activities, WriteDecisionLogActivity and then ApplyStateActivity. The realignment merges them into one RecordAndApply activity, because ADR-022 writes the record and the change in one transaction: if the record cannot be written, nothing moves. Version 3 is the loser of that conflict and the steps above are the version 4 order (CG-B-TECH-07-8; ASM-B-TECH-07-7).

The workflow carries no Drools type and no rule logic: it sees four fields and the step order. NoPackageInForce is non-retryable, so a missing package fails the workflow at once and writes nothing. The rule package version in the result is the audit link between the decision log, the version that was in force and the workbook in Blob. A rule change therefore needs no workflow version; only a change to the step order does, and that change passes the E2-040 replay gate.

# 8. Data

The rule store is two new tables and four added columns. Physical Schema v6 counts 93 tables: the previous 92, plus rule_package and rule_package_version, less payment_match_rule. Temporal's own tables are outside the Physical Schema and are not counted. All four rule tables are in schema rwb_decision with the login rwb_decision, the P7 schema of Rules R4 and ADR-014 (CG-B-TECH-07-9; ASM-B-TECH-07-9).

| Entity | Fields | DF-REF | Owner |
|---|---|---|---|
| rule_package | id, package_code, title, owner_role, hit_policy | 274 to 278 | P7 rwb-decision |
| rule_package_version | id, package_id, version_label, status, source_blob_ref, drl_source, checksum, valid_from, valid_to, author, approver, loaded_at, approved_at, test_result, dry_run_counts, rollback_of, change_checklist | 279 to 295 | P7 rwb-decision |
| rule_row (added) | package_version_id, drools_rule_name, outputs | 296 to 298 | P7 rwb-decision |
| rule_test_case (added) | package_version_id | 299 | P7 rwb-decision |
| payment_match_rule (retired) | All fields dropped; payment matching moves to PAYMENT_MATCH rows | 261 to 273 retired | retired |

rule_row stays the rule catalog (T6): the parsed, queryable copy of each row, linked to its package version, with outputs jsonb. A caller reads action_text, owner_role, timer_spec and target_queue_code from the catalog by rule ID and version; it never reads the package source. rule_package_version holds the workbook reference (source_blob_ref), the generated DRL, the checksum, the dates, the author and approver, the test result and the dry run counts. rule_test_case names the scenario and its package version, so the Tests tab is queryable. payment_match_rule is dropped and payment matching moves to PAYMENT_MATCH rows with match type, tolerance, window, grace and partial floor as decision-table columns; DF-REF-261 to DF-REF-273 are retired.

The decision records are not registry rows. Every service's schema carries its business tables plus outbox, inbox and decision_record (Architecture v5 slide 20); the service writes its record in the same transaction as its change, hash-linked to its previous record, and publishes DecisionRecorded. rwb-decision consumes rwb.decision-record.v1 into the central ledger (decision_log_entry) within 5 minutes, alerts on a gap, checks the chain at 02:00 (JOB-14) and seals the daily hash to WORM storage (ADR-022). The 93-table count of Physical Schema v6 stays the count of the target schema set; its distribution over the 19 schemas is the split work of RWB-PLT-NF06-DB (CG-B-TECH-07-9; ASM-B-TECH-07-9).

# 9. Roles

Six roles take part, and the separation of duty is enforced in the service, not only on a screen. Since the realignment the four governance roles act on the registry in rwb-decision, and SY-RULES is the identity of each service that evaluates its own packages; RW-PLATADM receives the cache and checksum incidents of all of them (ASM-B-TECH-07-3).

| Role | May do | Right |
|---|---|---|
| RW-COE | Authors the workbook, loads a package version and calls rollback | Rules and parameters CRUD |
| RW-RISK | Approves a package version | Rules and parameters A |
| RW-AUDIT | Reads versions, scenarios, dry run counts and the change log | Rules and parameters R |
| RW-REFADM | Prepares load files and lists; may not approve | Rules and parameters C (prepare only) |
| SY-RULES | Evaluates packages, runs the scenarios and the dry run, serves the catalog | Service identity; no endpoint right |
| RW-PLATADM | Operates the service and receives cache and checksum incidents | Platform administration U |

RW-COE authors and loads; RW-RISK approves; the same person cannot do both. The approve call checks approver != author and refuses with MSG-P7-002, so a role claim that combines the two does not defeat the control. RW-AUDIT reads every version, scenario, dry run count and change log entry but changes nothing. RW-REFADM prepares the file and the lists and may not approve. SY-RULES is the service identity that evaluates, runs the scenarios and the dry run and serves the catalog; it has no endpoint right. RW-PLATADM operates the service, receives the cache and checksum incidents and does not decide a rule.

A role is data, not a code constant: Recovery roles, scope, masking and the DoA table live in rwb-access (P4), and every call to the registry and to an evaluator is authorised through its authorise contract before the work starts (DP-08; Architecture v5 slide 14). The approver of a rule version is checked against the DoA table in rwb-access, and the delegation_limit rows stay P4 data (Ownership Map v1).

# 10. Delivery by epic

Phase 1 delivers the runtime and the authoring path, with the five Epic 1 packages loaded. Epic 2 adds three packages for engines that already exist. Epic 3 moves the universal rules and the case workflows onto the same evaluator. Every release date below is the date of the source, unchanged and tentative (ASM-B-TECH-07-13).

| Story | Scope | Release | Delivered in |
|---|---|---|---|
| E1-072 | Drools runtime and rule package store: rule_package, rule_package_version, the four added columns, KieBaseRegistry, RuleEvaluator, RuleCatalog, DecisionLogAgendaListener, NoPackageInForce and GET /admin/rule-packages. | 30 November 2026 (tentative) | The registry in rwb-decision (P7) and the embedded kit in the 19 services (PLT, DP-04) |
| E1-073 | Authoring, validation, scenarios, approval and rollback: workbook parser, compile, schema, overlap, unreachable and default checks, RuleScenarioRunner, RuleDryRun, five endpoints, RulePackageEffectiveDateJob and RuleScenarioBuildGate. | 30 November 2026 (tentative) | The registry endpoints in rwb-decision (P7) (CG-B-TECH-07-6; ASM-B-TECH-07-6) |
| E2-041 | Governance and audit report: change checklist in change_checklist, GET /admin/rule-packages/change-report and decisions per package version (the new home of E1-048). | 31 December 2026 (tentative) | rwb-decision (P7) |
| E2-042 | Epic 2 packages: RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH authored in the template, each with at least 50 scenarios, loaded through E1-073. | 31 December 2026 (tentative) | S2 rwb-treatment, with the registry in rwb-decision (P7) |
| Epic 3 | UNIVERSAL package: the R-UNI-xx rules that Epic 1 cites move from code to a package; case workflows call the same RuleEvaluator inside an activity. | Phase 2 | Every service, with the registry in rwb-decision (P7) |

The order keeps one engine and one authoring path. E1-072 gives every caller the same evaluator before any rule moves. E1-073 gives RW-COE and RW-RISK the control that makes a change safe. E2-042 proves the control on three more packages without a code release. Epic 3 closes the gap for the universal rules, and the case workflows of that phase use the same activity boundary as E2-043.

## 10.1 What each service carries after the realignment

| Item | Where it lives | Basis |
|---|---|---|
| KIE runtime libraries: drools-engine, drools-mvel, drools-decisiontables, drools-xml-support | Every one of the 19 services, from the service template | ADR-017; §1 |
| KieBaseRegistry with drools.kiebase.cache.max = 20 | Every service, keyed by package version | §6 |
| RuleEvaluator and the EvaluateRules activity | Every service, on task queue rwb-<service> | T7; §7 |
| RuleCatalog, RulePackageRepository, rule_package, rule_package_version, rule_row, rule_test_case | rwb-decision (P7), schema rwb_decision | Ownership Map v1; §8 |
| GET /rule-models/{n}/{v} and the /admin/rule-package paths | rwb-decision (P7), under /api/recovery/decision/v1 | Architecture v5 slide 14; Rules R4 |
| RulePackageInForce (EV-30) consumer and the model swap | Every service that owns a package | Architecture v5 slides 27 and 43 |
| Rule promote at 00:01 (JOB-20) and chain check at 02:00 (JOB-14) | rwb-decision (P7), as Temporal Schedules | Architecture v5 slide 44; ADR-016 |
| Decision record, outbox and inbox | Every service, in its own schema | ADR-022; Architecture v5 slide 20 |

The per-service work is a delta on top of the preserved Epic 1 stories: the kit is H RWB-PLT-E1072-CON and each service's local load is a C dependency on the rwb-decision contract, so no service waits for another service's build to start (DP-04; Rules R5.4).

# 11. References

- ADR-012 Evaluate rules with embedded Drools from versioned rule packages. It supersedes ADR-004.

- ADR-004 Rules as versioned data. Superseded by ADR-012; its principle is kept.

- ADR-017 Embedded Drools in each service, with the rule package registry in rwb-decision. It amends ADR-012 and D-RCV-36 T1 and T2.

- ADR-014 One schema and one login per service in the ACE PostgreSQL database.

- ADR-016 A reusable Temporal layer, and Temporal Schedules in place of Quartz.

- ADR-022 A local decision record plus a central ledger.

- D-RCV-36, decisions T3 (embedded KIE runtime only), T4 (workbook to approved version with rollback), T5 (first match), T6 (rule_row as catalog), T7 (Drools only in an activity) and T10 (payment_match_rule retired).

- D-RCV-60, the realignment decision, with DL44 (adopt Architecture v5), DL45 (service epics plus business-epic tags), DL46 (soft ownership by team type) and DL49 (gap and assumption registers).

- RWB-E1-072 Drools runtime and rule package store.

- RWB-E1-073 Rule authoring, validation, test scenarios, approval and rollback in Drools.

- RWB-E2-041 Rule change governance and audit report.

- RWB-E2-042 Epic 2 rule packages in Drools.

- Recovery Workbench Workflow Engine Design v3 (Temporal, activity boundary and the decision log order).

- Recovery Workbench Physical Schema v6 and Logical Data Model v8 (DF-REF-274 to DF-REF-299; 93 tables).

- Recovery Workbench Error and Message Standard v4 (MSG-P3-027, MSG-P7-002).

- Recovery Workbench Architecture v5 Text Extract v1, slides 11, 13, 14, 20, 24, 27, 28, 41, 43 and 44.

- Recovery Workbench Temporal and Drools Design Text Extract v1, slides 11 to 16 and 27.

- Recovery Workbench Microservice Ownership Map v1 (Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Rulings).

- Recovery Workbench Microservice Story Template and Rules v1 (R3 source precedence, R4 naming, R5.4 dependency classes, R5.5 DP-04, R5.7 lanes, R8.1 header, R9 gaps and assumptions).
