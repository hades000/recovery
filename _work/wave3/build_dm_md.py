# -*- coding: utf-8 -*-
import io, os

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
DST = os.path.join(BASE, r"04 User stories\Recovery Workbench Data Migration Stories v3.md")

HEAD = """# Recovery Workbench data migration stories

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

One story per Workbench data product: extract from the legacy Workbench, map the ids to ACE business keys, load, reconcile and cut over.

Version 3 is re-based on D-RCV-35 and ADR-010. No story loads a source record. ACE holds the account, payment, customer, contact, collateral, asset, appraisal, collections, legal, proof-of-delivery, write-off and score data, and the Workbench reads it through the recovery.v_ace_* views. Two stories leave because the data is already in ACE (RWB-DM-001, RWB-DM-002) and four are reduced to their Workbench-only part (RWB-DM-005, RWB-DM-006, RWB-DM-011, RWB-DM-013). Every account link is an account_key and every person link is a person_key, held as a business key with no foreign key into ACE.

---

"""

MSG = {
    "MSG-P1-001": ("Warning", "{product} is from {date}. Today's ACE batch has not arrived."),
    "MSG-P1-012": ("Warning", "The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent."),
    "MSG-GEN-001": ("Error", "Enter {field}."),
    "MSG-P4-002": ("Error", "You cannot {action} here. Your role does not include it."),
    "MSG-P7-003": ("Error", "The action was not taken because the decision could not be recorded. Try again in a few minutes."),
}

ROW_CASE = "| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |"
ROW_CASE_ACC = "| case_account | id, case_id, account_key, is_primary, linked_from, linked_to | DF-CAS-024 to DF-CAS-029 |"
ROW_CASE_PTY = "| case_party | id, case_id, person_key, party_role, role_from, role_to | DF-CAS-030 to DF-CAS-035 |"

S = []

