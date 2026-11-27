## Sheet: Read me

| SCB Collections and Recovery. Henka Group, 22 November 2026. |
|---|
| (C) Siam Commercial Bank and Henka Pte Ltd |
| Recovery Workbench Users Roles and Permissions v5 (D-RCV-60 microservice realignment) |
| Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Status: Draft. Supersedes v4 of 15 November 2026. |
| Source: Recovery Workbench Users Roles and Permissions v4.xlsx. Every sheet, role row, letter, number and date of v4 is kept word for word. The realignment adds this sheet, the Authorise contract and Area owners sheets at the end, one column on the Roles tab, two rows on the Access flow tab and one note row on each of the Separation of duty, Single sign-on and Systems by role tabs. |
| Change log |
| Version \| Date \| Change \| Decision \| Tool |
| \| 5 \| 22 November 2026 \| D-RCV-60 microservice realignment \| D-RCV-60 \| T3 Code / OpenCode / DeepSeek v4.1 Flash \| |
| \| 4 \| 15 November 2026 \| the COLLINS data load actor is removed under D-RCV-35 (U1); SY-RECOVERY added; supersedes v3 \| D-RCV-35 \| not named in the source \| |
| Change-log row (Template and Rules R8.1): 5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| What changed in v5 |
| 1. New sheet Authorise contract: the one access contract of the target architecture. P4 rwb-access provides POST /authorise, GET /me/permissions, GET /doa-limits and GET /masking-policies; every service checks the object itself with cached permission data, a 2 s timeout and a circuit breaker (Architecture v5 slides 14, 35 and 41; Template and Rules DP-08). |
| 2. New sheet Area owners: the 14 capability areas of the Permissions tab, each with the service that owns its data and its enforcement, taken from the Microservice Ownership Map v1 (Tables, Endpoints, Events, Jobs and Parameters sheets). |
| 3. Roles tab: one new column K, Enforcing services (D-RCV-60), computed from the letters the role already holds on the Permissions tab. No existing cell changes. |
| 4. Access flow tab: two rows added. Review step 3 is the six-monthly JOB-18 access review list, a Temporal Schedule in rwb-access. Break-glass step 5 is AccessPolicyChanged, published so every service refreshes its cached permissions and DoA limits. |
| 5. Separation of duty tab: one note row. The eight pairs are rows in rwb_access.role_conflict, owned by P4; the grant check and the sign-in check read the same rows. |
| 6. Single sign-on tab: one note row. rwb-access resolves each Entra ID group above to a role code at sign-in through ACE Common group-to-role (Architecture v5 slides 14, 30 and 41). |
| 7. Systems by role tab: one note row. ACE and TDR data reaches a role through the contract of P1 rwb-source-data or the recovery.v_ace_* views, never by a direct table read (DP-05). |
| 8. Key tab: six rows added, for column K, the two new sheets, the tentative-release rule, the access check and version v5. |
| What did not change |
| All 54 role rows of the Roles tab, with every role code, name, class, group, unit, description, L1 process, screen, default scope and first release. |
| The permission matrix: 54 roles against 14 capability areas, every letter of every row. Every approve right still works within the delegation of authority table. |
| The 8 separation-of-duty pairs, the 15 access-flow rows, the 49 single sign-on rows and the 37 systems-by-role rows of the bank roles. |
| The Counts tab (blank in v4, kept as it is), the 16 Key rows of v4, the Roles tab note row of 15 November 2026 and the Key version row v4. |
| No date is added, changed or removed. v4 states no release date. The release labels E1 to E8 are copied unchanged, and every one of them is tentative (D-RCV-60, U7). |
| No table, column, function, message or rule name of the source is renamed. |
| Owners (Microservice Ownership Map v1) |
| Every owner named in v5 is taken from the Microservice Ownership Map v1 Services, Tables, Endpoints, Jobs, Events and Parameters sheets, or from Architecture v5 slides 14, 35, 41, 42, 43 and 44. P4 rwb-access owns the roles, permissions, role conflicts, masking, DoA limits and the access log. |
| Where v4 says 'the Workbench', v5 names the service behind it and leaves the v4 sentence in place. |
| Contract stories (Template and Rules DP-08, R5.4 and R5.7) |
| RWB-P4-E1037-CON: the rwb-access contract, P4, wave 1, Day 1. |
| RWB-PLT-E1037-CON: the access guard library every service builds against. |
| Every service carries the contract as a C dependency and builds against its fake, so no service waits for P4 to be built. |
| Open points (placeholders of Template and Rules R9) |
| 1. Request and response schema of the four authorise operations: Not specified in the source documents (GAP-0159; ASM-0243). |
| 2. Contract name of the sign-in read, /me/permissions or /me/session: Not specified in the source documents (GAP-0160; ASM-0244). |
| 3. Cache lifetime and the rule on a failed authorise call: Not specified in the source documents (GAP-0161; ASM-0245). |
| 4. DoA limit amounts: Not specified in the source documents (GAP-0162; ASM-0246). |
| 5. Masking rules per role, area and field group: Not specified in the source documents (GAP-0163; ASM-0247). |
| 6. Partner user to role mapping between S9 and P4: Not specified in the source documents (GAP-0164; ASM-0248). |
| 7. Access log table in rwb_access: Not specified in the source documents (GAP-0165; ASM-0249). |
| 8. Credential of the six non-human actors: Not specified in the source documents (GAP-0166; ASM-0250). |
| 9. Counts tab values: Not specified in the source documents (GAP-0167; ASM-0251). |
| 10. Scope values, Own/Team/All/Placed cases against the legacy REGION: Not specified in the source documents (GAP-0168; ASM-0252). |
| 11. Approval and status of this document: Not specified in the source documents (GAP-0169; ASM-0253). |
| Counts of this version |
| Sheets: 11 (the 8 sheets of v4 in the v4 order, plus Read me, Authorise contract and Area owners). |
| Roles: 54, of which 37 bank users, 7 partner users, 4 customer parties and 6 non-human actors (unchanged). |
| Capability areas: 14 (unchanged). Separation-of-duty pairs: 8 (unchanged). Access-flow rows: 17 (15 of v4 plus 2). |

## Sheet: Roles

