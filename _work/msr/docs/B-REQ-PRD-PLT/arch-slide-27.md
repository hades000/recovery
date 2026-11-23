
Rules: approved in one place, run inside the service that owns the decision

Business owns the rules; the workflow just asks for the answer

GOVERNED CENTRALLY · rule registry in rwb-decision (P7)

Author
Business writes the DMN decision table

Test
At least 50 test cases pass

Approve
Four-eyes sign-off

Publish
Event RulePackageInForce

RUN IN THE OWNING SERVICE (e.g. rwb-valuation)

Load
GET /rule-models/{n}/{v}, verify checksum, swap in

Evaluate
Inside an activity, under 300 ms

Record
Answer and model version in the decision record

Kafka: RulePackageInForce

Example

RouteDecisionWorkflow asks: which route for case 123?

Route model v14 answers: litigation (reasons L2, L5)

Decision record: v14, inputs, answer, approver

No shared rules server to fail: each service holds its own approved copy, and every answer names the version used.

27

Notes: Today (ADR-012): embedded Drools with XLS decision tables stored in the database; packages ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, RESTRUCTURE, PAYMENT_MATCH, BOOKING_MATCH, UNIVERSAL; route sets total 448 rules. RW-COE authors, RW-RISK approves, at least 50 test scenarios, JOB-20 promotes at 00:01, EV-30 RulePackageInForce refreshes the cache. DoA is reference data (delegation_limit). Rule evaluations 283-318k a month; target < 300 ms.

Proposal: OMG DMN 1.6 decision models (Drools supports DMN at conformance level 3). XLS decision tables are a Drools-native format compiled to DRL, separate from DMN; both run on the same Drools runtime, so tables are converted one at a time with no big bang.

Governance stays central in rwb-decision: authoring, test scenarios, four-eyes approval, effective dating, audit of every version. Evaluation is local: each model has exactly one owning service, which loads it, verifies the checksum, and swaps it atomically, keeping the last good model if a new one fails to load. This avoids a shared rule server on every hot path.

With Temporal: rules run in an activity, never in workflow code, so workflows stay deterministic and replays reuse the recorded result. The model name and version are written into the decision record.

