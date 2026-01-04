#!/bin/bash

# ===========================================
# WanderFlow 一键部署脚本
# 支持 Linux/macOS/Windows (WSL)
# ===========================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
PROJECT_NAME="WanderFlow"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="${SCRIPT_DIR}/docker"
ENV_FILE="${COMPOSE_DIR}/.env"

# 打印带颜色的消息
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印横幅
print_banner() {
    echo -e "${BLUE}"
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   🚀 WanderFlow AI Travel Planner 一键部署脚本             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."

    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        log_info "安装命令: curl -fsSL https://get.docker.com | sh"
        exit 1
    fi
    log_success "Docker 已安装: $(docker --version)"

    # 检查 Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装"
        exit 1
    fi

    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
    log_success "Docker Compose 已安装"

    # 检查 Git
    if ! command -v git &> /dev/null; then
        log_warning "Git 未安装，部分功能可能受限"
    fi
}

# 检查环境变量
check_env() {
    log_info "检查环境变量配置..."

    if [ ! -f "${ENV_FILE}" ]; then
        log_warning "未找到 .env 文件，正在创建..."
        if [ -f "${ENV_FILE}.example" ]; then
            cp "${ENV_FILE}.example" "${ENV_FILE}"
            log_success "已创建 .env 文件模板"
            log_warning "请编辑 ${ENV_FILE} 填入配置信息"
            log_info "编辑命令: nano ${ENV_FILE}"
            exit 0
        else
            log_error "未找到 .env.example 模板文件"
            exit 1
        fi
    fi

    # 检查关键配置
    if grep -q "your-super-secret-key" "${ENV_FILE}" 2>/dev/null; then
        log_warning "检测到默认 JWT_SECRET_KEY，请修改为随机字符串"
        log_info "生成命令: python -c \"import secrets; print(secrets.token_hex(32))\""
    fi

    if grep -q "sk-ant-api03-xxxxxxxx" "${ENV_FILE}" 2>/dev/null; then
        log_warning "请填入真实的 Anthropic API Key"
    fi

    log_success "环境变量检查完成"
}

# 拉取最新代码
pull_code() {
    log_info "检查代码更新..."

    if [ -d "${SCRIPT_DIR}/.git" ]; then
        cd "${SCRIPT_DIR}"
        if command -v git &> /dev/null; then
            read -p "是否拉取最新代码? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git pull
                log_success "代码已更新"
            fi
        fi
    fi
}

# 构建和启动
deploy() {
    log_info "开始部署 ${PROJECT_NAME}..."

    cd "${COMPOSE_DIR}"

    # 拉取最新镜像（如果有）
    log_info "拉取最新镜像..."
    ${COMPOSE_CMD} pull

    # 构建并启动容器
    log_info "构建并启动容器..."
    ${COMPOSE_CMD} up -d --build

    log_success "部署完成!"
}

# 停止服务
stop() {
    log_info "停止服务..."

    cd "${COMPOSE_DIR}"
    ${COMPOSE_CMD} down

    log_success "服务已停止"
}

# 重启服务
restart() {
    log_info "重启服务..."

    cd "${COMPOSE_DIR}"
    ${COMPOSE_CMD} restart

    log_success "服务已重启"
}

# 查看日志
logs() {
    cd "${COMPOSE_DIR}"

    if [ "$1" = "-f" ]; then
        ${COMPOSE_CMD} logs -f
    else
        ${COMPOSE_CMD} logs --tail=100
    fi
}

# 查看状态
status() {
    cd "${COMPOSE_DIR}"
    ${COMPOSE_CMD} ps

    echo
    log_info "服务健康检查:"
    curl -s http://localhost/health 2>/dev/null && echo " ✅ 后端正常" || echo " ❌ 后端异常"
}

# 清理资源
cleanup() {
    log_warning "此操作将删除所有容器、数据卷和镜像!"
    read -p "确定要继续吗? (输入 'yes' 确认) " -r

    if [ "$REPLY" = "yes" ]; then
        cd "${COMPOSE_DIR}"
        ${COMPOSE_CMD} down -v --rmi all --volumes
        log_success "已清理所有资源"
    else
        log_info "已取消"
    fi
}

# 更新数据库
migrate() {
    log_info "运行数据库迁移..."

    cd "${COMPOSE_DIR}"
    ${COMPOSE_CMD} exec backend python -m alembic upgrade head

    log_success "数据库迁移完成"
}

# 备份数据库
backup() {
    BACKUP_DIR="${SCRIPT_DIR}/backups"
    mkdir -p "${BACKUP_DIR}"

    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="${BACKUP_DIR}/wanderflow_${TIMESTAMP}.sql"

    log_info "正在备份数据库..."

    cd "${COMPOSE_DIR}"
    ${COMPOSE_CMD} exec -T db mysqldump -u root -p"${MYSQL_ROOT_PASSWORD:-password}" wanderflow > "${BACKUP_FILE}"

    log_success "备份完成: ${BACKUP_FILE}"
}

# 恢复数据库
restore() {
    if [ -z "$1" ]; then
        log_error "请指定备份文件路径"
        log_info "用法: $0 restore <backup_file.sql>"
        exit 1
    fi

    if [ ! -f "$1" ]; then
        log_error "备份文件不存在: $1"
        exit 1
    fi

    log_warning "恢复数据库将覆盖现有数据!"
    read -p "确定要继续吗? (输入 'yes' 确认) " -r

    if [ "$REPLY" = "yes" ]; then
        log_info "正在恢复数据库..."

        cd "${COMPOSE_DIR}"
        ${COMPOSE_CMD} exec -T db mysql -u root -p"${MYSQL_ROOT_PASSWORD:-password}" wanderflow < "$1"

        log_success "数据库恢复完成"
    else
        log_info "已取消"
    fi
}

# 显示帮助信息
show_help() {
    echo -e "${BLUE}用法:${NC} $0 <命令> [选项]

${GREEN}可用命令:${NC}
  start       启动所有服务
  stop        停止所有服务
  restart     重启所有服务
  logs        查看日志 (使用 -f 选项实时查看)
  status      查看服务状态
  deploy      部署/更新应用
  migrate     运行数据库迁移
  backup      备份数据库
  restore     恢复数据库 (用法: $0 restore <backup_file.sql>)
  cleanup     清理所有资源（危险！）
  help        显示此帮助信息

${GREEN}示例:${NC}
  $0 deploy           # 部署应用
  $0 logs -f          # 实时查看日志
  $0 restart          # 重启服务
  $0 backup           # 备份数据库
  $0 restore backup.sql  # 恢复数据库

${GREEN}配置文件:${NC}
  环境变量: ${ENV_FILE}
"
}

# 主函数
main() {
    print_banner

    # 解析参数
    COMMAND="${1:-help}"
    shift || true

    case "${COMMAND}" in
        help|--help|-h)
            show_help
            ;;
        start|stop|restart|status)
            check_dependencies
            ${COMMAND}
            ;;
        deploy)
            check_dependencies
            check_env
            pull_code
            deploy
            ;;
        logs)
            check_dependencies
            logs "$@"
            ;;
        migrate)
            check_dependencies
            migrate
            ;;
        backup)
            check_dependencies
            backup
            ;;
        restore)
            check_dependencies
            restore "$@"
            ;;
        cleanup)
            check_dependencies
            cleanup
            ;;
        *)
            log_error "未知命令: ${COMMAND}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
