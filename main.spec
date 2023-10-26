# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'buttons.py', 'callbacks.py', 'headmen_commands.py', 'headmen_reg_commands.py', 'messages.py', 'middlewares.py', 'personal_chat_commands.py', 'poll.py', 'request.py', 'service.py', 'states.py', 'work_api.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    name='main',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
