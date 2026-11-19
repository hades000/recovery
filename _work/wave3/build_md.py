import re, sys, io, os

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(BASE, r"04 User stories\Recovery Workbench User Stories Epic 2 v5.md")
DST = os.path.join(BASE, r"04 User stories\Recovery Workbench User Stories Epic 2 v6.md")
FRAG = os.path.join(BASE, r"_work\wave3")

text = open(SRC, encoding="utf-8").read()
frag = {k: open(os.path.join(FRAG, "e2-%s.md" % k), encoding="utf-8").read().rstrip("\n") + "\n"
        for k in ("001", "003", "007", "008", "010", "034")}

# ---------- split header, summary table, stories ----------
m = re.search(r"(?m)^## RWB-E2-001 ", text)
head = text[:m.start()]
body = text[m.start():]
parts = re.split(r"(?m)^(?=## RWB-E2-\d+ )", body)
parts = [p for p in parts if p.strip()]
stories = {}
order = []
for p in parts:
    key = re.match(r"## (RWB-E2-\d+)", p).group(1)
    stories[key] = p.rstrip("\n") + "\n"
    order.append(key)
assert len(order) == 35, len(order)

# ---------- summary table edits ----------
head = head.replace("| Stories | 35 |", "| Stories | 34 |")
head = head.replace("| Modules | P1 (1), P2 (10), P3 (5), P4 (1), P5 (4), P6 (3), P7 (3), P8 (2), P9 (1), P10 (5) |",
                    "| Modules | P1 (1), P2 (9), P3 (5), P4 (1), P5 (4), P6 (3), P7 (3), P8 (2), P9 (1), P10 (5) |")

titles = {
    "RWB-E2-001": "EFS hand-over with full history",
}
deps = {
    "RWB-E2-001": "RWB-E1-069, RWB-E1-015, RWB-E1-007",
    "RWB-E2-003": "RWB-E1-069, RWB-E1-007",
    "RWB-E2-007": "RWB-E2-004, RWB-E1-069, RWB-E1-007",
    "RWB-E2-008": "RWB-E2-004, RWB-E1-069",
    "RWB-E2-010": "RWB-E2-004, RWB-E1-069, RWB-E1-016, RWB-E1-015",
    "RWB-E2-034": "RWB-E1-027, RWB-E2-016, RWB-E1-069, RWB-E1-007, RWB-E1-066, RWB-E1-067, RWB-TE-006",
}

head_lines = head.split("\n")
out_head = []
for ln in head_lines:
    mm = re.match(r"\| (RWB-E2-\d+) \| ([^|]+) \| ([^|]+) \| ([^|]*) \| ([^|]+) \|$", ln)
    if mm:
        key, title, module, reqs, dep = [x.strip() for x in mm.groups()]
        if key == "RWB-E2-023":
            continue
        if key in titles:
            title = titles[key]
        if key in deps:
            dep = deps[key]
        ln = "| %s | %s | %s | %s | %s |" % (key, title, module, reqs, dep)
    out_head.append(ln)
head = "\n".join(out_head)

# ---------- replace rewritten stories, drop 023 ----------
order = [k for k in order if k != "RWB-E2-023"]
for k, v in frag.items():
    stories["RWB-E2-" + k] = v

doc = head.rstrip("\n") + "\n\n" + "\n---\n\n".join(stories[k].rstrip("\n") for k in order) + "\n"

