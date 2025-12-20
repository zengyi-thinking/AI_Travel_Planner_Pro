# AI旅游助手 - 后端架构设计文档（优化版）

## 目录
1. [项目概述](#项目概述)
2. [核心理念](#核心理念)
3. [技术架构](#技术架构)
4. [目录结构](#目录结构)
5. [核心层设计](#核心层设计)
   - [Infrastructure层（基础设施层）](#infrastructure层基础设施层)
   - [Common层（公共组件层）](#common层公共组件层)
   - [Modules层（业务领域层）](#modules层业务领域层)
6. [AI架构设计](#ai架构设计)
7. [模块详细设计](#模块详细设计)
   - [用户管理模块](#用户管理模块)
   - [行程规划模块](#行程规划模块)
   - [问答助手模块](#问答助手模块)
   - [文案生成模块](#文案生成模块)
8. [接口规范](#接口规范)
9. [部署架构](#部署架构)
10. [监控与日志](#监控与日志)

---

## 项目概述

### 项目定位
AI旅游助手后端采用FastAPI框架开发，遵循**"Core 提供能力，Modules 定义业务"**的架构理念，支持行程规划、问答助手、文案生成三大核心功能。采用AI优先设计，实现了底层模型调用与上层业务逻辑的物理隔离。

### 设计原则
- **最小化原则**：接口设计遵循最小必要原则，避免过度设计
- **模块化**：业务模块独立，低耦合高内聚
- **异步优先**：全面采用异步编程，提升并发性能
- **AI解耦**：底层LLM调用与上层Agent/Prompt物理隔离
- **可扩展性**：支持水平扩展，微服务架构友好
- **类型安全**：使用Pydantic进行数据验证和序列化

### 技术栈
- **Web框架**: FastAPI 0.110+
- **异步 ORM**: SQLAlchemy 2.0 + aiomysql
- **数据验证**: Pydantic 2.5+
- **认证授权**: JWT + Passlib
- **缓存**: Redis 7.0 + aioredis
- **任务队列**: Celery + Redis
- **文档**: 自动生成OpenAPI/Swagger文档
- **测试**: pytest + httpx
- **AI框架**: LangChain / 自研轻量级AI SDK

---

## 核心理念

### 🎯 架构哲学：Core + Modules

```
┌─────────────────────────────────────────────┐
│              Modules (业务领域层)              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │  用户模块 │ │ 规划模块  │ │  QA模块   │    │
│  │  Users   │ │ Planner  │ │   Q&A    │    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘    │
│       │            │            │           │
│       └────┬───────┴────────────┘           │
│            │                                │
│  ┌─────────▼────────────────────────────┐   │
│  │        Common (公共组件层)             │   │
│  └─────────┬────────────────────────────┘   │
│            │                                │
│  ┌─────────▼────────────────────────────┐   │
│  │     Core (基础设施层)                 │   │
│  │  [通用能力 · 与业务无关]               │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### 关键优势

1. **职责清晰**
   - `Core`：提供基础设施能力（AI工厂、数据库、缓存等）
   - `Modules`：定义业务逻辑（用户管理、行程规划等）
   - `Common`：提供公共组件（DTO、异常、工具等）

2. **AI解耦**
   ```
   ┌──────────────────────────────┐
   │    Modules层 (业务逻辑)        │
   │  ┌────────────────────────┐   │
   │  │  Agent (业务智能体)      │   │
   │  │  Prompts (提示词)       │   │
   │  │  Tools (业务工具)       │   │
   │  └─────────┬──────────────┘   │
   └────────────┼──────────────────┘
                │
   ┌────────────▼──────────────────┐
   │      Core层 (AI基础设施)       │
   │  ┌────────────────────────┐   │
   │  │  LLM工厂 (OpenAI/...)   │   │
   │  │  Embedding接口          │   │
   │  │  Vector Store抽象       │   │
   │  └────────────────────────┘   │
   └──────────────────────────────┘
   ```

3. **快速微服务拆分**
   - 未来可将 `modules/planner` 直接拆分为独立微服务
   - 只需复制 `core` 目录，无需改动业务逻辑

---

## 技术架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Nginx (反向代理 + 负载均衡)                     │
└────────────────────┬──────────────────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────────────────┐
│                 FastAPI 应用层 (Gunicorn + Uvicorn)             │
│  ┌───────────────┬───────────────┬───────────────┬──────────┐  │
│  │   Users模块    │  Planner模块   │    Q&A模块    │ Copy模块 │  │
│  │   API/Router  │   API/Router  │   API/Router  │API/Router│  │
│  └───────┬───────┴───────┬───────┴───────┬──────┴──────┬───┘  │
│          │               │               │              │      │
│  ┌───────▼───────┐ ┌─────▼──────┐ ┌─────▼─────┐ ┌────▼─────┐│
│  │ Common Layer  │ │    RAG     │ │  Planner  │ │ Copy     ││
│  │  (公共组件)    │ │   Service  │ │  Agent    │ │ Agent    ││
│  └───────┬───────┘ └─────┬──────┘ └─────┬─────┘ └────┬─────┘│
│          │               │               │              │      │
│  ┌───────▼───────┐ ┌─────▼──────┐ ┌─────▼─────┐ ┌────▼─────┐│
│  │ Service Layer │ │  Service   │ │  Service  │ │ Service  ││
│  │   (业务逻辑)   │ │  Layer     │ │  Layer    │ │  Layer   ││
│  └───────┬───────┘ └─────┬──────┘ └─────┬─────┘ └────┬─────┘│
│          │               │               │              │      │
│  ┌───────▼───────┐ ┌─────▼──────┐ ┌─────▼─────┐ ┌────▼─────┐│
│  │ DAO Layer     │ │  DAO Layer │ │  DAO Layer│ │ DAO Layer││
│  │   (数据访问)   │ │   (数据访问) │ │  (数据访问) │ │ (数据访问)││
│  └───────┬───────┘ └─────┬──────┘ └─────┬─────┘ └────┬─────┘│
│          │               │               │              │      │
│  ┌───────▼───────┐ ┌─────▼──────┐ ┌─────▼─────┐ ┌────▼─────┐│
│  │ Model Layer   │ │  Model     │ │  Model    │ │ Model    ││
│  │   (数据模型)   │ │  Layer     │ │  Layer    │ │ Layer    ││
│  └───────────────┴─┴────────────┴─┴───────────┴─┴──────────┘│
│                                                                │
└────────────────────┬─────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌─────────────┐ ┌──────────┐ ┌─────────────┐
│   MySQL     │ │  Redis   │ │ 外部服务集成  │
│  (主数据库)  │ │  (缓存)   │ │  (AI/搜索等)  │
└─────────────┘ └──────────┘ └─────────────┘
```

---

## 目录结构

### 完整项目结构

```
backend/
├── app/
│   ├── main.py                          # FastAPI 应用入口
│   │
│   ├── core/                            # 【基础设施层】(Infrastructure)
│   │   ├── config/                      # 配置管理
│   │   │   └── settings.py              # Pydantic Settings (环境变量)
│   │   │
│   │   ├── db/                          # 数据库基础设施
│   │   │   ├── __init__.py
│   │   │   ├── session.py               # Session 工厂
│   │   │   ├── base.py                  # ORM Base 类
│   │   │   └── engine.py                # 引擎配置
│   │   │
│   │   ├── security/                    # 安全相关
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py                   # JWT 工具
│   │   │   ├── password.py              # 密码哈希
│   │   │   └── deps.py                  # 通用依赖注入 (get_current_user等)
│   │   │
│   │   ├── ai/                          # 【AI 基础设施层】(关键)
│   │   │   ├── __init__.py
│   │   │   ├── factory.py               # LLM 工厂 (OpenAI/Spark/GLM)
│   │   │   ├── interface.py             # LLM 抽象接口
│   │   │   ├── embedding.py             # 向量化通用接口
│   │   │   └── exceptions.py            # AI 相关异常
│   │   │
│   │   └── tools/                       # 【通用工具】(非业务绑定)
│   │       ├── __init__.py
│   │       ├── calculator.py            # 计算器
│   │       ├── web_search.py            # 通用联网搜索
│   │       └── date_utils.py            # 日期工具
│   │
│   ├── common/                          # 【公共组件层】(Common)
│   │   ├── __init__.py
│   │   │
│   │   ├── dtos/                        # 通用 DTO
│   │   │   ├── __init__.py
│   │   │   ├── base.py                  # 基础 DTO
│   │   │   ├── pagination.py            # 分页请求/响应
│   │   │   └── response.py              # 标准响应结构
│   │   │
│   │   ├── utils/                       # 通用工具函数
│   │   │   ├── __init__.py
│   │   │   ├── random_id.py             # 随机ID生成
│   │   │   ├── time_helper.py           # 时间处理
│   │   │   └── formatter.py             # 格式化工具
│   │   │
│   │   └── exceptions.py                # 自定义异常类
│   │       ├── __init__.py
│   │       ├── base.py                  # 基础异常
│   │       ├── auth.py                  # 认证异常
│   │       └── business.py              # 业务异常
│   │
│   └── modules/                         # 【业务领域层】(Domain)
│       ├── __init__.py
│       │
│       ├── users/                       # 用户模块 (标准 CRUD)
│       │   ├── __init__.py
│       │   ├── api/
│       │   │   ├── __init__.py
│       │   │   └── v1.py                # 路由定义
│       │   ├── schemas/
│       │   │   ├── __init__.py
│       │   │   ├── user.py              # Pydantic 模型
│       │   │   └── auth.py              # 认证相关
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   └── user_service.py      # 业务逻辑
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   └── user.py              # SQLAlchemy 模型
│       │   └── daos/
│       │       ├── __init__.py
│       │       └── user_dao.py          # 数据访问对象
│       │
│       ├── planner/                     # 【行程规划模块】(AI 重业务)
│       │   ├── __init__.py
│       │   ├── api/
│       │   │   ├── __init__.py
│       │   │   └── v1.py
│       │   ├── schemas/
│       │   │   ├── __init__.py
│       │   │   └── plan_schema.py       # 行程相关 DTO
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   ├── itinerary.py         # Itinerary 模型
│       │   │   └── activity.py          # Activity 模型
│       │   ├── daos/
│       │   │   ├── __init__.py
│       │   │   ├── itinerary_dao.py
│       │   │   └── activity_dao.py
│       │   ├── agents/                  # 【业务智能体层】
│       │   │   ├── __init__.py
│       │   │   └── planner_agent.py     # 行程规划智能体
│       │   ├── tools/                   # 【专属业务工具】
│       │   │   ├── __init__.py
│       │   │   ├── flight_tool.py       # 查航班工具
│       │   │   ├── hotel_tool.py        # 查酒店工具
│       │   │   └── weather_tool.py      # 查天气工具
│       │   ├── prompts/                 # 【专属 Prompt 管理】
│       │   │   ├── __init__.py
│       │   │   └── planning_prompts.py  # 行程规划提示词
│       │   └── services/
│       │       ├── __init__.py
│       │       └── plan_service.py      # 协调 Agent 和 DAO
│       │
│       ├── qa/                          # 【问答助手模块】(RAG 业务)
│       │   ├── __init__.py
│       │   ├── api/
│       │   │   ├── __init__.py
│       │   │   └── v1.py
│       │   ├── schemas/
│       │   │   ├── __init__.py
│       │   │   └── chat_schema.py
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   ├── conversation.py
│       │   │   └── message.py
│       │   ├── daos/
│       │   │   ├── __init__.py
│       │   │   ├── conversation_dao.py
│       │   │   └── message_dao.py
│       │   ├── rag/                     # 【RAG 专属逻辑】
│       │   │   ├── __init__.py
│       │   │   ├── retriever.py         # 检索逻辑
│       │   │   ├── vector_store.py      # 向量库操作
│       │   │   └── knowledge_base.py    # 知识库管理
│       │   ├── agents/
│       │   │   ├── __init__.py
│       │   │   └── qa_agent.py          # 问答智能体
│       │   ├── tools/
│       │   │   ├── __init__.py
│       │   │   └── search_tool.py       # 搜索工具
│       │   ├── prompts/
│       │   │   ├── __init__.py
│       │   │   └── qa_prompts.py        # 问答提示词
│       │   └── services/
│       │       ├── __init__.py
│       │       └── chat_service.py      # 协调 Agent 和 RAG
│       │
│       └── copywriter/                  # 【文案生成模块】
│           ├── __init__.py
│           ├── api/
│           │   ├── __init__.py
│           │   └── v1.py
│           ├── schemas/
│           │   ├── __init__.py
│           │   └── content_schema.py
│           ├── models/
│           │   ├── __init__.py
│           │   └── content.py
│           ├── daos/
│           │   ├── __init__.py
│           │   └── content_dao.py
│           ├── agents/
│           │   ├── __init__.py
│           │   └── copywriter_agent.py  # 文案智能体
│           ├── tools/
│           │   ├── __init__.py
│           │   └── image_tool.py        # 图片处理工具
│           ├── templates/               # 【模板库】
│           │   ├── __init__.py
│           │   ├── social.py            # 朋友圈文案模板
│           │   ├── blog.py              # 游记模板
│           │   └── advertisement.py     # 推广文案模板
│           ├── prompts/
│           │   ├── __init__.py
│           │   └── copywriting_prompts.py
│           └── services/
│               ├── __init__.py
│               └── content_service.py
│
├── alembic/                             # 数据库迁移
│   └── versions/
│
├── tests/                               # 测试目录
│   ├── unit/                            # 单元测试
│   ├── integration/                     # 集成测试
│   └── fixtures/                        # 测试夹具
│
├── scripts/                             # 脚本目录
│   ├── init_db.py                       # 初始化数据库
│   └── seed_data.py                     # 填充测试数据
│
├── requirements.txt                     # 依赖清单
├── .env.example                         # 环境变量示例
├── Dockerfile                           # Docker 构建文件
├── docker-compose.yml                   # Docker Compose
└── README.md                            # 项目说明
```

---

## 核心层设计

### Infrastructure层（基础设施层）

#### 1. AI 基础设施 (`core/ai/`)

**核心目标**：提供通用的AI能力，与具体业务无关。

**关键文件说明**：

**`core/ai/factory.py`** - LLM 工厂
```python
from app.core.config.settings import settings
from langchain.chat_models import ChatOpenAI

class LLMFactory:
    """LLM 工厂 - 负责创建不同类型的 LLM 客户端"""

    @staticmethod
    def create_client(model_type: str = "openai", temperature: float = 0.7):
        """
        工厂模式：根据配置返回底层的 LLM 客户端
        注意：这里是纯技术实现，不含业务逻辑
        """
        if model_type == "openai":
            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL_NAME,
                temperature=temperature
            )
        elif model_type == "spark":
            # 返回星火大模型客户端...
            pass
        elif model_type == "glm":
            # 返回智谱 GLM 客户端...
            pass
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
```

**`core/ai/interface.py`** - LLM 抽象接口
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLMClient(ABC):
    """LLM 抽象基类 - 定义统一的接口"""

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """聊天接口"""
        pass

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """向量化接口"""
        pass
```

**`core/ai/embedding.py`** - 向量化通用接口
```python
from app.core.ai.factory import LLMFactory

class EmbeddingService:
    """向量化服务 - 通用能力"""

    def __init__(self):
        self.client = LLMFactory.create_client(temperature=0)

    async def embed_text(self, text: str) -> List[float]:
        """将文本转换为向量"""
        return await self.client.embed(text)

    async def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """批量向量化"""
        return [await self.embed_text(doc) for doc in documents]
```

#### 2. 数据库基础设施 (`core/db/`)

**`core/db/base.py`** - ORM Base
```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

**`core/db/session.py`** - Session 工厂
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """依赖注入：获取数据库会话"""
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

#### 3. 安全基础设施 (`core/security/`)

**`core/security/deps.py`** - 通用依赖注入
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.core.db.session import AsyncSession
from app.core.security.jwt import verify_token

security = HTTPBearer()

async def get_current_user(
    token: str = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """通用依赖：获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    payload = verify_token(token.credentials)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # 这里可以查询数据库获取用户信息
    return user_id
```

### Common层（公共组件层）

#### 1. 通用 DTO (`common/dtos/`)

**`common/dtos/response.py`** - 标准响应结构
```python
from pydantic import BaseModel
from typing import Optional, Any

class ResponseDTO(BaseModel):
    """标准响应 DTO"""
    code: int = 200
    message: str = "Success"
    data: Optional[Any] = None

class ErrorResponseDTO(BaseModel):
    """错误响应 DTO"""
    code: int = 400
    message: str
    error: Optional[str] = None
```

**`common/dtos/pagination.py`** - 分页
```python
from pydantic import BaseModel
from typing import List, Generic, TypeVar

T = TypeVar('T')

class PaginationRequest(BaseModel):
    """分页请求"""
    page: int = 1
    size: int = 20

class PaginationResponse(BaseModel, Generic[T]):
    """分页响应"""
    page: int
    size: int
    total: int
    items: List[T]
```

#### 2. 通用异常 (`common/exceptions/`)

**`common/exceptions/base.py`** - 基础异常
```python
class BusinessException(Exception):
    """业务异常基类"""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundException(BusinessException):
    """未找到异常"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)
```

### Modules层（业务领域层）

#### 架构特点

1. **垂直拆分**：每个模块包含完整的 API → Service → DAO → Model 链路
2. **AI隔离**：Agent、Tools、Prompts 独立于 Core
3. **低耦合**：模块之间无直接依赖，通过事件或消息队列通信

---

## AI架构设计

### 核心理念：物理隔离

```
┌─────────────────────────────────────────────────────┐
│                Modules 层 (业务逻辑)                  │
│  ┌─────────────────────────────────────────────┐   │
│  │                Planner 模块                  │   │
│  │  ┌─────────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │   Agent     │ │  Tools   │ │ Prompts  │  │   │
│  │  │  (业务智能)   │ │ (业务工具) │ │ (提示词)  │  │   │
│  │  └──────┬──────┘ └─────┬────┘ └────┬────┘  │   │
│  └─────────┼──────────────┼────────────┼───────┘   │
│            │              │            │           │
│            └──────┬───────┴────────────┘           │
│                     │                            │
│  ┌──────────────────▼────────────────────────────┐ │
│  │           Core.ai (基础设施)                    │ │
│  │  ┌────────────┐ ┌──────────┐ ┌─────────────┐  │ │
│  │  │   LLM      │ │Embedding │ │Vector Store │  │ │
│  │  │   Factory  │ │ Interface│ │  Abstract   │  │ │
│  │  └────────────┘ └──────────┘ └─────────────┘  │ │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 具体实现

#### Module 层的 Agent (`modules/planner/agents/planner_agent.py`)

```python
# app/modules/planner/agents/planner_agent.py
from app.core.ai.factory import LLMFactory
from app.modules.planner.prompts import planning_prompts
from app.modules.planner.tools import flight_tool, hotel_tool

class TravelPlannerAgent:
    """行程规划智能体 - 纯业务逻辑，不涉及底层实现"""

    def __init__(self):
        # 1. 从 Core 获取通用计算能力
        self.llm = LLMFactory.create_client(temperature=0.2)

        # 2. 绑定本模块专属的 Tools
        self.tools = [flight_tool, hotel_tool]

    async def generate_plan(self, destination: str, days: int) -> dict:
        """
        生成行程计划
        注意：这里只关注业务逻辑，底层LLM调用由Core提供
        """
        # 3. 使用本模块专属的 Prompt
        prompt = planning_prompts.create_planning_prompt(destination, days)

        # 4. 调用 Core 的 LLM（底层细节被隐藏）
        response = await self.llm.chat(prompt)

        # 5. 处理业务逻辑
        return self._parse_response(response)

    def _parse_response(self, response: str) -> dict:
        """解析响应 - 业务逻辑处理"""
        # 这里可以调用 DAO 保存到数据库
        pass
```

#### Module 层的 Tools (`modules/planner/tools/flight_tool.py`)

```python
# app/modules/planner/tools/flight_tool.py
from typing import Dict, Any

class FlightTool:
    """航班查询工具 - 业务专属"""

    async def search_flights(
        self,
        departure: str,
        destination: str,
        date: str
    ) -> Dict[str, Any]:
        """
        搜索航班 - 业务工具的具体实现
        这里可以调用真实的航班 API
        """
        # 业务逻辑：调用第三方 API
        # 例如：携程、去哪儿、飞猪等
        return {
            "flights": [
                {
                    "flight_no": "CA1234",
                    "departure_time": "08:00",
                    "arrival_time": "10:30",
                    "price": 1200
                }
            ]
        }
```

#### Module 层的 Prompts (`modules/planner/prompts/planning_prompts.py`)

```python
# app/modules/planner/prompts/planning_prompts.py

PLANNING_SYSTEM_PROMPT = """
你是一个专业的旅行规划师。请根据用户的需求，制定详细的旅行计划。
"""

PLANNING_USER_PROMPT = """
目的地：{destination}
天数：{days}
预算：{budget}
兴趣：{interests}
"""

def create_planning_prompt(
    destination: str,
    days: int,
    budget: str = "中等",
    interests: str = "文化、美食"
) -> list:
    """创建规划提示词"""
    messages = [
        {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": PLANNING_USER_PROMPT.format(
                destination=destination,
                days=days,
                budget=budget,
                interests=interests
            )
        }
    ]
    return messages
```

### 优势总结

1. **职责分离**
   - Core.ai：只负责底层技术实现（OpenAI API调用、向量化等）
   - Modules：只负责业务逻辑（Agent、Tools、Prompts）
   - 两者之间通过简单接口通信，无耦合

2. **易于维护**
   - 更换底层LLM供应商（如从OpenAI切换到Spark）：只需修改 `core/ai/factory.py`
   - 业务逻辑调整：只需修改对应模块的 Agent/Tools/Prompts
   - 互不影响

3. **快速微服务拆分**
   - 未来可将 `modules/planner` 直接拆分为独立微服务
   - 只需复制一份 `core`，业务模块即可独立运行

4. **测试友好**
   - Core.ai：可轻松 Mock LLM 工厂进行测试
   - Modules：可独立测试业务逻辑，无需真实 AI 调用

---

## 模块详细设计

### 用户管理模块 (`modules/users/`)

#### 职责
标准的用户 CRUD 操作，包括注册、登录、信息管理。

#### API 路由 (`modules/users/api/v1.py`)

```python
# app/modules/users/api/v1.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_user
from app.modules.users.schemas.user import UserCreate, UserResponse, UserUpdate
from app.modules.users.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建用户"""
    service = UserService(db)
    return await service.create_user(user_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户信息"""
    service = UserService(db)
    return await service.get_user(current_user_id)

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    service = UserService(db)
    return await service.update_user(current_user_id, user_data)
```

#### 数据模型 (`modules/users/models/user.py`)

```python
# app/modules/users/models/user.py
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.db.base import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    avatar_url = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
```

#### 业务服务 (`modules/users/services/user_service.py`)

```python
# app/modules/users/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models.user import User
from app.modules.users.daos.user_dao import UserDAO
from app.modules.users.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security.password import get_password_hash, verify_password
from app.common.exceptions.business import BusinessException

class UserService:
    """用户业务服务"""

    def __init__(self, db: AsyncSession):
        self.user_dao = UserDAO(db)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """创建用户"""
        # 检查邮箱是否已存在
        existing = await self.user_dao.get_by_email(user_data.email)
        if existing:
            raise BusinessException("邮箱已被注册")

        # 创建用户
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name
        )
        created = await self.user_dao.create(user)
        return UserResponse.from_orm(created)

    async def authenticate(self, email: str, password: str) -> User:
        """用户认证"""
        user = await self.user_dao.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise BusinessException("邮箱或密码错误")

        return user
```

### 行程规划模块 (`modules/planner/`)

#### 职责
使用AI生成智能行程规划，调用航班、酒店等业务工具。

#### API 路由 (`modules/planner/api/v1.py`)

```python
# app/modules/planner/api/v1.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_user
from app.modules.planner.schemas.plan_schema import (
    PlanRequest, PlanResponse, PlanListResponse
)
from app.modules.planner.services.plan_service import PlanService

router = APIRouter(prefix="/planner", tags=["planner"])

@router.post("/generate", response_model=PlanResponse)
async def generate_plan(
    request: PlanRequest,
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """生成行程规划"""
    service = PlanService(db)
    return await service.generate_plan(current_user_id, request)

@router.get("/my-plans", response_model=PlanListResponse)
async def get_my_plans(
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取我的行程"""
    service = PlanService(db)
    return await service.get_user_plans(current_user_id)
```

#### 数据模型 (`modules/planner/models/itinerary.py`)

```python
# app/modules/planner/models/itinerary.py
from sqlalchemy import Column, String, Text, Integer, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.db.base import Base

class Itinerary(Base):
    """行程模型"""
    __tablename__ = "itineraries"

    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.id"), index=True)
    title = Column(String(200), nullable=False)
    destination = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(Integer, nullable=False)
    budget = Column(Integer)
    travelers = Column(Integer, default=1)
    preferences = Column(JSON)  # 存储偏好设置
    plan_details = Column(JSON)  # 存储AI生成的详细行程
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activities = relationship("Activity", back_populates="itinerary")

class Activity(Base):
    """活动模型"""
    __tablename__ = "activities"

    id = Column(String(50), primary_key=True)
    itinerary_id = Column(String(50), ForeignKey("itineraries.id"))
    day = Column(Integer, nullable=False)
    time = Column(String(20))  # 例如：09:00
    title = Column(String(200), nullable=False)
    description = Column(Text)
    location = Column(String(200))
    duration = Column(Integer)  # 分钟
    estimated_cost = Column(Integer)
    notes = Column(Text)

    itinerary = relationship("Itinerary", back_populates="activities")
```

#### 业务智能体 (`modules/planner/agents/planner_agent.py`)

```python
# app/modules/planner/agents/planner_agent.py
from app.core.ai.factory import LLMFactory
from app.modules.planner.prompts import planning_prompts
from app.modules.planner.tools import flight_tool, hotel_tool, weather_tool

class TravelPlannerAgent:
    """行程规划智能体"""

    def __init__(self):
        self.llm = LLMFactory.create_client(temperature=0.3)
        self.tools = [flight_tool, hotel_tool, weather_tool]

    async def generate_itinerary(
        self,
        destination: str,
        start_date: str,
        end_date: str,
        budget: int,
        travelers: int,
        preferences: dict
    ) -> dict:
        """
        生成行程规划
        """
        # 1. 构建 Prompt
        prompt = planning_prompts.create_comprehensive_prompt(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            travelers=travelers,
            preferences=preferences
        )

        # 2. 调用 LLM
        response = await self.llm.chat(prompt)

        # 3. 解析响应
        return self._parse_itinerary(response)

    def _parse_itinerary(self, response: str) -> dict:
        """解析AI响应为结构化数据"""
        # 这里可以调用专门的解析器或使用LLM再次调用
        # 简化处理
        return {
            "days": [],
            "total_cost": 0,
            "recommendations": []
        }
```

#### 业务工具 (`modules/planner/tools/`)

**`modules/planner/tools/flight_tool.py`**

```python
# app/modules/planner/tools/flight_tool.py
from typing import Dict, List, Any

class FlightTool:
    """航班查询工具"""

    async def search_flights(
        self,
        departure: str,
        destination: str,
        date: str,
        passengers: int = 1
    ) -> List[Dict[str, Any]]:
        """搜索航班"""
        # 调用真实 API 或模拟数据
        return [
            {
                "flight_no": "CA1234",
                "airline": "中国国航",
                "departure": {
                    "airport": departure,
                    "time": "08:00"
                },
                "arrival": {
                    "airport": destination,
                    "time": "10:30"
                },
                "price": 1200,
                "duration": 150  # 分钟
            }
        ]

    async def compare_prices(
        self,
        departure: str,
        destination: str,
        date: str
    ) -> Dict[str, Any]:
        """比价查询"""
        # 聚合多个航班API的数据
        pass
```

**`modules/planner/tools/hotel_tool.py`**

```python
# app/modules/planner/tools/hotel_tool.py
from typing import Dict, List

class HotelTool:
    """酒店查询工具"""

    async def search_hotels(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int,
        budget: int
    ) -> List[Dict[str, Any]]:
        """搜索酒店"""
        return [
            {
                "name": "希尔顿酒店",
                "location": destination,
                "rating": 4.5,
                "price_per_night": 600,
                "amenities": ["WiFi", "健身房", "游泳池"],
                "availability": True
            }
        ]
```

#### 专属 Prompt (`modules/planner/prompts/planning_prompts.py`)

```python
# app/modules/planner/prompts/planning_prompts.py

SYSTEM_PROMPT = """
你是一个专业的旅行规划师，擅长根据用户需求制定详细、实用的旅行计划。
你需要考虑：
1. 目的地的主要景点和特色
2. 合理的行程安排（避免过于紧密）
3. 当地美食推荐
4. 交通方式
5. 预算控制
请以 JSON 格式返回结果。
"""

def create_basic_prompt(destination: str, days: int) -> List[Dict[str, str]]:
    """创建基础规划 Prompt"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"请为 {destination} 制定一个 {days} 天的旅行计划"
        }
    ]

def create_comprehensive_prompt(
    destination: str,
    start_date: str,
    end_date: str,
    budget: int,
    travelers: int,
    preferences: dict
) -> List[Dict[str, str]]:
    """创建综合规划 Prompt"""
    content = f"""
目的地：{destination}
出行日期：{start_date} 至 {end_date}
预算：{budget} 元
人数：{travelers} 人
偏好：{preferences}

请制定详细的旅行计划，包括：
1. 每日行程安排
2. 推荐景点
3. 住宿建议
4. 餐饮推荐
5. 交通方式
6. 预计费用

请以 JSON 格式返回。
"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content}
    ]
```

#### 业务服务 (`modules/planner/services/plan_service.py`)

```python
# app/modules/planner/services/plan_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.planner.models.itinerary import Itinerary
from app.modules.planner.daos.itinerary_dao import ItineraryDAO
from app.modules.planner.agents.planner_agent import TravelPlannerAgent
from app.modules.planner.schemas.plan_schema import PlanRequest, PlanResponse

class PlanService:
    """行程规划服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.itinerary_dao = ItineraryDAO(db)
        self.agent = TravelPlannerAgent()

    async def generate_plan(
        self,
        user_id: str,
        request: PlanRequest
    ) -> PlanResponse:
        """生成行程规划"""
        # 1. 调用 AI Agent 生成行程
        ai_plan = await self.agent.generate_itinerary(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            budget=request.budget,
            travelers=request.travelers,
            preferences=request.preferences
        )

        # 2. 保存到数据库
        itinerary = Itinerary(
            id=generate_id(),
            user_id=user_id,
            title=f"{request.destination} {request.days}日游",
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            days=request.days,
            budget=request.budget,
            travelers=request.travelers,
            preferences=request.preferences,
            plan_details=ai_plan
        )
        created = await self.itinerary_dao.create(itinerary)

        return PlanResponse.from_orm(created)

    async def get_user_plans(self, user_id: str) -> PlanListResponse:
        """获取用户的所有行程"""
        itineraries = await self.itinerary_dao.get_by_user(user_id)
        return PlanListResponse(items=itineraries)
```

### 问答助手模块 (`modules/qa/`)

#### 职责
基于RAG的AI问答系统，检索旅游知识库并生成回答。

#### 架构特点
- **RAG分离**：检索逻辑与业务逻辑分离
- **向量化抽象**：基于 Core.ai.embedding 接口
- **知识库管理**：独立的知识库模块

#### API 路由 (`modules/qa/api/v1.py`)

```python
# app/modules/qa/api/v1.py
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.core.security.deps import get_current_user
from app.modules.qa.schemas.chat_schema import ChatRequest, ChatResponse
from app.modules.qa.services.chat_service import ChatService

router = APIRouter(prefix="/qa", tags=["qa"])

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    """单轮问答"""
    service = ChatService()
    return await service.chat(current_user_id, request)

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, user_id: str = Depends(get_current_user)):
    """WebSocket 实时对话"""
    service = ChatService()
    await service.websocket_chat(websocket, user_id)
```

#### RAG 服务 (`modules/qa/rag/retriever.py`)

```python
# app/modules/qa/rag/retriever.py
from typing import List, Dict, Any
from app.core.ai.embedding import EmbeddingService

class RAGRetriever:
    """RAG 检索器 - 业务专属"""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        # 这里可以注入向量数据库实例 (如 Pinecone, Weaviate, Chroma)

    async def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """检索相关文档"""
        # 1. 查询向量化
        query_vector = await self.embedding_service.embed_text(query)

        # 2. 向量相似度搜索
        # 实际项目中会调用向量数据库
        results = await self._vector_search(query_vector, top_k)

        # 3. 格式化结果
        return [
            {
                "content": doc["text"],
                "metadata": doc.get("metadata", {}),
                "score": doc.get("score", 0)
            }
            for doc in results
        ]

    async def _vector_search(
        self,
        query_vector: List[float],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """向量搜索实现"""
        # 这里调用实际的向量数据库
        # 例如：Pinecone, Weaviate, ChromaDB
        pass
```

#### 问答智能体 (`modules/qa/agents/qa_agent.py`)

```python
# app/modules/qa/agents/qa_agent.py
from app.core.ai.factory import LLMFactory
from app.modules.qa.rag.retriever import RAGRetriever
from app.modules.qa.prompts import qa_prompts

class QAAgent:
    """问答智能体"""

    def __init__(self):
        self.llm = LLMFactory.create_client(temperature=0.7)
        self.retriever = RAGRetriever()
        self.max_context_length = 5  # 最多使用5个检索结果

    async def chat(self, query: str) -> str:
        """对话"""
        # 1. 检索相关文档
        relevant_docs = await self.retriever.retrieve(query, top_k=self.max_context_length)

        # 2. 构建上下文
        context = "\n\n".join([doc["content"] for doc in relevant_docs])

        # 3. 构建 Prompt
        messages = qa_prompts.create_rag_prompt(query, context)

        # 4. 调用 LLM
        response = await self.llm.chat(messages)

        return response
```

#### RAG Prompt (`modules/qa/prompts/qa_prompts.py`)

```python
# app/modules/qa/prompts/qa_prompts.py

SYSTEM_PROMPT = """
你是一个专业的旅游助手。请根据提供的旅游知识库回答用户的问题。
如果知识库中没有相关信息，请说明你不知道，并建议用户咨询人工客服。
"""

def create_rag_prompt(query: str, context: str) -> List[Dict[str, str]]:
    """创建 RAG Prompt"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
问题：{query}

相关知识库内容：
{context}

请基于以上内容回答问题。
"""
        }
    ]
```

### 文案生成模块 (`modules/copywriter/`)

#### 职责
使用AI生成各类旅游文案（朋友圈、游记、推广等）。

#### 模板系统 (`modules/copywriter/templates/`)

```python
# app/modules/copywriter/templates/social.py
SOCIAL_MEDIA_TEMPLATES = {
    "vacation": {
        "name": "度假朋友圈",
        "template": """
🌴 {destination} · {duration}天{duration}夜
✨ 一些美好，正在路上...

{highlights}

📍 {location}
📸 记录每一个瞬间
#旅行 #{destination} #美好时光
""",
        "variables": ["destination", "duration", "highlights", "location"]
    },
    "food": {
        "name": "美食分享",
        "template": """
🍜 {restaurant_name}
📍 {location}

{review}

⭐️ 评分：{rating}/5
#美食 #探店 #{city}
""",
        "variables": ["restaurant_name", "location", "review", "rating", "city"]
    }
}

class TemplateFactory:
    """模板工厂"""

    @staticmethod
    def get_template(template_key: str) -> Dict[str, str]:
        """获取模板"""
        return SOCIAL_MEDIA_TEMPLATES.get(template_key)

    @staticmethod
    def render_template(template_key: str, variables: Dict[str, str]) -> str:
        """渲染模板"""
        template = TemplateFactory.get_template(template_key)
        if not template:
            raise ValueError(f"Template not found: {template_key}")

        content = template["template"]
        return content.format(**variables)
```

#### 文案智能体 (`modules/copywriter/agents/copywriter_agent.py`)

```python
# app/modules/copywriter/agents/copywriter_agent.py
from app.core.ai.factory import LLMFactory
from app.modules.copywriter.templates.template_factory import TemplateFactory
from app.modules.copywriter.prompts import copywriting_prompts

class CopywriterAgent:
    """文案生成智能体"""

    def __init__(self):
        self.llm = LLMFactory.create_client(temperature=0.8)

    async def generate_content(
        self,
        content_type: str,
        destination: str,
        style: str = "casual",
        custom_variables: Dict[str, str] = None
    ) -> str:
        """生成文案"""
        # 1. 获取模板
        template = TemplateFactory.get_template(content_type)
        if not template:
            # 如果没有模板，使用 AI 直接生成
            prompt = copywriting_prompts.create_generate_prompt(
                content_type, destination, style
            )
            response = await self.llm.chat(prompt)
            return response

        # 2. 渲染模板（如果有变量，调用 AI 填充）
        if template["variables"]:
            variables = await self._generate_variables(
                template["variables"], destination, style, custom_variables
            )
        else:
            variables = {}

        # 3. 渲染模板
        content = TemplateFactory.render_template(content_type, variables)

        return content

    async def _generate_variables(
        self,
        variables: List[str],
        destination: str,
        style: str,
        custom_vars: Dict[str, str]
    ) -> Dict[str, str]:
        """生成模板变量"""
        # 这里可以调用 AI 来生成每个变量
        # 简化处理
        return {var: f"Generated {var}" for var in variables}
```

---


# WanderFlow - API接口规范（精简版）

## 概述

基于前端实际需求和精简数据库设计，采用最小化接口原则，提供RESTful API。

### 基础信息
- **Base URL**: `http://api.wanderflow.com/api/v1`
- **认证方式**: Bearer Token (JWT)
- **Content-Type**: `application/json`
- **字符编码**: UTF-8

---

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "code": 200,
  "message": "Success",
  "data": {
    // 具体数据
  }
}
```

### 错误响应
```json
{
  "success": false,
  "code": 400,
  "message": "Bad Request",
  "error": "详细错误信息"
}
```

### 分页响应
```json
{
  "success": true,
  "code": 200,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

---

## 接口列表

## 1. 认证模块 (Auth)

### 1.1 用户登录
```
POST /auth/login
```

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "remember": false
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "张三",
      "avatar_url": "https://..."
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 86400
  }
}
```

### 1.2 用户注册
```
POST /auth/register
```

**请求体**:
```json
{
  "email": "user@example.com",
  "phone": "13800138000",
  "password": "password123",
  "name": "张三",
  "agreed_to_terms": true
}
```

### 1.3 用户登出
```
POST /auth/logout
```
**Headers**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### 1.4 获取当前用户
```
GET /auth/me
```
**Headers**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "张三",
    "phone": "13800138000",
    "avatar_url": "https://...",
    "status": "active",
    "email_verified": true,
    "last_login_at": "2024-01-01T12:00:00Z"
  }
}
```

### 1.5 更新用户信息
```
PUT /auth/me
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "name": "李四",
  "phone": "13900139000",
  "avatar_url": "https://..."
}
```

---

## 2. 用户设置模块 (Settings)

### 2.1 获取用户设置
```
GET /users/settings
```
**Headers**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "success": true,
  "data": {
    "language": "zh-CN",
    "theme": "light",
    "timezone": "Asia/Shanghai",
    "currency": "CNY",
    "preferences": {
      "budget_range": [1000, 10000],
      "accommodation_type": "comfort",
      "interests": ["美食", "文化"]
    }
  }
}
```

### 2.2 更新用户设置
```
PUT /users/settings
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "language": "zh-CN",
  "theme": "dark",
  "currency": "USD",
  "preferences": {
    "budget_range": [500, 5000],
    "accommodation_type": "budget"
  }
}
```

### 2.3 获取订阅信息
```
GET /users/subscription
```
**Headers**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "success": true,
  "data": {
    "plan_type": "pro",
    "status": "active",
    "start_date": "2024-01-01",
    "end_date": "2025-01-01",
    "auto_renew": true
  }
}
```

---

## 3. 行程规划模块 (Planner)

### 3.1 生成行程
```
POST /planner/generate
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "destination": "北京",
  "departure": "上海",
  "days": 3,
  "budget": 5000,
  "travel_style": "leisure"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "itinerary": {
      "id": 1001,
      "title": "北京3日游",
      "destination": "北京",
      "days": 3,
      "budget": 5000,
      "travel_style": "leisure",
      "status": "draft",
      "ai_generated": true,
      "days_detail": [
        {
          "day_number": 1,
          "date": "2024-06-01",
          "title": "初到北京",
          "activities": [
            {
              "time": "09:00",
              "activity": "天安门广场",
              "location": "东城区",
              "type": "sightseeing",
              "duration": 120,
              "notes": "提前预约"
            }
          ]
        }
      ]
    }
  }
}
```

### 3.2 获取我的行程列表
```
GET /planner/itineraries
```
**Headers**: `Authorization: Bearer <token>`

**查询参数**:
- `page`: 页码 (默认1)
- `size`: 每页数量 (默认10)
- `status`: 行程状态 (draft/active/completed/archived)

**响应**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1001,
        "title": "北京3日游",
        "destination": "北京",
        "days": 3,
        "budget": 5000,
        "travel_style": "leisure",
        "status": "active",
        "created_at": "2024-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 5,
      "pages": 1
    }
  }
}
```

### 3.3 获取行程详情
```
GET /planner/itineraries/{id}
```
**Headers**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1001,
    "title": "北京3日游",
    "destination": "北京",
    "departure": "上海",
    "days": 3,
    "budget": 5000,
    "travel_style": "leisure",
    "status": "active",
    "metadata": {
      "travelers": 2,
      "special_requests": "无"
    },
    "days_detail": [...],
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

### 3.4 更新行程
```
PUT /planner/itineraries/{id}
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "title": "北京3日游（修改版）",
  "budget": 6000,
  "days_detail": [...]
}
```

### 3.5 删除行程
```
DELETE /planner/itineraries/{id}
```
**Headers**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "success": true,
  "message": "Itinerary deleted successfully"
}
```

---

## 4. AI助手模块 (QA)

### 4.1 创建聊天会话
```
POST /qa/sessions
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "title": "北京旅游咨询",
  "features": {
    "knowledge_base": true,
    "weather": false,
    "voice": true
  }
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "session": {
      "id": 2001,
      "title": "北京旅游咨询",
      "features": {
        "knowledge_base": true,
        "weather": false,
        "voice": true
      },
      "created_at": "2024-01-01T12:00:00Z"
    }
  }
}
```

### 4.2 发送消息
```
POST /qa/messages
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "session_id": 2001,
  "content": "北京三日游有什么推荐？",
  "message_type": "text"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "message": {
      "id": 3001,
      "session_id": 2001,
      "role": "assistant",
      "content": "北京三日游推荐...",
      "message_type": "text",
      "created_at": "2024-01-01T12:00:00Z"
    }
  }
}
```

### 4.3 获取聊天历史
```
GET /qa/sessions/{session_id}/messages
```
**Headers**: `Authorization: Bearer <token>`

**查询参数**:
- `page`: 页码
- `size`: 每页数量

**响应**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 3001,
        "role": "user",
        "content": "北京三日游有什么推荐？",
        "message_type": "text",
        "created_at": "2024-01-01T12:00:00Z"
      },
      {
        "id": 3002,
        "role": "assistant",
        "content": "北京三日游推荐...",
        "message_type": "text",
        "created_at": "2024-01-01T12:00:01Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 50,
      "total": 10,
      "pages": 1
    }
  }
}
```

### 4.4 查询天气
```
GET /qa/weather/{city}
```
**Headers**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "success": true,
  "data": {
    "city": "北京",
    "forecast": [
      {
        "date": "2024-06-01",
        "weather": "晴",
        "temp_high": 28,
        "temp_low": 18,
        "humidity": 60,
        "wind": "南风3级",
        "uv_index": 7
      }
    ]
  }
}
```

### 4.5 语音转文字
```
POST /qa/speech-to-text
```
**Headers**: `Authorization: Bearer <token>`

**请求体**: `multipart/form-data`
- `audio`: 音频文件
- `session_id`: 会话ID

**响应**:
```json
{
  "success": true,
  "data": {
    "text": "帮我查询一下北京的天气",
    "session_id": 2001
  }
}
```

### 4.6 文字转语音
```
POST /qa/text-to-speech
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "text": "北京今天天气晴朗，温度28度",
  "voice": "default"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "audio_url": "https://cdn.wanderflow.com/audio/12345.mp3",
    "duration": 3.5
  }
}
```

---

## 5. 文案生成模块 (Copywriter)

### 5.1 生成文案
```
POST /copywriter/generate
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "platform": "xiaohongshu",
  "image_url": "https://example.com/image.jpg",
  "keywords": ["日落", "治愈", "大海"],
  "emotion": 0.7
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "content": {
      "id": 4001,
      "platform": "xiaohongshu",
      "output_content": "今天来看日落啦！✨ 蔚蓝的大海配上橙红色的晚霞，这就是最治愈的画面...",
      "input_data": {
        "platform": "xiaohongshu",
        "keywords": ["日落", "治愈", "大海"],
        "emotion": 0.7
      },
      "created_at": "2024-01-01T12:00:00Z"
    }
  }
}
```

### 5.2 上传图片
```
POST /copywriter/upload-image
```
**Headers**: `Authorization: Bearer <token>`

**请求体**: `multipart/form-data`
- `image`: 图片文件

**响应**:
```json
{
  "success": true,
  "data": {
    "image_url": "https://cdn.wanderflow.com/images/12345.jpg",
    "image_id": 12345
  }
}
```

### 5.3 获取我的文案列表
```
GET /copywriter/contents
```
**Headers**: `Authorization: Bearer <token>`

**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `platform`: 平台筛选

**响应**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 4001,
        "content_type": "copywriting",
        "platform": "xiaohongshu",
        "output_content": "今天来看日落啦！✨...",
        "rating": 5,
        "created_at": "2024-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 10,
      "pages": 1
    }
  }
}
```

### 5.4 评价文案
```
POST /copywriter/contents/{id}/rate
```
**Headers**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "rating": 5,
  "feedback": "生成效果很好，符合平台风格"
}
```

---

## 6. 知识库模块 (Knowledge)

### 6.1 搜索知识库
```
GET /knowledge/search
```
**Headers**: `Authorization: Bearer <token>`

**查询参数**:
- `q`: 搜索关键词
- `tags`: 标签筛选 (JSON数组)
- `page`: 页码
- `size`: 每页数量

**响应**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 5001,
        "title": "北京旅游攻略",
        "content": "北京是中国的首都...",
        "tags": ["北京", "攻略", "文化"],
        "created_at": "2024-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 5,
      "pages": 1
    }
  }
}
```

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/Token无效 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

---

## 请求示例

### 完整流程示例

#### 1. 登录
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### 2. 生成行程
```bash
curl -X POST "http://localhost:8000/api/v1/planner/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "北京",
    "days": 3,
    "budget": 5000,
    "travel_style": "leisure"
  }'
