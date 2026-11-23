# RWB-SVC-P3 rwb-case (Case and workflow) - Epic Overview v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Wave 1. Stories: 84. Ownership is suggested only; any team may pick up any story.

## Suggested owners

| Team type | Stories |
|---|---|
| ACE team (suggested; any team may pick up this story) | 1 |
| DevOps team (suggested; any team may pick up this story) | 10 |
| SCB IT infrastructure (suggested; any team may pick up this story) | 2 |
| TechX (suggested; any team may pick up this story) | 71 |

## Day-1 stories

- RWB-P3-AD019-APP Data quality and reconciliation console
- RWB-P3-E1002-APP Case list v1 with case ID, owner and queue
- RWB-P3-E1007-APP Integration adapters for outbound files
- RWB-P3-E1011-APP Reconciliation and data quality report
- RWB-P3-E1013-APP Baseline measures
- RWB-P3-E1018-CON Case ID issuance and case record v1
- RWB-P3-E1018-OPS Case ID issuance and case record v1
- RWB-P3-E1019-APP Roles, teams and queues as data
- RWB-P3-E1019-CON Roles, teams and queues as data
- RWB-P3-E1019-DB Roles, teams and queues as data
- RWB-P3-E1020-CON Allocation and assignment engine v1
- RWB-P3-E1020-OPS Allocation and assignment engine v1
- RWB-P3-E1021-CON Transfer rules and engine v1
- RWB-P3-E1021-OPS Transfer rules and engine v1
- RWB-P3-E1023-CON Case record view v1, read only
- RWB-P3-E1028-CON Service levels, timers, escalation and prescription dates
- RWB-P3-E1028-OPS Service levels, timers, escalation and prescription dates
- RWB-P3-E1030-CON Daily rebalancing and queue measures
- RWB-P3-E1030-OPS Daily rebalancing and queue measures
- RWB-P3-E1031-CON Queue and owner on the case list with filters
- RWB-P3-E1032-APP Automatic attach from the OCR intake
- RWB-P3-E1035-CON Case record view v1.1 with documents and history timeline
- RWB-P3-E1042-APP Central configuration service and parameter catalog
- RWB-P3-E1042-CON Central configuration service and parameter catalog
- RWB-P3-E1043-APP Reference data service with versioned tables
- RWB-P3-E1043-CON Reference data service with versioned tables
- RWB-P3-E1045-APP Multi-product parameters for Mortgage, HP and SSME
- RWB-P3-E1050-APP Document classification
- RWB-P3-E1052-APP Notice generation v1
- RWB-P3-E1054-APP Review queue for low-confidence documents
- RWB-P3-E1055-APP Proof of delivery capture design with WIN
- RWB-P3-E1065-APP Sandbox database with synthetic recovery data
- RWB-P3-E1066-APP Interaction ledger store and writer
- RWB-P3-E1067-APP Every Workbench action into the interaction ledger
- RWB-P3-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools
- RWB-P3-E1073-CON Rule authoring, validation, test scenarios, approval and rollback in Drools
- RWB-P3-E1073-INF Rule authoring, validation, test scenarios, approval and rollback in Drools
- RWB-P3-E2001-APP EFS hand-over with full history
- RWB-P3-E2002-APP ACE plan status on the case
- RWB-P3-E2004-CON Treatment entity and plan timers data model
- RWB-P3-E2004-OPS Treatment entity and plan timers data model
- RWB-P3-E2006-APP Credit approval pack for NLEADS
- RWB-P3-E2007-APP Booking confirmation from the ALS load
- RWB-P3-E2009-APP Steering dashboard v1 data set
- RWB-P3-E2011-CON Queue view screens: my queue, team queues, filters and ageing
- RWB-P3-E2012-APP Manual transfer and reassignment screen with reason
- RWB-P3-E2012-CON Manual transfer and reassignment screen with reason
- RWB-P3-E2012-OPS Manual transfer and reassignment screen with reason
- RWB-P3-E2013-APP Approval routing with the delegation of authority table
- RWB-P3-E2014-APP Approval screen for D7.1 demand and recall notices
- RWB-P3-E2015-APP Timers, escalation and the deviation flag on the case record view
- RWB-P3-E2015-CON Timers, escalation and the deviation flag on the case record view
- RWB-P3-E2015-OPS Timers, escalation and the deviation flag on the case record view
- RWB-P3-E2016-CON Full case record view with the history timeline
- RWB-P3-E2021-APP Letter dispatch loop with proof of delivery from WIN
- RWB-P3-E2024-APP Field app photos and bills into the document hub
- RWB-P3-E2033-APP Case and queue list with status, owner and ageing
- RWB-P3-E2034-APP Interaction ledger on the case and from every channel
- RWB-P3-E2035-APP Next action on the case
- RWB-P3-E2036-APP Queue write interface for models and agents
- RWB-P3-E2041-CON Rule change governance and audit report
- RWB-P3-E2042-CON Epic 2 rule packages in Drools
- RWB-P3-E2042-INF Epic 2 rule packages in Drools
- RWB-P3-E2042-OPS Epic 2 rule packages in Drools
- RWB-P3-E2043-APP Temporal and Drools integration pattern and reference case workflow
- RWB-P3-E2043-CON Temporal and Drools integration pattern and reference case workflow
- RWB-P3-E2043-OPS Temporal and Drools integration pattern and reference case workflow
- RWB-P3-E3013-APP Check encumbrance and eligibility before negotiation
- RWB-P3-E5002-APP Record proof of delivery on a notice
- RWB-P3-E6017-APP Route the population to the committee and schedule it
- RWB-P3-E6025-APP Close the case after the retention period

