SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Test data plan

Version 4, 22 November 2026. The version 3 text is dated 15 November 2026.

| Item | Detail |
|---|---|
| Document | Recovery Workbench test data plan |
| Version | 4 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119 |
| Decision | D-RCV-60 microservice realignment; ADR-014 schema and login per service; ADR-020 contract-first REST; ADR-021 per-service Flyway; DL44 |
| Supersedes | Version 3, 15 November 2026 (D-RCV-35 (U1, U4); ADR-010; DL43) |
| Status | Draft |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Change log | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |


# 1. Sources

Every environment below SIT is seeded from the ACE schema and from the 19 Recovery schemas `rwb_<service>`. No environment holds a copy of a source table or a load table, because neither exists under D-RCV-60 (DL44). SIT and UAT read source data through the 30 `recovery.v_ace_*` views, and one login has SELECT on them: `rwb_source_data` (ADR-010; Architecture v5 slide 29; DP-05). No Recovery schema holds a copy of a source row, and no service reads another service's tables (DP-01).

A test that needs another service's data does not join to it. Below SIT it calls the fake of that service's published contract; in SIT and UAT it calls the service itself (Template and Rules R5.4, class C and class I). That is what makes 19 schemas testable as one Workbench.

| Environment | Data | Source | Personal data |
|---|---|---|---|
| DEV | Synthetic ACE-shaped rows and synthetic rows in each of the 19 `rwb_*` schemas, rebuilt from the DDL and the data dictionary | RWB-E1-065 SandboxGenerator, seed 20261128; the per-service Flyway baseline of each schema (DP-15; ADR-021) | None |
| SIT | Masked copy of the ACE tables, ingested by ACE from the SIT sources, plus scripted cases in each schema and the 19 contract fakes | ACE ingestion; PII service (RWB-TE-004); rwb-source-data (P1) as the only reader of the 30 views | Masked |
| UAT | Masked ACE copy plus scripted cases and the contract fakes | PII service; testers | Masked |
| Performance | Masked ACE copy scaled to the 2027 volume | PII service with scaling | Masked |


# 2. What the sandbox seeds

The sandbox is the only test data set below SIT. RWB-E1-065 builds it from the same DDL as SIT: ACE Schema PostgreSQL v1.sql for the 22 Tier 1 tables, the RWB-ACE-001 DDL for the 14 Tier 2 tables, then the `V0001` baseline of each of the 19 schemas for the 92 recovery tables and the four extension tables, and `recovery_views.sql` for the 16 Section A views and the 14 Section B views. It seeds rows by reading `sys_objects`, `sys_fields` and `lov_value`, so a schema change reaches the sandbox with no generator edit.

Each service seeds its own schema and nothing else (CG-B-TESTDOC-41-6; ASM-B-TESTDOC-41-6). A row that belongs to another service is reached through that service's contract or its fake, so the seed links cases across schemas by `case_id`, `account_id` and `party_key`, never by a foreign key (DP-01, DP-11). The Ownership Map sheet Tables assigns all 93 tables; the source count of 92 recovery tables and the map count of 93 tables are not reconciled (CG-B-TESTDOC-41-1; ASM-B-TESTDOC-41-1).

