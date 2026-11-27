"""One REQUEST-DONE or REQUEST-REJECTED row per request row aimed at the contract files."""
import csv
import os
import re

from ed import ROOT, log

rows = {r['edit_id']: r for r in csv.DictReader(open(os.path.join(ROOT, 'packets', 'requests all agents.csv'), encoding='utf-8-sig'))}
ids = [l.split()[1] for l in open(os.path.join(ROOT, 'qa', 'fd1-contracts', 'myrequests.txt'), encoding='utf-8') if l.startswith('[')]
ids.append('S2b-stories-0222')
assert len(ids) == len(set(ids)) == 85

DONE = {}
REJ = {}


def done(why, *i):
    for x in i:
        DONE[x] = why


def rej(why, *i):
    for x in i:
        REJ[x] = why


by_index = lambda *n: [ids[k] for k in n]

done('GET /admin/reconciliation/results and /{resultId} are in rwb-source-data.yaml 5.1.0; flag-off 404, REC owner note added.', *by_index(0, 2, 7, 10, 11))
done('GET /payments published as one operation with the query forms businessDate or accountKey (RD-P1-061; accountKey is the wire name of accountId).', *by_index(1, 39))
done('GET /proof-of-delivery is in rwb-source-data.yaml 5.1.0 with the rwb-comms access and flag behaviour stated.', *by_index(3, 4, 8))
done('GET /booking-facts and GET /batch-status are in the file (checksum and rwb-payment access added).', *by_index(5, 37))
done('GET /payments and GET /accounts/{accountKey}/installment-facts are in the file.', *by_index(6))
done('GET /contact-points, POST failed-contacts and Interaction.barcodeStatus are in the file; counted-reference store stated (RD-P1-070).', *by_index(9, 41, 40))
done('POST /authorise published in rwb-access.yaml with request and answer Pending (NEW-GAP-F09-3). GET /masking-policies and the rwb-partner staff read are not added: no ruled shape (GAP-0983; NEW-GAP-F07-02).', *by_index(12, 18, 67))
rej('Pending, owner S9 contract owner (NEW-GAP-F07-02, RD-P1-063 rule 6): no ruled staff read of one instruction.', *by_index(13, 68))
rej('Pending, owner S7 contract owner (NEW-GAP-F07-02, RD-P1-063 rule 6): no ruled read of a write-off decision.', *by_index(14))
done('Catalog gateway-bff rows now read GET /customers/{personKey}, GET /accounts/{accountKey} and GET /data-products/freshness (RD-P1-060).', *by_index(15))
done('GET /customers/{personKey}, /accounts/{accountKey} and /collateral/{assetKey} published with schemas Customer, Account and Collateral (RD-P1-060).', *by_index(16, 46, 47, 64))
done('Staged asyncapi carries rwb.decision.DecisionRecorded.v1, the two headers and rwb-source-data as consumer.', *by_index(17, 77))
done('PUT /extension-facts operations are in 5.1.0 with If-Match; the first-write value stays Pending (NEW-GAP-W1-contracts-1).', *by_index(19))
done('GET /parameters/{key} (getParameter) added to rwb-case.yaml and listed in the Catalog (RD-P1-063 rule 3); date query name Pending (NEW-GAP-FD1-contracts-1).', *by_index(20, 21, 63))
rej('Not added: the story gives no member names for the run state or the retry answer; owner P6 contract owner at the rwb-comms fix (GAP-1166).', *by_index(22))
done('Contract keeps `product`; RWB-P1-E1015-CON text is corrected by the story editor (RD-P1-063 rule 2).', *by_index(23))
done('Idempotency-Key header, 400 and the key-conflict and key-store codes declared (RD-P1-001, RD-P1-004); 409 added on postAdminTemplates.', *by_index(24, 25, 27, 33))
done('Answered by RD-P1-060 rule 4: the DP02 records read keeps no contact value for every caller; clear values come only from GET /customers/{personKey} (masking rows Pending, NEW-GAP-D1).', *by_index(26))
rej('POST /internal/pod-digests is a service-internal write of rwb-comms with no published member names; owner P6 contract owner. Not added to the published contract in this run.', *by_index(28))
rej('The yaml keeps 400 (RD-P1-005 rule 9: every operation declares 400); RWB-P1-E1055-APP aligns its error list.', *by_index(29))
rej('Not P1 and no ruling gives the shapes: the rwb-document retention operations are for the P5 contract fix (RD-P1-047 rules the P1 side only, which is published).', *by_index(30))
rej('Consumption not confirmed (NEW-GAP-F18-2 open); no pair added.', *by_index(31))
rej('RD-P1-067 rule 1 amends RD-P1-010 rule 8: the /efs-history gate is DP01 and DP05, so the description is correct.', *by_index(32))
done('Checked: only rwb-comms is a consumer of GET /proof-of-delivery in the Catalog.', *by_index(34))
done('GET /reports/measures declares 400, 404 and 422 with Problem. GET /measure-definitions is not added: no member names ruled; owner P9 contract owner.', *by_index(35))
done('GET /efs-history is in the file; 404 while flagged off added (RD-P1-045).', *by_index(36, 72))
rej('The fake and the workload-identity permission belong to the rwb-case contract and the access matrix; the Catalog already lists rwb-source-data as consumer of GET /cases/{caseId}/accounts.', *by_index(38))
done('422 added on GET /data-products/{productCode}/records.', *by_index(42))
rej('Pending GAP-2696: no ruled response shape for the treatment reads; owner S2 contract owner.', *by_index(43))
rej('Pending GAP-2738: no ruled response shape for the guarantee claim read; owner S3 contract owner.', *by_index(44))
done('rwb-access authorise consumption listed. The treatment and guarantee window reads are not catalogued: not published (GAP-2696, GAP-2738).', *by_index(45))
rej('Pending NEW-GAP-S13-4 (RD-P1-068 rule 1): no field added; the asyncapi description now states the interim and that migrated entries are not published.', *by_index(48, 71))
done('Checked: no Catalog row makes rwb-source-data a consumer of reference-loads or verify; GET /admin/lists/{listCode} is listed.', *by_index(49))
done('Aggregate reads are published; break detail stays Pending (GAP-1508, NEW-GAP-S2B-03; RD-P1-069 rule 1).', *by_index(50))
rej('Pending GAP-3273 / GAP-0337: no ruled path or shape for the dated allocation, exclusion and open-case reads; owner rwb-case service owner.', *by_index(51))
done('Query `product` restricted to DP01-DP14 (400 MSG-GEN-007). Gate value member not added (NEW-GAP-S3-7 not ruled); account-page read stays GAP-3274.', *by_index(52))
done('Staged asyncapi is 5.1.0 with key sourceSystem:businessDate and typed payload (verified, RD-P1-063 rule 1).', *by_index(53, 76))
rej('Not a file edit: baselining the contract and publishing the 5.1.0 fake are delivery steps (RD-P1-011).', *by_index(54))
rej('Published artefact already follows RD-P1-004/005; FieldValue.value stays type string because no ruling or source gives a non-text encoding; owner P1 contract owner.', *by_index(55))
done('422 added on the records read. FieldValue.value typing for non-text values not changed: no ruling gives the encoding.', *by_index(56))
rej('GET /retention-classes belongs to the P5 contract (RWB-P5-AD021-CON); not published in this run, no ruled change to rwb-document.yaml.', *by_index(57))
done('holdReport now cites NEW-GAP-S5-1.', *by_index(58))
done('retentionMonths minimum 1, maximum 600 (MSG-GEN-002).', *by_index(59))
done('Description states the flag-closed answer, the missing reason member (GAP-0579) and the Pending capability (NEW-GAP-S5-15); no member or x-capability invented.', *by_index(60))
done('Dictionary counts now at least 123 objects and 1,379 fields. 422 not declared until a maximum size is set.', *by_index(61))
done('Stale instruction removed; access-log failure answers MSG-GEN-006.', *by_index(62))
done('GET /admin/jobs declares 422 and 404 MSG-P4-003; the rerun description covers the flag.', *by_index(65))
done('Counts recounted from the files: rwb-comms 18, rwb-agent 13, rwb-source-data 32, rwb-case 25, rwb-access 5; x-totals 174.', *by_index(66))
rej('Pending GAP-3271 (widened by RD-P1-065 rule 2): rwb-case serves JOB-03 and JOB-06 reads and reruns; no ruled path or shape.', *by_index(69))
rej('No event or field added (RD-P1-003, RD-P1-066 rule 4, RD-P1-060 rule 5): GL starts on AceDataReady GL/COMPLETED; flags come from GET /customers/{personKey}. The asyncapi description now says so.', *by_index(70))
done('messageCode pattern widened in all 20 OpenAPI files: ^MSG-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{2,3}$. The Decision Register text of RD-P1-004 needs the same change (request raised).', *by_index(75))
done('Verified: Problem schema, E400/E409/E428/E503 and Idempotency-Key are in rwb-source-data.yaml (first W1 pass); error envelope line in Catalog 3.3.', *by_index(73, 74))
done('rwb-document asyncapi requires ce_actor and ce_idempotencykey (verified).', *by_index(78))
done('Verified: job monitor run set, failed-only rerun and retention-run operations are published.', *by_index(79))
done('Verified: GET /cases/retention-exclusions and /cases/closure-dates are in rwb-case.yaml.', *by_index(80))
done('Catalog section 6.1 and the Temporal contracts sheet list the P1 workflows, activities, FreshnessQuery, events, consumer groups and retention ownership.', *by_index(81, 83))
rej('Not a contract file: Test Cases belong to the W2-tests writer.', *by_index(82))
done('GET /payments account form published for rwb-source-data.yaml (RD-P1-061); the fake is a delivery step (RD-P1-011).', 'S2b-stories-0222')

assert set(DONE) | set(REJ) == set(ids), sorted(set(ids) - set(DONE) - set(REJ))
assert not set(DONE) & set(REJ)
for i in ids:
    r = rows[i]
    action = 'REQUEST-DONE' if i in DONE else 'REQUEST-REJECTED'
    log(action, r['file'], r['section'], r['after'], DONE.get(i) or REJ.get(i), r['decision_refs'], i, r['gap_asm_refs'])
print(len(DONE), 'done', len(REJ), 'rejected')
