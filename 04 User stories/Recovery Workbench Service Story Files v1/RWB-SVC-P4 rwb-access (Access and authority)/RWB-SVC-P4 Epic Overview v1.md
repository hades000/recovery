# RWB-SVC-P4 rwb-access (Access and authority) - Epic Overview v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Wave 1. Stories: 111. Ownership is suggested only; any team may pick up any story.

## Suggested owners

| Team type | Stories |
|---|---|
| ACE team (suggested; any team may pick up this story) | 3 |
| DevOps team (suggested; any team may pick up this story) | 1 |
| SCB IT infrastructure (suggested; any team may pick up this story) | 1 |
| TechX (suggested; any team may pick up this story) | 106 |

## Day-1 stories

- RWB-P4-AD001-CON Map Entra ID groups to Workbench roles
- RWB-P4-AD002-APP Permission matrix as a versioned load
- RWB-P4-AD002-CON Permission matrix as a versioned load
- RWB-P4-AD003-APP Scope per role
- RWB-P4-AD003-CON Scope per role
- RWB-P4-AD004-APP Masking profiles per role
- RWB-P4-AD004-CON Masking profiles per role
- RWB-P4-AD005-CON Separation of duty check at sign-in
- RWB-P4-AD006-CON Break-glass access
- RWB-P4-AD006-DB Break-glass access
- RWB-P4-AD007-CON Access log search and export
- RWB-P4-AD008-CON Access review list
- RWB-P4-AD009-APP Load a list of values version
- RWB-P4-AD009-CON Load a list of values version
- RWB-P4-AD010-CON Approve a reference data load
- RWB-P4-AD011-APP Load a rule version
- RWB-P4-AD011-CON Load a rule version
- RWB-P4-AD012-CON Approve a rule version
- RWB-P4-AD013-CON Roll back a rule or reference version
- RWB-P4-AD014-APP Configure queues
- RWB-P4-AD014-CON Configure queues
- RWB-P4-AD015-APP Configure service levels and timers
- RWB-P4-AD015-CON Configure service levels and timers
- RWB-P4-AD016-CON Load the delegation of authority table
- RWB-P4-E1001-APP Recovery tables for the 14 data products
- RWB-P4-E1007-APP Integration adapters for outbound files
- RWB-P4-E1008-APP Decision log store v1, append only and hash chained
- RWB-P4-E1016-APP Access control per data product and catalog entries
- RWB-P4-E1018-APP Case ID issuance and case record v1
- RWB-P4-E1019-APP Roles, teams and queues as data
- RWB-P4-E1020-APP Allocation and assignment engine v1
- RWB-P4-E1021-APP Transfer rules and engine v1
- RWB-P4-E1022-APP Sign-on with SSO, MFA and the first roles
- RWB-P4-E1022-CON Sign-on with SSO, MFA and the first roles
- RWB-P4-E1022-DB Sign-on with SSO, MFA and the first roles
- RWB-P4-E1023-APP Case record view v1, read only
- RWB-P4-E1028-APP Service levels, timers, escalation and prescription dates
- RWB-P4-E1037-CON Role to permission matrix as data and PDPA field masking by role
- RWB-P4-E1038-APP Delegation of authority table as reference data
- RWB-P4-E1039-CON Access log into the decision log and break-glass admin
- RWB-P4-E1039-DB Access log into the decision log and break-glass admin
- RWB-P4-E1039-OPS Access log into the decision log and break-glass admin
- RWB-P4-E1054-APP Review queue for low-confidence documents
- RWB-P4-E1062-APP Deviation screening agent in shadow [E2b]
- RWB-P4-E1063-APP Agent monitoring dashboard v1 [E2c]
- RWB-P4-E1064-APP Data dictionary for the 14 data products
- RWB-P4-E1065-APP Sandbox database with synthetic recovery data
- RWB-P4-E1069-APP Read-only ACE source views, grants and boundary rule
- RWB-P4-E2002-APP ACE plan status on the case
- RWB-P4-E2003-APP Customer's other products on the case
- RWB-P4-E2004-APP Treatment entity and plan timers data model
- RWB-P4-E2007-APP Booking confirmation from the ALS load
- RWB-P4-E2008-APP Payment matching with the missed payment event
- RWB-P4-E2013-APP Approval routing with the delegation of authority table
- RWB-P4-E2014-APP Approval screen for D7.1 demand and recall notices
- RWB-P4-E2015-APP Timers, escalation and the deviation flag on the case record view
- RWB-P4-E2017-APP Contract, CA and mortgage document generation screens
- RWB-P4-E2019-CON Partner identities through the external gateway
- RWB-P4-E2019-INF Partner identities through the external gateway
- RWB-P4-E2021-APP Letter dispatch loop with proof of delivery from WIN
- RWB-P4-E2022-APP SMS and LINE dispatch through NSS and LINE OA
- RWB-P4-E2024-APP Field app photos and bills into the document hub
- RWB-P4-E2026-APP Document generation engine for contract, CA and mortgage templates
- RWB-P4-E2027-APP Payment matching rules with the data team
- RWB-P4-E2031-APP Agent monitoring dashboard v2 [E3d]
- RWB-P4-E2033-APP Case and queue list with status, owner and ageing
- RWB-P4-E2034-APP Interaction ledger on the case and from every channel
- RWB-P4-E2035-APP Next action on the case
- RWB-P4-E2036-APP Queue write interface for models and agents
- RWB-P4-E2041-APP Rule change governance and audit report
- RWB-P4-E2042-APP Epic 2 rule packages in Drools
- RWB-P4-E8006-APP Run the full administration screens
- RWB-P4-E8006-CON Run the full administration screens
- RWB-P4-E8007-APP Change a decision rule through the administration screens
- RWB-P4-E8007-CON Change a decision rule through the administration screens
- RWB-P4-E8008-APP Move an approval limit
- RWB-P4-E8008-CON Move an approval limit
- RWB-P4-E8009-APP Set the treatment policy by product
- RWB-P4-E8009-CON Set the treatment policy by product
- RWB-P4-E8010-APP Add a letter template with Compliance approval
- RWB-P4-E8010-CON Add a letter template with Compliance approval
- RWB-P4-E8011-APP Roll back a configuration version
- RWB-P4-E8011-CON Roll back a configuration version
- RWB-P4-E8012-APP Publish a panel change
- RWB-P4-E8012-CON Publish a panel change
- RWB-P4-E8013-APP Run a QA sample against the rule version applied
- RWB-P4-E8013-CON Run a QA sample against the rule version applied
- RWB-P4-E8014-APP Return a defective pack
- RWB-P4-E8014-CON Return a defective pack
- RWB-P4-E8015-APP Detect a broken hash chain in the decision log
- RWB-P4-E8015-CON Detect a broken hash chain in the decision log
- RWB-P4-E8016-APP Handle a data subject request
- RWB-P4-E8016-CON Handle a data subject request
- RWB-P4-E8017-APP Manage an incident
- RWB-P4-E8017-CON Manage an incident
- RWB-P4-E8018-APP Refer a case to Aric
- RWB-P4-E8018-CON Refer a case to Aric
- RWB-P4-E8019-APP Control access by role and by agent
- RWB-P4-E8019-CON Control access by role and by agent

