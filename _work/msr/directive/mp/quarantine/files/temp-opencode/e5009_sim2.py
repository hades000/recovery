import sys
sys.path.insert(0, r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\directive")
import lint

now_path = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\directive\mp\out\RWB-S4-E5009-APP.md"
before_path = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\pipeline\all-stories-2026-11-26\4-applied\04 User stories\Recovery Workbench Service Story Files v1\RWB-SVC-S4 rwb-litigation (Litigation)\RWB S4 E5009 APP Instruct the firm through the portal v2.md"
now = open(now_path, encoding="utf-8").read()
before = open(before_path, encoding="utf-8").read()

pairs = [
("| TC-E5-009-07 | Section 12 operations, events and activities | Contract | Not specified in the source documents (DOR-RWB-S4-E5009-APP-12) |","| TC-E5-009-20 | Section 12 operations, events and activities | Contract | Not specified in the source documents (DOR-RWB-S4-E5009-APP-12) |"),
("| TC-E5-009-08 | Section 12.7 tables (ASM-3438) | Component | No statement outside `rwb_litigation`, no `v_ace_*` read, no write to another schema |","| TC-E5-009-21 | Section 12.7 tables (ASM-3438) | Component | No statement outside `rwb_litigation`, no `v_ace_*` read, no write to another schema |"),
("| TC-E5-009-07 | Access | Component | AC5: a role without the Litigation right is refused with MSG-P4-002 before any change |","| TC-E5-009-07 | AC5 | Component | AC5: a role without the Litigation right is refused with MSG-P4-002 before any change |"),
("| TC-E5-009-08 | Boundary | Pipeline | AC6: a statement reaching a protected object fails the boundary test and the build |","| TC-E5-009-08 | AC6 | Pipeline | AC6: a statement reaching a protected object fails the boundary test and the build |"),
("| TC-E5-009-09 | Business rules | Component | AC7: only rwb_litigation evaluates the rules and no other owner's row is written or joined |","| TC-E5-009-09 | AC7 | Component | AC7: only rwb_litigation evaluates the rules and no other owner's row is written or joined |"),
("| TC-E5-009-10 | Business rules | Component | AC8: the decision record holds the rule ID and package version before any change |","| TC-E5-009-10 | AC8 | Component | AC8: the decision record holds the rule ID and package version before any change |"),
("| TC-E5-009-11 | Idempotency | Component | AC9: the same signal twice writes once and the repeat is counted |","| TC-E5-009-11 | AC9 | Component | AC9: the same signal twice writes once and the repeat is counted |"),
("| TC-E5-009-12 | Timer | Component | AC10: the partner clock is 2 working days from the calendar in force |","| TC-E5-009-12 | AC10 | Component | AC10: the partner clock is 2 working days from the calendar in force |"),
("| TC-E5-009-13 | Data | Component | AC11: no person data enters the decision record, a log or the workflow input |","| TC-E5-009-13 | AC11 | Component | AC11: no person data enters the decision record, a log or the workflow input |"),
("| TC-E5-009-14 | Breach | Component | AC12: R-LIT-28 marks the breach and answers FIRM_BREACHED_SLA when the clock expires |","| TC-E5-009-14 | AC12 | Component | AC12: R-LIT-28 marks the breach and answers FIRM_BREACHED_SLA when the clock expires |"),
("| TC-E5-009-15 | Activity | Component | AC13: a consumed contract that does not answer inside 2 s or whose breaker is open is retried and writes nothing |","| TC-E5-009-15 | AC13 | Component | AC13: a consumed contract that does not answer inside 2 s or whose breaker is open is retried and writes nothing |"),
("| TC-E5-009-16 | Activity | Component | AC14: a failed consumed call writes nothing; Not specified in the source documents (NEWAC-RWB-S4-E5009-APP-AC11) |","| TC-E5-009-16 | AC14 | Component | AC14: a failed consumed call writes nothing; Not specified in the source documents (NEWAC-RWB-S4-E5009-APP-AC11) |"),
("| TC-E5-009-17 | Status change | Component | AC15: a case state the rule does not allow is refused with 409 and nothing changes |","| TC-E5-009-17 | AC15 | Component | AC15: a case state the rule does not allow is refused with 409 and nothing changes |"),
("| TC-E5-009-18 | Access | Component | AC16: an unknown firm or a case outside its state is answered with an error and nothing is written |","| TC-E5-009-18 | AC16 | Component | AC16: an unknown firm or a case outside its state is answered with an error and nothing is written |"),
("| TC-E5-009-19 | Idempotency | Component | AC17: a replay with the same idempotency key returns the stored answer and writes nothing again |","| TC-E5-009-19 | AC17 | Component | AC17: a replay with the same idempotency key returns the stored answer and writes nothing again |"),
("The five legacy test case IDs, their Covers and their Data are kept in order and character for character; TC-E5-009-01 covers legacy AC1","The five legacy test case IDs, their Covers and their Data are kept in order and character for character, except that TC-E5-009-06 now says decision record where the legacy said decision log (CG-ALL-9195); TC-E5-009-01 covers legacy AC1"),
]

for old,new in pairs:
    assert now.count(old)==1, (now.count(old), old[:80])
    now = now.replace(old,new,1)

base = lint.lint_text("RWB-S4-E5009-APP", before, before)
keys = {(f["check"],f["detail"]) for f in base}
res = [f for f in lint.lint_text("RWB-S4-E5009-APP", before, now) if (f["check"],f["detail"]) not in keys]
print("filtered findings:", res)
