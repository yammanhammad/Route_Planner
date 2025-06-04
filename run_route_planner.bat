@echo off
REM Route Planner - Windows Root Launcher
REM This script delegates to the actual launcher in the scripts directory

set "SCRIPT_DIR=%~dp0"
call "%SCRIPT_DIR%scripts\run_route_planner.bat" %*
