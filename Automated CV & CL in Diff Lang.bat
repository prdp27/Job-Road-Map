@echo off

:START

cd /d "D:\prdp\Data Analytics\Job Raod Map"

"D:\prdp\Data Analytics\.venv\Scripts\python.exe" "Automated CV & CL in Diff Lang.py"

echo.
choice /C YN /M "Do you want to run again"

if errorlevel 2 goto END
if errorlevel 1 goto START

:END
exit