#!/bin/bash
# Automated .deb packaging for USB Energy Monitor
set -e

# Install prerequisites automatically
echo "Installing prerequisites..."
sudo apt-get update
sudo apt-get install -y dpkg-dev fakeroot python3 python3-pyqt5

# Build executable and assets
bash install_usb_monitor.sh

PKGDIR="usb-energy-monitor_"
BINNAME="usb-energy-monitor"
DESKTOPFILE="usb-energy-monitor.desktop"
ICONFILE="usb-energy-monitor.png"

# Clean previous package
rm -rf "$PKGDIR" usb-energy-monitor_*.deb

# Create directory structure
mkdir -p "$PKGDIR/DEBIAN"
mkdir -p "$PKGDIR/usr/local/bin"
mkdir -p "$PKGDIR/usr/share/applications"
mkdir -p "$PKGDIR/usr/share/icons/hicolor/128x128/apps"

# Control file
cat > "$PKGDIR/DEBIAN/control" <<EOF
Package: usb-energy-monitor
Version: 1.0
Section: utils
Priority: optional
Architecture: amd64
Depends: python3, python3-pyqt5
Maintainer: Your Name <your@email.com>
Description: Monitor and control USB ports and energy usage
EOF

# Copy binary, desktop file, icon
cp dist/$BINNAME "$PKGDIR/usr/local/bin/$BINNAME"
cp dist/$DESKTOPFILE "$PKGDIR/usr/share/applications/$DESKTOPFILE"
cp dist/$ICONFILE "$PKGDIR/usr/share/icons/hicolor/128x128/apps/$ICONFILE"

# Update desktop file for menu integration
sed -i "s|Icon=.*|Icon=usb-energy-monitor|" "$PKGDIR/usr/share/applications/$DESKTOPFILE"

# Build .deb
fakeroot dpkg-deb --build "$PKGDIR"

# Instructions
cat <<EOM

Package built: $PKGDIR.deb
Install with:
  sudo dpkg -i $PKGDIR.deb

If icon does not appear, run:
  sudo update-desktop-database
  sudo gtk-update-icon-cache /usr/share/icons/hicolor
EOM
