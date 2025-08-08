#!/usr/bin/env python3
"""
简化的GUI启动脚本
解决导入路径问题
"""

import sys
import os
from pathlib import Path

# 设置正确的Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 启动Streamlit
if __name__ == "__main__":
    import subprocess
    
    print("🚀 启动 Jarvis AI Agent v2.0 Web界面...")
    print("📍 访问地址: http://localhost:8501")
    print("💡 使用 Ctrl+C 停止服务")
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['PYTHONPATH'] = str(current_dir)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/ui/gui.py",
            "--server.headless", "true",
            "--server.fileWatcherType", "none",
            "--browser.gatherUsageStats", "false"
        ], env=env, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 GUI已关闭")
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        print("\n💡 请尝试手动启动:")
        print(f"   cd {current_dir}")
        print("   python -m streamlit run src/ui/gui.py")
