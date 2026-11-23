<!-- source: 05 Technical architecture/Recovery Workbench Event and Messaging Design v4.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `05 Technical architecture/Recovery Workbench Event and Messaging Design v4.xlsx`  
> **Converted from:** XLSX

## Events

| Events inside the Workbench |  |  |  |  |  |
|---|---|---|---|---|---|
| 30 entries: 26 published domain events, 2 consumed (EV-21 from the partner portal, EV-26 from the ACE batch record), 1 Temporal signal (EV-29) and 1 application event (EV-30). Domain events are in-process in the ACE service and written to the outbox in the same transaction. There is no external event bus today (D-RCV-35). |  |  |  |  |  |
| Version 4, 16 November 2026. D-RCV-36. |  |  |  |  |  |
| ID | Event | Direction | Owning module | Payload | Consumers |
| EV-01 | CaseCreated | Published | Case and workflow | caseId, caseNo, productGroup, accounts, businessDate | Allocation, ledger, reporting |
| EV-02 | CaseAllocated | Published | Case and workflow | caseId, queueId, ownerId, ruleId, ruleVersion | Ledger, reporting |
| EV-03 | CaseAllocationFailed | Published | Case and workflow | caseId, reason, ruleGap | Exception queue |
| EV-04 | CaseTransferred | Published | Case and workflow | caseId, fromOwner, toOwner, reasonCode | Ledger, timers |
| EV-05 | CaseStateChanged | Published | Case and workflow | caseId, fromState, toState, ruleId, decisionLogEntryId | Timers, reporting |
| EV-06 | DeviationRaised | Published | Deviation handling | caseId, deviationCode, raisedBy | Timers, communications (contact stop) |
| EV-07 | DeviationCleared | Published | Deviation handling | caseId, deviationCode, outcome | Timers, communications |
| EV-08 | DecisionRecorded | Published | Decision center and log | entryId, caseId, decisionCode, approver | Ledger, reporting |
| EV-09 | ApprovalRequested | Published | Decision center and log | approvalId, caseId, level, amount | Approval queue, notifications |
| EV-10 | TreatmentApproved | Published | TDR, settlement and deed in lieu | treatmentId, caseId, terms | Communications, booking confirmation |
| EV-11 | TreatmentBooked | Published | Payments and posting | treatmentId, bookingRef, businessDate | Case and workflow |
| EV-12 | PaymentMissed | Published | Payments and posting | treatmentId, dueDate, amountDue | Case and workflow (transfer rule) |
| EV-13 | NoticeGenerated | Published | Communications | noticeId, caseId, type, templateVersion | Approval queue |
| EV-14 | NoticeDispatched | Published | Communications | noticeId, barcode, sentDate | Ledger |
| EV-15 | NoticeDelivered | Published | Communications | noticeId, deliveredAt, status | Timers (notice period) |
| EV-16 | DocumentStored | Published | Document hub | documentId, caseId, type, source | Intake agent, checklist |
| EV-17 | DocumentFieldsExtracted | Published | Document hub | documentId, fields, confidence | Review queue, case |
| EV-18 | TimerDue | Published | Case and workflow | timerId, caseId, timerType | Rules component |
| EV-19 | TimerBreached | Published | Case and workflow | timerId, caseId, escalateTo | Notifications |
| EV-20 | InstructionIssued | Published | Partner management | instructionId, partnerId, type, dueOn | Partner portal |
| EV-21 | PartnerResultSubmitted | Consumed | Partner portal | instructionId, result, documents | Case and workflow |
| EV-22 | AssetTakenOn | Published | Assets and auction | assetId, caseId, source | Timers (holding age) |
| EV-23 | LotAwarded | Published | Debt sale | lotId, buyerId, price | Case and workflow (R-UNI-47) |
| EV-24 | WriteOffApproved | Published | Write-off and recovery | writeOffId, caseId, amount | Posting |
| EV-25 | ProceedsMatched | Published | Payments and posting | proceedsId, caseId, amount | Case and workflow |
| EV-26 | AceDataReady | Consumed | ACE ingestion, read through v_ace_batch_status | sourceSystem (source_system), businessDate (business_date), status, completedAt (completed_at) | Case creation (JOB-02), reconciliation (JOB-04), payment matching (JOB-07), booking confirmation (JOB-08), write-off scan (JOB-16) |
| EV-27 | AceDataLate | Published | Recovery data engine, from v_ace_batch_status | sourceSystem (source_system), businessDate (business_date), status, completedAt (completed_at) | Alerts, stale marker, data steward |
| EV-28 | AgentRunCompleted | Published | Agent runtime | runId, agent, caseId, outcome, fallback | Decision center, monitoring |
| EV-29 | CaseEvent | Signal | Case and workflow | caseId, eventType, sourceEventId, businessDate | CaseWorkflow on case-{caseId} (Epic 3+) |
| EV-30 | RulePackageInForce | Application event | Rules | packageCode, packageVersion, versionId, validFrom, approvedBy | KieBase cache refresh, rule change report (E2-041) |

## Rules

| Rules every event follows |  |
|---|---|
| Applies to every domain event; EV-26 and EV-27 are exempt from the Transactions rule. EV-29 and EV-30 are not domain events. |  |
| Rule | Detail |
| Ordering | Events for one case are processed in the order they were written, by a sequence per case in the outbox |
| Delivery | At least once; consumers are idempotent |
| Duplicates | Each event carries an event ID and an idempotency key; a repeat is ignored and counted (R-UNI-40) |
| Transactions | The event is written in the same transaction as the change; no event without the change and no change without the event. EV-26 and EV-27 are exempt: they are raised from the ACE batch record, not from a Workbench change |
| Payload | References and codes; no personal data |
| Versioning | An event carries its schema version; consumers accept the current and previous version |
| Failure | A consumer failure retries; after the limit the event goes to the exception queue with its owner |
| Signals | A Temporal signal goes to one workflow ID; it is not a broadcast, not a domain event and not written to the outbox |
| Outbox | The outbox stays for outbound work in Epics 1 and 2; from Epic 3 the multi-step outbound chain on rwb-integration writes through the outbox before the external call |
| History | Temporal history is the workflow's own record; it is not an event bus and no consumer subscribes to it |
