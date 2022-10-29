@echo off

echo.
echo Running Scheduling Reboot Task.
echo.


For /F "Tokens=1*Delims=\" %%# In ('SchTasks /Query /FO List^|Find /I "RebootTask"')Do @SchTasks /Delete /TN "%%$" /F

<nul set /p="Y" |SCHTASKS /Create /SC weekly /D WED /TN "RebootTask" /ST 06:30 /TR "%SystemRoot%\system32\shutdown.exe -r -f -t 10" /RU %USERNAME% /RL HIGHEST

pause
echo.
echo Completed.
echo.