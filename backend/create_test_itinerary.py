"""
创建带坐标的测试行程数据
用于验证前端地图标记显示
"""
import asyncio
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def create_test_itinerary():
    """创建带坐标的测试行程"""
    print("=" * 70)
    print("🧪 测试行程数据验证（带百度地图坐标）")
    print("=" * 70)

    # 模拟完整的行程数据（带百度地图坐标）
    test_itinerary_data = {
        "title": "北京3日文化深度游",
        "destination": "北京",
        "departure": "上海",
        "days": 3,
        "budget": 5000,
        "travel_style": "leisure",
        "days": [
            {
                "day_number": 1,
                "title": "故宫周边深度游",
                "date": "2025-01-10",
                "activities": [
                    {
                        "time": "09:00",
                        "title": "故宫博物院",
                        "type": "attraction",
                        "description": "中国明清两代的皇家宫殿，世界文化遗产",
                        "location": "北京市东城区景山前街4号",
                        "duration": "3小时",
                        "average_cost": 60,
                        "coordinates": {
                            "lng": 116.40198150528495,
                            "lat": 39.927388327577795
                        }
                    },
                    {
                        "time": "12:30",
                        "title": "全聚德烤鸭店",
                        "type": "meal",
                        "description": "百年老字号，品尝正宗北京烤鸭",
                        "location": "北京市东城区前门大街30号",
                        "duration": "1.5小时",
                        "average_cost": 200,
                        "cuisine": "北京菜",
                        "coordinates": {
                            "lng": 116.397029,
                            "lat": 39.900123
                        }
                    },
                    {
                        "time": "15:00",
                        "title": "天安门广场",
                        "type": "attraction",
                        "description": "世界上最大的城市广场之一",
                        "location": "北京市东城区",
                        "duration": "1小时",
                        "average_cost": 0,
                        "coordinates": {
                            "lng": 116.4224009776628,
                            "lat": 39.93482727239599
                        }
                    },
                    {
                        "time": "19:00",
                        "title": "北京饭店",
                        "type": "accommodation",
                        "description": "四星级商务酒店",
                        "location": "北京市东城区东长安街33号",
                        "duration": "晚上",
                        "average_cost": 600,
                        "coordinates": {
                            "lng": 116.410123,
                            "lat": 39.915456
                        }
                    }
                ],
                "total_cost": 860
            },
            {
                "day_number": 2,
                "title": "长城一日游",
                "date": "2025-01-11",
                "activities": [
                    {
                        "time": "08:00",
                        "title": "八达岭长城",
                        "type": "attraction",
                        "description": "明长城的精华路段，雄伟壮观",
                        "location": "北京市延庆区八达岭",
                        "duration": "4小时",
                        "average_cost": 40,
                        "coordinates": {
                            "lng": 116.016863,
                            "lat": 40.358431
                        }
                    },
                    {
                        "time": "13:00",
                        "title": "长城脚下农家菜",
                        "type": "meal",
                        "description": "品尝当地特色菜",
                        "location": "北京市延庆区八达岭镇",
                        "duration": "1小时",
                        "average_cost": 80,
                        "cuisine": "农家菜",
                        "coordinates": {
                            "lng": 116.018542,
                            "lat": 40.359123
                        }
                    }
                ],
                "total_cost": 120
            },
            {
                "day_number": 3,
                "title": "颐和园漫步",
                "date": "2025-01-12",
                "activities": [
                    {
                        "time": "09:00",
                        "title": "颐和园",
                        "type": "attraction",
                        "description": "中国古典园林之首",
                        "location": "北京市海淀区新建宫门路",
                        "duration": "3小时",
                        "average_cost": 30,
                        "coordinates": {
                            "lng": 116.28438433097374,
                            "lat": 40.008141350407804
                        }
                    },
                    {
                        "time": "12:30",
                        "title": "颐和园附近餐厅",
                        "type": "meal",
                        "description": "享用午餐",
                        "location": "北京市海淀区",
                        "duration": "1小时",
                        "average_cost": 100,
                        "coordinates": {
                            "lng": 116.283123,
                            "lat": 40.009234
                        }
                    }
                ],
                "total_cost": 130
            }
        ],
        "summary": "深度游览北京故宫、长城、颐和园三大世界文化遗产",
        "highlights": [
            "故宫博物院深度游",
            "八达岭长城壮丽风光",
            "颐和园皇家园林美景"
        ],
        "best_season": "春季和秋季",
        "weather": "注意保暖，建议穿舒适的鞋子",
        "preparation": {
            "documents": ["身份证", "学生证（如有）"],
            "essentials": ["舒适的步行鞋", "防晒霜", "充电宝"],
            "booking_reminders": ["故宫需提前预约", "长城建议提前预订往返交通"]
        },
        "tips": {
            "transportation": "地铁+公交是最佳出行方式",
            "accommodation": "建议住在二环内，交通便利",
            "food": "北京烤鸭、涮羊肉必尝",
            "shopping": "王府井、西单适合购物",
            "safety": "注意保管财物，避免拥挤"
        }
    }

    print(f"\n✅ 测试数据准备完成:")
    print(f"   行程标题: {test_itinerary_data['title']}")
    print(f"   目的地: {test_itinerary_data['destination']}")
    print(f"   天数: {test_itinerary_data['days']}")
    print(f"   总活动数: {sum(len(day['activities']) for day in test_itinerary_data['days'])}")

    print(f"\n📍 坐标数据验证:")
    for day in test_itinerary_data['days']:
        print(f"\n   第{day['day_number']}天 - {day['title']}:")
        for activity in day['activities']:
            has_coords = 'coordinates' in activity and activity['coordinates']
            status = "✅" if has_coords else "❌"
            coords = activity.get('coordinates', {})
            print(f"      {status} {activity['title']}: {coords if has_coords else '无坐标'}")

    print(f"\n" + "=" * 70)
    print(f"📝 前端测试步骤:")
    print(f"=" * 70)
    print(f"1. 访问: http://localhost:3002")
    print(f"2. 登录系统")
    print(f"3. 生成新行程（目的地：北京，天数：3）")
    print(f"4. 等待 AI 生成完成并自动添加坐标")
    print(f"5. 查看地图预览区域")
    print(f"6. 应该看到:")
    print(f"   - 📍 多个彩色标记点（景点=红，美食=橙，住宿=蓝）")
    print(f"   - 🔗 虚线连接各点形成路线")
    print(f"   - 点击标记查看详情")
    print(f"   - 切换天数查看不同路线")
    print(f"=" * 70)


if __name__ == "__main__":
    asyncio.run(create_test_itinerary())
