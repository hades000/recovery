<!-- source: 06 Data/Recovery Workbench Data Quality and Reconciliation Rules v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Data Quality and Reconciliation Rules v2.xlsx`  
> **Converted from:** XLSX

## Load checks

| Checks on every inbound load |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| 98 checks: seven on each COLLINS and file interface. Tolerances are proposed until the data lead confirms them (DL25). |  |  |  |  |  |  |  |  |
| ID | Interface | Source | Data product | Check | What it tests | Tolerance | If it fails | Owner |
| DQ-001 | INT-01 | Core bank (ALS) | DP01 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-002 | INT-01 | Core bank (ALS) | DP01 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-003 | INT-01 | Core bank (ALS) | DP01 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-004 | INT-01 | Core bank (ALS) | DP01 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-005 | INT-01 | Core bank (ALS) | DP01 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-006 | INT-01 | Core bank (ALS) | DP01 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-007 | INT-01 | Core bank (ALS) | DP01 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-008 | INT-02 | Core bank (ALS) | DP01, DP13 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-009 | INT-02 | Core bank (ALS) | DP01, DP13 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-010 | INT-02 | Core bank (ALS) | DP01, DP13 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-011 | INT-02 | Core bank (ALS) | DP01, DP13 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-012 | INT-02 | Core bank (ALS) | DP01, DP13 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-013 | INT-02 | Core bank (ALS) | DP01, DP13 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-014 | INT-02 | Core bank (ALS) | DP01, DP13 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-015 | INT-04 | SCBPDM | DP02 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-016 | INT-04 | SCBPDM | DP02 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-017 | INT-04 | SCBPDM | DP02 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-018 | INT-04 | SCBPDM | DP02 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-019 | INT-04 | SCBPDM | DP02 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-020 | INT-04 | SCBPDM | DP02 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-021 | INT-04 | SCBPDM | DP02 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-022 | INT-05 | UDP | DP01, DP02 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-023 | INT-05 | UDP | DP01, DP02 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-024 | INT-05 | UDP | DP01, DP02 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-025 | INT-05 | UDP | DP01, DP02 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-026 | INT-05 | UDP | DP01, DP02 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-027 | INT-05 | UDP | DP01, DP02 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-028 | INT-05 | UDP | DP01, DP02 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-029 | INT-06 | AAL | To confirm | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-030 | INT-06 | AAL | To confirm | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-031 | INT-06 | AAL | To confirm | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-032 | INT-06 | AAL | To confirm | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-033 | INT-06 | AAL | To confirm | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-034 | INT-06 | AAL | To confirm | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-035 | INT-06 | AAL | To confirm | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-036 | INT-07 | EFS | DP05 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-037 | INT-07 | EFS | DP05 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-038 | INT-07 | EFS | DP05 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-039 | INT-07 | EFS | DP05 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-040 | INT-07 | EFS | DP05 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-041 | INT-07 | EFS | DP05 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-042 | INT-07 | EFS | DP05 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-043 | INT-08 | COLLINS models | DP11 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-044 | INT-08 | COLLINS models | DP11 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-045 | INT-08 | COLLINS models | DP11 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-046 | INT-08 | COLLINS models | DP11 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-047 | INT-08 | COLLINS models | DP11 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-048 | INT-08 | COLLINS models | DP11 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-049 | INT-08 | COLLINS models | DP11 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-050 | INT-09 | LIT | DP07 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-051 | INT-09 | LIT | DP07 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-052 | INT-09 | LIT | DP07 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-053 | INT-09 | LIT | DP07 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-054 | INT-09 | LIT | DP07 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-055 | INT-09 | LIT | DP07 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-056 | INT-09 | LIT | DP07 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-057 | INT-10 | CCMS | DP06 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-058 | INT-10 | CCMS | DP06 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-059 | INT-10 | CCMS | DP06 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-060 | INT-10 | CCMS | DP06 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-061 | INT-10 | CCMS | DP06 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-062 | INT-10 | CCMS | DP06 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-063 | INT-10 | CCMS | DP06 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-064 | INT-11 | SVAF | DP06 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-065 | INT-11 | SVAF | DP06 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-066 | INT-11 | SVAF | DP06 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-067 | INT-11 | SVAF | DP06 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-068 | INT-11 | SVAF | DP06 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-069 | INT-11 | SVAF | DP06 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-070 | INT-11 | SVAF | DP06 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-071 | INT-12 | AMIS | DP06 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-072 | INT-12 | AMIS | DP06 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-073 | INT-12 | AMIS | DP06 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-074 | INT-12 | AMIS | DP06 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-075 | INT-12 | AMIS | DP06 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-076 | INT-12 | AMIS | DP06 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-077 | INT-12 | AMIS | DP06 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-078 | INT-13 | RPS | DP06 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-079 | INT-13 | RPS | DP06 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-080 | INT-13 | RPS | DP06 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-081 | INT-13 | RPS | DP06 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-082 | INT-13 | RPS | DP06 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-083 | INT-13 | RPS | DP06 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-084 | INT-13 | RPS | DP06 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-085 | INT-15 | WIN | DP07 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-086 | INT-15 | WIN | DP07 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-087 | INT-15 | WIN | DP07 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-088 | INT-15 | WIN | DP07 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-089 | INT-15 | WIN | DP07 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-090 | INT-15 | WIN | DP07 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-091 | INT-15 | WIN | DP07 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |
| DQ-092 | INT-16 | GL | DP13 | Business date | The load is for the expected business date and is not a repeat | None | Refuse the load | Data steward |
| DQ-093 | INT-16 | GL | DP13 | Structure | Every field present with its type and length | None | Refuse the load | Data steward |
| DQ-094 | INT-16 | GL | DP13 | Control total | Record count and balance total match the trailer | Zero | Refuse the load | Data steward |
| DQ-095 | INT-16 | GL | DP13 | Keys | Every record has its key; no key twice | None | Refuse the load | Data steward |
| DQ-096 | INT-16 | GL | DP13 | References | Each account, customer or asset can be matched | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-097 | INT-16 | GL | DP13 | Lists of values | Each code maps to its list | Up to 0.5 percent held | Hold the records; refuse above the tolerance | Data steward |
| DQ-098 | INT-16 | GL | DP13 | Movement | Count and balance within the expected change from the previous load | Plus or minus 10 percent | Load and alert the data steward | Data steward |

## Reconciliations

| Reconciliations |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Each compares a source to the Workbench after the load. |  |  |  |  |  |  |
| ID | Source side | Workbench side | Compared on | Tolerance | When | Break goes to |
| REC-01 | Accounts at 90 days past due in the ALS load | Open recovery cases | Count by product | Zero unexplained | Daily | Break list to the data steward |
| REC-02 | Balances in the ALS load | Balances on the case accounts | Sum by product | Zero | Daily | Break list |
| REC-03 | Approved treatments | Bookings in the next ALS load | Count and amount | Zero after two days | Daily | Task to the officer |
| REC-04 | Payments in the ALS load | Proceeds matched to cases | Count and amount | Unmatched held on the exception list | Daily | Reconciliation agent; Credit Administration |
| REC-05 | Notices sent to WIN | Barcodes returned | Count | Zero after three days | Daily | Platform administrator |
| REC-06 | Write-offs approved | GL postings | Count and amount | Zero | Monthly | Credit Administration |
| REC-07 | Assets taken on | AMIS and RPS records | Count | Zero | Weekly | Head of NPA |
| REC-08 | Decision log copy | Live decision log | Count and last hash | Zero | Nightly | Data steward |

## Quality measures

| Data quality measures |  |  |
|---|---|---|
| Reported daily on the data quality console. |  |  |
| Measure | Meaning | Target |
| Completeness | Mandatory fields filled | 99.9 percent |
| Validity | Codes in their lists | 99.5 percent |
| Timeliness | Loads on time | 99 percent of days |
| Accuracy | Reconciliation breaks cleared within one day | 100 percent |
| Uniqueness | One case per customer per product | 100 percent |
