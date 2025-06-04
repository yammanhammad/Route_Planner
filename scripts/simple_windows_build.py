#!/usr/bin/env python3
"""
Simple Windows Executable Builder for Testing
"""

import sys
import subprocess
from pathlib import Path

def build_windows_exe():
    """Build a simple Windows executable for testing"""
    project_root = Path(__file__).parent.parent
    
    # Create a simple PyInstaller command that should work cross-platform
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "RoutePlanner",
        "--distpath", str(project_root / "dist"),
        "--hidden-import", "PyQt5.QtCore",
        "--hidden-import", "PyQt5.QtWidgets", 
        "--hidden-import", "PyQt5.QtWebEngineWidgets",
        "--hidden-import", "folium",
        "--hidden-import", "requests",
        "--hidden-import", "geopy",
        "--hidden-import", "networkx",
        "--hidden-import", "numpy",
        "--collect-all", "folium",
        str(project_root / "main.py")
    ]
    
    print("🏗️ Building Windows executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            print(f"Executable created at: {project_root}/dist/RoutePlanner.exe")
            return True
        else:
            print("❌ Build failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

if __name__ == "__main__":
    build_windows_exe()
