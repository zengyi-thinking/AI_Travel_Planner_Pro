# WanderFlow 项目文档

## 文档概述

本项目包含三份核心架构设计文档，基于实际前端演示界面需求，遵循**精简原则**和**最小化接口设计**。

---

## 核心文档

### 1. 📊 数据库设计文档
**文件名**: `database-design.md`

**内容概要**:
- 数据库概述和技术选型
- 9个精简核心表设计
- 索引策略和性能优化
- 数据关系图

**核心表**:
- `users` - 用户主表
- `user_settings` - 用户设置
- `subscriptions` - 订阅管理
- `itineraries` - 行程主表
- `itinerary_days` - 行程详细
- `chat_sessions` - 聊天会话
- `chat_messages` - 聊天消息
- `knowledge_base` - 知识库
- `generated_contents` - 生成内容
- `audit_logs` - 审计日志

**特点**:
- ✅ 精简设计，遵循3NF
- ✅ JSON字段存储灵活数据
- ✅ 索引优化，查询高效
- ✅ 外键约束，完整性保证

---

### 2. 🖥️ 前端架构设计文档
**文件名**: `frontend-design.md`

**内容概要**:
- 技术选型：Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia
- 7个页面详细设计
- 50+组件架构
- 状态管理方案
- 路由设计和API层设计
- 样式系统和构建部署

**页面结构**:
1. 首页 (Home) - 品牌展示
2. 登录 (Login) - 用户认证
3. 注册 (Register) - 用户注册
4. 行程规划 (Planner) - AI生成行程
5. AI助手 (QA) - 智能对话
6. 文案生成 (Copywriter) - 内容生成
7. 设置 (Settings) - 用户设置

**架构分层**:
```
Views → Components → Composables → Stores → Utils → Types
```

**特点**:
- ✅ 现代化技术栈
- ✅ 组件化设计
- ✅ TypeScript类型安全
- ✅ 响应式设计

---

### 3. ⚙️ 后端架构设计文档
**文件名**: `backend-design.md`

**内容概要**:
- Core + Modules架构理念
- 核心层设计（Infrastructure + Common + Modules）
- AI架构设计（物理隔离）
- 24个精简API接口
- 部署架构和监控

**API接口统计**:
- 认证模块: 5个接口
- 用户设置: 3个接口
- 行程规划: 5个接口
- AI助手: 6个接口
- 文案生成: 4个接口
- 知识库: 1个接口

**核心优势**:
- ✅ 清晰的架构分层
- ✅ AI解耦设计
- ✅ 最小化接口
- ✅ RESTful规范
- ✅ JWT认证
- ✅ 微服务就绪

---

## 架构设计原则

### 1. 精简原则
- **前端**: 移除不必要组件，避免过度工程化
- **数据库**: 精简字段，使用JSON存储灵活数据
- **接口**: 最小化设计，仅提供必要功能

### 2. 模块化设计
- **前端**: 组件化、模块化、页面独立
- **数据库**: 表关系清晰，职责分明
- **后端**: Core + Modules架构，职责分离

### 3. 性能优化
- **前端**: 代码分割、懒加载、缓存策略
- **数据库**: 索引优化、查询优化
- **接口**: 统一响应、分页查询

### 4. 可维护性
- **前端**: TypeScript类型安全、清晰目录结构
- **数据库**: 遵循范式、注释详细
- **接口**: RESTful规范、文档完整

---

## 开发指南

### 技术栈

**前端**:
- Vue 3.4+ (Composition API)
- TypeScript 5.0+
- Vite 5.0+
- Tailwind CSS 3.4+
- Pinia (状态管理)

**后端**:
- FastAPI 0.110+
- SQLAlchemy 2.0 + aiomysql
- Pydantic 2.5+
- JWT + Passlib
- Redis 7.0+

**数据库**:
- MySQL 8.0+ (主库)
- SQLite 3.x (备份)
- Redis 7.0+ (缓存)

### 开发优先级

1. **第一阶段**: 认证模块（登录、注册、用户管理）
2. **第二阶段**: 行程规划模块（生成、CRUD操作）
3. **第三阶段**: AI助手模块（聊天、天气、语音）
4. **第四阶段**: 文案生成模块（图片上传、内容生成）
5. **第五阶段**: 知识库模块（搜索、RAG）

---

## 文件结构

```
docs/
├── README.md                 # 本文档
├── database-design.md        # 数据库设计（精简版）
├── frontend-design.md        # 前端架构（精简版）
└── backend-design.md         # 后端架构（精简版）

demonstration/
├── index.html                # 首页
├── login.html                # 登录页
├── register.html             # 注册页
├── planner.html              # 行程规划页
├── qa.html                   # AI助手页
├── copywriter.html           # 文案生成页
├── settings.html             # 设置页
├── css/styles.css            # 样式文件
└── js/theme.js               # 主题脚本
```

---

## 关键数据

| 维度 | 数量 |
|------|------|
| 前端页面 | 7个 |
| 前端组件 | 50+ |
| 数据库表 | 9个（精简） |
| API接口 | 24个（精简） |
| 文档总行数 | 3,870行 |
| 文档总大小 | 112KB |

---

## 架构优势

### ✅ 清晰的分层
- 前端：Views → Components → Composables → Stores → Utils
- 后端：Infrastructure → Common → Business (Modules)

### ✅ 精简高效
- 数据库：移除冗余字段，使用JSON存储
- 接口：最小化设计，避免过度工程化
- 前端：组件化复用，代码量优化

### ✅ 易于维护
- TypeScript类型安全
- 清晰的文档和注释
- 统一的编码规范

### ✅ 易于扩展
- 模块化设计，支持功能独立开发
- 微服务就绪架构
- 灵活的数据结构（JSON字段）

### ✅ 现代化技术栈
- Vue 3 + Vite（快速开发）
- FastAPI（高性能异步框架）
- TypeScript（全链路类型安全）

---

## 总结

本架构设计基于**实际前端界面需求**，采用**精简设计**和**最小化接口原则**，确保系统：

1. **结构清晰** - 分层明确，职责分明
2. **易于开发** - 现代化工具链，完善文档
3. **易于维护** - 类型安全，代码规范
4. **易于扩展** - 模块化设计，微服务就绪

整个架构**简洁、高效、可扩展**，为WanderFlow项目提供了坚实的架构基础！ 🚀

---

**文档版本**: v2.0 (精简版)
**更新时间**: 2024-12-19
**作者**: Claude Code
