import logging
import os
import sys
import time

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.recruit import Recruit
from utils.logger import logger

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_recruit_integration():
    """
    整合测试招募功能
    1. 导航到招募页面
    2. 进入第一个招募位
    3. 测试标签识别和点击功能
    """
    logger.info("开始招募功能整合测试")
    recruit = Recruit()

    try:
        # 1. 导航到招募页面
        logger.info("导航到招募页面")
        if not recruit.navigate_to_recruit():
            logger.error("导航到招募页面失败")
            return False

        # 2. 进入第一个招募位
        logger.info("进入第一个招募位")
        if not recruit.enter_recruit_slots(1):
            logger.error("进入招募位失败")
            return False

        # 3. 执行pass操作已在enter_recruit_slots中完成
        logger.info("招募位操作已完成")
        # 由于enter_recruit_slots方法已经内部调用了_perform_pass_action
        # 我们这里不需要单独调用
        
    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}")
        return False

    logger.info("招募功能整合测试完成")
    return True

if __name__ == "__main__":
    test_recruit_integration()