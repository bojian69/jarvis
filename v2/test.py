#!/usr/bin/env python3
"""
Jarvis AI Agent v2.0 测试脚本
验证新架构的基本功能
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_config():
    """测试配置系统"""
    print("🧪 测试配置系统...")
    try:
        from src.core.config import Config
        config = Config()
        
        print(f"✅ 项目根目录: {config.project_root}")
        print(f"✅ 日志目录: {config.logs_dir}")
        print(f"✅ API状态: {config.api_status}")
        print(f"✅ 浏览器配置: {config.browser_config}")
        
        return True
    except Exception as e:
        print(f"❌ 配置系统测试失败: {e}")
        return False

def test_logger():
    """测试日志系统"""
    print("\n🧪 测试日志系统...")
    try:
        from src.core.config import Config
        from src.core.logger import Logger
        
        config = Config()
        logger = Logger(config)
        
        logger.info("这是一条测试信息")
        logger.debug("这是一条调试信息")
        logger.warning("这是一条警告信息")
        
        print("✅ 日志系统测试成功")
        return True
    except Exception as e:
        print(f"❌ 日志系统测试失败: {e}")
        return False

def test_middleware():
    """测试中间件系统"""
    print("\n🧪 测试中间件系统...")
    try:
        from src.core.config import Config
        from src.core.logger import Logger
        from src.core.middleware import MiddlewareManager, LoggingMiddleware
        
        config = Config()
        logger = Logger(config)
        middleware_manager = MiddlewareManager()
        
        # 添加日志中间件
        middleware_manager.add_middleware(LoggingMiddleware(logger))
        
        # 测试函数
        def test_function(message="Hello"):
            return f"处理消息: {message}"
        
        # 使用中间件执行函数
        context = {
            "action": "test_function",
            "args": {"message": "测试消息"}
        }
        
        result = middleware_manager.execute_with_middleware(test_function, context)
        print(f"✅ 中间件执行结果: {result}")
        
        return True
    except Exception as e:
        print(f"❌ 中间件系统测试失败: {e}")
        return False

def test_modules():
    """测试功能模块"""
    print("\n🧪 测试功能模块...")
    try:
        from src.core.config import Config
        from src.core.logger import Logger
        from src.core.middleware import MiddlewareManager
        from src.modules.api import APIModule
        from src.modules.code import CodeModule
        
        config = Config()
        logger = Logger(config)
        middleware_manager = MiddlewareManager()
        
        # 测试API模块
        api_module = APIModule(config, logger, middleware_manager)
        result = api_module.execute_command("api_test_connection")
        success1 = isinstance(result, dict) and result.get('success') is not None
        print(f"✅ API模块测试: {success1}")
        
        # 测试代码模块
        code_module = CodeModule(config, logger, middleware_manager)
        result = code_module.execute_command("code_execute_python", code="print('Hello from code module!')")
        success2 = isinstance(result, dict) and result.get('success') is not None
        print(f"✅ 代码模块测试: {success2}")
        
        return success1 and success2
    except Exception as e:
        print(f"❌ 功能模块测试失败: {e}")
        return False

def test_agent():
    """测试主代理"""
    print("\n🧪 测试主代理...")
    try:
        from src.core.agent import JarvisAgent
        
        # 创建代理实例（不启动浏览器）
        agent = JarvisAgent()
        
        # 测试代码执行
        result = agent.execute_command("code_execute_python", code="print('Hello from Jarvis Agent!')")
        success1 = isinstance(result, dict) and result.get('success') is not None
        print(f"✅ 代理代码执行测试: {success1}")
        
        # 测试API调用
        result = agent.execute_command("api_test_connection")
        success2 = isinstance(result, dict) and result.get('success') is not None
        print(f"✅ 代理API测试: {success2}")
        
        # 关闭代理
        agent.close()
        
        return success1 and success2
    except Exception as e:
        print(f"❌ 主代理测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 Jarvis AI Agent v2.0 架构测试")
    print("=" * 50)
    
    tests = [
        test_config,
        test_logger,
        test_middleware,
        test_modules,
        test_agent
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！新架构工作正常。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关模块。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
