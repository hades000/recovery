<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->

# ADR-012 Evaluate rules with embedded Drools from versioned rule packages

- Status: Accepted
- Date: 16 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-36; supersedes ADR-004

### Context and problem

Thresholds, limits, routes, timers and templates change often. If they are written in code, every change needs a release, and the business waits a month to move a number. ADR-004 held every rule as a versioned row, evaluated by a decision-table component built in the recovery module. That component is code the squads maintain: the parser, the checks, the test runner, the dry run and the rollback. Each new shape of condition or output is a change to it, and a rule author is limited to the shapes the component was built for.

Drools is approved as an embedded library. The question is how rules are authored, evaluated and versioned, and whether a rules engine runs beside the Workbench or inside it.

### Decision drivers

- A business change without a code release
- An audit trail of which rule version decided each case
- Open cases kept on the version they were decided under
- One evaluator for the engines, the tests and the dry run, so a passed test means the same result in production
- No new server to operate and no new release path
- Rules as versioned data, the principle ADR-004 set

### Options considered

1. Embedded Drools, with XLS decision-table workbooks held as versioned data in the database
2. Drools rules shipped as code, built into the release
3. A separate KIE server or Business Central, with KJARs deployed to it

### Decision

Option 1. Drools is embedded in the recovery module with the KIE runtime libraries only: `drools-engine`, `drools-mvel`, `drools-decisiontables` and `drools-xml-support`. There is no KIE Server, no Business Central and no KJAR in Maven.

- RW-COE authors each package as an Excel workbook in Drools XLS decision-table format. On upload the workbook is compiled to a KieBase, checked, and run against its scenarios and a dry run. It is stored as a `rule_package_version` row with the workbook in Blob, the generated DRL and a checksum.
- RW-RISK approves. The author cannot approve. The version is in force from its valid-from date, and rollback is one call. A rule change needs no release.
- First match is kept. Each decision table has RuleSet = package code, each row is a rule whose NAME is the rule ID, rows share one activation-group, and salience follows row order, so exactly one row decides. The default row is last.
- `rule_row` stays as the rule catalog: the parsed, queryable copy of each row, linked to its package version, with `outputs` jsonb. Stories read action text, owner role, timer spec and target queue from the catalog by rule ID and version, not from the package source.
- Evaluation happens only inside a Temporal activity from Epic 3. The package version is chosen at evaluation time, returned in the `RuleResult` and written to the decision log. `decision_log_entry.rule_id` and `rule_version` keep their columns and now carry the Drools rule name and the package version label.
- `payment_match_rule` is dropped. Payment matching is package PAYMENT_MATCH, with match type, tolerance, window, grace and partial floor as decision-table columns.
- The R-UNI-xx rules that Epic 1 cites stay coded and are cited by ID in Phase 1. They move into a UNIVERSAL package in Epic 3.

### Consequences

- Good: a threshold, route or timer moves on its effective date with no release, and rolls back the same way.
- Good: the decision log records the rule ID and the package version for every move, in the columns that already exist.
- Good: one evaluator serves the engines, the scenarios, the dry run and the build gate, so a scenario that passes proves the production path.
- Good: rules stay versioned data, which is ADR-004's principle, now with a standard authoring format and a compiler that checks it.
- Good: no KIE Server, no Business Central and no KJAR to operate or deploy. The engine is a library in the same service.
- Bad: RW-COE must be trained in XLS decision-table authoring: RuleSet and RuleTable rows, condition and action columns, salience from row order, the default row and the Tests tab. The template reduces the risk but does not remove the skill change.
- Bad: the Drools library is a dependency the squads must upgrade: a pinned version per release, a compatibility check against `drl_source` in every stored package, and a regression run of every in-force package's scenarios on every build.
- Bad: a package that compiles can still be wrong. The checks and the scenarios catch less than a code review, so the dry run over open cases and the Risk approval carry more weight.
- Bad: the package store, the checksum and the Blob reference are new data the Workbench owns, and a corrupt or missing DRL refuses the version at load into the cache until it is fixed.

---
