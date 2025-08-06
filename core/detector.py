"""
检测器模块
负责处理图像识别和文字识别功能，用于识别游戏界面中的元素和文字
"""
import cv2
import numpy as np
import easyocr
from PIL import Image
import os
import logging
from .exceptions import ImageRecognitionError, ElementNotFoundError
from utils.logger import logger


class Detector:
    """检测器类，提供图像识别和文字识别的功能"""

    def __init__(self, template_dir=None):
        """
        初始化检测器

        Args:
            template_dir (str): 模板图像所在目录
        """
        # 初始化EasyOCR读取器
        try:
            # 语言设置为中文和英文
            self.reader = easyocr.Reader(['ch_sim', 'en'])
        except Exception as e:
            raise ImageRecognitionError(f"EasyOCR初始化失败: {str(e)}")

        # 设置模板目录
        if template_dir:
            self.template_dir = os.path.normpath(template_dir)
        else:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.template_dir = os.path.normpath(os.path.join(project_root, 'templates'))
        # 确保模板目录存在
        if not os.path.exists(self.template_dir):
            raise FileNotFoundError(f"模板目录不存在: {self.template_dir}")

    def crop_image(self, image, region):
        """
        裁剪图像的特定区域

        Args:
            image (numpy.ndarray): 要裁剪的图像
            region (tuple): 裁剪区域 (x1, y1, x2, y2)

        Returns:
            numpy.ndarray: 裁剪后的图像

        Raises:
            ImageRecognitionError: 图像裁剪失败时抛出
        """
        try:
            x1, y1, x2, y2 = region
            # 确保坐标有效
            if x1 < 0 or y1 < 0 or x2 > image.shape[1] or y2 > image.shape[0]:
                raise ImageRecognitionError("裁剪区域超出图像范围")
            # 裁剪图像
            cropped_image = image[y1:y2, x1:x2]
            return cropped_image
        except Exception as e:
            raise ImageRecognitionError("图像裁剪失败") from e

    def capture_screen(self, region=None):
        """
        捕获屏幕图像

        Args:
            region (tuple): 捕获区域 (x, y, width, height)

        Returns:
            numpy.ndarray: 捕获的图像

        Raises:
            ImageRecognitionError: 屏幕捕获失败时抛出
        """
        try:
            import mss
            import mss.tools

            with mss.mss() as sct:
                monitor = sct.monitors[1]  # 主显示器
                if region:
                    monitor = {
                        "top": region[1],
                        "left": region[0],
                        "width": region[2],
                        "height": region[3],
                        "mon": 1,
                    }

                screenshot = sct.grab(monitor)
                # 转换为OpenCV格式
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                return img
        except ImportError:
            raise ImageRecognitionError("需要安装mss库: pip install mss")
        except Exception as e:
            raise ImageRecognitionError("屏幕捕获失败") from e

    def find_template(self, screenshot, template_name, threshold=0.8):
        """
        在屏幕截图中查找模板图像

        Args:
            screenshot (numpy.ndarray): 屏幕截图
            template_name (str): 模板图像名称
            threshold (float): 匹配阈值

        Returns:
            tuple: (x, y, width, height) 匹配区域的坐标和大小

        Raises:
            ElementNotFoundError: 未找到匹配的模板时抛出
            ImageRecognitionError: 图像识别失败时抛出
        """
        try:
            # 构建模板路径
            template_path = os.path.join(self.template_dir, template_name)

            # 检查模板文件是否存在
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"模板文件不存在: {template_path}")
            logger.debug(f"模板文件存在: {template_path}")

            # 使用PIL库加载模板图像，以解决中文路径问题
            try:
                from PIL import Image
                pil_image = Image.open(template_path)
                # 转换为OpenCV格式
                template = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            except ImportError:
                raise ImageRecognitionError("需要安装PIL库: pip install pillow")
            except Exception as e:
                raise ImageRecognitionError(f"无法加载模板图像: {template_path}") from e

            # 获取模板的宽度和高度
            template_height, template_width = template.shape[:2]

            # 进行模板匹配
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # 检查匹配结果是否超过阈值
            if max_val >= threshold:
                # 计算匹配区域的中心坐标
                top_left = max_loc
                x = top_left[0] + template_width // 2
                y = top_left[1] + template_height // 2
                return (x, y, template_width, template_height)
            else:
                raise ElementNotFoundError(template_name, f"未找到匹配的模板: {template_name}, 最大匹配值: {max_val}")
        except ElementNotFoundError:
            raise
        except Exception as e:
            raise ImageRecognitionError(f"模板匹配失败: {template_name}") from e

    def recognize_text(self, image, lang='chi_sim+eng', config='--psm 6'):
        """
        识别图像中的文字

        Args:
            image (numpy.ndarray): 包含文字的图像
            lang (str): 语言，默认为中文简体+英文（此参数在EasyOCR中已预设置，仅为保持接口兼容）
            config (str): 配置参数（此参数在EasyOCR中无效，仅为保持接口兼容）

        Returns:
            str: 识别出的文字

        Raises:
            ImageRecognitionError: 文字识别失败时抛出
        """
        try:
            # 确保图像是RGB格式
            if len(image.shape) == 3 and image.shape[2] == 3:
                # EasyOCR直接处理BGR格式图像
                # 进行文字识别
                results = self.reader.readtext(image)
                # 提取识别结果中的文字
                text = ' '.join([result[1] for result in results])
                return text.strip()
            else:
                raise ImageRecognitionError("无效的图像格式，需要BGR格式的图像")
        except ImportError:
            raise ImageRecognitionError("需要安装easyocr库: pip install easyocr")
        except Exception as e:
            raise ImageRecognitionError("文字识别失败") from e

    def find_color(self, screenshot, target_color, threshold=30):
        """
        在屏幕截图中查找指定颜色

        Args:
            screenshot (numpy.ndarray): 屏幕截图
            target_color (tuple): 目标颜色 (b, g, r)
            threshold (int): 颜色匹配阈值

        Returns:
            list: 匹配区域的中心坐标列表 [(x1, y1), (x2, y2), ...]

        Raises:
            ImageRecognitionError: 颜色识别失败时抛出
        """
        try:
            # 转换为HSV颜色空间以便更好地进行颜色匹配
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

            # 定义目标颜色的HSV范围
            b, g, r = target_color
            lower = np.array([max(0, b - threshold), max(0, g - threshold), max(0, r - threshold)])
            upper = np.array([min(255, b + threshold), min(255, g + threshold), min(255, r + threshold)])

            # 创建掩码
            mask = cv2.inRange(hsv, lower, upper)

            # 查找轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 计算每个轮廓的中心坐标
            centers = []
            for contour in contours:
                if cv2.contourArea(contour) > 10:
                    M = cv2.moments(contour)
                    if M['m00'] > 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        centers.append((cx, cy))

            return centers
        except Exception as e:
            raise ImageRecognitionError("颜色识别失败") from e