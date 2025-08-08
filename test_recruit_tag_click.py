import os
import sys
import time

# 设置项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.recruit import Recruit
from utils.logger import logger

def test_recruit_tag_click():
    """
    测试招募位标签点击功能
    """
    logger.info("开始测试招募位标签点击功能")
    recruit = Recruit()

    try:
        # 1. 导航到公开招募页面
        logger.info("导航到公开招募页面")
        if not recruit.navigate_to_recruit():
            logger.error("导航到公开招募页面失败，测试终止")
            return False

        # 等待页面加载完成
        time.sleep(2)

        # 2. 进入招募位并执行标签处理
        logger.info("进入招募位并执行标签处理")
        # 为了测试目的，我们可以修改enter_recruit_slots方法
        # 只处理第一个招募位，方便测试
        recruit_slot_templates = ["recruit_1.png"]

        for slot_template in recruit_slot_templates:
            logger.info(f"尝试进入招募位: {slot_template}")
            try:
                # 捕获屏幕截图
                screenshot = recruit.detector.capture_screen()

                # 查找招募位
                logger.debug(f"正在查找招募位: {slot_template}")
                slot_position = recruit.detector.find_template(screenshot, slot_template, threshold=0.7)

                if slot_position:
                    logger.info(f"找到招募位: {slot_template}，准备点击")
                    # 点击招募位
                    recruit.controller.click(slot_position[0], slot_position[1])
                    logger.info(f"已点击招募位: {slot_template}")
                    # 等待页面加载
                    time.sleep(1.5)

                    # 执行标签处理操作
                    logger.info(f"在招募位 {slot_template} 执行标签处理操作")
                    result = recruit._perform_pass_action()
                    if result:
                        logger.info(f"招募位 {slot_template} 标签处理成功")
                    else:
                        logger.warning(f"招募位 {slot_template} 标签处理失败")
                else:
                    # 这里不应该到达，因为find_template在未找到时会抛出异常
                    logger.warning(f"未找到招募位: {slot_template}，可能已锁定或不存在")
            except Exception as e:
                logger.error(f"处理招募位 {slot_template} 时出错: {str(e)}")

            # 等待一段时间再处理下一个招募位
            time.sleep(1)

        logger.info("招募位标签点击测试完成")
        return True
    except Exception as e:
        logger.error(f"测试招募位标签点击功能时出错: {str(e)}")
        return False

if __name__ == "__main__":
    test_recruit_tag_click()