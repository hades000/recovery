SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Records retention and archiving

| Item | Detail |
|---|---|
| Document | Recovery Workbench records retention and archiving |
| Version | 3 |
| Date | 22 November 2026 |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | Henka Group |
| Structure | Thai PDPA, bank records policy |
| Source version | 1, 28 October 2026. The metadata table of the source reads version 1 and its date reads 28 October 2026; the source file name reads v2 (CG-B-CTRL-33-1; ASM-B-CTRL-33-1) |
| Delivery model | 19 services, one ACE PostgreSQL schema and one login per service, rwb_<name> (ADR-013, ADR-014) |
| Status | Draft. No approval is recorded for this version (ASM-B-CTRL-33-10) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60 |


# Change log

| Version | Date | Change |
|---|---|---|
| 3 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Retention is now stated per service schema: every row of section 1 names the schema and the service that hold the record, and section 1.1 reads the same periods one schema at a time. The decision log is kept in rwb_decision and no copy goes to a data lake. Destruction is JOB-17 as a Temporal Schedule in rwb-document, acting through the owner of each schema. Sections 1 to 4 keep their headings, their order and their values; sections 1.1, 2.1, 3.1, 4.1, 5, 6 and 7 are added |
| 1 | 28 October 2026 | The proposed retention schedule, where records move, how destruction happens and legal hold (sections 1 to 4). This is the version that version 3 realigns; the metadata table reads 1 while the file name reads v2 (CG-B-CTRL-33-1; ASM-B-CTRL-33-1) |


# 1. Retention schedule, proposed

Periods are proposed until Compliance issues the bank retention schedule for recovery records (DL26). Each period is a reference data value and changes by load.

The periods do not change in this version. What changes is where each record is kept. The single recovery schema becomes one schema per service (ADR-014; DP-01), so every row below now names the schema and the service that hold the record, read from the Microservice Ownership Map v1 and the run ownership file (ASM-B-CTRL-33-13). A record the source lists under two data products is named against both schemas. A record whose data product no table carries is named against the read that supplies it (CG-B-CTRL-33-3; ASM-B-CTRL-33-3). No source document maps a data product to a schema, so each row is read from the owner of the tables that carry it (CG-B-CTRL-33-9; ASM-B-CTRL-33-9).

| Record | Data product | Retention | Archive | Reason | Owning schema and service |
|---|---|---|---|---|---|
| Case record and case history | DP03 | 10 years after the case closes | Archive after 2 years closed | Legal claims and audit | rwb_case (P3 rwb-case) |
| Account, payments and money | DP01, DP13 | 10 years after the case closes | Archive after 2 years closed | Accounting and tax records | rwb_source_data (P1 rwb-source-data) for DP01; rwb_payment (P8 rwb-payment) for DP13 |
| Customer and party | DP02 | 10 years after the last case closes | Archive after 2 years closed | Legal claims | rwb_source_data (P1 rwb-source-data); case_party in rwb_case (P3 rwb-case) |
| Treatments and offers | DP04 | 10 years after the treatment ends | Archive after 2 years | Contract evidence | rwb_treatment (S2 rwb-treatment); report copies dp_treatment and dp_guarantee_claim in rwb_source_data (P1 rwb-source-data) |
| Contact and interaction ledger | DP05 | 5 years after the case closes | Archive after 1 year closed | Conduct review | rwb_source_data (P1 rwb-source-data) |
| Collateral and assets | DP06 | 10 years after disposal | Archive after 2 years | Legal claims | rwb_asset (S5 rwb-asset); valuation_ext in rwb_source_data (P1 rwb-source-data) |
| Legal actions and notices | DP07 | 10 years after the legal action ends | Archive after 2 years | Legal claims | rwb_litigation (S4 rwb-litigation) for legal actions; rwb_comms (P6 rwb-comms) for notices |
| Partner performance | DP08 | 5 years | Archive after 1 year | Contract management | rwb_partner (S9 rwb-partner) |
| Debt sale | DP09 | 10 years after transfer | Archive after 2 years | Legal claims | rwb_debtsale (S6 rwb-debtsale) |
| Legal documents | DP10 | 10 years after the case closes; write-once | Archive after 2 years closed | Legal claims | rwb_document (P5 rwb-document); the files are in the Blob write-once container |
| Other documents | DP10 | 5 years after the case closes | Archive after 1 year closed | Operations | rwb_document (P5 rwb-document) |
| Scores | DP11 | 2 years | Delete | Model monitoring | No Workbench schema; v_ace_score is read through the ACE view contract of rwb_source_data (P1 rwb-source-data) (CG-B-CTRL-33-3; ASM-B-CTRL-33-3) |
| Decision log | DP12 | 10 years after the case closes | Copy kept in the central decision ledger of rwb_decision; the data lake is removed (the source reads: copy kept in the data lake) (CG-B-CTRL-33-2; ASM-B-CTRL-33-2) | Audit and regulatory | rwb_decision (P7 rwb-decision) |
| Reference data versions | DP14 | 10 years after superseded | Archive | Audit: which rule applied | rwb_case (P3 rwb-case) for reference_version and reference_row; rwb_decision (P7 rwb-decision) for rule_package_version and rule_row |
| Access log | None | Per the bank security standard | Archive | Security and audit | rwb_access (P4 rwb-access); the store behind GET /admin/access-log is not in Physical Schema v6 (CG-B-CTRL-33-7; ASM-B-CTRL-33-7) |
| Application logs | None | 90 days | Archive for 1 year | Operations | No Workbench schema; every service writes audit and PII logs to ACE Common and to the SOC, and traces to OpenTelemetry (ASM-B-CTRL-33-14) |


