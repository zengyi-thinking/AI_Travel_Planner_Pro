"""
测试百度地图完整集成流程
"""
import asyncio
import sys
import os
import io

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.baidu_geocoding_service import BaiduGeocodingService
from app.core.config.settings import settings


async def test_service_integration():
    """测试服务集成"""
    print("=" * 70)
    print("🧪 测试百度地图服务完整集成")
    print("=" * 70)

    # 1. 检查配置
    print("\n📋 配置检查:")
    print(f"  MAP_PROVIDER: {settings.MAP_PROVIDER}")
    print(f"  MAP_API_KEY: {settings.MAP_API_KEY[:20]}...{settings.MAP_API_KEY[-10:] if settings.MAP_API_KEY else 'None'}")

    # 2. 初始化服务
    print(f"\n🔧 服务初始化:")
    service = BaiduGeocodingService()
    print(f"  API Key: {service.api_key[:20]}...{service.api_key[-10:]}")
    print(f"  服务状态: ✅ 已就绪")

    # 3. 测试地址解析（模拟真实行程数据）
    print(f"\n🗺️ 测试地址解析（模拟行程数据）:")
    print("-" * 70)

    # 模拟一个真实行程
    test_activities = [
        {"title": "故宫博物院", "location": "北京市东城区景山前街4号", "city": "北京"},
        {"title": "天安门广场", "location": "北京市东城区", "city": "北京"},
        {"title": "颐和园", "location": "北京市海淀区新建宫门路", "city": "北京"},
        {"title": "外滩", "location": "上海市黄浦区", "city": "上海"},
        {"title": "宽窄巷子", "location": "成都市青羊区", "city": "成都"},
    ]

    for activity in test_activities:
        address = activity.get("location") or activity.get("title")
        city = activity.get("city", "")

        print(f"\n  📍 解析: {activity['title']}")
        print(f"     地址: {address}")

        try:
            coords = await service.geocode(address=address, city=city)

            if coords:
                print(f"     ✅ 成功!")
                print(f"     坐标: ({coords['lng']}, {coords['lat']})")
                activity['coordinates'] = {"lng": coords['lng'], "lat": coords['lat']}
            else:
                print(f"     ❌ 失败: 未找到坐标")

        except Exception as e:
            print(f"     ❌ 异常: {e}")

    # 4. 测试行程数据格式
    print(f"\n📦 测试行程数据格式:")
    print("-" * 70)

    mock_itinerary = {
        "title": "北京3日游",
        "days": [
            {
                "day_number": 1,
                "title": "北京市区游览",
                "activities": [
                    {
                        "time": "09:00",
                        "title": "故宫博物院",
                        "location": "北京市东城区景山前街4号",
                        "coordinates": test_activities[0].get('coordinates')
                    },
                    {
                        "time": "14:00",
                        "title": "天安门广场",
                        "location": "北京市东城区",
                        "coordinates": test_activities[1].get('coordinates')
                    }
                ]
            }
        ]
    }

    print(f"\n  行程标题: {mock_itinerary['title']}")
    print(f"  总天数: {len(mock_itinerary['days'])}")

    for day in mock_itinerary['days']:
        print(f"\n  第{day['day_number']}天: {day['title']}")
        print(f"  活动数量: {len(day['activities'])}")

        for activity in day['activities']:
            has_coords = activity.get('coordinates') is not None
            status = "✅" if has_coords else "❌"
            coords = activity.get('coordinates', {})
            print(f"    {status} {activity['title']}: {coords if has_coords else '无坐标'}")

    # 5. 总结
    print(f"\n" + "=" * 70)
    print(f"✅ 测试完成!")
    print(f"=" * 70)
    print(f"\n🎯 下一步:")
    print(f"  1. 生成一个新的行程")
    print(f"  2. 检查后端日志确认坐标获取成功")
    print(f"  3. 在前端查看地图显示效果")
    print(f"\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(test_service_integration())
