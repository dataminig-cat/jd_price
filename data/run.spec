# -*- mode: python -*-

block_cipher = None


a = Analysis(['run.py'],
              pathex=['E:\\数据挖掘项目\\爬虫数据喵\\jd_price','C:\\Users\\33171\\AppData\\Local\\Programs\\Python\\Python37',],
             binaries=[],
             datas=[(r'C:\Users\33171\AppData\Local\Programs\Python\Python37\Lib\site-packages\win10toast\data\python.ico','.'),
             (r'E:\\数据挖掘项目\\爬虫数据喵\\jd_price\setting.json','.')],
             hiddenimports=['pymysql','numpy.core._dtype_ctypes','crawler.spiders','crawler.pipeline'],
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
          [],
          exclude_binaries=True,
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='run')
