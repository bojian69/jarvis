#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{{project_name}} - 主应用模板
"""

import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from pathlib import Path
from werkzeug.utils import secure_filename

from config.settings import get_config
from core.knowledge_engine import KnowledgeEngine

# 初始化配置
config = get_config()

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret_key']
app.config['MAX_CONTENT_LENGTH'] = config['max_content_length']

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化知识库引擎
knowledge_engine = KnowledgeEngine(config)

# 确保存储目录存在
for path_key in ['documents_path', 'uploads_path', 'vector_db_path']:
    Path(config[path_key]).mkdir(parents=True, exist_ok=True)

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
        
        # 安全文件名处理
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'success': False, 'message': '无效的文件名'})
        
        # 文件类型验证
        file_ext = filename.lower().split('.')[-1]
        if file_ext not in config['allowed_extensions']:
            return jsonify({'success': False, 'message': '不支持的文件类型'})
        
        # 保存临时文件
        temp_path = Path(config['uploads_path']) / filename
        file.save(str(temp_path))
        
        try:
            # 添加到知识库
            result = knowledge_engine.add_document(str(temp_path), file_ext)
            return jsonify(result)
        finally:
            # 清理临时文件
            if temp_path.exists():
                temp_path.unlink()
        
    except Exception as e:
        logging.error(f"文件上传错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@socketio.on('query')
def handle_query(data):
    """处理查询请求"""
    try:
        question = data.get('question', '').strip()
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

@app.errorhandler(413)
def too_large(e):
    """文件过大错误处理"""
    return jsonify({'success': False, 'message': '文件过大'}), 413

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info(f"🤖 {config.get('project_name', 'AI应用')} 启动中...")
    logging.info(f"访问地址: http://localhost:{config['port']}")
    
    socketio.run(
        app,
        host=config['host'],
        port=config['port'],
        debug=config['debug']
    )