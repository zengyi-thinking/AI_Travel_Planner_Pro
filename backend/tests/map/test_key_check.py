"""
API Key 诊断脚本
"""
import asyncio
import httpx
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


async def diagnose_api_key():
    """诊断 API Key 配置"""
    print("=" * 70)
    print("🔍 高德地图 API Key 诊断")
    print("=" * 70)

    api_keys = [
        ("你提供的 Key", "2d0d33e3834b6ae17252e588ef5bdd097bd7a8646f6e5b41d900433b333830"),
        ("原 .env 中的 Key", "AWOJy2FcuCFxtns6sdS3YS57RArBNp74"),
    ]

    print("\n建议检查以下内容：\n")
    print("1. 高德地图控制台: https://console.amap.com/dev/key/app")
    print("2. 确认你的 key 名称: langchain_using")
    print("3. 检查「绑定服务」是否包含：「Web端」或「Web服务」")
    print("4. 检查「IP白名单」设置（应该为空或包含你的服务器IP）")
    print("5. 检查 key 状态是否为「启用」\n")

    print("=" * 70)
    print("常见错误代码含义：")
    print("=" * 70)
    print("10001 | INVALID_USER_KEY")
    print("      -> Key 无效、未激活或服务未开通")
    print("      -> 解决：检查 key 配置，确保开通了「Web端服务」")
    print()
    print("10003 | INVALID_SIGNATURE")
    print("      -> 签名验证失败")
    print("      -> 解决：检查安全密钥配置")
    print()
    print("10004 | ACCESS_KEY_OVER_LIMIT")
    print("      -> 配额超限")
    print("      -> 解决：升级配额或等待配额重置")
    print("=" * 70)

    print("\n\n🔧 临时解决方案：")
    print("=" * 70)
    print("选项 1: 使用示例坐标数据")
    print("  - 优点：立即可用，不需要 API Key")
    print("  - 缺点：坐标是固定的，不能动态解析任意地址")
    print()
    print("选项 2: 重新申请一个新的 API Key")
    print("  - 访问：https://console.amap.com/dev/key/app")
    print("  - 点击「创建新 Key」")
    print("  - 服务选择：Web端")
    print("  - IP白名单：留空（不限制）")
    print()
    print("选项 3: 检查现有 Key 配置")
    print("  - 登录控制台")
    print("  - 找到 Key: langchain_using")
    print("  - 点击「设置」")
    print("  - 确认绑定了「Web服务」或「Web端API」")
    print("  - 如果没有绑定，需要重新创建 key 并选择正确服务")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(diagnose_api_key())
