@echo off
cd /d "C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
python -u -I "22 Microservice Realignment\compat\run_parallel.py" --queue B2 --max 24 --status "_work\msr\status-B2b.json" >> "_work\msr\logs\stageB2.log" 2>&1
echo %ERRORLEVEL% > "_work\msr\logs\stageB2.exit"
