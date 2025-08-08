#!/usr/bin/env python3
"""
Streamlit GUI界面
增强版Web界面，支持所有功能模块
"""

import streamlit as st
import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root / "src"))

from core.agent import JarvisAgent

class StreamlitGUI:
    """Streamlit GUI界面类"""
    
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="Jarvis AI Agent v2.0",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def initialize_session_state(self):
        """初始化会话状态"""
        if 'jarvis_agent' not in st.session_state:
            st.session_state.jarvis_agent = None
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        if 'command_history' not in st.session_state:
            st.session_state.command_history = []
    
    def run(self):
        """运行GUI界面"""
        # 标题和描述
        st.title("🤖 Jarvis AI Agent v2.0")
        st.markdown("**智能助手 - 支持浏览器自动化、API调用、代码执行**")
        
        # 侧边栏
        self.render_sidebar()
        
        # 主界面
        self.render_main_interface()
    
    def render_sidebar(self):
        """渲染侧边栏"""
        with st.sidebar:
            st.header("🎛️ 控制面板")
            
            # Agent状态
            if st.session_state.jarvis_agent is None:
                if st.button("🚀 启动 Jarvis Agent", type="primary"):
                    with st.spinner("正在启动 Jarvis Agent..."):
                        try:
                            st.session_state.jarvis_agent = JarvisAgent()
                            st.success("✅ Jarvis Agent 启动成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ 启动失败: {e}")
            else:
                st.success("✅ Jarvis Agent 已启动")
                if st.button("🔄 重启 Agent"):
                    st.session_state.jarvis_agent.close()
                    st.session_state.jarvis_agent = None
                    st.rerun()
                
                if st.button("🛑 关闭 Agent"):
                    st.session_state.jarvis_agent.close()
                    st.session_state.jarvis_agent = None
                    st.success("👋 Agent 已关闭")
                    st.rerun()
            
            st.divider()
            
            # 配置信息
            if st.session_state.jarvis_agent:
                st.subheader("📊 系统状态")
                config = st.session_state.jarvis_agent.config
                
                # API状态
                st.write("**API服务状态:**")
                for service, status in config.api_status.items():
                    icon = "✅" if status else "❌"
                    st.write(f"{icon} {service.upper()}")
                
                # 浏览器状态
                browser_status = "✅ 已启动" if st.session_state.jarvis_agent.driver else "❌ 未启动"
                st.write(f"**浏览器状态:** {browser_status}")
            
            st.divider()
            
            # 日志查看
            st.subheader("📋 最近日志")
            if st.session_state.jarvis_agent:
                recent_logs = st.session_state.jarvis_agent.logger.get_recent_logs(lines=5)
                for log in recent_logs[-5:]:
                    st.text(log.strip())
    
    def render_main_interface(self):
        """渲染主界面"""
        if st.session_state.jarvis_agent is None:
            st.info("👆 请先在侧边栏启动 Jarvis Agent")
            return
        
        # 创建标签页
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌐 浏览器操作", "🔌 API调用", "💻 代码执行", "📸 截图管理", "📊 系统监控"
        ])
        
        with tab1:
            self.render_browser_tab()
        
        with tab2:
            self.render_api_tab()
        
        with tab3:
            self.render_code_tab()
        
        with tab4:
            self.render_screenshot_tab()
        
        with tab5:
            self.render_monitoring_tab()
    
    def render_browser_tab(self):
        """渲染浏览器操作标签页"""
        st.header("🌐 浏览器自动化")
        
        # 浏览器配置选项
        with st.expander("🔧 浏览器配置", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                use_local_profile = st.checkbox("使用本地浏览器配置", value=True, 
                                              help="使用您本地浏览器的配置文件、扩展和设置")
                headless_mode = st.checkbox("无头模式", value=False,
                                          help="在后台运行浏览器，不显示窗口")
            
            with col2:
                browser_type = st.selectbox("浏览器类型", ["auto", "Chrome", "Edge"], 
                                          help="选择要使用的浏览器类型")
                profile_name = st.text_input("配置文件名", value="Default",
                                           help="浏览器配置文件名称")
            
            # 显示浏览器配置文件信息
            if st.button("🔍 检测浏览器配置"):
                if st.session_state.jarvis_agent:
                    result = st.session_state.jarvis_agent.execute_command("browser_list_profiles")
                    if result.get("success"):
                        st.success("✅ 浏览器配置检测成功")
                        
                        browsers = result.get("browsers", {})
                        recommended = result.get("recommended")
                        
                        if recommended:
                            st.info(f"🎯 推荐配置: {recommended['browser']} - {recommended['profile']}")
                        
                        for browser_name, profiles in browsers.items():
                            st.write(f"**{browser_name}:**")
                            for profile, info in profiles.items():
                                st.write(f"  - {profile}: {info['extensions_count']} 个现有扩展, "
                                       f"{info['size_mb']} MB")
                    else:
                        st.error(f"❌ 检测失败: {result.get('error')}")
        
        # 浏览器控制
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            url = st.text_input("🔗 网址", placeholder="https://www.example.com")
        
        with col2:
            if st.button("🚀 启动浏览器"):
                if st.session_state.jarvis_agent:
                    # 使用配置选项启动浏览器
                    success = st.session_state.jarvis_agent.setup_browser(
                        headless=headless_mode,
                        use_local_profile=use_local_profile,
                        browser_type=browser_type,
                        profile_name=profile_name
                    )
                    if success:
                        st.success("✅ 浏览器启动成功")
                        if use_local_profile:
                            st.info("💡 已使用您的本地配置，包括所有现有扩展和设置")
                        st.rerun()
                    else:
                        st.error("❌ 浏览器启动失败")
        
        with col3:
            if st.button("🌐 访问网页", disabled=not url):
                result = st.session_state.jarvis_agent.execute_command(
                    "browser_navigate", url=url
                )
                self.display_result(result)
        
        # 显示本地配置优势
        if use_local_profile:
            st.info("🎯 **使用本地配置的优势:**\n"
                   "- 保持您的登录状态\n"
                   "- 使用您已安装的所有扩展\n"
                   "- 保留您的书签和设置\n"
                   "- 无需重新配置任何内容")
        
        # 扩展信息显示
        if st.session_state.jarvis_agent and st.session_state.jarvis_agent.driver:
            with st.expander("🧩 当前浏览器扩展", expanded=False):
                if st.button("📋 查看扩展列表"):
                    result = st.session_state.jarvis_agent.execute_command(
                        "browser_get_extensions", 
                        browser_type=browser_type,
                        profile_name=profile_name
                    )
                    if result.get("success"):
                        extensions = result.get("extensions", [])
                        if extensions:
                            st.write(f"**当前使用的 {len(extensions)} 个扩展:**")
                            for ext in extensions:
                                st.write(f"- **{ext['name']}** (v{ext['version']})")
                                if ext['description']:
                                    st.caption(ext['description'][:100] + "..." if len(ext['description']) > 100 else ext['description'])
                        else:
                            st.info("当前配置文件中没有扩展")
                    else:
                        st.error(f"获取扩展失败: {result.get('error')}")
        
        # 快速操作按钮
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📸 截图"):
                result = st.session_state.jarvis_agent.execute_command(
                    "browser_screenshot", description="手动截图"
                )
                self.display_result(result)
        
        with col2:
            if st.button("🔄 刷新页面"):
                if st.session_state.jarvis_agent and st.session_state.jarvis_agent.driver:
                    try:
                        st.session_state.jarvis_agent.driver.refresh()
                        st.success("✅ 页面已刷新")
                    except Exception as e:
                        st.error(f"❌ 刷新失败: {e}")
        
        with col3:
            if st.button("📊 页面信息"):
                result = st.session_state.jarvis_agent.execute_command("browser_get_page_info")
                self.display_result(result)
        
        st.divider()
        
        # 元素操作
        st.subheader("🎯 元素操作")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**点击元素**")
            click_selector = st.text_input("选择器", key="click_selector")
            click_by = st.selectbox("选择方式", ["css", "xpath", "id", "class"], key="click_by")
            if st.button("👆 点击", disabled=not click_selector):
                result = st.session_state.jarvis_agent.execute_command(
                    "browser_click", selector=click_selector, by=click_by
                )
                self.display_result(result)
        
        with col2:
            st.write("**输入文本**")
            input_selector = st.text_input("选择器", key="input_selector")
            input_text = st.text_input("输入内容", key="input_text")
            if st.button("⌨️ 输入", disabled=not (input_selector and input_text)):
                result = st.session_state.jarvis_agent.execute_command(
                    "browser_input", selector=input_selector, text=input_text
                )
                self.display_result(result)
        
        # Google搜索
        st.divider()
        st.subheader("🔍 Google搜索")
        search_query = st.text_input("搜索关键词")
        if st.button("🔍 搜索", disabled=not search_query):
            result = st.session_state.jarvis_agent.execute_command(
                "browser_search_google", query=search_query
            )
            self.display_result(result)
            
            if result.get("success") and result.get("results"):
                st.write("**搜索结果:**")
                for i, item in enumerate(result["results"][:5], 1):
                    with st.expander(f"{i}. {item['title']}"):
                        st.write(f"**链接:** {item['url']}")
                        st.write(f"**摘要:** {item['snippet']}")
    
    def render_api_tab(self):
        """渲染API调用标签页"""
        st.header("🔌 API调用")
        
        # API选择
        api_type = st.selectbox("选择API类型", [
            "OpenAI聊天", "Google搜索", "GitHub搜索", "天气查询", "通用HTTP请求", "连接测试"
        ])
        
        if api_type == "OpenAI聊天":
            message = st.text_area("消息内容", height=100)
            model = st.selectbox("模型", ["gpt-3.5-turbo", "gpt-4"])
            if st.button("💬 发送消息", disabled=not message):
                result = st.session_state.jarvis_agent.execute_command(
                    "api_openai_chat", message=message, model=model
                )
                self.display_result(result)
        
        elif api_type == "Google搜索":
            query = st.text_input("搜索关键词")
            num_results = st.slider("结果数量", 1, 10, 5)
            if st.button("🔍 搜索", disabled=not query):
                result = st.session_state.jarvis_agent.execute_command(
                    "api_google_search", query=query, num_results=num_results
                )
                self.display_result(result)
        
        elif api_type == "GitHub搜索":
            query = st.text_input("搜索关键词")
            search_type = st.selectbox("搜索类型", ["repositories", "users", "issues"])
            if st.button("🔍 搜索", disabled=not query):
                result = st.session_state.jarvis_agent.execute_command(
                    "api_github_search", query=query, search_type=search_type
                )
                self.display_result(result)
        
        elif api_type == "天气查询":
            city = st.text_input("城市名称", value="Beijing")
            if st.button("🌤️ 查询天气", disabled=not city):
                result = st.session_state.jarvis_agent.execute_command(
                    "api_weather", city=city
                )
                self.display_result(result)
        
        elif api_type == "通用HTTP请求":
            url = st.text_input("请求URL")
            method = st.selectbox("请求方法", ["GET", "POST", "PUT", "DELETE"])
            headers = st.text_area("请求头 (JSON格式)", value="{}")
            if st.button("🌐 发送请求", disabled=not url):
                try:
                    headers_dict = json.loads(headers) if headers.strip() else {}
                    result = st.session_state.jarvis_agent.execute_command(
                        "api_generic_request", url=url, method=method, headers=headers_dict
                    )
                    self.display_result(result)
                except json.JSONDecodeError:
                    st.error("请求头JSON格式错误")
        
        elif api_type == "连接测试":
            if st.button("🔗 测试连接"):
                result = st.session_state.jarvis_agent.execute_command("api_test_connection")
                self.display_result(result)
    
    def render_code_tab(self):
        """渲染代码执行标签页"""
        st.header("💻 代码执行")
        
        # 代码类型选择
        code_type = st.selectbox("选择操作类型", [
            "Python代码执行", "Shell命令", "文件读取", "文件写入", "目录列表", "包安装"
        ])
        
        if code_type == "Python代码执行":
            code = st.text_area("Python代码", height=200, value="print('Hello, Jarvis!')")
            timeout = st.slider("超时时间(秒)", 5, 300, 30)
            if st.button("▶️ 执行代码", disabled=not code):
                result = st.session_state.jarvis_agent.execute_command(
                    "code_execute_python", code=code, timeout=timeout
                )
                self.display_result(result)
        
        elif code_type == "Shell命令":
            command = st.text_input("Shell命令", placeholder="ls -la")
            timeout = st.slider("超时时间(秒)", 5, 300, 30)
            if st.button("▶️ 执行命令", disabled=not command):
                result = st.session_state.jarvis_agent.execute_command(
                    "code_execute_shell", command=command, timeout=timeout
                )
                self.display_result(result)
        
        elif code_type == "文件读取":
            filepath = st.text_input("文件路径")
            encoding = st.selectbox("编码格式", ["utf-8", "gbk", "ascii"])
            if st.button("📖 读取文件", disabled=not filepath):
                result = st.session_state.jarvis_agent.execute_command(
                    "code_read_file", filepath=filepath, encoding=encoding
                )
                self.display_result(result)
        
        elif code_type == "文件写入":
            filepath = st.text_input("文件路径")
            content = st.text_area("文件内容", height=200)
            if st.button("💾 写入文件", disabled=not (filepath and content)):
                result = st.session_state.jarvis_agent.execute_command(
                    "code_write_file", filepath=filepath, content=content
                )
                self.display_result(result)
        
        elif code_type == "目录列表":
            dirpath = st.text_input("目录路径", value=".")
            pattern = st.text_input("文件模式", value="*")
            if st.button("📁 列出目录"):
                result = st.session_state.jarvis_agent.execute_command(
                    "code_list_directory", dirpath=dirpath, pattern=pattern
                )
                self.display_result(result)
        
        elif code_type == "包安装":
            package = st.text_input("包名称", placeholder="requests")
            if st.button("📦 安装包", disabled=not package):
                result = st.session_state.jarvis_agent.execute_command(
                    "code_install_package", package=package
                )
                self.display_result(result)
    
    def render_screenshot_tab(self):
        """渲染截图管理标签页"""
        st.header("📸 截图管理")
        
        if st.session_state.jarvis_agent:
            screenshots_dir = st.session_state.jarvis_agent.config.logs_dir / "screenshots"
            
            if screenshots_dir.exists():
                # 获取截图文件
                screenshot_files = list(screenshots_dir.glob("*.png"))
                screenshot_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                if screenshot_files:
                    st.write(f"**共找到 {len(screenshot_files)} 张截图**")
                    
                    # 分页显示
                    items_per_page = 6
                    total_pages = (len(screenshot_files) + items_per_page - 1) // items_per_page
                    
                    if total_pages > 1:
                        page = st.selectbox("选择页面", range(1, total_pages + 1)) - 1
                    else:
                        page = 0
                    
                    start_idx = page * items_per_page
                    end_idx = min(start_idx + items_per_page, len(screenshot_files))
                    
                    # 显示截图
                    cols = st.columns(3)
                    for i, screenshot_file in enumerate(screenshot_files[start_idx:end_idx]):
                        col_idx = i % 3
                        with cols[col_idx]:
                            st.image(str(screenshot_file), caption=screenshot_file.name, use_column_width=True)
                            
                            # 文件信息
                            file_stat = screenshot_file.stat()
                            st.caption(f"大小: {file_stat.st_size / 1024:.1f} KB")
                            st.caption(f"时间: {datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    st.info("暂无截图文件")
            else:
                st.info("截图目录不存在")
    
    def render_monitoring_tab(self):
        """渲染系统监控标签页"""
        st.header("📊 系统监控")
        
        if st.session_state.jarvis_agent:
            config = st.session_state.jarvis_agent.config
            
            # 配置信息
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("⚙️ 配置信息")
                st.json({
                    "浏览器配置": config.browser_config,
                    "日志配置": config.logging_config,
                    "API配置": config.api_config
                })
            
            with col2:
                st.subheader("📈 运行状态")
                
                # 日志统计
                logs_dir = config.logs_dir
                log_stats = {}
                
                for log_type in ["debug", "info", "error"]:
                    log_file = logs_dir / log_type / f"{log_type}.log"
                    if log_file.exists():
                        log_stats[log_type] = log_file.stat().st_size
                    else:
                        log_stats[log_type] = 0
                
                st.write("**日志文件大小:**")
                for log_type, size in log_stats.items():
                    st.write(f"- {log_type}: {size / 1024:.1f} KB")
                
                # 截图统计
                screenshots_dir = logs_dir / "screenshots"
                if screenshots_dir.exists():
                    screenshot_count = len(list(screenshots_dir.glob("*.png")))
                    st.write(f"**截图数量:** {screenshot_count}")
            
            # 最近日志
            st.subheader("📋 最近日志")
            log_level = st.selectbox("日志级别", ["info", "debug", "error"])
            log_lines = st.slider("显示行数", 10, 100, 20)
            
            recent_logs = st.session_state.jarvis_agent.logger.get_recent_logs(log_level, log_lines)
            if recent_logs:
                log_text = "".join(recent_logs)
                st.text_area("日志内容", value=log_text, height=300)
            else:
                st.info(f"暂无{log_level}级别的日志")
    
    def display_result(self, result: dict):
        """显示执行结果"""
        if result.get("success"):
            st.success("✅ 执行成功")
            
            # 显示结果详情
            if "message" in result:
                st.info(result["message"])
            
            # 显示其他信息
            display_data = {k: v for k, v in result.items() 
                          if k not in ["success", "message"] and v is not None}
            
            if display_data:
                with st.expander("📋 详细结果", expanded=True):
                    st.json(display_data)
        else:
            st.error(f"❌ 执行失败: {result.get('error', '未知错误')}")
        
        # 添加到日志
        st.session_state.logs.append({
            "timestamp": datetime.now().isoformat(),
            "result": result
        })

def main():
    """主函数"""
    gui = StreamlitGUI()
    gui.run()

if __name__ == "__main__":
    main()