| Users and roles |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 54 roles: 37 bank users, 7 partner users, 4 customer parties and 6 non-human actors. One row is one role, held as data in the roles table. Version 4, 15 November 2026: the COLLINS data load actor is removed under D-RCV-35 (U1); SY-RECOVERY added. |  |  |  |  |  |  |  |  |  |  |
| Role code | Role name | Class | Group | Unit or organization | What the role does | L1 processes | Main screens | Default scope | First release with real users | Enforcing services (D-RCV-60) |
| RW-CASEOWN | Case owner | Bank user | Shared operations | Shared operations | Owns the case from day 90 to close. Accepts the hand-over, reads expected net recovery after cost per route, approves inside the limit, answers for ageing against the service level | 06 to 10 | Case list, case record, my queue | Own | E2 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-TEAMMGR | Team manager | Bank user | Shared operations | Shared operations | Runs the team: allocation overrides, reassignment, caseload and service level breaches, coaching, the spread between collectors | 06 to 10 | Team queues, transfer screen, queue measures | Team | E2 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-PHONECOL | Phone collector | Bank user | Shared operations | Shared operations | Works the pre-90 list on EFS. Reads the case record for accounts that have moved to recovery so the customer is not called twice | pre-06 | Case record read only | Own | E2 | P4 rwb-access; P3 rwb-case; P5 rwb-document; P9 rwb-reporting |
| RW-FIELDCOL | Field collector | Bank user | Shared operations | Shared operations, field | Visits the customer or the asset, captures photos, bills and signed documents into the case through the field app | 06, 09 | Field app intake, case record | Own | E7 | P4 rwb-access; P3 rwb-case; S5 rwb-asset; P5 rwb-document |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | Shared operations | FCR, restructuring | Builds and sends the restructure offer inside the band, records affordability, books the plan. Exceptions only reach a person | 07 | Treatment screen, offer builder, plan view | Team | E3 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | Shared operations | Shared operations | Takes cases flagged X2 or X3, sets contact limits, decides a hardship plan or a BOT relief program | 11 deviations | Deviation queue, case record | Team | E7 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-COMPLAIN | Complaint officer | Bank user | Shared operations | Conduct, shared operations | Takes X1 disputes and complaints, applies the contact stop, builds the evidence pack, resolves inside the service level and returns the case to the same decision | 11 deviations | Deviation queue, contact stop | Team | E7 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-FRAUD | Fraud investigator | Bank user | Control functions and committees | Fraud | Takes X4 referrals, investigates, confirms or clears, which sends the case to D9 or back to D2 | 11 deviations | Deviation queue, case record | All | E7 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-LITOFF | Litigation officer | Bank user | Shared operations | Legal and litigation | Checks the agent-assembled case pack against the defect list, instructs the law firm, files, manages to judgment | 08 | Litigation workspace, case pack, panel scorecard | Team | E2 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-ENFORCE | Enforcement owner | Bank user | Shared operations | Legal and litigation | Owns enforcement after judgment: seizure, LED auction entry, or a coded deferral with its reason. One of the three points with no owner today | 08 | Enforcement workspace, LED tracker | Team | E5 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-LEGAL | Legal counsel | Bank user | Control functions and committees | Legal | Approves notice and contract templates, rules on estate and bankruptcy claims, joins X3 and X5 deviations | 08, 11 | Template approval, deviation queue | All | E3 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-SALEOFF | Sale officer | Bank user | Shared operations | Shared operations with the product head | Runs the auction schedule, the listing and the price ladder, approves inside the floor, sends anything below it for a second signature | 09 | Asset list, listing, price ladder, bid review | Team | E3 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-NPAMGR | NPA and asset manager | Bank user | Shared operations | Asset liquidity | Holds and manages repossessed assets: custody, insurance, maintenance, the stock balance. The stock balance is one of the three unowned points today | 09 | Asset list, holding cost, stock balance | Team | E3 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-DEBTSALE | Debt sale officer | Bank user | Shared operations | Asset liquidity | Builds the lots, sets the reserve from the model, runs the buyer process, transfers the data on award | 09 | Lot builder, buyer portal admin, award screen | Team | E6 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-WRITEOFF | Write-off team member | Bank user | Shared operations | Credit administration | Runs the monthly scan on both tracks, proposes the population, prepares the committee pack | 10 | Write-off proposal, committee pack | Team | E6 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-CREDITAD | Credit Administration officer | Bank user | Shared operations | Credit administration | Posts the approved write-off, releases the provision, publishes completeness, records post charge-off recovery | 10 | Posting screen, completeness report | Team | E3 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-GUARANT | Guarantee officer | Bank user | Shared operations | Shared operations | Files and tracks TCG and insurance claims, records the subrogation position | 07 | Guarantee claim workspace | Team | E4 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-AGENCYMG | Partner and agency manager | Bank user | Shared operations | OA management team | Runs every partner type on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit. Sets placements by measured return | 06 to 10, 12 | Partner portal, scorecard, placement screen | All | E6 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-CONDUCT | Conduct and QA officer | Bank user | Center of excellence | Conduct, center of excellence | Reviews contacts blocked by the contact check, matches complaints to the preceding contact, samples decisions against the rule version applied | all | Conduct review, QA sample, contact log | All | E8 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-CAPACITY | Capacity and workforce planner | Bank user | Shared operations | Shared operations | Sets next week's roster from inflow by product, bucket and region, the answer curve and the field coverage map. A role with no structure chart today | all | Capacity planner, inflow forecast | All | E2 | P4 rwb-access; P3 rwb-case; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | Product heads | Product | Owns approval limits for the product, approves above the case owner limit, owns the floor price and the band | 07 to 10 | Approval queue, delegation view | All | E2 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-HEADLIT | Head of Litigation | Bank user | Shared operations | Legal and litigation | Approves legal spend above the limit, rules on panel conflicts and escalations | 08 | Approval queue, panel console | All | E2 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-HEADNPA | Head of NPA | Bank user | Shared operations | Asset liquidity | Approves holding, price steps below the floor and transfers to RAMC | 09 | Approval queue, asset list | All | E3 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-HEADASL | Head of Asset Liquidity | Bank user | Shared operations | Asset liquidity | Approves lots, reserve prices and buyer panel changes | 09 | Approval queue, lot builder | All | E6 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-CREDCOMM | Credit approval committee member | Bank user | Control functions and committees | Credit | Approves restructures and settlements above the delegated limit | 07 | Approval queue, committee pack | All | E4 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-WOCOMM | Write-off committee member | Bank user | Control functions and committees | Credit, Finance, Risk | Approves the write-off population inside the delegation, rules on the exception loop | 10 | Committee pack, approval queue | All | E6 | P4 rwb-access; P3 rwb-case; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting |
| RW-RISK | Risk and model risk officer | Bank user | Control functions and committees | Risk | Reviews drift and calibration, raises a decision with an owner and a date on a breach, signs rule version changes | all | Model monitor, rule version log | All | E2 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-COE | Center of excellence analyst | Bank user | Center of excellence | Center of excellence | Owns the rule tables, the parameter catalog, the measure definitions and the QA program. Loads and rolls back rule versions | all | Rule console, parameter catalog, reference data | All | E1 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting; P2 rwb-integration; PLT platform library |
| RW-DATASTEW | Data steward and data product owner | Bank user | Platform | Data and analytics | Owns a data product: definition, quality rules, freshness, access. Signs the daily reconciliation to ALS | all | Data quality console, catalog, reconciliation report | All | E1 | P4 rwb-access; P3 rwb-case; P5 rwb-document; P7 rwb-decision; P9 rwb-reporting; P2 rwb-integration; PLT platform library |
| RW-FINANCE | Finance and CFO delegate | Bank user | Control functions and committees | Finance | Reviews benefit realisation monthly, owns the provision and posting rules | 10 | Benefit dashboard, posting report | All | E6 | P4 rwb-access; P3 rwb-case; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P7 rwb-decision; P9 rwb-reporting |
| RW-AUDIT | Internal audit | Bank user | Control functions and committees | Audit | Queries the decision log, samples cases, tests that every action carries a rule version and an approver | all | Decision log query, audit export | All | E1 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting; P2 rwb-integration; PLT platform library |
| RW-COMPLY | Compliance and PDPA officer | Bank user | Control functions and committees | Compliance | Rules on data subject requests, consent, retention and masking. Approves regulatory reporting content | all | PDPA console, retention classes, consent log | All | E1 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting; P2 rwb-integration; PLT platform library |
| RW-PLATADM | Platform administrator | Bank user | Platform | TechX platform | Runs the environment: configuration service, feature flags, jobs, interfaces, incident handling, break-glass | all | Admin console, job monitor, interface monitor | All | E1 | P4 rwb-access; P3 rwb-case; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting; P2 rwb-integration; PLT platform library |
| RW-REFADM | Reference data administrator | Bank user | Center of excellence | Center of excellence | Maintains the versioned reference tables: queues, roles, templates, document checklists, action codes, product parameters | all | Reference data service, versioned tables | All | E1 | P4 rwb-access; P7 rwb-decision; P3 rwb-case; P9 rwb-reporting |
| RW-SECADM | Security administrator | Bank user | Control functions and committees | SCB IT security | Owns the role to permission matrix, joiner mover leaver, break-glass approval, the access log | all | Access admin, permission matrix, access log | All | E1 | P4 rwb-access; P7 rwb-decision; P3 rwb-case; P9 rwb-reporting; P2 rwb-integration; PLT platform library |
| RW-BIANAL | Reporting and BI analyst | Bank user | Platform | Data and analytics | Builds and runs the steering dashboard, the queue measures and the regulatory extracts | all | Power BI workspace, report builder | All | E2 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| RW-TRIBE | Tribe lead and squad members | Bank user | Platform | Collections and Recovery Tribe | Run the weekly squad review, own the backlog and the release train | all | Backlog, release board | All | E2 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision; S9 rwb-partner; P9 rwb-reporting |
| PT-AGENCY | Collection agency (OA) user | Partner user | Partner user | 73 agencies on a fixed 20 percent share | Receives placements, records contact outcomes and payments, returns the account at recall or panel exit | 06, 10 | Partner portal: placement list, outcome capture | Placed cases | E6 | P4 rwb-access; P3 rwb-case; P5 rwb-document; S9 rwb-partner |
| PT-LAWFIRM | Law firm user | Partner user | Partner user | 11 to 12 firms on the panel | Receives the instruction and the case pack, files, reports court state and hearing dates, invoices against the fee schedule | 08 | Partner portal: instruction, court state, invoice | Placed cases | E5 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; P5 rwb-document; S9 rwb-partner |
| PT-VALUER | Valuer | Partner user | Partner user | Panel valuers | Receives the valuation instruction, uploads the report and the value, which feeds the band and the floor | 07, 09 | Partner portal: instruction, report upload | Placed cases | E4 | P4 rwb-access; S5 rwb-asset; P5 rwb-document; S9 rwb-partner |
| PT-AUCTION | Auction vendor | Partner user | Partner user | 4 vendors allocated by distance | Runs the auction rounds on the ladder, reports results per round, settles proceeds | 09 | Partner portal: schedule, round result, settlement | Placed cases | E4 | P4 rwb-access; S5 rwb-asset; P5 rwb-document; S9 rwb-partner |
| PT-BUYER | Debt buyer and AMC | Partner user | Partner user | 35 buyers | Qualifies, views the lot data room, bids, receives the data transfer on award, confirms remittance | 09 | Partner portal: data room, bid, award, transfer | Placed cases | E5 | P4 rwb-access; S6 rwb-debtsale; P5 rwb-document; S9 rwb-partner |
| PT-RAMC | RAMC user | Partner user | Partner user | SCB asset management company | Takes the transfer of assets and accounts that move to RAMC and confirms the position | 09 | Partner portal: transfer, confirmation | Placed cases | E4 | P4 rwb-access; S5 rwb-asset; S6 rwb-debtsale; P5 rwb-document; S9 rwb-partner |
| PT-LED | Legal Execution Department and court officer | Partner user | Partner user | Government | Runs the enforcement auction on the 100 / 90 / 80 / 70 percent ladder and issues the official value. Reached by interface and filing, not by a Workbench login | 08, 09 | No login: filing and result interfaces | Placed cases | No login | No Workbench capability area held: reached by filing and result interfaces, not by a Workbench login (Roles tab, First release) |
| CU-BORROW | Customer (borrower) | Customer party | Customer party | Retail and SSME customers | Is told who owns the case, supplies documents, accepts or declines an offer, signs, pays, hands over an asset | 06 to 10 | Notices, HOME.SCB, e-signature link | Own case | E4 self-service through bank channels | No Workbench capability area held: reached through the bank channels (Roles tab, First release) |
| CU-GUARANT | Guarantor and co-borrower | Customer party | Customer party | Connected parties | Receives the demand, answers it, may pay, settle or be pursued | 07, 08 | Notices, e-signature link | Own case | Through bank channels | No Workbench capability area held: reached through the bank channels (Roles tab, First release) |
| CU-HEIR | Heir and estate representative | Customer party | Customer party | Connected parties | Is notified on a death, supplies the certificate, deals with the estate claim | 11 deviations | Notices | Own case | Through bank channels | No Workbench capability area held: reached through the bank channels (Roles tab, First release) |
| CU-BIDDER | Retail asset bidder | Customer party | Customer party | Public | Views the listing and bids in an auction round | 09 | Public listing, auction portal | Own case | Through bank channels | No Workbench capability area held: reached through the bank channels (Roles tab, First release) |
| SY-CASEWF | Case workflow module | Non-human actor | Non-human actor | Recovery module | Holds the case state, runs every stage clock, timer, escalation and prescription date, and moves the case on each rule result | all | None | All | E1 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision |
| SY-RULES | Rules component | Non-human actor | Non-human actor | Recovery module | Evaluates the versioned rule tables for allocation, assignment, transfer, route and approval routing | all | None | All | E1 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision |
| SY-RECOVERY | Recovery service identity | Non-human actor | Non-human actor | Recovery module | Reads ACE source data for the recovery module through the SELECT-only recovery.v_ace_* views (read-only ACE view access). No direct read of a public ACE table and no write on any ACE table or view (D-RCV-35, U4) | all | None | All | E1 | P4 rwb-access; P3 rwb-case; S4 rwb-litigation; S5 rwb-asset; S7 rwb-writeoff |
| SY-OCR | OCR and extraction pipeline | Non-human actor | Non-human actor | Autonomous Ops | Classifies an incoming document, extracts its fields into the index and attaches it to the case | all | Review queue for low confidence | All | E1 | P4 rwb-access; P3 rwb-case; P5 rwb-document; P7 rwb-decision |
| SY-DECLOG | Decision log writer | Non-human actor | Non-human actor | Recovery module | Writes an append-only, hash-chained entry for every decision with the rule ID and version, the inputs and the approver | all | None | All | E1 | P4 rwb-access; P7 rwb-decision |
| SY-AGENT | Agent platform | Non-human actor | Non-human actor | Enterprise AI | Runs the recovery agents through the tool gateway at autonomy levels L0 to L4 | all | Agent monitor | All | E1 | P4 rwb-access; P3 rwb-case; S2 rwb-treatment; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; P5 rwb-document; P7 rwb-decision |

