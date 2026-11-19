import glob, re, os, sys, json

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 Story Files v6")
DST = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.md")

files = sorted(glob.glob(os.path.join(SRC, "RWB*.md")))
assert len(files) == 71, len(files)

# ---------- targeted ACE re-base corrections ----------
FIX = {
"RWB-E1-025": [
 ("| Depends on | RWB-E1-012 |", "| Depends on | RWB-E1-069 |"),
 ("- RWB-E1-012 is done: the local trackers are listed with their owners, so the types in the current trackers are known.",
  "- RWB-E1-069 is done: the 30 ACE views are in place, so the source fields that each document type can carry are known."),
 ("Needs only the tracker list (RWB-E1-012) and the P4 reference load endpoint",
  "Needs only the ACE view list (RWB-E1-069) and the P4 reference load endpoint"),
],
"RWB-E1-046": [
 ("| Depends on | RWB-E1-012 |", "| Depends on | RWB-E1-001, RWB-E1-069 |"),
 ("- RWB-E1-012 is done: recovery data comes only from the recovery tables.",
  "- RWB-E1-001 and RWB-E1-069 are done: the recovery tables exist and recovery data comes only through the 30 ACE views."),
 ("Needs only the recovery tables (RWB-E1-012) and the P4 reference load path",
  "Needs only the recovery tables (RWB-E1-001, RWB-E1-069) and the P4 reference load path"),
],
"RWB-E1-058": [
 ("| Depends on | RWB-E1-001, RWB-E1-003, RWB-E1-037 |", "| Depends on | RWB-E1-001, RWB-E1-069, RWB-E1-037 |"),
 ("- RWB-E1-001 (recovery tables) and RWB-E1-003 (account and arrears load) are done, so synthetic cases exist in DEV and SIT.",
  "- RWB-E1-001 (recovery tables) and RWB-E1-069 (read-only ACE views) are done, so synthetic cases and ACE source data exist in DEV and SIT."),
 ("Needs only the recovery tables (RWB-E1-001, RWB-E1-003) and the masking service (RWB-E1-037)",
  "Needs only the recovery tables (RWB-E1-001, RWB-E1-069) and the masking service (RWB-E1-037)"),
],
"RWB-E1-066": [
 ("- Done when: the tests in section 16 pass and the EFS history load (RWB-E1-004) writes through append().",
  "- Done when: the tests in section 16 pass and the ACE collections history read through `v_ace_efs_action` writes through append()."),
],
"RWB-TE-004": [
 ("| DF-PTY-001 to DF-PTY-012 | party | all fields | Write |\n| DF-PTY-013 to DF-PTY-020 | contact_point | all fields | Write |\n| DF-ACC-001 to DF-ACC-021 | loan_account | all fields | Write |\n| DF-ACC-022 to DF-ACC-028 | account_payment | all fields | Write |\n| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |\n| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |\n| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |\n| DF-REF-105 | sys_fields | is_personal | Read |",
  "| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |\n| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |\n| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |\n| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |\n| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |\n| DF-EXT-001 to DF-EXT-012 | party_ext | all fields | Write |\n| DF-EXT-013 to DF-EXT-026 | contact_point_ext | all fields | Write |\n| DF-REF-105 | sys_fields | is_personal | Read |"),
 ("the manifest lists 28,119 loan accounts", "the manifest lists 28,119 case accounts"),
 ("Then every column tagged is_personal in party and contact_point holds a token or a masked value",
  "Then every column tagged is_personal in interaction and document_field holds a token or a masked value"),
 ("Then each party token joins to the same case_party and loan account rows as in the extract",
  "Then each person key joins to the same case_party and case_account rows as in the extract"),
 ("Given party row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in id_no_token",
  "Given interaction row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in summary"),
 ("check \"unmasked value in party.id_no_token\"", "check \"unmasked value in interaction.summary\""),
 ("Given the loan_account file holds 28,118 rows", "Given the case_account file holds 28,118 rows"),
 ("check \"Control totals loan_account 28,118 against 28,119\"", "check \"Control totals case_account 28,118 against 28,119\""),
 ("keeps balances, dates and keys unchanged so counts and reconciliations behave as in production", "keeps dates, keys and row counts unchanged so counts and reconciliations behave as in production"),
 ("row count and balance totals per table", "row count per table"),
 ("control totals (row count and balance sum)", "control totals (row count per table)"),
 ("rows and balance totals per table", "rows per table"),
 ("Row count or balance total differs from the manifest", "Row count differs from the manifest"),
 ("with total_balance sums per product", "with row counts per product"),
 ("Then balances keep their shape: the count and the total_balance sum per product equal the manifest", "Then the row counts keep their shape: the count per table and per product equals the manifest"),
 ("| BR4 | Balances, dates and keys are not masked; counts and totals equal the manifest |", "| BR4 | Dates and keys are not masked; counts equal the manifest |"),
 ("Injected value with a valid check digit in party row 4,512", "Injected value with a valid check digit in interaction row 4,512"),
 ("loan_account file with 28,118 rows", "case_account file with 28,118 rows"),
],
"RWB-TE-011": [
 ("| DF-PTY-002 | party | cif_no | Read (definition) |\n| DF-PTY-004 | party | first_name | Read (definition) |\n| DF-PTY-005 | party | last_name | Read (definition) |\n| DF-PTY-007 | party | id_no_token | Read (definition) |\n| DF-PTY-008 | party | date_of_birth | Read (definition) |\n| DF-PTY-010 | party | vulnerable_flag | Read (definition) |\n| DF-PTY-011 | party | deceased_flag | Read (definition) |\n| DF-PTY-012 | party | bankruptcy_flag | Read (definition) |\n| DF-PTY-016 | contact_point | value_token | Read (definition) |",
  "| DF-ACE-055 | v_ace_customer | cif_no | Read (definition) |\n| DF-ACE-057 | v_ace_customer | first_name | Read (definition) |\n| DF-ACE-058 | v_ace_customer | last_name | Read (definition) |\n| DF-ACE-073 | v_ace_customer | id_no_masked | Read (definition) |\n| DF-ACE-059 | v_ace_customer | date_of_birth | Read (definition) |\n| DF-EXT-002 | party_ext | vulnerable | Read (definition) |\n| DF-ACE-061 | v_ace_customer | deceased_flag | Read (definition) |\n| DF-EXT-004 | party_ext | bankruptcy | Read (definition) |\n| DF-ACE-078 | v_ace_contact | contact_value | Read (definition) |"),
 ("marks first_name, last_name, cif_no, id_no_token, date_of_birth, value_token, summary and field_value as personal",
  "marks first_name, last_name, cif_no, id_no_masked, date_of_birth, contact_value, summary and field_value as personal"),
 ("that writes party.getFirstName()", "that writes customer.getFirstName()"),
 ("a log statement that writes the object \"party\" of type PartyEntity", "a log statement that writes the object \"customer\" of type CustomerEntity"),
 ("whose \"idNoToken\" holds", "whose \"idNoMasked\" holds"),
 ("the dictionary marks loan_account.contract_no as personal", "the dictionary marks v_ace_account.contract_no as personal"),
 ("console.log(party.lastName)", "console.log(customer.lastName)"),
 ("message \"No case for \" + party.getCifNo()", "message \"No case for \" + customer.getCifNo()"),
 ("ContactPointEntity includes value_token in its text form", "ContactEntity includes contact_value in its text form"),
 ("Then the build fails with rule PDPA-TOSTRING for value_token", "Then the build fails with rule PDPA-TOSTRING for contact_value"),
 ("ContactPointEntity text form with value_token", "ContactEntity text form with contact_value"),
],
}

