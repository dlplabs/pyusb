# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/usb_desktop_app.py'],
    pathex=[],
    binaries=[('/usr/lib/x86_64-linux-gnu/libusb-1.0.so.0', '.')],
    datas=[],
    hiddenimports=['usb.backend.libusb1', 'usb.core', 'usb.util', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='usb-energy-monitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