## Sheet: Permissions

| Permission matrix |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Each role against the 14 capability areas. C create, R read, U update, D delete, A approve, a dash for none. Every approve right works within the delegation of authority table. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Role code | Role name | Class | Case record | Queue and allocation | Treatment and offer | Litigation | Asset and disposal | Debt sale | Write-off and posting | Documents | Rules and parameters | Reference data | Decision log | Partner portal | Reporting | Platform administration |
| RW-CASEOWN | Case owner | Bank user | CRU | R | CRU | R | R | - | - | CRU | R | R | R | R | R | - |
| RW-TEAMMGR | Team manager | Bank user | R | CRUA | R | R | R | - | - | R | R | R | R | R | R | - |
| RW-PHONECOL | Phone collector | Bank user | R | R | - | - | - | - | - | R | - | R | - | - | R | - |
| RW-FIELDCOL | Field collector | Bank user | R | R | - | - | R | - | - | CR | - | R | - | - | - | - |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | RU | R | CRUA | - | - | - | - | CRU | R | R | R | - | R | - |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | RU | R | CRU | - | - | - | - | CRU | R | R | R | - | R | - |
| RW-COMPLAIN | Complaint officer | Bank user | RU | R | R | R | R | - | - | CRU | R | R | R | - | R | - |
| RW-FRAUD | Fraud investigator | Bank user | RU | R | R | R | - | - | R | CRU | R | R | R | - | R | - |
| RW-LITOFF | Litigation officer | Bank user | RU | R | R | CRUA | R | - | - | CRU | R | R | R | CRU | R | - |
| RW-ENFORCE | Enforcement owner | Bank user | RU | R | - | CRU | CRU | - | - | CRU | R | R | R | CRU | R | - |
| RW-LEGAL | Legal counsel | Bank user | R | - | R | RA | R | - | - | CRUA | R | RU | R | R | R | - |
| RW-SALEOFF | Sale officer | Bank user | RU | R | - | R | CRUA | R | - | CRU | R | R | R | CRU | R | - |
| RW-NPAMGR | NPA and asset manager | Bank user | R | - | - | R | CRU | R | - | CRU | R | R | R | CRU | R | - |
| RW-DEBTSALE | Debt sale officer | Bank user | RU | R | - | R | R | CRUA | R | CRU | R | R | R | CRU | R | - |
| RW-WRITEOFF | Write-off team member | Bank user | R | - | - | R | R | R | CRU | CRU | R | R | R | - | R | - |
| RW-CREDITAD | Credit Administration officer | Bank user | R | - | - | R | R | R | CRUA | CRU | R | R | R | - | R | - |
| RW-GUARANT | Guarantee officer | Bank user | RU | R | CRU | R | - | - | - | CRU | R | R | R | CRU | R | - |
| RW-AGENCYMG | Partner and agency manager | Bank user | R | R | - | R | R | R | - | R | R | RU | R | CRUDA | R | - |
| RW-CONDUCT | Conduct and QA officer | Bank user | R | R | R | R | R | R | R | R | R | R | R | R | R | - |
| RW-CAPACITY | Capacity and workforce planner | Bank user | R | RU | - | - | - | - | - | - | R | R | - | R | R | - |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | R | R | RA | RA | RA | RA | RA | R | R | R | R | R | R | - |
| RW-HEADLIT | Head of Litigation | Bank user | R | R | - | RA | R | - | - | R | R | R | R | RA | R | - |
| RW-HEADNPA | Head of NPA | Bank user | R | - | - | R | RA | R | - | R | R | R | R | RA | R | - |
| RW-HEADASL | Head of Asset Liquidity | Bank user | R | - | - | R | RA | RA | - | R | R | R | R | RA | R | - |
| RW-CREDCOMM | Credit approval committee member | Bank user | R | - | RA | - | - | - | - | R | R | R | R | - | R | - |
| RW-WOCOMM | Write-off committee member | Bank user | R | - | - | - | - | - | RA | R | R | R | R | - | R | - |
| RW-RISK | Risk and model risk officer | Bank user | R | R | R | R | R | R | R | R | RA | R | R | R | R | - |
| RW-COE | Center of excellence analyst | Bank user | R | R | R | R | R | R | R | R | CRUD | CRUD | R | R | R | R |
| RW-DATASTEW | Data steward and data product owner | Bank user | R | - | - | - | - | - | - | R | R | RU | R | - | CRU | R |
| RW-FINANCE | Finance and CFO delegate | Bank user | R | - | - | - | R | R | RA | - | R | R | R | - | R | - |
| RW-AUDIT | Internal audit | Bank user | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| RW-COMPLY | Compliance and PDPA officer | Bank user | R | - | - | R | - | - | - | RU | R | RU | R | R | R | R |
| RW-PLATADM | Platform administrator | Bank user | R | R | - | - | - | - | - | R | R | R | R | R | R | CRUD |
| RW-REFADM | Reference data administrator | Bank user | - | - | - | - | - | - | - | - | R | CRUD | R | - | R | - |
| RW-SECADM | Security administrator | Bank user | - | - | - | - | - | - | - | - | R | R | R | - | R | CRUDA |
| RW-BIANAL | Reporting and BI analyst | Bank user | R | R | R | R | R | R | R | - | R | R | R | R | CRUD | - |
| RW-TRIBE | Tribe lead and squad members | Bank user | R | R | R | R | R | R | R | R | R | R | R | R | R | - |
| PT-AGENCY | Collection agency (OA) user | Partner user | R | - | - | - | - | - | - | CR | - | - | - | RU | - | - |
| PT-LAWFIRM | Law firm user | Partner user | R | - | - | RU | - | - | - | CRU | - | - | - | RU | - | - |
| PT-VALUER | Valuer | Partner user | - | - | - | - | R | - | - | CR | - | - | - | RU | - | - |
| PT-AUCTION | Auction vendor | Partner user | - | - | - | - | RU | - | - | CR | - | - | - | RU | - | - |
| PT-BUYER | Debt buyer and AMC | Partner user | - | - | - | - | - | RU | - | R | - | - | - | RU | - | - |
| PT-RAMC | RAMC user | Partner user | - | - | - | - | RU | R | - | R | - | - | - | RU | - | - |
| PT-LED | Legal Execution Department and court officer | Partner user | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-BORROW | Customer (borrower) | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-GUARANT | Guarantor and co-borrower | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-HEIR | Heir and estate representative | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-BIDDER | Retail asset bidder | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| SY-CASEWF | Case workflow module | Non-human actor | CRU | CRU | R | R | R | R | R | R | R | R | C | - | - | - |
| SY-RULES | Rules component | Non-human actor | R | R | R | R | R | R | R | R | R | R | C | - | - | - |
| SY-RECOVERY | Recovery service identity | Non-human actor | R | - | - | R | R | - | R | - | - | R | - | - | - | - |
| SY-OCR | OCR and extraction pipeline | Non-human actor | R | - | - | - | - | - | - | CRU | - | R | C | - | - | - |
| SY-DECLOG | Decision log writer | Non-human actor | - | - | - | - | - | - | - | - | - | - | C | - | - | - |
| SY-AGENT | Agent platform | Non-human actor | R | R | R | R | R | R | R | R | R | R | C | - | - | - |

