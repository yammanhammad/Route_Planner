#!/usr/bin/env python3
"""
Generate Windows version info file for PyInstaller.
This dynamically creates version information for the Windows executable.
"""

import sys
from pathlib import Path

def get_version():
    """Get the current version from route_planner/__init__.py"""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    sys.path.insert(0, str(project_dir))
    
    try:
        from route_planner import __version__
        return __version__
    except ImportError:
        # Fallback: read directly from file
        init_file = project_dir / "route_planner" / "__init__.py"
        if init_file.exists():
            import re
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
            if match:
                return match.group(1)
    
    raise RuntimeError("Unable to determine version")

def generate_version_file():
    """Generate version info file for PyInstaller"""
    version = get_version()
    version_parts = version.split('.')
    
    # Ensure we have 4 parts for Windows version (major.minor.patch.build)
    while len(version_parts) < 4:
        version_parts.append('0')
    
    version_tuple = tuple(int(part) for part in version_parts[:4])
    
    version_info_template = f'''# UTF-8
# Version information for PyInstaller - automatically generated
from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, 
    StringStruct, VarFileInfo, VarStruct
)

version_info = VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers={version_tuple},
    prodvers={version_tuple},
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Route Planner Team'),
        StringStruct(u'FileDescription', u'Route Planner - Delivery Route Optimization Application'),
        StringStruct(u'FileVersion', u'{version}'),
        StringStruct(u'InternalName', u'RoutePlanner'),
        StringStruct(u'LegalCopyright', u'© 2025 Route Planner Team. Licensed under MIT License.'),
        StringStruct(u'OriginalFilename', u'RoutePlanner.exe'),
        StringStruct(u'ProductName', u'Route Planner'),
        StringStruct(u'ProductVersion', u'{version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''

    # Write to version file
    version_file = Path(__file__).parent / "version_info_generated.py"
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(version_info_template)
    
    print(f"Generated version info file for version {version}")
    return str(version_file)

if __name__ == "__main__":
    generate_version_file()