## 1.1 Retention by schema

The same schedule read the other way, one row for each of the 19 services (ADR-013). The retention and the archive rule are the ones of the data-product row above; no period is added or changed. Tables that carry no data-product row in the Logical Data Model v8, such as the loads and operations tables of rwb_source_data and rwb_integration, the reporting tables of rwb_reporting and the agent tables of rwb_agent, have no period in the source and none is invented (CG-B-CTRL-33-4; ASM-B-CTRL-33-4). A schema row acts only on its own schema: no service archives or destroys rows of another service (DP-01).

| Schema | Service and wave | Data-product records held | Retention | Archive |
|---|---|---|---|---|
| rwb_source_data | P1 rwb-source-data, wave 1 | DP01 account and arrears; DP02 customer and party; DP04 report copies of treatments and guarantees; DP05 contact and interaction ledger | 10 years after the case closes (DP01); 10 years after the last case closes (DP02); 10 years after the treatment ends (DP04); 5 years after the case closes (DP05) | Archive after 2 years closed (DP01, DP02) and after 2 years (DP04); after 1 year closed (DP05) |
| rwb_integration | P2 rwb-integration, wave 1 | No data-product record; interface config, outbound items and job catalog only | Not specified in the source documents (CG-B-CTRL-33-4; ASM-B-CTRL-33-4) | Not specified in the source documents (CG-B-CTRL-33-4; ASM-B-CTRL-33-4) |
| rwb_case | P3 rwb-case, wave 1 | DP03 case record and case history; DP14 reference data versions | 10 years after the case closes (DP03); 10 years after superseded (DP14) | Archive after 2 years closed (DP03); archive at supersession (DP14) |
| rwb_access | P4 rwb-access, wave 1 | DP14 reference data versions for roles, delegation limits and masking; access log | 10 years after superseded (DP14); per the bank security standard (access log) | Archive at supersession (DP14); archive (access log) |
| rwb_document | P5 rwb-document, wave 1 | DP10 legal documents and other documents; retention_rule (DP14) and retention_action (DP10) | 10 years after the case closes and write-once (legal documents); 5 years after the case closes (other documents); 10 years after superseded (retention_rule) | Archive after 2 years closed (legal documents) and after 1 year closed (other documents); archive at supersession (retention_rule); Blob archive tier |
| rwb_comms | P6 rwb-comms, wave 1 | DP07 notices; DP14 reference data versions for templates and merge fields | 10 years after the legal action ends (DP07); 10 years after superseded (DP14) | Archive after 2 years (DP07); archive at supersession (DP14) |
| rwb_decision | P7 rwb-decision, wave 1 | DP12 decision log and approvals; DP14 reference data versions for rule packages | 10 years after the case closes (DP12); 10 years after superseded (DP14) | Central ledger entry, kept; archive at supersession (DP14) |
| rwb_payment | P8 rwb-payment, wave 2 | DP13 account, payments and money | 10 years after the case closes (DP13) | Archive after 2 years closed |
| rwb_reporting | P9 rwb-reporting, wave 1 | No data-product record; measures, snapshots and publishes only | Not specified in the source documents (CG-B-CTRL-33-4; ASM-B-CTRL-33-4) | Not specified in the source documents (CG-B-CTRL-33-4; ASM-B-CTRL-33-4) |
| rwb_agent | P10 rwb-agent, wave 1 | No data-product record; agent policies, prompts, runs and evaluations only | Not specified in the source documents (CG-B-CTRL-33-4; ASM-B-CTRL-33-4) | Not specified in the source documents (CG-B-CTRL-33-4; ASM-B-CTRL-33-4) |
| rwb_valuation | S1 rwb-valuation, wave 3 | DP06 collateral and assets, for valuations and the route decision | 10 years after disposal (DP06) | Archive after 2 years |
| rwb_treatment | S2 rwb-treatment, wave 2 | DP04 treatments and offers | 10 years after the treatment ends (DP04) | Archive after 2 years |
| rwb_guarantee | S3 rwb-guarantee, wave 3 | DP04 treatments and offers, for TCG and insurance claims | 10 years after the treatment ends (DP04) | Archive after 2 years |
| rwb_litigation | S4 rwb-litigation, wave 3 | DP07 legal actions and notices | 10 years after the legal action ends (DP07) | Archive after 2 years |
| rwb_asset | S5 rwb-asset, wave 2 | DP06 collateral and assets, for assets taken on, listings and auction rounds | 10 years after disposal (DP06) | Archive after 2 years |
| rwb_debtsale | S6 rwb-debtsale, wave 3 | DP09 debt sale | 10 years after transfer (DP09) | Archive after 2 years |
| rwb_writeoff | S7 rwb-writeoff, wave 4 | DP13 account, payments and money, for the write-off and the recovery after charge-off | 10 years after the case closes (DP13) | Archive after 2 years closed |
| rwb_deviation | S8 rwb-deviation, wave 2 | DP03 case record and case history, for the X1 to X7 deviations | 10 years after the case closes (DP03) | Archive after 2 years closed |
| rwb_partner | S9 rwb-partner, wave 4 | DP08 partner performance | 5 years (DP08) | Archive after 1 year |