S.append(dict(
    n="003", title="Migrate case and ownership", epic="E1, release 30 November 2026",
    story=("As a data steward, I want the Workbench case and ownership records migrated from the legacy Workbench with their ACE business keys, so that every open case keeps its owner, its queue and its history from the first day."),
    feature="Migrate case and ownership",
    given="the legacy Workbench case, case account, case party and assignment records for the open cases at cutover",
    then="each case keeps its case number, its owner, its queue and its stage, each account link carries an account_key and each party link a person_key",
    no_copy="no account and no customer record is copied from ACE",
    data_rows=[ROW_CASE, ROW_CASE_ACC, ROW_CASE_PTY,
          "| assignment | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 4 more | DF-WRK-009 to DF-WRK-040 |"],
    screen="No screen in this story.",
    msg_ids=["MSG-P1-001", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="004", title="Migrate treatment and offers", epic="E2, release 31 December 2026",
    story=("As a data steward, I want the agreed but unbooked treatments and their approvals migrated from the legacy Workbench, so that a restructure, settlement or deed already promised to a customer continues without a break at cutover."),
    feature="Migrate treatment and offers",
    given="the legacy Workbench treatment and approval records for the open cases at cutover",
    then="each treatment keeps its case, its type, its offer amount, its approval level and its outcome, and the plan it refers to is read from v_ace_plan",
    no_copy="no plan record is copied and no plan is booked by the migration",
    data_rows=[ROW_CASE,
          "| treatment | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 15 more | DF-TRT-001 to DF-TRT-033 |",
          "| v_ace_plan | plan_ref, account_key, plan_status, booked_at, closed_at, closed_reason and 12 more | DF-ACE-160 to DF-ACE-177 |"],
    screen="| SCR-45 Data quality | Loading; breaks |",
    msg_ids=["MSG-P1-001", "MSG-P1-012", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="005", title="Migrate contact and promises", epic="E1, release 30 November 2026",
    story=("As a data steward, I want the open promises and contact notes held outside EFS migrated to the case, so that no promise a customer made is lost at cutover while the EFS history itself is read from ACE."),
    feature="Migrate contact and promises",
    given="the open promises and contact notes that the legacy Workbench holds outside EFS, with their case numbers",
    then="each interaction keeps its case, its person_key, its contact_key, its promise date and its promise amount",
    no_copy="no EFS contact or promise row is copied, because the history is read from v_ace_efs_action",
    data_rows=[ROW_CASE,
          "| interaction | id, case_id, person_key, occurred_at, channel, direction and 23 more | DF-INT-001 to DF-INT-029 |",
          "| contact_point_ext | contact_key, contact_type, consent_given, consent_at, verified_at, failed_count and 8 more | DF-EXT-013 to DF-EXT-026 |"],
    screen="No screen in this story.",
    msg_ids=["MSG-P1-001", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="006", title="Migrate collateral and assets", epic="E2, release 31 December 2026",
    story=("As a data steward, I want the listings, the case asset links and the open sale instructions migrated from the legacy Workbench, so that an asset already offered for sale is not lost at cutover while the collateral, appraisal and NPA asset records are read from ACE."),
    feature="Migrate collateral and assets",
    given="the legacy Workbench listing, case asset link, sale instruction and appraisal acceptance records at cutover",
    then="each listing and each sale carries its asset_key, and each appraisal decision its valuation_key",
    no_copy="no collateral, appraisal, NPA asset or NPA sale record is copied, because each is read from v_ace_collateral, v_ace_valuation, v_ace_asset, v_ace_npa_asset or v_ace_npa_sale",
    data_rows=[ROW_CASE,
          "| listing | id, asset_key, sale_channel, start_price, floor_price, round_no, listed_at, status | DF-SAL-001 to DF-SAL-008 |",
          "| asset_sale | id, asset_key, listing_id, contract_date, sale_date, sale_price and 5 more | DF-SAL-009 to DF-SAL-019 |",
          "| valuation_ext | valuation_key, accepted, accepted_at, accepted_by, valuer_partner_id, stale_flag and 8 more | DF-EXT-036 to DF-EXT-049 |"],
    screen="| SCR-45 Data quality | Loading; breaks |",
    msg_ids=["MSG-P1-001", "MSG-P1-012", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="007", title="Migrate legal events and cases", epic="E2, release 31 December 2026",
    story=("As a data steward, I want the legal actions, the notices already sent and the open law firm instructions migrated from the legacy Workbench, so that litigation continues at cutover while the court case and hearing records are read from ACE."),
    feature="Migrate legal events and cases",
    given="the legacy Workbench legal action, notice and partner instruction records for the open cases at cutover",
    then="each legal action keeps its case, its court, its claim and its judgment, each notice its person_key, and each instruction its firm and its due date",
    no_copy="no lawsuit and no hearing record is copied, because the court record is read from v_ace_lawsuit and v_ace_hearing",
    data_rows=[ROW_CASE,
          "| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 |",
          "| notice | id, case_id, document_id, notice_type, sent_date, barcode and 8 more | DF-LEG-015 to DF-LEG-034 |",
          "| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |"],
    screen="| SCR-45 Data quality | Loading; breaks |",
    msg_ids=["MSG-P1-001", "MSG-P1-012", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="008", title="Migrate partner performance", epic="E2, release 31 December 2026",
    story=("As a data steward, I want the panel firms, their users and their open instructions migrated from the legacy Workbench, so that panel status and performance continue across cutover."),
    feature="Migrate partner performance",
    given="the legacy Workbench partner, partner user and partner instruction records at cutover",
    then="each firm keeps its panel status, its contract end and its score, each user its role and its dates, and each instruction its case and its result",
    no_copy="no case record is duplicated and no settlement figure is read by the migration",
    data_rows=[ROW_CASE,
          "| partner | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | DF-PRT-001 to DF-PRT-007 |",
          "| partner_user | id, identity_ref, partner_id, role_code, valid_from, valid_to | DF-REF-212 to DF-REF-217 |",
          "| partner_instruction | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | DF-PRT-008 to DF-PRT-016 |"],
    screen="| SCR-45 Data quality | Loading; breaks |",
    msg_ids=["MSG-P1-001", "MSG-P1-012", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="009", title="Migrate debt sale", epic="E2, release 31 December 2026",
    story=("As a data steward, I want the debt sale lots and their accounts migrated from the legacy Workbench, so that a sale in flight keeps its accounts, its reserve price and its buyer."),
    feature="Migrate debt sale",
    given="the legacy Workbench debt sale lot and debt sale account records at cutover",
    then="each lot keeps its cut-off date, its segment, its reserve price and its buyer, and each account link carries an account_key",
    no_copy="no balance and no payment is copied, because both are read from v_ace_account and v_ace_payment",
    data_rows=[ROW_CASE,
          "| debt_sale_lot | id, lot_no, cut_off_date, segment, reserve_price, buyer_partner_id and 5 more | DF-SAL-020 to DF-SAL-030 |",
          "| debt_sale_account | id, lot_id, account_key, borrower_code, outstanding, selling_price, put_back_status | DF-SAL-031 to DF-SAL-037 |"],
    screen="| SCR-45 Data quality | Loading; breaks |",
    msg_ids=["MSG-P1-001", "MSG-P1-012", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="010", title="Migrate documents and extracted fields", epic="E1, release 30 November 2026",
    story=("As a data steward, I want the documents of the open cases and their extracted fields migrated from the legacy Workbench, so that the case file is complete on the first day."),
    feature="Migrate documents and extracted fields",
    given="the legacy Workbench document and document field records for the open cases at cutover",
    then="each document keeps its case, its person_key, its type and its storage reference, and each extracted field its document and its confidence",
    no_copy="no document is re-extracted and no scan is repeated at migration",
    data_rows=[ROW_CASE,
          "| document | id, case_id, person_key, document_type, source, storage_ref and 14 more | DF-DOC-001 to DF-DOC-033 |",
          "| document_field | id, document_id, field_name, field_value, confidence, confirmed_by and 2 more | DF-DOC-012 to DF-DOC-035 |"],
    screen="No screen in this story.",
    msg_ids=["MSG-P1-001", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="011", title="Migrate scores and route economics", epic="E2, release 31 December 2026",
    story=("As a data steward, I want the route each open case carries and the route economics baseline the Workbench calculates migrated, so that the baseline and the route history survive cutover while the COLLINS score itself is read from ACE."),
    feature="Migrate scores and route economics",
    given="the legacy Workbench route decisions, case list rows and baseline measure snapshots at cutover",
    then="each case keeps its route code and route state, and each measure snapshot keeps its dimension, its value and its baseline flag",
    no_copy="no COLLINS score is copied, because the score, its estimate and its route are read from v_ace_score",
    data_rows=[ROW_CASE,
          "| case_list_row | id, business_date, case_id, case_no, account_key, product_group and 13 more | DF-RPT-001 to DF-RPT-019 |",
          "| measure_snapshot | id, measure_code, definition_version, business_date, product_group, dimension_code and 6 more | DF-RPT-041 to DF-RPT-052 |"],
    screen="| SCR-45 Data quality | Loading; breaks |",
    msg_ids=["MSG-P1-001", "MSG-P1-012", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="012", title="Migrate decision log", epic="E1, release 30 November 2026",
    story=("As a data steward, I want the decisions taken outside the Workbench on the open cases migrated with their rule and model version and their hash chain, so that the audit trail is unbroken from the first day."),
    feature="Migrate decision log",
    given="the legacy Workbench decisions taken outside it on the open cases at cutover",
    then="each entry keeps its case, its decision code, its rule and model version, its approver and its position in the chain",
    no_copy="no entry is rewritten, renumbered or re-hashed, because every entry is append-only",
    data_rows=[ROW_CASE,
          "| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 16 more | DF-DEC-001 to DF-DEC-031 |"],
    screen="No screen in this story.",
    msg_ids=["MSG-P1-001", "MSG-GEN-001", "MSG-P4-002", "MSG-P7-003"],
    extra_test="| TC-DM-012-05 | Principle 5 | A forced decision log write failure stops the migration with MSG-P7-003 |",
))

S.append(dict(
    n="013", title="Migrate money and closure", epic="E2, release 31 December 2026",
    story=("As a data steward, I want the open proceeds matches and the closures recorded in the legacy Workbench migrated, so that money already received stays matched to its case and a closed case keeps its closure reason."),
    feature="Migrate money and closure",
    given="the legacy Workbench proceeds, closure and write-off decision records at cutover",
    then="each proceeds row carries its payment_code and its case, each closure keeps its closed date and reason, and each write-off decision its committee date",
    no_copy="no payment and no GL posting is copied, because both are read from v_ace_payment and v_ace_write_off",
    data_rows=[ROW_CASE,
          "| proceeds | id, case_id, treatment_id, payment_code, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |",
          "| write_off | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date and 5 more | DF-FIN-010 to DF-FIN-020 |"],
    screen="| SCR-45 Data quality | Loading; breaks |",
    msg_ids=["MSG-P1-001", "MSG-P1-012", "MSG-GEN-001", "MSG-P4-002"],
))

S.append(dict(
    n="014", title="Migrate reference data", epic="E1, release 30 November 2026",
    story=("As a data steward, I want the rules, the approval limits, the lists of values and the letter templates that the Workbench owns migrated as versioned reference data, so that the versions in force at go-live are the ones the business approved."),
    feature="Migrate reference data",
    given="the legacy Workbench reference versions, their rows and the lists of values that the Workbench owns",
    then="each version keeps its table code, its version number, its valid from date and its approver, and each row its key and its data",
    no_copy="no list that ACE holds is re-loaded, because the action codes, the products, the branches and the holidays are read from v_ace_efs_action_code, v_ace_product, v_ace_branch and v_ace_holiday",
    data_rows=["| lov_value | id, lov_code, value_code, label_en, label_th, sort_order and 1 more | DF-REF-027 to DF-REF-033 |",
          "| reference_version | id, table_code, version_no, version_label, valid_from, valid_to and 16 more | DF-REF-159 to DF-REF-180 |",
          "| reference_row | id, version_id, row_key, row_data | DF-REF-181 to DF-REF-184 |"],
    screen="No screen in this story.",
    msg_ids=["MSG-P1-001", "MSG-GEN-001", "MSG-P4-002"],
))

REMOVED_001 = """## RWB-DM-001 Migrate account and arrears

**Removed by D-RCV-35. The data is already in ACE.**

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Status | Removed |
| Decision | D-RCV-35 (U1) |
| Why | ACE ingests the ALS account, arrears and balance data and holds the one copy. The Workbench loads none of it, so there is nothing to extract, transform, load or reconcile. |
| Read path instead | v_ace_account for the account, the arrears, the balances, the classification and the ACE business date; v_ace_bucket_log for the monthly bucket history; v_ace_product and v_ace_branch for the product and branch lists |
| Data product | DP01 stays in the catalog with system of record "ACE (ingested from ALS)" and its view list. Only the migration story leaves. |
| Withdrawn IDs | AC1 to AC3; TC-DM-001-01 to TC-DM-001-04 |
| Later home | None. Any column the Workbench still needs is raised once in RWB-ACE-001. |

---

"""

REMOVED_002 = """## RWB-DM-002 Migrate customer and party

**Removed by D-RCV-35. The data is already in ACE.**

| Item | Value |
|---|---|
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Status | Removed |
| Decision | D-RCV-35 (U1) |
| Why | ACE ingests the SCBPDM customer, phone, email and address data and holds the one copy. The Workbench loads none of it, so there is nothing to extract, transform, load or reconcile. |
| Read path instead | v_ace_customer for the customer and the masked identity, v_ace_contact for phone, email and address, v_ace_ca_relation for the borrower, guarantor and co-borrower roles, and party_ext and contact_point_ext for the Workbench flags and consent |
| Data product | DP02 stays in the catalog with system of record "ACE (ingested from SCBPDM)" and its view list. Only the migration story leaves. |
| Withdrawn IDs | AC1 to AC3; TC-DM-002-01 to TC-DM-002-04 |
| Later home | None. Any column the Workbench still needs is raised once in RWB-ACE-001. |

---

"""


def block(s):
    n = s["n"]
    rows = "\n".join(s["data_rows"])
    msgs = "\n".join("| %s | %s | %s |" % (m, MSG[m][0], MSG[m][1]) for m in s["msg_ids"])

    if n == "014":
        ac2 = """  Scenario: AC2 Reconcile the versions
    Given the migrated reference versions
    When the reference data service validates them
    Then every version in force has its row count, its content hash and its approver
    And every rule row names the test case that proves it"""
    else:
        ac2 = """  Scenario: AC2 Reconcile the business keys
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team"""

    tests = ["| TC-DM-%s-01 | AC1 | Extract the Workbench records |" % n,
             "| TC-DM-%s-02 | AC2 | Reconcile the business keys |" % n if n != "014" else "| TC-DM-%s-02 | AC2 | Reconcile the versions |" % n,
             "| TC-DM-%s-03 | AC3 | Cut over |" % n,
             "| TC-DM-%s-04 | Access | A role without the right is refused with MSG-P4-002 |" % n]
    if s.get("extra_test"):
        tests.append(s["extra_test"])
    tests = "\n".join(tests)

    screen = s["screen"]
    if screen.startswith("|"):
        screen = "| Screen | States |\n|---|---|\n" + screen

    return """## RWB-DM-{n} {title}

| Item | Value |
|---|---|
| Epic | {epic} |
| Module | P1 Recovery data engine |
| Feature | None |
| Process | All recovery processes |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-069 |
| Decision | DL25 |

**Story.** {story}

**Acceptance criteria**

```gherkin
Feature: {feature}

  Scenario: AC1 Extract the Workbench records
    Given {given}
    When the migration reads them
    Then {then}
    And {no_copy}

{ac2}

  Scenario: AC3 Cut over
    Given ten clean days on the migrated records
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
```

**Data**

| Entity | Fields | BR Field IDs |
|---|---|---|
{rows}

**Endpoints**

No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract.

**Screen and states**

{screen_out}

**Permission checks**

| Capability area | Right | Roles that hold it |
|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM |

**Validation and messages**

| ID | Type | Message |
|---|---|---|
{msgs}

**Test cases**

| ID | Covers | Test |
|---|---|---|
{tests}

**Guardrails.** No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row.

---

""".format(**s, rows=rows, msgs=msgs, tests=tests, ac2=ac2, screen_out=screen)


out = [HEAD, REMOVED_001, REMOVED_002]
for s in S:
    out.append(block(s))
doc = "".join(out)
io.open(DST, "w", encoding="ascii", newline="\n").write(doc)
print("written", DST, len(doc), "sections", doc.count("\n## RWB-DM-"))
