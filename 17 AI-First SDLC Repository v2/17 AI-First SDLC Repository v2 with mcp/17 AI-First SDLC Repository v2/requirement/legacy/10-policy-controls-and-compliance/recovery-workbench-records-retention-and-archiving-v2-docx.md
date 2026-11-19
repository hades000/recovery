<!-- source: 10 Policy, controls and compliance/Recovery Workbench Records Retention and Archiving v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `10 Policy, controls and compliance/Recovery Workbench Records Retention and Archiving v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Records retention and archiving

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench records retention and archiving |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Thai PDPA, bank records policy |

# 1. Retention schedule, proposed

Periods are proposed until Compliance issues the bank retention schedule for recovery records (DL26). Each period is a reference data value and changes by load.

| Record | Data product | Retention | Archive | Reason |
|---|---|---|---|---|
| Case record and case history | DP03 | 10 years after the case closes | Archive after 2 years closed | Legal claims and audit |
| Account, payments and money | DP01, DP13 | 10 years after the case closes | Archive after 2 years closed | Accounting and tax records |
| Customer and party | DP02 | 10 years after the last case closes | Archive after 2 years closed | Legal claims |
| Treatments and offers | DP04 | 10 years after the treatment ends | Archive after 2 years | Contract evidence |
| Contact and interaction ledger | DP05 | 5 years after the case closes | Archive after 1 year closed | Conduct review |
| Collateral and assets | DP06 | 10 years after disposal | Archive after 2 years | Legal claims |
| Legal actions and notices | DP07 | 10 years after the legal action ends | Archive after 2 years | Legal claims |
| Partner performance | DP08 | 5 years | Archive after 1 year | Contract management |
| Debt sale | DP09 | 10 years after transfer | Archive after 2 years | Legal claims |
| Legal documents | DP10 | 10 years after the case closes; write-once | Archive after 2 years closed | Legal claims |
| Other documents | DP10 | 5 years after the case closes | Archive after 1 year closed | Operations |
| Scores | DP11 | 2 years | Delete | Model monitoring |
| Decision log | DP12 | 10 years after the case closes | Copy kept in the data lake | Audit and regulatory |
| Reference data versions | DP14 | 10 years after superseded | Archive | Audit: which rule applied |
| Access log | None | Per the bank security standard | Archive | Security and audit |
| Application logs | None | 90 days | Archive for 1 year | Operations |

# 2. Where records move

| Stage | Where | Access |
|---|---|---|
| Active | ACE database and document storage | By role and scope |
| Archived | Archive tier of storage; database partitions detached to the archive | Compliance and internal audit on request |
| Destroyed | Removed from every store and backup cycle | None; the disposal decision is kept |

# 3. How destruction happens

- The retention job lists records past their period each month.

- Records under a legal hold or with an open case, claim or dispute are excluded.

- Compliance reviews the list and approves disposal or an extension; the decision is recorded.

- Approved records are destroyed and a disposal certificate is kept with counts by type.

# 4. Legal hold

- Legal counsel places a hold on a case, a party or a document with a reference.

- A hold stops archiving and destruction for as long as it is in place.

- Lifting a hold is recorded; retention resumes from the original dates.
