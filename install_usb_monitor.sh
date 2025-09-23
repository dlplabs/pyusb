#!/bin/bash
set -e

# Ensure venv exists
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install pyinstaller PyQt5 pyusb

# Build executable
pyinstaller --onefile --windowed src/usb_desktop_app.py --name usb-energy-monitor
mkdir -p dist
mv dist/usb-energy-monitor dist/

# Copy icon
ICON_SRC="src/dashboard/frontend/public/usb-energy-monitor.png"
ICON_DST="dist/usb-energy-monitor.png"
if [ -f "$ICON_SRC" ]; then
  cp "$ICON_SRC" "$ICON_DST"
fi

# Create desktop shortcut
cat > dist/usb-energy-monitor.desktop <<EOF
[Desktop Entry]
Name=USB Energy Monitor
Comment=Monitor and control USB ports and energy usage
Exec=sudo dist/usb-energy-monitor
Icon=dist/usb-energy-monitor.png
Terminal=false
Type=Application
Categories=Utility;System;
EOF

chmod +x dist/usb-energy-monitor
chmod +x launch_usb_monitor.sh

# Optionally install shortcut to user's desktop
if [ -d "$HOME/Desktop" ]; then
  cp dist/usb-energy-monitor.desktop "$HOME/Desktop/"
fi
