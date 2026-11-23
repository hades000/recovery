## Sheet: Read me

| SCB Collections and Recovery. Henka Group, 22 November 2026. |
|---|
| (C) Siam Commercial Bank and Henka Pte Ltd |
| Recovery Workbench System Disposition and Integration Inventory v4. Decision D-RCV-60. Next version of Recovery Workbench System Disposition and Integration Inventory v3 (15 November 2026). |
| The 25 systems and tools that recovery uses today and the 36 numbered interfaces with the 32 systems behind them: what happens to each path, who owns the data path and when, the route, the data product and the standard. Every section, ID, number and date of v3 is kept. The realignment adds one Service column to the Disposition and Interfaces sheets and fills it for every row from the Microservice Ownership Map v1; the By route counts are calculated, and a By service sheet, the Service rules and the Realignment changes are added. |
| Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. |
| Status: Draft. This document is issued with no approval recorded (ASM-B-TECH-16-1). |
| Release: the paths are delivered across waves 1 to 4 of the Microservice Ownership Map v1. No release date appears in v3 and none is added; any release date written into this workbook later is tentative (Template and Rules v1 R1 U7; DL48). |
| Change log |
| v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| v3, 15 November 2026 (the source of this version; it is not changed by this run). |
| What this version holds |
| Disposition: the 25 systems and tools of v3, one row each, with Role in recovery today, Disposition, In ACE today, Owner, What the Workbench does with it, From, Interfaces and Decision unchanged; one Service column added after Owner and filled on 25 of 25 rows. |
| Interfaces: the 36 numbered interfaces of v3, one row each, with System, What the Workbench uses it for, Direction, Route, Path, Frequency, Data product, In ACE today, Owner, First needed, Standard and Decision unchanged; one Service column added after Owner and filled on 36 of 36 rows. |
| By route: the six rows of v3 (COLLINS, File, Direct through ACE, Through partners, Not at all today and Total) with the In, Out, Both and Total counts calculated from the 36 interfaces. v3 left every count cell empty although the sheet says it is calculated (CG-B-TECH-16-1; ASM-B-TECH-16-2). |
| By service: new sheet. The 36 interfaces counted per owning service, calculated from the Service column, with the interfaces of each service named. |
| Key: the 23 key rows of v3 unchanged, plus six rows for the Service column, the per-service reading of the Owner column, the two interface IDs that Architecture v5 removes, and the pointer to the Service rules. |
| Service rules: new sheet. One rule per path group with the service it gives and the slide, ADR or Ownership Map ruling behind it. |
| Realignment changes: new sheet. Every change of this version with the v3 value, the v4 value, the decision, the pattern and the basis. |
| Counts |
| 25 systems and tools: 25 Service cells filled; 15 rows lead with P1 rwb-source-data and 9 name more than one service because the source row spans more than one interface. |
| 36 interfaces: P1 rwb-source-data owns 17, P6 rwb-comms 3, S5 rwb-asset 3, P2 rwb-integration 2, P9 rwb-reporting 2, and P4 rwb-access, P8 rwb-payment, P10 rwb-agent, PLT (RWB-PLT-OBS), S3 rwb-guarantee, S4 rwb-litigation, S6 rwb-debtsale, S8 rwb-deviation and S9 rwb-partner 1 each. |
| 2 interface IDs kept although Architecture v5 removes them: INT-19 (data lake and Power BI) and INT-20 (COLLINS model learning). |
| 16 of the 20 owner entries own at least one row: the 19 services and the platform observability set, less P3 rwb-case, S1 rwb-valuation, S2 rwb-treatment, S7 rwb-writeoff (CG-B-TECH-16-3; ASM-B-TECH-16-13). |
| Sources |
| Recovery Workbench System Disposition and Integration Inventory v3.xlsx (15 November 2026), sheets Disposition, Interfaces, By route and Key. |
| Recovery Workbench System Disposition and Integration Inventory v2.xlsx (3 November 2026), sheet By route, read only to confirm that the counts were blank there too. |
| Recovery Workbench Microservice Ownership Map v1, sheets Services, Tables, Endpoints and Jobs, and _work/msr/plan/ownership.json. |
| Recovery Workbench Architecture v5 Text Extract v1, slides 2, 6, 7, 8, 9, 13 to 20, 23, 29, 30, 37, 41, 44 and 45. |
| Recovery Workbench Temporal and Drools Design Text Extract v1 (one transaction, decision record, points of no return). |
| Recovery Workbench Microservice Story Template and Rules v1 R1 (U2, U5, U7), R3 (R-PREC and the default rulings), R5.5 (DP-01, DP-05, DP-11, DP-16, DP-17, DP-18), R8.1, R8.2 and R9. |
| _work/msr/plan/ids.json: ADR-013 to ADR-023 and DL44 to DL49 are the decisions of this run. |
| Open points |
| INT-19 and INT-20 stay in this workbook with the IDs of v3 while Architecture v5 removes them; no story is raised for either (CG-B-TECH-16-2; ASM-B-TECH-16-4). |
| The source names no owning service for any system or interface; the Service column is derived from the Ownership Map and the Architecture v5 catalogue and the rule behind each group sits on the Service rules sheet (CG-B-TECH-16-4; ASM-B-TECH-16-3). |
| The data product of INT-06 reads To confirm in v3 and is kept as written (CG-B-TECH-16-5; ASM-B-TECH-16-5). |
| INT-33 has no standard in v3 and two candidate services, S4 and S9 (CG-B-TECH-16-6; ASM-B-TECH-16-9). |
| Three statements of v3 are kept word for word although they read as outdated: the Interfaces description says the Workbench owns the reporting feeds, the Disposition description says the workbook supersedes v2, and the partner portal row says the external gateway (CG-B-TECH-16-7; CG-B-TECH-16-8; ASM-B-TECH-16-10; ASM-B-TECH-16-11). |
| No date is raised by this workbook: no release date appears in the source (ASM-B-TECH-16-16). |

