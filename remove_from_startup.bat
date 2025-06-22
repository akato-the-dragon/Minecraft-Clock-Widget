@echo off
setlocal enabledelayedexpansion

:: Switch to script directory
cd /d "%~dp0"

:: Automatically find first EXE file in directory
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

:: Request admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Define paths for removal
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_NAME=MinecraftClockWidget.lnk"

:: Terminate program
taskkill /f /im "%APP_EXE%" >nul 2>&1

:: Remove shortcut from startup
del "%STARTUP_DIR%\%SHORTCUT_NAME%" >nul 2>&1

:: Remove launcher script
del "%~dp0app_launcher.vbs" >nul 2>&1

echo Shortcut removed from Startup folder: 
echo %STARTUP_DIR%\%SHORTCUT_NAME%
echo Program "%APP_EXE%" uninstalled from autorun.
timeout /t 3 >nul
exit