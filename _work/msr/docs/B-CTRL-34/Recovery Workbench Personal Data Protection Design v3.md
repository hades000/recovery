SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Personal data protection design

Version 3, 22 November 2026. The version 2 text is dated 28 October 2026 and its own version stamp reads 1 (CG-B-CTRL-34-1; ASM-B-CTRL-34-1).

| Item | Detail |
|---|---|
| Document | Recovery Workbench personal data protection design |
| Version | 3 |
| Date | 22 November 2026 |
| Source version | 2, dated 28 October 2026 |
| Prepared by | Henka Group |
| Structure | Thai Personal Data Protection Act B.E. 2562 |
| Decision | D-RCV-60 microservice realignment |
| Status | Draft (no approval is recorded in version 2; CG-B-CTRL-34-4; ASM-B-CTRL-34-4) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Dates | Programme dates are tentative (D-RCV-60) |
| Change log | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

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

In the target architecture the contact point and its consent state are held by rwb-source-data (P1) in contact_point_ext (Ownership Map v1); the contact plan that reads the state is run by rwb-comms (P6) on the instruction of the case. The table and column that carry the consent state in the target schema are read as contact_point_ext in rwb_source_data, and the column name is Not specified in the source documents (CG-B-CTRL-34-3; ASM-B-CTRL-34-3).

# 4. Minimization and masking

- National ID and passport numbers are tokenized at load; the clear value is not stored.

- Each role has a masking profile; fields are masked unless the role may see them.

- Each screen and each agent receives only the fields it needs.

- Debt sale tapes carry only the fields the sale terms allow and pass a masking check.

The four points are unchanged. Their target owners are: the load and the tokenization point, rwb-source-data (P1, the only service that reads the ACE views); the masking profile, rwb-access (P4, masking_rule); the field scope of a screen, the owning service behind gateway-bff; the field scope of an agent, rwb-agent (P10) through the tool gateway. Each service enforces the masking rules of rwb-access in its own code (ADR-014, DP-08), so a service can never return a field outside the caller's profile. Which service mints the token and in what format is Not specified in the source documents (CG-B-CTRL-34-8; ASM-B-CTRL-34-8); the load point is rwb-source-data (P1) and the clear value is not written to any schema. Which service performs the masking check on a debt sale tape is Not specified in the source documents (CG-B-CTRL-34-5; ASM-B-CTRL-34-5); it is read as rwb-debtsale (S6) selecting the fields and rwb-integration (P2) performing the check at delivery.

# 5. Access

- Access by role, capability area and scope; out of scope records are not returned.

- Every read of a personal field is logged through PII Kafka.

- Access is reviewed every six months by the role owners.

The role, capability area and scope data stay in rwb-access (P4): role, permission, masking_rule, delegation_limit and role_conflict, with the access log. The six-monthly review is a Temporal Schedule on queue rwb-access (Architecture v5 slide 14), so the review list is a job of P4. The read log is the ACE Common PII logging path to the SOC (Architecture v5 slides 8 and 34); its event contract is Not specified in the source documents (CG-B-CTRL-34-6; ASM-B-CTRL-34-6), and no business topic carries it.

# 6. Retention

Retention is set per data product and document type in the records retention and archiving schedule. A legal hold overrides retention. Expired data is disposed of by a recorded decision.

Retention is now a service obligation: rwb-document (P5) owns retention_rule and retention_action and the retention Schedule (JOB-17), and every other service applies the rule set for the data products it owns, inside its own schema (ADR-014, ADR-021). The schedule itself is unchanged by this version.

# 7. Data subject rights

| Right | Path | Time |
|---|---|---|
| Access | Request through the bank's PDPA process; Compliance retrieves the case data | Within 30 days |
| Correction | Corrected in the system of record; the next load updates the Workbench | Within 30 days |
| Erasure or restriction | Assessed against the legal claims exemption; automated processing held while assessed (R-UNI-11) | Within 30 days |
| Objection | Assessed by Compliance | Within 30 days |