# 2. Where records move

| Stage | Where | Access |
|---|---|---|
| Active | ACE database and document storage | By role and scope |
| Archived | Archive tier of storage; database partitions detached to the archive | Compliance and internal audit on request |
| Destroyed | Removed from every store and backup cycle | None; the disposal decision is kept |


## 2.1 The same three stages in the target

The three stages do not change. What changes is the store: the ACE database now holds 19 schemas and 19 logins, one per service, and a record sits in the schema of its owner (ADR-013, ADR-014; DP-01, DP-02). The stage table above, read for the target:

| Stage | Where in the target | Who acts | Access |
|---|---|---|---|
| Active | The owner's schema rwb_<name> in the ACE database; the document files in the Blob write-once container of rwb-document | The owning service, with its own login | By role and scope, through the owner's contract |
| Archived | The archive tier, by schema: the owner's partitions detached to the archive, and the Blob archive tier for the files of rwb-document | The owning service, on the decision of JOB-17 | Compliance and internal audit on request |
| Destroyed | Removed from the owner's schema, from the archive and from the backup cycle; the disposal decision and its certificate stay in rwb_document | The owning service, on the decision of JOB-17 | None; the disposal decision is kept |


- The ACE database holds the 19 schemas and 19 logins, and no service reads or writes another service's tables (ADR-013, ADR-014; DP-01, DP-02).

- Azure Blob holds the document files, in a write-once container for legal types, written through rwb-document only (P5; Architecture v5 slide 16).

- ACE Common holds the audit and PII logs and sends them to the SOC; rwb-access owns the access log (P4; Architecture v5).

- Kafka holds the events of a topic for 7 days and is not a record store (Architecture v5; ADR-015).

- Temporal keeps the history of a closed workflow for 30 days and archives it to Blob (Temporal and Drools Design v1; RWB-E2-039).

# 3. How destruction happens

- The retention job lists records past their period each month.

- Records under a legal hold or with an open case, claim or dispute are excluded.

- Compliance reviews the list and approves disposal or an extension; the decision is recorded.

