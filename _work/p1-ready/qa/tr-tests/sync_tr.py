"""Runs W2 sync.py / prune.py unchanged except that edit-log rows go to TR-tests.csv. Usage: python -I sync_tr.py sync|prune [--write]"""
import sys, os
base = r'C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14/_work/p1-ready/w2-sync'
which = sys.argv[1]
path = base + '/' + which + '.py'
src = open(path, encoding='utf-8').read()
src = src.replace('W2-tests.csv', 'TR-tests.csv').replace('W2-tests-(', 'TR-tests-(').replace("'W2-tests-%04d'", "'TR-tests-%04d'")
src = src.replace("MODEL, 'W2-tests'", "MODEL, 'TR-tests'").replace("'claude-sonnet-5-5','W2-tests'", "'claude-sonnet-5-5','TR-tests'")
sys.argv = [path] + sys.argv[2:]
exec(compile(src, path, 'exec'), {'__file__': path, '__name__': '__main__'})