Compliance keeps the process. Retrieval is through the contract of each owning service, one hop, under the Compliance role and scope (section 11); rwb-case (P3) supplies the case view and the case ID that joins the services. How a rights request is addressed across 19 services is Not specified in the source documents (CG-B-CTRL-34-7; ASM-B-CTRL-34-7).

# 8. Sharing outside the bank

| Recipient | What | Safeguard |
|---|---|---|
| Law firms, agencies, valuers, auction vendors | The data the instruction needs | Contract with data protection terms; firm scope in the partner portal |
| Debt buyers and AMCs | Masked data tape before award; full data after transfer | Non-disclosure agreement; masking check |
| Courts and the Legal Execution Department | Filings | Legal obligation |
| Cross-border | None planned; data stays in the SCB Azure tenant, Southeast Asia | Bank position to confirm |

Each row now has an owning service. The partner portal and the firm scope are rwb-partner (S9); the tape and the sale terms are rwb-debtsale (S6), with rwb-integration (P2) delivering the file over MFT/SFTP (INT-25); court filings and the Legal Execution Department ladder are rwb-litigation (S4); the cross-border position is the bank's, DL33 stands, and the model endpoint is called only by rwb-agent (P10) inside the SCB tenant.

# 9. Breach

A suspected breach is an incident to SCB security operations. Compliance assesses it and notifies the regulator within 72 hours where the Act requires, and the people affected where the risk is high.

The evidence a breach assessment needs is now split across services: audit and PII access logs reach the SOC through the ACE Common PII Kafka path (all 19 services), the decision trail is sealed in the central ledger of rwb-decision (P7), and the documents are in rwb-document (P5). No service adds a second audit path.

# 10. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL26 | Retention and masking | Proposed classes and profiles |
| DL33 | Model endpoint location | Inside the SCB tenant; no cross-border transfer |

# 11. Personal data boundaries per service

The microservice realignment gives every service its own schema, its own login and its own tables (ADR-014, DP-01, DP-02). The rule of this design is unchanged: personal data stays in the owning service, and every other service reaches it through a contract. This section writes that rule per service. Version 2 states the categories and the controls but names no service owner for any of them (CG-B-CTRL-34-2; ASM-B-CTRL-34-2). Every owner below is the table owner in the Ownership Map v1 (D-RCV-60); the service, schema and REST base are its architecture rows.

Table 11.1 — what each service may hold and must not hold.

