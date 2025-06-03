#!/usr/bin/env python3
"""
Route Planner Virtual Environment Setup
======================================

This script sets up a virtual environment for the Route Planner application.
It works on Windows, macOS, and Linux.
"""

import os
import platform
import subprocess
import sys
import venv
from pathlib import Path

def main():
    """Set up the virtual environment and install dependencies."""
    print("╔════════════════════════════════════════╗")
    print("║  Route Planner Environment Setup Tool  ║")
    print("╚════════════════════════════════════════╝")
    
    # Get the current script directory
    script_dir = Path(__file__).parent.absolute()
    venv_dir = script_dir / '.venv'
    requirements_file = script_dir / 'requirements.txt'
    
    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print("\n🔧 Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        print("✅ Virtual environment created!")
    
    # Determine the Python executable in the virtual environment
    if platform.system() == 'Windows':
        python_executable = venv_dir / 'Scripts' / 'python.exe'
        pip_executable = venv_dir / 'Scripts' / 'pip.exe'
    else:
        python_executable = venv_dir / 'bin' / 'python'
        pip_executable = venv_dir / 'bin' / 'pip'
    
    # Install dependencies
    if requirements_file.exists():
        print("\n📦 Installing dependencies...")
        try:
            subprocess.run([str(pip_executable), 'install', '--upgrade', 'pip'], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run([str(pip_executable), 'install', '-r', str(requirements_file)], 
                          check=True)
            print("✅ Dependencies installed!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return 1
    else:
        print(f"❌ Requirements file not found: {requirements_file}")
        return 1
    
    print("\n🎉 Environment setup complete!")
    print("\nTo activate the virtual environment:")
    if platform.system() == 'Windows':
        print(f"  Run: {venv_dir}\\Scripts\\activate.bat")
    else:
        print(f"  Run: source {venv_dir}/bin/activate")
    
    print("\nTo run the application:")
    print("  1. Activate the virtual environment")
    if platform.system() == 'Windows':
        print("  2. Run: python route_planner.py")
    else:
        print("  2. Run: ./route_planner.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
