# USB Energy Monitor .deb Packaging Instructions

## Prerequisites
- Install `dpkg-dev` and `fakeroot`:
  ```bash
  sudo apt-get install dpkg-dev fakeroot
  ```

## Steps
1. Build the PyInstaller executable using `install_usb_monitor.sh`.
2. Create the following directory structure:
   ```
   usb-energy-monitor_
   ├── DEBIAN/
   │   └── control
   └── usr/
       └── local/
           └── bin/
               └── usb-energy-monitor
   └── usr/
       └── share/
           └── applications/
               └── usb-energy-monitor.desktop
   ```
3. Example `control` file (edit as needed):
   ```
   Package: usb-energy-monitor
   Version: 1.0
   Section: utils
   Priority: optional
   Architecture: amd64
   Depends: python3, python3-pyqt5
   Maintainer: Your Name <your@email.com>
   Description: Monitor and control USB ports and energy usage
   ```
4. Copy the PyInstaller binary to `usr/local/bin/usb-energy-monitor`.
5. Copy the desktop file to `usr/share/applications/usb-energy-monitor.desktop`.
6. Build the .deb package:
   ```bash
   dpkg-deb --build usb-energy-monitor_
   ```
7. Install with:
   ```bash
   sudo dpkg -i usb-energy-monitor_.deb
   ```

---
For more advanced packaging, consider using `debuild` or `checkinstall`.
