# 🤖 Jarvis AI Agent

一个智能AI助手项目，支持浏览器自动化、API调用、代码执行等功能。

## 📁 项目结构

```
jarvis/
├── v1/                    # 原始版本 (v1.0)
│   ├── main.py           # 原始主程序
│   ├── run.py            # 原始运行脚本
│   ├── gui.py            # 原始Web界面
│   └── ...               # 其他原始文件
├── v2/                    # 优化版本 (v2.0) ⭐ 推荐
│   ├── src/              # 模块化源代码
│   ├── main.py           # 优化主程序
│   ├── run.py            # 增强运行脚本
│   └── ...               # 其他优化文件
├── .env                  # 环境变量配置
├── .gitignore           # Git忽略文件
└── README.md            # 本文件
```

## 🚀 快速开始

### 推荐使用 v2.0 版本

```bash
# 进入v2目录
cd v2

# 安装依赖
python run.py --install

# 检查环境
python run.py --check

# 启动Web界面
python run.py --gui

# 或启动命令行界面
python run.py --cli

# 运行功能演示
python demo.py
```

### 使用 v1.0 版本（原始版本）

```bash
# 进入v1目录
cd v1

# 安装依赖
python run.py --install

# 启动Web界面
python run.py --gui
```

## 📊 版本对比

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 代码结构 | 单文件集中 | 模块化分离 ✅ |
| 日志系统 | 基础日志 | 多级别日志 ✅ |
| 截图管理 | 手动保存 | 自动截图 ✅ |
| 中间件支持 | ❌ | 完整支持 ✅ |
| 配置管理 | 环境变量 | 配置文件+环境变量 ✅ |
| 用户界面 | Web界面 | Web+CLI界面 ✅ |
| 错误处理 | 基础处理 | 增强处理+重试 ✅ |
| 扩展性 | 有限 | 高度可扩展 ✅ |

## 🎯 主要功能

### 🌐 浏览器自动化
- 真实Chrome浏览器操作
- 智能元素定位和操作
- 自动截图记录
- Google搜索集成

### 🔌 API调用
- OpenAI GPT模型对话
- Google搜索API
- GitHub代码搜索
- 天气查询API
- 通用HTTP请求

### 💻 代码执行
- Python代码安全执行
- Shell命令执行
- 文件读写操作
- Python包自动安装

### 📸 截图和日志
- 操作过程自动截图
- 多级别日志记录
- 结构化日志存储
- 可视化日志查看

## ⚙️ 配置说明

### 环境变量配置 (.env)
```bash
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Google API
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# GitHub API
GITHUB_TOKEN=your_github_token_here

# 其他API密钥...
```

### v2.0 配置文件 (v2/config/settings.json)
```json
{
  "browser": {
    "headless": false,
    "window_size": [1920, 1080],
    "timeout": 10
  },
  "logging": {
    "level": "INFO",
    "max_file_size": "10MB"
  },
  "api": {
    "timeout": 30,
    "retry_count": 3
  }
}
```

## 🛠️ 开发指南

### 选择版本
- **学习和简单使用**: 选择 v1.0
- **生产环境和扩展开发**: 选择 v2.0 ⭐

### v2.0 扩展开发
```python
# 添加新功能模块
from v2.src.core.agent import JarvisAgent

with JarvisAgent() as agent:
    result = agent.execute_command("your_command", **kwargs)
```

### 添加新中间件
```python
# 在 v2/src/core/middleware.py 中
class CustomMiddleware(Middleware):
    def before_request(self, context):
        # 请求前处理
        return context
    
    def after_request(self, context, result):
        # 请求后处理
        return result
```

## 📋 系统要求

- **Python**: 3.8+
- **操作系统**: Windows/macOS/Linux
- **浏览器**: Chrome（自动下载驱动）
- **内存**: 建议4GB+

## 🤝 贡献指南

1. Fork 项目
2. 选择合适的版本目录 (v1/ 或 v2/)
3. 创建功能分支
4. 提交更改
5. 创建Pull Request

## 📄 许可证

MIT License

## 🆘 常见问题

### Q: 应该选择哪个版本？
A: 
- 新用户和生产环境推荐使用 **v2.0**
- 需要简单快速上手可以使用 v1.0
- v2.0 提供更好的架构和功能

### Q: 如何从v1.0迁移到v2.0？
A: 
- v2.0 保持了API兼容性
- 配置文件需要重新设置
- 详细迁移指南请查看 v2/README_DETAILED.md

### Q: 两个版本可以同时使用吗？
A: 可以，它们在不同目录中，互不干扰

## 📞 支持

- 查看对应版本的README文件获取详细信息
- 提交Issue报告问题
- 查看 OPTIMIZATION_SUMMARY.md 了解v2.0优化详情

---

**推荐使用 v2.0 版本获得最佳体验！** 🚀
