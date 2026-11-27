import io, re

p = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\directive\mp\out\RWB-S7-E6022-APP.md"
t = io.open(p, encoding="utf-8").read()

edits = [
("| Contract dependencies | None |\n| Integration dependencies | None |",
 "| Contract dependencies | None |\n| Contract version | v1 (base path /api/recovery/writeoff/v1) |\n| Integration dependencies | None |"),
("on task queue `rwb-writeoff` in namespace `rwb-recovery`: R-WO-26",
 "on task queue `rwb-writeoff`: R-WO-26"),
("| TC-E6-022-04 | Access: a role without the right is refused with MSG-P4-002 | Component | A caller without Write-off and posting R on the write-off read; no read and no record |",
 "| TC-E6-022-04 | AC4: a role without the right is refused with MSG-P4-002 | Component | A caller without Write-off and posting R on the write-off read; no read and no record |"),
("| TC-E6-022-06 | No tax criteria version in force: the case is held at PROVISION_RELEASED with MSG-S7-001 and nothing is written | Component | No version in force at the business date; the run resumes after Finance publishes it |",
 "| TC-E6-022-06 | AC5: no tax criteria version in force: the case is held at PROVISION_RELEASED with MSG-S7-001 and nothing is written | Component | No version in force at the business date; the run resumes after Finance publishes it |"),
("| TC-E6-022-07 | A case not at PROVISION_RELEASED, or already moved, is refused with 409 and not fed twice | Component | A case at another state or outside the population when the run arrives |",
 "| TC-E6-022-07 | AC6: a case not at PROVISION_RELEASED, or already moved, is refused with 409 and not fed twice | Component | A case at another state or outside the population when the run arrives |"),
("| TC-E6-022-08 | A dependency that does not answer inside 2 s is retried, writes nothing and answers 503 | Component | rwb-case, rwb-decision or the reference-data read does not answer or its breaker is open |",
 "| TC-E6-022-08 | AC7: a dependency that does not answer inside 2 s is retried, writes nothing and answers 503 | Component | rwb-case, rwb-decision or the reference-data read does not answer or its breaker is open |"),
("| TC-E6-022-09 | A rejected file records the rejection code, answers FINANCE_FEED_REJECTED and raises the two-working-day task | Component | The Finance provision feed rejects the file |",
 "| TC-E6-022-09 | AC8: a rejected file records the rejection code, answers FINANCE_FEED_REJECTED and raises the two-working-day task | Component | The Finance provision feed rejects the file |"),
("| TC-E6-022-10 | The same business date, population and package version, or the same Idempotency-Key, twice gives one record, one feed and one answer | Component | The run and the key repeated |",
 "| TC-E6-022-10 | AC9: the same business date, population and package version, or the same Idempotency-Key, twice gives one record, one feed and one answer | Component | The run and the key repeated |"),
("| TC-E6-022-11 | A statement reaching a v_ace_* view, a recovery_case row or another service's schema is refused and fails the build | Component | A component, a statement or a test reaches a forbidden object |",
 "| TC-E6-022-11 | AC10: a statement reaching a v_ace_* view, a recovery_case row or another service's schema is refused and fails the build | Component | A component, a statement or a test reaches a forbidden object |"),
("| TC-E6-022-12 | A changed or absent Finance feed row is obeyed, or no feed is built and the cases stay at PROVISION_RELEASED | Component | The feed row changes between runs or no row is in force |",
 "| TC-E6-022-12 | AC11: a changed or absent Finance feed row is obeyed, or no feed is built and the cases stay at PROVISION_RELEASED | Component | The feed row changes between runs or no row is in force |"),
("| TC-E6-022-13 | The provision inputs and the tax file leave as two feed items and the case move is answered, not written | Component | The rwb-case contract mock returns the case at PROVISION_RELEASED |",
 "| TC-E6-022-13 | AC12: the provision inputs and the tax file leave as two feed items and the case move is answered, not written | Component | The rwb-case contract mock returns the case at PROVISION_RELEASED |"),
("| TC-E6-022-14 | Only this service's write_off rows are read and no personal data enters a record, feed item, log or workflow input | Component | The posted population of the business date |",
 "| TC-E6-022-14 | AC13: only this service's write_off rows are read and no personal data enters a record, feed item, log or workflow input | Component | The posted population of the business date |"),
("| TC-E6-022-15 | The tax criteria version is read with its version and no business value is written in code | Component | Reference data holds the tax criteria version |",
 "| TC-E6-022-15 | AC14: the tax criteria version is read with its version and no business value is written in code | Component | Reference data holds the tax criteria version |"),
("| TC-E6-022-16 | A cleared rejection returns the case to FINANCE_FEED_SENT and the feed elements are held in the decision record and case state | Component | A case at FINANCE_FEED_REJECTED and an accepted re-send |",
 "| TC-E6-022-16 | AC15: a cleared rejection returns the case to FINANCE_FEED_SENT and the feed elements are held in the decision record and case state | Component | A case at FINANCE_FEED_REJECTED and an accepted re-send |"),
("| TC-E6-022-17 | The month-end close runs as a durable timer of WriteOffWorkflow and not as a Schedule | Component | The month-end close of R-WO-26 |",
 "| TC-E6-022-17 | AC16: the month-end close runs as a durable timer of WriteOffWorkflow and not as a Schedule | Component | The month-end close of R-WO-26 |"),
("| TC-E6-022-18 | The decision is recorded with the rule ID and the package version before anything leaves; a failed write changes nothing | Component | The decision for the case is ready |",
 "| TC-E6-022-18 | AC17: the decision is recorded with the rule ID and the package version before anything leaves; a failed write changes nothing | Component | The decision for the case is ready |"),
("| TC-E6-022-06 | Contract: the operations, events and activities named in §12 match their contract elements | Contract | The operations, events and activities of §12 with their contract elements, checked against the contract |",
 "| TC-E6-022-22 | Contract: the operations, events and activities named in §12 match their contract elements | Contract | The operations, events and activities of §12 with their contract elements, checked against the contract |"),
("| TC-E6-022-07 | Boundary: only the tables of §12.7 are written or read; no statement outside rwb_writeoff, no v_ace_* read, no foreign key (ASM-3438) | Component | The statements of the step recorded on the fake; only the tables of §12.7 appear |",
 "| TC-E6-022-23 | Boundary: only the tables of §12.7 are written or read; no statement outside rwb_writeoff, no v_ace_* read, no foreign key (ASM-3438) | Component | The statements of the step recorded on the fake; only the tables of §12.7 appear |"),
("The three criteria are the three criteria of RWB-E6-022, word for word, with their origin tags added and nothing else changed:",
 "The three criteria are the three criteria of RWB-E6-022, with their origin tags added, the legacy `decision log` wording replaced by `decision record`, and nothing else changed:"),
]

for i, (old, new) in enumerate(edits, 1):
    c = t.count(old)
    if c != 1:
        print("BAD", i, c)
    t = t.replace(old, new, 1)

# duplicate TC IDs
ids = re.findall(r"^\| (TC-E6-022-\d+) \|", t, re.M)
from collections import Counter
dups = {k: v for k, v in Counter(ids).items() if v > 1}
print("TC ids count", len(ids), "dups", dups)
print("AC tokens in section 16:")
sec16 = t.split("### 16. Test cases")[1].split("### 17.")[0]
for n in range(1, 21):
    if ("AC%d" % n) not in sec16:
        print("missing AC%d" % n)
print("namespace remaining", t.count("rwb-recovery"))
print("contract version row", "| Contract version | v1 (base path /api/recovery/writeoff/v1) |" in t)
io.open(r"C:\Users\SahilMore\AppData\Local\Temp\opencode\after.md", "w", encoding="utf-8").write(t)
