#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档处理器 - 处理PDF和Markdown文件
"""

import PyPDF2
import markdown
import hashlib
from pathlib import Path
from typing import Dict, List
from utils.text_utils import TextProcessor

class DocumentProcessor:
    def __init__(self, config: Dict):
        self.config = config
        self.text_processor = TextProcessor()
    
    def process_document(self, file_path: str, doc_type: str) -> Dict:
        """处理文档并返回结构化数据"""
        if doc_type == "pdf":
            return self._process_pdf(file_path)
        elif doc_type == "markdown":
            return self._process_markdown(file_path)
        else:
            raise ValueError(f"不支持的文档类型: {doc_type}")
    
    def _process_pdf(self, file_path: str) -> Dict:
        """处理PDF文件"""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        return self._create_document_data(file_path, text, "pdf")
    
    def _process_markdown(self, file_path: str) -> Dict:
        """处理Markdown文件"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 保留原始markdown，同时提取纯文本
            html = markdown.markdown(content)
            import re
            text = re.sub('<[^<]+?>', '', html)
        
        return self._create_document_data(file_path, text, "markdown", content)
    
    def _create_document_data(self, file_path: str, text: str, doc_type: str, raw_content: str = None) -> Dict:
        """创建文档数据结构"""
        file_path = Path(file_path)
        doc_id = hashlib.md5(f"{file_path.name}_{text[:100]}".encode()).hexdigest()
        
        # 文本分块
        chunks = self.text_processor.split_text(text)
        
        return {
            "doc_id": doc_id,
            "filename": file_path.name,
            "type": doc_type,
            "text": text,
            "raw_content": raw_content or text,
            "chunks": chunks,
            "metadata": {
                "size": len(text),
                "chunk_count": len(chunks)
            }
        }