## Lanes

| Lane | Stories | Ready to start |
|---|---|---|
| CG-W1 | RWB-P4-E1022-CON, RWB-P4-E1037-CON, RWB-P4-E1039-CON | Day 1 |
| CG-W2 | RWB-P4-E2019-CON | Day 1 |
| CG-W4 | RWB-P4-AD001-CON, RWB-P4-AD002-CON, RWB-P4-AD003-CON, RWB-P4-AD004-CON, RWB-P4-AD005-CON, RWB-P4-AD006-CON, RWB-P4-AD007-CON, RWB-P4-AD008-CON, RWB-P4-AD009-CON, RWB-P4-AD010-CON, RWB-P4-AD011-CON, RWB-P4-AD012-CON, RWB-P4-AD013-CON, RWB-P4-AD014-CON, RWB-P4-AD015-CON, RWB-P4-AD016-CON, RWB-P4-E8006-CON, RWB-P4-E8007-CON, RWB-P4-E8008-CON, RWB-P4-E8009-CON, RWB-P4-E8010-CON, RWB-P4-E8011-CON, RWB-P4-E8012-CON, RWB-P4-E8013-CON, RWB-P4-E8014-CON, RWB-P4-E8015-CON, RWB-P4-E8016-CON, RWB-P4-E8017-CON, RWB-P4-E8018-CON, RWB-P4-E8019-CON | Day 1 |
| L-P4-A | RWB-P4-AD001-APP, RWB-P4-AD005-APP, RWB-P4-AD006-APP, RWB-P4-AD007-APP, RWB-P4-AD008-APP, RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-E1039-APP, RWB-P4-E2019-APP | After RWB-P4-E1022-APP; After RWB-P4-E1022-APP, RWB-P4-E1039-APP; After RWB-P4-E1039-APP; Day 1 |
| L-P4-AA | RWB-P4-E1064-APP | Day 1 |
| L-P4-AB | RWB-P4-E1065-APP | Day 1 |
| L-P4-AC | RWB-P4-E1069-APP | Day 1 |
| L-P4-AD | RWB-P4-E2002-APP | Day 1 |
| L-P4-AE | RWB-P4-E2003-APP | Day 1 |
| L-P4-AF | RWB-P4-E2004-APP | Day 1 |
| L-P4-AG | RWB-P4-E2007-APP | Day 1 |
| L-P4-AH | RWB-P4-E2008-APP | Day 1 |
| L-P4-AI | RWB-P4-E2013-APP | Day 1 |
| L-P4-AJ | RWB-P4-E2014-APP | Day 1 |
| L-P4-AK | RWB-P4-E2015-APP | Day 1 |
| L-P4-AL | RWB-P4-E2017-APP | Day 1 |
| L-P4-AM | RWB-P4-E2019-INF | Day 1 |
| L-P4-AN | RWB-P4-E2021-APP | Day 1 |
| L-P4-AO | RWB-P4-E2022-APP | Day 1 |
| L-P4-AP | RWB-P4-E2024-APP | Day 1 |
| L-P4-AQ | RWB-P4-E2026-APP | Day 1 |
| L-P4-AR | RWB-P4-E2027-APP | Day 1 |
| L-P4-AS | RWB-P4-E2031-APP | Day 1 |
| L-P4-AT | RWB-P4-E2033-APP | Day 1 |
| L-P4-AU | RWB-P4-E2034-APP | Day 1 |
| L-P4-AV | RWB-P4-E2035-APP | Day 1 |
| L-P4-AW | RWB-P4-E2036-APP | Day 1 |
| L-P4-AX | RWB-P4-E2041-APP | Day 1 |
| L-P4-AY | RWB-P4-E2042-APP | Day 1 |
| L-P4-AZ | RWB-P4-E8006-APP | Day 1 |
| L-P4-B | RWB-P4-AD002-APP | Day 1 |
| L-P4-BA | RWB-P4-E8007-APP | Day 1 |
| L-P4-BB | RWB-P4-E8008-APP | Day 1 |
| L-P4-BC | RWB-P4-E8009-APP | Day 1 |
| L-P4-BD | RWB-P4-E8010-APP | Day 1 |
| L-P4-BE | RWB-P4-E8011-APP | Day 1 |
| L-P4-BF | RWB-P4-E8012-APP | Day 1 |
| L-P4-BG | RWB-P4-E8013-APP | Day 1 |
| L-P4-BH | RWB-P4-E8014-APP | Day 1 |
| L-P4-BI | RWB-P4-E8015-APP | Day 1 |
| L-P4-BJ | RWB-P4-E8016-APP | Day 1 |
| L-P4-BK | RWB-P4-E8017-APP | Day 1 |
| L-P4-BL | RWB-P4-E8018-APP | Day 1 |
| L-P4-BM | RWB-P4-E8019-APP | Day 1 |
| L-P4-C | RWB-P4-AD003-APP | Day 1 |
| L-P4-D | RWB-P4-AD004-APP | Day 1 |
| L-P4-E | RWB-P4-AD006-DB | Day 1 |
| L-P4-F | RWB-P4-AD009-APP, RWB-P4-AD010-APP | After RWB-P4-AD009-APP; Day 1 |
| L-P4-G | RWB-P4-AD011-APP, RWB-P4-AD012-APP, RWB-P4-AD013-APP | After RWB-P4-AD011-APP; After RWB-P4-AD012-APP; Day 1 |
| L-P4-H | RWB-P4-AD014-APP | Day 1 |
| L-P4-I | RWB-P4-AD015-APP | Day 1 |
| L-P4-J | RWB-P4-AD016-APP, RWB-P4-E1038-APP | After RWB-P4-E1038-APP; Day 1 |
| L-P4-K | RWB-P4-E1001-APP | Day 1 |
| L-P4-L | RWB-P4-E1007-APP | Day 1 |
| L-P4-M | RWB-P4-E1008-APP | Day 1 |
| L-P4-N | RWB-P4-E1016-APP | Day 1 |
| L-P4-O | RWB-P4-E1018-APP | Day 1 |
| L-P4-P | RWB-P4-E1019-APP | Day 1 |
| L-P4-Q | RWB-P4-E1020-APP | Day 1 |
| L-P4-R | RWB-P4-E1021-APP | Day 1 |
| L-P4-S | RWB-P4-E1022-DB | Day 1 |
| L-P4-T | RWB-P4-E1023-APP | Day 1 |
| L-P4-U | RWB-P4-E1028-APP | Day 1 |
| L-P4-V | RWB-P4-E1039-OPS | Day 1 |
| L-P4-W | RWB-P4-E1039-DB | Day 1 |
| L-P4-X | RWB-P4-E1054-APP | Day 1 |
| L-P4-Y | RWB-P4-E1062-APP | Day 1 |
| L-P4-Z | RWB-P4-E1063-APP | Day 1 |
