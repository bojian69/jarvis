# 🚀 Jarvis AI Agent 快速开始指南

## 📋 项目概述

Jarvis AI Agent 现在提供两个版本：
- **v1.0**: 原始版本，功能集中，适合快速上手
- **v2.0**: 优化版本，模块化架构，功能更强大 ⭐ **推荐**

## ⚡ 5分钟快速开始

### 1. 检查项目状态
```bash
python run.py --status
```

### 2. 选择版本并安装依赖

#### 使用 v2.0 版本 (推荐)
```bash
# 安装依赖
python run.py --v2 --install

# 检查环境
python run.py --v2 --check

# 启动Web界面
python run.py --v2 --gui
```

#### 使用 v1.0 版本
```bash
# 安装依赖
python run.py --v1 --install

# 启动Web界面
python run.py --v1 --gui
```

### 3. 体验功能演示
```bash
# 交互式演示选择
python demo.py

# 直接运行v2.0演示
python demo.py --v2

# 版本对比
python demo.py --compare
```

## 🎯 主要使用方式

### 🖥️ Web界面 (推荐新手)
```bash
# v2.0 Web界面 (功能更丰富，支持本地浏览器配置)
python run.py --v2 --gui

# v1.0 Web界面 (简单直接)
python run.py --v1 --gui
```
然后在浏览器中访问显示的地址 (通常是 http://localhost:8501)

**🌟 v2.0 新特性 - 本地浏览器配置:**
- ✅ 使用您本地浏览器的所有设置和扩展
- ✅ 保持所有网站的登录状态
- ✅ 无需重新配置任何内容
- ✅ 真正的"本地浏览器"自动化体验

### ⌨️ 命令行界面 (仅v2.0)
```bash
python run.py --v2 --cli
```
提供类似shell的交互式命令行体验

### 💻 编程接口 (v2.0)
```python
import sys
sys.path.append('v2')
from src.core.agent import JarvisAgent

with JarvisAgent() as agent:
    # 浏览器操作
    result = agent.execute_command("browser_navigate", url="https://www.google.com")
    
    # API调用
    result = agent.execute_command("api_weather", city="Beijing")
    
    # 代码执行
    result = agent.execute_command("code_execute_python", code="print('Hello!')")
```

## 🔧 配置说明

### 环境变量配置 (.env)
```bash
# 复制示例文件
cp .env.example .env

# 编辑配置文件，添加你的API密钥
# OpenAI API (用于AI对话)
OPENAI_API_KEY=your_openai_api_key_here

# Google API (用于搜索)
GOOGLE_API_KEY=your_google_api_key_here

# GitHub API (用于代码搜索)
GITHUB_TOKEN=your_github_token_here
```

### v2.0 高级配置 (可选)
编辑 `v2/config/settings.json`:
```json
{
  "browser": {
    "headless": false,
    "window_size": [1920, 1080]
  },
  "logging": {
    "level": "INFO"
  }
}
```

## 🎮 功能体验

### 1. 浏览器自动化
- 访问网页
- 自动搜索
- 元素点击和输入
- 自动截图记录

### 2. AI对话 (需要API密钥)
- OpenAI GPT模型对话
- 智能问答
- 代码生成

### 3. API调用
- 天气查询
- GitHub搜索
- 通用HTTP请求

### 4. 代码执行
- Python代码运行
- Shell命令执行
- 文件操作

## 🆘 常见问题

### Q: 应该选择哪个版本？
**A: 推荐使用v2.0版本**
- 新用户: v2.0 (功能更完整，界面更友好)
- 快速测试: v1.0 (启动更快)
- 生产使用: v2.0 (架构更稳定)

### Q: 没有API密钥可以使用吗？
**A: 可以！** 
- 浏览器自动化功能无需API密钥
- 代码执行功能无需API密钥
- 部分API功能需要密钥 (如OpenAI对话)

### Q: 如何查看日志？
**A: v2.0版本提供完整日志**
```bash
# 查看最近日志
cd v2
python -c "
from src.core.config import Config
from src.core.logger import Logger
config = Config()
logger = Logger(config)
logs = logger.get_recent_logs('info', 10)
for log in logs: print(log.strip())
"
```

### Q: 浏览器启动失败怎么办？
**A: 尝试以下解决方案**
```bash
# 使用无头模式
python run.py --v2 --agent --headless

# 检查Chrome是否安装
# macOS: 确保安装了Chrome浏览器
# 或者使用Web界面，在界面中启动浏览器
```

### Q: 如何扩展功能？
**A: v2.0支持模块化扩展**
1. 在 `v2/src/modules/` 下添加新模块
2. 在 `v2/src/core/middleware.py` 中添加中间件
3. 参考现有代码结构

## 📚 进阶使用

### 命令行快捷方式 (v2.0)
```bash
cd v2
python -c "
from src.core.agent import JarvisAgent
agent = JarvisAgent()
# 你的代码
agent.close()
"
```

### 批量操作示例
```python
# 批量网页截图
urls = ['https://www.google.com', 'https://www.github.com']
for url in urls:
    agent.execute_command('browser_navigate', url=url)
    agent.execute_command('browser_screenshot', description=f'screenshot_{url}')
```

### 自定义中间件
```python
# 在 v2/src/core/middleware.py 中添加
class TimingMiddleware(Middleware):
    def before_request(self, context):
        context['start_time'] = time.time()
        return context
    
    def after_request(self, context, result):
        duration = time.time() - context['start_time']
        print(f"操作耗时: {duration:.2f}秒")
        return result
```

## 🎉 开始使用

选择一个命令开始你的Jarvis之旅：

```bash
# 最简单的开始方式
python run.py --v2 --gui

# 或者先看看演示
python demo.py --v2

# 或者查看项目状态
python run.py --status
```

**祝你使用愉快！** 🚀

---

💡 **提示**: 
- 遇到问题查看对应版本目录下的README文件
- v2.0版本功能更强大，推荐优先使用
- 所有操作都有详细日志记录，便于调试
