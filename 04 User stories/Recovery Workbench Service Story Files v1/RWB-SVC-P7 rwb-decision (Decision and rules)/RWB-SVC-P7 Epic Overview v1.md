# RWB-SVC-P7 rwb-decision (Decision and rules) - Epic Overview v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Wave 1. Stories: 52. Ownership is suggested only; any team may pick up any story.

## Suggested owners

| Team type | Stories |
|---|---|
| ACE team (suggested; any team may pick up this story) | 1 |
| DevOps team (suggested; any team may pick up this story) | 3 |
| TechX (suggested; any team may pick up this story) | 48 |

## Day-1 stories

- RWB-P7-E1001-APP Recovery tables for the 14 data products
- RWB-P7-E1008-APP Decision log store v1, append only and hash chained
- RWB-P7-E1008-CON Decision log store v1, append only and hash chained
- RWB-P7-E1008-DB Decision log store v1, append only and hash chained
- RWB-P7-E1008-OPS Decision log store v1, append only and hash chained
- RWB-P7-E1017-APP Retention and archive rule for the data store
- RWB-P7-E1018-APP Case ID issuance and case record v1
- RWB-P7-E1020-APP Allocation and assignment engine v1
- RWB-P7-E1021-APP Transfer rules and engine v1
- RWB-P7-E1027-CON Decision log writer v1
- RWB-P7-E1028-APP Service levels, timers, escalation and prescription dates
- RWB-P7-E1030-APP Daily rebalancing and queue measures
- RWB-P7-E1032-APP Automatic attach from the OCR intake
- RWB-P7-E1039-APP Access log into the decision log and break-glass admin
- RWB-P7-E1046-APP Template and merge field catalog as data
- RWB-P7-E1052-APP Notice generation v1
- RWB-P7-E1054-APP Review queue for low-confidence documents
- RWB-P7-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools
- RWB-P7-E2001-APP EFS hand-over with full history
- RWB-P7-E2002-APP ACE plan status on the case
- RWB-P7-E2004-APP Treatment entity and plan timers data model
- RWB-P7-E2005-CON Decision log query API for audit
- RWB-P7-E2006-APP Credit approval pack for NLEADS
- RWB-P7-E2007-APP Booking confirmation from the ALS load
- RWB-P7-E2008-APP Payment matching with the missed payment event
- RWB-P7-E2012-APP Manual transfer and reassignment screen with reason
- RWB-P7-E2013-APP Approval routing with the delegation of authority table
- RWB-P7-E2013-CON Approval routing with the delegation of authority table
- RWB-P7-E2013-OPS Approval routing with the delegation of authority table
- RWB-P7-E2014-CON Approval screen for D7.1 demand and recall notices
- RWB-P7-E2014-OPS Approval screen for D7.1 demand and recall notices
- RWB-P7-E2017-APP Contract, CA and mortgage document generation screens
- RWB-P7-E2019-APP Partner identities through the external gateway
- RWB-P7-E2021-APP Letter dispatch loop with proof of delivery from WIN
- RWB-P7-E2022-APP SMS and LINE dispatch through NSS and LINE OA
- RWB-P7-E2024-APP Field app photos and bills into the document hub
- RWB-P7-E2025-APP Extraction for the stage 2 and 3 document types
- RWB-P7-E2026-APP Document generation engine for contract, CA and mortgage templates
- RWB-P7-E2027-APP Payment matching rules with the data team
- RWB-P7-E2028-APP Case intake agent live at L1 [E3a]
- RWB-P7-E2029-APP Deviation screening agent evaluation and L1 on one segment [E3b]
- RWB-P7-E2032-APP TDR offer-suggestion model through the model gateway [E3e]
- RWB-P7-E2035-APP Next action on the case
- RWB-P7-E2036-APP Queue write interface for models and agents
- RWB-P7-E2041-APP Rule change governance and audit report
- RWB-P7-E2042-APP Epic 2 rule packages in Drools
- RWB-P7-E2043-APP Temporal and Drools integration pattern and reference case workflow
- RWB-P7-E6028-APP Sell a post charge-off population
- RWB-P7-TE013-APP Agent runtime client with fallback

