import logging
import os
from datetime import datetime

# 初始化日志记录器
def setup_logger(log_level="INFO"):
    """设置日志系统"""
    # 创建日志目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 日志文件名
    log_filename = f"{datetime.now().strftime('%Y%m%d')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    # 配置日志
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("ZOOT")

# 创建默认日志器
logger = setup_logger()
    