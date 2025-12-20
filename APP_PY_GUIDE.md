# 🎉 WanderFlow - app.py 启动指南

## ✅ 当前状态

### 后端服务
- **文件**: `backend/app.py` (完整版)
- **状态**: ✅ 正在运行
- **地址**: http://localhost:8000
- **启动方式**: `python app.py`

### 前端服务
- **文件**: `frontend/` (Vue 3 + Vite)
- **状态**: ✅ 正在运行
- **地址**: http://localhost:3000
- **启动方式**: `npm run dev`

## 🚀 使用方法

### 启动后端

```bash
cd backend

# Windows
source venv\Scripts\activate
python app.py

# Linux/Mac
source venv/bin/activate
python app.py
```

### 启动前端

```bash
cd frontend
npm run dev
```

### 指定端口 (后端)

```bash
python app.py 3000  # 使用 3000 端口
```

## 📡 可用的 API 端点

### 基础端点
- `GET /` - 应用信息
- `GET /health` - 健康检查
- `GET /docs` - API 文档 (Swagger UI)
- `GET /redoc` - API 文档 (ReDoc)

### 用户认证
- `POST /api/v1/auth/register` - 注册
- `POST /api/v1/auth/login` - 登录
- `GET /api/v1/users/me` - 当前用户

### 行程规划
- `GET /api/v1/itineraries` - 获取行程列表
- `POST /api/v1/itineraries` - 创建行程
- `GET /api/v1/itineraries/{id}` - 获取行程详情
- `POST /api/v1/itineraries/{id}/generate` - AI 生成行程

### 智能问答
- `POST /api/v1/qa/chat` - 发送消息
- `GET /api/v1/qa/sessions` - 获取对话列表
- `POST /api/v1/qa/sessions` - 创建对话

### 文案生成
- `POST /api/v1/copywriting/generate` - 生成文案
- `GET /api/v1/copywriting/results` - 获取历史记录

## 📊 文件结构

```
wanderflow/
├── backend/
│   ├── app.py              # ← 新的完整版入口文件
│   ├── simple_main.py      # 旧的简化版 (不再使用)
│   ├── app/                # 完整应用结构
│   │   ├── main.py         # 原始完整入口 (未启用)
│   │   ├── core/           # 核心模块
│   │   ├── common/         # 公共层
│   │   └── modules/        # 业务模块
│   ├── venv/               # 虚拟环境
│   └── requirements.txt    # 依赖
│
├── frontend/               # Vue 3 前端
│   ├── src/                # 源码
│   ├── node_modules/       # 依赖
│   └── package.json        # 配置
│
├── docs/                   # 文档
│   ├── BACKEND.md
│   └── FRONTEND.md
│
└── README.md               # 主文档
```

## 🔧 开发命令

### 后端
```bash
cd backend

# 激活环境
source venv/Scripts/activate

# 启动服务
python app.py

# 安装依赖
pip install package_name
```

### 前端
```bash
cd frontend

# 启动服务
npm run dev

# 构建生产版
npm run build

# 代码检查
npm run lint
```

## ✨ 新特性

### app.py 的优势
1. **完整模块结构** - 所有业务模块已定义
2. **清晰的项目结构 - Core + Modules 三层架构
3. **完整 API 文档 - 自动生成 Swagger/ReDoc
4. **错误处理 - 全局异常处理
5. **CORS 支持 - 跨域请求支持
6. **热重载 - 开发时自动重载
7. **中文支持 - 中文错误信息

### 技术栈
- **后端**: FastAPI + Uvicorn + SQLAlchemy + Pydantic
- **前端**: Vue 3 + TypeScript + Vite + Tailwind CSS
- **数据库**: MySQL + Redis (待配置)
- **AI 集成**: OpenAI (待配置)

## 📝 下一步开发

### 立即可做
1. 查看 API 文档: http://localhost:8000/docs
2. 访问前端应用: http://localhost:3000
3. 测试各个 API 端点

### 近期计划
1. 实现具体的业务逻辑
2. 配置数据库连接
3. 添加用户认证系统
4. 集成 AI 服务
5. 完善前端页面

## 🆘 常见问题

### Q: 如何停止服务？
A: 在终端按 `Ctrl+C`

### Q: 端口被占用？
A: 指定其他端口: `python app.py 8001`

### Q: 如何重启服务？
A: 停止后重新运行 `python app.py`

### Q: 前端无法连接后端？
A: 检查后端是否在 8000 端口运行

## 📚 更多文档

- [后端开发指南](docs/BACKEND.md)
- [前端开发指南](docs/FRONTEND.md)
- [快速开始](QUICKSTART.md)
- [项目文档](README.md)

---

**创建时间**: 2024-12-20  
**状态**: ✅ 开发环境就绪  
**版本**: v1.0.0
