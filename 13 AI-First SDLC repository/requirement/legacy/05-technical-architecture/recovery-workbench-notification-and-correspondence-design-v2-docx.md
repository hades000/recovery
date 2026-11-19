<!-- source: 05 Technical architecture/Recovery Workbench Notification and Correspondence Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Notification and Correspondence Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Notification and correspondence design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench notification and correspondence design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 runtime view |

# 1. What is sent

| Kind | Examples | Channel | Proof |
|---|---|---|---|
| Statutory notice | Demand, recall, statutory sale notice, guarantor notice | Registered mail through WIN | Proof of delivery from WIN |
| Customer letter | Offer, settlement terms, restructure terms | Registered or ordinary mail; e-signature link | Delivery record; signed copy |
| Message | Reminder, offer ending, payment received | SMS through NSS; LINE OA | Delivery receipt from the channel |
| Partner instruction | Instruction, recall, fee approval | Partner portal | Acceptance by the partner |
| Internal alert | Task, warning, escalation | Workbench and email | Read on the case timeline |

# 2. How a notice is produced

- A rule raises the notice (R-LIT-03 for demand and recall).

- The Workbench checks the contact stop and the consented channel. A stop holds the notice (R-LIT-05).

- It fills the current template version approved by Legal for the type, product and language.

- The litigation officer approves the notice where the template requires approval.

- The notice goes to WIN in the daily outbound file through the outbox.

- WIN returns the barcode, then the proof of delivery in the weekly file.

- The delivery date starts the notice period (R-LIT-07). No proof within the window marks the notice unserved (R-LIT-08).

# 3. Templates

| Item | Design |
|---|---|
| Held as | Template rows with code, version, language, product group, body and Legal approval |
| Merge fields | From a catalog held as data; a template may use only catalog fields |
| Approval | Legal counsel approves each version; Compliance approves customer wording |
| Withdrawal | A withdrawn template holds generation (R-LIT-04) |
| Language | Thai by default; English where the customer chose English (DL10) |

# 4. Contact rules

- No message goes to a channel without consent; statutory notices continue when consent is withdrawn (R-UNI-10).

- A contact stop for a complaint, death or legal hold stops messages and letters except statutory notices where the law requires them.

- Contact times and frequency follow the Debt Collection Act and bank policy, held as reference data.

- Every message sent is written to the interaction ledger.

# 5. Volumes

| Item | Volume |
|---|---|
| Registered letters | About 1,900 a month |
| Proofs of delivery | About 1,900 a month |
| Messages | Set by the contact strategy; sized on the ACE notification path |

# 6. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL10 | Thai wording | English drafts with Thai requested |
| DL28 | Letter templates | Current bank templates loaded as version 1 |
