#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量数据库浏览器 - Web界面
"""

import sys
sys.path.append('..')

from flask import Flask, render_template_string, jsonify
import chromadb
from config.settings import get_config

app = Flask(__name__)

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ChromaDB 浏览器</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #667eea; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat-card { background: #f8f9fa; padding: 15px; border-radius: 8px; flex: 1; }
        .documents { background: white; border: 1px solid #ddd; border-radius: 8px; }
        .doc-item { padding: 15px; border-bottom: 1px solid #eee; }
        .doc-item:last-child { border-bottom: none; }
        .doc-title { font-weight: bold; color: #333; }
        .doc-meta { color: #666; font-size: 14px; margin: 5px 0; }
        .doc-content { background: #f8f9fa; padding: 10px; border-radius: 4px; margin-top: 10px; font-family: monospace; font-size: 12px; }
        .btn { background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #5a6fd8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 ChromaDB 向量数据库浏览器</h1>
            <p>实时查看和管理向量数据库内容</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <h3>📄 文档数量</h3>
                <div id="docCount">加载中...</div>
            </div>
            <div class="stat-card">
                <h3>🧩 文本片段</h3>
                <div id="chunkCount">加载中...</div>
            </div>
            <div class="stat-card">
                <h3>📚 集合数量</h3>
                <div id="collectionCount">加载中...</div>
            </div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <button class="btn" onclick="loadData()">🔄 刷新数据</button>
            <button class="btn" onclick="exportData()" style="background: #28a745;">📥 导出数据</button>
        </div>
        
        <div class="documents">
            <h2 style="padding: 15px; margin: 0; background: #f8f9fa; border-bottom: 1px solid #ddd;">📋 文档列表</h2>
            <div id="documentList">加载中...</div>
        </div>
    </div>

    <script>
        function loadData() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('docCount').textContent = data.document_count || 0;
                    document.getElementById('chunkCount').textContent = data.total_chunks || 0;
                    document.getElementById('collectionCount').textContent = data.collections || 1;
                });
            
            fetch('/api/documents')
                .then(response => response.json())
                .then(documents => {
                    const listDiv = document.getElementById('documentList');
                    if (documents.length === 0) {
                        listDiv.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">暂无文档</div>';
                        return;
                    }
                    
                    listDiv.innerHTML = documents.map(doc => `
                        <div class="doc-item">
                            <div class="doc-title">📄 ${doc.filename}</div>
                            <div class="doc-meta">
                                类型: ${doc.type} | 片段数: ${doc.chunks} | ID: ${doc.doc_id}
                            </div>
                            <div class="doc-content">${doc.sample_content}</div>
                        </div>
                    `).join('');
                });
        }
        
        function exportData() {
            window.open('/api/export', '_blank');
        }
        
        // 页面加载时获取数据
        loadData();
        
        // 每30秒自动刷新
        setInterval(loadData, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    try:
        config = get_config()
        client = chromadb.PersistentClient(path=str(config['vector_db_path']))
        collection = client.get_collection("documents")
        
        total_chunks = collection.count()
        collections = len(client.list_collections())
        
        # 获取文档统计
        if total_chunks > 0:
            results = collection.get()
            documents = {}
            for metadata in results['metadatas']:
                filename = metadata['filename']
                if filename not in documents:
                    documents[filename] = 0
                documents[filename] += 1
            
            return jsonify({
                'total_chunks': total_chunks,
                'document_count': len(documents),
                'collections': collections
            })
        else:
            return jsonify({
                'total_chunks': 0,
                'document_count': 0,
                'collections': collections
            })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/documents')
def get_documents():
    try:
        config = get_config()
        client = chromadb.PersistentClient(path=str(config['vector_db_path']))
        collection = client.get_collection("documents")
        
        results = collection.get()
        documents = {}
        
        for i, metadata in enumerate(results['metadatas']):
            filename = metadata['filename']
            if filename not in documents:
                documents[filename] = {
                    'filename': filename,
                    'type': metadata['type'],
                    'doc_id': metadata['doc_id'],
                    'chunks': 0,
                    'sample_content': results['documents'][i][:200] + "..."
                }
            documents[filename]['chunks'] += 1
        
        return jsonify(list(documents.values()))
    except Exception as e:
        return jsonify([])

@app.route('/api/export')
def export_data():
    try:
        config = get_config()
        client = chromadb.PersistentClient(path=str(config['vector_db_path']))
        collection = client.get_collection("documents")
        
        results = collection.get()
        
        from flask import Response
        import json
        
        export_data = {
            'collection_name': 'documents',
            'count': len(results['ids']),
            'export_time': str(__import__('datetime').datetime.now()),
            'documents': []
        }
        
        for i in range(len(results['ids'])):
            export_data['documents'].append({
                'id': results['ids'][i],
                'document': results['documents'][i],
                'metadata': results['metadatas'][i]
            })
        
        response = Response(
            json.dumps(export_data, ensure_ascii=False, indent=2),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=chroma_export.json'}
        )
        return response
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🌐 启动 ChromaDB 浏览器...")
    print("📍 访问地址: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)