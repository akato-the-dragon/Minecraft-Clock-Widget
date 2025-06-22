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

:: Create startup folder shortcut
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_NAME=MinecraftClockWidget.lnk"

:: Create shortcut using VBS script
set "VBS_SCRIPT=%TEMP%\create_shortcut.vbs"
(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "%STARTUP_DIR%\%SHORTCUT_NAME%"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "%~dp0%APP_EXE%"
    echo oLink.WorkingDirectory = "%~dp0"
    echo oLink.IconLocation = "%~dp0%APP_EXE%,0"
    echo oLink.Save
) > "%VBS_SCRIPT%"

cscript //nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%" >nul 2>&1

:: Create invisible launcher VBS script for silent startup
set "VBS_LAUNCHER=%~dp0app_launcher.vbs"
(
    echo Set WshShell = CreateObject("WScript.Shell"^)
    echo WshShell.CurrentDirectory = "%cd%"
    echo WshShell.Run """" ^& "%cd%\%APP_EXE%" ^& """", 0, False
) > "%VBS_LAUNCHER%"

:: Update shortcut to launch via VBS for silent start
(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "%STARTUP_DIR%\%SHORTCUT_NAME%"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "%VBS_LAUNCHER%"
    echo oLink.WorkingDirectory = "%~dp0"
    echo oLink.IconLocation = "%~dp0%APP_EXE%,0"
    echo oLink.Save
) > "%VBS_SCRIPT%"

cscript //nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%" >nul 2>&1

:: Launch program normally (visible)
start "" "%~dp0%APP_EXE%"

echo Shortcut for "%APP_EXE%" added to Startup folder: 
echo %STARTUP_DIR%\%SHORTCUT_NAME%
echo Note: Application will launch silently on system startup.
timeout /t 5 >nul
exit