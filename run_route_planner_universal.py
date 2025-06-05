#!/usr/bin/env python3
"""
Universal Runner for Route Planner
=================================

This script provides a unified entry point for running Route Planner
on any platform. It detects the current platform and launches the
application using the most appropriate method.

Usage:
    python run_route_planner_universal.py [args...]
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

def get_app_dir():
    """Get the application directory."""
    return Path(__file__).parent.absolute()

def run_windows():
    """Run Route Planner on Windows."""
    print("🪟 Running Route Planner on Windows...")
    app_dir = get_app_dir()
    
    # Try to find executable first (best option)
    exe_path = app_dir / "dist" / "RoutePlanner.exe"
    if exe_path.exists():
        print(f"✅ Found executable: {exe_path}")
        subprocess.run([str(exe_path)] + sys.argv[1:])
        return 0
    
    # Try batch file next
    batch_path = app_dir / "scripts" / "run_route_planner.bat"
    if batch_path.exists():
        print(f"✅ Found batch file: {batch_path}")
        subprocess.run([str(batch_path)] + sys.argv[1:], shell=True)
        return 0
    
    # Fall back to Python module
    print("ℹ️ No native launcher found, using Python module")
    return run_python_module()

def run_macos():
    """Run Route Planner on macOS."""
    print("🍎 Running Route Planner on macOS...")
    app_dir = get_app_dir()
    
    # Try to find .app bundle first (best option)
    app_bundle = app_dir / "dist" / "RoutePlanner.app"
    if app_bundle.exists():
        print(f"✅ Found application bundle: {app_bundle}")
        subprocess.run(["open", str(app_bundle)] + sys.argv[1:])
        return 0
    
    # Try shell script next
    shell_path = app_dir / "scripts" / "run_route_planner.sh"
    if shell_path.exists():
        print(f"✅ Found shell script: {shell_path}")
        subprocess.run(["bash", str(shell_path)] + sys.argv[1:])
        return 0
    
    # Fall back to Python module
    print("ℹ️ No native launcher found, using Python module")
    return run_python_module()

def run_linux():
    """Run Route Planner on Linux."""
    print("🐧 Running Route Planner on Linux...")
    app_dir = get_app_dir()
    
    # Try to find AppImage first (best option)
    appimages = list(app_dir.glob("*.AppImage"))
    if appimages:
        appimage = appimages[0]
        print(f"✅ Found AppImage: {appimage}")
        subprocess.run([str(appimage)] + sys.argv[1:])
        return 0
    
    # Try shell script next
    shell_path = app_dir / "scripts" / "run_route_planner.sh"
    if shell_path.exists():
        print(f"✅ Found shell script: {shell_path}")
        os.chmod(shell_path, 0o755)  # Ensure executable
        subprocess.run([str(shell_path)] + sys.argv[1:])
        return 0
    
    # Fall back to Python module
    print("ℹ️ No native launcher found, using Python module")
    return run_python_module()

def run_python_module():
    """Run Route Planner as a Python module."""
    print("🐍 Running Route Planner as Python module...")
    app_dir = get_app_dir()
    
    # Make sure the app directory is in sys.path
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))
    
    # First try to import and run from the module
    try:
        from route_planner.core import main
        print("✅ Running from installed module")
        return main()
    except ImportError:
        pass
    
    # Then try to run main.py directly
    main_py = app_dir / "main.py"
    if main_py.exists():
        print(f"✅ Running main.py: {main_py}")
        subprocess.run([sys.executable, str(main_py)] + sys.argv[1:])
        return 0
    
    # If all else fails, try the route_planner.py launcher
    launcher_py = app_dir / "route_planner.py"
    if launcher_py.exists():
        print(f"✅ Running launcher: {launcher_py}")
        subprocess.run([sys.executable, str(launcher_py)] + sys.argv[1:])
        return 0
    
    print("❌ Could not find any way to run Route Planner")
    return 1

def main():
    """Main entry point."""
    print("🚚 Route Planner Universal Runner")
    print(f"🖥️  Detected platform: {platform.system()}")
    
    # Run appropriate platform-specific launcher
    system = platform.system()
    if system == "Windows":
        return run_windows()
    elif system == "Darwin":  # macOS
        return run_macos()
    elif system == "Linux":
        return run_linux()
    else:
        print(f"⚠️ Unknown platform: {system}")
        return run_python_module()

if __name__ == "__main__":
    sys.exit(main())
