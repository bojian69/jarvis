# 🤖 Jarvis AI机器人

一个具备语音识别、AI对话和浏览器控制功能的实体机器人项目。支持OpenAI GPT集成和完整的日志系统。

## 功能特性
- 🎤 **语音识别** - 支持中文语音输入
- 💬 **Web界面** - 现代化的聊天界面
- 🌐 **浏览器控制** - 语音命令打开浏览器
- 🤖 **AI智能回复** - 集成OpenAI GPT
- 📈 **日志系统** - 完整的操作日志
- 🔊 **语音合成** - TTS语音输出

## 硬件材料

### 基础版本
- **树莓派 4B** (4GB+) - 主控制器
- **USB麦克风** - 语音输入
- **小音箱** - 语音输出
- **5V 3A电源** - 供电
- **MicroSD卡** (32GB+) - 存储

### 可选配件
- 摄像头模块 - 视觉交互
- LED指示灯 - 状态显示
- 亚克力外壳 - 保护和美观

**预算成本：约￥500-850**

## 安装指南

### 1. 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd jarvis

# 给脚本执行权限
chmod +x setup.sh start.sh
```

### 2. 安装依赖
```bash
# 自动安装所有依赖
./setup.sh

# 或手动安装
brew install portaudio  # macOS
pip3 install -r requirements.txt
```

### 3. 配置设置
编辑 `config.py` 文件：
```python
# AI配置
OPENAI_API_KEY = "your-openai-api-key"  # 可选

# 服务器配置
HOST = "0.0.0.0"
PORT = 8080

# 浏览器默认页面
DEFAULT_URL = "https://www.google.com"
```

## 使用方法

### 启动服务
```bash
# 方式1：使用启动脚本
./start.sh

# 方式2：直接运行
~/.pyenv/shims/python3 jarvis_simple.py

# 方式3：完整版本（需要麦克风）
python3 jarvis_robot.py
```

### 访问界面
打开浏览器访问：`http://localhost:8080`

### 使用功能
1. **文本聊天** - 在输入框中输入消息
2. **语音交互** - 点击🎤按钮进行语音输入
3. **浏览器控制** - 说“打开浏览器”

## 项目结构
```
jarvis/
├── jarvis_simple.py    # 简化版本（推荐）
├── jarvis_robot.py     # 完整版本
├── config.py           # 配置文件
├── requirements.txt    # Python依赖
├── setup.sh           # 安装脚本
├── start.sh           # 启动脚本
├── jarvis.log         # 日志文件
├── templates/
│   └── index.html      # Web界面
└── README.md          # 项目说明
```

## 安全注意事项

⚠️ **重要安全提示**：

1. **API密钥安全**
   - 不要将OpenAI API Key提交到版本控制
   - 使用环境变量存储敏感信息
   - 定期轮换API密钥

2. **生产环境**
   - 关闭调试模式
   - 使用HTTPS加密
   - 配置防火墙规则

3. **输入验证**
   - 用户输入已做基础清理
   - 日志记录可能存在注入风险

## 故障排除

### 常见问题

**1. 端口被占用**
```bash
# 查看端口占用
lsof -i :8080
# 终止进程
kill -9 <PID>
```

**2. 麦克风权限问题**
- macOS: 系统偏好设置 > 安全性与隐私 > 麦克风
- 添加终端应用权限

**3. OpenAI API错误**
- 检查API Key是否有效
- 确认账户余额充足
- 检查网络连接

### 日志查看
```bash
# 实时查看日志
tail -f jarvis.log

# 查看错误日志
grep "ERROR" jarvis.log
```

## 开发计划

- [ ] 支持更多语音命令
- [ ] 添加智能家居控制
- [ ] 集成更多AI模型
- [ ] 移动端App开发
- [ ] 语音识别精度优化

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License - 详见LICENSE文件

## 联系方式

如有问题请提交Issue或联系开发者。
