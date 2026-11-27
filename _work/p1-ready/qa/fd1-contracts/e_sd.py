"""Batch D and request edits for rwb-source-data.yaml."""
from ed import API, Doc, ref

X = Doc(API + 'rwb-source-data.yaml')

# ---------------------------------------------------------------- header
X.sub('This document holds 29 operations under', 'This document holds 32 operations under', 'info.description', d='RD-P1-060')
X.sub('    Moved out of this document to another service: none.\n',
      '    Moved out of this document to another service: none.\n'
      '    Added by the D-RCV-60 P1 developer readiness run: GET /customers/{personKey}, GET /accounts/{accountKey} and\n'
      '    GET /collateral/{assetKey} (RD-P1-060).\n', 'info.description', d='RD-P1-060')
X.sub('  operations: 29\n', '  operations: 32\n', 'x-service.operations', d='RD-P1-060')

# ---------------------------------------------------------------- interaction ledger
P = '  /cases/{caseId}/interactions:'
X.sub('      description: Add query parameter actor. Interaction adds', '      description: Interaction adds',
      'GET /cases/{caseId}/interactions description (stale instruction removed)', within=P, f='RWB-P1-E1068-APP#4;RWB-P1-E1068-APP#23', d='RD-P1-004')
X.sub('event cannot be written (MSG-P7-003)', 'event cannot be written (MSG-GEN-006)',
      'GET /cases/{caseId}/interactions description (access-log failure code)', within=P, f='RWB-P1-E1068-APP#4', d='RD-P1-004')
X.sub('        an empty page with MSG-P3-024.\n',
      '        an empty page with MSG-P3-024. While the flag rwb.dataengine.ledger-read is off the operation answers 404 (RD-P1-045).\n',
      'GET /cases/{caseId}/interactions description (flag off)', within=P, d='RD-P1-045')
X.sub("      description: Schema Interaction adds deliveryStatus (string) and externalRef (string), returned by POST /cases/{caseId}/messages and in\n"
      "        the ledger.\n",
      "      description: 'Schema Interaction adds deliveryStatus (string) and externalRef (string), returned by POST /cases/{caseId}/messages and in\n"
      "        the ledger. REST callers, each under its own workload identity: rwb-case, rwb-comms, rwb-integration, rwb-document, rwb-payment,\n"
      "        rwb-treatment and rwb-partner; rwb-source-data appends in process (RD-P1-007, RD-P1-064). The same Idempotency-Key with another body\n"
      "        answers 409 MSG-PLT-N009-05; a new key with an existing business key answers 200 with the existing entry. On 503 MSG-P1-022 the caller\n"
      "        does not commit its action, or retries with the same header key and business key. While the flag rwb.dataengine.ledger-writer is off\n"
      "        the append path answers 404 (RD-P1-045).'\n",
      'POST /cases/{caseId}/interactions description', within=P, d='RD-P1-064;RD-P1-007;RD-P1-045', g='ASM-5391')
