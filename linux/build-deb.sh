#!/bin/bash
# Build .deb package for Route Planner
# ====================================

set -e

APP_NAME="route-planner"
VERSION="1.0.2"
ARCH="all"
MAINTAINER="Route Planner Team <support@routeplanner.com>"
DESCRIPTION="Advanced delivery route optimization tool with TSP algorithms"

BUILD_DIR="build/debian"
PACKAGE_DIR="$BUILD_DIR/${APP_NAME}_${VERSION}_${ARCH}"

# Clean up previous builds
rm -rf "$BUILD_DIR"
mkdir -p "$PACKAGE_DIR"

echo "📦 Building .deb package for Route Planner v$VERSION"

# Create directory structure
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR/opt/route-planner"
mkdir -p "$PACKAGE_DIR/usr/local/bin"
mkdir -p "$PACKAGE_DIR/usr/share/applications"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor"

# Copy application files
echo "📋 Copying application files..."
cp -r . "$PACKAGE_DIR/opt/route-planner/"
rm -rf "$PACKAGE_DIR/opt/route-planner/build"
rm -rf "$PACKAGE_DIR/opt/route-planner/.git"

# Create launcher script
cat > "$PACKAGE_DIR/usr/local/bin/route-planner" << 'EOF'
#!/bin/bash
cd /opt/route-planner
if [ ! -d "venv" ]; then
    echo "Setting up Route Planner for first run..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
fi
source venv/bin/activate
python3 main_app.py "$@"
EOF
chmod +x "$PACKAGE_DIR/usr/local/bin/route-planner"

# Create desktop entry
cat > "$PACKAGE_DIR/usr/share/applications/route-planner.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Route Planner
GenericName=Delivery Route Optimizer
Comment=Optimize delivery routes using advanced algorithms
Exec=/usr/local/bin/route-planner
Icon=route-planner
Terminal=false
Categories=Office;Utility;Geography;
Keywords=route;delivery;optimization;map;navigation;TSP;
StartupNotify=true
StartupWMClass=Route Planner
EOF

# Create control file
cat > "$PACKAGE_DIR/DEBIAN/control" << EOF
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Depends: python3 (>= 3.8), python3-pip, python3-venv, python3-dev, python3-tk, libqt5-dev
Maintainer: $MAINTAINER
Description: $DESCRIPTION
 Route Planner is a sophisticated PyQt5-based desktop application for optimizing
 delivery routes in any urban area. It combines advanced graph algorithms with
 an intuitive user interface to solve the Traveling Salesman Problem (TSP).
 .
 Key Features:
  - Interactive GUI with embedded Folium map visualization
  - Real-time road network data integration via OpenStreetMap
  - Dual algorithm support: Held-Karp (optimal) and Christofides (approximation)
  - Comprehensive onboarding system with guided tutorials
  - Offline operation support with intelligent caching
  - Multithreaded processing to maintain UI responsiveness
EOF

# Create postinst script
cat > "$PACKAGE_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Create virtual environment and install dependencies
cd /opt/route-planner
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Create application icon
if [ -f "linux/create_icon.py" ]; then
    source venv/bin/activate
    python3 linux/create_icon.py
    deactivate
    
    # Install icons
    if [ -d "linux/icons" ]; then
        cp -r linux/icons/hicolor/* /usr/share/icons/hicolor/
    fi
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor
fi

echo "Route Planner installed successfully!"
echo "You can find it in your Applications menu or run 'route-planner' from terminal."
EOF
chmod +x "$PACKAGE_DIR/DEBIAN/postinst"

# Create prerm script
cat > "$PACKAGE_DIR/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e

# Remove virtual environment
rm -rf /opt/route-planner/venv

# Remove icons
find /usr/share/icons -name "route-planner.*" -delete 2>/dev/null || true

echo "Route Planner removed successfully!"
EOF
chmod +x "$PACKAGE_DIR/DEBIAN/prerm"

# Build the package
echo "🔨 Building package..."
dpkg-deb --build "$PACKAGE_DIR"

# Move package to current directory
mv "$PACKAGE_DIR.deb" "./route-planner_${VERSION}_${ARCH}.deb"

echo "✅ Package built successfully: route-planner_${VERSION}_${ARCH}.deb"
echo
echo "To install:"
echo "  sudo dpkg -i route-planner_${VERSION}_${ARCH}.deb"
echo "  sudo apt-get install -f  # Fix dependencies if needed"
echo
echo "To uninstall:"
echo "  sudo apt remove route-planner"
