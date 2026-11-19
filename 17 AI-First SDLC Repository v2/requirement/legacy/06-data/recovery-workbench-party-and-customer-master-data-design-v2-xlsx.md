<!-- source: 06 Data/Recovery Workbench Party and Customer Master Data Design v2.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Party and Customer Master Data Design v2.xlsx`  
> **Converted from:** XLSX

## Party fields

| Party master fields |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| The fields that identify and describe a party, with their source. |  |  |  |  |  |  |
| Entity | Field | Data type | Physical type | Source | Source field | Meaning |
| case_party | id | TEXT | uuid | Workbench | None | Record identifier of the case party link |
| case_party | case_id | CROSS_REF | uuid | Workbench | None | The recovery_case this record belongs to |
| case_party | party_id | CROSS_REF | uuid | Workbench | None | The party this record belongs to |
| case_party | party_role | LOV | varchar(20) | Workbench | None | Borrower, co-borrower, guarantor, authorized signatory, heir |
| case_party | role_from | DATE | date | Workbench | None | Date the role starts |
| case_party | role_to | DATE | date | Workbench | None | Date the role ends |
| party | id | TEXT | uuid | Workbench | None | Record identifier of the party |
| party | cif_no | TEXT | varchar(20) | SCBPDM via COLLINS | CIF | Customer number in the bank |
| party | party_type | LOV | varchar(15) | SCBPDM via COLLINS | None | Individual or juristic person |
| party | first_name | TEXT | varchar(100) | SCBPDM via COLLINS | None | First name or company name |
| party | last_name | TEXT | varchar(100) | SCBPDM via COLLINS | None | Last name |
| party | id_type | LOV | varchar(20) | SCBPDM via COLLINS | None | Thai national ID, passport, company registration |
| party | id_no_token | TEXT | varchar(64) | SCBPDM via COLLINS | None | Tokenized identity number. The clear value is never stored in the Workbench |
| party | date_of_birth | DATE | date | SCBPDM via COLLINS | None | Date of birth |
| party | segment | LOV | varchar(20) | SCBPDM via COLLINS | Segment | Retail, SSME, corporate |
| party | vulnerable_flag | BOOLEAN | boolean | Workbench | None | Vulnerable customer or hardship confirmed |
| party | deceased_flag | BOOLEAN | boolean | Workbench | None | Death confirmed |
| party | bankruptcy_flag | BOOLEAN | boolean | Workbench | None | Bankruptcy or receivership confirmed |
| contact_point | id | TEXT | uuid | Workbench | None | Record identifier of the contact point |
| contact_point | party_id | CROSS_REF | uuid | Workbench | None | The party this record belongs to |
| contact_point | channel | LOV | varchar(15) | Workbench | None | Mobile, home phone, work phone, LINE, email, postal address |
| contact_point | value_token | TEXT | varchar(256) | SCBPDM via COLLINS | None | The number, handle or address, stored masked |
| contact_point | source | LOV | varchar(15) | Workbench | None | Bank record, field visit, agency, bureau trace, customer |
| contact_point | consent_status | LOV | varchar(12) | Workbench | None | Given, withdrawn, unknown |
| contact_point | verified_at | DATE | timestamptz | Workbench | None | When it last reached the right party |
| contact_point | failed_count | NUMBER | integer | Workbench | None | Failed attempts since last success |
| partner | id | TEXT | uuid | Workbench | None | Record identifier of the partner |
| partner | partner_code | TEXT | varchar(20) | Workbench | OACode | Partner code |
| partner | partner_name | TEXT | varchar(160) | Workbench | REPOSS_NAME / Investor | Registered name |
| partner | partner_type | LOV | varchar(15) | Workbench | None | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC |
| partner | panel_status | LOV | varchar(12) | Workbench | None | Active, on notice, suspended, exited |
| partner | contract_end | DATE | date | Workbench | None | Contract end date |
| partner | score | NUMBER | numeric(5,2) | Workbench | None | Latest scorecard result |

## Match rules

| Match rules |  |  |  |
|---|---|---|---|
| Applied at load and when a party is entered. |  |  |  |
| Rule | Condition | Result | Action |
| M1 | CIF number equal | Same party | Automatic |
| M2 | Identity type and token equal | Same party | Automatic |
| M3 | Name and date of birth equal, no CIF or token | Possible duplicate | Data steward decides |
| M4 | Company registration equal | Same juristic person | Automatic |
| M5 | Partner tax ID equal | Same partner firm | Partner and agency manager confirms |