X.sub("      description: 'For eventCode LETTER (RWB-P1-E2021-APP): conductCheck is required when deliveryStatus is SENT or absent; externalRef is required when deliveryStatus is present.'\n",
      "      description: >-\n"
      "        For eventCode LETTER (RWB-P1-E2021-APP): conductCheck is required when deliveryStatus is SENT or absent; externalRef is required\n"
      "        when deliveryStatus is present. Ledger callers (RD-P1-064). Dispatch entry, appended by rwb-comms when the WIN file is sent: channel\n"
      "        LETTER, direction OUTBOUND, deliveryStatus SENT, externalRef = the WIN barcode of the notice, conductCheck PASSED, actorType SERVICE,\n"
      "        actorRef rwb-comms, sourceRef INT-14 WIN, idempotencyKey LETTER-<caseNo>-<yyyyMMdd of sent date>-<noticeId>. A letter refused by the\n"
      "        conduct check appends conductCheck BLOCKED with no deliveryStatus and no externalRef. Delivery entry, appended by rwb-comms only, one\n"
      "        per matched row of GET /proof-of-delivery: deliveryStatus from the row, externalRef = barcode, else noticeRef when barcode is null (a\n"
      "        row with neither gets no entry), occurredAt = callbackDate at 00:00 Asia/Bangkok, idempotencyKey\n"
      "        LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<u>, where <u> is the UUID version 5 of podKey in the RFC 9562 URL namespace. Hand-recorded\n"
      "        proof, through rwb-comms only: actorType USER, actorRef the user ID, externalRef = the barcode of the notice, idempotencyKey\n"
      "        LETTER-<caseNo>-<yyyyMMdd>-<id of the rwb-comms record of the hand entry>. Pending: mapping of WIN delivery_status to SENT,\n"
      "        DELIVERED, READ and FAILED, owner rwb-comms owner with the WIN interface owner, tracked as NEW-GAP-D3. Other entries: PROMISE when\n"
      "        the entry records a promise to pay, else CONTACT; SMS and LINE messages are CONTACT entries with channel SMS or LINE, direction\n"
      "        OUTBOUND and deliveryStatus; partner results are PARTNER_RESULT with actorType PARTNER and actorRef the partner code, over this\n"
      "        append; an answer given on HOME.SCB is CONTACT, INBOUND, channel PORTAL (Pending confirmation, owner product owner, NEW-GAP-F16-1),\n"
      "        actorType SERVICE, actorRef rwb-comms. No eventCode identifies a complaint (Pending, NEW-GAP-F10-02).\n",
      'InteractionRequest description', d='RD-P1-064;RD-P1-007', g='NEW-GAP-D3;NEW-GAP-F16-1;NEW-GAP-F10-02')

# ---------------------------------------------------------------- job monitor
P = '  /admin/jobs:'
def quote_extend(start, extra, section, within, **kw):
    """Turn a one-line plain description into a quoted one and append text."""
    line = [l for l in X.text.split('\n') if l.startswith('      description: ' + start)][0]
    X.sub(line, "      description: '" + line.split('description: ', 1)[1] + extra + "'", section, within=within, **kw)


quote_extend('One item per rwb-source-data run',
             ' Errors 422: size outside its range (MSG-GEN-002) or from later than to (MSG-GEN-003). While the flag rwb.p1.jobmonitor is off both job operations answer 404 MSG-P4-003 (RD-P1-045).',
             'GET /admin/jobs description', P, d='RD-P1-004;RD-P1-045', f='RWB-P1-AD018-CON#13;RWB-P1-AD018-CON#16')
X.add_response(P, '    get:', '404', ref('404'), 'GET /admin/jobs responses.404 (flag off)', d='RD-P1-045', f='RWB-P1-AD018-CON#16')
X.add_response(P, '    get:', '422', ref('422'), 'GET /admin/jobs responses.422', d='RD-P1-004', f='RWB-P1-AD018-CON#13')
P = '  /admin/jobs/{jobId}/rerun:'
X.sub("      - $ref: '#/components/parameters/IdempotencyKey'\n      responses:\n",
      "      - $ref: '#/components/parameters/IdempotencyKey'\n"
      "      description: 'Only a FAILED run is rerun: a new run for the same business date, started with Temporal reuse policy ALLOW_DUPLICATE_FAILED_ONLY. A complete or running run answers 409 MSG-P1-011 (RD-P1-012, RD-P1-065). While the flag rwb.p1.jobmonitor is off the operation answers 404 MSG-P4-003 (RD-P1-045).'\n"
      "      responses:\n",
      'POST /admin/jobs/{jobId}/rerun description', within=P, d='RD-P1-065;RD-P1-012;RD-P1-045')

# ---------------------------------------------------------------- freshness
P = '  /data-products/freshness:'
X.sub("      - name: product\n        in: query\n        required: false\n        schema:\n          type: string\n",
      "      - name: product\n        in: query\n        required: false\n        schema:\n          type: string\n          pattern: '^DP(0[1-9]|1[0-4])$'\n",
      'GET /data-products/freshness query product pattern (400 MSG-GEN-007)', within=P, d='RD-P1-005;RD-P1-004', f='RWB-P1-E1015-APP#6;RWB-P1-E1015-CON#7')
