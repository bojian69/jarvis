#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量上传功能测试脚本
"""

import requests
import os
from pathlib import Path

def test_batch_upload():
    """测试批量上传功能"""
    
    # 创建测试文件
    test_files_dir = Path("test_files")
    test_files_dir.mkdir(exist_ok=True)
    
    # 创建测试Markdown文件
    test_md1 = test_files_dir / "测试文档1.md"
    test_md1.write_text("""# 测试文档1

这是第一个测试文档。

## 内容
- 项目介绍
- 功能特性
- 使用方法

### 详细说明
这个文档用于测试批量上传功能，确保原始文件名得到保持。
""", encoding='utf-8')
    
    test_md2 = test_files_dir / "Test Document 2.md"
    test_md2.write_text("""# Test Document 2

This is the second test document.

## Features
- Batch upload support
- Original filename preservation
- Multi-language support

### Description
This document tests the batch upload functionality with English content.
""", encoding='utf-8')
    
    # 测试单文件上传
    print("🧪 测试单文件上传...")
    with open(test_md1, 'rb') as f:
        files = {'file': (test_md1.name, f, 'text/markdown')}
        response = requests.post('http://localhost:8080/upload', files=files)
        result = response.json()
        print(f"单文件上传结果: {result}")
    
    # 测试第二个文件上传
    print("\n🧪 测试第二个文件上传...")
    with open(test_md2, 'rb') as f:
        files = {'file': (test_md2.name, f, 'text/markdown')}
        response = requests.post('http://localhost:8080/upload', files=files)
        result = response.json()
        print(f"第二个文件上传结果: {result}")
    
    # 获取知识库统计
    print("\n📊 获取知识库统计...")
    response = requests.get('http://localhost:8080/stats')
    stats = response.json()
    print(f"知识库统计: {stats}")
    
    # 清理测试文件
    test_md1.unlink()
    test_md2.unlink()
    test_files_dir.rmdir()
    
    print("\n✅ 测试完成！")

if __name__ == "__main__":
    test_batch_upload()