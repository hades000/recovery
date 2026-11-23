<!-- source: 05 Technical architecture/Recovery Workbench Event and Messaging Design v2.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `05 Technical architecture/Recovery Workbench Event and Messaging Design v2.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench event and messaging design

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

The Workbench publishes and consumes events inside the ACE service. Each event is written to the outbox in the same transaction as the change that raises it, and delivered to its consumers at least once. There is no external event bus today; data from other systems arrives by the COLLINS daily load and file loads (DT12). If a same-day feed is approved under DL06, the same events are published to it without changing their payloads.

## Rules

| Rule | Detail |
|---|---|
| Ordering | Events for one case are processed in the order they were written, by a sequence per case in the outbox |
| Delivery | At least once; consumers are idempotent |
| Duplicates | Each event carries an event ID and an idempotency key; a repeat is ignored and counted (R-UNI-40) |
| Transactions | The event is written in the same transaction as the change; no event without the change and no change without the event |
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
| EV-26 | LoadCompleted | Consumed | Recovery data engine | Case creation, matching |
| EV-27 | LoadRefused | Published | Recovery data engine | Alerts, stale marker |
| EV-28 | AgentRunCompleted | Published | Agent runtime | Decision center, monitoring |

## AsyncAPI 3.0

```yaml
asyncapi: 3.0.0
info:
  title: Recovery Workbench internal events
  version: 1.0.0
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
  LoadCompleted:
    address: recovery.LoadCompleted
    messages:
      LoadCompleted:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            source: {type: string}
            businessDate: {type: string}
            rows: {type: string}
            checks: {type: string}
  LoadRefused:
    address: recovery.LoadRefused
    messages:
      LoadRefused:
        payload:
          type: object
          properties:
            eventId: {type: string, format: uuid}
            occurredAt: {type: string, format: date-time}
            schemaVersion: {type: integer}
            source: {type: string}
            businessDate: {type: string}
            failedCheck: {type: string}
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
  receiveLoadCompleted:
    action: receive
    channel:
      $ref: '#/channels/LoadCompleted'
  sendLoadRefused:
    action: send
    channel:
      $ref: '#/channels/LoadRefused'
  sendAgentRunCompleted:
    action: send
    channel:
      $ref: '#/channels/AgentRunCompleted'
```