## Lanes

| Lane | Stories | Ready to start |
|---|---|---|
| CG-W1 | RWB-P3-E1018-CON, RWB-P3-E1019-CON, RWB-P3-E1020-CON, RWB-P3-E1021-CON, RWB-P3-E1023-CON, RWB-P3-E1028-CON, RWB-P3-E1030-CON, RWB-P3-E1031-CON, RWB-P3-E1035-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1073-CON | Day 1 |
| CG-W2 | RWB-P3-E2004-CON, RWB-P3-E2011-CON, RWB-P3-E2012-CON, RWB-P3-E2015-CON, RWB-P3-E2016-CON, RWB-P3-E2041-CON, RWB-P3-E2042-CON, RWB-P3-E2043-CON | Day 1 |
| L-P3-A | RWB-P3-AD019-APP | Day 1 |
| L-P3-AA | RWB-P3-E2006-APP | Day 1 |
| L-P3-AB | RWB-P3-E2007-APP | Day 1 |
| L-P3-AC | RWB-P3-E2009-APP | Day 1 |
| L-P3-AD | RWB-P3-E2012-APP, RWB-P3-E2015-APP, RWB-P3-E2016-APP | After RWB-P3-E2015-APP, RWB-P3-E2012-APP; Day 1 |
| L-P3-AE | RWB-P3-E2012-OPS | Day 1 |
| L-P3-AF | RWB-P3-E2013-APP | Day 1 |
| L-P3-AG | RWB-P3-E2014-APP | Day 1 |
| L-P3-AH | RWB-P3-E2015-OPS | Day 1 |
| L-P3-AI | RWB-P3-E2021-APP | Day 1 |
| L-P3-AJ | RWB-P3-E2024-APP | Day 1 |
| L-P3-AK | RWB-P3-E2033-APP | Day 1 |
| L-P3-AL | RWB-P3-E2034-APP | Day 1 |
| L-P3-AM | RWB-P3-E2035-APP | Day 1 |
| L-P3-AN | RWB-P3-E2036-APP | Day 1 |
| L-P3-AO | RWB-P3-E2042-OPS | Day 1 |
| L-P3-AP | RWB-P3-E2042-INF | Day 1 |
| L-P3-AQ | RWB-P3-E2043-OPS | Day 1 |
| L-P3-AR | RWB-P3-E2043-APP | Day 1 |
| L-P3-AS | RWB-P3-E3013-APP | Day 1 |
| L-P3-AT | RWB-P3-E5002-APP | Day 1 |
| L-P3-AU | RWB-P3-E6017-APP | Day 1 |
| L-P3-AV | RWB-P3-E6025-APP | Day 1 |
| L-P3-B | RWB-P3-E1002-APP | Day 1 |
| L-P3-C | RWB-P3-E1007-APP | Day 1 |
| L-P3-D | RWB-P3-E1011-APP | Day 1 |
| L-P3-E | RWB-P3-E1013-APP | Day 1 |
| L-P3-F | RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1023-APP, RWB-P3-E1028-APP, RWB-P3-E1030-APP, RWB-P3-E1031-APP, RWB-P3-E1035-APP, RWB-P3-E1045-APP, RWB-P3-E1073-APP, RWB-P3-E2004-APP, RWB-P3-E2011-APP, RWB-P3-E2041-APP, RWB-P3-E2042-APP | After RWB-P3-E1018-APP; After RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP; After RWB-P3-E1018-APP, RWB-P3-E1045-APP, RWB-P3-E2042-APP; After RWB-P3-E1020-APP; After RWB-P3-E1020-APP, RWB-P3-E1073-APP; After RWB-P3-E1023-APP; After RWB-P3-E1045-APP, RWB-P3-E1020-APP; After RWB-P3-E1073-APP; Day 1 |
| L-P3-G | RWB-P3-E1018-OPS | Day 1 |
| L-P3-H | RWB-P3-E1019-DB | Day 1 |
| L-P3-I | RWB-P3-E1020-OPS | Day 1 |
| L-P3-J | RWB-P3-E1021-OPS | Day 1 |
| L-P3-K | RWB-P3-E1028-OPS | Day 1 |
| L-P3-L | RWB-P3-E1030-OPS | Day 1 |
| L-P3-M | RWB-P3-E1032-APP | Day 1 |
| L-P3-N | RWB-P3-E1042-APP | Day 1 |
| L-P3-O | RWB-P3-E1043-APP | Day 1 |
| L-P3-P | RWB-P3-E1050-APP | Day 1 |
| L-P3-Q | RWB-P3-E1052-APP | Day 1 |
| L-P3-R | RWB-P3-E1054-APP | Day 1 |
| L-P3-S | RWB-P3-E1055-APP | Day 1 |
| L-P3-T | RWB-P3-E1065-APP | Day 1 |
| L-P3-U | RWB-P3-E1066-APP | Day 1 |
| L-P3-V | RWB-P3-E1067-APP | Day 1 |
| L-P3-W | RWB-P3-E1073-INF | Day 1 |
| L-P3-X | RWB-P3-E2001-APP | Day 1 |
| L-P3-Y | RWB-P3-E2002-APP | Day 1 |
| L-P3-Z | RWB-P3-E2004-OPS | Day 1 |