## Sheet: Disposition

| System disposition |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 25 systems and tools that recovery uses today, what happens to each, who owns the data path and when. Supersedes v2. |  |  |  |  |  |  |  |  |  |
| System | Role in recovery today | Disposition | In ACE today | Owner | Service | What the Workbench does with it | From | Interfaces | Decision |
| Core bank (ALS) | System of record for loan accounts, balances, payments and bookings | Keep | Partly | ACE team | P1 rwb-source-data (INT-01, INT-02); P8 rwb-payment (INT-03) | ACE ingests the accounts, payments and bookings daily and the Workbench reads them through v_ace_account and v_ace_payment; the officer still books in the core bank | E1 | INT-01, INT-02, INT-03 | DL12 |
| SCBPDM | Customer profile, identifiers and contact details | Keep | Partly | ACE team | P1 rwb-source-data | ACE ingests the customer profile, identifiers and contact details and the Workbench reads them through v_ace_customer and v_ace_contact | E1 | INT-04 | DL20 |
| UDP | Customer and account attributes in the data platform | Keep | Yes | ACE team | P1 rwb-source-data | ACE ingests the customer and account attributes through COLLINS and the Workbench reads them through the account and customer views | E1 | INT-05 | DL20 |
| AAL | Data ACE already receives | Keep | Yes | ACE team | P1 rwb-source-data | ACE ingests the data through COLLINS and the Workbench reads it through the account and customer views | E1 | INT-06 | DL12 |
| EFS | Collections case handling to day 90; recovery teams also look up history in it | Keep for collections | Partly | ACE team | P1 rwb-source-data | Takes over each case at day 90 with its contact history, action codes and promises, read through v_ace_efs_action; recovery case handling moves to the Workbench | E1 | INT-07 | DL29 |
| COLLINS | Collection engine data platform and models | Keep and feed | Partly | ACE team | P1 rwb-source-data (INT-08); P9 rwb-reporting (INT-20) | Feeds the daily batch ACE ingests; receives decisions and outcomes back for model learning | E1 | INT-08, INT-20 | DT12 |
| ACE | Collection workbench in production: sign-in, access, audit, case view, restructure calculator | Extend | Yes | ACE team | P2 rwb-integration (INT-34); P4 rwb-access (INT-21); PLT RWB-PLT-OBS (INT-22) | The Workbench is built inside ACE as its recovery module; common parts are reused and source data is read through the v_ace_* views | E1 | INT-21, INT-22, INT-34 | DT07, DT08 |
| LIT | Litigation tracking and lawsuit numbers | Keep | No | ACE team | P1 rwb-source-data (INT-09); S4 rwb-litigation (INT-33) | ACE ingests the litigation status and hearings and the Workbench reads them through v_ace_lawsuit and v_ace_hearing; law firms report through the partner portal from Epic 5 | E1 | INT-09, INT-33 | DL12 |
| CCMS | Collateral records | Keep | Partly | ACE team | P1 rwb-source-data | ACE ingests the weekly file and the Workbench reads it through v_ace_collateral and v_ace_collateral_detail | E1 | INT-10 | DL06, DL12 |
| SVAF | Appraisals | Keep | No | ACE team | P1 rwb-source-data | ACE ingests the appraisal file, which replaces the manual appraisal file, and the Workbench reads it through v_ace_valuation | E1 | INT-11 | DL06, DL12 |
| AMIS | Assets held, book values and asset sales | Keep | Partly | ACE team | P1 rwb-source-data | ACE ingests the monthly file and the Workbench reads it through v_ace_npa_asset and v_ace_npa_sale | E3 | INT-12 | DL06, DL12 |
| RPS | Repossessed vehicles and stock | Keep | No | ACE team | P1 rwb-source-data | ACE ingests the weekly file and the Workbench reads it through v_ace_npa_asset | E3 | INT-13 | DL06, DL12 |
| WIN | Registered mail for notices | Keep | No | ACE team | P6 rwb-comms (INT-14); P1 rwb-source-data (INT-15) | Sends notices out by daily file; ACE ingests the proof of delivery weekly and the Workbench reads it through v_ace_pod | E1 | INT-14, INT-15 | None |
| GL | General ledger | Keep | No | ACE team | P1 rwb-source-data | ACE ingests the monthly write-off postings and the Workbench reads them through v_ace_write_off | E6 | INT-16 | DL12 |
| NSS and LINE OA | SMS and LINE messages to customers | Keep | Yes | ACE team | P6 rwb-comms (INT-17, INT-18) | Sends through the ACE notification path | E2 | INT-17, INT-18 | DL30 |
| Data lake and Power BI | Bank reporting | Keep and feed | Not applicable | Workbench | P9 rwb-reporting (INT-19) | Receives case, queue, decision and outcome data daily; recovery reports move here from spreadsheets | E1 | INT-19 | None |
| Enterprise AI model endpoint | Bank model hosting in the SCB tenant | Reuse | No | Bank platform | P10 rwb-agent (INT-23) | The agents call it through a private endpoint | E1 | INT-23 | DL33 |
| Partner portal | Does not exist | New | No | Workbench | S9 rwb-partner (INT-24); S6 rwb-debtsale (INT-25) | Workbench screens for law firms, auction houses and buyers through the external gateway; needs the architecture change with one to three months of lead time | E5 | INT-24, INT-25 | DL03 |
| NLEADS | Credit approval for restructure plans | Keep | No | ACE team | P1 rwb-source-data (INT-35); no path for INT-26 (the officer submits in NLEADS) | ACE ingests the credit decision result through INT-35 and the Workbench reads it through v_ace_credit_decision; the officer still submits the request in NLEADS (INT-26) | E3 | INT-26, INT-35 | DL12 |
| HOME.SCB | Public listing of assets for sale | Keep | No | Workbench | S5 rwb-asset (INT-27) | No interface; the sales team publishes the listing and records it on the asset | E4 | INT-27 | DL12 |
| SCIS, TCG, NCB, Aric, Salesforce | Vehicle transfer, guarantee claims, contact tracing, fraud referral, NPA work orders | Keep | No | Workbench | S5 rwb-asset (INT-28, INT-32); S3 rwb-guarantee (INT-29); P1 rwb-source-data (INT-30); S8 rwb-deviation (INT-31) | No interface; the officer works in the system and records the result on the case | E3 | INT-28 to INT-32 | DL12 |
| Recovery team spreadsheets and SharePoint lists | Open recovery work, trackers and approvals | Retire | No | Workbench | P1 rwb-source-data | Leaves system scope; open items are cleared or migrated in the cutover, then each spreadsheet retires with a read-only archive | E1 | None (cutover) | None |
| Email approvals in Outlook | Approval of recovery decisions | Replace | No | Workbench | P7 rwb-decision | Approvals move to the Workbench approval queue with the decision log | E2 | None | None |
| Shared folders of scanned documents | Recovery documents and originals custody | Replace | No | Workbench | P5 rwb-document | The document hub becomes the system of record for recovery documents | E1 | None | DT06 |
| EasyApp | E-signature for restructure agreements | Keep | No | ACE team | P1 rwb-source-data (INT-36); P5 rwb-document for the signed file | ACE ingests the signature request reference and status through INT-36 and the Workbench reads it through v_ace_esign; the signed file stays in the document hub | E2 | INT-36 | D-RCV-35 |

