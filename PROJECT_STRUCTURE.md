# 📁 Jarvis AI Agent 项目结构说明

## 🏗️ 整体架构

项目采用版本分离的架构设计，将不同版本的代码完全分离，便于维护和选择使用。

```
jarvis/
├── 📁 v1/                     # v1.0 原始版本
├── 📁 v2/                     # v2.0 优化版本
├── 📄 run.py                  # 统一运行脚本
├── 📄 demo.py                 # 统一演示脚本
├── 📄 README.md               # 项目说明
├── 📄 PROJECT_STRUCTURE.md    # 本文件
├── 📄 OPTIMIZATION_SUMMARY.md # 优化总结
├── 📄 .env                    # 环境变量配置
└── 📄 .gitignore             # Git忽略文件
```

## 📂 v1.0 版本结构 (原始版本)

```
v1/
├── 📄 main.py                 # 主程序文件
├── 📄 run.py                  # v1运行脚本
├── 📄 gui.py                  # Streamlit Web界面
├── 📄 api_tools.py            # API调用工具
├── 📄 browser_tools.py        # 浏览器操作工具
├── 📄 console.py              # 控制台界面
├── 📄 housing.py              # 房产相关功能
├── 📄 requirements.txt        # v1依赖包
├── 📄 README.md               # v1说明文档
└── 📄 *.py                    # 其他辅助文件
```

### v1.0 特点
- **单文件架构**: 功能集中在几个大文件中
- **基础功能**: 浏览器自动化、API调用、Web界面
- **简单配置**: 主要依赖环境变量
- **适用场景**: 快速上手、学习使用

## 📂 v2.0 版本结构 (优化版本)

```
v2/
├── 📁 src/                    # 源代码目录
│   ├── 📁 core/              # 核心模块
│   │   ├── 📄 __init__.py
│   │   ├── 📄 agent.py       # 主代理类
│   │   ├── 📄 config.py      # 配置管理
│   │   ├── 📄 logger.py      # 日志系统
│   │   └── 📄 middleware.py  # 中间件系统
│   ├── 📁 modules/           # 功能模块
│   │   ├── 📄 __init__.py
│   │   ├── 📄 browser.py     # 浏览器操作
│   │   ├── 📄 api.py         # API调用
│   │   └── 📄 code.py        # 代码执行
│   └── 📁 ui/                # 用户界面
│       ├── 📄 __init__.py
│       ├── 📄 gui.py         # Web界面
│       └── 📄 cli.py         # 命令行界面
├── 📁 logs/                  # 日志目录
│   ├── 📁 screenshots/       # 截图文件
│   ├── 📁 debug/            # 调试日志
│   ├── 📁 info/             # 信息日志
│   └── 📁 error/            # 错误日志
├── 📁 config/               # 配置文件
│   └── 📄 settings.json     # 主配置文件
├── 📄 main.py              # 主入口文件
├── 📄 run.py               # v2运行脚本
├── 📄 demo.py              # 功能演示
├── 📄 test.py              # 架构测试
├── 📄 requirements.txt     # v2依赖包
├── 📄 README.md            # v2说明文档
└── 📄 README_DETAILED.md   # 详细文档
```

### v2.0 特点
- **模块化架构**: 清晰的代码分离和组织
- **中间件系统**: 可插拔的功能扩展
- **增强日志**: 多级别日志和自动截图
- **配置管理**: JSON配置文件 + 环境变量
- **多种界面**: Web界面 + 命令行界面
- **适用场景**: 生产环境、功能扩展、团队开发

## 🚀 统一入口脚本

### run.py (根目录)
统一的运行脚本，支持选择版本和功能：

```bash
# 使用v2.0版本 (推荐)
python run.py --v2 --gui        # Web界面
python run.py --v2 --cli        # 命令行界面
python run.py --v2 --install    # 安装依赖

# 使用v1.0版本
python run.py --v1 --gui        # Web界面
python run.py --v1 --install    # 安装依赖

# 查看状态
python run.py --status          # 项目状态
```

### demo.py (根目录)
统一的演示脚本：

```bash
python demo.py                  # 交互式选择
python demo.py --v2             # v2.0演示
python demo.py --v1             # v1.0演示
python demo.py --compare        # 版本对比
```

## 📋 配置文件说明

### .env (根目录)
环境变量配置，两个版本共享：

```bash
# API密钥配置
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
```

### v2/config/settings.json
v2.0版本的详细配置：

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

## 🔄 版本选择指南

### 选择 v1.0 的情况
- ✅ 快速上手和学习
- ✅ 简单的自动化任务
- ✅ 不需要复杂的日志和配置
- ✅ 单人使用

### 选择 v2.0 的情况 (推荐)
- ✅ 生产环境使用
- ✅ 需要详细的日志记录
- ✅ 功能扩展和定制
- ✅ 团队协作开发
- ✅ 复杂的自动化流程

## 🛠️ 开发指南

### 在v1.0基础上开发
1. 进入v1目录：`cd v1`
2. 修改对应的功能文件
3. 测试：`python run.py --gui`

### 在v2.0基础上开发
1. 进入v2目录：`cd v2`
2. 在对应模块中添加功能
3. 测试：`python test.py`
4. 演示：`python demo.py`

### 添加新功能模块 (v2.0)
1. 在 `src/modules/` 下创建新模块
2. 实现 `execute_command` 方法
3. 在 `src/core/agent.py` 中注册

### 添加新中间件 (v2.0)
1. 在 `src/core/middleware.py` 中创建新类
2. 继承 `Middleware` 基类
3. 实现必要的方法

## 📊 目录大小和文件统计

### v1.0 版本
- 文件数量: ~15个Python文件
- 代码行数: ~2000行
- 主要文件: main.py, gui.py, api_tools.py

### v2.0 版本
- 文件数量: ~20个Python文件
- 代码行数: ~3000行
- 模块数量: 3个核心模块 + 3个功能模块

## 🔧 维护说明

### 依赖管理
- v1.0: `v1/requirements.txt`
- v2.0: `v2/requirements.txt`
- 分别管理，避免冲突

### 日志管理
- v1.0: 基础日志输出
- v2.0: `v2/logs/` 目录下分类存储

### 配置管理
- 共享: `.env` 环境变量
- v2.0专用: `v2/config/settings.json`

## 🚀 未来规划

### 短期计划
- [ ] 完善v2.0的测试覆盖
- [ ] 添加更多中间件
- [ ] 优化性能和内存使用

### 长期计划
- [ ] 考虑v3.0异步架构
- [ ] 添加插件系统
- [ ] 支持分布式部署

---

这个项目结构设计确保了：
- **版本隔离**: 不同版本互不干扰
- **易于选择**: 根据需求选择合适版本
- **便于维护**: 清晰的目录结构
- **扩展友好**: 支持功能扩展和定制