X.sub("A product is stale when no completed batch exists for the expected business date (RWB-E1-015).'\n",
      "A product is stale when no completed batch exists for the expected business date (RWB-E1-015). A never-stamped product answers businessDate null, status STALE, staleSince null and no sourceExtractedAt or loadedAt; a reader treats it as having no data date (RD-P1-062).'\n",
      'GET /data-products/freshness description', within=P, d='RD-P1-062')

# ---------------------------------------------------------------- records, catalog, dictionary, contracts
P = '  /data-products/{productCode}/records:'
X.add_response(P, '    get:', '422', ref('422'), 'GET /data-products/{productCode}/records responses.422 (page or size out of range)',
               d='RD-P1-005;RD-P1-004', f='RWB-P1-E2010-CON#7;RWB-P1-E1016-APP#22')
X.add_response('  /admin/data-products:', '    get:', '404', ref('404'), 'GET /admin/data-products responses.404 (flag rwb.source-data.product-access off)', d='RD-P1-045')
P = '  /admin/data-dictionary/fields:'
X.sub("sys_fields: 122 objects (92 tables and 30 v_ace_* views) and 1,366\n        fields.",
      "sys_fields: at least 123 objects (93 tables and 30 v_ace_* views) and 1,379\n        fields (RD-P1-025).",
      'GET /admin/data-dictionary/fields description counts', within=P, d='RD-P1-025', f='RWB-P1-E1064-APP#16')
X.add_response(P, '    get:', '404', ref('404'), 'GET /admin/data-dictionary/fields responses.404 (flag rwb.dataengine.data-dictionary off)', d='RD-P1-045')
X.add_response('  /admin/data-contracts:', '    get:', '404', ref('404'), 'GET /admin/data-contracts responses.404 (flag rwb.dataengine.data-dictionary off)', d='RD-P1-045')

# ---------------------------------------------------------------- readiness
P = '  /business-days/{date}/ready:'
X.sub("          description: Readiness check accepted; a repeat for the date replays 202\n",
      "          description: 'Readiness check accepted. A date that already has a business_day_readiness row answers 202 with the stored state: while AceIngestCheck runs the call attaches (USE_EXISTING); once the row is DONE or LATE it starts nothing. A second ReconciliationWorkflow run of a date exists only through the rerun of a FAILED run (RD-P1-040, RD-P1-065).'\n",
      'POST /business-days/{date}/ready 202 description', within=P, d='RD-P1-065;RD-P1-040')

# ---------------------------------------------------------------- EFS history
P = '  /efs-history:'
quote_extend('Reads one account from v_ace_efs_action',
      " On 409 the rwb-integration hand-over run waits on a durable timer and retries every 5 minutes until DP05 is stamped for the date or until handover.hold_until (Pending: parameter row, owner rwb-integration owner with RW-COE, NEW-GAP-D4; interim 09:00); at that limit it hands over without history and appends the rows when DP05 arrives (business key EFS:<efsRecordKey>). Only that run appends them (RD-P1-007, RD-P1-067). While the flag rwb.dataengine.efs-handover-reads is off the operation answers 404 (RD-P1-045).",
      'GET /efs-history description', P, d='RD-P1-067;RD-P1-045', g='NEW-GAP-D4')
X.sub("          description: Freshness gate refused; MSG-P1-001\n",
      "          description: 'Freshness gate refused, including a never-stamped DP01 or DP05; MSG-P1-001 (RD-P1-062)'\n",
      'GET /efs-history 409 (never stamped)', within=P, d='RD-P1-062;RD-P1-067')
X.add_response(P, '    get:', '404', ref('404'), 'GET /efs-history responses.404 (flag off)', d='RD-P1-045', f='RWB-P1-E2001-APP#5')

