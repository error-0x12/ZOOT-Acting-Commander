"""
基建管理模块
负责处理与明日方舟基建相关的操作，包括从主菜单导航到基建等功能
"""
import os
import time
from core import Controller, Detector
from core.exceptions import ElementNotFoundError, OperationFailedError
from utils import logger

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 设置模板目录路径
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')


class BaseManagementModule:
    """基建管理类，提供与基建相关的操作方法"""

    def __init__(self, controller=None, detector=None):
        """
        初始化基建管理类

        Args:
            controller (Controller): 控制器实例
            detector (Detector): 检测器实例
        """
        self.controller = controller or Controller()
        self.detector = detector or Detector()
        # 模板图片路径
        self.base_btn_template = os.path.join(TEMPLATES_DIR, 'main_menu_base_btn.png')
        self.back_btn_template = os.path.join(TEMPLATES_DIR, 'back_btn.png')
        # 通知相关模板图片路径
        self.notification_btn_template = os.path.join(TEMPLATES_DIR, 'base_notification.png')
        self.notification_title_template = os.path.join(TEMPLATES_DIR, 'base_notification_title.png')
        # 退出基建相关模板图片路径
        self.top_bar_template = os.path.join(TEMPLATES_DIR, 'top_bar.png')
        self.home_btn_template = os.path.join(TEMPLATES_DIR, 'home_btn.png')
        self.true_btn_template = os.path.join(TEMPLATES_DIR, 'true_btn.png')

    def navigate_to_base(self, threshold=0.8):
        """
        从主菜单导航到基建

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到基建按钮时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找基建按钮
            base_btn_pos = self.detector.find_template(screenshot, self.base_btn_template, threshold=threshold)

            if base_btn_pos:
                # 点击基建按钮
                x, y, _, _ = base_btn_pos
                self.controller.click(x, y)
                logger.info("成功导航到基建")
                return True
            else:
                raise ElementNotFoundError('main_menu_base_btn.png', "未找到基建按钮")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到基建") from e

    def navigate_back_from_base(self):
        """
        从基建返回到主菜单

        Returns:
            bool: 返回成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到返回按钮时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找返回按钮
            back_btn_pos = self.detector.find_template(screenshot, self.back_btn_template)

            if back_btn_pos:
                # 点击返回按钮
                x, y, _, _ = back_btn_pos
                self.controller.click(x, y)
                logger.info("成功从基建返回主菜单")
                return True
            else:
                raise ElementNotFoundError('back_btn.png', "未找到返回按钮")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("从基建返回主菜单") from e

    def exit_from_base(self, threshold=0.8):
        """
        退出基建，返回到主界面

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 操作成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找顶栏
            top_bar_pos = self.detector.find_template(screenshot, self.top_bar_template, threshold=threshold)

            if top_bar_pos:
                # 点击顶栏
                x, y, _, _ = top_bar_pos
                self.controller.click(x, y)
                logger.info("成功点击顶栏")
                
                # 等待菜单加载
                time.sleep(1)
                
                # 重新捕获屏幕截图
                screenshot = self.detector.capture_screen()
                
                # 在截图中查找首页按钮
                home_btn_pos = self.detector.find_template(screenshot, self.home_btn_template, threshold=threshold)
                
                if home_btn_pos:
                    # 点击首页按钮
                    x, y, _, _ = home_btn_pos
                    self.controller.click(x, y)
                    logger.info("成功点击首页按钮")
                    
                    # 等待确认对话框加载
                    time.sleep(1)
                    
                    # 重新捕获屏幕截图
                    screenshot = self.detector.capture_screen()
                    
                    # 在截图中查找确认按钮
                    true_btn_pos = self.detector.find_template(screenshot, self.true_btn_template, threshold=threshold)
                    
                    if true_btn_pos:
                        # 点击确认按钮
                        x, y, _, _ = true_btn_pos
                        self.controller.click(x, y)
                        logger.info("成功点击确认按钮")
                        return True
                    else:
                        raise ElementNotFoundError('true_btn.png', "未找到确认按钮")
                else:
                    raise ElementNotFoundError('home_btn.png', "未找到首页按钮")
            else:
                raise ElementNotFoundError('top_bar.png', "未找到顶栏")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("退出基建") from e

    def complete_tasks(self, threshold=0.8):
        """
        完成基建中的事项

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 操作成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找通知按钮
            notification_btn_pos = self.detector.find_template(screenshot, self.notification_btn_template, threshold=threshold)

            if notification_btn_pos:
                # 点击通知按钮
                x, y, _, _ = notification_btn_pos
                self.controller.click(x, y)
                logger.info("成功点击通知按钮")
                
                # 等待通知面板加载
                time.sleep(1)
                
                # 重新捕获屏幕截图
                screenshot = self.detector.capture_screen()
                
                # 在截图中查找通知标题
                notification_title_pos = self.detector.find_template(screenshot, self.notification_title_template, threshold=threshold)
                
                if notification_title_pos:
                    # 计算点击位置（标题右面约75像素）
                    title_x, title_y, title_width, _ = notification_title_pos
                    click_x = title_x + title_width + 75
                    click_y = title_y
                    
                    # 点击5次
                    for i in range(5):
                        self.controller.click(click_x, click_y)
                        logger.info(f"成功点击位置 ({click_x}, {click_y})，第 {i+1} 次")
                        time.sleep(0.5)  # 间隔0.5秒
                        
                    # 计算关闭按钮位置（标题向上偏移100像素）
                    close_x = title_x
                    close_y = title_y - 100
                    
                    # 点击关闭按钮
                    self.controller.click(close_x, close_y)
                    logger.info(f"成功点击关闭位置 ({close_x}, {close_y})，退出待办事项")
                    return True
                else:
                    raise ElementNotFoundError('base_notification_title.png', "未找到通知标题")
            else:
                raise ElementNotFoundError('base_notification.png', "未找到通知按钮")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("完成事项") from e