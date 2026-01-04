# WanderFlow 部署指南

## 📋 目录

- [快速开始](#快速开始)
- [准备工作](#准备工作)
- [本地测试](#本地测试)
- [服务器部署](#服务器部署)
- [域名配置](#域名配置)
- [HTTPS 配置](#https-配置)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 方式一：Docker 一键部署（推荐）

```bash
# 1. 进入部署目录
cd deploy/docker

# 2. 配置环境变量
cp .env.example .env
nano .env  # 编辑配置

# 3. 启动服务
cd ..
./deploy.sh deploy
```

### 方式二：手动部署

```bash
# 1. 安装 Docker
curl -fsSL https://get.docker.com | sh

# 2. 安装 Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 3. 配置并启动
cd deploy/docker
cp .env.example .env
# 编辑 .env 文件

docker-compose up -d
```

---

## 准备工作

### 1. 购买服务器

推荐配置：
- **CPU**: 2核
- **内存**: 4GB
- **带宽**: 3-5Mbps
- **硬盘**: 50GB SSD

推荐服务商：
- [阿里云轻量应用服务器](https://www.aliyun.com/product/swas)
- [腾讯云轻量应用服务器](https://cloud.tencent.com/product/lighthouse)

### 2. 购买域名

推荐服务商：
- [阿里云](https://www.aliyun.com/domain)
- [腾讯云](https://cloud.tencent.com/act/domain)
- [GoDaddy](https://www.godaddy.com)

### 3. 准备 API Key

需要申请 [Anthropic API Key](https://www.anthropic.com/):
1. 访问 Anthropic 官网注册账号
2. 进入 Console → API Keys
3. 创建新的 API Key
4. 充值或确保账户有足够余额

---

## 本地测试

### 1. 配置环境变量

```bash
cd deploy/docker

# 复制模板
cp .env.example .env

# 编辑配置
nano .env
```

修改以下关键配置：

```env
# 数据库（本地测试使用 SQLite）
DATABASE_URL=sqlite+aiosqlite:///./wanderflow.db

# JWT 密钥（生成随机字符串）
JWT_SECRET_KEY=your-random-secret-key-here

# AI API Key
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxx

# 域名配置
DOMAIN=http://localhost:8000
```

### 2. 启动服务

```bash
# 使用 Docker Compose 启动
docker-compose up -d

# 或使用一键部署脚本
cd ..
./deploy.sh deploy
```

### 3. 验证服务

```bash
# 检查服务状态
./deploy.sh status

# 查看日志
./deploy.sh logs -f

# 健康检查
curl http://localhost/health
```

预期输出：
```json
{"status":"healthy","version":"1.0.0"}
```

---

## 服务器部署

### 1. 连接服务器

```bash
# 使用 SSH 连接（Windows 用户可使用 PuTTY 或 Xshell）
ssh root@你的服务器IP
```

### 2. 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 添加当前用户到 docker 组
sudo usermod -aG docker $USER

# 验证安装
docker --version
docker-compose --version
```

### 3. 上传项目

**方式 A：使用 Git（推荐）**

```bash
# 安装 Git
apt install git -y

# 克隆项目
git clone https://github.com/你的用户名/wanderflow.git
cd wanderflow
```

**方式 B：使用 SCP 上传**

```bash
# 从本地上传文件到服务器
scp -r deploy/ root@服务器IP:/root/wanderflow/
```

### 4. 配置环境变量

```bash
cd deploy/docker

# 复制环境变量模板
cp .env.example .env

# 编辑配置
nano .env
```

填写以下配置：

```env
# 数据库配置（使用 MySQL）
DATABASE_URL=mysql+pymysql://root:你的密码@db:3306/wanderflow

# JWT 密钥（生成随机字符串）
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxx

# 域名配置（生产环境域名）
DOMAIN=https://your-domain.com

# 调试模式（设为 false）
DEBUG=false
```

### 5. 启动服务

```bash
# 一键部署
cd ..
chmod +x deploy.sh
./deploy.sh deploy
```

### 6. 验证部署

```bash
# 检查服务状态
./deploy.sh status

# 查看日志
./deploy.sh logs

# 测试 API
curl http://localhost/api/v1/auth/quota -H "Authorization: Bearer your-token"
```

---

## 域名配置

### 1. 添加 A 记录

登录域名控制台，添加以下记录：

| 主机记录 | 记录类型 | 记录值 |
|---------|---------|--------|
| @ | A | 你的服务器 IP |
| www | A | 你的服务器 IP |

### 2. 等待生效

域名解析通常在 **10分钟-2小时** 内生效，可通过以下命令验证：

```bash
# Linux/Mac
dig 你的域名

# 或
nslookup 你的域名

# Windows
nslookup 你的域名
```

---

## HTTPS 配置

### 方式一：Let's Encrypt 免费证书（推荐）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书（自动配置 Nginx）
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 方式二：阿里云/腾讯云 SSL 证书

1. 登录云服务商控制台
2. 进入 SSL 证书页面
3. 申请免费证书
4. 下载证书文件（Nginx 格式）
5. 上传到服务器 `/etc/nginx/ssl/`

### 配置 Nginx HTTPS

编辑 `nginx/production.conf`，取消 HTTPS 配置的注释：

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/your-domain.com.pem;
    ssl_certificate_key /etc/nginx/ssl/your-domain.com.key;

    # ... 其他配置
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}
```

---

## 常用维护命令

```bash
# 进入部署目录
cd deploy

# 服务管理
./deploy.sh start      # 启动服务
./deploy.sh stop       # 停止服务
./deploy.sh restart    # 重启服务
./deploy.sh status     # 查看状态

# 日志查看
./deploy.sh logs       # 查看最近 100 行日志
./deploy.sh logs -f    # 实时查看日志

# 数据库操作
./deploy.sh backup              # 备份数据库
./deploy.sh restore backup.sql  # 恢复数据库

# 系统清理
./deploy.sh cleanup  # 清理所有 Docker 资源（危险！）
```

---

## 常见问题

### Q1: Docker 权限错误

```bash
# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker
```

### Q2: 数据库连接失败

```bash
# 检查数据库状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 检查连接字符串是否正确
cat .env | grep DATABASE_URL
```

### Q3: 前端静态资源加载失败

```bash
# 重新构建前端
cd deploy/docker
docker-compose build frontend
docker-compose up -d frontend
```

### Q4: API 请求超时

```bash
# 增加 Nginx 超时时间
# 编辑 nginx 配置，增加以下内容：

location /api/ {
    proxy_connect_timeout 300;
    proxy_send_timeout 300;
    proxy_read_timeout 300;
    # ... 其他配置
}
```

### Q5: 如何更新应用

```bash
cd deploy

# 拉取最新代码
git pull

# 重新部署
./deploy.sh deploy
```

### Q6: 查看资源使用情况

```bash
# Docker 容器资源使用
docker stats

# 磁盘使用
df -h

# 内存使用
free -h
```

---

## 成本估算

| 项目 | 月费用 |
|------|--------|
| 服务器（2核4G） | ¥100-200 |
| 域名 | ¥30-80/年 |
| SSL 证书 | 免费 |
| API 调用费用 | 按量付费 |

**总计**: 约 ¥100-200/月 + API 调用费用

---

## 技术支持

如果遇到问题：

1. 查看日志：`./deploy.sh logs`
2. 检查服务状态：`./deploy.sh status`
3. 健康检查：`curl http://localhost/health`
4. 查看 [常见问题](#常见问题)

---

## 下一步

- [ ] 配置 HTTPS（推荐）
- [ ] 配置自动备份
- [ ] 配置监控告警
- [ ] 配置日志轮转
