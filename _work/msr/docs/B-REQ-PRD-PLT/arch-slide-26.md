
Deals that span services: undo before the point of no return, finish after it

Debt sale example: seven steps across five services, no shared transaction

Can still be undone

Must finish: retried until done

1. Reserve accounts
rwb-debtsale

2. Approve sale
rwb-decision

3. Buyer pays
rwb-payment

4. Transfer accounts
rwb-debtsale

5. Post proceeds
rwb-payment

6. Close cases
rwb-case

7. Tell customers
rwb-comms

Point of no return

undo: release accounts

undo: cancel approval

undo: refund buyer

If a step fails after this point it is retried, not undone

Settlement

Agree terms

Approve

Customer pays

Debt released

Post

Close case

Deed in lieu

Value asset

Approve

Sign deed

Title transferred

Book asset

Close case

Every step is a Temporal activity on the owner's queue; at each point of no return the ledger must confirm first.

26

Notes: Saga pattern (microservices.io), orchestrated by DebtSaleWorkflow in rwb-debtsale using the Saga runner from the workflow kit. Each step is a local transaction in one service's own schema, called as an activity on that service's queue. Before the pivot step, each completed step has a compensating activity. The pivot is the point of no return; after it, steps are retried until they succeed.

Strict decision-log mode applies at each pivot: the step waits for the central ledger acknowledgement before executing.

Other sagas: settlement and deed in lieu in rwb-treatment (pivots: debt released once the customer pays; title transfer registered).

