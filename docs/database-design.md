# WanderFlow - 数据库设计文档（精简版）

## 目录
1. [概述](#概述)
2. [设计原则](#设计原则)
3. [数据表设计](#数据表设计)
4. [索引策略](#索引策略)
5. [数据关系图](#数据关系图)
6. [性能优化](#性能优化)

---

## 概述

### 技术选型
- **主数据库**: MySQL 8.0+
- **字符集**: utf8mb4 (支持emoji)
- **存储引擎**: InnoDB (支持事务和外键)

### 数据库配置
```sql
-- 基础配置
CHARACTER SET: utf8mb4
COLLATION: utf8mb4_unicode_ci
ENGINE: InnoDB
```

---

## 设计原则

### 1. 范式设计
- 遵循第三范式（3NF）
- 减少数据冗余
- 保证数据一致性

### 2. 精简原则
- 移除不必要的字段
- 避免过度设计
- 仅存储核心业务数据

### 3. 性能优先
- 关键字段建立索引
- 避免过多JOIN查询
- 合理使用JSON字段

### 4. 扩展性
- 使用JSON字段存储灵活属性
- 预留扩展空间
- 支持软删除

---

## 数据表设计

### 用户管理模块

#### 1. users - 用户主表

**表名**: `users`

**描述**: 存储用户核心信息，最小化字段设计。

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT '邮箱地址',
    phone VARCHAR(20) COMMENT '手机号码',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    name VARCHAR(100) NOT NULL COMMENT '用户姓名',
    avatar_url VARCHAR(500) COMMENT '头像URL',
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active' COMMENT '账户状态',
    email_verified BOOLEAN DEFAULT FALSE COMMENT '邮箱是否验证',
    last_login_at TIMESTAMP NULL COMMENT '最后登录时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    -- 索引
    INDEX idx_users_email (email),
    INDEX idx_users_phone (phone),
    INDEX idx_users_status (status),
    INDEX idx_users_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

**字段精简说明**:
- 移除不必要的字段（如is_active冗余，用status代替）
- 合并相似字段
- 仅保留核心认证和展示字段

#### 2. user_settings - 用户设置表

**表名**: `user_settings`

**描述**: 存储用户偏好设置，使用JSON存储灵活配置。

```sql
CREATE TABLE user_settings (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    user_id BIGINT NOT NULL UNIQUE COMMENT '用户ID',
    language VARCHAR(10) DEFAULT 'zh-CN' COMMENT '界面语言',
    theme ENUM('light', 'dark', 'auto') DEFAULT 'auto' COMMENT '主题模式',
    timezone VARCHAR(50) DEFAULT 'Asia/Shanghai' COMMENT '时区',
    currency VARCHAR(10) DEFAULT 'CNY' COMMENT '默认货币',
    preferences JSON COMMENT '用户偏好JSON (预算范围、住宿偏好等)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_settings_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设置表';
```

**设计说明**:
- 使用JSON字段存储灵活偏好，避免过多列
- 一对一关系（UNIQUE约束）

#### 3. subscriptions - 用户订阅表

**表名**: `subscriptions`

**描述**: 存储用户会员订阅信息。

```sql
CREATE TABLE subscriptions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    plan_type ENUM('free', 'pro', 'enterprise') DEFAULT 'free' COMMENT '订阅计划',
    status ENUM('active', 'cancelled', 'expired') DEFAULT 'active' COMMENT '订阅状态',
    start_date TIMESTAMP NOT NULL COMMENT '开始日期',
    end_date TIMESTAMP NOT NULL COMMENT '结束日期',
    auto_renew BOOLEAN DEFAULT FALSE COMMENT '是否自动续费',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_subscriptions_user_id (user_id),
    INDEX idx_subscriptions_status (status),
    INDEX idx_subscriptions_end_date (end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户订阅表';
```

---

### 行程规划模块

#### 1. itineraries - 行程主表

**表名**: `itineraries`

**描述**: 存储用户创建的行程核心信息。

```sql
CREATE TABLE itineraries (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '行程ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    title VARCHAR(200) NOT NULL COMMENT '行程标题',
    destination VARCHAR(200) NOT NULL COMMENT '目的地',
    departure VARCHAR(200) COMMENT '出发地',
    days INT NOT NULL COMMENT '旅行天数',
    budget DECIMAL(12, 2) COMMENT '预算 (CNY)',
    travel_style ENUM('leisure', 'adventure', 'foodie') DEFAULT 'leisure' COMMENT '旅行风格',
    status ENUM('draft', 'active', 'completed', 'archived') DEFAULT 'draft' COMMENT '行程状态',
    ai_generated BOOLEAN DEFAULT FALSE COMMENT '是否AI生成',
    metadata JSON COMMENT '扩展元数据 (人数、偏好等)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_itineraries_user_id (user_id),
    INDEX idx_itineraries_destination (destination),
    INDEX idx_itineraries_status (status),
    INDEX idx_itineraries_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='行程主表';
```

**字段精简说明**:
- 移除冗余的description字段（可存储在metadata中）
- 使用ENUM优化状态和风格字段
- 合并相关属性到metadata JSON

#### 2. itinerary_days - 行程详细安排表

**表名**: `itinerary_days`

**描述**: 存储每天的详细行程安排。

```sql
CREATE TABLE itinerary_days (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    itinerary_id BIGINT NOT NULL COMMENT '行程ID',
    day_number INT NOT NULL COMMENT '第几天 (从1开始)',
    date DATE COMMENT '具体日期',
    title VARCHAR(200) COMMENT '当天主题',
    activities JSON COMMENT '活动列表JSON (包含时间、地点、活动类型)',
    notes TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_itinerary_days_itinerary_id (itinerary_id),
    INDEX idx_itinerary_days_day (day_number),
    UNIQUE KEY uk_itinerary_day (itinerary_id, day_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='行程详细安排表';
```

**设计说明**:
- 使用JSON存储灵活的活动列表
- 避免过度规范化（活动不需要单独建表）

---

### AI助手模块

#### 1. chat_sessions - 聊天会话表

**表名**: `chat_sessions`

**描述**: 存储用户的聊天会话。

```sql
CREATE TABLE chat_sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '会话ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    title VARCHAR(200) COMMENT '会话标题',
    features JSON COMMENT '启用的功能 (knowledge_base, weather, voice)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_chat_sessions_user_id (user_id),
    INDEX idx_chat_sessions_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci表';
```

** COMMENT='聊天会话- 会话可设计说明**:
保存启用的功能配置
- 支持多个会话

#### 2. chat_messages - 聊天消息表

**表名**: `chat_messages`

**描述**: 存储聊天消息内容。

```sql
 (
    id BIGCREATE TABLE chat_messagesINT PRIMARY KEY AUTO_INCREMENT COMMENT '消息ID',
    session_id BIGINT NOT NULL COMMENT '会话ID',
    role ENUM('user', 'assistant', 'system') NOT NULL COMMENT '消息角色',
    content TEXT NOT NULL COMMENT '消息内容',
    message_type ENUM('text', 'image', 'audio', 'weather', 'quick_action') DEFAULT 'text' COMMENT '消息类型',
    metadata JSON COMMENT '扩展元数据 (语音转文字结果、天气数据等)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_chat_messages_session_id (session_id),
    INDEX idx_chat_messages_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='聊天消息表';
```

**设计说明**:
- 支持多种消息类型
- 使用JSON存储特殊消息的元数据（如天气、语音识别结果）

#### 3. knowledge_base - 知识库表

**表名**: `knowledge_base`

**描述**: 存储旅游攻略知识库文档。

```sql
CREATE TABLE knowledge_base (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '文档ID',
    title VARCHAR(200) NOT NULL COMMENT '文档标题',
    content LONGTEXT NOT NULL COMMENT '文档内容',
    source_type ENUM('pdf', 'web', 'manual') DEFAULT 'pdf' COMMENT '来源类型',
    source_url VARCHAR(500) COMMENT '来源URL',
    tags JSON COMMENT '标签数组 (城市、主题等)',
    embedding VECTOR(1536) COMMENT '向量嵌入 (可选)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- 索引
    INDEX idx_kb_tags (tags),
    INDEX idx_kb_source_type (source_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识库表';
```

**设计说明**:
- 使用LONGTEXT存储大文本
- 预留向量字段支持RAG检索
- JSON标签支持多维度分类

---

### 文案生成模块

#### 1. generated_contents - 生成内容表

**表名**: `generated_contents`

**描述**: 存储AI生成的内容。

```sql
CREATE TABLE generated_contents (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '内容ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    content_type ENUM('copywriting', 'itinerary', 'chat') NOT NULL COMMENT '内容类型',
    platform ENUM('xiaohongshu', 'wechat', 'weibo', 'other') COMMENT '平台',
    input_data JSON COMMENT '输入参数 (图片、关键词、情感等)',
    output_content LONGTEXT NOT NULL COMMENT '生成的内容',
    rating INT COMMENT '用户评分 (1-5)',
    feedback TEXT COMMENT '用户反馈',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

    -- 索引
    INDEX idx_gc_user_id (user_id),
    INDEX idx_gc_type (content_type),
    INDEX idx_gc_platform (platform),
    INDEX idx_gc_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='生成内容表';
```

**设计说明**:
- 复用表存储不同类型生成内容
- JSON存储灵活的输入参数

---

### 系统模块

#### 1. audit_logs - 审计日志表

**表名**: `audit_logs`

**描述**: 记录关键操作日志。

```sql
CREATE TABLE audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    user_id BIGINT COMMENT '用户ID',
    action VARCHAR(100) NOT NULL COMMENT '操作类型',
    resource_type VARCHAR(50) COMMENT '资源类型',
    resource_id BIGINT COMMENT '资源ID',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    metadata JSON COMMENT '额外信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,

    -- 索引
    INDEX idx_audit_user_id (user_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';
```

---

## 索引策略

### 核心索引

1. **主键索引**: 所有表的主键自增索引
2. **唯一索引**: email、user_id等唯一约束
3. **复合索引**: 常用查询条件的组合索引
4. **覆盖索引**: 避免回表的索引

### 索引建议

```sql
-- 用户表核心查询优化
CREATE INDEX idx_users_email_status ON users(email, status);
CREATE INDEX idx_users_last_login ON users(last_login_at);

-- 行程表查询优化
CREATE INDEX idx_itineraries_user_status ON itineraries(user_id, status);
CREATE INDEX idx_itineraries_dest_style ON itineraries(destination, travel_style);

-- 聊天消息查询优化
CREATE INDEX idx_chat_messages_session_time ON chat_messages(session_id, created_at);
```

---

## 数据关系图

```
┌─────────────┐
│    users    │◄─────────────┐
└──────┬──────┘             │
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────────┐
│user_settings│     │ subscriptions   │
└─────────────┘     └────────┬────────┘
                              │
       ┌──────────────────────┘
       ▼
┌─────────────┐      ┌─────────────────┐
│ itineraries │◄────►│ itinerary_days  │
└──────┬──────┘      └─────────────────┘
       │
       ▼
┌─────────────┐      ┌─────────────────┐
│chat_sessions│◄────►│ chat_messages   │
└──────┬──────┘      └─────────────────┘
       │
       ▼
┌─────────────┐
│knowledge_base│
└─────────────┘
       │
       ▼
┌─────────────┐
│generated_   │
│ contents    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ audit_logs  │
└─────────────┘
```

---

## 性能优化

### 1. 查询优化
- 避免SELECT *
- 使用LIMIT分页
- 合理使用JOIN
- 读写分离（主从复制）

### 2. 缓存策略
- Redis缓存热点数据
- 查询结果缓存
- 会话数据缓存

### 3. 分区表
- 大表按时间分区（chat_messages、audit_logs）
- 按用户分区（用户数据量大时）

### 4. 归档策略
- 历史聊天消息定期归档
- 审计日志定期清理
- 软删除代替硬删除

---

## 总结

### 精简设计要点

1. **表数量精简**: 9个核心表，涵盖所有功能
2. **字段精简**: 移除冗余字段，使用JSON存储灵活数据
3. **索引优化**: 关键查询路径建立索引
4. **范式平衡**: 3NF + 适当反规范化
5. **扩展性**: JSON字段支持未来扩展

### 与前端功能映射

- **用户管理**: users, user_settings, subscriptions
- **行程规划**: itineraries, itinerary_days
- **AI助手**: chat_sessions, chat_messages, knowledge_base
- **文案生成**: generated_contents
- **系统功能**: audit_logs

### 优势

1. **结构清晰**: 核心表逻辑分明
2. **性能高效**: 精简字段，快速查询
3. **易于维护**: 合理分层，减少复杂度
4. **扩展灵活**: JSON字段支持变化需求
5. **数据一致**: 外键约束保证完整性
