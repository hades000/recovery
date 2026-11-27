"""rwb-case, rwb-access, rwb-comms, rwb-litigation, rwb-reporting, asyncapi and the messageCode pattern."""
import glob
import os
import re

from ed import API, BS, STAGE, Doc, ref

OLD = "'^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-" + BS + "d{3}$'"
NEW = "'^MSG-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{2,3}$'"

IDEM = ('  parameters:\n'
        '    IdempotencyKey:\n'
        '      name: Idempotency-Key\n'
        '      in: header\n'
        '      required: true\n'
        '      description: Canonical UUID key for one POST request.\n'
        '      schema:\n'
        '        type: string\n'
        '        format: uuid\n')
E400 = ('    E400:\n'
        '      description: Bad request. Messages MSG-GEN-001, MSG-GEN-007 and MSG-PLT-N009-03\n'
        '      content:\n'
        '        application/problem+json:\n'
        '          schema:\n'
        "            $ref: '#/components/schemas/Problem'\n")
E404 = ('    E404:\n'
        "      description: Not found. The record does not exist or is outside the caller's scope. Messages MSG-P4-003\n"
        '      content:\n'
        '        application/problem+json:\n'
        '          schema:\n'
        "            $ref: '#/components/schemas/Problem'\n")
PREF = "      - $ref: '#/components/parameters/IdempotencyKey'\n"


def add_idem(X, path, opid, d, f):
    """Declare the Idempotency-Key header on the POST of one path."""
    a, b = X.block(path)
    a, b = X._inner('    post:', a, b)
    seg = X.text[a:b]
    assert 'operationId: ' + opid in seg and 'IdempotencyKey' not in seg, opid
    if '\n      parameters:\n' in seg:
        seg = seg.replace('\n      parameters:\n', '\n      parameters:\n' + PREF)
    else:
        seg = seg.replace('\n      responses:\n', '\n      parameters:\n' + PREF + '      responses:\n')
    X.text = X.text[:a] + seg + X.text[b:]
    X.pending.append(('ADD', opid + ' header Idempotency-Key', '', PREF.strip(), d, f, ''))


def components_head(X, with404=False):
    """Add the IdempotencyKey parameter and the E400 (and E404) responses."""
    X.sub('  responses:\n    E401:\n', IDEM + '  responses:\n' + E400 + '    E401:\n',
          'components.parameters.IdempotencyKey and responses.E400', d='RD-P1-001;RD-P1-004')
    if with404:
        X.sub('    E409:\n', E404 + '    E409:\n', 'components.responses.E404', within='  responses:', d='RD-P1-004')


def key_codes(X):
    X.sub('Messages MSG-P3-005, MSG-GEN-004, MSG-P7-001, MSG-P7-002\n',
          'Messages MSG-P3-005, MSG-GEN-004, MSG-P7-001, MSG-P7-002, MSG-PLT-N009-05\n', 'components.responses.E409 (key reuse)', d='RD-P1-001')
    X.sub('Messages MSG-P7-003, MSG-GEN-006\n', 'Messages MSG-P7-003, MSG-GEN-006, MSG-PLT-N009-06\n',
          'components.responses.E503 (key store)', d='RD-P1-001')


def ops_count(X, old, new, d=''):
    X.sub('This document holds %d operations' % old, 'This document holds %d operations' % new, 'info.description operation count', d=d)
    X.sub('  operations: %d\n' % old, '  operations: %d\n' % new, 'x-service.operations', d=d)


# ---------------------------------------------------------------- rwb-case
X = Doc(API + 'rwb-case.yaml')
ops_count(X, 24, 25, d='RD-P1-063')
param = (
    '  /parameters/{key}:\n'
    '    get:\n'
    '      tags: [Administration]\n'
    '      summary: Read one parameter with its value in force\n'
    '      operationId: getParameter\n'
    '      x-module: P3\n'
    '      x-owner: P3\n'
    '      x-first-release: E1\n'
    "      description: 'RD-P1-028, RD-P1-063; builder RWB-P3-E1042-CON. Service workload identities only. The parameter catalog row and the value in force from parameter_value on the business date. A key the catalog does not list, or a parameter with secret true, answers 404 MSG-P4-003. One hop, 2 s. Consumer: rwb-source-data. Pending: name of the business date query parameter, owner rwb-case service owner, tracked as NEW-GAP-FD1-contracts-1.'\n"
    '      parameters:\n'
    '      - name: key\n'
    '        in: path\n'
    '        required: true\n'
    '        schema: {type: string, maxLength: 100}\n'
    '      responses:\n'
    "        '200':\n"
    '          description: The catalog row and the value in force\n'
    '          content:\n'
    '            application/json:\n'
    '              schema:\n'
    '                allOf:\n'
    "                - $ref: '#/components/schemas/Parameter'\n"
    '                - type: object\n'
    '                  properties:\n'
    '                    description: {type: string}\n'
    '                  required: [key, valueInForce, versionNo, validFrom]\n'
    + ''.join(ref(c) for c in ('401', '403', '404', '503')))