# ---------------------------------------------------------------- retention
X.add_response('  /retention-runs:', '    post:', '404', ref('404'), 'POST /retention-runs responses.404 (flag rwb.source-data.retention off)', d='RD-P1-045')
X.sub("              retentionMonths:\n                type: integer\n",
      "              retentionMonths:\n                type: integer\n                minimum: 1\n                maximum: 600\n                description: 'Outside the range: 422 MSG-GEN-002'\n",
      'RetentionRunRequest.rules.retentionMonths range', d='RD-P1-004', f='RWB-P1-E1017-CON#3;RWB-P1-E1017-CON#4')
X.sub("description: 'Pending: holdReport fields, owner Solution architect, tracked as GAP-3271.'",
      "description: 'Pending: holdReport fields, owner Solution architect, tracked as NEW-GAP-S5-1.'",
      'RetentionRun.holdReport gap citation', d='RD-P1-047', f='RWB-P1-E1017-CON#4;RWB-P1-E1017-CON#5', g='NEW-GAP-S5-1')

# ---------------------------------------------------------------- reconciliation, proof of delivery
P = '  /admin/reconciliation/results:'
X.sub("tracked as NEW-GAP-S2B-02.'\n",
      "tracked as NEW-GAP-S2B-02. P1 computes REC-01, REC-02 and REC-05 only; REC-04 and REC-06 are computed by the daily reconciliation of rwb-payment (RD-P1-069). rwb-case reads reconciliation results here. While the reconciliation flag is off the operation answers 404 MSG-P4-003 (RD-P1-045).'\n",
      'GET /admin/reconciliation/results description', within=P, d='RD-P1-069;RD-P1-045', g='NEW-GAP-S2B-02')
X.add_response(P, '    get:', '404', ref('404'), 'GET /admin/reconciliation/results responses.404 (flag off)', d='RD-P1-045')
P = '  /proof-of-delivery:'
X.sub("tracked as GAP-0577.'\n",
      "tracked as GAP-0577. rwb-comms is the one caller and the one appender of delivery ledger entries (RD-P1-064). While the flag rwb.dataengine.pod-read is off the read answers 200 with no row and DP07 STALE with a null businessDate (RD-P1-043); the answer has no member for the reason (Pending: GAP-0579). No read of held rows or of the REC-09 break is published in version 1 (GAP-0577, GAP-1508; RD-P1-069). Pending: capability area and right, tracked as NEW-GAP-S5-15.'\n",
      'GET /proof-of-delivery description', within=P, d='RD-P1-064;RD-P1-069;RD-P1-043', f='RWB-P1-E1055-APP#10;RWB-P1-E1055-APP#12', g='GAP-0577;GAP-0579;NEW-GAP-S5-15')

# ---------------------------------------------------------------- booking facts, batch status
NS = '; includes a never-stamped product, with {date} empty (wording Pending, NEW-GAP-D2; RD-P1-062)'
P = '  /booking-facts:'
X.sub("the account data is current as of another date'\n", "the account data is current as of another date" + NS + ". Flag rwb.dataengine.booking-facts off answers 404 (RD-P1-045)'\n",
      'GET /booking-facts 409 (never stamped)', within=P, d='RD-P1-062;RD-P1-045', g='NEW-GAP-D2')
P = '  /batch-status:'
X.sub("      description: 'RWB-P1-E2007-APP. Access: the booking-confirmation workload identity (rwb-integration).'\n",
      "      description: 'RWB-P1-E2007-APP. Access: the booking-confirmation workload identity (rwb-integration) and the rwb-payment workload identity (RD-P1-066). The answer carries the v_ace_batch_status checksum, used by the proceeds reconciliation of rwb-payment (RD-P1-069). While the flag rwb.dataengine.booking-facts is off the operation answers 404 (RD-P1-045).'\n",
      'GET /batch-status access and description', within=P, d='RD-P1-066;RD-P1-069;RD-P1-045')
