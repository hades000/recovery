
Service contracts 4/7 · Communications, payment, partner

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  POST /notices (request) · GET /cases/{id}/notices
EVT  DeviationRaised / Cleared (contact stop) · TreatmentApproved, PaymentMissed · CaseStateChanged
TMP  NoticeDispatchWorkflow (kit template)

DB  writes schema rwb_comms: notices, templates, merge fields, proof of delivery
EVT  rwb.comms.events.v1: NoticeGenerated, NoticeDispatched, NoticeDelivered
TMP  Document: generate letter · Decision: child: approval · Integration: deliverFile (WIN letters)
REST  ACE Common: notification path (SMS, LINE)

P6 · rwb-comms
Communications
queue rwb-comms
rwb.comms.events.v1

IN

OUT

REST  GET /cases/{id}/payments · POST /proceeds/{id}/allocate (manual)
EVT  AceDataReady · TreatmentApproved, LotAwarded · AssetSold, WriteOffApproved
TMP  Act: matchPayments, confirmBookings · Act: postProceeds (saga step)

DB  writes schema rwb_payment: payment and proceeds matching, fees, bookings, posting files
EVT  rwb.payment.events.v1: TreatmentBooked, PaymentMissed, ProceedsMatched
TMP  Source data: payments for business date · Integration: deliverFile (posting file)

P8 · rwb-payment
Payments & posting
queue rwb-payment
rwb.payment.events.v1

IN

OUT

REST  Staff: GET/POST /partners, /instructions · Partner portal: /partner/v1/* (FAPI 2.0)
EVT  (work arrives as Temporal tasks)
TMP  InstructionWorkflow: SLA timers · Act: issueInstruction, recordResult

DB  writes schema rwb_partner: panel, partner users, instructions, results, fees, scorecards
EVT  rwb.partner.events.v1: InstructionIssued, PartnerResultSubmitted
REST  Document: partner uploads (link) · Partners (law firms, agencies, buyers): via partner gateway, MFA

S9 · rwb-partner
Partner management
queue rwb-partner
rwb.partner.events.v1

17

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-comms (P6, Communications)
IN: REST POST /notices (request); GET /cases/{id}/notices | events DeviationRaised / Cleared (contact stop); TreatmentApproved, PaymentMissed; CaseStateChanged | Temporal NoticeDispatchWorkflow (kit template)
OUT: schema rwb_comms (notices, templates, merge fields, proof of delivery) | topic rwb.comms.events.v1: NoticeGenerated, NoticeDispatched, NoticeDelivered | TMP Document: generate letter · Decision: child: approval · Integration: deliverFile (WIN letters) | REST ACE Common: notification path (SMS, LINE)

rwb-payment (P8, Payments & posting)
IN: REST GET /cases/{id}/payments; POST /proceeds/{id}/allocate (manual) | events AceDataReady; TreatmentApproved, LotAwarded; AssetSold, WriteOffApproved | Temporal Act: matchPayments, confirmBookings; Act: postProceeds (saga step)
OUT: schema rwb_payment (payment and proceeds matching, fees, bookings, posting files) | topic rwb.payment.events.v1: TreatmentBooked, PaymentMissed, ProceedsMatched | TMP Source data: payments for business date · Integration: deliverFile (posting file)

rwb-partner (S9, Partner management)
IN: REST Staff: GET/POST /partners, /instructions; Partner portal: /partner/v1/* (FAPI 2.0) | events (work arrives as Temporal tasks) | Temporal InstructionWorkflow: SLA timers; Act: issueInstruction, recordResult
OUT: schema rwb_partner (panel, partner users, instructions, results, fees, scorecards) | topic rwb.partner.events.v1: InstructionIssued, PartnerResultSubmitted | REST Document: partner uploads (link) · Partners (law firms, agencies, buyers): via partner gateway, MFA

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

