
Example: the same case, a different approver after a rule change

Settlement approval limits are versioned and take effect on a date

Settlement case
Principal THB 2.4m · loss 20%

2 Jan 2027

Rule version DOA-2026.11
approved, dated

Approver: L6
before 2 January

Logged: DOA-2026.11

Rule version DOA-2027.01
approved, dated

Approver: L5
from 2 January

Logged: DOA-2027.01

No code change, no release: the business changed a table and set a date.

Rules change on a date, by approval, and every answer shows which version made it.

6

Notes: From FSD P7 AC-ALT-P7-015: a D6.4 MORTGAGE settlement on principal THB 2,400,000 at 20% loss (THB 480,000) routes to an L6 approver (U-9201) under version DOA-2026.11. From 2 Jan 2027 version DOA-2027.01 is in force and the same case routes to L5. Raising the principal to THB 120m moves it to L5 under either version, because L6's limit is THB 100m (DoA item 2.1.1).

The version used is written into the decision log, so an auditor can always see why a case went to a given approver. Delegation limits are held as versioned reference data (delegation_limit) and follow the same approve-and-date discipline as the Drools packages.

