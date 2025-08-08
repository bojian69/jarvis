# Jarvis AI Agent v2.0 (优化版本)

这是 Jarvis AI Agent 的优化版本，采用模块化架构，支持中间件、增强日志等功能。

## 项目结构

```
v2/
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
├── config/               # 配置文件
├── main.py              # 主入口文件
├── run.py               # 运行脚本
├── demo.py              # 功能演示
└── test.py              # 架构测试
```

## 使用方法

```bash
cd v2
python run.py --install  # 安装依赖
python run.py --check    # 检查环境
python run.py --gui      # 启动Web界面
python run.py --cli      # 启动命令行界面
python demo.py           # 运行功能演示
```

## 主要特性

- 🏗️ 模块化架构
- 🛡️ 中间件系统
- 📋 增强日志系统
- 📸 自动截图记录
- ⚙️ 配置管理系统
- 🖥️ 多种用户界面