## Sheet: Interfaces

| Integration inventory |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 36 numbered interfaces with 32 systems. ACE ingests every inbound source and the Workbench reads it through the read-only v_ace_* views. The Workbench owns its outbound files, the reporting feeds and the partner portal; SMS, LINE and the audit and security logs (INT-17, INT-18, INT-22) leave through paths the ACE team owns. No component calls a system of record directly. INT-35 (NLEADS credit decision) and INT-36 (EasyApp e-signature) are the two new ACE inbound interfaces raised in RWB-ACE-001. |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ID | System | What the Workbench uses it for | Direction | Route | Path | Frequency | Data product | In ACE today | Owner | Service | First needed | Standard | Decision |
| INT-01 | Core bank (ALS) | Loan accounts, balances, arrears, days past due, classification | In | COLLINS | ACE ingests the COLLINS batch | Daily, end of day | DP01 | Partly | ACE team | P1 rwb-source-data | E1 | File specification | None |
| INT-02 | Core bank (ALS) | Payments posted to each account | In | COLLINS | ACE ingests the COLLINS batch | Daily, end of day | DP01, DP13 | Yes | ACE team | P1 rwb-source-data | E1 | File specification | None |
| INT-03 | Core bank (ALS) | Restructure, settlement and write-off bookings | Out | Not at all today | Booked by the officer; confirmed on the next day's load | As approved | DP04, DP13 | Not applicable | Workbench | P8 rwb-payment | E3 | None | DL12 |
| INT-04 | SCBPDM | Customer profile, identifiers and contact details | In | COLLINS | ACE ingests the COLLINS batch | Daily, end of day | DP02 | Partly | ACE team | P1 rwb-source-data | E1 | File specification | DL20 |
| INT-05 | UDP | Customer and account attributes held in the data platform | In | COLLINS | ACE ingests the COLLINS batch | Daily, end of day | DP01, DP02 | Yes | ACE team | P1 rwb-source-data | E1 | File specification | DL20 |
| INT-06 | AAL | Data ACE already receives through COLLINS | In | COLLINS | ACE ingests the COLLINS batch | Daily, end of day | To confirm | Yes | ACE team | P1 rwb-source-data | E1 | File specification | DL12 |
| INT-07 | EFS | Collections history, action codes and promises before day 90 | In | COLLINS | ACE ingests the COLLINS batch | Daily, end of day | DP05 | Partly | ACE team | P1 rwb-source-data | E1 | File specification | DL29 |
| INT-08 | COLLINS models | Scores, return by route, price and sale success estimates, scheme suggestions | In | COLLINS | ACE ingests the COLLINS batch | Daily; monthly for some models | DP11 | No | ACE team | P1 rwb-source-data | E1 | File specification | None |
| INT-09 | LIT | Litigation status and lawsuit numbers | In | COLLINS | ACE ingests the COLLINS batch | Daily, end of day | DP07 | No | ACE team | P1 rwb-source-data | E1 | File specification | None |
| INT-10 | CCMS | Collateral records | In | File | ACE ingests the file | Weekly | DP06 | Partly | ACE team | P1 rwb-source-data | E1 | File specification | DL06, DL12 |
| INT-11 | SVAF | Appraisals | In | File | ACE ingests the file | Weekly | DP06 | No | ACE team | P1 rwb-source-data | E1 | File specification | DL06, DL12 |
| INT-12 | AMIS | Assets held, book values and asset sales | In | File | ACE ingests the file | Monthly | DP06 | Partly | ACE team | P1 rwb-source-data | E3 | File specification | DL06, DL12 |
| INT-13 | RPS | Repossessed vehicles and stock | In | File | ACE ingests the file | Weekly | DP06 | No | ACE team | P1 rwb-source-data | E3 | File specification | DL06, DL12 |
| INT-14 | WIN | Demand, recall and sale notices for registered mail | Out | File | File | Daily | DP07 | No | Workbench | P6 rwb-comms | E1 | File specification | None |
| INT-15 | WIN | Proof of delivery for registered mail | In | File | ACE ingests the file | Weekly | DP07 | No | ACE team | P1 rwb-source-data | E2 | File specification | None |
| INT-16 | GL | Write-off postings | In | File | ACE ingests the file | Monthly | DP13 | No | ACE team | P1 rwb-source-data | E6 | File specification | DL12 |
| INT-17 | NSS | SMS to customers | Out | Direct through ACE | ACE notification path | As sent | DP05 | Yes | ACE team | P6 rwb-comms | E2 | Common module interface | DL30 |
| INT-18 | LINE OA | LINE messages to customers | Out | Direct through ACE | ACE notification path | As sent | DP05 | Yes | ACE team | P6 rwb-comms | E2 | Common module interface | DL30 |
| INT-19 | Data lake and Power BI | Case, queue, decision and outcome data for reporting | Out | File | Daily batch | Daily | DP03, DP12 | Not applicable | Workbench | P9 rwb-reporting | E1 | File specification | None |
| INT-20 | COLLINS | Decisions and outcomes for model learning | Out | File | Daily batch to the data lake | Daily | DP12 | Not applicable | Workbench | P9 rwb-reporting | E2 | File specification | None |
| INT-21 | Entra ID and the bank IAM | Sign-in and the roles each user holds | In | Direct through ACE | ACE sign-in | At each sign-in | DP14 | Partly | ACE team | P4 rwb-access | E1 | OpenID Connect | DL40 |
| INT-22 | PII Kafka, audit and SOC logs | Personal data access, audit and security events | Out | Direct through ACE | ACE logging | As they happen | None | Yes | ACE team | PLT RWB-PLT-OBS | E1 | AsyncAPI 3.0 | None |
| INT-23 | Enterprise AI model endpoint | The model the agents call | Both | Direct through ACE | Private endpoint in the SCB tenant | Per request | None | No | Bank platform | P10 rwb-agent | E1 | OpenAPI 3.1 | DL33 |
| INT-24 | Partner portal | Instructions to partners and the results they report | Both | Direct through ACE | Workbench screens through the external gateway | As entered | DP06, DP07, DP08 | No | Workbench | S9 rwb-partner | E2 | OpenAPI 3.1 | DL03 |
| INT-25 | Debt buyers | Debt sale data tape for an awarded lot | Out | File | File through the data room | Per lot | DP09 | No | Workbench | S6 rwb-debtsale | E5 | File specification | None |
| INT-26 | NLEADS | Credit approval for restructure plans | Out | Not at all today | Submitted by the officer in NLEADS; the decision returns through INT-35 | As needed | DP04 | Not applicable | Workbench | P2 rwb-integration | E3 | None | DL12 |
| INT-27 | HOME.SCB | Listings of assets for sale | Out | Not at all today | Not available today; published by the sale officer | As listed | DP06 | No | Workbench | S5 rwb-asset | E3 | None | DL12 |
| INT-28 | SCIS | Vehicle registration transfer | Out | Not at all today | Not available today; prepared by the officer | As needed | DP06 | No | Workbench | S5 rwb-asset | E4 | None | DL12 |
| INT-29 | Thai Credit Guarantee Corporation | Quota and claim submission | Both | Not at all today | Not available today; entered and filed by the guarantee officer | As needed | DP04 | No | Workbench | S3 rwb-guarantee | E4 | None | DL12 |
| INT-30 | NCB | Contact tracing for lost contact | In | Not at all today | Not available today; by the officer | As needed | DP02 | No | Workbench | P1 rwb-source-data | E7 | None | DL12 |
| INT-31 | Aric | Fraud referral | Out | Not at all today | Not available today; by the fraud investigator | As needed | None | No | Workbench | S8 rwb-deviation | E8 | None | DL12 |
| INT-32 | Salesforce | Work orders and operational status for NPA | In | Not at all today | Not available today | None | DP06 | No | Workbench | S5 rwb-asset | Not planned | None | DL12 |
| INT-33 | Legal Execution Department and courts | Enforcement and court records | In | Through partners | Through the law firms in the partner portal | As entered | DP07 | Not applicable | Workbench | S4 rwb-litigation | E5 | None | None |
| INT-34 | ACE common module | Shared case view, entities, restructure calculator, notification path | Both | Direct through ACE | Published module interface | Per request | DP03, DP04 | Yes | ACE team | P2 rwb-integration | E1 | Module interface | DL14 |
| INT-35 | NLEADS | Credit decision result for restructure plans | In | File | ACE ingests the file | As decisions are made | DP04 | No | ACE team | P1 rwb-source-data | E3 | File specification | D-RCV-35 |
| INT-36 | EasyApp | E-signature reference and status for restructure agreements | In | File | ACE ingests the file | As signatures are requested | DP10 | No | ACE team | P1 rwb-source-data | E2 | File specification | D-RCV-35 |