- Approved records are destroyed and a disposal certificate is kept with counts by type.

## 3.1 The monthly job in the target

JOB-17 stays one monthly job with the four rules above, and it becomes a Temporal Schedule in rwb-document, monthly on the first Sunday (Architecture v5 slide 44; ADR-016). The rules, placed on the services:

| Step | Owner | What happens |
|---|---|---|
| 1. List | P5 rwb-document | JOB-17 runs as a Temporal Schedule in rwb-document and reads retention_rule in rwb_document, the only copy of the retention tables (Ownership Map v1 ruling) |
| 2. Exclude holds | P3 rwb-case, P5 rwb-document | A case under a legal hold or open, and a record with an open claim or dispute, is excluded; the case flag is recovery_case.legal_hold of rwb_case (section 4.1) |
| 3. Approve | Compliance, through P7 rwb-decision | The list is approved as an approval of rwb-decision and the decision is recorded as a decision record |
| 4. Destroy and certify | The owner of each schema, with P5 rwb-document | Each service archives or destroys rows only in its own schema, so P5 asks the owner of the schema over that owner's REST contract, one hop with a 2 s timeout, because no expiry operation or event is in the catalogs (CG-B-CTRL-33-6; ASM-B-CTRL-33-6). P5 writes one retention_action row per document and one DOCRET decision record per archive, and the disposal certificate keeps the counts by class (FSD P5 v3 A2.17) |


- The decision log is never destroyed by the job: retention_rule.table_name excludes decision_log_entry, and JOB-14 checks the hash chain (Physical Schema v6; Architecture v5 slide 44).

- The record class LAKE_COPY of retention_rule has no target once the data lake is removed, and the class is retired with the lake (CG-B-CTRL-33-8; ASM-B-CTRL-33-8).

- Every decision of the job is written through the local decision-record library and published on rwb.decision-record.v1 (DP-03; ADR-022).

- JOB-17 replaces the Quartz scheduler of the source; the monthly cadence and the four steps do not change (ADR-016).

# 4. Legal hold

- Legal counsel places a hold on a case, a party or a document with a reference.

- A hold stops archiving and destruction for as long as it is in place.

- Lifting a hold is recorded; retention resumes from the original dates.

## 4.1 Legal hold in the target

- The hold on a case is recovery_case.legal_hold with status_before_hold, in rwb_case (P3 rwb-case), placed through POST /cases/{caseId}/legal-hold (Ownership Map v1 endpoints; Physical Schema v6).

- A hold on a party or on a document has no field of its own in the target: it is recorded on the case and applied by JOB-17, which excludes the documents of a held case (CG-B-CTRL-33-5; ASM-B-CTRL-33-5).

- The hold is placed by legal counsel, a role and not a person; the hold and its lifting are decision records of rwb-decision (P7 rwb-decision).

- The document hub keeps the write-once container and the bank backup service, with legal hold and e-discovery in its build scope (DL27; P5 rwb-document).

# 5. Change register for this version

| Section or item | Version 1 | Version 3 | Decision or reason |
|---|---|---|---|
| Metadata table | Version 1, Date 28 October 2026 | Version 3, Date 22 November 2026; the source reading stays in the Source version row | Template and Rules R8.1, R8.2 (CG-B-CTRL-33-1; ASM-B-CTRL-33-1) |
| 1, retention table | Record, Data product, Retention, Archive, Reason | A sixth column names the schema and the service; every period and every reason is unchanged | ADR-014, DP-01 (ASM-B-CTRL-33-13) |
| 1, decision log row | Archive: copy kept in the data lake | Archive: copy kept in the central decision ledger of rwb_decision | ADR-018, DP-17 (CG-B-CTRL-33-2; ASM-B-CTRL-33-2) |
| 1, scores row | 2 years, delete | The period is kept; the record is read from v_ace_score and no Workbench table holds it | CG-B-CTRL-33-3; ASM-B-CTRL-33-3 |
| 1.1, retention by schema | None | 19 rows, one per schema, with the periods of section 1 | ADR-013, ADR-014 (ASM-B-CTRL-33-9) |
| 2, where records move | ACE database and document storage; archive tier; destroyed | The same three stages, each read per schema, with the acting owner named | ADR-014, DP-01 |
| 3, how destruction happens | Four steps of a monthly job | The same four steps on JOB-17 as a Temporal Schedule of rwb-document, with the owner of each schema acting | ADR-016, DP-03, DP-10 (CG-B-CTRL-33-6; ASM-B-CTRL-33-6) |
| 4, legal hold | A hold on a case, a party or a document | The case flag of rwb_case, with the party and document hold read from the case | CG-B-CTRL-33-5; ASM-B-CTRL-33-5 |
| 5, 6 and 7 | None | Change register, decisions, open items and out of scope | Template and Rules R8.1 (ASM-B-CTRL-33-11) |