```

#### 3. AI对话
```bash
curl -X POST "http://localhost:8000/api/v1/qa/messages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 2001,
    "content": "北京有什么好吃的？",
    "message_type": "text"
  }'
```

#### 4. 生成文案
```bash
curl -X POST "http://localhost:8000/api/v1/copywriter/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "xiaohongshu",
    "keywords": ["日落", "治愈"],
    "emotion": 0.8
  }'
```

---

## 总结

### 接口设计特点

1. **最小化原则**: 仅提供必要接口，避免冗余
2. **RESTful设计**: 遵循REST规范，语义清晰
3. **统一响应格式**: 所有接口使用相同响应结构
4. **JWT认证**: 使用Bearer Token进行认证
5. **分页支持**: 列表接口支持分页查询
6. **错误处理**: 统一的错误码和错误信息
7. **扩展性**: JSON字段支持未来扩展

### 接口统计

- **认证模块**: 5个接口
- **用户设置**: 3个接口
- **行程规划**: 5个接口
- **AI助手**: 6个接口
- **文案生成**: 4个接口
- **知识库**: 1个接口

**总计**: 24个核心接口，满足所有前端功能需求


## 部署架构

### Docker 部署

#### Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./app.db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./:/app

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery-worker:
    build: .
    command: celery -A app.core.celery worker --loglevel=info
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./app.db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./:/app
```

