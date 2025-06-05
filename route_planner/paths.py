#!/usr/bin/env python3
"""
Path Utilities for Cross-Platform Compatibility
==============================================

This module provides path-related utility functions that ensure
cross-platform compatibility for the Route Planner application.
"""

import os
import sys
import platform
from pathlib import Path

def get_app_dir():
    """
    Get the application directory in a cross-platform compatible way.
    
    Returns:
        Path: The application directory
    """
    return Path(__file__).parent.absolute()

def get_home_dir():
    """
    Get the user's home directory in a cross-platform compatible way.
    
    Returns:
        Path: The user's home directory
    """
    return Path.home()

def get_config_dir():
    """
    Get the configuration directory in a cross-platform compatible way.
    
    Returns:
        Path: The configuration directory
    """
    # Check for WINDOWS_MOCK environment variable for testing
    if os.environ.get('WINDOWS_MOCK') == 'true':
        app_data = os.environ.get('APPDATA')
        if app_data:
            return Path(app_data) / "RoutePlanner"
    
    if platform.system() == "Windows":
        # Use AppData/Roaming on Windows
        app_data = os.environ.get('APPDATA')
        if app_data:
            return Path(app_data) / "RoutePlanner"
        else:
            return get_home_dir() / ".route_planner"
    elif platform.system() == "Darwin":  # macOS
        return get_home_dir() / "Library/Application Support/RoutePlanner"
    else:  # Linux and other Unix
        xdg_config = os.environ.get('XDG_CONFIG_HOME')
        if xdg_config:
            return Path(xdg_config) / "route_planner"
        else:
            return get_home_dir() / ".config/route_planner"

def get_cache_dir():
    """
    Get the cache directory in a cross-platform compatible way.
    
    Returns:
        Path: The cache directory
    """
    app_dir = get_app_dir()
    cache_dir = app_dir / "cache"
    
    # Create cache directory if it doesn't exist
    if not cache_dir.exists():
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to create cache directory: {e}")
            # Fallback to a temporary directory
            import tempfile
            cache_dir = Path(tempfile.gettempdir()) / "route_planner_cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
    
    return cache_dir

def get_data_dir():
    """
    Get the data directory in a cross-platform compatible way.
    
    Returns:
        Path: The data directory
    """
    app_dir = get_app_dir()
    data_dir = app_dir / "data"
    
    # Create data directory if it doesn't exist
    if not data_dir.exists():
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to create data directory: {e}")
            # Fallback to a temporary directory
            import tempfile
            data_dir = Path(tempfile.gettempdir()) / "route_planner_data"
            data_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir

def get_logs_dir():
    """
    Get the logs directory in a cross-platform compatible way.
    
    Returns:
        Path: The logs directory
    """
    app_dir = get_app_dir()
    logs_dir = app_dir / "logs"
    
    # Create logs directory if it doesn't exist
    if not logs_dir.exists():
        try:
            logs_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to create logs directory: {e}")
            # Fallback to a temporary directory
            import tempfile
            logs_dir = Path(tempfile.gettempdir()) / "route_planner_logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
    
    return logs_dir

def get_platform_script(script_name):
    """
    Get the appropriate script name for the current platform.
    
    Args:
        script_name (str): Base name of the script
    
    Returns:
        Path: The platform-specific script path
    """
    app_dir = get_app_dir().parent  # Go up one level to project root
    
    if platform.system() == "Windows":
        # Check for .bat extension first, then .py
        if (app_dir / f"{script_name}.bat").exists():
            return app_dir / f"{script_name}.bat"
        else:
            return app_dir / f"{script_name}.py"
    else:
        # Check for .sh extension first, then .py
        if (app_dir / f"{script_name}.sh").exists():
            return app_dir / f"{script_name}.sh"
        else:
            return app_dir / f"{script_name}.py"

