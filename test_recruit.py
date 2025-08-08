import os
import sys

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.recruit import Recruit
from utils.logger import logger

if __name__ == "__main__":
    logger.info("开始测试公开招募模块")
    recruit = Recruit()
    result = recruit.navigate_to_recruit()
    if result:
        logger.info("导航到公开招募页面成功")
    else:
        logger.info("导航到公开招募页面失败")