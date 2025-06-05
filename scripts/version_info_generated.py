# UTF-8
# Version information for PyInstaller - automatically generated
from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, 
    StringStruct, VarFileInfo, VarStruct
)

version_info = VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1, 1, 2, 0),
    prodvers=(1, 1, 2, 0),
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
        StringStruct(u'FileVersion', u'1.1.2'),
        StringStruct(u'InternalName', u'RoutePlanner'),
        StringStruct(u'LegalCopyright', u'© 2025 Route Planner Team. Licensed under MIT License.'),
        StringStruct(u'OriginalFilename', u'RoutePlanner.exe'),
        StringStruct(u'ProductName', u'Route Planner'),
        StringStruct(u'ProductVersion', u'1.1.2')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
