#!/usr/bin/env python3
import webbrowser
import openai
import logging
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from config import OPENAI_API_KEY, DEFAULT_URL

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JarvisRobot:
    def __init__(self):
        if OPENAI_API_KEY and OPENAI_API_KEY != "your-api-key-here":
            openai.api_key = OPENAI_API_KEY
            self.use_openai = True
        else:
            self.use_openai = False
        
    def open_browser(self, url=DEFAULT_URL):
        """打开浏览器"""
        logger.info(f"打开浏览器: {url}")
        webbrowser.open(url)
        
    def chat_with_ai(self, message):
        """AI对话"""
        logger.info(f"收到消息: {message}")
        
        if "浏览器" in message:
            self.open_browser()
            response = "已为您打开浏览器"
            logger.info(f"回复: {response}")
            return response
        
        if self.use_openai:
            try:
                logger.info("调用OpenAI API")
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": message}],
                    max_tokens=150
                )
                ai_response = response.choices[0].message.content.strip()
                logger.info(f"OpenAI回复: {ai_response}")
                return ai_response
            except Exception as e:
                logger.error(f"OpenAI错误: {e}")
                return "AI服务暂时不可用，请稍后再试。"
        else:
            if "你好" in message:
                response = "你好！我是Jarvis，有什么可以帮助您的吗？"
            else:
                response = f"您说：{message}。我正在学习中..."
            logger.info(f"基础回复: {response}")
            return response

# Flask Web界面
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jarvis_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

jarvis = JarvisRobot()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    logger.info(f"WebSocket收到消息: {message}")
    response = jarvis.chat_with_ai(message)
    emit('receive_message', {'message': response})
    logger.info(f"WebSocket发送回复: {response}")

if __name__ == '__main__':
    logger.info("🤖 Jarvis AI机器人启动中...")
    logger.info("访问: http://localhost:8080")
    if jarvis.use_openai:
        logger.info("✅ OpenAI已启用")
    else:
        logger.info("⚠️  使用基础回复模式")
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, allow_unsafe_werkzeug=True)