# Pipeline run (ALL, all stories)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Total time 411.7 s.

| Stage | Result |
|---|---|
| 1 Check | 12086 story rows |
| 2 Fixes (stories, X20) | 1504 line fixes, 88 lines held |
| 2 Fixes (Decision Log) | 3 decision rows cite an older version; 4 fix records |
| 4 Apply | 1508 of 1508 fixes applied over 763 files |
| 5 Re-check (stories) | 8933 rows (was 12086) |
| 5 Re-check (Decision Log) | 0 rows (expected 0) |

| Step | Seconds |
|---|---|
| detcheck.py | 197.6 |
| x20_fixes.py | 8.9 |
| declog_versions.py | 1.1 |
| apply_fixes.py | 10.6 |
| detcheck.py | 192.2 |
| declog_versions.py | 0.8 |

## Log

- detcheck.py: rc 0, 197.6 s: 1034 stories, 12086 rows, 81 assumptions, 197.4 s -> C:\Users\SahilMore\AppData\Local\Temp\claude\664128f151027658\db817fe5-3931-4d8e-b124-0e68970dbe8f\scratchpad\pipe\all\1-check
- x20_fixes.py: rc 0, 8.9 s: 1034 stories, 762 files with fixes, 1504 line fixes, 88 held -> C:\Users\SahilMore\AppData\Local\Temp\claude\664128f151027658\db817fe5-3931-4d8e-b124-0e68970dbe8f\scratchpad\pipe\all\2-fixes\stories
- declog_versions.py: rc 0, 1.1 s: 3 decision rows with older versions, 4 fix records -> C:\Users\SahilMore\AppData\Local\Temp\claude\664128f151027658\db817fe5-3931-4d8e-b124-0e68970dbe8f\scratchpad\pipe\all\2-fixes\declog
- apply_fixes.py: rc 0, 10.6 s: 1508/1508 fixes applied over 763 files -> C:\Users\SahilMore\AppData\Local\Temp\claude\664128f151027658\db817fe5-3931-4d8e-b124-0e68970dbe8f\scratchpad\pipe\all\4-applied
- detcheck.py: rc 0, 192.2 s: 762 stories, 8933 rows, 37 assumptions, 192.0 s -> C:\Users\SahilMore\AppData\Local\Temp\claude\664128f151027658\db817fe5-3931-4d8e-b124-0e68970dbe8f\scratchpad\pipe\all\5-recheck\stories
- declog_versions.py: rc 0, 0.8 s: 0 decision rows with older versions, 0 fix records -> C:\Users\SahilMore\AppData\Local\Temp\claude\664128f151027658\db817fe5-3931-4d8e-b124-0e68970dbe8f\scratchpad\pipe\all\5-recheck\declog
