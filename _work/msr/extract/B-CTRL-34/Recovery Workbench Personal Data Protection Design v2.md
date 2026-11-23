Recovery Workbench

Personal data protection design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench personal data protection design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Thai Personal Data Protection Act B.E. 2562 |


# 1. What personal data is held

| Category | Examples | Classification |
|---|---|---|
| Direct identifier | Name, tokenized national ID, date of birth, contact points, interaction summaries, extracted document fields | Restricted |
| Sensitive | Vulnerable, deceased and bankruptcy flags | Restricted |
| Indirect identifier | Account, contract, case, lawsuit and title deed numbers | Confidential |
| Customer data | Balances, arrears, treatments, legal actions, assets | Confidential |
| Staff identifier | Users who act on cases; partner users | Internal |


The field-level inventory is the data classification and personal data inventory workbook.

# 2. Lawful basis

| Processing | Basis, proposed | Section |
|---|---|---|
| Recovering the debt under the loan contract | Contract | 24(3) |
| Statutory notices, regulatory reporting, court filings | Legal obligation | 24(6) |
| Sensitive flags: death, bankruptcy, vulnerability | Establishment, exercise or defense of legal claims; explicit consent where it applies | 26(4) |
| Contact on optional channels such as LINE | Consent | 19 |
| Fraud prevention and monitoring | Legitimate interest | 24(5) |
| Staff and partner user data | Employment and contract; legitimate interest | 24 |


Compliance confirms the bases (DL26).

# 3. Consent

- Consent state is held per contact point and channel (contact_point.consent_status).

- Withdrawal removes the channel from the contact plan at once; statutory notices continue (R-UNI-10).

- Consent comes from the bank's consent records through COLLINS; the Workbench does not collect new consent.

# 4. Minimization and masking

- National ID and passport numbers are tokenized at load; the clear value is not stored.

- Each role has a masking profile; fields are masked unless the role may see them.

- Each screen and each agent receives only the fields it needs.

- Debt sale tapes carry only the fields the sale terms allow and pass a masking check.

# 5. Access

- Access by role, capability area and scope; out of scope records are not returned.

- Every read of a personal field is logged through PII Kafka.

- Access is reviewed every six months by the role owners.

# 6. Retention

Retention is set per data product and document type in the records retention and archiving schedule. A legal hold overrides retention. Expired data is disposed of by a recorded decision.

# 7. Data subject rights

| Right | Path | Time |
|---|---|---|
| Access | Request through the bank's PDPA process; Compliance retrieves the case data | Within 30 days |
| Correction | Corrected in the system of record; the next load updates the Workbench | Within 30 days |
| Erasure or restriction | Assessed against the legal claims exemption; automated processing held while assessed (R-UNI-11) | Within 30 days |
| Objection | Assessed by Compliance | Within 30 days |


# 8. Sharing outside the bank

| Recipient | What | Safeguard |
|---|---|---|
| Law firms, agencies, valuers, auction vendors | The data the instruction needs | Contract with data protection terms; firm scope in the partner portal |
| Debt buyers and AMCs | Masked data tape before award; full data after transfer | Non-disclosure agreement; masking check |
| Courts and the Legal Execution Department | Filings | Legal obligation |
| Cross-border | None planned; data stays in the SCB Azure tenant, Southeast Asia | Bank position to confirm |


# 9. Breach

A suspected breach is an incident to SCB security operations. Compliance assesses it and notifies the regulator within 72 hours where the Act requires, and the people affected where the risk is high.

# 10. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL26 | Retention and masking | Proposed classes and profiles |
| DL33 | Model endpoint location | Inside the SCB tenant; no cross-border transfer |

