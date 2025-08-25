"""
ZOOT代理指挥核心模块
提供游戏控制和图像识别的基础功能
"""

# 导出异常类
from .exceptions import (
    ZOOTException,
    ImageRecognitionError,
    ElementNotFoundError,
    OperationFailedError,
    GameNotRunningError,
    ConfigurationError
)

# 导出控制器和检测器类
from .controller import Controller
from .detector import Detector

# 定义公共API
__all__ = [
    # 异常类
    'ZOOTException',
    'ImageRecognitionError',
    'ElementNotFoundError',
    'OperationFailedError',
    'GameNotRunningError',
    'ConfigurationError',
    # 核心类
    'Controller',
    'Detector'
]