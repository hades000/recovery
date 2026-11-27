import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import lint

p = Path(__file__).resolve().parents[1] / "out" / "RWB-S4-E5009-APP.md"
t = p.read_text(encoding="utf-8")

big_old = """| TC-E5-009-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-009-07 | Access | Component | AC5: a role without the Litigation right is refused with MSG-P4-002 before any change |
| TC-E5-009-08 | Boundary | Pipeline | AC6: a statement reaching a protected object fails the boundary test and the build |
| TC-E5-009-09 | Business rules | Component | AC7: only rwb_litigation evaluates the rules and no other owner's row is written or joined |
| TC-E5-009-10 | Business rules | Component | AC8: the decision record holds the rule ID and package version before any change |
| TC-E5-009-11 | Idempotency | Component | AC9: the same signal twice writes once and the repeat is counted |
| TC-E5-009-12 | Timer | Component | AC10: the partner clock is 2 working days from the calendar in force |
| TC-E5-009-13 | Data | Component | AC11: no person data enters the decision record, a log or the workflow input |
| TC-E5-009-14 | Breach | Component | AC12: R-LIT-28 marks the breach and answers FIRM_BREACHED_SLA when the clock expires |
| TC-E5-009-15 | Activity | Component | AC13: a consumed contract that does not answer inside 2 s or whose breaker is open is retried and writes nothing |
| TC-E5-009-16 | Activity | Component | AC14: a failed consumed call writes nothing; Not specified in the source documents (NEWAC-RWB-S4-E5009-APP-AC11) |
| TC-E5-009-17 | Status change | Component | AC15: a case state the rule does not allow is refused with 409 and nothing changes |
| TC-E5-009-18 | Access | Component | AC16: an unknown firm or a case outside its state is answered with an error and nothing is written |
| TC-E5-009-19 | Idempotency | Component | AC17: a replay with the same idempotency key returns the stored answer and writes nothing again |
| TC-E5-009-06 | Principle 5 | NFR | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E5-009-07 | Section 12 operations, events and activities | Contract | Not specified in the source documents (DOR-RWB-S4-E5009-APP-12) |
| TC-E5-009-08 | Section 12.7 tables (ASM-3438) | Component | No statement outside `rwb_litigation`, no `v_ace_*` read, no write to another schema |"""

big_new = """| TC-E5-009-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-009-06 | Principle 5 | NFR | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E5-009-07 | AC5 | Component | A role without the Litigation right is refused with MSG-P4-002 before any change |
| TC-E5-009-08 | AC6 | Pipeline | A statement reaching a protected object fails the boundary test and the build |
| TC-E5-009-09 | AC7 | Component | Only rwb_litigation evaluates the rules and no other owner's row is written or joined |
| TC-E5-009-10 | AC8 | Component | The decision record holds the rule ID and package version before any change |
| TC-E5-009-11 | AC9 | Component | The same signal twice writes once and the repeat is counted |
| TC-E5-009-12 | AC10 | Component | The partner clock is 2 working days from the calendar in force |
| TC-E5-009-13 | AC11 | Component | No person data enters the decision record, a log or the workflow input |
| TC-E5-009-14 | AC12 | Component | R-LIT-28 marks the breach and answers FIRM_BREACHED_SLA when the clock expires |
| TC-E5-009-15 | AC13 | Component | A consumed contract that does not answer inside 2 s or whose breaker is open is retried and writes nothing |
| TC-E5-009-16 | AC14 | Component | A failed consumed call writes nothing; Not specified in the source documents (NEWAC-RWB-S4-E5009-APP-AC11) |
| TC-E5-009-17 | AC15 | Component | A case state the rule does not allow is refused with 409 and nothing changes |
| TC-E5-009-18 | AC16 | Component | A call without a valid credential, by a role without the right or for an unknown firm is answered with 401, 403 or 404 and nothing is written |
| TC-E5-009-19 | AC17 | Component | A replay with the same idempotency key returns the stored answer and writes nothing again |
| TC-E5-009-20 | Section 12 operations, events and activities | Contract | Not specified in the source documents (DOR-RWB-S4-E5009-APP-12) |
| TC-E5-009-21 | Section 12.7 tables (ASM-3438) | Component | No statement outside `rwb_litigation`, no `v_ace_*` read, no write to another schema |"""

ac15_old = "    Given the case is not in FIRM_SELECTION for R-LIT-24 or in FIRM_ESCALATED for R-LIT-26"
ac15_new = "    Given the case is not in FIRM_SELECTION for R-LIT-24, or not in FIRM_ESCALATED for R-LIT-26"

