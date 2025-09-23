#!/bin/bash
# Remove all build artifacts and reset installer output
rm -rf dist build __pycache__ *.spec
rm -f $HOME/Desktop/usb-energy-monitor.desktop
rm -f dist/usb-energy-monitor.desktop
rm -f dist/usb-energy-monitor.png
