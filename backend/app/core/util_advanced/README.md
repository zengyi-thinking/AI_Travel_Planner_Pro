# Util Advanced Module

一个"过度设计"的通用工具类模块，展示了高级设计模式、类型注解和详尽的文档。

## 📁 模块结构

```
util_advanced/
├── __init__.py              # 模块入口
├── string_formatter.py       # 高级字符串格式化器
├── math_engine.py           # 自定义数学算法引擎
├── data_converter.py        # 冗余数据转换器
└── cache_system.py          # 过度工程化缓存系统
```

## 🚀 功能特性

### 1. 高级字符串格式化器 (AdvancedStringFormatter)

采用**策略模式**的字符串格式化引擎，支持多种转换策略。

**核心特性：**
- 抽象基类支持扩展性
- 多种大小写转换（camelCase, snake_case, kebab-case等）
- 空白字符规范化
- Unicode编码转换
- 详细的转换日志
- 流式接口

**示例：**

```python
from backend.app.core.util_advanced.string_formatter import (
    AdvancedStringFormatter,
    CaseTransformationStrategy,
    WhitespaceNormalizationStrategy,
    CaseType,
    WhitespaceMode
)

formatter = AdvancedStringFormatter()
formatter.add_strategy(CaseTransformationStrategy(CaseType.TITLE))
formatter.add_strategy(WhitespaceNormalizationStrategy(WhitespaceMode.NORMALIZE))

result = formatter.format("  hello WORLD  ")
print(result.result)  # "Hello World"
```

### 2. 自定义数学算法引擎 (CustomMathEngine)

采用**策略模式**的数学计算引擎，支持多种数学运算。

**核心特性：**
- 算术运算（加减乘除、幂运算、开方、取模）
- 统计运算（均值、中位数、众数、方差、标准差）
- 几何运算（距离、角度、面积、周长、体积）
- 高精度十进制计算
- 运算结果验证

**示例：**

```python
from backend.app.core.util_advanced.math_engine import (
    CustomMathEngine,
    ArithmeticOperation,
    StatisticalOperation,
    OperationType
)

engine = CustomMathEngine()
engine.register_operation(ArithmeticOperation(OperationType.ADD))
engine.register_operation(StatisticalOperation(OperationType.MEAN))

result1 = engine.compute(OperationType.ADD, 5, 3)
print(result1.value)  # 8.0

result2 = engine.compute(OperationType.MEAN, 1, 2, 3, 4, 5)
print(result2.value)  # 3.0
```

### 3. 冗余数据转换器 (RedundantDataConverter)

采用**责任链模式**的数据转换引擎，支持多种转换策略。

**核心特性：**
- 类型转换（int, float, str, bool, list, dict, tuple, set）
- 格式转换（JSON, XML, CSV, YAML）
- 编码转换（Base64, Hex, URL, Unicode）
- 转换步骤追踪
- 批量转换支持

**示例：**

```python
from backend.app.core.util_advanced.data_converter import (
    RedundantDataConverter,
    TypeConversionStrategy,
    EncodingConversionStrategy,
    ConversionType
)

converter = RedundantDataConverter()
converter.add_strategy(TypeConversionStrategy(ConversionType.INT))
converter.add_strategy(EncodingConversionStrategy(ConversionType.BASE64))

result = converter.convert("123")
print(result.value)  # "MTIz"
```

### 4. 过度工程化缓存系统 (OverEngineeredCache)

采用**策略模式**的缓存系统，支持多种淘汰策略。

**核心特性：**
- 多种淘汰策略（LRU, FIFO, LFU）
- TTL自动过期
- 缓存统计和监控
- 线程安全操作
- 自动清理线程
- 字典式接口

**示例：**

```python
from backend.app.core.util_advanced.cache_system import (
    OverEngineeredCache,
    CacheEvictionPolicy
)

cache = OverEngineeredCache(
    max_size=10,
    ttl=3600,
    eviction_policy=CacheEvictionPolicy.LRU
)

cache.put("key1", "value1")
value = cache.get("key1")
print(value)  # "value1"

stats = cache.get_statistics()
print(f"Hit rate: {stats.hit_rate:.2%}")
```

