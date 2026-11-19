<!-- source: 09 Testing and quality/Recovery Workbench User Acceptance Test Plan v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `09 Testing and quality/Recovery Workbench User Acceptance Test Plan v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

User acceptance test plan

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench user acceptance test plan |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119 |

# 1. What the business tests

The business tests what each release changes for its users: the main paths, the approvals, the notices and the controls. Business testers work with the squads during the build, so UAT confirms work they have already seen.

# 2. When

| Epic | UAT week | Sign-off |
|---|---|---|
| E1 | 23 Nov to 27 Nov | 27 Nov |
| E2 | 21 Dec to 25 Dec | 25 Dec |
| E3 | 18 Jan to 22 Jan | 22 Jan |
| E4 | 15 Feb to 19 Feb | 19 Feb |
| E5 | 15 Mar to 19 Mar | 19 Mar |
| E6 | 12 Apr to 16 Apr | 16 Apr |
| E7 | 10 May to 14 May | 14 May |
| E8 | 7 Jun to 11 Jun | 11 Jun |

# 3. Who

| Role | Tests |
|---|---|
| Business testers named for each release (DL09) | The scripts for their team |
| Business lead | Signs the UAT exit |
| Business analysts | Prepare the scripts and support |
| QA engineers | Log defects and retest |

# 4. Order

- Access: each tester signs in with their role and checks what they see.

- Main paths in the order the case moves.

- Approvals and limits.

- Notices and documents.

- Exceptions and deviations.

- Reports and measures.

# 5. Scripts

| ID | Epic | Script | Who | Steps | Expected |
|---|---|---|---|---|---|
| UAT-01 | E1 | Case list matches the core bank | Data steward; business tester | Open the case list for Mortgage; compare the count with the inventory report for the same business date | Counts match; every case shows its owner, queue and business date |
| UAT-02 | E1 | Find a document by case | Document services | Search a case number; open the title deed; check the extracted title number | Document found; field correct or in the review queue |
| UAT-03 | E1 | Decision log shows an allocation | Internal audit | Search the decision log for a new case | Entry with the allocation row, version and queue |
| UAT-04 | E2 | Take over a new case | Case owner | Open My work; open the new case; read the history from collections | Owner, clocks and history shown; prescription date set |
| UAT-05 | E2 | Transfer a case | Team manager | Transfer a case with and without a reason; to an owner at the cap | Refused without a reason; refused at the cap; transferred otherwise with the reason logged |
| UAT-06 | E2 | Approve within and above the limit | Approver | Approve a decision within the limit, then one above | First approved and logged; second routed to the next level |
| UAT-07 | E2 | Approve a notice and see proof of delivery | Litigation officer | Approve a generated demand notice; check the WIN barcode and proof the next week | Notice sent; proof attached; notice period started |
| UAT-08 | E2 | Raise a deviation | Case owner | Raise X1 on a case | Case on hold; contact stop applied; prescription date still shown |
| UAT-09 | E3 | Settle a case to booking | Restructuring officer; approver; Credit Administration | Build a settlement offer below the floor; approve; book in ALS; check the next-day confirmation | Routed for approval; booked; confirmed from the load |
| UAT-10 | E3 | List an asset | Sale officer | Set the list and floor price; publish to HOME.SCB | Floor within the limit; listing published |
| UAT-11 | E4 | Decide the route | Case owner; approver | Open the route recommendation; override with a reason; approve | Recommendation with reasons; override logged; route set |
| UAT-12 | E5 | Instruct a law firm | Litigation officer; law firm user | Approve a pack; the firm accepts and records filing | Instruction issued by rule; filing recorded with the black case number |
| UAT-13 | E6 | Award a debt sale lot | Debt sale officer; Head of Asset Liquidity | Build a lot; approve; open the data room; award | Tape masked; award above the reserve; accounts closed as sold |
| UAT-14 | E6 | Write off at committee | Write-off team; committee | Run the scan; remove a case with a reason; approve at committee | Population correct; removal logged; postings sent |
| UAT-15 | E7 | Handle a deceased customer | Hardship and vulnerability specialist | Raise X3; record the estate claim | Contact stopped; claim deadline set |
| UAT-16 | E8 | Change a limit without a release | Reference data administrator; Risk | Load a new delegation version with a future date; approve | New limit applies from its date; old decisions keep theirs |

# 6. Entry and exit

| Gate | Criteria |
|---|---|
| Entry | SIT exit met; scripts walked through; masked data loaded; testers have access |
| Exit | Every script passed or its defect accepted by the business lead; no open severity 1 or 2 |

# 7. Sign-off

| Role | Name | Date |
|---|---|---|
| Business lead |  |  |
| Product owner |  |  |
| Application owner |  |  |
