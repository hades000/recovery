import io, json, sys

p = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\directive\mp\out\RWB-ITG-E1002-ITG.md"
s = io.open(p, encoding="utf-8", newline=None).read()

edits = []

edits.append((
"""    Then the case and its case_account link are unchanged

  Scenario: AC11 Access to the ReconciliationWorkflow run listing is refused for a role without the right (from TC-E1-002-11-ITG)
    Given RW-CASEOWN signs in with a role that does not include the ReconciliationWorkflow run listing
    When RW-CASEOWN calls the ReconciliationWorkflow run listing on the rwb-source-data base
    Then the call is refused with 403 and the error envelope carries MSG-P4-002 "You cannot {action} here. Your role does not include it."

  Scenario: AC12 JOB-04 runs as an event-started workflow and reads the list through the rwb-case contract (new, D-RCV-60)""",
"""    Then the case and its case_account link are unchanged

  Scenario: AC12 JOB-04 runs as an event-started workflow and reads the list through the rwb-case contract (new, D-RCV-60)"""))

edits.append((
"| X8 | A role without the right lists the JOB-04 runs | 403 with the error envelope | MSG-P4-002 | AC11, AC16 |",
"| X8 | A role without the right lists the JOB-04 runs | 403 with the error envelope | MSG-P4-002 | AC16 |"))

edits.append((
"""| TC-E1-002-11-ITG | AC11, Access | Integration | RW-CASEOWN calls the ReconciliationWorkflow run listing on the rwb-source-data base; refused with MSG-P4-002 |
| Not specified in the source documents (NEWAC-RWB-ITG-E1002-ITG-AC16) | AC16, Access | Integration | RW-CASEOWN with a role without the right lists the JOB-04 runs on the rwb-source-data base; refused with 403 and MSG-P4-002 |
| Not specified in the source documents (NEWAC-RWB-ITG-E1002-ITG-AC17) | AC17, Boundary | Integration | Boundary check of the AC12 to AC14 run: one hop per call, no other service's tables read, no lake path written |""",
"""| TC-E1-002-11-ITG | AC16, Access | Integration | RW-CASEOWN calls the ReconciliationWorkflow run listing on the rwb-source-data base; refused with MSG-P4-002 |
| TC-ITG-E1002-06 | AC17, Boundary | Integration | Boundary check of the AC12 to AC14 run: one hop per call, no other service's tables read, no lake path written |"""))

edits.append((
"""  Scenario: AC16 A role without the right lists the JOB-04 runs is refused (new, D-RCV-60)
    Given RW-CASEOWN signs in with a role that does not include the ReconciliationWorkflow run listing
    When RW-CASEOWN lists the JOB-04 runs on the rwb-source-data base""",
"""  Scenario: AC16 A role without the right lists the ReconciliationWorkflow runs is refused (new, D-RCV-60)
    Given RW-CASEOWN signs in with a role that does not include the ReconciliationWorkflow run listing
    When RW-CASEOWN lists the ReconciliationWorkflow runs on the rwb-source-data base"""))

edits.append((
"The parameters and reference data the run reads are the rwb-case contracts (DP-06, DP-07), the topic and event names come from the naming library (DP-14), the schema objects arrive through the P1 Flyway sequence (DP-15) and the account and arrears facts come from the ACE views read by rwb-source-data alone (DP-05). The target read operation by which rwb-case serves the list that rwb-source-data builds is `GET /api/recovery/case/v1/cases` and `GET /api/recovery/case/v1/queues/{queueId}/cases` on the rwb-case base, and the daily extract reaches rwb-reporting through the rwb-integration activity `deliverFile` on queue `rwb-integration` with a manifest of fileId, batchId, sha256 and record count, with `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` on `rwb.integration.events.v1` and no data lake path (GAP-0335, resolved at the wave-1 contract review).",
"The parameters and reference data the run reads are the rwb-case contracts (DP-06, DP-07), the topic and event names come from the naming library (DP-14), the schema objects arrive through the P1 Flyway sequence (DP-15) and the account and arrears facts come from the ACE views read by rwb-source-data alone (DP-05). What no source states is the target read operation by which rwb-case serves the list that rwb-source-data builds, and how the daily extract reaches rwb-reporting once the data lake is removed: Not specified in the source documents (GAP-0335; ASM-0429). The story proves the two operations that exist today and records the choice as an assumption, so a change of operation is one contract edit and one test change."))

edits.append((
"The five legacy criteria are carried unchanged, including their lake and Power BI wording, because they are the legacy proof; the removed data lake is replaced by the delivery of 12.3 and 12.4 to rwb-reporting, and AC12 to AC15 prove that replacement on the real services.",
"The five legacy criteria are carried with their values and their lake and Power BI wording, because they are the legacy proof; their setup lines now read through the rwb-source-data contract, the removed data lake is replaced by the delivery of 12.3 and 12.4 to rwb-reporting, and AC12 to AC15 prove that replacement on the real services."))

for i, (old, new) in enumerate(edits, 1):
    c = s.count(old)
    print(i, "count", c)
    if c != 1:
        print("  OLD:", repr(old[:160]))
    s = s.replace(old, new, 1)

print("remaining AC11 refs:")
for line in s.splitlines():
    if "AC11" in line:
        print("  ", line[:200])
print("AC16 refs:")
for line in s.splitlines():
    if "AC16" in line:
        print("  ", line[:200])
print("AC17 refs:")
for line in s.splitlines():
    if "AC17" in line:
        print("  ", line[:200])
print("TC-ITG-E1002-05/06 refs:")
for line in s.splitlines():
    if "TC-ITG-E1002-0" in line:
        print("  ", line[:200])