X.insert_before('components:\n  securitySchemes:\n', param, 'path GET /parameters/{key}', d='RD-P1-063;RD-P1-028',
                f='RWB-P3-E1042-APP#3;RWB-P1-E1068-APP#18', g='NEW-GAP-F11-8;NEW-GAP-FD1-contracts-1')
X.save()

# ---------------------------------------------------------------- rwb-access
X = Doc(API + 'rwb-access.yaml')
ops_count(X, 4, 5, d='RD-P1-063')
auth = (
    '  /authorise:\n'
    '    post:\n'
    '      tags: [Work]\n'
    '      summary: Answer whether the caller may act (allow or deny)\n'
    '      operationId: postAuthorise\n'
    '      x-module: P4\n'
    '      x-owner: P4\n'
    '      x-first-release: E1\n'
    "      description: 'RD-P1-063; builder RWB-P4-E1016-APP. Role, scope and delegation-of-authority check, cached in rwb-case. Pending: request and answer fields, owner rwb-access contract owner, tracked as NEW-GAP-F09-3. Until they are published a caller asserts only allow or deny and the Problem messageCode, never a role or scope value. An authorise check is written to the access log only and publishes no DecisionRecorded (RD-P1-072).'\n"
    '      parameters:\n' + PREF +
    '      requestBody:\n'
    '        required: true\n'
    '        content:\n'
    '          application/json:\n'
    '            schema:\n'
    '              type: object\n'
    "              description: 'Pending: request fields, tracked as NEW-GAP-F09-3'\n"
    '      responses:\n'
    "        '200':\n"
    "          description: 'Allow or deny. Pending: answer fields, tracked as NEW-GAP-F09-3'\n"
    '          content:\n'
    '            application/json:\n'
    '              schema:\n'
    '                type: object\n'
    + ''.join(ref(c) for c in ('400', '401', '403', '404', '409', '422', '503')))
X.insert_before('components:\n  securitySchemes:\n', auth, 'path POST /authorise', d='RD-P1-063;RD-P1-001;RD-P1-072',
                f='RWB-P4-E1016-APP#4;RWB-ITG-DM007-ITG#12', g='NEW-GAP-F09-3')
components_head(X, with404=True)
key_codes(X)
X.save()

# ---------------------------------------------------------------- rwb-comms
X = Doc(API + 'rwb-comms.yaml')
ops_count(X, 11, 18)
components_head(X)
key_codes(X)
D = 'RD-P1-001;RD-P1-004'
for path, opid, f in (('/cases/{caseId}/notices', 'postCasesCaseidNotices', 'RWB-P6-E1032-APP#3;RWB-P6-E1052-CON#1'),
                      ('/admin/templates', 'postAdminTemplates', 'RWB-P6-E1046-APP#2'),
                      ('/admin/templates/{templateId}/approve', 'postAdminTemplatesTemplateidApprove', 'RWB-P6-E1046-APP#2'),
                      ('/admin/templates/{templateId}/withdraw', 'postAdminTemplatesTemplateidWithdraw', 'RWB-P6-E1046-APP#3')):
    key = '  %s:' % path
    add_idem(X, key, opid, D, f)
    X.add_response(key, '    post:', '400', ref('400'), opid + ' responses.400', d=D, f=f)
    if path == '/admin/templates':
        X.add_response(key, '    post:', '409', ref('409'), opid + ' responses.409', d=D, f=f)
X.save()

# ---------------------------------------------------------------- rwb-litigation
X = Doc(API + 'rwb-litigation.yaml')
components_head(X)
key_codes(X)
for path, opid in (('/notices/{noticeId}/approve', 'postNoticesNoticeidApprove'),
                   ('/cases/{caseId}/legal-actions', 'postCasesCaseidLegalActions')):
    key = '  %s:' % path
    add_idem(X, key, opid, D, 'RWB-S4-E5001-APP#2')
    X.add_response(key, '    post:', '400', ref('400'), opid + ' responses.400', d=D, f='RWB-S4-E5001-APP#2')
X.save()

