import logging
import os
import sys
import time
import cv2
import numpy as np

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from core.detector import Detector
from core.controller import Controller
from utils.logger import logger

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_tag_coordinate_click():
    """
    测试标签坐标点击功能
    1. 捕获屏幕截图
    2. 模拟招募详情页面
    3. 测试标签识别和坐标点击
    """
    logger.info("开始测试标签坐标点击功能")
    detector = Detector()
    controller = Controller()

    try:
        # 1. 捕获屏幕截图
        logger.info("捕获屏幕截图")
        screenshot = detector.capture_screen()

        # 2. 查找招募详情标题作为基准点
        logger.info("查找招募详情标题")
        detail_title_template = "recruit_detail_title.png"
        try:
            title_position = detector.find_template(screenshot, detail_title_template, threshold=0.7)
            logger.info(f"找到招募详情标题，位置: {title_position}")
        except Exception as e:
            logger.error(f"未找到招募详情标题: {str(e)}")
            # 为了测试继续，假设一个位置
            title_position = (300, 200, 100, 50)
            logger.warning(f"假设招募详情标题位置: {title_position}")

        # 3. 计算识别区域
        x_base = title_position[0]
        y_base = title_position[1]
        y_top = max(0, y_base - 100)
        y_bottom = min(screenshot.shape[0], y_base + 100)
        x_left = x_base + 150  # 向右拓展150像素作为左边界
        x_right = min(screenshot.shape[1], x_base + 780)  # 向右拓展至780像素作为右边界
        logger.info(f"计算识别区域: x_left={x_left}, y_top={y_top}, x_right={x_right}, y_bottom={y_bottom}")

        # 4. 裁剪识别区域
        tag_region = (x_left, y_top, x_right, y_bottom)
        tag_image = detector.crop_image(screenshot, tag_region)
        logger.info(f"裁剪标签识别区域: {tag_region}")

        # 5. 识别文字并获取坐标
        logger.info("识别标签文字和坐标")
        recognized_text_with_coords = detector.recognize_text(tag_image, return_coordinates=True)
        logger.info(f"识别到招募标签: {[item['text'] for item in recognized_text_with_coords]}")

        # 6. 显示所有识别到的标签及其坐标
        logger.info("所有识别到的标签及其坐标:")
        for i, item in enumerate(recognized_text_with_coords):
            logger.info(f"标签 {i+1}: {item['text']}, 边界框: {item['bbox']}, 中心坐标: {item['center']}, 置信度: {item['confidence']}")

        # 7. 尝试点击标签
        target_tags = ["重装干员", "新手", "医疗干员"]  # 增加医疗干员作为目标
        found_target = False
        target_index = 0  # 默认点击第一个识别到的标签

        # 优先寻找目标标签
        for item in recognized_text_with_coords:
            for target_tag in target_tags:
                if target_tag in item['text']:
                    logger.info(f"找到目标标签: {target_tag}")
                    
                    # 获取标签在识别区域中的中心坐标
                    tag_center_x, tag_center_y = item['center']
                    
                    # 计算标签在整个屏幕上的绝对位置
                    abs_x = x_left + tag_center_x
                    abs_y = y_top + tag_center_y
                    logger.info(f"定位到标签位置: ({abs_x}, {abs_y})")
                    
                    # 执行点击
                    logger.info(f"点击标签位置: ({abs_x}, {abs_y})")
                    controller.click(abs_x, abs_y)
                    found_target = True
                    break
            if found_target:
                break

        # 如果没有找到目标标签，点击第一个识别到的标签
        if not found_target and recognized_text_with_coords:
            item = recognized_text_with_coords[target_index]
            logger.warning(f"未找到目标标签: {target_tags}，点击第一个识别到的标签: {item['text']}")
            
            # 获取标签在识别区域中的中心坐标
            tag_center_x, tag_center_y = item['center']
            
            # 计算标签在整个屏幕上的绝对位置
            abs_x = x_left + tag_center_x
            abs_y = y_top + tag_center_y
            logger.info(f"定位到标签位置: ({abs_x}, {abs_y})")
            
            # 执行点击
            logger.info(f"点击标签位置: ({abs_x}, {abs_y})")
            controller.click(abs_x, abs_y)
            found_target = True

        if found_target:
            logger.info("标签坐标点击测试成功")
        else:
            logger.warning("未识别到任何标签，测试失败")

    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}")
        return False

    logger.info("标签坐标点击功能测试完成")
    return True

if __name__ == "__main__":
    test_tag_coordinate_click()