X.sub("        feedVersion: {type: [string, 'null'], maxLength: 20}\n",
      "        feedVersion: {type: [string, 'null'], maxLength: 20}\n        checksum: {type: [string, 'null'], maxLength: 64, description: 'v_ace_batch_status.checksum'}\n",
      'BatchStatusAnswer.checksum', within='    BatchStatusAnswer:', d='RD-P1-069')

# ---------------------------------------------------------------- payments
P = '  /payments:'
a, b = X.block(P)
old = X.text[a:b]
i = old.index('      summary:')
j = old.index('      operationId:')
X.sub(old[i:j], '      summary: Read the payments of one business date or of one account\n', 'GET /payments summary', within=P, d='RD-P1-061')
a, b = X.block(P)
old = X.text[a:b]
i = old.index("      description: 'RWB-P1-E2008-APP.")
j = old.index('      responses:')
new = ("      description: 'Builder RWB-P1-E1013-APP; contract published in RWB-P1-E1015-CON (RD-P1-022, RD-P1-061). Exactly one of the queries businessDate or accountKey; both or neither answers 400 MSG-GEN-001 with field. businessDate form (rules of RWB-P1-E2008-APP): one row per payment_code from v_ace_payment for the date, ordered by paymentCode, with batchStatus and productStatus. accountKey form: the v_ace_payment rows of the account, ordered by paymentDate then paymentCode, in the same PaymentsAnswer shape with businessDate = the DP01 stamp in use. Both forms are unpaged (Pending: paging and row cap, owner data architect, GAP-0601, NEW-GAP-S10-04). Callers: date form - rwb-payment JOB-07 (RWB-P8-E2008-APP), RWB-P8-E4044-APP, RWB-P8-E4045-APP and RWB-P8-E4050-APP; account form - RWB-P1-E1013-APP baseline measures and gateway-bff. While the flag rwb.source-data.payment-facts is off the operation answers 404 (RD-P1-045).'\n"
       "      x-one-of-query: [businessDate, accountKey]\n"
       "      parameters:\n"
       "      - name: businessDate\n"
       "        in: query\n"
       "        required: false\n"
       "        schema: {type: string, format: date}\n"
       "      - name: accountKey\n"
       "        in: query\n"
       "        required: false\n"
       "        schema: {type: string, maxLength: 255}\n")
X.sub(old[i:j], new, 'GET /payments description and query forms', within=P, d='RD-P1-061;RD-P1-045', f='RWB-P1-E2008-APP;RWB-ITG-E1013-ITG#1', g='NEW-GAP-S10-14;NEW-GAP-S2B-17;GAP-0601;NEW-GAP-S10-04')
X.sub("the data is current as of another date'\n", "the data is current as of another date" + NS + "'\n",
      'GET /payments 409 (never stamped)', within=P, d='RD-P1-062', g='NEW-GAP-D2')
X.add_response(P, '    get:', '404', ref('404'), 'GET /payments responses.404 (flag off)', d='RD-P1-045')
P = '  /accounts/{accountKey}/installment-facts:'
X.sub("the data is current as of another date'\n", "the data is current as of another date" + NS + "'\n",
      'GET /accounts/{accountKey}/installment-facts 409 (never stamped)', within=P, d='RD-P1-062', g='NEW-GAP-D2')

# ---------------------------------------------------------------- contact points
X.add_response('  /contact-points:', '    get:', '404', ref('404'), 'GET /contact-points responses.404 (flag rwb.source-data.ledger-message off)', d='RD-P1-045')
P = '  /contact-points/{contactPointKey}/failed-contacts:'
X.sub("Pending: store of counted references, tracked as NEW-GAP-S10-17.'",
      "Counted references are processed_event rows (consumer rwb-source-data.failed-contacts; idempotency_key FC: followed by the lowercase hex SHA-256 of <contactPointKey>|<reference>; event_id null), written in one transaction with the failed_count increase; a repeat adds 1 to hit_count and answers 201 with counted false (RD-P1-070). While the flag rwb.source-data.ledger-message is off the operation answers 404 (RD-P1-045).'",
      'POST failed-contacts description', within=P, d='RD-P1-070;RD-P1-045', g='NEW-GAP-S10-17')

