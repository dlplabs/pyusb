#!/bin/bash
# Permanently block a USB device by vendor and product ID using a udev rule
# Usage: sudo ./block_usb.sh <vendor_id> <product_id>

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo)"
  exit 1
fi

if [ $# -ne 2 ]; then
  echo "Usage: sudo $0 <vendor_id> <product_id>"
  echo "Example: sudo $0 1234 5678"
  exit 1
fi

VENDOR_ID="$1"
PRODUCT_ID="$2"
RULE_FILE="/etc/udev/rules.d/99-usb-block.rules"

# Add the rule
LINE="SUBSYSTEM==\"usb\", ATTR{idVendor}==\"$VENDOR_ID\", ATTR{idProduct}==\"$PRODUCT_ID\", ATTR{authorized}=\"0\""

grep -q "$LINE" "$RULE_FILE" 2>/dev/null || echo "$LINE" >> "$RULE_FILE"

echo "Rule added to $RULE_FILE:"
echo "$LINE"

echo "Reloading udev rules..."
sudo udevadm control --reload
sudo udevadm trigger

echo "Device with vendor $VENDOR_ID and product $PRODUCT_ID is now blocked. Replug the device to apply."