# ---------------------------------------------------------------- rwb-reporting
X = Doc(API + 'rwb-reporting.yaml')
F = 'RWB-P9-E1013-APP#6'
extra = ''
for code, text in (('400', 'Bad request. Messages MSG-GEN-001'), ('404', 'Not found. Messages MSG-P4-003'),
                   ('422', 'Unprocessable. A value fails validation. Messages MSG-GEN-001')):
    extra += ('    E%s:\n      description: %s\n      content:\n        application/problem+json:\n          schema:\n'
              "            $ref: '#/components/schemas/Problem'\n") % (code, text)
X.sub('  responses:\n    E401:\n', '  responses:\n' + extra + '    E401:\n', 'components.responses E400, E404, E422', d='RD-P1-004', f=F)
for code in ('400', '404', '422'):
    X.add_response('  /reports/measures:', '    get:', code, ref(code), 'GET /reports/measures responses.%s' % code, d='RD-P1-004', f=F)
X.save()

# ---------------------------------------------------------------- source-data asyncapi
X = Doc(API + 'asyncapi/rwb-source-data.asyncapi.yaml')
X.sub('Produced by rwb-source-data; consumers: rwb-case, rwb-payment, rwb-deviation, rwb-writeoff"',
      'Produced by rwb-source-data; consumers: rwb-case, rwb-payment, rwb-integration, rwb-deviation, rwb-writeoff. One event per source system and business date: no second AceDataReady is published for a stamped date (RD-P1-065). Daily work starts only on ALS with status COMPLETED; the monthly GL write-off reconciliation of rwb-writeoff starts on GL with status COMPLETED (RD-P1-066). Party flags are not carried: read GET /customers/{personKey} (RD-P1-060)"',
      'AceDataReady description and consumers', d='RD-P1-066;RD-P1-065;RD-P1-060;RD-P1-003')
X.sub('x-consumers: ["rwb-case", "rwb-payment", "rwb-deviation", "rwb-writeoff"]',
      'x-consumers: ["rwb-case", "rwb-payment", "rwb-integration", "rwb-deviation", "rwb-writeoff"]',
      'AceDataReady x-consumers', d='RD-P1-066;RD-P1-040')
groups = ('x-consumer-groups:\n'
          '- note: "One consumer group per service per topic, with one listener that starts that service\'s workflows by signal-with-start (RD-P1-003, RD-P1-066). rwb-source-data has no group on its own topic"\n'
          '  topic: "rwb.source-data.events.v1"\n'
          '  groups:\n'
          + ''.join('  - {group: "%s.rwb.source-data.events.v1", service: "%s", acl: "READ"}\n' % (s, s)
                    for s in ('rwb-case', 'rwb-payment', 'rwb-integration', 'rwb-deviation', 'rwb-writeoff', 'gateway-bff'))
          + 'x-retry-acl: "Each consumer service has WRITE and READ on <topic>.retry.1m, .retry.10m and .retry.1h and WRITE on <topic>.dlt of every topic it consumes (RD-P1-066)"\n')
X.insert_before('x-shared-topics:\n', groups, 'x-consumer-groups and x-retry-acl', d='RD-P1-066;RD-P1-003')
X.save()

# ---------------------------------------------------------------- decision record asyncapi
X = Doc(API + 'asyncapi/rwb.decision-record.v1.asyncapi.yaml')
X.sub('    Events carry IDs and facts, never personal data (Arch v5 slide 42 notes).\n',
      '    Events carry IDs and facts, never personal data (Arch v5 slide 42 notes).\n'
      '    A read is not a decision: reads and authorise checks go to the access log only and publish no DecisionRecorded\n'
      '    (RD-P1-072). rwb-decision owns chain_seq and prev_hash; a producer sets no chain field. Pending: fields that carry\n'
      '    the rule, versions and legacy hashes of a migrated entry, owner rwb-decision contract owner with compliance,\n'
      '    tracked as NEW-GAP-S13-4; migrated entries are not published until then (RD-P1-068).\n',
      'info.description (reads, chain fields, migrated entries)', d='RD-P1-072;RD-P1-068', g='NEW-GAP-S13-4')
X.save()

# ---------------------------------------------------------------- messageCode pattern, every file
for path in sorted(glob.glob(os.path.join(STAGE, API, '*.yaml')) + glob.glob(os.path.join(STAGE, API, 'asyncapi', '*.yaml'))):
    rel = os.path.relpath(path, STAGE).replace(BS, '/')
    X = Doc(rel)
    n = X.text.count(OLD)
    if not n:
        continue
    X.text = X.text.replace(OLD, NEW)
    X.pending.append(('EDIT', 'Problem messageCode pattern (%d places)' % n, OLD, NEW, 'RD-P1-001;RD-P1-004', '', ''))
    X.save()
    print(os.path.basename(path), n)