# ---------------------------------------------------------------- the three entity reads (RD-P1-060)
COMMON = ' Every read is written to the access log. Every field tagged is_personal passes through FieldMasker.mask for the user session or workload identity of the caller; a field with no rule is masked. GET only: no Idempotency-Key.'


def op(path, name, oid, summary, desc, schema):
    return ('  %s:\n'
            '    get:\n'
            '      tags: [Cases]\n'
            '      summary: %s\n'
            '      operationId: %s\n'
            '      x-module: P1\n'
            '      x-owner: P1\n'
            '      x-capability:\n'
            '        area: Case record\n'
            '        right: R\n'
            '      x-first-release: E1\n'
            "      description: '%s'\n"
            '      parameters:\n'
            '      - name: %s\n'
            '        in: path\n'
            '        required: true\n'
            '        schema: {type: string, maxLength: 255}\n'
            '      responses:\n'
            "        '200':\n"
            '          description: Success\n'
            '          content:\n'
            '            application/json:\n'
            '              schema:\n'
            "                $ref: '#/components/schemas/%s'\n") % (path, summary, oid, desc, name, schema) + \
        ''.join(ref(c) for c in ('400', '401', '403', '404', '503'))


paths = (
    op('/customers/{personKey}', 'personKey', 'getCustomer', 'Read the ACE customer of one person key',
       'RD-P1-060; builder RWB-P1-E1069-APP. The v_ace_customer columns, the contact points of v_ace_contact with consentStatus and verifiedAt of contact_point_ext, the party_ext facts and the DP02 freshness record. No freshness refusal: the caller applies its own stale rule. contactValue, firstName, lastName and the address columns are clear only when isUnmasked is true for the session, else masked. partyType, idType and segment are added when RWB-ACE-001 is deployed (DL43 flag, RD-P1-043). Callers: gateway-bff (case screen composite), rwb-comms, rwb-integration, rwb-deviation, rwb-case (portal offer view facts through gateway-bff) and RWB-P1-DM002-APP verification. The clear recipient name and postal address are read only here, by the rwb-comms notice and rwb-integration outbound-file workload identities. Pending: the masking rule rows that unmask them for those identities, owner data protection officer with the rwb-access owner, tracked as NEW-GAP-D1.' + COMMON,
       'Customer')
    + op('/accounts/{accountKey}', 'accountKey', 'getAccount', 'Read the ACE account of one account key',
         'RD-P1-060; builder RWB-P1-E1069-APP. The v_ace_account columns, the relations of v_ace_ca_relation, the account_ext facts and the DP01 freshness record. No freshness refusal. Callers: gateway-bff, rwb-case, rwb-payment (RWB-P8-E4045-APP, collectionsFee) and RWB-P3-E2006-APP. This is the single-account form; the multi-key account-page read stays Pending, GAP-3274.' + COMMON,
         'Account')
    + op('/collateral/{assetKey}', 'assetKey', 'getCollateral', 'Read the ACE collateral of one asset key',
         'RD-P1-060; builder RWB-P1-E1069-APP. The v_ace_collateral rows of the asset key, the v_ace_collateral_detail columns once Section B is live (DL43 flag, RD-P1-043) and the DP06 freshness record. No freshness refusal. Callers: RWB-P3-E2006-APP and rwb-asset. A date-wide DP06 read is not published (Pending, NEW-GAP-F10-03).' + COMMON,
         'Collateral')
)
X.insert_before('components:\n  parameters:\n', paths, 'paths /customers/{personKey}, /accounts/{accountKey}, /collateral/{assetKey}',
                d='RD-P1-060', f='RWB-P1-DM001-APP#1;RWB-P1-DM002-APP#1;RWB-PLT-N001-CON#1;RWB-P1-E1069-APP#1', g='GAP-0549;GAP-0566;NEW-GAP-F08-4;NEW-GAP-D1')


