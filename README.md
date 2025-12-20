# WanderFlow - AI智能旅行规划助手

<div align="center">

![WanderFlow Logo](https://via.placeholder.com/200x200/14b8a6/ffffff?text=WanderFlow)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-username/wanderflow)
[![FastAPI](https://img.shields.io/badge/FastAPI-00599C?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=flat&logo=Vue.js&logoColor=white)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=TypeScript&logoColor=white)](https://www.typescriptlang.org/)

</div>

## 📖 项目简介

WanderFlow 是一款基于AI的智能旅行规划助手，帮助用户快速生成个性化旅行行程、生成社交媒体文案，并提供智能问答服务。

### ✨ 核心功能

- **🗺️ 智能行程规划** - AI驱动的个性化行程推荐
- **🤖 AI旅行助手** - 智能问答，解答旅行相关问题
- **✍️ 文案生成器** - 一键生成朋友圈/小红书/微博文案
- **⚙️ 个人设置** - 完整的用户配置和偏好管理

## 🏗️ 技术架构

### 后端 (FastAPI + Core+Modules)

```
backend/
├── app/
│   ├── core/               # 核心层 - 基础设施
│   │   ├── config/         # 配置管理
│   │   ├── db/             # 数据库
│   │   ├── security/       # 安全认证
│   │   ├── ai/             # AI模块
│   │   └── tools/          # 工具函数
│   ├── common/             # 公共层 - 通用组件
│   │   ├── dtos/           # 数据传输对象
│   │   └── exceptions/     # 异常处理
│   └── modules/            # 模块层 - 业务模块
│       ├── users/          # 用户模块
│       ├── planner/        # 行程规划模块
│       ├── qa/             # 问答模块
│       └── copywriter/     # 文案生成模块
```

### 前端 (Vue 3 + TypeScript)

```
frontend/
├── src/
│   ├── views/              # 页面组件
│   ├── components/         # 公共组件
│   ├── stores/             # Pinia状态管理
│   ├── composables/        # 组合式函数
│   ├── utils/              # 工具函数
│   └── types/              # 类型定义
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 7.0+

### 后端部署

1. **克隆项目**

```bash
git clone https://github.com/your-username/wanderflow.git
cd wanderflow
```

2. **创建虚拟环境**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库、Redis等信息
```

5. **初始化数据库**

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE wanderflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 运行迁移
alembic upgrade head
```

6. **启动服务**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端部署

1. **安装依赖**

```bash
cd frontend
npm install
# 或
pnpm install
```

2. **配置环境变量**

```bash
cp .env.example .env.local
# 编辑 .env.local 文件
```

3. **启动开发服务器**

```bash
npm run dev
# 或
pnpm dev
```

4. **构建生产版本**

```bash
npm run build
# 或
pnpm build
```

## 📚 开发指南

### 代码规范

#### 后端

- **遵循 PEP 8** 代码风格
- **使用 Black** 进行代码格式化
- **使用 isort** 整理导入语句
- **使用 MyPy** 进行类型检查

```bash
# 格式化代码
black app/
isort app/

# 类型检查
mypy app/
```

#### 前端

- **遵循 Vue 3 官方风格指南**
- **使用 TypeScript** 严格模式
- **使用 ESLint** 进行代码检查
- **使用 Prettier** 进行代码格式化

```bash
# 代码检查和修复
npm run lint

# 代码格式化
npm run format
```

### 项目结构说明

#### 后端架构 - Core + Modules

**Core 层 (基础设施层)**
- `config/` - 应用配置管理
- `db/` - 数据库连接和模型
- `security/` - JWT认证和安全
- `ai/` - AI/LLM集成
- `tools/` - 通用工具函数

**Common 层 (公共层)**
- `dtos/` - 数据传输对象
- `exceptions/` - 自定义异常类

**Modules 层 (业务模块)**
- `users/` - 用户管理（注册、登录、资料）
- `planner/` - 行程规划（AI生成、CRUD）
- `qa/` - 智能问答（聊天、RAG）
- `copywriter/` - 文案生成（模板、平台适配）

#### 前端架构 - Views + Components

**页面层 (Views)**
- `Home.vue` - 首页
- `Login.vue` / `Register.vue` - 认证页面
- `Planner.vue` - 行程规划
- `QA.vue` - AI助手
- `Copywriter.vue` - 文案生成
- `Settings.vue` - 设置页面

**组件层 (Components)**
- `common/` - 通用组件
- `auth/` - 认证相关组件
- `chat/` - 聊天组件
- `planner/` - 行程规划组件
- `copywriter/` - 文案生成组件
- `settings/` - 设置组件

### API 文档

启动后端服务后，访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 测试

### 后端测试

```bash
cd backend
pytest
```

### 前端测试

```bash
cd frontend
npm run test
```

## 📦 部署

### Docker 部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 生产环境部署

#### 后端部署

1. 使用 Gunicorn 作为 WSGI 服务器

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. 配置 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 前端部署

1. 构建项目

```bash
npm run build
```

2. 使用 Nginx 部署静态文件

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/wanderflow/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 🔧 配置说明

### 后端环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DB_HOST` | 数据库主机 | localhost |
| `DB_PORT` | 数据库端口 | 3306 |
| `DB_USER` | 数据库用户 | root |
| `DB_PASSWORD` | 数据库密码 | - |
| `DB_NAME` | 数据库名称 | wanderflow_db |
| `REDIS_HOST` | Redis主机 | localhost |
| `REDIS_PORT` | Redis端口 | 6379 |
| `SECRET_KEY` | JWT密钥 | - |
| `OPENAI_API_KEY` | OpenAI API密钥 | - |

### 前端环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `VITE_API_BASE_URL` | API基础URL | http://localhost:8000/api |
| `VITE_APP_TITLE` | 应用标题 | WanderFlow |

## 📝 更新日志

### v1.0.0 (2024-12-20)

- ✨ 初始版本发布
- 🗺️ 实现AI行程规划功能
- 🤖 实现智能问答助手
- ✍️ 实现文案生成功能
- ⚙️ 实现用户认证和设置

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式化
refactor: 重构代码
test: 添加测试
chore: 更新依赖或构建配置
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👥 团队

- **项目负责人**: Alex Chen
- **后端开发**: [Your Name]
- **前端开发**: [Your Name]
- **UI/UX 设计**: [Your Name]

## 📞 联系我们

- 📧 邮箱: contact@wanderflow.com
- 🐦 微博: [@WanderFlowApp](https://weibo.com/wanderflow)
- 💬 微信群: 扫描二维码加入

## 🙏 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/) - 现代高性能Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的CSS框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL工具包
- [Pydantic](https://docs.pydantic.dev/) - 数据验证库

## 📊 项目统计

![GitHub stars](https://img.shields.io/github/stars/your-username/wanderflow?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-username/wanderflow?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/your-username/wanderflow?style=social)

---

<div align="center">

**用 ❤️ 和 AI 打造的智能旅行助手**

[⬆️ 回到顶部](#wanderflow---ai智能旅行规划助手)

</div>
