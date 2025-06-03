@echo off
title Route Planner - Windows Builder
echo.
echo =====================================
echo Route Planner Windows Builder
echo =====================================
echo.
echo This will create a Windows executable that users can double-click to run.
echo No Python installation required for end users!
echo.
pause

echo.
echo Installing build dependencies...
python -m pip install pyinstaller pillow --upgrade

echo.
echo Building Windows executable...
python scripts\build_windows_dist.py

echo.
echo Build complete! Check the dist_windows folder for output files.
echo.
pause