## Sheet: Separation of duty

| Separation of duty |  |  |
|---|---|---|
| Role pairs one person may not hold. Checked by the role owner at each grant and by the Workbench at each sign-in. A person may not approve a decision they proposed or prepared. |  |  |
| Role | May not also hold | Reason |
| Security administrator | Any business role | The person who maps groups to roles could grant themselves business access |
| Platform administrator | Any business role | Technical access combined with business access passes around scope and masking |
| Access administrator position | Role owner for the same roles | One person would approve and carry out the same grant |
| Reference data administrator | Risk and model risk officer | Loading a delegation or rule version and approving it are separate steps |
| Center of excellence analyst | Risk and model risk officer | Writing a rule and approving it are separate steps |
| Restructuring officer | Credit approval committee member | Proposing a restructure and approving it are separate steps |
| Write-off team member | Write-off committee member | Proposing a write-off and approving it are separate steps |
| Internal audit | Any other role | Audit reads and changes nothing |
| Note | Held as data | The pairs above are rows of rwb_access.role_conflict, owned by P4 rwb-access (Ownership Map v1 Tables sheet). The grant check and the sign-in check read the same rows, and a change publishes AccessPolicyChanged on rwb.access.events.v1 (D-RCV-60). |

## Sheet: Access flow

| Request, grant, review and removal |  |  |  |  |
|---|---|---|---|---|
| Who does what at each step. The review interval, the leaver response time and the break-glass window are DL38. |  |  |  |  |
| Event | Step | Who | Action | Where |
| Joiner | 1 | Line manager | Raises a request naming the person, the role and the reason | Bank IAM |
| Joiner | 2 | Role owner | Approves or rejects, after checking the separation of duty table | Bank IAM |
| Joiner | 3 | Access administrator | Adds the person to the Entra ID group for the role in each environment requested | Bank IAM to Entra ID |
| Joiner | 4 | The person | Signs in with multi-factor authentication | Workbench |
| Joiner | 5 | Workbench | Resolves the roles, scope and masking and writes the session to the access log | Workbench |
| Mover | 1 | Line manager | One request removes the previous roles and adds the new ones in the same change | Bank IAM |
| Mover | 2 | Role owners | The owners of the old and the new roles approve. A mover never holds both sets | Bank IAM |
| Leaver | 1 | Line manager or HR leaver record | Starts removal from every Workbench group | Bank IAM |
| Leaver | 2 | Workbench | Ends the open session at the next request and refuses a new one | Workbench |
| Review | 1 | Role owner | Recertifies every holder of the role at each review. A holder not recertified is removed | Bank IAM |
| Review | 2 | Application owner | Signs the review result | Bank IAM |
| Break-glass | 1 | Platform administrator | Requests access beyond the role, naming the open incident, the area, the scope and the reason | Bank IAM |
| Break-glass | 2 | Security administrator | Approves. A request with no open incident is refused | Bank IAM |
| Break-glass | 3 | Workbench | Marks every action under break-glass in the access log. The grant ends when its window ends | Workbench |
| Break-glass | 4 | Security administrator | Reviews the use inside the review window. An unreviewed use goes to the head of SCB IT security and to Compliance | Bank IAM |
| Review | 3 | rwb-access (P4) | Temporal Schedule JOB-18 (six-monthly) publishes the list of every holder of every role; the role owner recertifies from it and a holder not recertified is removed | Workbench (rwb-access) |
| Break-glass | 5 | rwb-access (P4) | Publishes AccessPolicyChanged on rwb.access.events.v1 so every service refreshes its cached permissions and DoA limits; the grant ends when its window ends | Workbench (rwb-access) |

## Sheet: Single sign-on

