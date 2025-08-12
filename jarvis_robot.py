#!/usr/bin/env python3
import speech_recognition as sr
import pyttsx3
import webbrowser
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import openai

class JarvisRobot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
    def setup_tts(self):
        """配置语音合成"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            self.tts_engine.setProperty('voice', voices[0].id)
        self.tts_engine.setProperty('rate', 150)
        
    def listen(self):
        """语音识别"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            return self.recognizer.recognize_google(audio, language='zh-CN')
        except:
            return None
            
    def speak(self, text):
        """语音输出"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        
    def open_browser(self, url="https://www.google.com"):
        """打开浏览器"""
        webbrowser.open(url)
        
    def chat_with_ai(self, message):
        """AI对话 - 这里可以集成你喜欢的AI API"""
        # 简单回复逻辑，可替换为OpenAI API
        if "浏览器" in message:
            self.open_browser()
            return "已为您打开浏览器"
        elif "你好" in message:
            return "你好！我是Jarvis，有什么可以帮助您的吗？"
        else:
            return f"您说：{message}。我正在学习中..."

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
    response = jarvis.chat_with_ai(message)
    jarvis.speak(response)
    emit('receive_message', {'message': response})

@socketio.on('start_listening')
def handle_listening():
    def listen_and_respond():
        text = jarvis.listen()
        if text:
            response = jarvis.chat_with_ai(text)
            jarvis.speak(response)
            socketio.emit('receive_message', {'message': f"您说：{text}\n回复：{response}"})
    
    threading.Thread(target=listen_and_respond).start()

if __name__ == '__main__':
    print("🤖 Jarvis AI机器人启动中...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)