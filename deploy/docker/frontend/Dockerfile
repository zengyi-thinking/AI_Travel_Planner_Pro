# 构建阶段
FROM node:20-alpine AS builder

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV NODE_ENV=production

# 安装依赖
COPY frontend/package*.json ./
RUN npm ci

# 复制代码并构建
COPY frontend/ ./
RUN npm run build

# 生产阶段 - 使用 Nginx 作为服务器
FROM nginx:alpine AS production

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY deploy/docker/nginx/frontend.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