| Single sign-on mapping |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| One Entra ID group per role per environment, granted through the bank IAM. Group names follow the pattern shown until SCB IT security issues the bank standard names (DL40). |  |  |  |  |  |  |
| Role code | Role name | Identity | DEV | SIT | UAT | PROD |
| RW-CASEOWN | Case owner | Entra ID group | RWB-DEV-RW-CASEOWN | RWB-SIT-RW-CASEOWN | RWB-UAT-RW-CASEOWN | RWB-PROD-RW-CASEOWN |
| RW-TEAMMGR | Team manager | Entra ID group | RWB-DEV-RW-TEAMMGR | RWB-SIT-RW-TEAMMGR | RWB-UAT-RW-TEAMMGR | RWB-PROD-RW-TEAMMGR |
| RW-PHONECOL | Phone collector | Entra ID group | RWB-DEV-RW-PHONECOL | RWB-SIT-RW-PHONECOL | RWB-UAT-RW-PHONECOL | RWB-PROD-RW-PHONECOL |
| RW-FIELDCOL | Field collector | Entra ID group | RWB-DEV-RW-FIELDCOL | RWB-SIT-RW-FIELDCOL | RWB-UAT-RW-FIELDCOL | RWB-PROD-RW-FIELDCOL |
| RW-RESTRUCT | Restructuring officer (FCR) | Entra ID group | RWB-DEV-RW-RESTRUCT | RWB-SIT-RW-RESTRUCT | RWB-UAT-RW-RESTRUCT | RWB-PROD-RW-RESTRUCT |
| RW-SPECIAL | Hardship and vulnerability specialist | Entra ID group | RWB-DEV-RW-SPECIAL | RWB-SIT-RW-SPECIAL | RWB-UAT-RW-SPECIAL | RWB-PROD-RW-SPECIAL |
| RW-COMPLAIN | Complaint officer | Entra ID group | RWB-DEV-RW-COMPLAIN | RWB-SIT-RW-COMPLAIN | RWB-UAT-RW-COMPLAIN | RWB-PROD-RW-COMPLAIN |
| RW-FRAUD | Fraud investigator | Entra ID group | RWB-DEV-RW-FRAUD | RWB-SIT-RW-FRAUD | RWB-UAT-RW-FRAUD | RWB-PROD-RW-FRAUD |
| RW-LITOFF | Litigation officer | Entra ID group | RWB-DEV-RW-LITOFF | RWB-SIT-RW-LITOFF | RWB-UAT-RW-LITOFF | RWB-PROD-RW-LITOFF |
| RW-ENFORCE | Enforcement owner | Entra ID group | RWB-DEV-RW-ENFORCE | RWB-SIT-RW-ENFORCE | RWB-UAT-RW-ENFORCE | RWB-PROD-RW-ENFORCE |
| RW-LEGAL | Legal counsel | Entra ID group | RWB-DEV-RW-LEGAL | RWB-SIT-RW-LEGAL | RWB-UAT-RW-LEGAL | RWB-PROD-RW-LEGAL |
| RW-SALEOFF | Sale officer | Entra ID group | RWB-DEV-RW-SALEOFF | RWB-SIT-RW-SALEOFF | RWB-UAT-RW-SALEOFF | RWB-PROD-RW-SALEOFF |
| RW-NPAMGR | NPA and asset manager | Entra ID group | RWB-DEV-RW-NPAMGR | RWB-SIT-RW-NPAMGR | RWB-UAT-RW-NPAMGR | RWB-PROD-RW-NPAMGR |
| RW-DEBTSALE | Debt sale officer | Entra ID group | RWB-DEV-RW-DEBTSALE | RWB-SIT-RW-DEBTSALE | RWB-UAT-RW-DEBTSALE | RWB-PROD-RW-DEBTSALE |
| RW-WRITEOFF | Write-off team member | Entra ID group | RWB-DEV-RW-WRITEOFF | RWB-SIT-RW-WRITEOFF | RWB-UAT-RW-WRITEOFF | RWB-PROD-RW-WRITEOFF |
| RW-CREDITAD | Credit Administration officer | Entra ID group | RWB-DEV-RW-CREDITAD | RWB-SIT-RW-CREDITAD | RWB-UAT-RW-CREDITAD | RWB-PROD-RW-CREDITAD |
| RW-GUARANT | Guarantee officer | Entra ID group | RWB-DEV-RW-GUARANT | RWB-SIT-RW-GUARANT | RWB-UAT-RW-GUARANT | RWB-PROD-RW-GUARANT |
| RW-AGENCYMG | Partner and agency manager | Entra ID group | RWB-DEV-RW-AGENCYMG | RWB-SIT-RW-AGENCYMG | RWB-UAT-RW-AGENCYMG | RWB-PROD-RW-AGENCYMG |
| RW-CONDUCT | Conduct and QA officer | Entra ID group | RWB-DEV-RW-CONDUCT | RWB-SIT-RW-CONDUCT | RWB-UAT-RW-CONDUCT | RWB-PROD-RW-CONDUCT |
| RW-CAPACITY | Capacity and workforce planner | Entra ID group | RWB-DEV-RW-CAPACITY | RWB-SIT-RW-CAPACITY | RWB-UAT-RW-CAPACITY | RWB-PROD-RW-CAPACITY |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Entra ID group | RWB-DEV-RW-PRODHEAD | RWB-SIT-RW-PRODHEAD | RWB-UAT-RW-PRODHEAD | RWB-PROD-RW-PRODHEAD |
| RW-HEADLIT | Head of Litigation | Entra ID group | RWB-DEV-RW-HEADLIT | RWB-SIT-RW-HEADLIT | RWB-UAT-RW-HEADLIT | RWB-PROD-RW-HEADLIT |
| RW-HEADNPA | Head of NPA | Entra ID group | RWB-DEV-RW-HEADNPA | RWB-SIT-RW-HEADNPA | RWB-UAT-RW-HEADNPA | RWB-PROD-RW-HEADNPA |
| RW-HEADASL | Head of Asset Liquidity | Entra ID group | RWB-DEV-RW-HEADASL | RWB-SIT-RW-HEADASL | RWB-UAT-RW-HEADASL | RWB-PROD-RW-HEADASL |
| RW-CREDCOMM | Credit approval committee member | Entra ID group | RWB-DEV-RW-CREDCOMM | RWB-SIT-RW-CREDCOMM | RWB-UAT-RW-CREDCOMM | RWB-PROD-RW-CREDCOMM |
| RW-WOCOMM | Write-off committee member | Entra ID group | RWB-DEV-RW-WOCOMM | RWB-SIT-RW-WOCOMM | RWB-UAT-RW-WOCOMM | RWB-PROD-RW-WOCOMM |
| RW-RISK | Risk and model risk officer | Entra ID group | RWB-DEV-RW-RISK | RWB-SIT-RW-RISK | RWB-UAT-RW-RISK | RWB-PROD-RW-RISK |
| RW-COE | Center of excellence analyst | Entra ID group | RWB-DEV-RW-COE | RWB-SIT-RW-COE | RWB-UAT-RW-COE | RWB-PROD-RW-COE |
| RW-DATASTEW | Data steward and data product owner | Entra ID group | RWB-DEV-RW-DATASTEW | RWB-SIT-RW-DATASTEW | RWB-UAT-RW-DATASTEW | RWB-PROD-RW-DATASTEW |
| RW-FINANCE | Finance and CFO delegate | Entra ID group | RWB-DEV-RW-FINANCE | RWB-SIT-RW-FINANCE | RWB-UAT-RW-FINANCE | RWB-PROD-RW-FINANCE |
| RW-AUDIT | Internal audit | Entra ID group | RWB-DEV-RW-AUDIT | RWB-SIT-RW-AUDIT | RWB-UAT-RW-AUDIT | RWB-PROD-RW-AUDIT |
| RW-COMPLY | Compliance and PDPA officer | Entra ID group | RWB-DEV-RW-COMPLY | RWB-SIT-RW-COMPLY | RWB-UAT-RW-COMPLY | RWB-PROD-RW-COMPLY |
| RW-PLATADM | Platform administrator | Entra ID group | RWB-DEV-RW-PLATADM | RWB-SIT-RW-PLATADM | RWB-UAT-RW-PLATADM | RWB-PROD-RW-PLATADM |
| RW-REFADM | Reference data administrator | Entra ID group | RWB-DEV-RW-REFADM | RWB-SIT-RW-REFADM | RWB-UAT-RW-REFADM | RWB-PROD-RW-REFADM |
| RW-SECADM | Security administrator | Entra ID group | RWB-DEV-RW-SECADM | RWB-SIT-RW-SECADM | RWB-UAT-RW-SECADM | RWB-PROD-RW-SECADM |
| RW-BIANAL | Reporting and BI analyst | Entra ID group | RWB-DEV-RW-BIANAL | RWB-SIT-RW-BIANAL | RWB-UAT-RW-BIANAL | RWB-PROD-RW-BIANAL |
| RW-TRIBE | Tribe lead and squad members | Entra ID group | RWB-DEV-RW-TRIBE | RWB-SIT-RW-TRIBE | RWB-UAT-RW-TRIBE | RWB-PROD-RW-TRIBE |
| PT-AGENCY | Collection agency (OA) user | Entra ID group | RWB-DEV-PT-AGENCY | RWB-SIT-PT-AGENCY | RWB-UAT-PT-AGENCY | RWB-PROD-PT-AGENCY |
| PT-LAWFIRM | Law firm user | Entra ID group | RWB-DEV-PT-LAWFIRM | RWB-SIT-PT-LAWFIRM | RWB-UAT-PT-LAWFIRM | RWB-PROD-PT-LAWFIRM |
| PT-VALUER | Valuer | Entra ID group | RWB-DEV-PT-VALUER | RWB-SIT-PT-VALUER | RWB-UAT-PT-VALUER | RWB-PROD-PT-VALUER |
| PT-AUCTION | Auction vendor | Entra ID group | RWB-DEV-PT-AUCTION | RWB-SIT-PT-AUCTION | RWB-UAT-PT-AUCTION | RWB-PROD-PT-AUCTION |
| PT-BUYER | Debt buyer and AMC | Entra ID group | RWB-DEV-PT-BUYER | RWB-SIT-PT-BUYER | RWB-UAT-PT-BUYER | RWB-PROD-PT-BUYER |
| PT-RAMC | RAMC user | Entra ID group | RWB-DEV-PT-RAMC | RWB-SIT-PT-RAMC | RWB-UAT-PT-RAMC | RWB-PROD-PT-RAMC |
| SY-CASEWF | Case workflow module | Managed identity | RWB-DEV-SY-CASEWF | RWB-SIT-SY-CASEWF | RWB-UAT-SY-CASEWF | RWB-PROD-SY-CASEWF |
| SY-RULES | Rules component | Managed identity | RWB-DEV-SY-RULES | RWB-SIT-SY-RULES | RWB-UAT-SY-RULES | RWB-PROD-SY-RULES |
| SY-RECOVERY | Recovery service identity | Managed identity | RWB-DEV-SY-RECOVERY | RWB-SIT-SY-RECOVERY | RWB-UAT-SY-RECOVERY | RWB-PROD-SY-RECOVERY |
| SY-OCR | OCR and extraction pipeline | Managed identity | RWB-DEV-SY-OCR | RWB-SIT-SY-OCR | RWB-UAT-SY-OCR | RWB-PROD-SY-OCR |
| SY-DECLOG | Decision log writer | Managed identity | RWB-DEV-SY-DECLOG | RWB-SIT-SY-DECLOG | RWB-UAT-SY-DECLOG | RWB-PROD-SY-DECLOG |
| SY-AGENT | Agent platform | Managed identity | RWB-DEV-SY-AGENT | RWB-SIT-SY-AGENT | RWB-UAT-SY-AGENT | RWB-PROD-SY-AGENT |
| Note - group to role: rwb-access (P4) resolves each Entra ID group above to a role code at sign-in through ACE Common group-to-role (Architecture v5 slides 14, 30 and 41). The group names above are kept exactly as they are (D-RCV-60). |  |  |  |  |  |  |