# 6. Decisions

| ID | Decision | Effect here |
|---|---|---|
| D-RCV-60 | Adopt Architecture v5 and realign the documents and the stories | This version, and every owner in it |
| ADR-013 | 19 services inside ACE | Retention is stated per service |
| ADR-014 | Schema and login per service in ACE PostgreSQL | Section 1.1; DP-01, DP-02 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | Events are not a record store; 7-day topic retention |
| ADR-016 | Reusable Temporal layer, Schedules replace Quartz | JOB-17 is a Schedule in rwb-document |
| ADR-018 | No data lake; rwb-reporting read model from events | Decision-log copy and LAKE_COPY (CG-B-CTRL-33-2, CG-B-CTRL-33-8) |
| ADR-021 | Per-service Flyway and migration ownership | Each schema's partitions and DDL belong to its owner |
| ADR-022 | Local decision record plus central ledger | DOCRET entries and the central ledger |
| ADR-023 | Observability per service | Logs leave for ACE Common and the SOC |
| DL26 | Retention and masking come from Compliance | The periods stay proposed and unchanged |
| DL27 | Document hub storage, backup, legal hold and e-discovery | The write-once container and the backup stay |
| DL44 | Adopt Architecture v5 | The 19 services and their schemas |
| DL45 | Service epics plus business-epic tags | Not used by this document |
| DL46 | Soft ownership by team type | Owners here are services, not teams |
| DL47 | Epic 1 preservation rule | No story is changed by this document |
| DL48 | Dates unchanged and tentative | The source date is kept and read as tentative |
| DL49 | Gap and assumption registers | Sections 1 and 5 cite the rows of this version |


# 7. Open items and out of scope

| Open item | Gap | Assumption | Where |
|---|---|---|---|
| The metadata table reads version 1 and the file name reads v2 | CG-B-CTRL-33-1 | ASM-B-CTRL-33-1 | Metadata table |
| The decision log was archived to a data lake | CG-B-CTRL-33-2 | ASM-B-CTRL-33-2 | Section 1, decision log row |
| Scores (DP11) have no owning schema or table | CG-B-CTRL-33-3 | ASM-B-CTRL-33-3 | Section 1, Scores row |
| Tables with no data-product row have no period | CG-B-CTRL-33-4 | ASM-B-CTRL-33-4 | Section 1.1, three rows |
| A hold on a party or a document has no field | CG-B-CTRL-33-5 | ASM-B-CTRL-33-5 | Section 4.1 |
| No expiry operation or event crosses a schema boundary | CG-B-CTRL-33-6 | ASM-B-CTRL-33-6 | Section 3.1, step 4 |
| The bank security standard for the access log is not in the run sources | CG-B-CTRL-33-7 | ASM-B-CTRL-33-7 | Section 1, access log row |
| The record class LAKE_COPY has no target | CG-B-CTRL-33-8 | ASM-B-CTRL-33-8 | Section 3.1 |
| No source maps a data product to a schema | CG-B-CTRL-33-9 | ASM-B-CTRL-33-9 | Section 1, opening paragraph |


Out of scope of this version:

- The periods are not renegotiated: they stay proposed until Compliance issues the bank retention schedule for recovery records (DL26).

- Masking is not changed here. DL26 pairs retention with masking, and the Personal Data Protection Design keeps the masking rules (ASM-B-CTRL-33-15).

- No story, story file, build order or master document is changed by this document; the story masters and the story template of Rules v1 R7 do not apply to a policy document (ASM-B-CTRL-33-15).

- The date of this version is 22 November 2026 and the source date of 28 October 2026 is kept; no release date is named here, and no date is raised as a gap (ASM-B-CTRL-33-12; DL48).

- No issue tracker, wiki, repository or web call is made by this version.