# stale schema citation, every story
GLOBAL = [("Physical Schema v4.sql", "Physical Schema v5.sql")]

# Thai text in the v6 files, made ASCII for the v8 set
NONASCII = [
 ("\"\u0e1c\u0e39\u0e49\u0e04\u0e49\u0e33\u0e17\u0e14\u0e2a\u0e2d\u0e1a \u0e2b\u0e19\u0e36\u0e48\u0e07\"", "\"SYN GUARANTOR ONE\""),
 ("\"\u0e1c\u0e39\u0e49\u0e04\u0e49\u0e33\u0e17\u0e14\u0e2a\u0e2d\u0e1a\"", "\"SYN GUARANTOR\""),
 ("\"\u0e44\u0e21\u0e48\u0e21\u0e35\u0e04\u0e33\u0e19\u0e35\u0e49\"", "\"NO SUCH TEXT\""),
 ("Regulation \u0e01\u0e01\u0e04.540031 as amended by \u0e01\u0e01\u0e04.690070", "Regulation 540031 as amended by Regulation 690070"),
 ("credit approval regulation \u0e23\u0e1a.-\u0e01\u0e2a.450032", "credit approval regulation 450032"),
 ("\"1 \u0e18\u0e31\u0e19\u0e27\u0e32\u0e04\u0e21 2569\"", "\"1 December 2569 BE\""),
 ("\"15 \u0e18\u0e31\u0e19\u0e27\u0e32\u0e04\u0e21 2569\"", "\"15 December 2569 BE\""),
 ("\"32 \u0e18\u0e31\u0e19\u0e27\u0e32\u0e04\u0e21 2569\"", "\"32 December 2569 BE\""),
 ("\"20 \u0e21\u0e01\u0e23\u0e32\u0e04\u0e21 2570\"", "\"20 January 2570 BE\""),
]

def section(t, n):
    m = re.search(r"^## %d\. .+?$(.*?)(?=^## \d+\. |\Z)" % n, t, re.M | re.S)
    return m.group(1) if m else ""