# ---------- global entity and field edits ----------
pairs = [
    ("| DF-ACC-002 | loan_account | account_no | Read |", "| DF-ACE-002 | v_ace_account | account_code | Read |"),
    ("| DF-ACC-004 | loan_account | product_code | Read |", "| DF-ACE-008 | v_ace_account | product_key | Read |"),
    ("| DF-ACC-008 | loan_account | interest_rate | Read |", "| DF-ACE-025 | v_ace_account | interest_rate | Read |"),
    ("| DF-ACC-009 | loan_account | principal_outstanding | Read |", "| DF-ACC-009 | v_ace_account | principal_outstanding | Read (Section B, RWB-ACE-001) |"),
    ("| DF-ACC-010 | loan_account | interest_outstanding | Read |", "| DF-ACC-010 | v_ace_account | interest_outstanding | Read (Section B, RWB-ACE-001) |"),
    ("| DF-ACC-012 | loan_account | total_balance | Read |", "| DF-ACE-020 | v_ace_account | total_balance | Read |"),
    ("| DF-ACC-012 | loan_account | total_balance | Read through the P1 data product interface, with its business date |",
     "| DF-ACE-020 | v_ace_account | total_balance | Read through the P1 data product interface, with its business date |"),
    ("| DF-ACC-014 | loan_account | days_past_due | Read |", "| DF-ACE-018 | v_ace_account | days_past_due | Read |"),
    ("| DF-ACC-018 | loan_account | next_installment_date | Read |", "| DF-ACE-028 | v_ace_account | next_installment_date | Read |"),
    ("| DF-ACC-019 | loan_account | tdr_flag | Read |", "| DF-ACE-031 | v_ace_account | tdr_flag | Read |"),
    ("| DF-ACC-020 | loan_account | last_tdr_date | Read |", "| DF-ACE-030 | v_ace_account | last_tdr_date | Read |"),
    ("| DF-ACC-021 | loan_account | data_as_of | Read |", "| DF-ACE-036 | v_ace_account | data_as_of | Read |"),
    ("| DF-ACC-022 | account_payment | id | Read |", "| DF-ACE-043 | v_ace_payment | payment_code | Read |"),
    ("| DF-ACC-023 | account_payment | account_id | Read |", "| DF-ACE-044 | v_ace_payment | account_key | Read |"),
    ("| DF-ACC-025 | account_payment | payment_date | Read |", "| DF-ACE-045 | v_ace_payment | payment_date | Read |"),
    ("| DF-ACC-026 | account_payment | payment_amount | Read |", "| DF-ACE-046 | v_ace_payment | payment_amount | Read |"),
    ("| DF-COL-002 | collateral | collateral_no | Read |", "| DF-ACE-091 | v_ace_collateral | collateral_no | Read |"),
    ("| DF-COL-003 | collateral | collateral_type | Read |", "| DF-ACE-097 | v_ace_collateral | collateral_type | Read |"),
    ("| DF-COL-004 | collateral | title_doc_no | Read |", "| DF-ACE-197 | v_ace_collateral_detail | title_doc_no | Read |"),
    ("| DF-COL-023 | valuation | appraised_value | Read |", "| DF-ACE-191 | v_ace_valuation | appraised_value | Read |"),
    ("| DF-COL-025 | valuation | appraisal_date | Read |", "| DF-ACE-193 | v_ace_valuation | appraisal_date | Read |"),
    ("| DF-COL-025 | valuation | appraisal_date | Read (X7 collateral event inputs) |", "| DF-ACE-193 | v_ace_valuation | appraisal_date | Read (X7 collateral event inputs) |"),
    ("| DF-PTY-001 | party | id | Read |", "| DF-ACE-056 | v_ace_customer | person_key | Read |"),
    ("| DF-PTY-004 | party | first_name | Read |", "| DF-ACE-057 | v_ace_customer | first_name | Read |"),
    ("| DF-PTY-005 | party | last_name | Read |", "| DF-ACE-058 | v_ace_customer | last_name | Read |"),
    ("| DF-PTY-014 | contact_point | party_id | Read |", "| DF-ACE-077 | v_ace_contact | person_key | Read |"),
    ("| DF-PTY-015 | contact_point | channel | Read |", "| DF-ACE-075 | v_ace_contact | contact_type | Read |"),
    ("| DF-PTY-016 | contact_point | value_token | Read |", "| DF-ACE-078 | v_ace_contact | contact_value | Read |"),
    ("| DF-PTY-016 | contact_point | value_token | Read masked through the owning module's DTO |", "| DF-ACE-078 | v_ace_contact | contact_value | Read masked through the owning module's DTO |"),
    ("| DF-PTY-018 | contact_point | consent_status | Read |", "| DF-EXT-015 | contact_point_ext | consent_given | Read through the P1 interface |"),
    ("| DF-PTY-019 | contact_point | verified_at | Read |", "| DF-EXT-017 | contact_point_ext | verified_at | Read through the P1 interface |"),
    ("| DF-PTY-020 | contact_point | failed_count | Write, through the P1 interface |", "| DF-EXT-018 | contact_point_ext | failed_count | Write, through the P1 interface |"),
    ("| DF-CAS-026 | case_account | account_id | Read |", "| DF-CAS-026 | case_account | account_key | Read |"),
    ("| DF-CAS-004 | recovery_case | primary_customer_id | Read |", "| DF-CAS-004 | recovery_case | primary_person_key | Read |"),
    ("| DF-DOC-100 | signature_request | party_id | Write |", "| DF-DOC-100 | signature_request | person_key | Write |"),
    ("| DF-INT-003 | interaction | party_id | Write, through the ledger writer |", "| DF-INT-003 | interaction | person_key | Write, through the ledger writer |"),
    ("| DF-FIN-004 | proceeds | account_payment_id | Write |", "| DF-FIN-004 | proceeds | payment_code | Write |"),
    # prose
    ("- RWB-E2-001 (case creation from the COLLINS load) is done.", "- RWB-E2-001 (case creation from the ACE data) is done."),
    ("reads the case, accounts, collateral, latest valuation, plan terms and documents through the owning modules' interfaces.",
     "reads the case, accounts, collateral, latest valuation, plan terms and documents through the owning modules' interfaces and the P1 interfaces over the ACE views."),
    ("- The COLLINS load for the business date has passed its checks, or the case list shows its date as stale.",
     "- The ACE batch for the business date is COMPLETE, or the case list shows its date as stale."),
    ("| X5 | Today's COLLINS load has not arrived | The list shows with the stale banner and the date of the data | MSG-P1-001 | AC8 |",
     "| X5 | Today's ACE batch has not arrived | The list shows with the stale banner and the date of the data | MSG-P1-001 | AC8 |"),
    ("Given the COLLINS load of 2026-12-15 has not arrived and the case data is from 2026-12-14",
     "Given the ACE batch of 2026-12-15 has not arrived and the case data is from 2026-12-14"),
    ("Given the total balance comes from the COLLINS load of business date 13 December 2026",
     "Given the total balance comes from the ACE account data of business date 13 December 2026"),
    ("- RWB-E1-052 and RWB-E1-055 are done: generation, the WIN file, the acknowledgment and the INT-15 load run.",
     "- RWB-E1-052 and RWB-E1-055 are done: generation, the WIN file and the acknowledgment run, and ACE ingests the INT-15 proof file."),
    ("6. JOB-09: loads the INT-15 file; a Delivered record sets Delivered and publishes NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07).",
     "6. The proof read: DeliveryResultReader reads the day's proof rows from v_ace_pod by barcode (INT-15 is ingested by ACE); a Delivered record sets Delivered and publishes NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07)."),
    ("| SY-DATALOAD, data load from COLLINS | Runs JOB-10 and the INT-15 step |",
     "| The recovery service identity | Runs JOB-10 and reads the proof rows from v_ace_pod |"),
    ("**Jobs.** JOB-10 WIN outbound notices (daily 16:00) gets two steps: the proof window step first, then the conduct check before each file record. JOB-09 File loads adds the Refused and Undeliverable results to the INT-15 step. Idempotency for each: notice ID and business date; a rerun from SCR-44 skips notices already Unserved, Held or in a file of that date.",
     "**Jobs.** JOB-10 WIN outbound notices (daily 16:00) gets two steps: the proof window step first, then the conduct check before each file record. The INT-15 results are not a Workbench load: ACE ingests them, and DeliveryResultReader takes the Refused and Undeliverable results from v_ace_pod. Idempotency for each: notice ID and business date; a rerun from SCR-44 skips notices already Unserved, Held or in a file of that date."),
    ("- Contact points with consent status are loaded through COLLINS (INT-04).",
     "- Contact points and consent are held in ACE, which receives them from SCBPDM (INT-04)."),
    ("| SY-DATALOAD, data load from COLLINS | Runs JOB-07 |", "| The recovery service identity | Runs JOB-07 |"),
    ("| SY-DATALOAD, data load | Calls the ACE interface and writes the stored plan status through P3 |",
     "| The recovery service identity | Calls the ACE interface and writes the stored plan status through P3 |"),
    ("9. SY-DATALOAD: for a case with a stored plan that ACE no longer returns, keeps the stored status and date and writes a data quality exception for the ACE team.",
     "9. The recovery service identity: for a case with a stored plan that ACE no longer returns, keeps the stored status and date and writes a break for the data steward and the ACE team."),
    ("| X1 | ACE returns no status for a plan the case holds | The case keeps its last known status and date; a data quality exception lists the plan for the ACE team | MSG-P2-008 | AC3 |",
     "| X1 | ACE returns no status for a plan the case holds | The case keeps its last known status and date; a break on the data quality console lists the plan for the ACE team | MSG-P2-008 | AC3 |"),
    ("| X3 | ACE returns a status code not in the plan status list | The status is not stored; a data quality exception with check \"Lists of values\" is written | None | AC5 |",
     "| X3 | ACE returns a status code not in the plan status list | The status is not stored; a break with check \"Lists of values\" is written | None | AC5 |"),
    ("    Then a data quality exception with product \"DP04\" lists plan \"TDR-SYN-0310\" for the ACE team",
     "    Then a break with product \"DP04\" lists plan \"TDR-SYN-0310\" for the ACE team"),
    ("    Then a data quality exception with check \"Lists of values\" names the code \"SUSPENDED\"",
     "    Then a break with check \"Lists of values\" names the code \"SUSPENDED\""),
    ("| RW-DATASTEW, RW-PLATADM | Read the data quality exceptions for the ACE team (Platform administration, R) |",
     "| RW-DATASTEW, RW-PLATADM | Read the breaks for the ACE team (Platform administration, R) |"),
    # Thai test strings to ASCII
    ("\"12 \u0e18\u0e31\u0e19\u0e27\u0e32\u0e04\u0e21 2569\"", "\"12 December 2569 BE\""),
    ("\"2,400,000.00 \u0e1a\u0e32\u0e17\"", "\"2,400,000.00 baht\""),
    ("\"1 \u0e1e\u0e24\u0e28\u0e08\u0e34\u0e01\u0e32\u0e22\u0e19 2569\"", "\"1 December 2569 BE\""),
    ("\"\u0e1e\u0e34\u0e1e\u0e32\u0e01\u0e29\u0e32 \u0e13 \u0e27\u0e31\u0e19\u0e17\u0e35\u0e48 5 \u0e21\u0e35\u0e19\u0e32\u0e04\u0e21 2570\"", "\"Judgment at 5 March 2570 BE\""),
    ("\"1,250,000.00 \u0e1a\u0e32\u0e17 (\u0e2b\u0e19\u0e36\u0e48\u0e07\u0e25\u0e49\u0e32\u0e19\u0e2a\u0e2d\u0e07\u0e41\u0e2a\u0e19\u0e2b\u0e49\u0e32\u0e2b\u0e21\u0e37\u0e48\u0e19\u0e1a\u0e32\u0e17\u0e16\u0e49\u0e27\u0e19)\"", "\"1,250,000.00 baht (one million two hundred fifty thousand baht)\""),
    ("\"10 \u0e18\u0e31\u0e19\u0e27\u0e32\u0e04\u0e21 2569\"", "\"10 December 2569 BE\""),
]

for old, new in pairs:
    c = doc.count(old)
    if c == 0:
        print("MISS:", old[:90])
    else:
        doc = doc.replace(old, new)

# SY-DATALOAD in E2-002 flow only
def fix_e2_002(doc):
    m = re.search(r"(?ms)^## RWB-E2-002 .*?(?=^## RWB-E2-004 )", doc)
    blk = m.group(0)
    blk2 = blk.replace("SY-DATALOAD:", "The recovery service identity:")
    return doc[:m.start()] + blk2 + doc[m.end():]
doc = fix_e2_002(doc)

open(DST, "w", encoding="ascii", newline="\n").write(doc)
print("written", len(doc), "chars")
print("stories", len(re.findall(r"(?m)^## RWB-E2-\d+ ", doc)))
print("Acs", doc.count("  Scenario: "))
print("tests", len(re.findall(r"\| TC-E2-\d{3}-\d{2} \|", doc)))
