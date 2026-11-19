<!-- source: 02 Business architecture and process/Recovery Workbench Role to System Access Matrix v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Role to System Access Matrix v2.xlsx`  
> **Converted from:** XLSX

## Matrix

| Role to system access |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Each of the 54 roles against 21 systems: R read, W write, RW read and write, a dash for no access. Access to systems other than the Workbench is granted by each system's owner through bank IAM. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Role code | Role name | Class | Recovery Workbench | Partner portal | EFS | Core bank (ALS) | GL | COLLINS | NLEADS | LIT | CCMS | SVAF | AMIS | RPS | WIN | Power BI | Data lake | TCG portal | Aric | HOME.SCB | Field app | NSS and LINE OA | Entra ID and bank IAM |
| RW-CASEOWN | Case owner | Bank user | RW | - | R | R | - | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-TEAMMGR | Team manager | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - | - | - | - | - |
| RW-PHONECOL | Phone collector | Bank user | R | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | R | - |
| RW-FIELDCOL | Field collector | Bank user | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | RW | - | - |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | R | - | RW | R | - | R | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | RW | - | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-COMPLAIN | Complaint officer | Bank user | RW | - | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-FRAUD | Fraud investigator | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | RW | - | - | - | - |
| RW-LITOFF | Litigation officer | Bank user | RW | - | - | - | - | - | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-ENFORCE | Enforcement owner | Bank user | RW | - | - | - | - | - | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-LEGAL | Legal counsel | Bank user | R | - | - | - | - | - | - | R | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-SALEOFF | Sale officer | Bank user | RW | - | - | - | - | - | - | - | - | RW | RW | R | - | - | - | - | - | RW | - | - | - |
| RW-NPAMGR | NPA and asset manager | Bank user | RW | - | - | - | - | - | - | - | - | R | RW | RW | - | - | - | - | - | - | - | - | - |
| RW-DEBTSALE | Debt sale officer | Bank user | RW | RW | - | R | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-WRITEOFF | Write-off team member | Bank user | RW | - | - | R | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-CREDITAD | Credit Administration officer | Bank user | RW | - | - | RW | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-GUARANT | Guarantee officer | Bank user | RW | - | - | R | - | - | - | - | - | - | - | - | - | - | - | RW | - | - | - | - | - |
| RW-AGENCYMG | Partner and agency manager | Bank user | RW | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-CONDUCT | Conduct and QA officer | Bank user | R | - | R | - | - | - | - | - | - | - | - | - | - | R | - | - | - | - | - | - | - |
| RW-CAPACITY | Capacity and workforce planner | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - | - | - | - | - |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - | - | - | - | - |
| RW-HEADLIT | Head of Litigation | Bank user | RW | - | - | - | - | - | - | R | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-HEADNPA | Head of NPA | Bank user | RW | - | - | - | - | - | - | - | - | - | R | R | - | - | - | - | - | - | - | - | - |
| RW-HEADASL | Head of Asset Liquidity | Bank user | RW | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-CREDCOMM | Credit approval committee member | Bank user | R | - | - | - | - | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-WOCOMM | Write-off committee member | Bank user | RW | - | - | R | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-RISK | Risk and model risk officer | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - | - | - | - | - |
| RW-COE | Center of excellence analyst | Bank user | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-DATASTEW | Data steward and data product owner | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | R | R | - | - | - | - | - | - |
| RW-FINANCE | Finance and CFO delegate | Bank user | RW | - | - | R | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-AUDIT | Internal audit | Bank user | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-COMPLY | Compliance and PDPA officer | Bank user | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-PLATADM | Platform administrator | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-REFADM | Reference data administrator | Bank user | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| RW-SECADM | Security administrator | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | RW |
| RW-BIANAL | Reporting and BI analyst | Bank user | RW | - | - | - | - | - | - | - | - | - | - | - | - | RW | R | - | - | - | - | - | - |
| RW-TRIBE | Tribe lead and squad members | Bank user | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PT-AGENCY | Collection agency (OA) user | Partner user | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PT-LAWFIRM | Law firm user | Partner user | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PT-VALUER | Valuer | Partner user | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PT-AUCTION | Auction vendor | Partner user | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PT-BUYER | Debt buyer and AMC | Partner user | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PT-RAMC | RAMC user | Partner user | - | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| PT-LED | Legal Execution Department and court officer | Partner user | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-BORROW | Customer (borrower) | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - |
| CU-GUARANT | Guarantor and co-borrower | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-HEIR | Heir and estate representative | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-BIDDER | Retail asset bidder | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | R | - | - | - |
| SY-CASEWF | Case workflow module | Non-human actor | RW | - | - | - | - | - | - | - | - | - | - | - | W | - | - | - | - | - | - | W | - |
| SY-RULES | Rules component | Non-human actor | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | W | - | - | - | R | R | - | - | R | R | R | R | R | - | - | - | - | - | - | - | - |
| SY-OCR | OCR and extraction pipeline | Non-human actor | RW | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| SY-DECLOG | Decision log writer | Non-human actor | W | - | - | - | - | - | - | - | - | - | - | - | - | - | W | - | - | - | - | - | - |
| SY-AGENT | Agent platform | Non-human actor | R | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |

## Access list

| Every access a role holds |  |  |  |  |
|---|---|---|---|---|
| 114 role and system pairs with access. Use this list to request and review access. |  |  |  |  |
| Role code | Role name | Class | System | Access |
| RW-CASEOWN | Case owner | Bank user | Recovery Workbench | Read and write |
| RW-CASEOWN | Case owner | Bank user | EFS | Read |
| RW-CASEOWN | Case owner | Bank user | Core bank (ALS) | Read |
| RW-CASEOWN | Case owner | Bank user | COLLINS | Read |
| RW-TEAMMGR | Team manager | Bank user | Recovery Workbench | Read and write |
| RW-TEAMMGR | Team manager | Bank user | Power BI | Read |
| RW-PHONECOL | Phone collector | Bank user | Recovery Workbench | Read |
| RW-PHONECOL | Phone collector | Bank user | EFS | Read and write |
| RW-PHONECOL | Phone collector | Bank user | NSS and LINE OA | Read |
| RW-FIELDCOL | Field collector | Bank user | Recovery Workbench | Read |
| RW-FIELDCOL | Field collector | Bank user | Field app | Read and write |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | Recovery Workbench | Read |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | EFS | Read and write |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | Core bank (ALS) | Read |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | COLLINS | Read |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | NLEADS | Read and write |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | Recovery Workbench | Read and write |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | EFS | Read |
| RW-COMPLAIN | Complaint officer | Bank user | Recovery Workbench | Read and write |
| RW-COMPLAIN | Complaint officer | Bank user | EFS | Read |
| RW-FRAUD | Fraud investigator | Bank user | Recovery Workbench | Read and write |
| RW-FRAUD | Fraud investigator | Bank user | Aric | Read and write |
| RW-LITOFF | Litigation officer | Bank user | Recovery Workbench | Read and write |
| RW-LITOFF | Litigation officer | Bank user | LIT | Read and write |
| RW-ENFORCE | Enforcement owner | Bank user | Recovery Workbench | Read and write |
| RW-ENFORCE | Enforcement owner | Bank user | LIT | Read and write |
| RW-LEGAL | Legal counsel | Bank user | Recovery Workbench | Read |
| RW-LEGAL | Legal counsel | Bank user | LIT | Read |
| RW-SALEOFF | Sale officer | Bank user | Recovery Workbench | Read and write |
| RW-SALEOFF | Sale officer | Bank user | SVAF | Read and write |
| RW-SALEOFF | Sale officer | Bank user | AMIS | Read and write |
| RW-SALEOFF | Sale officer | Bank user | RPS | Read |
| RW-SALEOFF | Sale officer | Bank user | HOME.SCB | Read and write |
| RW-NPAMGR | NPA and asset manager | Bank user | Recovery Workbench | Read and write |
| RW-NPAMGR | NPA and asset manager | Bank user | SVAF | Read |
| RW-NPAMGR | NPA and asset manager | Bank user | AMIS | Read and write |
| RW-NPAMGR | NPA and asset manager | Bank user | RPS | Read and write |
| RW-DEBTSALE | Debt sale officer | Bank user | Recovery Workbench | Read and write |
| RW-DEBTSALE | Debt sale officer | Bank user | Partner portal | Read and write |
| RW-DEBTSALE | Debt sale officer | Bank user | Core bank (ALS) | Read |
| RW-DEBTSALE | Debt sale officer | Bank user | GL | Read |
| RW-WRITEOFF | Write-off team member | Bank user | Recovery Workbench | Read and write |
| RW-WRITEOFF | Write-off team member | Bank user | Core bank (ALS) | Read |
| RW-WRITEOFF | Write-off team member | Bank user | GL | Read |
| RW-CREDITAD | Credit Administration officer | Bank user | Recovery Workbench | Read and write |
| RW-CREDITAD | Credit Administration officer | Bank user | Core bank (ALS) | Read and write |
| RW-CREDITAD | Credit Administration officer | Bank user | GL | Read and write |
| RW-GUARANT | Guarantee officer | Bank user | Recovery Workbench | Read and write |
| RW-GUARANT | Guarantee officer | Bank user | Core bank (ALS) | Read |
| RW-GUARANT | Guarantee officer | Bank user | TCG portal | Read and write |
| RW-AGENCYMG | Partner and agency manager | Bank user | Recovery Workbench | Read and write |
| RW-AGENCYMG | Partner and agency manager | Bank user | Partner portal | Read and write |
| RW-CONDUCT | Conduct and QA officer | Bank user | Recovery Workbench | Read |
| RW-CONDUCT | Conduct and QA officer | Bank user | EFS | Read |
| RW-CONDUCT | Conduct and QA officer | Bank user | Power BI | Read |
| RW-CAPACITY | Capacity and workforce planner | Bank user | Recovery Workbench | Read and write |
| RW-CAPACITY | Capacity and workforce planner | Bank user | Power BI | Read |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | Recovery Workbench | Read and write |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | Power BI | Read |
| RW-HEADLIT | Head of Litigation | Bank user | Recovery Workbench | Read and write |
| RW-HEADLIT | Head of Litigation | Bank user | LIT | Read |
| RW-HEADNPA | Head of NPA | Bank user | Recovery Workbench | Read and write |
| RW-HEADNPA | Head of NPA | Bank user | AMIS | Read |
| RW-HEADNPA | Head of NPA | Bank user | RPS | Read |
| RW-HEADASL | Head of Asset Liquidity | Bank user | Recovery Workbench | Read and write |
| RW-HEADASL | Head of Asset Liquidity | Bank user | Partner portal | Read and write |
| RW-CREDCOMM | Credit approval committee member | Bank user | Recovery Workbench | Read |
| RW-CREDCOMM | Credit approval committee member | Bank user | COLLINS | Read |
| RW-WOCOMM | Write-off committee member | Bank user | Recovery Workbench | Read and write |
| RW-WOCOMM | Write-off committee member | Bank user | Core bank (ALS) | Read |
| RW-WOCOMM | Write-off committee member | Bank user | GL | Read |
| RW-RISK | Risk and model risk officer | Bank user | Recovery Workbench | Read and write |
| RW-RISK | Risk and model risk officer | Bank user | Power BI | Read |
| RW-COE | Center of excellence analyst | Bank user | Recovery Workbench | Read |
| RW-DATASTEW | Data steward and data product owner | Bank user | Recovery Workbench | Read and write |
| RW-DATASTEW | Data steward and data product owner | Bank user | Power BI | Read |
| RW-DATASTEW | Data steward and data product owner | Bank user | Data lake | Read |
| RW-FINANCE | Finance and CFO delegate | Bank user | Recovery Workbench | Read and write |
| RW-FINANCE | Finance and CFO delegate | Bank user | Core bank (ALS) | Read |
| RW-FINANCE | Finance and CFO delegate | Bank user | GL | Read |
| RW-AUDIT | Internal audit | Bank user | Recovery Workbench | Read |
| RW-COMPLY | Compliance and PDPA officer | Bank user | Recovery Workbench | Read |
| RW-PLATADM | Platform administrator | Bank user | Recovery Workbench | Read and write |
| RW-REFADM | Reference data administrator | Bank user | Recovery Workbench | Read |
| RW-SECADM | Security administrator | Bank user | Recovery Workbench | Read and write |
| RW-SECADM | Security administrator | Bank user | Entra ID and bank IAM | Read and write |
| RW-BIANAL | Reporting and BI analyst | Bank user | Recovery Workbench | Read and write |
| RW-BIANAL | Reporting and BI analyst | Bank user | Power BI | Read and write |
| RW-BIANAL | Reporting and BI analyst | Bank user | Data lake | Read |
| RW-TRIBE | Tribe lead and squad members | Bank user | Recovery Workbench | Read |
| PT-AGENCY | Collection agency (OA) user | Partner user | Partner portal | Read and write |
| PT-LAWFIRM | Law firm user | Partner user | Partner portal | Read and write |
| PT-VALUER | Valuer | Partner user | Partner portal | Read and write |
| PT-AUCTION | Auction vendor | Partner user | Partner portal | Read and write |
| PT-BUYER | Debt buyer and AMC | Partner user | Partner portal | Read and write |
| PT-RAMC | RAMC user | Partner user | Partner portal | Read and write |
| CU-BORROW | Customer (borrower) | Customer party | HOME.SCB | Read |
| CU-BIDDER | Retail asset bidder | Customer party | HOME.SCB | Read |
| SY-CASEWF | Case workflow module | Non-human actor | Recovery Workbench | Read and write |
| SY-CASEWF | Case workflow module | Non-human actor | WIN | Write |
| SY-CASEWF | Case workflow module | Non-human actor | NSS and LINE OA | Write |
| SY-RULES | Rules component | Non-human actor | Recovery Workbench | Read and write |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | Recovery Workbench | Write |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | GL | Read |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | COLLINS | Read |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | CCMS | Read |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | SVAF | Read |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | AMIS | Read |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | RPS | Read |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | WIN | Read |
| SY-OCR | OCR and extraction pipeline | Non-human actor | Recovery Workbench | Read and write |
| SY-DECLOG | Decision log writer | Non-human actor | Recovery Workbench | Write |
| SY-DECLOG | Decision log writer | Non-human actor | Data lake | Write |
| SY-AGENT | Agent platform | Non-human actor | Recovery Workbench | Read |

## Systems

| Systems and who grants access |  |  |
|---|---|---|
| Who approves access to each system, and how many roles hold access. |  |  |
| System | Grants access | Roles with access |
| Recovery Workbench | Application owner (DL02) | 43 |
| Partner portal | Application owner (DL02) | 9 |
| EFS | Collections system owner | 6 |
| Core bank (ALS) | Core banking owner | 8 |
| GL | Finance systems owner | 6 |
| COLLINS | Data and analytics owner | 4 |
| NLEADS | Credit systems owner | 1 |
| LIT | Legal systems owner | 4 |
| CCMS | Collateral systems owner | 1 |
| SVAF | Valuation systems owner | 3 |
| AMIS | NPA systems owner | 4 |
| RPS | Repossession systems owner | 4 |
| WIN | Document services owner | 2 |
| Power BI | Data and analytics owner | 7 |
| Data lake | Data and analytics owner | 3 |
| TCG portal | Guarantee officer (external portal) | 1 |
| Aric | Fraud systems owner | 1 |
| HOME.SCB | Digital channels owner | 3 |
| Field app | Collections system owner | 1 |
| NSS and LINE OA | Digital channels owner | 2 |
| Entra ID and bank IAM | SCB IT security | 1 |

## Key

| Key |  |  |
|---|---|---|
| What each term means. |  |  |
| Item | Term | Meaning |
| Access | R | Read: view records; no change |
| Access | W | Write: create or send records; no view (interfaces only) |
| Access | RW | Read and write |
| Access | - | No access |
| Standard | NIST RBAC | Access follows the role; a person holds roles, never direct rights |
| Note | Customer parties | Customers have no Workbench sign-in; they reach offers and listings through bank channels |
| Note | Non-human actors | Service identities with managed credentials; no person signs in as them |
