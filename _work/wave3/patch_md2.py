import os
BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
MD = BASE + r"\04 User stories\Recovery Workbench User Stories Epic 2 v6.md"
doc = open(MD, encoding="ascii").read()
pairs = [
    ('    When the list is read at 10 December 2026 09:00\n'
     '    Then row "RW-2026-000105" shows service level state RUNNING\n'
     '    When the list is read at 10 December 2026 09:01\n'
     '    Then row "RW-2026-000105" shows service level state BREACHED',
     '    When the list is read at 10 December 2026 09:00\n'
     '    Then row "RW-2026-000105" shows service level state RUNNING\n'
     '    Then when the list is read again at 10 December 2026 09:01, row "RW-2026-000105" shows service level state BREACHED'),
    ('    When the manager filters by product SSME\n'
     '    Then the list shows the empty state with message MSG-P3-020\n'
     '    When the manager chooses Extract with the same filter\n'
     '    Then an Excel file downloads with the header row and no data row',
     '    When the manager filters by product SSME and then chooses Extract with the same filter\n'
     '    Then the list shows the empty state with message MSG-P3-020\n'
     '    Then an Excel file downloads with the header row and no data row'),
]
for old, new in pairs:
    c = doc.count(old)
    assert c == 1, (c, old[:60])
    doc = doc.replace(old, new)
open(MD, "w", encoding="ascii", newline="\n").write(doc)
print("ok", len(doc))
