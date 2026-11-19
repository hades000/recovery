# Recovery Workbench event and messaging design

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench event and messaging design |
| Version | 3 |
| Status | In review |
| Date | 15 November 2026 |
| Owner | Solution architect |
| Decision | D-RCV-35 |

The Workbench publishes and consumes events inside the ACE service. Each event is written to the outbox in the same transaction as the change that raises it, and delivered to its consumers at least once. There is no external event bus today. Source data arrives in ACE through ACE's own ingestion, and the Workbench learns that a source is ready by reading the ACE batch record, `recovery.v_ace_batch_status` (D-RCV-35, U1). EV-26 and EV-27 are raised from that record; every other event is raised by a Workbench change. If a same-day feed is approved under DL06, the same events are published to it without changing their payloads.

## Rules

| Rule | Detail |
|---|---|
| Ordering | Events for one case are processed in the order they were written, by a sequence per case in the outbox |
| Delivery | At least once; consumers are idempotent |
| Duplicates | Each event carries an event ID and an idempotency key; a repeat is ignored and counted (R-UNI-40) |
| Transactions | The event is written in the same transaction as the change; no event without the change and no change without the event. EV-26 and EV-27 are exempt: they are raised from the ACE batch record, not from a Workbench change |
| Payload | References and codes; no personal data |
| Versioning | An event carries its schema version; consumers accept the current and previous version |
| Failure | A consumer failure retries; after the limit the event goes to the exception queue with its owner |

## Events

| ID | Event | Direction | Owning module | Consumers |
|---|---|---|---|---|
| EV-01 | CaseCreated | Published | Case and workflow | Allocation, ledger, reporting |
| EV-02 | CaseAllocated | Published | Case and workflow | Ledger, reporting |
| EV-03 | CaseAllocationFailed | Published | Case and workflow | Exception queue |
| EV-04 | CaseTransferred | Published | Case and workflow | Ledger, timers |
| EV-05 | CaseStateChanged | Published | Case and workflow | Timers, reporting |
| EV-06 | DeviationRaised | Published | Deviation handling | Timers, communications (contact stop) |
| EV-07 | DeviationCleared | Published | Deviation handling | Timers, communications |
| EV-08 | DecisionRecorded | Published | Decision center and log | Ledger, reporting |
| EV-09 | ApprovalRequested | Published | Decision center and log | Approval queue, notifications |
| EV-10 | TreatmentApproved | Published | TDR, settlement and deed in lieu | Communications, booking confirmation |
| EV-11 | TreatmentBooked | Published | Payments and posting | Case and workflow |
| EV-12 | PaymentMissed | Published | Payments and posting | Case and workflow (transfer rule) |
| EV-13 | NoticeGenerated | Published | Communications | Approval queue |
| EV-14 | NoticeDispatched | Published | Communications | Ledger |
| EV-15 | NoticeDelivered | Published | Communications | Timers (notice period) |
| EV-16 | DocumentStored | Published | Document hub | Intake agent, checklist |
| EV-17 | DocumentFieldsExtracted | Published | Document hub | Review queue, case |
| EV-18 | TimerDue | Published | Case and workflow | Rules component |
| EV-19 | TimerBreached | Published | Case and workflow | Notifications |
| EV-20 | InstructionIssued | Published | Partner management | Partner portal |
| EV-21 | PartnerResultSubmitted | Consumed | Partner portal | Case and workflow |
| EV-22 | AssetTakenOn | Published | Assets and auction | Timers (holding age) |
| EV-23 | LotAwarded | Published | Debt sale | Case and workflow (R-UNI-47) |
| EV-24 | WriteOffApproved | Published | Write-off and recovery | Posting |
| EV-25 | ProceedsMatched | Published | Payments and posting | Case and workflow |
| EV-26 | AceDataReady | Consumed | ACE ingestion, read through `v_ace_batch_status` | Case creation (JOB-02), reconciliation (JOB-04), payment matching (JOB-07), booking confirmation (JOB-08), write-off scan (JOB-16) |
| EV-27 | AceDataLate | Published | Recovery data engine, from `v_ace_batch_status` | Alerts, stale marker, data steward |
| EV-28 | AgentRunCompleted | Published | Agent runtime | Decision center, monitoring |

## The ACE batch record

EV-26 and EV-27 are not raised by a Workbench change. They come from the ACE batch record, one row per source system and business date, which the ACE team adds in RWB-ACE-001.

| Item | Detail |
|---|---|
| Read path | `recovery.v_ace_batch_status` |
| Grain | One row per `source_system` and `business_date` |
| Fields | `source_system`, `business_date`, `status`, `started_at`, `completed_at`, `record_count` |
| Ready | `status` is `COMPLETED` for the business date the Workbench expects |
| Late | That business date is still not complete at the Workbench cut-off for the source; the cut-off is configuration |
| Raised | EV-26 when the record completes; EV-27 when the cut-off passes first |
| Consumer action | Start the data jobs for that business date. No job reads a file and no job loads a row |

