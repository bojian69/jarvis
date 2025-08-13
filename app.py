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
        
        # 安全文件名处理
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        
        # 确定文件类型
        if filename.lower().endswith('.pdf'):
            doc_type = 'pdf'
        elif filename.lower().endswith(('.md', '.markdown')):
            doc_type = 'markdown'
        else:
            return jsonify({'success': False, 'message': f'不支持的文件类型: {filename}'})
        
        # 检查文件大小
        if len(file.read()) > config.get('max_file_size', 10 * 1024 * 1024):  # 10MB
            return jsonify({'success': False, 'message': '文件过大'})
        file.seek(0)  # 重置文件指针
        
        # 保存临时文件
        temp_path = config['uploads_path'] / filename
        
        # 避免文件名冲突
        counter = 1
        original_path = temp_path
        while temp_path.exists():
            name, ext = original_path.stem, original_path.suffix
            temp_path = original_path.parent / f"{name}_{counter}{ext}"
            counter += 1
        
        try:
            file.save(str(temp_path))
            
            # 添加到知识库
            result = knowledge_engine.add_document(str(temp_path), doc_type)
            
            return jsonify(result)
            
        finally:
            # 确保清理临时文件
            if temp_path.exists():
                temp_path.unlink()
        
    except Exception as e:
        logging.error(f"文件上传错误: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/upload/batch', methods=['POST'])
def upload_batch():
    """批量文件上传接口"""
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        results = []
        success_count = 0
        
        for file in files:
            if file.filename == '':
                continue
                
            try:
                from werkzeug.utils import secure_filename
                filename = secure_filename(file.filename)
                
                # 确定文件类型
                if filename.lower().endswith('.pdf'):
                    doc_type = 'pdf'
                elif filename.lower().endswith(('.md', '.markdown')):
                    doc_type = 'markdown'
                else:
                    results.append({'filename': filename, 'success': False, 'message': '不支持的文件类型'})
                    continue
                
                # 保存临时文件
                temp_path = config['uploads_path'] / filename
                counter = 1
                original_path = temp_path
                while temp_path.exists():
                    name, ext = original_path.stem, original_path.suffix
                    temp_path = original_path.parent / f"{name}_{counter}{ext}"
                    counter += 1
                
                file.save(str(temp_path))
                
                try:
                    # 添加到知识库
                    result = knowledge_engine.add_document(str(temp_path), doc_type)
                    if result.get('success'):
                        success_count += 1
                    results.append({'filename': filename, **result})
                finally:
                    if temp_path.exists():
                        temp_path.unlink()
                        
            except Exception as e:
                results.append({'filename': file.filename, 'success': False, 'message': str(e)})
        
        return jsonify({
            'success': success_count > 0,
            'message': f'成功上传 {success_count}/{len(files)} 个文件',
            'results': results,
            'success_count': success_count,
            'total_count': len(files)
        })
        
    except Exception as e:
        logging.error(f"批量上传错误: {e}")
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
    import socket
    
    # 获取本机 IP 地址
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    local_ip = get_local_ip()
    port = config['port']
    
    logging.info("🤖 Jarvis AI 知识库启动中...")
    logging.info(f"🏠 本地访问: http://localhost:{port}")
    logging.info(f"🌍 外网访问: http://{local_ip}:{port}")
    logging.info(f"📊 管理面板: http://localhost:{port}/stats")
    
    socketio.run(
        app,
        host=config['host'],
        port=port,
        debug=config['debug']
    )