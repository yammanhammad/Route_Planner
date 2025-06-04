;Route Planner Windows Installer Script (NSIS)
;Creates a professional Windows installer with Visual C++ Redistributable

!define APP_NAME "Route Planner"
!define APP_VERSION "1.1.0"
!define APP_PUBLISHER "Route Planner Team"
!define APP_URL "https://github.com/yammanhammad/Route_Planner"
!define APP_EXECUTABLE "RoutePlanner.exe"
!define VCREDIST_URL "https://aka.ms/vs/17/release/vc_redist.x64.exe"

;Include Modern UI and additional functionality
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "nsDialogs.nsh"

;Required for downloading files
!include "WinVer.nsh"

;General Settings
Name "${APP_NAME}"
OutFile "dist\RoutePlanner-${APP_VERSION}-Setup.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKCU "Software\${APP_NAME}" ""
RequestExecutionLevel admin

;Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

;Welcome page
!insertmacro MUI_PAGE_WELCOME

;License page  
!insertmacro MUI_PAGE_LICENSE "LICENSE"

;Directory page
!insertmacro MUI_PAGE_DIRECTORY

;Installation page
!insertmacro MUI_PAGE_INSTFILES

;Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXECUTABLE}"
!define MUI_FINISHPAGE_RUN_TEXT "Start ${APP_NAME}"
!insertmacro MUI_PAGE_FINISH

;Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;Languages
!insertmacro MUI_LANGUAGE "English"

;Version Information
VIProductVersion "1.1.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "${APP_NAME}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "© 2025 ${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "${APP_NAME} Installer"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${APP_VERSION}"

;Check and install Visual C++ Redistributable
Function .onInit
  ;Check if Visual C++ Redistributable is installed
  Call CheckVCRedist
FunctionEnd

Function CheckVCRedist
  ;Check registry for Visual C++ 2015-2022 Redistributable
  ReadRegStr $0 HKLM "SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Version"
  ${If} $0 == ""
    ;Check alternative location
    ReadRegStr $0 HKLM "SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Version"
  ${EndIf}
  
  ${If} $0 == ""
    MessageBox MB_YESNO|MB_ICONQUESTION \
      "Microsoft Visual C++ Redistributable is required but not installed.$\n$\nWould you like to download and install it now?$\n$\n(This is necessary for the application to run properly)" \
      IDYES InstallVCRedist IDNO SkipVCRedist
    
    InstallVCRedist:
      DetailPrint "Downloading Visual C++ Redistributable..."
      NSISdl::download "${VCREDIST_URL}" "$TEMP\vc_redist.x64.exe"
      Pop $R0
      ${If} $R0 == "success"
        DetailPrint "Installing Visual C++ Redistributable..."
        ExecWait '"$TEMP\vc_redist.x64.exe" /quiet /norestart' $0
        Delete "$TEMP\vc_redist.x64.exe"
        ${If} $0 != 0
          MessageBox MB_OK|MB_ICONEXCLAMATION \
            "Visual C++ Redistributable installation failed.$\n$\nYou may need to install it manually from:$\n${VCREDIST_URL}"
        ${Else}
          DetailPrint "Visual C++ Redistributable installed successfully"
        ${EndIf}
      ${Else}
        MessageBox MB_OK|MB_ICONEXCLAMATION \
          "Failed to download Visual C++ Redistributable.$\n$\nPlease download and install it manually from:$\n${VCREDIST_URL}"
      ${EndIf}
      Goto EndVCRedist
    
    SkipVCRedist:
      MessageBox MB_OK|MB_ICONWARNING \
        "The application may not work properly without Visual C++ Redistributable.$\n$\nIf you encounter errors, please install it from:$\n${VCREDIST_URL}"
    
    EndVCRedist:
  ${Else}
    DetailPrint "Visual C++ Redistributable is already installed"
  ${EndIf}
FunctionEnd

;Installation Section
Section "Main Application" SecMain
  SetOutPath "$INSTDIR"
  
  ;Add files
  File "dist\${APP_EXECUTABLE}"
  File "README.md"
  File "LICENSE"
  File "CHANGELOG.md"
  
  ;Add documentation folder if exists
  IfFileExists "docs" 0 +3
  SetOutPath "$INSTDIR\docs"
  File /r "docs\*.*"
  
  ;Store installation folder
  WriteRegStr HKCU "Software\${APP_NAME}" "" $INSTDIR
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ;Add to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "DisplayIcon" "$INSTDIR\${APP_EXECUTABLE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "URLInfoAbout" "${APP_URL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                   "DisplayVersion" "${APP_VERSION}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                     "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
                     "NoRepair" 1
SectionEnd

;Start Menu Shortcuts
Section "Start Menu Shortcuts" SecStartMenu
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

;Desktop Shortcut
Section "Desktop Shortcut" SecDesktop
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}"
SectionEnd

;Section Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} "Install the main ${APP_NAME} application."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Create shortcuts in the Start Menu."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create a shortcut on the Desktop."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;Uninstaller Section
Section "Uninstall"
  ;Remove files and directories
  Delete "$INSTDIR\${APP_EXECUTABLE}"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\LICENSE" 
  Delete "$INSTDIR\CHANGELOG.md"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir /r "$INSTDIR\docs"
  RMDir "$INSTDIR"
  
  ;Remove shortcuts
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  
  ;Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKCU "Software\${APP_NAME}"
SectionEnd