| Owner (Ownership Map) | Personal data it may hold | Where it is held | What it must not hold |
|---|---|---|---|
| P1 rwb-source-data | All five categories of section 1 at field level, because it is the only load point: the tokenized national ID and passport number, date of birth, contact points with consent state, interaction summaries, the extension attributes, and the dated copies of treatment and guarantee records | rwb_source_data: party_ext, contact_point_ext, account_ext, valuation_ext, interaction, efs_ledger_outcome, case_list_row, dp_treatment, dp_guarantee_claim, reconciliation_result, sys_fields | The masking profile (P4); documents and OCR text (P5); notice content (P6); agent prompts and runs (P10); the case state of record (P3) |
| P2 rwb-integration | The file content only while it is in transit, and the delivery details of the outbound item | rwb_integration: interface_config, outbound_item, file runs | The business record the file carries; any personal data after delivery beyond the file run; the case state or the document |
| P3 rwb-case | The case, party and account references, the queue and task facts, allocation and timer facts, the exclusion list, queue measures, and the staff identifier of the officer who owns a task | rwb_case: recovery_case, case_party, case_account, task, queue, queue_member, assignment, timer, case_entry_exclusion, queue_measure | The party master record and the contact points (P1); balances and arrears (the P1 data products); documents (P5); notices (P6) |
| P4 rwb-access | Staff identifiers of internal users, roles, capability areas, scopes, DoA limits, masking profiles and the access log | rwb_access: role, permission, masking_rule, delegation_limit, role_conflict, access log | Customer personal data of any category in section 1 |
| P5 rwb-document | The document, its OCR text and extracted fields (direct identifiers), the signature requests, the custody trail and the retention rules | rwb_document: document, document_text, document_field, document_type, document_intake, document_custody, document_checklist_item, case_document_check, signature_request, retention_rule, retention_action | The case state (P3); the notice (P6); the business record the document proves; extracted field values on any event |
| P6 rwb-comms | The notice as issued, with its recipient and merge fields, and the proof of delivery | rwb_comms: notice, template, merge_field | The case state (P3); documents and extracted fields (P5); any data the notice does not need |
| P7 rwb-decision | The decision and the approval for a case: case ID, decision code, rule package and version, the acting staff identifier and role; no case content | rwb_decision: approval, decision_log_entry, rule_package, rule_package_version, rule_row, rule_test_case | Customer personal data; live personal data in rule rows or rule test cases |
| P8 rwb-payment | Payment and proceeds facts: account reference, amounts, fees, bookings and the posting file | rwb_payment: proceeds | The party master and the contact points (P1); documents (P5) |
| P9 rwb-reporting | Measures, snapshots, the steering dashboard and the regulatory reports, built from business events | rwb_reporting: measure_definition, measure_snapshot, measure_publish | The case of record; any service's operating tables (DP-01); a data lake copy, which does not exist (DP-17) |
| P10 rwb-agent | The agent policies, prompts, runs, guardrails, evaluations, samples, feedback and alerts; prompts and samples carry masked fields only | rwb_agent: agent_policy, agent_prompt, agent_run, agent_evaluation, agent_evaluation_run, agent_sample, agent_feedback, agent_alert | Clear identifiers in a prompt, a sample or a run; the case of record |
| S1 rwb-valuation | The valuations of collateral, the D6 route decision and the route agent output | rwb_valuation: valuation | The valuation extension attributes (P1); documents (P5) |
| S2 rwb-treatment | Treatments, contracts, settlement and deed-in-lieu agreements and plan timers | rwb_treatment: treatment | The party master and contact points (P1); the signed document and the signature request (P5) |
| S3 rwb-guarantee | TCG and insurance claims, guarantor notices and pursuit, including the guarantor's personal data | rwb_guarantee: guarantee_claim | The borrower's party master (P1); contact points (P1) |
| S4 rwb-litigation | Legal actions, hearings, judgments and enforcement, with the court case references | rwb_litigation: legal_action, hearing | Documents (P5); the notice content (P6) |
| S5 rwb-asset | Assets taken on, their holding, floor price, listings, auction rounds and the sale record | rwb_asset: asset_sale, listing | The party master (P1); the valuation record (S1) |
| S6 rwb-debtsale | Lots, the data room, buyer terms, bids, the award and the transfer; the masked tape pack and the buyer's user records | rwb_debtsale: debt_sale_lot, debt_sale_account | The unmasked tape; full data before the transfer; another service's case record |
| S7 rwb-writeoff | Eligibility, the committee, the posting and the recovery after charge-off | rwb_writeoff: write_off | The party master (P1); documents (P5) |
| S8 rwb-deviation | The X1-X7 screening, the pause, the handling and the return, and the sensitive flags of section 1 as they are screened | rwb_deviation: deviation | A second copy of the party flags, which P1 brings (P1) |
| S9 rwb-partner | The panel, partner users (a staff identifier), instructions, results, fees and scorecards, and the case data an instruction needs | rwb_partner: partner, partner_user, partner_instruction | The case of record (P3); any data beyond the instruction |

Table 11.2 — where each control is enforced.

