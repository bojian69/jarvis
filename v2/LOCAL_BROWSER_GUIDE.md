# 🌐 本地浏览器配置使用指南

## 📋 概述

Jarvis AI Agent v2.0 现在支持使用您本地浏览器的配置文件，这意味着：

- ✅ **保持登录状态** - 无需重新登录各种网站
- ✅ **使用现有扩展** - 您已安装的所有扩展都会正常工作
- ✅ **保留个人设置** - 书签、主题、偏好设置等都保持不变
- ✅ **无需安装任何新扩展** - 直接使用您现有的配置

## 🚀 快速开始

### 1. 使用 Web 界面

```bash
# 启动 Web 界面
cd v2
python run.py --gui
```

在浏览器中访问显示的地址，然后：

1. 在侧边栏启动 Jarvis Agent
2. 进入"🌐 浏览器操作"标签页
3. 在"🔧 浏览器配置"中：
   - ✅ 勾选"使用本地浏览器配置"
   - 选择浏览器类型（推荐"auto"）
   - 点击"🚀 启动浏览器"

### 2. 使用命令行界面

```bash
# 启动命令行界面
cd v2
python run.py --cli

# 在命令行中执行
jarvis> browser setup --local
jarvis> browser navigate https://www.google.com
```

### 3. 使用编程接口

```python
from src.core.agent import JarvisAgent

with JarvisAgent() as agent:
    # 启动浏览器，使用本地配置
    agent.setup_browser(
        headless=False,  # 显示浏览器窗口
        use_local_profile=True,  # 使用本地配置
        browser_type="auto"  # 自动选择最佳配置
    )
    
    # 访问网页
    result = agent.execute_command("browser_navigate", url="https://www.google.com")
```

## 🔍 检测浏览器配置

### 查看可用配置

```bash
# 命令行方式
jarvis> browser profiles

# 或者运行检测脚本
python -c "
from src.utils.browser_profiles import BrowserProfileDetector
detector = BrowserProfileDetector()
browsers = detector.get_available_browsers()
for name, profiles in browsers.items():
    print(f'{name}: {list(profiles.keys())}')
"
```

### 查看扩展信息

```bash
# 命令行方式
jarvis> browser extensions Chrome Default

# 或者在 Web 界面中点击"📋 查看扩展列表"
```

## 🎯 使用场景

### 1. 保持登录状态进行自动化

```python
# 启动使用本地配置的浏览器
agent.setup_browser(use_local_profile=True)

# 访问需要登录的网站，您已经是登录状态
agent.execute_command("browser_navigate", url="https://github.com")

# 直接进行操作，无需登录
agent.execute_command("browser_click", selector="[data-testid='header-search-button']")
```

### 2. 使用现有扩展功能

如果您安装了广告拦截器、密码管理器等扩展，它们都会正常工作：

```python
# 浏览器启动时会自动加载您的所有扩展
agent.setup_browser(use_local_profile=True)

# 访问网页时，广告拦截器等扩展会自动工作
agent.execute_command("browser_navigate", url="https://example.com")
```

### 3. 保持个人偏好设置

```python
# 您的主题、语言、搜索引擎等设置都会保持
agent.setup_browser(use_local_profile=True)

# 浏览器外观和行为与您平时使用的完全一致
```

## ⚙️ 配置选项

### 浏览器类型选择

```python
# 自动选择（推荐）
agent.setup_browser(browser_type="auto")

# 指定使用 Chrome
agent.setup_browser(browser_type="Chrome", profile_name="Default")

# 指定使用特定配置文件
agent.setup_browser(browser_type="Chrome", profile_name="Profile 1")
```

### 显示模式选择

```python
# 显示浏览器窗口（推荐用于调试）
agent.setup_browser(headless=False)

# 后台运行（推荐用于自动化脚本）
agent.setup_browser(headless=True)
```

## 🛠️ 故障排除

### 问题1: 浏览器启动失败

**可能原因:**
- Chrome 浏览器未安装
- 浏览器正在运行中
- 配置文件路径问题

**解决方案:**
```bash
# 1. 确保 Chrome 已安装
# 2. 关闭所有 Chrome 窗口
# 3. 尝试使用默认配置
python -c "
from src.core.agent import JarvisAgent
with JarvisAgent() as agent:
    agent.setup_browser(use_local_profile=False)
"
```

### 问题2: 扩展不工作

**可能原因:**
- 扩展需要用户交互
- 扩展版本不兼容

**解决方案:**
- 使用非无头模式查看扩展状态
- 在常规浏览器中更新扩展

### 问题3: 配置文件检测失败

**可能原因:**
- 非标准安装路径
- 权限问题

**解决方案:**
```python
# 手动指定配置文件路径
chrome_options.add_argument("--user-data-dir=/path/to/your/chrome/profile")
```

## 📊 性能对比

| 配置方式 | 启动速度 | 功能完整性 | 登录状态 | 扩展支持 |
|---------|---------|-----------|---------|---------|
| 默认配置 | 快 ⚡ | 基础 | ❌ | ❌ |
| 本地配置 | 中等 🚀 | 完整 ✅ | ✅ | ✅ |

## 💡 最佳实践

### 1. 开发阶段
```python
# 使用非无头模式，便于调试
agent.setup_browser(headless=False, use_local_profile=True)
```

### 2. 生产环境
```python
# 使用无头模式，提高性能
agent.setup_browser(headless=True, use_local_profile=True)
```

### 3. 批量处理
```python
# 启动一次，重复使用
with JarvisAgent() as agent:
    agent.setup_browser(use_local_profile=True)
    
    for url in urls:
        agent.execute_command("browser_navigate", url=url)
        # 处理页面...
```

## 🔒 安全注意事项

1. **隐私保护**: 使用本地配置时，您的浏览历史和 Cookie 会被访问
2. **权限控制**: 确保只在可信环境中使用本地配置
3. **数据备份**: 建议定期备份浏览器配置文件

## 🎉 总结

使用本地浏览器配置让 Jarvis AI Agent 更加强大和便利：

- 🚀 **即开即用** - 无需重新配置任何设置
- 🔐 **保持登录** - 所有网站登录状态都保留
- 🧩 **扩展支持** - 您的所有扩展都正常工作
- ⚡ **高效自动化** - 真正的"本地浏览器"体验

现在就开始使用吧！

```bash
cd v2
python test_local_browser_simple.py
```
