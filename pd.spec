
# pd.spec

block_cipher = None

a = Analysis(
    ['pd/__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('pd/assets/*', 'pd/assets'), 
        ('pd/core/*', 'pd/core'),
        ('pd/launcher/*, 'pd/launcher'),
        ('pd/platform/*', 'pd/platform'),
        ('pd/startup/*', 'pd/startup'),
        ('pd/ui/*', 'pd/ui')
        ],
    hiddenimports=['numpy._core._multiarray_umath', 'numpy._core.multiarray'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    exclude_binaries=False,
    name='PD UI Mng',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)