| Control (section) | Enforced in every service by | Owner of the rule |
|---|---|---|
| Tokenization at load (4) | The load into rwb_source_data; no other service loads ACE data | P1 rwb-source-data |
| Masking profile per role (4) | The guard library of DP-08, called on every read | P4 rwb-access |
| Field scope per screen (4) | gateway-bff composite route and the owning service | The owning service, with P4 rwb-access |
| Field scope per agent (4) | The read-only tool gateway of the agent run | P10 rwb-agent, with P4 rwb-access |
| Access by role, scope and DoA (5) | POST /authorise on every action; the service caches the answer | P4 rwb-access |
| Read of a personal field is logged (5) | The ACE Common PII logging path to the SOC | ACE Common (role: SOC), for every service |
| Retention and legal hold (6) | The retention Schedule and retention_action | P5 rwb-document |
| Business events carry no personal data (12) | The outbox and the schema registry, checked by the contract test | The producing service |

Two design points follow and are the only new decisions in this version. First, no service reads another service's tables: a cross-service read is a REST call with a 2 s timeout, one hop (ADR-020, DP-11), and ACE data is read only by rwb-source-data through the 30 read-only recovery.v_ace_* views (ADR-010, DP-05). Second, a field a service is not allowed to hold is fetched at the moment of need through the owner's contract under the caller's own profile, and is never copied into the caller's schema.

# 12. Personal data in events, workflow payloads and logs

Events carry IDs and business facts, never personal data (Architecture v5 slides 22, 42 and 43). The realignment makes that a per-topic contract rather than a habit.

Table 12.1 — the event envelope.

| Element | Rule | Basis |
|---|---|---|
| Envelope | CloudEvents 1.0, binary mode; ce_id, ce_type, ce_source, ce_subject as headers; W3C traceparent | ADR-015, DP-09 |
| Key | caseId | Architecture v5 slide 22 |
| Body | IDs and business facts only; no names, contact points, national IDs, extract values or free text that repeats them | Architecture v5 slides 22, 42 and 43 |
| Schema | JSON Schema registry, BACKWARD compatibility; the AsyncAPI document per service is the contract | ADR-015 |
| Transport | Outbox in the same transaction as the state change; inbox dedupe on ce_id; retry topics and a dead-letter topic with a replay tool | ADR-015, DP-09 |
| ACL | One topic per service, with its own ACLs and quotas, separate from the ACE PII logging topics | ADR-015; Architecture v5 slide 37 |

Table 12.2 — what each event may carry, and where the personal data stays.

| Event | Producer (owner) | What travels on the topic | Where the personal data stays |
|---|---|---|---|
| CaseCreated | P3 rwb-case | Case ID, product group, queue code, business date | rwb_case; the party and its contact points stay with P1 |
| CaseStateChanged | P3 rwb-case | Case ID, from state, to state, stage code | rwb_case |
| DocumentStored | P5 rwb-document | Document ID, case ID, document type code | rwb_document; the file in the Azure Blob WORM store |
| DocumentFieldsExtracted | P5 rwb-document | Document ID, case ID, the field codes and the field count | rwb_document, document_field; the extracted values never leave P5 on the topic |
| NoticeGenerated | P6 rwb-comms | Notice ID, case ID, template code, channel code | rwb_comms, notice; the recipient and the content stay in P6 |
| NoticeDispatched, NoticeDelivered | P6 rwb-comms | Notice ID, channel code, dispatch and delivery status, proof reference | rwb_comms; the proof of delivery |
| DecisionRecorded | All 19, ledger in P7 | Ledger entry ID, case ID, decision code, rule package and version | rwb_decision, decision_log_entry |
| ApprovalRequested | P7 rwb-decision | Approval ID, case ID, DoA level code, requested action code | rwb_decision, approval; the acting staff identifier |
| TreatmentApproved | S2 rwb-treatment | Treatment ID, case ID, scheme code | rwb_treatment |
| PaymentMissed | P8 rwb-payment | Payment ID, case ID, instalment reference, due date, status | rwb_payment |
| AgentRunCompleted | P10 rwb-agent | Run ID, case ID, agent code, policy and prompt version, outcome code, confidence band | rwb_agent; no prompt text and no model output on the topic |
| InstructionIssued | S9 rwb-partner | Instruction ID, partner ID, service type code, SLA due time | rwb_partner; the partner user and the instruction detail |
| LotAwarded, AccountsTransferred | S6 rwb-debtsale | Lot ID, bid ID, and the account references under the transfer (an indirect identifier, section 1) | rwb_debtsale; the masked tape travels as an encrypted file through P2 (INT-25) |
| GuaranteeClaimFiled | S3 rwb-guarantee | Claim ID, case ID, claim type code, guarantor reference | rwb_guarantee; the guarantor's personal data |
| AceDataReady, AceDataLate | P1 rwb-source-data | Business date, source code, record counts, freshness time | rwb_source_data |
| RulePackageInForce | P7 rwb-decision | Package code, version, checksum, effective date | No personal data anywhere on this topic |

