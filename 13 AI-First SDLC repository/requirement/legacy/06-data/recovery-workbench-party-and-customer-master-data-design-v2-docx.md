<!-- source: 06 Data/Recovery Workbench Party and Customer Master Data Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `06 Data/Recovery Workbench Party and Customer Master Data Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Party and customer master data design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench party and customer master data design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29148, bank TSD section T3 |

# 1. The design on one page

| Element | Design |
|---|---|
| Golden source | SCBPDM and the core bank, through the COLLINS daily load (DL20) |
| Key | CIF number for customers; tokenized national ID, passport or company registration as the match key |
| In the Workbench | One party row per person or company; case_party links a party to a case with its role |
| Partners | Partner master held in the Workbench; one row per firm |
| Duplicates | Matched on CIF, then on the identity token; possible duplicates go to the data steward |

# 2. Parties

| Party | Identified by | Source |
|---|---|---|
| Borrower | CIF number; identity token | SCBPDM through COLLINS |
| Co-borrower and guarantor | CIF number where they hold one; identity token | SCBPDM and the core bank |
| Heir and estate representative | Identity token; name and relationship | Entered in the Workbench from documents |
| Juristic person | Company registration number; CIF | SCBPDM |
| Partner firm | Partner code; tax ID | Workbench partner master |

# 3. Matching rules

- A party with a CIF number is matched on CIF.

- A party without a CIF is matched on identity type and token.

- A match on name and date of birth alone is a possible duplicate, never an automatic merge.

- Possible duplicates go to the data steward's list; a confirmed merge keeps both source keys and is logged.

- A case is never merged by the party match; duplicate cases follow R-UNI-17.

# 4. Survivorship

| Attribute | Wins |
|---|---|
| Name, identity, date of birth | SCBPDM |
| Contact points | The most recently verified; source recorded on each contact point |
| Vulnerable, deceased, bankruptcy flags | Set in the Workbench by the handler, with the evidence document |
| Consent | The bank consent records through COLLINS |

# 5. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL20 | Source of customer facts | SCBPDM and the core bank through COLLINS |
