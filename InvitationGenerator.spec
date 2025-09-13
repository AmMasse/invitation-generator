# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates/', 'templates/'),  # Include template folder
    ],
    hiddenimports=[
        # --- Your direct imports ---
        'customtkinter',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'reportlab.lib.units',
        'reportlab.lib.utils',
        'reportlab.lib.enums',
        'pandas',
        'openpyxl',
        'PIL',
        'PIL.Image',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'threading',
        'json',
        'os',
        'sys',

        # --- Standard library that PyInstaller sometimes misses ---
        'secrets',
        'ctypes',
        'logging',
        'queue',
        'concurrent.futures',
        'multiprocessing',

        # --- Numpy / pandas internals ---
        'numpy',
        'numpy._globals',
        'numpy._distributor_init',
        'numpy.core._methods',
        'numpy.lib.format',
        'numpy.linalg',
        'numpy.fft',
        'numpy.random',
        'numpy.ma',
        'numpy.ctypeslib',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.skiplist',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter'
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='InvitationGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = windowed app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