Workflow payloads and histories follow the same rule.

- Temporal payloads are encrypted by PdpaPayloadCodec (AES-GCM, keys in Key Vault, one key set per namespace rwb-recovery).
- The search attributes are CaseId, Stage, ProductGroup and QueueCode only.
- A history never holds clear personal data; retention is 30 days for closed workflows, then the archive to Blob (E2-039).
- The CaseWorkflow parent passes a case ID and a stage code to each stage child workflow (DP-12); case content is read inside an activity, from the owning service's contract, and is not carried in the workflow input.
- Decoding a payload is a break-glass action for RW-SECADM; RW-PLATADM operates and RW-AUDIT reads without decoding (Temporal and Drools Design v1 slide 11).
- A decision record keeps the rule package and version, so a replay or an audit reads the same answer without the case content (DP-03); the central ledger is rwb-decision (P7).

Logs, traces and the PII path.

- Every service sends audit and personal-data access logs through the ACE Common PII Kafka path to the SOC; that path is not a business topic and no service publishes to it directly (Architecture v5 slides 8 and 34).
- Application logs, traces and metrics carry the case ID, the service name and the W3C trace context; never a name, a contact point, a national ID or a document field value.
- The read log of section 5 keeps its version 2 wording; its event schema is Not specified in the source documents (CG-B-CTRL-34-6; ASM-B-CTRL-34-6).

Files and third parties follow section 8.

- A debt sale tape is selected by S6 rwb-debtsale to the sale terms, checked against the masking rules of P4 before it leaves, and delivered by P2 rwb-integration as an encrypted file (INT-25).
- A WIN letter is generated by P6 rwb-comms and delivered by P2 as the daily outbound file (INT-14).
- A partner uploads and downloads through the partner gateway (FAPI 2.0) into rwb-document (P5), under the firm scope held by rwb-partner (S9).

# 13. Change log

| Version, date, change, tool |
|---|
| 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

What changed in version 3, and nothing else:

- The header lines are the Template and Rules R8.1 header; the title block and the metadata table keep the version 2 rows, add the source version, the decision, the status, the tool and the change-log row, and mark programme dates tentative.
- Sections 1, 2, 6, 9 and 10 are kept word for word, with a closing paragraph where the target owner of a statement has to be named (sections 6 and 9).
- Section 3 keeps its three points word for word and names rwb-source-data (P1) as the owner of the contact point and its consent state.
- Section 4 keeps its four points word for word and names the target owner of each.
- Section 5 keeps its three points word for word and names rwb-access (P4) as the owner of the role, scope and masking data and of the six-monthly review.
- Section 7 keeps its table word for word and states the retrieval path against the service contracts.
- Section 8 keeps its table word for word and names the owning service of each row.
- Sections 11 and 12 are new: the personal data boundary per service, and the rule for events, workflow payloads, logs and files.
- Every category, classification, lawful-basis section, right, recipient, safeguard, decision ID (DL26, DL33), rule reference (R-UNI-10, R-UNI-11), time limit and date of version 2 is kept.
