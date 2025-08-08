#!/usr/bin/env python3
"""
Jarvis AI Agent 安装验证脚本
检查所有组件是否正确安装和配置
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro} (需要3.8+)")
        return False

def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")
    
    required_paths = {
        "v1/main.py": "v1.0主程序",
        "v1/run.py": "v1.0运行脚本",
        "v2/main.py": "v2.0主程序", 
        "v2/run.py": "v2.0运行脚本",
        "v2/src/core/agent.py": "v2.0核心代理",
        "v2/src/ui/gui.py": "v2.0 GUI界面",
        "v2/src/ui/cli.py": "v2.0 CLI界面",
        "run.py": "统一运行脚本",
        "demo.py": "统一演示脚本",
        ".env": "环境变量配置"
    }
    
    all_good = True
    for path, description in required_paths.items():
        if Path(path).exists():
            print(f"✅ {description}: {path}")
        else:
            print(f"❌ {description}: {path}")
            all_good = False
    
    return all_good

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    required_packages = [
        "streamlit",
        "selenium", 
        "requests",
        "undetected_chromedriver"
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (未安装)")
            all_good = False
    
    return all_good

def check_browser_profiles():
    """检查浏览器配置"""
    print("\n🌐 检查浏览器配置...")
    
    try:
        sys.path.insert(0, str(Path("v2/src")))
        from utils.browser_profiles import BrowserProfileDetector
        
        detector = BrowserProfileDetector()
        browsers = detector.get_available_browsers()
        
        if browsers:
            print(f"✅ 检测到 {len(browsers)} 个浏览器配置:")
            for browser_name, profiles in browsers.items():
                print(f"  📁 {browser_name}: {list(profiles.keys())}")
            
            recommended = detector.get_recommended_profile()
            if recommended:
                print(f"🎯 推荐配置: {recommended[0]} - {recommended[1]}")
            
            return True
        else:
            print("❌ 未检测到浏览器配置")
            return False
            
    except Exception as e:
        print(f"❌ 浏览器配置检查失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    try:
        # 测试v2配置检测
        sys.path.insert(0, str(Path("v2/src")))
        from core.config import Config
        from core.logger import Logger
        
        config = Config()
        logger = Logger(config)
        
        print("✅ 配置系统正常")
        print("✅ 日志系统正常")
        
        # 测试浏览器配置检测
        from utils.browser_profiles import BrowserProfileDetector
        detector = BrowserProfileDetector()
        browsers = detector.get_available_browsers()
        
        if browsers:
            print("✅ 浏览器检测正常")
        else:
            print("⚠️ 浏览器检测无结果")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def show_usage_instructions():
    """显示使用说明"""
    print("\n🚀 使用说明:")
    print("=" * 50)
    
    print("📊 查看项目状态:")
    print("  python run.py --status")
    
    print("\n🎯 v2.0版本 (推荐):")
    print("  python run.py --v2 --gui      # Web界面")
    print("  python run.py --v2 --cli      # 命令行界面")
    print("  cd v2 && python run.py --gui  # 直接启动")
    
    print("\n🎯 v1.0版本:")
    print("  python run.py --v1 --gui      # Web界面")
    print("  cd v1 && python run.py --gui  # 直接启动")
    
    print("\n🎬 功能演示:")
    print("  python demo.py                # 交互式演示")
    print("  python demo.py --v2           # v2.0演示")
    
    print("\n🌐 本地浏览器配置测试:")
    print("  cd v2 && python test_local_browser_simple.py")

def main():
    """主函数"""
    print("🔍 Jarvis AI Agent 安装验证")
    print("=" * 60)
    
    checks = [
        ("Python版本", check_python_version),
        ("项目结构", check_project_structure), 
        ("依赖包", check_dependencies),
        ("浏览器配置", check_browser_profiles),
        ("基本功能", test_basic_functionality)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name}检查异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 验证结果: {passed}/{total} 项通过")
    
    if passed == total:
        print("🎉 所有检查通过！系统已准备就绪。")
        show_usage_instructions()
        return True
    else:
        print("⚠️ 部分检查失败，请根据上述信息进行修复。")
        
        if passed >= 3:  # 基本功能可用
            print("\n💡 基本功能可用，您仍然可以尝试启动:")
            print("  python run.py --v2 --gui")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
