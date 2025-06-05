#!/usr/bin/env python3
"""
Route Planner Installation Script
=================================

This script automates the installation process for Route Planner.
It now uses the UniversalInstaller for enhanced cross-platform support.
"""

import os
import platform
import subprocess
import sys
import site
import shutil
from pathlib import Path

# Try to import our universal installer
try:
    from universal_installer import UniversalInstaller
    UNIVERSAL_INSTALLER = True
except ImportError:
    UNIVERSAL_INSTALLER = False

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        if platform.system() == 'Windows':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

def create_desktop_shortcut(app_path):
    """Create a desktop shortcut for the application."""
    try:
        home = Path.home()
        if platform.system() == 'Windows':
            desktop = home / 'Desktop'
            # Create a batch file
            shortcut_path = desktop / 'Route Planner.bat'
            with open(shortcut_path, 'w') as f:
                f.write(f'@echo off\nstart "" "{app_path}"')
            return True
        elif platform.system() == 'Linux':
            desktop = home / 'Desktop'
            # Create a .desktop file
            shortcut_path = desktop / 'route-planner.desktop'
            with open(shortcut_path, 'w') as f:
                f.write(f"""[Desktop Entry]
Name=Route Planner
Exec={app_path}
Icon=map
Terminal=false
Type=Application
Categories=Office;
""")
            os.chmod(shortcut_path, 0o755)
            return True
        elif platform.system() == 'Darwin':  # macOS
            # Create a .command file on the desktop
            desktop = home / 'Desktop'
            shortcut_path = desktop / 'Route Planner.command'
            with open(shortcut_path, 'w') as f:
                f.write(f'#!/bin/bash\n"{app_path}"\n')
            os.chmod(shortcut_path, 0o755)
            return True
        return False
    except Exception as e:
        print(f"Warning: Could not create desktop shortcut: {e}")
        return False

def main():
    """Main installation function."""
    print("╔════════════════════════════════════╗")
    print("║    Route Planner Installation Tool ║")
    print("╚════════════════════════════════════╝")
    
    # Check if universal installer is available
    if UNIVERSAL_INSTALLER:
        print("\n✨ Using enhanced cross-platform installer")
        
        # Determine installation mode
        global_install = len(sys.argv) > 1 and sys.argv[1] == '--global' and is_admin()
        
        # Create and run universal installer
        installer = UniversalInstaller(global_install=global_install)
        success = installer.install()
        
        # Return appropriate exit code
        return 0 if success else 1
    
    # Legacy installer code if universal installer is not available
    print("\n⚠️ Enhanced installer not available, using legacy installer")
    
    # Determine installation mode
    if len(sys.argv) > 1 and sys.argv[1] == '--global' and is_admin():
        print("\n🌐 Performing global installation (system-wide)")
        global_install = True
    else:
        print("\n👤 Performing user installation (current user only)")
        global_install = False
        if len(sys.argv) > 1 and sys.argv[1] == '--global':
            print("⚠️  Administrator privileges required for global installation.")
            print("   Falling back to user installation.")
    
    # Get the current script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Install the package
    print("\n📦 Installing Route Planner package...")
    try:
        cmd = [sys.executable, '-m', 'pip', 'install']
        if not global_install:
            cmd.append('--user')
        cmd.append('.')
        
        subprocess.run(cmd, cwd=script_dir, check=True)
        print("✅ Package installed successfully!")
        
        # Create shortcut if possible
        if site.USER_BASE and 'route-planner' in str(site.USER_BASE):
            bin_dir = Path(site.USER_BASE) / ('Scripts' if platform.system() == 'Windows' else 'bin')
            app_path = bin_dir / ('route-planner.exe' if platform.system() == 'Windows' else 'route-planner')
            if app_path.exists():
                if create_desktop_shortcut(app_path):
                    print("✅ Desktop shortcut created!")
        
        print("\n🎉 Installation complete!")
        print("\nYou can now run Route Planner by:")
        print("1. Running 'route-planner' from the command line")
        print("2. Using the desktop shortcut (if created)")
        print("3. Running route_planner.py from the project directory")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return 1
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