| Object group | What is seeded |
|---|---|
| Tier 1 ACE tables (22) | One or more rows in account, payment, customer, phone, email, address, ca_relation, aa_relation, collateral, asset, efs_action, efs_action_code, efs_assignment, bucket_log_snapshot, product, branch, bot_holiday, iam_user, ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation and ai_recommended_plan. 184,500 account rows carry the ALS business shape; 28,140 of them sit at 90 days past due or more, with accounts at 89 and at 90. |
| Tier 2 ACE tables (14) | ace_batch_run holds one row per source and business date, with COMPLETED, FAILED and LATE rows; valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product, credit_decision, esign_request and iam_group each hold rows for every Workbench read. The 12 new columns on account, customer and efs_action are filled. Behind DL43: until the DDL lands, the Section B views and their features stay behind their flags. |
| Recovery tables (92) | 2,812 cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME, plus 10 cases for each exception shape; their accounts, parties, contact points, collateral, valuations, payments, interactions and documents are linked by business key. The case rows go to rwb_case (P3), the treatments to rwb_treatment (S2), the proceeds to rwb_payment (P8), the notices to rwb_comms (P6), the documents to rwb_document (P5), the decisions to rwb_decision (P7) and the interactions to rwb_source_data (P1); the link between them stays a plain key. |
| Extension tables (4) | party_ext, contact_point_ext, account_ext and valuation_ext, 49 columns in all, one row per ACE business key where a Workbench decision exists. All four are in rwb_source_data (P1). |
| Views (30) | The 16 Section A and 14 Section B `recovery.v_ace_*` views; each returns at least one row; each has one sys_objects row and one sys_fields row per column. The views stay in schema `recovery`, read only, and only the `rwb_source_data` login holds SELECT on them. |
| Removed tables (20) | None. loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory and tracker_row do not exist in any Recovery schema and are neither seeded nor read. |
| Service schemas (19) | One schema `rwb_<name>` and one login per service, created and seeded by that service's own baseline. The boundary test in every build fails on any cross-schema reference, view or foreign key (Architecture v5 slide 29). |
| Platform library objects (6) | outbox_event, outbox_delivery, processed_event and idempotency_key exist in all 19 schemas, because DP-09 and Architecture v5 slide 20 make the outbox and inbox part of every service schema. feature_flag and feature_flag_change exist once, in rwb_integration, which serves the feature-flag admin API. |
| Contract fakes (20) | One fake per service and one for gateway-bff, each generated from the provider's published OpenAPI 3.1, AsyncAPI 3.0 or activity contract jar (section 3.1). The fakes hold the same business keys as the seed, so a case, account or party ID means the same row on both sides of a contract. |


There is no copy table and no load table in the sandbox. A test that needs a source value reads it through its view; the expected value comes from the ACE-shaped row, not from a Workbench copy. A test that needs another service's value reads it through that service's contract or its fake.

## 2.1 Rows per schema

The table gives the synthetic rows each schema must hold, and the owner of that schema in the Ownership Map. Row counts are the count of cases and their linked rows, not a second set of cases: the 2,812 cases are seeded once, in rwb_case, and every other schema holds the rows of those cases that its own service owns.

