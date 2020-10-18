# -*- mode: python ; coding: utf-8 -*-
from sys import platform

block_cipher = None

icon = None
if platform.startswith("darwin"):
    icon = 'images/icon.icns'

a = Analysis(['speed_tester.py'],
             binaries=[],
             datas=[('images/*','amda_sciqlop_speed_tester/images')],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)


if platform.startswith("darwin"):
    exe = EXE(pyz,
              a.scripts,
              [],
              exclude_binaries=True,
              name='speed_tester',
              debug=True,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              upx_exclude=[],
              icon=icon,
              runtime_tmpdir=None,
              console=False )

    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='AMDA_SciQLop_Speed_tester')

    app = BUNDLE(coll,
      name='AMDA_SciQLop_Speed_tester.app',
      icon=icon,
      bundle_identifier=None,
      info_plist={
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True
      })

else:
    exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='speed_tester',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
