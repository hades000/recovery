## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION
Recovery Workbench: architecture and build

Executive presentation for the CTO. Henka Group, 28 October 2026
(C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

Architecture decisions taken

2

| Decision | What it means |
|---|---|
| Build on ACE (DT07) | One service, one repository, one front end; reuse of ACE sign-in, IAM, audit, PII and SOC logs |
| Modular monolith (DT08) | Collection, recovery and common modules by folder; boundaries checked at build time |
| Programmatic workflow (DT09) | Case, stage and task state in the database; CMMN 1.1 terms; no Temporal |
| Data through COLLINS (DT12) | Daily batch into the ACE database; file loads for CCMS, SVAF, AMIS, RPS, WIN and GL |
| Trunk based with flags (DT11) | Untested code is not merged; any change can be switched off |
| Document hub (DT06) | The recovery module is the system of record for recovery documents |


## Slide 3

The architecture on one page

3

| Layer | Design |
|---|---|
| Front end | React on Vite with Radix in the ACE front end; recovery screens in the recovery module folder |
| Service | Spring Boot ACE service; recovery module with ten platform and nine stage modules |
| Data | PostgreSQL with the recovery schema: 108 entities, 1,256 fields, 14 data products; Blob storage with a write-once container |
| Rules | 448 rules in ten route sets as DMN decision tables; versioned data |
| Integration | COLLINS batch, file loads, outbox with retry; 144 REST endpoints in OpenAPI 3.1 |
| AI | 12 agents through one orchestrator and tool gateway; 10 bank models from COLLINS; fallback to rules |
| Security | Entra ID, role, capability, scope and masking on every request; decision log hash chained |


## Slide 4

Data

4

|  | Data product | System of record | How it arrives | Freshness |
|---|---|---|---|---|
| DP01 | Account and arrears | Core bank (ALS) | COLLINS daily batch | End of day; in the Workbench the next morning |
| DP02 | Customer and party | SCBPDM and core bank | COLLINS daily batch | End of day; in the Workbench the next morning |
| DP03 | Case and ownership | Recovery Workbench | Held in the Workbench | As it changes |
| DP04 | Treatment and offers | Recovery Workbench; restructure plans in ACE | Held in the Workbench | As it changes |
| DP05 | Contact and promises | EFS before day 90; the Workbench after | COLLINS daily batch from EFS; held in the Workbench | End of day for EFS history; as it changes after |
| DP06 | Collateral and assets | CCMS, SVAF, AMIS, RPS | File load until a batch feed exists | Weekly or monthly today |
| DP07 | Legal events and cases | LIT for court records; the Workbench for instructions | COLLINS daily batch for litigation status; held in the Workbench | End of day for LIT status |


## Slide 5

Integration

5

| Route | What | How often |
|---|---|---|
| In through COLLINS | Accounts, payments, customers, collections history, litigation status, scores | Daily |
| In by file | Collateral, appraisals, assets, repossessions, proofs of delivery, postings | Weekly or monthly |
| Out | Notices to WIN; SMS and LINE through ACE; reporting to the data lake | Daily or as sent |
| Partners | Partner portal through the external gateway (DL03) | As entered |


## Slide 6

Build approach

6

| Item | Approach |
|---|---|
| Squads | Two TechX recovery squads with the ACE team and the collection squad in one repository |
| Flow | Kanban; monthly releases; SIT and UAT one week each |
| Quality | Nine pipeline gates; rule table tests for every row; regression suite on every release |
| AI-assisted development | Coding tool under DL32; AI first-pass review on every pull request |
| Specifications | FSD and TSD per module; Epics 1 and 2 at development detail; Epics 3 to 8 at architecture, API and integration detail |


## Slide 7

Technical decisions needed

7

|  | Decision | Recommended answer |
|---|---|---|
| DL03 | How partners reach the partner portal from outside the bank | Raise the external gateway change in November; partners keep current channels until then |
| DL05 | Who creates the recovery module in ACE | TechX builds in its own package from 2 November; the ACE team applies the boundaries |
| DL06 | Which interfaces need real-time data | Daily batch; same-day triggers named now: EFS hand-over, payment received, legal event |
| DL07 | How the front end is split into modules | One front end with a recovery module folder |
| DL11 | Non-functional target values | ACE values where ACE has them; proposed values for the rest |
| DL12 | Which legacy systems are kept | Keep the systems in the integration inventory, with what the Workbench reads from each |
| DL21 | Which systems carry the case identifier | The Workbench and WIN carry the case number in Epics 1 and 2 |
| DL27 | Storage, backup, legal hold and e-discovery for the document hub | ACE storage pattern with a write-once container and the bank backup |

