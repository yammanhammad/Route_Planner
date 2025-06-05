#!/usr/bin/env python3
"""
Universal Installer for Route Planner
=====================================

This module provides a unified installer class that adapts to different platforms
while maintaining a consistent API. It allows for platform-specific optimizations
while keeping a clean cross-platform interface.
"""

import os
import sys
import platform
import subprocess
import site
import shutil
import logging
from pathlib import Path

# Try to import enhanced platform management
try:
    # Add parent directory to sys.path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from route_planner.paths import (
        get_platform_manager, 
        get_home_dir, 
        get_config_dir, 
        get_cache_dir, 
        get_data_dir,
        make_executable, 
        ensure_dir_exists
    )
    ENHANCED_PLATFORM = True
except ImportError:
    ENHANCED_PLATFORM = False
    
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("UniversalInstaller")

class UniversalInstaller:
    """
    Cross-platform installer that adapts to the current platform
    while providing a consistent interface.
    """
    
    def __init__(self, global_install=False):
        """
        Initialize the installer with platform detection.
        
        Args:
            global_install (bool): Whether to perform a global installation
        """
        self.platform = platform.system()
        self.global_install = global_install
        self.installer_map = {
            "Windows": self.install_windows,
            "Darwin": self.install_macos,
            "Linux": self.install_linux
        }
        
        # Try to use enhanced platform management if available
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from route_planner.paths import get_platform_manager
            self.platform_manager = get_platform_manager()
            logger.info(f"Enhanced platform management enabled for {self.platform}")
        except ImportError:
            self.platform_manager = None
            logger.warning("Enhanced platform management not available")
        
        # Setup platform manager if available
        self.pm = None
        if ENHANCED_PLATFORM:
            try:
                self.pm = get_platform_manager()
                logger.info(f"Enhanced platform features enabled for {self.platform}")
            except Exception as e:
                logger.warning(f"Could not initialize platform manager: {e}")
        
        # Common paths
        self.script_dir = Path(__file__).parent.absolute()
        self.project_dir = self.script_dir.parent
        self.platform_manager = self.pm if ENHANCED_PLATFORM else None
        
        # Set up common install paths
        self.bin_dir = self._get_bin_dir()
        self.app_path = self._get_app_path()
        
    def install(self):
        """
        Install using platform-appropriate method.
        
        Automatically selects the appropriate installation method based on
        the detected platform, with graceful fallback to generic installation.
        
        Returns:
            bool: Whether installation was successful
        """
        logger.info(f"Starting installation on {self.platform} (global: {self.global_install})")
        
        # Display platform capabilities if enhanced platform management is available
        if self.platform_manager:
            features = self.platform_manager.features
            enabled = [k for k, v in features.items() if v]
            logger.info(f"Platform features: {', '.join(enabled[:5])}{' ...' if len(enabled) > 5 else ''}")
            
            # Log recommended format
            recommended = self.platform_manager.get_best_executable_format()
            logger.info(f"Recommended format: {recommended.get('description', 'Unknown')}")
            
            # Show supported packaging formats on Linux
            if self.platform == "Linux" and isinstance(recommended.get('formats'), dict):
                formats = recommended.get('formats', {})
                available_formats = [f"{info.get('name', key)} ({key})" 
                                    for key, info in formats.items() 
                                    if info.get('available', False)]
                if available_formats:
                    logger.info(f"Available packaging formats: {', '.join(available_formats)}")
        
        # Get the appropriate installer method or use generic fallback
        installer = self.installer_map.get(self.platform, self.install_generic)
        
        # Execute the installation
        try:
            success = installer()
            if success:
                logger.info("Installation completed successfully!")
                self.show_success_notification()
                return True
            else:
                logger.error("Installation failed!")
                return False
        except Exception as e:
            logger.error(f"Installation error: {e}")
            return False
            
    def install_windows(self):
        """
        Install on Windows platform.
        
        Returns:
            bool: Whether installation was successful
        """
        logger.info("Installing for Windows...")
        success_count = 0
        
        # Install package
        if self._install_package():
            success_count += 1
            logger.info("Package installed successfully!")
            
            # Create desktop shortcuts and start menu entries
            try:
                if self._create_windows_shortcut(self.app_path):
                    success_count += 1
                    logger.info("Desktop shortcut created!")
                    
                if self._create_windows_start_menu(self.app_path):
                    success_count += 1
                    logger.info("Start menu entry created!")
            except Exception as e:
                logger.warning(f"Could not create Windows integration: {e}")
        
        return success_count > 0
    
    def install_macos(self):
        """
        Install on macOS platform.
        
        Returns:
            bool: Whether installation was successful
        """
        logger.info("Installing for macOS...")
        success_count = 0
        
        # Install package
        if self._install_package():
            success_count += 1
            logger.info("Package installed successfully!")
            
            # Create desktop shortcuts and Applications folder links
            try:
                if self._create_macos_shortcut(self.app_path):
                    success_count += 1
                    logger.info("Desktop shortcut created!")
                    
                if self._create_macos_applications_link(self.app_path):
                    success_count += 1
                    logger.info("Applications link created!")
            except Exception as e:
                logger.warning(f"Could not create macOS integration: {e}")
        
        return success_count > 0
    
    def install_linux(self):
        """
        Install on Linux platform.
        
        Returns:
            bool: Whether installation was successful
        """
        logger.info("Installing for Linux...")
        success_count = 0
        
        # Install package
        if self._install_package():
            success_count += 1
            logger.info("Package installed successfully!")
            
            # Create desktop entry and application menu integration
            try:
                if self._create_linux_desktop_entry(self.app_path):
                    success_count += 1
                    logger.info("Desktop entry created!")
                    
                # Check for Linux packaging capabilities
                packaging_formats = {}
                
                # Use the enhanced platform manager if available
                if self.platform_manager:
                    try:
                        recommended = self.platform_manager.get_best_executable_format()
                        if 'formats' in recommended:
                            packaging_formats = recommended.get('formats', {})
                    except Exception as e:
                        logger.warning(f"Could not retrieve packaging formats: {e}")
                
                # Fallback to basic packaging detection if platform manager didn't provide formats
                if not packaging_formats:
                    packaging_support = self._check_linux_packaging_support()
                    if packaging_support:
                        packaging_formats = {
                            packaging_support.lower(): {
                                'name': packaging_support,
                                'available': True
                            }
                        }
                
                # Handle available packaging formats
                if packaging_formats:
                    available_formats = [format_info.get('name', format_id) 
                                         for format_id, format_info in packaging_formats.items() 
                                         if format_info.get('available', False)]
                    
                    logger.info(f"Linux packaging support detected: {', '.join(available_formats)}")
                    
                    # AppImage support
                    if 'appimage' in packaging_formats and packaging_formats['appimage'].get('available', False):
                        appimage_script = packaging_formats['appimage'].get('script_path')
                        
                        # If script path is provided by platform manager, use it
                        if not appimage_script:
                            appimage_script = str(Path(self.project_dir / 'scripts' / 'build_appimage.py'))
                            
                        if Path(appimage_script).exists():
                            logger.info("AppImage build script available - can create portable package")
                            print("\n💡 You can create an AppImage package with: python scripts/build_appimage.py")
                    
                    # Flatpak support
                    if 'flatpak' in packaging_formats and packaging_formats['flatpak'].get('available', False):
                        flatpak_manifest = packaging_formats['flatpak'].get('manifest_path')
                        
                        if flatpak_manifest and Path(flatpak_manifest).exists():
                            logger.info("Flatpak manifest available - can create Flatpak package")
                            print("\n💡 You can create a Flatpak package with: flatpak-builder build-dir " + 
                                  f"{flatpak_manifest}")
                        else:
                            logger.info("Flatpak support detected - can create Flatpak package")
                            print("\n💡 Flatpak is available but no manifest found. Create a manifest to build a Flatpak.")
                    
                    # Snap support
                    if 'snap' in packaging_formats and packaging_formats['snap'].get('available', False):
                        snap_manifest = packaging_formats['snap'].get('snapcraft_path')
                        
                        if snap_manifest and Path(snap_manifest).exists():
                            logger.info("Snap manifest available - can create Snap package")
                            print("\n💡 You can create a Snap package with: snapcraft")
                        else:
                            logger.info("Snap support detected - can create Snap package")
                            print("\n💡 Snapcraft is available but no snapcraft.yaml found. " +
                                  "Create a manifest to build a Snap.")
            except Exception as e:
                logger.warning(f"Could not create Linux integration: {e}")
        
        return success_count > 0
    
    def install_generic(self):
        """
        Generic installation for unsupported platforms.
        
        Returns:
            bool: Whether installation was successful
        """
        logger.info(f"Installing with generic method for {self.platform}...")
        
        # Just install the package without platform-specific features
        if self._install_package():
            logger.info("Package installed successfully!")
            return True
            
        return False
        
    def _install_package(self):
        """
        Install the Route Planner package.
        
        Returns:
            bool: Whether installation was successful
        """
        try:
            # Build pip command
            cmd = [sys.executable, '-m', 'pip', 'install']
            
            if not self.global_install:
                cmd.append('--user')
                
            # Install from current directory
            cmd.append('.')
            
            logger.info(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, cwd=str(self.project_dir), check=True)
            return True
        except Exception as e:
            logger.error(f"Package installation failed: {e}")
            return False
    
    def _get_bin_dir(self):
        """
        Get the binary directory for the current platform.
        
        Returns:
            Path: Path to the binary directory
        """
        try:
            if site.USER_BASE:
                if self.platform == "Windows":
                    return Path(site.USER_BASE) / 'Scripts'
                else:
                    return Path(site.USER_BASE) / 'bin'
            else:
                logger.warning("USER_BASE not found, using system paths")
                if self.platform == "Windows":
                    return Path(sys.prefix) / 'Scripts'
                else:
                    return Path(sys.prefix) / 'bin'
        except Exception as e:
            logger.error(f"Could not determine bin directory: {e}")
            return None
    
    def _get_app_path(self):
        """
        Get the path to the executable.
        
        Returns:
            Path: Path to the application executable
        """
        if not self.bin_dir:
            return None
            
        if self.platform == "Windows":
            return self.bin_dir / 'route-planner.exe'
        else:
            return self.bin_dir / 'route-planner'
    
    def _create_windows_shortcut(self, app_path):
        """
        Create a Windows desktop shortcut.
        
        Args:
            app_path: Path to the application executable
            
        Returns:
            bool: Whether creation was successful
        """
        if self.platform_manager:
            try:
                return self.platform_manager.create_desktop_entry(
                    app_name="Route Planner",
                    exec_path=str(app_path),
                    description="Delivery Route Optimization Application"
                )
            except Exception as e:
                logger.warning(f"Enhanced shortcut creation failed: {e}")
        
        # Fallback method
        try:
            desktop = Path.home() / 'Desktop'
            shortcut_path = desktop / 'Route Planner.bat'
            with open(shortcut_path, 'w') as f:
                f.write(f'@echo off\nstart "" "{app_path}"')
            return True
        except Exception as e:
            logger.error(f"Shortcut creation failed: {e}")
            return False
    
    def _create_windows_start_menu(self, app_path):
        """
        Create a Windows Start Menu entry.
        
        Args:
            app_path: Path to the application executable
            
        Returns:
            bool: Whether creation was successful
        """
        try:
            start_menu = Path(os.environ.get('APPDATA', '')) / "Microsoft/Windows/Start Menu/Programs"
            rp_folder = start_menu / "Route Planner"
            
            # Create folder if it doesn't exist
            if not rp_folder.exists():
                rp_folder.mkdir(parents=True, exist_ok=True)
            
            # Create shortcut
            shortcut_path = rp_folder / 'Route Planner.bat'
            with open(shortcut_path, 'w') as f:
                f.write(f'@echo off\nstart "" "{app_path}"')
            
            return True
        except Exception as e:
            logger.error(f"Start menu entry creation failed: {e}")
            return False
    
    def _create_macos_shortcut(self, app_path):
        """
        Create a macOS desktop shortcut.
        
        Args:
            app_path: Path to the application executable
            
        Returns:
            bool: Whether creation was successful
        """
        if self.platform_manager:
            try:
                return self.platform_manager.create_desktop_entry(
                    app_name="Route Planner",
                    exec_path=str(app_path),
                    description="Delivery Route Optimization Application"
                )
            except Exception as e:
                logger.warning(f"Enhanced shortcut creation failed: {e}")
        
        # Fallback method
        try:
            desktop = Path.home() / 'Desktop'
            shortcut_path = desktop / 'Route Planner.command'
            with open(shortcut_path, 'w') as f:
                f.write(f'#!/bin/bash\n"{app_path}"\n')
            os.chmod(shortcut_path, 0o755)  # Make executable
            return True
        except Exception as e:
            logger.error(f"Shortcut creation failed: {e}")
            return False
    
    def _create_macos_applications_link(self, app_path):
        """
        Create a link in the macOS Applications folder.
        
        Args:
            app_path: Path to the application executable
            
        Returns:
            bool: Whether creation was successful
        """
        try:
            user_apps = Path.home() / 'Applications'
            
            # Create Applications folder if it doesn't exist
            if not user_apps.exists():
                user_apps.mkdir(parents=True, exist_ok=True)
            
            # Create application launcher
            app_launcher = user_apps / 'Route Planner.command'
            with open(app_launcher, 'w') as f:
                f.write(f'#!/bin/bash\n"{app_path}"\n')
            os.chmod(app_launcher, 0o755)  # Make executable
            
            return True
        except Exception as e:
            logger.error(f"Applications link creation failed: {e}")
            return False
    
    def _create_linux_desktop_entry(self, app_path):
        """
        Create a Linux desktop entry.
        
        Args:
            app_path: Path to the application executable
            
        Returns:
            bool: Whether creation was successful
        """
        if self.platform_manager:
            try:
                return self.platform_manager.create_desktop_entry(
                    app_name="Route Planner",
                    exec_path=str(app_path),
                    description="Delivery Route Optimization Application"
                )
            except Exception as e:
                logger.warning(f"Enhanced desktop entry creation failed: {e}")
        
        # Fallback method
        try:
            # Create .desktop file
            desktop = Path.home() / 'Desktop'
            user_apps = Path.home() / '.local/share/applications'
            
            # Ensure directories exist
            if not user_apps.exists():
                user_apps.mkdir(parents=True, exist_ok=True)
            
            # Create desktop entry content
            content = f"""[Desktop Entry]
Name=Route Planner
Exec={app_path}
Icon=map
Terminal=false
Type=Application
Categories=Office;Utility;
Comment=Delivery Route Optimization Application
"""
            
            # Write desktop file
            desktop_file = user_apps / 'route-planner.desktop'
            with open(desktop_file, 'w') as f:
                f.write(content)
            os.chmod(desktop_file, 0o755)  # Make executable
            
            # Create desktop shortcut
            desktop_shortcut = desktop / 'route-planner.desktop'
            shutil.copy(desktop_file, desktop_shortcut)
            os.chmod(desktop_shortcut, 0o755)  # Make executable
            
            # Update desktop database
            try:
                subprocess.run(['update-desktop-database', str(user_apps)], 
                             capture_output=True)
            except:
                pass  # Not critical if this fails
            
            return True
        except Exception as e:
            logger.error(f"Desktop entry creation failed: {e}")
            return False
    
    def _check_linux_packaging_support(self):
        """
        Check for Linux packaging support (AppImage, Flatpak, Snap).
        
        Returns:
            str or dict: The type of packaging support found or detailed dict if multiple found
        """
        # Use enhanced platform manager if available
        if self.platform_manager:
            try:
                # Get packaging capabilities from platform manager
                recommended = self.platform_manager.get_best_executable_format()
                
                # If platform manager provides formats, use those
                if 'formats' in recommended and recommended.get('formats'):
                    available_formats = [
                        format_id for format_id, format_info in recommended.get('formats', {}).items() 
                        if format_info.get('available', False)
                    ]
                    
                    if len(available_formats) > 1:
                        # Return dict of available formats
                        return {
                            format_id: recommended.get('formats', {}).get(format_id, {}).get('name', format_id.capitalize())
                            for format_id in available_formats
                        }
                    elif len(available_formats) == 1:
                        # Return the single format name for backward compatibility
                        format_id = available_formats[0]
                        return recommended.get('formats', {}).get(format_id, {}).get('name', format_id.capitalize())
            except Exception as e:
                logger.warning(f"Error checking platform manager for packaging support: {e}")
        
        # Fallback to basic detection
        packaging_tools = {
            'appimage-builder': 'AppImage',
            'appimagetool': 'AppImage',
            'flatpak-builder': 'Flatpak',
            'flatpak': 'Flatpak',
            'snapcraft': 'Snap',
            'snap': 'Snap'
        }
        
        found_formats = {}
        
        for tool, packaging_type in packaging_tools.items():
            try:
                result = subprocess.run(['which', tool], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    found_formats[packaging_type.lower()] = packaging_type
            except:
                continue
        
        if len(found_formats) > 1:
            return found_formats
        elif len(found_formats) == 1:
            return next(iter(found_formats.values()))
        
        return None
    
    def show_success_notification(self):
        """Show a platform-appropriate success notification."""
        message = "Installation completed successfully! You can now run Route Planner."
        
        if self.platform_manager:
            try:
                self.platform_manager.show_notification(
                    title="Route Planner",
                    message=message
                )
                return
            except Exception as e:
                logger.warning(f"Enhanced notification failed: {e}")
        
        # Fallback notification
        print("\n" + "=" * 60)
        print(f"✅ {message}")
        print("=" * 60)


# Direct execution handling
if __name__ == "__main__":
    print("╔════════════════════════════════════════╗")
    print("║ Route Planner Universal Installer Tool ║")
    print("╚════════════════════════════════════════╝")
    
    # Check for test mode
    if "--test" in sys.argv:
        print("\n🧪 Running in test mode - no changes will be made")
        
        # Create installer for testing only
        installer = UniversalInstaller(global_install=False)
        
        # Get and display platform information
        print(f"\n📊 Platform: {installer.platform}")
        
        if installer.platform_manager:
            print("\n✅ Enhanced platform management is available")
            features = installer.platform_manager.features
            enabled = [k for k, v in features.items() if v]
            print(f"📋 Platform features: {', '.join(enabled)}")
            
            # Show packaging formats if available
            recommended = installer.platform_manager.get_best_executable_format()
            print(f"\n🔍 Recommended format: {recommended.get('description', 'Unknown')}")
            
            if installer.platform == "Linux" and isinstance(recommended.get('formats'), dict):
                formats = recommended.get('formats', {})
                available_formats = [f"{info.get('name', key)} ({key})" 
                                    for key, info in formats.items() 
                                    if info.get('available', False)]
                if available_formats:
                    print(f"📦 Available packaging formats: {', '.join(available_formats)}")
        else:
            print("\n⚠️ Enhanced platform management is not available")
            
        # Test packaging support detection
        if installer.platform == "Linux":
            packaging_support = installer._check_linux_packaging_support()
            if packaging_support:
                if isinstance(packaging_support, dict):
                    print(f"\n📦 Multiple packaging formats detected: {', '.join(packaging_support.keys())}")
                else:
                    print(f"\n📦 Packaging support detected: {packaging_support}")
            else:
                print("\n⚠️ No packaging support detected")
                
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    
    # Check for global installation flag
    global_install = "--global" in sys.argv
    if global_install:
        print("\n🌐 Performing global installation (system-wide)")
    else:
        print("\n👤 Performing user installation (current user only)")
    
    # Create and run the installer
    installer = UniversalInstaller(global_install=global_install)
    success = installer.install()
    
    if success:
        print("\n🚀 Installation Summary:")
        print("- Route Planner is now installed")
        print("- You can run it by typing 'route-planner' in a terminal")
        if installer.app_path:
            print(f"- Executable path: {installer.app_path}")
        
        # Platform-specific notes
        if installer.platform == "Windows":
            print("\n💡 Windows users: Check your Start menu and Desktop for shortcuts")
        elif installer.platform == "Darwin":
            print("\n💡 macOS users: Check your Applications folder and Desktop for shortcuts")
        elif installer.platform == "Linux":
            print("\n💡 Linux users: Check your application menu and Desktop for shortcuts")
        
        sys.exit(0)
    else:
        print("\n❌ Installation failed. Please see the logs above for details.")
        sys.exit(1)
