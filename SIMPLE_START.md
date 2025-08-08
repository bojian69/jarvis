# 🚀 Jarvis AI Agent 简单启动指南

## ✅ 当前状态

- ✅ 项目结构完整
- ✅ 依赖包已安装
- ✅ 浏览器配置检测正常（Chrome + 13个扩展）
- ✅ 本地浏览器配置功能已优化

## 🎯 推荐启动方式

### 方式1: 直接启动v2.0 GUI（最简单）

```bash
cd v2
python start_gui.py
```

然后在浏览器中访问: http://localhost:8501

### 方式2: 使用统一启动脚本

```bash
# 从项目根目录
python run.py --v2 --gui
```

### 方式3: 手动启动Streamlit

```bash
cd v2
python -m streamlit run src/ui/gui.py
```

## 🌟 本地浏览器配置特性

启动GUI后，您可以：

1. **检测浏览器配置**
   - 自动发现Chrome浏览器
   - 显示13个现有扩展
   - 推荐最佳配置

2. **启动本地浏览器**
   - 保持所有登录状态
   - 使用现有扩展
   - 保留个人设置

3. **自动化操作**
   - 网页导航
   - 元素操作
   - 自动截图

## 🧪 快速测试

如果GUI有问题，可以直接测试核心功能：

```bash
cd v2
python test_local_browser_simple.py
```

## 💡 故障排除

### 如果GUI启动失败

1. **检查端口占用**
   ```bash
   lsof -i :8501
   # 如果有进程占用，杀掉它
   pkill -f streamlit
   ```

2. **手动启动**
   ```bash
   cd v2
   export PYTHONPATH=$(pwd)
   python -m streamlit run src/ui/gui.py
   ```

3. **使用简化启动器**
   ```bash
   cd v2
   python start_gui.py
   ```

### 如果浏览器检测失败

```bash
cd v2
python -c "
from src.utils.browser_profiles import BrowserProfileDetector
detector = BrowserProfileDetector()
browsers = detector.get_available_browsers()
print('检测结果:', browsers)
"
```

## 🎉 开始使用

**推荐命令:**
```bash
cd v2
python start_gui.py
```

然后：
1. 在浏览器中打开 http://localhost:8501
2. 点击侧边栏的"🚀 启动 Jarvis Agent"
3. 进入"🌐 浏览器操作"标签页
4. 确保"使用本地浏览器配置"已勾选
5. 点击"🚀 启动浏览器"
6. 享受本地浏览器自动化！

**您将看到:**
- 🔍 自动检测到Chrome配置
- 🧩 显示13个现有扩展
- 🔐 保持所有登录状态
- ⚡ 真正的本地浏览器体验

立即开始体验吧！🚀
