"""
自定义异常类定义
用于处理项目中各种特定错误情况
"""


class ZOOTException(Exception):
    """ZOOT代理指挥的基础异常类"""
    def __init__(self, message=None):
        self.message = message
        self.more_info = Exception

        super().__init__(self.message)



class ImageRecognitionError(ZOOTException):
    """图像识别错误"""
    def __init__(self, message="图像识别失败"):
        self.message = message
        super().__init__(self.message)


class ElementNotFoundError(ZOOTException):
    """未找到目标元素"""
    def __init__(self, element_name, message=None):
        self.element_name = element_name
        self.message = message or f"未找到元素: {element_name}\n详细信息: {self.more_info}"

        super().__init__(self.message)


class OperationFailedError(ZOOTException):
    """操作失败"""
    def __init__(self, operation_name, message=None):
        self.operation_name = operation_name
        self.message = message or f"操作失败: {operation_name}"
        super().__init__(self.message)


class GameNotRunningError(ZOOTException):
    """游戏未运行"""
    def __init__(self, message="明日方舟游戏未运行"):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(ZOOTException):
    """配置错误"""
    def __init__(self, config_name, message=None):
        self.config_name = config_name
        self.message = message or f"配置错误: {config_name}"
        super().__init__(self.message)