| Code | Service | Schema | Tables owned | Synthetic rows the schema holds |
|---|---|---|---|---|
| P1 | rwb-source-data | rwb_source_data | 18 | The four extension tables, interaction, case_list_row as the daily case-list projection, the four data-product tables with data_product_access and data_product_load, efs_ledger_outcome, dp_treatment, dp_guarantee_claim, reconciliation_result, the dictionary (sys_objects, sys_fields, sys_field_version) and lake_copy_watermark, which is kept with no target (DP-17). |
| P2 | rwb-integration | rwb_integration | 3 | interface_config, job_catalog and outbound_item at every file status, with a file delivered, a file failed and a file whose arrival is missing. It is the only schema that holds feature_flag and feature_flag_change. |
| P3 | rwb-case | rwb_case | 15 | The 2,812 cases (recovery_case), with case_account, case_party, assignment, task, timer, queue, queue_member and queue_measure; the case_entry_exclusion rows; the parameters and reference data (parameter_catalog, parameter_value, reference_row, reference_version, lov_value) at one version per business date. |
| P4 | rwb-access | rwb_access | 5 | role, permission and role_conflict for every role; delegation_limit at each level and amount boundary; masking_rule at the approved masking version. |
| P5 | rwb-document | rwb_document | 12 | The labeled sample of 180 documents across the six types, with document, document_text, document_field, document_type, the checklist items and case_document_check; document_custody, document_intake and document_hub_parameter; retention_rule and retention_action; signature_request at each state. The file bytes sit in Blob with WORM, not in the schema. |
| P6 | rwb-comms | rwb_comms | 3 | notice, template and merge_field for every template version and every notice status, including a notice with proof of delivery and a notice that failed. |
| P7 | rwb-decision | rwb_decision | 6 | approval at each level and amount boundary, with approve, refuse and return; decision_log_entry for every recorded decision; rule_package, rule_package_version, rule_row and rule_test_case, with at least 50 scenarios for each package (rules.testcases.min=50). |
| P8 | rwb-payment | rwb_payment | 1 | proceeds for every payment and every proceeds match, including a payment in v_ace_payment with no proceeds and a proceeds match that arrives twice. |
| P9 | rwb-reporting | rwb_reporting | 3 | measure_definition, measure_snapshot and measure_publish for each measure and business date, projected from the events of the other services, with a business date that has a late source. |
| P10 | rwb-agent | rwb_agent | 8 | agent_policy, agent_prompt, agent_run, agent_alert, agent_evaluation, agent_evaluation_run, agent_feedback and agent_sample; a run that answers inside 60 s and a run that falls back to the rule result. |
| S1 | rwb-valuation | rwb_valuation | 0 | No table in the Ownership Map sheet Tables (CG-B-TESTDOC-41-2; ASM-B-TESTDOC-41-2). The route decision reads valuation_ext through the rwb-source-data contract, and each RouteDecided outcome is recorded as a decision record in rwb_decision (P7); the seed therefore holds the inputs in rwb_source_data and the outcome in rwb_decision. |
| S2 | rwb-treatment | rwb_treatment | 1 | treatment for every stage of the TreatmentWorkflow, at each approval state and each plan timer, with a treatment that closes and a plan that is missed. |
| S3 | rwb-guarantee | rwb_guarantee | 1 | guarantee_claim at each claim state, filed, settled and refused, with the TCG and insurance claim of the same case. |
| S4 | rwb-litigation | rwb_litigation | 2 | legal_action and hearing at each step, with a judgment recorded and an auction result that comes back after the hearing. |
| S5 | rwb-asset | rwb_asset | 2 | asset_sale and listing at each auction round, with an asset that sells and an asset that does not sell. |
| S6 | rwb-debtsale | rwb_debtsale | 2 | debt_sale_lot and debt_sale_account for each lot and each buyer, with a lot awarded and a lot withdrawn. |
| S7 | rwb-writeoff | rwb_writeoff | 1 | write_off at each scan and each committee decision, with a write-off approved and a write-off refused. |
| S8 | rwb-deviation | rwb_deviation | 1 | deviation for each of X1 to X7, at pause, handling and return, with a deviation raised and a deviation cleared. |
| S9 | rwb-partner | rwb_partner | 3 | partner of each partner type, partner_user for each role, and partner_instruction in every status, with an instruction accepted, invoiced and resulted. |
| PLT | platform library | all 19 schemas | 6 | outbox_event, outbox_delivery, processed_event and idempotency_key in every schema, each seeded with a published event, a retried delivery and a duplicate event, so the inbox dedupe and the outbox relay (JOB-11) are testable; feature_flag and feature_flag_change once, in rwb_integration. |


# 3. What each test needs

| Test | Data |
|---|---|
| Allocation | Cases for every product group, region and exposure band; owners at and below the capacity limit and one owner above it. The cases are recovery_case and the limit is queue_measure, both in rwb_case (P3). |
| Routing rules | One case per rule row in its from state, with its condition true and false. The rule rows are rule_row and rule_test_case in rwb_decision (P7); the case states are in rwb_case (P3). |
| Case list | v_ace_account at 89 and at 90 days past due; 21 entry exclusions; 37 case accounts below the threshold; v_ace_batch_status with COMPLETED and missing rows. case_list_row is the daily projection of rwb-source-data (P1) and the case list API is rwb-case (P3); below SIT the P1 fake returns the same rows. |
| Reconciliation | Variances at zero, below and above recon.tolerance.pct; a person_key with no v_ace_customer row; a payment in v_ace_payment with no proceeds. reconciliation_result is P1; the payment match is P8. |
| Freshness | One ace_batch_run row per source and business date, with COMPLETED, FAILED, LATE and duplicate rows; a weekly source between its batches. Read by P1 only; AceDataReady and AceDataLate (EV-26, EV-27) carry the result to P3, P8, S8 and S7. |
| Views and dictionary | One row per view; a view column with no sys_fields row; a recovery constraint that points at public; a role with no grant. The dictionary is P1 (sys_objects, sys_fields); the 30 views stay in schema recovery and only the rwb_source_data login reads them. |
| Approvals | Decisions at each level and amount boundary of the delegation table. delegation_limit is P4 and approval is P7. |
| Deviations | Cases with each of X1 to X7. deviation is S8; the raise and the clear are EV-06 and EV-07. |
| Documents | The labeled sample of 180 documents across the six types. document, document_text, document_field and signature_request are P5; the file bytes are in Blob with WORM. |
| Batch and job runs | JOB-02, JOB-03 and JOB-04 held by the daily gate, failed at a step and rerun; no inbound file and no file arrival. A job is a Temporal Schedule or an event-started workflow in its owner (Architecture v5 slide 44): JOB-02 and JOB-03 in rwb-case (P3), JOB-04 in rwb-source-data (P1), JOB-11 in every service. |
| Partners | A firm of each partner type with instructions in every status. partner, partner_user and partner_instruction are S9; the partner path enters through the partner gateway in the DMZ. |


