#!/usr/bin/env python3
"""
代码执行模块
支持Python代码执行、文件操作等
"""

import os
import sys
import subprocess
import tempfile
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path
from ..core.middleware import with_middleware

class CodeModule:
    """代码执行模块"""
    
    def __init__(self, config, logger, middleware_manager):
        self.config = config
        self.logger = logger
        self.middleware_manager = middleware_manager
        self.temp_dir = Path(tempfile.gettempdir()) / "jarvis_code"
        self.temp_dir.mkdir(exist_ok=True)
    
    def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """执行代码命令"""
        command_map = {
            'code_execute_python': self.execute_python,
            'code_execute_shell': self.execute_shell,
            'code_read_file': self.read_file,
            'code_write_file': self.write_file,
            'code_list_directory': self.list_directory,
            'code_install_package': self.install_package,
            'code_run_script': self.run_script
        }
        
        if command in command_map:
            return command_map[command](**kwargs)
        else:
            return {"success": False, "error": f"未知的代码命令: {command}"}
    
    @with_middleware
    def execute_python(self, code: str, timeout: int = 30, **kwargs) -> Dict[str, Any]:
        """执行Python代码"""
        try:
            # 创建临时文件
            temp_file = self.temp_dir / f"temp_code_{int(time.time())}.py"
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # 执行代码
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, str(temp_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.temp_dir)
            )
            execution_time = time.time() - start_time
            
            # 清理临时文件
            temp_file.unlink(missing_ok=True)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "execution_time": execution_time,
                "message": "Python代码执行完成"
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"代码执行超时 ({timeout}秒)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            # 确保清理临时文件
            if 'temp_file' in locals():
                temp_file.unlink(missing_ok=True)
    
    @with_middleware
    def execute_shell(self, command: str, timeout: int = 30, **kwargs) -> Dict[str, Any]:
        """执行Shell命令"""
        try:
            start_time = time.time()
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            execution_time = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "execution_time": execution_time,
                "command": command,
                "message": "Shell命令执行完成"
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"命令执行超时 ({timeout}秒)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def read_file(self, filepath: str, encoding: str = 'utf-8', **kwargs) -> Dict[str, Any]:
        """读取文件"""
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                return {"success": False, "error": f"文件不存在: {filepath}"}
            
            if not file_path.is_file():
                return {"success": False, "error": f"不是文件: {filepath}"}
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            file_info = file_path.stat()
            
            return {
                "success": True,
                "content": content,
                "filepath": str(file_path.absolute()),
                "size": file_info.st_size,
                "modified_time": file_info.st_mtime,
                "encoding": encoding,
                "message": f"文件读取成功: {filepath}"
            }
            
        except UnicodeDecodeError:
            return {"success": False, "error": f"文件编码错误，请尝试其他编码格式"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def write_file(self, filepath: str, content: str, encoding: str = 'utf-8', 
                   create_dirs: bool = True, **kwargs) -> Dict[str, Any]:
        """写入文件"""
        try:
            file_path = Path(filepath)
            
            # 创建目录
            if create_dirs:
                file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            file_info = file_path.stat()
            
            return {
                "success": True,
                "filepath": str(file_path.absolute()),
                "size": file_info.st_size,
                "encoding": encoding,
                "message": f"文件写入成功: {filepath}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def list_directory(self, dirpath: str = ".", pattern: str = "*", **kwargs) -> Dict[str, Any]:
        """列出目录内容"""
        try:
            dir_path = Path(dirpath)
            
            if not dir_path.exists():
                return {"success": False, "error": f"目录不存在: {dirpath}"}
            
            if not dir_path.is_dir():
                return {"success": False, "error": f"不是目录: {dirpath}"}
            
            items = []
            for item in dir_path.glob(pattern):
                item_info = item.stat()
                items.append({
                    "name": item.name,
                    "path": str(item.absolute()),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item_info.st_size if item.is_file() else None,
                    "modified_time": item_info.st_mtime
                })
            
            # 按类型和名称排序
            items.sort(key=lambda x: (x["type"], x["name"]))
            
            return {
                "success": True,
                "directory": str(dir_path.absolute()),
                "items": items,
                "count": len(items),
                "message": f"目录列表获取成功: {dirpath}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def install_package(self, package: str, **kwargs) -> Dict[str, Any]:
        """安装Python包"""
        try:
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            execution_time = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "package": package,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "execution_time": execution_time,
                "message": f"包安装{'成功' if result.returncode == 0 else '失败'}: {package}"
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "包安装超时"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @with_middleware
    def run_script(self, script_path: str, args: list = None, timeout: int = 60, **kwargs) -> Dict[str, Any]:
        """运行脚本文件"""
        try:
            script_file = Path(script_path)
            
            if not script_file.exists():
                return {"success": False, "error": f"脚本文件不存在: {script_path}"}
            
            # 构建命令
            cmd = [sys.executable, str(script_file)]
            if args:
                cmd.extend(args)
            
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(script_file.parent)
            )
            execution_time = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "script_path": str(script_file.absolute()),
                "args": args or [],
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "execution_time": execution_time,
                "message": f"脚本执行{'成功' if result.returncode == 0 else '失败'}: {script_path}"
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"脚本执行超时 ({timeout}秒)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
