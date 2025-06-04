#!/usr/bin/env python3
"""
Simple Windows Executable Builder for Route Planner
Creates a single executable file that Windows users can double-click to run
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                         check=True)
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_simple_launcher():
    """Create a simple launcher script that handles errors gracefully"""
    launcher_content = '''#!/usr/bin/env python3
"""
Route Planner Launcher
Simple launcher that provides user-friendly error handling
"""

import sys
import os
import traceback
from pathlib import Path

def show_error(title, message):
    """Show error message using available GUI toolkit"""
    try:
        # Try PyQt5 first
        from PyQt5.QtWidgets import QApplication, QMessageBox
        app = QApplication([])
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        return
    except ImportError:
        pass
    
    try:
        # Fallback to tkinter
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
        return
    except ImportError:
        pass
    
    # Final fallback - print to console
    print(f"ERROR: {title}")
    print(f"{message}")
    input("Press Enter to exit...")

def main():
    """Main entry point with comprehensive error handling"""
    try:
        # Add current directory to path
        current_dir = Path(__file__).parent.resolve()
        sys.path.insert(0, str(current_dir))
        
        # Import and run the main application
        from route_planner.main import main as app_main
        
        print("Starting Route Planner...")
        app_main()
        
    except ImportError as e:
        error_msg = f"""Route Planner failed to start due to missing dependencies.

Error: {str(e)}

This usually means Python packages are not properly installed.
Please try:
1. Reinstalling Route Planner
2. Downloading the latest version from GitHub
3. Running 'pip install -r requirements.txt' in the application folder

For support, visit: https://github.com/yammanhammad/Route_Planner"""
        
        show_error("Route Planner - Missing Dependencies", error_msg)
        
    except Exception as e:
        error_msg = f"""An unexpected error occurred while starting Route Planner.

Error: {str(e)}

Please try:
1. Restarting the application
2. Checking system requirements (Python 3.8+, 4GB+ RAM)
3. Downloading the latest version

For detailed error information, check the console output.
For support, visit: https://github.com/yammanhammad/Route_Planner"""
        
        show_error("Route Planner - Startup Error", error_msg)
        
        # Print detailed error for debugging
        print("\\nDetailed error information:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
'''
    
    launcher_path = Path("route_planner_windows_launcher.py")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"✓ Created launcher script: {launcher_path}")
    return launcher_path

def build_executable():
    """Build standalone executable using PyInstaller"""
    print("\\n🏗️  Building Windows executable...")
    
    launcher_path = create_simple_launcher()
    
    # PyInstaller command for creating a single executable
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name", "RoutePlanner",       # Executable name
        "--distpath", "dist_windows",   # Output directory
        "--workpath", "build_temp",     # Temporary build directory
        
        # Include all necessary files and modules
        "--add-data", "main.py;.",
        "--add-data", "config.py;.",
        "--add-data", "README.md;.",
        "--add-data", "LICENSE;.",
        
        # Hidden imports (modules not automatically detected)
        "--hidden-import", "PyQt5",
        "--hidden-import", "PyQt5.QtCore",
        "--hidden-import", "PyQt5.QtWidgets", 
        "--hidden-import", "PyQt5.QtWebEngineWidgets",
        "--hidden-import", "folium",
        "--hidden-import", "requests",
        "--hidden-import", "geopy",
        "--hidden-import", "networkx",
        "--hidden-import", "numpy",
        "--hidden-import", "matplotlib",
        
        # Collect all data files from packages
        "--collect-all", "folium",
        
        str(launcher_path)
    ]
    
    # Add icon if it exists
    icon_path = Path("icon.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    try:
        print("Running PyInstaller...")
        print("This may take several minutes...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            
            # Check if executable was created
            exe_path = Path("dist_windows/RoutePlanner.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 Executable size: {size_mb:.1f} MB")
                print(f"📁 Location: {exe_path.absolute()}")
                return True
            else:
                print("❌ Executable file not found after build")
                return False
        else:
            print("❌ Build failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build failed with exception: {e}")
        return False
    
    finally:
        # Clean up launcher file
        if launcher_path.exists():
            launcher_path.unlink()

def create_portable_package():
    """Create a portable ZIP package"""
    print("\\n📦 Creating portable package...")
    
    exe_path = Path("dist_windows/RoutePlanner.exe")
    if not exe_path.exists():
        print("❌ Executable not found, cannot create portable package")
        return False
    
    # Create portable directory
    portable_dir = Path("dist_windows/RoutePlanner_Portable")
    portable_dir.mkdir(exist_ok=True)
    
    # Copy executable
    shutil.copy2(exe_path, portable_dir / "RoutePlanner.exe")
    
    # Copy documentation
    docs = ["README.md", "LICENSE", "CHANGELOG.md"]
    for doc in docs:
        doc_path = Path(doc)
        if doc_path.exists():
            shutil.copy2(doc_path, portable_dir / doc)
    
    # Create user-friendly README
    readme_content = """# Route Planner - Portable Version

## Quick Start
Double-click "RoutePlanner.exe" to start the application.

## What is Route Planner?
Route Planner is a powerful tool for optimizing delivery routes and travel paths.
It uses advanced algorithms to find the most efficient routes between multiple locations.

## Features
- Interactive map interface
- Multiple optimization algorithms
- Offline operation capability
- No installation required (portable version)

## System Requirements
- Windows 7 or later
- 4GB RAM recommended
- Internet connection for map data

## Support
For help and updates, visit:
https://github.com/yammanhammad/Route_Planner

## License
This software is licensed under the MIT License.
See LICENSE file for details.
"""
    
    with open(portable_dir / "README.txt", 'w') as f:
        f.write(readme_content)
    
    # Create ZIP package
    import zipfile
    zip_path = Path("dist_windows/RoutePlanner-Portable.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in portable_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(portable_dir.parent)
                zipf.write(file_path, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"✅ Portable package created: {zip_path.name} ({size_mb:.1f} MB)")
    return True

def main():
    """Main build process"""
    print("🚀 Route Planner Windows Executable Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found in current directory")
        print("Please run this script from the Route_Planner root directory")
        return False
    
    # Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Build executable
    if not build_executable():
        return False
    
    # Create portable package
    create_portable_package()
    
    print("\\n" + "=" * 50)
    print("🎉 Build completed successfully!")
    print("\\n📋 What you can do now:")
    print("1. Test the executable: dist_windows/RoutePlanner.exe")
    print("2. Distribute the portable ZIP: dist_windows/RoutePlanner-Portable.zip")
    print("3. Share with Windows users - they just need to double-click to run!")
    print("\\n✨ No Python installation required for end users!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
