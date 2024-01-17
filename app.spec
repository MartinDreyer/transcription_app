# -*- mode: python ; coding: utf-8 -*-
import sys
import os

# Define the function to find the 'whisper' path
def find_whisper_path():
    python_executable = sys.executable
    python_base_path = os.path.dirname(os.path.dirname(python_executable))
    whisper_path = os.path.join(python_base_path, 'Lib', 'site-packages', 'whisper')
    return whisper_path
def find_tqdm_path():
    python_executable = sys.executable
    python_base_path = os.path.dirname(os.path.dirname(python_executable))
    tqdm_path = os.path.join(python_base_path, 'Lib', 'site-packages', 'tqdm')
    return tqdm_path

# Use the function to get the 'whisper' path
whisper_path = find_whisper_path()
tqdm_path = find_tqdm_path()


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[(whisper_path, './whisper'),('ffmpeg.exe','.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='T-TEX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico"

)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='T-TEX',
)
