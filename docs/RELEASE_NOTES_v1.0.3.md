# Release Notes - Version 1.0.3

**Release Date**: June 2025

## 🔒 Enhanced Security and Permissions

This release focuses on fixing GitHub Actions permissions and improving the automated build system.

### 🆕 What's New

- **Fixed GitHub Actions Permissions**: Added proper permissions for release creation
- **Enhanced Build Security**: Improved workflow security with explicit permission declarations
- **Robust Release Process**: Fixed automated release creation process

### 🔧 Technical Improvements

- Added `contents: write` permission for GitHub Actions to create releases
- Added `actions: read` permission for workflow artifact access
- Added `checks: write` permission for creating status checks
- Enhanced workflow reliability for automated builds

### 📦 Download Options

**For Windows Users (Recommended)**:
- Download the Windows executable ZIP file from the release assets below
- Extract and double-click `RoutePlanner.exe` to run
- No Python installation required!

**For Python Users**:
- Install via pip: `pip install route-planner==1.0.3`
- Download source code and run: `python main.py`

### 🛠️ Build System

- ✅ GitHub Actions workflow permissions fixed
- ✅ Automatic building on tag releases working properly
- ✅ Manual trigger support maintained
- ✅ Cross-platform compatibility preserved

### 📚 Documentation

- All version references updated to 1.0.3
- Consistent versioning across all files and documentation
- Enhanced release process documentation

---

**Windows executable will be available shortly after release publication.**

**Full Changelog**: https://github.com/yammanhammad/Route_Planner/compare/v1.0.2...v1.0.3

For support or questions, please open an issue on GitHub.
