#!/usr/bin/env python3
"""
Release preparation script.
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from version import get_version, update_package_version

def update_version(new_version):
    """Update version in route_planner/__init__.py"""
    init_file = Path("route_planner") / "__init__.py"
    
    if not init_file.exists():
        print(f"❌ Error: {init_file} not found")
        return False
    
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update version
    updated_content = re.sub(
        r'__version__ = [\'"][^\'"]*[\'"]',
        f'__version__ = "{new_version}"',
        content
    )
    
    if content == updated_content:
        print(f"✅ Version already set to {new_version}")
        return True
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Updated version to {new_version} in {init_file}")
    return True

def update_nsis_fallback_version(new_version):
    """Update fallback version in scripts/installer.nsi"""
    nsis_file = Path("scripts") / "installer.nsi"
    
    if not nsis_file.exists():
        print(f"❌ Error: {nsis_file} not found")
        return False
    
    with open(nsis_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update fallback version in NSIS installer
    updated_content = re.sub(
        r'!define APP_VERSION "[^"]*"  ; Fallback version - should be updated by scripts/prepare_release\.py',
        f'!define APP_VERSION "{new_version}"  ; Fallback version - should be updated by scripts/prepare_release.py',
        content
    )
    
    if content == updated_content:
        print(f"✅ NSIS fallback version already set to {new_version}")
        return True
    
    with open(nsis_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Updated NSIS fallback version to {new_version} in {nsis_file}")
    return True

def add_changelog_entry(version):
    """Add a new entry to CHANGELOG.md"""
    changelog_file = Path("CHANGELOG.md")
    
    if not changelog_file.exists():
        print(f"❌ Error: {changelog_file} not found")
        return False
    
    with open(changelog_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find where to insert the new version
    insert_index = None
    for i, line in enumerate(lines):
        if line.startswith("## ["):
            insert_index = i
            break
    
    if insert_index is None:
        print("❌ Error: Could not find existing version entries in CHANGELOG.md")
        return False
    
    # Check if version already exists
    if f"## [{version}]" in lines[insert_index]:
        print(f"✅ Version {version} already exists in CHANGELOG.md")
        return True
    
    # Create new entry
    today = datetime.now().strftime("%Y-%m-%d")
    new_entry = [
        f"## [{version}] - {today}\n",
        "\n",
        "### Added\n",
        "- \n",
        "\n",
        "### Changed\n",
        "- \n",
        "\n",
        "### Fixed\n",
        "- \n",
        "\n",
    ]
    
    # Insert new entry
    lines[insert_index:insert_index] = new_entry
    
    with open(changelog_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ Added new entry for version {version} to CHANGELOG.md")
    return True

def add_release_notes_entry(version):
    """Add a new entry to docs/RELEASE_NOTES.md"""
    release_notes_file = Path("docs") / "RELEASE_NOTES.md"
    
    if not release_notes_file.exists():
        print(f"❌ Error: {release_notes_file} not found")
        return False
    
    with open(release_notes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if version already exists
    if f"## Route Planner v{version} (Latest)" in content:
        print(f"✅ Version {version} already exists in RELEASE_NOTES.md")
        return True
    
    # Find where to insert (after the Actions note)
    insertion_point = "*All Windows executables and cross-platform packages are automatically built and published using GitHub Actions.*\n\n"
    
    if insertion_point not in content:
        print("❌ Error: Could not find insertion point in RELEASE_NOTES.md")
        return False
    
    # Create new entry
    today_month_year = datetime.now().strftime("%B %Y")
    new_entry = f"""## Route Planner v{version} (Latest)

**Release Date:** {today_month_year}

### 🚀 New Features
- 

### 🔧 Improvements
- 

### 🐛 Bug Fixes
- 

"""
    
    # Update "Latest" marker
    content = content.replace(" (Latest)", "")
    content = content.replace(insertion_point, insertion_point + new_entry)
    
    with open(release_notes_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Added new entry for version {version} to RELEASE_NOTES.md")
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/prepare_release.py <version>")
        print("Example: python scripts/prepare_release.py X.Y.Z (semantic versioning)")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("❌ Error: Version must be in format X.Y.Z (e.g., 1.2.0)")
        sys.exit(1)
    
    print(f"🚀 Preparing release for version {new_version}")
    print("=" * 50)
    
    success = True
    success &= update_version(new_version)
    success &= update_nsis_fallback_version(new_version)
    success &= add_changelog_entry(new_version)
    success &= add_release_notes_entry(new_version)
    
    if success:
        print("=" * 50)
        print(f"✅ Successfully prepared release for version {new_version}")
        print("Next steps:")
        print("1. Edit CHANGELOG.md and docs/RELEASE_NOTES.md to add details")
        print("2. Commit changes: git add . && git commit -m 'Prepare release v{new_version}'")
        print("3. Create tag: git tag v{new_version}")
        print("4. Push: git push && git push --tags")
    else:
        print("❌ Some operations failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