## Sheet: Systems by role

| Systems each bank role uses |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R read, W write, R/W both, blank none. Every bank role also uses the Workbench and signs in through Entra ID. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Role code | Role name | ALS core and GL | EFS | COLLINS | ACE and TDR | NLEADS | CCMS | SVAF | AMIS and RPS | LIT | Document hub | NCB | Aric | WIN | Partner portal | Power BI | Entra ID |
| RW-CASEOWN | Case owner | R | R/W | R |  |  |  |  |  |  | R/W |  |  | W |  | R | R |
| RW-TEAMMGR | Team manager |  | R |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-PHONECOL | Phone collector | R | R/W |  |  |  |  |  |  |  |  | R |  |  |  |  | R |
| RW-FIELDCOL | Field collector |  | R |  |  |  |  |  |  |  | W |  |  |  |  |  | R |
| RW-RESTRUCT | Restructuring officer (FCR) | W | R | R/W | R/W | W |  |  |  |  | R/W |  |  |  |  |  | R |
| RW-SPECIAL | Hardship and vulnerability specialist |  | R/W |  |  |  |  |  |  |  | R |  |  |  |  |  | R |
| RW-COMPLAIN | Complaint officer |  | R/W |  |  |  |  |  |  |  | R/W |  |  |  |  |  | R |
| RW-FRAUD | Fraud investigator |  | R |  |  |  |  |  |  |  |  |  | R/W |  |  |  | R |
| RW-LITOFF | Litigation officer |  |  |  |  |  |  |  |  | R/W | R/W |  |  |  | R/W |  | R |
| RW-ENFORCE | Enforcement owner |  |  |  |  |  |  |  | R | R/W |  |  |  |  | R/W |  | R |
| RW-LEGAL | Legal counsel |  |  |  |  |  |  |  |  | R | R/W |  |  | R |  |  | R |
| RW-SALEOFF | Sale officer | R |  |  |  |  |  | R | R/W |  |  |  |  |  | R/W |  | R |
| RW-NPAMGR | NPA and asset manager | R |  |  |  |  |  | R | R/W |  |  |  |  |  |  |  | R |
| RW-DEBTSALE | Debt sale officer | R/W |  |  |  |  |  |  |  |  |  |  |  |  | R/W | R | R |
| RW-WRITEOFF | Write-off team member | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-CREDITAD | Credit Administration officer | R/W |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-GUARANT | Guarantee officer | R |  |  |  |  |  |  |  |  | R/W |  |  |  | R/W |  | R |
| RW-AGENCYMG | Partner and agency manager |  |  |  |  |  |  |  |  |  |  |  |  |  | R/W | R | R |
| RW-CONDUCT | Conduct and QA officer |  | R |  |  |  |  |  |  |  | R |  |  |  |  | R | R |
| RW-CAPACITY | Capacity and workforce planner |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-HEADLIT | Head of Litigation |  |  |  |  |  |  |  |  | R |  |  |  |  |  | R | R |
| RW-HEADNPA | Head of NPA |  |  |  |  |  |  |  | R |  |  |  |  |  |  | R | R |
| RW-HEADASL | Head of Asset Liquidity |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R | R |
| RW-CREDCOMM | Credit approval committee member |  |  | R | R |  |  |  |  |  |  |  |  |  |  |  | R |
| RW-WOCOMM | Write-off committee member | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-RISK | Risk and model risk officer |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-COE | Center of excellence analyst |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-DATASTEW | Data steward and data product owner | R | R |  |  |  | R | R |  |  |  |  |  |  |  | R | R |
| RW-FINANCE | Finance and CFO delegate | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-AUDIT | Internal audit |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-COMPLY | Compliance and PDPA officer |  |  |  |  |  |  |  |  |  | R |  |  |  |  | R | R |
| RW-PLATADM | Platform administrator | R | R |  |  |  |  |  |  |  | R |  |  |  | R |  | R/W |
| RW-REFADM | Reference data administrator |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |
| RW-SECADM | Security administrator |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R/W |
| RW-BIANAL | Reporting and BI analyst |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R/W | R |
| RW-TRIBE | Tribe lead and squad members |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| Note - ACE and TDR: in the target architecture a role reaches ACE and TDR data through the contract of P1 rwb-source-data or the recovery.v_ace_* views it owns, never by a direct read of an ACE table (Architecture v5 slide 41; Template and Rules DP-05; D-RCV-60). The R and R/W marks above are kept unchanged. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## Sheet: Counts

| Roles by class and first release |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| Calculated from the Roles tab. |  |  |  |  |  |  |  |  |  |
| Class | Roles | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 |
| Bank user |  |  |  |  |  |  |  |  |  |
| Partner user |  |  |  |  |  |  |  |  |  |
| Customer party |  |  |  |  |  |  |  |  |  |
| Non-human actor |  |  |  |  |  |  |  |  |  |
| Total |  |  |  |  |  |  |  |  |  |

## Sheet: Key

| Key |  |  |
|---|---|---|
| What each letter, scope and value means. |  |  |
| Item | Term | Meaning |
| Letter | C | Create |
| Letter | R | Read |
| Letter | U | Update |
| Letter | D | Delete |
| Letter | A | Approve, within the limit set for the role in the delegation of authority table |
| Letter | - | No access to the area |
| Scope | Own | Cases the person owns or has a task on |
| Scope | Team | Cases in the person's team queues |
| Scope | All | Every case |
| Scope | Placed cases | Cases placed with the partner firm |
| Release | E1 to E8 | The release that gives the role a screen and real users. Before it, the role has named test users in SIT and UAT |
| Release | No login | Reached by filing and result interfaces, not by a Workbench login |
| Standard | NIST RBAC | Users, roles, permissions and sessions as in ANSI/INCITS 359 |
| Note | SY-RECOVERY | Recovery service identity: read-only ACE view access through recovery.v_ace_* (SELECT only), no write on ACE; matches Role to System Access Matrix v3 and Admin and Access Model v5 (8.3). The ACE view owner that owns the views is a database identity, not a role |
| Note | Retired actor | SY-DATALOAD (data load from COLLINS) is removed under D-RCV-35 (U1): ACE ingests every source and the Workbench loads none |
| Version | v4 | 15 November 2026. Supersedes v3 |
| Column | Enforcing services (D-RCV-60) | The services that enforce a role's rights: P4 rwb-access for the role, scope, DoA and masking data, plus the service that owns each capability area the role holds a letter in. Derived from the role's own row of the Permissions tab and from the Area owners tab; no value of the role row changes. |
| Sheet | Authorise contract | The contract of P4 rwb-access: the operations every service calls, the events, the schedule, the tables, the fake and the check sequence (D-RCV-60; Template and Rules DP-08). |
| Sheet | Area owners | The owner of each of the 14 capability areas of the Permissions tab, taken from the Microservice Ownership Map v1. |
| Release | Tentative | Every release E1 to E8 and every date in this document is tentative (D-RCV-60, U7). v4 states no release date and none is added or changed. |
| Note | Access check | Role, scope, DoA and masking are held by P4 rwb-access. Each service checks the object itself with cached permission data, a 2 s timeout and a circuit breaker per downstream (Architecture v5 slides 14, 35 and 41). |
| Version | v5 | 22 November 2026. Supersedes v4 |

## Sheet: Authorise contract

