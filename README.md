# PRTS Acting Commander

PRTS Acting Commander 是一个为明日方舟设计的自动化工具，灵感来源于开源项目 Better Genshin Impact。该工具基于 Python 开发，旨在为玩家提供便捷的游戏辅助功能，减轻重复操作的负担。

## 功能特点

- **自动战斗**：支持在指定关卡进行自动战斗
- **基建管理**：自动收取基建资源、处理订单
- **招募系统**：智能识别招募标签，筛选高稀有度干员
- **任务管理**：自动完成日常、周常任务
- **可视化界面**：提供简洁直观的图形用户界面
- **配置灵活**：支持自定义各种功能参数
- **日志系统**：详细记录工具运行状态和操作

## 项目结构

```
PRTS Acting Commander/
├── config/           # 配置文件
├── core/             # 核心功能模块
│   ├── controller.py # 控制器
│   ├── detector.py   # 图像识别模块
│   └── exceptions.py # 自定义异常
├── gui/              # 图形界面
├── logs/             # 日志文件
├── modules/          # 功能模块
│   ├── base_management.py # 基建管理
│   ├── combat.py     # 战斗系统
│   ├── mission.py    # 任务系统
│   ├── recruit.py    # 招募系统
│   └── task_management.py # 任务管理
├── templates/        # 图像模板
├── utils/            # 工具函数
├── run.py            # 程序入口
└── test_combat_flow.py # 测试文件
```

## 安装说明

1. 确保已安装 Python 3.8 或更高版本
2. 克隆或下载此项目到本地
3. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```
   *注：如果没有 requirements.txt 文件，请手动安装以下依赖：opencv-python, pyautogui, pillow, pyyaml, logging, tkinter*

## 使用方法

1. 运行程序：
   ```bash
   python run.py
   ```
2. 在图形界面中配置各项功能参数
3. 选择需要执行的功能模块
4. 点击开始按钮，程序将自动执行相应操作

## 配置说明

配置文件位于 `config/settings.py`，可以根据需要修改以下参数：

- `SCREEN_RESOLUTION`: 屏幕分辨率设置
- `DETECTION_THRESHOLD`: 图像识别阈值
- `AUTO_COMBAT_SETTINGS`: 自动战斗相关设置
- `BASE_MANAGEMENT_SETTINGS`: 基建管理相关设置
- `RECRUIT_SETTINGS`: 招募系统相关设置

## 注意事项

1. 本工具仅用于学习和研究目的，请勿用于商业用途
2. 使用前请确保游戏窗口处于前台且未被遮挡
3. 不同屏幕分辨率可能需要调整图像识别参数
4. 使用过程中如遇到问题，请查看日志文件获取详细信息
5. 本工具可能会随着游戏更新而失效，需要及时更新适配

## 许可证

[MIT License](LICENSE)

## 联系我们

如果您有任何问题或建议，请通过以下方式联系我们：
- GitHub Issues: [提交问题](https://github.com/error-0x12/PRTS-Acting-Commander/issues)
- 邮箱: 3919086204@qq.com

© 2025 PRTS Acting Commander 开发者