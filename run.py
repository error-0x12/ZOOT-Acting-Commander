from gui.main_gui import main

if __name__ == "__main__":
    main()

# """
# PRTS代理指挥启动器
# 用于测试和运行PRTS代理指挥工具
# """
# import time
# import sys
# from utils import logger
# from modules import BaseManagementModule, CombatModule, TaskManagementModule
# from core.exceptions import ElementNotFoundError, OperationFailedError


# def check_dependencies():
#     """
#     检查必要的依赖库是否已安装
#     """
#     required_libraries = [
#         'pyautogui',
#         'cv2',  # opencv-python的导入名称
#         'mss',
#         'pytesseract'
#     ]
    
#     missing_libraries = []
#     for lib in required_libraries:
#         try:
#             __import__(lib)
#         except ImportError:
#             missing_libraries.append(lib)
    
#     if missing_libraries:
#         logger.error(f"错误: 缺少必要的依赖库: {', '.join(missing_libraries)}")
#         logger.info("请使用以下命令安装:")
#         for lib in missing_libraries:
#             logger.info(f"pip install {lib}")
#         return False
    
#     return True


# def test_base_navigation(threshold=0.6):
#     """
#     测试基建导航功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试基建导航功能...")
#     logger.info("请在3秒内唤出明日方舟游戏窗口，并确保主菜单可见...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建基建管理模块实例
#         base_manager = BaseManagementModule()
        
#         logger.info("正在尝试导航到基建...")
#         # 导航到基建
#         success = base_manager.navigate_to_base(threshold=threshold)
#         time.sleep(5)
#         if success:
#             logger.info("基建导航测试成功!")
#         else:
#             logger.error("基建导航测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配或基建按钮不可见")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")


# def test_complete_tasks(threshold=0.6):
#     """
#     测试完成事项功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试完成事项功能...")
#     logger.info("请确保已在基建界面，且通知按钮可见...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建基建管理模块实例
#         base_manager = BaseManagementModule()
        
#         logger.info("正在尝试完成事项...")
#         # 完成事项
#         success = base_manager.complete_tasks(threshold=threshold)
        
#         if success:
#             logger.info("完成事项测试成功!")
#         else:
#             logger.error("完成事项测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配或通知按钮不可见")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")


# def test_claim_task_rewards(threshold=0.6):
#     """
#     测试领取任务奖励功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试领取任务奖励功能...")
#     logger.info("请在3秒内唤出明日方舟游戏窗口，并确保主菜单可见...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建任务管理模块实例
#         task_manager = TaskManagementModule()
        
#         # 调用领取奖励方法阈值为0.6
#         success = task_manager.claim_all_rewards(threshold=0.6)
        
#         if success:
#             logger.info("领取任务奖励测试成功!")
#         else:
#             logger.error("领取任务奖励测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")

# def test_exit_from_base(threshold=0.6):
#     """
#     测试退出基建功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试退出基建功能...")
#     logger.info("请确保已在基建界面...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建基建管理模块实例
#         base_manager = BaseManagementModule()
        
#         logger.info("正在尝试退出基建...")
#         # 退出基建
#         success = base_manager.exit_from_base(threshold=threshold)
        
#         if success:
#             logger.info("退出基建测试成功!")
#         else:
#             logger.error("退出基建测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")


# def test_mission_navigation(threshold=0.6):
#     """
#     测试作战导航功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试作战导航功能...")
#     logger.info("请在3秒内唤出明日方舟游戏窗口，并确保主菜单可见...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建作战模块实例
#         combat_manager = CombatModule()
        
#         logger.info("正在尝试导航到作战界面...")
#         # 导航到作战界面
#         success = combat_manager.navigate_to_mission(threshold=threshold)
#         time.sleep(5)
#         if success:
#             logger.info("作战导航测试成功!")
#         else:
#             logger.error("作战导航测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配或作战按钮不可见")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")

# i = 0
# def test_sanity_and_acting_commander(threshold=0.8):
#     """
#     测试理智识别和代理指挥功能

#     Args:
#         threshold (float): 模板匹配阈值，默认为0.8
#     """
#     logger.info("开始测试理智识别和代理指挥功能...")
#     logger.info("请在3秒内唤出明日方舟游戏窗口，并确保在作战界面...")
#     logger.info(f"当前模板匹配阈值: {threshold}")

#     # 等待3秒
#     time.sleep(3)

#     try:
#         # 创建作战模块实例
#         combat_manager = CombatModule()

#         # 测试识别剩余理智
#         logger.info("正在尝试识别剩余理智...")
#         remaining_sanity = combat_manager.recognize_remaining_sanity()
#         time.sleep(1)

#         # 测试识别消耗理智
#         logger.info("正在尝试识别消耗理智...")
#         consuming_sanity = combat_manager.recognize_consuming_sanity()
#         time.sleep(1)

#         # 测试计算可执行次数
#         logger.info("正在尝试计算可执行次数...")
#         executable_times = combat_manager.calculate_executable_times()
#         logger.info(f"可执行次数: {executable_times}")
        