| Authorise contract of P4 rwb-access (D-RCV-60) |  |  |  |  |  |
|---|---|---|---|---|---|
| The one access contract of the target architecture: every service asks rwb-access, then checks the object itself. Owner P4 rwb-access (Microservice Ownership Map v1 Services, Endpoints and Tables sheets; Architecture v5 slides 14, 35 and 41). REST base /api/recovery/access/v1; schema rwb_access; topic rwb.access.events.v1; task queue rwb-access; wave 1. Patterns DP-08 and DP-11 of the Template and Rules; contract stories RWB-P4-E1037-CON and RWB-PLT-E1037-CON. |  |  |  |  |  |
| A1. REST operations provided by rwb-access |  |  |  |  |  |
| Operation | Purpose | Caller | Inputs named in a source | Response | Note |
| POST /authorise | Decide one action of one subject on one object, with the scope and the DoA limit applied | every service, through the access guard library (RWB-PLT-E1037-CON) | role, scope and DoA (Architecture v5 slide 14); the object is the record the calling service holds; the request body is Not specified in the source documents (GAP-0159; ASM-0243) | the decision with the effective scope and the DoA limit; the body is Not specified in the source documents (GAP-0159; ASM-0243) | cached reference read; 2 s timeout; circuit breaker per downstream (Architecture v5 slide 35); a POST is not retried |
| GET /me/permissions | Resolve the signed-in user's roles, each with its scope, masking and DoA limit, at sign-in | gateway-bff; every service | the subject of the JWT; the exact request body is Not specified in the source documents (GAP-0159; ASM-0243) | roles with scope, masking policy, DoA limit and policy version; the body is Not specified in the source documents (GAP-0159; ASM-0243) | Architecture v5 slides 14 and 41 name /me/permissions; the API catalogue names GET /me/session for the same read, and the resolution of the two names is Not specified in the source documents (GAP-0160; ASM-0244) |
| GET /doa-limits | Read the DoA limit of a role for a product and an action | P7 rwb-decision (ApprovalWorkflow DoA lookup); the services with an approval step | role, product group, action and business date are implied by the delegation_limit rows; the parameters are Not specified in the source documents (GAP-0159; ASM-0243) | the limit in force with its version and effective dates; the amounts are Not specified in the source documents (GAP-0162; ASM-0246) | delegation_limit is owned by P4 (Ownership Map v1); P7 reads it through this operation (Architecture v5 slide 14, P7 OUT 'REST Access: DoA limits') |
| GET /masking-policies | Read the masking rule of a role for an area and a field group | every service, before it renders personal data | role, area and field group; the parameters are Not specified in the source documents (GAP-0159; ASM-0243) | mask type and field list for the role; the rules themselves are Not specified in the source documents (GAP-0163; ASM-0247) | masking_rule is owned by P4 (Ownership Map v1); a field with no rule is masked (Compliance sets the values, DL26) |
| GET /admin/roles | List the role rows and their permission rows | RW-SECADM (role owner); RW-REFADM and RW-AUDIT (read) | filter and page | role rows | API Specification v4, x-module P4 (Ownership Map v1 Endpoints) |
| GET /admin/access-log | Query the access log | RW-SECADM; RW-AUDIT; RW-COMPLY | subject, date range, area and outcome | access log rows, with no personal data value | the log is named by Architecture v5 slides 14 and 41; the table name, columns and retention are Not specified in the source documents (GAP-0165; ASM-0249) |
| POST /admin/break-glass-grants | Open a break-glass grant naming the incident, area, scope and reason | RW-PLATADM requests it; RW-SECADM approves it | incident, area, scope, reason and window | grant ID and expiry | Access flow tab, Break-glass steps 1 to 4; the grant ends when its window ends |
| GET /me/session | Read the current session (the API Specification v4 name of the sign-in read) | gateway-bff | none | session, roles and expiry | kept for the v4 catalogue; whether the two names are one operation is Not specified in the source documents (GAP-0160; ASM-0244), and ASM-0244 reads them as one |
| A2. REST operations consumed by rwb-access |  |  |  |  |  |
| Operation | Provider | Purpose | Call type | On failure | Note |
| Sign-in, user JWT and group to role | ACE Common (ACE team), through gateway-bff | Entra ID sign-in with MFA, and the group membership that resolves to a role code | REST / OIDC | no token and no session: the request ends at the gateway with 401 | Architecture v5 slide 14 (P4 OUT) and slide 30 |
| None other | - | rwb-access reads no other service; the role, permission, conflict, masking and DoA data it serves is its own | - | - | Architecture v5 slide 14: events none, the reference-data owner |
| A3. Events published (topic rwb.access.events.v1, CloudEvents) |  |  |  |  |  |
| Event | Key | Published when | Consumers | Payload | Note |
| AccessPolicyChanged | roleCode | a role, permission, role-conflict, scope or masking row changes, including a break-glass grant | all 19 services (cache refresh); gateway-bff | role code, policy version and the changed areas; no personal data | Architecture v5 slide 43 additions row; no EV number is assigned in the source |
| DoaLimitChanged | roleCode + product group | a delegation_limit row changes, or a new DoA rule version is in force (DOA-2026.11 to DOA-2027.01) | P7 rwb-decision (ApprovalWorkflow); the services with an approval step | limit, version and effective dates | Architecture v5 slide 43 additions row |
| A4. Events consumed |  |  |  |  |  |
| None. rwb-access is the reference-data owner for access, so it consumes no event (Architecture v5 slide 14: events none). |  |  |  |  |  |
| A5. Workflow and schedule |  |  |  |  |  |
| Item | Type | When | Task queue | Purpose | Note |
| JOB-18 access review list | Temporal Schedule | six-monthly | rwb-access | publish the list of every holder of every role for the role owner to recertify (Access flow, Review steps 1 to 3) | Architecture v5 slide 44; Ownership Map v1 Jobs |
| Workflow | none | - | - | no workflow is specified for rwb-access; the authorise call is a synchronous read | Architecture v5 slide 14 lists a Schedule only |
| A6. Tables owned (schema rwb_access, owner P4) |  |  |  |  |  |
| Table | Holds | Written by | Read by | Note |  |
| role | role code, name, class, group, unit, default scope and first release — the Roles tab | a versioned reference load with an approver | GET /me/permissions, POST /authorise | Ownership Map v1 Tables |  |
| permission | the 54 roles against the 14 capability areas, letters C R U D A or - — the Permissions tab | a versioned reference load with an approver (RW-SECADM) | POST /authorise | Ownership Map v1 Tables |  |
| role_conflict | the eight separation-of-duty pairs — the Separation of duty tab | a versioned reference load with an approver | the grant check and the sign-in check | Ownership Map v1 Tables |  |
| masking_rule | the masking rule per role, area and field group | a versioned reference load with an approver (RW-COMPLY, DL26) | GET /masking-policies | Ownership Map v1 Tables |  |
| delegation_limit | the DoA limit per role, product and action, with its version and effective dates | a DoA change with an approver; publishes DoaLimitChanged | GET /doa-limits | Ownership Map v1 Tables; the amounts are Not specified in the source documents (GAP-0162; ASM-0246) |  |
| access log | every sign-in, authorise decision, refusal and break-glass action, append-only | the service on every decision | GET /admin/access-log | named by Architecture v5 slides 14 and 41; the table name, columns and retention are Not specified in the source documents (GAP-0165; ASM-0249) |  |
| A7. Contract fake and the build rule |  |  |  |  |  |
| Fake | Covers | Fixtures | Used by | Note |  |
| rwb-access stub v1 | POST /authorise, GET /me/permissions, GET /doa-limits, GET /masking-policies | 54 role fixtures taken from the Roles tab; allow and deny per area; unknown role; policy version mismatch; a 2 s timeout | the contract tests of every service (C dependency on RWB-P4-E1037-CON) | contract first: the fake is generated from the OpenAPI document of the contract story, so no service waits for P4 to be built (Template and Rules R5.7 rule 2; DP-08) |  |
| A8. Call-type summary |  |  |  |  |  |
| Call type | Use in the authorise path | Rule | Note |  |  |
| REST | POST /authorise; GET /me/permissions, /doa-limits, /masking-policies; the four administration operations of A1 | one hop; 2 s timeout; circuit breaker per downstream; GET retry once with jitter; POST not retried | Architecture v5 slide 35 note |  |  |
| Kafka | AccessPolicyChanged and DoaLimitChanged to every service; audit and PII logs on the ACE PII path | CloudEvents, outbox in the same transaction, key roleCode, BACKWARD schema | Architecture v5 slides 30 and 43 |  |  |
| Temporal | JOB-18 access review list only | Schedule in rwb-access, namespace rwb-recovery | Architecture v5 slide 44 |  |  |
| File | None | - | - |  |  |
| A9. Check sequence on every action |  |  |  |  |  |
| Step | What happens | Source |  |  |  |
| 1 | Sign-in at gateway-bff with Entra ID and MFA; an idle session ends after 15 minutes | Architecture v5 slides 30 and 35 |  |  |  |
| 2 | ACE Common returns the group membership; rwb-access resolves each Entra ID group of the Single sign-on tab to a role code, one group per role per environment | Architecture v5 slides 14, 30 and 41; Single sign-on tab |  |  |  |
| 3 | The service resolves the subject's roles, scope, DoA limit and masking from rwb-access and caches the answer; the cache lifetime is Not specified in the source documents (GAP-0161; ASM-0245) | Architecture v5 slide 35: cached permission data from rwb-access |  |  |  |
| 4 | The service checks the object itself (OWASP API1 object-level authorisation) against the scope the answer names: Own, Team, All or Placed cases | Architecture v5 slide 35; Key tab of this document |  |  |  |
| 5 | An approve action is compared with the DoA limit for the role, product and action; above the limit the action routes to the approver role through ApprovalWorkflow in P7 | Architecture v5 slide 14 (P7 IN); Temporal and Drools design, L3 kit Approval template |  |  |  |
| 6 | Personal data is masked by the masking rule before it leaves the service; a field with no rule is masked | Architecture v5 slides 35 and 41 |  |  |  |
| 7 | The decision, the role code, the policy version, the area and the outcome go to the access log and to the ACE PII path (Kafka to the SOC) | Architecture v5 slides 30, 35 and 41 |  |  |  |
| 8 | A change of role, permission, scope, masking or DoA publishes AccessPolicyChanged or DoaLimitChanged; every service refreshes its cache on the event | Architecture v5 slides 14, 41 and 43 |  |  |  |
| A10. Refusal and failure model |  |  |  |  |  |
| Case | Response | Message | Seen by |  |  |
| No token, or a session that has ended | 401 | MSG-P4-001 | the user |  |  |
| The role holds no letter in the area | 403 | MSG-P4-002 | the user |  |  |
| The record is outside the role's scope | 404, and the excluded count is never shown | MSG-P4-003 | the user |  |  |
| An approve action above the DoA limit | the action is routed to the approver role named for the limit | - | the user and the approver |  |  |
| rwb-access does not answer inside 2 s, or the circuit is open | the action is refused and logged, which is the fail-closed reading recorded as ASM-0245; the source states the timeout and the breaker but not the outcome (GAP-0161) | - | the user and RW-PLATADM |  |  |
| An unknown role code, or a policy version the caller does not hold | the action is refused and logged | - | RW-SECADM |  |  |
| Message IDs are those of the access story RWB-E1-037 and are kept unchanged. |  |  |  |  |  |
| A11. Owner, dependency and wave |  |  |  |  |  |
| Item | Value |  |  |  |  |
| Owner | P4 rwb-access (Microservice Ownership Map v1 Services sheet; Architecture v5 slides 14, 35 and 41) |  |  |  |  |
| Contract stories | RWB-P4-E1037-CON for P4 rwb-access; RWB-PLT-E1037-CON for the access guard library (Template and Rules DP-08) |  |  |  |  |
| Consumers | all 19 services; gateway-bff; the Approval template of the workflow kit in P7 |  |  |  |  |
| Wave and readiness | wave 1 (P4, Architecture v5 slide 41); the contract is Day 1 and every consumer builds against its fake (Template and Rules R5.4 and R5.7) |  |  |  |  |
| Non-human actors | the six SY roles of the Roles tab are authorised on the same path; their credential is Not specified in the source documents (GAP-0166; ASM-0250) (Architecture v5 slide 35: mTLS, identified both ways) |  |  |  |  |
| Partner roles | the seven PT roles are held as role rows by P4 while the partner user record is S9 rwb-partner; the mapping is Not specified in the source documents (GAP-0164; ASM-0248) (Ownership Map v1 ruling) |  |  |  |  |

