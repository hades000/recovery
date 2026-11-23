
Changing a rule: no software release, four-eyes, dated, one-call rollback

The business owns the rule; IT owns the engine

Author
RW-COE edits the Excel decision table

1

Compile
Table → DRL → KieBase + checksum

2

Check + test
overlap, default row, 50+ scenarios

3

Approve
RW-RISK; author can't approve

4

Go live
rwb-decision publishes EV-30 at 00:01

5

Run
owning service checks and swaps it in

6

rollback: one call

WHAT IS STORED FOR EVERY VERSION  (rule_package_version)

Workbook (Blob)

Generated DRL

SHA-256

Valid-from date

Approver

PHASE 1 PACKAGES

ENTRY

EXCLUSION

ALLOCATION

ASSIGNMENT

TRANSFER

RESTRUCTURE

PAYMENT_MATCH

BOOKING_MATCH

A rule change is data, not code: tested, approved and dated, with the version stamped on every answer.

15

Notes: T4: RW-COE writes each rule package as an Excel workbook in Drools XLS decision-table format. On upload the workbook is compiled to a KieBase, checked and run against at least 50 scenarios (rules.testcases.min=50), then stored as a rule_package_version row with the workbook, the generated DRL and a checksum. RW-RISK approves; the author cannot approve. It is in force from its valid-from date; JOB-20 (a Temporal Schedule in rwb-decision) promotes at 00:01 and publishes RulePackageInForce (EV-30) on Kafka; each owning service fetches the model (GET /rule-models/{n}/{v}), verifies the checksum and swaps it in. Rollback is one call. Version states: LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED. Load checks: compile, schema, overlap, unreachable row, default row, at least 50 scenarios, dry run.

T6: rule_row stays as the parsed, queryable catalog (action_text, owner_role, timer_spec, target_queue_code read by rule ID and version).

Where it lives (v5): governance (authoring, tests, four-eyes approval, effective dating, version audit) is central in rwb-decision (P7); evaluation is local in the one service that owns each model, inside an activity, under 300 ms. No shared rule server on the hot path.

Target (v5 deck): move from XLS tables to OMG DMN 1.6 decision models table by table; the same Drools runtime executes both.

