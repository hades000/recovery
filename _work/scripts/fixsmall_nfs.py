import sys; sys.path.insert(0, r'_work/scripts')
from fixsmall_lib import load, rep1, set_modified, save
P = r'03 Requirements and specifications/Recovery Workbench Non Functional Specification v3.docx'
z, x, core = load(P)
# 3.2 intro: NFR-008/NFR-009 include view reads
x = rep1(x, '95th percentile read from the traces.',
         '95th percentile read from the traces. The NFR-008 and NFR-009 targets include reads through the recovery.v_ace_* views, with ACE and recovery data joined at the busiest hour.')
# NFR-015 target and status
x = rep1(x, 'End of day; in the Workbench the next morning. Same-day needs are named under DL06',
         'Visible as soon as the ACE batch completes; no Workbench lag; same-day needs under DL06')
x = rep1(x, 'Proposed</w:t>', 'Proposed, DL43</w:t>', start='NFR-015<')
# 1 Freshness row (matches NFR-018)
x = rep1(x, 'reconciled to the core bank every day', 'reconciled to the ACE account view every day')
# NFR-032 (coordinator: identical to BRD Program v4); owner and status unchanged
x = rep1(x, 'A retired local file is kept as a read-only archive at a recorded location.',
         'Under D-RCV-35 (U5), retired local files and Excel and SharePoint trackers are handled through the Cutover and Go Live Plan, which keeps each as a read-only archive at a recorded location. The Workbench loads and holds no tracker.')
x = rep1(x, 'Archive location recorded per file<', 'Archive location recorded per file in the Cutover and Go Live Plan<')
save(P, z, x, set_modified(core))
print('NFS done')
