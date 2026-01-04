"""
测试百度地图 API Key
"""
import asyncio
import httpx
import sys
import io

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


async def test_baidu_geocoding():
    """测试百度地图地理编码 API"""
    print("=" * 60)
    print("🔍 测试百度地图地理编码 API")
    print("=" * 60)

    api_key = "AWOJy2FcuCFxtns6sdS3YS57RArBNp74"
    print(f"\n📋 API Key: {api_key}")

    # 百度地图地理编码 API
    url = "http://api.map.baidu.com/geocoding/v3/"

    params = {
        "address": "故宫",
        "city": "北京",
        "output": "json",
        "ak": api_key
    }

    print(f"\n📤 请求 URL: {url}")
    print(f"📤 请求参数: {params}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            print(f"\n📥 响应状态码: {response.status_code}")
            print(f"📄 响应内容:")
            print(response.text)

            data = response.json()

            if data.get("status") == 0:
                print(f"\n✅ 成功!")
                result = data.get("result", {})
                location = result.get("location", {})
                print(f"   经度: {location.get('lng')}")
                print(f"   纬度: {location.get('lat')}")
                print(f"   精确度: {location.get('precise')}")
                print(f"   置信度: {location.get('confidence')}")
                return True
            else:
                print(f"\n❌ 失败:")
                print(f"   status: {data.get('status')}")
                print(f"   message: {data.get('message')}")
                return False

    except Exception as e:
        print(f"\n❌ 异常: {e}")
        return False

    finally:
        print("\n" + "=" * 60)


async def test_multiple_addresses():
    """测试多个地址解析"""
    print("\n" + "=" * 60)
    print("🗺️ 测试多个热门景点")
    print("=" * 60)

    api_key = "AWOJy2FcuCFxtns6sdS3YS57RArBNp74"
    url = "http://api.map.baidu.com/geocoding/v3/"

    test_cases = [
        ("故宫", "北京"),
        ("外滩", "上海"),
        ("宽窄巷子", "成都"),
        ("天山天池", "新疆"),
    ]

    for address, city in test_cases:
        params = {
            "address": address,
            "city": city,
            "output": "json",
            "ak": api_key
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                data = response.json()

                if data.get("status") == 0:
                    result = data.get("result", {})
                    location = result.get("location", {})
                    print(f"\n✅ {address} ({city})")
                    print(f"   坐标: ({location.get('lng')}, {location.get('lat')})")
                else:
                    print(f"\n❌ {address} ({city})")
                    print(f"   错误: {data.get('message')}")

        except Exception as e:
            print(f"\n❌ {address} ({city})")
            print(f"   异常: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # 测试单个地址
    success = asyncio.run(test_baidu_geocoding())

    # 如果成功，测试多个地址
    if success:
        asyncio.run(test_multiple_addresses())