## Lanes

| Lane | Stories | Ready to start |
|---|---|---|
| CG-W1 | RWB-P7-E1008-CON, RWB-P7-E1027-CON | Day 1 |
| CG-W2 | RWB-P7-E2005-CON, RWB-P7-E2013-CON, RWB-P7-E2014-CON | Day 1 |
| L-P7-A | RWB-P7-E1001-APP | Day 1 |
| L-P7-AA | RWB-P7-E2017-APP | Day 1 |
| L-P7-AB | RWB-P7-E2019-APP | Day 1 |
| L-P7-AC | RWB-P7-E2021-APP | Day 1 |
| L-P7-AD | RWB-P7-E2022-APP | Day 1 |
| L-P7-AE | RWB-P7-E2024-APP | Day 1 |
| L-P7-AF | RWB-P7-E2025-APP | Day 1 |
| L-P7-AG | RWB-P7-E2026-APP | Day 1 |
| L-P7-AH | RWB-P7-E2027-APP | Day 1 |
| L-P7-AI | RWB-P7-E2028-APP | Day 1 |
| L-P7-AJ | RWB-P7-E2029-APP | Day 1 |
| L-P7-AK | RWB-P7-E2032-APP | Day 1 |
| L-P7-AL | RWB-P7-E2035-APP | Day 1 |
| L-P7-AM | RWB-P7-E2036-APP | Day 1 |
| L-P7-AN | RWB-P7-E2041-APP | Day 1 |
| L-P7-AO | RWB-P7-E2042-APP | Day 1 |
| L-P7-AP | RWB-P7-E2043-APP | Day 1 |
| L-P7-AQ | RWB-P7-E6028-APP | Day 1 |
| L-P7-AR | RWB-P7-TE013-APP | Day 1 |
| L-P7-B | RWB-P7-E1008-APP, RWB-P7-E1027-APP, RWB-P7-E2005-APP | After RWB-P7-E1008-APP; Day 1 |
| L-P7-C | RWB-P7-E1008-OPS | Day 1 |
| L-P7-D | RWB-P7-E1008-DB | Day 1 |
| L-P7-E | RWB-P7-E1017-APP | Day 1 |
| L-P7-F | RWB-P7-E1018-APP | Day 1 |
| L-P7-G | RWB-P7-E1020-APP | Day 1 |
| L-P7-H | RWB-P7-E1021-APP | Day 1 |
| L-P7-I | RWB-P7-E1028-APP | Day 1 |
| L-P7-J | RWB-P7-E1030-APP | Day 1 |
| L-P7-K | RWB-P7-E1032-APP | Day 1 |
| L-P7-L | RWB-P7-E1039-APP | Day 1 |
| L-P7-M | RWB-P7-E1046-APP | Day 1 |
| L-P7-N | RWB-P7-E1052-APP | Day 1 |
| L-P7-O | RWB-P7-E1054-APP | Day 1 |
| L-P7-P | RWB-P7-E1073-APP | Day 1 |
| L-P7-Q | RWB-P7-E2001-APP | Day 1 |
| L-P7-R | RWB-P7-E2002-APP | Day 1 |
| L-P7-S | RWB-P7-E2004-APP | Day 1 |
| L-P7-T | RWB-P7-E2006-APP | Day 1 |
| L-P7-U | RWB-P7-E2007-APP | Day 1 |
| L-P7-V | RWB-P7-E2008-APP | Day 1 |
| L-P7-W | RWB-P7-E2012-APP | Day 1 |
| L-P7-X | RWB-P7-E2013-APP, RWB-P7-E2014-APP | After RWB-P7-E2013-APP; Day 1 |
| L-P7-Y | RWB-P7-E2013-OPS | Day 1 |
| L-P7-Z | RWB-P7-E2014-OPS | Day 1 |
