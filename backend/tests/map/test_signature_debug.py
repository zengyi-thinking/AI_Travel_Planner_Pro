"""
调试高德地图 API 签名
"""
import asyncio
import httpx
import hashlib
import sys
import io

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = "2d0d33e3834b6ae17252e588ef5bdd097bd7a8646f6e5b41d900433b333830"
SECRET_KEY = "997bd7a8646f6e5b41d900433b333830"


def generate_signature(params: dict) -> str:
    """生成签名"""
    print("\n=== 签名生成过程 ===")

    # 1. 排序参数
    sorted_params = sorted(params.items())
    print(f"1. 排序后的参数: {sorted_params}")

    # 2. 拼接参数
    param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
    print(f"2. 参数字符串: {param_str}")

    # 3. 添加密钥
    sign_str = param_str + SECRET_KEY
    print(f"3. 签名原文: {sign_str}")
    print(f"   密钥: {SECRET_KEY}")

    # 4. 计算 MD5
    md5 = hashlib.md5()
    md5.update(sign_str.encode('utf-8'))
    signature = md5.hexdigest()
    print(f"4. MD5 签名: {signature}")

    return signature


async def test_with_signature():
    """测试带签名的 API 调用"""
    print("=" * 60)
    print("🔍 测试高德地图 API 签名认证")
    print("=" * 60)

    url = "https://restapi.amap.com/v3/geocode/geo"

    # 准备参数（不包含 key 和 sig）
    params = {
        "address": "故宫",
        "city": "北京"
    }

    # 生成签名
    sig = generate_signature(params)

    # 添加签名和 key
    params["sig"] = sig
    params["key"] = API_KEY

    print(f"\n📤 最终请求参数:")
    for k, v in sorted(params.items()):
        print(f"   {k}={v}")

    print(f"\n🌐 请求 URL: {url}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            print(f"\n📥 响应状态码: {response.status_code}")
            print(f"📄 响应内容:")
            print(response.text)

            data = response.json()
            if data.get("status") == "1":
                print(f"\n✅ 成功!")
            else:
                print(f"\n❌ 失败:")
                print(f"   status: {data.get('status')}")
                print(f"   info: {data.get('info')}")
                print(f"   infocode: {data.get('infocode')}")

    except Exception as e:
        print(f"\n❌ 异常: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_with_signature())
