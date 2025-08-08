import os
import sys
import time

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.recruit import Recruit
from utils.logger import logger

def test_recruit_slots():
    logger.info("开始测试招募位功能")
    recruit = Recruit()
    
    logger.info("导航到公开招募页面")
    if not recruit.navigate_to_recruit():
        logger.error("导航到公开招募页面失败，测试终止")
        return False
    
    logger.info("开始进入招募位并执行pass操作")
    result = recruit.enter_recruit_slots()
    
    if result:
        logger.info("招募位功能测试成功")
    else:
        logger.info("招募位功能测试失败")
    
    return result

if __name__ == "__main__":
    test_recruit_slots()