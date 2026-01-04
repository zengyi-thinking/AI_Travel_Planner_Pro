# 🔄 CI/CD 自动化部署配置

## 概述

本项目配置了完整的 CI/CD 流程：

1. **CI（持续集成）**：代码提交后自动测试、构建
2. **CD（持续部署）**：测试通过后自动部署到服务器
3. **定时备份**：每天自动备份数据库

---

## 📁 配置文件

| 文件 | 说明 |
|------|------|
| `.github/workflows/ci.yml` | 测试与构建流程 |
| `.github/workflows/deploy.yml` | 自动部署流程 |
| `.github/workflows/schedule-backup.yml` | 定时备份流程 |

---

## 🚀 快速开始

### 1. 推送代码到 GitHub

```bash
# 初始化 Git 仓库（如果尚未初始化）
git init
git add .
git commit -m "Initial commit"

# 创建 GitHub 仓库并推送
# 在 GitHub 网站创建仓库后：
git remote add origin https://github.com/你的用户名/wanderflow.git
git branch -M main
git push -u origin main
```

### 2. 配置 GitHub Secrets

在 GitHub 仓库页面，依次点击：

**Settings → Secrets and variables → Actions**

添加以下 Secret：

#### 必需 Secrets

| Secret 名称 | 值 | 说明 |
|-------------|-----|------|
| `ANTHROPIC_API_KEY` | 你的 Anthropic API Key | AI 功能测试 |

#### 部署 Secrets（部署到服务器需要）

| Secret 名称 | 值 | 说明 |
|-------------|-----|------|
| `SERVER_HOST` | 服务器 IP 地址 | 如 `123.45.67.89` |
| `SERVER_USER` | SSH 用户名 | 通常是 `root` |
| `SERVER_SSH_KEY` | SSH 私钥内容 | 服务器 SSH 私钥 |

#### 可选 Secrets

| Secret 名称 | 值 | 说明 |
|-------------|-----|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 部署通知 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 部署通知 |

---

## 📋 工作流说明

### CI 工作流（ci.yml）

```
触发条件：
├── push 到 main/master 分支
├── pull request 到 main/master 分支
└── 忽略 docs/ 目录和 *.md 文件

执行步骤：
1. 前端构建测试
   ├── 安装 Node.js 20
   ├── 安装 npm 依赖
   ├── 运行 ESLint 检查
   ├── 类型检查
   └── 构建前端（验证无编译错误）

2. 后端测试
   ├── 安装 Python 3.11
   ├── 安装依赖
   ├── 启动 MySQL 测试数据库
   └── 运行 pytest 测试

3. Docker 构建
   └── 构建并推送到 GitHub Container Registry
```

### CD 工作流（deploy.yml）

```
触发条件：
└── CI 工作流成功完成后

执行步骤：
1. 构建最新 Docker 镜像
2. SSH 连接到服务器
3. 拉取最新代码
4. 拉取最新镜像
5. 重启 Docker 容器
6. 清理旧镜像
7. 发送 Telegram 通知（如果配置了）
```

### 备份工作流（schedule-backup.yml）

```
触发条件：
├── 每天凌晨 3 点（自动）
└── 手动触发（workflow_dispatch）

执行步骤：
1. SSH 连接到服务器
2. 执行数据库备份
3. 上传备份文件到 GitHub Actions
4. 发送 Telegram 通知
```

---

## 🛠️ 服务器配置

### 1. 生成 SSH 密钥

```bash
# 在本地生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your-email@example.com"

# 查看公钥（添加到服务器）
cat ~/.ssh/id_ed25519.pub

# 查看私钥（添加到 GitHub Secrets）
cat ~/.ssh/id_ed25519
```

### 2. 配置服务器 SSH

```bash
# 连接到服务器
ssh root@你的服务器IP

# 编辑 SSH 配置
nano /etc/ssh/sshd_config

# 确保以下配置：
# PasswordAuthentication no  # 禁用密码登录（可选）
# PubkeyAuthentication yes  # 启用公钥登录

# 重启 SSH 服务
systemctl restart sshd

# 将公钥添加到 authorized_keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "你的公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 3. 在服务器上准备项目

```bash
# 连接到服务器
ssh root@你的服务器IP

# 安装 Docker（如果未安装）
curl -fsSL https://get.docker.com | sh

# 克隆项目
git clone https://github.com/你的用户名/wanderflow.git
cd wanderflow

# 配置环境变量
cd deploy/docker
cp .env.example .env
nano .env

# 启动服务（首次部署）
cd ..
chmod +x deploy.sh
./deploy.sh deploy
```

---

## 📱 配置 Telegram 通知（可选）

### 1. 创建 Telegram Bot

1. 在 Telegram 中搜索 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 获取 Bot Token

### 2. 获取 Chat ID

1. 在 Telegram 中搜索 @userinfobot
2. 发送任意消息获取你的 Chat ID

### 3. 添加到 GitHub Secrets

- `TELEGRAM_BOT_TOKEN`: 你获取的 Bot Token
- `TELEGRAM_CHAT_ID`: 你的 Chat ID

---

## ✅ 验证 CI/CD

### 1. 推送代码触发 CI

```bash
# 创建一个测试提交
echo "Test CI/CD" >> README.md
git add .
git commit -m "Test CI/CD"
git push origin main
```

### 2. 查看 GitHub Actions

访问 `https://github.com/你的用户名/wanderflow/actions` 查看：

- ✅ CI 工作流是否成功
- ✅ 构建产物是否生成
- ✅ 测试是否通过

### 3. 手动触发部署

如果 CI 通过，可以在 GitHub Actions 页面手动触发 CD：

1. 进入 Actions 标签
2. 选择 "CD - 自动部署"
3. 点击 "Run workflow"
4. 选择分支并运行

---

## 🐛 常见问题

### Q1: CI 构建失败

**检查步骤**：
1. 查看 GitHub Actions 日志
2. 常见问题：
   - `npm install` 失败 → 检查 package-lock.json
   - `pytest` 失败 → 检查测试用例
   - Docker 构建失败 → 检查 Dockerfile

### Q2: 部署时连接服务器失败

**检查步骤**：
1. 确认服务器 IP 是否正确
2. 确认 SSH 密钥是否正确添加到 Secrets
3. 确认服务器是否允许 SSH 连接
4. 检查防火墙是否开放 22 端口

### Q3: Docker 镜像拉取失败

**检查步骤**：
1. 确认 GitHub Container Registry 登录是否正确
2. 确认镜像标签是否正确
3. 检查网络连接

### Q4: 部署后服务无法访问

**服务器上检查**：
```bash
# 查看容器状态
./deploy.sh status

# 查看日志
./deploy.sh logs

# 检查端口占用
netstat -tlnp
```

---

## 📊 工作流状态徽章

在 README.md 中添加状态徽章：

```markdown
![CI Status](https://github.com/你的用户名/wanderflow/actions/workflows/ci.yml/badge.svg)
![CD Status](https://github.com/你的用户名/wanderflow/actions/workflows/deploy.yml/badge.svg)
```

---

## 🔒 安全建议

1. **不要在代码中暴露 Secrets**：全部使用 GitHub Secrets
2. **定期轮换密钥**：API Key、SSH 密钥定期更换
3. **限制分支保护**：main 分支设置 PR 审查要求
4. **使用最小权限**：部署用户使用 sudo 权限而非 root
