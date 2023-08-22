# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import os
import sys

# Define the function to find the 'whisper' path
def find_whisper_path():
    python_executable = sys.executable
    python_base_path = os.path.dirname(os.path.dirname(python_executable))
    whisper_path = os.path.join(python_base_path, 'lib', 'python3.11', 'site-packages', 'whisper')
    return whisper_path

# Use the function to get the 'whisper' path
whisper_path = find_whisper_path()

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[('ffmpeg','.')],
    datas=[(whisper_path, './whisper'),('ffmpeg','.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='T-Tex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico"
)
