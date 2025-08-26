FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /data/documents /data/vector_db /data/uploads /data/logs

# 设置环境变量
ENV PYTHONPATH=/app
ENV JARVIS_DATA_PATH=/data
ENV JARVIS_HOST=0.0.0.0
ENV JARVIS_PORT=8080
ENV JARVIS_DEBUG=false

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/stats || exit 1

# 启动应用
CMD ["python", "app.py"]