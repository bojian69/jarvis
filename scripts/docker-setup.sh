#!/bin/bash
# Jarvis AI Docker 部署脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    print_success "Docker 环境检查通过"
}

# 创建环境配置文件
setup_env() {
    if [ ! -f .env ]; then
        print_info "创建环境配置文件..."
        cp .env.example .env
        print_success "已创建 .env 文件，请根据需要修改配置"
    else
        print_info ".env 文件已存在"
    fi
}

# 构建镜像
build_image() {
    print_info "构建 Jarvis AI Docker 镜像..."
    docker-compose build
    print_success "镜像构建完成"
}

# 启动服务
start_services() {
    local profile=""
    
    # 询问是否启动Ollama服务
    read -p "是否启动 Ollama 服务? (y/N): " start_ollama
    if [[ $start_ollama =~ ^[Yy]$ ]]; then
        profile="--profile ollama"
        print_info "将启动 Ollama 服务..."
    fi
    
    print_info "启动 Jarvis AI 服务..."
    docker-compose $profile up -d
    
    print_success "服务启动完成"
    print_info "访问地址: http://localhost:${JARVIS_PORT:-8080}"
}

# 下载Ollama模型
setup_ollama_models() {
    if docker ps | grep -q jarvis-ollama; then
        print_info "下载推荐的 Ollama 模型..."
        
        # 询问要下载的模型
        echo "请选择要下载的模型:"
        echo "1) qwen2.5:1.5b (轻量级, ~1GB)"
        echo "2) qwen2.5:7b (推荐, ~4GB)"
        echo "3) qwen2.5:14b (高性能, ~8GB)"
        echo "4) 跳过模型下载"
        
        read -p "请输入选择 (1-4): " model_choice
        
        case $model_choice in
            1)
                docker exec jarvis-ollama ollama pull qwen2.5:1.5b
                ;;
            2)
                docker exec jarvis-ollama ollama pull qwen2.5:7b
                ;;
            3)
                docker exec jarvis-ollama ollama pull qwen2.5:14b
                ;;
            4)
                print_info "跳过模型下载"
                ;;
            *)
                print_warning "无效选择，跳过模型下载"
                ;;
        esac
    else
        print_warning "Ollama 服务未启动，跳过模型下载"
    fi
}

# 显示服务状态
show_status() {
    print_info "服务状态:"
    docker-compose ps
    
    print_info "服务日志 (最近10行):"
    docker-compose logs --tail=10 jarvis-ai
}

# 停止服务
stop_services() {
    print_info "停止服务..."
    docker-compose down
    print_success "服务已停止"
}

# 清理数据
cleanup_data() {
    read -p "确定要清理所有数据吗? 这将删除所有文档和向量数据 (y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        print_warning "清理数据..."
        docker-compose down -v
        docker volume prune -f
        print_success "数据清理完成"
    else
        print_info "取消清理操作"
    fi
}

# 显示帮助信息
show_help() {
    echo "Jarvis AI Docker 部署脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  setup     - 完整设置 (检查环境、构建镜像、启动服务)"
    echo "  build     - 构建镜像"
    echo "  start     - 启动服务"
    echo "  stop      - 停止服务"
    echo "  restart   - 重启服务"
    echo "  status    - 显示服务状态"
    echo "  logs      - 显示服务日志"
    echo "  models    - 下载 Ollama 模型"
    echo "  cleanup   - 清理所有数据"
    echo "  help      - 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 setup          # 完整部署"
    echo "  $0 start          # 启动服务"
    echo "  $0 logs jarvis-ai # 查看特定服务日志"
}

# 主函数
main() {
    case "${1:-setup}" in
        setup)
            check_docker
            setup_env
            build_image
            start_services
            setup_ollama_models
            show_status
            ;;
        build)
            check_docker
            build_image
            ;;
        start)
            check_docker
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            start_services
            ;;
        status)
            show_status
            ;;
        logs)
            if [ -n "$2" ]; then
                docker-compose logs -f "$2"
            else
                docker-compose logs -f
            fi
            ;;
        models)
            setup_ollama_models
            ;;
        cleanup)
            cleanup_data
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"