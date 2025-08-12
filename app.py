#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis AI 本地知识库 - 主应用
"""

import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from pathlib import Path
import os

from config.settings import get_config
from core.knowledge_engine import KnowledgeEngine
from utils.logger import setup_logger

# 初始化配置
config = get_config()
setup_logger()

# 创建Flask应用
app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.config['SECRET_KEY'] = 'jarvis-ai-knowledge-base'
app.config['MAX_CONTENT_LENGTH'] = config['max_file_size']

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化知识库引擎
knowledge_engine = KnowledgeEngine(config)

# 确保存储目录存在
for path in [config['documents_path'], config['uploads_path'], config['vector_db_path']]:
    Path(path).mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """文件上传接口"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': '文件名为空'})
        
        # 确定文件类型
        if file.filename.lower().endswith('.pdf'):
            doc_type = 'pdf'
        elif file.filename.lower().endswith(('.md', '.markdown')):
            doc_type = 'markdown'
        else:
            return jsonify({'success': False, 'message': '不支持的文件类型'})
        
        # 保存临时文件
        temp_path = config['uploads_path'] / file.filename
        file.save(temp_path)
        
        # 添加到知识库
        result = knowledge_engine.add_document(str(temp_path), doc_type)
        
        # 清理临时文件
        temp_path.unlink()
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"文件上传错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@socketio.on('query')
def handle_query(data):
    """处理查询请求"""
    try:
        question = data.get('question', '')
        if not question:
            emit('response', {'answer': '请输入问题', 'sources': []})
            return
        
        # 查询知识库
        result = knowledge_engine.query(question)
        emit('response', result)
        
    except Exception as e:
        logging.error(f"查询错误: {e}")
        emit('response', {'answer': '查询出错，请稍后重试', 'sources': []})

@app.route('/stats')
def get_stats():
    """获取知识库统计"""
    try:
        stats = knowledge_engine.get_stats()
        return jsonify(stats)
    except Exception as e:
        logging.error(f"获取统计信息错误: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    logging.info("🤖 Jarvis AI 知识库启动中...")
    logging.info(f"访问地址: http://localhost:{config['port']}")
    
    socketio.run(
        app,
        host=config['host'],
        port=config['port'],
        debug=config['debug']
    )