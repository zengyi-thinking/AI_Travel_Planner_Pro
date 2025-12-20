# 后端开发指南

## 目录

- [架构设计](#架构设计)
- [项目结构](#项目结构)
- [核心模块](#核心模块)
- [开发规范](#开发规范)
- [数据库设计](#数据库设计)
- [API接口](#api接口)
- [测试指南](#测试指南)
- [常见问题](#常见问题)

## 架构设计

### Core + Modules 三层架构

WanderFlow 后端采用 **Core + Modules** 三层架构模式，实现清晰的分层和职责分离：

```
┌─────────────────────────────────────┐
│           Modules Layer             │  ← 业务逻辑层
│  (users, planner, qa, copywriter)  │
├─────────────────────────────────────┤
│            Common Layer             │  ← 公共组件层
│     (dtos, exceptions, utils)       │
├─────────────────────────────────────┤
│            Core Layer               │  ← 基础设施层
│  (config, db, security, ai, tools)  │
└─────────────────────────────────────┘
```

#### Core 层 (基础设施层)

**职责**: 提供底层基础设施和公共服务

- **config/** - 应用配置管理 (Pydantic Settings)
- **db/** - 数据库连接、会话管理、模型基类
- **security/** - JWT认证、安全策略、权限控制
- **ai/** - AI/LLM集成抽象层，支持多提供商
- **tools/** - 通用工具函数 (日期、文件、验证等)

#### Common 层 (公共组件层)

**职责**: 提供跨模块共享的通用组件

- **dtos/** - 数据传输对象 (请求/响应模型)
- **exceptions/** - 自定义异常类层次结构

#### Modules 层 (业务模块层)

**职责**: 实现具体的业务功能

- **users/** - 用户认证与资料管理
- **planner/** - AI驱动的行程规划
- **qa/** - 智能问答与RAG
- **copywriter/** - 社交媒体文案生成

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   │
│   ├── core/                   # 核心层 - 基础设施
│   │   ├── __init__.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py     # 应用配置
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # 模型基类
│   │   │   └── session.py      # 数据库会话
│   │   │
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py          # JWT 工具
│   │   │   └── deps.py         # 依赖注入
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   └── factory.py      # AI 工厂模式
│   │   │
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── date_utils.py   # 日期工具
│   │
│   ├── common/                 # 公共层 - 通用组件
│   │   ├── __init__.py
│   │   ├── dtos/
│   │   │   ├── __init__.py
│   │   │   └── base.py         # 基础 DTO
│   │   │
│   │   └── exceptions/
│   │       ├── __init__.py
│   │       └── base.py         # 基础异常
│   │
│   └── modules/                # 模块层 - 业务模块
│       ├── __init__.py
│       │
│       ├── users/              # 用户模块
│       │   ├── __init__.py
│       │   ├── api/
│       │   │   └── v1.py       # API 路由
│       │   ├── schemas/
│       │   │   └── user.py     # 用户模型
│       │   ├── models/
│       │   │   └── user.py     # 数据库模型
│       │   ├── daos/
│       │   │   └── user_dao.py # 数据访问层
│       │   └── services/
│       │       └── user_service.py # 业务逻辑
│       │
│       ├── planner/            # 行程规划模块
│       │   ├── __init__.py
│       │   ├── agents/         # AI 智能体
│       │   ├── tools/          # 工具函数
│       │   ├── prompts/        # 提示词模板
│       │   ├── api/
│       │   ├── schemas/
│       │   ├── models/
│       │   ├── daos/
│       │   └── services/
│       │
│       ├── qa/                 # 问答模块
│       │   ├── __init__.py
│       │   ├── rag/            # RAG 专属逻辑
│       │   ├── api/
│       │   ├── schemas/
│       │   ├── models/
│       │   ├── daos/
│       │   └── services/
│       │
│       └── copywriter/         # 文案生成模块
│           ├── __init__.py
│           ├── templates/      # 文案模板库
│           ├── api/
│           ├── schemas/
│           ├── models/
│           ├── daos/
│           └── services/
│
├── alembic/                    # 数据库迁移
│   ├── versions/
│   └── env.py
│
├── tests/                      # 测试目录
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users/
│   ├── test_planner/
│   ├── test_qa/
│   └── test_copywriter/
│
├── requirements.txt            # Python 依赖
├── .env.example               # 环境变量示例
├── alembic.ini               # 数据库迁移配置
└── README.md
```

## 核心模块

### 1. 配置管理 (config/settings.py)

使用 Pydantic Settings 管理应用配置：

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "WanderFlow"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # 数据库配置
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "wanderflow_db"

    # JWT 配置
    secret_key: str
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    # OpenAI 配置
    openai_api_key: Optional[str] = None
    openai_base_url: str = "https://api.openai.com/v1"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. 数据库 (db/session.py)

异步数据库会话管理：

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    f"mysql+aiomysql://{settings.db_user}:{settings.db_password}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}",
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### 3. JWT 认证 (security/jwt.py)

JWT Token 创建和验证：

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
```

### 4. AI 工厂模式 (ai/factory.py)

支持多 AI 提供商的抽象层：

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, prompt: str, **kwargs) -> str:
        # 实现 OpenAI 调用
        pass

class LLMFactory:
    _providers: Dict[str, BaseLLMProvider] = {}

    @classmethod
    def register_provider(cls, name: str, provider: BaseLLMProvider):
        cls._providers[name] = provider

    @classmethod
    def get_provider(cls, name: str) -> Optional[BaseLLMProvider]:
        return cls._providers.get(name)

# 注册默认提供商
LLMFactory.register_provider("openai", OpenAIProvider(settings.openai_api_key))
```

## 开发规范

### 代码风格

1. **遵循 PEP 8** - Python 代码风格指南
2. **使用 Black** - 代码格式化工具
3. **使用 isort** - 导入语句排序
4. **使用 MyPy** - 静态类型检查

```bash
# 安装开发工具
pip install black isort mypy

# 格式化代码
black app/
isort app/

# 类型检查
mypy app/
```

### 命名约定

- **文件名**: 小写字母，下划线分隔 (`user_service.py`)
- **类名**: PascalCase (`UserService`)
- **函数/变量**: snake_case (`get_user_by_id`)
- **常量**: UPPER_CASE (`MAX_RETRIES`)
- **私有成员**: 前缀下划线 (`_private_method`)

### 文档字符串

使用 Google 风格的 docstring：

```python
def create_user(email: str, name: str) -> User:
    """创建新用户。

    Args:
        email: 用户邮箱
        name: 用户姓名

    Returns:
        创建的用户对象

    Raises:
        ValueError: 当邮箱已存在时
    """
    pass
```

## 数据库设计

### 模型基类 (core/db/base.py)

```python
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

### 示例模型 (modules/users/models/user.py)

```python
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.core.db.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    membership_level = Column(Enum('free', 'pro', name='membership_levels'), default='free')

    # 关系
    itineraries = relationship("Itinerary", back_populates="user")
```

## API 接口

### 用户模块 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 | ❌ |
| POST | `/api/v1/auth/login` | 用户登录 | ❌ |
| GET | `/api/v1/users/me` | 获取当前用户信息 | ✅ |
| PATCH | `/api/v1/users/me` | 更新用户信息 | ✅ |

### 行程规划 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | `/api/v1/itineraries` | 获取行程列表 | ✅ |
| POST | `/api/v1/itineraries` | 创建行程 | ✅ |
| GET | `/api/v1/itineraries/{id}` | 获取行程详情 | ✅ |
| PATCH | `/api/v1/itineraries/{id}` | 更新行程 | ✅ |
| DELETE | `/api/v1/itineraries/{id}` | 删除行程 | ✅ |
| POST | `/api/v1/itineraries/{id}/generate` | AI 生成行程 | ✅ |

### QA 问答 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | `/api/v1/qa/chat` | 发送消息 | ✅ |
| GET | `/api/v1/qa/sessions` | 获取对话列表 | ✅ |
| POST | `/api/v1/qa/sessions` | 创建新对话 | ✅ |
| DELETE | `/api/v1/qa/sessions/{id}` | 删除对话 | ✅ |

### 文案生成 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | `/api/v1/copywriting/generate` | 生成文案 | ✅ |
| GET | `/api/v1/copywriting/results` | 获取生成历史 | ✅ |
| DELETE | `/api/v1/copywriting/results/{id}` | 删除结果 | ✅ |

## 测试指南

### 单元测试

使用 pytest 进行单元测试：

```python
import pytest
from app.core.db.session import get_db
from app.modules.users.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_user(db: AsyncSession):
    user_service = UserService(db)
    user = await user_service.create_user(
        email="test@example.com",
        name="Test User"
    )
    assert user.email == "test@example.com"
    assert user.name == "Test User"
```

### API 测试

使用 httpx 进行 API 测试：

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## 常见问题

### Q: 如何添加新的 API 路由？

A: 在对应模块的 `api/v1.py` 中添加路由：

```python
from fastapi import APIRouter, Depends
from app.core.security.deps import get_current_user
from app.modules.users.models.user import User

router = APIRouter()

@router.get("/example")
async def example_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": "Hello, World!"}
```

然后在 `main.py` 中注册路由：

```python
from app.modules.users.api.v1 import router as users_router
from app.modules.planner.api.v1 import router as planner_router

app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(planner_router, prefix="/api/v1/planner", tags=["planner"])
```

### Q: 如何创建数据库迁移？

A: 使用 Alembic 创建迁移：

```bash
# 创建迁移文件
alembic revision --autogenerate -m "Add user table"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### Q: 如何处理异常？

A: 使用自定义异常类：

```python
# 在 common/exceptions/base.py 中定义
class WanderFlowException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

# 在 API 中使用
from fastapi import HTTPException

@router.post("/example")
async def example():
    try:
        # 业务逻辑
        pass
    except SomeException as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## 性能优化建议

1. **数据库优化**
   - 使用索引优化查询性能
   - 使用连接池管理数据库连接
   - 使用异步 I/O 提高并发性能

2. **缓存策略**
   - 使用 Redis 缓存热点数据
   - 合理设置缓存过期时间
   - 实现缓存预热机制

3. **API 优化**
   - 实现分页查询
   - 使用字段选择减少数据传输
   - 实现 API 响应缓存

4. **资源管理**
   - 及时释放数据库会话
   - 合理配置连接池大小
   - 监控内存使用情况

## 安全最佳实践

1. **认证与授权**
   - 使用强密钥生成 JWT
   - 设置合理的 Token 过期时间
   - 实施基于角色的访问控制

2. **输入验证**
   - 使用 Pydantic 进行数据验证
   - 过滤和转义用户输入
   - 限制上传文件类型和大小

3. **日志与监控**
   - 记录关键操作日志
   - 监控异常和错误
   - 实施安全审计

---

更多详细信息请参考 [主 README](../README.md)