A twelfth test is the daily journey smoke run (JOB-22, PlatformSmokeWorkflow). It uses the DEV seed of all 19 schemas and the fakes, and it creates its own case for each journey step, so it leaves the rows of the other tests untouched (CG-B-TESTDOC-41-8; ASM-B-TESTDOC-41-8).

## 3.1 Contract mocks

Below SIT no test waits for another service. Every provider publishes its contract before its code (Architecture v5 slide 11): OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, and an activity contract jar for Temporal. A consuming story builds against the published contract and its fake (Template and Rules R5.4, class C), and the fake is generated from the artefact, never written by hand, so a contract change updates the fake and the test in the same build.

Each fake serves the same business keys as the seed (CG-B-TESTDOC-41-4; ASM-B-TESTDOC-41-4). A case, account or party ID in the fake resolves to the same row as in the sandbox, and every response carries the contract version, so a consumer test proves the pair without a second data set. The events that Architecture v5 slide 43 names without a number appear here by their name and their topic, and take their EV number when the event catalogue owner allocates one (CG-B-TESTDOC-41-7; ASM-B-TESTDOC-41-7).

| Provider | Contract artefacts | What the fake serves | Data in the fake |
|---|---|---|---|
| P1 rwb-source-data | OpenAPI 3.1, 18 REST operations on /api/recovery/source-data/v1; AsyncAPI 3.0, EV-26 AceDataReady and EV-27 AceDataLate; no workflow of its own | GET /data-products/{productCode}/records and GET /data-products/freshness for every data product; GET /cases/{caseId}/interactions; the two events | The account, customer and party keys of the seed; freshness rows COMPLETED, FAILED, LATE and duplicate; a person_key with no v_ace_customer row |
| P2 rwb-integration | OpenAPI 3.1, 11 REST operations; AsyncAPI 3.0, FileDelivered and FileFailed on rwb.integration.events.v1; no workflow of its own | GET /cases/{caseId}/customer-products, GET /cases/{caseId}/plan-status, GET /treatments/{treatmentId}/credit-pack and GET /treatments/{treatmentId}/credit-result; an outbound item at each file status | A credit pack and a credit result; an outbound item that failed and was resent; a file with no arrival |
| P3 rwb-case | OpenAPI 3.1, 22 REST operations; AsyncAPI 3.0, EV-01 to EV-05, EV-19 and EV-29 on rwb.case.events.v1; CaseWorkflow | GET /cases, GET /cases/{caseId}, GET /cases/{caseId}/next-action, GET /cases/{caseId}/timeline, GET /queues, GET /me/tasks; the case events; the CaseWorkflow and its child signals | The 2,812 cases; 21 entry exclusions; 37 case accounts below the threshold; a queue at its limit and one above it |
| P4 rwb-access | OpenAPI 3.1, 4 REST operations; AsyncAPI 3.0, AccessPolicyChanged and DoaLimitChanged on rwb.access.events.v1 (Architecture v5 slide 43) | GET /admin/roles, GET /admin/access-log, GET /me/session, POST /admin/break-glass-grants; the two cache-refresh events | A role with no grant, a role_conflict pair, delegation_limit at each amount boundary, one break-glass grant |
| P5 rwb-document | OpenAPI 3.1, 17 REST operations; AsyncAPI 3.0, EV-16 DocumentStored and EV-17 DocumentFieldsExtracted; DocumentIntakeWorkflow | GET /cases/{caseId}/documents, GET /documents/{documentId}/content as a SAS link, GET /review-items; the two events | The labeled sample of 180 documents across the six types, with a document whose OCR text is empty and a field capture that is corrected |
| P6 rwb-comms | OpenAPI 3.1, 11 REST operations; AsyncAPI 3.0, EV-13, EV-14 and EV-15; NoticeDispatchWorkflow | GET /notices/{noticeId}, POST /cases/{caseId}/notices, the template operations; the three notice events | Every notice status, a notice with proof of delivery, a notice that failed, a template version that is withdrawn |
| P7 rwb-decision | OpenAPI 3.1, 19 REST operations; AsyncAPI 3.0, EV-08 on rwb.decision-record.v1, EV-09 and EV-30; ApprovalWorkflow | GET /approvals and POST /approvals/{approvalId}/approve, refuse and return; GET /decision-log; GET /cases/{caseId}/recommendation; the three events | approval at each level, a rule package with 50 scenarios, a package in force and one superseded, a decision record for every case |
| P8 rwb-payment | OpenAPI 3.1, 2 REST operations; AsyncAPI 3.0, EV-11, EV-12 and EV-25 | GET /proceeds and POST /proceeds/{proceedsId}/match; the three events | A payment with no proceeds, a match that arrives twice, a plan that is missed |
| P9 rwb-reporting | OpenAPI 3.1, 1 REST operation; no event of its own; no workflow of its own | GET /reports/measures | Measures for each business date, with one date that has a late source |
| P10 rwb-agent | OpenAPI 3.1, 11 REST operations; AsyncAPI 3.0, EV-28 AgentRunCompleted; AgentRunWorkflow | GET /cases/{caseId}/agent-outputs, the run and evaluation operations; the event; the workflow interface | A run that answers inside 60 s, a run that falls back to the rule result, one evaluation and one sample per policy |
| S1 rwb-valuation | OpenAPI 3.1, 3 REST operations; AsyncAPI 3.0, RouteDecided on rwb.valuation.events.v1; RouteDecisionWorkflow | POST /cases/{caseId}/route, POST /assets/{assetId}/valuations, POST /assets/{assetKey}/valuations; the workflow interface | The D6 route inputs from the seed, an asset with and without a valuation, a route decision that is overridden |
| S2 rwb-treatment | OpenAPI 3.1, 4 REST operations; AsyncAPI 3.0, EV-10 TreatmentApproved; TreatmentWorkflow | GET and PATCH /treatments/{treatmentId}, POST /cases/{caseId}/treatments, POST /treatments/{treatmentId}/submit | A treatment at every approval state, a plan timer that fires, a treatment that closes |
| S3 rwb-guarantee | OpenAPI 3.1, 2 REST operations; AsyncAPI 3.0, GuaranteeClaimFiled and GuaranteeClaimSettled (Architecture v5 slide 43); GuaranteeClaimWorkflow | POST /cases/{caseId}/guarantee-claims, PATCH /guarantee-claims/{claimId} | A TCG claim and an insurance claim for the same case, one settled and one refused |
| S4 rwb-litigation | OpenAPI 3.1, 5 REST operations; AsyncAPI 3.0, JudgmentRecorded and AuctionResult (Architecture v5 slide 43); LitigationWorkflow | POST /cases/{caseId}/legal-actions, POST /legal-actions/{legalActionId}/hearings, GET and PATCH /legal-actions/{legalActionId} | A legal action at each step, a judgment recorded, a hearing that is adjourned |
| S5 rwb-asset | OpenAPI 3.1, 6 REST operations; AsyncAPI 3.0, EV-22 AssetTakenOn and AssetSold (Architecture v5 slide 43); AssetDisposalWorkflow | GET /assets, GET /assets/{assetId}, POST /assets/{assetId}/listings, POST /listings/{listingId}/rounds | An asset taken on, a listing at each auction round, an asset that sells and one that does not |
| S6 rwb-debtsale | OpenAPI 3.1, 5 REST operations; AsyncAPI 3.0, EV-23 LotAwarded and AccountsTransferred (Architecture v5 slide 43); DebtSaleWorkflow | POST /debt-sale-lots, POST /debt-sale-lots/{lotId}/award, GET /partner/data-room/{lotId} | A lot at each stage, a bid in the data room, a lot awarded and a lot withdrawn |
| S7 rwb-writeoff | OpenAPI 3.1, 2 REST operations; AsyncAPI 3.0, EV-24 WriteOffApproved; WriteOffWorkflow | POST /write-off-scans and POST /write-offs/{writeOffId}/committee-decision; the workflow interface | A write-off approved and one refused; a home and a car in the scan |
| S8 rwb-deviation | OpenAPI 3.1, 2 REST operations; AsyncAPI 3.0, EV-06 and EV-07; DeviationWorkflow | POST /cases/{caseId}/deviations and PATCH /deviations/{deviationId} | A deviation for each of X1 to X7, at pause, handling and return |
| S9 rwb-partner | OpenAPI 3.1, 6 REST operations; AsyncAPI 3.0, EV-20 and EV-21; InstructionWorkflow | GET /partners, GET /partner/instructions, POST /cases/{caseId}/instructions, POST /partner/instructions/{instructionId}/results | A partner of each partner type, an instruction in every status, an invoice and a result |
| gateway-bff | No OpenAPI 3.1 of its own; the composite route over the services; Redis holds sessions only | The composite screen routes and the session, for the screen tests | The session of each role, and the composites of the case screen |


