
The decision log: recorded locally at once, then sealed centrally

Every decision can be traced and cannot be quietly changed

1

Saved with the change
The service writes the decision and the change in one transaction

2

Chained
Each record is linked to the one before, so gaps or edits show

3

Collected centrally
rwb-decision reads rwb.decision-record.v1 into the ledger within 5 minutes

4

Sealed daily
A fingerprint is stored in write-once storage

inside each of the 19 services

in rwb-decision (P7)

Strict mode for points of no return
Debt transfer, write-off, auction sale and title transfer wait until the central ledger confirms the record. Everything else carries on at full speed.

What auditors get
One place to search every decision, with the rule version and approver; alerts for missing records; the chain checked every day.

This changes ADR-009, so it needs Risk and Internal Audit sign-off.

28

Notes: Proposal (changes ADR-009): (1) each service writes a decision record in its own schema in the same transaction as the state change, hash-linked to the previous record, plus DecisionRecorded through its outbox to topic rwb.decision-record.v1; (2) rwb-decision consumes it idempotently into the central ledger, with a 5-minute completeness target, gap alerts and chain verification; (3) daily anchor of the ledger hash to immutable (WORM) storage.

Strict mode: irreversible steps (debt transfer, write-off, auction sale, title transfer) wait for the ledger acknowledgement before executing.

Why not today's design: writing the central log synchronously inside every call becomes a distributed transaction once there are 19 services. Needs Risk and Internal Audit sign-off.

