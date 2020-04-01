# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Nic\\PycharmProjects\\OhEight'],
             binaries=[],
           datas=[
           ("C:\\Users\\Nic\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\branca\\*.json","branca"),
           ("C:\\Users\\Nic\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\branca\\templates","templates"),
           ("C:\\Users\\Nic\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\folium\\templates","templates"),
           ("C:\\Users\\Nic\\PycharmProjects\\OhEight\\sit_logo.ico", ".")
           ],
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
          [],
          icon='sit_logo.ico',
          exclude_binaries=True,
          name='main',
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
               upx_exclude=[],
               name='main')
