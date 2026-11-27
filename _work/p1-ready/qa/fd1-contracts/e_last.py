"""gateway-bff error pass-through note, then NEW-GAP, NEW-ASM and outgoing REQUEST rows."""
from ed import API, Doc, log

X = Doc(API + 'gateway-bff.yaml')
X.sub('    from v4 and follow that base.\n',
      '    from v4 and follow that base.\n'
      '    Errors (RD-P1-063, RD-P1-004): a downstream Problem is passed through unchanged (status, messageCode, traceId);\n'
      '    the errors of the gateway itself use the same envelope. Pending: message code of the edge 500, owner platform edge\n'
      '    owner, tracked as NEW-GAP-F08-2.\n',
      'info.description (gateway error pass-through)', d='RD-P1-063;RD-P1-004', g='NEW-GAP-F08-2')
X.save()

A = '05 Technical architecture/Recovery Workbench API Specification v7/'
log('NEW-GAP', A + 'rwb-case.yaml', 'GET /parameters/{key}', '',
    'Name of the business date query parameter of GET /parameters/{key}; no source or ruling names it. Owner rwb-case service owner. Blocks build: No (path published).',
    'RD-P1-028;RD-P1-063', '', 'NEW-GAP-FD1-contracts-1', '', '')
log('NEW-ASM', A + 'rwb-source-data.yaml', 'schemas Customer, Account, Collateral', '',
    'NEW-ASM-FD1-contracts-1: Collateral answers assetKey, rows[] (one per account-collateral-asset link) and detail (object or null); the list items of Customer, Account and Collateral are inline, not named schemas. RD-P1-060 names no wrapper for the collateral rows.',
    'RD-P1-060', '', 'NEW-ASM-FD1-contracts-1', 'v6', 'v7')

REQ = [
    ('24 P1 Developer Readiness v1/Recovery Workbench P1 Decision Register v1.md', 'RD-P1-004 rule 2',
     'messageCode pattern is now ^MSG-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{2,3}$ in the contracts (MSG-PLT-N009-03, -05, -06 must validate); change the ruling text and any story or Error and Message Standard copy of the old pattern.', 'RD-P1-004', ''),
    ('23 Document Gaps', 'register rows',
     'Add NEW-GAP-FD1-contracts-1 and NEW-ASM-FD1-contracts-1; close NEW-GAP-S10-14, NEW-GAP-S2B-17 (account form answers PaymentsAnswer), NEW-GAP-S10-17 and NEW-GAP-F11-8; keep NEW-GAP-S5-1 (holdReport), NEW-GAP-F09-3, NEW-GAP-D1 to D4.', 'RD-P1-061;RD-P1-070;RD-P1-063', 'NEW-GAP-FD1-contracts-1'),
    ('05 Technical architecture/Recovery Workbench Service Catalog v2', 'sections 6.3, 6.4 and 6.1',
     'rwb-case provides GET /parameters/{key} and rwb-access POST /authorise in the 5.1.0 files; section 6.1 Temporal lists no payments activity while Service Contract Catalog v3 still carries the slide 17 pair (NEW-GAP-W1-contracts-2).', 'RD-P1-063', 'NEW-GAP-W1-contracts-2'),
    ('05 Technical architecture/Recovery Workbench Service Contract Catalog v3', 'REST operations owned of P2, P6, P7, P10, S1, S5',
     'Pre-existing drift from the Ownership Map, outside batch D: nine spec operations of P6 and P10 are not listed and nine listed operations of P2, P7, S1 and S5 are not in the specs. Contract owner at the service fixes.', '', ''),
    (A + 'rwb-comms.yaml', 'operationId', 'Pre-existing: four operations carry no operationId (GET /parties/{partyId}/contact-points, PUT /contact-points/{contactKey}, GET and POST /notices/{noticeId}/custody-movements). P6 contract fix.', '', ''),
    ('04 User stories RWB-P1-E1055-APP and -CON', 's12.1', 'getProofOfDelivery declares 400 as well as 401, 403, 422 and 503 (RD-P1-005 rule 9).', 'RD-P1-005', ''),
    ('04 User stories RWB-P1-E1013-APP, E1015-CON, E2008-APP', 's12.1', 'GET /payments takes exactly one of businessDate and accountKey (maxLength 255); both or neither 400 MSG-GEN-001; builder RWB-P1-E1013-APP.', 'RD-P1-061', ''),
    ('04 User stories RWB-P1-E1069-APP, E1016-APP, E1016-CON', 's12.1', 'GET /customers/{personKey}, /accounts/{accountKey}, /collateral/{assetKey} are published (schemas Customer, Account, Collateral; wrapper members partyFacts, contacts, relations, accountFacts, rows, detail, freshness).', 'RD-P1-060', ''),
    ('04 User stories RWB-P1-E1015-APP, E1015-CON', 's12.1', 'Freshness query product is restricted to DP01-DP14 (400 MSG-GEN-007).', 'RD-P1-005', ''),
]
for file, sec, text, d, g in REQ:
    log('REQUEST', file, sec, '', text, d, '', g, '', '')
print(len(REQ))
