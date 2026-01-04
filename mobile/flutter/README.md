# 📱 WanderFlow AI Travel Planner - Flutter 移动端

## 项目概述

WanderFlow AI 旅行助手的 Flutter 移动端应用，支持 Android 和 iOS 双平台。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Flutter | 3.x | 跨平台 UI 框架 |
| Dart | 3.x | 编程语言 |
| Provider/Riverpod | 6.x / 2.x | 状态管理 |
| Dio | 5.x | 网络请求 |
| GoRouter | 13.x | 路由管理 |
| GoogleFonts | 6.x | 字体管理 |

---

## 项目结构

```
lib/
├── main.dart                     # 应用入口
├── api/                          # API 接口层
│   ├── api_client.dart           # HTTP 客户端
│   ├── endpoints.dart            # 接口定义
│   ├── auth_api.dart             # 认证 API
│   ├── planner_api.dart          # 行程规划 API
│   ├── copywriter_api.dart       # 文案生成 API
│   └── qa_api.dart               # AI 对话 API
├── models/                       # 数据模型
│   ├── user.dart                 # 用户模型
│   ├── user_quota.dart           # 用户配额模型
│   ├── itinerary.dart            # 行程模型
│   ├── copywriting_result.dart   # 文案结果模型
│   └── chat_message.dart         # 聊天消息模型
├── screens/                      # 页面
│   ├── auth/                     # 认证页面
│   │   ├── login_screen.dart     # 登录
│   │   └── register_screen.dart  # 注册
│   ├── home/                     # 首页
│   ├── planner/                  # 行程规划
│   ├── copywriter/               # 文案生成
│   ├── chat/                     # AI 对话
│   ├── profile/                  # 个人中心
│   └── settings/                 # 设置
├── components/                   # 组件
│   ├── common/                   # 通用组件
│   │   ├── app_button.dart       # 按钮
│   │   ├── app_input.dart        # 输入框
│   │   └── app_card.dart         # 卡片
│   ├── auth/                     # 认证组件
│   ├── planner/                  # 行程规划组件
│   └── copywriter/               # 文案组件
├── services/                     # 服务
│   └── auth_service.dart         # 认证服务
├── theme/                        # 主题
│   ├── app_theme.dart            # 应用主题
│   └── dimensions.dart           # 尺寸定义
├── utils/                        # 工具
│   ├── constant.dart             # 常量
│   ├── validators.dart           # 验证器
│   └── toast.dart                # 提示
└── routes/                       # 路由
    └── app_router.dart           # 路由配置
```

---

## 环境配置

### 1. 安装 Flutter SDK

下载并安装 Flutter SDK：https://docs.flutter.dev/get-started/install

### 2. 配置环境变量

```bash
export PATH="$PATH:`pwd`/flutter/bin"
```

### 3. 验证安装

```bash
flutter doctor
```

### 4. 配置 API 地址

编辑 `lib/utils/constant.dart`：

```dart
class ApiConstants {
  static const String devUrl = 'http://localhost:8000/api/v1';
  static const String prodUrl = 'https://your-domain.com/api/v1';

  // 开发环境设为 true，生产环境设为 false
  static const bool isDev = true;
}
```

---

## 运行项目

### Android

```bash
# 1. 连接 Android 设备或启动模拟器
flutter devices

# 2. 运行应用
flutter run

# 3. 构建 APK
flutter build apk --release
```

### iOS

```bash
# 1. 打开项目
open ios/Runner.xcworkspace

# 2. 在 Xcode 中配置签名

# 3. 运行应用
flutter run

# 4. 构建 IPA
flutter build ios --release
```

---

## 开发指南

### 1. 创建新页面

1. 在 `lib/screens/` 对应目录创建页面文件
2. 使用 `ConsumerWidget` 或 `ConsumerStatefulWidget`
3. 在 `lib/routes/app_router.dart` 添加路由

```dart
// 示例：创建新页面
class MyNewScreen extends ConsumerWidget {
  const MyNewScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('新页面')),
      body: Center(child: Text('内容')),
    );
  }
}
```

### 2. 调用 API

```dart
import '../api/planner_api.dart';

class MyWidget extends StatelessWidget {
  final PlannerApi _api = PlannerApi();

  Future<void> loadData() async {
    try {
      final response = await _api.getItineraries();
      // 处理响应
    } catch (e) {
      // 处理错误
    }
  }
}
```

### 3. 状态管理

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// 定义 Provider
final myProvider = Provider((ref) => MyService());

// 使用 Provider
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final service = ref.watch(myProvider);
    return Text('数据: ${service.data}');
  }
}
```

---

## 与后端 API 对接

### 认证流程

```
1. 用户输入邮箱密码
2. 调用 AuthApi.login()
3. 保存 access_token 到安全存储
4. 自动添加 Authorization 头到后续请求
```

### API 错误处理

```dart
try {
  final response = await _api.someMethod();
} on DioException catch (e) {
  if (e.response?.statusCode == 401) {
    // Token 失效，重新登录
    await AuthService().logout();
  }
}
```

---

## 开发路线图

### ✅ 已完成

- [x] 项目结构搭建
- [x] 主题配置
- [x] API 客户端封装
- [x] 数据模型定义
- [x] 认证服务
- [x] 路由配置
- [x] 登录/注册页面
- [x] 通用组件库

### 🚧 进行中

- [ ] 首页功能
- [ ] 行程规划功能
- [ ] 文案生成功能
- [ ] AI 对话功能

### 📋 计划中

- [ ] 个人中心
- [ ] 设置页面
- [ ] 语音输入
- [ ] 图片上传
- [ ] PDF 导出

---

## 开发时间估算

| 功能模块 | 预估时间 | 说明 |
|----------|----------|------|
| 首页 | 3天 | 功能入口、卡片展示 |
| 行程规划 | 7天 | 核心功能，较复杂 |
| 文案生成 | 5天 | 图片上传、结果展示 |
| AI 对话 | 4天 | 聊天界面、语音 |
| 个人中心 | 3天 | 信息编辑、订单历史 |
| 设置 | 2天 | 应用配置 |
| 测试优化 | 5天 | 多设备适配 |

**总计**：约 4-5 周

---

## 常见问题

### Q1: Flutter 依赖冲突

```bash
flutter pub get
flutter pub upgrade
```

### Q2: 构建失败

```bash
flutter clean
flutter pub get
flutter run
```

### Q3: iOS 签名问题

在 `ios/Runner.xcworkspace` 中配置：
1. Team 选择
2. Bundle Identifier
3. Provisioning Profile

### Q4: Android 打包问题

检查 `android/app/build.gradle`：
```gradle
minSdkVersion 21
targetSdkVersion 33
```

---

## 性能优化建议

1. **图片优化**：使用 WebP 格式，压缩图片
2. **懒加载**：列表使用 `ListView.builder`
3. **缓存**：使用 `cached_network_image`
4. **代码分割**：按需加载页面
5. **常量优化**：使用 `const` 构造函数

---

## 上架指南

### Android 上架

1. 生成签名密钥
2. 配置 `android/key.properties`
3. 构建 APK：`flutter build apk --release`
4. 上传到 Google Play Console

### iOS 上架

1. 配置开发者账号
2. 在 Xcode 中配置签名
3. 构建 Archive
4. 上传到 App Store Connect

---

## 技术支持

- Flutter 文档：https://docs.flutter.dev/
- Dart 文档：https://dart.dev/guides
- Pub.dev：https://pub.dev/

---

**开发团队**：WanderFlow Team
**最后更新**：2026-01-05
