import csv, re, os, sys, collections
REV = r'C:\Users\SahilMore\Downloads\RWB Story Review P1'
OUT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\p1-ready\packets'
W = [  # (writer, regex on root_doc + conflicts_with + suggested_fix)
 ('W1-contracts', r'API Spec|\.yaml|OpenAPI|AsyncAPI|Service Contract Catalog|Contract Catalog'),
 ('W2-tests', r'Test Cases|\bRTM\b|Traceability|Regression Suite|Test Data Plan'),
 ('W3-messages', r'Error and Message|Message Standard|Error Handling|Resilience Standard|\bMSG-'),
 ('W4-data', r'Physical Schema|\bLDM\b|Logical Data Model|Data Dictionary|Reference Data|LOV|parameter catalog|parameter-catalog|Data Quality and Reconciliation'),
 ('W5-runtime', r'Kafka|Temporal|Batch and Scheduling|Workflow Engine|Event and Messaging'),
 ('W7-platform', r'Environment and Deployment|\bE&D\b|Observability|\bObs\b|Service Template|Non Functional|\bNFS\b|Integration Test Plan'),
 ('W8-reqs-security', r'\bPRD\b|\bFSD\b|\bTSD\b|Users Roles|Role to System|Delegation of Authority|Data Classification|Personal Data|Security and Access|ACE Source Views|ACE Field Gap|ACE Data Tier|Business Rules|Screen Spec|Business Requirements|\bBRD\b|Records Retention|Controls Catalog|Architecture'),
 ('W9-governance', r'Decision Log|Ownership Map|Service Story Catalog|Story Defects|Definition of Ready and Done|Document Index|Document Control|Dependency Map|Story Build Order|Service Catalog\b'),
 ('W6-registers', r'Gap Register|Assumptions Register|Cross-document Change|Service Review Pack'),
]
rows = [r for r in csv.DictReader(open(os.path.join(REV, 'all findings.csv'), encoding='utf-8-sig')) if r['severity'] != 'Rejected']
packets = collections.defaultdict(list); unrouted = 0
for r in rows:
    hay = ' '.join([r['root_doc'], r['conflicts_with'], r['suggested_fix']])
    hit = False
    for w, rx in W:
        if re.search(rx, hay, re.I): packets[w].append(r); hit = True
    if not hit: unrouted += 1
cols = ['story_key', 'gap_no', 'severity', 'type', 'codes', 'story_section', 'conflicts_with', 'suggested_fix', 'known_ref', 'verify_verdict', 'root_doc']
os.makedirs(OUT, exist_ok=True)
for w, rs in packets.items():
    with open(os.path.join(OUT, f'{w} findings.csv'), 'w', encoding='utf-8', newline='') as fh:
        wr = csv.writer(fh, quoting=csv.QUOTE_ALL); wr.writerow(cols)
        for r in rs: wr.writerow([r.get(c, '') for c in cols])
    print(w, len(rs))
print('unrouted (story-only)', unrouted, 'of', len(rows))
