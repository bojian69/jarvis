#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

class DocumentManager:
    def __init__(self, storage_path="./documents"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # 创建子目录
        (self.storage_path / "pdf").mkdir(exist_ok=True)
        (self.storage_path / "markdown").mkdir(exist_ok=True)
        (self.storage_path / "metadata").mkdir(exist_ok=True)
        
        self.metadata_file = self.storage_path / "metadata" / "documents.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """加载文档元数据"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self):
        """保存文档元数据"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    def add_document(self, file_path: str, doc_type: str) -> Dict:
        """添加文档到存储系统"""
        try:
            # 生成文档ID
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            # 检查是否已存在
            if file_hash in self.metadata:
                return {"success": False, "message": "文档已存在"}
            
            # 复制文件到存储目录
            filename = Path(file_path).name
            storage_subdir = self.storage_path / doc_type
            new_path = storage_subdir / f"{file_hash}_{filename}"
            shutil.copy2(file_path, new_path)
            
            # 保存元数据
            self.metadata[file_hash] = {
                "original_name": filename,
                "type": doc_type,
                "storage_path": str(new_path),
                "upload_time": datetime.now().isoformat(),
                "size": os.path.getsize(file_path)
            }
            
            self._save_metadata()
            
            logging.info(f"文档已存储: {filename}")
            return {
                "success": True, 
                "doc_id": file_hash,
                "storage_path": str(new_path)
            }
            
        except Exception as e:
            logging.error(f"文档存储错误: {e}")
            return {"success": False, "message": str(e)}
    
    def get_document_list(self) -> List[Dict]:
        """获取文档列表"""
        documents = []
        for doc_id, info in self.metadata.items():
            documents.append({
                "id": doc_id,
                "name": info["original_name"],
                "type": info["type"],
                "upload_time": info["upload_time"],
                "size": info["size"]
            })
        return sorted(documents, key=lambda x: x["upload_time"], reverse=True)
    
    def delete_document(self, doc_id: str) -> bool:
        """删除文档"""
        try:
            if doc_id in self.metadata:
                # 删除文件
                storage_path = Path(self.metadata[doc_id]["storage_path"])
                if storage_path.exists():
                    storage_path.unlink()
                
                # 删除元数据
                del self.metadata[doc_id]
                self._save_metadata()
                
                logging.info(f"文档已删除: {doc_id}")
                return True
            return False
        except Exception as e:
            logging.error(f"删除文档错误: {e}")
            return False