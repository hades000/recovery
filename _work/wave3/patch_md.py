import os
BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
MD = BASE + r"\04 User stories\Recovery Workbench User Stories Epic 2 v6.md"
doc = open(MD, encoding="ascii").read()

pairs = [
    ("| Acceptance criteria | 360 |", "| Acceptance criteria | 352 |"),
    ("| Test cases | 415 |", "| Test cases | 406 |"),
    ("Idempotency key unchanged (account_payment_id).", "Idempotency key unchanged (payment_code)."),

    ('    Then the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS"\n'
     '    When the clock passes 2026-12-31 23:59 and the timer check runs\n'
     '    Then the system publishes a TimerDue event with timer type "INSTALLMENT_DUE" and the treatment ID',
     '    Then the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS"\n'
     '    Then when the clock passes 2026-12-31 23:59 and the timer check runs, the system publishes a TimerDue event with timer type "INSTALLMENT_DUE" and the treatment ID'),

    ('    Then the screen stays in state "On hold"\n'
     '    When "X1" is cleared on 2026-12-14 and "X3" stays open\n'
     '    Then the screen stays in state "On hold" with only "X3" open and "X1" shown as cleared on 2026-12-14',
     '    Then the screen stays in state "On hold"\n'
     '    Then when "X1" is cleared on 2026-12-14, the screen stays in state "On hold" with only "X3" open and "X1" shown as cleared on 2026-12-14'),

    ('    When "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077"\n'
     '    When NSS accepts the message with reference "NSS-7781" and returns result "DELIVERED"',
     '    When "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077", and NSS accepts it with reference "NSS-7781" returning result "DELIVERED"'),

    ('    When "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND"\n'
     '    When LINE OA reports the message delivered and then read',
     '    When "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND", and LINE OA reports it delivered and then read'),

    ('    When the manager filters by queue "MTG-BKK-CO", product MORTGAGE and breached Yes\n'
     '    Then 1 row shows, "RW-2026-000101"\n'
     '    When the manager chooses Extract with the same filters\n',
     '    When the manager filters by queue "MTG-BKK-CO", product MORTGAGE and breached Yes and then chooses Extract with the same filters\n'
     '    Then 1 row shows, "RW-2026-000101"\n'),

    ('    Given a rule with timer "same day" fires on 14 December 2026\n'
     '    Then the due date is 14 December 2026',
     '    Given a rule with timer "same day" moves case "RW-2026-000406" on 14 December 2026\n'
     '    When the next action is set from that rule\n'
     '    Then the due date is 14 December 2026'),

    ('    Then the case status becomes ASSIGNED\n'
     '    When both owners hold 150 open cases and the model places case "RW-2026-000502"\n'
     '    Then case "RW-2026-000502" is in queue "MTG-BKK-OVF" with no owner and status NEW',
     '    Then the case status becomes ASSIGNED\n'
     '    Then when both owners hold 150 open cases and the model places case "RW-2026-000502", that case is in queue "MTG-BKK-OVF" with no owner and status NEW'),
]

for old, new in pairs:
    c = doc.count(old)
    assert c == 1, (c, old[:80])
    doc = doc.replace(old, new)

open(MD, "w", encoding="ascii", newline="\n").write(doc)
print("patched", len(doc))
