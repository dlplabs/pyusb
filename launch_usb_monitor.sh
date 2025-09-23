#!/bin/bash
# Launcher script for USB Energy Monitor desktop app

if [ "$EUID" -ne 0 ]; then
  echo "This application requires administrator privileges. Relaunching with sudo..."
  exec sudo "$0" "$@"
fi

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
VENV_PY="$SCRIPT_DIR/.venv/bin/python"
APP_PATH="$SCRIPT_DIR/src/usb_desktop_app.py"

exec "$VENV_PY" "$APP_PATH"
