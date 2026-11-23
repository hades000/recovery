import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
base = Path('04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration')
exp = {
 '1030': dict(key='RWB-ITG-E1030-ITG', legacy='RWB-E1-030', disp='Split (rework)', pat='DP01, DP03, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP17, DP19', dep='RWB-P3-E1030-APP, RWB-P7-E1030-APP'),
 '1031': dict(key='RWB-ITG-E1031-ITG', legacy='RWB-E1-031', disp='Split (rework)', pat='DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19', dep='RWB-P4-E1039-APP, RWB-P3-E1031-APP'),
 '1032': dict(key='RWB-ITG-E1032-ITG', legacy='RWB-E1-032', disp='Split (rework)', pat='DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19', dep='RWB-P5-E1032-APP, RWB-S9-E1032-APP, RWB-P3-E1032-APP, RWB-P6-E1032-APP, RWB-P7-E1032-APP'),
 '1034': dict(key='RWB-ITG-E1034-ITG', legacy='RWB-E1-034', disp='Moved (no impact)', pat='DP01, DP07, DP13, DP19', dep='RWB-P1-E1015-APP, RWB-P6-E1034-APP'),
 '1037': dict(key='RWB-ITG-E1037-ITG', legacy='RWB-E1-037', disp='Split (rework)', pat='DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP10, DP11, DP13, DP15, DP17, DP19', dep='RWB-P1-E1069-APP, RWB-PLT-E1037-APP, RWB-P4-E1037-APP'),
}
for k, e in exp.items():
    p = [x for x in base.glob('RWB ITG E%s ITG*.md' % k)][0]
    t = p.read_text(encoding='utf-8')
    def val(row):
        m = re.search(r'^\|\s*%s\s*\|\s*(.*?)\s*\|$' % re.escape(row), t, re.M)
        return m.group(1) if m else None
    checks = {
        'Story key': val('Story key') == e['key'],
        'Work type': val('Work type') == 'ITG (Integration)',
        'Owner': val('Suggested owner') == 'TechX (suggested; any team may pick up this story)',
        'Service': val('Service') == 'integration',
        'Epic': val('Service epic') == 'RWB-ITG-W1',
        'Wave': val('Wave') == '1',
        'Biz epic': val('Business epic') == 'EP01',
        'Release': val('Release') == '30 November 2026 (tentative)',
        'Legacy': val('Legacy key') == e['legacy'],
        'Disposition': val('Legacy disposition') == e['disp'],
        'Build': val('Build status') == 'Not started',
        'Patterns': val('Patterns applied') == e['pat'],
        'Lane': val('Parallel lane') == 'L-ITG-W1',
        'Ready': val('Ready to start') == 'Day 1',
        'H': val('Depends on (build)') == 'None',
        'C': val('Contract dependencies') == 'None',
        'I': val('Integration dependencies') == e['dep'],
        'X': val('External dependencies') == 'None',
        'PRD': val('PRD reference') == 'Pending (C1)',
        'Status': val('Status') == 'Draft (realignment v1)',
    }
    bad = [c for c, ok in checks.items() if not ok]
    print(e['key'], 'OK' if not bad else ('BAD ' + str(bad)))
