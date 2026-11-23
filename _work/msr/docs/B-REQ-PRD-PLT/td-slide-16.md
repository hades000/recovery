
Inside a decision table: first match wins, one row decides

Each row is one rule; its name is the rule ID written to the decision record

| Rule ID | Product | Region | → Queue | → Owner role |
|---|---|---|---|---|
| ALLOC-010 | HIRE PURCHASE | any | HP-CO | RW-OFF |
| ALLOC-014 | MORTGAGE | BKK | MTG-BKK-CO | RW-OFF |
| ALLOC-015 | MORTGAGE | any | MTG-UPC-CO | RW-OFF |
| ALLOC-999 | any | any | GEN-CO | RW-OFF |


conditions

outputs

default row is always last  ·  other rows illustrative

Facts: new case
MORTGAGE · BKK

first match

ALLOC-014 fires
queue MTG-BKK-CO → officer U-03

WHAT COMES BACK  (RuleResult)

packageCode

ALLOCATION

packageVersion

ALLOC-2026.12

ruleId

ALLOC-014

outputs

queue, owner role

Decision record: ruleId + ruleVersion, hash-chained

Exactly one row decides, and its ID and version are logged, so every outcome can be explained.

16

Notes: Example from FSD P3 AC-P3-007: a MORTGAGE case in BKK matches ALLOC-014 and goes to queue MTG-BKK-CO; owner selection then picks the officer with the fewest cases (U-01/U-02/U-03 hold 120/95/140; U-02 had the last case, so U-03), skipping anyone at the cap of 150. Other rows on this slide are illustrative.

T5: first-match semantics. RuleSet = package code; each row is one rule whose NAME is the rule ID; rows share one activation-group; salience from row order; default row last. DecisionLogAgendaListener captures the rule that fired. KieBaseRegistry holds one KieBase per package version (LRU, max 20), never recompiled per call.

Version labels look like ALLOC-2026.12. Decision record (written by the owning service in its own schema, in the same transaction as the state change, then collected into the central ledger in rwb-decision): chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, prev_hash, entry_hash (append-only, hash-chained; JOB-14 checks the chain at 02:00).

