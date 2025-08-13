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
import socket

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
        file.save(str(temp_path))
        
        # 添加到知识库
        result = knowledge_engine.add_document(str(temp_path), doc_type)
        
        # 记录文件上传
        if result.get('success'):
            logging.info(f"📄 文件上传成功: {file.filename} ({doc_type})")
        else:
            logging.warning(f"⚠️ 文件上传失败: {file.filename} - {result.get('error', '未知错误')}")
        
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
        
        # 记录用户问题
        logging.info(f"💬 用户问题: {question[:100]}{'...' if len(question) > 100 else ''}")
        
        # 查询知识库
        result = knowledge_engine.query(question)
        
        # 记录AI回复
        answer_preview = result['answer'][:150].replace('\n', ' ')
        sources_count = len(result.get('sources', []))
        logging.info(f"🤖 AI回复: {answer_preview}{'...' if len(result['answer']) > 150 else ''} [来源:{sources_count}个]")
        
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

@app.route('/view/<path:filename>')
def view_file(filename):
    """查看源文件内容"""
    try:
        # 递归查找文件
        docs_path = Path(config['documents_path'])
        file_path = None
        
        # 在所有子目录中查找文件
        for file_candidate in docs_path.rglob('*'):
            if file_candidate.is_file() and file_candidate.name == filename:
                file_path = file_candidate
                break
        
        if not file_path:
            # 尝试从向量数据库获取内容
            try:
                vector_content = knowledge_engine.get_document_content(filename)
                if vector_content:
                    return jsonify({
                        'filename': filename,
                        'type': 'markdown',
                        'content': vector_content,
                        'source': 'vector_db'
                    })
            except Exception as ve:
                logging.error(f"从向量数据库获取内容失败: {ve}")
            
            logging.warning(f"文件未找到: {filename}")
            return jsonify({'error': f'文件未找到: {filename}'}), 404
        
        # 读取文件内容
        if file_path.suffix.lower() in ['.md', '.markdown']:
            content = file_path.read_text(encoding='utf-8')
            logging.info(f"成功读取文件: {file_path}")
            return jsonify({
                'filename': filename,
                'type': 'markdown',
                'content': content,
                'path': str(file_path)
            })
        else:
            return jsonify({'error': f'不支持的文件类型: {file_path.suffix}'}), 400
            
    except Exception as e:
        logging.error(f"查看文件错误: {e}")
        return jsonify({'error': str(e)}), 500

def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    logging.info("🤖 Jarvis AI 知识库启动中...")
    
    local_ip = get_local_ip()
    port = config['port']
    
    logging.info(f"🌐 本地访问: http://localhost:{port}")
    logging.info(f"🌍 外网访问: http://{local_ip}:{port}")
    
    socketio.run(
        app,
        host=config['host'],
        port=port,
        debug=config['debug']
    )