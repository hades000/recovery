# RWB-SVC-P6 rwb-comms (Communications) - Epic Overview v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Wave 1. Stories: 48. Ownership is suggested only; any team may pick up any story.

## Suggested owners

| Team type | Stories |
|---|---|
| DevOps team (suggested; any team may pick up this story) | 4 |
| SCB IT infrastructure (suggested; any team may pick up this story) | 1 |
| TechX (suggested; any team may pick up this story) | 43 |

## Day-1 stories

- RWB-P6-AD017-CON Manage letter and notice templates
- RWB-P6-E1007-APP Integration adapters for outbound files
- RWB-P6-E1011-APP Reconciliation and data quality report
- RWB-P6-E1019-APP Roles, teams and queues as data
- RWB-P6-E1032-APP Automatic attach from the OCR intake
- RWB-P6-E1046-APP Template and merge field catalog as data
- RWB-P6-E1046-CON Template and merge field catalog as data
- RWB-P6-E1049-APP OCR pipeline on the Workbench document hub
- RWB-P6-E1052-CON Notice generation v1
- RWB-P6-E1055-CON Proof of delivery capture design with WIN
- RWB-P6-E1055-INF Proof of delivery capture design with WIN
- RWB-P6-E1055-OPS Proof of delivery capture design with WIN
- RWB-P6-E1063-APP Agent monitoring dashboard v1 [E2c]
- RWB-P6-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools
- RWB-P6-E2013-APP Approval routing with the delegation of authority table
- RWB-P6-E2014-APP Approval screen for D7.1 demand and recall notices
- RWB-P6-E2017-APP Contract, CA and mortgage document generation screens
- RWB-P6-E2018-OPS E-signature flow for customers and the bank
- RWB-P6-E2021-CON Letter dispatch loop with proof of delivery from WIN
- RWB-P6-E2021-OPS Letter dispatch loop with proof of delivery from WIN
- RWB-P6-E2022-CON SMS and LINE dispatch through NSS and LINE OA
- RWB-P6-E2022-OPS SMS and LINE dispatch through NSS and LINE OA
- RWB-P6-E2026-APP Document generation engine for contract, CA and mortgage templates
- RWB-P6-E2042-APP Epic 2 rule packages in Drools
- RWB-P6-E4035-APP View the offer on LINE and web
- RWB-P6-E4035-CON View the offer on LINE and web
- RWB-P6-E4036-APP Accept an offer in self-service
- RWB-P6-E4036-CON Accept an offer in self-service
- RWB-P6-E4037-APP Pay in self-service
- RWB-P6-E4037-CON Pay in self-service
- RWB-P6-E4038-APP Raise a dispute in self-service
- RWB-P6-E4038-CON Raise a dispute in self-service
- RWB-P6-E4039-APP Maintain the contact repository
- RWB-P6-E4039-CON Maintain the contact repository
- RWB-P6-E4040-APP Record a custody movement of a document
- RWB-P6-E4040-CON Record a custody movement of a document
- RWB-P6-E4041-APP Answer a legal or audit document request
- RWB-P6-E4041-CON Answer a legal or audit document request
- RWB-P6-E4042-APP Apply retention on case closure
- RWB-P6-E4042-CON Apply retention on case closure
- RWB-P6-E5002-APP Record proof of delivery on a notice

## Lanes

| Lane | Stories | Ready to start |
|---|---|---|
| CG-W1 | RWB-P6-E1046-CON, RWB-P6-E1052-CON, RWB-P6-E1055-CON | Day 1 |
| CG-W2 | RWB-P6-E2021-CON, RWB-P6-E2022-CON | Day 1 |
| CG-W3 | RWB-P6-E4035-CON, RWB-P6-E4036-CON, RWB-P6-E4037-CON, RWB-P6-E4038-CON, RWB-P6-E4039-CON, RWB-P6-E4040-CON, RWB-P6-E4041-CON, RWB-P6-E4042-CON | Day 1 |
| CG-W4 | RWB-P6-AD017-CON | Day 1 |
| L-P6-A | RWB-P6-AD017-APP, RWB-P6-E1034-APP, RWB-P6-E1046-APP, RWB-P6-E1052-APP, RWB-P6-E1055-APP, RWB-P6-E2018-APP, RWB-P6-E2021-APP, RWB-P6-E2022-APP | After RWB-P6-E1034-APP; After RWB-P6-E1046-APP; After RWB-P6-E1052-APP; After RWB-P6-E1052-APP, RWB-P6-E1055-APP; After RWB-P6-E2022-APP; Day 1 |
| L-P6-AA | RWB-P6-E5002-APP | Day 1 |
| L-P6-B | RWB-P6-E1007-APP | Day 1 |
| L-P6-C | RWB-P6-E1011-APP | Day 1 |
| L-P6-D | RWB-P6-E1019-APP | Day 1 |
| L-P6-E | RWB-P6-E1032-APP | Day 1 |
| L-P6-F | RWB-P6-E1049-APP | Day 1 |
| L-P6-G | RWB-P6-E1055-OPS | Day 1 |
| L-P6-H | RWB-P6-E1055-INF | Day 1 |
| L-P6-I | RWB-P6-E1063-APP | Day 1 |
| L-P6-J | RWB-P6-E1073-APP | Day 1 |
| L-P6-K | RWB-P6-E2013-APP | Day 1 |
| L-P6-L | RWB-P6-E2014-APP | Day 1 |
| L-P6-M | RWB-P6-E2017-APP | Day 1 |
| L-P6-N | RWB-P6-E2018-OPS | Day 1 |
| L-P6-O | RWB-P6-E2021-OPS | Day 1 |
| L-P6-P | RWB-P6-E2022-OPS | Day 1 |
| L-P6-Q | RWB-P6-E2026-APP | Day 1 |
| L-P6-R | RWB-P6-E2042-APP | Day 1 |
| L-P6-S | RWB-P6-E4035-APP | Day 1 |
| L-P6-T | RWB-P6-E4036-APP | Day 1 |
| L-P6-U | RWB-P6-E4037-APP | Day 1 |
| L-P6-V | RWB-P6-E4038-APP | Day 1 |
| L-P6-W | RWB-P6-E4039-APP | Day 1 |
| L-P6-X | RWB-P6-E4040-APP | Day 1 |
| L-P6-Y | RWB-P6-E4041-APP | Day 1 |
| L-P6-Z | RWB-P6-E4042-APP | Day 1 |
