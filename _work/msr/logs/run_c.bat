@echo off
cd /d "C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
python -u -I "22 Microservice Realignment\compat\run_parallel.py" --queue C --max 24 --status "_work\msr\status-C.json" >> "_work\msr\logs\stageC.log" 2>&1
echo %ERRORLEVEL% > "_work\msr\logs\stageC.exit"