The rules that hold for every fake:

- One fake per provider, generated from the contract artefact: the OpenAPI 3.1 document, the AsyncAPI 3.0 document or the activity contract jar. The product that hosts the fakes is Not specified in the source documents (CG-B-TESTDOC-41-3; ASM-B-TESTDOC-41-3).

- A fake holds no state of its own. It returns the rows of the seed file it was loaded with, keyed by caseId, accountId or partyKey, and it is reloaded whenever the seed changes.

- A REST fake answers inside the 2 s timeout and returns RFC 9457 problem details for the error cases the contract lists, including 404, 409 and 422 (Architecture v5 slide 11).

- A Kafka fake publishes CloudEvents 1.0 in binary mode on the provider topic with key caseId, and can replay a duplicate so the consumer's inbox dedupe (processed_event) is exercised.

- A Temporal fake is the provider's activity contract jar with a stub implementation on the consumer's test worker. Workflow code is tested against the Temporal test server with time skipping, and the recorded histories are replayed in every build (Architecture v5 slide 46).

- A fake is never used where the dependency class is I. The integration stories of RWB-ITG-W1 to RWB-ITG-W4 run against the real services in SIT (Template and Rules R5.4 and R5.7 rule 4).

- No fake carries personal data. It carries the masked or synthetic values of the seed only, and events and workflow inputs carry IDs and business facts (Template and Rules R7.2, section 17).

