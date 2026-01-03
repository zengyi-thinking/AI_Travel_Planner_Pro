"""
简化版AI生成测试
只测试AI生成功能，不涉及数据库
"""

import asyncio
import sys
import os
from pathlib import Path

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.modules.planner.agents.planner_agent import TravelPlannerAgent
import json
from datetime import datetime


async def test_ai_generation_only():
    """
    只测试AI生成功能，不保存到数据库
    """
    print("=" * 80)
    print("🚀 测试AI行程生成功能（简化版）")
    print("=" * 80)

    # 创建agent
    agent = TravelPlannerAgent(use_strict_json=True)

    # 测试数据
    test_cases = [
        {
            "name": "成都休闲游",
            "destination": "成都",
            "days": 3,
            "budget": 3500,
            "travel_style": "leisure",
            "departure": "上海"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"测试 {i}/{len(test_cases)}: {test_case['name']}")
        print(f"{'=' * 60}")
        print(f"  目的地: {test_case['destination']}")
        print(f"  天数: {test_case['days']}")
        print(f"  预算: ¥{test_case['budget']}")
        print(f"  风格: {test_case['travel_style']}")

        try:
            print(f"\n⏳ 正在调用AI生成行程，请稍候（10-30秒）...")

            # 调用AI生成
            result = await agent.generate_itinerary(
                destination=test_case['destination'],
                days=test_case['days'],
                budget=test_case['budget'],
                travel_style=test_case['travel_style'],
                departure=test_case['departure']
            )

            print(f"\n✅ AI生成成功！")

            # 显示基本信息
            print(f"\n📋 基本信息:")
            print(f"  标题: {result.get('title')}")
            print(f"  概述: {result.get('summary')}")

            # 显示亮点
            highlights = result.get('highlights', [])
            if highlights:
                print(f"\n✨ 行程亮点:")
                for highlight in highlights:
                    print(f"    • {highlight}")

            # 显示最佳季节和天气
            if result.get('best_season'):
                print(f"\n📅 最佳季节: {result['best_season']}")
            if result.get('weather'):
                print(f"🌤️  天气提示: {result['weather']}")

            # 显示行前准备
            preparation = result.get('preparation', {})
            if preparation:
                print(f"\n🎒 行前准备:")
                if preparation.get('documents'):
                    print(f"  📄 必备证件: {', '.join(preparation['documents'])}")
                if preparation.get('essentials'):
                    print(f"  🔧 必带物品: {', '.join(preparation['essentials'])}")
                if preparation.get('suggestions'):
                    print(f"  💡 建议携带: {', '.join(preparation['suggestions'])}")
                if preparation.get('booking_reminders'):
                    print(f"  ⏰ 预订提醒:")
                    for reminder in preparation['booking_reminders']:
                        print(f"      • {reminder}")

            # 显示实用提示
            tips = result.get('tips', {})
            if tips:
                print(f"\n💡 实用提示:")
                if tips.get('transportation'):
                    print(f"  🚗 交通: {tips['transportation']}")
                if tips.get('accommodation'):
                    print(f"  🏨 住宿: {tips['accommodation']}")
                if tips.get('food'):
                    print(f"  🍜 餐饮: {tips['food']}")
                if tips.get('shopping'):
                    print(f"  🛍️ 购物: {tips['shopping']}")
                if tips.get('safety'):
                    print(f"  ⚠️ 安全: {tips['safety']}")
                if tips.get('other'):
                    print(f"  📝 其他:")
                    for other_tip in tips['other']:
                        print(f"      • {other_tip}")

            # 显示费用明细
            cost_breakdown = result.get('cost_breakdown')
            if cost_breakdown:
                print(f"\n💰 费用明细:")
                print(f"  交通: ¥{cost_breakdown.get('transportation', 0)}")
                print(f"  住宿: ¥{cost_breakdown.get('accommodation', 0)}")
                print(f"  餐饮: ¥{cost_breakdown.get('food', 0)}")
                print(f"  门票: ¥{cost_breakdown.get('tickets', 0)}")
                print(f"  购物: ¥{cost_breakdown.get('shopping', 0)}")
                print(f"  其他: ¥{cost_breakdown.get('other', 0)}")
                print(f"  总计: ¥{result.get('actual_cost', 0)}")

            # 显示每日行程
            days = result.get('days', [])
            if days:
                print(f"\n📅 每日行程 (共{len(days)}天):")
                for day in days:
                    print(f"\n  第{day.get('day_number')}天: {day.get('title')}")
                    if day.get('summary'):
                        print(f"    概述: {day['summary']}")

                    activities = day.get('activities', [])
                    if activities:
                        print(f"    活动 ({len(activities)}个):")

                        # 显示前3个活动详情
                        for j, activity in enumerate(activities[:3], 1):
                            print(f"\n    {j}. {activity.get('title', '未知活动')}")
                            print(f"       ⏰ 时间: {activity.get('time', '未指定')}")
                            print(f"       📍 类型: {activity.get('type', '未分类')}")

                            # V2新增字段
                            if activity.get('highlights'):
                                print(f"       ⭐ 推荐: {', '.join(activity['highlights'][:2])}")

                            if activity.get('type') == 'attraction':
                                if activity.get('ticket_price') is not None:
                                    print(f"       🎫 门票: ¥{activity['ticket_price']}")
                                if activity.get('need_booking'):
                                    print(f"       📝 预订: {activity.get('booking_info', '需要预订')}")
                                if activity.get('best_time'):
                                    print(f"       ⏰ 最佳时间: {activity['best_time']}")

                            if activity.get('type') == 'meal':
                                if activity.get('cuisine'):
                                    print(f"       🍽️ 菜系: {activity['cuisine']}")
                                if activity.get('recommended_dishes'):
                                    print(f"       🥢 必点: {', '.join(activity['recommended_dishes'][:3])}")
                                if activity.get('wait_time'):
                                    print(f"       ⏳ 排队: {activity['wait_time']}")
                                if activity.get('opening_hours'):
                                    print(f"       🕐 营业: {activity['opening_hours']}")

                            if activity.get('tips'):
                                print(f"       💡 提示: {activity['tips'][0]}")

                        if len(activities) > 3:
                            print(f"\n    ... 还有 {len(activities) - 3} 个活动")

                    if day.get('total_cost'):
                        print(f"    💵 当日花费: ¥{day['total_cost']}")

                    if day.get('notes'):
                        print(f"    📝 备注: {day['notes']}")

            # 质量评估
            print(f"\n{'=' * 60}")
            print(f"📊 质量评估:")

            score = 0
            total = 100

            # 基本信息 (20分)
            if result.get('title') and result.get('summary'):
                print(f"  ✅ 基本信息完整 (+20分)")
                score += 20

            # 亮点 (15分)
            if result.get('highlights'):
                print(f"  ✅ 有行程亮点 (+15分)")
                score += 15

            # 行前准备 (20分)
            prep = result.get('preparation', {})
            if prep.get('documents') and prep.get('essentials'):
                print(f"  ✅ 行前准备完整 (+20分)")
                score += 20

            # 实用提示 (20分)
            tips = result.get('tips', {})
            if tips.get('transportation') or tips.get('food'):
                print(f"  ✅ 有实用提示 (+20分)")
                score += 20

            # 每日活动 (15分)
            if result.get('days') and len(result['days']) > 0:
                avg_activities = sum(len(d.get('activities', [])) for d in result['days']) / len(result['days'])
                if avg_activities >= 3:
                    print(f"  ✅ 每日活动充足 (平均{avg_activities:.1f}个) (+15分)")
                    score += 15
                else:
                    print(f"  ⚠️ 每日活动偏少 (平均{avg_activities:.1f}个) (+{int(avg_activities*5)}分)")
                    score += int(avg_activities * 5)

            # 活动详情 (10分)
            has_details = False
            for day in result.get('days', []):
                for activity in day.get('activities', []):
                    if activity.get('highlights') or activity.get('tips'):
                        has_details = True
                        break
                if has_details:
                    break

            if has_details:
                print(f"  ✅ 活动包含详细信息 (+10分)")
                score += 10

            print(f"\n  总分: {score}/100 ({score}%)")

            if score >= 90:
                print(f"  🌟 评级: 优秀")
            elif score >= 70:
                print(f"  👍 评级: 良好")
            elif score >= 50:
                print(f"  👌 评级: 一般")
            else:
                print(f"  ⚠️ 评级: 需要改进")

            # 保存结果
            result_dir = backend_dir / "test_results"
            result_dir.mkdir(exist_ok=True)
            result_file = result_dir / f"ai_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "test_time": datetime.now().isoformat(),
                    "test_case": test_case,
                    "result": result,
                    "quality_score": score
                }, f, ensure_ascii=False, indent=2)

            print(f"\n💾 结果已保存到: {result_file}")

        except Exception as e:
            print(f"\n❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 80}")
    print(f"🎉 测试完成！")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    asyncio.run(test_ai_generation_only())
