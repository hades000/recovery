import os

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
P3 = os.path.join(ROOT, r"_work\staging\Recovery Workbench TSD P3 Case and workflow v2.md")
P8 = os.path.join(ROOT, r"_work\staging\Recovery Workbench TSD P8 Payments and posting v2.md")


def edit(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        assert old in s, "NOT FOUND in %s: %s" % (os.path.basename(path), old[:90])
        s = s.replace(old, new, 1)
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    bad = sorted({c for c in s if ord(c) > 127})
    print(os.path.basename(path), len(s), "non-ascii", bad)


head3_old = """| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
"""
head3_new = """| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
| Decision | D-RCV-35 (U1 to U5), ADR-010 |

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Module specification with the case, queue, task, timer and interaction model |
| 3 | 15 November 2026 | D-RCV-35: the case, its accounts and its parties link to ACE by business key. `primary_customer_id`, `account_id`, `party_id` and `contact_point_id` become `primary_person_key`, `account_key`, `person_key` and `contact_key`; no foreign key into ACE |
"""
edit(P3, [
    ("Henka Group, 28 October 2026.", "Henka Group, 15 November 2026."),
    ("| Document ID | P3-RWB-TSD-v2 |", "| Document ID | P3-RWB-TSD-v3 |"),
    (head3_old, head3_new),
    ("It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.",
     "It reaches other modules only through their published interfaces, and it reads ACE source data only through `recovery.v_ace_*` views."),
    ("""### T3.1 Object and field definitions

**recovery_case** (EXTEND ACE Case). One recovery case per customer per product, from 90 days past due to close.""",
     """### T3.1 Object and field definitions

The case is Workbench-owned. The account and the party are ACE records: the case links to them by business key and reads their attributes from `v_ace_account` and `v_ace_customer`. A link carries no foreign key, because ACE cascades deletes on `account` and a cascade would delete case history.

**recovery_case** (EXTEND ACE Case). One recovery case per customer per product, from 90 days past due to close."""),
    ("| DF-CAS-004 | primary_customer_id | CROSS_REF | uuid | Yes | None | Workbench |",
     "| DF-CAS-004 | primary_person_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_customer.person_key` |"),
    ("| DF-CAS-026 | account_id | CROSS_REF | uuid | Yes | None | Workbench |",
     "| DF-CAS-026 | account_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_account.account_key` |"),
    ("| DF-CAS-032 | party_id | CROSS_REF | uuid | Yes | None | Workbench |",
     "| DF-CAS-032 | person_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_customer.person_key` |"),
    ("| DF-CAS-057 | account_id | CROSS_REF | uuid | Yes | None | Workbench |",
     "| DF-CAS-057 | account_key | TEXT | varchar(255) | Yes | None | ACE `v_ace_account.account_key` |"),
    ("| DF-INT-003 | party_id | CROSS_REF | uuid | No | None | Workbench |",
     "| DF-INT-003 | person_key | TEXT | varchar(255) | No | None | ACE `v_ace_customer.person_key` |"),
    ("| DF-INT-022 | contact_point_id | CROSS_REF | uuid | No | None | Workbench |",
     "| DF-INT-022 | contact_key | TEXT | varchar(255) | No | None | ACE `v_ace_contact.contact_key` (composite `contact_type:key`) |"),
    ("""| recovery_case | primary_customer_id | party | Many to 1 |""",
     """| recovery_case | primary_person_key | v_ace_customer | Many to 1; business key, no foreign key |"""),
    ("""| case_account | account_id | loan_account | Many to 1 |""",
     """| case_account | account_key | v_ace_account | Many to 1; business key, no foreign key |"""),
    ("""| case_party | party_id | party | Many to 1 |""",
     """| case_party | person_key | v_ace_customer | Many to 1; business key, no foreign key |"""),
    ("""| interaction | party_id | party | Many to 0 or 1 |""",
     """| interaction | person_key | v_ace_customer | Many to 0 or 1; business key, no foreign key |"""),
    ("""| interaction | contact_point_id | contact_point | Many to 0 or 1 |""",
     """| interaction | contact_key | v_ace_contact | Many to 0 or 1; business key, no foreign key |"""),
    ("""| case_entry_exclusion | account_id | loan_account | Many to 1 |""",
     """| case_entry_exclusion | account_key | v_ace_account | Many to 1; business key, no foreign key |"""),
])

head8_old = """| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
"""
head8_new = """| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |
| Decision | D-RCV-35 (U1 to U5), ADR-010 |

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Module specification with proceeds matching against the account payment copy and the inbound GL file |
| 3 | 15 November 2026 | D-RCV-35: `proceeds.account_payment_id` becomes `payment_code`, read from `v_ace_payment`; the GL write-off is read from `v_ace_write_off`; INT-02 and INT-16 are owned by ACE ingestion; the SY-DATALOAD actor is removed |
"""
edit(P8, [
    ("Henka Group, 28 October 2026.", "Henka Group, 15 November 2026."),
    ("| Document ID | P8-RWB-TSD-v2 |", "| Document ID | P8-RWB-TSD-v3 |"),
    (head8_old, head8_new),
    ("It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.",
     "It reaches other modules only through their published interfaces, and it reads payments and GL postings only through `recovery.v_ace_payment` and `recovery.v_ace_write_off`."),
    ("""### T3.1 Object and field definitions

**proceeds** (NEW). Money received on a case and what it was matched to.""",
     """### T3.1 Object and field definitions

The proceeds record is Workbench-owned. The payment it matches is an ACE record: the link is `payment_code`, the business key of `v_ace_payment`, with no foreign key. A payment that ACE has not yet ingested cannot be matched; the proceeds row waits in UNMATCHED and shows the last ACE business date.

**proceeds** (NEW). Money received on a case and what it was matched to."""),
    ("| DF-FIN-004 | account_payment_id | CROSS_REF | uuid | No | None | Workbench |",
     "| DF-FIN-004 | payment_code | TEXT | varchar(255) | No | None | ACE `v_ace_payment.payment_code` |"),
    ("""| proceeds | account_payment_id | account_payment | Many to 0 or 1 |""",
     """| proceeds | payment_code | v_ace_payment | Many to 0 or 1; business key, no foreign key |"""),
    ("""| INT-02 | Core bank (ALS) | In | COLLINS batch | Daily, end of day |
| INT-03 | Core bank (ALS) | Out | Booked by the officer; confirmed on the next day's load | As approved |
| INT-16 | GL | In | File load | Monthly |""",
     """| INT-02 | Core bank (ALS) | In, into ACE | ACE ingestion (ACE team); the Workbench reads `v_ace_payment` | Daily, end of day |
| INT-03 | Core bank (ALS) | Out | Booked by the officer; confirmed on the next ACE batch through `v_ace_account` | As approved |
| INT-16 | GL | In, into ACE | ACE ingestion (ACE team); the Workbench reads `v_ace_write_off` | Monthly |"""),
    ("""| SY-DATALOAD Data load from COLLINS | U |
""", ""),
])
