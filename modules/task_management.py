import time
from core.controller import Controller
from core.detector import Detector
from core.exceptions import ElementNotFoundError, OperationFailedError
from utils.logger import logger

class TaskManagementModule:
    def __init__(self):
        self.controller = Controller()
        self.detector = Detector()
        
    def claim_all_rewards(self, threshold=0.6):
        """
        领取所有任务奖励（日常和每周）
        
        Args:
            threshold (float): 模板匹配阈值，默认为0.6
        """
        try:
            # 点击主任务按钮
            logger.info("开始领取任务奖励流程")
            screenshot = self.detector.capture_screen()
            task_btn_pos = self.detector.find_template(screenshot, "main_task_btn.png", threshold)
            if not task_btn_pos:
                raise ElementNotFoundError("main_task_btn.png", "未找到主任务按钮")
            x, y, _, _ = task_btn_pos
            self.controller.click(x, y)
            logger.info("成功点击主任务按钮")
            time.sleep(2)
            
            # 领取日常奖励
            logger.info("开始领取日常任务奖励")
            try:
                screenshot = self.detector.capture_screen()
                daily_btn_pos = self.detector.find_template(screenshot, "daily_btn.png", threshold)
                x, y, _, _ = daily_btn_pos
                self.controller.click(x, y)
                logger.info("成功点击日常任务按钮")
                time.sleep(4)
                
                try:
                    screenshot = self.detector.capture_screen()
                    get_all_btn_pos = self.detector.find_template(screenshot, "get_all_btn.png", threshold)
                    x, y, _, _ = get_all_btn_pos
                    self.controller.click(x, y)
                    logger.info("成功点击日常任务全部领取按钮")
                    time.sleep(3)
                    
                    # 原地点击
                    self.controller.click(x, y)
                    logger.info("原地点击确认")
                    time.sleep(2)
                except ElementNotFoundError as e:
                    logger.warning(f"未找到日常任务全部领取按钮，跳过: {str(e)}")
            except ElementNotFoundError as e:
                logger.warning(f"未找到日常任务按钮，跳过: {str(e)}")
            
            # 领取每周奖励
            logger.info("开始领取每周任务奖励")
            try:
                screenshot = self.detector.capture_screen()
                weekly_btn_pos = self.detector.find_template(screenshot, "weekly_btn.png", threshold)
                x, y, _, _ = weekly_btn_pos
                self.controller.click(x, y)
                logger.info("成功点击每周任务按钮")
                time.sleep(4)
                
                try:
                    screenshot = self.detector.capture_screen()
                    get_all_btn_pos = self.detector.find_template(screenshot, "get_all_btn.png", threshold)
                    x, y, _, _ = get_all_btn_pos
                    self.controller.click(x, y)
                    logger.info("成功点击每周任务全部领取按钮")
                    time.sleep(3)
                    
                    # 原地点击
                    self.controller.click(x, y)
                    logger.info("原地点击确认")
                    time.sleep(2)
                except ElementNotFoundError as e:
                    logger.warning(f"未找到每周任务全部领取按钮，跳过: {str(e)}")
            except ElementNotFoundError as e:
                logger.warning(f"未找到每周任务按钮，跳过: {str(e)}")
            
            # 返回主页
            logger.info("准备返回主页")
            try:
                screenshot = self.detector.capture_screen()
                top_bar_pos = self.detector.find_template(screenshot, "top_bar.png", threshold)
                if top_bar_pos:
                    x, y, _, _ = top_bar_pos
                    self.controller.click(x, y)
                    logger.info("成功点击顶部栏")
                    time.sleep(1)
                    
                    screenshot = self.detector.capture_screen()
                    home_btn_pos = self.detector.find_template(screenshot, "home_btn.png", threshold)
                    if home_btn_pos:
                        x, y, _, _ = home_btn_pos
                        self.controller.click(x, y)
                        logger.info("成功点击首页按钮，返回主页")
                        time.sleep(2)
                    else:
                        logger.warning("未找到首页按钮，跳过返回主页")
                else:
                    logger.warning("未找到顶部栏，跳过返回主页")
            except Exception as e:
                logger.error(f"返回主页过程中发生错误: {str(e)}")
            
            logger.info("任务奖励领取流程完成")
            return True
            
        except ElementNotFoundError as e:
            logger.error(f"领取任务奖励失败: {str(e)}")
            return False
        except OperationFailedError as e:
            logger.error(f"操作失败: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"领取任务奖励时发生未知错误: {str(e)}", exc_info=True)
            return False