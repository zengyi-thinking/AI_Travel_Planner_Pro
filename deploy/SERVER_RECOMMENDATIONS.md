# 🖥️ 服务器选购指南

## 📊 配置需求分析

### 最低配置（个人/测试）

| 配置项 | 规格 | 说明 |
|--------|------|------|
| CPU | 1 核 | 足够 1-10 并发用户 |
| 内存 | 2 GB | Python + MySQL 基础需求 |
| 带宽 | 1-2 Mbps | 适合开发测试 |
| 硬盘 | 20 GB SSD | 足够代码和数据库 |
| 月费用 | ¥30-60 | 新用户首年优惠 |

### 推荐配置（生产环境）

| 配置项 | 规格 | 说明 |
|--------|------|------|
| CPU | 2 核 | 支持 10-50 并发用户 |
| 内存 | 4 GB | 稳定运行 Python、MySQL、Redis |
| 带宽 | 3-5 Mbps | 良好用户体验 |
| 硬盘 | 50 GB SSD | 足够数据和日志 |
| 月费用 | ¥80-150 | 性价比最高 |

### 高配配置（生产环境）

| 配置项 | 规格 | 说明 |
|--------|------|------|
| CPU | 4 核 | 支持 50+ 并发用户 |
| 内存 | 8 GB | 流畅运行多个容器 |
| 带宽 | 10 Mbps | 高速访问体验 |
| 硬盘 | 100 GB SSD | 充足存储空间 |
| 月费用 | ¥200-350 | 企业级体验 |

---

## 🏢 推荐服务商

### 🥇 第一梯队：国内访问快，需备案

| 服务商 | 特点 | 官网 | 新用户优惠 |
|--------|------|------|-----------|
| **阿里云** | 稳定、文档完善 | aliyun.com | 首次购买 3-5 折 |
| **腾讯云** | 微信生态集成 | cloud.tencent.com | 学生/新用户优惠大 |
| **火山引擎** | 性价比高 | volcanengine.com | 首年低至 5 折 |

#### 阿里云轻量应用服务器（推荐）

```
配置：2核 4GB 80GB SSD 5Mbps
价格：¥ 612/年（约 ¥51/月）
链接：https://www.aliyun.com/product/swas
```

#### 腾讯云轻量应用服务器

```
配置：2核 4GB 60GB SSD 5Mbps
价格：¥ 379/年（约 ¥32/月）
链接：https://cloud.tencent.com/product/lighthouse
```

### 🥈 第二梯队：国际访问好，无需备案

| 服务商 | 特点 | 官网 |
|--------|------|------|
| **AWS Lightsail** | 稳定、全球节点 | aws.amazon.com/lightsail |
| **Google Cloud** | AI/ML 集成 | cloud.google.com |
| **DigitalOcean** | 开发者友好 | digitalocean.com |
| **Vultr** | 按小时计费 | vultr.com |

#### AWS Lightsail

```
配置：2核 4GB 60GB SSD
价格：$20/月（约 ¥145/月）
特点：全球节点，自动备份
```

#### DigitalOcean Droplet

```
配置：2核 4GB 80GB SSD
价格：$24/月（约 ¥175/月）
特点：开发者友好，一键部署
```

---

## 📋 选购建议

### 场景 1：国内用户为主 ✅ 推荐阿里云/腾讯云

**选择理由**：
- 国内访问速度快（延迟低）
- 备案流程简单（平台提供指导）
- 支付方便（支付宝/微信）
- 技术支持响应快

**推荐配置**：
```
阿里云轻量服务器 2核 4G 5M
价格：¥612/年
```

### 场景 2：海外用户为主 ✅ 推荐 AWS/DigitalOcean

**选择理由**：
- 全球 CDN 加速
- 无需备案
- 国际支付方便
- 技术文档完善

**推荐配置**：
```
AWS Lightsail 2核 4G
价格：$20/月
```

### 场景 3：预算有限 💰

