import logging
import time
import os
import sys

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from core.detector import Detector
from core.controller import Controller
from core.exceptions import ElementNotFoundError
from utils.logger import logger
from config.settings import settings

class RecruitModule:
    """
    公开招募模块，处理明日方舟中的公开招募功能
    """
    def __init__(self):
        self.logger = logger
        self.detector = Detector()
        self.controller = Controller()
        self.recruit_button_template = "main_recruit_button.png"
        
    def navigate_to_recruit(self, threshold=0.8):
        """
        导航到公开招募页面
        步骤：点击主界面上的招募按钮
        """
        self.logger.info("开始导航到公开招募页面")
        
        # 查找招募按钮
        self.logger.debug(f"正在查找招募按钮: {self.recruit_button_template}")
        try:
            # 捕获屏幕截图
            screenshot = self.detector.capture_screen()
            
            # 在屏幕截图中查找招募按钮
            button_position = self.detector.find_template(screenshot, self.recruit_button_template, threshold=threshold)
            
            if button_position:
                self.logger.info("找到招募按钮，准备点击")
                # 点击招募按钮（使用中心坐标）
                self.controller.click(button_position[0], button_position[1])
                self.logger.info("已点击招募按钮")
                # 等待页面加载
                time.sleep(2)
                return True
            else:
                # 这里不应该到达，因为find_template在未找到时会抛出异常
                self.logger.error(f"未找到招募按钮: {self.recruit_button_template}")
                return False
        except ElementNotFoundError as e:
            self.logger.error(f"未找到招募按钮: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"导航到公开招募页面失败: {str(e)}")
            return False

    def enter_recruit_slots(self, slot_number=None, target_tags=None, threshold=0.7):
        """
        进入招募位并执行pass操作
        步骤：点击指定招募位(如slot_number=None则依次点击所有招募位)，点击后执行pass
        参数:
            slot_number: 招募位编号(1-4)，None表示所有招募位
        """
        self.logger.info("开始进入招募位")
        
        # 招募位模板图片
        recruit_slot_templates = [
            "recruit_1.png",
            "recruit_2.png",
            "recruit_3.png",
            "recruit_4.png"
        ]
        
        # 确定要处理的招募位
        if slot_number is not None:
            if 1 <= slot_number <= 4:
                self.logger.info(f"处理指定招募位: {slot_number}")
                recruit_slot_templates = [recruit_slot_templates[slot_number - 1]]
            else:
                self.logger.warning(f"无效的招募位编号: {slot_number}，将处理所有招募位")
        else:
            self.logger.info("处理所有招募位")
        
        # 遍历每个招募位
        for slot_template in recruit_slot_templates:
            self.logger.info(f"尝试进入招募位: {slot_template}")
            try:
                # 捕获屏幕截图
                screenshot = self.detector.capture_screen()
                # 保存完整屏幕截图用于调试
                import time
                timestamp = time.strftime('%Y%m%d%H%M%S')
                self.detector.save_image(screenshot, filename=f'recruit_full_screen_{slot_template}_{timestamp}.png')
                
                # 查找招募位
                self.logger.debug(f"正在查找招募位: {slot_template}")
                slot_position = self.detector.find_template(screenshot, slot_template, threshold=threshold)
                
                if slot_position:
                    self.logger.info(f"找到招募位: {slot_template}，准备点击")
                    # 点击招募位
                    self.controller.click(slot_position[0], slot_position[1])
                    self.logger.info(f"已点击招募位: {slot_template}")
                    # 等待页面加载
                    time.sleep(1.5)
                    
                    # 检测招募详情标题是否存在
                    detail_title_template = "recruit_detail_title.png"
                    try:
                        # 捕获屏幕截图
                        screenshot = self.detector.capture_screen()
                        # 查找招募详情标题
                        self.logger.debug(f"正在查找招募详情标题: {detail_title_template}")
                        self.detector.find_template(screenshot, detail_title_template, threshold=threshold)
                        self.logger.info(f"招募详情标题存在，继续处理招募位 {slot_template}")
                        # 执行操作
                        self.logger.info(f"在招募位 {slot_template} 执行操作")
                        self._perform_pass_action(target_tags=target_tags, threshold=threshold)
                    except ElementNotFoundError:
                        self.logger.warning(f"未找到招募详情标题，跳过招募位 {slot_template}")
                else:
                    # 这里不应该到达，因为find_template在未找到时会抛出异常
                    self.logger.warning(f"未找到招募位: {slot_template}，可能已锁定或不存在")
            except ElementNotFoundError as e:
                self.logger.warning(f"未找到招募位: {slot_template}，可能已锁定或不存在: {str(e)}")
            except Exception as e:
                self.logger.error(f"处理招募位 {slot_template} 时出错: {str(e)}")
            
            # 等待一段时间再处理下一个招募位
            time.sleep(1)
        
        self.logger.info("所有招募位处理完成")
        return True
        
    def _perform_pass_action(self, target_tags=None, threshold=0.7):
        """
        执行招募位操作
        流程：点击招募时间按钮 -> 检查标签 -> 点击目标标签或刷新 -> 确认
        参数:
            target_tags: 目标标签列表
        """
        try:
            # 1. 点击招募时间按钮
            self.logger.info("点击招募时间按钮")
            time_btn_template = "recruit_time_btn.png"
            screenshot = self.detector.capture_screen()
            time_btn_position = self.detector.find_template(screenshot, time_btn_template, threshold=threshold)
            self.controller.click(time_btn_position[0], time_btn_position[1])
            time.sleep(1)

            # 2. 检查标签
            if target_tags is None:
                target_tags = ["快速复活","输出"]  # 默认目标标签
            senior_tags = ["资深干员", "高级资深干员"]
            max_refresh_count = 5
            refresh_count = 0
            previous_tags = None

            while refresh_count < max_refresh_count:
                # 捕获屏幕截图
                screenshot = self.detector.capture_screen()

                # 查找recruit_detail_title模板作为基准
                detail_title_template = "recruit_detail_title.png"
                try:
                    self.logger.debug(f"正在查找招募详情标题: {detail_title_template}")
                    title_position = self.detector.find_template(screenshot, detail_title_template, threshold=threshold)
                    x_base = title_position[0]
                    y_base = title_position[1]
                    self.logger.info(f"找到招募详情标题，以其为基准计算识别区域")
                except ElementNotFoundError:
                    self.logger.warning(f"未找到招募详情标题，使用屏幕中心作为备选基准")
                    # 使用屏幕中心作为备选基准
                    screen_center_x = screenshot.shape[1] // 2
                    screen_center_y = screenshot.shape[0] // 2
                    x_base = screen_center_x
                    y_base = screen_center_y

                # 计算识别区域: 以基准点为中心，y向上、下拓展150，x向右拓展150至780像素
                y_top = max(0, y_base - 150)
                y_bottom = min(screenshot.shape[0], y_base + 150)
                x_left = x_base + 150  # 向右拓展150像素作为左边界
                x_right = min(screenshot.shape[1], x_base + 780)  # 向右拓展至780像素作为右边界

                # 裁剪识别区域
                tag_region = (x_left, y_top, x_right, y_bottom)
                tag_image = self.detector.crop_image(screenshot, tag_region)
                # 保存裁剪后的标签区域截图用于调试
                if settings.SAVE_SCREENSHOTS:
                    self.detector.save_image(tag_image, filename=f'recruit_tag_region_{refresh_count}.png')

                # 识别文字并获取坐标
                # 识别文字并获取坐标
                recognized_text_with_coords = self.detector.recognize_text(tag_image, return_coordinates=True)
                # 如果未识别到文字，保存截图用于调试
                if not recognized_text_with_coords:
                    if settings.SAVE_SCREENSHOTS:
                        self.detector.save_image(tag_image, filename=f'recruit_text_recognition_failed_{refresh_count}.png')
                self.logger.info(f"识别到招募标签: {[item['text'] for item in recognized_text_with_coords]}")

                # 检查是否有高级资深干员标签
                for item in recognized_text_with_coords:
                    for senior_tag in senior_tags:
                        if senior_tag in item['text']:
                            self.logger.warning(f"发现{senior_tag}，请人工接管")
                            return False

                # 检查是否有目标标签
                found_target = False
                target_tag_position = None
                
                for item in recognized_text_with_coords:
                    for target_tag in target_tags:
                        if target_tag in item['text']:
                            self.logger.info(f"找到目标标签: {target_tag}")
                            
                            # 获取标签在识别区域中的中心坐标
                            tag_center_x, tag_center_y = item['center']
                            
                            # 计算标签在整个屏幕上的绝对位置
                            abs_x = x_left + tag_center_x
                            abs_y = y_top + tag_center_y
                            self.logger.info(f"定位到标签位置: ({abs_x}, {abs_y})")
                            # 点击标签
                            self.controller.click(abs_x, abs_y)
                            self.logger.info(f"已点击目标标签: {target_tag}")
                            time.sleep(0.5)
                            found_target = True
                            break
                    if found_target:
                        break

                if found_target:
                    # 3. 点击右侧按钮
                    self.logger.info("点击右侧按钮")
                    right_btn_template = "recruit_right_btn.png"
                    screenshot = self.detector.capture_screen()
                    right_btn_position = self.detector.find_template(screenshot, right_btn_template, threshold=threshold)
                    self.controller.click(right_btn_position[0], right_btn_position[1])
                    time.sleep(1)
                    return True
                else:
                    # 如果没有找到目标标签，点击第一个识别到的标签
                    if recognized_text_with_coords:
                        item = recognized_text_with_coords[0]
                        self.logger.warning(f"未找到目标标签: {target_tags}，点击第一个识别到的标签: {item['text']}")
                        
                        # 获取标签在识别区域中的中心坐标
                        tag_center_x, tag_center_y = item['center']
                        
                        # 计算标签在整个屏幕上的绝对位置
                        abs_x = x_left + tag_center_x
                        abs_y = y_top + tag_center_y
                        self.logger.info(f"定位到标签位置: ({abs_x}, {abs_y})")
                        
                        # 执行点击
                        self.logger.info(f"点击标签位置: ({abs_x}, {abs_y})")
                        self.controller.click(abs_x, abs_y)
                        time.sleep(0.5)
                        
                        # 点击右侧按钮
                        self.logger.info("点击右侧按钮")
                        right_btn_template = "recruit_right_btn.png"
                        screenshot = self.detector.capture_screen()
                        right_btn_position = self.detector.find_template(screenshot, right_btn_template, threshold=threshold)
                        self.controller.click(right_btn_position[0], right_btn_position[1])
                        time.sleep(1)
                        return True
                    else:
                        # 检查是否与上一次识别结果相同
                        current_tags = [item['text'] for item in recognized_text_with_coords] if recognized_text_with_coords else []
                        if current_tags == previous_tags:
                            self.logger.warning("标签没有变化，刷新失败")
                            break

                        previous_tags = current_tags
                        refresh_count += 1

                        # 4. 刷新标签
                        self.logger.info(f"刷新标签 (第{refresh_count}次)")
                        refresh_btn_template = "recruit_refresh_tags.png"
                        screenshot = self.detector.capture_screen()
                        refresh_btn_position = self.detector.find_template(screenshot, refresh_btn_template, threshold=threshold)
                        self.controller.click(refresh_btn_position[0], refresh_btn_position[1])
                        time.sleep(1)

                        # 点击确认按钮
                        true_btn_template = "true_btn.png"
                        screenshot = self.detector.capture_screen()
                        true_btn_position = self.detector.find_template(screenshot, true_btn_template, threshold=threshold)
                        self.controller.click(true_btn_position[0], true_btn_position[1])
                        time.sleep(1.5)

            # 达到最大刷新次数仍未找到目标标签
            self.logger.warning(f"达到最大刷新次数({max_refresh_count})，未找到目标标签")
            # 点击右侧按钮
            self.logger.info("点击右侧按钮")
            right_btn_template = "recruit_right_btn.png"
            screenshot = self.detector.capture_screen()
            right_btn_position = self.detector.find_template(screenshot, right_btn_template, threshold=0.7)
            self.controller.click(right_btn_position[0], right_btn_position[1])
            time.sleep(1)
            return True

        except ElementNotFoundError as e:
            self.logger.error(f"未找到元素: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"执行招募位操作失败: {str(e)}")
            return False

# 测试代码recruit
if __name__ == "__main__":
    recruit = RecruitModule()
    # 先导航到公开招募页面
    if recruit.navigate_to_recruit():
        # 然后进入招募位并执行pass操作
        recruit.enter_recruit_slots()