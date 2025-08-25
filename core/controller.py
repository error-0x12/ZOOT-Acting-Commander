"""
控制器模块
负责处理与游戏的交互，包括鼠标点击、键盘按键和鼠标拖动等操作
"""
import time
import pyautogui
from .exceptions import OperationFailedError


class Controller:
    """控制器类，提供与游戏交互的各种方法"""

    def __init__(self, delay=0.5):
        """
        初始化控制器

        Args:
            delay (float): 操作之间的延迟时间(秒)
        """
        self.delay = delay
        # 设置pyautogui的失败安全措施
        pyautogui.FAILSAFE = True

    def click(self, x, y, clicks=1, interval=0.2):
        """
        在指定坐标点击鼠标

        Args:
            x (int): 横坐标
            y (int): 纵坐标
            clicks (int): 点击次数
            interval (float): 多次点击之间的间隔时间

        Raises:
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 移动鼠标到指定位置
            pyautogui.moveTo(x, y, duration=0.2)
            # 点击鼠标
            pyautogui.click(clicks=clicks, interval=interval)
            # 添加延迟
            time.sleep(self.delay)
            return True
        except Exception as e:
            raise OperationFailedError("鼠标点击") from e

    def press_key(self, key, presses=1, interval=0.2):
        """
        按下指定的键盘按键

        Args:
            key (str): 要按下的键
            presses (int): 按下次数
            interval (float): 多次按下之间的间隔时间

        Raises:
            OperationFailedError: 按键操作失败时抛出
        """
        try:
            # 按下键
            pyautogui.press(key, presses=presses, interval=interval)
            # 添加延迟
            time.sleep(self.delay)
            return True
        except Exception as e:
            raise OperationFailedError(f"按下键 {key}") from e

    def drag(self, start_x, start_y, end_x, end_y, duration=1.0):
        """
        从起始坐标拖动鼠标到结束坐标

        Args:
            start_x (int): 起始横坐标
            start_y (int): 起始纵坐标
            end_x (int): 结束横坐标
            end_y (int): 结束纵坐标
            duration (float): 拖动持续时间

        Raises:
            OperationFailedError: 拖动操作失败时抛出
        """
        try:
            # 移动鼠标到起始位置
            pyautogui.moveTo(start_x, start_y, duration=0.2)
            # 按下鼠标左键
            pyautogui.mouseDown()
            # 拖动鼠标到结束位置
            pyautogui.moveTo(end_x, end_y, duration=duration)
            # 释放鼠标左键
            pyautogui.mouseUp()
            # 添加延迟
            time.sleep(self.delay)
            return True
        except Exception as e:
            raise OperationFailedError("鼠标拖动") from e

    def scroll(self, clicks, x=None, y=None):
        """
        滚动鼠标滚轮

        Args:
            clicks (int): 滚动的格数，正数向上，负数向下
            x (int): 鼠标位置的横坐标
            y (int): 鼠标位置的纵坐标

        Raises:
            OperationFailedError: 滚动操作失败时抛出
        """
        try:
            if x is not None and y is not None:
                pyautogui.moveTo(x, y, duration=0.2)
            # 滚动鼠标
            pyautogui.scroll(clicks)
            # 添加延迟
            time.sleep(self.delay)
            return True
        except Exception as e:
            raise OperationFailedError("鼠标滚动") from e