## Sheet: By route

| Interfaces by route and direction |  |  |  |  |
|---|---|---|---|---|
| Calculated from the Interfaces tab. |  |  |  |  |
| Route | In | Out | Both | Total |
| COLLINS | 8 | 0 | 0 | 8 |
| File | 8 | 4 | 0 | 12 |
| Direct through ACE | 1 | 3 | 3 | 7 |
| Through partners | 1 | 0 | 0 | 1 |
| Not at all today | 2 | 5 | 1 | 8 |
| Total | 20 | 12 | 4 | 36 |

## Sheet: Key

| Key |  |  |
|---|---|---|
| What each disposition, route and standard means. |  |  |
| Item | Term | Meaning |
| Disposition | Keep | The system stays as it is; the Workbench reads from it or the officer works in it |
| Disposition | Keep for collections | The system stays for collections; recovery work moves to the Workbench |
| Disposition | Keep and feed | The system stays and the Workbench sends data back to it |
| Disposition | Extend | The Workbench is built inside it |
| Disposition | Reuse | The Workbench uses the bank service as it is |
| Disposition | New | Built for the Workbench |
| Disposition | Replace | The Workbench takes over the work; the old way stops |
| Disposition | Retire | Switched off after the content moves to the Workbench |
| Route | COLLINS | The COLLINS daily batch, ingested by ACE and read through the v_ace_* views |
| Route | File | An inbound file ACE ingests, or an outbound file through the integration adapters |
| Route | Direct through ACE | A path ACE already runs: sign-in, logging, the notification path, the common module, the model endpoint, the partner portal |
| Route | Through partners | Entered by a partner in the partner portal |
| Route | Not at all today | No interface. A person does the step in the other system and records it on the case |
| Standard | OpenAPI 3.1 | Request and response interfaces |
| Standard | AsyncAPI 3.0 | Event interfaces |
| Standard | File specification | Batch files: layout, control totals, business date and checks, in the interface specifications |
| In ACE today | Yes | Every field the Workbench reads is in an ACE table that exists today (Tier 1), read through a v_ace_* view |
| In ACE today | Partly | Part of the data is in ACE tables today (Tier 1); RWB-ACE-001 adds the rest as new ACE tables or columns (Tier 2) |
| In ACE today | No | ACE does not hold it today; where the Workbench reads it, RWB-ACE-001 adds it as new ACE tables or columns only (Tier 2) |
| In ACE today | Not applicable | No source record for ACE to hold: a booking or submission the officer makes in the other system (INT-03, INT-26), a Workbench reporting feed (INT-19, INT-20) or records entered by partners (INT-33) |
| Owner | ACE team | Owns the ingestion and the data the Workbench reads for this system |
| Owner | Workbench | Owns the Workbench path to or from this system |
| Owner | Bank platform | Owns a shared bank service the Workbench calls |
| Service | P1 to P10, S1 to S9 and PLT | The owning service of the path, from the Microservice Ownership Map v1 and the Architecture v5 service catalogue (D-RCV-60; ADR-013, ADR-014). Every row of the Disposition and Interfaces sheets carries one; where a source row spans several interfaces the cell names one service per interface. |
| Owner | Workbench (read as per service) | v3 names the single Workbench. In this version each Workbench path is owned by the service in the Service column (D-RCV-60; ASM-B-TECH-16-3). |
| Owner | ACE team (read as the ingest path) | The ACE team keeps the ingestion, the checks and the 30 read-only v_ace_* views; rwb-source-data is the only reader of the views, so the Workbench side of every inbound ACE path is P1 (ADR-010). |
| Owner | Bank platform (read as the endpoint) | The endpoint stays with the bank platform; the Workbench side of INT-23 is P10 rwb-agent (Architecture v5 slides 16 and 30). |
| Interfaces | INT-19, INT-20 | Kept in this version with the IDs of v3 because the inventory keeps every ID. Architecture v5 removes both under DP-17 and ADR-018 (no data lake), so no story is raised for them; open point CG-B-TECH-16-2 (ASM-B-TECH-16-4). |
| Ruling | Service column | One rule per path group sits on the Service rules sheet, rows SR-01 to SR-19, with the slide, ADR or Ownership Map ruling behind each one. |

