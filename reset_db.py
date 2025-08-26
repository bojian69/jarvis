#!/usr/bin/env python3
import shutil
import os
from pathlib import Path

# 删除现有数据库
db_path = Path("/Volumes/common/jarvis/vector_db")
if db_path.exists():
    shutil.rmtree(db_path)
    print(f"已删除数据库目录: {db_path}")

# 重新创建目录
db_path.mkdir(parents=True, exist_ok=True)
os.chmod(db_path, 0o755)
print(f"已重新创建数据库目录: {db_path}")

print("数据库重置完成！")