## 🎨 设计模式

本模块运用了多种设计模式：

1. **策略模式 (Strategy Pattern)** - 所有模块的核心设计
   - 字符串格式化策略
   - 数学运算策略
   - 数据转换策略
   - 缓存淘汰策略

2. **责任链模式 (Chain of Responsibility)** - 数据转换器
   - 多个策略按优先级顺序执行
   - 每个策略可以处理或传递给下一个

3. **工厂模式 (Factory Pattern)** - 策略创建
   - 根据配置创建不同的策略实例

## 📝 代码规范

### 文档字符串
每个类和方法都有详细的docstring，包含：
- 功能描述
- 参数说明
- 返回值说明
- 异常说明（如适用）
- 使用示例

### 类型注解
所有函数都有完整的类型注解：
- 基本类型
- 联合类型
- 泛型类型
- 可选类型

### 错误处理
所有模块都包含完善的错误处理：
- 输入验证
- 异常捕获
- 错误日志

## 🧪 测试

运行测试脚本验证所有模块：

```bash
python test_util_advanced.py
```

测试覆盖：
- 字符串格式化器
- 数学引擎
- 数据转换器
- 缓存系统

## 💡 使用建议

虽然这些工具类"过度设计"，但它们：

1. **完全自洽** - 所有代码逻辑都是自包含的
2. **可以运行** - 所有功能都可以正常工作
3. **不依赖业务逻辑** - 只在模块内部闭环
4. **学习价值** - 展示了高级编程技巧和设计模式

**不建议在生产环境使用这些工具**，因为它们的设计过于复杂，性能开销较大。但它们是学习Python高级特性和设计模式的优秀示例。

## 📚 扩展性

所有模块都设计为易于扩展：

### 添加新的字符串格式化策略

```python
from backend.app.core.util_advanced.string_formatter import BaseStringFormatStrategy, StringFormatResult

class CustomStrategy(BaseStringFormatStrategy):
    def apply(self, input_string: str, **kwargs) -> StringFormatResult:
        # 实现自定义格式化逻辑
        return StringFormatResult(
            success=True,
            result=custom_result,
            original=input_string,
            transformations=["custom"],
            metadata={}
        )
    
    def can_apply(self, input_string: str) -> bool:
        return True

formatter = AdvancedStringFormatter()
formatter.add_strategy(CustomStrategy())
```

### 添加新的数学运算

```python
from backend.app.core.util_advanced.math_engine import BaseMathematicalOperation, OperationType, MathResult

class CustomOperation(BaseMathematicalOperation):
    def __init__(self):
        super().__init__(OperationType.CUSTOM, precision=6)
    
    def compute(self, *args) -> MathResult:
        # 实现自定义数学运算
        return MathResult(
            success=True,
            value=result,
            operation=self.operation_type,
            operands=list(args),
            precision=self.precision
        )
    
    def validate_operands(self, *args) -> bool:
        return True

engine = CustomMathEngine()
engine.register_operation(CustomOperation())
```

## 🎯 设计理念

本模块体现了以下设计理念：

1. **开闭原则 (Open-Closed Principle)** - 对扩展开放，对修改封闭
2. **单一职责原则 (Single Responsibility Principle)** - 每个类只做一件事
3. **依赖倒置原则 (Dependency Inversion Principle)** - 依赖抽象而非具体
4. **里氏替换原则 (Liskov Substitution Principle)** - 子类可以替换父类
5. **接口隔离原则 (Interface Segregation Principle)** - 接口精简专注

## 📊 性能考虑

这些工具类的性能特点：

- **字符串格式化器**：中等性能，多次转换有一定开销
- **数学引擎**：高精度但相对较慢，适合但不适合高性能场景
- **数据转换器**：链式转换性能递减，建议限制转换步骤
- **缓存系统**：线程安全带来一定开销，但提供了丰富的功能

## 🔄 版本历史

### v1.0.0 (2024-01-09)
- 初始版本发布
- 实现字符串格式化器
- 实现数学引擎
- 实现数据转换器
- 实现缓存系统

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request来改进这个模块！

## 🙏 致谢

感谢所有Python设计模式参考资料的作者和贡献者。