def table_rows(sec):
    out = []
    for l in sec.splitlines():
        s = l.strip()
        if s.startswith("|") and s.endswith("|"):
            out.append([c.strip() for c in s.strip("|").split("|")])
    return out

def ac_count(t):
    g = re.search(r"```gherkin\n(.*?)```", t, re.S)
    return len(re.findall(r"(?m)^  Scenario: AC\d+", g.group(1))) if g else 0

def tc_count(t):
    return len([r for r in table_rows(section(t, 16)) if r and re.match(r"TC-", r[0])])

sections = []
rows = []
for f in files:
    raw = open(f, encoding="utf-8-sig").read().replace("\r\n", "\n")
    title = re.match(r"^# (.+)$", raw.splitlines()[0]).group(1)
    key = title.split()[0]
    for old, new in GLOBAL:
        raw = raw.replace(old, new)
    for old, new in NONASCII:
        raw = raw.replace(old, new)
    for old, new in FIX.get(key, []):
        if old not in raw:
            print("MISS", key, old[:80]); sys.exit(1)
        raw = raw.replace(old, new)
    # metadata table onwards
    idx = raw.index("| Item | Value |")
    body = raw[idx:].rstrip("\n")
    body = re.sub(r"(?m)^## (\d+\. )", r"### \1", body)
    sections.append("## " + title + "\n\n" + body)
    # index row
    meta = {}
    for l in body.split("\n"):
        m = re.match(r"^\| ([A-Za-z][^|]*) \| (.+) \|$", l)
        if m and m.group(1).strip() not in meta:
            meta[m.group(1).strip()] = m.group(2).strip()
    rows.append((key, title[len(key)+1:], meta.get("Module", ""), meta.get("Requirement IDs", ""), meta.get("Depends on", "")))
    body_acs = ac_count(raw); body_tcs = tc_count(raw)

acs = sum(ac_count(open(f, encoding="utf-8-sig").read()) for f in files)
tcs = sum(tc_count(open(f, encoding="utf-8-sig").read()) for f in files)
print("ACS", acs, "TCS", tcs, "SECTIONS", len(sections))

import collections
mods = collections.Counter()
for r in rows:
    m = r[2]
    if m.startswith("P4"): m = "P4 Access and administration"
    mods[m] += 1
order = ["P1 Recovery data engine","P2 Integration","P3 Case and workflow","P4 Access and administration",
         "P5 Document hub","P6 Communications","P7 Decision center and log","P9 Reporting","P10 Agent runtime"]
modtxt = ", ".join("%s (%d)" % (m.split()[0], mods[m]) for m in order if mods[m])

head = """# Recovery Workbench user stories, Epic 1

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Stories | 71 |
| Acceptance criteria | %d |
| Test cases | %d |
| Modules | %s |

Release 30 November 2026. Epic 1 status: confirmed. This version is re-based on decision D-RCV-35 and ADR-010, agreed on 15 November 2026, the ACE re-base: the Workbench takes no inbound source data, ACE ingests every source, and the recovery module reads ACE only through the 30 SELECT-only `recovery.v_ace_*` views built by RWB-E1-069, 16 Section A views now and 14 Section B views once RWB-ACE-001 lands (DL43). The eight data load, inventory and retirement stories removed by the re-base, RWB-E1-003, RWB-E1-004, RWB-E1-005, RWB-E1-006, RWB-E1-009, RWB-E1-010, RWB-E1-012 and RWB-E1-051, are not in this file. The 11 technical enabler stories for Epic 1 are included.

Each story is written for build: the business rationale, preconditions, the main flow and its exception paths, acceptance criteria in Gherkin, business rules, state transitions, authority, the fields it reads and writes with their BR Field IDs, the contract, the solution plan, messages, screens, test cases and traceability to the business requirements. Field IDs are those in the Logical Data Model and Data Dictionary and Physical Schema v5, endpoints those in the API Specification, messages those in the Error and Message Standard and requirement IDs those in the Business Requirements. The same stories are also supplied one file per story, to hand to a coding agent with the module specifications.

| Key | Title | Module | Requirements | Depends on |
|---|---|---|---|---|
""" % (acs, tcs, modtxt)

head += "\n".join("| %s | %s | %s | %s | %s |" % r for r in rows) + "\n"
doc = head.rstrip("\n") + "\n\n" + "\n---\n\n".join(s.rstrip("\n") for s in sections) + "\n\n---\n"

bad = [(i+1, ascii(l)) for i, l in enumerate(doc.split("\n")) if any(ord(c) > 127 for c in l)]
print("NONASCII", len(bad))
for b in bad[:5]: print(b)
open(DST, "w", encoding="ascii", newline="\n").write(doc)
print("written", len(doc), "chars", doc.count("\n"), "lines")
print("sections in doc", len(re.findall(r"(?m)^## RWB-", doc)))
print("acs in doc", len(re.findall(r"(?m)^  Scenario: AC", doc)))
print("tcs in doc", len(re.findall(r"(?m)^\| TC-", doc)))
