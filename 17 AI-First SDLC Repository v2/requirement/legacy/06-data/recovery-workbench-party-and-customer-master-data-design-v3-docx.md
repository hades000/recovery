<!-- source: 06 Data/Recovery Workbench Party and Customer Master Data Design v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `06 Data/Recovery Workbench Party and Customer Master Data Design v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Party and customer master data design

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench party and customer master data design |
| Version | 3 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29148, bank TSD section T3 |
| Decision | D-RCV-35: ACE holds the source data, the Workbench reads it through recovery.v_ace_* views |

# 1. The design on one page

| Element | Design |
|---|---|
| Golden source | The ACE database. ACE ingests the customer, contact and account facts from SCBPDM and the core bank (DL20, as amended by D-RCV-35). The Workbench loads nothing. |
| Key | The ACE person_key. cif_no in v_ace_customer carries the same customer number, so a CIF match is a person_key match. |
| In the Workbench | No local party table and no local contact_point table. A party is the ACE customer and its ca_relation rows, read through v_ace_customer, v_ace_ca_relation and v_ace_contact, plus one recovery.party_ext row for the Workbench flags. |
| Identity matching | Run in ACE ingestion under M1 to M4. M5, the partner tax ID match, runs in the Workbench partner master. The Workbench consumes the surviving person_key and never re-masters, re-matches or merges a person. |
| Partners | Partner master held in the Workbench; one row per firm, keyed by partner_code. A partner firm is a Workbench record, not an ACE customer. |
| Duplicates | Decided before the row reaches the Workbench. A suspected duplicate is raised with the ACE data steward; the Workbench has no merge function. |
| Identity number | identification_number stays in ACE in clear. v_ace_customer returns id_no_masked and id_no_last4; no token is created at load because there is no load. |

# 2. Parties

| Party | Identified by | Source |
|---|---|---|
| Borrower | person_key, with cif_no from v_ace_customer; the account link from v_ace_ca_relation | ACE, ingested from SCBPDM and the core bank |
| Co-borrower and guarantor | person_key through v_ace_ca_relation, with relation_type, amount_of_guarantee and date_of_guarantee | ACE, ingested from SCBPDM and the core bank |
| Heir and estate representative | Named on the case in the document and decision log; linked as a case party by person_key only where ACE holds the person | Workbench documents; ACE where the person is a customer |
| Juristic person | person_key, with id_type and the masked registration number from v_ace_customer | ACE, ingested from SCBPDM |
| Partner firm | partner_code; tax ID | Workbench partner master |

No row in this table creates a person. A party that ACE does not hold is not a party in the Workbench: an heir or an estate representative is named in the case documents and the decision log, and is linked as a case party only when ACE holds them as a customer. The Workbench never adds a person to the customer master to make a case work.

# 3. Matching rules

M1 to M4 are ACE ingestion rules; M5 matches partner firms and runs in the Workbench partner master. M1 to M4 run before a customer row reaches the Workbench, and the outcome is a single person_key. The Workbench does not match, merge or re-master a person: it reads the key and links its own records to it. A duplicate that survives into the Workbench is raised with the ACE data steward and corrected in ACE, not in the recovery schema.

M1 - CIF equal. ACE treats the records as one customer and publishes one person_key. The Workbench reads that key.

M2 - Identity type and number equal. ACE treats the records as one customer, using identification_number as it holds it. The Workbench sees the masked value only.

M3 - Name and date of birth equal, with no CIF and no identity number. ACE raises a possible duplicate and the ACE data steward decides. It is never an automatic merge, and the Workbench never merges.

M4 - Company registration number equal. ACE treats the records as one juristic person.

M5 - Partner tax ID equal. Run in the Workbench partner master, not in ACE ingestion: a partner firm is a Workbench record, not an ACE customer. The Workbench treats the records as one firm and the partner and agency manager confirms the panel entry.

Cases. A case is never merged by the party match; duplicate cases follow R-UNI-17.

# 4. Survivorship

| Attribute | Wins |
|---|---|
| Name, identity, date of birth | ACE, ingested from SCBPDM. Read from v_ace_customer; no Workbench copy and no override |
| Contact points | ACE phone, email and address, read through v_ace_contact. All three are shown; the most recently verified is preferred, and the verification is held in contact_point_ext |
| Vulnerable, deceased, bankruptcy, fraud | recovery.party_ext, set in the Workbench by the handler with the evidence document. deceased_override wins over the ACE deceased flag, and the ACE value is shown beside it |
| Consent | recovery.contact_point_ext, recorded against contact_key and contact_type. ACE holds no consent column |

# 5. Identity numbers and masking

The clear identity number never leaves ACE, and no token is created in its place. The view is the only read path, and the grant on the view, E1-037 and the audit log are the control.

| Value | Where it lives | What the Workbench sees |
|---|---|---|
| identification_number | public.customer, in clear | id_no_masked, all but the last four replaced, and id_no_last4, both from v_ace_customer. No Workbench table holds the clear value |
| id_no_token | Removed | There is no tokenization at load because there is no load. E1-037 role masking replaces the token as the display control |
| phone_number, email, address | public.phone, email and address, in clear | contact_value in v_ace_contact, in full, for notices and calls; contact_value_masked for display. Every read is audited |
| Masking control | The SELECT grant on v_ace_customer, E1-037 at the API, the audit log | The view mask alone is not the control; the ACE DB Alignment Change Register records this as risk R5 |

A Workbench column, report extract or lake table never carries identification_number. Where a report needs an identifier it uses id_no_masked; where a case must prove identity it cites the document in the document hub.

# 6. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL20 | Source of customer facts | ACE, which ingests them from SCBPDM and the core bank. Closed by D-RCV-35 |
| DL43 | Does the ACE team accept the RWB-ACE-001 scope and dates? | Open. If the scope and dates are accepted, party_type, id_type and segment appear in v_ace_customer (Section B, after RWB-ACE-001) when RWB-ACE-001 lands; until then they read blank and the rest of the design is unaffected |
