#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本处理工具
"""

import re
from typing import List

class TextProcessor:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def split_text(self, text: str) -> List[str]:
        """智能文本分块"""
        # 清理文本
        text = self._clean_text(text)
        
        # 按段落分割
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) < self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # 过滤太短的块
        return [chunk for chunk in chunks if len(chunk.strip()) > 20]
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()""''—\-]', '', text)
        return text.strip()