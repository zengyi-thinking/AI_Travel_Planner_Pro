# 快速开始指南

欢迎使用 WanderFlow！本指南将帮助您在 5 分钟内启动项目。

## 🚀 快速启动

### 方式一：使用 Docker (推荐)

如果您已安装 Docker 和 Docker Compose：

```bash
# 克隆项目
git clone <repository-url>
cd wanderflow

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app
```

服务启动后，访问：
- 前端应用：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 方式二：本地开发

#### 1. 环境准备

确保您已安装以下软件：
- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 7.0+

#### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置文件
cp .env.example .env

# 编辑 .env 文件，配置数据库和 Redis
# 注意：需要先创建 MySQL 数据库
```

创建 MySQL 数据库：

```sql
mysql -u root -p -e "CREATE DATABASE wanderflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

运行数据库迁移：

```bash
alembic upgrade head
```

启动后端服务：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 前端设置

打开新终端窗口：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
# 或使用 pnpm
pnpm install

# 复制环境配置文件
cp .env.example .env.local

# 启动开发服务器
npm run dev
# 或
pnpm dev
```

前端应用将在 http://localhost:3000 启动

## 📝 首次使用

### 1. 创建管理员账户

访问 http://localhost:3000/register 注册新用户

### 2. 体验功能

- **行程规划**: 创建您的第一个 AI 行程
- **AI 助手**: 向 WanderBot 提问
- **文案生成**: 为您的旅行照片生成文案

### 3. 查看 API 文档

访问 http://localhost:8000/docs 查看 Swagger UI 文档

## 🛠️ 开发工作流

### 代码格式化

```bash
# 后端
cd backend
black app/
isort app/

# 前端
cd frontend
npm run format
npm run lint
```

### 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

### 数据库迁移

```bash
cd backend

# 创建新迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

## 📁 项目结构概览

```
wanderflow/
├── backend/              # 后端 (FastAPI)
│   ├── app/
│   │   ├── core/         # 核心层
│   │   ├── common/       # 公共层
│   │   └── modules/      # 业务模块
│   ├── requirements.txt  # 依赖
│   └── .env.example      # 环境变量示例
│
├── frontend/             # 前端 (Vue 3)
│   ├── src/
│   │   ├── views/        # 页面
│   │   ├── stores/       # 状态管理
│   │   ├── components/   # 组件
│   │   └── utils/        # 工具
│   ├── package.json      # 依赖
│   └── .env.example      # 环境变量示例
│
├── docs/                 # 文档
│   ├── BACKEND.md        # 后端指南
│   └── FRONTEND.md       # 前端指南
│
└── README.md             # 主文档
```

## 🔧 常用命令

### 后端

```bash
# 启动服务
uvicorn app.main:app --reload

# 代码格式化
black app/ && isort app/

# 类型检查
mypy app/

# 运行测试
pytest
```

### 前端

```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint

# 代码格式化
npm run format

# 类型检查
npm run type-check
```

## 🐛 常见问题

### Q: 数据库连接失败？

A: 检查 `.env` 文件中的数据库配置是否正确，并确保 MySQL 服务已启动。

```bash
# 检查 MySQL 状态
sudo systemctl status mysql

# 重启 MySQL
sudo systemctl restart mysql
```

### Q: Redis 连接失败？

A: 检查 Redis 服务是否启动：

```bash
# 检查 Redis 状态
redis-cli ping
# 应该返回 PONG

# 启动 Redis
redis-server
```

### Q: 前端页面空白？

A: 检查浏览器控制台是否有错误，通常是 API 代理配置问题。

检查 `frontend/vite.config.ts` 中的代理设置：

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

### Q: CORS 错误？

A: 后端需要配置 CORS。检查 `app/main.py`：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Q: 模块导入错误？

A: 检查 Python 路径设置：

```bash
# 在 backend 目录下运行
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 或使用
python -m uvicorn app.main:app --reload
```

## 📚 进阶阅读

- [后端开发指南](docs/BACKEND.md)
- [前端开发指南](docs/FRONTEND.md)
- [API 文档](http://localhost:8000/docs)
- [架构设计](README.md#技术架构)

## 💡 提示

1. **使用环境变量**: 不要在代码中硬编码配置
2. **代码提交前检查**: 运行 linting 和测试
3. **及时更新文档**: 修改代码时更新相关文档
4. **版本控制**: 使用有意义的 commit 消息

## 🆘 获取帮助

- 📧 邮箱: support@wanderflow.com
- 💬 讨论区: [GitHub Discussions](https://github.com/your-repo/discussions)
- 🐛 报告 Bug: [GitHub Issues](https://github.com/your-repo/issues)

---

祝您使用愉快！🎉