## Sheet: By service

| Interfaces by owning service |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| Calculated from the Service column of the Interfaces tab. |  |  |  |  |  |  |  |  |
| Service code | Service | Name | Wave | In | Out | Both | Total | Interfaces |
| P1 | rwb-source-data | Source data | 1 | 17 | 0 | 0 | 17 | INT-01, INT-02, INT-04, INT-05, INT-06, INT-07, INT-08, INT-09, INT-10, INT-11, INT-12, INT-13, INT-15, INT-16, INT-30, INT-35, INT-36 |
| P2 | rwb-integration | Integration | 1 | 0 | 1 | 1 | 2 | INT-26, INT-34 |
| P4 | rwb-access | Access and authority | 1 | 1 | 0 | 0 | 1 | INT-21 |
| P6 | rwb-comms | Communications | 1 | 0 | 3 | 0 | 3 | INT-14, INT-17, INT-18 |
| P8 | rwb-payment | Payment | 2 | 0 | 1 | 0 | 1 | INT-03 |
| P9 | rwb-reporting | Reporting | 1 | 0 | 2 | 0 | 2 | INT-19, INT-20 |
| P10 | rwb-agent | Agent | 1 | 0 | 0 | 1 | 1 | INT-23 |
| S3 | rwb-guarantee | Guarantee | 3 | 0 | 0 | 1 | 1 | INT-29 |
| S4 | rwb-litigation | Litigation | 3 | 1 | 0 | 0 | 1 | INT-33 |
| S5 | rwb-asset | Asset | 2 | 1 | 2 | 0 | 3 | INT-27, INT-28, INT-32 |
| S6 | rwb-debtsale | Debt sale | 3 | 0 | 1 | 0 | 1 | INT-25 |
| S8 | rwb-deviation | Deviation | 2 | 0 | 1 | 0 | 1 | INT-31 |
| S9 | rwb-partner | Partner | 4 | 0 | 0 | 1 | 1 | INT-24 |
| PLT | RWB-PLT-OBS | Platform observability | 0 | 0 | 1 | 0 | 1 | INT-22 |
| Total |  |  |  | 20 | 12 | 4 | 36 | 36 numbered interfaces |

