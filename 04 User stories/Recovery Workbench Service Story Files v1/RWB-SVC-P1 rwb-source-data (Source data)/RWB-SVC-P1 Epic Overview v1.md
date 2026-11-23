# RWB-SVC-P1 rwb-source-data (Source data) - Epic Overview v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Wave 1. Stories: 62. Ownership is suggested only; any team may pick up any story.

## Suggested owners

| Team type | Stories |
|---|---|
| ACE team (suggested; any team may pick up this story) | 4 |
| DevOps team (suggested; any team may pick up this story) | 9 |
| TechX (suggested; any team may pick up this story) | 49 |

## Day-1 stories

- RWB-P1-ACE001-DB ACE DB additions for the Recovery Workbench
- RWB-P1-AD018-CON Interface and job monitor
- RWB-P1-AD018-OPS Interface and job monitor
- RWB-P1-AD019-OPS Data quality and reconciliation console
- RWB-P1-DM001-APP Migrate account and arrears
- RWB-P1-DM002-APP Migrate customer and party
- RWB-P1-E1001-APP Recovery tables for the 14 data products
- RWB-P1-E1002-CON Case list v1 with case ID, owner and queue
- RWB-P1-E1002-OPS Case list v1 with case ID, owner and queue
- RWB-P1-E1011-CON Reconciliation and data quality report
- RWB-P1-E1011-OPS Reconciliation and data quality report
- RWB-P1-E1013-APP Baseline measures
- RWB-P1-E1015-CON Freshness stamp per data product
- RWB-P1-E1015-OPS Freshness stamp per data product
- RWB-P1-E1016-CON Access control per data product and catalog entries
- RWB-P1-E1016-DB Access control per data product and catalog entries
- RWB-P1-E1017-CON Retention and archive rule for the data store
- RWB-P1-E1017-OPS Retention and archive rule for the data store
- RWB-P1-E1018-APP Case ID issuance and case record v1
- RWB-P1-E1055-APP Proof of delivery capture design with WIN
- RWB-P1-E1064-CON Data dictionary for the 14 data products
- RWB-P1-E1064-OPS Data dictionary for the 14 data products
- RWB-P1-E1065-CON Sandbox database with synthetic recovery data
- RWB-P1-E1065-DB Sandbox database with synthetic recovery data
- RWB-P1-E1066-APP Interaction ledger store and writer
- RWB-P1-E1066-CON Interaction ledger store and writer
- RWB-P1-E1066-OPS Interaction ledger store and writer
- RWB-P1-E1067-CON Every Workbench action into the interaction ledger
- RWB-P1-E1069-DB Read-only ACE source views, grants and boundary rule
- RWB-P1-E2001-APP EFS hand-over with full history
- RWB-P1-E2007-APP Booking confirmation from the ALS load
- RWB-P1-E2008-APP Payment matching with the missed payment event
- RWB-P1-E2010-CON Stage 2 data products: contracts, plans and treatments
- RWB-P1-E2010-OPS Stage 2 data products: contracts, plans and treatments
- RWB-P1-E2021-APP Letter dispatch loop with proof of delivery from WIN
- RWB-P1-E2022-APP SMS and LINE dispatch through NSS and LINE OA
- RWB-P1-E2034-APP Interaction ledger on the case and from every channel

## Lanes

| Lane | Stories | Ready to start |
|---|---|---|
| CG-W1 | RWB-P1-E1002-CON, RWB-P1-E1011-CON, RWB-P1-E1015-CON, RWB-P1-E1016-CON, RWB-P1-E1017-CON, RWB-P1-E1064-CON, RWB-P1-E1065-CON, RWB-P1-E1066-CON, RWB-P1-E1067-CON | Day 1 |
| CG-W2 | RWB-P1-E2010-CON | Day 1 |
| CG-W4 | RWB-P1-AD018-CON | Day 1 |
| L-P1-A | RWB-P1-ACE001-DB, RWB-P1-AD018-APP, RWB-P1-AD019-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-DM014-APP, RWB-P1-E1001-APP, RWB-P1-E1002-APP, RWB-P1-E1011-APP, RWB-P1-E1015-APP, RWB-P1-E1016-APP, RWB-P1-E1017-APP, RWB-P1-E1064-APP, RWB-P1-E1065-APP, RWB-P1-E1069-APP, RWB-P1-E2010-APP | After RWB-P1-E1001-APP, RWB-P1-ACE001-DB; After RWB-P1-E1001-APP, RWB-P1-E1064-APP; After RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP; After RWB-P1-E1001-APP, RWB-P1-E1069-APP; After RWB-P1-E1015-APP, RWB-P1-E1069-APP; After RWB-P1-E1069-APP; After RWB-P1-E1069-APP, RWB-P1-E1015-APP; Day 1 |
| L-P1-B | RWB-P1-AD018-OPS | Day 1 |
| L-P1-C | RWB-P1-AD019-OPS | Day 1 |
| L-P1-D | RWB-P1-DM001-APP | Day 1 |
| L-P1-E | RWB-P1-DM002-APP | Day 1 |
| L-P1-F | RWB-P1-E1002-OPS | Day 1 |
| L-P1-G | RWB-P1-E1011-OPS | Day 1 |
| L-P1-H | RWB-P1-E1013-APP | Day 1 |
| L-P1-I | RWB-P1-E1015-OPS | Day 1 |
| L-P1-J | RWB-P1-E1016-DB | Day 1 |
| L-P1-K | RWB-P1-E1017-OPS | Day 1 |
| L-P1-L | RWB-P1-E1018-APP | Day 1 |
| L-P1-M | RWB-P1-E1055-APP | Day 1 |
| L-P1-N | RWB-P1-E1064-OPS | Day 1 |
| L-P1-O | RWB-P1-E1065-DB | Day 1 |
| L-P1-P | RWB-P1-E1066-APP, RWB-P1-E1067-APP, RWB-P1-E1068-APP | After RWB-P1-E1066-APP; Day 1 |
| L-P1-Q | RWB-P1-E1066-OPS | Day 1 |
| L-P1-R | RWB-P1-E1069-DB | Day 1 |
| L-P1-S | RWB-P1-E2001-APP | Day 1 |
| L-P1-T | RWB-P1-E2007-APP | Day 1 |
| L-P1-U | RWB-P1-E2008-APP | Day 1 |
| L-P1-V | RWB-P1-E2010-OPS | Day 1 |
| L-P1-W | RWB-P1-E2021-APP | Day 1 |
| L-P1-X | RWB-P1-E2022-APP | Day 1 |
| L-P1-Y | RWB-P1-E2034-APP | Day 1 |
