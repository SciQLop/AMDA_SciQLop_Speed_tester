# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['speed_tester.py'],
             binaries=[],
             datas=[('images/*','amda_sciqlop_speed_tester/images')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='speed_tester',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
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
  icon='images/icon.icns',
  bundle_identifier=None,
  info_plist={
    'CFBundleVersion': '1.0.0',
    'CFBundleShortVersionString': '1.0.0',
    'NSHighResolutionCapable': True
  })