def col(name, t, extra=''):
    types = {'s': "type: [string, 'null']", 'd': "type: [string, 'null'], format: date", 'n': "type: [number, 'null']",
             'i': "type: [integer, 'null']", 'b': "type: [boolean, 'null']", 't': "type: [string, 'null'], format: date-time"}
    return '        %s: {%s%s}\n' % (name, types[t], extra)


def cols(spec, personal=()):
    return ''.join(col(n, t, ', x-personal-data: true' if n in personal else '') for n, t in (s.split(':') for s in spec.split()))


def sub_cols(spec, personal=()):
    return ''.join('      ' + line for line in cols(spec, personal).splitlines(True))


CUSTOMER = ('    Customer:\n'
            '      type: object\n'
            "      description: 'v_ace_customer in camelCase, with the contact points, the party_ext facts and the DP02 freshness (RD-P1-060). partyType, idType and segment are present once Section B is live.'\n"
            '      properties:\n'
            '        personKey: {type: string, maxLength: 255}\n'
            + cols('cifNo:s firstName:s lastName:s dateOfBirth:d deceasedDate:d deceasedFlag:b gender:s nationality:s maritalStatus:s '
                   'occupation:s spouseName:s customerStatus:s category:s countryOfResidence:s isStaff:b branchCode:s vatNumber:s '
                   'idNoMasked:s idNoLast4:s partyType:s idType:s segment:s',
                   ('firstName', 'lastName', 'spouseName', 'vatNumber', 'idNoMasked', 'idNoLast4'))
            + '        partyFacts:\n'
              "          description: 'The party_ext facts; null when the person has no party_ext row'\n"
              '          oneOf:\n'
              "          - $ref: '#/components/schemas/PartyExtFacts'\n"
              "          - type: 'null'\n"
              '        contacts:\n'
              '          type: array\n'
              '          items:\n'
              '            type: object\n'
              '            properties:\n'
              '              contactKey: {type: string, maxLength: 255}\n'
              '              contactType: {type: string, enum: [PHONE, EMAIL, ADDRESS]}\n'
            + sub_cols('usageCode:s contactValue:s contactValueMasked:s city:s postCode:s country:s',
                       ('contactValue', 'city', 'postCode', 'country'))
            + '              consentStatus: {type: string, enum: [GIVEN, WITHDRAWN, UNKNOWN]}\n'
              "              verifiedAt: {type: [string, 'null'], format: date-time}\n"
              '            required: [contactKey, contactType]\n'
              "        freshness: {$ref: '#/components/schemas/DataProductFreshness'}\n"
              '      required: [personKey, partyFacts, contacts, freshness]\n')

ACCOUNT = ('    Account:\n'
           '      type: object\n'
           "      description: 'v_ace_account in camelCase, with the customer-account relations, the account_ext facts and the DP01 freshness (RD-P1-060).'\n"
           '      properties:\n'
           '        accountKey: {type: string, maxLength: 255}\n'
           + cols('accountCode:s accountName:s accountStatus:s accountStatusDate:d contractNo:s contractDate:d productKey:s productType:s '
                  'productCategory:s productCategoryEfs:s branchCode:s branchName:s ocCode:s companyCode:s collectionOfficer:s '
                  'collectionPhase:s daysPastDue:i classification:s totalBalance:n accountingBalance:n pastDueAmount:n '
                  'totalInterestFinCharge:n collectionsFee:n interestRate:n lastPaymentDate:d lastPaymentAmount:n nextInstallmentDate:d '
                  'nextInstallmentAmount:n lastTdrDate:d tdrFlag:b rescheduledFlag:b numberReschedules:i tdrAging:i principleNotReduce:s '
                  'dataAsOf:d daysSinceLastContact:i daysSinceLastCollectionActivity:i relationshipManager:s relationshipManagerPhone:s '
                  'specialMemo:s expiryDate:d')
           + '        relations:\n'
             '          type: array\n'
             '          items:\n'
             '            type: object\n'
             '            properties:\n'
             '              personKey: {type: string, maxLength: 255}\n'
             '              accountKey: {type: string, maxLength: 255}\n'
           + sub_cols('relationType:s amountOfGuarantee:n dateOfGuarantee:d')
           + '            required: [personKey, accountKey]\n'
             '        accountFacts:\n'
             "          description: 'The account_ext facts; null when the account has no account_ext row'\n"
             '          oneOf:\n'
             "          - $ref: '#/components/schemas/AccountExtFacts'\n"
             "          - type: 'null'\n"
             "        freshness: {$ref: '#/components/schemas/DataProductFreshness'}\n"
             '      required: [accountKey, relations, accountFacts, freshness]\n')

