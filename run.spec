# -*- mode: python ; coding: utf-8 -*-
import os

# 使用当前工作目录作为项目根目录
current_dir = os.getcwd()

# 添加数据文件
datas = []

# 添加图标资源
icon_dir = os.path.join(current_dir, 'gui', 'icon')
if os.path.exists(icon_dir):
    for file in os.listdir(icon_dir):
        if file.endswith(('.png', '.ico')):
            datas.append((os.path.join(icon_dir, file), os.path.join('gui', 'icon')))

# 添加模板文件
templates_dir = os.path.join(current_dir, 'templates')
if os.path.exists(templates_dir):
    for file in os.listdir(templates_dir):
        if file.endswith('.png'):
            datas.append((os.path.join(templates_dir, file), 'templates'))

# 添加配置文件
config_dir = os.path.join(current_dir, 'config')
if os.path.exists(config_dir):
    for file in os.listdir(config_dir):
        if file.endswith('.py') and file != '__init__.py':
            datas.append((os.path.join(config_dir, file), 'config'))

a = Analysis(
    ['run.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'core', 'core.controller', 'core.detector', 'core.exceptions',
        'modules', 'modules.base_management', 'modules.combat', 
        'modules.mission', 'modules.recruit', 'modules.task_management',
        'utils', 'utils.logger',
        'config.settings',
        'scipy._cyutility',
        'scipy.linalg._cythonized_array_utils'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ZOOT Acting Commander',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
