# -*- mode: python ; coding: utf-8 -*-


analysis_results = Analysis(
    ['src\\app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
python_archive = PYZ(analysis_results.pure)

executable_config = EXE(
    python_archive,
    analysis_results.scripts,
    analysis_results.binaries,
    analysis_results.datas,
    [],
    name='vim_dungeon',
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
)
