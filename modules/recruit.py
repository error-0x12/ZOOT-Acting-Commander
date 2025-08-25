import logging
import time
import os
import sys
import traceback

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
        # 招募标签模板列表（位于templates\recruit_tag目录下）
        self.tag_templates = [
            "recruit_tag\\新手.png",
            "recruit_tag\\术士干员.png",
            "recruit_tag\\治疗.png",
            "recruit_tag\\狙击干员.png",
            "recruit_tag\\生存.png",
            "recruit_tag\\群攻.png",
            "recruit_tag\\费用回复.png",
            "recruit_tag\\资深干员.png",
            "recruit_tag\\辅助干员.png",
            "recruit_tag\\输出.png",
            "recruit_tag\\近卫干员.png",
            "recruit_tag\\近战位.png",
            "recruit_tag\\远程位.png",
            "recruit_tag\\重装干员.png",
            "recruit_tag\\高级资深干员.png",
            "recruit_tag\\快速复活.png",
            "recruit_tag\\支援.png",
            "recruit_tag\\位移.png",
            "recruit_tag\\减速.png",
            "recruit_tag\\停顿.png",
            "recruit_tag\\控场.png",
            "recruit_tag\\削弱.png",
            "recruit_tag\\召唤.png",
            "recruit_tag\\爆发.png",
            "recruit_tag\\防护.png",
            "recruit_tag\\先锋.png",
            "recruit_tag\\医疗.png"
            # 已添加所有templates/recruit_tag目录下的标签模板
        ]
        
    def navigate_to_recruit(self, threshold=0.8):
        """
        导航到公开招募页面
        步骤：点击主界面上的招募按钮
        """
        self.logger.info("开始导航到公开招募页面")
        time.sleep(1)

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
                if settings.SAVE_SCREENSHOTS:
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

                # 使用全屏进行检测
                tag_image = screenshot

                # 保存全屏截图用于调试
                if settings.SAVE_SCREENSHOTS:
                    self.detector.save_image(tag_image, filename=f'recruit_tag_region_{refresh_count}.png')

                # 使用模板匹配识别标签（只比对用户选择的tag的模板）
                recognized_tags_with_coords = []
                
                # 构建用户选择的标签对应的模板列表
                target_templates = []
                if target_tags:
                    for tag_template in self.tag_templates:
                        tag_name = os.path.splitext(tag_template)[0]
                        if any(target_tag in tag_name for target_tag in target_tags):
                            target_templates.append(tag_template)
                
                # 如果没有匹配的模板，使用默认行为（遍历所有模板）
                if not target_templates:
                    target_templates = self.tag_templates
                    self.logger.warning("未找到与目标标签匹配的模板，将使用所有模板进行匹配")
                
                # 只遍历用户选择的标签模板
                for tag_template in target_templates:
                    try:
                        # 在标签区域中查找模板
                            self.logger.info(f"正在匹配模板: {tag_template}，阈值: 0.7")
                            tag_position = self.detector.find_template(tag_image, tag_template, threshold=0.7)
                            
                            if tag_position:
                                # 获取标签名称（去掉文件扩展名）
                                tag_name = os.path.splitext(tag_template)[0]
                                # 计算标签中心坐标
                                x, y, w, h = tag_position
                                center_x = x + w // 2
                                center_y = y + h // 2
                                # 添加到识别结果列表
                                recognized_tags_with_coords.append({
                                    'text': tag_name,
                                    'center': (center_x, center_y),
                                    'confidence': 1.0  # 模板匹配默认为100%置信度
                                })
                                self.logger.info(f"找到标签: {tag_name}，位置: ({center_x}, {center_y})")
                    except ElementNotFoundError as e:
                        # 未找到当前模板，继续查找下一个
                        self.logger.warning(f"未找到模板: {tag_template}，错误信息: {str(e)}")
                        continue
                self.logger.info(f"识别到招募标签: {[item['text'] for item in recognized_tags_with_coords]}")
                # 如果未识别到标签，保存截图用于调试
                if not recognized_tags_with_coords:
                    self.logger.warning(f"未识别到任何标签，刷新次数: {refresh_count}")
                    if settings.SAVE_SCREENSHOTS:
                        self.detector.save_image(tag_image, filename=f'recruit_template_matching_failed_{refresh_count}.png')

                # 检查是否有高级资深干员标签
                self.logger.info("开始检查高级资深干员标签")
                senior_tag_templates = ["recruit_tag\\资深干员.png", "recruit_tag\\高级资深干员.png"]
                for senior_template in senior_tag_templates:
                    try:
                        template_name = os.path.basename(senior_template)
                        self.logger.info(f"正在检查高级资深干员标签: {template_name}")
                        if self.detector.find_template(tag_image, senior_template, threshold=0.7):
                            senior_tag = os.path.splitext(template_name)[0]
                            self.logger.warning(f"发现{senior_tag}，请人工接管")
                            return False
                        else:
                            self.logger.debug(f"未找到高级资深干员标签: {template_name}")
                    except ElementNotFoundError as e:
                        self.logger.warning(f"未找到高级资深干员标签文件: {senior_template}. 错误: {str(e)}")
                        continue

                # 检查是否有目标标签
                found_target = False
                target_tag_position = None
                
                for item in recognized_tags_with_coords:
                    for target_tag in target_tags:
                        if target_tag == item['text']:
                            self.logger.info(f"找到目标标签: {target_tag}")
                            
                            # 获取标签在识别区域中的中心坐标
                            tag_center_x, tag_center_y = item['center']
                            
                            # 在全屏模式下，标签中心坐标已经是绝对位置
                            abs_x = tag_center_x
                            abs_y = tag_center_y
                            self.logger.info(f"定位到标签 '{target_tag}' 位置: ({abs_x}, {abs_y})")
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
                    if recognized_tags_with_coords:
                        item = recognized_tags_with_coords[0]
                        self.logger.warning(f"未找到目标标签: {target_tags}，点击第一个识别到的标签: {item['text']}")
                        
                        # 获取标签在识别区域中的中心坐标
                        tag_center_x, tag_center_y = item['center']
                        
                        # 在全屏模式下，标签中心坐标已经是绝对位置
                        abs_x = tag_center_x
                        abs_y = tag_center_y
                        self.logger.info(f"定位到标签位置: ({abs_x}, {abs_y})")
                        
                        # 执行点击
                        self.logger.info(f"点击非目标标签 '{item['text']}' 位置: ({abs_x}, {abs_y})")
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
                        current_tags = [item['text'] for item in recognized_tags_with_coords] if recognized_tags_with_coords else []
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
            self.logger.error(f"错误详情: {traceback.format_exc()}")
            return False

# 测试代码recruit
if __name__ == "__main__":
    recruit = RecruitModule()
    # 先导航到公开招募页面
    if recruit.navigate_to_recruit():
        # 然后进入招募位并执行pass操作
        recruit.enter_recruit_slots()