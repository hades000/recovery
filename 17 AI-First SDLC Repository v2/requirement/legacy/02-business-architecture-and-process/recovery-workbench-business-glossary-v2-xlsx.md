<!-- source: 02 Business architecture and process/Recovery Workbench Business Glossary v2.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Business Glossary v2.xlsx`  
> **Converted from:** XLSX

## Glossary

| Business glossary |  |  |  |  |  |
|---|---|---|---|---|---|
| 98 terms. One term, one definition, one name in the model, the code and the conversation. Thai terms are proposed and approved by Legal and Compliance under DL10. |  |  |  |  |  |
| Term | Definition | Thai term, proposed | Maps to | Category | Do not use |
| Agent | An AI component that prepares and recommends through the tool gateway | เอเจนต์ | role SY-AGENT | Decision | Bot, robot |
| Allocation | Placing a new case in a queue and giving it an owner by rule | การจัดสรรงาน | assignment.reason = ALLOCATION | Case | Distribution |
| Appraisal | A valuation of collateral or an asset | การประเมินราคา | valuation | Collateral | Valuation report |
| Approval level | One of the six levels of the bank approval authority regulation that may approve a decision | ระดับอำนาจอนุมัติ | delegation_limit.approval_level; LOV-APPROVAL-LEVEL | Decision | Authority, sign-off |
| Asset held for sale | An asset the bank holds after repossession, deed in lieu or auction purchase | ทรัพย์สินรอการขาย | asset | Disposal | None |
| Autonomy level | How far an agent may act on a decision, from L0 to L4 | ระดับการทำงานอัตโนมัติ | Agent runtime | Decision | None |
| Black case number | The court number given when a case is filed | หมายเลขคดีดำ | legal_action.black_case_no | Legal | None |
| Book value | The value of an asset held for sale in the bank's books | มูลค่าตามบัญชี | asset.book_value | Disposal | None |
| Borrower | The party the loan was made to | ผู้กู้ | case_party.party_role = BORROWER | Party | Debtor |
| Break-glass | Emergency access beyond a role, with a reason and a review | การเข้าถึงกรณีฉุกเฉิน | Access log | Control | Super user |
| Buy-back | The customer buying back an asset transferred in lieu | การซื้อทรัพย์คืน | treatment.treatment_type = BUY_BACK | Treatment | None |
| Case file item | A piece of information the case holds, such as the account, a document or a decision | รายการในแฟ้มกรณี | Case model | Case | None |
| Case number | The identifier issued when a case is created, in the form RW-YYYY-NNNNNN, never reused | เลขที่กรณี | recovery_case.case_no | Case | Case ID in other systems |
| Case owner | The person who holds the case from day 90 to close and answers for its outcome | ผู้รับผิดชอบกรณี | recovery_case.owner_user_id; role RW-CASEOWN | Case | Collector, handler |
| Case status | One of New, Assigned, In progress, Waiting customer, Waiting partner, Waiting approval, On hold, Closed | สถานะกรณี | recovery_case.status; LOV-CASE-STATUS | Case | Stage, step |
| Caseload cap | The most open cases one person may hold in a queue | จำนวนกรณีสูงสุดต่อคน | queue.capacity_cap | Case | Quota |
| Co-borrower | A party who borrowed jointly with the borrower | ผู้กู้ร่วม | case_party.party_role = CO_BORROWER | Party | None |
| Collateral | Property or a vehicle securing one or more accounts | หลักประกัน | collateral | Collateral | Security |
| Collection agency | A firm placed with accounts to collect | บริษัทติดตามหนี้ | partner.partner_type = AGENCY | Partner | None |
| Contact point | A way to reach a party, with its consent and whether it works | ช่องทางการติดต่อ | contact_point | Party | Phone number, address |
| Contact stop | An instruction that no one contacts the customer while it is in force | การระงับการติดต่อลูกหนี้ | deviation.contact_stop | Case | Do not call |
| Cure | Arrears cleared so the account falls below 90 days past due and the case closes | การกลับมาเป็นหนี้ปกติ | recovery_case.closure_reason = CURED | Money and closure | None |
| Custody | Where an original document is and who holds it | การเก็บรักษาต้นฉบับ | document_custody | Document | None |
| Data product | A set of entities with one system of record, one way in and one freshness | ชุดข้อมูลผลิตภัณฑ์ | Conceptual data model | Platform | Data mart, dataset |
| Days past due | Days since the oldest unpaid installment fell due | จำนวนวันค้างชำระ | loan_account.days_past_due | Account | None |
| Debt sale | Sale of accounts to a debt buyer | การขายหนี้ | debt_sale_lot | Disposal | None |
| Decision | One of D1 to D9 or their sub-decisions, made by a rule, a model, an agent or a person | การตัดสินใจ | decision_log_entry.decision_code | Decision | Approval |
| Decision log | The append-only, hash-chained record of every decision with its inputs, versions, approver and outcome | บันทึกการตัดสินใจ | decision_log_entry | Decision | Audit trail, history |
| Deed in lieu | Transfer of the collateral to the bank in settlement of the debt | การโอนทรัพย์ชำระหนี้ | treatment.treatment_type = DEED_IN_LIEU | Treatment | None |
| Delegation of authority table | The limits each approval level may approve, by decision, product and amount | ตารางมอบอำนาจอนุมัติ | delegation_limit | Decision | DOA matrix |
| Demand notice | A notice demanding payment before legal action | หนังสือบอกกล่าวทวงถาม | notice.notice_type = DEMAND | Legal | Letter |
| Deviation | An event that stops the normal route: X1 to X7 | เหตุผิดปกติ | deviation; LOV-DEVIATION | Case | Exception, issue |
| Document hub | The Workbench store and index for recovery documents | ศูนย์เอกสาร | document | Document | DMS, folder |
| Document type | The class a document belongs to on the document checklist | ประเภทเอกสาร | document.document_type | Document | None |
| Enforcement | Steps after judgment to seize and sell assets | การบังคับคดี | legal_action.action_type = ENFORCEMENT | Legal | None |
| Event listener | A point in the case model that waits for an outside event, such as a payment or a court date | ตัวรอเหตุการณ์ | Case model | Case | Hook |
| Exposure band | The band a case's outstanding balance falls in at entry | กลุ่มยอดหนี้ | recovery_case.exposure_band | Account | Segment |
| Floor price | The lowest price approved for a sale | ราคาขั้นต่ำ | listing.floor_price | Disposal | Reserve price, for an asset |
| Forced sale value | The value expected in a quick sale | ราคาขายบังคับ | valuation.forced_sale_value | Collateral | Liquidation value |
| Freshness | How old a loaded value is, from its business date | ความเป็นปัจจุบันของข้อมูล | data_as_of | Platform | None |
| Guarantee claim | A claim against a Thai Credit Guarantee Corporation guarantee or an insurer | การยื่นขอรับค่าประกันชดเชย | guarantee_claim | Treatment | TCG claim, when an insurer is meant |
| Guarantor | A party who guaranteed the loan | ผู้ค้ำประกัน | case_party.party_role = GUARANTOR | Party | Surety |
| Haircut | The amount forgiven in a settlement | ส่วนลดหนี้ | treatment.haircut_amount | Treatment | None |
| Heir | A party who represents a deceased borrower's estate | ทายาท | case_party.party_role = HEIR | Party | None |
| Interaction ledger | The ordered record of every contact, letter, promise, payment and hand-over on a case | บันทึกการติดต่อ | interaction | Decision | Contact history, notes |
| Judgment | The court's decision on the claim | คำพิพากษา | legal_action.judgment_date, judgment_amount | Legal | None |
| Law firm | A firm instructed to file and run lawsuits | สำนักงานกฎหมาย | partner.partner_type = LAW_FIRM | Partner | Lawyer, when the firm is meant |
| Lawsuit | A civil case filed against the borrower or guarantor | การฟ้องร้องคดี | legal_action.action_type = CIVIL_CASE | Legal | Litigation, when one suit is meant |
| Legal Execution Department | The government department that runs enforcement auctions | กรมบังคับคดี | role PT-LED | Legal | None |
| Legal hold | A hold that stops routing while a legal matter is decided | การระงับเพื่อเหตุทางกฎหมาย | recovery_case.legal_hold | Case | None |
| List of values | A closed set of codes a field may take | รายการค่าที่กำหนด | lov_value | Platform | Drop-down, lookup |
| Listing | An asset offered for sale, with its prices and rounds | รายการประกาศขาย | listing | Disposal | None |
| Loan account | An account in the core bank | บัญชีสินเชื่อ | loan_account | Account | Contract, when the account is meant |
| Lot | A group of accounts offered to debt buyers together | กองหนี้ | debt_sale_lot | Disposal | Pool, portfolio |
| Masking | Hiding a personal data field from a role not allowed to see it | การปกปิดข้อมูล | Personal data fields | Control | None |
| Milestone | A point the case reaches that matters to the bank, such as judgment obtained or asset sold | หมุดหมาย | Case model | Case | Checkpoint |
| Non-performing loan | A loan at 90 days past due or more | หนี้ที่ไม่ก่อให้เกิดรายได้ | loan_account.classification | Account | Bad loan |
| Override | A decision that does not follow the recommendation, with the reason recorded | การตัดสินใจต่างจากข้อเสนอแนะ | decision_log_entry.override_reason | Decision | None |
| Partner | An outside firm the bank places work with | คู่ค้า | partner | Partner | Vendor, outsource |
| Partner instruction | Work placed with a partner on a case | คำสั่งงานคู่ค้า | partner_instruction | Partner | Order, assignment |
| Partner portal | The Workbench screens partners use for their placed cases | หน้าจอสำหรับคู่ค้า | P4 partner identities; capability area Partner portal | Partner | None |
| Party | A person or company with a role on a case | บุคคลที่เกี่ยวข้อง | party | Party | Customer, when the person is not the borrower |
| Payoff | The amount that settles the account on a given date | ยอดปิดบัญชี | treatment.offer_amount | Account | Settlement figure |
| Permission | A letter C, R, U, D or A in one capability area | สิทธิ์ | permission | Control | Right |
| Prescription date | The earliest date a legal claim on the case expires. It never pauses | วันขาดอายุความ | recovery_case.prescription_date | Case | Expiry |
| Principle 1 | Every rule, limit, threshold, template, name, queue, role, timer and route is a versioned data row, changed by a validated load without a code release | หลักการที่ 1 | All reference data | Platform | None |
| Proceeds | Money received on a case and what it was matched to | เงินที่ได้รับ | proceeds | Money and closure | Collection |
| Proof of delivery | Evidence that a registered notice reached the party | หลักฐานการส่งหนังสือ | notice.callback_date, notice.delivery_status | Legal | None |
| Put-back | A buyer returning an account under the sale terms | การขอคืนบัญชี | debt_sale_account.put_back_status | Disposal | None |
| Queue | A list of cases belonging to one team and one role | คิวงาน | queue | Case | Bucket, basket |
| Recall notice | A notice ending the loan and calling the full balance | หนังสือบอกเลิกสัญญา | notice.notice_type = RECALL | Legal | None |
| Recommendation | The option a rule, model or agent proposes, with reasons and confidence | ข้อเสนอแนะ | decision_log_entry.recommendation | Decision | Suggestion |
| Recovery after charge-off | Money collected after a write-off | การติดตามหนี้หลังตัดหนี้สูญ | write_off.recovered_after | Money and closure | None |
| Recovery case | One case per customer per product, from 90 days past due to close, with its accounts linked | กรณีติดตามหนี้ | recovery_case | Case | Ticket, file, job |
| Red case number | The court number given at judgment | หมายเลขคดีแดง | legal_action.red_case_no | Legal | None |
| Repossession | Taking back a vehicle under a hire purchase contract | การยึดรถ | asset.repossessed_date | Disposal | None |
| Reserve price | The lowest price approved for a debt sale lot | ราคาสงวน | debt_sale_lot.reserve_price | Disposal | None |
| Restructure | New terms for the debt agreed with the customer | การปรับโครงสร้างหนี้ | treatment.treatment_type = RESTRUCTURE | Treatment | None |
| Return by route | The expected recovery after cost of each route for a case | ผลตอบแทนตามแนวทาง | score.estimate_value, score.route_code | Decision | Net present value |
| Role | A job function with the permissions it needs | บทบาท | role | Control | Profile, group |
| Route | The resolution path chosen for a case: R1 restructure to R8 write-off | แนวทางการแก้ไขหนี้ | recovery_case.route_code; LOV-ROUTE | Case | Strategy, track |
| Route state | The state in a route set's decision table that the case is in | สถานะตามแนวทาง | recovery_case.route_state | Case | Status |
| Rule | One row of a decision table: from state, event and condition in; action, next state, owner and timer out | กฎ | rule_row | Decision | Logic, script |
| Rule version | The version of a rule in force when a decision was made | ฉบับของกฎ | rule_row.rule_version | Decision | None |
| Scope | Which cases a role sees: own, team, region or all | ขอบเขตการเข้าถึง | role.default_scope | Control | None |
| Score | A value COLLINS returns for an account or a case, such as a risk score or a price estimate | คะแนนจากแบบจำลอง | score | Decision | None |
| Sentry | A rule that lets a stage, task or milestone start or finish when an event occurs and its condition holds | เงื่อนไขเปิดปิดขั้นตอน | rule_row | Case | Trigger |
| Service level | How long a case may stay in a state before it escalates | ระยะเวลามาตรฐาน | timer.timer_type = SERVICE_LEVEL | Case | SLA in free text |
| Settlement | Payment of an agreed amount that closes the debt | การชำระหนี้เพื่อปิดบัญชี | treatment.treatment_type = SETTLEMENT | Treatment | Discount |
| Stage | A part of the case lifecycle, such as litigation or asset disposal, in CMMN 1.1 terms | ขั้นตอนหลัก | recovery_case.stage_code; LOV-STAGE | Case | Phase, bucket |
| Stage clock | The time a case has spent in its current state, paused while a deviation is open | นาฬิกาขั้นตอน | recovery_case.stage_clock_start | Case | Aging |
| System of record | The system whose value is correct when two systems differ | ระบบต้นทางหลัก | Entity attribute | Platform | Master, when not meant |
| Task | A unit of work on a case for a person, a customer, a partner or a decision | งาน | task | Case | Activity, to-do |
| Total balance | Principal, interest and fees outstanding | ยอดหนี้คงค้างรวม | loan_account.total_balance | Account | Outstanding |
| Transfer | Moving a case to another owner or queue with a reason | การโอนงาน | assignment.reason = TRANSFER | Case | Reassign without a reason |
| Treatment | A resolution put to the customer or carried out on the case | แนวทางการแก้ไขที่เสนอ | treatment | Treatment | Offer, when a booked plan is meant |
| Vulnerable customer | A customer with hardship or vulnerability confirmed, treated under X2 | ลูกหนี้กลุ่มเปราะบาง | party.vulnerable_flag | Party | None |
| Write-off | Removing the balance from the books after approval | การตัดหนี้สูญ | write_off | Money and closure | None |

## Categories

| Terms by category |  |
|---|---|
| Calculated from the Glossary tab. |  |
| Category | Terms |
| Case |  |
| Decision |  |
| Party |  |
| Account |  |
| Treatment |  |
| Legal |  |
| Collateral |  |
| Disposal |  |
| Money and closure |  |
| Partner |  |
| Document |  |
| Platform |  |
| Control |  |
| Total |  |

## Key

| Key |  |  |
|---|---|---|
| What each column and rule means. |  |  |
| Item | Term | Meaning |
| Column | Term | The one name used for the concept in screens, documents, the data model and the code |
| Column | Maps to | The entity, field, list of values or role that holds the concept in the logical data model |
| Column | Do not use | Names that mean something else or are ambiguous. A reviewer rejects code or text that uses them |
| Rule | New term | Added here before it is used in a story, a screen or the code |
| Rule | Changed term | Changed here first, then in the data dictionary and the code |
| Standard | Domain driven design | One ubiquitous language shared by the business and the squads |