# 4. Handling personal data

Masking follows RWB-E1-037. The rules, the masking version and the masking position are data; they are held in rwb_access (P4) as masking_rule, and Compliance sets them and approves each version (CG-B-TESTDOC-41-5; ASM-B-TESTDOC-41-5).

- No production data in DEV. The sandbox is synthetic and is rebuilt from the seed and the DDL of each schema.

- The ACE-shaped tables hold clear values where ACE holds them, because ACE is the system of record; the sandbox verifier allows a clear identity number only there.

- recovery.v_ace_customer exposes id_no_masked (DF-ACE-073) and id_no_last4 (DF-ACE-074) only. The clear identification number never leaves ACE, there is no token and no token store, and only the `rwb_source_data` login reads the view.

- recovery.v_ace_contact exposes contact_value and contact_value_masked (DF-ACE-078, DF-ACE-079). Phone, email and address are clear in the view because notices and calls need them; display masking is applied at the API, by the service that owns the field.

- Masking is applied by role under RWB-E1-037 with masking version MASK-SIT-01; a personal field with no masking rule is masked.

- No clear personal value is written to any of the 19 Recovery schemas. The sandbox verifier fails the build and names the schema, the table and the column when one appears.

- No personal data crosses a service boundary. Events, workflow inputs and activity payloads carry IDs and business facts only, and Temporal payloads are encrypted by the codec (AES-GCM, Key Vault keys) (Architecture v5 slides 11 and 46).