def make_executable(file_path):
    """
    Make a file executable (Unix only).
    
    Args:
        file_path (Path): Path to the file
    """
    if platform.system() != "Windows" and os.path.exists(file_path):
        current_mode = os.stat(file_path).st_mode
        executable_mode = current_mode | 0o111  # Add executable bit for user/group/others
        os.chmod(file_path, executable_mode)

def ensure_dir_exists(dir_path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        dir_path (Path): Path to the directory
    
    Returns:
        bool: True if the directory exists or was created, False otherwise
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {dir_path}: {e}")
        return False

def get_venv_python():
    """
    Get the path to the Python executable in the virtual environment.
    
    Returns:
        Path: Path to the Python executable
    """
    app_dir = get_app_dir()
    venv_dir = app_dir / ".venv"
    
    if platform.system() == "Windows":
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"

def get_venv_pip():
    """
    Get the path to the pip executable in the virtual environment.
    
    Returns:
        Path: Path to the pip executable
    """
    app_dir = get_app_dir()
    venv_dir = app_dir / ".venv"
    
    if platform.system() == "Windows":
        return venv_dir / "Scripts" / "pip.exe"
    else:
        return venv_dir / "bin" / "pip"

def normalize_path(path_str):
    """
    Normalize a path string to a Path object, handling platform-specific separators.
    
    Args:
        path_str (str): Path string to normalize
    
    Returns:
        Path: Normalized path
    """
    # Convert to Path object which handles normalization
    return Path(path_str)

class PlatformManager:
    """
    Manage platform-specific features gracefully.
    
    This class provides a unified interface for platform-specific
    features while gracefully degrading when features are not available.
    It allows the application to take advantage of platform capabilities
    while maintaining cross-platform compatibility.
    """
    
    def __init__(self):
        """Initialize the platform manager with platform detection."""
        self.platform = platform.system()
        self.version = platform.version()
        self.machine = platform.machine()
        self.features = self._detect_features()
        self.paths = self._setup_platform_paths()
    
    def _detect_features(self):
        """
        Detect platform-specific features and capabilities.
        
        Returns:
            dict: Dictionary of available features
        """
        features = {
            "desktop_integration": False,
            "native_notifications": False,
            "system_tray": False,
            "start_menu": False,
            "dock_integration": False,
            "mime_types": False,
            "autostart": False,
            "url_handlers": False,
            "file_associations": False,
            "native_packaging": False
        }
        
        if self.platform == "Windows":
            features.update({
                "desktop_integration": True,
                "native_notifications": True,
                "system_tray": True,
                "start_menu": True,
                "autostart": True,
                "url_handlers": True,
                "file_associations": True,
                "native_packaging": True
            })
        elif self.platform == "Darwin":  # macOS
            features.update({
                "desktop_integration": True,
                "native_notifications": True,
                "dock_integration": True,
                "autostart": True,
                "url_handlers": True,
                "file_associations": True,
                "native_packaging": True
            })
        elif self.platform == "Linux":
            features.update({
                "desktop_integration": True,
                "native_notifications": self._check_linux_notifications(),
                "mime_types": True,
                "autostart": True,
                "url_handlers": True,
                "file_associations": True,
                "native_packaging": self._check_linux_packaging()
            })
            
        return features
    
    def _check_linux_notifications(self):
        """
        Check if Linux desktop notifications are available.
        
        Returns:
            bool: True if notifications are available, False otherwise
        """
        try:
            import subprocess
            result = subprocess.run(['which', 'notify-send'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _check_linux_packaging(self):
        """
        Check for Linux packaging capabilities.
        
        Returns:
            dict: Dictionary with packaging capabilities information
        """
        # Check for AppImage, Flatpak, or Snap support
        packaging_formats = {
            'appimage': {
                'available': False,
                'tools': ['appimage-builder', 'appimagetool'],
                'name': 'AppImage',
                'priority': 1,  # Preferred option (simplest to distribute)
                'script_path': None
            },
            'flatpak': {
                'available': False,
                'tools': ['flatpak-builder', 'flatpak'],
                'name': 'Flatpak',
                'priority': 2,
                'manifest_path': None
            },
            'snap': {
                'available': False,
                'tools': ['snapcraft', 'snap'],
                'name': 'Snap',
                'priority': 3,
                'snapcraft_path': None
            }
        }
        
        found_any = False
        
        # Check each packaging format
        for format_id, format_info in packaging_formats.items():
            for tool in format_info['tools']:
                try:
                    import subprocess
                    result = subprocess.run(['which', tool], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        packaging_formats[format_id]['available'] = True
                        found_any = True
                        break
                except:
                    continue
        
        # Check for AppImage build script
        app_dir = get_app_dir()
        project_root = app_dir.parent
        
        # Look for build scripts in the project
        if packaging_formats['appimage']['available']:
            appimage_script = project_root / 'scripts' / 'build_appimage.py'
            if appimage_script.exists():
                packaging_formats['appimage']['script_path'] = str(appimage_script)
                
        # Look for Flatpak manifest
        if packaging_formats['flatpak']['available']:
            flatpak_manifest = project_root / 'flatpak' / 'org.routeplanner.RoutePlanner.yml'
            if flatpak_manifest.exists():
                packaging_formats['flatpak']['manifest_path'] = str(flatpak_manifest)
                
        # Look for Snap manifest
        if packaging_formats['snap']['available']:
            snapcraft_yaml = project_root / 'snap' / 'snapcraft.yaml'
            if snapcraft_yaml.exists():
                packaging_formats['snap']['snapcraft_path'] = str(snapcraft_yaml)
        
        # For backward compatibility, still return a boolean if nothing has changed
        if not found_any:
            return False
            
        return packaging_formats
    
    def _setup_platform_paths(self):
        """
        Setup platform-specific path configurations.
        
        Returns:
            dict: Dictionary of platform-specific paths
        """
        paths = {
            "config": get_config_dir(),
            "cache": get_cache_dir(),
            "data": get_data_dir(),
            "logs": get_logs_dir(),
            "app": get_app_dir(),
            "home": get_home_dir()
        }
        
        # Add platform-specific paths
        if self.platform == "Windows":
            paths.update({
                "start_menu": Path(os.environ.get('APPDATA', '')) / "Microsoft/Windows/Start Menu/Programs",
                "desktop": get_home_dir() / "Desktop",
                "temp": Path(os.environ.get('TEMP', '')),
                "program_files": Path(os.environ.get('PROGRAMFILES', ''))
            })
        elif self.platform == "Darwin":
            paths.update({
                "applications": Path("/Applications"),
                "user_applications": get_home_dir() / "Applications",
                "desktop": get_home_dir() / "Desktop",
                "library": get_home_dir() / "Library"
            })
        elif self.platform == "Linux":
            paths.update({
                "desktop": get_home_dir() / "Desktop",
                "applications": Path("/usr/share/applications"),
                "user_applications": get_home_dir() / ".local/share/applications",
                "autostart": get_home_dir() / ".config/autostart"
            })
            
        return paths
    
    def get_best_executable_format(self):
        """
        Return the best executable format for current platform.
        
        Returns:
            dict: Dictionary with recommended formats and alternatives
        """
        if self.platform == "Windows":
            return {
                "primary": "windows_executable",      # .exe with bundled deps
                "alternatives": [
                    "windows_installer",              # NSIS installer
                    "python_package"                  # pip install
                ],
                "description": "Windows Executable (.exe)",
                "status": "supported",
                "tools": ["pyinstaller", "NSIS"]
            }
        elif self.platform == "Darwin":
            return {
                "primary": "macos_app_bundle",        # .app bundle
                "alternatives": [
                    "python_package",                 # pip install
                    "macos_pkg"                       # macOS installer
                ],
                "description": "macOS App Bundle (.app)",
                "status": "supported",
                "tools": ["py2app", "create-dmg"]
            }
        elif self.platform == "Linux":
            # Check for Linux packaging support
            packaging = self._check_linux_packaging()
            
            # Default to Python package
            result = {
                "primary": "python_package",           # pip install
                "alternatives": [
                    "python_script"                    # python main.py
                ],
                "description": "Python Package (pip)",
                "status": "basic",
                "tools": ["pip"],
                "formats": {}
            }
            
            # If we found packaging support, prioritize appropriately
            if isinstance(packaging, dict):
                formats = {}
                # Check for available formats
                for format_id, format_info in packaging.items():
                    if format_info.get('available', False):
                        formats[format_id] = {
                            "name": format_info.get('name'),
                            "available": True,
                            "script_path": format_info.get('script_path'),
                            "priority": format_info.get('priority', 999)
                        }
                
                result["formats"] = formats
                
                # AppImage is top priority if available
                if packaging.get('appimage', {}).get('available', False):
                    result["primary"] = "appimage"
                    result["alternatives"].insert(0, "python_package")
                    result["description"] = "AppImage (portable)"
                    result["status"] = "enhanced"
                    result["tools"].append("appimagetool")
                # Flatpak is second priority
                elif packaging.get('flatpak', {}).get('available', False):
                    result["primary"] = "flatpak"
                    result["alternatives"].insert(0, "python_package")
                    result["description"] = "Flatpak (sandboxed)"
                    result["status"] = "enhanced"
                    result["tools"].append("flatpak-builder")
                # Snap is third priority
                elif packaging.get('snap', {}).get('available', False):
                    result["primary"] = "snap"
                    result["alternatives"].insert(0, "python_package")
                    result["description"] = "Snap Package"
                    result["status"] = "enhanced"
                    result["tools"].append("snapcraft")
            
            return result
        
        # Generic fallback for unknown platforms
        return {
            "primary": "python_package",
            "alternatives": [
                "python_script"
            ],
            "description": "Python Package (pip)",
            "status": "basic",
            "tools": ["pip"]
        }
    
    def get_platform_requirements(self):
        """
        Get platform-specific Python requirements.
        
        Returns:
            list: List of required packages for the platform
        """
        base_reqs = ["PyQt5", "folium", "networkx", "osmnx", "requests", "geopy"]
        
        if self.platform == "Windows":
            base_reqs.extend(["pywin32", "winshell"])
        elif self.platform == "Darwin":
            base_reqs.extend(["pyobjc-framework-Cocoa"])
        elif self.platform == "Linux":
            # Check for specific Linux desktop environment
            desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
            if 'gnome' in desktop_env:
                base_reqs.extend(["PyGObject"])
            elif 'kde' in desktop_env:
                base_reqs.extend(["PyQt5"])  # Already included but ensure KDE compatibility
        
        return base_reqs
    
    def create_desktop_entry(self, app_name, exec_path, icon_path=None, 
                           description="Route Planner Application"):
        """
        Create platform-appropriate desktop entry/shortcut.
        
        Args:
            app_name (str): Name of the application
            exec_path (str): Path to the executable
            icon_path (str, optional): Path to the icon
            description (str, optional): Application description
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.features["desktop_integration"]:
            return False
            
        try:
            if self.platform == "Windows":
                return self._create_windows_shortcut(app_name, exec_path, icon_path)
            elif self.platform == "Darwin":
                return self._create_macos_shortcut(app_name, exec_path, icon_path)
            elif self.platform == "Linux":
                return self._create_linux_desktop_file(app_name, exec_path, 
                                                     icon_path, description)
        except Exception as e:
            print(f"Warning: Could not create desktop entry: {e}")
            return False
    
    def _create_windows_shortcut(self, app_name, exec_path, icon_path):
        """
        Create Windows desktop shortcut.
        
        Args:
            app_name (str): Name of the application
            exec_path (str): Path to the executable
            icon_path (str, optional): Path to the icon
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import winshell
            desktop = self.paths["desktop"]
            shortcut_path = desktop / f"{app_name}.lnk"
            winshell.CreateShortcut(
                Path=str(shortcut_path),
                Target=str(exec_path),
                Icon=(str(icon_path), 0) if icon_path else None,
                Description=f"Launch {app_name}"
            )
            return True
        except ImportError:
            # Fallback to batch file
            shortcut_path = self.paths["desktop"] / f"{app_name}.bat"
            with open(shortcut_path, 'w') as f:
                f.write(f'@echo off\nstart "" "{exec_path}"\n')
            return True
        except Exception as e:
            print(f"Warning: Could not create Windows shortcut: {e}")
            return False
    
    def _create_macos_shortcut(self, app_name, exec_path, icon_path):
        """
        Create macOS desktop shortcut.
        
        Args:
            app_name (str): Name of the application
            exec_path (str): Path to the executable
            icon_path (str, optional): Path to the icon
            
        Returns:
            bool: True if successful, False otherwise
        """
        shortcut_path = self.paths["desktop"] / f"{app_name}.command"
        with open(shortcut_path, 'w') as f:
            f.write(f'#!/bin/bash\n"{exec_path}"\n')
        make_executable(shortcut_path)
        return True
    
    def _create_linux_desktop_file(self, app_name, exec_path, icon_path, description):
        """
        Create Linux .desktop file.
        
        Args:
            app_name (str): Name of the application
            exec_path (str): Path to the executable
            icon_path (str, optional): Path to the icon
            description (str): Application description
            
        Returns:
            bool: True if successful, False otherwise
        """
        desktop_file = self.paths["desktop"] / f"{app_name.lower().replace(' ', '-')}.desktop"
        
        content = f"""[Desktop Entry]
Name={app_name}
Exec={exec_path}
Icon={icon_path or 'application-x-executable'}
Terminal=false
Type=Application
Categories=Office;Utility;
Comment={description}
"""
        
        with open(desktop_file, 'w') as f:
            f.write(content)
        make_executable(desktop_file)
        
        # Also install to applications directory if possible
        if "user_applications" in self.paths:
            apps_file = self.paths["user_applications"] / f"{app_name.lower().replace(' ', '-')}.desktop"
            ensure_dir_exists(self.paths["user_applications"])
            with open(apps_file, 'w') as f:
                f.write(content)
            make_executable(apps_file)
            
        return True
    
    def install_to_applications(self, app_name, exec_path, icon_path=None,
                              description="Route Planner Application"):
        """
        Install application to system applications directory.
        
        Args:
            app_name (str): Name of the application
            exec_path (str): Path to the executable
            icon_path (str, optional): Path to the icon
            description (str, optional): Application description
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.features["desktop_integration"]:
            return False
            
        try:
            if self.platform == "Linux":
                # Install to user applications directory
                app_file = self.paths["user_applications"] / f"{app_name.lower().replace(' ', '-')}.desktop"
                ensure_dir_exists(self.paths["user_applications"])
                
                content = f"""[Desktop Entry]
Name={app_name}
Exec={exec_path}
Icon={icon_path or 'application-x-executable'}
Terminal=false
Type=Application
Categories=Office;Utility;
Comment={description}
StartupNotify=true
"""
                with open(app_file, 'w') as f:
                    f.write(content)
                make_executable(app_file)
                
                # Update desktop database
                try:
                    import subprocess
                    subprocess.run(['update-desktop-database', 
                                  str(self.paths["user_applications"])], 
                                 capture_output=True)
                except:
                    pass  # Not critical if this fails
                    
                return True
            elif self.platform == "Darwin":
                # Create a link in the Applications folder
                apps_dir = self.paths["user_applications"]
                ensure_dir_exists(apps_dir)
                
                app_script = apps_dir / f"{app_name}.command"
                with open(app_script, 'w') as f:
                    f.write(f'#!/bin/bash\n"{exec_path}"\n')
                make_executable(app_script)
                return True
            elif self.platform == "Windows":
                # Create shortcut in Start Menu
                start_menu = self.paths.get("start_menu")
                if start_menu:
                    app_dir = start_menu / app_name
                    ensure_dir_exists(app_dir)
                    
                    shortcut_path = app_dir / f"{app_name}.bat"
                    with open(shortcut_path, 'w') as f:
                        f.write(f'@echo off\nstart "" "{exec_path}"\n')
                    return True
        except Exception as e:
            print(f"Warning: Could not install to applications: {e}")
            return False
    
    def show_notification(self, title, message, icon=None):
        """
        Show platform-appropriate notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            icon (str, optional): Path to the icon
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.features["native_notifications"]:
            return False
            
        try:
            if self.platform == "Windows":
                return self._show_windows_notification(title, message, icon)
            elif self.platform == "Darwin":
                return self._show_macos_notification(title, message)
            elif self.platform == "Linux":
                return self._show_linux_notification(title, message, icon)
        except Exception as e:
            print(f"Warning: Could not show notification: {e}")
            return False
    
    def _show_windows_notification(self, title, message, icon):
        """
        Show Windows notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            icon (str, optional): Path to the icon
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import win10toast
            toaster = win10toast.ToastNotifier()
            toaster.show_toast(title, message, icon_path=icon, duration=5)
            return True
        except ImportError:
            try:
                # Fallback to Windows Script Host
                import subprocess
                vbs_script = f"""
                Set objShell = CreateObject("Wscript.Shell")
                objShell.Popup "{message}", 5, "{title}", 64
                """
                with open("temp_notification.vbs", "w") as f:
                    f.write(vbs_script)
                subprocess.run(["cscript", "//nologo", "temp_notification.vbs"], 
                             check=True, stderr=subprocess.PIPE)
                import os
                os.remove("temp_notification.vbs")
                return True
            except:
                return False
    
    def _show_macos_notification(self, title, message):
        """
        Show macOS notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import subprocess
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], capture_output=True)
            return True
        except:
            return False
    
    def _show_linux_notification(self, title, message, icon):
        """
        Show Linux notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            icon (str, optional): Path to the icon
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import subprocess
            cmd = ['notify-send']
            if icon:
                cmd.extend(['-i', str(icon)])
            cmd.extend([title, message])
            subprocess.run(cmd, capture_output=True)
            return True
        except:
            return False
    
    def get_platform_info(self):
        """
        Get comprehensive platform information.
        
        Returns:
            dict: Platform information
        """
        return {
            "platform": self.platform,
            "version": self.version,
            "machine": self.machine,
            "python_version": sys.version,
            "features": self.features,
            "paths": {k: str(v) for k, v in self.paths.items()},
            "recommended_format": self.get_best_executable_format()
        }


# Global platform manager instance
_platform_manager = None

def get_platform_manager():
    """
    Get the global platform manager instance.
    
    Returns:
        PlatformManager: The global platform manager instance
    """
    global _platform_manager
    if _platform_manager is None:
        _platform_manager = PlatformManager()
    return _platform_manager

if __name__ == "__main__":
    # Print path information for debugging
    print("=== Route Planner Platform Information ===")
    print(f"Application Directory: {get_app_dir()}")
    print(f"Home Directory: {get_home_dir()}")
    print(f"Config Directory: {get_config_dir()}")
    print(f"Cache Directory: {get_cache_dir()}")
    print(f"Data Directory: {get_data_dir()}")
    print(f"Logs Directory: {get_logs_dir()}")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.executable}")
    
    # Platform-specific script information
    if platform.system() == "Windows":
        print(f"Windows-specific script: {get_platform_script('run_route_planner')}")
    else:
        print(f"Unix-specific script: {get_platform_script('run_route_planner')}")
    
    # Enhanced platform information
    print("\n=== Enhanced Platform Features ===")
    pm = get_platform_manager()
    info = pm.get_platform_info()
    
    print(f"Recommended Format: {info['recommended_format']}")
    print("Available Features:")
    for feature, available in info['features'].items():
        status = "✅" if available else "❌"
        print(f"  {status} {feature.replace('_', ' ').title()}")
    
    print("\nPlatform-Specific Paths:")
    for name, path in info['paths'].items():
        print(f"  {name}: {path}")
