#!/usr/bin/env python3
"""
测试文字识别模块
"""
import os
import cv2
import numpy as np
from core.detector import Detector
from core.exceptions import ImageRecognitionError, ElementNotFoundError
from utils.logger import logger


def test_text_recognition():
    """
    测试文字识别功能
    """
    try:
        # 初始化检测器
        detector = Detector()
        logger.info("检测器初始化成功")

        # 测试1: 使用本地图像文件
        test_image_path = os.path.join(os.path.dirname(__file__), 'logs', '9d79a969b497169a7dc8f735c3cb3da.png')
        if os.path.exists(test_image_path):
            # 加载图像
            image = cv2.imread(test_image_path)
            if image is not None:
                logger.info(f"成功加载测试图像: {test_image_path}")
                
                # 尝试不同的图像预处理方法和配置参数
                preprocess_methods = [
                    ('原始图像', image),
                    
                ]
                
                config_params = [
                    '--psm 7',  # 假设单行文本
                    '--psm 7 --oem 3',  # 单行文本 + 新OCR引擎
                    '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz之的了我是不人在有来他这上们个时大子说生国年动进”“',  # 限定字符集
                    '--psm 6 --oem 3',  # 块文本 + 新OCR引擎
                    '--psm 11 --oem 3'  # 稀疏文本 + 新OCR引擎
                ]
                
                for method_name, processed_image in preprocess_methods:
                    # 保存预处理后的图像用于调试
                    debug_image_path = os.path.join(os.path.dirname(__file__), 'logs', f'text_recog_{method_name}.png')
                    if len(processed_image.shape) == 2:
                        cv2.imwrite(debug_image_path, processed_image)
                    else:
                        cv2.imwrite(debug_image_path, processed_image)
                    logger.info(f"已保存预处理图像到: {debug_image_path}")
                    
                    for i, config in enumerate(config_params):
                        # 识别文字
                        try:
                            if len(processed_image.shape) == 2:
                                # 对于灰度图像，转换为BGR格式
                                processed_image_bgr = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
                                text = detector.recognize_text(processed_image_bgr, config=config)
                            else:
                                text = detector.recognize_text(processed_image, config=config)
                            logger.info(f"{method_name} (配置 {i+1}) 文字识别结果: {text}")
                            print(f"测试1 - {method_name} (配置 {i+1}) 文字识别结果: {text}")
                        except Exception as e:
                            logger.error(f"{method_name} (配置 {i+1}) 文字识别失败: {str(e)}")
                            print(f"测试1失败 - {method_name} (配置 {i+1}): {str(e)}")
            else:
                logger.error(f"无法加载图像: {test_image_path}")
                print(f"测试1失败: 无法加载图像")
        else:
            logger.error(f"测试图像不存在: {test_image_path}")
            print(f"测试1失败: 测试图像不存在")

        # 测试2: 捕获屏幕区域并识别文字
        try:
            # 捕获屏幕 (这里使用全屏幕，实际测试时可以指定区域)
            screenshot = detector.capture_screen()
            logger.info("成功捕获屏幕")
            
            # 假设我们知道游戏中某个包含文字的区域
            # 这里只是示例坐标，实际使用时需要调整
            text_region = (100, 100, 300, 50)  # (x, y, width, height)
            
            # 裁剪区域
            region_image = detector.crop_image(screenshot, (
                text_region[0], 
                text_region[1], 
                text_region[0] + text_region[2], 
                text_region[1] + text_region[3]
            ))
            
            # 保存裁剪后的图像用于调试
            debug_image_path = os.path.join(os.path.dirname(__file__), 'logs', 'text_recognition_debug.png')
            cv2.imwrite(debug_image_path, region_image)
            logger.info(f"已保存调试图像到: {debug_image_path}")
            
            # 识别文字
            text = detector.recognize_text(region_image)
            logger.info(f"屏幕区域文字识别结果: {text}")
            print(f"测试2 - 屏幕区域文字识别结果: {text}")
        except Exception as e:
            logger.error(f"屏幕捕获和文字识别失败: {str(e)}")
            print(f"测试2失败: {str(e)}")

        # 测试3: 使用预定义的模板图像
        try:
            # 捕获屏幕
            screenshot = detector.capture_screen()
            
            # 查找模板 (以剩余理智为例)
            template_name = 'remaining_sanity.png'
            try:
                x, y, w, h = detector.find_template(screenshot, template_name)
                logger.info(f"找到模板: {template_name}")
                
                # 假设文字在模板的某个相对位置
                text_region = (
                    x - w//2,  # x1
                    y + h//2,  # y1
                    x + w//2,  # x2
                    y + h//2 + 30  # y2
                )
                
                # 裁剪区域
                region_image = detector.crop_image(screenshot, text_region)
                
                # 保存裁剪后的图像用于调试
                debug_image_path = os.path.join(os.path.dirname(__file__), 'logs', 'template_text_debug.png')
                cv2.imwrite(debug_image_path, region_image)
                logger.info(f"已保存模板文字调试图像到: {debug_image_path}")
                
                # 识别文字
                # 尝试使用不同的配置参数提高识别率
                text = detector.recognize_text(region_image, config='--psm 7')
                logger.info(f"模板区域文字识别结果: {text}")
                print(f"测试3 - 模板区域文字识别结果: {text}")
            except ElementNotFoundError as e:
                logger.warning(f"未找到模板: {str(e)}")
                print(f"测试3失败: 未找到模板 {template_name}")
        except Exception as e:
            logger.error(f"模板文字识别测试失败: {str(e)}")
            print(f"测试3失败: {str(e)}")

    except Exception as e:
        logger.error(f"文字识别测试失败: {str(e)}")
        print(f"测试失败: {str(e)}")


if __name__ == '__main__':
    test_text_recognition()