COLLATERAL = ('    Collateral:\n'
              '      type: object\n'
              "      description: 'The v_ace_collateral rows of one asset key, the v_ace_collateral_detail columns once Section B is live, and the DP06 freshness (RD-P1-060).'\n"
              '      properties:\n'
              '        assetKey: {type: string, maxLength: 255}\n'
              '        rows:\n'
              '          type: array\n'
              "          description: 'One row per account-collateral-asset link'\n"
              '          items:\n'
              '            type: object\n'
              '            properties:\n'
              '              collateralNo: {type: string, maxLength: 255}\n'
              '              assetKey: {type: string, maxLength: 255}\n'
              '              accountKey: {type: string, maxLength: 255}\n'
              + sub_cols('collateralValue:n registerDate:d inActive:b collateralType:s description:s')
              + '            required: [assetKey, accountKey]\n'
                '        detail:\n'
                "          description: 'v_ace_collateral_detail; null while Section B is absent or when there is no row'\n"
                "          type: [object, 'null']\n"
                '          properties:\n'
              + ''.join('    ' + line for line in cols(
                    'titleDocNo:s plotNo:s areaText:s province:s district:s subdistrict:s insuredValue:n insuranceExpiry:d '
                    'lienRank:i sourceSystem:s dataAsOf:d').splitlines(True))
              + "        freshness: {$ref: '#/components/schemas/DataProductFreshness'}\n"
                '      required: [assetKey, rows, freshness]\n')

X.insert_before('    BusinessDayStatus:\n', CUSTOMER + ACCOUNT + COLLATERAL, 'components.schemas Customer, Account, Collateral', d='RD-P1-060', g='GAP-0549;GAP-0566')

# ---------------------------------------------------------------- shared components
X.sub("      description: Not found. The record does not exist or is outside the caller's scope. Messages MSG-P4-003\n",
      "      description: \"Not found. The record does not exist or is outside the caller's scope. Messages MSG-P4-003. Also answered while the feature flag of the operation is off (RD-P1-045); Pending: message ID of the flag-off 404 where the owning story names none, tracked as NEW-GAP-S10-01.\"\n",
      'components.responses.E404 (flag off)', d='RD-P1-045', g='NEW-GAP-S10-01')
X.sub("          description: ACE business date of the last completed batch; null only for a never-stamped product or while the Section B flag is off\n",
      "          description: ACE business date of the last completed batch; null only for a never-stamped product or while the Section B flag is off. A reader treats null as no data date (RD-P1-062)\n",
      'DataProductFreshness.businessDate', d='RD-P1-062')
X.sub("          description: ace_batch_run.completed_at\n", "          description: ace_batch_run.completed_at; absent for a never-stamped product\n",
      'DataProductFreshness.sourceExtractedAt', d='RD-P1-062')
X.sub("          description: Instant the Workbench wrote the freshness stamp\n", "          description: Instant the Workbench wrote the freshness stamp; absent for a never-stamped product\n",
      'DataProductFreshness.loadedAt', d='RD-P1-062')
X.sub("          description: First business date with no completed ACE batch; null when LOADED\n",
      "          description: First business date with no completed ACE batch; null when LOADED and for a never-stamped product, whose status is STALE\n",
      'DataProductFreshness.staleSince', d='RD-P1-062')

print(X.save())
