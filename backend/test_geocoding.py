"""
快速测试百度地图坐标获取
"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.baidu_geocoding_service import BaiduGeocodingService

async def test_geocoding():
    """测试坐标获取"""
    print("=" * 50)
    print("🔍 测试百度地图坐标获取")
    print("=" * 50)

    service = BaiduGeocodingService()
    print(f"✅ 服务初始化成功，API Key: {service.api_key[:20]}...")

    # 测试地址
    test_addresses = [
        ("滕王阁", "南昌"),
        ("外滩", "上海"),
        ("故宫博物院", "北京"),
    ]

    for address, city in test_addresses:
        print(f"\n📍 测试: {address} ({city})")
        result = await service.geocode(address=address, city=city)
        if result:
            print(f"  ✅ 成功: ({result['lng']}, {result['lat']})")
        else:
            print(f"  ❌ 失败: 未找到坐标")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_geocoding())