- Masked data never leaves SIT and UAT. Defect records and screenshots carry no personal data.

- The PDPA lint (RWB-TE-011) checks fixtures, code and logs in the pipeline. Test data is refreshed before each release and destroyed when the environment is rebuilt.

# 5. Owners

Every owner below is the owner the Ownership Map v1 records. The version 3 wording of each row is kept; the map adds the service that holds the data.

| Item | Owner | Where the Ownership Map records it |
|---|---|---|
| Synthetic seed and fixtures | rwb-source-data (P1) for the ACE-shaped rows and the extension tables; the owning service for the rows of each of the other 18 schemas | Sheets Services and Tables (93 rows) |
| ACE-shaped seed and batch rows | rwb-source-data (P1), the only login that reads the 30 recovery.v_ace_* views | Sheets Services and Tables |
| Masked copies | rwb-access (P4) holds the masking rules; rwb-source-data (P1) applies the mask at the view | Sheet Tables (masking_rule, P4) |
| Document sample | rwb-document (P5); the file bytes stay in Blob with WORM | Sheets Services and Tables |
| Approval of masking rules and masked copies | rwb-access (P4) holds the approved masking version; Compliance approves it | Sheet Tables (masking_rule) |
| View, dictionary and grant fixtures | rwb-source-data (P1) for the 30 views, the dictionary and the grants; the platform DB epic creates the 19 logins | Sheets Tables and Services |
| Contract fakes | the provider service of each fake, one per service, plus the platform for gateway-bff | Sheets Services, Endpoints, Events and Workflows and activities |
| Job and schedule data | the owning service of each job, one of the 22 jobs on the sheet | Sheet Jobs (22 rows) |


# 6. Counts the build checks

| Item | Count |
|---|---|
| Tier 1 ACE tables | 22 |
| Tier 2 ACE tables | 14 |
| Recovery tables | 92 |
| Extension tables | 4 |
| recovery.v_ace_* views | 30 (16 Section A, 14 Section B) |
| Dictionary objects | 122 |
| Dictionary fields | 1,366 (304 on the views, 49 on the extension tables) |
| Removed tables | 0 seeded, 0 read; 20 do not exist |
| Cases in the sandbox | 2,812 plus 10 for each exception shape |
| Service schemas | 19 (one per service, rwb_<name>) |
| Logins | 19 (one per service, with its own PgBouncer pool and connection cap) |
| Tables owned | 93 in the Ownership Map sheet Tables (87 in the 18 service schemas that own tables, 6 in the platform library) |
| Platform library objects | 4 in every schema; 2 (feature_flag, feature_flag_change) in rwb_integration only |
| REST operations | 156 in the Ownership Map sheet Endpoints (151 on the 19 services, 5 platform) |
| Events | 30 numbered in the Ownership Map (EV-01 to EV-30), plus the events Architecture v5 slide 43 names without a number |
| Workflows and activities | 15 (14 services and the platform smoke workflow) |
| Jobs | 22 in the Ownership Map sheet Jobs (Temporal Schedules and event-started workflows) |
| Contract fakes | 20 (one per service and one for gateway-bff) |


# 7. Change log

| Version | Date | Change | Source |
|---|---|---|---|
| 3 | 15 November 2026 | D-RCV-35 (U1, U4); ADR-010; DL43. One recovery schema, seeded by the sandbox and read through the 30 views. | Recovery Workbench Test Data Plan v3 |
| 4 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Synthetic data per schema in section 2.1, contract mocks in section 3.1, owners from the Ownership Map in section 5, and the counts each build checks in section 6. Every section, ID, number and date of version 3 is kept; the document states no release date, so no date is marked tentative. | Recovery Workbench Test Data Plan v3; Architecture v5 Text Extract v1; Ownership Map v1 |

