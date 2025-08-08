#!/usr/bin/env python3
"""
Jarvis GUI界面
使用Streamlit创建Web界面，支持无API密钥运行
"""

import streamlit as st
import os
import sys
import time
from main import JarvisAgent, check_api_keys
from api_tools import APITools

# 页面配置
st.set_page_config(
    page_title="Jarvis AI Agent",
    page_icon="🤖",
    layout="wide"
)

# 初始化session state
if 'jarvis' not in st.session_state:
    st.session_state.jarvis = None
if 'api_tools' not in st.session_state:
    st.session_state.api_tools = APITools()
if 'logs' not in st.session_state:
    st.session_state.logs = []

def add_log(message):
    """添加日志"""
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")
    # 只保留最近50条日志
    if len(st.session_state.logs) > 50:
        st.session_state.logs = st.session_state.logs[-50:]

def main():
    st.title("🤖 Jarvis AI Agent")
    st.markdown("智能助手 - 支持浏览器操作、API调用、Python执行")
    st.markdown("---")
    
    # 检查API状态
    api_status = check_api_keys()
    
    # 侧边栏
    with st.sidebar:
        st.header("🎛️ 控制面板")
        
        # API状态显示
        st.subheader("📊 API状态")
        col1, col2 = st.columns(2)
        with col1:
            st.write("OpenAI:", "✅" if api_status['openai'] else "❌")
            st.write("Google:", "✅" if api_status['google'] else "❌")
        with col2:
            st.write("GitHub:", "✅" if api_status['github'] else "❌")
        
        if not any(api_status.values()):
            st.warning("⚠️ 未配置API密钥\n浏览器功能仍可正常使用")
            with st.expander("📝 配置说明"):
                st.markdown("""
                **OpenAI API:**
                - 获取地址: https://platform.openai.com/api-keys
                - 用于AI对话功能
                
                **Google API:**
                - 获取地址: https://console.cloud.google.com/
                - 用于Google服务调用
                
                **配置方法:**
                在项目根目录的 `.env` 文件中添加相应的API密钥
                """)
        
        st.markdown("---")
        
        # 浏览器控制
        st.subheader("🌐 浏览器控制")
        if st.button("🚀 启动浏览器", use_container_width=True):
            if st.session_state.jarvis is None:
                with st.spinner("正在启动浏览器..."):
                    st.session_state.jarvis = JarvisAgent()
                if st.session_state.jarvis.driver:
                    st.success("✅ 浏览器启动成功！")
                    add_log("浏览器启动成功")
                else:
                    st.error("❌ 浏览器启动失败")
                    add_log("浏览器启动失败")
            else:
                st.warning("⚠️ 浏览器已经在运行中")
        
        if st.button("🛑 关闭浏览器", use_container_width=True):
            if st.session_state.jarvis:
                st.session_state.jarvis.close()
                st.session_state.jarvis = None
                st.success("✅ 浏览器已关闭")
                add_log("浏览器已关闭")
            else:
                st.warning("⚠️ 浏览器未启动")
        
        # 快捷网站
        st.subheader("🔗 快捷访问")
        common_sites = {
            "Google": "https://www.google.com",
            "GitHub": "https://github.com",
            "Stack Overflow": "https://stackoverflow.com",
            "ChatGPT": "https://chat.openai.com",
            "百度": "https://www.baidu.com"
        }
        
        for name, url in common_sites.items():
            if st.button(f"🌐 {name}", use_container_width=True):
                if st.session_state.jarvis and st.session_state.jarvis.driver:
                    st.session_state.jarvis.open_url(url)
                    st.success(f"✅ 已打开 {name}")
                    add_log(f"打开网站: {name}")
                else:
                    st.warning("⚠️ 请先启动浏览器")
        
        # 专用功能
        st.subheader("🏠 专用功能")
        if st.button("🏠 学生住房(London)", use_container_width=True):
            if st.session_state.jarvis and st.session_state.jarvis.driver:
                with st.spinner("正在打开学生住房网站并选择London..."):
                    success = st.session_state.jarvis.open_student_housing_london()
                if success:
                    st.success("✅ 已打开学生住房网站并尝试选择London")
                    add_log("打开学生住房网站(London)")
                else:
                    st.error("❌ 打开学生住房网站失败")
            else:
                st.warning("⚠️ 请先启动浏览器")
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 功能操作")
        
        # 网页操作
        with st.expander("🌐 网页操作", expanded=True):
            url_input = st.text_input("🔗 输入URL:", placeholder="https://www.google.com")
            col_url1, col_url2 = st.columns(2)
            
            with col_url1:
                if st.button("🌐 打开网页", use_container_width=True):
                    if st.session_state.jarvis and st.session_state.jarvis.driver and url_input:
                        with st.spinner("正在打开网页..."):
                            success = st.session_state.jarvis.open_url(url_input)
                        if success:
                            st.success(f"✅ 已打开: {url_input}")
                            add_log(f"打开URL: {url_input}")
                        else:
                            st.error("❌ 打开网页失败")
                            add_log(f"打开URL失败: {url_input}")
                    else:
                        st.warning("⚠️ 请先启动浏览器并输入URL")
            
            with col_url2:
                if st.button("📸 截图", use_container_width=True):
                    if st.session_state.jarvis and st.session_state.jarvis.driver:
                        filename = f"screenshot_{int(time.time())}.png"
                        success = st.session_state.jarvis.take_screenshot(filename)
                        if success:
                            st.success(f"✅ 截图保存: {filename}")
                            add_log(f"截图保存: {filename}")
                        else:
                            st.error("❌ 截图失败")
                    else:
                        st.warning("⚠️ 请先启动浏览器")
            
            # Google搜索
            search_query = st.text_input("🔍 Google搜索:", placeholder="输入搜索关键词")
            if st.button("🔍 搜索", use_container_width=True):
                if st.session_state.jarvis and st.session_state.jarvis.driver and search_query:
                    with st.spinner("正在搜索..."):
                        success = st.session_state.jarvis.search_google(search_query)
                    if success:
                        st.success(f"✅ 搜索完成: {search_query}")
                        add_log(f"Google搜索: {search_query}")
                    else:
                        st.error("❌ 搜索失败")
                        add_log(f"搜索失败: {search_query}")
                else:
                    st.warning("⚠️ 请先启动浏览器并输入搜索词")
        
        # API调用
        with st.expander("🔌 API调用"):
            tab1, tab2, tab3 = st.tabs(["🌐 通用API", "🤖 AI对话", "📊 公开API测试"])
            
            with tab1:
                api_url = st.text_input("🔗 API URL:", placeholder="https://api.example.com/data")
                api_method = st.selectbox("📋 请求方法:", ["GET", "POST", "PUT", "DELETE"])
                
                if api_method in ["POST", "PUT"]:
                    api_data = st.text_area("📝 请求数据 (JSON):", placeholder='{"key": "value"}')
                
                if st.button("🚀 调用API", use_container_width=True):
                    if api_url:
                        with st.spinner("正在调用API..."):
                            if api_method == "GET":
                                result = st.session_state.api_tools.get(api_url)
                            elif api_method == "POST":
                                import json
                                try:
                                    data = json.loads(api_data) if api_data else None
                                    result = st.session_state.api_tools.post(api_url, data)
                                except json.JSONDecodeError:
                                    st.error("❌ JSON格式错误")
                                    result = None
                        
                        if result:
                            st.success("✅ API调用成功")
                            st.json(result)
                            add_log(f"API调用成功: {api_url}")
                        else:
                            st.error("❌ API调用失败")
                            add_log(f"API调用失败: {api_url}")
                    else:
                        st.warning("⚠️ 请输入API URL")
            
            with tab2:
                if api_status['openai']:
                    ai_prompt = st.text_area("💭 AI对话:", placeholder="请输入您的问题...", height=100)
                    if st.button("🤖 发送", use_container_width=True):
                        if ai_prompt:
                            with st.spinner("AI正在思考..."):
                                response = st.session_state.api_tools.call_openai_api(ai_prompt)
                            if response:
                                st.success("✅ AI回答:")
                                st.write(response)
                                add_log("AI对话成功")
                            else:
                                st.error("❌ AI调用失败")
                        else:
                            st.warning("⚠️ 请输入问题")
                else:
                    st.warning("⚠️ OpenAI API未配置")
                    st.info("💡 请在.env文件中配置OPENAI_API_KEY以使用AI对话功能")
            
            with tab3:
                if st.button("🧪 测试公开API", use_container_width=True):
                    with st.spinner("正在测试公开API..."):
                        # 在这里显示测试结果
                        st.info("正在测试各种公开API...")
                        
                        # GitHub API测试
                        github_result = st.session_state.api_tools.call_github_api("users/octocat")
                        if github_result:
                            st.success("✅ GitHub API测试成功")
                            st.write(f"用户: {github_result.get('name', 'N/A')}")
                        
                        # 随机名言API测试
                        quote_result = st.session_state.api_tools.get("https://api.quotable.io/random")
                        if quote_result:
                            st.success("✅ 名言API测试成功")
                            st.write(f"名言: {quote_result.get('content', 'N/A')}")
                        
                        add_log("公开API测试完成")
        
        # Python代码执行
        with st.expander("🐍 Python代码执行"):
            python_code = st.text_area(
                "📝 输入Python代码:", 
                placeholder="""# 示例代码
import datetime
import math

print("Hello from Jarvis!")
print(f"当前时间: {datetime.datetime.now()}")
print(f"圆周率: {math.pi:.6f}")

# 简单计算
numbers = [1, 2, 3, 4, 5]
print(f"数字总和: {sum(numbers)}")""",
                height=200
            )
            
            col_py1, col_py2 = st.columns(2)
            with col_py1:
                if st.button("▶️ 执行代码", use_container_width=True):
                    if python_code:
                        try:
                            # 重定向输出
                            from io import StringIO
                            import contextlib
                            import sys
                            
                            output = StringIO()
                            with contextlib.redirect_stdout(output):
                                # 创建安全的执行环境
                                safe_globals = {
                                    '__builtins__': {
                                        'print': print,
                                        'len': len, 'str': str, 'int': int, 'float': float,
                                        'list': list, 'dict': dict, 'range': range,
                                        'enumerate': enumerate, 'zip': zip,
                                        'sum': sum, 'max': max, 'min': min,
                                    }
                                }
                                
                                # 允许导入常用模块
                                import datetime, math, json
                                safe_globals.update({
                                    'datetime': datetime,
                                    'math': math,
                                    'json': json,
                                })
                                
                                exec(python_code, safe_globals)
                            
                            result = output.getvalue()
                            if result:
                                st.success("✅ 代码执行成功")
                                st.code(result, language="text")
                                add_log("Python代码执行成功")
                            else:
                                st.success("✅ 代码执行完成（无输出）")
                                add_log("Python代码执行完成")
                        except Exception as e:
                            st.error(f"❌ 代码执行失败: {e}")
                            add_log(f"Python代码执行失败: {e}")
                    else:
                        st.warning("⚠️ 请输入Python代码")
            
            with col_py2:
                if st.button("🗑️ 清空代码", use_container_width=True):
                    st.rerun()
    
    with col2:
        st.header("📊 状态信息")
        
        # 系统状态
        st.subheader("🖥️ 系统状态")
        browser_status = "🟢 运行中" if (st.session_state.jarvis and st.session_state.jarvis.driver) else "🔴 未启动"
        st.write(f"**浏览器:** {browser_status}")
        
        if st.session_state.jarvis and st.session_state.jarvis.driver:
            current_url = st.session_state.jarvis.get_current_url()
            current_title = st.session_state.jarvis.get_page_title()
            if current_url:
                st.write(f"**当前URL:** {current_url[:50]}...")
            if current_title:
                st.write(f"**页面标题:** {current_title[:30]}...")
        
        # API状态详情
        st.subheader("🔑 API配置")
        for service, status in api_status.items():
            status_icon = "✅" if status else "❌"
            st.write(f"**{service.upper()}:** {status_icon}")
        
        # 操作日志
        st.subheader("📝 操作日志")
        log_container = st.container()
        with log_container:
            if st.session_state.logs:
                # 显示最近的10条日志
                for log in st.session_state.logs[-10:]:
                    st.text(log)
            else:
                st.text("暂无操作日志")
        
        # 清空日志按钮
        if st.button("🗑️ 清空日志", use_container_width=True):
            st.session_state.logs = []
            st.rerun()
        
        # 帮助信息
        with st.expander("❓ 使用帮助"):
            st.markdown("""
            **基础功能（无需API密钥）:**
            - 🌐 浏览器自动化操作
            - 🔍 Google搜索
            - 📸 网页截图
            - 🐍 Python代码执行
            - 🔌 通用API调用
            
            **高级功能（需要API密钥）:**
            - 🤖 AI对话 (OpenAI)
            - 🌤️ 天气查询 (OpenWeather)
            - 🔍 Google搜索API
            
            **使用提示:**
            - 遇到验证码时可手动处理
            - 支持保持登录状态
            - 代码在安全环境中执行
            """)

if __name__ == "__main__":
    main()
