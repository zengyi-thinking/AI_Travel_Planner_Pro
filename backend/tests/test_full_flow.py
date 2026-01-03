"""
完整流程测试：AI生成行程 → 保存到数据库 → 读取验证
"""

import asyncio
import sys
import json
from pathlib import Path

# Windows UTF-8编码支持
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.db.session import get_db
from app.modules.users.models.user import User
from app.modules.planner.services.plan_service import PlanService
from app.modules.planner.daos.plan_dao import PlanDAO
from sqlalchemy import select


async def test_full_flow():
    """测试完整流程：AI生成 → 数据库保存 → 读取验证"""

    print("=" * 80)
    print("完整流程测试：AI生成行程 → 保存到数据库 → 读取验证")
    print("=" * 80)

    # 获取数据库会话
    async for db in get_db():
        try:
            # 1. 创建或获取测试用户
            print("\n[步骤1] 查找/创建测试用户...")
            result = await db.execute(
                select(User).where(User.email == "test@example.com")
            )
            user = result.scalar_one_or_none()

            if not user:
                print("  创建新用户: test@example.com")
                user = User(
                    email="test@example.com",
                    hashed_password="test_hash",
                    name="测试用户",
                    is_active=True,
                    membership_level="free"
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
            else:
                print(f"  使用现有用户: {user.name} (ID: {user.id})")

            user_id = user.id

            # 2. 使用AI生成行程
            print("\n[步骤2] 使用AI生成行程...")
            plan_service = PlanService(db)

            from app.modules.planner.schemas.plan_schema import PlanCreate

            # 先创建基础行程
            itinerary_data = PlanCreate(
                title="成都3日休闲游",
                destination="成都",
                days=3,
                budget=3500,
                travel_style="leisure",
                departure="上海"
            )

            print(f"  目的地: {itinerary_data.destination}")
            print(f"  天数: {itinerary_data.days}天")
            print(f"  预算: ¥{itinerary_data.budget}")
            print(f"  风格: {itinerary_data.travel_style}")
            print(f"  出发地: {itinerary_data.departure}")

            print("\n  步骤2.1: 创建基础行程...")
            base_itinerary = await plan_service.generate_itinerary(user_id, itinerary_data)
            itinerary_id = base_itinerary.id
            print(f"  ✓ 基础行程已创建 (ID: {itinerary_id})")

            print("\n  步骤2.2: 使用AI生成详细行程...")
            result = await plan_service.generate_detailed_itinerary(
                user_id=user_id,
                itinerary_id=itinerary_id
            )

            itinerary_id = result.id
            print(f"\n  ✓ 详细行程已保存到数据库 (ID: {itinerary_id})")

            # 3. 从数据库读取验证
            print("\n[步骤3] 从数据库读取验证...")
            plan_dao = PlanDAO(db)
            retrieved = await plan_dao.get_plan_by_id(itinerary_id, user_id)

            if retrieved:
                print(f"  标题: {retrieved.title}")
                print(f"  目的地: {retrieved.destination}")
                print(f"  天数: {retrieved.days}")
                print(f"  预算: ¥{retrieved.budget}")
                print(f"  状态: {retrieved.status}")
                print(f"  AI生成: {retrieved.ai_generated}")

                # 检查metadata
                if retrieved.metadata_json:
                    metadata = retrieved.metadata_json
                    print(f"\n  行程摘要: {metadata.get('summary', 'N/A')[:50]}...")
                    print(f"  亮点数量: {len(metadata.get('highlights', []))}")
                    print(f"  实际花费: ¥{metadata.get('actual_cost', 'N/A')}")

                    # 检查preparation
                    prep = metadata.get('preparation', {})
                    if prep:
                        print(f"\n  准备事项:")
                        print(f"    必备证件: {len(prep.get('documents', []))}项")
                        print(f"    必备物品: {len(prep.get('essentials', []))}项")

                # 检查每日详情
                if retrieved.days_detail:
                    print(f"\n  每日行程:")
                    for day in retrieved.days_detail:
                        activities_count = len(day.activities) if day.activities else 0
                        print(f"    第{day.day_number}天: {day.title} ({activities_count}个活动)")
            else:
                print("  ✗ 未找到行程数据")
                return False

            # 4. 保存测试结果到文件
            print("\n[步骤4] 保存测试结果...")

            test_result = {
                "test_time": str(asyncio.get_event_loop().time()),
                "success": True,
                "user_id": user_id,
                "itinerary_id": itinerary_id,
                "itinerary": {
                    "title": retrieved.title,
                    "destination": retrieved.destination,
                    "days": retrieved.days,
                    "budget": float(retrieved.budget) if retrieved.budget else 0,
                    "status": retrieved.status,
                    "ai_generated": retrieved.ai_generated,
                    "metadata": retrieved.metadata_json,
                    "days_count": len(retrieved.days_detail) if retrieved.days_detail else 0
                },
                "input_data": {
                    "destination": itinerary_data.destination,
                    "days": itinerary_data.days,
                    "budget": float(itinerary_data.budget),
                    "travel_style": itinerary_data.travel_style,
                    "departure": itinerary_data.departure
                }
            }

            result_dir = backend_dir / "test_results"
            result_dir.mkdir(exist_ok=True)
            result_file = result_dir / f"full_flow_result_{itinerary_id}.json"

            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(test_result, f, ensure_ascii=False, indent=2)

            print(f"  ✓ 测试结果已保存到: {result_file}")

            # 5. 验证数据完整性
            print("\n[步骤5] 验证数据完整性...")

            checks = {
                "行程基本信息": bool(retrieved.title and retrieved.destination),
                "每日详情": bool(retrieved.days_detail and len(retrieved.days_detail) == itinerary_data.days),
                "元数据(摘要)": bool(retrieved.metadata_json and retrieved.metadata_json.get('summary')),
                "元数据(亮点)": bool(retrieved.metadata_json and retrieved.metadata_json.get('highlights')),
                "元数据(准备事项)": bool(retrieved.metadata_json and retrieved.metadata_json.get('preparation')),
                "元数据(提示)": bool(retrieved.metadata_json and retrieved.metadata_json.get('tips')),
            }

            all_passed = True
            for check_name, passed in checks.items():
                status = "✓" if passed else "✗"
                print(f"  {status} {check_name}")
                if not passed:
                    all_passed = False

            print("\n" + "=" * 80)
            if all_passed:
                print("✓ 完整流程测试成功！所有检查项都通过。")
            else:
                print("⚠ 测试完成，但部分检查项未通过。")
            print("=" * 80)

            return all_passed

        except Exception as e:
            print(f"\n✗ 错误: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = asyncio.run(test_full_flow())
    sys.exit(0 if success else 1)
