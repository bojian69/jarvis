#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志配置
"""

import logging
import sys
from pathlib import Path

def setup_logger():
    """配置日志系统"""
    # 创建logs目录
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_dir / "jarvis.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)