| Event | Payload |
|---|---|
| EV-26 AceDataReady | eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status, completedAt |
| EV-27 AceDataLate | eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status, completedAt |

The payload keeps the event naming convention. Each field maps one to one to the view column: `sourceSystem` is `source_system`, `businessDate` is `business_date`, `status` is `status`, and `completedAt` is `completed_at`.

## AsyncAPI 3.0

```yaml
asyncapi: 3.0.0
info:
  title: Recovery Workbench internal events
  version: 2.0.0
channels:
  CaseCreated:
    address: recovery.CaseCreated
    messages:
      CaseCreated:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            caseId: {type: string}
            caseNo: {type: string}
            productGroup: {type: string}
            accounts: {type: array}
            businessDate: {type: string}
  CaseAllocated:
    address: recovery.CaseAllocated
    messages:
      CaseAllocated:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            caseId: {type: string}
            queueId: {type: string}
            ownerId: {type: string}
            ruleId: {type: string}
            ruleVersion: {type: string}
  CaseAllocationFailed:
    address: recovery.CaseAllocationFailed
    messages:
      CaseAllocationFailed:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            caseId: {type: string}
            reason: {type: string}
            ruleGap: {type: string}
  CaseTransferred:
    address: recovery.CaseTransferred
    messages:
      CaseTransferred:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            caseId: {type: string}
            fromOwner: {type: string}
            toOwner: {type: string}
            reasonCode: {type: string}
  CaseStateChanged:
    address: recovery.CaseStateChanged
    messages:
      CaseStateChanged:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            caseId: {type: string}
            fromState: {type: string}
            toState: {type: string}
            ruleId: {type: string}
            decisionLogEntryId: {type: string}
  DeviationRaised:
    address: recovery.DeviationRaised
    messages:
      DeviationRaised:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            caseId: {type: string}
            deviationCode: {type: string}
            raisedBy: {type: string}
  DeviationCleared:
    address: recovery.DeviationCleared
    messages:
      DeviationCleared:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            caseId: {type: string}
            deviationCode: {type: string}
            outcome: {type: string}
  DecisionRecorded:
    address: recovery.DecisionRecorded
    messages:
      DecisionRecorded:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            entryId: {type: string}
            caseId: {type: string}
            decisionCode: {type: string}
            approver: {type: string}
  ApprovalRequested:
    address: recovery.ApprovalRequested
    messages:
      ApprovalRequested:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            approvalId: {type: string}
            caseId: {type: string}
            level: {type: string}
            amount: {type: string}
  TreatmentApproved:
    address: recovery.TreatmentApproved
    messages:
      TreatmentApproved:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            treatmentId: {type: string}
            caseId: {type: string}
            terms: {type: string}
  TreatmentBooked:
    address: recovery.TreatmentBooked
    messages:
      TreatmentBooked:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            treatmentId: {type: string}
            bookingRef: {type: string}
            businessDate: {type: string}
  PaymentMissed:
    address: recovery.PaymentMissed
    messages:
      PaymentMissed:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            treatmentId: {type: string}
            dueDate: {type: string}
            amountDue: {type: string}
  NoticeGenerated:
    address: recovery.NoticeGenerated
    messages:
      NoticeGenerated:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            noticeId: {type: string}
            caseId: {type: string}
            type: {type: string}
            templateVersion: {type: string}
  NoticeDispatched:
    address: recovery.NoticeDispatched
    messages:
      NoticeDispatched:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            noticeId: {type: string}
            barcode: {type: string}
            sentDate: {type: string}
  NoticeDelivered:
    address: recovery.NoticeDelivered
    messages:
      NoticeDelivered:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            noticeId: {type: string}
            deliveredAt: {type: string}
            status: {type: string}
  DocumentStored:
    address: recovery.DocumentStored
    messages:
      DocumentStored:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            documentId: {type: string}
            caseId: {type: string}
            type: {type: string}
            source: {type: string}
  DocumentFieldsExtracted:
    address: recovery.DocumentFieldsExtracted
    messages:
      DocumentFieldsExtracted:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            documentId: {type: string}
            fields: {type: array}
            confidence: {type: string}
  TimerDue:
    address: recovery.TimerDue
    messages:
      TimerDue:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            timerId: {type: string}
            caseId: {type: string}
            timerType: {type: string}
  TimerBreached:
    address: recovery.TimerBreached
    messages:
      TimerBreached:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            timerId: {type: string}
            caseId: {type: string}
            escalateTo: {type: string}
  InstructionIssued:
    address: recovery.InstructionIssued
    messages:
      InstructionIssued:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            instructionId: {type: string}
            partnerId: {type: string}
            type: {type: string}
            dueOn: {type: string}
  PartnerResultSubmitted:
    address: recovery.PartnerResultSubmitted
    messages:
      PartnerResultSubmitted:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            instructionId: {type: string}
            result: {type: string}
            documents: {type: array}
  AssetTakenOn:
    address: recovery.AssetTakenOn
    messages:
      AssetTakenOn:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            assetId: {type: string}
            caseId: {type: string}
            source: {type: string}
  LotAwarded:
    address: recovery.LotAwarded
    messages:
      LotAwarded:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            lotId: {type: string}
            buyerId: {type: string}
            price: {type: string}
  WriteOffApproved:
    address: recovery.WriteOffApproved
    messages:
      WriteOffApproved:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            writeOffId: {type: string}
            caseId: {type: string}
            amount: {type: string}
  ProceedsMatched:
    address: recovery.ProceedsMatched
    messages:
      ProceedsMatched:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            proceedsId: {type: string}
            caseId: {type: string}
            amount: {type: string}
  AceDataReady:
    address: recovery.AceDataReady
    messages:
      AceDataReady:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            sourceSystem: {type: string}
            businessDate: {type: string}
            status: {type: string}
            completedAt: {type: string, format: date-time}
  AceDataLate:
    address: recovery.AceDataLate
    messages:
      AceDataLate:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            sourceSystem: {type: string}
            businessDate: {type: string}
            status: {type: string}
            completedAt: {type: string, format: date-time}
  AgentRunCompleted:
    address: recovery.AgentRunCompleted
    messages:
      AgentRunCompleted:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            runId: {type: string}
            agent: {type: string}
            caseId: {type: string}
            outcome: {type: string}
            fallback: {type: string}
operations:
  sendCaseCreated:
    action: send
    channel:
      $ref: '#/channels/CaseCreated'
  sendCaseAllocated:
    action: send
    channel:
      $ref: '#/channels/CaseAllocated'
  sendCaseAllocationFailed:
    action: send
    channel:
      $ref: '#/channels/CaseAllocationFailed'
  sendCaseTransferred:
    action: send
    channel:
      $ref: '#/channels/CaseTransferred'
  sendCaseStateChanged:
    action: send
    channel:
      $ref: '#/channels/CaseStateChanged'
  sendDeviationRaised:
    action: send
    channel:
      $ref: '#/channels/DeviationRaised'
  sendDeviationCleared:
    action: send
    channel:
      $ref: '#/channels/DeviationCleared'
  sendDecisionRecorded:
    action: send
    channel:
      $ref: '#/channels/DecisionRecorded'
  sendApprovalRequested:
    action: send
    channel:
      $ref: '#/channels/ApprovalRequested'
  sendTreatmentApproved:
    action: send
    channel:
      $ref: '#/channels/TreatmentApproved'
  sendTreatmentBooked:
    action: send
    channel:
      $ref: '#/channels/TreatmentBooked'
  sendPaymentMissed:
    action: send
    channel:
      $ref: '#/channels/PaymentMissed'
  sendNoticeGenerated:
    action: send
    channel:
      $ref: '#/channels/NoticeGenerated'
  sendNoticeDispatched:
    action: send
    channel:
      $ref: '#/channels/NoticeDispatched'
  sendNoticeDelivered:
    action: send
    channel:
      $ref: '#/channels/NoticeDelivered'
  sendDocumentStored:
    action: send
    channel:
      $ref: '#/channels/DocumentStored'
  sendDocumentFieldsExtracted:
    action: send
    channel:
      $ref: '#/channels/DocumentFieldsExtracted'
  sendTimerDue:
    action: send
    channel:
      $ref: '#/channels/TimerDue'
  sendTimerBreached:
    action: send
    channel:
      $ref: '#/channels/TimerBreached'
  sendInstructionIssued:
    action: send
    channel:
      $ref: '#/channels/InstructionIssued'
  receivePartnerResultSubmitted:
    action: receive
    channel:
      $ref: '#/channels/PartnerResultSubmitted'
  sendAssetTakenOn:
    action: send
    channel:
      $ref: '#/channels/AssetTakenOn'
  sendLotAwarded:
    action: send
    channel:
      $ref: '#/channels/LotAwarded'
  sendWriteOffApproved:
    action: send
    channel:
      $ref: '#/channels/WriteOffApproved'
  sendProceedsMatched:
    action: send
    channel:
      $ref: '#/channels/ProceedsMatched'
  receiveAceDataReady:
    action: receive
    channel:
      $ref: '#/channels/AceDataReady'
  sendAceDataLate:
    action: send
    channel:
      $ref: '#/channels/AceDataLate'
  sendAgentRunCompleted:
    action: send
    channel:
      $ref: '#/channels/AgentRunCompleted'
```
