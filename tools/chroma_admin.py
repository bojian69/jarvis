#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChromaDB 管理工具
"""

import sys
import json
sys.path.append('..')

import chromadb
from pathlib import Path
from config.settings import get_config

class ChromaAdmin:
    def __init__(self):
        config = get_config()
        self.db_path = config['vector_db_path']
        print(" 数据库路径:", self.db_path)
        self.client = chromadb.PersistentClient(path=str(self.db_path))
    
    def list_collections(self):
        """列出所有集合"""
        collections = self.client.list_collections()
        print("📚 数据库集合:")
        for collection in collections:
            print(f"- {collection.name}")
        return collections
    
    def collection_info(self, collection_name="documents"):
        """获取集合详细信息"""
        try:
            collection = self.client.get_collection(collection_name)
            count = collection.count()
            
            print(f"\n📊 集合 '{collection_name}' 信息:")
            print(f"- 文档数量: {count}")
            
            if count > 0:
                results = collection.get(limit=10)
                print(f"- 示例文档:")
                for i, (doc_id, metadata) in enumerate(zip(results['ids'], results['metadatas'])):
                    print(f"  {i+1}. ID: {doc_id}")
                    print(f"     文件: {metadata.get('filename', 'N/A')}")
                    print(f"     类型: {metadata.get('type', 'N/A')}")
            
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    def export_data(self, collection_name="documents", output_file="chroma_export.json"):
        """导出数据"""
        try:
            collection = self.client.get_collection(collection_name)
            results = collection.get()
            
            export_data = {
                'collection_name': collection_name,
                'count': len(results['ids']),
                'documents': []
            }
            
            for i in range(len(results['ids'])):
                doc_data = {
                    'id': results['ids'][i],
                    'document': results['documents'][i],
                    'metadata': results['metadatas'][i]
                }
                export_data['documents'].append(doc_data)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据已导出到: {output_file}")
            
        except Exception as e:
            print(f"❌ 导出错误: {e}")
    
    def clear_collection(self, collection_name="documents"):
        """清空集合"""
        try:
            collection = self.client.get_collection(collection_name)
            results = collection.get()
            if results['ids']:
                collection.delete(ids=results['ids'])
                print(f"✅ 集合 '{collection_name}' 已清空")
            else:
                print(f"集合 '{collection_name}' 已经是空的")
        except Exception as e:
            print(f"❌ 清空错误: {e}")
            print("尝试重置数据库...")
            self.reset_database()
    
    def reset_database(self):
        """重置数据库（解决版本兼容性问题）"""
        try:
            import shutil
            import os
            
            # 关闭客户端
            if hasattr(self, 'client'):
                del self.client
            
            # 删除数据库文件
            if os.path.exists(self.db_path):
                shutil.rmtree(self.db_path)
                print(f"✅ 已删除旧数据库: {self.db_path}")
            
            # 重新创建数据库
            os.makedirs(self.db_path, exist_ok=True)
            self.client = chromadb.PersistentClient(path=str(self.db_path))
            
            print("✅ 数据库已重置，版本兼容性问题已解决")
            
        except Exception as e:
            print(f"❌ 重置数据库失败: {e}")
            # 尝试重新初始化客户端
            try:
                self.client = chromadb.PersistentClient(path=str(self.db_path))
            except:
                pass

def main():
    admin = ChromaAdmin()
    
    while True:
        print("\n" + "="*50)
        print("🔧 ChromaDB 管理工具")
        print("="*50)
        print("1. 列出所有集合")
        print("2. 查看集合信息") 
        print("3. 导出数据")
        print("4. 清空集合")
        print("5. 重置数据库")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            admin.list_collections()
        elif choice == '2':
            admin.collection_info()
        elif choice == '3':
            admin.export_data()
        elif choice == '4':
            confirm = input("确认清空集合? (y/N): ").strip().lower()
            if confirm == 'y':
                admin.clear_collection()
        elif choice == '5':
            confirm = input("确认重置数据库? 这将删除所有数据! (y/N): ").strip().lower()
            if confirm == 'y':
                admin.reset_database()

if __name__ == "__main__":
    main()