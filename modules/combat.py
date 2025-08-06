"""
作战模块
负责处理与明日方舟作战相关的操作，包括自动代理剿灭作战等功能
"""
import os
import time
import cv2
from core import Controller, Detector
from core.exceptions import ElementNotFoundError, OperationFailedError, ImageRecognitionError
from utils import logger

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 设置模板目录路径
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')


class CombatModule:
    """作战模块类，提供与作战相关的操作方法"""

    def __init__(self, controller=None, detector=None):
        """
        初始化作战模块类

        Args:
            controller (Controller): 控制器实例
            detector (Detector): 检测器实例
        """
        self.controller = controller or Controller()
        self.detector = detector or Detector()
        # 模板图片路径
        self.mission_btn_template = os.path.join(TEMPLATES_DIR, 'main_menu_mission_btn.png')
        self.back_btn_template = os.path.join(TEMPLATES_DIR, 'back_btn.png')
        self.normal_affairs_btn_template = os.path.join(TEMPLATES_DIR, 'normal_affairs_btn.png')
        self.exterminated_icon_template = os.path.join(TEMPLATES_DIR, 'exterminated_icon.png')
        self.longmen_01_template = os.path.join(TEMPLATES_DIR, 'longmen_01.png')
        self.longmen_02_template = os.path.join(TEMPLATES_DIR, 'longmen_02.png')
        self.longmen_03_template = os.path.join(TEMPLATES_DIR, 'longmen_03.png')
        self.current_commission_btn_template = os.path.join(TEMPLATES_DIR, 'current_commission_btn.png')
        # 代理指挥相关模板
        self.acting_commander_off_template = os.path.join(TEMPLATES_DIR, 'acting_commander_off.png')
        self.acting_commander_on_template = os.path.join(TEMPLATES_DIR, 'acting_commander_on.png')
        # 剩余理智模板
        self.remaining_sanity_template = os.path.join(TEMPLATES_DIR, 'remaining_sanity.png')
        # 作战流程相关模板
        self.operation_start_btn_template = os.path.join(TEMPLATES_DIR, 'OPERATION_START_btn.png')
        self.mission_start_btn_template = os.path.join(TEMPLATES_DIR, 'mission_start_btn.png')
        self.combat_briefing_template = os.path.join(TEMPLATES_DIR, 'combat_briefing.png')
        self.mission_results_template = os.path.join(TEMPLATES_DIR, 'MISSION_RESULTS.png')
        self.top_bar_template = os.path.join(TEMPLATES_DIR, 'top_bar.png')
        self.home_btn_template = os.path.join(TEMPLATES_DIR, 'home_btn.png')
        # 理智识别区域坐标（根据游戏界面调整）
        # x：templates\remaining_sanity.png向右偏移255至390，y：与templates\remaining_sanity.png相同
        self.remaining_sanity_area = (0, 0, 135, 40)  # 初始值，实际使用时会基于模板位置计算
        self.consuming_sanity_area = (850, 640, 950, 670)  # 再次调整消耗理智区域坐标 (x1, y1, x2, y2)

    def navigate_to_mission(self, threshold=0.8):
        """
        从主菜单导航到作战界面

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到作战按钮时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找作战按钮
            mission_btn_pos = self.detector.find_template(screenshot, self.mission_btn_template, threshold=threshold)

            if mission_btn_pos:
                # 点击作战按钮
                x, y, _, _ = mission_btn_pos
                self.controller.click(x, y)
                logger.info("成功导航到作战界面")
                return True
            else:
                raise ElementNotFoundError('main_menu_mission_btn.png', "未找到作战按钮")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到作战界面") from e

    def navigate_back_from_mission(self):
        """
        从作战界面返回到主菜单

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
                logger.info("成功从作战界面返回主菜单")
                return True
            else:
                raise ElementNotFoundError('back_btn.png', "未找到返回按钮")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("从作战界面返回主菜单") from e

    def navigate_to_normal_affairs(self, threshold=0.8):
        """
        从作战界面导航到常态事务

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到常态事务按钮时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找常态事务按钮
            normal_affairs_btn_pos = self.detector.find_template(screenshot, self.normal_affairs_btn_template, threshold=threshold)

            if normal_affairs_btn_pos:
                # 点击常态事务按钮
                x, y, _, _ = normal_affairs_btn_pos
                self.controller.click(x, y)
                logger.info("成功导航到常态事务")
                return True
            else:
                raise ElementNotFoundError('normal_affairs_btn.png', "未找到常态事务按钮")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到常态事务") from e

    def navigate_to_eliminate(self, threshold=0.8):
        """
        从常态事务界面导航到剿灭作战

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到剿灭作战图标时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找剿灭作战图标
            exterminated_icon_pos = self.detector.find_template(screenshot, self.exterminated_icon_template, threshold=threshold)

            if exterminated_icon_pos:
                # 计算向下偏移430像素后的点击位置
                x, y, _, _ = exterminated_icon_pos
                click_x = x
                click_y = y + 430

                # 点击计算后的位置
                self.controller.click(click_x, click_y)
                logger.info("成功导航到剿灭作战")
                return True
            else:
                raise ElementNotFoundError('exterminated_icon.png', "未找到剿灭作战图标")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到剿灭作战") from e

    def navigate_to_longmen(self, threshold=0.8):
        """
        导航到龙门外环

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找longmen_01模板
            longmen_01_pos = self.detector.find_template(screenshot, self.longmen_01_template, threshold=threshold)

            if longmen_01_pos:
                # 点击longmen_01
                x1, y1, _, _ = longmen_01_pos
                self.controller.click(x1, y1)
                logger.info("成功点击longmen_01")
                time.sleep(2)
            else:
                raise ElementNotFoundError('longmen_01.png', "未找到longmen_01模板")

            # 重新捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找longmen_02模板
            longmen_02_pos = self.detector.find_template(screenshot, self.longmen_02_template, threshold=threshold)

            if longmen_02_pos:
                # 记录longmen_02的坐标
                x2, y2, _, _ = longmen_02_pos
                self.longmen_02_position = (x2, y2)
                logger.info(f"已记录longmen_02坐标: ({x2}, {y2})")
                
                # 点击longmen_02向右偏移425像素的位置
                click_x = x2 + 425
                click_y = y2
                self.controller.click(click_x, click_y)
                logger.info("成功点击longmen_02向右偏移425像素的位置")
                time.sleep(2)
            else:
                raise ElementNotFoundError('longmen_02.png', "未找到longmen_02模板")

            # 使用之前记录的longmen_02坐标
            if hasattr(self, 'longmen_02_position'):
                # 点击longmen_02向上偏移100像素的位置
                x3, y3 = self.longmen_02_position
                click_x = x3
                click_y = y3 - 100
                self.controller.click(click_x, click_y)
                logger.info("成功点击longmen_02向上偏移100像素的位置")
                logger.info("成功导航到龙门外环")
                # 清除记录的坐标
                delattr(self, 'longmen_02_position')
                return True
            else:
                raise ElementNotFoundError('longmen_02.png', "未找到longmen_02模板或未记录坐标")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到龙门外环") from e

    def navigate_to_longmen_city(self, threshold=0.8):
        """
        导航到龙门市区

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找longmen_01模板
            longmen_01_pos = self.detector.find_template(screenshot, self.longmen_01_template, threshold=threshold)

            if longmen_01_pos:
                # 点击longmen_01
                x1, y1, _, _ = longmen_01_pos
                self.controller.click(x1, y1)
                logger.info("成功点击longmen_01")
                time.sleep(2)
            else:
                raise ElementNotFoundError('longmen_01.png', "未找到longmen_01模板")

            # 重新捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找longmen_03模板
            longmen_03_pos = self.detector.find_template(screenshot, self.longmen_03_template, threshold=threshold)

            if longmen_03_pos:
                # 记录longmen_03的坐标
                x2, y2, _, _ = longmen_03_pos
                self.longmen_03_position = (x2, y2)
                logger.info(f"已记录longmen_03坐标: ({x2}, {y2})")
                
                # 点击longmen_03向右偏移425像素的位置
                click_x = x2 + 425
                click_y = y2
                self.controller.click(click_x, click_y)
                logger.info("成功点击longmen_03向右偏移425像素的位置")
                time.sleep(2)
            else:
                raise ElementNotFoundError('longmen_03.png', "未找到longmen_03模板")

            # 使用之前记录的longmen_03坐标
            if hasattr(self, 'longmen_03_position'):
                # 点击longmen_03向上偏移100像素的位置
                x3, y3 = self.longmen_03_position
                click_x = x3
                click_y = y3 - 100
                self.controller.click(click_x, click_y)
                logger.info("成功点击longmen_03向上偏移100像素的位置")
                logger.info("成功导航到龙门市区")
                # 清除记录的坐标
                delattr(self, 'longmen_03_position')
                return True
            else:
                raise ElementNotFoundError('longmen_03.png', "未找到longmen_03模板或未记录坐标")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到龙门市区") from e

    def navigate_to_current_commission(self, threshold=0.8):
        """
        导航到当期委托地点

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找longmen_01模板
            longmen_01_pos = self.detector.find_template(screenshot, self.longmen_01_template, threshold=threshold)

            if longmen_01_pos:
                # 点击longmen_01
                x1, y1, _, _ = longmen_01_pos
                self.controller.click(x1, y1)
                logger.info("成功点击longmen_01")
                time.sleep(2)
            else:
                raise ElementNotFoundError('longmen_01.png', "未找到longmen_01模板")

            # 重新捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找当期委托按钮
            current_commission_btn_pos = self.detector.find_template(screenshot, self.current_commission_btn_template, threshold=threshold)

            if current_commission_btn_pos:
                # 点击当期委托按钮
                x, y, _, _ = current_commission_btn_pos
                self.controller.click(x, y)
                logger.info("成功点击当期委托按钮")
                logger.info("成功导航到当期委托地点")
                return True
            else:
                raise ElementNotFoundError('current_commission_btn.png', "未找到当期委托按钮")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到当期委托地点") from e

    def navigate_to_longmen_city(self, threshold=0.8):
        """
        导航到龙门市区

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 导航成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找longmen_01模板
            longmen_01_pos = self.detector.find_template(screenshot, self.longmen_01_template, threshold=threshold)

            if longmen_01_pos:
                # 点击longmen_01
                x1, y1, _, _ = longmen_01_pos
                self.controller.click(x1, y1)
                logger.info("成功点击longmen_01")
                time.sleep(2)
            else:
                raise ElementNotFoundError('longmen_01.png', "未找到longmen_01模板")

            # 重新捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 在截图中查找longmen_03模板
            longmen_03_pos = self.detector.find_template(screenshot, self.longmen_03_template, threshold=threshold)

            if longmen_03_pos:
                # 记录longmen_03的坐标
                x2, y2, _, _ = longmen_03_pos
                self.longmen_03_position = (x2, y2)
                logger.info(f"已记录longmen_03坐标: ({x2}, {y2})")
                
                # 点击longmen_03向右偏移425像素的位置
                click_x = x2 + 425
                click_y = y2
                self.controller.click(click_x, click_y)
                logger.info("成功点击longmen_03向右偏移425像素的位置")
                time.sleep(2)
            else:
                raise ElementNotFoundError('longmen_03.png', "未找到longmen_03模板")

            # 使用之前记录的longmen_03坐标
            if hasattr(self, 'longmen_03_position'):
                # 点击longmen_03向上偏移100像素的位置
                x3, y3 = self.longmen_03_position
                click_x = x3
                click_y = y3 - 100
                self.controller.click(click_x, click_y)
                logger.info("成功点击longmen_03向上偏移100像素的位置")
                logger.info("成功导航到龙门市区")
                # 清除记录的坐标
                delattr(self, 'longmen_03_position')
                return True
            else:
                raise ElementNotFoundError('longmen_03.png', "未找到longmen_03模板或未记录坐标")
        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("导航到龙门市区") from e

    def recognize_remaining_sanity(self):
        """
        识别右上角剩余理智数量

        Returns:
            int: 剩余理智数量

        Raises:
            OperationFailedError: 识别失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 查找剩余理智模板位置
            try:
                x, y, width, height = self.detector.find_template(screenshot, 'remaining_sanity.png', threshold=0.8)
                logger.info(f"找到剩余理智模板，位置: ({x}, {y})，大小: ({width}, {height})")
                # 基于模板位置计算剩余理智区域坐标
                # x：templates\remaining_sanity.png向右偏移255至400像素
                # y：y+模板文件高度/2 至 y-模板文件高度/3（确保起始值小于结束值）
                y_start = min(y + int(height/2), y - int(height/3))
                y_end = max(y + int(height/2), y - int(height/3))
                self.remaining_sanity_area = (x + 255, y_start, x + 400, y_end)
                logger.info(f"更新剩余理智区域坐标: {self.remaining_sanity_area}")
            except ElementNotFoundError:
                logger.warning("未找到剩余理智模板，使用默认区域: {self.remaining_sanity_area}")

            # 裁剪出剩余理智区域
            remaining_sanity_img = self.detector.crop_image(screenshot, self.remaining_sanity_area)

            # 保存裁剪后的图像用于调试
            import cv2
            debug_img_path = os.path.join('logs', 'remaining_sanity_debug.png')
            cv2.imwrite(debug_img_path, remaining_sanity_img)
            logger.info(f"已保存剩余理智调试图像到: {debug_img_path}")

            # 使用OCR识别剩余理智数量
            # 尝试使用不同的OCR配置
            remaining_sanity_text = self.detector.recognize_text(remaining_sanity_img, lang='eng', config='--psm 7 --oem 3')
            logger.info(f"识别到的原始文本: '{remaining_sanity_text}'")

            # 提取数字 (只取'/'前的部分)
            if '/' in remaining_sanity_text:
                # 分割字符串，取'/'前面的部分
                part_before_slash = remaining_sanity_text.split('/')[0]
                digits = ''.join(filter(str.isdigit, part_before_slash))
            else:
                digits = ''.join(filter(str.isdigit, remaining_sanity_text))

            if digits:
                remaining_sanity = int(digits)
                logger.info(f"识别到剩余理智数量: {remaining_sanity}")
                return remaining_sanity
            else:
                # 尝试使用中文+英文识别
                remaining_sanity_text = self.detector.recognize_text(remaining_sanity_img, lang='chi_sim+eng', config='--psm 7 --oem 3')
                logger.info(f"尝试中英文识别的原始文本: '{remaining_sanity_text}'")
                
                # 提取数字 (只取'/'前的部分)
                if '/' in remaining_sanity_text:
                    part_before_slash = remaining_sanity_text.split('/')[0]
                    digits = ''.join(filter(str.isdigit, part_before_slash))
                else:
                    digits = ''.join(filter(str.isdigit, remaining_sanity_text))
                     
                if digits:
                    remaining_sanity = int(digits)
                    logger.info(f"识别到剩余理智数量: {remaining_sanity}")
                    return remaining_sanity
                else:
                    logger.error("未能从识别文本中提取数字")
                    raise OperationFailedError("识别剩余理智数量")
        except Exception as e:
            raise OperationFailedError("识别剩余理智数量") from e

    def recognize_consuming_sanity(self):
        """
        获取消耗理智数量（根据用户要求固定为25）

        Returns:
            int: 消耗理智数量（固定为25）
        """
        logger.info("消耗理智数量固定为25")
        return 25

    def calculate_executable_times(self):
        """
        计算可执行次数

        Returns:
            int: 可执行次数

        Raises:
            OperationFailedError: 计算失败时抛出
        """
        try:
            remaining_sanity = self.recognize_remaining_sanity()
            consuming_sanity = self.recognize_consuming_sanity()

            if consuming_sanity == 0:
                raise OperationFailedError("消耗理智数量为0，无法计算可执行次数")

            executable_times = remaining_sanity // consuming_sanity
            logger.info(f"计算可执行次数: {executable_times} (剩余理智: {remaining_sanity}, 消耗理智: {consuming_sanity})")
            return executable_times
        except Exception as e:
            raise OperationFailedError("计算可执行次数") from e

    def check_and_enable_acting_commander(self, threshold=0.6):
        """
        检查并启用代理指挥

        Args:
            threshold (float): 模板匹配阈值，默认为0.6（降低阈值以提高匹配成功率）

        Returns:
            bool: 启用成功返回True，已启用返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()

            # 检查代理指挥是否已启用
            try:
                acting_commander_on_pos = self.detector.find_template(screenshot, self.acting_commander_on_template, threshold=threshold)
                if acting_commander_on_pos:
                    logger.info("代理指挥已经启用")
                    return True
            except ElementNotFoundError as e:
                logger.warning(f"未找到代理指挥已启用模板: {str(e)}，尝试检查未启用状态")

            # 检查代理指挥是否未启用
            try:
                acting_commander_off_pos = self.detector.find_template(screenshot, self.acting_commander_off_template, threshold=threshold)
                if acting_commander_off_pos:
                    # 点击启用代理指挥
                    x, y, _, _ = acting_commander_off_pos
                    self.controller.click(x, y)
                    logger.info("成功启用代理指挥")
                    time.sleep(1)
                    return True
            except ElementNotFoundError as e:
                logger.warning(f"未找到代理指挥未启用模板: {str(e)}")

            # 如果两个模板都未找到，尝试直接点击可能的位置
            logger.info("尝试直接点击可能的代理指挥位置")
            # 假设代理指挥按钮位于屏幕右下角区域（根据游戏界面调整坐标）
            self.controller.click(1700, 950)
            time.sleep(1)
            return True

        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("检查并启用代理指挥") from e

    def auto_eliminate(self, threshold=0.8):
        """
        自动进行已解锁的代理剿灭作战

        Args:
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 操作成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 首先导航到作战界面
            if not self.navigate_to_mission(threshold=threshold):
                raise OperationFailedError("无法导航到作战界面")

            # 等待作战界面加载
            time.sleep(2)

            # 这里将实现查找和点击剿灭作战的逻辑
            # 注意：由于缺少具体的模板图片和界面信息，以下代码为框架
            # 实际实现时需要添加相应的模板路径和点击逻辑

            logger.info("自动代理剿灭作战功能尚未完全实现")
            return False

        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("执行自动代理剿灭作战") from e


    def auto_combat_flow(self, cycles=1, threshold=0.8):
        """
        执行自动化作战流程(包含导航和检测)

        Args:
            cycles (int): 作战循环次数，默认为1
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 操作成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 首先导航到作战界面
            if not self.navigate_to_mission(threshold=threshold):
                raise OperationFailedError("无法导航到作战界面")

            # 等待作战界面加载
            time.sleep(2)

            # 启用代理指挥
            self.check_and_enable_acting_commander(threshold=threshold)

            # 调用仅作战流程
            return self.combat_only_flow(cycles, threshold)

        except ElementNotFoundError:
            raise
        except OperationFailedError:
            raise
        except Exception as e:
            raise OperationFailedError("执行自动作战流程失败") from e

    def combat_only_flow(self, cycles=1, threshold=0.8):
        """
        仅执行作战流程(从点击'开始行动'字样后开始)

        Args:
            cycles (int): 作战循环次数，默认为1
            threshold (float): 模板匹配阈值，默认为0.8

        Returns:
            bool: 操作成功返回True，失败返回False

        Raises:
            ElementNotFoundError: 未找到相关元素时抛出
            OperationFailedError: 点击操作失败时抛出
        """
        try:
            # 循环执行作战
            for cycle in range(cycles):
                logger.info(f"开始第 {cycle+1}/{cycles} 轮作战")

                # 1. 点击"开始行动"按钮模板
                logger.info("步骤1: 尝试点击开始行动按钮模板")
                # 检查模板文件是否存在
                if not os.path.exists(self.mission_start_btn_template):
                    raise FileNotFoundError(f"开始行动按钮模板不存在: {self.mission_start_btn_template}")
                
                screenshot = self.detector.capture_screen()
                start_btn_result = self.detector.find_template(screenshot, self.mission_start_btn_template, threshold=threshold)
                x, y, _, _ = start_btn_result  # 只提取x和y坐标，忽略宽度和高度
                self.controller.click(x, y)
                logger.info(f"成功点击开始行动按钮位置: ({x}, {y})")
                time.sleep(1)

                # 2. 点击开始行动按钮模板 OPERATION_START_btn.png
                logger.info("步骤2: 尝试点击开始行动按钮")
                # 检查模板文件是否存在
                if not os.path.exists(self.operation_start_btn_template):
                    raise FileNotFoundError(f"开始行动按钮模板不存在: {self.operation_start_btn_template}")
                
                screenshot = self.detector.capture_screen()
                start_btn_pos = self.detector.find_template(screenshot, self.operation_start_btn_template, threshold=threshold)
                if start_btn_pos:
                    x, y, _, _ = start_btn_pos
                    self.controller.click(x, y)
                    logger.info(f"成功点击开始行动按钮位置: ({x}, {y})")
                    time.sleep(2)
                else:
                    raise ElementNotFoundError('OPERATION_START_btn.png', "未找到开始行动按钮")

                # 3. 等待并点击作战简报模板
                logger.info("等待作战简报模板出现")
                briefing_found = False
                # 为作战简报模板设置较低的阈值，提高识别成功率
                briefing_threshold = threshold
                # 检查模板文件是否存在
                if not os.path.exists(self.combat_briefing_template):
                    raise FileNotFoundError(f"作战简报模板不存在: {self.combat_briefing_template}")
                if not os.path.exists(self.mission_results_template):
                    raise FileNotFoundError(f"行动结束模板不存在: {self.mission_results_template}")
                for _ in range(600):  # 最多等待30分钟（1800秒）                    
                    screenshot = self.detector.capture_screen()
                    try:
                        briefing_pos = self.detector.find_template(screenshot, self.combat_briefing_template, threshold=briefing_threshold)
                    except:
                        briefing_pos = None
                    if briefing_pos:
                        x, y, _, _ = briefing_pos
                        self.controller.click(x, y)
                        logger.info(f"成功点击作战简报模板位置: ({x}, {y})")
                        time.sleep(1)
                        break
                    time.sleep(3)
                    logger.info(f"未找到作战简报，当前匹配阈值: {briefing_threshold}")


                # 4. 等待并点击"行动结束"字样
                time.sleep(5)
                # 检查模板文件是否存在
                
                    
                screenshot = self.detector.capture_screen()
                logger.info(f"正在查找行动结束")
                try:
                    end_pos = self.detector.find_template(screenshot, self.mission_results_template, threshold=briefing_threshold)
                except:
                    end_pos = None
                if end_pos:
                        x, y, _, _ = end_pos
                        self.controller.click(x, y)
                        logger.info(f"成功点击行动结束位置: ({x}, {y})")
                        time.sleep(5)
                else:
                    logger.debug(f"未找到行动结束，当前匹配阈值: {briefing_threshold}")



                logger.info(f"第 {cycle+1}/{cycles} 轮作战完成")
            time.sleep(5)
            
            # 5. 返回首页
            logger.info("准备返回首页")

            # 点击top_bar.png
            screenshot = self.detector.capture_screen()
            top_bar_pos = self.detector.find_template(screenshot, self.top_bar_template, threshold=threshold)
            if top_bar_pos:
                x, y, _, _ = top_bar_pos
                self.controller.click(x, y)
                logger.info("成功点击顶部栏")
                time.sleep(1)
            else:
                logger.error("未找到顶部栏")

            # 点击home_btn.png
            screenshot = self.detector.capture_screen()
            home_btn_pos = self.detector.find_template(screenshot, self.home_btn_template, threshold=threshold)
            if home_btn_pos:
                x, y, _, _ = home_btn_pos
                self.controller.click(x, y)
                logger.info("成功点击首页按钮，返回首页")
                time.sleep(1)
            else:
                logger.error("未找到首页按钮")

            logger.info("自动化剿灭作战流程已完成")
            return True

        except ElementNotFoundError:
            logger.error("未找到相关元素")
        except OperationFailedError:
            logger.error("点击操作失败")
        except Exception as e:
            logger.error("执行自动化剿灭作战流程失败", exc_info=True)