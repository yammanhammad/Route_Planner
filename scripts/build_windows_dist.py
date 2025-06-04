#!/usr/bin/env python3
"""
Complete Windows Distribution Builder
Creates both standalone executable and installer for maximum user-friendliness
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
import platform

class WindowsDistributionBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = Path(__file__).parent
        self.dist_dir = self.project_root / "dist_windows"
        self.version = "1.0.3"
        
    def setup_environment(self):
        """Set up build environment"""
        print("🔧 Setting up build environment...")
        
        # Ensure we're in the right directory
        os.chdir(self.project_root)
        
        # Clean previous builds
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir()
        
        # Clean temporary directories
        for temp_dir in ["build", "build_temp", "__pycache__"]:
            temp_path = self.project_root / temp_dir
            if temp_path.exists():
                shutil.rmtree(temp_path)
        
        print("✓ Environment prepared")
    
    def install_dependencies(self):
        """Install build dependencies"""
        print("📦 Installing build dependencies...")
        
        dependencies = [
            "pyinstaller>=5.0",
            "pillow>=9.0.0",
        ]
        
        for dep in dependencies:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], check=True, capture_output=True)
                print(f"✓ Installed {dep}")
            except subprocess.CalledProcessError as e:
                print(f"⚠ Failed to install {dep}: {e}")
    
    def create_application_icon(self):
        """Create a professional application icon"""
        print("🎨 Creating application icon...")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create icon with multiple sizes
            sizes = [16, 32, 48, 64, 128, 256]
            images = []
            
            for size in sizes:
                img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Background gradient circle
                for i in range(size//4):
                    alpha = int(255 * (1 - i/(size//4)))
                    color = (52, 152, 219, alpha)
                    draw.ellipse([i, i, size-i, size-i], outline=color, width=2)
                
                # Main circle
                margin = size // 8
                draw.ellipse([margin, margin, size-margin, size-margin], 
                           fill=(52, 152, 219), outline=(41, 128, 185), width=max(1, size//64))
                
                # Route path (simplified for small icons)
                if size >= 32:
                    path_margin = size // 4
                    points = [
                        (path_margin, size//2),
                        (size//3, path_margin + size//8),
                        (2*size//3, path_margin + size//8), 
                        (size-path_margin, size//2),
                        (2*size//3, size-path_margin - size//8),
                        (size//3, size-path_margin - size//8)
                    ]
                    draw.polygon(points, fill=(255, 255, 255, 200))
                
                # Start/end points
                point_size = max(2, size//16)
                draw.ellipse([margin*2, size//2-point_size//2, 
                            margin*2+point_size, size//2+point_size//2], 
                           fill=(231, 76, 60))
                draw.ellipse([size-margin*2-point_size, size//2-point_size//2,
                            size-margin*2, size//2+point_size//2], 
                           fill=(46, 204, 113))
                
                images.append(img)
            
            # Save as ICO file
            icon_path = self.project_root / "icon.ico"
            images[0].save(icon_path, format='ICO', 
                          sizes=[(s, s) for s in sizes], 
                          append_images=images[1:])
            
            print(f"✓ Created icon: {icon_path}")
            return True
            
        except Exception as e:
            print(f"⚠ Could not create icon: {e}")
            return False
    
    def build_executable(self):
        """Build standalone executable"""
        print("🏗️  Building standalone executable...")
        
        # Create optimized launcher
        launcher_content = '''"""Route Planner - Windows Launcher"""
import sys
import os
from pathlib import Path

# Ensure proper import path
if hasattr(sys, '_MEIPASS'):
    # Running as PyInstaller bundle
    bundle_dir = Path(sys._MEIPASS)
else:
    # Running as script
    bundle_dir = Path(__file__).parent

sys.path.insert(0, str(bundle_dir))

def main():
    try:
        from route_planner.main import main as app_main
        app_main()
    except Exception as e:
        # Show error dialog
        try:
            from PyQt5.QtWidgets import QApplication, QMessageBox
            app = QApplication([])
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Route Planner Error")
            msg.setText(f"Failed to start Route Planner:\\n\\n{str(e)}")
            msg.setDetailedText("Please try downloading the latest version from GitHub.")
            msg.exec_()
        except:
            print(f"Error: {e}")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
        
        launcher_path = self.project_root / "windows_launcher.py"
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        # PyInstaller command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed", 
            "--name", "RoutePlanner",
            "--distpath", str(self.dist_dir),
            "--specpath", str(self.dist_dir),
            
            # Add data files
            "--add-data", f"{self.project_root}/main.py;.",
            "--add-data", f"{self.project_root}/config.py;.",
            
            # Hidden imports
            "--hidden-import", "PyQt5.QtCore",
            "--hidden-import", "PyQt5.QtWidgets",
            "--hidden-import", "PyQt5.QtWebEngineWidgets",
            "--hidden-import", "folium",
            "--hidden-import", "requests",
            "--hidden-import", "geopy",
            "--hidden-import", "networkx",
            "--hidden-import", "numpy",
            "--hidden-import", "matplotlib",
            "--hidden-import", "urllib3",
            "--hidden-import", "certifi",
            
            # Collect package data
            "--collect-all", "folium",
            "--collect-all", "branca",
            
            # Optimization
            "--strip",
            "--optimize", "2",
            
            str(launcher_path)
        ]
        
        # Add icon if available
        icon_path = self.project_root / "icon.ico"
        if icon_path.exists():
            cmd.extend(["--icon", str(icon_path)])
        
        try:
            print("   Building executable (this may take 5-10 minutes)...")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                exe_path = self.dist_dir / "RoutePlanner.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    print(f"✓ Executable created: {exe_path.name} ({size_mb:.1f} MB)")
                    return True
                else:
                    print("❌ Executable not found after build")
                    return False
            else:
                print("❌ Build failed:")
                print(result.stderr[-1000:])  # Last 1000 chars
                return False
                
        except Exception as e:
            print(f"❌ Build exception: {e}")
            return False
        finally:
            # Cleanup
            if launcher_path.exists():
                launcher_path.unlink()
    
    def create_portable_package(self):
        """Create portable ZIP package"""
        print("📦 Creating portable package...")
        
        exe_path = self.dist_dir / "RoutePlanner.exe"
        if not exe_path.exists():
            print("❌ Executable not found")
            return False
        
        # Create portable directory
        portable_dir = self.dist_dir / "RoutePlanner_Portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Copy executable
        shutil.copy2(exe_path, portable_dir / "RoutePlanner.exe")
        
        # Copy documentation
        docs = ["README.md", "LICENSE", "CHANGELOG.md"]
        for doc in docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                shutil.copy2(doc_path, portable_dir)
        
        # Copy docs folder
        docs_folder = self.project_root / "docs"
        if docs_folder.exists():
            shutil.copytree(docs_folder, portable_dir / "docs")
        
        # Create Windows-friendly README
        readme_content = """Route Planner - Portable Version
