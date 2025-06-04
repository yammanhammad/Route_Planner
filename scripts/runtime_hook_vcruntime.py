"""
PyInstaller runtime hook for better Visual C++ runtime loading
This hook ensures proper loading of Visual C++ runtime components
"""

import os
import sys
import ctypes
from pathlib import Path

def setup_vcruntime():
    """Setup Visual C++ runtime for better compatibility"""
    try:
        # Get the application directory
        if hasattr(sys, '_MEIPASS'):
            # Running from PyInstaller bundle
            app_dir = Path(sys._MEIPASS)
        else:
            # Running from source
            app_dir = Path(__file__).parent
        
        # Add app directory to PATH for DLL loading
        app_dir_str = str(app_dir)
        current_path = os.environ.get('PATH', '')
        if app_dir_str not in current_path:
            os.environ['PATH'] = app_dir_str + os.pathsep + current_path
        
        # Try to preload common Visual C++ runtime libraries
        runtime_libs = [
            'vcruntime140.dll',
            'msvcp140.dll', 
            'api-ms-win-crt-runtime-l1-1-0.dll',
            'ucrtbase.dll'
        ]
        
        for lib in runtime_libs:
            try:
                lib_path = app_dir / lib
                if lib_path.exists():
                    # Try to load the library
                    ctypes.windll.kernel32.LoadLibraryW(str(lib_path))
            except (OSError, AttributeError):
                # Library not found or not on Windows, continue
                pass
        
        # Set additional environment variables for runtime
        os.environ['PYTHONPATH'] = app_dir_str + os.pathsep + os.environ.get('PYTHONPATH', '')
        
    except Exception:
        # If anything fails, continue silently
        # We don't want runtime hook failures to break the app
        pass

# Run the setup
setup_vcruntime()
