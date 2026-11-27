"""Recover the saved batch E decisions without promoting index entries to rulings."""
import csv
import re
from pathlib import Path

LOG=Path('../../24 P1 Developer Readiness v1')
STAGE=Path('stage/24 P1 Developer Readiness v1')
BATCH=LOG/'decisions/batch-E.md'
V2='Recovery Workbench P1 Decision Register v2'
V3='Recovery Workbench P1 Decision Register v3 draft'
STAGE.mkdir(parents=True,exist_ok=True)
(STAGE/'decisions').mkdir(exist_ok=True)

def fields(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f)
        return list(rd.fieldnames),list(rd)

def write_csv(path,header,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,header,lineterminator='\n',quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)

def label(body, name):
    m=re.search(r'^\*\*'+re.escape(name)+r'\.\*\*[ \t]*(.*)',body,re.M)
    return m[1].strip() if m else ''

source=BATCH.read_text(encoding='utf-8')
parts=re.split(r'^## (RD-P1-\d+) · (.+)\n',source,flags=re.M)
index={m[1]:(m[2],m[3]) for m in re.finditer(r'^\| (RD-P1-\d+) \| (.*?) \| (.*?) \|$',parts[0],re.M)}
sections={parts[i]:(parts[i+1],parts[i+2]) for i in range(1,len(parts),3)}
assert list(index)==[f'RD-P1-{i:03}' for i in range(75,101)]
assert list(sections)==list(index)[:14]
v2header,v2rows=fields(LOG/(V2+'.csv'))
batch_header,_=fields(LOG/'decisions/batch-D.csv')
batch_rows=[]
merged=[]
amendments={}
for key,(title,body) in sections.items():
    assert title==index[key][0]
    ruling=re.search(r'^\*\*Ruling\.\*\*\s*(.+?)(?=\n\n\*\*|\Z)',body,re.M|re.S)[1].strip()
    assert all(label(body,x) for x in ('Status','Reuse note')),key
    refs=re.findall(r'RD-P1-\d+',index[key][1].partition('amends ')[2])
    refs+=re.findall(r'RD-P1-\d+',label(body,'Amends'))
    for ref in dict.fromkeys(refs):
        amendments.setdefault(ref,[]).append(key)
    row=dict(decision_id=key,title=title,ruling=' '.join(ruling.splitlines()),
        affected_services=label(body,'Affected services'), affected_stories=label(body,'Affected stories'),
        affected_documents=label(body,'Affected documents'), themes='',findings=label(body,'Findings settled'),
        gap_asm=label(body,'GAP/ASM'), status='Recovered draft; application and verification pending',
        model='Claude Opus 5.5',escalation_items=index[key][1])
    batch_rows.append(row)
    merged.append({k:row.get(k,'') for k in v2header}|{
        'final_ruling':row['ruling'],'values_chosen_without_source':label(body,'Values chosen without a source')})
assert list(batch_rows[0])==batch_header
assert not set(sections)&{r['decision_id'] for r in v2rows}
for row in v2rows:
    refs=amendments.get(row['decision_id'],[])
    if refs:
        row['amended_by']='; '.join(filter(None,[row['amended_by'],*refs]))

write_csv(STAGE/'decisions/batch-E recovered draft.csv',batch_header,batch_rows)
write_csv(STAGE/(V3+'.csv'),v2header,v2rows+merged)
prior=(LOG/(V2+'.md')).read_text(encoding='utf-8')
prior=prior.replace('# '+V2,'# '+V3,1)
prior=prior.replace('| Version | v2, 27 November 2026 (v1 stays unchanged beside it) |',
                    '| Version | v3 draft, 27 November 2026 |',1)
prior=prior.replace('| Status | Proposed – Claude Opus 5.5 (applied) |','| Status | Batch E recovery draft. Application and verification pending. |',1)
prior=prior.replace('## Purpose','Batch E recovery includes 14 full rulings. RD-P1-089 to RD-P1-100 are index entries with no saved ruling text. Sections inherited from v2 retain their historical wording. Refer to the batch E amendment cross-reference when updating affected decisions.\n\n## Purpose',1)
for ref,targets in amendments.items():
    pattern=re.compile(r'(^## '+re.escape(ref)+r' · .+\n)',re.M)
    prior,n=pattern.subn(lambda m:m[1]+'\n**Draft batch E amendment.** See '+', '.join(targets)+'. Application and verification pending.\n',prior,count=1)
    assert n==1,ref
head='\n\n## Batch E recovered decision text\n\nSource: decisions/batch-E.md. The source states the proposed application status. This draft records the decision text and leaves application open.\n'
saved=source[source.index('## RD-P1-075 ·'):]
pending='\n\n## Batch E index entries awaiting ruling text\n\n| Planned ID | Question | Review references |\n|---|---|---|\n'
for key,(title,refs) in index.items():
    if key not in sections:
        pending+=f'| {key} | {title} | {refs} |\n'
out=STAGE/(V3+'.md')
out.write_text(prior.rstrip()+head+'\n'+saved.rstrip()+pending,encoding='utf-8',newline='\n')
_,b=fields(STAGE/'decisions/batch-E recovered draft.csv')
_,v=fields(STAGE/(V3+'.csv'))
assert len(b)==14 and len(v)==59 and len({r['decision_id'] for r in v})==59
assert saved.rstrip() in out.read_text(encoding='utf-8')
print('Recovered decisions:',len(b),'missing:',len(index)-len(b),'register rows:',len(v))
print('Draft amendment links:',amendments)

