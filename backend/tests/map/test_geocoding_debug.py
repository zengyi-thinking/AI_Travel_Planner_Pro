"""
调试高德地图 API 调用
"""
import asyncio
import httpx
import sys
import io

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def test_amap_api():
    """直接测试高德地图 API"""
    api_key = "2d0d33e3834b6ae17252e588ef5bdd097bd7a8646f6e5b41d900433b333830"
    base_url = "https://restapi.amap.com"

    print("=" * 50)
    print("🔍 测试高德地图地理编码 API")
    print("=" * 50)
    print(f"\nAPI Key: {api_key[:20]}...{api_key[-10:]}")

    # 测试地址解析
    url = f"{base_url}/v3/geocode/geo"
    params = {
        "key": api_key,
        "address": "故宫",
        "city": "北京"
    }

    print(f"\n请求 URL: {url}")
    print(f"请求参数: {params}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            print(f"\n响应状态码: {response.status_code}")
            print(f"响应内容:\n{response.text}")

            if response.status_code == 200:
                data = response.json()
                print(f"\n解析结果:")
                print(f"  status: {data.get('status')}")
                print(f"  info: {data.get('info')}")
                print(f"  infocode: {data.get('infocode')}")

                if data.get("status") == "1" and data.get("geocodes"):
                    geocode = data["geocodes"][0]
                    location = geocode.get("location", "")
                    print(f"\n✅ 成功获取坐标:")
                    print(f"  位置: {location}")
                    print(f"  格式化地址: {geocode.get('formatted_address', '')}")
                else:
                    print(f"\n❌ API 返回错误:")
                    print(f"  status: {data.get('status')}")
                    print(f"  info: {data.get('info')}")
                    print(f"  infocode: {data.get('infocode')}")

    except httpx.HTTPError as e:
        print(f"\n❌ HTTP 请求失败: {e}")
    except Exception as e:
        print(f"\n❌ 异常: {e}")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(test_amap_api())