## Sheet: Service rules

| Service rules for the Service column |  |  |  |  |
|---|---|---|---|---|
| One rule per path group: the service it gives and the source behind it (D-RCV-60). |  |  |  |  |
| Rule | Path group | Service | Rows covered | Basis |
| SR-01 | Inbound ACE source read through a recovery.v_ace_* view | P1 rwb-source-data | INT-01, INT-02, INT-04 to INT-13, INT-15, INT-16, INT-30, INT-35, INT-36 | ADR-010; Architecture v5 slides 7, 9, 15 and 29: only rwb-source-data reads the 30 recovery.v_ace_* views, every other service asks it through REST or a Temporal activity (ASM-B-TECH-16-6). |
| SR-02 | Booking the officer makes in the core bank | P8 rwb-payment | INT-03 | Architecture v5 slide 17: rwb-payment owns payment and proceeds matching, fees, bookings and posting files; the disposition row keeps the officer booking in the core bank (ASM-B-TECH-16-8). |
| SR-03 | Registered mail letters (WIN) | P6 rwb-comms, with P2 rwb-integration for the file | INT-14 | Architecture v5 slide 17 (rwb-comms: generate letter; Integration: deliverFile) and slide 30 (5); Ownership Map v1 ruling JOB-10 (16:00 window); ASM-B-TECH-16-7. |
| SR-04 | SMS and LINE messages to customers | P6 rwb-comms | INT-17, INT-18 | Architecture v5 slide 17 (ACE Common notification path: SMS, LINE) and slide 30 (5). |
| SR-05 | Sign-in and the roles a user holds | P4 rwb-access | INT-21 | Architecture v5 slide 14 (rwb-access: sign-in, group-to-role) and slide 30 (1); the ACE team keeps the Entra path. |
| SR-06 | Audit and personal-data access logs | PLT RWB-PLT-OBS | INT-22 | Architecture v5 slide 30 (2) and slide 23: every service sends audit and personal-data access logs through the ACE PII Kafka path; the platform capability owns the sender. |
| SR-07 | Enterprise AI model endpoint | P10 rwb-agent | INT-23 | Architecture v5 slide 16 (rwb-agent: Enterprise AI endpoint, HTTPS private endpoint) and slides 6 and 8. |
| SR-08 | Partner portal and the results partners report | S9 rwb-partner | INT-24 | Architecture v5 slide 8 (partner gateway, FAPI 2.0, in front of rwb-partner) and slide 17; ASM-B-TECH-16-11. |
| SR-09 | Debt-buyer data tape for an awarded lot | S6 rwb-debtsale, with P2 rwb-integration for the file | INT-25 | Service Catalog v1, S6 file contract; Architecture v5 slide 17 (Integration: deliverFile, buyer file); ASM-B-TECH-16-7. |
| SR-10 | Reporting and model-learning output | P9 rwb-reporting | INT-19, INT-20 | ADR-018 and Architecture v5 slide 15 (rwb-reporting: measures, snapshots, regulatory reports; deliverFile for the extract); DP-17 removes the data lake. CG-B-TECH-16-2. |
| SR-11 | Credit approval request for a restructure plan | P2 rwb-integration | INT-26 | Architecture v5 slide 16 (interface config, file runs, outbound items, ACE integration paths); API Specification v4 GET /treatments/{treatmentId}/credit-pack, x-module P2. |
| SR-12 | Listing, vehicle transfer and NPA work order | S5 rwb-asset | INT-27, INT-28, INT-32 | Architecture v5 slide 19 (rwb-asset: assets taken on, holding, floor price, listings, auction rounds). |
| SR-13 | Guarantee quota and claim | S3 rwb-guarantee | INT-29 | Architecture v5 slide 18 (rwb-guarantee: TCG and insurance claims, guarantor notices and pursuit). |
| SR-14 | Litigation, enforcement and court records | S4 rwb-litigation, with S9 rwb-partner for the entry | INT-33 | Architecture v5 slide 19 (rwb-litigation: legal actions, hearings, judgments, enforcement) and slide 17 (partners enter through the partner gateway). |
| SR-15 | Deviation screening and handling | S8 rwb-deviation | INT-31 | Architecture v5 slide 15 (rwb-deviation: X1-X7 screening, pause, handling, return). |
| SR-16 | Approval of a recovery decision | P7 rwb-decision | Disposition: Email approvals in Outlook | Architecture v5 slide 14 (rwb-decision: approvals, central decision ledger); DP-03. |
| SR-17 | Recovery documents and originals custody | P5 rwb-document | Disposition: Shared folders of scanned documents; EasyApp signed file | Architecture v5 slide 16 (rwb-document: metadata, custody, OCR, signatures, retention). |
| SR-18 | Open recovery work trackers | P1 rwb-source-data | Disposition: Recovery team spreadsheets and SharePoint lists | API Specification v4 /admin/trackers, x-module P1; trackers leave system scope (D-RCV-35 U5). |
| SR-19 | ACE Common shared services | P2 rwb-integration | INT-34 | Architecture v5 slide 7 (ACE Common, INT-34) and slide 30 (1) to (6): sign-in, logging, shared case view, restructure calculator, notification path and shared entities; rwb-integration owns the interface configuration and the ACE integration paths (ASM-B-TECH-16-12). |