================================

QUICK START:
Double-click "RoutePlanner.exe" to start the application.

WHAT IS THIS?
Route Planner helps you find the most efficient routes between multiple locations.
Perfect for delivery drivers, sales teams, or anyone who needs to visit multiple places.

FEATURES:
✓ Interactive map interface
✓ Smart route optimization
✓ Multiple algorithm options  
✓ Works offline after initial setup
✓ No installation required

SYSTEM REQUIREMENTS:
- Windows 7 or newer
- 4GB RAM recommended
- Internet connection for maps

TROUBLESHOOTING:
If the app doesn't start:
1. Right-click RoutePlanner.exe → "Run as administrator"
2. Check Windows Defender isn't blocking it
3. Download the latest version from GitHub

SUPPORT:
Visit: https://github.com/yammanhammad/Route_Planner
Email: [your-email]

LICENSE:
MIT License - See LICENSE file for details.
"""
        
        with open(portable_dir / "README.txt", 'w') as f:
            f.write(readme_content)
        
        # Create ZIP
        zip_path = self.dist_dir / f"RoutePlanner-{self.version}-Portable.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for file_path in portable_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(portable_dir.parent)
                    zipf.write(file_path, arcname)
        
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"✓ Portable package: {zip_path.name} ({size_mb:.1f} MB)")
        return True
    
    def create_installer_package(self):
        """Create installer package using existing script"""
        print("📋 Creating installer package...")
        
        # Check if NSIS installer script exists
        nsis_script = self.scripts_dir / "installer.nsi"
        if not nsis_script.exists():
            print("⚠ NSIS installer script not found, skipping installer creation")
            print("   To create installer:")
            print("   1. Install NSIS (https://nsis.sourceforge.io/)")
            print(f"   2. Compile {nsis_script.name}")
            return False
        
        print(f"ℹ To create installer, compile {nsis_script.name} with NSIS")
        return True
    
    def test_executable(self):
        """Basic test of the executable"""
        print("🧪 Testing executable...")
        
        exe_path = self.dist_dir / "RoutePlanner.exe"
        if not exe_path.exists():
            print("❌ Executable not found for testing")
            return False
        
        try:
            # Test that executable can start (just check it doesn't crash immediately)
            process = subprocess.Popen([str(exe_path)], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Give it a moment to start
            import time
            time.sleep(3)
            
            # Check if process is still running (good sign)
            if process.poll() is None:
                process.terminate()
                print("✓ Executable starts successfully")
                return True
            else:
                stdout, stderr = process.communicate()
                print("⚠ Executable exited immediately")
                if stderr:
                    print(f"   Error: {stderr.decode()[:200]}")
                return False
                
        except Exception as e:
            print(f"⚠ Could not test executable: {e}")
            return False
    
    def build_all(self):
        """Complete build process"""
        print("🚀 Route Planner Windows Distribution Builder")
        print("=" * 60)
        
        # Setup
        self.setup_environment()
        self.install_dependencies()
        self.create_application_icon()
        
        # Build executable
        if not self.build_executable():
            print("❌ Failed to build executable")
            return False
        
        # Test executable
        self.test_executable()
        
        # Create packages
        self.create_portable_package()
        self.create_installer_package()
        
        # Summary
        print("\\n" + "=" * 60)
        print("🎉 Windows distribution build completed!")
        print("\\n📦 Created files:")
        
        for file_path in self.dist_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.endswith('.spec'):
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"   📄 {file_path.name} ({size_mb:.1f} MB)")
        
        print(f"\\n📁 Output directory: {self.dist_dir}")
        print("\\n🎯 Distribution options:")
        print("   1. RoutePlanner.exe - Direct executable")
        print("   2. RoutePlanner-*-Portable.zip - Portable package")
        print("   3. Create installer using NSIS (see scripts/installer.nsi)")
        
        print("\\n✨ Windows users can now:")
        print("   • Double-click the .exe to run (no installation needed!)")
        print("   • Extract and run the portable version") 
        print("   • Install using the installer (if created)")
        
        return True

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Route Planner Windows Distribution Builder")
        print("Creates standalone executable and packages for Windows users")
        print("\\nUsage: python build_windows_dist.py")
        print("\\nOutput: dist_windows/ directory with all distribution files")
        return
    
    builder = WindowsDistributionBuilder()
    success = builder.build_all()
    
    if not success:
        print("\\n❌ Build failed. Check error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
