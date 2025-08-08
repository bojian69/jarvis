# 🤖 Jarvis AI Agent v2.0

一个全面重构的智能AI助手，采用模块化架构，支持浏览器自动化、API调用、代码执行等功能。**无需API密钥即可使用核心功能！**

## ✨ 新版本特性

### 🏗️ 架构优化
- **模块化设计**: 清晰的代码分离，易于维护和扩展
- **中间件系统**: 支持请求拦截、日志记录、错误处理、重试机制
- **配置管理**: 统一的配置系统，支持JSON配置文件
- **增强日志**: 多级别日志、自动截图、结构化日志记录

### 📁 项目结构
```
jarvis/
├── src/                    # 源代码目录
│   ├── core/              # 核心模块
│   │   ├── agent.py       # 主代理类
│   │   ├── config.py      # 配置管理
│   │   ├── logger.py      # 日志系统
│   │   └── middleware.py  # 中间件系统
│   ├── modules/           # 功能模块
│   │   ├── browser.py     # 浏览器操作
│   │   ├── api.py         # API调用
│   │   └── code.py        # 代码执行
│   └── ui/                # 用户界面
│       ├── gui.py         # Web界面
│       └── cli.py         # 命令行界面
├── logs/                  # 日志目录
│   ├── screenshots/       # 截图文件
│   ├── debug/            # 调试日志
│   ├── info/             # 信息日志
│   └── error/            # 错误日志
├── config/               # 配置文件
├── main_v2.py           # 主入口文件
└── run_v2.py            # 运行脚本
```

## 🚀 快速开始

### 1. 环境准备
```bash
# 克隆项目
cd /Volumes/bojian/github-bojian/jarvis

# 安装依赖
python run_v2.py --install

# 检查环境
python run_v2.py --check
```

### 2. 配置API密钥（可选）
编辑 `.env` 文件，添加你的API密钥：
```bash
# OpenAI API（用于AI对话）
OPENAI_API_KEY=your_openai_api_key_here

# Google API（用于搜索）
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# GitHub API（用于代码搜索）
GITHUB_TOKEN=your_github_token_here
```

### 3. 启动应用

#### Web界面（推荐）
```bash
python run_v2.py --gui
```
然后在浏览器中访问 `http://localhost:8501`

#### 命令行界面
```bash
python run_v2.py --cli
```

#### 纯代理模式
```bash
python run_v2.py --agent
```

## 🎯 功能特性

### 🌐 浏览器自动化
- **真实浏览器**: 使用Chrome浏览器，避免反机器人检测
- **智能操作**: 点击、输入、滚动、截图等操作
- **自动截图**: 操作前后自动截图，便于调试
- **Google搜索**: 内置Google搜索功能

### 🔌 API调用
- **OpenAI集成**: 支持GPT模型对话
- **Google搜索**: 高级搜索API
- **GitHub搜索**: 代码仓库搜索
- **天气查询**: 实时天气信息
- **通用HTTP**: 支持任意HTTP API调用

### 💻 代码执行
- **Python执行**: 安全的Python代码执行环境
- **Shell命令**: 系统命令执行
- **文件操作**: 读写文件、目录列表
- **包管理**: 自动安装Python包

### 📸 截图管理
- **自动截图**: 操作过程自动截图记录
- **手动截图**: 支持手动截图
- **图片管理**: Web界面查看和管理截图
- **时间戳**: 自动添加时间戳和描述

### 🛡️ 中间件系统
- **日志中间件**: 自动记录操作日志
- **截图中间件**: 操作前后自动截图
- **重试中间件**: 失败自动重试
- **验证中间件**: 参数验证

## 📖 使用示例

### Web界面操作
1. 启动Web界面：`python run_v2.py --gui`
2. 在浏览器中打开应用
3. 在侧边栏启动Agent
4. 选择功能标签页进行操作

### 命令行操作
```bash
# 启动CLI
python run_v2.py --cli

# 浏览器操作
jarvis> browser navigate https://www.google.com
jarvis> browser search "Python教程"
jarvis> browser screenshot "搜索结果"

# API调用
jarvis> api chat "你好，请介绍一下Python"
jarvis> api weather Beijing

# 代码执行
jarvis> code python "print('Hello, Jarvis!')"
jarvis> code shell "ls -la"
```

### 编程接口
```python
from src.core.agent import JarvisAgent

# 创建Agent实例
with JarvisAgent() as agent:
    # 浏览器操作
    result = agent.execute_command("browser_navigate", url="https://www.google.com")
    
    # API调用
    result = agent.execute_command("api_openai_chat", message="Hello!")
    
    # 代码执行
    result = agent.execute_command("code_execute_python", code="print('Hello!')")
```

## ⚙️ 配置说明

### 配置文件位置
- 主配置：`config/settings.json`
- 环境变量：`.env`

### 主要配置项
```json
{
  "browser": {
    "headless": false,
    "window_size": [1920, 1080],
    "timeout": 10
  },
  "logging": {
    "level": "INFO",
    "max_file_size": "10MB",
    "backup_count": 5
  },
  "api": {
    "timeout": 30,
    "retry_count": 3,
    "retry_delay": 1
  },
  "screenshots": {
    "enabled": true,
    "quality": 90,
    "format": "PNG"
  }
}
```

## 🔧 开发指南

### 添加新功能模块
1. 在 `src/modules/` 下创建新模块文件
2. 继承基础模块类，实现 `execute_command` 方法
3. 在 `src/core/agent.py` 中注册新模块

### 添加新中间件
1. 在 `src/core/middleware.py` 中创建新中间件类
2. 继承 `Middleware` 基类
3. 实现 `before_request`、`after_request`、`on_error` 方法

### 自定义配置
1. 修改 `config/settings.json` 文件
2. 或通过代码调用 `config.set(key, value)` 方法

## 📋 系统要求

- **Python**: 3.8+
- **操作系统**: Windows/macOS/Linux
- **浏览器**: Chrome（自动下载驱动）
- **内存**: 建议4GB+

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License

## 🆘 常见问题

### Q: 浏览器启动失败？
A: 确保系统已安装Chrome浏览器，或尝试使用无头模式：`--headless`

### Q: API调用失败？
A: 检查网络连接和API密钥配置，使用 `api test` 命令测试连接

### Q: 截图功能不工作？
A: 检查 `logs/screenshots/` 目录权限，确保可写入

### Q: 如何查看详细日志？
A: 使用 `logs debug 50` 命令查看最近50条调试日志

## 📞 支持

如有问题或建议，请提交Issue或联系开发者。

---

**Jarvis AI Agent v2.0** - 让AI助手更智能、更可靠、更易用！