## Sheet: Realignment changes

| Realignment changes in v4 (D-RCV-60) |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| One row per change: the v3 value, the v4 value, the decision, the pattern and the basis. |  |  |  |  |  |  |
| Ref | Sheet | v3 value | v4 value | Decision | Pattern | Basis |
| R-01 | All sheets | Four sheets and no header or change log | Read me sheet first: header lines 1 and 2, document control, change-log row, what the version holds, counts, sources and open points | D-RCV-60 | none | Template and Rules v1 R8.1 and R8.2 |
| R-02 | Disposition | No Service column; Owner was the ACE team, the Workbench or the bank platform | Service column added after Owner and filled on 25 of 25 rows from the Microservice Ownership Map v1 | ADR-013, ADR-014, DL44 | DP-01, DP-05 | Ownership Map v1 sheet Services; Architecture v5 slides 13 to 20 and 41 |
| R-03 | Interfaces | No Service column; Owner was the ACE team, the Workbench or the bank platform | Service column added after Owner and filled on 36 of 36 rows from the Microservice Ownership Map v1 | ADR-013, ADR-014, DL44 | DP-05, DP-11, DP-16 | Ownership Map v1 sheet Services; Architecture v5 slides 15 to 20, 29 and 30; ADR-010 |
| R-04 | Interfaces | The Workbench was one owner for every inbound and outbound path | 17 inbound rows owned by P1 rwb-source-data, the only reader of the recovery.v_ace_* views | ADR-010 | DP-01, DP-05 | Architecture v5 slides 7, 9, 15 and 29 |
| R-05 | Interfaces | INT-14, INT-17 and INT-18 owned by the Workbench | P6 rwb-comms owns INT-14, INT-17 and INT-18; P2 rwb-integration builds and transfers the WIN file | ADR-013 | DP-11, DP-16 | Architecture v5 slides 17, 30 (5) and 44 JOB-10; Ownership Map v1 ruling JOB-10 |
| R-06 | Interfaces | INT-19 and INT-20 nightly to the data lake and Power BI, owned by the Workbench | Both IDs kept as written and owned by P9 rwb-reporting; no story is raised for them (CG-B-TECH-16-2) | ADR-018, DL44 | DP-17 | Architecture v5 slides 2, 7, 9 and 37; Template and Rules v1 R5.5 DP-17 |
| R-07 | Interfaces | INT-21, INT-22, INT-23, INT-24, INT-25, INT-34, INT-35 and INT-36 owned by the ACE team, the Workbench or the bank platform | The same owners, with the Workbench side named: P4, PLT (RWB-PLT-OBS), P10, S9, S6, P2, P1 and P1 | ADR-013, ADR-019, ADR-023 | DP-05, DP-08, DP-16, DP-20 | Architecture v5 slides 7, 8, 14, 16, 17 and 30 |
| R-08 | Disposition | Every system row had one Owner and no service | Every row carries the owning service of its data path; nine rows name one service per interface because the source row spans several | ADR-013, DL46 | DP-01, DP-05, DP-11 | Ownership Map v1 sheet Services; Architecture v5 slides 13 to 20 |
| R-09 | By route | Six route rows with every count cell empty although the sheet says it is calculated from the Interfaces tab | In, Out, Both and Total calculated from the 36 interfaces: 20 In, 12 Out, 4 Both, 36 Total | D-RCV-60 | none | v3 sheet Interfaces, columns Direction and Route; CG-B-TECH-16-1 |
| R-10 | By service | Sheet not present | New sheet: the 36 interfaces counted per owning service, with the interfaces of each service named | D-RCV-60 | none | The Service column of this version |
| R-11 | Key | 23 key rows (rows 5 to 27) | The same 23 rows plus six: Service, the three readings of the Owner column, the two interface IDs Architecture v5 removes, and the pointer to the Service rules | D-RCV-60 | none | ASM-B-TECH-16-14 |
| R-12 | Service rules | Sheet not present | New sheet: 19 rules, one per path group, with the service and the slide, ADR or ruling behind it | D-RCV-60 | none | Architecture v5 slides 7 to 20, 29, 30 and 41; ADR-010 |
| R-13 | Workbook properties | The author and last-modified-by properties carried a person name | Henka Group and T3 Code / OpenCode / DeepSeek v4.1 Flash; title v4; dated 22 November 2026 | D-RCV-60 | none | Root AGENTS.md rule 4; ASM-B-TECH-16-15 |
| R-14 | All sheets | No other value changed | Every other cell of the 25 disposition rows and the 36 interface rows is unchanged, checked cell by cell | D-RCV-60 | none | ASM-B-TECH-16-14 |
