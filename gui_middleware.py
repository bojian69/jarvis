#!/usr/bin/env python3
"""
Jarvis GUI - 中间件架构版本
"""

import streamlit as st
import time
from jarvis_agent import JarvisAgent

# 页面配置
st.set_page_config(
    page_title="Jarvis AI Agent - Middleware",
    page_icon="🤖",
    layout="wide"
)

# 初始化
if 'jarvis' not in st.session_state:
    st.session_state.jarvis = JarvisAgent()
if 'logs' not in st.session_state:
    st.session_state.logs = []

def add_log(message):
    """添加日志"""
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")
    if len(st.session_state.logs) > 50:
        st.session_state.logs = st.session_state.logs[-50:]

def main():
    st.title("🤖 Jarvis AI Agent - 中间件架构")
    st.markdown("重构版本 - 使用中间件模式的智能助手")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("🎛️ 控制面板")
        
        # 快捷操作
        st.subheader("🌐 浏览器操作")
        
        if st.button("🌐 打开Google", use_container_width=True):
            response = st.session_state.jarvis.open_url("https://www.google.com")
            if response.success:
                st.success("✅ Google已打开")
                add_log("打开Google成功")
            else:
                st.error(f"❌ {response.error}")
        
        if st.button("📸 截图", use_container_width=True):
            response = st.session_state.jarvis.take_screenshot()
            if response.success:
                filename = response.data.get('filename', 'screenshot.png')
                st.success(f"✅ 截图保存: {filename}")
                add_log(f"截图保存: {filename}")
            else:
                st.error(f"❌ {response.error}")
        
        if st.button("🛑 关闭浏览器", use_container_width=True):
            response = st.session_state.jarvis.close_browser()
            if response.success:
                st.success("✅ 浏览器已关闭")
                add_log("浏览器已关闭")
            else:
                st.error(f"❌ {response.error}")
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 功能操作")
        
        # 浏览器操作
        with st.expander("🌐 浏览器操作", expanded=True):
            url_input = st.text_input("🔗 URL:", placeholder="https://www.google.com")
            col_url1, col_url2 = st.columns(2)
            
            with col_url1:
                if st.button("🌐 打开网页"):
                    if url_input:
                        response = st.session_state.jarvis.open_url(url_input)
                        if response.success:
                            st.success(f"✅ 已打开: {response.data.get('title', url_input)}")
                            add_log(f"打开URL: {url_input}")
                        else:
                            st.error(f"❌ {response.error}")
                    else:
                        st.warning("⚠️ 请输入URL")
            
            with col_url2:
                search_query = st.text_input("🔍 搜索:", placeholder="输入关键词")
                if st.button("🔍 Google搜索"):
                    if search_query:
                        response = st.session_state.jarvis.search_google(search_query)
                        if response.success:
                            st.success(f"✅ 搜索完成: {search_query}")
                            add_log(f"Google搜索: {search_query}")
                        else:
                            st.error(f"❌ {response.error}")
                    else:
                        st.warning("⚠️ 请输入搜索关键词")
        
        # API调用
        with st.expander("🔌 API调用"):
            tab1, tab2, tab3 = st.tabs(["🌐 通用API", "🤖 AI对话", "📊 GitHub API"])
            
            with tab1:
                api_url = st.text_input("🔗 API URL:", placeholder="https://api.example.com/data")
                if st.button("🚀 GET请求"):
                    if api_url:
                        response = st.session_state.jarvis.call_api_get(api_url)
                        if response.success:
                            st.success("✅ API调用成功")
                            st.json(response.data.get('result', {}))
                            add_log(f"API调用成功: {api_url}")
                        else:
                            st.error(f"❌ {response.error}")
                    else:
                        st.warning("⚠️ 请输入API URL")
            
            with tab2:
                ai_prompt = st.text_area("💭 AI对话:", placeholder="请输入您的问题...", height=100)
                if st.button("🤖 发送"):
                    if ai_prompt:
                        response = st.session_state.jarvis.call_openai_api(ai_prompt)
                        if response.success:
                            st.success("✅ AI回答:")
                            st.write(response.data.get('answer', ''))
                            add_log("AI对话成功")
                        else:
                            st.error(f"❌ {response.error}")
                    else:
                        st.warning("⚠️ 请输入问题")
            
            with tab3:
                github_endpoint = st.text_input("📋 GitHub端点:", placeholder="users/octocat")
                if st.button("📊 调用GitHub API"):
                    if github_endpoint:
                        response = st.session_state.jarvis.call_github_api(github_endpoint)
                        if response.success:
                            st.success("✅ GitHub API调用成功")
                            st.json(response.data.get('result', {}))
                            add_log(f"GitHub API: {github_endpoint}")
                        else:
                            st.error(f"❌ {response.error}")
                    else:
                        st.warning("⚠️ 请输入GitHub端点")
        
        # Python代码执行
        with st.expander("🐍 Python代码执行"):
            python_code = st.text_area(
                "📝 Python代码:",
                placeholder="""# 示例代码
import datetime
import math

print("Hello from Jarvis Middleware!")
print(f"当前时间: {datetime.datetime.now()}")
print(f"圆周率: {math.pi:.6f}")

numbers = [1, 2, 3, 4, 5]
print(f"数字总和: {sum(numbers)}")""",
                height=200
            )
            
            if st.button("▶️ 执行代码"):
                if python_code:
                    response = st.session_state.jarvis.execute_python_code(python_code)
                    if response.success:
                        st.success("✅ 代码执行成功")
                        output = response.data.get('output', '')
                        if output:
                            st.code(output, language="text")
                        add_log("Python代码执行成功")
                    else:
                        st.error(f"❌ {response.error}")
                else:
                    st.warning("⚠️ 请输入Python代码")
    
    with col2:
        st.header("📊 状态信息")
        
        # 系统状态
        st.subheader("🖥️ 系统状态")
        st.write("**架构:** 中间件模式")
        st.write("**状态:** 🟢 运行中")
        
        # 操作日志
        st.subheader("📝 操作日志")
        if st.session_state.logs:
            for log in st.session_state.logs[-10:]:
                st.text(log)
        else:
            st.text("暂无操作日志")
        
        if st.button("🗑️ 清空日志"):
            st.session_state.logs = []
            st.rerun()
        
        # 帮助信息
        with st.expander("❓ 中间件架构说明"):
            st.markdown("""
            **中间件架构优势:**
            - 🔧 模块化设计，易于扩展
            - 🛡️ 统一的错误处理
            - 📝 完整的日志记录
            - ✅ 参数验证
            - 🔄 可插拔的组件
            
            **中间件执行顺序:**
            1. LoggingMiddleware - 日志记录
            2. ValidationMiddleware - 参数验证
            3. BrowserMiddleware - 浏览器操作
            4. APIMiddleware - API调用
            5. PythonExecutorMiddleware - 代码执行
            """)

if __name__ == "__main__":
    main()