ac16_old = """  Scenario: AC16 A call to an unknown firm or a case outside its state is answered with an error and writes nothing (X4)
    Given the rwb-partner contract mock returns no firm LF-2026-0009 in the caller's scope
    When the firm-instruction step reads the firm
    Then the read is answered with 404 or 409 as section 5 X4 states
    Then the step stops and nothing is written
    Then the answer to a call without a valid credential is Not specified in the source documents (NEWAC-RWB-S4-E5009-APP-AC8)
    Then the answer to a role without the Litigation right is refused with MSG-P4-002 as in AC5"""

ac16_new = """  Scenario: AC16 Error answers 401, 403 and 404 of the provided operations (X4)
    Given the provided operations API-S4-002 and API-S4-003
    When a call is made without a valid credential, by a role without the Litigation right, or for a firm unknown in the caller's scope
    Then the call without a valid credential is answered with 401
    Then the call by a role without the Litigation right is answered with 403 and MSG-P4-002 as in AC5
    Then the call for a firm unknown in the caller's scope is answered with 404 or 409 as section 5 X4 states
    Then nothing is written"""

para_old = "AC5 and AC6 are not legacy criteria: they carry X2 and X11 of section 5. AC7 to AC12 carry BR1 to BR9 and R-LIT-28, each with its test case in section 16."
para_new = "AC5 and AC6 are not legacy criteria: they carry X2 and X11 of section 5. AC7 to AC12 carry BR1 to BR9 and R-LIT-28, AC13 and AC14 carry X8, AC15 carries X3, AC16 carries the 401, 403 and 404 answers of the provided operations, and AC17 carries the replay of a write under BR7, each with its test case in section 16."

tcpara_old = "The five legacy test case IDs, their Covers and their Data are kept in order and character for character; TC-E5-009-01 covers legacy AC1,"
tcpara_new = "The five legacy test case IDs, their Covers and their Data are kept in order and character for character, except the `decision log` wording of TC-E5-009-06, which now reads `decision record` (CG-ALL-9195); TC-E5-009-01 covers legacy AC1,"

x3_old = "| X3 | The case is not in `FIRM_SELECTION` for R-LIT-24, or not in `FIRM_ESCALATED` for R-LIT-26 | 409 on the call; no rule is evaluated, nothing changes and no decision record is written | None | AC2, AC3 |"
x3_new = "| X3 | The case is not in `FIRM_SELECTION` for R-LIT-24, or not in `FIRM_ESCALATED` for R-LIT-26 | 409 on the call; no rule is evaluated, nothing changes and no decision record is written | None | AC2, AC3, AC15 |"

x8_old = "| X8 | A consumed contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered | None | AC2, AC3 |"
x8_new = "| X8 | A consumed contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered | None | AC2, AC3, AC13, AC14 |"

x9_old = "| X9 | The same case and firm signal arrives twice | One record, one instruction request, one clock and one answer; the repeat is counted | None | AC2, AC3 |"
x9_new = "| X9 | The same case and firm signal arrives twice | One record, one instruction request, one clock and one answer; the repeat is counted | None | AC2, AC3, AC9, TC-E5-009-11 |"

br_old = "BR7 by AC9 (TC-E5-009-11); BR8 by AC10 (TC-E5-009-12);"
br_new = "BR7 by AC9 (TC-E5-009-11) and AC17 (TC-E5-009-19); BR8 by AC10 (TC-E5-009-12);"

edits = [(big_old, big_new), (ac15_old, ac15_new), (ac16_old, ac16_new), (para_old, para_new),
         (tcpara_old, tcpara_new), (x3_old, x3_new), (x8_old, x8_new), (x9_old, x9_new), (br_old, br_new)]

for i, (o, n) in enumerate(edits, 1):
    c = t.count(o)
    print(i, "count", c)
    assert c == 1
    t = t.replace(o, n, 1)

meta = json.loads((Path(__file__).resolve().parents[1] / "chunks" / "RWB-S4-E5009-APP" / "meta.json").read_text(encoding="utf-8"))
before = Path(meta["input_file"]).read_text(encoding="utf-8") if Path(meta["input_file"]).exists() else t
print("before exists:", Path(meta["input_file"]).exists())
fs = lint.lint_text("X", before, t)
for f in fs:
    print(f["check"], f["line"], f["detail"][:120])
print("findings", len(fs))