## Sheet: Area owners

| Capability areas of the Permissions tab and the service that owns each one (D-RCV-60) |  |  |  |  |  |
|---|---|---|---|---|---|
| Every owner is taken from the Microservice Ownership Map v1 (Services, Tables, Endpoints, Jobs, Events and Parameters sheets) and Architecture v5 slide 41. The letters of the Permissions tab are not changed; this sheet says where each area's data and enforcement live. |  |  |  |  |  |
| Capability area | Owning service | Schema | REST base | What the owner holds (Ownership Map v1) | Roles with a letter in this area (of 54) |
| Case record | P3 rwb-case | rwb_case | /api/recovery/case/v1 | recovery_case, case_account, case_party, task, timer (Tables); EV-01 CaseCreated, EV-04 CaseTransferred (Events); GET /cases/{id} (Endpoints) | 42 |
| Queue and allocation | P3 rwb-case | rwb_case | /api/recovery/case/v1 | queue, queue_member, assignment, queue_measure (Tables); JOB-03 morning allocation, JOB-06 rebalancing (Jobs) | 27 |
| Treatment and offer | S2 rwb-treatment | rwb_treatment | /api/recovery/treatment/v1 | treatment (Tables); EV-10 TreatmentApproved (Events); TreatmentWorkflow (Workflows and activities) | 20 |
| Litigation | S4 rwb-litigation | rwb_litigation | /api/recovery/litigation/v1 | legal_action, hearing (Tables); LitigationWorkflow; JudgmentRecorded and AuctionResult (Architecture v5 slide 43, additions row); Partner instruction in the kit (S4) | 30 |
| Asset and disposal | S5 rwb-asset | rwb_asset | /api/recovery/asset/v1 | asset_sale, listing (Tables); EV-22 AssetTakenOn (Events); JOB-19 re-appraisal (Jobs); AssetDisposalWorkflow | 31 |
| Debt sale | S6 rwb-debtsale | rwb_debtsale | /api/recovery/debtsale/v1 | debt_sale_lot, debt_sale_account (Tables); EV-23 LotAwarded (Events); DebtSaleWorkflow | 21 |
| Write-off and posting | S7 rwb-writeoff | rwb_writeoff | /api/recovery/writeoff/v1 | write_off (Tables); EV-24 WriteOffApproved (Events); WriteOffWorkflow; JOB-16 write-off scan (Jobs) | 17 |
| Documents | P5 rwb-document | rwb_document | /api/recovery/document/v1 | document, document_custody, document_text, signature_request, retention_rule (Tables); EV-16 and EV-17 (Events); DocumentIntakeWorkflow; JOB-12 document intake, JOB-17 retention (Jobs) | 42 |
| Rules and parameters | P7 rwb-decision (rules) + P3 rwb-case (parameters) | rwb_decision; rwb_case | /api/recovery/decision/v1; /api/recovery/case/v1 | rule_package, rule_package_version, rule_row, rule_test_case (P7); parameter_catalog, parameter_value (P3; contract RWB-P3-E1042-CON); JOB-20 rule promote | 38 |
| Reference data | P3 rwb-case | rwb_case | /api/recovery/case/v1 | reference_row, reference_version, lov_value (Tables); contract RWB-P3-E1043-CON; R-PREC default ruling, DP-07 | 42 |
| Decision log | P7 rwb-decision | rwb_decision | /api/recovery/decision/v1 | decision_log_entry, approval (Tables); EV-08 DecisionRecorded on rwb.decision-record.v1; JOB-14 hash-chain check | 39 |
| Partner portal | S9 rwb-partner | rwb_partner | /api/recovery/partner/v1 | partner, partner_instruction, partner_user (Tables); EV-20 InstructionIssued, EV-21 PartnerResultSubmitted (Events); InstructionWorkflow | 29 |
| Reporting | P9 rwb-reporting | rwb_reporting | /api/recovery/reporting/v1 | measure_definition, measure_snapshot, measure_publish (Tables); JOB-15 reporting extract (Jobs) | 36 |
| Platform administration | P2 rwb-integration + PLT platform library | rwb_integration | /api/recovery/integration/v1 | interface_config, outbound_item, job_catalog (P2); feature_flag, feature_flag_change (PLT, R-PREC default ruling) | 6 |
| Not an area of the matrix: the role, permission, scope, DoA and masking data itself | P4 rwb-access | rwb_access | /api/recovery/access/v1 | role, permission, role_conflict, masking_rule, delegation_limit (Tables); POST /authorise, GET /me/permissions, /doa-limits, /masking-policies (Architecture v5 slide 14); JOB-18 access review | 54 (every role is resolved here) |
| Note - partner and customer roles: the seven PT roles and the four CU roles are held as role rows by P4, while the partner user record is owned by S9 rwb-partner (Ownership Map v1 ruling) and a customer reaches the Workbench through the bank channels; the mapping of a partner user to role codes is Not specified in the source documents (GAP-0164; ASM-0248). |  |  |  |  |  |
| Note - derived counts: the last column counts the non-dash letters of each column of the Permissions tab, so it is a count of roles, not of rights. It is computed here and no cell of the Permissions tab changes. |  |  |  |  |  |