**推荐选择**：
```
火山引擎轻量服务器 2核 2G
价格：¥99/年（首年）
```

---

## 🔧 购买后操作

### 1. 远程连接（SSH）

**Windows 用户**：
1. 下载安装 [PuTTY](https://www.putty.org/) 或 [Xshell](https://www.xshell.com/)
2. 输入服务器 IP 地址
3. 用户名：`root`
4. 密码：购买时设置或短信接收

**Mac/Linux 用户**：
```bash
ssh root@你的服务器IP
```

### 2. 修改 SSH 密码

```bash
# 修改 root 密码
passwd

# 创建新用户（建议）
adduser deploy
usermod -aG sudo deploy

# 切换到新用户
su - deploy
```

### 3. 安装必要软件

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装 Git
sudo apt install git -y

# 安装 unzip（用于解压）
sudo apt install unzip -y
```

### 4. 配置防火墙

```bash
# 安装 ufw
sudo apt install ufw -y

# 开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS

# 启用防火墙
sudo ufw enable
```

### 5. 上传项目

**方式 A：Git 克隆（推荐）**

```bash
# 安装 git（如果未安装）
sudo apt install git -y

# 克隆项目
git clone https://github.com/你的用户名/wanderflow.git
cd wanderflow

# 如果是私有仓库，需要配置 SSH Key
```

**方式 B：本地打包上传**

```bash
# 本地打包
tar -czvf wanderflow.tar.gz wanderflow/

# 上传到服务器（使用 SCP）
scp wanderflow.tar.gz root@服务器IP:/root/

# 服务器上解压
cd /root
tar -xzvf wanderflow.tar.gz
```

---

## 🐳 Docker 部署步骤

```bash
# 1. 进入部署目录
cd wanderflow/deploy/docker

# 2. 配置环境变量
cp .env.example .env
nano .env
# ⚠️ 填入你的配置信息

# 3. 启动服务
cd ..
chmod +x deploy.sh
./deploy.sh deploy

# 4. 检查状态
./deploy.sh status
```

---

## ❓ 常见问题

### Q1: 选择 Linux 还是 Windows 服务器？

**推荐 Linux（Ubuntu）**：
- Docker 支持更好
- 资源占用更低
- 稳定性更高
- 社区支持更广泛

### Q2: 需要独立 IP 吗？

**不需要**：
- 轻量服务器自带公网 IP
- 域名解析到 IP 即可

### Q3: 带宽不够怎么办？

**方案**：
1. 升级带宽（按需付费）
2. 使用 CDN 加速静态资源
3. 优化图片（WebP 格式）

### Q4: 服务器续费多少钱？

**注意**：
- 新用户优惠通常只限首年
- 续费价格可能是新购价的 2-3 倍
- 建议：首年快到期时，考虑重新购买（新用户优惠）

### Q5: 如何迁移服务器？

1. 备份数据库：`./deploy.sh backup`
2. 打包项目：`tar -czvf wanderflow.tar.gz wanderflow/`
3. 上传到新服务器
4. 在新服务器恢复：`./deploy.sh restore`

---

## 💰 成本对比表

| 方案 | 月费用 | 年费用 | 适用场景 |
|------|--------|--------|----------|
| 火山引擎 2核2G | ¥8/月 | ¥99/年 | 个人测试 |
| 腾讯云 2核4G | ¥32/月 | ¥379/年 | 小型项目 |
| 阿里云 2核4G | ¥51/月 | ¥612/年 | 生产环境 |
| AWS Lightsail | ¥145/月 | ¥1740/年 | 海外用户 |
| 阿里云 4核8G | ¥180/月 | ¥2160/年 | 高并发 |

---

## 📞 技术支持

如果遇到问题：

1. **阿里云**：控制台 → 工单 → 提交问题
2. **腾讯云**：控制台 → 工具 → 工单
3. **社区**：Stack Overflow、CSDN、SegmentFault
4. **项目**：[GitHub Issues](https://github.com/your-username/wanderflow/issues)
