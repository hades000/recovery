import re, os

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14'
P = os.path.join(ROOT, r'12 Project communication\Recovery Workbench Document Index v12.md')

WHAT = {
 '10': 'Where each piece of information comes from, how ACE ingests it, how the Workbench reads it through a view, how often, and what happens when it does not arrive.',
 '11': 'Every entity with every field: name, type, length, mandatory, default, list of values, key, and the ACE table and column each external field is read from.',
 '25': 'Every system recovery uses today, whether ACE already ingests it and who owns that ingestion, what happens to each and when, and every interface with its route, direction and frequency.',
 '26': 'Create statements with indexes, constraints, the four extension tables, the ACE views and seed reference data, for Postgres.',
 '32': 'Every field classified by sensitivity, with the personal data fields named, the ACE column that holds each one and the handling rule, including the masking in the views.',
 '36': 'Per interface: approach, trigger, payload fields, frequency, volume, error handling, retry and owner, with the inbound interfaces owned by ACE and the outbound by the Workbench.',
 '46': 'Every Workbench view field mapped from the ACE column that holds it, with the source system ACE ingests from, the transform in the view and the refresh.',
 '61': 'What is reconciled to ACE, the tolerance, and what happens when a check fails.',
 '74': 'Every scheduled job: what it does, when it runs against the ACE batch-complete record, what it depends on, and what happens when it fails or runs late.',
 '99': 'Which history is already in ACE, what still moves, what happens to cases in flight, and whether there is a parallel run.',
 '101': 'Reconcile the ACE data behind each data product, validate it, cut over and prove it, one story per data product.',
 '116': 'Every story, build note, code, term and original file in one page that works with no network and no sign-in. The v16 rebuild on the ACE re-base is outstanding; the v15 build in 14 Story Updates predates it.',
}

row_re = re.compile(r'^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$')
lines = open(P, encoding='utf-8').read().split('\n')
hit = set()
for i, line in enumerate(lines):
    m = row_re.match(line)
    if m and m.group(1) in WHAT:
        rid, doc, what, std, files = m.groups()
        lines[i] = '| %s | %s | %s | %s | %s |' % (rid, doc, WHAT[rid], std, files)
        hit.add(rid)
open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('updated', len(hit), 'of', len(WHAT), 'missing', sorted(set(WHAT) - hit))
