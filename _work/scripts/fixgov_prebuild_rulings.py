P = '01 Decisions and governance/Recovery Workbench RWB-E1-001 Pre-Build Rulings v2.md'
t = open(P, encoding='utf-8').read()

def rep(old, new):
    global t
    assert t.count(old) == 1, (old, t.count(old))
    t = t.replace(old, new)

rep('| Superseded by | D-RCV-35 |', '| Superseded by | Counts superseded by D-RCV-35 (section 0) |')
rep('The four answers and their reasoning stand. Where',
    'The four answers and their reasoning stand. Q4 (= R4 in the Specification Rulings) holds: the 14 definitions are seeded from the Conceptual Data Model v6 Data products tab, and the systems of record become "ACE (ingested from X)" - for example "ACE (ingested from ALS)" for DP01 - because ACE is the store the Workbench reads. Where')
rep('| Q4 - missing definitions | 1 - definitions from the CDM v5 Data products tab |',
    '| Q4 - missing definitions | 1 - definitions from the CDM v6 Data products tab |')
rep('Sourced from the CDM v5 Data products tab (identical text in Data Ownership v2); all 14 fit varchar(400) (longest 143 characters).',
    'Sourced from the CDM v6 Data products tab (v5 when first ruled); all 14 fit varchar(400) (longest 154 characters, DP02).')
rep('the 14 definitions are seeded from the CDM v5 Data products tab and repeated in the catalog load.',
    'the 14 definitions are seeded from the CDM v6 Data products tab and repeated in the catalog load.')
assert 'CDM v5' not in t and 'Conceptual Data Model v5' not in t
open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
