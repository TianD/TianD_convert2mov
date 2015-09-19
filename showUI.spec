# -*- mode: python -*-
a = Analysis(['showUI.py'],
             pathex=['E:\\Scripts\\Eclipse\\TianD_convert2mov'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='showUI.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
