#!/bin/bash
# Jarvis AI机器人安装脚本

echo "🤖 安装Jarvis AI机器人依赖..."

# 安装系统依赖 (macOS)
brew install portaudio
export CPPFLAGS="-I$(brew --prefix portaudio)/include"
export LDFLAGS="-L$(brew --prefix portaudio)/lib"

# 安装Python依赖
pip3 install -r requirements.txt

echo "✅ 安装完成！"
echo "运行命令: python3 jarvis_robot.py"
echo "访问: http://localhost:5000"