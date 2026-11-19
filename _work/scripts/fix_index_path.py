import io

p = r'12 Project communication\Recovery Workbench Document Index v12.md'
t = io.open(p, encoding='utf-8-sig').read()
old = ('| 116 | Project hub for the squads | Every story, build note, code, term and original file in one page that works with no network and no sign-in. '
       'Version 16 is the ACE re-base of 15 November 2026: 323 live stories, the 30 recovery.v_ace_* views and the eight load stories removed. | Henka writing rules | '
       '14 Story Updates\\Recovery Workbench Project Hub v16.html |')
new = ('| 116 | Project hub for the squads | Every story, build note, code, term and original file in one page that works with no network and no sign-in. '
       'Version 16 is the ACE re-base of 15 November 2026: 323 live stories, the 30 recovery.v_ace_* views and the eight load stories removed. The file is in 14 Story Updates. | Henka writing rules | '
       'Recovery Workbench Project Hub v16.html |')
assert old in t
io.open(p, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
print('updated')
