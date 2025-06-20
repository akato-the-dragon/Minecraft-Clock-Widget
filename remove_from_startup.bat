@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "APP_EXE="
for %%i in (*.exe) do (
    if not "%%i"=="%~nx0" (
        set "APP_EXE=%%i"
        goto :exe_found
    )
)

:exe_found
if not defined APP_EXE (
    echo Error: No EXE file found in current directory.
    pause
    exit /b
)

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

taskkill /f /im "%APP_EXE%" >nul 2>&1

reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "MinecraftClockWidget" /f >nul 2>&1

echo Program "%APP_EXE%" terminated and removed from autorun.
timeout /t 3 >nul
exit