@echo off
cd /d "C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
python -u -I "22 Microservice Realignment\compat\run_parallel.py" --queue D --max 24 --status "_work\msr\status-D.json" >> "_work\msr\logs\stageD.log" 2>&1
echo %ERRORLEVEL% > "_work\msr\logs\stageD.exit"
