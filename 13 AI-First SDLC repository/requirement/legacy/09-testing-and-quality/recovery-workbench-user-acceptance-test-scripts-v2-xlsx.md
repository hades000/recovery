<!-- source: 09 Testing and quality/Recovery Workbench User Acceptance Test Scripts v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `09 Testing and quality/Recovery Workbench User Acceptance Test Scripts v2.xlsx`  
> **Converted from:** XLSX

## Scripts

| UAT scripts |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 16 scripts across the eight releases. Each tester records the result and any defect ID. |  |  |  |  |  |  |  |  |  |
| ID | Epic | Script | Who | Steps | Expected | Result | Defect | Tester | Date |
| UAT-01 | E1 | Case list matches the core bank | Data steward; business tester | Open the case list for Mortgage; compare the count with the inventory report for the same business date | Counts match; every case shows its owner, queue and business date |  |  |  |  |
| UAT-02 | E1 | Find a document by case | Document services | Search a case number; open the title deed; check the extracted title number | Document found; field correct or in the review queue |  |  |  |  |
| UAT-03 | E1 | Decision log shows an allocation | Internal audit | Search the decision log for a new case | Entry with the allocation row, version and queue |  |  |  |  |
| UAT-04 | E2 | Take over a new case | Case owner | Open My work; open the new case; read the history from collections | Owner, clocks and history shown; prescription date set |  |  |  |  |
| UAT-05 | E2 | Transfer a case | Team manager | Transfer a case with and without a reason; to an owner at the cap | Refused without a reason; refused at the cap; transferred otherwise with the reason logged |  |  |  |  |
| UAT-06 | E2 | Approve within and above the limit | Approver | Approve a decision within the limit, then one above | First approved and logged; second routed to the next level |  |  |  |  |
| UAT-07 | E2 | Approve a notice and see proof of delivery | Litigation officer | Approve a generated demand notice; check the WIN barcode and proof the next week | Notice sent; proof attached; notice period started |  |  |  |  |
| UAT-08 | E2 | Raise a deviation | Case owner | Raise X1 on a case | Case on hold; contact stop applied; prescription date still shown |  |  |  |  |
| UAT-09 | E3 | Settle a case to booking | Restructuring officer; approver; Credit Administration | Build a settlement offer below the floor; approve; book in ALS; check the next-day confirmation | Routed for approval; booked; confirmed from the load |  |  |  |  |
| UAT-10 | E3 | List an asset | Sale officer | Set the list and floor price; publish to HOME.SCB | Floor within the limit; listing published |  |  |  |  |
| UAT-11 | E4 | Decide the route | Case owner; approver | Open the route recommendation; override with a reason; approve | Recommendation with reasons; override logged; route set |  |  |  |  |
| UAT-12 | E5 | Instruct a law firm | Litigation officer; law firm user | Approve a pack; the firm accepts and records filing | Instruction issued by rule; filing recorded with the black case number |  |  |  |  |
| UAT-13 | E6 | Award a debt sale lot | Debt sale officer; Head of Asset Liquidity | Build a lot; approve; open the data room; award | Tape masked; award above the reserve; accounts closed as sold |  |  |  |  |
| UAT-14 | E6 | Write off at committee | Write-off team; committee | Run the scan; remove a case with a reason; approve at committee | Population correct; removal logged; postings sent |  |  |  |  |
| UAT-15 | E7 | Handle a deceased customer | Hardship and vulnerability specialist | Raise X3; record the estate claim | Contact stopped; claim deadline set |  |  |  |  |
| UAT-16 | E8 | Change a limit without a release | Reference data administrator; Risk | Load a new delegation version with a future date; approve | New limit applies from its date; old decisions keep theirs |  |  |  |  |
