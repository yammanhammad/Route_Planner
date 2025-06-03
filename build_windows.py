#!/usr/bin/env python3
"""
Windows Build Script for Route Planner
Creates standalone executable and installer for Windows users
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

class WindowsBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build_windows"
        self.dist_dir = self.project_root / "dist_windows"
        self.version = "1.0.0"
        
    def clean_build_dirs(self):
        """Clean previous build directories"""
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
            dir_path.mkdir(exist_ok=True)
        print("✓ Cleaned build directories")
    
    def install_build_dependencies(self):
        """Install required build tools"""
        dependencies = [
            "pyinstaller",
            "auto-py-to-exe",
            "inno-setup-compiler",  # For creating installer
            "pillow",  # For icon handling
        ]
        
        print("Installing build dependencies...")
        for dep in dependencies:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
                print(f"✓ Installed {dep}")
            except subprocess.CalledProcessError:
                print(f"⚠ Could not install {dep} - may need manual installation")
    
    def create_executable(self):
        """Create standalone executable using PyInstaller"""
        print("Creating standalone executable...")
        
        # Create a simple launcher script
        launcher_content = '''
import sys
import os
from pathlib import Path

# Add the application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Import and run the main application
try:
    from main_app import RoutePlannerApp
    import tkinter as tk
    from tkinter import messagebox
    
    def main():
        try:
            app = RoutePlannerApp()
            app.run()
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Route Planner Error", 
                               f"Failed to start Route Planner:\\n{str(e)}")
            root.destroy()
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Route Planner Error", 
                       f"Missing dependencies:\\n{str(e)}")
    root.destroy()
'''
        
        launcher_path = self.project_root / "route_planner_launcher.py"
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        # PyInstaller command
        pyinstaller_args = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "RoutePlanner",
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),
            "--add-data", f"{self.project_root}/main_app.py;.",
            "--add-data", f"{self.project_root}/config.py;.",
            "--add-data", f"{self.project_root}/requirements.txt;.",
            "--add-data", f"{self.project_root}/README.md;.",
            "--hidden-import", "PyQt5",
            "--hidden-import", "folium",
            "--hidden-import", "requests",
            "--hidden-import", "geopy",
            "--collect-all", "folium",
            str(launcher_path)
        ]
        
        # Add icon if available
        icon_path = self.project_root / "icon.ico"
        if icon_path.exists():
            pyinstaller_args.extend(["--icon", str(icon_path)])
        
        try:
            subprocess.run(pyinstaller_args, check=True)
            print("✓ Standalone executable created successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create executable: {e}")
            return False
    
    def create_installer_script(self):
        """Create Inno Setup installer script"""
        installer_script = f'''
#define MyAppName "Route Planner"
#define MyAppVersion "{self.version}"
#define MyAppPublisher "Route Planner Team"
#define MyAppURL "https://github.com/yammanhammad/Route_Planner"
#define MyAppExeName "RoutePlanner.exe"

[Setup]
AppId={{{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile={self.project_root}\\LICENSE
OutputDir={self.dist_dir}
OutputBaseFilename=RoutePlanner-{self.version}-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile={self.project_root}\\icon.ico
UninstallDisplayIcon={{app}}\\{{#MyAppExeName}}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "{self.dist_dir}\\RoutePlanner.exe"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.project_root}\\README.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.project_root}\\LICENSE"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.project_root}\\docs\\*"; DestDir: "{{app}}\\docs"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{{app}}"
'''
        
        script_path = self.build_dir / "installer.iss"
        with open(script_path, 'w') as f:
            f.write(installer_script)
        
        print("✓ Installer script created")
        return script_path
    
    def create_icon(self):
        """Create application icon"""
        try:
            from PIL import Image, ImageDraw
            
            # Create a simple icon
            size = (256, 256)
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw a simple route icon
            # Background circle
            draw.ellipse([20, 20, 236, 236], fill=(52, 152, 219), outline=(41, 128, 185), width=3)
            
            # Route path
            points = [(60, 120), (100, 80), (156, 80), (196, 120), (156, 176), (100, 176)]
            draw.polygon(points, fill=(255, 255, 255), outline=(236, 240, 241), width=2)
            
            # Start and end points
            draw.ellipse([50, 110, 70, 130], fill=(231, 76, 60))
            draw.ellipse([186, 110, 206, 130], fill=(46, 204, 113))
            
            # Save as ICO
            icon_path = self.project_root / "icon.ico"
            img.save(icon_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
            print("✓ Application icon created")
            return True
        except ImportError:
            print("⚠ Pillow not available, skipping icon creation")
            return False
    
    def create_portable_version(self):
        """Create a portable version with all dependencies"""
        portable_dir = self.dist_dir / "RoutePlanner_Portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_source = self.dist_dir / "RoutePlanner.exe"
        if exe_source.exists():
            shutil.copy2(exe_source, portable_dir / "RoutePlanner.exe")
        
        # Copy documentation
        docs_to_copy = ["README.md", "LICENSE", "CHANGELOG.md"]
        for doc in docs_to_copy:
            doc_path = self.project_root / doc
            if doc_path.exists():
                shutil.copy2(doc_path, portable_dir / doc)
        
        # Copy docs directory
        docs_dir = self.project_root / "docs"
        if docs_dir.exists():
            shutil.copytree(docs_dir, portable_dir / "docs", dirs_exist_ok=True)
        
        # Create portable launcher batch file
        batch_content = '''@echo off
title Route Planner
echo Starting Route Planner...
RoutePlanner.exe
if errorlevel 1 (
    echo.
    echo An error occurred while running Route Planner.
    echo Please check that all dependencies are properly installed.
    pause
)
'''
        
        with open(portable_dir / "Start_RoutePlanner.bat", 'w') as f:
            f.write(batch_content)
        
        # Create README for portable version
        portable_readme = '''# Route Planner - Portable Version

This is the portable version of Route Planner. No installation required!

## Quick Start

1. Double-click "RoutePlanner.exe" to start the application
2. Alternatively, run "Start_RoutePlanner.bat" for better error handling

## Features

- No installation required
- Runs from any location
- All dependencies included
- Cross-platform route optimization

## System Requirements

- Windows 7 or later (64-bit recommended)
- 4GB RAM minimum
- Internet connection for map data

## Documentation

See the docs/ folder for detailed documentation and user guides.

## Support

For support and updates, visit:
https://github.com/yammanhammad/Route_Planner
'''
        
        with open(portable_dir / "README_Portable.txt", 'w') as f:
            f.write(portable_readme)
        
        print("✓ Portable version created")
    
    def create_zip_packages(self):
        """Create ZIP packages for distribution"""
        import zipfile
        
        # Create portable ZIP
        portable_dir = self.dist_dir / "RoutePlanner_Portable"
        if portable_dir.exists():
            zip_path = self.dist_dir / f"RoutePlanner-{self.version}-Portable.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in portable_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(portable_dir.parent)
                        zipf.write(file_path, arcname)
            print(f"✓ Created {zip_path.name}")
    
    def build_all(self):
        """Build all Windows distributions"""
        print("🏗️  Building Route Planner for Windows...")
        print("=" * 50)
        
        # Step 1: Clean and prepare
        self.clean_build_dirs()
        
        # Step 2: Install dependencies
        self.install_build_dependencies()
        
        # Step 3: Create icon
        self.create_icon()
        
        # Step 4: Create executable
        if not self.create_executable():
            print("❌ Failed to create executable. Build aborted.")
            return False
        
        # Step 5: Create portable version
        self.create_portable_version()
        
        # Step 6: Create installer script
        installer_script = self.create_installer_script()
        
        # Step 7: Create ZIP packages
        self.create_zip_packages()
        
        print("\n" + "=" * 50)
        print("🎉 Windows build completed successfully!")
        print("\n📦 Created files:")
        
        for file_path in self.dist_dir.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size / (1024 * 1024)  # MB
                print(f"   • {file_path.name} ({size:.1f} MB)")
        
        print(f"\n📁 Build output directory: {self.dist_dir}")
        print("\n📋 Next steps:")
        print("   1. Test the RoutePlanner.exe executable")
        print("   2. Install Inno Setup to compile the installer:")
        print("      https://jrsoftware.org/isinfo.php")
        print(f"   3. Compile {installer_script.name} with Inno Setup")
        print("   4. Distribute the portable ZIP or installer")
        
        return True

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Route Planner Windows Builder")
        print("Usage: python build_windows.py")
        print("Creates standalone executable and installer for Windows")
        return
    
    builder = WindowsBuilder()
    success = builder.build_all()
    
    if success:
        print("\n✨ Build completed successfully!")
        print("Windows users can now double-click the executable to run Route Planner!")
    else:
        print("\n❌ Build failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
