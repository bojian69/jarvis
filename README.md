# 🤖 Jarvis AI Agent

一个智能AI助手，支持浏览器自动化操作、第三方API调用、Python代码执行等功能。**无需API密钥即可使用核心功能！**

## ✨ 主要功能

### 🆓 核心功能（无需API密钥）
- 🌐 **浏览器操作**: 使用真实Chrome浏览器，避免反机器人检测
- 🔍 **智能搜索**: Google搜索及网页浏览
- 📸 **网页截图**: 保存当前页面截图
- 🐍 **Python执行**: 内嵌Python代码执行环境
- 🔌 **通用API**: 调用各种公开API
- 🛡️ **人工干预**: 支持验证码等人工处理

### 🔑 高级功能（需要API密钥）
- 🤖 **AI对话**: OpenAI GPT模型对话
- 🌤️ **天气查询**: 实时天气信息
- 🔍 **Google API**: 高级搜索功能

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Volumes/bojian/github-bojian/jarvis
python run.py --install
```

### 2. 检查环境

```bash
python run.py --check
```

### 3. 启动应用

**GUI模式 (推荐):**
```bash
python run.py --mode gui
```

**命令行模式:**
```bash
python run.py --mode cli
```

## 📋 无API密钥快速体验

即使没有配置任何API密钥，你也可以立即使用以下功能：

1. **启动浏览器**: 自动打开Chrome浏览器
2. **网页浏览**: 访问任何网站
3. **Google搜索**: 直接在Google上搜索
4. **截图功能**: 保存网页截图
5. **Python代码**: 执行Python代码片段
6. **公开API**: 调用GitHub、天气等公开API

```bash
# 立即开始体验
python run.py --mode gui
```

## 🔧 API密钥配置（可选）

如果你想使用AI对话等高级功能，可以配置相应的API密钥：

### OpenAI API Key
- **获取地址**: https://platform.openai.com/api-keys
- **用途**: AI对话功能
- **配置**: 在`.env`文件中设置`OPENAI_API_KEY`

### Google API Key
- **获取地址**: https://console.cloud.google.com/apis/credentials
- **用途**: Google服务调用
- **配置**: 在`.env`文件中设置`GOOGLE_API_KEY`

### 配置步骤
1. 复制`.env.example`为`.env`
2. 编辑`.env`文件，填入你的API密钥
3. 重启应用即可使用高级功能

## 📁 项目结构

```
jarvis/
├── main.py              # 主程序入口
├── gui.py               # Streamlit GUI界面
├── run.py               # 启动脚本
├── browser_tools.py     # 浏览器操作工具
├── api_tools.py         # API调用工具
├── requirements.txt     # 项目依赖
├── .env                 # 环境变量配置
├── .env.example         # 配置示例
└── README.md           # 项目说明
```

## 💡 使用示例

### 浏览器自动化（无需API密钥）

```python
from main import JarvisAgent

jarvis = JarvisAgent()

# 打开网页
jarvis.open_url("https://www.google.com")

# Google搜索
jarvis.search_google("Python AI开发")

# 截图
jarvis.take_screenshot("search_result.png")

# 等待人工操作
jarvis.wait_for_manual_action("请处理验证码后按回车...")

jarvis.close()
```

### API调用（无需API密钥）

```python
from api_tools import APITools

api = APITools()

# 调用GitHub公开API
result = api.get("https://api.github.com/users/octocat")
print(f"用户: {result['name']}")

# 测试各种公开API
api.call_public_api_examples()
```

### Python代码执行（无需API密钥）

```python
code = """
import datetime
import math

print(f"当前时间: {datetime.datetime.now()}")
print(f"圆周率: {math.pi:.6f}")

# 简单计算
numbers = [1, 2, 3, 4, 5]
print(f"总和: {sum(numbers)}")
"""

jarvis.execute_python_code(code)
```

## 🛡️ 安全特性

- **真实浏览器**: 使用undetected-chromedriver避免检测
- **用户数据目录**: 保持登录状态和用户偏好
- **人工干预**: 支持验证码等人工处理
- **安全执行**: Python代码在受控环境中执行
- **隐私保护**: API密钥本地存储，不会上传

## 🔍 常见问题

### Q: 没有API密钥可以使用吗？
A: **可以！** 浏览器自动化、网页搜索、截图、Python执行等核心功能都无需API密钥。

### Q: 浏览器启动失败？
A: 请确保已安装Google Chrome浏览器，并运行 `python run.py --setup` 检查配置。

### Q: 被网站检测为机器人？
A: 项目使用真实Chrome浏览器和undetected-chromedriver来避免检测，如遇到验证码可以手动处理。

### Q: 如何添加新的API？
A: 在`api_tools.py`中添加新的API调用方法，参考现有的API调用示例。

## 🚀 进阶使用

### 自定义浏览器选项
```python
# 在main.py中修改Chrome选项
options.add_argument("--window-size=1920,1080")  # 设置窗口大小
options.add_argument("--start-maximized")        # 最大化窗口
```

### 添加新的API服务
```python
# 在api_tools.py中添加
def call_custom_api(self, endpoint):
    """调用自定义API"""
    return self.get(f"https://api.example.com/{endpoint}")
```

### 扩展Python执行环境
```python
# 在main.py中的execute_python_code方法中添加更多模块
import requests
safe_globals.update({'requests': requests})
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

MIT License

## 🙏 致谢

- [Selenium](https://selenium.dev/) - 浏览器自动化
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) - 反检测Chrome驱动
- [Streamlit](https://streamlit.io/) - Web界面框架
- [Requests](https://requests.readthedocs.io/) - HTTP库
