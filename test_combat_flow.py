import logging
import time
from modules.combat import CombatModule
from core.exceptions import ElementNotFoundError, OperationFailedError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/test_combat_flow.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def test_auto_combat_flow():
    """
    测试自动作战流程功能
    """
    try:
        logger.info("开始测试自动作战流程")
        # 初始化作战模块
        combat_module = CombatModule()

        # 执行自动作战流程，循环2次
        logger.info("执行自动作战流程，循环2次")
        success = combat_module.auto_combat_flow(cycles=2, threshold=0.4)

        if success:
            logger.info("自动作战流程测试成功")
            return True
        else:
            logger.error("自动作战流程测试失败")
            return False

    except ElementNotFoundError as e:
        logger.error(f"测试失败: 未找到元素 - {e}")
        return False
    except OperationFailedError as e:
        logger.error(f"测试失败: 操作失败 - {e}")
        return False
    except Exception as e:
        logger.error(f"测试失败: 发生未预期的异常 - {e}")
        return False


if __name__ == "__main__":
    test_auto_combat_flow()