### Kubernetes 部署

#### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: travel-ai-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: travel-ai-backend
  template:
    metadata:
      labels:
        app: travel-ai-backend
    spec:
      containers:
      - name: api
        image: travel-ai-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

#### Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: travel-ai-ingress
spec:
  rules:
  - host: api.travel-ai.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: travel-ai-backend
            port:
              number: 8000
```

---

## 监控与日志

### 日志配置

#### 结构化日志
```python
# app/core/logging.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
)
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### 性能监控

#### Prometheus 指标
```python
# app/core/monitoring.py
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency'
)

ACTIVE_USERS = Gauge(
    'active_users_total',
    'Number of active users'
)
```

#### 使用示例
```python
# app/main.py
from app.core.monitoring import REQUEST_COUNT, REQUEST_LATENCY
from fastapi import Request
import time

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.observe(process_time)

    return response
```

### 健康检查

```python
# app/api/health.py
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    """应用健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

@router.get("/ready")
async def readiness_check():
    """就绪检查"""
    # 检查数据库连接
    # 检查 Redis 连接
    # 检查外部 API 连接
    return {"status": "ready"}

@router.get("/live")
async def liveness_check():
    """存活检查"""
    return {"status": "alive"}
```

---

## 总结

### 架构优势

1. **清晰的分层**
   - Infrastructure：通用能力
   - Common：公共组件
   - Modules：业务逻辑

2. **AI解耦**
   - Core.ai：底层技术实现
   - Modules.Agent：上层业务逻辑
   - 物理隔离，易于维护

3. **高可扩展性**
   - 模块化设计，易于添加新功能
   - 快速微服务拆分

4. **易于测试**
   - 核心层可轻松 Mock
   - 业务层独立测试

5. **生产级特性**
   - 异步优先
   - 完善的错误处理
   - 结构化日志
   - 性能监控
   - 健康检查

### 最佳实践

1. **依赖倒置**
   - Core 层不依赖 Modules
   - Modules 只依赖 Core 和 Common

2. **接口抽象**
   - AI 接口抽象
   - 数据访问接口抽象

3. **配置外化**
   - 所有配置通过环境变量
   - 敏感信息使用密钥管理

4. **异步优先**
   - 所有 I/O 操作异步化
   - 提升并发性能

5. **类型安全**
   - 全面使用 Pydantic
   - 运行时类型检查

这个架构设计遵循了 Clean Architecture 和 DDD 的思想，特别针对 AI 应用的特点进行了优化，是目前 Python 后端开发大型 AI 应用的**最佳实践**。
