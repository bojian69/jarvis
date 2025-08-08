# 🏠 学生住房功能使用说明

Jarvis智能体现在包含了专门的学生住房网站自动化功能，可以自动打开 `https://wearehomesforstudents.com/agent-booking/xejs-uhomes` 并尝试选择London城市。

## 🚀 使用方法

### 方法1: 控制台模式（推荐）
```bash
# 启动控制台模式
python run.py --mode console

# 在控制台中使用命令
Jarvis> start      # 启动浏览器
Jarvis> housing    # 打开学生住房网站并选择London
Jarvis> screenshot # 截图
Jarvis> quit       # 退出
```

### 方法2: 快速启动脚本
```bash
# 直接运行学生住房功能
python housing.py
```

### 方法3: GUI界面
```bash
# 启动GUI界面
python run.py --mode gui

# 在侧边栏点击 "🏠 学生住房(London)" 按钮
```

### 方法4: CLI模式
```bash
# 启动CLI模式
python run.py --mode cli

# 在交互命令中输入
> housing
```

## 🔧 功能特点

### 自动化操作
- ✅ 自动打开学生住房网站
- ✅ 智能识别城市选择器
- ✅ 自动选择London城市
- ✅ 支持多种页面元素类型（下拉框、输入框、按钮等）

### 容错处理
- 🔄 多种选择器尝试策略
- 🔄 自动重试机制
- 🔄 手动操作回退选项
- 🔄 详细的错误提示

### 页面元素识别
程序会尝试以下类型的城市选择器：
- `select` 下拉选择框
- `input` 输入框（支持自动完成）
- 按钮和链接
- 包含"London"文本的任何元素

## 📋 控制台命令

### 基础命令
- `start` - 启动浏览器
- `close` - 关闭浏览器
- `quit/exit` - 退出程序
- `help` - 显示帮助信息

### 网页操作
- `url <网址>` - 打开指定网址
- `search <关键词>` - Google搜索
- `screenshot` - 截图
- `info` - 显示当前页面信息

### 专用功能
- `housing` - 打开学生住房网站并选择London城市

## 🛠️ 故障排除

### 如果自动选择失败
1. 程序会提示手动操作
2. 在浏览器中手动选择London城市
3. 按回车继续程序执行

### 如果页面加载缓慢
- 程序会等待5秒让页面完全加载
- 如需更长时间，可以手动等待后继续

### 如果找不到城市选择器
- 程序会尝试多种选择器策略
- 最终会回退到手动操作模式

## 📸 截图功能

所有模式都支持截图功能：
- 自动截图：`housing_<timestamp>.png`
- 手动截图：`screenshot_<timestamp>.png`

## 🔍 调试信息

程序会显示详细的执行信息：
- ✅ 成功操作
- ⚠️ 警告信息  
- ❌ 错误信息
- 💡 提示信息

## 📞 技术支持

如果遇到问题：
1. 检查Chrome浏览器是否正确安装
2. 确保网络连接正常
3. 尝试手动操作模式
4. 查看控制台错误信息

## 🎯 使用示例

```bash
# 完整使用流程
$ python run.py --mode console

🤖 Jarvis控制台
==================================================
输入 'help' 查看命令帮助
输入 'start' 启动浏览器
==================================================

Jarvis> start
🚀 正在启动浏览器...
✅ 浏览器启动成功！

Jarvis> housing
🏠 正在打开学生住房网站并选择London城市...
✅ 已打开: https://wearehomesforstudents.com/agent-booking/xejs-uhomes
🔍 正在查找城市筛选器...
✅ 找到城市选择器: select[name='city']
📋 检测到下拉选择框
✅ 通过文本选择了London
✅ 学生住房网站已打开
   当前URL: https://wearehomesforstudents.com/agent-booking/xejs-uhomes
   页面标题: Student Housing - London

Jarvis> screenshot
✅ 截图已保存: screenshot_1691234567.png

Jarvis> quit
👋 再见！
✅ 浏览器已关闭
```
