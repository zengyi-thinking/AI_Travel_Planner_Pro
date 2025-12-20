# WanderFlow Backend - app.py 使用指南

## 概述

`app.py` 是 WanderFlow 后端的完整应用入口文件，提供了所有核心功能模块的 API 接口。

## 快速开始

### 启动服务

```bash
cd backend

# 激活虚拟环境
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac

# 启动服务
python app.py
```

### 指定端口

```bash
python app.py 3000
```

## 功能模块

### 1. 健康检查
- `GET /` - 根路径，返回应用信息
- `GET /health` - 健康检查
- `GET /api/v1/health` - 健康检查 (API路径)

### 2. 用户认证 (Auth)
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/users/me` - 获取当前用户信息

### 3. 行程规划 (Planner)
- `GET /api/v1/itineraries` - 获取行程列表
- `POST /api/v1/itineraries` - 创建行程
- `GET /api/v1/itineraries/{id}` - 获取行程详情
- `POST /api/v1/itineraries/{id}/generate` - AI生成行程

### 4. 智能问答 (QA)
- `POST /api/v1/qa/chat` - 发送聊天消息
- `GET /api/v1/qa/sessions` - 获取对话列表
- `POST /api/v1/qa/sessions` - 创建新对话

### 5. 文案生成 (Copywriting)
- `POST /api/v1/copywriting/generate` - 生成文案
- `GET /api/v1/copywriting/results` - 获取文案历史

## API 文档

启动服务后，访问以下地址查看 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 技术特性

- ✅ FastAPI 框架
- ✅ 异步支持
- ✅ 自动生成 API 文档
- ✅ CORS 支持
- ✅ 错误处理
- ✅ 热重载开发模式

## 目录结构

```
backend/
├── app.py                 # 主入口文件
├── app/                   # 应用源码
│   ├── main.py           # 原始完整入口 (未启用)
│   ├── core/             # 核心模块
│   │   ├── config/       # 配置管理
│   │   ├── db/           # 数据库
│   │   ├── security/     # 安全认证
│   │   ├── ai/           # AI 集成
│   │   └── tools/        # 工具函数
│   ├── common/           # 公共层
│   │   ├── dtos/         # 数据传输对象
│   │   └── exceptions/   # 异常处理
│   └── modules/          # 业务模块
│       ├── users/        # 用户模块
│       ├── planner/      # 行程规划模块
│       ├── qa/           # 问答模块
│       └── copywriter/   # 文案生成模块
├── venv/                 # 虚拟环境
└── requirements.txt      # 依赖列表
```

## 开发说明

### 添加新的 API 路由

在 `app.py` 中添加新的路由处理器：

```python
@app.get("/api/v1/example", tags=["example"])
async def example_endpoint():
    return {"message": "Example endpoint"}
```

### 使用完整的应用结构

如果需要使用完整的应用结构（数据库、认证等），可以修改 `app.py` 中的导入：

```python
# 启用完整模块导入
from app.core.config import settings
from app.core.db.session import engine, AsyncSessionLocal
from app.core.db.base import Base

# 导入完整的路由
from app.modules.users.api.v1 import router as users_router
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
```

## 常见问题

### Q: 如何停止服务？
A: 在终端中按 `Ctrl+C`

### Q: 如何查看日志？
A: 服务启动后会显示实时日志

### Q: 如何修改端口？
A: 在启动时指定端口号：`python app.py 3000`

## 下一步

- 实现具体的业务逻辑
- 连接数据库
- 添加用户认证
- 集成 AI 服务
- 完善 API 文档

---

更多信息请查看项目主文档。
