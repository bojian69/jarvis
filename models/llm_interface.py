#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM接口 - 本地大语言模型接口
"""

import requests
import logging
from typing import List, Dict

class LLMInterface:
    def __init__(self, config: Dict):
        self.base_url = config.get("llm_url", "http://localhost:11434")
        self.model = config.get("llm_model", "qwen2.5:7b")
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """检查模型是否可用"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_answer(self, question: str, context_docs: List[Dict]) -> str:
        """基于上下文生成回答"""
        if not context_docs:
            return self._format_no_result_answer(question)
        
        # 基于检索结果生成回答
        context = self._build_context(context_docs)
        
        # 如果有Ollama服务，尝试使用
        if self.available:
            try:
                prompt = self._build_prompt(question, context)
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.7}
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if "response" in result:
                        return self._format_markdown_answer(result["response"])
            except Exception as e:
                logging.error(f"LLM调用失败: {e}")
        
        # 备用Markdown格式回答
        return self._format_fallback_answer(question, context_docs)
    
    def _build_context(self, docs: List[Dict]) -> str:
        """构建上下文文本"""
        if not docs:
            return "没有找到相关文档。"
        
        # 按文档来源分组
        docs_by_source = {}
        for doc in docs:
            source = doc.get('source', '未知来源')
            if source not in docs_by_source:
                docs_by_source[source] = []
            docs_by_source[source].append(doc)
        
        context_parts = []
        for source, source_docs in docs_by_source.items():
            context_parts.append(f"### 文档：{source}")
            
            for i, doc in enumerate(source_docs, 1):
                content = doc.get('content', '')
                score = doc.get('score', 0)
                if content:
                    # 保留更多内容，根据相似度调整长度
                    max_length = 400 if score > 0.7 else 300
                    truncated_content = content[:max_length]
                    if len(content) > max_length:
                        truncated_content += "..."
                    
                    context_parts.append(f"片段{i}（相似度: {score:.2f}）：")
                    context_parts.append(truncated_content)
            
            context_parts.append("")  # 文档间空行
        
        return "\n".join(context_parts)
    
    def _build_prompt(self, question: str, context: str) -> str:
        """构建提示词"""
        return f"""你是一个专业的文档分析助手。请基于提供的多个文档片段综合回答用户问题。

## 文档内容
{context}

## 用户问题
{question}

## 回答要求
- **综合分析**：请综合上述所有文档片段的信息，给出全面的回答
- **信息整合**：如果不同文档中有相关信息，请整合并去重
- **来源标注**：在适当位置指出信息来源（如“根据文档A”）
- **Markdown格式**：使用标题、列表、代码块等格式化元素
- **结构化回答**：如果信息较多，请用清晰的段落和小标题组织
- **重点突出**：重要信息使用**加粗**或`代码格式`强调

请综合以上所有文档信息回答："""
    
    def _format_no_result_answer(self, question: str) -> str:
        """格式化无结果回答"""
        return f"""## ❌ 未找到相关信息

对不起，我在知识库中没有找到与 **"{question}"** 相关的信息。

### 建议
- 📄 请尝试上传相关文档
- 🔄 换个关键词重新提问
- 💡 检查问题是否与已上传的文档内容相关"""
    
    def _format_markdown_answer(self, answer: str) -> str:
        """格式化Markdown回答"""
        # 确保回答已经是Markdown格式，如果不是则简单格式化
        if not any(marker in answer for marker in ['#', '*', '`', '-', '1.']):
            # 简单格式化纯文本回答
            lines = answer.split('\n')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    if line.endswith('：') or line.endswith(':'):
                        formatted_lines.append(f"### {line}")
                    else:
                        formatted_lines.append(line)
                else:
                    formatted_lines.append('')
            return '\n'.join(formatted_lines)
        return answer
    
    def _format_fallback_answer(self, question: str, context_docs: List[Dict]) -> str:
        """格式化备用回答"""
        answer_parts = [f"## 📋 关于 \"{question}\" 的综合信息\n"]
        
        # 按文档来源分组展示
        docs_by_source = {}
        for doc in context_docs:
            source = doc.get('source', '未知来源')
            if source not in docs_by_source:
                docs_by_source[source] = []
            docs_by_source[source].append(doc)
        
        # 综合概述
        if len(docs_by_source) > 1:
            answer_parts.append("基于多个文档的相关信息，以下是综合整理的内容：\n")
        
        for source, source_docs in docs_by_source.items():
            answer_parts.append(f"### 📄 来自《{source}》")
            
            # 合并同一文档的内容
            combined_content = ""
            for doc in source_docs[:2]:  # 每个文档最多2个片段
                content = doc.get('content', '')
                if content:
                    combined_content += content[:250] + " "
            
            if combined_content:
                # 去除重复内容并格式化
                combined_content = combined_content.strip()
                if len(combined_content) > 500:
                    combined_content = combined_content[:500] + "..."
                
                answer_parts.append(f"> {combined_content}\n")
        
        # 添加总结
        if len(context_docs) > 3:
            answer_parts.append(f"---")
            answer_parts.append(f"📊 **信息统计**: 共找到 {len(context_docs)} 个相关片段，来自 {len(docs_by_source)} 个文档")
        
        answer_parts.append("\n💡 *以上信息已综合多个文档片段，如需更详细信息，请查看原始文档。*")
        
        return '\n'.join(answer_parts)