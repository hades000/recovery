<!-- source: 06 Data/Recovery Workbench Data Migration Approach v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `06 Data/Recovery Workbench Data Migration Approach v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Data migration approach

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench data migration approach |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Henka word rules |

# 1. What moves

| What | Data product | Scope | History | How | When |
|---|---|---|---|---|---|
| Case history from EFS | DP05 | Contact and promise history for accounts at 90 days past due or more | 12 months before day 90 | COLLINS (DL29) | E2 |
| Recovery team spreadsheets | DP03, DP04 | Excel and SharePoint lists of open recovery work | Open items only | File load, then retired (RWB-E1-010, RWB-E1-012) | E1 |
| Hire purchase accounts outside the active inventory | DP01, DP03 | 156,351 accounts at 90 days past due or more | Current position | COLLINS, loaded once as case history | E2 |
| Litigation in progress | DP07 | Lawsuits filed and in hearing | From filing | LIT through COLLINS | E5 |
| Assets held | DP06 | 4,736 NPA properties and repossessed vehicles | From take-on | AMIS and RPS file loads | E3 |
| Restructures in force | DP04 | 173,807 accounts under restructure | Current terms and status | Core bank and ACE | E2 |
| Documents | DP10 | Documents for open cases in shared drives and the mailroom | Open cases only; originals tracked | Bulk intake through OCR | E1 and E2 |
| Partners and open instructions | DP08 | Panel firms and their open work | Open instructions | Partner master load | E4 to E6 |

# 2. Principles

- The systems of record keep their data; the Workbench loads it through COLLINS and file loads as it does every day.

- Only open work and the history a decision needs move; closed history stays in its source.

- Every migrated record carries its source and load date.

- Each migration reconciles to its source before cutover.

- Spreadsheets are retired with a read-only archive once their content is on the case.

# 3. Cases in flight

| State today | On the Workbench |
|---|---|
| Account at 90 days past due with no recovery action | New case, allocated by rule |
| In restructure or settlement | Case with the treatment record and its status |
| In litigation | Case in the litigation stage with the legal action and court dates |
| Asset held | Asset record linked to its case where the case is open |
| In a partner's hands | Case with an open partner instruction |

# 4. Parallel run

Each team runs its spreadsheet and the Workbench side by side for two weeks after its first release. The data steward reconciles daily. The spreadsheet retires when the business lead signs ten clean days.

# 5. Reconciliation

Counts and balances per data product reconcile to the source within the tolerance under DL25. Breaks are listed for the data steward and cleared before cutover.

# 6. Open decisions

| Decision | What is needed |
|---|---|
| DL12 | Which legacy systems are kept |
| DL29 | How much contact history comes from EFS |
