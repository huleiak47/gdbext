@echo off

if exist %HOME%\.gdbinit del %HOME%\.gdbinit

cp .gdbinit %HOME%\.gdbinit
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

echo so %~dp0init.py >> %HOME%\.gdbinit
