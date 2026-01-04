"""
测试不带签名的 API 调用
"""
import asyncio
import httpx
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = "2d0d33e3834b6ae17252e588ef5bdd097bd7a8646f6e5b41d900433b333830"


async def test_no_signature():
    """测试不带签名的调用"""
    print("=" * 60)
    print("🔍 测试不带签名的 API 调用")
    print("=" * 60)

    url = "https://restapi.amap.com/v3/geocode/geo"

    # 只使用基本参数，不使用 sig
    params = {
        "key": API_KEY,
        "address": "故宫",
        "city": "北京"
    }

    print(f"\n📤 请求参数: {params}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()

            print(f"\n📥 响应:")
            print(f"   status: {data.get('status')}")
            print(f"   info: {data.get('info')}")
            print(f"   infocode: {data.get('infocode')}")

            if data.get("status") == "1":
                print(f"\n✅ 成功! 不需要签名")
                if data.get("geocodes"):
                    geocode = data["geocodes"][0]
                    print(f"   坐标: {geocode.get('location')}")
            else:
                print(f"\n❌ 失败")

    except Exception as e:
        print(f"\n❌ 异常: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_no_signature())
