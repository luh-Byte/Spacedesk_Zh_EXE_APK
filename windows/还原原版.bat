@echo off
chcp 65001 >nul
setlocal
set DIR=%SPACEDESK_DIR%
if "%DIR%"=="" set DIR=C:\Program Files\spacedesk
echo 正在关闭 spacedesk 控制台与托盘程序...
taskkill /f /im spacedeskConsole.exe >nul 2>&1
taskkill /f /im spacedeskServiceTray.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo 正在还原原始文件...
copy /y "%DIR%\原版备份\spacedeskConsole.exe" "%DIR%\spacedeskConsole.exe" >nul
copy /y "%DIR%\原版备份\spacedeskServiceTray.exe" "%DIR%\spacedeskServiceTray.exe" >nul
echo 正在重新启动托盘程序...
start "" "%DIR%\spacedeskServiceTray.exe"
echo.
echo 已还原为原版（英文）界面。
pause