#         time.sleep(1)

#         # 测试检查并启用代理指挥
#         logger.info("正在尝试检查并启用代理指挥...")
#         acting_commander_success = combat_manager.check_and_enable_acting_commander(threshold=threshold)
#         time.sleep(1)

#         if acting_commander_success:
#             logger.info("代理指挥功能测试成功!")
#         else:
#             logger.error("代理指挥功能测试失败!")

#         logger.info("理智识别和代理指挥功能测试完成!")
#         return executable_times
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行或OCR识别失败")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

# def test_eliminate_navigation(threshold=0.6):
#     """
#     测试剿灭作战导航功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试剿灭作战导航功能...")
#     logger.info("请在3秒内唤出明日方舟游戏窗口，并确保主菜单可见...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建作战模块实例
#         combat_manager = CombatModule()
        
#         logger.info("正在尝试导航到作战界面...")
#         # 导航到作战界面
#         if not combat_manager.navigate_to_mission(threshold=threshold):
#             logger.error("无法导航到作战界面")
#             return
#         time.sleep(2)
        
#         logger.info("正在尝试导航到常态事务...")
#         # 导航到常态事务
#         if not combat_manager.navigate_to_normal_affairs(threshold=threshold):
#             logger.error("无法导航到常态事务")
#             return
#         time.sleep(2)
        
#         logger.info("正在尝试导航到剿灭作战...")
#         # 导航到剿灭作战
#         success = combat_manager.navigate_to_eliminate(threshold=threshold)
#         time.sleep(5)
#         if success:
#             logger.info("剿灭作战导航测试成功!")
#         else:
#             logger.error("剿灭作战导航测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")

# def test_normal_affairs_navigation(threshold=0.6):
#     """
#     测试常态事务导航功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试常态事务导航功能...")
#     logger.info("请确保已在作战界面...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建作战模块实例
#         combat_manager = CombatModule()
        
#         logger.info("正在尝试导航到常态事务...")
#         # 导航到常态事务
#         success = combat_manager.navigate_to_normal_affairs(threshold=threshold)
#         time.sleep(5)
#         if success:
#             logger.info("常态事务导航测试成功!")
#         else:
#             logger.error("常态事务导航测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配或常态事务按钮不可见")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")


# def test_longmen_navigation(threshold=0.6):
#     """
#     测试导航到龙门功能
    
#     Args:
#         threshold (float): 模板匹配阈值，默认为0.6
#     """
#     logger.info("开始测试导航到龙门功能...")
#     logger.info("请在3秒内唤出明日方舟游戏窗口，并确保主菜单可见...")
#     logger.info(f"当前模板匹配阈值: {threshold}")
    
#     # 等待3秒
#     time.sleep(3)
    
#     try:
#         # 创建作战模块实例
#         combat_manager = CombatModule()
        
#         logger.info("正在尝试导航到作战界面...")
#         # 导航到作战界面
#         if not combat_manager.navigate_to_mission(threshold=threshold):
#             logger.error("无法导航到作战界面")
#             return
#         time.sleep(2)
        
#         logger.info("正在尝试导航到常态事务...")
#         # 导航到常态事务
#         if not combat_manager.navigate_to_normal_affairs(threshold=threshold):
#             logger.error("无法导航到常态事务")
#             return
#         time.sleep(2)
        
#         logger.info("正在尝试导航到剿灭作战...")
#         # 导航到剿灭作战
#         if not combat_manager.navigate_to_eliminate(threshold=threshold):
#             logger.error("无法导航到剿灭作战")
#             return
#         time.sleep(2)
        
#         logger.info("正在尝试导航到龙门...")
#         # 导航到龙门
#         success = combat_manager.navigate_to_longmen(threshold=threshold)
#         time.sleep(5)
#         if success:
#             logger.info("导航到龙门测试成功!")
#         else:
#             logger.error("导航到龙门测试失败!")
#     except ElementNotFoundError as e:
#         logger.error(f"测试失败: 未找到元素 - {e}")
#         logger.warning("可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
#     except OperationFailedError as e:
#         logger.error(f"测试失败: 操作失败 - {e}")
#         logger.warning("可能的原因: 鼠标点击操作未能正确执行")
#     except Exception as e:
#         logger.error(f"测试过程中发生未知错误: {str(e)}")
#         import traceback
#         traceback.print_exc()

#     logger.info("测试完成")


# if __name__ == "__main__":
#     # 检查依赖
#     if not check_dependencies():
#         sys.exit(1)
    
#     # test_base_navigation()
#     # test_complete_tasks()
#     # test_exit_from_base()
#     test_claim_task_rewards()


#     # test_longmen_navigation()
#     # i = test_sanity_and_acting_commander()
#     # print(i)
#     # i = 2
#     # combat_module = CombatModule()
#     # # 调用仅作战流程方法(从点击'开始行动'字样后开始)，循环2次，匹配阈值0.5
#     # combat_module.combat_only_flow(cycles=i, threshold=0.7)

    