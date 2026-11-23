
Points of no return: undo before, retry after

Each long deal is a chain of local steps (a saga) across services, run by the kit's Saga runner

Can still be undone

Must finish: retried until done

S2 Settlement

Agree terms

Approve (DoA)

Customer pays

Book ALS / NLEADS

Release collateral

Close case

payment reversed → case reopens

S5 Auction

Approve floor

Auction round

Award, buyer pays

Transfer title

Apply proceeds

Close or shortfall

no payment in 5 days → award cancelled

S7 Write-off

Scan

Build pack

Committee approves

Post to ALS / GL

Release provision

Track recovery

deferred → review timer

Point of no return

the central ledger confirms the decision record before this step (strict mode)

Before the line a step can be undone; after it Temporal keeps retrying until the step succeeds.

26

Notes: Saga pattern orchestrated by Temporal: each step is a local transaction; before the pivot each completed step has a compensating action; after the pivot steps are retried until they succeed.

S2 settlement: payment reversal reopens the case (R-SET-23/24); booking in ALS/NLEADS and collateral release (R-SET-21) are irreversible.
S5 auction: non-payment within 5 days cancels the award and reopens the round (R-DIS-49/50); title transfer via SCIS or Land Office is final (R-DIS-51/52).
S7 write-off: posting to ALS/GL is the pivot (R-WO-21); failures are re-posted, returned to scan or referred to committee (R-WO-44/45/46).

Aligned to v5 slides 26 and 28: each step is an activity on the owning service's queue, run by the kit's Saga runner (for example DebtSaleWorkflow in rwb-debtsale, settlement and deed in lieu in rwb-treatment). Every step writes its decision record with its change in one transaction (R-UNI-39). Strict mode at the point of no return: debt transfer, write-off posting, auction sale and title transfer wait until the central ledger in rwb-decision confirms the record; everything else carries on at full speed.

