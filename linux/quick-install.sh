#!/bin/bash
# One-Line Route Planner Installer
# Usage: curl -sSL https://raw.githubusercontent.com/yammanhammad/Route_Planner/master/linux/quick-install.sh | bash

set -e

REPO_URL="https://github.com/yammanhammad/Route_Planner"
TEMP_DIR="/tmp/route-planner-install"

echo "🚚 Route Planner Quick Installer"
echo "================================="

# Clean up function
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Check if git is available
if command -v git &> /dev/null; then
    echo "📥 Downloading via git..."
    rm -rf "$TEMP_DIR"
    git clone "$REPO_URL.git" "$TEMP_DIR"
else
    echo "📥 Downloading via wget..."
    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"
    wget -q -O master.zip "$REPO_URL/archive/master.zip"
    unzip -q master.zip
    mv Route_Planner-master/* .
    rm -f master.zip
fi

cd "$TEMP_DIR"

# Check if user wants system-wide or user installation
echo
echo "Choose installation type:"
echo "1) User installation (recommended, no sudo required)"
echo "2) System-wide installation (requires sudo)"
echo
read -p "Enter choice [1]: " choice
choice=${choice:-1}

case $choice in
    1)
        echo "🏠 Starting user installation..."
        bash linux/install-user.sh
        ;;
    2)
        echo "🌐 Starting system-wide installation..."
        sudo bash linux/install-linux.sh
        ;;
    *)
        echo "❌ Invalid choice. Using user installation..."
        bash linux/install-user.sh
        ;;
esac

echo
echo "🎉 Installation complete!"
echo "The Route Planner should now appear in your Applications menu."
